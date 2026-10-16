#!/usr/bin/env python3
"""Independent coupled-load saved-result checker; source-authored, not pre-run.

The byte-identical published pair reference is loaded only by main after local
manifest verification. Its old case generator/main/controls are never invoked.
No candidate implementation, child process or network operation is used.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path, PurePosixPath
import re
import sys

MAX_INPUT_BYTES = 32 * 1024 * 1024
MAX_REPORT_BYTES = MAX_INPUT_BYTES - 65536
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_SPEC_BYTES = 256 * 1024
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_SOURCE_TOTAL = 64 * 1024 * 1024
MAX_SOURCE_FILES = 256
MAX_ERRORS = 48

class CheckError(Exception):
    """An intentionally public-safe validation failure."""


def require(condition, code):
    if not condition:
        raise CheckError(code)


def canonical_integer(value):
    require(isinstance(value, str) and len(value) <= 128,
            "endpoint-string-shape")
    require(re.fullmatch(r"0|-?[1-9][0-9]*", value) is not None,
            "endpoint-string-syntax")
    return int(value)


def pairs_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate-json-key")
        result[key] = value
    return result


def reject_json_constant(_value):
    raise CheckError("nonfinite-json-number")


def same_json(left, right):
    """Structural equality without Python's True == 1 or 1.0 == 1 aliases."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_json(a, b) for a, b in zip(left, right))
    return left == right


def load_json(path, limit):
    require(path.is_file(), "required-file-missing")
    require(path.stat().st_size <= limit, "input-file-budget")
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    require(len(data) <= limit, "input-file-budget")
    try:
        return json.loads(data, object_pairs_hook=pairs_without_duplicates,
                          parse_constant=reject_json_constant)
    except (UnicodeError, ValueError, RecursionError):
        raise CheckError("invalid-json") from None


def relative_name(path, root):
    try:
        relative = path.resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        raise CheckError("input-path-outside-root-or-missing") from None
    require(relative.parts and not any(p in (".", "..") for p in relative.parts),
            "invalid-relative-path")
    return relative.as_posix()


def file_sha256(path, limit=MAX_SOURCE_BYTES):
    h = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            total += len(block)
            require(total <= limit, "source-file-budget")
            h.update(block)
    return total, h.hexdigest()


def verify_manifest(manifest_path, root, spec_path, contract_path):
    manifest = load_json(manifest_path, MAX_MANIFEST_BYTES)
    require(isinstance(manifest, dict), "manifest-object-required")
    files = manifest.get("files")
    require(isinstance(files, list) and 1 <= len(files) <= MAX_SOURCE_FILES,
            "manifest-file-count")
    seen = set()
    verified = []
    total = 0
    for item in files:
        require(isinstance(item, dict), "manifest-record-object")
        name = item.get("path")
        require(isinstance(name, str) and len(name) <= 512 and "\\" not in name,
                "manifest-path-shape")
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and str(parts) == name and
                all(part not in (".", "..") for part in parts.parts),
                "manifest-path-not-relative")
        require(name not in seen, "duplicate-manifest-path")
        seen.add(name)
        size = item.get("bytes")
        expected_sha = item.get("sha256")
        require(type(size) is int and 0 <= size <= MAX_SOURCE_BYTES,
                "manifest-size-shape")
        require(isinstance(expected_sha, str) and
                re.fullmatch(r"[0-9a-f]{64}", expected_sha) is not None,
                "manifest-hash-shape")
        source_path = root / name
        require(relative_name(source_path, root) == name,
                "manifest-noncanonical-file-path")
        actual_size, actual_sha = file_sha256(source_path)
        total += actual_size
        require(total <= MAX_SOURCE_TOTAL, "source-total-budget")
        require(actual_size == size and actual_sha == expected_sha,
                "source-manifest-pin-mismatch")
        verified.append({"path": name, "bytes": size, "sha256": actual_sha})
    require(relative_name(spec_path, root) in seen, "spec-not-source-pinned")
    require(relative_name(contract_path, root) in seen,
            "result-contract-not-source-pinned")
    require(relative_name(Path(__file__), root) in seen,
            "checker-not-source-pinned")
    return verified


class PublicArgumentParser(argparse.ArgumentParser):
    def error(self, _message):
        raise CheckError("invalid-command-line")
