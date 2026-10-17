# Next experiment: make the checked loads drive the swarm

Recommend one **64-drone synchronized coupled-integration bridge**, starting
from the complete saved `fresh-a-t5` state. Do this before another large static
reference run or a Python optimization. The current native production path
can calculate total loads, but the latest fresh64/large5k recorded local Boids
path never consumes them. Closing that interface is necessary progress toward actual coupled
5,000-drone flight. Passing this pilot would not complete that larger goal.

This is a source-only recommendation. No source implementation, scientific
execution, new benchmark, parameter change or cap increase is authorized or
performed here. The accompanying source receipt pins the actual files read.

## Evidence that changes the priority

- The capacity index records exact accuracy and practical-hurdle passes for
  64/180/180, 45,455 suffix calls, 16.95629358291626 seconds through pre-index
  closure, and process-lifetime peak RSS 127,139,840 bytes. Dense180 has 3,056
  positive terms and 600 nonpoint roots. Its profiled regeneration is
  12.317360833287239 seconds; `snapshot` alone has 1.929684955 seconds own time.
  These Python costs belong to the independent measuring instrument. They
  cannot explain production Chrome frame time; cumulative times overlap and
  profiling adds uncalibrated overhead.
- The existing native `kernel.cjs` still loops over every nonself `i,j` before
  its coordinate screen. The qualified 5,000-drone Chrome medians are
  366–396 ms per aerodynamic query, excluding steering, integration and
  rendering. That is already much longer than the simulator's 10 ms control
  period, without multiplying it into a claim about a coupled implementation.
  Python optimization would not remove this production enumeration cost.
- The inspected `sim.cjs` calls per-drone `F.integrate(s,controls[i].u,dt)` and
  labels its recordings `airflow:'off'`. `physics.cjs` already derives nominal
  thrust, arm torque and yaw reaction from motor states; its extra argument is
  force only. `native-load.cjs` returns total delivered rotor/collective/world
  force and thrust-arm world moment, not a correction and not yaw reaction.
  Adding that force through the existing external-force argument doubles
  thrust; ignoring the moment loses feedback. Calling the solver separately
  during each drone's RK stage also uses inconsistent swarm states.
- An earlier `m31-motion-feedback` adapter already projects all whole-swarm
  stages, adds effective-minus-nominal force/roll-pitch correction and retains
  nominal yaw. Its 16-drone coupled diagnostic completed, so coupling itself
  is not a new invention. Its 32 refinement gates were all below the declared
  comparison floor and did not establish an observed order. The new question
  is transfer of the now-qualified native delivered-load interface, with
  strict independent checks of **every** used stage, to the complete64state.
  Reuse that joint-stage structure; do not claim its previous qualification
  transfers automatically to the new load/frame/ID boundary.

## One fixed pilot and its measurable hypothesis

Use all 64 stable IDs of the pinned `fresh-a-t5` input, preserving its original
nominal motor states, wide factory, wall-priority filter, local-neighbor Boids
and shared route. Continue for **0.02 simulated seconds at dt=0.0025**:
eight synchronous whole-swarm RK steps, four stages each, **32 native F load
queries and 32 independent reference calls**. The controller updates at the
existing 0.01-second cadence, so the second control interval reads an evolved
coupled state. This is a new coupled continuation of a saved state, with no
new seed or initial-condition generation, subset, replacement or retry.
Record original time `t=5+offset` as well as relative offset; controller updates
are at relative0 and0.01seconds, using the evolving continuation state.

The primary hypothesis is that every declared stage is admitted; all actual
consumed load words satisfy the unchanged four-category 1e-8 numerical error
contract; stage/source/ID associations are complete; and nonzero aerodynamic
loads enter the derivative and subsequent state/control updates. Require an
explicit first-stage witness that the applied force or arm moment differs
from nominal, and a recorded dependency chain from that derivative to the
next stage/state and the second controller update. A checksum-only consumer
does not satisfy this hypothesis. Save states, commands, stage inputs,
prepared words, native solved/delivered loads, actual derivative inputs,
derivatives and resulting states, with stable-ID joins and exact word pins.

This is the smallest proposed pilot that uses an already admitted, nonzero
moving swarm intact and includes a subsequent Boids control update. It is a
coupling/accuracy experiment, not an end-to-end performance trial. Production
wall phases may be recorded descriptively without cProfile, warmups or repeats.

## Predeclare the stage convention; do not rescue a raw-stage failure

Raw RK intermediate quaternions need not remain unit length. For unit q and
qdot perpendicular to q, the raw second stage has
`||q + h*qdot/2||² = 1 + h²*||omega||²/16`. This can violate the frozen
`qTolerance=1e-10` and associated geometry checks (`1e-9`). Merely connecting
the existing per-drone RK4 code is therefore not a coherent plan.

