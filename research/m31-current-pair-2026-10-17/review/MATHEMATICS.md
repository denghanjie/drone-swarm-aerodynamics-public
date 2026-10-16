# Independent mathematics and target-semantics review

2026-10-17. Package: research/m31-current-pair-2026-10-17.

## Explicit gate decision

**APPROVE the uniquely defined constant-encoding and rounded-preparation target for this prospective checkpoint. APPROVE the inspected conditional pair-coefficient arithmetic for source freeze.** I found no remaining mathematical blocker in the source and final target definitions identified below.

This approval is of a defined model and reviewed construction, not advance empirical qualification. The emitted constants and every prepared operand must still agree with the independent exact oracle in the sole allocated execution. A mismatch must fail qualification. Separate checker-validation and supervision reviews, the exact source-publication gate, and the frozen execution limits remain required. This review does not approve an unseen implementation of the checker validator or a full M-current solver.

The final stress-exception policy resolves the concern raised during this review: only tiny-force with unresolved/normalizer and huge-force with unresolved/unresolved-range may be accounted as declared stress refusals. They remain unqualified cases. The broader status vocabulary is not an acceptance rule; unexpected invalid-input or other unresolved statuses must fail verification, including on those two IDs.

## Scope and activity

This was source-only reasoning. No package module, constant graph, case generator, primitive, reference, checker, control, or scientific model was imported or evaluated. No numerical test, symbolic-algebra program, external source, prior campaign, swarm array, or trajectory was used. No agent was spawned. I authored only this review and communicated source findings; candidate source and earlier drafts were preserved.

Two inherited content files were read, within the limit of twelve. Eleven paths in the new package were accessed, with full/partial/hash-only modes specified in the inventory. Source hashing and filename/definition listings did not evaluate code. The fixed suite's case count and intended coverage remain prospective declarations, not observations made by this review.

## 1. Constants are prospectively unique

The target defines decimal literals, including both tolerances, as binary64 round-to-nearest ties-to-even encodings. PI is a specified bit pattern. Derived constants follow a fixed expression graph. In a simple named form, the induced graph rounds eight-times-rho, rounds its product with A, rounds mg divided by that product, and correctly rounds the resulting square root. Redundant RN wrappers around an already rounded value in the prose do not change that graph.

This uniquely determines each target bit pattern before execution. Materializing the table later does not make the target result-dependent, provided a mismatch is a failure rather than a choice of new constants. The candidate's native Math.sqrt values are proposals. Their presence in adapter.cjs is not itself a proof of correct rounding or a portable all-runtime guarantee.

The inspected independent oracle reconstructs decimal and ordinary-operation rounding with exact rationals. Its rn routine obtains the binary exponent by bit lengths and an exact correction, rounds an integer significand with a remainder comparison and even-tie rule, handles subnormal rounding and the transition to the least normal, and handles overflow through the normal significand carry. Underflow preserves the required zero sign. The constant graph's multiplication/division order matches the declared graph.

The oracle's sqrt_rn searches ordered nonnegative finite binary64 encodings using exact squared dyadics. After finding the largest representable value with square no greater than the input, it compares the input with the exact squared midpoint to the next representable value. Squaring preserves order on these nonnegative values; an equality is a genuine nearest-value tie, resolved by the least significant significand bit. No approximate native root is used as evidence. Binary search is finite over the bounded encoding set.

The constant/preparation gate therefore has a coherent implementation-independent definition and a mathematically appropriate independent checking construction. Qualification must still establish the actual emitted equality. Later uses must retain the verified encodings or requalify their target/runtime; copying unverified native proposals into a browser would not inherit this gate.

## 2. Rounded preparation and exact later geometry are distinct

The candidate reproduces the inherited cross-product/rotation operation graph: each product and difference rounds as binary64, the first cross product is multiplied by two, a second cross product is formed, and the final component uses the specified nested sum with quaternion w. Rotor offsets use the declared corner order; rotor points are rounded center-plus-offset sums.

