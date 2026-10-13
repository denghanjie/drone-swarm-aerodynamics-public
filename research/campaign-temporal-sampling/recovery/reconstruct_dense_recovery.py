#!/usr/bin/env python3
"""Recovery-authored, offline-only transport verifier/reconstructor (2026-10-13).

This is a new replacement for an unavailable archival utility. It performs no
simulation, decompression, download, or numerical interpretation. Requires POSIX
directory-fd and O_NOFOLLOW support. Use a trusted local directory without
concurrent writers. Every output is installed atomically without overwriting.
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
SCHEMA = "temporal-airflow-recovery-v1"


def require_posix():
    if os.name != "posix" or not all(hasattr(os, n) for n in ("O_NOFOLLOW", "O_DIRECTORY")):
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


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise Refused("unsupported recovery manifest schema")
    entries = manifest.get("git_objects")
    outputs = manifest.get("dense_outputs")
    if not isinstance(entries, list) or not entries or not isinstance(outputs, list) or not outputs:
        raise Refused("manifest needs nonempty git_objects and dense_outputs arrays")
    if exact_int(manifest.get("expected_object_count"), "expected_object_count") != len(entries):
        raise Refused("Git object count differs from manifest")
    by_path = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise Refused("invalid Git object entry")
        name = entry.get("path")
        relative_parts(name)
        if name in by_path:
            raise Refused(f"duplicate Git object path: {name}")
        exact_int(entry.get("bytes"), "Git object bytes")
        digest(entry.get("git_blob_sha1"), 40, "Git blob SHA-1")
        by_path[name] = entry
    destinations = set()
    used_parts = set()
    for output in outputs:
        if not isinstance(output, dict):
            raise Refused("invalid output entry")
        name = output.get("path")
        relative_parts(name)
        if name in by_path or name in destinations:
            raise Refused(f"output overlaps an input or another output: {name}")
        destinations.add(name)
        size = exact_int(output.get("bytes"), "output bytes")
        digest(output.get("compressed_sha256"), 64, "compressed SHA-256")
        digest(output.get("git_blob_sha1"), 40, "dense Git blob SHA-1")
        parts = output.get("parts")
        if not isinstance(parts, list) or len(parts) < 2:
            raise Refused("each dense output needs an explicit ordered part list")
        for part in parts:
            relative_parts(part)
            if part not in by_path or part in used_parts:
                raise Refused(f"missing or repeated part identity: {part}")
            used_parts.add(part)
        if sum(by_path[p]["bytes"] for p in parts) != size:
            raise Refused(f"part sizes do not sum to output bytes: {name}")
    names = set(by_path) | destinations
    for name in names:
        segments = name.split("/")
        if any("/".join(segments[:i]) in names for i in range(1, len(segments))):
            raise Refused(f"a file path is an ancestor of another file: {name}")
    return by_path


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


def verify_git_object(root_fd, entry, sink=None, whole_hashes=()):
    parent_fd, name = open_parent(root_fd, entry["path"])
    try:
        fd = open_regular(parent_fd, name)
        try:
            hasher = hashlib.sha1(b"blob " + str(entry["bytes"]).encode("ascii") + b"\0")
            hashers = [hasher, *whole_hashes]
            read_and_hash(fd, entry["bytes"], hashers, sink)
            if hasher.hexdigest() != entry["git_blob_sha1"]:
                raise Refused(f"Git blob SHA-1 mismatch: {entry['path']}")
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def dense_hashers(output):
    return (hashlib.sha256(), hashlib.sha1(b"blob " + str(output["bytes"]).encode("ascii") + b"\0"))


def check_dense_hashes(hashers, output):
    sha256, git_sha1 = (h.hexdigest() for h in hashers)
    if sha256 != output["compressed_sha256"] or git_sha1 != output["git_blob_sha1"]:
        raise Refused(f"dense compressed SHA-256 or Git blob SHA-1 mismatch: {output['path']}")
    return {"path": output["path"], "bytes": output["bytes"],
            "compressed_sha256": sha256, "git_blob_sha1": git_sha1}


def stream_dense(root_fd, output, by_path, sink=None):
    hashers = dense_hashers(output)
    for part in output["parts"]:
        verify_git_object(root_fd, by_path[part], sink, hashers)
    return check_dense_hashes(hashers, output)


def verify_existing(parent_fd, name, output):
    try:
        fd = open_regular(parent_fd, name)
    except FileNotFoundError:
        return False
    try:
        hashers = dense_hashers(output)
        read_and_hash(fd, output["bytes"], hashers)
        check_dense_hashes(hashers, output)
        return True
    finally:
        os.close(fd)


def reconstruct_one(root_fd, output, by_path):
    parent_fd, name = open_parent(root_fd, output["path"])
    temp = None
    try:
        if verify_existing(parent_fd, name, output):
            return {"path": output["path"], "status": "existing_verified"}
        candidate = ".dense-recovery-" + uuid.uuid4().hex + ".tmp"
        fd = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent_fd)
        temp = candidate
        with os.fdopen(fd, "wb") as sink:
            # Reverify while copying: a preliminary verification is no substitute.
            identity = stream_dense(root_fd, output, by_path, sink)
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
    by_path = validate_manifest(manifest)
    root_fd = open_directory_path(root)
    try:
        for entry in manifest["git_objects"]:
            verify_git_object(root_fd, entry)
        # Also verify the original joined identities, even when no output is written.
        dense_streams = [stream_dense(root_fd, output, by_path)
                         for output in manifest["dense_outputs"]]
        # Reject known destination problems before creating any output.
        for output in manifest["dense_outputs"]:
            parent_fd, name = open_parent(root_fd, output["path"])
            try:
                verify_existing(parent_fd, name, output)
            finally:
                os.close(parent_fd)
        results = [] if verify_only else [
            reconstruct_one(root_fd, output, by_path) for output in manifest["dense_outputs"]
        ]
        return {"authorship": "recovery-authored replacement utility",
                "status": "verified_only" if verify_only else "reconstruction_complete",
                "git_objects_verified": len(by_path), "dense_streams_verified": dense_streams,
                "outputs": results,
                "parts_preserved": True, "numerical_computation_performed": False}
    finally:
        os.close(root_fd)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root containing all 17 retained Git objects")
    parser.add_argument("--manifest", default=str(Path(__file__).absolute().with_name("raw-recovery-manifest.json")))
    parser.add_argument("--verify-only", action="store_true", help="verify inputs, joined dense identities and any existing outputs; create nothing")
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
