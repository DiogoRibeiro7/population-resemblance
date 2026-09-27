"""Tests for the Population Resemblance Statistic."""

from __future__ import annotations

import math

import pytest

from population_resemblance import population_resemblance_statistic


def test_identical_distributions_have_zero_prs() -> None:
    """PRS must be zero when the observed and reference distributions are identical."""
    result = population_resemblance_statistic(
        observed=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
    )

    assert result == pytest.approx(0.0)


def test_prs_matches_manual_calculation() -> None:
    """PRS must match the defining Pearson-type discrepancy."""
    observed = [0.4, 0.35, 0.25]
    reference = [0.5, 0.3, 0.2]

    expected = sum(
        (observed_value - reference_value) ** 2 / reference_value
        for observed_value, reference_value in zip(observed, reference, strict=True)
    )

    result = population_resemblance_statistic(observed=observed, reference=reference)

    assert math.isfinite(result)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    ("observed", "reference"),
    [
        ([0.5, 0.5], [1.0, 0.0]),
        ([0.5, 0.4], [0.5, 0.5]),
        ([0.5, 0.5], [0.5, 0.4]),
        ([0.5, -0.5, 1.0], [0.5, 0.25, 0.25]),
        ([1.0], [1.0]),
    ],
)
def test_invalid_inputs_raise_value_error(
    observed: list[float],
    reference: list[float],
) -> None:
    """Invalid distributions must fail explicitly rather than producing misleading results."""
    with pytest.raises(ValueError):
        population_resemblance_statistic(observed=observed, reference=reference)
