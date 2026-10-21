# Saved audit-result review: paired time-step sensitivity

21 October 2026. Accepted within the saved-report/index review scope below. No blocking inconsistency was found in the recorded outcomes, common-window aggregates, initial-match accounting or retained identity-read anomalies.

## Scope and evidence identities

This review read only the completed `audit/audit.json` and `results/index.json`. It did not import or execute scientific/audit modules, rerun the producer or audit, read the viewer position buffers, decompress journals, parse raw records, extract old initial prefixes, run native queries, or modify frozen source/results. Simple independent review calculations reaggregated already saved per-update MAEs and reconciled metadata/counts. This is an inspection of completed evidence, not another allocation or an independently derived controller/native solver. The reviewer authored the audit adaptation; the separate protocol reviewer supplies independent source review.

| Reviewed file | Bytes | SHA-256 |
| --- | ---: | --- |
| audit/audit.json | 1,760,914 | `0394724825ad6d6931d4b951ea3bf66f99d867e93fec8b0abcc65a541b4104a5` |
| results/index.json | 323,936 | `57d697efbdccea3bb8d529c678eb3020b3993f330c85769f3174ccec51b0aec2` |

The report's index pin matches the directly read index bytes exactly. Both name source commit `08fc10c6fb3d38dc0e22b7f1aa595e8cb9a50848`; the report names source-manifest SHA-256 `6b376a062e328205cf7da697eccb9852a62b15abd9bea4ba09e56515c52382f2`. It records passed/evidenceIntegrityPassed true, a 636.9199576249999-second internal audit wall, and zero native/model calls by the auditor. The producer index is complete, has no failure, and records 716.6250460419999 seconds. These internal records do not by themselves certify external supervisor closure, UI success, result freeze or publication; those remain the surrounding result review's responsibility.

The report pins a 48,966,402-byte viewer export with SHA-256 `24f9b3d4e62485f871b1d28385026eb657c761682379c7f58582eaeec7ea5fb9`. This review did not read or rehash that export. Positional metric values below are the saved auditor's results; this review checked their indexing/bounds and internal relationships, not their derivation again from position buffers.

## Outcomes and refused-trial semantics

The four new fine outcomes bind exactly between producer index and audit case outcomes, including status/reason/refusal, completed/attempted counts, nominal last time, issues and controller memory. The report's four pair entries retain order fine seed1, coarse seed1, fine seed2, coarse seed2 and explicit sourceResolution labels. Overall completion/admission flags and outcome counts are correctly scoped to the new fine paths.

| Seed / controller | Fine completed steps | Fine attempted stages | Fine outcome |
| --- | ---: | ---: | --- |
| 2026102101 / original | 1,447 | 5,792 | stopped: native refusal |
| 2026102101 / memory | 2,000 | 8,000 | completed to 5 s |
| 2026102102 / original | 2,000 | 8,000 | completed to 5 s |
| 2026102102 / memory | 2,000 | 8,000 | completed to 5 s |

For seed2026102101 original, both resolutions record domain-refused / native-admission / build / near-field at k4, absolute refused-trial time 3.62 s. Coarse local step523 and fine local step1047 are distinct saved attempts. Coarse last completed nominal time is 3.615 s (actual saved 3.6149999999999998); fine last completed time is 3.6175 s. Both have empty endpoint termination issues. Refused frames have kind refused-stage and safetyPassed:null, with their own record provenance; outcome summaries explicitly state that the trial is not a completed endpoint. This is a numerical/model-domain admission stop, not an observed collision or physical safety conclusion.

The completion categories agree across resolutions: memory-only-completed for seed2026102101 and both-completed for seed2026102102. The preserved stopping times show why category agreement must not be described as identical endpoint histories. Fine allPathsCompleted and allAttemptedNativeStagesAdmitted are false; allMemoryPathsCompleted is true. A faithfully recorded native stop is compatible with a passing evidence audit.

Stage accounting reconciles: 7,447 completed steps, 29,792 attempted native calls/stages, 29,791 successful stages and one refusal. The k4 stop contributes three successful stages plus its refused fourth stage beyond completed steps. Each path obeys attemptedStages = 4×completedSteps + refusedStageIndex when applicable. There are 7,447 safety records, 1,906,624 derivative/native-load rows (=29,791×64), eight journals, 93 compressed parts and 46,564 raw records. Descriptor totals agree between report and index. Compressed journal bytes are 3,075,331,252; adding the pinned 118-byte launch yields the index's 3,075,331,370 bytes before index. The config retains the unchanged 4 GiB producer cap, 32,000 attempted-stage/native cap and 4,800-second successful wall limit.

