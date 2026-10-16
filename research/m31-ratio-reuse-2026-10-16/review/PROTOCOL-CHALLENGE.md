# Prospective challenge: direct-root temporal reuse with full wrench feedback

Date: 2026-10-16. Reviewer: `/root/m31_protocol_challenge`.
Repository inspected read-only: `repository root`, HEAD `3c8430ff67f50168a035257735e83a198b13a61b`.
Intended package: `research/m31-ratio-reuse-2026-10-16` (not yet present during this review).

## Assessment and scope

The proposed six-path diagnostic asks a distinct question from the completed force ablation and prescribed-path cadence work: whether holding directly returned, dimensionless coupled rotor roots for 10 ms preserves a selected numerical accuracy budget when current motor states, attitude, controller commands and full modeled wrench affect the path. It does not test omission of aerodynamic moment, a prescribed trajectory, physical wake lag, or actual computational speedup.

The protocol is defensible with the boundary, sampled-domain, acceptance and accounting rules below. This is a prospective protocol challenge, not approval of executable source. No candidate import, scientific computation, simulation, external acquisition or repository edit was performed. Prior source and already-saved JSON were read only; storage and call arithmetic below are planning calculations. Static executable review remains necessary after the package exists.

## 1. Fix the hybrid update order and the load side

Parent has adopted the following positive-boundary convention. At each accepted 10 ms boundary:

1. Complete the preceding RK4 step with its old cache through its ending k4, even though that stage has the boundary timestamp. Project the weighted accepted quaternion and run the existing accepted-step safety checks.
2. At the accepted state, evaluate `left` using the preceding cache and the incoming held commands. Do not confuse the k4 trial state with the accepted state.
3. Run exactly one current-state coupled geometry/build/solve/residual evaluation. Save its instantaneous result and direct returned `x`; this supplies the new cache. Save `right` using the reuse derivative code with that new cache, the same accepted state, and the same incoming commands.
4. At positive 100 ms sample times, the legacy sample aliases `left`. Update the controller before the next propagation interval. The next k1 at the same timestamp uses the new cache and new held commands.

At t=0 there is no preceding interval: initialize once, set `left` absent, and let the legacy sample use `right`. At t=2 s, retain the terminal `left`, instantaneous solve and `right`; count that solve even though its new cache has no subsequent interval. A post-refresh load comparison is a construction check; it cannot replace the left-side stale-load test.

Use integer step/interval indexes to select boundaries, with all three h dividing 10 ms. Specify timestamps and cache IDs so the ending k4 has cache age 10 ms, while the subsequent k1 has age zero. An interval must have one immutable cache, not a cache refreshed by a stage timestamp test. Positive samples retain the historical incoming-command convention, including the terminal sample.

## 2. State exactly what is held and applied

Cache the solver-returned 16-by-4 rotor `x` array directly, with event ID and creation time. Do not recover roots by dividing effective thrust by old nominal thrust. At each reuse stage, use that stage's current nominal motor state `f0` and compute `T = f0 * x_cached`. Recompute the effective-minus-nominal collective force in the current quaternion orientation and the roll/pitch moment from current rotor deltas. Keep nominal rotor torques, nominal yaw torque, body-rate gyroscopic terms, quaternion dynamics and motor lag unchanged. “Full wrench” here means the inherited modeled axial-force and roll/pitch correction; it does not introduce an aerodynamic yaw torque.

A cache contains roots, not stale geometry, source totals, roots' alpha values, rotor thrusts, world force, body moments, or derivatives to reuse as if current. At refresh, `right` and instantaneous loads/wrench should agree to the prospectively stated construction tolerance. Initial every-stage/reference and reuse states, commands and loads should match. Beyond t=0 each arm follows its own states and controls.

## 3. Cheap stage checks cannot assert current coupled admission

Inherited `kernel.cjs:prepare` checks finite 17-state vectors, positive nominal rotor values and finite vehicle nominal totals, quaternion error at most 1e-10 and transformed-axis/offset errors at most 1e-9. Its 45-degree tilt count is a diagnostic, not an admission criterion. Full admission additionally checks near-field and invalid symbols and scaled coefficient caps; descending graph eligibility is separate. These depend on current inter-vehicle geometry.

At reuse stages, check finite/shape-correct states and commands; current strictly positive nominal rotors and finite totals; valid projected quaternions and finite axes/tilt; immutable 16-by-4 finite roots with 0 < x <= 1; finite forces, moments and derivatives; valid cache ID; and age within the allocated interval. Keep raw quaternion-norm error as a diagnostic, distinct from the projected-norm test. If a 45-degree ceiling is added, name it a new numerical experiment guard, not inherited admission or physical validity.

Use explicit metadata such as `currentCoupledAdmission: "not-evaluated"` and `currentClosureResidual: null` at reused stages. Old residuals and source/receiver mismatch belong under `cacheOrigin`; they are not current closure witnesses. Do not fill current geometry/closure fields with stale numbers, zero, or `admitted:true`. Full event solves retain the inherited residual limits, 1e-9 and 2e-9, and reject unsupported current geometry without fallback.

