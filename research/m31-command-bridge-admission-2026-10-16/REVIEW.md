# NASA command-transfer source admission

2026-10-16. **Methods support a promising fixed-PWM transfer candidate; numeric
evidence is not yet admitted for scoring.**

Read the complete §§3.1–3.5 in the author-uploaded full text of Simmons and Hatke,
*Investigation of High Incidence Angle Propeller Aerodynamics for Subscale eVTOL
Aircraft*, NASA/TM-20210014010 (May 2021), available on
[ResearchGate](https://www.researchgate.net/publication/351477086_Investigation_of_High_Incidence_Angle_Propeller_Aerodynamics_for_Subscale_eVTOL_Aircraft).
This was direct methods text, not search snippets. The coordinator separately
verified the [official NASA record](https://ntrs.nasa.gov/citations/20210014010).
Official retrieval failures were not retried. No PDF/data file was acquired,
numerical result figure inspected, target digitized, calculation run, author
contacted or repository edited. This desk task is separate from the closed GWS
campaign and grants no execution permission.

## What the methods establish

The isolated propulsion units use 16-inch, three-bladed folding propellers; the
commercial CW and custom CCW variants differ. A six-component strain-gauge balance
measures loads. PWM and RPM are recorded; operation is described as open loop.
Each incidence sweep holds PWM and dynamic-pressure setting fixed. The test
matrix includes zero and positive pressure at the same PWM levels. Warmup and
balance-zero procedures address thermal/drift effects. Table 2 reports balance
accuracy as 95% intervals relative to maximum loading. The report also describes
model-residual-based identification, retesting and replacement of suspect runs.
Its supply description of 29 V at 32 A is not a published per-point constant-current
or constant-power record. These facts come from the full methods cited above.

## Conditional transfer that this could support

The coordinator's proposed **CW, axial incidence `ip=0`, PWM 1475**, with its matched
zero-flow baseline and the lowest two positive pressure settings, **0.25 and
0.5 psf**, is a small prospectively selected comparison. These are design settings,
not targets scored in this review. Do not pool CW and CCW, substitute their
baselines, or extend the one-dimensional law to oblique/reversed-flow conditions.

Declare `f0=T0(PWM)` as the hypothesis connecting a real command to the nominal
state. Hold the selected measured baseline fixed at both inflows. With the model's
definitions and consistently expressed units, the coordinator's identity
`alpha=sqrt(4*A*q/T0)` removes explicit density from the input calculation. It does
not remove uncertainty in disk area, pressure or baseline, nor establish baseline
invariance under environmental changes. Use actual recorded dynamic pressure if
available; nominal pressure settings must remain explicitly nominal. A setting
converted to airspeed using standard atmosphere is not a per-point measured speed.

Pair baseline and targets by propeller/drive, PWM, axial orientation, supply and
thermal procedures, balance zero and force/coordinate treatment. These are
different runs, so the matching and residual drift cannot be assumed away. Confirm
what background/installation loads remain in the reported axial balance force
before interpreting it as pure rotor thrust. The source provides a direct load
observable, but the bridge remains a testable assumption. Fixed PWM does not
establish fixed RPM, shaft power or ideal disk power; a discrepancy challenges the
law and bridge together.

## Uncertainty and remaining evidence gate

Balance calibration accuracy is not the total uncertainty of `T/T0`. Retain
pressure/angle/geometry uncertainty, run drift, thermal/supply effects, shared
baseline covariance and any extraction error separately. Contiguous filtered
samples are not independent replicates; no SEM follows from sample count alone.
The authors' model-informed run screening must remain visible as data provenance;
do not call the resulting release an untouched blind sample.

The accessible methods do **not** establish an acquired reusable numerical table,
per-point actual pressure/density, baseline/target run identifiers, full zero/tare
records, repeat histories or a complete uncertainty budget. This review did not
search for those items and does not assert that they do not exist. The coordinator
reports the author-PDF click also failed; no second attempt was made here.

Next admission requires either traceable reusable numeric evidence or a separately
declared figure-extraction protocol establishing the selected baseline and targets,
axes/units, curve identity and graphical limits. A plotted line alone must not be
promoted into raw repeated observations. Incomplete physical uncertainty may
permit a qualified descriptive transfer, but not statistical rejection or practical
adequacy. No scoring is authorized at this methods-only stage.

Even an admitted comparison would concern this larger isolated propulsion unit
under steady controlled inflow. It would not qualify the original 46 mm receiver,
nonuniform neighbor wakes, rotor interactions, transient command dynamics or the
5,000-drone accuracy/computation objective.
