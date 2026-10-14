#!/usr/bin/env python3
"""Offline exact-byte verifier/reconstructor for the joint-stage checkpoint.

Adapted from the recovery-authored POSIX transport helper on 2026-10-14.
It performs no simulation, download, or numerical interpretation. Raw .f64
parts are joined without changing their bytes. Requires POSIX directory-fd,
O_NOFOLLOW, and hard-link support. Use a trusted checkout without concurrent
writers. Each reconstructed file is installed atomically without overwriting;
the set of files is not a single atomic transaction.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid


class Refused(ValueError):
    """An input, identity, or destination cannot be accepted safely."""


BLOCK = 1024 * 1024
SCHEMA = "joint-stage-binary-transport/v1"
MAX_OBJECT_BYTES = 8_000_000
DIR_FD_SUPPORTED = all(fn in os.supports_dir_fd for fn in (os.open, os.link, os.unlink))


def require_posix():
    if (os.name != "posix"
            or not all(hasattr(os, n) for n in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK"))
            or not DIR_FD_SUPPORTED):
        raise Refused("POSIX O_NOFOLLOW and directory-fd support are required")


def relative_parts(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise Refused("manifest paths must be nonempty, relative POSIX paths")
    parts = value.split("/")
    if any(p in ("", ".", "..") or not re.fullmatch(r"[A-Za-z0-9_.-]+", p) for p in parts):
        raise Refused(f"unsafe manifest path: {value!r}")
    return parts


def exact_int(value, label):
    if type(value) is not int or value < 0:
        raise Refused(f"{label} must be a nonnegative integer")
    return value


def digest(value, length, label):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{%d}" % length, value):
        raise Refused(f"invalid {label}")
    return value


def validate_identity(entry, label):
    if not isinstance(entry, dict):
        raise Refused(f"invalid {label} entry")
    exact_int(entry.get("bytes"), f"{label} bytes")
    digest(entry.get("sha256"), 64, f"{label} SHA-256")
    digest(entry.get("gitSha"), 40, f"{label} Git blob SHA-1")


def validate_manifest(manifest):
    """Validate the complete inventory before opening any manifest-named path.

    localPath is provenance only. All actual I/O uses logicalPath or object.path,
    relative to the supplied repository root; no local path remapping occurs.
    """
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise Refused("unsupported binary transport manifest schema")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise Refused("manifest needs a nonempty files array")
    if exact_int(manifest.get("logicalFiles"), "logicalFiles") != len(files):
        raise Refused("logical file count differs from manifest")
    by_path = {}
    logical_paths = set()
    outputs = []
    for logical in files:
        validate_identity(logical, "logical file")
        name = logical.get("logicalPath")
        relative_parts(name)
        if name in logical_paths:
            raise Refused(f"duplicate logical file path: {name}")
        logical_paths.add(name)
        mode = logical.get("mode")
        objects = logical.get("objects")
        if mode not in ("whole", "parts") or not isinstance(objects, list) or not objects:
            raise Refused("logical file needs a whole/parts mode and a nonempty objects array")
        if mode == "whole" and len(objects) != 1:
            raise Refused("whole mode requires exactly one object")
        if mode == "parts" and len(objects) < 2:
            raise Refused("parts mode requires at least two ordered objects")
        offset = 0
        for entry in objects:
            validate_identity(entry, "transport object")
            part = entry.get("path")
            relative_parts(part)
            if part in by_path:
                raise Refused(f"duplicate transport object path: {part}")
            if exact_int(entry.get("offset"), "object offset") != offset:
                raise Refused(f"nonconsecutive or reordered object offset: {part}")
            if entry["bytes"] > MAX_OBJECT_BYTES:
                raise Refused(f"transport object exceeds 8,000,000 bytes: {part}")
            if mode == "parts" and entry["bytes"] == 0:
                raise Refused(f"split object must not be empty: {part}")
            offset += entry["bytes"]
            by_path[part] = entry
        if offset != logical["bytes"]:
            raise Refused(f"object sizes do not sum to logical file bytes: {name}")
        if mode == "whole":
            entry = objects[0]
            if entry["path"] != name or any(entry[k] != logical[k] for k in ("bytes", "sha256", "gitSha")):
                raise Refused(f"whole object identity differs from logical file: {name}")
        else:
            outputs.append({"path": name, "bytes": logical["bytes"],
                            "sha256": logical["sha256"], "gitSha": logical["gitSha"],
                            "parts": [entry["path"] for entry in objects]})
    if exact_int(manifest.get("storedObjects"), "storedObjects") != len(by_path):
        raise Refused("transport object count differs from manifest")
    if exact_int(manifest.get("logicalBytes"), "logicalBytes") != sum(f["bytes"] for f in files):
        raise Refused("logical byte total differs from manifest")
    for output in outputs:
        if output["path"] in by_path:
            raise Refused(f"split output overlaps a transport object: {output['path']}")
    names = set(by_path) | logical_paths
    for name in names:
        segments = name.split("/")
        if any("/".join(segments[:i]) in names for i in range(1, len(segments))):
            raise Refused(f"a file path is an ancestor of another file: {name}")
    return by_path, outputs


def open_directory_path(value):
    """Open a root/manifest directory, rejecting symlinks in every component."""
    value = os.fspath(value)
    if not value or "\x00" in value or "\\" in value:
        raise Refused("unsafe local directory path")
    raw_parts = value.split("/")
    if ".." in raw_parts:
        raise Refused("parent traversal is not allowed in local paths")
    if not os.path.isabs(value):
        raw_parts = os.getcwd().split("/") + raw_parts
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in raw_parts:
            if part in ("", "."):
                continue
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def open_parent(root_fd, relative):
    parts = relative_parts(relative)
    fd = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd, parts[-1]
    except BaseException:
        os.close(fd)
        raise


def open_regular(parent_fd, name):
    # NONBLOCK avoids hanging if a path has been replaced with a FIFO.
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise Refused(f"not a regular file: {name}")
    return fd


def load_manifest(path):
    value = os.fspath(path)
    if ".." in value.split("/") or "\\" in value:
        raise Refused("unsafe manifest filename")
    parent, name = os.path.split(value)
    if not name or name in (".", ".."):
        raise Refused("manifest must name a regular JSON file")
    parent_fd = open_directory_path(parent or ".")
    try:
        fd = open_regular(parent_fd, name)
        with os.fdopen(fd, "r", encoding="utf-8") as stream:
            def no_duplicate_keys(pairs):
                result = {}
                for key, val in pairs:
                    if key in result:
                        raise Refused(f"duplicate JSON key: {key}")
                    result[key] = val
                return result
            manifest = json.load(stream, object_pairs_hook=no_duplicate_keys)
    finally:
        os.close(parent_fd)
    validate_manifest(manifest)
    return manifest


def fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def read_and_hash(fd, expected_size, hashers, sink=None):
    before = os.fstat(fd)
    if before.st_size != expected_size:
        raise Refused(f"byte size mismatch: expected {expected_size}, found {before.st_size}")
    count = 0
    while True:
        chunk = os.read(fd, BLOCK)
        if not chunk:
            break
        count += len(chunk)
        if count > expected_size:
            raise Refused("file grew while being read")
        for hasher in hashers:
            hasher.update(chunk)
        if sink is not None:
            sink.write(chunk)
    if count != expected_size or fingerprint(before) != fingerprint(os.fstat(fd)):
        raise Refused("file changed while being read")


def verify_transport_object(root_fd, entry, sink=None, whole_hashes=()):
    parent_fd, name = open_parent(root_fd, entry["path"])
    try:
        fd = open_regular(parent_fd, name)
        try:
            sha256 = hashlib.sha256()
            git_sha1 = hashlib.sha1(b"blob " + str(entry["bytes"]).encode("ascii") + b"\0")
            read_and_hash(fd, entry["bytes"], [sha256, git_sha1, *whole_hashes], sink)
            if sha256.hexdigest() != entry["sha256"]:
                raise Refused(f"transport object SHA-256 mismatch: {entry['path']}")
            if git_sha1.hexdigest() != entry["gitSha"]:
                raise Refused(f"transport object Git blob SHA-1 mismatch: {entry['path']}")
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def file_hashers(output):
    return (hashlib.sha256(), hashlib.sha1(b"blob " + str(output["bytes"]).encode("ascii") + b"\0"))


def check_file_hashes(hashers, output):
    sha256, git_sha1 = (h.hexdigest() for h in hashers)
    if sha256 != output["sha256"] or git_sha1 != output["gitSha"]:
        raise Refused(f"joined file SHA-256 or Git blob SHA-1 mismatch: {output['path']}")
    return {"path": output["path"], "bytes": output["bytes"],
            "sha256": sha256, "gitSha": git_sha1}


def stream_parts(root_fd, output, by_path, sink=None):
    hashers = file_hashers(output)
    for part in output["parts"]:
        verify_transport_object(root_fd, by_path[part], sink, hashers)
    return check_file_hashes(hashers, output)


def verify_existing(parent_fd, name, output):
    try:
        fd = open_regular(parent_fd, name)
    except FileNotFoundError:
        return False
    try:
        hashers = file_hashers(output)
        read_and_hash(fd, output["bytes"], hashers)
        check_file_hashes(hashers, output)
        return True
    finally:
        os.close(fd)


def reconstruct_one(root_fd, output, by_path):
    parent_fd, name = open_parent(root_fd, output["path"])
    temp = None
    try:
        if verify_existing(parent_fd, name, output):
            return {"path": output["path"], "status": "existing_verified"}
        candidate = ".checkpoint-reconstruction-" + uuid.uuid4().hex + ".tmp"
        fd = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent_fd)
        temp = candidate
        with os.fdopen(fd, "wb") as sink:
            # Reverify while copying: a preliminary verification is no substitute.
            identity = stream_parts(root_fd, output, by_path, sink)
            sink.flush()
            os.fsync(sink.fileno())
            if os.fstat(sink.fileno()).st_size != output["bytes"]:
                raise Refused(f"reconstructed byte size mismatch: {output['path']}")
        try:
            # Hard-link installation is atomic and refuses to replace any destination.
            os.link(temp, name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd,
                    follow_symlinks=False)
            status = "reconstructed_verified"
        except FileExistsError:
            if not verify_existing(parent_fd, name, output):
                raise Refused("destination changed during installation")
            status = "concurrently_created_verified"
        os.fsync(parent_fd)
        return {**identity, "status": status}
    finally:
        if temp is not None:
            try:
                os.unlink(temp, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
        os.close(parent_fd)


def recover(root, manifest, verify_only=False):
    require_posix()
    by_path, outputs = validate_manifest(manifest)
    root_fd = open_directory_path(root)
    try:
        for entry in by_path.values():
            verify_transport_object(root_fd, entry)
        # Check joined identities even when no reconstructed file is written.
        joined_streams = [stream_parts(root_fd, output, by_path) for output in outputs]
        # Reject all known destination problems before creating any output.
        for output in outputs:
            parent_fd, name = open_parent(root_fd, output["path"])
            try:
                verify_existing(parent_fd, name, output)
            finally:
                os.close(parent_fd)
        results = [] if verify_only else [
            reconstruct_one(root_fd, output, by_path) for output in outputs
        ]
        return {"schema": "joint-stage-binary-verification-report/v1",
                "status": "verified_only" if verify_only else "reconstruction_complete",
                "logical_files_verified": len(manifest["files"]),
                "logical_bytes_verified": manifest["logicalBytes"],
                "transport_objects_verified": len(by_path),
                "joined_streams_verified": joined_streams, "outputs": results,
                "parts_preserved": True, "numerical_computation_performed": False}
    finally:
        os.close(root_fd)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="downloaded repository root containing every manifest transport object")
    parser.add_argument("--manifest", default=str(Path(__file__).absolute().with_name("BINARY-TRANSPORT-MANIFEST.json")))
    parser.add_argument("--verify-only", action="store_true", help="verify inputs, joined raw-byte identities and any existing outputs; create nothing")
    args = parser.parse_args(argv)
    try:
        require_posix()
        result = recover(args.root, load_manifest(args.manifest), args.verify_only)
    except (OSError, ValueError, TypeError) as exc:
        print(f"reconstruction refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
