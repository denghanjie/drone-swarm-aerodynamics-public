# Prospective challenge: collective-force versus full-wrench feedback

2026-10-16. Conditionally support a new, separately frozen mechanism diagnostic. The preceding motion-feedback allocation is complete and closed. This review reads existing public source, protocol, saved-result interpretation and reference-file hashes only. No scientific code was imported or executed; no target, source acquisition, repository edit or new agent was used.

## Question and smallest useful scope

Ask: **for the already exposed Boids16 seed260201 and unchanged controller, how much does the sampled trajectory/tilt response change when the added aerodynamic roll/pitch moment is suppressed?** This is a counterfactual intervention in the provisional equations. The seed was chosen after seeing its response; it supplies neither independent replication nor generalization to another seed or physical aircraft.

Freeze nine Boids paths: off, full coupled, and force-only; each2s at dt .005/.0025/.00125. Preserve the exact cached17-state initial array, wide-factory environment, IDs/order, original Boids/route/grid/filter/controller,10ms held commands,100ms endpoint observations and projected-stage RK4. No tuning, new seed, extended duration, extra dt or alternate solver. Recompute all coupled loads on each arm's own simultaneous current stage state. Reusing the full arm's geometry, forces, commands or trajectory in force-only would answer a different question.

Include the suggested offset fixed-command force-only control at all three dt values:0.5s, lower[-6,0,4.5], upper[-5.96,0,5.1], zero velocities/rates, identity quaternions, four nominal states and fixed commands mg/4. This gives12 paths maximum. A useful frozen order is synthetic adapter controls, three pair controls, six off/full Boids repeats, then three new force-only Boids paths only after controls/repeat/refinement gates pass. Save all attempted paths and explicit skipped slots. A legitimate null or small ablation effect must remain a valid result.

## Define the intervention precisely

For every coupled query preserve the unchanged source/receiver solve and its four solved loads T_r. With delta_r=T_r-f0_r, compute the modeled correction

- world force: R(q)[0,0,sum(delta_r)];
- body moment: [sum(y_r delta_r),-sum(x_r delta_r),0].

Full applies both. Force-only applies that world force and an exactly zero added body moment. Off applies neither. Preserve all original nominal roll/pitch/yaw torques, motor-lag derivatives and gyroscopic terms. In particular, zeroing the total angular derivative, removing nominal controller roll/pitch action, averaging the nominal motor states, or changing yaw would introduce another intervention.

Save **modeled** and **applied** corrections separately. Keep the solved rotor loads unchanged as the load-model output, even when their modeled moment is suppressed. In force-only these values do not by themselves specify the applied physical per-rotor wrench: the intervention deliberately combines the modeled collective force with nominal differential torque. Label it a counterfactual wrench rule; do not imply a validated physically realizable rotor law. The independent derivative checker must apply its own explicit mode mask and must not reuse the candidate masking helper.

At the common initial state full and force-only must have identical commands, coefficient/branch witnesses, solved loads, modeled corrections and applied world force. Their angular derivatives differ only by the removed modeled moment divided componentwise by inertia. Equality of subsequent forces/commands is neither expected nor required because their states diverge.

## Gates that should be frozen before dispatch

**1. Historical repeat agreement.** Pin all six old Boids records below and the old source/runtime dependencies. Under the same recorded Node/runtime, require exact parsed numeric equality for the shared initial state and every corresponding accepted sample's full17-state array, held commands, solved loads, modeled/applied full correction and derivative; require exact sample times and schedule/count identities. New off maps to old off and new full maps to old coupled. Compare selected scientific fields, excluding IDs, labels, runtime and new diagnostics. This is a deterministic regression check, not a new independent replicate. Do not use the much looser trajectory-resolution tolerances to excuse changed baselines or relax equality after a mismatch. If a different arithmetic/runtime contract is genuinely needed, choose and justify its repeat tolerance prospectively instead.

