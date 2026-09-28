"""Named-category convenience API for population monitoring."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from population_resemblance.reporting import (
    PopulationMonitoringReport,
    assess_population_monitoring,
)


@dataclass(frozen=True, slots=True)
class NamedPopulationMonitoringReport:
    """Monitoring report with explicit category labels."""

    categories: tuple[str, ...]
    counts: tuple[int, ...]
    reference_probabilities: tuple[float, ...]
    monitoring: PopulationMonitoringReport


def assess_named_population(
    counts: Mapping[str, int],
    reference: Mapping[str, float],
    *,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
    ks_simulations: int = 10_000,
    ks_seed: int | None = None,
) -> NamedPopulationMonitoringReport:
    """Assess a categorical population using named categories.

    Category keys are aligned by the insertion order of the reference mapping.
    The current-count mapping must contain exactly the same category names.
    """
    if len(reference) < 2:
        raise ValueError("reference must contain at least two categories.")
    if set(counts) != set(reference):
        missing = sorted(set(reference) - set(counts))
        extra = sorted(set(counts) - set(reference))
        raise ValueError(
            "counts and reference must contain exactly the same category names; "
            f"missing={missing}, extra={extra}."
        )

    categories = tuple(reference.keys())
    resolved_counts: list[int] = []
    resolved_reference: list[float] = []

    for category in categories:
        count = counts[category]
        probability = reference[category]

        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError(f"count for category {category!r} must be an integer.")
        if count < 0:
            raise ValueError(f"count for category {category!r} must be non-negative.")

        resolved_counts.append(count)
        resolved_reference.append(float(probability))

    monitoring = assess_population_monitoring(
        counts=resolved_counts,
        reference=resolved_reference,
        delta=delta,
        c=c,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
        ks_simulations=ks_simulations,
        ks_seed=ks_seed,
    )

    return NamedPopulationMonitoringReport(
        categories=categories,
        counts=tuple(resolved_counts),
        reference_probabilities=tuple(resolved_reference),
        monitoring=monitoring,
    )