The independent fp_add, fp_sub, and fp_mul routines model the same rounded graph, including signed-zero behavior and the specified nonfinite conventions. Exact cancellation in round-to-nearest produces positive zero except the negative-zero addition case; multiplication uses the operand sign xor. The constant oracle and preparation graph do not use native norm calculations as admission evidence.

The supplied prepared center, axis, offset, and point encodings then denote exact dyadics. In particular, the receiver point is the already rounded sum. Replacing it during the pair calculation with a new exact center-plus-offset sum would change the target; pair.cjs correctly uses the supplied point.

All seventeen entries of both raw records must be finite, including the unused velocity/angular-velocity components. All eight nominal rotor forces must be strictly positive. These checks precede preparation, and preparation failure precedes self or any geometric zero exit. Both prepared records are computed and retained before geometry validation rejects them. The candidate and inspected oracle follow that order.

The squared norm test is correct: for a positive lower threshold, a nonnegative norm is in [b-t,b+t] exactly when its squared norm is between (b-t)^2 and (b+t)^2. For the declared quaternion/axis tolerances b=1 and t<1; the offset reference radius exceeds its tolerance. The reference explicitly requires the latter relation. The asymmetric squared endpoints are necessary. A symmetric squared-deviation threshold such as 2t+t^2 would not be equivalent on the lower side.

Quaternion, axis, offset norm, and offset-axis dot tests use exact rational values decoded from the actual prepared bits. Near-unit acceptance does not turn the axes or rotation into exact orthonormal objects. These predicates validate the declared model operands, not ideal quaternion-rotation accuracy, coordinate fidelity, actual attitude, or physical geometry. Rounded points at very large coordinate origins remain rounded model inputs; no lost-resolution guarantee is supplied.

Self is explicitly a supplied identity-exclusion flag after validating both supplied records. This is a defined pair-interface input, not a reconstructed proof of source ownership. Future row integration must bind that flag to the actual source/receiver identity. The candidate's raw helpers also assume the declared well-formed generated bit arrays; they are not a general hostile-object or malformed-input API boundary.

## 3. Guard precedence and non-unit-axis geometry

The pair source uses source center minus receiver center for the center tests and source center minus the selected prepared receiver point for the rotor displacement. It never substitutes a source rotor point. Exact rational decoding, arithmetic, and comparisons preserve threshold decisions without a rounded hypot premise.

The inspected sequence is consistent with the target:

1. Global preparation, then self exclusion.
2. Center component/norm guards, then neighbor zero.
3. Rotor component guard, then absolute down guard, then upstream and down-cut zeros.
4. Radial guard, then the near-field conjunction and its admitted outside branch.
5. Positive width, then radial-support zero, then projection zero.
6. The active coefficient, whole-source-domain caps, and positive-normalizer requirement.

The near-field test is the conjunction 0 < down < minDown*D and radial < nearRad. A zero receiver projection cannot bypass it or the earlier radial guard. A far-neighbor zero cannot bypass the center guard. Strict/inclusive endpoint decisions in the source agree with the declared comparisons.

For actual prepared source axis a, the code computes e = d - (d dot a)*a and radial squared as e dot e. This is the intended formula even when the axis is not exactly unit. It does not use the unavailable simplification norm(d)^2 - (d dot a)^2. Squared norm comparisons are valid because their thresholds are positive; width is proved positive before squaring its radial-cut threshold.

The final protocol correctly treats boundary names as descriptive intentions. For example, a decimal identity among raw literals need not remain an exact identity among their independently rounded dyadics. It also acknowledges that component bounds of 257 make a center norm greater than 512 unreachable in the remaining three-dimensional component box. The combined center-guard control is not evidence of isolated coverage of that norm branch. No all-branch coverage claim is justified merely by case labels.

## 4. Exact rational bridge and interval coefficient chain

The rational helper normalizes denominator sign, reduces by a terminating Euclidean gcd, and keeps exact sums, differences, products, quotients, dot products, and comparisons. Its toInterval conversion multiplies a rational numerator by the lattice scale and corrects truncation in the appropriate direction for floor and ceiling. This supplies a valid bridge from exact rational model quantities into the previously reviewed 2^96 lattice. Large rational values do not become rounded native totals.

