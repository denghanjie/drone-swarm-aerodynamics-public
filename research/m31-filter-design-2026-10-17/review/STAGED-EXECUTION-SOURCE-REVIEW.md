# Independent staged-execution source review

Reviewer: `m31_evidence_audit`. Date: 2026-10-17. Status: completed prefreeze source review; findings F1 and F2 resolved prospectively. Text inspection and JSON structure checks only. No scientific imports, numerical runs, checker controls, or suite execution were performed. The inherited original-file reading count remains 10 of 12; all files read in this continuation belong to the new package, including a separately disclosed local copy of an inherited reference helper.

## Runner and representation binding

At runner SHA-256 `2ce652e43efda4f698ef456e5229e608e9cee26da8a646dc686b1601bbee4536`, each pair is admitted by the unchanged adapter. The exact and fast receiver/source objects are then constructed in the same local scope from the same admitted prepared words. The exact baseline and candidate call receive the same rotor. Preparation rejection bypasses the filter and retains the original rejection branch. This satisfies the internal trusted-wrapper correspondence precondition identified in the numerical audit.

`Q.constants(A.constantBits)` fails closed if a constant word is nonfinite: finite singleton decoding raises before records are produced, leaving a partial journal that cannot qualify as a complete kernel run. This is distinct from proving the constant map is correct. The independent checker must reconstruct the entire constant map and preparation graph, and the manifest must bind their inherited source dependencies.

The primitive runner distinguishes adjacent-value word results (which can be infinity sentinels at finite extrema) from interval operations (which refuse nonfinite widened endpoints). The independent primitive oracle must use the same declared distinction and not accept arbitrary nonfinite interval endpoints.

Every admitted pair first runs the baseline exact query. A candidate fallback runs that exact query again. This is appropriate correctness evidence but prevents interpreting verification elapsed time as filtered total-cost performance. Timing here is resource telemetry only.

The runner fsyncs journal events and emits a terminal count before it writes the final result document. Therefore journal completion alone cannot qualify the kernel. Normal exit, the complete result document, exact journal structure/counts, and independent semantic validation are all needed. The supervisor checks process success and both files; the checker must check their content.

## Supervision and guardian

Initial reviewed supervisor SHA-256: `751d16ffb2c893dca2da01cc8ade35a8b31cd7324e3177f33b41c9cb2fcb5520`. Guardian SHA-256: `b3d6be72fccd56be18d7cd2b59e0ff87aac0442eebf8470c8b7308eb853732de`.

The source contains single-use stage markers, an empty-results requirement for kernel launch, pre/post source and runtime identity checks, retained private raw logs, and immutable kernel evidence pins checked again before and after checker execution. The checker uses the same private-log directory identity. Existing stage artifacts prevent automatic retry.

The guardian is a retained process-group leader. It records child exit and waits for the supervisor to verify that the scientific child is absent before releasing the group. Supervisor signal handling is conditioned on the owned guardian still being alive. The guardian also terminates a live child on supervisor disconnection or its own deadline. These mechanisms fit the explicitly limited scope of reviewed scientific children that spawn no subprocesses. They are not hostile-code or escaped-descendant isolation.

Output accounting recursively inspects the results directory against a closed filename set, rejects unexpected directories and symlinks, includes both stages' private raw logs and public copies, applies separate document/journal/checker/log/report limits, and checks the aggregate budget. It requires both kernel scientific files and both checker outputs to exist for their respective stages. Finite sampling cannot guarantee the absence of all instantaneous RSS/output spikes; reports must retain observed sample gaps and describe sampled RSS honestly.

The intended limits in this source are 300 seconds per supervised stage, 310 seconds per guardian, 512 MiB sampled group RSS, and 96 MiB aggregate retained output. Scientific computation begins in the timed child; preflight file hashing is metadata work. Finalization and postrun identity work are included in the reported wall duration and can cause a stage to fail its wall limit even after the child exits.

## Finding before source freeze

**F1 — explicitly require inherited import dependencies in the manifest.** The initial supervisor required list enumerates new-package files, while the runner imports inherited adapter, rational, and pair-query modules, which in turn depend on inherited interval code and inherited `spec.json`. Checking all manifest entries does not establish that every imported dependency was included. Require the explicit inherited dependency paths, plus any additional checker dependencies, before accepting the manifest. This finding was sent to the parent and supervisor author. Resolution is pending review of the amended source.

