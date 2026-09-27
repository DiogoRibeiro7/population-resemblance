"""Population Stability Index benchmark implementation."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt

from population_resemblance.prs import _as_probability_vector


def population_stability_index(
    observed: Sequence[float] | npt.NDArray[np.floating],
    reference: Sequence[float] | npt.NDArray[np.floating],
) -> float:
    """Compute the Population Stability Index (PSI).

    This follows the formulation used in the source paper, including its
    convention of omitting categories whose observed probability is zero.
    """
    observed_array = _as_probability_vector(observed, name="observed")
    reference_array = _as_probability_vector(reference, name="reference")

    if observed_array.shape != reference_array.shape:
        raise ValueError("observed and reference must have the same number of categories.")
    if np.any(reference_array <= 0.0):
        raise ValueError("reference probabilities must be strictly positive.")

    positive = observed_array > 0.0
    observed_positive = observed_array[positive]
    reference_positive = reference_array[positive]

    terms = (
        (observed_positive - reference_positive)
        * (np.log(observed_positive) - np.log(reference_positive))
    )
    return float(np.sum(terms))


def lewis_psi_status(psi: float) -> str:
    """Classify PSI using the traditional Lewis rule-of-thumb thresholds.

    The thresholds are retained only as a benchmark: below 0.10 is green,
    0.10 up to 0.25 is amber, and 0.25 or above is red.
    """
    if not np.isfinite(psi):
        raise ValueError("psi must be finite.")
    if psi < 0.0:
        raise ValueError("psi must be non-negative.")
    if psi < 0.10:
        return "green"
    if psi < 0.25:
        return "amber"
    return "red"
