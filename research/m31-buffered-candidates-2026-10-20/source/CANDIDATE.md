# Source-only buffered source-ID candidate

20 October 2026. Implementation only: none of these modules has been imported or executed during development. No fixture, scientific query, control or timing was run. Qualification requires the parent's separate prospective protocol, independent review, exact source freeze and public verification.

## Entry point and ownership

Use source/candidate.cjs, whose supported API is:

```js
query(input, method = 'F', guard = () => {})
encodeEvidence(result)
reset()
cacheStats()
witness()
cacheLimits
limits
```

Input and complete result/evidence schemas are the original native-load schemas. Call `query(input, 'F', guard)` for this candidate. The reported method remains `F`; distinguish experiment arms in the external harness envelope. The optional original `L` route remains delegated unchanged and does not consume the candidate enumerator. `reset()` discards the private candidate cache and resets its counters. `cacheStats()` returns an independent scalar/metadata snapshot; it exposes no mutable cached arrays. Call it after each query, outside the chosen scientific result comparison, and record whether its collection is inside the parent's wall-timing boundary. `witness()` returns owned copies of the existing source IDs, flat stored box endpoints and source-ID rows, plus entry count/last action; it performs no classification, geometry or rebuild. Its box layout is six numbers per canonical ID: xLo,xHi,yLo,yHi,zLo,zHi. Serialize these finite endpoints as binary64 words if exact sign-bit preservation is needed. The parent intends witnesses only for controls and the first measured candidate stream, outside query timing. Mutating the returned arrays cannot mutate the cache.

candidate.cjs differs from the native-load wrapper only in its kernel import, passing canonical current IDs to the builder, and adding cache API exports. candidate-kernel.cjs is a minimal fork of the F kernel. Its original anchor-kernel, lean-anchor and reference-excerpt dependencies are imported by relative path from the unchanged `m31-native-fresh-transfer-2026-10-17/source/vendor` directory, exactly the parent's baseline lineage. Static byte comparison confirms that the older native-load-baseline wrapper/kernel and these three dependencies match the fresh-transfer files; the actual imports nevertheless use fresh-transfer explicitly. The only modified F work is source enumeration. candidate-cache.cjs retains the exact canonical ID vector, finite reference boxes and ascending canonical-index rows, plus work counters. The public witness resolves those indices back to source IDs outside query timing. It retains no attitude, rotor position, force, coefficient, admission, graph, normalizer, solve or load value.

Every query still validates and owns all 17 current input words per drone, canonicalizes IDs, freshly prepares geometry and forces, evaluates the current global screen, applies the unchanged current component and center-distance tests to every enumerated source, assembles current coefficients, schedules, solves, checks the residual, materializes all four loads and consumes their ID/status/word checksum. Mutable inputs are copied by the inherited wrapper. The supported lifecycle is synchronous and non-reentrant; guards must be ordinary resource guards, not recursive queries or resets.

## Stored binary64 boxes and completeness

For each coordinate of each reference center, build the actual stored endpoints

```text
lo = nextDown(RN(center - 0.125))
hi = nextUp  (RN(center + 0.125))
```

`nextDown`/`nextUp` move one binary64 word outward. Cache eligibility requires finite current coordinates with absolute value at most 2**20; otherwise the query uses full current F enumeration. Finite, ordered endpoints containing the reference coordinate are checked explicitly. Reuse requires the same count and exact canonical ID vector, and every current coordinate to satisfy its stored inclusive `lo <= value <= hi`. A box exit causes a complete rebuild anchored on current centers. This condition is displacement-triggered containment, not a rounded Euclidean-displacement estimate.

For receiver i and source j, omit j from i's row only if at least one axis satisfies

```text
RN(source.lo - receiver.hi) >= 4
or
RN(source.hi - receiver.lo) <= -4.
```

For any represented current coordinates s and r within those stored intervals, monotonicity gives the real ordering `source.lo - receiver.hi <= s-r <= source.hi - receiver.lo`. Monotonic rounding of binary64 subtraction therefore bounds the exact operation used by F:

```text
RN(source.lo - receiver.hi) <= RN(s-r)
RN(s-r) <= RN(source.hi - receiver.lo).
```

Thus an omitted source necessarily satisfies F's existing `max(abs(dx),abs(dy),abs(dz)) >= 4` screen at every reusable current query. Equality is screened out by F. No omitted source reaches F's center norm or rotor classifier. Outward endpoint padding can add candidates but cannot remove a necessary one. The bounded coordinates make the endpoint operations finite and conservatively limit the cache's domain; the proof uses actual stored endpoints, so it does not assume that subtracting two nominal displacement bounds is exact.

