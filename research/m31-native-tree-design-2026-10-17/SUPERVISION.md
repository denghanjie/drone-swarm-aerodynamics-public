# Native-tree qualification supervision

This is an unexecuted source package. `config.json` is disabled, with null authorization and cutoff. Source preparation does not authorize a query, import of scientific modules, syntax check, benchmark, or retry. The parent owns review, runtime metadata, source manifests, publication verification, future authorization and any eventual launch.

The proposed qualification compares H and H0 with the retained original F on exactly 42 fixed cases, at most 64 drones per case, in fixed case order and method order F, H0, H: 126 calls total. There is one previously exposed saved64 regression. There is no fresh trajectory, 5000-drone run, performance threshold, speed claim, new physical validation or novelty claim. The independent checker decides numerical/evidence qualification. Producer completion alone does not.

## Source and runtime closure

The execution manifest must pin exact bytes and SHA-256 for these repository-relative files:

- This package's `config.json`, `runtime.json`, `source/run.py`, `source/harness.cjs`, `source/check.py`, `source/cases.json`, `source/native-load.cjs`, `source/kernel.cjs`, and `source/tree.cjs`.
- `research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs`.
- `research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs`, `anchor-kernel.cjs`, `lean-anchor.cjs`, and `reference-excerpt.cjs`.
- `research/m31-native-fresh-transfer-2026-10-17/results/inputs/fresh-a-t5.json`: 21,955 bytes, SHA-256 `48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c`.
- The reviewed protocol and supervision documents. Other parent-owned review or viewer sources may be included as additional pins; they are not scientific imports.

Original F requires its original `vendor/kernel.cjs`; that kernel requires the retained anchor, lean-anchor and reference-excerpt. The new native load requires the new kernel, which requires the new tree and the three retained vendor modules. Anchor requires reference-excerpt; lean-anchor requires anchor and reference-excerpt. The harness rejects CommonJS cache entries outside this explicitly listed closure. No bundler, browser loader, Chrome, browser profile or external package is required.

`runtime.json` supplies `platform: "darwin"`, `architecture: "arm64"` and `node`/`python` objects with `version`, `bytes`, and `sha256`. `source-manifest.json` supplies `files: [{path,bytes,sha256}, ...]` with no duplicate paths and matching `runtime.node`/`runtime.python` byte/hash pins. Runtime version strings must match the existing pinned installation: Node v24.19.0 and the full Python 3.12.14 `sys.version` string. The retained binary pins are Node 121,304,480 bytes / `3c9448363b9976bf3d9e8f4d320397975800131b42c7b1be342dadc05871dd25`, and Python 18,058,560 bytes / `7a314947596fc484d4ec36ffc28e843b78d6d749c68736f8b5c24e7333f418eb`.

## Review and publication gates

A future enabled config must contain `authorization: {id, approvedUtc, reviewedSourceManifestSha256}` and an explicit timezone-aware `launchCutoffUtc`. The reviewed hash identifies the disabled draft; the actual enabled config is pinned by the execution manifest, avoiding a self-hash cycle. The renewed user window does not silently change this disabled draft.

Before launch, the parent must publish the frozen source manifest and all its pinned files, then create `source-publication.json` with the exact `commit`, `manifestSha256`, `manifestPath`, `manifestBytes`, `verifiedFilePins`, `remoteBytesEqualLocal: true`, `committedBytesEqualLocal: true`, and `verifiedUtc`. This receipt is separately protected; it must predate the attempt. It records verification of published/committed bytes, not merely a local commit identifier.

The sole entry is the pinned Python executable running `-I -B source/run.py MANIFEST_SHA SOURCE_COMMIT` from this package's repository. This is a contract for a future authorized invocation, not an instruction to execute this draft. Required private environment fields are `RESEARCH_EXECUTION_CONTEXT=tool-require-escalated`, `RESEARCH_NODE` (the pinned executable), and `RESEARCH_PRIVATE_LOG_DIR` (a new canonical absolute directory outside the repository, preferably under `/private/tmp`). `NODE_OPTIONS` and `NODE_PATH` must be empty. Paths are not placed in public output; the private-directory identity is hashed.

The supervisor requires a fresh, absent `results/` directory. It creates one exclusive attempt marker and never overwrites a scientific artifact. The only replaceable file is its own `run-attempt.json`, using an exclusive temporary file, fsync, atomic replace and directory fsync. A failed attempt cannot be rerun in place; it is retained. No retry is implemented or authorized by this package.

Before scientific `require`, the harness checks authorization, supervisor token/stage binding, source manifest, every listed source/input pin, runtime identity and publication receipt. The supervisor supplies a random run token; public evidence contains only its hash. The work-stage attempt ledger is itself protected against mutation while Node is active. The supervisor rechecks sources, initial inputs, publication and prior stage artifacts before and after each stage. Earlier artifacts are verified **before** taking a replacement snapshot.

## Time and resources

