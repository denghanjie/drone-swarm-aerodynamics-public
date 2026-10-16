# Exposed-corpus qualification supervision interface

Source preparation only. No qualification run, numerical helper import, probe or scientific evaluation is authorized by this file. The old moving-admission experiment remains failed. This is a separate attempt for qualification of a validator using an already exposed corpus.

## Invocation and ownership

Supervisor command: `PYTHON -I -B source/supervise.py qualification`, with the current package as the script's location. `RESEARCH_PRIVATE_RUN_DIR` names a fresh empty private log directory outside the repository. No Node runtime is launched or required. The active Python binary must match `runtime-pins.json` before and after the child. Python isolated mode and bytecode suppression are mandatory for supervisor, guardian and driver. Loader injection variables are refused; inherited Node/Python preload and search overrides are removed from the child environment.

The supervisor owns the exclusive permanent `results/qualification-attempt.json`, guardian events, private/public logs, `qualification-supervision.json` and any terminal-error record. The driver must not create, overwrite or reinterpret these files. Both the new results directory and private log directory must be empty before allocation. The attempt is written and fsynced before child launch; its existence prevents a retry. The old package and old outputs are read-only inputs, never output destinations.

Driver command:

`PYTHON -I -B source/qualify.py --config PACKAGE/source/config.json --manifest PACKAGE/source-manifest.json --output PACKAGE/results/qualification.json --root REPOSITORY_ROOT`

The driver returns exit 0 only when its exposed-corpus qualification passes, otherwise exit 1. A programmer error or incomplete report also closes the allocation. A failed result cannot be retried or replaced.

## Exact attempt and environment

Attempt fields are exactly `stage,sourceCommit,sourceManifestSha256,configSha256,priorSourceCommit,priorResultCommit,priorResultManifestSha256,launchCutoffUtc,allocation,startedUtc`. Stage is `qualification`. Allocation is `sole attempt; existence prevents retry`. startedUtc is timezone-aware UTC ISO text preserving microseconds. The three commits are distinct: old source, old published results, and new qualification source.

Supervisor provides these environment bindings:

- `RESEARCH_SUPERVISION_STAGE=qualification`.
- `RESEARCH_SOURCE_MANIFEST_PATH`: absolute new source-manifest path.
- `RESEARCH_EXPECTED_MANIFEST_SHA256`: new source-manifest raw-byte hash.
- `RESEARCH_SOURCE_COMMIT`: new publicly verified source commit.
- `RESEARCH_PRIOR_RESULT_MANIFEST_PATH`: absolute historical result-manifest path.
- `RESEARCH_PRIOR_RESULT_MANIFEST_SHA256`: historical result-manifest raw-byte hash.
- `RESEARCH_PRIOR_SOURCE_COMMIT`: `2a957d2b0bb26e731c8cd184bc13f51f673e9a0d`.
- `RESEARCH_PRIOR_RESULT_COMMIT`: `5a5efeef2d216188fa93a8034c4573d7327c5411`.

The driver verifies its required gates before importing historical helper functions. These environment fields bind a saved receipt and exclusive attempt; they do not replace source-file or corpus hash verification.

## Source and immutable corpus gates

New `source-manifest.json` has a unique closed list of `{path,bytes,sha256}` pins using canonical repository-relative POSIX paths. Mandatory entries include PROTOCOL.md, runtime-pins.json, this interface, config, result-contract, qualify, supervise and guardian, plus the old source/result manifests, historical result publication receipt, and old checker/pair-reference/semantic-reference/config/spec files.

New `source-publication.json` must record a lowercase 40-hex commit, exact manifest path/hash/bytes/file count, `remoteBytesEqualLocal:true`, `committedBytesEqualLocal:true`, and timezone-aware verifiedUtc before launch/cutoff. The supervisor verifies the current new manifest and all listed pins against the exact new committed blobs and requires HEAD to equal that source commit before and after qualification. It trusts the parent's saved exact-commit HTTPS transport receipt for remote verification; it performs no remote fetch itself.

The historical source commit is `2a957d2b0bb26e731c8cd184bc13f51f673e9a0d`, with source-manifest SHA256 `37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21` and 53 pins. The historical result commit is `5a5efeef2d216188fa93a8034c4573d7327c5411`, with result-manifest SHA256 `e60a5bf356f9f27bf31f79fc3274c0c37675353f1b8b0de20a1a6fc1b69487d8` and 128 pins. Its separate exact-publication receipt is pinned in config and the new source manifest.

Every old source/result pin is hashed as opaque bytes and compared with its corresponding historical committed blob before and after the child. The old check.json hash, `passed:false`, `advancement:false` and original source commit remain required. The old checker source hash remains required. These checks preserve historical evidence and do not rerun its main checker or scientific generation. Old publication/result qualification is never rewritten by a new outcome.

## Closed output set and resources

The driver may create only `results/qualification.json` and `results/reference/ID.json` for the following exact ordered IDs: positive, distant-zero, raw-force, order-incompatible, run-a-t0, run-a-t5, run-a-t10, run-b-t0, run-b-t5, run-b-t10. All 11 files are required for supervisor success. The only allowed scientific subdirectory is reference. Unexpected files/directories, symlinks and private log entries fail closure.

Scientific outputs share 64 MiB, including a 2 MiB report subcap and 32 MiB per-reference subcap. The driver reserves report capacity before reference writes. Attempts, guardian/supervision records, terminal errors and both public/private raw logs share 16 MiB; combined 80 MiB. The final supervisor report is capped at 64 KiB and its capacity is reserved during final accounting. The old immutable corpus is input evidence and is not included in new output accounting.

One driver allocation has a 600s supervised wall limit, a 610s independent guardian limit and sampled process-group RSS limit 1 GiB. All process launches are refused at or after `2026-10-16T23:00:00Z`. Supervisor and guardian each recheck cutoff immediately before their child launch. Timing and RSS include the qualification child and retained guardian according to the saved supervision scope. Final identity/output checks are included in the supervisor's reported elapsed duration and may fail the 600s limit.

## Closure and result interpretation

The retained guardian owns the process-group identity while its direct child runs and after that child exits. It emits exclusive append-only fsynced start/exit events, waits for the supervisor to observe child absence, and exits only after release or its deadline. Parent disconnection, guardian failure, unexpected descendants, resource violations or residual group members fail closure. The supervisor signals an owned group only while its guardian is alive, then requires group absence. This is reviewed non-hostile-child containment, with sampled RSS/process tables, not continuous peak measurement or hostile-process isolation.

Supervisor success requires driver exit 0, guardian exit 0, all 11 scientific artifacts, no resource/identity/closure failure, and a qualification report with `passed:true` and `exposedCorpusQualificationPassed:true`. The report's top-level `sourceCommit,sourceManifestSha256,configSha256,priorSourceCommit,priorResultCommit,priorResultManifestSha256` must equal the supervisor attempt bindings. The report must retain `historicalOriginalPassed:false`, `historicalOriginalAdvancement:false` and `transferAuthorized:false`. Source/runtime, the permanent attempt and the entire old corpus are rechecked before successful finalization. Both a failed scientific report and a supervisor error preserve the consumed attempt; neither permits an old-result change or a fresh retry.

`qualification-supervision.json` records the new/prior identities, current runtime pins, exact command template, resource/accounting scope, child/guardian exit codes, source/runtime and prior-corpus rechecks, public/private log pins, scientific evidence pins and overall closure. Any terminal finalization error writes a separate failure marker when possible and exits nonzero. A report file alone is insufficient to establish qualification success.
