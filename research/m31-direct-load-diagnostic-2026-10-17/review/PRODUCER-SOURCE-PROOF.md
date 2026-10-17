# Direct-load producer: source-only handoff

Producer: `../source/analyze.py`, 24,394 bytes, SHA256 `d474e67ca9f8695272bda8868ab1848b5058e47d36a2fbac0935a01e020bdff4`. Read-only handoff, not a public freeze or execution authorization. This memo contains static reasoning and declared fixtures, not passed test results.

## Interface and frozen inputs

`run(root, config=None)` returns one JSON-compatible object. With no explicit config, it reads `config.json` beside the module. It has no CLI/main routine and imports only Python stdlib modules. The external dispatcher must verify source/runtime/input pins before import, enforce the registered resource limits, serialize exclusively, read back output, and apply the post-output RSS gate. The producer does not implement that dispatcher or certify its own publication.

The six fixed IDs are run-a-t0, run-a-t5, run-a-t10, run-b-t0, run-b-t5, run-b-t10. Only their saved `inputs/<id>.json` and `reference/<id>.json` under `research/m31-normalizer-replication-2026-10-17/results` are consumed. No old baseline call records, simulator, coefficient evaluator, geometry preparer, or independent checker are imported. Prepared force words must match raw input positions 13:17; centers must match positions 0:3. Geometry is taken from admitted saved prepared values and independently checked by the checker, not regenerated here.

Config compatibility: schema `m31-direct-load-config-v1`; fixed states, prior, candidateIterations=48, rootBisections=54, tiers=[1e-8,1e-4,1e-2], and exact mask recipe must match source. Resource fields belong to the dispatcher and are not interpreted by the producer. `constantBits` is exactly `{mg: "3fd0f3a14cec41dd", R: "3fa4462fb7ff5035"}`. `constantProvenance` is exactly `{path: "research/m31-normalizer-replication-2026-10-17/results/index.json", sha256: "3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393"}`; no `fields` member. Parent supplied these words by reading the already-public saved record. This agent did not recompute or inspect that record.

The producer verifies state admission, canonical input-envelope hash, 64 distinct stable IDs, prepared/load ID order, pair domain/uniqueness/completeness, positive-term count, nonnegative coefficient intervals, and their fixed192 endpoint grid. A positive term with zero lower endpoint remains positive. Structural or resource failure is a failed attempt; no substitute state or retry is supplied.

## Native recipe and mask

The omitted mask is exactly ceil(P/10) declared positives, sorted by exact coefficient upper endpoint then stable (receiver ID, rotor, source ID). Mask order is retained in the output. Native row accumulation instead follows input source order, independently of the mask ranking or a tree traversal.

Both proposals start at all ones. Each reference coefficient midpoint is formed exactly as `(aL+aU)/2` and converted to `float` once. This differs from the prior JS numerator/denominator conversion; no bit-equivalence with the old baseline is claimed. Native force sums are explicit left folds from 0.0, followed by force/total division. Each round left-folds weight*x, uses `math.sqrt`, left-folds midpoint*y in source order, and performs exactly 54 bisections of x^3+alpha*x=1 over [0,1], using strict `>1` to update hi. All 48 rounds update simultaneously. No `sum` over floats, `fsum`, fused operation, residual stop, reference-root warm start, or outcome-based adaptation is used.

The full and omitted candidates are always generated for all six states on a structurally valid completed attempt. A/B/C numerical outcomes cannot truncate that schedule: exactly 12 proposals. Full-control A strict interpretation is deferred until independent checking.

## Arithmetic inclusion argument

Every candidate float is converted to its exact dyadic rational. Source weights are nominal prepared force / exact sum of the four forces. Candidate y is the square root of sum(weight*x), enclosed on the fixed absolute 2^-192 grid. For nonnegative rational q=n/d, k=isqrt(floor(n*S^2/d)); the endpoints are k/S and (k or k+1)/S according to exact equality k^2*d=n*S^2. This encloses sqrt(q), including perfect squares, using integer arithmetic only.

B sums full nonnegative coefficient*y intervals. C retains kept contributions and replaces the omitted sum [L,U] by [0,U]. Therefore C's contraction contains B's for the identical candidate; this is upper-only omission, not a geometric bound. The emitted mass diagnostics separately retain coefficient mass and candidate-weighted mass for all 256 rows, including zero rows.

For each row, p=[x^3+x*sL,x^3+x*sU], k=max(1,pU,1/pL), K=max(k). Positive x and nonnegative s ensure pL>0. Apply the inherited M-current corollary [x/(kK),min(1,x*kK)] using exact rationals. Then floor its lower endpoint and ceil its upper endpoint to the 2^-192 grid. This root quantization is outward, preserves containment, and keeps endpoints in [0,1]. The emitted `xstar` is this quantized enclosure; the raw unquantized root is reconstructible from x,k,K. This deliberate quantization avoids denominator growth when adding four signed rotor loads. All other rational sums/products/divisions remain exact; norm square roots use the same fixed192 enclosure.

Loads are f_nom*x, collective sum, actual signed axis*collective, and sum(cross(actual offset,actual axis)*rotor). Candidate loads are exact points. B/C loads are propagated from the emitted root boxes with sign-aware scalar multiplication. Correlations can be lost but enclosure is preserved. No x-squared load rule or unsigned lever substitution is used.

