# Independent prepared-reference static review

2026-10-17. **Source review passes for the proposed fixed 24-scene qualification.** This is a source-only finding, not a successful qualification result or a run allocation. No scientific module, fixture, reference, native calculation or browser was imported or executed. Reads, JSON metadata inspection, byte hashes and Python AST comparisons were used.

Reviewed: `source/run.py`, `source/cases.json`, `source/prepared-reference.py`, `source/DESIGN.md`; the frozen tree dispatcher and its qualified saved records/index; the frozen pair and semantic helpers; and the saved fresh native/reference schemas. The final source manifest/publication remains the parent's freeze step. The driver now fails before scientific imports unless every saved baseline tree pin is present exactly in that verified manifest.

## Fixed baseline, serialization and native shapes

`cases.json` is byte-identical to the qualified tree package's case list. It retains all 18 old exact-screening cases, four moving controls and both fresh N=64 targets in the same order, with no added scene, seed or regenerated motion. Each candidate scene is constrained to its declared size and at most 64 drones. The logical total remains 79,048; the previously qualified tree record total is 26,570 scalar pairs.

The driver's `wire` function is AST-identical to the qualified tree driver's serializer. The new target is compared by complete JSON structure equality with the corresponding saved tree record, covering raw words, prepared records, tree, order, canonical status/branch/witness, sparse scalar rows and coefficients, roots/all signed loads, compact coverage and its work counters. The comparator cannot accept only matching aggregate counts or positive subsets. It does not invoke the old all-pair scene oracle or recreate a fresh full reference.

The frozen baseline index is `research/m31-tree-first-reference-2026-10-17/results/index.json`, SHA-256 `3cd3f06d9d4ef1c43ffeceff445ba3fcd424f32c3e569ead4cceddf442104a7e`. It records the independently reviewed 24/24 qualification, with 16 admitted scenes and eight expected refusals. Before scientific imports, the new driver requires unique manifest paths, this index's membership, complete/qualified status and 24 cases, and exact equality of every index tree-record `{path,bytes,sha256}` pin with the manifest entry. The existing verifier hashes every manifest file. The new case-list path must also be pinned. Thus an omitted or differently pinned baseline cannot pass the import gate.

For the two fresh targets, the driver checks exact prepared/load equality and the complete positive identity/coefficient map against the prior saved reference. Its adapter retains the saved reference shape expected by `native.reference_target`: raw input drones, prepared records, full saved pair records, interval load rows, constant words and semantic input hash. The four F/L saved native reports must equal the prior frozen reports exactly. The 14 arithmetic fixtures and four existing load-law corruptions are explicitly retained in this allocation; their checks are not new browser/native simulations. The six prior tree-coverage controls are read from the qualified baseline and explicitly marked not rerun.

## Prepared binding and exact suffix

The prepared adapter is internal to one synchronous scene. It receives the pinned original, semantic and tree modules from the driver and imports only standard-library `Fraction` itself. `InputHelper.literal` preserves the decimal-versus-raw-word distinction, and all other original operations remain delegated to the frozen pair source.

Admission to its registry requires all 17 raw integer words, finiteness and positive nominal forces; then the original preparation function, the same returned object identity and unchanged contents, the original preparation validator and matching constant context. The unchanged tree already performs the scientific raw checks first, preserving its canonical raw/preparation refusal behavior. Adapter binding failures remain exceptions rather than scientific zero/refusal results.

The raw key preserves all 17 canonical words, including signed-zero bits and words unused by scalar geometry. Constants, corners and exact constant operands are snapshot-bound. Registered prepared objects are checked against their snapshots on scalar lookup. Duplicate raw rows retain all returned object bindings, so mutation of an earlier duplicate is not hidden by a later row. Exact center, axis, force, point and offset vectors are obtained from the frozen converter after successful validation; the offsets support `semantic.prepared_exact` and signed moments. No eager beta, normalizer, profile or positive interval calculation is introduced during registration.

An AST comparison confirms that the candidate suffix from the self branch through the final positive return is identical to the corresponding frozen `oracle_case` suffix. Its local operations bind the original exact helpers; `exact_vector` returns the cached value of the same validated word tuple. The self/center/neighbor/rotor/down/residual/near/width/radial/projection/cap/normalizer order, strict/non-strict boundaries, interval fields and coefficient expression are unchanged. The candidate makes no call to `original.oracle_case` and no call to the full semantic scene regeneration. Residual queries enter the adapter override through the unchanged tree dispatcher.

