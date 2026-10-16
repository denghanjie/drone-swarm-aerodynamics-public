# Independent coupled-system checker: source-stage review

Prepared 2026-10-16 before target coefficient/root evaluation. This is source
construction and static scrutiny only. `check_saved.py` has not been invoked on
any fixture or scientific input. Its eventual invocation requires the coordinator's
separate frozen-source and saved-evidence authorization.

## Inputs reviewed and implementation independence

Read the new coupled-solve `PROTOCOL.md`, `review/CONTRACT-CHALLENGE.md`, the
historical geometric derivation, source-accounting `reference-excerpt.cjs` and
`witness.cjs`. Read candidate `source/experiment.cjs` solely as text to establish
the saved JSON schema and inspect its source. The checker imports no candidate,
historical JavaScript module or third-party package.

The Python stdlib implementation reconstructs fixture geometry from the protocol,
including the near-rejection frame. It checks serialized geometry against that
construction, then independently evaluates historical support on the serialized
geometry through vector operations rather than the candidate's packed layout.
The fade is evaluated in an algebraically expanded form. All pair symbols,
validity/stage codes, diagnostic coordinates, K and dimensionless a coefficients
are compared. Float comparisons use the declared `2e-12 + 2e-12*abs(reference)`
tolerance. Geometry/coefficient/admission failures prevent reference solving of
the affected case.

## Static conclusions and prospective clarifications

The log contraction proof is consistent with the retained four-rotor, fixed
nonnegative-coefficient contract. In particular, zero coefficients must remain
admitted zeros, individual nominal rotor forces must be positive, and source
totals and recomputed receiver totals are distinct away from a fixed point.
The per-rotor relative error expression follows from the log-state error bound;
it must not be relabeled a rigorous numerical certificate without enclosing
inner-root/map error.

The deterministic near-frame recipe is now explicit: for the prescribed corner
unit direction e, set f=axis cross e, u=(-e+f)/sqrt(2), v=axis cross u. With the
frozen corner ordering, rotor 0 is R*e. This removes the former ambiguity in the
phrase “choose a square frame.”

The candidate saves its final residual map separately from the loads generating
the last Picard update. The checker evaluates the map at the returned state,
checks that residual map and compares its individual rotor forces with the
independent solution. Direct stored loads are also compared explicitly with both
the reference and the simultaneous result.

The global one-half log contraction alone did not guarantee `1e-40` within the
initially proposed 100 outer updates. Before any evaluation, the coordinator
prospectively increased the reference outer cap to **160**. The finite-input bound
uses at most seven incoming sources, the per-source speed cap and the minimum
nominal rotor force to bound the first log displacement, after which the global
contraction applies. The checker uses 160 outer updates and 100 inner Newton
updates. This is a pre-execution design revision, not a result-driven retry.

The candidate work field is `bisectionIterations`: it counts 56 loop evaluations
for each positive-alpha root. It must not be described as 56 actual IEEE-754
bracket halvings, since midpoint stagnation is possible. `candidatePass` contains
candidate-only gates; complete development qualification also needs the independent
geometry, numeric and agreement checks.

## Numerical definition and coverage

JSON floating numbers are parsed directly as Decimal, preserving their serialized
decimal spellings. The reference uses saved a and saved nominal rotor f0. It
recomputes S0 as the Decimal sum of those f0 values; saved binary64 S0 is checked
as an approximate sum, not promoted to a new independent constant. Map evaluation
uses `sqrt(sum(f0*x)/sum(f0))`, retaining normalized weights and avoiding a separate
sum of rounded individual weight fractions. This agrees with the exact-real
normalized-weight contract up to the declared Decimal arithmetic. Candidate
binary64 versus reference differences are evaluated at the frozen tolerances.

Inner roots use rearranged Newton updates in 80-digit arithmetic, with polynomial
residual target `1e-65`; the outer reference uses synchronous Picard with a directly
reevaluated final log-residual target `1e-40`. Nonconvergence within the frozen caps
is retained as failure. There is no automatic cap increase or fallback method.
The script has a cooperative 115-second guard within the 120-second review budget;
external wall supervision remains the coordinator's responsibility.

The checker verifies:

- Exact fixture list, nominal forces, frames, complete non-self pair inventory,
  full-cube scaled pair caps, admission and graph records.
- Ladder descending DAG/positive height edges, all four rotor terms on each
  prescribed hexagon-cycle edge, and both constructed near-corner rejections.
- Every saved Picard transition, initialization, final state, first eligible stop
  up to a declared `3e-15` binary64 log-reconstruction allowance, and convergence.
- Direct eligibility, uncoupled one-update map, final maps and all root/iteration/
  positive-term work counters. The uncoupled calculation is the first Picard
  update, not additional candidate work to add a second time.
- Every final amplitude and rotor force against the Decimal solution at `1e-9`
  relative tolerance, including direct-versus-simultaneous comparisons.
- Independently recomputed final log residual, `2*r_log`,
  `exp(2*r_log)-1`, source/receiver total mismatch and uncoupled force difference.

These high-precision values are numerical estimates, not outward-rounded interval
enclosures. The checker makes no physical-validation, trajectory, speedup, browser,
GPU, population or 5,000-drone claim. Output creation is exclusive; failures are
saved and exit nonzero rather than overwriting an earlier review.

Viewer-facing output has top-level `passed`, `check_count`, and `checks`, with
each check represented as `{name, passed}`. `failures` contains failed names;
`cases` contains reference solutions and candidate-final diagnostic summaries.
Decimal values are serialized as strings to retain precision. This is the output
schema; no output record has been generated during source construction.

## Planned invocation after authorization only

`python3 check_saved.py SAVED_CANDIDATE_JSON NEW_REVIEW_JSON`

Ordinary syntax parsing may be performed before freeze. Importing or invoking the
checker, including synthetic fixture evaluation, is outside this source-only stage.
