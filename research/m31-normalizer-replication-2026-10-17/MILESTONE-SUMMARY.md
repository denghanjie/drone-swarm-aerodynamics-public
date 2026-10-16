# Caching kept the answers but missed the speed target

We tested a simple shortcut: reuse identical calculations within each aerodynamic query. On two new 64-drone Boids flights, it preserved the complete scientific answers. **None of the six sampled states met our predefined speed target.** We will keep the verified baseline and redirect effort toward shortcuts that avoid more substantial interaction work.

The target was at least a 10% improvement in median paired cost, with the candidate faster in at least three of four comparisons, at every sampled state. Timing included the entire fresh worker: startup, source checks, input, calculation, saving the answer and cleanup. A ratio below 1 favours caching; passing required at most 0.90.

| State | Baseline median ms | Cached median ms | Median paired ratio | Cached wins |
|---|---:|---:|---:|---:|
| run-a-t0 | 691.0 | 741.7 | 1.0147 | 2/4 |
| run-a-t5 | 1844.9 | 1774.2 | 0.9700 | 3/4 |
| run-a-t10 | 1858.8 | 1854.7 | 0.9808 | 3/4 |
| run-b-t0 | 802.7 | 697.4 | 0.9605 | 4/4 |
| run-b-t5 | 2071.6 | 1937.2 | 0.9431 | 2/4 |
| run-b-t10 | 2037.7 | 2013.1 | 0.9766 | 3/4 |

These are medians of paired ratios, not ratios of the two displayed medians. [Every timing is retained](analysis/descriptive-summary.json), including slow observations. Repeated measurements share two trajectories and one host, so they do not establish a population effect or identify the cause of timing variation.

**The numerical checks passed.** All six states were reached, independently verified and certified under the existing four normalized 1e-8 bounds. Complete scientific records matched exactly across arms and repetitions. All 48 deliberate corruption checks reached their intended rejection. Direct cache tests and a change-and-return test also passed. The independent checker reconstructed 12 unique inputs; the experiment completed 62 full method calls.

The [new Three.js view](viewer/) shows the two actual recorded flights and all 24 timing pairs. Each flight saved 51 pose frames over 10 seconds. Local separation, alignment and cohesion operate alongside shared route guidance and obstacle avoidance. The sampled drones tilted, changed relative positions in three dimensions and changed interaction graphs. **Airflow was off during flight; aerodynamic loads were calculated afterwards.** Playback speed is unrelated to calculation speed.

The kernel and independent checker closed normally after approximately 84.3 and 44.4 seconds. The checker returned exit 1 because the overall speed rule failed; its numerical integrity, equality and admission checks passed. This is a completed negative performance result, not missing evidence. Detailed lifecycle, resource and dispatch records remain available.

The experiment used an Apple M4 with 24 GiB RAM, pinned Node 24.19.0, AC power and low-power mode off. No other research benchmark or browser test overlapped timing; background desktop activity was not controlled.

This result supports finite numerical correctness for the tested shortcut and rejects its practical speed claim on this suite. It does not establish physical accuracy, general safety, live browser performance, 5,000-drone capability, novelty or publication readiness. The reference remains limited to 180 drones. In the original eight-step roadmap, this advances computation testing and evaluation; physical interaction validation and coupled browser scaling remain open.

[Source checkpoint](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/08ed31c184f88f95217dca689d3727c44c75e8c4) · [Protocol](PROTOCOL.md) · [Independent numerical report](results/check.json) · [Claim ledger](RESULT-CLAIM-LEDGER.md) · [Reproduction](REPRODUCTION.md) · [Restart](RESTART.md). The result manifest and separate publication receipt identify the final public checkpoint.
