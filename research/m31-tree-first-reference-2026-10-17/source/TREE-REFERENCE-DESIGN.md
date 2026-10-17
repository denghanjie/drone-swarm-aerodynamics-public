# Tree-first exact scene reference: source design

Status: source implementation only. No fixture, scene reference, equality check,
coverage check, or timing run was executed while authoring this source. The parent
campaign owns source freezing, input selection, allocation, execution, independent
checking, publication, and any scientific claim.

## Interface and caller obligations

```python
target = regenerate_scene(scene, spec, constant_bits, helper, semantic, guard=None)
record = to_record(target, semantic)
```

Importing `tree-reference.py` imports only standard-library `re`; it does not load
any scientific module, allocate a campaign, evaluate an oracle, or write output.
The caller supplies verified frozen modules after its own source/runtime/allocation
gates. The module publishes these dependency paths and SHA-256 pins as constants:

| Dependency | SHA-256 |
| --- | --- |
| `research/m31-native-fresh-transfer-2026-10-17/source/pair-reference.py` | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `research/m31-native-fresh-transfer-2026-10-17/source/semantic-reference.py` | `ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c` |

These constants are declarations, not an internal file-verification mechanism.
The caller must verify dependency bytes, the candidate source, the input spec,
the constant words, and the corner order before import/use. `helper` is the frozen
pair module or a caller-verified adapter with the same methods. The existing
`RawWordHelper` adapter can admit saved raw binary64 words through `literal`
without changing `oracle_case`. `semantic` is the frozen semantic module.

The source requires `maxDrones` to be an integer in `[1,180]`, the actual scene
count not to exceed it, `leafCapacity == 8`, reference coefficient/source bits
`192/192`, root bisections `128`, and `positiveTermCap == 2000000`. The caller
supplies the adopted spec and constants; this interface does not create or mutate
them. `scene` retains the inherited exact field set `id,family,expectedClass,drones`;
each drone retains `id,state`, with 17 raw string literals/words and a unique
integer stable ID in `[0,65535]`.

`guard`, if supplied, is a zero-argument administrative poll. Polls occur at entry,
for each preparation, before global proof, for every receiver/rotor query and node
visit, before every residual scalar, and before/after the unchanged root routine.
Guard and helper exceptions propagate: there is no conversion to zero, admitted,
or reference-undecidable. A failed call returns no partial target. The root
routine, tree builder, and individual helper calls contain no new internal poll;
the parent must enforce an external process wall/CPU/resource guard.

## Preserved scientific operations

The scene preparation pass preserves raw-word parsing, binary64 preparation,
finite/positive-force checks, geometry validation, and all preparation records.
It completes every drone preparation before selecting the first invalid drone in
input order. A globally invalid scene returns the same refusal and stable-ID
witness without tree or pair work.

For valid preparations, geometry comes from the actual prepared words, including
near-unit axes and actual rotor points. The unchanged `global_guard` proves all
earlier magnitude guards before any node can be pruned. Failure of that proof
selects complete scalar fallback. No failed guard is interpreted as zero.

The unchanged deterministic tree uses largest exact coordinate span with xyz
tie order, coordinate/stable-ID sorting, a floor midpoint, leaf capacity eight,
preorder nodes, and left-first traversal. The inherited builder computes member
tuples once while constructing bounds. The dispatcher immediately discards those
tuples and never expands a proved-zero node's members during query traversal.

Every visited node uses the unchanged rational `zero_rule`, in inherited order:
`neighbor`, `upstream`, `down-cut`, `near-outside`, `radial`. Its exact residual is
`d - h * axis`; no unit-axis identity or rounded proxy is substituted. Successful
proofs emit one constant-size range terminal. An unresolved internal node descends;
an unresolved leaf evaluates its nonself sources with the unchanged
`helper.oracle_case`. Complete fallback uses that same scalar helper. Residual
scalar calls continue to parse and prepare both rows internally; this design does
not extract or replace prepared-pair arithmetic.

Positive coefficients receive the same single outward 192-bit quantization.
After traversal, evaluated pairs are sorted by original receiver input index,
rotor, and original source input index. Canonical outcome precedence remains:
first rejected pair, first reference-undecidable pair, first backward positive
ordering violation, positive-term budget, otherwise admitted. The receiver order
remains descending exact prepared center height with stable-ID ties. The unchanged
`reference_roots` reads only positive pairs, so omission of proved zeros preserves
its source order, independent 192-bit source boxes, 128 root bisections, and signed
rotor, collective, world-force, and world-moment load boxes.

## In-memory target

The target schema is `m31-tree-first-reference-scene-v1`. It contains:

```text
schema, id, input, prepared, exact, geometry, planned, pairs, order,
expectedClass, tree, globalGuard, guardEvidence, coverage, globalInvalid,
status, branch, witness, referenceClass
```

Admitted targets additionally contain `roots` and `loads` with the inherited
in-memory Fraction interval structures. `exact` is keyed by stable ID, and
`geometry` follows original input order. `planned` is always `4*N*(N-1)`, including
globally invalid scenes. For globally invalid scenes `geometry` is empty,
`tree/globalGuard/guardEvidence` are `None`, and `order/pairs` are empty.

Only actually evaluated scalar pairs appear in `pairs`:

```python
{
    'i': receiver_stable_id, 'r': rotor, 'j': source_stable_id,
    'ii': receiver_input_index, 'jj': source_input_index,
    'oracle': {'status': status, 'branch': branch},
    # present only for positive status:
    'coefficient': (lower_fraction, upper_fraction),
}
```

All evaluated zeros, rejections, and undecidable results remain in this list.
There is no dense `lookup`, complete `plans`, or per-member record for a zero node.
This target therefore must not be passed directly to the old `validate_assembly`,
which requires the old dense lookup/plans contract.