Full current geometry at every propagation stage would defeat this allocation's intended workload reduction. Conversely, full admission at each event does not prove admission between events: support, near-field, graph-order and cap boundaries can be crossed and recrossed. An independent fresh-geometry check of retained first/last reuse stages is useful if frozen and counted separately, but it neither repairs propagation nor certifies unsaved stages. Any observed intermediate rejection must be reported as such; it cannot be hidden behind successful event checks.

## 4. Keep numerical resolution separate from approximation accuracy

Retain the five inherited 100 ms refinement metrics: maximum per-vehicle position norm (m), velocity norm (m/s), sign-invariant full quaternion angle (rad), body-rate norm (rad/s), and maximum modeled rotor difference divided by mg/4. Use tolerances 0.001, 0.001, pi/1800, 0.001 and 0.001 respectively. Apply the inherited adjacent-grid rule independently to each arm: medium/fine discrepancy <= tolerance and <= 0.75 times coarse/medium discrepancy, unless both are below 1% of tolerance. Below-floor results do not establish RK order or rigorous error bounds. In particular, decreasing h at fixed 10 ms cache cadence resolves a different hybrid model; it need not converge to the every-stage arm.

Freeze a separate approximation decision. Recommended primary comparison: the finest-grid reuse path against the finest-grid full path, at the same 21 legacy sample times and with the sample-side convention above, using the same five tolerances. Report all three paired-grid differences. Require both arms' refinement gates before describing the fine-grid approximation comparison as resolved at the tested levels. Do not silently substitute a coarser grid, alter cadence, or change a tolerance after viewing outcomes.

For pre-refresh instantaneous error, compare `left` against the fresh solution on the reuse arm's own accepted state with the same commands. A comparison to the independently evolving reference arm mixes stale-load and path-state effects. Recommended numerical preferences, maximized over all 200 positive events and 16 vehicles per reuse path:

- `||F_left - F_instant||_2 / (mg) <= 0.001`.
- `||tau_xy,left - tau_xy,instant||_2 / (mg*R) <= 0.001`, where `R = sqrt(2)*0.028 m` is the rotor-corner lever arm, not rotor aerodynamic radius.
- Retain maximum individual same-state rotor error in hover units; preferably gate it at 0.001 as well, so net-wrench cancellation cannot mask individual errors.

For m=0.027 kg and g=9.81 m/s^2, these limits are 0.00026487 N and 0.000010488316895441329 N m. The scale is defensible as a numerical budget: if every rotor error is at most 0.001*(mg/4), triangle and lever-arm bounds imply these force and moment limits at the same attitude. It is not a physical, control-design or safety tolerance. The rotor threshold across two evolving paths does not itself imply the same-state stale-load bounds; the two tests remain separate.

Report every grid's event maxima and argmax event/vehicle/rotor, raw units and normalized units. Pre-refresh events are samples, not a maximum-error theorem: interior error need not be monotone or peak immediately before refresh. With all implementation checks passing, failure of approximation or wrench preferences is a retained negative scientific result, not a reason to retry or redefine protocol validity. Audit validity, reference/refinement qualification, and approximation preference should have separate booleans and conclusions.

## 5. Minimum retained evidence and independent audit

For each event save the accepted state and incoming commands once, old/new cache IDs and direct roots, both load sides and the instantaneous load result, added force/moment, derivatives, current event geometry and solver witness, and full event admission/residual diagnostics. Save the geometry only for the current instantaneous refresh; old geometry is already available at its cache origin. Reuse 100 ms samples may refer to the saved event data, with their side explicit; they must not trigger another observer solve.

Keep ordinary stage diagnostics without duplicating full geometry. Retain full first and last step witnesses for each completed path, including projected stage states, all four slopes, actual reused roots/provenance, current nominal motor states, forces/wrench/commands and accepted step assembly. Six completed paths give 12 captured full steps and 48 global captured stages. These captures must expose both cache initialization and the old-cache ending k4; selected witnesses are not a full re-integration audit.

The independent reviewer should reconstruct every reference endpoint and every refresh geometry/root, verify cached loads and full nominal-plus-correction derivatives, validate event/cache chains and side aliases, and reconstruct first/last RK4 assembly. It must use direct saved cache roots for reused derivatives, not solve a fresh root and compare that fresh derivative to a stale derivative. If it separately reconstructs current geometry at the 24 retained reuse stages, label and count those reviewer-only checks. As a planning count: 603 reuse event reconstructions + 63 reference endpoints + 24 full-arm captured stages = 690 independent current-state evaluations; adding one at each of the 24 captured reuse stages gives 714, before any explicitly declared extra controls. Legacy reuse aliases need no additional geometry evaluation.

