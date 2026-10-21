# Historical check: prospective paired configuration diagnostic

21 October 2026. This source-only note uses saved narrative results and receipts. No simulation, numerical code, old raw-journal analysis or new external research acquisition was performed. No additional broad seed search was run for this review.

## Fixed question and evidence status

The exact seed values **2026102101 and 2026102102 are fixed prospectively without simulation screening**. Each uses N64, h = 0.005 s only, a five-second horizon split into 1 + 4 s, and two newly executed arms: unchanged original controller and unchanged vertical-memory controller, both with full current aerodynamic coupling. Four paths are prescribed; no new finer-resolution arm is included.

“Newly prescribed” means fixed for this campaign. This note does **not** assert that these values were never used anywhere. The parent separately records the status and limits of the historical seed-text search. The directory name does not establish global seed novelty, held-out status or independent random sampling. No candidate outcome is known from this source-only review.

## Closest completed history

- [First-seed memory diagnostic](../m31-vertical-memory-2026-10-21/SUMMARY.md): exposed seed 2026102001, h = 0.005/0.0025 s. Both memory paths completed five seconds with coupling retained; the reused original-controller paths had stopped at 4.6200/4.6175 s. This was selected after observing failure, not blind confirmation. [Result receipt](../publication-receipts/m31-vertical-memory-result-2026-10-21.json): commit `dbb8596098a7223d57fa7499df8ad76a171acf2f`, manifest SHA-256 `c6a00e16c356a72152b6f77c2ef510b51cb9ec78f31545de55ad8535b50a59a9`.
- [Second-seed transfer](../m31-vertical-transfer-2026-10-21/SUMMARY.md): exposed seed 2026102002, same two resolutions. Both unchanged-memory paths and both reused original-controller baselines completed five seconds. Mean descent differed, approximately 0.51 versus 2.29 m, but completion was preserved rather than improved. The [claim ledger](../m31-vertical-transfer-2026-10-21/RESULT-CLAIMS.md) expressly leaves performance on previously unexecuted seeds unestablished. Candidate-only controller statistics did not support matched fleet tracking comparison because the old export lacked fleet desired velocities.
- The exact [transfer result receipt](../publication-receipts/m31-vertical-transfer-result-2026-10-21.json) records commit `341cfa5e9bec84c0615825b82665385469d84a2b`, [result-manifest](../m31-vertical-transfer-2026-10-21/result-manifest.json) SHA-256 `530b5b76624dfea7e21127832e552af9deeab7358816ed164cfa00a0130b872a`, 198 pins and both local/public-manifest and local/committed equality flags true, verified at `2026-10-21T02:41:04.491386+00:00`. This is retained receipt provenance, not a new remote check; its scope excludes full remote-journal redownload. The saved audit's file-read anomaly remains preserved and was not a numerical rerun.
- Earlier [historical review](../m31-vertical-memory-2026-10-21/HISTORICAL-CHECK.md) covers fixed-height PD tests, horizontal position-hold/gain changes, [N16 force ablation](../m31-force-ablation-2026-10-16/MILESTONE-SUMMARY.md), short N64 coupled/off qualification and the [nominal-load comparison](../m31-nominal-comparison-2026-10-21/SUMMARY.md). Controller comparison, compensation and integral action are established ideas.

The distinct contribution sought here is a small prospectively fixed paired diagnostic with **both arms newly recorded** and their own controller requests available. It is not another test of the two exposed prior seeds, another torque mask, or a new controller design. No exact-duplicate or repository-wide absence conclusion is made pending the separately recorded search status.

## Unchanged intervention and interpretation

Retain the prior [memory protocol](../m31-vertical-memory-2026-10-21/PROTOCOL.md), [configuration](../m31-vertical-memory-2026-10-21/config.json) and controller implementation: gain 2.5, 0.01 s updates using the previous error, integral-acceleration clamp [-5,+5] m/s², specified initial zero memory and exact target-expression grouping. This is integral clamping, not saturation-aware anti-windup. No gain, bound, controller, model, timestep or horizon adjustment follows observed outcomes.

Each arm evolves from the matched original physical state and reads its own evolving flock. At t = 1, preserve each path's physical state and, for memory, integral/previous-error/update-count state. Do not reset or transfer memory between arms or seeds. Seventeen physical words alone do not specify a memory-controller restart.

Primary evidence is each seed's **paired completion/stopping categories**. Preserve all native refusals, contact/vehicle-limit stops and missing suffixes. Secondary position/height comparisons use the last common completed endpoints. Vertical MAE comparisons use only common saved controller indices, with sample counts and extent explicit, and each arm's error against **its own requested vertical velocity**. Diverging paths change neighbors and requests: this is a paired own-request descriptor, not tracking a common target or guaranteeing better tracking.

The single timestep supplies no new refinement evidence. Earlier other-seed coarse/fine agreement cannot certify these paths. Four paths are two paired deterministic configurations, not four independent trials. No population success rate, physical validity, general safety/stability, optimality, novel integral method, scalability or overall research-completion claim follows.
