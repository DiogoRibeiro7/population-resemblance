"""Benchmark chunked versus single-batch PRS Monte Carlo simulation."""

from __future__ import annotations

import argparse
from time import perf_counter

from population_resemblance import simulate_region_probabilities


def _parse_args() -> argparse.Namespace:
    """Parse benchmark options."""
    parser = argparse.ArgumentParser(
        description="Benchmark memory-bounded PRS Monte Carlo simulation."
    )
    parser.add_argument("--simulations", type=int, default=100_000)
    parser.add_argument("--batch-size", type=int, default=5_000)
    parser.add_argument("--categories", type=int, default=10)
    parser.add_argument("--sample-size", type=int, default=500)
    parser.add_argument("--seed", type=int, default=2026)
    return parser.parse_args()


def _matrix_megabytes(rows: int, categories: int) -> float:
    """Estimate the raw int64 multinomial count-matrix size in MiB."""
    return rows * categories * 8 / (1024**2)


def main() -> None:
    """Run equivalent full and chunked simulations and report timing estimates."""
    args = _parse_args()

    if args.categories < 2:
        raise ValueError("categories must be at least 2.")
    reference = [1.0 / args.categories] * args.categories

    start = perf_counter()
    full = simulate_region_probabilities(
        current=reference,
        reference=reference,
        sample_size=args.sample_size,
        simulations=args.simulations,
        seed=args.seed,
    )
    full_seconds = perf_counter() - start

    start = perf_counter()
    chunked = simulate_region_probabilities(
        current=reference,
        reference=reference,
        sample_size=args.sample_size,
        simulations=args.simulations,
        seed=args.seed,
        batch_size=args.batch_size,
    )
    chunked_seconds = perf_counter() - start

    if full != chunked:
        raise AssertionError("chunked and single-batch results differ")

    effective_batch = min(args.batch_size, args.simulations)

    print(f"simulations={args.simulations}")
    print(f"categories={args.categories}")
    print(f"sample_size={args.sample_size}")
    print(f"batch_size={effective_batch}")
    print(f"full_seconds={full_seconds:.6f}")
    print(f"chunked_seconds={chunked_seconds:.6f}")
    print(
        "full_count_matrix_mib="
        f"{_matrix_megabytes(args.simulations, args.categories):.3f}"
    )
    print(
        "chunked_count_matrix_mib="
        f"{_matrix_megabytes(effective_batch, args.categories):.3f}"
    )


if __name__ == "__main__":
    main()
