# Original interrupted body-load campaign: viewer QA

**Result: 14 browser check groups passed after display-only fixes.** Scientific status remains failed, qualified false, with no GPU observation or field-to-body-load result. The browser review verifies an evidence viewer, not the scientific result. No generator, profile/root evaluator, shader dispatch, WebGPU compute or new scientific invocation ran.

The final run used existing Playwright 1.62.1 and installed Chrome 155.0.8059.80 in headless mode. Fallback reason: **Browser plugin not available**. No dependency was installed. The original scientific browser-version failure is preserved; using the installed browser to view saved records does not repair or rerun that campaign.

Target URL: `http://127.0.0.1:8876/research/m31-body-load-2026-10-16/viewer/`. Desktop viewport: 1440 × 1000. Mobile viewport: 390 × 844. Full-page screenshots extend beyond those heights. The existing repository server was reused and left running.

## Checked interaction loop

Open checkpoint → verify terminal outcome and final-review scope → select every original pair → inspect saved geometry and R/Q table → orbit, zoom, reset → choose all four missing families → return to controls → keyboard selection and disclosures → open historical audit and advance saved time → return → narrow viewport and horizontal table scroll → interrupt a delayed selection with a newer empty family → corrupt a selected response → reject → reload intact evidence and recover.

- All 15 pair selections matched saved R/Q policy symbols, validity masks and displayed scalars. Numeric comparisons allowed display-rounding error only. Saved receiver/source positions, axes and offset values were compared with the original16 binary. Invalid fields remained unavailable; every GPU cell remained “Not observed.” These checks neither reevaluate a physical field nor create scientific gates.
- Orbit changed canvas pixels; reset restored the baseline image. Zoom changed pixels; reset again restored it. Force-color and receiver-focus controls were hidden for pair inputs.
- All four main families displayed not executed, no receiver/rotor/body records and no scene canvas. Receiver, color, focus and reset controls were disabled. Returning to pair controls recreated the saved scene.
- Keyboard focus was visible, typing the native select label and pressing Tab selected a pair, and record/review/report/receipt disclosures opened and closed. The receipt distinguished browser-verified assets from offline-only hashes.
- Mobile layout had no document-wide horizontal overflow; controls and scene remained visible. The diagnostic table scrolled horizontally to expose its GPU column. Dense table content deliberately remains horizontally scrollable rather than compressing numerical columns.
- A response held in transit could not overwrite a newer family selection. Loading clears the readiness flag; only the completed current selection sets it again.
- Playwright response interception separately flipped one byte and removed one byte from the selected pair-position response. Both tests displayed the expected SHA-256/length failure, disabled every selector/camera control, removed the canvas, cleared records and showed an explicit unavailable state. Canonical evidence files were never edited. Removing interception and reloading restored verified controls.
- Final run had zero console warnings/errors, zero page errors and zero HTTP failures. Network requests included selected small evidence, reports and local Three modules; no full policy arrays were downloaded.

## Final review and unchanged scientific outcome

The mapped final authority is the externally observed `publication/observer-execution.json` at SHA-256 `eca5f4a3189afb3a9fcc065f51368e5b10e54ac4ac6974bf42708fce24208a4a`, using `/observedIntegrityVerified`. The UI renders “Evidence integrity verified” and scientific qualification false. The observer's candidate output and saved-review completion are retained as reports without being promoted to separate final authorities.

Bound artifact SHA-256: `975bd4ef3273150decf7f5f7e404af5e119a3929c3ce10145b9ea76fd2da3738`. Scientific result SHA-256: `7f876389a2013060cd308a51c2fea84efc6cc3e7d5cc2e2aa894c61102a4e71c`. Binding ran once and copied 10 selected assets exactly. All 13 entries listed by the raw manifest were hashed; the raw directory has 14 files because it also contains `result.json`.

## Screenshot review and visual comparison

The desktop, full-page mobile, pair 14, empty-family, corruption and recovery screenshots were opened for visual inspection. The existing coordinate-viewer reference `research/m31-coordinate-origin-2026-10-16/results/desktop-initial.png` was also inspected. The body-load viewer retains its pale blue page, large dark heading, teal links/focus, white rounded explorer and dark scene. Its sparse two-point geometry and diagnostic tables intentionally differ from the reference's recorded flock cloud.