## Compact coverage schema

`coverage.schema` is `m31-tree-first-coverage-v1`:

```python
{
    'schema': 'm31-tree-first-coverage-v1',
    'mode': 'hierarchy' | 'fallback' | 'global-preparation',
    'complete': bool,
    'logicalPairs': 4 * N * (N - 1),
    'requiredCoveredPairs': 4 * N * (N - 1),  # zero for global-preparation
    'coveredPairs': integer,
    'permutation': [stable_ids],
    'queries': [query],
    'work': work_counts,
}
```

Hierarchy uses the exact tree permutation; fallback uses original input IDs.
Queries occur in original receiver input order, then rotor order `0,1,2,3`:

```python
{
    'i': receiver_input_index, 'id': receiver_stable_id, 'r': rotor,
    'selfPosition': receiver_position_in_permutation,
    'terminals': [terminal],
}
```

Each query's nonempty half-open terminal ranges partition `[0,N)` contiguously,
without overlap or gaps. A terminal count is
`end - start - int(start <= selfPosition < end)`. A range containing only the
receiver is allowed and has count zero. Self exclusion always uses permutation
position, never an assumption about stable-ID order.

```python
# Proved zero; no per-member indices or oracle branches are emitted.
{'kind': 'zero', 'node': node_id, 'start': start, 'end': end,
 'count': nonself_count, 'proofRule': rule}

# Unresolved tree leaf; all and only these scalars were evaluated.
{'kind': 'leaf', 'node': node_id, 'start': start, 'end': end,
 'count': scalar_count, 'sourceIndices': sorted_original_input_indices}

# Complete fallback, exactly one terminal per query.
{'kind': 'scan', 'node': None, 'start': 0, 'end': N,
 'count': N - 1, 'sourceIndices': sorted_original_input_indices}
```

`proofRule` states the node proof. It is not a fabricated scalar first-zero
branch: a group upstream proof can cover a member whose scalar oracle would stop
at neighbor. An independent checker must establish that each omitted nonself
member has scalar zero status, without requiring its branch to equal `proofRule`.
An independent small-scene checker may expand ranges; this production dispatcher
does not expand pruned ranges.

The source reconciles each query's contiguous cursor and count, all query counts,
and `zeroPairs + scalarPairs == planned`. `complete` is set only after traversal
and these checks succeed. For global preparation refusal, the schema explicitly
uses `mode='global-preparation'`, empty permutation/queries, zero required and
covered pairs, and `complete=True`; preparation invalidity discharges pair work
without claiming that logical pair queries were evaluated.

Work fields use the frozen semantic names:

| Field | Meaning |
| --- | --- |
| `preparationCalls` | Number of drone rows in the scene-level preparation pass. As in the inherited work convention, this excludes preparation inside residual `oracle_case` calls and includes raw refusals. |
| `globalProofs` | One for a valid-preparation scene, otherwise zero. |
| `treeNodes` | Constructed hierarchy node count; zero in fallback/global refusal. |
| `nodeVisits` | Number of query/node visits. |
| `nodeRuleTests` | Sum of `zero_rule`'s returned first-success index, or five on failure; this is the inherited logical-test counter, not a count of eager Python predicate evaluations. |
| `zeroNodes` | Number of successful zero terminals, including possible self-only ranges. |
| `zeroPairs` | Sum of their nonself counts. |
| `leafVisits` | Number of unresolved leaf terminals, including possible self-only leaves. |
| `scalarPairs` | Actual residual `oracle_case` calls. |
| `scalarZeroPairs` | Evaluated scalar zero outcomes. |
| `positiveTerms` | Evaluated scalar positive outcomes. |
| `rejectedPairs` | Evaluated scalar rejected outcomes. |
| `unresolvedPairs` | Evaluated scalar reference-undecidable outcomes. |

No counter purports to measure elapsed time or all internal helper operations.

## JSON record adapter and validation boundary

`to_record` evaluates no oracle. It returns the following JSON-ready fields:

```text
schema, id, input, prepared, expectedClass, referenceStatus, branch, witness,
referenceClass, globalInvalid, globalGuard, guardEvidence, order,
plannedPairs, evaluatedPairs, pairs, tree, coverage, loads, recipe
```

`referenceStatus` maps from target `status`; `plannedPairs` maps from `planned`.
Pair rows retain `i,r,j,ii,jj`, flatten `oracle` into `status,branch`, and encode
positive `coefficient` endpoints through frozen `interval_wire`. Guard evidence
uses frozen `fraction_wire`. Admitted load rows follow original input order:

```python
{'id': stable_id,
 'roots': [four_interval_wires],
 'loads': {'rotor': [four_interval_wires], 'collective': interval_wire,
           'force': [three_interval_wires], 'moment': [three_interval_wires]}}
```

Nonadmitted records have empty `loads`. The recipe is exactly
`{'coefficientBits':192,'sourceBits':192,'rootBisections':128}`. In-memory
`exact/geometry` are not serialized; the independent checker can reconstruct them
from raw/prepared words. This adapter does not deep-copy every nested structure;
the caller must treat returned targets/records as immutable while recording them.

The parent driver is responsible for provenance, source/input hashes, durable
writing, campaign budgets, and comparing against the frozen complete oracle. The
parent independent checker must verify dependency pins, tree/global-guard
equality, exact terminal traversal/ranges/self exclusion, scalar membership,
node proofs, omitted-member zero status, work counts, canonical pairs and
witnesses, positive coefficients, roots, and all signed load endpoints. Source
inspection and AST parsing alone do not establish those scientific equalities.
