#!/usr/bin/env python3
"""Materialize four immutable transport parts and two verified dense byte arrays.

This is a new input-acquisition receipt generator, not original campaign code.
It performs hashing and gzip decoding only. It does not interpret Float64 values,
evaluate fields, integrate trajectories, replay diagnostics, or run a simulation.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import time
import zlib

WORKSPACE = Path(__file__).absolute().parent.parent
ROOT = WORKSPACE / "research-next" / "inputs"
COMMIT = "b9bd5065d02561920af27468f5e4740b301bd174"
REPO = "denghanjie/drone-swarm-aerodynamics-public"
RECOVERY = WORKSPACE / "research-recovery"
PART_IDENTITIES = {
    "s840131-p1-a4.dense.f64.gz.part01": (6750000, "74f57f04697daa786d6ab635f006abf3dd142db5"),
    "s840131-p1-a4.dense.f64.gz.part02": (6621234, "e6e846722cbac148050d35fd35aee7e22149755e"),
    "s840137-p1-a4.dense.f64.gz.part01": (6750000, "dfd2c004c0ffabee49d7acef5e9b02bf30d827aa"),
    "s840137-p1-a4.dense.f64.gz.part02": (6615454, "e531ca472003b42270a97f5827d6096ea25dfc02"),
}


def regular(path):
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"not a regular nonsymlink file: {path}")


def file_identity(path):
    regular(path)
    size = path.stat().st_size
    git = hashlib.sha1(b"blob " + str(size).encode() + b"\0")
    sha = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            git.update(chunk)
            sha.update(chunk)
    return {"bytes": size, "git_blob_sha1": git.hexdigest(), "sha256": sha.hexdigest()}


def save_receipt(receipt):
    target = ROOT / "INPUT-ACQUISITION.json"
    if target.is_symlink():
        raise RuntimeError("receipt path is a symlink")
    temporary = ROOT / "INPUT-ACQUISITION.json.tmp"
    with temporary.open("x", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    os.replace(temporary, target)


def main():
    started = time.monotonic()
    for folder in (ROOT, ROOT / "parts", ROOT / "arrays", ROOT / "metadata", ROOT / "http"):
        if folder.is_symlink():
            raise RuntimeError(f"unsafe output directory: {folder}")
        folder.mkdir(parents=True, exist_ok=True)
    inventory_file = RECOVERY / "github/raw-binary-inventory.json"
    inventory = json.loads(inventory_file.read_text())
    entries = [x for x in inventory["entries"] if Path(x["path"]).name in PART_IDENTITIES]
    if len(entries) != 4 or len({x["path"] for x in entries}) != 4:
        raise RuntimeError("four exact dense part records required")
    receipt = {
        "schema": "dense-input-acquisition/v1", "authoredDuringRecovery": True,
        "status": "acquiring", "repository": REPO, "immutableCommit": COMMIT,
        "taskTimeReferenceUTC": "2026-10-13T23:33:30Z", "taskTimeReferenceSource": "clock.curr_time before acquisition preparation",
        "scope": "Four public immutable raw-part downloads, transport integrity, and streaming gzip materialization only.",
        "toolFormatLimitation": "The GitHub MCP fetch_blob path cannot decode gzip payloads. Public shell curl GET is used; no access restriction is bypassed.",
        "sourceInventorySha256": hashlib.sha256(inventory_file.read_bytes()).hexdigest(),
        "parts": [], "arrays": [], "joinedCompressedFilesWritten": False,
        "numericalSimulationOrDiagnosticsPerformed": False,
    }
    save_receipt(receipt)
    try:
        for entry in sorted(entries, key=lambda x: x["path"]):
            name = Path(entry["path"]).name
            expected_size, expected_git = PART_IDENTITIES[name]
            if (entry["size"], entry["sha"]) != (expected_size, expected_git):
                raise RuntimeError(f"inventory changed: {name}")
            url = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{entry['path']}"
            output = ROOT / "parts" / name
            transfer = {"mode": "existing_local_verified"}
            if output.exists() or output.is_symlink():
                identity = file_identity(output)
            else:
                fd, temporary_name = tempfile.mkstemp(prefix="incoming-", dir=ROOT / "parts")
                os.close(fd)
                temporary = Path(temporary_name)
                header = ROOT / "http" / (name + ".headers.txt")
                try:
                    command = ["curl", "--fail", "--silent", "--show-error", "--location",
                               "--proto", "=https", "--proto-redir", "=https", "--connect-timeout", "20",
                               "--max-time", "180", "--dump-header", str(header), "--output", str(temporary),
                               "--write-out", "%{http_code}\n%{url_effective}\n%{size_download}\n", url]
                    result = subprocess.run(command, capture_output=True, text=True, timeout=190)
                    if result.returncode:
                        raise RuntimeError(f"curl failed for {name}: {result.stderr.strip()}")
                    status, effective_url, transferred_bytes = result.stdout.strip().splitlines()
                    if status != "200" or effective_url != url or int(transferred_bytes) != expected_size:
                        raise RuntimeError(f"unexpected HTTP transfer identity for {name}: {result.stdout}")
                    identity = file_identity(temporary)
                    if (identity["bytes"], identity["git_blob_sha1"]) != (expected_size, expected_git):
                        raise RuntimeError(f"downloaded part identity mismatch: {name}")
                    os.link(temporary, output)
                    transfer = {"mode": "downloaded", "httpStatus": int(status), "effectiveUrl": effective_url,
                                "downloadedBytes": int(transferred_bytes), "headers": str(header.relative_to(ROOT))}
                finally:
                    temporary.unlink(missing_ok=True)
            if (identity["bytes"], identity["git_blob_sha1"]) != (expected_size, expected_git):
                raise RuntimeError(f"existing part identity mismatch: {name}")
            record = {"repositoryPath": entry["path"], "localPath": str(output.relative_to(ROOT)),
                      "immutableUrl": url, "expectedGitBlobSha1": expected_git, "expectedBytes": expected_size,
                      "verified": True, **identity, "transfer": transfer}
            receipt["parts"].append(record)
            save_receipt(receipt)
            print(json.dumps({"partVerified": name, "bytes": identity["bytes"]}), flush=True)
        retention = json.loads((RECOVERY / "embedded/recovered/results/RAW-RETENTION-MANIFEST.json").read_text())
        for seed in (840131, 840137):
            gzip_name = f"s{seed}-p1-a4.dense.f64.gz"
            source_sidecar = RECOVERY / "embedded/recovered/results/raw" / (gzip_name + ".json")
            original = json.loads(source_sidecar.read_text())
            historical = next(x for x in retention["files"] if x["path"] == original["path"])
            if original["shape"] != [6401, 16, 17] or math.prod(original["shape"]) * 8 != original["uncompressedBytes"]:
                raise RuntimeError("unexpected dense byte-array dimensions")
            output = ROOT / "arrays" / gzip_name.removesuffix(".gz")
            if output.exists() or output.is_symlink():
                raise RuntimeError(f"array destination already exists; explicit verification required: {output}")
            compressed_hash = hashlib.sha256()
            dense_git = hashlib.sha1(b"blob " + str(original["compressedBytes"]).encode() + b"\0")
            uncompressed_hash = hashlib.sha256()
            decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
            compressed_count = decoded_count = 0
            fd, temporary_name = tempfile.mkstemp(prefix="decoding-", dir=ROOT / "arrays")
            temporary = Path(temporary_name)
            try:
                with os.fdopen(fd, "wb") as sink:
                    for part in (gzip_name + ".part01", gzip_name + ".part02"):
                        source = ROOT / "parts" / part
                        regular(source)
                        part_hash = hashlib.sha1(b"blob " + str(PART_IDENTITIES[part][0]).encode() + b"\0")
                        part_count = 0
                        with source.open("rb") as f:
                            while chunk := f.read(128 * 1024):
                                part_count += len(chunk)
                                part_hash.update(chunk)
                                compressed_count += len(chunk)
                                compressed_hash.update(chunk)
                                dense_git.update(chunk)
                                decoded = decoder.decompress(chunk, original["uncompressedBytes"] - decoded_count + 1)
                                decoded_count += len(decoded)
                                if decoded_count > original["uncompressedBytes"] or decoder.unused_data or decoder.unconsumed_tail:
                                    raise RuntimeError("unexpected gzip expansion/trailing data")
                                uncompressed_hash.update(decoded)
                                sink.write(decoded)
                        if (part_count, part_hash.hexdigest()) != PART_IDENTITIES[part]:
                            raise RuntimeError(f"part changed during streaming: {part}")
                    decoded = decoder.flush()
                    decoded_count += len(decoded)
                    uncompressed_hash.update(decoded)
                    sink.write(decoded)
                    sink.flush()
                    os.fsync(sink.fileno())
                if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
                    raise RuntimeError("gzip stream did not terminate cleanly")
                if (compressed_count, compressed_hash.hexdigest(), dense_git.hexdigest()) != (
                    original["compressedBytes"], original["sha256"], historical["gitBlobSha1"]):
                    raise RuntimeError("original compressed identity mismatch")
                if (decoded_count, uncompressed_hash.hexdigest()) != (original["uncompressedBytes"], original["uncompressedSha256"]):
                    raise RuntimeError("original uncompressed identity mismatch")
                os.link(temporary, output)
            finally:
                temporary.unlink(missing_ok=True)
            metadata = {"authorship": "New materialization metadata; original nested sidecar preserved below.",
                        "localArray": str(output.relative_to(ROOT)), "encoding": "little-endian Float64 bytes; no values interpreted",
                        "originalSidecar": original, "sourceSidecarSha256": hashlib.sha256(source_sidecar.read_bytes()).hexdigest(),
                        "originalSidecarProvenance": "Complete nested denseStates object recovered from the matching historical run record embedded in the reattached viewer; not a byte-identity claim for the lost original standalone sidecar."}
            metadata_path = ROOT / "metadata" / (gzip_name.removesuffix(".gz") + ".json")
            with metadata_path.open("x", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
                f.write("\n")
            receipt["arrays"].append({"seed": seed, "localPath": str(output.relative_to(ROOT)),
                "metadataPath": str(metadata_path.relative_to(ROOT)), "shape": original["shape"],
                "compressedBytes": compressed_count, "compressedSha256": compressed_hash.hexdigest(),
                "originalCompressedGitBlobSha1": dense_git.hexdigest(), "uncompressedBytes": decoded_count,
                "uncompressedSha256": uncompressed_hash.hexdigest(), "allIdentitiesVerified": True})
            save_receipt(receipt)
            print(json.dumps({"denseArrayVerified": output.name, "bytes": decoded_count}), flush=True)
        receipt.update(status="verified_complete", elapsedSeconds=time.monotonic()-started,
                       logicalArrayBytes=sum(x["uncompressedBytes"] for x in receipt["arrays"]),
                       retainedTransportPartBytes=sum(x["bytes"] for x in receipt["parts"]))
        receipt["retainedDataBytes"] = receipt["logicalArrayBytes"] + receipt["retainedTransportPartBytes"]
        receipt["partsPreserved"] = True
        save_receipt(receipt)
        print(json.dumps({k: receipt[k] for k in ("status", "logicalArrayBytes", "retainedTransportPartBytes", "retainedDataBytes", "elapsedSeconds")}), flush=True)
    except BaseException as exc:
        receipt.update(status="stopped", errorType=type(exc).__name__, error=str(exc), elapsedSeconds=time.monotonic()-started)
        save_receipt(receipt)
        raise


if __name__ == "__main__":
    main()
