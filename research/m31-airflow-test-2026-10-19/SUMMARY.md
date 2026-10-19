# We found a mismatch in the airflow, before adding a second drone

Imagine trying to predict how a fan pushes a toy airplane. First, we should check whether we predict the fan's wind correctly. That is what this checkpoint did for one drone.

We compared two fixed formulas with3,240 measured locations in a published laser measurement of airflow. Our current model predicts stronger downward airflow on this sample than the measurements indicate. The paper's own fitted curve comes closer, but also has a remaining mismatch. Neither formula was tuned during this test.

| Formula | Average absolute difference from measured downward velocity |
|---|---:|
| Our current airflow model | 0.2320 reference-speed units |
| Paper's fitted curve | 0.0857 reference-speed units |

These numbers are units of the experiment's reference speed, not percentage errors and not metres per second. The first comparison assumes that our model's reference speed matches the experiment's; that equality is not independently calibrated. The original source model describes speed magnitude, while our project treats its output as downward airflow. These distinctions could contribute to the mismatch.

This is useful because it shows a disagreement before we use the formula that turns airflow into another drone's thrust. We should resolve the airflow comparison before tuning that thrust formula. Otherwise one adjustment could hide a different error.

The paper's curve was fitted to this same experimental study. Its smaller error is therefore a useful reference, not independent proof that we have solved the physics. The experiment measured one plane; we have not validated airflow throughout a3D volume, flying groups, safety or a novel result.

The calculation and independent audit both completed successfully. The audit checked12,960 original data values,6,480 field predictions and all saved summaries. It verifies the calculations, not the truth of a physical model. Original data, frozen source, all selected readings, limits and reviews are preserved. Source was published and independently verified before execution.

[Open the rotatable3D evidence view](http://127.0.0.1:8876/research/m31-airflow-test-2026-10-19/viewer-v2/). Switch between measured airflow, our prediction, the paper's fitted curve, and our prediction error. This is an evidence view of a real measurement plane, not a new swarm flight simulation. Desktop/mobile and all four modes passed the second display check; the first check's404 failure is retained.

Next: make the airflow model's units, measurement plane and reference-speed assumptions explicit, resolve what the published fit actually represents, then test any revision under a new bounded protocol. These now-exposed measurements cannot become an unseen validation set. The two-drone thrust law and swarm model remain unresolved.

[Protocol](PROTOCOL.md) · [Full result](results/comparison.json) · [Independent audit](results/audit.json) · [Interpretation review](review/RESULT-REVIEW.md) · [Verified literature](LITERATURE.md) · [Restart](RESTART.md).

“Published” here means a reproducible public repository checkpoint; it does not mean a peer-reviewed paper.
