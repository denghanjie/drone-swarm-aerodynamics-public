# Why our neighbor lists stayed almost full

23 October 2026. **Making the existing buffer smaller has very little room to help on these saved clips. A different distance rule has more room, but we have not shown that using it would make the program faster.**

Think of each drone keeping a list of other drones it must check. Our previous method remembered that list to avoid rebuilding it repeatedly. The problem was that it kept every other drone on the list.

We have now examined all 1,920 saved calculation stages from twelve short clips of 64 drones. We counted what the existing program had already recorded; we did not run another flight or calculate new forces. An independently written checker reconstructed every row and total from the original records and agreed exactly.

| What the saved records show | Count across the saved stages | What it means |
|---|---:|---|
| All possible directed pair checks | 7,741,440 | One drone checking another counts separately from the reverse direction. The same pairs recur over time. |
| Pairs rejected by the existing 4 m axis rule | 320, about 0.0041% | Even an optimistically tight buffer using this same rule would still retain almost every pair. |
| Pairs rejected next by the existing 3 m center-distance rule | 753,910, about 9.74% | This different rule offers a larger possible target for avoiding repeated checks. It already exists in the baseline. |

The first finding is **small, not zero**. There were two axis rejections per stage in one 160-stage clip; the other eleven clips had none. Our prewritten rule said to retire buffer-width tuning only if there were no axis rejections at all. That condition was not met, so the formal result remains “unresolved.” We will not rewrite it as a successful retirement test. The tiny measured upper bound nevertheless makes buffer-width tuning a low priority for these clips; that is a research judgment, not a new pass/fail threshold.

The second finding suggests the next question: can we remember which pairs are definitely beyond the model's 3 m cutoff while the drones move, without changing the answers or hiding a reason for the model to stop? We must establish that rule first. Checking and maintaining the new list could cost more than it saves; 9.74% of pairs does not mean 9.74% faster execution.

The one previously recorded near-field refusal is still present, at trial time 3.62 s. It is not a new failure or a collision. A pair that contributes no force may still cause this refusal, so simply keeping only force-producing pairs would be unjustified.

**Next decision:** prioritize a separately reviewed proof and comparison contract for the center-distance rule before considering another benchmark. No new candidate is implemented or qualified by this checkpoint. Physical accuracy and novelty remain unestablished.

[Open the interactive Three.js evidence view](viewer/) to play the saved clips, select a drone, and compare the illustrated 3 m sphere with the 4 m axis box. These overlays show software thresholds, not airflow or safety zones. The replay preserves the refused trial.

Evidence: [fixed protocol](PROTOCOL.md), [exact results](results/summary.json), [independent audit](audit/audit.json), [result claims](RESULT-CLAIMS.md), [prior-art ledger](LITERATURE.md), [restart record](RESTART-RESULT.md). All four single-use allocations completed within their original limits. GitHub publication is recorded separately after exact public verification.
