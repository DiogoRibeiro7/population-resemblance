"""Tests for empirical reference-count monitoring."""

from __future__ import annotations

import pytest

from population_resemblance import (
    assess_against_reference_counts,
    assess_population_monitoring,
)


def test_reference_counts_match_fixed_probability_api() -> None:
    """Empirical reference counts should reproduce the conditional fixed-p0 API."""
    from_counts = assess_against_reference_counts(
        current_counts=[40, 35, 25],
        reference_counts=[500, 300, 200],
        ks_simulations=2_000,
        ks_seed=123,
    )
    fixed_reference = assess_population_monitoring(
        counts=[40, 35, 25],
        reference=[0.50, 0.30, 0.20],
        ks_simulations=2_000,
        ks_seed=123,
    )

    assert from_counts.monitoring == fixed_reference
    assert from_counts.reference_probabilities == pytest.approx((0.50, 0.30, 0.20))


def test_sample_sizes_are_preserved() -> None:
    """The wrapper should retain both current and baseline sample sizes."""
    result = assess_against_reference_counts(
        current_counts=[20, 15, 15],
        reference_counts=[200, 150, 150],
        ks_simulations=500,
        ks_seed=7,
    )

    assert result.current_sample_size == 50
    assert result.reference_sample_size == 500


def test_reference_zero_count_is_rejected() -> None:
    """A zero baseline cell is invalid under the fixed-reference PRS assumptions."""
    with pytest.raises(ValueError, match="strictly positive"):
        assess_against_reference_counts(
            current_counts=[10, 20, 30],
            reference_counts=[100, 0, 200],
            ks_simulations=100,
            ks_seed=1,
        )


def test_category_mismatch_is_rejected() -> None:
    """Current and baseline count vectors must use the same categories."""
    with pytest.raises(ValueError, match="same number of categories"):
        assess_against_reference_counts(
            current_counts=[10, 20, 30],
            reference_counts=[100, 200],
            ks_simulations=100,
            ks_seed=1,
        )


def test_explicit_delta_passes_through() -> None:
    """A domain-specific delta should reach the underlying PRS assessment unchanged."""
    result = assess_against_reference_counts(
        current_counts=[40, 35, 25],
        reference_counts=[500, 300, 200],
        delta=0.01,
        m=2.0,
        ks_simulations=500,
        ks_seed=5,
    )

    assert result.monitoring.prs.delta == pytest.approx(0.01)
