# Viewer QA

Flow: load actual recorded loads → choose encounter/refresh interval/time/side → inspect recorded airflow arrows and load discrepancies.

Browser plugin not available; regular Playwright1.62.1 with installed Chrome155.0.8059.40. No dependency installation. Tested desktop1440×1000 and mobile390×844. Initial mobile slider was too short; stacked it full-width and tightened camera framing, then repeated all checks. Screenshots saved beside this report show the final page, without browser/account UI.

| Check | Result |
|---|---|
| Identity, content, WebGL canvas, no framework overlay | Passed |
| 2 encounters ×4 intervals ×3 times | Displayed force matches raw records |
| Initial/terminal refresh-left and ordinary sample | Passed |
| Play/pause/wrap, orbit/reset | Passed |
| Mobile layout | No horizontal overflow; usable full-width slider |
| Five evidence links | HTTP200 |
| Normal console/page/network errors | None |
| Corrupted raw data | SHA256 mismatch visibly rejected; controls disabled |

`qa.json` gives machine-readable checks. The animation uses exact sampled poses from a prescribed-path test, not integrated flight. Graphics show four measured-model receiver inflows and do not reconstruct a physical wake volume. QA confirms display behavior on one browser/device, not scientific validity or speed.
