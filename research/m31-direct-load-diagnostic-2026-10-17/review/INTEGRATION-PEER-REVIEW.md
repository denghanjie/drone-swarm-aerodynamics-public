# Direct-load integration and independent-checker peer review

Decision: source-only accepted; no material integration, arithmetic, or schema blocker found at the pins below. This is not execution authorization or an empirical resource-fit claim. No Python import, syntax parse/compile, test, fixture, or scientific execution was performed by this reviewer. The earlier producer handoff and source-proof memo remain unchanged.

## Reviewed identities

- Integrated `research/m31-direct-load-diagnostic-2026-10-17/source/analyze.py`: SHA256 `98f1802b3cf880009998bdb1235f57dadd91cc49c4dbd921731501fb8281cf37`.
- Integrated `source/run.py`: SHA256 `6158e4c309797e17d583b0f9ad2ca474b8edd56ec7840bba4c4585298056167e`.
- Integrated `source/config.json`: SHA256 `06faace0212dc10a01510ce8aa591b47a72cfb0833790c0ad1923d1a18ee9e6c`.
- Independent draft `source/check.py`: 44,013 bytes; SHA256 `819a272ccf855765bd0fc6d4331caec784a0d0911d663318ab7a38f3e5c18c51`.

The checker was read at its initial 43,625-byte draft, then the final coupled-native fixture addition was inspected and the final source rehashed. No other logic change was reported by its author. The final integrated producer/config/runner hashes were rechecked unchanged after the checker review. Also read the prospective `ANALYSIS-PLAN.md`; it adds saved-row descriptive comparisons only.

## Producer/config integration

The integrated producer differs from the locked handoff only by checking config `sqrtFractionBits` and `rootFractionBits` are integer 192. Config agrees with the six IDs, prior path, raw mg/R words, exact path+SHA provenance object, native 48/54 schedule, tiers, fixed 10% mask ordering, both precisions, and the runner's current resource constants. The earlier provenance `fields` mismatch is resolved.

No candidate recipe changed during integration. The coefficient midpoint is exact before one float conversion; reductions are left folds in input source order; rounds are simultaneous. Full/omit10 outcomes cannot truncate the fixed 12-proposal schedule. Exact f_nom*x candidate loads, one sourceY list per proposal, absent full-C/present omission-C, all 256 omission-diagnostic rows, exact s/p/k/K, and outward192 roots agree with the checker.

## Runner review

The exclusive initial attempt precedes scientific imports. The runner checks the manifest digest and file pins, runtime bytes, and publication record's commit/manifest/path/size/count/time and verification flags before importing a scientific module. The check stage additionally requires a completed, zero-exit, failure-free producer attempt with matching source identity and output size/SHA.

Limits match config: CPU soft/hard 120/121 seconds, 180-second alarm, 16 MiB/output, Darwin RSS units, and 512 MiB post-output observed RSS acceptance. Output uses exclusive creation, flush/fsync, and directory fsync; final attempt replacement is atomic after a separately exclusive temporary write. Output serialization and readback occur before the RSS acceptance observation.

These remain the registered operational limits, not stronger guarantees: the alarm excludes interpreter startup/teardown; the final usage snapshot precedes final attempt serialization; a deadline signal during reporting need not produce a complete failure report. The RSS threshold is an observation after output, not enforced memory containment. The runner retains failure state rather than accepting a failed checker. No new execution or retry is implied by this review.

## Independent checker review

Constant expectations are not only copied between config and producer: the checker separately reads the saved index, checks its SHA against `3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393`, and compares the actual saved `constants.mg`/`constants.R` with the frozen words. The supplied words are decoded using integer sign/exponent/significand arithmetic. This reviewer did not open that target record; its future provenance check is inspected in source.

The reference schema and `loads` shape agree with the frozen `scene_reference` / `semantic-reference.py` source already inspected. The extra reference-root/load identity test uses the same exact signed propagation that produced those saved boxes; it does not recompute physics or demand a new reference. Input-envelope hashing, admitted prepared IDs, force/center binding, pair completeness/positivity/grid and positive denominator all align.

Native replay independently reconstructs input-order terms and the full/omitted recipe, then requires exact xHex equality. Integer hex-to-rational parsing retains the exact candidate. Native values remain proposals only; exact certification uses exact force weights and independent rational source-y reconstruction.

Checker square roots use a separate Newton integer-floor implementation and explicitly prove squared endpoint inclusion. Root quantization, exact local/global factors, signed load propagation, scalar interval distance, vector norm bounds, category maxima and normalization agree with the producer. No reference midpoint is used as truth. The checker enforces C/B contraction, root, load and error-upper containment relations. Its A-versus-certificate consistency checks use necessary lower/upper conditions, not a claim that the finite independent reference interval must always be contained in the other interval.

Wire schema, strings, order, exact rational representation, 15 producer-fixture names, 12 proposals, 3,072 candidate rotors, 96,768 reference pairs, 4,608 certificate rows and 1,536 omission-diagnostic rows align. Full C is absent; all six omission C records are checked. Corruption checks use one saved first-state omission record and do not construct fresh scientific candidates.

A classifications are pass/definite-fail/unresolved; B/C are pass/not-certified with zero error lower bounds. Record validity is explicitly separate from scientific headroom. Decision order correctly requires all-six full-control A strict pass before omission attribution, blocks zero-positive vacuity, then considers stress definite failure, strict A nonpass, B insufficiency, C insufficiency, or strict headroom requiring a separate practical experiment. Loose tiers cannot override the strict gate.

## Controls and prospective interpretation

The final checker declares 29 literal fixtures and 13 saved-record corruption controls. Their arithmetic expectations and targeted failure paths were reviewed statically; this memo does not say they passed. In particular the two-drone 7/4 chain has source roots 1 and receiver roots 1/2, exact retained defects 1, and K=1; deleting its four receiver terms yields all-one native roots. That addition exercises both literal native modes without inspecting target outcomes.

The prospective equality note is unchanged: if each C lower defect tL and shared upper defect U satisfy tL*U>=1, B/C local factors equal U, yielding equal global factors and root/load certificates. The analysis plan correctly evaluates this sufficient condition from saved C endpoints, counts satisfied and unsatisfied rows with denominator 256, and reports exact equality separately. It makes no prediction or candidate change. B/C equality need not imply equality of contraction uncertainty or necessity of the sufficient condition.

All findings are limited to static review of the identified source versions. Parent public freeze/pin verification and a separate allocation remain necessary before execution; any later code change requires corresponding delta review. No new target values or direct-load results were read during this peer review.

Public-copy note: isolated temporary checker path replaced by its package-relative destination. Original review remains locally retained; source digest and findings unchanged.
