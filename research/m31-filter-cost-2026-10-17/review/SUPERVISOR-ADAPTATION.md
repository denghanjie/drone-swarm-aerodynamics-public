# Prospective supervisor adaptation

Author: `m31_verified_literature`. Source-only adaptation for the fresh `m31-filter-cost-2026-10-17` cycle. Independent containment review and the full public source gate remain required before execution. No scientific source was imported or run, no runtime was probed, and no previous allocation was reopened.

The base supervisor and guardian come from the closed screening-cost cycle. The prior filter-design supervisor was read to carry forward its exclusive-stage and lifecycle evidence protections. Runtime pins are an exact copy of the screening-cost bytes; they are expected identities to be enforced at the future source gate and each stage, not a claim that a runtime was executed here.

## Bounds and result graph

| Category | Bound |
| --- | ---: |
| Kernel / checker wall limit | 600 s each |
| Guardian deadline | 610 s each |
| Sampled process-group RSS | 1 GiB |
| Aggregate retained output | 768 MiB |
| Each scene or first-mismatch shard | 128 MiB |
| All scene and anomaly shards combined | 384 MiB |
| Checker main report and six reference shards combined | 128 MiB |
| Timing index / journal | 8 MiB each |
| Logs and metadata, including private raw logs and public copies | 16 MiB |
| Each supervision report | 64 KiB |

Exactly six distinct scene IDs, restricted to the declared safe filename pattern, define the closed result graph. Kernel paths are `timing-index.json`, `timing-index.json.jsonl`, `scenes/{id}.json`, and the optional `anomalies/first-mismatch.json`. Checker paths are `independent-check.json` and `reference-scenes/{id}.json`. The runner and checker authors confirmed these names and the existing checker CLI. An anomaly prevents qualification. No extra scene, reference, directory, or private entry is admitted.

## Retained and strengthened gates

The guardian retains session-leader ownership until the child exits and the supervisor releases it. Group RSS/descendant sampling, termination escalation while the owned guardian is still alive, residual-group checks, disconnect handling, cleanup, and closed-stage reporting retain their existing control flow. The guardian changes only its deadlines. Sampling remains an observed limit and is not hostile-code or escaped-descendant isolation.

Publication must record remote and committed manifest byte equality, the exact manifest length/hash, and a 40-character commit identity. Required local pins include the entire candidate graph, both reference helpers, checker, runner, spec, contract, runtime pins, guardian, supervisor, and protocol. The source files are local copies; no external runtime import is intended. Every pinned path must be canonical, a regular file, and free of symlink resolution. Runtime binary lengths/hashes are checked before and after each future stage. The manifest and publication bytes themselves are retained and rechecked.

The kernel requires empty result and private-log directories. Current-stage outputs, attempts, reports, guardian journals, raw logs, and public logs must not preexist. Attempt and report creation is exclusive and durable; raw logs are exclusive; this adaptation also makes published redacted log copies exclusive and durable. All private entries are accounted for and unknown entries rejected.

The checker requires a successful, closed kernel with zero child/guardian exit codes, absent child group, scientific-child disappearance before release, and successful post-run source/runtime checks. The complete scientific evidence set, kernel report, attempt, guardian journal, public stdout/stderr, and both private raw logs are pinned before checker allocation and rechecked after it. The current stage's output and budget checks remain active throughout supervision and at finalization, with report headroom reserved. Missing required outputs or any anomaly prevents success. Finalization failure retains an exclusive terminal failure record with closure unproven.

## Validation and scope

The new Python files were AST-parsed without import or execution. Runtime-pin bytes were compared with the recorded source, and explicit source diffs/required-path changes were inspected. This is not an empirical containment test, cost result, physical validation, or novelty claim. The upcoming numerical protocol/checker will be reviewed separately once ready. Previously verified literature remains available through the existing filter-design review and ledger; no new literature retrieval was needed.

Fresh-cycle inherited-content reads are four distinct paths against the cap of sixteen, recorded in `SUPERVISOR-ADAPTATION-READING.json`. Current-cycle generated review/source files do not add inherited paths. No installation, numerical execution, scientific probe, or commit was performed.

## Current authored pins

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/m31-filter-cost-2026-10-17/source/supervise.py` | 22023 | `4d517a3515f66816b4ca74864147e63cc61aa15af0e2fc8e78aa6c640e4365cb` |
| `research/m31-filter-cost-2026-10-17/source/guardian.py` | 1890 | `074f3e4921bf94718fd6a9eb5fec83b524d786cf445bc733946c026d4e30eed1` |
| `research/m31-filter-cost-2026-10-17/runtime-pins.json` | 248 | `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087` |
