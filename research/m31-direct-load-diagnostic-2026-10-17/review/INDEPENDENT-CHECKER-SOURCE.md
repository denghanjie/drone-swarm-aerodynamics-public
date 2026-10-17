# Independent direct-load checker: source-only handoff

Status: preparation only. No scientific allocation, target numerical inspection,
producer/checker import, fixture execution, proposal execution or rerun occurred.
This review read the proposal, prior source schemas, producer draft and prospective
configuration/runner source. AST parsing is the only executable source check.
The checker is at `check.py` in this isolated directory; it must be copied,
reviewed, frozen and bound by the separate public-source execution protocol.

## Interface and audit scope

`run(root, config=None, analysis_path=None)` returns a JSON-compatible report and
does not write results. Once copied to a package's `source/check.py`, its default
configuration is sibling `config.json`, and default saved producer output is
`package/results/analyze.json`. The outer runner owns the exclusive attempt,
source/runtime/publication verification, output writes and resource limits.
No producer or historical scientific module is imported.

The checker uses integer binary64 decoding; integer parsing of canonical native
hex candidates; Newton integer square roots and endpoint-square inclusion checks;
exact `Fraction` arithmetic; and a separately implemented native recipe replay.
Replay follows the prescribed once-rounded coefficient midpoint, input source
order, explicit binary64 left folds, all-ones start, 48 simultaneous updates and
54 cubic bisections. It verifies the saved candidate, not a new tuned proposal.
No baseline byte-equivalence claim is made.

All six states, two proposals per state and all 256 rows are compulsory. It
checks 96,768 nonself reference pair records, 3,072 candidate rotor values,
12 A audits, 12 B audits, six C audits, 4,608 certificate rows and 1,536 omission
diagnostic rows. Zero-status coefficients must be absent; positive intervals
may have zero lower endpoints. Rational wires must be normalized and source
coefficient endpoints must lie on the declared fixed192 grid.

Constants are fixed to mg `3fd0f3a14cec41dd` and R `3fa4462fb7ff5035`. During the
future check stage, the index bytes must match SHA-256
`3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393`, and the index
constant fields must match those exact words. Configuration explicitly fixes
both square-root and root-grid precision at 192. Input-envelope SHA-256, source
file pins, prepared center/force words and stable-ID domains are checked. Saved
reference roots must reproduce their saved signed load intervals exactly, but
the checker does not regenerate the physics oracle or its admission proof.

## Mathematical checks

The global mask contains exactly ceil(P/10) declared positive terms, sorted by
exact coefficient upper endpoint and then receiver ID, rotor and source ID.
No lower-positive filter, per-row budget or tree restriction is introduced.
The full control has zero deleted terms. P=0 stays visible and blocks any
nontrivial all-six continuation conclusion.

A computes each candidate-induced load using f*x, exact force-normalized source
weights, the supplied signed axis and cross(offset, axis) lever arms. For a
scalar reference box, minimum distance is zero when the point lies inside and
otherwise its distance to the near endpoint; maximum distance is the farther
endpoint distance. Vector errors use outward square roots of sums of squared
component minimum/maximum distances. These are bounds on the box distance even
when physical components are correlated; reference midpoints are never truth.
Worst lower/upper errors are maximized across every rotor/drone, without pooling.
Normalizations are mg/4, mg, mg and mg*R for the four declared categories.

B encloses the complete coefficient-times-y contraction at that exact candidate.
The checker derives p, k=max(1,pU,1/pL), global K, and the root corollary from
exact rational operations. It applies the prescribed outward fixed192 root
grid only after computing the exact raw corollary. Signed loads are propagated
from those emitted root boxes, not tighter pre-grid roots.

C uses the same candidate, y and mask. Retained terms keep both endpoints;
deleted contributions have lower zero and the full sum of aU*yU as upper.
The checker enforces C lower contraction <= B lower and equal upper, C root
and load boxes containing B, and C upper errors >= B. Equality is allowed:
C is not assumed to widen B strictly. B/C root hulls include the candidate,
so all their error lower bounds must be zero. A lower error cannot exceed a
B/C upper error, and an A definite failure cannot coexist with a proof pass
at the same tier.

The candidate loads, source-y values, every B/C contraction/defect/factor/root,
all four error intervals, category/overall tier classifications and all 256
coefficient/y-weighted omission diagnostics are compared with independently
reconstructed expected values. Zero-deletion rows cannot be hidden.

## Interpretation and controls

A has `pass`, `definite-fail` and `unresolved` outcomes. B/C have `pass` or
`not-certified`; a large upper bound is not evidence of actual error.
The checker applies the fixed global decision order: full-control strict A
adequacy first, then nonzero denominators, omitted stress definite failure,
omitted strict accuracy, B sufficiency, C sufficiency and finally strict
headroom for a separately registered practical experiment. One failed or
unresolved state prevents the corresponding all-six pass. Record validation
`passed` is separate from the scientific headroom decision.

Twenty-nine fixed literal fixtures precede the first target-file read. They
include exact arithmetic/decoding, root-grid inclusion, scalar and Euclidean
error bounds, signed load propagation, f*x versus squared ratios, mg/4 and mgR
normalization, ceil/tie mask selection, complete versus upper-only contraction,
global-K propagation from one bad row, the exact two-drone 7/4 coupled chain,
native replay of that chain with and without deletion, corrupted factor/root
rejection, control precedence, stress stopping and zero/unresolved denominators.

After all twelve saved proposals validate, thirteen fresh in-memory mutations
must reach their registered core mathematical failures: mask cardinality,
candidate identity, induced load identity, exact weighted y, A error interval,
A tier decision, B contraction/local/global factors/root grid, C contraction,
C's non-inaccuracy semantics and candidate-weighted omission mass. These do
not rely on a generic file-digest mismatch or modify saved evidence. The first
unexpected failure stops the checker without repair or retry.

## Resources and source review findings

Each read is capped at 16 MiB and rejects duplicate JSON keys and nonfinite
constants. States are processed sequentially; only the first normalized state
and independent expectations are retained for corruption controls. Checker
output contains compact summaries and observed input pins, not another full
copy of every certificate. The prospective outer limits are 120s soft/121s hard
CPU, 180s alarm, 16 MiB per output, and a 512 MiB observed post-output RSS gate.
None has been empirically exercised here; RSS acceptance is not an enforced
memory ceiling. No post-exposure precision or schedule extension is provided.

Runner source review recommended stronger prior-stage checks (schema, stage,
exit 0, null first failure, verified-pin count and output bytes) and publication
receipt fields/chronology in addition to its commit/manifest/output digests.
Parent reported these were being tightened before source freeze. That operational
review is distinct from this checker's numerical independence and does not
authorize execution. The isolated source remains subject to the parent's final
integrated-source review and public pin verification.

The resulting experiment can establish conditional exposed-state numerical
headroom or locate this proposal's accuracy/certificate obstacle. It cannot
establish physical validity, general impossibility, speed savings, scalability,
an online Q-current implementation, novelty or new holdout confirmation.
