# Browser-screen supervision: bounded final static review

**Disposition: no unresolved blocking static defect found in the six-file snapshot identified below.** This is a source-only assessment after the parent corrected the findings in this review. It is not evidence that process launch, cleanup, persistence, numerical checks, or the experiment have executed successfully.

Scope was exactly `source/run.py`, `source/group-runner.py`, `source/process-registry.cjs`, `source/controller.cjs`, `config.json`, and `runtime.json` in `research/m31-browser-screen-2026-10-16`. The source was read, reread after corrections, and byte-pinned. No browser or process-supervisor test was launched; no scientific module, generator, control, warmup, query, result array, or new literature was evaluated or retrieved. The reviewer edited no parent file. The final reviewed copies were retained locally for stable source identity.

## Corrections verified in the final source snapshot

| Initial issue | Resolution seen in final source |
|---|---|
| Collector ignored short `fs.writeSync` results and used replacement-capable rename without directory sync | `controller.cjs:28` loops until the chunk is fully written; lines 30–33 fsync and close the file, publish by no-replace hard link, unlink the partial name, fsync the directory, reread the published bytes, verify their length/hash, and only then return the durable/exclusive acknowledgment. |
| Private child/exit/active/ack JSON could become visible before its content was complete | Guardian child/exit records and monitor barrier acknowledgments publish complete temporary files atomically; active-slot publication is an atomic replacement. The active marker is retained until the next replacement, eliminating the exists/read/unlink race. |
| Observed descendants that escaped the retained process group were detected but not killed | `run.py:134` onward uses fresh matching start-identity checks before signaling known escaped survivors, records the signals/failure, and resamples bounded absence. Successful qualification cannot follow the escape or cleanup signal. |
| Sampled storage accounting could fail when a normally completed `.partial` disappeared | `run.py:45`–54 tolerates only `FileNotFoundError` for transient `.partial` paths. Other stat failures remain failures; final stable artifact checks remain strict. |
| A stale pre-exit snapshot could reject a child that had just exited normally | `run.py:119`–122 reads the atomic exit record and takes a new process snapshot before checking residual owned processes and releasing the guardian. |
| Errors arriving during awaited shutdown could leave campaign success true | `controller.cjs:88` derives final completion from scientific completion, runtime/input verification, no pending transport, successful browser/barrier closure, owned-process absence, and zero errors. Any false result sets the campaign failure state and prevents later slots. Scientific schedule completion is retained separately. |
| Candidate metadata claimed a 1.5 GiB aggregate RSS cap while enforcing different component caps | Candidate metadata now uses `rssCapBytes:null` and records separate controller and browser-tree limits. Generation/review retain their explicit sampled group limits. |
| Spawn registration accepted any executable with a matching suffix and did not exclude reused profile arguments | `process-registry.cjs:11`–14 verifies the actual canonical launcher path and launcher bytes/hash, and rejects missing or previously used profile arguments. Chrome is forced to `detached:false`. |
| Controller source names/routes did not match the browser-bundle interface | The allowlist now includes `browser-bundle.js` and `source-bundle.json`; root `/source/` paths resolve through the allowlist. The page receives the parsed `sourceBundle` and runtime evidence in its configuration. |

The inherited generator handoff also had a separately identified lock-name collision: the supervisor creates `generation-invocation.lock`, so the child must use `generation-child-invocation.lock`. The parent reported adopting that correction; the delivered `/tmp` generator also contains it. Its input index now includes `generationPin` directly from the exact generation-record write result. The integrated parent generator is outside this six-file final snapshot and must remain checked by its own source pin/integration review.

## Lifecycle, failure, resource, and interface assessment

The guardian remains the owned session/group leader while its direct child runs and until the parent has observed child exit and an otherwise empty owned group. Parent-pipe loss directs the guardian to kill its own group. The monitor retains observed descendant identities, checks group escape, samples total/component RSS, and requires two empty browser/helper observations before issuing a per-slot barrier acknowledgment. The controller waits for that acknowledgment before beginning another slot. A launch/identity/page/transport/close/barrier failure sets failure, retains available evidence, and stops the remaining slots. Exclusive stage/slot locks prevent an ordinary retry from replacing the consumed invocation.

The collector admits only single-component `results/` filenames, canonical bounded base64 chunks, one in-flight artifact, and the declared normal/emergency output budgets. Final acknowledgments contain `path`, `bytes`, `sha256`, `durable:true`, `exclusive:true`, `fsync:true`, and `directoryFsync:true` only after successful publication and reread. The browser author's obligation to await the raw-record acknowledgment before validation remains outside this six-file review; the collector now provides the needed acknowledgment semantics.

