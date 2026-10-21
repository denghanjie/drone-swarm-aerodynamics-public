# Does the unchanged correction transfer to another arrangement?

21 October 2026. Computational-only milestone; overall research remains unfinished.

**2 of the two prescribed vertical-memory paths reached five seconds.** Both use the same exposed 64-drone starting configuration, tested at two time steps. The existing original-controller paths both completed five seconds. This is an exposed second-seed transfer/regression check: preserved completion alone is not an improvement over that baseline. Full modeled airflow coupling remained enabled in the new runs.

The unchanged controller remembers a persistent difference between requested and actual vertical motion and adds a bounded lift correction. The local Boids rules, aerodynamic calculation, physical parameters, motor lag, geometry and stopping rules remain unchanged. Each flock continues to respond to its own changing neighbors and motion.

| Time step | Vertical memory | Saved original controller |
| --- | --- | --- |
| 0.005 s | completed at last completed t=5.0000 s; reason: none | completed at 5.0000 s |
| 0.0025 s | completed at last completed t=5.0000 s; reason: none | completed at 5.0000 s |

In plain language: both controllers completed this arrangement. At five seconds, the corrected flock had fallen about 0.51 m on average, versus 2.29 m with the original controller. This is less recorded descent; height alone is not proof of better tracking of the changing flock request.

## Compare at the same saved endpoint

Height refers to the drone center; the modeled body radius is 0.075 m. The following comparison stops at the last integer step present in both paths. Later candidate-only positions are not compared to an invented baseline suffix.

| Time step | Common nominal time | Drone 17 height, memory | Drone 17 height, original | Fleet mean-height difference, memory minus original |
| --- | ---: | ---: | ---: | ---: |
| 0.005 s | 5.0000 s | 3.592007 m | 1.733773 m | 1.778653 m |
| 0.0025 s | 5.0000 s | 3.592015 m | 1.733773 m | 1.778653 m |

This is a finite-path controller intervention inside the implemented model. The second configuration was already exposed, and its baseline completed. It was excluded from the prior first-seed diagnostic and is tested here under a separate protocol. This is not unseen or randomly sampled validation. The two time steps are dependent resolution checks, not independent flight trials or a population success rate. The gain was fixed before execution and no tuning or numerical reruns followed the outcomes.

## What was checked

The independent saved-data audit checked 12,000 attempted native stages (12,000 successful, 0 refused), 3,000 completed steps, 768,000 full derivative rows and 64,000 controller-memory rows. Initial physical words match the old saved starts. Every reached segment join retains its own physical state and controller integral, previous error and update count. Zero baseline reruns occurred.

The audit checks saved native evidence/load consumption, quaternion projection, rigid-body/motor-lag derivatives, projected RK arithmetic and the unchanged memory recurrence. It does not rerun the native geometry/root solver, Boids steering, inherited actuator control law or contact geometry. The old baseline depends on its prior published audits/exports. Numerical consistency does not establish physical accuracy.

Candidate coarse/fine maximum common-endpoint center difference: 2.50359036e-05 m over 1001 paired endpoints. This is sampled resolution sensitivity, not a continuous-time error bound or convergence proof.

Candidate controller-error and integral statistics are retained in the audit export. They describe tracking of each candidate flock's own changing Boids request. The old replay lacks fleet desired-velocity data, so no matched fleet tracking-improvement claim is made. Integral-state clamping is distinct from saturation-aware anti-windup.

## Visible evidence and next question

The [paired Three.js replay](viewer/) shows saved completed endpoints, the floor and highlighted drone 17 with its trail. It reports actual saved times and stop categories, separates refused trial metadata from completed motion, and hides missing suffixes. It contains no online physics simulation. Other factory obstacles are omitted and the larger wire halo is a visibility aid.

Prospectively test a small fixed set of previously unexecuted starting configurations with matched original-controller and unchanged memory-controller arms. Keep all settings fixed, define comparison measures before execution, and preserve all outcomes. Longer horizons require their own bounded allocation.

No physical aerodynamic validation, general flight safety, new integral-control method, optimality, population reliability, large-swarm scalability or speedup is established. Relevant real research and its reading limits remain in [LITERATURE.md](LITERATURE.md).

[Protocol](PROTOCOL.md) · [Independent audit](audit/audit.json) · [Result claims](RESULT-CLAIMS.md) · [Allocation closure](ALLOCATION-CLOSURE.json) · [Restart](RESTART-RESULT.md). All raw evidence remains in ordered lossless parts under results/. Final public identity is recorded separately in publication-receipts after verification.

## Preserved file-read anomaly

The auditor encountered a timeout (errno 60), then an empty-byte mismatch on the same compressed part. Its third permitted identity read matched the exact saved hash before the bytes were parsed. Both anomalies are retained in audit/audit.json. No simulation, parsing or arithmetic was retried. The audit then completed within its fixed allocation; a successful checksum read does not explain the underlying storage cause.
