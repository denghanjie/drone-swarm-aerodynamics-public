# Static independent GPU-readback evidence contract

This is preparation for a distinct engineering question, archived under `research/m31-gpu-readback-preparation-2026-10-16`. It allocates no browser, GPU, network, diagnostic or saved-review invocation. The original overnight launch cutoff, `2026-10-15T23:00:00Z`, is unchanged. Earlier terminal campaigns remain immutable. Only pure reference calculations, inert tests and source syntax inspection were performed here. An independent checker of saved actual files is **not implemented or executed** by this package.

The proposed question is whether actual uint32 shader outputs can be copied from a mapped readback range into separately owned ordinary heap memory, then survive unmapping and resource destruction before a single Playwright return and exact, closed-file persistence. It is a byte-transfer and resource-lifetime question. No physical, aerodynamic, numerical-model, throughput, reliability, scaling or historical-failure claim follows from it.

## Agreed tiny fixture

Root adopted this fixture before implementation of the reference primitives. It has 32 uint32 words, exactly 128 bytes: four prefix sentinel words, 17 active words and 11 suffix sentinel words. Initially every word, including the active region, contains

`S(j) = 0xD15EA5E5 XOR ((j × 0x01010101) mod 2^32)`, for `j = 0…31`.

The proposed shader uses workgroup size 8 and three workgroups, yielding 24 invocations. Only `i < 17` writes. Its sole write is

`word[4+i] = ((((0x9E3779B9 × (i+1)) mod 2^32) XOR 0xA5A5A5A5) + 0x7F4A7C15) mod 2^32`.

Multiplication wraps before XOR; addition follows XOR and wraps independently. The seven extra lanes must return without touching padding. Every active expected word differs from its initialization. Prefix bytes 0–15 and suffix bytes 84–127 must remain unchanged; active bytes 16–83 must match the arithmetic reference. Checking only the 17 active words is insufficient.

Initialization uses explicit little-endian byte encoding, rather than relying on native typed-array byte order. The independently adopted expected file also uses explicit little-endian encoding. Compare the **actual raw 128 mapped bytes**, with no endian normalization after readback. A layout mismatch is a mismatch to this representation contract; do not select a different endianness after observing output.

| Fixture artifact | Bytes | SHA-256 |
|---|---:|---|
| `initial-sentinels.bin` | 128 | `944fbd39dc3fa2a2b8c9a2eef1c9c02b812911f4831b22c6c4e17cfe6a770e3a` |
| `expected.bin` | 128 | `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951` |

`FIXTURE.json` records all words, formulas, region sizes and exact expected bytes. The first three active words are `badd5831`, `1915d2ec`, `fe4e44a3`; the last is `a3552d01`. The independent Python reference uses arbitrary-precision arithmetic with explicit modular reduction and `struct.pack('<32I', ...)`. Inert tests cross-check it with repeated modular addition and manual byte extraction, rather than depending on native word-array encoding.

## What the predecessor establishes about design

The inspected predecessor source is `research/m31-control-channel-2026-10-16`. Its browser script creates an ordinary CPU heap array directly; its host strictly validates the actual decoded return, persists those actual values and separately compares them with a frozen fixture. It supplies a useful source pattern for separating actual returned bytes from expected bytes. It contains no GPU readback, map/unmap or device destruction operation, so its source cannot establish those new lifetime properties.

The predecessor's published producer records carry its own `browserContext`, phase, timing and closure claims. Its independent saved-review source rereads actual public payload files and compares named shared fields; it does not independently observe the earlier browser internals. The same distinction must remain explicit in a future GPU implementation. The predecessor sources were inspected and hashed here; no historical checker, producer or evidence was executed or modified.

## Required provenance and ownership boundaries

The expected output must stay outside the browser's output-production path. A future frozen page may construct only the distinct initial sentinels on the CPU; the shader is the sole intended writer of active output words. The expected fixture must never be copied into GPU output, the returned array or the output file to repair a failure. Freeze the shader, browser code, host validation/persistence code, reference and relevant runtime/source identities before any separately authorized invocation.

The proposed order is: initialize output with sentinels; submit the single compute and output-to-readback copy; await mapping; view the complete mapped range; allocate a **new** ordinary 128-byte heap buffer; copy mapped bytes into that separate buffer while the mapping is valid; unmap; destroy the readback/output buffers and the owned device; only then construct the returned primitive array from the owned copy. A view sharing the mapped ArrayBuffer, or a delayed conversion from that view after unmap, does not meet the ownership contract. Preserve no returned alias to mapped storage. Cleanup flags should identify each resource/API boundary, rather than a single ambiguous `destroyed` flag.

