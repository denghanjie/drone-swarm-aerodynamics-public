"""Project existing native saved outputs for display; no model imports or execution.

Source-only draft. Parent runs this administrative adapter after accepting its
source and deciding the explicit audit binding. Every output is exclusive.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

PACKAGE = 'research/m31-native-load-baseline-2026-10-17'
AUDIT = 'research/m31-native-saved-audit-2026-10-17'
AUDIT_SOURCE = 'eb049deb66c4c7aee78826b2eecde8281d02a1b9'
AUDIT_PINS = {
    'manifest': ('source-manifest.json', 69013, '7ca777cfe98e6498d8cc789244f3f3d14223a45f807c60c7e8a99913d64ac3c1'),
    'publication': ('source-publication.json', 867, '7325bc2f5fd7b9f497d321df75604e76f70045a80e19f71be443241f25584992'),
    'attempt': ('results/check-attempt.json', 1966, 'd9531ae0ebde1385ec8aa212ffb8ca630adcdf95499bf61aed5be47fbe7d3434'),
    'report': ('results/check.json', 52914, 'e4b93e1b5d03f378b2d7ac254256fcb7deb2e3371dc4dd70136ec6c376974080'),
}
SOURCE = 'e6f99b140c70887fa0ed05c14574221eb5db12da'
MANIFEST = '8bae9d039d2fbfd40a34085b1bc00f3c76725c57675ea2a681121add083f4019'
BROWSER = (5353146, '2f1a599000e782f1ac50163cf05fd046b7fb3c20e9ed350c7566b8c9fce900fe')
ATTEMPT = (1201, '2d9db1aa6db0f61118ab735a7db6d2dca919a0a48d94b0a1cf49a4f5e9ad2c33')
PLAN = [{'id': run + '-t' + str(t), 'runId': run, 't': t}
        for run in ['run-a', 'run-b'] for t in [0, 5, 10]]


def need(value, label):
    if not value:
        raise ValueError(label)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def words(value, length):
    return isinstance(value, list) and len(value) == length and all(
        isinstance(word, str) and re.fullmatch('[a-f0-9]{16}', word) for word in value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--audit-binding', type=Path,
                        help='Reviewed explicit audit pin/identity document; omit to preserve Pending.')
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    output = args.output.resolve(strict=True)
    need(output.is_dir(), 'existing output source directory required')
    need(not any((output / name).exists() for name in ['display-data.json', 'binding.json']), 'preserve previous display build')
    app = (output / 'app.js').read_text()
    need(app.count("const BINDING_SHA='__BINDING_SHA__';") == 1, 'one unbound app marker required')
    pins = {}

    def raw_pin(relative, expected=None):
        need(not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'canonical path required')
        file = root / relative
        need(file.is_file() and not file.is_symlink() and file.resolve() == file, 'canonical saved file required')
        need(file.stat().st_size <= 16 * 1024 * 1024, 'saved file size cap')
        raw = file.read_bytes()
        pin = {'path': relative, 'bytes': len(raw), 'sha256': digest(raw)}
        if expected is not None:
            need((pin['bytes'], pin['sha256']) == expected, 'accepted saved pin mismatch: ' + relative)
        pins[relative] = pin
        return raw

    def load(relative, expected=None):
        return json.loads(raw_pin(relative, expected), object_pairs_hook=unique)

    manifest = load(PACKAGE + '/source-manifest.json')
    need(pins[PACKAGE + '/source-manifest.json']['sha256'] == MANIFEST, 'native source manifest identity')
    source_pins = {pin['path']: pin for pin in manifest['files']}
    checker_pin = source_pins[PACKAGE + '/source/check.py']
    raw_pin(checker_pin['path'], (checker_pin['bytes'], checker_pin['sha256']))
    publication = load(PACKAGE + '/source-publication.json')
    need(publication['commit'] == SOURCE and publication['manifestSha256'] == MANIFEST and
         publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True,
         'native publication identity')
    config = load(PACKAGE + '/config.json')
    need(pins[PACKAGE + '/config.json'] == source_pins[PACKAGE + '/config.json'], 'configuration frozen pin')
    need(len(config['cases']) == len(PLAN), 'exact six-case denominator')
    browser = load(PACKAGE + '/results/browser.json', BROWSER)
    attempt = load(PACKAGE + '/results/browser-attempt.json', ATTEMPT)
    journal = browser['journal']
    raw_pin(journal['path'], (journal['bytes'], journal['sha256']))
    need(browser['schema'] == 'm31-native-browser-qualification-v1' and browser['sourceCommit'] == SOURCE
         and browser['sourceManifestSha256'] == MANIFEST and browser['complete'] is True
         and browser['completedTargetCalls'] == browser['expectedTargetCalls'] == len(browser['calls']) == 12,
         'native browser schedule identity')
    need(attempt['schema'] == 'm31-native-load-attempt-v1' and attempt['sourceCommit'] == SOURCE
         and attempt['sourceManifestSha256'] == MANIFEST and attempt['status'] == 'failed'
         and attempt['childExitCode'] == 0 and attempt['exitCode'] == 1 and attempt['cleanupError'] is True
         and attempt['firstFailure']['type'] == 'PermissionError', 'preserve original failed supervision')
    schedule = [(p['id'], method) for i, p in enumerate(PLAN)
                for method in (['L', 'F'] if i % 2 else ['F', 'L'])]
    need([(call['caseId'], call['method']) for call in browser['calls']] == schedule, 'fixed twelve-call schedule')
    need([call['sequence'] for call in browser['calls']] == list(range(12)), 'native output field addresses')
    states = []
    for p, case in zip(PLAN, config['cases']):
        need(case['id'] == p['id'] and case['n'] == 64, 'fixed six states')
        raw = load(case['input']['path'], (case['input']['bytes'], case['input']['sha256']))
        need(pins[case['input']['path']] == source_pins[case['input']['path']], 'raw input frozen pin')
        ids = [row['id'] for row in raw['drones']]
        need(len(ids) == 64 and ids == sorted(set(ids)), 'raw stable IDs')
        need(all(words(row['state'], 17) for row in raw['drones']), 'raw state word shape')
        semantic = digest(canonical({'domain': 'm31-moving-admission/input/v1', 'id': p['id'], 'input': raw}))
        need(semantic == case['semanticInputSha256'], 'semantic raw identity')
        state = {**p, 'ids': ids, 'poseWords': [row['state'][:3] + row['state'][6:10] for row in raw['drones']], 'methods': {}}
        for method in ['F', 'L']:
            call = next(row for row in browser['calls'] if row['caseId'] == p['id'] and row['method'] == method)
            evidence = call['evidence']
            need(call['semanticInputSha256'] == semantic and call['inputFileSha256'] == case['input']['sha256']
                 and call['inputUnchanged'] is True, 'native call identity')
            need(evidence['schema'] == 'm31-native-load-evidence-v1' and evidence['caseId'] == p['id']
                 and evidence['method'] == method and evidence['semanticInputSha256'] == semantic
                 and evidence['inputFileSha256'] == case['input']['sha256'], 'native evidence identity')
            need(evidence['raw'] == raw['drones'] and evidence['ids'] == ids, 'native raw/ID ownership')
            need(evidence['status'] == 'native-success' and evidence['reason'] is None, 'accepted recorded native status')
            need([row['id'] for row in evidence['prepared']] == ids and
                 all(row['center'] == inp['state'][:3] for row, inp in zip(evidence['prepared'], raw['drones'])),
                 'recorded center equality')
            loads = evidence['loads']
            need([row['id'] for row in loads] == ids and all(words(row['rotor'], 4)
                 and words([row['collective']], 1) and words(row['worldForce'], 3)
                 and words(row['worldMoment'], 3) for row in loads), 'actual delivered load words')
            state['methods'][method] = {'sequence': call['sequence'], 'status': evidence['status'],
                'reason': evidence['reason'], 'inputFileSha256': call['inputFileSha256'],
                'semanticInputSha256': semantic, 'loads': loads,
                'loadWordsSha256': digest(canonical({'ids': ids, 'loads': loads})),
                'positiveTerms': len(evidence['coefficients']['K']),
                'fieldPath': 'calls[' + str(call['sequence']) + '].evidence'}
        states.append(state)
    audit = None
    if args.audit_binding:
        audit = json.loads(args.audit_binding.read_bytes(), object_pairs_hook=unique)
        need(audit['schema'] == 'm31-native-saved-audit-view-link-v1' and audit['package'] == AUDIT
             and audit['sourceCommit'] == AUDIT_SOURCE,
             'reviewed audit binding schema')
        # Exact scientific/operational gate validation occurs in the viewer's audit verifier.
        # Only pin existing records here; no checker or reference module is executed.
        for name in ['manifest', 'publication', 'attempt', 'report']:
            pin = audit[name]
            relative, count, sha256 = AUDIT_PINS[name]
            need(pin == {'path': AUDIT + '/' + relative, 'bytes': count, 'sha256': sha256},
                 'accepted independent audit pin')
            load(pin['path'], (pin['bytes'], pin['sha256']))
    model = {'schema': 'm31-native-load-display-v1', 'package': PACKAGE,
        'sourceCommit': SOURCE, 'sourceManifestSha256': MANIFEST,
        'nativeBrowser': {'internalComplete': browser['complete'], 'returnedCalls': len(browser['calls']),
                         'browserProduct': browser['browser']['product'], 'browserOutputSha256': BROWSER[1]},
        'originalAttempt': {key: attempt[key] for key in ['status', 'childExitCode', 'exitCode', 'cleanupError', 'firstFailure']},
        'states': states}
    encoded = canonical(model) + b'\n'
    binding = {'schema': 'm31-native-load-view-binding-v1', 'package': PACKAGE,
        'sourceCommit': SOURCE, 'sourceManifestSha256': MANIFEST, 'schedule': PLAN,
        'display': {'path': 'display-data.json', 'bytes': len(encoded), 'sha256': digest(encoded)},
        'pins': list(pins.values()), 'audit': audit}
    bound = canonical(binding) + b'\n'
    for relative, pin in pins.items():
        raw = (root / relative).read_bytes()
        need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'saved record changed during projection')
    with (output / 'display-data.json').open('xb') as stream:
        stream.write(encoded)
    with (output / 'binding.json').open('xb') as stream:
        stream.write(bound)
    (output / 'app.js').write_text(app.replace("const BINDING_SHA='__BINDING_SHA__';",
                                           "const BINDING_SHA='" + digest(bound) + "';"))


if __name__ == '__main__':
    main()
