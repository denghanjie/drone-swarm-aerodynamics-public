# Independent saved-data checker: source review

Prepared 2026-10-17, before the new analyzer/checker execution. This review
inspected source only. No target numerical input, reference, baseline, or
analysis-result file was opened; neither new module was imported or executed.
AST parsing of `source/check.py` succeeded. That is syntax evidence only.

## Interface and independence

`source/check.py` exports `run(root)` and returns a JSON-compatible report with
`passed`, immutable first failure, verified counts, per-state summaries, observed
file pins, fixed-fixture results and corruption-control results. It performs no
writes, repairs, retries, or reruns. The bounded runner owns exclusive output,
frozen-source/runtime verification, attempt identity and resource enforcement.

The checker imports only the Python standard library. It does not import the
analyzer or any simulator/reference arithmetic module. It independently decodes
binary64 center words through integer sign/exponent/significand arithmetic;
constructs split topology before preorder flattening; determines maximal
prefixes using cumulative totals; and selects tree groups with an explicit
left-first stack. Fractions remain exact throughout.

Source cross-checks established that reference `i` and `j` are stable drone IDs
(`semantic-reference.py`, pair construction), and that `inputSha256` is SHA-256
of canonical JSON `{domain: "m31-moving-admission/input/v1", id, input}`
(`moving-admission/source/check.py`, `input_hash` and `ENCODER`). It is not the
input file-byte digest. The checker separately records the observed file digest.

## Checks encoded

- Six named states in order, 256 receiver/rotor rows each, three fixed tiers,
  two trees per tier, and all 16,128 directed rotor/source reference pairs per
  state. No zero-positive row/state is dropped.
- Admitted references, canonical input-envelope binding, prepared center-word
  equality, certified baseline-r0 identity and exact baseline input binding.
- Complete unique stable-ID pair domain; only `zero` or `positive` statuses;
  zero has no coefficient; positive intervals are normalized rationals with
  `0 <= lower <= upper` and `upper > 0`. A zero lower endpoint remains positive.
- Exact T8/T2 reconstruction, T8 structural equality to saved baseline, and
  T2 nesting by member sets rather than full leaf-permutation equality.
- Exact tier/16 budgets; deterministic `(endpoint, stable ID)` ordering;
  maximal lower prefix and feasible upper prefix, including exact-budget ties.
- Left-first traversal, receiver exclusion, at least two positive sources per
  selected group, exact member upper masses, cumulative budget, stopped descent
  under accepted parents, exact fallback order, complete disjoint source
  partition, positive/member counts and node visits.
- Per-state summaries and integer ten-percent count hurdles; denominator zero
  remains visible and never passes a hurdle.

## Controls and failure behavior

Nineteen literal analytical fixtures execute before the first target-file read.
They cover normalized rationals, exact budgets and binary64 decoding, prefix
ties/maximality, zero lower bounds and zero-positive rows, preorder/tie behavior,
cumulative spending, two-positive minimum, nesting, and zero-denominator hurdles.
An analytical overspend mutant keeps its declared total within budget while its
actual selected groups exceed budget, exercising the cumulative group check.

After all six saved states validate, fourteen fresh in-memory corruptions of
verified saved records must fail in their registered core family. They cover
ceiling and feasible counts, prefix members, duplicate/self/missing sources,
upper-mass total, budget excess, visits, state identity, input binding, positive
denominator, T8 topology and a flipped hurdle. The mass and partition controls
remain applicable when no tree group is selected; the receiver's T8 leaf always
provides fallback sources. Controls do not alter saved files or use a generic
file-hash mismatch as their rejection witness.

The first failure stops processing and is retained in the report. A failing
control is a checker failure. No execution has yet established that fixtures,
saved records or corruptions pass their registered tests.

## Resource and scientific scope

Inputs are processed one triple at a time, retaining only the first normalized
context for later corruptions. JSON rejects duplicate keys and nonfinite
constants; each file read is capped at 16 MiB, without a cumulative input cap.
The runner's limits are 90 seconds wall, 60 seconds soft CPU, 512 MiB RLIMIT_DATA
(not total RSS), and 16 MiB output/file. This source review provides no measured
runtime or memory claim.

Saved reference coefficients are trusted evidence inputs; this audit checks
their stated interval shape and derived coefficient-mass calculations, not
their physical derivation. Observed hashes alone are not independent historical
authentication. Count hurdles do not establish an executable conservative
bound, a load-error guarantee, a runtime saving, or physical validity.
