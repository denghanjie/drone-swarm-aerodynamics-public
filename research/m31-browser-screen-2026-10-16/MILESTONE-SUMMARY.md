# Chrome milestone: the finite screen benefit repeats

The current-position screen passed the predeclared browser test. On both new 5,000-drone states, in each of three fresh Chrome processes, it preserved the checked outputs and met the timing rule. This is a completed computational checkpoint, not completion of the broader research goal.

## What we did, in plain language

The existing calculation considers every ordered pair of drones. Many pairs are too far apart to contribute under the specified model. The candidate uses a cheap coordinate check to skip an expensive distance calculation for some of those pairs; it does not skip enumeration of the pairs or change the load model. L is the unchanged lean calculation; F adds the screen.

We generated three new five-second flights with local 3D Boids and the existing rigid-body dynamics. These flights had airflow off. Their final positions and attitudes became frozen inputs to a separate aerodynamic query. Three fresh, sequential Chrome processes received exactly the same input bytes. Each ran its fixed correctness checks, six warmups and 36 measured calls. All source, thresholds, seeds, runtime identities and resource limits were published and independently checked before execution.

## What happened

All six primary cells passed: each had a median paired F/L ratio at most 0.90 and at least five strict wins in six pairs. Ratios of 0.7411–0.8048 mean about 20–26% lower paired median query time on these large cases. The 1,000-drone case did not meet the improvement rule in any process. Four of the 36 large-case pairs were slower with F; every one remains in the analysis.

| Drones / seed | Process | L median (ms) | F median (ms) | Median paired F/L | Strict F wins | Fixed cell rule |
|---|---|---:|---:|---:|---:|---|
| 1,000 / 261701 | p0 | 44.80 | 50.55 | 1.1381 | 2/6 | Missed (contextual) |
| 5,000 / 261702 | p0 | 502.80 | 377.65 | 0.7596 | 6/6 | Met |
| 5,000 / 261703 | p0 | 507.50 | 395.80 | 0.8048 | 5/6 | Met |
| 1,000 / 261701 | p1 | 38.80 | 40.75 | 0.9922 | 3/6 | Missed (contextual) |
| 5,000 / 261702 | p1 | 528.15 | 392.50 | 0.7473 | 5/6 | Met |
| 5,000 / 261703 | p1 | 512.55 | 396.30 | 0.7718 | 5/6 | Met |
| 1,000 / 261701 | p2 | 44.15 | 40.15 | 0.9960 | 4/6 | Missed (contextual) |
| 5,000 / 261702 | p2 | 507.35 | 366.15 | 0.7411 | 6/6 | Met |
| 5,000 / 261703 | p2 | 528.60 | 378.55 | 0.7426 | 5/6 | Met |

Paired ratios compare F and L within each of the six fixed blocks. The ratio of the separately displayed medians is a different statistic. These ranges and repetitions do not constitute population confidence intervals. Three processes on one machine are not three devices, and two large input states are not 36 independent swarm trials. The strict-win rule retains exact recorded comparisons, including timer-scale differences in the small case; there was no adaptive resampling.

The independent saved-file audit passed **57,572 named check groups**, with no failed groups. It independently reconstructed the declared geometry and numerical reference, checked complete saved arrays, audited omitted-pair classifications, and checked cross-process output equality. In-browser full comparisons also checked timed transient outputs, which were not all independently persisted. That distinction is retained.

All 144 scientific controls, 168 adapter assertions, 18 ownership builds, 18 qualification builds/solves and 126 query calls are recorded. The 126 calls include 18 warmups and 108 measured queries. Conditional control solves have their separate admitted/descending policy. Generation, all three browser slots, the candidate supervisor, the saved reviewer and the final metadata seal closed successfully. The final authority is [qualification.json](results/qualification.json).

## What this means

Retain F as a candidate implementation for this named workload. The query still took **366–396 ms per large-case median**. Those times exclude flight steering/integration, rendering, loading, serialization, compression, transport and later validation. They do not show a live 5,000-drone frame rate. The implementation still enumerates 24,995,000 directed nonself pairs per 5,000-drone query; no asymptotic improvement is claimed.

The recorded [Three.js viewer](viewer/) shows all 26 actual frames of each new flight and all three process timing tables. It offers no fastest-process shortcut. Final-pose colors are model predictions from the separately qualified load calculation, with no claim of measured thrust or aerodynamic feedback during the flight.

Physical predictive accuracy and novelty remain unresolved. We have verified a finite numerical/runtime property of the specified model, not the model's validity for real interacting 27 g drones. The closed fixed-PWM admission and prior GPU wake failure remain unchanged. Ordinary coordinate screening is not presented as a new scientific method.

## Execution and provenance

Source commit: `3a2b9e3ceca3798f56596617dc483c45a09a309c`; manifest SHA256 `2c16bfa246e3b06e8f7d10c3e24449e01f02fab6e0298e48c7358d479d20fbc7`. Runtime: pinned Chrome 155.0.8059.80, headless page JavaScript on the recorded Mac host. The transparent wrapper preserved the exact five inherited CJS source slices. Historical arithmetic-file exposure remains disclosed; this is confirmation of a known candidate, not an unexposed discovery.

Generation: 408.504 s, sampled group RSS 568,901,632 bytes. Candidate campaign: 96.275 s, sampled owned browser-tree sum 1,487,011,840 bytes and controller 320,126,976 bytes. Saved review: 30.806 s, sampled group RSS 228,802,560 bytes. Total supervised science: 535.585 s, within the fixed 4,500 s allocation. Metadata seal: 0.323 s, within its separate 20 s allocation. Sampled RSS sums can double-count shared pages and miss spikes; they are not peak-memory guarantees. Stage and overlapping detailed transport totals must not be summed as disjoint work.

Read [the fixed protocol](PROTOCOL.md), [full timing analysis](results/analysis.json), [claim ledger](RESULT-CLAIM-LEDGER.md), [next decision](NEXT-DECISION.md), [restart record](POSTRUN-RESTART.md) and [inherited research sources](LITERATURE-EXPERIMENT-LEDGER.md). No new literature priority claim is made.
