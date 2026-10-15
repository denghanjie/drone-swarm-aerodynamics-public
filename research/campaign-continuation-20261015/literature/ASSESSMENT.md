> Historical prospective assessment, preserved after completion. See the [core result](../core/results/REPORT.md) and [independent review](../core/results/INDEPENDENT-REVIEW.md). This assessment does not claim novelty.

# Publication path: an extent-aware support certificate

Planning only, 2026-10-15; no experiment run.

## Recommendation and current evidence

Pursue a **finite-population certificate for accumulation hidden by fixed downstream support, wholly inside the radial core at all four receiver rotors**. Combine proof, tiny deterministic fixtures, and existing genuine local3D replay. This is a candidate methods note, not demonstrated novelty or a physical prediction.

Reject “compute only below physical uncertainty”: error balancing is established, and no calibrated physical-error bound exists here.

[PUBLIC-SUPPORT-FACTORIAL-20261015](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/23fec0a263fe3cec939417fdebc8525dbc8e2204/research/campaign-public-support-factorial) rescored 401 fixed endpoints of one 16-vehicle genuine local3D trajectory. Radial-taper removal changed predicted thrust by at most 1.9686% of weight. No far-field pair reached the 2 m axial fade, so zero axial sensitivity reflects missing exposure. Over one quarter of added inflow came from xi>5. The 1.969% sensitivity cannot become physical uncertainty.

Prior weak pruning bounded finite-support omissions over 4,848 snapshots/1,330,776 receiver comparisons but failed all 36 speed gates. Support-expansion examples and receiver Lipschitz bounds already exist. The unconverged temporal reference blocks dynamical-performance claims.

## Closest verified primary work

