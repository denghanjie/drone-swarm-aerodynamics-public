# Native tree: prospective fixed control and saved-evidence protocol

This is source preparation, not a qualification result. The first proposed run contains 42 fixed cases, each queried once in the fixed order F, H0, H: 126 native queries. The largest input is the already exposed 64-drone `fresh-a-t5` input from the earlier native transfer experiment. There is no new trajectory, new random sample, 5000-drone case, repeated timing campaign, parameter search, or new exact-reference calculation. A pass would establish only the registered saved-record checks on the pinned runtime. It would not establish independent exact accuracy of F, universal floating-point equivalence, real-time performance, physical validity, or novelty.

`source/cases.json` supplies literal binary64 state words and fixed recipes. The unchanged comparator is `../m31-native-fresh-transfer-2026-10-17/source/native-load.cjs`; H/H0 are the new native fork. The checker hardcodes the old comparator and four numerical dependency hashes, the exposed input pin, all 18 ±4 boundary words, and the nine radius-boundary placements. Source configuration and every dependency must also belong to the reviewed manifest. This protocol does not authorize execution; the supervisor's disabled configuration must be separately reviewed, published and authorized.

## Registered inputs and expected outcomes

| Group | Cases | Required behavior, in each arm |
| --- | ---: | --- |
| All-axis ±4 faces | 18 | Each axis, both signs, equality and adjacent words toward/away from zero. Receiver at zero plus eight sources at the specified face. Equality/outside permit H group omission; inside permits none. All succeed. |
| Strict center radius 3 | 9 | Each axis at predecessor, equality, successor. Two directed center tests; exactly two center-eligible pairs strictly inside, zero at equality/outside. Both directed signs occur in each pair. All succeed. |
| Coincident centers, distinct IDs | 1 | Nine distinct IDs at one center; no source may disappear or be deduplicated by position. All candidates retained; success. |
| Positive/canonical and permuted | 2 | Four identical physical drones with two input-array orders. Canonical IDs, nonempty positive CSR, ascending sources, roots and loads coincide. At least one CSR row contains two sources for the order-corruption control. |
| Translated sparse geometry | 1 | Exact finite translation and separation; success with independently reconstructed culls. |
| Rounded span 256 | 2 | Equality remains eligible; its next word falls back to unchanged all-pairs lean evaluation. Both succeed. |
| Invalid far geometry/input | 3 | Finite separation 513 plus malformed quaternion falls back and refuses with geometry and eight invalid rotor terms; a nonfinite raw position refuses before build; a zero nominal rotor force refuses before build. |
| Near field, scaled cap, graph order | 3 | Fixed expected domain refusals and specific reasons/diagnostics. Scaled-cap control uses a large finite source force; graph control preserves words from the earlier exposed order-incompatible control. |
| Duplicate/missing ID | 2 | `duplicate-id` and `record-fields`, respectively, before build. No canonical raw array or tree is claimed. |
| Exposed 64 regression | 1 | Byte-pinned old `fresh-a-t5` input, expected success. An exposed regression, never a fresh 64 sample. |
| **Total** | **42** | **Preregistered 34 successes and eight refusals per arm. An unexpected refusal or unexpected success fails; no case substitution.** |

The fixed base state has identity quaternion, zero velocities/rates and four nominal forces of 0.0625. Inline overrides, input ordering and stable IDs are explicit. Boundary expansion is fixed: receiver ID 0 and source IDs 10 through 17; other coordinates are positive zero. The exposed input is 21,955 bytes with SHA-256 `48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c`. State words, including the deliberate quiet-NaN word in one raw refusal control, are decoded without JSON numeric conversion. The harness saves each fully expanded word input and verifies it was not mutated by any arm.

## Independent checker and complete coverage

`source/check.py` imports only Python's standard library. It never imports or executes a producer, numerical kernel, oracle, trajectory generator, or saved scientific helper. Its binary64 decoder, exact integer/Fraction round-to-nearest ties-to-even routine and subtraction checker operate on saved words. Exact cancellation yields positive zero except the IEEE `-0 - +0` case; underflow retains sign. Node comparisons use the resulting rounded words, not exact-unrounded distance comparisons or the host Python float subtraction.

The checker independently reconstructs the widest-rounded-axis, lowest-axis-tie, stable-ID median tree, leaf capacity 8, preorder IDs, every bound and every leaf member. It verifies the actual saved tree equals that reconstruction. For every receiver it reconstructs the complete left/right traversal; evaluates positive then negative endpoint tests in axis order; and checks saved cull node, axis, side and rounded difference. H0 evaluates the same first-satisfied predicate but always descends. Both modes' exact comparison, node, leaf, gathering and completion counts are recomputed.

