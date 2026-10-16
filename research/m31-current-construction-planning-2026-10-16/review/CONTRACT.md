# Current-position far screen: independent source-contract challenge

Date: 2026-10-16. Repository-relative desk scope: `research/m31-current-construction-planning-2026-10-16`.

## Disposition

**Reject the proposed omission as a formally certified runtime-equivalent optimization under the currently inspected source contract.** The geometric and basic binary64-subtraction argument is sound for the predeclared 4 m component threshold and whole-scene rounded spans at most 256 m. The missing premise is a quantitative guarantee for the value returned by the existing runtime's `Math.hypot`. The existing lean builder uses that returned value both for invalidity and for neighbor exclusion. None of the inspected local contracts supplies a bound or implementation proof sufficient to connect it to the exact norm throughout the proposed domain.

This is a rejection of the present formal justification, not evidence that the proposed screen produces a numerical mismatch on the existing runtime or that it cannot be useful. No implementation, execution, control evaluation, target-array computation, timing, retrieval, or new agent was performed. A pinned finite test would answer a narrower empirical question and requires a separate prospective decision; it cannot be treated as an already authorized consequence of this review.

**The narrower empirical experiment is defensible if separately adopted and frozen.** I find no additional safety or interpretation blocker to a finite controls-plus-fresh-state equivalence and complete-query comparison on a named Node binary, with unchanged L as comparator and complete omitted-symbol, CSR, admission, load, and residual checks. That experiment need not claim a theorem about the primitive. A complete pass would qualify the observed finite input/runtime combinations only; it would not establish portable exactness, runtime-general equivalence, or an operational guarantee for unseen inputs. The missing universal premise is a blocker to the broader certification claim, not to collecting transparently scoped finite comparative evidence.

This was not a clean unexposed design review: one mistakenly selected review artifact exposed saved result arrays. The exact file and read extent are disclosed below. No value from that exposure was used to select constants or claims, and no new counts, ratios, or timing conclusions were calculated. The 4 m and 256 m values were specified in the assignment before that exposure and are unchanged.

## Existing lean path and the obligation created by omission

The authoritative path inspected is `m31-typed-assembly-2026-10-16/source/kernel.cjs`, mode L. It prepares current states, then visits receivers in order and source IDs in strictly ascending order. Its center logic is at lines 101–107:

1. Form the three binary64 world-coordinate differences with the existing subtraction expressions.
2. Compute `center = Math.hypot(dx,dy,dz)`.
3. Before any far-neighbor skip, classify all four rotor entries as symbol 11 if `center` is nonfinite, `center > 512`, or any absolute component exceeds 257.
4. Otherwise leave all four entries at the initialized symbol 1 when `center >= 3`.
5. Only remaining pairs enter the unchanged rotor classifier.

Therefore “far in real geometry” alone is insufficient for exact preservation. A skipped pair must be known to take branch 4, not branch 3 or branch 5, in the original runtime. A naive component test over arbitrary scenes would turn some guard rejections into admitted zero support. The guard-before-neighbor ordering is part of the observable contract, not disposable work.

The rotor classifier must still preserve finite/range guards, downward and radial support tests, unsupported near-field symbol 4, other zero-support distinctions, projection/speed handling, and invalid symbol 11. A zero coefficient is not interchangeable with a rejected or unsupported term. Global input, nominal, geometry, scaled-cap, and final admission diagnostics remain independently significant.

## What the 4 m / 256 m argument does establish

Assume ordinary unmodified numeric inputs and the declared binary64 arithmetic model, with no proxies, getters, concurrent mutation, or monkey-patched math primitives. Run the unchanged preparation before deciding whether the screen is eligible. Use the same finite center coordinates that the prepared buffer supplies to L.

For one axis, let `m` and `M` be the exact selected minimum and maximum among the finite stored binary64 coordinates. Let `RN` denote the binary64 rounding used by the existing subtraction. Check the rounded span

`s = RN(M-m)`

is finite, nonnegative, and at most 256 for every axis. The whole scene must satisfy this certificate before any pair omission occurs.

For any pair, its exact coordinate difference is between `-(M-m)` and `M-m`. Monotonicity of round-to-nearest and sign symmetry of magnitude imply

`|RN(source-receiver)| <= RN(M-m) = s <= 256`.

Signed zero causes no problem for this magnitude claim. An opposite-sign overflow would also make the spanning subtraction fail the certificate. A large common origin does not invalidate this argument: it uses the original subtractions and rounding order, not an assumption that translated coordinates subtract identically. A rounded span at most 256 does not itself prove the exact real span is at most 256; the justified conclusion is about the rounded components actually passed to the reference norm.

