# Independent source review: separate saved-record audit

Review date: 2026-10-17. This review read source/configuration and hashed bytes only. It did not import or execute either new audit source, the original checker, arithmetic fixtures, corruption tests, a browser or scientific targets. The author made all source corrections; the reviewer made no source edits.

## Decision

No remaining source blocker was found for freezing the exact reviewed revision and proceeding through its publication and allocation gates. This is source acceptance for the separately adopted audit, not numerical approval, evidence of a run or repair of the original failed stage. Actual package copies now match the authors’ final pins below. A new frozen manifest must contain the full original closure plus the new source, configuration and decision records.

The new implementation makes the intended distinction explicit: original browser supervision remains failed, the original conditional check stage stays unexecuted, and one new Python-only audit can evaluate the fixed saved outputs with the exact previously frozen checker. No browser, raw-state selection, reference regeneration, target repetition, new tolerance, changed fixture, changed corruption or scientific source repair appears in this path.

## Exact checker reuse and output separation

`audit.py` verifies its package location, dispatch attestation, new manifest, pinned Python runtime, six designated original input pins and every original manifest file. Every one of the 306 original pins must appear identically in the new flat manifest. It requires the original failed-attempt status, child exit code, cleanup error class and old source identities. Both original check artifacts must remain absent. The saved inputs in the new configuration were independently rehashed and match the preceding failed-supervisor review.

Only after those checks and the import cutoff does the child resolve the original checker at its exact original absolute repository path, construct a non-`__main__` import specification and execute that unchanged file. It calls `module.main(root, original_manifest_sha, original_source_commit)` without changing constants, globals, arguments, paths, functions or `__file__`. Consequently the original checker's location, original source/runtime/input/provenance/control gates, fourteen arithmetic fixtures, four fixed corruption tests and numerical criteria remain intact. Its command-line block does not run and cannot create the original package's `results/check.json`.

The wrapper copies every field of the returned scientific report unchanged and adds only `savedEvidenceAudit` provenance. It writes exclusively to the new package's `results/check.json`; the added metadata explicitly retains original failed supervision, no repair, no launch/cleanup compliance claim, zero new browser calls and no performance or online-certificate claim. The fixture and corruption ID lists match the frozen original source, and both child and supervisor require their pass assertions for a completed audit. A valid unqualified numerical report is preserved rather than transformed into qualification. If the child throws before producing a report, the separate failed attempt and private child-log identity remain the failure record.

The unchanged original checker imports only the standard library and has no network, subprocess or native-producer import. Neither the wrapper nor the checker launches descendants. There is therefore one Python child for the new supervisor to own.

## Publication, one-use and preservation gates

The supervisor requires a new exclusive attempt marker before launch. It verifies the new source manifest and each file, exact inclusion of the original closure, the pinned executable, fixed resource contract, original input pins and original failed-attempt identity. It validates both the old publication receipt and the new receipt, including commit, manifest length/hash/path, verified pin count, exact-local/remote flags and publication timestamps before the respective attempt starts. The outer supervisor is the supported execution entry point; the child is its implementation, not an alternative authorization path.

The new source manifest and publication receipt are separately captured for postrun preservation because neither is treated as an ordinary self-pinned manifest file. All manifest inputs are reverified in `finally`, on failures as well as normal completion, and original check artifact absence is rechecked. Final completed status requires a successful child, accepted report provenance, fixture/corruption integrity and preservation. A completed saved audit cannot retroactively add missing output hashes or cleanup success to the original attempt.

The report, attempt and private log use exclusive initial creation. Attempt finalization writes a separate temporary file before replacement. File contents are flushed and fsynced; this is not a claim of a host-crash-atomic transactional directory or immunity to storage/permission errors. Raw stdout/stderr stays private; public metadata carries only its size/hash. Both public exception-reporting paths redact repository/home prefixes. No process identifier is published by this new supervisor.

## Resources and failure behavior

