# Independent saved-result review

21 October 2026. Package: `research/m31-nominal-comparison-2026-10-21`.

**Disposition: ACCEPTED for the stated finite-path computational comparison, conditional on the final complete result-byte freeze and separate exact-public result verification. No result-level blocker was found.** All four nominal paths completed five seconds. The preserved first-seed coupled paths stopped at 4.6200 and 4.6175 seconds; the second-seed coupled paths completed five seconds. The result supports this specified model intervention and its recorded outcomes, with the limitations below. It does not complete the overall research.

This review reads saved evidence and inspected screenshots. It did not run a numerical producer, scientific module, initializer, controller, native query, arithmetic audit, finalizer or browser. It did not decompress or rehash the 44 new raw parts. Their whole-byte and arithmetic checks are the completed auditor's evidence; this review checked descriptor consistency, file inventory, file sizes, offsets and aggregate accounting. Only this review was written.

## Source and saved-evidence binding

The recorded source commit is `f90d17f2b3cad19752f538040efc36893c64c3fc`, with the previously reviewed 67-pin manifest, SHA-256 `9e4b37c33ad679c9d1b035a238f7a042226a09667815ba1b3d42ab07ef271bab`. The source publication receipt records exact local/committed/public manifest equality, 67 verified pins and no read events before producer launch. I checked its binding to the audit; I did not repeat remote verification.

All 63 non-journal source pins were independently rechecked and remain unchanged. The four original `.part000` pins were already independently checked during manifest review and were deliberately not reread. The new audit, producer index, publication receipt, closure pins and viewer pins match their saved byte lengths and hashes. Source commit/configuration identities agree across the receipt, producer index, audit and export. The export's outcome summaries, last-common comparisons and same-seed comparisons equal the corresponding audit objects.

| Saved artifact, package-relative | Bytes | SHA-256 |
| --- | ---: | --- |
| `source-publication.json` | 752 | `46ba976ced9a6bdfb82eed37cf0433b9795c45a0f25acc5d46f1c4dbcfc0f742` |
| `results/index.json` | 276,205 | `47eb973f2b813f588fea57517643da55c9befefbdaf1b78d4e066a5d80afb206` |
| `audit/audit.json` | 27,436 | `2f22547283b6af6dcaf01eddcd3396428f6ca2a3790fba14aece31b9226f7122` |
| `audit/viewer-data.json` | 48,096,556 | `edf30e0fec416c1319da1822169ca1bc14bd831d0dd9c96bbaf5030f87794141` |
| `viewer/pins.json` | 637 | `074e15201855fb73f07cd997dd02ab3a6c32aee52d516bfa9aef9c34368631bc` |
| `ui/qa.json` | 534 | `d65cb79b19981936b8d7b6ae838cc27b102dd043e5b80f04d335da01c2e1bf8d` |

The eight journal descriptors in the producer index exactly equal the audit's journal pins. They describe 44 unique regular part files, each at most 32 MiB, with contiguous offsets and matching file sizes. The results directory contains exactly those parts plus launch, exit and index files. The descriptors total 1,386,682,566 compressed bytes and 4,553,116,974 uncompressed bytes, across 38,016 records. These descriptor totals are not a second verification of raw contents; the final freeze must bind every part.

## Closed allocations and audit scope

All four supervisors report return code zero, successful wall/output caps and no timeout. The saved phase-directory sizes match the reported output totals and `ALLOCATION-CLOSURE.json`; every phase has one retained launch lock and one closed-passed allocation. Producer and audit exits are closed with zero exit codes. No failure file is present in this package. The finalizer and UI each retain two passing byte-gate records with empty read-event arrays. Producer-index and audit read-event arrays are also empty.

| Allocation | Saved supervisor wall seconds | Verified output bytes | Successful wall cap |
| --- | ---: | ---: | ---: |
| Producer | 361.997061292 | 1,386,958,946 | 1,200 s |
| Audit | 223.938930791 | 48,124,354 | 1,200 s |
| Finalizer | 0.553768458 | 162 | 120 s |
| UI | 14.229344666 | 449,769 | 150 s |

The finalizer additionally produced the separately checked 637-byte viewer pin file, below its 64 KiB allowance. Phase outputs are below their prospective 2 GiB, 128 MiB, 2 MiB and 16 MiB caps. Wall values are allocation-accounting evidence, not performance measurements.

The saved independent audit reports 6,000 completed steps, 24,000 attempted and successful nominal stages, 6,000 safety records, 2,000 controller records and 1,536,000 derivative/load rows. The record total reconciles as 8 initial records, 8 case-end records, 2,000 controllers, 24,000 stages, 6,000 endpoints and 6,000 safety records. Stage rows equal 24,000 × 64. Projection/root rows equal (24,000 + 6,000) × 64 = 1,920,000. All 4 × 64 × 17 = 4,352 original initial words and the same number of own-state segment-boundary words were checked. All four paths reached their boundary and final horizon. The audit reports zero one-ULP root differences, zero native queries and zero new numerical producer calls by the auditor.

The audit reconstructed saved nominal loads, projections, motor-lag and rigid-body derivatives, and projected RK endpoints under the frozen arithmetic policy. Zero observed root differences does not expand the policy into an exact-rational, cross-platform or formal trajectory proof. The scalar helpers' adaptation from an earlier independent Python audit remains disclosed.

