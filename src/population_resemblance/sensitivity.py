"""Sensitivity grids for PRS calibration parameters."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import product

import numpy as np
import numpy.typing as npt

from population_resemblance.calibration import (
    CalibrationDiagnostics,
    evaluate_calibration,
)


@dataclass(frozen=True, slots=True)
class CalibrationSensitivityPoint:
    """One parameter combination in a PRS calibration sensitivity grid."""

    c: float
    m: float
    alpha1: float
    alpha2: float
    diagnostics: CalibrationDiagnostics | None
    error: str | None

    @property
    def feasible(self) -> bool:
        """Return whether this parameter combination produced a valid calibration."""
        return self.diagnostics is not None and self.error is None


@dataclass(frozen=True, slots=True)
class CalibrationSensitivityGrid:
    """Collection of PRS calibration results over a parameter grid."""

    points: tuple[CalibrationSensitivityPoint, ...]

    @property
    def feasible_points(self) -> tuple[CalibrationSensitivityPoint, ...]:
        """Return all valid calibration combinations."""
        return tuple(point for point in self.points if point.feasible)

    @property
    def infeasible_points(self) -> tuple[CalibrationSensitivityPoint, ...]:
        """Return all parameter combinations rejected by the PRS constraints."""
        return tuple(point for point in self.points if not point.feasible)


def _validated_values(
    values: Sequence[float],
    *,
    name: str,
    lower: float,
    upper: float | None = None,
    strict_lower: bool = False,
) -> tuple[float, ...]:
    """Validate a non-empty sequence of finite scalar parameter values."""
    resolved = tuple(float(value) for value in values)
    if not resolved:
        raise ValueError(f"{name} must contain at least one value.")

    for value in resolved:
        if not np.isfinite(value):
            raise ValueError(f"{name} must contain only finite values.")
        if strict_lower:
            if value <= lower:
                raise ValueError(f"{name} values must be greater than {lower}.")
        elif value < lower:
            raise ValueError(f"{name} values must be at least {lower}.")
        if upper is not None and value > upper:
            raise ValueError(f"{name} values must not exceed {upper}.")

    return resolved


def sweep_calibration_parameters(
    reference: Sequence[float] | npt.NDArray[np.floating],
    sample_size: int,
    *,
    c_values: Sequence[float] = (0.5, 0.7, 1.0),
    m_values: Sequence[float] = (1.2, 1.5, 2.0),
    alpha1_values: Sequence[float] = (0.05,),
    alpha2_values: Sequence[float] = (0.10,),
) -> CalibrationSensitivityGrid:
    """Evaluate PRS calibration across a Cartesian parameter grid.

    Invalid combinations are retained with an explanatory error rather than
    aborting the entire sweep. This makes structural constraints such as
    M * delta <= min(p0) visible during sensitivity analysis.
    """
    resolved_c = _validated_values(
        c_values,
        name="c_values",
        lower=0.0,
        strict_lower=True,
    )
    resolved_m = _validated_values(
        m_values,
        name="m_values",
        lower=1.0,
        strict_lower=True,
    )
    resolved_alpha1 = _validated_values(
        alpha1_values,
        name="alpha1_values",
        lower=0.0,
        upper=1.0,
    )
    resolved_alpha2 = _validated_values(
        alpha2_values,
        name="alpha2_values",
        lower=0.0,
        upper=1.0,
    )

    points: list[CalibrationSensitivityPoint] = []

    for c, m, alpha1, alpha2 in product(
        resolved_c,
        resolved_m,
        resolved_alpha1,
        resolved_alpha2,
    ):
        try:
            diagnostics = evaluate_calibration(
                reference=reference,
                sample_size=sample_size,
                c=c,
                m=m,
                alpha1=alpha1,
                alpha2=alpha2,
            )
        except ValueError as exc:
            points.append(
                CalibrationSensitivityPoint(
                    c=c,
                    m=m,
                    alpha1=alpha1,
                    alpha2=alpha2,
                    diagnostics=None,
                    error=str(exc),
                )
            )
        else:
            points.append(
                CalibrationSensitivityPoint(
                    c=c,
                    m=m,
                    alpha1=alpha1,
                    alpha2=alpha2,
                    diagnostics=diagnostics,
                    error=None,
                )
            )

    return CalibrationSensitivityGrid(points=tuple(points))
