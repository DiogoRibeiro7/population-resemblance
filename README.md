# population-resemblance

Statistically principled monitoring of categorical population and distribution shifts.

## Scope

`population-resemblance` is a Python package for measuring and monitoring changes in
categorical probability distributions. The project begins with the Population Resemblance
Statistic (PRS) proposed by Potgieter, Van Zyl, Schutte, and Lombard and is intentionally
designed as a general distribution-monitoring library rather than a banking-specific tool.

The initial implementation provides the core statistic

\[
\operatorname{PRS} = \sum_{j=1}^{B}
\frac{(\hat p_j - p_{0j})^2}{p_{0j}}.
\]

The package now implements the paper's \(\delta\)-resemblance decision framework,
including sample-size-aware tolerance calibration, least-favourable non-centrality,
non-central chi-square critical values, and the three PRS decision regions.

The package also includes the traditional Population Stability Index (PSI) and Lewis
threshold classification as explicit benchmarks. They are kept separate from the PRS
decision framework because they answer a different monitoring question and do not account
for sample size in the same way.

Monte Carlo tooling is available for studying the operating characteristics of the PRS
decision regions under controlled population shifts.

The package also supports direct Monte Carlo comparison of PRS and PSI on identical samples.

The package also includes a discrete Kolmogorov-Smirnov benchmark with Monte Carlo
calibration under the categorical reference distribution.

A unified reporting API can now evaluate PRS, PSI, and discrete KS from the same observed
count vector.

Future work will add further benchmark drift measures and extensions such as two-sample
and cost-sensitive monitoring.

## Installation

The first public package release is version `0.1.0`.

After publication to PyPI:

```bash
python -m pip install population-resemblance
```

The package supports Python 3.12, 3.13, and 3.14.

For development from source:

```bash
git clone https://github.com/DiogoRibeiro7/population-resemblance.git
cd population-resemblance
poetry install --with docs
```

## Quick start

For real observed samples, the count-based API is preferred because it derives the sample
size directly from the data.

```python
from population_resemblance import assess_population_counts

result = assess_population_counts(
    counts=[400, 350, 250],
    reference=[0.50, 0.30, 0.20],
)

print(result.statistic)
print(result.region)
print(result.critical_values)
```

A probability-based API is also available when empirical proportions and the sample size
are already known explicitly.

```python
from population_resemblance import assess_population_resemblance

result = assess_population_resemblance(
    observed=[0.40, 0.35, 0.25],
    reference=[0.50, 0.30, 0.20],
    sample_size=1_000,
)
```

If a domain-specific tolerance is available, pass `delta=` explicitly. Otherwise the
package uses the sample-size-aware recommendation from the source methodology.

## Simulation

The simulation API can estimate how often a specified current population is classified into
each PRS decision region.

```python
from population_resemblance import (
    recommended_delta,
    simulate_region_probabilities,
    symmetric_category_shift,
)

reference = [0.2] * 5
delta = recommended_delta(reference, sample_size=50, c=0.7)
current = symmetric_category_shift(reference, delta)

result = simulate_region_probabilities(
    current=current,
    reference=reference,
    sample_size=50,
    simulations=30_000,
    seed=123,
    delta=delta,
)

print(result.probabilities)
```

This is useful for sensitivity analysis, calibration checks, and reproducing the simulation
logic used to validate the original PRS framework.

## PRS versus PSI

The comparison API applies both methods to the same Monte Carlo samples, making it possible
to study how the sample-size-aware PRS framework behaves relative to the traditional fixed
PSI thresholds.

```python
from population_resemblance import simulate_prs_psi_comparison

result = simulate_prs_psi_comparison(
    current=[0.17, 0.17, 0.20, 0.23, 0.23],
    reference=[0.20] * 5,
    sample_size=500,
    simulations=10_000,
    seed=123,
)

print(result.prs)
print(result.psi)
```

This comparison is descriptive: PRS and PSI use different decision rules, so matching
classification probabilities are neither expected nor required.

## Discrete KS benchmark

The package also exposes a discrete Kolmogorov-Smirnov benchmark. Because the discrete
KS statistic is not distribution-free with respect to the reference probabilities, the
package calibrates its p-value by Monte Carlo simulation under the multinomial reference.

