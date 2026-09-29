"""Reproduce selected small-sample classifications from Table 3."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from population_resemblance import DecisionRegion, assess_population_resemblance


@dataclass(frozen=True, slots=True)
class Table3Case:
    """One selected published Table 3 example."""

    counts: tuple[int, ...]
    expected_region: DecisionRegion
    expected_statistic: float


CASES = (
    Table3Case((6, 9, 10, 11, 14), DecisionRegion.R1, 0.068),
    Table3Case((4, 10, 11, 11, 14), DecisionRegion.R2, 0.108),
    Table3Case((2, 5, 13, 14, 16), DecisionRegion.R3, 0.300),
)


def main() -> None:
    """Compute and validate selected published Table 3 classifications."""
    print("counts,prs,prs_paper,region,region_paper")

    for case in CASES:
        sample_size = sum(case.counts)
        observed = [count / sample_size for count in case.counts]
        reference = [0.2] * len(case.counts)

        result = assess_population_resemblance(
            observed=observed,
            reference=reference,
            sample_size=sample_size,
            c=0.7,
            m=2.0,
            alpha1=0.05,
            alpha2=0.10,
        )

        if not isclose(
            result.statistic,
            case.expected_statistic,
            rel_tol=0.0,
            abs_tol=5e-4,
        ):
            raise AssertionError(
                f"expected PRS {case.expected_statistic:.4f}, "
                f"got {result.statistic:.4f}"
            )
        if result.region is not case.expected_region:
            raise AssertionError(
                f"expected {case.expected_region.value}, got {result.region.value}"
            )

        counts = "-".join(str(count) for count in case.counts)
        print(
            f"{counts},{result.statistic:.6f},{case.expected_statistic:.6f},"
            f"{result.region.value},{case.expected_region.value}"
        )


if __name__ == "__main__":
    main()
