# Source-only supervision adaptation

Author: `m31_verified_literature`. Date: 2026-10-17. The parent authorized implementation after accepting the prospective storage/budget choices, subject to the separate final mathematical proof. This note records the implementation and source checks; it is not independent acceptance or permission to execute science.

## Files and preserved lineage

- `source/supervise.py`: recursive output accounting, new file layout and complete prior-stage scientific evidence pins.
- `source/guardian.py`: inherited retained-session behavior, with both stage deadlines changed to 1,810 seconds.
- `prefreeze/inherited-supervision/supervise.py` and `guardian.py`: byte-identical copies of the previous package's originals. The originals and the preserved initial spec-count typo were not modified.

The preserved supervisor is 12,881 bytes, SHA-256 `ec49c30922908dd9733687fc4a0a1c09c5acd76fa599f4bbb9f031b5d4c8aaba`. The preserved guardian is 1,746 bytes, SHA-256 `c82b1189a966c04ddf602a99dddda1fe24cf8afaf0ec037ba6e2d476f1541755`.

## Frozen interface for parent/contract review

The outer manifest remains `PACKAGE/source-manifest.json`, with `files` entries `{path, bytes, sha256}` using repository-relative paths. The supervisor checks every frozen file and runtime before launch and after finalization, and binds the manifest's exact raw bytes to the publication receipt. The required-source set now includes `canonical.cjs` and, as confirmed with the checker author, `semantic-reference.py` alongside `check.py` and `pair-reference.py`. Candidate `contract.sourceFiles` remains the candidate source identity projection; independent helpers and supervision are pinned by the complete outer manifest.

The kernel receives `RESEARCH_RESULT_PATH=PACKAGE/results/timing-index.json` and `RESEARCH_SOURCE_MANIFEST_PATH=PACKAGE/source-manifest.json`. Checker arguments remain `--spec PACKAGE/source/spec.json --input PACKAGE/results/timing-index.json --manifest PACKAGE/source-manifest.json --output PACKAGE/results/independent-check.json --root REPOSITORY_ROOT`.

The exact scene filename set comes from the six unique validated frozen scene IDs. Permitted scientific files are `scenes/<sceneId>.json`; the only optional mismatch file is `anomalies/first-mismatch.json`. Checker reference paths are `reference-scenes/<sceneId>.json`. Files are written directly at declared paths; undeclared temporary files/subdirectories fail accounting. A future need for temporary filenames must be incorporated into the frozen contract and supervisor before execution.

## Limits and accounting

Both supervisor stage ceilings are 1,800 seconds; both guardian deadlines are 1,810 seconds. Sampled guardian-plus-child RSS is limited to 1 GiB. The inherited nominal 0.05-second sampling sleep, maximum observed sample-gap report, descendant checks, retained process-group ownership, release handshake and cleanup/fail-closed reporting remain.

The results tree is scanned recursively. It admits only the three declared subdirectories, known scientific/reference filenames, and fixed attempt/guardian/log/report/terminal-error names. Unexpected regular files still contribute to aggregate/unclassified byte counts and cause rejection; unexpected directories, symlinks or other file types also cause rejection. No unrecognized nested scientific file can silently escape accounting.

- Timing index: 8 MiB; timing journal: 8 MiB.
- Each scientific/anomaly shard: 64 MiB; all six scene shards plus the optional anomaly together: 128 MiB.
- Checker main output plus all six reference shards together: 96 MiB.
- Both stages' private stdout/stderr raw logs, all public log copies and fixed attempt/guardian/terminal-error metadata together: 16 MiB.
- Each supervision report: 64 KiB; aggregate retained outputs: 384 MiB.

The report saves category totals and all recognized relative output names/sizes, with a final report-size reserve checked against aggregate accounting. Failure leaves the journal, partial shards, raw logs and allowed anomaly in place; the supervisor does not delete or truncate scientific evidence to fit a limit. Sampled enforcement may observe an already-exceeded limit; it is not a claim of instantaneous host/filesystem containment.

To keep cross-stage private-log accounting meaningful, kernel supervision records a hash of the resolved private log-directory path and pins both kernel raw logs by basename, size and SHA-256. Checker startup requires the same directory identity and unchanged raw files; those pins are rechecked after checker completion. Absolute private paths are not published in these fields. All four raw log names are counted whenever they exist, including earlier-stage logs.

## Prior-stage evidence and success rules

Kernel `scientificEvidence` contains every emitted allowed index/journal/scientific/anomaly file, including partial files on failure. `anomalyEvidence` also identifies any first-mismatch file explicitly. Existing `output` and `journal` pin fields are retained. Kernel success requires index, journal and every declared scene shard, zero child exit, successful guardian release, source/runtime recheck, complete group closure, no anomaly and no budget/accounting failure.

Checker startup requires the exact scientific pin set of index, journal and all six scientific shards from a successful, closed kernel report with matching source publication. It checks every pin against disk, refuses any anomaly, and pins the kernel supervision report itself. Every prior scientific pin and raw-log pin is rechecked after the checker. Checker success also requires its main report and all six reference scene files. The checker remains responsible for schema/mathematical/trial validation and for exiting unsuccessfully on a failed qualification; file presence alone is not an independent scientific verdict.

Exclusive attempt creation remains before child launch, and exclusive raw-log creation prevents accidental reuse. The supervised scientific child is not permitted to spawn subprocesses. The process group contains the guardian and one scientific child; `ps` runs in the observing supervisor. Monitoring and recursive filesystem accounting contribute to the observed environment and do not establish host isolation.

## Checks completed and remaining gate

Both new Python files passed `ast.parse` without importing or executing either module. Preserved original byte equality and SHA-256 were checked. Static source inspection covered category membership, recursive unknown-file rejection, total rather than per-reference checker accounting, same-directory prior raw logs, exact prior scientific pin-set equality, post-stage rechecks, known deadlines and retained cleanup paths. No scientific or supervision smoke test, child process launch, fixture/control run, installation or numerical probe was performed.

Parent review must reconcile these paths, category limits, helper names and scientific pin fields with the forthcoming final contract, runner, checker, protocol and manifest. The final independent source reviews, mathematical proof, source freeze/publication and exact-commit receipt remain prerequisites for numerical execution.
