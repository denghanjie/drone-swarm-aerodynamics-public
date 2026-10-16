# Browser source handoff (source only)

No browser, scientific import, fixture/control evaluation, generation, query, timing, input/output-data read or numerical checker ran while producing this directory. Validation is text inspection, exact source-byte comparison, bundle-slice verification and JavaScript parser checks. Scientific computation first becomes possible when the host explicitly calls the entry point after the final frozen/publication gates.

## Files to serve and freeze

* `index.html`: empty page, no animation or renderer, loads `/source/browser.js`; CSP permits same-origin fetch/script plus the verified Blob script.
* `browser.js`: combined nonexecuting definitions from `browser-loader.js` and `browser-harness.js`; loading it defines the entry point and loader, without executing scientific factories or constructing controls.
* `browser-bundle.js`: five CJS function factories containing the exact original bytes of reference, anchor, lean, kernel and controls.
* `source-bundle.json`: configuration payload for `config.sourceBundle`, including bundle hash and exact source byte ranges/hashes.
* `source/*.cjs`: exact copies for publication/provenance. Serving them individually is unnecessary.
* `adapt-source.py`: source-only reproduction of the adaptation from the old experiment driver. It reads source text/raw bytes and concatenates/transforms strings; it does not import scientific modules. Its current old-driver path is local to the preparation workspace and should be parameterized if retained as a public reproduction tool. Freeze the delivered generated artifacts regardless.

The loader fetches `/source/browser-bundle.js` as bounded bytes, checks the complete digest and every module-slice digest against the host-supplied frozen manifest, then creates a script Blob from that same verified buffer. The installed factories are executed only afterward through the fixed five-ID CommonJS cache. The local Buffer shim supports only zero/one-filled fresh Uint8Array allocation (up to 100,000,000 bytes) and buffer-local LE float64/unsigned BigInt64 methods, with default offset zero and Node-compatible write return offsets. It changes no native prototype or global Buffer/Math/performance object.

After source hashes pass, before even loading the verified script Blob, the loader executes exactly nine fixed adapter-control groups containing 56 named assertions. These are separate from the 48 unchanged scientific controls. The group IDs/counts are `zero-allocation` (4), `one-fill` (2), `fresh-storage` (4), `float64-le` (6), `float64-special` (6), `uint64-le` (9), `offset-rejection` (14), `value-rejection` (4), and `allocation-rejection` (7). They cover zero/one fill, fresh dedicated buffers and local methods, exact LE bytes and write return offsets for 1 and -0, NaN/infinity roundtrip, zero/pattern/max uint64 bytes and values, offset rejection, value-range rejection, and allocation/fill rejection. The largest successful allocation in these controls is 24 bytes. NaN payload preservation is not claimed.

`adapter-controls-spec.json` supplies the exact ordered group/check IDs and expected receipt fields for independent checking. The runtime receipt is `sourceReceipt.adapterControls`, schema `m31-browser-buffer-controls-v1`, with `expectedGroups:9`, `expectedChecks:56`, `executedGroups:9`, `executedChecks:56`, `beforeScientificFactories:true`, `groupIds`, `groups` and `pass:true` required for qualification. Every group must have its exact ordered checks, each `pass:true`, the declared `expectedChecks`, `errorClass:null` and group `pass:true`. Any mismatch prevents factory execution. The source receipt is installed before controls and retained in failure metadata. Success records factory order `kernel`, `anchor`, `reference`, `lean`, `controls` under `factoryExecutionIds` using exact `./name.cjs` IDs. Adapter test definitions have only been parsed and inspected during preparation; they have not run.

## Entry point and required configuration

Call exactly once per fresh process/page:

```javascript
const completion = await window.runBrowserExperiment(config, inputIndex);
```

`config` is the frozen browser experiment configuration plus the runtime's declared process identity and observed runtime receipt. Required fields:

* `schema: "m31-browser-screen-v1"`, `browserProcessId: "p0" | "p1" | "p2"` (the parser accepts any safe 1–64 character ID; controller fixes these three), and `sourceBundle` equal to the generated manifest.
* Original `methods:["L","F"]`, `permutations:["LF","FL"]`, `blocks:6`, `warmupCalls:6`, `measuredCalls:36`, `totalCalls:42`, `controls:48`, exact `controlIds`, `ownershipExtraBuilds:6`, exact `ownershipSequence`, `qualificationBuilds:6`, `qualificationSolves:6`, and original literal `controlSolvePolicy` string.
* `screen:{componentThreshold:4,spanLimit:256}`.
* Three ordered `cases` with safe unique `id`, `n:[1000,5000,5000]`, `seed:[261701,261702,261703]`, and `t:5`.
* `generation` retains `factoryVariant`, `filter`, `mode`, `search`, `expectedCourse` and other host-generation rules, with `duration:5`, `dt:.0025`, `frameEvery:.2`. The cadence is the parent's revised 26 frames at .2 seconds because unchanged simulation source rejects .25.
* `limits.candidateCooperativeSeconds:895`, `normalScientificBytes:536870912`, `scientificBytes:553648128`, `compressedSymbolsBytesPerBundle:67108864`.
* `runtimeEvidence`: the controller's actual Chrome/CDP/OS/runtime/pins/flags receipt. The page records this as externally supplied evidence and also records its own UA, platform, page visibility, secure-context/isolation flags, concurrency, clock/time origin and source-verification receipt. A page flag or reported version does not independently verify whole-installation identity.

