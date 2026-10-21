# Prospective protocol and source review

21 October 2026. Independent protocol reviewer. **Accepted for source freeze and exact-public source verification, conditional on the identities below remaining unchanged.** No remaining blocking finding was identified in this bounded static review. This is not execution acceptance, result validation, a source-publication receipt or authorization for another attempt after a closed allocation.

## Reviewed candidate identities

Paths in this table are relative to `research/m31-paired-resolution-2026-10-21/`. SHA-256 values cover complete local bytes. The auditor and contract were held at the identities supplied by their independent author before this acceptance.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| config.json | 1452 | 9400e8a237fe25a8f7b54da1aedfe26f2a3c006f36c731838c86f6892aa85566 |
| runtime.json | 113 | 8347eef171a70a8e9ecd298684ee4c8e445b907aeb61630a26d105670641d225 |
| PROTOCOL.md | 11872 | e31d7cb910e5263eeedf82ee048e284ee5fc39143a6a7979891c9f322185b83a |
| AUDIT-CONTRACT.md | 34697 | e748ba3246e86e74288cab10a0a9ee922e06d6c0b44f2c4408723c96e7ef37df |
| HISTORICAL-CHECK.md | 3937 | 0c6ac45c4971f6dd81de19e485d23ae9aea648660f7cb27dc7976914500d8fd7 |
| LITERATURE.md | 2597 | 51c2a6b51c827ab89a277dfeddccabe2c1f445f2bd6ed2a83ce8fde68c924e0c |
| PRIVACY-SOURCE.md | 700 | eb126b1efa67f85cb9c99e623603e6b0f9194899f48d2852ea971804262585d6 |
| source/run.cjs | 7042 | 1585de5fe1e6e9f9bc47b4dc25b6455484d59a4e96e6f16bfe8cafc51d4dd967 |
| source/gate.cjs | 1271 | 91b158731394a60a87f131ac28102acdc5143e5369c945bc1b4baa2a4e2916ab |
| source/audit.py | 98830 | 8686efc2c38979122054ba37a3e749365a6f1e37a90db2c740a0d657aa7a9b2d |
| source/supervise.py | 2145 | ddcf5d0db247b7310c4baefdc0e1f6b914e92a6e8855ca60154c6f631298d595 |
| source/finalize.py | 2395 | 440403f858a1b9ef51d96ac6148d667baa328038a3ece23a751ea2afe1908374 |
| source/ui.cjs | 11108 | abb06adcc35a12765e98d388bd8620842e87694705b685f7ff095e1dee1afd05 |
| viewer/app.js | 10331 | 06fef327f88053c104449321c805eb481f3320ea08cd8ba6bf46aff7eb75f99a |
| viewer/index.html | 5268 | 09d56d7098f948a70c26f09692a1b2d8fda092389b71bd961f6c032154eac1fe |

## Scope and checks performed

I read the protocol, contract, configuration, producer/supervisor and comparison changes, viewer/UI interface, historical/literature/privacy notes and prospective manifest-helper text. I inspected source differences against the preceding paired study, parsed Python ASTs and JSON, and used syntax-only checks on JavaScript with the identity-checked pinned Node runtime and environment injection options removed. A scoped source-pattern scan found no local home/temp paths, key headers or recognizable token strings in the 15 candidate files; that is a scoped check, not an exhaustive privacy guarantee.

Independent AST comparison found 49 inherited functions/classes unchanged, including controller, memory, native evidence, projection, derivative, endpoint, Journal, separation, paired-error and storage-gate helpers. The only changed inherited functions are `source_gate`, `audit_case`, `audit` and `main`; the former motivation gate is replaced by explicit coarse-evidence binding. The producer's change from the prior runner is its study schema; the fixed new config selects the authorized half-step paths. Gate, finalizer and runtime identity remain the prior bytes. The two controller files independently hash to their pinned originals: original 2,836 bytes, SHA-256 `c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373`; memory 3,848 bytes, SHA-256 `f7966691b52f2e14c2fbba82ed136fc99cf7a87b8d53725e08be9923128cea16`.

No initializer, controller, native solver, numerical producer, audit, finalizer or browser was executed. No scientific module was imported. This reviewer did not read, decompress or extract any raw journal part. Initial-only, odd fine-stop, segment-boundary, refusal and empty-intersection behavior were assessed from source, not by running those branches.

## Design and comparison assessment

