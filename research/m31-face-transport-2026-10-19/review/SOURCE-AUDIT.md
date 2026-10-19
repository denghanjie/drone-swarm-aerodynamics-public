# Independent saved surface-transport source review

19 October 2026. Source-only preparation. The protocol, producer, independent auditor and supervisor were inspected as text. Bundled Python 3.12.14 parsed the three Python files with `ast.parse`; no file was imported or run. No input payload, selected-node domain values, admission counts, control or scientific calculation was inspected/executed in this preparation. Only this document and the new `source/audit.py` were authored by this reviewer.

**Static disposition:** the implementation is consistent with the prospective saved-boundary diagnostic. The separate challenger has inspected the independent auditor's saved-reference arithmetic, admission branch and preservation checks without identifying a static blocker. Numerical execution still requires the immutable public source freeze, exact-public verification, bounded single-use launch and successful receipts. This review does not predict whether the saved model-domain admission will pass or whether its transport comparison will be favorable.

## Source identities

| Source | Bytes | SHA-256 |
|---|---:|---|
| `source/evaluate.py` | 11,421 | `6970471ba89ac91e440f7cb8e7ca1cf2cbe38768887b894811bddd4c29380bcc` |
| `source/audit.py` | 32,966 | `cd21f2b5a8244a319406ecb0594bb7d632336b9084e9b807ce324c93f7356674` |
| `source/supervise.py` | 1,715 | `8796138c2d41de00f3ce91c8680d655e8f451bdae2dbfccdbc71e6ea8eb0ed20` |

These hashes identify the source bytes parsed and reviewed, not executed outcomes. Later source changes require reconciliation and new pins before freeze.

## Immutable evidence and domain admission

The fixed annular input is 3,020,398 bytes with SHA-256 `e7885559d832f4d7dc0136c9d5656a7c4a83c3ac6ab3aeee45e62c2d8562210a`; the crossstream input is 2,291,932 bytes with SHA-256 `1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a`. The independent auditor binds each to its earlier public source/result manifests, execution, successful independent audit and evaluator/auditor supervisor receipts. It does not rerun earlier code.

The entire annular JSON tree is retained as inheritedAnnular. Recursive checks enforce original value types, dictionary key sets, list order and every binary64 word including signed zero. Annular originalCases must exactly equal crossstream cases. The saved gain is checked against the exact fixed value 0.5450089857597356 and copied without refitting or applying it again. The auditor verifies the declared inherited counts and six ordered region IDs, all twelve non-null resolution records, original selected-node identities and copied X/Z/U/v values. It introduces no new window, pairing, interpolation, geometric selection or measured-field reconstruction.

Admission is rebuilt independently for all selected nodes, including interior nodes. A selected model case must have included exactly true, excludedReason null, finite axialCore/radialCandidate/candidate/radius/xi, positive radius and xi within the closed interval [0,2]. The model fields themselves remain unchanged. Missing fields, nonfinite values, predecessor exclusions, out-of-core nodes and numerical radius mismatch are retained as explicit node issues and per-region failure counts. No alternate tapered field, original.a, new wake evaluation or derivative is used.

Before payload inspection, the protocol explicitly fixed a numerical radius-consistency gate of 2e-12 absolute. The two predecessors used mathematically equivalent x*x and X**2 expressions, which can differ in their final floating-point bits. The saved model radius is preserved, its signed difference from the inherited projected R is reported, and the exact inherited annular R becomes integrationRadius for every model integrand. Neither implementation computes a new square root or changes either saved field. This is a declared numerical consistency rule, not a physical radius-error allowance.

The auditor subtracts exact binary64 inputs in Decimal60 for the gate and checks the correctly rounded stored signed difference. A case exactly near the gate could be classified differently from the producer's rounded binary64 subtraction. Such a disagreement fails the audit; neither implementation widens the tolerance, changes the radius or rescues support after seeing a result.

Any failed node causes global admission failure: modelNodes is empty and all six full/coarse/difference records are null. The independent audit follows a branch that performs no model-integrand or transport arithmetic in that case, while checking the failed predicate and complete trace. Broken provenance, malformed input/structure, failed controls and time/output breaches are execution failures, not scientific admission outcomes.

## Independent saved-boundary arithmetic

For an admitted case, the producer and auditor use saved native Z coordinates for the radial walls and saved native R coordinates for top/bottom. They retain all original face-node indices and ordering. Inner/top outward signs are negative; outer/bottom signs are positive. Full/coarse support and endpoints are inherited intact.

