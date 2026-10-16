"""One administrative seal of saved Boolean gates and terminal process evidence.

No scientific import, solver, target arithmetic or timing reanalysis. Run only
after the two frozen scientific allocations have terminal supervisor records.
"""
from pathlib import Path
import hashlib
import json
import sys
import time

p = Path(__file__).resolve().parent.parent
repo = p.parent.parent
out = p/'results'
started = time.monotonic()
with (out/'qualification-seal.lock').open('x') as f:
    f.write('One administrative metadata seal consumed; do not repeat.\n')
result = dict(kind='terminal-center-screen-qualification', sealSuccess=False,
              evidenceQualified=False, practicalRulePass=False, sourceCommit=None,
              sourceManifestSha256=None, failureReasons=[], sourceFilesVerified=0,
              artifactPinsVerified=0, numericalReanalysis=False,
              scientificInvocationsAdded=0, inputs={})

def check(condition, reason):
    if not condition:
        raise ValueError(reason)

def guard():
    check(time.monotonic()-started <= 20, 'metadata-wall-limit')

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            guard()
            h.update(b)
    return h.hexdigest()

def safe_path(base, name):
    q = Path(name)
    check(not q.is_absolute() and '..' not in q.parts, 'nonrelative-pin')
    path = base/q
    check(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(base.resolve()), 'missing-or-escaping-pin')
    return path

def verify_pin(base, pin):
    f = safe_path(base, pin['path'])
    check(f.stat().st_size == pin['bytes'] and digest(f) == pin['sha256'], 'artifact-pin-mismatch')

def load(name):
    f = safe_path(p, name)
    check(f.stat().st_size <= 64*1024**2, 'metadata-input-size')
    result['inputs'][name] = dict(bytes=f.stat().st_size, sha256=digest(f))
    def reject(value):
        raise ValueError('nonfinite-metadata')
    return json.loads(f.read_text(), parse_constant=reject)

try:
    check(len(sys.argv) == 3 and sys.flags.optimize == 0, 'metadata-arguments')
    expected_sha, expected_commit = sys.argv[1:]
    result.update(sourceCommit=expected_commit, sourceManifestSha256=expected_sha)
    manifest = load('source-manifest.json')
    check(result['inputs']['source-manifest.json']['sha256'] == expected_sha, 'source-manifest-identity')
    for pin in manifest['files']:
        verify_pin(repo, pin)
        result['sourceFilesVerified'] += 1
    receipt_path = repo/'research/publication-receipts/m31-center-screen-source-2026-10-16.json'
    receipt = json.loads(receipt_path.read_text())
    check(receipt.get('commit') == expected_commit and receipt.get('manifestSha256') == expected_sha
          and receipt.get('remoteManifestMatchesLocal') is True and receipt.get('localAndCommittedPinsMatch') is True,
          'source-publication-receipt')
    result['sourceReceiptSha256'] = digest(receipt_path)
    candidate, reviewer = load('results/candidate-run.json'), load('results/review-run.json')
    audit, analysis = load('results/independent-review.json'), load('results/analysis.json')
    gates = {}
    for kind, rec, cap in [('candidate', candidate, 900), ('review', reviewer, 180)]:
        check(rec.get('kind') == kind and rec.get('sourceCommit') == expected_commit
              and rec.get('sourceManifestSha256') == expected_sha, 'supervisor-source-identity')
        check(rec.get('closed') is True and rec.get('childGroupAbsent') is True, 'science-not-terminal')
        check(isinstance(rec.get('artifacts'), list), 'supervisor-artifact-list')
        for pin in rec['artifacts']:
            verify_pin(p, pin)
            result['artifactPinsVerified'] += 1
        gates[kind+'ClosureQualified'] = (
            rec.get('supervisorSuccess') is True and rec.get('returncode') == 0
            and rec.get('runtimeIdentityVerified') is True
            and rec.get('protectedInputsUnchanged') is True and rec.get('candidateOutputsUnchanged') is True
            and rec.get('rssSamples', 0) > 0 and 0 < rec.get('sampledPeakRSSBytes', 0) <= 1610612736
            and 0 <= rec.get('elapsedSeconds', -1) <= cap
            and 0 <= rec.get('logBytes', -1) <= 4194304
            and not any(rec.get(k) for k in ['signals','monitorErrors','exception','cleanupError','finalizationError',
                                             'finalWallCapExceeded','finalStorageCapExceeded']))
    check(analysis.get('practicalRulePass') is None and analysis.get('requiresReviewSupervisorClosure') is True,
          'analysis-premature-or-missing-qualification-boundary')
    check('performanceRulePass' in analysis and (analysis['performanceRulePass'] is None or type(analysis['performanceRulePass']) is bool), 'malformed-internal-performance-rule')
    gates['independentReviewPassed'] = (audit.get('pass') is True and audit.get('complete') is True
                                       and analysis.get('independentAuditPass') is True)
    gates['performanceRuleAvailable'] = type(analysis['performanceRulePass']) is bool
    result['gates'] = gates
    result['evidenceQualified'] = all(gates.values())
    result['performanceRulePass'] = analysis['performanceRulePass']
    result['practicalRulePass'] = result['evidenceQualified'] and analysis['performanceRulePass']
    result['decision'] = ('qualified-finite-runtime-center-screen' if result['practicalRulePass']
                          else 'rejected-fixed-practical-rule' if result['evidenceQualified'] else 'unqualified-evidence')
    result['failureReasons'] = [k for k, v in gates.items() if not v]
    result['sealSuccess'] = True
except Exception as exc:
    result['failureReasons'].append(str(exc) if type(exc) is ValueError else 'metadata-exception-'+type(exc).__name__)
    result['decision'] = 'unqualified-metadata-seal'

total = sum(f.stat().st_size for name in ['results','inputs','generation'] for f in (p/name).rglob('*') if f.is_file())
result['scientificBytesBeforeSealOutput'] = total
result['elapsedSeconds'] = time.monotonic()-started
if result['elapsedSeconds'] > 20:
    result.update(sealSuccess=False, evidenceQualified=False, practicalRulePass=False, decision='unqualified-metadata-seal')
    result['failureReasons'].append('metadata-final-wall-limit')
lock_bytes = (out/'qualification-seal.lock').stat().st_size
while True:
    payload = (json.dumps(result, indent=2, allow_nan=False)+'\n').encode()
    fits = len(payload)+lock_bytes <= 1048576 and total+len(payload) <= 218103808
    if fits or ('metadata-final-storage-limit' in result['failureReasons'] and result['sealSuccess'] is False):
        break
    # Keep the final failure record even if a previous observed overshoot used
    # the reserve. Such a closure is explicitly unqualified, never a cap pass.
    result.update(sealSuccess=False, evidenceQualified=False, practicalRulePass=False, decision='unqualified-metadata-seal')
    result['failureReasons'].append('metadata-final-storage-limit')
with (out/'qualification.json').open('xb') as f:
    f.write(payload)
print(json.dumps({k: result[k] for k in ['sealSuccess','evidenceQualified','practicalRulePass','decision','failureReasons']}))
sys.exit(0 if result['sealSuccess'] else 1)
