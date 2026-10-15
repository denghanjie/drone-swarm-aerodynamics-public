# Proposed bounded source-omission challenge

Date: 2026-10-16. Status: **static design only**. No geometry, field, receiver root, generated case, perturbation, benchmark, or integration was evaluated while preparing this proposal. The completed static reference remains immutable; this proposal is a separate campaign requiring selection, implementation, independent critique, freeze and launch authorization under the existing research procedure.

## Decision and falsifiable question

Test one deterministic source-omission algorithm against the unchanged M28 four-receiving-rotor field: can a cheap source-level upper bound safely omit weak contributions under declared body-thrust and roll/pitch error budgets, and does the complete implementation cost less after paying for its bounds, domain safeguards and selection?

Unlike broadcasting a center sample to all motors, retained sources still receive all four rotor evaluations. Unequal rotor loads and their roll/pitch moments are retained. Omission remains an approximation: its moments need not equal the reference, and their bounds must be checked. Do not assume novelty or speed. A correct algorithm that omits nothing or runs slower is a valid negative result.

Use the closed twelve-pose reference only after its independent saved-data review has passed. Its source freeze is89c3b14; pin the full commit, result/schema/data hashes and published review at the new freeze. Those12poses are **exposed development diagnostics**, not confirmation. Do not modify or resume that campaign, infer historical motor inputs, or qualify a full flight from a static result.

## One real-arithmetic source bound

Notation for receiver i and source j: c=p_j−p_i; source axis n_j; receiver body-to-world map R_i; receiving rotor offsets v_k=R_i*r_k; a=0.028m; rotor radial arm l=sqrt(2)*a; f0=mg/4; D=2*sqrt(2)*a. Preserve exact stored quaternions and the original unnormalized rotation algebra.

**Do not silently assume exactly unit axes or exactly orthogonal rotations.** Compute l_i=max_k||v_k|| from the actual four precomputed offsets, s_j=||n_j|| and b_j=max(1,|1−s_j²|). For the source radial projection P_j=I−n_j*n_j^T, b_j is its Euclidean operator norm. These quantities reduce to l,1,1 for ideal unit quaternions. Precomputation belongs in the timed algorithm and in the matched baseline; it is shared across sources, not imported from reference outputs.

At the receiver center define d0=c·n_j and r0=||c−d0*n_j||. Every receiving rotor satisfies

`d− = d0−s_j*l_i <= d_k <= d0+s_j*l_i = d+`

`r_k >= r− = max(0, r0−b_j*l_i)`.

This follows from Cauchy–Schwarz and the reverse triangle inequality applied to P_j*v_k. The simpler ±l and r0−l bounds are justified only for exact unit/orthogonal geometry. The receiving-axis projection c_ij=max(0,n_i·n_j) is common to its four source terms; use the actual value and do not clamp it to1.

The unchanged far-field contribution is

`w(d,r)=c_ij * vi0 * [10.11/(d/D+5.817)] * F(d) * Q(r/H(d))`,

where vi0=sqrt(f0/(2*rho*A)), H(d)=0.07668*(d+5.817D), F is the existing downstream fade, and `Q(q)=radialFade(q)/[1+(sqrt(2)−1)*q²]²`. On the far domain, the decay factor and F are nonincreasing in d, H is increasing, and Q is nonincreasing in q>=0. The complete wake need not be monotone in d; do not assume that.

After resolving the domain rules below, intersect the downstream interval with the retained far range:

`dL=max(d−,2.5D)`; `dH=min(d+,2.5m)`; `qL=r−/H(dH)`.

When this far interval is nonempty, a common upper bound for all four rotor contributions is

`B_ij=c_ij * vi0 * [10.11/(dL/D+5.817)] * F(dL) * Q(qL)`.

Each monotone factor is bounded separately. Their extrema need not occur at one physical rotor; this makes the bound conservative but potentially loose. A source's four individual terms may all be tiny while B_ij is large. The candidate must report this limitation rather than tune after seeing it.

## Domain fidelity before omission

Keep the exact strict3m source-center selection and global20° axis tilt gate. An omitted source is only omitted for a particular receiving vehicle; it is not removed from the flock or other receivers.

