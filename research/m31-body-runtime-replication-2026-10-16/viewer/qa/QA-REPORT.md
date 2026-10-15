# Runtime replication viewer QA

**Passed: 17 browser verification groups.** The page displays the submitted pair dispatch and missing GPU output, while scientific qualification and saved-review integrity remain false. No scientific host, generator, root/profile evaluator, GPU compute or review checker was executed.

Environment: existing local server at `http://127.0.0.1:8876/research/m31-body-runtime-replication-2026-10-16/viewer/`; Chrome 155.0.8059.80; Playwright 1.62.1; desktop 1440×1000 and mobile 390×844. Browser plugin availability: absent. Fallback reason: **Browser plugin not available**. No installation or new server was required.

| Required check | Result |
|---|---|
| Page URL/title and meaningful content | Passed |
| No framework overlay | Passed |
| Console warnings/errors, page errors, HTTP failures | 0 / 0 / 0 / 0 |
| Actual saved pair controls | All 15 passed: geometry, CPU R/Q diagnostics, validity and absent GPU output |
| Actual scalar controls | All 146 passed: 292 R/Q records, all scalar raw bits, validity and status fields |
| Signed-zero/invalid coverage | 6 signed-zero reference fields and 170 invalid reference fields retained |
| Main families and absent GPU/H | Four empty families; no invented geometry or values |
| Final authority mapping | Actual failed review shown separately; `/observedIntegrityVerified` remains false |
| Interaction | Native keyboard selection, orbit/zoom/reset, disclosures, historical saved-pose audit |
| Mobile | Controls visible, no page overflow, diagnostic table horizontally scrollable |
| Stale response and corruption | Cancellation, pair/scalar SHA and length rejection, disabled failure controls and cleared records, recovery |
| Request audit | No scientific-source or policy-array request |

Flow: runtime checkpoint → fixed pair selection → saved CPU diagnostics and original geometry → scalar controls without geometry → four empty families → saved reports/failed review → separate historical saved-pose audit. Every selected pair and scalar was checked against its exact saved JSON/binary bytes; only byte decoding and display comparisons were used.

The final desktop, pair, scalar and mobile screenshots were inspected. The page separates the unavailable GPU values, empty main families and failed review. Full-page mobile screenshots are tall; the diagnostic table intentionally scrolls horizontally. The final screenshots are in `final/` and include recovery/failure states. `final/qa-summary.json` preserves all checks, request paths, artifact pin and screenshot hashes.

## Retained failures and corrections

The first binder invocation stopped before copying anything: the privacy matcher misread the public phrase `directory/private/pipe` as an absolute path. Requiring a path-leading boundary corrected the false positive while retaining private absolute-path and evidence-endpoint rejection. The second invocation succeeded; evidence was not rewritten.

Browser attempt 01 passed page, disposition, pair and camera checks, then its test harness read a collapsed scalar disclosure with `innerText`, yielding empty JSON. The harness now reads `textContent`. No viewer behavior changed for that correction. Attempt 02 passed all 17 groups. Attempt 01's summary and screenshots are retained under `attempts/run-01/`; private stack traces remain outside the repository.

The public `regression.cjs` differs from the scratch harness only by removing the private default Playwright module path and requiring an explicit new scratch output directory. Set `M31_VIEWER_QA_AUTHORIZED=1`, the exact final review hash in `M31_QA_FINAL_REVIEW_SHA256`, `M31_QA_URL`, `M31_QA_OUTPUT` and optionally `M31_QA_PLAYWRIGHT`, then run the harness with Node. It refuses an unbound artifact or different final authority. No tests import scientific code.

## Preservation and limits

`PRESERVATION-CHECKS.json` verifies 114 protected files with unchanged lengths, SHA-256, modification times and inodes, all 57 frozen science pins, all 21 raw manifest entries, 26 bound browser assets and 69 predecessor viewer pins. The final manifest records the exact viewer package. Preparation-stage ledgers remain historical prebinding records.

Main-family receiver picking, all-receiver displays, force/lift color modes and saved GPU/H numerical paths remain untested because their actual evidence is absent. No substituted fixtures were used. No claim about scientific correctness, physics, timing, unseen browsers or real flight follows from UI QA. The scientific run failed, and the sole saved review failed; neither was repeated or repaired by these checks.
