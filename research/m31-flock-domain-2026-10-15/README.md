# M31 checkpoint: the retained flock fits the model's input limits

We checked whether the airflow model can accept the recorded large-flock positions before attempting to accelerate its calculations. **All 12 selected snapshots pass the implemented tilt, near-wake exception and unit-quaternion screens.** This is evidence about the implementation's domain, not evidence that its airflow predicts a real swarm accurately.

The [Three.js view](viewer/index.html) shows the exact saved 3D flocks and each selected receiver's retained and skipped source relationships. Click a drone, use its ID, or choose “Most retained entries.” Cyan lines show sources whose geometry lies inside the retained formula support. Gold lines show the explicit near-field skip policy. Center-to-center lines are identifiers, not computed wake shapes or forces. The 3× glyph scale is for visibility only.

## What was tested

- The unchanged M28 geometry rules on all vehicles in the retained primary M31 wide1000, narrow1000 and wide5000 snapshots at 0, 20, 30 and 60 seconds: **28,000 pose records**.
- Original grid enumeration plus double-cross rotation versus independent all-source enumeration plus matrix rotation. Exact indexed classifications, counts, ordered near-event identities and tilt decisions must agree. Numeric geometry tolerance was fixed at 1e-12.
- No force, wake-amplitude, controller or integration evaluation. No new flight, assumed historical motor state, active-mask reconstruction, post-exposure tolerance change or repeated campaign.

This is a prospective analysis of already exposed historical development evidence. The poses are from airflow-off local 3D Boids flights with broad map guidance and 34 solid obstacles. Their earlier individual-path refinement failures remain failed. It is not a fresh held-out flight study.

## Observations

| Flock | Saved time s | Maximum tilt ° | Eligible ordered source/receiver pairs | Retained rotor entries | Near-field policy skips | Domain screen |
|---|---:|---:|---:|---:|---:|---|
| wide1000 | 0 | 0.000000 | 148,126 | 9,017 | 61,728 | PASS |
| wide1000 | 20 | 7.537975 | 275,358 | 14,166 | 66,732 | PASS |
| wide1000 | 30 | 7.003258 | 249,226 | 12,509 | 61,289 | PASS |
| wide1000 | 60 | 8.612321 | 213,142 | 10,839 | 53,821 | PASS |
| narrow1000 | 0 | 0.000000 | 147,228 | 8,933 | 61,636 | PASS |
| narrow1000 | 20 | 7.458491 | 292,876 | 18,498 | 65,528 | PASS |
| narrow1000 | 30 | 7.133664 | 263,550 | 17,679 | 59,240 | PASS |
| narrow1000 | 60 | 7.295729 | 151,156 | 8,666 | 40,734 | PASS |
| wide5000 | 0 | 0.000000 | 925,686 | 48,124 | 394,464 | PASS |
| wide5000 | 20 | 7.220505 | 2,313,748 | 115,943 | 518,697 | PASS |
| wide5000 | 30 | 8.273289 | 2,282,534 | 116,670 | 512,361 | PASS |
| wide5000 | 60 | 7.789237 | 2,115,930 | 110,491 | 477,620 | PASS |

The counts are directed source–receiver–rotor tuples; they are not independent samples, unique physical pairs, collisions or force magnitudes. Across the selected snapshots:

- **107,972,000** independent nonself center-pair checks and **75,028,480** combined eligible rotor classifications across both implementations completed.
- **Zero** tilt-limit violations, near-wake exceptions or unit-quaternion assumption violations. Largest tilt was **8.612321°**, below the implemented 20° limit. Largest quaternion norm defect was **4.440892098500626e-16**, below 1e-10.
- **491,535** retained positive-projection source–rotor entries and **2,373,850** near-field policy skips were recorded. A skip is an explicit model policy; its physical error was not measured.
- Every indexed code vector agreed. The maximum axis/world-rotor coordinate discrepancy was **3.552713678800501e-15**. All reached code3/4 coordinates were compared in the invocation; only code3 full coordinates are retained, while every code identity is preserved losslessly.
- The smallest inspected predicate gap was **4.315612445182637e-8 m**, at wide5000/30 s, receiver2882/source4942/rotor0, downstream cutoff. This checks reached predicates only; it is not a global robustness margin or a physical uncertainty.

