# Preliminary static source review — runtime-qualified body-load replication

**Disposition:** preliminary static pass for the revised snapshot. Numerical inheritance and environment-first ordering are supported; the runtime-failure evidence issue found during this review was corrected and re-reviewed below. No remaining actionable source issue was found in this scope. This is not allocation, final approval, source-publication verification, or permission to launch. The pending parent-result commit is expected at this stage.

Reviewed directory: `research/m31-body-runtime-replication-2026-10-16/` in the M31 checkpoint repository. Baseline: the original `research/m31-body-load-2026-10-16/` files, checked against that campaign's saved `freeze.json` pins. Exact reviewed hashes are listed below and separately in `preparation/PRELIMINARY-SOURCE-PINS.json`.

## Scope and method

Read source/JSON/documentation, computed source-file hashes and byte comparisons, inspected textual diffs, parsed the three changed JavaScript modules with `node --check`, and parsed `run-once.py` with Python `ast.parse`. No campaign module was imported. No browser, installed-runtime inspection function, shader compiler, input generator, reference solve, numerical evaluator, binary science decoder, GPU workload, binder or viewer was executed. No integrated edits were made.

Thirty-three static checks passed after the revision; their complete results are in `preparation/PRELIMINARY-STATIC-CHECKS.json`. Empty `raw/` and `results/` directories existed, but contained no entries. No replication freeze or sole-launch lock existed. Only the two runtime admission sources and their source-change-ledger entry changed from the first snapshot; those changes were explicitly re-reviewed and the hashes refreshed. This is evidence about the inspected workspace snapshot, not a statement that the draft was published or allocated.

## Finding corrected during this review

**Resolved P2 — Partial runtime inventory on admission failure.** The initial `runtime-pins.cjs` snapshot (`34cb86a7903e545c19badceb5d396644ea4ed83c1b922c62f2a3484aec5bf717`) returned inventory data only after every pin passed. A failure discarded the reached labels/byte counts/actual hash and retained only the generic terminal error. This was an auditability issue, not an admission bypass.

The revised helper creates a bounded `out` receipt before admission, records the safe actual framework version, completed pin records, and a current-file record with public label, expected/observed size, bytes read, and actual hash only if reached. Its outer catch at line 35 attaches `{kind:'runtime-inventory', buffers:{}, metadata:...}` to the error. `experiment.cjs:80` now wraps both before/after calls in `saveRuntime`, invokes the unchanged `savePartial` writer on error, and rethrows. Because `buffers:{}` is present, the existing writer saves the metadata as `browser-runtime-before-launch-partial-status.json` or `browser-runtime-after-launch-partial-status.json`, subject to the existing evidence cap and filesystem availability. The existing public-value sanitizer removes local paths from error messages; source-controlled labels stay relative. No retry, resumed hash, added scientific work, or scientific gate change was introduced. Parser checks and static control flow support this correction; no failure fixture or runtime function was executed.

## Verified inheritance

