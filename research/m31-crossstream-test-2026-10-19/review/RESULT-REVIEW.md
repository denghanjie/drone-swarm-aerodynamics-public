# Saved-result review: signed cross-component diagnostic

19 October 2026. **The fixed continuity-derived candidate improves the saved lateral comparison against zero, without a new fit. The improvement is descriptive and incomplete.** The sole evaluator and independent saved-result audit completed successfully; both scientific allocations are closed. No production adoption or physical validation follows from this result.

This reviewer read saved result summaries, controls and receipts as text, inspected file metadata/hashes and wrote this note. No prediction, fit, metric, pair matching, parity decomposition, raw-array decoding, parser/checker or browser run was performed. Numerical values below are transcribed from the saved result or its receipts, not independently recomputed here. The independent audit supplies the numerical consistency check.

## What the saved comparison establishes

The inherited gain remains exactly 0.5450089857597356. The candidate adds the specified signed radial completion and x projection under the axisymmetric, regular-axis, zero-mean-swirl assumptions. It was not fitted to lateral v. The primary included region contains 2,440 saved locations at Z>=12. All 17 geometry exclusions are in the near region; there are no missing-lateral exclusions. Across all groups, 3,223 of 3,240 original records are included and every original record remains preserved.

| Saved group | Cells | Zero-baseline RMSE | Candidate RMSE | Candidate NRMSE |
|---|---:|---:|---:|---:|
| Primary, Z>=12 | 2,440 | 0.015374280580725576 | 0.011747573789293128 | 0.7641055935990152 |
| Near, Z<12, descriptive | 783 | 0.015686856090177347 | 0.01203026206885224 | 0.7669007734688941 |
| Middle, 12<=Z<20 | 1,640 | 0.0162875557299085 | 0.012648691776116966 | 0.7765862469400755 |
| Far, Z>=20 | 800 | 0.01330754554382122 | 0.009640459886573187 | 0.7244356109718005 |

The saved primary RMSE reduction is 0.0036267067914324477, with relative reduction 0.2358944064009848, conventionally reported as 23.6%. Primary MAE also improves, from 0.013339393742546331 to 0.009906866740937508. Thus the improvement is present in both squared-error and absolute-error summaries and in each prespecified group. The fixed near result is descriptive; its axial observations supplied the inherited gain. Middle/far group differences do not establish a monotonic downstream trend or uncertainty-qualified superiority.

The candidate NRMSE of 0.7641055935990152 means RMS residual remains about 76.4% of the measured lateral field's RMS signal under the selected equal-cell weighting. It does not mean 76.4% of points failed, each point has that percentage error, or a physical threshold was passed. Baseline NRMSE is one by definition when predicting zero against a nonzero target. RMSE and MAE remain in the archive's reference-speed units, with no demonstrated SI conversion. Selection-band labels describe protocol intervals, not proof of observed coverage through each interval's endpoint.

The useful conclusion is narrow: the frozen inherited axial scaling plus this known local vector completion describes these saved lateral values better than omitting lateral motion. It is evidence for retaining the candidate as an experimental hypothesis. It does not show that the closure captures all important cross-stream structure or that its remaining mismatch is acceptable for a receiving vehicle or a swarm.

## What the bias suggests, and does not identify

Primary signed bias changes only slightly: baseline -0.004078179848146051; candidate -0.0040781622000187695. The middle and far candidate biases likewise remain close to their zero-baseline biases. This is compatible with an odd-in-X candidate contributing little net mean over the sampled coverage while reducing a different part of the residual. It is not a measured symmetry decomposition and does not by itself prove lateral drift, a displaced jet, asymmetric thrust, swirl or a preprocessing offset.

The negative bias indicates underprediction of the selected field's signed average in the declared coordinate convention. That average depends on spatial support and weighting. A nearly symmetric finite grid is not automatically an exactly mirrored grid, and pooling can hide height-dependent or side-dependent structure. No physical explanation should be assigned to this aggregate statistic without a diagnostic designed to separate the relevant spatial components.

The leftover discrepancy has several unresolved possible contributors: the axisymmetric extension of the scalar axial model, its interpretation as axial rather than speed magnitude, mean swirl, nonaxisymmetric jet merger/loading, coordinate-center or measurement offsets, and unavailable preprocessing/calibration. Measurement uncertainty is not established here. No one contributor is identified by improved RMSE or persistent signed bias. Cross-component NRMSE also should not be compared directly with the earlier axial NRMSE as if their different target norms measured the same physical error scale.

## Recommended next same-dataset diagnosis

**A fixed-center, matched-geometry left/right diagnostic is more informative than another fit as the next use of these saved data.** It directly challenges the odd symmetry imposed by the candidate and helps distinguish the part of the measured field this closure can represent from the part it cannot. This is a recommendation for a separate prospective allocation; no such calculation has been performed or authorized by this review.

For ideal pairs at the same Z and coordinates +X and -X, the observed lateral pair can be decomposed into

    even part = [v(+X,Z) + v(-X,Z)]/2,
    odd part  = [v(+X,Z) - v(-X,Z)]/2.

The fixed candidate has zero even part on exact mirrored coordinates and a prescribed odd part. A nonzero observed even part would establish a discrepancy with that symmetry under the declared center and measurement mapping; an odd residual would describe mismatch within the component the candidate attempts to model. Neither determines a unique physical cause. In particular, on Y=1 an axisymmetric swirl contribution to v_x is even in X, but so can be lateral drift or other effects. An even signal would not demonstrate swirl.

