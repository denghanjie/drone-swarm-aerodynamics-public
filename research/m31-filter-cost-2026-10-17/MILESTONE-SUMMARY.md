# The safe shortcut reduced total calculation time in this test

The filter passed the complete numerical checks and the speed rule declared before execution. In the three dense groups, median paired calculation time fell by about **32–38%**. Every one of the 24 measured pairs favoured filtering. All six groups retained the same scientific outputs, all load-error limits passed, and the independent checker detected all 18 deliberate corruption controls.

This is useful progress on computation. It is still far from our final objective: the filtered 180-drone dense group took a median **3.891 seconds** per calculation. We have not demonstrated real-time flight or a coupled 5,000-drone browser simulation.

## What changed

The existing spatial hierarchy already groups distant or irrelevant interactions so they can be skipped together. The added filter examines the interactions left over. When inexpensive interval arithmetic proves one is zero, it avoids the more expensive exact calculation. When the answer is uncertain, it uses the original exact calculation.

We measured the entire declared method call, including preparation, hierarchy, filtering, exact fallback, load calculation and accuracy certificate. The comparison therefore pays the new filter's setup and bookkeeping costs. Shared input-literal conversion, result serialization/hashing and file writes are outside that method boundary; conversion and serialization/hashing have separate saved timings. This is not total process wall time.

## Results

| Group | Hierarchy median | Filtered median | Median paired filtered / hierarchy | Filter wins |
|---|---:|---:|---:|---:|
| Dense 80 | 1.469 s | 0.855 s | 0.683 | 4 / 4 |
| Dense 120 | 3.168 s | 1.948 s | 0.621 | 4 / 4 |
| Dense 180 | 5.984 s | 3.891 s | 0.651 | 4 / 4 |
| Sparse 80 | 0.219 s | 0.192 s | 0.873 | 4 / 4 |
| Sparse 120 | 0.327 s | 0.265 s | 0.817 | 4 / 4 |
| Sparse 180 | 0.493 s | 0.448 s | 0.899 | 4 / 4 |

Lower ratios favour filtering. The primary rule required a median paired ratio <=0.90 and at least three wins in four pairs **at every dense size**. It passed. Sparse groups were declared contextual and were not pooled into this decision.

The paired ratio is calculated within each comparison, then its median is taken. It is not generally equal to the ratio of the two separately reported medians; the difference is noticeable for Dense 80. Both statistics and every individual pair are saved. These are descriptive observations from one fixed Node allocation on this machine, with a balanced call order; no population confidence interval, cross-machine performance or general speedup theorem is claimed.

## Why the result is credible within that scope

The reviewed source was committed, pushed and independently verified before execution: `fb9754529a4df7350410187123c5d443e463cdf0`, with 61 source pins. Exactly one warmup pair and four measured pairs ran for each of six fresh scenes, for 60 calls total. The scientific allocation was not retuned or repeated.

The independent checker reconstructed 422,560 logical interactions and validated 845,120 method outcomes, including skipped interactions, positive coefficients, complete load certificates and all four normalized 1e-8 error limits. All 60 trial digests/work records and the 80-event journal reconciled; there were zero checker errors. The 18 corruption controls included invented zero interactions, wrong branches, altered coefficients/loads and misleading timing/work records.

In one representative pass over the six groups, exact scalar calls fell from **72,271 to 24,380**. The filter proved 47,891 residual interactions zero, while both methods retained the same 5,880 positive terms. This count supports the observed work reduction; it is not a separate timing result or an estimate for arbitrary swarms. Even after filtering, combined assembly dominated the dense 180 group's mean time (3.775 s of 3.923 s). That stage includes multiple operations and does not isolate a primitive's causal cost.

## What we can conclude—and the next useful test

For these fixed upright static groups and this implementation, adding the verified zero filter preserved the declared numerical results and reduced measured method cost enough to pass the prospective decision rule. Published interval filtering already exists; this is evidence about its integration into our declared aerodynamic calculation, not a novel general algorithm.

The next useful gate is transfer toward the actual browser/moving-flock pipeline using fresh local 3D Boids states, while retaining uncertainty, model refusals and the same accuracy obligations. This result does not cover changing geometry, tilted/cyclic coupling, flight feedback or physical measurements. A smoother or faster animation cannot settle those questions. Real-world model validity and a defensible novelty comparison remain separate research work.

The updated Three.js view displays the six actual saved groups. Select a receiver and rotor: teal boxes show hierarchy skips; purple markers identify additional scalar-filter zeros; the timing table and every pair remain visible. It is explicitly a static evidence view. Earlier group views retain links to historical moving Boids recordings, with airflow off.

The kernel closed successfully in 100.454 seconds (1,251 memory samples; peak sampled group RSS 395,919,360 bytes). The checker closed in 121.359 seconds (1,522 samples; peak 176,898,048 bytes). These stage durations describe containment, not method speed. All scientific allocations are closed. Preserve the source, raw records, independent references and failures; future science requires a fresh protocol and public source gate.
