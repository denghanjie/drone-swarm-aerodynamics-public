# Native-load wrapper draft: source only

This directory is a source-only draft for parent review. Nothing here grants execution permission. No scientific module has been imported, no control has been evaluated, and no target query has run. The only JavaScript checks performed were `node --check` on the two new modules; both exited0. Historical files were copied byte-for-byte and were not edited in their original locations.

## Files and API

- `source/native-load.cjs`: wrapper, native output materialization and evidence encoder.
- `source/native-controls.cjs`:24 literal additional microcontrols and their prospective assertions; imports only the copied inherited control definitions.
- `source/vendor/{kernel,lean-anchor,anchor-kernel,reference-excerpt,controls}.cjs`: unchanged copies from `research/m31-browser-screen-2026-10-16/source`.
- `SOURCE-PINS.json`: byte lengths/SHA-256 of source files and verified original-copy relationships.

After separately approved source publication and run allocation, the callable interface is:

```js
const result = nativeLoad.query({drones: [{id, state: [/*17 native numbers*/]}]}, 'F', guard);
const wire = nativeLoad.encodeEvidence(result); // outside query timing
```

Method is `F` or `L`, default F. `guard` is an optional no-argument cooperative callback; default no-op. It is called inside the query timer and passed into the unchanged native builder/solver/residual. A thrown guard becomes `resource-failure/cooperative-guard`. This is cooperative interruption, not a hard realtime bound. The harness still needs independent wall/RSS/process supervision.

`native-controls.cjs` exports `additionalControls()`, `additionalControlIds`, `evaluateControl(spec,result)`, `inheritedControls()`, `inheritedControlIds` and `ownershipSequence`. Definitions and assertions are functions; no fixture construction/evaluation occurs merely because the source is read or syntax checked. The CommonJS require of vendor controls at module load only obtains definitions.

## Fixed implementation choices

Input is exactly a plain/null-prototype record with one own data property `drones`. Each drone is a plain/null-prototype record with exactly own data properties `id,state`. Arrays must use Array.prototype, have only own `length` plus contiguous own data indices and no extra symbol/string properties; holes/accessors are refused. Native typed arrays and cross-realm array prototypes are not this interface. This is a contract for trusted plain data, not a sandbox for hostile Proxy traps.

N is1–5000. IDs are unique nonnegative safe integers; negative zero is refused. Each row has17 finite native numbers. The wrapper copies all rows before any kernel call and sorts its copies by ID. The caller's row order/storage is not modified. Canonical sorting is a declared wrapper change: the inherited index tie order becomes stable-ID order, and its complete cost is timed.

Each nominal force must be positive. Native left-fold totals and the native normalizer/source-scale operations must yield finite positive values. The same grouping as the historical formula is used: `sqrt(f/(2*rho*A))` and `sqrt(S0/mg)`. A finite raw value is not a promise that all downstream native arithmetic is representable.

F is the copied screen builder; L is copied lean all-pairs. `fullSymbols=false` is retained. F still visits every ordered pair and can only skip center norms through the retained finite-span component predicate; fallback pays both F preflight and L work. The2,000,000 actual positive-term cap remains an immediate inherited resource limit, with no truncation.

Returned coefficient arrays are checked for shape, monotone row offsets, sorted nonself source indices, finite strictly positive K/a and the actual term limit. A stored positive K whose normalized coefficient underflows to0 is an explicit numerical-failure. Native admission and descending graph eligibility must pass. Geometry/nominal/cap/domain behavior is the unchanged kernel behavior. Native admission does not claim exact M-current admission.

The solver remains O with its original56-bisection cubic closure, alpha0 shortcut, source reduction order and y construction. No48-round diagnostic recipe, exact coefficients, cached solution or oracle is supplied. The complete native residual map remains computed unchanged and checked. Both solve/residual y and x must be finite in(0,1], alpha finite and nonnegative, T positive finite and <=its nominal force. Residual log<=1e-9 and normalized source/receiver mismatch<=2e-9 are new explicit engineering guards on this wrapper's success status, using the cutoffs from the historical browser comparison. They do not substitute for any of the four strict offline1e-8 accuracy criteria.

Native delivered output is explicitly:

1. rotor force uses the solver's rounded `T=f*x`;
2. collective starts at0 and adds rotor0,1,2,3;
3. worldForce multiplies each prepared axis component by collective;
4. each worldMoment component starts at0 and accumulates `cross(preparedOffset[r],preparedAxis)[k]*T[r]` for rotor0,1,2,3, with native separate products/subtraction for cross.

No physical yaw reaction moment or body-torque conversion is added. The prepared axes are their supplied near-unit words, not idealized exact orthonormal axes. A linear-force underflow that produces a zero native T is unsuccessful rather than silently admitted.

The success-status string is consumed first as character codes; then each exact-safe-integer ID is consumed as its binary64 word immediately before its11 delivered load words. Words are read into a DataView and mixed as their two32-bit halves by a simple FNV-style checksum. Counts are separately recorded as `loadWords=11*N`, `identityWords=N`, `statusCharacters=14`, with `status:'native-success'`. This consumes every delivered word and its ID/status association without a floating accumulation that might overflow. The checksum is not collision-resistant evidence or a numerical certificate; byte-identified evidence and independent checking remain required.

## Query timing and evidence

`performance.now()` starts before method/input validation. Copying, canonicalization, force/range checks, preparation, screen/fallback, coefficient assembly, admission, ordering, solve, residual, prepared-evidence fields, actual loads, finite/range checks and full output consumption all occur inside the timer. Successful result object assembly is also before the final timestamp. Attaching the timing metadata itself occurs after that final timestamp. Failure time remains included; completed phases plus the unfinished/finalization phase sum to total time up to ordinary timer arithmetic.

