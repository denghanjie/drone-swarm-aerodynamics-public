# Candidate-author cross-review of independent infrastructure

Review scope: text-only review by the candidate/adapter author of the separately authored transport, host store, browser loader/controller, process supervisor and compact Python checker. This reviewer is independent of those implementations, but not of the compact producer format or native candidate. This document is not an independent review of the candidate itself. No candidate import, syntax check, test, scientific execution, browser, network or Git operation was used in this review.

## Findings requiring closure

1. **Saved-data control field mismatch — deterministic preflight failure.** `qualify-transport.cjs` emits each codec control as `{id,pass}`, while `validate-saved.py` initially required `c.get('passed') is True`. All six successful codec controls would still fail the consumer. Reported to both authors. The producer and consumer must use the same explicit field before source freeze.
2. **Startup journal prefix mismatch — deterministic saved-check failure.** The browser loader appends `source` and `factories` before invoking the driver, while the initial new checker expected the journal to start with twelve `wiring-control` records. Reported to the checker author. The expected prefix and actual source/Buffer/factory provenance checks must be integrated; dropping the startup records is not the repair.
3. **Optimized-array decode depth mismatch.** The initial Python resolver accepted a tag 8/9/10 optimized array at depth 64 whose scalar children occupy depth 65. The JavaScript encoder and decoder reject that shape. Reported to the checker author; the added `depth+1 <= 64` condition was observed in source. This aligns the declared bounded grammar; the ordinary scientific data does not approach that depth.

All three reported findings have now been corrected and the revised source inspected. This closes the identified source-level issues, subject to final author closure and the parent's complete freeze/publication/runtime gates. It is not an execution result.

## Compact proof review

The checker reconstructs deterministic bounds and topology using the frozen independent word-based helper. Its shared integer scale includes 2^-52. The positive predicate becomes `receiver <= node.min - (4 - 2^-52)` and uses `bisect_right`; the negative predicate becomes `receiver >= node.max + (4 - 2^-52)` and excludes only the strict prefix from `bisect_left`. These choices include both midpoint ties to the even word ±4. Signed-zero coordinate values coincide for predicate comparisons while actual endpoint words and saved cull differences are checked separately.

For every receiver, decoded actual gathered indices equal the selected dictionary leaf descendant mask and contain self. Culled descendant masks cannot intersect that gathered set, self or previous culls. Their union must cover every canonical index. Leaf/cull IDs are ordered. Ancestor unions reconstruct the actual visited nodes. At each visited node, the first-success predicate mask is compared with the recorded cull mask for H; H0 records no culls and gathers the entire canonical set. A fabricated deeper cull beneath an already qualifying ancestor cannot pass because that ancestor is visited and would require its own cull, which would violate the disjoint partition. Endpoint-comparison counters count remaining receiver masks before each ordered predicate, preserving the short circuit even for H0's ignored success.

The run/literal decoder enforces positive run lengths, range, increasing nonadjacent runs, canonical strict-shorter run selection, literal order and exact cardinality. Exact dictionary sequence uniqueness and complete reference use are checked. No N-by-N Fraction replay is introduced by the compact partition proof. The saved-data preflight still checks agreement with all frozen exhaustive certificates and reconstructs the full prior logical payload.

## Transport and persistence review

The encoder retains finite numeric words including negative zero, exact 16-digit word strings, ordinary strings, arrays, objects and explicit tags. Optimized word/u32/number arrays preserve the same logical values. A packed field crosses canonical 1 MiB chunk boundaries without padding; every nonfinal shard must be exactly 1 MiB. Descriptors retain field order, lengths and element counts. The decoders reject unknown tags, truncated blocks, trailing bytes, duplicate object keys and inconsistent element counts.

The host recomputes each shard hash, checks canonical base64 and actual byte length, and uses `Buffer.equals` before reusing an existing hash-addressed shard. No semantic-equality Boolean substitutes for that actual-byte check. The checker resolves hashes and full bytes before caching an equal stream, and separately verifies all previously read pins at closure. Its `jsonBytes` field is expressly a bounded source diagnostic; binary sizes, decoded elements and types are independently checked.

The host store charges additions before exclusive writes, fsyncs files and containing directories, and enforces the 160 MiB evidence partition, 64 MiB private allowance and 256 MiB aggregate with closure reserve. The outer supervisor independently scans the public/private partitions and per-file limits. Logical-record and buffer allowances do not assert an OS memory ceiling. Deduplication and repeated directory scans remain operational work within the prescribed wall allocation.

The append acknowledgment's complete transport timing includes the final descriptor/journal acknowledgment; host journal metrics necessarily describe the preceding prefix. Candidate stage and driver timing records now preserve `serializationMilliseconds` as well as total append, transfer and persistence measurements. Persistence is nested within transfer, and those intervals must not be added as disjoint costs.

## Bundle and process containment review

The browser loader verifies the bundle and source slices before installing module factories, runs the retained 56 Buffer assertions before scientific factories, uses a finite module allowlist and resolves the candidate's retained relative numerical imports to the pinned original modules. The factory process shim selects the registered wide course locally; it does not replace global process or Buffer state.

`run.py` requires the complete 960-second reservation before the fixed cutoff, matching stage caps, enabled source authorization, manifest/runtime/publication bindings and an exclusive fresh result directory. Saved validation is inside the shared overhead budget and must finish successfully before fresh browser execution. The saved-validation/browser guardian remains unreaped until explicit release, so failure cleanup can signal its owned process group without recycling a reaped leader PID. The browser controller forces its Chrome spawn into that owned group, binds the executable/profile/runtime and records the particular Chrome root's exit and close. Normal completion requires zero root exit/close codes. The outer supervisor remains independent of renderer responsiveness.

