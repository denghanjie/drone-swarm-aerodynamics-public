# Candidate-author source cross-review

Reviewed on 2026-10-17, closed before 04:37 UTC. Scope: final independently authored `source/check.py` and `source/run.py`, their integration with the frozen decoder, the candidate/layout contracts, and `PROTOCOL.md`. This is a text and byte-identity review only. The reviewer executed no checker, supervisor, candidate, codec, producer, browser, reference, import, syntax check or test. Standard-library file reads and hashes were used to identify the reviewed bytes.

**Disposition: no source-level blocker found for the single, separately gated saved-data qualification.** This is not evidence that execution will finish within its allocation or that any reconstruction/size target has passed. The parent still owns final packaging, source review receipt, authorization, exact publication verification, launch, and external process-exit observation.

## Reviewed identities

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `source/check.py` | 28,351 | `9835d12054ad51cfdaa3530f3019d4745466b30c2bdf421e38701a0344aa716c` |
| `source/run.py` | 12,724 | `ac542c4659879503b434456c3f295d301539d8be2592857280f8817016b066f2` |
| `source/layout.cjs` | 7,545 | `310fce3d5f72abcdd1493cff487ae9c312027ec65f5e253fb0144dd50fb81c8e` |
| `source/candidate.cjs` | 12,802 | `7a7d592163a6574220f85307a9869f44125bd65fe318682dd7b61814d7e25b1d` |
| `source/transport.cjs` | 9,829 | `0dde5d59389ad13f5bdffee498533faf0585391eed40a99bb39546015fe2295b` |

The checker pins the prior pure Python decoder `research/m31-native-tree-browser-probe-2026-10-17/source/compact-check.py` to SHA-256 `87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee`. Its `Resolver` implementation was read for interface, type/word reconstruction, cache preservation and evidence-file inventory compatibility. Its scientific tree-validation routines are not called by the new checker.

## Checker and layout compatibility

- `input_records` fixes the three failed-probe anchor hashes and source commit/manifest, then reconstructs precisely the 126 saved rows followed by the 30 durable native journal rows. Exact typed row equality prevents an index/origin/sequence substitution. The input-manifest set must equal the complete anchor/descriptor/reachable-shard closure; unreferenced failed-append shards cannot become fixtures.
- A source descriptor's actual field set determines tree presence. Absence requires a null output pin and zero new bytes. Present null requires a real tree-only output descriptor decoding to null. Object trees require complete comparison. The candidate's roundtrip flag is required but does not establish the independent comparison.
- `TransportSupport` supplies the exact interface required by the frozen `Resolver`. The new reader uses the new package prefix and requires one `tree` field. Its full descriptor checks retain binary/element/depth/count limits and reject malformed/trailing data. All original inputs, including unchanged non-tree native fields, remain pinned and are rehashed even though the checker only decodes fields needed by this representation experiment.
- Exact base comparison preserves all original compact-tree non-receiver properties, including schema, nodes, bound words, members, canonical IDs, complete leaf dictionary, counters and status flags. Receiver, leaf-reference and gathered values are compared per original row; no other native arm supplies a replacement witness.
- Cull offsets bind complete ordered cull segments. Integer division/remainder decodes `node*6 + axis*2 + side` with the agreed side mapping. The checker checks node bounds, traversal order, exact cull count and every reconstructed cull key/value against the original. Difference words remain strings; no floating conversion or predicate recomputation manufactures them.
- Old runs and new runs are decoded independently of the JavaScript implementation. Endpoint arithmetic uses exclusive Python ranges and requires a gap between successive canonical runs. Bounds, strict source ordering, cardinality, and canonical representation choice are checked. Bitmap decoding uses least-significant set bits in each word, preserving ascending source order across words; high bits outside n are rejected.
- The independent byte-cost formulas match the pinned transport: literal `59+4*count`, runs `56+8*runCount`, bitmap `58+8*ceil(n/64)`, with the agreed tie priority. The checker derives run count from reconstructed actual values rather than trusting the candidate's cost calculation.
- `exact_equal` distinguishes scalar types and preserves floating signed zero by binary64 packing. The frozen reader retains 16-hex word strings verbatim; finite integral scalar numbers become integers consistently on both sides, while negative zero remains a float. Object key order is outside the stated equivalence relation, and all sequence order remains inside it.
- Both target records are fixed to browser journal sequences `[60,63]`. The checker recomputes each new/original tree-stream byte count from saved descriptors and applies the exact half-size gate to both. Candidate target rows must match the independently constructed rows. All 156 inputs are compared; the candidate accumulates all size rows before a ratio-only failure becomes terminal.
- The exact new evidence-file closure equals `new_reader.seen`. `Resolver.clear()` clears its value cache but retains `seen`, so this comparison covers every descriptor/shard across all 156 rows and rejects extra/unreferenced output evidence. `verify_preserved()` rechecks the seen pins before closure.

