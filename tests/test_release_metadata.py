"""Release metadata consistency checks."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _project_version() -> str:
    """Read the package version from pyproject.toml."""
    with (ROOT / "pyproject.toml").open("rb") as handle:
        data = tomllib.load(handle)
    return str(data["tool"]["poetry"]["version"])


def _citation_version() -> str:
    """Read the software version declared in CITATION.cff."""
    content = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    match = re.search(r'^version:\s*"([^"]+)"\s*$', content, flags=re.MULTILINE)
    if match is None:
        raise AssertionError("CITATION.cff does not declare a software version")
    return match.group(1)


def test_release_version_is_consistent_across_metadata() -> None:
    """Release-facing metadata should use one package version."""
    version = _project_version()
    releases = (ROOT / "docs" / "releases.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert _citation_version() == version
    assert f"## {version}" in releases
    assert f"## {version}" in changelog


def test_first_public_release_remains_pre_one_point_zero() -> None:
    """The initial public release should remain explicitly pre-1.0."""
    major = int(_project_version().split(".", maxsplit=1)[0])

    assert major == 0
