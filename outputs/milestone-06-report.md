# Milestone 6 — imperfect navigation information

## Goal
Test whether the passage schedules still work when their navigation information is biased or delayed. This is a robustness study within original Step 5, not original Step 6 (WebGPU).

## Method
150 runs: 2 fixed controllers × 3 opening widths (0.6, 1.2, 2.4 m) × 5 observation profiles × 5 deterministic seeds. Each run uses 50 drones, 0.6 m initial spacing, 0.5 m/s requested speed and a 60 s horizon. All 150 runs were recalculated; 30 ideal cases were checked against prior results. No controller parameters were adjusted in response to these results.

Profiles: ideal; fixed horizontal bias bounded by ±2 cm per axis; 0.10 s navigation delay; both; stress with ±5 cm per axis and 0.25 s delay. Each vehicle has an independent, fixed x/y offset from a separate seeded random stream. Profiles are illustrative, not measured sensor specifications. Controllers receive the same offsets and initial conditions in each paired comparison.

The navigation scheduler and velocity-reference calculation receive delayed state and biased position. The initial map supplied to the scheduler is exact. Low-level stabilization uses exact, current physical state. This does not model end-to-end communications latency, delayed actuation, drifting localization, wind or aerodynamic coupling. Delay uses a 10 ms observation buffer, held at the initial state during startup; integration refinements retain this observation interval.

True state determines every crossing, separation check and replay. Swept pair separation is measured along the straight segment between integration endpoints. Below 20 cm is a desired-spacing breach; below 15 cm stops the simulation as a contact-envelope event. Gate crossings require 7.5 cm center clearance. The opening is a virtual plane, with no wall impact response. Invalid crossings and unfinished queues remain in the results. Throughput always uses the planned 60 s denominator, including stopped runs.

## Results
The smaller-error profiles had no invalid crossings or sub-20 cm pairs in the tested cases. Delay reduced total flow-rule passages from 470 to 435 across 15 matched runs. Under the stronger stress profile, the flow rule had invalid crossings in 9/15 runs and sub-20 cm pairs in 4/15; the cautious rule had 10/15 and 5/15 respectively. No contact/model stops occurred. Neither rule is robust to this stress profile.

Total passages below sum 15 runs per row (maximum 750); these are descriptive counts, not independent-trial confidence estimates.

| Rule | Information | Cases | Total valid passages | Runs stopped | Runs below 20 cm | Runs with invalid crossings | Minimum distance |
|---|---|---:|---:|---:|---:|---:|---:|
| scheduled | ideal | 15 | 370 | 0 | 0 | 0 | 0.310 m |
| scheduled | bias | 15 | 370 | 0 | 0 | 0 | 0.274 m |
| scheduled | delay | 15 | 310 | 0 | 0 | 0 | 0.283 m |
| scheduled | combined | 15 | 310 | 0 | 0 | 0 | 0.247 m |
| scheduled | stress | 15 | 221 | 0 | 5 | 10 | 0.150 m |
| flow | ideal | 15 | 470 | 0 | 0 | 0 | 0.310 m |
| flow | bias | 15 | 470 | 0 | 0 | 0 | 0.274 m |
| flow | delay | 15 | 435 | 0 | 0 | 0 | 0.291 m |
| flow | combined | 15 | 435 | 0 | 0 | 0 | 0.256 m |
| flow | stress | 15 | 397 | 0 | 4 | 9 | 0.153 m |

## Numerical verification
- PASS: All 30 ideal cases reproduce previous metrics exactly.
- PASS: 100 ms delay selects exactly 10 controller ticks ago, cold-start held at initial state.
- PASS: Bias is reproducible and within per-axis bounds.
- PASS: Paired controllers share initial conditions and observation errors.
- PASS: 150 unique cases, finite metrics, complete replay endpoints.
- PASS: Six refined disturbed runs preserve passage/invalid counts and stops, final positions within 1 cm.

Six disturbed seed-1 flow cases were refined from 10 ms to 5 ms to 2.5 ms integration steps, retaining the same 10 ms controller sampling. Detailed values are in the verification JSON. This tests numerical implementation, not agreement with real flight.

## Implications and limits
A fixed bias shifts where a vehicle actually aligns relative to its intended lane. Delay makes phase decisions use older information. Successful cases support feasibility only inside this limited model and tested range; failures identify conditions requiring controller improvement. Five seeds and fixed biases do not establish a reliable probability of failure. Cautious scheduling is a comparator, not a safety-certified fallback.

The next useful navigation experiment is to reserve extra clearance for uncertainty and test it on new seeds and error profiles, retaining failures. The original aerodynamic research question still requires measured or independently validated interaction data in Steps 3–4. These scheduling results establish neither aerodynamic accuracy nor research novelty. Airflow remains off; motion is near one altitude with full rigid-body mechanics.

[Interactive Three.js comparison](milestone-06-robustness.html) · [Full data](milestone-06-study.json) · [CSV](milestone-06-study.csv) · [Verification](milestone-06-verification.json) · [Frozen protocol](milestone-06-protocol.json)

Post-result checks also refined each controller’s closest approach. At 2.5 ms, the cautious minimum was 0.150141 m and the flow minimum 0.152504 m; neither triggered a contact stop. The cautious case is only about 0.14 mm above the assumed threshold, so a “no contact” label must not be interpreted as a comfortable margin. See [extreme-case refinements](milestone-06-extreme-checks.json).
