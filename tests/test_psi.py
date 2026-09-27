"""Tests for the Population Stability Index benchmark."""

from __future__ import annotations

import math

import pytest

from population_resemblance import lewis_psi_status, population_stability_index


def test_identical_distributions_have_zero_psi() -> None:
    """PSI must be zero for identical distributions."""
    result = population_stability_index(
        observed=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
    )

    assert result == pytest.approx(0.0)


def test_psi_matches_manual_calculation() -> None:
    """PSI should match its defining symmetrized log-ratio expression."""
    observed = [0.4, 0.35, 0.25]
    reference = [0.5, 0.3, 0.2]

    expected = sum(
        (observed_value - reference_value)
        * (math.log(observed_value) - math.log(reference_value))
        for observed_value, reference_value in zip(observed, reference, strict=True)
    )

    result = population_stability_index(observed=observed, reference=reference)

    assert result == pytest.approx(expected)


def test_zero_observed_category_is_omitted_per_source_definition() -> None:
    """Observed zero-probability categories follow the paper's indicator convention."""
    result = population_stability_index(
        observed=[0.0, 0.5, 0.5],
        reference=[0.2, 0.4, 0.4],
    )

    expected = 2 * ((0.5 - 0.4) * (math.log(0.5) - math.log(0.4)))
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    ("psi", "expected"),
    [
        (0.0, "green"),
        (0.099999, "green"),
        (0.10, "amber"),
        (0.249999, "amber"),
        (0.25, "red"),
        (0.40, "red"),
    ],
)
def test_lewis_thresholds(psi: float, expected: str) -> None:
    """Lewis benchmark thresholds should preserve their conventional boundaries."""
    assert lewis_psi_status(psi) == expected


@pytest.mark.parametrize("psi", [-0.01, float("nan"), float("inf")])
def test_invalid_psi_status_input_raises(psi: float) -> None:
    """Invalid PSI values should fail explicitly."""
    with pytest.raises(ValueError):
        lewis_psi_status(psi)


def test_reference_zero_probability_is_rejected() -> None:
    """PSI cannot be evaluated with zero reference probability."""
    with pytest.raises(ValueError):
        population_stability_index(
            observed=[0.5, 0.5],
            reference=[1.0, 0.0],
        )
