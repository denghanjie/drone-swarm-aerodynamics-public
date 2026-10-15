# Airflow cadence checkpoint: a conditional cost–error baseline

Reusing airflow values saved computation and introduced load discrepancy in two prescribed one-second encounters. The independently written formula agreed to rounding precision. **This is a model diagnostic, not physically validated flight, an accepted cadence, or a novel method.**

The instantaneous comparison evaluates the same quasi-static wake formula at known poses. No controller or path integration was used for the scientific encounters. The earlier integrated-reference failures on the newer main branch remain unchanged.

## Measured peak discrepancies

Maxima below include uniform samples plus the old-hold value immediately before every refresh, including t=1 s. They are observed maxima, not continuous-time error bounds.

| Encounter | Airflow interval | Lift discrepancy (mN) | Pitch discrepancy (µN·m) | Query calls | Median query loop (ms) | Observed range (ms) |
|---|---:|---:|---:|---:|---:|---:|
| lateral-pass | Every 1 ms query | 0.000000 | 0.000000 | 1001 | 14.045125 | 13.781625–14.614000 |
| lateral-pass | 10.0 ms | 1.849104 | 41.682859 | 101 | 1.843000 | 1.798750–1.893708 |
| lateral-pass | 5.0 ms | 0.925021 | 20.892924 | 201 | 3.209333 | 3.143125–3.246750 |
| lateral-pass | 2.5 ms | 0.462526 | 10.452911 | 401 | 5.869750 | 5.792834–6.079417 |
| offset-approach | Every 1 ms query | 0.000000 | 0.000000 | 1001 | 13.926333 | 13.672208–14.281459 |
| offset-approach | 10.0 ms | 0.018951 | 1.217334 | 101 | 1.800917 | 1.703750–2.022083 |
| offset-approach | 5.0 ms | 0.009486 | 0.608974 | 201 | 3.262500 | 3.151875–3.592292 |
| offset-approach | 2.5 ms | 0.004745 | 0.304564 | 401 | 6.093375 | 6.022375–6.270500 |

All roll discrepancies were at rounding scale (maximum 4.34e-19 N·m), consistent with the symmetric chosen paths. This is not evidence that roll is generally unimportant. Force is normalized by mg and moment by mg times the opposite-motor distance in the machine-readable metrics. Different prior studies use different arm-length conventions; percentages are not interchangeable.

## What passed and what remained unresolved

- Eight implementation fixture groups passed. Over the fixed fixtures and every refined observation pose, the independent arithmetic comparator differed by at most 5.55e-17 m/s in inflow, 1.11e-16 N in thrust, and 1.89e-18 N·m in moment. This checks the specified equations, not their physical truth.
- All augmented peak metrics agreed between the 1 ms and 0.5 ms grids for these cases. At 5 ms refresh, uniform-sample RMS thrust and pitch changed by more than the frozen 5% sampling screen in both paths; all four affected comparisons remain unresolved. No further refinement or changed threshold was attempted. Other sampled RMS comparisons passed their declared screen; that is limited self-consistency, not an integral-error bound.
- Shorter holds reduced the observed peak force and pitch discrepancies in both paths. The same 10 ms interval gave very different errors in the two encounters; they also differ in separation and motion, so this does not isolate movement direction as the sole cause.
- A source with its motor states set to zero still produced the same field, as the fixed-hover model defines. This fixture documents why source-thrust changes require a different physical assumption; it is not evidence of a real unpowered wake.

## Timing scope and resource record

Five recorded technical repeats followed one warmup per path/variant, with rotated order. All timed output checksums exactly matched the retained primary samples. Query-loop time includes prescribed-pose construction, scheduling, field evaluation, receiver law, wrench computation, budget/counter instrumentation and timing overhead. Field and receiver timer buckets are separately saved. It excludes raw persistence, independent checks, flight dynamics, local Boids, contacts, rendering, GPU/transfers and browser overhead. This very small two-drone workload on one Apple M4 does not establish browser or 5,000-drone feasibility. No confidence interval or multi-device population claim is made. A slow release download was active in the background; no other solver or benchmark ran concurrently.

The sole supervised invocation used 0.513021083 s wall time, 29,924 total field calls, and 3,184,006 raw bytes, within 120 s / 40,000 calls / 32 MiB. Source was committed and pushed as `fd857ed1f5a4662ff98635e1998b53944b98738a` before execution. All raw files are included in this result checkpoint. No retry occurred. An independent saved-record recomputation added 0.097805959 s and passed 25,671 arithmetic/accounting checks; it reevaluated no physical model. Total accounted science/review time is 0.610827042 s.

## Evidence and next decision

- [Three.js recorded diagnostic](viewer/index.html), tied to checksum-verified raw loads and exact prescribed poses. It is not a live flight simulation.
- [Prospective protocol](PROTOCOL.md), [source freeze](freeze.json), [result JSON](results/result.json), [raw records](raw/), [claim ledger](claims.md), [independent saved-record review](results/independent-review.json), [reproduction](REPRODUCE.md).
- [Prior-work and literature map](literature-and-prior-work.md); [physical-data discovery](physical-data-discovery.md). Public telemetry exists, but no compatible force/moment-versus-flow dataset with necessary metadata and reuse terms was secured.

Next: test a causal temporal predictor against simple holds under a separately frozen protocol and fresh challenge paths. It must retain event-aware peaks, compare at matched field calls, expose onset/turning failures, and include current receiver response. Do not call extrapolation new or reuse these cases as fresh confirmation. If physical evidence remains unavailable, all conclusions stay numerical and model-conditional. The closed M31 diagnosis and failed historical reference screens cannot be reopened by this checkpoint.
