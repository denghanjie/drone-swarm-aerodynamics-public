# Challenge: qualify the moving load-consumption boundary before scale

17 October 2026. Source and saved-record review only, within a five-minute
planning assignment. No module was imported, numerical case evaluated, code
implemented, cap raised or execution allocation created by this review.
Frozen source/results and the completed capacity audit remain unchanged.

**Choose the short synchronized 64-drone coupling bridge proposed in the
parallel decision, subject to the concrete interface requirements below.** A
larger static reference or another Python cache change would leave the most
direct end-to-end failure modes untested. The proposed bridge is new numerical
method work, not merely attaching the already qualified query to a viewer.

The original benchmark calls for genuinely local 3D Boids, shared route
guidance, drone dynamics, explicit aerodynamic approximations and defensible
accuracy/computation evidence. The newest strict native evidence instead
queries final snapshots of airflow-off flights. Its generator explicitly
loads no aerodynamic module and its simulator calls per-drone
`F.integrate(s, controls[i].u, dt)`. The 5,000-drone Chrome screen record is also
posthoc: its 366–396 ms large-case query medians exclude flight steering,
integration and rendering. Those facts make actual consumption of current
loads the missing experiment; they do not diminish the saved numerical results.

The exact-reference ceiling is still 180. Its new capacity pass establishes
finite offline feasibility on fixed 64/180/180 cases, with different dense and
sparse work, not a live-flight or scale guarantee. No reference cap increase is
needed to test the next missing interface.

## The smallest decisive primary continuation

Use the entire saved, already admitted `fresh-a-t5` state: all 64 IDs and all
17 words per drone. Preserve the same local neighbor rules, wide factory,
wall-priority filter, shared route and nominal motor states. Starting from a
known nonzero-coupling state avoids manufacturing a new seed merely to find a
favorable case. It also preserves all source drones; selecting a convenient
subset changes the interaction problem.

The parallel proposal's 0.02-second continuation at dt=0.0025 is appropriately
small: eight whole-swarm steps, 32 synchronized RK stage queries, and two
control intervals at the existing 0.01-second cadence. The second Boids update
must read the evolved coupled state, not commands copied from the old flight.
Preserve the original t=5 origin and relative continuation clock explicitly.
Reusing its initial state creates a **new coupled continuation**; it is not a
replay and should not be described as no new simulation.

The production native calculation must run in the actual browser integration
path and supply the values used by the derivative before advancement. Save
every full stage state, stable-ID map, command, prepared record, native output,
consumed load and derivative, with the resulting stage/state dependency chain.
Check every one of the 32 actual stage states once using the unchanged
independent prepared/tree reference. Independent validation may inspect the
saved consumed stages; what cannot be posthoc is the production aerodynamic
feedback itself. A checksum of loads is not consumption.

Keep the four existing numerical observables and their exact normalization:
rotor error by mg/4, collective and Euclidean world-force errors by mg,
Euclidean world-moment error by mg*R, each at most 1e-8. Neither F/L agreement
alone nor positional similarity replaces those independent same-state tests.
Require a first-stage nonzero correction witness and demonstrate its path into
subsequent derivatives, stage states and the second local controller update.

## Concrete failures that the contract must expose

**Total loads versus corrections.** `physics.derivative` already includes
nominal collective force, nominal arm torque and nominal actuator yaw reaction.
Its optional external argument accepts only a world force. Native
`materializeLoads` returns total rotor/collective/world-force loads and the
world moment from rotor lever arms; it does not return a correction or certify
yaw reaction. Feeding its total world force into the old external argument
doubles thrust, while using that argument alone cannot apply arm torque.
Replace nominal translational thrust and nominal arm torque, keep gravity once,
and declare the retained nominal-actuator yaw law separately. Check world/body
frame conversion with a tilted unequal-thrust control. No reinterpretation of
world moment as body torque is acceptable.

**Motor states versus motor commands.** The 17-word input's final four words
are current nominal motor thrust states. `mix` may command zero; motor lag
means a zero command need not produce a zero current thrust. Feeding command
`u` instead of current states changes both source scaling and receiving-rotor
normalization. Never overwrite nominal motor states with attenuated delivered
thrust. Check actual stage motor states against the strict positive domain;
retain a genuine zero/nonpositive-state refusal rather than flooring it or
mistaking a zero command for an immediate refusal.

