# Independent prospective protocol and source review

21 October 2026. Package: `research/m31-vertical-memory-2026-10-21`.

**Disposition: source accepted for the prescribed producer, audit, finalizer and display allocations, conditional on complete source/input freeze, independent manifest coverage verification and separate exact-public source verification before launch. No source-level blocker remains in the candidate identified below.** No numerical outcome is assumed, and every earlier allocation stays closed.

This review covers the protocol, configuration, motion wrapper, producer, byte gate, supervisor, independent auditor and contract, finalizer, paired viewer/UI checks, runtime metadata, source reuse, historical/literature assessment, claims, privacy and restart instructions. Relevant inherited controller, adapter, native-load, physics, initialization, steering, safety, storage and baseline provenance sources were inspected. Python abstract-syntax parsing, JSON parsing and five JavaScript syntax-only checks passed. No scientific module, initializer, controller, simulation, native query, audit, storage qualification, finalizer or browser was executed. Only this review was written.

## Question and historical scope

The question is whether one fixed bounded vertical-velocity memory term changes the recorded outcome on the already exposed failing N64 configuration while retaining full current aerodynamic coupling. The selected seed is 2026102001, run in order at h=0.005 and 0.0025 seconds for at most five seconds. These are dependent resolution checks of one selected configuration. Seed 2026102002 is prospectively excluded; no claim about its response is supported.

The historical assessment identifies earlier fixed-altitude PD tests, horizontal position feedback and gain search, force/moment ablations, short current-adapter N64 qualification and the completed nominal/coupled comparison. Its absence finding for a completed integral vertical-velocity intervention is limited to the named inspected scope. The new diagnostic is outcome-selected, not held-out confirmation, a first feedback experiment or a novel integral method.

The nominal result is used as motivation, not as a newly executed or displayed third arm. Its final public manifest/receipt and summary match the identities required by the new auditor: result commit `d04ca0f763529ae694373da48b7aab48fd7fc0f8`, 148 pins, 30,926-byte manifest and SHA-256 `b65c8d868a8d6cc31733ac840ee3c37c1a23c157541e98b4977460b3e33aca0e`. This review checked the saved metadata binding without repeating network verification or reading that result's raw trajectory.

The retained literature distinguishes previously verified sources from a new search, preserves their reading dates and limits, and does not attribute this accumulator law or its gains to those papers. No specifically verified PI/anti-windup source is asserted. The claim ledger correctly excludes physical airflow accuracy, real-flight safety, general stability, controller optimality, population reliability, novelty, speedup, scalability and overall research completion.

## Exact intervention and state

The new motion wrapper retains the inherited own-state local 3D Boids, neighbor lookup, wall-priority filtering, horizontal targets, yaw construction and F.control call. The safety function body was independently compared and is byte-identical to the continuation wrapper. The added behavior is per-drone integral/error/count state, exact target-z correction, global controller indexing and corresponding evidence records.

Each of the 64 memory records starts with positive-zero integral and previous error and update count zero. The first update contributes positive zero. Later updates use exactly `(2.5*.01)*previousError`, then add to the saved integral and clamp to [-5,+5]. Only afterward is the current `desiredVz - vz` stored for the next update. The exact target is `z + ((2.5*desiredVz + 1.5*vz) + I)/6`. The auditor repeats that operation grouping and checks every saved before/increment/unclamped/after/target word, including finite computed intermediates.

Before limits, explanatory real arithmetic gives the intended vertical correction `2.5*(desiredVz-vz)+I`. That algebra is not substituted for the frozen target-based computation. The integral gain 2.5 s^-2 and inherited proportional coefficient 2.5 s^-1 define a one-second P/I ratio. The ±5 m/s² integral bound is a fixed choice based on the magnitude of the existing positive acceleration cap, not a fitted, optimal or stability-certified value.

The inherited net vertical command clamp remains [-4,+5] m/s², followed by unchanged attitude/tilt and motor mixer behavior. The accumulator bound is separate. Integration is not conditional on actuator saturation and has no back-calculation term; it is not saturation-aware anti-windup. Unfavorable clipping or transient behavior must remain an observed result rather than trigger gain or bound changes.

The producer initializes each physical path once through the pinned initializer, then evolves its own states. Each complete initial 64×17-word input must equal the corresponding saved original input. Memory resets only between the two resolution paths. The two segments are local 0..1 with origin zero and local 0..4 with origin one. At the join, every physical word and integral/error word is encoded and reparsed without extra normalization; update counts also carry exactly. The auditor binds the second initial record to the candidate's own first terminal record, not to the old coupled state.

