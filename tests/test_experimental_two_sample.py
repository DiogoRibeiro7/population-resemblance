"""Tests for the experimental independent two-sample API."""

from __future__ import annotations

import pytest

import population_resemblance
from population_resemblance.experimental import (
    ExperimentalTwoSampleResult,
    assess_independent_two_sample_resemblance,
)
from population_resemblance.result import DecisionRegion


def test_identical_well_populated_samples_are_r1() -> None:
    """Identical supported samples should produce zero statistic and R1."""
    result = assess_independent_two_sample_resemblance(
        [40, 30, 20, 10],
        [40, 30, 20, 10],
        samples_are_independent=True,
    )

    assert isinstance(result, ExperimentalTwoSampleResult)
    assert result.statistic == pytest.approx(0.0)
    assert result.region is DecisionRegion.R1
    assert result.effective_sample_size == pytest.approx(50.0)
    assert result.minimum_expected_count == pytest.approx(10.0)


def test_statistic_matches_two_sample_pearson_identity() -> None:
    """Experimental statistic should equal the pooled Pearson quadratic form."""
    first = [44, 31, 25]
    second = [192, 123, 85]

    result = assess_independent_two_sample_resemblance(
        first,
        second,
        samples_are_independent=True,
    )

    n = sum(first)
    second_n = sum(second)
    pooled = [
        (first[index] + second[index]) / (n + second_n)
        for index in range(3)
    ]
    first_p = [value / n for value in first]
    second_p = [value / second_n for value in second]
    n_eff = n * second_n / (n + second_n)
    expected = n_eff * sum(
        (first_p[index] - second_p[index]) ** 2 / pooled[index]
        for index in range(3)
    )

    assert result.statistic == pytest.approx(expected)


def test_zero_pooled_category_is_rejected() -> None:
    """Zero pooled cells must fail instead of being smoothed or dropped."""
    with pytest.raises(ValueError, match="zero_pooled_category"):
        assess_independent_two_sample_resemblance(
            [40, 30, 30, 0],
            [35, 35, 30, 0],
            samples_are_independent=True,
        )


def test_sparse_expected_count_is_rejected() -> None:
    """Sparse pooled categories must fail the explicit support policy."""
    with pytest.raises(ValueError, match="insufficient_expected_count"):
        assess_independent_two_sample_resemblance(
            [70, 15, 8, 5, 2],
            [69, 16, 8, 5, 2],
            samples_are_independent=True,
        )


def test_dependent_samples_are_explicitly_unsupported() -> None:
    """The experimental API must not silently accept dependent samples."""
    with pytest.raises(ValueError, match="independent samples only"):
        assess_independent_two_sample_resemblance(
            [40, 30, 20, 10],
            [40, 30, 20, 10],
            samples_are_independent=False,
        )


def test_structural_bound_is_enforced_for_explicit_delta() -> None:
    """An explicit tolerance must keep the wider region inside the simplex."""
    with pytest.raises(ValueError, match="structural_probability_bound"):
        assess_independent_two_sample_resemblance(
            [40, 30, 20, 10],
            [40, 30, 20, 10],
            samples_are_independent=True,
            delta=0.15,
            m=2.0,
        )


def test_experimental_api_is_not_root_exported() -> None:
    """Experimental symbols must not enter the stable root compatibility surface."""
    assert "ExperimentalTwoSampleResult" not in population_resemblance.__all__
    assert (
        "assess_independent_two_sample_resemblance"
        not in population_resemblance.__all__
    )
