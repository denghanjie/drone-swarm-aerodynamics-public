# Clarification of the published query timing boundary

The prior next-decision prose warned about removing dense classification tensors from a prospective production query. Source inspection now resolves that ambiguity: **the timed L and F queries already pass `fullSymbols=false`.** The dense tensors are present for separate qualification builds and retained scientific evidence; they are not materialized inside the measured `kernel.query` calls.

Evidence in the byte-pinned browser source package:

- `source/kernel.cjs`, function `query`: F calls `build(states,'screen',false,guard)`.
- `source/lean-anchor.cjs`, function `query`: L calls `build(states,'lean',false,guard)`.
- Both builders allocate dense symbols only under `fullSymbols ? ... : null`; per-class symbol counts and other metadata still exist.
- `source/browser.js`, `recordTiming`: measures the unchanged returned query total, persists it, then performs complete validation against a separately qualified builder.

This is a source-reading correction to planning interpretation, not a new timing run or change to the prior result. The source, raw timings, qualification and result manifest remain unchanged. The prior full-tensor record remains valid evidence for qualification coverage. No future speedup may be attributed to removing dense allocation that was already absent from this timed boundary.

The real interface question remains substantial: existing queries construct sparse coefficients, dependency graph/order and metadata, solve, evaluate residuals, and consume outputs. A bounded-omission method cannot return exact omitted coefficients and exact full residuals without paying to obtain them. A changed production-load contract must therefore be explicit and shared by F, an exact hierarchy and the approximate method. Any requalified baseline remains a new experiment; the closed query times are historical context if those tasks change. Exact admission/rejection semantics and diagnostic/certificate work must be treated separately and honestly.
