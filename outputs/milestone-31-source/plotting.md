# Reproducing the passage figure

`plot.py` reads the six saved, matched, primary records: baseline and candidate for 1,000/wide/2001, 1,000/narrow/2002 and 5,000/wide/2001. All six files must exist. It uses exact finish-line crossing times, draws cumulative step curves and ends each curve at the actual recorded stop. It does not fit a curve, extrapolate a stopped run or average different cases.

The figure is descriptive. Each panel is one matched starting case. Comparisons across panels do not isolate doorway width, count or seed effects. Numerical refinements and the development case are reported separately.

Outputs are `milestone-31-passage.png`, `milestone-31-passage.pdf` and `milestone-31-figure-sources.json`. The latter retains every plotted crossing time and a hash of the plotted numerical input. Rendering uses Matplotlib's noninteractive Agg backend; it does not change the simulation.

Use Python 3.12 and the versions in `plotting-requirements.txt`. A separate virtual environment is sufficient:

```sh
python3.12 -m venv work/plot-env
work/plot-env/bin/python -m pip install -r outputs/milestone-31-source/plotting-requirements.txt
work/plot-env/bin/python outputs/milestone-31-source/plot.py
```

For a complete isolated rerun, invoke `research-reproduce.py --stage 31` with that environment's Python and an available Node executable supplied through `--node`. The helper checks for Matplotlib before starting the long numerical calculation, then regenerates the figure before its report. Add `--skip-figures` for numerical-only reproduction; copied figures are removed so they cannot be mistaken for newly generated output.

This workspace uses a local package target at `work/plotting-deps` with the bundled Python, rather than changing global packages. The standalone figure command is:

```sh
PYTHONPATH=./work/plotting-deps python3 outputs/milestone-31-source/plot.py
```

Use that absolute `PYTHONPATH` for full reproduction too, because child commands execute inside the isolated copy. A complete second numerical campaign was not run merely to verify the plot.
