# Boids result complete locally; public publication pending

The scientific, saved-data audit, UI and archive allocations are closed. Do not rerun them. The final independent review and final 100-file manifest/index check passed.

Result commit: `637c25294f162bea39970d12df0206f25dead889`.
Result manifest SHA-256: `a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b` (20,563 bytes, 100 pins).
Final independent review: `research/m31-boids-admission-2026-10-20/review/RESULT-REVIEW.md`.

## Publication failure

Six upload attempts failed: ordinary SSH, SSH with keep-alives, HTTPS, HTTPS with a larger replay buffer, a 96 MiB archive-only batch, and a final 32 MiB archive-only transfer. Observed errors included `Can't assign requested address`, `Broken pipe`, and `unexpected disconnect`. The HTTPS client also reported `unable to rewind rpc post data`; increasing the buffer did not resolve the connection failure. No auto-review rejection occurred.

Two successful remote-ref reads during recovery still showed `94af0e9f9269183e408b5ce22d220329bf103770` on `codex/m31-audit-2026-10-15`. The second read reported no `codex/m31-evidence-transfer-2026-10-20` branch. The final remote-ref read itself failed to connect, so the final remote state is unconfirmed. No successful upload or exact-public result receipt exists. Do not label this result published.

The reviewed result commit and files remain unchanged. Temporary archive-only transport commits were created locally without checking out or changing the research branch. Attempts to publish temporary commits `192a8d614a56a443c0fe2d2ff71100d532eefa95` and `14bdd0cc9965a9fba8bf9ce0293c64d786363870` returned failure. These contain only already-reviewed archive parts, not new scientific results. No temporary branch should be treated as a research checkpoint.

## Resume publication only

1. Confirm the clean working tree and read the result manifest, review and this handoff. Inspect actual remote refs before retrying.
2. Push the unchanged result commit (and this separate handoff commit) to `codex/m31-audit-2026-10-15` once connectivity permits. Preserve history; do not force-push or alter frozen evidence.
3. Independently retrieve the exact-commit public `research/m31-boids-admission-2026-10-20/result-manifest.json` from commit `637c25294f162bea39970d12df0206f25dead889` over verified HTTPS. Compare its bytes and SHA-256 with the local manifest. Verify each manifest file against both local bytes and the committed blob. Record the distinction between a fetched remote manifest and a full remote binary download.
4. Save the successful receipt as `research/publication-receipts/m31-boids-admission-result-2026-10-20.json`, privacy-check, commit, push, and verify its public identity.
5. If the temporary transfer branch exists, delete only that task-created branch after successful final publication; do not delete any scientific branch.

No new numerical allocation is opened. All four original journals remain locally intact and exactly reconstructible from the 18 pinned archive parts. Keep localhost 8876 available; the recorded Three.js replay is `research/m31-boids-admission-2026-10-20/viewer/`. Follow `RESTART-RESULT.md` only after resolving the publication gate. The broader research goal remains incomplete.

Recorded UTC: 2026-10-20T10:51:47.562519+00:00
