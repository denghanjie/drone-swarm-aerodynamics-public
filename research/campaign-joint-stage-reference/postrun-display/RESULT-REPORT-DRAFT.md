# Joint-stage reference cycle: retained partial result

**Status: incomplete; numerical reference unqualified.** The closed execution window is preserved. No additional scientific calculation, comparison, integration, retry or gate evaluation was performed for this report.

## What completed

- All 10 internal implementation fixtures and 31 independent synthetic/fault fixtures passed. These are implementation checks, not physical validation.
- Both historical saved-path preflights passed: 6,401 endpoints and 100 nonterminal controller events per seed, including exact saved command hashes.
- The seed 4301 held-input compatibility run reproduced the historical terminal state/inflow hash and prescribed work counts.
- All six J1–J3 runs completed. Both prescribed joint self-consistency screens passed. Seed 840131 H4 also completed.

## Why the campaign stopped

Seed 840131 P1 reached tick 50,768, or 0.9915625 s, then stopped on the per-job cooperative wall cap. Its scheduler-recorded job time was 44.030 s, including serialization, within the 45 s hard job boundary. Its exact stopped accepted state and incomplete raw record are retained. No extension or retry was made.

Of 16 prescribed new coupled rows, 7 completed, 1 stopped and 8 were skipped. The held-physics comparison, historical bridge and cross-family approach checks were not completed. Passing the J screen therefore does not establish the required cross-checked reference.

## Retained J2–J3 maximum differences

| Seed | Position (m) | Velocity (m/s) | Primary attitude (rad) | Body rate (rad/s) |
|---|---:|---:|---:|---:|
| 840131 | 8.79913707e-11 | 2.01764251e-10 | 4.21468485e-08 | 1.735562e-09 |
| 840137 | 1.23794497e-10 | 3.71411916e-10 | 4.21468485e-08 | 3.7574459e-09 |

Values above are transcribed from the retained gate records, not recomputed. The primary attitude comparator has its known near-zero numerical floor; the retained atan2 diagnostic is separate. These tiny differences do not prove fourth-order convergence or physical truth.

## Audit and resource interpretation

The saved preflights and all visited new trajectory samples retained zero finite-jump risk flags. This is a sampled diagnostic result, not proof that every continuous path is regular. The new paths used their own genuine 100 Hz local 3D Boids controller. The frozen mean-wake and receiver model remains physically unvalidated.

The supervisor recorded 223.477 s wall and 233.82 CPU seconds; its final validity record recorded 223.486 s wall and 233.83 CPU seconds before that validity write. Neither total cap was the stopping cause. Execution validity remains false because the prescribed cycle did not complete.

The original campaign’s airflow-reference failures remain unchanged. No operational airflow cadence, safe-flight claim, mission extension, browser throughput or 5,000-drone feasibility result follows from this cycle.

## Display deliverables

- [Offline actual-record HTML](joint-stages-partial-offline.html): two historical paths plus the eight attempted new paths, with explicit partial/unqualified status.
- [Display preparation receipt](DISPLAY-PREPARATION.json): separately measured build time, source/input/output hashes and retained bytes.
- [Link and embedded-source checks](STATIC-DISPLAY-VERIFICATION.json).

The incomplete P1 display contains saved poses through 0.990 s. The frozen app visually holds that last displayed pose during later playback; the offline page states this explicitly and gives the actual 0.9915625 s stop. It does not invent extra simulated motion.

**Browser rendering has not been verified.** Headless Chromium failed to launch because the sandbox denied a socket operation, before any page loaded. The failed attempt and its timing are retained. The HTML is statically checked; it should not be described as browser-tested.

## Record caveat and sources

The frozen matrix-status output gives completed rows a generic stop-reason string even though their status is complete. This report uses each run’s complete flag and endTick alongside the matrix status. The original file is preserved; no result was rewritten.

- [Campaign and gates](../implementation/results/campaign.json)
- [Execution validity](../implementation/results/execution-validity.json)
- [Supervisor record](../implementation/results/supervisor.json)
- [P1 stopped run](../implementation/results/runs/s840131-P1.json)
- [Frozen source identity](../implementation/FREEZE.json)

Frozen source aggregate: `0475b03ad8907e6ca527233a00e8eee3d17cbbc4f70fab6bb0b48e03e62be9e1`.
Adopted plan SHA256: `b68a2a93b29e85b3784d874010c767ee7ba3eacfdcc71d4bb6b91d31606d4bba`.
