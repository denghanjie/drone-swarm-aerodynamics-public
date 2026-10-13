# Frozen temporal-sampling protocol

Adopted 2026-10-13T11:45:07Z before numerical execution. The priority amendment at the end overrides any ambiguity or conflict in the original proposal. No experimental outcomes were observed during drafting. Harness source review is ongoing; all source and configuration hashes must be frozen before the compatibility run.

Baseline evidence checkpoint: `63befe815c85f76d42fe843b9a69bcaaa363e05c`. This is a new numerical campaign, not a physical-validation study. The verified literature audit is `research/research-audit-20261013/`; model provenance and limitations are recorded there. Reference thresholds here are analyst-designed empirical screens, not a published convergence theorem.

# Proposed bounded temporal-reference cycle

Status: adopted prospectively on 2026-10-13 before any numerical case. This plan and the priority amendment below must be frozen before numerical execution. This is a new numerical study of the frozen model, not an amendment that changes old results. No physical-model parameter fitting, new physics, GPU, publication, or full mission is implied.

## Selection and purpose

Prioritize this over the earlier runtime-attribution proposal. Temporal reference quality is prerequisite to interpreting any future aerodynamic approximation. Another timing study would mainly refine an already modest speed claim. The unavailable empirical data and potentially inconsistent published length normalization are separate physical-model questions: freeze the current source and explicitly condition every numerical conclusion on it. If a physics correction is later adopted, rerun this protocol under a new source hash rather than pool versions.

Competing explanations:

- A: most short-window numerical error is stale airflow sampling; independently refining physics changes little, and fixed-path force/impulse error decreases as airflow cadence shortens.
- B: physics integration, insufficient quadrature/reference resolution, or coupled feedback prevents clean cadence attribution. A small terminal position difference alone does not distinguish these explanations.

The experiment estimates temporal error within this implemented model. It does not estimate error against real airflow. Pointwise trajectory differences can include nonlinear amplification; they are not by themselves evidence of physical inaccuracy or a demonstration of chaos.

## Why existing evidence is insufficient

`research/campaign-exact-efficiency/src/boids.cjs` records positions/quaternions and held rotor inflows every 50 ms. Interior velocity, angular velocity and nominal motor thrust are absent. Full initial/final states and rolling hashes do not recover those missing states. Old frames cannot resolve 10/5/2.5 ms sampling or faithful receiver loads without invented interpolation.

The exact campaign already tested 2.5→1.25 ms physics and 10→5 ms airflow separately for one 1-second N16 seed; maximum saved-position differences were approximately 7.21 nm and 7.01 mm respectively. That is a two-level, sparse-output screening result, not an accepted force/impulse reference.

Milestone 28's source protocol, `outputs/milestone-28-source/study.cjs`, planned 2.5/1.25 ms physics and 10/5 ms airflow on long missions, judged chiefly by terminal position and matching completion/stops. Milestone 31's source uses 100 Hz local Boids and RK4; the retained roadmap reports failed long-horizon trajectory-refinement criteria. Earlier large raw mission records are not present in this checkout. This proposal does not invent their missing quantitative results or repeat full missions. It adds dense same-path load observables, three-level physics/cadence checks and two fresh seeds.

## Exact production semantics to preserve

The state has 17 entries: world position (3), world velocity (3), quaternion (4), body angular velocity (3), and nominal motor thrusts (4).