**Synchronized stages versus partially updated neighbors.** Four independent
per-drone RK stages cannot supply a consistent swarm snapshot. For each RK
stage, construct every drone's state first, perform one joint load query, then
evaluate all derivatives from that same immutable stage. Bind by stable ID and
stage/time identity, not array position alone. A stale previous-stage result,
ID permutation, omitted source or partially updated neighbor must fail before
state advancement. Holding a load across RK stages is a different approximation
and is not a fallback for a refused current-state stage.

**Quaternion admission is a known interface issue, not a surprise trial.**
The reference does not normalize supplied quaternions. Its preparation gate
uses qTolerance=1e-10 and geometryTolerance=1e-9. The inherited integrator
normalizes only endpoints. In exact algebra with unit q, the raw second stage
has norm squared `1 + h²*||omega||²/16`; finite-word initial norm and arithmetic
must still be checked on actual words. Endpoint admission therefore does not
imply raw-stage admission. Burning a full raw-stage coupled allocation to
rediscover this would be weak experimental design.

Predeclare a cheap first raw-stage preparation/admission diagnostic, without a
second swarm solve. Independently declare the projected-stage method as the
sole primary candidate before either result is seen; it is not a rescue chosen
after refusal. Project each whole stage's quaternion once and use those same
projected words for aerodynamics, derivative qdot and moment conversion. Keep
body omega, gyroscopic terms and controller/motor semantics consistent. Do not
hide projection inside the old reference or relax its tolerances.

There is relevant prior art **inside this repository**: the earlier
`m31-motion-feedback-2026-10-16/source/adapter.cjs` already projects every joint
RK stage and endpoint, adds effective-minus-nominal force/body roll-pitch
corrections, and retains nominal yaw. Its 16-Boids feedback paths completed,
but all 32 convergence gates were below the comparison floor, so they did not
establish integration order. The next bridge must not claim to invent projected
coupling or reuse those results as qualification of today's strict native
delivered-word/browser interface.

## Projected-method and derivative-draft review

Source-only inspection of the parent's new `derivative.cjs` shows the intended
structural repair: total world force replaces nominal translational thrust,
gravity appears once, delivered world moment is converted to body coordinates,
nominal yaw is added separately, and the motor derivative retains nominal
state/command lag. `projectState` explicitly declares a new projected method.
This is a plausible unexecuted alternative, not a qualified or adopted adapter.
The parent now explicitly favors reusing and extending the earlier projected
joint-stage adapter in the next executable design. Preserve these new drafts
as unadopted alternatives; do not replace proven structure merely because a
shorter new implementation is available. The new question is the strict native
delivered-word interface at every consumed 64-drone stage, not first-ever
airflow coupling.

It intentionally cannot establish load/state or stable-ID binding. The eventual
whole-stage caller must provide that proof; the draft must not be advertised as
a complete pipeline. Its world-to-body conversion and floating expression
order differ from the older delta adapter. Consequently no old bitwise or
strict numerical result transfers automatically. Also, the lightweight
`Array.every` vector predicate skips sparse-array holes: the production boundary
must use the qualified dense owned-input capture, rather than treating this
helper as a replacement input validator. No execution was used to test it.

Before the primary continuation, freeze manufactured controls for zero-airflow
baseline recovery, no double thrust, sign/frame-correct unequal arm moments,
separate yaw, unchanged nominal actuator evolution, stable-ID association and
stage freshness. Make any intentionally manufactured force input explicit;
an artificial fixed world force is a wiring test, not a physical airflow case.

Projection changes the numerical method. The proposed fixed h/h2/h4 analytic
translation/hover and principal-axis rotation controls are useful, provided
their exact norms, acceptance floors and failure rule are frozen first. A
roundoff-floor pass cannot establish fourth-order convergence. Continuous-time
trajectory accuracy remains a separate obligation after the load-consumption
bridge; do not infer it from 1e-8 same-state aerodynamic load agreement.

