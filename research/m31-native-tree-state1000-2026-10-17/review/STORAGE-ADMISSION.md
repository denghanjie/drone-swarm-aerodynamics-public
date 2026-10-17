# Cold storage admission for one N1000 state

This is a source-only arithmetic review, not an execution result. **Admit the complete successful 22-record schedule at a conservative 137,225,341 bytes (130.8683 MiB) of evidence, with 30,546,819 bytes (29.1317 MiB) below the unchanged 160 MiB evidence cap.** No shard sharing, numerical sparsity, favorable seed geometry, or reduced positive-term guard is credited. Adding the entire unchanged 64 MiB private, 30 MiB downstream and 2 MiB closure allowances gives **237,888,637 bytes (226.8683 MiB)**, below 256 MiB by the same 29.1317 MiB.

The precise admission scope is `cold-complete-success-evidence-no-sharing`. Complete failure capture is not guaranteed. The concrete exception is the recursive `nativeMalformed.response`, `nativeThrown.detail`, or `nativeInputMutation.actualInput` snapshot in `browser-adapter.cjs`: it is not restricted to the successful schema, and can expand beyond the structural bound. Existing transport/store guards must stop such a path and retain its incomplete prefix, including orphan shards. No deletion, retry, raised cap, or missing failure record may be relabelled as successful completion. This admission does not authorize a launch; `config.json` remains disabled and no fresh state was generated for this review.

## Exact schedule and storage partition

`browser.js` emits source and factories once; `browser-driver.cjs` emits 12 fixed wiring controls, one initial state, one controller, three full native records in F/H0/H order, one stage with 1000 derivative rows, one case summary, and one driver summary. Total: 22. There is no step, RK intermediate, endpoint, safety record, second state, source-code body copy, or fresh reference record. Bundle/source entries carry byte/hash/path metadata only. Saved prerequisites are read and hash-checked in place; the new preflight writes only the small `results/saved-validation.json`, with no old record/shard copy or reencoding.

The 160 MiB partition consists of `results/shards`, `results/records`, and `results/saved-records`. Journal, browser/checker summaries, saved-validation report, public logs and other result metadata fall in the separately reserved 30 MiB downstream partition. Browser profile, private logs and scratch fall in the 64 MiB private partition. The final attempt/closure allowance is 2 MiB. The arithmetic reserves these full allowances; it does not spend unused private or downstream capacity to rescue an evidence overrun. Runtime directory monitoring is polling, not an OS filesystem quota.

## Transport accounting

The frozen lossless transport stores null/boolean in 1 byte, finite scalar numbers or exact 16-hex words in 9 bytes, strings in `5+UTF8_length`, arrays in `5+sum(item_cost)`, and objects in `5+sum(5+UTF8_key_length+value_cost)`. Nonempty uint32 arrays cost `5+4n`; nonempty exact-word arrays cost `5+8n`. Empty arrays cost 5 bytes. Top-level fields are actually separate streams; the helper occasionally charges full object framing as a conservative overcount. The helper constructs only integer byte counts, never a scientific value array or a codec input, and imports only Python standard-library metadata/arithmetic support.

Every complete-success body has at most 32 top-level fields and each such key is at most 64 UTF8 bytes. A descriptor has at most 32 field headers, charged 256 bytes each, plus at most `96+32=128` chunk references under the unchanged 96 MiB per-record transport ceiling. Each reference costs at most 320 JSON bytes: its fixed new-package path, 64-hex digest, size and punctuation fit within that allowance. A 256-byte outer allowance gives **49,408 bytes/descriptor**, or **1,086,976 bytes for all 22 descriptors**. This intentionally uses the 96 MiB transport ceiling even for tiny controls. It is below the unchanged 2 MiB descriptor ceiling. Binary shards are at most 1 MiB and have no on-disk header or padding; every nonfinal stream shard is exactly 1 MiB. Thus the 32 MiB file ceiling is respected by every evidence shard and descriptor.

The largest successful native record bound is 43,777,970 bytes, below 96 MiB. Successful native coefficient arrays contribute 6,004,001 elements and less than 84.1 million logical JSON bytes; adding the bounded native/tree fields remains below 8 million elements and 128 MiB logical JSON. Other records are smaller. Consequently the unchanged 16-million-element, 256 MiB logical JSON and depth-64 transport limits are not hidden lower caps on this successful layout.

## Coefficients and complete non-tree evidence

For each native call, take the full unchanged cap `T=2,000,000`, even though this is deliberately conservative for an admitted N1000 directed graph. The coefficient payload is `20T+4(4N+1)`: source index is 4 bytes; K and a are 8 bytes each; offsets have 4001 entries. This is **40,016,004 raw bytes/call** and **120,048,012 raw bytes across three calls**. Exact coefficient object/array framing raises the per-call number to **40,016,071 bytes**. No shared input, K/a array, native result or tree bytes are deduplicated in this bound.

