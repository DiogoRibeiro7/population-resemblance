# Finite-sample calibration of the two-sample plug-in candidate

This note addresses research issue #46.

It studies the independent two-sample resemblance candidate derived in #44 and #45. The
procedure examined here is still research code, not a public package API.

## Candidate under study

For independent samples of sizes \(n\) and \(m\), define

\[
n_{\mathrm{eff}}=\frac{nm}{n+m}
\]

and the empirical pooled proportions

\[
\widehat r_j
=
\frac{X_j+Y_j}{n+m}.
\]

The candidate statistic is

\[
Q_{n,m}
=
n_{\mathrm{eff}}
\sum_j
\frac{(\widehat p_j-\widehat q_j)^2}{\widehat r_j}.
\]

The plug-in tolerance is

\[
\widehat\delta
=
c\min_j
\sqrt{
\frac{\widehat r_j(1-\widehat r_j)}
{n_{\mathrm{eff}}}
}.
\]

The corresponding plug-in least-favourable non-centrality and nested decision boundaries
are recomputed separately for each simulated pair of samples.

For comparison, the study also evaluates:

- **oracle calibration**, using the true pooled population centre \(r\);
- the classical Pearson homogeneity test at the 5% point-null significance level.

The Pearson benchmark answers a different question from resemblance testing and is included
only as a calibration reference.

## Simulation design

The executable study is:

```bash
poetry run python research/simulate_two_sample_calibration.py
```

The scenarios include:

| Scenario | Reference distribution | \(n\) | \(m\) |
| --- | --- | ---: | ---: |
| balanced small | \((0.2,0.2,0.2,0.2,0.2)\) | 50 | 50 |
| balanced medium | same | 200 | 200 |
| balanced large | same | 1000 | 1000 |
| balanced unequal | same | 100 | 400 |
| imbalanced | \((0.40,0.25,0.15,0.12,0.08)\) | 100 | 100 |
| sparse | \((0.70,0.15,0.08,0.05,0.02)\) | 100 | 100 |

For each scenario, the true difference vector is placed at:

- \(0\delta\): equality;
- \(1\delta\): the tighter resemblance boundary;
- \(2\delta=M\delta\): the wider boundary for \(M=2\);
- \(3\delta\): outside the wider resemblance region, when the true probabilities remain valid.

The difference direction uses the same fixed-centre extreme-point geometry derived in #45.

## Main empirical findings

With 30,000 simulations per configuration and the repository seed 2026, the broad pattern is
stable.

### Point-null benchmark

For the non-sparse scenarios, the classical Pearson homogeneity rejection probability stays
close to 5% under equality. This is expected because the candidate statistic is exactly the
Pearson homogeneity statistic at the point null.

The sparse scenario is more fragile because some simulated pooled cells are zero.

### Upper resemblance boundary

At the \(\delta\) boundary, the plug-in probability of entering \(R_3\) is generally close
to the target \(\alpha_1=0.05\) in balanced and moderately imbalanced settings.

In the balanced small-sample case, the empirical plug-in \(R_3\) probability is about
5%, while the oracle value is slightly lower. The discrepancy shrinks with increasing sample
size.

### Wider resemblance boundary

At \(M\delta=2\delta\), the target probability of remaining in \(R_1\) is
\(\alpha_2=0.10\).

The empirical plug-in values are near 0.10 for moderate and imbalanced cases, but can be
somewhat conservative in smaller balanced samples. The finite-sample deviation is visible
rather than negligible, which is one reason the procedure should not yet be promoted to a
public statistical API.

### Unequal sample sizes

The \(n=100,m=400\) scenario behaves similarly to equal-size balanced scenarios with a
comparable effective sample size. This supports the role of

\[
n_{\mathrm{eff}}=\frac{nm}{n+m}
\]

as the correct first-order scaling quantity.

It does not, by itself, prove uniform resemblance calibration.

### Sparse categories

The sparse reference

\[
(0.70,0.15,0.08,0.05,0.02)
\]

exposes the main practical weakness.

Roughly 9% of the simulated pairs fail the research procedure's interior/feasibility checks
at \(n=m=100\), primarily because pooled empirical cells can be zero or the data-dependent
wider resemblance region violates the probability-domain bound.

The \(3\delta\) extreme alternative is itself infeasible for the true probability vectors in
this scenario.

This is not a numerical nuisance to hide. It is a structural limitation that a production
method must address explicitly.

## Plug-in versus oracle calibration

For balanced small samples, recomputing \(\widehat\delta\) and
\(\lambda_{\sup}(\widehat r,\widehat\delta)\) from the data changes the decision
probabilities visibly relative to oracle calibration.

The difference becomes smaller as sample size increases.

For the moderately imbalanced scenario studied here, plug-in and oracle classifications are
already quite close at \(n=m=100\).

This supports **pointwise plausibility**, not uniform validity.

## Research conclusion

The simulations do not falsify the independent plug-in candidate in well-populated
categories. Boundary behavior is reasonably close to nominal values across the balanced,
unequal-size, and moderately imbalanced scenarios examined.

However, the study also shows two reasons not to expose the method as a public API yet:

1. finite-sample plug-in calibration is not identical to oracle calibration, especially in
   smaller samples;
2. sparse categories create zero pooled cells and feasibility failures with non-negligible
   probability.

The remaining dependence problem in #47 is separate and potentially more consequential:
all results here assume independent samples.

## Status after #46

The independent-sample candidate now has:

- an asymptotic derivation;
- conditional least-favourable critical values;
- finite-sample plug-in simulation evidence;
- a classical point-null benchmark.

A production method still requires a policy for sparse categories and a clear restriction to
independent samples, unless #47 provides a validated covariance correction for dependent or
overlapping samples.
