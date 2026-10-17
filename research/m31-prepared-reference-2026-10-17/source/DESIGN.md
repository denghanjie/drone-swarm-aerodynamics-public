# Prepared exact-reference adapter

Source-only implementation. No module import, fixture, oracle, reference, checker,
or browser execution was performed while authoring this module. The parent owns
the reviewed source freeze, public preregistration, allocation, execution, saved
baseline equality, and result claims.

## Entry points

```python
target, reuse_counters, binding_reports = regenerate_scene(
    scene, spec, constant_bits, original, semantic, tree,
    guard=None, budget=None, run_controls=False)
```

`original` provides the frozen pair methods, optionally through the existing raw
word literal adapter. Its `literal` must match the scene's encoding; all other
arithmetic methods must remain frozen. `semantic` and `tree` are the verified
frozen semantic module and qualified tree dispatcher. They are supplied by the
caller, never imported by this module. The caller verifies source/runtime/spec
and input pins before scientific imports. Declared source pins are:

- Pair: `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0`.
- Semantic: `ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c`.
- Tree dispatcher: `d08efc5e80910066d061a664aa7902c7ae7bab27dc710f5c00c9b2bf1671df65`.

The tree function is called unchanged. Its preparation, proof, traversal,
coverage, scalar-record order, outcome precedence, coefficient quantization,
roots, and signed loads remain its responsibility. The returned `target` has no
new scientific fields; existing `coverage.work` counts retain their exact meaning.
The parent can serialize with the previous `run.wire` and compare the entire JSON
record to the pinned saved tree output. No frozen module globals are patched.

`budget` may be the parent's shared dictionary
`{'oracleCalls': 0, 'limit': 30000}`. The adapter checks the current nonnegative
integer count/limit, then increments immediately before each suffix execution.
It cannot rely on an outer `original.oracle_case` proxy because it intentionally
bypasses that function. Counts include attempted suffix calls even if the suffix
raises. Failed binding controls do not execute the suffix or spend this budget.
Administrative `guard` polls occur at preparation, validation, and scalar entry,
in addition to unchanged tree polls. All administrative and binding exceptions
propagate; none becomes a scientific zero/refusal/uncertain result. The parent
must enforce its independent wall/output/window controls.

The exact counter fields are:

| Counter | Meaning |
| --- | --- |
| `prepareOneCalls` | Actual calls to the original scene preparation function. Raw refusals are excluded. |
| `preparationValidCalls` | Actual calls to original geometry/preparation validation. |
| `oracleCalls` | Actual prepared suffix entries, including a suffix that subsequently raises. |
| `operandLookups` | Registry lookup attempts, in receiver then source order. Successful science has exactly twice `oracleCalls`. |
| `pairPreparations` | Zero: the suffix has no preparation operation; any new registration after evaluation begins is refused. |

Counters are copied immediately after the successful scene calculation, before
optional controls. Control reports retain their own deltas, so failed lookups do
not contaminate scientific counts. The legacy logical `preparationCalls` need not
equal `prepareOneCalls`: the former includes raw-invalid rows by convention.

## Trusted internal adapter contract

The public factory is `PreparedHelper(original, constant_bits, corners,
guard=None, budget=None)`. It delegates unchanged methods except
`prepare_one`, `preparation_valid`, `exact_vector`, and `oracle_case`, and provides
`close()`. It is intended for one synchronous scene, not as a general external
prepared-pair validation API or a thread-safe shared cache.

The factory snapshots every constant word and the entire corner structure with
type-sensitive snapshots, and constructs the exact constant operands once. Every
registration and scalar call checks both the live bound context and the supplied
context against these snapshots. Mutation of the exact constant map is also
detected. Equivalent independently copied context values are allowed; different
words or corner order are not.

`prepare_one` verifies all 17 raw integer words, finiteness, and positive nominal
forces once, then invokes the frozen binary64 preparation function. These checks
also prevent direct factory users from bypassing the raw prefix. The tree's own
raw checks still run first and produce its original scientific refusal. The
adapter's guard errors are internal API errors, not alternative scientific
outcomes. A pending entry records the returned object identity and all fields.