The controller is due at local zero in both segments, but global index continues from 99 at t=.99 to 100 at t=1. The t=.99 error is integrated once at the join. No endpoint-only memory update is invented. If both paths complete, there are 500 controller records per path, 1,000 total, 64,000 memory rows and 63,872 prior-error integrations. These are conditional full-horizon counts, not acceptance assumptions. Physical state alone is no longer a sufficient restart state.

## Coupling, stopping and raw evidence

The producer calls only native method F through the unchanged coupled adapter. Motor lag, quaternion projection, nominal reaction yaw, arm moment, gyroscopic terms and projected synchronous RK integration remain inherited. No load inversion, aerodynamic feedback into the controller, warmup or extra endpoint force query is introduced.

Static traversal of the producer's literal CommonJS dependencies reaches 17 files: three new files and 14 inherited files. All 14 inherited files match the prior continuation source pins, including native-load and its kernel dependencies. The final source manifest must cover this closure, not merely the edited files. Runtime metadata names the same previously checked Node executable identity: 121,304,480 bytes, SHA-256 `d0c6c74401e6a544bb4d4b2a9ded9c43298d4e6dcd5ebac4dd010c4c81774105`. The producer verifies the executable bytes and restricted launch environment before scientific imports.

Every reached initial, controller, stage, completed endpoint, safety and case-end record is retained. A full allocation has at most 3,000 completed steps and 12,000 attempted stages/native F calls. The first endpoint with inherited safety issues stops that path, preserving all returned issues and the triggering completed endpoint. No second segment follows a first-segment stop.

A saved native domain/input/numerical refusal stops the path only when the failed adapter stage and native status have the prescribed structure. The refusal remains distinct from endpoint contact and from a successful horizon. The attempted RK step produces no completed endpoint or safety record. Physical state remains the last completed endpoint, while memory remains the most recent emitted controller state, including an update immediately before refusal. The auditor verifies this deliberate lack of rollback and preserves the refused trial separately. Unexpected exceptions, resource failures, malformed native output or persistence errors close the entire allocation. Only a structured path stop permits the remaining prescribed resolution path to proceed.

The unchanged qualified Journal retains its 16 MiB raw blocks, at most 32 MiB compressed parts and 4 MiB record cap. No storage trial is repeated. Raw/compressed hashes, ordered parts, line provenance and exact record order are audited. Unexpected termination can still leave incomplete buffered evidence; that is a failed closed allocation, not permission to reconstruct a successful suffix or erase a failure.

## Independent auditor and its limits

The completed `source/audit.py` and `AUDIT-CONTRACT.md` match the author's final identities in the table below. The auditor imports neither producer JavaScript nor an earlier audit. Its scalar/native/projection/derivative helpers are reused or adapted from the independent continuation auditor, and its segmented reader/provenance/join code derives from the nominal auditor. Independence is from the JavaScript producer; those helper ancestries are not a third independent implementation.

The auditor checks fixed configuration, complete producer closure, source/runtime metadata, exact source pins and transitive relative dependency coverage. It follows those dependencies as text. Its independent streaming reader checks whole-part bytes before consumption, contiguous names/offsets, complete aggregate compressed/raw hashes, newline-bounded records, duplicate-key/nonfinite-number rejection, exact sequence and prescribed record order. Extra result files or mismatched supervisor byte accounting fail. Source, closure and raw-part identities are rechecked before a passing report is emitted.

New memory arithmetic is independently reconstructed for all reached controller rows, including current-state/desired-velocity bindings, previous-error use, signed-zero initial words, exact clamp/target grouping, global counts and initial/boundary/terminal snapshots. The inherited actuator controller is not rerun. Neighbor shape/order and x/y target bindings are checked, but neighbor membership, Boids steering, yaw trigonometry, actuator law and saturation decisions remain reused source trust.

For each reached native stage the audit checks method/schema/model, canonical input hashes and stage binding; constants; prepared centers/axes/rotor offsets and points; projected motor forces/totals; coefficient dimensions/order and saved scale arithmetic; saved alpha sums; rotor force products; collective/world force and moment; and the consumption checksum. Successful evidence must report admitted/descending diagnostics and residual diagnostics within the inherited limits. The audit does not independently regenerate geometry-derived K coefficients, native root solves or the residual model. Its reported scope must not be expanded into a fresh aerodynamic-law verification or interval reference solve.

Every successful derivative consumes the same-ID native loads. The auditor reconstructs body arm moments, unchanged nominal reaction yaw, total torque, gyro terms, all 17 derivative components, weighted RK endpoints, projection and next-state binding. Basic arithmetic compares exact binary64 words under the frozen grouping. Positive saved roots may differ by at most one ULP from Python's reference and are then used downstream. A refused stage lacks saved per-row norm evidence, so the audit tests the reference root and its two adjacent candidates against exact projected words and counts that reconstruction. It does not claim to recover a saved norm. Native root-two constants use the disclosed candidate policy. None of these checks establishes an exact-rational, cross-platform or physical error-bound proof.

