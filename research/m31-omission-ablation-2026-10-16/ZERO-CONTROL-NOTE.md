# Static method and API note: Z zero-screening control

Date: 2026-10-16. **Implementation prepared without scientific execution.** Only source reads, text edits, a textual diff and hashes were used. No module import, syntax execution, case generation, fixture creation, geometry/field/root calculation or benchmark was performed. The original candidate and repository files were not edited.

## Artifacts and placement

- New temporary module: `/tmp/m31-ablation-zero-control.cjs`, SHA256 `c85390788f5db157fd17b0703de187774d118679514c59e1e1da7cfdebfcee01`.
- Saved unified static diff: `/tmp/m31-ablation-zero-control.diff`, SHA256 `4b3afae96c7cd3117dc513b211a52c74091c43bd1f0ab5b2536c6672eca169f6`.
- Inspected frozen source: `research/m31-source-omission-2026-10-16/source/candidate.cjs`, SHA256 `c88eef4e67b29ba133dd24965db7cf831cb4337853a5e42f282cca4ceed9317e`.
- Intended new destination: `research/m31-omission-ablation-2026-10-16/source/zero-control.cjs`, beneath `<REPOSITORY_ROOT>`.

The coordinator reports the current omission checkpoint closed/published at `85e789c8d29a05364b163714a6540f6dc265134a`, with remote commit/manifest, local hashes and independent review verified. This task does not reopen that campaign.

Imports intentionally remain exactly the frozen relative paths: `../../../outputs/step02c-source/physics.cjs`, `../../../outputs/milestone-28-source/aero.cjs`, `../../../outputs/step03a-source/wake.cjs`, and `../../../outputs/milestone-26-source/grid.cjs`. They resolve at the intended repository destination. The temporary `/tmp` copy is **not** a runnable standalone location; no import path was redirected to the working tree or a saved result. The new freeze must pin these same dependency bytes.

## Scientific intervention and static diff

The text of imports, constants, targets, allowances, capacity, nextUp, dot, fade, sourceBound, exactTerm and loadRows is unchanged. In particular, no cheap early branch, numerical reformulation, domain-rule adjustment, tolerance change or bound optimization was introduced.

`fields` now always uses the C path (`omit=true`). Geometry/grid construction, source order, zero decisions, near fallback, nextUp capacity selection, code writes, omitted-list appends and B accumulation remain the frozen operations. All C masks/lists/records are constructed even if `evidence` is false.

At the one positive-envelope acceptance branch, the frozen C bookkeeping executes unchanged. Z then evaluates and adds all four exact source terms before continuing. It does not overwrite code3 with code2 in the shadow mask. The usual retained path still evaluates its sources exactly once. As each source is handled in the original ascending ID loop, each rotor accumulates every nonzero-class source in ascending source order, including shadow selections. Exact zeros remain skipped. No decisions depend on a wind/load result or reference value.

Two small additions distinguish the counters: an extra two-counter `selectedSourceWork` object counts work performed for shadow code3 sources; an `actualCounts` view combines it with the unchanged C counters. The original internal `counts` object remains the shadow C counter set. No source classifications, fallback IDs or retained-positive bound values are added to the hot loop.

## API

`query(states, options={})` accepts the same17-value state rows as the frozen candidate. Call it with options as its **second** argument; there is no method-string argument. It returns:

- `rows`, `checksum`: actual Z inflows, effective thrusts, body/world loads and the unchanged checksum reduction, with the frozen17-column output order.
- `counts`: actual Z work. `positiveOmissions` and `actualPositiveOmissions` are both0. `retained` includes shadow C retained and shadow C positive-selected sources. `rotorVisits` and `profileEvaluations` include all terms Z actually evaluates. Candidates, bound attempts, zero culls and near fallback counts have their ordinary actual meanings.
- `shadowCounts`: the original C-style decisions and work counts. `positiveOmissions` here means selected by the shadow C capacity rule; `retained` is C-retained only. Rotor/profile counts include only sources C would evaluate. The identical term calculation supplies those counts during Z's pass; no second C pass occurs inside Z.
- `selectedSourceWork`: `rotorVisits` and `profileEvaluations` from only the additionally evaluated shadow code3 sources.
- `records`: per-receiver shadow C records with the explicit fields described below.
- `recordSemantics:'shadow-C'` and `actualOmittedInflowBound:0`: prevent confusing the shadow budget with an actual Z approximation budget.

