"""Finite-sample calibration study for the two-sample resemblance candidate."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.stats import chi2, ncx2


@dataclass(frozen=True, slots=True)
class Scenario:
    """One independent two-sample simulation scenario."""

    name: str
    reference: tuple[float, ...]
    n: int
    m: int


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    """Summary of one finite-sample simulation configuration."""

    scenario: str
    delta_multiple: float
    simulations: int
    valid_fraction: float
    r1_probability: float
    r2_probability: float
    r3_probability: float
    oracle_r1_probability: float
    oracle_r2_probability: float
    oracle_r3_probability: float
    homogeneity_rejection_probability: float


SCENARIOS = (
    Scenario("balanced_small", (0.2, 0.2, 0.2, 0.2, 0.2), 50, 50),
    Scenario("balanced_medium", (0.2, 0.2, 0.2, 0.2, 0.2), 200, 200),
    Scenario("balanced_large", (0.2, 0.2, 0.2, 0.2, 0.2), 1_000, 1_000),
    Scenario("balanced_unequal", (0.2, 0.2, 0.2, 0.2, 0.2), 100, 400),
    Scenario("imbalanced", (0.40, 0.25, 0.15, 0.12, 0.08), 100, 100),
    Scenario("sparse", (0.70, 0.15, 0.08, 0.05, 0.02), 100, 100),
)


def _recommended_delta(
    reference: np.ndarray,
    effective_sample_size: float,
    *,
    c: float,
) -> float:
    """Return the candidate two-sample tolerance for a fixed centre."""
    return float(
        c
        * np.min(
            np.sqrt(
                reference
                * (1.0 - reference)
                / effective_sample_size
            )
        )
    )


def _least_favourable_difference(
    reference: np.ndarray,
    magnitude: float,
) -> np.ndarray:
    """Construct one fixed-centre least-favourable difference vector."""
    categories = int(reference.size)
    difference = np.zeros(categories, dtype=np.float64)

    if categories % 2 == 0:
        half = categories // 2
        difference[:half] = -magnitude
        difference[half:] = magnitude
        return difference

    zero_index = int(np.argmax(reference))
    perturbed = [index for index in range(categories) if index != zero_index]
    half = (categories - 1) // 2

    for index in perturbed[:half]:
        difference[index] = -magnitude
    for index in perturbed[half:]:
        difference[index] = magnitude

    return difference


def _lambda_sup(
    reference: np.ndarray,
    effective_sample_size: float,
    delta: np.ndarray | float,
) -> np.ndarray:
    """Compute fixed-centre least-favourable non-centrality values."""
    inverse_sum = np.sum(1.0 / reference, axis=-1)

    if reference.shape[-1] % 2 == 1:
        inverse_sum = inverse_sum - 1.0 / np.max(reference, axis=-1)

    return effective_sample_size * np.square(delta) * inverse_sum


def _classification_probabilities(
    statistic: np.ndarray,
    lower: np.ndarray | float,
    upper: np.ndarray | float,
) -> tuple[float, float, float]:
    """Return R1, R2, and R3 frequencies."""
    r1 = statistic <= lower
    r3 = statistic > upper
    r2 = ~(r1 | r3)

    return (
        float(np.mean(r1)),
        float(np.mean(r2)),
        float(np.mean(r3)),
    )


def simulate_scenario(
    scenario: Scenario,
    *,
    delta_multiple: float,
    simulations: int,
    seed: int,
    c: float = 0.7,
    m_multiplier: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
) -> ScenarioResult | None:
    """Simulate the empirical pooled-centre resemblance candidate."""
    reference = np.asarray(scenario.reference, dtype=np.float64)
    rho = scenario.n / (scenario.n + scenario.m)
    effective_sample_size = (
        scenario.n * scenario.m / (scenario.n + scenario.m)
    )
    delta = _recommended_delta(reference, effective_sample_size, c=c)

    difference = _least_favourable_difference(
        reference,
        delta_multiple * delta,
    )
    p = reference + (1.0 - rho) * difference
    q = reference - rho * difference

    if (
        np.any(p < 0.0)
        or np.any(q < 0.0)
        or np.any(p > 1.0)
        or np.any(q > 1.0)
    ):
        return None

    rng = np.random.default_rng(seed)
    x = rng.multinomial(scenario.n, p, size=simulations)
    y = rng.multinomial(scenario.m, q, size=simulations)

    pooled = (x + y) / float(scenario.n + scenario.m)
    p_hat = x / float(scenario.n)
    q_hat = y / float(scenario.m)

    interior = np.all(pooled > 0.0, axis=1)
    pooled = pooled[interior]
    p_hat = p_hat[interior]
    q_hat = q_hat[interior]

    if pooled.size == 0:
        raise AssertionError("no simulated pooled distribution was interior")

    statistic = effective_sample_size * np.sum(
        np.square(p_hat - q_hat) / pooled,
        axis=1,
    )

    plug_in_delta = (
        c
        * np.min(
            np.sqrt(
                pooled
                * (1.0 - pooled)
                / effective_sample_size
            ),
            axis=1,
        )
    )

    probability_bound = (
        np.min(np.minimum(pooled, 1.0 - pooled), axis=1)
        / max(rho, 1.0 - rho)
    )
    feasible = m_multiplier * plug_in_delta <= probability_bound

    statistic = statistic[feasible]
    pooled = pooled[feasible]
    plug_in_delta = plug_in_delta[feasible]

    if statistic.size == 0:
        raise AssertionError("no simulated plug-in calibration was feasible")

    plug_in_lambda = _lambda_sup(
        pooled,
        effective_sample_size,
        plug_in_delta,
    )
    plug_in_lower = ncx2.ppf(
        alpha2,
        reference.size - 1,
        m_multiplier**2 * plug_in_lambda,
    )
    plug_in_upper = ncx2.ppf(
        1.0 - alpha1,
        reference.size - 1,
        plug_in_lambda,
    )
    plug_in_probabilities = _classification_probabilities(
        statistic,
        plug_in_lower,
        plug_in_upper,
    )

    oracle_lambda = float(
        _lambda_sup(
            reference[np.newaxis, :],
            effective_sample_size,
            np.asarray([delta]),
        )[0]
    )
    oracle_lower = float(
        ncx2.ppf(
            alpha2,
            reference.size - 1,
            m_multiplier**2 * oracle_lambda,
        )
    )
    oracle_upper = float(
        ncx2.ppf(
            1.0 - alpha1,
            reference.size - 1,
            oracle_lambda,
        )
    )
    oracle_probabilities = _classification_probabilities(
        statistic,
        oracle_lower,
        oracle_upper,
    )

    homogeneity_threshold = float(
        chi2.ppf(0.95, reference.size - 1)
    )
    homogeneity_rejection = float(
        np.mean(statistic > homogeneity_threshold)
    )

    valid_fraction = (
        float(np.mean(interior))
        * float(np.mean(feasible))
    )

    return ScenarioResult(
        scenario=scenario.name,
        delta_multiple=delta_multiple,
        simulations=simulations,
        valid_fraction=valid_fraction,
        r1_probability=plug_in_probabilities[0],
        r2_probability=plug_in_probabilities[1],
        r3_probability=plug_in_probabilities[2],
        oracle_r1_probability=oracle_probabilities[0],
        oracle_r2_probability=oracle_probabilities[1],
        oracle_r3_probability=oracle_probabilities[2],
        homogeneity_rejection_probability=homogeneity_rejection,
    )


def _parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Simulate finite-sample calibration of the independent "
            "two-sample resemblance plug-in candidate."
        )
    )
    parser.add_argument("--simulations", type=int, default=30_000)
    parser.add_argument("--seed", type=int, default=2026)
    return parser.parse_args()


def main() -> None:
    """Run all finite-sample research scenarios."""
    args = _parse_args()

    print(
        "scenario,delta_multiple,valid_fraction,"
        "r1,r2,r3,oracle_r1,oracle_r2,oracle_r3,"
        "homogeneity_reject"
    )

    for scenario_index, scenario in enumerate(SCENARIOS):
        for multiple in (0.0, 1.0, 2.0, 3.0):
            result = simulate_scenario(
                scenario,
                delta_multiple=multiple,
                simulations=args.simulations,
                seed=args.seed + 10 * scenario_index + int(multiple),
            )

            if result is None:
                print(
                    f"{scenario.name},{multiple:.1f},"
                    "true-distribution-infeasible"
                )
                continue

            print(
                f"{result.scenario},{result.delta_multiple:.1f},"
                f"{result.valid_fraction:.6f},"
                f"{result.r1_probability:.6f},"
                f"{result.r2_probability:.6f},"
                f"{result.r3_probability:.6f},"
                f"{result.oracle_r1_probability:.6f},"
                f"{result.oracle_r2_probability:.6f},"
                f"{result.oracle_r3_probability:.6f},"
                f"{result.homogeneity_rejection_probability:.6f}"
            )

            if multiple == 0.0 and scenario.name != "sparse":
                if abs(result.homogeneity_rejection_probability - 0.05) > 0.02:
                    raise AssertionError(
                        "homogeneity benchmark is unexpectedly miscalibrated "
                        f"for {scenario.name}"
                    )

            if multiple == 1.0 and scenario.name != "sparse":
                if abs(result.r3_probability - 0.05) > 0.03:
                    raise AssertionError(
                        "plug-in upper-boundary calibration is unexpectedly poor "
                        f"for {scenario.name}"
                    )

            if multiple == 2.0 and scenario.name != "sparse":
                if abs(result.r1_probability - 0.10) > 0.05:
                    raise AssertionError(
                        "plug-in lower-boundary calibration is unexpectedly poor "
                        f"for {scenario.name}"
                    )


if __name__ == "__main__":
    main()
