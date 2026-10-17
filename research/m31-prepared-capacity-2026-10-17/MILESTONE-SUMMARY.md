# Milestone: exact reference checks at 180 drones

**The fixed test passed both accuracy and the predeclared practical hurdle.** The unchanged prepared reference reproduced the complete saved root and signed-load bounds for a dense and a sparse 180-drone scene. Its 64-drone control also reproduced its complete earlier record. This is progress toward affordable numerical verification; it does not demonstrate a real-time 5,000-drone simulation.

Think of this reference as the careful measuring instrument against which a faster simulation will be checked. We tested whether that instrument still gives the same answers at its current permitted size, and recorded where its work goes. We changed neither the aerodynamic model nor its numerical precision.

| Fixed input | Drones | Scalar pair checks | Positive interactions | Profiled calculation |
|---|---:|---:|---:|---:|
| Saved Boids state A | 64 | 7,408 | 228 | 2.517 s |
| Dense static group | 180 | 34,707 | 3,056 | 12.317 s |
| Sparse static group | 180 | 3,340 | 0 | 1.754 s |

All three calculations ran once in this prescribed order, with profiling enabled. These are observations of that instrumented run, not average timings, a speed comparison, or browser frame times. The dense and sparse groups are regular upright grids; the 64-drone state comes from a previous local 3D Boids run with airflow off.

The driver recorded **127,139,840 bytes (about 121.3 MiB)** of process-lifetime peak resident memory through pre-index closure. This includes earlier cases and loaded evidence. It is not isolated memory per scene or an operating-system memory limit. The predefined practical hurdle was at most 60 seconds per profiled calculation and at most 1 GiB lifetime peak RSS; all passed. The driver wall observation was 16.956 seconds through closure before final index serialization and stdout.

## What the accuracy result covers

For both 180-drone cases, every saved raw input word, prepared drone operand and complete independently saved root/load interval matched exactly by stable ID. Rotor order and signed force/moment components are preserved. The complete positive interaction support agrees with both older producer methods. New 192-bit coefficient intervals fit exactly within the older saved 96-bit bounds. The older independent files do not contain 192-bit pair coefficients, so equality to an independent pair table at that precision is unavailable; it is not claimed.

The three calls performed 45,455 scalar checks while preserving coverage of 273,888 logical pairs. They prepared each of the 424 scene rows once; no preparation was repeated inside pair calculations. All 767 frozen source pins and saved outputs were preserved at closure. No new full-oracle, native-browser, flight, control rerun or physical experiment was performed. The earlier 24-case qualification and controlled failure tests remain prior evidence.

Evidence: [raw terminal index](results/index.json), [prospective protocol](PROTOCOL.md), [source review](review/STATIC-REVIEW.md), and [implementation/observation boundaries](source/DESIGN.md). The [profile interpretation](review/PROFILE-INTERPRETATION.md) explains the retained work and timing boundaries. The [new Three.js view](viewer/) passed 81 UI checks across 48 fixed selections, with desktop/mobile inspection. The separately allocated [independent saved-data audit](review/SAVED-RESULT-REVIEW.md) passed: all three records, 767 local and committed source pins, complete saved coverage accounting and the practical hurdle were verified without rerunning the science.

## What remains unresolved

This makes exact verification at these fixed sizes feasible within the chosen offline budget. It does not establish accuracy on unseen large flocks, dynamic coupling, physical fidelity or a useful browser rate. Dense and sparse groups have very different work at the same drone count. Extrapolating these three observations to 5,000 would be unjustified.

The next scale proposal must budget actual positive interactions, unresolved scalar checks, exact roots and saved output size on its intended states. The present cap remains 180; this pass does not authorize an automatic increase or another optimization. Physical evidence remains a separate track: the [literature decision](../m31-next-evidence-decision-2026-10-17/literature/EVIDENCE-TABLE.md) identifies promising measured interaction data, but no calibrated physical benchmark has yet been admitted.

## Physical scope clarified

A separate [review of retained primary research and model source](../m31-physical-compatibility-2026-10-17/NOTE.md) found that the model can represent lower-drone thrust loss and offset moments, but omits upright upper-drone interaction effects and velocity/history dependence at fixed inputs. Published experiments report these effects. This limits any general mutual or dynamic aerodynamics claim; an admitted-domain numerical falsification still requires matched spacing, geometry, actuation and uncertainty. The next physical question is whether upper-drone thrust or pitch changes measurably in an arrangement admitted by this model, which predicts exactly no upper interaction response. No physical score or new experiment was generated by that review.
