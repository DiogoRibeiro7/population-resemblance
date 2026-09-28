# Getting started

## Requirements

Population Resemblance targets Python 3.12.

The runtime dependencies are deliberately small:

- NumPy
- SciPy

## Install from source

Clone the repository and install with Poetry:

```bash
git clone https://github.com/DiogoRibeiro7/population-resemblance.git
cd population-resemblance
poetry install
```

Run the test suite:

```bash
poetry run pytest
```

## First assessment

For real monitoring data, the count-based API is usually the safest entry point because the sample size is derived directly from the observed counts.

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
