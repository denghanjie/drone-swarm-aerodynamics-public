# Independent numerical design audit

Date: 2026-10-17. Reviewer: `m31_evidence_audit`. Status: source-level design review only; no numerical execution, model imports, candidate execution, fixture generation, or suite rerun.

## Recommendation and evidentiary limit

Choose one first hypothesis: add a scalar, zero-only binary64 interval filter immediately before the unchanged exact scalar query, after unchanged admission/preparation. Keep the global guard, tree, coefficient construction, fixed96 operations, load solver, and certificate unchanged. A filter may return only one of the existing scalar zero branches after proving that every earlier scalar branch is inapplicable. Any unresolved predicate, rejected-path possibility, nonfinite intermediate, or arithmetic refusal calls the existing exact query on the original exact inputs. An internal filter refusal must never become the scientific status `unresolved`.

This is a precise, independently checkable hypothesis, not a finding that floating arithmetic is the dominant cost or that this filter is faster. The closed evidence localizes a combined assembly stage containing traversal, exact scalar work, collection, and sorting. The previously reported hierarchy counts of 95,339 scalar queries and 5,404 positive terms identify possible zero work; their difference is neither measured filter coverage nor saved runtime. In particular, remaining leaf queries have already survived tree screening and may be disproportionately difficult for an interval filter.

The strongest simpler competitors are eliminating the second identical center-distance dot product inside one exact query, sharing the center guard/neighbor result across the four rotor queries of one ordered drone pair, and avoiding duplicated preparation of identical receiver/source input. Keep these as separate prospective variants so a later comparison can attribute changes. No primitive timing or runtime result was produced in this review.

## Existing semantics that constrain the design

The exact model uses the binary64 words emitted by the adapter, decoded as rational numbers. The adapter's rounded constants, including the outputs of its native square roots, are model operands. They are not ideals to be replaced by more accurate mathematical constants. Prepared rotor points are the actual rounded `center + offset` words. Reconstructing unrounded points would change the model.

The scalar query evaluates exact rational predicates in a fixed order. Its first guards can reject an input even if a later predicate would have returned zero. After the predicate prefix, coefficient computation uses fixed96 directed intervals with explicit domain/range refusals. The distinction among zero, positive, rejected, and unresolved is part of the required result, as is the scalar branch label.

The preparation validator allows near-unit axes; it does not assert exact unit length. The tree and global guard use exact rational boxes. A scalar-only filter does not justify changing those boxes, tree membership, node-rule order, node counters, or global fallback behavior.

Required integration invariant: for each invocation, the fast and exact receiver/source objects must be derived from the same admitted prepared words, with the same rotor index and constant-word set. Separate validity of the objects is insufficient: mismatched valid objects could make a fast zero unsound. Keep the cached fast objects immutable or otherwise owned by the same invocation. Do not reuse prepared input from a previous timed invocation.

The wrapper is an internal trusted primitive, not an admission API for arbitrary independently supplied exact/fast states. The runner must construct both representations from the same successful preparation. A future independent checker should compare saved raw/prepared representations and every fast-zero eligibility claim, with mismatch and post-preparation mutation controls. Finite-operand validation inside interval operations remains required, but does not establish this semantic correspondence. These are prospective checker obligations; no such checker evaluation was performed in this review.

## Primitive enclosure proof obligations

Let `D(t)` and `U(t)` be the adjacent representable values below and above a finite binary64 value `t`. Assume the runtime implements correctly rounded binary64 `+`, `-`, `*`, and `/`, gradual underflow, and the explicit operation graph without reassociation or fused replacements. For one basic operation with exact real result `z` and finite rounded result `t`,

`D(t) <= z <= U(t)`.

The nearest representable rounding cell is contained between the adjacent values, so this bound is conservative even when `t` is exact. It also covers a subnormal result rounded to either signed zero. Both zero signs need `D(0) = -2^-1074` and `U(0) = 2^-1074`. A nonfinite result, NaN, or nonfinite widened endpoint must refuse the filter and use exact fallback. A finite result at an extreme can therefore conservatively refuse when its adjacent value is infinite.

