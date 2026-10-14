# Independent static physics/numerics review

Status: FINAL STATIC REVIEW. The file-specific disposition and digests are recorded in `REVIEW-OUTCOME.json`. No model evaluation, integration, replay, fixture, numerical test, or numerical array interpretation was performed by this reviewer. Source/document reads, byte comparisons, and primary-source consultation only. This is not execution approval or a numerical-reference claim. The coordinator must adopt and hash-freeze the complete reviewed implementation before any numerical execution.

## Findings available now

The proposed target is a legitimate *candidate numerical experiment* for the frozen equations. On exact unit-quaternion states, evaluating the frozen full swarm field on a geometry-only normalized copy leaves the field unchanged. Passing the raw stage state to the frozen aerodynamic derivative also leaves the prescribed on-manifold derivative unchanged. This does not validate the physical model or establish fourth-order accuracy.

The inspected initial `joint-step.cjs` constructs each complete swarm stage before the corresponding full field call. It then evaluates every vehicle derivative from that one stage state and field, keeping commands fixed. This is the required coupled-stage distinction. The copied `snapshot/` tree and `src/exact-aero.cjs`/`src/source.cjs` were byte-identical to the recovered source at inspection (recursive `diff` and `cmp`, no source execution).

In the first `branch-audit.cjs` draft, this review identified:

1. Signed-margin retention kept only nearest-to-zero margins, rather than minimum, maximum, and nearest with identities.
2. Selected J branch/risk evidence saved normalized geometry states but omitted raw RK trial inputs.
3. The `downstreamZero` sign used `down >= 0`, whereas the actual field skips `down <= 0`. Exact predicate equality needs consistent treatment.
4. Separate endpoint-only and full-trial finite-jump flags had not yet been implemented.

These findings were sent directly to the implementation worker and coordinator. All four were corrected and statically re-read. Signed minimum, maximum, and nearest margins now cover every pair and all drones' tilt margins. Selected J brackets preserve both geometry and raw trial input. The exact downstream predicate is documented. The range audit retains distinct endpoint and full-trial flags, endpoint flagged-pair IDs, sample roles, and coverage counts; it includes stage 1 as well as both half-stage trials, stage 4, and accepted endpoints.

## Same-equation and model scope

- Frozen `snapshot/outputs/step02c-source/physics.cjs:18` uses quaternion derivative `0.5*q*[omega,0]`; in exact arithmetic its inner product with q is zero, so the unit manifold is invariant. The proposed extension is meaningful in a neighborhood with nonzero finite quaternion norm.
- Frozen `snapshot/outputs/milestone-28-source/aero.cjs:18` computes receiver effective rotor thrusts, restores nominal yaw torque, and restores the original first-order nominal-motor ODE. These choices remain part of the target, including its limitations.
- Frozen `src/exact-aero.cjs:10–12,89–103` fixes source strength from mass/hover geometry; it does not use source motor thrust. Normalizing source/receiver attitude geometry does not authorize changing source strength, receiver inversion, fades, or source order.
- Frozen `src/exact-aero.cjs:31–49` requires finite full17 states, bounded coordinates, unit quaternions, and the 20-degree source/receiver tilt bound. Geometry-copy normalization must reject zero/nonfinite norms before division; it must never overwrite raw derivatives' stage states.
- Frozen `src/exact-aero.cjs:92–102` has a possible finite positive jump at the lower far-field switch in the narrow radial interval `[0.15, 0.15152108978535467)` m. The upper value is the previously documented arithmetic from frozen constants, not a newly evaluated path finding. The cubic fades are C1 at joins, not globally C4. Neither source inspection nor sampled non-crossing establishes continuous-path regularity.

## Hybrid controller and baseline fairness

- `src/coupled.cjs:25–28` refreshes held field, then controller when due, then independently integrates each vehicle. H/P must retain `M.integrate` byte-identically, including its zero-inflow shortcut and endpoint normalization arithmetic; no opportunistic correction is allowed.
- Frozen `snapshot/outputs/milestone-31-source/sim.cjs:9–25` supplies local 3D separation, alignment/cohesion, common route guidance, pair constraints, six projection sweeps, and wall-priority repair. All rows must run this from their own states. Diagnostic recomputation cannot become command replay or feed back.
- New `controller.cjs:7–10` initially calls the frozen `B.steer` and `F.control` with the original reference conversion and thrust ratio. Adding a diagnostic callback is observational: the callback does not change the returned velocity.
- At controller boundaries, J k4 belongs to the preceding left-command interval. No new command is applied until the following step. No controller or held-field production event occurs at final T; a J k4 field call at T remains legitimate and separately counted.
- H/P and saved-path branch audits must use the actual accepted input quaternion without extra normalization. J uses its geometry copy. An additional normalization of H input can change tiny boundary margins relative to the frozen authoritative field.
- Controller logs need actual commands, not only quaternion sign labels. A quaternion representation sign flip need not change physical commands. Constraint membership must be described as eligible/generated unless actual projection activation is separately instrumented; final-speed proximity alone is not a complete internal limiter branch trace.

