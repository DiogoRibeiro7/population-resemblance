"""Convenience API for empirical reference distributions built from counts."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.counts import _as_count_vector, counts_to_proportions
from population_resemblance.reporting import (
    PopulationMonitoringReport,
    assess_population_monitoring,
)


@dataclass(frozen=True, slots=True)
class ReferenceCountMonitoringReport:
    """Monitoring report using an empirical reference sample conditionally as fixed."""

    current_sample_size: int
    reference_sample_size: int
    reference_probabilities: tuple[float, ...]
    monitoring: PopulationMonitoringReport


def assess_against_reference_counts(
    current_counts: Sequence[int] | npt.NDArray[np.integer],
    reference_counts: Sequence[int] | npt.NDArray[np.integer],
    *,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
    ks_simulations: int = 10_000,
    ks_seed: int | None = None,
) -> ReferenceCountMonitoringReport:
    """Assess current counts against a reference sample represented by counts.

    The reference counts are converted to empirical probabilities and then
    treated as fixed for the existing one-sample PRS framework. This is a
    convenience wrapper for conditional inference; it is not a two-sample PRS
    test and does not propagate reference-sample uncertainty into the critical
    values.

    Parameters
    ----------
    current_counts:
        Current observed counts by category.
    reference_counts:
        Baseline or model-development counts by the same categories.
    delta:
        Optional explicit PRS tolerance.
    c:
        Multiplier used for automatic PRS tolerance calibration.
    m:
        Wider resemblance multiplier.
    alpha1:
        Upper PRS error-control parameter.
    alpha2:
        Lower PRS error-control parameter.
    ks_simulations:
        Monte Carlo sample count used to calibrate the discrete KS benchmark.
    ks_seed:
        Optional random seed used for the discrete KS calibration.

    Returns
    -------
    ReferenceCountMonitoringReport
        Sample-size metadata, empirical reference probabilities, and the
        unified PRS/PSI/KS monitoring report.
    """
    current_array = _as_count_vector(current_counts, name="current_counts")
    reference_array = _as_count_vector(reference_counts, name="reference_counts")

    if current_array.shape != reference_array.shape:
        raise ValueError(
            "current_counts and reference_counts must have the same number of categories."
        )
    if np.any(reference_array == 0):
        raise ValueError(
            "reference_counts must be strictly positive in every category "
            "for the fixed-reference PRS framework."
        )

    current_sample_size = int(np.sum(current_array, dtype=np.int64))
    reference_sample_size = int(np.sum(reference_array, dtype=np.int64))
    reference_probabilities_array = counts_to_proportions(reference_array)

    monitoring = assess_population_monitoring(
        counts=current_array,
        reference=reference_probabilities_array,
        delta=delta,
        c=c,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
        ks_simulations=ks_simulations,
        ks_seed=ks_seed,
    )

    return ReferenceCountMonitoringReport(
        current_sample_size=current_sample_size,
        reference_sample_size=reference_sample_size,
        reference_probabilities=tuple(
            float(value) for value in reference_probabilities_array
        ),
        monitoring=monitoring,
    )
