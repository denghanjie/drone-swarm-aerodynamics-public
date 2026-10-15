# Viewer verification

Flow: open fixed-state order viewer → choose a saved flock and drone → compare measured request arrows and original neighbors.

Browser plugin not available; used Playwright 1.62.1 and installed Chrome 155.0.8059.40. No dependency installation. URL path: `/research/m31-diagnosis-2026-10-15/viewer/`. Desktop 1440×1000 and mobile 390×844.

| Check | Result |
|---|---|
| Identity, meaningful screen, canvas, no framework overlay | Passed |
| Both cases, four selected IDs in each, largest-effect selection | Passed against saved data |
| Both camera buttons, three arrow toggles, orbit | Passed by rendered-image changes |
| Console, page errors, HTTP failures | None on normal page |
| Mobile overflow | None |
| Five footer evidence links | HTTP 200 |
| Missing data | Visible error; controls remain disabled |

Visual inspection of the focus and mobile screenshots confirmed readable controls and visible selected-drone arrows. Screenshots are page-only and stored beside this report. `qa.json` records the checks. Shader appearance and interactions were checked on one Chrome/Apple M4 system; this is not a browser-performance, physical-validation, or live-simulation test. The earlier proposed distant focus was tightened before these checks.
