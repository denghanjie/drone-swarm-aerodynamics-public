# Second-reader static audit of the swarm saved-record checker

Prepared prospectively on 2026-10-16. Status: final source reread complete;
identified definite defects resolved. This is a private source-only
mathematical/numerical review.

## Scope and non-execution

Read the checker as text against the public PROTOCOL.md, SCHEMA.md,
reference-excerpt.cjs, experiment.cjs and run-review.py. Read only source-identity
metadata from inputs/index.json. Did not read target f64 contents, import or
execute the checker or JavaScript, evaluate any fixture or target science, or
rerun a closed allocation. The author separately reports AST-only parsing; this
second-reader review did not perform it.

Initial inspected checker SHA256:
`1405c3535041aa0bb2b6cf9320c94e5bb822eecf4ea62bbb96801ce67512177b`.
Final reviewed checker SHA256:
`650f770cb3493a42c4f6291e5bbb053075688cf78623bf7af3cfc0f850a8e6e1`
(39,294 bytes). Author source note SHA256:
`a54133ac35dc4373843d7c6773d63ef775e520e08175a0de527ee37c0628030f`.
These hashes were computed as file-byte reads, without executing the source.

Public definitions inspected:

- PROTOCOL.md SHA256 `c5c2b18449650116d15effd8f070b663f9af2715a833cf73d91bc43f5cf87822`.
- SCHEMA.md SHA256 `8d4833b9bfbd7eb44596b7104b2c9343f34a1fecc1fa0c53ea9c2bcfc527a0e2`.

## Findings sent before freeze

1. **Scientific byte accounting.** The initial checker recursively summed every
   result file and tested only 256 MiB. This included supervisor logs, invocation
   locks, provenance bookkeeping and the review output, despite their explicit
   exclusion, and omitted the 255 MiB normal-science reserve rule. The author
   agreed to correct scientific-payload accounting and both limits. Unexpected
   scientific payloads must not disappear from accounting merely because a
   record does not reference them. **Resolved:** the reread source excludes only
   explicit supervisor/reviewer bookkeeping names and the current review output;
   it counts all other result payloads and checks both 255 and 256 MiB. Excluded
   supervisor names match run.py and run-review.py source declarations.

2. **Conditional solver gate.** The initial checker invoked the hyperbolic solver
   whenever independently computed admission/order permitted, including when
   preceding exact symbol, CSR-support or coefficient checks failed. The protocol
   makes root review conditional on passing geometry and an existing solve. The
   author agreed to gate this evaluation, retain mismatches and preserve a skip
   reason. An absent solution for an admitted eligible case must still fail.
   **Resolved:** all preceding per-case checks must pass; missing eligible
   solutions fail explicitly; skipped root review receives a reason.

3. **Bisection work at floating underflow.** The initial checker counted 56 times
   the number of nonempty positive-K rows for every map. Positive K does not imply
   a positive floating alpha when coefficient scaling or products underflow; the
   schema has no representability lower bound. The author agreed to count actual
   positive alpha separately for the direct map, every Picard map and residual
   maps. This is a source-level issue, not an observation about target inputs.
   **Resolved:** map_work counts the independently recomputed alpha > 0 for each
   map; Picard accumulates every update's work and residual work is separate.

4. **Fixed original-source identity.** Initial metadata validation accepted any
   relative source identity. The fixed-selection protocol supplies the exact
   identity for each n/time: outputs/milestone-31-source/checkpoint-heldout-2001-
   {n}-wide-wall-priority-0.0025-{t}.json. Recommended exact identity validation;
   metadata read confirms the selected index uses these strings. Original JSON
   bytes remain outside this review; validation of extraction/provenance relies
   on the frozen extractor, original hash metadata and publication checks.
   **Resolved:** source strings, byte counts and SHA256 metadata are compared to
   fixed pins. The four pins match the inspected original-source index metadata.

5. **Nonfinite diagnostics on rejected geometry (robustness caveat).** Even finite
   states can produce nonfinite rotation/norm intermediates for extreme invalid
   quaternions. JavaScript JSON serialization then emits null for those scalar
   diagnostics; the initial checker close comparison rejects nonfinite expected
   values. The schema did not specify serialization of these unavailable
   diagnostic scalars. Flagged prospectively for clarification; no selected
   input was evaluated to determine whether this occurs. **Open, nonblocking
   schema caveat:** strict checker behavior is unchanged; the author relayed the
   issue to the coordinator. A resulting failure must remain visible, with no
   target-driven reinterpretation or rerun.

## Mathematical and structural assessment

The source expresses the stated xyzw quaternion rotation without normalization,
the four historical rotor offsets in the prescribed order, and explicit nominal
total summation. Geometry branches preserve the reference ordering: center/self
handling, displacement/down guards, down exclusions, near-field classification,
radial support, projection and positive/zero/invalid terminal codes. Symbols are
compared over the full canonical tensor; a numerical boundary mismatch remains a
failure rather than an epsilon repair. Independently nested NumPy hypot and JS
Math.hypot can differ in rounding, as the protocol already acknowledges.

CSR partitions, byte lengths, dtype/shape declarations, source bounds, finite
positive K, row support and coefficient values are checked. Exact per-row source
comparison against independently increasing source IDs also detects duplicates
and ordering errors. The segmented-sum sentinel with empty-row masking handles
trailing and internal empty rows correctly by source inspection.

Unique dependencies are recovered from all four positive rotor rows. Height
violations and sorted-rank violations are separate. Lexicographic order uses
descending center z and ascending ID; eligibility is precisely zero rank
violations. Dependency roots have depth zero; dependent depth is one plus the
largest predecessor depth.

The cubic formula is algebraically correct for alpha > 0:
`x = 2 sqrt(alpha/3) sinh(asinh(3 sqrt(3)/(2 alpha^(3/2)))/3)`.
The small-z branch is the equivalent product
`alpha^-1 [sinh(t)/t] [asinh(z)/z]`, with both removable limits set to one.
The large-z branch uses a stable log expression for asinh and log-sinh without
forming alpha powers that would overflow. Alpha zero returns one. This is
mathematical source reasoning, not an empirical numerical error certificate.

The independent direct solve uses normalized nominal weights and positive roots.
The Picard audit checks saved initial ones, every synchronous update, first-stop
semantics, final generating rotors, separate residual maps, final residual log
norm and source/receiver mismatch. Returned source amplitudes and all four rotor
forces/roots are compared to the independent direct solution. Work records remain
consistency checks against the specified algorithm, not proof that an internal
loop ran a claimed number of times.

## Limits

No runtime, memory, target admission, convergence, boundary, output-size or
performance result follows from this static review. The checker still needs its
separately allocated, once-only saved-record invocation after source freeze and
remote manifest observation. The finite review does not establish physical
validity, coupled-flight validity, outward-rounded bounds, or independent-trial
statistical evidence. Shared historical poses remain airflow-off source states.

## Final disposition

No unresolved definite blocker found in the final inspected source. The three
definite defects and fixed-selection strengthening above are corrected. Maximum
observed relative errors are now retained in comparison records, and exception
messages redact the local package root. The remaining nonfinite-diagnostic
serialization issue is a prospective robustness/schema caveat, not a demonstrated
target defect or a reason to assume target success.

This disposition applies only to the exact final source hash above and means
ready for the coordinator's source-freeze process. It does not authorize a run or
claim any numerical result. No checker, candidate or target science was executed
in this review.
