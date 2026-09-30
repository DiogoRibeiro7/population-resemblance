# Development

## Environment

The project supports Python 3.12, 3.13, and 3.14. Python 3.12 is the canonical version for Ruff, mypy, and documentation validation, while the test suite also runs against every supported Python version.

Install **Poetry 2.5.x**; **2.5.1** matches CI. With
[pipx installed](https://pipx.pypa.io/stable/installation/):

```bash
pipx install poetry==2.5.1
```

From a source checkout, install the dependencies in the committed lockfile:

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

A strict documentation build runs in CI to check internal documentation links, navigation,
and mkdocstrings output. It does not verify the availability of external websites.

CI also executes the actual Python fences in `README.md` and every Markdown page under
`docs/`, using `tests/test_documentation.py`. Run just those checks with:

```bash
poetry run pytest tests/test_documentation.py -v
```

Use top-level triple-backtick fences labelled `python` for runnable examples. Blocks
execute in page order with a shared namespace within each page and a fresh namespace for
each new page, so explicitly import anything a page needs. If a `text` fence immediately
follows a Python fence, separated only by whitespace, its contents are checked against
standard output. Format numerical output to a stable precision and set random seeds
when examples use simulation. Shell installation commands are not executed by this check.

The documentation deployment workflow runs these example checks before building. It also
rebuilds on `src/**` changes, so docstring updates reach the published API reference, and
on lockfile changes, so the site uses the current documentation dependencies.

## Scientific changes

Changes that extend beyond the published PRS formulation should be clearly identified as extensions rather than silently presented as part of the original method.
