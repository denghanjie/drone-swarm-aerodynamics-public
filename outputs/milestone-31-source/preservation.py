"""Compare every historical source-tree artifact to the pre-milestone snapshot."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent.parent
reference = root / 'archive-before-full-priority-missions/research-manifest.json'
manifest = json.loads(reference.read_text())
entries = [e for e in manifest['files'] if '-source/' in e['path']]
changed = []
for entry in entries:
    path = root / entry['path']
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
        changed.append(entry['path'])
result = dict(reference=str(reference.relative_to(root)),
              historicalSourceTreeFilesChecked=len(entries),
              changedOrMissing=changed, passed=not changed)
(root / 'milestone-31-preservation-check.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result))
if changed:
    raise SystemExit(1)
