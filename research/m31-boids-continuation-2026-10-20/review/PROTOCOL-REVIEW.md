# Independent prospective continuation review

20 October 2026. Reviewer: the independent protocol/source review agent. Scope: the new `research/m31-boids-continuation-2026-10-20` package, before source freeze or any of its allocations.

**Disposition: suitable for source freeze and public verification, subject to the execution gates below. No remaining source-level blocker was found in the reviewed scope. This is not a storage qualification, numerical result, completed audit or display result.**

The review read source and retained small evidence files, compared source text and hashes, parsed JSON and Python syntax, and used the pinned Node executable only with `--check`. It did not import or execute scientific modules, invoke an initializer, perform a native query, decompress prior journals, run the new auditor, run storage fixtures, launch a browser or execute an archive allocation. No earlier frozen file was changed. Only this new review document was written by this reviewer.

## Scientific scope and fixed workload

The question is a defensible conditional continuation of exposed computational paths. All four prior paths remain in the workload and denominator. They are not new independent trials or held-out replications. The fixed additional four seconds may expose an admission or inherited contact/vehicle limit during further motion, but success would establish only persistence along the prescribed discrete paths under the implemented calculation.

The cases remain seed-major: `2026102001` at h=0.005 then h=0.0025, followed by `2026102002` in the same resolution order. Each coarse case has at most 800 additional steps and 3,200 native calls; each fine case has at most 1,600 steps and 6,400 calls. The maximum is 4,800 additional steps, 19,200 native calls, 1,600 controller updates and 30,408 journal records. These are prospective maxima, not observed counts.

The five-second total horizon is not a claimed physical timescale, convergence test, new flocking mechanism, safety certificate or large-swarm result. No new native formulation, controller tuning, alternate arm, optimized cache, speed comparison or post-result extension is introduced. The earlier descent remains exposed evidence with an unisolated cause.

## Exact continuation provenance

The prescribed prior result commit is `637c25294f162bea39970d12df0206f25dead889`. The retained public receipt identifies the 20,563-byte, 100-pin result manifest with SHA-256 `a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b`. This review independently checked that manifest hash and the current local bytes of its selected index, audit, allocation closure, two internal exits and two native/audit supervisor receipts against their published pins. It did not repeat the remote fetch or prior scientific audit.

All four selected prior cases are completed at t=1, with 200/400 steps and canonical IDs 0 through 63, each retaining 17 state words. The producer restores `prior.finalInput.drones` through the unchanged adapter's binary64 word decoder. It preserves the saved IDs, positions, velocities, quaternion, angular rates and all four motor states. The decoder uses `DataView` and preserves signed zero. No initializer, first-second replay, fine-to-coarse reset or restoration-time quaternion normalization appears in the new runner.

The producer binds the selected prior files to the prior manifest and receipt before importing scientific modules. It requires passing prior audit/index state, one closed-passed allocation in each prior closure phase, and successful prior native/audit internal and external receipts within their original limits. The new auditor additionally fixes the known prior manifest identity, matches prior case configuration and outcomes, binds the earlier audit's saved index/exit/supervisor pins, and compares every new initial input object to its own prior `finalInput` word for word. The current source manifest must include those selected prior files and the receipt. This is explicit reliance on the published prior audit, not a claim to re-audit its entire closed corpus.

## Controller, clock and integration semantics

The new `control` and `safety` function bodies match the corresponding functions in the qualified `m31-coupled-stage-qualification-2026-10-17/source/browser-driver.cjs` exactly after stripping only surrounding whitespace. The steering, physical controller and safety functions operate from supplied states and fixed parameters. They do not require the preceding controller command, a hidden random generator or a global trajectory clock.

At relative step zero, the controller is recomputed from the saved t=1 endpoint. This is the due 0.01-second control update at original t=1. The local control index restarts at zero. The returned commands remain held for all four RK stages and the prescribed two or four integration steps until the next controller update. In particular, a k4 stage at the next controller timestamp still uses the old held command.

The unchanged adapter performs whole-swarm projected RK4: it projects each raw trial before the native query, consumes the same-stage delivered loads, constructs the weighted endpoint and projects that endpoint. There is no additional native query at an endpoint or at the final state. The final endpoint can therefore remain unqueried.

