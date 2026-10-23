# Independent public result verification — composite coverage

Passed: all 2,029 declared file pins plus the result manifest have complete identity coverage. This conclusion combines the original successful checks and separately documented recoveries. The original acquisition and recoveries v1/v2 remain failed; their full records are preserved.

- Result commit: `8c80900fdb5de6b1cf5b3b211c8a461ecac86f1a`.
- Manifest: `research/m31-radial-integration-2026-10-23/result-manifest.json`; 537,067 bytes; SHA-256 `7b0871190878f7d034677beb0f23b9f995871dbdda3fdee0935cf80cb8bc2b34`.
- All 2,029 pins plus the manifest matched local and result-commit Git bytes during the original acquisition. Recovered API pins were also freshly checked locally and in the result commit.
- Fresh result-file public routes: 1,939 unauthenticated raw-GitHub checks + 2 authenticated Contents API checks from v2 + 38 authenticated Contents API checks from v3.
- The manifest was also freshly verified through unauthenticated raw GitHub. These 1,980 successful remote reads total 381,637,487 bytes.
- Fifty unchanged immutable input public/origin-Git proofs are explicitly reused from the pinned source-public receipt; they cover 222,250,897 bytes and each descriptor/local/result-Git identity was verified.
- All declared files plus the manifest account for 603,888,384 bytes. No unresolved file remains and no byte/hash mismatch was observed.

The API checks use existing-gh authentication against a repository whose exact identity and public visibility were verified in v2 metadata event 1. V3 explicitly reuses that metadata event and the two v2 file proofs; it retrieves only the remaining 38 files. API checks are not unauthenticated raw-CDN proofs.

## Preserved acquisition history

| Acquisition | Recorded outcome | Contribution and limits |
| --- | --- | --- |
| Original raw-GitHub acquisition | Incomplete; unchanged | 1,939 result pins + manifest; 50 prior input proofs reused. 160 connection-timeout attempts across 80 paths; 40 pins exhausted three attempts. At most four concurrent transfers, 10-second connection and 45-second transfer timeout. |
| Recovery v1 | Failed; unchanged | Default restricted environment; two metadata connection errors, zero file retrieval. Cause was not established by the generic error. |
| Recovery v2 | Failed; unchanged | Explicit network permission; public metadata and two files verified. A verifier event-number bookkeeping bug stopped assembly. Exact valid event proofs are recorded in the closure clarification. |
| Recovery v3 | Passed | Reviewed event-return fix; only 38 remaining files. Explicit network permission, two concurrent transfers, two attempts/file, 45 seconds/attempt, 900 seconds overall, 64 MiB capture cap. No failed API attempt; 9.542 seconds and 5,312,831 captured bytes. |

The composite JSON pins all 22 supplemental protocol, receipt, journal and clarification records and maps every file to its exact evidence events. It preserves all 162 failed transport attempts plus the v2 administrative failure. Earlier limits were not expanded, failed acquisitions were not reopened, and successful original file transfers were not repeated.

All four scientific/display allocations remained closed at the original and recovery boundaries. All 29 source pins and the final closure descriptors were rehashed after recovery and remain unchanged. No source/model/audit module execution, native query, diagnostic, archive decompression, saved-state reaggregation, new statistic, or UI launch occurred.

The source-public input receipt is `research/publication-receipts/m31-radial-integration-source-public-review-2026-10-23.json`; 152,721 bytes; SHA-256 `d311fdbfc6902383499fbcfbe9b46642087b9a08dd51111fb17cb3a0fc32a400`.

Scientific gates are quoted from the identity-verified frozen manifest: `{"cost":false,"coverage":false,"keep":false}`. This receipt establishes publication identity, not scientific validity or universal runtime equivalence.

The parent reported a successful push with a 77.08 MiB GitHub large-file advisory for queries.jsonl and successful completion of background Git autopack. The advisory was not a transfer failure.

Privacy checks found no credential token, credential authorization header or private user root in the 22 supplemental records or final receipts.

## Supplemental record inventory

| Record | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-failure.json` | 3968875 | `9a59bf5d8e38b0c060b0f4cf623ffc9a769f5085745c49c82d8fd673915292e0` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-incomplete.json` | 18924 | `a5b7da05b47bd6f12473208aa5e58b8e77e0be1d0bc00a0510bf96dc890a4002` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-incomplete.md` | 11387 | `facc74873b261573f9fcca1c7ae2bfe466f1b7a57608e35eb90b1ad7002c4bbb` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-closure.json` | 5561 | `d80ebe5acc79d98fc2d8f339978bac645a8d3bc67d80f67e26b52d97aebc0e42` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-closure.md` | 1863 | `adb47e9a409cde03499c9190df5336cc64657193db060c456440518e027cabc4` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-events.jsonl` | 1144 | `59565f440f7e77f382ad221fe4e2cb3e1ef90f612bc4126e5ba4a1a633304473` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-protocol.json` | 14075 | `ef16dcf90f737a1610f04a3765f2a3a625fb2f248685b4d1cb1ceffebf367acf` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-protocol.md` | 10482 | `1c4ad10e5060c04ae2dc41fb9dccbc52810553a6580b225c2362496681a9479d` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-closure.json` | 13058 | `8ab89f1993b653cdec24b52190494a67aee191f22569c517e336101a6dea3e4e` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-closure.md` | 1482 | `e1100570808a55fcf8d9724805f314c97ba0197ac56e6d50fd10e1714bdc507d` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-events.jsonl` | 5978 | `21aba234fdd02d29728fd713bb5ae87ded5b5028eefd92aed768fe8f011f3898` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-protocol.json` | 15708 | `ed7c52e4633731d534a770c8da18339e060fe9f7d3916bea6841d748f972c975` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2-protocol.md` | 10609 | `e1deb18cc6d95e754e908b6af986b34203ba61f44f939af112f68ead63deb31e` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2.json` | 53562 | `8d9460b59598952d9f73bd714021489c7d564edba5402cf78853d6b3a5a41ed5` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v2.md` | 4815 | `88da72223ffb3042a03d4564b740555839f7b0d2b461c97bce33f339dd81dde5` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3-events.jsonl` | 70358 | `6345cbcb9cccdfbeed7a58272d230aca42b06aaa84ec906de70e9b31759535c0` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3-protocol.json` | 23781 | `ade4e9297439f45006aa25734523d1919267612bbda087d6ba3b64e6525e359b` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3-protocol.md` | 9791 | `f845542b39b1f957964b7dc4ba41779b64d02c0deb39d866354424d1257db696` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3.json` | 140849 | `0cbc0d0634c223914464096d4780080a7a79b7d421828b217c2fd80ddad7bc72` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3.md` | 9979 | `5b3ccacf5f4fcea787d244e8f6dbd694178d3fd9355d162e10e69ebda700f140` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery.json` | 43697 | `796dfc491b9dc18e31e5019ff9b8f503dcb4806157a0eb28b424bf864c4482d4` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery.md` | 2089 | `08ec2f0288998498298ff50ad8be7e3a70f19c0f7994024a29d0c5efef0569c6` |
