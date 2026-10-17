# One fresh saved-frame viewer QA attempt

Status: source prepared; launch requires the parent's explicit approval of these pins and this allocation. No browser or QA run has occurred. No automatic retry is allowed.

The attempt reads the immutable fresh-transfer saved records from source commit `b48e12ab813121fd9d65b706c08392c2a831b82e`, manifest `b089cad5f961accb6bd01ec55a32ee845403e054b4eb700bc88cc2dd48216e40`. The administrative binding is `efe52b55952a948246574bf024d949f3a39897b741de65caf231d960ae5b4be3` (5,998 bytes, 18 records/dependency files). No builder, simulator, reference, native query, checker or numerical fixture is executed during QA.

Allocation: one attempt; 240 seconds outer wall, 230 seconds before direct-child termination request, 215 seconds QA work deadline. At most 32 MiB aggregate QA artifacts, with a 32 MiB child per-file limit. No enforced memory ceiling or hard process containment is claimed. Private browser-profile scratch is transient and separate from the artifact cap. The owned Chrome root has direct exit/close listeners and a fresh private profile. Successful cleanup requires graceful Browser.close, root exit and close code 0/null signal, reaping, and profile removal. Direct-root TERM/KILL is a failure-only cleanup fallback, makes the attempt fail, and is never used on another browser. The outer supervisor acts only on its own Node child; no group signals or claim about every helper exiting.

Use the unchanged existing HTTP server at `http://localhost:8876/`; do not restart it. Use the named installed Chrome 155.0.8059.80 and Playwright 1.62.1, with selected runtime component hashes from the frozen `runtime.json` checked before launch. Browser-plugin support was unavailable for the prior adopted viewer QA; this carries forward the explicitly selected installed Chrome/Playwright path. All page requests must remain on localhost and within the pinned saved-record/dependency or viewer-file inventory.

The finite checks are:

1. Both fixed runs, each of 26 stored frames: exact saved time/index and all 64 uploaded Float32 centers, with final-only arrows. No interpolation.
2. Four final run/method selections: all 64 saved force vectors and scaled endpoints; first/last selected-drone load words and checker rows.
3. Playback, pause, single-frame stepping, initial/final selectors, method/ID selection, fixed arrow scale/toggle and camera reset controls.
4. All two target rows/four target calls and eight moving-control outcomes; separate operational/qualification cards; retained-stage failure link.
5. Desktop 1440×1050 and mobile 390×844, no page overflow, controls and wide tables accessible, local evidence links resolve.
6. One corrupted saved-generation response fails closed in a separate tab. An invalid post-acceptance fixed selection clears stale geometry and load words.
7. No unexpected page errors, warnings or failed requests; all frozen source, scientific result and viewer-source bytes unchanged before/after.

Exactly two retained screenshots: `attempt01/desktop.png` and `attempt01/mobile.png`. The parent independently inspects them after completion. The attempt also preserves STARTED/attempt receipts, report, and before/after pin inventories. A failed attempt is retained unchanged and returned to the parent without another launch.

Required dispatch environment: `RESEARCH_ROOT`, `RESEARCH_NODE`, `RESEARCH_CHROME`, single-directory `NODE_PATH`, `RESEARCH_EXECUTION_CONTEXT=tool-require-escalated`, and `RESEARCH_VIEWER_QA_APPROVED=fresh-attempt01`. Run `qa/attempt01/supervise.py` with the pinned bundled Python. Environment attestation is an execution guard, not a substitute for approval.
