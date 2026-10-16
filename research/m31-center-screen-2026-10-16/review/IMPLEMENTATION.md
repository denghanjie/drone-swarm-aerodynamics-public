# Center-screen candidate and fixed controls

Prepared 2026-10-16 for `research/m31-center-screen-2026-10-16/PROTOCOL.md` and `config.json`. Status: isolated static source preparation only. No candidate/control module was imported or evaluated, no control was materialized, and no scientific run or benchmark occurred. The inherited exposure disclosure remains applicable: the earlier contract review opened an existing result-bearing arithmetic file. This source preparation does not erase that disclosure or claim an unexposed design process.

## Files and pins

- `lean-anchor.cjs`: unchanged copy of `research/m31-typed-assembly-2026-10-16/source/kernel.cjs`; SHA256 `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96`.
- `kernel.cjs`: candidate copied from that source and patched only at the screen predicate, center-norm path, explicit metadata, mode dispatch and F wrapper. SHA256 `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8`.
- `controls.cjs`: retains the original 24 positional definitions and adds 24 fixed definitions; SHA256 `bf54381ee7f4dab8fbb19e48ada7e11c0f6d129cec1bcd21e5ce5075fc91f1ba`. The original controls source SHA256 was `2b228b5d24542979896d25805265923d82468394a6d607d11c4e8c6449de028b`.

The parent must copy and pin the unchanged `anchor-kernel.cjs` and `reference-excerpt.cjs` dependencies before integration. No dependency path is replaced by a live remote or external source. This note creates no numerical allocation.

## Callable interface and fallback

`build(states, 'lean', fullSymbols, guard)` and `query(states, 'L', guard)` delegate directly to the unchanged `lean-anchor.cjs`. Existing non-F modes/labels also delegate to it. `build(states, 'screen', fullSymbols, guard)` and `query(states, 'F', guard)` expose the candidate. The original exported constants, schedule, fullGraph, solve, residual, cached and checksum functions remain the inherited anchor functions.

F first performs the unchanged current-state preparation. Its predicate reads only the prepared position components in `p`: per-axis `Math.min`/`Math.max` accumulate every coordinate, rounded spans are `max-min`, and eligibility requires all coordinates finite and every span finite and in `[0,256]`. Quaternion, nominal and other input diagnostics are still prepared and preserved; position eligibility does not imply model admission.

If ineligible, F calls the unchanged `lean.build(...,'lean',...)` for the entire evaluation. It does not selectively screen invalid coordinates or keep any partly screened rows. This intentionally repeats preparation on fallback: the candidate pays its first preparation/predicate and the full delegated lean build. The returned model data are those of the delegated build, with separate screen metadata attached.

If eligible, F retains the original receiver/source/rotor traversal and computes the same center differences. It skips the center norm only when `Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz)) >= 4`. Such entries retain the preinitialized symbol `1`. All other pairs execute the original center norm, original invalid guards, strict neighborhood cutoff, rotor branch/arithmetic order, ordinary storage, scaling and dependency construction. Solve/residual and consumption remain unchanged. `assemblyStats.mode` remains `lean`, accurately describing the unchanged ordinary assembly mechanism.

This is a finite pinned-runtime empirical intervention. It carries no universal JavaScript `Math.hypot` equivalence guarantee. Qualification must independently compare every inferred omission with the corresponding L symbol entries. Invalid and near-field outputs must remain visible; no expected screen eligibility is an assertion that a control is physically/model-admitted.

## Screen record and work counters

Only F returns `q.screen`, with schema `m31-center-screen-work-v1`:

| Field | Definition |
|---|---|
| `finiteRuntimeOnly` | Always `true`. |
| `runtimeGeneralEquivalenceProven` | Always `false`. |
| `historicalCertifiedSkippedPairsIsFormalProof` | Always `false`; disambiguates the inherited counter name. |
| `spanLimit`, `componentThreshold` | Fixed `256` and `4`. |
| `coordinateFinite`, `spanFinite` | Recorded results of the complete coordinate/span predicate. |
| `min`, `max`, `spans` | Fresh per-call arrays, including special-number values when present. |
| `eligible`, `fallback` | Predicate result and its negation. |
| `fallbackReason` | `null` if eligible; otherwise priority order `coordinate-nonfinite`, `span-nonfinite`, `span-out-of-range`. |
| `orderedPairVisits` | `geometryWork.gatheredNonselfCandidates`; all ordered nonself pairs remain visited. |
| `componentTests` | All visited pairs on an eligible scene; zero on full fallback. |
| `skippedCenterNormCalls` | `geometryWork.certifiedSkippedPairs`; a work count, not formal certification. |
| `actualCenterNormCalls` | `geometryWork.directedCenterTests`, incremented immediately before each actual center norm. |
| `omissionEvidence` | Literal `reconstruct-from-saved-current-positions-and-frozen-predicate`. |

