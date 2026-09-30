"""Experimental independent two-sample population resemblance assessment.

This module is intentionally outside the package-root stable API. It implements the
independent-sample plug-in procedure derived in the repository research notes.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.stats import ncx2

from population_resemblance.counts import _as_count_vector
from population_resemblance.result import CriticalValues, DecisionRegion


@dataclass(frozen=True, slots=True)
class ExperimentalTwoSampleResult:
    """Result of an experimental independent two-sample resemblance assessment."""

    statistic: float
    effective_sample_size: float
    pooled_probabilities: tuple[float, ...]
    delta: float
    lambda_sup: float
    critical_values: CriticalValues
    region: DecisionRegion
    first_sample_size: int
    second_sample_size: int
    minimum_expected_count: float
    structural_margin: float

    @property
    def label(self) -> str:
        """Return the descriptive decision-region label."""
        return self.region.label


def _validate_probability_parameter(value: float, *, name: str) -> None:
    """Validate a finite probability parameter in [0, 1]."""
    if not np.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1].")


def _validate_positive(value: float, *, name: str) -> None:
    """Validate a finite positive scalar."""
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be a positive finite value.")


def _lambda_sup(
    pooled: npt.NDArray[np.float64],
    effective_sample_size: float,
    delta: float,
) -> float:
    """Compute the fixed-centre least-favourable non-centrality."""
    inverse_sum = float(np.sum(1.0 / pooled))
    if pooled.size % 2 == 1:
        inverse_sum -= 1.0 / float(np.max(pooled))
    return effective_sample_size * delta**2 * inverse_sum


def assess_independent_two_sample_resemblance(
    first_counts: Sequence[int] | npt.NDArray[np.integer],
    second_counts: Sequence[int] | npt.NDArray[np.integer],
    *,
    samples_are_independent: bool,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
    minimum_expected_count: float = 5.0,
) -> ExperimentalTwoSampleResult:
    """Assess two independent categorical samples with the experimental method.

    This API is experimental and intentionally not exported from the stable
    package-root public API.
    """
    if samples_are_independent is not True:
        raise ValueError(
            "experimental two-sample resemblance currently supports "
            "independent samples only."
        )

    first = _as_count_vector(first_counts, name="first_counts")
    second = _as_count_vector(second_counts, name="second_counts")

    if first.shape != second.shape:
        raise ValueError("first_counts and second_counts must have the same shape.")

    _validate_positive(c, name="c")
    _validate_positive(m, name="m")
    _validate_positive(minimum_expected_count, name="minimum_expected_count")
    _validate_probability_parameter(alpha1, name="alpha1")
    _validate_probability_parameter(alpha2, name="alpha2")

    if m <= 1.0:
        raise ValueError("m must be greater than 1.")

    n = int(np.sum(first, dtype=np.int64))
    second_n = int(np.sum(second, dtype=np.int64))
    total = n + second_n

    pooled_counts = first + second
    if np.any(pooled_counts == 0):
        raise ValueError(
            "zero_pooled_category: every pooled category must contain observations."
        )

    pooled = pooled_counts.astype(np.float64) / float(total)
    minimum_pooled_probability = float(np.min(pooled))
    minimum_expected = min(n, second_n) * minimum_pooled_probability

    if minimum_expected < minimum_expected_count:
        raise ValueError(
            "insufficient_expected_count: minimum pooled expected count "
            f"{minimum_expected:.6g} is below {minimum_expected_count:.6g}."
        )

    effective_sample_size = n * second_n / float(total)
    rho = n / float(total)

    resolved_delta = (
        float(
            c
            * np.min(
                np.sqrt(
                    pooled * (1.0 - pooled) / effective_sample_size
                )
            )
        )
        if delta is None
        else float(delta)
    )
    _validate_positive(resolved_delta, name="delta")

    probability_bound = float(
        np.min(np.minimum(pooled, 1.0 - pooled))
        / max(rho, 1.0 - rho)
    )
    structural_margin = probability_bound - m * resolved_delta

    if structural_margin < 0.0:
        raise ValueError(
            "structural_probability_bound: m * delta exceeds the "
            "two-sample probability-domain bound."
        )

    first_proportions = first.astype(np.float64) / float(n)
    second_proportions = second.astype(np.float64) / float(second_n)
    difference = first_proportions - second_proportions

    statistic = float(
        effective_sample_size
        * np.sum(np.square(difference) / pooled)
    )

    lambda_sup = _lambda_sup(
        pooled,
        effective_sample_size,
        resolved_delta,
    )
    degrees_of_freedom = int(pooled.size - 1)

    lower = float(
        ncx2.ppf(
            alpha2,
            degrees_of_freedom,
            m**2 * lambda_sup,
        )
    )
    upper = float(
        ncx2.ppf(
            1.0 - alpha1,
            degrees_of_freedom,
            lambda_sup,
        )
    )

    if np.isnan(lower) or np.isnan(upper):
        raise ValueError("parameters produced undefined critical values.")
    if lower > upper:
        raise ValueError("parameters produce overlapping decision boundaries.")

    thresholds = CriticalValues(lower=lower, upper=upper)

    if statistic <= lower:
        region = DecisionRegion.R1
    elif statistic <= upper:
        region = DecisionRegion.R2
    else:
        region = DecisionRegion.R3

    return ExperimentalTwoSampleResult(
        statistic=statistic,
        effective_sample_size=effective_sample_size,
        pooled_probabilities=tuple(float(value) for value in pooled),
        delta=resolved_delta,
        lambda_sup=lambda_sup,
        critical_values=thresholds,
        region=region,
        first_sample_size=n,
        second_sample_size=second_n,
        minimum_expected_count=minimum_expected,
        structural_margin=structural_margin,
    )
