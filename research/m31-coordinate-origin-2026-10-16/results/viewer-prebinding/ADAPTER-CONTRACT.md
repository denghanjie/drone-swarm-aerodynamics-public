# Saved-evidence adapter handoff

Status: actual terminal result and raw schema mapped; independent-review receipt and external closure are not yet bound. The shipped page must stay locked. This is a source deliverable, not a browser-QA or independent scientific-review claim.

The source publication is `ccafbd9b9fd3a3cdd7ffacb5fb360ee5f3dc1abc`; the existing freeze SHA-256 is `ccfeac8a7b6386f647d00899933757004146f4e01f8b135eaf73389190f9efaa`. These identify this campaign only. The preceding wake campaign's result/review cannot unlock it.

## Manifest and unlock sequence

`data.json` currently has `bindingState: "pending-independent-review"`, `reviewContract.bound: false`, and the actual descriptors already available. `adapter.js` has `ADAPTER_READY = false`. All three must change only after binding actual terminal independent review and closure. `loadEvidence()` stops before anchor or scientific-array fetch while any lock remains.

Once the actual review format is available, add the real `files.review`, `files.reviewClosure`, and `files.reviewInputIndex` descriptors and review-contract identity pins. Implement `verifyPublishedEvidence({meta, documents})` against that actual format. Do not merely return `true` or reuse a prior review's verifier without checking this campaign's schema.

The loader first length/SHA-256 checks and parses these anchors: `freeze`, `result`, `budget`, `review`, `reviewClosure`, `reviewInputIndex`. The verifier must establish all of the following from those original artifacts:

- The result and scientific budget are terminal, the attempt is inactive, ownership/process cleanup is confirmed, and the single-attempt disposition is closed. A numerical failure can be valid evidence.
- The independent review is terminal and its evidence-integrity decision passes. Its result/source/freeze/input-index/checker identities agree with this campaign's declared pins. Review integrity is separate from `result.pass`, individual numerical gates, and candidate qualification.
- The independent review's external supervisor/closure is terminal, inactive, within its prescribed output/time bounds, and confirms owned-process cleanup. A review process's self-asserted completion alone is insufficient.
- The review input index binds the actual terminal result, budget, frozen sources, original raw-file index and relevant reports. Cross-check the actual receipt/input-index/checker hash chain, not an independently mutable flag in this viewer.
- The manifest receiver IDs equal the result's reviewed configuration; both origin offsets equal the reviewed configuration; all six origin/arm exposures, missing files, and dispositions agree with the saved review/index. Missing exposure must be an explicit reviewed absence, not a failed fetch.
- The independent review confirms the source freeze against the source publication and original saved inputs. The viewer itself never runs that checker or the scientific sources.

The verifier returns `{integrityVerified: true, boundFiles}`. `boundFiles` is an object keyed by every entry in `meta.files`, with its verified `{bytes, sha256}` identity. It must be built from the cross-checked original source/raw/review indexes and anchored review chain, not copied unconditionally from `meta.files`.

The loader additionally compares each descriptor with `rawName` against `documents.result.files[].name`, and each descriptor with `repoPath` against `documents.freeze.files[].path`. Both comparisons require the original byte length and SHA-256. All declared files must occur in `boundFiles`. Declared JSON and text files are checked before projection; binary files are checked before decoding on the selected origin's first load. A hash/length/fetch failure locks the page; it never turns a declared file into a “skipped” stage.

This is consistency verification against published artifacts, not an authenticity signature. The manifest and viewer code remain part of the publication trust boundary.

## Actual manifest shape

- `schemaVersion: 1`, `nSources: 5000`, `receiverIds` (four distinct reviewed IDs), `receiverIdsFile` (file key for the original 16-byte generated ID array), `sourceCommit`.
- `origins`: exactly two `{id, offset, poses, preparedOffsets, references}` entries with IDs 0 and 1. `poses` and `preparedOffsets` are file keys or explicit null. `references` maps R/Q0/Q1 to `{metadata, scalars, terms, sums, compensatedSums, validity, counts}` file keys. All displayed origin-1 poses are actual saved origin-1 poses; they are not translated in the viewer.
- `cells`: exactly six `{origin, arm, terms, serial}` entries. A/B/C are separate even when a cell is skipped. Absent buffers are null. Do not copy another cell's pointers to fill a gap.
- `files`: descriptors `{url, bytes, sha256, format, label, rawName?, repoPath?}`. `format` is json/text/binary. URLs must be public HTTP(S), same-origin and credential-free. Redirects are rejected. No private absolute paths.
- `initialSelection`: display-only `{origin, arm, selection, rotor, source, color}`. The actual manifest starts on origin 1, C, first receiver, rotor 0, source 0, `error-T:C-R`. It does not auto-search a scientific candidate or claim the initially selected pair is a maximum.

