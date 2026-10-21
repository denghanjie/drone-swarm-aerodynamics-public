# Matched nominal-load comparison

21 October 2026, Asia/Shanghai. Computational-only. User requested continuation. All earlier allocations remain closed. This package is source-only until independent review, exact source freeze, public push and separate public-source verification. It opens no expired overnight window.

## Question and meaning

Does replacing the implemented coupled aerodynamic loads with nominal rotor loads alter the previously observed descent or floor stopping outcome of the exact two N64 initial configurations? Earlier off/on work exists; this is a targeted diagnostic in an exposed workload, not a novel algorithm or held-out validation. See HISTORICAL-CHECK.md. The intervention estimates the total effect of the implemented coupling, including subsequent changes in neighbors and steering. It does not isolate a direct force-only effect, prove the aerodynamic law, establish real-flight safety, or find the best controller.

## Fixed comparison

Use seeds 2026102001 and 2026102002, each with h=.005 then .0025 seconds, 64 vehicles, fixed total horizon5seconds. Regenerate each initial state once with the identical pinned initializer and check every one of its 64x17 saved words against the original journal in the independent audit. No alternative seed, parameter tuning, replacement path or rerun. The two resolutions are dependent checks, not independent trials.

Only the new nominal arm runs. Use the existing projected synchronous RK adapter's builtin `off` branch. Its nominal world force and arm moment come from the four current motor states and saved orientation; it retains nominal reaction yaw. No native airflow solver is loaded or queried. A forbidden-call stub throws if that contract is violated. Local 3D Boids, wide factory, wall-priority filtering, vehicle parameters, controller, motor lag, nominal yaw and stopping rules are unchanged. The off state evolves independently, so later steering need not match coupled commands.

Preserve the published baseline's two-segment clock semantics: local0..1 and local0..4 with timeOrigin1 for the second segment. At the boundary pass all17state words without another normalization; commands are recalculated because a controller update is due. There is no initialization at this boundary. Both segments use their local integer step indices for the inherited arithmetic. Save each segment separately; no second segment if the first stops. A horizon/stop endpoint has no newly computed force.

Reuse the existing audited original and continuation coupled endpoint exports, result indices, audits, closure files, manifests and publication receipts. Do not rerun the coupled arm. The old first journal parts supply initial-state verification; no new full baseline arithmetic audit is allocated. The coupled export's previous independent verification is reused trust. Match comparisons by discrete global step index, while preserving each actual saved time label. After one arm stops, do not extrapolate, hold its final position as continuing flight, or call later off-only motion a matched comparison.

## Fixed observations and stopping rules

Report each arm's status, horizon, recorded stop reason, off stopping identities, mean initial-to-final vertical displacement, and drone17's final height/vertical velocity when saved. Compare last common saved endpoint positions: maximum and RMS drone-center separation, mean-height difference, ID17height difference. Also report each off same-seed coarse/fine maximum center discrepancy over common completed endpoints, as resolution sensitivity only. No continuous event-time or convergence-order inference. The shared stopped prefix and missing suffix stay explicit. No population success probability from two seeds.

Each path stops at the first inherited endpoint vehicle/contact issue, retaining the stopping step and all issues, then proceeds to the next prescribed path. Unexpected arithmetic, persistence, resource or malformed-output failure stops the entire allocation. Off paths have no native-domain admission test; completing them cannot show that coupled airflow supports those states. No bypassed aerodynamic-domain refusal is a physical success.

## Finite allocations

Producer: one attempt, success wall<=1200seconds including supervisor cleanup, external deadline1220seconds; at most6000steps and24000derivative stages across four paths; zero native calls. At most2GiB result files, reserve1MiB for closure, max4MiB raw JSON line. Use the unchanged previously qualified lossless Journal:16MiB uncompressed blocks,32MiB compressed parts. Reuse its published passing storage qualification and source identity; no duplicate storage allocation. Every initial, control, stage, step, safety and case-end record is saved, with exact state/command/load/derivative words and aggregate raw/compressed hashes. Buffered records may be lost on unexpected failure; that remains an incomplete failed allocation.

Audit: one independent saved-evidence attempt,1200seconds success/1220external,128MiB output. No initialization, controller or contact-geometry regeneration. Verify exact source and producer closure, initial/boundary state equality, all schedules/bindings and declared projected-RK/nominal-load/derivative arithmetic, every journal hash, stopping linkage, descriptors and export. AUDIT-CONTRACT.md defines reused helpers and numerical tolerances. Passing arithmetic is not physical validation.

Finalization: one byte-only allocation,120seconds success/140external,2MiB output plus64KiB viewer pins. It binds the passing audit/export and supervisor evidence, without new arithmetic or model calls.

Display: one allocation,150seconds success/160external,16MiB output. The Three.js page replays saved endpoints only. Check both arm buffers, unequal stopping times and no fabricated suffix, floor/ID17, controls, orbit/reset, desktop/mobile captures, page errors and corrupt-evidence refusal. Browser plugin absent; use existing Playwright. No install. A failed allocation closes and is preserved; any repair needs a separate reviewed source and prospective allocation.

## Identity, records and claims

Exact manifest pins all sources/config/runtime identity records, dependencies, baseline exports and four original first journal parts. Source is immutable after freeze. File-identity reads allow up to3 attempts per independent operation only when bytes mismatch or I/O fails; record each anomaly. Gate-before, evidence read and gate-after are separate byte operations. No scientific calculation, audit, browser or allocation retries are implied. Scientific numeric failures never use these byte retries.

Before science require existing independent review, public source commit and independently fetched exact public manifest. Before audit require complete passed producer closure. Before finalization require passed audit closure. Before display require frozen viewer pins. Preserve raw failures, reviewer notes, citations/access scope, claim ledger, understandable summary, screenshots and restart instructions. Privacy-check, commit/push, verify exact public results and receipt. Keep localhost8876. No paid resources, installs, contact or submission. Overall research remains unfinished regardless of this result.
