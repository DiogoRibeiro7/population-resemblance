"""Tests for count-based population resemblance assessment."""

from __future__ import annotations

import numpy as np
import pytest

from population_resemblance import (
    DecisionRegion,
    assess_population_counts,
    assess_population_resemblance,
    counts_to_proportions,
)


def test_counts_to_proportions() -> None:
    """Counts should be converted to a normalized empirical distribution."""
    proportions = counts_to_proportions([6, 9, 10, 11, 14])

    assert proportions.dtype == np.float64
    assert proportions.tolist() == pytest.approx([0.12, 0.18, 0.20, 0.22, 0.28])
    assert float(proportions.sum()) == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("counts", "expected_region", "expected_statistic"),
    [
        ([6, 9, 10, 11, 14], DecisionRegion.R1, 0.068),
        ([4, 10, 11, 11, 14], DecisionRegion.R2, 0.108),
        ([2, 5, 13, 14, 16], DecisionRegion.R3, 0.300),
    ],
)
def test_count_api_reproduces_selected_table_3a_examples(
    counts: list[int],
    expected_region: DecisionRegion,
    expected_statistic: float,
) -> None:
    """Count inputs should reproduce the paper's selected small-sample examples."""
    result = assess_population_counts(counts=counts, reference=[0.2] * 5)

    assert result.sample_size == 50
    assert result.statistic == pytest.approx(expected_statistic, abs=5e-4)
    assert result.region is expected_region


def test_count_and_probability_apis_are_equivalent() -> None:
    """Count and probability APIs should agree for the same observed sample."""
    counts = [40, 35, 25]
    reference = [0.50, 0.30, 0.20]

    from_counts = assess_population_counts(counts=counts, reference=reference)
    from_probabilities = assess_population_resemblance(
        observed=[0.40, 0.35, 0.25],
        reference=reference,
        sample_size=100,
    )

    assert from_counts == from_probabilities


@pytest.mark.parametrize(
    "counts",
    [
        [0, 0, 0],
        [1, -1, 2],
        [1],
        [1.0, 2.0, 3.0],
        [True, False],
    ],
)
def test_invalid_counts_raise(counts: list[object]) -> None:
    """Malformed count vectors should fail before statistical assessment."""
    with pytest.raises((TypeError, ValueError)):
        counts_to_proportions(counts)  # type: ignore[arg-type]


def test_count_api_rejects_category_mismatch() -> None:
    """Observed counts and reference probabilities must have matching dimensions."""
    with pytest.raises(ValueError, match="same number of categories"):
        assess_population_counts(
            counts=[10, 20, 30],
            reference=[0.5, 0.5],
        )
