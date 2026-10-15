# Overnight restart record — diagnosis CLOSED

**Do not launch D1–D6 or L1–L4. Do not repeat the consumed microchecks or increase this tranche’s cap.**

The fixed-state order probe and four microchecks completed. All four 0.05 s traces agree exactly in final physical/scheduler state, held controls, event flags and command streams. Their source commit is `e6680fe`; the order-probe source commit is `9e8fe14`.

The frozen full-matrix estimate is 1500.1949766500018 s, exceeding the 1196.248672 s remaining from the 1200 s cap after 3.751328 s actual executable time. `results/planning-gate.json` records the declined launch; `results/budget.json` is terminal. No D/L study trajectory ran. The historical divergence cause remains unresolved. Four verification traces consumed the entire 0.2 s microcheck allowance.

Raw microcheck evidence is under `raw/` (56,706,272 bytes), packaged separately for immutable release with checksums. Fixed-state outputs are in `results/order-probe.json`. The updated Three.js viewer displays exact saved poses and the measured velocity requests; it is a fixed-state visualization, not simulated flight or a runtime benchmark.

Next permissible action: complete publication/verification of this diagnostic checkpoint, then a separately frozen and bounded aerodynamic implementation-verification campaign. Do not enter another automatic controller-diagnosis loop. Keep numerical and physical validity unresolved. Preserve newer main/DOT work and its partial-stop record, inspect it before proposing optimization. Original eight-step framework remains the organizing roadmap.

If a smaller temporal study is proposed later: a single 0.5 s same-state D1/D5 feedback-versus-command-replay pair with explicit initial states, recording cadence and budget could test limited replay parity. This is an unexecuted future proposal, not approval to reuse this closed budget or evidence of the long-flight cause.

Overnight follow-ups stop launching work at 07:00 Asia/Shanghai on 2026-10-16. Do not overlap solver jobs. Continue from the most recent research checkpoint; a closed campaign cannot be restarted by a heartbeat.