A refusal has no consumable native load/solution/checksum or derivative rows. Its available preparation/coefficient evidence, reason and stage are checked; thrown, malformed or unexpected native statuses fail. Attempted stages reconcile to four times completed steps plus the refused stage index, with successful/refused counts kept separate. The separate refused trial never enters completed-frame comparisons.

Safety checks validate saved issue fields and linkage without regenerating swept-contact geometry or vehicle-limit decisions. First recorded failure, case-end, index, final physical state and latest memory must agree. A passed audit can therefore establish correctly recorded refusal/contact evidence; `passed`, `allMemoryPathsCompleted` and `allAttemptedNativeStagesAdmitted` are intentionally separate facts.

## Baseline reuse and comparisons

The comparator remains the old public coupled paths, pinned to original commit `637c25294f162bea39970d12df0206f25dead889` and continuation commit `a0f595f34a4f9ef8cef516caa0cde60053e0eade`. Their exact manifests, receipts, audits, indexes, replay exports, exits, supervisors, closure records and storage qualification are required. Their previous audits remain reused trust. Only the selected two original initial-record prefixes are extracted after whole first-part verification; the old coupled trajectories are not rescanned or re-audited.

The selected coupled join retains 2,773 frames: 925 coarse and 1,848 fine. Exactly one duplicate continuation initial frame is removed per path, while original t=1 remains. Saved clocks, integer global steps, boundary positions and final positions are checked against the old indexed states. This does not newly check every full coupled boundary word; prior full-state continuation evidence is reused.

Candidate-versus-baseline position differences use the last integer step available in both corresponding completed lists, preserving both actual timestamps and safety flags. Terminal summaries are separate. Initial step zero remains a valid comparison if a new path refuses before completing a step. Refused trial positions and missing suffixes are never substituted for completed endpoints.

Candidate coarse/fine sensitivity pairs coarse step k with fine step 2k through their common completed prefix. The maximum is over saved endpoints and vehicles, not continuous time. No independent-trial, convergence-order or physical-accuracy claim follows.

Candidate controller observations export mean absolute vertical error over its own 64 saved references and integral minima/maxima. Baseline exports do not contain corresponding fleet desired velocities, so the source correctly avoids matched fleet tracking-improvement claims or hidden new baseline extraction. Coupled intermediate ID17 velocity and contact identities remain null with disclosures; the prior final full state supports a separate terminal velocity. Each arm's later neighbors, desired velocities and commands can diverge, so the intervention measures total own-state feedback consequences, not isolated force, torque or one controller mechanism.

## Budgets, closure and display

| Allocation | Successful wall including cleanup | External termination | Output cap |
| --- | ---: | ---: | --- |
| Producer | 1,800 s | 1,820 s | 3 GiB, including 1 MiB closure reserve |
| Audit | 1,800 s | 1,820 s | 128 MiB |
| Finalizer | 120 s | 140 s | 2 MiB plus at most 64 KiB viewer pins |
| UI | 150 s | 160 s | 16 MiB |

Exclusive locks and new output directories enforce single attempts. Supervisors terminate/reap the owned process group and count cleanup in the success wall. A zero-return child exceeding wall/output caps still fails. Optimized Python is explicitly rejected by the audit, supervisor and finalizer. The existing localhost server stays outside the allocation's owned group.

Verified byte reads allow at most three attempts per operation before bytes are exposed. Separate before/consumption/after checks have separate bounds. Parsing, arithmetic, browser launch and whole allocations are not retried. Producer/audit events and finalizer/UI gate records retain anomalies, including failed gate attempts. Finalization requires passing closed producer/audit evidence, a complete index, no failure files and exact audit/export binding. UI checks additionally require passing finalization and recheck pins/gates before and after. Browser code verifies loaded bytes and producer/audit supervisors before displaying evidence.

The viewer's candidate pane is full coupling with memory, not the previous nominal/off arm. It displays only initial/completed endpoints, actual saved timestamps, ID17 and its trail, and the modeled floor extent 102×20 centered at (-9,0,0). Unavailable suffixes hide cloud, highlight and trail. The physical 0.075-radius body and larger visibility halo are distinguished; other factory obstacles are omitted.

Review identified a refusal-label ambiguity: a failed trial may occur after the last completed endpoint. The corrected source now labels native refusal outcomes with the last completed time and separately shows refused trial time/status/reason. It never inserts those trial positions into the completed path. Terminal stop categories are displayed, and UI checks verify their presence; if a refused frame occurs, checks also verify its separate time/status/reason. These corrections are included in the candidate identities below.

