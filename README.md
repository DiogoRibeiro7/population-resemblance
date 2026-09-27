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

Future work will add simulation tooling, benchmark drift measures, and extensions such as
two-sample and cost-sensitive monitoring.

## Quick start

```python
from population_resemblance import assess_population_resemblance

result = assess_population_resemblance(
    observed=[0.40, 0.35, 0.25],
    reference=[0.50, 0.30, 0.20],
    sample_size=1_000,
)

print(result.statistic)
print(result.region)
print(result.critical_values)
```

If a domain-specific tolerance is available, pass `delta=` explicitly. Otherwise the
package uses the sample-size-aware recommendation from the source methodology.

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
