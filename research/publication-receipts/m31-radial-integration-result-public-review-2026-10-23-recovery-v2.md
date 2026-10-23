# Separate environment-corrected public transport recovery v2

Outcome: incomplete/failed. This separate recovery does not change the failed/incomplete status or 160 timeout events of the first acquisition.

- Exact result commit: `8c80900fdb5de6b1cf5b3b211c8a461ecac86f1a`.
- Route: existing-gh authenticated GitHub REST Contents API with raw Accept and exact commit ref. Public visibility established: True. This is not unauthenticated raw.githubusercontent.com evidence.
- Recovered 0 of 40 files; 0 pinned bytes. All recovered files freshly matched frozen manifest, local and result-Git bytes.
- Aggregate captured stdout/stderr: 323,256 bytes of the 64 MiB cap; 0 failed API attempts.
- Limits: two concurrent transfers, two attempts per identity including metadata, 45 seconds per attempt, 900 seconds overall.
- All 29 source pins were rechecked at start/end; all four allocations remained closed.
- Original failure/incomplete records, result manifest and prospective protocol were preserved.
- No model/audit/UI execution, new statistics, archive decoding, saved-state reaggregation or frozen source/result edits occurred.

Prospective protocols:
- `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-protocol.json`: 15708 bytes; SHA-256 `ed7c52e4633731d534a770c8da18339e060fe9f7d3916bea6841d748f972c975`.
- `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-protocol.md`: 10609 bytes; SHA-256 `e1deb18cc6d95e754e908b6af986b34203ba61f44f939af112f68ead63deb31e`.

All recovery attempt events, including any failures, are preserved in `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-events.jsonl` and the JSON receipt. Captured response bodies and headers are represented by identities and a small safe-header allowlist; no credential or authorization header is recorded.

## Recovery coverage

| Repository path | Bytes | SHA-256 |
| --- | ---: | --- |

Failure: `{"errorType":"RuntimeError","detail":"recovery-file-failures:[{\"errorType\": \"KeyError\", \"detail\": \"'event'\"}, {\"errorType\": \"KeyError\", \"detail\": \"'event'\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}, {\"errorType\": \"BoundFailure\", \"detail\": \"recovery-stopped\"}]"}`.
