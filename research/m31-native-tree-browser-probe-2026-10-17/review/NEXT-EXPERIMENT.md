# Next experiment: qualify complete evidence storage before another browser attempt

Status: **source-only proposal after a terminal operational failure**. This document neither changes the frozen protocol nor authorizes implementation, a new producer/reference/checker call, a retry, a resume, a replacement seed, or a cap increase. Its author only read source and saved files, parsed saved descriptors/value streams with a standalone standard-library reader, counted bytes, and computed hashes. No candidate, reference, or checker module was imported or executed for this analysis.

The proposed next work is a separately reviewed, saved-data-only storage-format qualification. A fresh scientific experiment would follow only if that qualification provides a credible whole-attempt capacity case under the existing caps and receives separate authorization. The current attempt remains failed regardless of a later format's success.

## What failed, and what can be claimed

The frozen attempt is bound to source manifest `52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449` and source commit `4e1818c5b1ac7032018925edf17cecb1a6965e3d`. Saved126 validation completed successfully. Browser persistence then failed with `store-evidence-cap`; the supervisor recorded terminal failure. The exact-reference and independent-check stages never started.

The durable journal contains 66 records, including 30 native records and ten stage records: all four stages at N64, all four at N1000, and the first two at N5000-a. The final committed record is `0065-stage.json`, for N5000-a k2. Fixed execution order next schedules H at k3, but no descriptor/journal row for that append was committed. Unreferenced stored chunks do not establish a complete k3 result.

This establishes an operational storage limitation. It does not establish the registered N5000 speed gate, all-stage correctness, numerical reference acceptance, or a full 5,000-drone result. Partial producer agreement, candidate counts, and serialization times cannot replace the missing independent checks or turn an incomplete storage attempt into speed evidence. No primary query-time ratio is inferred here.

## Saved-byte diagnosis

The following counts are file-content bytes, not filesystem allocation blocks. Referenced-shard accounting uses the union of paths in all 126 saved descriptors and all 66 committed browser descriptors. All shards, including unreferenced ones, remain part of the evidence partition and are preserved.

| Saved quantity | Bytes |
| --- | ---: |
| All 948 shard files | 166,311,854 |
| 126 saved-validation descriptors | 687,982 |
| 66 browser descriptors | 412,031 |
| **Total evidence partition** | **167,411,867** |
| Fixed 160 MiB ceiling | 167,772,160 |
| Remaining capacity at failure | 360,293 |
| Shards referenced by committed descriptors, union | 146,083,646 |
| 23 shards with no committed descriptor reference | 20,228,208 |
| Unique shards referenced by saved validation | 694,701 |
| Unique shards referenced by committed browser records | 145,389,684 |
| Shards shared between those two sets | 739 |

Saved validation's complete footprint was 1,382,683 bytes: its descriptors plus its unique shards. Moving or omitting that required preflight evidence would not address the main cause. The storage controller's browser-instance counters report 166,029,184 new bytes and 40,671,014 deduplicated bytes. Those counters include progress on the failed append and must not be interpreted as the committed-record union. Their new-byte total plus the saved-validation footprint exactly equals the observed evidence partition.

The failed append's unreferenced 20,228,208 bytes explain why the partition can be full while committed descriptors refer to fewer bytes. Removing them would not finish the experiment; it would discard failure evidence and leave most large-case stages unrecorded. Record-level reservation could make a future failure cleaner, but cannot create storage capacity.

For the completed large-case records:

| Stage and method | Native record binary bytes | `tree` binary bytes |
| --- | ---: | ---: |
| N5000-a k1 F | 6,765,421 | absent |
| N5000-a k1 H0 | 7,701,348 | 935,926 |
| N5000-a k1 H | 49,796,102 | 43,030,681 |
| N5000-a k2 H0 | 7,701,368 | 935,926 |
| N5000-a k2 H | 49,805,520 | 43,040,079 |
| N5000-a k2 F | 6,765,441 | absent |

