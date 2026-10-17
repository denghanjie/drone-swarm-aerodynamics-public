# Native tree browser probe implementation

This source package implements the fixed prospective procedure in `PROTOCOL.md`. Source preparation alone does not authorize execution. No candidate import, syntax check, test, scientific producer, browser, network call or Git operation was used to prepare the files described here. The author's checks were text reads, textual transformations/comparisons and byte hashes. Parent review, complete dependency/transport closure, a disabled then enabled source freeze and exact public verification remain prerequisites to a launch.

## Source ownership and immutable dependencies

- `source/native-tree.cjs` contains the prior qualified tree kernel in a private IIFE, followed by its prior native wrapper. It exports `query`, `encodeEvidence` and `limits`. The IIFE avoids an additional kernel file and avoids top-level name collisions. Its numerical imports remain the immutable fresh-transfer `anchor-kernel.cjs`, `lean-anchor.cjs` and `reference-excerpt.cjs`; its `./tree.cjs` is this package's compact collector variant.
- `source/tree.cjs` keeps the deterministic tree, endpoint predicates, DFS and actual gathered-array behavior. Only evidence representation changes.
- `source/compact-codec.cjs` imports no numerical kernel. It exports `encodeIndices`, `createLeafDictionary`, `compactLegacyTree` and `semanticDifference`. The saved-data preflight can use the same candidate-array encoder and dictionary interner without running any native query.
- `source/browser-adapter.cjs` preserves projection, nominal fixture load, load binding, load consumption and RK expressions; it injects F/H0/H evaluation and saves full native records separately.
- `source/browser-driver.cjs` retains the fixed wiring, controller and safety routines and runs the four registered fresh t=0 cases once each.
- `source/science-config.json` freezes the case IDs, counts, seeds, four method orders per case, one-step integration, reference scope, controls and timing interpretation.

The unchanged F is `../m31-native-fresh-transfer-2026-10-17/source/native-load.cjs` (SHA-256 `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1`). The baseline vendor kernel SHA-256 is `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8`; anchor is `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a`; lean anchor is `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96`; reference excerpt is `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e`. The bundle must pin their actual bytes and map the candidate's retained relative import paths explicitly. Old completed packages are not modified.

## Textual identity inventory

A text-only extraction of the embedded kernel is **exactly equal** to all 16,690 bytes of the prior tree kernel after reversing the single final `return {...}` back to `module.exports={...}`. That restored text has SHA-256 `42cb6deeb32e9b5bd633679d3ea58489940009a9f77f690a0368b6f22de2a971`. No numerical, require, guard, timer, eligibility, cap, source order, assembly or solver line inside that kernel changed.

A text-only reconstruction of the native wrapper is **exactly equal** to the prior 17,214-byte wrapper (SHA-256 `05d9fcb5aa9fc8d3f4812a14e469096f5c3d6110b18f7b164496df7e21dd530b`) after (1) replacing the embedded IIFE with its former `require('./kernel.cjs')` and (2) reversing only the new compact-tree serialization lines. Those serialization edits copy `leafDictionary`, preserve `leavesRef`, copy gathered `kind/data`, and allow null partial gathered/canonical-ID values. All input capture, admission, load construction/consumption, refusal mapping and query timing code matches the prior wrapper.

The following extracted function substrings (trailing separator whitespace removed) match the prior coupled adapter/driver exactly:

| Text region | SHA-256 |
| --- | --- |
| `project` | `8d9ddef00120d7147f50c66b84ee99b93300d00bdcf440c2ca1e9a474aef8c3b` |
| `nominalLoad` | `b459a40fe4f786c498db2bf61650772638135896508a7a61a67424115c128df9` |
| `bind` | `ea9b485159bbebe157a245a7c5e879e94e431087100dc2a85405a22054f1adc5` |
| `consume` | `88570da3a769be9e89c311cca0c8e362f1ce03e3abdf20d9e8da4c6bf67c64f8` |
| `wiringControls` | `81389096a8d563a2129fa7bef65dc5bca8f5cbcc4696e2abe5fcd41535bf210c` |
| Contiguous `control` and `safety` | `418afb7b8a2c4aeedb3ff966a3412abb5e099469511c26bbe9bf2a9526127faf` |

The RK scheduling wrapper now adds case identifiers and separate timers, but retains the original expressions `value+scale*k[i][j]` and `value+dt*(((k1[i][j]+2*k2[i][j])+2*k3[i][j])+k4[i][j])/6`, dt/2 intermediate stages, and endpoint projection. There is no new inner tree guard poll. Whole-scene fallback still delegates to the unchanged lean build. The immediate 2,000,000 positive-term guard remains before the original scaled-cap calculation.

