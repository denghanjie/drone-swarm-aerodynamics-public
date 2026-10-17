# Browser load calculations agree with the retained numerical reference

**What we tested.** We checked whether ordinary browser arithmetic can return the same drone forces and twisting effects as our carefully verified numerical model. This establishes a baseline before comparing faster methods. Both implementations received raw drone states and calculated their own interactions; neither received reference answers.

**What happened.** All twelve saved calculations—two methods on each of six 64-drone snapshots—passed every required numerical error limit. The two methods also returned identical scientific outputs on every snapshot. The independent checker passed fourteen arithmetic fixtures and detected all four deliberately corrupted records.

| Quantity checked | Largest normalized error upper bound, approximately | Required upper limit |
|---|---:|---:|
| Individual rotor force |2.76×10⁻¹⁶|10⁻⁸|
| Total thrust |2.66×10⁻¹⁶|10⁻⁸|
| Force in world coordinates |2.74×10⁻¹⁶|10⁻⁸|
| Twisting effect in world coordinates |1.07×10⁻¹⁶|10⁻⁸|

The force is the rotor-thrust resultant, excluding gravity; the moment is produced by those thrusts at their rotor offsets, excluding rotor reaction torque. These are normalized numerical differences, including reference uncertainty. Rotor error uses mg/4, total/world force uses mg, and moment uses mgR. They are not percentages of real-world physical accuracy. Exact rational checks determine acceptance; table values are rounded for reading.

**A preserved operational failure.** The browser itself completed its scheduled work, but the original outer supervisor failed with a permissions error during process cleanup. We kept that attempt failed. Its planned conditional checker was never launched. After a separate reviewed and published protocol, a new audit checked the unchanged saved records with the original checker. That separate audit completed successfully; it did not repeat drone calculations or repair the original supervision outcome. Both statuses remain visible in the 3D view.

**What this supports.** Ordinary native arithmetic is a numerically adequate baseline on these six retained snapshots under the current model. That is useful engineering evidence, not a new scientific algorithm. We can now prepare a small genuinely fresh-state transfer test before a matched cost comparison.

**What remains open.** These snapshots were already exposed during development. The original flights used local 3D Boids with shared course guidance and airflow disabled; the aerodynamic loads were calculated afterward and never changed those flights. We have not established generalization, aerodynamic flight response, physical accuracy, a speedup, real-time operation, or a 5,000-drone coupled browser system. No timing benchmark or fresh case was run in this milestone.

[Open the actual-record Three.js view](../m31-native-load-baseline-2026-10-17/viewer/) · [Raw browser outputs](../m31-native-load-baseline-2026-10-17/results/browser.json) · [Exact checker report](results/check.json) · [Readable all-call values](results/summary.json) · [New audit attempt](results/check-attempt.json) · [Original failed attempt](../m31-native-load-baseline-2026-10-17/results/browser-attempt.json) · [Reproduction](REPRODUCTION.md) · [Result claims](RESULT-CLAIM-LEDGER.md).

Native source checkpoint: [e6f99b1](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/e6f99b140c70887fa0ed05c14574221eb5db12da). Separate audit source and preserved failure: [eb049de](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/eb049deb66c4c7aee78826b2eecde8281d02a1b9). The later result publication receipt binds this summary, viewer and completed evidence.

The [inherited literature ledger](../m31-native-load-baseline-2026-10-17/LITERATURE-EXPERIMENT-LEDGER.md) records the model's sources and limitations. Numerical agreement does not validate their adaptation to this drone. No new novelty claim is made.