The first scalar call closes registration; pending preparation is prohibited. The wrapper closes its helper in `finally`. There is no shared cross-scene registry or mutable patch to frozen module globals. Arbitrary edits to private registry internals and concurrent callers are outside the documented internal API. This is a scoped reuse adapter, not a general external prepared-input certification interface.

## Six fixed binding controls and counters

Controls run once, after the completed `dense-cube-27` candidate, using receiver ID 100/input index 0, source ID 101/input index 1 and rotor 0. Missing fixed identities or an unexpectedly registered replacement row fail setup. No alternative witness is searched.

| Control | Required failure |
|---|---|
| Unregistered receiver, fixed raw x word changed to exact 1 | `prepared-unregistered-receiver` |
| Unregistered source, fixed raw x word changed to exact 2 | `prepared-unregistered-source` |
| Registered prepared center temporarily changed | `prepared-operand-mutated` |
| Copied `mg` constant word with low bit flipped | `prepared-constants-context` |
| Copied corner rows 0/1 exchanged | `prepared-corners-context` |
| Original pair attempted after context close | `prepared-context-closed` |

The prepared-center mutation is restored in `finally`, followed by a snapshot restoration check. Other mutations use copies. Scientific counters are copied before controls; each control reports its own counter and shared-budget deltas. Only the designated `BindingError` is caught; an unexpected exception propagates. Detection requires the exact reason and zero suffix calls. If a mutation reaches the suffix, that call is counted and cannot qualify as a successful control.

The driver requires six detected controls, per-scene suffix calls equal to both the emitted scalar record count and the saved tree count, exactly two scientific operand lookups per pair, zero pair preparations and a global total of 26,570 calls. The counter schema includes `prepareOneCalls`, `preparationValidCalls`, `oracleCalls`, `operandLookups` and `pairPreparations`. Preparation counters exclude raw-invalid rows; the legacy tree `coverage.work.preparationCalls` intentionally still counts input rows. A zero `pairPreparations` counter is supported by the source restriction and unchanged suffix; it is not a substitute for those source checks.

## Allocation and failure behavior

The driver pins the isolated, no-bytecode Python runtime and verifies public-source receipt identity before scientific imports. It requires at least 600 seconds remaining before the fixed 03:00 UTC cutoff, both before and after pin/baseline verification. A preexisting STARTED receipt or results directory prevents reuse of this allocation.

One candidate call is made for each of the 24 cases. A single shared suffix budget starts at zero with limit 30,000, is passed to every scene and increments immediately before suffix entry. The reviewed path neither replaces nor increases that limit. Preparation/validation/query guard polls and a 540-second alarm bound scientific work; closure is limited to the remaining allowance capped at 60 seconds, within the 600-second reservation. There are no sleep loops, retries, background workers, full-oracle comparison runs, simulations, browser calls or drone-cap extensions. A timeout, budget or binding failure cannot be converted into a model decision or qualification.

Output files are bounded by 32 MiB each and 256 MiB combined; creation is exclusive. Source and protected output bytes are rechecked during closure. Failures clear complete/qualified status, and an overall deadline excess also fails qualification. Recorded timings explicitly include the scheduled binding controls and are labeled one ordered qualification, not a performance estimate.

## Resolved findings and review boundary

Three pre-run issues were resolved during this source review:

1. The initial vector registry omitted offsets consumed by `semantic.prepared_exact`; offset registration is now present.
2. The initial counter schema lacked the driver's `pairPreparations` field; it is now present with the documented zero meaning.
3. The initial driver relied on general manifest coverage of baseline files; it now explicitly binds the qualified index and all 24 exact tree-record pins before scientific imports.

No remaining source correctness blocker was found in the reviewed path. This approval depends on freezing these reviewed bytes and all read dependencies, including the baseline records, fresh saved references/browser/check/generation/input files and original helpers, then satisfying the public-source and finite-allocation gates. It does not authorize a rerun after failure or a changed case/cap/budget.

The prepared module reviewed after fixes has SHA-256 `19efcb01f4c6d45b517b2388bcdaf045daf382bc11e7442dd8b9627e1807a921`; its design note has SHA-256 `9a1179cf7999f0cbfc89d87009de9d166a5e8c93ebd4c294a4987469ac95c4d2`. The driver and complete dependency hashes belong in the final source manifest. AST/suffix equality and this review are source evidence only. A later exact saved-baseline pass would qualify this reuse change on the finite corpus; it would establish no speedup, 5,000-state feasibility, aerodynamic-model novelty or physical validation.