On the admitted active branch, D, spread, width, the axial base, and the denominator are positive. Thus

    xi^2 = radial^2 / width^2

is an exact algebraic identity for the declared expression. The unfaded profile can be evaluated exactly as a rational using radial squared. Reassociation here belongs to the exact-real model and makes no claim about the historical binary64 expression's rounding.

The remaining square roots and interval products use the unchanged primitive kernel, whose fresh hash equals the previously reviewed and qualified source identity. Ordinary interval inclusion tolerates repeated/dependent operands; it may be loose but does not assume statistical independence.

Fade is constant outside its transition and has derivative -6t(1-t)/(end-start) inside it. It is therefore nonnegative and nonincreasing. The candidate encloses fade at the upper argument endpoint for its lower bound and at the lower argument endpoint for its upper bound. The source's endpoint branch decisions are valid because the actual fade thresholds 2, 2.5, and 3 are exact points on the fixed lattice. This proof does not make fadePoint a general routine for uncertain threshold intervals.

Each active exact coefficient is positive after support and positive projection are established, even if its conservative interval lower endpoint is zero. A zero-containing interval must not be confused with an admitted zero interaction. The source returns the positive active classification only after the exact branch proof; it does not infer that classification from a rounded lower endpoint.

The beta calculation sums the source's four force dyadics exactly and divides by the exact supplied mg before square-root enclosure. Nu uses the exact receiver force divided by exact 2*rho*A. This is deliberately different from the rounded intermediate denominator in the induced-constant graph. The inspected candidate and reference honor the distinction. Complete current weights/candidate source aggregation are not implemented by this pair interface.

## 5. Whole-source caps and unresolved outcomes

For fixed nonnegative K and positive beta, K*beta*y is bounded above by K*beta throughout 0 < y <= 1. Therefore an enclosure upper bound no greater than 128 for both K and scaledK is a sufficient whole-source-domain cap test. A lower bound greater than 128 proves a cap violation at the maximum source amplitude. The source uses those directions correctly.

If a cap interval straddles 128, the code returns unresolved rather than inferring rejection. It also refuses to divide by a nu interval with nonpositive lower endpoint. Range/domain exceptions from lattice arithmetic become named unresolved records; unrelated errors propagate as failed execution. Computing a normalization enclosure before a potentially decidable cap can make a result less decisive, but cannot create an unsound successful certificate.

This review initially questioned the broad unresolved vocabulary as a possible stress-case acceptance loophole. The final explicit map resolves it: only normalizer for tiny-force and unresolved-range for huge-force are permitted stress mechanisms without verification failure. Those cases remain unqualified, and any remaining reference-undecidable result also prevents full qualification. The prospective rule does not permit invalid-bits, invalid-interval, failed sqrt checking, or an unrelated unresolved code to masquerade as a sound stress refusal.

The numerical validator must enforce the distinction between verificationPassed and fullQualification. It must also verify the raw/prepared identities for unresolved records, so a permitted refusal cannot conceal a corrupted input. Implementation of that final validator is the separate checker reviewer's responsibility; only the oracle portion identified below was inspected here.

## 6. Independent reference and limits of its conclusion

The inspected oracle separately computes exact branch decisions and prepared bits. Its fixed-192 square-root enclosure takes an integer square root of the floor of the scaled nonnegative rational, which gives the same integer lower root as the unfloored rational; an exact square comparison determines whether to increment the upper endpoint. The radial fade is bounded from a direct enclosure of sqrt(radial^2/width^2), a mathematically valid construction different from the candidate's radial-root/division sequence. Beta and nu are separately enclosed from their exact rational arguments.

Requiring the entire valid reference interval to be contained in the candidate interval is a sufficient finite comparison criterion. Failure of that inclusion need not prove that the candidate missed the true value: overlapping conservative intervals can fail containment. The final model note handles this correctly as failed evidence rather than permission to tune or tighten the oracle after observation. Reference uncertainty and fixed precision remain explicit.

