# Most measured savings came from the zero-screening package on these two inputs

The single preregistered ablation completed all26input checks and202queries. Its numerical/control qualification passed. **The incremental positive-omission speed criterion failed on both fresh inputs.** That is a completed negative performance result; nothing was rerun or retuned.

[Open the Three.js evidence viewer](http://127.0.0.1:8876/research/m31-omission-ablation-2026-10-16/viewer/) or serve this repository locally and open `viewer/`. Switch between keeping and omitting the selected contributions on identical saved3Dposes. This is an evidence view, not a live flight or browser simulation benchmark.

## The research question in plain language

The previous method became faster while doing two things: skipping contributions known to be zero, and approximating the answer by omitting some small contributions. We introduced a control that makes the same decisions but still calculates the small selected contributions. This separates their incremental benefit from the broader package of zero screening, bounds and bookkeeping.

B is the original implementation. M retains all sources using the candidate's geometry/traversal. Z screens exact zeros and computes the same shadow decisions as C, but retains every positive-bound selection. C actually omits those selections. Z includes a disclosed extra reporting cost; this comparison concerns these complete implementations.

## What was measured

Two prospectively seeded static lattices:1,000 and5,000vehicles, plus24previously exposed regression fixtures. These are synthetic static states, not integrated Boids flights. All five implementations agree on the4expected domain rejections;22valid inputs pass their fixed numerical gates. Eight balanced timing blocks per fresh case follow one warmup. Node24.19.0, AppleM4, Darwin25.5.0arm64; steering, integration, rendering and transfers excluded.

| Input | Median B | Median M | Median Z | Median C | Median paired C/Z | C faster blocks |
|---|---:|---:|---:|---:|---:|---:|
|1,000|147.193ms|106.316ms|85.189ms|84.883ms|1.003815|3/8|
|5,000|1,730.988ms|1,322.118ms|1,087.359ms|1,080.092ms|0.993453|5/8|

The median paired ratio is NOT the ratio of the marginal medians. Frozen H1 required paired median<=0.95 AND at least7/8Cwins on each case. Neither passed. Timing ranges and all individual blocks remain in `results/descriptive-summary.json`, `raw/timings.ndjson` and `raw/performance.json`. Technical repeats do not quantify generalization over swarms; no significance or population claim.

Using sums of the SAME eight blocks, the zero-screen package supplied90.268% and92.424% of net M-to-C savings; both pass frozen H2>=50%. In seconds,1,000-drone net savings0.179721252=zero-package0.162230834+positive-omission0.017490418;5,000-drone net1.897484709=1.753727624+0.143757085. These positive aggregate savings coexist with H1 failure. The decomposition includes bookkeeping and resulting receiver-law work; it is not a pure source-term hardware cost measurement.

C's largest body-thrust error was0.135754mN against1.32435mN allowed; largest roll/pitch errors2.809916/3.746700µN·m against10.488317µN·m each. Z and M were bitwise identical on both fresh output matrices and agreed with independent I within fixed precision gates. The targets are chosen numerical tolerances, not flight-safety tolerances.

On1,000vehicles,4,931positive-bound receiver–source pairs were selected:2,416had a positive realized term,2,515had four actual zero terms. On5,000,26,463selected pairs:12,987positive-realized and13,476all-zero. These counts are directed receiver–source pairs, not distinct drone counts. A positive bound is not proof that nonzero wake was omitted. Z evaluates all these selections. Its actual positive omissions are0.

## Supported conclusion and next question

Within these two static inputs and this implementation, positive-bound omission did not provide the predefined useful incremental speed improvement, despite satisfying numerical load budgets. Most aggregate savings belonged to the exact-zero-screen package. This supports investigating cheaper exact-zero geometry screening next. It does NOT establish that positive approximation is generally unhelpful, that a lean zero-only implementation is fast, or that5,000interacting drones can run in real time. A5,000-drone query still takes about1.08s.

Physical wake/source/receiver assumptions remain unvalidated. No new flight occurred; prior long-flight1cmfailures remain unchanged. No novelty, low-end hardware, browser-real-time or publishable-breakthrough claim. Generic bounded pruning has verified prior art: [parent literature audit](../m31-source-omission-2026-10-16/prior-work.md).

## Evidence and checkpoint identity

Source freeze committed and independently verified BEFORE execution: `b6aafb006bbc406deb95f7defcebde6801eaa7f5`; freeze SHA256 `ccd1695ca48fefd85225c830fd1a93fbbd6bfbde4e1fcaffd1e0532a9c799ec0`,34direct pins. The sole scientific invocation took59.989628333s externally;34,017,127runtime assertions;254raw files,22,074,354bytes. Budget terminal, no rerun permitted. The sole independent saved-only review passed1,594,583checks with0failures in1.7938165s externally. Combined science+review61.783444833s; separate caps respected. [Review and limits](INDEPENDENT-SAVED-REVIEW.md).

Read [protocol](PROTOCOL.md), [claim ledger](claims.md), [raw result](raw/result.json), [performance](raw/performance.json), [source review](FINAL-PREFLIGHT.md), [restart](POSTRUN-RESTART.md) and [reproduction](REPRODUCE.md). The source protocol and original scientific outputs remain immutable.

The separate [physical-data audit](physical-data-followup.md) and [compatibility challenge](physical-compatibility-review.md) locate partial experimental targets but do not validate M28. One terminology clarification: the cubic keeps **ideal actuator-disk power including thrust times axial flow** constant; it does not impose measured constant shaft/electrical power. The40ms motor-state lag applies nominal thrust commands, not a measured inflow response. A fixed-RPM dataset would test a separately declared model transfer. No data fitting or physical score was produced.
