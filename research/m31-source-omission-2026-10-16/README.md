# M31 checkpoint: bounded omission of wake sources

**The candidate passed all planned finite numerical checks and reduced complete static-query time on both new configurations.** This is a useful implementation result relative to the existing equations. It does not establish physical accuracy, real-time browser flight or novelty.

In plain language: for each drone, we estimated the largest effect each nearby source could have on any of its four rotors. We skipped provably zero sources and a limited total of weak sources. The remaining sources still received four rotor calculations, preserving different loads on different sides of a drone.

[Explore the saved Three.js evidence](viewer/) · [Frozen protocol](PROTOCOL.md) · [Claims and limits](claims.md) · [Verified prior work](prior-work.md) · [Reproduce](REPRODUCE.md)

## What was tested

One frozen invocation:24adverse small cases,12already-exposed historical flock snapshots, and two fresh static synthetic configurations of1,000/5,000vehicles.34valid cases passed every accuracy gate. Four deliberately invalid cases were rejected by all four implementations. All38case checks passed, with69,285,616runtime assertions,152attempted field queries and36warmup/measured queries. No flight integration occurred.

Targets were fixed before execution: body-thrust error<=1.32435mN and each roll/pitch moment error<=10.488316895µN·m. Roll and pitch moments describe the model's tendency to turn the drone, caused by unequal rotor thrust. These are analyst-selected numerical allowances, not safety tolerances. Maximum observed body-thrust error was0.282433261mN; maximum roll/pitch error was5.111174061µN·m. Every inspected per-source and aggregate bound passed its frozen numerical allowance.

## Computation cost

B is the original implementation; M shares the candidate's geometry/traversal structure but retains every source; C applies zero screening and bounded positive omission. Each timed query rebuilds all geometry, neighbors and decisions, evaluates fields and receiver loads, and computes a checksum. One warmup and five recorded passes per method/input; all successful repeat outputs were checked against their corresponding correctness output.

| Static input | Original B median s | Matched M median s | Candidate C median s | C/B | C/M |
|---|---:|---:|---:|---:|---:|
| fresh1000 | 0.170814 | 0.108610 | 0.084826 | 0.4966 | 0.7810 |
| fresh5000 | 1.888841 | 1.333427 | 1.121855 | 0.5939 | 0.8413 |

At5,000vehicles, C took40.6%less time than B and15.9%less than M. At1,000, the reductions were50.3%and21.9%. These are descriptive technical repeats on AppleM4, macOSDarwin25.5.0 arm64, Node24.19.0. They are not confidence intervals across swarms/devices. One5,000-vehicle query still takes over a second; this does not establish real-time browser simulation or low-end device feasibility. Full timings and ranges are retained in results/descriptive-summary.json and raw/timings.ndjson.

## Evidence by large input

All loads use prescribed equal nominal motor inputs0.0662175N, fixed isolated-hover source strength and the unchanged M28 sum-rotor equations. Historical motor states were not recovered. New lattice inputs are static synthetic algorithm tests; original historical poses came from local3D Boids flights with map guidance and airflow off.

| Input | Vehicles | Max thrust error mN | Max roll/pitch error µN·m | Exact-zero source culls | Positive-bound source omissions |
|---|---:|---:|---:|---:|---:|
| historical-case-0-t-0 | 1000 | 0.064859 | 1.799079 | 145,670 | 290 |
| historical-case-0-t-20 | 1000 | 0.266343 | 4.753059 | 270,947 | 1,016 |
| historical-case-0-t-30 | 1000 | 0.280578 | 5.014146 | 245,294 | 926 |
| historical-case-0-t-60 | 1000 | 0.262743 | 4.856025 | 209,759 | 753 |
| historical-case-1-t-0 | 1000 | 0.052837 | 1.351743 | 144,795 | 279 |
| historical-case-1-t-20 | 1000 | 0.274170 | 4.768040 | 287,112 | 1,275 |
| historical-case-1-t-30 | 1000 | 0.229448 | 4.810041 | 258,029 | 1,238 |
| historical-case-1-t-60 | 1000 | 0.235550 | 5.111174 | 148,441 | 595 |
| historical-case-2-t-0 | 5000 | 0.067186 | 1.810719 | 912,472 | 1,632 |
| historical-case-2-t-20 | 5000 | 0.281561 | 5.055113 | 2,277,318 | 8,526 |
| historical-case-2-t-30 | 5000 | 0.282433 | 4.919857 | 2,245,843 | 8,483 |
| historical-case-2-t-60 | 5000 | 0.266645 | 4.901585 | 2,081,167 | 8,146 |
| fresh1000 | 1000 | 0.125632 | 3.515062 | 684,020 | 4,965 |
| fresh5000 | 5000 | 0.141524 | 3.407386 | 6,488,768 | 26,742 |

Zero culls and positive omissions are counts of receiver/source pairs; a source may be retained for one receiver and omitted for another. Drones are not removed from the flock. The original finite-neighborhood/wake cutoffs remain part of the model.

## Conclusion, limitations and next decision

Supported: the candidate meets the fixed body-load budgets on every valid planned case and costs less than B/M on the two new inputs. The campaign used one40.740462375s supervised science invocation and retained240raw files/38,259,345bytes. Source freeze88dc542604d902909b7cc96c0bd0ca93b88cab0c was pushed and independently verified before execution;66direct input/source pins were checked.

Not yet isolated: how much benefit comes from approximating positive contributions. C bundles that approximation with exact-zero screening. Most skipped pair visits are exact zeros; the C/M timing result cannot by itself assign a causal speed benefit to positive omission. A separately frozen zero-screen-only ablation is the next useful test. No post-exposure tuning or rerun of this campaign is permitted.

The real-arithmetic bounds use standard monotonicity and Lipschitz arguments. Their binary64 implementation has frozen engineering margins and finite tests, not a universal rounding certificate. Generic error-controlled source pruning is established prior work. Fixed-power receiver physics, source strength, overlapping wakes, walls/ground/unsteadiness, long-flight numerical accuracy and novel publication value remain unresolved. The viewer renders exact saved poses/loads; it performs no new physics.

Independent saved-data review passed2,829,776checks with zero failures in its sole invocation (4.16695675s externally). The science plus review total is44.907419125s; budget is terminal. [Review scope and limits](INDEPENDENT-SAVED-REVIEW.md), [closed restart record](POSTRUN-RESTART.md).
