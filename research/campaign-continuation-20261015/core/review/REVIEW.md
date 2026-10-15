# Independent proof and static execution review

2026-10-15 UTC. READY for one explicitly released, externally supervised attempt. No fixture generation, model calls or runner execution occurred in this review. Read source and code only.

Frozen plan: PLAN.md, 5,660 bytes, SHA256 b71f9b869b64836b38f0cb21c87cebd460def9cafd62dee9315d4d68c4ca4eaa.
Runner: run-core-extent.cjs, 14,660 bytes, SHA256 f61b20ca327110262dd55fe4b8f907acca959e34c54a74caad742d4306439c3a.
Interpretation reviewed against research-publication-path/ASSESSMENT.md, SHA256 e4369477b4996dadf8ac7b2645eea93a96bbdf0c27b16de03a545d9a6231e014.

## Finite all-rotor certificate

With r0=sqrt(2)*a=D/2 and R(d)=2*b(d)-r0, each actual rotor has horizontal offset norm r0. The triangle inequality gives radial distance <=R+r0=2*b for every included source. The lower disk radius 2*b-2*r0 is positive already at d=0.5 and increases with d. Identity orientations give projection one; d>=0.5 exceeds the source model's near-field floor 2.5*D. A source is one merged vehicle jet, not four source-rotor jets.

For c=sqrt(2)-1, t=d+s and xi=radial/b in [0,2], the unchanged profile is u=A/t*(1+c*xi^2)^(-2). Its radial factor lies between f2=(1+4*c)^(-2) and 1. Each omitted term has weight 1-fz>=0. Multiplying the pointwise inequality by that weight and summing the exact layer counts gives A*f2*B <= X-P <= A*B separately for every rotor. This proof needs no empirical ground truth: it certifies a difference between two stipulated mathematical sums. It supplies no bound on physical error.

Production support is downstream<2.5 and radial<3*b. A conservative source-center envelope is sqrt(2.5^2+[3*k*(2.5+s)]^2)+r0; the runner adds 1e-6 m before requiring <2.64 m and <3 m. Thus the all-source P calculation cannot add a nonzero contribution omitted by the original center-neighbor radius. Source heights also avoid near-field guard behavior. This equivalence is specific to these upright fixtures, not arbitrary swarm geometry.

## Extent argument

Integrating the stated radial profile over a centered disk gives F(d,Q)=pi*A*k^2*t/c*[1-(1+c*(Q/b)^2)^(-1)]. Relative to each offset rotor, the source disk contains a rotor-centered disk of radius 2*b-2*r0 and is contained in one of radius 2*b. Both layer integrals have the same positive leading coefficient times d, and their difference is O(1). Integration over height therefore gives the stated continuum C*L^2+O(L), while source volume gives N=4*eta*pi*k^2*L^3/3+O(L^2).

For any horizontal lattice phase, each square cell lies within h=delta/sqrt(2) of its center. The union of cells with centers in radius R contains the disk max(R-h,0) and lies inside radius R+h. Its area is n*delta^2, establishing the two count inequalities. With fixed vertical spacing these counts and the finite speed bounds establish the same Theta(N^(2/3)) growth order. They do not establish the continuum coefficient for finite lattice fixtures. Three tested extents cannot estimate an asymptotic exponent. Increasing inflow alone proves no momentum violation because total source forcing increases too.

## Runner correspondence and safeguards

Static comparison with the immutable public wake/aero/physics/grid code confirms the normalized profile, original ordered rotor offsets, area-first induced-speed arithmetic, normalized-downstream half-width arithmetic, fade polynomial and P multiplication order. The public-baseline path is resolved explicitly. The runner imports aero for constants and does not call its field, load, controller or integration functions.

Generation is deterministic height/y/x enumeration, phase-major then extent. The fixture builder checks source uniqueness, layer coverage and finite cell-count bounds. Preflight checks exact coordinate/layer prefixes, maximum 4,096 sources per fixture and the total 196,608 arm-slot ceiling before scoring. Coordinates use ordered Float64 little-endian triples for hashes, without retained duplicate arrays.

Scoring asserts xi<=2+1e-12, radial weight exactly one, safe downstream domain, finite nonnegative pair terms and agreement of the closed expression with the imported profile. Every rotor has direct omitted-pair summation, aggregate-difference cancellation checks and finite-bound/slack reporting. Cross-extent checks require bit-identical P(4)/P(8), strict X growth and positive omitted lower bounds at 4/8 m. Exact coverage, input rehashing and public-source rechecks gate final success. Scalar tolerance matches the plan.

An explicit --execute and hash-bound ADOPTION.json are required. Results-directory creation is exclusive. Atomic replacements account for old plus pending bytes; ordinary output reserves 8 KB for failure evidence. Progress and failure-receipt writes are attempted separately. Partial fixture completion and source/rotor location survive ordinary exceptions; an outer supervisor must retain timeout, exit code and stdout/stderr if termination prevents an internal receipt. The 59-second cooperative checks do not replace the root's 60-second wall limit. The 100 KB output and 200 KB campaign caps include subsequent receipts/reviews.

## Scope and decision

No blocking mathematical or static implementation issue found. Root may bind the reviewed hash and release one attempt. Failures must remain terminal evidence without hidden retuning.

These are static stress populations, not Boids flight or physical truth. Staying within the radial core does not validate 8 m axial extrapolation, linear source independence, entrainment, room boundaries, wake age or response of a real receiver. Existing replay remains context only and supplied no axial-cutoff exposure. The report should present finite bounds and extent ratios, without novelty, speed, changed-flight or measured-aerodynamics claims.
