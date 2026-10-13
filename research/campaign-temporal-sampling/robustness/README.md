# Temporal harness robustness checks

These are bounded analytic and synthetic harness fixtures. They are not genuine local 3D Boids campaign records, independent swarm replicates, benchmarks, or physical validation. They do not change frozen production mechanics or campaign seeds, N, horizon, or matrix.

Status: two separately parent-authorized unit attempts are complete. The final 24-group attempt passed; see RESULTS.md. Further numerical execution still requires parent authorization. Source inspection and `node --check` do not run the fixtures.

Run when authorized:

`node swarm-temporal-campaign/robustness/test-harness.cjs --parent-authorized`

The fixture loader intercepts output and replaces costly orchestration dependencies where needed. Production replay and gate code are exercised with short synthetic arrays; scalar-load checks call the frozen physical load function only on explicitly constructed endpoints. All artifacts stay under `robustness/results/`. Every failure, command, source hash, configuration and runtime is retained. The suite does not call the campaign CLI or create fresh coupled trajectories.

Coverage planned:

- Four held projected scalars; current endpoint motor states and orientation; preserved nominal yaw
- Both refresh limits and terminal left limit; event-aware trapezoids; zero and constant inflow
- Torque rotation into the world frame before integration; fine/coarse stride consistency
- Invalid stride and nonfinite screen inputs; domain and invalid-input failure retention
- Stopping gate reduction floors, each-seed gating, no continuation after a failed gate
- Terminal no-refresh and production event ordering via synthetic dependency injection
- Binary Float64 little-endian/gzip roundtrip and checksum tampering
- Source graph completeness and immutable source/config/plan provenance
- Hard wall/job/storage caps and checkpoint honesty, by static review and separately authorized bounded supervisor fixtures

No watchdog load fixture may overlap campaign measurement. Supervisor tests will use an intentionally stalled synthetic child only, never an extra numerical case.
