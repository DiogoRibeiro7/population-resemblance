# Simulation

## Region probabilities

`simulate_region_probabilities()` estimates how often repeated multinomial samples fall into \(R_1\), \(R_2\), or \(R_3\).

```python
from population_resemblance import simulate_region_probabilities

result = simulate_region_probabilities(
    current=[0.40, 0.35, 0.25],
    reference=[0.50, 0.30, 0.20],
    sample_size=250,
    simulations=10_000,
    seed=123,
)

print(result.probabilities)
```

## Symmetric category shifts

The helper `symmetric_category_shift()` reproduces the structured perturbation used by the source simulation study.

For an odd number of categories, the central category is unchanged while equal-magnitude shifts are applied to the lower and upper halves.

## Operating-characteristic curves

The package can evaluate classification behavior over increasing multiples of \(\delta\):

```python
from population_resemblance import simulate_operating_characteristic_curve

curve = simulate_operating_characteristic_curve(
    reference=[0.2] * 5,
    sample_size=50,
    delta_multiples=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    simulations=10_000,
    seed=123,
)

print(curve.delta_multiples)
print(curve.r1_probabilities)
print(curve.r2_probabilities)
print(curve.r3_probabilities)
```

The explicit grid above keeps every shifted probability valid. Here
\(\delta\approx0.039598\), so the largest shift is \(5\delta\approx0.198 < 0.2\).
For this uniform reference, shifts cannot exceed 0.2. For a general reference, each
decreased probability must remain non-negative and each increased probability must
remain at most one.

If `delta_multiples` is omitted, the function uses the paper's 30-point grid from
\(0\) to \((3M+2)\delta\). It does **not** truncate infeasible points. With the
configuration above, that default reaches \(8\delta\approx0.317\), creates negative
probabilities, and raises `ValueError`. Supply a feasible grid for your reference and
calibration. See [Reproducibility](reproducibility.md#source-deviation-grid-simulation)
for the source-grid constraint and an example that simulates only the feasible prefix.

!!! note
    These are operating-characteristic curves for the nested decision framework. They should not be relabeled as conventional power curves.

## Memory-bounded Monte Carlo

Large simulation studies can be evaluated in batches so memory use depends on the batch
size rather than the total number of Monte Carlo samples.

```python
from population_resemblance import simulate_region_probabilities

result = simulate_region_probabilities(
    current=[0.40, 0.35, 0.25],
    reference=[0.50, 0.30, 0.20],
    sample_size=250,
    simulations=1_000_000,
    seed=123,
    batch_size=10_000,
)
```

With a fixed seed, batching preserves the same generated multinomial stream and therefore
the same region classifications. The mean PRS is numerically equivalent, although its final
floating-point value can differ at machine-roundoff scale because partial sums are grouped
by batch. The main practical difference is the maximum number of simulated rows held in
memory at once.

Operating-characteristic curves expose the same `batch_size` option and forward it to
each curve-point simulation.

For a quick runtime and working-set estimate, run:

```bash
poetry run python examples/benchmark_chunked_simulation.py \
  --simulations 100000 \
  --batch-size 5000
```

The benchmark reports elapsed time and the approximate size of the dominant multinomial
count matrix for the full and chunked cases.

## Monte Carlo uncertainty

Simulation probabilities have finite Monte Carlo error. Wilson intervals can be attached to the three region estimates:

```python
from population_resemblance import simulation_uncertainty

uncertainty = simulation_uncertainty(result, confidence_level=0.95)
```

These intervals quantify simulation error only.

## PRS versus PSI

Use `simulate_prs_psi_comparison()` to classify the same simulated samples with PRS and the traditional Lewis PSI thresholds.

```python
from population_resemblance import simulate_prs_psi_comparison

comparison = simulate_prs_psi_comparison(
    current=[0.17, 0.17, 0.20, 0.23, 0.23],
    reference=[0.20] * 5,
    sample_size=500,
    simulations=10_000,
    seed=123,
)

print(comparison.prs)
print(comparison.psi)
```

This makes the operating differences directly inspectable while preserving the fact that the two methods use different decision rules.

## Discrete KS benchmark

The discrete KS statistic is

\[
\max_j |\hat F(j)-F_0(j)|.
\]

Because its null distribution depends on the discrete reference probabilities, `discrete_ks_test_counts()` calibrates the p-value by Monte Carlo simulation under the multinomial reference.

```python
from population_resemblance import discrete_ks_test_counts

ks = discrete_ks_test_counts(
    counts=[35, 40, 45, 45, 47, 50, 55, 58, 60, 65],
    reference=[0.10] * 10,
    simulations=10_000,
    seed=123,
)

print(ks.statistic)
print(ks.p_value)
print(ks.status)
```

Choose and preserve a meaningful category order: the KS statistic is calculated from
cumulative probabilities. Read the [ordering guidance](user-guide.md#category-order-and-the-ks-benchmark)
before applying it to nominal categories.
