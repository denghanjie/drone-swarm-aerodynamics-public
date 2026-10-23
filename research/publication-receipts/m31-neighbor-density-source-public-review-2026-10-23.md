# Independent public-source acceptance — neighbor-density diagnosis

23 October 2026. **Passed.** The frozen source manifest and all 51 file pins were independently checked against fresh exact public bytes, local working-tree bytes and committed bytes. This satisfies the public-byte verification prerequisite of the static protocol review for source commit `acc97c17b446a9ab1c6f1b24a623529dc3030a7f`. It is not a diagnostic result or an allocation execution receipt.

The machine-readable operation log is [m31-neighbor-density-source-public-review-2026-10-23.json](m31-neighbor-density-source-public-review-2026-10-23.json): 92,371 bytes, SHA-256 `12e4c41c36f3eea5b7e6f47a0f67176e0538ae004173e6df3b081d3360149b4a`. This document and its JSON receipt are outside the frozen checkpoint folder.

## Exact source identity and scope

The public source manifest is [source-manifest.json at the full source commit](https://raw.githubusercontent.com/denghanjie/drone-swarm-aerodynamics-public/acc97c17b446a9ab1c6f1b24a623529dc3030a7f/research/m31-neighbor-density-2026-10-23/source-manifest.json):

- Repository path: `research/m31-neighbor-density-2026-10-23/source-manifest.json`.
- Bytes: 13,084.
- SHA-256: `810aed6dec7efe9aa10e580978af8d7019472c188219b73dcbedc7b37078594b`.
- Inventory: 51 unique pins, comprising 25 source pins and 26 input pins.

The successful acquisition performed 182 complete identity operations: 52 local file checks, 52 Git blob checks at the source commit, 26 additional Git blob checks at input origin commits, and 52 fresh HTTPS reads. The remote set is the manifest plus all 51 pins, totaling 207,252,798 verified bytes. Each successful remote request returned HTTP 200 and matched both byte length and SHA-256. The operation log retains the full relative path, immutable commit, exact public URL, identity and attempt outcome for every check.

For source pins, the public URL used source commit `acc97c17b446a9ab1c6f1b24a623529dc3030a7f`. For inputs, the public URL used the origin commit explicitly declared by that pin: the preceding result commit `0461153a7d6f75cb6e8564850b77e8b6f04cebb2`, or receipt/supplement commit `d948a58315020eda1a1502277362ab65116c873b`. All 51 pins were also checked in the local source-commit tree, and all 26 origin blobs were checked separately. Thus this receipt does not rely solely on prior public verification or only on small metadata files. It does not claim an additional remote request at the new source commit for each inherited input; its fresh remote input checks use the exact origin URLs consumed by the frozen protocol.

All fifteen source identities listed in the accepted static `review/PROTOCOL-REVIEW.md` were separately matched against the final manifest after acquisition. The review itself is prospectively pinned at 14,524 bytes, SHA-256 `c5f0825b1d054e9dfc60f50fd5fad8e2a2ce3f5762da767021a67cea12b3399e`. The final manifest contains the corrected supervisor, UI pre-write limits, independent audit, explicit comparison-contract wording and runtime scope already accepted in that review.

## Archive and display closure

All six `selected.jsonl.gz.part000` through `part005` files received fresh complete remote byte verification, plus local/source-commit/origin-commit verification. The independently downloaded part bytes were then concatenated logically into one streaming hash in the pinned order; no new archive file was published or decompressed. The aggregate is 194,862,495 bytes, SHA-256 `b0d833c23eb6e81c2aa600ef82b2e344587762775a07c412a198d49fc2a56dfa`, matching the original selected archive descriptor. This is lossless transport verification only, not validation of record contents or newly calculated scientific counters.

The complete current browser module closure was included among the prospectively frozen and freshly verified source files: viewer HTML, viewer JavaScript, `OrbitControls.js`, `three.module.js` and the transitively imported `three.core.js`. The exact core is 1,403,455 bytes, SHA-256 `eb077d2417f61d3e6d9264c317cabc4ea35769ed6b0ab533067292a550784c20`. This current complete pin does not retroactively repair the earlier checkpoint's missing prospective core pin. The previous provenance qualification and supplemental receipt documents were themselves included in the verified input set.

The runtime claim remains limited: only the Node executable has a declared byte pin checked by the launcher. Python and its standard library, Playwright and the installed browser remain unpinned environment dependencies. This receipt verifies the published source/runtime declaration, not those installed runtime binaries, a hermetic environment, display rendering or performance.

## Preserved acquisition anomaly

The initial sandboxed acquisition checked the local and source-commit manifest successfully, then failed to resolve `raw.githubusercontent.com` on three bounded read-only requests. Each returned curl exit 6 before any remote manifest bytes were received. It did not reach any archive or diagnostic input processing. The failed attempt is preserved without deletion in [m31-neighbor-density-source-public-review-2026-10-23-failure.json](m31-neighbor-density-source-public-review-2026-10-23-failure.json): 2,722 bytes, SHA-256 `2bdb6df4bc20bca6d58e15bb7fde0a1a0f21e13817a68b802992589038c3dfd9`.

A separate network-enabled read-only acquisition then completed every operation on its first attempt, with no identity mismatch, transfer error or retry. Its success receipt explicitly pins and links the earlier failed acquisition. The reported zero failed attempts in the successful acquisition must not be read as erasing the three preceding sandbox DNS failures. The environment's name-resolution failure is an acquisition observation, not a scientific failure or benchmark result.

## Acceptance limits

No selected archive was decompressed, no diagnostic count or aggregate was calculated, no model or scientific code was imported, no native query occurred, and no producer/audit/finalizer/UI allocation was launched. All four new allocation directories and supervisor locks were absent at the beginning and end of verification. Historical allocations remain closed.

The parent may now create the source-publication gate from these exact verified identities and the accepted static review. The four fixed single-use allocations still require their own successful supervised closures, independent result audit, UI verification, visual inspection and result publication review. No timing, flight safety, physical validity, novelty, alternative-candidate or research-completion claim follows from this public-source acceptance.
