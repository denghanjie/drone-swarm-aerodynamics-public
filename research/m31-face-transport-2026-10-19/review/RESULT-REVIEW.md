# Saved surface-transport result review

19 October 2026. Saved-result interpretation only. This pass read the current comparison, selected saved face-local arrays, independent audit, control/execution/supervisor receipts and source-publication record. It rechecked file byte identities against the frozen source manifest. It did not recalculate integrands, quadratures, errors, admission, summaries or controls, run a new diagnostic, rerun any scientific source, or modify a frozen file. This review is the only file authored in this pass.

**Disposition:** the sole evaluator and independent auditor completed successfully. The fixed model has smaller integrated radial-transport magnitudes than the conditional measured reconstruction on all twelve full-grid inner/outer faces. Opposing errors cancel between surfaces in every full-grid region; some also cancel within individual faces. This is an exposed-field mismatch under the declared geometry and measurement assumptions. It is not an improvement, a verified physical cause, independent physical validation or a novel conservation result.

## Full-grid boundary evidence

All six regions passed the saved model-domain admission, with zero issues and zero failed nodes in every region. The completed audit checked all 1,220 selected model nodes, their preserved fields and integration radii, both resolutions of each region, and all 48 oriented face records. Admission did not remove unfavorable nodes or faces.

The following signed values are transcribed from the saved full-grid records, rounded for display. They use the saved dimensionless transport normalization; they are not independently calibrated SI flow rates. Negative inner values denote the declared inward boundary orientation. The magnitude comparison holds for each of these twelve integrated radial terms, not necessarily at every individual sampled point.

| Region | Inner measured | Inner model | Outer measured | Outer model |
|---|---:|---:|---:|---:|
| left-lower | −0.131330720 | −0.044382325 | +0.087769598 | +0.031529794 |
| left-middle | −0.087886769 | −0.036568716 | +0.120974461 | +0.042944655 |
| left-upper | −0.075412876 | −0.031696414 | +0.143640459 | +0.049230881 |
| right-lower | −0.218257344 | −0.044352004 | +0.182685532 | +0.031586018 |
| right-middle | −0.144818250 | −0.036538535 | +0.255412755 | +0.042976684 |
| right-upper | −0.109687362 | −0.031667181 | +0.213263516 | +0.049246797 |

For example, the right-middle outer face stores measured transport 0.2554127551915952, model transport 0.04297668447239781 and signed error −0.21243607071919737. This direct face comparison must not be replaced by the much smaller net model balance.

## Integrated errors and cancellation

The table below transcribes full-grid normalized errors and saved cancellation quantities. Both fractions use the same saved observed denominator: the sum of absolute **integrated** measured face terms. The cancellation columns are raw saved normalized-transport quantities, not fractions.

| Region | Face-vector fraction | Sampled local-error fraction | Between-face cancellation | Within-face cancellation |
|---|---:|---:|---:|---:|
| left-lower | 0.1550760142 | 0.1770541319 | 0.2700520455 | 0.0412525674 |
| left-middle | 0.1106716262 | 0.1120081265 | 0.1478886881 | 0.0025878634 |
| left-upper | 0.1059848088 | 0.1059848088 | 0.1710435929 | 1.1102230246e−16 |
| right-lower | 0.1971998340 | 0.2244552031 | 0.3478106798 | 0.0627608959 |
| right-middle | 0.2273461099 | 0.2273461099 | 0.4442067739 | 0 |
| right-upper | 0.1822929092 | 0.1838410808 | 0.3890182225 | 0.0035359190 |

Across the six full-grid outcomes, the face-vector fractions span approximately 10.59848–22.73461% of the observed denominator. The sampled local-error fractions happen to have the same endpoint range, but the two quantities differ within several regions. These percentages are error normalizations, not “model accuracy” percentages. The denominator includes large axial through-flow terms and can obscure the size of a relative radial discrepancy. No new radial-only denominator, pooled score or physical threshold is introduced here.

Between-face cancellation is positive in all six saved full-grid records. In right-middle, for instance, sumAbsoluteFaceError is 0.5565535151223825 while errorSum is −0.11234674118742767; the saved betweenFaceCancellation is 0.44420677393495483. The near-zero modelDefect, 0.00002416167420803833, therefore does not imply agreement with individual measured surface transports. The chosen model completion already imposes a continuity relation; small numerical net balance and accurate boundary transport are different requirements.

The right-lower top face shows clear sampled within-face cancellation. Its saved localSignedError array begins with positive values and ends with negative values. The signed integrated error is −0.016425609598679447, whereas localAbsoluteError is 0.07918650551936726 and withinFaceCancellation is 0.06276089592068781. This supports the stated cancellation of sampled errors on that face. J remains the trapezoid of absolute nodal errors, not the exact continuous absolute-error integral between sign changes.

