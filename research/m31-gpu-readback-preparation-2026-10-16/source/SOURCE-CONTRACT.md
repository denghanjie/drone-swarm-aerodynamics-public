# Static-only GPU readback source contract

This isolated package prepares a distinct question: actual GPU-written buffer → map → copy into newly owned ordinary heap bytes while mapped → unmap/destroy → one automation result → persisted raw bytes → later independent exact comparison. It is not an operational result.

Preparation began at the observed clock reading **2026-10-15 22:59:55 UTC**, before the original **2026-10-15 23:00 UTC** launch cutoff. Parent permission to finish static preparation afterward does not allocate execution or extend the cutoff. No host wrapper is included. No browser, GPU, server, network, shader compilation, persistence trial or closure trial was launched.

## Files and isolation

`browser.html` loads the adjacent page definition; `gpu-readback-page.js` only defines `window.runSyntheticGPUReadback`. A page-realm latch rejects a second invocation; preventing reloads, new realms, retries and extra calls remains a future external responsibility. `fixture.wgsl` exactly matches the embedded shader and has not been compiled/run.

`validation.cjs` is pure: no I/O, browser, network, hashing or expected-output generation. `generate-fixture.cjs` derives static fixture artifacts using BigInt and manual byte extraction; it never imports/evaluates the page/shader. `validation.test.cjs` imports only the validator and Node file/pure-data primitives, using handcrafted reports and static text/binary reads. `expected.bin`, `initial-sentinels.bin` and `FIXTURE.json` are expectations, never observations. Receipts/inventory bind delivered static bytes only.

The frozen published control-channel source at `research/m31-control-channel-2026-10-16` was consulted only as design reference. No frozen campaign was edited, imported, executed or revived. No aerodynamic data, scientific qualification, historical-cause explanation or performance claim is present.

## Fixed fixture

ID `m31-u32-readback-128-v1`: 32 uint32 words/128 bytes, prefix words0..3, active words4..20, suffix words21..31. Workgroup size8 ×3 groups launches24 lanes; only i<17 writes. Initialize each word j with `0xD15EA5E5 XOR ((j * 0x01010101) mod 2^32)`. Active output is `word[4+i] = ((((0x9E3779B9 * (i+1)) mod 2^32) XOR 0xA5A5A5A5) + 0x7F4A7C15) mod 2^32`; XOR precedes final addition. Guards remain untouched. The page computes initial sentinels only, never expected active output.

Initialization is explicit little-endian via DataView; the reference uses manual extraction at bit shifts0/8/16/24. Exact matching assumes little-endian uint32 buffer representation. Actual mapped bytes must be preserved raw: no swapping, regeneration or normalization after readback.

Initial128B SHA-256: `944fbd39dc3fa2a2b8c9a2eef1c9c02b812911f4831b22c6c4e17cfe6a770e3a`.
Expected128B SHA-256: `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951`.

The producer independently derived these using BigInt/manual bytes; hashes agree with the separate reviewer's fixture in `../review`. Agreement between expectations is not GPU evidence.

## Proposed lifetime and error behavior

The source requires secure context/WebGPU, requests one adapter, and proceeds only when `adapter.info.isFallbackAdapter` is Boolean false. True/unavailable (including missing/throwing getter) fails before device request. No identifying adapter strings are collected. This is API-reported nonfallback admission, not hardware attestation.

It would request one device; admit default limits; push out-of-memory/internal/validation scopes; create one128B STORAGE/COPY_SRC/COPY_DST buffer and one128B COPY_DST/MAP_READ buffer; initialize; observe compilation messages; create one pipeline; encode one dispatch/copy; submit once; and map once.

While mapped, it copies the raw128B range into `new Uint8Array(128)`. It then unmaps, observes mapped-range detachment, destroys both buffers, pops scopes **before deliberate device destruction**, destroys the device, observes expected destroyed loss, and only then makes the plain byte array with `Array.from(owned)`. Successfully copied/released raw bytes are preserved even when a later scope/device condition fails. No expected-byte substitution occurs.

Lengths, backing-buffer inequality, counts, events, adapter status, scope results and loss observations are all **page self-report**. Schema consistency is not independent proof of GPU execution, ownership transitions or closure. Empty compilation messages or successful pipeline creation alone do not establish device health. GPUPipelineError reasons reduce to validation/internal/other; arbitrary API exception text is excluded. A null scope result after loss cannot establish success: candidate requires no unexpected loss, no observed pre-destroy loss, scopes settled before deliberate destruction, and separate expected destroyed loss. mapAsync certifies mapped-buffer availability, not unrelated queue/device completion.

Static API review used cached primary material the cached primary HTML identified by its recorded SHA256 and inherited `API-EVIDENCE.md`/`api-evidence.json` under `research/m31-browser-receiver-2026-10-16`. No fresh network fetch occurred.

## Bounds and exact assumptions

Work guard8,000ms and cleanup deadline10,000ms are browser-local elapsed from entry, **not execution allocations**. Cleanup is not an additional10seconds. Pending flags clear on underlying fulfillment/rejection; Promise.race timeout does not cancel. Rejections are observed even at an already-expired deadline. Sealing prevents late callback mutation; a late device receives best-effort destroy without claiming observed closure. Final elapsed/deadline is checked before candidate status.

JavaScript timers are cooperative; synchronous calls, browser/GPU scheduling and transport may outlast them. A future host must own and externally terminate/observe its browser/processes under a separately authorized whole-lifecycle limit. Its evaluate timeout must exceed page cleanup; the old10s control-channel host timeout must not be blindly copied. No host/supervisor is delivered here.

Each operation counter is capped at one. Events≤64, failures≤16, uncaptured errors≤8, compilation messages≤64; overflows fail. Failure codes are fixed. Partial creation uses separate cleanup flags; early failures, unsettled operations, mapping/loss/scope/cleanup failures remain failures.

Validator inputs must be ordinary deserialized records/dense plain arrays, not executable Proxy objects or modified built-ins. Exact own enumerable data keys are required (array length excepted); custom prototypes, accessors, symbols/extras, holes, invalid bytes, NaN/Infinity, floats and negative zero are rejected before byte conversion. A future host must bound transport/JSON size before parsing; field limits cannot undo parser allocations.

Candidate requires fixed layout, all counters1, exact normal event order, clean scopes/loss, API nonfallback admission, release observations, no pending work and final elapsed<10,000ms. Failed reports retain bounded branch-aware structure/failure reasons; elapsed≤60,000ms and observed lengths≤4096 are representation limits, not runtime authorizations. Browser times imply no cross-clock relationship or performance result.

The proposed `page-origin` is exactly `http://127.0.0.1:8876`; validator admits that label for candidates. No server/port is allocated. A changed origin requires source/contract changes and new hashes before a separately allocated run.

## Evidence boundary

Validator output is `candidateByPageSelfReport`, checked raw byte values when present, and `independentPersistenceVerified:false`. Wrong active/guard bytes or stale sentinels can be structurally valid: content correctness must be checked separately. Failed raw bytes may be retained as failure evidence.

Parent protocol still needs separately allocated host/supervisor execution, one automation result, validation before coercion, an exact persisted raw128B artifact, closure evidence and source/path/hash binding. After closure, an independent reviewer must reread that exact disk artifact and compare full length/all bytes against the independent fixture. In-memory equality, producer hashes, returned metadata, self-report and static tests are insufficient. All prefix/active/suffix bytes must match; no repair/overwrite is permitted. This package remains static, unallocated preparation.
