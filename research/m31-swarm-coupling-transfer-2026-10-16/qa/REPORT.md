# Viewer QA

The flow under test: open the new viewer -> select all four saved snapshots -> inspect complete drone counts and admission -> change glyph magnification -> orbit/reset -> inspect mobile layout and evidence links.

Browser plugin not available. Installed Playwright with Chrome155.0.8059.80 was used against localhost127.0.0.1:8876; no dependency installed. Desktop1440×1000 and mobile390×844. The page shows byte/hash-bound saved poses and results, not a running scientific model.

Attempt1: sandboxed Chrome aborted at launch before any page checks, SIGABRT/cleanup EPERM. Raw logs retained privately; public sanitized failure and original hash are in attempt-1/report-sanitized.json. The failure was an environment launch issue, not evidence that the viewer passed. Attempt2 reran the same QA script under the authorized unrestricted local execution mode; no UI/source change intervened.

Attempt2 passed32 functional checks: identity, meaningful content, no framework overlay, explicit frozen airflow-off scope, all four selected snapshot identities and complete1000/5000-instance counts, actual/4×/8× display-size controls, visible orbit-camera change, reset, no mobile document overflow, all evidence links, and zero console/HTTP errors or warnings. report.json records each check. Screenshots desktop.png, swarm5000.png, mobile.png and mobile-scene.png were manually inspected: readable controls/labels, intact group bounds, no clipping or overlap of text, complete responsive layout. The world positions and attitudes are unchanged by display size; the swarm's recorded shape is not artificially thickened for appearance.

The display's load colors are saved source-load ratios, not measured force or physical validation. Glyphs default to4× actual size for visibility and can be returned to actual scale. Camera/renderer performance, other browsers, live flight integration and evidence-tampering negative tests were not benchmarked here. Only the selected initial/final saved records are drawn; there is no invented interpolation between times. The scientific allocation was not rerun for either QA attempt.

Command inputs: installed Node/Playwright, `RESEARCH_CHROME`, `RESEARCH_QA_OUTPUT`, qa/run.cjs. Local executable/profile paths and identifiers are intentionally excluded from public logs. Detailed browser checks do not establish scientific validity or end-to-end runtime.
