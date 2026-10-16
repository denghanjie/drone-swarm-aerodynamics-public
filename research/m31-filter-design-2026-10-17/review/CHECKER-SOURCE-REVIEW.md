# Independent checker source review

Reviewer: `m31_verified_literature`. Disposition: **accepted for source freeze at the exact pins below**. This is source acceptance, with no numerical result or execution authorization implied. Numerical qualification and publication remain separate gates.

## Reviewed source identity

All paths below are relative to `research/m31-filter-design-2026-10-17/`.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `source/check.py` | 35689 | `1d9f1181d55b4ed5ca76688ad4de29baedec1e008d7eac04806c28c10fc2784e` |
| `prefreeze/checker-v0.py` | 35048 | `0b62f26287be6a6751b47a4443519eed3ff318af215f4a8ffacfbc5315b78dbe` |
| `source/semantic-reference.py` | 44757 | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `source/result-contract.json` | 6662 | `4b9890937fac0131830548dc73241296b2c57783b1883a6762961c3dc45ca5ac` |
| `source/spec.json` | 55777 | `2715ab48ad1c6437244e78ea66c8685c074d579c961f5b4c47857534e2e8de55` |
| `source/run.cjs` | 4323 | `2ce652e43efda4f698ef456e5229e608e9cee26da8a646dc686b1601bbee4536` |
| `source/supervise.py` | 19730 | `a09af9c14853fc1440440e25c443163594bafed7f6257b8194ae3fb8208cdf7d` |
| `source/guardian.py` | 1890 | `b3d6be72fccd56be18d7cd2b59e0ff87aac0442eebf8470c8b7308eb853732de` |
| `PROTOCOL.md` | 10220 | `4e0af980a7be0295cac06550e851d5282a44f5d494e81c9dfc632582ea810bb0` |
| `review/NUMERICAL-DESIGN-AUDIT.md` | 18281 | `29ca8523ff930e6f3decd71b037b498e23ac36dc96f17348394432c7fb3563b4` |

The checker was read in full before the last counter-only edit; the complete diff from preserved `prefreeze/checker-v0.py` to the pinned current checker was then reviewed. The new `primitiveOutcomeCounts`, `primitiveRefusalReasonCounts`, `oracleBranchCounts`, and `fallbackBranchCounts` increment only after the corresponding primitive or pair validation succeeds. They describe validated outcomes and do not alter acceptance predicates, control witnesses, allocations, or qualification gates. The final checker passed AST parsing only.

## Independent numerical acceptance

The fixed allocation is 108 ordered records: 72 primitive records and 36 raw-pair records, with 110 journal events and 16 targeted controls. The spec was parsed as data and its keys, constants, IDs, uniqueness, and record counts inspected. No fixture arithmetic or empirical outcome was computed during this review.

Primitive references independently decode binary64 words and use exact rational arithmetic. Adjacent-word handling covers signed zero, subnormal boundaries, and the maximum-finite to infinity sentinel. Nonfinite inputs refuse. For add, subtract, multiply, divide, and square, a returned interval must have finite endpoints and enclose the complete exact input-interval range. Division across zero cannot produce a qualifying finite interval. A square interval crossing zero has exact lower bound zero. Conservative fallback is allowed, but each of the five operations must have at least one validated finite interval in the allocated sample.

Pair references start with the raw fixture, regenerate the complete prepared-word structure, and independently regenerate the constant graph. Raw nonfinite handling, raw-force handling, preparation failure, and scalar branch ordering remain distinct and ordered. The actual near-unit residual is retained. Both baseline and candidate results are checked against the independent oracle before candidate/baseline equality is considered. Fast zero requires the original admitted zero branch and an exact zero wire payload; positive values cannot be substituted by a fast result.

Every positive fallback must provide fixed96 intervals for K, scaledK, beta, nu, and coefficient that enclose the fixed192 reference. Nonnegative endpoints, K/scaledK upper bounds of 128, and a strictly positive nu lower bound are enforced. Every fixed96 unresolved outcome and every fixed192 reference-undecidable outcome fails qualification; stress-labelled fixtures have no exemption. The full candidate result must equal the full baseline result.

