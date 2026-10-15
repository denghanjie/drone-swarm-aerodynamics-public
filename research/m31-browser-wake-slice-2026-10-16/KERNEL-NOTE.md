# Prepared-geometry WGSL source note

2026-10-16. Static draft. No shader compilation, browser launch, adapter/device request, pipeline creation, dispatch, readback, geometry evaluation, wake evaluation, source summation or receiver/root evaluation was performed by this task. No source repository file was edited. The sole materialization was sixteen explicit literal control records, encoded by `struct.pack` into u32 words; the script is retained. Binary/JSON word identity, lengths and file hashes were checked without decoding/evaluating scientific inputs.

## Selected source and arithmetic

The port target is `research/m31-source-omission-2026-10-16/source/independent.cjs`, SHA256 `da857f37129c6d3fc87fe223efd2b37b140fbf11417c1f1bb92331d5cfa53cec`. In particular, it uses the field implementation's inlined profile and its factored fade. This deliberately does not mix in production M28's subtractive fade or its separate normalizedWake helper check. The original reference owner must reconstruct saved I from this same independent source before testing Q/G.

The shader receives host-prepared positions, axes and rotor offsets. Its written arithmetic matches the independent field's placement, explicit component dot, residual-vector expression, near predicate, half-width grouping, xi expression, profile denominator, normalized speed, factored fade and final multiplication order. Its `length` differs from host `Math.hypot`; the original binary64 rotation and preparation are outside this GPU component. Source-induced speed, D and sqrt2Minus1 are frozen uploaded constants, not constructed inside the shader. The source constant expression differs in written grouping from the receiver-only vi construction and must remain separately pinned.

No hidden normalizedDown>=minDownstream check is added after `down < minDownstream*D`. A tiny represented discrepancy between those mathematically related tests must not create an unselected rejection path. No root, power, load/wrench, controller or temporal state is calculated.

`policy` is the common staged decision helper used by the normal prepared-geometry path and synthetic scalar controls. Earlier branches take precedence even when controls also supply later zero/cutoff conditions. `finishProfile` and `factoredFade` are common to both paths. Controls12and15 pass through the complete prepared-geometry path; the near-domain control checks an actual invalid geometric arrangement. Controls8–11 are deliberately synthetic stage interfaces; control11 creates a valid zero through the radial fade endpoint without inventing a zero-strength source. Its scalar quantities are not claimed to describe one realizable pose.

## Safety and record semantics

Input exponent/padding validation is integer-only. No NaN/infinity payload is interpreted as a float before its record's complete raw check. Finite component bounds are checked before geometric arithmetic. The host additionally owns exact constant identity, all-source original/packed admission and the original tilt rule; the shader does not claim a global GPU rejection contract.

The declared component limits keep squared position differences finite. Center exclusion precedes rotor geometry; downstream exits precede the radial calculation. Positive D and spread, negative origin, and fixed fade endpoint gaps bound every divisor away from zero. Before profile divisions the source checks D through the constants contract, span>=4, halfWidth>=0.01 and normalizedHalf>=0.25. Before the squared profile denominator it bounds xi and then checks denominator>=1. The numerical profile/sum checks are diagnostics within this bounded contract, not a general exception-catching mechanism for arbitrary WGSL inputs.

Bounds are deliberately conservative: centerNorm<=512, absolute down<=1024, radial<=2048, normalizedDown<=64, halfWidth<=8, absolute axisDot<=4, xi/radialRatio<=128, normalizedSpeed<=3, each fade<=1.001, term<=128 and final sum<=1,000,000. The small fade headroom avoids treating a permitted tiny rounding overshoot as an input-policy change; numerical gates remain the coordinator's responsibility. These are guard bounds, not measured data ranges or accuracy tolerances. No value is clipped into them. The one `max(0,axisDot)` is the stated model projection policy.

Terms are stored as raw u32 words in a separate completed dispatch. Reduction later reads that same retained GPU buffer; the kernel does not regenerate or reupload terms. Thus the accumulator consumes saved f32 values rather than an unmaterialized expression. The ascending-source source code still does not prohibit WGSL reassociation or establish per-addition IEEE round-to-nearest behavior.

Status0/default storage is unwritten. Domain-invalid/malformed/arithmetic-invalid records have no valid numeric term, even when termBits is zero. Early zero and evaluated-profile zero are separate statuses, and I code7 can accompany evaluated zero. All typed identities and reached-field validity masks are retained. A valid profile zero is tested numerically as zero; WGSL does not promise signed-zero preservation. Invalid/unreached placeholders are direct u32 zero assignments and must remain exact zero words.

The reducer additionally checks every ordinal, receiver/source/rotor identity, status, policy-compatible mask, permitted main-record routing, term exponent and nonnegative range. It writes the accepted-prefix count and first offending slot if it rejects. Reduction is attempted only after the driver's independent term qualification; these guards are not a substitute for that qualification.

## Primary language checks and static correction

The prior verified language ledger remains applicable: [W3C WGSL, Candidate Recommendation Draft21September2026](https://www.w3.org/TR/2026/CRD-WGSL-20260921/), §§15.7.2–15.7.6 and17.5.32. f32 arithmetic, fusion/reassociation, subnormals, `length` and division have the specification's permitted behavior. No JavaScript-fround emulator or compensated-summation theorem is claimed to reproduce all conforming implementations. The prior verified WebGPU API ledger governs eventual compilation/error/loss/readback handling.

During static source reading, §16.2 was freshly checked on the same dated specification. An initial uncompiled draft used the reserved identifier `self`; it was renamed to `isSelf` before the final source hash below. `half` was renamed to `halfWidth` for clarity, without asserting it was reserved. §§16.1–16.2 and8.19–8.20 were then read for identifier and operator-group reconciliation. Mixed logical/bitwise groups are explicitly parenthesized where required. These were documentation/text checks only, not a parser or compiler pass. A successful future compile is still unobserved.

## Boundaries

This is an implementation component for four exposed receivers and5,000 source IDs. It does not imply5,000 positive terms, a full receiver set, physical validity, new numerical methodology, speed or coupled local-3D Boids qualification. The source model, aggregation, near-policy omissions and receiver assumptions retain the project's verified literature limitations. No old campaign/review budget is reopened; R8 benchmarkPermission remains false. Independent static review and a completed source/input/protocol freeze are prerequisites for any use.

The final file hashes are recorded in `static-artifacts.json`; they describe this draft, not numerical results.
