# population-resemblance

Python tools for monitoring changes in categorical populations with the Population
Resemblance Statistic (PRS), sample-size-aware thresholds, PSI and discrete KS benchmarks,
and Monte Carlo simulation.

[Documentation](https://diogoribeiro7.github.io/population-resemblance/) ·
[Getting started](https://diogoribeiro7.github.io/population-resemblance/getting-started/) ·
[API reference](https://diogoribeiro7.github.io/population-resemblance/api/) ·
[Contributing](CONTRIBUTING.md)

## What it does

Compare current category counts against a fixed reference distribution, assess whether
the shift is acceptable under a chosen tolerance, and identify which categories contribute
to the discrepancy. Applications include model-output classes, customer segments, and
other discrete populations.

The core statistic is

$$
\operatorname{PRS} = \sum_{j=1}^{B} \frac{(\hat p_j - p_{0j})^2}{p_{0j}}.
$$

The package implements the $\delta$-resemblance framework of Potgieter et al., including
three decision regions. PSI and discrete KS are benchmarks with different decision rules.
Named categories, temporal reports, reusable monitors, calibration diagnostics, and JSON
export support recurring monitoring workflows.

## Installation

**Status: preparing the first public release, 0.1.0; not yet published to PyPI.**
Use a source installation with Python **3.12, 3.13, or 3.14**:

```bash
git clone https://github.com/DiogoRibeiro7/population-resemblance.git
cd population-resemblance
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux or
`.\.venv\Scripts\Activate.ps1` in Windows PowerShell, then install:

```bash
python -m pip install .
```

NumPy and SciPy are installed automatically. Contributors should use **Poetry 2.5.x**
(2.5.1 matches CI); see the [development setup](CONTRIBUTING.md#development-environment).
Track publication in the [release notes](https://diogoribeiro7.github.io/population-resemblance/releases/).

## Quick start

Run this in the installed environment. The count-based API derives the sample size from
the data; the counts and reference probabilities must use the same category order.

```python
from population_resemblance import assess_population_counts

result = assess_population_counts(
    counts=[400, 350, 250],
    reference=[0.50, 0.30, 0.20],
)

print(f"PRS: {result.statistic:.6f}")
print(f"Region: {result.region} ({result.label})")
print(
    f"Thresholds: {result.critical_values.lower:.6f}, "
    f"{result.critical_values.upper:.6f}"
)
```

```text
PRS: 0.040833
Region: R3 (fully discrepant)
Thresholds: 0.000710, 0.007793
```

Here the PRS exceeds the upper threshold, placing the sample in R3 under the default
calibration. Investigate the population change; this classification alone does not
establish that a predictive model has failed.

| Region | Label | Interpretation |
| --- | --- | --- |
| R1 | acceptable | PRS is at or below the lower threshold; continue monitoring. |
| R2 | partially discrepant | PRS is between the thresholds; increase monitoring. |
| R3 | fully discrepant | PRS exceeds the upper threshold; investigate the discrepancy. |

PRS is a discrepancy statistic, not a p-value. Supply `delta=` for an explicit
category-probability tolerance, or use the default that varies with sample size.
See [calibration choices](https://diogoribeiro7.github.io/population-resemblance/user-guide/#choosing-calibration-parameters)
before interpreting decisions in your application.

## Assumptions and limitations

- PRS uses a fixed reference with strictly positive category probabilities. Reference
  counts are treated conditionally as fixed probabilities; this is not a two-sample test.
- PRS thresholds use an asymptotic approximation. Sparse categories and small samples
  need calibration checks.
- Discrete KS depends on category order. Choose a meaningful, fixed order before comparing
  periods; arbitrary ordering of nominal labels changes the benchmark.
- PSI follows the source paper's convention of omitting zero observed-probability
  contributions. It does not automatically smooth them.
- Temporal reports assess each period separately, without adjustment for repeated testing
  or dependence between periods.

Read the [input and interpretation guidance](https://diogoribeiro7.github.io/population-resemblance/user-guide/#inputs-and-assumptions)
for zero counts, category alignment, and sparse data. Two-sample extensions remain
[research](https://diogoribeiro7.github.io/population-resemblance/two-sample-research/).

## More examples

| Task | Documentation |
| --- | --- |
| Named categories and reusable monitors | [Getting started](https://diogoribeiro7.github.io/population-resemblance/getting-started/#named-categories) |
| Temporal monitoring, diagnostics, and export | [User guide](https://diogoribeiro7.github.io/population-resemblance/user-guide/) |
| Calibration and sensitivity | [Calibration choices](https://diogoribeiro7.github.io/population-resemblance/user-guide/#choosing-calibration-parameters) |
| PRS/PSI comparisons and operating-characteristic curves | [Simulation](https://diogoribeiro7.github.io/population-resemblance/simulation/) |
| Complete runnable workflows | [Examples](https://diogoribeiro7.github.io/population-resemblance/examples/) |
| Reproducing published numerical results | [Reproducibility](https://diogoribeiro7.github.io/population-resemblance/reproducibility/) |

## Citation and license

This is an independent implementation and extension of:

> Potgieter, C. J., Van Zyl, C., Schutte, W. D., & Lombard, F. (2026).
> *The population resemblance statistic: a chi-square measure of fit for banking*.
> Annals of Operations Research, 361, 413–435.
> [doi:10.1007/s10479-025-07024-6](https://doi.org/10.1007/s10479-025-07024-6)

For research use, cite both the methodology and this software using [CITATION.cff](CITATION.cff).
Distributed under the [MIT license](LICENSE).
