#!/usr/bin/env python3
"""Single-use saved-failure export. No native/scientific modules or subprocesses."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import signal
import struct
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
OUT = BASE / 'results'
OLD = ROOT / 'research/m31-buffered-candidates-2026-10-20'
CORRECTED = ROOT / 'research/m31-buffered-candidates-corrected-2026-10-20'
LIMIT = 10 * 1048576
PINS, BINDINGS = {}, []
START, WRITTEN = None, 0


class EvidenceFailure(Exception):
    pass


def need(ok, message):
    if not ok:
        raise EvidenceFailure(message)


def tick(*_):
    need(START is not None and time.monotonic() - START < 30, 'export wall budget')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rel(path):
    return path.relative_to(ROOT).as_posix()


def compact(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode()


def pairs(items):
    obj = {}
    for key, value in items:
        need(key not in obj, 'duplicate JSON key')
        obj[key] = value
    return obj


def parse(data):
    def bad(_):
        raise EvidenceFailure('nonfinite JSON constant')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad)


def read_bytes(path, gated=True):
    tick()
    name = rel(path)
    need(path.is_file() and not path.is_symlink(), 'missing/nonregular file: ' + name)
    size = path.stat().st_size
    need(0 < size <= 64 * 1048576, 'source file size')
    data = path.read_bytes()
    need(len(data) == size, 'file changed during read')
    if gated:
        need(name in PINS and PINS[name] == {'bytes': size, 'sha256': sha(data)}, 'manifest pin: ' + name)
    return data


def read(path):
    return parse(read_bytes(path))


def write(name, value, terminal=False):
    global WRITTEN
    data = compact(value) + b'\n'
    need(WRITTEN + len(data) <= LIMIT - (0 if terminal else 16384), 'export output budget')
    with (OUT / name).open('xb') as stream:
        stream.write(data)
    WRITTEN += len(data)
    return {'file': name, 'bytes': len(data), 'sha256': sha(data)}


def number(word):
    need(isinstance(word, str) and re.fullmatch(r'[0-9a-f]{16}', word), 'binary64 word')
    value = struct.unpack('>d', bytes.fromhex(word))[0]
    need(math.isfinite(value), 'nonfinite saved word')
    return value


def id_word(value):
    return struct.pack('>d', value).hex()


def input_record(value, duplicate=False):
    need(set(value) == {'drones'} and isinstance(value['drones'], list), 'input record shape')
    drones, ids = [], []
    for item in value['drones']:
        need(set(item) == {'id', 'state'}, 'drone record shape')
        ident, state = item['id'], item['state']
        need(type(ident) is int and 0 <= ident < 2**53, 'safe input ID')
        need(isinstance(state, list) and len(state) == 17, 'input state shape')
        for word in state:
            number(word)
        drones.append({'id': ident, 'state': state})
        ids.append(ident)
    need(0 < len(ids) <= 5000 and (len(set(ids)) < len(ids)) == duplicate, 'input identity/count')
    return {'drones': drones}


def gate():
    manifest_bytes = read_bytes(BASE / 'source-manifest.json', False)
    manifest = parse(manifest_bytes)
    receipt = parse(read_bytes(BASE / 'source-publication.json', False))
    need(receipt['manifestSha256'] == sha(manifest_bytes), 'public manifest hash')
    need(receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True,
         'exact public source prerequisite')
    need(re.fullmatch(r'[0-9a-f]{40}', receipt['commit']) is not None, 'full public source commit')
    for pin in manifest['files']:
        name = pin['path']
        need(isinstance(name, str) and not Path(name).is_absolute() and '..' not in Path(name).parts
             and name not in PINS, 'manifest path')
        PINS[name] = {'bytes': pin['bytes'], 'sha256': pin['sha256']}
    need(rel(Path(__file__).resolve()) in PINS and rel(BASE / 'PROTOCOL.md') in PINS, 'export source/protocol pins')
    for folder in (OLD, CORRECTED):
        for path in folder.rglob('*'):
            need(not path.is_symlink(), 'historical symlink prohibited')
            if path.is_file():
                need(rel(path) in PINS, 'unmanifested historical file: ' + rel(path))
    for name in PINS:
        read_bytes(ROOT / name)
    return receipt


def reference(folder, ref, prefix):
    name = ref['file']
    need(set(ref) == {'file', 'bytes', 'sha256'} and Path(name).name == name and name.startswith(prefix),
         'saved reference shape')
    data = read_bytes(folder / 'results' / name)
    need(len(data) == ref['bytes'] and sha(data) == ref['sha256'], 'actual reference bytes/hash')
    return parse(data), data


def archive(folder, expected_calls, inputs, controls):
    failure, closed, supervisor = read(folder / 'results/failure.json'), read(folder / 'results/exit.json'), read(folder / 'supervisor.json')
    need(failure['calls'] == closed['calls'] == expected_calls and failure['allocation'] == 'closed-no-rerun'
         and closed['exitCode'] == 1 and closed['allocation'] == 'closed', 'failed allocation closure')
    need(supervisor.get('returncode') == 1 and not supervisor.get('timeout'), 'failed native supervisor closure')
    historical_manifest = read_bytes(folder / 'source-manifest.json')
    publication, environment = read(folder / 'source-publication.json'), read(folder / 'results/environment.json')
    need(publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True,
         'historical exact public/committed source prerequisite')
    need(publication['manifestSha256'] == sha(historical_manifest) == environment['manifestSha256']
         and publication['commit'] == environment['sourceCommit'], 'historical source/input provenance')
    for pin in parse(historical_manifest)['files']:
        need(pin['path'] in PINS and PINS[pin['path']] == {'bytes': pin['bytes'], 'sha256': pin['sha256']},
             'historical dependency closure pin: ' + pin['path'])
    data = read_bytes(folder / 'results/queries.jsonl')
    need(data.endswith(b'\n'), 'complete journal final record')
    rows = [parse(line) for line in data.splitlines()]
    need(len(rows) == expected_calls, 'exact failed-attempt call count')
    records, previous = [], None
    for index, row in enumerate(rows):
        tick()
        is_control = index < (18 if folder == OLD else 24)
        stage = index // 2 if is_control else index - 24
        method = ('F' if index % 2 == 0 else 'C') if is_control else 'C'
        phase = 'control' if is_control else 'warmup'
        need((row['call'], row['phase'], row['batch'], row['stage'], row['method']) ==
             (index + 1, phase, -1, stage, method), 'closed prefix schedule')
        current = controls[stage] if is_control else inputs[stage]
        binding = sha(compact(current))
        need(row['inputPreserved'] is True and row['inputBeforeSha256'] == row['inputAfterSha256'] == binding,
             'saved input preservation/binding')
        value, body = reference(folder, row['semantic'], 'semantic-')
        need(row['semantic']['file'] == 'semantic-' + sha(body) + '.json', 'semantic content address')
        status = 'input-refused' if is_control and stage == 11 else 'domain-refused' if (is_control and stage == 8) or (not is_control and stage == 6) else 'native-success'
        reason = 'duplicate-id' if status == 'input-refused' else 'native-admission' if status == 'domain-refused' else None
        need(value['schema'] == 'm31-native-load-result-v1' and value['model'] == 'ordinary-binary64-full-contribution', 'native evidence identity')
        need(row['status'] == value['status'] == status and row['reason'] == value['reason'] == reason, 'saved status/reason')
        if status == 'input-refused':
            need(value['stage'] == 'input' and all(value[k] is None for k in ('raw', 'ids', 'prepared', 'coefficients', 'diagnostics')), 'duplicate refusal partial evidence')
        else:
            canonical = sorted(current['drones'], key=lambda item: item['id'])
            need(value['ids'] == [id_word(item['id']) for item in canonical] and
                 value['raw'] == [{'id': id_word(item['id']), 'state': item['state']} for item in canonical], 'semantic raw input binding')
            need(len(value['prepared']) == len(canonical), 'prepared evidence count')
            for item, prepared in zip(canonical, value['prepared']):
                need(prepared['id'] == id_word(item['id']) and prepared['center'] == item['state'][:3]
                     and prepared['forces'] == item['state'][13:17], 'prepared input binding')
            if status == 'domain-refused':
                need(value['stage'] == 'build' and value['diagnostics']['admission']['admitted'] is False, 'build admission refusal')
            else:
                need(value['diagnostics']['admission']['admitted'] is True and
                     all(len(value[key]) == len(canonical) for key in ('loads', 'solution')), 'recorded successful output completeness')
        if is_control and method == 'C':
            need(body == previous, 'actual complete control F/C byte equality')
        previous = body
        if row['witness'] is not None:
            reference(folder, row['witness'], 'witness-')
        BINDINGS.append({'package': rel(folder), 'call': index + 1, 'inputSha256': binding, 'semantic': row['semantic']})
        records.append((row, value))
    need(not list((folder / 'results').glob('batch-*.json')) and not list((folder / 'results').glob('warmup-*.json'))
         and not (folder / 'results/summary.json').exists(), 'no completed timing panel')
    return records


def main():
    receipt = gate()
    old_controls, controls = read(OLD / 'results/control-inputs.json'), read(CORRECTED / 'results/control-inputs.json')
    need(old_controls == controls and len(controls) == 12, 'unchanged twelve saved controls')
    controls = [input_record(row['input'], i == 11) for i, row in enumerate(controls)]
    inputs = []
    for stage in range(8):
        name = 'input-' + str(stage) + '.json'
        original, corrected = read_bytes(OLD / 'results' / name), read_bytes(CORRECTED / 'results' / name)
        need(original == corrected, 'unchanged saved synthetic input')
        current = input_record(parse(corrected))
        need(len(current['drones']) == 1000, 'saved frame has one thousand drones')
        inputs.append(current)
    archive(OLD, 18, inputs, controls)
    records = archive(CORRECTED, 31, inputs, controls)
    admission = records[-1][1]['diagnostics']['admission']
    need(admission['reasons'] == ['near-field'] and number(admission['unsupportedNearCount']) == 186
         and number(admission['invalidTermCount']) == 0 and number(admission['scaledCapViolationCount']) == 0,
         'saved near-field refusal classification')
    frames = []
    for stage, current in enumerate(inputs):
        row = records[24 + stage][0] if stage < 7 else None
        frames.append({'stage': stage, 'positions': [[number(w) for w in item['state'][:3]] for item in current['drones']],
                       'status': 'candidate-success' if stage < 6 else 'candidate-refused' if stage == 6 else 'not-evaluated',
                       'cache': row['cache'] if row is not None else None})
    counts = {'originalCalls': 18, 'correctedCalls': 31, 'correctedControlPairs': 12,
              'candidateWarmupSuccesses': 6, 'refusalStage': 6, 'unsupportedNearRotorSourceClassifications': 186,
              'baseline1000Queries': 0, 'measuredQueries': 0}
    view = {'schema': 'm31-buffered-failure-view-v1', 'synthetic': True, 'drones': 1000, 'frames': frames,
            'counts': counts, 'candidateQualified': False, 'physicalSafetyEstablished': False,
            'scope': 'Saved prescribed-state failure evidence only; no 1000-drone F/C equivalence or speed result.',
            'highlightScope': 'Whole-state status only; exact offending pairs are not identified or highlighted.'}
    view_ref = write('view-data.json', view)
    audit = {'schema': 'm31-buffered-failure-audit-v1', 'passed': True,
             'meaning': 'Saved failure evidence and display export verified; candidate not qualified.',
             'candidateQualified': False, 'physicalSafetyEstablished': False, 'counts': counts,
             'sourceCommit': receipt['commit'], 'manifestSha256': receipt['manifestSha256'],
             'viewData': view_ref, 'inputBindings': BINDINGS,
             'pins': [{'path': path, **PINS[path]} for path in sorted(PINS)],
             'checks': ['public source gate and complete historical file pins', '18-call and 31-call closed schedules',
                        'actual semantic bytes, input hashes and raw/prepared bindings', 'nine original and twelve corrected full control pairs',
                        'six recorded candidate successes and one near-field refusal; eighth input not evaluated',
                        'saved classification count 186, not recomputed and not a collision count', 'no baseline-1000 or measured query; no speed inference']}
    tick()
    write('audit.json', audit)


if __name__ == '__main__':
    START = time.monotonic()
    OUT.mkdir()  # Existing output is terminal: never resume or overwrite it.
    write('launch.json', {'startedUtc': dt.datetime.now(dt.timezone.utc).isoformat(), 'allocation': 'one-saved-evidence-export'})
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(EvidenceFailure('export wall budget')))
    signal.setitimer(signal.ITIMER_REAL, 30)
    code = 0
    try:
        main()
    except Exception as error:
        code = 1
        signal.setitimer(signal.ITIMER_REAL, 0)
        message = str(error) if isinstance(error, EvidenceFailure) else type(error).__name__
        write('failure.json', {'passed': False, 'message': message[:500], 'allocation': 'closed-no-rerun'}, True)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        write('exit.json', {'exitCode': code, 'exportWallSeconds': time.monotonic() - START,
                            'bytesBeforeExit': WRITTEN, 'allocation': 'closed'}, True)
    sys.exit(code)
