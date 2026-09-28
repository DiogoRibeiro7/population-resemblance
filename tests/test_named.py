"""Tests for named-category population monitoring."""

from __future__ import annotations

import pytest

from population_resemblance import assess_named_population, population_resemblance_statistic


def test_named_api_aligns_counts_to_reference_order() -> None:
    """Count mappings should be reordered to match the reference mapping."""
    result = assess_named_population(
        counts={"high": 25, "low": 40, "medium": 35},
        reference={"low": 0.50, "medium": 0.30, "high": 0.20},
        ks_simulations=1_000,
        ks_seed=123,
    )

    assert result.categories == ("low", "medium", "high")
    assert result.counts == (40, 35, 25)
    assert result.reference_probabilities == pytest.approx((0.50, 0.30, 0.20))
    assert result.monitoring.prs.sample_size == 100


def test_named_api_matches_numeric_monitoring_result() -> None:
    """Named-category monitoring should preserve the numerical PRS result."""
    result = assess_named_population(
        counts={"a": 40, "b": 35, "c": 25},
        reference={"a": 0.50, "b": 0.30, "c": 0.20},
        ks_simulations=500,
        ks_seed=7,
    )

    expected = population_resemblance_statistic(
        observed=[0.40, 0.35, 0.25],
        reference=[0.50, 0.30, 0.20],
    )

    assert result.monitoring.prs.statistic == pytest.approx(expected)


def test_category_mismatch_reports_missing_and_extra_names() -> None:
    """Mismatched named categories should produce a useful validation error."""
    with pytest.raises(ValueError, match="missing=.*high.*extra=.*other"):
        assess_named_population(
            counts={"low": 10, "medium": 20, "other": 30},
            reference={"low": 0.5, "medium": 0.3, "high": 0.2},
            ks_simulations=100,
            ks_seed=1,
        )


def test_negative_named_count_is_rejected() -> None:
    """Named count inputs must remain non-negative."""
    with pytest.raises(ValueError, match="non-negative"):
        assess_named_population(
            counts={"a": 10, "b": -1},
            reference={"a": 0.5, "b": 0.5},
            ks_simulations=100,
            ks_seed=1,
        )


def test_boolean_named_count_is_rejected() -> None:
    """Boolean values must not be silently interpreted as integer counts."""
    with pytest.raises(TypeError, match="integer"):
        assess_named_population(
            counts={"a": True, "b": 9},
            reference={"a": 0.5, "b": 0.5},
            ks_simulations=100,
            ks_seed=1,
        )
