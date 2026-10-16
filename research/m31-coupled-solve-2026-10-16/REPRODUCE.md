# Reproduction and record integrity

Use Node22+ and nonoptimized Python3.11+ (stdlib only). No package installation is required for the scientific calculation. The exact runtime versions will appear in saved evidence. The independent checker uses Decimal80 and independent vector geometry.

After checking out the published source commit, verify source-manifest.json and independently verify that commit/manifest on GitHub. From repository root, with your Node executable, manifest SHA256 and source commit:

```sh
python3 research/m31-coupled-solve-2026-10-16/source/run.py /path/to/node MANIFEST_SHA256 SOURCE_COMMIT
python3 research/m31-coupled-solve-2026-10-16/source/run-review.py /path/to/python3 MANIFEST_SHA256 SOURCE_COMMIT
```

Run in a fresh checkout without results; both runners create exclusive locks and output files. Do not remove original locks or overwrite evidence to reproduce. The authorized campaign uses exactly one invocation of each runner. Source commit/hash checks happen before consumption. Launch exceptions, timeouts and partial files are retained where normal process/filesystem operation permits. External termination or unwritable storage can prevent final record writing. Source SHA/commit verification is explicitly rejected under optimized Python.

Scientific output is results/evidence.json; supervisory records are run.json and review-run.json, with separate pipes. CandidatePass covers preliminary structural checks only. Full development qualification requires independent-review.json passed=true with all fixtures covered. All quantities and counts derive from saved records; elapsed supervisor/reviewer durations are bookkeeping, not repeated performance benchmarks.

The eventual viewer loads those saved files with byte-count/SHA256 verification; it does not run the scientific solver. Three.js and OrbitControls use existing repository-vendored files. Keep the existing local server at port8876; open research/m31-coupled-solve-2026-10-16/viewer/ after result publication.