**2. Mode-mask and preservation invariants.** At every candidate stage/endpoint force-only has exactly zero applied aerodynamic torque; full's applied correction equals its modeled correction; off's applied correction is zero. All modes retain the original motor derivatives and nominal/gyroscopic angular terms. Check force-only's applied force equals the modeled collective correction. Use saved common-state and selected-stage arithmetic to verify this independently, including at least an algebraic fixture with unequal nominal rotor states and nonzero rates so a mistaken removal of nominal torque or gyroscopic terms cannot hide behind a symmetric zero. Retain the existing single-rotor sign, quaternion-antipode/angle and zero-correction checks. No synthetic fixture needs a new wake solve merely to test the mode mask.

**3. Offset force-only negative control.** Require full duration, lower x/y unchanged, both quaternions at identity, body rates zero, all nominal motor states fixed, upper full state unchanged, each within the inherited1e-12 component/angle control threshold. At t0 the modeled lower pitch moment is positive and the modeled collective force is negative, but the applied moment is exactly zero. Lower altitude decreases at positive sample times, while lower lateral motion remains zero. The control must have a nonzero modeled moment so suppression is nonvacuous. Do not demand that its vertical trajectory equal either the old full-offset or centered trajectory. Candidate checks may cover all stage inputs; independent evidence covers endpoints and retained witnesses, not every unsaved stage.

**4. Completion/domain/contact.** Every required path must complete with finite states/commands/derivatives, admitted unchanged geometry and descending eligibility, log residual<=1e-9 and source/receiver mismatch<=2e-9. Retain ground/swept-body checks and factory-box checks for Boids. Stop each path at its first failure and retain its full failed state, last accepted state and command. Never substitute nominal/zero flow, change support or omit a source. A numerical/model/contact failure prevents a complete mechanism conclusion; it does not authorize a replacement.

**5. Sampled refinement, separately by case/arm.** Preserve the prior position1mm, velocity1mm/s, full sign-invariant quaternion angle0.1degree, and solved rotor-load difference0.001 times mg/4 tolerances. Compare all common samples and vehicle/rotor identities, including both endpoints. Require medium–fine<=tolerance and<=0.75 coarse–medium, exempting only when BOTH discrepancies are<1% of that tolerance. Explicitly report which branch passes. Also recommend a new prospective body-rate-vector threshold0.001rad/s with the same rule because angular response is now a mechanism observable. These remain numerical preferences, not physical accuracy margins. Body-axis angular discrepancy should be reported separately; the full quaternion tolerance already bounds it mathematically, so a duplicate pass is not independent evidence.

Do not combine effect magnitude or a preferred direction with these validity gates. A gate failure is an unsuccessful diagnostic, whereas a passed diagnostic with little full/force-only difference is an informative negative result.

## Estimands and decisions

Name arms O(off), F(full), C(force-only). Primary mechanism estimand: D_p(F,C), the maximum paired position-vector distance over all common times and vehicle IDs on the finest grid. Report its time/ID, and D_p(F,O), D_p(C,O) with their own time/IDs. Preserve the complete signed coordinate/altitude time series; differences between separately maximized summaries can hide different vehicles/times.

For attitude, retain full quaternion separation but also body-axis separation between n_A=R(q_A)e_z and n_B, and each arm's absolute tilt from world vertical. Use atan2(norm(n_A cross n_B),n_A dot n_B) for robust axis separation, and atan2(hypot(n_x,n_y),n_z) for tilt. Report body rates, nominal commands, own-nominal modeled force loss and modeled/applied moments. The preceding84degree full-orientation contrast included yaw; do not repeat it as tilt. Maximum stage tilt is a diagnostic over recorded stages, distinct from shared-sample maxima.

