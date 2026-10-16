# Moving-admission supervisor source adaptation

Status: source authored and AST-parsed only. This is a change record, **not independent acceptance of this author's supervisor**. The evidence-audit reviewer has been asked to inspect the exact current source. No scientific or browser execution has been allocated or performed.

## Sources and identity

The supervisor and guardian adapt the closed scalar-filter cost containment design. Runtime pins are an exact byte copy. Four inherited content paths were read under the fresh20-file cap; all hashes and scopes are in SUPERVISOR-ADAPTATION-READING.json. No old package was edited and no inherited run was reopened.

The scientific supervisor refuses startup unless its interpreter is in isolated mode. Eventual operator form is `PINNED_PYTHON -I PACKAGE/source/supervise.py kernel` (or checker), with RESEARCH_NODE and RESEARCH_PRIVATE_RUN_DIR supplied externally. Actual machine paths are never saved in public artifacts. Running these commands is not authorized by this note.

Before either stage, source-publication.json must assert independently verified remote/local/committed manifest equality and match its package-relative manifest path, SHA-256, byte count, file count and40-hex commit. Its UTC verification time must not be in the future or at/after the launch cutoff. The supervisor checks git HEAD equals that exact commit and reads the committed manifest and every manifested file; each must match the actual saved bytes and pinned identities. The same check repeats after closure. It also hashes the selected Node executable and its own Python executable against public runtime-pins.json. Receipt bytes and prior-stage evidence are rechecked, not just source filenames.

The required manifest closure explicitly includes final PROTOCOL.md and RECORD-CONTRACT.md, config/spec/result-contract, all method/filter/adapter/arithmetic/load helpers, runner, checker, both independent reference helpers, supervision/guardian and runtime pins. The runner supplied seven generator dependencies: milestone-31-source sim, grid, geometry, factory, factory-wide, wall-filter, plus step02c-source physics. Each is mandatory in the manifest. This author did not independently read that generator closure; its correctness is a separate runner/source-review obligation.

## Launch cutoff and runtime isolation

The hard cutoff is **2026-10-16T23:00:00Z** (07:00Asia/Shanghai on17October). It is checked at initial supervision entry, immediately before claiming the permanent attempt, immediately before launching the guardian, and by the guardian immediately before spawning the scientific child. A stage started before the cutoff retains its declared duration; this is a launch cutoff, not an invented early stop/retry policy. Config must declare the same cutoff and the same exact resource values as the supervisor constants.

Guardian and checker are launched with Python `-I -B`: isolated import configuration and no helper bytecode-file creation. NODE_OPTIONS and NODE_PATH are removed from the scientific-child environment, along with Node coverage/warning redirection and Python import/startup variables. The guardian independently refuses nonempty Node preload variables. Known dynamic-loader injection variables are refused by the supervisor and stripped from child environment. Required RESEARCH_* variables remain available. These precautions address accidental ambient preload; this is not isolation from a hostile machine or an already compromised process.

## Stage ownership and records

The supervisor alone creates and fsyncs permanent kernel-attempt.json/checker-attempt.json using exclusive creation. Any existing stage artifact/private raw log blocks reuse. The kernel starts only with empty result and private-log directories. Attempt fields are stage, sourceCommit, sourceManifestSha256, configSha256, launchCutoffUtc, allocation and startedUtc. The allocation string states that existence prevents retry. The runner must validate these identities and must not create a second marker with the same name.

Kernel CLI is `NODE PACKAGE/source/run.cjs PACKAGE_ROOT`. It receives manifest path, expected manifest SHA, source commit and stage through RESEARCH_* environment. Kernel output names are index.json, kernel-journal.jsonl, four fixed control shards, two generation recordings and the six possible scheduled scene shards. A recording contains its unscheduled terminal diagnostic, so no extra terminal scene is allocated.

