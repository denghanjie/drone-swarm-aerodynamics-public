"""Synthetic transport/safety tests only; no historical raw files or dynamics."""

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
spec = importlib.util.spec_from_file_location("recovery", HERE / "reconstruct_dense_recovery.py")
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


def git_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class ReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="recovery-synthetic-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "raw").mkdir()
        self.payloads = {
            "raw/example.dense.gz.part01": b"synthetic\x00first\x00part",
            "raw/example.dense.gz.part02": b"synthetic\xffsecond\x00part",
            "raw/other.gz": b"synthetic standalone object",
        }
        for path, data in self.payloads.items():
            (self.root / path).write_bytes(data)
        self.parts = list(self.payloads)[:2]
        self.joined = b"".join(self.payloads[p] for p in self.parts)
        self.destination = self.root / "raw/example.dense.gz"
        self.manifest = {
            "schema": recovery.SCHEMA,
            "expected_object_count": 3,
            "git_objects": [{"path": p, "bytes": len(b), "git_blob_sha1": git_sha(b)}
                            for p, b in self.payloads.items()],
            "dense_outputs": [{"path": "raw/example.dense.gz", "bytes": len(self.joined),
                               "compressed_sha256": hashlib.sha256(self.joined).hexdigest(),
                               "git_blob_sha1": git_sha(self.joined),
                               "parts": self.parts.copy()}],
        }

    def assert_refused(self, manifest=None, root=None):
        with self.assertRaises((recovery.Refused, OSError)):
            recovery.recover(root or self.root, self.manifest if manifest is None else manifest)
        self.assertFalse(any((self.root / "raw").glob(".dense-recovery-*.tmp")))

    def test_success_preserves_parts_and_exact_existing_output(self):
        before = {p: ((self.root / p).stat().st_ino, (self.root / p).read_bytes()) for p in self.parts}
        report = recovery.recover(self.root, self.manifest)
        self.assertEqual(report["git_objects_verified"], 3)
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
        self.assertEqual(report["dense_streams_verified"][0]["git_blob_sha1"], git_sha(self.joined))
        self.assertFalse(self.destination.exists())

    def test_verify_only_checks_joined_identity_without_existing_output(self):
        self.manifest["dense_outputs"][0]["compressed_sha256"] = "0" * 64
        with self.assertRaises(recovery.Refused):
            recovery.recover(self.root, self.manifest, verify_only=True)
        self.assertFalse(self.destination.exists())

    def test_original_dense_git_blob_identity_is_checked(self):
        self.manifest["dense_outputs"][0]["git_blob_sha1"] = "0" * 40
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
        (self.root / "raw/other.gz").write_bytes(b"x" * len(self.payloads["raw/other.gz"]))
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_missing_input_is_rejected(self):
        (self.root / self.parts[0]).unlink()
        self.assert_refused()

    def test_wrong_whole_sha_is_rejected_without_destination(self):
        self.manifest["dense_outputs"][0]["compressed_sha256"] = "0" * 64
        self.assert_refused()
        self.assertFalse(self.destination.exists())

    def test_wrong_part_order_rejected_by_original_whole_sha(self):
        self.manifest["dense_outputs"][0]["parts"].reverse()
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
        for field in ("git_objects", "dense_outputs"):
            for unsafe in ("../escape", "/tmp/escape", "raw/../escape", "./raw/part",
                           "raw//part", "raw\\part", "C:/escape", "", "raw/\x00bad"):
                with self.subTest(field=field, unsafe=unsafe):
                    manifest = copy.deepcopy(self.manifest)
                    manifest[field][0]["path"] = unsafe
                    self.assert_refused(manifest)

    def test_rejects_duplicate_input_and_output_overlaps(self):
        bad = copy.deepcopy(self.manifest)
        bad["git_objects"][1]["path"] = bad["git_objects"][0]["path"]
        self.assert_refused(bad)
        bad = copy.deepcopy(self.manifest)
        bad["dense_outputs"][0]["path"] = self.parts[0]
        self.assert_refused(bad)

    def test_rejects_noninteger_size_and_bad_hash(self):
        for value in (True, -1, "12", 1.5):
            with self.subTest(value=value):
                bad = copy.deepcopy(self.manifest)
                bad["git_objects"][0]["bytes"] = value
                self.assert_refused(bad)
        self.manifest["git_objects"][0]["git_blob_sha1"] = "g" * 40
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
        collision = self.root / "raw/.dense-recovery-collision.tmp"
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
        args = [sys.executable, str(HERE / "reconstruct_dense_recovery.py"), "--root", str(self.root),
                "--manifest", str(manifest_file), "--verify-only"]
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["git_objects_verified"], 3)
        (self.root / self.parts[0]).unlink()
        result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("reconstruction refused:", result.stderr)


class HistoricalManifestMetadataTests(unittest.TestCase):
    def test_seventeen_git_objects_and_two_original_dense_sha256_values(self):
        manifest = recovery.load_manifest(HERE / "raw-recovery-manifest.json")
        self.assertEqual(len(manifest["git_objects"]), 17)
        self.assertEqual(sum(x["bytes"] for x in manifest["git_objects"]), 64975968)
        self.assertEqual(len(manifest["dense_outputs"]), 2)
        self.assertEqual([x["bytes"] for x in manifest["dense_outputs"]], [13371234, 13365454])
        self.assertEqual([x["compressed_sha256"] for x in manifest["dense_outputs"]], [
            "94a3799c2e6f177b2d3bd1a9d20fd0b7cd659a1150f509bf47796644cf3605aa",
            "4464824125d4b6aafeb61b3e875eefe3d9afaf07f191d7cda9a042c76fa0ca65"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
