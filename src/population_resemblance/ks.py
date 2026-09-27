"""Discrete Kolmogorov-Smirnov benchmark for categorical distributions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.counts import _as_count_vector
from population_resemblance.prs import _as_probability_vector


@dataclass(frozen=True, slots=True)
class DiscreteKSTestResult:
    """Monte Carlo calibrated discrete Kolmogorov-Smirnov test result."""

    statistic: float
    p_value: float
    simulations: int
    sample_size: int

    @property
    def status(self) -> str:
        """Return the paper-style green/amber/red p-value classification."""
        return discrete_ks_status(self.p_value)


def discrete_ks_statistic(
    observed: Sequence[float] | npt.NDArray[np.floating],
    reference: Sequence[float] | npt.NDArray[np.floating],
) -> float:
    """Compute the discrete Kolmogorov-Smirnov statistic.

    The statistic is the maximum absolute difference between the empirical
    cumulative distribution and the reference cumulative distribution.

    Parameters
    ----------
    observed:
        Current categorical probability distribution.
    reference:
        Reference categorical probability distribution.

    Returns
    -------
    float
        Maximum absolute cumulative-distribution difference.
    """
    observed_array = _as_probability_vector(observed, name="observed")
    reference_array = _as_probability_vector(reference, name="reference")

    if observed_array.shape != reference_array.shape:
        raise ValueError("observed and reference must have the same number of categories.")

    observed_cdf = np.cumsum(observed_array)
    reference_cdf = np.cumsum(reference_array)
    return float(np.max(np.abs(observed_cdf - reference_cdf)))


def discrete_ks_test_counts(
    counts: Sequence[int] | npt.NDArray[np.integer],
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    simulations: int = 10_000,
    seed: int | None = None,
) -> DiscreteKSTestResult:
    """Monte Carlo calibrate the discrete KS statistic under the reference model.

    The null distribution is simulated from the multinomial reference because
    the discrete KS statistic is not distribution-free with respect to the
    underlying categorical probabilities.

    Parameters
    ----------
    counts:
        Observed category counts.
    reference:
        Reference categorical probability distribution.
    simulations:
        Number of Monte Carlo samples used for calibration.
    seed:
        Optional random seed for reproducibility.

    Returns
    -------
    DiscreteKSTestResult
        Statistic, Monte Carlo p-value, simulation count, and sample size.
    """
    count_array = _as_count_vector(counts)
    reference_array = _as_probability_vector(reference, name="reference")

    if count_array.shape != reference_array.shape:
        raise ValueError("counts and reference must have the same number of categories.")
    if isinstance(simulations, bool) or not isinstance(simulations, int):
        raise TypeError("simulations must be an integer.")
    if simulations <= 0:
        raise ValueError("simulations must be positive.")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None.")

    sample_size = int(np.sum(count_array, dtype=np.int64))
    observed = count_array.astype(np.float64) / float(sample_size)
    statistic = discrete_ks_statistic(observed, reference_array)

    reference_cdf = np.cumsum(reference_array)
    rng = np.random.default_rng(seed)
    simulated_counts = rng.multinomial(
        sample_size,
        reference_array,
        size=simulations,
    )
    simulated_cdfs = np.cumsum(simulated_counts, axis=1) / float(sample_size)
    simulated_statistics = np.max(
        np.abs(simulated_cdfs - reference_cdf),
        axis=1,
    )

    # Add-one correction avoids reporting an impossible Monte Carlo p-value of zero.
    exceedances = int(np.count_nonzero(simulated_statistics >= statistic))
    p_value = (exceedances + 1.0) / (simulations + 1.0)

    return DiscreteKSTestResult(
        statistic=statistic,
        p_value=float(p_value),
        simulations=simulations,
        sample_size=sample_size,
    )


def discrete_ks_status(
    p_value: float,
    *,
    red_alpha: float = 0.01,
    green_alpha: float = 0.10,
) -> str:
    """Classify a discrete KS p-value using the paper's comparison thresholds.

    Values below 1% are red, values above 10% are green, and intermediate
    values are amber by default.
    """
    if not np.isfinite(p_value) or not 0.0 <= p_value <= 1.0:
        raise ValueError("p_value must be finite and lie in [0, 1].")
    if not np.isfinite(red_alpha) or not np.isfinite(green_alpha):
        raise ValueError("classification thresholds must be finite.")
    if not 0.0 <= red_alpha < green_alpha <= 1.0:
        raise ValueError("require 0 <= red_alpha < green_alpha <= 1.")

    if p_value < red_alpha:
        return "red"
    if p_value > green_alpha:
        return "green"
    return "amber"
