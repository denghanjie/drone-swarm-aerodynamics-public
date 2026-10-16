# Saved-result review: full versus collective-force feedback

2026-10-16. Source commit a3705740e586941855a71a320d48e7374ccd5224; source manifest 5864adc22bbbf9d27afca25bb2ccb6f8da3c234997bf2a7e8c55bdafd750917d. This review reads saved records and performs arithmetic on recorded arrays only. No checker rerun, scientific import/evaluation, geometry reconstruction, reintegration, external acquisition or repository edit occurred. Both execution allocations are closed.

## Outcome and qualification

All12 paths completed. Exact historical off/full repeats, force-only masks, initial equality, pair controls, refinement and allocation gates passed. The saved independent review reports360,829 passing assertions,207 endpoint arrays and96 captured stage witnesses. It exercised960 force-only endpoint vehicle states with both nonzero body rates and unequal nominal rotor states, and288 such captured-stage states. Preservation of nominal angular dynamics was therefore checked beyond the symmetric zero-rate pair. These counts are implementation assertions, not independent experiments.

Nineteen of20 refinement gates use the predeclared below-floor exemption. Coupled body rate uses the ordinary rule: coarse–medium2.33370085e-5rad/s falls to medium–fine1.81894407e-6rad/s, below0.001rad/s and0.75 times the coarse discrepancy. The result supports the declared sampled resolution; it does not establish global convergence order or continuous-time error bounds. Full and force-only position medium–fine discrepancies are5.353805e-8m and6.904074e-9m, much smaller than their observed contrast, without being rigorous error bars.

Candidate/reviewer supervisors report successful closure in4.446899s and2.107516s. These are execution accounting, not a controlled speed comparison between arms.

## Observed mechanism sensitivity

Finest grid is dt0.00125s. Position maxima are over21 saved times and matched vehicle identities.

| Contrast | Maximum position distance | Location |
|---|---:|---|
| Full versus force-only |0.510847004m|t2.0s, zero-based vehicle12 (13th vehicle)|
| Off versus force-only |1.331128103m|t2.0s, zero-based vehicle12 (13th vehicle)|
| Off versus full |1.102444041m|t2.0s, zero-based vehicle15 (16th vehicle)|

At the full/force-only maximum, full position is[-6.550033577,0.049593136,2.753380192]m and force-only is[-6.540961517,0.163677975,2.255517752]m. Full-minus-force-only is[-0.009072060,-0.114084839,+0.497862440]m, with horizontal norm0.114444977m. The largest difference is mainly vertical for this vehicle/time. It is not the vehicle attaining the off/full maximum, so subtracting the maxima has no component interpretation.

| Finest-path summary | Off | Full | Force-only |
|---|---:|---:|---:|
| Mean final altitude, m |4.283475406|3.655363984|3.654584264|
| Maximum recorded stage tilt, degrees |8.853804|19.555806|8.904407|
| Candidate minimum swept separation, m |0.613391|0.571454|0.633469|

Full/force-only mean final altitude differs by0.000779720m, but mean absolute individual altitude difference is0.116188586m. Individual full-minus-force-only altitude differences range from-0.258998237m to+0.497862440m, positive for3 vehicles and negative for13. Similar means hide different individual altitude patterns. Suppressing the modeled aerodynamic moments also brings maximum tilt close to off, while collective-force/controller feedback still generates large off/force-only displacement. Different observables respond differently to this intervention.

Full/force-only maximum quaternion separation is1.623085rad (92.996degrees), whereas maximum body-axis separation is0.315787rad (18.093degrees). The former includes yaw and must not be called tilt. Actual maximum full-path tilt is19.555806degrees. Armwise tilt maxima also occur at different times.

## Caveats and immediate decision

The force-only arm is not an accurate substitute for individual full-model motion at the declared position scale: it changes a sampled position by about half a metre despite close mean final altitudes. This does not establish that moments always worsen an outcome. Every arm changes later geometry, loads, commands, nominal motor states and nominal torque. The total consequence of suppression is observed; additive force/moment contributions and causal percentages are not identified.

Force-only retains the same coefficient construction and all rotor-load solves. Masking the final added torque demonstrates no useful computational saving. Solved rotor loads remain model outputs rather than physically applied individual thrusts under its hybrid wrench rule.

