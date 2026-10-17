# Retained native-load Chrome harness — source-only draft

2026-10-17. This draft implements the adopted retained qualification stage. It has not imported a scientific module, constructed/evaluated a fixture, launched Chrome, run a native target, or executed the source packer. JavaScript syntax checks and Python AST parsing are the only executable-source checks performed here. Administrative input hashes use existing raw JSON bytes only.

## Integration

Copy `source/controller.cjs`, `source/browser.js`, `source/browser.html`, and `source/build-bundle.py` into the new package; merge `config.json` after review. The wrapper agent supplies `source/native-load.cjs`, `source/native-controls.cjs`, and the five unchanged modules under `source/vendor/`. These drafts intentionally do not duplicate the other agent's scientific sources.

The separate source packer concatenates the seven exact module byte sequences into inert CommonJS factory definitions and writes their byte offsets, sizes, hashes, and repository-relative paths. It refuses existing bundle outputs and imports/evaluates no module. It must run only as a source-packaging step before the parent freezes all sources. Its outputs are `source/browser-bundle.js` and `source/source-bundle.json`; these must be included in the source manifest alongside all component files, browser harness files, config, runtime, and the six raw inputs. The packer has not been run in this draft directory.

Controller interface:

```
PINNED_NODE source/controller.cjs REPOSITORY_ROOT SOURCE_MANIFEST_SHA256 SOURCE_COMMIT
```

The fixed package is `research/m31-native-load-baseline-2026-10-17`. Manifest paths are repository-relative. The controller checks the manifest digest and every file before loading Playwright; it checks the publication receipt against the explicit source commit/digest. It rechecks the source/input file closure after the twelve calls. The parent supervisor remains responsible for verifying publication and its prospective launch cutoff before dispatch.

