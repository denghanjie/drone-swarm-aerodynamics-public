# Center-screen driver and supervisor handoff

Source preparation only, 2026-10-16. These files were authored outside the public
repository. The Node parser and Python `compile(..., 'exec')` accepted the files;
the scientific modules, controls, generator, queries and checker were not
imported or executed. No target, test, timing, fit or score was produced.

Copy `experiment.cjs` and `run.py` into the package's `source/` directory before
the source/checker freeze. Do not execute this temporary copy: its relative
dependencies deliberately refer to the eventual package layout. Parent owns
integration, complete dependency pins, independent static review, publication,
independent remote-byte verification and the subsequent serial allocation.

## Required frozen interfaces

- `kernel.cjs`: `build(states, 'lean'|'screen', fullSymbols, guard)` and
  `query(states, 'L'|'F', guard)`; unchanged solver, schedule, residual, checksum,
  graph and constants exports. L delegates the byte-pinned lean anchor.
- `controls.cjs`: `controls()`, literal `controlIds`, and `ownershipSequence`.
  Each definition has `id`, `positions`, `expectedScreenEligible`,
  `expectedFallbackReason` and optional `statePatches` (`vehicle,index,value`).
  The original default 17-state construction is followed by these patches.
  Original positional literals are not modified.
- Config: `controls:48`, literal `controlIds` in exact source order,
  `ownershipExtraBuilds:6`, exact `ownershipSequence` below,
  `controlSolvePolicy:'untimed solve+residual iff admitted and descendingEligible; otherwise explicit no-solve reason'`, qualification builds/solves
  6, warmups 6, measured calls 36, total calls 42. Unresolved placeholders stop
  the driver before scientific imports.
- Runtime identity comes from pinned `runtime.json`: `node` and `python` each
  have `version,bytes,sha256`; Python version is complete `sys.version`.
  `numpy` has `version,distributionRecordSha256`; the latter hashes UTF-8
  distribution RECORD text. Platform is darwin; architecture is arm64.

The driver checks Node binary bytes/hash/version, platform, flags and frozen
counts before any kernel/simulation/control import. The supervisor also checks
its resolved Python binary/full version, NumPy distribution metadata without a
NumPy import, the selected child binary and Node version before child launch.
NODE_OPTIONS and Node execution flags are forbidden; Python optimization is 0.

## Exact control and ownership schedule

48 control IDs, in order:

```text
radius-0-below, radius-0-exact, radius-0-above,
radius--6-below, radius--6-exact, radius--6-above,
cell-below, cell-exact, cell-above, signed-zero, coarse-origin, coarse-translated,
dense-16, span-256, span-nextUp256, far-invalid258, nonfinite-nan,
nonfinite-infinity, overflow-span, near-field, duplicates,
planes-62, planes-64, planes-66,
component-x-below, component-x-exact, component-x-above,
component-y-below, component-y-exact, component-y-above,
component-z-below, component-z-exact, component-z-above,
span-diagonal-256, span-nextDown256, center-257-fallback,
center-nextUp257-fallback, mixed-near-far, mixed-positive-far,
invalid-quaternion-far, nominal-zero-positive-far,
nominal-negative-positive-far, nominal-nan-positive-far, scaled-cap-positive-far,
invalid-quaternion-nan-far, nominal-infinity-positive-far,
nominal-total-overflow-positive-far, nominal-unequal-positive-far
```

Both complete builds are saved for every control, including invalid controls.
Both untimed ordered solves/residuals occur only after equal model outputs,
admitted input and descending-eligible graph. Otherwise `noSolveReason` is
`model-mismatch`, `admission` or `ordering`, with null solutions. These control
solves are separate from the six fresh qualification solves. The final evidence
reports `actualControlSolves`; no outcomes have yet been evaluated.

