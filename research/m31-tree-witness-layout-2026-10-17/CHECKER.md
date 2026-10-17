# Saved-only witness-layout checker

This is a prospective source contract. It does not record an execution or qualification result. The previous browser-probe package, its terminal failure and its evidence review remain immutable. This follow-on reads already exposed saved records and tests a representation change only. It never calls an initializer, native numerical query, browser, exact reference, omission proof, controller or derivative/RK auditor.

## Fixed input closure

The corpus is exactly 156 existing native-record descriptors: all 126 entries of the prior `results/saved-transport.json` in their original order, then the 30 `native` rows of the prior `results/browser-journal.jsonl` in journal order. Each row binds its original descriptor pin, origin and original sequence. The prior terminal `run-attempt.json` is also pinned. The three anchor hashes are hardcoded in the checker; they bind the failed source commit `4e1818c5b1ac7032018925edf17cecb1a6965e3d` and manifest `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449`.

`input-index.json` lists the exact sequence. `input-manifest.json` must contain exactly those three anchors, the 156 descriptors and every shard referenced by every field of those descriptors, with duplicate references merged only by identical pins. That closure must be included in the new execution manifest. The old orphan shards and unrelated browser rows are excluded. Every input byte is rehashed before work and again at closure. Old inputs remain read-only and outside the new output budget.

Unchanged native fields are input-only evidence. They are not rewritten, recalculated or substituted: the exact original full-record descriptor remains the binding for them. The checker decodes the old tree and small identity fields; it does not rerun a full scientific native-payload audit. This distinction prevents a lossless-layout pass from being presented as independent numerical qualification of the failed fresh probe.

## New representation

An object tree is represented by `m31-tree-witness-columns-v1` with exactly eight fields: `schema`, `base`, `receiverIds`, `cullOffsets`, `cullCodes`, `cullDifferences`, `leavesRefs`, and `gathered`. `base` retains every old compact-tree field except `receivers`, including the original schema, topology, bounds, canonical IDs, leaf dictionary, status/fallback/completion fields and counters. These values must compare exactly to the saved input.

Receiver and cull order are preserved. For R receivers, offsets have length R+1, start at zero, are nondecreasing and end at both cull-column lengths. Each cull code is an exact uint32 `node*6 + axis*2 + side`, where side zero is `min-ge4` and one is `max-le-neg4`. Python independently obtains node and axis/side by integer division/remainder. It checks node bounds and original strict cull ordering and compares every reconstructed cull object, including its exact sixteen-hex-digit difference word, to the old row. Signed-zero difference words remain distinct.

Each gathered value is null or exactly `{kind,count,data}`. Literal data contains strictly increasing uint32 indices; runs contain increasing, nonoverlapping, nonadjacent start/length pairs. A bitmap contains `ceil(n/64)` lowercase sixteen-hex-digit words. Index j maps to word `floor(j/64)`, bit `j % 64`; the least significant bit is the lowest source index. Every unused high bit in the final word must be zero. Count is the exact expanded cardinality.

The canonical choice minimizes the full encoded candidate-object cost under the frozen binary transport, not JSON text length:

| Representation | Exact binary value bytes |
| --- | ---: |
| Literal, k indices | `59 + 4*k` |
| Runs, r maximal runs | `56 + 8*r` |
| Bitmap | `58 + 8*ceil(n/64)` |

These constants include object/key tags, kind-string bytes, count's finite-number encoding and array tags. Empty arrays still carry the generic array header. Ties use literal, then runs, then bitmap. The checker computes these costs independently from decoded indices and rejects a nonminimal representation even when it reconstructs the right set. It validates run maximality and bitmap padding separately.

The original compact runs/literal representation is also canonical: runs only when two integers per run are strictly fewer than the literal indices; ties use literals. Thus exact expanded sequence equality plus both canonicality rules preserves the original complete logical gathered value. The checker expands at most one receiver's candidates at a time, avoiding simultaneous N-by-N Python lists. No candidate set is sampled.

Object property order is excluded from logical equality. All object key sets, scalar types, literal word strings, numeric signed-zero bits, nested values and ordered arrays—including receiver, cull, dictionary, node and gathered-index sequences—are preserved. This scope is agreed before execution; it is not byte-identical reproduction of the old JSON property order.

An absent tree remains absent with no new descriptor and zero tree-stream bytes. An explicit null tree remains null and has a descriptor containing `{tree:null}`. An object tree has a descriptor containing `{tree:layout}`. The only new logical record field is `tree`; other native fields remain bound to their original record.

## Independent decoding and comparison

The checker imports only the pinned old standard-library `compact-check.py`, SHA-256 `87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee`, and invokes its pure transport `Resolver`, never its scientific proof functions. Old and new readers have separate path namespaces and caches. New streams use the same typed binary grammar with only the shard-path prefix changed. The Python layout decoder is separately written from the candidate's JavaScript layout implementation.