Every full native record retains all 1000 raw rows (172 bytes/row), all 1000 prepared rows (511 bytes/row), all solution rows with four alpha/x/T objects, all load rows with rotor/collective/world force/world moment, and the complete coefficients. An additional **256 KiB per native call** covers all remaining fields: IDs, 19 constants, status/model/method, record metadata, two hashes, consumption, diagnostics, timing and audit timing. This is a reserve backed by static schema, not a guessed data compression ratio: diagnostics have only two N-length integer arrays (incomingDegree and scheduleIndices), 12 symbol counts, three 3-value screen vectors, fewer than 256 remaining named scalar/short-string entries, and fixed nested objects. Even charging 128 bytes per such named entry plus 32 KiB for outer keys/fixed text is well below the reserve. Neither an N² symbol tensor, dependency list nor residual map is emitted by encodeEvidence. Timing and consumption are fixed scalar objects. The raw/prepared/solution/load arrays are counted separately and in full.

## Tree witness bound

Balanced median splits with leaf capacity 8 give exactly 128 leaves and 255 nodes at N1000: after seven splits, each leaf contains 7 or 8 members. The helper overcounts every node as a leaf carrying eight members, while charging numeric left/right fields even where actual nulls are smaller. It permits 1000 distinct leaf-dictionary entries, each listing all 128 leaves; this retains the entire dictionary without assuming useful interning. The resulting dictionary term is `5+1000(5+4*128)=517,005` bytes.

A receiver's culls are pairwise disjoint stopped subtrees. Each contains at least one leaf, so at most 128 culls/receiver and at most 128,000/call are possible. cullCodes use uint32 and cullDifferences exact 8-byte words; the paired payload is at most 1,536,000 bytes. receiverIds, cullOffsets and leavesRefs are all retained; the leavesRefs bound uses 9 bytes/entry, allowing the larger generic encoding should nulls occur.

The qualified layout selects the least exact transport cost among literal, runs and bitmap. Hence every gathered object costs no more than the N1000 bitmap, `58+8*ceil(1000/64)=186` bytes. Its 1000-item outer array costs at most 186,005 bytes. The remaining tree metadata, canonical IDs and counters receive 64 KiB. The resulting bound is **2,367,735 bytes per tree record**. This same pessimistic bound is charged independently to both H0 and H; H0's empty culls and repeated leaf list do not reduce it. Null/fallback trees are smaller. No scientific validity, coverage correctness, losslessness result, speedup or state eligibility is inferred from this storage arithmetic.

## Controller, derivative and fixed-record bounds

Grid inserts each stable index into exactly one cell and visits each candidate cell once. The controller's neighbor list therefore has at most N entries; the bound charges N rather than N−1 for every receiver. Including the full state, desired velocity, target, commands, saturation and desired quaternion gives **4,482 bytes/row**, plus 16 KiB outer metadata.

The complete derivative row costs **1,023 bytes**: both raw and projected 17-word states, two norm words, command/nominal-motor words, every consumed load component, body/total arm vectors, nominal yaw, gyro and all 17 derivative words. The stage additionally retains two full input copies and the complete command matrix; 64 KiB covers refs, three query timings, common timings, status and fixed metadata. The initial record retains its full 1000-state input plus 16 KiB.

The twelve wiring records are charged **64 KiB each**. Each fixture has at most two drones; its raw/envelope snapshot contains only that fixed fixture's raw/input/load arrays and scalar wrappers, plus at most two derivative rows. Its actual fixed schema is below 16 KiB even with the numeric snapshot wrappers. The source record is charged 64 KiB for 19 bounded source pins, 56 fixed Buffer assertions and local-shim metadata; factories 16 KiB for at most 19 fixed module paths. The case summary receives 16 KiB. The driver summary receives 128 KiB for scalar counts, one case, one stage timing and at most 21 append-timing/pin entries. No arbitrary exception text is included in these successful-record reserves.

| Complete-success body group | Upper bound, bytes |
|---|---:|
| case summary | 16,384 |
| controller | 4,498,389 |
| driver summary | 131,072 |
| factories | 16,384 |
| initial | 188,405 |
| native F | 41,410,235 |
| native H | 43,777,970 |
| native H0 | 43,777,970 |
| source | 65,536 |
| stage | 1,469,588 |
| wiring control 12 | 786,432 |
| All binary bodies | 136,138,365 |
| All descriptors | 1,086,976 |
| Total evidence | **137,225,341** |

## Failure, partial upload and operational scope