The cooperative timer starts at entry and includes loader, controls, transfers, qualification, queries and persistence; it is not an external kill mechanism. The external supervisor must enforce 900 seconds, the declared sampled owned-Chrome-tree 2 GiB threshold, complete host/profile/output storage budgets, process ownership/closure, stop policy and cleanup reserve. This page makes no RSS-peak or process-closure claim. Native Chrome helpers/GPU processes remain the supervisor's responsibility even though all scientific arithmetic here is page JavaScript.

## Supplied input index and generation metadata

`inputIndex` has old-compatible `kind:"fresh-airflow-off-boids-states"`, `shape:["vehicle",17]`, `dtype:"float64le"`, and three ordered `cases`. Each case entry contains `{id,n,seed,t,path,bytes,sha256,generationPath,generationPin}`. The final state path is `inputs/${id}.f64`; `generationPath` and `generationPin.path` are both `generation/${id}.json`. `generationPin` is a normal `{path,bytes,sha256}` pin. The host retains the original index file/pin separately; the page records the SHA-256 of `JSON.stringify(encode(inputIndex))` without a newline, which is explicitly an object-serialization digest.

The supplied generation JSON retains the old record structure: `{id,n,seed,config,metrics,recording,initial,final,frames,poses,generationMs,initialMatches,complete}`. It must state `complete:true`, `initialMatches:true`, successful stop/failure metrics and recording `{cadence:.2,streamed:true}`. Final pin must match the index. Initial/final arrays contain all 17 float64 values per vehicle. There are exactly 26 frame pins at times `i/5`, each width `1+7*n` doubles, and a concatenated poses pin with matching width/frame count. The page fetches and hashes each pin, verifies frame/pose bytes and final pose/full-state agreement, and reconstructs little-endian full states without decimal JSON conversion. No simulation code is imported into the page and no failed case is replaced.

Only root-relative `/inputs/<safe-basename>` and `/generation/<safe-basename>` fetches are used. The host must whitelist exact manifest paths and response bytes, not expose arbitrary filesystem paths. Each fetched artifact is capped at 128 MiB before concatenation/hash. Generation metadata input JSON does not carry source instructions; the page treats it only as schema-checked data.

## Collector binding

Before entry, expose:

```javascript
window.__saveChunk = async (rel, base64, final, emergency) => { /* host-owned */ };
```

There is at most one awaited binding invocation in flight. The page sends no more than 3 MiB decoded bytes per invocation, hence no more than 4 MiB base64 characters. Files contain one or more chunks; empty files use one empty final chunk. `rel` is an old-compatible `results/<safe-basename>` path. The controller namespaces it to the current process's result directory. Every new path must be opened exclusively; append to its owned open file, never replace a completed artifact. Enforce chunk size, one active artifact, sequence/phase, declared process identity, per-file and aggregate byte/file/message caps independently in the host. Intermediate returns are not interpreted.

The final return must be `{path:rel,bytes,sha256,durable:true,exclusive:true,fsync:true,directoryFsync:true}` only after writing and file fsync/close, exclusive link/unlink publication, and parent-directory fsync, with the hash and length calculated by the collector over persisted bytes. The page verifies all flags and the receipt against its own digest. Saved persistence metadata says `directoryFsync:true` and `fsyncScope:"file content and parent directory after exclusive link/unlink publication"`, matching the inspected current host collector. This records completed fsync calls; it is not a general guarantee against all hardware/filesystem failures.

Ordinary writes are capped at 512 MiB; emergency failure records may use the additional 16 MiB. Host hard caps include partial files and bytes even when the page did not receive an acknowledgement. Page counters are acknowledged bytes, not proof of exact host totals after transport failure. Scientific source guards are unchanged; browser guard callbacks enforce cooperative time while external monitoring supplies resource observation. Writes can finish after a cooperative guard boundary so raw/error records have a chance to persist; final success is checked against the cooperative deadline again.

