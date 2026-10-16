# Next decision after the scoped browser-screen pass

2026-10-16. Bounded planning review only. No run, source acquisition, implementation, or physical-data access is allocated by this document.

## Recommendation

Close the F browser confirmation as useful engineering evidence. The next actionable research decision should be:

**Can conservative bounds computed from current geometry certify useful approximation of the coupled rotor loads without constructing every current interaction coefficient, and can that complete certified query materially beat the strongest exact implementation?**

Advance a mathematical and interface design for this question before considering execution. This targets the construction bottleneck and a missing numerical-error guarantee together. It is a possible contribution in verified numerical computation for the specified model, not a new aerodynamic law. An unsuccessful bound, unaffordable certificate, or exact comparator that performs just as well is a substantive negative answer.

The most consequential gap for the original *physical* research goal remains the sufficiency of the intended hardware's actuator/source contract, followed by receiver and aggregate-response validation. No physical hardware access or new matched measurements are available in the present session. All historical acquisition attempts remain closed. A data-admission prerequisite is therefore recorded below; it is not an immediately executable validation plan or a reason to repeat exhausted access attempts.

## Evidence used, and what it supports

The coordinator reports that the frozen campaign closed, its saved audit passed 57,572 groups, complete outputs agreed across three processes, and the six N5000 paired median F/L ratios were 0.7596, 0.8048, 0.7473, 0.7718, 0.7411, and 0.7426, with F cell medians approximately 366–396 ms. These are **coordinator-supplied completion facts**, not results independently reread or recomputed for this recommendation. The protocol I read still has its prospective status wording [D1].

Those facts answer the frozen finite browser question. They do not establish live coupling, complete frame cost, physical fidelity, general browser portability, or novelty. F retains ordered all-pairs enumeration and current coefficient construction [D10]. The frozen inputs are short airflow-off motion followed by final-state load queries [D1, D3].

The relevant unresolved gap is concrete:

- Earlier construction-inclusive work found its conservative grid slower than direct all-pairs, despite fewer candidates. Geometry construction represented 96.3–97.6% of aggregate grid-query time on those historical large states [D11]. These are historical Node observations on different states, not a measured phase decomposition of the new Chrome campaign.
- The adopted root-defect corollary assumes complete, fixed, **current** nonnegative coefficients and current weights. It can bound arbitrary candidate roots but does not itself avoid geometry construction, certify that construction, or establish useful floating-point tightness or cost [D9].
- Prior reuse and prediction ideas do not certify current admission or events between refreshes. The literature review explicitly warns that a monitor rebuilding the whole geometry can consume the proposed saving [D7]; the browser ledger preserves later ratio-reuse and secant failures [D2]. None is repaired here.

A faster root solve, another storage change, another scalar distance-screen tweak, or repeating the same F/L test leaves that central gap intact. A geometric hierarchy is not inherently superior: the recorded grid loss makes an equally lean exact spatial comparator essential.

## Prospective computational design — conditional, no allocation

### 1. Fix the mathematical and operational contract first

Retain the current source/receiver equations, binary64 input interpretation, current poses and nominal motors, support and rejection semantics, and declared load outputs. Do not combine the experiment with stale-state reuse, a changed physical law, a new flight controller, or a precision change. The principal endpoint is a same-state complete interaction query. Live trajectory accuracy is a later question.

The candidate should use a current spatial hierarchy with conservative spatial/orientation envelopes. It may omit admitted nonnegative contributions only when it retains a computable outward bound on their total effect. Source positions, rotor offsets, orientations, current motor normalization, support boundaries, and every domain-rejection branch must be covered. A coefficient that is zero by an admitted branch is not interchangeable with a pair whose validity is unknown.

An unresolved cluster must be refined or evaluated exactly. If the entire state cannot be certified as in the original contract, return its specified rejection or a named unqualified result. Do not use an approximate zero to hide invalid geometry. Support/membership changes are evaluated from the current state; prior acceptance grants no admission. Cyclic or otherwise out-of-contract cases are rejection/fallback controls unless a separately justified model contract admits them; they are not silently added to the ordered solver's domain.

