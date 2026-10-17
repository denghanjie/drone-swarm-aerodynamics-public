# Prospective supervision contract — execution disabled

This package is source preparation. `config.json` has `executionAllowed: false`, `authorization: null`, and `launchCutoffUtc: null`. No new execution window has been approved. The drafting agent did not import scientific modules, execute a driver, launch a browser, run the bundler, run syntax checks/tests, access the network, or invoke Git. Parent review, source packaging, syntax checks and publication remain separate steps.

## One attempt and a shared reservation

The intended sole entry is `source/run.py MANIFEST_SHA SOURCE_COMMIT`, using the approved pinned Python runtime. It dispatches browser → reference → check sequentially. Each child receives `ROOT MANIFEST_SHA SOURCE_COMMIT`; the browser child is the pinned Node controller, while reference/check are isolated Python children. The existing server on port 8876 is neither started nor modified.

The approved window must contain a full 960 seconds at entry, before an attempt marker or child spawn. The monotonic supervisor deadline is the earlier of entry + 960 seconds and the authorized UTC cutoff. Browser, reference, and check have child allocations of 120, 600, and 180 seconds. The remaining 60 seconds is a shared allowance for source/runtime validation, evidence accounting, handoffs, final checks and closure. Allocations do not reset on failure and unused time does not enlarge a stage. Source hashing polls the total deadline. Live-child polling checks stage deadline, total deadline and aggregate/per-file byte usage at intervals of up to 0.1 seconds plus filesystem traversal cost.

Node uses its own `performance.now()` deadline of 110 seconds for browser work; the outer Python stage independently enforces 120 seconds. The remaining 10 seconds is inside that browser allocation, for root/controller closure and guardian handoff. Page work receives the then-remaining controller budget minus one second. No assumption equates the Python monotonic epoch and Node hrtime epoch. UTC cutoff guards remain separate.

The supervisor report labels its duration `preFinalReportWallSeconds`. Its final durable report write and interpreter exit occur after that sample; a post-write deadline check rejects overrun. The report does not claim an exact duration through process exit. Ordinary userspace polling and filesystem writes do not constitute an OS hard wall-clock guarantee under host suspension or supervisor failure.

## Authorization and source closure

Before any scientific child launch, the supervisor requires enabled authorization, an approved timestamp, a future cutoff with the complete reservation, pinned source and runtime bytes, and a publication receipt binding the exact manifest to its source commit and verified public bytes. The eventual authorization object must contain `id`, `approvedUtc`, and `reviewedSourceManifestSha256`; the latter identifies the reviewed disabled draft, avoiding a self-hash cycle. The enabled configuration itself must be pinned in the execution manifest and republished before use. No authorization values have been invented.

The supervisor creates one exclusive `results/run-attempt.json` with a random token digest, source bindings and per-stage status. Children verify their environment token against that digest and their started stage. An occupied results directory or prior attempt refuses another launch. Failure preserves the first error and partial artifacts; there is no retry, replacement input or second browser launch.

The reference completion gate requires both `complete: true` and `qualified: true`. The checker completion gate requires `complete: true` and `passed: true`. Every later stage must preserve all earlier output/sidecar bytes. Source manifest, publication receipt, source files and initial retained input are reverified. Direct child entry points retain their own authorization/source/attempt checks before scientific imports.

## Browser source and durable evidence

The unexecuted `build-bundle.py` packages exact retained source bytes with byte offsets and SHA-256 identities; it does not import/evaluate them. Its allowlist consists of four existing native kernel dependencies, the native load interface, seven retained physics/swarm/grid/geometry/factory/filter modules, and the new adapter/browser driver. Existing source files remain unchanged. Bundle outputs are exclusive and capped at 2 MiB.

`browser.html` only defines the page entry point. The controller verifies the source manifest, publication, runtime, bundle and original source slices, then serves only the three pinned page files through its localhost route allowlist. The page verifies bundle bytes and each source slice again before factory execution. CommonJS dependency resolution is restricted to the fixed module list. Only the factory module receives a lexical frozen `process.env.FLOCK_FACTORY_VARIANT = 'wide'`; no global process or Buffer is changed. The retained local Buffer compatibility controls run before scientific factories.

The controller passes the exact pinned science configuration, retained initial raw-word state and provenance to the driver. Browser evidence is appended to `results/browser-journal.jsonl` as `{sequence, kind, body}`. Every append is fsynced before acknowledging `{durable: true}`. Every primary stage with a non-null projected `nativeInput`, including a failed native attempt, also creates an exclusive `results/inputs/<stageId>.json` containing exact `JSON.stringify(nativeInput)` UTF-8 bytes without a trailing newline. These sidecars are fsynced before the stage journal acknowledgment. `browser.json` maps stage IDs to those byte identities and contains the journal identity/count, source/runtime/input bindings, summary and operational status; it does not duplicate the full stage records. The reference/check agents consume this immutable journal.

The science driver owns the exact finite schedule: 32 primary native F stages, 32 matched-off stages without native queries, 12 wiring groups, 9 manufactured runs and 3 manufactured summaries. The manufactured 0.01-second interval at the three declared step sizes contains 84 steps / 336 stage evaluations with no native aerodynamic query. A raw first-k2 norm diagnostic performs no alternate full query. The science config and independent checker, rather than this operational controller, define scientific acceptance.

## Owned process shutdown

The verified prior design is retained: the browser guardian is an unreaped session/group leader while the controller runs. The controller intercepts the single pinned Chrome spawn, forces `detached: false`, saves process ownership data privately, and listens to that specific root's error/exit/close events before returning the handle to Playwright. A successful browser index requires successful context close and root exit/close codes 0 with no signal/error. Only then does the supervisor release and reap the guardian without group signaling.

On failure, the supervisor signals only the still-owned unreaped browser group. Parent-pipe loss makes the guardian kill its own group. No signal is sent to a group after its guardian has been reaped. The design confirms the controller and specific Chrome root, not every Chrome helper; guardian SIGKILL, host suspension or loss of the supervising process remains outside hard containment claims.

## Disk, paths and memory

Every output/log/scratch file is capped at 32 MiB; total new results, private logs/profile/scratch plus an explicit 2 MiB finalization byte allowance must fit within 256 MiB. Per-child file-size and CPU limits supplement polling. Aggregate disk enforcement is observed at polls and completion, so transient growth between polls is not a filesystem quota guarantee. Private profile symlinks are not followed during accounting. A journal record has a further 2 MiB cap. The reference uses separate capped stage files plus a descriptor journal to avoid a single oversized file.

Private runtime executable/module/profile/log paths arrive only through environment variables. Public artifacts contain path identities/hashes or redacted codes; detailed exception logs and Chrome arguments remain private. Source-relative paths and retained input pins are public. No paid service, contact or remote job is involved.

There is no OS memory limit. Supervisor peak RSS is macOS `ru_maxrss` for the lifetime of that supervisor process. Controller peak RSS is Node's process-lifetime `maxRSS` converted from KiB to bytes. Neither is a Chrome renderer/tree aggregate or an isolated stage measurement. Scientific reference/check memory scopes must be reported by their respective processes. These observations cannot establish all-helper memory containment.

## Remaining review work

This is an unexecuted implementation draft. Parent must review all file/event schemas together, run syntax checks, build and inspect the source bundle without evaluating its factories, freeze the complete source/runtime/input closure, privacy-review and verify publication. Any requested execution window must then cover the entire 960-second reservation, and its separately reviewed authorization must be frozen and published before dispatch. Source presence is not evidence of operational or scientific success.
