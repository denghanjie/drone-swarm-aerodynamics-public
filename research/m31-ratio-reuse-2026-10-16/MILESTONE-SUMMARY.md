# Ten-millisecond reuse saved queries but missed the accuracy screen

We tested a simple way to avoid repeatedly calculating mutual airflow: keep each rotor's solved load ratio for 10 milliseconds, while continuing to update steering, motor states, drone motion and the full pushing/turning effect. The comparison used the same exposed 16-drone 3D Boids case over two seconds, with three integration resolutions.

**The experiment was numerically adequate; the approximation failed.** All six paths completed, all three full-reference paths reproduced the prescribed saved sample fields from the earlier checkpoint exactly, all ten refinement gates passed, and the separate saved-data audit passed 559,589 assertions. Yet all 15 motion/load comparison gates and all nine before-refresh load gates missed their declared limits. No limits were changed and no failed path was discarded.

At the finest integration timestep (1.25 ms):

| Maximum sampled full/reuse difference | Observed | Declared limit |
|---|---:|---:|
| Position | 36.861 mm | 1 mm |
| Velocity | 0.168290 m/s | 0.001 m/s |
| Full orientation, including yaw | 0.162835 rad, about 9.33° | 0.001745 rad, 0.1° |
| Rotor load, divided by nominal mg/4 | 0.238347 | 0.001 |
| Body rate | 1.941097 rad/s | 0.001 rad/s |

The largest position difference occurred at 1.7 s for drone index 11 (zero-based). The position result stayed approximately 36.861 mm across all three integration timesteps. Finer integration did not remove this fixed-reuse discrepancy. The observed medium/fine position discrepancies within the full and reuse arms were 5.35e-8 and 2.96e-8 m; these are numerical-resolution context, not rigorous error bounds. Eight of ten refinement gates used the below-floor exemption, so we make no formal-order claim.

We also compared stale and freshly calculated loads at exactly the same state immediately before each refresh. On the finest path, maximum errors were 0.034641 nominal-hover units per rotor, 0.022282 mg in collective force and 0.010176 mgR in moment. All exceed 0.001. Those local same-state errors differ from the larger contrasts between the independently evolving trajectories. After refresh the load differences were exactly zero, as expected from copying the fresh roots; that identity does not establish accuracy during reuse.

What improved was the **number of joint queries**: across three grids, the full reference used 11,263, versus 603 reuse queries including three terminal audits. At the finest grid this was 6,421 versus 201. These are call counts, not measured speedups: the reuse arm still calculates steering, motor/body dynamics and cached loads. The instrumented resource timings are not benchmarks. The earlier roughly 475 ms 5,000-drone joint-query cost also remains unresolved by a 10 ms refresh schedule.

The new [Three.js comparison](viewer/) shows exact saved poses at all three integration timesteps, with the failed gates visible. It is recorded replay, not live simulation. This result supports rejecting this particular fixed shortcut under this declared screen. It does not prove that every reuse method fails, that the tolerances reflect real-flight needs, or that the underlying aerodynamic equations are physically valid. It is not a novelty or publication-ready claim.

Evidence: [frozen protocol](PROTOCOL.md), [configuration](config.json), [raw analysis](results/analysis.json), [independent review](results/independent-review.json), [saved argmax locations](analysis/saved-extrema.json), [claim and source ledger](RESULT-CLAIM-LITERATURE-LEDGER.md), [reproduction](REPRODUCE.md), [restart](POSTRUN-RESTART.md). Source: [b8ff0c4dca71187db7efd8d72cde2d83fcdb3288](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/b8ff0c4dca71187db7efd8d72cde2d83fcdb3288). Exact result commit and remote verification are recorded separately in `research/publication-receipts/m31-ratio-reuse-result-2026-10-16.json` after publication, avoiding a self-referential checksum.
