# Exact spatial screening: milestone summary

**The exact hierarchy preserved the complete method’s results in this declared static suite while using about75.3% fewer scalar pair evaluations.** All18 scenes passed independent verification:12 admitted load solutions met the exact1e-8 normalized force/moment tolerance, and6 correctly retained model/preparation/ordering refusals. All16 deliberate faults were detected by their intended independent checks. These are numerical-model findings, not a speedup, physical-validation or novelty result.

## In plain language

The method puts source drones into boxes. If a box is provably irrelevant to a receiver rotor, it skips all those pairs. Otherwise it opens the box or checks individual members. The independent checker still examines every pair, including those skipped by the candidate, so it can expose an incorrect shortcut.

The complete method made46,712 scalar calls; the hierarchy made11,548 and proved35,164 pairs zero in groups. Its answers, candidate bits and entire load-certificate payload matched the complete method exactly in all18 scenes. Tree creation, exact bounding and traversal are extra work. We have not measured whether the savings outweigh those costs.

## What was tested

Eighteen newly declared scenes contain312 drone records in total and at most64 drones in any scene: dense/sparse3D groups, tilted states, input permutation, cutoff boundaries, deliberately unsupported inputs and a conservative-proof fallback. The planned count is46,744 logical pairs per method. Two globally invalid scenes skip32 pairs per method before any pair work; they are refusals, not empty successful solutions. Of the remaining46,712 pairs per method, every nonself membership is accounted for.

All12 admitted scenes satisfy the four exact tolerance checks: rotor, collective thrust, world force and world moment. The six refusals preserve near-domain, cap, ordering, preparation, center-guard and raw-force reasons. A failed global box proof correctly triggers a complete scan before the center-guard refusal. No reference uncertainty or stress exception was needed.

| Scene | Outcome | Complete scalar calls | Hierarchy scalar calls | Pruned pairs |
|---|---|---:|---:|---:|
| offset-singleton | certified: loads | 0 | 0 | 0 |
| dense-cube-27 | certified: loads | 2808 | 1872 | 936 |
| dense-cube-64 | certified: loads | 16128 | 4992 | 11136 |
| sparse-cube-64 | certified: loads | 16128 | 896 | 15232 |
| four-columns-32 | certified: loads | 3968 | 1232 | 2736 |
| tilted-cube-16 | certified: loads | 960 | 648 | 312 |
| permuted-cube-27 | certified: loads | 2808 | 1872 | 936 |
| neighbor-boundary-16 | certified: loads | 960 | 0 | 960 |
| near-slab-outside-16 | certified: loads | 960 | 0 | 960 |
| radial-outside-16 | certified: loads | 960 | 0 | 960 |
| down-cut-boundary-16 | certified: loads | 960 | 0 | 960 |
| near-domain-refusal | rejected: pair-near | 8 | 4 | 4 |
| scaled-cap-refusal | rejected: pair-cap | 8 | 4 | 4 |
| upward-order-refusal | rejected: ordering | 8 | 4 | 4 |
| global-invalid-three | rejected: preparation | 0 | 0 | 0 |
| center-guard-fallback | rejected: pair-center-guard | 24 | 24 | 0 |
| center-guard-equality | certified: loads | 24 | 0 | 24 |
| raw-force-refusal | rejected: raw-force | 0 | 0 | 0 |

## What this supports—and what remains open

This supports exact-support screening correctness for the recorded scenes and the reviewed conservative predicates under the unchanged current-state model. It does not demonstrate that the hierarchy is faster, that it scales to5,000 drones, that coupled flight trajectories are stable, or that the aerodynamic law matches reality. The ordering restriction remains; arbitrary cyclic positive interactions are outside this allocation. The2,000,000-positive-term resource threshold is not experimentally reached.

The next useful checkpoint is a preregistered matched total-cost comparison: charge raw preparation, global proof, tree build, query work and load solve equally, measure both methods on fixed fresh size/density cases, and retain a new independent correctness check. If exact-bound overhead dominates, report that negative result before considering a separately specified optimization. Browser integration, larger scales, dynamic physics and verified prior-art/physical evidence remain separate obligations.

## Evidence and visibility

Source commit:20edde079fe3092e11da499405f0d6dbbbf38a27, remotely verified before execution. The raw paired records, append/fsync journal, independent reference/controls and supervision reports are in results/. Both sole scientific attempts are closed, their child groups absent, source/runtime identities rechecked. Their wall times are supervision evidence only and cannot be used as method speed measurements.

The Three.js viewer displays the saved group, selected receiver/rotor and zero-proof boxes. It is a static diagnostic. The linked historical5,000-drone Boids animation remains unchanged with airflow off. The full research goal is still active.
