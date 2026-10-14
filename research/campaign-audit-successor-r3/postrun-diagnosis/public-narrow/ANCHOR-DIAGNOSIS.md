# One retained failure: two tick units

**Event-only public derivative. R3 remains terminal `integrity_blocked`.** Detailed retained-file and runtime inventories are withheld pending explicit publication approval. This short diagnosis neither supplies that inventory nor implies approval. See [scope notice](PUBLIC-DERIVATIVE-NOTICE.md).

The saved-state job fully passed 19 cases. Its twentieth case, `json-9-final`, successfully compared baseline B with candidate C1 at the same input, then failed with **“Available endpoint original signature mismatch”**. It did not finish that case. Three saved-state cases and all benchmarks were never reached.

## What went wrong

The historical final state occurs at one second, recorded as tick 6400 using 1/6400-second ticks. The frozen selector copied that tick unchanged into the current 1/51200-second clock. Its anchor calculation divides by eight, selecting row 800 at 0.125 second. The same one-second event corresponds to current tick 51200 and existing anchor row 6400.

The prior data-only diagnosis compared already-retained bytes and outputs:

- Baseline and candidate outputs and class state agree at the failed observation.
- The captured 16 × 17 Float64 input equals the saved JSON final state and dense row 6400; it differs from dense row 800.
- Both captured signatures equal the existing row-6400 signature and differ from the incorrectly selected row-800 signature.
- No audit signature, trajectory or scientific result was regenerated.

This explains the failed anchor selection. It is not a candidate/baseline calculation mismatch in this event, and it does not establish whole-corpus equivalence or a successful repaired suite.

## Check the selected evidence

- [Original failed child receipt](../../implementation/results/receipts/saved-json-states.json)
- [Event-only comparison facts and signatures](EVIDENCE.json)
- [Selected frozen selector source](../../implementation/src/corpus.cjs): the final-state construction retains `run.endTick`, while preflight anchoring uses `tick/8`
- [Selected paired comparison source](../../implementation/src/context.cjs): exact observation comparison completes before the caller's anchor assertion
- [Independent aggregate review](../../postrun-review/REVIEW.narrow.md)

These two source files are selected explanatory code, not a full source/input inventory or executable public reproduction bundle. The source and results remain unchanged.

## Limits

The receipt's `running` label identifies the active case when the terminal exception occurred; the child is no longer running. The successful twentieth observation does not count as a fully passed twentieth case. No numerical retry or repair occurred. Unreached checks remain unknown, the old reference remains unqualified, and no speed or physical-safety claim follows. Any corrected experiment requires a separate prospective plan and authorization.
