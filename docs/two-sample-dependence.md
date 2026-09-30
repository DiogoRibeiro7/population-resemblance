# Dependence and overlapping two-sample populations

This note addresses research issue #47.

All previous two-sample derivations assumed independent multinomial samples. That assumption
is not innocuous. In monitoring applications, baseline and current samples may overlap,
reuse the same individuals, use rolling windows, or contain repeated observations.

The source PRS paper explicitly notes this complication and therefore keeps the reference
population fixed in its published one-sample formulation. The derivation here studies what
changes when both samples are random and dependent.

## General covariance identity

Let

\[
\widehat p,\widehat q\in\mathbb R^B
\]

be empirical category-proportion vectors.

For the difference,

\[
\widehat d=\widehat p-\widehat q,
\]

the covariance is

\[
\operatorname{Var}(\widehat d)
=
\operatorname{Var}(\widehat p)
+
\operatorname{Var}(\widehat q)
-
\operatorname{Cov}(\widehat p,\widehat q)
-
\operatorname{Cov}(\widehat q,\widehat p).
\]

Under independence, the cross-covariance terms vanish. Under overlap or repeated sampling,
they generally do not.

This means that the independent-sample effective size

\[
n_{\mathrm{eff}}=\frac{nm}{n+m}
\]

is not universally valid.

## Exact overlap model

Consider a simple case in which:

- sample 1 has size \(n\);
- sample 2 has size \(m\);
- exactly \(k\) observations are shared by both samples;
- shared observations contribute the same category indicator to both samples;
- all non-shared observations are independent draws from the same categorical distribution
  \(r\).

Let

\[
\Sigma(r)=\operatorname{diag}(r)-rr^\top.
\]

Then

\[
\operatorname{Var}(\widehat p)=\frac{1}{n}\Sigma(r),
\]

\[
\operatorname{Var}(\widehat q)=\frac{1}{m}\Sigma(r),
\]

and the shared observations give

\[
\operatorname{Cov}(\widehat p,\widehat q)
=
\frac{k}{nm}\Sigma(r).
\]

Therefore

\[
\operatorname{Var}(\widehat p-\widehat q)
=
\left(
\frac{1}{n}
+
\frac{1}{m}
-
\frac{2k}{nm}
\right)
\Sigma(r).
\]

Define

\[
n_{\mathrm{eff}}^{(k)}
=
\frac{nm}{n+m-2k}.
\]

Then

\[
\sqrt{n_{\mathrm{eff}}^{(k)}}
(\widehat p-\widehat q)
\]

has the same first-order covariance \(\Sigma(r)\) as the independent construction.

### Special cases

If \(k=0\),

\[
n_{\mathrm{eff}}^{(0)}
=
\frac{nm}{n+m},
\]

recovering the independent result.

If sample 1 is fully contained in sample 2, with \(k=n<m\),

\[
n_{\mathrm{eff}}^{(n)}
=
\frac{nm}{m-n}.
\]

If \(n=m=k\), the two empirical distributions are identical and

\[
\operatorname{Var}(\widehat p-\widehat q)=0.
\]

The comparison is then degenerate and there is no non-trivial chi-square test.

## Consequence for Pearson-style scaling

In the exact-overlap model above, dependence changes only the scalar multiplying
\(\Sigma(r)\). Therefore the Pearson geometry survives after replacing the independent
effective size by

\[
n_{\mathrm{eff}}^{(k)}
=
\frac{nm}{n+m-2k}.
\]

Using the independent effective size when \(k>0\) understates the correct scaling factor.
Because the shared observations reduce the variance of the sample difference, the naive
independent statistic is systematically too small and becomes conservative under the point
null.

This correction is valid only because the cross-covariance has exactly the same
\(\Sigma(r)\) structure as the marginal covariance matrices.

## Paired repeated measurements

A more general repeated-measures setting does not have that scalar structure.

Suppose \(N\) units are observed at two occasions. Let

\[
\Pi_{ab}
=
P(Y_1=a,Y_2=b)
\]

be the \(B\times B\) joint transition-probability matrix, with marginals \(p\) and \(q\).

For one paired observation, define one-hot vectors \(U\) and \(V\). Then

\[
\operatorname{Cov}(U,V)
=
\Pi-pq^\top.
\]

For \(N\) independent pairs,

\[
\operatorname{Cov}(\widehat p,\widehat q)
=
\frac{1}{N}
(\Pi-pq^\top).
\]

Hence

\[
\operatorname{Var}(\widehat p-\widehat q)
=
\frac{1}{N}
\left[
\Sigma(p)
+
\Sigma(q)
-
(\Pi-pq^\top)
-
(\Pi^\top-qp^\top)
\right].
\]

Even when \(p=q=r\), this need not be a scalar multiple of \(\Sigma(r)\).