For finite closed intervals, the following rules enclose every exact real operation on enclosed operands:

| Operation | Certified construction |
| --- | --- |
| `A + B` | `[D(A.l + B.l), U(A.u + B.u)]` |
| `A - B` | `[D(A.l - B.u), U(A.u - B.l)]` |
| `A * B` | Minimum and maximum of the four rounded endpoint products, then widen the minimum downward and maximum upward |
| `A / B` | Same four-corner construction, only if `B` excludes zero; otherwise refuse |
| `A²` | If `A` crosses zero, lower bound is exactly zero; otherwise widen the smaller endpoint square downward. Widen the larger endpoint square upward. |
| dot/norm squared | Compose the preceding operations, widening after each basic operation, not once after the final sum |

Multiplication and zero-excluding division attain rectangle extrema at corners. Monotonicity of the adjacent-value operations means widening the extremal rounded corner values encloses every exact corner value. The square rule uses the monotonicity of squaring on each side of zero. A slightly negative lower endpoint from widening a positive underflowed square is loose but sound; it must not be treated as evidence that an actual squared norm is negative.

Induction over the expression graph then encloses the exact rational scalar expressions. Correlation between repeated operands can make an interval loose but does not invalidate containment. This argument applies to the actual residual `d - down * axis`, including its cancellation.

Decode prepared words and adapter constant words directly to binary64 singleton intervals. Decoding two 32-bit hexadecimal halves is exact because each half is an exactly representable integer. Do not use `Number(n) / Number(d)` to recover a rational operand. Composite constants such as `minDown * D`, `nearRad²`, and `neighbor²` need interval arithmetic unless an independent exact-representability proof is provided. A singleton containing only a rounded product need not contain the intended exact product.

The fixed integer guards 257, 258, 1024, 512², and 2048² are exactly representable. Their use as singleton bounds requires no uncertain decimal conversion. Denominator `D` is the adapter's positive prepared constant; generic division must still reject any supplied interval that crosses zero.

The future implementation needs explicit adjacent-value coverage at zero, minimum subnormal, both signs, exponent transitions, and maximum finite values. A source argument is not a runtime validation. No such tests were executed in this cycle.

## Exact scalar branch eligibility

Write `L(x)` and `U(x)` for an enclosure of the exact scalar quantity `x`. Define `dc = source.center - receiver.center`, `c2 = dot(dc,dc)`, `d = source.center - receiver.point[rotor]`, `h = dot(d,source.axis)`, `e = d - h*source.axis`, `r2 = dot(e,e)`, `N = neighbor²`, `H = minDown*D`, `A = nearRad²`, `w = (spread*(h/D-origin))*D`, and `T = (radCut*w)²`. Each composite on the right is enclosed, not rounded to a singleton.

Every row is reached only after the required continuation proof from all earlier rows. Failure to prove a guard pass or either side of a predicate means immediate exact fallback. There is no need to identify which exact rejection will occur inside the filter.

| Scalar step | Zero permitted | Proof required to continue |
| --- | --- | --- |
| Center guard | None | Every `dc` interval inside `[-257,257]`, and `U(c2) <= 512²` |
| Neighbor | `L(c2) >= U(N)` gives `neighbor` | `U(c2) < L(N)` |
| Rotor guard | None | Every `d` interval inside `[-258,258]` |
| Down guard | None | `h` interval inside `[-1024,1024]` |
| Upstream | `U(h) <= 0` gives `upstream` | `L(h) > 0` |
| Down cut | `L(h) >= U(downCut)` gives `down-cut` | `U(h) < L(downCut)` |
| Radial guard | None | `U(r2) <= 2048²` |
| Near region | If `U(h) < L(H)` and `L(r2) >= U(A)`, give `near-outside` | To skip the entire near branch, require `L(h) >= U(H)`; otherwise fall back unless the stated zero is proved |
| Width | None | `L(w) > 0` |
| Radial cut | `L(r2) >= U(T)` gives `radial` | `U(r2) < L(T)` |
| Projection | `U(dot(receiver.axis,source.axis)) <= 0` gives `projection` | Always exact fallback for all remaining cases |

