"""Tests for PRS calibration sensitivity grids."""

from __future__ import annotations

import pytest

from population_resemblance import sweep_calibration_parameters


def test_sensitivity_grid_evaluates_cartesian_product() -> None:
    """All requested parameter combinations should be evaluated."""
    grid = sweep_calibration_parameters(
        reference=[0.2] * 5,
        sample_size=100,
        c_values=[0.5, 0.7],
        m_values=[1.5, 2.0],
        alpha1_values=[0.05, 0.10],
        alpha2_values=[0.10],
    )

    assert len(grid.points) == 8


def test_standard_source_configuration_is_feasible() -> None:
    """A standard paper-style calibration should remain valid."""
    grid = sweep_calibration_parameters(
        reference=[0.2] * 5,
        sample_size=50,
        c_values=[0.7],
        m_values=[2.0],
        alpha1_values=[0.05],
        alpha2_values=[0.10],
    )

    assert len(grid.feasible_points) == 1
    point = grid.feasible_points[0]
    assert point.diagnostics is not None
    assert point.diagnostics.delta == pytest.approx(0.039598, abs=5e-7)


def test_infeasible_combinations_are_retained() -> None:
    """Structural failures should be recorded rather than aborting the sweep."""
    grid = sweep_calibration_parameters(
        reference=[0.8, 0.1, 0.1],
        sample_size=100,
        c_values=[0.5, 2.0],
        m_values=[2.0],
        alpha1_values=[0.05],
        alpha2_values=[0.10],
    )

    assert len(grid.points) == 2
    assert len(grid.infeasible_points) >= 1
    assert all(point.error is not None for point in grid.infeasible_points)


def test_feasible_and_infeasible_partition_grid() -> None:
    """Every sensitivity point must belong to exactly one feasibility group."""
    grid = sweep_calibration_parameters(
        reference=[0.6, 0.3, 0.1],
        sample_size=50,
        c_values=[0.5, 1.0, 2.0],
        m_values=[1.2, 2.0],
    )

    assert len(grid.feasible_points) + len(grid.infeasible_points) == len(grid.points)


@pytest.mark.parametrize(
    ("keyword", "values"),
    [
        ("c_values", []),
        ("c_values", [0.0]),
        ("m_values", [1.0]),
        ("alpha1_values", [-0.1]),
        ("alpha2_values", [1.1]),
    ],
)
def test_invalid_parameter_grids_raise(keyword: str, values: list[float]) -> None:
    """Malformed sensitivity grids should fail before evaluation."""
    kwargs = {keyword: values}

    with pytest.raises(ValueError):
        sweep_calibration_parameters(
            reference=[0.5, 0.5],
            sample_size=100,
            **kwargs,
        )
