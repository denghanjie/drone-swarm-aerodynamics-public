# Prospective bounded vertical-memory diagnostic

21 October 2026. User-authorized computational continuation after the public nominal comparison. This is a new allocation; all earlier numerical, audit and display allocations remain closed.

## Question

Does one fixed bounded integral correction to the existing vertical-velocity request change the recorded floor-stop outcome while retaining the full current aerodynamic coupling? This is an outcome-motivated diagnostic on an exposed failing configuration, not a new controller invention, held-out confirmation, physical validation or a general success-rate experiment.

Use N=64 and seed 2026102001 only, in order h=0.005 then h=0.0025 s. Horizon 5 s, split exactly as the existing baseline: local 0..1 with origin 0, then local 0..4 with origin 1. Initial physical states must exactly match the corresponding previously saved original 64×17 words. Two paths are resolution checks of one selected configuration, not independent trials. The second historical seed is excluded prospectively to keep this first controller diagnostic and its raw evidence bounded; no inference about that configuration is permitted. Retain all historical results.

## One controller change

Keep original 3D local separation/alignment/cohesion, route guidance, obstacle filter, factory, physics parameters, actuator limits, motor lag, projected RK integration, full native F coupling, nominal reaction yaw and stopping rules. The controller sees only its own current states and desired Boids velocities. It does not observe or invert native loads.

For each drone separately, store integral acceleration I, previous vertical-velocity error e and update count, initially positive zero, positive zero and zero. At its first controller update I stays zero. At every later 0.01 s update use the previous sample: increment = (2.5 × 0.01) × e; unclamped = I + increment; I = max(-5,min(5,unclamped)). Compute the current e = desiredVz − actualVz and increment the update count. Construct the exact target expression `z + ((2.5*desiredVz + 1.5*actualVz) + I)/6`; pass this to unchanged F.control. The arithmetic grouping is fixed; do not simplify it algebraically in production or audit.

The gain is 2.5 s^-2: with inherited proportional coefficient 2.5 s^-1 this specifies a nominal P/I ratio of one second. The accumulator bound ±5 m/s² uses the magnitude of the inherited positive acceleration cap as a simple fixed bound, not a fitted or optimal choice. The inherited controller's net vertical command clamp is [-4,+5] m/s² and its motor mixer limits remain unchanged. Integral clamping is not saturation-aware anti-windup. Saturation may therefore limit recovery or cause undesirable transients; preserve that outcome instead of tuning after observation.

At t=1 save and bitwise serialize/reparse every physical word plus every controller integral/error word and count. Carry this path's own memory into the second segment; local controller index resets, global controller index continues at 100. Update the t=.99 error once at t=1. Reset memory only between the two independently evolving resolution paths. Native refusal retains the most recent emitted controller memory and last completed physical endpoint; it does not roll memory back. Physical state alone is no longer a complete restart state.

## Prespecified evidence and interpretation

Primary categorical observation: does each candidate reach 5 s without a structured native refusal or inherited endpoint contact/vehicle-limit stop? The saved original coupled counterparts stopped at 4.6200 and 4.6175 s. Reaching the horizon means only that these discrete checks passed in this finite simulation. A new native refusal is a recorded model-domain outcome, not a collision or improved safety.

Retain every initial/controller/stage/endpoint/safety/case-end record, all native inputs/evidence, consumed force/moment/derivative words, complete memory before/after, and all raw record hashes. Report attempted/successful stages and actual stopping category separately. The sole new arm is coupled plus vertical memory; the old coupled baseline is reused, never rerun. The published nominal result motivates this question but is not a third newly executed arm.

Compare candidate and old coupled positions only at integer steps available in both corresponding paths. Report last-common ID17 height, mean-height difference and maximum/RMS center separation, with each actual saved time. Report terminal heights/outcomes separately; never extrapolate a stopped suffix. Candidate same-seed coarse/fine position sensitivity uses common completed endpoints, with no convergence-order or physical-error-bound claim. Candidate controller error/integral statistics are descriptive own-reference quantities only: earlier baseline exports lack fleet tracking-error data, so do not claim matched fleet tracking improvement. Changed positions change neighbors and desired Boids velocities, so the total intervention includes downstream steering feedback.

Stop the current path at the first saved structured native domain/input/numerical refusal or inherited endpoint safety issue, retain it, then execute only the remaining prescribed path. Unexpected exception, malformed output, resource or persistence failure ends the entire allocation. No seeds, gains, bounds, horizons, tolerances or retries may be substituted after execution. No simulation warmup or extra endpoint native queries.

## Single-use allocations

- Producer: at most 12,000 native F calls and 12,000 attempted RK stages, 3,000 completed steps; successful wall limit 1,800 s including supervision cleanup, external termination at 1,820 s; total result output 3 GiB with 1 MiB closure reserve; raw record cap 4 MiB. Reuse the previously qualified Journal's unchanged lossless 16 MiB raw blocks / at most 32 MiB compressed parts. No storage trial is rerun.
- Independent saved-evidence audit: one allocation, successful wall 1,800 s, external termination 1,820 s, output 128 MiB. Reads all new raw records and checks native load/consumption/integration arithmetic and new memory arithmetic; never runs an aerodynamic solver or simulator. Detailed scope and exclusions are in AUDIT-CONTRACT.md. Prior coupled exports/audits are reused trust, except bounded original-initial prefix reads. No new baseline tracking extraction.
- Finalizer: one allocation, successful wall 120 s, external termination 140 s, output 2 MiB plus at most 64 KiB viewer pins. Requires closed passing producer and audit before pinning the replay export.
- Display: one allocation, successful wall 150 s, external termination 160 s, output 16 MiB; saved-data Three.js comparison only. Check every displayed position/time buffer, missing suffixes, case/time controls, playback, orbit/reset, desktop/mobile captures, corrupt-evidence refusal and page errors. No model runs in the viewer.

Each allocation has an exclusive launch lock and new output directory. A failed allocation stays closed; any repair requires a separately reviewed prospective protocol. Identity reads alone may retry up to three times before bytes are consumed, with anomalies retained. No parsing/arithmetic rerun. These wall budgets concern resource accounting, not speed measurements.

Before producer launch: independent protocol/source review, exact dependency manifest, privacy review, public commit/push and separate exact-public manifest verification. Before publication: independent result review, full byte freeze, privacy check, public push and exact-public receipt. Preserve understandable summary, claims/literature records, Three.js evidence and precise restart instructions. No real-flight, physical accuracy, novel control method, large-swarm scalability or overall completion claim. No installations, paid resources, author contact or submissions; keep localhost 8876 available.