The original `geometryWork.logicalDirectedPairs` and gathered count retain their semantics. Its historical `certifiedSkippedPairs` expression remains logical pairs minus actual center tests; the new screen record explicitly limits its interpretation. F makes no claim to enumerate fewer pairs. There is no new dense skipped-pair mask or list. The saved complete current states, frozen predicate, screen counts and complete L/F symbol tensors are the evidence: reconstruct the directed skip predicate independently and require all four L symbols to be exactly `1` at every inferred skipped pair.

Across L/F, normalize only the intended differences: `screen`, timing/phase values, and `geometryWork.directedCenterTests` / `geometryWork.certifiedSkippedPairs`. Independently verify those work fields instead of discarding them. All other geometry counters, coefficient/support/order data, ordinary assembly records, original all-pairs certificate, input/admission and graph/solution outputs must remain exactly equal under the saved special-value encoding. The original `certificate` stays unchanged with `certified:null`; do not reinterpret it as the new predicate.

Eligible F includes the predicate in the existing `index` phase. F fallback adds `screenPreflight`, covering the first preparation/predicate before delegated L starts; the delegated original phases remain intact. Query total includes this overhead and final metadata construction. As before, the wrapper's remainder reconciles complete time and phase sums. Do not remove this overhead from F timing.

No input is written. The unchanged inherited `q.states` reference convention remains; the candidate introduces no new input alias. Returned coefficient, offset, geometry and screen arrays are freshly owned per call, and no cross-call scratch is introduced. Ownership checks must cover both original returned arrays and new screen arrays, including full fallback.

## Fixed control manifest

`controls()` returns position literals and optional `statePatches`. Materialize each state exactly as the original harness does: position, zero velocities, quaternion `[0,0,0,1]`, zero angular velocity and four `kernel.constants.mg/4` nominal motors. Then apply each patch `{vehicle,index,value}` to that freshly materialized state. Do not apply patches to shared originals. The driver saves complete state atoms with explicit `-0`, `NaN`, `Infinity` and `-Infinity` tokens; ordinary JSON-number serialization is insufficient.

The final count is **48 controls** in the following exact order, also exported as frozen `controlIds`:

```text
radius-0-below
radius-0-exact
radius-0-above
radius--6-below
radius--6-exact
radius--6-above
cell-below
cell-exact
cell-above
signed-zero
coarse-origin
coarse-translated
dense-16
span-256
span-nextUp256
far-invalid258
nonfinite-nan
nonfinite-infinity
overflow-span
near-field
duplicates
planes-62
planes-64
planes-66
component-x-below
component-x-exact
component-x-above
component-y-below
component-y-exact
component-y-above
component-z-below
component-z-exact
component-z-above
span-diagonal-256
span-nextDown256
center-257-fallback
center-nextUp257-fallback
mixed-near-far
mixed-positive-far
invalid-quaternion-far
nominal-zero-positive-far
nominal-negative-positive-far
nominal-nan-positive-far
scaled-cap-positive-far
invalid-quaternion-nan-far
nominal-infinity-positive-far
nominal-total-overflow-positive-far
nominal-unequal-positive-far
```

Every control includes `expectedScreenEligible` and `expectedFallbackReason`. Expected fallback controls are `span-nextUp256`, `far-invalid258`, `center-257-fallback`, `center-nextUp257-fallback` (`span-out-of-range`); `nonfinite-nan`, `nonfinite-infinity` (`coordinate-nonfinite`); and `overflow-span` (`span-nonfinite`). All others are expected position-eligible. In particular, invalid quaternion/nominal controls intentionally remain position-eligible, so the candidate must preserve their original admission diagnostics despite far-pair skips. The inherited `expectedGrid` field is retained only for the original definitions as provenance; it does not select a grid.

The added controls fix 4 m adjacent-binary64/exact boundaries on each axis; diagonal and next-down 256 m spans; 257/next-up guard-domain fallback; near/far and positive/far mixtures; nonunit/NaN quaternion input; zero, negative, NaN, infinity and overflowing-total nominal input; a high-positive nominal scaled-cap challenge; and unequal positive current nominal motors. These are prospective inputs and expected predicate classes, not observed pass results or a claim of comprehensive guard coverage.

## Ownership sequence and verification status

Exported `ownershipSequence` fixes **six additional builds**:

```text
L:sparse2
F:sparse2
L:planes62
F:planes62
L:fallback258
F:fallback258
```

`sparse2` is `[[0,0,0],[4,0,0]]`; `planes62` is the original `planes-62` definition; `fallback258` is `[[0,0,0],[258,0,0]]`. Each uses fresh default states. Retain both L/F `planes-66` control outputs across this sequence and compare before/after, check inputs unchanged, and check returned storage disjointness including new screen arrays. No overwrite-and-recompute ownership test is hidden in the count.

The source diff was inspected and the copied baseline hash matched its original. Initial plain `node --check` attempts found no `node` in the non-login PATH and executed no parser or module. Syntax parsing, if subsequently performed with the pinned runtime, must be recorded separately; numerical controls/qualification remain unrun until the parent completes the required freeze and verification.
