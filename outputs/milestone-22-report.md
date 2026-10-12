# Milestone 22 — Local prediction development

## Research question

Can position extrapolation recover the retained 100 ms delay failure, and what happens at 200 ms?

## Method

Each drone selects neighbors inside 1.8 m using the delayed measurement, then estimates positions as measured position + measured velocity × measurement age. No unseen drone is added by prediction. Velocities are held constant. Both self and neighbor positions are predicted; only low-level stabilization receives current self state. The original local Boids, inward guidance, sequential velocity filter and rigid-body physics remain unchanged. Airflow, noise and dropped observations are off. The map and route preferences are given. No central passage schedule is used.

16 runs: three development seeds, with an additional 200 ms stress on 1103; every case at 2.5 and 1.25 ms.

## Results

|Seed|Course|Delay ms|Observer|Finished|Stop time/reason|Minimum pair distance m|Minimum obstacle clearance m|Minimum connected /50|Final connected /50|
|---|---|---:|---|---:|---|---:|---:|---:|---:|
|1101|tight|100|predict|50/50|none|0.31616|0.17465|50|50|
|1101|tight|100|raw|50/50|none|0.23201|0.16107|50|50|
|1103|tight|100|predict|50/50|none|0.23151|0.13034|49|50|
|1103|tight|100|raw|0/50|10.1725: contact envelope reached|0.14974|0.18190|50|50|
|1103|tight|200|predict|0/50|10.6275: contact envelope reached|0.14920|0.18673|50|50|
|1103|tight|200|raw|50/50|none|0.20616|0.10747|50|50|
|1104|tight|100|predict|50/50|none|0.28768|0.14679|49|50|
|1104|tight|100|raw|50/50|none|0.24147|0.16036|50|50|

One whole run stops when any contact/model limit is reached. Unfinished drones are not independent collisions. Pair distance uses a conservative 15 cm center envelope, not resolved rotor geometry. Connectivity is sampled every 0.1 s using actual positions and a 1.8 m link distance. Completion and connectedness are separate outcomes.

## Numerical checks

7/8 planned 2.5→1.25 ms comparisons pass. Acceptance requires identical finish count and stop reason, end-time difference below 0.01 s, and maximum final position difference below 0.01 m.

|Seed|Course|Observer|Delay ms|Maximum final difference m|Counts|Pass|
|---|---|---|---:|---:|---|---|
|1101|tight|predict|100|2.1575406e-06|[50, 50]|True|
|1101|tight|raw|100|2.0194226e-07|[50, 50]|True|
|1103|tight|predict|100|0.54854613|[50, 50]|False|
|1103|tight|raw|100|5.3764465e-09|[0, 0]|True|
|1103|tight|predict|200|0.0010708361|[0, 0]|True|
|1103|tight|raw|200|3.0099466e-05|[50, 50]|True|
|1104|tight|predict|100|1.5650491e-05|[50, 50]|True|
|1104|tight|raw|100|3.478902e-07|[50, 50]|True|

## Conclusion

Prediction recovers completion for the saved 100 ms failure at both steps, but the recovered trajectory fails our numerical criterion (0.548546 m final difference). At 200 ms, prediction causes contact while the original finishes at both steps. Delay effects are not monotonic in this nonlinear flock controller. Constant-velocity prediction is therefore not a validated replacement.

The six observer implementation checks pass, including local visibility, immutability, zero-delay equivalence and exact raw-command/trajectory regressions. Those checks establish implementation behavior, not safe flocking.

## Separate post-hoc finer-step audit

The 1.25→0.625 ms comparison for 1103/predict/100 ms has maximum final position difference 2.8848685e-08 m; finish counts[50, 50]; pass=True. This extra run was specified after inspecting the failed planned comparison. It does not replace or erase that failure. See the separate audit protocol and saved trajectory.

## Records and reproduction

[Three.js replay](milestone-22-lab.html) · [Protocol](milestone-22-protocol.json) · [All metrics](milestone-22-summary.json) · [Full study states](milestone-22-study.json) · [Numerical checks](milestone-22-comparisons.json). Each individual run and its failure snapshot is saved in`milestone-22-source/`. The viewer replays 2.5 ms trajectories, not live browser physics.

Run `python3 research-reproduce.py --stage 22 --node /path/to/node` from the outputs directory to verify hashes and rerun in an isolated copy.

## Saved trajectory divergence

The 2.5 ms versus 0.625 ms saved-frame comparison first exceeds 1 cm at 27.3 s and 0.1 m at 29.3 s; peak difference 0.5523 m at 58.3 s. This locates divergence without identifying its causal controller branch. [Trace](milestone-22-refinement-trace.json).