- `src/exact-aero.cjs:85–105` returns **four nonnegative scalar inflows per receiver**, not vector winds. The source/receiver-axis cosine is already applied when the field is evaluated.
- Between field updates, those four scalar values stay fixed. Do not reproject a stored vector with the current attitude; no such vector is stored in production.
- `outputs/milestone-28-source/aero.cjs:18–19` recomputes the receiver's effective rotor thrusts from the current RK4-stage nominal motor states and held scalars. The current RK4-stage attitude rotates net thrust into the world frame. Nominal yaw torque is preserved, while effective rotor thrust differences supply roll/pitch moments. Motor states evolve inside RK4 stages.
- `src/boids.cjs:15–24` orders field update, 100 Hz controller update, integration and safety checks. Preserve that ordering, source summation, wall-priority steering, all four rotors, the exact source hash and rejection behavior.
- For fixed-path endpoint diagnostics, `M.loads(y, U)` gives world thrust force and body torque when nominal rotor thrusts are nonnegative. Assert this condition. Production clamps stage nominal thrust in its aerodynamic derivative; do not silently introduce an inconsistent endpoint clamp or compare to gravity-inclusive force. Gravity cancels in the same-state force difference.

## Frozen workloads and coupled matrix

Use N=16 and T=1 second for both fresh seeds **840131 and 840137**. Exact seed-field/seed-array scanning of 360 accessible JSON, CJS and Markdown files found no declaration using either seed; see `temporal-seed-freshness.json`. This does not claim freshness against inaccessible historical archives. Use unchanged `B.initial`, genuine local 3D `B.steer(...,'boids','wall-priority')`, route, control mapping and receiver/rigid-body integrators. No seed replacement if a case fails.

Represent time by integer ticks of 1/6400 second = 0.15625 ms. Control period is 64 ticks. Field periods are 64, 32, 16, 8 and 4 ticks. Physics steps are 4, 2 and 1 ticks. Schedule events by integer modulo, avoiding floating-time equality tests.

Per seed, exactly seven coupled runs:

1. Airflow 0.625 ms, physics 0.625 ms
2. Airflow 0.625 ms, physics 0.3125 ms
3. Airflow 0.625 ms, physics 0.15625 ms
4. Airflow 1.25 ms, physics 0.15625 ms
5. Airflow 2.5 ms, physics 0.15625 ms
6. Airflow 5 ms, physics 0.15625 ms
7. Airflow 10 ms, physics 0.15625 ms

Total: fourteen fresh, one-second coupled runs. Run 1–3 first for the independent physics screen, then 4–5 for the finest airflow-reference screen, then 6–7 only after those screens pass. The candidate dense driver is run 3. It is a fine sampled-data solution, not a continuous-time exact solution.

Create a separate harness that imports the frozen functions; do not modify the old runner's allowed-step validation or frozen files. Before fresh runs, one compatibility preflight at old seed 4301, N16, dt=2.5 ms, airflow=10 ms, T=1 s must match the saved primary terminal full-state/held-field hash and work counts. This extra run checks harness semantics, not a fresh scientific replicate. Persist any failure before stopping.

## Prospective reference acceptance

All thresholds below are analyst-chosen engineering screens, **not** measured physical tolerances. Both seeds must pass separately; do not average away a failed seed. Evaluate coupled differences at every common 0.625 ms time, including all endpoints and control events. Do not align trajectories by nearest position, fit a time shift or relabel drones.

Observables: maximum over time and drone of position-norm error, velocity-norm error, attitude geodesic error `2*acos(min(1,abs(dot(q1,q2))))` for normalized quaternions, and body-angular-velocity norm error. Also retain terminal states, full-state hashes, max/min rotor thrust, minimum contact clearance, model-domain outcomes and nonfinite checks.

Physics screen at fixed airflow=0.625 ms:

- The finest 0.3125→0.15625 ms differences must be ≤0.1 mm position, ≤0.1 mm/s velocity, ≤0.1 mrad attitude and ≤1 mrad/s body angular velocity.
- Each finest difference must be no larger than the corresponding 0.625→0.3125 ms difference, allowing numerical comparison floors of 1e-8 m, 1e-8 m/s, 1e-7 rad and 1e-7 rad/s respectively. The relatively larger angular floor accounts for acos precision near identical orientations.
- No assumed fourth-order slope or Richardson estimate is required across sampled control/field events.

Airflow-reference screen at fixed physics=0.15625 ms:

