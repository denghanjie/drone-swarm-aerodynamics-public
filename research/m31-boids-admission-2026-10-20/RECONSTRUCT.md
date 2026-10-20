# Read the complete raw evidence

The four full gzip journals remain unchanged in the author's local results directory. Public Git contains all of their bytes in ordered 32 MiB parts under archive/. No records were removed or recompressed. The original journal hashes in results/index.json remain authoritative; archive/index.json maps each original to its ordered parts. The publication result manifest lists actual committed parts, not nonexistent full journal blobs.

To reconstruct in a clean checkout, run this standard-library Python snippet from the repository root. It creates each original only if absent, checks every part and verifies the reconstructed original identity. It does not run the model or reopen any closed research allocation.

```python
from pathlib import Path
import hashlib, json
base = Path("research/m31-boids-admission-2026-10-20")
archive = json.loads((base / "archive/index.json").read_text())
for item in archive["journals"]:
    destination = base / item["originalFile"]
    if destination.exists():
        raise FileExistsError(destination)  # Preserve existing evidence.
    h = hashlib.sha256()
    total = 0
    with destination.open("xb") as output:
        for part in item["parts"]:
            raw = (base / "archive" / part["file"]).read_bytes()
            assert len(raw) == part["bytes"]
            assert hashlib.sha256(raw).hexdigest() == part["sha256"]
            assert part["offset"] == total
            output.write(raw)
            h.update(raw)
            total += len(raw)
    assert total == item["bytes"] and h.hexdigest() == item["sha256"]
```

Each journal is a standard concatenated gzip stream. Python's gzip.open reads it as JSON lines. Read records without re-executing the producer or auditor. A failed reconstruction leaves its partial output for diagnosis; do not regard that file as verified. Passing the byte checks establishes file identity only, not correctness of the scientific model.