### 2. Establish the missing bridge from geometry to load error

The existing exact-real corollary supplies a useful starting point, not a completed implementation. For a candidate rotor vector with `0 < xhat_ir <= 1`, form the candidate source amplitudes from the **same current weights**, with conservative enclosure of

`yhat_i = sqrt(sum_r w_ir * xhat_ir)`.

The proposed new geometric machinery must enclose each complete current row contraction, including omitted contributions:

`sum_j a_irj * yhat_j in [sL_ir, sU_ir]`.

It must do so without covertly reconstructing all omitted coefficients. Outward arithmetic can then enclose

`p_ir = xhat_ir^3 + xhat_ir * sum_j a_irj * yhat_j`

as `[L_ir, U_ir]`. If every lower endpoint is positive, the inherited construction suggests outward `kbar_ir = max(1, U_ir, 1/L_ir)` and `Kbar = max_ir kbar_ir`, then conservative rotor-root intervals based on `xhat_ir/(kbar_ir*Kbar)` and `min(1, xhat_ir*kbar_ir*Kbar)` [D9].

**Proof obligation:** independently establish that the geometric row enclosures contain the original complete current coefficients, that the original model's whole-domain admission bridge still holds, and that all rounded operations preserve the enclosure. The displayed extension is a proposed way to use the corollary, not a newly proved theorem in this review. Rounded weights, candidate-derived square roots, support calculations, and denominator arithmetic cannot be treated as exact without justification. A saved coefficient interval alone does not certify its geometric origin.

Propagate rotor intervals to collective world force and roll/pitch moment using signed lever arms and an enclosed norm of the actual saved rotation column. Keep individual rotor, collective force, and moment errors separate. Missing admission, unbounded arithmetic, or an overly loose bound means refinement/fallback or rejection. A candidate residual computed only on the retained sparse matrix is insufficient.

This bridge is the immediate desk-stage go/no-go. If no conservative envelope can avoid essentially the same full construction, or the global factor makes the bounds uninformative, report that obstacle before proposing a timing campaign.

### 3. Close the actual comparator gap

Any later frozen comparison needs these distinct roles:

| Arm | Purpose |
|---|---|
| Original lean L / independently checked complete model evaluation | Semantic and numerical reference; retain original failures and guarded-domain behavior. |
| F, the now-confirmed current all-pairs screen | Strongest admitted complete-query performance baseline for the named browser; do not regress to a weaker builder. |
| H, an equally lean **exact** version of the proposed current hierarchy | Tests whether ordinary exact spatial enumeration alone accounts for the gain. Same data layout, allocation discipline, scheduling, and solver as far as the contract allows. |
| B, the bounded-omission version of H | Adds approximate omission, complete conservative certification, refinement and exact fallback. Tests the additional value of controlled approximation. |

H has not been implemented or qualified by the files read here. It must earn correctness and performance admission; the historical grid result is not a reason to presume its outcome. If H beats F and B adds no benefit, the result supports exact enumeration engineering, not a certified-approximation advantage. If B only beats the old slow grid, the substantive question has not been answered.

Freeze a common returned-output and evidence contract for every timing arm. The closed browser protocol retained complete classification-symbol tensors [D1]; a new candidate cannot obtain a claimed algorithmic win merely by omitting dense diagnostic outputs that F still materializes. If a production-load query excludes those tensors, apply that same exclusion to all timing arms and independently requalify the modified F-derived reference against the complete model. Call this a new query contract: the closed 366–396 ms measurements then remain context, not its matched baseline. Preserve full diagnostic checks where needed for qualification without charging unequal audit work to one method.

The timed boundary includes current hierarchy construction/update, current admission checks, all bounds, retained coefficient work, ordering/solve, certificate evaluation, refinements, fallbacks, allocation, and load assembly/consumption. Record end-to-end application overhead separately. Do not time a cached hierarchy or already-built matrix while describing moving-state cost. Diagnostic exact-oracle work may be outside the candidate clock only when it is not needed by the deployed candidate; all actual monitoring and fallback remain inside.

### 4. Make the future result falsifiable

