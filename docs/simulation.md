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
    simulations=10_000,
    seed=123,
)

print(curve.delta_multiples)
print(curve.r1_probabilities)
print(curve.r2_probabilities)
print(curve.r3_probabilities)
```

By default, the grid contains 30 points from \(0\) to \((3M+2)\delta\), matching the range used in the source study.

!!! note
    These are operating-characteristic curves for the nested decision framework. They should not be relabeled as conventional power curves.

## Monte Carlo uncertainty

Simulation probabilities have finite Monte Carlo error. Wilson intervals can be attached to the three region estimates:

```python
from population_resemblance import simulation_uncertainty

uncertainty = simulation_uncertainty(result, confidence_level=0.95)
```

These intervals quantify simulation error only.

## PRS versus PSI

Use `simulate_prs_psi_comparison()` to classify the same simulated samples with PRS and the traditional Lewis PSI thresholds.

This makes the operating differences directly inspectable while preserving the fact that the two methods use different decision rules.

## Discrete KS benchmark

The discrete KS statistic is

\[
\max_j |\hat F(j)-F_0(j)|.
\]

Because its null distribution depends on the discrete reference probabilities, `discrete_ks_test_counts()` calibrates the p-value by Monte Carlo simulation under the multinomial reference.
