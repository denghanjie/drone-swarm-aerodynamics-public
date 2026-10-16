# Oracle omission screen: final static source review

**Disposition: accepted for the three exact source/protocol pins below. No remaining material blocking error identified in this assigned scope.** The independently written checker, final manifest/publication verification, authorized dispatch, and saved-result acceptance remain separate gates.

All paths in the table are relative to `research/m31-oracle-omission-screen-2026-10-17/`.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `source/analyze.py` | 10400 | `50cd4111f107fcd99bf9cadcf098a4f2b298eec319ce0930cb0473150b2921e9` |
| `source/run.py` | 5553 | `fb5a72f4726f2bcca69bd564489daead5edfcd67e2f8209f8f2470d4d965d3c2` |
| `PROTOCOL.md` | 8360 | `11d46ed7e62f03348c4a3b745ecbc271e6d8c1bf6e7b2ab877f1a35fce415bc5` |

The final three files were read in full. Relevant static schema-writer definitions were also inspected in the earlier replication checker and moving-admission checker/semantic reference. No target input, coefficient, reference-result or baseline-result values were read in this task. No analyzer/checker/project module was imported or executed; no tests or AST execution were performed. The fixture assessment below is a manual source calculation, not an empirical pass.

## Identity, trees, and decisions

The final analyzer uses reference pair `i,j` directly as stable IDs, with membership and integer-domain checks. This matches `semantic-reference.py`'s emitted `ids[receiver]` and `ids[source]`; it does not remap them through input positions. The canonical input hash now includes the domain `m31-moving-admission/input/v1`, state ID, and input, with sorted compact JSON. This matches the prior checker's `input_hash`/encoder for these ASCII raw-word inputs. Baseline input equality, reference admission, prepared identity, and raw/prepared center-word equality are checked.

`Fraction.from_float` receives the exactly decoded binary64 center and therefore recovers its exact rational value. Longest-span choice uses x/y/z tie order, exact center then numeric stable-ID sorting, floor midpoint, left-first recursion, and unchanged incoming order when a leaf is reached. T8 permutation and structural fields are checked against the saved baseline. Running the same recursive rule to capacity two retains every capacity-eight node's member set by construction; IDs/permutation offsets of later nodes need not remain identical. The separate checker should verify that member-set property and the reported partitions as its protocol requires.

Zero rows are explicitly mapped to `(0,0)` only after validating status and absence of a coefficient. Every positive has `0 <= lower <= upper` and `upper > 0`; therefore the later `upper > 0` filter is exactly the validated positive roster and retains zero-lower positives. Duplicate pair identities are rejected. The permitted pair universe has exactly `4*64*63=16128` members; valid identity domains, uniqueness, and that exact cardinality establish complete coverage. The positive denominator is checked against the saved reference graph count and remains fixed across policies and tiers.

Both singleton prefixes sort exact fractions with stable-ID ties and accept budget equality. Lower-prefix count is the optimistic count ceiling; upper-prefix count is a feasible oracle construction under the mass proxy. Exact budgets come from `Fraction(tier)/16`. Per-row counts are summed with no pooled budget or averaged row percentages. State decisions use `positiveTerms > 0 and 10*count >= positiveTerms`, so equality passes and zero-positive states do not pass. The all-six rule is correctly stated in the protocol; the analyzer records the individual state decisions from which that conjunction must be formed.

Tree selections use whole self-free nodes, require at least two validated positives, charge all member upper endpoints cumulatively, and return immediately after accepting a parent. Rejected leaves retain all nonself members. One-positive nodes consume no budget. Thus the constructed selected/fallback partition is disjoint and complete. The protocol correctly distinguishes these feasible greedy examples from optimal grouped ceilings and warns that refinement or a larger budget can reduce greedy coverage. No practical bound, speed, full-load, physical, or fresh-evidence conclusion is encoded.

## Nine literal fixture expectations, checked by hand

| Fixture | Expected result is consistent with source |
| --- | --- |
| zero-lower-positive-included | Budget zero retains ID 7 with lower endpoint zero. |
| exact-budget-equality | `1/3 + 2/3 = 1`; both IDs retained. |
| tiny-overflow | Budget `1-1/10^50` retains only the `1/3` term. |
| tied-stable-id | Equal `1/10^50` values select ID 2 before ID 9. |
| zero-positive-row | Empty prefix and zero mass. |
| greedy-refinement-can-reduce-count | Capacity four skips mass 202 and selects four `3/5` terms, mass `12/5 <= 5/2`; capacity two first spends 2 on IDs 0/1, leaving insufficient budget for any later two-member positive node. Counts are 4 versus 2. |
| self-leaf-falls-back | Self is excluded and only source 1 is retained; missing self weight is never accessed. |
| one-positive-does-not-spend | The left one-positive node is retained without charge; IDs 2/3 are selected at total mass 1. |
| accepted-parent-prevents-overlap | At budget 2, the root is selected once and fallback is empty. |

## Single-process runner and finite limits

The runner exclusively creates the stage attempt before work, exclusively creates the stage result, verifies the caller-supplied expected manifest digest, listed file sizes/digests, and Python binary pin, and binds checker dispatch to the completed analyzer output hash and source-commit label. It imports only the selected saved-data stage; the inspected analyzer has no subprocess or simulator import. Checker internals are outside this review.

Configured limits are a 90-second SIGALRM guard, CPU soft/hard limits of 60/61 seconds, 512 MiB `RLIMIT_DATA`, and 16 MiB per output with a serialized-byte size check before writing and `RLIMIT_FSIZE`. Serialization occurs in memory under the data/CPU guard. `RLIMIT_DATA` is not total RSS; the protocol and attempt metadata correctly say so. The alarm remains active through normal final record I/O, and stdout printing has been removed. This is a signal-based guarded interval, not a strict whole-process deadline or a guarantee that a timeout can finish its report. Interpreter startup, initial marker creation, and teardown are explicitly outside its scope. Usage fields are a snapshot immediately before final attempt serialization, not a measurement of the remaining reporting tail.

Final attempt replacement now writes an exclusive `.final.tmp`, flushes and fsyncs it, atomically replaces the initial marker only after complete content exists, and fsyncs the directory. An interruption before replacement retains the started marker and possibly a partial temp; it is incomplete. If finalization completes, the first caught failure is preserved. No retry is enabled by either failure path. The protocol appropriately avoids a power-loss-proof guarantee, and the context label remains caller attestation rather than sandbox detection. Exact public commit verification remains an external prelaunch gate; the runner's commit field is not itself such a verifier.

## Prefreeze corrections disclosed

Four source/contract issues were corrected during static preparation: the initial positional remapping of stable pair IDs; the initial raw-file hash in place of the canonical input-envelope hash; truncating rewrite of the only durable attempt marker; and disabling the wall alarm before final reporting. The final pins above contain the corrected forms and the narrowed operational claims. These were source-review corrections before numerical execution, not failed experimental attempts or result-driven repairs.