## Completed endpoint comparisons

The saved comparison bounds use coarse k paired with fine 2k, including initial k = 0. For seed2026102101 original, the shared count is 724 through coarse 723 / fine 1446. The extra fine completed endpoint 1447 at 3.6175 and both refused trials at 3.62 are excluded. The last matched actual times are coarse 3.6149999999999998 and fine 3.615, preserving their separate floating-point expressions. The other three paths have 1,001 shared endpoints through coarse 1000 / fine 2000 at 5 s.

| Seed / arm | Last-common max center difference (m) | RMS at last common (m) | Maximum over all shared endpoints (m) | Maximizing ID / coarse k / fine k / actual time(s) |
| --- | ---: | ---: | ---: | --- |
| 2026102101 / original | 2.2032355712496346e-5 | 3.195278575189967e-6 | 2.2266225432333523e-5 | 16 / 718 / 1436 / 3.59, 3.59 |
| 2026102101 / memory | 2.3845355363148792e-5 | 4.3429536749721025e-6 | 2.3845355363148792e-5 | 40 / 1000 / 2000 / 5, 5 |
| 2026102102 / original | 8.563340568553525e-6 | 2.1498961843936735e-6 | 8.563340568553525e-6 | 25 / 1000 / 2000 / 5, 5 |
| 2026102102 / memory | 1.4742724387516053e-5 | 4.311584011918467e-6 | 1.5951682300060465e-5 | 35 / 964 / 1928 / 4.82, 4.82 |

All reported metrics are finite, maximizing IDs/indices lie within their stated shared windows, the maximizing fine index is twice coarse, and each whole-window maximum is at least its last-common maximum. Saved mean-z and ID17-z differences retain the fine-minus-coarse direction. No positional threshold is declared; convergenceOrderClaim/accuracyClaim/physicalValidity are false and acceptanceTolerance is null. All four observed comparisons have more than the initial endpoint. Initial-only and empty-control branches remain unobserved in this result; their prospective source review is not a new empirical exercise of those branches.

## Own-request errors and shared windows

Independent calculations used the per-update observations already embedded in `caseOutcomes`, summing chronologically from positive zero and dividing by the shared count. They did not reuse precomputed means from unlike windows, run a controller, or revisit raw per-drone errors. All four two-way comparisons reproduce their saved coarse/fine means and fine-minus-coarse differences exactly, with matching common controller time words, counts, first/last indices and separate actual time windows.

| Seed / arm | Shared controls / indices / time window | Coarse own-request MAE | Fine own-request MAE | Fine minus coarse |
| --- | --- | ---: | ---: | ---: |
| 2026102101 / original | 362 / 0–361 / 0–3.61 s | 0.27496676391925495 | 0.27496671380529525 | -5.0113959704223277e-8 |
| 2026102101 / memory | 500 / 0–499 / 0–4.99 s | 0.17889762106457152 | 0.17889760970517105 | -1.1359400475807746e-8 |
| 2026102102 / original | 500 / 0–499 / 0–4.99 s | 0.27966794716379867 | 0.27966797812482136 | 3.096102269006806e-8 |
| 2026102102 / memory | 500 / 0–499 / 0–4.99 s | 0.18023905404674234 | 0.18023918043957393 | 1.2639283158977221e-7 |

Four-way intersections were formed independently from the four saved observation lists. All four means and both contrasts, followed by fine contrast minus coarse contrast, reproduce the report exactly.

| Four-way metric | Seed2026102101 | Seed2026102102 |
| --- | ---: | ---: |
| Common count | 362 | 500 |
| Global indices | 0–361 | 0–499 |
| Each stream's actual window (s) | 0–3.61 | 0–4.99 |
| Coarse original MAE | 0.27496676391925495 | 0.27966794716379867 |
| Coarse memory MAE | 0.18679013763728544 | 0.18023905404674234 |
| Fine original MAE | 0.27496671380529525 | 0.27966797812482136 |
| Fine memory MAE | 0.18679013503542855 | 0.18023918043957393 |
| Coarse memory−original | -0.08817662628196951 | -0.09942889311705633 |
| Fine memory−original | -0.0881765787698667 | -0.09942879768524743 |
| Difference of differences | 4.751210280762308e-8 | 9.543180889970415e-8 |

