# Prospective amendment for parent adoption

Status: proposed before numerical execution; 2026-10-13. No campaign, compatibility simulation, benchmark, or synthetic numerical check was run for this review. The unchanged two-seed, seven-row matrix remains a numerical study of the frozen, physically unvalidated model. Every threshold below is analyst-designed; none is a physical tolerance, convergence theorem, confidence bound, or error bound.

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

No paid compute, GPU, simultaneous heavy jobs, new seeds, larger N, longer T, unplanned refinement, physics edits, publication, or empirical-accuracy claim is authorized by this amendment.
