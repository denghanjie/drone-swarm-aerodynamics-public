# Prospective Git Data API publication

This source-only preparation supports three distinct administrative publications. The helper and non-executable JSON template create no scientific result, public-verification success, publication approval, or allocation. No helper was run while preparing these files. Each actual commit requires its own publication ID, output prefix, exact protocol, independent review, and single execution. There is no automatic fallback, retry, or follow-on commit.

The helper uses only Python's standard library plus installed Git and `gh`. It does not install packages, change local branches/index/worktree, import numerical modules, run controls or audits, decode archives, benchmark, or open a UI. Reading source/input bytes for identity is not scientific parsing.

## Publication kinds and allocation boundaries

- `handoff`: records an administrative failure before any scientific or display allocation. Its parent must be the fixed published source commit `7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2`, root tree `a8e6a60e3e676224ee128562d1babbc559d7352a`. Every changed path must be under `research/publication-receipts/`, with one exact exception: `research/OVERNIGHT-RESTART.md` may receive a nonempty prepended prefix, following its newest-header-first convention. For that exception, the helper verifies the original source-parent Git blob identity, requires every original byte to remain an exact suffix, preserves its regular-file mode, and records both original and prefix identities. All frozen source/input pins remain byte-identical. No result manifest or allocation closure inside the frozen checkpoint is needed.
- `result`: uses that same fixed source parent. The producer must have a closed supervisor record; audit, finalize and UI must each be closed with pinned records or fully unstarted. Negative or failed results are permitted and retain their failures. This mode does not infer scientific success from publication success.
- `supplemental`: publishes only later administrative receipts after an actual result commit has been independently verified publicly. The supplied parent publication receipt must have `passed: true`, `closed: true`, and the exact `commit` and `tree`; its independent public-review receipt must have `passed: true`, `phase: "result"`, and the same `commit`. Changes are restricted to `research/publication-receipts/`; manifest-listed result/source files and the manifest itself cannot change. A fresh protocol and explicit action are required; publishing a result never launches this mode.

For handoff, the following paths must be absent at both start and end, relative to `research/m31-native-factor-reuse-2026-10-23/`: each of `producer-supervisor-launch.lock`, `producer-supervisor.json`, `results`, `audit-supervisor-launch.lock`, `audit-supervisor.json`, `audit`, `finalize-supervisor-launch.lock`, `finalize-supervisor.json`, `finalize`, `ui-supervisor-launch.lock`, `ui-supervisor.json`, `ui`, and `viewer/pins.json`. The receipt reports `state: "all-unstarted"`, `scientificResultExists: false`, and `administrativeFailureNotPromoted: true`.

Result/supplemental manifests must include `ALLOCATION-CLOSURE.json` with `allClosed: true`. Each present supervisor must be pinned in that manifest and have `closed: true` and an integer `returncode`. Each absent supervisor requires its matching launch lock and output directory also to be absent. The helper retains supervisor records without promoting a nonzero return code to success.

## Minimal handoff manifest

Choose a distinct output prefix under `research/publication-receipts/`. The handoff manifest can be `<outputPrefix>-manifest.json`. It is a regular JSON object with a `files` array; additional descriptive keys are allowed. Entries have `path`, `bytes`, and `sha256`. Include the unchanged source manifest and every new/modified administrative file intended for the commit; do not include the handoff manifest in its own `files` array.

```json
{
  "kind": "administrative-failure-handoff",
  "scientificResultExists": false,
  "files": [
    {
      "path": "research/m31-native-factor-reuse-2026-10-23/source-manifest.json",
      "bytes": 21212,
      "sha256": "858ba637b83da51296ffd8cc9cd4d91556de70ef568275fab144b353273eda4d"
    }
  ]
}
```

Append actual pins for the summary, restart instructions, failed acquisition receipts/journals, helper sources, review records and other intended administrative additions. The manifest itself is pinned separately by the prepare command. Every listed file must exist locally and its bytes must match the actual commit blob. Optional `--additional-pins` points to a JSON array of exact `{ "file": "repository/relative/path", "bytes": 0, "sha256": "64 lowercase hex digits" }` pins for files not in the manifest. Those pins also enter the frozen plan. All changed paths must be covered by one of these routes. Only added/modified regular files with mode `100644` or `100755` are accepted; deletions, renames and changed symlinks are rejected.

