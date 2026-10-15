# Causal airflow prediction: promising short-horizon result

Experiment: **CAUSAL-AIRFLOW-PREDICTOR-20261015**. One released attempt completed all 14 arms. At the same 1.25 ms refresh cadence, the stage-dependent predictor reduced every measured trajectory-error maximum by **26.5–54.1 times** across two new seeds. It met the predeclared fourfold target and unchanged absolute caps. This is a 0.1 s numerical result for the fixed public model, not physical validation, a speedup result or a new-method claim.

Status: COMPLETE. Decision: CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW. No extension or retry was executed. Original summary SHA256: `d6312e7420323c70f3ad36bc7e4f4c5df8c698433e499d63d08f4196d9d73767`.

## Actual error reductions

Each entry is the maximum over 16 vehicles and 41 saved comparison times. ZOH and predictor use h=8 ticks and are compared with separately qualified joint32 integration. Both arms use their own evolving local-3D Boids states and controller commands.

| Seed | Metric | ZOH error | Predictor error | Reduction |
|---|---|---:|---:|---:|
|840149|Position, m|1.81970e-5|4.86856e-7|37.38x|
|840149|Velocity, m/s|4.29308e-4|9.80793e-6|43.77x|
|840149|Attitude, rad|5.55235e-4|1.02608e-5|54.11x|
|840149|Angular rate, rad/s|8.59714e-3|1.80538e-4|47.62x|
|840163|Position, m|6.33741e-6|2.38852e-7|26.53x|
|840163|Velocity, m/s|2.57909e-4|5.54028e-6|46.55x|
|840163|Attitude, rad|3.59943e-4|8.39730e-6|42.86x|
|840163|Angular rate, rad/s|7.81610e-3|1.55387e-4|50.30x|

All eight baseline errors exceeded their screening floors. On these new seeds, ZOH itself also passed the absolute caps. This experiment therefore demonstrates a relative improvement; it does not reproduce or erase the earlier seed840131 absolute-cap failure. That earlier GATE_STOP remains unchanged.

The predictor uses only its last two scheduled fields, evaluated at each RK stage time, with one initial ZOH interval. There were **zero negative clamps** in all four predictor arms and their diagnostics. The clamp policy is implemented but its flight behavior was not exercised; only the fixed scalar fixture exercised clipping. Controller history was retained across command updates, as prescribed.

## Reference and physical-step checks

Both seeds passed the frozen joint128/64/32 reference screen before approximation arms began. At fixed refresh cadence, both ZOH and predictor passed h16-versus-h8 checks. Every reference/physical-step noise proxy was at most 0.0001432 of its corresponding trajectory-error signal, well below the required 0.1 fraction. These are observed self-consistency differences, not certified error bounds. Joint fine differences are below all four floors, so they do not establish an observed RK order.

Incoming predictor-versus-fresh inflow gaps, sampled before refresh on the controller grid, were 0.000878483 and 0.000589406 m/s. The ZOH gaps were 0.0304985 and 0.0234332 m/s. These same-state comparisons support the proposed hold-lag mechanism. Cross-arm trajectory errors also include evolving state/control differences. One cadence cannot establish second-order coupling.

## Equal field counts and actual resource use

Every approximate arm performed exactly 80 scheduled fields, including initialization, 11 auxiliary diagnostic fields and 10 controller calls. Predictor/ZOH pairs also matched physical steps, vehicle derivatives and stage callbacks. Successful returns equaled attempts; there were no fallback evaluations. Production candidate/kernel/guard counts matched for the h8 pairs in these cases; auxiliary guard counts differed slightly for one seed. Predictor arithmetic remains additional work, and there is no timed speedup comparison.

Scientific totals were 4400 steps, 281600 vehicle derivatives, 2880 production fields, 154 diagnostic fields and two baseline checks. Compatibility added eight steps, one shared field and one controller call; twelve scalar checks added no wake calls. The complete launch took 5.166 s wall time and 6.146 child CPU seconds. It returned zero without timeout, retry or skipped arms. All nineteen recorded gates passed. These timings describe the bounded attempt, not a performance benchmark.

Legacy compatibility matched its five public states byte-for-byte. The synchronized ZOH wrapper differed by at most 1.11022e-16 in that fixture, below the predeclared 1e-12 tolerance; it was not bit-identical. The fixture contained six zero-wind and ten nonzero-wind receiver vectors. This is finite-fixture compatibility, not universal arithmetic equivalence.

## Exposure and limitations

Production inflow reached about 4.020 and 3.646 m/s. Sampled raw motor thrusts stayed positive, with overall minimum 0.0382073 N. Pair constraints were present; seed840163 had two controller-neighbor changes. Comparison branch signatures matched. No wall constraints, tilt clips, motor-bound hits, speed limits or repair iterations were exercised.

The smallest sampled pair clearance was 0.49556 m and obstacle clearance 3.62348 m. Maximum positive downstream extent was below 1.674 m, so the 2 m axial fade and 2.5 m cutoff were not reached. All-stage and endpoint monitoring found no near-domain, contact or sampled finite-jump stop. Sampled checks do not prove continuous safety or regularity. The short horizon, small N, inactive clamp and limited geometry exposure restrict generalization.

The model remains physically unvalidated at this scale; the separate 2026 published-velocity screen found a substantial nominal amplitude/observable mismatch. Lower numerical error does not reduce that physical discrepancy. Causal extrapolation and hold fallback are established prior work; see the accompanying source ledger and bibliography.

## Saved-evidence verification and next decision

Author post-run checks used separate Python arithmetic on saved JSON/Float64 only. All frozen hashes and 14 comparison/witness hashes matched. Seventy state-witness values reproduced within 1.55e-16; 56 field/load witnesses and all nineteen gate decisions agreed. Thirty-seven terminal values and 28 reference witness rows could be checked directly. Complete unretained comparison streams prevent independently proving all global maxima and every terminal metric. The check receipt is [SAVED-EVIDENCE-CHECKS.json](results/SAVED-EVIDENCE-CHECKS.json).

The useful next milestone is a separately reviewed exposure-expansion test with a qualified longer-horizon reference, unchanged numerical goals and explicit guard/clamp coverage. Equal field counts should remain primary; any runtime claim requires a distinct fair cost protocol. This favorable result supplies a reason to consider that next test, not permission to run it or evidence that it will succeed.