For every omitted node the checker also checks every member individually against F's existing `max(abs(RN(source-center))) >= 4` exit. Culled node memberships and visited leaf memberships must form a disjoint complete partition of all canonical indices. A cull cannot include self. The actual gathered list must equal the sorted retained leaf members, including self exactly once; the original classifier then excludes self. Missing, duplicate, reordered or unrelated membership fails. Empty tree/receiver evidence and zero tree counters are required on fallback; pre-build capture refusals require a null tree. Partial tree coverage never passes a complete case.

Every explicit pair-visit diagnostic is bound to this reconstruction: F uses `N(N−1)`, H/H0 use their independently computed gathered nonself counts, and fallback uses all pairs with zero component tests. The unchanged `certifiedSkippedPairs` and `skippedCenterNormCalls` remain in full equality; neither is treated as a proof of whole-node omission.

## Semantic equality and artifact bindings

The complete encoded native payload must match F after removing exactly these paths: `method`, `tree`, `timing`, `diagnostics.buildPhasesMs`, `diagnostics.geometryWork.gatheredNonselfCandidates`, `diagnostics.screen.orderedPairVisits`, and `diagnostics.screen.componentTests`. The three differing count fields are separately checked against coverage. Unknown fields remain in equality by default.

Status, reason, refusal stage, constants, canonical raw words/IDs, prepared words, CSR offsets/source order/K/a, graph/admission diagnostics, all solution/root words, all rotor and resultant load words, and full status/ID/load consumption remain equal. The checker additionally validates raw-to-prepared bindings, strictly increasing nonself positive CSR sources, positive coefficient domains, solution/load IDs, and independently recomputes the FNV consumption from every saved status, ID and load word. This is semantic equivalence to F; it does not independently re-solve F's coefficients or roots.

Each of the 126 result sidecars is required at its fixed case-index/method path, with matching byte count/hash and body equal to the corresponding work row. Every complete case is durably appended to `results/work.jsonl`. The journal descriptor, complete rows and `work.json` case list must agree exactly in the frozen order. A missing/truncated journal, absent sidecar, partial arm set, changed input/source, unexpected record, mismatched manifest/commit/runtime, or incomplete work report cannot pass. Failure artifacts remain visible; there is no retry or replacement policy.

## Checker controls, separately reported

Six threshold comparison answers and 16 hardcoded subtraction answers exercise the checker's RN routine, including ±4 neighbors, ties on both sides of 4, signed zero, a subnormal and a span-boundary tie. These are checker sanity controls, not measurements of JavaScript arithmetic conformance.

Source review corrected one draft fixture before any execution: at the successor of 256, subtracting word `3d10000000000000` removes only one quarter ulp and must round back to the successor. The frozen intended tie fixture instead subtracts `3d20000000000000` (one half ulp), so its expected result is even word `4070000000000000`. No measured result motivated this correction.

Fifteen deliberate saved-record corruptions run only after unmodified primary records have passed: missing/duplicate/self gathering, a false cull, a wrong node bound, wrong node membership, raw ID, prepared center, reversed positive source order, coefficient word, root word, load word, consumption, admission and refusal status. Each must fail at its named check. They are labeled `saved-record-mutation-control`, retained separately from `primaryCases`, and never counted as native queries, primary refusals or independent samples. There are no injected failed certificates in the production query stream.

## Source preservation and explicit gaps

Textual diffs of both candidate wrapper and kernel were reviewed against their retained originals. Positive classification, immediate rotor consumption, coefficient append, the `positiveRotorTerms > 2000000` throw, scaled-cap arithmetic, graph/admission ordering, scaling, schedule, solve, residual, loads and consumption are unchanged. Source IDs are restored before the original loop body. The original whole-scene eligibility and fallback branch precede tree construction; center/rotor invalid guards retain their original order. No exact-reference radial/down rules were transplanted.

The scaled-cap refusal is distinct from the 2,000,000 positive-term resource limit. The latter cannot be reached by these small inputs and is **not dynamically exercised**. Its placement and error translation are source-reviewed only. Cooperative guard call sites are likewise source-preserved, but this first harness does **not** inject call-ordinal or wall-clock guard failures. Tree construction/traversal adds no cooperative polls and may add allocation failures; equality of timing-dependent failures or memory exhaustion is not claimed. Source review is not execution evidence for any of these gaps.

The proposed outer allocation remains work 120 seconds, checker 45 seconds, shared closure/overhead 15 seconds, 180 seconds total. The checker reserves ten seconds of its allocation for closure. Per-file output is capped at 32 MiB and combined results/private logs at 128 MiB with 2 MiB reserved for final records. Its live token, authorization/cutoff, publication, manifest, runtime and monotonic deadline checks precede saved-evidence work; it rechecks pinned sources before exclusive final output. No OS memory limit is claimed. A later separately preregistered whole-swarm/5000 experiment remains necessary even if every control here passes.
