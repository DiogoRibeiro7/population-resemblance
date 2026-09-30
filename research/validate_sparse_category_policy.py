"""Validate the proposed sparse-category policy with deterministic simulation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class PolicyResult:
    """Mechanical sparse-category eligibility result."""

    minimum_pooled_probability: float
    minimum_expected_count: float
    zero_pooled_categories: int
    eligible: bool
    reason: str | None


def evaluate_sparse_policy(
    first_counts: np.ndarray,
    second_counts: np.ndarray,
    *,
    minimum_expected_count: float = 5.0,
) -> PolicyResult:
    """Evaluate the proposed sparse-category support conditions."""
    if first_counts.shape != second_counts.shape:
        raise ValueError("count vectors must have the same shape")
    if first_counts.ndim != 1 or first_counts.size < 2:
        raise ValueError("count vectors must contain at least two categories")
    if np.any(first_counts < 0) or np.any(second_counts < 0):
        raise ValueError("counts must be non-negative")

    n = int(np.sum(first_counts))
    m = int(np.sum(second_counts))
    if n <= 0 or m <= 0:
        raise ValueError("both samples must be non-empty")

    pooled_counts = first_counts + second_counts
    zero_count = int(np.count_nonzero(pooled_counts == 0))

    if zero_count:
        return PolicyResult(
            minimum_pooled_probability=0.0,
            minimum_expected_count=0.0,
            zero_pooled_categories=zero_count,
            eligible=False,
            reason="zero_pooled_category",
        )

    pooled = pooled_counts / float(n + m)
    minimum_probability = float(np.min(pooled))
    expected = min(n, m) * minimum_probability

    if expected < minimum_expected_count:
        return PolicyResult(
            minimum_pooled_probability=minimum_probability,
            minimum_expected_count=expected,
            zero_pooled_categories=0,
            eligible=False,
            reason="insufficient_expected_count",
        )

    return PolicyResult(
        minimum_pooled_probability=minimum_probability,
        minimum_expected_count=expected,
        zero_pooled_categories=0,
        eligible=True,
        reason=None,
    )


def _eligibility_rate(
    reference: np.ndarray,
    *,
    sample_size: int,
    simulations: int,
    seed: int,
) -> float:
    """Estimate how often samples satisfy the proposed support policy."""
    rng = np.random.default_rng(seed)
    first = rng.multinomial(sample_size, reference, size=simulations)
    second = rng.multinomial(sample_size, reference, size=simulations)

    pooled = (first + second) / float(2 * sample_size)
    minimum_expected = sample_size * np.min(pooled, axis=1)
    no_zero = np.all(pooled > 0.0, axis=1)

    return float(np.mean(no_zero & (minimum_expected >= 5.0)))


def main() -> None:
    """Check deterministic examples and sparse-category eligibility rates."""
    supported = evaluate_sparse_policy(
        np.array([40, 30, 20, 10]),
        np.array([35, 30, 25, 10]),
    )
    if not supported.eligible:
        raise AssertionError("well-populated counts should be eligible")

    zero = evaluate_sparse_policy(
        np.array([40, 30, 30, 0]),
        np.array([35, 35, 30, 0]),
    )
    if zero.reason != "zero_pooled_category":
        raise AssertionError("zero pooled category must fail explicitly")

    sparse = evaluate_sparse_policy(
        np.array([70, 15, 8, 5, 2]),
        np.array([69, 16, 8, 5, 2]),
    )
    if sparse.reason != "insufficient_expected_count":
        raise AssertionError("sparse counts should fail expected-count policy")

    scenarios = (
        ("balanced", np.array([0.2] * 5), 50),
        ("moderate", np.array([0.40, 0.25, 0.15, 0.12, 0.08]), 100),
        ("sparse_100", np.array([0.70, 0.15, 0.08, 0.05, 0.02]), 100),
        ("sparse_200", np.array([0.70, 0.15, 0.08, 0.05, 0.02]), 200),
        ("sparse_500", np.array([0.70, 0.15, 0.08, 0.05, 0.02]), 500),
    )

    print("scenario,sample_size,min_true_expected,eligibility_rate")
    for index, (name, reference, sample_size) in enumerate(scenarios):
        rate = _eligibility_rate(
            reference,
            sample_size=sample_size,
            simulations=20_000,
            seed=2026 + index,
        )
        minimum_true_expected = sample_size * float(np.min(reference))
        print(
            f"{name},{sample_size},"
            f"{minimum_true_expected:.3f},{rate:.6f}"
        )

    balanced_rate = _eligibility_rate(
        np.array([0.2] * 5),
        sample_size=50,
        simulations=20_000,
        seed=3001,
    )
    sparse_rate = _eligibility_rate(
        np.array([0.70, 0.15, 0.08, 0.05, 0.02]),
        sample_size=100,
        simulations=20_000,
        seed=3002,
    )

    if balanced_rate < 0.98:
        raise AssertionError(
            "balanced scenario should have at least 98% policy eligibility"
        )
    if sparse_rate > 0.05:
        raise AssertionError(
            "sparse n=100 scenario should have at most 5% policy eligibility"
        )


if __name__ == "__main__":
    main()
