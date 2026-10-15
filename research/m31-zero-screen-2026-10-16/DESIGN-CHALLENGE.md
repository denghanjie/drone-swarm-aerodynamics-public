# Unselected proposal: cheaper exact-zero screening

Date: 2026-10-16. **Static design only.** The coordinator reports that the completed ablation passed numerical/control checks, failed the incremental positive-omission usefulness criterion on both fresh inputs, and attributed most observed savings to the zero-screen package. Those are motivation supplied by the coordinator, not newly evaluated results here. Publish/close that checkpoint before selecting a successor.

Inspected source in `<REPOSITORY_ROOT>`:

- `research/m31-source-omission-2026-10-16/source/candidate.cjs`, SHA256 `c88eef4e67b29ba133dd24965db7cf831cb4337853a5e42f282cca4ceed9317e`.
- `research/m31-omission-ablation-2026-10-16/source/zero-control.cjs`, SHA256 `c85390788f5db157fd17b0703de187774d118679514c59e1e1da7cfdebfcee01`.

Only source reads and hashes were used. No implementation, imports, case generation, scientific numerical evaluation, timing or repository edits occurred.

## Decision and interventions

This is a justified next bounded engineering question: can we retain Z's exact-zero classification and full-source outputs while lowering its complete query cost? It does not investigate a new aerodynamic mechanism. Separate two interventions so a favorable result has an interpretable cause:

| Method | Screening geometry | Positive-envelope/capacity work | Evaluated sources |
|---|---|---|---|
| Frozen M | No source-level screen | None | All eligible sources |
| Frozen Z | Eager center downstream/radial geometry | Complete frozen C bounds, shadow selection and records | Every source except the zero class |
| Proposed E | Same eager center geometry and zero/fallback branches as Z | None beyond what the zero/fallback classifier needs | Every source except the same zero class |
| Proposed L | Same classifier, with radial geometry delayed past downstream-zero exits | Same as E | Same sources and accumulation as E |

**E/Z** measures removal of the entire positive-policy apparatus, including its shadow reporting and bookkeeping. It must not be described as the isolated cost of one arithmetic expression. **L/E** isolates the lazy-radial evaluation schedule, with identical E/L instrumentation and output format. **E/M and L/M** show whether the lean screen remains worthwhile after its own cost. Frozen C need not be rerun: the completed ablation already addressed its incremental approximation, and neither new candidate omits a positive-class source.

## E: eager zero-only screen

Keep the exact axes/offsets, actual radius and nonunit-axis/operator norms, grid, strict center neighborhood, source order and geometry expansion from Z. Keep center `d0`, radial `r0`, downstream lo/hi and radial lower bound eager, with the same numerical expressions and grouping.

Keep the existing branch sequence and inequalities:

1. Zero if hi<=0 or lo>=downstreamCutoff.
2. If the interval can enter positive near downstream and rlo<nearFieldRadius, retain for exact four-rotor evaluation. Never let weak projection/radial support suppress a possible domain error.
3. After near-domain safety, zero if hi<minDownstream*D. Equality at the far-domain start remains potentially nonzero.
4. Compute the same maximum half-width and qlo; zero if qlo>=radialCutoff or projection===0.
5. Otherwise retain every source, regardless of its hypothetical positive bound or remaining budget.

The final retained category means “not screened to zero and not marked fallback,” not “proved positive contribution.” Some such sources have four actual zero terms.

Remove the positive-envelope magnitude tail: denominator/profile and fades used only for the upper-bound value, positive-bound inflation, nextUp and its associated capacity sum/comparison. Remove shadow B, positive-selected lists, shadow masks/counters, and the split code3-versus-code2 accumulation path. The dL calculation is unnecessary once the positive tail is gone; the dH/half/qlo calculations remain because radial zero screening needs them. This is not a tolerance change: all geometry guards and zero thresholds remain identical. Do not optimize scalar dot products, norms, grid layout, precision or projection timing in E.

