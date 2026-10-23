# Separate public transport recovery

Outcome: incomplete/failed. This separate recovery does not change the failed/incomplete status or 160 timeout events of the first acquisition.

- Exact result commit: `8c80900fdb5de6b1cf5b3b211c8a461ecac86f1a`.
- Route: authenticated GitHub REST Contents API with raw Accept and exact commit ref; public repository visibility was checked before file retrieval. This is not unauthenticated raw.githubusercontent.com evidence.
- Recovered 0 of 40 files; 0 pinned bytes. All recovered files freshly matched frozen manifest, local and result-Git bytes.
- Aggregate captured stdout/stderr: 188 bytes of the 64 MiB cap; 2 failed API attempts.
- Limits: two concurrent transfers, two attempts per identity including metadata, 45 seconds per attempt, 900 seconds overall.
- All 29 source pins were rechecked at start/end; all four allocations remained closed.
- Original failure/incomplete records, result manifest and prospective protocol were preserved.
- No model/audit/UI execution, new statistics, archive decoding, saved-state reaggregation or frozen source/result edits occurred.

Prospective protocols:
- `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-protocol.json`: 14075 bytes; SHA-256 `ef16dcf90f737a1610f04a3765f2a3a625fb2f248685b4d1cb1ceffebf367acf`.
- `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-protocol.md`: 10482 bytes; SHA-256 `1c4ad10e5060c04ae2dc41fb9dccbc52810553a6580b225c2362496681a9479d`.

All recovery attempt events, including any failures, are preserved in `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-events.jsonl` and the JSON receipt. Captured response bodies and headers are represented by identities and a small safe-header allowlist; no credential or authorization header is recorded.

## Recovery coverage

| Repository path | Bytes | SHA-256 |
| --- | ---: | --- |

Failure: `{"errorType":"RuntimeError","detail":"two-bounded-api-attempts-exhausted:repository-metadata"}`.
