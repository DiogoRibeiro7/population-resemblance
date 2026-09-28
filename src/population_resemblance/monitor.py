"""Reusable configured population monitor."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.named import (
    NamedPopulationMonitoringReport,
    assess_named_population,
)
from population_resemblance.reporting import (
    PopulationMonitoringReport,
    assess_population_monitoring,
)
from population_resemblance.temporal import (
    TemporalMonitoringSeries,
    assess_temporal_monitoring,
)


@dataclass(frozen=True, slots=True)
class PopulationMonitor:
    """Reusable monitoring configuration for a fixed reference distribution."""

    reference: tuple[float, ...]
    delta: float | None = None
    c: float = 0.7
    m: float = 2.0
    alpha1: float = 0.05
    alpha2: float = 0.10
    ks_simulations: int = 10_000
    ks_seed: int | None = None

    @classmethod
    def from_reference(
        cls,
        reference: Sequence[float] | npt.NDArray[np.floating],
        *,
        delta: float | None = None,
        c: float = 0.7,
        m: float = 2.0,
        alpha1: float = 0.05,
        alpha2: float = 0.10,
        ks_simulations: int = 10_000,
        ks_seed: int | None = None,
    ) -> "PopulationMonitor":
        """Create a monitor from a fixed reference probability vector."""
        array = np.asarray(reference, dtype=np.float64)
        return cls(
            reference=tuple(float(value) for value in array),
            delta=delta,
            c=c,
            m=m,
            alpha1=alpha1,
            alpha2=alpha2,
            ks_simulations=ks_simulations,
            ks_seed=ks_seed,
        )

    def assess(
        self,
        counts: Sequence[int] | npt.NDArray[np.integer],
    ) -> PopulationMonitoringReport:
        """Assess one current categorical sample."""
        return assess_population_monitoring(
            counts=counts,
            reference=self.reference,
            delta=self.delta,
            c=self.c,
            m=self.m,
            alpha1=self.alpha1,
            alpha2=self.alpha2,
            ks_simulations=self.ks_simulations,
            ks_seed=self.ks_seed,
        )

    def assess_temporal(
        self,
        counts_by_period: Sequence[Sequence[int]] | npt.NDArray[np.integer],
        *,
        labels: Sequence[str] | None = None,
    ) -> TemporalMonitoringSeries:
        """Assess repeated population snapshots using the stored configuration."""
        return assess_temporal_monitoring(
            counts_by_period=counts_by_period,
            reference=self.reference,
            labels=labels,
            delta=self.delta,
            c=self.c,
            m=self.m,
            alpha1=self.alpha1,
            alpha2=self.alpha2,
            ks_simulations=self.ks_simulations,
            ks_seed=self.ks_seed,
        )


@dataclass(frozen=True, slots=True)
class NamedPopulationMonitor:
    """Reusable monitor for a fixed named-category reference distribution."""

    reference: tuple[tuple[str, float], ...]
    delta: float | None = None
    c: float = 0.7
    m: float = 2.0
    alpha1: float = 0.05
    alpha2: float = 0.10
    ks_simulations: int = 10_000
    ks_seed: int | None = None

    @classmethod
    def from_reference(
        cls,
        reference: Mapping[str, float],
        *,
        delta: float | None = None,
        c: float = 0.7,
        m: float = 2.0,
        alpha1: float = 0.05,
        alpha2: float = 0.10,
        ks_simulations: int = 10_000,
        ks_seed: int | None = None,
    ) -> "NamedPopulationMonitor":
        """Create a monitor from a named fixed reference distribution."""
        return cls(
            reference=tuple((key, float(value)) for key, value in reference.items()),
            delta=delta,
            c=c,
            m=m,
            alpha1=alpha1,
            alpha2=alpha2,
            ks_simulations=ks_simulations,
            ks_seed=ks_seed,
        )

    @property
    def categories(self) -> tuple[str, ...]:
        """Return category names in canonical monitoring order."""
        return tuple(key for key, _ in self.reference)

    def assess(self, counts: Mapping[str, int]) -> NamedPopulationMonitoringReport:
        """Assess one named-category current sample."""
        return assess_named_population(
            counts=counts,
            reference=dict(self.reference),
            delta=self.delta,
            c=self.c,
            m=self.m,
            alpha1=self.alpha1,
            alpha2=self.alpha2,
            ks_simulations=self.ks_simulations,
            ks_seed=self.ks_seed,
        )
