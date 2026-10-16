# Saved-result interpretation: four-rotor coupled solve

This review reads the saved candidate evidence, independent review, run records, publication receipt and stdout summaries from `research/m31-coupled-solve-2026-10-16/results`. It performs no rerun, new root evaluation, coefficient calculation, dataset scoring, or new experiment. Numerical values below are transcribed or rounded for display from those saved records.

**Supported conclusion:** the four frozen cases passed the declared bounded development-verification checks for the explicitly assumed steady four-rotor source/receiver contract. Both one-shot invocations exited zero, and the saved independent review reports **10,007 passing checks, no failures and no fatal error**. This is implementation evidence for designed fixtures, not physical validation or a population-level result; the checks are not 10,007 independent experiments.

The run records identify published source commit `4068504296c6b5cc9f4f0139b5813797f7a2b097` and source-manifest hash `e6baf88c10fad32c8a0fee287989b6675c6144ba2d25440a34896b43e16ac941`. The saved publication receipt reports an exact remote commit/manifest read; it explicitly says the individual source blobs were not each remotely fetched. The evidence and review hashes recorded by the runners are, respectively, `e86fe34d98eb7fab677657dd2f2e9b075802555fa16f2f71cc48853e93443e71` and `7c841146c2e134e67367f960d237aee0e23e31b29407f3206b9b44e33c45aec8`. This interpretation does not independently re-fetch those artifacts.

## What the saved cases establish

| Fixture | Saved influence/admission result | Direct root closures | Picard update root closures | Final residual root closures |
|---|---|---:|---:|---:|
| Level ladder | Admitted; 27 vehicle edges; direct order eligible | 32 | 256 over 8 updates | 32 for each method |
| Tilted ladder | Admitted; 27 vehicle edges; direct order eligible | 32 | 256 over 8 updates | 32 for each method |
| Hexagon cycle | Admitted; six vehicle edges; direct order ineligible | No direct solve | 192 over 8 updates | 24 |
| Nearby rejection control | Six symbol-4 rejected rotor pairs | No solve | No solve | No solve |

The independent review reports agreement of final amplitudes and every retained rotor force under the frozen relative tolerance. The ladders therefore support the narrow statement that the admitted ordered pass reaches the same checked steady solution while performing fewer receiver-root closures than the saved simultaneous updates. Count the separate residual work on both sides. The first Picard update supplies the uncoupled-source ablation and must not be counted again as extra work.

Geometry costs remain separate: each ladder evaluated 224 rotor pairs; the hexagon evaluated 120; the nearby control evaluated eight. Positive rotor terms were 108, 104 and 24 for the admitted cases. These are saved work counts. They do not include every arithmetic operation or establish elapsed speed, browser/GPU performance, end-to-end speedup, scaling to 5,000 vehicles, or trajectory-level behavior. The recorded supervisor elapsed times are explicitly marked as non-performance measurements.

The nearby case is an admission test, not a solved zero-interaction case. Its empty accepted-edge list, zero coefficient placeholders and vacuous descending-order flag must not be presented as a valid physical solution. `solutions` is null, as required.

## The stronger theorem was not numerically distinguished here

The saved ordinary sup-norm bounds are:

| Admitted fixture | Ordinary `Lmax` |
|---|---:|
| Level ladder | 0.4801001142677395 |
| Tilted ladder | 0.16879798955673844 |
| Hexagon cycle | 0.07417511219535824 |

Every admitted case already lies below one. Thus ordinary contraction suffices for these cases; their convergence does not demonstrate the additional domain covered by the global one-half log-space theorem. The log theorem remains an analytical result for the fixed nonnegative-coefficient contract. The saved runs neither establish its empirical necessity nor show a solver-speed advantage attributable to that theorem. Its existence/uniqueness conclusion is mathematical, not inferred from eight observed updates.

## Residual estimates, reported rotor forces, and source totals

The independent reviewer uses binary64 geometry and 80-digit Decimal roots for the serialized coefficient system. Its residual-derived values are numerical estimates, not outward-rounded certificates. A zero binary64 residual in the ladders does not imply an exact mathematical fixed point: the saved high-precision residuals are nonzero.

The estimate `exp(2*r_log)-1` concerns rotor forces reconstructed through the exact mathematical root map at the candidate amplitude. It does not, by itself, include rounding in the reported binary64 rotor roots/forces, coefficient construction, or the high-precision residual evaluation. The saved numbers make this distinction visible: in the level ladder the maximum saved rotor relative difference is about `3.13136e-16`, while the residual-only theoretical estimate is about `2.20028e-16`. The tilted ladder also has a slightly larger saved force difference than its residual-only estimate. This is compatible with the omitted numerical evaluation errors; it does not contradict the exact-real theorem. Do not call the residual-only estimate a complete certificate for the saved floating-point forces.

For the hexagon, the saved high-precision log residual is about `6.98990e-14`, the residual-only rotor relative estimate is about `1.39798e-13`, and the maximum saved rotor relative difference is about `9.25672e-15`. These are observed estimates/comparisons within the declared tolerance, not new accuracy guarantees.

Before exact convergence, the provisional source total `T0_i*y_i^2` and the reconstructed receiver total `sum_r f0_ir*g(alpha_ir(y))` are different quantities. The saved maximum source/receiver total mismatches are approximately `3.30469e-17 N`, `5.56253e-17 N`, and `3.38338e-14 N` for the level ladder, tilted ladder and hexagon. Their small values support numerical consistency of these particular candidates; they must not be erased by defining the two totals to be identical. Individual rotor forces remain distinct throughout the contract.

The saved uncoupled-source ablation has maximum relative rotor-force differences of approximately `0.235692`, `0.0375426`, and `0.00514379` from the corresponding coupled reference results. These differences show that effective-source feedback changes the assumed model's predicted loads in these fixtures. They establish neither improved physical accuracy nor the sign or size of an actual vehicle effect.

## Most informative next verification and the separate physical gate

The most informative next computational question is whether a **fresh, prospectively specified cyclic case outside the ordinary contraction certificate's range** can converge with a checked per-rotor error estimate that includes inner-root/map evaluation error. The relevant criterion should defeat the tighter weighted ordinary bound as well as the conservative row-maximum bound; otherwise the example may only expose a loose bound. Positive root enclosures or another explicit numerical error analysis would address the incomplete force certificate seen here. Keep all four receiver roots and independently check source/receiver consistency.

If that future case is defined directly by coefficients, label it an algebraic contract test. A claim about the geometric field additionally needs those coefficients to arise from an admitted frozen geometry, with no near-field substitutions and all amplitude caps satisfied. Choose the case and limits analytically or by a separately declared design process before scoring, rather than tuning these completed cases. End-to-end timing would be a different planned verification, required before a runtime claim. No such experiment is allocated by this note.

The physical gate remains independent and unresolved: an identified source propeller/drive needs independently measured effective thrust and spatial flow across locked actuator conditions to test fixed-shape thrust scaling, including unequal source-rotor loading. The receiver closure also needs load/inflow evidence under a named actuator/control condition. Measurements require usable uncertainty and provenance. Nominal force, PWM, RPM, effective thrust and shaft power must remain distinct. More numerical agreement cannot supply these missing physical contracts.

The present result is therefore a successful finite implementation checkpoint for an explicitly source-dependent steady mathematical model. It does not establish physical validity, stability, novelty, safe flight, a calibrated aerodynamic law, or publication readiness.
