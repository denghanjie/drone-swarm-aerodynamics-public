# Proposed independent saved-only capacity audit

17 October 2026. This contract and `saved_audit.py` are proposed audit source.
They do not authorize execution. The parent must inspect both and the exact
`audit-source-manifest.json` before authorizing the sole invocation. The
scientific driver, frozen static review and earlier packages remain unchanged.

The only scientific allocation being inspected is source commit
`7528347a34c6638429430268ad6cc9e4bcb6e5f0`, source manifest
`d404173845985fd2eef76c9526adefb981c1486a49f7b8aacd1a6e565cf9ba5f`, with 767 file
pins. Its three saved cases are fixed in this order: fresh-a-t5 (64 drones),
dense-180-filter-cost (180), sparse-180-filter-cost (180). The scientific
allocation has already terminated; this audit cannot regenerate any case.

## Allowed operations and finite invocation

Use the scientific manifest's pinned macOS Python executable and full version,
isolated with `-I -B`. The entry point accepts only repository ROOT and the
parent-reviewed audit-manifest SHA256. Before launch a full 120 seconds must
remain before 03:00 UTC, 17 October 2026. The audit creates exclusive
`AUDIT-STARTED.json` and refuses an existing marker or `saved-audit-result.json`.
It starts a 115-second inspection timer, then at most the remainder of a total
120 seconds for byte-preservation checking and report closure. Expiry signals
repeat; this is in-process containment, not an external guardian. A timeout can
prevent a final report, leaving its exclusive marker and any partial report as
the consumed allocation. No failure, timeout, schema disagreement or wrong
threshold permits a retry within this contract.

Only Python standard-library source is imported. The audit reads JSON and
bytes, checks hashes, compares saved rational endpoints with `Fraction`, and
performs integer/set/index bookkeeping on saved records. Its only subprocess is
local read-only `git cat-file --batch`, in bounded batches with timeouts, to
compare the frozen 767 source blobs and source manifest against the stated
commit. No scientific helper, driver, oracle, checker, native or browser module
is imported or called. No geometry, zero predicate, coefficient, root, load,
fixture or physical measurement is newly evaluated. There is no network access.

The audit manifest pins this script and contract, every scientific-source pin,
the scientific source manifest/publication receipt, STARTED, and all eight
scientific result/profile/journal/index files. It records
`executionAuthorized: false` because it is prepared before parent review; the
parent's separate decision supplies authorization, without rewriting this
manifest after review. Scientific source pins are checked locally and against
committed blobs. Newly saved outputs are checked against their pinned local
bytes; they are not falsely described as already in the source commit. The
saved publication receipt is inspected and bound to that commit/manifest;
public network verification is not repeated by this audit.

## Independent saved comparisons

1. Require exactly three completed, accuracy-qualified cases, fixed order,
   sizes 64/180/180, suffix counts 7,408/34,707/3,340, positive counts
   228/3,056/0, total 45,455 suffix calls and 273,888 logical pairs. Recompute
   preparation/validation, operand-lookup and zero pair-preparation accounting.
   Preserve the prior qualified 24-case index and passing saved audit as
   prerequisites; they are not executed again.
2. Validate stable IDs, all 17 raw binary64-word strings, ordered prepared/load
   IDs, admissibility and current solve-order permutation. For fresh-a, require
   complete structural **and byte** equality to its saved prepared wire and
   exact original raw-input equality. For each 180 case, require the entire
   ordered raw input and both complete ordered producer prepared lists to equal
   the new record. Require the entire ordered root/signed-load list to equal
   saved independentReference192, including every canonical rational endpoint,
   four roots, four rotor loads, collective, three forces and three moments.
3. Translate old producer indices through the saved stable-ID list. Require
   complete producer queries, no duplicate positive keys, exact equality of the
   two saved 96-bit positive maps, and exact equality of new positive support to
   both. Check each new 192-bit interval is contained within the saved 96-bit
   interval using exact integer/rational arithmetic. The two saved independent
   180 references have no pair-coefficient table; independent-192 pair equality
   remains explicitly unavailable. Their old solve objects have no traversal
   order; a comparison to such an order remains unavailable.
4. Independently reconstruct the saved tree's parent/child/range structure,
   leaf capacity, permutation and complete ordered receiver/rotor queries.
   Require terminal ranges to partition every permutation exactly once, adjust
   counts for the receiver itself, and map leaf source indices back to original
   input IDs. Require canonical new scalar records to equal those leaf members
   with exact receiver/source index-to-ID association. Recompute all coverage
   work counts from saved partition structure, scalar statuses and saved rule
   labels, including node visits and declared rule-test count. Zero-rule names
   are validated as saved labels; no zero predicate or node geometry is
   reevaluated and no new full-pair oracle is built. The audit verifies the
   combinatorial partition, not a new independent physical zero proof.
5. Check every profile function ID, filename, line, count, time and caller edge;
   reject absolute or private machine paths. Caller tuples retain their
   total/primitive/own/cumulative ordering. Require nonnegative finite times,
   valid unique caller references and reconciled primitive/total function call
   sums. Reconcile the sum of own times with the recorded total using only a
   1e-9 absolute/relative floating bookkeeping tolerance, and require it not to
   exceed the observed profiled wall by more than 1e-6 seconds. These tolerances
   concern serialized clock sums only; all scientific comparisons are exact.
   Require one prepared and one tree regeneration entry, expected suffix and
   preparation call counts, and no binding-control invocation. Cumulative times
   are never summed across functions or converted into unprofiled speed.
6. Validate the nonnegative separate outer phase observations and their sum
   within the declared pre-index wall, closure under 60 seconds and total under
   600. Confirm wall/RSS observation labels, monotonically nondecreasing macOS
   process-lifetime RSS byte samples, and independently recompute the separate
   60-seconds-per-profile/1-GiB recorded capacity hurdle. This is a check of saved
   observations, not a new timing or memory experiment. Accuracy and capacity
   remain distinct, including a possible accurate capacity failure.
7. Require the exact six alternating start/complete events, matching case pins
   and shared suffix counts. Bind source/publication/STARTED/index identities,
   public-before-start chronology and full 600-second reservation. Require
   exactly the eight scientific result files, at most 32 MiB per evidence file,
   and at most 256 MiB total including STARTED; recompute the index's pre-index
   byte count. Recheck all audit-source/input pins at closure.

## Preserved report and claim limits

The audit writes only its exclusive marker and at most 1 MiB
`saved-audit-result.json`. The report contains case comparisons, endpoint and
coverage counts, profile validation, recorded phase observations, recomputed
capacity hurdle, source/output preservation and any failure. It records its own
wall observation before report serialization; it is not an exact completed-
process clock. Unexpected exception output is restricted to exception class;
audit failures use bounded repository-relative reason codes.

A pass means the saved three-case evidence satisfies this audit contract. It
does not create independent 192-bit coefficient equality for the 180 scenes,
reevaluate zero proofs, extend native qualification, show production speed or
strict 5,000-drone accuracy, validate measured flight, establish novelty, or
authorize a cap change, rerun or automatic optimization. Failure is retained
and cannot be repaired by reexecuting the scientific cases or this audit.
