# Release checklist

This checklist is used to prepare a public package release.

## Version consistency

- [ ] `pyproject.toml` contains the intended release version.
- [ ] `CITATION.cff` contains the same version.
- [ ] `CHANGELOG.md` contains release notes for that version.
- [ ] `docs/releases.md` contains matching release notes.

## Quality gates

- [ ] Ruff passes.
- [ ] mypy passes.
- [ ] the full test suite passes on Python 3.12, 3.13, and 3.14.
- [ ] documentation builds with `mkdocs build --strict`.
- [ ] source-paper reproducibility smoke checks pass.
- [ ] the package builds successfully.
- [ ] Twine validates the built distributions.
- [ ] the built wheel installs and imports in a clean virtual environment.

## Publication

- [ ] the PyPI Trusted Publisher is configured for `.github/workflows/release.yml`.
- [ ] the GitHub environment is named `pypi`.
- [ ] a GitHub Release is created with a tag matching the package version, normally `vX.Y.Z`.
- [ ] the release workflow publishes the same wheel and sdist that were validated.
- [ ] the GitHub Release contains the built distribution artifacts.
