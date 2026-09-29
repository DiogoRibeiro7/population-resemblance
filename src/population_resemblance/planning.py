"""Structural sample-size planning for recommended PRS tolerances."""

from __future__ import annotations

from collections.abc import Sequence
from math import ceil

import numpy as np
import numpy.typing as npt

from population_resemblance.framework import (
    _reference_vector,
    _validate_positive,
    recommended_delta,
)


def minimum_structural_sample_size(
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    c: float = 0.7,
    m: float = 2.0,
) -> int:
    """Return the smallest sample size satisfying the PRS probability bound.

    For the recommended tolerance delta = c * min_j sqrt(p0_j * (1 - p0_j) / n),
    the nested PRS framework requires m * delta <= min_j p0_j.

    This function solves that inequality for the minimum positive integer
    sample size. The result is a structural feasibility bound only. It does
    not guarantee adequate power, finite-sample calibration, or asymptotic
    accuracy.

    Parameters
    ----------
    reference:
        Fixed reference categorical probability distribution.
    c:
        Multiplier used by the recommended sample-size-aware tolerance.
    m:
        Multiplier defining the wider resemblance region. Must exceed one.

    Returns
    -------
    int
        Smallest positive integer sample size satisfying the structural bound.
    """
    reference_array = _reference_vector(reference)
    _validate_positive(c, name="c")
    _validate_positive(m, name="m")

    if m <= 1.0:
        raise ValueError("m must be greater than 1.")

    minimum_probability = float(np.min(reference_array))
    minimum_scale = float(
        np.min(np.sqrt(reference_array * (1.0 - reference_array)))
    )

    raw_bound = (m * c * minimum_scale / minimum_probability) ** 2
    candidate = max(1, ceil(raw_bound))

    while m * recommended_delta(reference_array, candidate, c=c) > minimum_probability:
        candidate += 1

    while (
        candidate > 1
        and m * recommended_delta(reference_array, candidate - 1, c=c)
        <= minimum_probability
    ):
        candidate -= 1

    return candidate
