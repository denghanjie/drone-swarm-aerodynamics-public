# Step 3A — Select an airflow model and identify the missing physics

## Goal
Build the next layer of the research without confusing three different quantities:

**Airflow at a location → changes in rotor forces and moments → drone motion.**

Step 2C checked the last connection for a prescribed force. This step selects and implements a candidate for the first connection. The middle connection is still missing.

## Evidence checked

[Bauersfeld et al., arXiv:2403.13321v3](https://arxiv.org/html/2403.13321v3), Sections III and VI–VII, gives a mean far-field wake model for hovering quadrotors. Its normalized constants are 10.11, 0.07668 and −5.817. The far-field threshold is approximately 2.5 motor-distance scales. The fit uses uncanted rotors; the smallest measured vehicle is 230 g. The paper also demonstrates downwash compensation, but its throttle conversion depends on the particular motor electronics.

[Kiran, Ayanian & Breuer, arXiv:2507.09463v1](https://arxiv.org/html/2507.09463v1), Sections II–III, measures Crazyflie interaction forces, moments and airflow. Its characteristic length is 32.5 mm. Offset configurations produce pitching moments; dynamic approach and retreat produce different loads. Its dataset is linked at [Brown](https://doi.org/10.26300/64d4-wa17), which returned a human-verification page in our previous retrieval. Raw measurements remain unavailable to this project. The paper's wording about thrust reduction is inconsistent between its results and conclusion; do not convert those summaries into fitted force coefficients.

The [Neural-Swarm repository](https://github.com/aerorobotics/neural-swarm) still refers to Box-hosted training files without an anonymously downloadable complete archive in the inspected README. A [Zenodo record for the Bauersfeld paper](https://zenodo.org/records/20804228) lists a PDF, not raw airflow data. This focused search did not establish another accessible raw dataset; it does not prove none exists.

## Method: reproduce the normalized equation first

Define `s` as distance down from the source rotor plane, `r` as radial distance from its axis, and `l` as the source model's motor-distance scale. We keep this scale explicit rather than substituting our existing center-to-motor arm parameter.

Use `s̄ = s/l`, `r̄ = r/l` and `UH` as the ideal induced velocity of the source in hover:

```
UH = sqrt(m g / (2 ρ π R² × 4))
b̄ = 0.07668 (s̄ + 5.817)
Uc/UH = 10.11 / (s̄ + 5.817)
ξ = r̄ / b̄
U/UH = (Uc/UH) / [1 + (sqrt(2) − 1) ξ²]²
```

These reproduce Eqs. 1, 3–9 and Section VI-C of Bauersfeld et al. The symbol `b` means half-width: at that radius, speed is half the centerline speed. The implementation refuses `s̄ < 2.5`; refusal means unknown, not zero airflow. That lower cutoff alone does not establish validity for every larger distance, vehicle or flight condition.

In everyday terms: sufficiently far below a hovering drone, its separate rotor wakes become a wider stream. The model predicts a stream that spreads sideways and slows along its center.

## Results from our implementation

These are calculated values, not measurements.

| Distance below source, s/l | Centerline speed / UH | Half-width / l |
|---:|---:|---:|
| 2.5 | 1.21558 | 0.63775 |
| 3 | 1.14665 | 0.67609 |
| 5 | 0.93464 | 0.82945 |
| 10 | 0.63919 | 1.21285 |

The original implementation is in [wake.cjs](step03a-source/wake.cjs). [24 checks](step-03a-verification.json) passed, covering domain rejection, half-width identity, radial and axial behavior, dimensional scaling, ideal-power identities and invalid input handling. [CSV samples](step-03a-wake-samples.csv) reproduce the table. Run `node outputs/step03a-source/verify.cjs` from the workspace.

The dimensional helper defaults to assumed air density 1.225 kg/m³ and g = 9.81 m/s²; neither is a calibration to the experiments. Its output is scalar mean speed, not a complete incompressible velocity field. No wall flow, turbulent fluctuation, wake memory or multi-source interaction is included.

## Why we have not connected this to flight yet

Our current motor state tracks thrust in newtons with a first-order delay. Incoming airflow does not affect that relationship. Giving this model a wind speed will therefore not automatically reduce lift.

There are two reasonable implementations to compare later:

| Approach | What it needs | What it predicts |
|---|---|---|
| Empirical force/moment correction | Measured changes at matched geometry and motor settings | Additional wrench applied to the rigid body |
| Rotor inflow model | Rotor and motor response to airflow, including operating point | Effective thrust and torque from each rotor |

Choose one consistent accounting scheme. Applying a measured total thrust loss and also reducing rotor thrust for the same interaction would count the effect twice.

The separate ideal-power helper implements the source paper's Eq. 11. With incoming speed equal to the receiver's hover induced speed, it gives a power ratio of 1.618. This is an ideal aerodynamic power requirement at maintained thrust. It is not 61.8% extra thrust, an electrical power prediction, or a calibrated correction for our simulated motors.

## Conclusion

**Proceed with the research, but treat this as equation reproduction, not physical validation.** We now have an inspectable candidate for the mean wake and a clear specification of the missing force conversion. No new two-drone flight demonstration is presented as validated. Step 2C remains available unchanged.

Applying this model to our 27 g vehicle is an unvalidated size extrapolation. The Brown study is closer in scale, but its geometry and normalization must be reconciled before reuse. We will not interchange the papers' length parameters or their fitted coefficients.

## Implications for novelty and the next experiment

A lightweight wake model and two-drone compensation already exist; those alone are not our contribution. Our proposed question remains: **how much aerodynamic detail is needed to preserve conclusions about swarm throughput at a given computation budget?** This is a candidate contribution, not an established novelty claim.

Before a crowd simulation can support that question:

1. **Match one vehicle and operating point.** Record rotor coordinates, propeller dimensions, mass, motor command convention and test conditions.
2. **Identify the force conversion.** Prefer measured forces and moments at several separations and commands. If unavailable, use an explicitly hypothetical rotor model and report sensitivity, not measured accuracy.
3. **Reserve whole configurations for testing.** Fit on some separations/runs and predict the withheld ones. A curve used to tune the model cannot also be its independent validation.
4. **Test two drones before summing neighbors.** Compare force, moment and transient response. Pairwise agreement does not establish that many overlapping wakes add correctly.
5. **Then compare throughput and runtime.** Keep controllers and actuator limits fixed, report how often the aerodynamic model is used outside its supported conditions, and make the virtual gate free of wall aerodynamics initially.

The next implementation milestone is a two-drone model with an explicit, documented rotor/force assumption and a switchable zero-interaction baseline. Physical validation remains a separate gate requiring measurements.
