# Adopted conditional corollary: arbitrary-root defect

2026-10-16. Read this together with the immutable DERIVATION-DRAFT.md and the complete independent MATHEMATICAL-CHALLENGE.md. This note incorporates the review; it does not overwrite the published draft. No numerical evaluation occurred.

For exact positive nominal forces, exact weights w_ir=f0_ir/sum_r(f0_ir), and complete fixed finite nonnegative CURRENT coefficients a_irj, define the original model by

    alpha_ir(y) = sum_j a_irj*y_j
    x_ir(y)^3 + alpha_ir(y)*x_ir(y) = 1
    F_i(y) = sqrt(sum_r w_ir*x_ir(y)).

The inherited log-space contraction is 1/2 and the log-root map is 1-Lipschitz. For any candidate 0 < xhat_ir <= 1, construct the exact candidate-derived yhat_i=sqrt(sum_r w_ir*xhat_ir). Define

    p_ir = xhat_ir^3 + (sum_j a_irj*yhat_j)*xhat_ir
    k_ir = max(p_ir, 1/p_ir), K = max_ir k_ir.

The independently checked enclosure is

    xhat_ir/(k_ir*K) <= xstar_ir <= min(1, xhat_ir*k_ir*K).

The proof uses the logarithmic derivative of x^3+alpha*x, which lies between 1 and 3; this bounds the local root defect by log(k_ir). Candidate-derived source inconsistency is at most log(K)/2; contraction bounds source error by log(K). Adding source sensitivity and local root defect gives the interval above. No new contraction theorem is claimed.

## Necessary scope clarifications

1. Coefficients and weights must correspond to the same current nominal motors and current geometry. Current coefficients are fixed with respect to unknown loads. Admitted zero support is distinct from rejected support. No clipping, stale matrix, load-dependent support or unaccounted geometry perturbation is allowed.
2. To certify the original guarded model, its cap/admission conditions must hold throughout the required source domain, using the inherited whole-cube argument or a separately proved invariant domain. Checking the candidate alone is insufficient. Without that bridge the theorem concerns only the frozen algebraic coefficient problem.
3. Source amplitudes in the proof are the exact weighted square roots of the candidate. A rounded source or independently rounded weights cannot silently substitute for that exact identity. Enclose their construction.
4. The formula avoids **cubic-root solves**. Square roots remain in source amplitudes, norms and normalization. “Root-free” is not a claim that all root arithmetic disappears.
5. If outward arithmetic encloses p in [L,U] with L>0, use an outward kbar=max(1,U,1/L) and global Kbar. Outward evaluation of the same interval with kbar,Kbar remains conservative. Invalid candidates, missing admission, nonpositive lower bounds or unbounded arithmetic produce named unqualified results, not successful zero-error certificates.
6. Exact rational interpretation of supplied binary64 coefficients certifies the assembled coefficient model. It does not enclose their geometric construction or validate physical airflow. Actual saved rotation-column arithmetic certifies that linear map, not the unknown physical attitude.

## Body-load bound

For each enclosing rotor interval [l,u], candidate-minus-solution thrust lies in D_ir=[f0_ir*(xhat_ir-u_ir), f0_ir*(xhat_ir-l_ir)]. Sum signed intervals for collective thrust. Multiply its largest absolute endpoint by an enclosure of the norm of the declared current rotation's body-z column for world-force error. Do not assume a saved near-unit quaternion is exactly unit.

For fixed rotor coordinates (x_r,y_r), propagate roll=sum_r y_r*D_ir and pitch=-sum_r x_r*D_ir using signed interval multiplication, then a conservative Euclidean norm. The zero aerodynamic yaw difference is inherited from this shared-axis correction model; it is not a physical yaw statement. Normalize with conservatively enclosed positive mg/4, mg and mgR. The entire construction, including denominators, needs outward arithmetic for a numerical certificate.

## Status

Adopted as a conditional exact-real corollary only. Floating-point soundness, useful tightness, runtime cost, physical validity, novel priority and flight benefit are untested. The original draft and both independent reviews remain retained. No certificate implementation or numerical allocation is created by this note.
