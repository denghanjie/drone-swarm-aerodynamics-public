# Does using smaller time steps change the result?

We asked: **if we calculate motion twice as often, does our earlier finding change?** In these two fixed examples, the answer was no: both memory-controller paths reached five seconds, while one original-controller path encountered the same airflow-model refusal at trial time 3.620 s. Across matching completed positions, the largest difference was about **0.024 mm**. This is evidence that the observed result is insensitive to this particular halving of the time step, within these saved windows; it is not a guarantee for other cases or real drones.

The paired completion category agreed between the two time steps in **2 of the two fixed arrangements**. The tables below retain each actual outcome; category agreement alone does not mean that the paths or refusal times are identical.

We ran four new 64-drone paths using .0025-second steps and compared them with the saved .005-second paths. Both controllers, the starting arrangements and the five-second horizon stayed fixed. The memory controller remembers past vertical error. The earlier runs were not repeated.

| Fixed seed | Saved .005 s category | New .0025 s category |
| --- | --- | --- |
| 2026102101 | memory-only-completed | memory-only-completed |
| 2026102102 | both-completed | both-completed |

A completed run means the implemented checks allowed it to reach five seconds. A native refusal means the airflow model declined a calculation; it is not an observed collision. Last-completed and refused-trial times remain separate in the raw evidence, audit report and replay.

| Seed and controller | Saved coarser outcome | New finer outcome | Largest center difference over shared endpoints (m) | Shared endpoints / actual last times |
| --- | --- | --- | ---: | --- |
| 2026102101 original | stopped, last completed 3.6150 s; native-refusal | stopped, last completed 3.6175 s; native-refusal | 2.22662254e-05 | 724 through 3.6150 / 3.6150 s |
| 2026102101 memory | completed, last completed 5.0000 s | completed, last completed 5.0000 s | 2.38453554e-05 | 1001 through 5.0000 / 5.0000 s |
| 2026102102 original | completed, last completed 5.0000 s | completed, last completed 5.0000 s | 8.56334057e-06 | 1001 through 5.0000 / 5.0000 s |
| 2026102102 memory | completed, last completed 5.0000 s | completed, last completed 5.0000 s | 1.59516823e-05 | 1001 through 5.0000 / 5.0000 s |

Only matching completed endpoints are compared. No stopped suffix is filled in. If only the initial state is shared, zero difference cannot establish agreement of moving trajectories. The exact maximum's drone, indices and both timestamps are retained in audit/audit.json. Each timestamp is checked against its own rounding expression.

For controller errors, all four streams within a seed use one shared observation window. Each number is the average absolute gap between that stream's requested and actual vertical velocity. The requests evolve differently, so these are not errors against a shared target.

| Seed | Coarser original (m/s) | Coarser memory | Finer original | Finer memory | Shared updates and window |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026102101 | 0.274967 | 0.186790 | 0.274967 | 0.186790 | 362 (0.00–3.61 s) |
| 2026102102 | 0.279668 | 0.180239 | 0.279668 | 0.180239 | 500 (0.00–4.99 s) |

The independent audit checked 29,792 new attempted native stages and 7,447 completed steps, both controller laws, memory continuation and saved integration arithmetic. It checked fine initial words against the four saved coarse initial records. Coarse trajectories use the previously audited, byte-bound export; their raw arithmetic was not re-audited. See [AUDIT-CONTRACT.md](AUDIT-CONTRACT.md) for exclusions.

Smaller steps also check limits more often and change native trial times. This is a sensitivity result for the implemented model, not proof of convergence, real airflow accuracy, safe flight, population reliability or algorithmic novelty. Two arrangements remain exposed fixed examples. No scientific or display allocation was repeated after its outcome.

All four allocations are closed. Preserve the 93 new raw parts (3,075,331,252 bytes), the coarse evidence, failures/read events, reviewed claims and restart record. [Explore the paired Three.js evidence](viewer/) or read [claim boundaries](RESULT-CLAIMS.md), [literature scope](LITERATURE.md) and [restart instructions](RESTART-RESULT.md).

Source commit: `08fc10c6fb3d38dc0e22b7f1aa595e8cb9a50848`. Public result completion requires the final verified receipt.

## Preserved acquisition observations

The producer had an observed synchronous source-file read wait and then completed without intervention inside its original limits; its identity-read event list is empty. Separately, the audit recorded four failed identity-read attempts across two new compressed parts: an errno60 read error, then a zero-byte/hash mismatch on each, followed by a verified third read. No unverified bytes were parsed and no arithmetic/model allocation was repeated. The audit report preserves the exact paths and events. The underlying storage cause is not established. See RUNTIME-OBSERVATION.json and RUNTIME-OBSERVATION-OUTCOME.md.

## Next research question

Return to the main accuracy-versus-computation question: can the existing conservative buffered-neighbor candidate reduce complete airflow-evaluation cost on actual recorded Boids motion while preserving F's loads and admission/refusal decisions? Keep failures in the workload and count list checks/rebuilds in the timing. This requires a new bounded reviewed protocol; no speedup or novel method is established by the present result.
