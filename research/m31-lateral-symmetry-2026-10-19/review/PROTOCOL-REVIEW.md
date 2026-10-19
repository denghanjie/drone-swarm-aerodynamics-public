# Static challenge: paired-support lateral residual decomposition

19 October 2026. **The protocol, evaluator, independent audit and display/check source below are accepted for prospective source freeze, conditional on complete immutable publication and exact-public verification before launch. No remaining static blocker was found.** This is source acceptance, not a passed execution or a scientific result.

This review used static text reading, source-file metadata/hashes and review writing only. No pair enumeration, source parser/test/checker, field evaluation, fit, metric, synthetic control, evaluator, audit, raw-data decoding or browser check was run by this reviewer. Previous scientific/display allocations stay closed. The sole input is the already published crossstream result, 2,291,932 bytes, SHA-256 `1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a`.

## Question and interpretation

The diagnostic is appropriate as a descriptive next use of the existing residual. It asks how the candidate's saved errors divide into same-direction and opposite-direction components on a fixed paired support. It does not construct a better predictor, add evidence from another experiment, fit a new parameter or remove a component from the model. Previously exposed response values cannot become a blind test by being transformed.

For a pair, E is half the sum and O half the right-minus-left difference. The residual convention remains model minus measurement. The inverse relation is e_R=e_E+e_O and e_L=e_E-e_O, giving

    e_R^2 + e_L^2 = 2*e_E^2 + 2*e_O^2.

This identity is valid for any two values, including imperfectly mirrored coordinates. It is an algebraic accounting identity, not evidence for physical symmetry, incompressibility or a correct flow law. RMSE contributions combine in squared form; neither RMS values nor MAE components can be added as if they obeyed the same identity.

E and O describe paired sum/difference components, not an exact parity decomposition of a continuous field. The predicted E must be retained when coordinates are not exact opposites. The implementation correctly derives both predicted components from the saved left/right predictions and compares them with the measured components. It does not assign zero to predicted E or attribute the entire observed E to model error.

**Same-direction E is defined separately for every pair and can vary with radius and height.** A large pooled E share would not establish a constant background velocity or justify subtracting one fitted offset. It could be compatible with multiple effects, including swirl, nonaxisymmetry, coordinate-center error, drift, calibration or stitching. This diagnostic cannot identify which effect is present. An O-dominated residual would likewise not uniquely identify a wake coefficient. No component share supplies a physical acceptance threshold or uncertainty estimate.

The original single-PIV normalization and independent-calibration gaps remain. The candidate's axisymmetric/no-swirl local completion, prior core admission and unresolved finite-support/global-vector implications also remain inherited limitations. Re-expressing the saved residual cannot establish receiving-drone force, flight/swarm safety or novelty. The literature and claim ledgers maintain these limits.

## Prospective geometry and coverage

Matching holds the declared axis X=0 and off-axis plane Y=1 fixed. The .01 limit is dimensionless in X=x/l, equivalent to a physical coordinate mismatch of .01l. It is an engineering support rule, not a measurement-uncertainty bound or a fitted displacement. Exact saved Z is used, with no height rounding or tolerance. Only predecessor-included records enter the graph, and opposite X signs are mandatory. X=0 records remain unpaired.

The producer constructs every eligible opposite-sign edge at a level and accepts only mutual degree-one edges. This is not greedy nearest-neighbor assignment: an endpoint with multiple eligible neighbors is ambiguous, and its singleton neighbor cannot override that ambiguity. Sorting positive-X original indices determines pair order and zero-based pairId; neighbor lists are sorted original indices. Each cell can appear only once. Neither v nor candidate/error values enter this matching routine.

The exhaustive reason precedence is consistent with the protocol: prior-excluded, axis, no eligible counterpart, own ambiguity, counterpart ambiguity, then paired. Every original record receives its reason, partner/pairId or null, and full eligible-neighbor list. The copied predecessor case still retains its original inclusion/exclusion fields. A second matching trace is saved to selection.json before support admission, so a geometry failure leaves a reviewable record rather than silently changing the rule.

