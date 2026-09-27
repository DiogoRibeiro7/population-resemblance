"""Temporal monitoring utilities for repeated categorical population snapshots."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.reporting import (
    PopulationMonitoringReport,
    assess_population_monitoring,
)


@dataclass(frozen=True, slots=True)
class TemporalMonitoringPoint:
    """Monitoring result for one labeled population snapshot."""

    label: str
    report: PopulationMonitoringReport


@dataclass(frozen=True, slots=True)
class TemporalMonitoringSeries:
    """Ordered monitoring results across multiple population snapshots."""

    points: tuple[TemporalMonitoringPoint, ...]

    @property
    def labels(self) -> tuple[str, ...]:
        """Return snapshot labels in temporal order."""
        return tuple(point.label for point in self.points)

    @property
    def prs_statistics(self) -> tuple[float, ...]:
        """Return PRS statistics in temporal order."""
        return tuple(point.report.prs.statistic for point in self.points)

    @property
    def psi_statistics(self) -> tuple[float, ...]:
        """Return PSI statistics in temporal order."""
        return tuple(point.report.psi.statistic for point in self.points)

    @property
    def ks_statistics(self) -> tuple[float, ...]:
        """Return discrete KS statistics in temporal order."""
        return tuple(point.report.ks.statistic for point in self.points)


def assess_temporal_monitoring(
    counts_by_period: Sequence[Sequence[int]] | npt.NDArray[np.integer],
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    labels: Sequence[str] | None = None,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
    ks_simulations: int = 10_000,
    ks_seed: int | None = None,
) -> TemporalMonitoringSeries:
    """Assess repeated categorical samples against one fixed reference distribution.

    Optional labels default to period_1, period_2, and so on. If a base
    KS seed is supplied, each period receives a deterministic seed offset.
    """
    counts_array = np.asarray(counts_by_period)

    if counts_array.ndim != 2:
        raise ValueError("counts_by_period must be a two-dimensional array-like object.")
    if counts_array.shape[0] == 0:
        raise ValueError("counts_by_period must contain at least one period.")
    if counts_array.shape[1] < 2:
        raise ValueError("each period must contain at least two categories.")
    if np.issubdtype(counts_array.dtype, np.bool_) or not np.issubdtype(
        counts_array.dtype, np.integer
    ):
        raise TypeError("counts_by_period must contain integer counts.")
    if np.any(counts_array < 0):
        raise ValueError("counts_by_period must not contain negative counts.")
    if np.any(np.sum(counts_array, axis=1) <= 0):
        raise ValueError("each period must contain at least one observation.")

    period_count = int(counts_array.shape[0])

    if labels is None:
        resolved_labels = tuple(f"period_{index + 1}" for index in range(period_count))
    else:
        if len(labels) != period_count:
            raise ValueError("labels must match the number of monitoring periods.")
        if any(not isinstance(label, str) or not label for label in labels):
            raise ValueError("labels must contain non-empty strings.")
        resolved_labels = tuple(labels)

    points: list[TemporalMonitoringPoint] = []

    for index, (label, counts) in enumerate(
        zip(resolved_labels, counts_array, strict=True)
    ):
        seed = None if ks_seed is None else ks_seed + index
        report = assess_population_monitoring(
            counts=counts,
            reference=reference,
            delta=delta,
            c=c,
            m=m,
            alpha1=alpha1,
            alpha2=alpha2,
            ks_simulations=ks_simulations,
            ks_seed=seed,
        )
        points.append(TemporalMonitoringPoint(label=label, report=report))

    return TemporalMonitoringSeries(points=tuple(points))