Apply the original branch order conservatively:

1. If d+<=0 or d−>=2.5m, all rotor contributions are exactly zero and the source can be culled.
2. If the interval can enter the open near slab, meaning d+>0 and d−<2.5D, and r−<0.15m, the bound cannot exclude a near-wake exception. **Fall back to exact geometry for all four rotors and retain this source for exact field evaluation.** If any exact rotor is invalid, reject the input as the original model does. Do not bypass this check because the estimated wake or projection is small.
3. If near-slab ambiguity has been resolved safely and d+<2.5D, no far rotor exists and all contributions are zero under the existing near-skip policy. Equality at2.5D is not a zero-cull condition.
4. On a nonempty far interval, qL>=3 implies exact radial-support zero. Zero projection is usable only after the domain obligation is resolved. Otherwise use B_ij above.

The fallback must not silently continue an invalid source. Preserve the original error type and declared domain decision. If first-offender identity is claimed identical, collect ambiguous invalid tuples and select original receiver/rotor/source traversal order before reporting; a source-first fallback traversal alone need not encounter the same first tuple. Simpler acceptable scope is domain-reject equivalence with explicit witness identities, without claiming instruction-exact exception order.

Old saved domain pass flags must not disable these guards: fresh inputs need them, and domain information from a full reference pass is not free input to the approximation.

## Load budget and deterministic selection

For equal prescribed nominal thrust f0, the positive receiver root obeys x³+alpha*x−1=0, alpha=U/vi0. Its derivative is

`dx/dalpha=−x/(3*x²+alpha)` and `|df/dU|<=L=f0/(3*vi0)`.

Let the omitted inflow at rotor k be E_k>=0, and let B_i=sum of B_ij over omitted positive-bound sources. Then E_k<=B_i. In real arithmetic, removing nonnegative inflow increases effective rotor thrust:

`0<=delta_f[k]=f_approx[k]−f_full[k]<=L*B_i`.

Consequently

`0<=delta_T<=4*L*B_i`,

`|delta_tauX|<=2*a*L*B_i`, `|delta_tauY|<=2*a*L*B_i`.

The factor2a, rather than4a, uses the two positive and two negative rotor lever signs together with one-sided thrust errors. Do not assume further cancellation or identical rotor errors. Nominal yaw remains0. World-force error is delta_T times the receiver axis; for nonunit numerical axes its Euclidean norm is bounded by ||n_i||*delta_T. World-moment bounds require the actual rotation-map norm or component interval propagation. Primary acceptance should remain in declared body thrust/roll/pitch units; report world errors separately.

Proposed fixed targets for this one challenge: epsilonT=0.005mg and epsilonX=epsilonY=0.0005mgD. These are analyst-chosen numerical fidelity budgets, with a tighter moment target so moment preservation is not vacuous under the thrust budget. They have no physical/safety interpretation and are not fitted from the12poses. The parent may choose different values **before implementation freeze**, but do not sweep/select budgets after results.

The common omission capacity is

`Bcap_i=min(epsilonT/(4L), epsilonX/(2aL), epsilonY/(2aL))`,

reduced prospectively for the numerical allowances below. Traverse eligible sources in ascending ID. Cull proven zeros; retain domain-ambiguous sources; for every remaining source, omit it only when adding its inflated bound preserves B_i<=Bcap_i, otherwise retain and evaluate all four rotors. No sorting, threshold fitting, reference-informed ranking, or reuse of an old omission mask in this first candidate. Retained term accumulation stays in ascending source order for each rotor.

This greedy ordering is deliberately simple and may spend the budget poorly. A later sorted or per-rotor-bound algorithm would be a separately frozen candidate, not an unreported rescue. A nonuniform source-bound vector could tighten moment budgets further, but that is outside this candidate.

## Floating-point status and gates

The inequalities above are real-arithmetic proofs. Ordinary binary64 center geometry, square roots, fades and accumulated bounds do not automatically constitute outward-rounded intervals. Choose and freeze explicit numerical margins before exposure; a reasonable initial engineering contract is1e-12m expansion of down/radial bounds,1e-12 relative plus1e-12m/s inflation of every positive source bound, upward accumulation of positive bounds using a reviewed nextUp addition, and1e-12N reserved per rotor for response arithmetic. Account these allowances in Bcap and the total/moment bound, rather than hiding them in a postrun tolerance.

