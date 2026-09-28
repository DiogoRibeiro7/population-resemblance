"""Tests for package distribution metadata."""

from __future__ import annotations

from importlib.resources import files


def test_pep561_marker_is_available() -> None:
    """The installed package should expose its PEP 561 typing marker."""
    marker = files("population_resemblance").joinpath("py.typed")

    assert marker.is_file()