- For 1.25→0.625 ms airflow, require ≤1 mm position, ≤1 mm/s velocity, ≤1 mrad attitude and ≤10 mrad/s body angular velocity.
- For each observable above its comparison floor, the 1.25→0.625 ms difference must be ≤0.6 times the 2.5→1.25 ms difference. This is a predefined empirical reduction screen, not proof of an asymptotic order or a continuum error bound.
- A failed screen means **no usable coupled numerical reference established** under this budget. Do not automatically add finer runs, extend the horizon, change seeds or loosen tolerances. Preserve and report the failure. Dense same-path diagnostics may still be reported conditionally on that driver, but may not be labeled reference-qualified.

## Fixed-path isolation and event-aware quadrature

For each accepted run-3 driver, save every step endpoint `Y[n]`, all 17 entries for all drones, at q=0.15625 ms, including n=0 and n=6400. Recompute the exact frozen field `Ustar[n] = M.fields(Y[n], {variant:'lean'}).winds` at every endpoint. This is diagnostic instantaneous evaluation on the saved path; it does not feed back into the driver.

For each proposed hold interval h in {10, 5, 2.5, 1.25, 0.625} ms, define k(n)=floor(n/(h/q))*(h/q), and hold `Uh[n]=Ustar[k(n)]`. Every h therefore sees **the same current full state**, differing only in the age of its four inflow scalars. Compute endpoint loads:

- `Lstar[n]=M.loads(Y[n],Ustar[n])`
- `Lh[n]=M.loads(Y[n],Uh[n])`

Take world-force difference and body roll/pitch torque difference. Also rotate torque differences by the current quaternion to world coordinates before integrating angular impulse. Body-torque integral alone is not a world angular impulse when attitude changes.

Integrate each error interval using event-aware trapezoids. On `[t_n,t_(n+1)]`, use the old held `Ustar[k(n)]` at **both** endpoint load evaluations; at the right endpoint subtract `Lstar[n+1]`. The next interval starts with the newly selected hold if it is a refresh event. This keeps distinct the left and right limits at field-update discontinuities. Never use a newly refreshed right-endpoint held value to integrate the preceding interval. No state interpolation is needed.

Repeat quadrature with q=0.3125 ms using every other state/field from the **same fine driver** and the same h-boundaries. This is a quadrature/sampling check, not a second trajectory simulation. Validate reference force and torque integrals as well as error integrals. If either check changes a normalized integral by more than 1e-4, or changes a normalized sampled peak by more than 1e-3, do not classify cadence pass/fail. These are 10% of the error-screen budgets below. State that reported maxima are maxima over the sampled endpoints/one-sided limits, not proven continuous-time suprema.

## Primary fixed-path outputs and screens

Let W=m*g and arm=sqrt(2)*a from frozen mechanics. Use per-drone quantities; do not sum opposing drone errors and call the cancellation accuracy. Report each seed and h separately.

1. Maximum sampled force error divided by W; screen ≤0.01.
2. Maximum sampled body roll/pitch torque error divided by W*arm; screen ≤0.01.
3. Maximum across drones and all prefixes of the norm of accumulated world-force error, divided by W*T; screen ≤0.001.
4. Maximum across drones and all prefixes of the norm of accumulated world-torque error, divided by W*arm*T; screen ≤0.001.
5. Time integral of force-error norm divided by W*T, and torque-error norm divided by W*arm*T; each ≤0.001. These prevent net-impulse cancellation from hiding rapidly alternating errors.

Also report absolute units (N, N m, N s, N m s), rotor inflow error, force/torque RMS, force/torque error versus elapsed time since refresh, number of positive rotor contributions, fraction of loaded receivers, and inflow temporal range. Denominators use fixed mechanical scales, avoiding division by an instantaneous nearly-zero torque. If no appreciable wake changes occur, label the case low-excitation rather than general evidence that 10 ms is adequate. Do not add a new tuned disturbance to manufacture a pass or failure.

