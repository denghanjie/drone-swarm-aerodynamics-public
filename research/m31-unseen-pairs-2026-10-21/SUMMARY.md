# Two fixed arrangements: matched controller comparison

The memory controller reached five seconds in both fixed arrangements and had lower recorded own-request vertical error in both. The original controller reached five seconds in one arrangement; in the other, the native airflow model refused a near-field trial at 3.620 s, after the last completed endpoint at 3.615 s. This refusal is not an observed collision.

We ran the same 64 simulated drones twice in each of two starting arrangements. The original controller reacts to the current request; the memory controller also remembers past vertical error. All settings stayed fixed, including the airflow coupling. Both versions started with exactly matching saved physical states within each pair.

The primary result is whether each run reached five simulated seconds:

| Fixed seed | Original | Memory | Paired category |
| --- | --- | --- | --- |
| 2026102101 | Stopped at 3.6150 s: native-refusal | Reached 5 s | memory-only-completed |
| 2026102102 | Reached 5 s | Reached 5 s | both-completed |

We also measured the average gap between requested and actual vertical speed. Smaller means a smaller gap against that controller's own changing request. These are different evolving requests, so this is not a comparison against one shared target.

| Fixed seed | Original gap (m/s) | Memory gap (m/s) | Memory minus original | Common updates | Sample times (s) |
| --- | ---: | ---: | ---: | ---: | --- |
| 2026102101 | 0.274967 | 0.186790 | -0.088177 | 362 | 0.00–3.61 |
| 2026102102 | 0.279668 | 0.180239 | -0.099429 | 500 | 0.00–4.99 |

- Seed 2026102101, last common completed endpoint 3.6150 s: average height change original -1.851540 m, memory -0.861564 m; drone 17 height original 1.260234 m, memory 2.555024 m.
- Seed 2026102102, last common completed endpoint 5.0000 s: average height change original -2.196420 m, memory -0.544466 m; drone 17 height original 1.130626 m, memory 2.964127 m.

These are two fixed examples at one time step, .005 s. They do not establish population reliability, long-flight performance, real airflow accuracy or safety. Higher altitude alone does not establish better tracking. Prior-use searches found no proposed seed in the completed inspected scope, but the broader search was incomplete; these are not certified held-out samples.

An independent saved-evidence auditor passed 14,896 attempted native stages and 3,723 completed steps, checked both controller formulas and paired initial words, and reconstructed the recorded integration arithmetic. Its exclusions remain in [AUDIT-CONTRACT.md](AUDIT-CONTRACT.md): it did not independently regenerate Boids steering, the initializer, contact geometry or the underlying airflow solution. This is numerical evidence inside the stated model, not a physical validation.

All four allocations are closed. The 51 raw parts (1,566,172,290 bytes), all outcomes, read events and search failures are retained. View the [paired Three.js replay](viewer/) and [claim boundaries](RESULT-CLAIMS.md). Established prior work is listed with retained verification scope in [LITERATURE.md](LITERATURE.md). No new algorithmic novelty or speed claim is made.

Next decision and restart details are recorded in [RESTART-RESULT.md](RESTART-RESULT.md). Source commit: `4647882e373d54df66f67b9a653ff115727a03d7`. Result publication is complete only when the final public receipt is verified.
