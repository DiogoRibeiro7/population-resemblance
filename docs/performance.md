# Performance benchmarks

The repository includes a small deterministic benchmark suite for the most computationally
expensive numerical paths.

The benchmark suite is **observational**, not a CI performance gate. Runtime depends on
hardware, operating system, NumPy/SciPy builds, and runner load, so ordinary CI does not fail
based on wall-clock thresholds.

## Run the full suite

```bash
poetry run python benchmarks/benchmark_suite.py
```

The suite measures:

- single-batch PRS Monte Carlo simulation;
- chunked PRS Monte Carlo simulation;
- operating-characteristic curves;
- discrete KS Monte Carlo calibration;
- repeated experimental independent two-sample assessments.

Each row prints the elapsed wall-clock time plus scenario details.

## CI smoke benchmark

A short deterministic workload is available for CI:

```bash
poetry run python benchmarks/benchmark_suite.py --smoke
```

This checks that the benchmark paths remain executable without treating runtime as a pass/fail
criterion.

## Memory estimate for Monte Carlo simulation

The dominant count matrix created by multinomial simulation contains approximately

\[
\text{rows}\times\text{categories}\times 8
\]

bytes when stored as 64-bit integers.

For example, with 100,000 simulations and 10 categories:

```text
100000 * 10 * 8 bytes ~= 7.63 MiB
```

A chunk size of 5,000 reduces that dominant matrix to approximately:

```text
5000 * 10 * 8 bytes ~= 0.38 MiB
```

The benchmark output reports both estimates directly.

## Interpreting results

Use the benchmark suite for:

- comparing local changes before and after optimization;
- inspecting how batch size changes working-memory estimates;
- spotting accidental order-of-magnitude regressions;
- comparing alternative implementations on the same machine.

Do not compare raw timings from different machines as if they were statistically controlled
measurements.

## Reproducibility

All benchmark scenarios use fixed seeds where randomness is involved.

The suite should remain lightweight enough to run locally, while CI runs only the `--smoke`
variant.
