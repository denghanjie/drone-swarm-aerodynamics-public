# M31 receiver-load data follow-up

Audit date: 2026-10-16. Scope: three independent public candidates for numerical thrust/torque versus imposed axial airflow. This was a source/schema inspection only: no model fitting, simulation, benchmark, author contact, paid access, or challenge bypass. Brown DOI retrieval and excluded Neural-Swarm telemetry were not revisited.

**Decision:** UIUC supplies the best verified small-propeller axial coefficient target, but its Crazyflie data are static-only and its GWS runs use prescribed RPM. ENOLA supplies openly licensed dimensional axial thrust/shaft-torque CSVs for much larger rotors, with provenance gaps and specific metadata defects. TU Delft documents fixed-throttle axial tests particularly clearly, but its released wind-tunnel data contain no measured thrust or moment. None directly validates the M28 ideal constant-induced-power receiver law, its 40 ms response, or quadrotor roll/pitch moments in spatially varying downwash.

| Candidate | Verified measurement target | Present status |
|---|---|---|
| UIUC Propeller Database, Vol. 2 | GWS 2.5×0.8, actual diameter 2.55 in, axial `J, CT, CP, eta` | Best small-rotor coefficient target; actuator and geometry adaptation required; reuse terms unresolved |
| ENOLA, Zenodo v1 | T-Motor MS1101, 279.4 mm diameter, axial `RPM, V, J, THRUST, TORQUE, CT, CQ, CP` | Numeric dimensional loads accessible under CC BY-SA 4.0; per-run actuator/calibration/tare provenance incomplete |
| TU Delft propeller_airspeed_sensor | 8 in system, fixed throttle, axial electrical/rotational feedback | Reject as receiver-load ground truth: no force or moment channel |

## 1. UIUC: small propeller axial coefficients, not Crazyflie inflow data