The four paths preserve the exposed seeds 2026102101/2026102102, original/memory controllers, N=64, five-second horizon and 1+4-second segmentation. New dt=.0025 and four steps per .01-second control interval compare with the published dt=.005 paths. There is no seed substitution, gain tuning, longer horizon or fresh storage trial. Caps agree across prospective config, supervisor and contract: 32,000 native calls/stages, 8,000 completed steps, producer/audit successful 4,800 seconds and external 4,820 seconds; producer 4 GiB, audit 256 MiB; finalizer 120/140 seconds and 2 MiB plus 64 KiB viewer pins; UI 150/160 seconds and 16 MiB. The protocol separately requires at least 10 GiB free disk and no overlapping active research job before launch. Neither prelaunch condition has been certified by this review.

One substantive issue was corrected before acceptance: matched endpoint timestamps cannot be required to have identical binary64 words across resolutions. Coarse and fine endpoints use different multiplication/addition sequences. The final protocol/auditor instead pair integer coarse k with fine 2k, validate each stream's own frozen expression, and report both actual saved times. The shared .01-second controller schedule has a separate time-word agreement check.

Every common completed endpoint, including the initial state, contributes to the prescribed maximum. Strict-greater updates in ascending k and the inherited ascending-ID separation rule preserve earliest-k/lowest-ID ties. An unmatched odd fine endpoint is excluded. The last-common calculation, maximum, indices, actual time windows and initial-only flag are retained. Refused trial positions stay separate from completed frames; no interpolation, extrapolation or suffix padding is introduced. Initial-only zero difference is expressly insufficient for horizon agreement.

Same-controller coarse/fine error means are recomputed from saved per-update MAEs over their common integer control indices. Each seed also receives an independently reaggregated four-way intersection before memory-minus-original contrasts and their difference are formed. This avoids subtracting precomputed means over unlike windows. Empty intersections return unavailable/null values without division; four-way time-window keys remain present. A due controller saved before refusal remains an observation of the current completed state. All comparisons disclose each arm's own evolving desired request and prohibit common-reference tracking, pooled statistical or physical-validity inference.

Primary category agreement is accompanied by each resolution/arm's status, reason, last nominal/actual endpoint times, issues and refusal metadata. Identical categories cannot replace those details. The report explicitly limits new completion/native/count flags to the four fine paths while labeling coarse comparators separately. Halving dt also changes native trial times and endpoint-check frequency, so the claim is sensitivity of the implemented discretization, not isolated truncation error, convergence order, numerical accuracy or a rigorous error bound.

## Coarse-evidence trust boundary

The audit fixes coarse result commit `73e8bae5261d01f4ffe79ad566f191df58d9b9fb`, its 31,241-byte, 150-pin manifest and SHA-256 `1237252ed0ee0799982dcd89365272ae8c4ee1c330d7cd5377af183dc8b3abe5`. I independently hashed the current final receipt: 1,541 bytes, SHA-256 `d90643cc9f88b0da9e16605ce268d9d82cc40a47fd2a0a0eaa704b2415ee0c68`, matching the candidate gate. This source review did not refetch or revalidate all old public evidence.

The coarse gate binds the selected source/result/audit/index/export/closure/supervisor identities to both manifests and checks the known passing allocations without demanding that all prior native stages were admitted. Its first original path's previously recorded refusal remains valid evidence. Coarse endpoint/controller data are trusted previously audited exports; additional checks are provenance, shape and scheduling checks, not old trajectory arithmetic reruns.

Only the first initial record of each of four old paths may be parsed. The whole corresponding compressed part must pass length/hash verification before decompression; output is bounded to one byte at a time through the first newline with a 4 MiB record bound. Compressed read-ahead is disclosed. The reader does not finish the stream or revalidate its footer/CRC: that qualification comes from the prior passed audit. It binds initial line provenance and all 64×17 words to the matching new path; original/memory initial pairing and distinct arrangements are separately retained. The prospective source helper selects exactly the four first parts, with no initial extraction during source preparation.

## Viewer interface and remaining gates

The viewer expects fine seed1, coarse seed1, fine seed2, coarse seed2, with explicit source labels and separate refusal rendering. Its resolution fields agree with the auditor's two seed summaries, four arm comparisons, endpoint counts/times/maxima and four-way error fields. The added UI group checks these labels and common-window displays; existing frame/buffer checks cover all four entries. Browser behavior and resource closure remain untested until their authorized single allocation.

Before launch, freeze the complete source/dependency manifest including this review, verify committed/local identities and independently verify exact public source bytes. Any change to a reviewed identity requires review of that change. Passing future saved-evidence, finalization, display, result/claim review and publication gates remains necessary; this prospective acceptance establishes none of those outcomes.
