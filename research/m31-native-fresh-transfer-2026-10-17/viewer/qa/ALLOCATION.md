# Explicit parent allocation: fresh viewer QA attempt 01

The parent explicitly authorized exactly one viewer-only QA attempt, under the reviewed `PROTOCOL.md`, with no scientific imports or execution and no automatic retry. A failed attempt must remain preserved and be returned to the parent. This allocation does not authorize republication or modification of scientific files.

Accepted SHA-256 pins:

- Protocol: `e6b57bc83141a6f02277a58650755017d10995d14b53031eff8b92d3acdec3d7`
- `attempt01/run.cjs`: `e500d1cff081f08061f9a4792800f847744cd4afc22f982bf7a1b4ee834930fb`
- `attempt01/supervise.py`: `68a46b32c370a4866890d557a586e3000640ba2e916d54a3716b53b071256c92`
- Viewer `SOURCE-PINS.json`: `306adddab065b9db39ac869407c09ac4e5ed834dd55860ba06b560c98f8316f7`
- Viewer binding: `efe52b55952a948246574bf024d949f3a39897b741de65caf231d960ae5b4be3`

The approved allocation is one attempt, 240 seconds outer wall, 215 seconds QA work, and 32 MiB aggregate QA artifacts, using the installed pinned Chrome 155.0.8059.80 with Playwright 1.62.1. The existing localhost:8876 server (observed PID 48039) must remain untouched. The attempt owns only its new browser profile and spawned Chrome root. Successful cleanup requires graceful close and root exit/close code 0 with null signal; forced cleanup makes the attempt fail. Two screenshots are retained for the parent's visual inspection.

The dispatch must use explicit escalation and the reviewed execution guards. The environment guards record this authorization but do not replace it. This allocation was written before launch; the execution receipt records the actual start and outcome.
