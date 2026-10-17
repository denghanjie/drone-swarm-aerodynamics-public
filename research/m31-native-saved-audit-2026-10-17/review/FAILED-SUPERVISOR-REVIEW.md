# Independent review of failed supervision and saved browser evidence

Review date: 2026-10-17. Scope: source text, saved JSON structure, byte hashes, Git object bytes and record linkage. No native scientific module, browser, checker, fixture, control or target was imported or executed. No binary64 words were decoded, native loads reconstructed, reference intervals evaluated or numerical accuracy verdict calculated.

## Conclusion

The original browser stage remains **failed**. The saved browser controller record is structurally complete and internally linked to its durable journal. This supports consideration of a separately adopted, bounded audit of the exact saved records; it does not authorize the original conditional check stage or establish numerical qualification.

All 306 files in the original frozen manifest match both their declared local byte pins and the blobs in source commit `e6f99b140c70887fa0ed05c14574221eb5db12da`. The manifest itself matches that commit and SHA-256 `8bae9d039d2fbfd40a34085b1bc00f3c76725c57675ea2a681121add083f4019`. The publication receipt's commit, manifest length/hash and file count agree. Its current bytes and the current manifest bytes also match the preservation identities recorded before the failed launch. This review did not repeat the remote HTTPS retrieval; exact-publication evidence remains the pinned original receipt, supplemented here by independent local Git-object comparison.

## Failure boundary

The attempt records `status: failed`, `exitCode: 1`, `childExitCode: 0`, `cleanupError: true`, and `PermissionError: [Errno 1] Operation not permitted`. It records child wall time of about 6.96 seconds and supervisor wall time of about 7.35 seconds. The private guardian exit record independently says `returncode: 0`, and the private browser log is empty.

In the frozen supervisor, the group cleanup call follows collection of the child's exit code and precedes the output hash, private-log identity, size checks, postrun preservation loop and completed status. The attempt has no `ownedGroupCleanupIssued`, `outputSha256`, `outputBytes`, `privateLog` or `preservationPassed` fields. These missing registrations must remain missing. The source and saved failure locate the problem in cleanup, but do not identify which signal operation was denied or establish the platform cause. Browser context closure is recorded; successful complete owned-process-group cleanup is not established by these files. This review did not inspect or signal live processes.

Current hashes can establish current preservation and support a new chain of custody. They cannot retroactively supply the original supervisor's omitted postrun registration or guarantee absence of intervening changes. The original attempt must not be edited, marked completed, replaced or treated as a completed registered browser stage. At this review, neither original `check-attempt.json` nor original `check.json` exists.

## Saved evidence completeness and linkage

The controller records `complete: true`, `errors: []`, `scheduleReturned: true`, `runtimeIdentityVerified: true`, `inputsAndSourcesPreserved: true`, `browserClosed: true`, twelve completed/expected target calls and empty unattempted/unfinished arrays. These are recorded browser assertions, not a completed outer stage.

The final browser JSON links exactly to the journal's 5,361,836 bytes, SHA-256 and 184 records. Journal sequence values are contiguous from 0 through 183; the file ends in a newline. Its contents comprise one source-verified record, one source record, 91 intent records, 48 inherited-control records, six ownership-build records, one ownership record, 24 wrapper-control records and twelve target records. The intents comprise 48 control, one ownership, six ownership-build, 24 wrapper-control and twelve target intents.

Every saved target, inherited control, wrapper control, ownership build, ownership summary and final source receipt exactly equals its corresponding journal body. Target intent bodies also exactly equal the final attempt list. No target or declared control body is missing. Target sequences, case/method order and input file/semantic identity fields agree with the frozen configuration and contract. Each target record contains 64 IDs, raw rows, prepared rows, solution rows and delivered-load rows, together with the declared CSR field names. All twelve target statuses are recorded as `native-success`. This is structural completeness; support, arithmetic, load accuracy and parity still require the independent audit.

The recorded control summaries show all 48 inherited controls passed, all 24 wrapper controls passed with the expected statuses, six ownership builds matching the final ownership summary, and ownership pass. The nine adapter groups contain 56 assertions, all recorded true. All target input-unchanged and saved wrapper/target ownership predicates are true. These reported outcomes were not re-executed or independently recomputed here.

## Source and runtime linkage

The source receipt equals the frozen bundle pin and seven source descriptors. Each embedded slice equals the separately pinned source bytes. The seven factory IDs agree with that source set, and both the source receipt and adapter record assert verification before scientific factories. The adapter receipt equals the final control record. All nine served-file pins agree with the manifest: the HTML, harness, bundle and six raw inputs.

The recorded runtime agrees with the frozen metadata: Chrome 155.0.8059.80, Node v24.19.0 with its full byte/hash pin, Playwright 1.62.1, darwin arm64, eleven selected Chrome components and five selected Playwright components. One launch and one profile are recorded, with detached mode false. This review compared saved runtime assertions and pinned metadata; it did not relaunch Chrome or independently attest every runtime dependency. The original selected-component scope still applies.

## Defensible separate saved-record audit

The parent has adopted a separate saved-record audit in `research/m31-native-saved-audit-2026-10-17/ADOPTED-DECISION.md`. It is an explicitly disclosed operational deviation after failure, with an unchanged pre-observation scientific question, unchanged cases, checker, arithmetic fixtures, corruptions and tolerance. Its numerical result may establish consistency of these saved outputs under the declared model; it cannot turn the original failed supervision into a successful stage.