The single supervised invocation took **12.109875667 s**, with **40,076,924 bytes** of raw evidence, inside the 300 s / 64 MiB caps. Child maximum RSS was 287,817,728 bytes on macOS (about274.5MiB); no memory acceptance limit was adopted. This is execution accounting, not a fair speed benchmark or a browser performance claim.

The original independent saved-data verifier passed **555,158 checks** on its first invocation, including all **432,000,000 inflated code bytes** against both saved hashes. It took2.488579667 supervised seconds within a separately bounded60s allowance; total accounted executable time is14.598455334s. It checks saved bytes, counts, identities and aggregates without rerunning geometry. Independent vectors/coordinates were compared at runtime but are not separately saved; code4 geometry and geometric nearest-boundary status cannot be reconstructed by this saved-data review. These evidence limits are explicit in its [report](results/independent-review.json). Original checker/stdout/stderr/review/runtime are preserved without correction or rerun.

## Supported decision and limitations

The feared model-domain rejection did **not** occur at these twelve saved configurations. A separate, frozen static numerical field comparison can now be designed for these exact poses. That comparison must prescribe missing motor inputs explicitly and must not pretend to recreate the historical airflow-coupled flight.

This result does not establish continuous-flight domain coverage, physical airflow validity, receiver-force validity, realistic multiwake aggregation, obstacle/ground aerodynamics, closed-loop stability, trajectory accuracy, novelty or real-time5,000-drone computation. Every saved vehicle was included; this does not establish agreement with an operational active/arrived subset. Twelve correlated selected snapshots supply a finite census, not a success probability.

The [original eight-step roadmap](../../outputs/research-roadmap.md) remains unchanged. This checkpoint links Steps3–4 (interaction model) to Step5 (local flock) and prepares the reference requirements for Steps6–7 (computation and scale). Step8's publication gate remains unmet. Later main/DOT work is preserved separately.

## Evidence and reproducibility

Source freeze: [`e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3`](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3), published and independently checked before execution. [Frozen protocol](PROTOCOL.md), [exact input/source hashes](freeze.json), [final static review](DRIVER-REVIEW.md), [preflight decisions](PREFLIGHT-RESOLUTIONS.md), [raw result](raw/result.json), [budget](results/budget.json), [independent saved-data review](results/independent-review.json), [claim ledger](claims.md), [reproduction](REPRODUCE.md), [restart](POSTRUN-RESTART.md).

All per-receiver compressed code vectors, both hashes, counts, tilt records and all near-invalid event records are in the committed raw directory. Zero near-invalid events is a measured result; near-field policy skips remain fully recoverable from the indexed vectors.

## Research informing this checkpoint

The field geometry is adapted from Bauersfeld et al., *Robotics meets Fluid Dynamics: A Characterization of the Induced Airflow below a Quadrotor as a Turbulent Jet*, [arXiv2403.13321v3](https://arxiv.org/html/2403.13321v3), especially VII/Eqs10–11 and the near-hover/far-field scope. Our 20° gate, finite cutoffs, near-field skip rule, rotor-point evaluation and extrapolation to27g vehicles are implementation assumptions, not independently validated facts from that paper. The exact checked source and limits are documented in the [verified ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md).

The uniform-grid enumeration is established methodology; Green's *Particle Simulation using CUDA* (2010), printedpp4–7, is discussed in that ledger. This CPU geometry audit makes no CUDA/WebGPU speed claim. Local 3D separation/alignment/cohesion follow established Reynolds Boids concepts; source access was limited to the author's abstract/citation and explanatory pages. The [machine-readable bibliography](../m31-restart-2026-10-15/literature/sources.bib) and source-access limitations remain authoritative. No new external publication or novelty claim is introduced here.
