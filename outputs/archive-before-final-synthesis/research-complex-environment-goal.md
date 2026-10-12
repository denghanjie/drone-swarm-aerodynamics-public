# Active goal — complex-environment local flocking

Build a reproducible factory/city benchmark in which a shared mission guides genuinely local 3D Boids, then measure how navigation and computation change from50 to200,1,000 and5,000 drones. Add explicitly labeled aerodynamic approximations and evaluate their accuracy only when independent observations are available.

## Milestones and completion evidence

1. **Factory benchmark:** build a collision-consistent3D factory with offset doorways, changing passage heights, racks and machinery. Establish a local Boids baseline and social-rule ablations; retain failures. Deliver a Three.js replay and a reproducible geometry/neighbor-search test suite.
2. **Actual flock scaling:** use spatial neighbor searches for the current flock. Test increasing count at documented density and confinement, preserving the same local rules. Report initialization, steering, rigid-body integration, contact checks, rendering and total cost separately. Short timing tests do not count as completed missions.
3. **Mission evaluation:** frozen unseen starting flocks, complex routes and passage widths. Measure completion, contacts, connectivity, spread, elapsed time and numerical sensitivity. Shared route guidance is allowed; individual assigned trajectories and passage slots are not the intended model.
4. **Aerodynamic comparison:** compare airflow-off and clearly identified approximate interaction models on matched missions. Validate the receiving-vehicle force response and geometry against independent measurements before claiming physical accuracy. Keep mean downwash, fluctuations and multiple-wake assumptions distinct.
5. **Synthesis:** conclude what works, what fails, what scales and what is still unvalidated. Preserve all source, configurations, raw results, failed cases and milestone replays.

The first environment is a synthetic factory. Dimensions are an explicit experimental design, not a reconstruction of a real facility. Route discovery is outside this first benchmark: the fleet receives a broad shared route corridor; local motion remains individually computed. The original eight research steps still apply, with this goal supplying the richer experiments for Steps5–8.

Success of the research goal means a defensible benchmark and evidence, not an obligation to make every5,000-drone mission succeed. Failures and computational limits are valid findings. The goal remains active until the required comparisons and records are complete.