**F1 runner-closure resolution.** The author preserved the original source in `prefreeze/supervise-before-external-pin-review.py` and added a required list for inherited `adapter.cjs`, `rational.cjs`, `pair-prepared.cjs`, `interval.cjs`, and `spec.json`. The reviewer inspected this exact diff. Supervisor SHA-256 `fbfee616177a8079d5c5dd7e8d321db1c7c7d51f5df7bbfca1b453660f5c72b7` resolves the runner dependency omission; checker-specific external dependencies remain to be confirmed when its source arrives.

**F1 checker-closure amendment.** The checker author declared only the new local `source/semantic-reference.py` plus standard-library imports. The supervisor now requires that helper too; the reviewer inspected the preserved-before/current diff. Supervisor SHA-256 `a09af9c14853fc1440440e25c443163594bafed7f6257b8194ae3fb8208cdf7d` contains both required closures. Final checker inspection must confirm this declared import boundary.

Kernel supervision success means a complete execution under resource/identity checks; it is not by itself scientific qualification. Final qualification must additionally require a successful independent checker report, exact record/journal/control counts, and no semantic errors. Protocol, spec, result contract, and checker were not yet present at this initial pass and remain to be reviewed.

## Design-stage semantics

The reviewed design/direction documents distinguish correctness verification from a future matched total-cost experiment and subsequent moving-swarm integration. They explicitly avoid deriving speed from hit counts or novelty from the use of filtering. No new performance evidence is claimed. Current document hashes at reading:

- `DESIGN-DRAFT.md`: `a79ed283e1486cb7f3f63573ed9d8d145428ad8ffd6b2725d91cdd4ffcfcb36f`.
- `RESEARCH-DIRECTION.md`: `1925e978d0290191181ce51e7d48500ea822c92f0d491cbe999a638b47332b4e`.
- `PREFREEZE-CHANGES.md`: `ca368eca9d3176858a271519f6233a7ce207ea036db3f41ae7acc167fd5e5a51`.

## Protocol and fixture structure continuation

The first received `PROTOCOL.md` agrees with the reviewed scope: 108 records, 110 journal events, 16 corruption controls (superseding the earlier 15-control planning count), one kernel and one saved checker, no timing claim, and no pre-gate numerical imports or runs. It correctly separates kernel execution success from independent scientific qualification, preserves incomplete evidence on failure, and requires targeted semantic detection before generic equality or digest rejection can count as a control success.

The reviewer parsed `spec.json` as JSON data and inspected fixture identities and hexadecimal strings without decoding words or evaluating model arithmetic. Structural inspection found 108 unique record IDs: 72 primitive rows and 36 pair rows. Primitive counts are 16 nextUp, 16 nextDown, and eight each add/subtract/multiply/divide/square. Every pair contains two arrays of 17 lowercase 16-hex-digit words and an integer rotor from 0 through 3. These fields agree with runner dispatch and fixture validation. The 108 record events plus header and completion imply the protocol's 110 events. These are syntax/allocation checks, not numerical outcomes.

**F2 — unresolved witness coverage must be explicit before freeze.** The protocol promises unchanged unresolved-tail coverage, but the first 36-pair specification has no explicitly identified unresolved-tail fixture; `tail-cap` appears intended as cap rejection. This was raised with the parent and protocol author before execution. An active geometry with max-finite positive source forces can analytically force the unchanged fixed96 normalizer input outside its range; alternatively sufficiently small positive receiver force can make the fixed96 normalizer lower endpoint zero. These are prospective construction suggestions, not executed results. Do not infer an unresolved witness from its case name or silently reduce the protocol's promised coverage after a run. Resolution is pending the final contract/spec.

**F2 resolved prospectively by an explicit gate definition.** The machine contract states that every fixed96 unresolved status and every fixed192 reference-undecidable outcome fails qualification, without stress exceptions or substitution. The parent corrected the protocol before execution: there is no required unresolved witness and no empirical unresolved-tail coverage claim. The reviewer inspected the corrected wording. No suggested fixture was added or evaluated. Preservation of an exact fallback's unresolved output remains a conditional source property of the unchanged callback; it is not a passing empirical outcome of this finite qualification set.

## Final independent-checker review

The complete initial checker source and the subsequent descriptive-count diff were reviewed. Final checker SHA-256: `1d9f1181d55b4ed5ca76688ad4de29baedec1e008d7eac04806c28c10fc2784e`. The change from the preserved initial checker adds primitive outcome/refusal counts and oracle/fallback branch counts; it does not relax a semantic gate.

The checker dynamically compiles only the hash-checked local reference helper into a named module after manifest verification. That module name prevents its old `__main__` allocation from running. The new checker calls only the helper's exact constant/preparation/oracle and rational/encoding utilities. Its old 322-row regeneration, validation, stress exceptions, controls, and main are uncalled. The new checker imports no candidate module and starts no subprocess.

