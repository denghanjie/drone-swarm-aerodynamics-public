"""Independent paired original/memory coupled saved-evidence audit. Never imports the producer.

Scalar/projection/derivative helpers are adapted from the prior independently
written continuation auditor. This is independent of JavaScript production,
not a third independent implementation of those prior Python helpers.
See AUDIT-CONTRACT.md. Source preparation alone authorizes no execution.
"""
from pathlib import Path, PurePosixPath
import datetime
import gzip
import hashlib
import io
import json
import math
import os
import re
import struct
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
REL = BASE.relative_to(ROOT).as_posix()
MAX_SECONDS = 2400
MAX_OUTPUT = 128*1024*1024
MAX_INPUT = 4*1024*1024*1024
MAX_PART = 32*1024*1024
MAX_RECORD = 4*1024*1024
HEX = re.compile(r'^[0-9a-f]{16}$')
HASH = re.compile(r'^[0-9a-f]{64}$')
START = None
READ_EVENTS = []
READ_OPERATION = 0
COUNTS = {key: 0 for key in ('records', 'controllerRecords', 'originalControllerRecords',
          'memoryControllerRecords', 'controllerRows', 'originalControllerRows', 'attemptedStages',
          'successfulStages', 'completedSteps', 'safetyRecords', 'projectionRows',
          'derivativeRows', 'sqrtComparisons', 'sqrtOneUlpDifferences',
          'initialWordsValidated', 'pairedInitialWordComparisons', 'segmentBoundaryWordComparisons',
          'nativeLoadRows', 'refusedStages', 'projectionNormsReconstructedForRefusal',
          'memoryRows', 'memoryIntegrations', 'initialMemoryWordComparisons',
          'segmentBoundaryMemoryWordComparisons')}
CASES = [
    {'caseId': 'seed2026102101-original-h005', 'pairId': 'seed2026102101-h005', 'arm': 'original',
     'seed': 2026102101, 'dt': .005, 'stepsPerControl': 2},
    {'caseId': 'seed2026102101-memory-h005', 'pairId': 'seed2026102101-h005', 'arm': 'memory',
     'seed': 2026102101, 'dt': .005, 'stepsPerControl': 2},
    {'caseId': 'seed2026102102-original-h005', 'pairId': 'seed2026102102-h005', 'arm': 'original',
     'seed': 2026102102, 'dt': .005, 'stepsPerControl': 2},
    {'caseId': 'seed2026102102-memory-h005', 'pairId': 'seed2026102102-h005', 'arm': 'memory',
     'seed': 2026102102, 'dt': .005, 'stepsPerControl': 2}]
PAIRS = [{'caseId': 'seed2026102101-h005', 'pairId': 'seed2026102101-h005',
          'seed': 2026102101, 'dt': .005, 'stepsPerControl': 2},
         {'caseId': 'seed2026102102-h005', 'pairId': 'seed2026102102-h005',
          'seed': 2026102102, 'dt': .005, 'stepsPerControl': 2}]
SEGMENTS = [{'segment': 0, 'timeOrigin': 0, 'duration': 1},
            {'segment': 1, 'timeOrigin': 1, 'duration': 4}]
EXPECTED_CONFIG = {'schema': 'm31-unseen-pairs-config-v1', 'n': 64,
    'controlDt': .01, 'duration': 5, 'maxStages': 16000, 'maxNativeCalls': 16000,
    'maxWallSeconds': 2400, 'maxOutputBytes': MAX_INPUT, 'maxRecordBytes': MAX_RECORD,
    'cases': CASES, 'segments': SEGMENTS,
    'verticalMemory': {'gain': 2.5, 'controlDt': .01, 'minimum': -5, 'maximum': 5,
                       'update': 'previous-sample-rectangle', 'initialIntegral': 0,
                       'initialPreviousError': 0, 'carryAcrossSegments': True}}
CONTINUATION = 'research/m31-boids-continuation-2026-10-20'
MEMORY_CONTEXT = 'research/m31-vertical-memory-2026-10-21'
TRANSFER_CONTEXT = 'research/m31-vertical-transfer-2026-10-21'
FRESH = 'research/m31-native-fresh-transfer-2026-10-17/source/'
IMMUTABLE = {
    MEMORY_CONTEXT+'/source/motion.cjs':
        'f7966691b52f2e14c2fbba82ed136fc99cf7a87b8d53725e08be9923128cea16',
    'research/m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs':
        'b14b81107a5c5f08db1b14e369e61baccd3bef18ef3c6d2717fd150165ab4332',
    FRESH+'native-load.cjs':
        'b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1',
    FRESH+'vendor/generation/step02c-source/physics.cjs':
        '0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1',
    FRESH+'vendor/generation/milestone-31-source/sim.cjs':
        '2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e',
    FRESH+'vendor/generation/milestone-31-source/grid.cjs':
        'f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302',
    FRESH+'vendor/generation/milestone-31-source/geometry.cjs':
        'e209e492fc523ab3c0c7df62745fb0d3dd7204f35e53309938a19d7895ed3d4f',
    CONTINUATION+'/source/motion.cjs':
        'c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373',
    CONTINUATION+'/source/journal.cjs':
        '689c3faae7a21fe0abf446b6260d907e1f92039688194c87ef7cb17bc3de0485'}

class AuditError(Exception):
    pass

def need(ok, label):
    if not ok:
        raise AuditError(label)

def guard():
    need(START is not None and time.monotonic() - START <= MAX_SECONDS, 'audit-wall-budget')

def strict_object(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate-json-key:' + key)
        out[key] = value
    return out

def reject_constant(value):
    raise AuditError('nonfinite-json-number:' + value)

def json_float(value):
    result = float(value)
    need(math.isfinite(result), 'overflowing-json-number')
    return result

def parse(raw):
    return json.loads(raw, object_pairs_hook=strict_object, parse_constant=reject_constant, parse_float=json_float)

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=True, allow_nan=False, separators=(',', ':')) + '\n').encode()

def safe_path(parent, relative):
    need(isinstance(relative, str) and relative != '' and '\\' not in relative, 'path-format')
    parts = PurePosixPath(relative)
    need(not parts.is_absolute() and all(p not in ('', '.', '..') for p in relative.split('/')), 'path-traversal')
    path = parent
    for part in parts.parts:
        path = path / part
        need(not path.is_symlink(), 'symlink:' + relative)
    need(path.is_file(), 'missing-file:' + relative)
    return path

def eq(actual, expected, label):
    need(actual == expected, label)

def integer(value, low, high, label):
    need(type(value) is int and low <= value <= high, label)
    return value

def num(word, finite=True):
    need(isinstance(word, str) and HEX.fullmatch(word) is not None, 'binary64-word')
    value = struct.unpack('>d', bytes.fromhex(word))[0]
    if finite:
        need(math.isfinite(value), 'nonfinite-binary64-word')
    return value

def word(value):
    return struct.pack('>d', value).hex()

def vector(value, size, finite=True):
    need(isinstance(value, list) and len(value) == size, 'word-vector-shape')
    return [num(x, finite) for x in value]

def equal_words(saved, values, label):
    eq(saved, [word(x) for x in values], label)

def add_count(name, count=1):
    COUNTS[name] += count

def same_number(value, expected, label):
    need(type(value) in (int, float) and math.isfinite(value), label)
    eq(word(float(value)), word(float(expected)), label)

def sqrt_check(saved, operand, label):
    value = num(saved)
    need(operand >= 0 and math.isfinite(operand) and value > 0, label + ':range')
    reference = math.sqrt(operand)
    distance = abs(int(saved, 16) - int(word(reference), 16))
    need(distance <= 1, label + ':greater-than-one-ulp')
    add_count('sqrtComparisons')
    if distance:
        add_count('sqrtOneUlpDifferences')
    return value

def states(value, field='state', wrapper=True):
    if wrapper:
        need(type(value) is dict and set(value) == {'drones'}, 'input-shape')
        value = value['drones']
    need(isinstance(value, list) and len(value) == 64, 'drone-count')
    out = []
    for i, row in enumerate(value):
        eq(type(row), dict, 'drone-record')
        integer(row.get('id'), i, i, 'canonical-id')
        vector(row.get(field), 17)
        out.append(row[field])
    return out

def input_from(values):
    return {'drones': [{'id': i, 'state': row} for i, row in enumerate(values)]}

def numeric(values):
    return [vector(row, 17) for row in values]

def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def rotate(q, v):
    t = [x*2 for x in cross(q, v)]
    u = cross(q, t)
    return [v[k] + (q[3]*t[k] + u[k]) for k in range(3)]

def left_sum(values):
    value = 0.0
    for item in values:
        value += item
    return value