A uses saved independent load boxes. A scalar error lower endpoint is distance from the candidate point to that interval, and the upper endpoint is the larger endpoint distance. Vector lower/upper bounds use sums of squared componentwise minimum/maximum distances and outward square roots. Normalize rotor by mg/4, collective and world force by mg, moment by mg*R. Category maxima take the maximum of all constituent lower endpoints and separately the maximum of upper endpoints. Reference midpoint truth is never assumed.

B/C use the same distance calculation on propagated load boxes. Those boxes include the candidate itself, so lower error endpoints are zero. B/C upper>tolerance is `not-certified`, never a measured failure. A uses `pass` (upper<=tau), `definite-fail` (lower>tau), and otherwise `unresolved`. Equality passes. No precision extension resolves overlaps.

## Exact output shapes

All rationals: `{n: decimal_string, d: positive_decimal_string}`, reduced. All intervals: `{l: rational, u: rational}`. Integer IDs/counts are JSON integers. Candidate `xHex` values are Python `float.hex()` strings; the checker must reconstruct their exact dyadics and independently replay the declared native recipe.

Top-level keys: `schema, scope, constantBits, constantProvenance, arithmetic, tiers, primaryTier, interpretation, fixtures, states, proposalCount`. Schema is `m31-direct-load-diagnostic-v1`; proposalCount=12. Exact descriptive strings are in source.

Each state: `id, inputSha256, inputFile, referenceFile, positiveTerms, maskRule, mask, proposals`. Each file pin: `path,bytes,sha256`. `mask` is an ordered list of `{i,r,j}`. `proposals` order is full then omit10.

Each proposal: `id, omittedCount, candidate, candidateLoads, sourceY, A, B`. Only omit10 also has `C, omissionDiagnostics`. Full omittedCount=0. Candidate entries: `{id,xHex:[four strings]}`. CandidateLoads entries: `{id,loads:{rotor:[four rationals],collective:rational,force:[three rationals],moment:[three rationals]}}`. SourceY entries: `{id,y:interval}`. These lists use input drone order.

A: `{maxErrors,tiers}`. B/C: `{rows,K,maxErrors,tiers}`. Rows are input receiver order, rotor 0..3: `{i,r,s:interval,p:interval,k:rational,xstar:interval}`. K is rational. No redundant propagated load boxes or per-drone error arrays are emitted; the independent checker reconstructs them exactly from roots and prepared geometry.

`maxErrors` has exactly rotor, collective, worldForce, worldMoment, each an interval. Each tiers entry: `{tier,categories,overall}` in the fixed tier order. Categories has those same four keys. A overall is pass iff all pass, else definite-fail if any definitely fails, else unresolved. B/C categories and overall use only pass/not-certified, testing upper endpoints. OmissionDiagnostics order is all 256 input-receiver/rotor rows: `{i,r,omittedCount,coefficientMass:interval,candidateWeightedMass:interval}`.

## Fixed fixture roster — declared, unexecuted

1. sqrt-one-exact
2. sqrt-two-fixed192
3. root-grid-outward-nondyadic
4. root-grid-exact-boundaries
5. cubic-alpha-zero
6. cubic-alpha-seven-fourths
7. candidate-y-one
8. signed-cancellation-and-linear-rotor-load
9. signed-load-boxes
10. upper-only-contraction-contains-full
11. exact-error-boundary-pass
12. exact-error-boundary-fail
13. exact-error-boundary-overlap
14. signed-euclidean-three-four-five
15. ceil-ten-percent-upper-tie-zero-lower

Each future successful fixture emits `{name,passed:true}`. Assertions retain the exact analytic expectations in source. No fixture was imported or executed during preparation. Independent checker controls and corruption cases remain independently authored.

## Resource and scientific limits

The source schedule has 12*48*256*54 = 7,962,624 native cubic-bisection loop iterations. Outward root quantization keeps later load arithmetic dyadic apart from fixed normalizations. Only one state's parsed inputs/reference are retained during production, plus accumulated output. Omitting redundant propagated boxes reduces output size. These are source-derived observations, not a demonstrated runtime/output/RSS fit.

Parent's revised external limits are CPU 120s soft/121s hard, 180s alarm, 16 MiB/output, observed post-output RSS<=512 MiB. Source preparation neither tests those limits nor promises success within them. A future failed/oversized attempt remains failed evidence without automatic retry.

The checker must independently apply all-six full-control A strict validity, fixed omission accuracy/certificate branch decisions, and positive-denominator nontriviality. These oracle masks and certificates are not a cheap practical algorithm. No speed, Q-current interface, physical validation, holdout confirmation, or 5,000-drone browser claim is made.

Preparation read source files only, plus the parent's draft source config/protocol. An overly broad read of the historical baseline spec exposed its old static scene literals; no six-target saved input/reference/result was opened by this agent. No Python import, parse/compile check, fixture/test, scientific execution, new allocation, or frozen-source modification occurred. Source review and parent acceptance remain prerequisites to any separate execution decision.

Public-copy note: the temporary source handoff path was replaced by its package-relative destination; source bytes and reported digest are unchanged. Original handoff memo retained locally.
