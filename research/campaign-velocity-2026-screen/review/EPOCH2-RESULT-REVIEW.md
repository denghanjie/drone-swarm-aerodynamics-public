# Independent saved-result review

2026-10-15 UTC. **PASS for saved-result consistency and stated scope.** This is not a physical validation decision. The six fixed-nominal predictions exceed their paired published centerline values by 0.629–0.760 m/s. The approximately self-similar pair near z/l=15 still has nominal differences of 0.720 and 0.732 m/s.

## Evidence checked

EPOCH2-RESULT.json: 11,196 bytes, SHA256 `eaf189fa69b2b74913c741e6ac58c8e373956d034898807cd803c7f9e702c1fe`.

I independently checked all six saved records against the frozen measurements, the manifest and every hash-bound input/output, release and evaluator hashes, and immutable public kernel bytes. The original plan/adoption and stopped first-epoch receipt remain unchanged. The supervisor receipt reports exit 0, 18 calls, empty stderr and no timeout; the evaluator source makes three calls per selected point. Its 0.060 s wall time is incidental execution metadata, not a performance benchmark.

No collector, evaluator or wake function was rerun. Saved q values were not regenerated through a copied formula. This review independently recomputed their subsequent scaling, paired differences, interval operations and group summaries.

## All six nominal comparisons

These use observed 4.36*v and predicted U_H*q, with U_H=4.373329400265024 m/s. Differences below are observed minus predicted.

| Gold ID | z/l | Observed m/s | Predicted m/s | Difference m/s |
|---|---:|---:|---:|---:|
| 12 | 6.615031 | 4.085328 | 4.845667 | -0.760338 |
| 13 | 7.141514 | 4.023913 | 4.709790 | -0.685877 |
| 20 | 10.826885 | 3.307594 | 3.937010 | -0.629416 |
| 21 | 11.353368 | 3.197510 | 3.846840 | -0.649330 |
| 27 | 14.512259 | 2.662328 | 3.382079 | -0.719751 |
| 28 | 15.038739 | 2.583357 | 3.315322 | -0.731965 |

The nominal length mapping is opposite-motor D=0.092 m from l=0.046 m, true axis r=0, with axial argument (z/l)/2. The saved normalization obeys kappa=U_H/4.36=1.0030572018956476. Primary normalized predictions correctly use kappa*q. Comparing unscaled q directly with v would discard the declared nominal normalization correction.

## Paired interval verification

For every point, the center difference equals v-kappa*q. Bounds equal [v_low-kappa*q_high-1e-12, v_high-kappa*q_low+1e-12]. Each observed value remains paired with predictions at its own coordinate and coordinate endpoints. All saved q intervals contain their centers in the stated decreasing order. Dimensional observed, prediction and difference fields follow their separately declared scales; all downstream operations match exactly in the independent calculation.

The three neighborhood unions are correctly formed from their respective two paired intervals. Their hulls contain no substituted cross-point comparisons. All six residual upper bounds are negative under the chosen graphical envelopes. This establishes separation of the specified nominal graphical ranges, not an experimental confidence statement. Shared calibration dependence is still present; a hull is not a simultaneous uncertainty distribution.

## Scientific reading and limits

The published gold markers concern mean axial PIV velocity in [Kiran et al., arXiv:2608.30900v1](https://arxiv.org/html/2608.30900v1), a preprint. The unchanged [Bauersfeld v3 model](https://arxiv.org/html/2403.13321v3) was calibrated using omnidirectional mean-speed measurements. Mean speed magnitude and mean axial velocity differ under fluctuations, even on the mean axis; the observed direction of the discrepancy does not identify its cause.

Keep the 7/11 developing-profile points separate from the approximately self-similar 15 pair. The latter shows that the nominal discrepancy is not confined to the two developing windows. This does not isolate a model-law error, establish a universal bias, validate a corrected coefficient or quantify physical uncertainty. Export history, symbol placement, PIV error, nominal geometry/scaling and measurement-quantity mismatch remain unbounded here.

The predeclared +/-0.01 SVG-unit envelopes support graphical sensitivity reporting only. They cannot serve as a physical-accuracy target or an uncertainty budget for allocating simulation precision. No fitting, new swarm flight, source aggregation test or physical/statistical pass/fail is supported by this screen.
