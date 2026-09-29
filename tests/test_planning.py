"""Tests for structural PRS sample-size planning."""

from __future__ import annotations

import pytest

from population_resemblance import (
    minimum_structural_sample_size,
    recommended_delta,
)


def test_balanced_reference_minimum_is_exact() -> None:
    """Balanced five-category example should have an exact structural minimum."""
    reference = [0.2] * 5
    sample_size = minimum_structural_sample_size(reference, c=0.7, m=2.0)

    assert sample_size == 8
    assert 2.0 * recommended_delta(reference, sample_size, c=0.7) <= 0.2
    assert 2.0 * recommended_delta(reference, sample_size - 1, c=0.7) > 0.2


def test_imbalanced_reference_minimum_is_exact() -> None:
    """The smallest reference category should tighten the structural bound."""
    reference = [0.8, 0.1, 0.1]
    sample_size = minimum_structural_sample_size(reference, c=0.7, m=2.0)

    assert sample_size == 18
    assert 2.0 * recommended_delta(reference, sample_size, c=0.7) <= 0.1
    assert 2.0 * recommended_delta(reference, sample_size - 1, c=0.7) > 0.1


def test_planner_matches_direct_constraint_for_custom_parameters() -> None:
    """Returned n should satisfy the bound while n-1 should violate it."""
    reference = [0.5, 0.3, 0.2]
    c = 0.9
    m = 1.5

    sample_size = minimum_structural_sample_size(reference, c=c, m=m)
    minimum_probability = min(reference)

    assert m * recommended_delta(reference, sample_size, c=c) <= minimum_probability
    if sample_size > 1:
        assert (
            m * recommended_delta(reference, sample_size - 1, c=c)
            > minimum_probability
        )


@pytest.mark.parametrize(
    ("reference", "c", "m"),
    [
        ([0.5, 0.4], 0.7, 2.0),
        ([0.5, 0.5], 0.0, 2.0),
        ([0.5, 0.5], 0.7, 1.0),
        ([0.5, 0.5], 0.7, float("inf")),
    ],
)
def test_invalid_planning_inputs_raise(
    reference: list[float],
    c: float,
    m: float,
) -> None:
    """Planning validation should match the calibration framework."""
    with pytest.raises(ValueError):
        minimum_structural_sample_size(reference, c=c, m=m)
