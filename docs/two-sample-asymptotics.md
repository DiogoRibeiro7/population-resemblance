# Independent two-sample PRS asymptotics

This note completes the first mathematical research task in #44.

The result below concerns **two independent multinomial samples only**. It does not yet
define a two-sample resemblance decision procedure or critical values for nested
\(\delta\)-resemblance hypotheses.

The source PRS paper explicitly keeps \(p_0\) fixed and notes a two-sample formulation
as future research. The derivation here is therefore an extension beyond the published
one-sample method.

## Setup and assumptions

For a fixed number of categories \(B\), let

\[
X_n \sim \mathrm{Multinomial}(n,p_n),
\qquad
Y_m \sim \mathrm{Multinomial}(m,q_m),
\]

with the two samples independent. Define empirical proportions

\[
\widehat p = X_n/n,
\qquad
\widehat q = Y_m/m.
\]

Assume:

1. \(n\to\infty\) and \(m\to\infty\);
2. \(n/(n+m)\to\rho\in(0,1)\);
3. \(p_n\to r\) and \(q_m\to r\) for an interior probability vector
   \(r\), with \(r_j>0\) and \(\sum_j r_j=1\);
4. under local alternatives,

   \[
   \sqrt{n_{\mathrm{eff}}}(p_n-q_m)\to\xi,
   \qquad
   \mathbf 1^\top\xi=0,
   \]

   where

   \[
   n_{\mathrm{eff}}=\frac{nm}{n+m}.
   \]

The interior condition is needed because the Pearson weights contain reciprocals of the
limiting probabilities.

## Difference-of-proportions CLT

Write

\[
Z_{n,m}
=
\sqrt{n_{\mathrm{eff}}}
\left(
\widehat p-\widehat q
\right).
\]

Using

\[
\sqrt{n_{\mathrm{eff}}}
=
\sqrt{\frac{m}{n+m}}\sqrt n
=
\sqrt{\frac{n}{n+m}}\sqrt m,
\]

we obtain

\[
Z_{n,m}
=
\sqrt{\frac{m}{n+m}}
\sqrt n(\widehat p-p_n)
-
\sqrt{\frac{n}{n+m}}
\sqrt m(\widehat q-q_m)
+
\sqrt{n_{\mathrm{eff}}}(p_n-q_m).
\]

The multinomial central limit theorem gives

\[
\sqrt n(\widehat p-p_n)
\xrightarrow{d}
N(0,\Sigma(r)),
\]

and

\[
\sqrt m(\widehat q-q_m)
\xrightarrow{d}
N(0,\Sigma(r)),
\]

where

\[
\Sigma(r)=D(r)-rr^\top,
\qquad
D(r)=\mathrm{diag}(r).
\]

Independence of the samples and
\(m/(n+m)\to 1-\rho\), \(n/(n+m)\to\rho\) imply

\[
Z_{n,m}
\xrightarrow{d}
N(\xi,\Sigma(r)).
\]

Under exact equality, \(p_n=q_m=r\), so \(\xi=0\).

## Rank and degrees of freedom

Let

\[
u=(\sqrt{r_1},\ldots,\sqrt{r_B})^\top.
\]

Then

\[
D(r)^{-1/2}\Sigma(r)D(r)^{-1/2}
=
I-uu^\top.
\]

Because \(u^\top u=1\), the matrix

\[
P=I-uu^\top
\]

is symmetric and idempotent:

\[
P^2=P.
\]

It is the orthogonal projector onto the \((B-1)\)-dimensional subspace orthogonal to
\(u\). Hence

\[
\mathrm{rank}\{\Sigma(r)\}=B-1.
\]

This is the same loss of one degree of freedom caused by the simplex constraint in the
one-sample multinomial problem.

## Known-weight quadratic form

Suppose temporarily that the limiting common probability vector \(r\) is known. Define

\[
Q_{n,m}(r)
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(\widehat p_j-\widehat q_j)^2}{r_j}.
\]

Equivalently,

\[
Q_{n,m}(r)
=
Z_{n,m}^\top D(r)^{-1}Z_{n,m}.
\]

Let

\[
W=D(r)^{-1/2}Z,
\qquad
Z\sim N(\xi,\Sigma(r)).
\]

Then

\[
W\sim N(\mu,P),
\qquad
\mu=D(r)^{-1/2}\xi.
\]

Since \(\mathbf 1^\top\xi=0\),

