# Native center-tree source design — 2026-10-17

This package is source preparation for the first numerical-equivalence qualification of H and H0 against the existing native F. No candidate module was imported, bundled, syntax-checked, or executed during this drafting cycle. No scientific result, timing result, performance improvement, new trajectory, runtime-wide equivalence, physical validation, or novelty is claimed. Parent review, source freeze, and a separately authorized bounded execution are still required.

The design follows `../m31-coupled-stage-qualification-2026-10-17/review/NEXT-EXPERIMENT.md`. The unchanged F still performs every directed nonself source visit before its component screen. H replaces only that enumeration with a center AABB tree that can certify the same component screen for a complete node. H0 builds and traverses the same tree but forces descent. Neither method changes positive contributions.

## Entry points and dependency boundary

The original comparator remains `../m31-native-fresh-transfer-2026-10-17/source/native-load.cjs`, called with `query(input, 'F', guard)`. It is not edited and does not import the candidate tree. It therefore incurs no candidate tree construction, traversal, gathering, ordering, or evidence collection within its query.

The candidate entry point is `source/native-load.cjs`:

```js
const answer = candidate.query(input, 'H', guard, {treeEvidence: true});
const encoded = candidate.encodeEvidence(answer);
// Substitute 'H0' for the forced-descent control.
```

The method defaults to H; only H and H0 are accepted by this fork. Omitting the fourth argument leaves `answer.tree` and `encoded.tree` null. The fourth argument is a trusted harness option, not an additional scientific input format. The raw drone interface, canonical copying, IDs, validation, limits, refusal reasons, and successful result schema are unchanged. The optional tree field is the only new top-level evidence field.

The candidate native wrapper requires `./kernel.cjs`; the kernel requires `./tree.cjs` and the retained `anchor-kernel.cjs`, `lean-anchor.cjs`, and `reference-excerpt.cjs` under `../../m31-native-fresh-transfer-2026-10-17/source/vendor/`. Anchor and lean continue to require their unchanged local reference excerpt; lean continues to require its unchanged local anchor. The original native comparator additionally requires its retained `vendor/kernel.cjs`. The source freeze must cover this complete dependency closure and the harness/checker/configuration files.

## Tree construction and candidate ordering

Native input capture sorts strictly increasing safe-integer IDs before preparing states. Every tree source index is the index in that canonical array; equal-coordinate ties on an axis are broken by canonical index and therefore by stable input ID.

The tree has leaf capacity 8. Every node's bounds are the component-wise `Math.min` and `Math.max` of its actual finite centers. Internal nodes choose the largest ordinary binary64 rounded `max[k] - min[k]`, with a strict greater-than comparison retaining the lowest axis on a width tie. Members are sorted by that coordinate and then canonical index, split at `floor(length / 2)`, and visited left then right. Node IDs follow preorder starting at 0. Only leaves retain member arrays; internal sizes are private traversal bookkeeping. Each receiver's gathered indices are sorted numerically in ascending canonical order before the unchanged F classifier consumes them. Self is retained in gathering and skipped at the original source-loop location.

For node `v` and receiver `i`, the only omission rules are, in axis order 0, 1, 2:

```text
RN(v.min[k] - receiver[k]) >= 4
RN(v.max[k] - receiver[k]) <= -4
```

The positive test precedes the negative test on each axis; testing stops at the first satisfied comparison. The endpoint operation is the same ordinary JavaScript subtraction used for the F source-center difference. For finite endpoint values, monotonicity of correctly rounded subtraction transfers either endpoint comparison to every member's same component. That member necessarily satisfies F's `max(abs(dx), abs(dy), abs(dz)) >= 4` screen. Equality at either face is included. This argument concerns only that unchanged component screen; it does not substitute for the later finite qualification of the complete native pipeline.

H0 calls the same predicate at every visited node, including its first-satisfied-test short circuit, but ignores a satisfied predicate and always descends or collects the leaf. H0 thus gathers every canonical index for every receiver. The forced-descent control includes tree construction, predicate work, traversal, leaf gathering and sorting. No down-axis, radial, rotor-aware or approximate-positive omission is present.

## Eligibility, arithmetic, and failure ordering

The F whole-scene predicate remains byte-for-byte unchanged: prepared center coordinates and the rounded axis spans must be finite, with all spans in `[0, 256]`. Tree construction occurs only after this predicate succeeds. An ineligible scene follows the same call to `lean.build(states, 'lean', fullSymbols, guard)`, including lean preparation and its original invalid-before-outside checks. The candidate performs no node omission in fallback. Raw input refusals still happen before preparation or tree evidence.

The numerical body of preparation, center tests, point sums, rotor classification, immediate per-rotor consumption, source tuples, incoming sets, CSR packing, dependency ordering, admission reason ordering, `K`, `a`, left-associated sums, schedule, root solve, residual, loads and consumption remains unchanged. The copy retains unreachable typed-assembly branches solely to minimize the source diff; H and H0 always use the ordinary tuple/Set assembly used by F.

The original receiver-level guard remains in the same place, before rotor point computation. No new guard is introduced inside tree construction or traversal. All other native guard call sites remain unchanged. Consequently a guard defined by call ordinal encounters the same numerical checkpoints; wall-clock deadlines can of course be reached at different checkpoints because the candidate does different enumeration work. The proposed first run is bounded to at most 64 and depends on the independent outer wall/CPU containment. No claim of 5000-ready cooperative containment is made. Tree allocations may also introduce resource failures of their own; this design does not claim equal memory-failure behavior.

