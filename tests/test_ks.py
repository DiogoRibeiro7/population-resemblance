"""Tests for the discrete Kolmogorov-Smirnov benchmark."""

from __future__ import annotations

import pytest

from population_resemblance import (
    discrete_ks_statistic,
    discrete_ks_status,
    discrete_ks_test_counts,
)


def test_identical_distributions_have_zero_ks_statistic() -> None:
    """The discrete KS statistic must vanish for identical distributions."""
    result = discrete_ks_statistic(
        observed=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
    )

    assert result == pytest.approx(0.0)


def test_ks_statistic_matches_manual_cumulative_difference() -> None:
    """The statistic should equal the largest cumulative probability gap."""
    result = discrete_ks_statistic(
        observed=[0.1, 0.2, 0.7],
        reference=[0.2, 0.3, 0.5],
    )

    assert result == pytest.approx(0.2)


def test_monte_carlo_ks_is_reproducible() -> None:
    """A fixed seed should reproduce the same calibrated result."""
    first = discrete_ks_test_counts(
        counts=[8, 12, 30],
        reference=[0.2, 0.3, 0.5],
        simulations=2_000,
        seed=123,
    )
    second = discrete_ks_test_counts(
        counts=[8, 12, 30],
        reference=[0.2, 0.3, 0.5],
        simulations=2_000,
        seed=123,
    )

    assert first == second


def test_extreme_shift_has_small_monte_carlo_p_value() -> None:
    """A large cumulative shift should be strongly inconsistent with the reference."""
    result = discrete_ks_test_counts(
        counts=[0, 0, 100],
        reference=[1 / 3, 1 / 3, 1 / 3],
        simulations=2_000,
        seed=7,
    )

    assert result.p_value < 0.01
    assert result.status == "red"


@pytest.mark.parametrize(
    ("p_value", "expected"),
    [
        (0.0, "red"),
        (0.0099, "red"),
        (0.01, "amber"),
        (0.10, "amber"),
        (0.1001, "green"),
        (1.0, "green"),
    ],
)
def test_default_status_thresholds(p_value: float, expected: str) -> None:
    """Default status thresholds should match the paper's comparison convention."""
    assert discrete_ks_status(p_value) == expected


def test_category_mismatch_raises() -> None:
    """Observed counts and reference probabilities must align by category."""
    with pytest.raises(ValueError, match="same number of categories"):
        discrete_ks_test_counts(
            counts=[10, 20, 30],
            reference=[0.5, 0.5],
        )


@pytest.mark.parametrize("simulations", [0, -1])
def test_invalid_simulation_count_raises(simulations: int) -> None:
    """Monte Carlo calibration requires a positive simulation count."""
    with pytest.raises(ValueError):
        discrete_ks_test_counts(
            counts=[10, 10],
            reference=[0.5, 0.5],
            simulations=simulations,
        )