These proposed margins require independent source scrutiny and adversarial testing; they are **not a proved universal rounding certificate**. A formal conservative floating-point claim would require verified enclosures for every geometry/transcendental/rounding step and receiver evaluation, which this proposal does not supply. Use “analytical omission bound with a frozen numerical allowance, checked on the specified cases.”

Before timing, require on all valid cases: original/reference domain agreement; finite nonnegative fields; independent full-reference agreement at the established precision gates; exact zero for every claimed exact-zero contribution; each independently checked omitted source's four terms <= its stored bound plus the frozen check allowance; summed omitted inflow and actual load errors within retained per-receiver bounds; and actual approximation errors within all three declared budgets. Record violations even when the final total load happens to meet budget. One bound violation fails the candidate's bound claim. No tolerance increase, different sum selection, fallback rewrite, or new run is allowed after exposure.

Keep solver residual/power/bracket checks from the qualified static reference. The implemented Newton response is not proved monotone for all floating inputs merely because the exact cubic is monotone. Directly check the expected error sign within the declared numerical allowance and retain any exception.

## Frozen cases: exposed diagnostics and separate fresh confirmation

Use the12existing poses only as candidate evaluations against their already saved, hash-verified full fields/loads. No additional full-field baseline evaluation is needed for those correctness comparisons. Their outcomes are diagnostic, not fresh confirmation.

Add exactly two newly generated static confirmation configurations: N=1000 on a10×10×10 lattice, and N=5000 on a20×25×10 lattice, spacing(0.30,0.30,0.50)m. Use a frozen, documented integer PRNG with independently fixed seeds before any case evaluation; jitter each position component within±0.02m, yaw over a full turn, roll and pitch within±8°. The generator and seed values must be reviewed/frozen before generating or viewing poses. Save its complete exact Float64 output and provenance. Do not regenerate a case that fails domain or yields few omissions. These are fresh synthetic configurations, not a random sample of real swarms or fresh integrated flights. Lattice regularity is a limitation; the second count is a scale check, not a second physical distribution.

Separately freeze16small adversarial fixtures, each with at most5vehicles. Fixtures are implementation challenges, not confirmation samples. Allocate them prospectively across: strict3m center boundary; down=0; down=2.5D; down=2.5m; near radius0.15m; radial support3H; both fade transitions; nonzero combined tilt/yaw; slight permitted quaternion norm defects; multiple weak sources whose sum exhausts the budget; opposite-sign moment lever patterns; and just-below/just-above budget acceptance. Include expected domain-rejection fixtures. Values at a boundary and one representable neighbor on each side may be packaged within a fixture, but freeze the exact total subcase/call count before implementation; the resource ceiling below assumes16actual field-input cases, not16unbounded families.

At least one fixture must make a center-only domain inference fail for a rotor, one must make the independent-factor bound loose, and one must challenge many small omitted terms summing near the capacity. Do not use the full reference to select which fixture variant “works.” Symbolic/analytic construction and explicit expected decisions should precede evaluation. Boundary success is finite coverage, not proof for every possible pose.

## Competing explanations and fair cost study

Report whether improvement or failure is explained by the observed mechanism: many exact-zero culls; genuinely small positive omissions; too-loose independent-factor bounds; near-domain fallbacks; a tight moment budget; weak original interactions; data layout/precomputation changes; or bound overhead exceeding saved wake work. Record eligible sources, exact-zero culls, positive omissions, retained sources, fallback counts, bound evaluations, actual rotor/profile evaluations, and used budget separately.

Time three implementations on only the two fresh confirmation configurations, after all correctness gates pass:

- **B:** unchanged M28 full field, receiver law and load assembly.
- **M:** the candidate's preprocessing/traversal/load code with all sources retained and bound computation disabled; require full-output agreement with B. This isolates benefits caused by restructuring/precomputation.
- **C:** the actual bounded-omission candidate, including all bound and fallback work.

