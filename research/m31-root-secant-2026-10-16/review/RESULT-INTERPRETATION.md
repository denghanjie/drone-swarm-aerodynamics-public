# M31 saved-root secant: independent result interpretation challenge

Date: 2026-10-16. Repository-relative package: `research/m31-root-secant-2026-10-16`.

This challenge reads only the saved `results/summary.json`, `results/independent-review.json`, `results/candidate-run.json`, and `results/review-run.json`. It interprets their existing aggregates and closure fields; it does not rescore event data, import a scientific program, integrate a trajectory, run controls, retrieve a source, or modify the frozen package. Both scientific allocations are closed. No rerun, repair, tuning, or additional experiment is proposed as part of this review.

## Disposition

**The fixed causal secant is rejected on this declared endpoint diagnostic, and the experiment is intact.** All 200 positive targets were scored. The independent audit completed, passed 1,098,131 checks, and retained no failures. Its strict independently reconstructed qualification agrees with the candidate: all three absolute error gates fail; all three maximum-error comparisons against hold pass; four finite predicted roots violate the declared domain. Audit success validates the recorded rejection under this protocol, not the approximation's scientific qualification.

Both external closures report return code zero, `supervisorSuccess: true`, `closed: true`, absent child groups, unchanged protected inputs and candidate outputs, positive RSS sample counts, and no recorded monitor errors, exit races, or signals. Candidate/reviewer elapsed times and sampled peaks are operational closure evidence only. They are not a speedup measurement or a comparison of alternative flight algorithms.

## What the retained maxima establish

Every threshold below is 0.001. Values are dimensionless under the row's stated normalization, and all are existing saved maxima.

| Metric | Normalization | Primary candidate, 200 targets | Secondary candidate, 199 targets | Hold maximum |
| --- | --- | ---: | ---: | ---: |
| Rotor error | `mg/4` | 0.018768458300 | 0.016180553420 | 0.034641310307 |
| World-force error | `mg` | 0.009938113764 | 0.009938113764 | 0.022282031285 |
| Body-moment error | `mgR`, `R = sqrt(2) * 0.028 m` | 0.004127670070 | 0.004127670070 | 0.010175726666 |

The candidate lowers each maximum relative to hold but misses every absolute screen. Improvement over a comparator that already fails the screens is evidence of relative diagnostic improvement; it does not meet the declared accuracy requirement. The independent strict maxima confirm the same gate outcomes. Tiny last-bit differences in an independently reconstructed hold value do not affect any outcome.

The primary per-event-maximum comparison counts are rotor 199 better / 1 equal / 0 worse, force 196 better / 1 equal / 3 worse, and moment 197 better / 1 equal / 2 worse. These are comparisons of each event's maximum, not a statement that every drone/rotor improves, every event passes a threshold, or a particular fraction of the flight is accurate. Force and moment are not uniformly improved event by event.

## Why a startup-only explanation is insufficient

The largest primary rotor error occurs at the mandatory cold-start target: event 1, 0.01 s, zero-based drone 12 / rotor 0. Its value, 0.018768458300, is material and cannot be discarded from primary qualification.

However, the saved secondary population already removes that one target and still misses all three absolute screens:

- Rotor maximum 0.016180553420 occurs at event 45, 0.45 s, drone 15 / rotor 1.
- Force maximum 0.009938113764 occurs at event 45, 0.45 s, drone 15.
- Moment maximum 0.004127670070 occurs at event 43, 0.43 s, drone 15.

The force and moment maxima are unchanged by removing startup. The secondary also retains the same four out-of-domain roots. It has no separate qualification flag and cannot rescue primary failure.

Therefore merely omitting the cold-start target, or supplying startup history while leaving the subsequent prescribed secant and saved-fresh-root history unchanged, does not address the observed later misses. At later targets this protocol uses the preceding saved fresh roots regardless of the previous prediction; an improved first prediction does not feed into those later predictor inputs. This is a narrow conclusion about a startup-only change under the unchanged saved-event rule. A different predictor, history policy, cadence, or predictor-driven feedback trajectory was not tested and cannot be declared successful or unsuccessful from this result.

