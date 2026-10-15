# M31 checkpoint: full-flock static force reference

**All 12 fixed-pose comparisons pass the numerical screens set before execution.** Two independently written implementations agree across all 28,000 saved vehicle poses and 112,000 receiving rotors, with flocks up to 5,000 drones. A separate saved-data-only review passes 3,067,306 checks in its first and only invocation.

In plain language: before asking a cheaper calculation to imitate our airflow model, we checked that two different calculations of that model give the same answer. This checkpoint supplies a conditional numerical reference. It establishes neither a new method nor correct real-world forces.

[Inspect the Three.js flock and selected drone's loads](viewer/) · [Frozen protocol](PROTOCOL.md) · [Evidence limits](claims.md) · [Independent review](INDEPENDENT-SAVED-REVIEW.md) · [Reproduce](REPRODUCE.md)

## Method

The original implementation uses a spatial grid, double-cross quaternion rotation and Newton's method. The independent implementation enumerates every source, uses matrix rotation, independently coded wake arithmetic and bracketed bisection. It imports none of the original scientific modules. Both apply the unchanged M28 `sum-rotor` equations to exact historical M31 poses at 0, 20, 30 and 60 seconds in three cases. All saved vehicles are included; no active mask is reconstructed.

Historical motor states were not retained. We explicitly prescribe all four nominal motor thrusts as mg/4 = 0.0662175 N. Source amplitude stays fixed at the original isolated-hover value. These inputs are not recovered historical actuation or a tilted-hover equilibrium. All computations are static; no controller or integration is run.

## Evidence

Source freeze: `89c3b14e6d59f2446d257bd106e3af4bbcb029c6`. Its 22 pinned files and exact freeze bytes were independently verified before execution. One science invocation completed in 7.878831208 seconds; the separate review took 5.317982083 seconds externally. These are execution diagnostics, not speed comparisons. All 50 raw files (32,883,829 bytes) are retained. The budget is terminal.

Largest absolute differences: inflow 7.549516567451064e-14 m/s; effective rotor thrust 3.608224830031759e-16 N; body thrust/world-force components 4.996003610813204e-16 N; world-moment components 1.588356182691264e-17 N m. Independent classifications match the preceding complete domain audit. Ordinary versus compensated summation differs by at most 1.7763568394002505e-15 m/s; this is a numerical diagnostic, not a certified error bound.

| Flock | Saved time s | Vehicles | Max inflow difference m/s | Max body-thrust difference N | Max modeled body-thrust loss mN | Max modeled absolute roll/pitch µN m |
|---|---:|---:|---:|---:|---:|---:|
| wide1000 | 0 | 1000 | 4.396e-14 | 1.665e-16 | 94.772260 | 444.335837 |
| wide1000 | 20 | 1000 | 8.438e-15 | 5.551e-17 | 100.277959 | 520.413880 |
| wide1000 | 30 | 1000 | 2.665e-15 | 5.551e-17 | 104.862642 | 409.934687 |
| wide1000 | 60 | 1000 | 1.554e-15 | 1.110e-16 | 91.693101 | 415.969297 |
| narrow1000 | 0 | 1000 | 4.707e-14 | 1.943e-16 | 98.150862 | 414.059900 |
| narrow1000 | 20 | 1000 | 7.105e-15 | 5.551e-17 | 123.726313 | 455.983310 |
| narrow1000 | 30 | 1000 | 1.155e-14 | 1.110e-16 | 139.818086 | 530.741897 |
| narrow1000 | 60 | 1000 | 1.998e-14 | 5.551e-17 | 98.042968 | 489.846183 |
| wide5000 | 0 | 5000 | 7.550e-14 | 4.996e-16 | 100.215670 | 443.600745 |
| wide5000 | 20 | 5000 | 1.776e-14 | 1.110e-16 | 121.579508 | 508.174697 |
| wide5000 | 30 | 5000 | 2.220e-14 | 1.110e-16 | 139.903298 | 537.610180 |
| wide5000 | 60 | 5000 | 3.331e-14 | 1.110e-16 | 124.802974 | 564.126785 |

The last two columns are outputs of the prescribed model, not measured flight effects. The largest predicted body-thrust loss is 0.1399032982187171 N (52.82% of nominal weight). That large effect depends on unvalidated fixed-source, additive-wake and constant ideal induced-power assumptions; it is not evidence that the historical drones experienced that loss. Body thrust also differs from world-vertical support at nonzero tilt.

## Conclusion and next decision

The finite static arithmetic comparison is qualified on these inputs. It is now reasonable to design a separately frozen approximation test against this retained reference. A promising question is whether negligible source contributions can be omitted under a summed force/moment error budget. This remains a hypothesis requiring adverse cases, independent review and measurement of both error and cost.

Physical calibration, held-out generalization, the original long-flight numerical failures and novelty remain unresolved. The viewer shows exact saved local3D Boids poses with prescribed static model loads; it adds no live flight or aerodynamic measurement. Later main/DOT work is preserved.
