# Publication privacy and checkpoint review

## Disposition

**Approved locally for an explicit-allowlist partial-result checkpoint, subject to final remote tree verification.** The proposed scientific results, replay data, display artifacts, interpretation, retention review, transport manifest, updated README, finalized milestone report and literature–experiment ledger contain no identified private owner data or credentials. This review did not run experiments, recompute gates, integrate trajectories, or modify scientific bytes.

`PUBLIC-FILE-INVENTORY.json` lists exact recommended repository-relative additions with byte counts, SHA-256 and Git blob identities. Its binary entries describe transport objects, including split offsets, rather than inventing replacement scientific files. `CHECKPOINT-VERIFICATION.json` records the local evidence checks. The inventory itself can also be published; it is not self-hashed.

## Privacy decisions

- Exclude every file under `coordination/` from this checkpoint. In particular, `coordination/offline-library-receipt.json` contains an owner-scoped Library identifier and must remain private. Other transfer receipts are unnecessary public bookkeeping. Use the public transport manifest and verified commit/tree facts instead.
- No sanitization of the reviewed scientific outputs or derived display/report files is required. The two browser-failure logs contain generic workspace, script and temporary Chromium-profile paths, not a personal home directory, private conversation URL, credential or user identity. They may remain byte-exact.
- All 14 HTML-embedded evidence documents were decoded and matched their original files byte-for-byte. Embedded records, application code and vendor modules were also scanned. No hidden private identifiers were found. Vendor documentation URLs, variable names and synthetic path-security test strings are not owner data.
- The archive reconstruction utility, synthetic tests and instructions contain no private owner data. Their byte-recovery and synthetic-test evidence must not be described as a new numerical experiment or a remote-checkout validation.
- Exclude generated Python caches and any future owner-specific Library/upload receipt. Re-review new or changed files rather than recursively publishing the working directory.

## Completeness and recorded claims

- The binary manifest covers all 52 existing result binaries, totaling 58,664,800 bytes, as 54 exact transport objects. Whole-file hashes, object hashes, Git blob identities and consecutive split offsets matched local bytes. Both dense files have two pieces. Empty J field streams are intentional artifacts and remain included.
- All 71 frozen source identities matched. Frozen source/protocol checkpoint: `3f25c755a7073a120e5fd1e85f1534f0e3e5f0e7`.
- All six J trajectories completed. Both saved self-consistency gates passed, with every fine comparison below its prescribed floor. This is floor-limited self-consistency, not a measured convergence order or a physical truth-error bound.
- H4 for seed 840131 completed. P1 for that seed stopped at accepted tick 50,768 (0.9915625 s) on the 44 s cooperative job guard. Its retained total job time, including serialization, is 44.029648370 s, below the separate 45 s hard boundary.
- The new matrix contains 7 completed rows, 1 failed/incomplete row and 8 skipped rows. Failure JSON, the incomplete raw prefix, supervisor record, last durable checkpoint and execution-validity rejection must all be retained. A generic matrix reason on completed rows is a known labeling blemish; the original status/run records are unchanged.
- Held-physics and cross-family gates remain unfinished. There is no qualified full numerical reference, physical validation, safe-flight result or browser-throughput result.
- Browser launch failed before page load. Static HTML/link checks passed; rendered browser behavior remains unverified. Keep both the launch failure and timing evidence.

## Publication closure

Object uploads alone do not establish a published checkpoint. Verify the committed branch tree against every approved repository path and Git blob SHA, including all failure/partial records and 54 binary objects. Confirm private receipts are absent, retain the existing frozen implementation tree, and record the final commit and tree identity. Two dense logical paths require the documented byte reconstruction before consumers open them directly. This review establishes local completeness; it does not claim remote publication has already succeeded.
