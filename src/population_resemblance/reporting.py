"""Unified monitoring report across PRS, PSI, and discrete KS benchmarks."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from population_resemblance.counts import assess_population_counts, counts_to_proportions
from population_resemblance.ks import DiscreteKSTestResult, discrete_ks_test_counts
from population_resemblance.psi import lewis_psi_status, population_stability_index
from population_resemblance.result import PopulationResemblanceResult


@dataclass(frozen=True, slots=True)
class PSIAssessment:
    """Population Stability Index result and Lewis benchmark status."""

    statistic: float
    status: str


@dataclass(frozen=True, slots=True)
class PopulationMonitoringReport:
    """Unified monitoring results for one observed categorical sample."""

    prs: PopulationResemblanceResult
    psi: PSIAssessment
    ks: DiscreteKSTestResult

    @property
    def statuses(self) -> tuple[str, str, str]:
        """Return PRS, PSI, and KS statuses in a compact tuple."""
        return (self.prs.label, self.psi.status, self.ks.status)


def assess_population_monitoring(
    counts: Sequence[int] | npt.NDArray[np.integer],
    reference: Sequence[float] | npt.NDArray[np.floating],
    *,
    delta: float | None = None,
    c: float = 0.7,
    m: float = 2.0,
    alpha1: float = 0.05,
    alpha2: float = 0.10,
    ks_simulations: int = 10_000,
    ks_seed: int | None = None,
) -> PopulationMonitoringReport:
    """Assess one observed sample with PRS, PSI, and discrete KS.

    PRS is the primary tolerance-based framework. PSI and discrete KS are
    returned as descriptive benchmarks because their decision rules differ
    from the PRS composite-null formulation.

    Parameters
    ----------
    counts:
        Observed category counts.
    reference:
        Fixed reference probability distribution.
    delta:
        Optional explicit PRS tolerance.
    c:
        Multiplier used for automatic PRS tolerance calibration.
    m:
        Wider PRS resemblance multiplier.
    alpha1:
        Upper PRS error-control parameter.
    alpha2:
        Lower PRS error-control parameter.
    ks_simulations:
        Monte Carlo sample count used to calibrate the discrete KS p-value.
    ks_seed:
        Optional random seed used for the discrete KS calibration.

    Returns
    -------
    PopulationMonitoringReport
        Unified PRS, PSI, and discrete KS results.
    """
    prs_result = assess_population_counts(
        counts=counts,
        reference=reference,
        delta=delta,
        c=c,
        m=m,
        alpha1=alpha1,
        alpha2=alpha2,
    )

    observed = counts_to_proportions(counts)
    psi_statistic = population_stability_index(observed=observed, reference=reference)
    psi_result = PSIAssessment(
        statistic=psi_statistic,
        status=lewis_psi_status(psi_statistic),
    )

    ks_result = discrete_ks_test_counts(
        counts=counts,
        reference=reference,
        simulations=ks_simulations,
        seed=ks_seed,
    )

    return PopulationMonitoringReport(
        prs=prs_result,
        psi=psi_result,
        ks=ks_result,
    )
