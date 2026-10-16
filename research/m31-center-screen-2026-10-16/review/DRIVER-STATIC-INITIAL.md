# Independent static review of center-screen driver, supervisor and seal

2026-10-16. This reviewer authored the candidate kernel/controls, but did not author the driver, supervisor or metadata seal reviewed here. Review is source-only: no scientific source import/evaluation, controls, generator, solver, target read, timing or saved-data review occurred. No repository edits were made.

**Disposition: hold launch for the final-serialization cap correction below and completion of the explicitly pending freeze/reviewer checks.** The inspected driver schedule, runtime-before-import gate, candidate interface and raw-timing-before-validation order otherwise align with the prospective protocol. This is a static assessment, not qualification evidence.

## Finding requiring a prefreeze correction

**Final serialized size must be the size used by the resource qualifier.** In the inspected `source/run.py`, line 185 serializes `rec`, lines 186–192 then change elapsed time and potentially add final-limit flags, and line 193 reserializes it. The checks at lines 190–192 use the earlier payload length, while line 195 writes the later payload. Near a declared byte boundary, the record can therefore retain a successful qualifier even if the actual written payload exceeds the closure reserve or aggregate cap. In `source/seal.py`, lines 115–119 similarly test one payload and may enlarge it by adding failure facts before an unconditional write at line 121.

Use the final encoded bytes for both size checks. Set final status fields before producing the immutable payload; if a failure changes the record size, recompute and verify that final failure payload as well, or use a small predeclared failure representation that fits the reserved space. Keep truthful unqualified closure evidence when an observed child overshoot has already exhausted capacity, rather than calling the cap qualified. The correction must not change scientific inputs, limits or gates. Parent and driver author were informed immediately; this finding applies to the hashes below.

The final elapsed-time field should likewise be refreshed after administrative verification/serialization work that the qualifier intends to include. Neither source may claim a hard real-time write guarantee; the protocol already states the sampled/cooperative limitation.

## Pending launch prerequisites, not inferred completed

`source/review.py` and the final `source-manifest.json` were not present in the integrated package at this inspection. Consequently this review cannot yet confirm the reviewer's output schema against the new seal, its exact transient-evidence limitations, or the final dependency closure. Before launch, verify that the manifest includes the final driver/supervisor/seal, kernel/controls/lean anchor/helpers, independent reviewer/numeric reference, runtime/config/protocol and every imported simulation/scientific dependency. The supervisor's five critical-name subset at `run.py:93–94` is a minimum gate, not proof of that complete closure.

The seal expects `analysis.json` to have a strict Boolean `performanceRulePass`, `practicalRulePass:null`, and `requiresReviewSupervisorClosure:true`; the independent audit must have `pass:true` for qualification. Its publication receipt must use the exact `commit`, `manifestSha256`, `remoteManifestMatchesLocal` and `localAndCommittedPinsMatch` fields at `seal.py:69–71`. Confirm these interfaces before freeze; no existing output was consulted or repaired.

The supervisor requires current Git HEAD to equal the published source commit before each invocation (`run.py:91`). Keep that condition satisfied through candidate and review launches; independent verification receipts may be saved without advancing HEAD until this restriction is no longer needed. This is a workflow condition of the inspected supervisor, not an instruction to alter the fixed source after publication.

## Confirmed static paths

**Runtime before scientific imports.** `experiment.cjs:67–73` checks argument shape, little-endian runtime, absence of Node flags/options, resolved executable bytes/hash/version, platform/architecture and fixed schedule counts before importing kernel, simulation and controls. Its earlier imports are Node built-ins. `run.py:104–123` checks its Python executable/full version/platform, optimization/options, NumPy distribution RECORD/version metadata and the child executable before launching it. NumPy RECORD identity is metadata identity, not a hash of every installed package file; the subsequent reviewer should retain that precise scope. No package was imported in this review.

**Source/process closure.** The supervisor consumes an exclusive invocation lock before checks, verifies manifest/local/published source bytes, and checks pins again after closure. It waits/reaps the child and probes process-group absence, retaining cleanup signals, monitor errors and exit races. A prelaunch failure can be marked closed but cannot pass because `returncode` is not zero. Review launch requires candidate terminal closure. Candidate output hashes are protected across the review. Actual success requires positive RSS samples and no errors/signals, as well as immutable protected inputs. The code does not silently turn an exit race into an RSS observation.

