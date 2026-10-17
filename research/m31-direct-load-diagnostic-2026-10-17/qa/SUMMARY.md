# Direct-load saved-data viewer QA — 2026-10-17

The final bounded browser attempt passed all **761 checks in 8.545 seconds**, with **zero console/page errors and zero warnings**. All three authorized browser attempts are retained. No additional browser attempt was made after this pass.

This is presentation and saved-data binding QA. It made no scientific imports, solver/checker reruns, builder reruns, candidate changes, or frozen-data edits. The parent had already built the accepted display data once. QA used the existing local server without starting or changing it.

## Environment and coverage

- Installed Chrome **155.0.8059.80**, headless through Playwright **1.62.1**, with background networking disabled. This was the authorized local fallback after Browser/IAB was unavailable.
- Desktop viewport **1440 × 1050**; narrow viewport **390 × 844**. The narrow test resized desktop Chrome; it does not establish behavior on physical phones, touch input, mobile Safari, or other browser engines.
- All **36** combinations of six saved snapshots, two candidates, and three tolerance tiers: **2,304** rendered bodies, **6,912** center-coordinate components, and **1,008** link endpoints checked across these combinations.
- All **12** overview projections of four load categories and three tiers, retaining all six rows and comparing the displayed statuses, normalized errors, and exact-interval tooltip data with the saved results.
- Actual Float32 overlay uploads and actual WebGL line draw counts checked against the saved positive-term masks: A0 **39**, A5 **26**, A10 **20**, B0 **40**, B5 **26**, B10 **17**. Full-control overlays are empty and C is explicitly not applicable for that control.
- Orbit, zoom, reset, overlay hiding, stale-link clearing, desktop and narrow-screen controls, horizontal table scrolling, page identity, evidence binding, and corrupted-binding/corrupted-data rejection checked.

## Retained attempt history

| Attempt | Recorded checks | Elapsed | Outcome |
|---|---:|---:|---|
| [01](attempt-01/report.json) | 738 | 6.860 s | Failed exact whole-PNG reset comparison after all 36 combinations and 12 projections. |
| [02](attempt-02/report.json) | 759 | 8.887 s | Functional, narrow-screen, and corruption checks passed; one missing-favicon console error failed the final console check. |
| [03](attempt-03/report.json) | 761 | 8.545 s | Passed, including zero errors/warnings and preservation checks. |

Each attempt retains its report, screenshots, viewer-source snapshots, run-script snapshot, and immutable-before/after records. Failed attempts remain failed; their reports and screenshots were not rewritten.

The reset-test correction is documented in [RESET-COMPARISON-NOTE.md](RESET-COMPARISON-NOTE.md). Exactly 942 of 424,842 pixels differed, entirely in the one-pixel top clipping boundary of the 942 × 451 element screenshot. All **422,060 interior pixels were exactly equal**. Later attempts require that exact interior equality and retain the full-image difference statistics. No screenshot was edited, and no pose, endpoint, status, interval, GPU-upload, or draw-count check was weakened.

The sole viewer repair was an **inline SVG favicon in `viewer/index.html`**. A read-only request confirmed that Chrome's default `/favicon.ico` request returned 404. The inline favicon removed this request; attempt 03 then had no console errors. `app.js`, `scene.js`, `style.css`, and `build-binding.py` are byte-identical to the attempt-01 source snapshots. Built binding and display data are unchanged.

A shell launcher typo before attempt 03 returned exit code 127 because the selected Node executable path did not exist. The QA program did not start and that command did not create attempt-03. The corrected executable launched the third and final browser attempt. [launcher-before-attempt-03.txt](launcher-before-attempt-03.txt) is a clearly labeled transcription of that operational tool output, with its home path redacted; original/public hashes are recorded in the privacy manifest. It was not a fourth browser attempt.

## Screenshot inspection

All **15 final-attempt PNGs** were opened and visually inspected: the desktop first viewport, strict and stress overviews, selected error table and overlay, the narrow first viewport and overlay, both horizontal ends of the narrow table, before/orbit/zoom/reset canvases, and both corruption screens. Text and statuses are readable, failure/certificate distinctions are visible, and the rendered amber links are present. Orbit and zoom visibly change the scene; reset restores its framing and content. Both corrupt-evidence screens disable controls, show an empty scene, and explicitly refuse to accept saved evidence.

The overview screenshots are viewport captures, so some lower rows fall below the image edge; the following detail view shows the continuation including B10. Narrow-table captures show its top portion and both horizontal ends. DOM assertions independently verify all six rows and horizontal scrolling. The page uses normal vertical scrolling, with no unexpected horizontal page overflow or selection-based row filtering. Screenshots alone are not claimed to show every row simultaneously.

## Scientific interpretation preserved

The saved computation's **integrity pass** is distinct from **A accuracy decisions** and from **B/C certificate sufficiency**. Full control A/B passes the strict tier for all six states. Omission A definitely fails the strict and 1e-4 tiers for all six. At the 1e-2 stress tier, omission A fails A0/B0 and passes the other four; B/C certify only A10/B10. A B/C “Not certified” result means that the upper bound is too wide and does not establish measured force inaccuracy.

The scene reuses the prior normalizer-replication poses at exactly 0, 5, and 10 seconds from airflow-off flights. Amber links depict omitted-coefficient bookkeeping, not wake streamlines or force vectors. The saved candidate loads are oracle-assisted post-hoc calculations. This QA supplies no live-physics, speed, physical 1% accuracy, flight-safety, or 5,000-drone feasibility claim.

## Preservation and operational privacy

[FINAL-PRESERVATION.json](FINAL-PRESERVATION.json) records a fresh administrative byte/hash comparison against [IMMUTABLE-BEFORE.json](IMMUTABLE-BEFORE.json): **all 159 frozen pins and all four accepted result files are unchanged**. It also verifies the source-manifest digest, all 22 viewer evidence pins, the accepted binding/display digests, and the narrowly limited viewer-source change.

Accepted display: **220,047 bytes**, SHA-256 `4da9f4965d686f04ef1ac082cdd6e01a5f7054684c03ea43ea7eb37e895ea9ad`. Accepted binding SHA-256: `286d6b3d49acf01cdd594f6a42f46961ad0dd4258682b1e23e7c2ee045d2f970`. Source commit: `ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf`. Source-manifest SHA-256: `93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b`.

After QA, the public `run.cjs` and all three attempt script copies received one limited privacy replacement: the operational redactor's personal home fallback became `[HOME_UNSET]`. Every other script byte is preserved. The original executed script bytes and original operational launcher transcription are retained privately outside the repository, with exact locations in a private manifest only. [PRIVACY-SANITIZATION.json](PRIVACY-SANITIZATION.json) contains public original/sanitized byte counts and SHA-256 hashes. These sanitized script snapshots were not rerun; reports, screenshots, viewer files, built JSON, and scientific files were not changed by sanitation.

[ARTIFACT-MANIFEST.json](ARTIFACT-MANIFEST.json) lists the byte count and SHA-256 of every public QA artifact except itself, after sanitation and closeout. It is a saved-artifact inventory, not a new scientific result.