`preparation_valid` requires that exact pending object, unchanged contents, raw
key, and exact constant context; it calls the frozen validator. Only true results
are registered. The cache key contains all 17 canonical raw words, including
velocity/angular velocity words and signed-zero bits, even though the scalar
geometry uses only some fields. The registry stores every returned prepared
object for duplicate raw rows; scalar lookup checks all their snapshots, so
mutation of an earlier duplicate cannot be hidden by a later equivalent row.

All cached vectors are obtained through the frozen `exact_vector` after validation:
center, axis, forces, four points, and four offsets. Offsets are needed by
`semantic.prepared_exact` for signed moments. Equal word tuples can share one exact
tuple. No new square root, profile, beta/nu, or positive arithmetic runs during
registration. Actual prepared axes and rounded points are preserved.

The first scalar call seals registration. It requires no unfinished preparation,
looks up both canonical raw rows, checks all registered prepared objects against
their saved contents, and only then enters the suffix. An unregistered row,
mutated prepared object, changed context, or closed adapter is an error. The
wrapper always closes its adapter in `finally`; the factory must likewise be
closed by direct users. The runtime is synchronous; arbitrary mutation of private
registry internals or concurrent callers is outside this trusted internal API.

## Exact suffix boundary

The suffix begins at the frozen pair oracle's `if case['input']['self']` branch,
immediately after successful raw/preparation validation, and ends at the original
positive return. Its source text is copied literally. Local aliases bind the
frozen `dot`, `require`, `fade_exact`, `sqrt_enclosure`, `positive_product`,
`dyadic`, and `parse_bits`; `Fraction` is the standard-library exact type. Only
`exact_vector` resolves a prevalidated word tuple to its cached exact value.

The self branch and all scalar guard/zero/refusal priorities remain unchanged.
The result retains `id,input,prepared,status,branch` and every original
`referenceIntervals` component where the branch returns it: `K,scaledK,beta,nu`
and `coefficient`. Scalar preparation evidence points to the same validated
prepared objects, with the original list/string schema. No eager normalizer
cache, center-predicate sharing, extra precision, reassociation, unit-axis
simplification, or alternate root algorithm is introduced.

## Six fixed live-context controls

Set `run_controls=True` only for `dense-cube-27`. The wrapper runs controls after
the valid target is complete, snapshots scientific counters first, and then
closes the context. All witnesses are fixed receiver ID100/input index0, source
ID101/input index1, rotor0. There is no setup re-preparation and no witness search.
Missing identities or an unexpectedly registered changed raw row fail setup.

| Report ID | Fixed mutation | Required reason |
| --- | --- | --- |
| `unregistered-receiver` | Replace raw receiver center-x word by exact1 (`3ff0000000000000`). Require that complete changed row is absent. | `prepared-unregistered-receiver` |
| `unregistered-source` | Replace raw source center-x word by exact2 (`4000000000000000`). Require that complete changed row is absent. | `prepared-unregistered-source` |
| `mutated-prepared-center` | Temporarily replace registered receiver prepared center-x by exact1; restore with `finally` and check restoration. | `prepared-operand-mutated` |
| `changed-constant-word` | Pass a copied constant map with the low bit of `mg` flipped. | `prepared-constants-context` |
| `changed-corner-order` | Pass copied corners with rows0/1 swapped. | `prepared-corners-context` |
| `closed-context` | Close this live context and attempt its original pair. | `prepared-context-closed` |

Each report contains `id,scene,detected,expectedReason,reason,reuseCounterDelta,
budgetOracleDelta,setupPreparationCalls`. Detection requires the precise
`BindingError` reason and zero suffix calls. Unexpected exception types propagate.
An unexpectedly accepted mutation remains an actually counted suffix attempt and
a failed control; no replacement is selected. Raw/constant/corner mutations use
copies. The only mutation of a target prepared object is restored before return.
These six controls differ from the six previously executed tree coverage controls,
whose evidence remains retained and must not be reported as newly executed here.

## Qualification boundary

AST parsing and literal suffix comparison are source checks only. Parent
qualification must bind the reviewed bytes, use all 24 existing inputs once,
require complete scientific wire equality to the saved tree records, compare
actual counts, and require every new control. The source does not import or run
the old full oracle for scene comparison. Any separately included arithmetic,
native, or load corruption checks must be explicitly allocated. A pass is a
finite regression qualification of prepared reuse, not a new sample, speedup,
5,000-drone exact error guarantee, physical validation, or cap authorization.
