"""Final byte-only publication inventory; never executes science or its reviewer."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parents[1]
repo = base.parents[1]
target = base / 'manifest.json'
if target.exists():
    raise SystemExit('Final publication manifest already exists; preserve it')

freeze_bytes = (base / 'freeze.json').read_bytes()
freeze = json.loads(freeze_bytes)
authority = json.loads((base / 'publication/review-capture-execution.json').read_text())
assert authority['actualCaptureExitCode'] == 1
assert authority['terminalReviewFailureObserved'] is True
assert authority['observedIntegrityVerified'] is False
assert authority['decisionVerified'] is False
assert authority['scientificQualified'] is False
assert authority['toolSessionCompleted'] is True
assert authority['completeSummaryBindingVerified'] is True

files = {p for p in base.rglob('*') if p.is_file() and p != target}
files.update(repo / pin['path'] for pin in freeze['files'])
files.update(repo / 'outputs/step02b-source/vendor' / name
             for name in ['three.core.js', 'three.module.js', 'OrbitControls.js'])
files.update(p for p in (repo / 'research/m31-source-contract-planning-2026-10-16').rglob('*') if p.is_file())
pins = []
for path in sorted(files):
    if path.is_symlink() or not path.is_relative_to(repo):
        raise SystemExit('Nonregular or noncontained publication entry')
    data = path.read_bytes()
    pins.append({'path': path.relative_to(repo).as_posix(), 'bytes': len(data),
                 'sha256': hashlib.sha256(data).hexdigest()})

manifest = {
    'status': 'Terminal GPU-output persistence failure and terminal saved-review schema failure',
    'sourceCommit': 'f12d8c836e7b991ec33e6de662d00ed05dcce33e',
    'sourceFreezeSHA256': hashlib.sha256(freeze_bytes).hexdigest(),
    'reviewFreezeSHA256': authority['reviewFreezeSHA256'],
    'scienceAttemptTerminal': True,
    'reviewAttemptTerminal': True,
    'savedReviewIntegrityVerified': False,
    'savedReviewScientificDecisionVerified': False,
    'scientificQualified': False,
    'retryPermitted': False,
    'scope': 'Preserved failed attempts, static diagnoses, actual-control Three.js view and presentation QA. Byte manifest is not a substitute successful scientific or saved-review verdict.',
    'files': pins,
}
data = (json.dumps(manifest, indent=2) + '\n').encode()
with target.open('xb') as output:
    if output.write(data) != len(data):
        raise SystemExit('Incomplete publication manifest; preserve partial file')
print(json.dumps({'manifestSHA256': hashlib.sha256(data).hexdigest(),
                  'manifestBytes': len(data), 'files': len(pins)}))
