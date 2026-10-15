Public edition of the frozen prospective protocol. Original SHA256: 1b5375f79cf8c1da955d64408dd6f81ce31ed2584c106ceb6f832884a95d6361. Local resource/admission routing is summarized; scientific settings and gates are unchanged.

# Causal stage-airflow predictor: prospective draft

2026-10-15 UTC. IMPLEMENTATION PROTOCOL; execution needs separate release. ID: CAUSAL-AIRFLOW-PREDICTOR-20261015. Freeze the reviewed plan/config/code before one released attempt. The earlier public-reference qualification remains GATE_STOP, unchanged.

## Question and fixed design

Can causal stage-dependent linear-plus-nonnegative-clamp airflow prediction reduce trajectory error fourfold versus zero-order holding (ZOH), at identical scheduled field counts? Keep the same finite-support physics, receiver closure and genuine own-state local-3D Boids. No physical accuracy, speedup, stability, order or novelty claim follows. The 2026 measured-amplitude/observable mismatch remains unresolved.

Use public commit 1336f5c416875a9651f92b58b2ed06649f25b04e and the public source identities in [SOURCE-MAP.json](SOURCE-MAP.json). Hash-check original modules through the reviewed in-memory path map. No private R8 reconstruction or refit. Factory=wide, airflow=sum-rotor, evaluator=lean.

N=16; seeds 840149 and 840163, selected without initialization/model previews, new relative to the preceding qualification. Q=1/51200 s; horizon=5120 ticks=0.1 s; controls every 512 ticks; accepted-state comparisons every 128 ticks. No seed replacement.

First run joint-field whole-swarm RK4 at h=128/64/32 ticks for BOTH seeds. Both references must qualify before approximation work. Then, per seed: ZOH h=16/8 and predictor h=16/8, all with air=64 ticks=1.25 ms. Fourteen scientific arms. One cadence gives no cadence-order estimate. Cadence64 follows a resolved cap failure on an earlier exploratory seed; new outcomes cannot tune it.

All arms copy one initializer output per seed and use their own evolving state for controller decisions. Both approximations use the same synchronized RK4 wrapper: normalized trial geometry for monitoring, original raw trial states for derivatives, original endpoint projection. Their stage callback supplies held/predicted scalars without a wake evaluation. Joint arms evaluate a complete fresh field each stage. Preserve original derivative/contact/controller arithmetic and source bytes.

## Predictor and events

For each receiver/rotor retain two fresh fields from its own arm: U_n at refresh tick t_n and U_previous at t_n-64. At stage tick t in [t_n,t_n+64], alpha=(t-t_n)/64, raw=U_n+alpha*(U_n-U_previous); supply max(0,raw). Use RK fractions 0,1/2,1/2,1, including old-interval alpha=1 at its final stage. No future field or accepted endpoint substitutes for a trial stage. 
At t=0 obtain one scheduled field. Missing history means ZOH until tick64, with no artificial prior sample or extra warm-up evaluation. Later refreshes shift actual samples. No slope cap, smoothing, history reset, rollback, adaptive refresh or fallback after startup. History spans controller events: accepted geometry is continuous, but commands/higher derivatives can change. At shared events: observe incoming approximation, refresh field, update controls, integrate. No terminal production refresh/control.

Clamp negative predictions to zero; nonfinite predictions stop. Record raw minimum/negative-excursion witness, clamp count, affected stage vectors, distinct receiver/rotor indices and startup-hold stages. Diagnostic counters are separate. Active-clamp results describe the clamped method, not pure linear extrapolation. Geometry-triggered recovery is deferred.

## Compatibility within this attempt

Reproduce seed4301 initialization and four legacy held h128/air512 steps against the five public saved states byte-for-byte. With the same initial state, commands and sole field, repeat four steps using the new ZOH stage callback. Report bit equality and require maximum component difference<=1e-12 across all five states. Original zero-wind quaternion projection uses reciprocal multiplication while the joint wrapper uses division; change neither original. This is fixture-only compatibility, not universal equivalence. Record all-zero-wind dispatch and raw-stage nominal motor exposure; failed equivalence stops.

Four scalar fixtures at alpha=0,0.5,1 check arithmetic without wake calls: constant(prev=2,current=2)->(2,2,2); affine(1,2)->(2,2.5,3); declining(3,1)->raw(1,0,-1), output(1,0,0); missing-history/current=2->(2,2,2). These 12 evaluations are software checks. Verify source/config hashes and input nonmutation before/after. First lean field per new seed must equal original A.fields on identical geometry; count those two extra evaluations.