For result or supplemental mode, use the existing `research/m31-native-factor-reuse-2026-10-23/result-manifest.json` with the same `files` entry structure. Every mode must retain the source manifest and all its source/input entries unchanged; the source manifest blob is anchored to the exact parent tree.

## Offline preparation and exact review

After the actual local commit exists, invoke the helper's `prepare` subcommand with these explicit arguments: `--kind`, `--publication-id`, `--output-prefix`, `--protocol-output`, `--parent`, `--parent-tree`, `--commit`, `--manifest`, `--manifest-bytes`, and `--manifest-sha256`; optionally add `--additional-pins`. Supplemental mode also requires `--parent-publication-receipt` and `--parent-independent-review`. Paths are repository-relative. Publication IDs match `m31-native-factor-reuse-[a-z0-9-]{1,110}`. Protocol paths and output prefixes are direct children of `research/publication-receipts/` and must not collide with generated files.

Preparation is offline. It creates an exclusive plan launch lock, a retained closed plan report, the needed parent-tree reachability proof, and a protocol with `status: "awaiting-independent-review"` and `reviewed: false`. Commit/tree IDs, exact byte identities, author/committer/message metadata, changed paths, object counts, and request counts are derived from the actual commit; none are invented from this template. A preparation failure remains recorded and does not authorize an automatic reattempt.

An independent reviewer must inspect that exact plan, allocation boundary, commit, manifest, helper identity, Merkle proof, request bounds, and all prospective body identities. Record and pin that review, then set only the agreed protocol fields to `independentReviewPin`, `reviewed: true`, `status: "reviewed-ready"`, and any explicitly reviewed `priorPublicationEvidence` pins. Freeze the resulting complete protocol by SHA256. The later `publish --protocol <path> --protocol-sha256 <exact reviewed hash>` call is a separately authorized `require_escalated` operation. The template itself cannot run.

Preparation and publication receipts describe events after the target commit exists. They therefore need not belong to that same commit. Do not rewrite the frozen target to insert self-referential publication evidence. A later receipt-only commit, if separately authorized, uses a fresh supplemental context and the independently verified actual result parent.

## Parent blob reuse and exact API objects

For each changed content OID already in the exact parent tree, preparation selects a parent witness path and reconstructs every necessary Git tree object from metadata. It computes each Git SHA1 and verifies the path from the fixed parent root to the reused leaf. No blob content is semantically interpreted. During publication, a fresh remote GET of the parent commit must confirm the same root tree. These Merkle paths establish reachability without one HTTP request per reused blob. Unique new OIDs are uploaded once even when several paths share them.

The API tree uses the exact parent root as `base_tree` plus every changed path/mode/OID. Its returned SHA must equal the actual local commit's root tree. The commit body preserves the exact UTF-8 newline-terminated message, parent, author/committer names/emails, epoch and timezone. The API-created commit SHA/tree/parent must match the local object before any branch update. Initial and immediate pre-update reference reads require the exact parent. The branch update uses `force: false`; a reserved final read records the actual branch state. The API does not provide compare-and-swap for refs, so a concurrent move remains a residual race after the immediate precheck; the helper uses no force update or retry.

## Bounds, failures, and closure

The successful request count is `unique new blobs + 8`, with one request for repository metadata, initial ref, parent commit, each new blob, tree, commit, pre-update ref, reference PATCH, and final ref. Exact outbound body bytes are calculated before publication, including base64 expansion. Limits are frozen in the template/helper: 1,800 seconds overall, 180 seconds per request, 256 requests, one concurrent request, one attempt per mutation/read, 512 MiB outbound payload total, 160 MiB per request, 100 MiB per changed blob, 768 MiB changed local bytes, 64 MiB captured responses, 80 MiB saved evidence, 16 KiB per event, 8 MiB final receipt, and 64 MiB/45 seconds per bounded Git metadata operation (64 MiB is aggregate). Final observation reserves 180 seconds and closure reserves 10 seconds.

The helper writes a request intent before dispatch and saves bounded stdout/stderr with original identities and credential-pattern redaction. Failed or unknown mutation outcomes are preserved without retry. A final target ref after an unknown PATCH does not erase the original failure. Closure rechecks the exact protocol, helper, review, reachability proof, manifest snapshot, source/input identities, commit object and allocation boundary. It retains final-reference errors and closure failures separately. Public byte-identity verification is a separate action and is never inferred from API publication success.