A defensible implementation should:

1. Pin the original failed attempt, browser output, journal, source manifest, publication receipt and full 306-file closure as immutable inputs; verify these before the new launch and again afterward. Pin and publish the new audit source, adoption record and bounded allocation before its single invocation.
2. Reuse the exact original checker source and invoke its unchanged `main(root, original_manifest_sha, original_commit)` from a new, independently recorded Python-only child, with no monkeypatch, producer import, new target, new reference or changed acceptance criterion. Preserve its original `__file__` identity check. Write its report into the new audit package, wrapped or supplemented with explicit original-stage-failed provenance.
3. Maintain exclusive attempt/output creation, pinned Python identity, a bounded child wall deadline, per-process CPU/file limits, private raw logs and a specific child handle for cleanup. A single Python checker that creates no descendants does not require the failing browser-group cleanup mechanism. The exact replacement supervisor must receive a source review before use.
4. Keep the original conditional check stage closed. Distinguish the new audit's execution/integrity status from its saved-output numerical verdict and from the failed original supervision. Do not claim a performance measurement, successful original operational reproducibility, fresh-state confirmation or broader validity from a positive saved-record audit.

This review supports the feasibility and evidentiary basis of that route. It does not approve an unseen new supervisor or perform the audit. The separate draft is being reviewed independently after this memo.

## Exact reviewed file pins

Public paths are repository-relative. Private paths below are relative to the private operational-log directory; their contents and process IDs are not reproduced here.

| Public file | Bytes | SHA-256 |
|---|---:|---|
| `research/m31-native-load-baseline-2026-10-17/source-manifest.json` | 64557 | `8bae9d039d2fbfd40a34085b1bc00f3c76725c57675ea2a681121add083f4019` |
| `research/m31-native-load-baseline-2026-10-17/source-publication.json` | 871 | `1aa8bde931534e4f20f755a8ab3929cdb93bb91657720156be1edb44fbdc966e` |
| `research/m31-native-load-baseline-2026-10-17/source/run.py` | 9505 | `a2bd813f9af9e18123a8ccbd13415c95d520230c6076408f4af15de99b29d1b4` |
| `research/m31-native-load-baseline-2026-10-17/source/group-runner.py` | 1067 | `5afedcbc870c6aac0898309e53e086c6763433d06a6fec115e36ff0fc30ef262` |
| `research/m31-native-load-baseline-2026-10-17/source/check.py` | 42628 | `bbf4a0fd042b0a19fe553ce3fd3be8e3775073fc958d38e19871c09c13ef09ef` |
| `research/m31-native-load-baseline-2026-10-17/source/controller.cjs` | 17166 | `11e59e977a0549813ae466769406e418490786bd2feedb78b53d19a573d4dfeb` |
| `research/m31-native-load-baseline-2026-10-17/source/checker-contract.json` | 9053 | `e648de28497b1ff830b51e9cd4e79be781283b2257ff4109b058949e9e64306f` |
| `research/m31-native-load-baseline-2026-10-17/runtime.json` | 6698 | `67930bf3cfd67628f088333247bf0142d3681a0626c78a9511d791a25aa52580` |
| `research/m31-native-load-baseline-2026-10-17/config.json` | 7025 | `168a12cf7db03f0645b50b0a9e1addcba3b53a7a21e7897f11a9b56f68cdca67` |
| `research/m31-native-load-baseline-2026-10-17/source/source-bundle.json` | 2089 | `2e08851800dd653112d3663ccd17ebe76d659f3b4592ca3b686c282f0212197d` |
| `research/m31-native-load-baseline-2026-10-17/source/browser-bundle.js` | 79419 | `292223cfcae5413b34ab7c29c561e77499dc38cde3d2ccc6a8b57d5203e5a54a` |
| `research/m31-native-load-baseline-2026-10-17/PROTOCOL.md` | 6198 | `e479842fab70be19b3676f655e774a588d05e00c69836aff1acf5b6e0cfed6e7` |
| `research/m31-native-load-baseline-2026-10-17/results/browser-attempt.json` | 1201 | `2d9db1aa6db0f61118ab735a7db6d2dca919a0a48d94b0a1cf49a4f5e9ad2c33` |
| `research/m31-native-load-baseline-2026-10-17/results/browser.json` | 5353146 | `2f1a599000e782f1ac50163cf05fd046b7fb3c20e9ed350c7566b8c9fce900fe` |
| `research/m31-native-load-baseline-2026-10-17/results/browser-journal.jsonl` | 5361836 | `8d5afa30fe10445a51fc81d4335dda9c10e6affd3cdb2f2bed354bc60b438cc8` |

| Private operational record | Bytes | SHA-256 |
|---|---:|---|
| `browser-process.json` | 1986 | `3666be66ddc797ce24175be6ac1cbb142b5d4dcebeeec40a237ced32ac345008` |
| `browser-supervisor/child.json` | 30 | `df72c7f12ce959f3443787bde84ad0d22f4809a3a739f045a547b681723e0e12` |
| `browser-supervisor/exit.json` | 17 | `c365161d39236fe0f1d32937fbc549796b8487d8faf65ed3879b96897c78ea5d` |
| `browser.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Machine-readable metadata companion: `m31-native-failed-supervisor-metadata.json`; 11201 bytes; SHA-256 `444aacea75f02df27fdb5fdac2500f50dc915385f732002f3d9557a94bc487bf`.
