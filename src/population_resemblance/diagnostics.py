"""Category-level diagnostics for Population Resemblance Statistic results."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.counts import _as_count_vector
from population_resemblance.prs import _as_probability_vector


@dataclass(frozen=True, slots=True)
class CategoryContribution:
    """Contribution of one category to the overall PRS value."""

    category: str
    observed_probability: float
    reference_probability: float
    signed_shift: float
    absolute_shift: float
    prs_contribution: float
    contribution_share: float


@dataclass(frozen=True, slots=True)
class ResemblanceDiagnostics:
    """Decomposition of PRS into category-level contributions."""

    statistic: float
    categories: tuple[CategoryContribution, ...]

    @property
    def largest_contributor(self) -> CategoryContribution:
        """Return the category contributing most to the PRS statistic."""
        return max(self.categories, key=lambda item: item.prs_contribution)

    @property
    def maximum_absolute_shift(self) -> float:
        """Return the largest absolute category probability shift."""
        return max(item.absolute_shift for item in self.categories)


def population_resemblance_diagnostics(
    observed: Sequence[float] | npt.NDArray[np.floating],
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    labels: Sequence[str] | None = None,
) -> ResemblanceDiagnostics:
    """Decompose PRS into interpretable category-level contributions.

    Parameters
    ----------
    observed:
        Current categorical probability distribution.
    reference:
        Reference categorical probability distribution.
    labels:
        Optional category labels. If omitted, labels are generated as
        category_1, category_2, and so on.

    Returns
    -------
    ResemblanceDiagnostics
        Overall PRS statistic and per-category contribution details.
    """
    observed_array = _as_probability_vector(observed, name="observed")
    reference_array = _as_probability_vector(reference, name="reference")

    if observed_array.shape != reference_array.shape:
        raise ValueError("observed and reference must have the same number of categories.")
    if np.any(reference_array <= 0.0):
        raise ValueError("reference probabilities must be strictly positive.")

    category_count = int(observed_array.size)

    if labels is None:
        resolved_labels = tuple(
            f"category_{index + 1}" for index in range(category_count)
        )
    else:
        if len(labels) != category_count:
            raise ValueError("labels must match the number of categories.")
        if any(not isinstance(label, str) or not label for label in labels):
            raise ValueError("labels must contain non-empty strings.")
        resolved_labels = tuple(labels)

    shifts = observed_array - reference_array
    contributions = np.square(shifts) / reference_array
    statistic = float(np.sum(contributions))

    if statistic == 0.0:
        shares = np.zeros_like(contributions)
    else:
        shares = contributions / statistic

    categories = tuple(
        CategoryContribution(
            category=label,
            observed_probability=float(observed_value),
            reference_probability=float(reference_value),
            signed_shift=float(shift),
            absolute_shift=float(abs(shift)),
            prs_contribution=float(contribution),
            contribution_share=float(share),
        )
        for label, observed_value, reference_value, shift, contribution, share in zip(
            resolved_labels,
            observed_array,
            reference_array,
            shifts,
            contributions,
            shares,
            strict=True,
        )
    )

    return ResemblanceDiagnostics(statistic=statistic, categories=categories)


def population_count_diagnostics(
    counts: Sequence[int] | npt.NDArray[np.integer],
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    labels: Sequence[str] | None = None,
) -> ResemblanceDiagnostics:
    """Decompose PRS directly from observed category counts.

    The empirical distribution is derived from the supplied count vector before
    delegating to the probability-based diagnostic implementation.
    """
    count_array = _as_count_vector(counts)
    sample_size = int(np.sum(count_array, dtype=np.int64))
    observed = count_array.astype(np.float64) / float(sample_size)

    return population_resemblance_diagnostics(
        observed=observed,
        reference=reference,
        labels=labels,
    )
