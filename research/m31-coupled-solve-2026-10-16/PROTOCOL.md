# Four-rotor steady coupling: bounded implementation verification

Prospective protocol, 2026-10-16. This is a new small computational question motivated by the completed source-accounting audit, separate from all closed experiments and the expired original overnight launch window. No field/load result for these fixtures has been computed at protocol creation. It is development verification of a hypothesized law, not a held-out physical experiment or publication-ready performance campaign.

## Question and contract

Can descending-height evaluation solve an admitted acyclic four-rotor load system as accurately as simultaneous iteration, while evaluating fewer roots? Does simultaneous iteration converge on a prescribed directed cycle? Does the implementation reject the unsupported nearby configuration instead of replacing it with zero?

The full law and proof are in review/CONTRACT-CHALLENGE.md. With positive nominal per-rotor forces f0, fixed admitted nonnegative hover-field coefficients K, total nominal force S0, and source amplitude y=sqrt(S/S0), use a_irj=K_irj*sqrt(S0_j/mg)/sqrt(f0_ir/(2*rho*A)), x_ir=g(sum_j a_irj*y_j), g the positive root of x^3+alpha*x-1=0, and F_i(y)=sqrt(sum_r f0_ir*x_ir/S0_i). Retain all four roots. Source scaling by sqrt(effective total force), fixed wake shape/support, summed scalar inflows and the ideal-power receiver closure are explicit unvalidated assumptions. Unequal source-rotor loads do not alter source shape. This is not a fixed-PWM or fixed-RPM model.

Copy the historical pairTerm verbatim. Every rejected symbol4 or11 rejects the entire geometry; no solver runs there. Verify unit axes, rotor offsets perpendicular to own axis with norm R=sqrt(2)*.028, all positive f0, and K*sqrt(S0_j/mg)<=128 over the full y cube. Zero coefficient must be an admitted zero. Baseline constants are those in the source-accounting witness (mg=.027*9.81 N, rho=1.225, rotor radius=.023 m).

## Frozen deterministic fixtures

No seeds, fitting or parameter sweeps. Every definition below is frozen before evaluation. Use IDs ascending for accumulation. In each admitted case f0_ir=(mg/4)*[.8+ .1*((i+2*r) mod 5)], making nominal forces positive and unequal. Four rotor offsets are arm*(s*u+t*v), signs (-1,-1),(1,-1),(1,1),(-1,1). For a unit axis a, choose u=normalized(zhat cross a) when its horizontal norm exceeds 1e-12, else u=xhat; v=a cross u. Geometry values are computed once and saved.

1. `level-ladder`: eight centers (0,0,.4*i), axis (0,0,1).
2. `tilted-ladder`: eight centers (.035*(-1)^i,.02*(i mod 3),.4*i), tilt beta_i=(-1)^i*pi/12 in x-z plane, axis (sin beta_i,0,cos beta_i).
3. `hexagon-cycle`: six centers at vertices of a regular horizontal hexagon, side L=2*sqrt(10)*R, circumradius L, q_i=(L*cos(i*pi/3),L*sin(i*pi/3),0). Axis a_i=3/sqrt(10)*(q_i-q_(i-1))/L + zhat/sqrt(10). Check prescribed edges i to i-1 after admission; preserve failure if any other pair rejects the whole geometry.
4. `near-rejection`: centers (0,0,0),(R,0,0), axes (-sin(pi/12),0,cos(pi/12)) and (sin(pi/12),0,cos(pi/12)). Choose each square frame so a rotor points along the rejection construction in review/DERIVATION-AND-NEXT-QUESTION.md. This is a deliberate unsupported-input control. No solver is allowed if rejected.

## Methods, limits and measurements

One Node scientific invocation after source commit/push and independent remote manifest verification. Maximum 30 seconds wall time, four fixed fixtures, 64 simultaneous updates per admitted fixture, 56 bisection loop iterations for every nonzero-alpha root (alpha=0 returns exactly 1). A runner records source commit, exact frozen manifest hash, stdout/stderr and exit; scientific failure consumes this invocation and is retained. No rerun or fixture repair in this campaign.

