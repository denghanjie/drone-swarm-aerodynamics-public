# Prospective independent saved-evidence review plan

Prepared at 03:11 UTC on 17 October 2026, before reading any result from this qualification. This reviewer authored the coupling adapter and driver draft and therefore is not independent of implementation authorship. The review is a separate saved-evidence critique, performed without invoking those implementations; the separately authored exact checker supplies the principal arithmetic cross-check. This distinction must remain explicit in the final review.

The parent has authorized one qualification attempt in a new window ending at 05:06:20 UTC. The reviewer will wait for the parent's explicit run-complete notice before reading numerical outputs. The notice may report success, failure or forced termination. Completion of source preparation is not permission to start a scientific run.

## Review boundary

The only new files this reviewer may write are in this package's `review/` directory. This plan is closed after preparation. After the run-complete notice, the reviewer may write `INDEPENDENT-REVIEW.md` and small saved-evidence extraction receipts if useful. Source, configuration, manifests, original results, browser state and Git remain untouched.

Allowed operations after the notice are read-only filesystem inspection; byte counts and SHA-256 with Python standard-library `pathlib` and `hashlib`; JSON/JSONL decoding with duplicate-key and nonfinite-value rejection; binary64 decoding with `struct`; and ordinary arithmetic on saved numbers to summarize the actual records. No candidate module, reference module, checker module or viewer code will be imported or executed. No scientific function, native call, exact-reference evaluation, syntax test, browser action or retry will be invoked. Computing a norm or a difference of two already saved vectors is descriptive extraction, not a replacement reference solve.

The review will not recreate or modify missing outputs. Missing evidence is a result limitation. If a result's declared byte hash differs from its actual bytes, its content may be described as untrusted diagnostic data but cannot support a qualification claim.

## Questions fixed before observation

1. Does one bounded attempt bind the published source, enabled authorization, runtime provenance and outputs into a consistent record, with no retry or replacement input?
2. Did the actual run produce every required primary stage and independent reference, plus the matched off arm and fixed controls, without treating refusals or unavailable witnesses as successes?
3. Do the saved records show an aerodynamic load difference that was actually consumed, an evolved state difference and a changed subsequent controller command? Is the observation attributed to the exact stage and stable drone ID, with nominal motors distinguished from effective loads?
4. Does the recorded result support the narrow implementation qualification in PROTOCOL.md? Which physical, numerical, robustness and scaling claims remain unsupported?

No additional favorable metric, state, seed or time interval will be selected to rescue a failed gate. Descriptive maxima may summarize the fixed records, but they will be labeled as such and will not replace the prospectively fixed witness or acceptance decision.

## Binding chain to inspect

First read the parent's completion notice and the final frozen PROTOCOL.md and enabled config. Record the reported source commit and execution-manifest SHA-256 without inferring them from working-tree names. Hash the actual `source-manifest.json` bytes and compare the hash supplied to the attempt. For each listed source pin, verify its exact path, size and SHA-256 using standard-library file reads. Verify that all paths remain within the repository and reject symbolic-link substitutions or duplicate manifest paths. This is a byte check; do not evaluate any pinned program.

Read `source-publication.json` and verify its declared commit, manifest path, manifest byte count and hash, verified-file count and committed/public-byte-equality flags against the source manifest and run attempt. The local review can establish that the saved receipt is internally bound; it cannot independently prove remote publication or Git history without a new remote/Git operation, which is outside this assignment. State that limitation rather than calling the saved receipt a live network verification.

Read `results/run-attempt.json`. Check the source commit and manifest identity, authorization window, one-attempt status, stage order, stage statuses, output pins, first failure, cleanup outcome, preservation flags and retry count. Check that its declared child allocations remain browser 120 seconds, reference 600 seconds, checker 180 seconds, with shared overhead/closure 60 seconds and total 960 seconds. Report recorded timing scope honestly: supervisor pre-final-report timestamps do not include the complete exited-process lifetime. Do not infer a performance result from these limits.

Read each available stage result only after hashing it against the attempt's corresponding output descriptor. For browser output, verify its journal descriptor against actual `browser-journal.jsonl` bytes; verify contiguous sequence numbers, declared record count, final newline and absence of duplicate JSON keys. For reference output, verify the descriptor journal and every referenced per-stage JSON file against actual pins. Verify that every primary input sidecar has the exact canonical UTF-8 `nativeInput` bytes, compact recursively sorted keys and no trailing newline, and that its actual pin agrees with the recorded semantic/inline hash.