The committed browser `tree` streams occupy 101,195,041 unique bytes, 69.60% of its unique referenced-shard footprint. In fact, every committed browser tree chunk is distinct across records: tree logical-byte total equals unique stored tree-byte total. H k1 and k2 share zero tree chunks; H0 k1 and k2 also share zero tree chunks. Top-level field separation already saved substantial common native evidence across methods, but it did not provide tree reuse.

Direct parsing of the two completed H tree streams locates the growth:

| H tree component | k1 | k2 |
| --- | ---: | ---: |
| Encoded cull arrays, including repeated cull objects | 21,543,024 B | 21,552,838 B |
| Cull entries | 244,426 | 244,539 |
| Encoded gathered-index objects/arrays | 18,062,676 B | 18,062,304 B |
| Gathered source indices, including self | 4,465,669 | 4,465,576 |
| Receivers using literal gathered arrays | 5,000 / 5,000 | 5,000 / 5,000 |
| Encoded leaf dictionary | 2,743,162 B | 2,743,118 B |
| Distinct leaf sequences | 3,833 | 3,833 |
| Stored leaf indices across that dictionary | 680,998 | 680,987 |
| Encoded tree nodes | 291,233 B | 291,233 B |

Cull and gathered evidence alone occupy 92.04% of the k1 tree stream. Generic tagged objects repeat `node`, `axis`, `side`, and `difference` keys for each cull. Every difference word is required evidence; repeated key strings and repeated schema structure are representation costs. All 5,000 H gathered arrays selected literals under the frozen rule, so run encoding did not help those actual arrays. This is an observed encoding result, not an assumption about arbitrary random layouts. In contrast, each H0 receiver's actual gathered array encoded as one run, and all H0 receivers shared one 1,024-entry leaf sequence, explaining its much smaller tree.

The fixed 1 MiB chunks begin at each top-level field. Changing numeric bounds and cull difference words, or inserting/removing nested entries, can change those chunks without allowing stable nested parts to share storage. The saved zero-reuse result shows the limitation here; it does not prove that another chunking scheme will succeed.

There is also material overhead outside the tree. In the first N5000 stage, native `prepared`, `solution`, and `loads` fields together contain 1,400,000 bytes of repeated property keys. The stage `records` field is 5,115,005 bytes, including 1,445,000 bytes of property keys, 275,005 bytes of array headers, and 50,000 bytes of object headers. The controller `records` field is 3,431,389 bytes, including 885,000 bytes of property keys. These are counted representation bytes; removing them requires a validated, reversible schema representation, not omission of the corresponding values.

## Proposed format experiment, still to be designed and qualified

The most promising scope is a complete evidence-format change with fixed schemas for repeated records, exact typed columns, and separately addressable bounded blocks. It should leave the numerical method and scientific evidence requirements unchanged. The following are design hypotheses and arithmetic payload counts, not a working codec or proof that the full experiment fits.

1. **Encode culls as ordered columns with receiver offsets.** Store each actual cull's node as u32, axis as a checked one-byte enum, side as a checked one-byte enum, and exact difference word as eight bytes. Preserve receiver order and within-receiver cull order through explicit offsets. A fixed schema reconstructs the original keys and exact side strings. For the saved k1/k2 counts, the raw columns plus 5,001 u32 offsets would occupy 3,441,968 / 3,443,550 bytes, before tags, schema binding, descriptors, and integrity metadata. Both cull words and order remain fully recoverable; no predicate is rerun to manufacture the witness.

2. **Add a canonical bitmap option for actual sorted gathered arrays.** A 5,000-bit set takes 625 payload bytes per receiver, or 3,125,000 bytes for 5,000 receivers before framing. The encoder must first validate and encode the actual array that feeds the unchanged classifier: finite integer domain, strict ascending order, no duplicates, exact membership, and exact length. A fixed deterministic comparison among literal, run, and bitmap byte sizes chooses the representation. Include domain/length, reject nonzero unused bits, and verify decoded cardinality and sequence. Keep the smaller actual H0 runs. A bitmap must never be synthesized merely because the method label is H0 or because a tree suggests membership.

