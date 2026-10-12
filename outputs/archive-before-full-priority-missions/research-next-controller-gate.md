# Next controller gate after milestone 30

The wall-priority study is an early-failure test. Its large-flock horizon is only20seconds. Keeping the flock clear of the first wall does not establish passage through the other halls or exclude a later jam.

Before treating the candidate as a reliable navigation method:

1. Freeze full-duration missions, with candidate and baseline on matched initial flocks. Treat the seeds already used in30 as development/regression evidence; reserve different initial flocks and geometry variations for evaluation.
2. Count complete passage, contacts, unfinished drones and connectivity separately. Retain whole-flock early stops. Report whether the added wall priority creates a queue or violates drone separation later.
3. Refine integration on representative successful and failing cases at common physical times. Extend command logging to identify individual obstacle/pair constraints and actual actuator outputs if investigating a new failure.
4. Test delayed/noisy local observations and disturbance compensation only after establishing the no-airflow controller behavior. Reintroducing the present unvalidated airflow model is a model-sensitivity experiment, not physical validation.
5. Use matched physical data before an aerodynamic accuracy claim. Keep GPU/current-pipeline throughput work distinct from Three.js replay speed.

The standard projection technique is not claimed as a new algorithm. The potential value is a reproducible diagnosis, controlled comparisons and, eventually, a validated accuracy/cost result.