```python
from population_resemblance import discrete_ks_test_counts

result = discrete_ks_test_counts(
    counts=[35, 40, 45, 45, 47, 50, 55, 58, 60, 65],
    reference=[0.10] * 10,
    simulations=10_000,
    seed=123,
)

print(result.statistic)
print(result.p_value)
print(result.status)
```

The default status convention mirrors the paper's comparison: p-values below 1% are red,
above 10% are green, and intermediate values are amber.

## Unified monitoring report

For practical monitoring workflows, all three methods can be evaluated from the same
observed count vector.

```python
from population_resemblance import assess_population_monitoring

report = assess_population_monitoring(
    counts=[35, 40, 45, 45, 47, 50, 55, 58, 60, 65],
    reference=[0.10] * 10,
    ks_simulations=10_000,
    ks_seed=123,
)

print(report.prs)
print(report.psi)
print(report.ks)
```

PRS remains the tolerance-based decision framework. PSI and discrete KS are reported as
benchmarks because their null hypotheses and decision rules are different.

## Temporal monitoring

Repeated population snapshots can be assessed against the same fixed reference distribution.

```python
from population_resemblance import assess_temporal_monitoring

series = assess_temporal_monitoring(
    counts_by_period=[
        [50, 30, 20],
        [45, 35, 20],
        [40, 35, 25],
    ],
    reference=[0.50, 0.30, 0.20],
    labels=["2026-Q1", "2026-Q2", "2026-Q3"],
    ks_simulations=5_000,
    ks_seed=123,
)

print(series.labels)
print(series.prs_statistics)
print(series.psi_statistics)
print(series.ks_statistics)
```

The reference distribution remains fixed while each period is assessed independently.
This makes the API suitable for recurring model- or population-monitoring workflows.

## Category diagnostics

PRS can also be decomposed into category-level contributions, making it easier to see
which parts of the population are driving the overall discrepancy.

```python
from population_resemblance import population_count_diagnostics

diagnostics = population_count_diagnostics(
    counts=[400, 350, 250],
    reference=[0.50, 0.30, 0.20],
    labels=["low", "medium", "high"],
)

print(diagnostics.statistic)
print(diagnostics.largest_contributor)

for category in diagnostics.categories:
    print(
        category.category,
        category.signed_shift,
        category.prs_contribution,
        category.contribution_share,
    )
```

The decomposition is exact: the per-category PRS contributions sum to the full statistic.
This adds interpretability without changing the underlying method.

## Calibration diagnostics

The PRS framework can be inspected before any monitoring decision is made.

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

print(calibration.delta)
print(calibration.widened_delta)
print(calibration.lambda_sup)
print(calibration.lower_critical_value)
print(calibration.upper_critical_value)
print(calibration.feasible)
```

This is useful for validating parameter choices and understanding how the tolerance,
reference distribution, and sample size determine the PRS decision boundaries.

## Empirical reference samples

When the baseline is available as counts rather than probabilities, the package can derive
the empirical reference distribution directly.

```python
from population_resemblance import assess_against_reference_counts

result = assess_against_reference_counts(
    current_counts=[40, 35, 25],
    reference_counts=[500, 300, 200],
    ks_simulations=5_000,
    ks_seed=123,
)

print(result.reference_probabilities)
print(result.current_sample_size)
print(result.reference_sample_size)
print(result.monitoring.prs)
```

This is still the paper's one-sample conditional formulation: the empirical baseline is
converted to probabilities and then treated as fixed. It is not a two-sample PRS test and
does not propagate uncertainty from the reference sample into the critical values.

## Operating-characteristic curves

The package can reproduce the simulation design used in the paper by evaluating PRS
classification probabilities across a sequence of deviations measured in multiples of
\(\delta\).

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

By default, the curve uses 30 deviation values from zero to \((3M + 2)\delta\), matching
the range described in the source simulation study.

## Calibration sensitivity analysis

Calibration choices can be explored over a full Cartesian grid of `c`, `M`,
`alpha1`, and `alpha2`.

```python
from population_resemblance import sweep_calibration_parameters

