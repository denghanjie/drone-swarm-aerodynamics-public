# Prospective annular continuity diagnostic

19 October2026. User “move on” authorizes this new bounded cycle. Previous allocations remain closed. Question: under an explicit axisymmetric, no-mean-swirl interpretation of the offset PIV plane, what finite annular flux imbalance is obtained from the saved measured axial/lateral velocities? No model coefficient, prediction or calibration is changed. The six fixed regions are all endpoints; no region is selected by its answer.

## Evidence and limitations

Primary input: research/m31-lateral-symmetry-2026-10-19/results/comparison.json,3,793,293bytes,SHA256b253b7199df24e8a2d5ff3000bed1f73937cd898ada8449256c91f0172962be3. Second fixed provenance input: research/m31-airflow-test-2026-10-19/results/comparison.json,1,112,834bytes,SHA256dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3. Require upstream counts.nonfiniteCoordinates==0 and counts.missingU==0; do not inspect these counts before freeze. Exactly preserve its saved cases as the primary input nested original rows. These are the inherited stride-four retained samples, not the complete raw PIV grid. A tensor check cannot reveal an entirely absent upstream level, so this conservative metadata gate is mandatory.

Use the primary input originalCases and nested original X,Z,u,v,index,row,column. All records and response values were previously exposed. No original MAT decode, field evaluation, old evaluator/auditor, new raw measurement, gain, shift, smoothing or fit. Preserve all originalCases and predecessor fullFieldSubsets unchanged. Do not filter by the predecessor model's core-inclusion flag.

Declared X=x/l,Y=1,Z=z/l,l=.0325m and both velocity components nominally divided by Ui. Cylindrical radius R=sqrt(X²+1); measured lateral v is mapped to radial V=R*v/X. This mapping assumes axisymmetry and zero mean swirl and is used only for |X|>=1. It is not measured radial velocity or a measured three-dimensional volume. Left and right side reconstructions remain separate; do not average them. Actual calibration, stitching, nonaxisymmetry and swirl are unresolved. Any imbalance is conditional, not proof that incompressibility fails. No physical pass threshold, p-value, confidence interval or experimental-error bound.

## Fixed geometry and admission

Six windows: left(X<0) and right(X>0) independently, with1<=|X|<=3, and Z bands[12,16),[16,20),[20,24]. All bounds are dimensionless, selected before new payload inspection. Each admitted window uses actual minimum/maximum selected R and Z as its boundary; no interpolation to the nominal bounds. Report actual bounds and counts. Different left/right extents must not be relabeled identical support.

Use all saved original records in each window. Require finite X,Z throughout input; unique original indices; exactly one record for each exact binary64 (X,Z) coordinate in every window; at least5distinct X and5distinct Z values; and a complete tensor-product lattice with the same X levels at every Z. Exact means saved binary64 equality, without tolerance or rounded bucketing. Reject duplicate/missing nodes, nonfinite u/v at any selected node, or insufficient support. All six windows must pass before any real flux calculation. Bound malformed-grid evidence: save expected/observed unique coordinate counts, exact missing-coordinate count and only the first missing coordinate in ascending Z then |X| order. Build nodeIndices only when the grid is a unique complete tensor product. No full missing-product expansion. Save geometry selection/reason records before admission; any admission failure consumes the sole invocation. A valid admission-failed artifact is procedural completion with status admission-failed, all six full/coarse/difference records null and no projectedNodes or measured-flux arithmetic. An independent audit verifies the failed predicate and trace. Malformed input, broken provenance, failed controls, or time/output breaches are execution failures, never relabeled admission failures. Do not widen windows, infer missing values or continue only favorable regions.

Sort selected nodes by increasing R within increasing Z; R order is increasing |X|, so left-side order is intentionally different from signed X order. Preserve original indices and coordinates. Every original case receives its region ID or outside-windows reason, independent of prior inclusion. Count all selected interior nodes even though boundary quadrature uses only face nodes. Whole-input coverage is descriptive, not an accuracy requirement. Max3,240input records,6regions,3,240selected records and12quadrature records (six full and six coarse).

## Balance and normalization

