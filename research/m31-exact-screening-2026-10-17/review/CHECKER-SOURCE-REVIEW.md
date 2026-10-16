# Independent exact-screening checker source review

This review concerns source authoring and static inspection only. No scientific module was imported, numerical expression evaluated, fixture generated, checker/kernel run or closed suite reopened. No candidate implementation contents were read. No external operation or new agent was used. Five inherited files were read within the fresh limit of sixteen; exact paths and hashes are in `CHECKER-DESIGN-READING.json`.

## Authored artifacts and preserved drafts

- `source/check.py`: 70784 bytes, SHA256 `df3c6330dc2f8577819a582f88d8a2a0379fc9377f8b7ec3097dc6565cee2599`.
- `source/result-contract.json`: 8505 bytes, SHA256 `b24b550aa1df45680d92b069a008be568cf3a4ff067a051c532cbaff7bdd2cf3`.
- `source/pair-reference.py`: 44757 bytes, SHA256 `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0`, unchanged from the published independent reference.

The initial design report and inventory are retained under `prefreeze/checker-design/`. The published coupled independent checker is retained as source text in `prefreeze/inherited-independent-check.py`. The first complete new checker and result contract are retained as `prefreeze/first-complete-check.py` and `prefreeze/first-result-contract.json`. The sole subsequent checker correction before this review removes an unused provisional width assignment; the actual width formula was already correct. The contract added an explicit requirement that fault controls trigger their intended independent core failures.

The new checker source copies only selected independent arithmetic and certificate routines from the published coupled checker. It does not call that checker's old regeneration, main, validator or controls. The independent pair helper's old suite/main/generator are likewise never called. The new main verifies the entire local source manifest and immutable original helper digest, then reads, rehashes, compiles and executes exactly the same helper source buffer. A cached bytecode artifact cannot replace the hashed source. Public publication and independent exact-commit manifest verification remain the parent's prerequisite before the allocated execution.

## Contract resolutions adopted before implementation

The final compact interface is `CONTRACT-DRAFT.md` plus `source/result-contract.json`. The original broader design recommendation is retained rather than rewritten as though it were the final contract. Specific resolutions are:

- Every scene has complete and hierarchy method records, each starting from its own preparation. Exact prepared data, canonical model result/witness, positive coefficient list, candidate bits and complete load certificate must agree within that scene after each method passes independent validation.
- Query receiver `i` and entry source `j` are original input indices. Tree permutation, prepared/candidate/load identities and result witnesses use stable IDs. Independent lookup maps this boundary explicitly.
- Tree leaves retain their incoming recursive order; a root of at most eight members retains input order. Exact center/axis extrema use canonical rational endpoint pairs. Node IDs and child/range structure are preorder and deterministic.
- Empty self-only terminal sets are explicitly allowed, unlike the initial design preference. They cover zero nonself pairs but still contribute actual node/predicate/terminal work according to the fixed traversal.
- Preparation precedes a complete global proof. A completed false proof triggers a full scalar fallback with no tree. Administrative exceptions fail the stage; they never become a zero, model rejection or automatic fallback.
- Positive output contains only the fixed96 coefficient interval. The independent full oracle still proves admission/caps and each coefficient enclosure; unchanged internal five-interval scalar arithmetic is the candidate source reviewers' responsibility.
- No stress exception is allowed. Every implicit zero is checked against the full independent oracle. Unexpected candidate uncertainty or unresolved independent reference prevents qualification.

## Independent coverage, proofs and loads

The checker independently regenerates all new literal inputs, constant expression-graph bits and prepared operands. Expected-class labels do not drive admission; disagreement is visible and fails the prospective claim. The declared 18 scenes, 312 drone records and 46744 planned pairs per method are validated at the authorized run. Every globally valid pair is independently classified, even after another pair rejects a scene. Old numerical suites are not executed.

The checker recomputes all five global magnitude-box proofs, deterministic tree construction, fixed-order node zero predicates and complete traversal/work counters. Reported tree bounds must exactly match independently reconstructed extrema and membership. Each scan/leaf complement is an explicit zero claim, not a count shortcut. Every zero node also receives both its exact interval proof and a finite full-member oracle cross-check. Terminal effective member sets must partition exactly the nonself source universe. Positive/rejected/unresolved membership and canonical refusal order remain independent of tree order. Actual positive status counts even when a coefficient lower endpoint is zero.

