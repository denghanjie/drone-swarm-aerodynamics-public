# Next question: can the fixed closure face a traceable independent component test?

19 October 2026. Saved-evidence and source review only. I read stored full/coarse surface results, execution/audit receipts, the actual frozen producer and upstream closure source, and existing verified-source reviews. JSON selection copied stored fields without recomputing a metric. No new model evaluation, integration, fit, control, raw-data decode, dataset acquisition, research browsing or rerun was performed. Only this recommendation document was written.

**Recommendation:** stop adding numerical summaries of the same exposed field. The next useful scientific question is whether the fixed, consistently defined axial/crossstream model transfers to an independently acquired, geometrically compatible and calibrated velocity measurement in its admitted downstream domain. Before any comparison, conduct an evidence-admission checkpoint. Exact single-PIV preprocessing provenance could resolve a critical uncertainty in the current evidence, but the existing README and plotting script have already reached their limit; rereading them is not a new calibration result.

## What the completed result establishes

The successful independent audit binds `results/comparison.json` at 3,868,464 bytes, SHA-256 `f7efadfe741c1bd678f1d633ea101a2fe792bb141c8126619ea86f18c961bf7a`. It reports all 1,220 selected model nodes admitted, twelve comparisons and 48 oriented faces checked. The frozen face-transport producer remains SHA-256 `6970471ba89ac91e440f7cb8e7ca1cf2cbe38768887b894811bddd4c29380bcc`; the upstream crossstream producer is SHA-256 `d7bbc3f85c36f933b3b0e5d16034acba2188aedc4a6666dc54274bfe5aa41cd2`. These identities, not a new calculation, ground this note.

On each of the twelve full-grid radial faces, the model's integrated transport has the same sign and smaller magnitude than the saved observed transport. Observed inner-wall terms are negative and outer-wall terms positive under the fixed outward convention. Left and right measured terms differ. They use their own actual coordinates and are not exactly paired surfaces or independent trials, so this observation does not establish physical asymmetry, its statistical significance or its cause.

Every saved full/coarse comparison has positive between-face cancellation. Thus a small net transport discrepancy can coexist with larger individual surface errors. Several faces have J close to the magnitude of their signed error: little sampled within-face cancellation does not imply a small error. Tiny signed cancellation differences at the declared numerical tolerance have no physical interpretation. These are descriptions of already saved boundary errors, not a new explanation of the older whole-field lateral score.

The model's small balance defect is expected of its continuity-derived pair, subject to discrete quadrature error. It does not establish the accuracy of that pair. The new face comparison has answered the preceding NEXT-QUESTION: conservation consistency alone concealed substantial individual boundary mismatch. Another balance, denominator or aggregation of these same surfaces would add little ability to distinguish the competing assumptions.

## Do not infer a lateral correction from radial underprediction

The actual crossstream producer fixes the same inherited gain in Uc and both `axialCore` and `radialCandidate`; it retains the S/2 and c terms and projects radial velocity onto the offset Y=1 plane. The face producer uses those saved components without fitting or reevaluating them. No missing coefficient or source-supported sign reversal has appeared in this chain.

The existing [source reconciliation](../../m31-closure-premises-2026-10-19/SOURCE-RECONCILIATION.md) already shows that radial velocity depends on the axial profile's height derivatives, including the evolution of centerline strength and width. Agreement in axial values at sampled points is not verification of those derivatives. This gives a reason that axial and lateral performance may differ, not evidence selecting a particular failed assumption.

Multiplying only the radial/lateral component while leaving the axial field fixed would generally break the continuity relation that defines this model pair. Scaling both components together preserves that relation but changes the already fixed model and axial calibration; fitting such a scale to these exposed outcomes would be another descriptive fit. Changing spreading rate, origin, width, center or a side-specific gain also changes the tested hypothesis and requires a separately derived, prospective model. None is a calibration correction justified by this result.

Likewise, the declared common Ui for u_piv and v_piv does not verify the actual preprocessing history. A deficient radial prediction is not evidence of a component-specific unit error or a factor-two correction. Mean swirl, nonaxisymmetry, the imposed axial interpretation of a speed-based profile, geometry, source-section stitching and component calibration remain distinguishable possibilities only with further evidence. The current result identifies none as the cause.

## First gate: recover an exact measurement chain only if new provenance exists

The useful question for the current field is narrow: **can the exact released single-source u_piv/v_piv arrays be traced to documented dimensional components and the measurement geometry used in this comparison?** An adequate source would identify the release/version and supply the following chain, with evidence rather than assumptions:

- Component definitions, axes and signs from acquisition through the saved arrays, including any camera-to-physical rotation or component transform.
- Dimensional velocity calibration and timing, plus the exact Ui definition and operating quantities actually used for both components; distinguish total from per-rotor thrust and the data used by unrelated multi-vehicle scripts.
- Coordinate origin, rotor-center layout, sheet position, length scale and any resampling; distinguish the old Cartesian half-spacing from later center-to-motor arm conventions and front-rotor versus diagonal cuts.
- Averaging, section stitching, interpolation, filtering and validity masks sufficient to connect the published fields to these specific arrays, with available measurement and processing uncertainty.

