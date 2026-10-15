# Error-budgeted refresh envelope — prospective challenge

**Unexecuted proposal until source freeze and review.** Test whether a conservative analytical field envelope can choose update intervals that stay within a declared model-load error budget, and whether its full overhead costs less than fixed holds. No novelty or physical validity is assumed. This is one fresh analytic encounter, not confirmation on a flight population.

## Why this follows the pilot

The previous prescribed-path pilot (`fd857ed` source, `4965c73` results) showed ordinary hold-error/cost trade-offs, already known from the newer internal temporal study. It also exposed 5 ms uniform-RMS sampling failures. Those failures remain. This experiment changes the RMS estimand prospectively to a time-integral approximation using event-split trapezoids; it does not relabel the old result. Relevant mean-wake, receiver and prior-work sources are linked by the [existing ledger](../m31-airflow-cadence-2026-10-15/literature-and-prior-work.md). The interval construction below is our direct mathematical derivation for those declared equations; it is not attributed to an external algorithm or claimed as new. A broader novelty search remains required before publication claims.

## One frozen challenge and comparison

For 0≤t≤1 s, source is fixed at [0,0,1.8] m; receiver is [0.34 cos(πt), 0.04 sin(πt), 1.15+0.08 cos(πt)] m. Both orientations stay identity, yaw and angular velocity zero; all motor-state thrusts are mg/4. These kinematic poses are not integrated flight. The path crosses radial wake support, varies spacing and speed, and excites both moments. Its global speed bound is π√(0.34²+0.08²), acceleration bound π²√(0.34²+0.08²). They are bounds for this prescribed input, not an observer for unknown real motion.

Compare six variants on the same poses: instantaneous formula; holds at 10/5/2.5 ms; causal linear prediction with 5 ms actual field refresh; and the envelope scheduler. All actual field calls use unchanged M28 `sum-rotor`. Prediction uses only the last two actual inflow samples, extrapolates their slope, clamps predicted inflow at zero, and uses a hold before the second sample. No future path fields inform predictions. Report prediction onset/turning behavior without fitting.

Envelope load budgets: εT=0.005mg and εroll=εpitch=0.005mgD, D the opposite-motor distance. These are analyst-chosen numerical fidelity targets for this challenge, with no physical/safety significance. Choose the longest accepted horizon from 16,8,4,2,1,0.5 ms, never beyond the final time. If no candidate meets both domain and budgets, stop the entire invocation and retain the failure; no tuning, shorter step or retry. Use exact integer ticks of 0.25 ms; all refresh events occur on the primary 0.5 ms grid. Refinement queries every0.25 ms do not change refresh schedules.

## Analytical envelope and its limits

At refresh time t0, use δ(h)=min(Vmax h, |v(t0)|h + Amax h²/2). With fixed yaw this bounds every relative rotor-center displacement throughout the hold. Endpoint displacement alone would not suffice. For each receiver rotor, define d±=d0±δ, r−=max(0,r0−δ), r+=r0+δ. Reject any interval with d−<2.5D before support shortcuts.

Let C(d)=v_induced·10.11/(d/D+5.817), H(d)=0.07668(d+5.817D), F(d)=downstream fade and Q(ξ)=radial fade/[1+(√2−1)ξ²]². C,F,Q decrease and H increases on this domain. The full wake need not decrease with downstream distance. A real-arithmetic enclosure is

U−=C(d+)F(d+)Q(r+/H(d−)); U+=C(d−)F(d−)Q(r−/H(d+)).

It handles radial support entry and downstream fading conservatively. Fixed source strength, orientations and receiver nominal thrust are essential. Apply monotone decreasing receiver response to get rotor-thrust bounds. Subtract each actual production held rotor load, then sum signed intervals for thrust and y_k/-x_k weighted roll/pitch. Do not allow unproven cancellation. Independent rotor bounds discard actual correlations and may be loose.

Implementation adds declared 1e-12 m/s wind margins and 1e-14 N thrust margins around independent bisection-root brackets. These are explicit numerical allowances, **not formally verified outward rounding**. Dense independent checks can find violations but cannot prove continuous-time floating-point containment. Call the result an empirically checked analytical envelope, not a certified safety guarantee. This two-drone restriction avoids cached-neighbor entry and many-source accumulation issues; neither scalability nor general yaw/tilt coverage follows.

## Measurements and gates

Save every fine-grid pose, reference inflow, treatment inflow, modeled total thrust/roll/pitch, refresh flags, old-hold/prediction left limits at every event including terminal, and envelope decisions with proposed horizon, δ, bounds and evaluated error estimates. No left limit at t=0. Independent all-pairs/bisection oracle checks every reference fine pose within1e-12 SI units. Require the envelope's current interval to contain observed load errors at all uniform and refresh-left queries within the declared1e-12 check tolerance; record exact worst excess and time. Any violation fails this candidate, stops the entire invocation before timing and prohibits its speed claim. Do not silently expand bounds after observation.

Compare augmented sampled peaks and event-split time RMS from squared-error trapezoids on 0.5 and0.25 ms grids. At a refresh, use the old value for the preceding interval's endpoint and the new value to start the next. The primary/fine sample differences must be ≤max(5% refined value,1e-9 N or1e-11 N·m) to pass that diagnostic screen. Preserve failures without another refinement. Neither sampled peaks nor trapezoid convergence is a proven continuous bound. Report all fixed/predicted/envelope results, including violations of numerical targets; only the envelope seeks to enforce targets by construction.

Timing: one warmup and five recorded passes per variant at0.5 ms queries; rotate order across passes. Include pose creation, current velocity, displacement bounds, all horizon attempts, bisection bounds, fallback/refresh decisions, field, receiver, accounting and timing overhead. Save field and bound call counts separately. Compare complete-loop median and min/max, with exact output checksums against retained primary samples. All variants use the same existing field API; this is not a comparison with an optimized two-drone closed form. Exclude only independent verification, saved-data persistence, rendering and absent flight/Boids/contact/GPU work. Fewer field calls do not establish a speed improvement.

Candidate decision is conditional and per encounter: all sampled containment checks and numerical targets must hold; any cost improvement must be measured against the fixed baselines with their actual errors disclosed. The causal predictor has the same field-call schedule as hold5ms, enabling a matched-call comparison. No statistical-population claim, uncertainty CI from dependent samples, physical cadence recommendation or publication-readiness claim follows.

## Budget and immutable evidence

One supervised invocation;120 executable seconds,50,000 total field calls including independent oracle/warmup/timing,100,000 bound attempts,64MiB raw data, no paid resources. All counters include failed calls. External watchdog and cooperative guards stop work; retain partial records. No post-outcome patch/retry. Freeze protocol/configuration/all sources and dependencies, privacy-review and push before running. Save raw evidence, every failed check, independent saved-record review, 3D milestone and source-linked claim ledger. Do not restart either prior terminal campaign.