Coverage uses all predecessor-included cells in each fixed region, including axis and unmatched/ambiguous cells. Numerator is twice the number of admitted pairs, with no cell reuse. The primary requirements of twenty pairs, three distinct heights and at least 90% coverage reject inadequate support without widening tolerance or changing center. The 90% threshold is a design admission rule, not a confidence or accuracy percentage. Secondary empty groups remain valid and null. Near is descriptive; middle/far are fixed subdivisions of the primary Z>=12 region.

The source uses binary64 addition/comparison for matching. The independent audit constructs the graph from exact saved words with Decimal60 and an exact decimal .01 limit. A numerical-boundary classification disagreement is explicitly a failure, not permission to widen the interval or select another matching. No such comparison has been executed during this review.

## Components, metrics and preservation

The producer uses only the saved v_L,v_R,p_L,p_R. It computes observed/predicted E and O, then their signed differences. Direct per-pair SSE is computed from the two original residuals; E/O contributions retain the factor two. Pair records include original indices, coordinates, exact level and admitted coordinate mismatch, so their spatial support stays auditable.

The primary endpoint is pooled E energy divided by pooled E-plus-O energy. It is not the mean of pairwise fractions, which would weight small and large residual pairs differently. A zero total residual keeps perfect agreement valid and returns null shares rather than failing or changing selection. For each fixed region, the source also reports signed-component RMS summaries, pooled energies, paired candidate RMSE, maximum coordinate mismatch, counts and coverage.

Baseline/candidate left, right and joint MAE/RMSE/bias use exactly the same paired support. Side-dependent errors cannot be hidden by moving to different cells for different models. The joint metric and the paired SSE/RMSE describe the same retained population. Unmatched cells remain in the record and coverage denominator; they are not treated as zero residuals. The entire predecessor fullFieldSubsets object is copied unchanged to retain full-field context. A favorable paired-support summary must not replace the earlier complete-selection result.

OriginalCases preserves all predecessor nested records, including their coordinates, measured values, candidate values, residuals, flags and exclusions. The inherited gain is merely copied. There is no wake evaluation, gain call, center shift, lateral offset, interpolation, resampling, threshold sweep or response-selected partition. The declared fixed synthetic controls cover the component identity, zero residual, matching constraints/ambiguity, response invariance, exclusion precedence and empty summaries; they are prospective source controls, not passed checks at this review boundary.

## Independently authored audit and operational bounds

The independent audit imports no producer or physics code. It groups coordinates by exact binary64 Z words, constructs a separate Decimal bipartite graph, checks the complete neighbor/reason table and deterministic pair ordering, and rejects cell reuse. It reconstructs the selection trace and fixed region support independently; its 90% admission uses an exact integer inequality. It verifies both the saved selection.json and the corresponding result fields.

Its component calculation follows a different arithmetic route: form e_L and e_R first, then take their sum/difference, rather than subtracting the separately formed observed/predicted components. With sixty-digit Decimal arithmetic it checks every pair component and energy, all four region summaries, the baseline/candidate side metrics, pooled fractions and null behavior. Saved and independent pair/group SSE identities have a fixed 2e-12 absolute tolerance. That tolerance is for calculation consistency, not experimental error or confidence.

Recursive preservation checks compare originalCases and fullFieldSubsets by JSON structure, types, integer/boolean/null values, list order and exact floating-point words including sign bits. The inherited gain is checked exactly. The predecessor result is bound to its source-publication receipt, execution, successful evaluator/audit supervisors, audit report and result-publication chain. The current source and saved inputs/results/selection/receipts are rechecked after the audit. A passing audit would establish preservation, matching and arithmetic consistency; it would not validate the physical interpretation of a component.

The evaluator's manifest/publication guard precedes its fixed controls and input matching. Its permanent launch lock and the supervisor's per-mode locks make each allocation single-use. The external supervisor enforces sixty seconds and aggregate saved-output limits, observes logs/results/UI output, terminates the process group on breach and checks final elapsed/output values. The audit independently reconstructs the evaluator's saved-byte accounting, excluding the later receipt and its own newly added lock/log files. Do not add unrelated output between these scientific invocations.

