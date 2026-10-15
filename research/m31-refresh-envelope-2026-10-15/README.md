# M31 refresh envelope: checking has a cost

The error-envelope scheduler met the numerical load targets at all checked samples of this **one prescribed two-drone encounter**, but a meaningful speed advantage over the 2.5 ms hold is unestablished. The simple 5 ms causal predictor had smaller sampled peak errors and lower recorded total time than the envelope. This is useful negative evidence against assuming that fewer field calls make an adaptive algorithm faster.

The first question was: can bounds on how much the prescribed input can move tell us how long to reuse an airflow calculation? The candidate searches several future intervals, bounds the resulting lift and torque errors, and accepts the longest interval within the chosen targets. These checks themselves cost computation. The comparison includes that cost.

[Open the Three.js recorded-model viewer](viewer/index.html). Serve the repository root over HTTP as described in [reproduction](REPRODUCE.md). It shows exact saved poses and airflow arrows, with six comparison methods, update-boundary values and a receiver close-up. It does not integrate flight or run Boids.

## Results

Source frozen and pushed before execution: `f56909390c4875db5a9241ba6bc79596b84628a6`. All variants use unchanged M28 `sum-rotor` field and the same current-pose receiver law. Orientations and nominal motor thrusts are fixed. One second of prescribed motion; primary 0.5 ms queries and refined 0.25 ms queries; peaks also include old values immediately before each refresh.

| Method | Peak lift error, mN | Peak roll error, µN·m | Peak pitch error, µN·m | Median loop, ms | Five-repeat range, ms | Field / bound calls per pass |
|---|---:|---:|---:|---:|---:|---:|
| instant | 0.000000 | 0.000000 | 0.000000 | 27.135500 | 26.822458–27.941375 | 2001 / 0 |
| hold-10ms | 3.359653 | 24.736207 | 74.869986 | 2.022667 | 1.952417–2.248583 | 101 / 0 |
| hold-5ms | 1.688122 | 12.384094 | 37.751544 | 3.555208 | 3.260875–4.081833 | 201 / 0 |
| hold-2.5ms | 0.845139 | 6.198530 | 18.903571 | 6.393833 | 5.871458–6.573125 | 401 / 0 |
| predict-5ms | 0.193205 | 1.515585 | 4.161062 | 3.569500 | 3.479500–3.901333 | 201 / 0 |
| envelope | 1.000160 | 5.880452 | 21.847394 | 6.367416 | 6.241667–6.844458 | 196 / 615 |

Numerical targets were 1.32435 mN lift and 104.883169 µN·m for each moment. The 10 ms and 5 ms holds exceeded the lift target; 2.5 ms hold, predictor and envelope passed the sampled targets. These targets are analyst choices, not flight-safety limits. The instantaneous formula is a same-model reference, not aerodynamic truth.

The envelope made 196 field calls and 615 bound attempts per timed pass. The 2.5 ms hold made 401 field calls but had almost the same median loop time, with overlapping ranges. The 5 ms predictor made 201 field calls and had a lower, nonoverlapping recorded timing range in this encounter. Five technical repetitions do not represent an independent population or establish a universal ranking. Timings include pose creation, scheduler, horizon search, bounds, receiver roots and accounting. They exclude independent validation, raw persistence, rendering, flight dynamics, Boids and GPU work. The unchanged field API includes a grid even for this pair; no claim is made against an optimized direct two-drone implementation. A slow independent download of earlier evidence was active in the background.

## Verification and what remains uncertain

- Independent direct-pair/rotation/bisection oracle agreed at every fine-grid input: maximum lift difference 1.11e-16 N; roll 1.31e-18 N·m; pitch 1.06e-18 N·m. This checks implementations of declared equations, not their physical validity.
- 12,585 saved sample/observable interval checks, zero observed target violations. Worst interval excess −1.427455339278054e-15. This is sampled containment; the numerical margins are not formally certified outward rounding.
- Every augmented-peak and new event-split RMS grid screen passed. The earlier pilot's four failed uniform-RMS checks remain failed. This prospectively changed estimand does not repair that earlier evidence.
- Independent saved-record review recomputes metrics, causal prediction, signed intervals, accounting, hashes and timing checksums without evaluating the model again. Its first arithmetic checker used a different operation order at one predictor sample; the observed 5.42e-20 m/s discrepancy and checker correction are retained. The corrected review checks exact predictor values and passes 57,504 checks.

The complete scientific invocation used 0.524042875 supervised seconds, 27,709 field calls (including 4,001 independent oracle calls), 4,309 bound calls and 6,278,564 raw bytes. It ran once. All raw results, including unfavorable baselines, are retained. See [budget](results/budget.json), [independent review](results/independent-review.json), [claim ledger](claims.md), [frozen protocol](PROTOCOL.md) and [postrun restart](POSTRUN-RESTART.md).

## Research decision

Retain the envelope as an examined candidate, not the preferred algorithm. Challenge the simple predictor on fresh, prospectively specified paths involving support entry/exit, reversal, orientation change and multiple source wakes. A result on this already exposed path cannot count as fresh confirmation after tuning.

There is no novelty claim, physical validation, accepted operational refresh cadence, verified integrated long-flight trajectory, or 5,000-drone real-time result. The earlier Milestone 31 trajectory discrepancies remain unresolved. The original eight-step framework and later main/DOT work are preserved.

References used for the field, receiver assumptions and existing temporal work are linked in the [verified literature and prior-work note](../m31-airflow-cadence-2026-10-15/literature-and-prior-work.md) and [eight-source evidence ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md). The interval construction is a direct derivation for those equations, not a literature novelty claim.
