"""Pure byte-evidence predicates; no filesystem, browser or source execution."""

import hashlib


def byte_array(value, length=3840):
    """Decode only a JSON array of exact Python ints in the byte range."""
    if type(value) is not list:
        raise ValueError("returned payload must be a JSON array")
    if len(value) != length:
        raise ValueError("returned payload length must equal fixture length")
    if any(type(item) is not int or not 0 <= item <= 255 for item in value):
        raise ValueError("returned payload entries must be integer bytes")
    return bytes(value)


def compare_bytes(returned_array, persisted_bytes, fixture_bytes):
    """Separate actual evidence agreement from expected fixture equality."""
    if type(persisted_bytes) is not bytes or type(fixture_bytes) is not bytes:
        raise ValueError("persisted and fixture evidence must be bytes")
    returned_bytes = byte_array(returned_array, len(fixture_bytes))
    return {
        "returned_sha256": hashlib.sha256(returned_bytes).hexdigest(),
        "persisted_sha256": hashlib.sha256(persisted_bytes).hexdigest(),
        "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "persisted_matches_returned": persisted_bytes == returned_bytes,
        "returned_matches_fixture": returned_bytes == fixture_bytes,
        "persisted_matches_fixture": persisted_bytes == fixture_bytes,
    }
