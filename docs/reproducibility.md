# Reproducing published PRS examples

The repository includes executable scripts for reproducing selected numerical results and simulation designs from the source PRS paper.

These scripts are deliberately separate from the unit-test suite. Unit tests protect correctness; the scripts provide inspectable, user-facing reproductions.

## Table 2 calibration values

Run:

```bash
poetry run python examples/reproduce_table2.py
```

The script reproduces the four published combinations already covered by the regression tests:

| Sample size | Categories | Published \(\delta\) | Published \(\tau_1\) | Published \(\tau_2\) |
| ---: | ---: | ---: | ---: | ---: |
| 50 | 5 | 0.039598 | 0.07441 | 0.25722 |
| 500 | 10 | 0.009391 | 0.03063 | 0.04890 |
| 2,000 | 10 | 0.004696 | 0.00766 | 0.01222 |
| 10,000 | 20 | 0.001526 | 0.00394 | 0.00439 |

The script raises an error if the reproduced values exceed the documented numerical tolerances.

## Selected Table 3 classifications

Run:

```bash
poetry run python examples/reproduce_table3.py
```

The script reproduces three selected small-sample examples spanning all three PRS decision regions:

- \(R_1\), PRS approximately 0.068;
- \(R_2\), PRS approximately 0.108;
- \(R_3\), PRS approximately 0.300.

These are the same published examples used in the regression tests.

## Source deviation-grid simulation

Run:

```bash
poetry run python examples/reproduce_deviation_grid.py
```

By default, the script uses:

- reference distribution \((0.2,0.2,0.2,0.2,0.2)\);
- sample size \(n=50\);
- \(c=0.7\);
- \(M=2\);
- \(\alpha_1=0.05\);
- \(\alpha_2=0.10\);
- 30 equally spaced deviation values from 0 to \((3M+2)\delta = 8\delta\);
- 10,000 Monte Carlo samples per grid point.

The repository seed is 2026. This seed is chosen for software reproducibility and is **not claimed to be a seed reported by the paper**.

For a faster smoke run:

```bash
poetry run python examples/reproduce_deviation_grid.py --simulations 200
```

For a larger numerical study, increase `--simulations`.

## Interpretation

The deviation-grid outputs are operating-characteristic probabilities for the nested PRS decision framework. They should not be relabeled as conventional power estimates.

The scripts reproduce the published methodology and selected published numerical targets; they do not extend the statistical model.
