# Complete prospective record contract

The source/result-contract.json fixes validation recipes, resource limits and scientific decisions. The following exact wire interface is adopted from the independently authored runner interface before source freeze. No execution is implied by this document.

# Runner wire contract

Source-preparation contract, 2026-10-17. No scientific execution is represented by this document. Candidate CLI is `source/run.cjs PACKAGE_ROOT`. All paths in records are repository-relative POSIX paths. The permanent attempt belongs exclusively to the supervisor.

## Encoding and identities

Every runner JSON artifact uses recursive lexicographic object-key ordering, ordinary JSON string escaping, compact separators and one trailing LF. Arrays retain order. Diagnostic finite numbers retain native JSON numeric values; negative zero is `{ "negativeZero": true }`; nonfinite numbers are `{ "nonfinite": "nan" | "+infinity" | "-infinity" }`; undefined is `{ "undefined": true }`. These markers never replace scientific state words. No duplicate keys, raw NaN or raw Infinity are written. Hashes and byte lengths bind the saved UTF-8 bytes directly; no cross-language float reserialization is required.

Inputs have exactly `{drones:[{id,state}]}`. Each state is 17 lowercase 16-hex binary64 words. Generated IDs are the unchanged generator array indices 0 through 63. Full captures copy and freeze each word synchronously inside the existing progress callback; pose frames copy their supplied 7N words synchronously inside frameSink. Input SHA256 hashes the inherited canonical encoder's output for `{domain:"m31-moving-admission/input/v1",id,input}` (no added newline).

The shared identity fields are `configId`, `configSha256`, `sourceManifestSha256`, `sourceCommit`, and `runtime`. Runtime has exactly `{node,platform,arch,executableSha256}`. Source commit equals the supervisor-provided 40-lowercase-hex commit and permanent attempt field. `sourceSha256` maps exactly the twelve local scientific files (methods, adapter, canonical, rational, interval, boxes, tree, pair-prepared, loads, zero-filter, binary64-interval, spec), local run.cjs and config.json, and the seven generator closure files to their SHA256s. No absolute paths occur in this map. `constants` is the unchanged adapter.constantBits object.

## Method records

The four control IDs are config order: positive, distant-zero, raw-force, order-incompatible. Scheduled IDs are run-a-t0, run-a-t5, run-a-t10, run-b-t0, run-b-t5, run-b-t10.

Each record has exactly `{id,kind,input,method,error}`, where kind is `control` or `scheduled`. Normal filtered outcomes, including scientific refusals, have complete unchanged `method` and null `error`. A caught programming exception has null method and `{name,message}` error and terminates the allocation after preservation.

Each record descriptor has exactly `{id,kind,path,bytes,sha256,inputSha256,capture,call}`. Controls use capture `{type:"control",controlIndex}`. Scheduled records use `{type:"generation-slot",runId,generationSha256,slotIndex,t}`. Call has `{sequence,startNs,endNs,totalNs,phases}`: sequence is one-based across actual method invocations; startNs and endNs are process.hrtime.bigint offsets from the runner's process-local origin; totalNs=endNs-startNs. Each phase is `{name,offsetNs}`, offset from call start. All ns values are nonnegative decimal integer strings. Phases may be a proper prefix of prepared, spatial, assembled on preparation refusal or error. JSON serialization is outside call timing.

## Generation records

Generation record fields are exactly `schema,configId,configSha256,sourceManifestSha256,sourceCommit,runtime,id,seed,requested,generatorOptions,generatorSource,initial,final,frames,slots,terminal,callbacks,runSummary,error`. Schema is `m31-moving-admission-generation-v1`. Requested equals config.generation. generatorOptions has exactly `seed,count,duration,dt,mode,search,filter,record,frameEvery`, the actual accepted scalar run arguments. Callback functions are supplied separately. generatorSource has `{entry,environment,sha256}`: entry is `outputs/milestone-31-source/sim.cjs`; environment is `{FLOCK_FACTORY_VARIANT:"wide"}`; sha256 maps exactly the seven generator closure paths. The environment is set before simulator import.

Initial and final are full-word input objects copied from returned initial/final arrays. On a generator programming exception, both are null and runSummary is null; captured frames, slots and callbacks remain saved. Initial capture provenance remains explicitly in reached slot0. Frames are `{t,words}` arrays in callback order, with each words array length 7N. Slots are exactly three ordered `{t,status,input,reason}` entries: reached has actual captured input and null reason; missing has null input, status `not-reached`, and the exact nonempty simulator stopReason (or `generator-error` following an exception). Terminal is null, or `{t,input,reason}` for the sole off-schedule terminal callback; reason is the exact stopReason and terminal is never queried. Callbacks are the copied diagnostic progress objects `{t,passed,stopReason,wallMs}` in actual order. runSummary is the complete returned simulator object excluding initial, final and frames, recursively diagnostically encoded. Errors are null or `{name,message}`.

