# Source review: first integration diagnostic, then conditional feedback

2026-10-16. **Conditionally adopt the revised small design.** The primary experiment is a fixed nominal-command pair integration check, not closed-loop flight. The six exploratory Boids paths address feedback only after all eighteen primary paths pass the gates below. This review read existing source/protocols only: no source acquisition, candidate import, model evaluation, target rescoring, numerical experiment, or repository edit occurred. It grants no execution allocation and reopens no earlier allowance.

## Freeze the revised scope

Use three pair cases, each for exactly0.5s, with airflow off/on and dt `.005,.0025,.00125`: (1) side-by-side separation4m with zero influence; (2) centered vertical separation0.6m; (3) vertical separation0.6m with the upper vehicle offset `+0.04m` in world x. This replaces the original up-to5s hover-controller proposal. Initial velocities/body rates are zero, quaternions identity, and all four nominal rotor states and held inputs are `mg/4`. Freeze exact full coordinates, IDs, ordering and contact environment; heights alone are insufficient. A common x origin at−6m keeps these fixtures away from factory partitions; state explicitly whether the same factory contact envelope is used. These are chosen synthetic fixtures, not physically calibrated encounters.

The primary offset pair tests the force/moment adapter while nominal motor states remain constant. `u=mg/4` is a simulator input, not a measured PWM setting or an established shaft/ideal-power control. Do not describe the falling/tilting fixed-command pair as a stabilized hover. The original controller has horizontal **velocity** targets and altitude, not x/y position hold; adding position restoration would be another intervention.

Only after every primary path completes and passes identity, symmetry/wrench bookkeeping, admission and numerical-resolution gates may the unchanged16-vehicle Boids initialization, seed260201, execute for2s, off/on at all three dt values. Generate that one initial full17-state array once and reuse identical bytes across its six paths. Keep original broad route, grid search, controller, wall-priority filter, gains and held-command cadence `.01s`; no controller tuning or replacement seed. Record the feedback arm as provisional because its nominal-state-to-effective-load relation is now used while nominal motor states change.

Total scheduled paths:18primary plus6conditional exploratory, all in one fresh candidate invocation. A primary gate failure marks the exploratory paths unexecuted, not zero-error successes. Retain failures and completed prefixes; no time, seed, dt, condition or method substitution. Primary paths must all reach0.5s and exploratory paths2s for their respective full-window convergence claims. Common-prefix differences after a failure may be descriptive only and cannot rescue a failed case.

## Adapter contract that must be explicit

For rotor r at body coordinates `(x_r,y_r,0)`, let `delta_r=T_effective,r−f0_r`. Starting from the original derivative evaluated with the same stage quaternion, add exactly

```
delta_F_world = R(q) [0,0,sum_r delta_r]
delta_tau_body = [sum_r y_r*delta_r, -sum_r x_r*delta_r, 0]
delta_vdot = delta_F_world / m
delta_omegadot = [delta_tau_x/Ix, delta_tau_y/Iy, 0]
```

The original derivative already contains nominal thrust, gravity, rigid-body gyroscopic coupling and nominal yaw torque. Do not add full effective thrust on top of it, rotate body torque into the world frame, treat force as acceleration, or pass effective forces into `wrench()` without suppressing its yaw change. The correction adds no yaw torque. Keeping the original motor-state yaw torque is an explicit extra assumption because the receiver closure supplies axial force, not motor reaction torque. This is not a complete aerodynamic wrench model.

Motor lag remains `(u_r−f0_r)/motorTau`; neither its state nor command becomes `T_effective`. Source strength must use the effective totals from the same stage's complete coupled solution, as the existing kernel defines. A previous-stage amplitude, previous-step matrix, sequential per-vehicle update or stale geometry would be a different model/integrator.

The model is an instantaneous, quasi-steady, pose-based extension: it omits wake transport/history and receiver/source translational-velocity corrections. Original motor lag does not model those aerodynamic delays. Existing source-field, command bridge, aggregation and scale assumptions remain unqualified physically. Feedback can expose behavior of those assumptions, not establish their physical validity.

## Global RK4 and controls

Write the numerical map precisely: form each complete raw stage array from the same accepted `Y_n` and the preceding global slope; make a fresh normalized-quaternion copy `P(Y_stage)`; use that **same** copy for geometry, loads and the original derivative. Evaluate all vehicle slopes before forming the next stage. Combine slopes with the usual RK4 weights from `Y_n`, then normalize final quaternions. Preserve input arrays and completed stage witnesses. Reject nonfinite/zero quaternion norms before projection and save pre-projection norm deviations; normalization must not silently erase an invalid state.

