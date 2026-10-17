# Saved tree-witness layout qualification

This is a separate, initially disabled saved-data representation experiment. It cannot resume or qualify the failed browser probe. The only permitted future work is encoding the tree evidence already present in 156 frozen native records and independently reconstructing that same tree evidence. No new scientific inputs, seeds, queries, derivatives, integration steps, reference computations, browser sessions, or native-kernel imports are part of this protocol.

Source is prepared and reviewed before any codec or checker execution. The parent owns syntax review, metadata packaging, disabled-source review receipt, effective authorization, full source/input/runtime manifest, commit, remote publication verification, and any single supervised launch. `config.reviewed-disabled.json` remains `executionAllowed: false`, `authorization: null`, `launchCutoffUtc: null`. No result directory is created during drafting. A source-only draft or packaging success is not a qualification result.

## Fixed evidence and selection

Input package: `research/m31-native-tree-browser-probe-2026-10-17`. The source attempt is frozen as failed, with original execution commit `4e1818c5b1ac7032018925edf17cecb1a6965e3d` and manifest SHA-256 `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449`.

Selection is fixed before layout execution:

1. All 126 records in frozen `results/saved-transport.json`, in that index's existing order. These are the prior saved-data compact tree representations, not regenerated native results.
2. All 30 `kind: native` records in the frozen `results/browser-journal.jsonl`, in journal order. They are the durable native-record subset of the failed probe, not a complete fresh scientific experiment.

The other 36 durable browser records, all 23 unreferenced partial shards, and any unacknowledged query are outside this input selection. They remain frozen in the old package. Shards needed by the selected descriptors are read-only inputs. No private browser log, profile, or absolute machine path is included in the public input manifest.

The packaging helper `source/prepare-inputs.py` is metadata-only. It checks these exact anchors, reads selected descriptors only to collect shard pins, hashes all reachable bytes, and creates exclusive metadata outputs. It imports no project source and does not decode scientific payloads.

| Frozen anchor | Bytes | SHA-256 |
|---|---:|---|
| Saved transport index | 58,498 | `b5245538e86c9f2a657205ce6177c90702e0c27bf22e247d44db5e63fe6900c7` |
| Browser journal | 23,514 | `e66b7234016d9851ce0dbc078e80e97c88dd2bbe8ed139db234b46c5d1eaa173` |
| Failed attempt report | 2,096 | `ccae2f966e131fe4a4c78640f3268722025060f885138242efa90e32962abc36` |

`input-index.json` has schema `m31-tree-witness-layout-inputs-v1`, the source package, the three anchor pins named `savedTransportPin`, `browserJournalPin`, `sourceAttemptPin`, and exactly 156 rows. Each row is `{index, origin, sourceSequence, recordPin}`. `index` is the consecutive combined index 0 through 155; `origin` is `saved` or `browser`; `sourceSequence` is the original saved-index position or original browser journal sequence; `recordPin` binds the complete original native descriptor. No record is selected by its observed compression ratio.

`input-manifest.json`, schema `m31-tree-witness-layout-input-manifest-v1`, lists the three anchors, 156 descriptors, and every distinct shard reachable from those descriptors. No source-native payload is rewritten as new output. Input files are excluded from the new-write budget because they remain read-only; their bytes must be hashed, pinned, and preserved.

`source/source-bundle.json` is an import/source-closure metadata document, not a browser bundle. It pins new source files and two frozen transport-only decoder dependencies: old `source/transport.cjs` and old `source/compact-check.py`. The execution manifest must union the complete input manifest, source closure, generated metadata, runtime, effective configuration, disabled review configuration, and protocol. The candidate may import the frozen JavaScript decoder only after gates. The independent checker may import the frozen Python Resolver only after gates. Neither stage may invoke the old scientific checker, producer, reference, or native kernel.

## Representation and equality contract

The layout is tree-only. A native record's non-tree fields stay bound through its unchanged original descriptor and input-shard closure. They are not re-encoded, omitted from the original input, newly recomputed, or represented as a newly qualified native record.

The candidate distinguishes three states explicitly:

- An absent `tree` field: output row records absence, `recordPin: null`, and zero original/new tree bytes.
- A present null `tree`: a new descriptor records `{tree: null}` and must reconstruct a present null field.
- A present tree object: a new descriptor records `{tree: layout}`. The independent decoder must reconstruct every logical property, list order, integer, exact binary64 word, schema, receiver, node, cull, leaf list, gathered candidate sequence, and counter from the selected original tree.

The planned representation packs culls into columns and represents actual gathered-index sequences using fixed deterministic bitmap/run/literal choices. It is lossless representation work. No certificate item may be discarded, inferred from a different native execution, replaced by aggregate counts, or skipped because it looks redundant. Exactly equal components may be shared only after actual byte/sequence equality; a hash alone never proves equality. Unknown shapes, malformed references, out-of-range indices, duplicate or unsorted membership, malformed runs/bitmaps, and changed word strings must be rejected under the source-defined limits.

