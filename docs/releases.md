# Releases

## 0.1.0

Status: release candidate.

Version 0.1.0 is being prepared for its first public publication and is not yet available
on PyPI. Use the [source installation](getting-started.md#install) in the meantime.

The initial public release establishes a tested implementation of categorical population resemblance monitoring with:

- the Population Resemblance Statistic;
- the full \(\delta\)-resemblance decision framework;
- count-based and named-category APIs;
- PSI and discrete KS benchmarks;
- simulation and operating-characteristic tooling;
- diagnostics and calibration sensitivity;
- temporal monitoring;
- reusable monitor objects;
- serialization helpers.

The complete change list is maintained in [CHANGELOG.md](https://github.com/DiogoRibeiro7/population-resemblance/blob/main/CHANGELOG.md).


## Automated PyPI publishing

Publishing is triggered only when a GitHub Release is published.

The release workflow:

1. checks that the release tag matches the package version;
2. validates project metadata and the committed lockfile;
3. builds both the source distribution and wheel;
4. validates the built files with Twine;
5. installs the built wheel in a clean virtual environment;
6. publishes to PyPI using Trusted Publishing;
7. attaches the same distribution files to the GitHub Release.

No PyPI password or API token is stored in the repository.

### PyPI Trusted Publisher setup

Before the first release, configure a Trusted Publisher for the PyPI project with:

- owner: `DiogoRibeiro7`;
- repository: `population-resemblance`;
- workflow: `release.yml`;
- environment: `pypi`.

The GitHub environment name and the PyPI publisher configuration must match.

### Release procedure

Update the package version first, merge all release preparation changes, then create and
publish a GitHub Release with a matching tag such as `v0.1.0`.

If the tag and package version differ, the workflow stops before building or publishing.
