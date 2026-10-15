# Wall-activity audit: listed walls were inactive

Public audit addendum, 2026-10-15. The separately reviewed replay completed once with exact controller-output parity across all 50 saved reference states. **All 2,412 wall projection tests were inactive.** The earlier zero final-repair count did not hide early-pass wall corrections on these sampled J32 states.

Pair avoidance did act: **697 branches fired and 677 produced a nonzero floating-point velocity change.** A fired operation can round back to the same velocity. The largest single pair correction was 0.2539216624752528 m/s.

|Pass|Wall tests / fires / changes|Pair tests|Pair fires|Pair changes|Largest pair change, m/s|
|---|---:|---:|---:|---:|---:|
|0|402 / 0 / 0|7460|321|321|0.2539216624752528|
|1|402 / 0 / 0|7460|142|138|0.020818920119833537|
|2|402 / 0 / 0|7460|60|56|0.0016875232032973126|
|3|402 / 0 / 0|7460|58|54|0.00013678589212484736|
|4|402 / 0 / 0|7460|58|54|1.1087480307110381e-05|
|5|402 / 0 / 0|7460|58|54|8.987200189587097e-07|

## What was checked
Exactly 50 pre-control frames, ticks 0..25088 at spacing 512; terminal frame 50 was excluded. Each state was passed once to the original controller and once to an instrumented copy. All original returned values, including commands, controls, branch signatures and diagnostics, matched as tagged binary64 data, including signed zero. Inputs remained unchanged. There were 100 swarm-controller calls, comprising 1,600 vehicle steering/control blocks; the observer covered the 800 instrumented blocks.

The six projection passes produced 47,172 row tests: 2,412 wall plus 44,760 pair. All 4,800 post-pass speed-limit checks showed no change. The separate initial steering speed limit was outside this observer. Zero initializer, wake, load or dynamics calls occurred. This was saved-state controller replay; no flight was regenerated.

[RESULT.json](RESULT.json) preserves every aggregate and all 50 equal-output hashes. [WITNESSES.json](WITNESSES.json) decodes all 13 retained first/maximum witnesses, with the actual 17-entry wall normals and full binary64 values. The [exact narrow source patch](instrumentation.json) adds observations after existing arithmetic. The [independent review](INDEPENDENT-RESULT-REVIEW.md) checked saved geometry and witnesses without rerunning controllers. Full returned outputs and dense pass tapes were not retained: complete parity and coverage rely on the reviewed instrumentation, rather than an independent rerun.

## Limits and unchanged qualification
The event-stress outcome remains **EVENT_EXPOSURE_INSUFFICIENT**. This later diagnostic supplies no missing wall response or C1 support crossing. It only resolves early-pass activity on the saved J32 reference path; it does not test every approximate-arm state. Later operations may undo a correction, so pair activity does not prove a net counterfactual trajectory effect. The route field can encode the course independently of wall projection. Correction sums are descriptive, not accumulated displacement.

No physical wall aerodynamics, collision-safety, speedup, novelty or general event-robustness claim follows. The original unused failure-writer schema limitation remains unresolved. See the [published event-stress report](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/f1632213839104990eed9ec9c29600d2360d52cf/research/campaign-predictor-event-stress/results/REPORT.md) and [retention erratum](https://github.com/denghanjie/drone-swarm-aerodynamics-public/blob/f1632213839104990eed9ec9c29600d2360d52cf/research/campaign-predictor-event-stress/results/RETENTION-ERRATUM.md).

One actual replay completed, exit 0, after a wrapper-availability error before any controller execution. The corrected wrapper was separately authorized. There was no experiment retry or model change. Runtime figures are omitted from this audit edition; it is not a performance benchmark.