The layout schema is `m31-tree-witness-columns-v1`, with exactly `schema`, `base`, `receiverIds`, `cullOffsets`, `cullCodes`, `cullDifferences`, `leavesRefs`, and `gathered`. `base` preserves the original compact tree's other fields, including the complete leaf dictionary. A cull code is `node * 6 + axis * 2 + side`, with side 0 for `min-ge4` and 1 for `max-le-neg4`; offsets retain each receiver's ordered cull segment. Differences remain exact binary64 word strings. A gathered sequence uses `{kind, count, data}` with literal/run uint32 data or bitmap sixteen-hex-digit words. Source index j occupies the least-significant-bit position `j % 64` in word `floor(j / 64)`. Fixed representation costs are `59 + 4*count` for literal, `56 + 4*data.length` for runs, and `58 + 8*ceil(n/64)` for bitmap, with ties resolved literal, runs, bitmap. Reconstruction preserves logical object contents, scalar types, word bits, and list order; JavaScript object-key enumeration order is outside the equivalence claim.

New evidence uses the existing `m31-lossless-record-v1` descriptor with a new package-specific shard prefix. Shards are content addressed, at most 1 MiB, and nonfinal chunks have the fixed 1 MiB boundary. The candidate imports its own source-pinned transport copy for new output; the copy's new path prefix cannot make old input references valid as new output.

The candidate index is `results/candidate.json`, schema `m31-tree-witness-layout-candidate-v1`, with source manifest/commit, `inputIndexPin`, `complete`, `passed`, `records`, `controls`, transport accounting, and scope. Each of its 156 rows binds `index`, `origin`, `sourceSequence`, `sourceRecordPin`, method, tree state, new `recordPin` or null, `originalTreeBinaryBytes`, `newTreeBinaryBytes`, and `logicalRoundtrip`. Original record bindings must equal the input index exactly. The independent checker binds and validates the actual descriptor/shard bytes rather than trusting the candidate's roundtrip flag or size counters.

## Frozen acceptance criteria and interpretation

Success requires all of the following, without selecting a passing subset:

1. Exactly all 156 selected records have correctly bound absent/null/object tree states and exact independent reconstruction of the complete original tree evidence. The candidate's own roundtrip is only a preliminary check.
2. Every fixed source-defined positive and malformed-representation control passes its expected outcome. The independent checker enforces the fixed list, not only a producer-supplied success boolean.
3. Original and new logical tree stream sizes are reported for every selected record. Record descriptor bytes, distinct new shard bytes, deduplication, and overall new retained bytes must be reported separately so the logical ratio is not confused with disjoint physical storage.
4. **Both retained N=5000 H trees** meet `newTreeBinaryBytes * 2 <= originalTreeBinaryBytes`. The denominator is the original descriptor's tree-field binary stream byte count; the numerator is the new descriptor's tree-field binary stream byte count. These are the two durable H inputs at original journal sequences 60 and 63, whose original tree streams are 43,030,681 and 43,040,079 bytes. Exactly these two target records must be present and independently checked. Descriptor and shared-shard overhead is separately disclosed.
5. All source, old-input, runtime, publication, output-preservation, cutoff, time, per-file, aggregate, and fixed-partition checks pass. Candidate and checker stages both exit 0, complete and passed. The outer supervisor must complete; its actual process exit is separately observed by the parent.

The candidate control list is fixed to eight entries, each exactly `{id, passed: true}` on success, in this order: `literal-selection`, `run-selection`, `bitmap-boundary-roundtrip`, `empty-roundtrip`, `duplicate-source-rejected`, `bitmap-tail-rejected`, `wrong-count-rejected`, `noncanonical-choice-rejected`. These exercise deterministic choice, word-boundary and empty roundtrips, duplicate indices, forbidden bitmap tail bits, count mismatch, and noncanonical representation choice. The independent checker must enforce this list and its own fixed malformed-layout controls, not infer control coverage from a count alone.

The independent control list is also fixed: one preserved positive control `fixed-three-encodings-and-literal-zero`, then sixteen rejected mutations in this order: `noncanonical-choice`, `padding`, `offset-end`, `offset-order`, `cull-code`, `difference-word`, `receiver-order`, `gather-order`, `gather-count`, `leaf-reference`, `unknown-field`, `base-literal-word`, `cull-order`, `run-overlap`, `bitmap-width`, `boolean-id`. Each mutation must fail with the exact source-defined reason documented in `CHECKER.md`; an unrelated exception is not a passed control.

The 50% ratio is an engineering target on development data already examined after a failed probe. It is not held-out evaluation, a new scientific result, or evidence that unseen trees will compress similarly. A ratio target failure is terminal for this single attempt even if exact reconstruction succeeds; the full observed table remains reportable with the failed target.

