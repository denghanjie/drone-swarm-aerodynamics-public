# Candidate schedule preflight: independent review

## Finding

The evidence supports a metadata-only candidate correction. The exact source patch changes ORDERS[840137][6] from CB to BC; every other supervisor byte is unchanged. Block numbers are zero-based.

The original production helper rejects the frozen valid schedule. The corrected helper accepts it. All 64 corrected slots match the independently derived plan orders, protocol, configured jobs and cost-validator schedule helper. Original mismatches are slots 28, 29, 60 and 61. Corrected seed orders are complementary in every block and each has four BC and four CB pairs.

The 16 saved checks comprise one expected original rejection, one candidate acceptance and fourteen candidate rejections. The negative cases cover reversed order, missing/extra/duplicate jobs, duplicate slots with unique IDs, wrong seed/block/variant/workload, string seed, boolean block, phase order, unknown phase and empty jobs. Complete test inputs and outcomes are included. Traceback paths are the only redacted outcome fields; flags identify affected records.

## Preservation and method

Independent review reconciled both original-tree snapshots against all 111 current original files and confirmed byte equality. The inventories are intentionally not included. The review checked exact AST-extracted production function bodies and literal constants, the exact patch, frozen input copies, schedule arrays, raw cases and result records. It did not rerun reviewed helpers or execute numerical code.

The completed preflight compiled only the named pure function definitions and populated required constants with literal evaluation. It did not import or initialize the full supervisor. The exact extraction function is provided as a standalone source excerpt without an execution entry point. Full original and candidate source are retained for comparison, not as an instruction or authorization to run them.

## Resource caveat

Recorded metadata execution was approximately 0.04175 seconds wall and 0.04094 seconds CPU. Closed execution artifacts total 430,689 bytes, approximately 431 kB. The raw final count of 429,916 bytes was printed before the remaining 773 bytes of buffered standard output were written. Later display, publication and independent-review files are outside that execution census.

Interactive preparation through test completion took approximately 129.66 seconds, exceeding the requested 30-second elapsed bound. Therefore this is not end-to-end budget compliance. The in-process timers exclude startup/imports, interactive preparation and this review; end-to-end CPU usage was not established. The failed first launcher never started the test harness and remains disclosed.

## Limits

This is a focused schedule check, not exhaustive validator coverage or full supervisor integration. The harness independently parsed plan orders but supplied workload ordering and eight-block structure; this review corroborated those against the plan prose and frozen JSON sources. The cost-validator schedule helper was isolated, not its complete receipt-validation path. Before/after/current hashes establish equality at those snapshots, not an independently attested event history.

No numerical equivalence, performance, physics, safety or old-campaign-success claim follows. The terminal campaign remains unchanged. No numerical successor or publication is authorized by this report. This directory is a locally prepared, screened evidence subset; no remote action was taken.
