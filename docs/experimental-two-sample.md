# Experimental independent two-sample resemblance

The package includes an **experimental** API for comparing two independent categorical
samples while propagating sampling uncertainty from both samples.

It is deliberately not exported from the stable package root.

## Import

Use the experimental namespace explicitly:

```python
from population_resemblance.experimental import (
    assess_independent_two_sample_resemblance,
)

result = assess_independent_two_sample_resemblance(
    [420, 330, 250],
    [390, 360, 250],
    samples_are_independent=True,
)

print(result.statistic)
print(result.region)
print(result.effective_sample_size)
print(result.pooled_probabilities)
```

The explicit `samples_are_independent=True` argument is intentional. This implementation
must not be used silently for overlapping, paired, repeated, clustered, or otherwise
dependent samples.

## Statistic

For sample sizes \(n\) and \(m\),

\[
n_{\mathrm{eff}}=\frac{nm}{n+m}.
\]

Let \(\widehat p\) and \(\widehat q\) be the sample proportions and let

\[
\widehat r_j
=
\frac{x_j+y_j}{n+m}
\]

be the pooled empirical distribution.

The experimental statistic is

\[
Q_{n,m}
=
n_{\mathrm{eff}}
\sum_j
\frac{
(\widehat p_j-\widehat q_j)^2
}{
\widehat r_j
}.
\]

At the point null this is exactly Pearson's two-sample homogeneity statistic.

## Plug-in resemblance calibration

If `delta` is omitted, the experimental method uses

\[
\widehat\delta
=
c\min_j
\sqrt{
\frac{
\widehat r_j(1-\widehat r_j)
}{
n_{\mathrm{eff}}
}
}.
\]

The least-favourable non-centrality and nested decision boundaries are then calculated from
the pooled empirical centre.

This is the plug-in procedure studied in the repository research work. It has finite-sample
simulation support, but it does **not** have a claim of uniform composite-null validity.

## Sparse-category policy

The experimental API enforces the Phase 2 sparse-category policy.

It rejects the assessment when:

- any pooled category count is zero;
- the minimum pooled expected count is below 5;
- the widened resemblance region violates the structural probability-domain bound.

The method never adds epsilon smoothing, silently drops categories, or merges categories.

## Dependence is unsupported

The independent effective sample size is invalid in general when samples overlap or contain
paired/repeated observations.

The research notes derive an exact correction for one special overlap model, but that
correction is **not** part of this experimental API.

For general dependence, a covariance-aware Wald construction is required.

See:

- [Independent asymptotics](two-sample-asymptotics.md)
- [Critical values](two-sample-critical-values.md)
- [Finite-sample calibration](two-sample-calibration.md)
- [Dependence and overlap](two-sample-dependence.md)
- [Sparse-category policy](two-sample-sparse-policy.md)

## Stability status

The experimental namespace is outside the stable package-root compatibility boundary.

Its function names, result objects, validation policy, and statistical calibration may change
before promotion to the stable public API.
