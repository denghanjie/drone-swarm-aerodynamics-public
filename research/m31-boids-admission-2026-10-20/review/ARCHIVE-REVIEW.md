# Independent archival source review

20 October 2026. Decision: **PASS for the proposed one-time byte-preservation operation**, subject to the archive-source manifest/publication and closure gates below. No remaining actionable static blocker was found in the reviewed files.

This review reads source and metadata and hashes files. It does not execute the archive scripts, decompress journals, inspect/recompute scientific records, rerun the model, rerun the saved-evidence audit or operate the viewer. Only this review document is written. The prior scientific protocol review and all frozen scientific sources remain unchanged; all 39 original source-manifest file pins were independently rechecked during this review.

## Preservation design

Splitting already-produced gzip bytes is a documentary storage conversion. The original four gzip files remain present and unchanged locally. Source/archive.py opens each original read-only and writes successive numbered parts exclusively into a new archive directory. It never invokes gzip, imports scientific code or modifies the original stream. Each part is at most 32 MiB, so the four fixed originals require 18 parts with the existing byte counts. This avoids the oversized regular Git blobs while preserving every original byte.

The authoritative originals are fixed by results/index.json. The copying loop checks each entire source's byte count and SHA-256 against that index, records part order, offsets, lengths and hashes, rereads every part after writing, and independently verifies the concatenated byte count/hash against the original pin. It then rechecks the archived inputs and all archive-source manifest pins before emitting successful closure. Partial output is retained on failure. Exclusive directory/file creation and the separate supervisor launch lock prevent reuse of the same allocation.

The archive scripts are additional documentary sources and do not alter the frozen native/audit/display runner or supervisor. The internal 180-second and external 200-second bounds are separate from the previous scientific allocations. The supervisor's allocationWallPassed flag conservatively includes startup and process-group cleanup. The 520 MiB output budget is additional archival storage, with a one MiB reserve for metadata/failure closure; it is not an increase to the earlier 512 MiB native-result allowance. No speed or scientific inference follows from successful copying.

The four new ignore rules are exact root-anchored paths for the four complete gzip journals. They do not exclude archive parts or other scientific records. RECONSTRUCT.md explains the storage distinction, ordered concatenation and verification, refuses to overwrite existing evidence, and warns that a failed reconstruction leaves unverified partial output. The reader recipe performs byte copying only. Public verification of the manifest and archived mapping precedes trust in reconstructed files.

## Publication and closure requirements

Before the operation, the archive-source manifest must pin these reviewed archive scripts/documents, this review, the exact ignore-file version, authoritative results/index.json, results/launch.json, results/exit.json, native-supervisor.json, original source-manifest/source-publication, and all 39 original frozen source-file entries. The archive script rechecks its own manifest entries; inclusion of the original source closure is therefore required for the claimed original-source recheck. The parent has confirmed this coverage. The manifest must exclude the oversized full gzip blobs as actual Git files while retaining their authoritative original hashes through results/index.json.

Freeze and publish that manifest and obtain a separate exact-public verification receipt before the byte-copy allocation. This static signoff does not itself establish public availability or successful copying. It does not authorize changing any scientific source or repeating any closed scientific allocation.

After copying, final review must require archive supervisor returncode=0, no timeout, allocationWallPassed=true, archive exitCode=0/closed=true, no failure record, and total archive output within 520 MiB. Verify every part and archived original mapping against the authoritative original index. The final result manifest must include every actual part, archive/index.json, archive closure records, original results/index.json and reconstruction instructions, while explicitly excluding only the four full local journal files from its actual Git-file inventory. Do not claim those complete gzip blobs are separately present in Git. A failed or partial archive cannot be published as a verified complete preservation.

## Original journal metadata

The following values are read from the completed producer's index, not newly generated scientific evidence. Their total is 512,819,047 bytes. This review has not performed the archival concatenation operation; its identity checks are required in the declared operation and final result review.

| Original filename | Bytes | SHA-256 |
| --- | ---: | --- |
| `seed2026102001-h005.jsonl.gz` | 86333780 | `57749747201018eb47e8d4eb32625adaa8056da5a84d7bc9e97c30b4f2af95da` |
| `seed2026102001-h0025.jsonl.gz` | 170411979 | `3713e936779052b1d64cbd8fb0c75563e9d91da04a947c3e73d9f1c575f5212d` |
| `seed2026102002-h005.jsonl.gz` | 86109445 | `66064686478963e85ae6ddb570aabca246013888dc336b6f4da82e14ffcbc938` |
| `seed2026102002-h0025.jsonl.gz` | 169963843 | `0cdb3bd9c2123bac9a24b1f1e84ebd44f2db41ce2e28467a655ec805b78c0893` |

## Reviewed file identities

Paths below are repository-relative. Any change to the reviewed archive sources or instructions requires review before their separate freeze.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `research/m31-boids-admission-2026-10-20/ARCHIVE-PROTOCOL.md` | 2140 | `db2d849b0be2619627100749effaef21b62b3248731f0c4115aaa12472e36081` |
| `research/m31-boids-admission-2026-10-20/RECONSTRUCT.md` | 1963 | `166573eecf71172d1b8873a909cc317758a8b764f9b87ad99e52fc71cafe6112` |
| `research/m31-boids-admission-2026-10-20/source/archive.py` | 3413 | `e7ef182cd83bd5e032011be1bb0f0111635ac19ad2eb6359669d288985fc9c7b` |
| `research/m31-boids-admission-2026-10-20/source/archive-supervise.py` | 1037 | `b532ae9031adc3d3e9e16c882944974d8106853a6021a0d9e8762e04430ccc87` |
| `.gitignore` | 19572 | `0b015b714eea6583fa5b19eb019f5df6b8efe0e9363a4558b1b82093d1bfafad` |
| `research/m31-boids-admission-2026-10-20/results/index.json` | 89927 | `22fa1439277fadcc23a7fc545e0e189609cde507ef68551cd4de9c9488cb877d` |
