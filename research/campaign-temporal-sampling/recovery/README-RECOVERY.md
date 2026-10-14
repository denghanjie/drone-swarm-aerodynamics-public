# Temporal airflow campaign: recovery checkpoint

This is a **post-workspace-loss recovery checkpoint**, prepared on 2026-10-13. It preserves surviving evidence and labels newly authored recovery material. It is not the complete original final package.

The historical scientific conclusion is unchanged: both airflow-reference screens failed, and no airflow cadence was qualified or recommended. Recovery did not rerun the campaign, replay diagnostics, or raw-array gate calculations.

Read [RETENTION-ADDENDUM.md](RETENTION-ADDENDUM.md) alongside the historical report. In particular, the report's complete-retention statements describe its pre-loss workspace context; they do not describe the completeness of this recovered package.

## New transport utility

`reconstruct_dense_recovery.py` and `raw-recovery-manifest.json` are explicitly new recovery-authored replacements. The original `coordination/packaging/reconstruct_dense.py` and `coordination/dense-transport-parts.json` have not been recovered.

The manifest inventories all 17 uploaded Git objects: 13 whole gzip files and four ordered parts for two dense gzip files. Keep the objects at their exact repository-relative paths. Obtain them separately through an authorized route; the utility has no network access or download feature.

From the directory containing this utility and its manifest, verify without creating dense files:

```sh
python3 reconstruct_dense_recovery.py --root /path/to/repository --verify-only
```

To verify and reconstruct the two dense gzip files:

```sh
python3 reconstruct_dense_recovery.py --root /path/to/repository
```

Both modes verify all 17 input sizes and Git blob SHA-1 identities. They also stream each ordered dense pair to verify the original whole compressed SHA-256 and whole Git blob SHA-1, even when no dense destination exists. Reconstruction verifies the parts again while copying. No decompression or numerical calculation occurs.

- Requires Python 3.9+ on a POSIX filesystem with directory-fd and `O_NOFOLLOW` support; tested with Python 3.12.14 on Linux.
- Use a trusted local directory without concurrent writers. Paths and all directory components must be free of symlinks. Manifest paths must be relative, without parent traversal.
- All 17 input files and output parent directories must already exist. Incomplete downloads are rejected before reconstruction.
- Existing destinations must match original size, SHA-256, and Git identity. Mismatches are rejected and never overwritten. Matching files are left untouched.
- New files are staged locally and installed atomically without replacing an existing destination. Installation is atomic per file, not a multi-file transaction. An interruption can leave an already verified dense output or a temporary file; a later run verifies existing outputs before continuing.
- Parts are preserved. The utility never repairs, deletes, or edits input blobs.
- A successful check confirms transport identities, not physical validity, model accuracy, or cadence qualification. It does not restore the missing records listed in the addendum.

## Verification performed during recovery

`test_reconstruct_dense_recovery.py` uses only tiny synthetic files plus manifest metadata. It covers correct reconstruction, read-only joined verification, wrong hashes/sizes/order, missing input, repeated runs, mismatched existing outputs, symlinks, path traversal, FIFOs, mutation after precheck, installation collisions, and preserving unrelated temporary files. The captured result is `synthetic-test-results.txt`.

```sh
python3 test_reconstruct_dense_recovery.py
```

At preparation time, **27 tests passed**. No original raw payload was downloaded, concatenated, decompressed, or numerically evaluated in those tests. Original binary-content verification remains a separate step when the retained objects are materialized.