A defensible predeclared interpretation rule for position is: call D_p(F,C) 'resolved beyond the declared numerical scale' only if it exceeds max(0.01m,10 times the sum of F and C medium–fine position discrepancies). The1cm margin is a numerical reporting preference, not an application or physical threshold; the observed dt differences are not rigorous error bars. If D_p(F,C)<=0.001m, describe agreement within the declared sampled position tolerance. Values between those labels remain reported without a large/small mechanism verdict. Other observables can disagree and must remain visible.

Report D_p(C,O)/D_p(F,O) descriptively only when the denominator exceeds0.01m; otherwise mark it unresolved/undefined. Never interpret1 minus this ratio as a percentage of physical motion 'caused by torque,' clamp ratios to[0,1], or subtract the three maxima as additive components. Removing moments changes subsequent geometry, loads, controller commands and nominal torque. The contrast is the total consequence of suppressing that pathway in this model. A large retained C/O response shows collective-force/controller feedback can generate substantial response without applied aerodynamic moments; a smaller response supports sensitivity to the moment pathway. Neither outcome identifies independent additive force/moment contributions.

## Evidence and finite allocation

Use a new package, source manifest, result directory and one-use invocation locks; keep the old allocation immutable. Publish the new frozen source/reviewer/configuration and verify remote pins before dispatch. Retain accepted endpoints with load/coefficient witnesses, modeled/applied corrections and derivatives; first and planned-terminal step starts/finals and four stage slopes; all-stage scalar admission/mask diagnostics; control records; and first-failure/compact resource records. Do not save per-drone full moment tensors at every stage solely to repeat a zero-mask check.

The independent saved-only reviewer may recompute geometry/load roots at the frozen saved endpoints and captured stages, check the mode-specific derivative and RK4 assembly, compare immutable repeat references, and recalculate all gates/contrasts. It must not rerun trajectories/controllers or choose extra targets. Its scope should be explicit before freeze.

A fresh cap such as one300s candidate/280s cooperative, one120s reviewer/115s cooperative and768MiB RSS is sufficient as a proposed ceiling, not an execution authorization. Size storage from record shapes before freeze: the six old Boids records already total about16.36MB, so another three Boids records plus pair controls can exceed the former24MiB normal-write allowance. A prospective40MiB total with8MiB compact-failure reserve and32MiB normal writes is a reasonable bounded starting proposal. Do not thin records after seeing an outcome. Count reference copies and supervisor/reviewer outputs if included in the generated-evidence budget; hashed reads of the immutable old files avoid unnecessary duplication.

No performance, physical-accuracy, safety, novelty or5,000-drone claim follows. This source challenge supports a specific new diagnostic only; it neither reopens nor adds runs to the completed campaign.

## Immutable repeat references

Old source commit: `ee1c888d1e10fd712750c8a80150b13abb32eb19`. Old source manifest SHA256: `4cffb621a5925441fd0c4fcea5a55e7d1fa70d7bd931496fd74b45d9bcb6b63d`. The following paths are relative to `research/m31-motion-feedback-2026-10-16/results/`; their hashes were read from disk without executing the model.

| Record | SHA256 |
|---|---|
| `boids16-off-0.005.json` | `eca1e7332d43a1b273797f89d238fb536249811f814534da6c31d1f89cd177fd` |
| `boids16-off-0.0025.json` | `8c4b30ec74463c6e9aad25b66ddb4b8a877b627e4776011da4190d33e3645303` |
| `boids16-off-0.00125.json` | `03dc1f5a4b7074564ce4f820c31feb409a7e7eb49ede250e4bd539c8046e2ff0` |
| `boids16-coupled-0.005.json` | `341c0fcd9e796f316b528741bccc79b832032952e6e468ef7488645e571a9e5d` |
| `boids16-coupled-0.0025.json` | `70cbb865cdafa9946e808d84a894ef89b435cac1de496f28c2045f478ede19cf` |
| `boids16-coupled-0.00125.json` | `37fc64506929f0e5280bf4d3dc7b905532344583850cc1b95383bbf96652ce3f` |