The source review does not establish observed constant agreement, case resolution counts, bound width, performance, or browser portability. Pair-level correctness does not prove complete nonself row membership, global positive-term count, ordering admission, fixed-point accuracy, force/moment errors, hierarchy efficiency, or a coupled simulation. This checkpoint's narrow scope and continued broader research obligations are stated accurately.

## Actual reading inventory and retained identities

All paths are repository-relative. New-package sources are covered by the package's separate allowance; only the final two rows are inherited content reads. The spec was partially displayed, so this review does not claim an exhaustive per-case inspection. The checker was still being authored: I read only its oracle block, not the later validator/report. The SHA-256 of the exact bytes emitted by sed for lines 150–560 of that inspected checker snapshot is 845c1462651ac76456e83493905b9c8ac44485a6be99fbd87628d205405cc020.

| Path | Access | SHA-256 inspected |
| --- | --- | --- |
| research/m31-current-pair-2026-10-17/PROTOCOL-DRAFT.md | Full immutable draft | ce3c69ab343ffb1a44d73cd3700a4fffbf0ffbaadf3c66c507a8b17c103f0323 |
| research/m31-current-pair-2026-10-17/PROTOCOL.md | Full note, then final appended exception rule | 5c5b736ff8c5a96098e71f0ed12025c773ae2bd5638ec809ba3e4241d46eccb9 |
| research/m31-current-pair-2026-10-17/MODEL.md | Full | 542978ef7f69f76c8b241631d15a823acf974c61e6feee18576a83beffb8403b |
| research/m31-current-pair-2026-10-17/source/spec.json | Partial case display plus constants/layout/corners/explicit controls; full-file hash | 49ca3fef52dd0a12df8696db4c40ba43c155eba91533675ec6261cb4f61d66ab |
| research/m31-current-pair-2026-10-17/source/result-contract.json | Full initial/intermediate/final versions; final map approved | be32e10be8065ade07754b8d3aa1a20f70e77ab19ce6133f0665537241f3f589 |
| research/m31-current-pair-2026-10-17/source/rational.cjs | Full | de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333 |
| research/m31-current-pair-2026-10-17/source/adapter.cjs | Full | 5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145 |
| research/m31-current-pair-2026-10-17/source/pair.cjs | Full | e9fb2f4d7e4d1da09f53c082cf09a3b01c906a9d77642ae333319118b2f568cc |
| research/m31-current-pair-2026-10-17/source/run.cjs | Full | 26f36b36ff66fb7a2c8a8ccdf8cf3850fb7a48213d9265a4795de16157081f28 |
| research/m31-current-pair-2026-10-17/source/interval.cjs | Hash-only identity with previously reviewed primitive | 73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3 |
| research/m31-current-pair-2026-10-17/source/check.py | Oracle block, lines 150–560, during authoring | 8854930b3383f5164aba0fed9c48b6fcdb1374bfb1989410957d1600cd17920d |
| research/m31-browser-screen-2026-10-16/source/anchor-kernel.cjs | Full inherited source, read only | c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a |
| research/m31-browser-screen-2026-10-16/source/reference-excerpt.cjs | Full inherited source, read only | ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e |

Additional inspected prefinal identities of the same paths: PROTOCOL.md 6ab6409b2f9e68a7add693c5151c5904a1107dca1840ce87b217b20cd0db4295; result-contract.json 770d2e0efcbb9bd9f9d6f446544e9b210e414ad33456dafc9aeed5027a5e8d0e and 06236c082b0b754ce8fc68c4455c4a0088c66a0f4c6fa4260fc8fa013612760c. An early definition-name listing of check.py was obtained at eef664afb60d4f39ec27e03d235c2bd243ee7139d4c55b8976291b11edc62df8 before its oracle body was ready; no body approval is inferred from that listing. Later checker additions require the separate full checker review. These recorded source-only revisions were not guided by numerical outputs.
