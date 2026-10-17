# Prospective strict coupled-stage qualification — not frozen or executable

Source preparation started17October2026. Execution disabled. No new execution window is approved; the previous window ends03:00UTC17October. This draft is not permission to launch. All open items below must be resolved into a frozen source/configuration before requesting a new window and dispatching science.

## Question and scope

Can the existing projected whole-swarm integration approach consume the latest native delivered aerodynamic loads on every stage of a short64-drone Boids continuation while retaining the specified numerical load observables and correct state/controller feedback?

The original eight-step framework remains: this is numerical interaction/flight integration verification (Steps3–6), a prerequisite for coupled scaling (Step7), with no contribution/novelty gate satisfied (Step8). Earlier16-drone projected coupling already exists. This tests the newer strict load interface and every consumed stage; it does not claim first-ever coupling.

The physical target remains the specified hypothetical directed axial-load/source-strength model with no wake memory and no new reaction-yaw law. Numerical agreement is not measured aerodynamic accuracy. The prior upper-response literature review remains unresolved for a matched admitted-domain falsification.

## Fixed primary continuation

Use the complete saved `fresh-a-t5` input, all64stable IDs and all17binary64 words, at original absolute time5s. No subset, seed search or new initialization. Continue0.02s using8whole-swarm projected RK steps of0.0025s, with4synchronized stage evaluations per step. The second local Boids/control update occurs after0.01s and reads the actual evolved state. Preserve inherited local separation/alignment/cohesion, shared broad route guidance, wide-factory geometry, wall-priority policy, motor lag and nominal actuator states.

Primary on branch:32native F queries on complete simultaneous stage states,32unchanged exact-reference evaluations on the actual saved consumed states. Matched off branch uses the same projection/control/step schedule and nominal loads; its derivative stages and feedback are saved, with no aerodynamic solver required for zero influence. Native reference calls must be enumerated by exact stable stage IDs; duplicate/missing/extra stage evidence prevents qualification.

This is a new coupled simulation starting from an exposed saved state, not a replay or fresh held-out confirmation. The claim is interface qualification on that continuation. It does not establish robustness, mission success or scaling.

## Integration and consumption contract

Project each stage quaternion once before querying and evaluating derivative geometry; preserve raw stage words separately. Use the projected words consistently in preparation, qdot and frame conversion. The driver combines stage derivatives from the common step base and normalizes the endpoint. Freeze floating operation order. Retain one cheap raw second-stage preparation/admission diagnostic, with no alternate full solve or fallback branch. Projection is predefined and is not chosen after observing refusal.

Keep the existing nominal first-order motor state and explicitly provisional nominal reaction-yaw policy. Replace or equivalently correct nominal translational rotor force and lever-arm moment exactly once; gravity remains separate. Native total world moment excludes reaction yaw. World/body conversion and effective-minus-nominal arithmetic must be independently checked rather than assuming the old correction adapter proves a different expression graph.

A returned load must match the exact current stage, stable IDs and nominal motor states. Save raw/projected stage inputs, commands, native prepared/solved/delivered words, actual consumed force/moment, derivatives, intermediate and endpoint states. Do not substitute a checksum for use in the derivative. Record a nonzero initial influence and its path through subsequent states and the second control update. Stage freshness, nominal state/command distinction and world/body semantics are separate gates.

## Controls and numerical acceptance

Retain the unchanged pair/root reference precision:192-bit coefficient/source intervals,128root bisections, maxDrones180, unchanged scientific guards. Every consumed on-stage load must satisfy all four normalized numerical error limits1e-8: per-rotor maximum/(mg/4), collective/mg, Euclidean world force/mg, Euclidean world moment/(mgR), including reference uncertainty. Unsupported/reference-unresolved states are failures, never omitted.

Before primary continuation, execute a fixed manufactured suite for identity/no-influence, no double thrust, unequal-force moment sign, tilted force/moment frame conversion, nominal reaction yaw and motor-state evolution. Adversarial saved controls must challenge stale stage, ID misassociation, missing moment, wrong frame, doubled force and overwritten motor state. The final source config and independent checker must name every case, mutation, expectation and count before freezing; no favourable-witness search.

Analytic no-flow translation/hover and principal-axis rotation controls use a common0.01s interval at h=.0025/.00125/.000625. Freeze exact state/quaternion norms and roundoff floors before launch. An error below a roundoff floor cannot establish an observed convergence order. Same-state aerodynamic accuracy does not bound continuous-time trajectory error. All finite controls must pass before the primary branch.

## Resource and shutdown contract

Proposed full reservation:960s, comprising browser120s, exact reference600s, saved checker180s and60s shared closure/accounting. Include all source verification, setup, serialization, handoff and closure inside the allocation boundaries; uncounted overhead cannot enlarge the reservation. Final implementation must define per-stage launch checks and cumulative absolute budget handling. No deliberately overlapping heavy benchmarks.

Per-file output cap32MiB, aggregate new outputs/logs/profile/scratch256MiB. Report observed memory scope honestly; a1GiB observed hurdle is not OS containment. The exact reference must retain the existing per-call30,000suffix cap; the32whole64cases have516,096logical rotor/source pairs in total. Confirm total admitted numerical/fixture work separately from this identity in final config.

Browser work uses a newly owned Chrome root/controller and existing local static server8876. Retain the guardian until those owned root/controller handles report terminal closure. Do not signal a reaped group or claim all-helper containment. Preserve first failure and partial outputs; no retry or recovered second run in this allocation. Failed cleanup remains an operational failure even if numerical files exist.

## Required before launch

- Complete and independently review adapter, browser driver, loader/controller, exact reference, checker and supervisor together; reconcile file/event schemas and all control counts.
- Resolve explicit config thresholds and floors, comparison/rounding semantics, actual runtime identity, immutable source closure and every start/stop/size budget. Config currently must disable execution and have no fabricated future cutoff.
- Build the source bundle without evaluating scientific factories, freeze all bytes, privacy-review and push the exact source. Verify public bytes.
- Obtain an explicit new execution window containing the complete reservation, bind its authorization prospectively, and freeze any resulting configuration change before launch. Do not reuse or modify the consumed earlier window.
- After execution, preserve raw results/failures, independent review, plain-language summary, actual-record Three.js replay and exact-public GitHub checkpoint.

No experiment, fit, physical score, speed claim or novelty claim is produced by preparing this draft.
