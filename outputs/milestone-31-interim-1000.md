# Milestone 31 — interim 1,000-drone comparison

This is an intermediate record. At this checkpoint, four of ten prescribed trials had completed; the large-flock missions and finer-step checks were still running or queued. It is not the final milestone conclusion.

|Starting case|Original controller|Wall-priority controller|
|---|---|---|
|Seed 2001, wide doors|Wall contact at 16.775 s; 0 finished|1,000 finished by 109.75 s; no contact through 180 s|
|Seed 2002, narrow doors|Wall contact at 9.995 s; 0 finished|1,000 finished by 149.77 s; no contact through 180 s|

Both corrected flocks remain connected at every recorded science sample. The wide case's minimum sampled center spacing is 0.37659 m; the narrow case's is 0.23496 m. The contact model uses a 0.15 m center-spacing envelope. These sampled minima are descriptive; the separate stepwise contact checks determine stopping events.

Both corrected runs have zero wall-request violations at the frozen 1e-7 m/s threshold. Pair-request violations still occur. The narrow case also reaches the repair's 512-iteration cap on five drone-control updates; its maximum returned wall deficit is approximately 1e-10 m/s. This is recorded as an unmet solver stop criterion, even though no wall-request violation or contact is detected. The planned finer-step check remains necessary.

The two within-case controller comparisons use identical starts. Wide versus narrow uses different seeds, so the 40.02 s difference in last-finish time does not isolate doorway width alone.

The 5,000-drone development run exactly reproduces milestone 30 at its 20-second checkpoint, including all 17 state components per drone. Its longer mission remains underway. All 793 historical source-tree artifacts still match the pre-milestone archive.

The simulator uses local 3D Boids and shared route guidance, ideal observations and no aerodynamic interaction. These results support simulated passage in the two cases; they do not establish measured physical accuracy, reliable large-flock navigation or algorithmic novelty.

[3D replay](milestone-31-lab.html) · [Frozen protocol](milestone-31-protocol.json) · [Checkpoint agreement](milestone-31-continuation-check.json) · [Source preservation](milestone-31-preservation-check.json) · [Final milestone report, pending](milestone-31-report.md).
