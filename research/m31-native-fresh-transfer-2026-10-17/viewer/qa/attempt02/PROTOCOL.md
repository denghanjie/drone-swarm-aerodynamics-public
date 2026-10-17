# Focused camera-fit QA attempt 02

Status: source prepared only. Launch requires a separate explicit parent authorization of the new source pins. Exactly one attempt is proposed; no automatic retry.

Attempt 01 remains unchanged. Its exact app, scene, HTML, CSS, binding and source inventory were preserved under `../attempt01/original-viewer-source/` before editing. Attempt 01 passed its functional checks but its mobile screenshot clipped the final B swarm. This focused attempt validates the narrow camera repair; it does not rerun the scientific experiment or duplicate the earlier integrity/link/load audit.

The camera now fits one padded envelope for the complete selected run's saved trajectory and final force endpoints at the selected scale. Its distance uses the narrower horizontal/vertical field of view. Run, method, scale and viewport changes refresh the fit; playback frames retain the camera. Reset fits the complete envelope. No saved pose, load, scientific source or numerical output was changed.

Allocation: one attempt, at most **120 seconds outer wall**, **95 seconds work**, 110 seconds before direct-child termination, then at most 9 seconds fallback cleanup. Aggregate attempt artifacts and child per-file output limit: **16 MiB**. No enforced memory ceiling, hard process containment or every-helper-exit claim. Private browser-profile scratch is separate from this artifact cap. Only the new owned Chrome root/profile may be operated on. Successful completion requires graceful Browser.close, root exit and close code 0/null signal, reaping and profile removal. Direct-root TERM/KILL is failure-only cleanup and makes the attempt fail. The supervisor signals only its owned Node child, never a process group.

Use the existing localhost:8876 server unchanged, installed Chrome 155.0.8059.80 and Playwright 1.62.1. Runtime component byte hashes are checked against the unchanged frozen runtime metadata before launch. This continues the adopted regular Chrome/Playwright path. No scientific modules, simulator, reference, native query, checker, fixtures or administrative binder are executed.

Focused checks:

1. Both recorded runs, all 26 frames each, at desktop 1440×1050 and mobile 390×844: 104 views. Check exact saved centers, camera stability between frames, and all glyph bounds inside the actual camera frustum using exposed projection/view matrices and independent homogeneous projection.
2. Both final run states, both F/L methods, scales 1/4/8, both viewports: 24 combinations. Check unchanged actual force vectors/endpoints plus padded arrow bounds inside the actual camera frustum. Also verify immediate resize containment and canvas aspect.
3. Initial/final/step/play/pause, force toggle, manual orbit, frame changes preserving the user camera, and reset restoring the full-run fit. No page overflow or unexpected page errors, warnings or failed requests; only reviewed local requests.
4. Exactly two retained screenshots: `desktop.png` and `mobile.png`, with fitted final F forces at scale 4. Parent visual inspection remains separate from automated checks.
5. Verify all frozen scientific sources/results, current viewer files, and all preserved attempt 01 evidence before and after. Keep this attempt's receipts/report/screenshots whether successful or failed.

Dispatch with the pinned bundled Python and `RESEARCH_ROOT`, `RESEARCH_NODE`, `RESEARCH_CHROME`, single-directory `NODE_PATH`, `RESEARCH_EXECUTION_CONTEXT=tool-require-escalated`, and `RESEARCH_VIEWER_QA_APPROVED=fresh-attempt02`. The guard is not a substitute for explicit parent authorization.