The complete reservation is 180 seconds: work 120, independent checker 45, and 15 shared seconds for supervisor preflight, runtime hashing, handoffs, closure and other overhead. At sole entry, the full 180 seconds must remain before the UTC cutoff, before any marker or spawn. The total deadline also begins at supervisor entry, so preflight time is charged. Stage intervals include spawn, polling and reaping; other work is charged to shared overhead.

Node uses its own `performance.now()` epoch and a 115-second cooperative work deadline, leaving five seconds inside its 120-second allocation for serialization/handoff. Python independently enforces stage and total limits, with 0.1-second polling and a per-child CPU limit. The checker receives Python monotonic deadlines and its 45-second budget. Node never compares its monotonic epoch with Python's. The parent should observe the supervisor process's exit code: `run-attempt.json` is a pre-exit record, not proof of process exit. All final report writes receive a post-write total/cutoff check.

Each output or private log file is capped at 32 MiB. Results, evidence sidecars, private logs and any scratch share a 128 MiB budget, including a 2 MiB finalization allowance for the attempt report and its temporary replacement. Node checks existing results/private-log bytes before every evidence/journal write. The supervisor monitors both trees and installs `RLIMIT_FSIZE`; the checker must check the same aggregate before writing its report. These checks preserve the first observed failure and stop the owned child. There is no OS memory ceiling or claim that an entire process tree was measured or contained. The pinned programs do not spawn descendants; only the two owned direct child handles are killed/reaped if needed. Private logs remain private; their byte/hash identities may be reported.

Node peak RSS is process-lifetime `process.resourceUsage().maxRSS` converted from KiB to bytes. Supervisor RSS is macOS `ru_maxrss`, already bytes. Neither is a stage-isolated or aggregate child-tree measurement. Timing is diagnostic only. Durations explicitly stop before the final report write; final fsync and interpreter exit occur later. Failed child time remains child time and is not relabeled overhead.

## Evidence and checker interface

The supervisor launches `node source/harness.cjs ROOT MANIFEST_SHA SOURCE_COMMIT`, then only after successful work launches `python -I -B source/check.py ROOT MANIFEST_SHA SOURCE_COMMIT`. It sets `RESEARCH_STAGE`, `RESEARCH_RUN_TOKEN`, `RESEARCH_CHILD_BUDGET_MILLISECONDS`, `RESEARCH_CHILD_DEADLINE_MONOTONIC_NS` and `RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS`. The checker reads saved files independently and imports no producer/scientific module.

`source/cases.json` defines inline cases, repeated descriptors, boundary recipes and the one saved input. Inline states are copied from `baseStateWords`, then center words and indexed overrides are applied. Missing IDs stay absent; NaN words and other invalid-input controls are decoded as supplied. Each method gets a fresh ordinary numeric object with the same expanded input. Input ownership is compared recursively with `Object.is` so NaN and signed zero are represented honestly. No expected status is enforced by the producer.

The work outputs are:

- `results/evidence/NNN-CASE-METHOD.json`: exclusive, fsynced full `encodeEvidence` output immediately after each query returns. F comes from the original implementation; H/H0 come from the new implementation with `{treeEvidence:true}`. Native refusal and incomplete tree evidence are retained. These sidecars survive a later query failure.
- `results/work.jsonl`: one fsynced JSON line per completed case, exactly `{id,input,methods:{F,H0,H},inputUnchanged:{F,H0,H}}`, where input states are full binary64 words. It is the durable completed-case prefix when a later case fails.
- `results/work.json`: schema `m31-native-tree-work-v1`; bindings `sourceCommit`/`sourceManifestSha256`; `complete`, `status` (`completed` or `failed`), structured failure `reason`, all complete `cases`, full evidence-sidecar pins, journal pin/count, runtime/preservation flags and diagnostic timing/RSS. A completed run has journal rows equal to `cases`; an interrupted/missing/incomplete run fails qualification.
- `results/check.json`: independently generated by the checker, with the same source bindings and `complete:true, passed:true` required for supervisor success. It validates all saved native payloads and H coverage/cull certificates, including checker-side mutation/arithmetic controls.
- `results/run-attempt.json`: schema `m31-native-tree-attempt-v1`, status `running`, `completed` or `failed`; stage order and per-stage records, first failure, preservation result, output/log hashes and resource scopes. A nonzero actual supervisor exit invalidates overall success even if a pre-exit report was written.

Every successful or refused native payload is saved whole, including raw/prepared state, coefficients, solver outputs, loads, admission diagnostics and consumption checksum. The checker determines precisely which timing/method/work fields may differ and must not replace full evidence comparison with a checksum or producer self-certification. H/H0 tree certificates accompany their native evidence. The full original F evidence remains the numerical comparator.

## Source-only handoff

No drafted module has been imported, queried, syntax-checked, tested or run during this author's source phase. No network or Git operation was performed. Parent review may use pinned Node `--check` on CJS files and pinned Python `-I -B` with `ast.parse` on Python source; a bytecode-producing compile is unnecessary. Those prospective checks are not qualification results. Freeze/publication must include any fixes made during that review before the single authorized attempt.
