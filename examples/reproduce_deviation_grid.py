"""Run the source-paper deviation-grid simulation design."""

from __future__ import annotations

import argparse

from population_resemblance import simulate_operating_characteristic_curve


def _parse_args() -> argparse.Namespace:
    """Parse command-line options for the reproducibility simulation."""
    parser = argparse.ArgumentParser(
        description="Simulate the 30-point PRS deviation grid from the source study."
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=10_000,
        help="Monte Carlo samples per grid point.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="Repository reproducibility seed; not a seed reported by the paper.",
    )
    return parser.parse_args()


def main() -> None:
    """Simulate and print the complete 30-point operating-characteristic grid."""
    args = _parse_args()

    curve = simulate_operating_characteristic_curve(
        reference=[0.2] * 5,
        sample_size=50,
        simulations=args.simulations,
        seed=args.seed,
        c=0.7,
        m=2.0,
        alpha1=0.05,
        alpha2=0.10,
    )

    if len(curve.points) != 30:
        raise AssertionError(f"expected 30 grid points, got {len(curve.points)}")
    if abs(curve.delta_multiples[0]) > 1e-12:
        raise AssertionError("the source grid must start at zero")
    if abs(curve.delta_multiples[-1] - 8.0) > 1e-12:
        raise AssertionError("for M=2, the source grid must end at 8 delta")

    print(f"delta={curve.delta:.8f}")
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
