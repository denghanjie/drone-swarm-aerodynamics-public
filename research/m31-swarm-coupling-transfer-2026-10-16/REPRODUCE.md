# Reproduction and allocation boundary

Node with standard modules; Python3 with NumPy; little-endian machine. No package installation is required here. Resolve Node/Python executables from your environment. Preserve the exact published source commit and manifest digest from the source-publication/run records.

1. Verify source-manifest.json and every pinned file, including the2,176,000 extracted input bytes. Original checkpoints are public at the historical commit/release identified by inputs/index.json. To redo extraction in a separate copy, remove only that copy's generated input files and run `python3 source/extract-inputs.py ORIGINAL_DATA_ROOT`; never remove original invocation locks.
2. In a fresh separate reproduction checkout at the source commit, run `python3 source/run.py NODE_EXECUTABLE VERIFIED_SOURCE_MANIFEST_SHA256 SOURCE_COMMIT` from the package directory (paths to scripts relative to that directory). This consumes one180s invocation and saves complete/partial records.
3. After candidate completes, run `python3 source/run-review.py PYTHON_EXECUTABLE VERIFIED_SOURCE_MANIFEST_SHA256 SOURCE_COMMIT` once, capped240s. It consumes an independent review lock; no candidate JavaScript is imported by the checker.
4. Examine all admission fields before any solution. A rejected state is not a zero-force state. Source cube speed cap and sparse support cannot be bypassed.

The original experiment allocations close after their single invocations; reproducibility instructions do not authorize rerunning those allocations. A new reproduction must be distinctly labeled, retain differences and failures and use new output paths. Single durations measure invocation bookkeeping, not performance. The viewer reads saved states/results and is not a live flight solver.
