"""Pinned provenance and saved-generation checks; no producer imports."""
from pathlib import Path
from fractions import Fraction
import datetime
import hashlib
import importlib.util
import json
import os
import sys

NAME = 'research/m31-native-fresh-transfer-2026-10-17'
FILE_CAP = 32 * 1024 * 1024
SLOTS = [('fresh-a-t5', 26171711, ['F', 'L']), ('fresh-b-t5', 26171712, ['L', 'F'])]
CONTROL_IDS = ['positive', 'distant-zero', 'raw-force', 'order-incompatible']

def need(value, code):
    if not value:
        raise ValueError(code)

def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def identity(path):
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            size += len(data)
            digest.update(data)
    return {'bytes': size, 'sha256': digest.hexdigest()}

def pin(root, path):
    return {'path': path.relative_to(root).as_posix(), **identity(path)}

def verify(root, value):
    relative = value['path']
    need(type(relative) is str and not Path(relative).is_absolute()
         and all(p not in ('', '.', '..') for p in relative.split('/')), 'pin-path')
    path = root / relative
    need(path.is_file() and path.resolve() == path, 'pin-regular-canonical')
    need(identity(path) == {k: value[k] for k in ('bytes', 'sha256')}, 'pin-bytes')
    return path

def parse(data):
    def pairs(items):
        answer = {}
        for key, value in items:
            need(key not in answer, 'duplicate-json-key')
            answer[key] = value
        return answer
    def bad(_value):
        raise ValueError('nonfinite-json')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad)

def load(path):
    need(path.stat().st_size <= FILE_CAP, 'json-file-cap')
    return parse(path.read_bytes())

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')

def semantic_digest(identifier, value):
    return hashlib.sha256(canonical({'domain': 'm31-moving-admission/input/v1', 'id': identifier, 'input': value})).hexdigest()

