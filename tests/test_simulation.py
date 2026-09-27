"""Tests for Monte Carlo PRS simulation utilities."""

from __future__ import annotations

import pytest

from population_resemblance import (
    recommended_delta,
    simulate_region_probabilities,
    symmetric_category_shift,
)


def test_symmetric_category_shift_even_categories() -> None:
    """Even category counts should shift equal halves in opposite directions."""
    shifted = symmetric_category_shift([0.25, 0.25, 0.25, 0.25], 0.05)

    assert shifted.tolist() == pytest.approx([0.20, 0.20, 0.30, 0.30])
    assert float(shifted.sum()) == pytest.approx(1.0)


def test_symmetric_category_shift_odd_categories() -> None:
    """The middle category should remain unchanged for odd category counts."""
    shifted = symmetric_category_shift([0.2] * 5, 0.03)

    assert shifted.tolist() == pytest.approx([0.17, 0.17, 0.20, 0.23, 0.23])


def test_simulation_is_reproducible_with_seed() -> None:
    """A fixed seed should make the Monte Carlo result exactly reproducible."""
    first = simulate_region_probabilities(
        current=[0.40, 0.35, 0.25],
        reference=[0.50, 0.30, 0.20],
        sample_size=250,
        simulations=2_000,
        seed=1234,
    )
    second = simulate_region_probabilities(
        current=[0.40, 0.35, 0.25],
        reference=[0.50, 0.30, 0.20],
        sample_size=250,
        simulations=2_000,
        seed=1234,
    )

    assert first == second


def test_region_probabilities_sum_to_one() -> None:
    """Every simulated sample must belong to exactly one decision region."""
    result = simulate_region_probabilities(
        current=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
        sample_size=200,
        simulations=5_000,
        seed=7,
    )

    assert sum(result.probabilities) == pytest.approx(1.0)


def test_source_boundary_behavior_at_delta() -> None:
    """At the delta boundary, the empirical R3 rate should be close to alpha1."""
    reference = [0.2] * 5
    sample_size = 50
    delta = recommended_delta(reference, sample_size, c=0.7)
    current = symmetric_category_shift(reference, delta)

    result = simulate_region_probabilities(
        current=current,
        reference=reference,
        sample_size=sample_size,
        simulations=30_000,
        seed=123,
        delta=delta,
        m=2.0,
        alpha1=0.05,
        alpha2=0.10,
    )

    assert result.r3_probability == pytest.approx(0.05, abs=0.015)


def test_source_boundary_behavior_at_m_delta() -> None:
    """At the M-delta boundary, the empirical R1 rate should be close to alpha2."""
    reference = [0.2] * 5
    sample_size = 50
    delta = recommended_delta(reference, sample_size, c=0.7)
    current = symmetric_category_shift(reference, 2.0 * delta)

    result = simulate_region_probabilities(
        current=current,
        reference=reference,
        sample_size=sample_size,
        simulations=30_000,
        seed=321,
        delta=delta,
        m=2.0,
        alpha1=0.05,
        alpha2=0.10,
    )

    assert result.r1_probability == pytest.approx(0.10, abs=0.02)


def test_invalid_simulation_count_raises() -> None:
    """Simulation count must be a positive integer."""
    with pytest.raises((TypeError, ValueError)):
        simulate_region_probabilities(
            current=[0.5, 0.5],
            reference=[0.5, 0.5],
            sample_size=100,
            simulations=0,
            seed=1,
        )


def test_invalid_seed_raises() -> None:
    """Seed must be an integer or None."""
    with pytest.raises(TypeError):
        simulate_region_probabilities(
            current=[0.5, 0.5],
            reference=[0.5, 0.5],
            sample_size=100,
            simulations=1_000,
            seed=1.5,  # type: ignore[arg-type]
        )
