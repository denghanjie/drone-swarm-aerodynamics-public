# Proposed M31 full-flock static force-reference checkpoint

Date: 2026-10-15. Status: **design only; no geometry, field, receiver-root, benchmark, or integration evaluation performed for this proposal.** No repository edits. Read M28 source/checks/report, the recent prescribed-path protocols and independent arithmetic module, the completed saved-flock domain records, and all five later-main notes in `/tmp/m31-main-read`.

## Recommendation and fresh question

Proceed, if selected by the coordinator, with one **reference-only** checkpoint: at the twelve exact retained primary M31 poses, with every receiver assigned the same prescribed isolated-hover nominal rotor thrust, can the unchanged M28 `sum-rotor` field and receiver-load mapping be independently reproduced for every vehicle?

This adds full-flock coverage of the *declared instantaneous equations*: twelve snapshots, 28,000 vehicles and 112,000 receiving rotors. It does not establish a coupled trajectory reference. The data are already exposed development poses, not fresh flight holdouts. The domain campaign's 12/12 pass is a necessary implemented-input screen, not validation of the wake or motor model.

The new scope must be described against existing work:

- M28 already checked the cubic receiver response against bisection, the ideal-power identity, pair symmetry, overlap examples, and force/moment accounting. A new bisection comparison is not a new method.
- The recent 2–4-vehicle pilots already compared direct-pair field calculations; the predictor challenge independently checked all vehicles' inflows but only receiver 0's loads. Here every saved large-flock receiver receives a load check.
- Later main's temporal-airflow study used two 16-vehicle, one-second paths and failed both airflow-reference gates. Its fixed-path diagnostics remain conditional. The subsequent joint-stage cycle is incomplete, and AUDIT-C1-R8 stopped before its independent correctness gate. None is repaired or superseded by this static calculation.
- No novelty, physical validation, cadence acceptance, continuous-time bound, mission success, or browser/5,000-vehicle runtime claim follows. “5,000-vehicle static equation reproduction” is the permitted scale statement if it completes.

## Frozen inputs and prescribed actuation

Use the exact same metadata/binary pair from input commit `07e5165fa56f2f23bab24562b278dda1c82ed05e` and primary offsets as the domain audit. Freeze hashes before execution: metadata `f69cae28818dd0802863b512af96a448ffcd3aa7aa8824f528b4ed59032d613c`; 3,360,000-byte binary `c9918697fc61576a9c0454cda354a8d66f42b0b6e21e082cdbf12054b372c927`. Cases are wide1000/seed2001, narrow1000/seed2002, wide5000/seed2001; exact times 0,20,30,60 s. Their primary Float64 value offsets are respectively `[0,14000,28000,42000]`, `[70000,84000,98000,112000]`, and `[140000,210000,280000,350000]`. Multiply by eight; never interpolate.

Pin the completed domain source commit `e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3` and its evidence manifest. The currently read `results/result.json` hashes to `7e8cf6d53fe4a94c7c6faaf1bc1af36dfd1f30da6b519680c3a82d84ab2f5584`; verify this again when freezing the new protocol. Use all saved vehicles as sources/receivers. Do not infer an active/arrived subset.

Set all four nominal motor-state thrust inputs to **f0 = m*g/4 = 0.0662175 N** with m=0.027 kg and g=9.81 m/s². These are new prescribed inputs, not reconstructed historical motors. If the 17-state API is used, insert exact retained position/quaternion, zero velocity and body-rate placeholders, and four f0 values. Record that the placeholders are unused by the static field/receiver functions; do not treat them as recovered flight states. No motor ODE, controller, derivative, or integrator is called.

Call this “isolated-hover nominal thrust,” not a tilted-hover equilibrium: the retained attitude can be tilted, so total prescribed body thrust mg would provide vertical support mg*axisZ. Do not compensate thrust by 1/axisZ. M28 source strength remains its existing isolated-hover constant regardless of source nominal/effective thrust or tilt. Quaternions remain unchanged; finite-input, norm-defect (1e-10), and exact axisZ<cos(20°) gates remain prerequisites. A new input/domain discrepancy is an implementation/integrity failure, not an invitation to filter vehicles.

## Production and independent paths

