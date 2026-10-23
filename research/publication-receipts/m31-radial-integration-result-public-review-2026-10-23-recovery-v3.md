# Separate environment-corrected public transport recovery v3

Outcome: passed. This separate recovery does not change the failed/incomplete status or 160 timeout events of the first acquisition.

- Exact result commit: `8c80900fdb5de6b1cf5b3b211c8a461ecac86f1a`.
- Reused prior v2 public metadata and two file proofs explicitly; no metadata or two-file duplicate network retrieval.
- Route: existing-gh authenticated GitHub REST Contents API with raw Accept and exact commit ref. Public visibility established: True. This is not unauthenticated raw.githubusercontent.com evidence.
- Recovered 38 of 38 files; 5,256,772 pinned bytes. All recovered files freshly matched frozen manifest, local and result-Git bytes.
- Aggregate captured stdout/stderr: 5,312,831 bytes of the 64 MiB cap; 0 failed API attempts.
- Limits: two concurrent transfers, two attempts per identity including metadata, 45 seconds per attempt, 900 seconds overall.
- All 29 source pins were rechecked at start/end; all four allocations remained closed.
- Original failure/incomplete records, result manifest and prospective protocol were preserved.
- No model/audit/UI execution, new statistics, archive decoding, saved-state reaggregation or frozen source/result edits occurred.

Prospective protocols:
- `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3-protocol.json`: 23781 bytes; SHA-256 `ade4e9297439f45006aa25734523d1919267612bbda087d6ba3b64e6525e359b`.
- `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3-protocol.md`: 9791 bytes; SHA-256 `f845542b39b1f957964b7dc4ba41779b64d02c0deb39d866354424d1257db696`.

All recovery attempt events, including any failures, are preserved in `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23-recovery-v3-events.jsonl` and the JSON receipt. Captured response bodies and headers are represented by identities and a small safe-header allowlist; no credential or authorization header is recorded.

## Recovery coverage

