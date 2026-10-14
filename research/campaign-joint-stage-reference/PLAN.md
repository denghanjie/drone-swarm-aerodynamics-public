# Proposed next study: joint-state temporal reference

Status: **PROPOSED; NOT RUN; NOT A NEW REFERENCE CLAIM.** Prepared 2026-10-13 from recovered frozen source, retained campaign summaries, and primary literature. This work only inspected source/documents, checked provenance, and calculated planning counts from printed constants. No model, simulation, numerical replay, unit fixture, or implementation was executed. No remote write or paid compute was performed. Continued research is already user-authorized. The numerical work below awaits coordinator adoption, independent review, and a hash-frozen implementation; no renewed user permission is implied.

## Prospective storage amendment

Before any numerical fixture, preflight or simulation was executed, the coordinator increased only the retained-data cap from 150,000,000 to 200,000,000 bytes. Independent static accounting showed that required inputs, raw states, signature/controller streams and bounded bracket states nearly filled the initial cap before all source, metadata and failure evidence. Approximately 31.5 GB of workspace disk was available. This change preserves evidence; it was not triggered by an observed numerical outcome. The original plan is preserved in PLAN-INITIAL.md and Git commit f7ee3c703a4aa5156675e31d3065a901904b7c0e. Time caps, seeds, scenarios, numerical gates and the 2 MB failure reserve remain unchanged. See STORAGE-AMENDMENT-001.json.

## Decision

Choose **B: a true joint-state stage-wise field reference**, with a small mandatory saved-path branch/regularity audit as its preflight. Do not make the entire next cycle another diagnostic-only study, and do not simply keep halving the production hold interval until one metric passes.

Why: the previous independent physics screens passed by large margins, while all four airflow differences approximately halved. The present code holds four scalar rotor inflows fixed throughout each per-drone RK4 step; it therefore solves a sampled-data airflow system very accurately without establishing its zero-hold limit. A saved-path audit can expose a branch, domain, or controller obstruction, but cannot establish that limit. A properly defined joint-stage method supplies a different numerical route to it. Its success is a hypothesis, not an assumption.

The principal question is whether the held-input family approaches a self-consistent joint-stage solution of the same on-manifold equations, with the same sampled 100 Hz controller. “Continuous” below refers to airflow evaluation between controller events. The controller remains discrete, and the resulting system remains hybrid.

## 1. Retained result and provenance

The prior N=16, T=1 s campaign used seeds 840131 and 840137. Both physics screens passed. Both airflow-reference screens failed velocity, attitude, and body-angular-rate absolute caps. Position alone passed. All empirical reduction checks passed. The 5 and 10 ms coupled rows were skipped; their absence is not a successful result. The conditional fixed-path force/torque results do not qualify any cadence.

For airflow 1.25 to 0.625 ms at physics 0.15625 ms, the retained maxima were:

| Seed | Position, mm | Velocity, mm/s | Attitude, mrad | Body rate, mrad/s |
|---|---:|---:|---:|---:|
| 840131 | 0.889096 | 2.246735 | 2.438374 | 17.839376 |
| 840137 | 0.467362 | 2.134535 | 7.295006 | 72.349607 |

The prior caps were 1 mm, 1 mm/s, 1 mrad, and 10 mrad/s. They are analyst-chosen numerical screens, not physical tolerances. This plan retains those failures permanently and uses these already observed seeds as diagnostic cases, not fresh replicates or held-out validation.

Frozen implementation root: `../research-recovery/github/recovered/research/campaign-temporal-sampling/implementation/`. Evidence root: `../research-recovery/embedded/recovered/`.

