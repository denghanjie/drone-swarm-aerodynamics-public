# Inspect the retained evidence

This guide concerns inspection of the saved coordinate-origin diagnostic. **Do not rerun the closed science, launch an old review, remove locks, fill skipped cells or regenerate data.** Fresh replication requires separate authorization and an independently frozen protocol with its own scope, inputs, budgets and stopping rules.

The [terminal result](results/result.json) records no candidate. No broader confirmation was earned or run. The [supervisor budget](results/budget.json) records a terminal inactive science attempt and process cleanup. Its wall time is execution bookkeeping, not a benchmark.

**Independent review completed but failed its aggregate integrity gate.** It recorded two final-control bookkeeping mismatches. Static source inspection identifies a checker lifecycle-assumption error; the saved API record matches the frozen source. The immutable failed report and exit code remain unchanged, with no retry or waiver. Read the [disposition](INDEPENDENT-SAVED-REVIEW.md), [exact report](results/independent-review.json) and [external closure](results/saved-review/runtime.json). The observations below retain their recorded status; no complete independent qualification is claimed.

## Start with identity and disposition

1. Open the exact [source publication commit](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/ccafbd9b9fd3a3cdd7ffacb5fb360ee5f3dc1abc/research/m31-coordinate-origin-2026-10-16). Its commit is `ccafbd9b9fd3a3cdd7ffacb5fb360ee5f3dc1abc`.
2. Inspect [freeze.json](freeze.json), whose recorded SHA-256 is `ccfeac8a7b6386f647d00899933757004146f4e01f8b135eaf73389190f9efaa`, and the [prospective protocol](PROTOCOL.md). Preserve their pre-exposure wording and bytes. Hash/length comparison is read-only identity checking, not a scientific rerun or proof of physical validity.
3. Read the original result's `cells`, `references`, `qualifiedArms`, `candidate`, `decision` and `files`. The raw index retains names, byte lengths and SHA-256 values. The driver retained 185 raw files totaling 129,695,212 bytes. Inspect the [closure](results/budget.json), [claims](claims.md), [review contract](REVIEW-CONTRACT.md) and eventual saved review alongside it.

## Follow the saved numerical evidence

| Question | Original evidence |
|---|---|
| What was generated and how are the origins related? | [Generator audit](raw/generator-audit.json), original [origin-0 states](raw/o0-states.f64), [origin-1 states](raw/o1-states.f64), and indexed coordinate/reconstruction certificates |
| Did literal controls pass? | [Frozen literals](controls/controls.json), [A assessment](raw/controls-A-assessment.json), [B assessment](raw/controls-B-assessment.json), [C assessment](raw/controls-C-assessment.json) |
| Why were translated A/B skipped? | [Q0 assessment](raw/o1-Q0-assessment.json), [A disposition](raw/o1-A-disposition.json), [B disposition](raw/o1-B-disposition.json) |
| Why did exact coordinate recovery not qualify C? | [Q1 assessment](raw/o1-Q1-assessment.json), [C terms assessment](raw/o1-C-terms-assessment.json), [C disposition](raw/o1-C-disposition.json) |
| What is known about A/B returned vectors? | [Origin-0 saved comparison](raw/o0-B-A-vectors-assessment.json); translated A/B have no GPU buffers |
| Where are valid serial outcomes? | Origin-0 [A](raw/o0-A-serial-assessment.json), [B](raw/o0-B-serial-assessment.json), [C](raw/o0-C-serial-assessment.json); inspect original indexed reduction words alongside certificates |

Use the [saved-evidence viewer](viewer/) after its own integrity checks unlock. It reads retained poses, terms, vectors and report certificates; it must remain locked while its independent-review binding is incomplete. The numeric origin/arm labels and availability states matter. A skipped stage is not zero, and an unavailable combined gate is not a pass. Display recentering moves only drawing/camera coordinates. The [historical M31 Boids replay](../../outputs/milestone-31-lab.html) is separate, with airflow off.

For binary inspection, [schema.json](schema.json), the [kernel contract](KERNEL-CONTRACT.md) and [host contract](HOST-CONTRACT.md) specify little-endian layouts. GPU records contain 26 words; reference records contain eight metadata words and 18 binary64 fields. Each vector component requires its reached-validity bit. Preserve status, identity and masks; never interpret an unreached zero placeholder as a measured zero. Exact dyadic coefficients and saved booleans—not rounded viewer decimals—are authoritative for acceptance.

The saved source, binaries and review receipts support examination of this one outcome. They do not establish portability, physical validity, production speed, or a universally reproducible compiler operation order. Do not claim that a remote manifest check independently downloaded every binary unless the retained publication record actually says so.
