# Prospective administrative public identity verification

Source preparation only. No public acquisition is authorized by writing this document. The parent must supply the exact frozen source/result commit and manifest identity, complete the source-review gate, and authorize the corresponding single administrative acquisition. This verifier does not import scientific code, decode compressed archives, render images, aggregate logs or launch producer/audit/finalize/UI allocations.

## Helper and fixed bounds

Prepared administrative helper: `research/m31-native-factor-reuse-2026-10-23/source/public-verify.py`, 27,649 bytes, SHA-256 `21812d4d3c0a9e48471a8fdec099c76c62a44e53fc0e0caa8e4d7e1d1147cfee`. Its repository root is resolved relative to its own frozen path. It has been AST-parsed and its parser literals checked without importing or executing it. No numerical/runtime validation is claimed by those checks.

The helper supports separate source/result invocations, each prospectively bound to its exact manifest. Source invocation permits at most two concurrent public transfers, three attempts per identity, 45 seconds per attempt, 900 seconds overall, and 536,870,912 aggregate captured public stdout/stderr bytes. Result invocation permits at most four concurrent public transfers, three attempts per identity, 45 seconds per attempt, 3,600 seconds overall, and 805,306,368 aggregate captured public stdout/stderr bytes. The byte cap includes failed attempts and HTTP headers/JSON envelopes. Decoded binary payload is additionally checked by exact length/hash; the cap is not a process-memory limit. A retry can exhaust the overall cap, in which case acquisition fails and evidence is retained. There is no automatic alternate route or new budget after exhaustion.

The result-only increase is prospective administrative capacity, not an additional scientific allocation. The earlier radial-integration first result acquisition covered 2,029 declared pins: 1,939 successful fresh file reads plus 50 reused inputs, with 40 unresolved files and 160 retained connection-timeout attempts. Its successful fresh reads including the manifest covered 376,068,822 bytes; it used four concurrent HTTPS transfers and had no overall wall cap. The current checkpoint is expected to produce approximately 1,920 semantic payload files plus query logs and supporting evidence. Thus the source budget is not reused for the larger result workload. The 3,600-second/four-transfer/768-MiB result allowance gives bounded headroom for roughly 2,000 API reads and approximately 400 MB of fresh payload plus envelopes and retries. It does not guarantee transport success; any exhausted bound is a retained failure. No extra attempts or recovery are authorized by this rationale.

Use the existing authenticated `gh` CLI under `require_escalated`. Verify the exact repository `denghanjie/drone-swarm-aerodynamics-public` is public before requesting file bodies. This is authenticated public-repository evidence, not an unauthenticated raw-CDN claim. No installation or service purchase occurs.

## Identity and transport routes

Git identity uses fresh exact-commit tree metadata and a fresh local opaque-byte stream. Compute SHA-256 and Git blob SHA-1 over `blob <exact byte count>\0<bytes>`; require the recorded length/SHA-256 and the tree's ordinary-file blob OID to match. Input descriptors also carry originCommit and gitBlobOid. Bind every file to the frozen source/result tree and every input to its declared immutable origin tree. Do not call git show or cat-file to re-extract these large binary blobs. This is tree-metadata plus local-byte binding; it does not claim a new Git blob-body extraction. The original exhausted Git-show attempts and separately authorized administrative recovery remain preserved in INPUT-PREPARATION.json, INPUT-RECOVERY.json and ADMIN-IDENTITY-RECOVERY.md.

Fresh public text uses GitHub Contents API raw responses at the exact source/result ref. PNGs smaller than 1 MiB use Contents API JSON/base64 at that exact ref. Binary transport parts and larger PNGs use Git-blob JSON/base64 at the immutable blob OID independently obtained from that commit's tree. Base64 is only a transport envelope: validate path/type where applicable, size, encoding, decoded byte count, SHA-256 and Git blob SHA-1. The six compressed transport parts are never concatenated or decompressed by this checker. No PNG/image parser or renderer is used.

The current input set is exactly 35 pins totaling 209,531,895 bytes, including six binary transport parts. Source acquisition freshly checks every source/input pin and the manifest; no older public input proof is reused. Result acquisition can reuse only these exact source-verified immutable input descriptors, with fresh local/result-tree/origin-tree bindings. Every noninput result pin and the result manifest receives a fresh public read. The source-proof receipt itself must be a result-manifest pin and receive fresh public verification. Every frozen source/input descriptor must remain unchanged in the result manifest.

## Exact protocol binding before each invocation

After freeze, write a separate prospective JSON protocol outside the scientific checkpoint at `research/publication-receipts/m31-native-factor-reuse-<phase>-public-review-2026-10-23-protocol.json`. It must bind the following fields; commit/manifest identities and source/result file counts must be actual frozen values, never placeholders:

- phase: source or result.
- commit: the exact 40-hex published commit.
- manifest: file, bytes and sha256 for the corresponding source-manifest.json or result-manifest.json.
- filePins: the manifest's exact complete file count.
- inputPins: 35; inputBytes: 209531895.
- source bounds: `{"maxConcurrentTransfers":2,"attemptsPerIdentity":3,"secondsPerAttempt":45,"overallSeconds":900,"aggregateCapturedPublicBytes":536870912}`.
- result bounds: `{"maxConcurrentTransfers":4,"attemptsPerIdentity":3,"secondsPerAttempt":45,"overallSeconds":3600,"aggregateCapturedPublicBytes":805306368}`.
- helper: its repository-relative file path, exact bytes and SHA-256 stated above; the helper checks its own identity before acquisition.
- executionPermission: `require_escalated`.
- gitIdentityRoute, exactly: `Fresh exact-commit tree metadata bound to freshly streamed local Git blob SHA1 and SHA256; no Git blob extraction`.
- binaryRoute, exactly: `Git blob JSON/base64 for binary parts; Contents JSON/base64 for PNG below 1MiB, Git blob JSON/base64 for larger PNG; no raw binary requests`.
- For result only, reusedInputSourceReview: the actual source-receipt path, bytes and sha256.

Hash that completed protocol and pass its SHA-256 to the helper along with the exact phase/commit/manifest/file/input pins. Result invocation also receives the exact source commit and source-review receipt identity. The helper checks its CLI values against protocol content before acquisition. Include the helper identity, acquisition scope, retained preparation failures and authentication/transport disclosure in the completed protocol.

## Failure retention and allocation boundary

Source checks require all four scientific/display allocations to remain unstarted at both start and end. Result checks require frozen ALLOCATION-CLOSURE.json and all four matching closed supervisor records at both boundaries. These are administrative records; the verifier does not rerun a query or any validation routine. End-state checks are attempted after failure as well as success.

Each attempt records operation, path, identity, HTTP status when available, safe response metadata, captured stdout/stderr identities, bounded diagnostic text and elapsed time. The append-only event journal and successful or failed receipt are retained. An end-check failure is retained alongside any earlier acquisition error rather than replacing it. Successful file proofs point to exact numbered events; reused result-input proofs additionally point to the fixed source receipt and successful public event. A failed acquisition remains failed even if a later, separately authorized administrative recovery completes missing coverage. Original failures, receipts and declared limits must never be overwritten.

Publication identity success does not imply scientific correctness, cost qualification or completion of the overall research. The parent separately records source-publication.json only after source verification passes, and separately handles result/publication receipts after all required checks close. This document creates no numerical allocation and grants no source change or rerun after freeze.
