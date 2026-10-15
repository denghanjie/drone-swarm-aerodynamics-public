# Public edition of the prospective finite-support sensitivity plan

Public redacted edition prepared after the run. The original prospective plan was frozen before execution with SHA-256 2879a16281c5ce16ef064165fbcd9254ccf77ca6fde7759844144838305add44. This edition is not byte-identical to that original. It retains scientific methods and removes private recovery/workspace-accounting and coordination text. See ../PUBLICATION.json for hash mapping. Results are in ../results/REPORT.md. Archival implementation is in ../implementation/run-support.cjs; the public subset is not a standalone rerun bundle.

## Recommendation and hypothesis

Run one fixed-state, all-pairs field/load comparison on the existing 401-frame, 16-drone public trajectory. Determine whether artificial finite support materially changes the predicted rotor inflows, total thrust, and roll/pitch moments in this particular trajectory. This addresses a scientific approximation directly, rather than another audit-cost study.

Primary question: how much does removing the axial fade/cutoff while preserving the radial fade change predicted loads on this saved sequence, and which source geometries cause that change? Secondary contrasts isolate radial-tail sensitivity and its interaction with axial truncation. All comparisons concern the stipulated mathematical model; none establishes which arm is physically accurate.

The existing run JSON claims genuine local 3D Boids on its own evolving state. Its saved states remain byte-for-byte unchanged. This study evaluates aerodynamic outputs on those states; it is an open-loop replay, not a new flight, a newly closed-loop Boids experiment, or evidence that a changed aerodynamic model would preserve those trajectories.

## Minimal available kernel and missing capabilities

Let J = research/campaign-joint-stage-reference/implementation in the [pinned public source tree](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/1336f5c416875a9651f92b58b2ed06649f25b04e/research/campaign-joint-stage-reference/implementation).

The minimum runnable dependency closure is:
- J/snapshot/outputs/milestone-28-source/aero.cjs
- J/snapshot/outputs/step02c-source/physics.cjs
- J/snapshot/outputs/step03a-source/wake.cjs
- J/snapshot/outputs/milestone-26-source/grid.cjs

These are CommonJS modules using only each other. They supply the original finite-support field, rotor layout/rigid-body quantities, normalized mean-wake formula, thrust response, and neighbor search. A new runner can load these files read-only; no package install, clone, remote access, paid compute, copied source tree, or audit loader is needed. Optional J/src/exact-aero.cjs and source.cjs are available but unnecessary for this experiment.

Input is J/results/raw/s4301-compatibility.common.f64 and its adjacent .json sidecar, plus J/results/runs/s4301-compatibility.json. Shape is [401,16,17], Float64 little-endian, 872576 bytes; row cadence is 0.0025 s, duration 1 s. Input SHA-256 is 055fa27e4b7baeb3e363a2f6a912a4fd50b44cb52ce948d23e061dffd8c4ed8d. Read it in place. Do not duplicate it into new evidence.

The saved config says kind=held, physics step 128 ticks, air/control interval 512 ticks, base tick=1/51200 s. The historical run refreshed air at 100 times, but this proposed diagnostic evaluates the instantaneous field at all 401 saved endpoints. It does not reproduce the historical held-air forcing or reinterpret endpoint replay as production refreshes.

The local3D swarm controller, controller-record implementation, swarm factory/simulator, runner, and joint-step source bytes are absent from this selected subset. Their hashes appear in predecessor provenance, but hashes are not source. Do not replace them with physics.cjs's single-drone target/controller or a scripted formation. Fresh closed-loop research requires the genuine pinned controller closure in a separate future step. R3 corpus.cjs describes historical decoding but imports unavailable audit modules; do not execute it or present it as R8.

## Exact model and known limitations

Original A.fields(states,'sum-rotor') is the baseline. Use sum-rotor only. Hold rotor point geometry, source direction, receiver/source cosine, source hover amplitude, source summation rule, receiver thrust closure, and nominal yaw torque unchanged in every arm.

