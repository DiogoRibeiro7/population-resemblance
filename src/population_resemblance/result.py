"""Typed result objects for population resemblance monitoring."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DecisionRegion(StrEnum):
    """Three PRS decision regions defined by the resemblance framework."""

    R1 = "R1"
    R2 = "R2"
    R3 = "R3"

    @property
    def label(self) -> str:
        """Return the source methodology's neutral descriptive label."""
        labels = {
            DecisionRegion.R1: "acceptable",
            DecisionRegion.R2: "partially discrepant",
            DecisionRegion.R3: "fully discrepant",
        }
        return labels[self]


@dataclass(frozen=True, slots=True)
class CriticalValues:
    """Lower and upper PRS decision thresholds."""

    lower: float
    upper: float


@dataclass(frozen=True, slots=True)
class PopulationResemblanceResult:
    """Complete result of a PRS population resemblance assessment."""

    statistic: float
    delta: float
    lambda_sup: float
    critical_values: CriticalValues
    region: DecisionRegion
    sample_size: int
    categories: int

    @property
    def label(self) -> str:
        """Return a human-readable description of the decision region."""
        return self.region.label
