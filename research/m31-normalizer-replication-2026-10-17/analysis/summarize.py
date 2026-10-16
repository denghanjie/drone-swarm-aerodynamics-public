"""Saved-record descriptive summary only; never imports scientific modules."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import statistics

package = Path(__file__).resolve().parents[1]
root = package.parents[1]
results = package / 'results'
check = json.loads((results / 'check.json').read_text())
index = json.loads((results / 'index.json').read_text())
rows = []
for result in check['performance']:
    slot = next(s for s in index['scheduled'] if s['id'] == result['id'])
    pairs = []
    for repetition in range(4):
        calls = {d['arm']: d for d in slot['calls'] if d['repetition'] == repetition}
        a, b = (int(calls[arm]['wallNs']) for arm in ('baseline', 'candidate'))
        ratio = Fraction(b, a)
        reported = result['pairs'][repetition]
        assert reported['baselineWallNs'] == str(a) and reported['candidateWallNs'] == str(b)
        assert ratio == Fraction(int(reported['ratio']['n']), int(reported['ratio']['d']))
        pairs.append({'repetition': repetition, 'baselineWallNs': str(a),
                      'candidateWallNs': str(b), 'ratio': float(ratio)})
    ratios = sorted(Fraction(int(x['candidateWallNs']), int(x['baselineWallNs'])) for x in pairs)
    median = (ratios[1] + ratios[2]) / 2
    wins = sum(r < 1 for r in ratios)
    passed = median <= Fraction(9, 10) and wins >= 3
    assert median == Fraction(int(result['medianRatio']['n']), int(result['medianRatio']['d']))
    assert result['wins'] == wins and result['benefitPassed'] is passed
    row = {'id': result['id'], 'pairs': pairs, 'medianPairedRatio': float(median),
           'medianPairedRatioExact': {'n': str(median.numerator), 'd': str(median.denominator)},
           'candidateWins': wins, 'benefitPassed': passed}
    for arm in ('baseline', 'candidate'):
        wall = [int(x[arm + 'WallNs']) / 1e6 for x in pairs]
        method = [int(d['methodNs']) / 1e6 for d in slot['calls'] if d['arm'] == arm]
        row[arm] = {'medianWallMs': statistics.median(wall), 'minWallMs': min(wall),
                    'maxWallMs': max(wall), 'medianMethodMs': statistics.median(method)}
    rows.append(row)

assert len(rows) == 6 and len(index['calls']) == 56
summary = {'schema': 'm31-normalizer-descriptive-summary-v1',
           'sourceCommit': check['sourceCommit'],
           'scope': 'Descriptive six-state paired isolated-worker comparison on two trajectories; no population confidence interval.',
           'rule': 'Each state must have median paired candidate/baseline <=0.9 and at least3/4 strict wins, plus all numerical gates.',
           'gates': {k: check[k] for k in ('recordIntegrityPassed', 'equivalencePassed', 'admissionPassed', 'benefitPassed', 'fixedControlsPassed')},
           'counts': check['counts'], 'states': rows,
           'references': len(check['referenceFiles']),
           'corruptionControls': len(check['corruptionControls']),
           'cacheControls': len(check['cacheControls']),
           'inputs': []}
for name in ('check.json', 'index.json'):
    path = results / name
    data = path.read_bytes()
    summary['inputs'].append({'path': path.relative_to(root).as_posix(), 'bytes': len(data),
                              'sha256': hashlib.sha256(data).hexdigest()})
output = package / 'analysis/descriptive-summary.json'
with output.open('x') as stream:
    json.dump(summary, stream, indent=2, allow_nan=False)
    stream.write('\n')
print(json.dumps({'states': len(rows), 'passingBenefitStates': sum(r['benefitPassed'] for r in rows),
                  'output': output.relative_to(root).as_posix()}))
