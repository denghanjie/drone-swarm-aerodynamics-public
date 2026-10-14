# Independent post-run physics and numerical interpretation

Status: **Joint-stage self-consistency observed on both diagnostic windows; full numerical reference not established.** The cycle terminated at its prescribed cooperative per-job limit. This review only inspected existing saved JSON records and source bytes. It did not integrate, rerun fixtures, decode/recompare trajectory arrays, evaluate new geometry, or modify any frozen source, input, or review directory.

## What the retained records establish

The six J trajectories completed their prescribed one-second windows. Both per-seed J refinement gates are recorded as passed, over 1,601 common endpoints and all 16 drones. The only other completed prescribed new row is H4 for seed 840131. P1 for that seed stopped before final T, so its independent held-physics comparison was never evaluated. Eight prescribed rows remain skipped. The historical seed-4301 compatibility run is separate from these eight attempted new rows.

The positive result is a stage-consistent candidate which is numerically self-consistent under the prescribed screens. It is not an accepted reference, a demonstrated zero-hold limit, a truth-error bound, or physical validation. The execution-validity record correctly rejects campaign qualification.

Sources: `implementation/results/campaign.json` → `gates`, `comparisons`, `runIds`; `implementation/results/matrix-status.json`; `implementation/results/execution-validity.json`.

## Joint comparison results, copied from saved gates

| Seed | J2–J3 position, m | Velocity, m/s | Primary attitude, rad | Body rate, rad/s |
|---|---:|---:|---:|---:|
| 840131 | 8.799137067744731e-11 | 2.0176425055042244e-10 | 4.2146848510894035e-8 | 1.7355620045940678e-9 |
| 840137 | 1.2379449674492317e-10 | 3.7141191570972284e-10 | 4.2146848510894035e-8 | 3.7574459035789136e-9 |

The saved absolute caps are 1e-4 m, 1e-4 m/s, 1e-4 rad, and 1e-3 rad/s. More importantly, **every fine difference is below its prescribed comparison floor**: 1e-8 m, 1e-8 m/s, 1e-7 rad, and 1e-7 rad/s. Thus all reduction tests pass at the screen's resolution; they do not provide a resolved measurement of numerical order. The primary attitude result is identical at both refinement differences, as expected when its normalized-dot/acos near-zero limitation dominates. Saved secondary atan2 fine differences are 1.2826950986369821e-10 rad and 2.4879856498981526e-10 rad. These are supplementary diagnostics, not replacements for the frozen primary metric.

The saved J1–J2/J2–J3 controller comparisons each cover 100 events and report no differences in the recorded controller branch signature. Fine maximum actual motor-command differences are 5.925607227119656e-12 N (840131) and 4.1678299700365073e-11 N (840137). This is useful evidence that these J refinements did not diverge in the instrumented controller decisions. It does not certify every internal controller predicate or prove physical feedback robustness.

Sources: `campaign.json` → `gates[0..1].rows`, `.fine.maximum`, `.coarse.maximum`; `controllerComparisons`. These values are copied from existing comparisons, not independently recomputed here.

## Branch and domain evidence

Both saved-path preflights visited all 6,401 endpoints and checked all 100 nonterminal controller events. Their recorded status is passed, which includes exact reproduction of the historical command hashes on the identical saved states. This is distinct from demanding identical commands across independently evolved trajectories.

Every saved audit for preflight, compatibility, completed J/H4 rows, and the observed P1 prefix has an empty `risks` list. No source/receiver tilt, near-wake, nonfinite-state, or contact-domain stop is recorded. Coverage in the six completed J rows is 8,001 / 16,001 / 32,001 observations per seed, with 1,600 / 3,200 / 6,400 full-trial and endpoint range tests. H4 has 12,801 endpoint observations and 12,800 range tests. P1 has 25,385 observations and 25,384 range tests before stopping. Production refresh aliases are separately counted.