A cadence is screen-qualified only if the driver-reference and quadrature gates pass and all six force/torque screens pass on both seeds. Report all cadences, not only the smallest passing one. Nonmonotone errors are retained; no smoothing/fitting of a convergence curve is allowed.

## Limited coupled interpretation

Compare runs 6–7 and all finer airflow runs to run 3 on common times. A cadence passing fixed-path loads but failing coupled position/attitude screens indicates feedback sensitivity or an overly weak load screen; it does not invalidate the same-path isolation. A cadence failing fixed-path loads already has directly observed stale-field error without trajectory divergence as an explanation. Neither result identifies chaotic dynamics by itself.

The previously used 1 cm short-window position screen may be shown as a historical comparison, but is not the new reference-acceptance screen. Do not change the controller's 10 ms cadence while studying airflow, and do not use different physics steps across the main airflow comparison.

## Resources, retention and stopping

- Exclusive serial CPU window, 300-second total wall cap including compatibility check, fresh runs and analysis; 45-second per-job cap. No concurrent heavy work, paid compute, GPU, N>16, or longer horizons in this cycle.
- Saved earlier N16/1 s lean work took about 0.10–0.12 s at dt=2.5 ms, and one recorded dt=1.25 ms case took 0.33 s. Pure step-count extrapolation puts finest runs near seconds each; extra field refreshes, dense recording and host effects add uncertainty. Expect tens of seconds to roughly two minutes for fourteen runs plus replay analysis; this is an estimate, not measured new performance. The hard cap controls escalation.
- Dense drivers alone: two ×6401×16×17×8 bytes ≈27.9 MB uncompressed. Their instantaneous four-scalar fields add ≈6.6 MB. Use Float64 little-endian arrays with explicit shape, order, tick/cadence metadata and SHA256 before/after optional gzip. Store compact per-cadence error summaries, per-drone prefix maxima, representative traces and precise offending indices; avoid duplicating full driver states for every h.
- Other coupled runs need full initial/final state, at least all common-time comparison states or lossless streamed comparison evidence, event/work counts and rolling hashes. Save enough to recompute reported maxima and locate worst cases. Suggested total uncompressed cap 150 MB; actual cap and serialization must be frozen.
- Stop on checksum or compatibility failure, any nonfinite state, invalid quaternion/input, model-domain exit, contact, exhausted wall/storage cap or missing reference gate. Save the exact stopped state, tick, held-field timestamp, attempted field inputs and error before reporting. Never compare a stopped member's shorter runtime or trajectory against a complete member as if work matched.
- No empirical-accuracy, full-mission, safe-flight or hardware-throughput claim. End with either a bounded reference/cadence screen or the specific unresolved numerical blocker.


# Adopted priority amendment

Status: adopted before numerical execution; 2026-10-13. No campaign, compatibility simulation, benchmark, or synthetic numerical check was run for this review. The unchanged two-seed, seven-row matrix remains a numerical study of the frozen, physically unvalidated model. Every threshold below is analyst-designed; none is a physical tolerance, convergence theorem, confidence bound, or error bound.

## 1. Immutable source and event semantics

Freeze SHA256 and resolved paths for exact-aero.cjs plus the complete transitive source graph (physics, aero, wake, grid, sim, geometry, factory, wall-filter and their dependencies), harness, plan and configuration. A hash of exact-aero.cjs alone does not freeze the model. Import byte-identical source through a pinned snapshot. Record Node version/platform. Do not alter controller, initial conditions, summation, receiver law, integrator, stage quaternion treatment, route or safety logic.