Constants in source:
- D = 2*sqrt(2)*0.028 m; rotor offset from body center is D/2.
- Rotor radius 0.023 m, mass 0.027 kg, density 1.225 kg/m^3, g=9.81 m/s^2.
- Far-field start d0=2.5D; near-core exclusion r<0.15 m for 0<d<d0.
- Downstream speed fade from d=2 to 2.5 m; zero at/after 2.5 m.
- Radial speed fade from xi=2 to 3; zero at/after xi=3.
- Source-center search radius 3 m; allowed source/receiver tilt <=20 degrees.
- b(d)=0.07668*(d+5.817D); xi=r/b; Uc(d)=10.11*D*vi/(d+5.817D).
- vi=sqrt(m*g/(2*rho*pi*rotorRadius^2*4)); u(d,r)=Uc/(1+(sqrt(2)-1)*xi^2)^2.

This is a hovering-source mean-field formula adapted to a moving, tilted swarm. Source amplitude ignores instantaneous source thrust; superposition and fixed-ideal-power receiver response are unvalidated modeling choices. Free-air, hover, scale, and quasi-steady assumptions are not established by the saved trajectory. The selected source's 20-degree limit is an exploratory code limit, not empirical validation.

Physics review of Bauersfeld v3 reports that the analytic radial tail overpredicts measurements for xi>2, with noise dominant beyond xi>5. Therefore a larger radial support is not automatically better physics. Keep core xi<=2, transition 2<xi<3, outer 3<=xi<=5, and extreme xi>5 contributions separate. The reviewer also identifies a mass-scale extrapolation: the 27 g-like kernel is below the paper's fitted vehicle set. These literature points require the separate physics review's citations in any public write-up; they are not new measurements from this experiment.

## Four arms, plus one cheap baseline reproduction check

Use ascending source index, receiver-major/rotor-major traversal, identical arithmetic where practical. Enumerate all 15 other sources in research arms. Compute the untapered formula once per eligible pair and apply these weights:

P: both original axial fade and original radial fade. This all-pairs reconstruction must reproduce the untouched original grid-based A.fields output.
X: remove axial fade/cutoff; retain the original xi=2..3 radial fade. This is the primary contrast X-P. Removing the neighbor gate is necessary when extending axial range.
R: retain original axial fade/cutoff; remove radial fade/cutoff. This is the radial-tail contrast R-P, not an improved-physics arm.
U: remove both artificial tapers/cutoffs. This is the finite-population, untapered-formula sensitivity envelope. Its difference from P contains both omissions; interaction is U-X-R+P at the inflow level.

No empirical upper-domain claim is made for U or for added distant contributions. All arms use only the finite 16-drone population; U is not an infinite-swarm limit. Report maximum downstream distance and xi of newly admitted contributions. Do not add a radius/cutoff sweep or tune parameters to the result.

All arms retain the same domain rules:
- Validate 17 finite state entries, nonnegative nominal rotor thrusts, quaternion norm within 1e-10, and source/receiver tilt <=20 degrees.
- For d<=0, contribution is zero under the stipulated model.
- For 0<d<d0 and r<0.15 m, stop with the exact row/drone/rotor/source witness; do not fill in a near-wake formula.
- For 0<d<d0 and r>=0.15 m, do not extrapolate the far-field formula. Record these as unmodeled/excluded pairs, not physically measured zero flow.
- For d>=d0 use the profile and applicable taper weights.

Changing source strength, source interaction, disk averaging, superposition, rotor response, or dynamic integration is outside this study.

## Why a radius-only sweep is unnecessary

With original support, every contributing rotor-source displacement satisfies d<2.5 m and r<3*0.07668*(2.5+5.817D). Therefore its receiver-center/source-center distance is at most

sqrt(2.5^2 + [3*0.07668*(2.5+5.817D)]^2) + D/2 < 2.64 m < 3 m.

Add a conservative 1e-6 m margin for tiny accepted quaternion deviations and roundoff; this does not bridge the >0.36 m margin. The original 3 m grid gate is conservative for original nonzero support. Near-core guard geometries are also much closer than 3 m. Enlarging that radius alone cannot test a meaningful truncation error here.

Verify this bound numerically as one scalar preflight assertion, and compare all-pairs P against the original grid-based field on all 401 rows. Any mismatch invalidates that implementation/check; do not reinterpret it as an aerodynamic effect. A source outside the original support can legitimately contribute to X, R, or U after their support definition changes.

## Cheap analytic probes before replay

Use a fixed 25-point single-source profile grid: d in {1,2,2.25,2.5,3} m and xi in {0,1,2,2.5,3}. These are scalar profile probes, not manufactured Boids states or new flight trajectories. Compare P/X/R/U weights against direct smoothstep calculations and retain the small grid.

