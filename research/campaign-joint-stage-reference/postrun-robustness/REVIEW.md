# Independent post-run retention and cost review

## Outcome

**The reference remains unqualified.** Both recorded joint self-consistency gates passed, but the prescribed held-physics/cross-family sequence did not complete. The binding stop was the per-job cooperative wall limit in `s840131-P1`; no external kill, signal termination, domain failure or storage exhaustion is reported.

The new 16-row matrix retains seven completed rows, one failed/incomplete row and eight skipped rows. The separately prescribed historical compatibility run completed and passed its retained identity/work contract. Historical airflow failures remain historical failures.

## Verification scope and timing

`VERIFICATION-PLAN.json` was saved before this verification. The bound was 30 wall seconds. Verification inspected existing JSON, sizes, checksums, shape/count contracts, frozen identities and saved timing/cost records only. No fixture was rerun; no integration, field/controller evaluation or scientific trajectory comparison was performed. The frozen `robustness-review` directory was not edited.

The checksum/retention verification plus primary report write took **0.136207506 wall seconds and 0.133988714 CPU seconds**. These are separate verification costs, not part of the already-ended numerical benchmark. `VERIFICATION.json` and `VERIFICATION-TIMING.json` preserve the checks and timing scope.

## What was verified

- All **41 fixtures passed**: 10 implementation fixtures plus 31 independent fixtures (joint/guard 10, I/O 9, branch-boundary 6, watchdog 4, actual-runner clock 2). All five independent fixture processes exited 0 with no signal.
- Both saved-path preflights completed all 6,401 endpoints and 100 controller events.
- All **71 frozen source identities** and **25 frozen input/reviewer identities** matched. The frozen plan, adoption and storage-amendment hashes also matched.
- **52 referenced result binaries**, totaling **58,664,800 B**, matched recorded sizes and SHA256. Every available shape product matched its byte size. Signature/field streams had complete 32-byte records and no trailing bytes.
- No `.partial` files were present. This was a controlled cooperative stop rather than a mid-write interruption.
- Existing retained files totaled **118,140,355 B** at the audit's inventory snapshot, safely below the adopted 200,000,000 B cap. This snapshot precedes the audit's own primary output write and any later display/publication artifacts; those additions still count toward retention.
- The final execution-validity record explicitly says `qualifiedResultsMayBeConsidered=false`. The worker's gate successes are provisional and do not override it.

## Partial-row boundary and failure retention

P1 reached accepted tick **50,768**, or **0.9915625 s**, after **25,384 completed physics steps** and **1,624,576 completed vehicle derivative calls**. Its common-grid raw artifact has shape `[1587,16,17]`, exactly **3,453,312 B**. Common samples run from tick 0 through **50,752**, at 32-tick spacing. The exact stopped endpoint is 16 ticks later and is retained in the run/failure JSON; it was not fabricated as an extra common-grid sample.

The run retained **25,385 endpoint audit signatures**, **12,692 actual held-field refresh hashes** and all **100 nonterminal controller events**. Having 100 controller events does not make the trajectory complete: the last controller boundary at tick 50,688 precedes the stopped endpoint.

`results/failures/s840131-P1.json` preserves the exact cooperative stopping state and reason. `results/failures/campaign.json` preserves the propagated campaign failure. The separate last durable checkpoint is tick **50,688** and explicitly says `exactStoppedState=false`; it is not substituted for the later exact cooperative endpoint.

The matrix marks `s840131-P1` failed, not passed. The eight unstarted rows are `s840131-H1/H2/H3` and `s840137-H1/H2/H3/H4/P1`. A generic “Earlier fixture, preflight or gate stopped cycle” reason also appears on some completed matrix rows; the explicit status and retained run record are the authoritative facts. That generic reason is a labeling blemish, not evidence those completed rows failed.

## Cost accounting

