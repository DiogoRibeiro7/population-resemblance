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

The paper states a grid of 30 equally spaced values from \(0\) to
\((3M+2)\delta\). For the illustrated configuration \((n,B)=(50,5)\),
\(c=0.7\), and \(M=2\), this means a stated upper endpoint of \(8\delta\).

There is an important feasibility constraint in that same simulation construction. The
perturbed probabilities are formed as \(1/B-\delta_v\) and
\(1/B+\delta_v\), so a valid multinomial distribution requires
\(\delta_v\le 1/B\). In the illustrated case, \(\delta\approx0.039598\),
hence \(8\delta\approx0.3168 > 0.2 = 1/B\). The final part of the stated grid
would therefore imply negative category probabilities.

The script preserves the paper's stated 30-point grid for inspection, computes the
feasibility boundary explicitly, and simulates only the feasible prefix rather than silently
constructing invalid probability vectors.

By default, it uses:

- reference distribution \((0.2,0.2,0.2,0.2,0.2)\);
- sample size \(n=50\);
- \(c=0.7\);
- \(M=2\);
- \(\alpha_1=0.05\);
- \(\alpha_2=0.10\);
- 10,000 Monte Carlo samples per feasible grid point.

The repository seed is 2026. This seed is chosen for software reproducibility and is
**not claimed to be a seed reported by the paper**.

For a faster smoke run:

```bash
poetry run python examples/reproduce_deviation_grid.py --simulations 200
```

For a larger numerical study, increase `--simulations`.

## Interpretation

The deviation-grid outputs are operating-characteristic probabilities for the nested PRS decision framework. They should not be relabeled as conventional power estimates.

The scripts reproduce the published methodology and selected published numerical targets; they do not extend the statistical model.
