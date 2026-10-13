# Same-equation airflow efficiency campaign

This local CPU study compares the unchanged legacy finite-support wake implementation, the previous campaign's zero-budget implementation, and three exact implementation variants. No positive in-model contribution may be pruned. The mean wake and receiver response remain physically unvalidated.

Read PLAN.md and append-only AMENDMENTS.md before reproducing. Code needs Node 24 (tested runtime recorded with results), no runtime package install. From the repository root:

- `node research/campaign-exact-efficiency/src/checks.cjs tiny`
- `node research/campaign-exact-efficiency/src/checks.cjs development`
- `node research/campaign-exact-efficiency/src/checks.cjs heldout`
- `node research/campaign-exact-efficiency/src/benchmark.cjs '{"seed":4301,"count":50,"family":"sparse","stage":"development"}'`

Timing must run serially with the declared exclusive serial measurement window and timeout protocol. Do not treat arbitrary CLI selection as evidence that a frozen campaign gate passed. All new evaluator outputs own their winds arrays; reuse retains only internal scratch geometry and flags. Accepted numeric domain has finite 17-entry states, quaternion norm within 1e-10 of 1, position components within 1e6 m. Tilt and near-wake domain checks still apply; nominal rotor response inputs are checked in loads().

The original eight-step research roadmap remains outputs/research-roadmap.md. Current work addresses software equivalence and measured CPU efficiency. Physical validation, browser/WebGPU coupled performance, full-mission behavior and 5,000-drone feasibility remain open. A Three.js replay will link to actual retained short local 3D Boids records; rendering is separate from simulation timing.


## Replay and portable evidence

The repository demo is [demo/index.html](demo/index.html). Serve the campaign folder with `python -m http.server 8000 --bind 127.0.0.1 --directory research/campaign-exact-efficiency`, then open `http://127.0.0.1:8000/demo/`. This is a recorded-state Three.js viewer, not live physics or a browser throughput benchmark.

A self-contained offline HTML is delivered separately as a private attachment. Rebuild it with `python research/campaign-exact-efficiency/src/build-standalone.py`; it needs no build dependency and bundles local module sources, actual Boids records, report/provenance and the full Three.js MIT notice. The generated HTML is deliberately excluded from Git to avoid duplicating the embedded records. Browser rendered QA was blocked by a verified socket permission denial; see results/viewer-qa/browser-check.json and the independent static audit.

The [report](REPORT.md) separates primary previous-zero comparisons from the independent legacy comparator. It preserves mixed family/seed outcomes and the stop before N=500. Source provenance maps field timing, pre-A5 recorded Boids and A5 whole-pipeline timing to their exact runner versions. The historical pre-A5 recording runner is preserved in source-versions/boids-pre-A5.cjs.txt; its simulated equations and recorded poses are unchanged by the later terminal-checksum harness addition.