## Acceptance and evidence review criteria

The prospective 0.6 joint and 0.7 cross-family reduction factors, four absolute caps, and numerical floors are analyst-defined screens. No paper supplies those drone tolerances. Per-seed/per-observable maxima over exact common endpoints, including T, must be kept without time shifting, averaging seeds, or relabeling vehicles. The old normalized-dot/acos attitude comparator remains primary; an atan2 relative-quaternion diagnostic is secondary. A two-level H4/P1 check is not an order estimate. Even all prescribed passes establish only a bounded, cross-checked numerical reference for two one-second diagnostic windows and the frozen model.

Finite-jump checks must include every ordered receiver-rotor/source pair on old endpoint brackets and on new J/H/P step samples. J equal-time half-stage states are numerical trials, not ordered physical observations. The conservative downstream-range/radial-range test can flag false positives; any candidate is a retained inconclusive stop, not an excuse to smooth or interpolate a replacement path. Separate endpoint-only and full-trial candidate records are mandatory. A no-flag result cannot rule out unsampled crossings.

Required selected evidence includes actual whole-swarm raw J trial states, normalized geometry copies, location/role/tick, held commands, field if available, derivative if available, and exact guard. Ordinary stage hashes are integrity evidence only. All failures, skips, and last-durable-versus-exact-state distinctions must survive resource stops.

The coordinator prospectively adopted `RETENTION-CLARIFICATION-002.json`: the frozen H/P integrator has no internal-stage exception hook. An unexpected exception inside it retains the exact pre-step input, held winds/commands, and vehicle ID, with `exactIntegratorInput=true`, `exactStoppedState=false`, and the hidden stage explicitly unavailable. It must halt and withhold reference acceptance. No replay or baseline alteration may fabricate that stage. J retains raw stage and raw combined-endpoint projection failures. The active plan hash after this clarification is `b68a2a93b29e85b3784d874010c767ee7ba3eacfdcc71d4bb6b91d31606d4bba`; the previous storage-amended plan is preserved. This is an honest evidence limitation rather than a changed physical/numerical target.

## Retention and cost

The baseline is 131,223,856 bytes for retained historical transport parts, decompressed historical arrays, and new state arrays, before other metadata. The initial 150,000,000-byte cap left only 18,776,144 bytes, including a 2,000,000-byte failure reserve. Before any numerical execution, the coordinator adopted a storage-only increase to 200,000,000 bytes in `STORAGE-AMENDMENT-001.json`, leaving 68,776,144 bytes including the unchanged reserve. The coordinator explicitly confirmed that 150 MB was coordinator-proposed rather than a user-imposed limit; the user authorized bounded autonomous research without paid compute. Current plan hash `4dfd2234c5aeafc2fd0fb23427e9cddc77d504196e0d83387a7bfc0fe16e271a` and preserved initial plan hash `26588970eb3d6aa0e984dfeffe23e94e32d26622daef551138051b374efcadaa` were independently checked. Time caps, model, seeds, gates, and failure reserve did not change. This prospective evidence-retention amendment creates no physics/fairness objection.

A per-sample raw 32-byte hash stream is substantially safer than JSON hex strings. Retain margin extrema and first/worst category brackets rather than full margin histories, as prospectively agreed. All required margins are still evaluated at all required samples.

The first controller implementation retained full constraint objects, residuals, repeated commands, and pretty-printed JSON for every control event. That static storage risk has been addressed by a compact 18-Float64-per-drone controller record, including exact bit masks for neighbor/constraint memberships, actual commands, and diagnostic scalars. No overrun was measured. A complete serialization forecast must still cover every artifact and bounded temporary/atomic-write allocation before freeze. Compact required values/IDs or binary records are acceptable when their encoding, role schedule, and reconstruction limits are explicit. The budget may not be extended or important diagnostics silently dropped after an outcome is known.

## Primary sources independently reopened for this review

Consulted 2026-10-13. These are methodological/model-provenance sources only; no associated code or dataset was run. No new exhaustive correction/retraction search was performed in this audit.

