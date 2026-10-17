# Qualitative physical compatibility of the current directional receiver model

17 October 2026. Retained primary articles and current source only. No network,
new body acquisition/extraction, figure digitization, numerical data extraction,
simulation, fit or score. This is a model-scope assessment, not a physical
validation result. Bibliographic identities and retained-body hashes are in
`READ-RECEIPT.json`; third-party bodies remain private.

**The current model can represent qualitative lower-vehicle thrust loss and
offset-induced pitch/roll, but it cannot represent every interaction reported
in the retained experiments.** Its upright-pair upper-vehicle response and its
fixed-input velocity/history response are structurally absent. Published upper
vehicle effects and dynamic approach/retreat differences therefore rule out
calling this a general mutual, dynamic aerodynamic model. They do **not** yet
constitute a matched falsification of its admitted, quasi-static far-field
subdomain: geometry, actuation and the explicit near-field refusals must match.
The available evidence does not establish a quantitative accuracy level.

## What the code actually assumes — our source deductions

These deductions come from the currently inherited
[`pair-reference.py`](../m31-native-fresh-transfer-2026-10-17/source/pair-reference.py)
(`constants_from_graph`, `prepare_one`, `oracle_case`),
[`semantic-reference.py`](../m31-native-fresh-transfer-2026-10-17/source/semantic-reference.py)
(`prepared_exact`, `bisect_cubic`, `reference_roots`, `load_boxes`), the unchanged
[`tree-reference.py`](../m31-tree-first-reference-2026-10-17/source/tree-reference.py)
admission order, and the delivered native `materializeLoads` load map. The model
descriptions were also read, but do not replace these source checks.

1. **A directed, fixed-shape source field.** For source axis `b_j`, the scalar
   coordinate is `down = (sourceCenter − receiverRotorPoint) · b_j`. `down ≤ 0`
   returns upstream zero. The profile is radial around that source axis, has a
   prescribed width increasing with downstream coordinate, and is multiplied by
   `max(0, b_i · b_j)`. It has finite neighbour/downstream/radial support. Close
   on-axis pairs are explicitly **rejected** below `minDown × D`, not assigned
   a reliable near-field load. Source geometry does not bend or change width
   because a neighbour is present. Source-strength coupling changes amplitude.
   The admitted exact-reference graph additionally requires every positive
   source edge to precede its receiver in descending centre-z order; a backward
   positive edge is refused. For tilted vehicles, the pair halfspace is axis
   based, so “above-to-below” alone is an incomplete description.
2. **A positive, loss-only receiver law.** The code solves
   `x_ir³ + α_ir x_ir = 1`, with `α_ir = Σ_j a_irj y_j ≥ 0`,
   `y_i = sqrt(Σ_r w_ir x_ir)`, and delivered rotor thrust `f_ir x_ir`.
   Thus `0 < x_ir ≤ 1`; zero inflow gives exactly one and positive inflow gives
   a reduction. This is the chosen ideal-power-style cubic with prescribed
   nominal thrust, not a motor/voltage/RPM transfer model. The coupling is
   **already nonlinear**; it is not a sum of independently predicted force
   losses. Neither source code nor the physical articles demonstrate that this
   particular source-strength closure is a measured constitutive law.
3. **Axial rotor loads and lever-arm moments.** All rotor forces share the
   prepared vehicle axis: `F_i = b_i Σ_r f_ir x_ir` and
   `M_i = Σ_r (offset_ir × b_i) f_ir x_ir`. Unequal rotor losses can produce
   pitch and roll. There is no separate airframe side-force, rotor drag torque,
   or aerodynamic yaw law. In the exact map, force is parallel to `b_i` and
   moment has no component along `b_i`; a tilted vehicle can still have nonzero
   **world-z** moment. Treating the stored three-component vector as a general
   measured six-axis aerodynamic response would overstate the model.
4. **Instantaneous response at fixed supplied inputs.** `prepare_one` reads
   position, quaternion and four nominal forces; velocity/angular-velocity
   words are checked/bound but do not enter the physics. The root solver has
   no wake state or history. Identical geometry and nominal forces produce the
   same solution irrespective of approach/retreat. A separate controller could
   change the supplied nominal forces; that would not establish velocity or
   memory dependence in this law itself.

The dimensions require care: the code's `arm` multiplies each corner coordinate,
`R = sqrt(2) × arm`, and `D = 2R`. Kiran's `l` is centre-to-motor distance;
Bauersfeld's `l` is its defined motor distance (Fig. 2). These symbols must not be
equated by name. No experimental case was instantiated or classified here.

## Published observation versus model deduction

### Kiran, Ayanian and Breuer — arXiv:2507.09463v1

