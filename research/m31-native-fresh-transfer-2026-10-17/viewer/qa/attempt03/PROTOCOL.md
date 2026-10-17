# Focused camera QA attempt 03: harness correction only

Status: prepared; no launch without a separate explicit parent authorization of the final pins. Exactly one new attempt is proposed. No automatic retry.

Attempt 02 remains failed and unchanged. It stopped before frame/frustum checks at an aspect assertion that compared the renderer's fractional `getBoundingClientRect()` dimensions to integer `clientWidth/clientHeight`. Attempt 03 changes that assertion to use the fractional rectangle and records both fractional and integer measurements alongside the actual camera aspect. The tolerance remains 1e-10. Viewer app/scene/HTML/CSS/binding and every scientific file remain unchanged.

Other code differences are attempt identifiers/authorization guard and preservation coverage for all attempt 02 artifacts plus attempt 03 source pins. The fixed viewport, frame, force-scale, control, request, runtime, shutdown and artifact checks are unchanged. The viewer source inventory stays SHA-256 `8fefa21440399e104830171db5f83965183e183087a8ec361a2541abb02a60e5`; this attempt has a separate source inventory.

Allocation remains one attempt, **120 seconds outer wall**, **95 seconds work**, 110 seconds before direct-child termination plus at most 9 seconds fallback cleanup; **16 MiB** aggregate attempt artifacts and child per-file limit. Private profile scratch is separate. No enforced memory ceiling, hard containment or every-helper-exit claim. Use the unchanged existing localhost:8876 server and pinned installed Chrome 155.0.8059.80 / Playwright 1.62.1. Operate only the new owned Chrome root/profile. Success requires graceful Browser.close, root exit/close code 0 with null signals, reaping and profile removal; forced cleanup makes the attempt fail.

Coverage is unchanged: all 52 saved frames at desktop 1440×1050 and mobile 390×844 (104 views), both final runs/methods at scales 1/4/8 on both viewports (24 combinations), exact centers and padded body/arrow frustum checks against actual camera matrices, resize aspect/containment, playback/step/endpoint/force/orbit/reset controls, stable user camera across frames, no page overflow/errors/warnings/failed requests and only reviewed local requests. Exactly two retained screenshots, desktop.png and mobile.png, require independent parent visual inspection.

No scientific simulator, reference, native query, checker, fixture, projection builder or administrative binder executes. All frozen scientific/current-viewer/earlier-attempt evidence is checked before and after. Failed attempts remain preserved.

Dispatch uses pinned bundled Python plus RESEARCH_ROOT, RESEARCH_NODE, RESEARCH_CHROME, single-directory NODE_PATH, RESEARCH_EXECUTION_CONTEXT=tool-require-escalated and RESEARCH_VIEWER_QA_APPROVED=fresh-attempt03. The guard records explicit approval and never substitutes for it.
