# Receiver-data compatibility challenge

Date: 2026-10-16. Static review of `/tmp/m31-receiver-data-followup.md`, retained UIUC methods/index/coefficient files, ENOLA README/CSV headers, Delft schema/script/README, and the original M28 `aero.cjs` and nominal-actuator definitions. No fitting, numerical scientific evaluation, downloads, module execution, old-run repeat, author contact or repository edit occurred.

**Decision:** none of these releases directly validates or falsifies the original M28 nanoquad receiver closure under its intended actuator condition. A separate, explicitly labeled single-propeller transfer comparison is scientifically useful; UIUC is the clearest first candidate. It must not be sold as unchanged-M28 validation. First resolve the baseline/control mapping and define the measured observable and uncertainty criterion; do not produce an accuracy score yet.

## What the model actually asserts

M28 uses rotor radius0.023m, area A=pi*R² and fixed density1.225kg/m³. Its nominal state f0 is a thrust in newtons, driven by `df0/dt=(command−f0)/0.04`; it is not an RPM, PWM, voltage or power state. At each instant the inflow correction is algebraic. The40ms constant therefore belongs to the nominal command-state lag, not a measured wake-response delay.

For f0>0 and U>=0, define vi0=sqrt(f0/(2rhoA)) and T=f0*x. The cubic imposes

`x³+(U/vi0)x−1=0`, equivalently

`P*(T,U)=T[U/2+sqrt(U²/4+T/(2rhoA))]=f0*vi0`.

Writing the ideal induced velocity as `vi=sqrt(U²/4+T/(2rhoA))−U/2`, P*=T(U+vi). Thus this is **ideal actuator-disk power including TU**, not merely T*vi, and not measured electrical or shaft power. Constant RPM, constant throttle, constant shaft power and constant P* are distinct conditions. Holding measured shaft power constant would still require an explicit loss-model assumption to identify it with constant P*.

The physically unresolved bridge is which real motor/ESC operating condition holds nominal f0 fixed and makes P* approximately invariant as external airflow changes. The code does not supply that bridge. Any single-propeller test must distinguish failure of that closure from failure of a separately introduced RPM/PWM/power mapping. Do not redefine f0 separately from each observed inflow thrust: that can make the comparison circular.

Also distinguish rotor diameter2R from M28's motor-spacing length `motorDistance`. Propeller coefficients use rotor diameter, never the quadrotor's opposite-motor spacing.

## What each dataset can test

