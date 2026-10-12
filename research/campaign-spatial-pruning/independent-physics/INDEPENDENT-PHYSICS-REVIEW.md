# Independent physics and numerical evidence review

Reviewed against source commit `c591ce2b195fa01b895d4ba881a44a4b92fdd703` and candidate SHA-256 `1d9e1afcf9983b900034b7b586c4ffd02ec4b3242c467f8e684fbdda1850d562`.

## Finding

The positive-inflow omission envelope and accumulated receiver force/moment bounds are mathematically consistent with the declared model. Independent finite tests and raw-record sampling found no bound violation. Neither of the two timing studies establishes a useful pruning speed benefit. These results support a bounded numerical approximation study, not aerodynamic validity, flight safety, a fastest-possible exact implementation, or coupled browser/WebGPU feasibility.

## Important distinctions

- The original 3 m center query already encloses the full declared support and receiver offset: maximum required distance is 2.6307104489 m. It is not a previously missing long-range search.
- Both legacy force-only and rotor-aware variants evaluate four rotor locations. The force-only variant suppresses aerodynamic roll/pitch after computing loads; it is not lower-resolution receiver sampling.
- The source uses fixed isolated-hover strength; the receiver law is an uncalibrated constant-ideal-induced-power assumption. The model has no wake history, resolved turbulence, wall flow or relative translational inflow.
- The zero-budget control intentionally pays the same bounding overhead. Its gain over legacy combines same-equation implementation changes and exact-zero support culling. A pruning comparison against it is a mechanism comparison, not proof of an optimal accuracy-cost frontier.
- Greedy omissions depend on source order and can introduce a small moment in a symmetric case. Passing the absolute moment bound does not imply symmetry preservation or harmlessness under closed-loop feedback.

Source: [aerodynamic implementation](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/c591ce2b195fa01b895d4ba881a44a4b92fdd703/outputs/milestone-28-source/aero.cjs), [model limitations](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/c591ce2b195fa01b895d4ba881a44a4b92fdd703/outputs/milestone-28-report.md), [physical validation contract](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/c591ce2b195fa01b895d4ba881a44a4b92fdd703/outputs/research-physical-validation-gate-2026-10-12.md).

## Bound and guard review

For rotor thrust f and nonnegative inflow U, the response derivative satisfies |dT/dU| ≤ sqrt(2 rho A f)/3. Apply that to the sum of all omitted inflows, not each source independently. Summing the resulting four thrust bounds bounds the force-vector norm; summing absolute lever-arm contributions bounds roll/pitch moments. The exact monotone receiver interval tightens the same guarantee. Force AND moment criteria must pass.

At epsilon 0.04 m/s and the assumed 2.25×hover nominal-thrust cap, conservative force and combined roll/pitch bounds are 0.49594% weight and 0.70137% weight-times-arm. The 0.5% / 0.75% screens are numerical design choices, not independently validated physical or application tolerances. Actual-state bounds are necessary outside the assumed cap.

The v1 envelope uses the minimum valid downstream, maximum possible half-width, minimum possible radial coordinate and conservative upper bounds of both nonincreasing fades. The failed v0 no-fade envelope is correctly preserved. Near-field checks precede omission and retain all four original rotor locations; global tilt checks remain independent. Simultaneous domain violations can have a different first-reported pair because traversal order differs, without changing supported/unsupported classification.

## Evidence checked independently

- 336 receiver-law combinations matched an independent bisection solution to 1.12e−16 N and passed the analytical derivative bound.
- 144 baseline pair cases matched independently expressed all-pairs fields within 6.0e−14 m/s.
- A separate 1,200-case candidate sweep included 1,193 valid tilted/boundary/unequal-thrust cases and 7 matching domain exits. It exercised 243 omissions and found no accumulated-inflow, force or moment bound violation.
- The complete compressed raw stream contains 14,544 records: 144 seed/count/family/budget groups ×101 times. The receiver recount is 1,330,776. Stratified full inspection checked 432 records /39,528 receiver rows at t=0, 0.5 and 1 s, covering every group.
- Every one of the eight Boids records matches its index configuration and metrics, has 51 strictly increasing full-state frames, preserves exact initial/final state arrays, and records the actual held-field timestamp. All end at 1 s without a stop.
- The primary timing table was independently recomputed: 0/36 speed-gate passes, across-case median ratios 0.99918/0.99461/0.99238 for the three budgets, and 1.534–1.951× zero-budget/legacy speed improvement. Independent cost evidence also has 0/14 passes.

The 4,848-state accuracy matrix pools development and held-out seeds. Each half has 665,388 receiver comparisons. The held-out force maximum equals the pooled maximum; the pooled moment maximum occurs in development. This distinction must remain visible.

## Support and temporal sensitivity

Separate all-pairs diagnostics change the axial fade/cutoff from 2–2.5 m to 4–5 m and radial fade/cutoff from 2–3 half-widths to 4–5. Four-rotor sampling, receiver law, fixed source strength and near-domain limits remain unchanged. These are extrapolated model assumptions, not a higher-fidelity reference. The 7.56%-weight force difference for a source 3 m overhead and approximately 20% for a constructed 16-source ring illustrate sensitivity to support choices; they are neither measured baseline errors nor a population/uncertainty estimate.

The 6.855 mm refresh-refinement difference in the selected 1 s run is much larger than its pruning perturbation, despite passing the chosen 1 cm screen. One halving and one short interval do not establish temporal convergence. Earlier M28 cadence and M31 long-trajectory failures remain unresolved. Any false-safe classification must be labeled model-relative and distinguish hidden domain exits, modeled contacts, numerical-budget failures, and censored runs.

## Reproduction of this review

If this folder is placed at `research/campaign-spatial-pruning/independent-physics/`, run from it:

```
node audit-baseline.cjs ../../../outputs
node audit-candidate.cjs ../src/pruned-aero.cjs
python audit-records.py ..
```

The final command requires the separately provided `accuracy-raw.jsonl.gz` in the campaign's `results/` directory. It scans existing records; it does not rerun the campaign. JSON files here state the exact scope and observed maxima. These finite checks are not a proof over all configurations or a substitute for physical measurements.

The original eight-step roadmap remains unchanged. Original project material has no selected open-source license; preserved third-party notices remain applicable.