This projected stage method differs from original `F.integrate`, which normalizes only the final quaternion. Use the identical projected global adapter for off and on. Off/on agreement in the no-influence case verifies the toggle/adapter; it does **not** prove bit-identical original M31 integration or formal fourth-order convergence of this projected method.

Use integer counters for control and output events: all three dt values divide `.01s` and `.1s`. Recompute the controller synchronously from accepted states at control ticks, then hold its inputs through all four stages, including k4 at a tick boundary. The new command applies on the next step. Do not recompute control at RK substages or give one vehicle a newly updated neighbor state.

At each shared `.1s` observation, obtain effective forces from the **accepted endpoint state**. k4 is evaluated at `Y_n+h*k3`, not at the final weighted state; its forces are not endpoint forces. Freeze and count these diagnostic load queries, including t0 and terminal samples. Off-arm applied rotor force is its nominal state. Record residual/admission for each actual on-arm stage and endpoint query. An admissible final stage cannot excuse an inadmissible intermediate stage.

Any unsupported near-field, invalid term, nonpositive nominal state, scaled-cap violation, failed closure/residual, or descending-order failure rejects the case. Do not switch to another schedule, omit a source, clamp a force, or substitute zero flow. Record case/treatment/dt, step, stage, attempted time, last accepted state, command, geometry/admission/census, and the first failing data. A stage-domain rejection time is not a physical collision time.

Preserve finite-state, ground/body/contact checks. Separate accepted-step/segment contact events from internal-stage envelope failures. The existing swept chord checks do not prove continuous curved-path collision freedom. Record control saturation, filter activity and topology/branch changes to help interpret nonsmooth behavior; these are not automatic excuses to delete discrepant samples.

## Proposed numerical gates before execution

For each case and each treatment separately, compare matching vehicle IDs at **all** shared `.1s` times, including both endpoints. Define `E_coarse=max distance(dt=.005,dt=.0025)` and `E_fine=max distance(dt=.0025,dt=.00125)`. Use maxima over time and vehicles; for force, over rotors too. Do not pool vehicles/cases into an average that hides a failing one.

| Observable | Distance | Proposed resolution target epsilon |
|---|---|---|
| Position | Euclidean world-position difference |0.001m|
| Velocity | Euclidean world-velocity difference |0.001m/s|
| Attitude | Sign-invariant quaternion geodesic angle |0.1degree|
| Effective rotor force | Absolute difference divided by the fixed `mg/4` scale |0.001|

Require `E_fine<=epsilon` and `E_fine<=0.75*E_coarse`. Exempt the reduction test only when **both** errors are below `0.01*epsilon`, reporting “below comparison floor,” not an estimated order. Evaluate the inequality directly, so a zero denominator cannot produce an automatic ratio pass. The rotation metric should use a normalized relative quaternion and `2*atan2(norm(vector),abs(scalar))`; Euler differences and raw quaternion subtraction are unsuitable near wraps or sign flips.

These thresholds are prospective numerical preferences, not measured sensor precision, physical accuracy, safety margins or application adequacy. Three dt levels are not an extrapolated truth or proof of an asymptotic regime. Fourth-order factors are not required: controller clipping, filtering and support changes can reduce observed order. A failed gate means the selected sampled resolution has not been established, not that the physical model or RK4 is disproved. Do not adjust thresholds or add a finer dt after seeing results.

The `.1s` metrics remain sampled maxima. Preserve per-step/stage records and failure checks so between-sample problems remain visible; passing these sampled gates does not bound continuous-time error. Report full17-state finiteness and nominal-motor/body-rate differences as diagnostics even though they are not additional primary resolution thresholds.

Additional primary witnesses, fixed prospectively:

- **No influence:** on-arm CSR is empty, all alpha values0, `x=y=1`, effective equals nominal force and corrections vanish. On/off full17 states should match exactly if both use the same zero-correction arithmetic path. If exactness is not chosen in source, freeze a maximum component discrepancy `1e-12` in each component's SI/native unit and force discrepancy `1e-12*(mg/4)` before execution; do not choose between tests afterward.
- **Centered pair, initial state:** upper vehicle has zero inflow; lower four effective rotor forces are equal and initial roll/pitch correction is zero within the frozen arithmetic tolerance. This checks rotor labels and signs without claiming a measured force magnitude.
- **Positive-x offset pair, initial state:** symmetry across y requires equal paired rotor forces and zero roll correction. The nearer positive-x receiver rotors have stronger downwash/lower effective force than their negative-x counterparts, giving positive pitch correction with the existing rotor convention. Freeze the offset sign and IDs. These are implications of the admitted radial model, not expected observations from hardware.

For the on/off response itself, retain differences separately from dt errors. A finest-grid effect comparable to its on/off discretization differences is numerically unresolved. If reporting an effect larger than those differences, state the actual ratio; observed dt differences are not rigorous error bars. Do not require the hypothetical airflow to improve tracking, separation or safety.

