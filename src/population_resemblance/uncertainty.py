"""Uncertainty summaries for Monte Carlo classification probabilities."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from scipy.stats import norm

from population_resemblance.simulation import SimulationResult


@dataclass(frozen=True, slots=True)
class ProbabilityInterval:
    """Point estimate and confidence interval for a simulated probability."""

    estimate: float
    lower: float
    upper: float


@dataclass(frozen=True, slots=True)
class SimulationUncertainty:
    """Confidence intervals for PRS region probabilities."""

    confidence_level: float
    r1: ProbabilityInterval
    r2: ProbabilityInterval
    r3: ProbabilityInterval


def _wilson_interval(
    successes: float,
    trials: int,
    *,
    confidence_level: float,
) -> ProbabilityInterval:
    """Compute a Wilson score interval for a binomial proportion."""
    if trials <= 0:
        raise ValueError("trials must be positive.")
    if not 0.0 <= successes <= trials:
        raise ValueError("successes must lie between 0 and trials.")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie strictly between 0 and 1.")

    estimate = successes / trials
    z = float(norm.ppf(0.5 + confidence_level / 2.0))
    z2 = z * z
    denominator = 1.0 + z2 / trials
    center = (estimate + z2 / (2.0 * trials)) / denominator
    half_width = (
        z
        * sqrt(
            estimate * (1.0 - estimate) / trials
            + z2 / (4.0 * trials * trials)
        )
        / denominator
    )

    return ProbabilityInterval(
        estimate=float(estimate),
        lower=max(0.0, float(center - half_width)),
        upper=min(1.0, float(center + half_width)),
    )


def simulation_uncertainty(
    result: SimulationResult,
    *,
    confidence_level: float = 0.95,
) -> SimulationUncertainty:
    """Attach Wilson confidence intervals to Monte Carlo region probabilities.

    These intervals quantify Monte Carlo simulation error only. They are not
    confidence intervals for the underlying PRS parameters or population shift.
    """
    trials = result.simulations

    return SimulationUncertainty(
        confidence_level=confidence_level,
        r1=_wilson_interval(
            result.r1_probability * trials,
            trials,
            confidence_level=confidence_level,
        ),
        r2=_wilson_interval(
            result.r2_probability * trials,
            trials,
            confidence_level=confidence_level,
        ),
        r3=_wilson_interval(
            result.r3_probability * trials,
            trials,
            confidence_level=confidence_level,
        ),
    )
