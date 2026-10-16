# Prospective resolution review

Reviewer: `m31_verified_literature`. Date: 2026-10-17. This supplements `PROTOCOL-DRAFT-REVIEW.md`; it reviews the parent's proposed per-scene shards, first measured representatives, 60-entry trial ledger, fsynced trial journal and scene-at-a-time checker. No scientific source was imported or executed. No supervision, spec or preserved prefreeze file was edited.

**Disposition: the revised storage and scheduling direction resolves the draft's loose-cap objection, conditional on the explicit geometry/support proof and final source enforcement below.** The arithmetic fits both 64 MiB per scientific scene and 128 MiB across scientific shards. The 384 MiB aggregate is ample for the proposed category caps. This is a static budget review, not evidence of admission, performance, peak RSS or completion within 1,800 seconds, and not a numerical execution gate.

## Independent accounting

Balanced splitting with leaf capacity eight gives 8/16/32 leaves and 15/31/63 nodes at 64/125/216 drones. Across both scene families this is 218 hierarchy tree nodes. The 75,392 terminal bound counts only hierarchy terminals: `2 × (4×64×8 + 4×125×16 + 4×216×32)`. Complete adds `4×810 = 3,240` scan terminals, for **78,632 terminal wrappers**. Parent acknowledged this correction.

The proposed dense support bound is `36 n (edge−1)`: 6,912, 18,000 and 38,880 positive terms per method for the three dense scenes, or 63,792 total; sparse scenes contribute none under the proposed strict-neighbor separation proof. These are prospective upper bounds, not observed term counts. Their use remains conditional on independent proof that the actual decimal-to-binary64 lattice/offset computations preserve the required neighbor/radial margins and that all saved nonzero outcomes are within the accounted admitted shape. Expected admission alone is not such a proof.

| Retained paired scientific component | Count/cap | Bytes |
| --- | --- | ---: |
| Positive entries | 2 × 63,792 × 384 | 48,992,256 |
| Loads | 1,620 × 12 KiB | 19,906,560 |
| Certificate rows | 6,480 × 1 KiB | 6,635,520 |
| Hierarchy tree nodes | 218 × 8 KiB | 1,785,856 |
| All terminal wrappers | 78,632 × 128 | 10,064,896 |
| Other scientific structure | 16 MiB | 16,777,216 |
| Total | | **104,162,304** |
| Margin below 128 MiB | | **30,055,424** |

The 128-byte terminal allowance must mean the terminal's own structure, excluding its entry array elements already counted above. The miscellaneous allowance must explicitly cover entry/row/load array separators, query wrappers, raw/prepared states, solver candidates, permutations, method/scene envelopes, schema/source/runtime metadata, and any timing metadata retained in scientific shards. It cannot be an unnamed allowance later consumed by duplicate scientific copies. Inherited field caps are compact JSON byte caps; pretty-printing requires separate accounting.

For a dense scene, including both methods, its tree and all complete/hierarchy terminals, assigning even the **entire shared 16 MiB miscellaneous allowance to that one scene** yields:

| Drone count | Conditional bound, bytes | 64 MiB limit |
| --- | ---: | --- |
| 64 | 24,600,576 | fits |
| 125 | 36,039,168 | fits |
| 216 | 57,880,576 | fits by 9,228,288 bytes |

The same-size sparse scene is smaller under the zero-positive proof. Keep per-scene and total-shard caps simultaneously enforced. If an unforeseen refusal or implementation error breaks the admitted-shape bound, retain a bounded failure and close the allocation; do not silently enlarge the limits or discard the outcome.

## Rational and reference sizes

Source inspection independently supports the proposed dyadic denominator argument for the actual upright input shape. Quaternion `[0,0,0,1]` leaves axis `[0,0,1]` and horizontal offsets `±arm` unchanged. The four nominal force words have denominator at most `2^57`, and arm has denominator at most `2^58`. Starting native bisection at `[0,1]`, 54 midpoint steps and the final midpoint give a candidate denominator at most `2^55`; binary64 rounding can coarsen this dyadic grid. Thus candidate rotor/collective/force values need denominator at most `2^112`, and moments at most `2^170`. Sums of these dyadics do not multiply denominators.

