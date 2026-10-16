# Milestone: the coupled calculation transfers to saved 5,000-drone states

**What we tested.** The previous checkpoint used small stacks of drones. This checkpoint asked whether the same four-rotor load calculation can be applied to actual saved M31 swarms, with every drone and interaction retained. We fixed four snapshots before scoring:1,000 drones at20s and5,000 drones at20s,60s and180s, all from the same exposed historical scenario/seed family.

**What happened.** All four snapshots passed the declared model-domain checks. Both the ordered solve and repeated simultaneous updates completed. The independent Python/NumPy review passed all581 grouped checks:304 million receiver/source/rotor classifications matched exactly; all320,200 positive coefficients and all returned rotor loads and amplitudes passed their stated tolerances. No near-field or invalid-term rejection was found in these four snapshots. No threshold, input, model or source change followed observation.

| Saved state | Positive vehicle dependencies | Longest dependency depth | Simultaneous updates | Ordered solve root closures | Simultaneous solve root closures |
|---|---:|---:|---:|---:|---:|
|1,000 drones,20s|4,111|8|7|4,000|28,000|
|5,000 drones,20s|33,706|14|10|20,000|200,000|
|5,000 drones,60s|32,097|15|10|20,000|200,000|
|5,000 drones,180s|23,201|8|8|20,000|160,000|

Each solver also performs one separate final check, costing another4N root closures. The table excludes that extra pass and all geometry work. A closure with zero inflow returns immediately; closures are not interchangeable units of CPU time. These counts do **not** establish a runtime speedup.

**What improved.** The numerical evidence now covers complete5,000-vehicle records, including actual saved attitudes and four different motor-force states per drone. The maximum observed relative discrepancy in the independent solution comparisons was2.28e-14 (below the declared1e-9 tolerance). The maximum coefficient discrepancy was2.23e-15 in the inherited speed units. This is a double-precision consistency test, not a mathematically rounded certificate.

**What remains uncertain.** The historical flight was generated with airflow OFF. We froze those positions and interpreted its motor-lag force states as nominal inputs to a new, hypothetical thrust-dependent wake law and ideal-power receiver law. The resulting loads were not fed back into motion. The lowest predicted total-load/nominal ratio was about0.563; that substantial modeled change is a reason to avoid treating the old flight path as a validated aerodynamically coupled mission. It is not a measured thrust loss.

All maximum tilts were below8.37degrees, every positive influence descended in center height, and all ordinary contraction bounds were below0.356. These are mild admitted conditions. They do not test the stronger log theorem's extra domain, cycles, unsteady wake history, near-field forces, extreme attitudes, real-world accuracy, fresh independent scenarios, low-end hardware, real-time browser simulation or novelty. Three times share one trajectory; this is not a statistical sample of independent trials.

**What comes next.** The calculation used75,984,000 center checks and25,324,040 rotor-pair evaluations to retain320,200 positive coefficients. We should measure where time is actually spent before declaring ordering useful. A new bounded campaign should compare complete coefficient construction plus solving, with an exact spatial-neighbor baseline, repeated timings and correctness checks. Physical validation remains a separate evidence gap.

The [Three.js viewer](viewer/index.html) shows the actual recorded group poses and final saved source-load colors. It is a frozen-state viewer; display magnification changes drone glyph size only. Historical local3D Boids motion remains linked separately. [Full evidence](results/evidence.json), [independent checks](results/independent-review.json), [descriptive analysis](results/analysis.json), [frozen protocol](PROTOCOL.md), [reproduction](REPRODUCE.md), [claim ledger](RESULT-CLAIM-LEDGER.md) and [literature provenance](LITERATURE-EXPERIMENT-LEDGER.md) preserve the trail.

Source commit: [702abf6](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/702abf6b02d53b1008495e2fa579aabf58a445c5). Exact result commit is recorded by the separate publication receipt after remote verification. Both scientific allocations are closed; the overall research goal remains open.
