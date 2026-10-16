# Independent interval checker: source review

**Disposition: authored for the prospective source gate, not executed or numerically qualified.** The independent checker source is `m31-interval-check.py` (delivery artifact; copy into the package and include the copied file in the frozen source manifest before execution).

Checker bytes: 30506. SHA256: `99e79de9747063825d3a6c8c0d2f8dc1e5fba6af8739204fa9b322184d96703c`.

## Independence and declared interface

Only the new protocol draft, specification and declarative result contract informed the checker. Neither `source/interval.cjs` nor `source/run.cjs` was opened, imported or evaluated. The checker imports only standard-library modules when eventually run and has no subprocess or network calls. This source review included AST parsing of the authored checker, which checks Python syntax without importing or executing it. No case generation, numerical expectations, fault controls or checker results were evaluated during authoring.

The CLI is `python check.py --spec <spec.json> --input <primitive-results.json> --manifest <source-manifest.json> --output <independent-check.json> --root <repository-root>`. The result contract is read from the specification's sibling `result-contract.json`; the journal is the input path plus `.jsonl`. The final checker must be run from its manifest-pinned package copy, not its delivery location. Report creation is exclusive. Reports contain repository-relative paths and Python version/implementation, with no interpreter or machine paths; ordinary error messages are replaced by bounded public-safe codes.

The checker requires the supplied source manifest's unique relative file entries to match current bytes and SHA256 values. The specification, result contract, checker and each runner-reported source must be pinned. It checks the runner's three source hashes against that verified inventory. This is local integrity checking against the supplied manifest; the parent's independent published-manifest verification remains the trust anchor.

## Mathematical and coverage checks

The checker independently consumes the unsigned LCG in declaration order: 128 binary64 draws, then three draws for each of 128 generated intervals, then two draws for each of 208 generated pairs. Explicit cases consume no draws. The revised 48 explicit pairs precede those 208 pairs, and generated indexes use the high 32 bits. It reconstructs all IDs, order, inputs and 1,488 cases from the declarations. Fixed allocation, algorithm-rule text and shape/range checks reject silent declaration drift. The clarified contract applies pair IDs to all 256 pairs.

Finite binary64 values are decoded by sign, exponent and significand into exact `Fraction` values. NaNs/infinities are classified before conversion/range handling. No Python float or decimal approximation supplies numerical expectations.

For add/subtract, the image extrema follow monotonicity. Products and division by an interval excluding zero use the four rational corners. Square uses zero as its minimum when the input spans zero; otherwise it uses the smaller squared endpoint. Integer floor/ceiling of the scaled exact extrema produce the tight lattice interval. A zero-containing divisor and a negative sqrt lower endpoint are domain failures before endpoint-range handling. Outward endpoints beyond the declared integer resource range produce unresolved-range, without being reclassified as a physical-domain failure.

For sqrt, the checker uses `isqrt(floor(q))` for the exact nonnegative rational quantity q equal to the input endpoint times S squared. Because consecutive integer squares bound q, this gives its integer floor root; exact equality distinguishes the ceiling. This is independent of the implementation's proposed capped iteration. The checker also verifies actual returned nonnegative endpoint squares against the original rational endpoint values. Other successful operations have a separate rational-inclusion check in addition to exact endpoint equality.

Every record must retain its status, match its regenerated input and ID/order, and report `inputUnchanged` as the actual JSON boolean true. Success/failure shapes are exact, and unexpected iteration/check/invalid statuses fail qualification rather than disappearing from the count. Expected and observed status counts retain all named statuses, including zero counts.

The baseline additionally requires the journal header, all 1,488 ordered rows and completion marker to agree with the final result. Type-sensitive structural comparison avoids Python's boolean/integer equality aliases. Source integrity and journal checking do not substitute for numerical validation.

## Fault controls in the single future execution

The baseline and all mutations use the same core document/arithmetic validator. Journal comparison is a separate baseline gate, so controls cannot succeed merely because an unmodified journal differs from a mutated final document. In-memory copies preserve the original document and files.

Five required categories contain six concrete probes:

1. Narrow the positive minimum-subnormal conversion from [0,1] to [1,1] in lattice units. This remains ordered but excludes the exact positive value, which is smaller than 1/S; it is not just a different valid wide interval.
2. Replace the successful exact-zero conversion with unresolved-domain.
3. Remove the final required record.
4. Separately replace the second record with a duplicate of the first, and exchange the first two records.
5. Alter the first zero input to the minimum positive subnormal while retaining its zero output.

Each probe records rejection and bounded validator errors. All five categories must execute and reject their probes; a missing, skipped or ineffective control prevents pass. Invalid baseline data is retained as failure and does not gain a passing control result.

## Limits and execution gate

No runtime, numerical pass, observed status distribution or resource-use result is claimed. The checker has bounded file sizes, source counts, record counts, integer-string lengths, errors and report output. The separate supervisor must still enforce the prospective 120-second/process-group RSS limits and preserve failures; this checker does not spawn a guardian or enforce those external budgets itself.

Finite-suite success would support only those declared cases. General inclusion, implementation domain/range logic, the 512-step algorithm and integration remain separate source-proof obligations. The checker can enforce returned original operands, the reported true mutation flag and journal consistency; it cannot observe hidden in-process mutation directly. Frozen-operand/source review must support that claim. Similarly, journal contents alone cannot prove the promised fsync cadence. Python implementation/runtime provenance is reported, but executable provenance and source publication are the parent's gates.

No source manifest was executed or scientifically tested in this authoring task. Commit/push, independent exact-manifest retrieval and explicit source-gate completion remain prerequisites to the sole runner/checker allocation.

## Exact reading inventory

This checkpoint used **0 inherited content files of the 16-file allowance** and the following **3 distinct new declarative input paths**. The checker source itself was read solely for syntax parsing and ordinary byte/hash metadata. No external retrieval occurred.

| New input path | Bytes at final metadata check | SHA256 |
| --- | ---: | --- |
| `research/m31-interval-primitives-2026-10-16/PROTOCOL-DRAFT.md` | 6226 | `15f86c9e11f7b69386b073219946539cbd66c59fe92b10b25936fdb53150a891` |
| `research/m31-interval-primitives-2026-10-16/source/spec.json` | 2550 | `73d539b2f6575e21b3f8c512ce79a4be22ff0b09c98c527cb18dfc06a6dc21f7` |
| `research/m31-interval-primitives-2026-10-16/source/result-contract.json` | 2863 | `a41c1a936b3b4772e90de182abffd7b41dc552a0f217a15738015f5359a3d522` |

The same specification path was first inspected before the parent's source-only revision (initial SHA256 `d8065903820d08a730489abea8d92d1bad735770818e9e6717ca5ff6ab6fb2e4`) and then reread after its 48+208 pair declaration. The result contract was first inspected at SHA256 `c888bb0c7040b44848d50380de64211a4bb37f6584577a9f8726457354a16da6`; its final ID wording was subsequently inspected. These are prefreeze declaration changes, not changes informed by numerical observations. Earlier checkpoint reports and package science were untouched.
