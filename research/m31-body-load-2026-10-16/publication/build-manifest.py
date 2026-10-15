"""Byte-only final publication manifest; no numerical or review execution."""
from pathlib import Path
import hashlib, json

base = Path(__file__).resolve().parents[1]
repo = base.parents[1]
target = base / 'manifest.json'
if target.exists():
    raise SystemExit('Publication manifest already exists; do not replace it')
freeze_bytes = (base / 'freeze.json').read_bytes()
freeze = json.loads(freeze_bytes)
review_observation = json.loads((base / 'publication/observer-execution.json').read_text())
files = {p for p in base.rglob('*') if p.is_file() and p != target}
files.update(repo / pin['path'] for pin in freeze['files'])
files.update(repo / 'outputs/step02b-source/vendor' / name for name in
             ['three.core.js', 'three.module.js', 'OrbitControls.js'])
pins = []
for path in sorted(files):
    if path.is_symlink() or not path.is_relative_to(repo):
        raise SystemExit('Nonregular or noncontained publication entry')
    data = path.read_bytes()
    pins.append({'path': path.relative_to(repo).as_posix(), 'bytes': len(data),
                 'sha256': hashlib.sha256(data).hexdigest()})
manifest = {
    'status': 'Terminal browser-version admission failure; no GPU/main-family observations',
    'sourceCommit': 'e60702197dde11893f01f01496edafbefb4a43de',
    'sourceFreezeSHA256': hashlib.sha256(freeze_bytes).hexdigest(),
    'scienceAttemptTerminal': True,
    'reviewAttemptTerminal': (base / 'review/results/sole-review.lock').is_file(),
    'savedReviewIntegrityVerified': review_observation['observedIntegrityVerified'],
    'savedReviewScientificDecisionVerified': review_observation['decisionVerified'],
    'retryPermitted': False,
    'scientificQualified': False,
    'scope': 'Preserved failed attempt, saved-only review and actual-control Three.js evidence view. No accuracy, physics, scaling, speed or novelty result.',
    'files': pins,
}
data = (json.dumps(manifest, indent=2) + '\n').encode()
with target.open('xb') as output:
    output.write(data)
print(json.dumps({'manifestSHA256': hashlib.sha256(data).hexdigest(),
                  'manifestBytes': len(data), 'files': len(pins)}))
