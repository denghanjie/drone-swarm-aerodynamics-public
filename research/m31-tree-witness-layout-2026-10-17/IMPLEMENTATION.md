# Saved tree-witness layout implementation

This is a source-only implementation description pending parent review, exact publication, authorization and the single supervised attempt. The candidate author has not imported or executed this codec, the candidate, any checker, or any scientific producer during source preparation. There is no browser or new numerical evaluation in this package.

The input corpus is fixed at 156 full native descriptors: the previous failed probe's 126 compact saved-validation payloads in saved-index order, followed by its 30 durably journaled browser native payloads in journal order. The old descriptors and every referenced shard are input-only. No orphan chunk is promoted to a complete record. Every source pin is checked before decoding; every input-manifest file is checked again before successful completion. Full native bodies are decoded only to obtain the actual tree field and method, while all other fields remain input-only and are never replaced by new numerical results.

## Evidence boundaries

An absent tree property, an explicit null tree, and an object tree are distinct. Candidate index rows record these as `absent`, `null`, and `object`. An absent tree has no new descriptor and both tree byte counts zero. A present tree, including null, is stored as a new transport record with exactly one field, `tree`.

The logical equivalence relation preserves object key sets, scalar types, every word-string bit pattern, numeric signed zero, nulls, and every array's order. JSON object property order is not evidence: the original compact tree's receivers property may have a different insertion position after reconstruction. All receiver order, within-receiver cull order, leaf-dictionary order and entries, gathered-array order, IDs, nodes, counters and bounds are retained.

The candidate does not establish native geometry, coefficient, load, RK, reference, safety, or query-speed correctness. Successful reconstruction says that this layout preserves the already saved witness, including any error the witness may contain. The original browser attempt stays a terminal storage failure with no retry or resume.

## Layout v1 contract

For an object tree, `layout.cjs` emits exactly:

```
{
  schema: "m31-tree-witness-columns-v1",
  base,
  receiverIds,
  cullOffsets,
  cullCodes,
  cullDifferences,
  leavesRefs,
  gathered
}
```

`base` retains every original `m31-native-center-tree-compact-v1` property except `receivers`, including the original schema, mode, leaf capacity, eligibility/fallback fields, completeness flag, n, canonical IDs, all nodes/bounds/members, complete leaf dictionary and counters. This experiment does not change leaf-dictionary encoding. The accepted base key set is fixed; n is an integer in [0,5000], nodes are bounded to 10,000, and receivers to n. These are saved-corpus format bounds, not new scientific admissibility claims.

For R recorded receivers, `receiverIds`, `leavesRefs` and `gathered` have length R; `cullOffsets` has length R+1, starts at zero and ends at the cull-column length. Offsets are nondecreasing and bounded. Receiver IDs and valid dictionary references remain their actual values; a null leaf reference stays null.

The cull columns concatenate each receiver's original culls in receiver order. For each cull:

```
code = node * 6 + axis * 2 + side
side = 0 for "min-ge4", 1 for "max-le-neg4"
```

Node and axis bounds are checked before packing. The code is a nonnegative u32 integer. `cullDifferences` stores each exact lowercase 16-hex-digit difference word in the same position. Decoding uses integer quotient/remainder to recover node/axis/side and preserves the difference string without floating conversion. Offsets bind each resulting cull sequence to its original receiver. No cull is inferred by rerunning a predicate.

A null gathered value remains null. Otherwise each new gathered value is exactly `{kind,count,data}`, with count equal to the actual number of source indices. Input compact runs/literals are expanded, checked for bounded strictly increasing integer indices, and checked against the old canonical rule before the new representation is selected. The old rule uses runs only when their integer-element count is strictly smaller than literal length. It chooses literals on ties, including an empty literal array.

The new options are:

| Kind | Data | Exact encoded value bytes under pinned transport |
| --- | --- | ---: |
| `literal` | Actual ordered indices as u32 values | 59 + 4 × count |
| `runs` | Alternating start,length integers | 56 + 4 × data.length |
| `bitmap` | Exactly ceil(n/64) lowercase 16-hex words | 58 + 8 × ceil(n/64) |

These costs include the entire three-property value's transport object/header/keys, kind string, count scalar and array header. Empty arrays retain the generic five-byte array representation. Selection takes the minimum cost with tie order literal, runs, bitmap. Costs are evaluated before bitmap construction; a full H0 actual set can remain a two-integer run. The formula is an encoding rule, not a deduplication estimate.

