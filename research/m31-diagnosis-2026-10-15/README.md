# M31 checkpoint: isolate the order effect, preserve the limit

We held two historical flocks still and changed one calculation at a time. The large immediate change comes from the order of the pair-avoidance constraints. Reversing the social-rule summation alone changed the requested velocities only at floating-point rounding scale in these states. **This does not explain the later flight divergence.**

The four short restart checks passed exactly. The preset timing estimate for the longer diagnostic was 1,500.195 s, exceeding the remaining 1,196.249 s allowance. We therefore **did not launch** any of its ten study trajectories. This is a planning-gate closure, not a failed flight or proof that the study is impossible.

- [Measured order result](ORDER-RESULT.md), including every drone and both states.
- [Microcheck outcome](results/microchecks.json) and [recorded launch decision](results/planning-gate.json).
- [Interactive Three.js view](viewer/index.html): exact stored poses and measured requested-velocity arrows. A fixed-state visualization, not live simulation.
- [Claim ledger](claims.md), [reproduction](REPRODUCE.md), [public-payload review](publication-audit.md), and [restart state](RESTART.md).
- [Raw evidence release](https://github.com/denghanjie/drone-swarm-aerodynamics-public/releases/tag/m31-diagnosis-2026-10-15-v1), checked against [raw-manifest.json](raw-manifest.json).

The original eight-step research framework remains in effect: this checkpoint verifies the existing numerical implementation before interpreting aerodynamic compromises. All original M31 1 cm trajectory failures are retained. The next campaign returns to the aerodynamic model and its computational cost after independently checking coupling and reference calculations. Novelty, physical validation and 5,000-drone browser feasibility remain unresolved.

Protocols were published before results: order isolation at `9e8fe14`, microchecks at `e6680fe`. The Git commit containing this result package pins delivery files. Newer main/DOT work remains separate and preserved.