## Scientific schedule and artifacts

The driver retains 48 controls, their admitted-and-descending solve policy, six cross-call ownership builds, six full qualification builds/solves, omission-tensor audit, six warmup calls and 36 measured calls in the old six-block counterbalanced schedule. Every process uses the same once-generated three inputs. Repetitions within a process are dependent observations. The three processes remain declared prospective repetitions, not retries or independent swarm populations.

Comparison coverage remains symbols, offsets, source IDs, coefficients/scaling, prepared inputs, nominal/S0, admission, full graph/dependencies, certificate, symbol counts, model geometry, ordinary bound, assembly/ownership, solution values/work/termination/residual and full solution object; same-method repeated calls also compare screen and all geometry work. Input bytes and hashes are checked for mutation. Timing totals must be finite and strictly positive; all reported phase values must be finite. The fixed 128 clock reads are metadata only and never trigger adaptive resampling.

Full symbols are persisted as native `CompressionStream('gzip')` output with raw byte length/hash, then completely compared before release. Compressed bytes can differ from Node zlib level 6; independent checking must decompress and verify the raw tensor rather than requiring the same gzip bytes. Large tensors are never expanded into JSON number arrays. Literal symbol arrays are used only for the small fixed control/ownership cases. Binary typed-array payloads retain the old byte format on an admitted little-endian runtime.

Matrix hashing exactly concatenates offset bytes, source-ID bytes, K bytes, a bytes when present, then UTF-8 JSON.stringify(encode({input,admission,graph,symbolCounts,ordinaryLmax})) with no separator/newline, as in the old driver. Solution hashing retains the old encoded solution-record JSON ordering. Both use asynchronous native SHA-256; concatenations/hashes have a 128 MiB cap. JSON artifacts have a 16 MiB cap. Gzip output has a 64 MiB cap. These are explicit failure limits, not measured resource claims.

Each returned query's `call-NNN-raw.json` is persisted and acknowledged before comparison, additional checksum, input hashing or matrix/solution validation. Query exceptions get an emergency raw attempt record. Validation follows in `call-NNN.json`; mismatches attempt a full failure bundle. The raw file is not a pass result. Main evidence, controls, ownership, qualification bundles and failure records keep the old names/shapes with additive browser/runtime/transport fields.

Native `kernel.query().totalMs` and phase timers remain untouched. There is an explicit event-loop turn before every query and after each input case, and asynchronous persistence/hash/compression boundaries elsewhere; no await/event-loop yield is inserted inside a numerical query. All serialization/hash/compression/transport/validation costs are outside the query timer. `stageAccounting` records source loading, input fetch/decode, encoding, base64 encoding, SHA, gzip, acknowledged transport and explicit yield costs. These inclusive phase totals overlap detailed counters and must not be summed as disjoint timings. Persisted evidence counters stop before its own final persistence; completion metadata adds `accountingAtCompletion` after it.

Completion `{complete:true,...}` requires successful schedule, scientific checks, durable final evidence acknowledgement and final cooperative guard. It still does not imply external cleanup/resource qualification. Failure returns `{complete:false,failure,...}` and attempts `failure.json` and `partial-evidence.json`; failures of those writes are represented in returned metadata. Host failure/termination must retain its own evidence even if the page never returns.

## Content-file inspection log and static limits

The initial implementation extended the prior ten-file assessment by two existing content files: `research/m31-center-screen-2026-10-16/source/controls.cjs` and `research/m31-center-screen-2026-10-16/source/experiment.cjs`. The final interface review added `research/m31-browser-screen-2026-10-16/source/controller.cjs` and `research/m31-browser-screen-2026-10-16/source/generate.cjs`, both read as source only. The four numerical modules were already inspected. Other reads were generated scratch files or repeat byte reads of those same sources. No repository, host or supervisor file was edited by this subagent.

The inspected controller's source paths, process namespace, `generationPin`, base64 chunk bound, awaited binding receipts, and file+directory fsync flags match this interface. Parent should copy `index.html` as `source/browser.html` (or use the identical provided `browser.html` alias). One failure-retention issue was reported and then confirmed fixed in a targeted source reread: the controller now assigns `rec.pageResult=result` immediately after page.evaluate and before asserting result.complete, preserving an incomplete page's returned failure/source receipt. This review did not execute the controller, simulator, page, controls or any network request and does not establish process containment.

Static validation does not establish runtime API availability, actual CSP/Blob/Playwright interoperability, Control/nextUp equivalence in Chrome, completion within caps, Chrome output agreement, timing benefit or process containment. Those remain prospective gated checks. The parent must independently review this generated source and its host/checker integration before the frozen launch allocation.