**Controls and ownership.** `experiment.cjs:75–89` checks the full configured/exported ID sequence and processes all 48 source-defined controls, applying patches after fresh default state construction. Input bytes/tokens are retained; the same control states feed L and F. Full builds and omission checks are performed even for model-invalid controls. Ordered solves/residuals are conditional on equal admitted descending-eligible output, with explicit no-solve reason otherwise. Input mutation is checked after each performed build/solve. `experiment.cjs:90–96` fixes all six extra ownership builds, retains planes-66 L/F records, and checks typed buffers, ordinary arrays and new screen arrays for cross-call aliasing/nonmutation. The inherited `q.states` input reference is not misrepresented as independent storage. Conditional control solves are counted separately from fresh qualification solves.

**Fresh-state and timing schedule.** The integrated config contains the three stated seeds/cases. `experiment.cjs:98–107` retains initial/final state arrays, all expected frames and generation metadata, and rejects incomplete generation without replacement. The nested case/method loop at lines 109–125 creates six fresh builds and six solves/residuals. Both classification tensors persist before complete L/F comparison/omission auditing; they are released before timing. Lines 126–128 produce the declared six warmups and 36 measured calls, rotating case traversal and alternating paired LF/FL order, and assert the final total of 42. No runtime outcome of those loops has been evaluated.

**Exact versus intended differences.** Cross-method comparisons include full symbols, CSR bytes, Object.is K/a, prepared geometry bytes, current nominal/source totals, input/admission, dependencies/graph, certificate, symbol census, ordinary bound, ordinary assembly and complete solutions/residuals. Only the two intended geometry work fields are removed from the model-geometry comparison. Screen metadata is checked independently and then compared exactly against its own method's qualification on each timing call. The qualification-versus-timing `commonSymbolBytes` distinction is separately checked against whether a tensor was requested. New counters do not claim fewer logical pairs or portable certification.

**Raw evidence and failure preservation.** `recordTiming` writes raw returned metadata at line 59 before comparison, hash or input validation; a thrown query attempts a separate raw failure record at line 57. Validated records are written before mismatch assertion and an attempted failure bundle. Fresh qualification bundles are written before comparison assertions; domain rejection persists its build. Completed control/generation/qualification records remain append-only. The catch path retains progress and partial evidence with the emergency budget and separately catches failure-write errors. An abrupt process termination can still interrupt an in-progress artifact; the supervisor's terminal status/pins must remain the authority for whether the invocation completed. The schema correctly discloses that transient timed arrays are compared in-process rather than all persisted.

**Resource and final Boolean gates.** Candidate writes use exclusive files and separate normal/emergency limits; compressed symbols have their own cap. The supervisor observes external wall/RSS/log/directory caps and holds a closure reserve. The seal is a separate exclusive metadata-only operation and does not reanalyse targets/timings. It verifies source identity, publication receipt, both terminal supervisor identities and artifact pins, then combines closure gates, independent audit pass and the saved internal performance Boolean. It cannot qualify an open review merely because the child audit passed. `sealSuccess` means the administrative result was produced; it must not be confused with `evidenceQualified` or `practicalRulePass`. The final-serialization defect above must be corrected before relying on its cap qualification.

## Inspected sources and identities

Content read: package `PROTOCOL.md`, `config.json`, `runtime.json`, `SCHEMA.md`, `source/experiment.cjs`, `source/run.py`, `source/seal.py`. The integrated kernel/lean-anchor/controls hashes were checked against the previously authored source interface. Filename discovery and an attempted read of the not-yet-present reviewer added no content source. No source-manifest or result data was read.

| File | SHA256 at review |
|---|---|
| `source/experiment.cjs` | `7bc39548f93a486007723e4cf257a7e2e6c7dcc983f6f503f3015329d128d4a3` |
| `source/run.py` | `30d1fd9e6fce93b67f3bfa5b25ab861f2f9f12977ba88292c577c82238c9f5de` |
| `source/seal.py` | `53a8095b9efdd67ee79cc27fea0508f992966d9b1d872df56d5dedba6bdf4579` |
| `config.json` | `a09cec7cbb51cba9132df1748fe61a2d91f5297ddd47eb46234bae094204195b` |
| `runtime.json` | `d36f55e4f8ff26e5e63c0c01008a6a82d4bcb69c27aea8254f21caa690be359c` |
| `source/kernel.cjs` | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| `source/lean-anchor.cjs` | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| `source/controls.cjs` | `bf54381ee7f4dab8fbb19e48ada7e11c0f6d129cec1bcd21e5ce5075fc91f1ba` |

All paths above are relative to `research/m31-center-screen-2026-10-16/`. Any subsequent source correction needs its own static delta review and final pins. No launch authorization is supplied by this note.
