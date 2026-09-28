"""Tests for reusable population monitor objects."""

from __future__ import annotations

import pytest

from population_resemblance import (
    NamedPopulationMonitor,
    PopulationMonitor,
    assess_population_monitoring,
)


def test_population_monitor_matches_functional_api() -> None:
    """Configured monitor output should match the existing functional API."""
    monitor = PopulationMonitor.from_reference(
        [0.50, 0.30, 0.20],
        ks_simulations=1_000,
        ks_seed=123,
    )

    via_monitor = monitor.assess([40, 35, 25])
    via_function = assess_population_monitoring(
        counts=[40, 35, 25],
        reference=[0.50, 0.30, 0.20],
        ks_simulations=1_000,
        ks_seed=123,
    )

    assert via_monitor == via_function


def test_population_monitor_reuses_configuration() -> None:
    """Stored calibration parameters should apply across repeated assessments."""
    monitor = PopulationMonitor.from_reference(
        [0.5, 0.3, 0.2],
        delta=0.01,
        m=1.5,
        ks_simulations=500,
        ks_seed=7,
    )

    first = monitor.assess([50, 30, 20])
    second = monitor.assess([45, 35, 20])

    assert first.prs.delta == pytest.approx(0.01)
    assert second.prs.delta == pytest.approx(0.01)


def test_population_monitor_temporal_api() -> None:
    """A configured monitor should assess repeated periods without re-supplying settings."""
    monitor = PopulationMonitor.from_reference(
        [0.50, 0.30, 0.20],
        ks_simulations=500,
        ks_seed=5,
    )

    series = monitor.assess_temporal(
        [
            [50, 30, 20],
            [45, 35, 20],
        ],
        labels=["before", "after"],
    )

    assert series.labels == ("before", "after")
    assert len(series.points) == 2


def test_named_monitor_preserves_reference_order() -> None:
    """Named monitor should preserve the canonical reference category order."""
    monitor = NamedPopulationMonitor.from_reference(
        {"low": 0.50, "medium": 0.30, "high": 0.20},
        ks_simulations=500,
        ks_seed=9,
    )

    result = monitor.assess(
        {"high": 25, "low": 40, "medium": 35},
    )

    assert monitor.categories == ("low", "medium", "high")
    assert result.categories == ("low", "medium", "high")
    assert result.counts == (40, 35, 25)


def test_named_monitor_rejects_category_mismatch() -> None:
    """Named monitor should retain the strict category-name validation."""
    monitor = NamedPopulationMonitor.from_reference(
        {"a": 0.5, "b": 0.5},
        ks_simulations=100,
        ks_seed=1,
    )

    with pytest.raises(ValueError, match="same category names"):
        monitor.assess({"a": 10, "c": 10})
