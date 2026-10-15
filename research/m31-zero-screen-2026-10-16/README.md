# M31 checkpoint: simpler exact-zero screening

**The forces stayed the same; neither simplification met its preset speed-usefulness rule on both test sizes.** This is a completed negative engineering result. It is not a numerical failure to retry, a new algorithm, or a physical-validation result.

[Open the Three.js evidence view](viewer/index.html). It shows the actual saved static drone poses, source categories, rotor inflows and forces. E/L switching leaves the categories and loads unchanged while showing different center-norm counts. It does not animate a new Boids flight or establish browser simulation speed.

## What we tested

Think of checking whether another drone can affect this drone. Z already discards contributions known to be exactly zero, but still does bookkeeping for an approximation it no longer uses. E removes that bookkeeping. L also waits to calculate a radial distance until a cheaper downstream check says it is needed. M keeps all eligible sources and supplies a matched full-traversal comparison. All methods preserve the existing wake and receiver equations.

The frozen campaign used 24 previously exposed small fixtures and two fresh static lattices with 1,000 and 5,000 drones, seeds253741/608897. There is only one fresh input per size. Eight paired timing blocks per input are repeated technical measurements, not eight independent swarms. Local 3D Boids remain part of the wider project; these inputs isolate static force computation and do not integrate motion.

## Evidence and outcome

All26case checks completed:22valid inputs and4expected domain rejections. E and L matched Z bit for bit in every saved17-component valid output, including signed-zero distinctions. All full methods agreed with the independent reference within frozen numerical gates. No positive contributions were omitted.

The sole saved-only review passed1,371,035checks with0failures. It reconciled40source pins,275raw files,26,810,779bytes,202calls,72timings and104,000,424retained independent classification bytes. Full successful source-term vectors and repeated timed matrices were not retained; runtime assertions cover those unavailable values. See [independent review](INDEPENDENT-SAVED-REVIEW.md) for precise limits.

Each speed rule required a median paired ratio at most0.95 AND at least7of8strict wins, on both fresh inputs. A ratio below1means less time. We did not change the rule after seeing the data.

| Input | Comparison | Median paired ratio | Strict wins | Criterion |
|---|---|---:|---:|---|
| fresh1000 | E / Z | 0.990559335 | 5 / 8 | Unmet |
| fresh1000 | L / E | 0.961402996 | 8 / 8 | Unmet |
| fresh5000 | E / Z | 0.952401558 | 6 / 8 | Unmet |
| fresh5000 | L / E | 0.977629068 | 5 / 8 | Unmet |

L reduced the classifier's center radial norm count by roughly49%, derived from saved branch counts and static evaluation order. That is not a49%runtime improvement and not hardware instruction profiling. Individual downstream-exit source IDs were not saved, so the viewer does not color those IDs.

| Input | E center norms | L center norms | Avoided norms | Reduction |
|---|---:|---:|---:|---:|
| fresh1000 | 706,960 | 359,640 | 347,320 | 49.1287% |
| fresh5000 | 6,614,678 | 3,363,552 | 3,251,126 | 49.1502% |

For context, measured complete-query durations were:

| Input | Method | Median seconds | Min–max seconds |
|---|---|---:|---:|
| fresh1000 | M | 0.104677000 | 0.102911458–0.112182792 |
| fresh1000 | Z | 0.087028500 | 0.085069583–0.096543750 |
| fresh1000 | E | 0.086798146 | 0.085186167–0.092575458 |
| fresh1000 | L | 0.082701167 | 0.081938000–0.089488666 |
| fresh5000 | M | 1.299449480 | 1.282076291–1.382626083 |
| fresh5000 | Z | 1.192637416 | 1.084263583–1.221730875 |
| fresh5000 | E | 1.083176459 | 1.072171500–1.198452625 |
| fresh5000 | L | 1.058974854 | 1.038007375–1.198738292 |

The paired ratios above are not ratios of marginal medians. Cost includes the instrumented query, grid, screening, rotor fields, receiver roots, loads and checksum in Node24.19.0 on AppleM4/Darwin25.5.0arm64. It excludes input generation, validation, compression/persistence, rendering, transfers to a GPU and flight integration. E/Z removes a package of unused policy/reporting work; L/E changes scheduling with matching instrumentation. Shared-machine/JIT/GC/thermal/order effects remain. No statistical significance or equivalence claim is made.

## What this means for the research

The particular changes preserve the finite numerical predictions, but do not meet the chosen practical threshold. That does not prove they never help. It also does not justify more tiny adjustments against the same exposed inputs. The next proposed question is whether browser f32 arithmetic can represent the wake/receiver calculation accurately enough, with representation error separated from arithmetic error before speed testing.

Related exact-zero screening already exists in later DOT work. [Prior-work comparison](PRIOR-WORK-COMPARISON.md) and [existing-work audit](EXISTING-WORK-AUDIT.md) explain the different numerical contracts and baselines. Current M is not claimed to be DOT's fastest lean method. No novelty,5,000-drone browser real-time, trajectory accuracy or physical truth is established. Earlier failed path comparisons remain failed. The receiver closure and nominal40msmotor-command lag still lack compatible experimental validation.

This advances the original roadmap's numerical verification and accuracy–cost investigation. It does not finish the research or satisfy the publication gate. See [claims](claims.md), [frozen protocol](PROTOCOL.md), [reproduction record](REPRODUCE.md), [restart](POSTRUN-RESTART.md) and [raw results](raw/result.json).

Source frozen and independently verified before execution: [4717d9b](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/4717d9b5bb3d82fe2b3d75ea26801de201d124b6). FreezeSHA2562f1313c8476c09352ae22711be15afce5c7a3d229755a0502b1266201cb41f6a. Sole science53.795325667s; sole review3.262752916s under separate300s/60scaps; both terminal. All prior source/protocol documents retain their prospective wording as immutable historical records.
