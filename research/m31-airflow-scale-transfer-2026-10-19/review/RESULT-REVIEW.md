# Saved scale-transfer result: interpretation review

19 October 2026. **Accept this as a completed, independently audited within-dataset transfer diagnostic. The result materially weakens an interpretation that the earlier unscaled amplitude discrepancy rejected Model A's underlying measured-plane spatial profile.** One empirically fitted scalar carries from the near calibration band to both farther evaluation bands. It remains an empirical correction, not a physically identified or deployable velocity calibration.

This reviewer read the saved comparison, audit and two supervisor receipts only, then performed metadata/hash operations and wrote this note. No fit, rescoring, raw-data decoding, additional cases, prior wake evaluation or browser execution occurred. Both scientific allocations are closed.

## Saved evidence

The source commit is `1eb9841b70362923a4f7ffacde13af439d46dcf3`; the parent reports exact-public verification at 08:46:32 UTC before launch. The saved independent audit reports 23 verified source pins, preservation of input/source/results, 25,920 exact original binary64-word checks, two calibration-only gains, 6,480 corrected predictions and sixteen metric groups. It explicitly records that no evaluation cells entered calibration and that neither physical calibration nor independent physical validation was established. Both supervisors report exit 0 with no timeout or output breach: evaluator 0.09061216656118631 seconds, audit 0.11949783470481634 seconds.

The fit used exactly 800 near-band cells. The fixed evaluation contains 2,440 cells, split into 1,640 middle and 800 far cells. All are spatially correlated samples of one already-exposed stitched mean field; they are not independent experimental trials.

Values below are copied from saved summaries, rounded for display. NRMSE is the whole-field residual norm divided by measured signal norm, not average pointwise percentage error or an uncertainty bound. MAE and bias remain in the predecessor's reference-speed units; bias is predicted minus measured.

| Candidate | Near-band gain | Corrected evaluation NRMSE | Corrected evaluation MAE | Corrected evaluation bias |
|---|---:|---:|---:|---:|
| A: current axial interpretation | 0.545009 | 0.098043 | 0.023621 | −0.001338 |
| B: published planar reference | 1.117278 | 0.296402 | 0.075377 | −0.067135 |

A's evaluation MAE changes from 0.22325522730650763 to 0.023621408583267816, with saved relative reduction 0.8941954960327181 (about 89.42%). That before/after reduction is conditional on the predecessor's reference-speed convention. The corrected NRMSE, by contrast, is invariant to a common positive multiplicative change of the observed velocity scale with the prescribed gain re-estimated.

A's corrected NRMSE is 0.10496705415069685 in the middle band and 0.07777667219779479 in the far band; its near calibration value is 0.20468348297214697. The transferred gain therefore works across both farther bands in the recorded aggregate metrics, while the appreciably larger near-band residual prevents describing the scalar as an exact explanation across the full window. No calibrated accuracy threshold was set, so these are measured discrepancies, not a physical pass/fail decision.

## Revised interpretation

The preceding unscaled test correctly reported an amplitude discrepancy under the assumed shared speed convention. It did not separate that convention from spatial profile error. This new result demonstrates that a single near-band amplitude adjustment removes much of the farther discrepancy while leaving the spatial pattern unchanged. That supports retaining A's spatial profile as a candidate for this measured plane and range, rather than rejecting it on the earlier raw error alone.

The corrected ranking also differs from the raw comparison: A is now closer than the separately gain-adjusted B on the prescribed evaluation endpoint. This is not evidence of general predictive superiority or a fair independent contest. B's published coefficients were already fitted to this experimental study; the reconstruction's correspondence to the original fitting procedure remains unresolved. Its remaining corrected residual and negative bias do not establish an error in the paper or data. They do mean that its earlier lower raw MAE did not justify adopting it as a replacement three-dimensional wake.

The gain 0.5450089857597356 is a descriptive nuisance parameter. It could absorb reference-speed scale, model amplitude, operating-point or observable differences. The source's original speed-magnitude observable and this project's mean downward-axial interpretation remain distinct. A near-half fitted multiplier is not proof of an omitted four-rotor term or any other physical factor. The inspected multi-vehicle plotting scripts process separate magnitude fields and do not reveal how the single-vehicle u_piv field was normalized. Their formula cannot calibrate this single field.

These exposed, correlated cells provide no blind holdout, independent replication, statistical significance or uncertainty-calibrated model validation. Low mean bias does not eliminate local residuals. The result covers the selected measured plane, not every height, a three-dimensional wake volume, receiving-rotor lift, interacting wakes or a flying swarm. The descriptive transfer is useful evidence; it is not a novelty proof or a runtime gain recommendation.

## Concrete next evidence requirement

The next required evidence artifact is a traceable **single-vehicle PIV normalization record**, connecting dimensional mean axial velocities in m/s to the released u_piv values. It must identify the exact release/processing version, coordinate origin and rotor-row plane, displacement/time/spatial calibration, any stitched-section scaling, the induced-speed formula actually used, measured source thrust or operating point, air density, rotor count and total rotor area. A numerical factor inferred from the current residuals or copied from the multi-vehicle scripts does not satisfy this requirement. No author contact or new acquisition is performed by this review.

Before adopting a physical amplitude or changing the runtime model, require an independently calibrated single-drone axial profile/map with matching geometry and documented operating point. Derive its velocity conversion from external metadata, freeze it before examining its measured profile, and evaluate the unchanged declared candidates without fitting a new gain on that evidence. Preserve calibration/systematic uncertainty and repeat-run information as experimental evidence rather than substituting grid-cell counts. The present 0.545009 gain may remain an explicitly empirical candidate; demonstrating its numerical success here does not turn it into an externally calibrated constant.

If that normalization evidence is unavailable, the justified next state is a retained empirical planar candidate with unresolved physical amplitude. Re-fitting the same exposed field cannot resolve that identification gap. Any additional diagnostic, independent measurement comparison, force transfer or model adoption needs a separate specification and allocation; none is authorized by this result review.

## Evidence binding

The saved audit binds the new comparison to 1,766,917 bytes and SHA-256 `027165cb42fe4445496779d3f4cdb87a902248d38cdf9a8ddc4adfa1b042d269`, and the unchanged original comparison to 1,112,834 bytes and SHA-256 `dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3`. Its new source-manifest SHA-256 is `1fc97a9f74b5f2372d2d67ae1f9f873f2c92c04b68f960147504cd19df293a55`. The review handoff records direct metadata hashes of the four read outputs and this note; no scientific quantity is recomputed by those hash operations.
