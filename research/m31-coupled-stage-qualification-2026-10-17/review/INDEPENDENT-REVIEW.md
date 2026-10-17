# Saved-evidence review of the coupled-stage qualification

The saved record supports the prospective interface qualification for this exposed 64-drone, 0.02-second continuation. The source and result bindings checked here are consistent, the declared attempt completed without a recorded failure or retry, every required primary reference is present and admitted, and the separately authored checker reports all fixed gates passing. The actual saved words also show the required load-to-state-to-controller feedback path.

This reviewer authored the adapter and browser-driver draft. This is therefore a separate saved-evidence critique, not a review by an independent implementation author. The numerical arithmetic verdict comes from the separately authored checker. This review directly verified bytes, identities, counts and literal word associations, then made descriptive differences from saved values. It did not import or execute candidate, native, reference, checker or viewer code; rerun tests; use a browser, Git or the network; or alter scientific source or results.

## Exact record and binding checks

The source commit recorded throughout the attempt is `25cfcee43b02f88a021fe0bae59d07cabf5fc163`. The actual source manifest is 9,870 bytes with SHA-256 `d713bbe2535328553ed7e9dc7ce7fae2a8b04c8052d00f9edd1d20324b1f84f0`, matching the parent's dispatch identity and all stage outputs.

The standard-library-only review verified all 44 manifest file pins against actual bytes, all 14 byte-identical bundle slices, all 32 canonical primary input sidecars, all 32 per-stage reference files, and both descriptor journals. Paths, sizes and SHA-256 values matched. JSON decoding rejected duplicate keys and nonfinite JSON constants. Browser and reference journal sequences were contiguous and terminated with a newline. No missing, duplicate or replacement primary stage was found.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `results/run-attempt.json` | 2,571 | `1fb7cd665b3673b21c1701bfd6fa3aad039d6a383c1e8300f079a19cd69e7c4f` |
| `results/browser.json` | 10,935 | `7dd6baa5b297d1bc147a192c5af1792a911fb183e4c0b744f345b238311cd8f8` |
| `results/reference.json` | 1,418 | `0fcf612bde6a6b1a0e95d2a58481cc6b042d393fe118b4b5015952eb4b3b1ca4` |
| `results/check.json` | 218,691 | `bff01040bddc1c7ee8bd4d27b07d1594f4dbeffc36a07ee1f727a3d7e594f33e` |
| `results/browser-journal.jsonl` | 17,610,247 | `3d2a0d2fd1bdced5af676a53de25bd50bd980683cd76651e7b8c866d0e3ec9d5` |
| `results/reference.jsonl` | 16,854 | `59de1ccd2b134d5ec0a2f9383ffd85358eb75f25a6843fda7349856af0350556` |

The exact fresh-a-t5 input pin matched its original 21,955-byte file and SHA-256 `48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c`. Both arms' first accepted bases match its complete 64-ID/17-word state. Every primary sidecar contains the exact compact canonical nativeInput JSON without a newline, and its actual file hash agrees with the stage's semantic/inline hash. Every reference file binds that same sidecar and consumed state.

The saved source-publication receipt is internally consistent with the source commit, manifest, file count and chronology; its recorded verification precedes the attempt. This review did not independently repeat remote publication or Git verification. Hashes establish identity of the inspected local files and receipts, not truth of a remote assertion by themselves.

The companion `receipt.json` contains the complete directly cited artifact pins, canonical pin-list digests, counts, fixed affected-ID lists and saved-word illustration. At review closure it is 15,643 bytes with SHA-256 `58923d74d2f311ee450878a86621e2183d20cc23468faef6462e0b4a80341254`.

## Complete counts and reported gates

The browser journal has exactly 131 records: one source, one factory, one initial, 12 wiring controls, nine manufactured runs, three manufactured summaries, four controller updates, 64 main stages, one raw diagnostic, 16 main steps, 16 safety records, two arm summaries and one final driver summary. These counts match the prospectively declared schedule.

