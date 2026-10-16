# Prediction helped, but did not meet the accuracy screen

We tested whether extending the recent trend in rotor-load ratios could replace holding the previous values. The test used all200 saved refresh endpoints on the already examined16-drone, two-second trajectory. The prediction used only earlier actual values; no new flight was simulated.

**Result: reject this fixed predictor for the declared screen.** Its largest errors were smaller than holding old values, but all three remained above the predeclared0.001 limits. Four predictions also slightly exceeded the model’s allowed ratio range. All200 targets were retained and scored.

| Error, in its declared reference units | Hold previous value | Straight-line prediction | Limit |
|---|---:|---:|---:|
| Individual rotor / nominal hover | 0.034641 | 0.018768 | 0.001 |
| Total force / weight | 0.022282 | 0.009938 | 0.001 |
| Turning moment / weight × motor-arm radius | 0.010176 | 0.004128 | 0.001 |

At startup, only one earlier value exists, so the predictor must hold it. That caused the largest rotor error. However, the199 later endpoints also missed all three limits. Simply excluding startup would not rescue the result on this unchanged recorded path. The force and moment peaks occurred later, around0.43–0.45s.

The practical finding is narrower than “prediction does not work”: this particular straight-line rule is insufficient at the tested10ms spacing. It does not establish what a different prediction method or a newly integrated flight would do. The calculations remain physically unvalidated, and there is no speedup or novelty claim.

The independent audit passed 1,098,131 checks and separately reconstructed the strict qualification decision. Both one-shot allocations closed successfully, with no rerun or tuning. Source commit: `5a555210fa6012a9df334ecfc4ae0c9a666b0e82`.

[Open the Three.js diagnostic](viewer/) to see the original exact poses colored by each method’s saved load error. This is the same recorded trajectory under both displays, not two different flights. [Frozen protocol](PROTOCOL.md), [all event records](results/events.jsonl), [saved summary](results/summary.json), [independent audit](results/independent-review.json) and [claims and limitations](RESULT-CLAIM-LEDGER.md) retain the full trace.
