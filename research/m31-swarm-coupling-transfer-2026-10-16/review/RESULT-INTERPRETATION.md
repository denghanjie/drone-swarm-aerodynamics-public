# Adversarial interpretation of the completed historical swarm transfer

Prepared 2026-10-16 from saved `results/analysis.json`, `results/independent-review.json`, both supervisor records, the source manifest, and source-review documentation. This note reads existing evidence and sums saved work counters only. It does not rerun the candidate/checker, decode historical target states, calculate new geometry/loads, or launch timing measurements. Proposed follow-up work below is a recommendation, not a new allocation.

## What the result establishes

The assumed four-rotor frozen-pose coupling calculation transferred from small designed fixtures to the four prescribed historical swarm snapshots, including three 5,000-vehicle states. Every selected snapshot satisfies the declared numerical input/domain contract, has no unsupported near-field or invalid terms, and has no positive dependency violating strict height descent or the actual sorted order. Both direct evaluation and synchronous Picard finish with all requested rotor/source records and pass the separate saved-record review.

This is stronger evidence than comparing two solvers on one potentially truncated candidate matrix. The checker reconstructs geometry and sparse coefficients independently, compares the full 304,000,000-element symbol census exactly, and reports zero symbol, sparse-support or coefficient-mismatch rows. Its largest saved coefficient difference is approximately 2.22e-15, within the declared 2e-12 absolute plus 2e-12 relative tolerance. It then uses independently reconstructed coefficients, normalized nominal-force weights and a distinct hyperbolic cubic formula. It checks every saved Picard update, final generating rotors, final residual map, stopping behavior and work-accounting identities.

Across the four snapshots, 64,000 returned rotor forces and 16,000 source amplitudes are compared for each solver. Those are 16,000 vehicle instances across repeated historical states, not 16,000 independent vehicles/experiments. The largest recorded relative rotor-force disagreement with the independent descending result is approximately 2.54e-15 for the candidate direct solver and 2.27e-14 for Picard; the corresponding largest source-amplitude disagreements are approximately 3.45e-16 and 9.20e-15. Both satisfy the predeclared 1e-9 relative tolerance.

The saved report has 581 passed grouped checks and no errors. A grouped vector assertion can cover millions of entries. Neither 581 nor 304 million is a count of statistically independent trials or a confidence level.

| Snapshot | Positive rotor coefficients | Maximum dependency depth | Picard updates | Ordinary bound Lmax |
|---|---:|---:|---:|---:|
| N=1,000, 20 s | 14,166 | 8 | 7 | 0.2630 |
| N=5,000, 20 s | 115,943 | 14 | 10 | 0.3147 |
| N=5,000, 60 s | 110,491 | 15 | 10 | 0.3360 |
| N=5,000, 180 s | 79,600 | 8 | 8 | 0.3557 |

The maximum tilt across the selected records is approximately 8.37 degrees, and every recorded vehicle satisfies the numerical 45-degree sufficient-condition census. All ordinary bounds are already below one. The application to a larger workload is established; the stronger logarithmic theorem's additional convergence domain has still not been exercised by these data. There is no reason to select a harder replacement snapshot after this result.

## Evidence boundaries that matter

**Implementation independence is not physical independence.** The checker is a separately expressed Python/NumPy implementation with a different root evaluation, not an external measurement of aerodynamic forces. Both implementations evaluate the same assumed source-strength scaling, wake support/cutoffs and ideal-power receiver law on the same saved inputs. A shared model error can pass every check. The historical motor-lag thrust states are being used as nominal forces for this new law; they do not identify actual held shaft power, RPM, PWM or actuator response under changed inflow.

**The force changes are counterfactual model outputs.** The saved source-load-ratio minima span roughly 0.563–0.645 and means roughly 0.877–0.918 across cases. These ratios are useful visual summaries of the assumed calculation. They do not measure real thrust loss, demonstrate insufficient flight authority, or validate historical trajectories under aerodynamic feedback. Historical positions and attitudes came from airflow-off motion; the new loads were never fed into those trajectories.

**Floating consistency is not an exact-real certificate.** A candidate residual of exactly zero is a floating-point fixed point of its own rounded map. The independently evaluated direct residuals are around 3.3e-16 rather than zero; the largest independent Picard residual is about 9.19e-15. The largest independent normalized source/receiver mismatch is about 1.15e-14. These support numerical consistency at the recorded tolerance. They do not supply outward-rounded root/map error bounds or permit a zero-error claim. A residual-based theorem bound must include map/root evaluation error before being advertised as a certified force bound.

**The selection is narrow and already exposed.** The snapshots share seed/scenario structure; the three large states share a historical trajectory. They were selected prospectively for this campaign but had been used in earlier research. They are not new held-out physical tests. Success at these states neither establishes domain admission along the intervening trajectory nor guarantees admission after aerodynamic feedback changes poses, attitudes and actuator states. No cyclic, highly tilted, unsupported-near, nonpositive-nominal or numerical-boundary success was required or observed here. Code paths for rejection were reviewed statically; this successful census does not empirically test them.

**Operation accounting is not a timing result.** The checker validates saved counters against the specified algorithm and saved map values. It does not independently observe each internal loop instruction. Source inspection and reproducible pinned execution strengthen that accounting, but it remains an algorithmic work record.

