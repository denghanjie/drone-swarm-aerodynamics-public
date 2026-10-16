# Independent saved-only review design

Prepared 2026-10-16 for the prospective finite-runtime center-screen experiment.
This is source preparation, not permission to run it. No scientific module was
imported, no control was materialized/evaluated, and no generation, benchmark,
saved-result check or new target access occurred during this preparation.
Validation was limited to source inspection, source copying/hashing, Python AST
parsing and `compile(source, filename, 'exec')` without execution. The parent
owns independent static review, complete source freeze/publication, independent
remote/local/committed-byte verification and the single supervised invocation.

## Installation and inherited pins

Copy `reviewer.py` to the new package's `source/review.py`, as required by the
frozen supervisor. Copy `numeric-reference.py` beside it unchanged. Place this
note in the package's review/source documentation and include all imported
scientific source and these files in the frozen manifest.

The new reviewer imports five scientific entry points from the unchanged copied
reference: `constants`, `prepare_geometry`, `classify_receiver`, `direct_solve`
and `csr_map`; the analytic `positive_root` is called internally by the latter
two. The source is:

- `research/m31-typed-assembly-2026-10-16/source/numeric-reference.py`,
  39,666 bytes, SHA256
  `4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb`.
- Non-scientific review helpers and the independent input/graph census were
  adapted from `research/m31-typed-assembly-2026-10-16/source/review.py`,
  65,581 bytes, SHA256
  `a6018cb1280bbe88182204d497ca4401cef8462588698a1c8aa082f8ecbb8bd5`.
- The unchanged lean comparator is checked against SHA256
  `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96`.

A static AST comparison confirmed that constants, geometry preparation,
receiver classification, analytic positive root, CSR map and ordered solve
have identical definitions in the two inherited Python sources. No functions
were called for that comparison. The copied reference's hash is checked before
its import at the authorized reviewer invocation. The inherited source is never
modified or used to open an old target/result artifact.

The new input census deliberately preserves the current JavaScript contract:
`nominalPositive` requires the *entire state* to be finite as well as positive
nominal motors; `nominalOK` additionally requires finite source totals. Offset
validity includes the finite check of norm-error plus perpendicular-error.
Those details matter for the prospective nonfinite controls. `required` is an
explicit alias of the checked `require` helper.

## Independent checks

The reviewer reads saved files only. It imports no candidate JavaScript,
generator, control module or solver. The fixed control literals/patches are
independently stated in the reviewer and evaluated only during the allocated
saved-review execution.

1. It validates the fixed configuration, complete source pins, inherited lean
   and reference pins, exact runtime identity, the candidate's actual terminal
   closure, artifact inventory, log/RSS/wall/resource records and consumed
   invocation locks. All candidate inventory files are rehashed and their
   summed bytes reconciled. Start/end environment metadata and default runtime
   flags are checked. Independent source publication verification remains the
   parent's prelaunch gate and the external seal's receipt check; a local hash
   comparison is not represented as remote verification.
2. It checks all 48 control IDs, positions, complete 17-value input states,
   patches, signed-zero/nonfinite atoms, before/after hashes, per-build and
   per-solve mutation checks, nullable solve policy and control solve counts.
   Geometry, sparse support/coefficient values, input/admission, graph/order,
   scaling, ordinary bound and assembly accounting are independently rebuilt.
   Admitted descending controls receive the inherited independent analytic
   ordered solve and residual-map check. Rejected controls must retain their
   rejection and explicit no-solve reason; position eligibility alone cannot
   bypass invalid quaternion, nominal, near-field or scaled-cap diagnostics.
3. It validates the exact six ownership builds, their fixed input states and
   hashes, the complete retained planes-66 outputs before/after, and recorded
   storage-disjointness. Extra build outputs are independently reconstructed;
   the planes-62 extras also match their original saved control outputs.
   Evidence includes screen arrays in the harness's storage checks. Saved
   artifacts cannot by themselves prove all future aliasing behavior.
4. It checks the three fixed generation records/seeds/configurations, initial
   and final complete states, all 21 separately pinned pose frames, concatenated
   poses, sample times, finite values, endpoints and final-state input identity.
   It does not run the generator again.
5. For each fresh state, it loads both saved L/F sparse bundles and streams
   their complete symbol tensors one receiver at a time. Every L/F symbol byte
   must agree. All CSR offsets, source IDs, K/a binary64 values and complete
   scientific metadata/solutions must agree exactly, except the two declared
   center-work counts and the separately checked screen record. No checksum
   replaces these full comparisons.
