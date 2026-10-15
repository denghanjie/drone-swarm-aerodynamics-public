# E/L zero-screen controls: static method and API note

Date: 2026-10-16. Prepared after coordinator selection of the next bounded E/L experiment. This task wrote temporary source and a textual diff only. No module import, JavaScript syntax execution, fixture/input generation, geometry/field/root evaluation or benchmark occurred. Repository sources were not edited.

## Files and provenance

- Module: `/tmp/m31-zero-screen-control.cjs`, SHA256 `e029139f71a7eaca1ca1e4f175eac0313060ae9aa1670c7e773ac077dcd73725`.
- Static diff versus frozen Z: `/tmp/m31-zero-screen-control.diff`, SHA256 `cd9e78c832ef92c622db440d370ed67248586d9d704403deb07eec6a000e18b7`.
- Inspected Z: `research/m31-omission-ablation-2026-10-16/source/zero-control.cjs`, SHA256 `c85390788f5db157fd17b0703de187774d118679514c59e1e1da7cfdebfcee01`.
- Intended destination: `research/m31-zero-screen-2026-10-16/source/control.cjs`, under `<REPOSITORY_ROOT>`.

The coordinator reports the preceding ablation published and independently verified at `f5dd23e20b4e64eda647f30870c4a8e0a717e99e`. This implementation does not modify or rerun it.

The four dependency imports are exactly Z's relative paths under `../../../outputs/`: `step02c-source/physics.cjs`, `milestone-28-source/aero.cjs`, `step03a-source/wake.cjs`, and `milestone-26-source/grid.cjs`. They resolve at the intended new repository destination, not at `/tmp`. No path was redirected or module loaded. The next freeze must pin these dependencies.

## What changed

The exactTerm and loadRows function text is unchanged from Z, as are dot, fade, the f0/area/vi0 expressions, rotated geometry and its numerical norms, grid neighborhood and source order. The retained geometry allowance remains1e-12m. Positive-bound inflation, Lipschitz/target/capacity calculations, nextUp, positive-selection lists/B/shadow counters and the split selected/retained accumulation paths are removed.

E preserves the eager downstream/radial geometry and all zero/fallback decisions of sourceBound. It returns a retained category after the final zero test instead of calculating a positive upper-bound magnitude. The internal screen still returns the original two-property `{kind,bound}` object shape. For zero and fallback it preserves the original0/null sentinel; remaining sources return `{kind:'retained',bound:null}`. This null is a compatibility placeholder, not a computed bound or hidden budget. Keeping the allocation shape avoids additionally bundling elimination of all per-pair result objects into E/Z.

L uses the same classifier expressions but delays only r0/rlo until after the two downstream-zero exits. Projection remains an eager caller argument in both methods. There is one shared traversal, exact-term loop, record construction, guard cadence and load/checksum path. Method selection chooses the screen function once per query; it does not add method-specific hot-loop diagnostics. Every nonzero category receives exactly four exactTerm calls in ascending source order, with each rotor's sum updated in that order.

Both source classifiers increment `counts.downstreamZeroExits` at the corresponding `hi<=0 || lo>=downstreamCutoff` return. Their other instrumentation is identical. Neither adds a secondary classification or field pass.

## Exact API

`query(states, method='E', options={})` accepts only method `'E'` or `'L'`. Unknown methods throw before field geometry. Options are the **third** argument; `query(states, options)` is not this API. `fields(states, method='E', options={})` has the same convention.

`query` returns:

- `rows`: actual17-column outputs in the frozen order U0..U3, f0..f3, bodyThrust, roll, pitch, worldFx..worldFz, worldMx..worldMz.
- `checksum`: the frozen sequential sum over every value in those rows.
- `counts`: actual work and the derived source-center norm count, described below.
- `records`: one completed-receiver category record per valid receiver.
- `method`, `recordSemantics:'source-screen-category-v1'`, `maskCodes`, and `actualOmittedInflowBound:0`.

`fields` returns actual `winds` instead of assembled rows/checksum, with the same remaining metadata. Exported names are `f0,D,vi0,a,allowances,recordSemantics,maskCodes,fields,query`. No bound/capacity/nextUp helper remains exported.

Options are `guard(counts)` and `onReceiver(row)`. Guard is invoked before each receiver, at the frozen cadence. Counts are the live actual counter object, not a shadow view. The receiver callback runs after its full wind and record are completed. An `evidence` option may be passed but does not suppress mask/record construction: both methods always construct them, including timed calls. Persistence belongs in the caller, outside prescribed timers.

