# Ideal axial actuator-disk coefficient reference

This package implements one conditional algebraic model, not a propeller performance prediction or a data analysis. Assume steady incompressible axial flow through an isolated, uniformly loaded, non-swirling ideal actuator disk. Let the undisturbed axial speed be V >= 0, induced speed at the disk be vi >= 0, thrust be T >= 0, density be rho > 0, and disk area be A = pi D^2 / 4 with D > 0. Rotation rate n > 0 is in revolutions per second.

The ideal momentum relation is

    T = 2 rho A vi (V + vi).

Solving the quadratic for its nonnegative propulsive branch gives

    vi = -V/2 + sqrt(V^2/4 + T/(2 rho A)).

The ideal disk power is force times flow speed through the disk:

    Pideal = T (V + vi)
           = T [V/2 + sqrt(V^2/4 + T/(2 rho A))].

Use the explicitly assumed conventional propeller coefficients

    CT = T/(rho n^2 D^4),
    J  = V/(n D),
    CP = P/(rho n^3 D^5).

Since T/(2 rho A) = (n D)^2 (2 CT/pi), dividing the power expression by rho n^3 D^5 yields

    CPideal = CT [J/2 + sqrt(J^2/4 + 2 CT/pi)].

This is the form implemented directly: the positive terms avoid subtracting nearly equal velocities. Equivalently, writing lambda = vi/(n D), CT = (pi/2) lambda (J + lambda) and CPideal = CT (J + lambda). The static limit is CPideal = sqrt(2/pi) CT^(3/2). Scaling CT by s^2 and J by s, for s > 0, scales CPideal by s^3; these identities support elementary synthetic tests.

The physical assumptions eliminate swirl, profile drag, nonuniform loading and finite-blade losses. The relation is an ideal disk baseline at the supplied thrust, not a prediction of measured shaft power, thrust, controller behavior, torque, aerodynamic calibration or an entire vehicle's electrical power. Density cancels algebraically only under the same coefficient convention. A dimensional channel compatibility screen is still required before applying it to ENOLA coefficients. Measurement/tare uncertainty, tunnel effects, specimen geometry and convention provenance are not supplied by this derivation.

The callable admits finite CT >= 0 and J >= 0, including CT = 0 solely as a mathematical boundary. The proposed measured-row eligibility remains stricter: positive n, T, Q, CT and CP with nonnegative V and J, after the separate convention screen. Negative thrust, reverse flow, windmill branches, vortex-ring behavior and general oblique inflow are outside this branch. Signed zero is treated as zero. No data row is classified or scored by this package.

An apparent CPideal/CPshaft > 1 would be a conditional discrepancy requiring provenance and uncertainty investigation. It is not, by this calculation alone, an energy-violation finding or a universal physical pass/fail test.

## Numerical construction

`ideal_power_coefficient(Decimal(CT_text), Decimal(J_text), precision)` supports exactly 80 or 120 significant decimal digits. Inputs must originate from retained decimal text; binary floats are rejected. Each call uses a fresh ROUND_HALF_EVEN context with 32 guard digits and Decimal square root, then rounds once to the requested output precision. Exceptional exponent-range or underflow failures propagate rather than causing rescaling or retries. Caller precision, rounding, traps and flags are preserved.

Pi is calculated independently using Machin's identity, pi = 16 atan(1/5) - 4 atan(1/239). The arctangent alternating series is evaluated with 16 additional guard digits and a fixed small-term cutoff. One justification: tan(2 atan(1/5)) = 5/12, tan(4 atan(1/5)) = 120/119, and tan(4 atan(1/5) - atan(1/239)) = 1; the relevant angle lies in the first quadrant, so it equals pi/4. No binary64 pi constant or measured value enters the implementation.

`reference_pair(CT, J)` returns both outputs, their absolute difference evaluated in a fresh 160-digit context, the fixed tolerance 1e-50, and its Boolean agreement result. Both values are retained when agreement fails. The two precisions share an implementation: agreement screens precision sensitivity, not independent code correctness. Guard digits, a convergent pi series and elementary identities are not an end-to-end certified rounding bound. The reference implements the chosen formula; it is not independent experimental validation of that formula.

Later callers computing ratios or signed discrepancies must explicitly choose and document their Decimal context rather than accidentally falling back to Python's usual 28 digits. This module does not calculate any measured power ratio, discrepancy, summary statistic, binary64 error or timing benchmark.