def projection(raw_words, projected_words, details=None):
    for i, (raw, projected) in enumerate(zip(numeric(raw_words), numeric(projected_words))):
        guard()
        q = raw[6:10]
        ns = ((q[0]*q[0] + q[1]*q[1]) + q[2]*q[2]) + q[3]*q[3]
        need(ns > 0 and math.isfinite(ns), 'projection-norm-square-range')
        if details is not None:
            row = details[i]
            eq(row['normSquareWord'], word(ns), 'projection-norm-square')
            norm = sqrt_check(row['normWord'], ns, 'projection-sqrt')
        else:
            # The unchanged adapter omits per-row norm evidence on a refusal.
            # Test the declared one-ULP sqrt candidates; do not infer a real norm.
            reference = math.sqrt(ns)
            candidates = [reference, math.nextafter(reference, 0.0), math.nextafter(reference, math.inf)]
            matches = [x for x in candidates if x > 0 and math.isfinite(x) and
                       [word(y/x) for y in q] == projected_words[i][6:10]]
            need(bool(matches), 'refusal-projection-sqrt-candidate')
            norm = matches[0]
            add_count('projectionNormsReconstructedForRefusal')
        expected = raw[:6] + [x/norm for x in q] + raw[10:]
        equal_words(projected_words[i], expected, 'projection-state')
        add_count('projectionRows')