3. **Consider a bitmap option for leaf dictionaries only when order is preserved.** Source allocates tree node IDs in preorder and visits left before right, so completed leaf sequences should follow a fixed leaf order. A future saved-only qualification must verify every actual sequence against the explicit leaf-ID/ordinal mapping; any nonmonotone or duplicate sequence requires a lossless ordered fallback or format rejection. At 1,024 leaves, the 3,833 saved distinct sequences would need 490,624 bitmap payload bytes before mapping, references, and framing. This is not permission to replace recorded traversal by inferred coverage. Keep exact sequence interning checks, not hash-only reuse.

4. **Columnize the complete repeated native, controller, and stage records.** Preserve every raw/prepared value, complete CSR offsets/source indices/K/a, all solution and load words, all controller neighbor IDs, projection data, consumed IDs/status/loads, derivatives, RK intermediates, endpoint and safety evidence. Fixed schema keys and fixed vector dimensions can be represented once; variable-length fields require explicit checked offsets. Preserve exact word strings and numeric signed zero. Any narrower integer representation needs checked bounds and exact reconstruction. The byte counts above make this a necessary part of the storage investigation, not a cosmetic optimization.

5. **Use path-bound, independently sharded sections for exact reuse.** Bind each section to schema/version, case, stage, method, field path, ordinal, shape, element count and total length. Hash lookup may select an existing candidate block, but sharing still requires comparison of every actual encoded byte. Do not bind an H payload to F data based on a boolean semantic-agreement result. Separate stable IDs, leaf dictionaries and other reusable columns from changing words where appropriate. New manifest overhead, small-block costs and reference counts must be measured, not ignored. Retain the existing top-level field, descriptor, journal, depth, element and logical-size limits; do not move an unbounded index into nested manifests.

6. **Stream bounded blocks and reserve writes explicitly.** Producing/consuming blocks incrementally can reduce live allocations and avoid holding a whole generic tree object plus encoded copy. It does not by itself reduce durable evidence bytes. A complete record's declared/derived size and descriptor headroom should be checked before commit, while staging/orphan bytes count against the same fixed partitions. A rejection remains terminal. No deletion of earlier required evidence, uncounted scratch area, extra output partition or relocated oversized file is a capacity strategy.

Tree-only changes are not a sufficient capacity argument. The k2 group added 13,667,460 unique non-tree shard bytes under the current format. Eight copies of that observed amount plus only the three proposed k2 cull/gather/leaf payloads would total 165,813,072 bytes, before tree nodes, manifests, large-case initial/controller/final records, or the smaller cases. Adding the already observed saved-validation and N64/N1000 prefix would reach 193,989,944 bytes. This illustrative repetition is not a forecast of unseen stages; it shows why a proposal must account for the entire evidence graph instead of presenting a tree compression percentage as a fit guarantee.

## Qualification gates for the proposed next work

The next authorized implementation effort should first operate only on already exposed data: the original saved126 evidence and all fully committed current records. Preserve the terminal attempt unchanged. The incomplete unreferenced shards may support forensic byte accounting but cannot be treated as complete qualification fixtures.

A separately authored decoder and format review should demonstrate exact reconstruction of every required logical value from the new representation, including word bits, signed zero, array and trace order, stable-ID associations, status/refusal cases and empty shapes. Compare against complete saved values, not their summaries. Retain the original saved corruption laws and add focused rejection cases for bitmap domain/tail/count changes, bad offsets, invalid enum codes, reordered or duplicate sections, schema/path substitutions, missing/extra/trailing data, oversized declarations, and changed reused bytes. Such checks would be transport qualification only; they would not add scientific queries or numerical acceptance to this failed attempt.

The feasibility report must count all encoded payloads, unique physical blocks, descriptors, journal/index bytes, staging/orphan allowance and qualification outputs. Report raw logical size and observed exact-dedup savings separately. Include cold unique-byte accounting so favorable reuse is not silently assumed. Measure encode/decode/transfer/persist costs separately if later authorized; successful offline storage does not establish browser runtime or query speed.

Before proposing a new scientific exposure, freeze a whole-attempt byte ledger covering all four cases, 16 stages and 48 native calls, both large-case steps, saved-validation evidence, every controller/step/safety record, and downstream reference/check/closure records. Derive fixed bounds where dimensions permit them and identify genuinely data-dependent quantities. Use pessimistic bounds or explicitly justified reserved capacity, never a guarantee extrapolated from these two large stages. If a credible full-plan capacity argument cannot be made within the existing ceilings, stop at the storage research result. A new attempt must retain hard runtime enforcement and accept terminal failure if its actual evidence exceeds the fixed bound.

