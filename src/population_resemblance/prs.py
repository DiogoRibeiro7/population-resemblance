"""Core Population Resemblance Statistic implementation."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt


def _as_probability_vector(
    values: Sequence[float] | npt.NDArray[np.floating],
    *,
    name: str,
) -> npt.NDArray[np.float64]:
    """Validate and normalize a probability vector input.

    Parameters
    ----------
    values:
        One-dimensional sequence of probability values.
    name:
        Human-readable variable name used in validation errors.

    Returns
    -------
    numpy.ndarray
        A one-dimensional float64 probability vector.

    Raises
    ------
    ValueError
        If the input is not one-dimensional, contains invalid values, or does not sum to one.
    """
    array = np.asarray(values, dtype=np.float64)

    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional.")
    if array.size < 2:
        raise ValueError(f"{name} must contain at least two categories.")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values.")
    if np.any(array < 0.0):
        raise ValueError(f"{name} must not contain negative probabilities.")
    if not np.isclose(float(array.sum()), 1.0, rtol=1e-10, atol=1e-12):
        raise ValueError(f"{name} must sum to 1.")

    return array


def population_resemblance_statistic(
    observed: Sequence[float] | npt.NDArray[np.floating],
    reference: Sequence[float] | npt.NDArray[np.floating],
) -> float:
    """Compute the Population Resemblance Statistic (PRS).

    The statistic is

    .. math::

        \mathrm{PRS} = \sum_j \frac{(\hat p_j - p_{0j})^2}{p_{0j}}.

    Parameters
    ----------
    observed:
        Current categorical probability distribution.
    reference:
        Reference categorical probability distribution.

    Returns
    -------
    float
        The PRS value.

    Raises
    ------
    ValueError
        If the vectors are invalid, have different lengths, or the reference contains zeros.
    """
    observed_array = _as_probability_vector(observed, name="observed")
    reference_array = _as_probability_vector(reference, name="reference")

    if observed_array.shape != reference_array.shape:
        raise ValueError("observed and reference must have the same number of categories.")
    if np.any(reference_array <= 0.0):
        raise ValueError("reference probabilities must be strictly positive.")

    differences = observed_array - reference_array
    return float(np.sum(np.square(differences) / reference_array))
