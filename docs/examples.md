# End-to-end examples

These examples show complete, domain-neutral monitoring workflows using the public package API.

## Single assessment and named categories

Run:

```bash
poetry run python examples/workflow_single_and_named.py
```

This example covers a count-based PRS assessment and the equivalent named-category workflow.

The count-based API is usually preferable when raw observations are available because the sample size is derived directly from the counts. Named categories are useful when category ordering should be explicit in application code.

## Temporal monitoring and category diagnostics

Run:

```bash
poetry run python examples/workflow_temporal_and_diagnostics.py
```

This example evaluates several population snapshots against one fixed reference distribution, then decomposes the final PRS value into category-level contributions.

The temporal results should be interpreted period by period. The package does not fit a time-series model to the sequence and does not account for dependence between monitoring periods.

## Calibration sensitivity, PRS versus PSI, and operating characteristics

Run:

```bash
poetry run python examples/workflow_calibration_and_comparison.py
```

This example demonstrates three related workflows:

1. sensitivity of the PRS calibration to choices of \(c\) and \(M\);
2. descriptive comparison of PRS and PSI classifications on identical Monte Carlo samples;
3. operating-characteristic probabilities over increasing population shifts.

!!! note
    The PRS-versus-PSI comparison is descriptive. The methods have different decision rules, so agreement is not a requirement.

!!! note
    The operating-characteristic output is not conventional statistical power. The PRS framework uses nested composite null hypotheses.

## JSON and tabular export

Run:

```bash
poetry run python examples/workflow_export.py
```

The example converts a unified monitoring report to a JSON-safe dictionary and a temporal monitoring series to flat records.

These outputs are suitable for application APIs, logging, persistence, or conversion to tools such as pandas without adding pandas as a runtime dependency.

## Related examples

For source-paper numerical reproductions, see [Reproducibility](reproducibility.md).

For large Monte Carlo workloads, see [Simulation](simulation.md#memory-bounded-monte-carlo).