E uses one unchanged exactTerm path for every retained source, four rotors per source, ascending source ID for each rotor. Use the identical receiver law, body/world load assembly and checksum. Neither E nor L has an approximation budget; actual positive omissions and actual omitted-inflow bound are0. Their acceptance uses full-reference precision gates, not the looser positive-omission budgets.

## L: delay only radial geometry

L differs from E only in the evaluation schedule of source-center radial geometry. Compute d0 and the identical lo/hi first. If hi<=0 or lo>=the cutoff, return the same zero category before forming radial residuals, Math.hypot or rlo. Otherwise form exactly E's r0/rlo expressions and continue its unchanged branch sequence.

These two downstream exits cannot enter the near-domain interval and do not depend on radial information. All surviving arithmetic uses the same numeric inputs and expressions; do not replace Math.hypot with squared distances, a cheaper approximate norm or a new threshold. The caller still computes projection eagerly, as in E/Z: delaying projection is a separate idea and is deliberately excluded here.

It is unsafe to move the later near-skip, radial-support or projection-zero decisions ahead of the near-domain guard. For an interval intersecting the near slab, radial information can determine whether the input must reject, even if no far contribution is expected. The global tilt gate also stays ahead of source screening.

The predicted savings is one source-center radial norm and its supporting arithmetic per downstream-zero exit. It is not one norm per every zero class; many zeros may require radial geometry. Prior Z records do not distinguish zero reasons, so their frequency and wall-time impact are unknown. Grid/neighbor work or memory traffic may dominate. The real-arithmetic envelope and frozen floating margins retain their prior limited status; moving unused calculations does not create a universal numerical certificate.

## Observable equality without a second field

Each prescribed correctness query performs its own screen and field once. Record decisions at that point. Do not run sourceBound again per pair to “verify” categories, construct a hidden shadow E inside L, replay exactTerm, or call a second field for evidence.

For E and L, use the same two-bit source **category** mask:

| Code | E/L category | Actual action |
|---|---|---|
| 0 | Self/outside neighborhood | None |
| 1 | Screened zero | Cull |
| 2 | Near-domain fallback | Evaluate all four terms |
| 3 | Remaining retained category | Evaluate all four terms |

This uses one mask write per candidate and the same storage shape as the existing masks. It adds no separate fallback-ID list. Both E and L create this mask and the same record fields during timed queries; only persistence is outside timing. The mask is not interchangeable with Z's shadow-C mask despite sharing a numeric code range.

After each method returns, ordinary byte/array comparisons establish:

- **E versus L:** exact category-mask equality, hence equality of zero, fallback and remaining-retained identities; exact candidate/zero/fallback/retained counts; identical rotor/profile work; and exact17-column output/checksum equality as the primary implementation-equivalence gate.
- **E/L versus frozen Z:** map E/L codes2and3 to actual retained2; map Z shadow code3 to actual retained2. Require equal actual masks, zero identities, candidate counts, actual retained/rotor/profile counts and fallback **counts**. Require exact full-output/checksum equality on completed valid inputs, since terms and their order are intended unchanged. Preserve every bitwise discrepancy as a failure of this implementation-equivalence claim, even if the independent numerical tolerance also passes.
- Each Z shadow-selected code3 must be E/L category3. Z code2 can map to E/L2or3. This does not recover the full set of Z fallback identities.
- **All full methods versus I:** apply the established independent precision, finite/range, root/bracket/power and domain gates. M/Z/E/L have full-model outputs; do not substitute C's approximation tolerance. Expected domain rejection is an outcome; completed-valid coverage must not be inferred from an empty prefix.

Frozen Z lacks fallback IDs, retained-positive bound values and zero-reason identities. Do not claim those were compared empirically with Z. Static branch identity supports the design; it is not a replacement for the observed masks, counters, independent zero tests and output gates. E/L exact categories are observable because both new methods retain them in their own passes.

In the sole scheduled I pass, its existing per-receiver source terms/classifications can check that each screened-zero source has four exactly zero terms. All E/L/Z masks are already available; a shared zero identity needs only the same oracle terms, not another oracle evaluation. Retain independent zero-test results/codes, all full output rows, and complete current-receiver failure witnesses. A saved-only review can compare recorded classifications with masks and recompute accounting from bytes; it cannot turn these records into an independent re-evaluation of geometry or physical truth.

