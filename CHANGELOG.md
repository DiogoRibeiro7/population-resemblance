# Changelog

All notable changes to `population-resemblance` are documented here.

The project follows semantic-versioning expectations described in the
[public API policy](docs/public-api.md).

## 0.1.0 — initial public release

### Statistical framework

- Population Resemblance Statistic (PRS)
- sample-size-aware recommended tolerance
- least-favourable non-centrality calculation
- nested PRS decision regions with non-central chi-square critical values
- structural feasibility diagnostics and sample-size planning

### Monitoring APIs

- probability- and count-based assessment
- named-category monitoring
- reusable configured monitor objects
- repeated temporal monitoring
- empirical reference-count wrapper with explicit one-sample interpretation

### Diagnostics and benchmarks

- category-level PRS contribution diagnostics
- calibration diagnostics and sensitivity sweeps
- Population Stability Index benchmark
- Monte Carlo calibrated discrete Kolmogorov-Smirnov benchmark
- PRS-versus-PSI simulation comparison

### Simulation

- PRS region-probability simulation
- operating-characteristic curves
- Monte Carlo uncertainty intervals
- memory-bounded chunked simulation
- source-paper reproducibility scripts

### Engineering

- typed Python API with PEP 561 marker
- Python 3.12, 3.13, and 3.14 support
- reproducible Poetry lockfile
- strict Ruff and mypy checks
- MkDocs Material documentation
- GitHub Pages deployment
- PyPI Trusted Publishing release workflow
- citation and contribution metadata

### Scope

The implemented PRS method follows the fixed-reference one-sample formulation.
The empirical reference-count wrapper treats the estimated baseline probabilities
as fixed conditionally and is not a genuine two-sample PRS test.
