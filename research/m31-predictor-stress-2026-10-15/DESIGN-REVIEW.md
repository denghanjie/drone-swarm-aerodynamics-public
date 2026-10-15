# Prospective independent review: fresh causal-inflow predictor challenge

Prepared before implementation freeze and before any candidate-field evaluation. This memo contains static mathematical design and source-based reasoning only. No solver, field evaluator, candidate trajectory, timing experiment, or numerical outcome was run to prepare it. No repository file was changed.

## Assessment and fixed scope

The previous single-path predictor result warrants a deliberately different six-case challenge. It does not establish a general advantage, a physical unsteady-wake model, an operational refresh cadence, or novelty. The construction remains a familiar linear extrapolation of cached inflow. The suite below is development evidence chosen after earlier results, not a statistically independent flight population or an untouched generalization benchmark.

Use the unchanged corrected M28 `sum-rotor` field and the independent all-pairs/bisection oracle. Source strength remains prescribed isolated-hover strength, independent of source motor states and of the loads induced on a source by another vehicle. Vehicle-centered source wakes, four receiver-rotor samples, finite support/fades, receiver projection, receiver thrust hypothesis, and nominal-yaw retention remain the existing assumptions.

Every case lasts exactly one second: t in [0,1], with t in seconds. Vehicle 0 is the primary receiver R. Sources follow in the listed order S1, S2, S3. All nominal rotor motor-state thrusts, including those on moving or tilted sources, are mg/4. Positions and orientations are prescribed kinematics; they are not dynamically realizable actuation commands or integrated flight. Populate translational velocities with the analytic derivatives below. Set angular velocity to zero for identity orientations; otherwise use the stated derivative. No integration is required.

Let P2=2*pi*t and P4=4*pi*t. Unless explicitly overridden, orientation is identity quaternion xyzw=[0,0,0,1]. The source/receiver labels identify the intended encounter; the production API still treats every vehicle as a potential source and receiver and must check every ordered pair.

## Six explicit cases

### 1. `support-transit`: enter and leave finite radial support

- R(t)=[-0.36+0.72*t, 0.035, 1.0]; vR=[0.72,0,0].
- S1=[0,0,1.8], fixed.
- Both orientations identity.

Purpose: traverse both wake edges and the core, with distinct rotor entry times. This does not rely on changing source thrust. At both endpoints the smallest absolute rotor x offset from the source is 0.332 m. For d=0.8 m, the radial support radius 3H(d) is less than 0.294 m, so every receiver rotor is outside support. At t=0.5 the largest rotor radial distance is less than 0.07 m, while 3H(0.8)>0.184 m, so every rotor is inside support. These inequalities establish a support crossing without evaluating a field value. The fades make entry/exit continuous; continuity does not guarantee predictor accuracy.

### 2. `cold-start-inflow`: no history despite nonzero initial inflow change

- R(t)=[0.14-0.50*t, 0.035, 1.0]; vR=[-0.50,0,0].
- S1=[0,0,1.8], fixed.
- Both orientations identity.

Purpose: test initialization when the receiver starts inside the wake with nonzero radial motion. At t=0, the largest rotor radial distance is less than 0.180 m, below the conservative lower bound 0.184 m for 3H(0.8); all four rotors start inside support. Their x coordinates relative to the source are nonzero and are moving, so this is not a stationary or zero-field warm start. At t=1 all rotors are outside support by the preceding endpoint argument.

The predictor must reset its history at this case's t=0. It holds the first measured inflow until the second actual sample at 5 ms. Predeclare the first 0–5 ms and 5–10 ms intervals as startup reporting windows; do not initialize with a negative-time sample or reuse another case's history.

### 3. `smooth-fast-reversal`: high curvature within radial support

- R(t)=[0.12+0.09*cos(P4), 0.04, 1.0].
- vR=[-0.36*pi*sin(P4),0,0].
- S1=[0,0,1.8], fixed; orientations identity.

Purpose: challenge a secant predictor around rapid smooth reversals rather than a discontinuous velocity command. The maximum speed is 0.36*pi m/s and maximum acceleration is 1.44*pi^2 m/s^2, by direct differentiation. Interior reversals occur at t=0.25, 0.50 and 0.75 s. The receiver x range is [0.03,0.21] m. Every rotor remains within radial support: its radial distance is at most sqrt(0.238^2+0.068^2)<0.248 m, whereas 3H(0.8)>0.28 m using D>0.079 m. Thus this case does not depend on a hard support entry to generate the reversal challenge.

