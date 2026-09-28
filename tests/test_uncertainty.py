"""Tests for Monte Carlo uncertainty summaries."""

from __future__ import annotations

import pytest

from population_resemblance import (
    simulate_region_probabilities,
    simulation_uncertainty,
)


def test_uncertainty_contains_simulated_estimates() -> None:
    """Each interval should contain its Monte Carlo point estimate."""
    result = simulate_region_probabilities(
        current=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
        sample_size=200,
        simulations=2_000,
        seed=123,
    )

    uncertainty = simulation_uncertainty(result)

    for interval in (uncertainty.r1, uncertainty.r2, uncertainty.r3):
        assert interval.lower <= interval.estimate <= interval.upper


def test_uncertainty_estimates_match_simulation_result() -> None:
    """Interval estimates should reproduce the simulation probabilities."""
    result = simulate_region_probabilities(
        current=[0.4, 0.35, 0.25],
        reference=[0.5, 0.3, 0.2],
        sample_size=250,
        simulations=1_500,
        seed=7,
    )

    uncertainty = simulation_uncertainty(result)

    assert uncertainty.r1.estimate == pytest.approx(result.r1_probability)
    assert uncertainty.r2.estimate == pytest.approx(result.r2_probability)
    assert uncertainty.r3.estimate == pytest.approx(result.r3_probability)


def test_larger_simulation_count_reduces_interval_width() -> None:
    """Wilson intervals should become narrower with more Monte Carlo samples."""
    small = simulate_region_probabilities(
        current=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
        sample_size=200,
        simulations=500,
        seed=3,
    )
    large = simulate_region_probabilities(
        current=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
        sample_size=200,
        simulations=5_000,
        seed=3,
    )

    small_interval = simulation_uncertainty(small).r1
    large_interval = simulation_uncertainty(large).r1

    assert (
        large_interval.upper - large_interval.lower
        < small_interval.upper - small_interval.lower
    )


@pytest.mark.parametrize("confidence_level", [0.0, 1.0, -0.1, 1.1])
def test_invalid_confidence_level_raises(confidence_level: float) -> None:
    """Confidence level must lie strictly between zero and one."""
    result = simulate_region_probabilities(
        current=[0.5, 0.5],
        reference=[0.5, 0.5],
        sample_size=100,
        simulations=100,
        seed=1,
    )

    with pytest.raises(ValueError):
        simulation_uncertainty(result, confidence_level=confidence_level)
