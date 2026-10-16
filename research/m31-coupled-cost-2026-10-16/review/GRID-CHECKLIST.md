# Coupled-cost kernel: prospective static checklist

2026-10-16. Awaiting the coordinator's kernel-ready message. Source-only scope:
inspect the forthcoming kernel.cjs without importing/executing it, evaluating
targets, timing, or running controls. Write only this private review directory;
old frozen packages remain unchanged. No checked box below implies execution.

## Kernel source review

- **Shared contract:** all-pairs and grid arms use the same original-coordinate
  center arithmetic, constants, four rotor offsets, pairTerm, K scaling, graph
  eligibility, root closures/stopping and residual definitions. Source IDs ascend
  within every receiver-rotor sum. No unrelated algebraic regrouping or altered
  summation is hidden in the grid arm.
- **Guard order:** self is symbol 1. For each actually visited nonself center,
  compute original dx,dy,dz and Math.hypot; nonfinite / norm >512 / component >257
  is invalid before center >=3 is outside. Only strict center <3 reaches the
  unchanged rotor rules. Radius filtering never hides far invalid pairs.
- **Certificate:** scan every original position for finiteness and exact stored
  minima/maxima; binary64 spans must be finite, nonnegative and <=256 on every
  axis. Local coordinates are for binning only. False/unsafe certificate selects
  the full original directed-center loop, not whole-snapshot rejection or silent
  omission. Record its cause and actual fallback work.
- **Coverage:** cell width is fixed at4; source bins use floor(u/4); query bounds
  are floor((u-3)/4)-1 through floor((u+3)/4)+1 inclusive in all three axes.
  Local coordinates and resulting indices are finite/safe; query loops cannot
  stall at unsafe integer magnitudes. Each occupied cell is queried once.
- **Completeness/order:** buckets retain every source, including dense occupancy
  and coincident positions. Self exclusion uses ID, not coordinate equality.
  Gathered IDs are numerically sorted; no top-k, capacity clamp, unordered sum,
  pair symmetry reduction or duplicate source contribution. Check exact source
  lists, not only sets or aggregate counts.
- **Costs/ownership:** certificate, local transform, grid/map construction, key
  allocation, gathering, sorting, K/CSR and dependency construction belong to
  cold complete queries. Stored scientific outputs are not borrowed from old
  runs. Reuse across iterations within one query is distinct from free setup
  across measured queries. Fallback includes its certificate overhead.
- **Accounting:** logical pair coverage, certified skips, candidate visits,
  actual center hypot calls, eligible centers, four-rotor calls, positive K,
  root closures, bisection loops and positive-term multiplies remain separate.
  A full symbol tensor still carries quadratic initialization/output work.
- **Failure/evidence:** bounds and resource failures preserve records and consume
  their allocation; no retry, alternative target or adaptive cell-size choice.
  Tiny-control code must not load target files, call load/root solvers or advance
  state. The coordinator clarified that the eventual allocated candidate may run
  both production geometry builders, including pairTerm, on the fixed controls;
  this current task still permits source inspection only.

At source review, record exact kernel hash/bytes, relevant protocol version and
line locations. Read source dependencies only as needed; no require/import.

## Assessment of proposed no-model tiny controls

Initial planning interpreted "no-model" as center-only controls. The coordinator
subsequently clarified that the21 fixed controls will run both production scalar
geometry builders, including pairTerm/K, once inside the allocated candidate
after freeze; no control load solve is intended. Full symbol/support/K equality
is therefore the planned comparison. Independently recount saved symbols and
check operation counts as well as cross-arm equality. The cases below are
prospective mathematical expectations, not observed results. Nothing was run in
this source-only review.

| Control | Construction and required observation | Important trap |
|---|---|---|
| Radius near0 | Receiver at0, sources at nextDown(3),3,nextUp(3) along one axis. Interior point is eligible; exact3 and exterior point are outside. | Keep the final predicate strict; do not inflate radius because the grid is padded. |
| Radius with receiver-6 | Receiver at-6, source boundary at-3. nextDown(-3) is inside; -3 and nextUp(-3) are outside in the positive direction. | nextUp on a negative value moves toward positive infinity. Spell out receiver and boundary rather than saying only “±ulp at-6.” |
| Cell boundary near4 | Include a separate origin/minimum anchor at0; use source points nextDown(4),4,nextUp(4), with a receiver at1 if also exercising the3m cutoff. | Without the0 anchor, the local minimum shifts the intended bin boundary away from4. |
| Signed zero/duplicates | Distinct IDs at +0 and -0/coincident centers; retain every nonself ID. | Coordinate equality is not self identity; signed-zero cell keys may coincide normally. |
| Common translation2^40 | Translate a coarse exactly representable geometry, e.g. dyadic eighth/quarter offsets, and compare against the independently evaluated translated center predicate. | Original ulp perturbations around0 or4 can collapse after this translation. Do not demand unchanged classifications for altered rounded input differences. |
| Dense16 centers | A small3D arrangement with every nonself center within3; all15 IDs per receiver must survive, ascending. | A fixed occupancy cap, self-by-position test, duplicate visit or gather-order bug must be observable. |
| Span256 | Use min0,max256 on one axis, other axes fixed. Certificate is true; distant pair is outside, not invalid. | Span certificate concerns original centers, not rotor offsets. |
| Span nextUp(256) | Use min0,max nextUp(256). Certificate must be false and choose all-pairs; this distance is still below257, so the pair is outside, not automatically invalid. | Symmetric endpoints around ±128 can round their subtraction to256; use min0 to make this a deterministic threshold control. |
| Far258 | min0,max258. Certificate false; fallback identifies the pair as invalid because component difference exceeds257, despite being far outside3. | This is the essential guard-before-neighbor-skip witness. |
| Nonfinite/overflow | NaN and Infinity positions force fallback and the canonical nonself invalid classification. Separate finite endpoints ±Number.MAX_VALUE force an overflowing span/difference and invalid fallback. | Do not send NaN/Infinity/unsafe indices into grid loops. Do not replace every matrix entry with invalid: self remains self/outside symbol1. |

Exercise x, y and z in the frozen controls rather than using only x-axis data;
otherwise an incorrect y/z stencil could pass. This may be one3D case or explicit
axis variants within the predeclared tiny-control budget. These are suggestions
to freeze, not permission to add cases after failures.

For translated radius boundaries, if desired, construct adjacent representable
values around the translated source coordinate itself. At magnitude2^40 the ulp
is much larger than at3/4; expected eligibility must come from the original
stored-coordinate subtraction at that magnitude. Such a control is different
from an invariance claim for a pre-rounded near-origin fixture.

The dense case can be specified exactly without random generation, for example
16 distinct centers on a2×2×4 lattice with spacing1/8. All nonself distances are
strictly below3 by a large margin; the independently written predicate still
serves as the execution oracle. Duplicate-center behavior belongs in its own
explicit ID-preservation case. No measurements or calculations on those points
have been executed here.

Boundary helpers must be source-audited: nextUp/nextDown handle signed zero,
negative values, infinities and NaN correctly and must not use an unverified
decimal epsilon. Expected lists must not call the grid helper they validate.
Reference center calculations must use the same Math.hypot runtime predicate as
the complete-query contract, with independent traversal/guard code.

## Pending work

Wait for ready notification, inspect the exact source, and report defects before
freeze. This checklist neither establishes correctness nor authorizes controls,
target evaluation or timing. No numerical execution occurred in its preparation.