Generation descriptor has exactly `{id,path,bytes,sha256,seed,status,frameCount,reachedTimes,missingTimes,error}`; status is `completed` or `error`. A normal early simulator stop is completed generation with explicit missing slots, not a runner exception. Both generation files are closed and fsynced before the `generations-ready` event and before any generated method invocation.

## Index and failures

Index schema is `m31-moving-admission-index-v1`. Exact fields are `schema,configId,configSha256,sourceManifestSha256,sourceCommit,runtime,sourceSha256,constants,controls,generations,scheduled,completion,error`. Controls and generations are descriptor arrays in fixed config order (completed prefixes on runner failure). Scheduled always contains six ordered entries `{id,runId,t,status,reason,generationSha256,inputSha256,record}`.

Scheduled transitions: initial status `not-generated`, reason `kernel-not-completed`, all three binding fields null; a captured reached slot becomes `reached-not-evaluated`, reason `query-pending`, generationSha256/inputSha256 populated, record null; missing becomes `not-reached`, reason exact stopReason (or `generator-error`), generationSha256 populated and other bindings null; method success becomes `evaluated`, reason null and record descriptor populated; method programming error becomes `error`, reason `method-error` and failed record descriptor populated. Reached-but-unqueried failure entries retain `reached-not-evaluated` and `query-pending`; top-level completion/error explains interruption. No missing slot is replaced or scored.

Completion has exactly `{status,stage,methodCalls,generationRuns,reachedScheduled,missingScheduled}`. Status is `complete` or `failed`; successful stage is `complete`, failure stage is the interrupted stage string (`initialization`, `control:ID`, `generation:ID`, `generated-queries`, or `scheduled:ID`). methodCalls counts attempted method calls, generationRuns counts attempted simulator calls, reachedScheduled counts captured scheduled slots, and missingScheduled counts explicit not-reached slots. Error is null or `{name,message}`. One exclusive index is written at successful completion or in the catch path; it is never overwritten. If resource/I/O failure prevents its preservation, no success is claimed and supervisor closes the allocation.

## Journal

Exclusive journal `results/kernel-journal.jsonl`; each line has exactly `{schema,sequence,type,payload}` with schema `m31-moving-admission-journal-v1` and a one-based contiguous event sequence. It is append-only and fsynced after every event. Max line64KiB, total4MiB.

Successful event order is run-start; four method-start/method-complete pairs for controls; generation-start/generation-complete for run-a then run-b; generations-ready; for each of the six ordered slots either slot-not-reached or method-start/method-complete; run-complete. A programmer/resource/I/O failure preserves the available prefix and attempts a final run-failed event. No generations-ready exists before both completed generation descriptors.

Exact event payloads:

- run-start: `{configId,configSha256,sourceManifestSha256,sourceCommit,runtime,sourceSha256,constants}`.
- method-start: `{id,kind,sequence,inputSha256,capture}` (sequence is method sequence).
- method-complete: the complete record descriptor, including on method programming error if it can be saved.
- generation-start: `{id,seed,generatorOptions}`.
- generation-complete: the complete generation descriptor, including on generation programming error if it can be saved.
- generations-ready: `{ids:["run-a","run-b"],sha256:[runASha256,runBSha256]}`.
- slot-not-reached: the complete scheduled entry.
- run-complete: `{path,bytes,sha256,completion}`, pinning the already-closed index.
- run-failed: `{error,index,completion}`; index is null or `{path,bytes,sha256}`.

The ordinary fully reached success journal has27events. Missing slots replace a two-event method pair with one missing-slot event. No event timestamp purports to measure simulator or physical time. Timing origin is runner process-local monotonic time and is only descriptive.

## Containment

Kernel scientific files (controls/scenes/generation/index/journal) share192MiB, scenes each32MiB, generations each8MiB, index2MiB and journal4MiB. Attempts, guardian/supervision records and public/private logs consume the separate16MiB metadata/log budget. The supervisor enforces total scientific256MiB, checker64MiB, combined272MiB, process-group RSS/time and sole launch. Runner reserves index/journal capacity before science writes, and does exclusive file creation, fsync, synchronous boundary time/RSS checks, before/after manifest checks, exact fixed schedule/config gates and diagnostic serialization checks. Boundary checks are not substitutes for supervisor sampling or its hard deadline. No source development import, trajectory generation, probe, candidate call or checker evaluation is authorized by this contract.