Now compute the same `dx`, `dy`, and `dz` as L and consider skipping only when their maximum absolute value is at least the exactly representable constant 4. Let

`H = sqrt(dx^2 + dy^2 + dz^2)`

denote the exact real norm of those already rounded components. Then

`4 <= H <= 256*sqrt(3) < 512`,

and the separate component guard `maxAbs > 257` is false. These are analytical inequalities derived from the fixed constants, not evaluated target statistics. They also show why an ambiguous test at the original 3 m boundary is unnecessary in this proposal. Pairs failing the far test would continue through the original `Math.hypot` and all original branches unchanged.

Do not replace the original differences with differences of translated local coordinates, squared-distance comparisons, reassociated arithmetic, or comparisons involving `position + 4`. Those are different floating-point expressions and would create additional proof obligations, especially at coarse common origins. They are not part of the reviewed proposal.

## The missing runtime premise

L compares the returned runtime value `h = Math.hypot(dx,dy,dz)`, not the mathematical quantity `H`. To omit that call while preserving its branch, the proof needs, for every skipped pair in the admitted domain,

`h is finite and 3 <= h <= 512`.

A specified uniform error bound smaller than the cutoff and guard margins would suffice; correctly rounded `hypot` is stronger than necessary. But the inspected kernel, anchor, schema, protocol, and static review contain neither the primitive's implementation nor such a guaranteed quantitative bound. They preserve calls and expression grouping; they do not prove the numerical range behavior of calls that a new method would omit.

A large geometric margin makes the missing bound plausible for an ordinary implementation; plausibility does not constitute a formal premise. Source-level use of `Math.hypot`, successful unrelated calls during preparation, or historical finite equality tests cannot establish its behavior over all admissible triples. No JavaScript specification or runtime implementation proof was retrieved in this desk scope. This review consequently does not assume an unspecified universal accuracy/monotonicity property for the primitive.

The anchor's existing grid path also uses a whole-scene span certificate and omits pairs. Its existence is antecedent implementation, not an independent proof of this new omission's portable numerical premise. This observation neither reopens the closed grid allocation nor replaces its finite historical evidence with a universal theorem.

Under the current available contract, the only fully justified fallback is to leave screening disabled and execute unchanged L. A new source or runtime arithmetic contract could later discharge the missing premise, but it must be explicit and independently challenged before the screen is called certified.

## Whole-scene admission, fallback, and ordering conditions

If the missing runtime premise is later established, a conservative frozen policy must satisfy all of the following:

- Complete unchanged input preparation and preserve every existing input/geometry/nominal diagnostic. Inspect all current center coordinates; do not substitute a prior scene or cached certificate.
- Establish finite centers and all three finite, nonnegative rounded spans at most 256 before enabling any omission. An even narrower validity gate may be chosen prospectively, but must not be selected from target outcomes or used to relabel an invalid scene admitted.
- If any certificate condition or runtime premise is unavailable, use the unchanged L path for the whole scene. Do not partially screen and then discover that a later source invalidates the certificate; do not repair nonfinite coordinates, truncate candidates, or silently replace rejection with zero.
- Keep the original receiver loop and strictly ascending `j` loop, including the same uniqueness/order check and self-pair handling. A far skip may remove only a proven symbol-1 pair. Retained source IDs remain an ascending subsequence, preserving each positive sparse row and source summation order.
- Keep receiver world-point preparation, retained-pair center computation and guards, rotor order, immediate positive-term consumption, the positive-entry cap's failure point, coefficient scaling, dependency construction, scheduling, solve, and residual code unchanged. Do not batch or reorder retained rotors to offset screening cost.
- Leave all four skipped entries at their original symbol 1. Preserve full symbol counts, all near/invalid distinctions, coefficient bytes and order, graph/admission fields, and downstream loads/residuals as required by the future comparison contract.
- Preserve source ownership and fresh current geometry on every call. The proposal introduces neither cross-call reuse nor a matrix-validity interval.

A new method cannot claim that all old work counters and certificate fields are identical: actual norm-call count is deliberately reduced. The future schema must distinguish intentional instrumentation changes from scientific output equality. In an ordered all-pairs scan, `gatheredNonselfCandidates` may still count every nonself pair, while `directedCenterTests` should count actual center-norm evaluations, and certified skips need an explicit definition. Pair-classification calls and positive terms must not be silently redefined to conceal work. The extra scene scan and component checks belong inside the complete query cost. No operation count by itself establishes elapsed-time improvement.

## Conditions for any separately frozen finite question