Predeclare +/-10 ms windows around each interior reversal for reporting signed error and predictor overshoot. Keep whole-case metrics as well; do not select only the largest observed reversal afterward. The acceleration is an intentionally demanding kinematic input, not an assertion about achievable vehicle motion.

### 4. `fixed-position-source-pitch`: source direction changes without translation

- R=[0.12,0.035,1.0], fixed, identity orientation.
- S1=[0,0,1.8], fixed position.
- Source pitch theta(t)=(pi/12)*sin(P4), so |theta|<=15 degrees.
- Source quaternion qS=[0,sin(theta/2),0,cos(theta/2)].
- Source body angular velocity omegaS=[0,(pi^2/3)*cos(P4),0].
- Both translational velocities are zero.

Purpose: force the unchanged instantaneous model to vary through source-axis geometry while both centers remain stationary. This probes a failure mode that displacement-only reasoning misses. It does not model wake transport, memory, propagation lag, or physically measured tilted unsteady wakes. The globally fixed source strength is retained despite tilt. The analytic extrema occur at t=0.125,0.375,0.625,0.875 s; sign changes at multiples of 0.25 s. These are reporting markers, not extra field-refresh events or predictor inputs.

### 5. `two-source-receiver-roll`: overlapping sources and moving receiver rotor geometry

- R(t)=[0.10*sin(P2),0.035,1.0]; vR=[0.20*pi*cos(P2),0,0].
- Receiver roll beta(t)=(pi/18)*sin(P4), so |beta|<=10 degrees.
- Receiver quaternion qR=[sin(beta/2),0,0,cos(beta/2)].
- Receiver body angular velocity omegaR=[(2*pi^2/9)*cos(P4),0,0].
- S1=[-0.22,0,1.8], S2=[0.22,0,1.8], both fixed and upright.

Purpose: challenge simultaneous changes in rotor sample positions, receiver-axis projection and the balance of two overlapping mean wakes. At t=0 the receiver is upright and centrally positioned. Its largest radial distance from either source is less than sqrt(0.248^2+0.063^2)<0.256 m, below 3H(0.8)>0.28 m; both sources contribute at all four rotor positions. Subsequent motion changes that overlap. No empirical aggregation validity follows from comparing two implementations of the same sum.

Report thrust and roll/pitch moments in the receiver's current body frame. If world-frame force is additionally reported, transform reference and treatment using the same current orientation; do not mix frames or predict the orientation. Constant nominal mg/4 motor states during roll are an isolation assumption, not a hover controller.

### 6. `stacked-moving-sources`: three wakes with active source-to-source exposure

- R(t)=[0.10*sin(P2),0.045*cos(P2),1.0].
- vR=[0.20*pi*cos(P2),-0.09*pi*sin(P2),0].
- S1=[-0.06,0,1.7], fixed.
- S2(t)=[0.06+0.08*sin(P2),0.02,2.1]; vS2=[0.16*pi*cos(P2),0,0].
- S3(t)=[0.04*cos(P2),-0.04,2.5]; vS3=[-0.08*pi*sin(P2),0,0].
- All four orientations identity; all angular velocities zero.

Purpose: test predictor behavior under the nonlinear receiving-thrust response to a sum of three changing source contributions. Upper sources also expose lower sources to changing fields. This interaction must not be deleted from the field API or the independent verification to make the test easier. Their nominal source amplitudes nevertheless remain unchanged by those received loads, exactly as in M28. This limitation must accompany interpretation. This case does not establish a high-density or large-swarm result.

## Domain proof for every vehicle pair

The same sufficient geometric argument covers all six cases, all time, both pair directions, and the tilted rotor poses.

1. Each rotor center lies at Euclidean distance a_rot=sqrt(2)*0.028<0.04 m from its vehicle center, regardless of rotation.
2. M28's near-wake exception requires simultaneously 0<d<2.5D and r<0.15 m, with D=2*sqrt(2)*0.028<0.08 m. Since source axes are unit vectors, source-center-to-receiver-rotor distance then equals sqrt(d^2+r^2)<sqrt(0.20^2+0.15^2)=0.25 m.
3. Consequently an exceptional pair would require vehicle-center separation below 0.25+0.04=0.29 m by the triangle inequality.
4. Cases 1–4 have center vertical separation 0.8 m. In case 5, receiver/source separations are at least 0.8 m and source/source separation is 0.44 m. In case 6, every source/source vertical separation is at least 0.4 m and every receiver/source vertical separation is at least 0.7 m. Thus every distinct pair in the entire suite has center separation at least 0.4 m, contradicting the required separation below 0.29 m.

