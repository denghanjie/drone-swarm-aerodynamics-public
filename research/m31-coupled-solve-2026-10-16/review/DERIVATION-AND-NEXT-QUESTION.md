# Static feasibility of vertical ordering for assumed thrust-scaled coupling

This is an analytical inspection only. No model code, dataset evaluation, random states, fitting, or numerical experiment was run. The public repository was not modified. A thrust-responsive source is a later explicit assumption: the inspected `pairTerm` still uses the fixed `c.induced` and does not read source motor thrust.

**Conclusion.** The current positive downstream support admits a conservative vertical-order guarantee when every axis is unit length, the rotor geometry is consistent with that axis, and every tilt from upward vertical is at most 45 degrees. Bounded tilt without a sufficiently small stated bound does not guarantee acyclicity: the symbolic six-vehicle construction below has a positive directed cycle at tilt `arctan(3) < 90 degrees`. The near-field rejection predicate can be mutual even at arbitrarily small nonzero tilt; it is not an admitted positive wake contribution.

## Exact inspected support and required geometry assumptions

Sources inspected:

- `research/m31-source-accounting-2026-10-16/source/reference-excerpt.cjs`, exact `pairTerm` and `fade`.
- `research/m31-source-accounting-2026-10-16/source/witness.cjs`, constants and four rotor offsets.
- `research/m31-source-contract-planning-2026-10-16/EVIDENCE-AND-NEXT-TEST.md`, distinction between effective thrust, nominal command, RPM, ideal power, and future implicit coupling.

Let `q_j` be source center, `q_i` receiver center, `a_j` source axis, and `r_ir` the receiver rotor offset. The code uses

`d = q_j - (q_i + r_ir)`, `h = d dot a_j`, and `rho_perp = ||d - h a_j||`.

It does not evaluate downwash at the receiver center. The receiver projection is `max(0, a_i dot a_j)`.

Write `R = sqrt(2) arm`, where `arm = 0.028`; this is the center-to-rotor-center distance, not the propeller radius `0.023`. The inspected constants give

`D = 2R`, `m = minDown D = 5R`, `b = -origin D = 11.634R`,

`kappa = radCut spread = 3(0.07668) = 0.23004`.

An admitted positive term requires center distance below 3, `m <= h < 2.5`, `rho_perp < kappa(h+b)`, positive receiver projection, finite admitted speed, and the other input guards. Fade factors are positive strictly inside their cutoffs. At `0 < h < m`, `rho_perp < 0.15` returns symbol 4/stage 4 with no valid positive field; outside that radius it returns symbol 5/zero. The near branch must not be silently filled with an invented wake law.

For the theorem, explicitly assume `||a_i||=1`, `a_i dot zhat >= cos(theta) > 0`, and rotor offsets obtained by rotating the inspected square with the vehicle, so `r_ir dot a_i=0` and `||r_ir||=R`. Consequently `|r_ir dot zhat| <= R sin(theta)`. The excerpt itself does not enforce normalization or consistency between axes and offsets. The witness establishes only its level, horizontal-offset instance; arbitrary-attitude invariants need a separate contract.

## Sufficient downstream ordering condition

For a potential positive edge `j -> i`, decompose `d = h a_j + v`, with `v` perpendicular to `a_j` and `||v||=rho_perp`. The source-minus-receiver **center** height is

`Delta_z = (q_j-q_i) dot zhat = h(a_j dot zhat) + v dot zhat + r_ir dot zhat`.

Thus

`Delta_z >= h cos(theta) - rho_perp sin(theta) - R sin(theta)`.

Use the downstream radial support and `h >= m`. A sufficient condition, which also makes the coefficient of `h` positive, is

`m cos(theta) > [kappa(m+b) + R] sin(theta)`.

Equivalently,

`tan(theta) < 5 / [1 + 0.23004(5+11.634)] = 5 / 4.82648536`.

Under that condition, every positive edge has strictly positive center height drop, with conservative lower margin

`R [5 cos(theta) - 4.82648536 sin(theta)]`.

In particular `theta <= 45 degrees` is sufficient because `5 > 4.82648536`. At zero tilt the direct identity gives `Delta_z=h>=m>0`. The down cutoff, neighbor cutoff, and projection gate can remove edges and cannot invalidate the ordering proof. The condition is sufficient, not claimed necessary or sharp.

A directed cycle would require a sum of strictly positive center height drops around a closed loop, but that sum telescopes to zero. Therefore the positive-support graph is a DAG. If a future scalar source amplitude depends on effective thrust and leaves this support fixed, the same geometric DAG permits evaluation in descending center height, provided each receiver's local closure is itself well-defined. This proves neither that closure's physical validity nor its scalar existence or uniqueness.

