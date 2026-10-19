# Display verification

## Result and environment
Corrected viewer-v2 passed 8 check groups. Original viewer failed mobile horizontal overflow after 5 groups; its failure and screenshots remain intact. No retries of either allocation. Existing Playwright/Chrome used because Browser plugin was not available; no installation. Local 8876, desktop 1280×1000 and mobile 390×844.

## Verified changes
The documentary panel has four source dispositions. The 3D scene displays historical coordinates and missing-core coverage, with highlight toggle, orbit and reset. v2 changes only responsive CSS; app logic and evidence pins are byte-identical to v1. Research conclusions are unchanged.

| Check | v1 | v2 |
|---|---|---|
| Public source/pins and page identity | Pass | Pass |
| Meaningful historical3Dscene and saved counts | Pass | Pass |
| Four source explanations and links | Pass | Pass |
| Coverage toggle, orbit/reset | Pass | Pass |
| Desktop overflow | Pass | Pass |
| Mobile overflow | Fail | Pass |
| Altered ledger/result/audit refusal | Not reached | Pass |
| Final console/page/HTTP health | Not reached | Pass |

No framework error screen was visible in parent-inspected screenshots; this is a plain static page, not a framework app. No claim about all browser warnings is made.

## Interaction path and evidence
Load → select each of four sources → toggle historical point highlighting → drag orbit → reset → mobile layout → separately intercept ledger, result and audit with invalid content and confirm refusal before scene creation. Checks compare saved identities and labels; they do not recompute scientific values. QA is not physical validation.

Source entry points: source/ui.cjs and source/ui-v2.cjs, each run once by its separately locked supervisor. v1 exited 1 in 2.052438 seconds; v2 exited 0 in 2.114400 seconds. Both stayed within monitored time/output cutoffs. These times are display-check durations, not simulation speed measurements.

Parent inspected desktop, mobile-top and mobile-scene screenshots for both versions. v1 visibly extended offscreen on mobile; v2 fits with wrapped controls. Screenshots contain only project content. Saved evidence: ui/qa.json, results/ui-supervisor.json, ui-v2/qa.json, results-v2/ui-supervisor.json and the corresponding PNGs. No untested corrupt-input paths are credited to v1.

## Limits
One installed Chrome build and two viewports tested. No physical calibration, additional browser/device coverage, live drone flight, new wake animation or new component dataset. Documentary source links were checked against the ledger, not fetched again in the browser check. User-requested committed records include this report and screenshots.