The supervisor snapshot records **223.476584260 s wall and 233.82 CPU s**, with code 1, no signal and no watchdog kill. A later validity record, after additional final accounting/serialization, records **223.485875585 s wall and 233.83 CPU s before its own write**. The later scope is the better rounded total (about 223.5 wall/233.8 CPU seconds); neither should be described as an exact post-process-exit timestamp.

P1's job record includes serialization: **44.029648370 s wall** and **44.925806 CPU s**. Its cooperative cutoff is intentionally earlier than the hard 45-second job ceiling, allowing evidence to be written. Global wall/CPU limits were not the first binding limits. Time remaining in the global budget did not authorize ignoring the independent job ceiling or restarting the campaign.

Per-job CPU records for independent fixture subprocesses measure the parent worker around `spawnSync`, so those individual numbers are not the fixture child CPU. The supervisor's process-tree accounting is the authoritative aggregate and includes live/reaped fixture children. CPU exceeding elapsed wall is possible from process/thread activity and does not imply a second numerical scenario was run concurrently.

## Saved timing evidence and bottleneck hypotheses

Timings below are the retained instrumented wall categories, in seconds. They are not newly benchmarked results or browser throughput claims.

| Row | Loop total | Safety/diagnostics | Field | RK arithmetic | Recording/hash | Job total |
|---|---:|---:|---:|---:|---:|---:|
| Seed 840131 H4 | 23.786 | 17.773 | 2.495 | 1.814 | 0.757 | 23.806 |
| Seed 840131 P1, partial | 44.009 | 35.093 | 2.565 | 3.500 | 1.559 | 44.030 |
| Seed 840131 J3 | 39.714 | 30.067 | 4.791 | 1.369 | 3.254 | 39.753 |
| Seed 840137 J3 | 39.852 | 30.105 | 4.923 | 1.345 | 3.257 | 39.895 |

1. **The first target for cost investigation is the combined safety/diagnostic path.** It accounts for about 80% of P1 loop time and 75–76% of J3 loop time. This timer combines branch geometry, jump-risk checks and swept-contact/clearance work; the saved data do not separate their individual shares.
2. **Per-step diagnostic work, rather than increased field refresh count, is implicated by the H4/P1 contrast.** H4 has 12,800 steps and 12,800 field updates; partial P1 has 25,384 steps and 12,692 field updates. Their field times are close, while safety/diagnostics and RK time approximately double. P1 performs 24,369,600 ordered rotor/source audit-pair samples versus H4's 12,288,960.
3. **Source-backed candidates for a separate, equivalence-checked optimization study:** `branch-audit.cjs` creates pair/margin/identity objects for all ordered receiver-rotor/source samples and recomputes the same center distance inside each of four rotor iterations. `run.cjs` combines mandatory contact checks with an all-pair swept-clearance diagnostic. Reusing exact per-sample center distances, reducing allocation with indexed buffers, and separately timing these blocks are concrete hypotheses. Their actual speedup is unmeasured; they must preserve all margins, roles, source order, guards and evidence.
4. **Final artifact serialization is not the dominant saved cost.** The difference between loop total and total-before-final-record is about 19 ms for P1 and 37–42 ms for J3. The separately timed in-loop recording/hash path is larger, about 1.56 s for P1 and 3.25 s for J3, but still smaller than safety/diagnostics. Hash/state encoding changes would require a new prospective identity/encoding contract, not an in-place edit to this run.
5. **Do not infer that finishing the last fraction of P1 would establish a reference.** Eight additional rows and subsequent gates remain unrun. The global budget had only about 76.5 wall seconds remaining; extrapolating the unrun matched work would be a planning estimate, not permission to extend the budget or claim the omitted outcomes.

## Recommended disposition

Retain this campaign as a resource-limited, scientifically incomplete outcome: joint self-consistency observed on both seeds; independent held-physics and cross-family reference not established. Preserve all failures/skips and existing raw outputs. Any next cycle should first prospectively separate and optimize the mandatory diagnostic costs with frozen equivalence checks and a complete cost forecast; it must not silently omit the costly checks or continue the stopped budget. No new run or code mutation was performed in this review.