Retain planes-66 L/F bundles while performing six additional fresh builds in
order: `L:sparse2,F:sparse2,L:planes62,F:planes62,L:fallback258,F:fallback258`.
The sparse pair has separation 4; fallback258 has separation 258. These are
source-defined controls, not data-selected replacements. Check dedicated typed
buffers, cross-call non-aliasing, nominal/dependency/source-total arrays, and
the new screen min/max/span arrays. Retained before/after literals are deep
copies. The inherited `q.states` input reference is intentionally not described
as independently owned returned storage.

## Numeric representation and exact comparisons

All JSON writes recursively preserve special numeric atoms as strings: `-0`,
`NaN`, `Infinity`, `-Infinity`. Finite ordinary numbers remain JSON numbers.
All entries in `stateTokens`, `inputBeforeTokens` and `positionTokens` are
numeric strings, including signed zero. Patched values are token strings too.
The checker must decode only known numeric fields. Binary `.f64` inputs and
matrix arrays preserve binary64 bytes; controls are never reconstructed from
JSON null substitutes.

Cross-method equality compares every symbol byte, CSR offset/source byte,
K/a value with Object.is, prepared geometry byte, current nominal/source total,
input/admission field, complete graph/dependencies, ordinary bound, symbol
census, original certificate, assembly metadata and complete solution/residual
objects. Hashes supplement these comparisons; equality never rests on hashes
alone. Only `screen`, timing phases and the two intentional geometry counters
(`directedCenterTests`, `certifiedSkippedPairs`) are excluded across methods.
Within each timed method, all screen fields and all geometry counters must
equal that method's own qualified output. `assemblyStats.commonSymbolBytes`
is independently checked against actual qualification/timing tensor policy;
other assembly metadata must match.

L's saved `screen` is null. F's full screen object includes finite/runtime
scope flags, limits, coordinate/span finiteness, min/max/spans, eligibility,
fallback/reason, ordered visits, component tests, skipped/actual norm counts,
and its omission-evidence statement. Historical skipped-pair wording is not
a portable arithmetic proof. `screenPreflight` is present only on fallback F;
L and eligible F omit that phase. No zero phase is invented for the anchor.

For each control and fresh state, `omissionAudit` enumerates every ordered
nonself pair from current positions. On eligible F scenes, each componentwise
omission must have all four L and F symbol bytes exactly 1. It records eligible,
orderedPairs, omittedPairs, checkedRotorSymbols, exactOutsideSymbols,
firstMismatch, screenCounts and pass. Both fresh tensors remain available
through this audit and complete element equality, then are released before
timing. The independent reviewer must reconstruct the predicate/counters and
inspect every inferred omission against saved tensors independently.

## Artifacts

Generation is the unchanged typed-assembly generation block, using this
checkpoint's three fixed seeds and input cases. No airflow is active. Save
initial/final 17-state arrays and 21 pose frames with exact terminal comparison.

- `inputs/index.json`: kind, shape, dtype and three case records with pins;
  `inputs/{id}.f64`: complete final states.
- `generation/{id}.json`: generator output/config/metrics and frame/input pins;
  initial `.f64`, per-frame `.f64` and concatenated `-poses.f64`.
- `results/control-{id}.json`: L/F literal model bundles, full state tokens,
  before tokens, patches/expectations, input hashes/unchanged flag, per-build and
  per-solve mutationChecks (null for unperformed solves), omission
  audit, comparisons and nullable L/F solutions.
- `results/ownership.json`: sequence, all six extra builds, before/after input
  tokens/hashes, retained deep-copied L/F literals, storage and mutation flags.
- `results/{id}-{L|F}.json`: full qualified metadata, screen, binary artifact
  pins, `solutions:{O:...}`, matrix/solution hashes. Separate compressed U8
  symbol tensor and uncompressed CSR offsets/sources/K/a binaries. Symbol
  tensor layout is `(receiver*N+source)*4+rotor`; raw length is `4*N*N`.
- `results/qualification-{id}-{L|F}.json`: saved bundle pin, compute/persistence
  times, exact comparison, input before/after hashes and pass. Only F has an
  omissionAudit; L has null.