There is no universal fit guarantee under the existing native admissibility limit: at 2,000,000 positive terms, K/a alone need 32,000,000 raw word bytes and source indices 8,000,000 bytes per stage before other evidence. Eight stages at that maximum exceed the evidence partition even with perfect F/H0/H sharing. This limitation must remain explicit. Do not lower that scientific limit, omit full coefficients, change the cases after observing size, or raise any storage/time threshold to manufacture a passing result.

## Scientific and timing invariants for any separately approved fresh protocol

Preserve the unchanged F kernel, full native pipeline, tree leaf capacity 8, split/traversal/sort rules, inclusive endpoint predicates, original guard sites and positive-term cap. Keep the real coupled projected RK step, shared projected-stage identity, independent per-method input decoding/copying, and exact all-arm semantic agreement before H loads drive the derivative. Preserve complete current source/runtime identity and supervision/closure requirements.

Retain the four small-case exact-reference stages and their fixed reference limits (maxDrones 180, 192 coefficient bits, 128 bisections, suffix cap 30,000), the four normalized load tolerances of 1e-8 plus frame checks, and all required independent evidence checks. Neither omitted references nor producer equality flags qualify the experiment.

Keep actual-array validation and compact witness capture inside the native query timer. If the evidence representation changes, account for its capture work at the same boundary for every arm. Transport encoding/comparison/persistence stay separately reported and inside the browser/overall wall budgets. Preserve the registered per-N5000 gate: the sum of four H query times at most 0.8 times the F sum, fewer gathered nonself candidates, and every correctness and operational gate passed. A format experiment cannot establish this gate.

Retain 256 MiB aggregate, 160 MiB evidence, 64 MiB private, 30 MiB downstream, 2 MiB closure, 32 MiB per file, and the existing logical/descriptor/journal limits. No no-retry rule is relaxed. The exposed current cases are development evidence for the format investigation; this document neither reclassifies them as fresh nor chooses replacement cases. Any later scientific protocol must identify exposure and seed policy prospectively, without selecting favorable instances from storage or timing outcomes.

## Evidence anchors

Paths below are relative to this package. These hashes anchor this proposal's observed inputs, not a new checker pass.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/browser-journal.jsonl` | 23,514 | `e66b7234016d9851ce0dbc078e80e97c88dd2bbe8ed139db234b46c5d1eaa173` |
| `results/browser.json` | 3,211 | `e619e52119aa3b8fd5d76d883855aa6763a1c6db7ab5357ddfba9378c31ebb2e` |
| `results/run-attempt.json` | 2,096 | `ccae2f966e131fe4a4c78640f3268722025060f885138242efa90e32962abc36` |
| `results/saved-validation.json` | 3,717 | `809fbdd360742df12ec5d8cba49e67d2845a320e682dbd265db46adb45091aec` |
| `results/records/0060-native.json` | 18,030 | `2de86534c7a94a61d59cdd1d00d0997c556c6cce25ea422e3b051521a35286d8` |
| `results/records/0063-native.json` | 18,029 | `5df442eb0730ed58e4ffa4b6d9e849b6308c35338ec7c16a69b06e2078f550a1` |
| `results/records/0065-stage.json` | 8,502 | `2a12c03418cc3614e5c182d951727c29928d8e78980802a4cea57336abe1f7df` |

The large H/H0 tree component accounting additionally read every referenced shard of records 0059, 0060, 0062 and 0063 and matched each shard's length and SHA-256 to its descriptor before parsing. The parser's byte-span totals matched the saved stream lengths. It did not recompute geometry, native outputs, reference values, or scientific acceptance. Frozen source rationale is in `SUPERVISION.md`, `IMPLEMENTATION.md`, and `source/{transport.cjs,transport-store.cjs,compact-codec.cjs,tree.cjs,browser-adapter.cjs,science-config.json}`.