**Published static observation:** §III-A, Figs. 5(a,c) and 6(a,c), reports a
stronger thrust reduction on the lower vehicle, a smaller reduction on the
upper vehicle, and pitch moments on **both** vehicles when horizontally offset.
The lower vehicle recovers towards nominal thrust as separation grows; offset
produces a stronger pitching effect than the symmetric stacked arrangement.
This is a reported force/transducer result, not an inference from the apparatus.

**Our deduction:** lower thrust loss is allowed by the cubic, and unequal
per-rotor losses allow an offset moment. These are qualitative compatibility,
not validation of magnitude, exact sign convention, optimum offset or decay.
For an isolated upright pair, the lower source is upstream-excluded for the
upper receiver. With no other upstream sources, all upper roots stay at one,
so moving the lower drone cannot change the upper model thrust or its
interaction-induced moment. The reported upper response is therefore an absent
mechanism. Numerical precision or faster pair evaluation cannot add it.

**Direct-test limitation:** §II-A uses tethered 4 V and hover PWM, explicitly not
constant rotor speed; constant voltage/PWM also does not imply constant ideal
power. Body/rotor geometry and nominal-thrust association are not matched to
the fixed current model. The strongest reported close-spacing effects must be
checked against its near-field refusal before they can be used as admitted
counterexamples. A refusal is lack of coverage, not a wrong predicted number.
The paper establishes that the upper effect exists in its experiments; this
review does not establish its size within the current admitted subdomain.

**Published dynamic observation:** §III-C, Figs. 14–16, reports phase-averaged
approach/retreat loops: at a given separation the approaching phase produces
lower thrust than retreat, with stronger destabilizing offset moments during
approach. The paper describes loop broadening with increasing separation rate.

**Our deduction:** a unique fixed-input algebraic response cannot reproduce
those distinct values as a function of separation alone. This establishes an
omitted dynamic dependence if the model is offered for those operations.
It does not identify whether velocity, wake memory or actuator dynamics is the
appropriate missing state. The test still needs matching geometry, admitted
separations, actual actuation and force conventions; fixed PWM is not an
experimental implementation of fixed ideal power.

The v1 wording is internally inconsistent about the amount of lower thrust
loss: §III-A describes thrust **at** a fraction of nominal, while §IV describes
a similar percentage as a **reduction**. The earlier literature ledger already
flags this. This note uses the supported direction of change only; it neither
chooses a percentage nor digitizes the figures to resolve the discrepancy.

### Gielis, Shankar, Kortvelesy and Prorok — arXiv:2312.03488v1

**Published observation:** §4.3, Figs. 5–6, reports that measured D-axis force
patterns from the three-neighbour Leader Follower formation become less
separated and concentrate away from the formation edges as vertical separation
increases; a simple sum of single-neighbour force models fails in that setting.
The authors interpret this as lateral wake merging/contraction and discuss a
forward displacement of the apparent final wake. The primary measurement here
is the load-stand force pattern; this is not a direct PIV measurement of that
inferred wake deformation.

**Our deduction:** the current kernels have no explicit neighbour-dependent
centreline/width deformation. This is an important modelling risk. However,
the current receiver cubic and source amplitudes are nonlinear, so the paper's
failure of **linear force summation** is not, by itself, a counterexample to
this implementation. Overlapping fixed profiles and nonlinear response can
also change an aggregate force pattern. Whether they reproduce the reported
pattern is unresolved; no prediction was generated here.

**Published direction/channel evidence:** §4.1 says N/E forces and yaw torques
have identifiable trends but are generally noise dominated; the authors name
measurement and facility/stand interference. §5 reports small, chaotic lateral
effects at distance. Those are useful warnings about the current axial-only
force map, but not a clean signed lateral-force falsification. Pitch/roll are
not absent from the model. Do not turn a six-axis instrument into evidence of
six independently resolved model failures.

**Test matching:** §3.1 uses NED axes and a powered-hover receiver tare; the
reported force is an incremental disturbance, whereas the code delivers total
rotor/collective/axis force. The proper isolated baseline must be subtracted
and signs aligned. The flying formation and constrained powered receiver also
do not establish fixed ideal power. §4/Fig. 4 and §5's weak lateral expansion
of a force footprint cannot directly refute the spreading of a *velocity*
half-width: observable, threshold, vehicle and actuation differ. No quantitative
far-support or zero-cutoff validation follows from “negligible” influence.

### Bauersfeld, Muller, Ziegler, Coletti and Scaramuzza — arXiv:2403.13321v3

