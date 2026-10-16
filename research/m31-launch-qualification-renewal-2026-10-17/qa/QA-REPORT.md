# Renewal viewer QA

## Summary

Passed 31 presentation checks in 6.121 seconds. The page shows the actual eight-case pass, seven closed owned groups and zero new scientific runs. It verifies the saved checker and all 39 checker evidence pins before revealing the result or historical replay. Corrupted evidence hides both.

## Environment

Preview: `http://127.0.0.1:8876/research/m31-launch-qualification-renewal-2026-10-17/viewer/`. Existing localhost server reused. Node 24.19.0, installed Playwright 1.62.1 and Chrome 155.0.8059.80; no dependencies installed. Browser plugin not available, so the frontend-testing-debugging skill's Playwright fallback was used. Desktop 1440×1050 and mobile 390×844 were tested. The browser run used explicitly escalated local tool execution after default sandbox localhost access was unavailable; this was display QA, not a harness/checker run.

## Checks

| Check | Result |
| --- | --- |
| Page URL/title and meaningful nonblank screen | Pass |
| Framework overlay absent | Pass |
| Actual 8/8, 7/7 and 0 result cards; 39 verified checker pins | Pass |
| Five negative and three clean case filters update visible rows | Pass |
| Caller-attested tool dispatch distinguished from saved checker evidence | Pass |
| Historical Three.js disclosure, run selection, scrub and playback | Pass |
| All seven evidence/navigation links respond | Pass |
| Desktop and mobile screenshots | Pass; visually inspected |
| Mobile page and iframe have no document-level horizontal overflow | Pass; case table intentionally scrolls within its container |
| Console errors and warnings | None |
| Six corrupted evidence/binding responses hide result and replay | Pass |

## Interaction loop

Load viewer → verify all eight saved outcomes → choose expected negative cases → observe five rows with retained original causes → choose clean cases → observe three rows → restore all eight. Open the environment disclosure and confirm that the checker cannot inspect tool dispatch. In the historical iframe choose Run B, scrub to frame 25/time 5.0 seconds, start playback and observe advancement, then pause. The replay contains 64 recorded drone bodies and no new scientific calculation.

Corruption checks used browser response interception only: the viewer binding, checker result, synthetic nonzero case report, timeout raw event file, source-publication receipt and historical viewer binding were each replaced with `{}` in a separate page. Every page hid result details, removed the iframe source and changed the headline to the failure state. No saved file was altered.

## Evidence and command path

`attempt-01/report.json` contains all 31 check outcomes. Screenshots are `attempt-01/desktop-first.png`, `desktop.png`, `mobile.png` and `historical.png`. The first viewport, mobile document and historical scene were visually inspected: text and cards are readable, controls are usable, and the historical label remains clear. `run.cjs` preserves the display-only test. It uses the installed Playwright module and Chrome supplied through environment variables; no private runtime installation paths are published here.

The flow used `chromium.launch`, page navigation, locators, select/input/click events, screenshot capture, response interception and viewport changes. The temporary scripts and captures were first produced outside the repository; their evidence copies are included in this requested closeout package. Source/result preservation was checked separately after QA.

## Remaining limits

QA covers this localhost page in the two stated Chrome viewports. It does not validate another browser, a hosted deployment, the scientific algorithms, the old failure's cause or the caller's historical launch context. The historical table, replay and original failed checkpoint retain their earlier limitations. Installing the Browser plugin is optional if future in-app browser QA is desired.
