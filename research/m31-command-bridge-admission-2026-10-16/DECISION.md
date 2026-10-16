# A fixed-command experiment is documented; numerical scoring is deferred

The finite search found a more suitable control condition than the exposed GWS prescribed-speed transfer. NASA/TM-20210014010 is admitted as a **methods reference**, conditionally promising for a separate test of `f0=T0(PWM)`. Traceable numerical baseline/target records have not been acquired, so no new prediction, residual, fit or physical-validation claim is admitted.

## Verified source facts

Simmons and Hatke (May 2021), *Investigation of High Incidence Angle Propeller Aerodynamics for Subscale eVTOL Aircraft*, [NASA/TM-20210014010](https://ntrs.nasa.gov/citations/20210014010), is a public technical memorandum. Its author-uploaded [methods §§3.1–3.5](https://www.researchgate.net/publication/351477086_Investigation_of_High_Incidence_Angle_Propeller_Aerodynamics_for_Subscale_eVTOL_Aircraft) describe 16-inch three-bladed propulsion units, different CW/CCW variants, direct balance loads, recorded PWM/RPM, fixed PWM and pressure within incidence sweeps, and static/positive-pressure cases sharing command levels. Table 2 gives balance accuracy relative to maximum loading. Warmup, zero drift, and model-informed retesting/replacement are disclosed.

The related Simmons paper, *System Identification for Propellers at High Incidence Angles*, [Journal of Aircraft 58(6), 2021](https://doi.org/10.2514/1.C036329), was consulted in its [NASA accepted manuscript](https://ntrs.nasa.gov/citations/20210024634). Section III corroborates the experimental controls; §§IV-E/V-A distinguish the steady motor mapping from aerodynamic response. Its fitted model and reported validation summaries are not newly acquired independent thrust measurements for our test.

## Our interpretation and useful design consequence

This establishes that a suitable *kind* of fixed-command experiment exists. It does not establish compatibility with our original 46 mm vehicle. Keep one CW variant, one PWM command and axial inflow; do not pool CW/CCW or interpret the reported supply description as measured constant electrical current/power. A larger propulsion unit can challenge a declared transfer hypothesis, with its actual hardware scope stated.

For our ideal-disk equation, define `vi0 = sqrt(T0/(2*rho*A))`, `alpha = U/vi0`, and measured dynamic pressure `q = rho*U^2/2`. Algebra gives `alpha = sqrt(4*A*q/T0)` for nonnegative axial inflow. This is an exact change of variables under those definitions, not a new experimental finding. It avoids inventing density when compatible pressure and baseline quantities are available. It does not remove their uncertainty, shared-baseline dependence, installation loads or between-run drift.

A potential later test can select CW, axial incidence, PWM 1475, a matched static baseline and pressure settings 0.25/0.5 psf before reading target thrust. These settings identify a prospective small question; no baseline or target thrust was scored here. Nominal pressure settings must remain nominal unless per-point measurements are supplied. Baseline/target matching, pressure/force uncertainty and specimen identity still need admission. An unchanged-static-thrust comparator should be retained alongside the transferred equation.

## Evidence boundary and next action

Direct PDF acquisition of the technical memorandum failed; the author-copy link also failed. Methods remain accessible as author-uploaded text. The smaller accepted manuscript was readable through the web document tool, but its inspected passages/figures concern fitted models and summarized evidence; they are not substitute raw observations. Source access and incidental exposure are recorded in SOURCE-ACCESS.json. Six discovery queries are consumed; no exhaustive search or proof that data do not exist is claimed. No author was contacted, dataset acquired or source figure digitized.

Before scoring, obtain traceable numerical data or adopt a separate figure-extraction protocol with axes, curve identity, extraction limits and exact source provenance. A calibration specification alone cannot supply total experimental uncertainty. Any graphical comparison with incomplete uncertainty must remain descriptive. Do not reuse fitted-model values as independent observations, or call a related paper an independent experimental campaign.

The bounded admission review is complete. It has advanced the control-condition evidence, while numeric access remains unresolved. The existing [Three.js result graph](../m31-gws-receiver-transfer-2026-10-16/viewer/) remains the latest actual-results display. A separate mathematical dependency-structure question is being assessed for future computation research; it has no bearing on physical qualification and no experiment is allocated by this file.
