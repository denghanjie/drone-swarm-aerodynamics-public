# Independent static review of the tree-first comparison driver

Reviewed before scientific execution on 17 October 2026. This review used source
reads, JSON metadata/shape inspection, SHA-256 hashing, and `ast.parse` only. It did
not import candidate or scientific modules, run fixtures, generate references,
run either validator, invoke a browser, or change the fixed corpus.

## Verdict

No deterministic scientific-interface or validator integration blocker was found
in the inspected sources. The fixed cases, frozen dependency fields, saved native
adapter, and canonical coverage comparisons are consistent. This is a static
verdict, not evidence that the run fits its budget or that any equality/control
has passed.

Four pre-freeze hardenings were recommended, adopted, and independently re-read:
recheck the 600-second cutoff after source verification; explicitly clear both
completion flags in the general exception and deadline paths; pin/verify the
event journal in closure; and compare the complete saved/new positive maps before
adapting the saved dense record. These changes preserve the scientific algorithm,
corpus, thresholds, and allocation. The final driver parsed successfully and has
no remaining static blocker identified by this review.

The source manifest/publication receipt did not exist when this review began.
Their completeness, runtime pin, committed/public byte equality, and launch gate
remain the parent's responsibility. A claimed successful scientific outcome
requires a successful terminal receipt, all controls, and preserved files.

## Inspected candidate identities

The final static pass inspected these bytes:

| File | SHA-256 |
| --- | --- |
| `source/run.py` | `a9cb32ae57b4081537f6a98aa88f9d8cbae790db6274d92dfe3e7af8ed917bb7` |
| `source/validate.py` | `acdf86593617b589ac6e640bb86c7416528db206d7fb59d148e6b2565690a51a` |
| `source/tree-reference.py` | `d08efc5e80910066d061a664aa7902c7ae7bab27dc710f5c00c9b2bf1671df65` |
| `source/corruptions.py` | `6a8163431b4824b113add66535cf5586b70698b07f8da817097b99fbcc5c5746` |
| `source/cases.json` | `4ecab97812205ac99f41b4f7c1e9ff1f0e83f278d4ea9a091d3d0b7895590193` |
| `PROTOCOL.md` | `043eb02d3c25b5caa69c826c2b5bc20dc0c7967b771120452e5dcec55b655e87` |
| `REPRODUCE.md` | `28bc233b269bf1fee2bd5d6d1c3bed263cd97a1f5dbab69d10cef7d1f3007581` |

All four Python sources parsed successfully as ASTs without import/execution.
The initial driver hash was
`e40c81fedde4c577622ec1dcc1b754be40a79edd338ed8b06196ef59385d7702`;
only the four hardenings described here changed it during this review.
The dispatcher dependencies match its declared pins:

- Frozen pair reference:
  `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0`.
- Frozen semantic reference:
  `ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c`.

## Dependency and record contracts

Metadata inspection establishes exactly 24 unique case IDs. The first 18 IDs,
sizes, and expected classes match the complete exact-screening scene list in
order. The six raw-word inputs have the expected `drones` object shape and 17
state words per row. Declared sizes produce 79,048 logical rotor-source pairs per
variant, and the maximum is 64. This calculation uses declared metadata only; no
scientific result was regenerated.

Fresh and old specs have equal constants, PI word, corners, reference
coefficient/source precision, root bisections, and positive-term cap. The fresh
spec supplies `maxDrones=180`, `leafCapacity=8`, `192/192/128`, and cap 2,000,000.
`pair.constants_from_graph` returns precisely the integer-word map expected by
both reference modules. The counted helper adapts only scene-level `literal` for
saved words; delegated scalar `oracle_case` remains the frozen function and
continues its own parse/preparation. Every scalar entry passes the one shared
counter and administrative poll.

The frozen semantic reference provides the target fields used by `wire` and
`validate`, plus dense `lookup`, `plans`, tree `boxes`, and `geometry` where
applicable. Globally invalid targets omit `guardEvidence` and `geometry`; the
validator safely compares guard evidence with `.get`, performs no geometry access
for the empty query plan, and handles an empty pair list. `tree` and `globalGuard`
are present and `None` in this branch. The candidate's explicit empty geometry
does not introduce a field-access error.

The driver deliberately uses its own nested-`oracle` wire format, not the
dispatcher's optional flattened `to_record` format. Its sparse positive adapter
reads that nested shape consistently. The fresh frozen reference writer uses the
same `interval_wire`, original input load order, four root boxes, and
`rotor/collective/force/moment` load keys as this driver's `wire` function.

Saved generation descriptors provide `semanticInputSha256` and
`input.sha256`. `native.reference_target` takes exactly the raw input, full dense
saved reference, constant-word map, and semantic digest supplied here. It accepts
the saved prepared shape `{id,value,rejection}`, validates the five prepared
geometry/force keys, and maps `force/moment` to native `worldForce/worldMoment`.
The driver adds `inputFileSha256`, which `native.audit_evidence` requires.

The two saved fresh references each contain 16,128 pair records, admitted `loads`
status, compatible graph metadata, and 64 load/prepared rows. Their pair rows are
flattened `{i,r,j,status,branch[,coefficient]}`, matching the adapter loop. Saved
browser calls are ordered `(fresh-a-t5,F)`, `(fresh-a-t5,L)`, `(fresh-b-t5,L)`,
`(fresh-b-t5,F)`; saved checker reports use that order and are qualified. The four
saved corruption IDs match the frozen `corruption_checks` function. No browser
or trajectory function is invoked by the new driver.

