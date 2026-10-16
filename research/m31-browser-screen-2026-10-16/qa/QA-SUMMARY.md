# Recorded-results viewer QA

The final viewer passed 96 rendered check groups in installed Chrome 155.0.8059.80 through Playwright. Browser plugin not available; the installed Playwright fallback was used. No package was installed and no scientific model, campaign, control fixture or saved numerical reviewer was rerun.

Flow: load the sealed Chrome result → select each of three cases and three process repetitions → scrub all recorded frames, play/pause, scale/orbit/reset → inspect desktop/mobile → inject altered evidence and verify the page removes claims.

Environment: localhost8876, desktop 1440×1000 and mobile 390×844, headless Chrome. Three.js and controls use the existing repository-local vendor files. The existing server was left running; QA browsers closed.

| Check | Result |
|---|---|
| Correct URL/title and meaningful content | Pass |
| No blank page or framework overlay | Pass |
| Console/network health | No errors or warnings |
| Three cases and all nine case/process cost labels | Pass; exact saved summary labels and all three process rows |
| Recorded-position binding | All 858,000 coordinate components across 78 case/frame combinations match the saved pose data at renderer float32 precision |
| Playback and final-only load scope | Pass; 26 actual frames per case, no interpolation, airflow off |
| Display scale and camera controls | Pass; scale leaves recorded positions unchanged |
| Responsive layout | Desktop and mobile screenshots inspected; no horizontal overflow |
| Error handling | Altered pins, missing closure, changed timing/call counts, duplicate cases/processes, changed sealed analysis and late corrupted pose payload, missing/substituted load pins and truncated load arrays all stop the display and remove success claims |
| Evidence links | All tested links return success |

Attempt 01 passed its original 78 groups. A separate static review then found that a late selected-file error could leave the passing headline visible, and fresh presentation hashes were not anchored to the sealed scientific inventory. Exact case/process coverage also needed stronger checks. The original tested script, viewer snapshot, report and screenshots are preserved under attempt-01.

The presentation fix clears the headline/lead on error, verifies stage/audit/analysis/closure pins against qualification.inputs, verifies selected generation/pose/load/evidence pins against the sealed reviewRun inventory, binds configuration to the frozen source manifest, and requires exact case/process coverage. Attempt 02 added the relevant fault checks and passed all 90 groups. A final static supplement identified an optional-load-pin gap. The page and derivation now require the exact case-specific p0/L load pin, record identity and array length. Attempt 03 added missing/substituted/truncated load faults and passed all 96 groups. The final derivation missing-generation guard and load identity guards were exercised by successful display generation before this final rendered run. No raw scientific records or frozen source files changed.

Evidence: attempt-03/report.json, desktop.png, swarm5000.png, mobile.png, mobile-scene.png, late-evidence-error.png; qa/run.cjs is the final test script. The independent static review and supplemental resolution note are in review/. Screenshots contain rendered research content only, with no OS/account UI.

Remaining limits: one Chrome build on one machine and two viewport sizes; no cross-browser, accessibility, touch-device or live-flight performance qualification. This viewer proves presentation behavior and record binding, not the physical validity of the model or universal integrity against an attacker replacing the entire publication.
