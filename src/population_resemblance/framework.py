"""Delta-resemblance decision framework."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
from scipy.stats import ncx2

from population_resemblance.prs import (
    _as_probability_vector,
    population_resemblance_statistic,
)
from population_resemblance.result import (
    CriticalValues,
    DecisionRegion,
    PopulationResemblanceResult,
)


def _validate_sample_size(sample_size: int) -> None:
    """Validate the current sample size."""
    if isinstance(sample_size, bool) or not isinstance(sample_size, int):
        raise TypeError("sample_size must be an integer.")
    if sample_size <= 0:
        raise ValueError("sample_size must be positive.")


def _validate_positive(value: float, *, name: str) -> None:
    """Validate a positive finite scalar."""
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a positive finite value.")


def _reference_vector(
    reference: Sequence[float] | npt.NDArray[np.floating],
) -> npt.NDArray[np.float64]:
    """Return a validated strictly positive reference distribution."""
    array = _as_probability_vector(reference, name="reference")
    if np.any(array <= 0.0):
        raise ValueError("reference probabilities must be strictly positive.")
    return array


def recommended_delta(
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    *,
    c: float = 0.7,
) -> float:
    """Compute the recommended sample-size-aware tolerance delta."""
    reference_array = _reference_vector(reference)
    _validate_sample_size(sample_size)
    _validate_positive(c, name="c")

    standard_errors = np.sqrt(
        reference_array * (1.0 - reference_array) / float(sample_size)
    )
    return float(c * np.min(standard_errors))


def maximum_noncentrality(
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    delta: float,
) -> float:
    """Compute the least-favourable non-centrality parameter."""
    reference_array = _reference_vector(reference)
    _validate_sample_size(sample_size)
    _validate_positive(delta, name="delta")

    if delta > float(np.min(reference_array)):
        raise ValueError("delta must not exceed the smallest reference probability.")

    inverse_sum = float(np.sum(1.0 / reference_array))
    if reference_array.size % 2 == 1:
        inverse_sum -= 1.0 / float(np.max(reference_array))

    return float(sample_size) * delta**2 * inverse_sum


def critical_values(
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    delta: float,
    *,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> CriticalValues:
    """Compute the lower and upper PRS critical values."""
    reference_array = _reference_vector(reference)
    _validate_sample_size(sample_size)
    _validate_positive(delta, name="delta")
    _validate_positive(m, name="m")

    if m <= 1.0:
        raise ValueError("m must be greater than 1.")
    if not 0.0 <= alpha1 <= 1.0 or not 0.0 <= alpha2 <= 1.0:
        raise ValueError("alpha1 and alpha2 must lie in [0, 1].")
    if m * delta > float(np.min(reference_array)):
        raise ValueError("m * delta must not exceed the smallest reference probability.")

    lambda_sup = maximum_noncentrality(reference_array, sample_size, delta)
    degrees_of_freedom = int(reference_array.size - 1)

    lower = float(
        ncx2.ppf(alpha2, degrees_of_freedom, (m**2) * lambda_sup)
        / float(sample_size)
    )
    upper = float(
        ncx2.ppf(1.0 - alpha1, degrees_of_freedom, lambda_sup)
        / float(sample_size)
    )

    if np.isnan(lower) or np.isnan(upper):
        raise ValueError("parameters produced undefined critical values.")
    if lower > upper:
        raise ValueError("parameters produce overlapping decision boundaries.")

    return CriticalValues(lower=lower, upper=upper)


def assess_population_resemblance(
    observed: Sequence[float] | npt.NDArray[np.floating],
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    *,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> PopulationResemblanceResult:
    """Assess an observed distribution with the PRS decision framework."""
    reference_array = _reference_vector(reference)
    observed_array = _as_probability_vector(observed, name="observed")
    if observed_array.shape != reference_array.shape:
        raise ValueError("observed and reference must have the same number of categories.")

    _validate_sample_size(sample_size)
    resolved_delta = (
        recommended_delta(reference_array, sample_size, c=c)
        if delta is None
        else float(delta)
    )
    _validate_positive(resolved_delta, name="delta")

    thresholds = critical_values(
        reference_array,
        sample_size,
        resolved_delta,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
    )
    lambda_sup = maximum_noncentrality(reference_array, sample_size, resolved_delta)
    statistic = population_resemblance_statistic(observed_array, reference_array)

    if statistic <= thresholds.lower:
        region = DecisionRegion.R1
    elif statistic <= thresholds.upper:
        region = DecisionRegion.R2
    else:
        region = DecisionRegion.R3

    return PopulationResemblanceResult(
        statistic=statistic,
        delta=resolved_delta,
        lambda_sup=lambda_sup,
        critical_values=thresholds,
        region=region,
        sample_size=sample_size,
        categories=int(reference_array.size),
    )
