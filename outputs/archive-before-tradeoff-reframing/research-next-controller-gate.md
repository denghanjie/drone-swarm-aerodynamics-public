# Next scientific gate after milestone 31

The frozen wall-priority controller completes all four prescribed primary missions, including two 5,000-drone cases, without contact through 180 seconds. The three matched fresh-seed baselines hit the first partition. This is useful evidence of a controller improvement under ideal observations and no airflow.

All three prescribed trajectory comparisons nevertheless fail the frozen 1 cm criterion. Maximum same-drone, same-time differences are 5.17 m and 32.77 m across the two full 1,000-drone missions, and 7.98 m across the first 60 seconds of the fresh 5,000-drone case. Full-mission numerical accuracy at 5,000 drones remains untested. The short-window agreement in milestone 30 does not resolve this long-horizon sensitivity.

Before promoting the model as reliable navigation research:

Milestone 32 narrows the first gate: in a post-hoc 20–30 s narrow-course restart, common-state step refinements differ by less than a micrometre, while differing historical starting states at the same step reproduce 4.85 cm of divergence. The coarse restart exactly reproduces the original saved coarse poses. This is evidence of inherited-state sensitivity in one interval, not a diagnosis of a specific switch or proof of chaos. A visible airflow explanation now exists, but uses historical baseline-controller trajectories and reconstructed pose-snapshot fields. [Evidence](milestone-32-report.md).

1. **Isolate which feedback decisions amplify inherited differences.** Use the retained error profiles and states to select a bounded follow-up. Separate integration error, discrete neighbor/constraint changes and controller sensitivity through controlled tests. Do not infer mathematical chaos or physical truth from two disagreeing simulations. Freeze any additional step sizes, control-cadence changes and comparison windows before running them.
2. **Choose the scientific prediction being evaluated.** Individual trajectories, passage times, connectivity and contact events answer different questions. Retain the failed individual-path criterion. Any new group-level tolerance needs an independent justification and a new evaluation protocol; it must not be introduced merely to make the current results pass.
3. **Keep wall and pair safety separate.** Successful missions still contain pair-request violations and repair iteration-limit events. Investigate those residuals, tracking lag and perturbations before claiming guarantees. Reused seeds are development cases in subsequent studies; reserve new seeds for evaluation. Match geometry changes on the same seeds if estimating a doorway-width effect.
4. **Test realistic observations and disturbances under a frozen protocol.** Delay, noise and wind are absent here. Adding them does not replace validation of the underlying model. The current airflow implementation remains an assumption-sensitive model, not calibrated aerodynamics.
5. **Acquire and match physical measurements.** Follow the [physical validation contract](research-physical-validation-gate-2026-10-12.md), including vehicle geometry and receiver response. Further navigation tuning must not indefinitely substitute for measurement validation.
6. **Measure computation independently.** This milestone ran overlapping CPU jobs and did not perform an isolated cost benchmark. Three.js renders recorded trajectories. GPU acceleration and real-time physics performance on the current pipeline remain open.

The standard wall-projection technique is not claimed as a new algorithm. The current contribution is reproducible diagnosis and controlled simulation evidence. A stronger accuracy-versus-cost contribution still needs physical references and matched external baselines.

[Milestone summary](milestone-31-summary.md) · [Detailed evidence](milestone-31-report.md) · [Original eight-step roadmap](research-roadmap.md).
