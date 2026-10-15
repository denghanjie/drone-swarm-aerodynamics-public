# Source and prior-work links

The machine-readable bibliography and primary-source verification remain in [sources.bib](../m31-restart-2026-10-15/literature/sources.bib) and the [annotated ledger](../m31-restart-2026-10-15/literature/annotated-ledger.md). No additional publication is cited without verification. No external code, raw measurement data, or paper figures were imported.

| Source | Material use | Scope here |
|---|---|---|
| Bauersfeld et al., arXiv:2403.13321v3, Eqs. 3–9 / VI-C; separately VII/Eqs. 10–11 | Existing normalized far-field mean wake and induced-power context. | Retain original M28 equations/parameters. Receiver constant-induced-power thrust reduction, cutoffs, projection, scale extrapolation and fixed-hover source remain assumptions; paper is not physical validation of this implementation. |
| Kiran, Ayanian & Breuer, RSS2025, DOI 10.15607/RSS.2025.XXI.102, III-A/B/C | Offset configurations, distinct force/moment observables and actuator matching. | Motivates reporting both thrust and torque; no calibration from unresolved reported-percentage wording. |
| Gielis et al., 2024 proceedings, DOI 10.1007/978-3-031-63596-0_35, §§2–4 | Overlap requires measured aggregation checks. | Main paths have one upstream source. Three-source fixture checks same-model arithmetic only, not physical aggregation. |
| Green, Particle Simulation using CUDA, revision1.3, 2010, pp.4–7 | Exact neighbor enumeration should preserve supported contributions. | Independent brute-force comparison of existing Grid implementation, not claimed new acceleration. |

All of the above relevant sections were verified in the earlier literature checkpoint. Their implementation links are the frozen M28 sources and this campaign's `source/independent.cjs`, `source/experiment.cjs`. Results will be added after one prospective run.

## Newer research already inspected

Remote main SHA `1336f5c416875a9651f92b58b2ed06649f25b04e` was verified via GitHub API. These are internal research records, not peer-reviewed sources or accepted methods:

- `research/campaign-temporal-sampling/README.md`, `implementation/configs/adopted-protocol.json`, and `implementation/REPORT.md`: read through the GitHub contents API at that SHA. Both absolute airflow-reference screens failed; conditional same-path diagnostics already show decreasing stale-load error for shorter holds, including left-limit queries. No cadence qualified. Thus a decrease in this pilot would not be a novel result. Their conditional loads use an unqualified integrated driver; our analytic paths isolate arithmetic/cadence behavior without that driver, but introduce prescribed-motion limitations.
- `research/campaign-joint-stage-reference/MILESTONE.md`: J screens passed but 7/16 new coupled rows completed, one stopped, eight skipped; cross-check incomplete. Reference remained unqualified.
- `research/campaign-audit-c1-r8/postrun/MILESTONE.md`: 218/229 correctness cases completed, one partial, ten unstarted; independent gate not run, benchmark permission false. Do not treat this as full correctness acceptance or a speed baseline.

After reading the previous event-aware diagnostics and before this pilot was frozen or executed, the protocol was strengthened to include old-hold left limits at every refresh event. Uniform-sample RMS remains separate from these augmented sampled maxima. Neither is a proven continuous-time bound. This adopts an existing internal safeguard, not a new method. A later estimator challenge needs separately frozen unused conditions. No novelty review is complete.