Required environment values are `RESEARCH_NODE_MODULES` (parent of `playwright` and `playwright-core`), `RESEARCH_CHROME_CONTENTS` (the named Chrome application's Contents directory), `RESEARCH_BROWSER_PROFILE` (a fresh nonexistent private profile path), and `RESEARCH_PRIVATE_LOG_DIR` (an existing private directory outside the repository). There are no personal path literals in the published draft. `runtime.json` follows the parent’s reverified historical schema: Node version/size/hash, Chrome version plus selected files, Playwright version plus selected entry files, platform, and architecture.

## Source and browser boundary

One pinned Chrome launcher is permitted, with one fresh persistent profile and one page. The selected Node, Chrome, and automation runtime pins are checked before launch. Actual CDP product/version must equal `Chrome/` plus the frozen version. A scoped child-process hook permits only the pinned launcher and the single expected profile, forces `detached: false`, and privately records the original launch command, arguments, and PID. Public evidence contains counts, the hashed profile identity, sanitized arguments, and the containment flag.

The existing port-8876 server is not started or changed. Playwright routing fulfills only three pinned source files and six pinned raw JSON inputs at `http://localhost:8876`; all other requests are refused. No exact-reference document, coefficient matrix, support list, oracle root, or prior output enters the browser. The native `vendor/reference-excerpt.cjs` is the previously reviewed native formula helper; its name does not designate saved exact-reference data.

The page hashes the complete fetched source bundle and every declared byte slice before installing a Blob made from those verified bytes. Its CommonJS dependency resolver admits only the seven frozen module IDs. The inherited nine Buffer compatibility groups / 56 assertions run before any scientific factory. A durable `source-verified` journal entry precedes factory installation; a final `source` entry also records the actual factory execution order.

## Fixed schedule and evidence

The page preserves the existing 48 screen controls against the unchanged vendor F/L builders, including full symbols, positive support, prepared arrays, screen expectations, omission-symbol checks, input immutability, admitted/descending-only solve and residual, and complete F/L solution equality. The six separately paid ownership builds retain the original planes-66 outputs while checking fresh storage and immutability. Additional controls use the wrapper agent's 24 literal fixtures, declared methods/statuses and `evaluateControl` assertions; input snapshots preserve signed-zero/nonfinite words, sparse-array ownership, and ID association. Every wrapper answer is also checked for array/typed-array/ArrayBuffer aliases with the caller and with the retained previous successful answer. The previous answer is re-encoded after the next query and must be unchanged. These ownership checks run outside the query timer and create no extra query. Their `ownership` record contains `inputStorageDisjoint`, `previousResultId`, `previousResultUnchanged`, `previousStorageDisjoint`, and `pass`. A failed control is saved before stopping.

Exactly twelve target calls follow successful controls:

| State | Order |
|---|---|
| run-a-t0 | F, L |
| run-a-t5 | L, F |
| run-a-t10 | F, L |
| run-b-t0 | L, F |
| run-b-t5 | F, L |
| run-b-t10 | L, F |

Each call receives a fresh numeric decode of the same pinned 64-row raw-word input and unique stable IDs. The wrapper performs its own validation, owned copying, canonical ordering, preparation, coefficient build, ordered solve, residual, actual rounded rotor/collective/world-force/world-moment assembly, and status/ID/load consumption. The harness retains the wrapper's encoded words, preparation, coefficients/support, diagnostics, status/reason, and complete input-immutability result.

`inputFileSha256` binds the exact saved input-file bytes. `semanticInputSha256` binds compact sorted-key JSON of `{domain: "m31-moving-admission/input/v1", id, input}`, with no newline. It is independently computed from the raw JSON and case ID; this differs from the file digest. Both fields appear in the call and the evidence object. These names avoid conflating the retained reference's semantic identity with its input-file pin.

The envelope schema is `m31-native-browser-qualification-v1`; calls contain `sequence`, `caseId`, `method`, both input digests, `inputUnchanged`, `diagnosticCallMs`, and `evidence`. The evidence schema is the wrapper's `m31-native-load-evidence-v1`. Browser identity, runtime checks, source receipt, all control records, ownership records, requested target attempts, completed calls, and errors are separate fields.

Raw-file fetch, hexadecimal decoding, immutability snapshotting, evidence encoding, transport, and persistence are outside `diagnosticCallMs`. Wrapper timing begins with the current numeric rows available to its query. This stage makes no benchmark claim, performs no warmup, and repeats no target. Startup/runtime verification and the entire controller elapsed time remain separate provenance.

## Failure and resource boundaries

Before every control/target operation, an intent is synchronously journaled and fsynced by the controller. Every returned control or target result is durably journaled before evaluating the next gate. Each of the six ownership builds has its own intent and return journal entries, in addition to the final cross-call ownership report. A target's scientific `input-refused`, `domain-refused`, or `numerical-failure` outcome is retained and the fixed schedule continues; no case is replaced. A target `resource-failure`, `internal-failure`, unknown status, mutation, or unexpected exception stops the stage with partial evidence. `targetAttempts`, `unfinishedTargetAttempts`, and `unattempted` distinguish a started call with no return from a genuinely undispatched slot.

`results/browser-journal.jsonl` and `results/browser.json` use exclusive creation. The journal cap is 24 MiB, each record is capped at 2 MiB, and the final output is capped at 32 MiB. The controller has a 90-second deadline, the page has an 85-second cooperative guard, and browser closure has a three-second bound. The parent supervises the child at 120 seconds with its declared per-file/per-process limits. No aggregate-memory guarantee is claimed. If a hard process kill prevents final output, the exclusive journal and parent attempt record preserve the available partial history.

The updated parent `run.py` was inspected as source. Its retained guardian stays alive while the scientific child finishes, and the parent polls the private completion file rather than reaping the group leader before TERM/KILL. Combined with the controller's forced non-detached Chrome launch, this addresses the ordinary Playwright detached-process escape from a Node-only process group. Parent-pipe loss triggers the guardian's own group cleanup. The supervisor records cleanup issuance; neither this source review nor a controller close promise proves that every possible descendant/helper was absent. The external supervisor owns that cleanup claim and any additional inspection.

Successful controller completion means the source/runtime/control and fixed-call schedule gates completed. It does not mean native/exact compatibility or load accuracy passed. The independent saved-result checker alone makes that scientific decision using the pinned exact references, actual delivered native words, all four strict normalized error criteria, and separate F/L parity checks.

## Static validation and remaining gate

`node --check` passed for `controller.cjs` and `browser.js`; Python AST parsing passed for `build-bundle.py`. Static scans found no personal home paths or stale historical config keys. The new configuration was assembled by parsing literal control declarations and hashing existing raw input JSON, without calling a control factory. There is no numerical result in this draft.

The parent must integrate the stable wrapper/checker sources, package the bundle, finish source review and manifest/publication binding, and authorize the already bounded single-use supervisor invocation. No target or control has been executed by this subtask.
