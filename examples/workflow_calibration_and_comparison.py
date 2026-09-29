"""End-to-end examples for calibration, method comparison, and simulation."""

from __future__ import annotations

from population_resemblance import (
    simulate_operating_characteristic_curve,
    simulate_prs_psi_comparison,
    sweep_calibration_parameters,
)


def main() -> None:
    """Run calibration sensitivity, PRS-vs-PSI comparison, and OC simulation."""
    reference = [0.2] * 5

    grid = sweep_calibration_parameters(
        reference=reference,
        sample_size=100,
        c_values=[0.5, 0.7, 1.0],
        m_values=[1.2, 1.5, 2.0],
        alpha1_values=[0.05],
        alpha2_values=[0.10],
    )

    print("calibration_sensitivity")
    print(f"total={len(grid.points)}")
    print(f"feasible={len(grid.feasible_points)}")
    print(f"infeasible={len(grid.infeasible_points)}")

    comparison = simulate_prs_psi_comparison(
        current=[0.17, 0.17, 0.20, 0.23, 0.23],
        reference=reference,
        sample_size=500,
        simulations=2_000,
        seed=300,
    )

    print("prs_vs_psi")
    print(
        "prs="
        f"({comparison.prs.green:.4f}, "
        f"{comparison.prs.amber:.4f}, "
        f"{comparison.prs.red:.4f})"
    )
    print(
        "psi="
        f"({comparison.psi.green:.4f}, "
        f"{comparison.psi.amber:.4f}, "
        f"{comparison.psi.red:.4f})"
    )

    curve = simulate_operating_characteristic_curve(
        reference=reference,
        sample_size=100,
        delta_multiples=[0.0, 0.5, 1.0, 1.5, 2.0],
        simulations=1_000,
        seed=400,
        batch_size=250,
    )

    print("operating_characteristic")
    for point in curve.points:
        print(
            f"multiple={point.delta_multiple:.2f}",
            f"r1={point.result.r1_probability:.4f}",
            f"r2={point.result.r2_probability:.4f}",
            f"r3={point.result.r3_probability:.4f}",
        )


if __name__ == "__main__":
    main()
