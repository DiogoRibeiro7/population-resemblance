"""Run the source-paper deviation-grid simulation design."""

from __future__ import annotations

import argparse

from population_resemblance import (
    recommended_delta,
    simulate_operating_characteristic_curve,
    source_deviation_grid,
)


def _parse_args() -> argparse.Namespace:
    """Parse command-line options for the reproducibility simulation."""
    parser = argparse.ArgumentParser(
        description="Simulate the feasible portion of the paper's 30-point PRS deviation grid."
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=10_000,
        help="Monte Carlo samples per feasible grid point.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="Repository reproducibility seed; not a seed reported by the paper.",
    )
    return parser.parse_args()


def main() -> None:
    """Validate the stated grid and simulate every mathematically feasible point."""
    args = _parse_args()

    reference = [0.2] * 5
    sample_size = 50
    c = 0.7
    m = 2.0

    delta = recommended_delta(reference, sample_size, c=c)
    stated_grid = source_deviation_grid(m=m, points=30)
    maximum_feasible_deviation = min(reference)
    maximum_feasible_multiple = maximum_feasible_deviation / delta

    feasible_multiples = tuple(
        multiple
        for multiple in stated_grid
        if multiple * delta <= maximum_feasible_deviation + 1e-12
    )

    if len(stated_grid) != 30:
        raise AssertionError(f"expected 30 source grid points, got {len(stated_grid)}")
    if abs(stated_grid[0]) > 1e-12:
        raise AssertionError("the source grid must start at zero")
    if abs(stated_grid[-1] - 8.0) > 1e-12:
        raise AssertionError("for M=2, the stated source grid must end at 8 delta")
    if not feasible_multiples:
        raise AssertionError("expected at least one feasible deviation-grid point")

    curve = simulate_operating_characteristic_curve(
        reference=reference,
        sample_size=sample_size,
        delta_multiples=feasible_multiples,
        simulations=args.simulations,
        seed=args.seed,
        delta=delta,
        c=c,
        m=m,
        alpha1=0.05,
        alpha2=0.10,
    )

    print(f"delta={delta:.8f}")
    print(f"source_requested_points={len(stated_grid)}")
    print(f"feasible_points={len(feasible_multiples)}")
    print(f"maximum_feasible_multiple={maximum_feasible_multiple:.8f}")
    print(f"simulations_per_point={args.simulations}")
    print(f"seed={args.seed}")
    print("delta_multiple,deviation,r1,r2,r3,mean_prs")

    for point in curve.points:
        result = point.result
        print(
            f"{point.delta_multiple:.8f},{point.deviation:.8f},"
            f"{result.r1_probability:.6f},{result.r2_probability:.6f},"
            f"{result.r3_probability:.6f},{result.mean_statistic:.8f}"
        )


if __name__ == "__main__":
    main()
