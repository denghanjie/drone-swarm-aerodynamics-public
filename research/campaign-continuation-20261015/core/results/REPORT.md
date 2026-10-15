# Core-only extent certificate: cutoff saturation and growing formal inflow

Experiment: **CORE-EXTENT-CERTIFICATE-20261015**. One supervised attempt completed on 2026-10-15 UTC. This report reads the saved results only; no model was rerun.

## Main result

All four receiver rotors satisfied the prospective finite support-omission bounds in all six fixtures. Extending the source population from 4 to 8 m left the original finite-support prediction P **bit-for-bit unchanged**, while the axially extended prediction X grew by factors of **3.56 and 3.83** in the two lattice phases.

At 8 m, the formal X sum reached **203.76 and 197.31 m/s**, approximately **50.53 and 48.93 times the single-vehicle hover-induced speed vi**. P omitted **90.27% and 92.73% of X**, respectively. These huge numbers are conditional sums of independent jets, not measurements or credible flight predictions. They illustrate why a small computational error against a truncated reference cannot establish physical accuracy.

## What ran

Six nested static source fixtures use 0.25 m lattice spacing, maximum heights 2/4/8 m, and horizontal phases (0,0)/(0.125,0.125) m. Every source and the receiver are upright. One receiver at the origin is evaluated at its four actual rotor positions. Source centers are restricted to radius R(d)=2b(d)-r0 so that every rotor/source pair remains inside the code's radial core, xi<=2.

P retains original axial and radial support. X removes only axial support. Every radial weight was exactly one, so the contrast has no radial-taper contribution. The original 2–2.5 m axial fade is the only changed modeling assumption.

There was no source-source coupling, receiver thrust law, flight integration, optimization, or Boids controller execution. These deliberately constructed populations are not flock trajectories. The genuine local3D Boids replay from PUBLIC-SUPPORT-FACTORIAL-20261015 remains a separate unchanged anchor; it had no axial-cutoff exposure.

## Finite observed values

Values below use rotor 0; symmetry makes the other three agree to floating-point roundoff. These are not independent replicates. vi=4.032743274 m/s. The omitted fraction uses X as denominator, not observed airflow.

| Horizontal phase (m) | Extent (m) | Sources | P (m/s) | X (m/s) | X/vi | (X-P)/X |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 19 | 17.8107 | 17.8107 | 4.4165 | 0% |
| 0 | 4 | 131 | 19.8194 | 57.2515 | 14.1967 | 65.3818% |
| 0 | 8 | 911 | 19.8194 | 203.7642 | 50.5274 | 90.2733% |
| 0.125 | 2 | 20 | 12.9399 | 12.9399 | 3.2087 | 0% |
| 0.125 | 4 | 128 | 14.3403 | 51.4886 | 12.7676 | 72.1486% |
| 0.125 | 8 | 900 | 14.3403 | 197.3104 | 48.9271 | 92.7321% |

The 4-to-8 m extension adds 780 sources and 146.5127 m/s in phase 0, or 772 sources and 145.8218 m/s in phase 0.125. Stable coordinate prefixes ensure this is the contribution of added sources, with existing source geometry unchanged. P sees none of these additions because all lie beyond its cutoff.

Even P is 3.56–4.91 vi at the larger extents. Saturation is therefore a property of its imposed support, not evidence that its absolute predictions are physically adequate.

## What the certificate establishes

For A=10.11Dvi, c=sqrt(2)-1 and s=5.817D, the core term is

u=A/(d+s)/[1+c*xi^2]^2.

Since 0<=xi<=2, its radial factor lies between f2=(1+4c)^-2 and 1. Let n_j be the saved exact source count in layer j and fz its original axial fade. Define B=sum_j n_j*(1-fz)/(d_j+s). The all-four-rotor finite bound is

**A*f2*B <= X-P <= A*B.**

| Phase (m) | Extent (m) | Lower bound (m/s) | Actual X-P (m/s) | Upper bound (m/s) |
|---|---:|---:|---:|---:|
| 0 | 4 | 13.0843 | 37.4321 | 92.3606 |
| 0 | 8 | 65.5558 | 183.9448 | 462.7502 |
| 0.125 | 4 | 13.0136 | 37.1483 | 91.8616 |
| 0.125 | 8 | 64.8613 | 182.9701 | 457.8475 |

Both bounds and the omission are zero at 2 m. The bounds are intentionally conservative, not uncertainty intervals. They establish an explicit positive model-relative omission for each finite population without assuming that an asymptotic regime has been reached.

The largest individually omitted contribution is 1.063618 m/s for phase 0 (source center (0,0,2.5), rotor 0), or 0.822878 m/s for phase 0.125 (source center (0.125,0.125,2.5), rotor 0). Aggregate omission is much larger than either term. These are not uniformly weak terms under the earlier pruning study's thresholds; that prior study's guarantees against P remain unchanged.

## Integrity and coverage

- All 6 fixtures and 24 rotor outputs completed: 8,436 source/rotor visits, 16,872 arm slots.
- Maximum observed xi was 1.9899222, with all 8,436 radial weights exactly one. The phase-0 minimum downstream distance was 0.5 m; phase 0.125's first populated layer was 1 m.
- All finite speed/count bounds, input hashes, source-file hashes, coordinate-prefix checks and P plateau identities passed.
- Largest closed-form/imported-kernel discrepancy: 4.441e-16 m/s. Largest direct-omission/arm-difference residual: 1.421e-13 m/s, within the prospective scaled tolerance.
- The conservative P source-center support envelope was 2.630711 m, inside the original 3 m search radius.
- Postresult analysis rechecked all six fixture-record SHA256 hashes listed in summary.json. The original coordinate hashes and exact layer counts remain in those records; no coordinate regeneration was needed for this report.

The outer supervisor recorded exit 0, no timeout, 0.119238 s wall time and 45,113 bytes of original outputs. This is one completion receipt, not a speed benchmark. The report is a later analysis artifact and is not included in that original output-byte figure.

## Interpretation and next decision

The independently reviewed proof gives formal Theta(N^(2/3)) growth for the stipulated fixed-density expanding cone, whereas fixed axial support saturates. The run tests finite bounds and extent ratios; three extents do not estimate or empirically confirm an asymptotic exponent or its coefficient.

This adds a rotor-aware finite certificate and a controlled extent comparison beyond earlier isolated stack/ring examples. It shows that growing omissions can arise entirely within the code's untapered radial region. It does not establish a novel general theorem, a better aerodynamic model, or a reason to enlarge the cutoff in production.

Physical interpretation remains blocked by independent-source assumptions, unmodeled jet interaction and entrainment, wake age, boundaries, and unvalidated axial extent. “Core” is a software-support label, not an empirical accuracy guarantee; the newer small-quadrotor preprint also reports departures from the analytic profile within that region. See the [publication-path assessment](../../literature/ASSESSMENT.md) and [2026 preprint addendum](../../literature/UPDATE-2026-PREPRINT.md).

The next useful publication decision is whether this narrow certificate fills a demonstrable prior-work gap. Further enlarged-population runs would not resolve the main physical uncertainty. A physical claim instead needs an independently justified multi-source reference; a changed-flight claim additionally needs a qualified temporal reference and the genuine Boids implementation.