The first seed's memory two-way metric legitimately uses 500 samples, while its four-way memory mean uses 362. Those distinct windows must remain separate in summaries. Each stream follows its own evolving requested vertical velocity; neither the signs nor close cross-resolution values establish common-target tracking, a population effect, convergence, accuracy, or physical validity. The final due observations before refusal describe saved completed states, not refused trial states.

## Initial equality and retained provenance

The passing report records 4,352 initial physical words checked, 4,352 coarse/fine initial-word comparisons (4×64×17), 2,176 fine original/memory paired-word comparisons (2×64×17), and4,352 segment-boundary physical-word comparisons. Initial and segment-boundary memory-word comparison counts are 256 each (2×64×2). Its source-checked distinct-seed requirement and exact word-equality checks are attested by the successful audit; this review did not reconstruct the initializer or read raw initial words again.

The coarse-evidence section retains the exact public result commit `73e8bae5261d01f4ffe79ad566f191df58d9b9fb`, 150-pin manifest `1237252ed0ee0799982dcd89365272ae8c4ee1c330d7cd5377af183dc8b3abe5`, final receipt pin `d90643cc9f88b0da9e16605ce268d9d82cc40a47fd2a0a0eaa704b2415ee0c68`, old source identity and closure/export pins. It lists four 32 MiB part000 identities and exactly one sequence 0 / offset 0 raw initial record per path, with lengths 22,095 bytes for originals and 28,160 for memory and individual SHA-256 values. This is explicitly four raw initial records parsed by the completed audit, four old audited export paths consumed, zero other old raw trajectory records parsed and zero old trajectory arithmetic reaudits. It does not assert that the old baseline was recomputed independently.

## Four retained identity-read anomalies

The report preserves four events across two verified-read operations; both refer to parts listed in the reviewed journal descriptors:

| Operation | Part | Attempt 1 | Attempt 2 | Expected complete identity |
| --- | --- | --- | --- | --- |
| 154 | seed2026102101-original-h0025-s1.jsonl.gz.part004 | read-error, errno 60 | byte-mismatch, 0 bytes, SHA-256 of empty input | 33,554,432 bytes; `564f416afe818d209eb0f1e00e4353cd1fc5f0ec5f5de2134442bd0a697b8867` |
| 202 | seed2026102102-original-h0025-s1.jsonl.gz.part009 | read-error, errno 60 | byte-mismatch, 0 bytes, SHA-256 of empty input | 33,554,432 bytes; `09ce0e28a5274201c33a2f396554714348a7919cb05a71ea7d3577e58b985cec` |

The empty-input digest is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. No successful-read event is logged by this implementation. Given the source-reviewed three-attempt helper, failure at attempts 1/2 followed by a passed audit implies the third read in each operation met the full expected byte/hash identity; otherwise the helper would have raised and failed the allocation. This inference should be distinguished from an explicit logged “attempt 3 succeeded” event. The failed/empty reads are not evidence bytes consumed by gzip/JSON/arithmetic. They are permitted pre-consumption identity retries, not numerical retries, dropped observations or second audit allocations. The record alone does not diagnose their underlying storage/OS cause. The producer index's own readEvents list is empty. All four audit anomalies must remain in published evidence and narrative.

## Acceptance boundaries

The saved report/index are internally consistent for the prespecified finite-path comparisons. No repair, source edit, reallocation or threshold change is requested. The accepted statement is that these two exposed starting arrangements retained their completion categories under the finer implemented step, with the recorded differences over their explicit shared windows and the retained first-original refusal. Halving dt also changed native trial times and endpoint-check frequency. No isolated RK-error/convergence-order or physical-accuracy conclusion follows.

The saved audit's exclusions remain binding: initializer, Boids steering/neighbor membership, inherited actuator law/saturation decisions, obstacle/contact geometry, native geometry coefficients, native root solve and residual model were not regenerated. There were 13,853,088 saved-root comparisons with zero one-ULP differences and 64 reconstructed norms for the refused stage; this is the declared root policy, not exact rational proof or a native-solver validation. Frozen-source identity, external allocation closure, display verification, claims review, result-byte freeze and exact-public publication checks must be completed or reviewed separately before publication is accepted.
