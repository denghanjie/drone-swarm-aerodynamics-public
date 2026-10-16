# Visible replay QA

The flow under test was: open the saved-evidence page, inspect each arrangement, replay source-amplitude updates, return to final state, check rejected-input behavior, resize to mobile and follow every evidence link. Browser plugin was unavailable; installed Playwright with Chrome 155.0.8059.80 was used. Desktop 1440×1000 and mobile 390×844 were tested against the existing local 8876 server. No scientific calculation ran in the page.

| Check | Final outcome | Evidence |
|---|---|---|
| Correct URL/title, meaningful content, no framework overlay | Pass | qa/attempt-2/report.json |
| SHA256-bound records and independent-check count displayed | Pass | app binding; report |
| Four arrangement selections, saved replay and final controls | Pass | report; cycle/near screenshots |
| Rejected input disables replay, preserves two rows and6 errors | Pass | near screenshot; report |
| Camera reset and responsive layout | Pass after correction | final desktop/mobile captures |
| Console/HTTP health and evidence links | Pass, zero errors or warnings | report |

Both functional suites passed 26 checks. Manual review of attempt1 found the upper drone clipped at default zoom despite those checks. The corrected camera fits a padded bounding sphere at each viewport; attempt2 screenshots were inspected and preserve all drone centers. The first captures and report remain saved alongside the correction note. No scientific output/source was altered.

The published QA script differs from the actual executed scratch script only by replacing two runtime paths with environment variables; both hashes and transformations are saved. Run with NODE_PATH pointing to installed Playwright, RESEARCH_CHROME to an installed Chrome and RESEARCH_QA_OUTPUT to a fresh output directory. Screenshots contain only this generated research page. No browser chrome, account page, private path or external dataset figure is captured.

Untested: other browsers/devices, touch gestures on physical hardware, future evidence states and live flight. Display QA is not solver verification or rendering-performance evidence.
