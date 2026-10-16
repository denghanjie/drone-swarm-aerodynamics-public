# One next receiver-reference question using retained UIUC data

2026-10-16. Private source/baseline assessment only. No external search, new primary-page request, payload acquisition, model evaluation, curve score, fitting or scientific execution. No public file was edited.

**Recommendation:** the retained UIUC GWS Direct Drive 2.5×0.8 run can support one separately authorized **descriptive coefficient-transfer evaluation**, conditional on a frozen RPM-setpoint-to-baseline bridge and an explicit interpolation sensitivity. Full measurement uncertainty is not required to describe computed discrepancies; it is required for stronger significance, adequacy or physical-validation claims. No such claims or physical pass threshold are justified here.

This is a new operationally specified question using old, exposed evidence—not a new dataset, a blinded confirmation, or a reopening of a completed scientific run. The genuinely new step is to fix the baseline rule and its sensitivity before computing the transfer. It does not resolve the intended 46 mm vehicle's command mapping. **No executable admission or execution allocation is granted by this memo.**

## Definitions that govern the comparison

The additive `CONTROL-CONDITION-CORRECTION.md` was read first. The frozen receiver law holds nominal thrust state `f0` and therefore its model-defined ideal actuator-disk power `f0 sqrt(f0/(2 rho A))`. It does not identify that quantity with fixed RPM, shaft power, electrical power or PWM.

Declare a separate physical bridge for this descriptive transfer:

`c = prescribed rotor-speed setpoint N* = 15030 RPM`

`f0 = T0(c)`

At a common reference density and speed, write the bridge as

`f0 = rho_ref (N*/60)^2 D^4 C0`.

`C0` is established only from the retained static sweep through the rule below, before any transfer computation. It is never redefined from each inflow thrust. This is a proposed bridge, not an independently proven property of RPM regulation. Applying the cubic at fixed `f0` under that bridge tests **receiver law plus bridge**. A discrepancy cannot identify either component as the unique cause.

The coefficient comparison avoids inventing dimensional density or force values. It is the explicit transfer

`alpha_i = J_i sqrt(pi/(2 C0))`

`x_i^3 + alpha_i x_i - 1 = 0`, with the positive root

`CT_pred,i = C0 x_i`.

Interpreting `x_i` literally as a dimensional thrust ratio additionally requires compatible actual rotational speeds and densities. The released axial file supplies neither per-row RPM nor density. Thus this is a nominal-speed coefficient transfer, not an exact reconstruction of the original dimensional experiment. Do not quietly restore those missing values by assuming perfect regulation or a universal density.

## Exact retained reference and minimum comparison