Eight declared unchanged files are byte-identical to their originals and those originals match the original frozen pins:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/host.cjs` | 51159 | `c7e67c4d2575611a50f6af50b94e6a71c5e98c4083394644b15ba8b29ed5f8fd` |
| `source/body.wgsl` | 26719 | `09aa77ff09dda9a93db6cce60dd4ef4599f0b6613b2945e90bc39eb74c417f2e` |
| `source/browser.js` | 11130 | `74e306c638723727ec86eeb160970a0fce9f582288e550d971a822f5551d5e95` |
| `source/browser.html` | 287 | `1743cb496cfc6d9237abd5c487b8495bd74d53af10811856c6c5b9e0d8ef76e7` |
| `source/process-registry.cjs` | 1539 | `cd6ceca7bc85b5de340cbd61996642f53bd7affc56654427a3c921c926ed3152` |
| `source/independent-frozen.source.txt` | 18306 | `da857f37129c6d3fc87fe223efd2b37b140fbf11417c1f1bb92331d5cfa53cec` |
| `schema.json` | 3799 | `fd4412677072bf7cc6765d3c3720a2e94dbc722c62352036393c952dbe51128a` |
| `BYTE-ACCOUNTING.json` | 1600 | `c77e0667e964cb7a75ba78952f7847f4995d83fb016b775ea20ce7f6c15d1901` |

The generator has exactly one literal replacement at `source/generator.cjs:12`: `m31.body-load.input.v1/2026-10-16\0` becomes `m31.body-load.runtime-replication.v1/2026-10-16\0`. Replacing that one old literal reproduces the entire new file byte-for-byte. No geometry, permutation, motor schedule, admission, function or import changes are present. This source check did not realize either namespace's outputs.

The supervisor differs only in its first-line description and private temporary-registry prefix. The worker helpers before the async invocation are unchanged; the relocated host/config/control block is unchanged; and the complete suffix beginning at `const controlGPU={};` through numerical work, failure handling and cleanup is byte-identical to the original. These comparisons support the source-change ledger's numerical-invariance claim without re-evaluating the numerical scheme.

The unchanged config blocks are `scope`, `families`, `stopNewLaunchUTC`, `limits`, `workLimits`, `expectedGPUCosts`, `decision` and `timingComparison`. Changed config fields are status, pending parent provenance, namespace, `replicationOf` and `environmentFirst`. Node/Playwright pins are unchanged. The runtime provenance changes Chrome bundle version from `155.0.8059.40` to `155.0.8059.80` and adds the six explicit Chrome pins and Current-framework version. Those are reviewed **expected pins**, not new independent observations of the installed browser during this review.

## Environment-first admission chain

The inspected `source/experiment.cjs` order is:

1. Lines 72–79 require source identity shape, cutoff, empty raw directory, matching freeze receipt and all frozen source bytes; check six inherited Node/Playwright entry pins; and save `started.json`.
2. Line 80 obtains the explicit private executable from `RESEARCH_CHROME_EXECUTABLE` and checks the six Chrome files and Current-framework target before launch.
3. Lines 81–82 perform the only `chromium.launch` call with `executablePath:chromeExecutable`, require spawn-time browser registration, compare the actual browser-reported version with the frozen version, and repeat the Chrome inventory before opening a page.
4. Lines 83–93 route the exact saved browser/shader source bytes, create the sink, initialize the GPU, verify returned shader bytes, save capability evidence, and require `supported`, `compiled`, and clean validation/loss/uncaptured state.
5. Only at lines 94–96 are `host.cjs` and `generator.cjs` imported, `createConfig()` called, and fixed controls constructed. The first reference invocation is at line 100. Family generation begins at line 119, after the inherited shared control gate.

The unchanged `source/browser.js:41–69` requires a nonfallback adapter, adequate adapter and actual default-device limits, compilation of all three fixed entry points, and clean API state. It does not dispatch a compute batch inside initialization. Thus the new placement is browser/device/pipeline admission within the sole invocation, not an additional science rehearsal. The initial browser module's empty ledgers/counters and the source transport do not construct the scientific fixed inputs.

`source/runtime-pins.cjs:8–32` requires an absolute resolved `.../MacOS/Google Chrome` path; derives its own bundle Contents directory; resolves Current; requires both the intended framework version and exact expected versioned directory; constrains each pin and its resolved target within Contents; verifies declared shape, file length, all bytes and EOF; and closes each fd in `finally`. It uses one 1-MiB buffer with cooperative guards. The draft runtime metadata has six distinct intended entries: loader, Info.plist, versioned framework, and main/GPU/renderer helper executables. The sum is 520,899,672 bytes per successful pass, or 1,041,799,344 bytes for two passes, matching the protocol. No runtime inspection helper was invoked by this review.

The inventory remains intentionally partial. It neither inventories every browser resource/OS/driver file nor prevents later updates after the checks. The protocol states those limits. No claim of continuous runtime immutability is supported.

## Persistence, budgets and sole-attempt behavior

The existing `savePartial` helper, scientific catch sites, raw sink write/failure handling, terminal result generation and cleanup suffix are unchanged. Original generated bytes are persisted before preparation; reference/handoff outputs and available partials are retained; valid numerical mismatch dispositions can continue the remaining fixed families; integrity/control/reference/API/resource failures terminate. Raw sink failures retain the written prefix and reservation state. Worker errors record `qualified:false`, saved context/error and available browser failure state; worker cleanup remains bounded and the final file manifest records retained evidence. These are source-path findings, not proof that every OS failure can guarantee a terminal scientific JSON record.

The unchanged external `run-once.py` creates a permanent exclusive `results/sole-launch.lock` and does not retry. It propagates the private executable environment, starts the worker in its own process group, observes owned RSS, kills the owned worker group near the external cap or on output/RSS/probe failure, then verifies ownership before signaling surviving detached browser groups. It writes terminal `results/budget.json` with `retryPermitted:false` and rejects incomplete cleanup or cap violations. A hard worker kill can prevent its JavaScript `finally` from completing; the external closure remains the authority for that failure. No new liveness or unconditional partial-flush guarantee has been introduced by the replication.

The inherited limits remain 300 seconds external / 285 seconds cooperative, 30-second GPU batches, 805,306,368 raw bytes with an 8,388,608-byte failure reserve, 33,554,432 scientific-result bytes, 218,103,808 tracked live GPU-buffer bytes, sampled 4,294,967,296 owned RSS bytes, and one 120-second / 33,554,432-byte saved review. Families remain 50, 500, 5000 and 5000. Work ceilings and expected costs are identical, including three pipeline creations, six dispatches, 10,711 active / 10,944 launched invocations, and zero final live GPU bytes. Browser hashing stays inside the same time/RSS envelope and has no timing-comparison status.

## Preconditions for the later final review

- Publish and independently verify the original failed checkpoint and terminal saved review first. Keep the campaigns separate; the old attempt remains consumed.
- Resolve `parentResultCommit: PENDING_FAILURE_RESULT_PUBLICATION` to the actual original result publication commit. This placeholder is expected here and is not an approved final pin.
- Preserve the reviewed runtime partial-receipt correction and re-review any further changed source. Recheck the exhaustive diff/ledger and refresh this snapshot's hashes after modifications.
- Final adoption/allocation, complete freeze coverage, independent remote retrieval, actual explicit executable selection and the unchanged UTC launch cutoff still require their prescribed later checks. This report does not supply or weaken them.
- Do not treat current metadata as a live environment admission or a successful GPU/scientific result. Do not bind/test the original viewer before the original saved review is terminal and binding has been authorized.

## Reviewed changed-source hashes

The following table is populated from the snapshot read for this review; full JSON pins and static-check details accompany this report in `preparation/`.

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/generator.cjs` | 16923 | `10a3196aa63a081fe085ae18ad93115ce0f41e74209b35e064a1b5fa6e2ada23` |
| `source/experiment.cjs` | 21911 | `f24d4cee65e9680bd02885c86a61ea10aa2e198942ed59dd041ff687fc15c95e` |
| `source/run-once.py` | 9789 | `4f211596301b809c8caf338c0ead229fea1615c677f20271305f07a105418847` |
| `source/runtime-pins.cjs` | 3265 | `eda85d5e2eaa7d95d56102f95f0a0ef4406a64081f627ce21bd73a824948eaa2` |
| `config.json` | 3455 | `a9a36cfdfac8d0c302dc7af33c6d337f73f7bc270778b9e07df44b5b7d78b60f` |
| `runtime-provenance.json` | 3770 | `06cc95615c5a6fef66a0407f46e502132c4ad9abe9de4c3c5f85f265272ac709` |
| `PROTOCOL.md` | 5303 | `ddbe96b894cd8c281580543a43fee6638de1b664c46b64a7dcfc5d36a809b74c` |
| `SOURCE-CHANGE-LEDGER.md` | 2138 | `73e2fd3484cde54419934d9c5f6cad7edb6eadd8416770e1fad1dcb31ce0b9cb` |
| `preparation/INHERITANCE-CHECKS.json` | 1770 | `3b76cbe40456dd6bf3df5e90baa1ae2e6570bb93e92da657fcbc2ad852f48fb1` |