Recheck the actual saved initial input against the fixed fresh-a-t5 pin: 21,955 bytes and SHA-256 `48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c`. Compare its full 64-ID/17-word object with the browser initial record and both first accepted bases. Preserve the distinction between its actual file hash and a semantic object hash.

The final review will record exact size and SHA-256 for every result or evidence file it directly cites, or a compact hash receipt covering that complete list. It will state the time of the byte verification. Hashes demonstrate identity of the inspected files, not correctness of the producer or truth of a status flag.

## Fixed counts and gate inventory

The final frozen source and science configuration are authoritative. The source draft establishes the following exact complete-run expectations:

| Evidence family | Required count | Native aerodynamic calls |
| --- | ---: | ---: |
| Coupled full-swarm stages | 32, ordered step0-k1 through step7-k4 | 32 F calls |
| Independent same-state references | 32 admitted consumed states | No producer rerun |
| Matched off full-swarm stages | 32 | 0 |
| Main accepted endpoints | 16 total, 8 per arm | 0 |
| Local controller updates | 4 total, relative 0 and 0.01 per arm | 0 |
| Main safety records | 16 if both arms complete | 0 |
| Runtime wiring groups | 12: 5 accepted, 7 rejected | 0 |
| Successful wiring derivatives | 6 single-drone records | 0 |
| Manufactured runs | 9: 3 cases × 3 timesteps | 0 |
| Manufactured steps/stages | 84 / 336 | 0 |
| Manufactured summaries | 3 | 0 |
| Raw first-k2 quaternion diagnostic | 1 | 0 |
| Saved-evidence mutation controls | 10 | 0 |
| Immutable arithmetic fixtures | 14 | 0 |
| Loader Buffer checks | 9 groups / 56 assertions | 0 |

The 32 coupled states contain 516,096 logical rotor/source pairs. Logical coverage is not identical to executed scalar suffix calls; tree certificates can cover groups, and the report must retain that distinction. Every reference uses the prospectively fixed 192-bit coefficient/source intervals, 128 root bisections, maxDrones 180 and per-stage 30,000 suffix-call cap. This review will inspect saved precision/work declarations and coverage summaries; it will not recompute the oracle.

The expected main browser journal has source and factory provenance, initial input, all fixed controls, both arms, and a final summary. With the current draft event schedule, a fully successful journal has 131 records. This total is a cross-check of the fixed event-kind counts, not an excuse to reject a prospectively documented source change before freezing. The frozen driver's actual declared schema is authoritative; any later discrepancy must be explained explicitly.

Inspect all four native load categories, including reference uncertainty: rotor/(mg/4), collective/mg, Euclidean world-force/mg and Euclidean world-arm-moment/(mgR), each at most 1e-8. Inspect the separate body-frame reference and conversion-only moment gates. Require all 32 stage results; a single refused, unresolved, missing, duplicate or extra primary record prevents the complete qualification.

For analytic controls, inspect every saved endpoint error and the independent interval decisions. The common interval is 0.01 seconds with h=0.0025, 0.00125 and 0.000625. Fine-grid tolerances are 2e-12 for position, velocity and angular velocity; 2e-10 for the quaternion chord proxy; 1e-8 for normalized motor error. The roundoff floor is 1e-12 and contraction factor one half. Errors below that floor provide no observed convergence-order evidence. Do not derive an empirical order from tiny ratios.

Inspect the fixed ten mutation outcomes individually, including unavailable-witness handling. Accepted runtime controls, expected rejected runtime controls and rejected mutated saved evidence are different families. A generic "all controls passed" flag is insufficient without the complete fixed inventory.

## Saved feedback reconstruction

Use the fixed initial coupled stage `coupled-step0-k1` and corresponding off stage, then the first accepted endpoint, the controller input at relative time 0.01 and that controller's command. Record the exact arm, step/stage and stable drone ID for every extracted item. Do not use array position as identity without checking the stored ID.

