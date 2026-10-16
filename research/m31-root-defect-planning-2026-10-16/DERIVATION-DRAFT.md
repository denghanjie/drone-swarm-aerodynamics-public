# Draft: polynomial defects of arbitrary predicted rotor ratios

Status: exact-real derivation proposed for independent challenge. No numerical evaluation, runtime certificate, physical validation or novelty claim. The earlier coupled-solve CONTRACT-CHALLENGE already derives log-space contraction factor1/2. This draft seeks a corollary that avoids recomputing roots when checking an arbitrary predicted rotor vector; it does not rebrand that earlier theorem.

## Exact fixed-coefficient problem

For each vehiclei/rotorr, positive nominal force f0_ir and S0_i=sum_r f0_ir. Fixed admitted coefficients a_irj>=0 are finite and independent of the unknown loads. With w_ir=f0_ir/S0_i,

alpha_ir(y)=sum_j a_irj*y_j;
x_ir(y)=g(alpha_ir(y));
F_i(y)=sqrt(sum_r w_ir*x_ir(y));

where g(alpha) is the unique positive root of x^3+alpha*x-1=0. The unique solution y* satisfies y*=F(y*) and x*_ir=g(alpha_ir(y*)). The earlier exact-real proof establishes G(z)=log F(exp z) is1/2-Lipschitz in sup norm on z<=0, while each log rotor root is1-Lipschitz with respect to log source amplitudes. These results require fixed coefficients and the declared positive model domain, not fresh numerical guesses of a Lipschitz constant.

Take any candidate rotor vector0<xh_ir<=1. Define a self-consistent provisional source amplitude

yh_i=sqrt(sum_r w_ir*xh_ir).

This yh is constructed from the candidate roots and CURRENT nominal motors. It is not the previously cached source amplitude. It belongs to(0,1]^N. Define current alpha_h=sum_j a_irj*yh_j and the positive polynomial value

p_ir = xh_ir^3 + alpha_h_ir*xh_ir,
k_ir = max(p_ir,1/p_ir), K=max_ir k_ir.

No cubic root is needed to form p. In exact arithmetic p>0 and k>=1. A finite/nonfinite or out-of-domain candidate must be handled explicitly before this construction; prior invalid secant roots must remain rejected, not clipped to enable this bound.

## Proposed bound

For fixed alpha>=0 put P(x)=x^3+alpha*x. On x>0,

d log P(x)/d log x = (3x^3+alpha*x)/(x^3+alpha*x), which lies in[1,3].

Because P(g(alpha))=1, integrating that derivative implies

|log xh - log g(alpha_h)| <= |log p| = log k.

Write xr_ir=g(alpha_h_ir), the uncomputed root at yh. Thus xh_ir/xr_ir lies in[1/k_ir,k_ir], hence also[1/K,K]. Summing with positive weights preserves the latter multiplicative interval, giving

|log yh_i - log F_i(yh)| <= (1/2)log K.

The inherited1/2 contraction then yields

||log yh-log y*||_infinity <= log K.

The inherited1-Lipschitz log-root map and the triangle inequality give

|log xh_ir-log x*_ir| <= log k_ir + log K.

Equivalently the proposed exact-real enclosure is

xh_ir/(k_ir*K) <= x*_ir <= min(1,xh_ir*k_ir*K).

No roots or log/exp calls are required to express this final interval. The proof uses the complete CURRENT coefficient set; it cannot be applied to an old coefficient matrix to claim a current-load guarantee. It also does not certify intermediate times or a controlled trajectory.

## From rotor intervals to force and moment

Let l_ir,u_ir enclose x*_ir. The candidate-minus-true rotor thrust difference lies in

D_ir=[f0_ir*(xh_ir-u_ir), f0_ir*(xh_ir-l_ir)].

Its absolute upper bound is the maximum absolute endpoint. Summing the four D intervals bounds the body-axis collective force difference. Multiplication by the fixed current rotation's body-z column bounds the world-force norm; if exact unit quaternions are assumed this column has norm1, but actual saved floating quaternions require either explicit arithmetic/error accounting or their actual column norm. It must not be silently assumed to be exactly1 in a numerical certificate.

Roll difference is sum_r y_r D_ir; pitch difference is -sum_r x_r D_ir. Signed interval multiplication is essential. Combine the separate roll/pitch absolute upper bounds using a conservative Euclidean norm. Aerodynamic yaw correction is zero in this model and the common nominal yaw cancels. Normalize rotor/force/moment by the same declared mg/4,mg,mgR units; R=sqrt(2)*.028m. Summing unsigned rotor bounds is allowed as a conservative fallback but may be much looser than signed interval propagation. These are error bounds, not evidence that the predictor meets the thresholds.

## Numerical and cost conditions before use

A floating implementation must enclose p and the reciprocal/max/product operations, including all sums, current motor weights, square roots, coefficients and unit normalizations. A numerical value rounded to nearest is not automatically an upper bound. If p is enclosed in[L,U] with0<L<=U, the prospective safe k is max(1,U,1/L), with outward arithmetic. Intervals must preserve coefficient ownership/order and all rejected/zero support distinctions. If any lower bound becomes nonpositive or an intermediate overflows, return an unqualified result with the reason; do not substitute zero.

An exact-rational reference can treat input binary64 values as exact rationals and enclose square roots using integer square-root bounds. Such a reference would establish the intended arithmetic on a finite saved set, but would not itself be a cheap operational algorithm. No such reference or candidate has been implemented or run in this checkpoint.

The method requires current coefficients and one sparse alpha pass after constructing yh, plus rotor/body interval arithmetic. It may avoid new cubic roots, but current coefficient building dominated the earlier measured large queries. Without a separately justified cheap current-geometry treatment, a root-free check may leave the main bottleneck untouched. Phase costs must be attributed to the exact completed implementation; no new speedup can be inferred from algebra alone.