Specific predictions, derived algebraically before execution:
- Axial fade equals one at 2 m, one half at 2.25 m, and zero at 2.5 m.
- For a core point, P at d=2.25 m has half the speed of X; at/after 2.5 m P has zero while X can remain positive.
- Radial fade is one at xi=2, half at xi=2.5, and zero at xi=3.
- U>=X>=P and U>=R>=P, up to the declared floating tolerance.

Optional analytic interpretation, not an extra numerical quadrature campaign: for c=sqrt(2)-1, the untapered mean-flow momentum proxy is rho*integral(u^2*2*pi*r*dr)=rho*pi*Uc^2*b^2/(3c), independent of downstream distance because Uc*b is constant. Axial speed taper multiplies this proxy by its square. Thus at 2.25 m the axial taper alone reduces this proxy by 75%, and at 2.5 m by 100%, relative to the stipulated continuation. This is not total turbulent momentum conservation or experimental validation; Reynolds stresses and other physics are absent. Radial taper also changes the proxy. No additional quadrature is needed for the core question.

## Physical observables and interpretation

At each of 401 times and 16 receivers, compute four inflows in m/s and loads using the SAME original A.effectiveThrust, F.wrench and quaternion rotation. Preserve nominal yaw torque, as the original model does. Describe outputs as model-predicted loads, not measurements.

For each X-P, R-P, U-P contrast report:
1. Maximum rotor inflow difference in m/s and divided by vi. Also report global max inflow, and descriptive median/p95/max across receiver-times. Avoid relative error divided by a possibly zero baseline inflow.
2. Total thrust difference in N and divided by mg; world-force difference norm is the corresponding scalar magnitude for the unchanged unit attitude.
3. Roll and pitch moment differences in N m, normalized by m*g*a, and corresponding instantaneous angular-acceleration changes Delta_tau_x/Ix and Delta_tau_y/Iy in rad/s^2. Yaw change should be zero by this fixed model convention.
4. Count/fraction of receiver-times exceeding each screening budget, and exact row/receiver/rotor witnesses for extrema.
5. Contributions from core/transition/outer/extreme radial bins, split by d<2, 2<=d<2.5, and d>=2.5 m. Attribute these at the inflow level; the nonlinear thrust law prevents adding isolated load changes as independent causes.

Before looking at results, declare descriptive effect-size bins, not acceptance tolerances:
- max rotor inflow change: <=0.01vi, (0.01,0.05]vi, >0.05vi;
- total-thrust change magnitude: <=0.001mg, (0.001,0.01]mg, >0.01mg;
- max absolute roll/pitch angular-acceleration change: <=0.01, (0.01,0.1], >0.1 rad/s^2.

These bins have no empirical safety status. The 0.01mg marker corresponds to 0.01g instantaneous translational-acceleration change. Report exact extrema and effect sizes so the interpretation does not depend on bins. Do not call any arm physically accepted or rejected based on these unvalidated markers. The numerical/data/domain checks below have pass/fail outcomes; the scientific output is a quantified approximation sensitivity.

A large X-P establishes sensitivity to the arbitrary axial support on this trajectory. A large R-P or U-P does not establish that radial taper is physically wrong. A small change supports only bounded paired-load sensitivity on these exact states. No result establishes flight stability, collision safety, energy accuracy, physical validation, generalization to other seeds, or publication novelty.

No confidence interval treats the 401 temporally correlated rows or the 16 interacting drones as independent replications. This is one deterministic trajectory, not 6416 independent experiments. Deliver effect sizes without a physical-validity pass claim.

## Numerical checks and stopping conditions

Preflight: pin Node version; verify the four source hashes against public-source-identities.json; verify raw byte count/hash and sidecar metadata; record hashes of the new runner and frozen plan. These are compact identity checks, not an audit campaign. Do not import branch-audit.cjs or run R3/R8 harnesses.

Baseline check: on every row require max|P_inflow-original_inflow| <= 1e-12 + 1e-12*max(|P|,|original|) m/s, and equivalent tight comparisons for load computations in their own units. Record the worst residual. Fail closed on larger discrepancy.

Require finite nonnegative inflows, finite loads, monotone inflow ordering within the same tolerance, and nonincreasing total effective thrust as inflow increases. For every rotor verify U-X-R+P equals the directly accumulated sum of u*(1-fz)*(1-fr), including the fixed receiver/source cosine, within floating tolerance, and is nonnegative within tolerance. This factorial interaction is an inflow identity, not an additive load identity. Do not impose monotonic roll/pitch moments; signed differential rotor loads can change them either way. Confirm all 401 rows and all 6416 receivers are accounted for. No interpolation, replacing a failed state, discarding a witness, or silently shrinking the sample.