Production: call the unchanged `A.fields(states,'sum-rotor')` once per snapshot; call unchanged `A.effectiveThrust(f0,U)` once per receiving rotor; use `F.wrench` and `F.rotate` for load assembly. Do not call `A.derivative` merely to obtain a wrench.

Independent: explicit quaternion matrix, direct nonself all-source loop, independent finite-support/fade/wake arithmetic, bracketed bisection for receiver roots, and explicit signed rotor wrench. It must import no production physics, wake, aero, Grid, or domain-classifier helper. The existing independent predictor module is a useful reviewed starting point, not an unseen oracle; any added counters/streaming diagnostics require a new source freeze and static review. Its current hash is `e0445be31ec647c8ddfb79533d4866dc8133e99ba5f25061bf393aab6bc58baf`.

Keep source IDs ascending for each receiver/rotor sum. Independently test strict source-center distance <3 m, every branch and unchanged source-axis/receiver-axis projection. Record independent per-receiver domain code hashes/counts and require exact agreement with the pinned domain rows; no additional geometry pass is needed. Compare production `candidates` with the saved eligible ordered-pair count and `contributions` with saved code6+code7 totals. Production counts include retained-support contributions even when projection is zero. Compare global maxima with the retained per-rotor arrays. No source-pair field evaluations may be substituted by old zero-load assumptions.

One vehicle contributes one modeled mean wake sampled at four *receiving* rotor points; `sum-rotor` does not mean four individual source-rotor wake models. Each per-source term is nonnegative. Add a Neumaier compensated total alongside the ordinary independent sum in the same loop, without reevaluating terms. This is a justified large-fan-in arithmetic diagnostic; save both totals and require the ordinary/compensated discrepancy to satisfy the same inflow gate. Use the ordinary independent sum for the declared comparison, and do not pick whichever sum happens to agree better.

Primary loads are each effective rotor thrust, total body thrust T, body roll/pitch moment, and thrust force in world coordinates. With rotor order (++),(-+),(--),(+-), a=0.028 m:

`T = f[0]+f[1]+f[2]+f[3]`

`tauX = a*(f[0]+f[1]-f[2]-f[3])`

`tauY = a*(-f[0]+f[1]+f[2]-f[3])`

For M28 `sum-rotor`, yaw is the **nominal** yaw moment, exactly zero here because nominal motors are equal; do not report the yaw component of `F.wrench(effective)` as modeled aerodynamic yaw. `forceWorld = T*axis`; `deltaForceWorld = (T-mg)*axis`. Body interaction moments are tauX/tauY with zero yaw. Exclude gravity, gyroscopic terms, contact, and translational drag. Save total and incremental values with units, and optionally rotate the declared body moment for display/verification.

## Receiver equation, uniqueness, and numerical gates

Let A=pi*(0.023 m)^2, rho=1.225 kg/m³, vi0=sqrt(f0/(2*rho*A)), alpha=U/vi0. The unchanged response is f=f0*x with

`g(x)=x^3+alpha*x-1=0`, `0<x<=1`.

For U=0, x=1 exactly. For alpha>0, g is strictly increasing, g(0)=-1 and g(1)=alpha; the unique root lies in `[1/(1+alpha), min(1,1/alpha)]`. This is the constant-*ideal-induced-power* equation, not an electrical-power, constant-PWM, or fixed-RPM model. Differentiation gives `dx/dalpha=-x/(3*x^2+alpha)<0`. On the positive-root branch, `|dx/dalpha|=x^2/(1+2*x^3)<=1/3`; hence `|df/dU|<=f0/(3*vi0)`. These are analytical checks of the stated equation, not new empirical findings or formal floating-point certificates.

Use at most 96 independent bisection iterations, retain alpha, endpoints, width, iteration count and residual, and handle exact zero inflow separately. The inherited solver collapses its bracket when the floating polynomial evaluates to zero; a zero rounded residual is not proof of an exact root. Report brackets as numerical brackets unless separately verified with directed/high-precision arithmetic. Do not claim a certified enclosure or add high-precision reevaluation after viewing a failure.

Freeze these proposed binary64 implementation gates before any field call:

