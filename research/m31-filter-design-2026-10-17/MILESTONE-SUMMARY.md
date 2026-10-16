# The shortcut passed its finite correctness test; speed is still unknown

All 108 fixed test cases qualified, and the independent checker detected all 16 deliberate corruption controls. The useful result is a small, verified step: the new filter can prove some interactions are exactly zero under the declared model, while sending difficult cases through the unchanged exact calculation.

The important limitation is coverage. Of 19 zero interactions in this deliberately difficult test set, the filter handled only five directly. The other 14 still needed exact fallback. This records conservative fallback behavior in the selected cases; it does not estimate typical swarm performance or isolate the cause of each fallback.

## What we tested

The frozen suite contained 72 arithmetic/adjacent-word tests and 36 full raw two-drone cases. It included signed zero, subnormal arithmetic, overflow, invalid intervals, threshold boundaries, tilted geometry, common translations, positive interactions, model rejections and invalid preparation. Source commit `abcee1164faa21c0e5a4b189daa4578699ea7577` and its 51-pin manifest were published and independently verified before execution.

The candidate uses outward binary64 intervals only to certify existing zero branches. Every uncertain or unsupported calculation calls the original exact query. It keeps the original order of guards and decisions. Positive coefficients and scientific refusals remain the responsibility of the unchanged exact code.

## What happened

| Two-drone path | Cases | Independent outcome |
|---|---:|---|
| Filter proved zero directly | 5 | All five were exact-model zeros: neighbor 2, upstream 1, near-outside 1, radial 1. |
| Exact fallback | 26 | 14 zeros, 6 positive interactions, 6 model rejections; all full candidate results matched the baseline. |
| Raw preparation refused | 5 | All retained the original refusal; none entered the filter. |

All 36 candidate results matched their baseline records and independently reconstructed reference status/branch. All five coefficient-related intervals for each positive result enclosed the fixed192 reference. No unresolved/reference-undecidable result occurred, and there were zero baseline errors. The arithmetic suite returned 24 adjacent-word results, 31 enclosing finite intervals and 17 explicit refusals; every case passed its declared check.

All 16 corruption controls failed for their intended reasons, including inward bounds, lost underflow, false finite overflow, division through zero, a square interval losing zero, a false zero on a positive interaction, wrong branch priority, changed preparation, lost positive coefficient and missing/reordered evidence. The complete 110-event journal passed.

## What improved, and what remains open

Five candidate queries avoided the exact scalar call. This is a work-path observation, not a measured time saving. The verification run also executes the baseline, so its elapsed time cannot estimate production performance. Filter overhead could still exceed the cost it avoids.

No fast down-cut or projection decision occurred, although those original branches were exercised through fallback. Exact threshold equalities and cancellation are intended sources of uncertainty for this conservative implementation. The suite is small and hand-picked to challenge boundaries; it does not establish a general hit rate or prove all possible runtime behavior.

Published work already establishes numerical filtering with exact fallback. This checkpoint adapts that principle and supplies finite verification for the declared graph; it does not establish novelty, physical validity, full load accuracy in a new group suite, moving Boids behavior or a real-time 5,000-drone browser simulation. The original physical model and its limitations remain unchanged.

The next gate is a fresh matched total-cost comparison with the filter disabled/enabled, charging preparation, filtering and exact fallback. If that is useful, return to moving-swarm integration. Preserve exact shared-work reuse and batching as competing options if filtering is ineffective.

## Inspect the evidence

- `viewer/` is an updated Three.js diagnostic for all 36 saved pair cases, with arithmetic outcomes and qualification details. It is static saved evidence; the prior group timing view and historical airflow-off moving replay remain separately linked.
- `results/filter-results.json` and its journal contain all raw records; `results/reference.json` and `results/independent-check.json` contain the independent evidence and controls.
- `PROTOCOL.md`, `REPRODUCIBILITY.md`, source and review records describe the frozen attempt and its trust boundaries.
- `review/literature/LITERATURE.md` and `bibliography.json` identify the verified prior research, versions and supporting passages. Original retrieved paper assets remain private.

Both sole scientific allocations completed and closed: kernel 0.753437 seconds with eight memory samples and 80,052,224 bytes peak sampled group RSS; checker 0.444883 seconds with four samples and 70,008,832 bytes peak. These are containment observations, not method benchmarks. All source/runtime/input identities passed. Do not rerun this closed allocation or modify its pinned evidence. Public result verification and a precise restart receipt complete this checkpoint; the overall research goal remains active.