This does **not** mean no branch changed. The saved records contain downstream-zero, lower-far-field, near-radius, radial-fade, and radial-cutoff signature changes. For example, seed-840131 J3 has 296 sampled category comparisons with a lower-far-field sign change; seed-840137 J3 has 151. These are geometric sign changes, potentially including inactive pairs and repeated endpoint/trial comparisons, not counts of physical jump events. The valid-annulus range criterion did not flag a possible finite field jump. A farStart sign change alone is insufficient to assert such a jump.

J2 and J3 half-stage samples remain trial states, including multiple states at the same nominal time. Neither their ordering nor the absence of a flag proves continuous-path regularity. H/P audits cover accepted endpoints and production-refresh aliases, not every hidden held-integrator stage. Close signed radial or downstream margins are not by themselves near-wake violations: the other guard predicates and pair eligibility must also hold. This review did not evaluate new geometry to turn separate extrema into an unsupported combined crossing claim.

The saved J3 quaternion raw-stage norm defects peak at 9.396387246063398e-8 and 9.736697825779572e-8; endpoint projection sizes peak at 4.983580072506977e-16 and 4.972850431340754e-16. These are diagnostics of the chosen extension/projection, not state-error estimates. Stored positive tilt margins are in cosine space; they must not be described as angular margins without an explicit conversion.

Sources: `results/audit/*.json` → `samples`, `stepRiskChecks`, `endpointRiskChecks`, `fullTrialRiskChecks`, `risks`, `brackets`, `extrema`; `results/preflight/*.json`; `results/runs/*-J3.json` → `metrics`.

## Exact meaning of the P1 stop

- Failed row: `s840131-P1`, held inflow 0.078125 ms, physics step 0.0390625 ms.
- Recorded cause: `Per-job cooperative wall cap`.
- Exact retained accepted endpoint: tick 50,768, time 0.9915625 s. The cooperative budget check stopped before the next step/refresh.
- Last held-field refresh: tick 50,764. The next due refresh at the stopped endpoint did not occur.
- Last durable checkpoint: tick 50,688 (0.99 s), explicitly labeled non-exact as an interruption checkpoint. It is superseded for this stop by the separate exact failure record.
- Common-state artifact: shape `[1587,16,17]`, covering the common grid through tick 50,752 (0.99125 s). The exact stopped endpoint is between common records and is retained in the failure/run JSON, not fabricated as an extra common-grid sample.
- All 100 controller events were reached, including the final scheduled event at tick 50,688. That does not make the trajectory complete at T=1 s.

This is a resource obstruction, not a detected physical instability, model-domain violation, hidden H-stage exception, or failed H4–P1 accuracy gate. It is also not a process kill. The source's cooperative guard leaves approximately one second for retention before the hard 45-second job deadline; the saved authoritative P1 job time is 44.02964837 s. Its exact stopped state is available because the stop happened between accepted steps. The prospective hidden-held-stage evidence limitation was not exercised.

Do not qualify a one-second physics gate by dropping the missing end of P1, comparing only the common prefix, treating 100 controller events as completion, or resuming the old budget. Such a different-window comparison would be a new scientific analysis and was not performed here.

Sources: `results/failures/s840131-P1.json`; `results/runs/s840131-P1.json`; `results/raw/s840131-P1.common.f64.json`; `results/last-checkpoint.json`; `campaign.json` → `jobs`.

## Actual cost and the useful next test

The supervisor records 223.47658426 s wall time and 233.82 CPU s, no terminating signal, no watchdog kill, and 118,104,714 retained bytes at its snapshot. The later validity-write receipt records 223.485875585 s and 233.83 CPU s. These are different observation points, not conflicting estimates. Both are below the adopted 300 s / 300 CPU s / 200 MB totals. The per-job cooperative stop is the binding limit actually encountered.

Selected saved timings:

| Work | Whole job including serialization, s | Safety/diagnostics bucket, s | Field, s | RK arithmetic, s |
|---|---:|---:|---:|---:|
| J3, seed 840131 | 39.753134901 | 30.067203445 | 4.791277965 | 1.369018488 |
| J3, seed 840137 | 39.895442270 | 30.105247716 | 4.922537076 | 1.344982403 |
| H4, seed 840131 | 23.806128743 | 17.772861825 | 2.495034393 | 1.813932434 |
| P1, seed 840131, incomplete prefix | 44.029648370 | 35.093140530 | 2.564962824 | 3.499567078 |

