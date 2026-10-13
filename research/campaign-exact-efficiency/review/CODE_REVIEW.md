# Exact evaluator: independent code and tiny-probe review

Reviewed source SHA-256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`.

## Decision

Approved for the broader independent correctness matrix on the A1/A2 amended, frozen source. Timing remains conditional on that matrix and an exclusive measurement window. This is a numerical implementation review, not physical validation.

## Positive findings

- Scalar quaternion rotation preserves the original component operation order. Dot products retain the initial zero and ascending component order. Wake normalization, source strength, profile, support comparisons and fades preserve the original expression order.
- All four receiver rotors remain. The original grid sorts candidate source IDs, and every rotor accumulates in ascending source order. The kernel retains the original rotor-major guard traversal, including first-error identity when one source is invalid for rotor 1 and another for rotor 0.
- Support flags never threshold a positive wake value. They use only conservative center-envelope tests of the already declared compact support. A support-zero pair inside the near-domain envelope still executes the original per-rotor near-wake guard; only a support-zero pair provably outside that envelope bypasses it.
- All states receive global tilt checks before pair traversal. New finite/unit-quaternion and coordinate checks are numerical API hardening, not claims of identical malformed-input behavior in legacy code.
- The reuse evaluator owns only geometry/pair-flag scratch. Returned winds, counters and result records are fresh per call. Relevant scratch prefixes are refreshed on every evaluation, including smaller swarms, and later growth reuses only fully overwritten slots. Failed preparation cannot create stale accepted output in a later valid call.
- Load conversion retains all four effective thrusts, world force, body roll/pitch moments, and the nominal yaw-torque convention. Physics integration, controller cadence, wake refresh and Boids rules remain inherited rather than redesigned here.

## Pre-measurement failure and correction

Version 0 (`ff34626a3ba63a50195c17ecd63df2ef7aa50ef2bfa438b7519ca64f7b2ced6b`) assumed the nominal rotor-offset radius plus a fixed tiny margin covered every finite translated state. At a receiver y coordinate of `3e14 m`, a 45-degree yaw causes the stored rotor point to round to a y offset of `0.0625 m`, larger than the nominal `0.03959798 m` radius. A two-state edge fixture then has legacy/lean inflow `0.001587065203100887 m/s` on one rotor, while support/reuse falsely return zero. Complete states, observed outputs and source identity are retained in `large-translation-v0.json`; this is an intentionally extreme software stress case, not a plausible flight configuration.

A second inherited issue is nontermination in the original grid at finite position `1e20 m`, where integer loop increments cannot advance. An isolated two-second probe of previous-zero exited with timeout status 124. It was not a timing measurement.

Amendment A2 restricts new evaluator position components to absolute value at most `1e6 m` and adds `128 * Number.EPSILON * 1e6 = 2.8421709430404007e-8 m` conservative coordinate roundoff padding. The original unit-quaternion envelope inflation remains. Rejected larger inputs are explicit API restrictions, not same-output equivalence outside the domain. The archived failure and amended rejection are both retained. No benchmark or held-out performance result preceded this correction.

Within the bounded position domain, a rotor-point addition and center subtraction incur errors far below that padding, including near-unit rotation arithmetic. The accepted source-axis norm deviation is also far below the `1e-8` radial-operator inflation. Radial support width is monotone in downstream distance; using the largest possible downstream and smallest possible radial distance cannot cull a positive in-model rotor contribution. The unchanged 3 m center search remains larger than the entire positive-support and near-domain center envelopes.

## Eight focused amended-source checks

`targeted-guards-v1.json` records four accepted near-limit translation/yaw fixtures at quaternion norms `1 ± 8e-11`, one simultaneous multi-source near-domain violation with the original first source identity, a near-domain failure at large accepted coordinates, and inside/equal axial-cutoff cases. All three new variants match original inflows bitwise on valid fixtures and match original exception type/detail on invalid-domain fixtures. Source hash remained unchanged.

The independent broader matrix supplies ownership, size-change, malformed-input, all-pairs, permutation and other coverage. Passing finite tests is evidence rather than a formal proof for every representable input. Numerical-domain restrictions and counterexamples must remain visible in the final report.
