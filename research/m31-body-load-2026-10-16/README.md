# Complete field-to-body-load feasibility checkpoint

**Source frozen and independently reviewed. No generated input, numerical result or scientific launch yet. Publication and independent remote verification are pending.**

We want to know whether a single browser GPU query can calculate the assumed airflow model for every drone, then deliver accurate rotor forces, total lift and body moments. Earlier tests rejected much stricter component error targets. Those failures remain unchanged. This is a distinct question with fresh inputs and prospectively chosen complete-output limits.

The intended test includes prescribed unequal motor-state inputs and every receiver at sizes up to 5,000. It excludes flight integration, control, Boids steering, world-coordinate force rotation, rendering and speed comparison. The existing local 3D Boids milestone remains the behavioral baseline; these new static arrangements are numerical test fixtures, not emergent flock motion.

The accuracy targets are engineering choices for agreement with an assumed model. They are not measured physical tolerances or evidence of flight safety. Physical validation, useful computational savings and publication novelty remain unresolved.

The preceding coordinate-origin result is published at commit `436762c2d05408a22ba66400d64e46e759cc7b99`. It has no candidate and a failed independent integrity review, with a separately documented checker lifecycle error. Its science/review budgets and omitted stages are permanently closed.

The adopted contract, implementation and fixed controls are prepared. Read `PROTOCOL.md`, `design/ADOPTION.md` and `design/API.md`. Numerical exposure still awaits final independent source review, freeze, privacy-reviewed publication and independent remote verification. Stop new overnight launches at 2026-10-15T23:00:00Z.
