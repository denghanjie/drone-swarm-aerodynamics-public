# Milestone 27 — sensitivity to aerodynamic assumptions

Generated: 2026-10-12T01:08:08+00:00 (UTC).

**Status: terminated after verified geometry error; completed and partial files preserved.**

## Identified implementation error

**The active-airflow results below use the wrong wake length scale:** adjacent rather than opposite motor spacing. Sources and runs are retained as an error record. The corrected paired rerun is milestone28. Airflow-off results are unaffected. See [correction audit](research-wake-normalization-correction.md).

## Question

With the same local flocking rules and starting positions, how much do different assumed aerodynamic loads change passage, contacts, connectedness and control demand? This is a sensitivity study. It does not establish which aerodynamic model is accurate.

## Four assumptions

- **Off:** no aerodynamic interaction between drones.
- **Sum, force only:** prescribed mean downwash contributions add linearly. A constant ideal induced-power response reduces each receiver rotor’s effective lift, but nominal body moments are retained.
- **Sum, rotor moments:** the same inflow and lift response also add roll/pitch moments from unequal rotor lift. Nominal yaw torque is retained.
- **Alternative overlap:** root-sum-square incoming axial speeds replace the linear sum, with rotor roll/pitch moments. This is an overlap heuristic, not a simulation of turbulence.