| Repository path | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/m31-radial-integration-2026-10-23/results/semantic-3cf3f0e1d816d145dfdb19e6f6b874e6f7bdc8c313838986ebd70098e1a16903.json` | 156317 | `3cf3f0e1d816d145dfdb19e6f6b874e6f7bdc8c313838986ebd70098e1a16903` |
| `research/m31-radial-integration-2026-10-23/results/semantic-3cf995abc4cc19986c415c98310f2f741e9821676c376bbd5517d96a70489cbd.json` | 156545 | `3cf995abc4cc19986c415c98310f2f741e9821676c376bbd5517d96a70489cbd` |
| `research/m31-radial-integration-2026-10-23/results/semantic-4fe280266b3f394c41d7feef1a0fd5a113d105954ce0d6d8bf612946cbf70c3e.json` | 156545 | `4fe280266b3f394c41d7feef1a0fd5a113d105954ce0d6d8bf612946cbf70c3e` |
| `research/m31-radial-integration-2026-10-23/results/semantic-4ff1d6b7b155e7ed9995e047b91f245e6073ed08860a311bf045141b710a1986.json` | 154208 | `4ff1d6b7b155e7ed9995e047b91f245e6073ed08860a311bf045141b710a1986` |
| `research/m31-radial-integration-2026-10-23/results/semantic-5012e84ed86e7b67861eb46c0c6d5fcf88175207e93a5f7725c2b8318a9fc8dd.json` | 154721 | `5012e84ed86e7b67861eb46c0c6d5fcf88175207e93a5f7725c2b8318a9fc8dd` |
| `research/m31-radial-integration-2026-10-23/results/semantic-501f868bd28a7842be09bf1d61fc34cc9322e92da94719ff27120895b29a2553.json` | 152099 | `501f868bd28a7842be09bf1d61fc34cc9322e92da94719ff27120895b29a2553` |
| `research/m31-radial-integration-2026-10-23/results/semantic-65bf86dfc270f7f189d9a3c31ec96eade7f3fb1869c4f944c28f3428d1cb202d.json` | 154607 | `65bf86dfc270f7f189d9a3c31ec96eade7f3fb1869c4f944c28f3428d1cb202d` |
| `research/m31-radial-integration-2026-10-23/results/semantic-65c524c8a83de7269040f0d4c44d97c473885abd582a50628817f785728a4ce2.json` | 152384 | `65c524c8a83de7269040f0d4c44d97c473885abd582a50628817f785728a4ce2` |
| `research/m31-radial-integration-2026-10-23/results/semantic-6631b353f84ed30472753d2e20dae136b61db7d304cc8dadfc6df2cc72aadc9d.json` | 153068 | `6631b353f84ed30472753d2e20dae136b61db7d304cc8dadfc6df2cc72aadc9d` |
| `research/m31-radial-integration-2026-10-23/results/semantic-66530c427e0a72beb3762585c9ad461bf5ae4a6967e18668a6f8221a6159639c.json` | 156431 | `66530c427e0a72beb3762585c9ad461bf5ae4a6967e18668a6f8221a6159639c` |
| `research/m31-radial-integration-2026-10-23/results/semantic-7c49d6c2c9d3f3962fc03817b836426ba5644f15607c8f863d72581447eb4fb7.json` | 153923 | `7c49d6c2c9d3f3962fc03817b836426ba5644f15607c8f863d72581447eb4fb7` |
| `research/m31-radial-integration-2026-10-23/results/semantic-7c4dc57f82f10b52512ed3cac73a171cc7eaa847470c6cff9a5db683a445e8a4.json` | 156431 | `7c4dc57f82f10b52512ed3cac73a171cc7eaa847470c6cff9a5db683a445e8a4` |
| `research/m31-radial-integration-2026-10-23/results/semantic-7c50c74123bf49dfc0060000289a34fa7de07d9737c62e8781f93c6b7bb7faf2.json` | 153353 | `7c50c74123bf49dfc0060000289a34fa7de07d9737c62e8781f93c6b7bb7faf2` |
| `research/m31-radial-integration-2026-10-23/results/semantic-7c68c6fbda18ea63e8c7332077f8366f2dc9cf65e1ac83bb326963fbabcd7ebd.json` | 152612 | `7c68c6fbda18ea63e8c7332077f8366f2dc9cf65e1ac83bb326963fbabcd7ebd` |
| `research/m31-radial-integration-2026-10-23/results/semantic-93d8f968b36ac8c157c517893b9b1b82ec65ca1d73e137ad45e730ace80913a3.json` | 152954 | `93d8f968b36ac8c157c517893b9b1b82ec65ca1d73e137ad45e730ace80913a3` |
| `research/m31-radial-integration-2026-10-23/results/semantic-93e875b12f427ecf2f71c4813eb5156e371a35b1d050028c11cde0291e171f93.json` | 152897 | `93e875b12f427ecf2f71c4813eb5156e371a35b1d050028c11cde0291e171f93` |
| `research/m31-radial-integration-2026-10-23/results/semantic-9438c18fcbc5fb92274d17bfcf3c4b155085bbafef32346b40c6469476dfbd53.json` | 156431 | `9438c18fcbc5fb92274d17bfcf3c4b155085bbafef32346b40c6469476dfbd53` |
| `research/m31-radial-integration-2026-10-23/results/semantic-94833cf69d05c95b1ec0ec1343ded9c036b579343eaa7e976b1b2f1bbb8ffe74.json` | 153011 | `94833cf69d05c95b1ec0ec1343ded9c036b579343eaa7e976b1b2f1bbb8ffe74` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ae1be83d601b02d35c24d03fd017d57733da2f1dbc18586237a7b46570b4b068.json` | 154550 | `ae1be83d601b02d35c24d03fd017d57733da2f1dbc18586237a7b46570b4b068` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ae2760524fb239c3341e72bdce74e96a976876d8a8ba573604dd54b07e830235.json` | 154664 | `ae2760524fb239c3341e72bdce74e96a976876d8a8ba573604dd54b07e830235` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ae342b630998ec45bc639165181fcab4effd0decdb1a22ea00a1bcf73fa9faca.json` | 152555 | `ae342b630998ec45bc639165181fcab4effd0decdb1a22ea00a1bcf73fa9faca` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ae54bf178a84eac4cd3f4986fe3a036673b65701a2fa7fda0c57b94eff60352b.json` | 153695 | `ae54bf178a84eac4cd3f4986fe3a036673b65701a2fa7fda0c57b94eff60352b` |
| `research/m31-radial-integration-2026-10-23/results/semantic-c768b3a0bed2e6a3197c5bd3bbdda6bb078de2f8722bc633c2a8e037fca086c4.json` | 156431 | `c768b3a0bed2e6a3197c5bd3bbdda6bb078de2f8722bc633c2a8e037fca086c4` |
| `research/m31-radial-integration-2026-10-23/results/semantic-c76e4f4f5856c85af2369cd66870454176f6e8e6b138b92b4356389266bce45e.json` | 156374 | `c76e4f4f5856c85af2369cd66870454176f6e8e6b138b92b4356389266bce45e` |
| `research/m31-radial-integration-2026-10-23/results/semantic-c76f733a8c42a48d0eb7e25a9f1ae2c2c2cae19c7a8a5362a0f69f10c4efd911.json` | 153638 | `c76f733a8c42a48d0eb7e25a9f1ae2c2c2cae19c7a8a5362a0f69f10c4efd911` |
| `research/m31-radial-integration-2026-10-23/results/semantic-c7efb7d0fbfaa9273b4a199f2c7e800ea64d9b9431a91ab52046f3431ab2a2ff.json` | 156317 | `c7efb7d0fbfaa9273b4a199f2c7e800ea64d9b9431a91ab52046f3431ab2a2ff` |
| `research/m31-radial-integration-2026-10-23/results/semantic-db291addadbe714dbec849b5f7785be9d50a7a811d9d2a3beedc291f722277cd.json` | 156317 | `db291addadbe714dbec849b5f7785be9d50a7a811d9d2a3beedc291f722277cd` |
| `research/m31-radial-integration-2026-10-23/results/semantic-db8a2d5ecafe0ee629a416d0d93aef98230c7bdc8ddb2dc983630d45f19468ae.json` | 156317 | `db8a2d5ecafe0ee629a416d0d93aef98230c7bdc8ddb2dc983630d45f19468ae` |
| `research/m31-radial-integration-2026-10-23/results/semantic-dba952e2f53ac73e2760e9b88a822a7942831f9490b0816c465540e96c07eba1.json` | 154436 | `dba952e2f53ac73e2760e9b88a822a7942831f9490b0816c465540e96c07eba1` |
| `research/m31-radial-integration-2026-10-23/results/semantic-dbd6e3130c7f0af7335fda3a21a729c959944b3c48b7e092ee1197275d1e7e6b.json` | 153980 | `dbd6e3130c7f0af7335fda3a21a729c959944b3c48b7e092ee1197275d1e7e6b` |
| `research/m31-radial-integration-2026-10-23/results/semantic-edc28eac092d49431a58dfccdcde86a6e4d995eba34f28f5b55c0f1a7da16794.json` | 152897 | `edc28eac092d49431a58dfccdcde86a6e4d995eba34f28f5b55c0f1a7da16794` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ee13597a15a185a70ddb3f9c73a2cee5ea12e25c9827216c757adab0666b44de.json` | 156431 | `ee13597a15a185a70ddb3f9c73a2cee5ea12e25c9827216c757adab0666b44de` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ee16ddedc470de278bb446ffa759941103a5e2ef7e057fbb28d2b6a1906d135f.json` | 155063 | `ee16ddedc470de278bb446ffa759941103a5e2ef7e057fbb28d2b6a1906d135f` |
| `research/m31-radial-integration-2026-10-23/results/semantic-ee513c5d517276b733c295a4dcd6c9071e69456a19420b23b022f436d45efcda.json` | 154208 | `ee513c5d517276b733c295a4dcd6c9071e69456a19420b23b022f436d45efcda` |
| `research/m31-radial-integration-2026-10-23/ui-supervisor-launch.lock` | 23 | `582728fcc60fc12fd7abcdaf58c67141dc65f2e824a859e4ec0c68c6587f124e` |
| `research/m31-radial-integration-2026-10-23/ui-supervisor.json` | 224 | `3ca237caaf440bc7c9f0fcbf8dc6afffd68607c3f4db6ff221eaa24794d110f0` |
| `research/m31-radial-integration-2026-10-23/ui/camera-after.json` | 58 | `f5f761338f9fa2a3fc708e4747ff445df0b43d4b82a5160eb719082ff5997180` |
| `research/m31-radial-integration-2026-10-23/ui/camera-before.json` | 57 | `770bb324de245d30438e86a9756a680c4c1431a8ccaa6b4bf20e1a2a2305c2f9` |
