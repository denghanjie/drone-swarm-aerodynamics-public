# Typed coefficient builder — independent static review

Date: 2026-10-16. Reviewer: m31_verified_literature.

**Verdict: no blocking source defect found in the inspected candidate. Adopt this
implementation for the coordinator's source-freeze review; runtime equivalence,
control coverage, practical benefit and scientific claims remain unresolved.**
This review does not authorize execution or certify a complete runner/reviewer.

The inspected intervention is stable typed sparse assembly, not a new arithmetic
kernel, SIMD method or novel algorithm. L and T share the known lean operations.
T/L compares the complete assembly package, including dependency construction;
it cannot isolate a row-storage, copy, Set/sort, allocation or GC effect.

## Scope and pins

Read source text only. No module import/evaluation, fixture construction, model
execution, target scoring, timing, raw-result recomputation or repository edit
was performed. Only this private review directory was written. File hashing and
ordinary text inspection are not scientific execution. The implementation
author reports a syntax-only parse; this reviewer did not repeat it.

Inspected isolated implementation directory:
`[isolated implementation directory]/`.

| File | SHA256 |
| --- | --- |
| kernel.cjs | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| anchor-kernel.cjs | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| reference-excerpt.cjs | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| README.md | `b4c405c26c81688c71bdb88deabe20cce4b45d3a5b9ae6b7e1202b68c18da51a` |

The isolated anchor/reference hashes equal the current closed coupled-cost
package's source hashes. The coordinator package inspected was
`research/m31-typed-assembly-2026-10-16/` in the checkpoint workspace. Its observed
document pins, which may change before final freeze, were:

| File | SHA256 |
| --- | --- |
| PROTOCOL.md | `52cbc9a307353b70e91f0a594cc70d7769ed53d75c04bac8dcb26a148deb5f3c` |
| SCHEMA.md | `a09cff6daaeeebfb867c0bbb0cb13e0ff0b0fd5751f4de2800c79867f9b2c306` |
| config.json | `41f4a5c7743f3647ffbcd34343f942e2b56ba1fefd895586e388830bf68cafd8` |

## Arithmetic, branches and failure progress

Preparation preserves the anchor's rotation expressions, typed geometry layout,
nominal slices, S0 reduction and input diagnostics. The candidate intentionally
does not substitute the earlier lean campaign's scalar rotation implementation.

For A, `query` delegates directly to the byte-pinned anchor; schedule, solver,
residual, graph-depth and checksum functions are the anchor exports. L and T use
one shared classifier and one shared query path, with the same original ordered
solver and residual. No scalar root or source-total coupling equation changed.

The all-pairs receiver/source/rotor traversal is preserved. Self pairs remain
symbol 1; invalid center checks still precede the strict neighbor skip. Center
differences, Math.hypot arguments and thresholds match the anchor. The candidate
computes each receiver's four world points once using exactly center+offset and
stores them in Float64 scratch. This retains each binary64 value and signed zero
for the ordinary numeric arrays in scope. It changes evaluation frequency, not
the expression or the scientific value; the private prepared array is not
mutated during the traversal.

The rotor differences, finite/range checks, down dot product, down comparisons,
radial Math.hypot, near-field test, half-width, support cutoff, xi, denominator,
normalized speed, fade calls and speed admission have the anchor's grouping and
branch order. Replacing the temporary `[dx,dy,dz].every(Number.isFinite)` with
three scalar finite predicates preserves the condition. No fast square root,
algebraic reassociation, additional support skip or approximation appears.

Projection is cached per receiver/source only when the first rotor reaches the
original projection branch. Its expression is unchanged, and its inputs are
constant for all four rotors. Later rotors still perform their own preceding
guards; projection does not become an early cull. Invalid projections and zero
speed retain their original terminal symbols. The historical diagnostic object's
down/radial/projection/stage/validity fields are omitted, but the anchor builder
never exposes or consumes those fields: its canonical output uses symbol and K.

Each rotor is classified and its positive term consumed immediately. The global
positive count is incremented after the append, and `> 2000000` throws before
scaled-cap work or evaluation of the next rotor, matching the anchor. T defers
the dependency append until the four rotors finish; this affects temporary
representation only and does not evaluate later scientific work before a cap
failure. The new row-overflow guard is unreachable under canonical all-pairs
enumeration because a rotor row has at most N-1 positive source IDs. It throws
rather than truncating if that structural invariant is broken.

The symbol buffer and census keep original `[i,j,r]` indexing, complete zero and
rejection classifications, and the same work counters. Scaled-cap accounting,
admission reason order, positive K-to-a scaling, rotor/source summation order,
ordinary bound and graph eligibility expressions match the anchor. The copied
all-pairs certificate is canonical, including its reason field. This conclusion
is about the frozen numeric input scope, not arbitrary proxies, monkey-patched
builtins or an expanded public input domain.

## Stable CSR, dependencies and fixed 4096-entry chunks

L retains the anchor's four ordinary row arrays of `[j,K]` tuples, Set insertion,
sorted dependencies, global ordinary source/K arrays and final typed copies.
T allocates four Uint32 source rows and four Float64 K rows with capacity N.
Lengths reset at every receiver; stale tails are never copied. Since j ascends
and each j is visited once, every positive row prefix has the anchor's source
order. Emitting rotor prefixes in order preserves CSR row order and offsets.