## Qualification and candidate decisions

Metrics: position norm(m), velocity norm(m/s), sign-invariant relative-quaternion angle(rad), angular-rate norm(rad/s), in that order. Maxima cover 16 vehicles and 41 common times. Unchanged small caps=(1e-4,1e-4,1e-4,1e-3); outer caps=(1e-3,1e-3,1e-3,1e-2); floors=(1e-8,1e-8,1e-7,1e-7). These are numerical goals, not physical tolerances.

Reference gate, each seed/metric: J64-versus-J32 maximum<=small and <=max(floor,0.6*(J128-versus-J64 maximum)); require nonzero production inflow. Failure stops before approximate arms as REFERENCE_UNQUALIFIED. No seed/step substitution.

After reference qualification complete all eight approximation arms unless safety/resource/source checks stop. Score all comparisons; a ZOH absolute-cap failure does not abort scoring. Each method/seed h16-versus-h8 maximum must be<=small. Let E_Z,E_P be h8 errors against J32; d_J,d_Z,d_P are joint-fine/fixed-method h differences. For each method U=max(d_J,d_method)<=0.1*E_method; if E_method<=floor instead require U<=floor with no resolved-error/order claim. Failure makes attribution NUMERICALLY_UNRESOLVED. These h differences are proxies, not certified bounds.

Candidate acceptance requires BOTH seeds and every metric: E_P<=outer; where E_Z>floor also E_P<=0.25*E_Z. Where E_Z<=floor require E_P<=floor and label that cell uninformative about fourfold improvement. Require at least one resolved baseline metric per seed; otherwise INCONCLUSIVE. All numerical qualification, exposure, count and domain checks must pass. Fourfold is a prospective useful-effect target, not a theoretical promise. Report every failed cell and ZOH absolute-cap status separately. Baseline failure neither aborts scoring nor becomes a pass. Unfavorable efficacy is CANDIDATE_TARGET_FAILED; favorable is CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW. Neither releases another run.

## Guards and observations

Apply the reviewed monitor's unchanged predicates to accepted endpoints AND normalized RK-stage geometries for all methods. This improves sampled coverage equally for ZOH/predictor, without continuous-time guarantees. Require nonnegative initial motors/commands and raw-stage motors, with h/motorTau<=1/16. Preserve near-wake/tilt/finite-state predicates, coordinate<=1e6 m, endpoint motor/ground checks, segment contacts, controller repair failure and all-pair finite-jump screening over each step's samples. Radial/axial smoothstep fades are C1; the far-start annulus can have a finite jump. Do not smooth that jump or call every support crossing discontinuous.

Retain guard margins/signature changes, controller branch differences, clearances, repair/clip counts, maximum field, source-pair visits and predictor exposure. At controller-grid times including 0/5120, compare incoming approximate wind/load with a fresh same-state field BEFORE refresh. At tick0 diagnose after initial field acquisition, without fictitious history. Joint diagnostics use fresh endpoint fields. Auxiliary fields never enter integration/history. Retain field age, inflow/force/roll-pitch gaps, state maxima/terminal metrics, commands and bounded paired-state witnesses. Separate same-state lag from cross-arm state/control divergence. No dense-time extremum claim.

## Work, retention and stopping

Each approximate arm has 80 production fields including startup, 10 controls and 11 auxiliary fields. Matched h has identical field/derivative counts for predictor and ZOH; arithmetic and wall/CPU overhead differ. Equal field counts are not equal total work or speedup. Scientific totals: 4400 steps, 281600 vehicle derivatives, 2880 production fields, 140 controls, 154 auxiliary fields, plus 2 baseline checks. Compatibility adds 8 steps, 512 derivatives, 1 shared field and 1 shared controller call. Scalar checks add no fields. Count callbacks/clamps and every evaluation; unexplained extra fields fail equal-field accounting.

Original execution used a separate hash-bound release, a 20 s whole-launch cap and one attempt. Private admission inventories and host logs are excluded. This archival source edition does not authorize execution or provide a standalone runtime bundle.

## Verified primary background

[CHOPtrey (SIMULATION93(3),2017, §§3.4.2,5.2-5.3)](https://arxiv.org/html/1610.09261v2) already covers causal polynomial extrapolation, context/history changes and holding fallbacks. [Chen et al. (2021), §§2.1-2.2](https://link.springer.com/article/10.1007/s11044-021-09785-x) analyze coupling error under LTI/low-aliasing assumptions and discuss stability limits. Neither proves order/stability for this hybrid/clamped flock. Coordinate literature detail with the physics review; no duplicate assets.
