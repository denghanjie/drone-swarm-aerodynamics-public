# Static physical-test protocol review

Reviewer: `/root/m31_protocol_challenge`. Corrected-geometry snapshot: 2026-10-19T03:04:00Z.

**Accept the corrected projected-arm source for the single registered descriptive empirical comparison, subject to the pending source/privacy freeze, publication and exact-public verification gates. No remaining source or physics blocker was found in this scope.** This acceptance applies only to `Kiran-stacked-projected-arm-fixedPWM-v1` and the hashes below. It is not an executed result, a calibrated physical rejection, or permission for replacement runs. The earlier radial-l interpretation and its acceptance are withdrawn; the unexecuted draft is preserved in `design-history/radial-l-unexecuted`. See `review/GEOMETRY-CORRECTION.md` for the primary figure/text evidence.

I read the amended `PROTOCOL.md` and `source/evaluate.py`, and retained my earlier static inspection of unchanged `SCHEMA.json`, the `mat5.py` dependency, `source/supervise.py`, the original static README and schema review. I also checked the relevant historical `anchor-kernel.cjs` and `reference-excerpt.cjs` formulas as text, and visually inspected the official paper's apparatus pages 3–4. Inspection used source text/images, coordinate metadata and file hashes only. No evaluator, parser, scientific function, synthetic control, audit or test was executed; no experimental force or moment values were decoded. This corrected review and `GEOMETRY-CORRECTION.md` are the only files I wrote in this geometry-correction task.

## Physical hypothesis and algebra

The named `Kiran-stacked-projected-arm-fixedPWM-v1` variant is a legitimate, narrowly stated operational hypothesis: apply the existing directed, memoryless law to the documented static fixed-voltage/PWM experiment using the figure-supported motor geometry. Fig. 3 dimensions the horizontal center-to-motor-column distance; Fig. 4 depicts a square/X layout; the text identifies opposing-column alignment at horizontal displacement 2l. Together these support coordinate components ±l, radial center-to-motor distance R = sqrt(2)l, and D = 2R. The primary upper contrast requires no numerical isolated baseline. The secondary lower-force prediction explicitly assumes nominal total force F0 = W, rather than pretending that W is an independently measured isolated transducer force. Fixed PWM is not fixed ideal power; disagreement challenges this combined operational approximation and cannot identify the receiver cubic alone as the cause.

The stacked scalar specialization matches the historical formula under its declared assumptions. Let P be the dimensionless profile including projection/fades, A the common rotor disk area, rho the common air density, and mg the historical reference force. The historical source coefficient and scaling give

`K = P sqrt(mg/(8 rho A))`, `beta_upper = sqrt(q_upper W/mg)`.

For four equal receiver nominal forces, the receiver normalizer is

`sqrt((q_lower W/4)/(2 rho A)) = sqrt(q_lower W/(8 rho A))`.

Their ratio is `P sqrt(q_upper/q_lower)`. The upper vehicle has no incoming positive source edge in the nominal upright pair, hence its source multiplier is one. Therefore the evaluator's alpha, upper force `q_upper W`, and lower force `q_lower W root(alpha)` are consistent. No missing factor of four remains. Rotor-disk area, density and historical force normalization cancel under common-hardware/equal-rotor assumptions. An undocumented propeller diameter is consequently unnecessary for this specialization. The radial motor-center distance R does not cancel: it remains essential in both the profile's radial argument and D. This does not establish cancellation for arbitrary rotor loads, different hardware, tilt or multi-vehicle geometry.

The scalar cubic has a unique root in (0,1] for nonnegative alpha; fixed bisection on [0,1] is appropriate. The amended source changes both radial distance to R = sqrt(2)l and D to 2R consistently. The radial profile, sign of origin -5.817, downstream fade and radial fade agree with the historical expressions. Experimental coordinates continue to use `z = z_l × 0.0325 m`; the source correctly does not rescale them by R. The test is an algebraic specialization, not execution or certification of every numerical guard in the full native query.

## Case selection and indexing

The coordinate-only schema is 14 by 12 in MATLAB column-major order. The first 14 elements form the stacked column x/l = 0. Selecting indices 3 through 13 therefore selects the declared 11 stacked cases; it is not a transpose or an offset slice. The revised rows are fixed from source geometry before experimental force decoding. The exact offset 2l is absent and is not interpolated.

The corrected model uses R = sqrt(2)l and D = 2R, so the near-height cutoff is 5sqrt(2)l. Rows 0–2 at 0.13, 0.17 and 0.21 m are outside this domain. The nearest selected nominal separation is 0.25 m. Across the registered sensitivity points, the smallest separation is 0.249 m and the largest near cutoff is 5sqrt(2) × 0.03255 m, below 0.231 m. Thus the entire finite evaluated set has a clear near-height margin. These are elementary bounds on declared inputs, not executed predictions or experimental pose-uncertainty claims. The revised selected-row test z/l >= 7 identifies exactly rows 3–13 in the pinned grid; it does not replace the predictor's actual near-domain check.

All registered positions are below the downstream cutoff and inside neighbor support. Upright stacked reverse edges are upstream zero. Square-layout yaw does not alter the radius R of a receiver rotor relative to the centered source axis in this axisymmetric scalar model. Actual pose uncertainty and actual near-field rotor structure remain physical limitations, not resolved measurements.

The evaluator checks each original member's hash and byte length against the frozen schema, verifies names/shapes for the used matrices, checks the stacked column, and checks the increasing z values and selected-row rule. Hash binding provides the exact coordinate-file identity beyond those shape assertions. The schema itself must be included in the source freeze.

## Primary and secondary interpretation

