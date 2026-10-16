# Independent protocol challenge: binary64 zero filter

Date: 2026-10-17. Reviewer: `m31_protocol_challenge`. This began as a design-only review; the parent subsequently authorized a bounded first verification protocol and independent checker authoring, with execution still gated by source freeze/publication/exact remote verification. Closed cost artifacts are immutable and their numerical outputs were not read or used for fixture tuning.

## Recommended claim and trust boundary

Use a scalar-only, branch-preserving **zero-or-exact-fallback** filter. Keep preparation, the exact hierarchy/global guard, the exact rational scalar law, positive coefficients, cap decisions, load solves and the four exact `1e-8` tolerances unchanged. A successful filter decision may return a zero only after proving that every earlier guard/branch is skipped in the original scalar order. Otherwise run the original exact scalar from its beginning. Do not return a native approximate positive coefficient or native rejection.

The narrowest useful alternative is only `neighbor`, `upstream`, and `down-cut` zeros: it needs outward add/subtract/multiply and avoids width/division/radial/projection proof obligations. If the parent's broader zero filter is retained, those later branches require the same strict earlier-branch proof and explicit arithmetic-domain handling. There is no need to expand to native positive/cap/root work in this cycle.

Treat prepared native words as exact dyadic singleton inputs. Each outward primitive must enclose the exact real result of its dyadic operands, with subnormal and signed-zero behavior covered. Nonfinite intermediates, invalid interval order, a denominator interval containing zero, or an unproved comparison cause fallback. No epsilon cutoff, inward endpoint, guessed cancellation, “almost zero,” or reassociation may substitute for an enclosure proof. The actual rounded rotor point is the input; the stored lever offset cannot silently replace `point-center`.

There are three separate obligations:

1. **General source proof:** explain the IEEE neighboring-word operation, primitive enclosure construction, guard/branch implications and fallback completeness. Finite fixtures cannot prove all binary64 values.
2. **Finite correctness:** independently verify the frozen primitive and raw-state cases below against exact dyadic arithmetic and the inherited independently pinned scalar reference. The reference helper and its previous mathematical review remain an explicitly inherited trust boundary; this cycle does not re-prove its entire law.
3. **Total cost:** defer measurement to a later fresh, prospectively frozen suite. Neither avoided exact calls nor a correct filter establishes a speedup. This cycle has no full load-solve or group-performance claim.

## Frozen small suite

The accepted expansion is **108 ordered rows**: 72 primitive rows, followed by 36 full-raw pair queries. The journal has one header, one durable event per row, and one completion event: **110 events**. No parameter sweep, witness search, adaptive repeat or changed input after observing results is permitted.

Primitive rows comprise:

- `nextUp` and `nextDown` for 16 fixed words: both signed zeros, both signs of minimum subnormal, maximum subnormal, minimum normal, one, maximum finite, infinity, and a quiet NaN. Finite boundary stepping may expose an infinity sentinel; it must never become a finite interval endpoint. Nonfinite input falls back.
- Eight rows each for add, subtract, multiply and divide: positive/negative rounding ties, cancellation, subnormal/underflow, sign combinations, nondegenerate intervals and overflow; division includes a zero-enclosing denominator.
- Eight square rows: zero crossing, signed zeros, positive/negative tiny subnormals, positive/negative nonzero intervals, overflow and reversed endpoints.

The exact raw words and operand endpoints are frozen in `source/spec.json`; original pair decimal/explicit-hex declarations are preserved under `prefreeze/`. Input authoring performs only standard decimal-to-binary64 serialization explicitly authorized by the parent, not candidate imports or model evaluation.

The 36 pair queries have complete 17-word receiver/source states and a declared rotor:

| Family | Count | Purpose |
|---|---:|---|
| Neighbor/center priority | 8 | Safely outside/inside, equality and adjacent words at distance 3, negative and diagonal displacements, center component guard equality. |
| Upstream/down-cut | 8 | Negative and zero down, both signs of minimum subnormal, equality and adjacent words at 2.5, an interior down value. |
| Tilt/cancellation/translation | 8 | Tilted and permuted axes, cancellation near zero/2.5, large common translation with rounded rotor points, and a center guard that must outrank a tempting zero. |
| Exact tail/invalid | 12 | Positive, near rejection, near-outside/radial/projection zeros, far cap rejection, overflow-prone geometry, zero/negative force, invalid quaternion, nonfinite unused velocity/angular input. |

