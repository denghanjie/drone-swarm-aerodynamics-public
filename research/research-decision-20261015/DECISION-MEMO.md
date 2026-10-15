# Publication decision: keep the evidence, narrow the claim

15 October 2026, edition 2. Completed public-code campaigns and targeted primary-source review; no new experiment. Stable evidence: [checkpoint 5975b71](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/5975b71bec076e5ec498296668479a03a2ad80ba/research).

## Recommendation

**Prepare a reproducible technical report now. Do not yet submit a paper claiming a new aerodynamic model, a novel prediction algorithm, event-robust swarm simulation, or accelerated large-scale simulation.** The strongest current result is narrower: an established causal predictor substantially reduces numerical error in this particular public model, under separately checked step sizes, on a few short genuine local-3D Boids trajectories.

Next: test support crossings against stronger causal predictors before another flock study. The 200 MB limit remains; execution requires a frozen protocol, review and storage approval.

## Position on the original eight-step roadmap

The [unchanged roadmap](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/5975b71bec076e5ec498296668479a03a2ad80ba/outputs/research-roadmap.md) remains the framework.

1. **Define the experiment:** bounded numerical questions now have explicit outcomes and failures.
2. **Build one credible drone:** implementation checks exist; physical credibility is unfinished.
3. **Establish two-drone interaction:** the velocity screen informs this step and exposes a discrepancy; it does not complete validation.
4. **Handle overlapping wakes:** support/extent checks expose model assumptions; multi-source physical validation remains open.
5. **Run a local flock:** short genuine own-state 3D Boids cases exist. Event-exposed application coverage remains incomplete.
6. **Accelerate validated calculations:** prediction is a provisional numerical lead. The physical-validation prerequisite and matched-error runtime/WebGPU evidence remain missing.
7. **Scale the actual flock:** not demonstrated for the aerodynamic workload. Earlier 5,000-drone missions had airflow disabled; trajectory refinements failed.
8. **Evaluate the contribution:** this memo is that decision work, not a publication-ready verdict.

## What the evidence actually demonstrates

| Evidence | Supported conclusion | Important boundary |
|---|---|---|
| Two-seed 0.1 s predictor screen | All four declared trajectory-error maxima were 26.5–54.1 times smaller than ZOH at matched scheduled field counts; all 14 arms and 19 gates completed. | Both ZOH baselines already met the absolute caps. No clamp, wall response or axial-cutoff exposure established. |
| Translated 0.5 s case | Predictor errors were 42.2–125.9 times smaller; all predictor caps passed while three ZOH caps failed. The new joint reference and physical-step checks passed. | One developmentally selected seed; outcome remains EVENT_EXPOSURE_INSUFFICIENT. |
| Saved-state wall replay | All outputs matched on 50 reference controller states. All 2,412 early-pass wall tests were inactive; pair avoidance was active. | This closes an ambiguity on those saved reference states, not on every approximate trajectory or future flight. |
| Support-factorial replay | Removing the stipulated radial taper changed predicted thrust by at most 1.9686% of weight on fixed historical states. | An in-model sensitivity, not a physical-error bar. There was no axial-fade exposure. |
| Core-extent certificate | All-four-rotor finite bounds held on six deterministic fixtures; fixed axial support saturated as the formal uncut sum grew. | Independent-source continuation reached about 49–51 hover-induced speeds. This is not a credible physical airflow prediction. |
| Six-point 2026 velocity screen | Unchanged nominal predictions exceeded selected published centerline symbols by 0.6294–0.7603 m/s under the declared graphical convention. | Different velocity observables and unresolved measurement/parameter uncertainties prevent a physically matched validation verdict. |

The earlier air64 hold-cadence cap failure remains stopped despite successful error reduction. Later checks do not qualify the old reference or inaccessible private R8. Weak-wake pruning did not establish its desired speedup.

Reviewed hashes and sampled witnesses do not independently establish every maximum over unretained dense histories. The event campaign also exposed a real defect in its unused failure writer: actual wall normals have 17 components, whereas its schema assumed three. The failure-envelope guarantee is unqualified. Preserve that record and correct/review any future implementation before reusing the writer.

## Why the obvious novelty claims do not survive comparison

