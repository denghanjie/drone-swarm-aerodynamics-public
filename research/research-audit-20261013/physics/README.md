# Physical-model literature audit

Retrospective addendum, 13 October 2026. The exact-equation CPU campaign was already complete before this audit. It remains an implementation-efficiency result for an unvalidated aerodynamic model. This audit did not run benchmarks, change physics, edit frozen records or publish anything.

## Result

The inherited mean-wake kernel has traceable provenance. The receiver response and multi-wake model still need independent validation. See the exact source attributions and limitations in [bibliography.json](bibliography.json), and the source-to-code-to-record mapping in [literature-experiment-ledger.json](literature-experiment-ledger.json).

- The repository explicitly credits [Bauersfeld et al.](https://arxiv.org/html/2403.13321v3). Its geometry mapping is consistent with the inspected Fig. 2. The publication issue year is 2025; the consulted preprint version is dated 2024. These are deliberately distinguished.
- [Jain et al.](https://doi.org/10.1109/ICUAS.2019.8798116) and [Kiran et al.](https://www.roboticsproceedings.org/rss21/p102.html) are verified related comparators. No evidence establishes that they informed this campaign.
- The code freezes source amplitude at isolated-hover weight, uses finite support and pointwise receiver inflows, rotates wake axes, sums incoming axial speeds, and converts inflow to force using an assumed constant induced-power cubic. Exact preservation of those choices is not evidence that they predict real vehicles accurately.
- The code’s 27 g vehicle, operating conditions and geometry require a properly matched reference. The source papers’ normalizations and actuator conditions must be reconciled before transferring data or coefficients.

## What the existing records establish

The ledger names only IDs verified in the saved experiment index. Four linked selected-variant Boids records have zero recorded position differences and identical state streams versus legacy. Their common aerodynamic assumptions prevent these matches from independently testing physics. Candidate source SHA-256: `6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189`.

No fabricated experimental IDs are assigned to suggested future tests. No current candidate publication commit is invented. Input repository and physics-baseline commits are recorded separately.

## Pre-execution normalization correction

The proposed near-merge figure screen was withdrawn before execution. The best-supported projected length interpretation puts its entire test window outside the model domain. [Correction and retained proposal](NORMALIZATION-CORRECTION-2026-10-13.md).

## Next scientific step

Acquire legitimate raw measurement access, reconcile geometry/units/actuation, then freeze an independent validation protocol for isolated wake velocity, receiver force/moment response and interacting wakes. Declare train/held-out configurations, uncertainty-aware acceptance thresholds and a stopping condition before calibration. Do not call any literature adaptation successful until that test is completed.

## Access and publication

[verification-and-access.json](verification-and-access.json) records bounded correction/version checks and access gaps. The cited dataset’s raw observations were not acquired. This subset does not establish novelty or clear all historical citations.

This publication includes the reviewed prose and machine-readable audit files listed in [the editorial mapping](../editorial-mapping.json). Cached third-party full text and renderings are not distributed. The source papers remain available at their original linked locations.