One warmup and five recorded paired passes per configuration; freeze a rotated/reversed three-method order before launch. Technical repeats are not independent swarms or confidence intervals. Report median and min/max complete query time, with C/B and C/M ratios and actual error/omission counts. A speed benefit against B alone does not establish that omission rather than restructuring helped.

The timed query begins with the same17-state input arrays and includes axes/rotors, grid and neighbor construction, bound preprocessing, every bound/zero/domain decision, omitted-mask construction, retained four-rotor field work, accumulation, receiver roots, body/world loads and output checksum. Do not reuse masks, fields, rotor geometry or neighbor lists computed during verification. Input file decoding/generation, independent oracle checking, persistence and rendering are outside all three timers and separately recorded. All timing outputs must reproduce the corresponding retained correctness result under the declared comparator. No browser, GPU, flight controller, dynamics, obstacle checking or end-to-end simulation speed claim follows.

## Proposed one-shot work and storage ceilings

Before launch, resolve the16fixture inputs and exact call table. With the matrix above, a conservative ceiling is120field-query invocations:12C calls on exposed poses;4implementations(B,M,C,independent full)×18fresh/fixture inputs; and3methods×6passes×2fresh configurations. Expected invalid fixtures may return early, but attempts still count.

Only the new full independent reference scans every nonself source on the two fresh cases and fixtures: `1000*999+5000*4999=25,994,000` checks, plus at most320fixture checks. Cap this at26,000,000. C makes at most289,930,320source-bound attempts across correctness/warmup/timing by the all-pairs shape bound; use290,000,000 as its cap. A conservative combined four-rotor visit ceiling for the proposed calls is2,719,365,120; use2,750,000,000. Grid's own cell/candidate work is additional and included in wall time, not mislabeled as direct-loop checks. The receiver-call ceiling is641,280; use650,000, including shortcuts. No integrations.

Suggest300executable seconds total and128MiB new raw evidence with4MiB reserved for failure. These are caps, not estimates of expected work or completion. Use the established one-shot lock, attempted-call accounting, cooperative guards and external process-group watchdog; no retries or extension. No memory acceptance limit or timing-only escape from failed correctness. Stop new launches at the existing07:00Asia/Shanghai2026-10-16 deadline.

Retain every valid vehicle's reference/candidate/M outputs as applicable, per-receiver B and predicted signed load bounds, actual errors, work counters, and the selected source classifications. A compact two-bit/source mask over the14main configurations has33,500,000uncompressed bytes by fixed shapes. Store positive-omission B_ij values in mask order, and on fresh/fixture cases store the four independently evaluated omitted-source terms needed to audit each bound. Exact-zero classes need no repeated zero doubles. Include full generated poses, timings/checksums, schema, hashes, every failed witness and completed prefixes. If complete required evidence exceeds128MiB, stop and report the cap; do not drop terms, choose a different compression-dependent scientific subset, or relaunch. Do not promise the cap will suffice before the static byte plan is finalized.

A separately bounded saved-data review can check masks/counts, sum stored positive bounds, reconstruct signed force/moment budgets, inspect per-source inequalities where retained, verify aggregate errors and timing statistics, and reconcile all hashes without geometry, fields, roots or benchmarking. For exposed poses, the old reference provides resultant fields/loads rather than every source term; clearly distinguish aggregate agreement there from the fresh same-pass per-source bound checks. No claim of a recoverable per-source proof should exceed the stored evidence.

## Permitted conclusion and next decision

Accept this candidate only if the domain/implementation/bound gates and numerical budgets pass on every required valid input, expected invalid inputs reject correctly, and all prescribed work completes. Report cost separately: a correct but slower candidate remains a useful negative result. A single budget setting and two fresh synthetic configurations do not establish a generally optimal method or a swarm population guarantee.

The underlying27g free-air mean-wake model, prescribed hover strength despite tilt/inflow, linear positive superposition, constant ideal-induced-power receiver law, rotor-point sampling, nominal-yaw retention, finite support, near-field policy and absent wall/ground/unsteady effects remain physically unvalidated. An omission bound controls error relative to those equations only. Literature novelty must be checked separately; monotonicity, Lipschitz error propagation, screening by upper bounds and compensated/ordered arithmetic are established ideas. No new aerodynamic mechanism is proposed.