The pair's zero rotation is a construction check. Candidate separation/contact reports and zero saturation counts establish neither continuous safety nor stability, tracking accuracy or physical feasibility. The exposed seed's deterministic repeats do not supply independent confirmation. The ideal-power/source-total law, nominal-yaw treatment, moving-pose extension and omitted wake-history/self-airspeed response remain unvalidated. Keep full wrench as the numerical reference for future approximations, with physical truth explicitly unresolved.

## One next bounded question, if a new allocation is adopted

**Can10ms refresh of the full coupled load response preserve this same16-vehicle closed-loop trajectory to predeclared numerical tolerances while reducing expensive coupled-query work?** This retains the moments shown to matter and targets calculation frequency. Limit a future first comparison to the same2s, seed260201, controller and three dt levels, with two arms: every-stage full reference and one precisely defined10ms approximation—six paths maximum. Do not add64 vehicles, prediction, adaptive intervals, another cadence or seed. A failed outcome is sufficient to stop this candidate.

Freeze what is held. A defensible candidate caches dimensionless rotor ratios x from each joint own-state refresh solve. Between refreshes use T_r(t)=f0_r(t)*x_r(last refresh), then assemble the full force and roll/pitch correction at the current quaternion, retaining nominal yaw, gyro and motor dynamics. This preserves response to current nominal motor states, but cached ratios generally do not satisfy instantaneous coupled closure between refreshes. Call it a stale-ratio numerical approximation. Holding world-frame force, absolute thrust, coefficients or source amplitudes would be different experiments.

Fix tick ordering: the previous cache serves the interval through its final RK stage; the next accepted boundary refreshes it before the next interval. Freeze controller/refresh order. Save pre-refresh left-limit and post-refresh loads at every10ms event, including the terminal boundary where defined, so update-aligned100ms observations do not conceal hold error. Compare trajectories and, at a fixed saved audit schedule, compare held loads with instantaneous loads at the approximation's own states. Audit/oracle calls must be prospectively counted separately from propagation calls; any timing exclusion must be explicit while total resource accounting includes them.

Retain full domain/contact failure evidence. Old cached residuals must never be presented as current-state residual passes. Apply trajectory refinement gates separately to both arms, retain full-wrench error including moments, and require exact reference repeat agreement. Record actual build/solve calls and complete loop cost including scheduling and assembly; call reduction alone is not measured speedup. New source/reviewer, finite caps and one-use locks must precede any launch. This review starts no such work.

This is distinct from the closed airflow-cadence/refresh-envelope studies: those used prescribed two-drone kinematics; the envelope fixed orientation and nominal thrust. They did not integrate this source-total coupled closure into moving multi-vehicle states with changing controller commands. Their negative cost evidence still matters: envelope checking overhead erased its expected advantage over a simple hold. The next question should therefore test one fixed reuse rule and no adaptive-envelope machinery. It does not reopen or repair prior studies.

I do not prioritize another browser-recording benchmark now. The saved typed-assembly summary already places lean5000 queries around474–477ms excluding steering/flight/rendering. The terminal GPU-readback trial produced no qualified output, and the associated runtime/monitor question remains unresolved. Browser qualification remains an engineering prerequisite, but repairing it would not answer this next numerical-fidelity question. At unchanged roughly0.475s/query,100Hz refresh would imply roughly47.5s of query work per simulated second—a workload illustration, not a cross-runtime prediction. Even success would establish only one possible ingredient for later5000 accuracy/computation work, never real-time5000 flight or physical validity.

The current ablation is complete and sufficient to publish with these limits. This next question is an option for a separately adopted allocation, not an obligation to execute now.

## Saved evidence pins

Paths are relative to research/m31-force-ablation-2026-10-16/results/.

| File | SHA256 |
|---|---|
| analysis.json |ae80740f689e104be4dbafba7a33bb559c6fe43f7a3b5be89670bdea44a14ab9|
| independent-review.json |468181e072e4ddd7b48e9b14c13c58fdb891e6f09c9452e69435284209c96804|
| boids16-off-0.00125.json |8b205e66ac37bfa14d669eff351a80a2fbb7a731a85fb2db3cd229ce3ee6b9aa|
| boids16-coupled-0.00125.json |2288c5161858dbbe32dbfc7bc5bb8b30ed26006bc5a89e3eef1572f6570ed4fb|
| boids16-force-only-0.00125.json |bdbe7896794e85c9b144b5b842077932c6d3aa660265782a497e6661d7ddf3aa|

Historical scope/cost was read from public typed-assembly, airflow-cadence, refresh-envelope and transport/GPU-readback protocol/result summaries only. No missing historical output was reconstructed and no old invocation was repeated.