1. Hairer, author-hosted preprint dated 25 May 1999, Section 1, pages 1–2, equations 1.1–1.2 and ordinary projection discussion. It assumes sufficient differentiability, explains the need for an off-manifold vector-field extension, and distinguishes ordinary projection from the paper's symmetric method. This plan uses ordinary endpoint normalization. https://www.unige.ch/~hairer/preprints/symproj.pdf
2. Nordam and Duran (2020), Sections 2.1–2.2, equations 5–9; Section 3.1; Section 3.3. RK stages evaluate stage-state right-hand sides; smoothness assumptions and event treatment matter for accuracy. The paper separates numerical work-precision comparisons from physical prediction. https://gmd.copernicus.org/articles/13/5935/2020/
3. Mørk, Nordam and Rühs (2025), Section 3.2, equation 5 and dense-output/event-location discussion; Appendix C, equation C1. Spatial boundary crossing detection and localization are different tasks; numerical-reference refinement is finite-precision limited. The present plan deliberately stops on unresolved candidates and does not import their event-location method. https://gmd.copernicus.org/articles/18/7831/2025/gmd-18-7831-2025.html
4. Bauersfeld et al., arXiv 2403.13321v3, Section VI-C, explicit time-averaged far-field recipe; Section VII-A, equations 10–11; Section VIII. The hover-power compensation relation and mean wake support provenance only. They do not independently validate this simulator's transient receiver-thrust inversion, finite-support modifications, multiwake summation, 27 g vehicle, or controller. https://arxiv.org/html/2403.13321v3

## Final disposition

No unresolved physics/numerical-design blocker was identified in the final reviewed source once the corrections below were applied. This is a static-review pass for the candidate, conditional on the coordinator's complete freeze and the independent robustness review. It does not say the fixtures pass, the numerical window will finish, or a reference has been established.

Additional corrections from this review:

- `src/run.cjs:9,27` gives the 128-base-tick historical compatibility row its own endpoint output cadence. The first draft would have rejected it by demanding divisibility into the ordinary 32-tick common grid.
- `src/compare.cjs:4–7` now rejects empty or incomplete equal-length data: each canonical comparison requires 1,601 common records, 16 drones, 32-tick cadence, and final tick 51,200. Primary normalized-dot/acos attitude arithmetic remains the historical formula; the relative-quaternion atan2 expression is a separately named diagnostic. Maxima retain indices even when the value is zero.
- `src/campaign.cjs:29–35` maps the immutable historical grid explicitly and compares actual preflight controller outputs with H1. This comparison is diagnostic, not a whole-trajectory equality gate; exact command hashes are required only when re-evaluating the identical saved historical state.
- `src/joint-step.cjs:44–47` retains failed raw combined endpoints separately from k4 trial states. Stage error evidence includes available geometry, field, derivative, commands, and original guard.
- `src/run.cjs:35–42` counts J derivative attempts/completions at each actual callback, including partial steps. H counts completed vehicle integrators and clearly labels the four-per-attempt derivative upper bound. Quaternion norm/projection maxima include tick/stage/drone identities.
- `src/run.cjs:54–58` no longer presents J's unused zero held-wind placeholder as final airflow. J has no claimed accepted-endpoint final field value. Timing scope distinguishes numerical-loop time from serialization and authoritative scheduler total job time.
- `src/campaign.cjs:14` scientific gate success is provisional and requires supervisor validity. A complete-looking inner report alone must not qualify a killed or resource-exhausted campaign.
- `src/campaign.cjs:2,9` rejects the environment-controlled narrow factory variant and checks the frozen wide course identity. Initial-state identity alone would not have guaranteed course identity.

The actual controller scheduler was additionally covered by a newly authored, deferred synthetic-stub fixture in `robustness-review/test_runner_clock.cjs`: it exercises `run.cjs` for event count, old commands through the preceding boundary step, new commands in the following step, exact common record count, and no terminal discrete update. `test_branch_boundaries.cjs` covers lower/outer annulus equalities and same-half-time trial straddles with endpoint flags kept separate. The independent tests also cover synchronized stages, copy nonmutation, invalid geometry, and raw projection failure retention. These fixtures were inspected as text only by this reviewer; their outcomes remain unobserved until the frozen supervised window.

Resource details, atomic-write faults, external watchdogs, process accounting, and interruption inventory are assigned to the independent robustness review. Its conservative static storage envelope is 191,713,040 bytes under the adopted 200,000,000-byte cap, including reserve and temporary/interrupted-write allowances; this is a forecast, not a measured run. The exact signature total is 278,819 observations or 8,922,208 bytes, including preflight and compatibility. Any stricter independent robustness blocker still prevents freeze.

No numerical or physical-validation finding has been made in this audit. All interpretation limits above remain mandatory after any eventual successful run.
