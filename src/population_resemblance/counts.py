"""Utilities for assessing observed categorical count data."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt

from population_resemblance.framework import assess_population_resemblance
from population_resemblance.result import PopulationResemblanceResult


def _as_count_vector(
    counts: Sequence[int] | npt.NDArray[np.integer],
    *,
    name: str = "counts",
) -> npt.NDArray[np.int64]:
    """Validate and return a one-dimensional vector of non-negative counts.

    Parameters
    ----------
    counts:
        Observed category counts.
    name:
        Human-readable name used in validation errors.

    Returns
    -------
    numpy.ndarray
        Validated integer counts.

    Raises
    ------
    TypeError
        If counts are not integer-valued.
    ValueError
        If counts are not one-dimensional, contain negative values, contain
        fewer than two categories, or sum to zero.
    """
    array = np.asarray(counts)

    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional.")
    if array.size < 2:
        raise ValueError(f"{name} must contain at least two categories.")
    if np.issubdtype(array.dtype, np.bool_) or not np.issubdtype(array.dtype, np.integer):
        raise TypeError(f"{name} must contain integer counts.")
    if np.any(array < 0):
        raise ValueError(f"{name} must not contain negative counts.")

    count_array = array.astype(np.int64, copy=False)
    if int(np.sum(count_array, dtype=np.int64)) <= 0:
        raise ValueError(f"{name} must contain at least one observation.")

    return count_array


def counts_to_proportions(
    counts: Sequence[int] | npt.NDArray[np.integer],
) -> npt.NDArray[np.float64]:
    """Convert categorical counts to empirical proportions.

    Parameters
    ----------
    counts:
        Observed category counts.

    Returns
    -------
    numpy.ndarray
        Empirical category proportions that sum to one.
    """
    count_array = _as_count_vector(counts)
    sample_size = int(np.sum(count_array, dtype=np.int64))
    return count_array.astype(np.float64) / float(sample_size)


def assess_population_counts(
    counts: Sequence[int] | npt.NDArray[np.integer],
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> PopulationResemblanceResult:
    """Assess observed counts against a fixed reference distribution.

    The current sample size is derived directly from the count vector, which
    prevents inconsistencies between empirical proportions and the supplied
    sample size.

    Parameters
    ----------
    counts:
        Current observed counts by category.
    reference:
        Fixed reference probability distribution.
    delta:
        Optional explicit resemblance tolerance. If omitted, the framework's
        sample-size-aware recommendation is used.
    c:
        Positive multiplier used when automatically calibrating delta.
    m:
        Multiplier defining the wider resemblance region.
    alpha1:
        Error-control parameter for the upper decision boundary.
    alpha2:
        Error-control parameter for the lower decision boundary.

    Returns
    -------
    PopulationResemblanceResult
        Complete PRS assessment.
    """
    count_array = _as_count_vector(counts)
    sample_size = int(np.sum(count_array, dtype=np.int64))
    observed = count_array.astype(np.float64) / float(sample_size)

    return assess_population_resemblance(
        observed=observed,
        reference=reference,
        sample_size=sample_size,
        delta=delta,
        c=c,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
    )
