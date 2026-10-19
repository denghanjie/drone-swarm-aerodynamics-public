# A second airflow component: useful improvement, substantial mismatch remains

We tested whether the adjusted downward-airflow model can also predict sideways air movement without fitting another number. It can describe some of that motion, but still misses a substantial part of the measured field. Keep this as a research candidate; it is not ready to be treated as validated swarm physics.

## What we did

The earlier checkpoint adjusted the strength of the downward jet using800near locations. This checkpoint kept that exact adjustment and used a standard conservation-of-mass relation to predict sideways motion. The new formula assumes a steady, symmetric jet with no mean swirl. It was projected onto the actual laser measurement plane, rather than pretending the measurements passed through the center of the drone.

All3,240saved records were retained.17locations outside the inner jet were excluded by a rule fixed before execution; none were excluded for their measured value or error. The main comparison used2,440farther locations. No new fit, sign choice, raw-array decoding or simulation trajectory was performed.

## What the evidence says

| Farther locations | Zero sideways baseline | Fixed physics candidate |
|---|---:|---:|
| RMS error, in the dataset's reference-speed units |0.01537428|0.01174757|
| Error divided by measured sideways signal |100%|76.41%|

The candidate reduced RMS error by23.59%. In the two fixed farther bands, remaining relative errors were77.66%and72.44%. The near band, reported descriptively only, had76.69%remaining relative error over783locations. These percentages describe whole-field RMS error, not an average percentage error at individual points. The zero baseline's100%is an identity for a nonzero measured signal.

The earlier adjusted axial comparison had9.80%relative RMS error on these2,440farther locations. Sideways motion is therefore much less well described relative to its own measured signal. The two components have different signal sizes; this does not say sideways error dominates total speed or drone force error.

## What this means

The axial fit does carry useful information into a second observed component without another tuned parameter. That is stronger evidence than showing another good-looking downward-flow plot. However, the remaining lateral mismatch is large. This experiment does not tell us whether its main source is left/right asymmetry, swirl, imperfect geometry, background drift, measurement stitching, calibration, or the scalar-to-vector interpretation.

These are previously exposed measurements from the same experiment. The result is descriptive cross-component evidence, not independent experimental validation. There is no experimental uncertainty envelope, statistical rejection, SI airspeed calibration, full3D or receiving-force validation, safe flocking claim, or demonstrated novelty. The continuity relation is already published theory.

## External-data search and next decision

We checked separate published experiments. Real3D measurements exist, but no compatible publicly downloadable raw far-field axial dataset was verified in this bounded search. We rejected a convenient two-plane flux comparison from Wolf2024 because both planes were too close to the drone for this model's admitted range. This is not a claim that no external dataset exists.

Next: use a separately preregistered left/right symmetry diagnostic to distinguish the part of the measured lateral field this symmetric candidate could possibly represent from the part it cannot. Pair only genuinely matching geometry, freeze one-to-one coordinate matching and mismatch rules before execution, retain unmatched cells and full-field metrics, and do not remove a mean drift or tune a lateral gain. This would diagnose a model assumption; separate calibrated measurements remain necessary for physical validation. Read the independent result review before adopting the next protocol.

## Reproducibility and display

Frozen source commit:b5a98584ce32f1cb2b11493dc259118192d94f85;35-file source manifest publicly verified2026-10-19T11:49:07.655920Z before execution. Sole evaluator and independent audit both exited0, without timeout/output-limit breach; both allocations are closed. Independent60-digit arithmetic checked all3,240candidate records,25,920original binary64words, inherited gain, complete selection and8metricgroups. Numerical tolerance2e-12 is not a physical accuracy claim.

[Three.js evidence view](viewer-v2/) shows the saved signed lateral measurements, candidate, residual and exclusions. Sparse arrows are enlarged display glyphs, not new flight paths or measured3D trajectories. [Test plan](PROTOCOL.md), [claim ledger](CLAIMS.md), [source and outcome reviews](review/), [external source search](review/EXTERNAL-DATA-SEARCH.md), [saved result](results/comparison.json), [independent audit](results/audit.json), [restart](RESTART.md). Final UI and result-publication status are recorded in UI-QA.md and the outside-manifest publication receipt.