def controller(body, case, step_index, current, origin, memory):
    is_memory = case['arm'] == 'memory'
    eq(body.get('schema'), 'm31-vertical-memory-controller-v1' if is_memory else 'm31-coupled-controller-v1', 'controller-schema')
    eq(body.get('arm'), 'coupled', 'physical-controller-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'controller-step')
    same_number(body.get('controlIndex'), step_index/case['stepsPerControl'], 'controller-index')
    eq(body.get('relativeTimeWord'), word(step_index*case['dt']), 'controller-time')
    eq(body.get('originalTimeWord'), word(origin + step_index*case['dt']), 'controller-original-time')
    global_index = round(origin/.01)+step_index//case['stepsPerControl']
    if is_memory:
        integer(body.get('globalControlIndex'), global_index, global_index, 'global-controller-index')
    else:
        need('globalControlIndex' not in body and memory is None, 'original-controller-has-no-memory-index')
    rows = body.get('records')
    eq(states(rows, 'stateWords', False), current, 'controller-current-state')
    commands, next_memory, errors, integrals = [], ([] if is_memory else None), [], []
    for i, row in enumerate(rows):
        ids = row.get('neighborIds')
        need(isinstance(ids, list), 'neighbor-list')
        for value in ids:
            integer(value, 0, 63, 'neighbor-id')
        eq(ids, sorted(set(ids)), 'neighbor-order-or-duplicate')
        need(i not in ids, 'self-neighbor')
        v = vector(row.get('desiredVelocityWords'), 3)
        target = row.get('target')
        need(type(target) is dict and set(target) == {'vxWord', 'vyWord', 'zWord', 'yawWord'}, 'target-fields')
        eq(target['vxWord'], row['desiredVelocityWords'][0], 'target-vx-binding')
        eq(target['vyWord'], row['desiredVelocityWords'][1], 'target-vy-binding')
        state = vector(current[i], 17)
        if is_memory:
            before = {key: value for key, value in memory[i].items() if key != 'id'}
            integer(before['updates'], global_index, global_index, 'memory-global-update-count')
            old_integral, previous_error = num(before['integralWord']), num(before['previousErrorWord'])
            increment = 0.0 if global_index == 0 else (2.5*.01)*previous_error
            unclamped = old_integral+increment
            integral = -5.0 if unclamped < -5.0 else 5.0 if unclamped > 5.0 else unclamped
            error = v[2]-state[5]
            need(all(math.isfinite(value) for value in (increment, unclamped, integral, error)), 'finite-independent-memory-arithmetic')
            after = {'integralWord': word(integral), 'previousErrorWord': word(error), 'updates': global_index+1}
            eq(row.get('verticalMemory'), {'before': before, 'incrementWord': word(increment),
               'unclampedWord': word(unclamped), 'after': after}, 'independent-memory-recurrence')
            target_z = state[2]+((2.5*v[2]+1.5*state[5])+integral)/6
            next_memory.append({'id': i, **after})
            integrals.append(integral)
            add_count('memoryRows')
            if global_index > 0:
                add_count('memoryIntegrations')
        else:
            need('verticalMemory' not in row, 'original-row-has-no-memory-evidence')
            target_z = state[2]+(2.5*v[2]+1.5*state[5])/6
            error = v[2]-state[5]
            need(math.isfinite(error), 'finite-own-request-vertical-error')
            add_count('originalControllerRows')
        need(math.isfinite(target_z), 'finite-controller-target-z')
        eq(target['zWord'], word(target_z), 'controller-target-z-operation-order')
        errors.append(abs(error))
        add_count('controllerRows')
        num(target['yawWord'])
        vector(row.get('commandsWords'), 4)
        vector(row.get('desiredQuaternionWords'), 4)
        need(type(row.get('saturated')) is bool, 'controller-saturation-type')
        commands.append(row['commandsWords'])
    add_count('controllerRecords')
    add_count('memoryControllerRecords' if is_memory else 'originalControllerRecords')
    mean_error = left_sum(errors)/64
    need(math.isfinite(mean_error), 'finite-controller-mean-absolute-error')
    descriptor = {'time': num(body['originalTimeWord']), 'timeWord': body['originalTimeWord'],
                  'segment': round(origin), 'localControlIndex': body['controlIndex'],
                  'globalControlIndex': global_index, 'meanAbsoluteVerticalError': mean_error,
                  'integralMinimum': min(integrals) if is_memory else None,
                  'integralMaximum': max(integrals) if is_memory else None,
                  'scope': 'own saved desiredVz minus own current saved vz; all 64 controller rows'}
    return commands, next_memory, descriptor


def initial_memory():
    return [{'id': i, 'integralWord': word(0.0), 'previousErrorWord': word(0.0), 'updates': 0}
            for i in range(64)]


def check_memory(saved, expected, label):
    if expected is None:
        need(saved is None, label+':original-memory-null')
        return
    need(type(saved) is list and len(saved) == 64, label+':count')
    for i, row in enumerate(saved):
        need(type(row) is dict and set(row) == {'id', 'integralWord', 'previousErrorWord', 'updates'}, label+':fields')
        integer(row['id'], i, i, label+':id')
        need(-5 <= num(row['integralWord']) <= 5, label+':integral-bound')
        num(row['previousErrorWord'])
        integer(row['updates'], 0, 500, label+':update-bound')
    eq(saved, expected, label+':exact-snapshot')

def derivative(row, load, commands, raw, projected):
    eq(row['rawStateWords'], raw, 'row-raw-binding')
    eq(row['stateWords'], projected, 'row-projected-binding')
    eq(row['commandsWords'], commands, 'row-command-binding')
    eq(row['nominalMotorWords'], projected[13:17], 'nominal-motor-binding')
    consumed = {'rotorWords': load['rotor'], 'collectiveWord': load['collective'],
                'worldForceWords': load['worldForce'], 'worldMomentWords': load['worldMoment']}
    eq(row['consumed'], consumed, 'same-id-native-load-consumption')
    s = vector(projected, 17)
    q, omega = s[6:10], s[10:13]
    force, moment = vector(load['worldForce'], 3), vector(load['worldMoment'], 3)
    arm = rotate([-q[0], -q[1], -q[2], q[3]], moment)
    yaw = 0.0
    for sign, thrust in zip((1.0, -1.0, 1.0, -1.0), s[13:17]):
        yaw += ((sign*7.94e-12)/3.16e-10)*thrust
    total = [arm[0], arm[1], arm[2]+yaw]
    inertia = [1.4e-5, 1.4e-5, 2.17e-5]
    gyro = cross(omega, [omega[k]*inertia[k] for k in range(3)])
    equal_words(row['bodyArmWords'], arm, 'body-arm')
    eq(row['nominalYawWord'], word(yaw), 'nominal-yaw')
    equal_words(row['totalBodyWords'], total, 'body-total')
    equal_words(row['gyroWords'], gyro, 'gyro')
    c = cross(q, omega)
    dq = [((omega[k]*q[3] + q[k]*0.0) + c[k])*.5 for k in range(3)]
    dq.append((q[3]*0.0-left_sum([q[k]*omega[k] for k in range(3)]))*.5)
    acceleration = [x/.027 for x in force]
    acceleration[2] -= 9.81
    expected = s[3:6] + acceleration + dq + [(total[k]-gyro[k])/inertia[k] for k in range(3)]
    expected += [(x-s[13+r])/.04 for r, x in enumerate(vector(commands, 4))]
    equal_words(row['derivativeWords'], expected, 'full-derivative-arithmetic')
    vector(row['derivativeWords'], 17)
    add_count('derivativeRows')
    return expected

def endpoint(body, case, step_index, current, ks, origin):
    eq(body.get('schema'), 'm31-coupled-step-v1', 'step-schema')
    eq(body.get('stepId'), f'coupled-step{step_index}', 'step-id')
    eq(body.get('arm'), 'coupled', 'step-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'step-index')
    dt = case['dt']
    t = step_index*dt+dt
    eq(body.get('relativeTimeWord'), word(t), 'step-time')
    eq(body.get('originalTimeWord'), word(origin+t), 'step-original-time')
    eq(body.get('dtWord'), word(dt), 'step-dt')
    eq(body.get('status'), 'completed', 'step-must-complete-in-closed-allocation')
    eq(body.get('reason'), None, 'step-reason')
    eq(states(body.get('start'), 'stateWords', False), current, 'step-start-binding')
    eq(body.get('stageIds'), [f'coupled-step{step_index}-k{k}' for k in range(1, 5)], 'step-stage-binding')
    base = numeric(current)
    expected = [[word(value+dt*(((ks[0][i][j]+2*ks[1][i][j])+2*ks[2][i][j])+ks[3][i][j])/6)
                 for j, value in enumerate(row)] for i, row in enumerate(base)]
    eq(states(body.get('rawFinal'), 'stateWords', False), expected, 'rk-weighted-endpoint')
    final = states(body.get('final'), 'stateWords', False)
    projection(expected, final, body['final'])
    add_count('completedSteps')
    return final

def safety(body, step_index):
    integer(body.get('stepIndex'), step_index, step_index, 'safety-step')
    need(type(body.get('pass')) is bool and isinstance(body.get('issues'), list), 'safety-shape')
    eq(body['pass'], len(body['issues']) == 0, 'safety-pass-issues-binding')
    for issue in body['issues']:
        kind = issue.get('kind')
        need(kind in ('vehicle-model-limit', 'obstacle-contact', 'drone-contact'), 'safety-kind')
        if kind == 'drone-contact':
            ids = issue.get('ids')
            need(isinstance(ids, list) and len(ids) == 2, 'safety-contact-ids')
            integer(ids[0], 0, 63, 'safety-id')
            integer(ids[1], ids[0]+1, 63, 'safety-id-order')
            need(num(issue.get('distanceWord')) >= 0, 'safety-distance')
        else:
            integer(issue.get('id'), 0, 63, 'safety-id')
            if kind == 'obstacle-contact':
                hits = issue.get('hits')
                need(isinstance(hits, list) and len(hits) > 0, 'safety-hits')
                for hit in hits:
                    need(isinstance(hit.get('id'), str) and type(hit.get('clearance')) in (int, float)
                         and math.isfinite(hit['clearance']) and hit['clearance'] < 0, 'safety-hit-fields')
    add_count('safetyRecords')
    return body['pass']


def checked(path, expected):
    """Verify a whole file before exposing bytes; retries never replay parsing."""
    global READ_OPERATION
    READ_OPERATION += 1
    operation = READ_OPERATION
    for attempt in range(1, 4):
        guard()
        try:
            with path.open('rb') as stream:
                raw = stream.read(expected['bytes']+1)
            digest = hashlib.sha256(raw).hexdigest()
            if len(raw) == expected['bytes'] and digest == expected['sha256']:
                return raw
            event = {'kind': 'byte-mismatch', 'bytes': len(raw), 'sha256': digest}
        except OSError as error:
            event = {'kind': 'read-error', 'errno': error.errno}
        READ_EVENTS.append({'path': path.relative_to(ROOT).as_posix(), 'operation': operation,
                            'attempt': attempt, **event})
    raise AuditError('verified-read-exhausted:'+path.relative_to(ROOT).as_posix())


def capture(relative, maximum=MAX_OUTPUT):
    """Capture a new small result's identity; no retry without an expected pin."""
    guard()
    path = safe_path(BASE, relative)
    need(path.stat().st_size <= maximum, 'small-result-size')
    raw = path.read_bytes()
    need(len(raw) <= maximum, 'small-result-size')
    return {'file': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}, raw


def parse_frozen(relative, pins):
    need(relative in pins, 'missing-source-pin:'+relative)
    return parse(checked(safe_path(ROOT, relative), pins[relative]))


def source_gate():
    manifest_pin, raw = capture('source-manifest.json', MAX_RECORD)
    publication_pin, publication_raw = capture('source-publication.json', MAX_RECORD)
    manifest, publication = parse(raw), parse(publication_raw)
    eq(publication.get('manifestSha256'), manifest_pin['sha256'], 'public-source-manifest-hash')
    need(publication.get('remoteBytesEqualLocal') is True
         and publication.get('committedBytesEqualLocal') is True, 'public-source-byte-gate')
    need(isinstance(publication.get('commit'), str)
         and re.fullmatch(r'[0-9a-f]{40}', publication['commit']), 'public-source-commit')
    files = manifest.get('files')
    need(type(files) is list and 1 <= len(files) <= 512, 'source-file-count')
    integer(publication.get('verifiedFilePins'), len(files), len(files), 'verified-source-count')
    pins = {}
    for item in files:
        need(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}, 'source-pin-fields')
        path = item['path']
        need(path not in pins, 'source-path-unique')
        integer(item['bytes'], 1, MAX_OUTPUT, 'source-pin-size')
        need(isinstance(item['sha256'], str) and HASH.fullmatch(item['sha256']), 'source-pin-hash')
        checked(safe_path(ROOT, path), item)
        pins[path] = item
    mandatory = {REL+'/'+name for name in ('config.json', 'runtime.json', 'PROTOCOL.md', 'SEED-EXPOSURE.md',
                 'AUDIT-CONTRACT.md', 'source/run.cjs', 'source/audit.py', 'source/supervise.py')}
    mandatory.update(IMMUTABLE)
    need(mandatory <= pins.keys(), 'source-mandatory-coverage')
    for relative, digest in IMMUTABLE.items():
        eq(pins[relative]['sha256'], digest, 'unchanged-inherited-source:'+relative)
    # Dependency inspection is text-only. Scientific JavaScript is never loaded.
    queue, visited = [REL+'/source/run.cjs'], set()
    while queue:
        relative = queue.pop()
        if relative in visited:
            continue
        visited.add(relative)
        need(relative in pins, 'source-dependency-pin:'+relative)
        text = checked(safe_path(ROOT, relative), pins[relative]).decode('utf-8')
        for dependency in re.findall(r"require\(['\"]([^'\"]+)['\"]\)", text):
            if dependency.startswith('node:'):
                continue
            need(dependency.startswith('.'), 'nonliteral-or-package-dependency')
            target = (ROOT/relative).parent.joinpath(dependency).resolve()
            need(target.is_relative_to(ROOT), 'dependency-outside-repository')
            queue.append(target.relative_to(ROOT).as_posix())
    need(FRESH+'native-load.cjs' in visited, 'coupled-native-dependency-required')
    need(MEMORY_CONTEXT+'/source/motion.cjs' in visited, 'unchanged-memory-controller-dependency-required')
    need(CONTINUATION+'/source/motion.cjs' in visited, 'unchanged-original-controller-dependency-required')
    eq(parse_frozen(REL+'/config.json', pins), EXPECTED_CONFIG, 'fixed-config')
    return publication, manifest_pin, publication_pin, pins, sorted(visited)


def storage_gate(source_pins):
    """Reuse only published storage qualification metadata, never old trajectories."""
    folder = CONTINUATION
    manifest_path = folder+'/result-manifest.json'
    receipt_path = 'research/publication-receipts/m31-boids-continuation-result-2026-10-20.json'
    expected = {'commit': 'a0f595f34a4f9ef8cef516caa0cde60053e0eade',
                'manifestPath': manifest_path, 'manifestBytes': 33149,
                'manifestSha256': '90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81',
                'verifiedFilePins': 157, 'remoteBytesEqualLocal': True, 'committedBytesEqualLocal': True}
    receipt = parse_frozen(receipt_path, source_pins)
    for key, value in expected.items():
        eq(receipt.get(key), value, 'storage-public-receipt:'+key)
    eq(source_pins.get(manifest_path), {'path': manifest_path, 'bytes': expected['manifestBytes'],
       'sha256': expected['manifestSha256']}, 'storage-manifest-pin')
    manifest = parse_frozen(manifest_path, source_pins)
    eq(manifest.get('schema'), 'm31-boids-continuation-result-v1', 'storage-manifest-schema')
    public = {item['path']: item for item in manifest['files']}
    eq(len(public), 157, 'storage-public-file-count')
    eq(len(manifest['files']), len(public), 'storage-public-path-uniqueness')
    evidence = {}
    for name in ('storage/qualification.json', 'storage-supervisor.json', 'ALLOCATION-CLOSURE.json'):
        relative = folder+'/'+name
        need(relative in public, 'storage-selected-public-pin')
        eq(source_pins.get(relative), public[relative], 'storage-selected-source-binding')
        evidence[name] = parse_frozen(relative, source_pins)
    storage, supervisor = evidence['storage/qualification.json'], evidence['storage-supervisor.json']
    need(storage.get('passed') is True and storage.get('closed') is True, 'prior-lossless-storage-qualified')
    need(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True,
         'prior-storage-supervised-success')
    closure = evidence['ALLOCATION-CLOSURE.json']
    eq(closure.get('schema'), 'm31-boids-continuation-closure-v1', 'storage-closure-schema')
    eq(closure['storage']['status'], 'closed-passed', 'storage-closed-passed')
    integer(closure['storage']['attempts'], 1, 1, 'storage-single-allocation')
    return {'resultCommit': expected['commit'], 'receiptPin': source_pins[receipt_path],
            'manifestPin': source_pins[manifest_path],
            'evidencePins': [source_pins[folder+'/'+name] for name in evidence],
            'scope': 'published lossless-storage qualification only; no new storage trial or old trajectory reads'}


def motivation_gate(source_pins):
    """Bind exposed transfer context and both inherited controllers as published bytes."""
    folder = TRANSFER_CONTEXT
    receipt_path = 'research/publication-receipts/m31-vertical-transfer-result-2026-10-21.json'
    manifest_path, summary_path = folder+'/result-manifest.json', folder+'/SUMMARY.md'
    expected = {'commit': '341cfa5e9bec84c0615825b82665385469d84a2b',
                'manifestPath': manifest_path, 'manifestBytes': 40238,
                'manifestSha256': '530b5b76624dfea7e21127832e552af9deeab7358816ed164cfa00a0130b872a',
                'verifiedFilePins': 198, 'remoteBytesEqualLocal': True, 'committedBytesEqualLocal': True}
    receipt = parse_frozen(receipt_path, source_pins)
    for key, value in expected.items():
        eq(receipt.get(key), value, 'motivation-public-receipt:'+key)
    eq(source_pins.get(manifest_path), {'path': manifest_path, 'bytes': expected['manifestBytes'],
       'sha256': expected['manifestSha256']}, 'motivation-manifest-pin')
    manifest = parse_frozen(manifest_path, source_pins)
    eq(manifest.get('schema'), 'm31-vertical-transfer-result-v1', 'motivation-manifest-schema')
    pins = {pin['path']: pin for pin in manifest['files']}
    eq(len(pins), expected['verifiedFilePins'], 'motivation-public-file-count')
    eq(len(manifest['files']), len(pins), 'motivation-unique-public-paths')
    required = (summary_path, CONTINUATION+'/source/motion.cjs', MEMORY_CONTEXT+'/source/motion.cjs')
    for relative in required:
        need(relative in pins, 'motivation-required-published-source')
        eq(source_pins.get(relative), pins[relative], 'motivation-exact-public-source-pin')
        checked(safe_path(ROOT, relative), pins[relative])
    return {'resultCommit': expected['commit'], 'receiptPin': source_pins[receipt_path],
            'manifestPin': source_pins[manifest_path], 'summaryPin': source_pins[summary_path],
            'controllerPins': [source_pins[relative] for relative in required[1:]],
            'scope': 'previously exposed transfer result and unchanged controller sources; no prior numerical path reused'}


def constant_evidence(constants):
    expected = {'mg': .027*9.81, 'arm': .028, 'radius': .023, 'rho': 1.225,
                'A': math.pi*.023*.023, 'decay': 10.11, 'spread': .07668,
                'origin': -5.817, 'minDown': 2.5, 'neighbor': 3.0, 'nearRad': .15,
                'downFade': 2.0, 'downCut': 2.5, 'radFade': 2.0, 'radCut': 3.0}
    need(type(constants) is dict and set(constants) == set(expected) | {'R', 'D', 'induced', 'kappa'}, 'native-constant-fields')
    for key, value in expected.items():
        eq(constants[key], word(value), 'native-constant:' + key)
    root2 = math.sqrt(2)
    # Constants containing square roots get the same explicitly bounded policy.
    candidates = [root2, math.nextafter(root2, 0.0), math.nextafter(root2, math.inf)]
    need(any(word(x*.028) == constants['R'] and word(x-1) == constants['kappa'] for x in candidates), 'native-root2-constants')
    eq(constants['D'], word(2*num(constants['R'])), 'native-D')
    sqrt_check(constants['induced'], expected['mg']/(8*expected['rho']*expected['A']), 'native-induced')
    return {key: num(value) for key, value in constants.items()}

def prepared_evidence(rows, raw, constants, success):
    if rows is None:
        need(not success, 'missing-native-prepared')
        return None
    need(isinstance(rows, list) and len(rows) == 64, 'native-prepared-count')
    for i, row in enumerate(rows):
        guard()
        integer(row.get('id'), i, i, 'prepared-id')
        s = vector(raw[i], 17)
        q = s[6:10]
        eq(row['center'], raw[i][:3], 'prepared-center-binding')
        eq(row['forces'], raw[i][13:17], 'prepared-force-binding')
        equal_words(row['axis'], rotate(q, [0.0, 0.0, 1.0]), 'prepared-axis')
        need(isinstance(row['offsets'], list) and len(row['offsets']) == 4, 'prepared-offsets-shape')
        need(isinstance(row['points'], list) and len(row['points']) == 4, 'prepared-points-shape')
        arm = constants['arm']
        corners = [[arm, arm, 0.0], [-arm, arm, 0.0], [-arm, -arm, 0.0], [arm, -arm, 0.0]]
        for r in range(4):
            offset = rotate(q, corners[r])
            equal_words(row['offsets'][r], offset, 'prepared-offset')
            equal_words(row['points'][r], [s[k]+offset[k] for k in range(3)], 'prepared-point')
        total = left_sum(s[13:17])
        eq(row['nativeTotal'], word(total), 'prepared-total')
        sqrt_check(row['nativeBeta'], total/constants['mg'], 'prepared-beta')
        need(isinstance(row['nativeNu'], list) and len(row['nativeNu']) == 4, 'prepared-nu-shape')
        for r in range(4):
            sqrt_check(row['nativeNu'][r], s[13+r]/(2*constants['rho']*constants['A']), 'prepared-nu')
    return rows

def coefficient_evidence(value, prepared, success):
    if value is None:
        need(not success, 'missing-native-coefficients')
        return
    need(type(value) is dict and set(value) == {'offsets', 'sourceIndices', 'K', 'a'}, 'coefficient-fields')
    offsets, src, kvals, avals = (value[key] for key in ('offsets', 'sourceIndices', 'K', 'a'))
    need(isinstance(src, list) and len(src) <= 64*63*4, 'coefficient-count')
    need(isinstance(offsets, list) and len(offsets) == 257, 'coefficient-offset-count')
    need(isinstance(kvals, list) and len(kvals) == len(src), 'coefficient-K-count')
    need(avals is None and not success or isinstance(avals, list) and len(avals) == len(src), 'coefficient-a-count')
    eq(offsets[0], 0, 'coefficient-offset-start')
    eq(offsets[-1], len(src), 'coefficient-offset-end')
    for r in range(256):
        guard()
        lo = integer(offsets[r], 0, len(src), 'coefficient-offset')
        hi = integer(offsets[r+1], lo, len(src), 'coefficient-offset-order')
        previous = -1
        for z in range(lo, hi):
            source = integer(src[z], 0, 63, 'coefficient-source')
            need(source > previous and source != r//4, 'coefficient-source-order')
            previous = source
            k = num(kvals[z], success)
            if success:
                need(k > 0, 'coefficient-K-range')
            if avals is not None:
                a = num(avals[z], success)
                if success:
                    need(a > 0, 'coefficient-a-range')
                    eq(avals[z], word(k*num(prepared[source]['nativeBeta'])/num(prepared[r//4]['nativeNu'][r%4])), 'coefficient-scale-arithmetic')

def consume_checksum(loads):
    status = 'native-success'
    value = 2166136261
    for char in status:
        value = ((value ^ ord(char))*16777619) & 0xffffffff
    for row in loads:
        words = [word(float(row['id']))] + row['rotor'] + [row['collective']] + row['worldForce'] + row['worldMoment']
        for item in words:
            for chunk in (item[:8], item[8:]):
                value = ((value ^ int(chunk, 16))*16777619) & 0xffffffff
    return {'kind': 'native-load-id-status-fnv32', 'status': status, 'loadWords': 64*11,
            'identityWords': 64, 'statusCharacters': len(status), 'value': value}

def native_evidence(body):
    n = body['native']
    need(type(n) is dict, 'native-evidence-missing')
    eq(n.get('schema'), 'm31-native-load-evidence-v1', 'native-schema')
    eq(n.get('model'), 'ordinary-binary64-full-contribution', 'native-model')
    eq(n.get('method'), 'F', 'native-method')
    eq(n.get('caseId'), body['stageId'], 'native-stage-id')
    encoded = json.dumps(body['nativeInput'], ensure_ascii=True, separators=(',', ':')).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    eq(n.get('semanticInputSha256'), digest, 'native-input-hash')
    eq(n.get('inlineInputCanonicalSha256'), digest, 'native-inline-hash')
    success = n.get('status') == 'native-success'
    need(success or n.get('status') in ('domain-refused', 'input-refused', 'numerical-failure'), 'unexpected-native-status')
    constants = constant_evidence(n.get('constants'))
    raw = states(body['nativeInput'])
    if n.get('raw') is not None:
        eq(states(n['raw'], wrapper=False), raw, 'native-raw-current-input-binding')
        eq(n.get('ids'), list(range(64)), 'native-ids')
    else:
        need(not success and n.get('stage') == 'input' and n.get('ids') is None, 'native-raw-missing')
    prepared = prepared_evidence(n.get('prepared'), raw, constants, success)
    coefficient_evidence(n.get('coefficients'), prepared, success)
    if not success:
        need(isinstance(n.get('reason'), str) and n['reason'] != '', 'native-refusal-reason')
        need(n.get('stage') in ('input', 'build', 'schedule', 'solve', 'residual', 'loads', 'consumption'), 'native-refusal-stage')
        need('loads' not in n and 'solution' not in n and 'consumption' not in n, 'refusal-has-consumable-loads')
        return None
    eq(n.get('reason'), None, 'native-success-reason')
    diag = n.get('diagnostics')
    need(type(diag) is dict, 'native-diagnostics')
    eq(diag['admission']['admitted'], True, 'native-admission')
    eq(diag['admission']['reasons'], [], 'native-admission-reasons')
    eq(diag['graph']['descendingEligible'], True, 'native-graph')
    for key in ('residualLog', 'sourceReceiverMismatch'):
        value = diag.get(key)
        need(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= (1e-9 if key == 'residualLog' else 2e-9), 'native-recorded-residual-range')
    eq(diag.get('scheduleIndices'), sorted(range(64), key=lambda i: (-num(raw[i][2]), i)), 'native-recorded-schedule')
    loads, solution = n.get('loads'), n.get('solution')
    need(isinstance(loads, list) and len(loads) == 64 and isinstance(solution, list) and len(solution) == 64, 'native-load-solution-count')
    coeff = n['coefficients']
    for i, (p, row, solved) in enumerate(zip(prepared, loads, solution)):
        guard()
        integer(row.get('id'), i, i, 'load-id')
        integer(solved.get('id'), i, i, 'solution-id')
        y = num(solved.get('y'))
        need(0 < y <= 1, 'solution-y-range')
        rotors = solved.get('rotors')
        need(isinstance(rotors, list) and len(rotors) == 4, 'solution-rotors')
        forces = vector(p['forces'], 4)
        rotor = vector(row.get('rotor'), 4)
        axis = vector(p['axis'], 3)
        collective = 0.0
        moment = [0.0, 0.0, 0.0]
        for r, rr in enumerate(rotors):
            alpha, x, thrust = (num(rr[key]) for key in ('alpha', 'x', 'T'))
            need(alpha >= 0 and 0 < x <= 1 and 0 < thrust <= forces[r], 'solution-rotor-range')
            eq(rr['T'], word(forces[r]*x), 'solution-thrust-product')
            eq(row['rotor'][r], rr['T'], 'load-rotor-binding')
            alpha_expected = 0.0
            for z in range(coeff['offsets'][4*i+r], coeff['offsets'][4*i+r+1]):
                alpha_expected += num(coeff['a'][z])*num(solution[coeff['sourceIndices'][z]]['y'])
            eq(rr['alpha'], word(alpha_expected), 'saved-alpha-sum')
            collective += rotor[r]
            lever = cross(vector(p['offsets'][r], 3), axis)
            for k in range(3):
                moment[k] += lever[k]*rotor[r]
        eq(row['collective'], word(collective), 'load-collective')
        equal_words(row['worldForce'], [x*collective for x in axis], 'load-world-force')
        equal_words(row['worldMoment'], moment, 'load-world-moment')
        sqrt_check(solved['y'], collective/num(p['nativeTotal']), 'solution-y-saved-load-ratio')
        add_count('nativeLoadRows')
    eq(n.get('consumption'), consume_checksum(loads), 'load-consumption-checksum')
    return loads


def stage(body, case, step_index, stage_index, raw, commands, origin):
    guard()
    eq(body.get('schema'), 'm31-coupled-stage-v1', 'stage-schema')
    eq(body.get('stageId'), f'coupled-step{step_index}-k{stage_index}', 'stage-id')
    eq(body.get('arm'), 'coupled', 'stage-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'stage-step')
    integer(body.get('stageIndex'), stage_index, stage_index, 'stage-index')
    dt = case['dt']
    t = step_index*dt
    relative = t if stage_index == 1 else t+dt/2 if stage_index in (2, 3) else t+dt
    eq(body.get('relativeTimeWord'), word(relative), 'stage-time')
    eq(body.get('originalTimeWord'), word(origin+relative), 'stage-original-time')
    eq(body.get('dtWord'), word(dt), 'stage-dt')
    eq(states(body.get('rawBeforeProjection')), raw, 'rk-stage-raw-binding')
    eq(body.get('commandsBeforeEvaluation'), commands, 'held-stage-commands')
    integer(body.get('nativeCalls'), 1, 1, 'native-call-per-stage')
    need('nativeThrown' not in body and 'nativeMalformed' not in body, 'unexpected-native-failure')
    projected = states(body.get('nativeInput'))
    loads = native_evidence(body)
    add_count('attemptedStages')
    if loads is None:
        eq(body.get('status'), 'failed', 'refused-stage-status')
        eq(body.get('reason'), 'native-non-success', 'refused-stage-reason')
        eq(body.get('records'), [], 'refused-stage-consumption')
        eq(body.get('projectedOnFailure'), body['nativeInput'], 'refused-projection-binding')
        projection(raw, projected)
        add_count('refusedStages')
        return None
    eq(body.get('status'), 'completed', 'successful-stage-status')
    eq(body.get('reason'), None, 'successful-stage-reason')
    rows = body.get('records')
    eq(states(rows, 'stateWords', False), projected, 'stage-projected-rows')
    projection(raw, projected, rows)
    derivatives = [derivative(row, loads[i], commands[i], raw[i], projected[i]) for i, row in enumerate(rows)]
    add_count('successfulStages')
    return derivatives


def journal_descriptor(case, segment, value):
    need(type(value) is dict and set(value) == {'file', 'bytes', 'sha256', 'records',
         'parts', 'rawBytes', 'rawSha256'}, 'journal-descriptor-fields')
    eq(value['file'], case['caseId']+f'-s{segment["segment"]}.jsonl.gz', 'journal-name')
    integer(value['bytes'], 1, MAX_INPUT, 'journal-byte-bound')
    steps = round(segment['duration']/case['dt'])
    records = 6*steps + (steps+case['stepsPerControl']-1)//case['stepsPerControl'] + 2
    integer(value['records'], 2, records, 'journal-record-bound')
    integer(value['rawBytes'], 1, value['records']*MAX_RECORD, 'raw-journal-byte-bound')
    for key in ('sha256', 'rawSha256'):
        need(isinstance(value[key], str) and HASH.fullmatch(value[key]), 'journal-hash-format')
    need(type(value['parts']) is list and 1 <= len(value['parts']) <= 128, 'journal-parts-count')
    offset = 0
    for i, part in enumerate(value['parts']):
        need(type(part) is dict and set(part) == {'file', 'bytes', 'sha256', 'offset'}, 'part-fields')
        eq(part['file'], value['file']+f'.part{i:03d}', 'part-name-order')
        integer(part['offset'], offset, offset, 'part-contiguous-offset')
        integer(part['bytes'], 1, MAX_PART, 'part-byte-bound')
        if i < len(value['parts'])-1:
            integer(part['bytes'], MAX_PART, MAX_PART, 'nonfinal-full-part')
        need(isinstance(part['sha256'], str) and HASH.fullmatch(part['sha256']), 'part-hash')
        safe_path(BASE/'results', part['file'])
        offset += part['bytes']
    eq(offset, value['bytes'], 'part-aggregate-byte-count')
    return value


class PartReader(io.RawIOBase):
    def __init__(self, descriptor):
        super().__init__()
        self.descriptor, self.index, self.current, self.at = descriptor, 0, b'', 0
        self.total, self.digest, self.verified = 0, hashlib.sha256(), False

    def readable(self):
        return True

    def readinto(self, buffer):
        guard()
        if not buffer:
            return 0
        if self.at == len(self.current):
            if self.index == len(self.descriptor['parts']):
                eq(self.total, self.descriptor['bytes'], 'compressed-byte-total')
                eq(self.digest.hexdigest(), self.descriptor['sha256'], 'compressed-hash-total')
                self.verified = True
                return 0
            part = self.descriptor['parts'][self.index]
            eq(part['offset'], self.total, 'stream-part-offset')
            self.current = checked(safe_path(BASE/'results', part['file']), part)
            self.at = 0
            self.index += 1
            self.total += len(self.current)
            self.digest.update(self.current)
        count = min(len(buffer), len(self.current)-self.at)
        buffer[:count] = self.current[self.at:self.at+count]
        self.at += count
        return count


class Journal:
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.parts = PartReader(descriptor)
        self.buffer = io.BufferedReader(self.parts, 1024*1024)
        self.stream = gzip.GzipFile(fileobj=self.buffer, mode='rb')
        self.sequence, self.raw_bytes, self.raw_hash = 0, 0, hashlib.sha256()

    def take(self, kind):
        guard()
        line = self.stream.readline(MAX_RECORD+1)
        need(0 < len(line) <= MAX_RECORD and line.endswith(b'\n'), 'missing-or-oversize-record')
        provenance = {'sequence': self.sequence, 'offset': self.raw_bytes,
                      'bytes': len(line), 'sha256': hashlib.sha256(line).hexdigest()}
        self.raw_bytes += len(line)
        self.raw_hash.update(line)
        need(self.raw_bytes <= self.descriptor['rawBytes'], 'raw-journal-byte-budget')
        value = parse(line)
        need(type(value) is dict and set(value) == {'sequence', 'kind', 'body'}, 'journal-envelope')
        integer(value['sequence'], self.sequence, self.sequence, 'journal-sequence')
        eq(value['kind'], kind, 'journal-order:'+kind)
        need(type(value['body']) is dict, 'journal-body')
        self.sequence += 1
        need(self.sequence <= self.descriptor['records'], 'excess-journal-record')
        add_count('records')
        return value['body'], provenance

    def finish(self):
        need(self.stream.read(1) == b'', 'trailing-journal-data')
        need(self.parts.verified, 'compressed-stream-verification')
        eq(self.raw_bytes, self.descriptor['rawBytes'], 'raw-journal-byte-total')
        eq(self.raw_hash.hexdigest(), self.descriptor['rawSha256'], 'raw-journal-hash')
        eq(self.sequence, self.descriptor['records'], 'journal-record-total')
        self.stream.close()
        self.buffer.close()


def memory_frame(current, time_word, segment, local_step, global_step, provenance, passed):
    return {'time': num(time_word), 'timeWord': time_word, 'segment': segment,
            'stepIndex': local_step, 'globalStep': global_step,
            'positions': [vector(row[:3], 3) for row in current],
            'id17Vz': num(current[17][5]), 'safetyPassed': passed,
            'recordProvenance': provenance}


def motion_summary(initial, final, final_words):
    return {'scope': 'initial to last saved completed endpoint',
            'meanDz': left_sum([b[2]-a[2] for a, b in zip(initial, final)])/64,
            'id17': {'initialZ': initial[17][2], 'finalZ': final[17][2],
                     'finalVz': num(final_words[17][5])}, 'physicalValidity': False}


def audit_case(case, entry, paired_initial=None):
    for key in ('caseId', 'pairId', 'arm', 'seed', 'dt', 'stepsPerControl'):
        eq(entry.get(key), case[key], 'path-configuration')
    segments = entry.get('segments')
    need(type(segments) is list and 1 <= len(segments) <= 2, 'path-segment-count')
    is_memory = case['arm'] == 'memory'
    current, memory, initial_words = None, initial_memory() if is_memory else None, None
    frames, journals, segment_outcomes, controls = [], [], [], []
    total_completed = total_attempted = 0
    status, reason, issues, refusal, refused_frame = 'completed', None, [], None, None
    for ordinal, segment in enumerate(SEGMENTS):
        need(ordinal < len(segments), 'required-path-segment-missing')
        saved = segments[ordinal]
        descriptor = journal_descriptor(case, segment, saved['journal'])
        journal = Journal(descriptor)
        body, provenance = journal.take('initial')
        if ordinal == 0:
            current = states(body.get('input'))
            initial_words = current
            add_count('initialWordsValidated', 64*17)
            if paired_initial is not None:
                eq(current, paired_initial, 'paired-all-64-by-17-initial-word-equality')
                add_count('pairedInitialWordComparisons', 64*17)
        expected_initial = {'caseId': case['caseId'], 'segment': ordinal,
                            'timeOrigin': segment['timeOrigin'], 'input': input_from(current),
                            'controllerMemory': memory}
        eq(body, expected_initial, 'exact-initial-or-own-boundary-state-and-memory')
        states(body['input'])
        check_memory(body['controllerMemory'], memory, 'initial-or-boundary-controller-memory')
        if ordinal == 0:
            if is_memory:
                add_count('initialMemoryWordComparisons', 64*2)
            frames.append(memory_frame(current, word(0.0), 0, None, 0, provenance, None))
        else:
            add_count('segmentBoundaryWordComparisons', 64*17)
            if is_memory:
                add_count('segmentBoundaryMemoryWordComparisons', 64*2)
        completed = attempted = 0
        commands = None
        max_steps = round(segment['duration']/case['dt'])
        status, reason, issues, refusal = 'completed', None, [], None
        for step_index in range(max_steps):
            guard()
            if step_index % case['stepsPerControl'] == 0:
                body, control_provenance = journal.take('controller')
                commands, memory, observation = controller(body, case, step_index, current,
                                                           segment['timeOrigin'], memory)
                controls.append({**observation, 'controllerProvenance': control_provenance})
            need(commands is not None, 'segment-initial-controller-required')
            base, ks = numeric(current), []
            for stage_index in range(1, 5):
                if stage_index == 1:
                    raw = current
                else:
                    scale = case['dt'] if stage_index == 4 else case['dt']/2
                    raw = [[word(value+scale*ks[-1][i][j]) for j, value in enumerate(row)]
                           for i, row in enumerate(base)]
                body, provenance = journal.take('stage')
                derivative_values = stage(body, case, step_index, stage_index, raw, commands, segment['timeOrigin'])
                attempted += 1
                if derivative_values is None:
                    native = body['native']
                    status, reason = 'stopped', 'native-refusal'
                    refusal = {'status': native['status'], 'reason': native['reason'], 'stage': native['stage'],
                               'admission': native.get('diagnostics', {}).get('admission') if native.get('diagnostics') else None,
                               'stepIndex': step_index, 'stageIndex': stage_index,
                               'relativeTimeWord': body['relativeTimeWord']}
                    trial = states(body['nativeInput'])
                    refused_frame = {'time': num(body['originalTimeWord']), 'timeWord': body['originalTimeWord'],
                                     'segment': ordinal, 'stepIndex': step_index, 'stageIndex': stage_index,
                                     'attemptedGlobalStep': total_completed+step_index,
                                     'positions': [vector(row[:3], 3) for row in trial],
                                     'id17Vz': num(trial[17][5]), 'status': native['status'],
                                     'reason': native['reason'], 'kind': 'refused-stage',
                                     'recordProvenance': provenance, 'safetyPassed': None}
                    break
                ks.append(derivative_values)
            if refusal is not None:
                break
            body, provenance = journal.take('step')
            current = endpoint(body, case, step_index, current, ks, segment['timeOrigin'])
            completed += 1
            check, safety_provenance = journal.take('safety')
            eq(set(check), {'stepIndex', 'issues', 'pass'}, 'safety-envelope-fields')
            passed = safety(check, step_index)
            frame = memory_frame(current, body['originalTimeWord'], ordinal, step_index,
                                 total_completed+completed, provenance, passed)
            frame['safetyProvenance'] = safety_provenance
            frames.append(frame)
            if not passed:
                status, reason, issues = 'stopped', 'endpoint-contact-or-vehicle-limit', check['issues']
                break
        terminal, _ = journal.take('case-end')
        expected = {'caseId': case['caseId'], 'segment': ordinal,
                    'timeOrigin': segment['timeOrigin'], 'completedSteps': completed,
                    'attemptedStages': attempted, 'status': status, 'reason': reason,
                    'refusal': refusal, 'lastTime': completed*case['dt'],
                    'finalInput': input_from(current), 'controllerMemory': memory, 'terminationIssues': issues}
        eq(terminal, expected, 'segment-case-end-binding')
        eq({key: value for key, value in saved.items() if key != 'journal'}, expected, 'segment-index-binding')
        check_memory(terminal['controllerMemory'], memory, 'terminal-controller-memory-without-rollback')
        journal.finish()
        total_completed += completed
        total_attempted += attempted
        segment_outcomes.append({key: value for key, value in expected.items() if key not in ('finalInput', 'controllerMemory')})
        journals.append(descriptor)
        if status == 'stopped':
            eq(len(segments), ordinal+1, 'no-segment-after-first-stop')
            break
    eq(len(journals), len(segments), 'no-extra-path-segment')
    last_segment = segment_outcomes[-1]
    absolute_last = last_segment['timeOrigin']+last_segment['lastTime']
    expected_case = {**case, 'segments': segments, 'status': status, 'reason': reason,
                     'refusal': refusal, 'controllerMemory': memory,
                     'completedSteps': total_completed, 'attemptedStages': total_attempted,
                     'lastTime': absolute_last, 'finalInput': input_from(current), 'terminationIssues': issues}
    eq(entry, expected_case, 'whole-path-index-binding')
    extra_stages = refusal['stageIndex'] if refusal is not None else 0
    eq(total_attempted, 4*total_completed+extra_stages, 'successful-prefix-and-refused-attempt-accounting')
    eq([frame['globalStep'] for frame in frames], list(range(len(frames))), 'completed-frame-contiguity')
    eq([record['globalControlIndex'] for record in controls], list(range(len(controls))), 'control-contiguity')
    if is_memory:
        for row in memory:
            integer(row['updates'], len(controls), len(controls), 'final-memory-update-count')
    else:
        need(memory is None, 'original-final-memory-null')
    view = {'pathCaseId': case['caseId'], 'pairId': case['pairId'], 'controllerKind': case['arm'],
            'frames': frames, 'status': status, 'reason': reason, 'refusal': refusal,
            'refusedFrame': refused_frame, 'lastTime': absolute_last, 'lastSavedTime': frames[-1]['time'],
            'completedSteps': total_completed, 'attemptedStages': total_attempted,
            'terminationIssues': issues, 'terminationIssueIds': sorted({identity for issue in issues
                for identity in (issue['ids'] if issue['kind'] == 'drone-contact' else [issue['id']])}),
            'controllerMemory': memory, 'controllerObservations': controls,
            'controllerObservationDisclosure': 'own saved requested vertical velocity; paired MAE uses common control indices, not a common desired trajectory',
            'segments': segment_outcomes,
            'descriptiveMotion': motion_summary(frames[0]['positions'], frames[-1]['positions'], current),
            'scope': 'new fully audited coupled path; initializer, steering and contact geometry not regenerated'}
    return view, journals, initial_words


def separation(left, right):
    delta = [[a[k]-b[k] for k in range(3)] for a, b in zip(left, right)]
    squared = [(row[0]*row[0]+row[1]*row[1])+row[2]*row[2] for row in delta]
    largest = max(range(64), key=lambda i: squared[i])
    return {'maxCenterSeparation': math.sqrt(squared[largest]), 'atMaxId': largest,
            'rmsCenterSeparation': math.sqrt(left_sum(squared)/64),
            'meanZDifference': left_sum([row[2] for row in delta])/64,
            'id17ZDifference': delta[17][2]}


def paired_error(memory, original):
    left = {row['globalControlIndex']: row for row in memory['controllerObservations']}
    right = {row['globalControlIndex']: row for row in original['controllerObservations']}
    common = sorted(left.keys() & right.keys())
    result = {'available': bool(common), 'commonControlCount': len(common),
              'vehicleSamplesPerArm': 64*len(common), 'firstGlobalControlIndex': None,
              'lastGlobalControlIndex': None, 'memoryTimeWindow': None, 'originalTimeWindow': None,
              'memoryMeanAbsoluteVerticalError': None, 'originalMeanAbsoluteVerticalError': None,
              'memoryMinusOriginal': None,
              'arithmetic': 'per control: left-to-right sum of 64 absolute own-request errors divided by 64; then chronological sum over common controls divided by count',
              'scope': 'paired descriptive own-request MAE; different state-dependent desired references; includes a saved due controller before native refusal',
              'commonDesiredReference': False, 'trackingGuarantee': False, 'pooledAcrossPairs': False}
    if not common:
        return result
    eq(common, list(range(len(common))), 'common-controller-prefix')
    for index in common:
        eq(left[index]['timeWord'], right[index]['timeWord'], 'paired-controller-schedule-time')
    memory_mean = left_sum([left[index]['meanAbsoluteVerticalError'] for index in common])/len(common)
    original_mean = left_sum([right[index]['meanAbsoluteVerticalError'] for index in common])/len(common)
    difference = memory_mean-original_mean
    need(all(math.isfinite(value) for value in (memory_mean, original_mean, difference)), 'finite-paired-mae')
    result.update({'firstGlobalControlIndex': common[0], 'lastGlobalControlIndex': common[-1],
                   'memoryTimeWindow': [left[common[0]]['time'], left[common[-1]]['time']],
                   'originalTimeWindow': [right[common[0]]['time'], right[common[-1]]['time']],
                   'memoryMeanAbsoluteVerticalError': memory_mean,
                   'originalMeanAbsoluteVerticalError': original_mean, 'memoryMinusOriginal': difference})
    return result


def compare_arms(case, memory, coupled):
    last = min(len(memory['frames']), len(coupled['frames']))-1
    left, right = memory['frames'][last], coupled['frames'][last]
    eq(left['globalStep'], last, 'memory-common-step')
    eq(right['globalStep'], last, 'original-common-step')
    return {'scope': 'memory minus newly audited original controller at the last common saved completed endpoint',
            'globalStep': last, 'nominalTime': last*case['dt'],
            'memorySavedTime': left['time'], 'coupledSavedTime': right['time'],
            'memorySafetyPassed': left['safetyPassed'], 'coupledSafetyPassed': right['safetyPassed'],
            'memoryMeanDz': left_sum([b[2]-a[2] for a, b in zip(memory['frames'][0]['positions'], left['positions'])])/64,
            'coupledMeanDz': left_sum([b[2]-a[2] for a, b in zip(coupled['frames'][0]['positions'], right['positions'])])/64,
            'memoryId17Z': left['positions'][17][2], 'coupledId17Z': right['positions'][17][2],
            'memoryId17Vz': left['id17Vz'], 'coupledId17Vz': right['id17Vz'],
            'id17VzDifference': left['id17Vz']-right['id17Vz'],
            'velocityDisclosure': 'both velocities come from the newly audited completed endpoint states',
            **separation(left['positions'], right['positions']),
            'pairedOwnRequestError': paired_error(memory, coupled),
            'extrapolated': False, 'causalAttribution': False, 'physicalValidity': False}


def audit():
    publication, manifest_pin, publication_pin, source_pins, dependencies = source_gate()
    storage_evidence = storage_gate(source_pins)
    motivating_context = motivation_gate(source_pins)
    gate_pins, gate = [], {}
    for name in ('producer-supervisor.json', 'results/launch.json', 'results/exit.json', 'results/index.json'):
        identity, raw = capture(name)
        gate_pins.append(identity)
        gate[name] = parse(raw)
    supervisor, exit_record, index = (gate['producer-supervisor.json'], gate['results/exit.json'], gate['results/index.json'])
    need(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True
         and 0 <= supervisor['wallSeconds'] <= 2400, 'producer-supervised-success')
    need(exit_record.get('closed') is True and exit_record.get('exitCode') == 0
         and 0 <= exit_record['wallSeconds'] <= 2400, 'producer-internal-success')
    eq(gate['results/launch.json']['sourceCommit'], publication['commit'], 'producer-launch-source')
    eq(index.get('schema'), 'm31-unseen-pairs-v1', 'producer-index-schema')
    need(index.get('complete') is True and 'failure' not in index, 'producer-index-complete')
    eq(index.get('sourceCommit'), publication['commit'], 'producer-index-source')
    eq(index.get('config'), EXPECTED_CONFIG, 'producer-config')
    integer(index.get('totalNativeCalls'), 1, 16000, 'native-query-budget')
    need(type(index.get('cases')) is list and len(index['cases']) == 4, 'four-producer-paths')
    need(type(index.get('wallSeconds')) in (int, float) and 0 <= index['wallSeconds'] <= 2400, 'producer-wall-bound')
    paths, descriptors, initial_by_pair = {}, [], {}
    for case, entry in zip(CASES, index['cases']):
        pair_id = case['pairId']
        if case['arm'] == 'original':
            need(pair_id not in initial_by_pair, 'original-path-first-in-pair')
            paired_initial = None
        else:
            need(pair_id in initial_by_pair, 'original-initial-required-for-memory-pair')
            paired_initial = initial_by_pair[pair_id]
        view, journals, initial = audit_case(case, entry, paired_initial)
        if case['arm'] == 'original':
            initial_by_pair[pair_id] = initial
        paths[case['caseId']] = view
        descriptors.extend(journals)
    need(initial_by_pair[PAIRS[0]['pairId']] != initial_by_pair[PAIRS[1]['pairId']], 'distinct-seeds-have-distinct-saved-initial-states')
    views = []
    categories = ('both-completed', 'original-only-completed', 'memory-only-completed', 'neither-completed')
    completion_counts = {key: 0 for key in categories}
    for pair in PAIRS:
        selected = {case['arm']: paths[case['caseId']] for case in CASES if case['pairId'] == pair['pairId']}
        original, memory = selected['original'], selected['memory']
        original_done, memory_done = original['status'] == 'completed', memory['status'] == 'completed'
        category = ('both-completed' if original_done and memory_done else
                    'original-only-completed' if original_done else
                    'memory-only-completed' if memory_done else 'neither-completed')
        completion_counts[category] += 1
        views.append({**pair, 'completionCategory': category, 'memory': memory, 'coupled': original,
                      'comparison': compare_arms(pair, memory, original)})
    integer(COUNTS['completedSteps'], 0, 4000, 'total-completed-step-budget')
    integer(COUNTS['attemptedStages'], 1, 16000, 'total-stage-budget')
    integer(index.get('totalStages'), COUNTS['attemptedStages'], COUNTS['attemptedStages'], 'producer-stage-accounting')
    integer(index['totalNativeCalls'], COUNTS['attemptedStages'], COUNTS['attemptedStages'], 'one-native-call-per-attempted-stage')
    eq(COUNTS['successfulStages']+COUNTS['refusedStages'], COUNTS['attemptedStages'], 'native-stage-outcome-accounting')
    eq(COUNTS['controllerRows'], COUNTS['controllerRecords']*64, 'controller-row-accounting')
    eq(COUNTS['originalControllerRecords']+COUNTS['memoryControllerRecords'], COUNTS['controllerRecords'], 'controller-arm-accounting')
    eq(COUNTS['originalControllerRows'], COUNTS['originalControllerRecords']*64, 'original-controller-row-accounting')
    eq(COUNTS['memoryRows'], COUNTS['memoryControllerRecords']*64, 'memory-row-accounting')
    eq(COUNTS['memoryIntegrations'], (COUNTS['memoryControllerRecords']-2)*64, 'prior-error-integrations-exclude-two-first-updates')
    eq(COUNTS['initialWordsValidated'], 4*64*17, 'four-saved-initial-states')
    eq(COUNTS['pairedInitialWordComparisons'], 2*64*17, 'two-exact-initial-pair-comparisons')
    eq(COUNTS['safetyRecords'], COUNTS['completedSteps'], 'one-safety-record-per-endpoint')
    expected_names = {'launch.json', 'index.json', 'exit.json'}
    for descriptor in descriptors:
        expected_names.update(part['file'] for part in descriptor['parts'])
    actual_paths = list((BASE/'results').iterdir())
    eq({path.name for path in actual_paths}, expected_names, 'producer-output-closed-set')
    need(all(path.is_file() and not path.is_symlink() for path in actual_paths), 'producer-output-regular-files')
    total_bytes = sum(path.stat().st_size for path in actual_paths)
    need(total_bytes <= MAX_INPUT, 'producer-output-byte-cap')
    integer(supervisor.get('outputBytes'), total_bytes, total_bytes, 'producer-supervisor-output-binding')
    launch_bytes = next(pin['bytes'] for pin in gate_pins if pin['file'] == 'results/launch.json')
    before_index_bytes = launch_bytes+sum(item['bytes'] for item in descriptors)
    integer(index.get('outputBytesBeforeIndex'), before_index_bytes, before_index_bytes, 'producer-pre-index-byte-accounting')
    for relative, pin in source_pins.items():
        checked(safe_path(ROOT, relative), pin)
    checked(safe_path(BASE, 'source-manifest.json'), manifest_pin)
    checked(safe_path(BASE, 'source-publication.json'), publication_pin)
    for pin in gate_pins:
        checked(safe_path(BASE, pin['file']), pin)
    for descriptor in descriptors:
        for part in descriptor['parts']:
            checked(safe_path(BASE/'results', part['file']), part)
    guard()
    index_pin = next(pin for pin in gate_pins if pin['file'] == 'results/index.json')
    viewer = {'schema': 'm31-unseen-pairs-view-v1', 'sourceCommit': publication['commit'],
              'sourceManifestSha256': manifest_pin['sha256'], 'indexPin': index_pin,
              'physicalValidity': False, 'focusId': 17, 'floorZ': 0, 'bodyRadius': .075,
              'timeLabel': 'absolute seconds from each pair shared saved initial state',
              'scope': 'four newly audited paths; completed endpoint comparisons and own-request MAE over paired common evidence',
              'cases': views, 'sameSeedComparisons': [], 'resolutionStudy': False}
    report = {'schema': 'm31-unseen-pairs-audit-v1', 'passed': True, 'evidenceIntegrityPassed': True,
              'sourceCommit': publication['commit'], 'sourceManifestSha256': manifest_pin['sha256'],
              'sourcePublicationPin': publication_pin, 'indexPin': index_pin,
              'producerClosurePins': gate_pins, 'storageQualification': storage_evidence,
              'motivatingContext': motivating_context, 'journalPins': descriptors,
              'staticDependencyClosure': dependencies, 'counts': COUNTS,
              'verifiedProducerNativeCalls': COUNTS['attemptedStages'], 'newNativeQueriesByAudit': 0,
              'newNumericalProducerCallsByAudit': 0, 'oldNumericalTrajectoriesParsedByAudit': 0,
              'seedExposurePin': source_pins[REL+'/SEED-EXPOSURE.md'],
              'seedExposureScope': 'scoped historical-search provenance only; audit does not establish randomness or exhaustive prior nonuse',
              'allPathsCompleted': all(path['status'] == 'completed' for path in paths.values()),
              'allMemoryPathsCompleted': all(case['memory']['status'] == 'completed' for case in views),
              'allOriginalPathsCompleted': all(case['coupled']['status'] == 'completed' for case in views),
              'allAttemptedNativeStagesAdmitted': COUNTS['refusedStages'] == 0,
              'pairedCompletionCounts': completion_counts,
              'primaryOutcome': 'per-pair original/memory completion category with each path status/reason/refusal retained',
              'memoryOutcomeCounts': {'completed': sum(case['memory']['status'] == 'completed' for case in views),
                                      'stopped': sum(case['memory']['status'] == 'stopped' for case in views)},
              'originalOutcomeCounts': {'completed': sum(case['coupled']['status'] == 'completed' for case in views),
                                        'stopped': sum(case['coupled']['status'] == 'stopped' for case in views)},
              'caseOutcomes': [{**{key: case[key] for key in ('caseId', 'pairId', 'seed', 'dt', 'completionCategory')},
                  'memory': {key: value for key, value in case['memory'].items() if key != 'frames'},
                  'coupled': {key: value for key, value in case['coupled'].items() if key != 'frames'},
                  'comparison': case['comparison']} for case in views],
              'sameSeedComparisons': [], 'resolutionStudy': False, 'readEvents': READ_EVENTS,
              'physicalValidity': False, 'causalAttribution': False, 'exactRationalProof': False,
              'statisticalInference': False, 'generalReliabilityClaim': False,
              'arithmeticScope': 'both new controller target laws and own-request errors; memory recurrences; all saved coupled native evidence/load bindings, projections, 17-component derivatives and projected RK endpoints',
              'sqrtPolicy': 'saved positive sqrt within one ULP of Python math.sqrt; saved value used downstream; refused-stage omitted norm checked against three sqrt candidates',
              'implementationDisclosure': 'standard-library-only auditor; native/projection/derivative helpers reused from independent continuation Python auditor; journal and memory checks inherited from independent vertical-memory/transfer auditors; new paired traversal/error aggregation; no producer imports',
              'notRegenerated': ['initializer', 'Boids steering', 'neighbor membership', 'inherited actuator controller law',
                                 'saturation decisions', 'obstacle/contact geometry', 'native geometry coefficients', 'native root solve', 'residual model'],
              'comparisonScope': 'two fixed new seed pairs at one resolution; own-reference descriptive MAE, not common-reference tracking; no pooled statistics, normality, significance, population reliability, resolution or physical-validation claim'}
    return report, viewer


def main():
    global START
    START = time.monotonic()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'optimized-Python-not-permitted')
    need((BASE/'audit-supervisor-launch.lock').is_file(), 'audit-supervisor-allocation-required')
    target = BASE/'audit'
    need(not target.is_symlink(), 'audit-output-symlink')
    target.mkdir()  # Exclusive: a failed allocation is never retried.
    launch = {'schema': 'm31-unseen-pairs-audit-launch-v1',
              'startedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'maxWallSeconds': MAX_SECONDS, 'maxOutputBytes': MAX_OUTPUT, 'python': sys.version,
              'scope': 'saved data only; no numerical producer or native execution'}
    with (target/'launch.json').open('xb') as stream:
        stream.write(json_bytes(launch))
    try:
        report, viewer = audit()
        raw_viewer = json_bytes(viewer)
        report['viewerPin'] = {'file': 'audit/viewer-data.json', 'bytes': len(raw_viewer),
                               'sha256': hashlib.sha256(raw_viewer).hexdigest()}
        report['wallSeconds'] = time.monotonic()-START
        raw_report = json_bytes(report)
        need(len(raw_viewer)+len(raw_report)+16384 <= MAX_OUTPUT, 'audit-output-byte-budget')
        with (target/'viewer-data.json').open('xb') as stream:
            stream.write(raw_viewer)
        guard()
        with (target/'audit.json').open('xb') as stream:
            stream.write(raw_report)
        guard()
        exit_code = 0
    except Exception as error:
        exit_code = 1
        failure = {'schema': 'm31-unseen-pairs-audit-v1', 'passed': False,
                   'evidenceIntegrityPassed': False, 'singleAllocationClosed': True,
                   'failure': type(error).__name__+': '+str(error).replace(str(ROOT), '[repository]')[:2000],
                   'countsAtFailure': COUNTS, 'readEvents': READ_EVENTS,
                   'wallSeconds': time.monotonic()-START, 'physicalValidity': False}
        filename = 'failure.json' if (target/'audit.json').exists() else 'audit.json'
        with (target/filename).open('xb') as stream:
            stream.write(json_bytes(failure))
    with (target/'exit.json').open('xb') as stream:
        stream.write(json_bytes({'closed': True, 'exitCode': exit_code, 'wallSeconds': time.monotonic()-START}))
    print(json.dumps({'passed': exit_code == 0, 'wallSeconds': time.monotonic()-START}))
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