Use actual per-receiver and aggregate counters with these completed-input invariants:

`screenCalls = candidates`;

`candidates = zeroCulls + nearFallbacks + remainingRetained`;

`actualRetained = nearFallbacks + remainingRetained`;

`rotorVisits = 4*actualRetained`; `actualPositiveOmissions = 0`.

Record `downstreamZeroExits` at the same return branch in E and L; require equality. The source-center radial-norm counts follow the inspected execution schedule: E uses `screenCalls`, L uses `screenCalls−downstreamZeroExits`. Label these as operation counts for this one norm, not all Math.hypot calls or measured CPU time. They exclude offset/axis precomputation and exactTerm's rotor radial calculations. Derive them from the same-pass counters and static schedule rather than add an extra per-source diagnostic pass. No reason counter is retroactively asserted for Z.

## Prospective matrix, timing and caps

If selected, reuse the24frozen small fixtures as exposed regression inputs. Add exactly two fresh inputs from a prospectively fixed generator family at the existing1000/5000sizes, using previously unexposed seeds. The ablation seeds421337/914629 and earlier733109/891007 are now exposed and are not fresh confirmation. Select/freeze new seeds before generation; this proposal selects none. No new geometry is created here. Preserve the existing limitations: one lattice family, fixed density, larger extent at the larger count, and no claim about all poses or huge translations.

Run M/Z/E/L/I on all26inputs. Only if all correctness/equality gates pass, time M/Z/E/L with one warmup each and8measured paired blocks per fresh input. One balanced four-block cycle is M-Z-L-E, Z-E-M-L, E-L-Z-M, L-M-E-Z; repeat twice and freeze case/warmup order. This balances within-block method position and predecessor pairs; it does not remove every runtime/thermal effect.

All methods rebuild geometry, neighbors, masks and loads from identical input bytes. Time the complete queries and their actual instrumentation. Compare every timed output with its corresponding saved correctness output without another field. Report all timings, paired E/Z and L/E ratios, and E/M/L/M context. A prospective engineering usefulness criterion can retain the prior5%median paired reduction and7of8faster blocks on each fresh input; no threshold is selected by this report or tuned after exposure. Correctness and usefulness remain separate. A negative result closes this candidate without a retry or “one more” microbenchmark.

This matrix would require202attempted queries:26×5correctness plus2×4×9timing. Static shape budgeting must count **three** screen-enabled methods Z/E/L, not the preceding campaign's two C/Z paths. For the stated shapes, conservative candidate ceilings are26million direct-oracle center checks,780million combined source-screen reservations,4.3billion rotor-visit reservations and1million receiver solves. Positive-bound arithmetic occurs only in Z. The coordinator/evidence reviewer must derive and verify exact charges before selection/freeze; guard and grid work still belongs in the wall budget.

A separate300s executable cap and128MiB raw cap with4MiB failure reserve are plausible proposal values, not completion estimates. Budget masks for all three screened methods, full M/Z/E/L/I outputs, oracle classifications/zero audits, input states, timings and failure prefixes. The three masks alone have3×the two-fresh-case shape `sum(N*ceil(N/4))` before compression; JSON overhead and independent evidence are additional. Freeze a lossless retention plan that allows a saved-only coverage/equality audit. Do not rely on favorable compression, drop required masks, trim cases or restart after exposure. Preserve one-shot lock/ledger, external watchdog and a separately bounded saved-data review.

## Scope and selection status

This is an engineering simplification and evaluation-order experiment motivated by an observed attribution result. Exact-zero screening, lazy evaluation and broad-phase rejection are established ideas. A pass would establish lower measured cost with unchanged outputs on the specified finite inputs; it would not validate the receiver physics, aerodynamic moments, numerical behavior over all coordinate magnitudes, or trajectories.

The proposal is **unselected**. No implementation or new scientific work follows from writing it. Publish the current checkpoint, then decide whether this one bounded question deserves its own reviewed source/protocol freeze and invocation.