At each nonterminal start tick: refresh field if due; refresh controller if due; record the resulting held scalars/event timestamps; integrate with held commands/scalars; perform unchanged production safety checks. Time is integer ticks. Terminal T has no production field/controller refresh. Keep the final held field from T-h; the diagnostic Ustar[T] is separate. On a field refresh, the state is continuous but diagnostic load has distinct left and right values. Evaluate all four rotor inflows as scalars already projected onto the receiver axis when sampled. At every load call use that endpoint's current nominal motor thrust and attitude; preserve nominal yaw torque. Do not reproject held scalars or clamp negative endpoint thrusts silently. Reject invalid endpoints and keep their data.

For same-path sampled peaks, include both sides of every refresh and the terminal left limit. At t=0 only the right limit exists. On every interval [n,n+s], where s is the quadrature stride (1 or 2 ticks), use Ustar[k(n)] at BOTH endpoint held-load evaluations, while using instantaneous Ustar[n] and Ustar[n+s] for reference loads. No interval crosses an h-boundary. Reset the hold for the next interval only. Error torque has zero body-yaw component; rotate its full [dx,dy,0] vector to world coordinates at each endpoint before angular-impulse integration.

Production rejection only samples field-domain checks at refreshes; diagnostic instantaneous field evaluation must retain every frozen field-domain check at every saved dense endpoint, including endpoints between production refreshes and T. A diagnostic domain rejection is a failed driver, never a zero field or a skipped sample: save the entire offending swarm state, tick, previous production held-field timestamp, attempted inputs, and guard error/detail, and stop all numerical jobs. Such a driver cannot be reference-qualified. Do not claim continuous-time or internal-RK-stage domain validity from sampled checks. Intermediate RK quaternions need not be unit length; preserve their production use. Unit-quaternion validity applies to saved step endpoints.

## 2. Gate order and explicit failure branch

One compatibility preflight only: seed 4301, N16, 1 s, dt=2.5 ms, airflow=10 ms. Required final SHA256(JSON.stringify([final17States,finalHeldWinds])) is fabdd3452577cfdc3cb948ecd12b90c93fc74ee8673129a9737ca2d3e1265ef7; require 400 completed steps, 100 field updates, 100 controller updates, completion at T, and no stop. Persist attempted result before rejecting.

Run rows 1-3 for both seeds. If either physics screen fails, run no further coupled rows. If both pass, run rows 4-5 for both seeds. If either airflow-reference screen fails, run no rows 6-7. Only if both seeds pass both gates may rows 6-7 run. A source/compatibility, safety/domain, nonfinite, checksum, wall or storage failure stops all numerical jobs.

After a numerical reference-screen failure (not a safety/domain/resource failure), same-path replay on already completed valid row-3 drivers remains permitted within the original caps; no replacement driver or further coupled run is allowed. Label it conditional, reference_failed, and cadence_qualified=false. It can diagnose the failed study but cannot establish a qualified reference. Never screen-qualify any cadence if either seed lacks a qualified reference.

For each physics metric, finest <= absolute_cap AND finest <= max(coarser, comparison_floor). For each airflow-reference metric, finest <= absolute_cap AND finest <= max(0.6*coarser, comparison_floor). Use the original four caps and floors, separately by seed and observable. Do not infer an order or use Richardson extrapolation.

For the ancillary all-cadence coupled comparison against row 3, freeze descriptive screens of 1 mm position, 1 mm/s velocity, 1 mrad attitude and 10 mrad/s body angular velocity at all common 4-tick times. This uses the already declared airflow-reference absolute caps. These ancillary screens do not substitute for any reference or fixed-path gate, and must not be described as physical accuracy.

## 3. Recomputable quadrature checks

Let W=m*g, arm=sqrt(2)*a, D_F=W*T, D_tau=W*arm*T. Store quadrature results per drone, not a swarm-summed quantity. Fine/coarse comparisons use identical fine-driver states and identical h-events; the coarse replay takes every other endpoint without re-simulation.

