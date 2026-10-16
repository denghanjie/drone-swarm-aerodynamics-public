# Exact screening saves time, but remains far from real time

**The hierarchy was faster in all24measured pairs, while all six scenes passed the independent numerical checks.** The useful result is a measured calculation-cost improvement under the unchanged model. The unresolved problem is absolute speed: the dense216-drone hierarchy calculation still took a median8.761seconds. This does not yet support a real-time5,000-drone swarm.

## What we did

Compared complete interaction enumeration with exact spatial screening on the same dense and sparse upright cubic lattices of64,125and216drones. Each scene had one recorded warmup per method and four measured pairs in the fixed order AB,BA,BA,AB. We timed validation, preparation, spatial work, pair assembly and certified loads together. Input-text conversion, final serialization/hashing, disk writes, rendering and shared startup are outside that method interval.

The full source was frozen, pushed and independently verified before the sole kernel/checker allocations. No scientific repair or rerun occurred. All60trials, six full paired scientific records, the journal and independent references are retained.

## What happened

| Group | Drones | Complete median (s) | Hierarchy median (s) | Median paired ratio | Ratio of medians |
|---|---:|---:|---:|---:|---:|
| Dense | 64 | 0.757 | 0.494 | 1.521x | 1.531x |
| Dense | 125 | 4.721 | 3.317 | 1.396x | 1.423x |
| Dense | 216 | 14.275 | 8.761 | 1.634x | 1.629x |
| Sparse | 64 | 0.371 | 0.101 | 3.667x | 3.686x |
| Sparse | 125 | 1.548 | 0.422 | 3.594x | 3.665x |
| Sparse | 216 | 4.770 | 0.598 | 7.879x | 7.982x |

Ratios are complete/hierarchy; larger than1means screening used less time. The median of paired ratios and ratio of medians are deliberately separate. Every individual duration and exact reduced fraction is in results/timing-index.json. The four pairs are descriptive observations, not a confidence interval or a claim across hardware/scenes.

All six scenes passed every normalized1e-8load tolerance. The independent checker regenerated527,776pair outcomes and validated1,055,552method outcomes, including implicit/pruned zeros. Both methods produced identical common scientific payloads. All60context-bound trial digests matched the fixed first-measured representatives. All15targeted corrupted records were rejected for the intended reasons; there were zero baseline errors.

## What this means

Screening saves time on this suite even after paying for exact bounds, tree construction and traversal. The largest benefit appears when drones are far apart and most interactions are zero. This replaces the earlier scalar-call-only claim with a measured total-method-cost result.

The remaining bottleneck is the combined traversal/scalar/assembly stage. For dense216, its hierarchy mean was8.656seconds out of an8.844second mean total; preparation was0.093seconds and admission/solve/certificate0.092seconds. These stage means describe a different statistic from the overall medians. They locate cost within the instrumented boundary; they do not isolate a single primitive such as rational arithmetic or garbage collection.

**We have not established novelty, flight-physics validity, real-time browser performance, or coupled5,000-drone trajectories.** These scenes use identity orientations and the admitted ordered positive-interaction subdomain; they do not test general tilted or cyclic swarms. No flight data were used. Exact agreement establishes numerical correctness for the declared model and scenes, not realism of that model.

The next research question is how to reduce the expensive interaction stage while preserving the same proof obligations. Any proposed faster filter must conservatively identify cases it can certify and fall back when uncertain; it needs a new prospective design, verified literature comparison and separate bounded experiment. This is a hypothesis, not a demonstrated solution.

## Inspect and reproduce

- Open viewer/index.html through localhost8876for the updated Three.js geometry, selected-rotor links, hierarchy boxes, all timing pairs and stage costs. This is a saved static diagnostic. The separately linked historical moving5,000-drone Boids replay has airflow off.
- PROTOCOL.md and source/result-contract.json state the frozen allocation. Source commit:7d3c94410aaece78a151c13b7192c3a40ecb60d0.
- results/timing-index.json and its journal bind all trials and six scientific shards. results/independent-check.json binds six independent reference files and all controls.
- Kernel supervision:202.456s,2515RSS samples,304594944B peak sampled group RSS. Checker:165.535s,1988samples,199229440B peak. Both child groups closed; source/runtime/input identity checks passed. These are supervision metrics, not method benchmark durations.
- Host activity, V8/JIT/GC/cache/thermal carryover, fixed scene order and supervisor polling can affect timings. The frozen timer is a trust boundary; saved evidence validates its arithmetic and provenance, not independent elapsed-time remeasurement.

Scientific allocations are closed. Preserve every original artifact. Updated display QA, saved-evidence audit and public result receipt are separate closeout records. The larger research goal remains active.
