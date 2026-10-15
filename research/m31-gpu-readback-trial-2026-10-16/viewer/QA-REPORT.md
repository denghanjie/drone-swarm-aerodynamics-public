# Presentation QA

The recorded failure view loads and shows the actual missing-data state. The Three.js canvas and word/comparison/event/reset controls work in the observed desktop/mobile views. Browser plugin not available; used installed Playwright1.62.1 and dedicated Chrome with the existing8876server. No diagnostic or saved checker was invoked.

Flow: load the saved view → select saved-versus-expected comparison → choose word31 → inspect unavailable actual bytes and the fixed reference → inspect the sole launch-intent event → reset camera. All11checks in qa-2/report.json pass: identity, meaningful content, binding/no overlay, canvas, failure display, comparison, word, event, reset, mobile overflow and console health. Zero observed console errors/warnings. Viewports1440×1100 and390×844.

The initial run stopped at a test assertion expecting “—” in the word-summary sentence; the application intentionally says “unavailable” there and uses “—” in the table. Correcting only the test made it pass. qa/report.json and its screenshot are retained. The immediate viewport-resize mobile capture appeared to contain a stale compositor fragment; a fresh mobile viewport after layout frames showed one header and correct layout. qa-mobile records that check. Root inspected desktop, selected-word, fresh-mobile and mobile-scene screenshots. No presentation source was changed after QA began.

Measured execution durations:2.206429625+1.949919875+1.197118875=5.353468375seconds, within the shared60second presentation execution cap. All retained screenshots/reports fit the12MiB cap. This is presentation timing only; no simulation or rendering-speed claim follows. Rendering, browser availability and digest matching do not establish scientific validity.

Key APIs: chromium.launch, page.goto, waitForFunction, locator.selectOption/click, screenshot, setViewportSize, console/pageerror capture, browser.close. Existing source modules passed Node syntax checks. Unchecked: successful actual-byte states, other browsers, screen readers and arbitrary display sizes.

Screenshots: qa-2/desktop.png, qa-2/word-detail.png, qa-mobile/mobile-settled.png, qa-mobile/mobile-scene.png. The preserved initial mobile capture is not used to assert final layout.
