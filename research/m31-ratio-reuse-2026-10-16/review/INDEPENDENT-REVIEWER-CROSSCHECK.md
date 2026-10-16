# Independent reviewer static cross-check

Date: 2026-10-16. Reviewer: `/root/m31_protocol_challenge`.
Reviewed source: `independent review scratch/review.py`.
Final reviewed size: **54,938 bytes**.
Final reviewed SHA-256: **9981390974b220cd2740e9ceb8e6330a350db97d898d2180720f5ea4c324fbb8**.

## Disposition

**No remaining blocking schedule/schema/count defect was identified in these final bytes.** This cross-check complements the independent-reviewer author's review and the candidate static addendum. It does not establish that either program executes successfully or that a future approximation passes. No reviewer/candidate execution, imports, controls, numerical geometry/solver calls, simulations or acquisition were performed. Validation was limited to source reading, AST parsing, literal extraction, source/reference hash inspection and bookkeeping arithmetic.

## Material finding corrected before freeze

The first reviewed version embedded a 48-character finest-grid reference SHA in `REFERENCE_TRIAL_PINS`:

`2288c5161858dbbe32dbfc7bc5a89e3eef1572f6570ed4fb`

The correct 64-character config/reference SHA is:

`2288c5161858dbbe32dbfc7bc5bb8b30ed26006bc5a89e3eef1572f6570ed4fb`

Because `frozen_config` compares the entire pinned reference list, the typo would have rejected correct evidence before any scientific reconstruction. It was reported promptly to the parent and reviewer author and corrected. AST literal extraction confirms all three final SHA literals are 64 characters and match candidate config; the reviewer author separately hashed all three reference files. Final AST parsing passes.

## Static consistency checks

- The reviewer recognizes candidate instantaneous and cached schemas. Captured-stage reconstruction removes `evaluationAttempted` from derivative metadata, does not require a full geometry witness where the candidate retained only a stage derivative witness, and does not confuse a cached derivative with a freshly solved derivative.
- `stage_cache_index = step // round(refreshDt/dt)` selects the cache at step start and keeps it through ending k4. The three frozen divisors are 2, 4 and 8. The next interval selects the next cache. Boundary timestamps do not prematurely change a stage's roots.
- Positive event/sample commands use the last controller record strictly before the boundary; t=0 uses its controller record. Captured steps use the control selected at the step start. These different conventions match the candidate's event-before-next-control order.
- Events require 201 entries/path, an absent initial LEFT, direct equality between the new cache and saved solver roots, 200 positive LEFT sides, and a terminal audit tied to final state. Positive legacy samples must exactly match LEFT; the initial sample must match RIGHT. No extra observer solve is assumed.
- For complete paths, full-arm counters reconstruct as stage evaluations plus 21 endpoint queries/path. Reuse counters reconstruct as 201 joint evaluations/path and stage evaluations plus 401 cached applications/path. Totals are 11,866 candidate joint attempts and 12,403 path cached applications, with 600 propagation refreshes and three terminal audits.
- The first/last-step capture rule requires 48 global stage witnesses over all six paths. Their projected stage assembly, held commands, saved slopes and accepted-state assembly are checked without full trajectory reintegration.
- All three full paths are checked against the pinned prior endpoints before conditional reuse is admitted. Both-arm refinement, post-refresh identity, all three matched-grid approximation sets and all three pre-refresh event-error sets are reconstructed separately. A failed approximation can coexist with a successful consistency audit; it cannot silently become an eligible approximation.
- Event error reconstruction uses old and fresh rotor loads on the same reuse-arm accepted state. The independent force/moment construction is algebraically equivalent to the candidate's difference of corrections, with mg and mgR normalization. The result comparisons allow small arithmetic rounding differences without replacing the prospectively fixed decision thresholds.
- The final coverage assertions are consistent: 666 instantaneous endpoints/events = 63 full endpoints + 603 reuse events; 1,293 cached reconstructions = three successful analytic-control evaluations + 1,203 event sides + 63 reuse samples + 24 captured reuse stages. Without the conditional reuse branch, the asserted counts are 63 and three. Rejected synthetic guard calls are part of the eight candidate control attempts but do not masquerade as successful cached reconstructions.
- Source-manifest, supervisor artifact, reference and candidate-result pins are checked. The one-pass reviewer keeps full event histories only while auditing each path and returns minimal records for cross-grid comparison. Its final output size participates in the aggregate cap.

## Limits that must remain explicit

The checker requires complete paths before it reconstructs counters. A global interruption or incomplete path therefore fails closed; it does **not** independently audit every retained failure-prefix count. The candidate's repaired cooperative-failure counters were reviewed statically in the preceding addendum. Hard-kill active-prefix loss remains a separately disclosed limitation. A failed audit is not grounds to consume a second invocation.

Current geometry at 24 captured reuse stages is deliberately recorded descriptively. If any such state is outside the current coupled domain, that fact is retained rather than converted into a claim of current closure. Neither a successful consistency audit nor event-only admission establishes domain validity between events. Result prose must not imply that every reuse stage received current-geometry admission.

Initial/controller generation, ordinary unsaved stage dynamics, group summaries and candidate swept-contact checks are not independently regenerated; full reference repetition and static source review supply their limited supporting evidence. Passing saved-state arithmetic is not physical validation, a stability or collision certificate, a rigorous error bound, a speed measurement, or a 5,000-drone result.

This disposition applies only to the final hash above. Any changed reviewer bytes require a scoped delta check before freeze.
