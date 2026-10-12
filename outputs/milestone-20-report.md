# Checkpoint 20 — stronger guidance and fixed heading do not solve passage

We tested two specific explanations for the failed soft filter: weak sideways guidance within an opening, and large heading changes near zero speed. A 2×2 comparison includes the unchanged soft reference from 19 plus three new combinations. The new 27 runs cover the same three development seeds at 5, 2.5, 1.25 ms. No new seed was used for tuning.

Center guidance replaces the zero lateral preference inside the target aperture with a preference toward its center, capped at the same lateral speed. The same centering error also feeds the existing forward-speed reduction, so this treatment changes lateral attraction and forward slowing together; it is not a pure lateral-gain ablation. Fixed heading holds the world yaw target at 0 while retaining 3D translation. Each drone still uses local separation, alignment and cohesion. No passage slots, global flock center or global connectivity constraint were added. The comparison changes known-map guidance, not route discovery.

## Results

- soft-fixedyaw: 77/150 completed at 5 ms.
- soft-center: 126/150 completed at 5 ms.
- soft-center-fixedyaw: 128/150 completed at 5 ms.

The old soft reference completed 84/150, and the prior interior controller completed 150/150 in 19. 1/18 new adjacent-step comparisons passed the 1 cm criterion. Contact stops across the 27 new runs: 0.

|Seed|Controller|Step(ms)|Finished|Contact stop|Smallest connected group|Final connected group|
|---|---|---:|---:|---|---:|---:|
|905|soft-center|5|42/50|None|32/50|32/50|
|905|soft-center|2.5|41/50|None|31/50|31/50|
|905|soft-center|1.25|42/50|None|40/50|40/50|
|905|soft-center-fixedyaw|5|42/50|None|37/50|37/50|
|905|soft-center-fixedyaw|2.5|44/50|None|37/50|37/50|
|905|soft-center-fixedyaw|1.25|45/50|None|37/50|37/50|
|905|soft-fixedyaw|5|21/50|None|30/50|30/50|
|905|soft-fixedyaw|2.5|23/50|None|30/50|30/50|
|905|soft-fixedyaw|1.25|24/50|None|22/50|33/50|
|1002|soft-center|5|41/50|None|29/50|29/50|
|1002|soft-center|2.5|42/50|None|50/50|50/50|
|1002|soft-center|1.25|42/50|None|50/50|50/50|
|1002|soft-center-fixedyaw|5|42/50|None|50/50|50/50|
|1002|soft-center-fixedyaw|2.5|42/50|None|50/50|50/50|
|1002|soft-center-fixedyaw|1.25|42/50|None|50/50|50/50|
|1002|soft-fixedyaw|5|26/50|None|37/50|45/50|
|1002|soft-fixedyaw|2.5|26/50|None|45/50|45/50|
|1002|soft-fixedyaw|1.25|26/50|None|32/50|45/50|
|1004|soft-center|5|43/50|None|50/50|50/50|
|1004|soft-center|2.5|43/50|None|50/50|50/50|
|1004|soft-center|1.25|43/50|None|50/50|50/50|
|1004|soft-center-fixedyaw|5|44/50|None|37/50|37/50|
|1004|soft-center-fixedyaw|2.5|44/50|None|37/50|37/50|
|1004|soft-center-fixedyaw|1.25|44/50|None|37/50|37/50|
|1004|soft-fixedyaw|5|30/50|None|23/50|23/50|
|1004|soft-fixedyaw|2.5|31/50|None|23/50|27/50|
|1004|soft-fixedyaw|1.25|30/50|None|27/50|27/50|

## Numerical checks

|Seed|Controller / scenario|Step pair(ms)|Maximum final position difference(m)|Finish counts|Pass 1 cm test|
|---|---|---|---:|---|---|
|905|soft-center|5→2.5|2.7595999|[42, 41]|No|
|905|soft-center|2.5→1.25|2.1392253|[41, 42]|No|
|905|soft-center-fixedyaw|5→2.5|3.8457525|[42, 44]|No|
|905|soft-center-fixedyaw|2.5→1.25|1.8128362|[44, 45]|No|
|905|soft-fixedyaw|5→2.5|6.5579227|[21, 23]|No|
|905|soft-fixedyaw|2.5→1.25|5.0195735|[23, 24]|No|
|1002|soft-center|5→2.5|4.4089234|[41, 42]|No|
|1002|soft-center|2.5→1.25|1.8883041|[42, 42]|No|
|1002|soft-center-fixedyaw|5→2.5|0.6607979|[42, 42]|No|
|1002|soft-center-fixedyaw|2.5→1.25|0.081901153|[42, 42]|No|
|1002|soft-fixedyaw|5→2.5|2.2970668|[26, 26]|No|
|1002|soft-fixedyaw|2.5→1.25|5.1282336|[26, 26]|No|
|1004|soft-center|5→2.5|0.066086896|[43, 43]|No|
|1004|soft-center|2.5→1.25|0.0038643179|[43, 43]|Yes|
|1004|soft-center-fixedyaw|5→2.5|0.87191087|[44, 44]|No|
|1004|soft-center-fixedyaw|2.5→1.25|0.12155937|[44, 44]|No|
|1004|soft-fixedyaw|5→2.5|5.1729341|[30, 31]|No|
|1004|soft-fixedyaw|2.5→1.25|4.4150537|[31, 30]|No|

## Decision

Do not promote any of these variants. Stronger map centering improves completion relative to the unsuccessful soft reference, but does not restore all-drone passage or consistent trajectories. Fixed heading does not resolve the sensitivity. This does not prove heading has no effect; it rules out treating this particular heading change as a sufficient fix.

The software checks verify exact reproduction of the unmodified soft controller, invariance to agent ordering within numerical precision, and no response to a far-away invisible drone. These are implementation checks, not successful research outcomes. The frozen optimization parameters and physical plant were unchanged. Timings in parallel execution are not a controlled speed benchmark.

[3D comparison](milestone-20-lab.html) · [Protocol](milestone-20-protocol.json) · [Full trial records](milestone-20-study.json) · [Software checks](milestone-20-control-checks.json). The viewer includes three exact reference replays from 19 plus nine new 5 ms replays. Run `build-replay.cjs` after the study to assemble them without rerunning simulations.
