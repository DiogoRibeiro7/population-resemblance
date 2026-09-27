# population-resemblance

Statistically principled monitoring of categorical population and distribution shifts.

This project implements and extends the **Population Resemblance Statistic (PRS)** framework introduced by Potgieter, Van Zyl, Schutte, and Lombard in *Annals of Operations Research* (2026).

The package is intended as a general-purpose statistical toolkit for monitoring whether an observed categorical distribution remains sufficiently close to a reference distribution. Banking and credit-risk monitoring are important applications, but the core methodology is domain-independent and can be used wherever categorical population drift matters.

## Planned scope

- Population Resemblance Statistic (PRS)
- \(\delta\)-resemblance and sample-size-aware decision thresholds
- green / amber / red monitoring decisions
- comparison with Population Stability Index (PSI) and related discrepancy measures
- simulation and calibration utilities
- extensions for two-sample monitoring
- cost-sensitive and weighted resemblance
- temporal population monitoring

## Reference

C. J. Potgieter, C. Van Zyl, W. D. Schutte, and F. Lombard,  
**The population resemblance statistic: a chi-square measure of fit for banking**,  
*Annals of Operations Research* 361, 413–435 (2026).  
https://doi.org/10.1007/s10479-025-07024-6

## Status

Early development.
