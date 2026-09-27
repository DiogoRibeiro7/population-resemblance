"""Tests for unified population monitoring reports."""

from __future__ import annotations

import pytest

from population_resemblance import (
    DecisionRegion,
    assess_population_monitoring,
)


def test_unified_report_contains_all_three_methods() -> None:
    """A monitoring report should include PRS, PSI, and discrete KS results."""
    report = assess_population_monitoring(
        counts=[40, 35, 25],
        reference=[0.50, 0.30, 0.20],
        ks_simulations=2_000,
        ks_seed=123,
    )

    assert report.prs.sample_size == 100
    assert report.psi.statistic >= 0.0
    assert 0.0 <= report.ks.p_value <= 1.0


def test_table_3a_small_sample_prs_and_psi_classifications() -> None:
    """The unified API should reproduce a selected paper comparison row."""
    report = assess_population_monitoring(
        counts=[2, 5, 13, 14, 16],
        reference=[0.2] * 5,
        ks_simulations=5_000,
        ks_seed=7,
    )

    assert report.prs.statistic == pytest.approx(0.300, abs=5e-4)
    assert report.prs.region is DecisionRegion.R3
    assert report.psi.statistic == pytest.approx(0.426, abs=5e-4)
    assert report.psi.status == "red"


def test_status_tuple_is_compact_and_ordered() -> None:
    """The status tuple should follow PRS, PSI, KS ordering."""
    report = assess_population_monitoring(
        counts=[10, 10, 10, 10],
        reference=[0.25] * 4,
        ks_simulations=1_000,
        ks_seed=11,
    )

    prs_status, psi_status, ks_status = report.statuses

    assert prs_status == report.prs.label
    assert psi_status == report.psi.status
    assert ks_status == report.ks.status


def test_unified_report_propagates_category_validation() -> None:
    """Dimension mismatches should fail before returning a partial report."""
    with pytest.raises(ValueError):
        assess_population_monitoring(
            counts=[10, 20, 30],
            reference=[0.5, 0.5],
            ks_simulations=100,
            ks_seed=1,
        )


def test_ks_seed_makes_unified_report_reproducible() -> None:
    """A fixed KS seed should reproduce the full report exactly."""
    first = assess_population_monitoring(
        counts=[8, 12, 30],
        reference=[0.2, 0.3, 0.5],
        ks_simulations=2_000,
        ks_seed=42,
    )
    second = assess_population_monitoring(
        counts=[8, 12, 30],
        reference=[0.2, 0.3, 0.5],
        ks_simulations=2_000,
        ks_seed=42,
    )

    assert first == second
