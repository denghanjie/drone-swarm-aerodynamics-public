# Milestone: the tree preserves the tested answers, but has not earned a speed claim

We tested whether distant groups could be skipped without changing the aerodynamic calculation. The single registered attempt **passed all 42 cases**. The original method, the tree method and its forced-descent control produced matching numerical payloads and the declared outcomes: 34 successful inputs and eight expected refusals per method. All 15 deliberately corrupted-record controls were rejected.

The important limitation is concrete: **the existing 64-drone flock was too compact for this tree to skip anything**. All 4,032 directed pairs remained. The tree added traversal work there. This is evidence against assuming that a working tree is automatically a useful optimization.

Artificial boundary and sparse controls did exercise group omissions, and the checker independently accounted for every omitted member. Across the fixed suite H omitted 64 pair visits in 14 group omissions; positive coefficients, roots, loads and refusal behavior stayed equal to F. These fixtures are implementation checks, not a representative workload or independent statistical samples. No timing comparison or speed conclusion is made.

The next useful question is whether the same idea pays for itself on fresh larger, more spread-out swarms in the browser. The present evidence format cannot simply be used at 5,000 drones: one forced-descent candidate list alone would exceed the per-file budget. That must be resolved prospectively while preserving complete verification. See the [next-experiment decision](review/NEXT-EXPERIMENT.md).

The [Three.js inspector](viewer/index.html) shows actual saved positions and per-receiver grouping decisions across all cases and methods. It is a static record inspector, not new flight motion. The preceding [recorded flight continuation](../m31-coupled-stage-qualification-2026-10-17/viewer/index.html) remains available. UI checks exercised all 126 case/method selections and all 64 receivers of the flock regression; missing/corrupt evidence withholds the display. See [QA](viewer/QA.md).

This checkpoint establishes finite native implementation equivalence and omission checks on the pinned Node runtime. It does **not** establish browser performance, independent exact-load accuracy of these new cases, physical validity, long-flight safety, novelty or publication readiness. Coincident-position controls are artificial numerical inputs and are not physically safe flight arrangements.

Evidence: [prospective protocol](PROTOCOL.md), [raw query records](results/work.json), [independent checker](results/check.json), [supervisor](results/run-attempt.json), [review](review/RESULT-REVIEW.md), [claims](claims.json), [literature](LITERATURE.md), [restart/reproduction](RESTART.md).

Frozen source: [52d7c95e0edbe38d9c7473058e42420e939a1c51](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/52d7c95e0edbe38d9c7473058e42420e939a1c51), exact-public verified before execution. Source manifest SHA-256: `d37b0769b331b2f07812b6591a4e92727de83481a0f15f9e2b905765fc29c396`. The later result publication receipt is retained outside this frozen package under `research/publication-receipts/`.