The primary quantity is upper mean force at row 3 minus upper mean force at row 13, both divided by W; the model contrast is exactly zero for the declared fixed input/orientation. This avoids calling the far case an isolated calibration. A nonzero recorded contrast is a descriptive discrepancy. It is not automatically a statistically resolved effect or a calibrated falsification, because calibration, differential tare/drift, full pose information and the statistic behind the SD fields remain unresolved.

`abs(difference)` is the deterministic differential correction needed to make the two reported means equal. Half that value is sufficient when corrections of opposite sign are assigned equally to the two cases. These are sensitivity thresholds, not measured bias or an uncertainty estimate; random error, rounding or differential systematic error could contribute. Reporting should preserve that distinction despite the source field's `BiasToReconcile` name.

The secondary signed residual is measured lower F/W minus conditional predicted lower F/W. The 11-case MAE and maximum absolute residual describe this fixed selected slice; they are not general physical error rates or an accuracy acceptance criterion. Conversion with approximately 0.265 N yields approximate newtons. A positive result cannot validate the many-drone, dynamic or control system.

The 81-point-per-case Cartesian product is exactly the four registered three-level choices, producing 891 outcomes plus 11 nominal predictions. Source retains every point and reports sampled minima/maxima. It performs no fit or best-parameter selection. The discarded radial mapping is not an evaluated alternative. The finite range is explicitly illustrative, not a confidence interval, experimental uncertainty budget, continuous enclosure or guaranteed input coverage. The known papers and coordinate schema make this a prospectively specified no-fit challenge, not a blind holdout.

The original SD values are retained separately. README “over three trials” and article unsteadiness descriptions do not uniquely identify their aggregation. No sqrt(n), p-value, confidence level or calibrated rejection is computed. This is the correct limited treatment of the available aggregate data.

## Source and operational review

The restricted MAT reader accepts only bounded little-endian MAT v5 real dense double matrices, requires one variable, checks dimensions and payload lengths, and rejects nonfinite decoded values. Compressed input uses a bounded decompressor with end/trailing checks. The registered synthetic controls exercise plain/compressed data, a small name tag, column-major contents, truncation and nonfinite rejection. Static inspection is not a claim that these controls have passed.

The final revision removes the outcome-dependent nonnegative-force gate: finite negative force means are retained for comparison, while SDs must be nonnegative. It also adds maximum absolute error in approximate newtons. Absolute-path loading of `mat5.py` is compatible with the supervisor's isolated Python invocation. The `-I -B` child invocation ignores ambient Python configuration, suppresses bytecode writes and does not disable assertions.

The protocol counts fixed controls separately: two admitted prediction calls at 0.25 m and 1.10 m, one refused near call at 0.21 m, five explicit root calls and the two roots inside the admitted controls. These control inputs have been updated consistently with the corrected geometry. The upper-null control checks the implemented scalar invariance; it is not an independent physical measurement or a substitute for the algebraic derivation above.

The external supervisor gives each preallocated evaluation/audit command its own 60-second timeout and an exclusive supervisor lock; the evaluator has an exclusive launch lock. The child evaluator contains no process-spawning path, so the supervisor's direct-child timeout is sufficient for the inspected evaluator. Any later audit implementation needs its own review. Result size is checked before saving, and serialization rejects NaN/infinity. Inputs, row count, sensitivity size and stdout are bounded by the registered fixed workload. This is not a hard filesystem quota or OS-memory guarantee.

Failure paths retain a failure record when the evaluator catches an error; an externally killed or abruptly terminated child instead relies on the supervisor receipt and retained partial files. A failed attempt remains consumed. The analysis source does not enforce publication by itself: the parent must finish the registered exact-public source verification before invoking it. This review does not claim that gate has already occurred.

The independent saved-result auditor and saved-only UI are separate registered work. Neither was executed or certified by this review. The supervisor's subsequently added `ui` command branch leaves its evaluator/auditor command unchanged; UI browser-descendant cleanup and UI behavior remain outside this review. Their output must not elevate a descriptive comparison into a confidence statement or a broad physical-validation claim.

## Exact reviewed snapshot

Paths below are relative to `research/m31-physical-test-2026-10-19`. Subsequent changes require a review update before this disposition is relied upon.

| Path | Bytes | SHA256 |
|---|---:|---|
| `PROTOCOL.md` | 7419 | `f7bf506252fc737631199e76af0b316fed4010ab5fec8a7c59e06ed1d6c1ef79` |
| `SCHEMA.json` | 10250 | `2b1e87af178d2a23becba9d5e852ca69d9f98af8c991b2b3ad4e1802a09806c2` |
| `source/evaluate.py` | 6251 | `d807dda83b7c20e74f68a4dca767a05b6ed57589d9965f715051cb1a5b0c1ea4` |
| `source/mat5.py` | 2445 | `c70e1c511a89bfe8adf1302dd5590f42042c412e6c46ef7beb6d191d13ed1032` |
| `source/supervise.py` | 1200 | `2c25c016c2fcbf549ef55e9b75532b211f4038f10295b352ccaa56696dbc681a` |
| `data/README_static.txt` | 4960 | `2695a000f2beac1c2f84d645bf6c0b24ca879f5b7ecb8d9873e2b6cfd8e4de6b` |
| `review/GEOMETRY-CORRECTION.md` | 5590 | `9ccdea340f61460c7d6c2ca5fa58494b6b82530496c00491c5fcc213c4728b8b` |

No further repair is requested for the pinned evaluator/protocol. Proceed through the pending freeze/publication gates to the one bounded comparison, and retain either outcome with the stated physical and uncertainty limits.
