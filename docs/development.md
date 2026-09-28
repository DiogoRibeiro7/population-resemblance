# Development

## Environment

The project targets Python 3.12 and uses Poetry.

```bash
poetry install --with docs
```

## Quality checks

Run the full local quality suite:

```bash
poetry run ruff check .
poetry run mypy src tests
poetry run pytest --cov=population_resemblance --cov-report=term-missing
poetry run mkdocs build --strict
```

## Pull-request workflow

Development should happen on focused branches and be merged through pull requests into `main`.

Keep changes small enough that statistical behavior, tests, and documentation can be reviewed together.

## Testing principles

New statistical functionality should normally include:

- direct numerical checks against the defining formula;
- validation of invalid or structurally impossible inputs;
- deterministic simulation tests when randomness is involved;
- regression checks against published examples when available;
- parity checks when introducing convenience wrappers around existing methods.

## Documentation

Serve the documentation locally with:

```bash
poetry run mkdocs serve
```

A strict documentation build runs in CI. Broken links, invalid navigation, and mkdocstrings failures should therefore be caught before merge.

## Scientific changes

Changes that extend beyond the published PRS formulation should be clearly identified as extensions rather than silently presented as part of the original method.