| Family | Saved outcome |
| --- | --- |
| Coupled stages/native F calls | 32 completed / 32 calls |
| Independent consumed-state references | 32 admitted, loads branch; none omitted |
| Off stages/native calls | 32 completed / 0 calls |
| Main endpoints and control updates | 16 endpoints; two updates per arm at relative 0 and 0.01 |
| Wiring controls | Five accepted and seven expected rejected; six successful single-drone derivative records |
| Manufactured controls | Nine complete runs, 84 steps, 336 stages, zero native calls |
| Saved-evidence corruptions | All ten detected at their stated checker layers |
| Arithmetic fixtures | 14 passing |
| Loader compatibility checks | Nine groups, 56 passing assertions |
| Safety records | 16, with zero recorded issues |

The checker's positive-audit counters are coherent with those records: 400 stage evaluations, 100 steps, 4,438 single-drone derivative evaluations and 75,446 derivative words. The 400 stages comprise 64 main full-swarm stages and 336 single-drone manufactured stages. The six wiring derivatives are additional single-drone records. The checker separately reports the small counter effect of negative saved-evidence controls, avoiding their inclusion as new primary cases.

Reference accounting is 516,096 logical rotor/source pairs, 237,056 executed scalar suffix calls, 2,048 prepared drone states, 8,192 root boxes and 22,528 signed load boxes. Logical coverage and scalar work are different quantities. The saved precision recipe is 192-bit coefficients, 192-bit sources and 128 bisections; maxDrones=180 is bound through the unchanged pinned spec and source preflight rather than repeated inside each three-field result recipe.

All four native load categories pass at every primary stage. The largest saved normalized upper bounds, displayed approximately, are:

| Category | Largest reported upper bound | Stage / witness |
| --- | ---: | --- |
| Rotor | 2.58842e-16 | step4-k2, ID 28, rotor index 1 |
| Collective | 2.75582e-16 | step6-k2, ID 24 |
| World force | 3.77771e-16 | step6-k2, ID 24 |
| World arm moment | 1.39775e-16 | step6-k2, ID 24 |

Each is below the fixed 1e-8 limit with reference uncertainty included by the checker. The largest saved body-frame moment upper bound is approximately 1.39976e-16; the conversion gates pass. These are decimal renderings of saved checker bounds, not newly generated reference calculations.

The saved coverage records explicitly state `zeroPredicatesReevaluated:false`. The coverage audit checks the partition, associations and saved records; this review does not independently reevaluate tree zero predicates, scalar coefficients or root arithmetic. The conclusion therefore relies on the pinned prepared-reference implementation and its earlier qualification, together with the current saved arithmetic/coverage audit. It must not be described as this reviewer independently solving every logical pair.

The translation and principal-spin analytic errors are below the 1e-12 floor. Translation position error actually rises from approximately 2.77e-16 to 6.11e-16 to 1.17e-15 as the grid is refined; its acceptance correctly uses the declared floor. The motor-relaxation normalized errors are approximately 1.57554e-8, 9.59370e-10 and 5.91846e-11. Its coarse error exceeds the fine-grid tolerance, as the prospective protocol permits; the finest error and contraction gates pass. None of these facts supports an observed convergence-order claim for the coupled trajectory.

## Actual saved feedback

Literal comparison independently reproduces the checker's affected-ID lists. At the first stage, 34 drones have changed delivered rotor words and changed derivative words between the coupled and off arms. Those same 34 IDs have changed raw first-k2 state words and changed state words at the second controller update. At that update, all 64 drones have at least one changed command word. This last count includes neighborhood/controller propagation; it does not mean that every drone had a direct initial aerodynamic load change, or that every changed word has equal practical magnitude.

For a readable illustration, ID 1 is the lowest ID in the fixed first-stage affected list. This descriptive choice does not replace any gate or select a new scientific case. Its nominal rotor thrusts are approximately [0.0665534, 0.0661308, 0.0665898, 0.0661646] N; the consumed delivered thrusts are [0.0624049, 0.0620049, 0.0600336, 0.0589480] N. The exact delivered rotor words are:

```text
3faff38983596923 3fafbf1aecab0de2 3faebcb8eb06c8d9 3fae2e6fd156d8a5
```

