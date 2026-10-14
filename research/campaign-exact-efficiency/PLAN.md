# Exact-equation airflow efficiency: frozen bounded plan

Saved before implementation or measured trials, 2026-10-13. Repository checkpoint: c024dfc27b9e6b7cd5b39132164d1339cb95b12f; underlying physics baseline: c591ce2b195fa01b895d4ba881a44a4b92fdd703. Existing source is unchanged. No archive download, paid compute, GPU, hosting, or 5,000-drone claim. Follow the original eight-step roadmap: (1) freeze experiment; (2) preserve mechanics; (3) check pair equations; (4) check overlap accumulation; (5) run genuine local 3D Boids; (6) measure CPU efficiency; (7) scale conditionally; (8) report limitations and failures.

## Question and frozen implementations

Can exact implementation changes improve CPU airflow time without dropping any positive interaction in the existing finite-support law? This means equivalence to unvalidated fixed-hover mean wakes and receiver response, not physical truth, turbulence simulation, or safe flight.

Five separately reported variants are fixed before evaluations:
- legacy: unmodified milestone-28 fields(states, 'sum-rotor').
- previous-zero: unmodified previous campaign fields(states, {epsilon:0}); retains positive omission-bound computation overhead.
- lean: scalar four-rotor geometry and kernel, no omission budget or pair bounds, same sorted source order and original grid.
- support: lean plus conservative pair envelope that can skip only exact-zero support. Domain checks remain independent and precede culling.
- reuse: support with reusable geometry/output scratch arrays and per-call geometry refresh. Original sorted grid remains; output lifetime is explicitly borrowed until the next call. No stale-state caching.

All three new variants keep 2.5 m axial support and fades, 3-half-width radial support and fades, 3 m center search, all four receiver rotors, fixed-hover source strength, sum-rotor receiver response, nominal yaw convention, control law and update cadence. Source summation remains ascending for each rotor. No positive-value threshold, support change, adaptive refresh, approximate reciprocal, GPU, or reduced sampling is allowed. Strict finite 17-element state/unit-quaternion checks are shared by new variants and previous-zero. Legacy lacks some input validation; unsupported malformed-input cases are recorded separately rather than misrepresented as identical legacy validation behavior.

## Correctness gates and independent review

Before timing, independently review plan and candidate code. Tiny deterministic checks only before review. Match legacy on valid cases at max inflow absolute error <=1e-12 m/s, force vector error <=1e-12 N and roll/pitch moment-vector error <=1e-13 N m, with no nonfinite outputs. Report bitwise equality as a stricter diagnostic without making it mandatory. Match tilt and near-wake outcomes and preserve rejection of unsupported malformed input in new variants. Cover exact support/fade/near-wake/tilt/search boundaries, asymmetric thrust, overlapping sources, permutations, changing swarm sizes and repeated workspace use. Domain failures must remain visible with saved inputs and exception details. Preserve first failure; fixes require append-only amendment and source-version retention before new held-out runs.

## Frozen fixtures and selection

Development seeds 4301 and 4302; untouched held-out seeds 4391 and 4392. Reuse the published deterministic cloud generator with families sparse, dense, tilted and times 0, 0.37, 0.91 seconds. These are prescribed-state benchmarks, never called flock trajectories. Tiny gate is deterministic pairs plus N=16. Correctness matrix N=16,50,100,200; N=500 only after the scale gate. New variant selection uses development cases only: report all five; select the fastest new variant that passes correctness. Freeze its source hash and identity before held-out timing and closed-loop evaluation. No retuning based on held-out outcomes.

## Timing protocol, scope and gates

Measurements require an exclusive serial timing window. No concurrent CPU-heavy work. One Node process, same host/version, serial balanced rotated variant order; one process warm-up and per-case warm-up. Retain individual paired repetitions, not only aggregates. Initial bounded scout uses development N=50 and100, each family, seven repetitions with enough repeated calls for >=10 ms target/batch but at most 20 calls/batch; report actual batch durations. Then held-out evaluation, nine paired repetitions at N=50,100,200. N=200 proceeds only if development N=100 shows >=10% median field saving versus previous-zero on at least two families. N=500 requires the same held-out gate at N=200 and projected cost within caps. Report ratios versus legacy and previous-zero separately, including regressions; bootstrap 95% paired intervals and medians are descriptive for this machine only.

Measure field time inclusive of validation, geometry preparation and search; geometry preparation separately only as a diagnostic. Measure receiver load time and field+receiver time in a separate serial pass. For reuse, setup allocation is recorded and amortized evaluation distinguished from one-shot allocation. No render FPS, GPU, physical fidelity or end-to-end speed claim from field timing. Record CPU model, OS, Node, git source SHA256, seeds, states checksums, warmup counts, sample count, call counts, raw times, counters, exceptions and active stage.

A provisional useful same-equation result requires correctness, >=10% median field savings and paired bootstrap 95% upper ratio below1 versus previous-zero on at least two held-out N>=100 families; legacy comparison is reported independently. This is not an accuracy-cost approximation frontier. Claim only observed count/family ranges. If speed gate fails, retain negative result and do not scale.

## Genuine Boids and linked replay

After correctness and selected-variant hash freeze, run unmodified milestone-31 local separation/alignment/cohesion, shared broad route and wall-priority steering with existing mechanics. Baseline and selected airflow share seeds, initial states, dt2.5ms, controller10ms and airflow10ms. Stage1: both held-out seeds, N16,1second, legacy/previous-zero/selected. Gate: both complete without domain/contact/nonfinite stop and max common-frame position difference <=1e-10m. Stage2 conditional N50,3seconds for both seeds, same variants. N200/500 only prescribed-state timing here. One N16 seed physics step1.25ms and airflow refresh5ms are separate diagnostics with 1cm comparison screen, never folded into equivalence. Save full initial/final states plus compact replay positions/quaternions and held rotor inflows every50ms; rolling SHA256 covers every integration state. Record stopped members and untouched failure states. Do not store redundant 200MB state copies.

Each milestone links an offline standalone Three.js replay to actual saved Boids records and metadata. Repository demo uses local Three.js, retains the full MIT notice and declares replay-only rendering. No invented trajectories. Check current browser availability once; a verified socket or access denial is recorded without retries or bypasses. Static/offline record integrity checks still run.

## Resource budget and stopping

Before review: source inspection and tiny checks only. Initial timing lease request <=5minutes. Total serial timing wall time <30minutes, each external job timeout<=60seconds, total generated data<1GB, no paid compute. Keep inventory and time ledger. Stop promotion on correctness failure, hidden domain discrepancy, nonfinite output, absent speed gate, or cap risk; preserve failure and report. Bounded closed-loop windows do not establish mission completion, numerical convergence or physical validity. All new work remains local until independent privacy review; authorized coherent GitHub checkpoints require privacy review.
