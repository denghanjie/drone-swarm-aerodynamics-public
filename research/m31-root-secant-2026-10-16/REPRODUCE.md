# Read and audit the saved endpoint diagnostic

The source manifest pins the protocol, configuration, candidate, independent checker, supervisor and inherited data/provenance. The input is referenced in its previous package rather than duplicated. No third-party physics code is imported by either calculation. Candidate uses Python standard library; independent checker additionally uses the existing NumPy runtime.

The authorized sequence is source review → frozen source publication → independent exact remote-manifest verification → sole supervised candidate → sole supervised independent saved review → tested raw-bound viewer → privacy-reviewed result publication. Source parsing is permitted before this sequence; prediction/load evaluation is not.

At the frozen source commit, the invocation interface is `python source/run.py candidate PYTHON_EXECUTABLE VERIFIED_SOURCE_MANIFEST_SHA PUBLISHED_SOURCE_COMMIT`, run from this package. The saved-only checker uses `review` with the same arguments. These commands consume permanent locks. They are instructions for the already allocated run, not permission to rerun a closed experiment. An independent future reproduction needs a separately named, prospectively recorded allocation and must retain these original results unchanged.

Scientific output is `results/prediction-trace.jsonl` (causal forecasts retained before scoring), `events.jsonl` (all paired per-event/per-drone loads/errors), `controls.json` (five fixed boundary fixtures) and `summary.json`. `independent-review.json` and both `*-run.json` files distinguish evidence integrity, source ancestry, resource observations and scientific qualification. Invalid finite forecasts are retained and tagged; their load errors are diagnostics outside the admitted root domain.

Publication receipts outside the package verify exact remote manifests and local committed pins. They do not claim to download every remote data file. No proprietary user records, private absolute paths, authentication data or original paper PDFs belong in this package. The later Three.js viewer uses saved poses and error arrays only, never a new scientific solver.