For all 32 primary stages and all IDs, this review directly compared native delivered rotor, collective, world-force and world-moment words with their actual consumed counterparts. They match literally. Nominal motor words match state components 13–16. ID 1's first-stage vertical acceleration is approximately −0.795509 m/s² in the coupled arm versus +0.0210509 m/s² off. Its first-stage nominal motor derivatives are identical between arms, consistent with retaining the actuator state rather than overwriting it with effective thrust.

| ID 1 accepted endpoint | Position difference | Velocity difference |
| --- | ---: | ---: |
| Relative 0.0025 s | 2.54983e-6 m | 0.00203909 m/s |
| Relative 0.01 s | 4.07033e-5 m | 0.00812800 m/s |
| Relative 0.02 s | 1.62234e-4 m | 0.0161587 m/s |

The second controller's saved input is literally the accepted endpoint from step3 in each arm, and its saved times decode to relative 0.01 and original 5.01 seconds. For ID 1, the subsequent coupled-minus-off command differences are approximately [−0.000122505, −0.000194581, +0.000365911, +0.000438673] N. The receipt preserves the exact command words. Every step's accepted endpoint also matches the following step's saved base by literal association.

These saved associations, the separately checked derivative/RK recurrences, and the changed second command establish the intended feedback for this continuation. A final position difference alone would have been weaker evidence. This review performed no fresh aerodynamic computation or independent Boids/controller reconstruction.

The raw first-k2 diagnostic reports 63 of 64 norm-prerequisite failures, with maximum defect approximately 2.71652e-8 at ID 49 against the 1e-10 diagnostic threshold. It explicitly records no full preparation attempt and no admission conclusion. All primary consumed states use the prospectively selected projection. This explains why the raw-stage norm issue matters, while supplying no evidence that an unprojected stage passed or failed the complete modeled domain. The deterministic diagnostic norm is also distinct from native Math.hypot evaluation.

## Operational outcome and scope

The recorded attempt ran from 03:13:28.976166 to 03:14:14.572320 UTC, inside the new authorization window. It reports no first failure, zero execution retries, preserved sources and exit code 0 for browser, reference and checker stages. Recorded stage wall times are approximately 7.899, 30.759 and 6.695 seconds. The supervisor's pre-final-report timestamp is approximately 45.620 seconds; it excludes final report writing and process exit and is not an exact end-to-end performance measurement.

Browser output records the named Chrome 155.0.8059.80 product, confirmed owned-root exit and close with code 0 and no signal, no root error, and released guardian without a group signal. These are saved process-ownership observations, not this review's fresh process inspection or a claim about every helper. The largest local result is the 17,610,247-byte browser journal, below 32 MiB. The inspected result directory contains 52,770,463 bytes; the supervisor reports 61,558,188 bytes including its private logs/profile/scratch, below the 256 MiB cap. This review did not locate or independently remeasure the private directory from its identity hash. Recorded process-lifetime memory observations are not OS containment or aggregate browser-tree measurements.

The rational checker identifies positive and negative zero numerically when reconstructing derivative/RK arithmetic; complete equality of every computed zero sign bit is not established. Literal source/input/load/consumption associations preserve their word strings. Neighbor membership is checked under the fixed 2^-40 squared-radius boundary exclusion, and the inherited controller is bound by provenance and actual input/output consumption. There is no independent transcendental controller oracle.

The supported statement is narrow: the current strict native total-load interface was consumed correctly, within the declared audit and numerical limits, throughout this projected 64-drone continuation with inherited local control. The source state was previously exposed, so this is not held-out confirmation. The duration is 0.02 seconds and the controller updates only twice per arm.

The hypothetical directed axial-load/source-strength model still lacks measured aerodynamic validation, wake memory, a newly validated upper-drone response and a validated new reaction-yaw law. The nominal motor reaction-yaw policy remains provisional. This result supplies no continuous-time trajectory error bound, general stability or mission-safety result, robustness across seeds, real-time throughput claim, 5,000-drone coupled scaling evidence or novelty claim. Earlier 16-drone coupling already existed. The result advances the interaction/flight implementation gate in Steps 3–6; Step 7 scaling and Step 8 contribution remain open. A recorded Three.js replay can communicate these saved states but adds no speed evidence.

No disqualifying binding or completeness issue was found within this saved-evidence review. Broader claims require new prospective evidence; this pass does not expand the completed attempt's scope.
