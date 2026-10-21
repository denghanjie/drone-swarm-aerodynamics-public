# Source reuse and static checks

21 October 2026. No scientific module or browser launched during these checks.

The original and continuation motion wrappers are byte-identical. The producer imports the existing control/safety wrapper, projected adapter and qualified storage code unchanged. The four initial states are generated once each by the same initializer; independent initial-word matching remains a required postrun audit gate.

| Unchanged source | SHA-256 |
| --- | --- |
| research/m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs | b14b81107a5c5f08db1b14e369e61baccd3bef18ef3c6d2717fd150165ab4332 |
| research/m31-boids-continuation-2026-10-20/source/motion.cjs | c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373 |
| research/m31-boids-continuation-2026-10-20/source/journal.cjs | 689c3faae7a21fe0abf446b6260d907e1f92039688194c87ef7cb17bc3de0485 |

Static Python parsing and Node syntax checks passed for the prepared sources. No fixture flight, controller execution or hidden warmup was used. The source review and manifest check are separate gates.

Browser plugin is absent. Display verification uses the existing Playwright package and installed Chrome, without installing or updating them. The exact Node binary identity matches runtime.json. OS, loaded system libraries and the complete browser/package dependency graph are not hermetically frozen; no performance or platform-independent reproducibility claim is made.

UI test flow: open the paired recorded replay, select each configuration and every saved step, verify both buffers and missing suffixes, exercise playback/rotation/reset, capture desktop and mobile, and reject altered evidence. All screenshots and reports are retained in the repository as requested.
