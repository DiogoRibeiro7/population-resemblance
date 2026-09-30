<div class="resemblance-hero" markdown="1">

# Monitor population shift with explicit statistical tolerance

Population Resemblance provides a typed Python toolkit for categorical distribution monitoring, built around the Population Resemblance Statistic (PRS), sample-size-aware decision boundaries, diagnostics, simulation, and practical monitoring workflows.

[Get started](getting-started.md){ .md-button .md-button--primary }
[Explore the API](api.md){ .md-button }

</div>

<div class="resemblance-cards" markdown="1">

<div markdown="1">

### Tolerance-aware decisions

Separate material population shift from exact equality using \(\delta\)-resemblance and non-central \(\chi^2\) decision boundaries.

</div>

<div markdown="1">

### Monitoring workflows

Assess raw counts, named categories, repeated periods, reusable monitors, and empirical reference samples.

</div>

<div markdown="1">

### Diagnostics and simulation

Inspect category contributions, calibration sensitivity, operating-characteristic curves, and Monte Carlo uncertainty.

</div>

</div>

## What the package does

The core statistic is

\[
\mathrm{PRS}
=
\sum_{j=1}^{B}
\frac{(\hat p_j-p_{0j})^2}{p_{0j}},
\]

where \(p_0\) is a fixed reference distribution and \(\hat p\) is the empirical current distribution.

The package implements the full decision framework around that statistic, including \(\delta\)-resemblance, least-favourable non-centrality, and the three decision regions \(R_1\), \(R_2\), and \(R_3\).

It also includes PSI and discrete Kolmogorov-Smirnov benchmarks, but keeps them conceptually separate because they use different decision rules.

## Where it fits

Population Resemblance is designed for any problem where a categorical population must be monitored against a baseline. Banking is the original application, but the abstraction applies equally to model-output classes, patient-risk groups, manufacturing states, customer segments, failure modes, or other discrete populations.

!!! note "Statistical scope"
    The implemented PRS methodology uses a fixed reference distribution \(p_0\). When reference counts are supplied, the package converts them to empirical probabilities and treats those probabilities as fixed conditionally. A genuine two-sample PRS formulation is not claimed.

## Scientific basis

The initial implementation follows:

> Potgieter, C. J., Van Zyl, C., Schutte, W. D., & Lombard, F. (2026).  
> *The population resemblance statistic: a chi-square measure of fit for banking*.  
> Annals of Operations Research, 361, 413–435.

See [Theory](theory.md) for the statistical formulation and [Simulation](simulation.md) for calibration and operating-characteristic tools.
