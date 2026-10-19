# Independent static correction review

20 October 2026. **No blocking finding in the minimal harness/display correction reviewed here.** This disposition applies to source freeze for the separate corrected allocation; it does not qualify numerical results, the separately reviewed audit, or rendered UI behavior.

Only source-text/byte comparisons and saved failure metadata were inspected. No native module, audit, test, supervisor or browser was executed. No original-checkpoint file was written by this reviewer.

## Observed failure and exact correction

The original [failure record](../../m31-buffered-candidates-2026-10-20/results/failure.json) reports 18 completed queries and an assertion expecting `native-success` but receiving `domain-refused`. Its final two journal entries are calls 17 and 18, control stage 8, methods F and C. Both record `domain-refused/native-admission` and reference the same complete semantic body. C records the intended global-screen fallback. The source compares F/C semantics before asserting the expected status, so this stopping point is consistent with a wrong control expectation rather than an observed F/C disagreement.

The corrected `source/run.cjs` has exactly one textual change from the original: the expected control status now selects `domain-refused` when `s === 8`, retaining `input-refused` for `s === 11` and `native-success` otherwise. The F/C full-semantic comparison still precedes that assertion. The [protocol](../PROTOCOL.md) identifies the precise stage-8 refusal as `domain-refused/native-admission`; the corresponding saved-evidence audit change is owned by the protocol/audit reviewer.

Stage indices are zero-based: stage 8 is the ninth control pair. The original run stopped inside the control loop before any warmup or measured stream query. Its small-control timings provide no N=1,000 performance result. The [original failure summary](../../m31-buffered-candidates-2026-10-20/FAILURE-SUMMARY.md) and original raw evidence remain the record of that closed attempt.

## Unchanged scientific and performance contract

Directory comparisons found `source/candidate.cjs`, `source/candidate-kernel.cjs` and `source/candidate-cache.cjs` byte-identical to the original checkpoint. The run-file diff establishes that the following are unchanged:

- The common saved N=1,000 input path and binary64 decoding.
- All twelve control recipes, their order, cache resets, and expected cache-event checks.
- The eight prescribed position/force perturbations and all stage-generation expressions.
- Candidate half-width, screening thresholds, current numerical calculation and baseline dependencies.
- Full semantic normalization/exclusions, input-preservation checks, derived-load checks and witness collection.
- One warmup pair and eight measured pairs, alternating FC/CF order, reset/query timing boundaries, and cold/rebuild inclusion.
- The maximum 168 native calls and existing time/storage bounds.
- The keep rule: median of eight paired C/F sequence ratios at most 0.90 and at least seven strict wins, conditional on all correctness gates.

There is no timing-based tuning, changed input recipe, new candidate variant or relaxed F/C output tolerance in this correction. The newly allocated attempt explicitly repeats all 24 control queries before the previously unexecuted 144-query warmup/measurement panel. It does not attempt to resume the original run at call 19 or reuse original control successes as fresh qualification.

## Display and isolation

The entire `viewer/` source directory is byte-identical to the original. The only difference in `source/ui.cjs` is its local viewer URL, which now points to `m31-buffered-candidates-corrected-2026-10-20/viewer/`. Geometry/table/decision checks, the exact one-launch assertion, browser ownership hook, reset check, corrupt-evidence test and display timeouts remain unchanged. The native and UI supervisors also remain unchanged in the compared copies.

Paths derived from each script's own directory place source manifests, receipts, exclusive result directories and display outputs under the corrected checkpoint. The corrected protocol explicitly preserves the original 18-call failure and requires a new source freeze/public verification before the new attempt. This is a separate bounded allocation; the old allocation is not reopened or rerun.

The audit's refusal-schema correction and its final byte-level source review are outside this report. The parent still owns the full corrected manifest, source publication verification and later execution decisions. The earlier static review's limits remain: no numerical or visual pass may be inferred from this source comparison.
