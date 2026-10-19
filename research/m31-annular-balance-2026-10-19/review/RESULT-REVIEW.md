# Saved annular diagnostic result review

19 October 2026. Saved-evidence interpretation only. This review read the existing comparison/selection records, control and execution receipts, independent audit, supervisor receipts and source-publication record. It checked file byte identities against the frozen manifest. It did not recalculate fluxes, projections, selection, statistics or controls, execute any scientific source, rerun an audit, or change a frozen file. This document is the only file authored in this review.

**Disposition:** the sole evaluator and independent auditor completed successfully. The six fixed reconstructions have descriptive net imbalances of about 1.1214–4.6144% of the sum of absolute integrated face terms. These are conditional internal-consistency results from the exposed planar measurements. They are not a physical acceptance test, independent validation, discovery or evidence that the reconstruction assumptions have been verified.

## Admission and saved outcome

The saved admission record passes with no issues. The upstream nonfinite-coordinate and missing-axial counts are both zero. All six selected grids have ten radial levels; each Z band has respectively 21, 20 and 20 axial levels on each side. The saved selected counts are 210, 200 and 200 per side, totaling 1,220; 2,020 inherited cases are outside the fixed windows. No selected grid has missing coordinates, duplicates or nonfinite components. These statements quote saved counts and the completed independent audit, not a newly recomputed selection.

The table transcribes saved scalars, rounded only for readable display. The fraction is signed total defect divided by the sum of absolute values of the four integrated faces. The last column is the saved coarse-minus-full change of that signed fraction.

| Side | Nominal Z band | Saved nodes | Full defect | Full signed fraction | Coarse-minus-full signed fraction |
|---|---|---:|---:|---:|---:|
| Left | [12,16) | 210 | −0.0210487871 | −0.0112141559 | +0.0007250818 |
| Left | [16,20) | 200 | +0.0664286115 | +0.0343070118 | +0.0008401063 |
| Left | [20,24] | 200 | +0.0344951001 | +0.0177912497 | +0.0003511044 |
| Right | [12,16) | 210 | +0.1062555979 | +0.0461439483 | +0.0016201823 |
| Right | [16,20) | 200 | +0.1123709029 | +0.0459023022 | −0.0003843190 |
| Right | [20,24] | 200 | +0.0273733845 | +0.0119852001 | −0.0005901381 |

The largest saved absolute signed-fraction change is the right [12,16) record, 0.0016201823393364664, or about 0.162018 percentage points. It is a fixed-coarsening sensitivity observation, not an estimated error bar, uncertainty bound or convergence result. No fraction is null in these six admitted full/coarse results.

The nominal windows are not their sampled integration endpoints. The saved left radial coordinates run from R=1.4762868056238843 to 3.0316967030142465; the right endpoints are 1.4753069858168502 and 3.030447704903718. The saved Z endpoints are [12.037476923076923,15.984184615384615], [16.181507692307694,19.930892307692307] and [20.128246153846153,23.8776]. Thus the two sides must not be called identical radial support, and adjacent nominal bands must not be presented as one gap-free sampled control volume.

The saved face-index arrays retain both endpoints in the prescribed coarse lists. Inner and top integrated terms are negative and outer and bottom terms positive in all six full records. The signed total is negative only in the left [12,16) record; its absolute fraction must not be substituted for its sign. The full raw face terms, node identities and integrands remain in `results/comparison.json`. The completed audit, rather than this interpretation pass, checked every corresponding numerical value.

## What the result does and does not establish

The annular calculation uses the two radial boundaries of each selected rectangle, so it does not need to assign an axial profile to the unobserved central disk. However, mapping the off-axis sheet to Vr still assumes axisymmetry and zero mean swirl. The saved arrays do not verify those assumptions, dimensional calibration, preprocessing, stitching, statistical independence or uncertainty. Left and right are two conditional reconstructions from the same exposed experiment, not independent trials.