This review does not itself allocate or authorize a test. A later decision may adopt either a contract-backed omission with the missing runtime premise established, or the defensible finite pinned-runtime equivalence experiment with no universal certification claim. The latter can proceed as a separately frozen empirical question without first proving a portable `Math.hypot` error bound, provided the limitation is explicit and the unchanged comparator and complete checks are retained. It would remain finite evidence even if all comparisons pass; it does not discharge the formal-source rejection above.

Before any scientific execution, freeze the exact screen and fallback conditions, thresholds, source/checker, runtime/platform/flags, intended output/counter differences, workload-selection rule, resources, publication/remote-verification gates, and failure policy. The disclosed result-file exposure must remain in the design history; the review cannot be reclassified as unexposed.

A prospective comparison would need literal boundary and failure cases spanning the component cutoff, neighbor cutoff, span boundary, nonfinite/overflow/large-origin behavior, signed zero/duplicates, center guard precedence, unsupported near field, rotor invalidity, scaled caps, ordering, and cross-call independence. These are requested coverage categories, not constructed or executed controls. Whole-scene fallback must be compared with unchanged L, and target equivalence must retain full classifications, CSR order/values, admission and downstream outputs before any performance interpretation. Any mismatch or resource failure must remain evidence rather than trigger a threshold change or rerun.

For the empirical route, the checker must specifically compare every omitted pair's retained symbol with L, not infer omission correctness from matching total loads or a checksum. Full coefficient and downstream agreement on that finite population can be established observationally even while a general proof remains unavailable. Scientific/model admission must remain separate from screen eligibility, and complete query timing must include the added certificate work and fallback cost. No finite success would license untested deployment, a physical-control claim, or extrapolation to another runtime. Previously exposed result artifacts limit design-blindness claims; newly frozen fresh states may still supply new finite evidence under their stated selection rule.

The method is ordinary geometric screening and is not established as distinct from every prior variant by this contract review. The separate history reviewer owns that comparison. This review supplies no timing estimate, phase percentage, measured skip count, practical benefit, physical-model validation, or novelty claim.

## Eight-file inventory and exposure record

Exactly eight distinct local content files were opened. Repeated targeted reads of the same files did not reset the limit. Filename discovery did not read target-file contents. No further content file was opened after the eighth.

| No. | Repository-relative file | Read extent and role | SHA-256 |
| ---: | --- | --- | --- |
| 1 | `research/m31-current-construction-planning-2026-10-16/PROSPECTIVE-SCOPE.md` | Entire scope | `9c4a0aaff7633fc06bc1eac81e9ef712678a703390c2c3af16a1a4fcf11d2ad4` |
| 2 | `research/m31-typed-assembly-2026-10-16/source/kernel.cjs` | Entire 209-line lean/typed source | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| 3 | `research/m31-typed-assembly-2026-10-16/PROTOCOL.md` | Entire protocol; reread after a truncated combined display | `52cbc9a307353b70e91f0a594cc70d7769ed53d75c04bac8dcb26a148deb5f3c` |
| 4 | `research/m31-typed-assembly-2026-10-16/review/KERNEL-STATIC.md` | Entire static review; reread after the same truncated display | `e7d9f2652e9e96bb8864c3b9f3f8f0fb7d4c4b00306717650cd09aa6f6c358a4` |
| 5 | `research/m31-typed-assembly-2026-10-16/review/ARITHMETIC.json` | Inadvertent entire-file `cat`: 3,077 lines, 84,786 bytes; combined tool display truncated, with saved result/timing arrays and summary/resource sections visibly exposed | `d211cd35a20c0367fac4aadbbe043b75fd308636078c5400b09235f7202ff4bf` |
| 6 | `research/m31-typed-assembly-2026-10-16/source/anchor-kernel.cjs` | Requested lines 1–230, covering the entire 112-line anchor | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| 7 | `research/m31-typed-assembly-2026-10-16/source/reference-excerpt.cjs` | Requested lines 1–100, covering the entire 38-line excerpt | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| 8 | `research/m31-typed-assembly-2026-10-16/SCHEMA.md` | Entire record/equivalence contract | `a09cff6daaeeebfb867c0bbb0cb13e0ff0b0fd5751f4de2800c79867f9b2c306` |

File 5 was selected under the mistaken belief that its name denoted an arithmetic source contract. The unrestricted read requested its whole content; display truncation is not claimed to erase or narrow that exposure. The parent was informed promptly and instructed that the exposure be preserved, that constants remain unchanged, and that no further use of those values be made. Its arrays are not reproduced here, and no count, ratio, target-dependent threshold, or timing claim was derived from them. Ordinary file hashes and line/byte metadata above are provenance checks, not scientific computation. This error limits the cleanliness of the desk review even though the rejection reasoning depends only on the source branches and the constants fixed before exposure.