Before any scoring, freeze disjoint development controls and prospective evaluation families, the complete sources, reference, numerical policy, source/runtime identities, and stopping/resource rules. Existing exposed states can serve as disclosed regression controls, not fresh confirmation.

The evaluation must include preregistered ordinary target workloads and stress strata covering expanded-volume versus increased-density scaling, nonuniform clusters, orientations and motor imbalance, support-boundary crossings, and near-domain failures. These are different sources of complexity; three fresh processes do not substitute for diverse states. Correctness controls must retain fallback/rejection cases. Choose the primary performance strata before results; report every adverse or failed stratum.

For a concrete provisional engineering design, use normalized maximum rotor, collective-force and roll/pitch-moment errors, each at most `1e-3` in the established `mg/4`, `mg`, and `mgR` units, with a separately frozen `1e-4` setting as a tighter secondary budget. These are numerical model-fidelity budgets, borrowing the scale of the inherited local screen [D7]; neither is an admitted physical tolerance. Their scientific meaning is control of error relative to the specified equations. They require prospective adoption and cannot be changed after observing cost or rejection rates.

Use an independently justified high-accuracy reference with a separately bounded solver/arithmetic error. Require every accepted answer's discrepancy to be consistent with its certificate after that reference uncertainty is accounted for, and require the candidate's certified bound itself to meet the selected budget. A floating reference is not the exact algebraic solution. Sampled agreement tests implementation failures; mathematical enclosure and outward-arithmetic arguments must provide the soundness claim. Preserve certificates, reference uncertainties/errors, rejected answers, refinements, fallback frequency, complete times and memory. One demonstrably unsound accepted certificate rejects certification. Correct fallback can preserve answer validity but cannot conceal its cost. Full local certification does not guarantee long-horizon path agreement; the retained refinement and cadence failures remain open [D5].

A deliberately material *proposed* practical hurdle is a paired median complete-query ratio at most `0.50` versus both F and H on every preregistered primary N5000 performance cell, together with a fixed majority-win rule and all correctness gates. This is a design recommendation demanding a structural gain, not an adopted threshold or a real-time requirement derived from flight. If prospective scope owners select another hurdle, justify and freeze it before evaluation. Even halving the reported 366–396 ms query times would not demonstrate a live frame budget. A two-budget result is only a finite numerical cost/error comparison, not a universal frontier.

No sample count, process slot, resource cap, new seed, implementation dispatch, or run permission is created here. A later protocol must set those before execution. Failure of the proof bridge ends this candidate; a timing miss, excessive fallback, or failure to beat H rejects its practical contribution without erasing useful counterexamples. Do not tune a new hierarchy or threshold on the evaluation set in the same cycle.

## Physical route: important but presently unavailable

For the original aerodynamic claim, retain the previously proposed single-source sufficiency question [D8]: **on the intended 27 g vehicle/propeller/drive, does one fixed spatial mean-wake shape, scaled by independently measured effective thrust and density, predict held-out actuator conditions?**

The prospective design uses an identified symmetric baseline, a lower symmetric command, and a preselected unequal command vector matched to the baseline total thrust using thrust-only calibration. Freeze commands before inspecting held-out flow. Compare measured downstream/radial profiles against `u0(x)*sqrt[(T/rho)/(T0/rho0)]`; include settled all-off background. Measure force independently of the velocity-field reconstruction. Retain commands, RPM, supply, specimen, mounting/tare, geometry/registration, repeatability, sensor uncertainty, and environmental conditions. Shaft-power claims additionally require torque and an identified power mapping. Resolved held-out shape/asymmetry changes falsify scalar source sufficiency over the tested domain. Non-rejection alone is not physical adequacy; any positive adequacy decision needs independently justified tolerances and simultaneous uncertainty coverage.

The immediate prerequisite is a lawfully usable, identifiable set of these observations with repeat/uncertainty metadata, or a separately agreed hardware-measurement capability. Neither is available here. The fixed-PWM report view consumed its 3/3 operations, admitted no thrust triplet or extraction specification, and remains closed [D12]. That access outcome does not prove that suitable data do not exist. It does not authorize another attempt, author contact, a new acquisition, or extracting inaccessible figures. Browser success changes none of those boundaries.

