# M31 browser-screen seal: supplemental static review

Date: 2026-10-16

Disposition: no remaining blocking static defect identified in the final two-file snapshot reviewed here. This is a narrow source-only supplement, not a qualification of any campaign, numerical result, runtime behavior, or performance result.

## Scope and exact source identities

Source root: `research/m31-browser-screen-2026-10-16`

| Reviewed file | Bytes | SHA-256 |
|---|---:|---|
| `source/seal.py` | 7635 | `4321bd90b63ef2ccba06d6f1b434f0792cac89ded6a4d8a1a5fed74a11f96d3a` |
| `source/controller.cjs` | 11291 | `a3c3797012ff820ed62aee4149e1c4e99caacacf13d1aefa56986d35cb5434cd` |

Read inventory for this supplement: the complete `seal.py`, its subsequent corrective delta, and the `controller.cjs` delta against the previously reviewed controller. Source-only snapshots are retained under `private source-only snapshot directory`. Final identity checks read both live source files and both snapshots and confirmed byte equality. No configuration or raw campaign results were read for this supplement. The earlier report was read only to confirm its byte count and hash.

The previous controller was 11134 bytes, SHA-256 `f5f3dc42b289f5f602865c47d5c56ef7e5a245115e87ae845d018acee87af8fd`.

## Findings and verified resolutions

Two integrity omissions were identified in the initial seal and corrected before this disposition:

1. The seal checked supplied artifact pins but did not require a complete, unique mandatory artifact chain. It now rejects duplicate artifact paths and requires the input index, generation evidence, and generation-child invocation lock for every stage. Candidate and review also require the generation supervisor record and all three p0/p1/p2 closure records; review additionally requires the candidate supervisor record, independent review, and analysis. Existing pin verification checks the required entries against current files. A failed campaign lacking closures remains unqualified.
2. The seal did not compare each stage's retained publication-receipt hash against the receipt loaded by the seal. It now requires every stage's `sourceReceiptSha256` to equal the SHA-256 recorded for the actual `source-publication.json` input.

The corrected source was read and its parser check passed. No further concrete blocking issue was identified within this scope.

## Seal interpretation

The seal reads saved metadata, hashes, and Boolean decisions; it performs no numerical reanalysis and records zero additional science invocations. Its exclusive lock and exclusive final output guard publication, with a cooperative 20-second metadata cap and final payload/storage checks.

Path handling rejects absolute paths, parent traversal, missing pinned files, final-file symlinks, and resolved paths outside the allowed base. Source pins, manifest identity, and the publication receipt are checked. Generation, candidate, and review supervisor records must match their stage and source identity and report closed terminal state and absent child/owned groups. Success, return code, runtime identity, unchanged protected/input/output metadata, positive RSS samples, declared memory limits, per-stage elapsed limits, log limits, and absence of signal, monitoring, cleanup, finalization, and cap failures are all qualification gates. The recorded supervisor elapsed sum must be at most 4500 seconds.

Exactly p0, p1, and p2 closures must satisfy the complete schedule and closure checks, closed browser and absent owned processes, runtime/input verification, no pending transport, no errors, source identity, and per-slot elapsed limits. Independent review and analysis must provide a passing complete audit and `independentAuditPass`. Analysis must retain `practicalRulePass` as null and require review-supervisor closure. The saved performance outcome must be a Boolean.

`evidenceQualified` is the conjunction of the seal's gates. `practicalRulePass` is `evidenceQualified && performanceRulePass`. Qualified evidence with a false performance result is explicitly rejected under the fixed browser practical rule. Successful metadata sealing therefore does not imply practical success. Exceptions and metadata cap failures remain unqualified.

## Controller delta

The sole reviewed controller change constructs the existing page execution configuration as `executionConfig`, records its exact `JSON.stringify` representation as `executionConfigJSON` and its SHA-256 as `executionConfigSha256`, then passes that same configuration object to `window.runBrowserExperiment` through `page.evaluate`.

This delta leaves the schedule, numerical source, source-bundle values, inputs, and execution gates unchanged. The binding is recorded in memory before the page invocation and later persisted with the closure record; this is not a claim of durable publication before execution. Consumption of this binding by the independent verifier is outside this two-file supplement.

## Validation and limits

Validation was limited to source inspection, byte/hash comparisons, Python `ast.parse` on the seal, and Node `--check` on the controller. The Node parser was `pinned Node runtime`. The parser checks passed for the exact final identities above. No reviewed module was imported or executed; no campaign, browser, child process under review, numerical analysis, fault injection, cleanup test, or resource enforcement test was run. No literature was retrieved and no parent source files were edited.

This supplement preserves and does not replace `design-reviews/SUPERVISOR-STATIC.md` (10662 bytes; SHA-256 `1376c40ea28bb09994b3bb988d28959735b86da8a354bd7baf1e167beb31559a`). Its other five reviewed file identities and findings remain as recorded there; this supplement updates only the controller identity and adds the seal review.

The prior limitations still apply: process/RSS/storage enforcement is sampled userspace enforcement rather than a kernel/cgroup or true-peak guarantee; PID/start checks and signaling are non-atomic; short-lived helpers and host/guardian failures can escape those observations; two empty snapshots establish sampled absence; and the runtime inventory is explicitly incomplete for transitive resources. The independent numerical checker and browser harness remain outside this supplement.