## Concise independent saved-only checker specification

Interface: `python source/review.py PACKAGE OUTPUT_JSON`, in one newly allocated review invocation. The initial review suggestion was algebra-only. The final prospective protocol explicitly adopts a broader independent check at saved endpoints and the fixed first/planned-terminal captured RK stage states: it may rebuild geometry and solve the pinned independent model for those exact saved states. No candidate import, trajectory/controller rerun, new target input, adaptive stage reconstruction by reintegration, or historical target rescoring is permitted. Saved-slope RK4 assembly and saved-trajectory metric calculations remain within scope. Independent root recomputation is restricted to those already saved endpoint and selected-stage states; it is an implementation check, not new scenarios, new trajectory evidence or physical validation.

Save one immutable full17-state initialization per case; exact source/config/runtime pins; the fixed24-path schedule and gating status; per-path shared accepted states/commands, output forces and sample times; and complete stage witnesses for the prospectively fixed first and planned terminal step of each complete path plus the first failure context. A useful witness is the actual raw and normalized stage state sent to the derivative, stored slope, held command, nominal/effective rotor forces, alpha/x/source amplitude, correction wrench and closure/residual/admission summary. Keeping these selected steps fits the small evidence scope better than claiming an independent audit of every unsaved stage. Save complete symbols/CSR at the prospectively fixed initial/shared observations and first failure; do not require enormous full CSR tensors for every stage merely to reconstruct a new experiment in the reviewer. Freeze byte shapes and the exact witness coverage before execution.

The independent checker should:

1. Verify hashes, shapes, IDs, unchanged shared initial states, event times, exact path coverage and stage counts, control hold intervals, source/parameter identity, failure-prefix semantics and invocation/resource closure. Confirm exploratory execution only follows passing primary gates.
2. For each retained step witness, reconstruct raw RK stages and the final weighted combination **from the saved accepted state and saved slopes**, then verify normalization and actual stage inputs. Independently check the derivative/wrench arithmetic using saved effective forces, including the zero yaw correction, unchanged motor-lag derivative and original gyroscopic term. This verifies the retained integration/adapter bookkeeping without evaluating a new aerodynamic trajectory. Unsaved stages remain supported by source inspection and recorded admission summaries, not an independent arithmetic replay.
3. Check saved load identities `T=f0*x`, `y²=sum(T)/sum(f0)`, cubic residual `x³+alpha*x−1`, source/rotor domain, graph-order evidence, and saved final-map residual thresholds. This does not independently validate every stage's geometric coefficient. Be explicit that the pinned, previously checked load kernel remains a dependency; a saved “admitted” flag alone is not new independent physics evidence.
4. Recompute the no-influence/symmetry/sign witnesses, all trajectory distances, the four per-case/treatment epsilon/reduction gates, and on/off contrasts. Report maximum value, time, vehicle/rotor and denominator. Keep gate failure distinct from saved-evidence inconsistency.
5. Audit first failures and unexecuted slots without filling them. All required full-window paths must be complete for a primary/exploratory convergence conclusion. A correctly recorded numerical-gate failure may still pass the evidence audit.

Before freezing, choose one null-path equality rule and exact arithmetic tolerances for the saved algebra; suggested inherited scales are `2e-12` absolute+relative for force/coefficient bookkeeping, `1e-9` relative for positive closure quantities, `1e-9` log residual and `2e-9` normalized source/receiver mismatch. State units for derivative checks and retain explicit absolute floors at zero; do not call these physical tolerances.

The current proposed config uses one300s candidate with280s cooperative guard, one120s saved reviewer,768MiB RSS, and32MiB evidence. The supervisor enforces the reviewer's120s limit, and the independent reviewer declares a115s cooperative guard. The current source partitions the evidence budget into24MiB normal writes plus an8MiB bounded failure reserve so a normal-write cap failure can leave a compact failure record. Derive worst-case output bytes from frozen record shapes before execution; the selected first/last-step witnesses and existing endpoint records must fit without post-result thinning. All generation,18primary paths, fixed endpoint queries, gate calculation and up to6exploratory paths consume that one candidate allowance. No benchmark repetitions, retries, fitting or alternative implementation arms are included. These are proposed new bounds, not authority to dispatch or recycle previous allocations.

## Inspected basis

Existing repository source only: `outputs/step02c-source/physics.cjs` (derivative, wrench, controller and original RK4); `outputs/milestone-31-source/{sim,factory-wide}.cjs` (initialization, held control, Boids/filter/contact semantics and geometry); `research/m31-typed-assembly-2026-10-16/source/{kernel,anchor-kernel}.cjs` (admission, ordered closure, residual and lean construction); and the closed `research/m31-airflow-cadence-2026-10-15/PROTOCOL.md` (earlier prescribed-motion/sample-resolution limits). The present fixed-command and feedback questions are new numerical scopes; they do not reopen that cadence campaign or add physical evidence.