- `results/call-NNN-raw.json`: raw returned call metadata is written before
  validation. Contains sequence, id/method/block/warmup, total/phases, checksum,
  screen/geometry/certificate/assembly metadata, solver work and residuals.
  A thrown query still records its attempt and observed elapsed time where
  the failure-reserve write succeeds; it is not a complete timed query.
- `results/call-NNN.json`: raw pin and subsequent complete validation, including
  input before/after hashes, inputUnchanged, full array comparisons, own-method
  metadata comparisons, hashes and finiteTiming. On mismatch the raw/validated
  evidence remains, a failure bundle is attempted, and the allocation stops.
- `results/evidence.json`: only after complete correctness schedule; contains
  controls, ownership pin, generation/qualification/timing records, start/end
  environment and sampled memory. On failure, `failure.json` and
  `partial-evidence.json` are attempted with the separate 8 MiB reserve.

Timed transient arrays are compared in the candidate process; they are not all
persisted. The independent reviewer can audit the saved metadata/hash agreement
and qualified arrays, but must disclose that transient-array limitation.

## Timing and downstream summary

Warmup: config case order, L then F for each case (six calls). Measured:
blocks 0..5, traversal j=0..2, case index c=(j+block)%3, order
`['LF','FL'][(block+c)%2]`. This yields 36 measured and 42 total complete
calls. Each query's internal timer includes current preparation, F predicate,
construction/scaling, schedule, solve, residual and output consumption.
Qualification, persistence and subsequent validation are outside that timer.

The independent saved-only reviewer owns paired ratios/differences,
median/min/max summaries, per-case practical gates and the final summary.
Driver completion is a correctness-schedule status, not a performance pass.
Both required N=5000 cases must meet the unchanged practical gates after all
correctness, resource and audit requirements; N=1000 remains contextual.

## Supervisor records and caps

Invocation: `python run.py candidate|review EXECUTABLE MANIFEST_SHA COMMIT`.
An exclusive invocation lock is created before source/runtime checks. Checks
compare the manifest and every listed file against local bytes and the exact
published commit; after child closure all source pins are checked again.
The supervisor does not itself establish independent remote verification;
that remains a separate required prelaunch parent check.

Records `candidate-run.json` / `review-run.json` use camelCase:
`sourceCommit,sourceManifestSha256,kind,startedUTC,wallCapSeconds,rssCapBytes,
sampledPeakRSSBytes,rssSamples,sampleIntervalSeconds,monitorErrors,exitRaces,
signals,returncode,closed,childGroupAbsent,runtimeIdentityVerified,runtime,
protectedInputsUnchanged,candidateOutputsUnchanged,scientificBytesBeforeClosure,
logBytes,artifacts,elapsedSeconds,supervisorSuccess,closureReserveBytes`.
Conditional exception/cleanup/finalization/cap fields preserve failure facts.
Review records also state candidateSupervisorSuccess. A failed candidate can
be inspected after actual closure; performance qualification still requires
successful candidate and review supervision and a successful independent audit.

Wait/reap the child, probe its actual process group, kill any residual group,
then observe absence. Signals, live-group cleanup, monitor errors, zero RSS
samples or source/output mutation prevent supervisor success. `closed` is true
for a launched child only after returncode and observed group absence. Exitraces
are explicit; a race is not silently converted into a positive RSS sample.

Caps remain 900/180 s external, 895/175 s cooperative, sampled RSS 1.5 GiB,
candidate normal writes 184 MiB plus 8 MiB failure reserve, scientific directory
208 MiB, aggregate logs 4 MiB, each compressed symbol artifact 64 MiB. A 1 MiB
supervisor closure reserve is held inside the 208 MiB aggregate cap. Final size
checks include every results/input/generation artifact after the child exits,
including review/analysis files, plus the prospective closure record. Sampling
and cooperative checks may overshoot; they are not hard real-time guarantees.
No cap increase, retry, replacement input or post-result control edit is allowed.


Timing summary accounting: if an F case falls back, summary-only absent phases are represented by zero for summation. In particular an L screenPreflight zero is not an observed preflight duration. Raw records retain method-specific actual phase keys; totals and paired gates are unchanged.