## Compact coverage schema

`m31-native-center-tree-compact-v1` keeps the old mode, leaf capacity, eligibility/fallback, completion, N, canonical IDs, node list and exact counter fields. It adds `leafDictionary`, an ordered list of ordered visited-leaf-ID sequences. Each receiver is:

```text
{receiver, culled:[{node,axis,side,difference}], leavesRef, gathered:{kind,data}}
```

`side` remains `min-ge4` or `max-le-neg4`; serialized bounds and cull differences retain their exact 16-digit binary64 words. `gathered.kind` is `runs` with flat `[start,length,...]` data or `literal` with the actual indices. The encoder first scans every element of the actual sorted gathered array and requires increasing nonnegative safe integer indices. It chooses runs exactly when their element count is strictly less than the literal count; ties use literals. It never synthesizes `[0,N)` from an H0 label. The same gathered array is then returned to the unchanged classifier; compact evidence is produced before classification and does not replace its input.

Leaf dictionary lookup uses length and an FNV bucket only to locate candidates. Every reused entry also requires exact element-by-element sequence equality. A hash collision cannot alias different traces. New entries copy the actual visited leaves. All culls, including the first-success axis/side and actual rounded difference, remain recorded per receiver.

A private WeakMap holds each evidence object's dictionary interner; it is not a serialized claim. The ordinary candidate and local leaf arrays need not survive each receiver. Build/fallback completion and counters retain their previous meaning. If capture fails during a receiver, its partial receiver record may have null `gathered` or `leavesRef`, and the overall tree remains incomplete. Such a record is preserved as failure evidence and cannot qualify as complete coverage. Eligible successful records require full references and data. Ineligible fallback records have no tree nodes, receivers or dictionary entries.

`compactLegacyTree` converts a saved old logical tree certificate without invoking the kernel, retaining endpoint/difference values in their original numeric or word representation. Independent saved-data validation must compare reconstruction against the already saved original certificate, rather than using the producer's equality routine as the sole oracle.

## Native comparison and stage records

The browser API is `createDriver({physics,swarm,Grid,geometry,nativeF,nativeTree})`, then `run({config,append,guard,sha})`. `sha` accepts a UTF-8 string and returns lowercase SHA-256. `append(kind,body)` must return `{durable:true,recordPin:{path,bytes,sha256},sequence,serializationMilliseconds,transferMilliseconds,persistMilliseconds}` only after persistence. The driver is single use.

For each actual stage, projection happens once. The complete projected input word record is shared as data; each arm independently decodes it into new arrays inside its common timer. Actual post-query input words are compared to the original shared words, and `recordMeta.inputUnchanged` records the result. On mutation the actual submitted input snapshot is retained, the full returned native result is still saved, and the stage fails. Independently checking returned `raw` against the submitted words remains mandatory.

Each native result is actually encoded, then compared against the first actual arm result. `semanticDifference` excludes exactly these paths and compares unknown fields by default:

```text
method
 tree
 timing
 diagnostics.buildPhasesMs
 diagnostics.geometryWork.gatheredNonselfCandidates
 diagnostics.screen.orderedPairVisits
 diagnostics.screen.componentTests
```

The complete native object is appended flat as kind `native`, with `recordMeta:{caseId,stageId,queryOrderIndex,inputUnchanged}`, top-level `caseId` equal to stage ID, both semantic input SHA fields and `auditTiming`. Metadata is explicit and separate from the scientific semantic comparison. Transport may deduplicate only actual encoded identical bytes; the equality result alone never substitutes for evidence. A mismatch's divergent payload is persisted before the stage is refused. A native refusal, malformed response, failed equality or input mutation stops the run without replacing a case or issuing a repeat query.

Stage IDs are `<caseId>-step0-k1` through `k4`; step IDs are `<caseId>-step0`. Stage records retain the prior raw-before-projection, commands, projected input, all consumed loads, body-frame terms and 17-component derivative word records. They replace the embedded native body with `nativeRefs:[{method,recordPin}]`, ordered query timings and the explicit `semanticAgreement` result. The independent checker resolves every referenced arm. H's actual result is load-bound and consumed only after all three succeed and agree.

