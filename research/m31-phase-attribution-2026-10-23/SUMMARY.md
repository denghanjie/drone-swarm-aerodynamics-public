# Where the recorded calculation spends its time

We have finished a new analysis of the saved experiment. We did not fly a new simulated flock or run new aerodynamic calculations. Think of it as examining a receipt to see where the money went.

For every 100 units of time spent on successful baseline queries, the largest recorded parts were:

| Work | Share of recorded query time |
| --- | ---: |
| Build the interactions between drones | 29.81% |
| Read and validate inputs | 18.98% |
| Construct forces | 14.96% |
| Other building and validation work | 10.64% |
| Check numerical residuals | 7.98% |
| Solve the interaction equations | 7.96% |

The complete table, including the smaller parts, is in the [3D evidence page](viewer/). These are rounded display values from the audited exact logged-decimal totals; they do not imply that the clock measured every displayed digit accurately.

## What we learned

Interaction building is the largest part in all eight recorded repetitions. But its 29.81% share is below our predeclared 50% majority requirement. The formal classification is therefore `distributed-or-unstable`: in this case **distributed**, with a consistent largest component. The result does not show unstable rankings or a single dominant bottleneck.

This helps explain why saving some distance calculations need not deliver a large overall gain: distance checks are only one activity inside the interaction-building bucket, which itself is only part of the complete query. This is a descriptive interpretation, not an isolated measurement of the distance checks or a causal explanation of the earlier small change. The existing timers cannot separate distance checks, rotor interactions, list/cache work and assembly within that bucket.

The earlier shortcut still fails the preset benefit and coverage requirements. Its median measured candidate/baseline ratio remains 0.980473 (about 1.95% less query time). This new analysis establishes no new speedup. In the pooled successful measured records, interaction building totals 4,050.121 ms for the baseline and 4,091.642 ms for the candidate; that observation does not prove which operation or runtime effect caused the difference. The displayed phase totals use successful measured queries and a pooled denominator; the prior median ratio uses its original per-repetition definition. They must not be substituted for each other.

## What was checked

All 34,560 existing query records were retained, covering 1,920 saved stages, both methods, warmup and eight measured repetitions. An independently written rational-arithmetic auditor reconstructed every row, every summary, 216 reset-inclusive group reconciliations and all 1,920 paired timing annotations. The headline uses 15,352 successful measured baseline queries. Warmup, resets and refusals remain separately recorded.

The one inherited near-field refusal remains visible, repeated eighteen times in the query records. Its missing kernel sub-timings are marked unavailable, never zero. The four producer/audit/finalizer/UI allocations each ran once and closed successfully. No native query or new flight ran. The updated Three.js page replays the earlier recorded positions, with new timing annotations and a baseline/candidate breakdown. All records and the display controls were tested; desktop/mobile screenshots were inspected.

## Decision and next step

Keep the previous decision to retire the exact radial-cache implementation on this workload. Inspect the interaction-building source for avoidable data creation or repeated work, while preserving the existing calculations, validation, refusal behavior and evidence contract. Use this cost map to choose one concrete change before opening another benchmark. Do not merely add more distance-skipping machinery on the assumption that fewer checks must be faster.

Any proposed replacement needs its own bounded reviewed experiment and a complete-query comparison. This checkpoint identifies where to look; it does not establish an optimization, physical accuracy, flight safety, novelty or large-swarm scaling. The research is not complete.

## Records

[Fixed protocol](PROTOCOL.md) · [Independent source review](review/PROTOCOL-REVIEW.md) · [Saved numerical report](results/summary.json) · [Independent audit](audit/audit.json) · [UI evidence](UI-QA.md) · [Restart instructions](RESTART-RESULT.md). The source was published and all 54 source/input file identities independently verified before execution. Final result publication is recorded in the separate publication receipts.
