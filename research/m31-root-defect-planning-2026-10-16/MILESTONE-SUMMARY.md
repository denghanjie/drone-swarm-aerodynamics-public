# A conditional bound for rotor-load error

We asked whether a proposed rotor-load estimate could be checked without solving every rotor equation again. Independent mathematical review supports a conditional error bound: a mismatch in the candidate equations can be converted into a conservative range for the model's true rotor forces and turning moments.

There is an important cost limit. The check still needs the interactions for the drones' **current positions and motor commands**. Building those interactions has been expensive in our completed large-swarm tests. Avoiding the final equation solves does not by itself remove that burden.

Decision: preserve the bound as a possible correctness tool, and prioritize how we construct the current interactions. No bound was calculated on experimental targets here, and no new speed, flight, physical-accuracy or novelty result is claimed. This analytical checkpoint is complete; the overall research is not.

The latest numerical Three.js demonstration is still [the root-secant replay](../m31-root-secant-2026-10-16/viewer/). It shows saved Boids/dynamics poses and the previous rejected forecast diagnostic. This desk review created no new trajectory.
