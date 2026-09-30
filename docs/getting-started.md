# Getting started

## Requirements

Population Resemblance supports Python 3.12, 3.13, and 3.14.

The runtime dependencies are deliberately small:

- NumPy
- SciPy

## Install

The first public release, 0.1.0, is being prepared and is **not yet published to PyPI**.
Install from source until publication is announced in the [release notes](releases.md).

```bash
git clone https://github.com/DiogoRibeiro7/population-resemblance.git
cd population-resemblance
python -m venv .venv
```

Activate the virtual environment:

- macOS/Linux: `source .venv/bin/activate`
- Windows PowerShell: `.\.venv\Scripts\Activate.ps1`

Then install the package and its runtime dependencies:

```bash
python -m pip install .
```

Run the Python examples below in that environment, either interactively with `python`
or from a saved script.

### Contributor installation

Development requires **Poetry 2.5.x**; **2.5.1** matches CI. With
[pipx installed](https://pipx.pypa.io/stable/installation/), install Poetry separately:

```bash
pipx install poetry==2.5.1
```

From the repository root, install the locked development and documentation dependencies:

```bash
poetry install --with docs
poetry run pytest
```

Run scripts with `poetry run python` and serve the docs with `poetry run mkdocs serve`.
See [Development](development.md) for the full check list.

## First assessment

For real monitoring data, the count-based API is usually the safest entry point because the sample size is derived directly from the observed counts.

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

The sample contains 1,000 observations. Its PRS exceeds the upper threshold, so the
default calibration assigns R3. This identifies a population discrepancy to investigate;
it does not establish that a predictive model has failed. PRS itself is not a p-value.

| Region | Label | Decision rule | Practical interpretation |
| --- | --- | --- | --- |
| R1 | acceptable | PRS ≤ lower threshold | Continue monitoring. |
| R2 | partially discrepant | Lower threshold < PRS ≤ upper threshold | Increase monitoring. |
| R3 | fully discrepant | PRS > upper threshold | Investigate the discrepancy. |

These decisions depend on the tolerance and calibration settings. See
[Choosing calibration parameters](user-guide.md#choosing-calibration-parameters) for the
meaning of `delta`, `c`, `m`, `alpha1`, and `alpha2`, and read
[Inputs and assumptions](user-guide.md#inputs-and-assumptions) before using new data.

The result contains the PRS value, calibrated tolerance, least-favourable non-centrality, decision boundaries, sample size, and final decision region.

## Named categories

When category order should be explicit, use mappings:

```python
from population_resemblance import assess_named_population

result = assess_named_population(
    counts={
        "high": 250,
        "low": 400,
        "medium": 350,
    },
    reference={
        "low": 0.50,
        "medium": 0.30,
        "high": 0.20,
    },
)

print(result.categories)
print(result.monitoring.prs)
```

The reference mapping defines the canonical category order. The current counts must contain exactly the same category names.

## Reusable monitor

For recurring production checks, configure the reference distribution once:

```python
from population_resemblance import PopulationMonitor

monitor = PopulationMonitor.from_reference(
    [0.50, 0.30, 0.20],
    c=0.7,
    m=2.0,
    ks_simulations=5_000,
    ks_seed=123,
)

first = monitor.assess([500, 300, 200])
second = monitor.assess([450, 350, 200])
```

Continue with the [User guide](user-guide.md) for the full workflow.