## Decision and claim boundary

Read the parallel DECISION as a proposal for a separately frozen allocation,
not execution authority. No new scientific run belongs in the remaining
current window, and reaching 03:00 UTC does not itself authorize a later run.
A new authorized window must contain the full proposed controls, 32 primary
queries/references, saved checking and closure, with fixed output/call bounds.

An input, projection, admission, load association, derivative-consumption or
manufactured-control failure is a decisive negative result. Stop at that
failure; do not drop drones, skip a stage, retain stale loads, change precision,
switch integrators or enlarge the ceiling. A pass establishes that the complete
discrete feedback path can preserve the specified numerical load observables
over this short exposed continuation. It does not establish mission success,
continuous-time accuracy, real-time 5,000-drone operation or robust new-flight
generalization.

Physical validity is independent: the closure, receiver response, superposed
wakes and retained yaw law remain model assumptions without matched flight
measurements. A numerically exact feedback simulation can still be physically
wrong. This challenge makes no new physical accuracy or novelty claim.

## Source pins

These are the exact read sources, not a proposed execution manifest. Paths are
repository-relative. Planning-document/draft pins are recorded in the appended
closure note when their writers close the reviewed versions.

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| `outputs/research-complex-environment-goal.md` | 2619 | `a5ccfe25faccdbf9d3f78cc7c4a5a50dc73f999e4f5052b03f7fedd4e78c8627` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs` | 11475 | `2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs` | 6115 | `0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1` |
| `research/m31-native-fresh-transfer-2026-10-17/source/pair-reference.py` | 44757 | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `research/m31-native-fresh-transfer-2026-10-17/source/spec.json` | 296772 | `a47b9b920ddbbd14e1838e9c031a0b34dd1820f14959ef1295cef039e7f48d2f` |
| `research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs` | 16262 | `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1` |
| `research/m31-native-fresh-transfer-2026-10-17/MILESTONE-SUMMARY.md` | 2010 | `0705899cbfcce89f690f56d65dff113d51dc1ffe0e92ce8351390b23683b5b98` |
| `research/m31-native-fresh-transfer-2026-10-17/results/inputs/fresh-a-t5.json` | 21955 | `48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c` |
| `research/m31-browser-screen-2026-10-16/MILESTONE-SUMMARY.md` | 6256 | `e92ff7718664c1d9796ff737d7d462195f232b4dbc9f1530bd2057a94868836e` |
| `research/m31-prepared-capacity-2026-10-17/review/saved-audit-result.json` | 5296 | `e6748154280c80f907d774d3f5bb95b4ef65471a87835156136ad21ad88ca412` |
| `research/m31-motion-feedback-2026-10-16/source/adapter.cjs` | 5367 | `332035b55439c568f3a4372c94557359e5ca4a264e3a0f635abdd28ac075a0a9` |
| `research/m31-motion-feedback-2026-10-16/POSTRUN-RESTART.md` | 1490 | `720ae1f8330d2cd9440f9f1bc71b4d93da4e5427fce3d4591a8eb430d435792d` |
| `research/m31-force-ablation-2026-10-16/NEXT-QUESTION.md` | 3429 | `6a08bdec0796baf7c6f0180f8e4489f525f9ea5cf4bfb356133310ed7b69560c` |

## Closure of this planning review

The final parallel decision was read, including its corrections for prior
16-drone projected coupling, a new continuation rather than replay, original
and relative clocks, and the requirement for a new authorized execution
window. Reviewed `research/m31-next-scale-decision-2026-10-17/DECISION.md`:
10,897 bytes, SHA256
`f7fa7db78132c3cf3c7a3bc000858611c9ba0ecceadecb1a01ccd6ea1dec7394`.

The source-only derivative observations apply to the inspected unexecuted
`research/m31-coupling-bridge-design-2026-10-17/source/derivative.cjs`:
3,444 bytes, SHA256
`f436b9daa7c15008f842c99cd12426a61d3b9db05d566427f7d07c22074fca5c`.
This review does not qualify the subsequently added synchronous-step draft or
approve either draft for execution. All challenge-task writes are closed.
