# Source-only adversarial contract review

## Decision and scope

Static acceptance for publication of the six reviewed inputs below and the proposed, separate eight-case harmless qualification. No unresolved source-contract blocker was found in the final reviewed bytes. This decision is not an execution result, a runtime capability finding, or permission to rerun any scientific allocation. Exact public-source verification, the stated launch context, cutoff and the parent's one-attempt allocation remain separate prerequisites.

This reviewer read six distinct new-package files, within the explicitly extended ten-file cap. No prior review files were reopened. Earlier snapshots of these same files were reread as the authors applied the findings. This pass performed text/data reads and opaque byte hashes only: no harness or checker launch, source import, inert-child execution, process-table query, simulator access or reproduction. No additional agents were started by this reviewer. The public manifest and publication receipt did not yet exist as final reviewed evidence and are not certified by this note.

## Final reviewed input pins

All paths below are relative to `research/m31-launch-qualification-2026-10-17/` in the checkpoint worktree.

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 5534 | `21bb0a0f1379f7a908329a61d3a8f8d5304514050852498feedccbf1eb829a3f` |
| `source/config.json` | 536 | `ae4eaeb165a1754cc4e81e8621f43d99290fe23f6c37a8f444fd29401fede6b7` |
| `source/run.py` | 12950 | `148de9f1da3f1ccf3a995f70b9f3b8158bd7b8927325483cdb970ef09de509dd` |
| `source/guard.py` | 2862 | `18851920da041242f7df7f85f5782e7d0647a72e4d5831fdc7bad9c940e35e80` |
| `source/inert.py` | 378 | `a48b286b39a3b3a80d703d842a7a3a3bec341da8c8f5c9ee8f76358af5324344` |
| `source/check.py` | 22458 | `ab70f93c4a00d69611ea5e2f4355b323accf8593ea1a1c3ef8f5d0f3a34b4bf7` |

## Findings resolved before freeze

The initial prose did not freeze exact per-case primary failures or distinguish their expected negative behavior from an infrastructure failure. The final protocol supplies the outcome table. The checker independently fixes the eight ordered case IDs and rejects unexpected first failures, extra secondary failures, missing case slots, wrong artifact sets and failed closure. Expected missing output is retained as a separate `missing-inert-output` record; it cannot replace the primary cause.

`run.py` now records source/config/runtime identity, supervisor PID and PGID, case start time, a real owned-leader observation, authorization, and a release observation containing only the retained leader. Before authorization it verifies the leader's PID/PGID, supervisor parent and positive RSS. The checker binds these records to the saved identities, requires readiness before observation before authorization before child-start, and requires recorded child exit and a leader-only process sample before normal release. Saved leader/release RSS must not exceed the reported sampled peak, which is itself bounded by 128 MiB.

The delayed-ready fixture now saves `guardian-start` before its 0.2-second wait. The checker demands at least 200,000,000 ns between guardian-start and ready. The timeout fixture saves the primary timeout timestamp and the child's wait result during forced cleanup; the checker demands at least 300,000,000 ns after authorization and a negative integer return code for that same child PID. These assertions rely on saved monotonic timestamps rather than a case's total wall time alone.

The sampler now rejects every nonempty row that is not exactly four ASCII decimal integer tokens. Injected nonzero and malformed cases traverse the same error-handling path as real samples after a successful real leader observation, but before any authorization. They retain the exact synthetic diagnostic and `injected: true`. A real sampler exception retains operation, command, timeout, exception class and a bounded sanitized message. A real OS failure cannot pass merely by sharing a synthetic failure's kind because the checker also requires the injected flag and exact diagnostic facts.

The first failure is assigned once. Subsequent cleanup, closure-probe and final-event-parse errors are recorded separately. The checker permits only the exact secondary missing-output record in the expected negative cases; a cleanup or parsing failure prevents qualification. Ordinary final report/index writes remain under their respective active run/checker alarms. Filesystem failure can still prevent durable reporting, so a missing or partial report must remain an allocation failure, never an inferred pass.

The capability slot positively checks the actual supervisor's numeric PID/PGID/RSS, records that observation, applies its RSS bound and binds the observation to the shared supervisor identity. Its `closed` flag is explicitly administrative: this slot does not create a child process group and does not fabricate two closure probes. All seven guarded slots require recorded guardian wait status and two absent-group probes. The early-exit case is separately constrained to guardian exit 5 and no ready, authorization or child-start.

## Eight fixed expectations checked in source

| Case | Primary result | Child/release evidence |
| --- | --- | --- |
| capability | no first failure | Actual supervisor observation; no child or authorization |
| normal | no first failure | Authorized child exits 0; normal release; exact inert output |
| child-exit7 | `child-exit`, exit 7 | Authorized child exits 7; normal release; missing output retained |
| sampler-nonzero | `sampler-nonzero`, injected return 13 | Real leader observed; no authorization or child; forced guardian cleanup |
| sampler-malformed | `sampler-malformed`, injected return 0 and ValueError | Exact malformed row preserved; no authorization or child; forced cleanup |
| delayed-ready | no first failure | Measured delay at least 0.2 seconds; ordered authorization/start; exit 0 and normal release |
| child-timeout | `child-timeout`, deadline 0.3 seconds | Authorized child; timed failure; same child's negative cleanup exit; forced guardian cleanup |
| early-guardian-exit | `guardian-exit-before-release`, exit 5 | Only guardian-start and early-exit events; no authorization, ready or child |

Negative-case missing output is expected only when the corresponding primary and all containment facts are correct. Each case is bounded to five seconds including cleanup/probes; the supervisor's case deadline is four seconds and the guardian's own watchdog is five seconds. The 15-second saved checker is a separate allocation from the 60-second run. The checker enforces the complete one-MiB result tree, per-file bounds, exact report pins, expected top-level and per-case files, immutable saved evidence during checking, source/runtime bindings and chronological case order. It reads saved files and does not query live processes or execute the harness.

## Interpretation limits

The execution-context variable is a saved caller attestation, not a sandbox detector. The external tool dispatch must independently show the explicitly escalated environment; any capability finding would apply only to that environment and the pinned runtime. This review has not inspected such a future dispatch and does not infer one from the environment string.

The RSS limit is a sampled owned-process bound, not an unsampled peak guarantee or hostile-process isolation. Closure probes record absence at their two observation times; the retained-leader protocol and fixed inert source supply the broader control-flow argument. This finite exposed suite does not establish universal containment under arbitrary children, scheduling, filesystem failures or untested malformed rows.

The old normalizer allocation remains closed. Synthetic sampler errors cannot establish its historical OS error. Passing this new operational suite cannot qualify the old supervisor, authorize another scientific run, demonstrate physical validity, or produce a new flight trajectory. Those claims remain outside this review and outside this qualification.
