# Three.js evidence view QA

Final display: viewer-v2/. Both separately bounded display allocations completed once; neither may be rerun. First view passed7automated groups, but parent inspection found its arrows too small for comfortable comparison. Original viewer, source, QA and screenshots remain preserved. The separately reviewed/public-frozen v2 enlarges only arrow glyphs, uses a sparser spatial display and smaller point glyphs; scientific values and result hash are unchanged.

Environment: localhost8876, existing installed Chrome/Playwright. Browser plugin not available; existing Playwright fallback used without installation. Desktop1280×1000, mobile390×844. Flow: load → four saved-data modes → orbit/reset → mobile → corrupted-evidence refusal.

| Check | Result |
|---|---|
| Page identity, meaningful screen, no error overlay | Pass |
| Inherited gain, primary metrics, counts, three bands equal saved evidence | Pass |
| Four modes and exact saved-value sparse arrow counts | Pass |
| Orbit and reset each change rendered view | Pass |
| Desktop/mobile screenshot evidence; no horizontal overflow | Pass |
| Corrupted result rejected before3D rendering | Pass |
| Console, page and HTTP errors | None |

First display external elapsed2.2405558331s; v2 elapsed2.1855830830s, both exit0, no timeout/output cap breach. V2 source commit0fd7cde086645e72459e3ee556a70dc1c5581723,71pins publicly verified at2026-10-19T11:53:41.248232Z before launch. V2 total saved results and both display folders before closure3,654,065bytes, within32MiB. Original scientific allocations remain closed.

Parent inspected original desktop/mobile/mode captures and v2 measured/candidate/mobile scene captures. V2 measured arrows now clearly show direction and relative strength; smaller candidate arrows legitimately reflect smaller saved predictions at those sampled locations. The measurement region is planar and narrow relative to the full context; users can zoom and rotate. The rectangle outlines the selection envelope; empty areas do not imply measured zero airflow. Sparse arrows are enlarged4m per reference-speed unit, not trajectories or calibrated physical lengths. Numeric cards retain the actual saved values.

Remaining limits: only installed Chrome and two viewports checked; no validation of measured3D volume, flight trajectories or physical accuracy from UI QA. Camera glyph placement and colors are display aids. Detailed first/v2 records in ui/qa.json and ui-v2/qa.json; screenshots in the corresponding folders. No third display allocation opened.
