"""Operating-characteristic curves for the PRS decision framework."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.framework import recommended_delta
from population_resemblance.simulation import (
    SimulationResult,
    simulate_region_probabilities,
    symmetric_category_shift,
)


@dataclass(frozen=True, slots=True)
class OperatingCharacteristicPoint:
    """One simulated operating-characteristic point."""

    delta_multiple: float
    deviation: float
    result: SimulationResult


@dataclass(frozen=True, slots=True)
class OperatingCharacteristicCurve:
    """Ordered PRS operating-characteristic results over increasing deviations."""

    delta: float
    points: tuple[OperatingCharacteristicPoint, ...]

    @property
    def delta_multiples(self) -> tuple[float, ...]:
        """Return deviation sizes measured in multiples of delta."""
        return tuple(point.delta_multiple for point in self.points)

    @property
    def deviations(self) -> tuple[float, ...]:
        """Return absolute category-wise deviations."""
        return tuple(point.deviation for point in self.points)

    @property
    def r1_probabilities(self) -> tuple[float, ...]:
        """Return empirical R1 probabilities along the curve."""
        return tuple(point.result.r1_probability for point in self.points)

    @property
    def r2_probabilities(self) -> tuple[float, ...]:
        """Return empirical R2 probabilities along the curve."""
        return tuple(point.result.r2_probability for point in self.points)

    @property
    def r3_probabilities(self) -> tuple[float, ...]:
        """Return empirical R3 probabilities along the curve."""
        return tuple(point.result.r3_probability for point in self.points)


def source_deviation_grid(
    *,
    m: float = 2.0,
    points: int = 30,
) -> tuple[float, ...]:
    """Return the deviation grid used by the source simulation design.

    The source paper studies deviations from zero to (3M + 2) times delta.
    This helper returns equally spaced multiples of delta over that interval.

    Parameters
    ----------
    m:
        Wider resemblance multiplier.
    points:
        Number of equally spaced deviation values.

    Returns
    -------
    tuple[float, ...]
        Deviation sizes expressed as multiples of delta.
    """
    if not np.isfinite(m) or m <= 1.0:
        raise ValueError("m must be finite and greater than 1.")
    if isinstance(points, bool) or not isinstance(points, int):
        raise TypeError("points must be an integer.")
    if points < 2:
        raise ValueError("points must be at least 2.")

    return tuple(float(value) for value in np.linspace(0.0, 3.0 * m + 2.0, points))


def simulate_operating_characteristic_curve(
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    *,
    delta_multiples: Sequence[float] | None = None,
    simulations: int = 10_000,
    seed: int | None = None,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> OperatingCharacteristicCurve:
    """Simulate PRS decision probabilities over a sequence of shift magnitudes.

    Each point uses the symmetric category perturbation employed in the source
    simulation study. The result is an operating-characteristic curve rather
    than conventional statistical power, because the PRS framework uses nested
    composite null hypotheses.

    Parameters
    ----------
    reference:
        Fixed reference categorical probability distribution.
    sample_size:
        Number of observations in each Monte Carlo sample.
    delta_multiples:
        Shift magnitudes expressed as multiples of delta. If omitted, the
        source paper's 30-point grid from zero to (3M + 2) delta is used.
    simulations:
        Monte Carlo samples per curve point.
    seed:
        Optional base random seed. Each curve point receives a deterministic
        seed offset.
    delta:
        Optional explicit resemblance tolerance.
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
    OperatingCharacteristicCurve
        Ordered simulation results across the requested deviation magnitudes.
    """
    reference_array = np.asarray(reference, dtype=np.float64)

    resolved_delta = (
        recommended_delta(reference_array, sample_size, c=c)
        if delta is None
        else float(delta)
    )

    if delta_multiples is None:
        resolved_multiples = source_deviation_grid(m=m, points=30)
    else:
        resolved_multiples = tuple(float(value) for value in delta_multiples)

    if not resolved_multiples:
        raise ValueError("delta_multiples must contain at least one value.")
    if any(not np.isfinite(value) or value < 0.0 for value in resolved_multiples):
        raise ValueError("delta_multiples must contain finite non-negative values.")

    curve_points: list[OperatingCharacteristicPoint] = []

    for index, multiple in enumerate(resolved_multiples):
        deviation = multiple * resolved_delta
        current = symmetric_category_shift(reference_array, deviation)
        point_seed = None if seed is None else seed + index

        result = simulate_region_probabilities(
            current=current,
            reference=reference_array,
            sample_size=sample_size,
            simulations=simulations,
            seed=point_seed,
            delta=resolved_delta,
            c=c,
            m=m,
            alpha1=alpha1,
            alpha2=alpha2,
        )

        curve_points.append(
            OperatingCharacteristicPoint(
                delta_multiple=multiple,
                deviation=deviation,
                result=result,
            )
        )

    return OperatingCharacteristicCurve(
        delta=resolved_delta,
        points=tuple(curve_points),
    )