The grouped safety/diagnostics work dominates these instrumented runs. This bucket includes both geometric/branch auditing and production safety checks; the saved timing alone does not locate a particular allocation or function as the bottleneck. These are one-off instrumented CPU costs with different completed work, not a speedup benchmark, accuracy-cost frontier, or browser prediction. P1 must remain labeled partial.

**Recommended next test:** prospectively design a diagnostic-equivalence and cost test using retained states and synthetic fixtures before another coupled window. Investigate the dominant safety/diagnostics bucket and reduce allocation/hash/geometry overhead while preserving every required sample, pair, exact predicate, risk flag, first/worst selection, failure record, and unchanged production stop ordering. Compare the optimized diagnostic outputs against the existing frozen definitions with deterministic ties and encoding retained. Do not accelerate by dropping audits, weakening guards, changing the field, smoothing the finite jump, reducing coverage, or retuning caps after seeing an outcome.

If that test succeeds, a separately bounded and newly frozen completion study should prioritize the missing full-T held-physics evidence: rerun the incomplete P1 from its original initial state, complete H4/P1 for seed 840137, then reach the held-refinement, historical bridge, and cross-family gates. The already completed J evidence can be retained under explicit identity checks; another finer J level is not motivated by the present floor-limited differences. The old failed window and exact stop must remain permanent records. Any reuse, changed harness, budget, or execution schedule must be declared prospectively, not treated as continuation under a reset budget. This paragraph is a recommendation only; no new test or run was launched.

Sources: `results/supervisor.json`; `results/execution-validity.json`; `campaign.json` → `jobs`; per-run `timing` scopes.

## What remains scientifically unresolved

1. H4–P1 integration contamination at the finest hold, for both complete windows.
2. H1's bridge to the retained 0.625 ms held-field driver under the prescribed caps.
3. Whether all three hold halvings approach J3 monotonically enough under the prospective 0.7 screen.
4. Whether H4–J3 satisfies all four original absolute caps on both seeds.
5. Whether a subsequent fully valid supervised completion supports the strictly bounded numerical-reference label.

No saved cross-family comparison exists in this window, so the new result cannot yet attribute the old discrepancy to hold error. It also cannot repair or replace the historical failures in velocity, attitude, and body-rate caps. Passing source compatibility and J screens is useful progress, but hypotheses involving held-input approach remain untested here.

The physical-model limits are unchanged: mean hover/near-hover wake scaling, fixed source hover amplitude, frozen receiver-thrust inversion and nominal yaw restoration, finite support, multiwake superposition, 20-degree domain, and a synthetic one-second local-Boids workload. Neither the scalar margins nor the absence of contact stops establishes real-world safe flight. There is no new measured-flight, novelty, full-mission, 5,000-drone, GPU, or browser feasibility result.

## Integrity and review scope

The 71 files listed in the saved source freeze were rehashed as bytes and all matched. The active plan hash still equals `b68a2a93b29e85b3784d874010c767ee7ba3eacfdcc71d4bb6b91d31606d4bba`; the saved source aggregate is `0475b03ad8907e6ca527233a00e8eee3d17cbbc4f70fab6bb0b48e03e62be9e1`. Fixture result records show all built-in and independent fixture groups passed, and seed-4301 compatibility reproduced its original terminal-state/held-wind hash and work counts. These are inspected saved outcomes, not reruns by this reviewer.

The supervisor's `matrix-status.json` uses a generic reason string even on completed rows and skipped rows; status fields and the specific P1 failure record should govern interpretation. No fixture or numerical gate is recorded as failed. `execution-validity.json` is correctly false because the campaign stopped. No record was edited to improve that status.

The accompanying `EVIDENCE.json` copies selected saved facts and records source paths/digests. Full trace/array numerical values were not newly analyzed. Primary-source methodological limits remain as documented in the pre-run independent review and bibliography; no new literature claim was needed for this result interpretation.
