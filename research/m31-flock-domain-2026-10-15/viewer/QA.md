# Viewer validation

Flow: open the domain viewer → select a flock/time/receiver → render exact saved poses and classification relationships with counts matching raw evidence.

Browser plugin unavailable; used existing Playwright1.62.1 and installed Chrome155.0.8059.40. No dependencies installed. Desktop1440×1000 and mobile390×844 tested.

| Check | Outcome |
|---|---|
| Page identity, meaningful content, WebGL canvas, no framework overlay | Pass |
| All12 snapshot domain/tilt values and first/last receiver counts/source sets | Pass against raw evidence |
| Most-retained choice, neighborhood/whole views, line toggles, orbit, next-snapshot | Pass |
| Mobile horizontal page overflow | None; table scrolls within its container |
| Normal console errors/warnings and failed HTTP requests | None |
| Corrupted raw snapshot | Rejected by checksum before controls enabled |
| Desktop, neighborhood, mobile screenshots | Visually inspected: labels, flock, colored links and metrics readable |

Screenshots retained in the local QA working area; QA metadata is results/viewer-qa.json. No browser performance or live physics inference. Direct canvas picking and browser engines other than installed Chrome are not covered by the automated interaction matrix. Evidence links are checked separately after all checkpoint documents exist.
