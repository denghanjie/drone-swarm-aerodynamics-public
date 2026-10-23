# Fewer distance checks, but too little benefit

The new rule really did reduce calculation work. Across eight measured repetitions it avoided **2,183,680 center-distance calculations**, while every query preserved the required scientific results and refusal decisions. However, the observed median query time fell by only **about 1.95%**, below the **10% improvement required in advance**. We will not advance this exact implementation on this workload as a worthwhile acceleration.

Imagine a shopkeeper keeping a list of shelves that do not need checking. The list saves some visits, but updating and checking the list also takes time, and the shopkeeper still has plenty of other work. Here the complete calculation includes much more than distance checks. The measured result tells us that this particular shortcut did not deliver the practical benefit we required; it does not isolate which overhead explains the difference.

We reused the same 1,920 recorded stages of a 64-drone swarm, in twelve short clips. Both the old method and the new method evaluated every stage during one warmup and eight measured repetitions: **34,560 complete queries** in total. This was a new calculation on saved states, not a new simulated flight. An independently written audit checked every recorded comparison, the work counters, cache bookkeeping and timing calculation.

| What we checked | Observed result |
| --- | --- |
| Scientific results and model refusals | All 34,560 calls matched the fixed comparison contract. Baseline also passed its stricter original comparison on 17,280 calls. |
| Measured center-distance calls | Baseline 61,928,960; candidate 59,745,280. |
| Median candidate/baseline query time | 0.9804733054420454: about 98.05 units of time for every 100 baseline units. |
| Repetitions with lower candidate time | 8 of 8, with the smallest difference very small. This is not a statistical population claim. |
| Preset practical-benefit test | Failed: median needed to be at most 0.90. |
| Motion-rebuild coverage | Failed:96 initial builds,15,264 reuses, zero motion-triggered rebuilds in measured clips. |

The earlier too-close trial remains refused. It appears eighteen times because both methods replay it in all nine repetitions; that is one inherited trial, not eighteen new flight failures. The short clips never exercised rebuilding after leaving a box. We kept that failed coverage requirement rather than changing it after the test.

The timing includes input copying, validation, list checks/builds, forces, refusal decisions and result construction. It excludes evidence encoding, comparison and saving. Those extra activities can still affect later timings through memory and processor state; the baseline also performs an extra strict comparison, while the candidate copies cache witnesses. Thus the small observed difference is evidence for this instrumented run, not a demonstrated 2% improvement in an entire flight simulator. Nor can we compare it directly with the previous run's timing to isolate the new rule's benefit.

**Decision:** retain the negative qualification result and stop refining this exact cache as the current speed solution for these clips. The next useful step is to examine the saved timing breakdown to identify a larger cost before designing another optimization. That analysis needs its own bounded plan; no extra experiment is opened here. This result does not reject neighbor-list methods in other workloads.

All four allocations completed once and closed. The 3D viewer passed checks of every saved position and new actual-work annotation, camera/playback controls, desktop/mobile layout and rejection of altered evidence. Both screenshots were inspected. The viewer shows earlier motion with new measured-query annotations. The conditional runtime proof gap remains, and no physical accuracy, flight safety, novelty or large-swarm claim is established.

[3D replay](viewer/) · [Raw timing summary](results/summary.json) · [Independent audit](audit/audit.json) · [Fixed protocol](PROTOCOL.md) · [Claim ledger](RESULT-CLAIMS.md) · [Sources](LITERATURE.md)