At every common coarse prefix and for every drone, require norm(Jfine-Jcoarse)/D <= 1e-4 for each world-force and world-torque prefix integral, both instantaneous reference loads and signed load errors. This vector-prefix comparison prevents two different vector errors having equal scalar maxima from masking disagreement. Also require absolute fine/coarse change in each normalized accumulated error-norm integral <= 1e-4 at every common prefix. For both reference and error sampled force and body-roll/pitch-torque peaks, require absolute change in normalized scalar peak <= 1e-3. These are absolute differences of already normalized quantities, not relative percentage changes or divisions by possibly zero errors.

Use event-aware trapezoids for signed vectors, error norms, and squared-error integrals. RMS is sqrt(integral(norm(error)^2)/T), per drone; report its maximum over drones plus per-drone values. All prefix maxima are maxima over stored quadrature endpoints, not continuous-time suprema. Report every metric's worst drone/tick/side and both quadrature values. Preserve enough states and field data to recompute all screening metrics. Quadrature tests are sampling-consistency screens only: unresolved within-step peaks and discontinuity crossings remain possible.

Qualification requires both reference gates, both seeds' quadrature gates for the cadence, and all six original force/torque error screens. Report every cadence and every failure; no smoothing or seed/cadence selection.

## 4. Prospective excitation labels

Define fixed induced-speed scale v0=sqrt(W/(8*rho*pi*rotorRadius^2)). On the fine driver's left endpoints n=0..6399, receiver i is loaded when max_r Ustar[n,i,r] >= 1e-3*v0. Let loaded_fraction be the time-and-receiver average of that indicator. Define inflow_range=max_(i,r)(max_n Ustar[n,i,r]-min_n Ustar[n,i,r])/v0 over all saved endpoints.

At the same endpoint state, compare instantaneous-wake loads with zero-inflow loads. Define force_wake_amplitude=max norm(Fstar-Fzero)/W, and torque_wake_amplitude=max norm((taustar-tauzero)[roll,pitch])/(W*arm).

Label overall field excitation low if loaded_fraction < 0.05 OR inflow_range < 1e-3. Separately label force excitation low if force_wake_amplitude < 1e-3, and torque excitation low if torque_wake_amplitude < 1e-4. Thresholds are frozen analyst choices, independently of the new outcomes. Report all four raw measures and labels. Low excitation does not invalidate the reference calculation or erase numerical screen results; it prevents interpreting a passing case as sufficient evidence for a general cadence recommendation. Use 'numerical screens passed on low-excitation cases' where applicable. Do not introduce disturbances or change seeds.

## 5. Hard resource and retention rules

Replace suggested_data_cap_bytes with hard_data_cap_bytes=150000000 (decimal bytes). Charge all retained campaign-owned artifacts by logical uncompressed size, including binary arrays, JSON/text, copied sources, reports and any retained compressed duplicates; do not escape the cap by gzip, moving data elsewhere or duplicate archives. Reserve 2,000,000 bytes within the cap for failure records/manifest. Project allocation and serialization sizes before writing; fail before exhausting the reserve. Dense driver states and instantaneous fields plus common 4-tick snapshots for the other 12 runs use about 76.22 MB before metadata, so retaining this evidence fits the cap without lossy summaries.

A serial supervisor must impose total wall <=300 s from the start of compatibility through all fresh jobs, replay, checksums, serialization and analysis, and each child job <=45 s including its output writes. Include all retries; no restart resets either budget. Set cooperative deadlines slightly inside the hard limits so ordinary failures can save exact tick, state, held-field timestamp, pending field inputs and error. An external watchdog enforces the hard limits even if a synchronous computation hangs. If the watchdog kills a job before exact final serialization, retain the last durable checkpoint and explicitly mark the stopped state unavailable; never mislabel an older checkpoint as the exact stopped state. The emergency record must state whether evidence is exact or last-checkpoint only. No complete/qualified result may rely on an interrupted member.

No paid compute, GPU, simultaneous heavy jobs, new seeds, larger N, longer T, unplanned refinement, physics edits, external paper submission, or empirical-accuracy claim is authorized by this amendment.
