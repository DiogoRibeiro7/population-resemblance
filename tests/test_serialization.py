"""Tests for monitoring result serialization."""

from __future__ import annotations

import json

import pytest

from population_resemblance import (
    assess_population_monitoring,
    assess_temporal_monitoring,
    monitoring_report_to_dict,
    records_column,
    temporal_series_to_records,
)


def test_monitoring_report_serializes_to_json() -> None:
    """Serialized monitoring reports should be directly JSON-compatible."""
    report = assess_population_monitoring(
        counts=[40, 35, 25],
        reference=[0.50, 0.30, 0.20],
        ks_simulations=500,
        ks_seed=123,
    )

    payload = monitoring_report_to_dict(report)
    encoded = json.dumps(payload)

    assert encoded
    assert payload["prs"]["sample_size"] == 100
    assert payload["psi"]["status"] in {"green", "amber", "red"}
    assert payload["ks"]["status"] in {"green", "amber", "red"}


def test_serialized_prs_values_match_original_report() -> None:
    """Serialization must preserve the original PRS numerical values exactly."""
    report = assess_population_monitoring(
        counts=[4, 10, 11, 11, 14],
        reference=[0.2] * 5,
        ks_simulations=500,
        ks_seed=7,
    )

    payload = monitoring_report_to_dict(report)

    assert payload["prs"]["statistic"] == report.prs.statistic
    assert payload["prs"]["delta"] == report.prs.delta
    assert payload["prs"]["region"] == report.prs.region.value


def test_temporal_series_serializes_to_flat_records() -> None:
    """Temporal serialization should produce one record per monitoring period."""
    series = assess_temporal_monitoring(
        counts_by_period=[
            [50, 30, 20],
            [45, 35, 20],
            [40, 35, 25],
        ],
        reference=[0.50, 0.30, 0.20],
        labels=["Q1", "Q2", "Q3"],
        ks_simulations=500,
        ks_seed=20,
    )

    records = temporal_series_to_records(series)

    assert len(records) == 3
    assert [record["label"] for record in records] == ["Q1", "Q2", "Q3"]
    assert all("prs_statistic" in record for record in records)
    assert all("ks_p_value" in record for record in records)


def test_temporal_records_are_json_compatible() -> None:
    """Temporal records should contain only JSON-safe values."""
    series = assess_temporal_monitoring(
        counts_by_period=[[10, 10], [12, 8]],
        reference=[0.5, 0.5],
        ks_simulations=200,
        ks_seed=1,
    )

    records = temporal_series_to_records(series)

    assert json.dumps(records)


def test_records_column_preserves_order() -> None:
    """Column extraction should preserve temporal ordering."""
    series = assess_temporal_monitoring(
        counts_by_period=[[10, 10], [12, 8]],
        reference=[0.5, 0.5],
        labels=["before", "after"],
        ks_simulations=200,
        ks_seed=1,
    )

    records = temporal_series_to_records(series)

    assert records_column(records, "label") == ("before", "after")


def test_records_column_raises_for_missing_column() -> None:
    """Unknown columns should fail explicitly."""
    with pytest.raises(KeyError):
        records_column([{"a": 1}], "missing")
