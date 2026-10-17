# Milestone: the browser calculation passed two fresh flock states

The numerical agreement carried over to two new, prospectively selected 64-drone runs. Both flocks reached 5 seconds, changed their relative formation, and produced states distinct from the six earlier inputs. Each final state had 228 positive rotor/source interactions under the reference model.

Both browser implementations passed all four error categories on both states: **4 of 4 target calls qualified**. The fixed error limit stayed 1e-8. The largest normalized error upper bound was approximately 2.65e-16; this describes numerical disagreement with the specified model, not physical prediction error. All eight moving-control calls produced their expected results, 14 arithmetic checks passed, and all four deliberate corruptions were detected.

The new browser execution also completed its shutdown checks: the recorded Chrome root and controller exited successfully, then the retained guardian was released without a group signal. The earlier failed experiment remains failed and preserved.

**What this changes:** we now have fresh-state evidence that the browser's screened (F) and lean baseline (L) calculations agree with the independent numerical reference. That is a firmer starting point for larger numerical and physical-evidence tests.

**What remains open:** the flight recordings used local 3D Boids with shared route guidance and airflow off. Aerodynamic loads were calculated afterwards. These two runs establish neither physical accuracy nor speed, coupled flight, 5,000-drone feasibility or novelty.

[Watch the recorded 3D runs](viewer/) · [Saved numerical summary](SAVED-SUMMARY.json) · [Fixed protocol](PROTOCOL.md) · [Exact raw results](results/check.json) · [Restart record](RESTART-RESULT.md)

[Next research decision](../m31-next-direction-2026-10-17/ADOPTED-DECISION.md): avoid repeating the earlier large-swarm speed test; pursue scalable independent checking and admission of compatible measured data.
