# Exact-byte checkpoint reconstruction

This directory contains an offline verifier/reconstructor for
`BINARY-TRANSPORT-MANIFEST.json`, schema `joint-stage-binary-transport/v1`.
The manifest describes 52 logical binary files, 54 transport objects, and
58,664,800 logical bytes. Fifty files are stored whole. Two raw `.dense.f64`
arrays are stored as consecutive parts of 8,000,000 and 5,928,576 bytes.
Reconstruction concatenates those bytes; it does not interpret floating-point
values, rerun a model, compress, or decompress anything.

## Run from a downloaded public repository root

Use a complete checkout of a trusted, pinned checkpoint commit. The repository
root is the directory containing `research/`, not this `archive/` directory.
Python 3.8 or newer and a POSIX filesystem with directory-fd, `O_NOFOLLOW`, and
hard-link support are required. No third-party packages, Git command, network
access, or credentials are required by the helper.

First verify every downloaded object and the two joined byte streams without
creating reconstructed files:

```sh
python3 -B research/campaign-joint-stage-reference/archive/reconstruct_binary_checkpoint.py --root . --verify-only
```

Then reconstruct the two missing logical files in their original paths:

```sh
python3 -B research/campaign-joint-stage-reference/archive/reconstruct_binary_checkpoint.py --root .
```

The helper loads the manifest next to its own script by default. An explicit
`--manifest PATH` can select a different manifest. Every `objects[].path` and
`logicalPath` is relative to `--root`; `localPath` is provenance metadata and is
never used for filesystem access.

Both commands print a JSON report and exit with code 0 on success, including
`logical_files_verified: 52`, `transport_objects_verified: 54`, and two
`joined_streams_verified` entries. A missing object, malformed manifest, unsafe
path, size mismatch, or hash mismatch prints `reconstruction refused:` to
standard error and exits with code 2. A successful verification establishes
integrity against the supplied manifest; it does not authenticate the publisher.

The reconstructed files are:

- `research/campaign-joint-stage-reference/implementation/results/raw/s840131-J3.dense.f64`
  - Bytes: `13928576`
  - SHA-256: `dbc554ed5e5f7056985a07b332afa788c7de7dfd10257507e0378c069c476ed5`
  - Git blob SHA-1: `acfd4e7f7e1dec15fdf4fc5aa26bf21789350366`
- `research/campaign-joint-stage-reference/implementation/results/raw/s840137-J3.dense.f64`
  - Bytes: `13928576`
  - SHA-256: `95fa467cd439c43afe2d8f0d4d75e1812c42bf862c38bba398ae509d5312d4b8`
  - Git blob SHA-1: `37fc384b3478b580ea25055369a15c6572a58b9c`

## Safety and disk use

- Checks all 54 object sizes, SHA-256 values, and Git blob SHA-1 identities.
  Git blob identity hashes `blob <decimal byte count>\0` followed by file bytes.
- Validates logical counts, byte totals, ordered contiguous part offsets,
  unique paths, file/ancestor collisions, and whole-file/object agreement.
- Verifies each joined stream's original size and both hashes, including in
  `--verify-only` mode. Parts are checked again while copying.
- Rejects symlinks in the root, manifest, input, destination, and their path
  components; rejects traversal, absolute manifest paths, and nonregular files.
- Never overwrites an existing destination. A matching regular file is verified
  and retained; a nonmatching file, directory, or symlink is refused.
- Checks every known destination before creating any output. Each missing file
  is written to a private temporary file, flushed, and installed by an atomic
  no-overwrite hard link. A later failure can leave earlier verified files in
  place: the two-file operation is not a single transaction. Rerunning is safe.
- Keeps all downloaded transport objects. Two reconstructed files require
  27,857,152 additional bytes, plus small filesystem overhead. Streaming uses
  1 MiB blocks. The temporary file becomes the installed output by hard link,
  so it does not require a second complete output copy.
- Use a trusted local checkout without concurrent writers. This is not a
  sandbox against an attacker modifying the checkout during execution. Normal
  exceptions remove the helper's temporary file; forcible termination may
  leave a `.checkpoint-reconstruction-*.tmp` file for manual inspection.

## Tests and verification limits

From the same repository root:

```sh
python3 -B research/campaign-joint-stage-reference/archive/test_reconstruct_binary_checkpoint.py
```

The 45 tests use tiny temporary byte strings and the manifest's metadata.
They cover exact reconstruction and reruns; independent SHA-256 and Git blob
checks; corruption, truncation, trailing bytes, and missing input; reordered
parts and invalid offsets; traversal and path collisions; symlinks and FIFOs;
existing destinations; changes during reads; install races; temporary-file
collisions; duplicate JSON keys; and CLI exit codes. Temporary fixtures are
removed after each test. No historical arrays are copied or used in a numerical
experiment by this test suite.

`synthetic-test-results.txt` records the test run and a separate read-only
local-source identity audit. That audit checks original logical files and each
manifest byte slice without writing part files. These are local checks, not a
claim that a downloaded public checkout was tested. Publication receipts and
remote-tree verification are separate evidence.

Successful byte recovery does not change the checkpoint's scientific status:
the run stopped at its per-job cooperative time cap and did not qualify a
reference result.
