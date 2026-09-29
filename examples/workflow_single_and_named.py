"""End-to-end examples for count-based and named-category monitoring."""

from __future__ import annotations

from population_resemblance import (
    assess_named_population,
    assess_population_counts,
)


def main() -> None:
    """Run single-sample and named-category monitoring examples."""
    reference = [0.50, 0.30, 0.20]
    counts = [420, 330, 250]

    result = assess_population_counts(
        counts=counts,
        reference=reference,
    )

    print("count_based")
    print(f"sample_size={result.sample_size}")
    print(f"prs={result.statistic:.6f}")
    print(f"region={result.region.value}")
    print(
        "critical_values="
        f"({result.critical_values.lower:.6f}, "
        f"{result.critical_values.upper:.6f})"
    )

    named = assess_named_population(
        counts={
            "segment_a": 420,
            "segment_b": 330,
            "segment_c": 250,
        },
        reference={
            "segment_a": 0.50,
            "segment_b": 0.30,
            "segment_c": 0.20,
        },
        ks_simulations=1_000,
        ks_seed=101,
    )

    print("named_categories")
    print(f"categories={named.categories}")
    print(f"prs={named.monitoring.prs.statistic:.6f}")
    print(f"region={named.monitoring.prs.region.value}")


if __name__ == "__main__":
    main()
