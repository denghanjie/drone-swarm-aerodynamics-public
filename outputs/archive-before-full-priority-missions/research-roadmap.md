# Research roadmap — the original eight steps

**Research question:** How much aerodynamic detail is needed to predict a drone flock moving through restricted space, and can the calculation run interactively in a browser?

The original eight steps still apply. The factory benchmark supplies a bounded set of experiments for Steps 5–8. Completing that benchmark does not complete physical validation or establish scientific novelty.

|Original step|Purpose|Evidence and remaining work|
|---|---|---|
|1. Define the experiment|Fix vehicle, task, measurements and references.|Frozen protocols and source inventory exist. Independent reference measurements matched to the vehicle remain needed.|
|2. Build one credible drone|Check forces, hover, attitude and motor response.|Rigid-body mechanics and numerical checks exist. Measured-flight agreement remains unestablished.|
|3. Model two-drone interaction|Predict how one wake affects another.|The published mean-wake geometry mapping has been corrected. Receiver-force response remains unvalidated. Historical erroneous examples carry notices.|
|4. Model overlapping wakes|Compare aggregation and force/moment assumptions.|Corrected matched comparisons exist. An airflow-refresh sensitivity failure and omitted flow effects prevent a convergence or physical-accuracy claim. Independent multi-wake data are needed.|
|5. Test a real local flock|Run local Boids through complex geometry.|The 34-solid factory uses genuine local 3D rules and a shared broad route. 50/200 primary missions complete; 1,000/5,000 contact failures repeat at finer steps. Milestone 30 corrects the early wall failure in short candidate windows, including two fresh 1,000-drone seeds. Reliable general navigation is unresolved.|
|6. Accelerate validated calculations|Compare CPU and WebGPU implementations.|Earlier mechanics checks do not validate the present coupled pipeline. Current computation is offline Node CPU; Three.js renders replays. GPU work on the current pipeline remains open.|
|7. Scale the actual flock|Test 50→200→1,000→5,000 with documented spacing.|Full mission attempts and exact replay records reach 5,000. Larger counts expand the starting cloud at nominal 0.75 m spacing; this is not fixed-volume density scaling. Isolated workload costs and early exits are reported separately.|
|8. Evaluate the contribution|Report accuracy, cost, limitations and novelty.|The benchmark provides reproducible software evidence and counterexamples. It does not establish a new algorithm or an accuracy-versus-cost frontier without physical references and matched external baselines.|

## Current records

- [30 — wall-priority avoidance](milestone-30-report.md) · [3D comparison](milestone-30-lab.html): both fresh 1,000-drone candidate flocks reach 20 seconds without contact while their baselines contact the wall; the 5,000-drone development case also reaches 20 seconds. The 50-drone full-mission regression and two prescribed step refinements pass. This is an early-failure improvement; full large-flock passage, delayed observations and airflow remain untested with the candidate.

- [26 — full missions](milestone-26-report.md) · [3D failures and successful passages](milestone-26-lab.html).
- [27 — preserved implementation-error record](milestone-27-report.md): 20 completed primary runs; five uncompleted refinements. No corrected-model claim.
- [28 — corrected airflow study](milestone-28-report.md) · [3D comparison](milestone-28-lab.html): 25 cases, four passing physics-step comparisons, one failed airflow-cadence comparison.
- [29 — actual computation cost](milestone-29-report.md) · [3D workload](milestone-29-lab.html): 48 prescribed serial jobs. See the report for completion status, early exits and measured costs.
- [25 — separate replay rendering and startup costs](milestone-25-report.md).
- [24 — factory and social-rule ablations](milestone-24-report.md): ablated variants also complete, so passage alone does not establish a Boids advantage.
- [Completion audit](research-goal-completion-audit.md) · [stage history](research-stage-log.md) · [current 3D view](research-results.html).

## Next scientific gates

1. Acquire independent wake/receiver-force measurements with matching geometry and motor operating conditions. The candidate dataset is still behind human verification; its raw observations have not been acquired.
2. Validate the receiver response and aggregate wake model. Resolve sensitivity to airflow update cadence separately from rigid-body integration accuracy. Add uncertainty and held-out physical configurations.
3. Compare stronger avoidance and disturbance-compensation methods on the retained failure cases, then on untouched seeds. Keep shared route guidance, local observations and individual motion explicit. Avoid tuning on evaluation cases and calling them fresh evidence.
4. Only then assess a matched accuracy-versus-cost contribution and accelerate the appropriate model. Render frame rate is not a substitute for simulation throughput.

The earlier observer experiments remain preserved: prediction helps some delayed-observation cases and hurts others. It is not a universally validated replacement. [Block 22–23](research-block-22-23-summary.md).
