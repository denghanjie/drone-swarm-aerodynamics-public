# A coupled-load calculation can be simpler in a restricted geometry

We implemented an explicit hypothetical source-strength response while retaining four individual receiver rotors. On two eight-drone stacks, calculating from top to bottom agreed with repeated simultaneous updates and an independent high-precision solution. Each ordered solve used 32 root closures instead of 256 iteration closures. The six-drone loop could not use height ordering, but simultaneous iteration converged. The unsupported nearby pair was rejected without solving.

This establishes small-case numerical consistency and an operation-count reduction under the declared equations. It does not establish physical accuracy, measured runtime improvement, a moving flock, 5,000-drone browser feasibility or novelty. The complete research goal remains active.

## What was tested and what was observed

Frozen source: [4068504296c6b5cc9f4f0139b5813797f7a2b097](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/4068504296c6b5cc9f4f0139b5813797f7a2b097). Exact manifest SHA256 `e6baf88c10fad32c8a0fee287989b6675c6144ba2d25440a34896b43e16ac941`,19 pins. Public source commit and manifest were independently retrieved before execution. One candidate invocation and one independent checker invocation completed, both exit 0, with empty stderr. Both allocations are now closed.

| Designed fixture | Rotor-pair construction calls | Positive vehicle edges | Ordered solve roots | Simultaneous update roots | Updates | Outcome |
|---|---:|---:|---:|---:|---:|---|
| Level stack,8 drones |224|27|32|256|8|Agreed with independent reference|
| Tilted staggered stack,8 drones |224|27|32|256|8|Agreed with independent reference|
| Tilted hexagon,6 drones |120|6|Ineligible|192|8|Cyclic solution agreed with independent reference|
| Nearby pair,2 drones |8|0|Not run|Not run|0|6 unsupported rotor pairs; both constructed corners reject|

Each method also performs one final residual check:32 roots per stack and24 in the hexagon. Including these checks gives 64 versus 288 closures per stack, a 4.5-fold closure-count difference. Excluding checks, 32 versus 256 is 8-fold. Neither ratio is a timing speedup. Geometry was built once per fixture and shared; sorting, graph construction, validation and arithmetic outside the counted positive terms are not represented as root closures. No dynamics, Boids, rendering, data transfer, synchronization or hardware benchmark is included.

The independent Python implementation reconstructed every fixture and every pair predicate/coefficient, then used Decimal80 Newton roots and an independent simultaneous solve. All **10,007 checks passed**, with zero failures. This is one designed suite, not10,007 independent trials. Its high-precision references took 8, 8 and 28 updates. Maximum saved final per-rotor relative differences were 3.14e-16,2.72e-16 and9.26e-15 respectively, within the frozen 1e-9 numerical tolerance. These are numerical agreement results, not experimental uncertainty estimates.

The unchanged-source ablation (one map evaluation from nominal source amplitudes) differed from the coupled reference by up to 23.57%,3.75% and0.514% per rotor in the three admitted fixtures. This shows that the new source-response assumption can materially change this model's answers. It does not show that the changes are physically better. The ablation reuses the first iteration and adds no candidate evaluations.

## The explanation and its limits

For consistent rotor geometry tilted at most 45 degrees, the existing admitted positive far-wake terms always point to a lower drone center. That gives an evaluation order. The symbolic proof is a sufficient condition, not a sharp flight limit. Near-field rejections remain outside the law. The broad-tilt hexagon is an explicit positive directed-cycle counterexample to unrestricted vertical ordering.

A separate exact-real derivation establishes that the fixed-coefficient four-rotor map contracts by at most 1/2 in logarithmic coordinates. That proves existence, uniqueness and convergence under its assumptions, including cyclic graphs. All three computed fixtures also have ordinary contraction bounds below 1 (0.4801,0.1688,0.0742), so this suite does not empirically demonstrate a benefit in a case where the ordinary bound fails. The log-coordinate technique has published antecedents; no priority claim is made.

The numerical review is not outward-rounded interval arithmetic. In the level stack, the saved rotor discrepancy (3.13e-16) exceeds the residual-only theoretical estimate (2.20e-16). This is compatible with separate root/map rounding, which the residual-only expression omits. We retain both and explicitly decline to label the expression a certified bound on the saved floating result. A formal numerical certificate would need enclosing evaluation-error bounds.

The source law scales a fixed hover wake by the square root of total effective force, while leaving shape/support unchanged. It ignores source-rotor asymmetry. The receiver uses the retained ideal-power cubic; this is not an experimentally identified fixed-PWM/RPM law. Physical comparisons remain unresolved, as recorded in the prior [command-bridge admission](../m31-command-bridge-admission-2026-10-16/DECISION.md).

## Records and visible update

[Three.js replay](viewer/) shows exact saved fixed geometry, graph edges and all saved source-amplitude iterates. It is a recorded steady solver, not flying/fluid simulation. The historical local-Boids replay is linked. Read [protocol](PROTOCOL.md), [all numerical evidence](results/evidence.json), [independent review](results/independent-review.json), [compact derived summary](results/summary.json), [reproduction](REPRODUCE.md), [result claims](RESULT-CLAIM-LEDGER.md), [literature ledger](LITERATURE-EXPERIMENT-LEDGER.md) and [next decision](NEXT-DECISION.md). Publication observation is recorded separately after pushing the result.
