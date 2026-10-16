# Source-only status display QA

Flow: open the current checkpoint → see accepted source review and eight unexecuted cases → select/scrub/play the historical Boids flight → retain the distinction between historical data and unexecuted qualification.

Browser plugin not available; used existing Playwright and Chrome without installing dependencies. Display-only attempt01 passed all24 checks in4471ms. No harness, checker, simulator or new force calculation was invoked by QA. The historical iframe's scientific contents are unchanged.

| Check | Result |
| --- | --- |
| Correct URL/title; meaningful content | Pass |
| Source review vs runtime outcome separation | Pass |
| Eight cases all NOT RUN; timing explanation | Pass |
| Historical disclosure and replay controls | Pass |
| Framework overlay | None found |
| Browser errors/warnings | None recorded |
| Desktop1440×1050 and mobile390×844 | Pass; no horizontal overflow |
| Four deliberately corrupted display resources | Details and replay hidden in every case |
| Navigation | All visible links respond successfully |

The parent inspected desktop.png and mobile.png visually. The source-only page, historical controls and drone canvas are present and legible. Evidence is in attempt-01/report.json and its two screenshots; the reproducible display driver is run.cjs. Execution used the already installed runtime with NODE_PATH, RESEARCH_QA_OUTPUT and RESEARCH_CHROME environment variables. No host paths are embedded in the driver.

This QA verifies presentation and a few unchanged historical controls. It does not rerun the prior exhaustive saved-position comparison, recompute attitudes/forces, exercise the proposed operational harness or establish scientific validity. Other browsers/devices remain untested. A dedicated Browser plugin could improve integrated inspection in future UI work; it was not installed here.