Primary data: [Volume 2](https://m-selig.ae.illinois.edu/props/volume-2/propDB-volume-2.html), compiled by Robert Deters, version dated 2015-05-27. Its Crazyflie Nano Quadcopter tractor/pusher 1.85 in entries, two specimens each, list geometry and **static** files only. The GWS Direct Drive 2.5×0.8 entries have wind-tunnel runs for three specimens. Specimen 1 lists 15030, 20016, 25063 and 25050 RPM. These index labels are not per-row motor telemetry.

Files actually inspected:

- [Axial run, 15030 RPM](https://m-selig.ae.illinois.edu/props/volume-2/data/gwsdd_2.5x0.8_0503rd_15030.txt): whitespace-delimited header `J CT CP eta`; 14 numerical rows. Endpoints are `(0.074376, 0.054228, 0.026204, 0.153921)` and `(0.564756, -0.046209, 0.009510, -2.744405)`.
- [Static sweep](https://m-selig.ae.illinois.edu/props/volume-2/data/gwsdd_2.5x0.8_static_0500rd.txt): `RPM CT CP`, 24 rows, approximately 3057–25987 RPM. This supplies a separate zero-inflow reference sweep, not identical pointwise RPMs.
- [Geometry table](https://m-selig.ae.illinois.edu/props/volume-2/data/gwsdd_2.5x0.8_geom.txt): `r/R c/R beta`; 18 radial stations. The [geometry plot](https://m-selig.ae.illinois.edu/props/volume-2/plots/gwsdd_2.5x0.8_geom.png), visually inspected, explicitly reports **true diameter 2.55 in (6.5 cm)**. Do not substitute the nominal 2.5 in diameter in coefficient conversion.

Primary methods: R. W. Deters, G. K. Ananda and M. S. Selig, *Reynolds Number Effects on the Performance of Small-Scale Propellers*, AIAA 2014-2151, [DOI 10.2514/6.2014-2151](https://doi.org/10.2514/6.2014-2151), [author-hosted PDF](https://m-selig.ae.illinois.edu/pubs/DetersAnandaSelig-2014-AIAA-2014-2151.pdf), §§II.A–F, pp. 2–8. The following methods summary is limited to what that paper establishes:

The computer commands an ESC through a modified ServoXciter; optical blade-passage sensing measures RPM. Advancing-flow tests set RPM and increase tunnel speed. For sub-9-in propellers, the drive is a Medusa MR-012-030-4000 motor and Phoenix 10 ESC. Thrust uses a pendulum/load-cell balance; shaft reaction torque uses a separate transducer. Precision weights calibrate thrust through a pulley and torque through a moment arm; calibration-slope changes were typically ≤1%. RPM sampling precedes simultaneous load/environment sampling, with reported speed change below 1% over those acquisition periods. The paper applies fairing and closed-test-section flow corrections. It defines `J=V/(nD)`, `CT=T/(rho*n^2*D^4)`, `CP=P/(rho*n^3*D^5)`, and `P=2*pi*n*Q`. A separate aerodynamic tare/zero-removal procedure was not established in the inspected paper. Prescribed RPM should not be described as fixed PWM or constant power; the released table does not expose the complete feedback/controller implementation.

**Use boundary:** these are reduced experimental coefficients, not raw load-cell time histories. They can support a steady, uniform-axial-flow coefficient comparison after explicitly choosing a compatible actuator/propeller model. Exact dimensional reconstruction also needs density and per-point rotational speed, absent from the four-column file. The torque is about the propeller shaft; it is not a measured quadrotor roll/pitch moment. M28 uses 46 mm diameter rotors and a different actuator law, so an agreement or discrepancy here cannot be labeled direct Crazyflie/M28 physical validation.

**Reuse:** accessible downloads and citation instructions were found, but no explicit propeller-dataset reuse license was identified in the inspected UIUC pages/files. Do not import a license from the separate UIUC airfoil database. The dissertation landing page is public, but its direct PDF request returned HTTP 403; no bypass was attempted, and no uninspected thesis detail is asserted.

## 2. ENOLA: open dimensional loads, larger hardware and metadata gaps

Primary record: Universitat Politècnica de València, *ENOLA numerical and experimental propeller database*, v1, 2026-05-10, [DOI 10.5281/zenodo.20111572](https://doi.org/10.5281/zenodo.20111572). The [public API](https://zenodo.org/api/records/20111572) explicitly identifies `cc-by-sa-4.0`; the [project release announcement](https://enola.webs.upv.es/blog/2026/prop-database/) agrees. The record also states its research/educational intended scope. Experimental files must be separated from the numerical BEM/CFD files in the same archive.

The 223,601,320-byte ZIP has recorded MD5 `245267e590546f160f3b971d7f8e05fb`. Its [native preview](https://zenodo.org/records/20111572/preview/Propeller_Database.zip?include_deleted=0) exposes the manifest. Only its 65,557-byte tail and ten selected small members were fetched through ordinary HTTP 206 byte ranges; selected members passed ZIP CRC verification. The full archive was not downloaded, so its full-archive MD5 was not independently recomputed.

**Best clean inspected slice:** `BBDD/T-Motor/MS1101/results/MS1101_exp_0deg.csv`.

- `00_Generalnfo.xlsx` gives MS1101 diameter **0.2794 m**. Its README identifies the original commercial propeller, experimental measurements at CMT's wind tunnel, and angles measured from the rotation axis: 0° means axial flow.
- UTF-8 BOM CSV, 62 data rows, exactly eight columns: `RPM,V[m/s],J,THRUST[N],TORQUE[Nm],CT,CQ,CP`. Recorded RPM spans 1453–6483; wind speeds are 0, 5 and 10 m/s. `CQ` is `NaN` in the inspected rows. No PWM, voltage, timestamps, calibration coefficients, or uncertainty columns occur in this file.
- Example static row: `1457,0,0,0.2760,0.004465,0.06342,NaN,0.02310`. Example axial row: `1784,5,0.6144,-0.3448,0.003101,-0.05365,NaN,0.01089`. These are individual observations, not a matched-RPM pair.

**Actuator/calibration/tare boundary:** the [official 2024 test-bench description](https://enola.webs.upv.es/blog/2024/prop_bench/) documents a custom force/moment balance, NI acquisition, a speed sensor, microcontroller-to-ESC throttle commands, and redundant telemetry. It does not establish whether these particular CSV sweeps held throttle, RPM, or power fixed. The [ICAS 2024 paper](https://www.icas.org/icas_archive/icas2024/data/papers/icas2024_0896_paper.pdf), §2.3 and §3, documents weight calibration, optical tachometry and repeated measurements for an **anechoic hover** setup. That is not sufficient evidence of calibration/tare policy for the later MS1101 wind-tunnel CSV. Exact per-run policy, support-drag tare and correction provenance remain open; do not silently transfer methods between setups.

**Specific data defects discovered:**

- AeronautCAM9x5 is a smaller **0.2286 m** alternative with 234 experimental data rows. Its header merges `THRUST[N]u_THRUST[N]`, giving 10 header fields versus 11 numeric fields. The likely missing comma is apparent, but the file must be explicitly repaired and uncertainty semantics checked before use.
- `Custom/Casalino/results/Casalino_SLA_exp_0deg.csv` contains inflow entries around **14.98°**, despite its filename. The archive directory gives the `0deg` and `15deg` files identical size and CRC. This is a substantive labeling/duplication flag; no 0° claim should be based on that filename.
- The inspected `XOAR9x7_exp_WT.csv` has `V=0` throughout. Its “WT” suffix alone is not proof of an imposed-inflow sweep.

**Use boundary:** the clean MS1101 file is a real axial load target worth retaining, but this is a 279.4 mm rotor, not a nanoquad rotor, and it does not close the actuator or nonuniform-downwash/moment gap. Use a separately documented comparison case only after filling the methods gaps.

## 3. TU Delft: fixed throttle verified, but no force/moment channel

Primary release: E. Ntouros, P. Kelley and E. Smeur, *Data and Code for Unmanned Aerial Vehicles airspeed estimation using propeller feedback*, 2025, [4TU DOI 10.4121/8bcecbac-5478-4595-b629-4378feac6dcb](https://doi.org/10.4121/8bcecbac-5478-4595-b629-4378feac6dcb); [GitHub repository](https://github.com/tudelft/propeller_airspeed_sensor), inspected commit `6db5cc19327f0d6c31a4e51783a442704007dbc3`.

Associated article: Ntouros, Kelley and Smeur, *Airspeed estimation for UAVs using only propeller feedback*, Aerospace Science and Technology 168 (2026), 110999, [DOI 10.1016/j.ast.2025.110999](https://doi.org/10.1016/j.ast.2025.110999). Accessible primary methods were read in [arXiv v1, §III.c](https://arxiv.org/html/2507.03456v1): axial tunnel flow at 10, 15 and 18 m/s; constant throttle commands from 10% to 80%; rotational speed limited to 10,000 RPM. These are fixed-throttle conditions, not fixed-RPM conditions. The article estimates mechanical propeller power from electrical input using an efficiency inferred using BEM/flight data; this is not a torque-transducer calibration.

Actual [input `wt.mat`](https://github.com/tudelft/propeller_airspeed_sensor/blob/6db5cc19327f0d6c31a4e51783a442704007dbc3/data/input/wt.mat), 1,991,327 bytes, was inspected as a MATLAB v5 structure. `data` contains exactly `airspeed`, `rpm`, `voltage`, `current`, `t` (each 254500×1 double) and scalar `fs=500` (uint16). **No thrust, shaft torque, force or moment measurement is present.** The [WT script](https://github.com/tudelft/propeller_airspeed_sensor/blob/6db5cc19327f0d6c31a4e51783a442704007dbc3/src/airspeed_fit_WT.m) uses diameter `8*0.0254` m and derives power as `voltage.*current*0.874`; its analysis filters out low-power, transient, high-RPM and low-J portions. The script was read, never executed.

The README explicitly places non-code files under CC BY 4.0 and source code under GPL-3.0. License scope is therefore clear even though GitHub's metadata returned no single detected license. This is useful actuator/power evidence, **not independent measured receiver-load ground truth**. Neither `BEM.mat` nor intermediate `data/Jcrit/wt.mat` should be substituted for measured thrust.

## Audit handoff

Supporting downloads, original selected ENOLA members, the remote ZIP directory manifest, extracted paper text and inspected Delft MAT schema are retained in `/tmp/m31-receiver-audit/`. The audit found partial targets rather than demonstrating that no suitable dataset exists. The practical next decision is whether to authorize a separate steady single-propeller validation case with compatible RPM control, or continue searching specifically for measured nanoquad fixed-command loads under imposed airflow. It is not yet justified to mark the M28 receiver law physically validated.
