"""Monte Carlo tools for studying PRS decision behavior."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.framework import (
    _reference_vector,
    _validate_sample_size,
    critical_values,
    recommended_delta,
)
from population_resemblance.prs import _as_probability_vector


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Empirical PRS decision probabilities from a Monte Carlo experiment."""

    simulations: int
    r1_probability: float
    r2_probability: float
    r3_probability: float
    mean_statistic: float

    @property
    def probabilities(self) -> tuple[float, float, float]:
        """Return region probabilities in R1, R2, R3 order."""
        return (
            self.r1_probability,
            self.r2_probability,
            self.r3_probability,
        )


def symmetric_category_shift(
    reference: Sequence[float] | npt.NDArray[np.floating],
    deviation: float,
) -> npt.NDArray[np.float64]:
    """Construct the symmetric perturbation used in the source simulation study.

    The first half of the categories is shifted downward by the supplied
    deviation and the last half upward by the same amount. For an odd number
    of categories, the central category remains unchanged.

    Parameters
    ----------
    reference:
        Reference categorical probability distribution.
    deviation:
        Absolute probability shift applied to each perturbed category.

    Returns
    -------
    numpy.ndarray
        Perturbed probability distribution.

    Raises
    ------
    ValueError
        If the deviation is invalid or would create an invalid probability.
    """
    reference_array = _reference_vector(reference)

    if not np.isfinite(deviation) or deviation < 0.0:
        raise ValueError("deviation must be a finite non-negative value.")

    shifted = reference_array.copy()
    half = int(reference_array.size // 2)

    shifted[:half] -= deviation
    shifted[-half:] += deviation

    if np.any(shifted < 0.0) or np.any(shifted > 1.0):
        raise ValueError("deviation produces invalid category probabilities.")
    if not np.isclose(float(np.sum(shifted)), 1.0, rtol=1e-12, atol=1e-12):
        raise ValueError("shifted probabilities must sum to 1.")

    return shifted


def simulate_region_probabilities(
    current: Sequence[float] | npt.NDArray[np.floating],
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    *,
    simulations: int = 10_000,
    seed: int | None = None,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> SimulationResult:
    """Estimate PRS decision probabilities under a specified current population.

    Samples are drawn independently from a multinomial distribution with the
    supplied current probabilities. Each simulated empirical distribution is
    classified into the PRS regions R1, R2, or R3.

    Parameters
    ----------
    current:
        True categorical probabilities from which simulated samples are drawn.
    reference:
        Fixed reference categorical probability distribution.
    sample_size:
        Number of observations in each simulated sample.
    simulations:
        Number of independent Monte Carlo samples.
    seed:
        Optional random seed for reproducibility.
    delta:
        Optional explicit resemblance tolerance. If omitted, the recommended
        sample-size-aware value is used.
    c:
        Tolerance multiplier used for automatic delta calibration.
    m:
        Multiplier defining the wider resemblance region.
    alpha1:
        Error-control parameter for the upper decision boundary.
    alpha2:
        Error-control parameter for the lower decision boundary.

    Returns
    -------
    SimulationResult
        Empirical decision-region probabilities and mean PRS value.
    """
    current_array = _as_probability_vector(current, name="current")
    reference_array = _reference_vector(reference)

    if current_array.shape != reference_array.shape:
        raise ValueError("current and reference must have the same number of categories.")

    _validate_sample_size(sample_size)

    if isinstance(simulations, bool) or not isinstance(simulations, int):
        raise TypeError("simulations must be an integer.")
    if simulations <= 0:
        raise ValueError("simulations must be positive.")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None.")

    resolved_delta = (
        recommended_delta(reference_array, sample_size, c=c)
        if delta is None
        else float(delta)
    )
    thresholds = critical_values(
        reference_array,
        sample_size,
        resolved_delta,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
    )

    rng = np.random.default_rng(seed)
    counts = rng.multinomial(
        sample_size,
        current_array,
        size=simulations,
    )
    observed = counts.astype(np.float64) / float(sample_size)
    differences = observed - reference_array
    statistics = np.sum(
        np.square(differences) / reference_array,
        axis=1,
    )

    r1 = statistics <= thresholds.lower
    r3 = statistics > thresholds.upper
    r2 = ~(r1 | r3)

    return SimulationResult(
        simulations=simulations,
        r1_probability=float(np.mean(r1)),
        r2_probability=float(np.mean(r2)),
        r3_probability=float(np.mean(r3)),
        mean_statistic=float(np.mean(statistics)),
    )