The limits remain one evaluator and one independent audit, each <=60 seconds with cumulative scientific output <=16 MiB, then one separate UI check <=60 seconds and total saved evidence <=32 MiB. The real-input bounds of 3,240 records and 1,620 unique pairs follow the fixed input and no-reuse rule; the explicit eligibility-comparison cap is retained. A failure consumes its invocation. This review authorizes no retry, omitted-stage completion, changed matching rule or production adoption.

## Display and checker source

The viewer verifies result byte size/hash and reads saved cases, pair components, matching and summaries. Original points remain at [X*l,l,-Z*l]. It maps E to the same signed error at both pair endpoints and O to negative on the left and positive on the right. Those are mathematical components at the actual recorded positions, not separately measured currents or a new field simulation. The total-error mode retains the predecessor residual; no component is subtracted to create a corrected candidate.

Six modes show total error, E error, O error, measured flow, fixed candidate and coverage. Only paired records receive arrows; all original points remain and unpaired/excluded points are gray. Sparse glyphs use the frozen original row/column%24 drawing rule, the previously reviewed 4m/reference-speed-unit enlargement and capped heads. The error modes share a common color scale; measured/candidate modes share a flow scale. The enlargement is disclosed as a glyph scale, not dimensional velocity calibration or a trajectory.

Text reports paired coverage/mismatch and both paired and unchanged full-field RMSE. It explains that the component shares are squared-error shares, not measured physical causes, and that the model is unchanged. Before freeze, the exact-share tie branch was corrected, the model-minus-measurement sign was made explicit, and the UI assertion was extended to check paired RMSE as well as full-field RMSE. These edits were re-read statically.

The prospective UI check covers six mode states, exact saved sparse-arrow counts including zero cases, primary/band share and coverage/mismatch text, both RMSE contexts, desktop/mobile captures, orbit/reset response, corrupted-evidence refusal before 3D rendering, and console/page/HTTP health. It does not recompute scientific metrics or fit anything. No browser run occurred in this review, and no rendered-legibility or UI pass is claimed. The parent must inspect saved screenshots after the sole UI allocation as required by the protocol.

## Remaining gates and reviewed identities

Before controls or real-data arithmetic, freeze the exact final protocol/evaluator/audit/supervisor, review/derivation notes, viewer/check source and vendor dependencies, plus the inherited input and complete predecessor publication/provenance chain. Publish the immutable source and independently verify the exact-public manifest and local/committed pins. Source receipt assertions inside the programs are not this reviewer's public retrieval. The viewer result pin must be created only from the actual completed result. Keep all earlier checkpoints and this allocation's locks/failures intact.

Paths below are relative to this package. Any source changes require static re-review before launch.

| File | Bytes | SHA-256 |
|---|---:|---|
| `PROTOCOL.md` | 7157 | `f71a7aa0e1876d5fd77c2be120cc0c71470cc11ca99f02e57b7b151460060d2c` |
| `source/evaluate.py` | 9053 | `84651fe343d8b66410d14c84d86ed78a3a99a9b442ecd7a1f695774368f8fd8f` |
| `source/audit.py` | 27738 | `19c207081b488e5085cb95903f37eae2509d6494948d31b05159d753c205d885` |
| `source/supervise.py` | 1715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |
| `source/ui.cjs` | 6070 | `90095f1dc099fd8a55ef2ef7e7d591cdd7588c95443ad86af1ee00e47808f4f3` |
| `viewer/app.js` | 7368 | `730c76e9861881f2fd04a7d67f9169ab8f05321a4f3d11374beea0f2f72f4116` |
| `viewer/index.html` | 5176 | `bb9d49ce9ad38f056067999e28bc830ac73e189f1db8e944a49d6082577b035c` |
| `review/PAIR-DECOMPOSITION.md` | 6072 | `c0b1e8f2816e13ce8c462827629e841b9c2237ca704aead5f5ddd3336fbf8371` |

No new pairing count, component share or other numerical result is known at this review boundary. The overall research objective remains incomplete regardless of the eventual descriptive decomposition.
