# Saved-result review: paired lateral residual components

19 October 2026. **Most of the unchanged primary residual is in the opposite-direction paired component: 84.03% of its squared-error sum, versus 15.97% in the same-direction component. All 2,440 previously included primary locations were paired.** The result describes the existing error; it does not improve the model or identify its physical cause.

The sole evaluator, independent saved-result audit and sole UI allocation completed successfully and are closed. This reviewer read retained result/receipt summaries and current conclusion documents as text, inspected file metadata/hashes and wrote this review. No pairing, numerical metric, fit, old scientific code, field evaluation, parser/checker or browser was rerun. Values below are transcribed from saved records. The frozen PROTOCOL-REVIEW.md remains unchanged.

## Retained support and numerical result

The accepted graph contains 1,611 pairs covering 3,222 records overall. The 17 prior exclusions remain excluded; one additional prior-included near record has no eligible counterpart. There are no axis or ambiguity exclusions. The primary region has 1,220 pairs covering all 2,440 prior-included cells, with no newly dropped primary locations. Middle and far also retain complete prior-included coverage; near retains 782 of 783 previously included cells in 391 pairs.

The saved maximum primary coordinate mismatch is 0.001341538461538505 in X units, inside the fixed .01 admission. Original coordinates were not moved. This mismatch remains nonzero, so E/O must continue to be called paired sum/difference components on approximately mirrored support, not exact parity of a measured continuous field. The mismatch is not a measurement-error bound.

| Fixed region | Pairs | Coverage | Saved E squared-error share | Saved O squared-error share |
|---|---:|---:|---:|---:|
| Primary, Z>=12 | 1,220 | 1.0 | 0.15973756334998876 | 0.8402624366500112 |
| Near, Z<12, descriptive | 391 | 0.9987228607918263 | 0.14169832691938788 | 0.8583016730806121 |
| Middle, 12<=Z<20 | 820 | 1.0 | 0.18088552211729336 | 0.8191144778827065 |
| Far, Z>=20 | 400 | 1.0 | 0.08510677455358276 | 0.9148932254464172 |

These are pooled squared-residual shares, not averages of local percentages, fractions of measured airflow or physical kinetic energy. They do not give independent-trial confidence or error probabilities. The near/middle/far results show the same descriptive O dominance on their fixed supports; their numerical differences do not establish a monotonic downstream trend or isolate a changing physical mechanism. Band endpoints remain selection limits rather than claims that measurements reach every endpoint.

Primary saved component RMS values are:

| Component | Observed RMS | Predicted RMS | Error RMS |
|---|---:|---:|---:|
| E, same direction | 0.004695223095166327 | 0.0000021835298886483414 | 0.004695174191776087 |
| O, opposite directions | 0.014639787684986838 | 0.003936218285901333 | 0.010768511004023104 |

The candidate's O component has a smaller RMS norm than the observed O component and leaves a substantial O residual. This is an aggregate amplitude discrepancy. It does not prove that every pair is underpredicted, that predicted and measured profiles are related by one constant multiplier, or that a particular coefficient/normalization is wrong. No multiplier or alternative model was fitted here. The small but nonzero predicted E was retained as required; it was not forced to zero. Its small size does not bound the effect of coordinate mismatch on the unknown measured field's gradients.

Primary direct SSE is 0.3367333954411241, partitioned into E SSE 0.053788972086333375 and O SSE 0.2829444233547907. The paired candidate RMSE is 0.011747573789293128, exactly the earlier full-field primary value. Because every primary cell was paired and all predictions were preserved, there is no primary support change masquerading as improvement. The prior baseline RMSE 0.015374280580725576 and prior 23.59% reduction remain inherited facts, not an additional gain from this checkpoint.

## Side summaries and limits of attribution

The saved primary candidate RMSE is 0.007098017997372147 on the left and 0.015020956040770339 on the right; their corresponding zero-baseline RMSE values are 0.010839348084671024 and 0.01884795850613773. Candidate signed bias is +0.0053370123193692935 on the left and -0.013493336719406833 on the right, while the joint bias remains -0.0040781622000187695. The baseline and candidate use identical paired support for these comparisons.