Every nonself source not proven screen-rejected is retained. Rows are built in canonical source-ID order and internally store the corresponding canonical indices, not caller row positions. The entire canonical ID vector is retained and checked on every reuse. Any count/ID change invalidates and rebuilds the entire list before an index can be used; mere input-row permutation is already normalized by the original wrapper. The kernel reads these indices directly, without rebuilding a Map or looking up a source ID per pair. The public `witness().rows` schema remains ascending actual source IDs, resolved from the retained vector while copying the witness outside query timing. This representation-only change preserves the same candidate set, order, completeness proof and F arithmetic order. It was made before freeze or any native execution; it does not introduce a second variant. Default screened-out symbols remain unchanged.

The current global screen is evaluated before any cache use. If it is ineligible, the cache is discarded and F's original lean fallback executes unchanged, including its current preparation/guards. If the cache's absolute-coordinate, identity, box or resource conditions cannot be satisfied, its return is null and the same current F all-pairs enumeration runs. There is no approximate truncation. A 2,000,000-entry cache cap bounds retained canonical-index rows; encountering the cap discards the partial build and falls back. A cooperative interruption never publishes a partial rebuilt cache. Scientific positive-term limits are inherited separately and unchanged.

## Result comparison and work accounting

Expected complete F output equivalence excludes only these enumerator/timing fields:

- `timing`;
- `diagnostics.buildPhasesMs`;
- `diagnostics.geometryWork.gatheredNonselfCandidates`;
- `diagnostics.screen.orderedPairVisits` and `diagnostics.screen.componentTests`.

All other result fields, including failure status/reason/stage where applicable, raw/current prepared evidence, constants, coefficient indices and binary64 words, symbols/counts, graph/admission, current center-norm counts, schedule/solve/residual work, solution/load words and consumption checksum, remain comparison targets. In particular, `certifiedSkippedPairs` still counts logical pairs minus actual center-norm calls and is not permission to skip its comparison. Do not remove the whole diagnostics object to force equality. Resource-guard interruption timing is operational behavior, not a guarantee of identical interruption position between differently instrumented implementations.

`cacheStats()` reports totals `queries`, `builds`, `reuses`, `fallbacks`, `invalidations`, `identityRebuilds`, `boxExitRebuilds`, `buildOrderedPairs`, `buildAxisIntervalTests` and `containmentCoordinateTests`, plus cached size and `last: {action, reason, n, candidateEntries}`. Enumerator `queries` counts reached F cache decisions, including global-screen bypass; an input refusal before the build or an `L` call does not increment it. Reasons include cold, count-change, id-change, box-exit, global-screen-ineligible, absolute-coordinate-bound and candidate-entry-cap. A guarded unfinished build can retain `action: building`; that is not a successful cache publication.

Cold/rebuild construction still scans ordered pairs and can cost more than F. Reuse still charges current global predicates, owned input/preparation, exact canonical-ID/box checks, candidate-index traversal and every current scientific operation. The fork's build geometry phase includes cache work; total query timing also includes input processing and the complete inherited result. No timing is subtracted or claimed here. This proposes amortized enumeration reuse, not a proof of speedup or reduced aerodynamic arithmetic.

## Small prospective qualification and limits

The parent plans one fixed eight-query 1,000-drone stream with per-ID signed x/y displacements 0, .02, .04, .06, .08, .10, .30, .32, unchanged z and deliberately changing current forces. Compare each reached candidate output to current F under the explicit field exclusions above, preserving cold/rebuild costs and all saved states. Early movement is intended to exercise containment reuse and the .30 transition a rebuild; actual actions must be recorded, not inferred as observed. Stable-ID permutation, replacement/count change, component-boundary words, stored-box boundary/exit, current force/attitude refresh and global/absolute-coordinate fallback are distinct control targets for the parent's bounded protocol. This document adds no calls or execution budget.

The binary64-box argument establishes candidate completeness relative to F's existing screen. It does not prove F versus a mathematical all-pairs model on arbitrary runtimes, improve its physical validity, establish continuous-time validity between queries or qualify a 5,000-drone deployment. Math.hypot/other inherited arithmetic retain the same pinned-runtime limitations. Cache ownership is per loaded CommonJS module instance; concurrent workloads require separate instances/processes or an explicit lifecycle. Historical sources are unchanged.