Declare two roles before any pilot execution. A **cheap raw-stage diagnostic**
records the first raw second-stage quaternion norm and preparation-admission
decision using the first primary stage's derivative; it does not run a second
full swarm solve or become an alternative success path. A **projected-stage
candidate** is the sole primary integrator regardless of that diagnostic's
outcome. Normalize each stage quaternion once, deterministically, before
constructing the entire stage state consumed by both aerodynamics and the
derivative. Use that same projected q for force geometry, world/body moment
conversion and `qdot = 0.5*q ⊗ [omega,0]`; keep body omega and `omega × I*omega`
gyroscopic terms in the same body frame. Combine stage derivatives from the
step's base state and normalize the final quaternion. Pin operation order and
refuse zero/nonfinite quaternion norms. Never relax model tolerances.

This reuses an existing projected-stage convention while specifying a new
native-load consumption boundary. It is not a claim that old raw-stage RK4
has been preserved or that fourth-order convergence has already been proved.
Before the primary run, fixed no-flow manufactured
controls must establish force/torque/frame wiring and convergence: zero-rate
translation/hover, pure principal-axis constant angular-rate rotation against
its analytic quaternion, and tilted unequal-thrust force/arm-moment mapping.
For the analytic cases use one common 0.0025-second interval at h=0.0025,
0.00125 and 0.000625, all declared in advance; require finite states and
decreasing state/quaternion errors (or a predeclared floating roundoff floor).
Do not infer the convergence order from one ratio. The exact floor and
component norms must be independently reviewed and frozen before launch;
failure blocks the coupled branch rather than selecting another integrator.

Replace the nominal translational thrust with total delivered world force,
and replace its nominal thrust-arm moment with the delivered world moment
converted once to body coordinates. Keep the original **nominal-actuator yaw
reaction law** as an explicitly separate modeling assumption; the current
aerodynamic load interface does not certify yaw reaction. Preserve motor lag
on nominal actuator states; never overwrite them with attenuated delivered
thrust. Require fixed wiring controls to reject double thrust, missing/wrong-
frame arm torque, stable-ID misassociation and overwritten actuator state.
Yaw-model validity and integration truncation error are separate from the
four aerodynamic load-error categories.

## Independent reference and numerical acceptance

For each of the 32 saved projected stage states, invoke the unchanged
prepared/tree reference once with maxDrones180, coefficient/source bits192
and root bisections128. Retain full exact coverage and independent signed
root/load boxes. Use the qualified native checker logic to compare actual
delivered-and-consumed words to those boxes, including source support and
binary64 arithmetic/association checks. Keep rotor error normalized by mg/4,
collective and Euclidean world-force error by mg, and Euclidean world-moment
error by mg*R, each at most 1e-8. Audit the additional world-to-body conversion
and derivative consumption independently; an accurate but unused load fails.

The reference checks the stage values actually used by the discrete method.
It does not certify continuous-time trajectory error or physical airflow
accuracy. Native F and L agreement alone is not an independent reference.
The current cap180 and all scientific arithmetic/admission constants stay
unchanged; no 5,000-drone exact-reference cap is lifted for this experiment.

## Prospective reservation and failure decision

Require a separately reviewed source freeze, public byte verification and a
**new execution window reserving at least 960 seconds**: at most 900 seconds
for fixed controls, primary integration, references and saved checking, plus
60 seconds closure. No execution is allowed in the current window ending
03:00 UTC; a new explicitly authorized window is required. Passing that clock
time does not itself grant permission. Proposed output limits remain 32 MiB
per file and 256 MiB total; observed memory hurdle is 1 GiB, explicitly not an
OS-enforced limit unless a separate reviewed guardian implements one.

Each reference retains its existing per-call 30,000 suffix budget; for 64
drones the 32 stage calls have a structural maximum of 516,096 logical
rotor/source queries in total. This is a new prospective finite allocation,
not permission to enlarge a closed checkpoint or modify any model cap. The
final protocol must reserve and enforce all controls, call counts, byte
limits and shutdown work before exposure. No profiling loop or unprofiled
repeat is added to this pilot.

If a control, admission, stage association, exact load test, finite-state check
or allocation limit fails, preserve the first failure and all partial records;
do not skip a stage, freeze old loads, relax precision, reduce the swarm or
switch between raw/projected variants. An accurate completed bridge would
justify designing a later production spatial-candidate experiment aimed at
the actual all-pairs bottleneck. It would not authorize that implementation,
prove 5,000-drone coupled affordability, validate real aerodynamics or establish
novelty. A failed bridge directs effort to the concrete integration/reference
failure before larger-scale speed work.
