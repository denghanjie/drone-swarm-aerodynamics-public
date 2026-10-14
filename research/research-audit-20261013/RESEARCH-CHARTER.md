# Sustained accuracy–computation research charter

Adopted 2026-10-13. This expands the project workflow without replacing the original eight-step research roadmap.

## Goal and claim boundary

Determine experimentally which computational compromises can make 5,000 locally controlled 3D Boids drones with flight dynamics and mutual aerodynamic interactions efficient in a browser while preserving explicitly selected predictions. The target, a useful accuracy–cost trade-off, a new algorithm and publication suitability are objectives, not established results.

Label statements as hypothesis, observation, supported conclusion within tested scope, or open question. Agent agreement, animation quality, code agreement and collision-free runs are insufficient to establish real-world aerodynamic validity or general flight safety. A more detailed or unconverged numerical model is not ground truth.

## Experimental cycle

1. Audit source, protocols, raw results, failures and limitations rather than inheriting report conclusions. Preserve genuine local 3D rules; disclose shared route guidance and any centralized information.
2. Before optimization, select observables, references, justified tolerances, swarm sizes/densities, device-specific compute/memory/render budgets and acceptance/rejection/stopping rules. Separate numerical, approximation and physical-model errors.
3. Check correctness and convergence of numerical references. Use independent compatible measurements for physical-validation claims, documenting uncertainty, provenance and reuse permissions. If unavailable, retain the physical-validation gap.
4. Verify relevant literature at outset, before novelty or major modeling choices, and when stalled. Maintain the literature–experiment ledger and machine-readable bibliography; source locations must support each attribution. Apply the verified-literature policy in this directory.
5. Consider competing compromises without presuming novelty: interaction truncation, adaptive spatial detail, process-specific update rates, reuse and local/distant hybrids. Explain avoided work, sacrificed information, failure conditions and decisive tests in plain language.
6. Save hypotheses, primary observables, analysis and decisions before confirmatory results. Start with interpretable cases, compare matched baselines, measure errors/cost/memory/failures, run causal ablations and then fresh confirmatory cases. Preserve deviations and negative results.
7. Justify trial/repetition counts or sequential stopping. Account for dependence, multiple comparisons, warmup, background load and timing variation. Do not tune on held-out cases, cherry-pick seeds, omit failures or silently relax thresholds.
8. Keep a claim–evidence ledger: exact scope, source/configuration, experiments/raw data, analysis/uncertainty, counterevidence, status and the next falsification. A failed test is not proof of impossibility.

## Execution and preservation

Proceed autonomously through successive bounded cycles with independent implementation, validation and adversarial scrutiny when supported. Use at most three configured research agents. Serialize heavy timing work. Do not purchase services or provision paid resources without approval, and do not imply execution continues through suspended environments.

Continue until a defensible publication candidate satisfies the gate, a genuine blocker prevents meaningful progress, resources require a checkpoint, or the project is stopped. A plan, short animation or elapsed time alone is not completion. When blocked, preserve an exact restart record and finish independent work.

At important checkpoints save source versions, plans, seeds, configurations, raw successes/failures, analysis, both ledgers, dependencies, commands, limitations, a plain-language milestone and restart instructions. Privacy-review every public artifact for secrets, personal or machine-identifying information, private paths and sharing restrictions. Keep originals private; describe sanitization and hash the actual public bytes. Use development branches and verified remote commit URLs. Preserve history; never claim an incomplete push succeeded. Use versioned release assets when available and appropriate for large evidence.

Every substantial milestone includes a visible Three.js demonstration linked to actual experiment records. Clearly label live computation, recorded replay and illustration; measure simulation separately from rendering. Relevant end-to-end performance includes steering, physics, aerodynamics, transfers and synchronization, with exclusions stated. Low-end feasibility requires measurements on specified low-end hardware.

## Publication gate

A candidate needs a precise limited claim, closest-prior-work comparison, reproducible meaningful evidence, fair baselines and ablations, fresh tests, uncertainty and failure boundaries, independent validation attempts, an explicit falsification attempt, separation of computational and physically validated findings, and verified citations. A rigorous negative finding can qualify only if it establishes a useful non-obvious limitation.

When satisfied, prepare a scoped paper draft, plain-language contribution, strongest evidence and counterexamples, reproducibility package, interactive demonstration and remaining validation needs. Review and publish supporting project checkpoints; external paper submission requires separate approval. Before writing, re-audit citations and describe the literature-search scope. Absence from a search does not establish novelty.

## Original organizing framework

Retain: (1) define the experiment; (2) one credible drone; (3) pair interaction; (4) overlapping wakes; (5) real local flock; (6) accelerate validated calculations; (7) scale the actual flock; (8) evaluate the contribution. Provisional computation studies do not mark physical-validation steps complete. See [the original research roadmap](../../outputs/research-roadmap.md) for historical status and limitations.