At the first stage, extract nominal motor words, delivered rotor/collective/world-force/world-moment words, consumed load words, nominal reaction-yaw word, transformed body-arm moment, total body moment and derivative words. Check literal equality of the delivered and consumed words and retain the independent checker's arithmetic verdict. Summarize the fixed witness's effective-minus-nominal load and corresponding coupled/off acceleration difference using only saved quantities. These descriptive differences do not replace an aerodynamic recomputation.

Follow the same stable ID through saved stage records and accepted endpoints. Compare coupled/off accepted state words and, descriptively, position, velocity, attitude and nominal motor differences. At the second controller update, verify its recorded input state equals the corresponding accepted endpoint from step3 and its relative/original times are 0.01/5.01. Compare its saved commands with the paired off-arm commands and identify the fixed independent feedback gate. A changed state without a changed command does not satisfy a protocol that explicitly requires both.

Do not infer causality solely from a final displacement. The case for correct feedback consists of the initial shared state, exact stage/input/load associations, saved derivative and RK chain checks, evolved controller input binding, changed command gate, and unmodified controller provenance together. There is no independently reimplemented transcendental Boids/controller oracle; describe that boundary.

The raw quaternion diagnostic will be reported only as a norm prerequisite. Its sqrt-of-rounded-squares expression is distinct from the frozen native geometry's Math.hypot expression. A pass cannot establish complete preparation/admission. The projection was fixed before observation and is not a data-selected fallback.

The checker reconstructs neighbor membership from rounded coordinate subtractions followed by an exact squared sum. Every distinct pair within the 2^-40 relative squared-radius exclusion margin fails that gate. Report any excluded boundary without adjusting the margin or rerunning. Literal input/load/consumption bindings preserve saved words; rational derivative/RK arithmetic identifies positive and negative zero numerically and does not certify every zero sign bit.

## Failure review

If the attempt fails, preserve the earliest recorded failure and locate its layer: authorization/publication/preflight; runtime or browser infrastructure; native admission/numerics; control or integration; independent reference refusal/resource limit; saved checker; persistence; or cleanup. Later errors may be consequences and must not replace the first failure.

Report actual completed counts and the first unavailable or failed record. Explain whether the failure supports a concrete implementation defect, a modeled-domain refusal, a reference limitation, a fixed-witness failure or only an operational limit. A timeout does not imply numerical inaccuracy. A preparation refusal does not imply physical impossibility. A checker failure does not justify ignoring that case or changing the acceptance denominator.

If persistence or cleanup is incomplete, distinguish saved scientific observations from operational qualification. A successful numerical file does not erase an unclosed owned process or failed source preservation. Conversely, a partial saved result may help diagnose the failure while remaining insufficient to claim success. No failed arm, stage, fixture or complete attempt will be rerun under this assignment.

## Scope of an eventual pass

Only a completely bound, complete attempt with all declared controls and checker gates passing can support the statement that the strict native total loads were correctly connected to the specified projected whole-swarm integration and inherited controller on this exposed 64-drone, 0.02-second continuation, within the declared numerical tolerances and audit scope.

It would not establish measured aerodynamic accuracy, physical validation, wake-memory effects, a validated upper-drone response, a new reaction-yaw law, general stability, mission safety, robustness across seeds, held-out confirmation, continuous-time trajectory accuracy, real-time throughput, 5,000-drone coupling, production scalability, a novel Boids algorithm or publishable novelty. The directed axial-load/source-strength model and provisional nominal reaction-yaw policy remain hypotheses. Earlier 16-drone coupling predates this qualification.

The eight-step roadmap therefore remains: this is an interaction/flight implementation gate in Steps 3–6. Coupled scaling in Step 7 and a defensible contribution in Step 8 remain open. Recorded Three.js replay is visualization of saved states; interpolation and playback slowdown supply no speed evidence.

## Final review structure

`INDEPENDENT-REVIEW.md` will lead with one of: qualification supported within scope; qualification failed at a named gate; or evidence insufficient because of a named binding/availability failure. It will then give exact source/attempt/result identities, actual counts, the first decisive failure or complete gate inventory, saved feedback observations, operational outcome, author-independence and arithmetic limitations, and claims that remain unsupported. It will distinguish direct byte/record checks performed by this reviewer from the independent checker's reported scientific verdicts.

This plan contains no result, predicted pass, observed timing or numerical extraction. Its preparation does not authorize execution and does not modify the frozen scientific task.
