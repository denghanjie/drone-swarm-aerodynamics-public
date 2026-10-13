# Robustness results

All 24 analytic/synthetic fixture groups passed on the final reviewed source, in the second authorized exclusive attempt. The first 23-group attempt and its exact source are also retained. Neither attempt ran compatibility, genuine Boids trajectories, or benchmarks.

- Latest result: `results/attempt-2026-10-13T12-09-00-853Z/test-results.json`
- Latest invocation/source/config provenance: `results/attempt-2026-10-13T12-09-00-853Z/invocation.json`
- Tested harness SHA256: `79604e0686fdf3764203cf5883c36beaf235e5bcc64af12a88ddd880e3b23cac`
- Source changed during either attempt: false
- Numerical unit-check failures: none
- Second harness administrative elapsed time: 119.662 ms, not a throughput measurement
- Command: `timeout --signal=TERM --kill-after=2s 43s node swarm-temporal-campaign/robustness/test-harness.cjs --parent-authorized`
- Every tested source byte is retained in content-addressed objects linked by the attempt records.

The final suite covers four held scalars with current endpoint loads; both refresh limits and the terminal old hold; analytic event-aware trapezoids; world torque rotation; same-path stride comparison; all-common-prefix vector disagreement; nonfinite metric failures; interior and terminal domain-failure retention; each-seed stopping gates and failed-member evidence; terminal no-refresh; Float64/gzip/checksum/shape checks; prospective logical storage caps and failure reserve; mocked external watchdog deadlines and honest last-checkpoint records; a final validity write crossing the wall cap; complete-bin display maxima; and actual CommonJS initialization of campaign and reconstruction modules.

The first suite mocked reconstruction. Later static review found the export-order circular-initialization defect and reporting/deadline gaps. These were fixed before the second attempt, and the added/extended checks now cover them. The first result is a passing report only for its stated 23 properties, not evidence that the untested old integration was correct. See `POST-ATTEMPT-FINDINGS.md`.

Synthetic gate and initialization fixtures mock dynamics, controller, fields and raw-series data. The CommonJS loader and reconstruction source are real. Watchdog fixtures use deterministic mock processes and clocks; no real stalled CPU process or concurrent load was used.

These checks establish narrow software properties. Genuine reference/cadence acceptance still depends on the authorized campaign and every source, reference, quadrature, safety and resource gate. They establish no physical accuracy, full-mission or large-swarm performance, flight safety, or hardware-throughput claim.
