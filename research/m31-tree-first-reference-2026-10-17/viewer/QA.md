# Saved-coverage viewer QA

## Findings and repair

Attempt01 failed on mobile horizontal page overflow after all 32 saved-data selections passed. The source/evidence identity line had no wrapping rule. The CSS-only fix adds `overflow-wrap:anywhere` to `#identity`. The failed report, screenshot and original stylesheet/inventory remain preserved. No scientific code, result, binding, app logic or scene logic changed for the repair.

## Summary and environment

Attempt02 passed 57 checks and 32 selections, with no relevant page errors, warnings or failed requests. The reviewer inspected both retained screenshots: the 3D flock, colour legend and controls render; the narrow-screen layout wraps and the evidence table scrolls within its container. No framework error overlay was visible. The overall scientific result is established separately from this UI QA.

URL: `http://127.0.0.1:8876/research/m31-tree-first-reference-2026-10-17/viewer/`. Desktop 1440×1050 and mobile 390×844. Browser plugin not available; installed Chrome 155.0.8059.80 and Playwright 1.62.1 used with pinned Node/Chrome/Playwright components. Both attempts used a fresh owned Chrome root and private profile. Attempt02 supervisor completed in 9.803seconds; internal report 5.274seconds. These are QA durations, not performance measurements.

## Verified changes and checks

The new page colours actual saved final poses according to exact recorded coverage for one receiver/rotor. It displays all 24 planned scene outcomes and preserves a link to the earlier moving 3D replay. The selected cases are the same two airflow-off Boids records; there is no new flight simulation.

| Check | Result |
|---|---|
| URL/title and meaningful first screen | Pass |
| No blank canvas/framework overlay | Pass; screenshot inspection |
| Exact aggregate counts and all 24 rows | Pass |
| Both flocks × receivers 0/63 × rotors 0–3 × two viewports |32 selections passed |
| All 64 uploaded centers and saved membership per selection | Pass |
| Group-box hide/show | Pass |
| Orbit changes camera; reset restores view | Pass |
| Invalid selected receiver | Fails closed and clears stale geometry |
| Corrupted saved response | Hash failure before rendering |
| Console and requests | No relevant page errors/warnings/failed requests; local pinned closure only |
| Preservation |613 frozen source/evidence/viewer files unchanged |
| Cleanup | Graceful Browser.close, owned-root exit/close0, reaped and private profile removed |

Interaction path: open viewer; select A/B; select receivers 0/63 and all rotors; verify exact saved memberships/positions; change viewport; toggle boxes; drag to orbit; reset; inject an invalid selected value and a separate corrupted saved response. The fixed coverage masks are inspected, not recalculated by a scientific kernel.

Command form: bundled isolated Python `qa/attempt02/supervise.py`, with explicit RESEARCH_ROOT/RESEARCH_NODE/RESEARCH_CHROME/NODE_PATH and the tree-attempt02 dispatch tag. The supervisor starts only its reviewed Node QA child. See attempt02/PROTOCOL.md for the 120-second/16MiB allocation and precise cleanup scope.

## Remaining limits

Other browsers, devices and receivers beyond the fixed selection set were not interactively tested. The scientific validator covers all receiver/rotor queries separately. This UI check establishes neither live flight, physical accuracy nor simulation speed. Chromium's native diagnostic log in the failed first attempt contains macOS display-link/default-app messages; the page console was clean, and that attempt's recorded failure was the mobile overflow assertion. No hard memory or all-helper process containment is claimed.

## Screenshot evidence

[Desktop](qa/attempt02/desktop.png) · [Mobile](qa/attempt02/mobile.png) · [Passed report](qa/attempt02/report.json) · [Preserved failed report](qa/attempt01/report.json) · [CSS repair](history/attempt02-style.patch).