## Final static implementation review

The reviewed candidate now implements the stated force correction, simultaneous projected-stage RK4, endpoint reevaluation, exact cached initialization copied to every path, synchronous held commands, numerical gates and primary-before-exploratory ordering. `controls.cjs` supplies four single-rotor sign checks, zero correction, antipodal quaternion identity and a90degree angle check. These are source-inspected synthetic controls; this review did not execute them.

Earlier draft findings have been corrected: invalid mode names reject; off-arm tilt is measured; input and output finiteness are checked; projection failures retain context; the null gate compares all17 state coordinates and empty/identity load witnesses; centered/offset initial wrench conditions join the primary gate; byte accounting advances only after a successful write; compact partial analysis precedes active-trial retention; and the initializer is cached once per case. The primary pair uses ground/body contact checks, while factory-box contact checks apply only to exploratory Boids, now stated explicitly in the protocol.

For the fixed first and planned terminal step, `stepWitnesses` retains the actual start, projected final state, time, h and held commands. Four associated stage witnesses retain actual normalized states, derivatives, forces and corrections. This closes the first-step final-update evidence gap: a saved-only reviewer can reconstruct the stage inputs and final RK4 combination from saved slopes without a new model evaluation. All other stages retain admission/numerical summaries. If a path stops early, its planned terminal-step witness does not exist and must not be implied. Final-projection failure has a raw final-state and accepted-start context.

The continuous supervisor pins source to the published commit/manifest before dispatch, consumes exclusive invocation locks, enforces fixed wall/RSS/storage limits, retains launch/monitor/cleanup failures and forbids optimization in its Python wrapper. Its recorded elapsed time and sampled RSS are accounting, not performance measurements. A supervisor kill can leave only a saved prefix; the reporting layer must distinguish that state from a completed evidence audit.

**Static verdict:** no remaining dynamics, primary-gating or retained-step bookkeeping blocker was found in the inspected source. The compact interrupted-trial fallback now includes `active.failure`, counts/end when available, the latest saved observations and stage records, and an explicit truncation notice. Compact partial analysis is written first. The final protocol explicitly permits independent geometry/root recomputation at saved endpoints AND the fixed first/planned-terminal captured RK stage states, alongside saved-slope RK4 assembly; this is broader than the initial algebra-only suggestion and adds no scenarios, trajectories or candidate runs. Its120s supervised/115s cooperative reviewer allocation is unchanged. This verdict is conditional on the separately required independent reviewer and frozen-source publication checks; it is not an execution result.

Remaining interpretation limits are substantive, not repairs: the law is provisional instantaneous pose-only aerodynamics; fixed commands are simulated nominal force inputs; nominal yaw torque remains; passing three sampled resolutions proves neither physical validity nor an asymptotic limit; and a saved-only checker independently verifies selected stage geometry/forces/derivatives and RK4 bookkeeping plus endpoint evidence, not every unsaved stage or the hardware model. The current `coupledQueryAttempts` count includes failed stage attempts that can precede an actual coefficient build; it should be read as attempted coupled evaluation slots on rejected paths, not successful solver calls. A completed path has no such ambiguity.

This is source-only review. No candidate import, scientific command, target rescoring, new source acquisition or numerical execution occurred. Repository files were read only; this report was written exclusively in its requested temporary review directory. The independently implemented saved-only review remains a separate required check. This review does not authorize execution, certify unseen results or reopen any closed allocation.

## Reviewed final source pins

Paths are relative to `research/m31-motion-feedback-2026-10-16/`. These identify the exact versions inspected above; later changes require review of their delta. No numerical target was executed for this review.

| File | SHA256 |
|---|---|
| `config.json` | `3554517f6f0c90e832395ec6ac275077cc0034c033103f3a3d24db9513e9b3fc` |
| `PROTOCOL.md` | `7a0ee2d1779d220978729c8f607b702aa4582b918c3c81f6c748642f62ea049f` |
| `source/adapter.cjs` | `332035b55439c568f3a4372c94557359e5ca4a264e3a0f635abdd28ac075a0a9` |
| `source/experiment.cjs` | `13a6f7034ac475cf6e4529394c5ccc6bbba82971e638ca7d90363c9c63d991b0` |
| `source/controls.cjs` | `f0e69bbdda7f85cad295341ac9ffa125265c310eabe3721f6a6454b39506cbff` |
| `source/run.py` | `14e45dc33b58c267b7cc793f3564d25d0436af767ea9c640b190848173d6ab6d` |