Initial, controller, step, safety and case-summary records retain complete actual data and case IDs. No full three-arm native array or repeated all-stage evidence is placed in a journal. Persistence failure propagates; it is not converted into a successful scientific failure record or retried. Counts and the first retained failure prevent a partial run from passing.

## Timing boundaries

`queryWallMs` begins before independent word decoding/input copying and ends after native return, its unchanged full load/ID/status consumption and the actual input-word preservation check. The native-owned copying and preparation, H/H0 tree build, construction sorts, traversal, candidate gather/source sort, compact capture, geometry, admission, solve, residual and load construction are inside. Nothing is subtracted for the collector. This is the registered audited query boundary for every arm.

`encodeWallMs`, `semanticCompareWallMs` and `appendWallMs` are separate wall measurements. The transport's own `serializationMilliseconds`, `transferMilliseconds` and `persistMilliseconds` are also retained. Native `encodeWallMs` is the word-evidence conversion; transport `serializationMilliseconds` is binary packing/hash/base64 CPU as defined by the transport owner. Stage and driver append acknowledgments contain the full transfer/persistence intervals, while the host journal necessarily stores the prefix before its final acknowledgment. These can be nested intervals and must not be added indiscriminately. All remain within the browser allocation; they are excluded equally from the primary query metric. The first result has no pairwise comparison, and its saved comparison time describes that actual trivial branch.

Stage common timings separately record projection, input-evidence preparation/hash work, and the H binding/derivative/derivative-evidence block. Step timings record RK combination, endpoint projection and endpoint evidence. Initializer, controller including its full record construction, and safety receive separate timers. Final H binding/derivative work is common work outside the query. Diagnostic browser/case wall times include all three arms and persistence; they are not production step time. The enclosing browser controller must report full operational wall time through final persistence/closure because the driver's final snapshot necessarily precedes its own final append.

No standalone tree-build phase is invented. Existing `diagnostics.buildPhasesMs.index` ends before tree construction. Existing `geometry` combines tree construction, gather/order/compact capture and actual geometry/classification. The full wrapper sum, not a selected phase, controls the fixed 0.80 H/F gate for each 5000 case. Report four H query times plus explicitly measured common work as an accounting boundary only.

## Fixed controls and claim limits

The science configuration fixes N64/1000/5000/5000 and the four seeds/method-order arrays from the protocol. There are exactly four complete actual stages per successful case and 48 primary queries for full completion. There is one controller update at t=0, one 0.0025-second coupled step per case, no off arm, warmup, repeated measurement or manufactured-motion rerun.

All 12 prior wiring controls are unchanged. The independent checker retains 14 fixed arithmetic fixtures. The ten prior coupled corruption controls are recorded as retained provenance, not rerun at possibly unavailable fresh t=0 witnesses. The saved-data preflight uses the original 42 tree cases/126 native records, their 15 corruption laws and focused codec/transport corruptions before exposing new seeds.

Independent fresh checks cover every native payload, full tree partition and every stage derivative and RK link. Fresh controller checks bind actual saved state, stable IDs, commands and elementary target arithmetic to the pinned source and complete actual neighbor records. This probe does not independently recompute neighbor membership or establish a fresh geometric exclusion margin at any N. Prior 64-drone exact membership checks remain provenance for the prior cases only.

Only the four actual N64 stage states receive exact load reference evaluation. Its maxDrones remains 180; 192-bit intervals, 128 bisections, 30,000 suffix-call limit and the four normalized 1e-8 load gates are unchanged. No N1000/N5000 reference accuracy claim follows native equivalence.

Transport and checker maintain their separately reviewed schema-derived bounds. The fixed 32 MiB file and 256 MiB aggregate limits are not a guarantee that every admitted 2,000,000-term native payload fits. Actual full evidence must fit the ledger and supervisor limits; a capacity failure is a terminal operational negative, not permission to omit data or tune the scientific cases. No OS memory ceiling or new inner-sort cooperative containment is claimed.

The transport owner's fixed disk ledger reserves 160 MiB for evidence directories, 64 MiB for private Chrome profile/log/scratch, 30 MiB for other public reference/check/journal/index files and 2 MiB for closure. Canonical shards are 1 MiB except each field's final shard; descriptor/journal files are capped at 2 MiB. Each logical record is bounded by 96 MiB encoded bytes, 256 MiB declared reconstructed JSON bytes, 16 million encoded nodes including object keys and depth 64. There is no compression. These are failure bounds; individual allowances do not override the total. See the transport owner's `SUPERVISION.md` for enforcement and allocation details.