The sole UI allocation checks every displayed float32 position buffer against saved positions converted to float32, actual times, floor/ID17, suffix absence, outcome rows, selection/playback, orbit/reset, desktop/mobile overflow and captures, page/console/HTTP errors and corrupt-data refusal. These are prospective checks, not observed successes or GPU-pixel/binary64-rendering guarantees. Screenshot inspection and cleanup/availability evidence remain result-stage requirements. Browser, Python, operating-system and system-library dependencies are not a hermetic frozen runtime; no portability or performance claim is accepted.

## Freeze and publication conditions

The 19 candidate text files were scanned for tested private home/temp paths, private-key headers and common token formats without a match. This is a scoped source check, not a universal secret-detection guarantee. This review, final manifest, later logs and screenshots require their corresponding privacy checks.

Before launch, freeze this review and every candidate below, complete transitive scientific/byte/viewer dependencies, exact baseline/publication/storage evidence, descent input descriptors and required original first parts, motivating nominal evidence, and historical/literature provenance. Independently verify coverage and every pin. Then commit/push and separately verify the exact-public source manifest/receipt. Local hashes or this review alone do not establish public availability.

After execution, require closure gates, independent saved-result review, screenshot/privacy inspection, a complete result-byte manifest and separate exact-public result verification. Preserve all old and new failures, raw records, locks and receipts. No failed allocation may be reopened by editing this frozen package. Any later gain, bound, seed, horizon or algorithm change requires a separately specified prospective study.

## Reviewed candidate identities

Paths are relative to this package. These source-only identities precede creation of this review.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `AUDIT-CONTRACT.md` | 21,905 | `ed5e5e6ef96d322bc74db1228a9bca6af7830313a9b2f372780aaf27989f48ea` |
| `CLAIMS.md` | 1,307 | `398b252f760b8131fdf6419e9b43b9daf900670af3a0fc48b5b2831cdb8cfd68` |
| `HISTORICAL-CHECK.md` | 8,667 | `3bbb4e9259ecaa47e6957fa03f1ae80a82f9492469fb31978c34326fe9ed7563` |
| `LITERATURE.md` | 5,062 | `a38f5967695c0f8a93ae2771f6c39f52d793c1ec4ef2518a500dd37a30addbef` |
| `PRIVACY-SOURCE.md` | 804 | `910d5b64bda3f3e20c85982491408d74bbf0d626fedf49b720ae7faf9958073e` |
| `PROTOCOL.md` | 7,893 | `0c94e0f22890980c8ed0575622fa740932f66ce71d4794628b2ca0d55cdbf348` |
| `RESTART.md` | 1,730 | `6129730adb4f803eefc096f1799c38a44bffb82d320bcf0fb0ad006541adfaeb` |
| `SOURCE-REUSE.md` | 2,253 | `e9029ec12790d2df276550f421dbc47d17282114913027a67f8e1e2eac42b89b` |
| `config.json` | 908 | `ebd8a8dd14cc492abe5297712eaf7d7d094e18b186c2ad94a7a6fe3006d634a5` |
| `runtime.json` | 113 | `8347eef171a70a8e9ecd298684ee4c8e445b907aeb61630a26d105670641d225` |
| `source/audit.py` | 78,076 | `0cc9f4fd5bc6c99bc924da0fa5d71b3356c69b09988b3e0d7cf659329cf0482d` |
| `source/finalize.py` | 2,395 | `440403f858a1b9ef51d96ac6148d667baa328038a3ece23a751ea2afe1908374` |
| `source/gate.cjs` | 1,271 | `91b158731394a60a87f131ac28102acdc5143e5369c945bc1b4baa2a4e2916ab` |
| `source/motion.cjs` | 3,848 | `f7966691b52f2e14c2fbba82ed136fc99cf7a87b8d53725e08be9923128cea16` |
| `source/run.cjs` | 6,746 | `a17f177c2ea84f8224885868529689ff131015d65dad788eb24a42481cee83ef` |
| `source/supervise.py` | 2,145 | `36ab0742dfd0563b452ce921107779d675c457101f313c5dc39397a35e7d8f61` |
| `source/ui.cjs` | 8,234 | `e15d96720eb10a616d77d357edc43132ff0cdcb2759077ccf3f4eee955d0ac77` |
| `viewer/app.js` | 7,952 | `4f46ab76a1516010003035c3ded7a2f506da64fd5d028d79163d196300946fe3` |
| `viewer/index.html` | 4,722 | `41b3ac0f84cbfa200e29411031119a5c6ea60d7a7b64fb3b785ac08efe079f4d` |
