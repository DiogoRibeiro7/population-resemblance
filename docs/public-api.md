# Public API and compatibility policy

This page defines which parts of `population-resemblance` are supported for downstream use and how compatibility changes are handled.

## Supported public API

The canonical public API is the set of names exported from the package root:

```python
import population_resemblance
print(population_resemblance.__all__)
```

Users should prefer imports such as:

```python
from population_resemblance import assess_population_counts
from population_resemblance import PopulationMonitor
```

Names listed in `population_resemblance.__all__` are intentional public interfaces. They include functions, result objects, monitor classes, diagnostics, simulation helpers, and serialization utilities.

## Internal implementation details

Names beginning with an underscore are internal unless explicitly documented otherwise.

Examples include validation and conversion helpers such as:

- `_as_probability_vector`;
- `_as_count_vector`;
- private validation functions used by the decision framework.

Internal helpers may change without a deprecation period. Downstream code should not import them.

Submodule paths are documented for API reference, but the package-root imports are the compatibility boundary. Code that imports implementation details directly from submodules accepts a higher risk of change.

## Versioning before 1.0

The package currently uses a pre-1.0 version.

Before 1.0:

- patch releases should remain backward compatible except when correcting behavior that is demonstrably incorrect or unsafe;
- minor releases may contain breaking API changes;
- breaking changes should still be documented clearly and should use deprecation periods when practical;
- statistical interpretation changes require especially explicit release notes.

A pre-1.0 version does not mean the API is arbitrary. Public changes should remain deliberate and reviewable.

## Versioning from 1.0 onward

After 1.0, the project will follow semantic-versioning expectations:

- patch: backward-compatible fixes;
- minor: backward-compatible functionality;
- major: incompatible public API changes.

Changes in numerical output caused by a documented statistical bug fix are treated separately from ordinary API compatibility and must be explained in release notes.

## Deprecation policy

When a public function, class, parameter, or behavior is replaced:

1. the old interface should normally remain available for at least one minor release;
2. the deprecated path should emit `DeprecationWarning`;
3. documentation should identify the replacement;
4. release notes should state the planned removal version when known;
5. removal should occur only in a version where breaking changes are permitted.

A deprecation period may be skipped for security issues, clearly incorrect behavior, or interfaces that were never part of the documented public API.

## Adding new public APIs

A new root-level export is a compatibility commitment.

Pull requests that add names to `population_resemblance.__all__` should include:

- tests;
- user-facing documentation;
- a clear statistical scope when relevant;
- an intentional update to the public API snapshot test.

This prevents convenience helpers or implementation artifacts from becoming public accidentally.

## Compatibility test

The test suite contains a snapshot of the expected root-level API. CI fails if a name is added to or removed from `__all__` without updating that snapshot.

The snapshot does not prevent API evolution. It makes API evolution explicit.