The sole retained `Popen` child is waited with a 120-second wall deadline. A timeout kills and reaps that specific child with up to five seconds of separately recorded cleanup, without group/session/guardian signaling. Reaped handles are cleared; general failure cleanup checks the retained handle and records exit/reap outcome. This avoids the original group-cleanup operation while preserving failure if specific-child cleanup itself fails.

The child inherits CPU limits of 120/121 seconds and a 32 MiB per-file limit. New evidence plus private child-log size is checked against 96 MiB, with space reserved for attempt finalization. There is no enforced memory ceiling. The source explicitly records that the wall deadline requires a live supervisor; per-process CPU/file limits survive parent loss. Host suspension, unexpected supervisor death and operating-system cleanup denial remain ordinary process-supervision limitations. This source review cannot predict execution time, memory consumption or success.

## Findings resolved before the new invocation

The initial draft's final preservation/size exception path exposed raw error text. It now uses the same repository/home redaction helper as the primary failure path. The author also completed explicit equality enforcement for every original pin in both parent and child, clarified parent-loss resource limits, removed unnecessary public child PID metadata and made timeout/reap bookkeeping single-pass. No numerical observations informed these changes.

## Parent documentation consistency

The packaged adopted decision, protocol, execution allocation, reproduction instructions and implementation memorandum agree with the reviewed code: one separately allocated saved-record audit, the original failure retained, unchanged original checker main call, original conditional check artifacts absent, new-package output only, fixed fixture/corruption/numerical criteria, the same cutoff and resource limits, preservation on failure and no retry. The reproduction note correctly says the environment attestation alone is not permission: the parent must actually use its authorized escalated dispatch. The documented live-supervisor limitation matches the implementation. No documentation grants a broader numerical, physical or operational claim than the saved audit can support.

## Reviewed packaged file pins

All paths below are repository-relative. The three packaged source/configuration files are byte-identical to the author’s sealed final draft. The packaged implementation memorandum is byte-identical to the author's final README. Parent documents were read from these exact package copies.

| File | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-native-saved-audit-2026-10-17/source/run.py` | 14578 | `af90686eb0a927683109bc66f9a0f4dc837c6fd537c72d946228feb1aad31cc6` |
| `research/m31-native-saved-audit-2026-10-17/source/audit.py` | 7421 | `14bc9fc6c794f71d1823293980fa2f53b3dfa805aed025e3ce5e652bd7aac077` |
| `research/m31-native-saved-audit-2026-10-17/config.json` | 2754 | `9dcfc700cc7cace45a8a88e123ffdeb6eeb03d33345ea4cf82e11e35701f5fcf` |
| `research/m31-native-saved-audit-2026-10-17/ADOPTED-DECISION.md` | 1642 | `e4ee80c9709c1ff65d65619474a6dee3ad728b68fcd79bee2d050c2ccb38c3e6` |
| `research/m31-native-saved-audit-2026-10-17/PROTOCOL.md` | 3160 | `8d537176bc08258428001613f6c4187f32829fe0cb11a1a169e36a8baf704e52` |
| `research/m31-native-saved-audit-2026-10-17/EXECUTION-ALLOCATION.md` | 843 | `329463b38bdf2da9c809fd75ff4b2d3ece62dd6b151c87c1ef3c49fd04571f80` |
| `research/m31-native-saved-audit-2026-10-17/REPRODUCTION.md` | 1423 | `30f4d7abe22c8cc5eb69172f038f34d85e3754fe047dda882660d92443a25be6` |
| `research/m31-native-saved-audit-2026-10-17/review/IMPLEMENTATION.md` | 6589 | `87be202ff1c424326bbd1da8e85407a186dff6259a3201d9ec8f13a9cc9767b0` |

Unchanged original checker: `research/m31-native-load-baseline-2026-10-17/source/check.py`; 42,628 bytes; SHA-256 `bbf4a0fd042b0a19fe553ce3fd3be8e3775073fc958d38e19871c09c13ef09ef`.