No browser/query speed, speedup, standalone frame cost, native semantic equivalence, exact-reference acceptance, or complete browser-stage qualification is claimed. A successful tree layout does not prove a complete future browser attempt fits the old 160 MiB evidence partition. Non-tree data and all stages still consume bytes. The existing two-million-positive-term admission ceiling permits a coefficient-only universal bound that cannot fit the old evidence allocation; this experiment does not change that ceiling or claim to solve that bound.

## Fixed resource and process envelope

| Allocation | Limit |
|---|---:|
| Candidate child wall time | 120 seconds |
| Independent checker child wall time | 120 seconds |
| Shared setup, source/input hashing, closure, and report overhead | 60 seconds |
| Whole supervisor reservation | **300 seconds** |
| User cutoff | **2026-10-17 05:06:20 UTC** |
| Latest possible full-reservation launch | **05:01:20 UTC** |
| New retained output + logs + scratch | **64 MiB = 67,108,864 bytes** |
| Any new file | **32 MiB = 33,554,432 bytes** |
| New shard | **1 MiB = 1,048,576 bytes** |

The supervisor requires a full 300 seconds remaining both before source-gate work and immediately before creating the fresh attempt marker. Setup time counts from interpreter start. It never stretches the total deadline or launches a partial-reservation attempt. Existing old input bytes are excluded from new-write totals; copies, rewritten payloads, private logs, temporary files, and new scratch are not excluded.

The fixed internal byte ledger is 56 MiB for `results/shards` plus `results/records`, 4 MiB for the entire private tree, 2 MiB for other public outputs, and 2 MiB for the attempt/finalization allowance. These allocations sum to 64 MiB and cannot borrow from one another. Each descriptor/index is additionally limited to 2 MiB. The aggregate guard counts extant files and reserves a further 2 MiB for closure; it may refuse conservatively before nominal partition balances are exhausted. Per-file and aggregate checks measure logical file bytes, not memory or allocated disk blocks. Output symlinks are rejected.

The candidate and checker must enforce cooperative guards while decoding/encoding and before new writes. The outer supervisor polls every 0.1 seconds, applies child CPU and file-size limits, kills and reaps its direct child on timeout or failure, and verifies the fixed byte partitions. A polling byte monitor is not an atomic operating-system aggregate disk quota. No process-memory ceiling or complete descendant-termination guarantee is claimed. The reviewed stages are forbidden to spawn children, create a browser, use network/Git, or create additional workers. The only scheduled processes are the supervisor and one direct stage child at a time.

Any input/source/publication mismatch, malformed record, failed control, ratio failure, output cap, missing full reservation, child failure, preservation failure, or deadline breach is terminal. There is one fresh results directory and one attempt marker, with no overwrite, rerun, retry, cap expansion, adaptive input replacement, or partial-result promotion.

## Authorization, publication, and preservation gates

The effective `config.json` schema is `m31-tree-witness-layout-supervision-v1`. Authorization uses exactly `{id, approvedUtc, reviewedSourceManifestSha256}` and the fixed cutoff. The reviewed disabled-manifest hash identifies the separately reviewed draft; the enabled config is itself bound by the execution manifest. The runtime is the exact prior pinned Node and Python byte identity in `runtime.json`; no Chrome or third-party package is needed.

Before opening outputs or importing codec/Resolver modules, each executable must verify the enabled configuration, source/input pins, actual runtime, `source-manifest.json` identity, and `source-publication.json`. Publication binds `commit`, `manifestSha256`, `manifestPath`, `manifestBytes`, `verifiedFilePins`, successful committed/remote-byte equality, and a verification time no later than the attempt start. Publication is created by the parent after the exact source bytes are reviewed and remotely verified.

The supervisor accepts `run.py MANIFEST_SHA SOURCE_COMMIT`. Direct stages accept `candidate.cjs ROOT MANIFEST_SHA SOURCE_COMMIT` or isolated Python `-I -B check.py ROOT MANIFEST_SHA SOURCE_COMMIT`. A stage requires `RESEARCH_EXECUTION_CONTEXT=tool-require-escalated`, its exact `RESEARCH_STAGE` (`candidate` or `check`), budget `120000`, the live run token whose SHA-256 appears in the running attempt, a started matching stage, source commit/hash binding, and the inherited monotonic child/total deadlines. Node options/path injection are rejected. The checker also requires the completed, pinned candidate output.

The attempt schema is `m31-tree-witness-layout-attempt-v1`. All stage output files are created exclusively. Before and after stages and at closure, the supervisor rehashes source/old-input pins and previously retained stage outputs. The checker may add its report but cannot mutate candidate artifacts. Results and private directories must be new, and private storage must be outside the repository. Reports contain sanitized errors and private-log byte/hash identities, not raw private paths.

`results/check.json` must independently report complete/passed, exact source binding, all 156 comparisons, fixed control outcomes, both target comparisons, per-record sizes, and limitations. `results/run-attempt.json` records source/input preservation, stage statuses and exits, byte accounting, elapsed-time scope, and no retries. Its `supervisorExitVerified` remains false because a process cannot self-certify its later exit; the parent records the external observation. Failed outputs remain evidence of the failed saved-data qualification only.
