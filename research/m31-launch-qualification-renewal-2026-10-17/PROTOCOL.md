# Prospective renewed harmless launch-harness qualification
This is a separate allocation under the standing research authorization for successive bounded cycles. The predecessor source-only package was never executed and remains immutable. Its source commit is a222ad048e49609e3eafddc099d27b245dfc2d76. New cutoff:2026-10-17T01:00:00Z. The parent rechecked the standing instruction delegating routine research decisions; the prior request for another window approval was unnecessary. This allocation relies on that existing authorization, not on an unanswered question or elapsed time. No prior attempt is deleted, retried or reclassified.

The only executable/configuration deltas are the new cutoff in config/checker and the checker package identity. All case logic, assertions, limits, runtime pin and fixture roster are unchanged. Existing reviews copied under review/inherited are historical; separate delta reviews must accept the new pins before source publication and any run.

This is a new operational allocation, separate from every scientific attempt. It does not repair or retry the failed normalizer study. There are no simulator, force, oracle, trajectory or candidate imports. The aim is to qualify a small replacement readiness/diagnostic mechanism before considering integration into a future scientific supervisor. Passing cannot qualify the old supervisor, establish the old root cause, or authorize another scientific run.

Freeze eight cases, in order: real process-table capability; normal inert child; child exit7; synthetic sampler nonzero; synthetic malformed sampler output; guardian ready delayed0.2s; inert child timeout0.3s; guardian exits before ready. Run each once, no retries. Real ps uses numeric pid/ppid/pgid/RSS fields only; no command arguments or unrelated process rows are published. Synthetic errors are explicitly injected, not claimed to reproduce the historical OS error. The intended launch environment is the tool's explicitly escalated local execution context, with the pinned isolated Python runtime; qualification does not transfer to a sandboxed context without another prospective allocation.

Each guarded case has one retained new process-group leader, at most one inert child, a five-second guardian watchdog and a four-second supervisor case deadline. The leader writes readiness before accepting start. The supervisor must complete a real process sample identifying the leader before writing authorization and sending start. Injected sampler faults occur at that boundary and must prevent start. A firstFailure object is set only once; missing output, cleanup and completeness errors are separate secondaryFailures. Group closure is recorded by two probes, and normal release requires the saved child-exit event and observed child absence. Never signal a group after its retained leader has exited.

Limits: one60-second run, one15-second saved-evidence check,128MiB sampled group RSS,1MiB complete result tree,64KiB per JSON report,32KiB per event/log file. Monitor sampled limits; this is not hostile-process isolation. The fixture code is inert and fixed. No dependency installation, network calls from the harness, scientific load or live process-table reproduction outside the sole run. Source preparation permits syntax/AST checks only, no imports or executions. Public-source manifest verification and independent review precede any run. No qualification launch at or after2026-10-17T01:00:00Z.

A separate checker reads saved files only. It must verify all eight slots, source/runtime/environment bindings, expected first failures, continued secondary missing-artifact facts, absence of unauthorized child starts, readiness→authorization→child-start ordering for launched cases, normal-release vs forced-cleanup distinction, positive observed process samples on actual cases, and recorded closure. An unknown failure, missing case or failed containment fails qualification. Preserve all failures. An infrastructure failure consumes this allocation.

Publish raw operational evidence, checker result, independent saved-evidence scrutiny, concise milestone, and an updated status page linking/embedding the already recorded historical Three.js flights with clear disclosure. This operational milestone produces no new 3D trajectory. The broader accuracy/computation and physical-validity goal remains unchanged and incomplete.

## Frozen expected outcomes

Case bounds include cleanup and two absence probes. The separate15-second saved checker is outside the60-second run budget. Expected failures qualify only when their exact cause and closure assertions match; child/sampler failure does not itself mean the qualification failed.

| Case | firstFailure.kind | Authorized / child-start | Expected child exit | Release | Required secondary failure |
| --- | --- | --- | --- | --- | --- |
| capability | null | no / no | none | not applicable | none |
| normal | null | yes / yes | 0 | normal | none |
| child-exit7 | child-exit | yes / yes | 7 | normal | missing-inert-output |
| sampler-nonzero | sampler-nonzero | no / no | none | forced cleanup | missing-inert-output |
| sampler-malformed | sampler-malformed | no / no | none | forced cleanup | missing-inert-output |
| delayed-ready | null | yes / yes | 0 | normal | none |
| child-timeout | child-timeout | yes / yes | termination recorded, no successful output | forced cleanup | missing-inert-output |
| early-guardian-exit | guardian-exit-before-release | no / no | none; guardian exits5 | no release | missing-inert-output |

Capability must positively find the running supervisor's own PID, expected process group and positive numeric RSS in real /bin/ps output; it has no new child group and its closed flag is administrative. All seven guarded cases require two absent group probes and recorded guardian wait status. Normal-release cases require released event, guardian exit0 and recorded child exit. Injected sampler faults occur after a successful real leader sample but before authorization. The synthetic nonzero result is return13 with stderr INJECTED process inspection failure. The synthetic malformed result returns0 with the exact line INJECTED MALFORMED ROW; parser grammar is four nonnegative decimal integers per nonempty row, and it must preserve ValueError plus the offending synthetic row. Both retain operation process-sample and injected=true. No injected failure is evidence about the old sandbox's actual behavior.