\[
u^\top\mu
=
\sum_{j=1}^{B}\xi_j
=
0,
\]

so the mean vector lies in the range of \(P\). Therefore

\[
W^\top W
\sim
\chi^2_{B-1}(\lambda),
\]

with

\[
\lambda
=
\mu^\top\mu
=
\xi^\top D(r)^{-1}\xi
=
\sum_{j=1}^{B}\frac{\xi_j^2}{r_j}.
\]

Hence

\[
Q_{n,m}(r)
\xrightarrow{d}
\chi^2_{B-1}(\lambda).
\]

Under exact equality, \(\lambda=0\), giving the central
\(\chi^2_{B-1}\) limit.

For a local sequence satisfying
\(\sqrt{n_{\mathrm{eff}}}(p_n-q_m)\to\xi\), the non-centrality may also be written as

\[
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(p_{n,j}-q_{m,j})^2}{r_j}
\to
\lambda.
\]

## Unknown common probabilities and pooled plug-in

A genuine two-sample problem does not know \(r\). Define the pooled empirical
distribution

\[
\widehat r_j
=
\frac{X_{n,j}+Y_{m,j}}{n+m}
=
\frac{n}{n+m}\widehat p_j
+
\frac{m}{n+m}\widehat q_j.
\]

Under the assumptions above,

\[
\widehat r\xrightarrow{p}r.
\]

Consider the plug-in statistic

\[
Q_{n,m}(\widehat r)
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(\widehat p_j-\widehat q_j)^2}{\widehat r_j}.
\]

For each category,

\[
n_{\mathrm{eff}}
(\widehat p_j-\widehat q_j)^2
=
O_p(1),
\]

while

\[
\frac{1}{\widehat r_j}
-
\frac{1}{r_j}
=
o_p(1).
\]

Because \(B\) is fixed and every \(r_j>0\),

\[
Q_{n,m}(\widehat r)-Q_{n,m}(r)
=
o_p(1).
\]

By Slutsky's theorem,

\[
Q_{n,m}(\widehat r)
\xrightarrow{d}
\chi^2_{B-1}(\lambda).
\]

Thus the pooled plug-in preserves the same limiting distribution under both equality and
the stated local alternatives.

## Exact connection to Pearson's homogeneity statistic

The plug-in statistic is not merely analogous to the classical Pearson two-sample
homogeneity statistic: it is exactly the same statistic.

The Pearson statistic for the \(2\times B\) contingency table is

\[
X^2
=
\sum_{j=1}^{B}
\frac{(X_{n,j}-n\widehat r_j)^2}{n\widehat r_j}
+
\sum_{j=1}^{B}
\frac{(Y_{m,j}-m\widehat r_j)^2}{m\widehat r_j}.
\]

Using

\[
X_{n,j}-n\widehat r_j
=
n_{\mathrm{eff}}
(\widehat p_j-\widehat q_j)
\]

and

\[
Y_{m,j}-m\widehat r_j
=
-
n_{\mathrm{eff}}
(\widehat p_j-\widehat q_j),
\]

the two terms combine to

\[
X^2
=
n_{\mathrm{eff}}
\sum_{j=1}^{B}
\frac{(\widehat p_j-\widehat q_j)^2}{\widehat r_j}
=
Q_{n,m}(\widehat r).
\]

So the independent two-sample candidate has a classical foundation under the point null.

What remains novel, and unresolved, is the **resemblance** extension: replacing exact
equality with nested composite tolerance regions and deriving valid least-favourable
critical values.

## What #44 establishes

For independent samples and fixed \(B\), with both sample proportions converging to an
interior common limit:

- the effective sample size is \(nm/(n+m)\);
- the normalized difference has limiting covariance \(\Sigma(r)\);
- the covariance has rank \(B-1\);
- the known-weight quadratic form has a non-central \(\chi^2_{B-1}\) limit under local
  alternatives;
- pooled empirical weights are asymptotically valid;
- the pooled quadratic form is exactly Pearson's two-sample homogeneity statistic.

## What #44 does not establish

This derivation does **not** yet establish:

- a two-sample \(\delta\)-resemblance hypothesis;
- a recommended two-sample tolerance;
- a least-favourable non-centrality over that tolerance set;
- two nested decision boundaries;
- finite-sample calibration;
- validity under overlapping or dependent samples.

Those questions remain in #45–#47.
