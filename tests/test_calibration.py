"""Tests for PRS calibration diagnostics."""

from __future__ import annotations

import pytest

from population_resemblance import evaluate_calibration


def test_default_calibration_is_feasible() -> None:
    """A standard balanced configuration should satisfy the framework constraints."""
    result = evaluate_calibration(
        reference=[0.2] * 5,
        sample_size=50,
    )

    assert result.feasible
    assert result.margin_to_probability_bound > 0.0
    assert result.lower_critical_value <= result.upper_critical_value


def test_calibration_matches_paper_table_2_first_row() -> None:
    """Derived values should reproduce the paper's first Table 2 configuration."""
    result = evaluate_calibration(
        reference=[0.2] * 5,
        sample_size=50,
        c=0.7,
        m=2.0,
        alpha1=0.05,
        alpha2=0.10,
    )

    assert result.delta == pytest.approx(0.039598, abs=5e-7)
    assert result.lower_critical_value == pytest.approx(0.07441, abs=5e-6)
    assert result.upper_critical_value == pytest.approx(0.25722, abs=5e-6)


def test_explicit_delta_is_respected() -> None:
    """Domain-specific delta should be reflected in all derived quantities."""
    result = evaluate_calibration(
        reference=[0.5, 0.3, 0.2],
        sample_size=1_000,
        delta=0.01,
        m=1.5,
    )

    assert result.delta == pytest.approx(0.01)
    assert result.widened_delta == pytest.approx(0.015)
    assert result.minimum_reference_probability == pytest.approx(0.2)
    assert result.margin_to_probability_bound == pytest.approx(0.185)


def test_infeasible_probability_bound_raises() -> None:
    """The framework should reject M-delta values exceeding the smallest p0."""
    with pytest.raises(ValueError):
        evaluate_calibration(
            reference=[0.8, 0.1, 0.1],
            sample_size=100,
            delta=0.06,
            m=2.0,
        )


def test_invalid_reference_raises() -> None:
    """Malformed references should fail explicitly."""
    with pytest.raises(ValueError):
        evaluate_calibration(
            reference=[0.5, 0.4],
            sample_size=100,
        )
