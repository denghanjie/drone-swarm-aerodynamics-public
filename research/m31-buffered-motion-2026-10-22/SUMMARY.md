# Remembering neighbors did not deliver the required speed benefit

22 October 2026 · Milestone 31 continuation · computational evidence only

Imagine giving each drone an address book of the other drones it might need to check. We hoped that keeping this book between calculations would save time. In the recorded clips, every book still contained all 63 other drones. Keeping the books saved rebuilding them, but did not remove any drone pairs from consideration.

We compared the unchanged shortcut with the original calculation on 1,920 recorded stages from twelve short clips of 64-drone Boids motion. Both controllers and both previously exposed starting arrangements were included. We used one warmup and eight measured repeats, totaling 34,560 calls. These are repeated calculations of saved trial states, not 34,560 independent flight experiments.

**The calculations matched, but the shortcut failed our preset keep test.** The median shortcut/original time ratio was 0.986884: roughly 1.3% less measured time. It was faster in five of eight repeats and slower in three. Before execution, we required a median ratio at most 0.90 and at least seven wins. Those requirements were not met. This small difference is not evidence of a reliable speed improvement.

The measured shortcut calls contained 96 initial list builds, 15,264 reuses, zero movement-triggered rebuilds and zero fallbacks. Every candidate query retained all 4,032 directed pairs (64 × 63). The test therefore exercised reuse with fully dense lists. It did not exercise pair omission or movement-triggered rebuilding. Our separate coverage requirement also failed. We did not extend clips or add repetitions after seeing this outcome.

An independent audit checked all 34,560 scientific-output comparisons, the original source records, cache transitions, status handling and timing arithmetic. The equality claim uses the fixed normalization in the protocol, which excludes method/timing/work-count metadata and separately checks source bindings. One recorded near-field refusal at 3.62 seconds was replayed eighteen times across both methods; these are repeats of one inherited refusal, not eighteen new flight failures. A refused trial is not a completed flight position or collision evidence.

The result tells us not to promote this unchanged shortcut for this workload. It does not show that every neighbor-list method fails, nor establish drone physics, flight safety, thousands-of-drones performance, or a novel method. Neighbor-list reuse is established prior art; see the verified antecedents and access limits in [LITERATURE.md](LITERATURE.md).

The next useful question is why the conservative lists contain everyone, and whether a mathematically justified tighter bound could exclude pairs while preserving the calculation. Start with the saved witnesses and source rules, not another timing run. Any new numerical test needs its own fixed, independently reviewed and publicly verified source protocol. If no useful conservative exclusion is available, retire this candidate rather than repeat the same benchmark.

[Open the Three.js recorded-state replay](viewer/) · [Independent audit](audit/audit.json) · [Independent result review](review/RESULT-REVIEW.md) · [Exact claims](RESULT-CLAIMS.md) · [Restart instructions](RESTART-RESULT.md)

All five scientific/display allocations and the separate lossless publication transport are closed. Historical milestones are preserved. The overall research remains unfinished.
