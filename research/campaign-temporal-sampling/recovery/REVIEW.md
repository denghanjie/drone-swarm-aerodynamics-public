# Independent recovery review

This is a recovery-time review, not the missing original post-run audit. No simulation, aerodynamic evaluation, replay, raw-array gate reconstruction, binary download, browser rendering, or remote write was performed.

## Finding

The recovered scientific records are internally consistent. The audit script performed 369 checks of attachment/source identities, extraction identities, saved metadata, gate-flag arithmetic, matrix counts, and all 24 report table rows for which supporting complete metadata or viewer summaries survive. All passed. The original HTML has SHA-256 `622ad9c80779dfef9434b92fc18cbc5d57c7b85a340e76a0a42dc0c2e0b54115` and is unchanged.

Both physics screens pass; both airflow-reference screens fail the velocity, attitude, and angular-rate absolute caps. Four coupled matrix rows were skipped. No cadence is qualified or physically validated. Successful supervised execution is separate from reference qualification.

The 13 direct gzip entries agree with their original Git blob IDs and sizes in uploaded tree `62e8d56e6500228cc536f6966d921697ec0bc3ad`. The four dense transport parts have the correct paths and combined sizes for two more gzip arrays. This is object-inventory verification, not a new compressed/uncompressed payload verification. Dense concatenation hashes must be checked by the reconstruction utility when the parts are available.

## Minimal honest checkpoint

1. Retain the entire existing uploaded Git tree, including its 17 binary objects, as the base. Overlay recovered artifacts; do not replace it with the incomplete local directory or the source-freeze tree alone.
2. Preserve the exact original offline HTML. It carries the surviving source material needed to independently re-extract every embedded value.
3. Restore the directly embedded JSON and decoded text/module files with explicit provenance. JSON literal slices, pretty-printed JSON, and nested-object sidecars must state their serialization method and whether original standalone bytes are known. Do not silently replace frozen source/config/plan identities.
4. Preserve the original report as historical text, with a conspicuous separate recovery addendum clarifying current gaps and stale links. Its historical complete-retention and prior-reconstruction statements are not new recovery claims.
5. Include a recovery-authored manifest connecting attachment hash, freeze commit, raw tree, recovered file hashes/source locations, derived dense sidecars, and unavailable evidence. A source-freeze file and an attachment-derived representation can be semantically equal without being byte-identical.
6. Include recovery-authored dense reconstruction directions and utility/manifest. Verify ordered part identities, combined byte length, original compressed SHA-256, and original Git blob SHA-1; preserve all parts and refuse replacement of any mismatched existing destination.
7. Include this independent review if useful. The raw literal maps are optional redundancy because the unchanged HTML plus extraction script already preserves them. A final tree audit must confirm every original raw path, mode, and blob ID remains unchanged.

The initial review was local/read-only. The parent subsequently recorded explicit retry approval and publication of raw-tree checkpoint `b9bd5065d02561920af27468f5e4740b301bd174` (tree `62e8d56e6500228cc536f6966d921697ec0bc3ad`, parent source-freeze commit) in the recovery receipt. This reviewer performed no remote writes. The metadata overlay should build on that exact retained raw tree.

## Evidence still unavailable

- Full original replay JSON for both drivers. Embedded viewer summaries/traces are partial and must not be presented as complete records.
- Full compatibility run JSON. Its work/hash summary survives; rounded timing values survive in the historical report only.
- The original standalone compatibility and two fresh-inflow sidecars. The retention manifest preserves partial metadata. Two dense sidecars survive as complete nested objects and can be extracted transparently, without an original-file-byte claim.
- The original invocation record, independent raw-reconstruction verification receipt, and browser-check failure receipt.
- The original final evidence ledger, transport manifest/reconstruction program, and pre-label-correction publication history. New recovery-authored replacements must be labeled as new.
- Other later review, QA, accounting, or checkpoint records whose exact content/names cannot be established from the recovered sources.
- Missing IPC-delimited per-job wall-time measurements were never asserted to have been logged; do not infer them from stage timers. Original supplied timing fields may be preserved, not regenerated.

The largest stated fine/coarse quadrature discrepancy and missing detailed replay metrics cannot be checked from the surviving abbreviated summaries. The historical report's raw-gate-reconstruction claim survives as prose, not as its missing independent receipt.

## Privacy and interpretation

A conservative scan of scientific records, report/README/plan text, and application code found no private absolute paths, email addresses, or common credential patterns. Vendor source was not treated as scientific/private metadata. This is a bounded scan, not a proof against every possible privacy issue.

The app differs from the frozen app only in the corrected label: “Instrumented simulation-loop wall time.” That label describes recorded elapsed loop time, not process CPU time or complete job duration. Rendering and interactivity remain unverified by this recovery.

## Reconstruction utility review

The recovery-authored utility and manifest pass review. In both modes, it verifies every raw input's exact size and Git blob identity, then streams the ordered dense parts to verify the original compressed SHA-256 and original whole-file Git blob identity. Verification-only mode writes no reconstructed outputs. Reconstruction re-verifies parts during copying, preserves input files, rejects path traversal/symlinks/nonregular files, checks all existing destinations before any output is created, and uses atomic no-overwrite installation.

The review reran 27 synthetic/metadata tests and added five independent checks, including two-output preflight failures that must leave both outputs uncreated. All passed. These are synthetic transport safety checks, not historical raw-payload verification or numerical experiments. The reviewed utility SHA-256 is `441feda779f7009ffed41ab191cbdd7b4cddac60c95de4efc23332ad7e9645fa`; reviewed manifest SHA-256 is `a298834f8152be1b71a8dfd551529e426d4493e675b396773b879dceecc8b9f3`. See `TRANSPORT-REVIEW.json`.

## Recommended minimal overlay selection

Keep unchanged frozen source/config/plan/manifest bytes from the existing tree. Add the original offline HTML, `demo/records.json`, corrected display-only `demo/app.js`, an explicitly documented display-only index correction, recovered historical report/README, and a prominent current recovery addendum. Restore the seven campaign-level results records, ten fresh run records, ten complete common-state sidecars and two transparently recovered nested dense sidecars. Include the restoration manifest, extractor and new reconstruction instructions/utility/manifest. Six full-run files also have matching fetched immutable Git objects; serialization provenance must distinguish these from unverified original-format candidates.

Unchanged vendor modules, source-freeze files and raw literal maps need not be duplicated in the overlay. The unchanged HTML plus extractor already preserves the literal-map evidence. Do not create full replay records, missing compatibility data, or unavailable original audit receipts from the summaries. Final publication should recheck all retained raw identities and make no complete-original-archive claim.
