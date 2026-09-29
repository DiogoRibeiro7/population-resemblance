"""Numerically validate algebra used in the independent two-sample research note."""

from __future__ import annotations

import numpy as np


def pooled_quadratic(x: np.ndarray, y: np.ndarray) -> float:
    """Compute the pooled two-sample quadratic form."""
    n = int(np.sum(x))
    m = int(np.sum(y))
    p_hat = x / n
    q_hat = y / m
    pooled = (x + y) / (n + m)
    n_eff = n * m / (n + m)

    return float(n_eff * np.sum((p_hat - q_hat) ** 2 / pooled))


def pearson_homogeneity(x: np.ndarray, y: np.ndarray) -> float:
    """Compute Pearson's statistic for a 2-by-B homogeneity table."""
    n = int(np.sum(x))
    m = int(np.sum(y))
    pooled = (x + y) / (n + m)

    expected_x = n * pooled
    expected_y = m * pooled

    return float(
        np.sum((x - expected_x) ** 2 / expected_x)
        + np.sum((y - expected_y) ** 2 / expected_y)
    )


def main() -> None:
    """Check exact algebraic identity and a null Monte Carlo moment sanity check."""
    x = np.array([44, 31, 25], dtype=np.float64)
    y = np.array([192, 123, 85], dtype=np.float64)

    candidate = pooled_quadratic(x, y)
    pearson = pearson_homogeneity(x, y)

    if not np.isclose(candidate, pearson, rtol=1e-14, atol=1e-14):
        raise AssertionError("pooled quadratic form does not match Pearson homogeneity")

    rng = np.random.default_rng(2026)
    reference = np.array([0.40, 0.35, 0.25])
    simulations = 20_000
    n = 250
    m = 400
    n_eff = n * m / (n + m)

    x_draws = rng.multinomial(n, reference, size=simulations)
    y_draws = rng.multinomial(m, reference, size=simulations)

    p_hat = x_draws / n
    q_hat = y_draws / m
    pooled = (x_draws + y_draws) / (n + m)

    statistics = n_eff * np.sum((p_hat - q_hat) ** 2 / pooled, axis=1)

    # Under the point null with B=3, the limiting chi-square has mean 2
    # and variance 4. These are intentionally loose finite-sample checks.
    empirical_mean = float(np.mean(statistics))
    empirical_variance = float(np.var(statistics))

    if abs(empirical_mean - 2.0) > 0.08:
        raise AssertionError(f"unexpected null mean: {empirical_mean}")
    if abs(empirical_variance - 4.0) > 0.35:
        raise AssertionError(f"unexpected null variance: {empirical_variance}")

    print(f"candidate={candidate:.12f}")
    print(f"pearson={pearson:.12f}")
    print(f"null_mean={empirical_mean:.6f}")
    print(f"null_variance={empirical_variance:.6f}")


if __name__ == "__main__":
    main()
