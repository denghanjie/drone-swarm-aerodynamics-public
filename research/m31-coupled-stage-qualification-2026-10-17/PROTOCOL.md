# Coupled-stage qualification: prospective protocol

## Status and authorization

The user explicitly approved a **new two-hour execution window** in this chat. Receipt was acknowledged against the clock at **2026-10-17 03:06:20 UTC**, with a fixed cutoff of **05:06:20 UTC** (11:06:20–13:06:20 Shanghai). The actual approval preceded that receipt; this uses the receipt as the recorded window start. Earlier expired allocations and evidence remain unchanged. No launch is authorized by this document alone: enabled pinned configuration, source publication verification and a full 960-second remaining reservation are required.

This allocation covers one qualification attempt, saved-evidence analysis, independent review and the associated recorded Three.js viewer. It does not authorize an unlimited campaign or a second scientific invocation after failure. New hypotheses require separate prospective protocols within the approved scope and remaining time. No paid services or external paper submission.

`PROTOCOL-DRAFT.md` and the implementation/supervision preparation notes preserve the earlier disabled drafting state. This document and the final execution configuration supersede their statements about whether a new window has been approved. They do not retroactively change earlier execution conditions.

## Plain-language question

Can we connect the aerodynamic calculation to the flight calculation without mixing up drones, forces, coordinate frames or time steps? A force can be calculated accurately yet applied incorrectly. We first check simple motions whose answers we know, then check every force consumed in a short continuation of 64 drones using local 3D Boids.

This is an implementation qualification, not physical validation, a new flocking result or a speed benchmark. The eight-step roadmap remains in place: interaction/flight verification supports Steps 3–6; 5,000-drone coupled scaling in Step 7 and a publication contribution in Step 8 remain unresolved. Earlier 16-drone coupling already exists; this is not first-ever coupling.

## Fixed experiment

- Start from the entire previously exposed `fresh-a-t5` state: 64 stable IDs, 17 binary64 state words per drone, original time 5 seconds. The science configuration pins its exact bytes. There is no new initialization, seed search, subset selection or held-out claim.
- Continue for **0.02 seconds**, with eight projected synchronous RK steps of 0.0025 seconds and four stages per step. Run one coupled arm and one matched aerodynamic-off arm.
- The coupled arm makes exactly **32 native F load queries**. Independently evaluate the exact reference on those same 32 consumed states. The off arm has 32 derivative stages and no native aerodynamic query.
- Local separation, alignment and cohesion, shared broad route guidance, wide factory, wall-priority steering, motor lag and nominal actuator states remain inherited. Update the controller at relative times 0 and 0.01 seconds; the second update must read the evolved state.
- Preserve raw and projected stage states, IDs, commands, exact delivered and consumed words, derivatives, endpoints, safety records and input sidecars. Both fixed arms may retain their own failure record; no replacement input or retry is permitted. Scientific qualification requires both complete arms and all later checks.

## Numerical contract

Project the quaternion before every stage and once at each accepted endpoint. The normalization uses a left-associated sum of four rounded squares, `Math.sqrt`, then four divisions. This explicitly differs from the old adapter's `Math.hypot` expression. Independently check the square root's rounding cell and the projection arithmetic. Save a single raw first-k2 quaternion norm diagnostic; it is not a full domain-admission test and triggers no alternate solve.

Replace the nominal total world force and thrust-arm moment exactly once. Transform the world moment into body coordinates once. Keep gravity separate and retain the provisional **nominal motor reaction-yaw law** and nominal motor-state lag. The aerodynamic moment excludes reaction yaw. Do not add a total load as an extra disturbance or overwrite nominal motor states with effective loads.

Keep the exact-reference recipe unchanged: 192-bit coefficient/source intervals, 128 root bisections, maxDrones 180, at most 30,000 suffix calls per stage. The 32 complete states have 516,096 logical rotor/source pairs. No unresolved or refused reference state can pass. Numerical bounds must include reference uncertainty and pass each of four limits: maximum rotor error/(mg/4), collective error/mg, Euclidean world-force error/mg and Euclidean world-arm-moment error/(mgR), all at most **1e-8**. The checker also bounds the body-frame moment conversion.