Run once, one ordinary Node process, one forward pass. The fixed work is 401*16*4*15 = 384960 ordered rotor/source evaluations for the research-arm formula; computing four weights in that pass avoids four full independent traversals. Original baseline adds at most the same number of ordered rotor/source visits. There are just 25 scalar probes and identity/summary work. This is a bounded <0.8 million pair-visit calculation, not a timing/speedup benchmark.

Use a 60 s wall limit as a conservative preliminary protection, not a predicted runtime. Keep memory small by retaining only fixed-size input/output arrays and aggregate statistics; a 256 MiB RSS guard is ample in principle but must be enforced or honestly reported as an observation, not invented. If timeout, resource cap, domain error, numerical check, identity mismatch, or output limit triggers, stop and preserve a compact exact failure witness and partial-coverage status. Do not relaunch with looser tolerances, changed limits or altered conditions without review. This is a new study's stop policy, independent of terminal historical R8.

## Evidence and storage budget

Existing source/input evidence is read in place; the experiment creates no duplicated input trajectory.

New experiment outputs: hard cap 2000000 bytes, adopted before execution. Retain the complete four-arm rotor inflows as one little-endian Float64 array [401,4,16,4], exactly 821248 bytes; order is time, arm [P,X,R,U], receiver, rotor. Include explicit dimensions, arm order, units, row/time mapping and SHA-256. These complete tensors support rotor-level factorial interaction and deterministic load reconstruction from unchanged states and original receiver law.

Additional outputs may include a compact per-receiver load/difference array, partition totals, metadata, 25-point probe table, bounded worst witnesses, result report and resource record. Retain derived results only within the combined 2000000-byte output cap; do not copy raw trajectories or serialize every pair. Pre-budget files and count actual bytes including all sidecars.

New source/design cap is separately <=100000 bytes under the pre-execution plan; this assessment report stays under 20000 bytes. An optional human-facing demo has a separate <=1000000-byte cap; it is unnecessary to obtain the first result and must be labeled fixed-state sensitivity, not a new flight. Account outputs/source/design/demo together against the global cap.

## Relationship to existing research

The already retained prior wake-pruning evidence report was statically inspected after the initial assessment. Its embedded accuracy-summary and REPORT were decoded as JSON/text only; the HTML/JavaScript was not executed or copied. The earlier study has 4848 prescribed snapshots and 1330776 receiver comparisons; it bounds weak-wake omissions INSIDE the already finite-support reference. Its pruning candidate met numerical budgets but failed its preregistered speed-benefit gate. That result remains unchanged.

Crucially, the prior report also includes selected support-assumption fixtures: a source 3 m above a receiver changed predicted thrust by 7.5562% of weight when axial support expanded from 2-2.5 m to 4-5 m; a deliberately selected 16-source ring changed it by 20.0016% with axial/radial expansion. These are previously reported, unvalidated model sensitivities, not new results or evidence that larger support is physically better.

This proposed study therefore does not claim the first discovery that support matters. Its incremental contribution is a complete four-arm factorial attribution of support effects, core/tail decomposition, and physical-load consequences on all endpoints of one existing genuine local3D trajectory. It tests the baseline support assumption itself, without additional weak-wake pruning or a speedup claim. This is useful evidence development, not independently established publication novelty.

## Public source identity and reproduction scope

The source snapshot is commit 1336f5c416875a9651f92b58b2ed06649f25b04e. Kernel sources and historical input are public predecessors; this study is separate from historical R8. Original code anchors: aero.cjs lines 4-19; wake.cjs lines 1-25; physics.cjs lines 3-19; grid.cjs lines 3-6. The saved run JSON states the endpoint schedule and local 3D Boids provenance. Public metadata links each source to its pinned repository URL and preserves hashes.

The exact executed runner is archived without changing its bytes. It expects the original workspace layout, identity manifest and adoption record; those workflow files are outside this narrow public checkpoint. This source disclosure is not a ready-to-run standalone package. The complete 401-row output tensors remain private; hashes, schemas, summaries and 25 selected demo frames are public. A portable reproduction adapter would be a separate artifact, not the already executed source.