Sources are consumed in ascending canonical order and rotors immediately in order 0 through 3. The existing `positiveRotorTerms > 2000000` throw remains immediately after the positive append and before the scaled-cap calculation, with the same error message and native translation. Scaled-cap and admission checks are not relocated. No cap is lowered for this fork. Small/64 qualification controls cannot exercise the fixed 2,000,000-term guard; source preservation of that throw must not be represented as an executed cap stress test.

## Requested coverage evidence

`encoded.tree` uses schema `m31-native-center-tree-v1`:

| Field | Meaning |
| --- | --- |
| `mode`, `leafCapacity`, `n` | H/H0, fixed 8, canonical input count |
| `eligible`, `fallback`, `fallbackReason` | Unchanged whole-scene F routing decision |
| `complete` | Full kernel build returned; it does not mean native admission or solve succeeded |
| `canonicalIds` | Canonical stable input IDs; index-to-ID association |
| `nodes` | Preorder nodes `{id,min,max,left,right}` with `members` only on leaves |
| `receivers` | Traversal records in receiver order |
| `counters` | Requested integer work accounting described below |

All node minima/maxima and cull differences are 16-digit big-endian binary64 words in encoded evidence. A receiver record is `{receiver, culled, leaves, gathered}`. `culled` contains `{node,axis,side,difference}`, with side `min-ge4` or `max-le-neg4`; `leaves` gives visited leaf IDs in traversal order; `gathered` is the actual sorted source array consumed by the classifier, including self. Internal node membership can be derived from descendant leaves. The checker must reconstruct the deterministic tree and the complete traversal partition, recompute rounded endpoint predicates, verify membership bounds and canonical ordering, and compare the actual gathered array with the sorted retained-leaf members.

Evidence creation is optional. Without a request, the live tree and one receiver's candidates still exist for computation, but no coverage record arrays or traversal counters are retained. With a request, node storage is O(N) and saved gathered lists can be O(N²) in a dense forced-descent scene. This first qualification is restricted to small cases and one exposed 64 case. The implementation never requests a 4N² symbol tensor for coverage (`fullSymbols` remains false in the native wrapper). No claim of linear-size dense full-candidate evidence or measured heap usage is made.

The sink publishes coverage before construction/fallback so a later build refusal can retain partial evidence. For pre-build raw failures, `tree` is null. A fallback build that returns has `complete:true`, no tree nodes or receiver records, and all tree counters zero. A later domain refusal may still have complete build coverage. A thrown build retains `complete:false`; it must not be counted as full coverage. A receiver record can contain its complete gathered array even if its classifier subsequently fails. `completedReceivers` distinguishes that case.

| Counter | Exact increment rule |
| --- | --- |
| `treeNodes`, `treeLeaves` | Nodes and leaves created during tree construction |
| `receiverTraversals` | Calls beginning `gather` |
| `nodeVisits` | Every visited node, before its predicate |
| `endpointComparisons` | Actual positive or negative endpoint comparisons, including H0's ignored satisfied predicate; 1 to 6 per visited node |
| `culledNodes` | Nodes actually omitted by H |
| `omittedNonselfCandidates` | Sum of member counts of actually culled nodes; self cannot be in a culled node |
| `visitedLeaves` | Leaves actually gathered |
| `gatheredIndices` | Lengths of gathered arrays, including self |
| `gatheredNonselfCandidates` | Gathered indices unequal to that receiver |
| `completedReceivers` | Receiver classifier, row packing and dependency checks completed |

The legacy `geometryWork.certifiedSkippedPairs` remains `logicalDirectedPairs - directedCenterTests`, just as in F. It counts omitted center-norm calls, not only whole-node culls. Tree omissions are separately represented by `tree.counters.omittedNonselfCandidates` and the certificates; the historic counter alone is not a proof.

## Equality boundary and first qualification

The comparison must retain all native evidence fields except the explicitly differing method label, optional tree field, timing fields, and these enumeration diagnostics: `diagnostics.buildPhasesMs`, `diagnostics.geometryWork.gatheredNonselfCandidates`, `diagnostics.screen.orderedPairVisits`, and `diagnostics.screen.componentTests`. These work differences must also be independently checked against the certificate rather than silently ignored. Every other diagnostic, status, refusal reason/stage, raw/canonical word, prepared word, coefficient/source order, solution/root word, load word, and consumption result remains in the equality comparison. Existing encoded native diagnostics retain their original serialization convention; the new tree endpoints use explicit words.

`source/cases.json`, `source/check.py`, and `CONTROL-PROTOCOL.md` are owned by the evidence reviewer; harness/supervisor/configuration are owned by the supervision reviewer. The first source plan includes all-axis ±4 faces with neighboring words, strict radius faces, coincident centers and distinct IDs, canonical/permuted IDs, positive contributions, translated sparse centers, span boundary and fallback, invalid far inputs, near-field/scaled-cap/order refusals, raw ID failures, guard checkpoints, and saved-evidence mutations for missing/duplicate candidates and false culls. The final frozen case manifest, not this prose, determines the authorized bounded run. Any omitted control must remain an explicit qualification gap.

The existing 64 input is an exposed regression, not fresh qualification. No 5000 benchmark is part of this source cycle. A passing first run would justify only the registered finite cases and checker controls, not an untested scale or general runtime theorem. Conservative spatial filtering and center trees have antecedents; this fork carries no novelty claim.

## Drafting verification

Only source reads, source writes, textual unified diffs, and byte hashes were used. `DIFF-INVENTORY.md` identifies the preserved arithmetic and every edited region. Production F and its retained dependency sources were not written. The parent owns the source review, preregistration, freeze, execution decision, and any later viewer/publication.