- [Braack and Ern (2003)](https://epubs.siam.org/doi/pdf/10.1137/S1540345902410482), *A Posteriori Control of Modeling Errors and Discretization Errors*, MMS 1(2), 221–238, DOI 10.1137/S1540345902410482: goal-oriented model/mesh adaptation already balances error components against a mathematical reference.
- [Farrell-Maupin and Oden (2017)](https://link.springer.com/article/10.1186/s40687-017-0104-2), RMS 4, 14, DOI 10.1186/s40687-017-0104-2: OPAL selects simpler models subject to quantity-of-interest validation under uncertainty. Ranking does not establish adequacy; reference observations are needed.
- [Gielis, Shankar, Kortvelesy and Prorok, v1 (2023), Sections 2–6](https://arxiv.org/html/2312.03488v1), final ISER chapter (2024), DOI 10.1007/978-3-031-63596-0_35: measured nonlinear force aggregation and learned set models already address multi-source downwash. Pairwise-force summation differs from this code's velocity sum followed by nonlinear rotor response.
- [Zong and Porté-Agel (2020)](https://doi.org/10.1017/jfm.2020.77), JFM 889, A8: momentum-conserving superposition compared with PIV/LES; publisher abstract/metadata verified, full derivation inaccessible. [Blondel (2023), Sections 1–3](https://wes.copernicus.org/articles/8/141/2023/), WES 8, 141–147, DOI 10.5194/wes-8-141-2023, read beyond the abstract: Eq. (1) has wake-overlap cross terms, extending momentum-based superposition to super-Gaussian profiles. These ambient-flow velocity deficits cannot simply replace hovering jets.
- [Lai and Lee (2012)](https://doi.org/10.1017/jfm.2012.332), JFM 708, 539–575: publisher abstract verifies entrainment/pressure-mediated interactions, merging, and momentum/energy superposition; full text unread. Failure of independent-jet assumptions is already known.
- [Bauersfeld et al., v3 (2024), III–VI](https://arxiv.org/html/2403.13321v3), final RA-L 10(2), 1241–1248 (2025), DOI 10.1109/LRA.2024.3518835: single-hover-vehicle profile; xi>2 tail overprediction motivates the core-only test. It does not validate arbitrary axial extent, 27 g extrapolation, or source independence.

Candidate increment: **rotor-aware finite-N support-error bounds connected to extent scaling**. This search establishes no novelty guarantee; an obvious toy theorem may be too small for a full paper.

## Analytic claim to prove before implementation

Use immutable public wake.cjs/aero.cjs at commit 1336f5c416875a9651f92b58b2ed06649f25b04e, upright equal-hover sources/receiver, and rotor offsets (±a,±a,0), a=0.028 m. Let r0=sqrt(2)a, D=2r0, s=5.817D, k=0.07668, A=10.11D*vi, c=sqrt(2)-1. The formal untapered scalar term is

u(d,r) = A/(d+s) / [1+c(r/(k(d+s)))^2]^2,   b(d)=k(d+s).

At d>=0.5 m, source centers occupy radius R(d)=2b(d)-r0 above the receiver center. Every rotor/source radial distance is <=R+r0=2b: radial weights and projections equal one; no near-field guard is entered. Arbitrarily tilted swarms do not inherit this certificate. A source vehicle is one merged far-field jet, not four source-rotor jets.

Let n_j be the exact number of sources in layer d_j, fz the original 2–2.5 m axial fade, and

B(L)=sum_{d_j<=L} n_j*(1-fz(d_j))/(d_j+s),   f2=[1+4c]^-2.

For EACH receiver rotor, the support omission obeys the finite, explicit bounds

A*f2*B(L) <= U_X(L)-U_P(L) <= A*B(L).

P retains original support; X removes only axial support. This bounds omission relative to X, not physical error. Existing weak-pruning guarantees against P remain valid.

For a continuum source density eta, the centered-disk integral is

F(d,R)=pi*A*k^2*(d+s)/c * [1-(1+c*(R/b)^2)^-1].

At each actual rotor, disk inclusion brackets the layer integral between F(d,2b-2r0) and F(d,2b). Their difference is O(1); both have a positive leading term proportional to d. Thus U_X=C*L^2+O(L), with C=eta*pi*A*k^2*[1-(1+4c)^-1]/(2c), while N=4*eta*pi*k^2*L^3/3+O(L^2). The formal growth is therefore Theta(N^(2/3)); P saturates beyond 2.5 m.

For a fixed-spacing square lattice, disk cell inclusion gives pi*max(R-h,0)^2 <= n_j*delta^2 <= pi*(R+h)^2, h=delta/sqrt(2). Combined with the rotor bound, this gives the same growth order without fitting a slope. Growing pointwise inflow alone does not prove momentum violation: total source forcing also grows. This is stipulated independent-source scaling, not actual merged flow.

## Minimum decisive experiment, after separate approval

One deterministic single-receiver test, two arms P/X:

1. delta=0.25 m; heights d_j=0.5+j*delta; nested extents L={2,4,8} m. Keep centers x^2+y^2<=R(d_j)^2. Two horizontal phases, (0,0) and (delta/2,delta/2), expose grid registration. All quaternions are identity. Stable height/y/x ordering preserves prefixes. Static fixtures are not Boids flight.
2. Evaluate only four receiver rotors with the immutable normalized wake function and checked fades; no all-receiver A.fields. Preflight cap: 4,096 sources/fixture, six fixtures, <=196,608 source/rotor/arm evaluations. Stop on cap/domain failure. No Monte Carlo, flight integration, source-source iteration, or tuning.
3. Retain layer counts, coordinate hashes, P/X inflows, B/bounds, omission fractions, and largest single-source term. Require all-rotor finite bounds within 1e-12*max(1,abs(bound),abs(inflow)) m/s, xi<=2+1e-12, d>=0.5 m, P(4)=P(8) bitwise, X(8)>X(4)>X(2), and positive omitted-core lower bounds at 4/8 m. These are mathematical checks, not physical acceptance limits. A failure stops the attempt for diagnosis, without outcome-driven retuning.
4. Reuse the existing 401-row genuine local3D replay as the application anchor, explicitly reporting no axial exposure. No replay rerun or changed-flight claim. Report finite ratios/bounds; three extents cannot establish an empirical asymptotic exponent.

One supervised attempt: 60 s wall, <=100 KB outputs, <=20 KB source/proof. No execution authorized here.

## Publication gate and blockers

Prove all-rotor bounds and expose extent-dependent omissions. If this only repeats stack/ring examples or an existing certificate, retain benchmark documentation without a novelty claim.

Core-only does not mean empirically supported at 8 m. Source coupling, entrainment changes, room boundaries, wake age and actuator response are omitted. The independent single-source screen underway cannot validate aggregate scaling. Physical large-swarm claims need multi-source measurements or a justified coupled-flow reference, neither supplied. Flight-performance claims also need the genuine Boids implementation and a qualified temporal reference. Private R8 remains inaccessible.
