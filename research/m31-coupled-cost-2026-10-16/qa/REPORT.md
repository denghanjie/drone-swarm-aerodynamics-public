# Viewer QA

Updated surface: `/research/m31-coupled-cost-2026-10-16/viewer/`. Shows PermissionError/no usable timing coverage and retains clearly labeled prior saved swarm poses/load colors. No scientific kernel runs in the page.

Flow: load page → verify failure scope and0/140coverage → select all four snapshots → change glyph scale → orbit/reset → mobile layout → evidence links. Browser plugin not available; existing Playwright/Chrome used with approved host execution. Chrome155.0.8059.80; desktop1440×1000, mobile390×844. No installation. QA is outside all scientific allocations.

| Check | Outcome |
|---|---|
| Identity, meaningful screen, no framework overlay | Pass |
| Permission failure, unknown operation and prior-data labels | Pass |
| All4snapshots and actual1000/5000instance counts | Pass |
|1×/8×glyph scales, orbit image change, reset | Pass |
| Mobile width, evidence links, console/HTTP health | Pass |

35checks passed; zero console warnings/errors and failed HTTP responses. One QA invocation, no code repair/rerun after it. Raw report and four screenshots retained in attempt-1. Desktop full page and mobile scene were manually inspected: readable labels, visible3Dgroup, no overlap or horizontal clipping. No unrelated desktop or private browser content captured. See desktop.png, swarm5000.png, mobile.png, mobile-scene.png. These demonstrate UI behavior, not simulation accuracy or runtime performance.

Command shape: `NODE_PATH=BUNDLED_MODULES RESEARCH_CHROME=INSTALLED_CHROME RESEARCH_QA_OUTPUT=PRIVATE_QA_DIR node PRIVATE_QA_SCRIPT`. Script and public report copied without changing content; screenshots show the local artifact only. Other browser engines/devices, scientific child processes and physical behavior remain untested by this QA.