Therefore a single adjusted effective sample size is generally insufficient.

## General covariance-corrected quadratic form

For arbitrary dependence, define

\[
V
=
\operatorname{Var}(\widehat p-\widehat q).
\]

Because the category differences sum to zero, \(V\) is singular in the full
\(B\)-dimensional space.

Choose any full-row-rank contrast matrix

\[
C\in\mathbb R^{(B-1)\times B}
\]

whose rows span the simplex contrast space. For example,

\[
C=
\begin{bmatrix}
1&0&\cdots&0&-1\\
0&1&\cdots&0&-1\\
\vdots&&\ddots&&\vdots\\
0&0&\cdots&1&-1
\end{bmatrix}.
\]

Let

\[
z=C(\widehat p-\widehat q)
\]

and

\[
V_C=CVC^\top.
\]

If \(V_C\) is nonsingular, the Wald statistic

\[
W
=
z^\top V_C^{-1}z
\]

has an asymptotic \(\chi^2_{B-1}\) distribution under equality, provided a consistent
estimator of \(V_C\) is available.

Under local alternatives with mean contrast \(\mu_C\), the asymptotic non-centrality is

\[
\lambda
=
\mu_C^\top V_C^{-1}\mu_C.
\]

This is the correct general framework for dependent samples.

## Why this complicates resemblance calibration

The independent resemblance derivation used a diagonal Pearson weighting and a simple
closed-form least-favourable non-centrality.

With general dependence, the relevant quadratic form is

\[
d_C^\top V_C^{-1}d_C,
\]

not

\[
\sum_j \frac{d_j^2}{r_j}.
\]

The least-favourable problem therefore becomes

\[
\sup_{
\substack{
\|d\|_\infty\le\delta\\
\mathbf 1^\top d=0
}
}
d_C^\top V_C^{-1}d_C.
\]

The one-sample even/odd closed form does not generally survive because the covariance
inverse couples categories.

For a known positive-definite \(V_C\), this is a convex quadratic maximization over a
polytope. The maximum occurs at an extreme point, but its value depends on the full
dependence structure.

## Which dependence settings are tractable

### Known overlap count with identical shared observations

This case is analytically tractable.

Required information:

- \(n\);
- \(m\);
- the exact overlap count \(k\).

The scalar effective-size correction above is sufficient under the stated sampling model.

### Fully paired repeated observations

This case is tractable if the paired category transitions are observed.

The empirical joint transition table estimates \(\Pi\), which gives a direct plug-in
estimate of the cross-covariance.

A contrast-space Wald statistic can then be constructed.

### Clustered or repeated observations with unit identifiers

A sandwich covariance estimator is a natural route when contributions can be grouped by
independent clusters or individuals.

The cluster identifier must be available. Aggregate marginal counts alone are not enough.

### Rolling windows

If the windows share observations and the identities of those shared observations are known,
the exact-overlap correction may apply when the repeated records are literally identical.

If observations evolve between windows, a joint transition or cluster-level covariance
estimate is required.

### Temporal dependence without matched identities

Marginal counts from two time points are insufficient to identify the cross-covariance.

A time-series model, block bootstrap, or another dependence model is required.

## What aggregate counts cannot identify

Suppose only two marginal count vectors are supplied.

Those counts determine \(\widehat p\) and \(\widehat q\), but they do not determine

\[
\operatorname{Cov}(\widehat p,\widehat q).
\]

Many different joint dependence structures can have the same marginals.

Therefore no statistically principled generic dependent-sample correction can be inferred
from two count vectors alone.

This is an identifiability limitation, not an implementation limitation.

## Bootstrap and resampling

When individual-level or cluster-level data are available but an analytic covariance model is
undesirable, resampling may be used.

The resampling unit must preserve the dependence structure:

- paired bootstrap for matched observations;
- cluster bootstrap for grouped repeated observations;
- block bootstrap for temporally dependent sequences.

Independent resampling of the two margins would destroy the dependence and is invalid.

## Result of issue #47

The dependence problem separates into two classes.

1. **Scalar-covariance dependence**, such as exact shared observations:
   an adjusted effective sample size can recover the independent Pearson geometry.

2. **General dependence**, such as paired transitions or temporal dependence:
   the method requires a full contrast-space covariance estimator and a Wald-type quadratic
   form.

For the general case, the simple PRS least-favourable closed form is lost.

## Implication for the first two-sample implementation

The first public two-sample resemblance implementation should be restricted to
**independent samples**.

A later API could support an explicit exact-overlap model if the overlap count is known.

General paired, repeated, clustered, or temporally dependent samples should remain out of
scope until a covariance-aware resemblance calibration is separately derived and validated.

This restriction is preferable to silently applying the independent formula where its
assumptions do not hold.