| Data | Compatible measured targets | What a discrepancy could establish | What remains unsupported |
|---|---|---|---|
| [UIUC GWS axial runs](https://m-selig.ae.illinois.edu/props/volume-2/propDB-volume-2.html) | CT(J), CP(J) for a stated specimen and prescribed-RPM run; static CT0/CP0 versus RPM | A preregistered transfer of the constant-P* thrust curve to this GWS propeller at prescribed RPM fails; measured power coefficients also constrain any proposed shaft-power interpretation | Original46mm hardware, fixed-command closure, transient response, spatial downwash or quadrotor moments |
| [ENOLA MS1101](https://doi.org/10.5281/zenodo.20111572) | T(U,n), Q(U,n), and shaft power2*pi*n*Q from genuine experimental rows | Once control and matched baselines are established, a specified279.4mm-propeller closure or power/loss assumption fails | An unidentified sweep is not a fixed-command or constant-power experiment; scalar normalization does not remove geometry/Reynolds differences |
| [Delft wind-tunnel release](https://doi.org/10.4121/8bcecbac-5478-4595-b629-4378feac6dcb) | RPM, voltage, current and imposed airspeed within documented throttle segments | With verified segment/control labels, whether electrical power or RPM remains constant under that control | No measured thrust or shaft torque, hence no independent T(U) or P*(T,U) test. VI*0.874 is an assumed efficiency conversion, not torque ground truth |

UIUC's Crazyflie entries are static-only. They cannot identify the response to U; setting f0 from static thrust makes T(0)=f0 true by construction. Similar diameter or a familiar brand does not establish the exact M28 propeller/drive identity. ENOLA's dimensional channels are valuable, but its CFD/BEM outputs must not be substituted for measured loads. Delft BEM or inversion of the tested law cannot manufacture an independent thrust target.

There is a useful coefficient-only route for UIUC, narrower than dimensional reconstruction. For positive thrust, the ideal power coefficient implied by measured CT and J is symbolically

`CP* = CT [J/2+sqrt(J²/4+2CT/pi)]`.

It can be compared with measured CP as an **explicit shaft-power/idealization diagnostic**, without requiring dimensional density/RPM conversion. Equality is not an assertion the M28 source independently makes about a real shaft. An unexplained CP−CP* difference cannot by itself falsify M28's conditional cubic; profile, swirl and other losses matter.

For a genuinely matched RPM/density baseline, a proposed fixed-RPM transfer uses `x=CT/CT0` and `U/vi0=J*sqrt(pi/(2CT0))`. This removes dimensions but does not remove the actuator substitution or Reynolds/specimen effects. The released static sweep is not at exactly the axial run's nominal RPM, and the axial table lacks per-row RPM. A fixed, uncertainty-aware baseline/interpolation rule is therefore needed before this becomes a numerical prediction. Do not choose that rule to improve inflow agreement.

Negative measured thrust at sufficiently large advance ratio cannot be represented by M28's strictly positive solution for f0>0. It marks a limitation of extending this closure to that operating regime, especially under fixed RPM; it does not isolate a defect under a different constant-power control. Declare the target regime prospectively and report out-of-regime rows explicitly, rather than removing inconvenient results after scoring.

## Metadata still needed

- **M28 physical bridge:** exact46mm propeller specimen/model, pitch/blade geometry, motor/ESC, voltage and command semantics; independent zero-inflow command-to-thrust baseline; whether f0 means fixed RPM, fixed electrical command or an abstract regulated power. No RPM map should be inferred merely from the presence of kf/km constants.
- **All comparisons:** airflow direction relative to thrust/rotation; U measured as external upstream flow rather than total induced disk velocity; flow uniformity, blockage/support corrections, force and torque zero/tare, repeated-run independence, sensor uncertainty and operating regime. Uniform tunnel flow is a limited receiver test, not validation of a nonuniform neighbor wake sampled at rotor points.
- **UIUC:** same-specimen static/axial association and the baseline at the selected RPM; actual per-point RPM/control tolerance and environmental variation if claiming dimensional T; geometry uncertainty and consistent use of the reported true2.55in diameter; relevant load/flow uncertainty and tare provenance. Calibration-slope repeatability<=1% is not total measurement uncertainty. Public access/citation instructions do not settle the dataset reuse license.
- **ENOLA:** each row's commanded/controlled variable, run/repeat grouping, pairing of static and axial conditions, sign conventions, density, calibration/tare and wind-tunnel correction provenance. Hover-bench methods do not establish these wind-tunnel details. CQ=NaN does not erase the reported dimensional Q, but CT/CP derived from the same sensors are not independent confirmations. Keep the flagged malformed/duplicated files excluded until explicitly resolved.
- **Delft:** correspondence between recorded samples and fixed-throttle commands, plus independently measured loads if it is ever promoted from actuator evidence to receiver-load evidence. The retained schema has no command, T or Q channel.

## Recommended next action

Prepare a small compatibility manifest and preregistration for **“GWS single-propeller fixed-RPM transfer of an ideal-disk thrust-loss curve.”** State the hardware/control change explicitly. Use only an independently established static baseline and the specified rotor geometry; freeze selection, interpolation and uncertainty propagation before scoring inflow rows. The inspected15030RPM curve is exposed development evidence. Any confirmation should use a numerically uninspected, prospectively selected run/specimen, with no outcome-driven switching.

The primary measurable target should be thrust coefficient versus advance ratio, with CP as a separate power diagnostic. Freeze an adequacy tolerance tied to experimental uncertainty and purpose; the simulator's1e-12N numerical tolerances are irrelevant to measurement agreement. Failure would reject this explicitly stated fixed-RPM transfer; agreement would support that finite hardware/regime only. Neither outcome directly settles the M28 fixed-command nanoquad closure.

For a **direct** M28 physical challenge, prioritize measured steady T and external U for the identified46mm rotor/drive at a documented fixed command and matched zero-flow baseline, logging n, Q, voltage and current to diagnose actuation and power changes. A shaft-power-regulated experiment answers a separate hypothesis. Do not regulate the inferred P* using the measured thrust and then claim its constancy independently validates the law. Steady single-propeller data cannot validate the40ms command dynamics, yaw policy, roll/pitch moments from unequal rotor loads or swarm trajectories.

Accordingly, a prospective measurable comparison is justified as a narrow model-transfer challenge. No available candidate currently justifies labeling the original receiver model physically validated, and no fitting or new computation is recommended before the observable/control/baseline metadata is fixed.
