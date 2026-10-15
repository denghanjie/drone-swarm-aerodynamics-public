# Prospective full-flock static equation qualification

Question: can independently implemented arithmetic reproduce unchanged M28 `sum-rotor` inflows and receiver loads for every vehicle in the twelve already domain-screened primary M31 pose snapshots? This is a reference-only checkpoint. No spatial or temporal approximation, timing comparison, integration, controller, new trajectory or physical validation is included.

## Frozen input and scope

Use the exact metadata and compact Float64LE binary from07e5165, independently pinned by SHA256 and byte length in config.json. Primary variant0, case-major wide1000/seed2001, narrow1000/seed2002, wide5000/seed2001, exact saved times0/20/30/60s.12snapshots,28,000vehicles,112,000receiving rotors. Primary value offsets respectively[0,14000,28000,42000], [70000,84000,98000,112000], [140000,210000,280000,350000]. No interpolation, filtering, pose correction or active/arrived-mask reconstruction. All original quaternion values retained, finite and norm defect<=1e-10 required.

Pin completed domain result and its manifest at770c2e77867b039e20ff5082e9299298aebc5642. Verify all required input and prior per-receiver records against those pins before using them. Every snapshot must retain a domain pass. These are exposed historical development poses from airflow-off local3D Boids with shared map guidance; their original trajectory-refinement failures remain unresolved.

Prescribe all nominal receiver motor thrust inputs as f0=m*g/4=0.0662175N. Source amplitude remains the M28 constant isolated-hover value. These are new static inputs, not recovered historical motors or tilted-hover equilibrium. The17-state API includes exact positions/quaternions, zero velocity/body-rate placeholders unused by these static functions, and four f0 values. No motor response, source-thrust feedback or thrust compensation for tilt is added.

## Matched independent calculation

Production calls unchanged A.fields(states,'sum-rotor') once per snapshot, A.effectiveThrust once per receiving rotor, and F.wrench/F.rotate for load assembly. It never calls a derivative/integrator. Independent code imports none of the production/grid/wake/domain modules: explicit rotation matrix, every nonself source enumerated directly, independent profile/fade arithmetic, bracketed bisection and signed rotor wrench. Source IDs ascend in both sums.

In the same independent field pass, preserve indexed geometry code hashes/counts for each receiver and require exact equality to the pinned domain rows. Compare axes/world rotor positions to original rotation with absolute1e-12 tolerance; exact tilt predicates and unit-input constraints must agree. Production candidate/contribution counts must equal independent and prior domain counts. Domain code6+7 is the contribution count; code7 alone is not substituted if code6 becomes nonzero. No field geometry is silently omitted based on past zero-load assumptions.

Alongside the ordinary independent sum, accumulate Neumaier's compensated sum of the same nonnegative terms without re-evaluating the field. This is a summation diagnostic, not an alternative reference chosen after exposure. Both ordinary/compensated and production/ordinary inflow comparisons must pass. The compensation method is a standard numerical technique; see [verified Neumaier1974 provenance](compensated-summation-source.md), p40/Eq(IV,1), and [BibTeX](sources.bib). No algorithmic novelty is claimed.

For each rotor retain both inflows/effective thrusts, compensated inflow, normalized roots, alpha, residual, independent bracket/iteration count, and ideal induced power. For each vehicle retain total body thrust, body roll/pitch moments, nominal yaw(0), world thrust force, change from nominal world force, and world-rotated body moment. The moment obtained from F.wrench(effective) is used only for roll/pitch; modeled yaw is the nominal yaw, exactly0 here. Each implementation rotates its thrust vector using its own rotation function; world-force change subtracts its corresponding nominal rotated force. Forces exclude gravity, drag, contact and gyro terms. Body thrust is not world-vertical support at nonzero tilt.

## Precision gates fixed before exposure

All quantities finite; U>=0,0<=f<=f0. Exact U=0 response must equal f0. A receiver rotor with no retained contribution must have exact0 inflow. Comparisons must pass for every rotor/vehicle, with no average-based rescue:

| Observable | Absolute / relative screen |
|---|---|
| Axes/world rotor geometry | absolute1e-12 native units; exact domain code/tilt agreement |
| Inflow, including ordinary vs compensated | 1e-11m/s +1e-12*max(abs(a),abs(b)) |
| Effective rotor thrust | absolute1e-12N |
| Total body thrust | absolute5e-12N |
| Body roll/pitch moment | absolute2e-13Nm |
| World force and force-change components | absolute1e-11N |
| World moment components | absolute1e-12Nm |
| Cubic residual at each solver's own U | absolute1e-12 dimensionless |
| Independent bracket | finite ordered endpoints in[0,1], width<=2e-15; <=96iterations; x within bracket |
| Ideal-power identity for both solvers | 1e-14W +1e-12*abs(P(f0,0)) |