Tiny signed cancellation values near machine precision are preserved as stored. For example, some face-level cancellation values are slightly negative, and the left-upper coarse aggregate is −1.942890293094024e−16. They are within the declared numerical tolerance and should not be clipped or presented as a physical negative cancellation effect.

The saved coarse comparisons and coarse-minus-full differences remain part of the result. For example, left-lower stores fraction changes +0.001953700775025935 for the face-vector measure and +0.004050266316967227 for sampled local error. They describe the one fixed coarsening operation on inherited endpoints. They do not estimate experimental uncertainty, prove convergence or improve the model. This review has not recomputed or extended that sensitivity check.

## Interpretation limits

“Measured radial transport” here means the saved off-axis planar reconstruction under axisymmetry and zero mean swirl. The result does not establish those assumptions, calibration, component normalization in actual preprocessing, stitching quality or experimental uncertainty. The whole inherited experiment was already exposed, and the gain and model fields were fixed in preceding work. No coefficient was updated and no model was improved in this cycle.

The saved face mismatch does not identify a physical cause or prove a particular parameter correction would solve it. Between-face and within-face cancellation are algebraic descriptions of these sampled errors, not causal attribution. Boundary weighting and the observed through-flow denominator differ from the earlier whole-field lateral RMS diagnostic; the current results are not a decomposition, replacement or improvement of that score. No new physical acceptance/rejection threshold, p-value, uncertainty interval or novelty claim is supported. The result also makes no statement of receiving-force accuracy, flight performance or swarm safety.

## Provenance, preservation and bounded execution

The evaluator supervisor records exit code 0, no timeout and no output-cap breach, with elapsed time 0.13756583258509636 seconds and 4,018,793 saved bytes before its receipt. The audit supervisor records exit code 0, no timeout/cap breach, elapsed time 0.19534491654485464 seconds and 4,022,234 saved bytes. The saved nine-item control receipt passes. These are existing receipts; no controls were run during this review.

The independent audit records `passed:true`, `complete:true` and `scientificStatus:completed-face-transport`. It checked 3,240 original cases, 1,220 selected model-node admissions and copied model nodes, twelve comparisons, 48 oriented faces and 568 face-local node occurrences with repetition. It records 117,896 recursive binary64 preservation checks and preservation of the entire inheritedAnnular result. Its predecessor pins bind the exact annular and crossstream results to their published source/result and earlier independent-audit/execution chains.

The auditor used Decimal60 nodal weights with the exact saved annular coordinates and unchanged saved model fields. It retained measured integrals, scale and defect as saved references; the report explicitly records zero measured quadrature recalculations, zero new square roots, zero fits and zero model-field evaluations. The 2e−12 tolerance is numerical consistency only. `admissionFailureHasNoModelNodesOrTransports:false` is expected because admission passed, not an audit failure.

The source-publication record binds source commit `de517a53e8084dd091522ae653e4fd84e7d7f267` to its separately retrieved exact-public manifest, with local/committed byte equality and 43 verified file pins before execution. This review rechecked current byte identities against all 43 saved manifest entries; all remain unchanged. That is a file-integrity check, not a second scientific audit or a new remote retrieval.

| Saved artifact | Bytes | SHA-256 |
|---|---:|---|
| source-manifest.json | 8,579 | `2105e6162e0d8b06dd0b09b593ef632f1ecb6c72ae839d79250fa26c44f04d72` |
| source-publication.json | 870 | `e071b180af5250900c6dc7a4bbf10dc02602f2da7408a958d32b384ce28f7c2b` |
| results/comparison.json | 3,868,464 | `f7efadfe741c1bd678f1d633ea101a2fe792bb141c8126619ea86f18c961bf7a` |
| results/admission.json | 144,825 | `4c198f6f72df477b197f82ece90a4b7e16a77b34623ad98c432e6112fc450f1a` |
| results/audit.json | 3,014 | `28a32a9f3451029357a448a62d9c7b25bb7172e719847cd3bab3e04f33c709db` |
| results/execution.json | 224 | `0153082b5382f427dca825b4d3cdfc96fc326ed5724e358fd23ec957ab1f30f9` |
| results/evaluate-supervisor.json | 206 | `ad4a9589ca97fd22dadc6e3987a04a092c57002fdcccf97e2e774bbb600d135f` |
| results/audit-supervisor.json | 203 | `52599b0c1197b0021b93b95e60e3264b2e2cc7dcb1215e3013b8454e18e68b9b` |

Result publication and display review are separate stages. This document does not assert that either has completed. Its conclusions are limited to the saved scientific outcome and provenance reviewed above.