Compute all 4*N*(N-1) coefficients once, storing every pair's symbol, geometry diagnostics and K; record pair calls, positive rotor terms, unique vehicle edges, unsupported terms and scaled cap bound. Order by descending center height, ID for ties. A direct solve is admitted only if every positive edge points from an earlier to a later node; otherwise record ineligible. The direct pass performs exactly four rotor closures per vehicle. Compare synchronous Picard starting y=1, with fixed source-ID summation. Save all iterates. Stop when max abs(log(y_next)-log(y))<=1e-11; save y_next and independently reevaluate its residual once. Separate iterative update work, final residual work and direct-solve work. Count root closures, bisection iterations and positive-term multiplications; include geometry pair work. No elapsed-speed or end-to-end speedup claim is made from these counts.

Also save the one-update y=1 loads as the explicit uncoupled-source ablation. It is a baseline, not a converged result. Report maximum relative per-rotor difference from the coupled direct/reference result. This isolates the consequence of the new source amplitude law within the assumed model, not whether it improves reality.

One independent saved-evidence review invocation, <=120 seconds, frozen before scientific execution. Reimplement geometry/support separately and compare all saved symbols and coefficients within 2e-12 absolute plus 2e-12 relative. Check saved axes/frames and fixture identities. Independently solve the serialized dimensionless coefficient system using 80-digit Decimal Newton roots, up to 100 inner iterations and 160 simultaneous updates, target log residual 1e-40. Compare final amplitudes and every per-rotor force, direct vs simultaneous and Decimal reference: relative tolerance 1e-9. Recompute candidate log residual at high precision and report theoretical error estimate 2*r_log, plus per-rotor relative estimate exp(2*r_log)-1. This high-precision review is NOT outward-rounded interval arithmetic or a machine-checked numerical certificate; report the precision and limits. The exact-real proof is distinct from the numerical evidence. No scientific result execution by browser or GPU.

## Decisions and limitations

Pass development verification only if both ladders admit with nonzero influence, direct and iterative solutions agree under tolerance, all independent checks pass, the hexagon admits and retains its six-edge cycle with a converged solution, and the nearby fixture rejects without a solve. If any condition fails, preserve it and narrow the conclusion. Do not fix source or loosen thresholds after results. Agreement checks implementations of an assumed model; it does not validate aerodynamic truth. This is four designed cases, not a population sample; no confidence interval, statistical significance or physical safety claim.

Follow successful verification with a separately planned fresh case campaign and end-to-end timing before scaling claims. Important unresolved work: physical source/receiver law, trajectory-level dynamics and Boids integration, 5,000-drone browser execution, hardware timing, novelty and publication gate. This milestone provides a Three.js inspection of actual saved geometry, edges and load iterates; label it recorded steady-solver replay, not flying or fluid simulation, and link the historical local-Boids view. No invented flock animation.

Source freeze, publication checks, reviewer and reproduction records accompany this protocol. Ordinary source parsing is allowed before freeze but target coefficient/root evaluations are not. The independent reviewer may identify source defects before freeze without running targets; record revisions before execution. Original static note's averaged-inflow proposal is superseded here by the four-rotor contract without editing that historical note.

## Pre-execution clarification

The exact near-control frame is e=the prescribed unit corner direction, f=axis cross e, u=(-e+f)/sqrt(2), v=axis cross u. Thus rotor index0 is R*e; rotor order remains the stated signs. Both methods separately save the receiver force array reevaluated at the returned final y, in residualMap; generating loads and final reevaluated loads are not silently identified. These clarifications precede all target calculations.

Before any target run, independent static review corrected work terminology: bisectionIterations counts polynomial loop evaluations, not guaranteed IEEE interval halvings (the midpoint may stagnate). Reviewer outer budget was prospectively changed from100 to160 because the global factor1/2 alone need not achieve1e-40 in100 updates. With at most8vehicles, scaled term cap128 and f0≥.8mg/4, alpha≤7*128/sqrt((.8mg/4)/(2*rho*A)); g(alpha)≥1/(alpha+1) bounds the initial log change, making160 sufficient in exact arithmetic. No target values informed this change. candidatePass is only the candidate's structural gates; full qualification requires the independent numeric checks.
