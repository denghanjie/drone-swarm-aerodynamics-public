# Static pre-freeze predictor-driver review

**Final disposition after static reread: cleared for freeze within driver/config/protocol/supervisor scope. No unresolved blocker found.** The original findings below are retained as review history; the final resolution section supersedes their initial blocking status. No experiment or model evaluation occurred during either review.

Review scope: `research/m31-predictor-stress-2026-10-15` in the M31 checkpoint worktree. This review used text reads only: no driver, model, field, receiver, poses, dynamics, refinements, or timing execution. No repository files were edited. The final six-case implementation and all-pairs analytic domain proof remain assigned to the separate design review; `cases.cjs` and `DESIGN-REVIEW.md` were not yet present when this review began.

Hashes captured at the initial review checkpoint (files were still being edited; these are provenance records, not an immutable initial snapshot):

| File | SHA-256 |
| --- | --- |
| source/experiment.cjs | 1fb7d6f276e4530d315121f65cf9489ff82c5178aa618d217e95a754e95dbc2f |
| source/run-step.py | 54acd31ee0a10ab5eda28139baf910eb8a684dbc7d39645dff270deb52c8a9f3 |
| config.json | d42c5f2b1bb89c33956e7f4fe4672eae6d0637b7b1eeb7478e6796f74b96d9cc |
| PROTOCOL.md | a070750ff5043a178f87489aa5ba04052592c398b0b7d70e9e626ff1bac5aa3e |

## Blocking findings before freeze

1. **Method order does not rotate within every case.** `source/experiment.cjs:48` chooses case `(ci+pass)%6` and method `(j+pass+ci)%5`. For a fixed case index q, `pass+ci` equals q or q+6, so the method rotation largely cancels the case rotation. Case index 5 has exactly the same method order in all six passes. Case index 0 has the same method order in all five recorded passes. This defeats the stated rotation for per-case comparisons. Use a method offset based on pass alone, or pass plus the stable case index. Five recorded passes would then put each method in every position once for each case. No count or scientific schedule changes are required.

2. **Timing failures retain stale science inputs.** `source/experiment.cjs:33` is the only assignment to `current`; the timed loop at lines 48–50 never updates it. A timing domain, receiver, field-cap, or wall-cap exception therefore saves the final fine-grid science input, not the failing timing case/method/pass/tick/state. Update stage and query context before the operation that can fail, including case, method, pass, tick, complete states, and relevant cache history. Keep context overhead inside every method's timed loop. A pose-construction failure also needs the new case/tick context assigned before calling the pose function. The checksum-specific failure already records case/method/pass and the observed/expected checksum.

3. **A raw-cap failure can consume the evidence budget.** `source/experiment.cjs:10,39,56` use the same full raw-byte cap for ordinary records and the catch-path records. The catch swallows failure-record write errors. If the next ordinary record reaches the remaining allowance, the larger failure object can also be rejected, leaving the failing input only in the `/tmp` log, which `source/run-step.py:20–23` excludes from the public payload. Reserve a bounded failure allowance inside 134,217,728 total raw bytes, and write a compact mandatory failure artifact first through the reserve. Optional partial summaries should not prevent mandatory evidence. The protocol should accurately distinguish cooperative exceptions from external hard termination: a hard kill can guarantee only already-written rows/start/supervisor evidence, unless current-query context has been durably retained beforehand.

## Clarifications to freeze prospectively

- `PROTOCOL.md:21`: Define "nontrivial" and "all relevant sampling screens" explicitly. A simple unambiguous rule is to compare all 18 case × observable refined metrics with the corresponding SI floor, require predictor ≤ hold5 + floor for each, at least one predictor < hold5 − floor across the suite, and passing relevant sampling screens for both predictor and hold5. Apply the same independent rule to RMS. If trivial metrics are to be omitted, define that criterion before exposure and ensure an all-trivial suite cannot pass a strict-improvement claim.
- `PROTOCOL.md:17`: Name the recorded observables as body-axis total rotor thrust T and body-axis roll/pitch torque. They are not world-vertical lift or world-axis moments, particularly in the receiver-roll case. `loads(s,w)` reads current nominal motor thrusts and supplied inflows; it does not apply the current attitude. Attitude affects the field's projected inflow when the field is actually refreshed. This is a clarification of the chosen model, not a request to change the experiment.
- The driver stores ingredients for suite decisions but does not yet emit suite-level comparison decisions. That is acceptable if the frozen saved-record reviewer implements the declared rule and records every contributing case/observable, both methods' sampling screens, strict-improvement witnesses, and failures. Do not infer an accuracy-qualified speed claim from timing alone.

