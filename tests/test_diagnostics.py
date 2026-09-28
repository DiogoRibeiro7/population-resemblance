"""Tests for category-level PRS diagnostics."""

from __future__ import annotations

import pytest

from population_resemblance import (
    population_count_diagnostics,
    population_resemblance_diagnostics,
    population_resemblance_statistic,
)


def test_contributions_sum_to_prs() -> None:
    """Category contributions must decompose the complete PRS statistic."""
    observed = [0.40, 0.35, 0.25]
    reference = [0.50, 0.30, 0.20]

    diagnostics = population_resemblance_diagnostics(observed, reference)
    statistic = population_resemblance_statistic(observed, reference)

    assert diagnostics.statistic == pytest.approx(statistic)
    assert sum(
        item.prs_contribution for item in diagnostics.categories
    ) == pytest.approx(statistic)
    assert sum(
        item.contribution_share for item in diagnostics.categories
    ) == pytest.approx(1.0)


def test_signed_and_absolute_shifts_are_reported() -> None:
    """Diagnostics should preserve both shift direction and magnitude."""
    diagnostics = population_resemblance_diagnostics(
        observed=[0.40, 0.35, 0.25],
        reference=[0.50, 0.30, 0.20],
        labels=["low", "medium", "high"],
    )

    first = diagnostics.categories[0]
    assert first.category == "low"
    assert first.signed_shift == pytest.approx(-0.10)
    assert first.absolute_shift == pytest.approx(0.10)


def test_largest_contributor_is_identified() -> None:
    """The largest PRS contribution should be easy to identify."""
    diagnostics = population_resemblance_diagnostics(
        observed=[0.35, 0.35, 0.30],
        reference=[0.50, 0.30, 0.20],
        labels=["a", "b", "c"],
    )

    assert diagnostics.largest_contributor.category == "a"
    assert diagnostics.maximum_absolute_shift == pytest.approx(0.15)


def test_identical_distributions_have_zero_contribution_shares() -> None:
    """Zero PRS should not produce undefined contribution shares."""
    diagnostics = population_resemblance_diagnostics(
        observed=[0.5, 0.3, 0.2],
        reference=[0.5, 0.3, 0.2],
    )

    assert diagnostics.statistic == pytest.approx(0.0)
    assert all(
        item.contribution_share == pytest.approx(0.0)
        for item in diagnostics.categories
    )


def test_count_diagnostics_match_probability_diagnostics() -> None:
    """Count and probability diagnostics should agree for the same sample."""
    from_counts = population_count_diagnostics(
        counts=[40, 35, 25],
        reference=[0.50, 0.30, 0.20],
    )
    from_probabilities = population_resemblance_diagnostics(
        observed=[0.40, 0.35, 0.25],
        reference=[0.50, 0.30, 0.20],
    )

    assert from_counts == from_probabilities


def test_label_mismatch_raises() -> None:
    """Category labels must align exactly with the probability vectors."""
    with pytest.raises(ValueError, match="labels"):
        population_resemblance_diagnostics(
            observed=[0.5, 0.5],
            reference=[0.5, 0.5],
            labels=["only-one"],
        )
