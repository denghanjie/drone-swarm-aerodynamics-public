# Exact corrections from draft v1 to v2

The first draft remains at `/tmp/m31-oracle-viewer-draft` without edits. V2 was copied to a separate directory before revision. No saved results, target values, generated binding or display data were read. No analyzer, checker, reference, viewer builder, syntax test or browser was executed. Only source reading, source copying and text edits were performed.

## Corrected identities

| First-draft behavior | V2 behavior |
|---|---|
| Treated saved reference `i` and `j` as indices in `ids`; required `0 <= i,j < 64`; stored `(ids[i], r, ids[j])`. | Validates `i` and `j` against the stable input-ID set and stores `(i, r, j)` directly. The displayed link endpoints are looked up by those same stable IDs. |
| Compared `ref.inputSha256` and saved analysis `inputSha256` with the SHA-256 of the input JSON file bytes. | Computes SHA-256 of the canonical envelope `{'domain':'m31-moving-admission/input/v1','id':name,'input':inp}` using sorted keys, compact separators, `ensure_ascii=True`, `allow_nan=False`, ASCII encoding and **no trailing newline**. Compares reference, analysis and prior scheduled semantic identities with that digest. |
| One ambiguous input-hash field plus file pins elsewhere. | Retains `inputSha256` as the canonical semantic identity and adds `inputFileSha256` for the saved file-byte digest. File-byte pins still bind frozen input bytes, including any newline. The browser checks the latter against its binding pin; the builder checks the former. |
| Package constant and integration instructions targeted `research/m31-oracle-omission-screen-2026-10-17`. | Package constants and integration instructions target `research/m31-oracle-omission-renewal-2026-10-17`. The analysis schema remains **`m31-oracle-omission-screen-v1`**, as required. Generic viewer/display schemas remain unchanged. |

The incorrect pair-index assumption could be concealed when stable IDs happen to equal positions. V2 no longer relies on that coincidence. These were draft-source errors, not executed viewer results; no output has been repaired or regenerated.

## Writer evidence rechecked

All paths below are repository-relative and refer to source, not result files.

- `research/m31-moving-admission-2026-10-17/source/semantic-reference.py`: `regenerate_scene` reads each `identifier` into `ids`; pair emission uses `i: ids[receiver]`, `j: ids[source]`. Internal positional fields are separately named `ii` and `jj`.
- `research/m31-moving-admission-2026-10-17/source/check.py`: `scene_reference` copies pair `i`, `r`, `j` unchanged into the saved reference. `ENCODER` specifies sorted, compact ASCII JSON; `canonical_hash` hashes encoder fragments without a newline; `input_hash` supplies the domain/id/input envelope. `pose_words` projects each input drone's words `[:3] + [6:10]` in input order.
- `research/m31-normalizer-replication-2026-10-17/source/check.py`: the saved reference writer uses the moving-admission `input_hash`, adds schema `m31-normalizer-ablation-reference-v1` and the replication source commit, and adds byte pins to `report.referenceFiles`.
- `research/m31-normalizer-replication-2026-10-17/source/run.cjs`: `save` emits a canonical JSON line and returns a repository-relative path, file-byte count and file-byte SHA-256. `projection` uses the same position/quaternion word layout. `generate` writes frames as `{t, words}`, slots with `status:'reached'` and their captured input, generation schema `m31-moving-admission-generation-v1`, and descriptors with status, frame count, reached/missing times, seed and byte pins. `indexValue` writes schema `m31-normalizer-ablation-index-v1`; scheduled entries bind canonical input identities and generation file digests.
- `research/m31-oracle-omission-renewal-2026-10-17/source/analyze.py`: confirms the corrected canonical envelope identity, stable-ID pair keys and unchanged analysis schema.
- `research/m31-oracle-omission-renewal-2026-10-17/source/check.py`: writes schema `m31-oracle-omission-independent-check-v1`, `passed`, `firstFailure`, and the complete verified-count record. V2 now checks that source-defined report shape/count completion before binding.
- `research/m31-oracle-omission-renewal-2026-10-17/source/run.py`: retains attempt schema `m31-oracle-analysis-attempt-v1`, completed status, output bytes/digest and exit code. Its peak-RSS test occurs after output writing; a failed gate changes the attempt to failed/nonzero. V2 continues requiring a completed zero-exit attempt for both stages, so an output file alone cannot satisfy acceptance.

## Additional source-grounded binding checks

The existing pose projection was confirmed, not replaced. V2 additionally checks the source-defined prior index/generation schemas, the six-state schedule, completed generation descriptors and their recorded frame counts, all three reached times, no missing times, exact reference-file pins in the prior independent check, and scheduled input/generation identities. These are saved-record consistency checks. They generate no pose, coefficient, selection or scientific proof.

The prior replication's failed speed gates remain separate: its numerical integrity/equivalence/admission fields are the pose-evidence prerequisites, not its overall benefit result.

## Renewal scope

The parent reports that the original launch stopped at unsupported macOS `RLIMIT_DATA` before source validation/import, with no scientific execution. This correction note does not independently audit that attempt. It preserves the first draft and targets the separately allocated renewal rather than treating it as an invisible retry.

The renewal's peak-RSS acceptance test is **observational and post-output**, not a hard memory limit; final report overhead is outside the stated observation. The viewer asserts no enforced-memory or runtime-performance result. No result or opportunity outcome has been assumed.

Pending parent work: inspect the final revised sources, perform any authorized syntax checks, bind only accepted renewal analysis/check evidence, and complete browser QA. V2 is still an unbuilt source draft.
