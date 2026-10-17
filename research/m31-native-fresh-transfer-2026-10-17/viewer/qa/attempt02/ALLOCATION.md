# Explicit parent authorization: focused attempt 02

The parent authorized exactly one focused camera-fit viewer QA attempt against the reviewed source hashes below. The limit is 120 seconds outer wall and 16 MiB aggregate attempt artifacts. No scientific imports/calls, source rebinding or automatic retry is authorized. All earlier evidence, including attempt 01 and its original viewer-source snapshot, must remain unchanged.

Accepted SHA-256 pins:

- `PROTOCOL.md`: `738299b81d2b398eefa74708c99d014f546cf3cf5d6bfaa64e5d3df2b5258a76`
- `run.cjs`: `a59b661fc38eb322f8f23a08cf2c1db7e89cb9eff42388eec15b1d3b89f52ea6`
- `supervise.py`: `4208072424cb9c0922f526ad343221fb76b37acf1a63de74c23adb39a06d8231`
- Current viewer `SOURCE-PINS.json`: `8fefa21440399e104830171db5f83965183e183087a8ec361a2541abb02a60e5`

Dispatch uses explicit escalation, the frozen installed runtime pins, a fresh private profile and owned Chrome root, and the existing localhost:8876 HTTP server without restarting or changing it. Success requires graceful Browser.close, root exit and close code 0/null signal, reaping and profile removal. A failure remains preserved and no further launch follows automatically.

The environment guard `RESEARCH_VIEWER_QA_APPROVED=fresh-attempt02` records this authorization; it does not replace it. This allocation was recorded before launch. The parent will inspect the two resulting screenshots independently of the automated frustum checks.
