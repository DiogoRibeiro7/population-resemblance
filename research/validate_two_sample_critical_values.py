"""Validate fixed-centre two-sample least-favourable calculations."""

from __future__ import annotations

from itertools import product

import numpy as np
from scipy.stats import ncx2


def closed_form_lambda_sup(
    reference: np.ndarray,
    n_eff: float,
    delta: float,
) -> float:
    """Return the fixed-centre least-favourable non-centrality."""
    inverse_sum = float(np.sum(1.0 / reference))
    if reference.size % 2 == 1:
        inverse_sum -= 1.0 / float(np.max(reference))
    return n_eff * delta**2 * inverse_sum


def brute_force_lambda_sup(
    reference: np.ndarray,
    n_eff: float,
    delta: float,
) -> float:
    """Enumerate extreme sign/zero patterns for the fixed-centre problem."""
    best = 0.0
    values = (-delta, 0.0, delta)

    for candidate in product(values, repeat=reference.size):
        d = np.asarray(candidate, dtype=np.float64)
        if not np.isclose(float(np.sum(d)), 0.0, atol=1e-12):
            continue
        value = n_eff * float(np.sum(d**2 / reference))
        best = max(best, value)

    return best


def full_cube_feasible(
    reference: np.ndarray,
    rho: float,
    widened_delta: float,
) -> bool:
    """Check the sufficient symmetric probability-domain bound."""
    bound = float(
        np.min(np.minimum(reference, 1.0 - reference))
        / max(rho, 1.0 - rho)
    )
    return widened_delta <= bound


def main() -> None:
    """Check closed-form geometry and conditional critical-value ordering."""
    cases = (
        np.array([0.25, 0.25, 0.25, 0.25]),
        np.array([0.40, 0.35, 0.25]),
        np.array([0.30, 0.25, 0.20, 0.15, 0.10]),
    )

    n = 300
    m = 500
    rho = n / (n + m)
    n_eff = n * m / (n + m)
    delta = 0.01
    multiplier = 2.0

    for reference in cases:
        closed = closed_form_lambda_sup(reference, n_eff, delta)
        brute = brute_force_lambda_sup(reference, n_eff, delta)

        if not np.isclose(closed, brute, rtol=1e-12, atol=1e-12):
            raise AssertionError(
                f"closed form {closed} does not match brute force {brute}"
            )

        if not full_cube_feasible(reference, rho, multiplier * delta):
            raise AssertionError("chosen validation case violates the probability bound")

        lower = float(
            ncx2.ppf(
                0.10,
                reference.size - 1,
                multiplier**2 * closed,
            )
        )
        upper = float(
            ncx2.ppf(
                0.95,
                reference.size - 1,
                closed,
            )
        )

        if lower > upper:
            raise AssertionError("conditional decision boundaries overlap")

        print(
            f"B={reference.size},lambda_sup={closed:.8f},"
            f"lower={lower:.8f},upper={upper:.8f}"
        )


if __name__ == "__main__":
    main()
