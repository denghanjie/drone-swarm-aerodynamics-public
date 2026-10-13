# Claim–evidence audit: exact-equation airflow campaign

## Main finding

The saved records support a bounded CPU implementation-efficiency result for one **physically unvalidated finite-support model**. They do not establish aerodynamic accuracy, long-horizon trajectory convergence, GPU throughput, or 5,000-drone feasibility.

**The original report required one correction, now documented in [CORRECTIONS.md](../../campaign-exact-efficiency/CORRECTIONS.md):** the independent nonzero field gate passes **3/12**, not 4/12, against the previous-zero implementation. Four cases meet the median-only threshold; one fails the separate upper-confidence-bound condition. The primary result remains **8/12**. Frozen evidence was not modified by this audit.

## What was independently checked

- All 151 primary cases (604 variant comparisons): zero saved inflow, force and moment errors; all bitwise indicators true.
- All 30 primary timing records and 720 summaries: paired medians, 5,000-resample bootstrap endpoints, gates, fixture identities, checksums and repetition counts agree with the raw measurements.
- All 14 independent field records and 56 summaries: 2,000-resample intervals and stored flags reproduce. Twelve nonzero cases all pass against legacy; only three pass against previous-zero. The two zero/isolated controls are reported separately.
- Both whole-pipeline records reproduce. Lean/previous-zero is 0.91124 [0.90124, 0.95959] in the primary workload and 0.95958 [0.93573, 1.01831] independently. Neither meets the 10% saving screen.
- All 14 short Boids records complete. Eight matched pairs have identical saved initial/final states, poses, held fields and stored rolling hashes. Full intermediate streams were not retained, so those hashes were compared, not reconstructed.
- The N=16 one-second refinement differences recompute to 7.21 nm for the physics-step change and 7.01 mm for airflow-refresh change, both below the 1 cm screen. This is a short-window screen, not a convergence proof.
- Eleven upstream source files and the candidate match their recorded SHA256 identities. Independent fixture, transformation, ownership and API assertion counts are 85, 45, 33 and 39 respectively.

No new simulation, timing, physical experiment or historical mission reanalysis was performed. The reproducible read-only checker is [audit-records.cjs](audit-records.cjs); detailed calculations and input content hashes are in [audit-results.json](audit-results.json). [claims.json](claims.json) gives every exact claim, status, raw-record identity, uncertainty, counterevidence and falsifying test.

## Corrected independent gate

The three passing nonzero cases against previous-zero are:

- 628791 / N=100 / sparse
- 628791 / N=200 / tilted
- 628792 / N=100 / tilted

The additional median-only case, 628791 / N=100 / tilted, has ratio **0.8721603**, but its 95% paired bootstrap interval is **[0.7046979, 1.0105362]**. Its saved `qualified` flag correctly says false. The discrepancy is in the prose count, not the individual raw summaries. No family/count passes on both independent seeds. See [the decisive raw record](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/dot/spatial-wake-pruning/research/campaign-exact-efficiency/robustness/raw/independent-field-628791-100-tilted-lean.json).

## Claim statuses

| Claim | Status | Evidence boundary |
|---|---|---|
| 151 same-equation checks pass | Confirmed within scope | Saved finite test cases, not physical truth |
| Positive contributions preserved for every accepted input | Provisional support | Broad tests and code inspection; no universal numerical proof |
| Original v0 support bound never falsely culls | Contradicted | Retained extreme-translation counterexample |
| Primary incremental gate is 8/12 | Confirmed within scope | N=100/200, two seeds, three families |
| Independent incremental gate is 4/12 | Contradicted | Correct count is 3/12 |
| Substantial improvement over legacy | Provisional support | Observed CPU workloads; previous-zero is the stronger incremental comparator |
| General ≥10% incremental gain | Unresolved | Mixed primary/fresh results, modest pipeline gains |
| 14 records and eight saved-data matches | Confirmed within scope | N=16/1 s and N=50/3 s plus two refinements |
| Long-horizon convergence, physical receiver response or multi-wake accuracy | Unresolved | Required reference evidence absent |
| Current N=500/5,000 or WebGPU throughput | Unresolved | No such current-campaign measurement |
| Physical accuracy–computation frontier | Hypothesis | Original research target, not an achieved result |

## Original eight-step framework retained

| Original step | Current contribution | Unmet gate |
|---|---|---|
| 1. Define the experiment | Current source/configuration and bounded protocol are identified. | Independent physical prediction contract and vehicle-matched measurements remain needed. |
| 2. Build one credible drone | Mechanics byte identity and numerical software comparisons checked. | Measured hover, attitude, motor and flight agreement remains unestablished. |
| 3. Model two-drone interaction | One-law implementation checks and original counterexample retained. | Independent source-flow and receiver-force validation remain missing. |
| 4. Model overlapping wakes | Overlap implementation equivalence checked. | Multi-wake superposition, cutoffs and airflow-cadence accuracy remain unvalidated. |
| 5. Test a real local flock | Short genuine local 3D Boids records and saved equivalence verified. | Full-mission behavior, numerical robustness and real-flight validity are not established by these short records. |
| 6. Accelerate validated calculations | CPU acceleration of an unvalidated model is measured, with corrected incremental counts. | Physical validation and present-pipeline GPU equivalence/throughput remain open. |
| 7. Scale the actual flock | Prescribed-state checks/timing reach N=200; recorded current Boids reaches N=50. | N=500 exact-campaign promotion stopped; 5,000 coupled browser feasibility remains a target. |
| 8. Evaluate the contribution | A reproducible implementation-efficiency contribution with explicit negative evidence is supported. | A physical accuracy–cost frontier, external novelty comparison and safe-flight claim are not established. |

Historical roadmap claims about factory missions, 1,000/5,000 candidate passage, longer trajectory failures and observer experiments are **explicitly not re-audited here**. They remain separate historical claims, even where their narrative is relevant. The current short exact-equation campaign must not inherit their mission-completion or scaling scope.

## Most informative next experiment

Prioritize **independent one-source/one-receiver force validation under matched operating conditions**. Use measured receiver-plane inflow, if available, to isolate the receiver law before testing source-profile and overlap errors. Freeze the unit/geometry mapping, response law, held-out condition groups, accuracy tolerance and uncertainty analysis before inspecting residuals.

Bound the first evaluation to a compact data-supported matrix, up to three inflow strata and three receiver operating levels. Require geometry, source and receiver command/RPM or equivalent operating-condition metadata, repeated-force observations and measurement uncertainty. Stop after a data-adequacy decision and one frozen held-out evaluation. Persistent held-out force bias beyond the declared tolerance falsifies the response model in that scope.

If those observations cannot be acquired, report the missing reference explicitly. A synchronized common-state airflow-cadence refinement can make useful numerical progress while data access is resolved, but cannot supply physical validation. More timing runs alone would improve a secondary uncertainty while leaving the central physical-error axis absent.

## Interpretation limits and provenance

The model fixes source strength from isolated-hover weight; receiver lift uses a constant-ideal-induced-power assumption; wakes are added algebraically and truncated. Exact implementation agreement preserves those assumptions. It does not validate them. Small paired timing samples, short batching and workload-specific instrumentation also prevent hardware-generalized performance conclusions.

Source checkpoint: `c024dfc27b9e6b7cd5b39132164d1339cb95b12f`. Candidate SHA256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`. The first published checkpoint is `d83a2a36d166eb2b3e83aa2cb673bd4ba1b2b4b3`; it is not assumed to contain all later evidence. Campaign links use the named branch and are paired with audited content hashes in the machine-readable evidence inventory.