If only `||r_ir||<=R` is guaranteed, without rotor-plane consistency, replace the offset term by `R`: the conservative condition becomes `5 cos(theta) - 3.82648536 sin(theta) > 1`. The 45-degree guarantee above must not be used under that weaker contract.

## Symbolic positive downstream cycle under a broader bounded tilt

Use six centers forming a horizontal regular hexagon of side length `L=2 sqrt(10) R`, all at the same height. Index cyclically. Define

`t_k = (q_k-q_(k-1))/L`,

`a_k = (3/sqrt(10)) t_k + (1/sqrt(10)) zhat`.

Every axis is unit length and has the same bounded tilt `arctan(3)`. Choose any square rotor frame perpendicular to its axis, with the inspected offsets of norm `R`. For source `k` and every rotor of receiver `k-1`,

`d = L t_k - r_(k-1),r`,

`h = 6R - r_(k-1),r dot a_k`, hence `5R <= h <= 7R`.

The perpendicular part obeys

`rho_perp <= L/sqrt(10) + R = 3R`.

But the downstream radial cutoff is at least

`kappa(m+b) = 3.82648536R > 3R`.

Adjacent axes have positive receiver projection:

`a_(k-1) dot a_k = 1/10 + (9/10) cos(60 degrees) = 11/20`.

Also `L<3`, `7R<2<2.5`, and all coordinates and derived quantities are far inside the excerpt's finite-magnitude guards. Both fades are positive. The term cap does not remove these edges: from the inspected constants, `c.induced<6` and `decay/(h/D-origin) <= 10.11/8.317 < 2`; the remaining multiplicative factors are at most one, so speed is below 12, hence below 128.

Therefore all six edges `k -> k-1` are admitted positive downstream terms, including all four receiver rotors. They form a directed cycle at equal center height. Other edges need not be absent: additional edges cannot remove this cycle. The dependency cycle persists under a later positive amplitude scaling that leaves geometry/support and admission status unchanged; scaling beyond the speed cap would instead require handling a rejection. This is a symbolic computational construction, not a physical flight configuration or a novelty claim.

## Why the near branch needs a separate admission rule

For any `0 < epsilon < 45 degrees`, put centers `q_A=(0,0,0)` and `q_B=(R,0,0)`, with axes

`a_A=(-sin(epsilon),0,cos(epsilon))`,

`a_B=(sin(epsilon),0,cos(epsilon))`.

Choose one permitted corner rotor offset on each receiver:

`r_A=(-R cos(epsilon),0,-R sin(epsilon))`,

`r_B=(R cos(epsilon),0,-R sin(epsilon))`.

Each offset has norm `R` and is perpendicular to its own axis. In both directed evaluations,

`h = R sin(epsilon) [1+2 cos(epsilon)]`, so `0<h<3R<5R=m`,

`rho_perp = R [cos(epsilon)+cos(2epsilon)] <= 2R < 0.15`.

Both evaluations therefore hit symbol 4. This is mutual **rejection geometry**, not a positive two-cycle in the admitted field. It shows why the downstream DAG theorem does not authorize treating near pairs as valid or filling that branch without renewed graph analysis. An operational acyclic solve needs both the downstream geometry conditions and a declared response to near-field rejection. At exactly zero tilt, positive down still implies higher source center.

## One next finite numerical question — proposed only

On the **single six-vehicle hexagon above**, can a frozen simultaneous solver satisfy all six equations of an explicitly assumed effective-thrust-scaled receiver/source contract within a declared residual and iteration budget, with that residual checked by an independent implementation?

For a concrete prospective contract, freeze geometry and the current wake shape/support, scale each source by `sqrt(T_j/(mg))`, define each vehicle's scalar inflow as the arithmetic mean of its four summed rotor inflows, and use total effective thrust with `A_total=4 pi radius^2` in the existing ideal-power closure:

`P_i = T_i [U_i/2 + sqrt(U_i^2/4 + T_i/(2 rho A_total))]`,

with a declared equal baseline `P_i = mg sqrt(mg/(2 rho A_total))`.

These source scaling, spatial averaging, total-disk, and ideal-power choices are new mathematical assumptions, not an identified fixed-command or shaft-power contract. A future allocation would need to lock the admissible domain, reject any unsupported near pairs, and predeclare method, initialization, stopping criterion, residual scaling, iteration and CPU limits, and evidence format before execution. Six unknown thrusts and at most 120 distinct non-self rotor-pair coefficients are sufficient for this one geometry; freezing coefficients is legitimate only while assumed shape/support stay thrust-independent. A solution would demonstrate simultaneous numerical consistency for this assumption set, not uniqueness, physical validity, stability, or a vehicle claim. This note allocates and executes no experiment.
