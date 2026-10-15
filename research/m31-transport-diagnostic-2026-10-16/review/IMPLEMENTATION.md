# New transport saved-public-evidence checker

Source-only draft. The checker has been AST-parsed and statically compared with the producer schema; it has never been imported or invoked. Freeze it separately only after the diagnostic has externally completed and the exact new evidence manifest exists. Source/schema corrections before freeze do not license a later retry.

## Scope and pass meaning

The pass scope requires a complete operational observation and consistent new public records. A fully observed failed synthetic transfer can pass this review. An early admission failure, missing result, truncated instrumentation, incomplete closure, or missing external completion cannot pass this scope; that rejection does **not** itself prove corrupted evidence. The report preserves an observed transport classification when it was reached before the rejection.

The checker reads the actual new received bytes after external closure, compares them with the frozen 3,840-byte fixture, and separately checks server acceptance, persistence and browser acknowledgement. `fetchCalls` is the pre-call binding reservation, not proof of a network request. Actual sink POST counts come from request-entry observations. No duplicate Playwright/CDP events are counted as independent requests. A transfer without a POST at the sink is not automatically assigned a policy cause.

Sink byte-count completion does not imply expected-fixture equality. The sink receipt is checked against the actual retained bytes and digest; expected-fixture equality is a separate fact, and successful browser acknowledgement additionally requires the expected digest. Honest observation of wrong content is distinct from a file changed after its recorded digest. The inert edge tests exposed and corrected an initial pre-freeze conflation; the original source and regression evidence are preserved.

The source freeze and all inspected new source bytes are reconciled. Public trace envelopes, selected field names, complete event order and recorder-health counts are checked. Optional browser/CDP observations remain optional. The checker reads no private trace or private directory. Private byte totals and RSS are explicitly reported as recorded observer values, not independently enumerated private artifacts or transient memory bounds. This is a limited public-evidence check, never a replacement for an earlier scientific review.

All scientific qualification, original-failure explanation and permission-for-more-science flags remain false. `candidatePublicEvidenceVerified` can become true only after all required checks. `publicEvidenceVerified` remains false inside the script: the coordinator must separately preserve actual checker exit 0 and the complete hash/length-matching stdout summary before making a final scoped review claim.

## Exact manifest contract

Create `review/evidence-manifest.json` after the terminal diagnostic and external completion artifacts exist. Freeze this exact manifest together with the checker and its review documents. It has:

```json
{
  "kind": "new-transport-public-evidence-manifest",
  "version": 1,
  "sourceCommit": "40 lowercase hexadecimal characters",
  "sourceFreezeSHA256": "64 lowercase hexadecimal characters",
  "files": [
    {"path": "campaign-relative path", "bytes": 0, "sha256": "actual SHA-256"}
  ]
}
```

The required paths are `freeze.json`, `payload.bin`, `payload.json`, `config.json`, `runtime-provenance.json`, `capture-launch.lock`, `raw/trace.public.ndjson`, `results/result.json`, `results/budget.json`, `results/capture.json`, `results/wrapper.json`, `results/diagnostic-stdout.txt`, `results/diagnostic-stderr.txt`, `results/sole-launch.lock`, `publication/capture-output.json`, `publication/observer-output.json`, and `publication/capture-execution.json`. Add `raw/received.bin` if it exists. Extra pins may be under this campaign's `source/`, `raw/`, `results/`, or `publication/`; they may not include `review/` or another campaign. Source-document pins need not be repeated because `freeze.json`'s repository-relative source pins are independently read and reconciled within the new campaign.

Do not add later files to `raw/` or `results/`; their exact phase directory counts are checked. Later publication and review artifacts belong in their separate directories. Manifest entries are unique, regular, contained files; symlinks and duplicate JSON keys are rejected.

The coordinator-agreed `publication/capture-execution.json` has `kind:"actual-transport-capture-tool-completion"`, `sourceCommit`, `sourceFreezeSHA256`, `toolSessionCompleted:true`, `actualCaptureExitCode`, and `actualFullElapsedSeconds`. The elapsed value is a conservative observation from before tool invocation until actual terminal tool completion, including tool latency. A session yield is not completion. Preserve the exact caller stdout summary at `publication/capture-output.json` and exact observer stdout summary at `publication/observer-output.json`.

## Accounting and lifecycle

The checker reconciles actual public raw/result directory bytes against their phase receipts. The inner total is raw plus pre-budget result directory plus the recorded private diagnostic total plus the exact budget and observer summary. The outer total adds its permanent lock, retained stderr, capture receipt and final summary. Internal summaries are counted once in their invocation phases.

The two later public summary copies are additional persisted files, separately recorded as `laterPublicationCopiesBytes`. The external execution receipt is recorded as `laterExecutionReceiptBytes`. Diagnostic output plus both later copies plus the external receipt must remain under 8 MiB. Source inputs and the frozen fixture are inputs, not generated diagnostic outputs.

The scoped pass requires actual external capture exit 0 within 60 seconds, the bound observer/capture summaries, clean recorded ownership/reaping, sampled RSS within the adopted cap, complete accounting, and a complete local observation. It does not assert a successful transfer merely because the process chain exits 0; the worker intentionally permits a fully observed failed transfer to exit 0.

## Sole review invocation, later only

Once separately frozen and authorized, the invocation shape is `python3 check-records.py ABSOLUTE_NEW_CAMPAIGN_ROOT`. The checker takes no old record path or executable argument, launches no process and imports only standard-library readers. It immediately reserves `review/sole-review.lock`, demands a fresh `review/results/`, and writes `review/results/review.json` plus one stdout summary. Every invocation is terminal, including a failure.

The timer starts before substantial imports/I/O, with a 25-second work deadline, final-write guard before 29 seconds, and a 30-second hard timer. Lock, report and stdout summary are counted under the separate 8-MiB review cap. The coordinator still measures actual full completion and retains exact stdout; later review-publication copies must be accounted separately. No tool receipt may substitute for an unobserved exit, and no corrected checker may rerun this closed review.

Before review freeze, inspect inert schema examples covering different producer wrappers, exact persistence with failed acknowledgement, complete failed fetch, incomplete traces, extra POST, corrupt payload, absent result and nonzero external exit. Do not import this operational script to test those examples: doing so creates its permanent invocation lock.

The standalone `run-inert-schema-tests.py` has now exercised 20 cases through a restricted interpreter over extracted pure AST expressions. `INERT-PREDICATES.json` pins the exact expressions and checker sources; `INERT-TEST-RESULTS.json` records outcomes and the interpreter pin. The operational checker was neither imported nor invoked. These predicate tests do not test real file handling, locks, timers, process supervision, browser behavior or a complete saved-evidence run.