For each actual rectangle R in[a,b],Z in[z0,z1], report four oriented fluxes using the composite trapezoid rule on actual nonuniform coordinates:

    inner = -a * integral_z0^z1 V(a,Z)dZ
    outer = +b * integral_z0^z1 V(b,Z)dZ
    top = - integral_a^b R*U(R,z0)dR
    bottom = + integral_a^b R*U(R,z1)dR
    defect = inner+outer+top+bottom
    scale = |inner|+|outer|+|top|+|bottom|
    signedFraction = defect/scale, absoluteFraction = |defect|/scale.

If scale is zero, fractions are null and the four zero integrated face terms are retained. Within-face cancellation can produce this condition even when some nodal velocities are nonzero; do not label it zero airflow. These dimensionless component values correspond to Ui*l² after omitting the common2pi angular factor. They are not mass flow in SI units or physical energy. The normalization is invariant to one shared nonzero velocity multiplier (absoluteFraction invariant; signedFraction changes sign for negative multiplier); it is not invariant to different u/v scalings or spatially varying calibration.

For the fixed coarse check take sorted full-grid indices0,2,4,... on each axis and append the final index if not already retained. Use exactly the same boundary endpoints. Recompute the four face integrals and fractions using those nodes. Report coarse-minus-full defect difference and signed-fraction difference (null if either undefined), plus every selected face-node index. This is one deterministic sensitivity check, not a convergence study or measurement uncertainty estimate. Do not choose fine/coarse based on which balances better.

No combined six-region pass rate or pooled score; report all signed face terms, normalized defects, actual geometry and discretization changes. The conservation identity derives from the divergence equation; it does not imply a closed measured disk because the absent core is canceled analytically. Strong agreement would be conditional consistency only; disagreement would not uniquely identify its cause.

## Fixed controls and independent audit

One evaluator<=60s,<=16MiB cumulative scientific output, permanent lock. Before real-data admission run fixed synthetic controls: irregular-grid divergence-free field U=2Z+3,V=-R (measured v=-X) on both sides, checking each analytic oriented face and total; known source field U=2Z+3,V=0 with analytic nonzero volume integral; allzero field/null fractions; common positive/negative rescaling of a field with nonzero radial and axial face terms (verify each scaled face as well as fractions) and constant-axial-flow cancellation; reflected-side coordinate/projection consistency; fixed coarse endpoint retention; and missing/duplicate lattice, nonfinite component and insufficient-axis rejection. Controls are numerical implementation checks, not physical evidence. Fixed numerical tolerance2e-12absolute for synthetic balance/expected values.

One independent saved-result audit<=60s,<=16MiB cumulative output. No producer import, wake evaluation or old scientific rerun. Independently rebuild geometry/selection from original input, preserve recursive original binary64 values, reconstruct all nodes/projected radial values and full/coarse face integrals using60-digit Decimal. Check every reported scalar/node/index/count and numerical differences with2e-12absolute tolerance, source/input/result/provenance pins and external supervisor receipts. This tolerance is numerical only. No rerun, repair or completion of omitted stages.

Both invocations require independent static protocol/source review, exact immutable public source freeze, separate exact-public manifest retrieval and verified local/committed pins before any controls or real arithmetic. External supervisor records time/output/exit; permanent single-use locks and failure records; no overlapping jobs.

## Saved Three.js display and publication

One separately bounded UI invocation<=60s,<=32MiB cumulative evidence after terminal evaluator and independent-audit success, including an explicitly audited admission-failed outcome. In the latter case show the selection/failure trace and saved original points with no invented flux values. Show only saved selected points, actual region faces/annular geometry and saved balance terms, with left/right kept separate. Mark axisymmetric cylindrical mapping and absent core as assumptions. No animation presented as flight or measured volumetric flow. Raw face terms and all six regions available. Desktop/mobile, region selection, full/coarse display, orbit/reset, corrupt-evidence refusal and source/result identity checks. Parent inspects screenshots. Any UI repair needs a separate prospective allocation preserving failure.

Save exact inputs/results hashes, all raw face/node evidence, failures, independent reviews, source/claim/literature ledgers, understandable summary and restart. Privacy-check,commit,push and verify public checkpoints. Keep8876. No installations, paid resources, contact or submission. Overall research remains incomplete; no physical-calibration, force/swarm safety or novelty claim.
