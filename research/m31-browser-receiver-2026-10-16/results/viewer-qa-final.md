# Viewer QA

Passed on the installed Chrome155.0.8059.40 using Playwright1.62.1. Browser plugin not available. Existing static server: http://127.0.0.1:8876/research/m31-browser-receiver-2026-10-16/viewer/. Desktop1440×1000 and mobile390×844 were exercised. No dependency installation or new server was required.

Flow: load saved evidence → select recorded context/drone/color/scalar → see the corresponding retained values and Three.js view.

| Check | Outcome |
|---|---|
| Correct URL/title, meaningful page, no framework overlay | Pass |
| Console/page/network health during normal use | No errors or warnings; no HTTP failures |
| Both 1,000- and 5,000-drone contexts | Pass |
| First, last and independently located largest-error drone in each context | Four rotor rows, host force sums and error displays match retained binaries |
| All four batch summaries and 32 scalar rows | Match saved values; scalar signed error components and row-click selection verified |
| Color selection, focus/whole view, orbit interaction | Controls update state; orbit changes rendered canvas |
| Mobile layout | No page overflow; rotor table uses horizontal scrolling |
| Document/replay/footer links | All nine return HTTP200 |
| Corrupted GPU, reference, scalar-reference and pose data | Each rejected by checksum before accepting the display |

Desktop/cloud and mobile screenshots were visually inspected: scene, controls and text were readable and did not overlap. Recorded static poses are explicit, and the earlier actual Boids replay is separately linked. The viewer reads the independent-review result and refuses qualification if it is absent or failed. Force sums are host display reductions; no GPU load assembly is implied.

One UI QA invocation was used. This did not execute the scientific WebGPU receiver kernel, solve new roots, compute a new wake field or benchmark anything. Direct canvas picking and the supervisor's forced-kill path were not automated. Other browsers and device classes remain untested.

Original temporary QA script/report/screenshots remain private; disclosure copies and hashes are in public-transformations.json. The tool path is replaced in the published QA script. The relevant UI checks could benefit from the Browser plugin's in-app tooling if it becomes available, but installed Playwright supplied the recorded evidence here.
