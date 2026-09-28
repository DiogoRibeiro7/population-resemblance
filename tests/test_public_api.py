"""Compatibility tests for the package root public API."""

from __future__ import annotations

import population_resemblance

EXPECTED_PUBLIC_API = (
    "CalibrationDiagnostics",
    "CalibrationSensitivityGrid",
    "CalibrationSensitivityPoint",
    "CategoryContribution",
    "ClassificationProbabilities",
    "CriticalValues",
    "DecisionRegion",
    "DiscreteKSTestResult",
    "NamedPopulationMonitor",
    "NamedPopulationMonitoringReport",
    "OperatingCharacteristicCurve",
    "OperatingCharacteristicPoint",
    "PRSPSIComparisonResult",
    "PSIAssessment",
    "PopulationMonitor",
    "ProbabilityInterval",
    "PopulationMonitoringReport",
    "PopulationResemblanceResult",
    "ReferenceCountMonitoringReport",
    "ResemblanceDiagnostics",
    "SimulationResult",
    "SimulationUncertainty",
    "TemporalMonitoringPoint",
    "TemporalMonitoringSeries",
    "assess_against_reference_counts",
    "assess_named_population",
    "assess_population_counts",
    "assess_population_monitoring",
    "assess_population_resemblance",
    "assess_temporal_monitoring",
    "counts_to_proportions",
    "critical_values",
    "discrete_ks_statistic",
    "discrete_ks_status",
    "discrete_ks_test_counts",
    "evaluate_calibration",
    "lewis_psi_status",
    "maximum_noncentrality",
    "monitoring_report_to_dict",
    "population_count_diagnostics",
    "population_resemblance_diagnostics",
    "population_resemblance_statistic",
    "population_stability_index",
    "recommended_delta",
    "records_column",
    "simulate_operating_characteristic_curve",
    "simulate_prs_psi_comparison",
    "simulate_region_probabilities",
    "simulation_uncertainty",
    "source_deviation_grid",
    "sweep_calibration_parameters",
    "temporal_series_to_records",
    "symmetric_category_shift",
)


def test_root_public_api_matches_snapshot() -> None:
    """Public root exports must change intentionally."""
    assert tuple(population_resemblance.__all__) == EXPECTED_PUBLIC_API


def test_every_public_export_resolves() -> None:
    """Every declared public export must exist on the package root."""
    for name in EXPECTED_PUBLIC_API:
        assert hasattr(population_resemblance, name)
