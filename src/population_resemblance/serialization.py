"""Serialization helpers for monitoring results."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from population_resemblance.reporting import PopulationMonitoringReport
from population_resemblance.temporal import TemporalMonitoringSeries


def monitoring_report_to_dict(
    report: PopulationMonitoringReport,
) -> dict[str, Any]:
    """Convert a population monitoring report to a JSON-safe dictionary."""
    return {
        "prs": {
            "statistic": report.prs.statistic,
            "delta": report.prs.delta,
            "lambda_sup": report.prs.lambda_sup,
            "critical_values": {
                "lower": report.prs.critical_values.lower,
                "upper": report.prs.critical_values.upper,
            },
            "region": report.prs.region.value,
            "label": report.prs.label,
            "sample_size": report.prs.sample_size,
            "categories": report.prs.categories,
        },
        "psi": {
            "statistic": report.psi.statistic,
            "status": report.psi.status,
        },
        "ks": {
            "statistic": report.ks.statistic,
            "p_value": report.ks.p_value,
            "status": report.ks.status,
            "simulations": report.ks.simulations,
            "sample_size": report.ks.sample_size,
        },
    }


def temporal_series_to_records(
    series: TemporalMonitoringSeries,
) -> list[dict[str, Any]]:
    """Convert a temporal monitoring series to flat JSON-safe records."""
    records: list[dict[str, Any]] = []

    for point in series.points:
        report = point.report
        records.append(
            {
                "label": point.label,
                "sample_size": report.prs.sample_size,
                "prs_statistic": report.prs.statistic,
                "prs_region": report.prs.region.value,
                "prs_label": report.prs.label,
                "prs_delta": report.prs.delta,
                "prs_lower_critical_value": report.prs.critical_values.lower,
                "prs_upper_critical_value": report.prs.critical_values.upper,
                "psi_statistic": report.psi.statistic,
                "psi_status": report.psi.status,
                "ks_statistic": report.ks.statistic,
                "ks_p_value": report.ks.p_value,
                "ks_status": report.ks.status,
            }
        )

    return records


def records_column(
    records: Sequence[dict[str, Any]],
    name: str,
) -> tuple[Any, ...]:
    """Extract one column from serialized temporal records."""
    return tuple(record[name] for record in records)
