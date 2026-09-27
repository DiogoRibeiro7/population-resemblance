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

Future work will add the paper's full \(\delta\)-resemblance decision framework,
sample-size-aware critical values, simulation tooling, benchmark drift measures, and
extensions such as two-sample and cost-sensitive monitoring.

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
