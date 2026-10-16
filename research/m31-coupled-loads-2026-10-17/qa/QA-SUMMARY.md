# Saved-group 3D viewer QA

The flow under test is: open the complete-group evidence page → select a saved scene and orbit its geometry → inspect the matching load/status display; on mobile, the same content remains readable. This is display-only validation. No scientific kernel, oracle or new trajectory ran in the browser.

Environment: http://127.0.0.1:8876/research/m31-coupled-loads-2026-10-17/viewer/ . Desktop1440×1050 and mobile390×844. Browser plugin not available; existing Playwright1.62.1 and installed Google Chrome were used. No dependency was installed. The existing localhost8876 server remained running. There is no package-level Playwright workflow for this static viewer, so the small retained qa/run.cjs script exercised the page.

| Required check | Final observed result |
|---|---|
| Page URL and title |Pass |
| Meaningful nonblank content |Pass |
| Framework error overlay absent |Pass |
| Console/page health |Zero errors and warnings |
| Screenshots |Desktop, mobile, stack, tilted and unqualified scenes saved and visually inspected |
| Interaction |19 options; six representative scene changes update saved geometry/status; orbit drag changes camera state |
| Responsive layout |No outer-page horizontal overflow at390px; load table remains locally scrollable if needed |
| Evidence corruption |Changing binding, model or raw result hides the claims |
| Linked records |All nine page links returned successful responses |

Attempt01 passed41 checks in2.083s. An independent source review then found that scenes with no load certificate inherited the no-reduction color. This was an interpretation issue not caught by those checks. Its entire viewer/QA source snapshot and original report/screenshots remain under attempt-01/source-snapshot and attempt-01/.

Before attempt02, unavailable load estimates became neutral gray with an explicit unavailable legend; preparation rejection remains red. Scientific source/results did not change. The evidence binding was repinned, and a dedicated unavailable-legend check/screenshot was added. Attempt02 passed42 checks in1.879s, with no warnings/errors. Both display allocations are now closed; do not rerun either or silently add another attempt.

Visual inspection found readable desktop/mobile text, matching statuses, visible Three.js geometry, and gray unqualified geometry without force arrows or a load table. The16-drone stack is compact at its default view; orbit and zoom support closer inspection. Display rounding, marker enlargement and arrow visual scale are disclosed. This page links the historical airflow-off Boids replay; it does not embed or revalidate its motion. Browser scientific accuracy, new flight, other browsers/viewports and all scene-specific camera compositions remain untested.

Key command template: NODE_PATH=EXISTING_NODE_MODULES RESEARCH_CHROME=INSTALLED_CHROME RESEARCH_QA_OUTPUT=FRESH_ATTEMPT NODE qa/run.cjs. The script uses chromium.launch, page.goto, selector/state checks, scene selectOption, camera drag, screenshots, desktop/mobile viewport changes and three deliberately corrupted-response pages. Browser process closes in finally.

Evidence: attempt-02/report.json, desktop.png, mobile.png, group.png, mobile-group.png and unqualified-group.png. Result publication pins the source and images. All screenshots contain only synthetic research data and local viewer content, with no account UI or personal path. The Browser plugin can optionally provide in-app browser testing in future; it was not required or installed here.