Those side differences are useful descriptive context but do not identify unequal thrust, sensor bias, drift, swirl, centering error or another cause. The same spatially correlated stitched experiment supplies all of them. There is no measurement-uncertainty model or independently calibrated component reference. A nonzero E component can coexist with a dominant O residual; neither finding invalidates the other, and pooled bias alone was insufficient to distinguish their roles.

E is a separate value for each pair and can vary with radius and height. The E share is not evidence for one uniform background velocity. O dominance is also not an empirical verification of exact antisymmetry or axisymmetry: it is a statement about the saved prediction-minus-measurement residual under the frozen matching and center convention.

## Why a constant additive sideways correction is insufficient

For the fixed pair support, adding the same constant c to both saved predictions would change residuals from e_R,e_L to e_R+c,e_L+c. Therefore

    new errorE = errorE + c,
    new errorO = errorO.

This cancellation is exact algebra and does not require the two coordinates to be perfect mirrors. A constant additive x-velocity offset can alter only the same-direction component; it cannot remove the dominant opposite-direction residual. Even allowing an arbitrary same-direction correction separately for every pair would leave O unchanged. The saved O SSE therefore remains an unavoidable contribution under that restricted kind of correction. The 84.03% share is a statement about the current squared-error sum, not the percentage of RMSE that a hypothetical correction would retain or remove. No such correction, optimum offset or hypothetical score was calculated.

A single constant cannot in general remove all E either, since E varies across pairs. This result rules out a constant additive velocity offset as a complete repair on the fixed support. It does not rule out ambient crossflow as a physical influence: crossflow could reshape or displace a wake rather than simply add one constant to its velocity values. Center shifts, geometry changes or changed flow dynamics would be different hypotheses requiring separate evidence and prospective tests, not consequences established here.

## Next decision: check the closure's premises before adding coefficients

The recommended next step is a targeted source-faithful review of the link between the axial model and lateral closure. The existing analytic derivation, fixed continuity controls and independent Decimal audit already support the implemented formula under its declared assumptions. Repeating the same algebra without a specific source/definition question would add little. The unresolved question is whether those assumptions and definitions describe this measured field and its normalization.

The review should reconcile the following without choosing a coefficient because it improves these exposed results:

1. **Observable and geometry.** Confirm which source quantities are mean speed magnitude, downward axial component or radial component; retain the actual Y=1 measurement plane, declared center, signs and all motor/rotor/arm-length definitions. A speed-magnitude fit used as a directed axial field is an additional modeling assumption.
2. **Width, spread and axial evolution.** Trace the half-width/profile convention, spreading parameter and virtual-origin definition into the same physical coordinates. The closure depends on how axial speed and width change with height, not just how closely axial values fit selected cells. Width/profile coefficients and coordinate conversions cannot be exchanged independently without changing that relationship.
3. **Velocity normalization.** Confirm whether the single-source measured u and v share the documented reference-speed and preprocessing chain. Retain the existing unresolved normalization limit if the relevant source processing is unavailable. A separate fitted lateral scale would not establish an instrument conversion.
4. **Published radial expressions.** Compare the distinct RSS 2025 Eq. 6 and 2026 merging-jet Eq. 9 using their full definitions and premises. Do not silently substitute one expression, omit or insert a spread factor, import a different fitted S, or borrow another experiment's height/length convention merely because the current O norm is small.

A strong match to recorded axial values does not by itself guarantee accurate spatial derivatives or the radial integral required by the continuity completion. Thus the earlier axial success and present lateral mismatch can coexist without a contradiction in the arithmetic. This does not establish which premise fails or prove that the radial relation is physically wrong.

A further limitation matters if the source check leads to a measured-axial-shape diagnostic: the off-axis Y=1 plane never samples the cylindrical axis or the R<1 central core, whereas the regular-axis continuity integral begins at R=0. The plane alone cannot provide a measurement-only radial reconstruction without an explicit core extension and axisymmetry assumptions. Spatial differentiation can also amplify measurement and stitching noise. Any proposed derivative, width, centerline or reconstructed-flow comparison needs a separate prospective protocol with those assumptions and support limits stated before numerical work. This review performs or authorizes none of those computations.