**Published observation:** §V, Figs. 4–5, reports distinct near-field rotor jets
and a central reduced-speed region before merging. §VI-A/B, Figs. 6–9, reports
the far-field radial-profile similarity, widening half-width and downstream
centreline decay of planar-rotor hover wakes. Canted-rotor vehicles show different
width/centreline behaviour. These observations support a restricted far-field
mean-profile approximation and warn against using a single centred jet in the
near field or silently treating rotor cant as whole-vehicle tilt.

**Our deduction and evidence limit:** the code adopts the paper's fitted
`10.11 / 0.07668 / −5.817` scaling constants (its Eq. 9), so re-agreement with
the fitted family is not independent holdout validation. §IV-A's hot-ball
probe is omnidirectional: it measures speed magnitude, not a signed velocity
vector. Those data do not establish the code's axial load direction, projection
rule, receiver cubic or mutual source-strength coupling. The near-field refusal
is consistent with a deliberate applicability limit; it does not solve the
reported near-field structures.

**Published controller result:** §VII-A/B, Eqs. 10–11, Fig. 10 and Table III,
reports improved height tracking when extra power/throttle compensation is
added while a small vehicle passes beneath a larger one. The compensation
uses the Kolibri ESC's stated throttle–power relation. This supports the broad
need for extra power to preserve thrust in downwash. It is a controlled-flight
tracking result, not a measured constant-power rotor-thrust curve or a direct
test of the current cubic on a 27 g vehicle. The hardware-specific mapping is
precisely why constant PWM, constant RPM, constant ideal power and hover regulation
cannot be exchanged without a declared actuator model.

## Decision supported now; matched questions still open

The defensible description is **a deterministic, directed, far-field-inspired
axial-load model with hypothetical source-strength coupling, qualified
numerically on its admitted inputs**. Claims of general mutual upper/lower
interaction, unsteady response, arbitrary six-axis aerodynamic load or verified
many-drone physical fidelity exceed its structure or the evidence.

The smallest useful physical challenge is a preregistered **upper-response
null test**: for an upright isolated pair at fixed matched actuation, determine
whether an interaction-induced upper thrust or pitch change is resolved at a
spacing admitted by the model. The model's null is exact for that arrangement.
A nonzero matched result beyond experimental uncertainty would falsify that
null without needing a broad fitted benchmark. The retained publication already
motivates the question; it does not yet supply all domain/actuation/uncertainty
associations needed to declare the present model failed on an admitted case.

A second clearly posed question is whether approach and retreat at matched
geometry **and nominal actuation** yield distinguishable lower loads within the
admitted range. A resolved difference would reject the memoryless description
for that operation. This is not permission to reconstruct firmware labels or
score a newly extracted dataset. Published figures can be sufficient for a
qualitative rejection when those associations and uncertainty are explicit;
downloadable raw data are not a universal prerequisite for physical reasoning.

No conclusion here forces a new model implementation, recommends tuning to
these exposed papers, or supplies a physical pass/fail score. Numerical
reference accuracy and computational capacity remain separate achievements.

## Exact citations

- **Kiran, Anoop; Ayanian, Nora; Breuer, Kenneth.** *Influence of Static and
  Dynamic Downwash Interactions on Multi-Quadrotor Systems.* RSS 2025,
  DOI [10.15607/RSS.2025.XXI.102](https://doi.org/10.15607/RSS.2025.XXI.102).
  Body actually read: [arXiv:2507.09463v1](https://arxiv.org/html/2507.09463v1),
  §II-A, §III-A/Figs. 5–6, §III-C/Figs. 14–16, §IV–V.
- **Gielis, Jennifer; Shankar, Ajay; Kortvelesy, Ryan; Prorok, Amanda.**
  *Modeling Aggregate Downwash Forces for Dense Multirotor Flight.* ISER 2023,
  proceedings published 2024, pp. 393–404,
  DOI [10.1007/978-3-031-63596-0_35](https://doi.org/10.1007/978-3-031-63596-0_35).
  Body actually read: [arXiv:2312.03488v1](https://arxiv.org/html/2312.03488v1),
  §3.1, §4.1–4.3/Figs. 4–6, §5. The publisher chapter body was not newly read.
- **Bauersfeld, Leonard; Muller, Koen; Ziegler, Dominic; Coletti, Filippo;
  Scaramuzza, Davide.** *Robotics meets Fluid Dynamics: A Characterization of
  the Induced Airflow below a Quadrotor as a Turbulent Jet.*
  [arXiv:2403.13321v3](https://arxiv.org/abs/2403.13321v3), 12 December 2024,
  accepted RA-L manuscript. Retained PDF identity verified; passages read from previously retained text:
  §III-A/Fig. 2, §IV-A–C, §V/Figs. 4–5, §VI/Figs. 6–9/Eq. 9,
  §VII/Eqs. 10–11/Fig. 10. Journal-version DOI/date ambiguity is not resolved anew.
