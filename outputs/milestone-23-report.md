# Milestone 23 — Frozen prediction evaluation on fresh flocks

## Research question

How does the unchanged local predictor behave on six previously unused flocks in two known courses at 100 ms delay?

## Method

Each drone selects neighbors inside 1.8 m using the delayed measurement, then estimates positions as measured position + measured velocity × measurement age. No unseen drone is added by prediction. Velocities are held constant. Both self and neighbor positions are predicted; only low-level stabilization receives current self state. The original local Boids, inward guidance, sequential velocity filter and rigid-body physics remain unchanged. Airflow, noise and dropped observations are off. The map and route preferences are given. No central passage schedule is used.

38 runs: 24 primary runs at 2.5 ms, plus 14 predefined 1.25 ms refinements (all 12 predicted cases and both raw 1201 courses). No tuning after development; the candidate was not promoted because of the retained development failures.

## Results

|Seed|Course|Delay ms|Observer|Finished|Stop time/reason|Minimum pair distance m|Minimum obstacle clearance m|Minimum connected /50|Final connected /50|
|---|---|---:|---|---:|---|---:|---:|---:|---:|
|1201|tight|100|predict|50/50|none|0.32209|0.13232|50|50|
|1201|slalom|100|predict|50/50|none|0.48656|0.63377|50|50|
|1201|tight|100|raw|50/50|none|0.27646|0.13670|50|50|
|1201|slalom|100|raw|50/50|none|0.48001|0.66294|50|50|
|1202|tight|100|predict|0/50|11.0275: contact envelope reached|0.14994|0.17626|50|50|
|1202|slalom|100|predict|50/50|none|0.46117|0.61474|50|50|
|1202|tight|100|raw|50/50|none|0.19656|0.17505|50|50|
|1202|slalom|100|raw|50/50|none|0.44487|0.64988|50|50|
|1203|tight|100|predict|50/50|none|0.26488|0.16618|50|50|
|1203|slalom|100|predict|50/50|none|0.47253|0.61886|50|50|
|1203|tight|100|raw|7/50|22.0025: contact envelope reached|0.14978|0.17492|50|50|
|1203|slalom|100|raw|50/50|none|0.46605|0.63588|50|50|
|1204|tight|100|predict|50/50|none|0.35504|0.15928|50|50|
|1204|slalom|100|predict|50/50|none|0.48446|0.57310|50|50|
|1204|tight|100|raw|50/50|none|0.33362|0.16536|50|50|
|1204|slalom|100|raw|50/50|none|0.47507|0.65493|50|50|
|1205|tight|100|predict|50/50|none|0.32304|0.15585|50|50|
|1205|slalom|100|predict|50/50|none|0.46614|0.61420|50|50|
|1205|tight|100|raw|50/50|none|0.25989|0.17502|50|50|
|1205|slalom|100|raw|50/50|none|0.44920|0.63501|50|50|
|1206|tight|100|predict|50/50|none|0.31910|0.17459|50|50|
|1206|slalom|100|predict|50/50|none|0.47970|0.65639|50|50|
|1206|tight|100|raw|50/50|none|0.26027|0.13900|49|50|
|1206|slalom|100|raw|50/50|none|0.43170|0.68506|50|50|

One whole run stops when any contact/model limit is reached. Unfinished drones are not independent collisions. Pair distance uses a conservative 15 cm center envelope, not resolved rotor geometry. Connectivity is sampled every 0.1 s using actual positions and a 1.8 m link distance. Completion and connectedness are separate outcomes.

## Numerical checks

13/14 planned 2.5→1.25 ms comparisons pass. Acceptance requires identical finish count and stop reason, end-time difference below 0.01 s, and maximum final position difference below 0.01 m.

|Seed|Course|Observer|Delay ms|Maximum final difference m|Counts|Pass|
|---|---|---|---:|---:|---|---|
|1201|tight|predict|100|0.40097661|[50, 50]|False|
|1201|slalom|predict|100|1.1205456e-06|[50, 50]|True|
|1201|tight|raw|100|2.196343e-07|[50, 50]|True|
|1201|slalom|raw|100|5.0419392e-07|[50, 50]|True|
|1202|tight|predict|100|5.5778178e-09|[0, 0]|True|
|1202|slalom|predict|100|1.5050738e-07|[50, 50]|True|
|1203|tight|predict|100|2.4652152e-06|[50, 50]|True|
|1203|slalom|predict|100|3.4737613e-07|[50, 50]|True|
|1204|tight|predict|100|4.277538e-06|[50, 50]|True|
|1204|slalom|predict|100|1.0182888e-07|[50, 50]|True|
|1205|tight|predict|100|4.4187091e-06|[50, 50]|True|
|1205|slalom|predict|100|1.1757821e-06|[50, 50]|True|
|1206|tight|predict|100|3.4881397e-06|[50, 50]|True|
|1206|slalom|predict|100|7.1893576e-07|[50, 50]|True|

## Conclusion

raw: 11/12 complete 50-drone runs; 1 stopped runs. Minimum sampled connected group across these runs: 49/50.
predict: 11/12 complete 50-drone runs; 1 stopped runs. Minimum sampled connected group across these runs: 50/50.

These six seeds and two related courses are a small, deliberately specified evaluation. Drones within a flock are coupled;600 drone passages are not 600 independent safety trials. The earlier 200 ms counterexample and 100 ms numerical failure remain relevant even if fresh primary cases succeed. No broad superiority, real-flight safety or calibrated latency tolerance is established.

## Records and reproduction

[Three.js replay](milestone-23-lab.html) · [Protocol](milestone-23-protocol.json) · [All metrics](milestone-23-summary.json) · [Full study states](milestone-23-study.json) · [Numerical checks](milestone-23-comparisons.json). Each individual run and its failure snapshot is saved in`milestone-23-source/`. The viewer replays 2.5 ms trajectories, not live browser physics.

Run `python3 research-reproduce.py --stage 23 --node /path/to/node` from the outputs directory to verify hashes and rerun in an isolated copy.

## Separate post-hoc raw-failure audits

1 additional runs selected after the primary study;1/1 comparisons pass. See [selection protocol](milestone-23-failure-audit-protocol.json), [comparisons](milestone-23-failure-audit.json) and [full audit states](milestone-23-failure-audit-runs.json). These are not part of the 14 predefined refinements.
