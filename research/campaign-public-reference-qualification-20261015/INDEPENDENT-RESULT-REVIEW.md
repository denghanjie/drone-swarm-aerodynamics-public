> Public edition of the preserved original, SHA256 `a7c8cfbb9e34b23142a8911ab95e06e56d38d42861e4fea6db33771c30c7ed44`. Result-review excerpt; the separate prospective next-hypothesis section is omitted. No completed-result finding changed.

# Independent qualification-result review

2026-10-15 UTC. **The saved result is internally consistent and remains GATE_STOP.** The air64 angular-rate error exceeds the frozen absolute budget; cadence refinement itself improves all four state-error families by almost a factor of two. This is a resolved numerical hold-lag signal in the observed case, not worsening convergence or evidence of physical accuracy. No model, collector or campaign was rerun.

## Exact stopping reason

Summary SHA256: `f5cd17150fc487220d95b5a601857758f5c5c9cc04053a45ea94685a025f3e36`.

The combined gate hold-reduction-840131-64 failed only angularVelocityRadps: 0.013884418690814795 rad/s versus the declared 0.01 rad/s cap, 38.84% above it. Its worst retained witness is drone 7 at tick 4352, t=0.085 s. The cadence reduction condition passed: 0.0138844/0.0277694=0.4999898, below 0.7. Position, velocity and attitude passed both parts of this gate.

Compatibility, both joint-convergence/exposure gates and all three seed 840131 held-physics gates passed. There are 13 completed runs including compatibility: six joint and six held scientific rows. The six seed 840137 held rows were skipped. The already-computed air32 comparisons are descriptive evidence; later cadence/cross-family/attribution gates were not reached. eligibleForExtension remains false. Do not convert their favorable numbers into a retroactive campaign pass.

## Saved metrics and numerical scale

Maxima against joint32 for seed 840131, using held h8:

| Hold ticks (seconds) | Position m | Velocity m/s | Attitude rad | Angular rate rad/s |
|---|---:|---:|---:|---:|
|128 (0.0025)|1.84506e-5|5.37030e-4|1.60161e-3|2.77694e-2|
|64 (0.00125)|9.35471e-6|2.70042e-4|8.06384e-4|1.38844e-2|
|32 (0.000625)|4.71007e-6|1.35406e-4|4.04585e-4|6.94211e-3|

First-halving ratios across these families are 0.499990–0.507015; second-halving ratios are 0.499993–0.503497. The finest observed angular-rate difference is below the 0.01 cap, but the earlier mandatory gate still failed.

For the failed air64 angular metric, joint64-versus32 differs by only 2.41614e-8 rad/s; held h16-versus8 differs by 7.40422e-11 rad/s. The larger of these is 1.74018e-6 of the hold-error signal. Across every stored cadence/family, this empirical ratio is below 3.49e-6. These measured differences are not certified bounds on reference error, but ordinary physical-step noise or the 1e-7 rad/s screening floor cannot plausibly explain the observed cap failure. Joint fine differences for both seeds lie below every corresponding floor; no high-order convergence rate should be inferred from their near-floor values.

Incoming-held versus fresh inflow gaps on the controller grid also approximately halve: 0.0522650, 0.0261390 and 0.0130701 m/s. Corresponding within-arm roll/pitch moment gaps are 1.55945e-5, 7.81702e-6 and 3.91280e-6 N m. These are correctly sampled before refresh. They support a hold-lag mechanism, while closed-loop state/control divergence remains part of the trajectory error.

## What I verified independently

All frozen source hashes remain unchanged. The summary, comparison records, witness tensors and two saved reference tensors match their recorded hashes and shapes. The public compatibility prefix hash agrees with the original first 10,880 bytes; every arm of a seed has the same initial-state hash. Both 11 x 16 x 17 reference tensors are finite, with unit quaternions/nonnegative nominal motors and matching recorded initial/final hashes.

All 50 retained state-metric witness values reproduce with maximum absolute discrepancy 1.11e-16, using independent vector/quaternion arithmetic. Their joint32 rows match the reference tensor where controller-grid timestamps permit that cross-check. Twenty-nine terminal metric values can also be recomputed directly from retained witness states and agree. The remaining terminal values and the claim that no unretained sample has a larger error rely on the inspected frozen comparator; full all-arm common-grid streams were intentionally not retained. A correct worst-point witness does not independently prove the global maximum.

All 40 retained field/load difference witnesses and ten command-difference witnesses agree arithmetically. Every executed gate boolean follows its frozen caps, floors and reduction rule. Completed work counts are 3444 physical steps, 220416 vehicle derivatives, 2801 production fields, 132 auxiliary fields, two baseline comparisons and 121 controls, including compatibility. Endpoint/stage sample and pair counts agree with each arm's prescribed coverage.

The child returned 2 for the gate stop; the supervisor returned 1 without timeout. The whole launch took 2.735 s; its receipt reports 3.549 CPU seconds. Failure evidence correctly identifies a post-comparison gate stop, not an integrator crash. No retry or extension was released. These timings are resource observations, not a speedup benchmark.

## Exposure and inference limits

Both seeds have nonzero production inflow; maxima are 4.26047 and 3.23308 m/s. Across scientific runs, sampled pair clearance stays above 0.4486 m and obstacle clearance above 3.5928 m. There are no wall constraints, tilt clips, motor-bound hits or repair iterations. Seed840131 records pair constraints and four controller-neighbor changes; comparison branch-signature mismatch counts are zero. Sampled finite-jump/contact checks did not stop a run.

Maximum downstream extent is below 1.639 m, so this case does not exercise the 2 m axial fade or 2.5 m cutoff. Radial/support margins and sample-order changes do not establish continuous regularity. Held internal stages remain unaudited, and clearances are control-grid summaries rather than continuous minimum clearances. The short obstacle-free exposure cannot qualify a one-second reference or general update cadence. Numerical consistency cannot remove the separate 2026 amplitude/observable mismatch.

