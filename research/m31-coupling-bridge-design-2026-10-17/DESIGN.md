# Next bridge: feed verified total loads into local Boids dynamics

17 October 2026. **Unexecuted source design, not a research result or execution allocation.** Previous numerical outputs, models and failed experiments are unchanged. The completed visible milestone remains the [180-drone evidence viewer](../m31-prepared-capacity-2026-10-17/viewer/); no new moving trajectory exists for this design.

## Why this is the next question

The fresh native-transfer experiment verified posthoc loads on two moving local-Boids states, with airflow off during integration. The capacity checkpoint makes the offline exact reference usable on the fixed 64/180/180 cases. Neither transfers the latest native delivered-load interface and strict reference checks into every consumed stage of a 64-drone coupled flight. Earlier [motion-feedback work](../m31-motion-feedback-2026-10-16/review/RESULT-INTERPRETATION.md) already demonstrated 16-drone coupled response and sampled integration consistency with a prior adapter. This is not a first-coupling proposal. Advancing the newer interface and every-stage evidence is relevant to the 5,000-drone target; further optimizing the offline measuring instrument alone would not make production flight faster.

Actual source inspection found that the inherited physics derivative computes nominal rotor force and moments internally, while its external argument adds world force only. Native loads already contain total modified rotor force and lever-arm moment. Adding native total force through that argument would count nominal thrust twice; it would also omit the changed roll/pitch moment. This is an interface deduction from code, not an observed flight failure.

The paired source locations are `m31-native-fresh-transfer-2026-10-17/source/native-load.cjs` (`materializeLoads`) and `source/vendor/generation/step02c-source/physics.cjs` (`wrench`, `derivative`, `integrate`). The source pins in this package preserve those inspected versions.

## Candidate interface

`source/derivative.cjs` is a new, unexecuted low-level draft alternative. It is not adopted for execution, plugged into an old flight or certified by old tests. The prior `m31-motion-feedback-2026-10-16/source/adapter.cjs` already has projected synchronous stages and nominal-force corrections; the preferred implementation direction is to extend that inspected structure to the current native interface and complete stage records. These drafts were prepared before that prior adapter was rediscovered and are retained transparently as unadopted design material, not as a replacement achievement. It:

- Keeps each motor-state entry as nominal isolated thrust, with the inherited first-order actuator lag. Actual reduced rotor thrust must not overwrite that state or be reduced twice.
- Replaces nominal rotor force with the delivered world force, divides by mass and subtracts gravity once.
- Converts the delivered world lever-arm moment to the body frame once, replacing nominal roll/pitch terms. It retains the inherited nominal-actuator reaction-yaw term as an explicitly provisional assumption. The current aerodynamic model supplies no reaction-torque law; this policy is not physically validated.
- Keeps angular gyroscopic terms and quaternion kinematics, using body angular velocity.
- Exposes a separate `projectState` helper. Stage projection is an explicitly specified numerical convention already used by the earlier motion-feedback adapter, not a hidden repair inside the frozen reference. The same projected stage words must be used for geometry, aerodynamic query and derivative evaluation.

Both draft files passed Node syntax-only checking (`node --check`), which does not import or run their code. No scientific module has been imported, test run, trial generated, reference extended or threshold changed for this source design. Merely reading/parsing source cannot qualify the arithmetic.

## Synchronized stages and load binding still to implement

A swarm RK stage must be assembled for all drones before any load query. The full stage is then projected, assigned stable IDs, queried once and joined back by exact ID. Returned state/prepared/load words must be bound to that stage. No drone may read a neighbour that has already advanced to the next stage. Missing IDs, refused native/reference status, nonfinite data, unsupported graph or nonpositive nominal force stops that branch with preserved partial evidence.

The existing per-drone `integrate` cannot provide those simultaneous swarm stages. The unexecuted `source/synchronous-step.cjs` draft now assembles four whole-swarm projected stages, checks returned raw state words and IDs, records consumed loads/derivatives, and combines the endpoint. It holds commands within one step. A whole-flight/control driver, independent checker and complete source review remain required. Failure persistence for exceptions and malformed native results is not yet implemented by a supervising harness; the draft is not execution-ready. The candidate derivative cannot independently prove that a supplied load belongs to its state; it must never be treated as doing so.