If the source check establishes a genuine definition or implementation mismatch, document the correction on source grounds and freeze a new bounded test before scoring it. If definitions remain consistent but their applicability is unresolved, retain that uncertainty rather than manufacture a missing-factor explanation. Independent calibrated evidence and the single-PIV normalization chain remain necessary for stronger physical conclusions. No production vector-field adoption, receiving-force inference or swarm validation follows from this component decomposition.

## Completion and provenance evidence

The retained source receipt identifies commit `997d194fca428ce6145b5d438c2e0ae7d499d9dc`, manifest SHA-256 `4a593847a852c99ba56b5ae943b3eca4ab869b94001fc67812381779eb2ed14b`, and 25 verified pins. It records exact remote/local plus committed/local manifest equality at `2026-10-19T12:16:11.930220+00:00`. This reviewer read that receipt and did not perform another network retrieval. The prelaunch documentation-pin correction remains preserved in history; the executed source is the corrected public identity.

The evaluator supervisor records exit zero, no timeout/output breach and elapsed 0.13628791645169258 seconds. The independent audit supervisor records exit zero, no timeout/output breach and elapsed 0.1890992084518075 seconds. Both satisfy the separate fixed 60-second, 16 MiB scientific limits. The fixed control receipt reports all eleven declared checks passed.

The audit reports 3,240 original cases, 1,611 pairs, 32,070 eligibility comparisons, four region summaries and 24 side metric groups checked. It confirms exact preservation of 48,615 copied binary64 values across the predecessor case/metric trees, the inherited gain, and source/input/result bytes. Its independent graph and residual-first Decimal60 computation agree with the saved matching and component summaries under the fixed numerical tolerance. There are zero new fits and zero new field evaluations. Numerical preservation and audit precision are not measurement accuracy or independent experimental validation.

The sole UI receipt also reports seven groups passed, including six modes, saved metric/coverage consistency, sparse glyph counts, desktop/mobile captures, orbit/reset, corrupt-evidence refusal and console/page/HTTP health. Its supervisor records exit zero, no timeout/output breach and elapsed 2.836713083088398 seconds under the separate 60-second/32 MiB cap. The parent reports inspection of desktop, mobile top/scene and E/O screenshots with legible rendering and no private material. This reviewer read the UI receipts but did not inspect those images or run a browser.

The evaluator, audit and UI allocations are consumed and must not be rerun or extended. Their saved outputs and all earlier checkpoints remain intact. Final result publication is a separate finishing step; this review does not assert a result-publication receipt that it has not read. The overall research objective remains incomplete.

## Reviewed saved identities

Paths are relative to this package. The sole inherited input retains the pin from the frozen protocol and passing audit.

| Saved file | Bytes | SHA-256 |
|---|---:|---|
| `results/comparison.json` | 3793293 | `b253b7199df24e8a2d5ff3000bed1f73937cd898ada8449256c91f0172962be3` |
| `results/selection.json` | 531679 | `251213298c8433600dbb14797dfaf8268d6ba1405df61ccb391d373656f6bf1c` |
| `results/audit.json` | 3181 | `8c1642721535338876f3bc643a98d2cb2d2a257e3924c08cf370cf0a7586e007` |
| `results/execution.json` | 174 | `ea2fc425596ca44f9e1848b63cc3bd62343cdd0e5667c9d3c7410847688b238f` |
| `results/evaluate-supervisor.json` | 206 | `a48c1057864ae4e3b22d733826928b37be903211a315b47c0ed847cea037ef2b` |
| `results/audit-supervisor.json` | 202 | `618330d8ca274c17f114afd3c8a605bb789a94c97281720ef6b9757f781b71a6` |
| `results/controls.json` | 430 | `9b50c11b924826eb6d8593151e2074e2ad2ec335b0a02d3463155f8e649e7bd3` |
| `source-publication.json` | 861 | `b2548a812f80c9af716ced76f35502dcf5d3c14e6bcdf0b98bfbec419b6471be` |
| `ui/qa.json` | 756 | `4c22d5fe4f5b44993f3505e98eb0048b9abdcc105b77f29b97616b9822f4be83` |
| `results/ui-supervisor.json` | 198 | `b78dcb651fd3b17bbdc64b63868a0105f43655babd438e3496511c93fcc655d0` |
