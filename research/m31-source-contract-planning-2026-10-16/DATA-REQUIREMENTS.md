# What would make the physical test possible?

We need observations that connect what the motors do to the air they move. Agreement between two computer implementations does not supply that connection.

The numerical vehicle assumes a mass of 27 g, rotor radius of 23 mm and arm coordinates of ±28 mm. These are model parameters, not verified properties of a tested physical vehicle. Identify the actual propeller, motor, controller, battery/supply, geometry and support arrangement before claiming compatibility. Data from larger drones may test a restricted scaling hypothesis, but cannot by themselves validate this vehicle.

The proposed dataset needs these items together:

| Item | Why it matters |
|---|---|
| Independently measured total thrust, with calibration and uncertainty | Tests whether wake strength follows actual force. Inferring both from the same flow measurement would make the comparison partly circular. |
| Spatial mean airflow, measurement locations, averaging intervals and repeated observations | Tests the wake's shape as well as its overall strength. A single airspeed number cannot expose a shifted or asymmetric wake. |
| Motor commands and measured rotor speeds, plus supply state | Distinguishes fixed command, fixed speed and controlled hover. They are different experimental conditions. |
| A symmetric baseline, a lower symmetric condition, and an unequal-command condition matched in total thrust | Separates changes in total strength from changes in spatial shape. Select the held-out commands using thrust-only information before inspecting their flow. |
| A fully settled all-off background | Checks the baseline and zero powered-source limit. This does not test shutdown transients. |
| Sensor/registration uncertainty, exclusions and repeatability | Allows differences to be judged against measurement limits. Missing regions must remain missing. |
| Raw or sufficiently resolved reusable observations and explicit reuse terms | Makes the result independently auditable and publishable. A paper's access license does not automatically license an unlocated raw dataset. |

A useful incoming record would identify each run, hardware/actuator condition, timestamp or averaging interval, measurement position, measured thrust and flow components, commands/RPM/supply, uncertainty interpretation and calibration reference. Units, coordinate axes, missing values and any correlations need definitions. Keep licensing and dataset-version provenance with the observations.

This is a data requirement, not a preregistered executable experiment. Actual conditions, repeats, uncertainty analysis and an application-based adequacy tolerance still need to be fixed before examining held-out flow. No apparatus was purchased, author contacted, physical dataset acquired, or model fitted. The verified references and their limits are in EVIDENCE-AND-NEXT-TEST.md. The current data gap remains unresolved.