## Checks that are sound in the reviewed source

- `cache` starts without history; tick 0 gets a real field sample. Before tick 20, predictor holds the first sample. At tick 20, the old left limit is computed before history mutation; the previous and current actual field samples then populate the two history slots. Later predictions use only those actual samples, with the ratio computed before multiplication and nonnegative clipping. No predicted value enters history.
- At every refresh, `left` uses the pre-refresh cache and the current receiver nominal motor states. Post-refresh output uses the newly sampled field. Terminal tick 4000 contributes the old left limit and the final refresh sample.
- The 10/5/2.5/5 ms periods are 40/20/10/20 fine ticks, all divisible by primary stride 2. Therefore every refresh event lies on both grids. Squared-error trapezoids start from the previous post-refresh sample and end at the current old left limit when present. No trapezoid bridges the discontinuous refresh jump. Peaks include old left limits as required.
- Target exceedances and sampling failures are recorded without aborting a scientifically valid run. Exceedance counts include sample and left-limit observations and are grid-dependent. Earlier uniform-RMS failures are explicitly retained under their original estimand.
- Instantaneous reference winds are reused only in the science `instant` variant. The timing loop supplies no reference and makes real field calls for instant. Hold5 and predict5 refresh at identical ticks and make identical field-call counts.
- Exact checksums sum `(T+roll)+pitch` sequentially at primary-grid ticks in both science and timing. No saved-data lookup is inside the timed query loop. Per-case checksum retrieval and persistence occur after the timer stops. A checksum mismatch throws before subsequent timing passes.
- Full pose creation, all-vehicle field calls when due, cache updates, prediction, receiver0 roots/wrench, query bookkeeping and checksum accumulation are inside the timer. Cache object initialization is outside the timer. The benchmark includes left-limit load evaluations on refreshes, even though only post-refresh loads enter the checksum; that overhead is consistent with the declared driver path. There are no calls to flight integration, Boids, rendering, bounds, or GPU routines.
- All vehicle/rotor instantaneous inflows are checked against the independent direct-pair oracle; receiver0 instantaneous thrust/roll/pitch are checked against the independent bisection receiver to 1e-12. This checks implementation arithmetic, not physical validity. The field's grid API computes all vehicles, whereas receiver load output is restricted to receiver0, as disclosed.

## Static count derivation

The following is loop arithmetic, not executable/model measurement.

- Science/oracle per case: 2×4001 + 101 + 201 + 401 + 201 = **8,906** calls.
- Science/oracle for six cases: **53,436** calls.
- One timing pass across all five methods for one case: 2001 + 101 + 201 + 401 + 201 = **2,905** calls.
- Six passes (one warmup, five recorded) × six cases: **104,580** timing calls.
- Total: **158,016** field calls, including **24,006** oracle calls; **0** bound calls. The 200,000 field-call cap leaves **41,984** calls unused.
- Timing files: 6 passes × 6 cases × 5 methods = **180** records, of which 150 are recorded and 30 warmup.
- Raw cap: **134,217,728 bytes = 128 MiB**, matching supervisor and config. This is the combined raw-directory cap, not a per-file cap.

## Supervisor assessment

The exclusive lock prevents simultaneous supervisor jobs in the campaign. The active ledger entry is persisted before spawn; duplicate IDs, active/review-required/terminal ledgers are rejected. The external process-group watchdog polls raw size and elapsed time, requests termination with approximately 1.1 s reserve, and escalates to kill after 1 s. The driver cooperatively checks wall and field caps on field calls. Already-written raw rows, start marker, and supervisor status survive normal child exceptions and many termination paths. Hard termination cannot guarantee a fresh application failure JSON. The once-only driver start marker prevents a second successful scientific invocation even if a distinct supervisor ID were supplied. Successful supervisor completion leaves terminal closure to the publication step, consistent with the protocol's explicit close-budget step.