6. It independently reconstructs the finite/span predicate from saved current
   positions, using explicit NaN and signed-zero extrema behavior. For every
   ordered nonself pair it forms the same rounded coordinate differences and
   the fixed `max(abs(dx),abs(dy),abs(dz)) >= 4` predicate. Every omitted pair's
   four L **and** F symbols must be exactly 1. It reconciles all omission counts,
   actual norms, component tests, logical visits, fallback reasons and complete
   candidate omission reports. The original all-pairs certificate remains
   unchanged; the historical skipped-pair counter is explicitly not a formal
   arithmetic certificate.
7. Independent NumPy full geometry classification and positive support are
   checked against every saved symbol/source row; all K/a entries retain the
   inherited tolerance `2e-12 + 2e-12*abs(reference)`. The ordered solution uses
   the inherited hyperbolic analytic cubic formula, not candidate bisection.
   Every source amplitude and rotor alpha/root/force plus every residual-map
   output is checked. Positive solution tolerance remains relative `1e-9`;
   residual gates remain `1e-9` log-amplitude and `2e-9` force consistency.
8. It reconciles all six qualification records and the exact 42-call schedule:
   six L/F warmups and six rotated, alternating paired blocks. Raw timing files
   are pinned and exactly equal to each validated record with only its later
   raw-pin/validation fields removed. Complete time includes the screen;
   fallback F alone adds `screenPreflight`. Every phase and solver/work count,
   qualified checksum/hash, full comparison report and input hash is checked.

All 100 million raw symbols per N=5000 bundle are streamed, not simultaneously
materialized in the reviewer. Independent CSR construction remains under the
fixed two-million-positive-term guard. The reviewer uses the existing 175 s
cooperative and 1.5 GiB RSS limits; the supervisor supplies the separate 180 s
external limit. Sampling/cooperative guards can overshoot. Output creation is
exclusive, preserves failed/partial evidence, and reserves 1 MiB inside the
208 MiB directory cap for supervisor closure.

## Timing output and terminal qualification

`results/analysis.json` has schema
`m31-center-screen-independent-analysis-v1` and contains:

- `independentAuditPass`: the complete internal audit result.
- `performanceRulePass`: Boolean only after all internal evidence gates and
  all 42 timing records pass; otherwise null.
- `practicalRulePass`: always null inside the child.
- `requiresReviewSupervisorClosure`: always true.
- Three case records with `id`, `n`, `seed`, method total/phase raw values and
  median/min/max, all paired F/L totals/ratios/differences, paired median,
  strict wins, phase differences, raw screen counts and per-case gates.

Both N=5000 cases must independently have median paired F/L <= .90 and at least
5/6 strict F wins. N=1000 is contextual. Six paired within-process repeats are
not six independent swarm trials. No performance qualification occurs after
an incomplete/failed audit.

`results/independent-review.json` contains `pass`, reviewer `complete`, separate
`candidateComplete`, named-string `errors`, named `checks` with Boolean `pass`
and optional details, generation/control/qualification coverage, resources,
analysis content and an exact analysis artifact pin. A generic exception class
and failed-check names are retained without private filesystem paths.

A child cannot observe its own terminal supervisor outcome. The separately
frozen stdlib-only `seal.py` must therefore verify **both** actual successful
closed supervisor records, protected source/output identities, the successful
independent report and its analysis evidence before exclusively creating
`results/qualification.json`. The seal combines saved gates only; it must not
recompute targets, tune thresholds or create another scientific allocation.
The viewer must bind practical claims to that terminal qualification and the
actual closure records.

## Limits of inference

This is a finite pinned-runtime experiment. It supplies no portable JavaScript
`Math.hypot` error theorem, no unseen-state certificate and no claim that fewer
norm calls necessarily improve full-query speed. Independent NumPy rounding
can differ; exact symbol checks and declared tolerances are never relaxed.

Timed transient arrays are completely compared within the candidate process
but are not all persisted. The independent reviewer can verify saved qualified
arrays and repeated comparison/hash metadata, not reconstruct every transient
array independently. Source/storage ownership checks likewise cover the
specified calls. The positive-term cap throw is source-reviewed, not exercised
with an extra giant fixture.

The earlier disclosed result-bearing arithmetic-file exposure remains. No
source-preparation step here reread those results or selected new seeds or
thresholds from them, and this note does not claim an unexposed design process.
Short synthetic airflow-off generation and frozen-state loads do not establish
aerodynamic validity, dense mutual-wake physics, coupled flight, browser/GPU/live
cost or a novel contribution.