The old builder phase values are nested diagnostic fields; do not add them to the wrapper phases. Constant/module initialization and source loading happen once outside the per-query timer. This is a query boundary, not startup-to-display or full physics-step cost. Encoder conversion to hex, JSON serialization, hashing, persistence and independent reference checking are outside this query timer and must be separately accounted. No new performance claim is supported by this source draft.

`encodeEvidence` accepts only the native result. It converts every raw/prepared/constant/coefficient/solution/load binary64 value to16 lowercase hexadecimal digits in big-endian word order. It preserves signed-zero words and can encode nonfinite diagnostic/prepared failure values; it does not claim to preserve all NaN payload bits. Numeric diagnostics that are nonfinite become `{nonfiniteWord: hex}` so JSON cannot silently turn them into null. IDs/CSR offsets/source indices remain integers.

The integrated harness appends `caseId`, `inputFileSha256` (literal saved-file bytes) and `semanticInputSha256` (canonical envelope with domain `m31-moving-admission/input/v1`, case ID and raw input). Those provenance labels are not mathematical/oracle inputs to the native query. The two hashes have different meanings and are independently checked. The wrapper does not invent another raw-input digest. The harness supplies source/runtime/input manifest metadata separately. This paragraph clarifies the originally drafted generic hash name before integration or execution; no wrapper code changed.

Wire schema `m31-native-load-evidence-v1` contains:

| Field | Meaning |
|---|---|
| model | `ordinary-binary64-full-contribution` |
| status,reason,method | native outcome, refusal reason or null, F/L |
| ids | canonical ascending stable IDs |
| raw | `{id,state:[17 words]}` records, or null before a complete validated copy |
| constants | mg,arm,radius,rho,A,R,D,decay,spread,origin,minDown,neighbor,nearRad,downFade,downCut,radFade,radCut,induced,kappa, each a word |
| prepared | `{id,center,axis,offsets,points,forces,nativeTotal,nativeBeta,nativeNu}` words |
| coefficients | `{offsets,sourceIndices,K,a}`; row index4*i+r, source indices index canonical ids |
| solution | success-only `{id,y,rotors:[{alpha,x,T}]}` words |
| loads | success-only `{id,rotor,collective,worldForce,worldMoment}` words; these actual delivered values are authoritative |
| diagnostics | native admission/input/graph/screen/counts, residual/work and successful schedule/phase diagnostics |
| timing,consumption | wrapper timer and all-load-word consumption record |
| stage | failure-only current phase |

When a native build returned before a refusal, its prepared/CSR evidence is retained. A throw during construction may leave no completed q; the status/reason, available canonical raw input and stage still return. No candidate load is fabricated for a failed query. A failed raw capture currently returns `raw:null`; the separately pinned harness input remains authoritative. Ordinary result arrays are owned by this query; output fields may reference other owned output storage, but none reference caller-owned arrays or buffers.

Statuses are `native-success`, `input-refused`, `domain-refused`, `numerical-failure`, `resource-failure` and `internal-failure`. These are native statuses only. The independent checker must retain separate exact-reference admitted/rejected/unresolved and four-category accuracy results. Unexpected exceptions become internal-failure; inherited positive cap and cooperative guard become resource-failure. A JavaScript RangeError becomes resource-failure/native-range-error, conservatively marking unsuccessful execution; this cannot distinguish every possible range/allocation cause. Fatal process termination or uncatchable out-of-memory remains a harness failure, not an in-process status.

## Prospective controls and limitations

The24 additional controls are fixed literals with at most two drones each. They cover canonical ID association, duplicate/unsafe/negative-zero IDs, strict shape/hole/empty input, nonfinite unused fields, nonpositive/huge/subnormal forces, native geometry/near/order refusal, active all-four support, exact neighbor/down cutoffs and a fixed adjacent below-cutoff word, projection zero, and tilted/unequal/canceling loads. All are single F calls. Expectations are prospective source requirements, not measured results.

`evaluateControl` verifies each expected status. Every native-success result must report canonical IDs, consume11 load words and1 ID word per drone plus the14-character success status, and return the linear native f*x force words. Additional assertions check active support/ratios, cutoff support, association, subnormal words, and analytic isolated/tilted/canceling loads. The three analytic load controls use a predeclared absolute1e-14 arithmetic tolerance in physical units. This control tolerance does not replace the four primary normalized1e-8 offline reference gates.

The unchanged48 inherited controls should continue to exercise the **vendor builders**, with full symbols and their original admitted-and-descending solve policy. Early wrapper rejection intentionally prevents access to the same screen metadata on some malformed/nonfinite cases. Therefore these48 are not silently reinterpreted as wrapper-status controls. The six inherited ownership definitions also stay at builder level, retaining the planes66 outputs as in the historical harness. The new controller must check actual input nonmutation and result storage independence around wrapper target/control calls; definitions alone are not execution evidence.

This bounded set is not exhaustive boundary coverage, and maxN5000 is an API guard, not a scale or deadline claim. No large positive-cap orN5001 fixture is included in the <=4-drone microcontrol allowance. Extreme mathematical inputs can be refused by the native range guards; no clipping or alternate solver repairs a failure. Native positive support can disagree with exact reference support near rounding/underflow boundaries; saved CSR and preparation make that discrepancy visible offline. All attempts must remain in the reported denominator.

No fresh input generator/seed/target selection, new numerical allocation, oracle import, exact online certificate or changed historical result is part of this draft.
