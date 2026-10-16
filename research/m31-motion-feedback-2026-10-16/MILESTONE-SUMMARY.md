# Milestone: aerodynamic loads now change the recorded motion

**We have verified a small numerical feedback implementation. We have not validated its physics or established a publication result.** Earlier 5,000-drone calculations evaluated loads on frozen poses. This checkpoint applies the provisional loads to motion at every integration stage, including their roll/pitch moments.

We first ran three interpretable pairs: no influence, centered vertical alignment, and a 4 cm lateral offset. Each ran with airflow off/on at three timestep sizes. All 18 primary paths and controls passed their declared numerical gates. This admitted the planned six exploratory paths for 16 local 3D Boids over two seconds. All 24 paths completed without model rejection or recorded contact. This is a short, designed numerical sample, not evidence of general stability or safety.

| Finest recorded case | Maximum sampled on/off position difference | What to learn |
|---|---:|---|
| No-influence control |0 m|Turning on an empty interaction field changes nothing.|
| Centered pair,0.5 s |0.246 m|The lower drone descends under the modeled thrust reduction.|
| Offset pair,0.5 s |0.496 m|Differential rotor loads produce a strong rotation in this unstabilized fixture.|
|16 local Boids,2 s |1.102 m|The previously ignored load feedback materially changes this model's short trajectory.|

In the 16-drone case, maximum recorded stage tilt from vertical was 19.56 degrees with coupling versus 8.85 degrees with airflow off. Its maximum on/off quaternion-orientation difference was 84.13 degrees, which includes yaw and must **not** be called 84 degrees of tilt. The offset fixed-command pair reached 92.97 degrees of tilt, well outside the hover evidence motivating the provisional wake shape. This is a model extrapolation, not a prediction established for real hardware.

The two finer 16-drone coupled runs differed by at most 5.35e-8 m at sampled positions, 2.14e-7 m/s in velocity, 1.43e-7 rad in orientation and 1.14e-7 nominal-hover force units. All 32 observable gates across the eight case/mode combinations used the predeclared “both discrepancies below 1% of tolerance” branch. They passed sampled numerical resolution preferences; this does not establish formal integration order or a rigorous continuous-time error bound.

The independent Python/NumPy check passed 283,446 checks covering 234 saved endpoints and 192 selected RK stage states, using independently reconstructed geometry, analytic cubic roots and body equations. It also checked saved-slope step assembly, source/result hashes, schedules and decision gates. It did not independently regenerate every trajectory, Boids command or contact check. The actual experiment and review took 2.551 s and 1.051 s under their separate continuous supervisors; these are execution records, not performance benchmarks.

What improved: the simulation now contains explicit pose→loads→force/moment→motion feedback, with matched airflow-off controls and saved numerical evidence. What remains provisional: the instantaneous wake shape, source-total amplitude, ideal-power receiver, command interpretation, nominal yaw torque and missing wake history/airspeed corrections. No compatible physical measurement was added. No browser simulation speed or 5,000-drone dynamic accuracy was measured.

The Three.js page shows exact new paired recordings, with common camera bounds, all four cases, frame controls and clear labels. Rendering uses no scientific solver. Read the raw results, frozen protocol, independent check and result claim ledger before interpreting the visible motion.

Next question: under the same small Boids controller, how much of the modeled trajectory change remains if aerodynamic roll/pitch moments are suppressed while collective force feedback is retained? That would isolate a modeling component within this provisional model, not establish a physical approximation or a speedup. Any new test needs its own frozen protocol; this campaign is closed.