The local duration is four seconds with `timeOrigin=1`; stage and endpoint original-time words use `1 + relativeTime`. The auditor checks the frozen arithmetic for controller, stage and endpoint time words. Endpoint arithmetic uses `stepIndex*dt + dt`, while nominal completed horizon uses `completedSteps*dt`; the export retains the recorded endpoint time. These expressions need not have identical words in every case. The package correctly avoids a claim of bitwise identity to a hypothetical uninterrupted run using global step indices.

The source forces the wide factory variant and rejects conflicting inherited settings. The literal relative dependency closure rooted at the new runner and motion wrapper contains 16 files: the three new run/motion/journal files and 13 inherited files. The inherited adapter, native-load, physics, simulation, grid and geometry hashes match the explicit immutable identities in the auditor. No substitution of `S.initial`, `S.run` or `F.integrate` occurs in the new runner.

## Stop classification and durable closure

A structured native `domain-refused`, `input-refused` or `numerical-failure`, carried by the adapter's failed `native-non-success` stage, stops that case. The runner retains the failed stage, does not advance the completed endpoint, emits the case-end record and proceeds to the next predefined case only after the journal is finalized. The auditor requires the matching failed-stage envelope, projected trial, zero consumed derivative rows, refusal descriptor and immediate case-end. Unexpected native evidence, thrown failures and incomplete allocations cannot pass the saved-evidence audit.

An inherited endpoint contact or vehicle-limit report retains the newly computed endpoint and its safety record, increments completed steps and stops the case. The display marks that endpoint separately through `safetyPassed: false`. These checks are the existing endpoint-segment contact envelopes and vehicle conditions; they do not certify curved continuous trajectories or physical flight safety.

Resource, persistence and unexpected implementation failures end the allocation. They are not turned into a native refusal or a replacement path. The runner's failure metadata now calls the count `acknowledgedRecords` and exposes `pendingRawBytes`; it does not mislabel buffered records as durable.

The unchanged adapter contains a historical “durable append” comment, but this package deliberately supplies a buffered callback. The prospective protocol and audit contract explicitly state the effective semantics: successful append can mean a complete record is still in memory; successful complete-case closure requires `finish()` to flush pending blocks, sync and close the parts, then return the full identity before the case index entry is added. That documented change in persistence semantics must accompany any description of the unchanged numerical adapter.

A crash or budget/persistence failure can leave acknowledged records absent from disk, or leave an incomplete compressed member. Such an allocation stays incomplete and failed. The absence of a final success index or matching raw/part identities is not permission to repair, retry or reinterpret it as a scientific outcome.

## Lossless parts and prospective storage qualification

The writer serializes each complete JSON record once with its newline, enforces the 4 MiB raw record cap, and groups whole records into gzip members with at most 16 MiB raw input. It writes compressed bytes directly across ordered physical parts of at most 32 MiB. The part boundary is independent of gzip-member and JSON-record boundaries. The output includes each part's offset, length and SHA-256, the compressed aggregate length/hash, the raw aggregate length/hash and the record count. No duplicate whole scientific journal is created.

Output charging precedes writing each compressed block. Full parts are synced on closure; the final partial part is synced during `finish()`. A write, sync, compression or budget error propagates rather than producing a completed case identity. Storage reconstruction instructions correctly require concatenating parts in order, never decompressing a physical part as an independent gzip file.

The new storage qualification is an explicitly separate, one-attempt allocation using deterministic synthetic byte fixtures and no scientific imports. Its source checks exact JSON-line reconstruction by independent Python gzip decoding, multiple raw blocks and physical parts, part offsets and identities, record sequence, oversize-record refusal and compressed-budget refusal. The smaller fixture boundaries exercise splitting; production defaults remain fixed. This source review did not execute that qualification or establish its result.

The auditor's independent forward-only `PartReader` supplies one compressed stream to `BufferedReader` and `gzip.GzipFile`. It checks per-part identities at each EOF, the aggregate compressed identity at final EOF, and raw line lengths/hashes while decoding. The terminal read requires stream exhaustion and verified compressed EOF. It also rejects unexpected result files and rehashes physical parts before a pass. It does not materialize a duplicate whole journal.

The contract accurately limits that check: the audit does not separately infer or measure the raw size of every gzip member. Group-size behavior is established by the frozen writer and the planned synthetic qualification; the scientific audit verifies the resulting identities, decoded records and schedule.

## Allocation and downstream gates