The auditor did not regenerate the initializer, neighbor membership, Boids steering, controller numerical law, saturation decisions or contact geometry. Initial-state word equality and controller/safety record linkage were checked; unchanged controller/contact implementations remain reused trust. Existing coupled trajectories and native-model evaluation were not rerun. Their published audits/exports remain the stated baseline trust boundary. A passed nominal safety record is not an independently certified safety assessment.

## Outcomes and claim limits

The following are the last common saved endpoints, not a comparison between different terminal times. Audit and export retain both actual timestamps and safety flags. The first-seed coupled endpoints are integration-complete but have a failed safety flag; the corresponding nominal endpoints pass the recorded check.

| Seed | Step size | Last common time | ID17 center height, nominal | ID17 center height, coupled | Mean-height difference, nominal minus coupled |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026102001 | 0.005 s | 4.6200 s | 3.136160 m | 0.074745 m | 1.746865 m |
| 2026102001 | 0.0025 s | 4.6175 s | 3.136096 m | 0.074935 m | 1.746210 m |
| 2026102002 | 0.005 s | 5.0000 s | 3.676985 m | 1.733773 m | 1.816600 m |
| 2026102002 | 0.0025 s | 5.0000 s | 3.676985 m | 1.733773 m | 1.816600 m |

The summary's rounded values agree with the saved report. First-seed nominal paths subsequently end at five seconds with ID17 near 3.146599 m; that later endpoint is kept separate from the table's common-prefix comparison. Coupled per-frame vertical velocity is unavailable in the reused replay representation, so comparison fields remain null and no velocity difference is invented. Coupled terminal vertical velocities exist separately in the final-state summaries. Contact identities are likewise null in the new export, with an explicit disclosure; the prior documented floor/vehicle stops remain preserved evidence.

Same-seed nominal coarse/fine maximum center differences are 6.993331217939613e-08 m and 4.9158113849045804e-08 m over 1,001 matched endpoints per seed. They describe endpoint sensitivity for these paths. They establish neither convergence order nor continuous-time error bounds, physical accuracy or independent replication.

The accepted interpretation is that changing the implemented load selection changed the first configuration's stopping outcome under the fixed computational protocol. Each arm reacts to its own changing state, neighbors and commands, so the contrast includes that downstream feedback. It does not isolate force, torque, motor lag or a particular controller defect. The no-causal-attribution fields are consistent with the disclosed absence of isolated mechanism or physical attribution.

`SUMMARY.md`, `RESULT-CLAIMS.md`, `RESTART-RESULT.md` and the latest root restart entry preserve the two exposed seeds, dependent resolution checks, reused baseline, computational-only scope and unfinished overall goal. The diagnostic was motivated by observed descent; it is not held-out confirmation or population evidence. Nominal completion does not show native-domain admission along those nominal trajectories. No real-air magnitude, validated controller cure, general safety, novelty, first off/full comparison, new flocking algorithm, speedup or scalability claim is supported. A possible vertical-tracking follow-up requires its own historical check, prospective bounded protocol, review and public source freeze.

## Display and privacy review

The saved UI report passes seven groups with no recorded page, console or HTTP errors. Its 11,779 checked arm buffers reconcile to 6,004 nominal frames plus 5,775 preserved coupled frames. The two first-seed coupled suffixes contain 76 and 153 unavailable states, totaling 229. Each arm's frame count equals its completed steps plus the initial endpoint; final frame steps/times match the outcome metadata. No missing coupled suffix is represented as continuing motion.

I inspected both saved full-page PNGs without launching a browser. Desktop shows two labeled flocks, ID17 trails, the z=0 floor and matching 4.6200-second labels; the contrasting heights are visible. Mobile stacks the panels, retains the controls and limitations, and shows no clipped page content. The narrow table wraps seed/time cells and the background drones are small dots at default zoom, as `UI-QA.md` discloses. The body radius, visibility halo, omitted factory obstacles and held-endpoint playback are described in the interface. The screenshots alone do not prove controls or every frame; those checks rely on the closed UI report and its previously reviewed source. No new browser or platform variant was tested.

- `ui/desktop.png`: 231,171 bytes; SHA-256 `d2d5f06f1722778b1129fa6a6d9f7b7f7bcf409a11c1fec5ada4ae9c8c354a56`.
- `ui/mobile.png`: 217,925 bytes; SHA-256 `6eb7a7943ff98657b4486a093484133ea5fb661f34adc2a8bf611ce71323e13f`.

`UI-AVAILABILITY.json` records the owned browser and process group absent, replay HTTP 200 and zero additional browser launches. I read this cleanup evidence without relaunching or probing the service. The saved captures contain no unrelated private content. A scoped scan of 47 source/result text files found no tested private home/temp paths, private-key headers or common token patterns. This was not a compressed-journal content scan or a universal secret-detection guarantee; the synthetic journal schema and the parent's result privacy review remain relevant.

## Publication condition

The final result manifest and exact-public result receipt were not yet present when this review was performed. The result must not be described as fully public-verified until the final manifest covers all 44 unchanged raw parts, the source/provenance closure, audit/export, phase closure and locks, viewer evidence, review, privacy and restart material, and that final identity receives separate exact-public verification.

`PUBLICATION-PLAN.md` appropriately separates bounded Git transport batches from the scientific allocation. Intermediate archive commits do not establish a complete published result. A transport failure may be repaired without changing or rerunning scientific evidence. Preserve every frozen source, raw part, prior failure, lock, receipt and coupled stopping outcome. All current producer/audit/finalizer/display allocations remain closed.
