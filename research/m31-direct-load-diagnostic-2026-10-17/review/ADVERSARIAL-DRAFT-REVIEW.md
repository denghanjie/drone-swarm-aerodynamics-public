# Source-only adversarial review — prospective direct-load diagnostic

Disposition: the proposed A/B/C comparison is mathematically coherent as a conditional, oracle-assisted numerical diagnostic. **Do not freeze or allocate the current producer/config pair yet:** there is an unconditional configuration mismatch, and several schema/checker obligations need to be closed. This is a desk review, not an executed validation or an allocation.

I read the protocol, configuration, predecessor proposal and producer draft, plus the inherited adopted model, root-defect corollary and prior-art review. I did not execute or import scientific code, read any of the six target input/reference/result records, or change the completed viewer QA. No external literature search was performed.

## Findings requiring resolution before freeze

### 1. P1 — Current producer rejects the current configuration

`source/analyze.py:28–30` defines `CONSTANT_PROVENANCE` with `path` and `sha256`. `source/config.json:16–23` also includes `fields`. The exact dictionary equality at producer lines 512–513 therefore fails for the supplied configuration before any target calculation. Resolve the shape consistently, preferably retaining the explicit field names in both. Pin the resolved pair and have the independent checker validate the same provenance identity.

This finding follows from source inspection; I did not run the failing path.

### 2. P2 — Protocol promises every row, producer emits only nonempty omission rows

Protocol line 23 promises omitted coefficient mass at y=1 and candidate-weighted mass for every row. Producer lines 493–501 append diagnostics only when `sources` is nonempty. Emit all 256 `(receiver ID, rotor index)` rows per omitted proposal, with exact `[0,0]` masses and count zero on unaffected rows. Alternatively explicitly freeze a sparse schema with a total-universe/default-zero rule, but the all-row representation is clearer and directly matches the protocol. The checker must reject missing/duplicate rows under whichever schema is adopted.

### 3. P2 — Give B/C certificate outcomes their own semantics

Producer `audit_summary` currently applies A's `pass / definite-fail / unresolved` helper to B and C as well. This does not presently generate a sound B/C claim of definite inaccuracy: each B/C root box contains the candidate itself, so signed load propagation contains its candidate load and every B/C error lower bound is zero. A B/C upper bound above tolerance therefore returns `unresolved` in this implementation.

The shared schema nevertheless invites exactly the interpretation error this diagnostic must avoid. Use explicit `certified / not-certified` B/C category and overall statuses based only on the upper endpoint, or include an equally explicit audit-kind/status contract and ensure every consumer applies it. Reserve `definite-fail` for A's lower bound above tolerance. Do not describe a B/C rejection as measured error, physical-force failure, or proof that the omission candidate is inaccurate.

Keep the branch wording precise: A-pass/B-not-certified demonstrates insufficiency of this implemented root/load certificate at that threshold; it does not establish that every certificate must be too loose. A+B-pass/C-not-certified identifies additional loss from the specified upper-only omission enclosure and its downstream certificate, not a universal lower bound on practical selector quality.

### 4. P2 — Bind the entire executable schedule to configuration

The producer validates schema/constants/provenance but otherwise uses hardcoded `STATES`, `PRIOR`, `ITERATIONS`, `BISECTIONS`, `TIERS`, fixed 192-bit enclosure grids and the 1/10 mask. The current declared values agree, but a changed or missing config state list, schedule, tier list, prior or mask would not be rejected by this module. Before freeze, require exact equality with the declared fixed schedule, either here or in the pin-verifying dispatcher/checker. Record both square-root and outward root-grid precision in the frozen configuration/output contract. Source pins alone prevent unnoticed edits; explicit validation also prevents an internally contradictory published protocol/config pair.

## Mathematical assessment

The native proposal is a deterministic proposal, not a proof. Forty-eight simultaneous updates and 54 bisections are correctly explicit; no reference-root warm start appears in the source. Native normalized weights use ordinary binary64 sums/divisions, while proof weights are exact nominal-force ratios. This distinction is legitimate because the arbitrary-candidate theorem requires the exact identity only in the audit. Clarify it in the protocol so “exact normalized weights” is not misread as a claim about the native proposal.

The fixed mask includes all declared positives, including lower endpoint zero, sorts exact coefficient upper endpoints then stable `(i,r,j)`, and takes `ceil(P/10)`. It is a global fixed mask, not a per-row coefficient budget. The reference pair checks enforce distinct valid keys and the complete nonself universe by cardinality. Stable IDs are not array indices.

