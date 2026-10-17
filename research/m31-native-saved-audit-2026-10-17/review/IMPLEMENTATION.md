# M31 saved native-load evidence audit

This package is a separate, single-attempt audit of frozen saved records. It does not repair the original browser stage, which remains failed because its supervisor received `PermissionError` during process-group cleanup. The original checker was not launched; the original package's `results/check-attempt.json` and `results/check.json` must stay absent.

The wrapper imports the byte-pinned original `research/m31-native-load-baseline-2026-10-17/source/check.py` by its original absolute path. It invokes `main(root, ORIGINAL_MANIFEST_SHA, ORIGINAL_SOURCE_COMMIT)` without patching constants, globals, paths, or functions. The imported file's `__main__` block does not execute. The new wrapper writes the returned report only to this package's `results/check.json` and adds `savedEvidenceAudit` provenance. Every original scientific field, schema, and qualification scope remains unchanged.

The original checker performs exact arithmetic on saved input, reference, and output records. This audit makes no browser calls and does not reconstruct coefficients, roots, or trajectories. It can establish saved-record numerical consistency only. It does not establish original launch/cleanup compliance, performance, online certification, fresh-state validation, or 5,000-drone feasibility.

## Frozen source and publication contract

Install these files at `research/m31-native-saved-audit-2026-10-17/`. The new `source-manifest.json` must have `files` entries with `path`, `bytes`, and `sha256`, plus `runtime.python` exactly equal to `config.json`. Its flat closure must include every one of the original manifest's 306 pins, all six configured original pins, and all new package source/configuration/documentation files. Identical overlapping entries appear once; conflicting pins or duplicate paths are rejected. The new manifest and its later publication receipt cannot include their own hashes.

Before launch, publish the frozen source commit and verify its committed and separately retrieved exact-commit manifest bytes. Save `source-publication.json` with `commit`, `manifestPath`, `manifestSha256`, `manifestBytes`, `verifiedFilePins`, `remoteBytesEqualLocal: true`, `committedBytesEqualLocal: true`, and timezone-aware `verifiedUtc`. The supervisor requires that receipt to bind the supplied new commit/manifest identity and predate the new attempt. The configured original receipt must similarly bind the original source and predate its original browser attempt. Receipt evidence is prepared separately; the runner performs no network operation.

Both scripts hash-check the complete new and original manifest closure before checker import. The supervisor also verifies publication, fixed runtime/resource policy, the frozen original failure, absence of original checker artifacts, and the exclusive new attempt before launching its child. It rechecks source/frozen-input preservation on success and failure. The launch/import cutoff remains `2026-10-17T03:00:00+00:00`.

## Supervision and resource scope

An authorized launch uses the pinned Python with `-I -B`, running `source/run.py NEW_MANIFEST_SHA NEW_SOURCE_COMMIT`. It requires `RESEARCH_EXECUTION_CONTEXT=tool-require-escalated` and an absolute `RESEARCH_PRIVATE_LOG_DIR` outside the repository. These environment fields are dispatch attestations, not an independent authorization system. The private `saved-check.log` is created exclusively and is not published.

The sole subprocess is the isolated Python audit wrapper. It creates no descendants. The supervisor retains the `Popen` handle and waits, kills, and reaps that child directly. It does not create or signal process groups, start a browser, or use a guardian. The child has a 120 s wall deadline, 120/121 s soft/hard CPU limits, and a 32 MiB per-file limit. Up to 5 s of kill/reap cleanup is recorded separately. The final aggregate check permits at most 96 MiB of new results and private log, reserving two 1 MiB attempt copies during atomic finalization. Attempt metadata itself is limited to 1 MiB.

The wall deadline and aggregate final check require a live supervisor. Ordinary parent loss can prevent wall-time termination, final preservation/accounting, and a completed attempt record; per-process CPU and file limits remain. There is no aggregate or per-process memory ceiling. An incomplete/failed attempt cannot support a supervised audit pass.

## Result interpretation

`results/check-attempt.json` has schema `m31-native-saved-audit-attempt-v1` and stage `saved-check`. Its exclusive creation prevents retries from replacing prior attempts. Supervised completion requires `status: completed`, `exitCode: 0`, `childExitCode: 0`, `childReaped: true`, and `preservationPassed: true`; `outputBytes` and `outputSha256` bind `results/check.json`.

The report retains schema `m31-native-load-check-v1`. Its added `savedEvidenceAudit` field uses schema `m31-native-saved-evidence-audit-provenance-v1` and binds the new source identity and original source/checker/browser/failed-attempt/journal pins. It states `originalSupervisorStatus: failed`, `originalSupervisorRepaired: false`, `originalCheckerMainUsedUnchanged: true`, `launchCleanupComplianceClaim: false`, `newBrowserCalls: 0`, `performanceClaim: false`, and `onlineCertificationClaim: false`.

The supervisor accepts either original numerical decision, `qualified` or `unqualified`, if report integrity, all 14 exact arithmetic fixtures, and all four corruption assertions pass. Thus `completed` is not equivalent to `qualified`. A display of retained-state audit success must additionally require `passed: true`, `decision: qualified`, all 12 qualified target calls, every original strict-category gate, and verified source/publication/attempt/output bindings. The original browser supervisor failure must remain visible.

If the unchanged checker raises before returning, the child exits unsuccessfully and no substitute checker report is fabricated. If a report is returned with a failed wrapper assertion, it is preserved as evidence while the new attempt fails. The original package remains untouched in either case.

## Draft validation

Draft preparation is source-only: syntax is checked by `ast.parse`, configuration is parsed as JSON, and source bytes are hashed. No draft or original scientific module, checker, fixture, or target calculation is imported or executed during this preparation. `SOURCE-PINS.json` identifies the reviewed draft files; the parent packaging step creates the complete publication manifest and its separate receipt.
