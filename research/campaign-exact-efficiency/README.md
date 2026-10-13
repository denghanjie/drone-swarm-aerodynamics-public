# Preliminary plan and code checkpoint

This checkpoint preserves the bounded method and early checks. Campaign measurements and the evidence-linked replay are not yet complete.

# Same-equation airflow efficiency campaign

This local CPU study compares the unchanged legacy finite-support wake implementation, the previous campaign's zero-budget implementation, and three exact implementation variants. No positive in-model contribution may be pruned. The mean wake and receiver response remain physically unvalidated.

Read PLAN.md and append-only AMENDMENTS.md before reproducing. Code needs Node24 (tested runtime recorded with results), no runtime package install. From the repository root:

- `node research/campaign-exact-efficiency/src/checks.cjs tiny`
- `node research/campaign-exact-efficiency/src/checks.cjs development`
- `node research/campaign-exact-efficiency/src/checks.cjs heldout`
- `node research/campaign-exact-efficiency/src/benchmark.cjs '{"seed":4301,"count":50,"family":"sparse","stage":"development"}'`

Timing must run serially with the declared gate/lease and timeout protocol. Do not treat arbitrary CLI selection as evidence that a frozen campaign gate passed. All new evaluator outputs own their winds arrays; reuse retains only internal scratch geometry and flags. Accepted numeric domain has finite17-entry states, quaternion norm within1e-10 of1, position components within1e6m. Tilt and near-wake domain checks still apply; nominal rotor response inputs are checked in loads().

The original eight-step research roadmap remains outputs/research-roadmap.md. Current work addresses software equivalence and measured CPU efficiency. Physical validation, browser/WebGPU coupled performance, full-mission behavior and5,000-drone feasibility remain open. A Three.js replay will link to actual retained short local3D Boids records; rendering is separate from simulation timing.

PLAN.original.sha256 and pre-evaluation.sha256 record pre-publication freeze hashes; editorial publication mappings are recorded in publication-edits.json.
