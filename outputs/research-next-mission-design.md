# Next full-mission design — draft before execution

This is preparation for the active goal, not a completed experiment or frozen protocol. Milestone 25 first establishes early-window calculation cost and investigates the 200-drone endpoint discrepancy. Its results must inform feasible execution and numerical settings without changing its already frozen tests.

The next mission block must execute actual 1,000/5,000 local drones through the entire factory horizon, rather than reuse the old scheduled queue or call two-second windows successful navigation. Preserve all unfinished and stopped cases. A failed or computationally expensive mission is evidence, not a reason to hide the case.

## Planned dimensions

Use fresh seeds, the same documented increasing-volume initialization and unchanged local rules. Vary passage geometry in separately frozen paired cases so the course challenges more than an initially forgiving 5×4 m doorway. Retain known shared route guidance, no assigned individual trajectories or scheduling, and count completion, contact, connectivity and spread separately. Numerical refinements must be labeled separately from primary missions; a single successful fine-step pair is not a guarantee at larger counts.

## Records and execution constraints

Large exact JSON replay arrays can dominate memory and serialization. Preserve full initial/final states and physics/contact outcomes; write sparse exact position/quaternion frames incrementally in Float64 binary files, with explicit timestamps and schema, rather than holding every frame in one giant JSON object. Visual interpolation between saved frames must be disclosed and never used as a contact detector. Contact checks stay at every physics step; scientific measurements keep their declared cadence.

Before using streamed recording, compare a small fixed run against the frozen simulator and require exactly identical final states and metrics. Record numerical and viewer sources, protocol hashes, initialization convention, count/geometry, wall cost, failures and per-run progress. Avoid concurrent numerical jobs when making timing claims. Select full-mission horizons before inspecting mission outcomes and keep truncations visible.

The goal then requires matched airflow-off and explicitly approximate aerodynamic models. Independent measurement access remains a separate gate; no comparison between two assumed models constitutes validation of either one.
