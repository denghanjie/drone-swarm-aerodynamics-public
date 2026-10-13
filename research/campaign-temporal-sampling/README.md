# Airflow-update temporal-sampling campaign

Status at this checkpoint: protocol adopted and independently reviewed; implementation review is in progress. No numerical case has run. The initial plan is saved before compatibility or fresh-case outputs. Source, configuration and harness hashes must be frozen before execution.

## Plain-language question

How long can a drone reuse its last airflow calculation before its predicted forces become noticeably different? Reusing a weather reading saves work, but an old reading can miss a change. Here we first check whether our numerical reference is fine enough, then measure that stale-reading error on exactly the same recorded drone states. Separate coupled runs check how errors feed back into movement.

These states will come from genuine local 3D Boids simulation, not scripted formations. Holding the trajectory fixed during the diagnostic deliberately isolates force error; it is not a second independently evolving flock. This is a numerical test of an unvalidated mean-airflow model, not a real-flight validation.

## Frozen design

- [Protocol and priority amendment](PLAN.md).
- [Machine-readable configuration](config.json).
- [Fresh-seed check](seed-freshness.json).
- Two new N=16, one-second workloads; at most fourteen coupled runs plus one known compatibility run.
- Separate physics-step and airflow-reference screens; a failed reference stops further coupled rows.
- Same-path force, torque, accumulated error and sampling checks. A failed reference may support only explicitly conditional diagnostics.
- Hard bounds: 300 seconds for the serial numerical window, 45 seconds per job, 150,000,000 logical uncompressed retained bytes, including a failure reserve.

All numerical thresholds are prospective engineering screens, not physical tolerances or mathematical convergence guarantees. No scaling, parameter fitting or paper-submission authorization follows from this plan.

## Evidence and literature basis

The preceding [exact-code campaign](../campaign-exact-efficiency/REPORT.md) verified software agreement but left airflow-cadence and long-horizon reference quality unresolved. Its [actual-record Three.js replay](../campaign-exact-efficiency/demo/index.html) is historical context, not a result of this new protocol. New records and their viewer will be added only after execution.

The [verified literature and claim audit](../research-audit-20261013/README.md) distinguishes the inherited mean-wake kernel from unsupported extensions. Bauersfeld et al.'s [equations 1 and 3–9](https://arxiv.org/html/2403.13321v3) inform the model being tested; they do not validate its numerical update cadence. Kiran et al.'s [static/dynamic experiments](https://arxiv.org/html/2507.09463v1) motivate caution about memoryless interaction assumptions, but their conditions and measurements are not used as a numerical reference here. The proposed cross-paper figure comparison was withdrawn because its length mapping did not satisfy the declared model domain. This cycle does not resolve that physical-validation gap.

## Restart instructions

1. Read PLAN.md, config.json and the prior audit; verify source graph and plan hashes.
2. Finish independent implementation and adversarial harness review before any numerical case.
3. Save a source-freeze checkpoint and publish it when permitted; never silently use later code under an earlier source identity.
4. Run the bounded serial supervisor exactly once, retaining partial and failed outcomes. Do not restart the resource clock or replace failing seeds.
5. Independently reproduce summaries, update both research ledgers, attach an actual-record viewer, and privacy-review the next checkpoint. Interpret every result within its tested scope.