A complete success has no interrupted append, so the full body sum accounts for every emitted shard even if every hash is distinct. A failed append can leave unreferenced chunks; those are counted by the store's recursive evidence budget and remain retained. Before each chunk/descriptor write, the store checks the 160 MiB evidence and 256 MiB aggregate limits, retaining closure allowance. The supervisor separately monitors 32 MiB/file, 64 MiB/private and 30 MiB/downstream. Arbitrary malformed snapshots are only transport-bounded (96 MiB binary, 256 MiB logical JSON, 16 million elements), not success-schema-bounded; a late such record may fail to persist completely. Thus **137,225,341 is a successful complete-schedule bound, while 160 MiB is the hard admitted evidence ceiling for incomplete prefixes**. Evidence-budget failure is operational failure, not a scientific pass or a reason to alter this case, cap or archive.

This analysis bounds retained filesystem bytes, not JavaScript heap, peak RSS, renderer memory, browser profile growth, CPU work or completion within 120/180/360 seconds. Those remain independently supervised failure conditions. The 2,000,000 positive-term guard and all numerical/source guards are unchanged.

## Seed exposure metadata

The read-only repository search `rg -n -F '2026101741' --hidden --glob '!.git/**' --glob '!**/shards/**' --glob '!**/*.bin' .` completed successfully at approximately 2026-10-17 04:50 UTC. Its only pre-existing match was `research/m31-tree-witness-layout-2026-10-17/review/NEXT-EXPERIMENT.md`, which nominates a prospective seed and explicitly requires later exposure review. It is a planning statement, not execution evidence. A subsequent targeted new-package search found only this disabled source/protocol's case/seed declarations (producer, science config, checker and prose); the package has no execution result.

A second metadata-only inventory used `rg --files --hidden --no-ignore` (excluding .git and shards), selecting config.json, attempt JSON, STARTED, registry, exposure, science-config, cases and schedule filenames. It read all **140 matching files, 288,026 bytes, with zero skipped files**; the only seed match was the new disabled `source/science-config.json`. The broader initial content search used rg default ignore/binary handling; this second metadata pass explicitly included ignored files. These inventories found package-local attempt records and process-registry.cjs modules, but no authoritative global seed-exposure registry. The process registries concern process ownership, not seed history. This supports only **no recorded prior execution exposure found in the searched repository metadata**. It does not prove that the seed has never been used outside this repository, in unrecorded sessions, in Git history, or in excluded binary shards. No initializer/query was run to select, inspect or replace the seed. If an authoritative external exposure record later conflicts, resolve that metadata before any future freeze/launch; do not replace a refused, trivial, slow or failed case after execution.

## Source identities and reproduction

The following bytes were inspected as text/metadata. `source/storage-bound.py` was executed only as a standard-library arithmetic/hash helper; no native module, codec, initializer, browser, control or checker was imported or executed. Run it from any directory to reproduce its numeric result and current source pins. The manifest must pin this proof, the admission JSON, the helper and the reviewed producer/transport dependencies. Any schema/cardinality/path change requires review of this bound before execution.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-native-tree-state1000-2026-10-17/source/browser.js` | 16972 | `612a9ea9078cd1d7a3774b509b651bfae4bed9a28126cb48b8ee15a02aeffe6e` |
| `research/m31-native-tree-state1000-2026-10-17/source/browser-driver.cjs` | 13837 | `7b70df3a987ade0966320fe759352bfae80e3e0350cab98429497780bce2412d` |
| `research/m31-native-tree-state1000-2026-10-17/source/browser-adapter.cjs` | 14856 | `66834f82600caa35d9417baaafc8b3b57276f8a47a4ad25ef8f3aefa0905e990` |
| `research/m31-native-tree-state1000-2026-10-17/source/tree.cjs` | 4849 | `aa2aef07a0a5643da13d3007be30423dac44479e8352cf2b50b74aaa90c9e7f6` |
| `research/m31-native-tree-state1000-2026-10-17/source/layout.cjs` | 7545 | `310fce3d5f72abcdd1493cff487ae9c312027ec65f5e253fb0144dd50fb81c8e` |
| `research/m31-native-tree-state1000-2026-10-17/source/native-tree.cjs` | 34091 | `7254a35017150e98fa893a494be8ff74eccfa655fe26be66e30c80a12941cbb5` |
| `research/m31-native-tree-state1000-2026-10-17/source/transport.cjs` | 9831 | `70f965a471b603cd2ceee80e73e6fedd29e0d7e2d7b3bc0249a00690cf1bbaad` |
| `research/m31-native-tree-state1000-2026-10-17/source/transport-store.cjs` | 3603 | `9c8c47f22f3042367cf024e317d7b12b6ab7533d2e9b24f3e22fdea7154960b8` |
| `research/m31-native-tree-state1000-2026-10-17/source/science-config.json` | 8365 | `476f0be0d76748087189b07d22a21da4770295f7a5f3d2981971c8362fd2020c` |
| `research/m31-native-tree-state1000-2026-10-17/source/storage-bound.py` | 6205 | `64cdab6db7e98290df981e6ff27b8599401c1495ceb1d3326793edfc6c7f81ec` |
| `research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs` | 16262 | `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs` | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs` | 14840 | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs` | 898 | `f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302` |
