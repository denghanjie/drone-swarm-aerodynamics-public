# Producer-side single-state draft

This package is source-only. No initializer, native query, layout codec, browser bundle, browser, checker or numerical reference was executed by the producer author. The bundle-building script was written but not invoked, and no results directory was created. Current-window scientific execution is outside this task; a later launch requires the parent's separate review/publication/authorization gates and the independent checker and supervisor.

## Fixed state and record contract

The science configuration schema is `m31-native-tree-state1000-science-v1`. There is exactly one case:

```
{caseId:"tree-t0-n1000-a", n:1000, seed:2026101741,
 methodOrders:[["F","H0","H"]]}
```

The same case label is used by the earlier source family, but the new package and fixed seed identify this prospective state. No earlier exposed state is relabelled as this input. The producer calls the unchanged `S.initial(seed,n)` once, records every original state word, runs the unchanged t0 controller once, and passes that original state and its actual commands into one `adapter.evaluate` call.

The evaluation context has arm `coupled`, stepIndex 0, stageIndex 1, original/relative time 0, dt 0, and stageId `tree-t0-n1000-a-step0-k1`. The inherited k1 label identifies the single derivative record; no RK step follows. Configuration has `steps:0`, `stagesPerStep:1`, `duration:0`, `timeOrigin:0`, `dt:0`, `controlDt:0.01` and `stepsPerControl:4`. The adapter no longer defines or exports `step`, and the driver has no safety/endpoint/RK continuation path.

For the fresh case, raw initialization is projected once with the unchanged quaternion arithmetic. The resulting canonical words are independently decoded/copied for the three methods in the fixed order F, H0, H. All three successful full native results must agree on the inherited exact semantic fields before H loads are bound to the actual projected IDs/input and consumed in one whole-swarm derivative evaluation. The 1,000 derivative rows retain every input, command, load, frame, motor and derivative word. Fixed wiring-control derivative fixtures are separate infrastructure controls, not additional fresh swarm evaluations.

The complete successful journal has exactly 22 entries:

| Sequence | Kind | Count |
| --- | --- | ---: |
| 0 | source | 1 |
| 1 | factories | 1 |
| 2–13 | wiring-control | 12 |
| 14 | initial | 1 |
| 15 | controller | 1 |
| 16–18 | native, F/H0/H | 3 |
| 19 | stage | 1 |
| 20 | case-summary | 1 |
| 21 | driver-summary | 1 |

Source/factory/wiring/initial/controller/native/stage schemas and their existing evidence fields are retained. Native references remain `{method,recordPin}` and bind all three complete native descriptors. `stage.rawBeforeProjection` derives directly from `initial.input`; `stage.commandsBeforeEvaluation` derives directly from the controller's actual command arrays. The case summary retains schema `m31-tree-browser-case-summary-v1` and reports `completedSteps:0`, `completedStates:1`, its stageId, 1,000 derivative records, and diagnostic initialization/controller/case wall times. The driver summary retains its old schema and reports one case, reference acceptance `not-in-scope`, and qualification not established by the producer.

Exact producer runtime counts are `{coupledStages:1,coupledCompleted:1,primaryNativeCalls:3,steps:0,controllers:1,initials:1,safetyChecks:0,wiringControls:12}`. No second stage, integrated endpoint, safety continuation or state advancement is emitted.

## Qualified layout integration and timing

The actual compact tree capture inside `nativeTree.query` is unchanged. After each actual native result is encoded to the original complete evidence shape, the producer applies the qualified `layout.encode` to a present tree and then `layout.decode`. Exact logical equality with the original compact tree is required, including ordered arrays and literal words. Semantic comparison receives the reconstructed compact tree together with the unchanged actual non-tree fields. Persistence receives the same non-tree fields with only `tree` replaced by the columnar representation. An absent tree remains absent; explicit null remains null.

All raw/prepared words, diagnostics, CSR offsets/source indices/K/a, complete solution/load evidence, consumption, IDs/status and input-binding hashes remain present. The layout does not infer an H or H0 witness from F, omit cull differences or gathered membership, change the native result, or substitute a boolean for saved arrays. Host storage may share actual encoded bytes only under its separately reviewed exact-byte comparison and budget contract.

Timing fields preserve their earlier scope and add explicit layout costs:

