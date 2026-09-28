"""Calibration diagnostics for PRS decision parameters."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.framework import (
    critical_values,
    maximum_noncentrality,
    recommended_delta,
)


@dataclass(frozen=True, slots=True)
class CalibrationDiagnostics:
    """Derived quantities for one PRS calibration configuration."""

    delta: float
    widened_delta: float
    lambda_sup: float
    lower_critical_value: float
    upper_critical_value: float
    minimum_reference_probability: float
    margin_to_probability_bound: float
    boundaries_overlap: bool

    @property
    def feasible(self) -> bool:
        """Return whether the calibration satisfies structural constraints."""
        return (
            self.margin_to_probability_bound >= 0.0
            and not self.boundaries_overlap
        )


def evaluate_calibration(
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    *,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> CalibrationDiagnostics:
    """Evaluate one PRS calibration without performing a population assessment.

    This exposes the main derived quantities that determine whether a chosen
    combination of tolerance and sensitivity parameters is practically valid.

    Parameters
    ----------
    reference:
        Fixed reference probability distribution.
    sample_size:
        Current sample size.
    delta:
        Optional explicit tolerance. If omitted, the recommended sample-size-
        aware value is used.
    c:
        Multiplier used for automatic delta calibration.
    m:
        Wider resemblance multiplier.
    alpha1:
        Upper decision error-control parameter.
    alpha2:
        Lower decision error-control parameter.

    Returns
    -------
    CalibrationDiagnostics
        Derived tolerance, non-centrality, critical values, and feasibility
        margins for the supplied configuration.
    """
    reference_array = np.asarray(reference, dtype=np.float64)
    if reference_array.ndim != 1:
        raise ValueError("reference must be one-dimensional.")
    if reference_array.size < 2:
        raise ValueError("reference must contain at least two categories.")
    if not np.all(np.isfinite(reference_array)):
        raise ValueError("reference must contain only finite values.")
    if np.any(reference_array <= 0.0):
        raise ValueError("reference probabilities must be strictly positive.")
    if not np.isclose(float(reference_array.sum()), 1.0, rtol=1e-10, atol=1e-12):
        raise ValueError("reference must sum to 1.")

    resolved_delta = (
        recommended_delta(reference_array, sample_size, c=c)
        if delta is None
        else float(delta)
    )

    minimum_reference_probability = float(np.min(reference_array))
    widened_delta = float(m * resolved_delta)
    margin = minimum_reference_probability - widened_delta

    lambda_sup = maximum_noncentrality(
        reference_array,
        sample_size,
        resolved_delta,
    )
    thresholds = critical_values(
        reference_array,
        sample_size,
        resolved_delta,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
    )

    return CalibrationDiagnostics(
        delta=resolved_delta,
        widened_delta=widened_delta,
        lambda_sup=lambda_sup,
        lower_critical_value=thresholds.lower,
        upper_critical_value=thresholds.upper,
        minimum_reference_probability=minimum_reference_probability,
        margin_to_probability_bound=margin,
        boundaries_overlap=thresholds.lower > thresholds.upper,
    )