Bitmap source index j maps to word floor(j/64), bit j mod 64, with bit zero the least-significant bit of that 64-bit word. The word is written as usual most-significant hex digit first. For n=70, indices `[0,1,63,64,69]` encode as `["8000000000000003","0000000000000021"]`. High bits outside the domain must be zero. The decoder checks word syntax, word count, tail bits, cardinality, strictly increasing expanded indices, and the canonical minimum-cost choice. It then reconstructs the original compact gathered object using the original run/literal rule. Original actual arrays are never replaced by membership inferred from method, tree, or a boolean equality flag.

## Transport and index

`source/transport.cjs` is copied from the byte-frozen prior pure transport. Its sole text change is the canonical shard directory prefix from the old package to `research/m31-tree-witness-layout-2026-10-17/results/shards/`. The candidate imports the old pure transport only for reading old descriptors, after authorization, source, runtime and publication checks. It imports no native/kernel/factory/reference module.

New records retain the standard `m31-lossless-record-v1` descriptor and `m31-value-stream-v1` field streams. All old transport type tags, bounds, one-MiB canonical chunks, word encoding, counts and shape checks remain. Each present tree descriptor contains only `{tree: layoutOrNull}`. Paths are `results/records/NNN-tree.json` using the fixed input ordinal, and content-addressed `results/shards/SHA256.bin`. Actual bytes are hashed and compared completely before any existing shard is reused; a hash match alone cannot authorize reuse. New files are exclusive writes, fsynced, followed by directory fsync.

`results/candidate.json` has schema `m31-tree-witness-layout-candidate-v1`, source-manifest/commit bindings, the input-index pin, complete/passed flags, records, fixed controls, target rows, input-preservation status and transport diagnostics. Each successful record row is:

```
{
  index, origin, sourceSequence, sourceRecordPin, method,
  treeState, recordPin,
  originalTreeBinaryBytes, newTreeBinaryBytes,
  logicalRoundtrip: true
}
```

The candidate first compares its direct layout decode with the original compact tree, then encodes/persists/decodes the new transport and repeats the logical comparison. The independent Python checker is separately authored and must establish its own reconstruction from the saved bytes. Candidate comparison booleans do not substitute for that checker.

The candidate requires exactly two target rows: browser-origin H objects with n=5000, each with new tree field binary bytes at most half its original tree field binary bytes. Descriptors, shard reuse and all output overhead are reported separately; the target is not a claim of physical whole-attempt fit. All 156 records and every control must pass before complete/passed becomes true.

## Fixed candidate controls

The ordered candidate control list uses `{id,passed}` rows:

1. `literal-selection`: one retained source index at n=5000 selects literal.
2. `run-selection`: 100 consecutive indices at n=5000 select runs.
3. `bitmap-boundary-roundtrip`: the n=70 example above selects bitmap and reconstructs exactly.
4. `empty-roundtrip`: the empty n=0 set reconstructs exactly under the new cost rule.
5. `duplicate-source-rejected`: duplicate input indices cannot be encoded.
6. `bitmap-tail-rejected`: a set out-of-domain high bit cannot be decoded.
7. `wrong-count-rejected`: declared cardinality must match actual data.
8. `noncanonical-choice-rejected`: a larger literal encoding cannot replace the required run form.

These are representation controls with no native calls. The independent checker additionally owns its saved-data corruption controls; their implementation and result must be assessed independently.

## Supervision and limitations

The candidate entry point is `node source/candidate.cjs ROOT SOURCE_MANIFEST_SHA SOURCE_COMMIT`. It refuses to proceed without enabled authorization, the exact running supervisor token/stage, 120,000 ms stage budget, matching runtime/source manifest/publication, and a private log directory outside the repository. Its shard and descriptor directories must not already exist. It spawns no children. The supervisor owns the one permitted attempt and the candidate/check stage exits.

Fixed resource limits are 120 seconds candidate, 120 seconds independent checker and 60 seconds overhead, with a full 300-second reservation before the absolute cutoff. All new outputs/private material share 64 MiB: 56 MiB evidence, 4 MiB private, 2 MiB other public and 2 MiB finalization allowance. Per-file maximum stays 32 MiB, shards 1 MiB, and descriptors/index 2 MiB. Every candidate write is budget checked; failed writes may leave an incomplete preserved prefix. The supervisor remains the independent total/partition/deadline authority.

The output is a narrower storage qualification on exposed witnesses. It cannot demonstrate that the original full 16-stage/48-query browser plan fits, that all unexposed N5000 stages will have similar witness sizes, that browser capture is faster, or that the native numerical result is correct. The original failed package is read-only provenance. No fresh seed, state, producer, browser or exact-reference call occurs here, and any candidate/check timeout, failure or quota event is terminal without retry.