- `queryWallMs`: independent input-word decoding/copy, unchanged native query and normal load/ID/status consumption, plus actual submitted-input preservation check. Existing compact tree capture remains inside this timer.
- `encodeWallMs`: original `native.encodeEvidence` only.
- `layoutEncodeWallMs`: conversion of the actual encoded tree to columns.
- `layoutRoundtripWallMs`: reconstruction and exact logical tree comparison.
- `semanticCompareWallMs`: inherited full native semantic comparison after reconstruction.
- Append/serialization/transfer/persistence fields retain their earlier separately reported scopes.

The two layout fields appear in each stage query-timing row and the corresponding native `auditTiming` record. They are zero when no tree property is present. Layout conversion, roundtrip and transport remain inside browser/overall wall budgets even though they are outside native query timing. This single-state draft contains no speed acceptance gate or standalone frame-time claim.

## Source identity, controls and dependency graph

Read-only source-byte comparisons established that new `compact-codec.cjs`, `tree.cjs` and `native-tree.cjs` exactly match the frozen browser-probe versions. The new `layout.cjs` exactly matches the successfully qualified saved-layout version. New transport code differs from the earlier transport only in the canonical output shard-directory prefix.

The adapter's word utilities/projection and its `nominalLoad`, `bind` and `consume` function bodies remain text-identical. The changes are the top-level pure layout dependency, explicit layout encoding/roundtrip around evidence persistence, separate timing fields, and removal of the unused RK step implementation. No native arithmetic, tree split/predicate/traversal/sort rule, guard site, numerical tolerance or positive-term limit is changed.

The driver's complete wiring-control and controller function bodies remain text-identical to the earlier browser probe. All twelve unchanged wiring controls and their frozen fixtures remain in the parent's science configuration. The browser's Buffer adapter and its nine groups/56 assertions are also text-identical. These are compatibility and wiring controls, not new numerical reference evidence; the earlier stated NaN-payload/general-Buffer limitations remain.

The bundle allowlist has 19 factories. Its 12 unchanged dependencies are under `research/m31-native-fresh-transfer-2026-10-17/source/`: native-load; vendor reference-excerpt/anchor-kernel/lean-anchor/kernel; physics; and sim/grid/geometry/factory/factory-wide/wall-filter. The seven local factories are transport, compact-codec, tree, native-tree, layout, browser-adapter and browser-driver. Browser and builder allowlists were parsed as source data and found equal; no factory was evaluated for that comparison.

The loader retains source-slice and complete-bundle hashing before any factory executes, the 2 MiB bundle limit, the local wide-factory process shim, and unchanged global Buffer/process behavior. Layout is required at adapter module initialization, so the `factories` record's execution order is the prior order with layout immediately after browser-adapter and before physics; all 19 factories are loaded before that record. The bundle's source-list order is separately fixed by the matching browser/builder allowlists.

The public invocation remains `window.runNativeTreeProbe(payload)`, with unchanged host bindings `__storeTreeShard` and `__appendTreeRecord`. All local paths use the new state1000 package. `build-bundle.py` remains an exclusive source-byte packager and must be reviewed and run separately by the parent. Its output metadata pins every exact source slice; it never imports or evaluates the source modules.

## Failure and claim boundaries

The driver and adapter preserve the earlier terminal failure behavior. Input mutation, non-success results, layout mismatch, semantic mismatch, malformed response, derivative failure or persistence failure prevents successful completion. A failed append cannot become a complete failure record. Original failure snapshots are retained without a new truncation rule; complete malformed/failure evidence is not guaranteed to fit. All successful and partial bytes remain subject to the fixed transport, storage and supervisor limits, and an incomplete prefix is not accepted as qualification.

The storage-admission document must distinguish a bound for complete successful bodies from an assumption about arbitrary malformed snapshots or orphan chunks. No native admission limit or storage cap is weakened to handle failure, and no retry or alternative seed is introduced.

The intended future checker scope is complete N1000 three-arm equivalence, saved cull/gather correctness and one derivative's binding/arithmetic, conditional on the retained source/model assumptions. This producer alone does not establish any of those results. There is no high-precision-reference computation or claim in this source draft, and the one-state scope cannot establish an RK trajectory, safety continuation, future N5000 performance or a complete larger experiment's fit.