Descriptors were read from actual terminal evidence and checked against its raw index during source preparation. No generator, scientific model, shader, checker or scientific sums were executed to prepare them.

## Raw binary contract

Every integer/float read uses explicit little-endian `DataView` access. The source-major ordinal is `((selectionIndex * 5000 + sourceID) * 4 + rotor)`, with 80,000 slots per origin/stage.

| Saved array | Layout / bytes |
|---|---|
| Original states | 5000 × 17 f64; 680,000 bytes; positions 0–2 and quaternion 6–9 only for drawing |
| Prepared original offsets | 16 × 4 f64; 512 bytes; first three values locate the displayed rotor marker |
| GPU terms | 26 u32 words/104 bytes per slot; 8,320,000 bytes |
| Reference metadata | 8 u32 per slot; 2,560,000 bytes |
| Reference scalars | 18 f64 per slot; 11,520,000 bytes |
| Reference terms | One f64 per slot; 640,000 bytes |
| Ordinary / compensated sums | 16 f64 each; 128 bytes each |
| Sum validity | 16 u8; 16 bytes |
| Optional serial output | 16 × 8 u32; 512 bytes |

GPU words 0–7 are ordinal, receiver ID, source ID, rotor, status, policy, validity mask, routing flags. GPU words 8–25 are raw f32 representations of the 18 fields in `FIELDS`. Reference metadata uses the same first eight words; its 18 f64 scalars use the same numeric field order.

Validity bit k governs numeric field k. Center components are fields 12–14; rotor displacement is 15–17. Each component is read only when its bit is reached and record identity matches. A later invalid status can retain earlier reached components and is displayed beside them. Unreached raw +0 is unavailable, never a numerical zero. A valid term additionally requires status 3/4/5, bit 11, and a finite nonnegative value. No local vector is reconstructed from positions, axes, downstream or radius.

Serial records are selection index, receiver ID, rotor, status, mask, count, sum bits, first bad slot. A valid serial sum requires matching identity, status 2, mask 1, count 5000, firstBadSlot `0xffffffff`, and a finite decoded value. Missing output remains unavailable with the disposition's saved reason. Reference ordinary sums display their completion validity; an incomplete retained prefix can be labeled raw/partial.

## Report projection

`projectPublishedReports` is already implemented against the actual terminal result. It receives `{meta, documents, verification}` after integrity verification. It returns:

- `campaign`: `{sourceCommit, qualified, outcomeLabel, summary}` copied/worded from the saved terminal disposition. Current saved decision is no-candidate.
- `cells`: six `{origin, arm, key, matchedReference, status, statusKind, qualified, qualificationLabel, note, availability, rows}` objects. A/B use Q0; C uses Q1. `availability.terms/serial` each has `{retained, label}`. Explicit raw/report exposure mismatch throws. Current saved states are three origin-0 qualified cells, translated A/B interface skips, and translated C term failure with no serial dispatch.
- Each `rows` array has 16 addressed entries: `{index, exactTermSum, termSumLabel, l1QR, l1TQ, l1TR, termPlusAllowance, reductionError, allowance, combined, epsilon, gateLabel, gatePass}`. Certificate objects are retained intact. The UI only displays their `approximateDisplay`; it never recomputes exact acceptance. `gatePass` comes from a saved serial/term/reference row's boolean, and the label names that stage. No missing final combined gate is invented.
- `vectorContrasts`: retained origin/comparison report metadata and original `fields` arrays. Their counts/maxima/witness slots are copied from saved B−A and C−B comparison reports. No aggregate is recomputed by the viewer.

Before unlocking, the actual verifier should confirm relevant embedded `result.references` and `result.cells` reports agree with the raw assessment/disposition files already included in the manifest and reviewed input set. This is an identity/content check, not a new numerical assessment.

## Display-only arithmetic

Allowed display operations are addresses/indices, finite/identity/validity checks, saved term differences, saved component differences, color normalization, largest displayed retained-value selection, and camera/mesh transforms. They are never scientific gates. Exact report certificates are not re-summed or re-evaluated.

Camera recenter subtracts only the selected declared origin for drawing. It does not mutate the raw arrays or the numeric tables. The scene uses all original saved poses and quaternions, enlarged glyphs, retained original rotor offsets, and actual connection endpoints. There are no magnified error arrows, continuous flight animation, physical wakes, generator execution or new model evaluations.
