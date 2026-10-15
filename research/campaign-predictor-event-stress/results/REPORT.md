# Numerical improvement, insufficient event exposure

**PREDICTOR-EVENT-STRESS-20261015 completed, but its prospective event-stress criterion was not met.** The causal predictor reduced numerical errors by 42.2–125.9 times at the same airflow-refresh count. However, the required reference, ZOH and predictor arms each had **zero strict wall-repair responses and zero eligible C1 support transitions**. The declared result remains `EVENT_EXPOSURE_INSUFFICIENT`.

## What was tested

One developmentally selected public seed, 840163, was translated by exactly +4.5 m in x and evolved for 0.5 s with 16 genuine own-state local-3D Boids. Its original initial-state hash was verified before translation. Joint whole-swarm RK4 at 128/64/32 ticks qualified the numerical reference first; ZOH and the unchanged causal stage predictor then each used physical steps of 16 and 8 ticks. Both used a 64-tick, 1.25 ms airflow refresh. The predictor retained its initial ZOH interval, actual RK-stage timing, history across controller events and nonnegative component clamp.

The single released attempt completed all seven arms in 15.129 s, with no timeout, source change or domain stop. Eleven of twelve gates passed; the event-exposure gate failed. The source remained the same physically unvalidated public model, not a recovered private reference.

## Literal numerical comparison

Maxima over 16 vehicles and 201 common times, with h8 approximations compared against joint32:

| Metric | ZOH | Predictor | Reduction |
|---|---:|---:|---:|
| Position, m | 0.000508432 | 0.00000498600 | 101.97× |
| Velocity, m/s | 0.00275892 | 0.0000219150 | 125.89× |
| Attitude, rad | 0.00187306 | 0.0000183628 | 102.00× |
| Angular rate, rad/s | 0.0212369 | 0.000502725 | 42.24× |

All four predictor errors met the unchanged absolute caps and fourfold target. ZOH exceeded the velocity, attitude and angular-rate caps, but its failure did not abort paired scoring or change any criterion. The largest numerical-resolution proxy/error ratio was 0.0002098, about 0.021%; this is a refinement diagnostic, not a certified error bound. Both methods' h16–h8 checks passed. One cadence does not establish coupling order.

The predictor's maximum angular-rate discrepancy occurred at vehicle 15, t=0.4125 s; its terminal angular-rate maximum was 0.000299157 rad/s. All H8/P8 versus reference controller branch-signature comparisons were equal on the recorded controller grid. Both approximate arms made 400 production fields, 51 auxiliary diagnostic fields and 50 controller calls. Their derivative count was also matched at fixed h. Predictor arithmetic adds work; no runtime speedup is claimed.

The scientific work totals were 11,000 steps, 704,000 vehicle derivative returns, 7,200 production fields, 357 diagnostic fields, one baseline field comparison and 350 controller attempts/returns. Compatibility added one field, one controller, eight steps, 512 derivatives and 12 scalar checks. No trajectory or diagnostic clamp was active.

## Why the event test remains inconclusive

Every arm listed 402 wall-constraint rows across 302 vehicle/controller occasions. All emitted before/after wall residuals were zero and no repair iteration occurred. Listing a wall is not evidence of the strict wall-response mechanism. Corrections already resolved in earlier projection passes are not excluded by this observation.

Each arm recorded 20 neighbor changes and 7,460 pair-constraint rows, so the simulation was not a rigid formation. Nevertheless, all radial-cut and axial-cut accepted-endpoint transition counts were zero. The requirement applied separately to J32, H8 and P8, and none qualified. There were no tilt clips, motor-bound events or speed-limit events.

The nearest downstream-only far-start margin in H8 was approximately 1.41e-8 m. That scalar does not indicate proximity to the eligible discontinuity annulus. The minimum saved joint distance in (downstream, radial) coordinates was approximately 0.45777 m. In J32, the downstream-only nearest tuple had radial distance 0.9710 m, whereas the outer radius at far-start is 0.15152 m. These are simultaneous saved geometry tuples, not unrelated minima combined into a claim. Sampled guards and margins do not prove continuous safety.

Minimum sampled body clearances were about 1.110 m to obstacles and 0.4837 m between vehicles. They describe this numerical case only.

## Evidence and review limits

The author checked the frozen source hashes; original and translated initial bytes; all 816 stored reference states; 35 paired state-metric witnesses; 28 field/load witnesses; seven command witnesses; 14 joint geometry tuples; and the recorded work/gate arithmetic. Maximum discrepancies from independent Python arithmetic were 1.11e-16 for state metrics and 3.89e-16 for geometry. These checks do not independently prove maxima or zero events over unretained dense stage history.

A post-run source-shape defect was found in the **unused failure writer**: stored wall normals have 17 entries, while its failure-column declaration and original shape proof assumed three. The successful run's native JSON preserves the actual arrays correctly. The failure-envelope/schema guarantee is unqualified, and future use requires correction and review. See [the retention erratum](RETENTION-ERRATUM.md); no frozen source was edited or rerun.

Original summary SHA256: `6efb79738c4c05e7eef033cae817ff5da5151ea01bb76d43bb21eb407fcf0d90`.

## What this adds

The earlier 0.1 s screen showed numerical improvement on two seeds. This translated 0.5 s case extends that numerical evidence to a longer, obstacle-near trajectory where three ZOH metrics exceed their caps. It does **not** demonstrate robustness to the specifically required wall response or support transition. Earlier stopped qualifications and physical-model amplitude discrepancies remain unresolved.

Causal polynomial extrapolation and hold fallback are established co-simulation techniques; no novelty is asserted. [CHOPtrey](https://arxiv.org/html/1610.09261v2) provides relevant prior art. The low-frequency analysis in [Chen et al.](https://link.springer.com/article/10.1007/s11044-021-09785-x) does not establish order or stability for this hybrid flock model.

A useful next contribution would require a separately adopted case with actual eligible event exposure and independently qualified numerical resolution, alongside correction of the failure schema. This outcome does not authorize an offset search, longer flight, retry or publication claim of event robustness.
