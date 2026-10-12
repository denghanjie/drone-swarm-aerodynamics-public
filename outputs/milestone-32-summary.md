# Milestone 32 — visible airflow and a better accuracy diagnosis

**We can now see the modeled interaction between drones. We have not validated it against real flight.**

Open the [Three.js wake lab](milestone-32-lab.html). Start with “Understand two drones”: the upper drone pushes air down, and the lower drone receives less predicted inflow when moved sideways. Return to the flock to see which neighbors influence each other. The moving dots are direction cues, not a fluid simulation.

The flock recordings come from milestone 28, where airflow really did affect the equations of motion. The matched airflow-off flock finishes; the three coupled examples stop at contact or a model limit. They use the earlier controller. The successful 5,000-drone missions still have airflow off.

**The new accuracy test points toward sensitivity to earlier state differences.** Starting all three step sizes from exactly the same saved flock at 20 s produces a maximum difference of 0.879 micrometres for 2.5 vs 1.25 ms through 30 s. Starting from the two slightly different historical states, but using the same 2.5 ms step, instead produces 48.5 mm. Their initial position difference was only 8.64 micrometres, although velocity, attitude, angular rates and motor states also differed.

This is a diagnosis in one selected interval, not a fix or a proof of chaos. The three earlier full-trajectory checks remain failed. The next task is to identify which feedback decisions amplify the inherited differences, then evaluate a proposed correction on fresh cases. Physical measurements remain separately necessary.

All six prescribed diagnostic continuations are saved, with commands, position traces, full endpoints and controller summaries. [Detailed report](milestone-32-report.md) · [Frozen first plan](milestone-32-protocol.json) · [Separate follow-up plan](milestone-32-checkpoint-protocol.json).