Both supervisor records pin source commit `702abf6b02d53b1008495e2fa579aabf58a445c5` and manifest SHA-256 `937f60cbcee413066c3d7a2ca3d6374be2b76f233032b903e743625e6e2ebed3`. They record return code zero, no timeout, consumed candidate/reviewer locks and empty stderr. The candidate elapsed record is about 5.55 s; the reviewer record is about 8.39 s. Both explicitly set `performance_measurement:false`. These single whole-invocation observations include unlike tasks and are bookkeeping, not repeated benchmarking, solver latency, a CPU/NumPy comparison, real-time evidence or a speedup. This note has not independently revisited the remote publication receipt.

## What the work counters reveal, and what they do not

Saved counters summed over the four snapshots are:

| Work | Saved count |
|---|---:|
| Directed center tests | 75,984,000 |
| Rotor pairTerm evaluations after the center gate | 25,324,040 |
| Retained positive rotor coefficients | 320,200 |
| Direct solve root closures, excluding residual check | 64,000 |
| Picard solve root closures, excluding residual check | 588,000 |
| Direct positive-term multiplications, excluding residual check | 320,200 |
| Picard positive-term multiplications, excluding residual check | 3,000,302 |
| Direct bisection loop iterations, excluding residual check | 2,910,040 |
| Picard bisection loop iterations, excluding residual check | 26,841,976 |

Each solver additionally performs 64,000 residual root closures and 320,200 residual positive-term multiplications over these cases. Including this required residual verification gives 128,000 direct versus 652,000 Picard root closures. A statement of a 7–10-fold root reduction applies only to each case's solve pass, not the complete verified calculation.

The positive matrices are sparse, but they were obtained using a complete O(N²) center census and millions of rotor branch evaluations. A direct solve reduces the repeated work on the retained matrix; it does not eliminate coefficient discovery, support/admission checks, graph preparation, input packing, or result handling. Conversely, unlike operation counts cannot prove that coefficient construction dominates time: root iterations, transcendental arithmetic, allocation, memory access, compression and serialization have different costs. The current run measures no per-stage time shares.

This distinction is central to the accuracy/computation objective. For the same admitted frozen coefficients, direct evaluation offers reduced algebraic work without intentionally changing the assumed solution. Broader claims about efficient aerodynamic simulation still require the cost of refreshing those coefficients as poses change. A matrix reused at an unchanged pose is a different workload from a complete pose refresh. The present scientific evidence pipeline also materializes/compresses a complete symbol tensor and duplicates detailed case records in a combined JSON; that audit cost is a third workload, not necessarily the intended runtime force interface.

## Recommended next bounded question

**On these same fixed four snapshots, how much of a complete CPU force refresh is spent constructing/admitting coefficients versus solving them, and does direct evaluation materially reduce total refresh cost once all required stages are included?**

This is the next computational question because the contract and exact matrix reproduction have now passed at the target size. It avoids optimizing root counts in isolation or changing the physical model to obtain attractive timing. It should be a separate prospective timing allocation, with source/input pins, one named hardware/runtime configuration, finite invocation/repetition/wall/memory limits, a fixed case/order policy and failure retention. Do not reopen either completed allocation.

Before measuring, specify the force-refresh interface and distinguish three reported quantities:

1. Complete rebuild from resident saved state through packing, full support/admission and coefficient construction, order/graph handling, solver, required residual check, and usable per-rotor output. Both solver alternatives must receive the same fresh-build obligation; no cached matrix may appear only on one side.
2. Solver-only time on an already-built immutable matrix, explicitly secondary. This can explain the root-count effect but cannot stand in for refresh latency.
3. Full scientific-audit overhead, including input file I/O/hash/decode, complete symbol retention/compression and artifact serialization. Report it separately and state exactly which of these stages are outside the intended refresh interface. Do not silently call a compute-only segment an entire application step.

A reasonable finite proposal to preregister is one warmup plus five paired measured repetitions per fixed case and solver, with a fixed alternating solver order and no adaptive tuning. This implies 48 complete pipeline evaluations including warmups if each path rebuilds independently; an explicit single-run wall/memory cap must be agreed before dispatch, and exhaustion ends the campaign. It is a planning example, not permission to execute 48 evaluations. Record all samples and phase durations, report distributions descriptively, and keep correlated repetitions distinct from independent swarm trials. Use the existing saved classification/coefficient/force evidence as the correctness gate; any mismatch remains a failed result without a replacement input or post-result retry.

If coefficient/admission construction dominates, the next optimization candidate should preserve the exact three-metre center/support/rejection contract while reducing discovery work, such as an exact spatial candidate index with canonical source ordering and full baseline comparison. The current campaign does not authorize implementing or testing that candidate. If roots dominate, investigate the root/solver implementation under the same numerical acceptance contract. If audit I/O dominates only the scientific pipeline, state that distinction instead of attributing the time to aerodynamics. An overall advantage may be small even when solver-only savings are large; that is an informative result.

Physical accuracy remains a separate necessary gate for the overall research objective. Timing can prioritize computation, but cannot validate the fixed-shape scaling or nominal-to-ideal-power interpretation. A later accuracy question should use independently sourced, compatible force/actuator measurements with declared geometry, operating conditions and uncertainty, preserve a calibration/validation distinction, and compare predictions without fitting to the validation observations. A larger airflow-coupled trajectory run should not be used as a substitute for that force-law evidence. No physical-data search, new numerical experiment, timing run or trajectory allocation is initiated by this note.
