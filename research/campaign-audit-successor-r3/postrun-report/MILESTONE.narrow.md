# AUDIT-C1-R3 milestone: results-only publication derivative

**Outcome: terminally blocked with useful partial evidence.** At 2026-10-14 05:41:00 UTC the one-shot attempt began. Its synthetic child passed all **81 cases**; the next child stopped with **“Available endpoint original signature mismatch”**.

The saved-state child completed **20 paired observations**, but only **19 full cases and historical-anchor checks**. The twentieth observation completed before the anchor failure. Across 229 required named cases, the retained review finds **100 passed, one failed while active, and 128 unattempted**. Eleven persisted baseline/candidate artifact pairs were byte-identical.

Exactly two of 82 children started: one passed and one failed. Sixteen further correctness children and all 64 performance children never started. The independent full-corpus correctness gate did not run. No full correctness conclusion, speedup measurement, qualified numerical reference, or physical validation follows.

## Why the anchor comparison failed

The [event-only diagnosis](../postrun-diagnosis/public-narrow/ANCHOR-DIAGNOSIS.md) shows a historical/current timebase mismatch. Old tick 6400 names the historical one-second final state. On the current 51,200-tick-per-second clock, tick 6400 is 0.125 s, which selected dense row 800 instead of the actual final row 6400. The captured baseline and candidate results agree, and their existing signature matches the correct one-second anchor. This diagnoses the wrong target without repairing or rerunning the failed campaign.

## Selected actual evidence

- [Original start marker](../robustness-review/results/WINDOW-STARTED.json)
- [Original synthetic child receipt](../implementation/results/receipts/synthetic.json)
- [Original failed saved-state child receipt](../implementation/results/receipts/saved-json-states.json)
- [Original final-accounting receipt](../robustness-review/results/FINAL-ACCOUNTING.json)
- [Original last-completed-job checkpoint](../robustness-review/results/last-durable-checkpoint.json)
- [Summary-only retained-evidence review](../postrun-review/REVIEW.narrow.md)

Final accounting records **4.2006738310046785 s wall** and **5.604814999999999 s process-tree CPU**, before its own write. These are partial-run costs, not benchmark results. Final in-window frozen/runtime checks were skipped after the failure; later static checks cannot backfill qualification. The release was one-shot, and its start marker says retry is not allowed.

The raw 325,273-byte failure capture is withheld. Its aggregate SHA-256 commitment is `dbdda8c74c5ac50d042eafb2e6d1572683a3602eda052f144c9f8e38f8b8bdbd`. Retained evidence describes current paired outputs and available inputs; the exact-whole-process stopped-state flags remain false.

Aggregate freeze commitment: `39fb07b5b0c461dab938302397914756cd645c81aa16718f4e267100dc54c74f`.

Aggregate release commitment: `7eb939908f3fa82356cb98a3c592f18c203ad6ce549c4df0ac60981e639af0bb`.

These commitments do not publish the detailed inventories or make this a complete reproduction package.

## Historical display and publication boundary

The [selected-record Three.js presentation](../postrun-demo/index.narrow.html) optionally loads the unchanged earlier historical replay. It creates no new trajectories. Historical P1 displays saved poses through 0.990 s and then holds; its accepted stop was 0.9915625 s. Playback and interpolation are display behavior, not additional simulation or physical validation.

Broader inventory publication remains pending. This separate, smaller checkpoint contains selected results and interpretation only, with no detailed source/input/runtime/validation inventory or raw-capture link. It is incomplete for full reproduction. Original records and all prior derivatives remain unchanged. No numerical code, browser, retry, or remote write was executed to prepare this presentation.

The [focused literature supplement](../postrun-literature/narrow/README.md) connects the diagnosis to verification methodology and a proposed future metadata test. It adds no new experimental result.