The independent exact reference's 128 bisections give root endpoints on a grid with denominator at most `2^128`. Its load moments therefore have denominator at most `2^243`. With these small bounded forces/levers and roots in `[0,1]`, numerator lengths are similarly small. A 256-character limit on each signed numerator and positive denominator is generous for those candidate/reference output values. This conclusion does not impose a 256-character cap on every intermediate oracle rational: source weights and coefficient calculations can have different denominators. Any newly emitted control/reference quantity, especially normalized gaps or internal proof evidence, needs its own derivation or an explicit output-size allowance.

A schema-only byte count of the inherited load shape, with all eleven candidate rationals using 256-character numerator and denominator strings, all eleven fixed96 intervals using 108-character endpoints, all seven error strings using 108 characters, and a five-digit ID, is **9,322 compact JSON bytes**. Thus the proposed 12 KiB per-load cap has 2,966 bytes of margin for that unchanged shape. This used synthetic maximum-width strings, not numerical evaluation.

Saved independent reference evidence contains four root intervals and eleven load intervals per drone: `810 × 15 × 2 = 24,300` rational endpoints. A 256/256-character endpoint occupies 527 compact JSON bytes; even the proposed conservative 1,056 bytes per endpoint totals 25,660,800 bytes before wrappers. The complete reference envelope, findings and control evidence must fit the declared **96 MiB total checker category**. Do not interpret 96 MiB as a separate allowance for each scene file plus another 96 MiB summary.

## Aggregate accounting and durable trial identity

Configured maximum category sizes are 128 MiB total scientific shards, 8 MiB ledger, 8 MiB journal, 96 MiB total checker evidence, 16 MiB combined declared logs/metadata, and two 64 KiB supervision reports. Their sum is **268,566,528 bytes**, leaving **134,086,656 bytes** under 384 MiB. Include every retained private raw log and public redacted copy from both stages in the declared log/aggregate scope, along with attempt records, guardian events, failure records and shard manifests. Existing files are not free just because a later stage did not write them. Freeze the recognized file set and category totals together, including temporary shards if they remain after failure.

Selecting the first **measured** representative for each method/scene is acceptable and prospective. Both warmup digests must later match those representatives. All five trial digests for a method/scene bind the same canonical scientific bytes. Journal and ledger duplicate compact trial metadata, not scientific records. Keep the complete 60-entry schedule and every outcome, exact phase timing, digest and selected work counter. Check identity/order/duplication independently of digest equality.

Specify the persistence sequence for representative bytes, shard pins and per-trial journal events. A journal reference to a not-yet-complete shard must be distinguished from a committed shard pin; success requires all six scientific shards durably complete and pinned. An interruption between writes fails qualification and leaves the partial evidence visible. Per-trial serialization, hashing, shard writing and fsync belong outside the declared method interval, within separately accounted harness/stage wall time. These operations can affect subsequent cache/heap/scheduling conditions; applying the same schedule consistently supports a descriptive comparison but not an isolation claim.

## Live-object and final-source conditions

Keep at most the current scene's scientific records and reference oracle live, with one relevant control copy at a time. The kernel still needs to retain first-measured representatives until the paired shard is saved; release later trials promptly. Avoid retaining prior-scene oracle closures, parsed shards, deep copies or serialization strings in summary arrays. Write per-scene checker evidence and retain compact pins/findings after release. Global scene/trial identity checks can operate over bounded manifests without loading every scientific shard together.

This plan removes avoidable all-scene accumulation but does not establish an exact CPython/V8 peak-RSS bound. Preserve the sampled 1 GiB stop condition and one-shot closure semantics. No numerical capacity probe is allocated. Preserve original timing caveats, including shared JIT/GC state, nominal polling versus actual gaps, monitor contention, four descriptive observations and the runner's role as measurement instrument.

Before implementation acceptance: obtain the independent geometry/support proof; freeze the exact overhead and output contracts; align runner/checker/supervisor file categories and limits; audit representative/journal integrity and release points; retain the original mistaken-count spec under `prefreeze/spec-before-count-metadata-correction.json` unchanged as provenance. Source publication and exact-commit verification remain prerequisites for numerical execution. The reviewer has not modified supervision or the preserved typo record.
