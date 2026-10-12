# Checkpoint 21 — a 100 ms observation delay exposes a contact failure

The unchanged reference controller can pass the tested courses under ideal observation, but a new starting flock reaches the drone-to-drone contact limit when high-level observations are 100 ms old. This is evidence against treating the controller as robust to that delay.

## Experiment

Four fresh seeds(1101–1104), two courses(tight staggered openings and a three-obstacle slalom), three observation delays(0/50/100 ms):24 primary runs at 2.5 ms. Eight refinements at 1.25 ms were selected before outcomes were known. After the first contact stop we added a separately documented four-run audit: exact replays and refinements of the failed case and its ideal counterpart. Total 36 numerical executions; two are exact replay regenerations, not additional independent cases.

The controller is the frozen checkpoint 18 inward-guidance/local Boids controller. High-level steering sees a coherent delayed snapshot of self and neighbors. At startup it holds the initial snapshot until delayed data is available. Low-level stabilization still uses exact current own state. Contact detection always uses true current geometry. This models high-level observation lag, not a calibrated radio system: no noise, packet loss, asynchronous clocks, wake forces or uncertain onboard stabilization are included.

## Fresh primary outcomes

|Course|Delay(ms)|Runs finishing 50/50|Contact-stop runs|Total individual passages|Worst sampled largest group|Final disconnected runs|
|---|---:|---:|---:|---:|---:|---:|
|tight|0|4/4|0|200/200|49/50|0|
|tight|50|4/4|0|200/200|49/50|0|
|tight|100|3/4|1|150/200|49/50|0|
|slalom|0|4/4|0|200/200|50/50|0|
|slalom|50|4/4|0|200/200|50/50|0|
|slalom|100|4/4|0|200/200|50/50|0|

These are small matched deterministic samples. Drones within one flock are not independent trials. A stopped run is terminated for all drones; unfinished counts after a stop are not 50 individually observed collisions. Connectivity is measured at the unchanged 1.8 m radius; a connected group can still reach the contact limit.

|Seed|Course|0 ms outcome|50 ms outcome|100 ms outcome|
|---|---|---|---|---|
|1101|tight|50/50; no stop|50/50; no stop|50/50; no stop|
|1101|slalom|50/50; no stop|50/50; no stop|50/50; no stop|
|1102|tight|50/50; no stop|50/50; no stop|50/50; no stop|
|1102|slalom|50/50; no stop|50/50; no stop|50/50; no stop|
|1103|tight|50/50; no stop|50/50; no stop|0/50; stop 10.1725 s|
|1103|slalom|50/50; no stop|50/50; no stop|50/50; no stop|
|1104|tight|50/50; no stop|50/50; no stop|50/50; no stop|
|1104|slalom|50/50; no stop|50/50; no stop|50/50; no stop|

## Numerical checks

|Seed|Controller / scenario|Step pair(ms)|Maximum final position difference(m)|Finish counts|Pass 1 cm test|
|---|---|---|---:|---|---|
|1101|slalom / delay 0 ms|2.5→1.25|3.3209601e-07|[50, 50]|Yes|
|1101|slalom / delay 50 ms|2.5→1.25|4.099631e-07|[50, 50]|Yes|
|1101|slalom / delay 100 ms|2.5→1.25|2.1935377e-07|[50, 50]|Yes|
|1101|tight / delay 0 ms|2.5→1.25|1.4789571e-05|[50, 50]|Yes|
|1101|tight / delay 50 ms|2.5→1.25|2.954793e-07|[50, 50]|Yes|
|1101|tight / delay 100 ms|2.5→1.25|2.0194226e-07|[50, 50]|Yes|
|1102|tight / delay 0 ms|2.5→1.25|1.3395016e-06|[50, 50]|Yes|
|1102|tight / delay 100 ms|2.5→1.25|1.8270301e-07|[50, 50]|Yes|
8/8 preregistered refinements pass the 1 cm endpoint, same-count/same-stop test. Failed comparisons remain failures; matching completion alone does not override them.

### Post-hoc contact audit

|Delay(ms)|End times at 2.5/1.25 ms|Finish counts|Final-position difference(m)|Numerical acceptance|Exact replay|
|---|---|---|---:|---|---|
|0|[60, 60]|[50, 50]|5.3921056e-07|True|True|
|100|[10.1725, 10.1725]|[0, 0]|5.3764465e-09|True|True|

At the original stop(10.1725 s), drones 20 and 47(zero-based IDs) are approximately 0.14974 m apart and closing at 0.222 m/s. This crosses the model's 0.15 m center-distance envelope. It is a conservative proximity failure, not a resolved rotor-contact simulation. The separate [diagnostic](milestone-21-contact-diagnostic.json) retains positions, actual velocities and last requested velocities. The replay marks the closest pair in red.

## Decision

Keep the reference as an experimental baseline, not a demonstrated delay-robust controller. Study a local delay-compensated avoidance/arrival rule next, retaining this failure and checking on new seeds before adoption. Do not use additional integration refinement to conceal an observation-model failure. Physical validation, airflow coupling, actual flock GPU scaling and scientific novelty remain open.

[3D replay](milestone-21-lab.html) · [Frozen protocol](milestone-21-protocol.json) · [Full records](milestone-21-study.json) · [Post-hoc audit protocol](milestone-21-failure-audit-protocol.json) · [Audit final states](milestone-21-failure-audit-runs.json) · [Delay implementation checks](milestone-21-delay-checks.json).