The auditor is independently authored for this diagnostic. It multiplies the exact saved integrationRadius by unchanged radialCandidate or axialCore in Decimal60. It integrates the model with nodal trapezoid weights (half adjacent interval widths), whereas the producer sums trapezoid segments. It forms the signed local errors using the saved measured integrand words, then integrates their sampled absolute values using the same nodal weights. It does not read the producer's computed integrands or errors as reference values.

Crucially, Q_obs, D_obs and observedDefect remain the exact **saved** measured face integral, fluxScale and defect. The audit never replaces them with a fresh measured quadrature. Every copied coordinate, index, measured integrand, measured face value, measured scale and measured defect is checked exactly; derived model integrands, local signed errors, model transports, face errors, J and all aggregates/differences are compared under the fixed absolute numerical tolerance 2e-12.

J is the trapezoid of absolute **sampled nodal** errors. It is not the exact integral of the absolute interpolated error across an interval containing a sign change. The source review supports only this discrete weighted-error interpretation. Per-face J−|e|, aggregate within-face and between-face cancellation, and the balance identity receive explicit numerical inequality/identity checks. Small negative cancellation differences within the declared tolerance are retained, not clipped. The use of a rounded saved Q_obs can itself leave a last-bit identity/cancellation residual; the independent audit checks this against the fixed tolerance without recomputing observations to force exact equality.

The face-vector and local-error fractions use saved D_obs and may exceed one. No cap, accuracy-percent conversion, alternate radial denominator, pooled region score or physical acceptance threshold is introduced. D_obs=0 requires null normalized fractions even when local/model errors are nonzero. Full/coarse differences are always coarse minus full for each face's signed error and J and for the two normalized fractions; undefined fractions produce null differences. These are sampling sensitivities, not measurement uncertainty or convergence estimates.

## Controls and execution mechanics

The frozen producer has nine fixed control-receipt labels covering the prospectively declared cases: irregular constant/linear analytic integrals with both outward signs; perfect agreement; within-face cancellation; between-face cancellation with zero measured scale and nonzero error; positive/negative common scaling; closed xi=2 admission versus outside-domain rejection; missing/nonfinite model fields; radius mismatch and inherited exclusion; and global six-region suppression from one failed node. The independent audit validates the exact saved receipt under the frozen producer and successful supervisor, without a second control invocation. No controls were run during preparation.

Producer and auditor have separate permanent exclusive locks, bounded outputs and preserved failure files. The external supervisor observes a fresh child process session for at most 60 seconds and monitors cumulative results/UI/log bytes against 16 MiB for scientific work, reserving 16 KiB for closure. This monitored cap is not an OS memory limit or proof against a transient between-poll output overshoot. The audit verifies the evaluator's exit, deadline, cap receipt and saved byte count, then rechecks source and retained evidence bytes before writing its exclusive report. No simultaneous job or retry is authorized by this review.

## Required source-manifest entries

At minimum, include these six files under the current package:

- `PROTOCOL.md`
- `source/evaluate.py`
- `source/audit.py`
- `source/supervise.py`
- `review/SOURCE-AUDIT.md`
- `review/PROTOCOL-REVIEW.md`

Under **each** of `research/m31-annular-balance-2026-10-19/` and `research/m31-crossstream-test-2026-10-19/`, include all nine files:

- `PROTOCOL.md`
- `source-manifest.json`
- `source-publication.json`
- `result-manifest.json`
- `results/comparison.json`
- `results/execution.json`
- `results/evaluate-supervisor.json`
- `results/audit.json`
- `results/audit-supervisor.json`

Also include `research/publication-receipts/m31-annular-balance-result-2026-10-19.json` and `research/publication-receipts/m31-crossstream-result-2026-10-19.json`. These are 26 mandatory entries; other presentation/review files may increase the count. The current manifest and later source-publication receipt are bound through the exact-public freeze gate rather than listed recursively in themselves.

## Interpretation boundary

This diagnostic compares saved predicted boundary transport with an assumed radial reconstruction of the same exposed experiment. It does not independently verify axisymmetry, zero mean swirl, calibration, stitching or experimental uncertainty. The model's empirical gain and original field values remain fixed. Integrated face errors, sampled local absolute errors and their cancellations are distinct descriptions; none is a causal explanation, decomposition or improvement of the earlier whole-field lateral RMS score. A balanced model can still transport the wrong amounts through individual surfaces, and opposing surface errors can cancel. Conversely, a favorable set of these boundary quantities would not validate unobserved interior flow, momentum, receiving-force response, flight or swarm safety. No discovery or novelty conclusion follows from the known weighted-error identities.