Native input and actual delivered/consumed associations are compared as literal words. Independent derivative/RK arithmetic uses exact rational reconstruction of binary64 operations; it identifies positive and negative zero numerically. Therefore this is not a proof of every signed-zero derivative bit. No independent transcendental oracle for the Boids/controller is claimed: controller source provenance and actual input/output consumption are checked.

## Controls fixed before observation

The science configuration names 12 wiring controls: five accepted groups and seven rejected groups, with six successful single-drone derivative consumptions. These include no extra force, tilted unequal loads, nominal yaw, motor lag, ID permutation, duplicate/missing IDs, stale stage/input and invalid load/quaternion cases. They call no native aerodynamic solver.

Three manufactured motions—translation, principal-axis spin and motor relaxation—run over 0.01 seconds at h=0.0025, 0.00125 and 0.000625. This is nine runs, **84 steps and 336 stages**. Their prescribed force and moment isolate the integrator; they are not a native aerodynamic law. The independent checker uses fixed 40-term rational series enclosures for sine, cosine and exponential.

Acceptance on the finest grid: position, velocity and angular velocity Euclidean errors ≤2e-12 in their respective SI units; quaternion chord attitude proxy ≤2e-10; maximum motor error normalized by mg/4 ≤1e-8. Each refinement must reduce error by at least half unless below the fixed 1e-12 floor. The independent interval decision uses upper errors against lower coarse-error bounds; ambiguous decisions fail. All errors remain saved. These are qualification thresholds, not evidence of an observed convergence order.

The checker additionally applies ten fixed corruptions to saved evidence: load word, squared force law, body-frame force, load ID, doubled force, missing moment, wrong frame, overwritten motor state, stale stage and consumed ID. No scientific producer or reference rerun is needed. Require an observed nonzero load change, its propagation into the state and a subsequent changed controller command; otherwise feedback qualification remains unresolved.

## Resources and stopping

One supervised attempt reserves **960 seconds** from entry: browser 120, reference 600, checker 180 and shared overhead/closure 60. Reference/check computation reserve their own finalization time inside their allocations. Full reservation must fit before the UTC cutoff. Failure is terminal for this attempt; partial output is evidence, not permission to rerun.

Cap individual files at 32 MiB, journal records at 2 MiB and all new output/private logs/profile/scratch at 256 MiB including the finalization allowance. Source packaging does not evaluate scientific factories. Selected runtime bytes are pinned; the running Chrome product must match. Keep server 8876 unchanged.

Process ownership, deadlines and disk checks follow `SUPERVISION.md`. Memory readings are process-lifetime observations, not OS limits or aggregate browser-tree measurements. There is no memory-performance acceptance claim in this qualification. Shutdown confirms the owned controller and Chrome root, not every helper under arbitrary OS failure. The supervisor timestamp excludes final report writing and process exit; do not present it as exact end-to-end exited-process timing.

## Interpretation and record

Hypothesis: the strict native loads can be correctly consumed throughout this continuation. Supported numerical qualification requires all declared checks, complete raw evidence and independent review. A failed check supports only the recorded failure and its diagnosed cause; it does not establish physical impossibility.

The model remains hypothetical: directed axial loads, no wake memory, no newly validated upper-drone response and provisional reaction yaw. Numerical agreement does not establish measured aerodynamic accuracy, continuous-time trajectory accuracy, mission safety, robustness, real-time performance or novelty. Retain the physical-domain review in `m31-upper-response-admission-2026-10-17` and its verified literature ledger.

Publish source before execution and preserve an exact source-commit receipt. After execution, publish raw outputs, failures, independent interpretation, claim/literature ledger updates, a digestible milestone summary and restart instructions. Show actual saved states in a Three.js replay, explicitly label its 0.02-second duration and any slowdown/interpolation. A replay supplies no real-time simulation evidence.
