# Two-sample population resemblance: research note

This note records the current mathematical research direction for a genuine two-sample
extension of the Population Resemblance Statistic (PRS).

It is intentionally **not** a public statistical API specification. The existing package
continues to implement the fixed-reference one-sample framework.

## Motivation

The current empirical-reference wrapper converts baseline counts into probabilities and then
treats those probabilities as fixed. That is a conditional one-sample construction.

A genuine two-sample procedure must propagate uncertainty from both samples.

Let

\[
\widehat p=(\widehat p_1,\ldots,\widehat p_B)^\top
\]

and

\[
\widehat q=(\widehat q_1,\ldots,\widehat q_B)^\top
\]

be empirical proportions from two multinomial samples of sizes \(n\) and \(m\).

## Independent-sample starting point

Assume first that the two samples are independent.

If both samples arise from a common probability vector \(r\), then

\[
\operatorname{Var}(\widehat p-\widehat q)
=
\left(\frac{1}{n}+\frac{1}{m}\right)
\Sigma(r),
\]

where

\[
\Sigma(r)=\operatorname{diag}(r)-rr^\top.
\]

Define the effective sample size

\[
n_{\mathrm{eff}}
=
\frac{nm}{n+m}.
\]

Then the candidate normalized difference is

\[
\sqrt{n_{\mathrm{eff}}}(\widehat p-\widehat q).
\]

Under equality, its limiting covariance is \(\Sigma(r)\), which has rank \(B-1\).

This suggests the candidate quadratic form

\[
Q_{n,m}
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(\widehat p_j-\widehat q_j)^2}{r_j}.
\]

If \(r\) were known, the natural conjecture is a limiting
\(\chi^2_{B-1}\) distribution under equality.

Because \(r\) is unknown in a true two-sample problem, a practical statistic would need a
plug-in estimate, most naturally the pooled empirical distribution

\[
\widehat r_j
=
\frac{n\widehat p_j+m\widehat q_j}{n+m}.
\]

The validity of replacing \(r\) by \(\widehat r\) must be established formally rather
than assumed.

## Local alternatives

A direct analogue of the one-sample local-alternative construction would consider

\[
p-q
=
\frac{\xi}{\sqrt{n_{\mathrm{eff}}}},
\qquad
\mathbf 1^\top\xi=0.
\]

If the covariance and plug-in arguments hold, the candidate limiting distribution becomes
non-central chi-square with

\[
\lambda
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(p_j-q_j)^2}{r_j}.
\]

This expression is currently a research target, not yet a package guarantee.

## Candidate resemblance definition

The simplest two-sample resemblance region would be

\[
\max_j |p_j-q_j| \le \delta.
\]

That preserves the original category-wise interpretation of resemblance.

However, the two-sample case introduces a nuisance probability vector \(r\), so the
least-favourable non-centrality problem is no longer automatically identical to the
one-sample derivation.

Questions still to prove include:

- whether pooled weights are asymptotically valid under local alternatives;
- whether the least-favourable configuration retains the same even/odd category structure;
- whether a closed form exists for arbitrary unequal sample sizes;
- how the recommended tolerance should scale with both \(n\) and \(m\);
- whether replacing \(n\) by \(n_{\mathrm{eff}}\) is sufficient.

## Dependence and overlapping samples

Independence is only the first research case.

In general,

\[
\operatorname{Var}(\widehat p-\widehat q)
=
\operatorname{Var}(\widehat p)
+
\operatorname{Var}(\widehat q)
-
2\operatorname{Cov}(\widehat p,\widehat q).
\]

Overlapping individuals, repeated measurements, rolling windows, or nested samples make the
cross-covariance non-zero.

A production two-sample method therefore needs one of:

- a model for the dependence structure;
- a consistent covariance estimator;
- a resampling procedure that preserves the dependence;
- or an explicit restriction to independent samples.

The first implementation, if validated, should likely target independent samples only.

## Validation requirements before implementation

A public two-sample API should not be merged until all of the following are available:

1. a complete asymptotic derivation;
2. a proof or controlled approximation for the pooled reference weights;
3. a well-defined resemblance region;
4. least-favourable critical values or a justified numerical optimization;
5. finite-sample simulation calibration;
6. comparison against the classical multinomial homogeneity test;
7. explicit behavior for sparse categories;
8. documented handling, or exclusion, of dependent samples.

## Research issues

The work is split into focused research tasks:

- #44 — independent two-sample asymptotics;
- #45 — two-sample resemblance critical values;
- #46 — finite-sample simulation calibration;
- #47 — overlapping and dependent samples.

The parent research item remains #32.

## Current package policy

Until this research is complete, the package should continue to state clearly that:

- the standard PRS API is one-sample with a fixed reference distribution;
- empirical reference counts are treated conditionally as fixed probabilities;
- no existing function should be renamed or reinterpreted as a two-sample test.
