"""End-to-end examples for temporal monitoring and diagnostics."""

from __future__ import annotations

from population_resemblance import (
    assess_temporal_monitoring,
    population_count_diagnostics,
)


def main() -> None:
    """Run repeated monitoring and inspect category-level PRS contributions."""
    reference = [0.50, 0.30, 0.20]
    periods = [
        [500, 300, 200],
        [470, 320, 210],
        [430, 340, 230],
        [390, 360, 250],
    ]

    series = assess_temporal_monitoring(
        counts_by_period=periods,
        reference=reference,
        labels=["period_1", "period_2", "period_3", "period_4"],
        ks_simulations=1_000,
        ks_seed=200,
    )

    print("temporal_monitoring")
    for point in series.points:
        print(
            point.label,
            f"prs={point.report.prs.statistic:.6f}",
            f"region={point.report.prs.region.value}",
            f"psi={point.report.psi.statistic:.6f}",
            f"ks={point.report.ks.statistic:.6f}",
        )

    diagnostics = population_count_diagnostics(
        counts=periods[-1],
        reference=reference,
        labels=["segment_a", "segment_b", "segment_c"],
    )

    print("category_diagnostics")
    for category in diagnostics.categories:
        print(
            category.category,
            f"shift={category.signed_shift:.6f}",
            f"contribution={category.prs_contribution:.6f}",
            f"share={category.contribution_share:.6f}",
        )

    print(f"largest_contributor={diagnostics.largest_contributor.category}")


if __name__ == "__main__":
    main()