| Phase | Success wall limit including supervisor cleanup | External termination | Saved-output cap |
| --- | ---: | ---: | ---: |
| Storage qualification | 20 s | 25 s | 8 MiB |
| Native producer | 1,200 s | 1,220 s | 3 GiB |
| Saved-evidence audit | 1,200 s | 1,220 s | 64 MiB |
| Display | 150 s | 160 s | 16 MiB |

The producer reserves 1 MiB within its result cap for index/closure files, checks the 19,200 native-call limit, and includes source verification and final checks in its internal timer. External supervisors own separate process groups, kill remaining children after completion or timeout, record allocation-wall and output-cap results, and convert output-cap overrun into a nonzero reported result. Exclusive launch locks and output creation prevent a second attempt.

The storage gate must pass and close before scientific imports. Native completion and internal/external closure gate the audit. A complete producer can contain an orderly scientific stop; a resource or persistence failure cannot be admitted by the audit. The auditor binds new storage/native receipts, checks declared output bytes against actual result files, verifies all prescribed cases and rejects a failure-bearing producer index.

The finalizer and UI require the passing audit, zero-exit closed audit receipt, passing external allocation-wall and output-cap flags, and absence of a late audit failure. The finalizer compares the export's computed pin to `audit.viewerPin`; it cannot simply repin altered viewer data as though the audit had checked it. The UI repeats that binding and verifies the pinned bytes. The browser checks the export pin against the audit before rendering. The UI reserves room for QA output and the supervisor independently checks its final directory cap.

The reviewed sources do not prove these future phases will finish within their caps. Their pass/fail receipts and retained locks must determine the actual outcome. A timeout or failed qualification closes the respective allocation and must not trigger a retry, source patch under the same freeze, or continuation to a downstream phase.

## Audit meaning and reported observations

The inherited numerical audit routines remain the prior saved-binary64 consistency checks, with changes for the continuation clock and added saved-data descriptors. They bind projected inputs, saved preparation, delivered loads, commands, all derivative words and RK endpoint arithmetic. Recorded square roots retain the declared one-ULP comparison policy; a refused projection reconstructs only the permitted norm candidates because the adapter did not save that norm.

This is not an exact rational reference calculation. It does not regenerate the initializer, neighbor membership, Boids steering, controller law, native geometry coefficients, native root solve, residual model or contact geometry. A passing audit cannot independently validate admission or physical accuracy merely by checking schemas and surrounding arithmetic.

The prospective descriptive outputs are appropriately bounded:

- Continuation-start to last-completed-endpoint center, vertical and COM-removed displacements exclude refused trials and do not imply a continuous-time maximum or causal explanation.
- Directed neighbor additions/removals compare consecutive saved controller sets within this continuation only. Saturation counts are saved update/vehicle records, not duration-weighted saturation.
- The orientation descriptor is the minimum saved completed-endpoint rotated body-axis z component, with a separate initial minimum and null completed value/location if there is no endpoint. It adds no normalization, clipping, angle conversion or threshold.
- Positive aerodynamic edge turnover is explicitly not measured.
- Same-seed comparisons match integer coarse step k to fine step 2k, include the inherited initial discrepancy, and stop at the common completed prefix. They do not reset paths, interpolate, extrapolate or establish convergence order.

## Viewer and claim boundaries

The all-endpoint export is frozen prospectively, with a maximum of 4,804 initial/endpoint frames and a larger 64 MiB audit cap. This is an acceptable alternative to endpoint subsampling. The renderer consumes only saved positions, holds frames between recorded times, distinguishes refused trials from completed endpoints, and labels the displayed clock as relative to the continuation beginning at original t=1. The audit export also contains original-time fields.

The UI source checks all exported position buffers against float32 conversion of the audited coordinates, exact result rows and outcome labels, safety-stop frame text, case controls, playback, orbit/reset, desktop/mobile overflow, and corrupted-export refusal. A saved refused trial is checked only when one actually exists. No empirical claim about that branch or any screenshot can be made from this source review.

The protocol, claim ledger and page correctly retain physical-model limitations and avoid novelty, real-flight safety, speedup, large-swarm scalability and whole-research completion claims. The literature record reuses the previously verified sources and explicitly allocates no new external search. This review made no new bibliographic verification.

## Review checks and resolved issues

The initial review identified incomplete producer binding of prior closure evidence, ambiguity between buffered acknowledgement and durable records, and missing explicit UI output-cap enforcement. The candidate was corrected before this review was written. Further alignment added explicit downstream output-cap flags, prior allocation-closure checks in the auditor, mandatory display source coverage and precise axis-z descriptor wording.

