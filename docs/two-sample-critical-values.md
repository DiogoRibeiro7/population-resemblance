# Two-sample resemblance critical values

This note addresses research issue #45.

The previous derivation established that, for two independent multinomial samples, the
pooled Pearson quadratic form is asymptotically non-central chi-square under local
alternatives. The question here is whether the one-sample resemblance critical-value
construction survives by simply replacing the one-sample size \(n\) with

\[
n_{\mathrm{eff}}=\frac{nm}{n+m}.
\]

The answer is **only conditionally**. If the limiting pooled probability vector is treated as
fixed, the one-sample geometry carries over. In a genuine symmetric two-sample problem,
however, that pooled vector is itself an unknown nuisance parameter, so a universal closed
form does not follow from the one-sample result.

## Setup

Let the population proportions be \(p\) and \(q\), with independent sample sizes \(n\)
and \(m\). Define

\[
\rho=\frac{n}{n+m},
\qquad
n_{\mathrm{eff}}=\frac{nm}{n+m},
\]

and the pooled population centre

\[
r=\rho p+(1-\rho)q.
\]

Let

\[
d=p-q.
\]

Then

\[
p=r+(1-\rho)d,
\qquad
q=r-\rho d.
\]

Under local alternatives, the two-sample Pearson-type statistic has candidate
non-centrality

\[
\lambda
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{d_j^2}{r_j},
\]

with

\[
\sum_{j=1}^{B}d_j=0.
\]

## Conditional resemblance region

Suppose first that \(r\) is fixed and known.

Define the two-sample resemblance set

\[
\mathcal D(\delta)
=
\left\{
d:
\max_j |d_j|\le\delta,
\quad
\mathbf 1^\top d=0
\right\}.
\]

If the full symmetric perturbation set is compatible with valid probability vectors
\(p\) and \(q\), maximizing \(\lambda\) over \(\mathcal D(\delta)\) is exactly the
same weighted convex optimization as in the one-sample PRS framework, with
\(n_{\mathrm{eff}}\) replacing \(n\).

Hence, conditionally on fixed \(r\),

\[
\lambda_{\sup}(r,\delta)
=
\begin{cases}
n_{\mathrm{eff}}\delta^2
\displaystyle\sum_{j=1}^{B}r_j^{-1},
& B \text{ even},\\[1em]
n_{\mathrm{eff}}\delta^2
\left(
\displaystyle\sum_{j=1}^{B}r_j^{-1}
-r_*^{-1}
\right),
& B \text{ odd},
\end{cases}
\]

where

\[
r_*=\max_j r_j.
\]

So the even/odd extreme-point geometry is retained **for a fixed centre**.

## Probability-domain constraint

The two samples must both remain valid probability vectors.

Because

\[
p_j=r_j+(1-\rho)d_j
\]

and

\[
q_j=r_j-\rho d_j,
\]

allowing every coordinate perturbation in \([-\delta,\delta]\) requires

\[
\delta
\le
\min_j
\left\{
\frac{r_j}{1-\rho},
\frac{1-r_j}{1-\rho},
\frac{r_j}{\rho},
\frac{1-r_j}{\rho}
\right\}.
\]

Equivalently,

\[
\delta
\le
\frac{
\min_j\min(r_j,1-r_j)
}{
\max(\rho,1-\rho)
}.
\]

For the wider resemblance region, replace \(\delta\) by \(M\delta\).

This is stricter than merely requiring \(|p_j-q_j|\le\delta\): it guarantees that the
entire symmetric perturbation set around the fixed pooled centre remains inside the
probability simplex for both samples.

## Conditional critical values

For the scaled statistic

\[
Q_{n,m}
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(\widehat p_j-\widehat q_j)^2}{r_j},
\]

a direct conditional analogue of the one-sample nested framework would use

\[
c_1
=
F^{-1}_{B-1}
\left(
\alpha_2,
M^2\lambda_{\sup}(r,\delta)
\right)
\]

and

\[
c_2
=
F^{-1}_{B-1}
\left(
1-\alpha_1,
\lambda_{\sup}(r,\delta)
\right).
\]

The corresponding regions would be

\[
R_1=\{Q_{n,m}\le c_1\},
\]

\[
R_2=\{c_1<Q_{n,m}\le c_2\},
\]

and

\[
R_3=\{Q_{n,m}>c_2\}.
\]

If instead an unscaled discrepancy

\[
D_{n,m}
=
\sum_{j=1}^{B}
\frac{(\widehat p_j-\widehat q_j)^2}{r_j}
\]

is reported, the thresholds are \(c_1/n_{\mathrm{eff}}\) and
\(c_2/n_{\mathrm{eff}}\).

This conditional construction is mathematically parallel to the one-sample method.

## Why the genuine two-sample problem is harder

A genuine two-sample test does not know \(r\).

The natural practical statistic uses the pooled empirical distribution

\[
\widehat r_j
=
\frac{n\widehat p_j+m\widehat q_j}{n+m}.
\]

For the point-null problem, replacing \(r\) by \(\widehat r\) is asymptotically valid
and yields Pearson's homogeneity statistic.

For resemblance testing, however, the critical values also depend on \(r\) through

\[
\lambda_{\sup}(r,\delta).
\]

Plugging \(\widehat r\) into the **critical-value calibration** is a stronger step than
plugging it into the test statistic.

Pointwise consistency suggests that

\[
\lambda_{\sup}(\widehat r,\delta)
\xrightarrow{p}
\lambda_{\sup}(r,\delta)
\]

for fixed interior \(r\), but that alone does not establish uniform Type I error control over
the composite two-sample resemblance null.

The nuisance parameter therefore enters twice:

1. in the quadratic-form weights;
2. in the least-favourable calibration itself.

## Why replacing n by n_eff is not enough

The substitution

\[
n\mapsto n_{\mathrm{eff}}
\]

correctly reproduces the independent two-sample covariance scaling.

But the one-sample PRS has a fixed reference vector \(p_0\). In a symmetric two-sample
problem there is no fixed analogue unless one is introduced by design.

Therefore the recipe

> replace \(n\) by \(n_{\mathrm{eff}}\) and \(p_0\) by \(\widehat r\)

is a plausible plug-in procedure, but it is **not yet a proven resemblance test with uniform
error guarantees**.

## Recommended tolerance: candidate only

A natural two-sample analogue of the one-sample recommendation is

\[
\delta
=
c\min_j
\sqrt{
\frac{r_j(1-r_j)}{n_{\mathrm{eff}}}
}.
\]

With unknown \(r\), the operational version would replace \(r\) by
\(\widehat r\).

This has an appealing interpretation: it scales tolerance by the standard error of the
difference between two independent proportions.

However, a data-dependent \(\delta\) changes the null region itself. Its calibration must
therefore be studied rather than assumed.

## Result of issue #45

The simple extension succeeds only under a **fixed pooled centre**:

- \(n_{\mathrm{eff}}\) replaces \(n\);
- the one-sample even/odd least-favourable geometry is preserved;
- conditional critical values follow from the same non-central chi-square quantiles;
- the probability-domain constraint depends on \(\rho\) as well as \(r\).

For the genuine symmetric two-sample problem, the pooled centre is unknown. The simple
closed form is therefore conditional on a nuisance parameter, and plugging in
\(\widehat r\) requires separate validation.

## Consequence for implementation

No public two-sample resemblance API should be added yet.

The next required step is #46: simulate the plug-in candidate across sample-size ratios,
reference distributions, and resemblance boundaries to determine whether the nominal
decision probabilities are preserved in finite samples and whether plug-in calibration is
stable enough to justify a practical method.
