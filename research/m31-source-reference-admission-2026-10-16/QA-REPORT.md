# Display QA and source review

The finite display plan is VIEWER-QA-PLAN.md. Attempt 1 passed the data/control checks but stopped at check 46 on a browser missing-resource 404; it did not reach the corrupted-data test. The exact failing script and screenshots are retained in qa/attempt-1. The missing icon request was eliminated with an explicit data-URL favicon; the next attempt had no HTTP errors. The initial console did not record a URL, so favicon attribution is inferred from the changed request and successful rerun, not independently logged on that first request.

Root inspected the initial desktop and mobile graph screenshots and increased graph-label legibility, separating labels when curves are overlaid. No scientific values or formulas changed. Attempt 2 passed 48 checks: all table values and saved JSON, primary metrics, both unit modes across all 17 radial selections, overlay, orbit/reset, mobile layout, clean console, and refusal of same-length corrupted evidence bytes.

After independent interpretation review, the lead paragraph was clarified to say normalized center speeds; the measured quantities and display logic were unchanged. Final screenshots were captured and inspected after that text correction. The view uses Three.js to plot saved scalar profiles; display depth is not a physical coordinate. The target-units mode uses rounded tabulated scales and is explicitly an unchanged-profile transfer illustration.

Checksums bind the two data files; no scientific solver or rendering benchmark is run in the page. No performance, physical-validation or novelty claim is supported by UI QA.
