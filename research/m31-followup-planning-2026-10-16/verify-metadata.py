"""Offline verification of public metadata; no CSVs, model or browser execution."""
from pathlib import Path, PurePosixPath
import hashlib
import json
from collections import defaultdict

BASE = Path(__file__).resolve().parent
D = BASE / "datasets"


def read(name):
    return json.loads((D / name).read_text())


def git_hash(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


for line in (D / "SHA256SUMS").read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    assert Path(name).name == name
    assert hashlib.sha256((D / name).read_bytes()).hexdigest() == digest, name

tree = read("nanobench-tree-projection.json")
commit = read("nanobench-commit-projection.json")
manifest = read("nanobench-pinned-manifest.json")
assert tree["truncated"] is False
assert tree["commit_sha"] == commit["commit_sha"] == manifest["commit"]
assert tree["root_tree_sha"] == commit["root_tree_sha"]
entries = {v["path"]: v for v in tree["tree"]}
assert len(entries) == len(tree["tree"]) == 416
children = defaultdict(list)
for path, entry in entries.items():
    children[str(PurePosixPath(path).parent)].append(entry)
trees = {".": tree["root_tree_sha"]}
trees.update({p: e["sha"] for p, e in entries.items() if e["type"] == "tree"})
for path, expected in trees.items():
    records = sorted(children[path], key=lambda e: (PurePosixPath(e["path"]).name + ("/" if e["type"] == "tree" else "")).encode())
    data = b"".join(e["mode"].lstrip("0").encode() + b" " + PurePosixPath(e["path"]).name.encode() + b"\0" + bytes.fromhex(e["sha"]) for e in records)
    assert git_hash("tree", data) == expected, path

files = {v["path"]: v for v in manifest["files"]}
scoped = {p: e for p, e in entries.items() if str(PurePosixPath(p).parent) == manifest["directory"] and e["type"] == "blob"}
assert len(files) == len(manifest["files"]) == 215
assert files.keys() == scoped.keys()
for path, f in files.items():
    assert (f["bytes"], f["git_blob_sha"]) == (scoped[path]["size"], scoped[path]["sha"])
csv = [e for p, e in scoped.items() if p.endswith(".csv")]
yaml = {p for p in scoped if p.endswith(".yaml")}
assert {e["path"][:-4] + "_metadata.yaml" for e in csv} == yaml
groups = defaultdict(list)
for e in csv:
    groups[e["sha"]].append(PurePosixPath(e["path"]).name)
repeated = {sha: sorted(names) for sha, names in groups.items() if len(names) > 1}
assert repeated == {e["git_blob_sha"]: sorted(e["names"]) for e in manifest["duplicate_csv_blob_groups"]}
counts = {"csv": len(csv), "yaml": len(yaml), "distinctCsvBlobs": len(groups), "repeatedGroups": len(repeated), "csvAdvertisedBytes": sum(e["size"] for e in csv), "reconstructedTrees": len(trees)}
assert counts == {"csv": 107, "yaml": 107, "distinctCsvBlobs": 87, "repeatedGroups": 18, "csvAdvertisedBytes": 290797892, "reconstructedTrees": 33}

bindings = {"nanobench-README.md": "README.md", "nanobench-LICENSE": "LICENSE"}
for name in ("A1b_multisine_sysid_rep1_metadata.yaml", "C4_battery_drain_rep1_metadata.yaml"):
    bindings[name] = manifest["directory"] + "/" + name
for name, path in bindings.items():
    data = (D / name).read_bytes()
    assert (len(data), git_hash("blob", data)) == (entries[path]["size"], entries[path]["sha"])

audit = json.loads((BASE / "m31-nanobench-independent-metadata-reconciliation.json").read_text())
assert all(value is True for value in audit["checks"].values())
assert audit["counts"]["csv_count"] == counts["csv"]
assert audit["counts"]["csv_unique_blob_count"] == counts["distinctCsvBlobs"]
print(json.dumps({"kind": "coordinator-public-metadata-reproduction", "passed": True, "counts": counts, "textBlobBindings": len(bindings), "publicPackageChecksumEntries": 13, "csvPayloadsRead": 0, "archivePayloadsRead": 0, "scope": "Saved public metadata consistency only; no physical validation, acquisition authentication or trial-independence inference."}, indent=2))