T appends j to its dependency row once if any of that source's four terms is
positive. This is the same unique, ascending sequence produced by L's Set/sort.
The public dependency representation remains independent ordinary arrays.

The chunk policy is a literal constant 4096, matching config. Source reasoning
covers the boundary cases without constructing or evaluating fixtures:

- Empty rows allocate no chunks and do not change length; an empty full matrix
  produces independent zero-length output arrays and zero chunks.
- A nonempty append allocates a chunk pair only if none exists or the previous
  pair is full. `take=min(remaining row, remaining chunk)` is positive, so every
  loop progresses and neither source nor destination overruns its prefix.
- Exactly filling a chunk allocates no extra pair until another positive entry
  arrives. An empty next row does not allocate an unnecessary chunk.
- A row can span multiple chunks; multiple rows can share a chunk. Every prior
  chunk is full and only the last may be partial, so finalization's sequential
  `min(4096, remaining total)` copies the correct used prefix exactly once.
- Offsets are updated after each complete rotor row from the cumulative writer
  length. No receiver/source reordering, count-first second geometry pass, dense
  4N-squared coefficient buffer or discarded positive entry appears.

At the campaign's N and two-million-entry cap, source IDs, offsets and lengths
fit the declared Uint32 representations. The implementation does not claim that
this storage API supports unbounded N or unbounded entry counts.

Final source/K arrays are newly allocated owning buffers. Chunk and row views
are used only as copy inputs and do not escape. Rows, chunks, point scratch,
lengths, offsets and dependencies are local to each build; there is no retained
cross-call matrix or stale geometry cache. Subsequent builds cannot overwrite a
returned CSR through these source paths. `states` retains the anchor's reference
semantics, so the ownership claim must not be widened to whole-result deep
immutability against caller mutation of original inputs.

## Accounting and comparator fairness

For M positive entries and C=ceil(M/4096), the candidate accounts for 48N row
payload bytes, 12*4096C chunk payload bytes, 12M final source/K bytes, 12M bytes
copied from rows to chunks and another 12M from chunks to final arrays. The row
capacity is structural, chunk growth adds pairs without copying old chunks, and
unused chunk capacity is counted. Copy-segment counts are logical paired ID/K
segments, not the number of `.set` calls. Ephemeral subarray view objects have
no new backing payload and remain unmeasured JS objects.

`finalizationOverlapKnownPayloadBytes` is a source-level logical payload overlap
account, not an observation of actual liveness, heap peak or RSS. An optimizing
runtime can release dead scratch earlier or retain garbage later. Adding the
later scaling array gives cumulative typed payload allocation, not a measured
simultaneous peak. Prepared geometry and optional symbol bytes are separate.
L's ordinary arrays, tuples, Sets and runtime overhead are unmeasured, so its
smaller partial typed-payload count cannot establish lower total memory use.

Both L and T pay for point scratch, scalar inlining/projection caching, common
counters and the same query work. T additionally pays row initialization,
prefix copies, chunk allocations/slack and final copies. The builder metadata
is constructed inside the full query; its work falls in total/remainder even
though it follows the final named builder phase boundary. A remains unchanged.

The primary T/L comparison is adequately matched for the stated assembly
package. It includes at least typed row/chunk storage, removal of coefficient
tuples/global accumulation, and elimination of dependency Set/sort. A result
cannot identify which component caused any gain. L/A includes known lean
rewriting plus corresponding loop/setup changes; it cannot identify just object
removal. Shared-function JIT specialization, warmup, allocation and GC behavior
are runtime effects to be reported cautiously, not established by source review.
Neither L nor current A is proven to be the best CPU implementation.

## Antecedents, protocol fit and remaining gates

Re-read the previously verified exact-efficiency source
`research/campaign-exact-efficiency/src/exact-aero.cjs (previously retrieved remote source)`
and its saved REPORT.md. That source already has typed axes/world points, scalar
rotation and an inline rotor kernel (lines 24-49 and 64-113), with refreshed
scratch in its reuse variant. It produces summed winds rather than retained
coupled CSR. Its report finds robust gains over allocation-heavy legacy and
mixed incremental results against previous-zero; support/reuse do not
consistently beat lean, and scaling stopped before N500. These are accepted
saved-report findings, not newly calculated evidence. Earlier arithmetic is
an antecedent, not a substitute for this candidate's pinned reference grouping.

The protocol correctly gives the known lean layer to both L and T, retains A,
freezes 4096 before results, charges full query construction, and describes a
practical threshold rather than a novelty or significance test. Its limited
fresh short-flight population and absence of integrated airflow/browser timing
preclude general live-swarm claims. Neither allocation syntax nor typed arrays
prove heap allocations, vectorization, GC savings or acceleration.

At this review's read, the coordinator controls/runner/independent-review harness
was not present in the inspected package, so this note does not certify those
sources or their coverage. Their freeze must still demonstrate literal boundary,
invalid/near-field and signed-zero controls; zero/full/partial/spanning chunks;
retained outputs across subsequent builds of differing sizes/densities; logical
capacity/copy assertions; and the complete A/L/T canonical comparisons specified
by SCHEMA. Source reasoning is not a replacement for that saved equivalence
evidence. The numerical reviewer and full harness need their own static audit.

No kernel change is requested by this review. Full runtime equivalence,
independent numerical verification, practical benefit, physical validity and
publication gates remain as declared by the coordinator.