Static checks completed:

- Six JavaScript files passed syntax-only `--check` with the executable whose bytes match `runtime.json`; four Python files passed `ast.parse`; both new JSON source files parsed.
- The inherited controller and safety bodies matched verbatim, and the literal relative run/motion dependency closure was enumerated without imports.
- The seven selected prior small-file identities matched the fixed published prior manifest; all four saved endpoints had the required complete state shape.
- The reviewed new text had no matches for the scoped personal absolute-path, private-key-header and common credential patterns. This is not an exhaustive secret-detection guarantee; final results and screenshots still need their own privacy review.
- At review time the new storage, results, audit and UI directories, their supervisor launch locks, and the new source manifest/publication receipt did not exist. No allocation result is implied by this document.

## Reviewed candidate identities

Paths below are relative to this checkpoint. These are the reviewed bytes before adding this document. Source freeze must include this review, the candidate, the full inherited dependency/display closure and the specified prior evidence; independent manifest coverage and public verification remain outstanding at this review boundary.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `PROTOCOL.md` | 8008 | `bf320d44ca2056ac5de2eb3969b3fb83ad40a44f58b67a697e2d9678632ebf8f` |
| `AUDIT-CONTRACT.md` | 20677 | `b5b3083a655b622be675b96be6b4dc5f138f44c98b3425d16efc95d55c6218c9` |
| `config.json` | 832 | `753719e831af158cadad27fdbfc297f0519f1490b8c02ad186702ae9c79fc7b5` |
| `runtime.json` | 113 | `8347eef171a70a8e9ecd298684ee4c8e445b907aeb61630a26d105670641d225` |
| `source/run.cjs` | 8997 | `2a7c59e559bd3031afcc1d2cd3b359cb1ee6700be338c42bdf8a5b01ef9a4080` |
| `source/journal.cjs` | 2689 | `689c3faae7a21fe0abf446b6260d907e1f92039688194c87ef7cb17bc3de0485` |
| `source/motion.cjs` | 2836 | `c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373` |
| `source/audit.py` | 61406 | `95e9f9c3d468c3cb45b8e975ae026c8f8256c7a0270279d07aa6ab551766d223` |
| `source/storage-test.cjs` | 2105 | `02f3ec994c1b60862699c51830efdeba98a3973f7129185510a57ef360da17fc` |
| `source/storage-check.py` | 2777 | `b6a8ff49b44dbe1b2c0d48305e8c6b4b0514b9e08b153c16fb7401f5132d2504` |
| `source/supervise.py` | 1923 | `9fc330bb91fa3894ffa4878ea4ac94b66f687ffef767809105ff536554119172` |
| `source/finalize-view.py` | 1205 | `d12e13d8349fa608f3bbd10cba63d04f457f832a55d9fcb7954ff0f4cc09f002` |
| `source/ui.cjs` | 8726 | `5eaa9734c3749e810661c2c96075aa94f7f17edc26695ac3746d4f4585437db8` |
| `viewer/app.js` | 6440 | `51ed54432f786bb799c2644cb5155cccc05efe093dacc621cea014b249a2d17c` |
| `viewer/index.html` | 4105 | `c711285821471c1a0dc2225a18219826ca2aa75045ae2afff50b97029110d4d2` |
| `CLAIMS.md` | 642 | `0680182108715263f55871130fc97ee70f395c02d79b88c39fa058133e3e12f7` |
| `LITERATURE.md` | 1837 | `64282092efd91619c0a0713b0f9763202d77a477c8f8d1a132e4c1c4c9e75190` |
| `PRIVACY-SOURCE.md` | 843 | `fbc6dc4a90ca8807d1c17b1e673ea69232600be4853b5dbabbcfbb1f504cdff3` |
| `RECONSTRUCT.md` | 792 | `2909685edde7e2d8e276307d5fa0c261643faf31d2dd23de716b71cae110f75f` |
| `RESTART-SOURCE.md` | 1553 | `00a98530b818c8c349eda602f3bb4cd251866cbcf00bc19bea425e708bc8d01c` |

Proceed only through the documented source-publication, storage, producer, audit and display gates. Preserve every completed or failed attempt. The next required evidence is a verified source freeze and the result of the single new storage qualification, not an assumed continuation success.
