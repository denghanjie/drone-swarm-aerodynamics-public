# Future independent GPU saved-file review contract

This is **static source preparation only**. No full checker, host, browser, GPU or network operation has been invoked. The closed overnight cutoff is unchanged. This package creates no new allocation or launch/review window. The future checker must be source-reviewed and frozen with the future campaign before any separately authorized use.

The CLI would be `python3 review/check_saved_files.py ABSOLUTE_CAMPAIGN_DIRECTORY`. The campaign must use the repository's `research/campaign` layout. `check_saved_files.py`, `review_primitives.py` and unchanged independent `byte_primitives.py` must be installed together and pinned. Pure source imports have bytecode writes disabled. The entry records a monotonic start, reads **only config.json**, and performs strict admission before setting an alarm, reading runtime artifacts, reserving `review.lock` or creating result files.

Admission requires config version 1, scope `synthetic-gpu-readback-host`, `executionAllocated:true`, and four non-null whole-second UTC strings: `notBeforeUTC`, `stopNewLaunchUTC`, `reviewNotBeforeUTC`, `reviewStopNewLaunchUTC`. Each start must precede its end; the present time must lie in the half-open review interval. False allocation, truthy integers, null dates, malformed dates or closed windows cause a bounded refusal with no runtime artifact access or reservation. The integration package remains `executionAllocated:false` with all four dates null.

The seven exact integer limits are wall 60 s, worker 40 s, host evaluation 12 s, observer cleanup 58 s, combined retained bytes 8,388,608, sampled owned RSS 2,147,483,648 and trace events 2,048. The page's 10 s cleanup and host's 34 s substantive/3 s browser-close margins remain host source obligations. These numbers are an input-schema contract, not an allocation.

After successful future admission, one exclusive `review.lock` and fresh `review/results/` are required. Work stops at 25 s, output mutations are guarded before 29 s, and a 30 s alarm remains armed through exit, measured from entry with preflight time subtracted. Reused reservation or output directories are refused. The checker writes only `review/results/report.json`, `summary.json` and one stdout summary; it does not launch subprocesses or import operational source.

## Exact future inputs

`freeze.json` has `files` entries `{path,bytes,sha256}` using repository-relative contained paths. It must cover the new capture/observer/relay/admission/registry/host/validator/page/shader sources, `PROTOCOL.md`, config, runtime provenance, `expected.bin`, source fixture metadata and all three independent checker modules. Every source pin is reread and hashed. Expected128 bytes are independently regenerated; their SHA-256 is `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951`. The known preparation commit is background provenance, not a substitute for the future campaign's exact freeze and source identity.

`review/evidence-manifest.json` has kind `new-gpu-readback-public-evidence-manifest`, integer version 1, `sourceCommit`, `sourceFreezeSHA256` and `files:[{path,bytes,sha256}]`. Paths are campaign-relative. The exact allowlist is:

- `raw/trace.public.ndjson`; conditionally `raw/returned.json`, `raw/rejected-return.json`, `raw/received.bin`.
- `results/result.json`, `wrapper.json`, `budget.json`, `capture.json`, `sole-launch.lock`, `diagnostic-stdout.txt`, `diagnostic-stderr.txt`.
- `capture-launch.lock` and `publication/capture-output.json`, `observer-output.json`, `capture-execution.json`.

The manifest binds every actual file in flat raw/results directories, has at most 128 entries and an aggregate 8 MiB read cap before loading payloads. Directory scans stop at 128 entries. Its own bytes and later reviewer outputs are excluded from its pin list and added separately to accounting. No unknown public path or symlink is admitted.

The two publication summary files must be the exact retained one-line capture and observer stdout bytes. The external completion receipt has kind `actual-gpu-readback-capture-tool-completion`, source commit/freeze identities, `toolSessionCompleted:true`, actual capture exit code 0, actual full elapsed below 60 s, and whole-second UTC `captureStartedUTC`/`captureCompletedUTC`. Start must fall in the allocated diagnostic window; completion must be at or after start and no more than 60 s later. Cleanup may finish after the launch window closes. Integer-second wall timestamps and the independently recorded full elapsed are bounded separately, not falsely asserted to be exact equal durations.