| Quantity | Gate on every applicable scalar |
| --- | --- |
| Independent/production rotated geometry and axes | absolute difference <=1e-12 in native SI/dimensionless units; exact domain/code decisions |
| Rotor inflow and ordinary-vs-compensated independent sum | `abs(delta)<=1e-11 m/s + 1e-12*max(abs(U1),abs(U2))` |
| Effective rotor thrust | absolute difference <=1e-12 N |
| Total body thrust | absolute difference <=5e-12 N |
| Body roll/pitch moment | absolute difference <=2e-13 N·m |
| World force components | absolute difference <=1e-11 N |
| Optional world moment components | absolute difference <=1e-12 N·m |
| Root polynomial, evaluated separately at each solver's own U | absolute dimensionless residual <=1e-12 |
| Independent root bracket | ordered finite endpoints in [0,1], width <=2e-15; at most96 iterations |
| Ideal-power identity, separately for both solvers | `abs(P(f,U)-P(f0,0))<=1e-14 W + 1e-12*abs(P(f0,0))` |

All values must be finite; U>=0 and 0<=f<=f0. No-contributor inflow and U=0 receiver response must be exact zeros/f0. The absolute thrust/moment gates account for four-rotor aggregation and the 0.028 m lever; they are precision screens, not physical tolerances. Retain every discrepancy and maximum location. There is no averaging away a failed receiver, post-outcome tolerance expansion, alternate summation rescue, or partial-snapshot pass. Reference acceptance requires all twelve complete snapshots, every prescribed comparison, and the exact counts below.

## Complete coverage and bounded work

Exact arithmetic counts follow from the fixed design and already saved domain counts; they have not been obtained by a new geometry run:

- Direct independent nonself center checks: `4*(1000*999 + 1000*999 + 5000*4999) = 107,972,000`.
- Saved combined eligible rotor classifications were 75,028,480, so there are 9,378,560 eligible ordered center pairs and 37,514,240 eligible rotor visits in each field implementation. Reproduce these as integrity counts; do not infer a runtime ratio from them.
- Hard shape-derived worst case: 431,888,000 rotor visits per implementation, 863,776,000 combined. Wake-profile evaluations occur only after geometry support checks and cannot exceed these counts. The production Grid's candidate-cell work is additional, not equal to direct-loop distance checks.
- Exactly 12 production plus 12 independent full-snapshot field calls, 112,000 production receiver calls and 112,000 independent receiver calls. A zero-inflow shortcut still counts as a receiver call. At most1,344,000 production Newton iterations and10,752,000 independent bisection iterations by source structure. No timing warmups/repeats, perturbed poses, new snapshots, or integrations.

Suggested one-shot limits: **300 executable seconds**, 24 total full-snapshot field calls, 110,000,000 direct independent center checks, 864,000,000 combined eligible rotor visits, 224,000 receiver calls, 96 iterations per independent root, **64 MiB new raw evidence including a 2 MiB failure reserve**. All attempted calls count. The exact planned counts must match on completion. The external supervisor terminates/reaps the process group; cooperative guards run before calls and within the independent receiver loop. The unchanged production call is not internally instrumented: account its returned counts and use the fixed input-size upper bound plus the external watchdog while it runs. Do not claim a live per-instruction operation limit.

Use an exclusive one-invocation lock, write-once started/terminal records and no retry after a cap, exception, mismatch, or incomplete output. No new launch after07:00Asia/Shanghai2026-10-16. Record wall/CPU and platform-labeled process RSS only as execution diagnostics. No RSS acceptance threshold is proposed, and these timings are not a speed benchmark. The prior domain audit's12.110 s completion is not a prediction for this different workload.

## Evidence and independent saved-data review

Save all112,000 rotor tuples for both paths, compensated inflow, root diagnostics, and all28,000 vehicle force/moment tuples; do not retain only aggregate maxima. Prefer chunked Float64 binary with an explicit column schema, snapshot/receiver indices, exact byte lengths and SHA-256 hashes, plus compact JSON metadata and per-receiver gate records. A binary plan comfortably avoids millions of repeated JSON keys: eight rotor doubles alone would occupy7,168,000 bytes, before separate vehicle diagnostics and metadata. Preflight the schema's full worst-case bytes; do not rely on compression to meet the cap.

