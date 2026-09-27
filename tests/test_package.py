"""Basic package-level tests."""

from population_resemblance import __version__


def test_version_is_defined() -> None:
    """The package exposes a semantic version string."""
    assert __version__ == "0.1.0"