One outward fixed192 coefficient reference is retained per active pair. The full-model topological reference uses exact positive weights, fixed192 predecessor source intervals and two fixed128 cubic endpoint bisections, with exact root one at zero alpha. All admitted root/load references are retained once per scene. The shared certificate verifier checks full returned coefficient/row/defect boxes, point upper factors, exact candidate domain and identities, corollary and independent-root containment, all-three-coordinate signed loads and full-returned-box normalized errors. Tolerance is exactly1/100000000; sound loose certificates remain visible tolerance failures.

## Fault controls and equality protection

Sixteen fixed mutations are implemented as declared in the contract. Witness selection is prospective and deterministic. Coverage controls include missing/duplicate terminals, a false node zero over a proved active member, and an omitted positive leaf entry with its zero count adjusted. Further controls corrupt deterministic membership, a witnessed bound extremum, prepared offset identity, failed global proof, complete fallback, coefficient, affected root, candidate, true nonzero error, and scene membership/order.

The strict zero-error witness requires the exact recorded candidate to lie outside its independent root enclosure and records a positive rational normalized separating bound. The false-root-one witness requires an independent root upper strictly below one. The coefficient-zero witness requires a strictly positive independent coefficient lower bound. Missing applicable witnesses fail control coverage.

A single-method mutation must not pass a control merely because common outputs differ. The core therefore checks method equality only after both independent method validators pass. Each control also records a fixed acceptable scientific/coverage failure-family list and requires an actual matching core error. Equality-only rejection cannot satisfy `intendedCoreFailure`. Mutated output documents are not retained or emitted; only compact witness/verdict/error records are saved. Journal comparison is separate and never used to detect a mutation.

## Output and runtime bounds

The CLI remains `--spec --input --manifest --output --root`; kernel input is `results/screening-results.json` with its `.jsonl` completed-scene journal. The checker streams journal lines and validates exact header, each scene row and completion wrapper. It preserves exclusive output and rehashes all frozen sources after its work.

The adopted aggregate allocation is384MiB, with kernel and journal128MiB each, checker96MiB, bounded logs/metadata and final-report reserves. This is a static protocol budget, not a measured memory or runtime claim. The checker enforces fixed96 integer length108, canonical load rational integer length4096, tree numerator310/denominator324, compact nonzero entry384B, certificate row1KiB, load96KiB and tree node8KiB.

Independent reference output is emitted only once per scene and never as a full pair-oracle dump. The fixed maximum312 drone records has30 rational endpoints per drone: four root intervals and eleven load intervals. With a conservative8256-byte rational allowance this component is bounded by77,276,160 bytes; control witnesses are each bounded64KiB, errors are at most48strings of256characters, and source/runtime metadata and36method summaries fit the remaining96MiB envelope. Actual payload length is checked before exclusive write. A breached output/runtime/RSS bound remains a failed allocation with no retry.

Stable report fields are `verificationPassed`, `fullQualification`, `tolerancePassed`, `totalRecords`, `qualifiedRecords`, `admittedRecords`, `tolerancePassedRecords`, `toleranceFailedRecords`, `methodEqualityRecords`, `faultControls` and `scenes`. Each scene retains its independent class/witness, prospective label agreement, two method mode/work/rule/verification summaries, within-scene equality and its single admitted reference evidence block.

## Static review disposition

The mathematical reviewer found no blocker in the first complete source's independent interval/tree/coverage/certificate/control sections and is checking the final dead-assignment-only delta. Final protocol review remains pending at the time this note is written. No scientific outcome, performance improvement, physical validity, dynamic qualification or novelty claim follows from source approval. The finite suite cannot qualify the2000000-positive-term overflow boundary or the original full-scale objective.

## Final outbound-serialization correction

The protocol reviewer confirmed the targeted-control and equality ordering, then identified one outbound-bound gap: generated reference/witness rationals used a serializer without the4096-character cap enforced on parsed candidate rationals. Before freeze, `fraction_wire` was changed to reject any emitted numerator or denominator longer than4096characters. This makes the static per-rational allowance explicit for generated evidence as well as inputs. No numerical algorithm or acceptance inequality changed. The immediately prior source is preserved in `prefreeze/check-before-outbound-rational-cap.py` at SHA256 `cffbcbbb8f714a1f5db72b2ae0bcd22a8c136e1a4d5d979365a7f5c3854823de`. Mathematical review had approved that source; narrow review of this serializer-only delta is pending. AST parsing only was repeated.
