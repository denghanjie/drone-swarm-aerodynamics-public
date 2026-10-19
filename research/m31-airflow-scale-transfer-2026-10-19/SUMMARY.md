# One strength adjustment transfers to farther measurements

Our model's airflow pattern deserves further investigation. In this dataset, much of its earlier mismatch can be removed by changing the predicted strength with one constant multiplier.

We used 800 locations near the drone to determine that multiplier, then kept it fixed at 2,440 farther locations. For our current model the multiplier was 0.545. No farther measurement was used in that fit.

At the farther locations, average absolute error dropped from 0.2233 to 0.0236 in the saved reference-speed units: an 89.4% reduction under that convention. The primary scale-independent comparison was a remaining whole-field relative RMS discrepancy of 9.8%. This means the RMS error is about one tenth of the RMS measured signal; it does not mean every point is within 9.8%, or that the model is 90.2% physically validated.

| Fixed formula, adjusted using the near band only | Multiplier | Farther-region relative RMS discrepancy |
|---|---:|---:|
| Our current model | 0.5450 | 9.80% |
| Published planar reference | 1.1173 | 29.64% |

Our adjusted model's two farther bands had discrepancies of 10.50% and 7.78%. Its near fitting band still had 20.47%, so one factor does not explain every feature. The published reference already used this experimental study when it was developed; this comparison does not establish general superiority over that paper's method.

The important change in understanding is this: the earlier unadjusted disagreement is not enough to dismiss our model's spatial pattern. A simple strength adjustment learned nearer the drone also works substantially better farther away. We have not shown why the adjustment is needed.

The source check found different reference-speed conventions in the article and some separate multi-drone plotting scripts. The single-drone preprocessing step remains unavailable. The fitted 0.545 is therefore an empirical number, not a proven physical conversion, and its proximity to one half does not establish a rotor-count error. The primary corrected relative-RMS result is unchanged by any one common positive rescaling of the measured speeds; it still cannot resolve spatially varying calibration, the axial-versus-speed distinction or 3D geometry.

All locations were exposed in the previous checkpoint. This is a prospective within-dataset transfer calculation, not blind or independent validation. It adds useful evidence, not a demonstrated novel result. No production wake, receiving-drone thrust formula or flocking controller has been replaced.

The prospective source was independently reviewed, published and verified before the single execution. The independent audit passed all 3,240 records, both training-only gains, 6,480 corrected predictions and 16 metric groups. The new Three.js view passed its first desktop/mobile check, six display modes, camera controls and corrupted-evidence refusal.

[Open the 3D evidence view](http://127.0.0.1:8876/research/m31-airflow-scale-transfer-2026-10-19/viewer/): orange locations set the adjustment; blue locations evaluate it. Switch to the original and adjusted airflow views to see the change. This shows a saved measured plane, not new flight simulation.

Next evidence needed: recover the actual single-drone dimensional normalization, and evaluate the preserved candidate against a separate documented axial-flow measurement. Neither has been established yet. Continue public-source investigation; no author contact, paid experiment or silent correction of the dataset. Further same-field tests must be labeled exploratory, with their own bounded protocol.

[Protocol](PROTOCOL.md) · [Full result](results/comparison.json) · [Independent audit](results/audit.json) · [Interpretation review](review/RESULT-REVIEW.md) · [Verified sources](LITERATURE.md) · [Restart](RESTART.md). Publication here is a public repository checkpoint, not a peer-reviewed paper.
