# Next question: does the fixed model reproduce the boundary transports?

19 October 2026. Source and saved-report review only. The completed evaluator stdout, execution receipt and independent audit were read; no payload was rescored, no control/model/integration was executed, and no frozen source was edited. This is a prospective design recommendation, not an allocation or a numerical result.

The saved audit admits six windows and 1,220 retained nodes. It binds the annular comparison at 3,020,398 bytes, SHA-256 `e7885559d832f4d7dc0136c9d5656a7c4a83c3ac6ab3aeee45e62c2d8562210a`, and reports twelve quadratures checked. The existing measured balance fractions are descriptive outcomes. Their small magnitude does not establish axisymmetry, absence of swirl, calibrated components, or accuracy of the fixed model.

**Recommended question:** on these exact boundaries, does the already fixed model reproduce the measured axial and radial transports, including their distribution along each face? This is distinct from asking whether either field approximately conserves volume. Two fields can each balance while transporting very different amounts through every surface.

## Preserve the four differences; do not reduce them to another balance

For every existing region and full/coarse resolution, retain the same outward signs and report, for each inner, outer, top and bottom face:

    measured signed face Q_obs
    model signed face Q_model
    signed transport error e = Q_model − Q_obs.

There are four separate transport discrepancies per rectangle. Their sum,

    Σ e = defect_model − defect_obs,

is only a linear identity. Reporting that sum alone would largely repeat the balance question and can hide compensating errors between faces. Keep all four measured/model/error terms visible. A useful optional summary within each region is `Σ|e| / D_obs`, where `D_obs` is the already saved sum of absolute measured integrated faces; report null if D_obs=0. This measures mismatch of the face-transport vector, rather than only its net sum. It may exceed one, must not be clipped, and is not a probability or an accuracy percentage. Do not pool the six regions or choose the most favorable resolution.

The common denominator may also be dominated by large axial inflow/outflow. Then even a substantial error relative to the smaller radial transports can look small on that scale. This is why separate raw radial-face comparisons must remain primary; neither the saved gap nor an all-face normalized error is a bound on relative lateral accuracy. Any additional radial-only reference scale would need its own prospective definition and zero handling, not post-result selection.

## Individual integrated faces can still hide local cancellation

Four signed integrals alone cannot establish that the earlier lateral mismatch was, or was not, hidden by cancellation. Positive and negative model errors along one wall may integrate to nearly zero. A more informative companion is a fixed weighted absolute local error on each face:

    J_face = trapezoid_on_the_same_nodes(|f_model − f_obs|),

where f is the oriented face integrand: ±R V_R on a cylindrical wall or ±R U on an axial face. This uses the same actual R/Z quadrature weights, not equal-cell weighting. It requires no new field evaluation if all model and observed values are inherited.

With positive trapezoid weights, `J_face ≥ |e_face|` in exact arithmetic. Their difference describes cancellation of local signed errors within that face; it is not a new conservation law. Preserve both raw quantities and their fixed numerical consistency tolerance. A large J with a small signed face error would support a narrowly stated cancellation finding on that sampled face. A small J would concern those boundary samples only. Neither describes the full interior field or uniquely explains the earlier paired lateral residual.

Use the already saved measured denominator for any displayed normalized version, and show the raw terms beside it. That denominator itself can be small because of within-face cancellation, so such ratios need this limitation. Introducing a different denominator after seeing outcomes would obscure the comparison.

## Use the already saved, internally consistent model pair

The closed crossstream producer explicitly saved `axialCore`, `radialCandidate`, `candidate`, `radius` and `xi` beside each original record; the paired and annular results retained those cases. See [the crossstream producer](../../m31-crossstream-test-2026-10-19/source/evaluate.py), its `radial`, `candidate` and `main` functions. The consistent axial/radial pair is **axialCore plus radialCandidate**, with the inherited fixed gain. Do not substitute `g * original.a`, import another formula, or regenerate a field: that would introduce a different profile/taper interpretation or an unnecessary model evaluation.

Before any new transport arithmetic, a separate protocol must require that every selected model node has the required finite saved fields and lies in the predecessor's admitted unfaded core/domain. Confirm the original identities and preserved source chain. If any node is outside that validity domain, retain a global admission failure; do not remove it, change a boundary, or extend the closure because an outside-domain value happens to have been saved. No such node/domain check has been performed here.

Reuse the annular result's exact region IDs, original-node IDs, face-node order, full/coarse index lists and native R/Z coordinates. Retain the saved measured integrals bit-for-bit. Compute model face transports using those same quadrature weights; compare local model integrands with the saved measured face integrands for J. A later independent audit should verify the saved model identity, the model-to-measured geometry mapping, the linearity relation for signed errors, and the absolute-error inequality independently. The model's own discrete balance is a numerical diagnostic, not evidence of physical correctness; a continuum continuity completion can still have a finite trapezoid defect.

## Interpretation and launch boundary

Keep the question measured-only versus one already fixed model; no fitted lateral multiplier, center, width, background velocity, normalization correction or alternate candidate. Report radial and axial face discrepancies separately. Calibration uncertainty, nonaxisymmetry, mean swirl, stitching and quadrature can all affect them. Left/right results use their own actual coordinates and are not independent trials.

These annular boundaries are a subset with a different weighting from the earlier all-point paired lateral diagnostic. The previous error and opposite-direction share remain unchanged; a new boundary-transport result must not be advertised as improving or decomposing that whole-field score. Conservation consistency imposes fewer constraints than field accuracy, so the two findings can coexist without contradiction.

A new prospective protocol must freeze input/result/source pins, model-domain admission, exact quadrature reuse, the four face errors and J definition, denominator/null rules, fixed analytic controls, numerical tolerances, all endpoints, independent audit and run/output bounds before executing anything. Controls should include compensating errors between faces and within a face, so a zero net defect is not mistaken for accurate transports. Preserve failures and all six outcomes. This note authorizes no calculation and reopens no closed allocation.
