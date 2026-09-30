# Sparse-category policy for experimental two-sample resemblance

This note implements Phase 2 issue #55.

The completed two-sample research showed that sparse categories are the main practical
failure mode for the plug-in resemblance candidate. The policy below is intended to be
mechanically enforceable by a future **experimental** independent two-sample API.

It is deliberately conservative. The package must fail loudly rather than silently smooth,
drop, or merge categories.

## Policy summary

A two-sample resemblance assessment is eligible for asymptotic classification only when
all of the following conditions hold:

1. every pooled empirical category probability is strictly positive;
2. the minimum pooled expected count in **each** sample is at least 5;
3. the widened resemblance tolerance satisfies the probability-domain feasibility bound;
4. both samples contain at least two categories after any user-performed preprocessing.

If any condition fails, the experimental API should reject the assessment rather than
return an \(R_1/R_2/R_3\) classification.

## Pooled empirical probabilities

For count vectors \(x\) and \(y\), with sample sizes

\[
n=\sum_j x_j,
\qquad
m=\sum_j y_j,
\]

define

\[
\widehat r_j
=
\frac{x_j+y_j}{n+m}.
\]

The future experimental statistic uses \(\widehat r_j\) in the Pearson denominator.
Therefore

\[
\widehat r_j=0
\]

is not merely undesirable: it makes the statistic and the plug-in calibration undefined.

### Rule 1 — zero pooled cells are unsupported

If

\[
x_j+y_j=0
\]

for any category \(j\), the procedure must raise an error.

The implementation must not:

- add epsilon values;
- apply Laplace smoothing;
- silently drop the category;
- silently merge it with another category.

If categories need to be combined, that must be a user decision made **before** the
statistical procedure is called.

## Expected-count diagnostic

Under the pooled point-null model, the expected counts are

\[
E[X_j]=n\widehat r_j,
\qquad
E[Y_j]=m\widehat r_j.
\]

Define

\[
e_{\min}
=
\min_j
\left\{
n\widehat r_j,
m\widehat r_j
\right\}
=
\min(n,m)\min_j \widehat r_j.
\]

### Rule 2 — require \(e_{\min}\ge 5\)

The experimental API should require

\[
e_{\min}\ge5.
\]

This threshold is a conservative asymptotic diagnostic, not a theorem guaranteeing exact
PRS resemblance calibration.

Its purpose is operational:

- below this level, zero pooled cells become common;
- the finite-sample study in #46 showed visibly conservative boundary behavior for sparse
  distributions;
- the plug-in tolerance and least-favourable calibration become unstable when the smallest
  empirical pooled probability is driven by one or two observations.

The threshold should therefore be described as a **support condition for the experimental
asymptotic implementation**, not as a universal law of categorical testing.

## Simulation evidence

The repository research simulations show the qualitative transition clearly.

For equal sample sizes and five categories:

| Smallest true category probability | Sample size per group | Smallest expected count | Observed behavior |
| ---: | ---: | ---: | --- |
| 0.20 | 50 | 10 | stable |
| 0.08 | 50 | 4 | mostly stable but more conservative |
| 0.02 | 50 | 1 | frequent invalid/filtered simulations |
| 0.02 | 100 | 2 | substantial improvement, still fragile |
| 0.02 | 200 | 4 | mostly stable |
| 0.02 | 500 | 10 | stable |

This does not prove that 5 is an optimal threshold. It supports using 5 as a simple,
conservative gate for the first experimental implementation.

## Structural feasibility is a different condition

Expected-count adequacy and resemblance feasibility are not the same thing.

For independent samples, let

\[
\rho=\frac{n}{n+m}.
\]

The full symmetric resemblance region requires

\[
M\delta
\le
\frac{
\min_j\min(\widehat r_j,1-\widehat r_j)
}{
\max(\rho,1-\rho)
}.
\]

### Rule 3 — enforce structural feasibility separately

Passing the expected-count threshold does **not** imply this probability-domain condition.

Likewise, satisfying the structural bound does **not** imply adequate asymptotic
approximation.

Both checks are required.

## User-performed category aggregation

Category aggregation may be statistically sensible when categories are substantively
exchangeable or were defined too finely.

The library should allow such preprocessing, but it must happen outside the resemblance
function.

The future API documentation should state:

> If sparse categories are merged, the grouping must be defined by the analyst before the
> test is run and must reflect a defensible domain-level category definition. The package
> does not choose or optimize category mergers.

This avoids data-dependent category engineering designed to force a desired classification.

## Proposed mechanical validation

A future experimental API can enforce the policy with quantities available from two count
vectors.

Given counts \(x,y\):

1. validate non-negative integer counts and matching category length;
2. require positive total size in both samples;
3. compute pooled counts \(x+y\);
4. reject if any pooled count is zero;
5. compute \(\widehat r\);
6. compute
   \[
   e_{\min}=\min(n,m)\min_j\widehat r_j;
   \]
7. reject if \(e_{\min}<5\);
8. compute the plug-in \(\delta\);
9. reject if the widened tolerance violates the probability-domain bound.

Suggested diagnostics should include:

- minimum pooled probability;
- minimum expected count;
- zero-cell count;
- structural-feasibility margin;
- a machine-readable reason when validation fails.

## Proposed error semantics

The future experimental implementation should distinguish causes rather than raise a generic
numerical error.

Suggested errors or diagnostic codes:

- `zero_pooled_category`
- `insufficient_expected_count`
- `structural_probability_bound`
- `invalid_counts`
- `dependent_samples_unsupported`

The exact Python exception hierarchy can be decided in #56.

## What the policy does not claim

The \(e_{\min}\ge5\) rule does not guarantee:

- exact finite-sample Type I error;
- uniform validity over every categorical distribution;
- accurate calibration under dependence;
- good behavior when the number of categories grows with sample size.

It is a conservative eligibility rule for the first independent-sample experimental API.

## Decision for #55

The first experimental two-sample resemblance implementation should:

- reject zero pooled categories;
- require minimum pooled expected count at least 5 in both samples;
- enforce the structural resemblance feasibility bound independently;
- never smooth, drop, or merge categories automatically;
- remain restricted to independent samples.

These conditions are intentionally stricter than the underlying formulas require. The goal
is to expose an experimental method only in the region where the completed simulation work
provides reasonable empirical support.
