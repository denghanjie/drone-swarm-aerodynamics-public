# Prospective two-arrangement matched-controller study

21 October 2026. Computational-only continuation authorized by the user. All earlier allocations remain closed. This protocol opens one new bounded allocation for four new paths, followed by one saved-evidence audit and one display check. No preliminary simulation or seed screening is allowed.

## Question and fixed cases

Does the unchanged vertical-memory controller preserve or change completion, descent and recorded own-request vertical error on two prospectively fixed starting arrangements, compared with the unchanged original controller?

Use N64, seeds **2026102101 and 2026102102**, and integration step **0.005 s only**. These are date-based fixed examples, not random draws. Their prior-execution search scope and limitations will be recorded in SEED-EXPOSURE.md before source freeze. Do not substitute seeds based on generated geometry or outcomes. This allocation contains no finer-resolution study; earlier resolution results cannot be imported as accuracy guarantees for these paths.

Run in this order: seed2026102101 original, seed2026102101 memory, seed2026102102 original, seed2026102102 memory. The exact case/pair IDs and parameters are in config.json. All four paths start at t=0 and have a five-second horizon. Preserve the previous segmentation: local0..1 at origin0, then local0..4 at origin1. Each arm generates its seed's initial physical state using the unchanged initializer, serializes/reparses the words and evolves independently. The auditor must compare every paired initial 64×17 physical word exactly, check that the two seed states differ, and verify every reached path's own segment boundary. It does not independently reproduce the initializer.

## Unchanged interventions

Import original control/safety from ../m31-boids-continuation-2026-10-20/source/motion.cjs and memory control/safety from ../m31-vertical-memory-2026-10-21/source/motion.cjs, both with their published bytes unchanged. Both use full current F coupling, original 3D local Boids/route/avoidance, factory geometry, physical constants, actuator limits, motor lag, nominal reaction yaw, projected RK and inherited stopping checks. Both adapter/controller model arms remain named coupled; the study arm is separately original or memory. No force-off, gain-search or additional controller is run.

The original target remains `z + (2.5*desiredVz + 1.5*actualVz)/6`. The memory arm keeps the exact previous intervention: per-drone integral/error/count initialized positive zero/positive zero/zero; first increment zero, later increment `(2.5*.01)*previousError`; add and clamp integral to [-5,+5], then store current desiredVz-actualVz and advance count. Target remains `z + ((2.5*desiredVz + 1.5*actualVz) + integral)/6`. No arithmetic regrouping. Integral bounds are not saturation-aware anti-windup; inherited net-command clamp [-4,+5] and motor limits remain active.

Original paths have controllerMemory:null. Memory paths preserve every integral/error word and update count across t=1, using the t=.99 error once at the next update. Reset only at a new memory path's t=0, never at the segment join. The original controller schema has no saved globalControlIndex; derive it from origin/local index without altering the inherited record. The memory schema retains its saved global index. Physical state alone is not a full memory-path restart.

## Prespecified comparisons

Primary: for each seed, report both-completed, original-only-completed, memory-only-completed or neither-completed at five seconds. Retain each arm's actual last completed time, structured native refusal category/trial metadata or endpoint contact/vehicle-limit reason. Completion means only that the implemented discrete checks passed over this finite horizon. A native refusal is a model-domain/numerical admission outcome, not a collision. Two chosen examples do not estimate population reliability. Do not pool earlier exposed results as new independent trials.

Secondary positional observations: at the last integer step available in both paired paths, report each actual saved time, each arm's mean vertical displacement from its matching initial state, mean-height difference, drone17 center heights, maximum and RMS center separation. Terminal outcomes/heights are separate when endpoints differ. ID17 is retained as the earlier fixed visual marker, not selected from these outcomes. Never extrapolate a stopped suffix. Higher altitude alone is not better tracking of a changing Boids request.

Secondary own-request error: at every saved controller update, independently compute |desiredVz-actualVz| for all64 drones and its arithmetic mean in ascending ID order. For each pair, intersect integer global control indices, then average each arm's per-update mean in increasing index order over that common set. Report both means, memory-minus-original, sample count, first/last indices and actual saved times. Include a due controller emitted before a later native refusal: it describes its saved current state, not an accepted trial endpoint. If no common samples exist report unavailable, never zero or invented data. Each arm has its own changing Boids reference; this is a descriptive whole-intervention comparison, not tracking of an identical target or an isolated aerodynamic mechanism. No statistical significance, population-rate, general-stability or optimality claim.

Retain per-update errors, memory extrema/words, commands, desired velocities, neighbors, physical states, all native inputs/evidence, consumed loads/derivatives, projected RK records, safety records and complete journal hashes. No raw rows may be discarded after outcomes. Retain branch noncoverage explicitly, including no-refusal or no-missing-suffix display paths when applicable.

## Stops and exclusive allocations

Stop a path at its first structured native domain/input/numerical refusal or inherited endpoint issue, preserve the record, then continue only to the remaining prescribed paths. Unexpected exceptions, malformed output, persistence or resource failure end the entire producer allocation. No replacement path, horizon extension, warmup, extra endpoint query, tuning or numerical retry. Unattempted paths remain unattempted. A failed allocation stays closed; repairs require a separately reviewed prospective protocol.

- Producer: maximum16,000 attempted native F calls/RK stages and4,000 completed steps; successful wall2,400s including cleanup, external termination2,420s;4GiB total result output with1MiB closure reserve;4MiB raw-record cap. Reuse the unchanged qualified journal's16MiB raw blocks and <=32MiB compressed parts; no new storage trial. These caps scale the prior12,000-call allocation to this four-path workload and are fixed before execution.
- Independent saved-evidence audit: one attempt, successful wall2,400s, external2,420s,128MiB output. Read every reached journal for all four new paths (four to eight journals); verify both controller target laws, memory recurrence where applicable, current-state/commands/load binding, projections, rigid-body/motor-lag derivatives and projected RK. Do not run native solvers, controllers, Boids, geometry or initializers. Exact exclusions and prior-source trust are in AUDIT-CONTRACT.md.
- Finalizer: one attempt, successful wall120s, external140s,2MiB output plus64KiB viewer pins. Requires closed passing producer/audit before pinning the export.
- Display: one attempt, successful wall150s, external160s,16MiB output; saved-data paired Three.js only. Check every displayed position/time buffer, actual outcomes, unavailable suffixes when present, selection/play/orbit/reset, desktop/mobile captures, corrupt-evidence refusal and page errors. No online numerical model.

Use exclusive launch locks and new output directories. Identity reads alone may retry up to three times before bytes are consumed; preserve every anomaly. No parsing/arithmetic rerun. Successful resource accounts are not speed benchmarks. Check no active research job overlaps and sufficient free storage exists before launch; do not delete historical evidence to make space.

## Admission and publication

Before execution: existing independent reviewer accepts source/protocol, exact dependency/source freeze, scoped privacy scan, public commit/push and separately independent exact-public source verification. The published prior transfer result motivates this question; it is not a newly computed comparator. No old trajectory or closed test is rerun.

Before publication: preserve raw evidence and all failures/anomalies, independent saved-result review, understandable summary, claims/literature ledgers, screenshots and Three.js replay, exact restart instructions, complete result-byte freeze, privacy check, public push and verification receipt. Keep localhost8876 available. No paid resources, installations, author contact or submissions. This study does not validate real aerodynamics, establish flight safety, invent integral control, demonstrate large-swarm scalability or finish the research goal.
