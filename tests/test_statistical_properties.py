"""Generated invariant tests for statistical properties.

These tests use deterministic pseudo-random generators instead of an additional
property-testing dependency so failures remain fully reproducible.
"""

from __future__ import annotations

import numpy as np
import pytest

from population_resemblance import (
    minimum_structural_sample_size,
    population_resemblance_diagnostics,
    population_resemblance_statistic,
    recommended_delta,
    simulate_region_probabilities,
    symmetric_category_shift,
)
from population_resemblance.experimental import (
    assess_independent_two_sample_resemblance,
)


def _random_probability_vector(
    rng: np.random.Generator,
    categories: int,
) -> np.ndarray:
    """Generate a strictly positive probability vector."""
    raw = rng.uniform(0.05, 1.0, size=categories)
    return raw / np.sum(raw)


def test_prs_is_non_negative_for_generated_distributions() -> None:
    """PRS must never be negative."""
    rng = np.random.default_rng(20260930)

    for categories in range(2, 11):
        for _ in range(25):
            reference = _random_probability_vector(rng, categories)
            observed = _random_probability_vector(rng, categories)

            statistic = population_resemblance_statistic(
                observed=observed,
                reference=reference,
            )

            assert statistic >= 0.0


def test_prs_is_zero_for_identical_generated_distributions() -> None:
    """PRS must be zero when observed and reference probabilities match."""
    rng = np.random.default_rng(20260931)

    for categories in range(2, 11):
        for _ in range(20):
            reference = _random_probability_vector(rng, categories)

            statistic = population_resemblance_statistic(
                observed=reference,
                reference=reference,
            )

            assert statistic == pytest.approx(0.0, abs=1e-15)


def test_diagnostic_contributions_sum_to_prs() -> None:
    """Generated category contributions must reconstruct the total PRS."""
    rng = np.random.default_rng(20260932)

    for categories in range(2, 9):
        for _ in range(20):
            reference = _random_probability_vector(rng, categories)
            observed = _random_probability_vector(rng, categories)

            diagnostics = population_resemblance_diagnostics(
                observed=observed,
                reference=reference,
            )

            contribution_sum = sum(
                item.prs_contribution for item in diagnostics.categories
            )

            assert contribution_sum == pytest.approx(
                diagnostics.statistic,
                rel=1e-12,
                abs=1e-15,
            )


def test_symmetric_shift_preserves_probability_mass() -> None:
    """Valid generated symmetric shifts must remain probability distributions."""
    rng = np.random.default_rng(20260933)

    for categories in range(2, 10):
        reference = np.full(categories, 1.0 / categories)
        max_deviation = 0.9 / categories

        for _ in range(20):
            deviation = float(rng.uniform(0.0, max_deviation))
            shifted = symmetric_category_shift(reference, deviation)

            assert np.all(shifted >= 0.0)
            assert np.all(shifted <= 1.0)
            assert float(np.sum(shifted)) == pytest.approx(1.0, abs=1e-12)


def test_region_probabilities_sum_to_one_for_generated_cases() -> None:
    """Monte Carlo classification probabilities must form a partition."""
    rng = np.random.default_rng(20260934)

    for categories in (2, 3, 5, 8):
        reference = np.full(categories, 1.0 / categories)

        for index in range(5):
            deviation = float(rng.uniform(0.0, 0.15 / categories))
            current = symmetric_category_shift(reference, deviation)

            result = simulate_region_probabilities(
                current=current,
                reference=reference,
                sample_size=250,
                simulations=750,
                seed=1000 + categories * 10 + index,
                batch_size=113,
            )

            assert sum(result.probabilities) == pytest.approx(1.0, abs=1e-15)


def test_chunked_and_single_batch_preserve_classifications() -> None:
    """Chunking must not change seeded R1/R2/R3 frequencies."""
    rng = np.random.default_rng(20260935)

    for categories in (3, 5, 7):
        reference = np.full(categories, 1.0 / categories)
        deviation = float(rng.uniform(0.0, 0.08 / categories))
        current = symmetric_category_shift(reference, deviation)

        full = simulate_region_probabilities(
            current=current,
            reference=reference,
            sample_size=200,
            simulations=1003,
            seed=categories,
        )
        chunked = simulate_region_probabilities(
            current=current,
            reference=reference,
            sample_size=200,
            simulations=1003,
            seed=categories,
            batch_size=127,
        )

        assert chunked.probabilities == full.probabilities


def test_sample_size_planner_returns_minimal_feasible_integer() -> None:
    """Generated planning results must satisfy the bound minimally."""
    rng = np.random.default_rng(20260936)

    for categories in range(2, 8):
        for _ in range(15):
            reference = _random_probability_vector(rng, categories)
            c = float(rng.uniform(0.3, 1.2))
            m = float(rng.uniform(1.1, 2.5))

            sample_size = minimum_structural_sample_size(
                reference,
                c=c,
                m=m,
            )
            minimum_probability = float(np.min(reference))

            assert (
                m * recommended_delta(reference, sample_size, c=c)
                <= minimum_probability + 1e-15
            )
            if sample_size > 1:
                assert (
                    m * recommended_delta(reference, sample_size - 1, c=c)
                    > minimum_probability - 1e-15
                )


def test_two_sample_statistic_matches_pearson_identity_for_generated_tables() -> None:
    """Experimental two-sample statistic must match Pearson algebraically."""
    rng = np.random.default_rng(20260937)

    for categories in (2, 3, 5, 7):
        for _ in range(20):
            # Keep all cells comfortably above the sparse-category support rule.
            first = rng.integers(20, 100, size=categories)
            second = rng.integers(20, 120, size=categories)

            result = assess_independent_two_sample_resemblance(
                first,
                second,
                samples_are_independent=True,
            )

            n = int(np.sum(first))
            m = int(np.sum(second))
            pooled = (first + second) / float(n + m)
            p_hat = first / float(n)
            q_hat = second / float(m)
            n_eff = n * m / float(n + m)

            expected = n_eff * float(
                np.sum(np.square(p_hat - q_hat) / pooled)
            )

            assert result.statistic == pytest.approx(
                expected,
                rel=1e-12,
                abs=1e-15,
            )


@pytest.mark.parametrize(
    "invalid",
    [
        [0.6, 0.6],
        [0.8, -0.2, 0.4],
        [1.0],
        [0.0, 1.0],
    ],
)
def test_invalid_probability_vectors_are_rejected(
    invalid: list[float],
) -> None:
    """Generated-input coverage should include invalid simplex inputs."""
    with pytest.raises((TypeError, ValueError)):
        population_resemblance_statistic(
            observed=invalid,
            reference=[0.5, 0.5],
        )