- Prior plan SHA256: `0f528635c0c0e12dad5870fa7ccbad509029da741294e75e18bb63823033f267`
- Prior source aggregate SHA256: `dc73105f85b4f81c9a84899a117eefbb03c82b3c651a34fa9c73716f2c2c289b`
- Exact evaluator SHA256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`
- Public recovery commit supplied by the parent: `b9bd5065d02561920af27468f5e4740b301bd174`, branch `dot/spatial-wake-pruning`. Resolve the repository and paths from verified recovery metadata; do not guess a repository URL. Raw availability was reported by the parent, not independently downloaded in this planning task.

Before implementation, hash the complete transitive source graph, this adopted plan, the new harness and configuration, all input sidecars, and runtime/platform metadata. Keep the original snapshot immutable. A new algorithm receives a new identity; it does not replace the historical source aggregate.

## 2. What the inspected equations actually do

Source locations are relative to the frozen implementation root.

1. `src/coupled.cjs:25–28`: the swarm field is refreshed, then local Boids/controller commands are refreshed when due, then each drone is independently advanced using held inflows and commands.
2. `snapshot/outputs/milestone-28-source/aero.cjs:18–19`: each RK stage updates receiver nominal motor states and attitude, but uses the same four scalar inflows. Effective rotor forces change roll/pitch torque; nominal yaw torque is preserved. The nominal motor ODE remains first order. Intermediate quaternions are unnormalized; only the accepted endpoint is normalized.
3. `src/exact-aero.cjs:31–49,85–105`: the field requires unit input quaternions, computes current source axes and receiver rotor positions, and returns already-projected nonnegative scalar inflows. The hover-induced source amplitude is fixed by mass/geometry; it does not vary with source motor state. Preserve this limitation.
4. `snapshot/outputs/milestone-31-source/sim.cjs:9–25`: the controller uses genuine local three-dimensional separation, alignment and cohesion, a shared route field, pair constraints, and wall-priority repair. No scripted trajectories, per-drone slots, global trajectory planner, or leader replaces this calculation.

The crucial distinction is that RK4 with held field values is not fourth-order RK4 applied to the fully state-dependent swarm field. Refining its physics step can remove integration error while leaving hold error essentially unchanged. Conversely, updating only a receiver at an RK stage while leaving source drones at the old state is not the proposed joint-state reference.

### Known regularity risks, identified statically

- The downstream and radial cubic fades in `exact-aero.cjs:23,102` are C1 at their joins, not globally C4. Classical fourth-order accuracy is not automatic across those joins.
- `exact-aero.cjs:92–98` has a lower far-field switch and a separate near-wake rejection. At the lower far-field boundary, the radial support extends slightly beyond the 0.15 m near-wake guard: the outer support there is `3 × spread × (2.5-origin) × motorDistance`, approximately 0.1515 m. Thus a thin valid annulus can change from zero below the switch to a positive contribution above it. This is a code-derived possible jump, not evidence either retained path actually crosses it. Do not smooth it away.
- Neighbor changes, speed/tilt/motor clipping, pair-constraint creation, finite projection iterations, desired-heading degeneracy, and shortest-quaternion-error sign selection can affect the controller. A change of algebraic quaternion representation alone is not necessarily a physical controller discontinuity; compare the resulting motor commands too.
- The 20-degree tilt and near-wake guards bound the implemented model. A stage guard failure is evidence that the proposed numerical reference was not established, not permission to disable the guard.

## 3. Competing hypotheses and discriminating outcomes

H1, held-field error: a joint-stage method passes independent refinement screens; held-input trajectories approach it as the airflow period shrinks; held-input physics refinement remains small. This supports numerical hold-error attribution on the two specified windows.

H2, branch/feedback sensitivity: finite field switches or controller branch differences coincide with disagreement, or the joint-stage family itself does not stabilize. The next useful outcome is a localized obstruction with exact state/event evidence, not a new cadence claim.

H3, implementation/target mismatch: joint-stage and held-input families appear internally stable but do not approach each other. Investigate stage synchronization, geometry extension, terminal/controller events, yaw torque and source summation before claiming different physics or chaos.

Branch proximity or temporal coincidence alone cannot prove causation. No controller ablation, command replay as a replacement controller, perturbation sweep, parameter tuning, or seed replacement belongs to this cycle.

## 4. Same-equation target and quaternion convention

Let Y contain all 17 states for all 16 drones. Let C_k be the unchanged controller output computed from that run's own Y at `t_k = k × 0.01 s` and held until the next control event. Let W(Y) be the frozen `lean` field evaluator on unit-quaternion states. On the unit-quaternion manifold, define each drone's derivative as the frozen aerodynamic derivative `A.derivative(Y_i, C_k,i, W_i(Y), 'sum-rotor')`.

For stage evaluation an off-manifold extension is essential: the original field rejects nonunit RK intermediate quaternions. Adopt the following explicit extension for this candidate only:

- Make a geometry copy Π(Y) that normalizes each nonzero finite quaternion and changes no other state entry.
- Evaluate the complete swarm field once on Π(Y) for that stage.
- Pass the raw RK stage state Y_i, the current stage field, and held C_k,i to the unchanged aerodynamic derivative. Keep the derivative's original stage attitude/motor treatment and nominal yaw restoration. Do not overwrite the raw stage state with its geometry copy.
- Apply the original endpoint quaternion normalization after combining the four stages. Retain raw stage quaternion-norm defects and endpoint projection sizes as diagnostics. Reject nonfinite or zero quaternion norms before division.

This extension equals the intended equations on the unit manifold in exact arithmetic. The continuous quaternion equation is tangent to that manifold. That supplies a consistent candidate extension; it does not prove this nonsmooth hybrid problem has a unique well-resolved solution or that the implemented RK4 retains fourth order. Finite-step values can differ from other consistent quaternion extensions. The held-input arm stays byte-identical to its original integrator.

The four RK derivatives use four simultaneously constructed full-swarm stages: Y, Y+hK1/2, Y+hK2/2, and Y+hK3. Only after a full stage field is ready may any drone derivative for that stage be evaluated. Never mix old, half-stage and final source states. Source ordering and the `lean` field kernel remain unchanged.

At a controller boundary, finish the preceding step, including its final RK derivative, with the old commands. Compute new commands only for the following interval. The final time T has no new controller update. A final RK field evaluation at T is part of the preceding continuous-field step; it is not a production held-field refresh. Keep these different event meanings in logs.

## 5. Preflight, without another trajectory

After coordinator adoption and implementation review, materialize only the two retained dense `s840131-p1-a4` and `s840137-p1-a4` arrays, their sidecars, corresponding run/event records, and the frozen manifest. Verify compressed/uncompressed SHA256, shape `[6401,16,17]`, tick grid, endpoints and run identity before use.

Use saved endpoints only; do not interpolate a new state path. At every saved endpoint, evaluate signed geometry margins and branch signatures for lower far-field, near-wake guard, downstream/radial fade joins and support boundaries, plus tilt margin. Retain a per-sample branch-signature hash; retain signed-margin extrema per run and boundary category with sample/time/pair/rotor IDs, rather than complete per-sample margin arrays. At the 100 nonterminal controller times, evaluate the unchanged controller and record local-neighbor IDs, active pair/wall constraints, steering speed, desired horizontal-speed norm, torque-error sign, motor saturation, and commands. Match the resulting command hashes to the retained production events. An independently computed diagnostic trace must not feed back into any trajectory.

Retain the first and worst bracket per boundary-signature category over all pairs, with whole swarm inputs and exact sample roles/IDs. This is not a first/worst record for every individual pair; all pairs are still audited and coverage counters are retained. Do not restrict the audit to the historical worst drone. Endpoint brackets are not exact crossing times, and a no-crossing sample record is not proof of continuous regularity. A merely continuous fade/clip switch is reported but does not automatically halt the study. A bracket implicating the valid-annulus finite field jump is an unresolved-discontinuity blocker for the smooth-reference interpretation: preserve it and stop before new coupled runs, rather than claiming ordinary RK order. A domain/input rejection or hash disagreement also stops the cycle.

Apply the same branch audit to every new trajectory: J at every field stage and accepted endpoint, H/P at every accepted endpoint and production refresh. Compare controller branch signatures and actual motor commands at every control event across matched runs. These traces are mandatory diagnostics and are charged to the resource caps. H/P endpoint checks do not certify internal-stage or continuous-path regularity.

Freeze a conservative finite-jump risk detector as follows. For each receiver-rotor/source pair, consider all geometry samples belonging to one step (for J, start, both half-stage states, final stage and accepted endpoint; for H/P, the two accepted endpoints). Flag unresolved jump risk when the sampled downstream range contains `farStart` and the sampled radial range overlaps `[nearFieldRadius, outerSupportAtFarStart)`. Equal-time J half-stage values are different trial states, not time-ordered observations. Store the endpoint-only bracket test and the full RK-trial-sample test as separate flags, with the exact role/time of every sample. The detector is therefore a conservative possible-crossing test, not an event locator. Save every flagged step and the complete sampled inputs; stop new numerical jobs and withhold reference acceptance. The same sampled-range rule applies to each consecutive pair of saved preflight endpoints. No automatic bisection, altered step, new state interpolation or discontinuity smoothing is added in this cycle. False positives remain an explicit inconclusive outcome; no flag is not proof that an unsampled crossing was absent.

The proposed preflight is a small prerequisite to B, not a claim that A has already diagnosed the prior failure. Current planning did not read the raw arrays or evaluate these diagnostics.

Implementation fixtures, before any new coupled run, must check full-swarm stage synchronization, a simple coupled analytic ODE's RK stages, zero-inflow reduction, geometry-copy nonmutation, controller-boundary left-command semantics, endpoint normalization, domain-failure retention, skipped-row logic, and raw-array/checksum round trips. Distinguish fixtures from genuine Boids runs. No fourth-order fixture on a smooth ODE establishes order for this model. A compatibility run must reproduce the historical seed-4301 final state/held-inflow hash and work counts; its attempt and any failure remain retained.

## 6. Bounded coupled matrix

Unchanged N=16; T=1 s; seeds 840131 and 840137; original initial state, 100 Hz local 3D Boids, route, wall-priority controller, mechanical/receiver/wake parameters, ordered source sums, and production contact checks. No new disturbance. All simulations are offline serial CPU.

Use an integer base tick of 1/51200 s = 0.01953125 ms so every stage half-time and every event is representable. Controller period is 512 ticks; common comparison/output period is 32 ticks = 0.625 ms. Retain T exactly, with no terminal held-field/controller refresh.

Per seed, at most eight new coupled runs:

| Arm | Physics step, ms | Field handling | Purpose |
|---|---:|---|---|
| J1 | 0.625 | Full joint stage field | Coarse continuous-field candidate |
| J2 | 0.3125 | Full joint stage field | Intermediate candidate |
| J3 | 0.15625 | Full joint stage field | Fine candidate |
| H1 | 0.078125 | Hold 0.625 ms | Bridge to retained production family |
| H2 | 0.078125 | Hold 0.3125 ms | Hold refinement |
| H3 | 0.078125 | Hold 0.15625 ms | Hold refinement |
| H4 | 0.078125 | Hold 0.078125 ms | Finest prescribed hold |
| P1 | 0.0390625 | Hold 0.078125 ms | Independent finest-hold physics check |

Run preflight/fixtures/compatibility first. Run J1–J3 for both seeds and evaluate their gate before starting H rows. If either joint gate fails, stop coupled work and report the failure. If both pass, run H4/P1 for both seeds and evaluate the independent physics gate, then H1–H3 for both seeds if it passes. A numerical gate failure ends new coupled jobs; bounded analysis of already valid retained records may finish within the same resource caps. Any domain/safety/resource/integrity failure stops all numerical jobs immediately.

This is 16 new one-second trajectories at most, plus one historical compatibility run. It does not resurrect the previous skipped 5/10 ms rows. No automatic extra level, alternate seed or longer horizon is permitted.

## 7. Acceptance and interpretation

Evaluate maxima over all drones and all common 0.625 ms endpoints, including initial/final and controller times, with no time alignment, relabeling or averaged-seed pass. Keep complete common full17 states so every reported maximum is recomputable. Use the retained normalized-quaternion geodesic comparison, with its known near-zero floor. Also retain stable relative-quaternion atan2 diagnostics, but do not silently change the primary historical comparator.

### Joint-stage refinement screen

For each seed separately, J2–J3 differences must be at most 0.1 mm position, 0.1 mm/s velocity, 0.1 mrad attitude, and 1 mrad/s body rate. Each finest difference must also be at most `max(0.6 × corresponding J1–J2 difference, comparison floor)`. Floors remain `1e-8 m`, `1e-8 m/s`, `1e-7 rad`, and `1e-7 rad/s`.

No safety/domain failure, nonfinite value, incomplete row, or integrity failure may pass. The result of this gate alone is “joint-stage self-consistency screen passed,” not an accepted exact reference or a proved fourth-order result.

### Held-input physics screen

H4–P1 must satisfy the same four small absolute caps. This two-level screen tests integration contamination at the new finest hold; it is not an order estimate. H1 must additionally agree with the retained 0.625 ms-hold / 0.15625 ms-physics path within the same small caps, after exact initial state/controller/source identity checks. This is a bridge check, not another new run.

### Cross-family approach and bounded numerical-reference status

Let E(h) be each of the four maximum common-endpoint differences between H(h) and J3. Require all three successive hold halvings to obey `E(h/2) <= max(0.7 × E(h), comparison floor)` for each seed/observable. The 0.7 factor is a new prospective empirical screen, not a theoretical order or error bound.

Require H4–J3 to be within the original four absolute caps: 1 mm, 1 mm/s, 1 mrad, 10 mrad/s. Both seeds must pass all joint, held-physics, bridge and cross-family screens. Only then label J3 a **bounded, cross-checked numerical reference for these windows and this frozen model**. Record numerical differences, not estimated truth-error bars.

If J passes but H4 fails a cap, retain “joint-stage self-consistency observed; cross-family reference not established within budget.” If reduction fails, retain nonmonotonicity and branch/controller histories; do not smooth a curve or cherry-pick a seed. Even a successful reference does not itself qualify any operational airflow cadence: the prior same-path force/torque screens remain conditional on their old drivers. Re-evaluating force/torque cadence qualification on a newly accepted driver would need a separate bounded plan.

## 8. Cost, raw requirements, retention, and stopping

No raw download is needed to adopt this proposal. Execution requires only the two original dense drivers, matching run/event JSON and sidecars, and the frozen source/manifest initially. The original instantaneous-field arrays are optional for checksum-backed consistency comparison; do not download them unless that check is explicitly included and storage accounted. All legacy files remain immutable.

The two original dense arrays occupy 27,857,152 logical bytes (26,736,688 stored gzip bytes) according to the retained manifest. For the new results, keep J3 dense endpoints for both seeds and common endpoints for the other 14 rows, without duplicate J3 common arrays: exactly 76,630,016 logical bytes. The combined old/new uncompressed state data are 104,487,168 bytes. The separately coordinated input-acquisition task plans to preserve both the original gzip parts and decompressed inputs; charging both raises the baseline to 131,223,856 bytes, leaving 68,776,144 bytes for all source, metadata, logs and fixtures, including the 2,000,000-byte failure reserve. That accounting is mandatory unless a prospectively documented retention change avoids a duplicate without losing provenance. No deletion is requested by this plan. Store arrays as little-endian Float64, with shape, field ordering, base tick, cadence, run identity and compressed/uncompressed hashes.

Retain full initial/final states, commands at every control event, all actual event/work/coverage counts, first/worst branch brackets per boundary category with whole swarm states, all comparison maxima and indices, source/runtime identities, per-run timings, all failures and skips, per-sample branch-signature hashes, per-run signed-margin extrema with indices/times/pair IDs, and rolling full-stage input/field/derivative hashes with a fully specified encoding. Every required margin is evaluated at every required sample/stage; complete margin arrays are not saved. Full retained accepted states allow their geometry margins to be rederived. General J stage histories are not retained: only first/worst/failing raw stage inputs are saved, so a stage hash does not establish full-stage reconstructibility. For a failed stage save its actual raw state, normalized geometry input, commands, field values if available, and exact failing guard. Retain a separate last-durable-checkpoint record if interruption prevents exact final-state capture; never label it exact. For J stage or projection failures, retain the actual offending raw trial/endpoint and available field/commands. The unchanged held integrator exposes no internal-stage exception hook: an unexpected exception inside H/P integration retains the exact pre-step input, held winds, commands and vehicle ID, labeled exactIntegratorInput=true and exactStoppedState=false; the hidden intermediate state is unavailable. Do not alter or replay the baseline to fabricate an original failure state. This limitation is prospective, and such a failure stops the cycle with no reference acceptance.

Compact branch-signature traces are provisionally estimated near 10 MB rather than approximately 34 MB for full margin traces. The implementation must calculate the complete logical allocation/serialization forecast, including all category brackets and metadata, before coordinator freeze. These are estimates, not permission to overrun the 200 MB cap or failure reserve.

Proposed hard limits: serial CPU, 300 s total wall and 300 CPU s for the complete numerical window, 45 s per job including writes, 200,000,000 logical retained bytes including materialized inputs/new data/source/logs and any duplicate forms, and a 2,000,000-byte failure reserve inside that cap. Do not retain both compressed and decompressed copies without charging both. Stream one run/input where practical. Include tests, compatibility, analysis, serialization, checksum work and retries in the numerical window; input acquisition and document preparation are separately recorded and are not simulation benchmarks.

The prescribed new matrix contains 176,000 swarm steps and 11,264,000 vehicle RK derivative evaluations before optional diagnostic work. Its dynamics require 163,200 whole-swarm field evaluations, excluding endpoint/preflight diagnostics. Require stage and accepted-endpoint domain checks for J; count any extra endpoint field evaluations separately. H retains its original production refresh checks; do not claim H's field domain is verified continuously or at all stages.

Using the previous instrumented N16 costs only as a rough linear proxy suggests about two to four minutes for the full cycle, with substantial uncertainty from stage field evaluation, hashing, retained data and runtime warmup. This is a planning estimate, not measured performance. If the cap is insufficient, retain the terminal evidence and stop. Do not restart a new budget, drop inconvenient validation, or silently loosen caps.

Time field, controller, RK arithmetic, safety/diagnostics, recording/hash work and total job wall separately. Report matched completed work, field/kernel counts and numerical discrepancy together. These one-off instrumented timings are not a browser speedup or an accuracy-cost frontier. No renderer, GPU, N>16, mission extension, physical refit, external submission, deployment or remote repository write is in this plan.

## 9. Original eight-step framework remains intact

1. Define the experiment: freeze the above target, hypotheses, metrics and budgets.
2. Build one credible drone: mechanics checks are retained; measured-flight validation remains absent.
3. Model two-drone interaction: mean-wake provenance is retained; receiver-force validation remains open.
4. Model overlapping wakes: isolate temporal numerical error in the existing superposition/receiver model; do not upgrade its physical status.
5. Test a real local flock: every coupled row uses genuine local 3D Boids in the original factory workload.
6. Accelerate validated calculations: this reference is a prerequisite for later matched CPU/WebGPU comparisons, not a new acceleration claim.
7. Scale the actual flock: N16 is a diagnostic gate; the objective remains 5,000 coupled browser drones with documented density/spacing and measured simulation budgets.
8. Evaluate the contribution: retain errors and failures, then compare physical/numerical accuracy against actual computation cost and appropriate baselines. A visually convincing replay or higher frame rate is not the scientific result.

## 10. Primary-source verification and limits

All four sources below were directly opened on 2026-10-13. They support method design or model provenance, not the numerical outcome of this unrun plan. No secondary-source claim is needed for the recommendation. Machine-readable consultation/correction-check records and prospective literature-to-experiment links are in `bibliography.json` and `literature-experiment-ledger.json`.

- Bauersfeld et al., *Robotics meets Fluid Dynamics*, arXiv:2403.13321v3, 12 Dec 2024. The author-deposited record identifies RA-L publication; v3 states acceptance on 28 Nov 2024. Inspected sections III-A–D (geometry/normalization), VI-C (mean far-field construction), VII-A, equations 10–11 (hover-power compensation), and VIII (limitations). These do not validate the implementation's transient receiver-thrust inversion, finite-support fades, multiple-wake aggregation, or 27 g drone. The DOI landing page was inaccessible in this session, so final journal pagination is deliberately not asserted. [Full text](https://arxiv.org/html/2403.13321v3), [version/status record](https://arxiv.org/abs/2403.13321).
- Nordam and Duran, *Numerical integrators for Lagrangian oceanography*, **published** GMD 13, 5935–5957, 1 Dec 2020, DOI 10.5194/gmd-13-5935-2020. Inspected §2.1, equations 5–7; §2.2, equation 9 (stage-state evaluations); §3.1–3.3 (regularity/discontinuities and event-aligned integration). Supports checking smoothness and event semantics instead of assuming RK order. It studies a different physical system and does not validate drone tolerances or this extension. [Publisher full text](https://gmd.copernicus.org/articles/13/5935/2020/).
- Hairer, *Symmetric projection methods for differential equations on manifolds*, **published** BIT 40(4), 726–734 (2000), DOI 10.1023/A:1022344502818. Read the author-hosted 25 May 1999 preprint, §1, pages 1–2: an off-manifold vector-field extension is needed for standard projected methods; order preservation is conditional on the smooth setting. Publication metadata independently matches the author's institutional repository. We use ordinary endpoint projection, not Hairer's symmetric algorithm, and claim neither symplecticity nor reversibility. [Author preprint](https://www.unige.ch/~hairer/preprints/symproj.pdf), [institutional publication record](https://archive-ouverte.unige.ch/unige:12526).
- Mørk, Nordam and Rühs, *Handling discontinuities in numerical ODE methods for Lagrangian oceanography*, **published** GMD 18, 7831–7851, 27 Oct 2025, DOI 10.5194/gmd-18-7831-2025. Inspected §2.1–2.3, §3.2 (event detection and spatial crossing localization), and Appendix C, equation C1 (numerical reference refinement). This later study reinforces that spatial boundary crossings require separate treatment and that ever-smaller steps do not guarantee better accuracy. It supports retaining an unresolved-crossing outcome here; its oceanographic results do not supply drone error bounds. No event-location implementation or reference data were imported. [Publisher full text](https://gmd.copernicus.org/articles/18/7831/2025/gmd-18-7831-2025.html).

**Stopping outcome:** either a cross-checked bounded numerical reference for the unchanged on-manifold model on these two windows, or a precisely retained numerical/domain/implementation/resource obstruction. Neither outcome establishes physical truth, safety, general navigation, novelty, or 5,000-drone browser feasibility.