The reported normalization includes the axial through-flow faces as well as radial faces. A percent-scale net defect is an integrated cancellation statement; it is not a claim of that percentage of local velocity accuracy, local divergence accuracy, calibration accuracy or recovered mass conservation. Within-face and between-face cancellation can conceal local departures. No local diagnostic or alternative normalization was computed in this review.

The deterministic coarsening differences are smaller than the reported full normalized imbalances, but this does not bound discretization error or establish a physical cause. Unknown component calibration, experimental effects, nonaxisymmetry, swirl and limitations of the reconstruction remain unresolved. No physical threshold was preregistered, so these values must not be labeled physical pass/fail. The saved arithmetic supports a reproducible conditional consistency description; it does not validate the earlier wake candidate, its empirical gain, the unseen core, global momentum, receiving forces, flight or swarm behavior.

## Execution, provenance and source preservation

The evaluator supervisor records exit code 0, no timeout and no output-cap breach, with elapsed time 0.15222166758030653 seconds and 3,380,517 saved bytes before its receipt. The audit supervisor likewise records exit code 0 with no timeout or output breach, elapsed time 0.18280737474560738 seconds and 3,383,614 saved bytes. The saved twelve-control receipt passes. These are existing execution records; no new controls were run for this review.

The independent audit records `passed:true`, `complete:true` and `scientificStatus:completed-annular-balance`. It checked 3,240 original cases, 74,535 recursively preserved binary64 words, six windows, 1,220 projected nodes, twelve quadratures and 48 oriented faces, using the frozen Decimal60 construction and numerical-only absolute tolerance 2e-12. It records no new fits or model-field evaluations and explicitly declines independent physical validation. Its `admissionFailureHasNoProjectedNodesOrFlux:false` is expected because admission passed; it is not an audit failure.

The source publication binds commit `56048e7731de8896434b35d31419b4b7c42bf88c` to the separately retrieved exact-public manifest. The receipt reports local/committed byte equality and 40 verified pins. This review independently rechecked the current byte identities of all 40 listed files against that saved manifest; all remain unchanged. This is a file-integrity check, not a second numerical audit or a new public retrieval. The additive post-freeze prose clarification is documented separately in `review/POSTFREEZE-CLARIFICATION.md`; the pinned source review was restored before verification/execution, and its current bytes match the freeze.

Relevant saved identities:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| source-manifest.json | 7,970 | `1beeea8e53710c6d8ffd98b0c9376429ba0a51d4c599bbdeb3ef18964686a1d9` |
| source-publication.json | 872 | `e8434969a7ec4b357700cc3aa30decdd5606ea835cad73281d98dc30682cbcaf` |
| results/comparison.json | 3,020,398 | `e7885559d832f4d7dc0136c9d5656a7c4a83c3ac6ab3aeee45e62c2d8562210a` |
| results/selection.json | 358,216 | `a3df84e931da67263b7f2660f62064742e6505b703f0dc5a3dd4c898c60175fc` |
| results/audit.json | 2,663 | `5d962927001525dab21f8cef6edcdde2da7e47823622db35265a8fb15cce0b17` |
| results/execution.json | 224 | `7114cf6f51883d58824af07410bdcc443b037b9f269aee6b71f2d2f7568c68c5` |
| results/evaluate-supervisor.json | 206 | `62d7a90635c1fda4b5c9347f93c52c74425d91b8e78e890cc91a554b2f2b57cc` |
| results/audit-supervisor.json | 203 | `76b198bfc912d3db0136e5b194366cedca94874eca71b80961263221fcc2be39` |

The saved audit also binds both exact predecessor inputs and their published result/source chains. Result publication and UI review are separate activities; this document does not assert either has occurred.

## One next scientific question

**Can independently identified, calibrated three-component measurements at another azimuth reproduce the four boundary terms on these same annular windows?** That would test the axisymmetric/no-swirl interpretation using information the current plane cannot supply, rather than interpreting its small integrated imbalance as verification of those assumptions. The data provenance, common physical support and component calibration would need to be fixed before such a comparison. This review proposes the question only; it performs no search, acquisition, calculation or new diagnostic toward it.
