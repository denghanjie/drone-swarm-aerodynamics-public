# QA — checkpoints 19–21

The flow under test is: open a milestone → choose a saved comparison → play or jump to its outcome/contact moment → see corresponding 3D trajectories and recorded statistics.

## Environment and scope

Loopback server: http://127.0.0.1:8875/outputs/research-results.html. Used the available unified computer-use in-app browser and supported locators/accessibility snapshots. A separate Browser skill was not listed; no external browser or browser dependency installation was used. Desktop 1440×1100; mobile 390×844. These are saved Three.js replays, not a live browser physics benchmark.

## Verified interactions

|Check|Evidence|
|---|---|
|Checkpoint 19 comparison|Seed 905 outcome: previous controller 50/50; soft candidate 26/50, largest group 36/50. Two 3D scenes rendered.|
|Checkpoint 20 treatment selection|Select 1004/both changes, then outcome: soft reference 25/50 vs combined 44/50, largest groups 30/50 vs 37/50.|
|Checkpoint 21 retained failure|Select 1103, Contact moment: clock 10.1725 s internally, right panel stops, closest pair gets red wire markers, left remains a running trajectory.|
|Checkpoint 21 successful course|Select 1101/slalom/100 ms, jump 25 s then Play: clock advances to 25.3 s, button becomes Pause, stats update; Contact moment disabled because neither run stops.|
|Mobile layout|390 px document width on 390 px viewport; both scene panes 356×350 px; controls wrap without horizontal overflow.|
|Console/overlay|No relevant errors or warnings in the inspected milestone pages; no runtime/framework overlay.|
|Screenshot review|Saved 19/20 desktop, 21 contact desktop and mobile screenshots inspected.|

## Numerical and artifact verification

Solver checks, unchanged-controller checks, local-neighbor/order checks and delay-buffer checks passed. Frozen source hashes, unique case counts, finite final states, crossing counts and exact replay endpoints were checked separately from scientific criteria. Two regenerated failure-audit replays match earlier final states and metrics exactly.

The new filter variants fail most trajectory-refinement criteria; those failures are preserved and reported. The delay contact case can pass numerical refinement while failing the mission. Neither result is relabeled as a software success proving safety.

The pre-block 447-file manifest was verified before updating the main reports. Source and result integrity for the new block is recorded in the milestone artifact-check files; the final manifest covers the completed output tree.

## Remaining limits

Only the in-app browser and the two specified sizes were tested. The contact geometry is a conservative distance envelope. Delayed high-level observation is idealized; low-level stabilization has current exact own state. Airflow, flight-data accuracy, multi-wake force validation and actual Boids GPU scaling are outside these checks. External dataset retrieval failed, while the paper and a newer preprint were accessible through web search.

## Evidence

- [Checkpoint 19](milestone-19-preview.png)
- [Checkpoint 20](milestone-20-preview.png)
- [Contact moment](milestone-21-contact-preview.png)
- [Mobile](milestone-21-mobile-preview.png)
- [Consolidated current viewer](research-block-19-21-preview.png)

Final dashboard check: the main URL/title loaded checkpoint21, Contact moment showed the retained1103 stop and red pair markers, and the console remained clean. All21 new JavaScript files passed syntax checks; checked local page/report links resolved;81 numerical executions are accounted for. See[artifact verification](research-block-19-21-artifact-checks.json).