## Fixed controls and outcome scope

The source fixes the eight candidate control IDs/order and requires each `passed` value to be true. It additionally executes its own one positive layout control and sixteen individually named corruptions, checking the exact expected rejection reason rather than accepting any exception. Source tracing of those mutations agrees with the intended branch: representation cost, tail padding, offset endpoints/order, cull code/word/order, receiver order, gather order/count, dictionary reference, unknown field, unchanged base word, run overlap, bitmap width and boolean ID.

The positive fixture includes all three gathered encodings and a literal negative-zero word. Neither fixture construction nor the new checker imports a scientific producer or performs a numerical query. The checker reports `scientificValidated:false`, limits success to layout reconstruction, and reports logical tree bytes separately from descriptor/physical evidence totals. These labels correctly exclude a complete-browser fit, numerical validation and timing/speed claims.

## Supervisor integration and fixed resources

- `run.py` checks the exact enabled configuration and authorization fields, the fixed absolute cutoff, complete source/input/import closure, pinned Node/Python identities and the full publication receipt. It requires at least 300 seconds remaining both before source-gate work and immediately before creating the fresh attempt marker. Interpreter setup counts toward its unextended monotonic total deadline.
- The stage sequence is exactly candidate then checker. Each direct child receives the live token, stage identity, 120,000 ms budget and inherited monotonic deadlines. The checker additionally requires candidate exit zero and the supervisor-pinned completed candidate output. The publication time must predate the running attempt in the stage checks.
- Results and private directories must be fresh, and private storage must be outside the repository. Evidence is fixed at 56 MiB, private at 4 MiB, other public outputs at 2 MiB, and finalization allowance at 2 MiB inside the 64 MiB combined budget. Aggregate accounting additionally reserves closure space conservatively. Per-file size remains 32 MiB; one-MiB shards and two-MiB descriptor/index limits are enforced by the writer/decoder/checker paths.
- The supervisor rejects output symlinks, polls disk/time limits, applies per-child CPU/file-size limits, and requires child exit zero plus complete/passed/source bindings. It rehashes all source/input pins and preserves prior stage outputs before and after stages and during finalization. The checker only adds its exclusive report.
- Failed child time remains part of stage elapsed time. The supervisor kills and reaps its owned direct child on failure. There is no descendant-termination or memory-cap claim, and reviewed stages contain no child-spawn path. Polling disk accounting is correctly described as a monitor, not an atomic aggregate operating-system quota.
- Any mismatch, failed target/control, timeout, cap or preservation failure prevents completed status. There is no retry loop or path to reuse an existing results directory. Report timestamps are explicitly pre-final-report; a post-write deadline check and the parent's observed exit are still required. `supervisorExitVerified:false` avoids self-certifying a later process exit.

## Review limits and closure

This review cannot predict cold decode/encode/fsync performance, resource consumption, or the single attempt's result. Shared use of the old transport format and frozen Python reader limits decoder independence; the new cull/gather reconstruction and comparisons remain separately authored. The work preserves an exposed witness and does not establish that the witness is scientifically correct.

The older failed browser experiment remains unchanged. Passing this narrower saved-data qualification would not rescue that attempt, establish all 16 stages/48 native calls, demonstrate the original 160 MiB browser evidence budget fits, or permit new seeds, a new scientific run, a retry or any cap increase. No source edit was made as part of this final cross-review.
