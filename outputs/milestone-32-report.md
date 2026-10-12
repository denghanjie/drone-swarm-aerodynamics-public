# Milestone 32 — airflow visualization and checkpoint diagnosis

## Goal and method

Make mutual aerodynamic influence inspectable, and distinguish fresh local integration differences from errors inherited before 20 s. This extends original steps 3–5 and 8; it does not close the eight-step research programme.

The first protocol was frozen before execution: restart the historical narrow seed 2002 1,000-drone coarse state at 20 s; integrate through 30 s at 2.5, 1.25 and 0.625 ms with 100 Hz feedback. Replay the coarse run's exact four-motor targets on both finer grids. Keep the same swept contacts and floor checks. Store positions every 0.1 s, full endpoints, and all closed-loop motor targets and controller summaries. Airflow remains off in these numerical diagnostic runs.

A separately frozen post-hoc follow-up integrates the historical fine checkpoint at 2.5 ms. Its comparison to the existing historical fine-step trajectory is explicitly reused evidence. The two initial states differ in all dynamic components, not only position. These are development cases chosen after milestone 31; there are no new acceptance thresholds or confidence claims.

## Results

|Comparison over 20–30 s|Maximum matched-drone position difference|
|---|---:|
|Same starting state, feedback: 2.5 vs 1.25 ms|8.78774451e-07 m|
|Same starting state, feedback: 1.25 vs 0.625 ms|5.35437269e-08 m|
|Identical motor commands: 2.5 vs 1.25 ms|9.84729242e-06 m|
|Identical motor commands: 1.25 vs 0.625 ms|6.02013698e-07 m|
|Same 2.5 ms step, different historical starting states|0.0485103676 m|
|Same fine starting state,2.5 ms vs historical 1.25 ms|8.46451972e-07 m|
|Historical runs, both starting state and step differ|0.048510325 m|

The first four rows use 0.1 s samples; rows involving historical recordings use their common 1 s grid. Same-step different-state comparisons use 0.1 s. All six new continuations reach 30 s without contact. The coarse-state/coarse-step continuation reproduces the historical coarse recording **exactly** at all 11 common saved times, validating restart alignment. Maximum initial position difference is 8.63887763e-06 m; the complete component comparison is retained in [checkpoint comparisons](milestone-32-checkpoint-comparisons.json).

Interpretation: local integration changes from a common state are much smaller than the divergence reproduced by changing the inherited state while keeping the integration step fixed. Feedback-sensitive evolution matters in this selected window. No individual neighbor threshold, yaw rule, constraint projection, or mathematical chaos mechanism has yet been isolated. Smaller RK4 steps alone do not establish long-mission accuracy. The original 1cm full-trajectory criteria remain failed. No numerical tuning or controller change is presented as a solution.

## What the airflow graphics mean

The four displayed recordings reuse corrected milestone 28 seed 1601, 50 drones, wide factory, baseline controller. “Off” completes 50/50 at the 180 s horizon. Linear-force coupling stops at 13.2375 s by obstacle contact; rotor-aware linear coupling stops at 7.770 s and RSS coupling at 8.915 s by vehicle model limits. These are historical outcomes, not new wall-priority trials. Every view includes original local Boids dynamics.

For every exact Float64 saved pose, the builder calls the existing corrected `aero.fields` implementation. This is possible without saved motor states because source amplitude is prescribed isolated-hover thrust. It yields a **reconstructed snapshot field**, not the field held during the original 10 ms coupling updates and not actual rotor loads. No interpolation is used for the numeric field. Course counts come from recorded crossing times. 1,708 static two-drone configurations expose unsupported near-wake geometry instead of inventing a continuation.

Teal envelopes follow the published normalized far-wake half-speed width, with the existing 2.5 m cutoff; bodies are enlarged 2×, envelopes are to scale. Receiver rotor colors show scalar axial inflow, saturated at 4 m/s. Amber arrows show the strongest two individual source contributions above 0.03 m/s per receiver; their lengths are source–receiver distance, not force. In RSS mode they identify component magnitudes, not additive shares. Decorative moving dots indicate downward direction only: there is no advected fluid, vortex computation or wall-resolved flow. The displayed nearby factory walls are context; they do not redirect the modeled wakes. Playback advances exact snapshots every 0.75 wall-clock seconds, unrelated to solver speed.

The static receiver estimate solves the constant ideal induced-power thrust hypothesis already used by milestone 28. At 0.8 m directly below, predicted mean rotor inflow is about 2.24 m/s and lift loss 18.3%. At 0.6 m sideways the existing radial cutoff gives zero. This zero is a truncated-model result, not a claim of zero physical air movement. The lower source's wake is omitted from the explanatory pair view because it does not affect the upper receiver in this downward-only model.

Omissions: calibrated motor/electrical response, source thrust feedback, wake transport, turbulence, moving-source relative flow, near wake, walls and ground. The [Bauersfeld et al. mean far-wake model](https://arxiv.org/abs/2403.13321v3) supplies the normalized profile. Its geometry mapping is corrected; physical measurement agreement is still unestablished. This is not CFD or a new aerodynamic law.

## Verification and reproduction

13 airflow checks pass, including self-exclusion, upstream behavior, cutoff, unsupported near wake, constant-power identity, half-width convention, binary frame lengths and decomposition of every valid reconstructed field into individual pair contributions. 897 numerical/provenance checks pass, including preservation of 870 historical source-tree files. Six new diagnostic runs complete. None of these checks establish real-world safety.

From the project root, verify the final manifest with `python3 outputs/research-reproduce.py`. To rerun the diagnostics and regenerate fields in a copied tree, use `python3 outputs/research-reproduce.py --stage 32 --node /path/to/node` as shown. No external packages are needed. The checkpoint follow-up uses its own source-directory metadata; all protocol sources and inputs are pinned.

Files ending `-positions.f64` contain little-endian Float64 rows `[time, x0,y0,z0, …]`, 3,001 values per row; 101 rows per new run. Closed-run `-commands.f64` files contain 1,000 consecutive 100 Hz updates of 1,000 drones×4 motor targets, held constant for 10 ms. JSON files contain final 17-component states, control diagnostics and stopping outcomes. The independent Python comparisons use nearest-rank P95 and conventional median; the original JS comparison trace used zero-based floor indices. Maxima and all conclusions are identical.

Previous delivery pages and manifest are preserved in `archive-before-visible-airflow`. [Browser QA](milestone-32-qa.md) and [artifact checks](milestone-32-artifact-checks.json) document the delivered view. [Summary](milestone-32-summary.md) · [Original eight-step roadmap](research-roadmap.md).
