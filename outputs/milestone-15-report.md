# Checkpoint 15 — diagnosing time-step sensitivity

This checkpoint is development work on the known difficult seed 801, not new validation. It tests the same tight course at physics steps 0.005 and 0.0025 s for five controller variants. All variants retain full rigid-body integration and contact checks. The purpose is to isolate which controller components amplify small numerical differences.

## Results

| Variant | Coarse/fine completions | Coarse/fine stop | Terminal difference | First sampled difference >1 cm |
|---|---:|---|---:|---:|
| joint | 31/31 | none/none | 2.489260573 m | 32.9 s |
| filter-only | 24/24 | none/none | 5.956055425 m | 35.1 s |
| steering-only | 49/49 | none/none | 0.000003727 m | not reached |
| retention | 17/16 | none/none | 10.772838791 m | 22.3 s |
| continuous | 23/23 | none/none | 7.083515921 m | 32.6 s |

`joint` is the preserved milestone-14 candidate. `filter-only` smooths constraint activation while retaining the old steering. `steering-only` smooths social-neighbor weights and map-guidance transitions, retaining the original joint filter. `continuous` combines both changes. `retention` adds local leading-drone slowdown and stronger cohesion to the combined variant.

## Interpretation

On this trajectory, smoothing steering alone dramatically improves numerical agreement and increases passage from 31 to 49. Smoothing the clearance filter does not help; both the filter-only and combined variants have large discrepancies. Therefore, smoothing everything is not an evidence-based fix. This is a component intervention on one development case, not proof of a single universal cause or of stability.

The threshold probes perturb position by only 0.2 micrometres across specific boundaries. The original joint controller has command jumps as large as about 1.36 m/s in these synthetic probes. The probes identify discontinuities, but do not by themselves prove that a particular switch causes the whole trajectory to diverge. The time-resolved differences and component tests provide complementary evidence.

The development retention variant also has a discovered neighbor-boundary discontinuity: its slowdown normalizes by a vanishing neighbor weight. That variant is rejected and preserved. Checkpoint 16 corrects the normalization and compares it using the original filter.

## Trace

- [3D coarse/fine replay](milestone-15-diagnosis.html)
- [Protocol](milestone-15-protocol.json), [all metrics and states](milestone-15-study.json), [time-resolved differences](milestone-15-differences.json), [threshold probes](milestone-15-switch-probes.json)
- [Simulator](milestone-15-source/sim.cjs), [continuous components](milestone-15-source/continuous.cjs)

No physical validation, airflow calculation, safety guarantee or final scientific novelty result is claimed.