Axis guides previously touched/clipped the top of the scene. Camera bounds now include guide endpoints and marker radii and refit on resize. Final desktop and mobile views keep the guides inside the scene. Status, legend, inspector and review scope remain readable. Empty and failed views remove unused color gradients and do not advertise unavailable scene interactions. Failure labels no longer remain at “Loading.” The mobile family option is shortened visually by the native select's width, while its complete option text remains available in the menu; the layout does not overflow.

## Historical link: failure preserved, valid existing replacement

The initial link reached `outputs/milestone-31-lab.html`, but that page's default asset `outputs/milestone-31-source/heldout-2001-5000-wide-wall-priority-0.0025.json` returned 404. Its favicon also returned 404. The screenshot and console records are preserved under `attempts/run-06/`; it was not reported as a successful historical replay.

The link now opens `research/m31-restart-2026-10-15/viewer/`, labeled “Historical M31 · local 3D Boids saved-pose audit.” Existing README/provenance describes local 3D Boids with airflow off. Its existing 3,360,000-byte snapshot binary matches SHA-256 `c9918697fc61576a9c0454cda354a8d66f42b0b6e21e082cdbf12054b372c927`. Browser loading, scene rendering, three available cases and advancing to the next exact saved time were checked. No historical data or science source was changed or regenerated; no full historical-science validation is claimed.

## Retained attempts and fixes

| Attempt | Outcome and disposition |
|---|---|
| run-01 | Local Node connection blocked by sandbox EPERM before browser launch; preserved summary; retried with authorized browser permissions. |
| run-02 | Test drag used coordinates measured before screenshot auto-scroll. Harness correction: scroll scene into view before measuring coordinates. Failure screenshot retained. |
| run-03 | Native macOS select arrow sequence did not commit a selection. Failure screenshot retained. |
| run-04 | Alternative popup key sequence also failed. A separate keyboard probe confirmed typing the option label and Tab works; later run passed. Failure screenshot retained. |
| run-05 | Mobile family return exposed stale readiness during loading. UI now sets ready false on selection start. Historical 404 also observed. Failure screenshot retained. |
| run-06 | All 13 then-current viewer groups passed; historical navigation identity passed but replay 404 remained an explicit limitation. Screenshot review prompted clearer failed/empty labels; original historical failure retained. |
| run-07 | Final 14 groups passed, including mobile table scroll and working historical saved-pose link; no console/page/HTTP failures. |

All retained attempt summaries and PNGs are byte-for-byte copies of scratch QA outputs. Private failure stacks, process/profile paths, runtime paths and test scripts were excluded. Only intended public artifacts were copied into this directory. No Git commit was made.

## Preserved evidence and limits

`PRESERVATION-CHECKS.json` confirms all 70 protected files retained size, modification time and inode; all 50 frozen source hashes, 13 listed raw hashes, six terminal report pins and 10 copied browser assets match. The raw/results `result.json` files remain byte-identical. The review/observer files were read only.

Main-family scene behavior, receiver picking/focus, receiver limits, and force/lift colors remain untested with actual campaign data because no main family ran. Scientific correctness, physical flight accuracy, timing comparisons and historical mission correctness are outside this UI QA. No synthetic substitute fixtures were created to imply these paths passed.

## Evidence files

- [Final checks](final/qa-summary.json)
- [Desktop full page](final/desktop-recovered.png)
- [Mobile full page](final/mobile-controls.png)
- [Mobile table at GPU column](final/mobile-table-scrolled.png)
- [Pair 14](final/pair-14-original-input.png)
- [Empty family](final/family-4-not-executed.png)
- [SHA-256 rejection](final/corrupt-sha256-rejected.png)
- [Length rejection](final/corrupt-length-rejected.png)
- [Working historical audit](final/historical-link-target.png)
- [Original historical missing-asset state](attempts/run-06/historical-link-target.png)
- [Final hashes and transformations](FINAL-MANIFEST.json)
- [Privacy scan](PRIVACY-CHECKS.json)
