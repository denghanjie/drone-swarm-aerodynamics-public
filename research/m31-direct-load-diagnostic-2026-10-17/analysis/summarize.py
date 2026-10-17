"""Saved-only registered readout; no scientific source imports or solver calls."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]


def q(value):
    return F(int(value['n']), int(value['d']))


def read(relative):
    path = PACKAGE / relative
    raw = path.read_bytes()
    return json.loads(raw), {'path': str(path.relative_to(ROOT)), 'bytes': len(raw),
                             'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    records, pins = {}, []
    for name in ('analyze', 'analyze-attempt', 'check', 'check-attempt'):
        records[name], pin = read('results/' + name + '.json')
        pins.append(pin)
    for name in ('analyze', 'check'):
        attempt = records[name + '-attempt']
        pin = next(p for p in pins if p['path'].endswith('/' + name + '.json'))
        assert attempt['status'] == 'completed' and attempt['exitCode'] == 0
        assert attempt['firstFailure'] is None
        assert attempt['outputSha256'] == pin['sha256'] and attempt['outputBytes'] == pin['bytes']
    assert records['check']['passed'] is True and records['check']['firstFailure'] is None
    states = []
    for state, checked in zip(records['analyze']['states'], records['check']['outcomes']):
        assert state['id'] == checked['id']
        full, omit = state['proposals']
        assert full['id'] == 'full' and omit['id'] == 'omit10'
        audits = {}
        for name in ('A', 'B', 'C'):
            actual = {k: omit[name][k] for k in ('maxErrors', 'tiers')}
            assert actual == checked['omit10'][name]
            audits[name] = {
                'maxErrorsExact': actual['maxErrors'],
                'maxErrorsDisplay': {cat: [float(q(b['l'])), float(q(b['u']))]
                                    for cat, b in actual['maxErrors'].items()},
                'tiers': actual['tiers']}
        sufficient = equal_k = equal_roots = 0
        for b, c in zip(omit['B']['rows'], omit['C']['rows']):
            assert (b['i'], b['r']) == (c['i'], c['r'])
            sufficient += q(c['p']['l']) * q(c['p']['u']) >= 1
            equal_k += b['k'] == c['k']
            equal_roots += b['xstar'] == c['xstar']
        assert len(omit['B']['rows']) == len(omit['C']['rows']) == 256
        if sufficient == 256:
            assert equal_k == equal_roots == 256 and omit['B']['K'] == omit['C']['K']
        states.append({
            'id': state['id'], 'positiveTerms': state['positiveTerms'],
            'omittedCount': len(state['mask']),
            'omittedFractionDisplay': len(state['mask']) / state['positiveTerms'],
            'fullControl': checked['full'], 'omission': audits,
            'BC': {'rows': 256, 'sufficientConditionRows': sufficient,
                   'conditionNotSatisfiedRows': 256 - sufficient,
                   'equalLocalFactorRows': equal_k, 'equalRootRows': equal_roots,
                   'equalGlobalFactor': omit['B']['K'] == omit['C']['K'],
                   'equalErrorIntervals': omit['B']['maxErrors'] == omit['C']['maxErrors']}})
    assert len(states) == 6
    report = {
        'schema': 'm31-direct-load-saved-summary-v1',
        'sourceCommit': records['analyze-attempt']['sourceCommit'], 'pins': pins,
        'decision': records['check']['decision'],
        'fullControlStrictPass': records['check']['fullControlStrictPass'],
        'states': states,
        'interpretation': 'Exact bounds and statuses retained. Decimal conversions are display only. '
                          'All six exposed states remain; no physical or speed claim.'}
    destination = PACKAGE / 'analysis/summary.json'
    with destination.open('x') as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')
    for state in states:
        print(state['id'], state['positiveTerms'], state['omittedCount'],
              {cat: f'{bounds[1]:.6g}' for cat, bounds in state['omission']['A']['maxErrorsDisplay'].items()},
              state['BC'])


if __name__ == '__main__':
    main()
