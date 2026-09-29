"""Reproduce the calibration values reported in Table 2 of the PRS paper."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from population_resemblance import critical_values, recommended_delta


@dataclass(frozen=True, slots=True)
class Table2Case:
    """One published Table 2 calibration case."""

    sample_size: int
    categories: int
    expected_delta: float
    expected_lower: float
    expected_upper: float


CASES = (
    Table2Case(50, 5, 0.039598, 0.07441, 0.25722),
    Table2Case(500, 10, 0.009391, 0.03063, 0.04890),
    Table2Case(2_000, 10, 0.004696, 0.00766, 0.01222),
    Table2Case(10_000, 20, 0.001526, 0.00394, 0.00439),
)


def _assert_close(actual: float, expected: float, tolerance: float) -> None:
    """Fail loudly when a reproduced value exceeds the documented tolerance."""
    if not isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance):
        raise AssertionError(
            f"expected {expected:.8f}, got {actual:.8f}, tolerance={tolerance}"
        )


def main() -> None:
    """Compute and validate all selected Table 2 rows."""
    print("n,B,delta,delta_paper,tau1,tau1_paper,tau2,tau2_paper")

    for case in CASES:
        reference = [1.0 / case.categories] * case.categories
        delta = recommended_delta(reference, case.sample_size, c=0.7)
        thresholds = critical_values(
            reference,
            case.sample_size,
            delta,
            m=2.0,
            alpha1=0.05,
            alpha2=0.10,
        )

        _assert_close(delta, case.expected_delta, 5e-7)
        _assert_close(thresholds.lower, case.expected_lower, 5e-6)
        _assert_close(thresholds.upper, case.expected_upper, 5e-6)

        print(
            f"{case.sample_size},{case.categories},"
            f"{delta:.8f},{case.expected_delta:.8f},"
            f"{thresholds.lower:.8f},{case.expected_lower:.8f},"
            f"{thresholds.upper:.8f},{case.expected_upper:.8f}"
        )


if __name__ == "__main__":
    main()