The raw projection test is equivalent to testing `max(rawProjection,0) <= 0`; no approximate clamp is required. The strict/non-strict choices match the scalar source. For example, an enclosure overlapping the neighbor threshold cannot merely be treated as “not proved zero” and passed to the upstream test: exact equality belongs to `neighbor` and would change the branch label.

Soundness follows by induction down this table. At a filter zero, every preceding guard is proved safe, every preceding zero condition is proved false, and the chosen exact zero condition is proved true. In every other case the original exact query supplies the original status, branch, and coefficient/interval data.

For scalar accounting, retain `scalarPairs` as the logical number of pairs offered to the scalar path, including filter hits and exact fallbacks. Additional counters can distinguish filter zero, ambiguity/exception fallback, and exact calls. Redefining `scalarPairs` as exact fallback calls would break the existing `scalarPairs + zeroPairs = 4*N*(N-1)` partition. Preserve the canonical positive order and rejection/unresolved witness selection. Do not shortcut global assembly because one batch finds a refusal.

## Algebraic hazards and counterexamples

These are symbolic arguments, not evaluated probes or claims that each family appears in the saved scenes.

1. **Guard precedence.** A center displacement `(258,0,0)` exceeds both the coordinate guard and the neighbor threshold. The exact branch is `rejected/center-guard`, not `zero/neighbor`. Any zero filter must discharge the earlier guard.
2. **Cancellation.** Exact arithmetic gives `(1 + 2^-53) - 1 = 2^-53`. Binary64 round-to-nearest-even addition rounds the first operation to 1, making the subsequent native difference zero. A relative error allowance proportional only to the computed zero has zero width and misses the exact value. Dot products and the residual subtraction require operation-wise enclosures. Subtraction of nearby already rounded inputs can be exact by Sterbenz's lemma; cancellation risk must not be confused with a claim that every such subtraction rounds incorrectly.
3. **Underflow.** With `t = 2^-1074`, the exact product `t*t` is positive while its binary64 result is zero. A relative-epsilon-only rule misses it. Adjacent-value widening around zero encloses it.
4. **Near-unit is not unit.** The exact identity is `||d-h*a||² = ||d||²-h² + h²*(||a||²-1)`, where `h = d·a`. The last term does not vanish under the validator's tolerance. For the abstract near-unit family `a=(0,0,1+delta)` and `d=(0,0,z)`, the shortcut `||d||²-h²` is negative for positive delta while the true squared residual is nonnegative. This algebra shows why normalization tolerance cannot justify the shortcut; it does not assert that every vector in this illustrative family is generated by the adapter.
5. **Finite operands can overflow.** Subtracting two opposite large finite center coordinates can overflow natively while the exact guard has a definite rejection. Overflow must invoke the exact guard path, not return a zero or a new unresolved outcome.
6. **Threshold equality.** At `h=0`, the exact upstream condition succeeds. Unconditional widening commonly makes its interval straddle zero, forcing fallback. Similar behavior occurs at radial/neighbor boundaries. Conservatism is correct, but saved zero counts are not predicted hit counts.

## Roots, coefficients, and why this boundary is narrow

The first filter contains no square root. Its geometric zero decisions use squared distances. The current fixed96 root implementation computes and checks integer square roots, then constructs exact floor/ceiling endpoints. Replacing it with a native root plus an assumed error margin would require a separate proof and could change coefficient endpoints, cap rejection versus cap uncertainty, normalizer uncertainty, and downstream certificates. The existing range/domain failure branches are observable semantics.

Native `Math.sqrt` also appears in two different roles that must stay distinct: adapter outputs become fixed model operands, while the load solver uses native roots only to propose a candidate that is then certified with exact/directed arithmetic. Neither role supplies a proof that a new native root is correctly bracketed for fixed96 coefficient construction. A future root proposal would need independent exact bracketing and preservation of the existing output/error semantics; merely being close is insufficient.

