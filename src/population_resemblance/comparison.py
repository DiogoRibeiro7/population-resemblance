"""Simulation tools for comparing PRS and PSI classifications."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.framework import critical_values, recommended_delta
from population_resemblance.prs import _as_probability_vector
from population_resemblance.psi import lewis_psi_status


@dataclass(frozen=True, slots=True)
class ClassificationProbabilities:
    """Empirical green/amber/red classification probabilities."""

    green: float
    amber: float
    red: float

    @property
    def total(self) -> float:
        """Return the total probability mass."""
        return self.green + self.amber + self.red


@dataclass(frozen=True, slots=True)
class PRSPSIComparisonResult:
    """Monte Carlo comparison between PRS and PSI classifications."""

    simulations: int
    prs: ClassificationProbabilities
    psi: ClassificationProbabilities


def simulate_prs_psi_comparison(
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
) -> PRSPSIComparisonResult:
    """Estimate PRS and PSI classification frequencies on identical samples.

    PRS classifications use the delta-resemblance decision boundaries. PSI
    classifications use the traditional Lewis thresholds of 0.10 and 0.25.

    Parameters
    ----------
    current:
        True categorical probabilities used to generate samples.
    reference:
        Fixed reference categorical distribution.
    sample_size:
        Number of observations per Monte Carlo sample.
    simulations:
        Number of simulated samples.
    seed:
        Optional random seed.
    delta:
        Optional explicit PRS tolerance.
    c:
        Multiplier used for automatic delta calibration.
    m:
        Wider resemblance multiplier.
    alpha1:
        Upper PRS error-control parameter.
    alpha2:
        Lower PRS error-control parameter.

    Returns
    -------
    PRSPSIComparisonResult
        Empirical classification probabilities for both methods.
    """
    current_array = _as_probability_vector(current, name="current")
    reference_array = _as_probability_vector(reference, name="reference")

    if current_array.shape != reference_array.shape:
        raise ValueError("current and reference must have the same number of categories.")
    if np.any(reference_array <= 0.0):
        raise ValueError("reference probabilities must be strictly positive.")
    if isinstance(sample_size, bool) or not isinstance(sample_size, int):
        raise TypeError("sample_size must be an integer.")
    if sample_size <= 0:
        raise ValueError("sample_size must be positive.")
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
    counts = rng.multinomial(sample_size, current_array, size=simulations)
    observed = counts.astype(np.float64) / float(sample_size)

    differences = observed - reference_array
    prs_values = np.sum(np.square(differences) / reference_array, axis=1)

    prs_green = prs_values <= thresholds.lower
    prs_red = prs_values > thresholds.upper
    prs_amber = ~(prs_green | prs_red)

    with np.errstate(divide="ignore", invalid="ignore"):
        positive = observed > 0.0
        log_observed = np.where(positive, np.log(observed), 0.0)
        log_reference = np.log(reference_array)
        psi_terms = np.where(
            positive,
            differences * (log_observed - log_reference),
            0.0,
        )
        psi_values = np.sum(psi_terms, axis=1)

    psi_green = np.array(
        [lewis_psi_status(float(value)) == "green" for value in psi_values],
        dtype=bool,
    )
    psi_red = np.array(
        [lewis_psi_status(float(value)) == "red" for value in psi_values],
        dtype=bool,
    )
    psi_amber = ~(psi_green | psi_red)

    return PRSPSIComparisonResult(
        simulations=simulations,
        prs=ClassificationProbabilities(
            green=float(np.mean(prs_green)),
            amber=float(np.mean(prs_amber)),
            red=float(np.mean(prs_red)),
        ),
        psi=ClassificationProbabilities(
            green=float(np.mean(psi_green)),
            amber=float(np.mean(psi_amber)),
            red=float(np.mean(psi_red)),
        ),
    )
