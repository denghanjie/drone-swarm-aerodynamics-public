# Saved-record review failed; the failed report is preserved

The sole saved-record audit stopped after **846 reported checks**, including the rejected check, at `saved-three-pipeline-admission`. Actual checker, observer and capture exits were all **1**. `completed`, `integrityVerified`, `terminalFailureVerified`, `decisionVerified` and `qualified` remain **false**. No retry, repaired report or waiver exists.

The failure is a checker schema mistake. The frozen science producer saves `raw/capability.json` as `{browserVersion, ...capability}` but keeps the unaugmented object in `result.capability`, with the version in a sibling field. The checker incorrectly requires those whole objects to be equal. Static inspection finds exactly the extra `browserVersion` key; all shared fields match, and the version agrees with the worker's sibling value. This explanation is supported by the saved JSON and the exact producer/checker source, not by another invocation.

The comparison short-circuits the remaining clauses of that predicate. Subsequent GPU-failure, lifecycle/accounting and final mutation checks were **not reached**. Diagnosing the mistake does not establish that those checks would pass. The failure does not itself show a GPU pipeline defect or corrupted raw evidence. Read the independent [static disposition](review/FAILURE-DISPOSITION.md), which also acknowledges the source-review miss.

## Scope and exact identities

The reviewer was deliberately narrower than a numerical validator. It used standard-library byte/hash, JSON, saved-counter, dimension and accounting checks. It imported no numerical module, decoded no numerical binary, solved no root, generated no input, launched no browser and performed no GPU work. In particular, this audit supplies no new reference-residual or force-accuracy result.

Source commit `f12d8c836e7b991ec33e6de662d00ed05dcce33e` and science freeze `c0c6b2fda84567a76025b2e5f06832cbc1dd5811c23a246df5623f46baf8f8a9` remain unchanged. The independently reconciled review freeze is `c8f16d4c2b7ba0b3c2185c948c0ffbbd7208c0edd860915a6490d4ee7fcce42f`, with six source/document pins and a separate science-manifest pin. The science manifest is `7ce34e3266c70e95fd715ec30fa95527cd749e9c7ce258ea1492f0d6b717e3e4`.

The exact [review report](review/results/review.json) has SHA-256 `ba8c3833027d60373d0b4e7ff9721dac71ba09ec493a6d0e864894b1b600647e`. The [capture receipt](review/results/capture.json) has SHA-256 `0e7f4d1d115dc6fcc0a6ae68309dee7be4f0e06572d3d871dfbc7b11c5740075`. The actual external completion record is [publication/review-capture-execution.json](publication/review-capture-execution.json), SHA-256 `4a0fb558acd26bbf53a2636d11b04fc2a644e89663aa4edd57cc963a8ce2c137`.

## Closure and accounting

The caller measured the observer from before process creation through actual reaping as **0.073793666 seconds**. The observer recorded its direct checker as reaped, with complete pipes, no kill request and a 0.044938583-second interval. The caller likewise observed its direct observer reaped with complete pipes and no kill request. The launching tool returned actual final exit1 and its complete bounded summary. There is no live review process inferred from a mere session yield.

The observer's four pre-budget files total845 bytes. Its2,051-byte budget plus689-byte final summary produce3,585 accounted bytes. The caller adds its56-byte lock, zero stderr,2,113-byte receipt and748-byte final summary, for **6,502 bytes** within the32-MiB allocation. The later six-file review results directory totals5,009 bytes; it excludes the separately retained observer summary and caller lock/summary. Publication copies and this disposition are later packaging, not retroactive runtime outputs.

Failure capture and process closure do not turn the failed reviewer into an integrity pass. The original scientific attempt likewise remains unqualified, with no saved GPU output and no main-family observations. The Three.js viewer must show both failures and all unavailable states explicitly. Neither attempt can be repeated or extended.