The [normalization source review](../../m31-airflow-scale-transfer-2026-10-19/review/NORMALIZATION-SOURCE.md), [geometry/sign review](../../m31-crossstream-test-2026-10-19/review/GEOMETRY-AND-CONTINUITY.md) and [verified-source ledger](../../m31-closure-premises-2026-10-19/LITERATURE.md) already establish what the README and display script do and do not reveal. They support declared component names, units and orientation; they do not expose the single-field dimensional conversion or full acquisition/preprocessing chain. The later paper's geometry and equations do not prove identity with the old archive.

This should be a bounded documentary admission task, not an open-ended attempt to infer missing metadata from residuals. Only genuinely new, exact provenance can advance it. If it remains unavailable, preserve that explicit unresolved outcome and stop that branch. Do not reconstruct an unknown conversion from the model's preferred answer, run unrelated multi-vehicle scripts as a substitute, or silently alter the frozen data. Even a successful reconstruction would improve interpretation of the current experiment; it would not create independent validation.

## Higher-value numerical destination: an independent compatible vector field

The independent-data branch offers stronger scientific progress if its gates can be satisfied. Use the already retained candidate ledger as a starting inventory, without treating it as an admitted dataset. Before choosing any score or reading target residuals, require:

| Gate | Required evidence and consequence |
|---|---|
| Independence | A separately acquired experiment, outside the coefficient/gain fitting evidence and the exposed RSS archive. Independent acquisition is distinct from a blind selection process. |
| Actual observable | Accessible mean signed axial and documented transverse velocity data, preferably volumetric or multiple planes. A speed-magnitude map, force, thrust or total mass-flux figure does not substitute for the component target. |
| Geometry and domain | Exact motor layout, coordinate conventions, rotor cant/height offsets, sheet or volume location and physical length mapping. All compared support must lie in the model's existing admitted domain; rotor diameter must not be substituted for motor-center scale. |
| Physical scale | Traceable dimensional velocities or an independently documented normalizer, operating point and uncertainty. The inherited empirical gain 0.5450089857597356 is not an SI conversion. Its intended transfer and units must be specified before an external prediction; never copy it between incompatible normalizations or refit it on the target. |
| Data and provenance | Verifiable measurement files, version, license, calibration/masking history, and any reconstruction constraints. A paper or repository record alone is insufficient. A continuity-constrained reconstruction cannot independently validate the continuity law it imposes. |
| Prospective comparison | Freeze the model, physical scaling, component mapping, domain/masks, observations, metrics/null rules, controls, uncertainty treatment and execution budget before numerical work. Preserve failure to admit rather than moving a boundary to obtain a score. |

Prefer comparison of directly measured Cartesian components in their documented geometry. Converting one offset-plane component into radial velocity requires assumptions about swirl and axisymmetry; more complete vector observations could challenge those assumptions rather than repeat them. A compatible planar dataset can still support a clearly conditional component test, but cannot by itself identify three-dimensional swirl or prove axisymmetry. No numerical method can create those missing observables.

The already reviewed candidates currently fail material gates. [Wolf et al.](https://doi.org/10.1007/s00348-024-03880-3) provide valuable volumetric evidence, but the proposed reported flux surfaces were rejected as upstream of this model's admitted domain, with different airframe geometry; FlowFit also imposes continuity. A new score or ratio does not remove those exclusions. Flem's examined experiment has coaxial/tilted geometry and no verified raw release for this use. Jin's examined release is request-only under the existing no-contact constraint. Other leads remain unverified. The [candidate ledger](../../m31-crossstream-test-2026-10-19/review/EXTERNAL-DATA-SEARCH.md) and [domain challenge](../../m31-crossstream-test-2026-10-19/review/EXTERNAL-DIAGNOSTIC-CHALLENGE.md) retain the precise evidence and limitations. No candidate has become admissible because the current model mismatch is clearer.

## Decision and stop rule

The next checkpoint should deliver an evidence-admission decision, not another same-field numerical score. If new exact single-field provenance is available, document its mapping and any independently demonstrated correction while preserving all closed results. If it is absent, retain the ambiguity and prioritize admission of an independent, compatible component dataset. If no such dataset is admitted, state that stronger physical testing is blocked by missing evidence and stop numerical escalation.

Only after admission should a separate protocol authorize the next calculation. That future test may challenge transfer of the fixed closure; it must not claim to isolate a causal mechanism from an observed mismatch without measurements that distinguish the competing explanations. No fit, derivative estimation, center adjustment, lateral multiplier, new dataset download or numerical launch is authorized by this note. Receiving-force accuracy, safe swarm flight, physical validation and novelty remain unestablished.
