"""Bind explicit immutable saved-result identities for the fresh viewer.

Administrative file verification only: no scientific module imports, simulator,
reference, native query or checker execution. Run once in an unbound viewer copy.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

PACKAGE = 'research/m31-native-fresh-transfer-2026-10-17'
STAGES = ['generation', 'reference', 'browser', 'check']
SLOTS = ['fresh-a-t5', 'fresh-b-t5']
MARKER = "const BINDING_SHA='__BINDING_SHA__';"


def need(value, label):
    if not value:
        raise ValueError(label)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--viewer', required=True, type=Path)
    parser.add_argument('--identities', required=True, type=Path)
    args = parser.parse_args()
    root, viewer = args.root.resolve(strict=True), args.viewer.resolve(strict=True)
    need(viewer.is_dir(), 'existing unbound viewer directory')
    need(not (viewer / 'binding.json').exists(), 'single-use binding output')
    app = (viewer / 'app.js').read_text()
    need(app.count(MARKER) == 1, 'one unbound application marker')
    identity_bytes = args.identities.read_bytes()
    identity = parse(identity_bytes)
    need(identity['schema'] == 'm31-native-fresh-view-identities-v1' and identity['package'] == PACKAGE,
         'explicit fresh identity schema')
    need(re.fullmatch('[a-f0-9]{40}', identity['sourceCommit']) and
         re.fullmatch('[a-f0-9]{64}', identity['sourceManifestSha256']), 'explicit source identities')
    need(set(identity['stages']) == set(STAGES), 'all four explicit stage slots')
    pins, parsed = {}, {}

    def read(pin, expected_path=None):
        relative = pin['path']
        need(isinstance(relative, str) and not Path(relative).is_absolute()
             and all(p not in ['.', '..', ''] for p in relative.split('/')), 'canonical relative pin')
        need(expected_path is None or relative == expected_path, 'expected record path')
        need(type(pin['bytes']) is int and 0 < pin['bytes'] <= 33554432
             and re.fullmatch('[a-f0-9]{64}', pin['sha256']), 'saved record pin shape')
        file = root / relative
        need(file.is_file() and not file.is_symlink() and file.resolve() == file, 'canonical saved file')
        raw = file.read_bytes()
        need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'saved byte pin mismatch: ' + relative)
        exact = {key: pin[key] for key in ['path', 'bytes', 'sha256']}
        need(relative not in pins or pins[relative] == exact, 'conflicting saved pin')
        pins[relative] = exact
        if relative.endswith('.json'):
            parsed[relative] = parse(raw)
            return parsed[relative]
        return None

    manifest = read(identity['manifest'], PACKAGE + '/source-manifest.json')
    need(identity['manifest']['sha256'] == identity['sourceManifestSha256'], 'source manifest hash')
    publication = read(identity['publication'], PACKAGE + '/source-publication.json')
    need(publication['commit'] == identity['sourceCommit'] and
         publication['manifestSha256'] == identity['sourceManifestSha256'] and
         publication['manifestBytes'] == identity['manifest']['bytes'] and
         publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True,
         'published source identity')
    source_pins = {pin['path']: pin for pin in manifest['files']}
    need(len(source_pins) == len(manifest['files']), 'unique frozen source inventory')
    science_pin = source_pins[PACKAGE + '/source/science-config.json']
    science = read(science_pin)
    need(science['schema'] == 'm31-native-fresh-science-config-v1' and
         [row['id'] for row in science['slots']] == SLOTS, 'fixed saved-record slots')
    stages = {}
    for name in STAGES:
        declared = identity['stages'][name]
        need(set(declared) == {'attempt', 'output'}, 'explicit availability fields')
        stages[name] = declared
        for key, suffix in [('attempt', '-attempt.json'), ('output', '.json')]:
            if declared[key] is None:
                continue
            record = read(declared[key], PACKAGE + '/results/' + name + suffix)
            need(record['sourceCommit'] == identity['sourceCommit'] and
                 record['sourceManifestSha256'] == identity['sourceManifestSha256'], 'stage source association')
        if declared['attempt']:
            a = parsed[declared['attempt']['path']]
            need(a['schema'] == 'm31-native-fresh-attempt-v1' and a['stage'] == name, 'attempt identity')
            if a['status'] == 'completed':
                need(declared['output'] and a['outputBytes'] == declared['output']['bytes'] and
                     a['outputSha256'] == declared['output']['sha256'], 'completed output association')
    generation_pin = stages['generation']['output']
    if generation_pin:
        generation = parsed[generation_pin['path']]
        need(generation['schema'] == 'm31-native-fresh-generation-v1' and
             [row['id'] for row in generation['slots']] == SLOTS, 'two persisted slots')
        for row in generation['slots']:
            for key, directory in [('generation', 'generation'), ('input', 'inputs')]:
                if row.get(key):
                    read(row[key], PACKAGE + '/results/' + directory + '/' + row['id'] + '.json')
    dependencies = parse((viewer / 'DEPENDENCIES.json').read_bytes())
    need(dependencies['schema'] == 'm31-native-fresh-view-dependencies-v1', 'viewer dependency schema')
    need([p['path'] for p in dependencies['files']] == ['outputs/step02b-source/vendor/three.module.js',
         'outputs/step02b-source/vendor/three.core.js', 'outputs/step02b-source/vendor/OrbitControls.js'],
         'unchanged Three.js dependency paths')
    for pin in dependencies['files']:
        read(pin)
    need(len(pins) <= 40 and sum(p['bytes'] for p in pins.values()) <= 64 * 1024 * 1024,
         'finite viewer inventory')
    binding = {'schema': 'm31-native-fresh-view-binding-v1', 'package': PACKAGE,
               'sourceCommit': identity['sourceCommit'], 'sourceManifestSha256': identity['sourceManifestSha256'],
               'manifest': identity['manifest'], 'publication': identity['publication'], 'science': science_pin,
               'stages': stages, 'dependencies': dependencies['files'], 'pins': list(pins.values()),
               'identityDocumentSha256': digest(identity_bytes), 'scope': 'Actual saved frames and qualified final native words only.'}
    # Preserve stage order for the readable binding; scientific source/results are never written.
    bound = json.dumps(binding, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii') + b'\n'
    need(len(bound) <= 131072, 'binding cap')
    for relative, pin in pins.items():
        raw = (root / relative).read_bytes()
        need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'saved record changed while binding')
    need((viewer / 'app.js').read_text() == app, 'application changed while binding')
    with (viewer / 'binding.json').open('xb') as stream:
        stream.write(bound)
    (viewer / 'app.js').write_text(app.replace(MARKER, "const BINDING_SHA='" + digest(bound) + "';"))
    print(json.dumps({'bindingBytes': len(bound), 'bindingSha256': digest(bound),
                      'verifiedSavedPins': len(pins), 'scientificExecution': False}))


if __name__ == '__main__':
    main()