The frozen `arithmetic_fixtures` body contains the prescribed 14 checks. The driver
requires count 14 and every pass flag. It also requires all four native reports
and all four load corruption reports to equal the saved reports, not merely to
share an aggregate success flag.

The finalized source manifest must cover the new source/cases/protocol/reviews;
the frozen pair, semantic, native-check and fresh-spec sources; the old scene spec;
fresh generation/browser/check records; all six selected raw input files; and the
two saved fresh reference records. Merely declaring a number of pins cannot
substitute for this exact dependency closure.

## Independent validation logic

`validate.py` imports only `Counter`, never the dispatcher. It derives the exact
tree, traversal plan, bounds, geometry, and scalar oracle results from the frozen
full target. It compares canonical scene fields, guards, exact roots, signed loads,
and tree before accepting coverage.

For every canonical receiver/rotor query it requires the exact self permutation
position, expected terminal count, contiguous nonempty ranges covering `[0,N)`,
original-index membership equality, self-adjusted count, node/range identity, and
terminal kind. Zero terminals must have a passed global guard, an independently
recomputed node proof, no expanded `sourceIndices`, and all omitted full-oracle
members zero. Scalar terminals must list exactly the sorted original indices in
their range. Scene sets must be disjoint, complete, and match the ordered scalar
pair array without duplicate keys. Actual scalar IDs, indices, oracle status and
branch, and positive intervals are compared with the full oracle. Complete
positive support is checked separately.

All 13 work counters are validated: eight against independently counted
membership/outcomes and five against the frozen full hierarchy plan. The
singleton/self-only terminal case is compatible with the old plan; ranges remain
nonempty while their nonself count can be zero. Global preparation refusal has
zero required coverage despite retaining the logical planned count.

The validator does not require a group's `proofRule` to equal every omitted
member's scalar first-zero branch. This is correct: a legal upstream group can
contain a member whose individual oracle stops earlier at neighbor.

The six fixed corruption mutations reach their intended validation checks by
source inspection: false zero proof (`node-proof-rule`), dropped scalar row
(`scalar-pair-canonical-membership`), equal-count duplicate source
(`scalar-member-list`), forged bound (`tree-identity`), center-guard result changed
to zero (`scalar-oracle`), and stable source ID swap (`scalar-j`). The mutation
module catches only the validator's intentional exception class and requires an
exact predeclared code; missing witnesses or administrative exceptions cannot
count as detected controls. These are prospective paths, not executed passes.

## Containment and failure-path recommendations

The inspected driver checks the executable bytes/version and isolated/no-bytecode
flags, expected manifest digest, source-publication receipt fields, source pins,
one-use markers, and available window before scientific imports. It runs one full
and one tree dispatch per fixed case and has no retry loop. The common scalar
counter refuses before an oracle call above 160,000. The theoretical fixed-corpus
two-variant count is already below that ceiling even without pruning.

The 540-second alarm/polls cover scientific work, with up to 60 seconds reserved
for closure. The protocol correctly states these are best-effort in-process
limits and claims neither hard OS memory containment nor an external guardian.
An interrupted root/helper call can fail the allocation; that is preferable to a
silent alternate scientific result. Exclusive output creation, individual byte
limits, total result-byte checks, and retained partial files support the no-rerun
policy. Lack of a successful terminal index cannot qualify.

The pre-freeze recommendations, all resolved in the final hash above, were:

1. Repeat the remaining-window check after `verify(root,manifest)` and immediately
   before allocation. Otherwise pin verification can consume part of the nominal
   600 seconds after the only check. **Resolved:** the final driver checks
   `full-budget-after-pin-verification` before creating the allocation directory.
2. Set `complete=False` and `qualified=False` in the general exception handler.
   A signal can arrive between the success assignments and leaving the `try`,
   producing `status='failed'` with a stale true flag. The exit code already fails,
   but the saved receipt should have no conflicting qualification flags. Also
   clear completion on total-deadline failure for a consistent receipt contract.
   **Resolved:** both paths explicitly clear both flags.
3. Close and pin `events.jsonl`, include that pin in the index/protected list, and
   verify its bytes in closure. The initial implementation counts journal bytes
   but `outputsPreserved=True` only verifies artifacts written by `save`.
   **Resolved:** closure closes the stream, bounds journal/total bytes, saves an
   `eventJournal` pin, adds it to the protected list, and rechecks it with the
   other artifacts.
4. Before filling the saved dense adapter, require its positive key set to equal
   the new sparse positive key set. The current dictionary lookup catches a
   missing new positive, but an extra new positive is not consumed by the saved
   mask. Complete candidate/full equality and saved load equality are already
   strong checks; explicit support equality makes the adapter's own promise
   direct and independently inspectable. **Resolved:** the final driver compares
   the complete key-to-coefficient maps, which is stronger than key-set equality.

No new fixture, scientific execution, or authorization to exceed the fixed
allocation follows from this review. The final static verdict is ready for the
parent's source freeze and publication gates; those gates and the prospective
execution outcome remain separate evidence requirements.