The stage supervisor checks source-manifest/local/committed pins and the publication receipt before launch, retains the receipt hash for its final unchanged check, and checks child/runtime identities before importing through the child process. It samples the retained group plus known descendants rather than only the direct Node process. Generation is capped at 900 s with a 64 MiB generated-output limit; candidate supervision is capped at 3000 s and independently applies a 900 s browser-slot timer from the first observed active marker; review is capped at 600 s and a 128 MiB new-output delta. The final controller slot check uses its own elapsed time from slot start. Generation/review RSS limits are 1610612736 bytes; candidate limits are 536870912 controller bytes and 2147483648 browser-tree bytes. Aggregate sampled RSS remains reported without inventing a candidate aggregate cap. The global directory/log/administrative-reserve checks remain separate.

The supervisor's success predicate requires terminal closure, return code zero, runtime identity, unchanged protected files, at least one sample, no cleanup signals/monitor failure/finalization failure, and elapsed time within the stage cap. Elapsed time is refreshed when preparing the final record; a final time or storage overflow revokes success. The controller preserves a returned incomplete page result before its completion assertion. A review supervisor can successfully review a closed failed candidate; that lifecycle success must never become the candidate's scientific qualification.

The parent states that the separate final seal will require success of all three stages, complete valid process closures, the independent numerical/performance gates, and the recorded actual elapsed sum at most 4500 s. That seal, the browser scientific harness, and the independent numerical checker were not among these six files, so their conjunction is **not certified by this report**. Missing or failed closure/evidence must remain nonqualification. No successful static review authorizes a new scientific invocation by itself.

## Limits that must remain disclosed

- Process discovery, RSS, storage, and per-slot timing enforcement are sampled userspace observations, not kernel containment or a proof of true peak memory. The slot timer starts at the monitor's first observation, with sampling latency; the controller's own timer and final elapsed check supply the complementary slot boundary.
- The PID/start-time check and later signal are not atomic. Very short-lived, never-observed helpers, an abrupt guardian kill, host suspension, or host-level failure remain outside the ordinary containment guarantee. Two empty snapshots are evidence of sampled absence, not a universal proof that no process ever escaped.
- Source/runtime pinning is the stated selected inventory. `runtime.json` explicitly does not claim a complete inventory of all transitive browser/runtime resources.
- No cleanup fault injection, launch probe, file-durability fault test, resource stress test, or scientific execution occurred. Parser success cannot establish any of those runtime properties.

## Parser-only validation

The parent-supplied pinned Node parser accepted the delivered `generate.cjs` and final reviewed `controller.cjs`/`process-registry.cjs` with `--check`. Python standard-library `ast.parse` accepted final `run.py`/`group-runner.py`; standard-library JSON parsing accepted `config.json`/`runtime.json`. These operations did not import or execute the reviewed modules. The initial generic `node --check` attempt found no `node` on PATH and executed no script; it was replaced by the explicit pinned-parser call.

Delivered generator source: 12858 bytes, SHA-256 `fec8b14b804c8fc0e930172c2e8f0fae620a33727ca5ed31b76932b569d440cc`. Its separate source/interface/static ledger is in the generator handoff directory. Later edits require new source identities and an appropriate delta review.

## Exact six-file content-read inventory and final identities

Paths below are relative to `research/m31-browser-screen-2026-10-16`. The final parser checks used the exact snapshot bytes identified here. Earlier defective snapshots are superseded by these final identities for this disposition.

| Content file | Bytes | SHA-256 |
|---|---:|---|
| `source/run.py` | 14328 | `31e54e76a6b3c2b560ab3c698d9dd4942fdfd453aa3c8a5e2639c62ea1878f45` |
| `source/group-runner.py` | 1067 | `5afedcbc870c6aac0898309e53e086c6763433d06a6fec115e36ff0fc30ef262` |
| `source/process-registry.cjs` | 1774 | `f5c3e724943b0785108049c13cfc1099bbeca41e919a7189af9dca4e1e04f078` |
| `source/controller.cjs` | 11134 | `f5f3dc42b289f5f602865c47d5c56ef7e5a245115e87ae845d018acee87af8fd` |
| `config.json` | 3972 | `a5d76a46bc8abf6531d1f6261db621e4615ca8be598159693d24fcfc66505c7a` |
| `runtime.json` | 6678 | `500a1522833696a7c4fff4bb3eeaf84514304ac101148ca11f56968bfced4460` |
