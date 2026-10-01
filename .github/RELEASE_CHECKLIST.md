# Release checklist

This checklist is used to prepare a public package release.

## Version consistency

- [x] `pyproject.toml` contains the intended release version.
- [x] `CITATION.cff` contains the same version.
- [x] `CHANGELOG.md` contains release notes for that version.
- [x] `docs/releases.md` contains matching release notes.

## Quality gates

- [x] Ruff passes.
- [x] mypy passes.
- [x] the full test suite passes on Python 3.12, 3.13, and 3.14.
- [x] documentation builds with `mkdocs build --strict`.
- [x] source-paper reproducibility smoke checks pass.
- [x] the package builds successfully.
- [x] Twine validates the built distributions.
- [x] the built wheel installs and imports in a clean virtual environment.

## Publication

- [x] the PyPI Trusted Publisher is configured for `.github/workflows/release.yml`.
- [x] the GitHub environment is named `pypi`.
- [x] a GitHub Release is created with a tag matching the package version, normally `vX.Y.Z`.
- [x] the release workflow publishes the same wheel and sdist that were validated.
- [x] the GitHub Release contains the built distribution artifacts.


## Phase 2 release readiness

- [x] package metadata migrated to PEP 621.
- [x] runtime dependencies migrated to PEP 621.
- [x] Node 24 compatible GitHub Actions majors are in use.
- [x] statistical property tests are in CI.
- [x] benchmark smoke test is in CI.
- [x] experimental two-sample API is isolated from the stable root API.
- [x] main CI is green before final release preparation.
- [x] actual publication date is added to `CITATION.cff`.
- [x] PyPI Trusted Publisher is confirmed.
- [x] GitHub Release `v0.1.0` is published by the repository owner.