For nonnegative rational `q`, `sqrt_point` computes `floor(2^192 sqrt(q))` using integer square root and a separately checked exact-square case. Thus its endpoints include the mathematical square root. Outward root-grid flooring/ceiling also includes the unquantized rational root interval; clamping the raw upper endpoint at one remains valid under the adopted candidate/model domain. The grid change limits denominator growth in subsequent signed load propagation and cannot improve a bound by rounding inward.

The B chain matches the inherited arbitrary-root corollary: same candidate-derived exact-weight square roots, complete coefficient contraction, positive `pL`, local `k=max(1,pU,1/pL)`, global `K`, and roots `[x/(kK), min(1,x*kK)]`, rounded outward. The theorem is conditional on the prior reference's complete guarded-model admission; an admitted-label string alone is insufficient without its pinned independently accepted provenance. It certifies the declared prepared-word model, not physical airflow or legacy native arithmetic.

C replaces only the omitted lower contribution with zero and retains its full candidate-dependent upper contribution. No re-solving occurs. Consequently `sC` contains `sB`, each `kC>=kB`, `KC>=KB`, C's root boxes contain B's root boxes, and C's signed load boxes contain B's. Outward grid quantization preserves this inclusion. **C's upper error cannot be smaller than B's, and C cannot certify a tolerance that B does not certify.** These are useful independent checker invariants, not empirical expectations.

Rotor loads use nominal thrust times ratio, not ratio squared. Collective, world force and world moment use signed propagation and actual supplied axis/lever components. No exact-unit-axis assumption is introduced. A's scalar distance intervals and coordinatewise minimum/maximum Euclidean distances enclose error relative to the saved reference boxes, even though component dependence can make them loose. Taking the maximum of lower endpoints and maximum of upper endpoints correctly encloses the worst category error across the state. The prescribed `mg/4`, `mg`, and `mg R` scales are positive frozen dyadic constants.

A upper <= tolerance establishes the requested numerical comparison; A lower > tolerance establishes definite numerical failure within the declared model; overlap is unresolved. Reference midpoints are not used as truth. An A definite failure and a B or C certificate at the same threshold would contradict two sound bounds on the same error and must be reported as an internal inconsistency, not a mixed scientific result. B passing while A is unresolved can occur if the saved reference box is too wide; the fixed protocol may still conservatively refuse advancement.

## Independent checker requirements

The checker should independently reconstruct these objects from pinned source/config and the accepted predecessor records, without importing producer routines:

1. The exact six-state schedule, two proposal labels per state, 12-candidate count, source/input/reference identities and canonical input envelope binding. Validate all expected IDs, pair classifications, positivity and complete row membership. Bind the upstream independent acceptance of reference admission, coefficient intervals and reference load boxes.
2. The full global mask and its order/count, including exact endpoint comparisons and tie breaking. Validate full control has zero omissions. Never infer the mask from a producer-provided count alone.
3. Native candidates using the frozen source-order reductions, rounded native normalization, exact rational-midpoint conversion to float, all-ones initialization, 48 simultaneous updates and 54 bisections. Compare exact binary64 identities. Keep runtime/platform scope explicit for native `sqrt`; proof soundness comes from exact auditing, not assumed cross-platform byte reproducibility.
4. Exact candidate loads, normalized proof weights summing to one, source-y enclosures, complete B/C contractions, defect intervals, local/global factors, outward grid root intervals and signed load propagation. Enforce identical candidate identity throughout A/B/C and no omitted contribution silently removed from either certificate.
5. A error intervals and category/state/tier decisions; B/C sufficiency decisions; all-row omission diagnostics; six-state aggregation with no averaging, omitted state or denominator shrinkage. Full-control A failure/unresolved invalidates omission attribution, even if some omission outcomes look favorable.
6. Invariants: candidate inside every B/C root/load enclosure; B/C error lower endpoints zero; C contains B; C upper errors >= B; no certified-C/not-certified-B combination; no A-definite-fail alongside B/C certification at the same threshold.
7. Source-derived analytic fixtures and malformed-record mutations. Cover nonuniform exact weights, asymmetric signed moments, non-unit axes, irrational square roots, nondyadic root-grid endpoints, lower-zero positive coefficients, mask ties and ceiling, exact tolerance equality/overlap, altered candidate bits, missing/duplicate pairs or diagnostic rows, stale candidate-dependent y, inward endpoint changes, omitted retained terms and changed constants. Mutation tests must actually reach their intended validator; a universal missing-file or schema rejection is not evidence for deeper checks.

