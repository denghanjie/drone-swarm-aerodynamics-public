# A faster calculation for the tested 5,000-drone states

We found a useful computational improvement. On both new 5,000-drone cases, the screen met the rule fixed before the experiment: at least 10% lower paired query time and at least five wins in six comparisons. Every checked model output was preserved. This is an engineering result; it is not a claim of a new aerodynamic law or a publishable breakthrough.

## What we changed

The existing calculation visits every ordered pair of drones. The new version first checks whether a pair is clearly too far apart to affect this model. For those pairs it skips a more expensive distance calculation. It still visits the pairs, uses current positions and retains the original calculation for nearby pairs. Invalid or too-wide position ranges use the unchanged calculation after paying the screen's preparation cost.

## What the measurements say

Three new local 3D Boids flights generated the inputs. Each lasted two simulated seconds with airflow off. At the final pose, we evaluated the coupled aerodynamic model separately. Six paired measured calls per method followed the saved warmups on the pinned Node runtime and Apple M4 host.

| Saved state | Original query median | Screened query median | Median paired F/L | Screen wins |
|---|---:|---:|---:|---:|
| 1,000 drones, seed261601 | 36.31 ms | 45.10 ms | 1.0402 | 2/6 |
| 5,000 drones, seed261602 | 478.95 ms | 369.35 ms | 0.7193 | 5/6 |
| 5,000 drones, seed261603 | 480.11 ms | 303.38 ms | 0.6608 | 6/6 |

The two larger cases therefore had approximately 28.1% and 33.9% lower median paired times. The paired ratio is computed within each matched block; it is not the ratio of the two separately reported medians. The smaller case did not benefit. One large-case pair also lost, and timing variability was substantial: all raw measurements, including those losses, remain in results/analysis.json. These six repeats share one process and are not six independent swarm trials.

All 48 controls, six ownership builds, six fresh qualification builds/solves and 42 complete query calls were retained. The independent Python/NumPy audit passed 18,458 named checks, including full symbol tensors, all omitted-pair symbols, sparse coefficients and complete loads/residuals. Its audit groups inspect arrays; the check count is not the number of scalar observations. Both supervised processes and the final metadata seal closed successfully.

## What this means for the research

The screen is worth retaining as a candidate implementation for further testing. It avoided roughly 20.65 million center norms in each large case, while still enumerating 24.995 million directed nonself pairs. The measured complete-query improvement is evidence; the lower operation count alone would not have been enough.

The remaining cost is still roughly 0.30–0.37 seconds per screened query by the separate medians. Timings exclude Boids steering, flight integration, rendering and transport. We have not demonstrated real-time coupled flight. The numerical agreement covers the fixed inputs and named runtime; it is not a proof for all inputs or JavaScript implementations. Physical validity and novelty remain unresolved.

The updated Three.js viewer replays the actual saved poses from this experiment. Colors at the final pose show model predictions; earlier poses have no integrated aerodynamic loads. It is a short recorded input demonstration, not evidence of mature flock behavior or successful aerodynamic flight through an obstacle course.

Source was frozen and published at 9404ce3d578636ea0ee69b54626b1b8e7c1a7057 and independently verified before execution. The full protocol, raw evidence, failed/source-review findings and independent reports are preserved. This experiment is closed; no thresholds, seeds or results will be repaired after observation.
