# CORE-EXTENT-CERTIFICATE-20261015

Prospective plan, 2026-10-15. Implementation and syntax checking only until independent static review and explicit root release. This is an incremental mathematical benchmark, with no novelty or physical-validity claim.

## Question and frozen design

Does fixed downstream support hide growing summed core inflow as a stipulated independent-source population extends? Compare original support P with axial-support-removed X at one receiver's four rotors. No source-source coupling, receiver load law, ODE, or new Boids flight is evaluated. Core-only does not validate the 8 m axial extrapolation.

Use unchanged public kernel commit 1336f5c416875a9651f92b58b2ed06649f25b04e: snapshot/outputs/step03a-source/wake.cjs, milestone-28-source/aero.cjs, step02c-source/physics.cjs and milestone-26-source/grid.cjs beneath research/campaign-joint-stage-reference/implementation. Their SHA256 identities are frozen in the runner and checked before import and after evaluation. Import aero for constants only; never call A.fields, integrate, or controller code.

One receiver at (0,0,0), identity quaternion. Its rotors are the original ordered (a,a),(-a,a),(-a,-a),(a,-a), a=0.028 m. Sources have identity orientation and the original hover-induced speed vi. Each is one merged vehicle jet, not four source-rotor jets.

Six fixtures, fixed order phase-major then extent:
- delta=0.25 m, d_j=0.5+j*delta, all d_j<=L.
- L=2,4,8 m; horizontal phases (0,0), (0.125,0.125) m.
- x=kx*delta+phase, y=ky*delta+phase, integer kx,ky; retain x*x+y*y<=R(d_j)^2.
- D=2*sqrt(2)*a, r0=D/2, s=5.817*D, k=0.07668, b(d)=k*(d+s), R(d)=2*b(d)-r0.
- Enumerate height, y, x ascending. Canonical coordinates are ordered xyz Float64 little-endian triples, SHA256 hashed in memory, never retained as duplicate raw input. No random values or postresult fixture changes.

The rotor offset margin gives radial<=R+r0=2*b for all four rotors. Downstream>=0.5>2.5D; no near guard is encountered. Source/receiver projection is one. Static stress fixtures are not a flock or a substitute for genuine Boids.

## Arms and finite proof

Evaluate immutable W.normalizedWake(d/D,radial/D).speed*vi. P retains original axial fade fz and radial fade fr with production support tests and multiplication order; X removes only axial fade/cutoff and retains fr. Assert fr===1 and xi<=2+1e-12 for every evaluated term. Original fz is 1 below 2 m, smoothstep fade on [2,2.5], zero at/above 2.5. All sources are enumerated for this single receiver. Original finite P support fits within 3 m; verify its conservative center-distance envelope<2.64 m so bypassing grid search cannot omit/introduce P contributions.

Let A=10.11*D*vi, c=sqrt(2)-1, f2=(1+4*c)^-2 and n_j the exact source count at layer j. The formal core speed lies between A*f2/(d+s) and A/(d+s). With B=sum_j n_j*(1-fz(d_j))/(d_j+s), each rotor obeys

A*f2*B <= X-P <= A*B.

Check direct summation of omitted pair terms against X-P. Report both bound slack and cancellation residual. Independently check the closed-form speed against the imported normalized function, without treating agreement as physical validation.

Continuum rationale: integral over a centered source disk of radius Q is F(d,Q)=pi*A*k^2*(d+s)/c*[1-(1+c*(Q/b)^2)^-1]. Each offset rotor's layer integral lies between F(d,2b-2r0) and F(d,2b). Their difference is O(1); at uniform density eta, X=C*L^2+O(L), C=eta*pi*A*k^2*[1-(1+4c)^-1]/(2c), and N=4*eta*pi*k^2*L^3/3+O(L^2). Hence formal X=Theta(N^(2/3)), whereas P saturates. For lattice layers, cell inclusion gives pi*max(R-h,0)^2<=n_j*delta^2<=pi*(R+h)^2, h=delta/sqrt(2); summing yields the same growth order. The run checks these finite count inequalities, not continuum quadrature or a fitted asymptotic exponent. Increasing pointwise inflow is not by itself proof of momentum violation.

## Checks, stopping and evidence

Preflight generate all six fixtures; cap each at 4,096 sources and the total at 196,608 source/rotor/arm slots. Verify nested coordinate prefixes, all expected layer counts, source uniqueness, and source identity. Per fixture retain hash, exact layer counts, four P/X inflows and U/vi, B/bounds, omission fractions, largest individual term/witness, xi/distance extrema, check residuals and completed coverage. Coordinates stay in memory and are rehashed after scoring to check nonmutation.

Tolerance: 1e-12*max(1,abs(a),abs(b)) for scalar comparisons. Require finite nonnegative terms, all finite bounds, positive omitted lower bounds at L=4/8, P(4)=P(8) bitwise per rotor, and X(8)>X(4)>X(2). These are mathematical checks, not physical pass/fail thresholds. Retain failures and partial coverage; no hidden retry or retuning. One released attempt, exclusive results directory; root enforces 60 s wall. Runner stops cooperatively at 59 s.

Output cap 100,000 bytes including receipts; total campaign cap 200,000 bytes including plan/code/proof/results/demo summaries. Runner<=15,000 bytes, plan<=6,000. No raw arrays, large plots, downloads, paid compute, or private R8 access. Summary and progress are atomically replaced, with separate failure-receipt attempt. Final status requires six fixture receipts, expected pair coverage, cross-extent checks, source recheck and caps. Root's outer supervisor preserves timeout/exit status and stdout/stderr.

Reuse PUBLIC-SUPPORT-FACTORIAL-20261015's existing 401-row genuine local3D replay as context only: it had no axial-cutoff exposure. Do not rerun it, infer changed flight, or treat the stress population as measured aerodynamics. Related-work/interpretation limits are in ../research-publication-path/ASSESSMENT.md.
