# Milestone 29 — corrected aerodynamic computation cost

Generated: 2026-10-12T01:54:54+00:00 (UTC).

**Status: complete.**

This study measures the actual local-flocking, rigid-body, contact and corrected airflow pipeline for one simulated second. It is run serially after the long mission studies have ended. Three timing repeats use the same initial scene; they are not independent mission trials. Rendering is separate.

|Drones|Model|Runs|Full windows|Median total wall s|Median airflow s|Median steering s|Median physics s|Median safety s|Median measurement s|
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
|50|off|3|3|0.77200|0.00000|0.30757|0.32227|0.08725|0.05215|
|50|sum-force|3|3|1.22613|0.35759|0.31810|0.39232|0.10297|0.05149|
|50|sum-rotor|3|3|1.44479|0.42167|0.37214|0.46745|0.12097|0.05770|
|50|rss-rotor|3|3|1.19578|0.36917|0.30387|0.36329|0.09335|0.04426|
|200|off|3|3|2.96640|0.00000|1.44923|0.99431|0.29216|0.22356|
|200|sum-force|3|3|4.89564|2.18664|1.20730|1.02270|0.25161|0.17439|
|200|sum-rotor|3|3|4.55963|2.06170|1.12813|0.96245|0.23910|0.16538|
|200|rss-rotor|3|0|no full window|no full window|no full window|no full window|no full window|no full window|
|1000|off|3|3|8.99383|0.00000|5.21147|2.41765|0.79134|0.58269|
|1000|sum-force|3|3|23.00918|13.23312|5.32658|3.02248|0.82902|0.59325|
|1000|sum-rotor|3|0|no full window|no full window|no full window|no full window|no full window|no full window|
|1000|rss-rotor|3|0|no full window|no full window|no full window|no full window|no full window|no full window|
|5000|off|3|3|133.94278|0.00000|87.20465|27.04419|9.03611|10.63281|
|5000|sum-force|3|3|297.44129|192.91693|63.55863|26.85353|7.33691|6.74696|
|5000|sum-rotor|3|0|no full window|no full window|no full window|no full window|no full window|no full window|
|5000|rss-rotor|3|0|no full window|no full window|no full window|no full window|no full window|no full window|

## Repeat variation

Three repetitions of one scene describe runtime variation, not independent mission reliability. Full-window values below are listed in repeat order. Differences can reflect operating-system load, thermal state and partially warmed JIT execution.

|Drones|Model|Full-window wall seconds, each repeat|
|---:|---|---|
|50|off|0.41787, 1.29565, 0.77200|
|50|sum-force|1.71664, 1.01305, 1.22613|
|50|sum-rotor|1.44479, 1.10413, 2.10997|
|50|rss-rotor|0.97355, 1.19578, 1.19772|
|200|off|2.96640, 4.53756, 2.86273|
|200|sum-force|4.89564, 4.01692, 4.90678|
|200|sum-rotor|4.55963, 4.25862, 10.18950|
|200|rss-rotor|no completed full windows|
|1000|off|12.11278, 8.82821, 8.99383|
|1000|sum-force|33.72531, 23.00918, 20.48870|
|1000|sum-rotor|no completed full windows|
|1000|rss-rotor|no completed full windows|
|5000|off|47.24112, 133.94278, 208.67997|
|5000|sum-force|128.81115, 297.44129, 477.18324|
|5000|sum-rotor|no completed full windows|
|5000|rss-rotor|no completed full windows|

## Early stops and missing full windows

|Case|Simulated end s|Stop|Measured work wall s|
|---|---:|---|---:|
|cost-200-rss-rotor-1|0.80000|aerodynamic model domain|3.24803|
|cost-200-rss-rotor-2|0.80000|aerodynamic model domain|3.48592|
|cost-200-rss-rotor-3|0.80000|aerodynamic model domain|6.41708|
|cost-1000-sum-rotor-1|0.49000|aerodynamic model domain|14.91321|
|cost-1000-rss-rotor-1|0.49000|aerodynamic model domain|14.65723|
|cost-1000-sum-rotor-2|0.49000|aerodynamic model domain|11.12810|
|cost-1000-rss-rotor-2|0.49000|aerodynamic model domain|11.43074|
|cost-1000-sum-rotor-3|0.49000|aerodynamic model domain|10.99338|
|cost-1000-rss-rotor-3|0.49000|aerodynamic model domain|10.61553|
|cost-5000-sum-rotor-1|0.24000|aerodynamic model domain|39.85184|
|cost-5000-rss-rotor-1|0.54000|aerodynamic model domain|187.83873|
|cost-5000-sum-rotor-2|0.24000|aerodynamic model domain|97.46707|
|cost-5000-rss-rotor-2|0.54000|aerodynamic model domain|215.38945|
|cost-5000-sum-rotor-3|0.24000|aerodynamic model domain|122.70112|
|cost-5000-rss-rotor-3|0.54000|aerodynamic model domain|296.04879|

Shorter stopped windows are incomplete workloads, not speedup evidence.

## Interpretation

Each child gets a short development warmup, excluded from timing. Startup, module loading and final serialization are excluded. In-memory recording and scientific measurement are included. Background operating-system load and thermal state remain uncontrolled. An [opportunistic host-load observation](milestone-29-host-load-observations.json) provides context but cannot identify the cause of timing variation. Model order rotates over repeats. Raw individual times and stop reasons remain in the results.

This is a one-second startup-window cost comparison, before the first wall. It does not measure crowded doorway cost, completed missions, aerodynamic accuracy, GPU execution or live browser physics. The Three.js page replays the recorded windows. Different recording and timestep settings from milestone25 preclude a direct optimization-speedup claim.

Force-only and rotor-moment models use the corrected opposite-motor wake length. Their assumptions remain exploratory; faster computation does not imply adequate physical fidelity.

Saved 48/48 prescribed runs.

[3D replay](milestone-29-lab.html) · [Runtime environment](milestone-29-runtime.json) · [Protocol](milestone-29-protocol.json) · [Raw results](milestone-29-progress.json) · [Corrected mission study](milestone-28-report.md) · [Earlier rendering measurements](milestone-25-rendering.json).