`fields(states, options={})` provides the same metadata with actual `winds` instead of assembled `rows` and `checksum`. Exports otherwise retain the frozen constants and bound helpers for the coordinator's existing checks. Their presence is not permission to evaluate them outside the sole frozen scientific invocation.

Options:

- `evidence`: accepted for interface familiarity; full C bookkeeping is constructed regardless, as in frozen C.
- `guard(actualCountsSnapshot, shadowCounts)`: called at the same per-receiver location as C. The first argument is a fresh actual-count snapshot; the second is the current shadow counter object. A callback that only uses its first argument sees actual work. No extra guard cadence is introduced.
- `onReceiver(row)`: called at the same completed-receiver point as C, after the row is appended to `records`.

Callbacks must observe, persist or stop; they must not mutate counters, decision records or input arrays. Failed calls throw the original errors and need the driver's normal failure context. Completed receiver callbacks do not imply a complete field after a later failure.

## Record and mask semantics

Each record preserves C's original fields: `receiver`, `mask`, `omitted`, `B`, `candidates`, `zeroCulls`, `retained`, `nearFallbacks`. It appends `semantics:'shadow-C'`, `actualRetained:retained+omitted.length`, and `actualPositiveOmissions:0`.

| Shadow code | Shadow C meaning | Actual Z behavior |
|---|---|---|
| 0 | Self or outside eligible neighborhood | No source evaluation |
| 1 | Bound classifies exact zero | Culled |
| 2 | C retains source, including fallback | Evaluates all four terms |
| 3 | Positive envelope selected within C capacity | **Evaluates all four terms and retains them** |

`record.omitted` and `record.B` are exclusively shadow C metadata. They must never be reported as actual Z omissions or actual Z load-error capacity. If the saved schema needs an actual retention mask, derive it outside the timer by mapping3to2 and retaining0/1/2. Preserve the original shadow mask so C/Z decisions remain auditable.

For complete valid calls, the implementation implies these static accounting identities:

`actual.retained = shadow.retained + shadow.positiveOmissions`;

`selectedSourceWork.rotorVisits = 4*shadow.positiveOmissions`;

`actual.rotorVisits = shadow.rotorVisits + selectedSourceWork.rotorVisits = 4*actual.retained`;

`actual.profileEvaluations = shadow.profileEvaluations + selectedSourceWork.profileEvaluations`.

These are prospective consistency assertions, not observed test results.

## Narrowed runtime equality gate

The frozen C evidence does not retain fallback IDs or bounds for all retained positive-envelope sources. Therefore compare only exact C/Z masks, selected `[source,bound]` lists, accumulated B, zero identities, candidate counts, shadow retained counts and near-fallback **counts**, plus other shared counters where present. `shadowCounts` should match C's corresponding complete-call counters; actual Z counts have the identities above. SourceBound and exactTerm branch identity is established statically by the saved diff.

Do not claim retained-positive bound equality or fallback-ID equality was empirically observed. Those intermediate objects were not recorded by C, and no unmatched instrumentation was added to obtain them. Likewise, “positive envelope selected” does not imply the actual four terms are positive.

Z must still pass the independent full-load, zero-term and domain-agreement gates. C must pass its original approximation gates. Source identity and bookkeeping agreement do not replace those numerical checks.

## Timing disclosure and readiness

The scientific calculations and all original C bookkeeping are retained. Z additionally allocates one selected-work counter object per query, forms an actual-count snapshot at each invoked guard and once on return, and appends the explicit semantic/actual-retention fields to each already-required record. Its returned metadata also exposes shadow/actual work. These are honest reporting costs inside the actual implementation; no unmeasured claim that their cost is zero or negligible is made. The exactTerm calls for code3 sources use the selected-work counter object, while C-retained terms use the original counter object. The comparison is between these complete implementations, not an instruction-identical hardware counterfactual.

There is no extra mask allocation, fallback-ID collection, retained-bound log, second field evaluation, mask reuse or reference-informed decision. The desired attribution still excludes the separately proposed lazy-radial-bound optimization.

This file is ready for the coordinator's source review/copy and the evidence agent's independent static audit. It has not been imported, parsed by a JavaScript runtime, or scientifically tested. The new protocol, freeze, coverage, gates and launch remain the coordinator's next steps under the existing research procedure.
