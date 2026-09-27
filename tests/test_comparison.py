"""Tests for PRS versus PSI Monte Carlo comparison."""

from __future__ import annotations

import pytest

from population_resemblance import (
    simulate_prs_psi_comparison,
    symmetric_category_shift,
)


def test_comparison_probabilities_sum_to_one() -> None:
    """Both methods must classify every simulated sample exactly once."""
    result = simulate_prs_psi_comparison(
        current=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
        sample_size=200,
        simulations=2_000,
        seed=42,
    )

    assert result.prs.total == pytest.approx(1.0)
    assert result.psi.total == pytest.approx(1.0)


def test_comparison_is_reproducible() -> None:
    """A fixed seed should produce identical comparison results."""
    first = simulate_prs_psi_comparison(
        current=[0.4, 0.35, 0.25],
        reference=[0.5, 0.3, 0.2],
        sample_size=250,
        simulations=1_500,
        seed=7,
    )
    second = simulate_prs_psi_comparison(
        current=[0.4, 0.35, 0.25],
        reference=[0.5, 0.3, 0.2],
        sample_size=250,
        simulations=1_500,
        seed=7,
    )

    assert first == second


def test_small_sample_no_shift_shows_different_operating_behavior() -> None:
    """PRS and fixed PSI thresholds should not be expected to behave identically."""
    result = simulate_prs_psi_comparison(
        current=[0.2] * 5,
        reference=[0.2] * 5,
        sample_size=50,
        simulations=8_000,
        seed=123,
    )

    assert result.prs != result.psi


def test_shifted_population_produces_nonzero_alert_probabilities() -> None:
    """Both methods should produce some alerts under a sufficiently shifted population."""
    reference = [0.2] * 5
    current = symmetric_category_shift(reference, 0.06)

    result = simulate_prs_psi_comparison(
        current=current,
        reference=reference,
        sample_size=500,
        simulations=5_000,
        seed=99,
    )

    assert result.prs.amber + result.prs.red > 0.0
    assert result.psi.amber + result.psi.red > 0.0


@pytest.mark.parametrize(
    ("sample_size", "simulations"),
    [(0, 100), (100, 0)],
)
def test_invalid_simulation_parameters_raise(
    sample_size: int,
    simulations: int,
) -> None:
    """Invalid Monte Carlo configuration should fail explicitly."""
    with pytest.raises((TypeError, ValueError)):
        simulate_prs_psi_comparison(
            current=[0.5, 0.5],
            reference=[0.5, 0.5],
            sample_size=sample_size,
            simulations=simulations,
        )