The copied supervisors retain their legacy lifecycle kinds and accounting equations. Their candidate flags, actual exit receipts, named shared projections, exact stdout hashes, ownership/closure observations, sampled RSS and byte accounting are checked. Page resource flags cannot satisfy process-closure requirements. The reviewer does not independently reobserve old processes or read private traces; private byte counts and process observations remain identified source-receipt evidence.

## Host/page schema and honest failures

The negotiated host kind is `synthetic-gpu-readback-diagnostic`, fixture ID `m31-u32-readback-128-v1`, and stdout kind `synthetic-gpu-readback-worker-summary`. The host schema is specified in its retained `RESULT-SCHEMA.md`. Actual validated envelopes, including failed page reports, are saved in `raw/returned.json` with a complete exclusive-write/close receipt. Actual values, when present, alone supply `raw/received.bin`. A safe rejected-envelope projection does not preserve the original malformed object.

The five evidence groups are frozen source/allocation, final public manifest, actual bytes plus reported page phases, external lifecycle projections, and resource/output accounting. There is no synthetic implementation-assertion total. The checker independently validates the bounded page report and its consistency, strictly decodes integer byte values, rereads actual persisted bytes, and compares all 128 bytes with both the actual return and independent expectation. Prefix/suffix padding is included. JSON rejects duplicate keys, non-finite/overflow values and negative zero. Nested projection equality distinguishes booleans from integers.

| Complete observed outcome that can pass record consistency | Preserved limitation |
|---|---|
| Settled non-timeout evaluate rejection | No returned page stages or byte content are inferred. |
| Closed, bounded rejected-envelope projection | Original malformed object was not retained, so its invalidity cannot be independently reproduced. |
| Valid page failure without values | Actual failed envelope is retained and checked; no output bytes are invented. |
| Valid page failure with values | Exact closed file must equal actual returned values; page failure remains failure even when bytes match the fixture. |
| Valid candidate report with wrong bytes | Exact closed file must equal the wrong returned bytes; expected-match remains false. |

Incomplete source, instrumentation, externally observed lifecycle, timeout/deadline overrun, partial persistence, close failure or contradictory returned/file bytes cannot pass this aggregate integrity scope. Their evidence may still be retained by the producer; a rejected review does not by itself prove corruption or misconduct. This checker does not promise an integrity pass for every faithfully recorded failed write.

`finding.actualByteFacts` describes independent byte comparisons. `pageCandidateBySelfReport` and `pageAndBytesCandidateOnly` remain narrow page/report-plus-byte conditions; the latter can be true while a later source/lifecycle group fails. It is not a complete engineering result. `gpuExecutionIndependentlyAttested` and `processClosureIndependentlyReobserved` always remain false. CPU-generated expected bytes can satisfy byte comparison, and matching bytes cannot prove the map/copy/unmap/destroy sequence. Overall `recordIntegrityCandidate` additionally requires all five groups, and still awaits actual external reviewer exit 0, full elapsed under 30 s and complete summary/report binding. Self-reported `recordIntegrityVerified` and `qualified` remain false.

Accounting adds the diagnostic's exact public sizes and reported private bytes, later publication copies and external capture receipt, manifest, review lock/report/summary and one stdout summary copy. Any later external review-completion receipt must be added by that recorder. Successful checks cannot be manufactured by finalization. If reservation, hard deadline or output writes fail, a complete report is not guaranteed.

## Static validation and derivation

Inert tests import only the independent byte module and review primitives. They exercise synthetic page reports, allocation/window predicates, malformed JSON and fresh disposable scratch files. They never call the full checker main or inspect actual campaign evidence. Source parsing is static only. Generic lifecycle/accounting functions were statically extracted from the previous independent control-channel review and adapted to the agreed new receipt identity; no historical checker was imported or invoked. All delivery, predecessor and negotiated-host hashes are retained in `STATIC-CHECKS.json`.