The receiver equation is x^3+alpha*x−1=0 with alpha=U/sqrt(f0/(2rhoA)). For alpha>=0 the root in(0,1] is unique; at zero inflow x=1. This is a constant ideal induced-power assumption, not a measured PWM/RPM/electrical-power response. Root residuals/brackets are binary64 diagnostics, not formally rounded interval certificates. The precision gates separate numerical consistency from the much larger unresolved physical-model uncertainty. No post-exposure tolerance adjustment or solver replacement.

Record per-snapshot max/RMS absolute discrepancies and maximizing indices, including all zeros. Record empirical nearest-rank q50/q95/max thrust-loss and absolute roll/pitch moment distributions over all saved vehicles. Fractions of nominal weight are descriptive, not measured losses in the historical flights. No confidence interval or success probability is inferred from dependent selected snapshots. All12complete snapshots and all gates are required for a completed qualification.

## One-shot budget and evidence

One invocation;300executable wall seconds;24full-snapshot field calls(12production+12independent),224,000receiver calls(112,000each),110,000,000independent nonself center checks,864,000,000combined eligible rotor visits,64MiBraw with2MiBreserved failure storage. Independent max96root iterations; unchanged production max12Newton iterations by source. Exact successful counts:107,972,000direct checks;9,378,560eligible ordered pairs per implementation;75,028,480combined eligible rotor visits;491,535support evaluations per implementation. Count attempted field/receiver calls before invocation. Independent counters report per receiver; production calls are bounded externally and accounted from returned counts, not live per-instruction instrumentation. Contributor-presence inspection of saved-classification byte arrays is separately counted and capped at432,000,000bytes visited; this is not another geometry or field calculation. No memory acceptance cap; record process RSS with platform semantics. No timing warmups/repeats or speed conclusion.

Scientific binary storage is fixed by schema.json:112,000×16×8rotor bytes +28,000×35×8vehicle bytes =22,176,000bytes. Store one bounded metadata row per vehicle with domain hashes/counts, plus fixed summaries and start/failure records. Before writing, enforce actual accumulated raw bytes below cap minus reserve; stop without dropping data if insufficient. No every-source contribution matrix. Complete previous domain vectors remain in the pinned prior checkpoint, not duplicated in this raw budget.

Write each completed receiver's full rotor row, vehicle row and metadata. Retain first mismatch with current snapshot/receiver/rotor/input pose, nominal inputs, both field values, completed rotor-evidence prefix, failing-stage root/load values as available, counters and previous complete receiver; retain partial streams. On failure during a full production call, only current snapshot/context and prior completed evidence may be available. No post-failure field rerun to make a richer witness. External supervisor terminates/reaps the process group; cooperative guards run before calls and within independent receiver progress. Raw/start and exclusive lock prevent duplicate launch. A failure/cap/mismatch closes the campaign with no patch/retry/enlargement. Zero integration steps. Stop new launches at07:00Asia/Shanghai2026-10-16.

Freeze source/config/schema/input pins, verified citation note and independent static review; privacy-review, push and independently verify before executing. Scientific files and raw results remain immutable afterward. A separate saved-data-only reviewer may use at most60seconds once to check hashes/coverage, comparisons, wrench arithmetic, residual/power identities from saved scalars and distributions; no geometry, field or new root solving. Preserve every original review output/failure before any correction; a correction needs separate recorded justification. Close the budget, preserve a claim/literature ledger, plain-language summary and actual-pose Three.js view, privacy-review/push/verify the checkpoint.

## Interpretation and next decision

Passing qualifies only a finite static arithmetic comparison for these prescribed inputs within unchanged exploratory equations. It does not qualify the long-flight trajectory, time interpolation, stale-field updates, physical force response, ground/obstacle effects, multiwake superposition, rotor-disk approximation or browser execution. Existing M28 already compared its cubic with bisection; current independent pair/path work already checks small-case fields. This checkpoint adds complete retained-flock coverage, not a new method. Later main's incomplete reference gates remain unchanged.

Only after this reference checkpoint is closed may a separately frozen center/rotor sampling compromise be proposed. Center sampling may erase roll/pitch response and has its own domain test; it is not automatically accepted or evaluated here. Existing verified aerodynamic sources and physical-target limitations remain linked through DESIGN-REVIEW.md and the literature ledger.
