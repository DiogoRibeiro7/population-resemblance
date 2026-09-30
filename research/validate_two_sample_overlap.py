"""Validate covariance scaling for overlapping categorical samples."""

from __future__ import annotations

import numpy as np
from scipy.stats import chi2


def _simulate_overlap(
    *,
    reference: np.ndarray,
    n: int,
    m: int,
    overlap: int,
    simulations: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate two categorical samples with an exact shared subset."""
    if overlap < 0 or overlap > min(n, m):
        raise ValueError("overlap must lie between zero and min(n, m).")

    rng = np.random.default_rng(seed)
    categories = int(reference.size)

    shared = rng.multinomial(overlap, reference, size=simulations)
    first_only = rng.multinomial(n - overlap, reference, size=simulations)
    second_only = rng.multinomial(m - overlap, reference, size=simulations)

    first = shared + first_only
    second = shared + second_only

    if first.shape != (simulations, categories):
        raise AssertionError("unexpected first-sample shape")

    return first, second


def _pearson_difference_statistic(
    first: np.ndarray,
    second: np.ndarray,
    *,
    n: int,
    m: int,
    effective_size: float,
    reference: np.ndarray,
) -> np.ndarray:
    """Compute a known-reference Pearson quadratic form."""
    p_hat = first / float(n)
    q_hat = second / float(m)
    difference = p_hat - q_hat

    return effective_size * np.sum(
        np.square(difference) / reference,
        axis=1,
    )


def main() -> None:
    """Show that overlap-adjusted scaling restores the null chi-square moments."""
    reference = np.array([0.40, 0.30, 0.20, 0.10])
    n = 200
    m = 300
    overlap = 100
    simulations = 40_000

    first, second = _simulate_overlap(
        reference=reference,
        n=n,
        m=m,
        overlap=overlap,
        simulations=simulations,
        seed=2026,
    )

    independent_effective = n * m / (n + m)
    overlap_effective = n * m / (n + m - 2 * overlap)

    naive = _pearson_difference_statistic(
        first,
        second,
        n=n,
        m=m,
        effective_size=independent_effective,
        reference=reference,
    )
    corrected = _pearson_difference_statistic(
        first,
        second,
        n=n,
        m=m,
        effective_size=overlap_effective,
        reference=reference,
    )

    degrees_of_freedom = reference.size - 1
    expected_mean = float(degrees_of_freedom)
    expected_variance = float(2 * degrees_of_freedom)
    critical = float(chi2.ppf(0.95, degrees_of_freedom))

    corrected_mean = float(np.mean(corrected))
    corrected_variance = float(np.var(corrected))
    corrected_rejection = float(np.mean(corrected > critical))
    naive_rejection = float(np.mean(naive > critical))

    if abs(corrected_mean - expected_mean) > 0.08:
        raise AssertionError(f"unexpected corrected mean: {corrected_mean}")
    if abs(corrected_variance - expected_variance) > 0.35:
        raise AssertionError(
            f"unexpected corrected variance: {corrected_variance}"
        )
    if abs(corrected_rejection - 0.05) > 0.01:
        raise AssertionError(
            f"unexpected corrected rejection rate: {corrected_rejection}"
        )
    if naive_rejection >= corrected_rejection:
        raise AssertionError(
            "independence scaling should be conservative under positive overlap"
        )

    nested_n = 100
    nested_m = 300
    nested_overlap = nested_n
    nested_effective = (
        nested_n
        * nested_m
        / (nested_n + nested_m - 2 * nested_overlap)
    )

    if not np.isclose(nested_effective, 150.0):
        raise AssertionError("nested-sample effective size formula is incorrect")

    print(f"independent_effective={independent_effective:.6f}")
    print(f"overlap_effective={overlap_effective:.6f}")
    print(f"corrected_mean={corrected_mean:.6f}")
    print(f"corrected_variance={corrected_variance:.6f}")
    print(f"corrected_rejection={corrected_rejection:.6f}")
    print(f"naive_rejection={naive_rejection:.6f}")
    print(f"nested_effective={nested_effective:.6f}")


if __name__ == "__main__":
    main()
