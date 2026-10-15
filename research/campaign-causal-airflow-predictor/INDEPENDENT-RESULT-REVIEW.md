# Independent saved-result review

2026-10-15 UTC. **VERIFIED: CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW for the declared two-seed, 0.1 s numerical screen.** All 14 arms completed and all 19 declared gates agree with saved evidence. The predictor's eight primary errors are 26.53–54.11 times smaller than matched ZOH errors, with the same scheduled field counts. This supports the bounded numerical mechanism question, not physical accuracy, speedup, general stability or another execution release.

No model, initializer, collector or fixture was rerun. Verification used saved JSON/binaries, independent vector/quaternion arithmetic, hashes and the frozen source already reviewed.

## Verified errors

Maxima cover 16 vehicles and 41 common accepted-state times; comparisons use h8 approximations versus joint32. Units are m, m/s, rad and rad/s respectively.

| Seed | Metric | ZOH | Predictor | ZOH/predictor |
|---|---|---:|---:|---:|
|840149|Position|1.81969549e-5|4.86855581e-7|37.38|
|840149|Velocity|4.29308162e-4|9.80792873e-6|43.77|
|840149|Attitude|5.55235128e-4|1.02608011e-5|54.11|
|840149|Angular rate|8.59714009e-3|1.80538482e-4|47.62|
|840163|Position|6.33741190e-6|2.38851937e-7|26.53|
|840163|Velocity|2.57909206e-4|5.54027911e-6|46.55|
|840163|Attitude|3.59943463e-4|8.39729821e-6|42.86|
|840163|Angular rate|7.81609630e-3|1.55386929e-4|50.30|

Every cell is above its screening floor, within the predictor's unchanged outer cap and better than the prospective fourfold target. Both new-seed ZOH baselines also meet their absolute caps. Therefore this is evidence of reduced numerical error; it is not a same-case rescue of the previous seed 840131 cap failure.

Both joint-step gates and all four method-specific physical-step gates pass. The largest observed numerical-difference proxy divided by its corresponding signal is 0.000143125, versus the allowed 0.1. That is 0.0143% of the signal. These differences resolve the observed effect well above the declared floors; they remain empirical proxies rather than certified error bounds.

The predictor's worst angular-rate witnesses occur before the final time: seed 840149 vehicle5 at tick1536 (0.03 s), and seed 840163 vehicle11 at tick4352 (0.085 s). Reporting only final error would miss them. The respective terminal angular-rate maxima are 1.62733426e-4 and 1.46466426e-4 rad/s.

## Independent checks and artifact limits

All 14 frozen entries and all 15 public functional-file identities match. The 14 comparison JSON hashes,14 witness tensor hashes/shapes, and both 11 x 16 x 17 reference tensors match their recorded identities. Every reference number is finite; quaternion norms/nonnegative nominal motors satisfy the recorded domain. Each seed has one common initial-state hash across its seven arms, and reference initial/final blocks match run hashes.

Independent arithmetic reproduced70 state-metric maximum witnesses,44 terminal metrics recoverable from saved witness locations,56 field/load witnesses and 14 command witnesses. Largest maximum-witness arithmetic discrepancy was1.11e-16. Twenty-eight saved joint32 witness rows also match controller-grid reference rows bit-for-bit. All 19 gate decisions were checked against their underlying comparisons, floors, caps, exposure and work records, rather than accepted from the summary alone.

The remaining26 terminal values and the assertion that no omitted sample has a larger error depend on the frozen comparator: dense all-arm trajectories were intentionally not retained. A correctly reproduced witness does not independently establish the global maximum. Same-state lag summaries also lack full saved diagnostic tapes and were not regenerated with the wake model.

Compatibility passed: the recorded legacy prefix hash matches the public first10,880 bytes. The reported wrapper discrepancy1.1102230246251565e-16 is reproduced by its saved scalar worst witness and is below 1e-12; wrapper bit equality is correctly false. All 12 saved scalar-fixture outputs agree arithmetically. The five new wrapper state arrays themselves were not retained, so their complete comparison cannot be independently re-executed from output alone. This is fixture-level compatibility, not universal wrapper equivalence.

## Matched field work and resource observations

For each approximate arm:80 production fields,11 separate fresh diagnostics and 10 controller updates. Matched h pairs have identical step, derivative, callback and field-attempt/return counts. Scientific totals reconcile to 4400 steps,281600 vehicle derivatives,2880 production fields,154 diagnostic fields,2 baseline checks,140 controls and 17600 stage callbacks. Compatibility separately adds8 steps,512derivatives,one field andone controller call. No hidden extra field or fallback is recorded.

Lean scientific production/diagnostic kernel totals are 167040/8932. These exclude the separate compatibility and baseline evaluators' unretained internal kernel counts. Equal field count does not mean identical total work: predictor arithmetic is additional, and some diagnostic guard-visit counts differ. No speedup or runtime-efficiency claim follows.

Outer launch exited0 in 5.165944 s, with no timeout, truncation or retry. Supervisor reports child CPU6.049231 s and its own CPU0.054348 s. Original result files total174,276 bytes, below 300,000. These are serial resource observations, not a matched timing benchmark.

## Exposure: where the result does and does not apply

All production fields have positive inflow. Peak values are about 4.020 m/s and 3.646 m/s for the two seeds. All four predictor arms record zero clamped components/vectors in 491520 stage-scalar supplies and 2816 diagnostic-scalar supplies. Startup holding occurred for16/32 stage callbacks at h16/h8 per seed, as planned. Thus no trajectory exercised active clamping; only the scalar declining fixture tested it.

No wall constraints, tilt/motor/speed clipping or wall-repair iterations occurred. Controller pair-constraint totals were 1486/1524 per arm, with0/2 within-arm neighbor-list changes. All cross-arm controller branch-mismatch counts are zero. Minimum sampled pair clearance is 0.49556 m and obstacle clearance exceeds 3.62348 m. Raw nominal motor thrust remains above 0.03820N. Source downstream extent stays below 1.67385 m, so the 2 m axial fade is not exercised.

The second seed does approach the all-pair far-start surface: the nearest saved scalar margin is about 1.04e-5 m. No finite-jump/domain stop occurred, but those scalar margins do not retain the joint radial eligibility needed to claim a tested discontinuous-annulus event. Do not describe this case as uniformly boundary-distant or general event robustness. Stage/endpoint guards and segment-contact checks remain sampled.

Only one cadence, a very short horizon and two fixed seeds were tested. No asymptotic order, statistical generality, sustained-flight or obstacle-negotiation result follows. The 2026 amplitude/measurement-quantity discrepancy remains unresolved. The earlier qualification remains GATE_STOP, its skipped arms remain skipped, and this result grants no automatic extension or tuning.

## Exact identities

- Revised freeze:4ded2177c6203024dec4a5f27895182324e484f3230d296a4e872529fc2844e8
- Summary:d6312e7420323c70f3ad36bc7e4f4c5df8c698433e499d63d08f4196d9d73767
- Gates:5d306f7c82e2fd3128b2ee459ff4334c0171d5b04cdeefd45b6786161a33deed
- Compatibility:82c08398ce61d2966a8594730a0c907c7a1c1421de17e254a8edd83c85c7aaaf
- Supervisor receipt:b45b5ccf14f352d4e9916c208d702eea73719146ee1b3144a0af269c87605219
- Whole-launch receipt:c6bebf51c8176316b3066e4cf00b475adece3f9b853712bb6d1fc21b760c1249