These are interpretable branch challenges, not a claim to cover every physically possible state. Some guards are unreachable under preceding validated bounds; do not invent a required witness for an unreachable branch. For example, all three center components bounded by 257 imply squared norm below `512^2`; nevertheless the original checks and precedence remain part of the source proof/interface.

## Saved record and independent validation

Primitive rows retain their exact declared arguments or stepping word and either a finite interval, a neighboring word, or an explicit fallback reason. The checker independently computes exact endpoint ranges; invalid/reversed intervals and zero-enclosing denominators must fall back. A conservative fallback for finite arguments is allowed, but mandatory finite-interval and useful fast-zero witnesses prevent an all-fallback implementation from qualifying.

Pair rows retain raw words, the complete `A.prepare` output, the original exact scalar result and the candidate decision/result. The checker independently regenerates preparation and the raw-state rejection precedence. For valid preparation it independently evaluates the inherited fixed-192 scalar oracle, validates **each** saved result's status/branch/domain and full returned coefficient-related intervals, then compares baseline and candidate full results exactly. Preparation failure is not a filter fast zero. A claimed zero on a positive or rejected model outcome fails even when the candidate agrees with a corrupted baseline.

No native replay or candidate source import belongs in the independent checker. Only the exact frozen independent helper may be loaded after manifest/source-buffer verification. Files and the complete ordered journal bind retained records to the source/spec/runtime pins. A journal is execution provenance, not cryptographic attestation that the recorded computations occurred.

## Exactly 16 fresh controls

The final machine contract fixes recipes and intended failure families. Semantic checks precede baseline/candidate equality and generic journal rejection.

1. Inward upper endpoint on a positive rounding-tie addition.
2. Inward lower endpoint on a negative rounding-tie addition.
3. Underflow product incorrectly collapsed to exact zero.
4. Overflow product claimed as a finite point interval.
5. Zero-enclosing divisor claimed to produce a finite interval.
6. Zero-crossing square given a falsely positive lower bound.
7. Known positive pair falsely classified zero.
8. Center-guard rejection incorrectly preempted by a zero.
9. Correct zero status with the wrong scalar branch.
10. Prepared rotor-point bit changed while raw input remains fixed.
11. Positive exact-fallback coefficient replaced by zero.
12. Invalid preparation bypassed with a fabricated candidate result.
13. Missing ordered row.
14. Duplicate ordered row.
15. Reordered rows.
16. A journal row inconsistent with the saved result.

Every control uses a fixed case ID or a prospectively declared first witness, requires its intended mathematical/coverage/provenance failure, and retains a bounded witness. Missing witnesses, a passing mutation or equality-only rejection fails the cycle. Do not rerun the previous cost/exact-screening controls.

## Qualification, stopping and later cost

Require all 108 records and 16 controls, source/input immutability, exact fallback identity, preparation/branch correctness, coefficient containment and the declared useful-witness coverage. Any failure is informative and stops qualification; preserve the attempt, do not retry or tune against it. Resource refusal is also a failed allocation. Concrete time/RSS/output limits and closed-set accounting must be frozen by the supervisor before execution; source-only output-size analysis is permitted, numerical budget probes are not.

After finite correctness succeeds, a later cost cycle should independently freeze a new heterogeneous geometry suite with admitted small groups, boundary-heavy fallback groups and clearly screened groups. Compare complete exact versus complete filtered scalar first, then separately compare exact hierarchy versus the same hierarchy with filtered residual scalar calls if useful. Both methods pay their own preparation/native-cache/filter/fallback costs from identical raw words; measure complete raw-words-to-method-record work with every proof, canonical assembly and unchanged load certificate. Use retained warmups and a fixed paired order, bind all trial science to first-measured representatives, and report all durations and fallback/fast-zero counts without replacing time by work counts. Do not tune this suite on the closed six lattice timings, and do not claim browser/dynamics/5000-drone/physical/novelty success from it.
