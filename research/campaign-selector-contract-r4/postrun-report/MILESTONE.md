# R4 milestone: eight completed checks, infrastructure stop

**Terminal result: `incomplete_or_blocked`.** R4 attempted a bounded, fixed-record selector contract test. It did not run a new flight simulation. Eight nominal cases, `json-0-initial` through `json-3-final`, have completed receipts recording expected and actual acceptance.

Of 100 planned cases, **8 completed, 1 was interrupted, and 91 were unreached**. Nominal completion is **8/23**. Negative controls are **0/73** reached and positive controls **0/4** reached. This is incomplete contract coverage, not a passed campaign.

## The interruption and retained context

The wrapper reports `FileNotFoundError` after the temporary checkpoint filename `current-context.next.json` disappeared during storage accounting. Static source inspection supports an enumeration-to-stat race with the checkpoint writer's atomic rename. The retained receipt has no traceback proving which census call encountered the disappearance; that exact call site remains uncertain.

The child was killed with return code −9. The last-durable context is sequence **116**, case **`json-4-initial`**, at **`before-case-receipt`**. It records a computed descriptor, matching state bytes, and a saved signature. There is no ninth completed receipt, so those partial fields do not count as a ninth pass. The context is not an exact interruption instruction or whole-process stopped-state capture; work may have advanced since it was saved.

There is no complete child result, child failure report, or final full-input preservation report. The attempt was consumed once and permits no retry. Original records have not been repaired or rewritten.

## Resource and preservation boundaries

The terminal receipt records **0.357154133 s wall** and **0.510175 s whole-tree CPU**, both before that receipt, and **84,267,008 bytes** of conservative RSS accounting. It records **98,669,013 source bytes last observed or reported**, while the conservative complete-read upper bound is explicitly **unknown**. Do not promote that partial read value into a finished total or a proven read-limit pass.

The storage observations are **894,466 bytes for the R4 scope** and **153,989,719 active campaign bytes**, before the terminal swap. Later terminal and presentation writes add storage. These are recorded observation points, not current totals.

The wrapper records unchanged source metadata and unchanged hashes for 55 pinned preparation/release records. Final full-input hashes remain unconfirmed. Those narrower observations do not establish full input preservation or complete qualification.

[Independent aggregate review](SEMANTIC-SUMMARY.md) corroborates these boundaries. [Sanitized aggregate evidence](EVIDENCE.json) contains selected facts and aggregate commitments to the original resource receipt, durable context, and completed receipt set. It is explicitly a derivative, not an original receipt. Detailed source/input/runtime inventories, full checkpoints, state bytes, and private paths are not included or linked.

## What this does and does not establish

The eight completed nominal records support only that completed prefix. No negative control or positive control was exercised, so the planned rejection coverage and full selector-contract gate are unestablished. R4 supplies no audit-equivalence, numerical-accuracy, speedup, or physical-validation result.

The [Three.js presentation](../postrun-demo/index.html) links this result to the unchanged earlier historical viewer. All displayed trajectories predate R4. Historical P1 displays saved poses through **0.990 s** and then holds; its accepted stop was **0.9915625 s**. Playback and interpolation are display behavior, not new simulation or evidence of physical accuracy.

## Delivery and publication

These postrun files are prepared locally, with no browser launch or remote write. Full inventory publication remains pending, and this results-only material is incomplete for full reproduction. Existing repository links remain pinned to commit `5293fba9093179096963784aa8fe765238259eb4`; no R4 publication is claimed.

The R3 standalone offline HTML is already built and delivered, with static checks and unverified browser rendering. A separate R4 offline delivery would require a prospectively approved allocation and build release. No R4 standalone has been built here.
