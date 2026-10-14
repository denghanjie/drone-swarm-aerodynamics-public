# Independent findings: exact-equation airflow efficiency

Editorial correction (2026-10-13): the independent previous-zero pass count is 3/12. See [the correction record](../CORRECTIONS.md); numerical records and simulation code are unchanged.

## Conclusion

The refreshed implementation passed the independent finite-support software-model checks. Its field evaluator is substantially faster than the historical allocation-heavy implementation on the tested workloads. Its additional improvement over the previous optimized zero-budget control is smaller and workload-sensitive. The independent whole-pipeline comparison did not meet the preregistered 10% savings gate. No N=500 extension, flight-feasibility or hardware-generalized speed claim follows.

## Correctness and API scope

- Candidate SHA256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`.
- 85 fixtures across historical, previous-zero, lean, support and reuse implementations passed. All 78 model-domain-valid fixtures were bitwise equal across all methods and the independent all-pairs oracle. The other seven retained matching near-wake or tilt failures. Sources were unchanged during the run.
- 45 permutation/translation/global-yaw checks passed. Largest inflow discrepancy was 9.77e-15 m/s, force-vector discrepancy 1.68e-16 N and roll/pitch moment-vector discrepancy 3.65e-18 N m, below frozen limits.
- 33 reusable-workspace/ownership checks passed, including changing N through 200, in-place geometry mutation, invalid-call recovery, separate evaluators, caller output mutation and old-result immutability. Four-rotor output shape, finite nonnegative values and positive-field preservation were checked.
- 39 explicit new-API rejection assertions passed. Empty input, malformed state, invalid options and out-of-range numerical coordinates are distinct from physical-model domain checks. Fields intentionally do not consume nominal thrust; receiver loads reject invalid nominal thrust separately.
- The original zero-support candidate had an independently identified large-coordinate false cull, retained in the separate physics review. A2 bounds coordinates to ±1e6 m and inflates the conservative envelope for coordinate roundoff. The refreshed suite covers the exact limits, one ULP outside, ±999999 translations, near-unit quaternion tolerances and the saved enormous-translation regression. Legacy/previous-zero huge-coordinate grid timeouts remain documented API differences.

Initial independent-suite results were retained before those explicit regressions were added. Their raw hash shows A2 was already present; the append-only correction distinguishes this suite version from the original failed candidate version.

## Independent performance

Frozen choice: lean. Fresh seeds 628791/628792, N=100/200, sparse/dense/tilted prescribed-state fixtures; nine seeded balanced paired repetitions per case. These prescribed states are not flock trajectories. Each field call validates inputs, prepares geometry, searches the original grid and returns owned four-rotor outputs. The independent harness includes the same checksum reduction in each measured call. The primary harness retains outputs and verifies SHA checksums after timing; do not pool their numbers.

All twelve nonzero field cases passed the ≥10%/paired-bootstrap gate versus legacy, with median paired ratios 0.498–0.708 (about 29–50% lower field time). Versus previous-zero, the ratios were 0.856–0.965; only three of twelve cases individually met both screen conditions (median ratio at most 0.9 and paired-bootstrap 95% upper ratio below 1), and no family/count did so in both fresh seeds. Four cases met the median-only threshold; the 628791/N=100/tilted case failed the upper-bound condition (1.0105362). That last observation is an additional robustness description, not a redefinition of the original gate. Several intervals overlap 1.0. The prior optimized control therefore remains the appropriate comparison for any incremental optimization claim.

| Seed | N | Family | Field ratio vs legacy | Field ratio vs previous-zero | Previous-zero field gate | Combined ratio vs previous-zero |
|---:|---:|---|---:|---:|---|---:|
| 628791 | 1 | zero | 0.674 | 0.705 | pass | 0.941 |
| 628791 | 100 | dense | 0.541 | 0.903 | fail | 0.936 |
| 628791 | 100 | sparse | 0.651 | 0.881 | pass | 0.917 |
| 628791 | 100 | tilted | 0.580 | 0.872 | fail | 0.953 |
| 628791 | 100 | zero | 0.833 | 0.818 | pass | 0.855 |
| 628791 | 200 | dense | 0.500 | 0.965 | fail | 0.941 |
| 628791 | 200 | sparse | 0.708 | 0.903 | fail | 0.870 |
| 628791 | 200 | tilted | 0.613 | 0.888 | pass | 0.941 |
| 628792 | 100 | dense | 0.567 | 0.914 | fail | 0.927 |
| 628792 | 100 | sparse | 0.611 | 0.909 | fail | 0.933 |
| 628792 | 100 | tilted | 0.545 | 0.856 | pass | 0.948 |
| 628792 | 200 | dense | 0.498 | 0.950 | fail | 0.940 |
| 628792 | 200 | sparse | 0.656 | 0.934 | fail | 0.906 |
| 628792 | 200 | tilted | 0.635 | 0.919 | fail | 0.970 |

The isolated control's field batches are sub-millisecond; its formal previous-zero pass is not a useful speed claim and lies outside the N≥100 gate. The N=100 zero-field case measures overhead without wake contributions. Zero/isolated controls and dense unfavorable results remain in the raw data. Process RSS/heap/external/load/CPU observations were retained in original records and withheld from the public copies. They do not establish allocation rate or a stable memory advantage.

Field+receiver gains over previous-zero are also modest: only one of twelve nonzero cases met the 10% combined-scope gate. All twelve combined cases comfortably beat legacy. Neither scope includes the controller, rigid-body integration, contact checks, recording, rendering or a flight mission.

## Genuine whole-pipeline crosscheck

Seed 628791, N=16, one simulated second, physics 2.5 ms, controller 10 ms and airflow 10 ms; unchanged local 3D Boids, receiver response, RK4 and safety checks; recording disabled. All warmups and 27 measured runs completed 400 steps and 100 field updates, with deterministic final states. Nine paired repeats gave:

- Lean/legacy median paired total-time ratio 0.917; 95% paired bootstrap interval [0.885,0.967].
- Lean/previous-zero ratio 0.960; interval [0.936,1.018].

Neither independent result meets the ≥10% whole-pipeline gate. The second interval includes no improvement. The separate primary run used seed 4301 and seven paired repetitions: ratio 0.847 [0.797, 0.918] versus legacy and 0.911 [0.901, 0.960] versus previous-zero. Its legacy comparison passes its measured-case gate; its previous-zero comparison does not. Independent recalculation confirms those statistics, and all 21 primary members completed identical work with matching final-full-state/held-field hashes. The independent harness checked deterministic final full states but did not store a terminal held-field hash. Different seeds, runner instrumentation and pairing are kept separate. These small numerical workloads do not support a stable ≥10% whole-pipeline claim across runs, or whole-flight extrapolation.

## Primary timing arithmetic and resources

An independent implementation recomputed all 30 primary timing files' medians, 5,000-draw paired bootstrap endpoints, pass/fail flags and per-call durations. All matched. Repetition counts, method coverage, deterministic complete-output checksums, saved fixture hashes and source/input guards also passed. Primary-case results remain separately reported; the fresh independent workload and instrumentation explain why replication need not reproduce identical speed ratios.

The 15-job independent batch completed in 24.71 seconds of wall time, with no source/checksum/completion failure. Each job was capped at 60 seconds; no concurrent heavy work was allowed. No paid compute or N>200 numerical benchmark was used.

## Replay and remaining limitations

All 14 saved Boids records passed numeric-record review. Eight legacy/previous-zero/lean matched pairs have identical saved poses, rotor fields, initial/final full states and stored rolling hashes. The rolling hashes were compared rather than reconstructed from unretained intermediate states. An independent recomputation from 520 saved poses whose field timestamp was fresh checked 82,240 individual rotor inflows against legacy, with exactly zero difference. Final held fields were correctly excluded from fresh-field recomputation.

The first standalone failed static parsing because a packer globally replaced a placeholder inside serialized vendored JavaScript. That failure is retained. After the packer fix, all embedded source modules, 14 Boids records, record shapes and endpoints matched, but provenance had been updated after embedding. That stale-provenance failure is also retained. The final integrated standalone passed identity verification at SHA256 `0b7ec7e511da1aa31a49d56f66486d32686dd1720aaff2078319901dcf47ff50` (6,693,831 bytes). All 17 embedded JSON records, four source modules and four text artifacts matched the integrated files. Four bundled modules plus the inline loader passed JavaScript syntax checks, and all eight document/download links had bundled targets. The two pre-delivery packaging failures remain separately preserved.

No rendered/interaction QA has passed. One recorded browser attempt failed at a Chromium socket permission check; the error and absence of a screenshot are saved. This independent evaluation did not retry browser launch or change security settings. Static checks do not establish appearance, WebGL execution, interaction behavior or download usability.

The source model remains an unvalidated fixed-hover, finite-support mean-wake and receiver-response approximation. Exact implementation equivalence does not repair source calibration, missing physics, cutoff assumptions, earlier cadence/convergence limitations, or mission completion. The viewer replays actual saved states and does not benchmark simulation throughput.
