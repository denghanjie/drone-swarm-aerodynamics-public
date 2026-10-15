# Independent saved-evidence review
2026-10-15 UTC. **Verified outcome: EVENT_EXPOSURE_INSUFFICIENT.** Seven arms completed and all numerical targets passed, but the required event exposure did not occur. Review used saved numbers and geometry arithmetic only, with no model calls.

## Integrity and coverage
Final freeze `030c25e0ae78452b0c9d10e43c6eb105e7400054506e56e3b03ee473e828e535` remains unchanged; all 23 entries and 15 original source bodies match. Release/receipts bind that freeze. Status COMPLETE, decision EVENT_EXPOSURE_INSUFFICIENT, eligibleForSeparateReview=false; seven completed, none skipped. Eleven of 12 gates pass; only event-exposure fails. There are no failure artifacts.

Reference 51 x 16 x 17 tensor: 110,976 B, finite states, quaternion norm defect<= 3.33e-16, nonnegative motors and matching endpoint hashes. Its initial block equals saved seed 840163 with +4.5 only on x; all arms share it.

All seven comparison files and seven paired-witness binaries match their recorded hashes. Independently recomputed 35 saved maximum-value witnesses, 28 field/load witnesses, 7 command witnesses and 22 of 35 terminal metric values recoverable from retained pairs. Maximum arithmetic difference 1.11e-16. Eleven J32 witness rows on the controller grid are bit-identical to the reference tensor. Remaining terminal values, dense maximality and full-step counts rely on the frozen comparator/observer; full approximation/stage tapes were not retained.

Compatibility's saved public five-state prefix hash matches, and its recorded worst scalar difference recomputes to1.1102230246251565e-16<1e-12. This is finite-fixture compatibility, not universal bitwise equivalence.

## Numerical result
Maximum errors against J32, with P8/ZOH8 ratios:

| Metric | ZOH8 | Predictor8 | Ratio |
|---|---:|---:|---:|
| Position,m | 5.08431726e-4 | 4.98600204e-6 | .00980663043 |
| Velocity,m/s | 2.75891757e-3 | 2.19149567e-5 | .00794331695 |
| Attitude,rad | 1.87305831e-3 | 1.83628215e-5 | .00980365714 |
| Angular rate,rad/s | 2.12369026e-2 | 5.02724760e-4 | .02367222605 |

Predictor errors are 42.24–125.89 times smaller for these four declared metrics. All predictor outer caps and fourfold targets pass. ZOH misses velocity, attitude and angular-rate caps; position passes. This translated developmental case does not retroactively qualify earlier stops.

Recomputed joint refinement, method-h, attribution and target inequalities from saved comparison values. Largest uncertainty/signal ratio is 0.00020978925, or 0.02098%, below the 10% requirement. The uncertainty quantities are resolution proxies, not rigorous error bounds. All comparison branch mismatches are zero; controls can still differ numerically.

## Exposure: intended stress was absent
Every arm records 302 listed-wall vehicle-ticks and 402 constraint rows, but zero repair iterations, significant before-residuals, strict wall responses or eligible radial/axial cutoff transitions. J32,H8,P8 each independently fail both required exposure tests. Each arm records 20 neighbor changes, no tilt/motor/speed clipping and no predictor clamps. Clamp robustness is untested.

Recomputed all 14 nearest-farStart/nearest-annulus tuples from their paired normalized states; largest discrepancy 2.22e-16. IDs, sample locations and nearest-farStart monitor records agree. H8 approaches the axial farStart surface to 1.4134e-8 m, but its simultaneous radial distance is .745526 m, well outside outerAtFar = .151521 m. The minimum sampled distance to the closed jump annulus is about .457769 m across arms. Thus the tiny axial margin alone was not dangerous joint proximity.

Positive downstream maxima are below 1.776400 m: neither the 2 m axial fade onset nor 2.5 m cutoff is exercised. Nearest sampled radial-cutoff absolute margin is at least .0247222 m. The zero-event criterion concerns outer support boundaries; it does not exclude changes within the radial taper. Sampled obstacle clearance remains>= 1.1102306 m and pair-body clearance>= .4837052 m. These are sampled margins.

On the retained 51-frame J32 controller grid alone, independently checked 48,960 ordered pair geometries: zero near-wake violations and zero eligible radial/axial transition brackets. This corroborates but cannot establish full-stage counts. Initial wall geometry/final residual recompute correctly. Unlogged pre-repair velocities and earlier projections prevent concluding zero obstacle influence.

## Counts and resources
Reconciled every arm and aggregate: 11,000 steps,704,000 successful vehicle derivatives, 44,000 stage callbacks, 7,200 production fields, 357 diagnostic fields, 350 attempted/returned/validated controller calls and 1 baseline comparison. Compatibility adds 8 steps, 512 derivatives, 1 field, 1 controller and 12 scalar checks. Matched H/P schedules hold at both h values. Production kernel returns total 403,200; diagnostic kernel returns 19,992. Baseline/compatibility internal kernel counts are not retained.

Observer totals reconcile: 55,007 samples, 52,806,720 ordered pair visits, 13,201,680 center distances, 11,007 endpoint samples, 10,560,000 endpoint pair comparisons and 5,600 controller rows. Counts are not timing.

Single external launch exited 0 after 15.128752955 s; supervisor reports no timeout, reason, truncation or stderr. Child CPU 16.539259 s and supervisor CPU .12486747 s are below their limits. Raw results total 211,934 B < 300,000 B. No retry/extension occurred.

## Post-run retention defect, preserved
Saved wall normals have 17 entries: three spatial entries followed by 14 zeros. Public boxDistance maps the full 17-component state. Steering/repair uses the spatial components, so this does not alter the scientific result or native JSON witnesses.

However, the frozen hypothetical failure packer appends lower to the full normal, yielding 18 columns, while its column label and prelaunch shape proof assume four. The prior review missed this shape. No failure artifact was produced. The formal prelaunch serialization bound is conditional on a false normal-length assumption and must not be reused as certified. A future corrected failure schema needs separate review; preserve this run/source unchanged. Mandatory binary sizing would increase by 7,616 B to 19,408 B, still below 20 KB, but that alone does not validate every JSON/layout bound.

## Hashes
- summary.json: `6efb79738c4c05e7eef033cae817ff5da5151ea01bb76d43bb21eb407fcf0d90`
- gates.json: `638a0b47fa233cfa373a3cdc420536e27e66c8f0a616ba1660f2191d17215e39`
- reference/s840163.f64: `57c41683a78b3b467b64ab00109fb92bb78118dfd7c3ff8e87f03803d24c9298`
- supervisor receipt: `d8ccfb55456bd5f9cc3ea3df5d56a0cfaf875f7ecfc781b3e49544cddb22b8ee`
- outer receipt: `ca564631bb2938cf15055a732e7dd25ddc19e770caf671292c0cbe318558043f`

Numerical advantage is supported; event-stress qualification is inconclusive. No physical validation, novelty, general robustness or speedup follows. Prior measured-model limitations and failures stand.
