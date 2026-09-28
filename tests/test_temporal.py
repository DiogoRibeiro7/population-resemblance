"""Tests for temporal population monitoring."""

from __future__ import annotations

import pytest

from population_resemblance import assess_temporal_monitoring


def test_temporal_monitoring_preserves_order_and_labels() -> None:
    """Temporal results should preserve input order and explicit labels."""
    result = assess_temporal_monitoring(
        counts_by_period=[
            [50, 30, 20],
            [45, 35, 20],
            [40, 35, 25],
        ],
        reference=[0.50, 0.30, 0.20],
        labels=["2026-Q1", "2026-Q2", "2026-Q3"],
        ks_simulations=1_000,
        ks_seed=10,
    )

    assert result.labels == ("2026-Q1", "2026-Q2", "2026-Q3")
    assert len(result.points) == 3
    assert len(result.prs_statistics) == 3
    assert len(result.psi_statistics) == 3
    assert len(result.ks_statistics) == 3


def test_default_labels_are_generated() -> None:
    """Default labels should be deterministic and one-indexed."""
    result = assess_temporal_monitoring(
        counts_by_period=[
            [10, 10],
            [12, 8],
        ],
        reference=[0.5, 0.5],
        ks_simulations=500,
        ks_seed=1,
    )

    assert result.labels == ("period_1", "period_2")


def test_temporal_monitoring_is_reproducible_with_base_seed() -> None:
    """A fixed base seed should reproduce the entire temporal result."""
    counts_by_period = [
        [20, 20, 10],
        [18, 22, 10],
        [15, 25, 10],
    ]
    reference = [0.4, 0.4, 0.2]

    first = assess_temporal_monitoring(
        counts_by_period=counts_by_period,
        reference=reference,
        ks_simulations=1_000,
        ks_seed=100,
    )
    second = assess_temporal_monitoring(
        counts_by_period=counts_by_period,
        reference=reference,
        ks_simulations=1_000,
        ks_seed=100,
    )

    assert first == second


@pytest.mark.parametrize(
    "counts_by_period",
    [
        [10, 20, 30],
        [[0, 0], [1, 1]],
        [[1, -1], [2, 2]],
        [[1.0, 2.0], [3.0, 4.0]],
    ],
)
def test_invalid_temporal_counts_raise(counts_by_period: object) -> None:
    """Malformed temporal count arrays should fail explicitly."""
    with pytest.raises((TypeError, ValueError)):
        assess_temporal_monitoring(
            counts_by_period=counts_by_period,  # type: ignore[arg-type]
            reference=[0.5, 0.5],
            ks_simulations=100,
            ks_seed=1,
        )


def test_label_count_mismatch_raises() -> None:
    """Labels must align one-to-one with monitoring periods."""
    with pytest.raises(ValueError, match="labels"):
        assess_temporal_monitoring(
            counts_by_period=[[10, 10], [11, 9]],
            reference=[0.5, 0.5],
            labels=["only-one-label"],
            ks_simulations=100,
            ks_seed=1,
        )
