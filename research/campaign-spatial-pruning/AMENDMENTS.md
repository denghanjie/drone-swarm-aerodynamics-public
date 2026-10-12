# Append-only pre-run clarifications

## 2026-10-12, after independent physics and experiment review, before benchmarks

- PLAN.md is preserved unchanged and its original SHA-256 is recorded in PLAN.original.sha256.
- The force/moment thresholds are model-relative screening budgets deliberately compatible with epsilon 0.04 and a 2.25×hover nominal rotor cap. They are not physically or application-validated usefulness/safety thresholds. Actual nominal thrusts above the cap are measured against actual-state bounds; the cap-based guarantee never silently extends to them.
- The pair upper bound clamps its minimum downstream at the valid far-field start, and its maximum downstream at existing support. Near-wake guards always precede omission and inspect all four original rotor points when the conservative center envelope can contain a near-domain point. Outside that envelope no rotor can be near-domain.
- Zero-budget fields must be permutation-equivalent to roundoff. Positive-budget greedy omission may choose different sources under permutations; each permutation must separately satisfy its accumulated bound and force/moment gates. Equal pruned fields are not required.
- The original module does not comprehensively validate malformed states. New explicit finite-state/unit-quaternion rejections are separately reported as hardened input handling, not claimed as identical legacy behavior. Shared legitimate model-domain outcomes still must agree.
- The matched zero-budget module computes the identical geometric bound and skips exact-zero support pairs. Thus a pruning speedup cannot be credited merely to allocation reduction or new exact-zero support culling. Original legacy cost, optimized zero-budget cost, and positive-budget costs are reported separately. All variants retain the same four receiver locations and response law.
- Closed-loop experiments remain separate numerical diagnostics, and may be useful even if pruning has no speed advantage. Begin at 16 agents for at most 1 s after tiny gates, within the assigned timing slot. No controller tuning or attractive-outcome selection.

## 2026-10-12, development failure v0 and bound refinement before held-out evaluation

- Independent robustness inspection found the no-fade envelope cannot have a positive value below 0.0487890367 m/s, above the largest preregistered epsilon 0.04. The first tiny checks accordingly omitted no positive-bound pair. This failed candidate is preserved as source-versions/pruned-aero-v0.cjs.txt with hash, and results/tiny-checks-v0-no-positive-omissions.json. No speed claim or held-out run occurred.
- Candidate v1 multiplies the envelope by conservative upper bounds on the two existing fades. The downstream fade is evaluated at dmin; the radial fade at rmin/halfmax. Both fades are nonincreasing and both arguments are lower bounds on every valid rotor argument, so multiplying their upper bounds remains conservative. All budgets/thresholds/scenarios remain unchanged. This is a development correction, not threshold adjustment after evaluation.
- Pre-freeze review inflated the near-domain center envelope by 1e−9 m plus the same rotor-offset inflation used by the bound, covering accepted quaternion roundoff. New load/bound helpers reject negative nominal thrust explicitly instead of silently clipping it. These are input/roundoff hardening changes; no physical law or threshold changes.

## 2026-10-12, publication scope update

- Later project authorization permits coherent GitHub branch checkpoints after privacy and evidence review. The initial plan correctly preserves its earlier local-only scope. No main-branch merge, public hosting, paid compute or expanded scientific claim follows from checkpoint permission.
- The preregistered original PLAN.md remains unchanged and its hash is preserved. Publication copies make documented neutral editorial changes to review-role wording; publication-edits.json records original and published hashes. Scientific criteria, budgets and methods are unchanged.
- Model-domain exit status is preserved. When several source/rotor violations occur simultaneously, source-major guard traversal can report a different first violating pair from the original rotor-major traversal; exact tie-event identity is not claimed.