Coverage requires a valid fast zero and a valid positive fallback. The controls independently require a positive `tail-positive` fallback witness, including a positive oracle/coefficient lower bound and a candidate fallback. The checker does not require all six zero branches to hit fast; observed per-branch counts are descriptive and must be reported as observed.

## Control witnesses and saved-data checks

The 16 controls target:

- Six primitive faults: inward add upper/lower endpoints, lost underflow, false finite overflow, zero-crossing divisor, and loss of the square-zero lower bound.
- Six pair faults: positive-to-zero substitution, an earlier guard bypass, wrong zero branch, prepared-point mutation, lost positive coefficient, and invalid-preparation bypass.
- Four structural faults: a missing row, duplicate row, reordered rows, and journal disagreement.

Controls mutate deep copies and retain witnesses. Each must produce its intended semantic rejection code; generic candidate/baseline disagreement alone is insufficient. Mathematical validation precedes baseline equality. The journal-disagreement control first requires the unchanged document to pass validation. A missing control witness fails qualification.

Strict JSON handling rejects duplicate keys, non-printable/non-ASCII strings, floating-number tokens, nonfinite constants, unsafe integers, and excessive nesting. The checker binds exact fields, record IDs/order, source/spec identity, constants, and prepared values. Its byte contract is compact ASCII JSON in retained insertion order plus exactly one newline, not sorted-key canonicalization. The journal must contain the exact header, 108 ordered rows, and completion event.

## Helper provenance, execution closure, and outputs

`source/semantic-reference.py` contains copied inherited `pair-reference.py` content and is conservatively counted as the fifth inherited path read in this cycle. Review covered its AST import/top-level structure, the complete referenced functions at lines 150–393, 448–559, and 601–616, and the guarded main tail at lines 945–960. Imports are standard-library only. Its old generation, suite, control, and main entry points are not called by the new checker. The old main remains protected by `__name__ == "__main__"`. The additional height<=0 width rejection is equivalent on the admitted positive spread/D domain because width = spread * height * D.

The helper is dynamically compiled from verified bytes only inside the future authorized checker main, after manifest and hardcoded SHA checks. The reviewer did not import or compile-execute either checker or helper; AST parsing does not execute them.

The checker and adapted supervisor require all local source files, including the helper, and the five explicit inherited baseline pins (`adapter.cjs`, `rational.cjs`, `pair-prepared.cjs`, `interval.cjs`, and `spec.json` under the closed screening-cost package). Manifest validation covers path canonicality, root containment, symlink rejection, source hashes, budgets, and the Python runtime pin. Inputs, sources, manifest, and runtime identities are checked again before checker output; the supervisor closes the stage with another identity check.

Qualification requires baseline/document validation, journal agreement, all 16 controls, and unchanged sources/inputs. `qualifiedRecords=108` is emitted only on complete success; failures exit nonzero. Full `reference.json` and `independent-check.json` are created exclusively and fsynced, with a combined 32 MiB limit. The adapted supervision source imposes one 300-second kernel and one 300-second checker, 310-second guardians, sampled RSS of 512 MiB, 16 MiB per kernel scientific file, 8 MiB for logs/metadata including private raw logs, 64 KiB per report, and 96 MiB aggregate retained output. This review adds no execution allocation.

## Scope and remaining gates

The accepted design addresses the allocated finite primitive and single-pair correctness checks. It establishes no all-input proof, runtime/capacity measurement, load-solver result, group-suite result, benchmark, browser/dynamics result, physical claim, or novelty claim. Source inspection cannot substitute for the sole allocated numerical run and its independently checked saved outputs. No prior package was edited or rerun.

The cumulative inherited-content reading inventory is five distinct paths against the cap of twelve, recorded in `review/CHECKER-SOURCE-READING.json`. The previous four-path inventory is preserved and pinned there. No additional inherited scientific contents were read for the final counter diff.