A source-test pass would support only a finite steady source contract. It would still leave the fixed-command receiver response, multi-wake aggregation, 46 mm hardware transfer of other sources, and live feedback prediction open. A failure could invalidate assumptions behind the computational workload and should be allowed to do so; do not calibrate away the held-out failure.

## Literature and claim status

All literature statements here are inherited from the local notes listed below. No original publication, web page, bibliography target, correction notice, or new dataset was opened. “Verified” below describes the **earlier records'** status, not new verification in this review.

- The inherited Bauersfeld arXiv v3 reading supports a near-hover/far-field normalized mean-wake model, with measured vehicles starting at 230 g; arbitrary motor-dependent scaling on this project's 27 g hardware remains an extension [D4, D8]. It supplies no universal fixed-command source/receiver contract.
- Wolf et al., *Experiments in Fluids* 65:152, DOI `10.1007/s00348-024-03880-3`, version of record 2024-10-02, is recorded as previously verified. Free-hover control with varying rotor speeds and normalized fields is not a fixed-PWM identification experiment. The inherited raw-data and uncertainty gaps remain [D8].
- Kiran's fixed-4-V/hover-PWM qualification, the prescribed-RPM GWS versus static Crazyflie distinction, and the Gielis aggregate-interaction caution are inherited summaries, not newly admitted measurements [D8]. The earlier contribution assessment identifies nonlinear aggregation and learned-control antecedents; it establishes no matched superiority for this project [D6].
- Ahmad–Cohen and Tuckerman–Berne–Martyna were previously admitted as method evidence with the source-status limitations in D7. They do not furnish this geometry-to-load certificate or a validated drone refresh policy. This proposed current-state enclosure is not a reproduction of either method.
- The root-defect corollary is adopted conditional exact-real project theory; floating-point soundness, tightness, implementation, physical relevance, and novel priority remain untested [D9]. Spatial hierarchies, interval bounds and certified residual methods have obvious methodological antecedents. This review establishes no originality claim or exhaustive literature clearance.

The defensible possible contribution is therefore a precisely scoped, reproducible **complete-cost comparison with sound local numerical guarantees and preserved failure regions**. Claiming a new method would additionally require a separately authorized, focused prior-art comparison and matched published baselines. Claiming physical prediction would require the missing physical evidence. Neither follows from a benchmark pass.

## Exact reading inventory

Exactly twelve existing content files were read. Directory/file-name listings were used only for selection. No linked files were followed, no raw target arrays or campaign result files were read, and no scientific code was imported or executed. No retrieval, new agent, renewed closed access, or repository edit occurred. The sole deliverable was the temporary planning note, copied here with private path prefixes removed.

All following paths are repository-relative in this public copy:

1. **D1:** `research/m31-browser-screen-2026-10-16/PROTOCOL.md`
2. **D2:** `research/m31-browser-screen-2026-10-16/LITERATURE-EXPERIMENT-LEDGER.md`
3. **D3:** `research/m31-browser-screen-2026-10-16/PHYSICS-BOUNDARIES.md`
4. **D4:** `research/m31-browser-screen-2026-10-16/design-reviews/m31-browser-screen-goal-alignment.md`
5. **D5:** `outputs/research-roadmap.md`
6. **D6:** `outputs/research-contribution-assessment.md`
7. **D7:** `research/m31-reuse-literature-2026-10-16/ADMISSION-AND-NEXT-TEST.md`
8. **D8:** `research/m31-source-contract-planning-2026-10-16/EVIDENCE-AND-NEXT-TEST.md`
9. **D9:** `research/m31-root-defect-planning-2026-10-16/ADOPTED-DERIVATION.md`
10. **D10:** `research/m31-current-construction-planning-2026-10-16/PARENT-DECISION.md`
11. **D11:** `research/m31-coupled-cost-host-2026-10-16/MILESTONE-SUMMARY.md`
12. **D12:** `research/m31-fixed-pwm-view-2026-10-16/ADMISSION.md`
