"""End-to-end example for JSON-safe and tabular monitoring exports."""

from __future__ import annotations

import json

from population_resemblance import (
    assess_population_monitoring,
    assess_temporal_monitoring,
    monitoring_report_to_dict,
    records_column,
    temporal_series_to_records,
)


def main() -> None:
    """Serialize single and temporal monitoring results."""
    reference = [0.50, 0.30, 0.20]

    report = assess_population_monitoring(
        counts=[420, 330, 250],
        reference=reference,
        ks_simulations=1_000,
        ks_seed=500,
    )
    payload = monitoring_report_to_dict(report)

    print("json_export")
    print(json.dumps(payload, indent=2, sort_keys=True))

    series = assess_temporal_monitoring(
        counts_by_period=[
            [500, 300, 200],
            [460, 320, 220],
            [420, 330, 250],
        ],
        reference=reference,
        labels=["baseline_like", "moderate_shift", "larger_shift"],
        ks_simulations=500,
        ks_seed=600,
    )
    records = temporal_series_to_records(series)

    print("tabular_records")
    print(json.dumps(records, indent=2, sort_keys=True))
    print(f"labels={records_column(records, 'label')}")
    print(f"prs_regions={records_column(records, 'prs_region')}")


if __name__ == "__main__":
    main()