This proof does not assume that the source-to-source down component is zero, or that the primary receiver is the only receiving vehicle. It covers rotating receiver rotors and source axes. Maximum tilt is 15 degrees in case 4 and 10 degrees in case 5, strictly inside the 20-degree M28 orientation limit. Other orientations are identity. Self-contributions remain excluded. Keep all production domain checks active despite this analytic proof.

The argument proves absence of the declared model's near-wake exception; it is not physical far-field validation, a collision/safety analysis, or a guarantee of realistic aerodynamic interactions.

## Prospective treatment and evidence requirements

Use five fixed methods: instantaneous, hold10ms, hold5ms, hold2.5ms and predict5ms. The predictor and hold5ms must have identical actual field-call ticks, including the initial and terminal calls. Prediction uses the last two actual inflow samples for the same rotor, their actual timestamp difference, and nonnegative clipping; use a hold until the second sample. Reset every method cache between cases and timing passes. Do not update the predictor with its own previous predictions, oracle samples, current analytic derivatives, future states, or refined-reference values.

Use integer 0.25 ms ticks, 4000 final tick inclusive, and primary queries every two ticks. Actual refreshes remain on the primary grid; finer reference queries must not alter any treatment schedule. At every refresh, retain old-hold or old-prediction left limits at the same current pose, including t=1 s, and retain the refreshed right value. Do not create a left limit at t=0.

For each method and case, report receiver-0 body-frame thrust and roll/pitch: signed error, augmented sampled absolute peak with time/side, and event-split trapezoidal time RMS. Apply the same prospectively frozen primary/refined sampling screen as the preceding envelope challenge. Preserve screen failures. Nonnegative clipping creates continuous kinks that may still affect quadrature; do not assume the new RMS estimator passes. Report absolute SI values and mg/mgD normalization. Retain the numerical budget target if a common reporting threshold is desired, but do not tune it or select a winning cadence afterward.

Verify **all** production rotor inflows for **all** vehicles against the independent oracle on every fine pose, especially the three source vehicles in case 6. The source-source contributions must not be omitted simply because the comparative performance metric concerns receiver 0. Save states, production and independent fields, indexed discrepancies, and failure context. If loads are independently checked only for receiver 0, state that exact boundary; do not call it all-vehicle load verification. Failure records must preserve the first offending tick, vehicle/rotor or observable, values, tolerance, and any current left-limit state before stopping.

Report outcomes per case before any pooled summary. Case 5 separates two-wake overlap plus receiver orientation from case 4's single-source pitch; case 6 adds dynamic source-source exposure. Six deliberately different cases are six analytic fixtures, not independent estimates of a flight-success probability. A predictor can improve one error metric while worsening another or showing overshoot; retain these distinctions. Match predictor/hold5ms call counts rather than implying matching accuracy.

## Cost and bounded execution critique

The planned 120 s, 200,000-field-call, 128 MiB, one-invocation cap is compatible with the static schedule, subject to the runtime/storage watchdogs. With one production and one independent reference field call on each of 4001 fine ticks, and separate noninstantaneous treatment fields, the scientific phase uses 8906 field calls per case. A primary timing pass uses 2001+101+201+401+201=2905 field calls across the five methods. Six passes (one warmup plus five recorded) over six cases therefore give a nominal schedule total of 158,016 field calls, before any extra fixtures or audits. Count every actual field call; do not count an entire two-/three-/four-vehicle field call as equivalent computational work across cases merely because the counter increments once.

Time the complete declared query loop: analytic pose creation including changing quaternions, unchanged all-vehicle field API, predictor scheduling/extrapolation/clipping, current receiver-0 load response, accounting and timing overhead. Exclude independent model verification, persistence and absent rendering/dynamics. Preserve exact timing checksums against retained primary samples. Rotate the five method orders so the five recorded passes cover every order position; report per-case median and min/max rather than inventing a population confidence interval from technical repeats.

All-vehicle production fields plus receiver-0 loads is a legitimate restricted timing scope. It is not total-flight cost and is not an optimized receiver-only closed-form comparison. Predictor wall time, field-call savings and numerical errors are separate measurements. A faster predictor with larger or unresolved errors is not a qualified replacement. Stop on cap or correctness failure, preserve partial evidence, and do not patch/rerun or add paths after observing results.

## Pre-freeze recommendation

Adopt these six explicit cases once, freeze the code/configuration/dependencies and exact interpretation before execution, and keep source/receiver-state generation independent of treatment history. The suite supplies concrete new stresses without introducing an adaptive algorithm or claiming physical unsteady wake prediction. No broader sweep is needed for this next challenge.