Initial disposition: do not freeze the first reviewed version until the three blocking findings and two semantic clarifications are resolved. This disposition is superseded by the following final static reread.

## Final static reread and clearance

Final source/config/protocol and newly available `cases.cjs` were reread without importing or executing them. Supervisor source remains unchanged. No repository edits were made by this reviewer.

| File | SHA-256 at final review checkpoint |
| --- | --- |
| source/experiment.cjs | 4f0a235dd44dd1f542012ed5a05dfa8422164170fb7bf2627baaa94ff17ada96 |
| source/run-step.py | 54acd31ee0a10ab5eda28139baf910eb8a684dbc7d39645dff270deb52c8a9f3 |
| source/cases.cjs | f836b6469cdc7a9ab8bf0b213394707b1ff9e6c74b4fe9321569e02f406f1452 |
| config.json | d42c5f2b1bb89c33956e7f4fe4672eae6d0637b7b1eeb7478e6796f74b96d9cc |
| PROTOCOL.md | 5f548e750665debc8de714924a3a14a75f17834dfdf6f2293220e71664b63a70 |

- **Method-order finding resolved.** Method offset is now `(j+pass)%5` while cases still rotate. For each case, recorded passes 1–5 place each method in each position exactly once. Full call counts remain unchanged.
- **Timing-context finding resolved.** Both science and timing assign phase/case/tick context before pose construction; timing also retains method and pass. Complete states are attached before `advance`. For model/domain failures, the saved context now identifies the actual failing query. Prior timing/science inputs no longer masquerade as the failing query.
- **Failure-reserve finding resolved.** Ordinary records stop at `rawByteCap−failureReserveBytes`; both config and protocol set a 1,048,576-byte reserve inside 134,217,728 total bytes. `failure.json` is written first with reserve access, followed by optional partial summaries. Current-query objects and this fixed six-case summary structure are small relative to the reserve. External hard kills still guarantee only already-written raw/start/supervisor evidence; do not promise an application failure JSON after hard termination.
- **Prospective suite rule resolved and implemented.** There are exactly 18 case × observable comparisons. Each peak/RMS metric uses refined values and its declared SI floor. No-worse must hold everywhere; both methods' corresponding sampling screens must pass everywhere; at least one strict improvement beyond the floor is required separately for peak and RMS. Zero/small metrics remain included. `suiteDecision` retains all contributing comparisons, so a failure cannot be hidden in an aggregate mean.
- **Observable semantics resolved.** The protocol explicitly distinguishes body-axis total rotor thrust from world-vertical lift, and body moments from world moments. It states that the cached/predicted scalar inflow already contains the projection at its refresh pose and that no extra current-attitude projection is applied later.
- **Saved-record sufficiency improved.** Every fine row now includes independent all-vehicle winds and independent receiver0 loads, in addition to production winds, states, and treatment sample/left values. A saved-record reviewer can directly recheck oracle discrepancies without model reevaluation.
- **Window summaries match declaration.** Cold-start windows cover inclusive ticks 0–20 and 20–40. Reversal windows cover ticks 1000/2000/3000 ±40. `windowMetrics` includes sample and old-left values at boundaries, uses treatment-minus-reference signs, retains three load extrema separately, and reports inflow extrema across rotors. These summaries add no poses or refreshes.
- **Analytic cases remain deterministic inputs.** `cases.cjs` imports no model/solver and returns explicit sinusoidal/linear pose states with constant mg/4 nominal motor thrusts. Its case IDs match config. Full all-ordered-pair geometric clearance remains the separately assigned design audit's responsibility; this driver clearance does not replace that audit.

Final count remains **158,016 total field calls, including 24,006 oracle calls**, with **0 bound calls**, **180 timing records**, and **128 MiB total raw cap including the 1 MiB failure reserve**. No further blocking issue was found in the final static driver/config/protocol/supervisor review.
