# Supervisor integration review — source preparation only

The new replication supervisor and guardian integrate the observed-leader readiness handshake and failure/closure evidence from the saved harmless renewal. This is a source review, not a scientific or runtime qualification. No target module was imported or executed, no live process probe was made, and no publication or allocation execution was performed.

## Evidence and scope

The renewal `results/check.json` and `results/index.json` report eight of eight operational cases passed, no fatal failure, caller-attested `tool-require-escalated` context, and qualified normal release/forced cleanup behavior. Their explicit negative claims remain in force: scientificQualification=false, historicalRootCauseEstablished=false, scientificRerunAuthorized=false. The harmless result does not establish the cause of the old failed scientific attempt or validate this larger integration at runtime.

The historical failed normalizer package was read only. Work was limited to the new package's `source/supervise.py`, `source/guardian.py`, this review, its static-check JSON and unified diff. The parent supplied new allocation ID `m31-normalizer-replication-v1`, seeds 26171021/26171022, and cutoff `2026-10-17T01:00:00Z`. Scientific worker/checker logic is outside this ownership scope.

## Integrated behavior

- The supervisor requires Python isolation and the explicit execution-context label before launch. The saved evidence describes that label as caller attestation; it is not a sandbox detector.
- The guardian exclusively creates and fsyncs its event file, emits `guardian-start` then `ready`, and waits for `start`. It cannot spawn the scientific child before reading authorization bound to stage, source commit, source manifest, config, cutoff, execution context, guardian PID, supervisor PID and positive leader observation.
- The supervisor performs a real `/bin/ps -axo pid=,ppid=,pgid=,rss=` sample with a two-second timeout. It parses every nonempty row as exactly four ASCII numeric fields, verifies the ready guardian as its direct child and positive-RSS group leader, exclusively writes/fsyncs authorization, then sends `start`. Guardian checks the cutoff immediately before Popen.
- Probe exception/nonzero/malformed failures retain operation, explicit command, timeout, exception or return code, bounded redacted diagnostic text and injected=false. Unrelated process-table rows are not published; malformed row text is redacted.
- The first failure sets terminationReason once and is immediately appended/fsynced to a separate durable journal. Missing index/journal, source recheck, accounting, cleanup and closure failures append secondary records. Terminal fallback recovers the first saved failure when possible. A persistence error is reported explicitly and prevents success.
- Normal release requires child-exit plus a positive sample containing only the retained guardian. Final closure records guardian wait status and exactly two timestamped group-absence probes. An absent group without known guardian wait status is not closed. If Popen never created a group, `noGroupCreated=true` states that narrower fact and success remains false.
- Guardian failure retains TERM/child-wait/KILL cleanup of its owned group and records a cleanup child status when available. The supervisor does not signal a group after observing that its retained owner has exited.

## Consumer and accounting contract

New stage metadata: `<stage>-authorization.json` and `<stage>-failures.jsonl`. Both are exclusive, included in metadata/total budgets, stage preexistence checks, prior-kernel lifecycle pins and final evidence checks. Authorization, failure journal and guardian journal each have a 64 KiB file cap within the existing 16 MiB metadata/log allocation. Success has an empty failures file.

Each journal line is `{"role":"firstFailure"|"secondaryFailure","failure":{"kind":...,"monotonicNs":...,...details}}`. The same failure objects appear as report `firstFailure` and `secondaryFailures`. On success: firstFailure=null, secondaryFailures=[], firstFailureDurable=null, failureJournalDurable=true. Authorization and failureJournal pins use path/bytes/sha256.

Successful guardianEvents contain exactly guardian-start, ready, child-start, child-exit, released, each with monotonicNs. The report preserves all legacy successful fields and adds execution context, supervisor PID/group, guardianReadyObserved, leaderObservation, authorization, authorizationEvidence, guardianEventsEvidence, normalRelease, releaseObservation, guardianWaitStatusKnown, closureProbes and durable failure fields. The parent checker consumer was text-reviewed against this schema; parent tightened event PID/group and authorization timestamp bindings following review.

## Preservation checks and limits

AST-only checks confirm unchanged resource constants, expected limit dictionary, scientific child commands/templates, controls, scene identifiers, output-science classifications, input/call schedule sets, allowed directories, raw-log names and loader cleanup definitions. Every original identity_check statement remains in its original order, with a new current-authorization byte check added. Existing source-manifest, publication receipt, Git/HEAD/blob, runtime identity, exclusive attempt and prior-evidence rechecks remain.

Caps remain 600 seconds per stage, 610 seconds for guardian, sampled group RSS 1 GiB, kernel output 192 MiB, checker output 64 MiB, metadata/logs 16 MiB and total 272 MiB. The scientific sequential-worker schedule and child command expressions are unchanged. Sampling remains sampled monitoring, not continuous RSS enforcement or hostile escape isolation. The new source has not been dynamically qualified; source acceptance/publication and any later execution gates remain separate.

## Bounded reading inventory

Twelve distinct input/source files were inspected: renewal results/check.json and results/index.json; old normalizer source/supervise.py, guardian.py and check.py; renewal source/guard.py, run.py and check.py; new replication source/config.json, supervise.py, guardian.py and check.py. The three generated review artifacts bring the conservative total to 15 of the 18-file cap. Repeated partial reads did not expand the distinct-file set.

## Source pins

- `research/m31-normalizer-replication-2026-10-17/source/supervise.py`: 45435 bytes; SHA-256 `25e143081816beac1f973133a63007819d7fa21ab9bb10b87f6ddfe944619359`.
- `research/m31-normalizer-replication-2026-10-17/source/guardian.py`: 5810 bytes; SHA-256 `a4afdbb265d8a375cafb576b6770b04b36ca3342016b3a7b36c21d88bef90885`.

See `INTEGRATION-STATIC-CHECK.json` for data-only verification and `SUPERVISOR-INTEGRATION.diff` for the complete two-file change against the historical source.