Checker CLI is `PYTHON -I -B PACKAGE/source/check.py --config PACKAGE/source/config.json --input PACKAGE/results/index.json --manifest PACKAGE/source-manifest.json --output PACKAGE/results/check.json --root REPOSITORY_ROOT`. References may use only the four fixed control IDs and six scheduled IDs in results/reference. No anomaly directory or undeclared output is allocated.

A kernel can close successfully while recording valid model refusals or explicit not-reached slots. Its mandatory structural outputs are the index, journal, four controls and two generation recordings. Scheduled shards are an allowed subset. The checker must verify the index's exact six-slot reached/not-reached structure and the corresponding file/capture identities; the supervisor does not infer numerical admission from file existence. Unhandled kernel failure or failed containment closes the kernel unsuccessfully and blocks saved-checker launch.

Before the checker launches, the previous kernel report must prove successful closure, zero child/guardian exits, scientific-child absence before release, child-group absence and unchanged source/runtime identities. Every extant kernel scientific output, lifecycle record and both private raw logs must match the previous exact pins; missing mandatory files or changed private-log directory identity fail the gate. Those inputs are pinned again through checker completion. Checker `passed` and `advancement` remain separate scientific report fields; supervisor success means a complete contained stage with exit0 and a saved check.json, not that every scheduled state was admitted.

## Resource accounting

| Limit | Budget |
|---|---:|
| Kernel / checker scientific child stage | 600seconds each, one attempt each |
| Guardian independent deadline | 610seconds per stage |
| Sampled process-group RSS | 1GiB |
| Kernel scientific output | 192MiB |
| Checker output, including references | 64MiB |
| Combined scientific output | 256MiB |
| Individual control/scene/reference shard | 32MiB |
| Individual run recording | 8MiB |
| index.json / kernel-journal.jsonl | 2MiB /4MiB, within kernel scientific budget |
| check.json | 2MiB, within checker budget |
| All metadata and private/public logs, including supervision reports | 16MiB |
| Combined scientific and metadata/log output | 272MiB |
| Individual supervision report | 64KiB |

Accounting recursively inspects a closed filename/directory set. It counts all existing files, private raw logs and public redacted copies; a file remains counted even if unrelated to an index descriptor. Symlinks, unexpected directories/files and unallocated private entries fail closed. During the kernel, checker-owned files, private logs and reference directory are refused. Each output category has its own cap in addition to aggregate caps; the two stage allocations cannot borrow unlimited capacity from one another. Final-report capacity is conservatively reserved in both aggregate and metadata budgets.

The supervisor samples the retained guardian's group, records sample count/peak RSS/maximum gap, refuses extra or observed escaped descendants, and bounds stage wall time. The guardian has its own deadline and detects supervisor disconnection. It retains the process-group leader after scientific-child exit until the supervisor confirms the child is absent and releases it. Failure cleanup terminates the still-owned group and verifies absence; it avoids signalling a reused group identifier after leader exit. RSS/output sampling can miss transient overshoot and cannot establish hostile-code containment. The reviewed children must not spawn subprocesses.

Public logs replace repository, private directory, executable, home and temporary-directory prefixes; raw logs remain private and are pinned. A finalization exception records a failed terminal report with closure unproven. Partial evidence and permanent attempt markers remain; no retry is created.

## Current source pins and review boundary

- source/supervise.py:26738bytes, SHA-256 `c10aaffea8ea75ba585bc3145aef3e75d473a88687d244467afb3ef4ba06c794`.
- source/guardian.py:2276bytes, SHA-256 `10341c52ab32fa8ff80c3909d578a7d368a3b2bcea59e78af7e8aa8f29c619f0`.
- runtime-pins.json:248bytes, SHA-256 `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087`.
- SUPERVISOR-ADAPTATION-READING.json:4023bytes, SHA-256 `957c63d5035cdecb2802627bca99201d03f011261e9c099aab91bd164563fb87`.

The only local verification was AST parsing and byte/hash comparison. No candidate import, simulator generation, control evaluation, reference calculation, scientific timing, browser run or runtime probe occurred. Independent supervisor acceptance, final protocol/checker review, source freeze, public publication and exact-source verification are still required before any allocation.