A checker cannot certify independence merely by comparing producer summaries or reusing the producer's emitted intermediate boxes. Its accepted output should record both per-state decisions and a single protocol branch, while preserving all 12 scheduled proposals when computation completes. If execution is interrupted, preserve the failure with the scheduled denominator rather than reporting a smaller successful experiment.

## Resource/source-design review

The producer deliberately delegates enforcement to an external dispatcher; no enforcement implementation was part of the reviewed producer draft. That is acceptable at source-preparation stage, but **the dispatcher and independent checker must also be reviewed and pinned before allocation**.

The protocol correctly calls 512 MiB a post-output peak-RSS acceptance gate rather than a hard memory ceiling and discloses that interpreter startup/teardown and final attempt serialization lie outside portions of accounting. Do not later present the 180-second alarm or RSS rule as stronger guarantees.

The dispatcher must create an exclusive single-use marker before scientific import, verify complete source/data/runtime pins, enforce the 120/121-second CPU limits and 180-second alarm without polling extensions, reject launches after the fixed cutoff, serialize outputs under the 16 MiB gate, apply platform-correct peak-RSS byte conversion, and retain nonzero exit, signal, timeout, oversized or incomplete attempts without retry. The checker gets its own single-use bounded attempt. No fallback precision, fraction sweep or alternate schedule may occur after outcomes are seen.

Source arithmetic has fixed precision and iteration counts, but that is not a demonstrated runtime/memory upper bound. A budget failure is a resource outcome, not A inaccuracy or B/C mathematical rejection. No target execution or performance claim is justified by this review.

## Literature and interpretation boundary

No new external citation is needed for this elementary, internally derived diagnostic. Link directly to the inherited M-current adopted design, arbitrary-root adopted corollary, and `m31-current-bound-design-2026-10-16/review/PRIOR-ART.md` rather than referring vaguely to an unnamed ledger. The prior-art review accurately limits Gray–Moore and Curtin et al. to established hierarchical-summation/traversal antecedents. Rump 2010 was only verified bibliographically and through an introductory extract; it must not be cited as if a specific square-root, rounding or nonlinear theorem was read there. The formulas reviewed here have their own inspectable inclusion arguments.

The six snapshots remain exposed dependent diagnostics from airflow-off flights. A success is numerical accuracy headroom under an oracle-assisted prepared-word model, not avoided coefficient work, online admission/certification, flight safety, physical fidelity, novelty, or 5,000-drone browser feasibility. The changed mask cannot reverse the prior fixed tau/16 proxy's negative result. A future practical selector and complete-cost comparison remain separately reviewed work.

## Reviewed source identities

Hashes below identify the versions inspected for this review. Later source changes require explicit reconciliation; they are not silently covered by this report.

| Source | SHA-256 |
| --- | --- |
| `research/m31-direct-load-diagnostic-2026-10-17/PROTOCOL.md` | `f9d6cbad0c8a6cedf01e11555f45702a25dc37c94b0c661429ffdfa52f82c8af` |
| `research/m31-direct-load-diagnostic-2026-10-17/source/config.json` | `432f3c1f74ad7b7cf9c71aca98a7ade570c9c5bc5f1b16c6068b9ef04b6dec0a` |
| `research/m31-oracle-omission-renewal-2026-10-17/review/NEXT-PROPOSAL-NOT-ALLOCATED.md` | `d7e251054814e78879bedd91a8c74ac9e0b3055e103033bd04278669205ade29` |
| producer draft `source/analyze.py` | `d474e67ca9f8695272bda8868ab1848b5058e47d36a2fbac0935a01e020bdff4` |
| `research/m31-current-bound-design-2026-10-16/ADOPTED-DESIGN.md` | `702d64e84c3fc12fdc9e85cb59abf4dd00e8df010647e1567a47eed49ee5387c` |
| `research/m31-current-bound-design-2026-10-16/review/PRIOR-ART.md` | `a35f4b75694957b6b0406a305aa5e37a9c2eb784312f81abd419f7c3d2bafd20` |

Additional source-only context read: `research/m31-root-defect-planning-2026-10-16/ADOPTED-DERIVATION.md` and `research/m31-oracle-omission-renewal-2026-10-17/LITERATURE-AND-DESIGN.md`. Directory listings exposed filenames only. No six-state target record contents were read.

Public-copy note: temporary producer handoff path replaced by source/analyze.py. Review identifies the earlier draft by its original digest; later resolution is separate.
