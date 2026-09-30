"""Reproducible numerical benchmark suite for population-resemblance."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter

from population_resemblance import (
    discrete_ks_test_counts,
    simulate_operating_characteristic_curve,
    simulate_region_probabilities,
)
from population_resemblance.experimental import (
    assess_independent_two_sample_resemblance,
)


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """One benchmark timing result."""

    name: str
    seconds: float
    detail: str


def _time_call(name: str, detail: str, function: Callable[[], object]) -> BenchmarkResult:
    """Run one benchmark callable and return elapsed wall-clock time."""
    start = perf_counter()
    function()
    return BenchmarkResult(
        name=name,
        seconds=perf_counter() - start,
        detail=detail,
    )


def _count_matrix_mib(rows: int, categories: int) -> float:
    """Estimate the dominant int64 multinomial count-matrix size in MiB."""
    return rows * categories * 8 / (1024**2)


def _benchmark_prs_simulation(
    *,
    simulations: int,
    batch_size: int,
    sample_size: int,
    categories: int,
) -> list[BenchmarkResult]:
    """Benchmark full and chunked one-sample Monte Carlo."""
    reference = [1.0 / categories] * categories

    full = _time_call(
        "prs_simulation_full",
        (
            f"simulations={simulations};sample_size={sample_size};"
            f"categories={categories};estimated_count_matrix_mib="
            f"{_count_matrix_mib(simulations, categories):.3f}"
        ),
        lambda: simulate_region_probabilities(
            current=reference,
            reference=reference,
            sample_size=sample_size,
            simulations=simulations,
            seed=100,
        ),
    )

    chunked = _time_call(
        "prs_simulation_chunked",
        (
            f"simulations={simulations};batch_size={batch_size};"
            f"sample_size={sample_size};categories={categories};"
            f"estimated_count_matrix_mib="
            f"{_count_matrix_mib(min(batch_size, simulations), categories):.3f}"
        ),
        lambda: simulate_region_probabilities(
            current=reference,
            reference=reference,
            sample_size=sample_size,
            simulations=simulations,
            seed=100,
            batch_size=batch_size,
        ),
    )

    return [full, chunked]


def _benchmark_operating_curve(
    *,
    simulations: int,
) -> BenchmarkResult:
    """Benchmark a short operating-characteristic curve."""
    return _time_call(
        "operating_characteristic",
        f"points=5;simulations_per_point={simulations}",
        lambda: simulate_operating_characteristic_curve(
            reference=[0.2] * 5,
            sample_size=200,
            delta_multiples=[0.0, 0.5, 1.0, 1.5, 2.0],
            simulations=simulations,
            seed=200,
            batch_size=max(100, simulations // 4),
        ),
    )


def _benchmark_discrete_ks(
    *,
    simulations: int,
) -> BenchmarkResult:
    """Benchmark Monte Carlo calibration of the discrete KS statistic."""
    return _time_call(
        "discrete_ks",
        f"categories=10;simulations={simulations};sample_size=1000",
        lambda: discrete_ks_test_counts(
            counts=[100] * 10,
            reference=[0.1] * 10,
            simulations=simulations,
            seed=300,
        ),
    )


def _benchmark_two_sample(
    *,
    repetitions: int,
) -> BenchmarkResult:
    """Benchmark repeated experimental two-sample assessments."""
    first = [420, 330, 250]
    second = [390, 360, 250]

    def run() -> None:
        for _ in range(repetitions):
            assess_independent_two_sample_resemblance(
                first,
                second,
                samples_are_independent=True,
            )

    return _time_call(
        "experimental_two_sample",
        f"repetitions={repetitions};categories=3",
        run,
    )


def _parse_args() -> argparse.Namespace:
    """Parse benchmark-suite options."""
    parser = argparse.ArgumentParser(
        description="Run deterministic population-resemblance numerical benchmarks."
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Use a short CI-friendly workload.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the benchmark suite and print machine-readable CSV-style output."""
    args = _parse_args()

    if args.smoke:
        simulations = 1_000
        operating_simulations = 250
        ks_simulations = 1_000
        two_sample_repetitions = 200
        batch_size = 100
    else:
        simulations = 100_000
        operating_simulations = 10_000
        ks_simulations = 100_000
        two_sample_repetitions = 20_000
        batch_size = 5_000

    results = _benchmark_prs_simulation(
        simulations=simulations,
        batch_size=batch_size,
        sample_size=500,
        categories=10,
    )
    results.append(
        _benchmark_operating_curve(
            simulations=operating_simulations,
        )
    )
    results.append(
        _benchmark_discrete_ks(
            simulations=ks_simulations,
        )
    )
    results.append(
        _benchmark_two_sample(
            repetitions=two_sample_repetitions,
        )
    )

    print("benchmark,seconds,detail")
    for result in results:
        print(
            f"{result.name},{result.seconds:.6f},"
            f"{result.detail}"
        )


if __name__ == "__main__":
    main()
