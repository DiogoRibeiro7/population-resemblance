# Contributing

Contributions are welcome when they preserve the statistical scope and engineering quality of the project.

## Development environment

The project targets Python 3.12 and uses Poetry.

```bash
git clone https://github.com/DiogoRibeiro7/population-resemblance.git
cd population-resemblance
poetry install --with docs
```

Install the pre-commit hooks:

```bash
poetry run pre-commit install
```

## Dependency reproducibility

Use the committed `poetry.lock` for normal development installs. Dependency updates should be deliberate: update constraints when needed, regenerate the lockfile with the project Poetry version, review the dependency diff, and run `poetry check` before opening a pull request.

```bash
poetry install --with docs
poetry lock
poetry check
```

Do not regenerate the lockfile merely to refresh unrelated transitive packages.

## Before opening a pull request

Run the same checks used by CI:

```bash
poetry run ruff check .
poetry run mypy src tests
poetry run pytest --cov=population_resemblance --cov-report=term-missing
poetry run mkdocs build --strict
```

A pull request should normally include tests for new behavior and documentation when the public API, statistical interpretation, or user workflow changes.

## Statistical changes

The original PRS implementation follows Potgieter, Van Zyl, Schutte, and Lombard (2026).

Please distinguish clearly between:

- reproduction of the published PRS methodology;
- software convenience layers that do not change the statistical method;
- methodological extensions beyond the paper.

Do not present an extension as part of the original PRS framework unless it is explicitly supported by the source methodology.

Changes to formulas, critical values, calibration rules, or hypothesis definitions should include either:

- a derivation with references;
- a reproducible simulation study;
- or a regression test against a published result.

## Coding standards

New Python code should:

- use explicit type annotations;
- pass strict mypy checks;
- pass Ruff without suppressing valid findings;
- include focused tests;
- avoid unnecessary dependencies;
- preserve deterministic behavior in simulations when a seed is supplied;
- document assumptions and failure modes.

## Public API changes

The compatibility boundary is the package root export list in `population_resemblance.__all__`.

If a pull request adds, removes, or renames a root-level public symbol, it must also update the public API snapshot test and the relevant user documentation. New public exports are treated as intentional compatibility commitments.

Underscore-prefixed helpers are internal implementation details and should not be used by downstream code.

## Pull-request scope

Prefer focused pull requests. Avoid combining statistical changes, API redesigns, documentation restructuring, and unrelated cleanup in one change unless they are inseparable.

## Documentation

Documentation uses MkDocs Material and is built strictly in CI.

For public APIs, prefer docstrings that are suitable for mkdocstrings rather than duplicating signatures manually in Markdown.

## Reporting problems

For reproducible statistical or numerical issues, include:

- the input distribution or counts;
- sample size;
- calibration parameters;
- random seed, when simulations are involved;
- expected behavior;
- observed behavior.