These are proposed source obligations, not proof that a driver physically released every resource at a particular instant. `mapAsync` resolution, `unmap`/`destroy` calls and phase timestamps are observations or assertions from the producer. Device-loss and validation-error observation must be armed before substantive GPU work; error scope, mapping rejection and device-loss outcomes remain separate. A returned phase array must not be promoted into an independent observer of its own producer.

Host observation can independently record that the sole `page.evaluate` call began, settled or failed, and what actual JSON it returned. The JSON is a representation of decoded automation values, not wire-protocol capture. The receiver must validate every returned byte before conversion, persist only those bytes through an exclusive write, retain any actual partial file, and record close separately from length or digest. A later separately authorized saved-file review must reread the closed file after external process closure, compare it byte-for-byte with the returned byte array and independent fixture, and bind exact file sizes/hashes to the final manifest. This package does not provide that operational reviewer.

## Separate evidence statements

| Statement | Supporting evidence and limit |
|---|---|
| Actual returned array equals actual persisted file | Independent comparison of retained decoded return and separately reread closed file. Neither a producer digest nor a reported `complete:true` flag substitutes for these bytes. |
| Active outputs and padding equal this fixture | Independent full-byte comparison with `expected.bin`, plus region comparisons. Padding failure identifies a mismatch, not its cause. |
| The mapped range was copied into different heap ownership before unmap | Frozen source inspection and producer's bounded phase/identity observations. Exact final bytes alone cannot establish the copy timing or object ownership. |
| The declared GPU path produced the output | Frozen source/runtime provenance, observed API outcomes and consistent retained bytes support a narrowly qualified engineering account. A known arithmetic fixture is forgeable by CPU computation and is not authenticated GPU execution or hardware attestation. |
| Owned software lifecycle closed | Actual external host completion and resource-ownership supervision would be required. Producer `destroyed`/`closed` flags and matching bytes do not independently prove closure. |

The pure tests deliberately create correct expected bytes on the CPU and show that byte comparison succeeds without any GPU operation. This is a limitation demonstration. Phase claims are not inputs to `compare_byte_evidence`; changing them cannot strengthen its byte-only conclusion. The separate ordinary-memory copy test illustrates ownership semantics in Python, not WebGPU detachment behavior.

## Allowed outcomes for a later separately scoped implementation

An unavailable API/adapter, shader or validation error, device loss, mapping rejection, automation rejection, malformed returned value, wrong bytes, padding mismatch, short write, close failure and incomplete observation must have distinct bounded dispositions. Preserve the last observed boundary; do not infer that later stages occurred. A timeout is not cancellation and leaves unobserved work unknown until cleanup is independently accounted. No retry, secondary extraction, expected-byte substitution or automatic successor is authorized here.

An honestly retained valid-shape wrong array may agree exactly with the actual persisted file. That is consistent evidence of a failed fixture transfer, not success. A file containing expected bytes when the retained return is wrong is an identity contradiction. Matching bytes alongside missing lifecycle, source or phase evidence establishes only the byte facts. An unchanged all-sentinel output fails this fixture, but cannot by itself prove that a dispatch was absent. Similarly, reversed words or damaged padding do not uniquely identify a shader, copy, serializer or persistence fault.

Any later complete positive engineering claim would require both independently matching bytes and a complete, consistent, separately reviewed provenance/lifecycle record. This package has no field that certifies GPU execution, record integrity, complete lifecycle or scientific success. Further operational source, a full saved-file checker, bounds, a new launch window and any invocation remain unallocated.

## Delivered primitive scope and static checks

`byte_primitives.py` contains only deterministic fixture generation, strict 128-byte array validation, bounded byte comparisons and comparison of a size/hash receipt with supplied actual bytes. It performs no filesystem, network, browser, GPU or process operation. It accepts at most 129 persisted bytes so a future bounded reader can detect one trailing byte; it never reads a file or certifies that it was closed. Its caller remains responsible for actual-file acquisition, source/manifest verification and lifecycle review.

Thirty-three inert cases passed, including unchanged initialization, reversed word endianness, an active-byte flip, prefix and last-suffix flips, empty/short/trailing files, replacement with expected bytes, forged expected digests, malformed values, and the producer-claim/byte-evidence distinction. Syntax was parsed without importing operational source. No more unit cases or operational runs are needed for this static handoff. Exact predecessor and delivery pins are in `STATIC-PREPARATION.json`.
