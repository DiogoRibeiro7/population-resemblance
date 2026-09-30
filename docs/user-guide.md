# User guide

## Inputs and assumptions

Counts must be non-negative integers with a positive total. Probability vectors must
sum to one, and current and reference arrays must describe the same categories in the
same order. Named-category APIs check that the category sets match and use the reference
mapping's insertion order.

Define category boundaries before monitoring. If you bin continuous values, reuse the
same bin edges for the reference and every current sample. Decide how missing values and
previously unseen labels are handled before constructing the reference; the library
does not bin raw data or align changing category sets for you.

### Zero counts and sparse categories

- PRS and PSI require every reference probability to be strictly positive. A zero
  reference count also fails when a reference sample is converted to probabilities.
- Zero current counts are allowed. Retain their categories so current and reference
  remain aligned.
- PSI follows the source paper's convention of omitting terms with zero observed
  probability. This can differ from implementations that apply smoothing or return
  infinity. PRS still includes the discrepancy from those categories.
- There is no automatic smoothing or category merging. If you choose to merge categories
  or smooth probabilities, apply a documented policy consistently and reassess calibration.
  Do not silently drop a category merely to make an assessment run.

PRS critical values use an asymptotic chi-square approximation. Small expected counts
(`sample_size * reference[j]`) can make that approximation unreliable. Use the
[simulation tools](simulation.md) to investigate finite-sample behavior for your reference
and sample size. Passing the structural sample-size bound does not guarantee statistical
accuracy or sufficient sensitivity.

### Category order and the KS benchmark

Discrete KS uses cumulative probabilities in the supplied category order. Reordering the
categories can change its statistic and p-value, even when current and reference are
reordered together. Use a meaningful order, such as ordered risk bands, and preserve it
across periods. For nominal labels with no meaningful order, the KS output should not be
treated as an order-independent measure of drift. PRS and PSI do not have this ordering
dependence when both vectors are permuted together.

Unified reports and named monitors also calculate KS. In a named report, the reference
mapping's insertion order therefore affects the KS benchmark.

### Reference and sampling assumptions

The PRS framework treats the reference probabilities as fixed and uses a multinomial
sampling model for the current counts. Reference-count wrappers do not account for
reference-sample uncertainty. Dependence among observations can change the sampling
variance; the package does not estimate that dependence.

## Choosing calibration parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `delta` | Automatic | Tolerated absolute change in any category probability; `0.01` means one percentage point. |
| `c` | `0.7` | Scales the automatic tolerance relative to sampling variability; used when `delta` is omitted. |
| `m` | `2.0` | Multiplier defining the wider tolerance `m * delta`; must exceed one. |
| `alpha1` | `0.05` | Upper-tail calibration parameter used for the upper PRS threshold. |
| `alpha2` | `0.10` | Lower-tail calibration parameter used for the lower PRS threshold. |

Choose an explicit `delta` when your application has a justified tolerance for category
probability changes. The automatic tolerance shrinks as sample size grows; it does not
represent a fixed business tolerance across differently sized periods. The alpha
parameters calibrate the nested resemblance hypotheses, not conventional PSI thresholds.
See [Theory](theory.md#three-decision-regions) for the exact definitions.

The widened tolerance must satisfy `m * delta <= min(reference)`, and the lower
threshold must not exceed the upper threshold. Impossible configurations raise
`ValueError`. Inspect the calibration before applying it:

```python
from population_resemblance import evaluate_calibration

calibration = evaluate_calibration(
    reference=[0.2] * 5,
    sample_size=50,
    c=0.7,
    m=2.0,
    alpha1=0.05,
    alpha2=0.10,
)

print(f"Tolerance: {calibration.delta:.6f}")
print(f"Widened tolerance: {calibration.widened_delta:.6f}")
print(f"Feasible: {calibration.feasible}")
```

```text
Tolerance: 0.039598
Widened tolerance: 0.079196
Feasible: True
```

Use `minimum_structural_sample_size()` for the probability-domain bound and
`sweep_calibration_parameters()` to compare configurations. The
[calibration workflow](examples.md#calibration-sensitivity-prs-versus-psi-and-operating-characteristics)
shows a complete sensitivity analysis.

## Count-based assessment

`assess_population_counts()` accepts observed category counts and a fixed reference probability vector.

```python
from population_resemblance import assess_population_counts

result = assess_population_counts(
    counts=[40, 35, 25],
    reference=[0.50, 0.30, 0.20],
)
```

The package derives

\[
n=\sum_j n_j,
\qquad
\hat p_j=\frac{n_j}{n},
\]

before evaluating PRS.

## Probability-based assessment

When empirical probabilities and sample size are already available:

```python
from population_resemblance import assess_population_resemblance

result = assess_population_resemblance(
    observed=[0.40, 0.35, 0.25],
    reference=[0.50, 0.30, 0.20],
    sample_size=1_000,
)
```

Use this form only when the supplied \(n\) genuinely corresponds to the empirical distribution.

## Unified monitoring report

PRS can be evaluated alongside PSI and the discrete KS benchmark:

```python
from population_resemblance import assess_population_monitoring

report = assess_population_monitoring(
    counts=[40, 35, 25],
    reference=[0.50, 0.30, 0.20],
    ks_simulations=10_000,
    ks_seed=123,
)

print(report.prs)
print(report.psi)
print(report.ks)
```

PRS is the tolerance-based decision framework. PSI and KS are comparison measures with different null hypotheses and thresholds.

## Temporal monitoring

Use a fixed reference across repeated monitoring periods:

```python
from population_resemblance import assess_temporal_monitoring

series = assess_temporal_monitoring(
    counts_by_period=[
        [50, 30, 20],
        [45, 35, 20],
        [40, 35, 25],
    ],
    reference=[0.50, 0.30, 0.20],
    labels=["Q1", "Q2", "Q3"],
    ks_simulations=5_000,
    ks_seed=123,
)
```

Each period is assessed independently against the same reference distribution. The report
does not adjust for repeated testing or dependence between periods. Overlapping windows
and repeated alerts need a monitoring policy appropriate to your application.

## Category diagnostics

The PRS decomposition identifies the categories driving the discrepancy:

```python
from population_resemblance import population_count_diagnostics

diagnostics = population_count_diagnostics(
    counts=[400, 350, 250],
    reference=[0.50, 0.30, 0.20],
    labels=["low", "medium", "high"],
)

for category in diagnostics.categories:
    print(
        category.category,
        category.signed_shift,
        category.prs_contribution,
        category.contribution_share,
    )
```

The category contributions sum exactly to the overall PRS value.

## Reference samples stored as counts

When the baseline is available as counts:

```python
from population_resemblance import assess_against_reference_counts

result = assess_against_reference_counts(
    current_counts=[40, 35, 25],
    reference_counts=[500, 300, 200],
)
```

!!! warning "Conditional interpretation"
    The reference counts are converted to empirical probabilities and then treated as fixed. This wrapper does not propagate uncertainty from the reference sample and is not a two-sample PRS test.

## Serialization

Monitoring results can be converted into JSON-safe structures:

```python
from population_resemblance import (
    assess_population_monitoring,
    monitoring_report_to_dict,
)

report = assess_population_monitoring(
    counts=[40, 35, 25],
    reference=[0.50, 0.30, 0.20],
)

payload = monitoring_report_to_dict(report)
```

Temporal series can be flattened with `temporal_series_to_records()` for downstream tabular analysis.