A rejection record must preserve attempted time/step/stage or event side, first failed state, preceding accepted state, current commands, old cache and origin, last successful refresh, and available admission details. Preserve the accepted prefix and the terminal failed event even if no post-refresh cache exists. Count attempts before work so a thrown build/solve is not omitted. A missing observer result cannot masquerade as a completed event. All reuse timesteps remain allocated after a disappointing approximation outcome; domain/resource termination and conditional scheduling remain explicit.

## 6. Complete-path call accounting

The reference keeps only the inherited 100 ms endpoint queries. Saving a reference 10 ms accepted state without geometry is free of additional coupled queries; evaluating full reference geometry there would add 540 queries across the three reference paths and is not proposed.

| h (s) | Steps/path | RK stage derivatives/path | Reference endpoint queries | Reference full evaluations | Reuse full refreshes |
|---|---:|---:|---:|---:|---:|
| 0.005 | 400 | 1,600 | 21 | 1,621 | 201 |
| 0.0025 | 800 | 3,200 | 21 | 3,221 | 201 |
| 0.00125 | 1,600 | 6,400 | 21 | 6,421 | 201 |
| Total/arm | 2,800 | 11,200 | 63 | 11,263 | 603 |

Thus all six complete paths perform 22,400 integration-stage derivative attempts, of which 11,200 use a fresh coupled query and 11,200 reuse roots. They perform **11,866 candidate full geometry/solve/residual evaluations**, not counting any separately declared analytic controls. There are 603 reuse events, 600 positive-event left sides, 63 reused legacy sample aliases, and 600 used cache intervals plus three terminal caches. Logged controller updates are 200/path, 1,200 overall; raw controller function calls may differ because the inherited initialization computes control before its t=0 update.

Use separate counters for full queries, reference endpoint queries, cache-refresh attempts/completions, cached stage derivative attempts, event-side reconstructions and aliases. The old `stageAttempts + sampleAttempts` coupled-call counter is incorrect for reuse. Report actual incomplete-path counts as well as this maximum plan. Full-query count ratios are arithmetic workload descriptions, not measured speedups. One instrumented candidate run and one instrumented reviewer run cannot establish performance scaling or real-time feasibility.

## 7. Prospective storage budget

Read-only inspection of the three already-published full-arm JSON files found a combined **10,067,919 bytes (9.60 MiB)**. Their 63 endpoints use about 1.77 MB total; a full endpoint is at most 28,556 compact JSON bytes. Ordinary full-stage metadata is at most 442 bytes in these existing records. These are old-data measurements for planning, not candidate results or a bound on new trajectory sizes.

The new reuse arm adds 603 full events. Three complete endpoint-shaped copies per event would consume about 51.66 MB (49.3 MiB) for those events alone, before reference records, reuse stages, controls, analysis or reviewer output. A 40 MiB aggregate cap is inadequate for that layout. With state and commands stored once, one current geometry witness, and explicit side load/wrench/derivative arrays, old payload dimensions suggest roughly 45-50 kB/event (about 27-30 MB for all events), plus several MB of stage/control metadata and 9.60 MiB of new reference records. This is still an estimate; new geometry could be denser.

Structural dimensions: each event has 64 direct roots (512 bytes as doubles), 272 state values (2,176 bytes as doubles), 1,024 symbol entries including diagonal placeholders, 65 CSR offsets, and at most 960 positive directed rotor/source terms. Across 603 events, root payload alone is 308,736 binary bytes and state payload 1,312,128 bytes; JSON syntax, decimal strings, redundant arrays and object/heap overhead are additional. Do not present these payload counts as RSS or serialized-byte guarantees.

Recommend freezing a final-schema byte estimate and an explicit aggregate evidence cap; **96 MiB with a declared normal-write and failure reserve** is a reasonable conservative proposal for a shared-state/event layout. A tighter cap requires an actual static schema calculation; a naive triple layout or copied reference inputs needs a larger budget. Decide before execution. Account for candidate/reviewer output, logs and any copied inputs consistently. No post-outcome cap enlargement. Preserve failure essentials even if a full active record exceeds the reserve; incremental durable prefixes or a prospectively defined compact failure record avoid losing the decisive state/cache evidence. Enforce both the serialized-byte limit and process RSS/wall limits.

## Closing conditions

Before freezing: specify approximation gate scope; adopt or replace the numerical wrench preferences with fixed values; finalize event schema and resource budget; and statically review executable event ordering, direct-root propagation, counters, reviewer semantics and failure retention. Reference repetition must match the three pinned completed full paths before conditional reuse paths run. Earlier ablation/cadence/storage/GPU/transport allocations remain closed.

If this diagnostic succeeds, the supportable conclusion is limited to sampled numerical accuracy and counted full-query reduction for one exposed 16-vehicle, 2-second seed under this provisional model and controller. It provides no physical validation, continuous-domain certificate, error bound between samples, stability or collision-free guarantee, or 5,000-drone timing result.