grid = sweep_calibration_parameters(
    reference=[0.2] * 5,
    sample_size=100,
    c_values=[0.5, 0.7, 1.0],
    m_values=[1.2, 1.5, 2.0],
    alpha1_values=[0.05, 0.10],
    alpha2_values=[0.10],
)

print(len(grid.feasible_points))
print(len(grid.infeasible_points))
```

Invalid parameter combinations are retained with their error message instead of aborting
the full sweep. This makes structural constraints and sensitivity trade-offs visible.

## Named categories

For application code, category names can be used directly rather than relying on positional
arrays. The reference mapping defines the canonical category order.

```python
from population_resemblance import assess_named_population

result = assess_named_population(
    counts={
        "high": 25,
        "low": 40,
        "medium": 35,
    },
    reference={
        "low": 0.50,
        "medium": 0.30,
        "high": 0.20,
    },
)

print(result.categories)
print(result.counts)
print(result.monitoring.prs)
```

The API requires the current and reference mappings to contain exactly the same category
names, preventing silent errors caused by inconsistent category ordering.

## Reusable monitor objects

For production workflows, the reference distribution and calibration settings can be stored
once and reused across many assessments.

```python
from population_resemblance import PopulationMonitor

monitor = PopulationMonitor.from_reference(
    [0.50, 0.30, 0.20],
    c=0.7,
    m=2.0,
    ks_simulations=5_000,
    ks_seed=123,
)

first = monitor.assess([50, 30, 20])
second = monitor.assess([45, 35, 20])

series = monitor.assess_temporal(
    [
        [50, 30, 20],
        [45, 35, 20],
        [40, 35, 25],
    ],
    labels=["Q1", "Q2", "Q3"],
)
```

A `NamedPopulationMonitor` provides the same pattern for named categories. These monitor
objects do not introduce new statistics; they package the existing validated configuration
for repeated use.

## Monte Carlo uncertainty

Simulation-based region probabilities can be accompanied by Wilson confidence intervals
that quantify Monte Carlo error.

```python
from population_resemblance import (
    simulate_region_probabilities,
    simulation_uncertainty,
)

result = simulate_region_probabilities(
    current=[0.40, 0.35, 0.25],
    reference=[0.50, 0.30, 0.20],
    sample_size=250,
    simulations=10_000,
    seed=123,
)

uncertainty = simulation_uncertainty(result, confidence_level=0.95)

print(uncertainty.r1)
print(uncertainty.r2)
print(uncertainty.r3)
```

These intervals describe simulation uncertainty only. They are not confidence intervals
for the PRS parameters or for the underlying population shift.

## Serialization

Monitoring outputs can be converted to JSON-safe dictionaries or flat temporal records for
APIs, logs, persistence, and tabular analysis.

```python
import json

from population_resemblance import (
    assess_population_monitoring,
    monitoring_report_to_dict,
)

report = assess_population_monitoring(
    counts=[40, 35, 25],
    reference=[0.50, 0.30, 0.20],
)

payload = monitoring_report_to_dict(report)
print(json.dumps(payload))
```

Temporal monitoring series can likewise be converted to one flat record per period using
`temporal_series_to_records()`.

## Development

The project supports Python 3.12, 3.13, and 3.14 and uses Poetry, pytest, Ruff, mypy, and pre-commit.

```bash
poetry install
poetry run pytest
poetry run ruff check .
poetry run mypy src tests
```

## Scientific attribution

The initial PRS methodology is based on:

> Potgieter, C. J., Van Zyl, C., Schutte, W. D., & Lombard, F. (2026).
> *The population resemblance statistic: a chi-square measure of fit for banking*.
> Annals of Operations Research, 361, 413–435.

This repository is an independent software implementation and extension of that methodology.


## Citation

If you use this software in research, cite the repository using `CITATION.cff` and cite the original PRS methodology:

> Potgieter, C. J., Van Zyl, C., Schutte, W. D., & Lombard, F. (2026).  
> *The population resemblance statistic: a chi-square measure of fit for banking*.  
> Annals of Operations Research, 361, 413–435.  
> https://doi.org/10.1007/s10479-025-07024-6

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow, statistical-change requirements, and local quality checks.