Callbacks must not mutate states, counts or records. Input finite/norm admission remains the prospective driver's responsibility, as for the parent candidate. Domain errors propagate unchanged. No claim of a full field or complete counter set follows from a thrown call.

## Counters, records and mask meanings

Aggregate `counts` keys are:

`candidates, screenCalls, zeroCulls, positiveOmissions, actualPositiveOmissions, retained, nearFallbacks, remainingRetained, downstreamZeroExits, centerRadialHypotCalls, rotorVisits, profileEvaluations`.

Both positive-omission counters are permanently0. `retained` includes near fallback and remaining-retained sources. `screenCalls` increments once per eligible pair. There is no `boundAttempts` key because neither method calculates a positive bound.

Per-receiver records contain:

`receiver, mask, candidates, screenCalls, zeroCulls, retained, nearFallbacks, remainingRetained, downstreamZeroExits, centerRadialHypotCalls, semantics, actualPositiveOmissions:0, actualOmittedInflowBound:0`.

The mask is Uint8Array of length ceil(N/4), with2bits/source, least-significant pair first. Padding bits stay0. Codes are0self/outside,1screened zero,2near-domain fallback,3remaining retained. Codes2and3 both evaluate all four source terms. Code3 does not assert that an actual source term is positive, nor does it mean omission. `semantics` equals the top-level recordSemantics string. `maskCodes` is a frozen descriptive object shared by both methods.

For complete valid calls, require:

- `screenCalls=candidates=zeroCulls+nearFallbacks+remainingRetained`.
- `retained=nearFallbacks+remainingRetained` and `rotorVisits=4*retained`.
- E: `centerRadialHypotCalls=screenCalls`.
- L: `centerRadialHypotCalls=screenCalls−downstreamZeroExits`.

Per-receiver downstream exits are the global counter difference across that receiver. Its norm count is derived from source calls and that branch count after the receiver completes; the aggregate norm count is updated at the same time. Thus guard sees a consistent completed-receiver prefix. A thrown mid-receiver query does not supply a current complete derived norm count. This count covers only the classifier's source-center radial Math.hypot, not axis/offset preprocessing or exactTerm's rotor radial norm. It is a static-schedule operation count, not hardware profiling.

E/L counters should agree except for `centerRadialHypotCalls`; their difference must equal the common downstreamZeroExits. Do not compare every record/counter field as blindly equal: the norm count intentionally differs and top-level `method` differs. All category masks and other category/work counts are intended identical.

## Static justification and prospective equality limits

E reproduces the original zero/fallback predicates with identical geometry expressions. Removing dL and the positive magnitude tail cannot affect an earlier zero/fallback decision. E does not reproduce numerical errors that might occur only in Z's unused positive-bound tail for arbitrary inadmissible inputs; equivalence is claimed for admitted inputs on which the frozen parent path completes, and the new scheduled Z baseline must itself pass.

For L, the downstream-only interval predicates do not depend on radial geometry. If hi<=0, no rotor can lie in the strictly positive near/far interval under the envelope. If lo>=the downstream cutoff, no rotor can enter its retained downstream range. Neither exit can suppress a near-domain obligation. For surviving pairs, L computes exactly E's r0/rlo expressions before the original near-domain test. The near test still precedes near-skip, radial-support and projection-zero pruning; equality at the lower far-domain boundary remains potentially nonzero. Eager projection and the global tilt check are preserved.

These arguments support identical classifier decisions under the shared finite input contract; they do not establish a new outward-rounded geometry certificate. The frozen margin still needs the prescribed independent finite-case checks.

Prospective runtime comparisons can use the records from each scheduled pass: exact E/L category-mask equality; E/L full rows/checksum equality; mapped actual-mask equality with Z (E/L2/3→retained2, Z shadow3→retained2); actual zero/candidate/retained/rotor/profile and fallback-count agreement with Z. Frozen Z has no full fallback-ID mask, retained-positive bound log or zero-reason identities, so do not claim those were empirically matched to Z. Every Z shadow-selected code3 should be E/L category3, but the reverse need not hold.

The scheduled independent I pass can check all shared zero identities against its already-produced terms/classifications. Do not invoke sourceScreen, sourceBound or exactTerm again solely to verify decisions. Exact equality is an implementation claim; separate I precision, root/range/power and domain gates remain required. No equality or timing result has yet been observed for this module.

The source is ready for coordinator copy, independent static review and the new protocol/source freeze. No scientific invocation is authorized or implied by this note alone.
