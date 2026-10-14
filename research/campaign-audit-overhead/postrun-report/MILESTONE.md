# AUDIT-C1: terminal launch rejection

**Outcome: `integrity_blocked`; no correctness or performance child launched.** The one-shot attempt began at **2026-10-14 04:53:51 UTC** and stopped while validating the frozen performance schedule. Its exact terminal reason is:

> Performance jobs must match all 64 prescribed serial slots, zero-based blocks

The [start marker](../robustness-review/results/WINDOW-STARTED.json), [supervisor receipt](../robustness-review/results/SUPERVISOR.json) and [final-accounting receipt](../robustness-review/results/FINAL-ACCOUNTING.json) are preserved as written. [Machine-readable evidence](EVIDENCE.json) records their exact byte lengths, SHA-256 identities and source fields.

## Why the schedule was rejected

The [independent static diagnosis](../postrun-diagnosis/REPORT.md) finds that the frozen supervisor uses **CB** for seed 840137, zero-based block 6, while the plan/protocol, jobs and cost validator require **BC**. That reversed pair affects four of 64 performance slots across the two workloads. The diagnosis preserves the source and proposes only a future, separately authorized correction.

## What this establishes

- The released supervisor was attempted once and rejected the schedule before the numerical child loop. In the frozen [supervisor source](../robustness-review/supervise.py), `verify_release()` calls `verify_jobs()` before that loop; the exception occurs there.
- `completedJobIds` and `reapedProcesses` are empty. The retained results contain only the three terminal receipts, with no child correctness/performance receipts or numerical checkpoint.
- `unrunJobIds` is also empty because `self.rows` is assigned only after `verify_jobs()` returns successfully. All **82 configured children (18 correctness and 64 performance)** were unrun, as was the independent correctness gate. The empty field does not mean the planned jobs were completed or waived. The supervisor's default checkpoint path is not evidence that a checkpoint exists.
- The one-shot marker says `retryAllowed: false`; the release admits zero retries. The frozen configuration, code and failure evidence remain unchanged. This report does not authorize a repair or another attempt.

## Resource evidence and its limits

The final-accounting receipt records **0.048071681001601974 s wall** and **0.046626999999999995 s process-tree CPU**, both **before its own write**. At that same pre-write point it records 1,604,492 new-study logical retained bytes and 135,833,805 combined logical retained bytes. Its `withinHardCapsBeforeWrite` field is true.

These are counters for a rejected launch, not an audit speed measurement or a guarantee about later postrun storage. They do not include a completed correctness gate, benchmark comparison or scientific qualification. Final frozen identity and runtime checks are explicitly `not_run_after_failed_window`; the earlier full frozen-file/runtime verification in `verify_release()` was also not reached because it follows the failed schedule check. The original timing qualifications are preserved rather than promoted into complete-window totals.

## No new scientific conclusion

Exact-output equivalence remains unestablished by this attempt. No speedup was measured, no new trajectories were produced, and no physical validation follows. The prior joint-stage numerical reference remains incomplete and unqualified. Its missing comparisons, retained partial/failure evidence and physically unvalidated airflow model are unchanged.

The [postrun Three.js demonstration](../postrun-demo/index.html) connects the actual terminal records to the existing historical viewer. Those flight paths predate this attempt. P1 displays poses through 0.990 s and then holds the last pose; the prior actual accepted stop was 0.9915625 s. Playback interpolation is for display only.

## Preparation and next decision

Only new `postrun-demo/` and `postrun-report/` artifacts were prepared here. The frozen original `demo/`, source/configuration, release and terminal receipts were not edited. No numerical code, browser or supervisor retry was run, and no remote write was made. [Static checks](STATIC-CHECKS.json) cover syntax, source hashes and both relative-link layouts; browser rendering is unverified.

A future experiment would require a separately authorized prospective repair/review/freeze/release while retaining this terminal outcome and its consumed attempt. This milestone does not propose restarting the old budget or relaxing the checks.
