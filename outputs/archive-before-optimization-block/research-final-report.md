# Research status — a working simulation, with validation still open

## Goal

Determine how much aerodynamic detail is needed to predict a flock of drones moving through restricted space, and whether that calculation can run interactively in a browser.

The project retains the original eight steps. Checkpoints 15–18 belong to Step 5: making the swarm-navigation experiment credible enough to support later aerodynamic comparisons.

## Method

We separate three questions:

1. **Does the code behave consistently?** Repeat the same initial conditions at a smaller physics step and compare the trajectories.
2. **Does the group accomplish its task?** Measure passage, contact stops and whether the flock remains connected. Preserve every failed trial.
3. **Does it predict real drones?** Compare against independent physical measurements. This question remains open.

The current navigation model contains 50 rigid bodies with attitude and motor dynamics. Drones use local separation, alignment and cohesion in all three dimensions, plus known-map route guidance and a local clearance filter. There is no central allocation of passage slots. Three.js displays the saved numerical trajectories; the research runs are computed offline in Node. Rendering them does not itself validate their physics or establish live browser compute speed.

## Current results

Smoothed flocking and route steering improved tight-course completion from 179/250 to 249/250 across five new matched starting conditions at the original 5 ms step. No contact stop occurred for either controller in that comparison. However, two of seven new-variant refinement checks failed, and a later 1.25 ms audit changed one case from 50 to 49 completions. Numerical trajectory reliability is still unresolved.

A further 10 cm inward steering offset completed all 50 drones in each of eight new cases at 5 ms, versus 399/400 total completions for the reference. No contact stops were recorded, but two flocks ended disconnected; the worst split was 41+9. It also reduced the minimum observed clearance. One of six initial refinement checks failed; that case did agree when comparing 2.5 ms against 1.25 ms. This is an experimental trade-off, not a validated replacement.

Stronger retention is rejected: it caused a collision in a fresh case, and several development/fresh numerical checks failed. All failures remain in the saved record.

## What the group behavior means

Neighbor interactions make group shape and individual trajectories emerge from local decisions. Earlier matched social-rules-off experiments established a flocking effect in open space. The latest passage controllers preserve these local rules. Their shared destination, aperture map and sphere-route preferences are prescribed, so these runs are not a demonstration of discovering a route through unknown terrain.

Completion, heading agreement and connectivity are different measurements. A group can finish while splitting; an aligned group can leave one drone behind. All three outcomes remain visible in the records.

## Physics and computation

The rigid-body mechanics and contact checks were unchanged in this block; dependency hashes match the pre-block archive. The time-step comparisons assess numerical agreement for a fixed 100 Hz controller. They do not establish flight-data accuracy, safety under observation errors, reliable wake forces, battery limits or controller-rate robustness.

Airflow is off in the current flock-passage experiments. Earlier wake equations and exploratory interactions remain available, but the necessary wake-to-force and multi-wake validation is unresolved. Earlier GPU measurements establish agreement for the implemented mechanics and performance for a scheduled hybrid baseline. They do not establish GPU scaling for this local Boids controller with validated aerodynamics.

## Conclusion and implications

The concept is technically plausible and worth pursuing as an exploratory simulation study. A local three-dimensional flock can be built, rendered, tested against controls and improved through reproducible experiments. We have not yet answered the original aerodynamic accuracy-versus-cost question or established a novel scientific contribution. Smoothing controller transitions and adding clearance margins are established techniques; these implementation improvements alone are not a novelty claim.

The next substantial research gate is to freeze the navigation candidates and their known failure cases, test its behavior under observation and control uncertainties, and obtain an independent physical reference for aerodynamic forces. Then compare aerodynamic models on the same missions and measure the full actual Boids computation at larger scales. A visually convincing flock or a large GPU body count cannot substitute for these tests.

## Records

- [Consolidated block summary](research-block-15-18-summary.md)
- [Current 3D viewer](research-results.html), [original eight-step roadmap](research-roadmap.md), [complete stage history](research-stage-log.md)
- [Earlier assessment, preserved before this block](archive-before-convergence-block/research-final-report.md)
- [Manifest](research-manifest.json), [verification and isolated reproduction helper](research-reproduce.py)