The reused transport reader verifies record/chunk descriptors, exact byte counts, content-addressed paths, hashes, fixed 1 MiB nonfinal boundaries, depth/element limits, types, finite numeric tags, duplicate keys, unknown tags, truncation and trailing bytes. It preserves literal word strings. Its cache performs strict structural checks before reuse and rehashes used pins at closure. Reusing this already qualified reader is disclosed; it is not a second independent binary-codec implementation.

For every input row the checker binds exact input order, method, presence/null/object state, original tree-stream length, new descriptor pin and new tree-stream length. It checks every unchanged base field, receiver ID, leaf reference, gathered sequence and decoded cull. Candidate roundtrip flags alone cannot pass: independent comparisons must succeed on all 156 entries. No original scientific theorem or physical calculation is reevaluated.

## Fixed controls

A tiny hand-written representation fixture has n=65, three receiver rows and four culls. It is not a generated swarm or a scientific witness. It includes all three selected encodings, an explicit negative-zero word, positive/negative cull sides and a second bitmap word. Its positive full comparison must pass.

Sixteen independent single-corruption controls each require their exact named rejection, preventing timeout or an unrelated error from masquerading as a successful control:

| Mutation | Required code |
| --- | --- |
| Correct sequence in a more expensive representation | `layout-gather-canonical-cost` |
| Nonzero bitmap padding | `layout-bitmap-padding` |
| Wrong final offset | `layout-offset-endpoints` |
| Decreasing offsets | `layout-offset-order` |
| Changed cull side/code | `layout-cull-equality` |
| Changed difference word, including negative to positive zero | `layout-cull-equality` |
| Reordered receiver IDs | `layout-receiver-order` |
| Reordered gathered indices | `layout-index-order` |
| Wrong gathered count | `layout-gather-cardinality` |
| Out-of-range leaf reference | `layout-leaf-reference` |
| Unknown layout field | `layout-fields` |
| Changed unchanged-base literal word | `layout-base-equality` |
| Repeated/out-of-order cull node | `layout-cull-order` |
| Overlapping runs | `layout-run-order` |
| Wrong bitmap word count | `layout-bitmap-width` |
| Boolean substituted for an integer ID | `layout-receiver-range` |

The candidate separately runs eight fixed JavaScript controls, whose exact ordered successful entries are required: literal selection, run selection, bitmap boundary roundtrip, empty roundtrip, duplicate source rejection, bitmap-tail rejection, wrong count rejection and noncanonical-choice rejection. These remain representation controls, not native queries or fresh scientific samples.

## Output and development-data size target

Each check-report row includes the original descriptor pin, origin/sequence, method, tree presence, n when available, new descriptor pin, old/new logical tree-stream bytes, full compared receiver/cull/gathered counts and encoding counts. A successfully compared row has `layoutQualified:true` and `scientificValidated:false`. This lets a saved-only viewer bind the changed layout to exactly the earlier captured poses and omission geometry without relabeling them as newly scientifically validated.

The fixed development-data storage target requires the new logical tree stream to be at most one half of the old stream for **both retained browser H trees at N5000**, in original journal sequence order **60, 63**. The checker independently calculates the integer inequality `2*newBytes <= oldBytes`, requires those exact two targets and binds the candidate's target records. It reports all 156 sizes, the total logical-tree ratio, physical unique evidence bytes and descriptor bytes separately. The actual new record/shard file inventory must equal the complete set of pins used by the new reader, so unreferenced evidence files cannot silently pass. A target miss is terminal; no alternative encoding recipe is tuned after exposure within this attempt.

This target uses already exposed development data. It is not held-out evidence, a native-query speed result, browser timing, an accuracy result, or proof that a future full four-case browser attempt fits its original cap. The old failed attempt remains failed. The new report's `passed` means the fixed representation qualification and registered storage target passed; `scientificValidated` remains false.

## Supervision and source boundary

Before imports, the Python entry point verifies enabled published source, all input/source pins, the matching live run token/stage, fixed isolated Python runtime and the closed candidate output hash. Publication binds the exact source commit, manifest path, bytes, hash and verified pin count; committed and remote bytes must equal local bytes, with verification no later than attempt start. The checker has 120 seconds with ten seconds reserved for preservation/reporting. Candidate and checker each have 120 seconds inside a 300-second total with 60 seconds overhead, all before the unchanged `05:06:20 UTC` cutoff. No subprocess is spawned by the checker.

New output plus private logs/scratch is bounded to 64 MiB: 56 MiB evidence, 4 MiB private files, 2 MiB other public outputs and 2 MiB final ledger allowance. Per file remains 32 MiB; shards are at most 1 MiB; descriptors/index/report are at most 2 MiB. The checker writes its report exclusively and rechecks all source/input/candidate output bytes first. Resource exhaustion is a terminal limitation, without a retry, changed seed, sampled comparison or increased cap.

The checker author reviewed the candidate layout and candidate driver text. The bit order, padding, three exact costs, cull code reconstruction, absence/null handling, unchanged-base preservation and actual byte-equality dedup contract match this document. No imports, tests, codec execution or scientific execution occurred during this source preparation. Parent syntax review, published freeze and any sole saved-only execution remain separate steps.