## Quaternion issue and prospective comparison

The frozen pair reference requires quaternion norm within `1e-10` and prepared geometry within `1e-9`. It does not normalize raw input. In exact arithmetic, for unit q and body angular velocity w, qdot is perpendicular to q and has norm |w|/2. An ordinary RK half stage therefore has squared norm `1 + h^2 |w|^2 / 16`. Endpoint normalization does not make intermediate stage geometry admissible. This identity motivates the design; actual rounded admissions remain to be measured.

Do not allocate a large full flight merely to rediscover this known interface risk. Freeze a small raw-stage admission diagnostic and a separate projected-stage candidate before observing either. The raw arm has no automatic fallback into projection. Projection cannot silently relax the original model tolerance. It differs from the original raw-stage integrator and requires explicit transfer of consistency and step-refinement evidence, including an airflow-off baseline using the same projection. Neither the old RK4 order nor old trajectory tolerances can be inherited without verification.

## Smallest informative experimental sequence — not yet allocated

1. Manufactured derivative controls: zero interaction must reproduce nominal force/roll/pitch under a matched projected attitude; known loss must reduce vertical acceleration; asymmetric losses must change the correct pitch/roll sign; tilted force/moment must transform once; motor derivative and declared yaw policy must remain separately testable. Deliberately doubled force, omitted moment, stale/incorrect ID and wrong-frame controls must fail independent checks.
2. A fixed, short continuation of one complete 64-drone local-Boids state, spanning at least two control updates. Preserve local separation/alignment/cohesion and inherited broad route guidance; no scripted formation or favourable seed selection. Compare matched airflow-off and on branches with synchronized stages. The chosen duration, step sizes, raw/projected arms, total query count and all stop rules must be frozen in an executable protocol first.
3. Independently verify every consumed stage load with the unchanged reference and all four normalized `1e-8` load criteria. Record the actually consumed derivatives and state updates, not merely matching load files. A full second trajectory reference/convergence contract is distinct from instantaneous load accuracy; record it explicitly before claiming trajectory accuracy.
4. Record observed contact/model-limit stops and whole-call time, including Boids, controls, stage construction, aerodynamic query, state integration, transfers and synchronization. Separate exact-reference verification cost, saving and rendering. This pilot is an integration diagnostic, not a speedup or 5,000-drone feasibility test.

The proposed fixed short continuation and budgets in the independent decision/challenge are inputs to the future executable protocol, not authorization to launch. No automatic size increase or held-load approximation follows. If stage projection changes convergence or reference admission fails, retain that outcome; do not select a smaller timestep after seeing results under the same allocation.

## Research status and next execution boundary

This is a concrete source candidate plus a design decision, not a new experimental milestone. Source inspection justifies testing this interface; it does not show the candidate works. Physical validity, whole-swarm stability, browser throughput, 5,000-drone scaling and publishable novelty remain open.

The approved execution window ends at03:00UTC17October2026. This package does not extend it. The adopted adapter extension, executable driver, test source, exact allocation and independent source approval must be completed and published before any scientific dispatch, with a valid window large enough for the entire reserved budget. Continue source preparation without pretending execution has occurred. After an eventual experiment, produce an actual-record Three.js replay and a new audited GitHub result checkpoint.

## Parent decision after independent source review

Adopt the [fixed short-continuation question](../m31-next-scale-decision-2026-10-17/DECISION.md), subject to the [independent interface challenge](../m31-next-scale-challenge-2026-10-17/CHALLENGE.md). Prefer extending the prior projected swarm adapter instead of starting a second competing integrator. The two newly written syntax-checked drafts remain unadopted. No benchmark or numerical experiment has run in this checkpoint. The advance is a corrected implementation target and an explicit evidence gap: current native delivered loads, all consumed stage words, controller feedback and independent strict numerical checking together.

The [upper-response admission audit](../m31-upper-response-admission-2026-10-17/ADMISSION.md) does not admit a physical rejection: the closest explicit case conditionally falls in the model's refused near field, while farther textual observations refer to flow or fluctuations. Published upper effects still limit a general-model claim. No physical accuracy conclusion changes.