Before any response arithmetic, inspect geometry alone and freeze pair eligibility, primary/secondary regions, equal-Z handling, one-to-one matching, coordinate tolerance, minimum support, unmatched records and signed endpoints. Do not assume row symmetry: saved edge X values read in this review include -3.848701538461538 and +3.847378461538461, which are not exact opposites. This observation is a reason to check geometry, not a completed pairing analysis. Keep the declared axis fixed rather than shifting it to improve symmetry or residuals.

If accepted pairs have small but nonzero geometric mismatch, retain the mismatch explicitly and compare the saved candidate's pair sums/differences with the measured pair sums/differences. Do not force the candidate sum to zero on nonmirrored coordinates. The resulting quantities describe the prescribed paired support rather than exact field parity. If exact symmetric support is unavailable, any interpolation, resampling or new center convention would need its own prospectively reviewed rule; do not silently widen tolerances, tune matches to v, or create apparent independent measurements by interpolation. Inadequate support is an admissible stopping result.

This diagnostic should preserve signed values, the inherited gain, original field pins and core admission. It should not add an offset, separate side gains, width/origin fit, fitted center, sign reversal or response-selected region. Keep raw and modeled pair components available so one favorable pooled score cannot hide an adverse side or component. Spatial pairs still come from the same exposed stitched mean field, so a larger pair count does not create independent trials or justify unmodeled confidence intervals.

This is the strongest immediate *same-dataset structural diagnosis*, not a substitute for independent scientific evidence. Establishing the single-PIV normalization/calibration chain and finding compatible independent calibrated measurements remain the main routes toward physical validation. Even a clean left/right pattern would not justify adopting a global production vector field, which still needs a consistent treatment of finite-support tapering and separate force/flight evidence.

## Execution, provenance and claim boundary

The source receipt identifies commit `b5a98584ce32f1cb2b11493dc259118192d94f85` and manifest SHA-256 `13eed106be087c9f158a8215542a1ac45003b0ffabd1dc9df9af67c070e35eb8`. It reports 35 verified pins and exact remote/local plus committed/local manifest equality at `2026-10-19T11:49:07.655920+00:00`. This review read that retained receipt; it did not perform another network retrieval.

The evaluator supervisor records exit zero, no timeout or output breach and elapsed 0.08657108433544636 seconds. The audit supervisor records exit zero, no timeout or output breach and elapsed 0.17455987446010113 seconds. Both are inside the separate fixed 60-second, 16 MiB scientific limits. The saved fixed controls report success. The independent audit reports 3,240 original records, 25,920 original binary64 words, 3,240 candidate records, eight metric groups, exact inherited gain, zero new fits, both predecessor receipt chains and preserved source/input/result bytes. Its separate 60-digit Decimal rational formula and metric checks passed the fixed 2e-12 numerical tolerance.

These receipts establish a completed bounded computation and an independently implemented consistency audit. They do not establish experimental uncertainty, an independent experiment, SI calibration, unique vector reconstruction, global continuity/momentum, receiving-force accuracy, safe flocking or novelty. The original lateral measurements were already exposed. The source-backed sign convention and missing preprocessing limitation remain as declared before launch; there is no reason to reverse the sign or reinterpret the target after seeing this result.

The first separate UI allocation also completed: its saved report records seven check groups, no errors, desktop 1280x1000/mobile 390x844 captures, four modes, orbit/reset, corruption refusal and saved-metric consistency. The UI supervisor reports exit zero, no timeout/output breach and elapsed 2.240555833093822 seconds under its 60-second/32 MiB cap. These are the retained automated results; this reviewer did not run a browser or independently inspect their images. The parent subsequently reported from screenshot inspection that the sparse arrows were barely visible. An automated pass does not settle that legibility concern.

The original viewer/source and first UI output must remain preserved. A separately frozen display-only revision may improve glyph size, sampling and contrast while consuming only a newly declared display allocation and leaving all scientific source/results/audit unchanged. That proposed revision is not yet accepted or executed by this review. No final result-publication claim is made here.

The evaluator and audit must not be rerun, tuned or extended under their consumed allocations. Preserve historical locks and all saved outcomes; the overall research objective remains incomplete.

## Reviewed saved identities

Paths are relative to this checkpoint package. The two inherited input pins remain the ones in the frozen protocol and passing audit.

| Saved file | Bytes | SHA-256 |
|---|---:|---|
| `results/comparison.json` | 2291932 | `1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a` |
| `results/audit.json` | 2445 | `a45d2384df611b9d6237d9f6c6f006753669307c2097a9a99a2d5e3b59dc43e8` |
| `results/execution.json` | 173 | `cd84f317b7579639516a1fd0eefd87983c1ff21d7331792477e77d88ca1a86f5` |
| `results/evaluate-supervisor.json` | 206 | `6bf688aaee4d4a333061d29ff90efa3c8374e52f16df63d18452fb4bac31da61` |
| `results/audit-supervisor.json` | 203 | `dc4cef83112dde026d9c6bdb2fc8b42ee4ab12cb52351f80f86fb6e660f86728` |
| `results/controls.json` | 457 | `ff8d16a19ccd7545b45d460fab541cd66d07747bce602c48bc15c9657e4f91c5` |
| `source-publication.json` | 861 | `19b59bfd8131db632cf6da3ffd2a7a15f39be0c091040826b259c148a755c677` |
| `ui/qa.json` | 731 | `004283fe294a584de3ff9484e8db2232ffa9ee8761ea18331c041ba5b1b398d6` |
| `results/ui-supervisor.json` | 198 | `575d4751cd207a0a329e0364736bca2ba65c2cffc30968c726b03e2931f185c7` |
