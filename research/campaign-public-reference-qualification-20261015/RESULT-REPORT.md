> Public edition of the preserved original, SHA256 `540a3e9e221a7cb59e1f92e31ae76eeb24a1406cfa0ebf7d53290e396e78ba38`. Clarifies signed downstream exposure and omits private global storage bookkeeping. Scientific numerical results and the stopped decision are unchanged.

# Qualification result: resolved hold error, predeclared cap stop

**GATE_STOP; no extension or retry.** The one released 0.1 s attempt passed public compatibility, both seeds' joint-step convergence and all three held-physics checks for seed840131. It then stopped at the predeclared combined air64 gate because angular-rate error exceeded its absolute cap. The reduction condition itself passed. Thirteen rows completed including compatibility; six held rows for seed840137 were skipped.

## Main numerical finding

For seed840131, held airflow on h8 physical steps was compared with the synchronized joint32 trajectory. Maxima cover all16 vehicles and41 accepted-state observations over0–0.1s; each arm used its own evolving local3D Boids controller.

| Airflow period | Position m | Velocity m/s | Attitude rad | Angular-rate norm rad/s |
|---|---:|---:|---:|---:|
|128ticks =2.5ms|1.8450554e-5|5.3702986e-4|1.6016114e-3|2.7769406e-2|
|64ticks =1.25ms|9.3547091e-6|2.7004217e-4|8.0638439e-4|1.3884419e-2|
|32ticks =0.625ms|4.7100709e-6|1.3540634e-4|4.0458488e-4|6.9421132e-3|

Errors roughly halved at each cadence halving. At air64, angular-rate maximum0.013884418690814795rad/s exceeded the declared0.01rad/s cap, even though the reduction ratio was0.4999898<0.7. The worst angular-rate case was vehicle7 at0.085s. The gate correctly stopped; its name `hold-reduction-840131-64` does not imply divergence. An initial short status described the gate name; this report states its exact cause.

The finest already-computed result is numerically smaller than that cap, but subsequent air32, finest-cross-family and attribution gates were **not reached**, and the second seed's held matrix was not run. These saved values cannot convert the campaign into a completed qualification. No criterion was changed after observing them.

## Separation from physical-step error

Joint64 versus joint32 differences, across both seeds, were at most8.543e-12m position,2.850e-10m/s velocity,8.272e-10rad attitude and2.417e-8rad/s angular rate. The declared joint convergence gates passed, including nonzero airflow on every production field.

For the three completed held cadence pairs, h16 versus h8 maxima were at most2.469e-14m,3.313e-13m/s,3.158e-12rad and7.405e-11rad/s respectively. These differences are far smaller than the observed cross-family differences. The saved data therefore resolves a temporal-hold effect on this case; it does not certify a true numerical error bound or asymptotic order. All comparisons use the unchanged finite-support model.

Incoming-held versus fresh inflow at the same current state, sampled before control-tick refresh, peaked at0.05226496,0.02613900 and0.01307009m/s for the three h8 held cadences. Their incoming ages were128/64/32ticks. Between-arm inflow/load differences also contain state/controller divergence; they must not be described as pure same-state lag. Diagnostic maxima are control-grid sampled, not all-time/stage maxima.

## Compatibility, exposure and limits

The public seed4301 initializer and first four h128/air512 steps matched all five saved states exactly:10,880bytes. Frozen plan/code/source hashes remained unchanged. No private R8 material was used.

There was genuine wake exposure: production maximum inflow4.26047m/s for seed840131 and3.23308m/s for840137; positive-contribution counts remained56 per field. The controller accumulated1440/1530 local pair constraints and4/2 neighbor-list changes over each corresponding10-update case. No wall constraints, speed/tilt/motor clipping or wall-repair failures occurred.

Minimum control-grid pair clearances were about0.486m/0.449m; obstacle clearance exceeded3.59m. Across the twelve scientific arms, the maximum positive sampled all-pair downstream distance was1.6386369259109237m (<1.639m), so the2m axial fade was not exercised. The original report's looser<1.762m statement used the largest absolute signed downstream extent, including upstream pairs; it was not the positive downstream maximum or a compatibility-only difference. The nearest sampled far-start margins remained about0.044m/0.058m from that boundary. Domain/contact/finite-jump stops did not occur. These data do not cover obstacle negotiation, near-wake events, sustained flights or general branch regularity. Held internal stages remain unaudited; contact checks use endpoint-segment envelopes. Do not interpret zero held projection diagnostics as a measured projection bound.

Numerical agreement is not physical accuracy. The separate2026 amplitude screen found a conditional0.629–0.760m/s discrepancy against published PIV symbols. Its measurement-quantity and physical-input limitations remain. This numerical study neither removes that discrepancy nor retroactively qualifies the old failed public reference or private R8.

## Execution and retained verification

One attempt; no timeout, cap overrun or retry. Whole launch, including supervisor, took2.735474s; outer child-process CPU3.549244s. Supervisor recorded Node CPU3.482971s and its own CPU0.030832s. Driver final observed RSS was91,381,760bytes, not a peak-RSS guarantee. This single serial observation is not a speedup benchmark.

Completed work including compatibility:3444physical steps,220416scalar derivative calls,2801production fields,132fresh diagnostic fields,2baseline-field comparisons and121controller updates. Both joint controller-grid reference tensors remain,11×16×17 doubles each. No all-arm dense archive was written.

A saved-output-only Python check verified all10comparison files and both reference hashes, and recomputed50 reported maxima from their paired binary witnesses. Largest arithmetic discrepancy was1.11e-16. It imported no model and made no model calls. This is an implementer check, not a substitute for independent review; it cannot establish that every dense maximum was selected correctly without the omitted trajectories.

Raw qualification outputs total131,849bytes. The original execution and failed records remain preserved. Global private storage bookkeeping is omitted from this public edition.

## Exact evidence

- Frozen implementation: `b6fe2ec97611338d98ce408094957a3077620194c20c7b5a6458fe367a617f2b`
- Summary: `f5cd17150fc487220d95b5a601857758f5c5c9cc04053a45ea94685a025f3e36`
- Failure: `d6f10c8639aa38d35c3de943b8a8b7186bbaf8f34462f05f5d08407c3dd79a58`
- Supervisor receipt: `44d2aee97803a6f986e518cf72315644d4d20fcf33429f9372e520c50aad4ae7`
- Whole-launch receipt: `e823038b16433ab78afb15998fd8fd6f197479c84eaa0890fff2f46a8ba586e8`
- Saved witness check: `9a5fd5d7b610d929ccb5173fd3d2a1f252440e6ce5e4f3d260b797ab2b6cdf47`
- Reference840131: `a51bfa15a1b62d04728c2c9dc43dd069ab7448c7c599d32781772f774771d1c6`
- Reference840137: `2283df7b7a92be9f6f56dc2fe0921f64b5f8b0f0c2815777279d31437641dbde`

The attempt ends here. A future study would need its own prospective question, authorization and preserved relationship to this failed gate; the existing extension remains ineligible.
