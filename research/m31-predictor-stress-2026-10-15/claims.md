# Claim ledger — six-case predictor stress

| Claim | Status and evidence boundary |
|---|---|
| Predict5 improves all tested peaks and RMS against hold5 | Supported by all18 case×observable comparisons, with both methods' sampling screens. Selected six-case model suite only. |
| Predict5 meets every chosen numerical target | Rejected: source-pitch thrust 2.898438mN exceeds 1.32435mN; maximum is first refresh-left at t=5ms. |
| Predictor improves startup immediately | Rejected: it equals the hold until a second actual sample; negative-time samples/history were not supplied. |
| Predictor dominates hold2.5 | Rejected: lower recorded time but several larger peaks; source-pitch and cold-start thrust are examples. |
| Predictor is faster than matched-call hold5 | Not established; timing ranges overlap in each case. |
| All independent implementation comparisons pass | Supported at all saved fine inputs for all-vehicle winds and receiver0 body thrust/roll/pitch; this checks declared equations. |
| Current-state receiver response includes fresh attitude projection | Incorrect: projected scalar inflow is retained/extrapolated; current nominal motor states feed the receiver root, with body-frame wrench output. |
| Sampling screens establish continuous accuracy | Not supported; two finite grids plus refresh-left values, no continuous proof. Earlier uniform-RMS failures remain. |
| A new prediction algorithm was discovered | Not supported; verified 1998 DC-1b prior art matches the causal two-sample predictor family. |
| Physical unsteady-wake or 5,000-drone real-time capability | Not established; prescribed 2–4 vehicle inputs, mean source model and receiver0 load timing only. |
| Earlier M31 long-flight trajectory discrepancy resolved | Not tested/resolved here. |

All underlying raw records and unfavorable cases are preserved. No post-outcome model/source patch, parameter change or rerun occurred.
