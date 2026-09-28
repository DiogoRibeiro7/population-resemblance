# Theory

## Population Resemblance Statistic

Let

[
p_0=(p_{01},ldots,p_{0B})^	op
]

be a fixed reference distribution with (p_{0j}>0), and let

[
hat p=(hat p_1,ldots,hat p_B)^	op
]

be the empirical current distribution.

The Population Resemblance Statistic is

[
operatorname{PRS}
=
sum_{j=1}^{B}
rac{(hat p_j-p_{0j})^2}{p_{0j}}.
]

The sample-size-scaled statistic is

[
Q_n=noperatorname{PRS}.
]

Under local alternatives, (Q_n) is asymptotically non-central chi-square with (B-1) degrees of freedom.

## (delta)-resemblance

The framework defines a current population (p) as (delta)-resemblant to (p_0) when

[
max_j |p_j-p_{0j}| le delta.
]

This changes the monitoring question from exact equality to whether the population shift exceeds a pre-specified tolerable amount.

The recommended automatic tolerance is

[
delta
=
cmin_j
sqrt{
rac{p_{0j}(1-p_{0j})}{n}
},
]

where (c>0) scales the acceptable shift relative to sampling variability.

## Least-favourable non-centrality

The non-centrality parameter is

[
lambda
=
nsum_{j=1}^{B}
rac{(p_j-p_{0j})^2}{p_{0j}}.
]

Because the true current probabilities are unknown, the framework uses the maximal non-centrality over the (delta)-resemblance region.

For even (B),

[
lambda_{sup}
=
ndelta^2sum_{j=1}^{B}p_{0j}^{-1}.
]

For odd (B),

[
lambda_{sup}
=
ndelta^2
left(
sum_{j=1}^{B}p_{0j}^{-1}
-
p_*^{-1}
ight),
]

where (p_*=max_j p_{0j}).

## Three decision regions

The package implements two nested resemblance hypotheses with tolerances (delta) and (Mdelta), where (M>1).

The PRS decision regions are

[
R_1={operatorname{PRS}le 	au_1},
]

[
R_2={	au_1<operatorname{PRS}le	au_2},
]

and

[
R_3={operatorname{PRS}>	au_2}.
]

The critical values are

[
	au_1
=
rac{
F^{-1}_{B-1}(alpha_2,M^2lambda_{sup})
}{n},
]

[
	au_2
=
rac{
F^{-1}_{B-1}(1-alpha_1,lambda_{sup})
}{n},
]

where (F^{-1}_{
u}(cdot,lambda)) is the non-central chi-square quantile function.

The package labels the regions as:

| Region | Package label | Interpretation |
| --- | --- | --- |
| (R_1) | `acceptable` | Continue using the model or process |
| (R_2) | `partially discrepant` | Enhanced monitoring |
| (R_3) | `fully discrepant` | Material discrepancy requiring action |

## Structural constraint

The widened tolerance must satisfy

[
Mdelta le min_j p_{0j}.
]

This prevents the resemblance region from implying invalid negative probabilities.

## Calibration

Use `evaluate_calibration()` to inspect the derived tolerance, non-centrality, critical values, and margin to the structural bound before running an assessment.

Use `sweep_calibration_parameters()` to examine sensitivity across combinations of (c), (M), (alpha_1), and (alpha_2).

## Statistical scope

The implementation follows the fixed-reference, one-sample formulation. An empirical reference sample can be converted into a fixed probability vector conditionally, but that does not make the procedure a two-sample test.

This distinction is deliberate. Reference-sample uncertainty requires a different statistical formulation.