**Prediction is established.** CHOPtrey combines causal polynomial extrapolation, contextual history and hold fallback. Linear-plus-clamp belongs to this family; a fair comparison needs more than ZOH. [CHOPtrey, §§4–5 and 7](https://arxiv.org/html/1610.09261v2).

**Error-controlled coupling is established.** ECCO uses residual power/energy at paired power ports. Our algebraic wake lacks a resolved fluid-energy port; load discrepancy times velocity is not automatically ECCO. [Sadjina et al., §§II–III](https://arxiv.org/html/1602.06434v2).

**Multirate integration is established.** MRI-GARK supplies fast/slow stage constructions and order conditions. Fine vehicle steps plus coarse airflow extrapolation neither invent a multirate integrator nor prove those conditions. [Sandu, §2](https://arxiv.org/html/1808.02759v3).

**Rotor-resolved aerodynamic disturbances are established.** Jain et al. already combine incident velocity with per-propeller thrust changes to obtain forces and torques. Their experimentally identified response is not our ideal fixed-power closure. [Jain et al., §§II-C and IV](https://hiperlab.berkeley.edu/wp-content/uploads/2019/05/Modeling_of_aerodynamic_disturbances_for_proximity_flight_of_multirotors.pdf).

**Multi-drone downwash simulation is established.** Panerati et al. include an identified center-of-mass downwash force and two-drone comparison. It uses identification data and acknowledges missing pitch effects; these limits do not erase its prior-art relevance. [Panerati et al., §§III-C3 and V-A4](https://arxiv.org/html/2103.02142v3).

RotorPy supplies aerodynamic wrenches and actuator dynamics; Aerial Gym supplies parallel simulation and throughput comparisons. Both matter as software/runtime baselines, with different workloads. A viewer or batching alone is insufficient; their rates cannot be compared directly with our instrumented runs. [RotorPy](https://arxiv.org/html/2306.04485v1), [Aerial Gym](https://arxiv.org/html/2503.01471v1).

**Full CHOPtrey is the closest comparator.** Causal quadratic is the cheapest screening baseline; a verified MRI-GARK method matters for later efficiency claims. ECCO needs a justified power-port model first.

## A defensible contribution to pursue

The plausible route is a **rotor-resolved benchmark and method-selection result for expensive, piecewise-smooth interaction models**: identify when ordinary extrapolation is sufficient, when support changes or clamps cause load errors, and whether geometry-aware refresh decisions offer a measured benefit over existing history-based methods.

This hypothesis needs a causal decision, a load/trajectory target and complete cost. Retrospective geometry is not an online certificate. A cutoff counter or standard fallback alone may be too small for a full paper.

The finite core-extent bound may support a compact methods note. Its novelty is unestablished; more cone runs would not repair its physical assumptions.

## Three independent publication blockers

1. **Increment beyond prior art.** Linear prediction has only been compared with a weak hold baseline. Neither a published contextual method nor a verified multirate alternative has been implemented here. A negative or replication-oriented benchmark remains legitimate, but should be presented as such.
2. **Physical validity.** The mean-hover model, its extrapolation to a much smaller vehicle, independent-source aggregation and receiver response are not jointly validated. The measured-symbol amplitude discrepancy persists even in the preassigned approximately self-similar stratum. Mean speed magnitude and mean axial PIV velocity differ; resolving that mismatch requires evidence, not a fitted scale factor. [Bauersfeld et al.](https://arxiv.org/html/2403.13321v3), [Kiran et al., 2026 preprint](https://arxiv.org/html/2608.30900v1). Multi-source force aggregation already has experimental literature that also challenges simple addition. [Gielis et al.](https://arxiv.org/html/2312.03488v1).
3. **Efficiency and scaling.** Equal scheduled field counts establish neither equal total work nor speedup. The event run included 52.8 million observer pair visits, whose timing contribution was not isolated. There is no matched-error runtime frontier, WebGPU compute result, or scaling series. Browser visualization is not evidence of GPU aerodynamic execution.

Do not combine a roughly 2% model-relative load sensitivity, a velocity-amplitude discrepancy and a trajectory integration error into one “physical uncertainty budget.” They concern different observables and references. We have no calibrated physical uncertainty distribution or bound. Better numerics remains useful for a reproducible benchmark, but cannot validate the model.

## The single next bounded experiment

**Question:** At rotor-resolved radial-support entry/exit, does linear-plus-clamp retain a useful error/cost tradeoff against quadratic prediction and a causal cliff fallback?

This is a prescribed operator fixture, not flight or Boids. Keep one stationary upright hover source and an upright receiver 0.5 m downstream, with original rotor offsets, kernel, taper and load closure. Prescribe receiver center x(t)=0.22−0.12 cos(2π(t+φ)/0.5) m, y=0, for 0≤t≤0.5 s. Use H={1.25,5} ms and φ={0,H/2}: four fixed cases. No outcome-driven path/cadence search.

The [independent operator critique](OPERATOR-REVIEW.md) verifies geometric feasibility and lists remaining preregistration requirements. All rotors start in the core and leave/re-enter support; no axial or near-field crossing occurs. Symmetry gives only two distinct rotor histories and analytically zero roll; pitch is informative. The taper is C1, with second-derivative changes, not an inflow discontinuity. This fixture cannot establish finite-jump or wall robustness.

Use identical scheduled samples for four methods:
- ZOH.
- Current linear-plus-clamp, with initial hold.
- Three-sample causal quadratic, with hold then linear startup and the same nonnegative clamp.
- Quadratic with a **CHOPtrey-inspired restricted cliff gate**, threshold 0.9. This is an adaptation, not full CHOPtrey.

The gate must retain an unclamped **shadow quadratic endpoint** from the old history even when ZOH was delivered; count that arithmetic. At each refresh, first score the incoming alpha=1 prediction, then reveal the new exact sample and compare its shadow residual with the previous hold residual. The decision selects only the next interval. Never use the delivered fallback as the shadow: that can trap the method in hold. Use causal scalar-per-rotor history, no negative-time samples or periodic wraparound. Freeze strict-threshold ties, zero denominators, startup and one-sided endpoint handling before implementation. Dense truth and geometry labels are scoring-only, inaccessible to method decisions.

Score a common 6,401-time grid per case, spacing 1/12,800 s. Original-kernel values at those geometries define a sampled mathematical reference. Four cases × 6,401 times × four rotors = **102,416 logical reference rotor slots**, not total runtime work; guards may skip normalized-kernel calls. Cap wake calls at 110,000 including crosschecks. Count all prediction, shadow, clamp and load operations separately. Truth reuse supports offline comparison, not a speedup claim. Grid maxima are sampled maxima without continuous-time bounds; any integrated score must declare its discrete/one-sided convention.

Score maximum inflow error, force error/weight and roll-pitch moment error/(weight×arm); disclose the symmetry. Record false inflow outside support, discrete integrated errors, raw negative predictions, clamps and complete work. Freeze norms, floors, normalizers and startup/interior/crossing strata before implementation; retain all four rotors.

One proposed attempt: 20 s outer wall, output ≤100 KB, source/design/results ≤200 KB, no fitting/repeats/extra geometries. Retain worst witnesses, event brackets, stream hashes and counts. This is not execution approval; the critique's unresolved conventions still block protocol freeze.

**Decision rule:** if **one fixed quadratic variant** weakly dominates linear in all three maximum-error metrics in all four cases, has a strict resolved improvement somewhere and no worse false-positive support leakage, reject a special linear advantage on this fixture. Do not choose a different winning baseline per case. A surviving crossing tradeoff earns comparison with full CHOPtrey, not a novelty claim. Missing crossings, invalid geometry, nonfinite values or numerical ambiguity stop the test without replacement.

## How a successful fixture must reach a real flock

The next application stage would be separately adopted and use genuine own-state 3D Boids, not the prescribed path. Freeze two untouched seeds and a geometrically admitted initial layout before method outcomes are observed. Retain the original controller, physical model and domain stops. Compare the selected method, full CHOPtrey and ZOH, with matched clocks and complete extra-work counts. First qualify a synchronized whole-swarm reference and physical-step refinement on those cases, using the existing numerical caps and attribution checks.

Require actual eligible support transitions in the reference and both compared approximation trajectories. If wall robustness is claimed, separately require measured wall-induced command changes under a prospective definition. If exposure is absent, report that outcome; do not search offsets until one passes. Record clamps, controller events and near/far geometry jointly. A claim about runtime then needs a matched-error timing study with diagnostics separated and all fallback/history costs included.

A successful unit test earns an application test. Physical claims additionally need matched-observable held-out evidence. This memo authorizes none of these later steps.

Edition 2 clarifies shadow causality, symmetry, smoothness and sampled-work limits before any run; recommendation and path unchanged. Prior memo SHA256: 5ba7be83cd6d4aecaf5f290baa800fe9be6a4b7e6ff7cc31d61e6c1a1aa05a9e. Full metadata/version/access notes: [references.bib](references.bib).