Independent primitive references use integer adjacency and exact rational arithmetic on entire input intervals. They distinguish a valid infinity sentinel returned by nextUp/nextDown at a finite extreme from a prohibited nonfinite arithmetic endpoint. Invalid intervals, nonfinite inputs, and zero-enclosing denominators require their specified refusal. Otherwise a conservative arithmetic refusal is allowed; finite enclosure coverage and fixed control witnesses prevent an all-refusal pass.

For pairs, the checker reconstructs the full raw/prepared binding from the frozen declaration and independently reconstructs the constant table. Preparation rejection, its retained prepared object, and the candidate's preparation decision must match. Baseline and candidate each independently satisfy exact status/branch checks and all applicable positive-interval checks before their full structural equality is required. Each of the five positive fixed96 intervals must enclose its fixed192 reference, with nonnegative bounds, both caps certified, and a strictly positive normalizer lower bound. Every fixed96 unresolved and fixed192 reference-undecidable result fails the new gate.

The checker validates source/spec identities, compact JSON representation, duplicate keys, integer/string constraints, exact ordered allocation, full journal row agreement, and exactly 110 events. Required source closure includes all eleven local files and all five inherited runner dependencies. It rechecks the source/manifest, kernel document/journal, and running Python binary before writing its two outputs. Output writing is exclusive, bounded, and fsynced. The report's final `passed` and zero exit require the semantic/journal checks, all sixteen controls, and unchanged identities. The supervisor then requires normal exit, both checker evidence files, successful lifecycle closure, and its own identity/resource checks.

All sixteen fixed mutation recipes were traced statically:

| Family | Controls and required semantic detection |
| --- | --- |
| Primitive containment/domain, six | Inward upper/lower addition bounds; lost positive underflow; finite interval for an overflowing product; zero-enclosing divisor accepted as an interval; lost zero in a crossing square interval. Each requires exact target evidence and its containment/domain code. |
| Pair semantics/binding, six | False zero on the positive witness; zero hiding the center guard; wrong zero branch; altered prepared rotor point; lost positive fallback coefficient; invalid preparation bypass. Independent target/status/branch/preparation/interval checks precede generic baseline equality. |
| Record/journal integrity, four | Missing row, duplicate ID, reordered rows, and a journal-only row mutation. The journal control requires the unmodified document validator to pass first. |

The mandatory `tail-positive` fallback witness is enforced by the pair control prerequisites as well as the general positive-fallback coverage check. A missing intended witness or absent intended error code fails the control gate. Control recipes reuse one precomputed independent reference set and never replay the candidate. No control was actually executed in this review.

On failed documents, descriptive counters count successfully validated rows and can therefore be partial. They must not be reported as complete case coverage unless qualification succeeds. On a qualified document they describe only the fixed tested records, not probabilities or performance.

## Final disposition and reviewed identities

No unresolved blocking source-review finding remains at the identities below. This is permission-neutral source-review evidence, not a numerical result: publication/source freeze, the one authorized kernel/checker allocations, and saved-evidence auditing remain separate gates. The scientific validity claims remain conditional on the numerical audit assumptions and the inherited reference trust boundary.

| Artifact | Reviewed SHA-256 |
| --- | --- |
| `source/run.cjs` | `2ce652e43efda4f698ef456e5229e608e9cee26da8a646dc686b1601bbee4536` |
| `source/check.py` | `1d9f1181d55b4ed5ca76688ad4de29baedec1e008d7eac04806c28c10fc2784e` |
| `source/supervise.py` | `a09af9c14853fc1440440e25c443163594bafed7f6257b8194ae3fb8208cdf7d` |
| `source/guardian.py` | `b3d6be72fccd56be18d7cd2b59e0ff87aac0442eebf8470c8b7308eb853732de` |
| `source/spec.json` | `2715ab48ad1c6437244e78ea66c8685c074d579c961f5b4c47857534e2e8de55` |
| `source/result-contract.json` | `4b9890937fac0131830548dc73241296b2c57783b1883a6762961c3dc45ca5ac` |
| `source/semantic-reference.py` | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `PROTOCOL.md` | `4e0af980a7be0295cac06550e851d5282a44f5d494e81c9dfc632582ea810bb0` |

`STAGED-EXECUTION-READING.json` records the new-package continuation reads and mechanical checks. Neither the numerical candidate nor checker was imported or executed. The old closed package was not edited or rerun.
