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

Future work will add additional benchmark drift measures and extensions such as two-sample
and cost-sensitive monitoring.

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

## Development

The project targets Python 3.12 and uses Poetry, pytest, Ruff, mypy, and pre-commit.

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