Use the one already exposed axial file `uiuc-gws-15030.txt` corresponding to [GWS 0503rd, nominal 15030 RPM](https://m-selig.ae.illinois.edu/props/volume-2/data/gwsdd_2.5x0.8_0503rd_15030.txt), with its existing 14 records. Preserve the entire run and original row numbering. Do not choose two favorable inflows, switch specimen, add another RPM curve, or select points from residuals. The file contains more than the required two nonzero-inflow observations.

Its zero-flow reference is the separate [static 0500rd sweep](https://m-selig.ae.illinois.edu/props/volume-2/data/gwsdd_2.5x0.8_static_0500rd.txt), retained as `uiuc-gws-static.txt`. The saved [Volume 2 index](https://m-selig.ae.illinois.edu/props/volume-2/propDB-volume-2.html), lines 365–370, places both links in the same first GWS 2.5×0.8 block, followed by explicitly separate specimen-2 and specimen-3 blocks. This supports the database association; it is not an independently inspected physical specimen log. There is no exact static observation at the nominal axial RPM.

Freeze these static anchors from data rows 13 and 14 (file lines 14 and 15):

| Anchor | RPM | CT |
|---|---:|---:|
| Nearest lower RPM | 15006.667 | 0.061549 |
| Nearest higher RPM | 15960.000 | 0.062855 |

The selection rule is nearest strictly lower/higher **RPM**, not row adjacency or convenient coefficient values. Earlier static rows are not perfectly sorted in RPM. The baseline is

`C0_linear = C_L + (15030 - N_L)/(N_H - N_L) × (C_H - C_L)`.

No interpolated value has been calculated in this task. Freeze three scenarios: the linear baseline, the lower-RPM anchor coefficient, and the higher-RPM anchor coefficient. Evaluate the same complete axial run under each. The endpoint scenarios describe sensitivity to the baseline choice; they are **not confidence limits or guaranteed bounds** on the true baseline. They do not cover calibration error, unknown speed/density variation, Reynolds effects, systematic tare or tunnel-correction error.

The smallest useful output is one private rowwise discrepancy table and one compact summary of how it changes across the three predeclared baselines. Retain all original rows. Tag observed nonpositive-thrust records as outside the positive-thrust comparison regime; do not delete them or silently reinterpret them as direct failures of a differently controlled physical system. Report any in-domain summary with its explicit membership rule, and avoid pooling out-of-domain rows into an unexplained headline score. No model fit, correction curve, tuned baseline, timing study or new specimen is needed.

All target values were exposed in prior work. During this assessment the existing axial file was reread with the static file before the parent's subsequent metadata-only steering; no target values were used to choose conditions and no curve was scored. The whole-run selection prevents a fresh convenient-point choice. No further target-value inspection followed that steering.

## What the primary methods establish

Deters, Ananda and Selig, *Reynolds Number Effects on the Performance of Small-Scale Propellers*, AIAA 2014-2151, [DOI 10.2514/6.2014-2151](https://doi.org/10.2514/6.2014-2151), was reread from its retained [author-hosted paper](https://m-selig.ae.illinois.edu/pubs/DetersAnandaSelig-2014-AIAA-2014-2151.pdf), §§II-A–E, pp. 2–5. It documents load-cell thrust, separate torque sensing, optical RPM, ESC actuation, prescribed-RPM advancing-flow tests, and separately measured static performance. Sub-9-inch propellers use the Medusa MR-012-030-4000 motor and Phoenix 10 ESC. The full controller implementation and per-row speed history are absent from the retained coefficient file.

The paper defines `CT`, `CP`, `J` and shaft power convention explicitly. It describes weight-based load calibration, roughly ≤1% calibration-slope changes, and less-than-1% speed changes during sequential RPM/load acquisition. Neither statement is a total uncertainty bound. Fairing and test-section corrections are applied; the latter uses thrust in the velocity correction, so errors in published `J` and `CT` need not be independent. This does not make the measured thrust an output of our cubic, but it prevents treating the published axes as independent exact observations.

The inherited geometry read reports true diameter 2.55 inches. The coefficient-only calculation needs no invented dimensional conversion; any later dimensional bridge must use consistent actual geometry and coefficient convention, not the nominal product label or quadrotor motor spacing.

## Interpretation and public reporting boundary

A finite descriptive calculation can answer how the proposed transferred curve differs from the published coefficients, and whether that description materially changes under the three baseline choices. It cannot produce a statistically calibrated rejection, physical adequacy verdict, confidence interval, or validation of the frozen M28 receiver. A useful result may simply show that the conclusion is sensitive to baseline choice; that is still an informative result. No acceptance threshold should be borrowed from numerical f32 gates or from the paper's calibration-slope statement.

The method does not assert fixed shaft power or ideal-power invariance in the apparatus. Report the control as prescribed RPM, with the bridge explicitly added by us. The result concerns the particular GWS propeller and nominal control condition. It supplies no 46 mm rotor/ESC identification, fixed-PWM response, transient time constant, spatially nonuniform receiver loading, vehicle moments or swarm qualification.

The retained records establish public download access and citation instructions, but no explicit dataset redistribution license. This does not require presenting a factual descriptive result as impossible. A public derived summary can avoid distributing the source files: publish the proposed method, original source links and hashes, aggregate discrepancy/sensitivity findings, exposure and uncertainty limitations. Keep the complete source tables, full methods PDF and rowwise derived table private. Do not publish a full per-row residual series with all predictors if it effectively reconstructs the raw coefficient table. Do not assert that a transformation automatically grants a redistribution license. No publication action is part of this task.

This route serves the broader accuracy-versus-computation goal by first defining a physical discrepancy question under an honest control mapping. It does not validate a new aerodynamic field or justify another GPU/5,000-drone benchmark. The original source/receiver coupling objective remains open.

## Scope and disposition

Existing UIUC admission records were inspected before deciding whether discovery was useful. No search was needed: all necessary inputs for the **declared descriptive transfer** are already retained. The narrower question above avoids reopening the old UIUC data routes or treating missing full uncertainty as permission for a validation claim.

Recommended next action for the parent is to consider a separately bounded, frozen one-run/three-baseline descriptive evaluation. Keep direct M28 physical qualification unadmitted. No experiment, data acquisition, implementation or execution is authorized by this report. Detailed bibliography, local hashes, existing-file access and zero-new-network accounting are in the accompanying files.