def write(root, path, value, cap=FILE_CAP):
    data = json.dumps(value, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode() + b'\n'
    need(len(data) <= cap, 'output-byte-cap')
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return pin(root, path)

def gate(root, expected, commit, stage, entry):
    need(root.is_absolute() and root.resolve() == root, 'root-canonical')
    package = root / NAME
    need(entry.resolve() == package / 'source' / (stage + '.py' if stage != 'check' else 'check.py'), 'entry-location')
    need(os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated', 'dispatch-attestation')
    need(sys.platform == 'darwin', 'darwin-runtime')
    need(len(expected) == 64 and len(commit) == 40 and all(c in '0123456789abcdef' for c in expected + commit), 'identity-arguments')
    manifest_path = package / 'source-manifest.json'
    manifest_pin = pin(root, manifest_path)
    need(manifest_pin['sha256'] == expected, 'manifest-sha')
    manifest = load(manifest_path)
    by_path = {p['path']: p for p in manifest['files']}
    need(len(by_path) == len(manifest['files']), 'duplicate-source-pin')
    for item in manifest['files']:
        verify(root, item)
    for name in ['fresh_support.py', 'science-config.json', 'checker-contract.json', entry.name]:
        need(NAME + '/source/' + name in by_path, 'required-source-pin')
    runtime = manifest['runtime']['python']
    need(identity(Path(sys.executable).resolve()) == {k: runtime[k] for k in ('bytes', 'sha256')}, 'python-runtime')
    science = load(package / 'source/science-config.json')
    need(science['schema'] == 'm31-native-fresh-science-config-v1' and science['referenceMaxDrones'] == 180, 'science-schema-cap')
    need(science['slots'] == [{'id': i, 'seed': s, 't': 5, 'n': 64, 'methods': m} for i, s, m in SLOTS], 'fixed-slots')
    need(science['generation'] == {'count': 64, 'duration': 5, 'dt': .0025, 'mode': 'boids', 'search': 'grid', 'filter': 'wall-priority', 'record': True, 'frameEvery': .2, 'factoryVariant': 'wide', 'airflow': 'off', 'observation': 'ideal'}, 'fixed-generator')
    need([x['id'] for x in science['movingControls']] == CONTROL_IDS, 'fixed-moving-controls')
    need([x['id'] for x in science['retainedInputs']] == ['run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10'], 'six-retained-inputs')
    for row in science['retainedInputs']:
        need(by_path.get(row['input']['path']) == row['input'], 'retained-input-source-binding')
    need(science['launchCutoffUtc'] == '2026-10-17T03:00:00+00:00'
         and datetime.datetime.now(datetime.timezone.utc) < datetime.datetime.fromisoformat(science['launchCutoffUtc']), 'launch-cutoff')
    attempt_path = package / 'results' / (stage + '-attempt.json')
    attempt, publication = load(attempt_path), load(package / 'source-publication.json')
    need(attempt['stage'] == stage and attempt['status'] == 'started' and attempt['sourceCommit'] == commit
         and attempt['sourceManifestSha256'] == expected, 'current-attempt')
    need(publication['commit'] == commit and publication['manifestSha256'] == expected
         and publication['manifestBytes'] == manifest_pin['bytes'] and publication['manifestPath'] == manifest_pin['path']
         and publication['verifiedFilePins'] == len(manifest['files']) and publication['remoteBytesEqualLocal'] is True
         and publication['committedBytesEqualLocal'] is True
         and datetime.datetime.fromisoformat(publication['verifiedUtc']) <= datetime.datetime.fromisoformat(attempt['startedUtc']), 'publication-binding')
    protected = [manifest_pin, pin(root, package / 'source-publication.json'), pin(root, attempt_path)]
    return {'root': root, 'package': package, 'manifest': manifest, 'protected': protected,
            'science': science, 'commit': commit, 'expected': expected, 'byPath': by_path}

def preserve(ctx):
    for item in ctx['manifest']['files'] + ctx['protected']:
        verify(ctx['root'], item)

def read_bound(ctx, descriptor):
    file = verify(ctx['root'], descriptor)
    ctx['protected'].append(descriptor)
    return load(file)

def closed_stage(ctx, stage):
    root, results = ctx['root'], ctx['package'] / 'results'
    ap, op = pin(root, results / (stage + '-attempt.json')), pin(root, results / (stage + '.json'))
    attempt, output = read_bound(ctx, ap), read_bound(ctx, op)
    need(attempt['stage'] == stage and attempt['status'] == 'completed' and attempt['exitCode'] == 0
         and attempt['preservationPassed'] is True and attempt['sourceCommit'] == ctx['commit']
         and attempt['sourceManifestSha256'] == ctx['expected']
         and attempt['outputBytes'] == op['bytes'] and attempt['outputSha256'] == op['sha256'], 'closed-stage:' + stage)
    need(output['sourceCommit'] == ctx['commit'] and output['sourceManifestSha256'] == ctx['expected'], 'stage-source:' + stage)
    return output, op

def load_module(ctx, name, fixed_sha=None):
    relative = NAME + '/source/' + name
    descriptor = ctx['byPath'].get(relative)
    need(descriptor is not None and (fixed_sha is None or descriptor['sha256'] == fixed_sha), 'helper-fixed-pin')
    path = verify(ctx['root'], descriptor)
    spec = importlib.util.spec_from_file_location('_fresh_' + name.replace('.', '_'), path)
    need(spec is not None and spec.loader is not None, 'helper-loader')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def word_fraction(word):
    need(type(word) is str and len(word) == 16 and all(c in '0123456789abcdef' for c in word), 'raw-word')
    b = int(word, 16)
    e, m = (b >> 52) & 2047, b & ((1 << 52) - 1)
    need(e != 2047, 'raw-nonfinite')
    if e:
        m += 1 << 52
        shift = e - 1023 - 52
    else:
        shift = -1074
    value = Fraction(m << shift) if shift >= 0 else Fraction(m, 1 << -shift)
    return -value if b >> 63 else value

def raw_shape(value, count, positive=True):
    need(type(value) is dict and set(value) == {'drones'} and type(value['drones']) is list and len(value['drones']) == count, 'raw-shape')
    for identifier, row in enumerate(value['drones']):
        need(set(row) == {'id', 'state'} and type(row['id']) is int and row['id'] == identifier
             and type(row['state']) is list and len(row['state']) == 17, 'raw-row')
        exact = [word_fraction(w) for w in row['state']]
        need(not positive or all(v > 0 for v in exact[13:]), 'raw-positive-forces')

def pose_words(value):
    return [w for d in value['drones'] for w in d['state'][:3] + d['state'][6:10]]

def movement(initial, final):
    changed = not same(initial, final)
    p0 = [[word_fraction(w) for w in d['state'][:3]] for d in initial['drones']]
    pt = [[word_fraction(w) for w in d['state'][:3]] for d in final['drones']]
    witness = next(({'id': i, 'axis': k} for i in range(1, 64) for k in range(3)
                    if (pt[i][k] - pt[0][k]) != (p0[i][k] - p0[0][k])), None)
    return {'stateChanged': changed, 'relativeGeometryChanged': witness is not None,
            'witness': witness, 'passed': changed and witness is not None}

def validate_generation(ctx, index):
    science = ctx['science']
    need(index['schema'] == 'm31-native-fresh-generation-v1' and index['complete'] is True
         and index['inputsAndSourcesPreserved'] is True and index['errors'] == [], 'generation-complete')
    need(len(index['slots']) == 2 and len(index['controls']) == 4, 'generation-denominator')
    journal_path = verify(ctx['root'], index['journal'])
    ctx['protected'].append(index['journal'])
    need(journal_path.stat().st_size <= 4 * 1024 * 1024, 'generation-journal-cap')
    events = [parse(line) for line in journal_path.read_bytes().splitlines()]
    need([x['sequence'] for x in events] == list(range(len(events))), 'journal-sequence')
    raws, motions, expected_events = {}, {}, []
    for retained in science['retainedInputs']:
        old_raw = read_bound(ctx, retained['input'])
        raw_shape(old_raw, 64)
        need(hashlib.sha256(canonical(old_raw)).hexdigest() == retained['rawContentSha256'], 'retained-canonical-raw-hash')
    for slot, fixed in zip(index['slots'], science['slots']):
        need(all(same(slot[k], fixed[k]) for k in fixed) and slot['status'] == 'captured', 'slot-fixed-capture')
        identifier = fixed['id']
        record = read_bound(ctx, slot['generation'])
        need(record['schema'] == 'm31-native-fresh-generation-record-v1' and record['id'] == identifier
             and record['seed'] == fixed['seed'] and record['status'] == 'captured' and record['error'] is None
             and record['sourceCommit'] == ctx['commit'] and record['sourceManifestSha256'] == ctx['expected'], 'generation-record')
        need(same(record['requested'], science['generation']), 'generation-request')
        options = {k: science['generation'][k] for k in ('count', 'duration', 'dt', 'mode', 'search', 'filter', 'record', 'frameEvery')}
        options['seed'] = fixed['seed']
        need(record['generatorOptions'] == options, 'generator-options')
        for key in ('initial', 'returnedInitial', 'final', 'snapshot'):
            raw_shape(record[key], 64)
        need(same(record['initial'], record['returnedInitial']) and same(record['final'], record['snapshot']), 'full-state-return-binding')
        frames, callbacks = record['frames'], record['callbacks']
        need([f['t'] for f in frames] == [i / 5 for i in range(26)], 'pose-cadence')
        for frame in frames:
            need(len(frame['words']) == 448, 'frame-width')
            for w in frame['words']:
                word_fraction(w)
        need([c['t'] for c in callbacks] == [0, 5] and all(c['stopReason'] is None for c in callbacks), 'normal-terminal-callbacks')
        need(pose_words(record['initial']) == frames[0]['words'] and pose_words(record['snapshot']) == frames[-1]['words'], 'full-state-pose-binding')
        returned = record['returnedSummary']
        need(returned['metrics']['end'] == 5 and returned['metrics']['stopReason'] is None, 'normal-terminal-return')
        need(returned['config'] == {'filter': 'wall-priority', 'seed': fixed['seed'], 'count': 64, 'mode': 'boids', 'dt': .0025, 'duration': 5, 'search': 'grid', 'course': 'factory-v1', 'airflow': 'off', 'observation': 'ideal'}
             and returned['recording'] == {'cadence': .2, 'streamed': True}, 'returned-generator-identity')
        raw = read_bound(ctx, slot['input'])
        need(same(raw, record['snapshot']) and slot['semanticInputSha256'] == semantic_digest(identifier, raw), 'target-raw-capture-binding')
        content_sha = hashlib.sha256(canonical(raw)).hexdigest()
        matches = [r['id'] for r in science['retainedInputs'] if r['rawContentSha256'] == content_sha]
        novelty = {'comparedCount': 6, 'matches': matches, 'passed': not matches, 'rawContentSha256': content_sha, 'retained': science['retainedInputs']}
        need(novelty['passed'] and same(slot['novelAgainstRetained'], novelty) and same(record['novelAgainstRetained'], novelty), 'novel-target-raw-content')
        move = movement(record['initial'], raw)
        need(move['passed'] and same(move, record['motion']) and same(move, slot['motion']), 'relative-geometry-motion')
        raws[identifier], motions[identifier] = raw, move
        expected_events.append({'kind': 'generation-start', 'body': {'id': identifier, 'seed': fixed['seed'], 'options': options}})
        for frame in frames:
            expected_events.append({'kind': 'pose', 'body': {'id': identifier, **frame}})
            if frame['t'] in (0, 5):
                expected_events.append({'kind': 'full-state', 'body': {'id': identifier, 't': frame['t'], 'stopReason': None, 'input': record['initial'] if frame['t'] == 0 else record['snapshot']}})
        expected_events.append({'kind': 'generation-complete', 'body': slot})
    need(same(events, [dict(sequence=i, **e) for i, e in enumerate(expected_events)]), 'generation-journal-binding')
    for position, (row, fixed) in enumerate(zip(index['controls'], science['movingControls'])):
        need(row['id'] == fixed['id'] and row['n'] == len(fixed['drones']) and row['n'] == (3 if position == 0 else 2)
             and row['methods'] == ['F', 'L'] and row['expectedReference'] == science['expectedReference'][position]
             and row['expectedNative'] == science['expectedNative'][position], 'control-schedule')
        raw = read_bound(ctx, row['input'])
        raw_shape(raw, row['n'], positive=False)
        need(row['semanticInputSha256'] == semantic_digest(row['id'], raw), 'control-semantic-input')
        raws[row['id']] = raw
    return raws, motions
