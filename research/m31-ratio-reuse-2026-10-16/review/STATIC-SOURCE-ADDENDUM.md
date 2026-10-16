# Static source addendum: full-wrench ratio reuse

Date: 2026-10-16. Reviewer: `/root/m31_protocol_challenge`.
Repository: `repository root`.
Package: `research/m31-ratio-reuse-2026-10-16`.
Related prospective review: `PROTOCOL-CHALLENGE.md`, SHA-256 `1d2fd2b44ca120b5975eedb6149e29ef72536b882125b7a82f5c427a8b4b2461`.

## Disposition

**No blocking defect remains in the reviewed candidate/config/protocol scope after the changes described below.** The complete-path mechanics and the revised cooperative-failure counters match the written protocol. This is a source-only disposition for the exact bytes listed at the end; it is not permission to skip the independent-reviewer audit, complete dependency/reference manifest, source freeze, publication verification or single-allocation rules.

The independent reviewer source was not part of this assignment and was not present when this final scoped read began. Its implementation and complete failure-path behavior require separate review. No target imports, candidate execution, controls, scientific calculations, model evaluation, simulations or external acquisition were performed here. Node `--check`, Python AST parsing, JSON parsing, already-saved reference hashing and arithmetic bookkeeping only were used. No repository files were edited by this reviewer; only the requested /tmp review files were written.

## Findings raised and resolved before freeze

1. **Projection failures were counted as entered coupled/cached evaluations.** Initially, every rejected-stage callback increased both stage and evaluator counters, including rejection by quaternion projection before either evaluator was called. `adapter.cjs:28` now initializes `evaluationAttempted=false` and sets it only after successful projection, immediately before evaluator entry. `experiment.cjs:32` always counts an attempted stage but counts its evaluator only when that marker is true. A final weighted-state projection failure adds no fifth stage/evaluator. This resolves the observed overcount.

2. **Cooperative global exceptions skipped the final counter snapshot.** Initially, wall/RSS/storage exceptions rethrew before assigning `rec.counts`, `final` and `end`, leaving the interruption record's counters empty. `experiment.cjs:40-42` now assigns them in `finally`. A guard failure before a step counts no attempted stage; an entered full/cached evaluation that throws still counts as an attempt. Counts are attempts, not successful builds or completed root solves. This resolves the observed loss on cooperative exceptions.

3. **Compact retention could lose the preceding cache after a rejected refresh.** Initially, only the last event was retained. A full-solve rejection leaves that event's new `cache` null, with only the old cache index. The compact fallback now retains the last two events (`experiment.cjs:64`), preserving the preceding cache roots together with the failed refresh record. Normal full records retain all earlier events. This resolves the identified compact-retention gap.

4. **Nonfinite cache times/index and nominal-total guard gaps.** The updated cached evaluator explicitly requires a nonnegative integer cache index, finite cache and evaluation times, an array with the expected rotor rows, and finite current nominal rotor sums. Individual nominal values remain finite and positive. This prevents NaN time from bypassing both age comparisons and avoids relying on a downstream derivative failure to identify an overflowing nominal total. Three rejection cases were added to the prospective controls for evaluation time, cache time and index. Those controls were read but not executed.

5. **Approximation gate scope differed from the earlier recommendation.** The code requires all three matched-timestep comparisons and all three event-error sets to pass. The protocol now explicitly adopts that stricter choice. This is consistent, prospectively fixed and acceptable; it is not represented as the original finest-grid-only recommendation.

6. **Hard-kill prefix preservation was overstated by implication.** The protocol now explicitly says external SIGKILL cannot execute candidate finally and only already-written path files, logs and the supervisor record are guaranteed. Loss of the in-memory active prefix is a disclosed limitation. No continuous-prefix preservation is claimed for that case. This is a declared evidence limitation, not a solved durability mechanism.

## Mechanics verified by source inspection

`makeCache` copies the solver-returned `witness.rotors[i][r].x` directly and freezes the outer cache, root matrix and each root row. It performs no T/f0 recovery. The cached evaluator multiplies each stage's current nominal motor state by the saved root, calls the inherited force/moment assembly with the current state, and adds that correction to the unchanged nominal derivative. Nominal yaw, body-rate gyroscopic dynamics, motor lag and quaternion derivative remain in `F.derivative`. The normalization length is `Math.SQRT2 * F.P.a` with inherited `F.P.a = 0.028`, which is the rotor-corner lever arm intended by mgR.

