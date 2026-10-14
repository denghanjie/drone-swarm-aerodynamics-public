"""Synthetic transport/safety tests only; no models or numerical experiments."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock


HERE = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location("recovery", HERE / "reconstruct_binary_checkpoint.py")
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


def git_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class ReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="checkpoint-synthetic-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "raw").mkdir()
        self.payloads = {
            "raw/example.dense.f64.part01": b"synthetic\x00first\x00part",
            "raw/example.dense.f64.part02": b"synthetic\xffsecond\x00part",
            "raw/other.bin": b"synthetic standalone object",
        }
        for path, data in self.payloads.items():
            (self.root / path).write_bytes(data)
        self.parts = list(self.payloads)[:2]
        self.joined = b"".join(self.payloads[p] for p in self.parts)
        self.destination = self.root / "raw/example.dense.f64"
        def identity(data):
            return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                    "gitSha": git_sha(data)}
        self.manifest = {
            "schema": recovery.SCHEMA,
            "logicalFiles": 2,
            "logicalBytes": len(self.joined) + len(self.payloads["raw/other.bin"]),
            "storedObjects": 3,
            "files": [
                {"logicalPath": "raw/example.dense.f64", "localPath": "ignored-provenance",
                 **identity(self.joined), "mode": "parts",
                 "objects": [{"path": p, "offset": sum(len(self.payloads[x]) for x in self.parts[:i]),
                              **identity(self.payloads[p])} for i, p in enumerate(self.parts)]},
                {"logicalPath": "raw/other.bin", **identity(self.payloads["raw/other.bin"]),
                 "mode": "whole", "objects": [{"path": "raw/other.bin", "offset": 0,
                                                **identity(self.payloads["raw/other.bin"])}]},
            ],
        }


    def assert_refused(self, manifest=None, root=None):
        with self.assertRaises((recovery.Refused, OSError)):
            recovery.recover(root or self.root, self.manifest if manifest is None else manifest)
        self.assertFalse(any((self.root / "raw").glob(".checkpoint-reconstruction-*.tmp")))

    def test_success_preserves_parts_and_exact_existing_output(self):
        before = {p: ((self.root / p).stat().st_ino, (self.root / p).read_bytes()) for p in self.parts}
        report = recovery.recover(self.root, self.manifest)
        self.assertEqual(report["transport_objects_verified"], 3)
        self.assertEqual(report["outputs"][0]["status"], "reconstructed_verified")
        self.assertEqual(self.destination.read_bytes(), self.joined)
        inode = self.destination.stat().st_ino
        again = recovery.recover(self.root, self.manifest)
        self.assertEqual(again["outputs"][0]["status"], "existing_verified")
        self.assertEqual(inode, self.destination.stat().st_ino)
        for p, identity in before.items():
            self.assertEqual(identity, ((self.root / p).stat().st_ino, (self.root / p).read_bytes()))

    def test_verify_only_does_not_create_output(self):
        report = recovery.recover(self.root, self.manifest, verify_only=True)
        self.assertEqual(report["status"], "verified_only")
        self.assertEqual(report["joined_streams_verified"][0]["gitSha"], git_sha(self.joined))
        self.assertFalse(self.destination.exists())

    def test_verify_only_checks_joined_identity_without_existing_output(self):
        self.manifest["files"][0]["sha256"] = "0" * 64
        with self.assertRaises(recovery.Refused):
            recovery.recover(self.root, self.manifest, verify_only=True)
        self.assertFalse(self.destination.exists())

    def test_original_dense_git_blob_identity_is_checked(self):
        self.manifest["files"][0]["gitSha"] = "0" * 40
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_wrong_part_hash(self):
        p = self.root / self.parts[0]
        p.write_bytes(b"x" * len(p.read_bytes()))
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_wrong_part_size(self):
        (self.root / self.parts[0]).write_bytes(b"short")
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_other_inventory_object_is_also_verified(self):
        (self.root / "raw/other.bin").write_bytes(b"x" * len(self.payloads["raw/other.bin"]))
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_missing_input_is_rejected(self):
        (self.root / self.parts[0]).unlink()
        self.assert_refused()

    def test_wrong_whole_sha_is_rejected_without_destination(self):
        self.manifest["files"][0]["sha256"] = "0" * 64
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_wrong_part_order_rejected_by_original_whole_sha(self):
        objects = self.manifest["files"][0]["objects"]
        objects.reverse()
        offset = 0
        for entry in objects:
            entry["offset"] = offset
            offset += entry["bytes"]
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_existing_mismatched_destination_is_never_overwritten(self):
        data = b"x" * len(self.joined)
        self.destination.write_bytes(data)
        inode = self.destination.stat().st_ino
        self.assert_refused()
        self.assertEqual(self.destination.read_bytes(), data)
        self.assertEqual(self.destination.stat().st_ino, inode)

    def test_existing_wrong_size_destination_is_never_overwritten(self):
        self.destination.write_bytes(b"keep")
        self.assert_refused()
        self.assertEqual(self.destination.read_bytes(), b"keep")

    def test_rejects_traversal_absolute_and_nonportable_paths(self):
        for field in ("object", "logical"):
            for unsafe in ("../escape", "/tmp/escape", "raw/../escape", "./raw/part",
                           "raw//part", "raw\\part", "C:/escape", "", "raw/\x00bad"):
                with self.subTest(field=field, unsafe=unsafe):
                    manifest = copy.deepcopy(self.manifest)
                    if field == "object":
                        manifest["files"][0]["objects"][0]["path"] = unsafe
                    else:
                        manifest["files"][0]["logicalPath"] = unsafe
                    self.assert_refused(manifest)

    def test_rejects_duplicate_input_and_output_overlaps(self):
        bad = copy.deepcopy(self.manifest)
        bad["files"][0]["objects"][1]["path"] = bad["files"][0]["objects"][0]["path"]
        self.assert_refused(bad)
        bad = copy.deepcopy(self.manifest)
        bad["files"][0]["logicalPath"] = self.parts[0]
        self.assert_refused(bad)

    def test_rejects_noninteger_size_and_bad_hash(self):
        for value in (True, -1, "12", 1.5):
            with self.subTest(value=value):
                bad = copy.deepcopy(self.manifest)
                bad["files"][0]["objects"][0]["bytes"] = value
                self.assert_refused(bad)
        self.manifest["files"][0]["objects"][0]["gitSha"] = "g" * 40
        self.assert_refused()

    def test_rejects_symlink_input(self):
        p = self.root / self.parts[0]
        p.unlink()
        p.symlink_to(self.root / self.parts[1])
        self.assert_refused()

    def test_rejects_symlink_output(self):
        external = self.root / "external"
        external.write_bytes(self.joined)
        self.destination.symlink_to(external)
        self.assert_refused()
        self.assertEqual(external.read_bytes(), self.joined)

    def test_rejects_dangling_symlink_output(self):
        self.destination.symlink_to(self.root / "nonexistent")
        self.assert_refused()
        self.assertTrue(self.destination.is_symlink())

    def test_rejects_symlink_parent(self):
        (self.root / "raw").rename(self.root / "actual")
        (self.root / "raw").symlink_to(self.root / "actual", target_is_directory=True)
        self.assert_refused()

    def test_rejects_symlink_root_and_root_ancestor(self):
        (self.root / "link").symlink_to(self.root, target_is_directory=True)
        self.assert_refused(root=self.root / "link")
        self.assert_refused(root=self.root / "link" / "raw")

    def test_rejects_fifo_without_blocking(self):
        p = self.root / self.parts[0]
        p.unlink()
        os.mkfifo(p)
        self.assert_refused()

    def test_part_changed_after_precheck_is_reverified(self):
        original = recovery.reconstruct_one
        def change_and_reconstruct(root_fd, output, by_path):
            p = self.root / self.parts[0]
            p.write_bytes(b"x" * len(p.read_bytes()))
            return original(root_fd, output, by_path)
        with mock.patch.object(recovery, "reconstruct_one", side_effect=change_and_reconstruct):
            self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_install_race_cannot_clobber_new_destination(self):
        original = os.link
        def race(*args, **kwargs):
            self.destination.write_bytes(b"concurrent data")
            return original(*args, **kwargs)
        with mock.patch.object(recovery.os, "link", side_effect=race):
            self.assert_refused()
        self.assertEqual(self.destination.read_bytes(), b"concurrent data")

    def test_temp_name_collision_preserves_existing_file(self):
        collision = self.root / "raw/.checkpoint-reconstruction-collision.tmp"
        collision.write_bytes(b"preserve unrelated file")
        with mock.patch.object(recovery.uuid, "uuid4", return_value=types.SimpleNamespace(hex="collision")):
            with self.assertRaises(FileExistsError):
                recovery.recover(self.root, self.manifest)
        self.assertEqual(collision.read_bytes(), b"preserve unrelated file")

    def test_manifest_symlink_and_duplicate_keys_rejected(self):
        valid = self.root / "manifest.json"
        valid.write_text(json.dumps(self.manifest))
        symlink = self.root / "linked.json"
        symlink.symlink_to(valid)
        with self.assertRaises(OSError):
            recovery.load_manifest(symlink)
        valid.write_text('{"schema":"a","schema":"b"}')
        with self.assertRaises(recovery.Refused):
            recovery.load_manifest(valid)

    def test_cli_success_and_failure_codes(self):
        manifest_file = self.root / "manifest.json"
        manifest_file.write_text(json.dumps(self.manifest))
        args = [sys.executable, str(HERE / "reconstruct_binary_checkpoint.py"), "--root", str(self.root),
                "--manifest", str(manifest_file), "--verify-only"]
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["transport_objects_verified"], 3)
        (self.root / self.parts[0]).unlink()
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("reconstruction refused:", result.stderr)

    def test_object_sha256_is_independently_checked(self):
        self.manifest["files"][0]["objects"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(recovery.Refused, "transport object SHA-256 mismatch"):
            recovery.recover(self.root, self.manifest)
        self.assertFalse(self.destination.exists())

    def test_object_git_blob_sha1_is_independently_checked(self):
        self.manifest["files"][0]["objects"][0]["gitSha"] = "0" * 40
        with self.assertRaisesRegex(recovery.Refused, "transport object Git blob SHA-1 mismatch"):
            recovery.recover(self.root, self.manifest)
        self.assertFalse(self.destination.exists())

    def test_truncated_by_one_byte_is_rejected(self):
        path = self.root / self.parts[0]
        path.write_bytes(path.read_bytes()[:-1])
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_extra_trailing_byte_is_rejected(self):
        path = self.root / self.parts[0]
        path.write_bytes(path.read_bytes() + b"x")
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_manifest_counts_and_total_are_checked(self):
        for field in ("logicalFiles", "logicalBytes", "storedObjects"):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest[field] += 1
                self.assert_refused(manifest)

    def test_offsets_reject_gaps_overlaps_and_wrong_types(self):
        for value in (0, 1, -1, True, "18", 999):
            with self.subTest(offset=value):
                manifest = copy.deepcopy(self.manifest)
                manifest["files"][0]["objects"][1]["offset"] = value
                self.assert_refused(manifest)

    def test_whole_identity_must_match_its_object(self):
        for field, value in (("logicalPath", "raw/elsewhere.bin"), ("bytes", 1),
                             ("sha256", "0" * 64), ("gitSha", "0" * 40)):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.manifest)
                manifest["files"][1][field] = value
                self.assert_refused(manifest)

    def test_modes_and_object_counts_are_checked(self):
        for mode in ("gzip", "", None, "whole"):
            with self.subTest(mode=mode):
                manifest = copy.deepcopy(self.manifest)
                manifest["files"][0]["mode"] = mode
                self.assert_refused(manifest)
        self.manifest["files"][0]["objects"].pop()
        self.assert_refused()

    def test_duplicate_logical_paths_are_rejected(self):
        self.manifest["files"][1]["logicalPath"] = self.manifest["files"][0]["logicalPath"]
        self.assert_refused()

    def test_file_as_ancestor_is_rejected(self):
        self.manifest["files"][0]["objects"][0]["path"] = "raw/other.bin/child"
        self.assert_refused()

    def test_oversized_transport_object_is_rejected_without_io(self):
        self.manifest["files"][0]["objects"][0]["bytes"] = recovery.MAX_OBJECT_BYTES + 1
        self.assert_refused()

    def test_local_path_metadata_is_never_used_for_io(self):
        self.manifest["files"][0]["localPath"] = "../../outside-this-checkout"
        report = recovery.recover(self.root, self.manifest)
        self.assertEqual(report["status"], "reconstruction_complete")
        self.assertEqual(self.destination.read_bytes(), self.joined)

    def test_verify_only_rejects_mismatched_existing_output(self):
        self.destination.write_bytes(b"preserve me")
        with self.assertRaises(recovery.Refused):
            recovery.recover(self.root, self.manifest, verify_only=True)
        self.assertEqual(self.destination.read_bytes(), b"preserve me")

    def test_rejects_existing_directory_as_destination(self):
        self.destination.mkdir()
        self.assert_refused()
        self.assertTrue(self.destination.is_dir())

    def test_rejects_dangling_symlink_input(self):
        path = self.root / self.parts[0]
        path.unlink()
        path.symlink_to(self.root / "absent")
        self.assert_refused()
        self.assertTrue(path.is_symlink())

    def test_checks_all_destinations_before_creating_any(self):
        second = copy.deepcopy(self.manifest["files"][0])
        second["logicalPath"] = "raw/second.dense.f64"
        for entry in second["objects"]:
            original = entry["path"]
            entry["path"] = original.replace("example", "second")
            (self.root / entry["path"]).write_bytes(self.payloads[original])
        self.manifest["files"].append(second)
        self.manifest["logicalFiles"] += 1
        self.manifest["storedObjects"] += 2
        self.manifest["logicalBytes"] += second["bytes"]
        destination = self.root / second["logicalPath"]
        destination.write_bytes(b"preserve later destination")
        self.assert_refused()
        self.assertFalse(self.destination.exists())
        self.assertEqual(destination.read_bytes(), b"preserve later destination")

    def test_detects_change_while_reading(self):
        original_read = os.read
        changed = False
        path = self.root / self.parts[0]
        def change_after_read(fd, size):
            nonlocal changed
            data = original_read(fd, size)
            if data and not changed:
                changed = True
                with path.open("ab") as sink:
                    sink.write(b"extra byte")
            return data
        with mock.patch.object(recovery.os, "read", side_effect=change_after_read):
            self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_matching_concurrent_destination_is_preserved(self):
        original = os.link
        installed_inode = []
        def race(*args, **kwargs):
            self.destination.write_bytes(self.joined)
            installed_inode.append(self.destination.stat().st_ino)
            return original(*args, **kwargs)
        with mock.patch.object(recovery.os, "link", side_effect=race):
            report = recovery.recover(self.root, self.manifest)
        self.assertEqual(report["outputs"][0]["status"], "concurrently_created_verified")
        self.assertEqual(self.destination.stat().st_ino, installed_inode[0])
        self.assertEqual(self.destination.read_bytes(), self.joined)
        self.assertFalse(any((self.root / "raw").glob(".checkpoint-reconstruction-*.tmp")))


class CheckpointManifestMetadataTests(unittest.TestCase):
    def test_52_logical_files_54_objects_two_exact_raw_dense_identities(self):
        manifest = recovery.load_manifest(HERE / "BINARY-TRANSPORT-MANIFEST.json")
        by_path, outputs = recovery.validate_manifest(manifest)
        self.assertEqual(len(manifest["files"]), 52)
        self.assertEqual(len(by_path), 54)
        self.assertEqual(manifest["logicalBytes"], 58664800)
        self.assertEqual(sum(x["bytes"] for x in by_path.values()), 58664800)
        self.assertEqual(len(outputs), 2)
        self.assertEqual([x["bytes"] for x in outputs], [13928576, 13928576])
        self.assertEqual([x["sha256"] for x in outputs], [
            "dbc554ed5e5f7056985a07b332afa788c7de7dfd10257507e0378c069c476ed5",
            "95fa467cd439c43afe2d8f0d4d75e1812c42bf862c38bba398ae509d5312d4b8"])
        for logical in manifest["files"]:
            if logical["mode"] == "parts":
                self.assertEqual([x["offset"] for x in logical["objects"]], [0, 8000000])
                self.assertEqual([x["bytes"] for x in logical["objects"]], [8000000, 5928576])


if __name__ == "__main__":
    unittest.main(verbosity=2)