The wake profile comes from the previously implemented [Bauersfeld et al. mean far-wake model](https://arxiv.org/abs/2403.13321). Source amplitude is prescribed from isolated hover weight and rotated with source attitude; it is not solved self-consistently from the source’s current effective thrust. Receiver translational relative-flow effects, wake history, confinement/wall effects, ground effect, fluctuations and aerodynamic yaw changes are omitted. A declared near-wake cylinder or tilt beyond 20° triggers a **model-domain exit**, not a physical-contact claim.

## Receiver response and units

For nominal isolated rotor thrust f₀ in newtons, vi₀ = √(f₀/(2ρA)) in m/s and α = U/vi₀. Effective thrust is f₀x, where the unique positive root satisfies x³ + αx − 1 = 0. This holds ideal induced power constant at its instantaneous nominal value. The flight controller can subsequently command more nominal thrust. This is not a calibrated PWM, rotor-speed or electrical-power model.

Unit checks verify the power identity, agreement with the earlier bisection calculation, zero-flow regression, pair symmetry, force/moment accounting, explicit domain exits and spatial-query coverage. They verify implementation, not physical fidelity. The current 27 g vehicle and rotor geometry are retained; independently measured configurations have not been silently substituted.

## Frozen experiment

Twenty primary missions: two fresh 50-drone seeds × two doorway sizes × four assumptions, plus one 200-drone wide-course seed × four assumptions. Four physics-step refinements and one separate field-refresh refinement complete the 25-job protocol. All horizons are 180 s. No gains or geometry are tuned after outcomes.

Primary physics steps are 2.5 ms, with 100 Hz control and wake fields held for 10 ms. Physics refinements use 1.25 ms with the same field cadence. The field-cadence comparison changes only wake refresh from 10 to 5 ms at 1.25 ms physics. Source and receiver states update synchronously at field refresh; rotor lift responds to the nominal motor state at RK stages.

Positions and quaternions stream as Float64LE every second and at terminal state. Scientific samples remain every 0.1 s. Visual interpolation has no role in contact detection. The 0.075 m body envelope is conservative geometry, not resolved rotor contact.

## All planned outcomes

|Drones|Seed|Doors|Airflow|Kind|Finished|Stop|End s|Minimum connected fraction|
|---:|---:|---|---|---|---:|---|---:|---:|
|50|1601|wide|off|primary|50/50|none|180.0000|1.0000|
|50|1601|wide|sum-force|primary|50/50|none|180.0000|1.0000|
|50|1601|wide|sum-rotor|primary|0/50|obstacle contact envelope|11.9275|1.0000|
|50|1601|wide|rss-rotor|primary|0/50|obstacle contact envelope|11.1800|1.0000|
|50|1601|narrow|off|primary|50/50|none|180.0000|1.0000|
|50|1601|narrow|sum-force|primary|50/50|none|180.0000|1.0000|
|50|1601|narrow|sum-rotor|primary|0/50|obstacle contact envelope|11.2825|1.0000|
|50|1601|narrow|rss-rotor|primary|0/50|obstacle contact envelope|11.9525|1.0000|
|50|1602|wide|off|primary|50/50|none|180.0000|1.0000|
|50|1602|wide|sum-force|primary|50/50|none|180.0000|1.0000|
|50|1602|wide|sum-rotor|primary|0/50|vehicle model limit|11.3625|1.0000|
|50|1602|wide|rss-rotor|primary|0/50|aerodynamic model domain|11.3900|1.0000|
|50|1602|narrow|off|primary|50/50|none|180.0000|1.0000|
|50|1602|narrow|sum-force|primary|50/50|none|180.0000|1.0000|
|50|1602|narrow|sum-rotor|primary|0/50|obstacle contact envelope|11.0225|1.0000|
|50|1602|narrow|rss-rotor|primary|0/50|obstacle contact envelope|11.0325|1.0000|
|200|1601|wide|off|primary|200/200|none|180.0000|1.0000|
|200|1601|wide|sum-force|primary|0/200|vehicle model limit|2.9300|1.0000|
|200|1601|wide|sum-rotor|primary|0/200|vehicle model limit|4.0200|1.0000|
|200|1601|wide|rss-rotor|primary|0/200|aerodynamic model domain|3.1100|1.0000|
|50|1601|wide|off|refinement|interrupted; not a completed result|—|—|—|
|50|1601|wide|sum-force|refinement|not run after error identification|—|—|—|
|50|1601|wide|sum-rotor|refinement|not run after error identification|—|—|—|
|50|1601|wide|rss-rotor|refinement|not run after error identification|—|—|—|
|50|1601|wide|sum-rotor|cadence|not run after error identification|—|—|—|

A single contact/domain exit stops the run. Other unfinished drones must not be counted as separate failures. Reaching the horizon without contact is distinct from every drone finishing.

## Numerical comparisons

The remaining erroneous-model refinements were terminated or not run after the source audit. No numerical-refinement result is inferred. All25 corrected cases remain prescribed in milestone28. [Termination record](milestone-27-termination.json).

[Supplemental event identities](milestone-27-event-comparisons.json) retain the affected drone, pair, obstacle or model-domain reason separately from the frozen joint criterion. Matched initial states are checked by the artifact audit.

## Control demand and computation

`aeroStats.nominalIdealEnergyJ` integrates the isolated-rotor ideal induced power implied by nominal motor states. It is not battery energy. Raw totals from runs that stop at different times must not be interpreted as an efficiency ranking. Maximum incoming speed and interaction-query counts are also retained. The inherited `maxTiltDegrees` metric is the maximum absolute roll or pitch coordinate angle; it is not the combined body-axis tilt. The20° model-domain check uses the body thrust-axis angle from vertical.

These jobs run serially within this study but may overlap milestone26. Their wall times are descriptive, not an isolated aerodynamic performance benchmark. The baseline serial computation/rendering evidence remains in milestone25. A separate isolated overhead benchmark is still required for a fair runtime comparison between aerodynamic models.

## Physical validation and interpretation

The [comparison contract](research-aerodynamic-comparison-contract.md) separates assumed-model sensitivity from independent validation. Raw force/wake observations have not been acquired. The fixed-supply/PWM experiment, receiving-rotor response, geometry normalization, wall effects and multiple-wake assumptions are not validated by agreement between these implementations. No physical-accuracy, real-flight-safety, turbulent-flow or novelty claim follows from these runs.

## Records

[3D replay](milestone-27-lab.html) · [Frozen protocol](milestone-27-protocol.json) · [Completed runs](milestone-27-progress.json) · [Aerodynamic implementation checks](milestone-27-aero-verification.json) · [Zero-flow/coupling development checks](milestone-27-coupling-development.json) · [Domain-exit recording checks](milestone-27-domain-verification.json) · [QA](milestone-27-qa.md). Raw states, samples and binary replays are under `milestone-27-source/`.
