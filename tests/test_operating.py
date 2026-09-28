"""Tests for PRS operating-characteristic curve simulation."""

from __future__ import annotations

import pytest

from population_resemblance import (
    simulate_operating_characteristic_curve,
    source_deviation_grid,
)


def test_source_grid_matches_paper_range() -> None:
    """The source grid should span zero to (3M + 2) delta."""
    grid = source_deviation_grid(m=2.0, points=30)

    assert len(grid) == 30
    assert grid[0] == pytest.approx(0.0)
    assert grid[-1] == pytest.approx(8.0)


def test_operating_curve_preserves_requested_multiples() -> None:
    """Curve points should preserve the requested deviation ordering."""
    curve = simulate_operating_characteristic_curve(
        reference=[0.2] * 5,
        sample_size=50,
        delta_multiples=[0.0, 1.0, 2.0],
        simulations=1_000,
        seed=10,
    )

    assert curve.delta_multiples == pytest.approx((0.0, 1.0, 2.0))
    assert len(curve.points) == 3


def test_each_operating_point_is_a_complete_probability_partition() -> None:
    """Every curve point must classify all simulations into R1, R2, or R3."""
    curve = simulate_operating_characteristic_curve(
        reference=[0.25] * 4,
        sample_size=100,
        delta_multiples=[0.0, 0.5, 1.0],
        simulations=1_500,
        seed=20,
    )

    for point in curve.points:
        assert sum(point.result.probabilities) == pytest.approx(1.0)


def test_operating_curve_is_reproducible() -> None:
    """A fixed base seed should reproduce the complete curve."""
    reference = [0.2] * 5
    delta_multiples = [0.0, 1.0, 2.0]

    first = simulate_operating_characteristic_curve(
        reference=reference,
        sample_size=50,
        delta_multiples=delta_multiples,
        simulations=1_000,
        seed=123,
    )
    second = simulate_operating_characteristic_curve(
        reference=reference,
        sample_size=50,
        delta_multiples=delta_multiples,
        simulations=1_000,
        seed=123,
    )

    assert first == second


def test_larger_shift_increases_mean_prs_in_deterministic_example() -> None:
    """A large structured shift should increase the mean simulated PRS."""
    curve = simulate_operating_characteristic_curve(
        reference=[0.2] * 5,
        sample_size=500,
        delta_multiples=[0.0, 2.0],
        simulations=4_000,
        seed=99,
    )

    assert curve.points[1].result.mean_statistic > curve.points[0].result.mean_statistic


@pytest.mark.parametrize(
    "multiples",
    [
        [],
        [-1.0, 0.0],
        [0.0, float("nan")],
    ],
)
def test_invalid_delta_multiples_raise(multiples: list[float]) -> None:
    """Invalid curve grids should fail explicitly."""
    with pytest.raises(ValueError):
        simulate_operating_characteristic_curve(
            reference=[0.5, 0.5],
            sample_size=100,
            delta_multiples=multiples,
            simulations=100,
            seed=1,
        )
