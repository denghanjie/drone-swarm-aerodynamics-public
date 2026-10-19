# Focused static review of display v2

20 October 2026. **Accepted for the separate prospective v2 source-freeze stage; no blocking static finding.** Display success is not certified. This review used source diffs, saved receipts and local file identities only. No browser, test, source execution, network access, scientific calculation or new delegation occurred. Only this review was written.

The original failure is preserved: results/ui-supervisor.json records exit code 1, elapsed 2.0524381659924984 seconds, and no time/output overrun. ui/qa.json records five passed groups followed by the horizontal-overflow assertion failure. Source order places that failure at the mobile check. Corrupt-input refusals and final console/page/HTTP certification were not reached. Three original screenshots exist; their visual inspection is the parent's reported work, not mine.

All **34 original source-manifest pins** still match local byte lengths and SHA-256 identities. The original manifest is 6,829 bytes, SHA-256 `2ce1e17ad32c7b5c7b7c8bf88943dba7330ee35c900e5a029d9a0c18d3bd9f80`. No original source or historical input changed.

The HTML diff contains only CSS changes: zero-minimum grid tracks on desktop and mobile, section min-width:0 and canvas max-width:100%. It introduces no document-level overflow hiding. These changes address the intrinsic-size mechanism without changing content or weakening the overflow assertion; whether they resolve the actual rendering failure remains for the prospective run. viewer-v2/app.js and pins.json are byte-identical to v1. Admission semantics, saved points, selected indices, historical nominal geometry and all scientific limits therefore remain unchanged.

The harness diff changes only manifest/publication references, viewer paths/URL and the output directory. Its full eight-group flow, both viewport assertions and all three corrupt-input checks remain intact. The supervisor diff changes only the child and output paths. Neither adds a model evaluation, fit, score, raw-data decode or scientific allocation.

The new supervisor exclusively creates results-v2/ui-supervisor.lock; the child requires a new ui-v2 directory and exclusive ui-v2/launch.lock. Logs, screenshots and receipts go to v2 paths, leaving the first failed allocation closed. The protocol retains one v2 invocation, no retry, monitored 60-second/32-MiB cutoffs, 25-ms polling, possible overshoot and detected-overrun failure.

Before browser launch, the harness requires the separate v2 manifest/publication receipt, zero scientific allocations, one display allocation, matching manifest hash, declared public/committed equality, and matching local bytes for every manifest entry. The protocol separately requires a full-commit public retrieval and freezing original source/input pins, original failure outputs and new correction files. At review time those v2 manifest/receipt files and both v2 locks were absent. Their eventual completeness and public identity remain prerequisites; receipt assertions are not themselves a remote retrieval. The parent must inspect the new screenshots and retain both display outcomes.

| Reviewed v2 file | Bytes | SHA-256 |
|---|---:|---|
| DISPLAY-V2-PROTOCOL.md | 1,861 | `8a92ad6c2cf003558c7b8c33292fd5182d08d3479a6ae8fa93e83be1426bd1b6` |
| viewer-v2/index.html | 4,504 | `a47bed7806156792b8538f55ff8b1c321c77dad4a4a3fd5e71d3f5fcd84377bb` |
| viewer-v2/app.js | 4,592 | `e3fb7d244a3bde8b54d240ea17005fe239694ec5da427703433807beebec234e` |
| viewer-v2/pins.json | 621 | `f80ac9044f05e13b36a8731d783bfb701758e22a708b017c382c0a2cde55f8b1` |
| source/ui-v2.cjs | 6,688 | `edf94dd1eba6672702c53613d8281ae0e9e888cff6229963d0a07961b6a9e768` |
| source/supervise-v2.py | 1,706 | `bf803483ee1102cf49ce5f13720a1b76edc4f14d6c1c32cd12f43c8ebaab41ed` |

Original failure receipt identities: results/ui-supervisor.json, 198 bytes, SHA-256 `7a2591305b9df052c730665b20f91e52501ef253be1c5108c7d17825acbf05fc`; ui/qa.json, 844 bytes, SHA-256 `22d224b9d3837588fae3ec544d9573fba3d0b63b0380637e98bc7b4fe2f4c6c2`.

FINAL for the reviewed bytes. Reviewer edits stop before freeze. No display or scientific rerun is performed or implicitly authorized by this review.