Controller failure attempts to append a plain failure object through a descriptor-only helper, which rejects it; its catch then records the failure in `browser.json` and leaves completion false. This is a retained failure-index path rather than a successful journal failure append. It does not create a false pass or bypass the external deadline, so it is not a launch blocker. Timeout likewise cannot pass. No all-helper exit or OS memory-cap guarantee is inferred.

No additional source-level blocker was identified in the reviewed transport/store/controller/group-supervisor logic. Runtime feasibility of the full evidence/derivative workload remains the fixed attempt's operational question, not something this source review establishes.

## Resolution log

- Optimized-array depth fix observed in `compact-check.py`: `s.need(depth+1 <= 64, 'stream-depth')` immediately before counting optimized scalar elements.
- Saved-control spelling fixed: the independent consumer now requires the exact six registered `{id,pass:true}` records in producer order.
- Startup prefix fixed: the checker now expects and resolves `source`/`factories`, verifies exact pinned bundle slices, the fixed 56 Buffer assertions, the local wide-factory shim and the actual 18-module execution order. That order was traced through the byte-pinned source require statements and matches the browser loader.
- Query/common/step/driver timing domains and acknowledgment-to-journal prefix bindings were inspected after the timing fields were added. Driver startup records are correctly excluded from driver-owned append summaries.
- Rechecked initial/controller/step compatibility: the unchanged StageAudit.step accepts general N; case-local initial states, four stage IDs, stable IDs, commands and endpoint fields bind to the derived compatibility view. The exact counts are 44,256 primary drone-stage derivatives plus six successful wiring derivatives, or 44,262 derivatives / 752,454 words total. No further integration mismatch was identified in these paths.

## Reviewed byte checkpoint

These are the inspected source bytes; later edits require parent reconciliation with this review.

| File | SHA-256 |
| --- | --- |
| `source/transport.cjs` | `ad5cc73b6bac321eb78deea82602d67fc8452cc204cc2e1d3b5a7ed84bef7e57` |
| `source/transport-store.cjs` | `ab9683bddbd57d5f68764c3993293ba62d4775922055e872ab3caa852f55f8ba` |
| `source/controller.cjs` | `89c7bb8cbb4981ebf00431eea480bc3c2a86a99aafbd2945d399070a178beaa9` |
| `source/run.py` | `7ed098bb88037d46874880483e36100bf1aef04d44aaf565c27ef5c48231840a` |
| `source/group-runner.py` | `5b4e22611b30c44e6a4a6026318d51d065855bfb40cd13143f4bdb78fea2c33a` |
| `source/browser.js` | `05e947a8a10a0a5d381b152729c1380b014285afa292e5c1923f90639463bcbd` |
| `source/build-bundle.py` | `30daed4db9aa5f8a5b3adabc1782375edbe7144c3ae6d8ed03e8ddb9f653868a` |
| `source/compact-check.py` | `87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee` |
| `source/check.py` | `6db03b1880711af2aaedfe12c246d9c8bc73b55f58ec06e4ad71db3c6e9b7d32` |
| `source/reference.py` | `d7255cc839c79ff0cf05259d40ed5bd07f35003ab797d610898802e65fa1f691` |
| `source/validate-saved.py` | `f98b2c42aa538f59f988e27a128315ed612126a89368b2d127a5b152ba5e7d99` |
| `source/qualify-transport.cjs` | `b26bcc099d7f45efbb8f9820d035132b83ae1a8ee7db23eda461553c8c982b22` |

## Final audit-source reconciliation

The audit author closed four files at 04:05:27 UTC. Their final byte hashes were checked against the supplied closure pins, their reported source changes were inspected read-only, and the four corresponding hash-table entries above now identify those final bytes. No source code was changed by this reconciliation.

- `check.py` now requires the insertion order of actual native journal results to equal the registered method order, rather than checking only recorded order metadata and references. It obtains saved-validation and reference prerequisites from the supervisor's completed-output pins, requires exactly four reference records and the expected reference schema, and preserves the four resolved reference sidecar pins through closure. These changes match the driver journal and supervisor output-record shapes.
- `reference.py` independently checks the stage execution context, fixed 15/600/180-second budget environment, fixed envelope, live child allocation and private-directory identity. The supervisor publishes those fields before starting each child. Publication must precede the attempt. Manifest, publication, prerequisite output and browser-journal pins are retained and rehashed; the actual stage descriptor/shards are also rechecked. The completed-output path is derived from the fixed prerequisite stage name and validated against the supervisor's recorded byte length/hash.
- `compact-check.py` adds strict integer record-level bounds and a 4096-byte UTF-8 field-key bound. They agree with the producer descriptor format, including the valid empty-record envelope, and do not change tree reconstruction or predicate-mask arithmetic.
- `validate-saved.py` preserves the saved transport index's observed bytes/hash for closure verification. Its compact corruption checks catch only the expected independent `InvalidRecord` with the exact registered rejection reason, so unrelated exceptions cannot count as successful negative controls.

No new source-level blocker or mismatch was found in these final deltas. The original source-only scope and claim limits remain: this reconciliation supplies no runtime feasibility, scientific result, syntax-test receipt or launch authorization.
