"""Tests for the delta-resemblance decision framework."""

from __future__ import annotations

import pytest

from population_resemblance import (
    DecisionRegion,
    assess_population_resemblance,
    critical_values,
    maximum_noncentrality,
    recommended_delta,
)


@pytest.mark.parametrize(
    ("sample_size", "categories", "expected_delta", "expected_lower", "expected_upper"),
    [
        (50, 5, 0.039598, 0.07441, 0.25722),
        (500, 10, 0.009391, 0.03063, 0.04890),
        (2_000, 10, 0.004696, 0.00766, 0.01222),
        (10_000, 20, 0.001526, 0.00394, 0.00439),
    ],
)
def test_reproduces_paper_table_2(
    sample_size: int,
    categories: int,
    expected_delta: float,
    expected_lower: float,
    expected_upper: float,
) -> None:
    """Recommended delta and critical values should reproduce Table 2."""
    reference = [1.0 / categories] * categories

    delta = recommended_delta(reference, sample_size, c=0.7)
    thresholds = critical_values(
        reference,
        sample_size,
        delta,
        m=2.0,
        alpha1=0.05,
        alpha2=0.10,
    )

    assert delta == pytest.approx(expected_delta, abs=5e-7)
    assert thresholds.lower == pytest.approx(expected_lower, abs=5e-6)
    assert thresholds.upper == pytest.approx(expected_upper, abs=5e-6)


def test_maximum_noncentrality_even_categories() -> None:
    """Even-category lambda_sup should include every reciprocal probability."""
    reference = [0.25, 0.25, 0.25, 0.25]

    result = maximum_noncentrality(reference, sample_size=100, delta=0.02)

    expected = 100 * 0.02**2 * sum(1.0 / value for value in reference)
    assert result == pytest.approx(expected)


def test_maximum_noncentrality_odd_categories() -> None:
    """Odd-category lambda_sup should omit the largest reference probability."""
    reference = [0.4, 0.35, 0.25]

    result = maximum_noncentrality(reference, sample_size=100, delta=0.02)

    expected = 100 * 0.02**2 * (
        sum(1.0 / value for value in reference) - 1.0 / max(reference)
    )
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    ("counts", "expected_region", "expected_statistic"),
    [
        ([6, 9, 10, 11, 14], DecisionRegion.R1, 0.068),
        ([4, 10, 11, 11, 14], DecisionRegion.R2, 0.108),
        ([2, 5, 13, 14, 16], DecisionRegion.R3, 0.300),
    ],
)
def test_reproduces_selected_table_3a_classifications(
    counts: list[int],
    expected_region: DecisionRegion,
    expected_statistic: float,
) -> None:
    """Selected small-sample examples should match the paper's PRS classifications."""
    sample_size = sum(counts)
    observed = [count / sample_size for count in counts]
    reference = [0.2] * 5

    result = assess_population_resemblance(
        observed,
        reference,
        sample_size,
        c=0.7,
        m=2.0,
        alpha1=0.05,
        alpha2=0.10,
    )

    assert result.statistic == pytest.approx(expected_statistic, abs=5e-4)
    assert result.region is expected_region


def test_explicit_delta_is_preserved() -> None:
    """A domain-specified tolerance should override automatic delta calibration."""
    result = assess_population_resemblance(
        observed=[0.48, 0.32, 0.20],
        reference=[0.50, 0.30, 0.20],
        sample_size=1_000,
        delta=0.01,
        m=2.0,
    )

    assert result.delta == pytest.approx(0.01)


@pytest.mark.parametrize(
    ("sample_size", "delta", "m"),
    [
        (0, 0.01, 2.0),
        (100, 0.0, 2.0),
        (100, 0.01, 1.0),
        (100, 0.30, 2.0),
    ],
)
def test_invalid_framework_parameters_raise(
    sample_size: int,
    delta: float,
    m: float,
) -> None:
    """Invalid framework parameters must fail explicitly."""
    with pytest.raises((TypeError, ValueError)):
        critical_values(
            reference=[0.5, 0.5],
            sample_size=sample_size,
            delta=delta,
            m=m,
        )