## Competing reductions

| Candidate | Source basis and possible saving | Semantic/cost constraint |
| --- | --- | --- |
| Reuse `dot(dc,dc)` within one query | The identical exact dot is called for the center norm guard and again for neighbor | Smallest exact change; no numerical benefit quantified |
| Pair-level center result | Center guard and neighbor do not depend on rotor | A receiver-local cache can bound lifetime; avoid unrestricted all-pairs memory and cross-invocation reuse |
| Single-drone preparation | Current method calls `prepare` with the same state as receiver and source; both copies are prepared and validated | Preserve raw admission and preparation refusal behavior; measure complete-call cost including setup |
| Prepared word/geometry reuse | Exact centers/axes/points are already decoded once in `methods`; fast singleton intervals can also be decoded once | Do not claim repeated exact decoding as a current scalar cost; added fast preparation must be charged |
| Source beta / receiver-rotor nu cache | Positive-path normalizers repeat across many interactions | Cache lazily at the original use point, or store tagged results/errors and expose them only at the original point. Eager throwing can turn an otherwise zero query into a refusal or change the first `Unqualified` code |
| Pair projection cache | Axis dot depends on the ordered drone pair, not rotor | Consult it at its existing branch position; cache lookup/allocation can outweigh work skipped |
| Batching/layout changes | May amortize dispatch, allocations, or repeated geometry access | Preserve per-query branch priority, canonical pair ordering, complete assembly, and witness selection; no source evidence isolates dispatch/allocation as dominant |
| Scalar interval zero filter | Can avoid exact rational predicate construction for robustly separated zero cases | Adds work to every fallback and positive query; dependency widening and boundary equality reduce coverage |

No source argument establishes a ranking of runtime gains among these alternatives. The selected filter is a first, falsifiable implementation hypothesis with a narrow exact oracle boundary; simpler exact reuse remains a serious competitor.

## Static review of the new prospective source

The parent supplied new-cycle source during this review. The reviewer read it as text only and did not import, syntax-check, or execute it. Reviewed snapshots:

- `source/binary64-interval.cjs`: SHA-256 `048068853915c0fa5e90272e4dd491cbe4448fcbdbb7157008c90abbd7e185ad`.
- `source/zero-filter.cjs`: SHA-256 `d755b78fb774cab645e254316318bd86d95c2869e8d7682a8ed4a927968f0d88`.

At these snapshots, no enclosure or branch-order defect was identified by inspection. Positive/negative uint32 adjacent-value stepping, special handling of zero, finite widened bounds, four-corner multiplication/division, zero-crossing division refusal, the square rule, and strict complement gates match the proof above. The wrapper's zero wire values match the existing encoded fixed96 zeros. The wrapper routes all other scientific statuses through the supplied exact callback.

This finding is conditional on the admission and same-word correspondence contract, the runtime arithmetic assumptions, and eventual independent tests. The modules are not integrated into the closed method or numerically validated by this review. Exact-zero operations are widened unconditionally, so upright same-plane upstream zeros are a concrete source-level coverage risk. This is not a correctness failure. Broadening the filter to rescue such equalities would require a separately reviewed exact-operation rule.

## Reading and execution record

The inherited content cap was 12 distinct files. This review read 10 distinct inherited files, listed with hashes and scope in `NUMERICAL-DESIGN-READING.json`. Nine small source files were read in full. The `spec.json` read produced truncated tool output; only the exposed constants/header, metadata/footer, and visible scene excerpts were inspected, and no full scene inspection is claimed. New-cycle candidate source is recorded separately and does not consume the inherited cap.

Only source reads, filename discovery, content hashing, and document writes were performed. The closed cost package was not edited. No mathematical experiments, model imports, runtime source evaluation, numerical fixture generation, or old suite rerun occurred. The design has no measured speedup or measured filter hit rate.