The same cache object is passed through all four RK stages. A k4 at a 10 ms boundary therefore uses the old cache; refresh is outside `A.step`, after weighted-state projection and accepted-step safety. The subsequent k1 uses the new cache. The integer step divisors are 2, 4 and 8 steps per refresh for the three frozen h values. Rounded event timestamps only identify accepted boundaries; they do not choose stage caches.

At t=0, commands exist before refresh, LEFT is absent, the full solve creates the first cache and RIGHT supplies the sample. The inherited t=0 controller update still occurs before propagation. At each positive event, LEFT, the full instantaneous solve and RIGHT use the same accepted states and incoming held commands. Positive 100 ms samples use LEFT and do not call another full evaluator. The next loop updates the controller. The terminal event is retained and counted but never propagated. `sampleSide` and `eventIndex` are saved explicitly.

Ordinary cached evaluations contain null geometry/admission/order/residual fields and `evaluation: "cached-ratio"`. No old residual is passed off as current, and the source performs no hidden full geometry evaluation inside `cached`. Tilt is a cheap diagnostic; the updated protocol correctly introduces no 45-degree admission guard. Current-event full solves retain inherited admission, descending-order and residual checks. These source facts do not certify coupled-domain validity between sampled geometry checks.

## Allocation and gates verified

The candidate runs the three full paths first. It verifies complete-path status, exact saved-field equality against three pinned prior full records, and inherited five-metric refinement before entering the reuse branch. The exact reference comparisons include t, states, commands, forces, modeled/applied corrections, derivatives, geometry witness and group summary; timing and newly added metadata are excluded. The three reference files' actual byte lengths and SHA-256 hashes match config during this static review.

The reuse branch runs all three preallocated grids. An approximation miss is computed after those paths and does not shorten the allocation. A model/contact failure saves its record and permits the fixed following paths; global resource failure exits. There is no adaptive cadence, alternative seed, predictor, extra grid, retry or model fallback in the candidate.

`allocationPass` requires full qualification, all path completions, both arms' refinement and post-refresh construction agreement. `approximationPass` additionally requires every matched-grid trajectory gate and every pre-refresh event gate. These are distinct as required. The inherited refinement rule retains the 1%-of-tolerance floor exemption; it remains an observed sampled comparison, not a rigorous bound. Wrench errors compare LEFT and fresh on the reuse arm's own accepted state. The force/moment thresholds use mg and mgR; full three-component torque norm equals the intended roll/pitch norm because the inherited correction's z component is exactly zero.

The source retains event maxima but does not store their argmax or raw-unit maxima in its analysis summary. All arrays needed to derive them are present in the events. This is a nonblocking reporting follow-up for the independent reviewer/result analysis; the protocol currently promises maxima, not an argmax table. No extra solve is required to report them.

## Call-count audit

All complete-path counts follow directly from the static schedule:

| h (s) | Steps | Stage evaluations | Full-arm joint attempts | Reuse joint attempts | Reuse cached applications |
|---|---:|---:|---:|---:|---:|
| 0.005 | 400 | 1,600 | 1,621 | 201 | 2,001 |
| 0.0025 | 800 | 3,200 | 3,221 | 201 | 3,601 |
| 0.00125 | 1,600 | 6,400 | 6,421 | 201 | 6,801 |
| Total/arm | 2,800 | 11,200 | 11,263 | 603 | 12,403 |

Thus six complete paths have 22,400 stage attempts and **11,866 candidate joint-query attempts**. Reuse cached applications equal 11,200 stage evaluations + 600 positive LEFT evaluations + 603 RIGHT evaluations. There are 603 refresh events: 600 propagation refreshes including the three initial events, plus three terminal audits. Each arm has 63 legacy samples, with reuse samples being aliases/reconstructions of existing event data. The first/last step capture rule gives 12 full step witnesses and 48 captured global stages.

Eight cached evaluator calls are separately allocated to synthetic controls: one identity call, two current-nominal scaling calls, two out-of-age rejection attempts and three nonfinite-cache metadata rejection attempts. The inherited controls perform analytic correction/angle checks and do not call the coupled solver. These are outside the 12,403 path cached-application count. No control was run in this review.