## Domain violation is an additional rejection reason

All four invalid predicted roots are finite, above one, and occur at zero-based drone 3 / rotor 0:

| Event | Time, s | Saved predicted root |
| ---: | ---: | ---: |
| 31 | 0.31 | 1.0000050076817075 |
| 32 | 0.32 | 1.0000280867081577 |
| 33 | 0.33 | 1.000025529595089 |
| 34 | 0.34 | 1.0000047468478048 |

The declared domain was finite `0 < x <= 1`; it had no overshoot allowance. Small finite overshoots therefore remain invalid rather than being relabeled acceptable roundoff or silently clipped. Their arithmetic was retained as diagnostic evidence, explaining why all 200 events can be scored while the candidate still fails the zero-invalid-root requirement. No nonfinite or unscored event is reported.

The later absolute error maxima at events 43 and 45 are outside these four flagged events. The result thus has both an absolute-accuracy failure and a domain failure; it is not explained only by startup or by the four overshoots.

## Claim boundaries and publication wording

A supported summary is: “On the exposed 200-target saved-event diagnostic, the fixed causal secant of coupled rotor roots reduced all three maximum load errors relative to hold, but failed all three 0.001 absolute screens and produced four finite roots above one. The independent audit passed, and both one-shot allocations closed. Removing startup still leaves all three absolute screens unmet.”

The population is the existing finest 10 ms reuse path with 16 drones and 201 saved refresh events over 2 s. The 200 positive endpoints are development evidence already exposed to the design process. The candidate evaluates same-state loads on saved states and saved fresh-root history. It does not generate a new secant-driven flight trajectory. Any visualization must retain the original poses and label the overlay as diagnostic errors on that existing trajectory.

This result does not establish that forecasting, secants in general, or coupled-root prediction are impossible. It also does not establish intermediate-time accuracy, feedback stability, adaptive-trigger usefulness, fewer actual solves, wall-time speedup, physical validity, validated flight tolerances, held-out generalization, or novelty. The current secant is an established extrapolation form applied to the newer coupled-root quantity. Fresh geometry/root correctness is inherited from the pinned prior audit at saved events; physical validation and between-event admission are not added by this audit.

## Planning-only next question

A defensible planning question is whether a separately specified causal method could satisfy both the root domain and all absolute load-error screens after startup, under a prospectively chosen evaluation population and an explicit history rule. Such a question would need its own frozen hypothesis, method, startup policy, evidence-selection rule, budgets, and independent audit before any execution. This result selects no replacement, changes no cadence or threshold, authorizes no clipping or retuning, and opens no new allocation.

## Reviewed evidence identities

Both closure records and the independent audit identify source commit `5a555210fa6012a9df334ecfc4ae0c9a666b0e82` and source-manifest SHA-256 `06d8a81dfba014349b48c649d30bf4ed06479632a7a34f4bcd45026b7f49eaf3`. The parent workflow supplied the completed pre-execution independent remote-verification status; this saved-report challenge performs no new remote verification.

| Saved report | SHA-256 |
| --- | --- |
| `results/summary.json` | `ad89a9ace8c0229c17b9bcb9bce421b0f5ac3cca996f9c65328eaece6610c773` |
| `results/independent-review.json` | `1dbc291d4e6474dbc18db57215d8cf3e6a5fd0329183463fd5df9348843a34a9` |
| `results/candidate-run.json` | `139b59fbc34bd7b6baebaf67443be4a8717891d3d8dcca4e64d2e31ead49d37d` |
| `results/review-run.json` | `dd1d6383e4bdfeee4a78052b623126bd0897f7a1638abf50d464d08668900d6b` |
