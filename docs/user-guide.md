# User guide

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

Each period is assessed independently against the same reference distribution.

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