Failure branches are consistent with attempt semantics: refresh counts increment when the event starts; LEFT counts immediately before entering its cached evaluator; a full attempt increments only after LEFT succeeds, except at initialization where LEFT is absent; RIGHT counts only after cache creation; stage attempts with failed projection do not increment evaluator counts. Sample attempts increment before the full-arm endpoint evaluator or reuse alias. Cooperative failure snapshots preserve actual counters. A hard external kill cannot furnish an exact unsaved active-prefix count, as now disclosed.

## Resource wrapper and evidence limitations

The fixed wrapper checks exact local/committed manifest bytes and current HEAD before consuming an exclusive invocation lock. Its candidate/reviewer time limits, RSS limit and 96 MiB aggregate cap match config/protocol. It samples the direct child, checks logging and aggregate artifacts during execution, rechecks after child exit and includes its own record size in the final aggregate determination. Candidate output uses an 88 MiB normal allowance with 8 MiB reserved for emergency writing. These are limits, not an assurance that every active full record fits the reserve; compact fallback remains explicitly labeled.

The source-only 96 MiB budget is plausible for the chosen shared-state event structure but is not a measured new serialized size or RSS guarantee. Arrays inside LEFT/instantaneous/RIGHT intentionally duplicate load/wrench/derivative data; geometry appears only on instantaneous evaluation. No benchmarking or speedup inference is available from this single instrumented campaign. The protocol preserves the known 5,000-drone timing limitation and provisional physics scope.

## Static validation and remaining pre-execution obligations

Parser-only checks passed on the final listed adapter, controls and experiment CJS files using the bundled Node binary with NODE_OPTIONS removed. Python AST parsing passed for `source/run.py`; JSON parsing passed for config. No module was imported by these checks. The prospective README, protocol, claim/literature ledger, reproduction and restart notes are consistent on six paths, one candidate/reviewer invocation, strict pre-freeze restrictions, prior allocations remaining closed, and no automatic expansion.

Remaining obligations are outside this scoped disposition: complete and statically audit the saved-only reviewer; pin every executable dependency/reference and the final documents; privacy-check and publish source; verify exact remote bytes before any target imports or execution; and keep HEAD fixed for the two consumed invocations. A final manifest differing from the hashes below needs an appropriate delta review. This addendum does not claim observed numerical success, post-freeze integrity or independent reviewer success.

## Exact reviewed bytes

| File, relative to package | Bytes | SHA-256 |
|---|---:|---|
| source/adapter.cjs | 4389 | c6759b7ccc90e0adbc4feb8eb552d1959a988ca33e54ff158d42373be8ecd74e |
| source/controls.cjs | 2193 | 3ad26698c7c7603a77f3545c80cbf1aa19ea42582e889a94bf19f2112230b846 |
| source/experiment.cjs | 11963 | d9142dd2bdfd0bfdd1e00da7b12719422e43ad14719ef0b86c457482a8b0ebb6 |
| source/run.py | 6671 | 0aa7f4f158c6b784ed62d43c4cfa55d02301b760411674f82de4a6ac4e8ae04b |
| config.json | 2086 | 965d3c4d6bafa641e571805b9f46992fb4f88a3dbd8f7c14a369d4b4d3d1e2fc |
| PROTOCOL.md | 12436 | 0322e5f156a7d369fe0d0bc71aaf8d730a5d00e198c11e2a71055158f8d7d8f4 |
| README.md | 1006 | d1315620c4794ca02b89c86ab94c2e0c6a06ed66c1a2defc5790a269e2f413ec |
| CLAIM-LITERATURE-LEDGER.md | 2211 | d1f65f8ff99386446ddaba908b3414d7dd432a749a7e243b25de10deccbce1ce |
| REPRODUCE.md | 1533 | e6940d498bcf27b4a90a53721ddad9c31e5bb48b4c05a9c9e4b9f97c843a5b2b |
| SOURCE-RESTART.md | 1056 | 0c82ac0365fe0784ae15bdda67f3db01ef04f59f02522ee4230a5504b082b347 |
| bibliography.bib | 1010 | df635286fe0e049edb8ba02740bd47fb3e0ac6766d1b97f9a291b165ea5bd0f3 |
