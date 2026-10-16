# Saved-only postrun containment review

The sole kernel attempt failed closed. The saved evidence localizes the failure to the first process-table sampling attempt, but does not preserve the initiating exception. A sandbox-related `ps` failure is a plausible explanation, not a proven cause. The source has a definite diagnostic defect: finalization can replace the initial failure reason with the secondary fact that the kernel journal is missing.

This review read saved records and frozen source only. It did not execute the supervisor, guardian, `ps`, candidate, generator or checker; reproduce the launch; import scientific modules; or change any source or prior result. The original attempt remains consumed. No checker or rerun is recommended for this allocation.

## Recorded facts and exact binding

The attempt binds to public source commit `2839f76cb0aaf908f82964dd3d1bf4296e7774b5`, source-manifest SHA256 `3e943151180c584eb4618056bd3a29d8ef6f9457d47468c6c3c43f72a86f86cb`, and config SHA256 `8023f4c8c508e344695549fda99645268fa96043b4e62bdd1e3f19bef00351b2`. The public receipt records verification at `2026-10-16T22:41:43.034625+00:00`; the permanent kernel attempt records start at `2026-10-16T22:41:48.359720+00:00`.

`results/kernel-supervision.json` records:

- `success: false`, `closed: true`, `childGroupAbsent: true`, and `sourceAndRuntimeRechecked: true`.
- `terminationReason: incomplete-stage-evidence`, `wallSeconds: 1.1954191653057933`, and process-group identifier `33446`.
- `samples: 0`, `peakSampledGroupRssBytes: 0`, and `maxSampleGapSeconds: 0.0020055407658219337`.
- No observed worker PIDs, no scientific evidence files, zero public/raw stdout and stderr bytes, and no output-accounting violation.
- No recorded `exitCode`, `guardianExitCode`, or `scientificChildAbsentBeforeRelease` fields.

The current saved result directory contains only the permanent attempt, supervision report and two empty public logs. The guardian event file, kernel index, kernel journal, checker attempt and checker report are absent. Zero sampled RSS means no completed RSS samples; it does not measure zero memory use. The 1.195-second wall interval includes cleanup and final identity/accounting work, and is not a candidate runtime measurement.

| File, relative to this package | Bytes | SHA256 |
| --- | ---: | --- |
| `source/supervise.py` | 29715 | `1e008611cd0e05132b2eb38e161b03c30c9ed2eb4fa1ddb3f494be62edfabddb` |
| `source/guardian.py` | 2964 | `4f34f3a34b6fcf059dfb7c40e2d3eb05e0c361c8290fd397781896c65bd6a771` |
| `results/kernel-supervision.json` | 4450 | `6a87f4df5626f39d4f495597da3a68c8a9fd1398702dc00319e2067a9b53f791` |
| `results/kernel-attempt.json` | 421 | `9c53e1bb0ca1caff4d2a6de6e3c81fc8a2c4c6c7e88b814f0e086082de1d492b` |
| `source-publication.json` | 868 | `94baf45b50363a0af7bc44ecaadbb09a852f891086e4ba71de60d74dace94d4b` |

Both inspected source files match their frozen source-manifest entries. This review did not repeat the full 88-file public verification or independently inspect private logs; the report records their empty-byte pins. The companion reading inventory binds the manifest, empty public logs, absences and review scope.

## What the frozen control flow supports

At supervisor lines 355–358, a returned `Popen` object supplies the recorded process-group PID. This establishes that the supervisor obtained a guardian process handle; it does not establish guardian readiness or scientific-child launch.

At lines 324–328, `sample()` first updates `maxSampleGapSeconds`, then runs `ps -axo pid=,ppid=,pgid=,rss=` with captured output, `check=True` and a two-second timeout. It parses integer rows and selects the guardian group before incrementing `samples`. The positive recorded gap with a zero sample count therefore places the failure after entering that first sample and before completing the process-table read/parse/group selection, under the frozen source control flow. A failed `ps` invocation, nonzero exit or row-parsing exception would fit. There is no saved return code, stderr, exception class or traceback to choose between them.

An ordinary race in which the guardian is simply not yet visible in an otherwise successful `ps` result is insufficient on its own: an empty selected group would still increment `samples`. A guardian exit detected by the subsequent `guardian.poll()` check would likewise occur after that increment. The zero count points earlier in the sampler.

At lines 385–386, the exception handler retains either a registered reason or only `supervisor-<exception class>`. It does not persist bounded `ps` stderr/return-code detail. At line 449, a missing kernel journal then unconditionally assigns `incomplete-stage-evidence`, overwriting that earlier reason. The missing-index branch at line 442 is more conservative, assigning a reason only when none exists; the missing-journal branch does not preserve this distinction. This loss of the initiating diagnosis is directly established by source inspection.

Normal-release exit codes are recorded only at line 384. They are absent here, so this record is not evidence of normal guardian release. The final closure fields instead arise from cleanup and subsequent process-group absence checks. They establish the supervisor's recorded closed state without supplying the missing launch/sampler diagnosis.

## Sandbox and startup-race hypotheses

The parent supplied execution context that the launch used the default tool sandbox (`sandbox_permissions` was omitted) and that no automatic approval-review rejection occurred. This is trusted task context, not a field independently corroborated by the saved supervision report. A sandbox restriction on process inspection is consistent with a first `ps` failure. It is not sufficient to conclude that `ps` was denied, nor that an approval mechanism rejected the launch.

The guardian creates and fsyncs its event file before spawning the scientific child (guardian lines 37–45). The supervisor does not wait for an explicit guardian-ready acknowledgment before its first sample. If sampling fails immediately, cleanup may signal the new guardian before it reaches event-file creation or installs its signal handler. That sequence is consistent with the missing guardian file and empty logs; it is a plausible secondary startup/cleanup race, not a demonstrated initiating cause. There is no affirmative saved child-start observation. Absence of scientific records is not, by itself, a complete process-execution trace proving that no scientific instructions ever ran.

The saved record does not establish an aerodynamic, normalizer, candidate-equivalence or performance failure. It also supplies no completed RSS measurement and no speed comparison. The original outcome remains an infrastructure/containment-stage failure with the initiating cause unresolved.

## Narrow future source-only correction scope

Start with a separate containment-source review, leaving this source and attempt unchanged:

1. Preserve an immutable first-failure record containing stage/operation, exception class, bounded sanitized message and, for the sampler subprocess, command identity, return code, bounded stdout/stderr and timeout status. Record missing index/journal and cleanup/accounting failures as separate secondary facts. Keep the final success gate fail-closed.
2. Define a guardian-ready/launch handshake. Persist readiness and process identity before permitting a scientific child; record supervisor authorization and child start separately. Preserve the retained-group ownership and bounded cleanup rules. Do not treat the absence of an initial process-table row as readiness evidence.
3. Specify a harmless containment harness that qualifies process-table access in the exact proposed launch environment, including its sandbox and runtime context. Its cases should cover a delayed guardian startup, a short-lived inert child, sampler nonzero/denied/malformed output, premature guardian exit and cleanup. This harness requires its own explicit allocation before execution; none was run here. Freeze successful environment/capability checks before a separately allocated scientific run, and retain failure details instead of silently dropping process monitoring.
4. Make assertions about cause retention, secondary completeness failures, readiness, exit/release state and final group closure part of that source contract. Only after independent review and a separately authorized harmless qualification should a fresh scientific protocol/source allocation be considered. Do not spend the old attempt again or launch the old checker on absent evidence.

These are prospective design changes only. This review neither implements them nor demonstrates that they would resolve the observed failure.