Pin/reference the earlier40 MiB domain evidence rather than copying it into the new raw budget. Do not save every source contribution: that is unnecessary for an all-receiver reproduction claim and can exceed storage bounds. Instead retain counts/code hashes and all resultant rotor values. On first mismatch save the snapshot/receiver/rotor, input pose and prescribed motor inputs, both full receiver rows, root/bracket/residual details, domain hashes, counters and last completed receiver. No post-failure field recomputation to construct a richer witness. A failure during a full production call may retain only its current snapshot and prior completed evidence; state that limit explicitly.

Independent postrun review can recompute comparisons, wrench sums, distributions and coverage from saved arrays without new geometry, wake, or root solving. If polynomial/power-identity checks are to be independently reevaluated from saved scalars, authorize that bounded algebraic audit explicitly in the frozen protocol; it is not another field evaluation. Report per-snapshot max/RMS discrepancies, exact failed counts, total thrust-loss distribution, body roll/pitch distributions and worst IDs. Every one of the28,000 vehicles must be included; zeros remain in denominators. Distribution summaries describe these snapshots, not independent population samples. Freeze/push all scientific dependencies and review before the single launch; retain failures and independently verify the publication manifest afterward.

## Center-sample approximation: defer, with a precise future contract

Do not fold a center approximation into this first full-flock reference checkpoint. It adds a different estimand and domain risk. If later selected prospectively, define it as one mean-wake sample at the receiving *body center*, with identical source cutoff, sources, amplitudes, axes, projection, fades and near-field policy; broadcast that one U to four identical receiver laws. It then predicts exactly zero roll/pitch interaction moment for equal nominal motors. That structural limitation must be disclosed before testing. Evaluating the field at the center is not averaging the four rotor inflows, and nonlinear receiver response must not be silently commuted with averaging.

Rotor-point domain admission does not prove body-center admission. A center near-wake exception makes that approximation unavailable for the affected configuration; it must not be converted to zero inflow or repaired by changing support. A fair later comparison evaluates all vehicles, compares total/world force and roll/pitch moment against the already qualified rotor reference, retains absolute errors near zero, and declares numerical targets before execution. No cost/speed claim follows merely from one spatial query replacing four. If both center implementations share the existing direct source scan, the additional eligible point visits are9,378,560 per implementation; a separately repeated all-source center scan would add107,972,000 center checks per independent pass and needs its own budget. No approximation or ablation is needed to answer the present reference question.

## Physical assumptions and source pins

The paper motivates a mean, near-hover, far-wake profile; the verified ledger reports measured source vehicles beginning at230 g, while unchanged M28 is27 g. M28 uses rotor radius23 mm, rotor coordinates(±28,±28) mm, radial arm sqrt(2)*28 mm, and opposite-motor spacing2*sqrt(2)*28 mm. The RSS2025 target's32.5 mm radial arm, fixed4 V hover-PWM actuation and unverified calibration/export metadata remain incompatible/unresolved; no measurement fit is authorized.

Tilted source wakes are rotated while their strength stays fixed at isolated-hover weight. Multiple projected nonnegative scalar wakes add linearly without source-thrust feedback, wake deformation, entrainment coupling or conservation closure. The receiver response assumes constant ideal induced power; nominal yaw is preserved. Rotor-point sampling omits disk integration. Finite3 m center search,2–2.5 m downstream fade,2–3 half-width radial fade,20° tilt gate and near-wake skip/exception policy are implementation choices. There are no walls, doorway/ground effects, free-stream/relative-velocity response, transport delay, wake history or turbulence. Retained poses came from a course with obstacles, but the static aerodynamic field is still free-air. Agreement of the two equation implementations validates none of these assumptions.

Unchanged production source SHA-256 pins read during planning:

| File | SHA-256 |
| --- | --- |
| `outputs/milestone-28-source/aero.cjs` | `710b0a8f0df62208e3385ac9b8288240b379fe9248a1a645251a77c533f24a62` |
| `outputs/step03a-source/wake.cjs` | `fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc` |
| `outputs/step02c-source/physics.cjs` | `0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1` |
| `outputs/milestone-26-source/grid.cjs` | `f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302` |

The proposed design is ready for coordinator selection, source implementation and independent static scrutiny. It does not authorize an automatic extension of the closed domain, temporal, predictor, or later-main campaigns.
