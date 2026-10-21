"""Independent nominal-arm saved-evidence audit. Never imports the producer.

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
MAX_SECONDS = 1200
MAX_OUTPUT = 128*1024*1024
MAX_INPUT = 2*1024*1024*1024
MAX_PART = 32*1024*1024
MAX_RECORD = 4*1024*1024
HEX = re.compile(r'^[0-9a-f]{16}$')
HASH = re.compile(r'^[0-9a-f]{64}$')
START = None
READ_EVENTS = []
READ_OPERATION = 0
COUNTS = {key: 0 for key in ('records', 'controllerRecords', 'attemptedStages',
          'successfulStages', 'completedSteps', 'safetyRecords', 'projectionRows',
          'derivativeRows', 'nominalLoadRows', 'sqrtComparisons', 'sqrtOneUlpDifferences',
          'initialWordComparisons', 'segmentBoundaryWordComparisons')}
CASES = [
    {'caseId': 'seed2026102001-h005', 'seed': 2026102001, 'dt': .005, 'stepsPerControl': 2},
    {'caseId': 'seed2026102001-h0025', 'seed': 2026102001, 'dt': .0025, 'stepsPerControl': 4},
    {'caseId': 'seed2026102002-h005', 'seed': 2026102002, 'dt': .005, 'stepsPerControl': 2},
    {'caseId': 'seed2026102002-h0025', 'seed': 2026102002, 'dt': .0025, 'stepsPerControl': 4}]
SEGMENTS = [{'segment': 0, 'timeOrigin': 0, 'duration': 1},
            {'segment': 1, 'timeOrigin': 1, 'duration': 4}]
EXPECTED_CONFIG = {'schema': 'm31-nominal-comparison-config-v1', 'n': 64,
    'controlDt': .01, 'duration': 5, 'maxStages': 24000, 'maxNativeCalls': 0,
    'maxWallSeconds': 1200, 'maxOutputBytes': MAX_INPUT, 'maxRecordBytes': MAX_RECORD,
    'cases': CASES, 'segments': SEGMENTS}
PRIOR = {'original': 'research/m31-boids-admission-2026-10-20',
         'continuation': 'research/m31-boids-continuation-2026-10-20'}
DESCENT_INPUTS = 'research/m31-descent-trace-2026-10-20/inputs.json'
PRIOR_PUBLICATIONS = {
    'original': ('admission', '637c25294f162bea39970d12df0206f25dead889', 20563,
        'a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b', 100),
    'continuation': ('continuation', 'a0f595f34a4f9ef8cef516caa0cde60053e0eade', 33149,
        '90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81', 157)}
FRESH = 'research/m31-native-fresh-transfer-2026-10-17/source/'
IMMUTABLE = {
    'research/m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs':
        'b14b81107a5c5f08db1b14e369e61baccd3bef18ef3c6d2717fd150165ab4332',
    FRESH+'vendor/generation/step02c-source/physics.cjs':
        '0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1',
    FRESH+'vendor/generation/milestone-31-source/sim.cjs':
        '2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e',
    FRESH+'vendor/generation/milestone-31-source/grid.cjs':
        'f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302',
    FRESH+'vendor/generation/milestone-31-source/geometry.cjs':
        'e209e492fc523ab3c0c7df62745fb0d3dd7204f35e53309938a19d7895ed3d4f',
    PRIOR['continuation']+'/source/motion.cjs':
        'c8cf434a23b6c7450eabbadb5bb371398d7a8d8c8810615667822529e8d12373',
    PRIOR['continuation']+'/source/journal.cjs':
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
        need(details is not None, 'successful-projection-evidence-required')
        row = details[i]
        eq(row['normSquareWord'], word(ns), 'projection-norm-square')
        norm = sqrt_check(row['normWord'], ns, 'projection-sqrt')
        expected = raw[:6] + [x/norm for x in q] + raw[10:]
        equal_words(projected_words[i], expected, 'projection-state')
        add_count('projectionRows')

def controller(body, case, step_index, current, origin):
    eq(body.get('schema'), 'm31-coupled-controller-v1', 'controller-schema')
    eq(body.get('arm'), 'off', 'controller-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'controller-step')
    same_number(body.get('controlIndex'), step_index/case['stepsPerControl'], 'controller-index')
    eq(body.get('relativeTimeWord'), word(step_index*case['dt']), 'controller-time')
    eq(body.get('originalTimeWord'), word(origin + step_index*case['dt']), 'controller-original-time')
    rows = body.get('records')
    eq(states(rows, 'stateWords', False), current, 'controller-current-state')
    commands = []
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
        eq(target['zWord'], word(state[2]+(2.5*v[2]+1.5*state[5])/6), 'target-z-arithmetic')
        num(target['yawWord'])
        vector(row.get('commandsWords'), 4)
        vector(row.get('desiredQuaternionWords'), 4)
        need(type(row.get('saturated')) is bool, 'controller-saturation-type')
        commands.append(row['commandsWords'])
    add_count('controllerRecords')
    return commands

def derivative(row, load, commands, raw, projected):
    eq(row['rawStateWords'], raw, 'row-raw-binding')
    eq(row['stateWords'], projected, 'row-projected-binding')
    eq(row['commandsWords'], commands, 'row-command-binding')
    eq(row['nominalMotorWords'], projected[13:17], 'nominal-motor-binding')
    consumed = {'rotorWords': load['rotor'], 'collectiveWord': load['collective'],
                'worldForceWords': load['worldForce'], 'worldMomentWords': load['worldMoment']}
    eq(row['consumed'], consumed, 'same-id-nominal-load-consumption')
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
    eq(body.get('stepId'), f'off-step{step_index}', 'step-id')
    eq(body.get('arm'), 'off', 'step-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'step-index')
    dt = case['dt']
    t = step_index*dt+dt
    eq(body.get('relativeTimeWord'), word(t), 'step-time')
    eq(body.get('originalTimeWord'), word(origin+t), 'step-original-time')
    eq(body.get('dtWord'), word(dt), 'step-dt')
    eq(body.get('status'), 'completed', 'step-must-complete-in-closed-allocation')
    eq(body.get('reason'), None, 'step-reason')
    eq(states(body.get('start'), 'stateWords', False), current, 'step-start-binding')
    eq(body.get('stageIds'), [f'off-step{step_index}-k{k}' for k in range(1, 5)], 'step-stage-binding')
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
    mandatory = {REL+'/'+name for name in ('config.json', 'runtime.json', 'PROTOCOL.md',
                 'AUDIT-CONTRACT.md', 'source/run.cjs', 'source/audit.py', 'source/supervise.py')}
    mandatory.add(DESCENT_INPUTS)
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
    need(FRESH+'native-load.cjs' not in visited, 'native-solver-must-not-be-imported')
    eq(parse_frozen(REL+'/config.json', pins), EXPECTED_CONFIG, 'fixed-config')
    return publication, manifest_pin, publication_pin, pins, sorted(visited)


def prior_gate(source_pins):
    prior, evidence, public_pins = {}, [], {}
    names = ('results/index.json', 'results/exit.json', 'audit/audit.json',
             'audit/viewer-data.json', 'audit/exit.json', 'native-supervisor.json',
             'audit-supervisor.json', 'ALLOCATION-CLOSURE.json')
    for phase, (tag, commit, size, digest, count) in PRIOR_PUBLICATIONS.items():
        folder = PRIOR[phase]
        manifest_path = folder+'/result-manifest.json'
        receipt_path = 'research/publication-receipts/m31-boids-'+tag+'-result-2026-10-20.json'
        receipt = parse_frozen(receipt_path, source_pins)
        for key, value in {'commit': commit, 'manifestPath': manifest_path, 'manifestBytes': size,
                           'manifestSha256': digest, 'verifiedFilePins': count,
                           'remoteBytesEqualLocal': True, 'committedBytesEqualLocal': True}.items():
            eq(receipt.get(key), value, 'prior-public-receipt:'+key)
        manifest_pin = {'path': manifest_path, 'bytes': size, 'sha256': digest}
        eq(source_pins.get(manifest_path), manifest_pin, 'prior-public-manifest-pin')
        manifest = parse_frozen(manifest_path, source_pins)
        eq(manifest.get('schema'), 'm31-boids-'+tag+'-result-v1', 'prior-manifest-schema')
        public = {item['path']: item for item in manifest['files']}
        need(len(public) == len(manifest['files']) == count, 'prior-public-pin-uniqueness')
        public_pins[phase] = public
        small = {}
        extra = ('archive/index.json',) if phase == 'original' else ('storage/qualification.json', 'storage-supervisor.json')
        for name in names+extra:
            relative = folder+'/'+name
            need(relative in public, 'prior-selected-public-pin')
            eq(source_pins.get(relative), public[relative], 'prior-selected-source-binding')
            small[name] = parse_frozen(relative, source_pins)
        index, report, view = (small['results/index.json'], small['audit/audit.json'],
                                small['audit/viewer-data.json'])
        eq(index.get('schema'), 'm31-boids-'+tag+'-index-v1', 'prior-index-schema')
        need(index.get('complete') is True and 'failure' not in index, 'prior-producer-complete')
        eq(report.get('schema'), 'm31-boids-'+tag+'-audit-v1', 'prior-audit-schema')
        need(report.get('passed') is True and report.get('evidenceIntegrityPassed') is True
             and report.get('allAttemptedNativeStagesAdmitted') is True, 'prior-evidence-passed')
        eq(view.get('schema'), 'm31-boids-'+tag+'-view-v1', 'prior-view-schema')
        eq(view.get('physicalValidity'), False, 'prior-view-validity-disclosure')
        for key, name in (('viewerPin', 'audit/viewer-data.json'), ('indexPin', 'results/index.json'),
                          ('producerExitPin', 'results/exit.json'), ('nativeSupervisorPin', 'native-supervisor.json')):
            pin = public[folder+'/'+name]
            eq(report.get(key), {'file': name, 'bytes': pin['bytes'], 'sha256': pin['sha256']}, 'prior-audit-pinned-evidence')
        eq(view['indexPin'], report['indexPin'], 'prior-view-index-binding')
        eq(view['sourceCommit'], report['sourceCommit'], 'prior-view-source-binding')
        eq(index['sourceCommit'], report['sourceCommit'], 'prior-producer-source-binding')
        closure = small['ALLOCATION-CLOSURE.json']
        eq(closure.get('schema'), 'm31-boids-allocation-closure-v1' if phase == 'original'
           else 'm31-boids-continuation-closure-v1', 'prior-closure-schema')
        closed_phases = ('native', 'audit', 'display', 'archive') if phase == 'original' else ('storage', 'native', 'audit', 'ui')
        for name in closed_phases:
            eq(closure[name]['status'], 'closed-passed', 'prior-phase-closed-passed')
            integer(closure[name]['attempts'], 1, 1, 'prior-single-allocation')
        for name, limit in (('native', 360 if phase == 'original' else 1200),
                            ('audit', 180 if phase == 'original' else 1200)):
            supervisor = small[name+'-supervisor.json']
            need(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
                 and supervisor.get('allocationWallPassed') is True
                 and 0 <= supervisor['wallSeconds'] <= limit, 'prior-supervisor-closed-passed')
            if phase == 'continuation':
                eq(supervisor.get('outputCapPassed'), True, 'prior-supervisor-output-cap')
            exit_record = small[('results' if name == 'native' else 'audit')+'/exit.json']
            need(exit_record.get('closed') is True and exit_record.get('exitCode') == 0,
                 'prior-internal-closed-success')
        if phase == 'continuation':
            storage, supervisor = small['storage/qualification.json'], small['storage-supervisor.json']
            need(storage.get('passed') is True and storage.get('closed') is True,
                 'prior-lossless-storage-qualified')
            need(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
                 and supervisor.get('allocationWallPassed') is True
                 and supervisor.get('outputCapPassed') is True, 'prior-storage-supervised-success')
        eq([case['caseId'] for case in index['cases']], [case['caseId'] for case in CASES], 'prior-index-case-order')
        eq([case['caseId'] for case in view['cases']], [case['caseId'] for case in CASES], 'prior-view-case-order')
        prior[phase] = small
        evidence.append({'phase': phase, 'commit': commit, 'manifestPin': manifest_pin,
                         'receiptPin': source_pins[receipt_path],
                         'viewerPin': source_pins[folder+'/audit/viewer-data.json']})
    return prior, evidence, public_pins


def original_initials(prior, source_pins, public_pins):
    """Only the initial JSONL record from each verified original first part."""
    inputs = parse_frozen(DESCENT_INPUTS, source_pins)
    selected = [item for item in inputs['streams'] if item['phase'] == 'original']
    eq([item['caseId'] for item in selected], [case['caseId'] for case in CASES], 'four-original-initial-streams')
    archive = prior['original']['archive/index.json']
    eq(archive['schema'], 'm31-boids-byte-archive-v1', 'original-archive-schema')
    initials, receipts = {}, []
    for case, stream, old in zip(CASES, selected, prior['original']['results/index.json']['cases']):
        eq(stream['folder'], PRIOR['original']+'/archive', 'original-initial-folder')
        journal = old['journal']
        matches = [item for item in archive['journals'] if item['originalFile'] == 'results/'+journal['file']]
        need(len(matches) == 1 and matches[0]['reconstructionVerified'] is True, 'original-archive-binding')
        mapping = matches[0]
        eq(stream['descriptor'], {**journal, 'parts': mapping['parts']}, 'descent-original-descriptor-binding')
        eq(mapping['bytes'], journal['bytes'], 'archive-compressed-byte-binding')
        eq(mapping['sha256'], journal['sha256'], 'archive-compressed-hash-binding')
        part = stream['descriptor']['parts'][0]
        eq(part['file'], case['caseId']+'.jsonl.gz.part000', 'original-first-part-name')
        integer(part['offset'], 0, 0, 'original-first-part-offset')
        relative = stream['folder']+'/'+part['file']
        pin = {'path': relative, 'bytes': part['bytes'], 'sha256': part['sha256']}
        eq(public_pins['original'].get(relative), pin, 'original-first-part-public-pin')
        eq(source_pins.get(relative), pin, 'original-first-part-source-pin')
        raw = checked(safe_path(ROOT, relative), pin)
        with gzip.GzipFile(fileobj=io.BytesIO(raw), mode='rb') as compressed:
            line = compressed.readline(MAX_RECORD+1)
        need(0 < len(line) <= MAX_RECORD and line.endswith(b'\n'), 'original-initial-record-line')
        obj = parse(line)
        eq(set(obj), {'sequence', 'kind', 'body'}, 'original-initial-envelope')
        integer(obj['sequence'], 0, 0, 'original-initial-sequence')
        eq(obj['kind'], 'initial', 'original-initial-kind')
        eq(obj['body']['caseId'], case['caseId'], 'original-initial-case')
        initials[case['caseId']] = states(obj['body']['input'])
        receipts.append({'caseId': case['caseId'], 'partPin': pin, 'initialRecord': {
            'sequence': 0, 'offset': 0, 'bytes': len(line), 'sha256': hashlib.sha256(line).hexdigest()},
            'scope': 'verified first compressed part; initial record only, no complete baseline journal audit'})
    return initials, receipts


def nominal_load(projected):
    state = vector(projected, 17)
    q, rotor = state[6:10], state[13:17]
    axis = rotate(q, [0.0, 0.0, 1.0])
    corners = ((.028, .028, 0.0), (-.028, .028, 0.0),
               (-.028, -.028, 0.0), (.028, -.028, 0.0))
    collective, moment = 0.0, [0.0, 0.0, 0.0]
    for offset, thrust in zip(corners, rotor):
        collective += thrust
        lever = cross(rotate(q, offset), axis)
        for k in range(3):
            moment[k] += lever[k]*thrust
    add_count('nominalLoadRows')
    return {'rotor': projected[13:17], 'collective': word(collective),
            'worldForce': [word(x*collective) for x in axis],
            'worldMoment': [word(x) for x in moment]}


def stage(body, case, step_index, stage_index, raw, commands, origin):
    guard()
    eq(body.get('schema'), 'm31-coupled-stage-v1', 'stage-schema')
    eq(body.get('stageId'), f'off-step{step_index}-k{stage_index}', 'stage-id')
    eq(body.get('arm'), 'off', 'nominal-stage-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'stage-step-index')
    integer(body.get('stageIndex'), stage_index, stage_index, 'stage-number')
    dt, t = case['dt'], step_index*case['dt']
    relative = t if stage_index == 1 else t+dt/2 if stage_index in (2, 3) else t+dt
    eq(body.get('relativeTimeWord'), word(relative), 'stage-relative-time')
    eq(body.get('originalTimeWord'), word(origin+relative), 'stage-absolute-time')
    eq(body.get('dtWord'), word(dt), 'stage-dt')
    eq(body.get('status'), 'completed', 'off-stage-must-complete')
    eq(body.get('reason'), None, 'off-stage-no-refusal')
    integer(body.get('nativeCalls'), 0, 0, 'off-stage-zero-native-calls')
    eq(body.get('native'), None, 'off-stage-no-native-evidence')
    need(not any(key in body for key in ('nativeThrown', 'nativeMalformed', 'projectedOnFailure')),
         'unexpected-stage-failure-evidence')
    eq(states(body['rawBeforeProjection']), raw, 'rk-raw-stage-binding')
    eq(body['commandsBeforeEvaluation'], commands, 'held-controller-command-binding')
    projected = states(body['nativeInput'])
    rows = body['records']
    eq(states(rows, 'stateWords', False), projected, 'stage-row-projected-binding')
    projection(raw, projected, rows)
    derivatives = [derivative(row, nominal_load(projected[i]), commands[i], raw[i], projected[i])
                   for i, row in enumerate(rows)]
    add_count('attemptedStages')
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
    need(type(value['parts']) is list and 1 <= len(value['parts']) <= 64, 'journal-parts-count')
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


def off_frame(current, time_word, segment, local_step, global_step, provenance, passed):
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


def audit_off_case(case, entry, prior_initial):
    for key in ('caseId', 'seed', 'dt'):
        eq(entry.get(key), case[key], 'off-case-configuration')
    segments = entry.get('segments')
    need(type(segments) is list and 1 <= len(segments) <= 2, 'off-segment-count')
    current, frames, journals, segment_outcomes = prior_initial, [], [], []
    total_completed = total_attempted = 0
    status, reason, issues = 'completed', None, []
    for ordinal, segment in enumerate(SEGMENTS):
        need(ordinal < len(segments), 'required-off-segment-missing')
        saved = segments[ordinal]
        descriptor = journal_descriptor(case, segment, saved['journal'])
        journal = Journal(descriptor)
        body, provenance = journal.take('initial')
        expected_initial = {'caseId': case['caseId'], 'segment': ordinal,
                            'timeOrigin': segment['timeOrigin'], 'input': input_from(current)}
        eq(body, expected_initial, 'all-64-by-17-initial-or-boundary-binding')
        states(body['input'])
        if ordinal == 0:
            add_count('initialWordComparisons', 64*17)
            frames.append(off_frame(current, word(0.0), 0, None, 0, provenance, None))
        else:
            add_count('segmentBoundaryWordComparisons', 64*17)
        completed = attempted = 0
        commands = None
        max_steps = round(segment['duration']/case['dt'])
        status, reason, issues = 'completed', None, []
        for step_index in range(max_steps):
            guard()
            if step_index % case['stepsPerControl'] == 0:
                body, _ = journal.take('controller')
                commands = controller(body, case, step_index, current, segment['timeOrigin'])
            need(commands is not None, 'segment-initial-controller-required')
            base, ks = numeric(current), []
            for stage_index in range(1, 5):
                if stage_index == 1:
                    raw = current
                else:
                    scale = case['dt'] if stage_index == 4 else case['dt']/2
                    raw = [[word(value+scale*ks[-1][i][j]) for j, value in enumerate(row)]
                           for i, row in enumerate(base)]
                body, _ = journal.take('stage')
                ks.append(stage(body, case, step_index, stage_index, raw, commands, segment['timeOrigin']))
                attempted += 1
            body, provenance = journal.take('step')
            current = endpoint(body, case, step_index, current, ks, segment['timeOrigin'])
            completed += 1
            check, safety_provenance = journal.take('safety')
            eq(set(check), {'stepIndex', 'issues', 'pass'}, 'safety-envelope-fields')
            passed = safety(check, step_index)
            frame = off_frame(current, body['originalTimeWord'], ordinal, step_index,
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
                    'refusal': None, 'lastTime': completed*case['dt'],
                    'finalInput': input_from(current), 'terminationIssues': issues}
        eq(terminal, expected, 'segment-case-end-binding')
        eq({key: value for key, value in saved.items() if key != 'journal'}, expected, 'segment-index-binding')
        journal.finish()
        total_completed += completed
        total_attempted += attempted
        segment_outcomes.append({key: value for key, value in expected.items() if key != 'finalInput'})
        journals.append(descriptor)
        if status == 'stopped':
            eq(len(segments), ordinal+1, 'no-segment-after-safety-stop')
            break
    eq(len(journals), len(segments), 'no-extra-off-segment')
    last_segment = segment_outcomes[-1]
    absolute_last = last_segment['timeOrigin']+last_segment['lastTime']
    expected_case = {**case,
                     'segments': segments, 'status': status, 'reason': reason,
                     'completedSteps': total_completed, 'attemptedStages': total_attempted,
                     'lastTime': absolute_last, 'finalInput': input_from(current),
                     'terminationIssues': issues}
    eq(entry, expected_case, 'whole-path-index-binding')
    view = {'frames': frames, 'status': status, 'reason': reason,
            'lastTime': absolute_last, 'lastSavedTime': frames[-1]['time'],
            'completedSteps': total_completed, 'attemptedStages': total_attempted,
            'terminationIssues': issues, 'terminationIssueIds': sorted({identity for issue in issues
                for identity in (issue['ids'] if issue['kind'] == 'drone-contact' else [issue['id']])}),
            'segments': segment_outcomes,
            'descriptiveMotion': motion_summary(frames[0]['positions'], frames[-1]['positions'], current)}
    return view, journals


def coupled_view(case, position, prior, initial):
    joined, segment_meta = [], []
    boundary_words = None
    for ordinal, phase in enumerate(('original', 'continuation')):
        index = prior[phase]['results/index.json']['cases'][position]
        view = prior[phase]['audit/viewer-data.json']['cases'][position]
        for key in ('caseId', 'seed', 'dt', 'stepsPerControl'):
            eq(view[key], case[key], 'coupled-view-case-binding')
        eq(index['caseId'], case['caseId'], 'coupled-index-case')
        for key in ('completedSteps', 'attemptedStages', 'status', 'reason', 'lastTime', 'refusal'):
            eq(view[key], index[key], 'coupled-view-index-outcome')
        need(index['refusal'] is None and view['refusedFrame'] is None, 'frozen-coupled-no-refusals')
        maximum = round((1 if ordinal == 0 else 4)/case['dt'])
        completed = integer(index['completedSteps'], 1, maximum, 'coupled-completed-step-count')
        if ordinal == 0:
            eq(completed, maximum, 'coupled-original-horizon')
            eq(index['status'], 'completed', 'coupled-original-completed')
        eq(index['attemptedStages'], completed*4, 'coupled-stage-count')
        same_number(index['lastTime'], completed*case['dt'], 'coupled-nominal-end-time')
        frames = view['frames']
        need(type(frames) is list and len(frames) == completed+1, 'coupled-frame-count')
        final_words = states(index['finalInput'])
        for j, frame in enumerate(frames):
            guard()
            relative = 0.0 if j == 0 else (j-1)*case['dt']+case['dt']
            same_number(frame['time'], relative, 'coupled-saved-relative-time')
            absolute = relative if ordinal == 0 else 1.0+frame['time']
            if ordinal == 1:
                same_number(frame['originalTime'], absolute, 'coupled-saved-original-time')
            eq(frame['kind'], 'initial' if j == 0 else 'completed-endpoint', 'coupled-completed-frame-kind')
            eq(frame['stepIndex'], None if j == 0 else j-1, 'coupled-local-step')
            need(type(frame['positions']) is list and len(frame['positions']) == 64, 'coupled-frame-id-order')
            for coordinates in frame['positions']:
                need(type(coordinates) is list and len(coordinates) == 3
                     and all(type(x) in (int, float) and math.isfinite(x) for x in coordinates), 'coupled-position-finiteness')
            if j == 0:
                eq(frame['safetyPassed'], None, 'coupled-initial-no-safety-test')
                expected_words = initial if ordinal == 0 else boundary_words
                for coords, state in zip(frame['positions'], expected_words):
                    equal_words(state[:3], coords, 'coupled-initial-or-boundary-position-binding')
            else:
                expected_pass = not (j == completed and index['status'] == 'stopped')
                eq(frame['safetyPassed'], expected_pass, 'coupled-stop-frame-linkage')
            if ordinal == 1 and j == 0:
                continue  # Exactly one duplicated boundary frame is excluded.
            global_step = j if ordinal == 0 else round(1/case['dt'])+j
            joined.append({'time': absolute, 'timeWord': word(absolute), 'segment': ordinal,
                           'stepIndex': frame['stepIndex'], 'globalStep': global_step,
                           'positions': frame['positions'], 'safetyPassed': frame['safetyPassed'],
                           'savedViewerSequence': frame['sequence']})
        for coords, state in zip(frames[-1]['positions'], final_words):
            equal_words(state[:3], coords, 'coupled-final-position-state-binding')
        boundary_words = final_words
        segment_meta.append({key: index[key] for key in ('completedSteps', 'attemptedStages',
                            'status', 'reason', 'lastTime', 'refusal')})
    terminal = prior['continuation']['results/index.json']['cases'][position]
    expected_status = 'stopped' if position < 2 else 'completed'
    eq(terminal['status'], expected_status, 'fixed-coupled-outcome')
    eq(terminal['reason'], 'endpoint-contact-or-vehicle-limit' if position < 2 else None, 'fixed-coupled-reason')
    expected_counts = (724, 1447, 800, 1600)
    integer(terminal['completedSteps'], expected_counts[position], expected_counts[position], 'fixed-coupled-horizon')
    eq([frame['globalStep'] for frame in joined], list(range(len(joined))), 'coupled-joined-step-contiguity')
    return {'frames': joined, 'status': terminal['status'], 'reason': terminal['reason'],
            'lastTime': 1.0+terminal['lastTime'], 'lastSavedTime': joined[-1]['time'],
            'completedSteps': len(joined)-1, 'segments': segment_meta,
            'terminationIssues': None, 'terminationIssueIds': None,
            'terminationIssueDisclosure': 'prior audited replay and index retain safety flag/reason but not contact identities',
            'descriptiveMotion': motion_summary(joined[0]['positions'], joined[-1]['positions'], boundary_words),
            'scope': 'existing audited completed endpoints; no coupled rerun or interpolation'}


def separation(left, right):
    delta = [[a[k]-b[k] for k in range(3)] for a, b in zip(left, right)]
    squared = [(row[0]*row[0]+row[1]*row[1])+row[2]*row[2] for row in delta]
    largest = max(range(64), key=lambda i: squared[i])
    return {'maxCenterSeparation': math.sqrt(squared[largest]), 'atMaxId': largest,
            'rmsCenterSeparation': math.sqrt(left_sum(squared)/64),
            'meanZDifference': left_sum([row[2] for row in delta])/64,
            'id17ZDifference': delta[17][2]}


def compare_arms(case, off, coupled):
    last = min(len(off['frames']), len(coupled['frames']))-1
    left, right = off['frames'][last], coupled['frames'][last]
    eq(left['globalStep'], last, 'off-common-step')
    eq(right['globalStep'], last, 'coupled-common-step')
    return {'scope': 'off minus coupled at the last common saved completed endpoint only',
            'globalStep': last, 'nominalTime': last*case['dt'],
            'offSavedTime': left['time'], 'coupledSavedTime': right['time'],
            'offSafetyPassed': left['safetyPassed'], 'coupledSafetyPassed': right['safetyPassed'],
            'offMeanDz': left_sum([b[2]-a[2] for a, b in zip(off['frames'][0]['positions'], left['positions'])])/64,
            'coupledMeanDz': left_sum([b[2]-a[2] for a, b in zip(coupled['frames'][0]['positions'], right['positions'])])/64,
            'offId17Z': left['positions'][17][2], 'coupledId17Z': right['positions'][17][2],
            'offId17Vz': left['id17Vz'], 'coupledId17Vz': None,
            'velocityDisclosure': 'coupled per-frame velocity is not in the saved replay; no velocity difference is inferred',
            **separation(left['positions'], right['positions']),
            'extrapolated': False, 'causalAttribution': False, 'physicalValidity': False}


def resolution_sensitivity(views):
    output = []
    for coarse, fine in ((views[0], views[1]), (views[2], views[3])):
        for arm in ('off',):
            a, b = coarse[arm]['frames'], fine[arm]['frames']
            horizon = min(len(a)-1, (len(b)-1)//2)
            maximum, at = -1.0, None
            for k in range(horizon+1):
                guard()
                left, right = a[k], b[2*k]
                eq(left['globalStep'], k, 'coarse-global-step')
                eq(right['globalStep'], 2*k, 'fine-global-step')
                metric = separation(left['positions'], right['positions'])
                if metric['maxCenterSeparation'] > maximum:
                    maximum = metric['maxCenterSeparation']
                    at = {'coarseGlobalStep': k, 'fineGlobalStep': 2*k, 'id': metric['atMaxId'],
                          'coarseSavedTime': left['time'], 'fineSavedTime': right['time']}
            output.append({'seed': coarse['seed'], 'arm': arm,
                'coarseCaseId': coarse['caseId'], 'fineCaseId': fine['caseId'],
                'commonEndpointCountIncludingInitial': horizon+1,
                'lastCommonNominalTime': horizon*coarse['dt'],
                'lastCommonCoarseSavedTime': a[horizon]['time'],
                'lastCommonFineSavedTime': b[2*horizon]['time'],
                'lastCommon': separation(a[horizon]['positions'], b[2*horizon]['positions']),
                'maxCommonEndpointCenterDifference': maximum, 'atMaximum': at,
                'scope': 'same-seed coarse/fine endpoint sensitivity; integer step matching; no extrapolation',
                'independentReplicates': False, 'convergenceClaim': False, 'physicalValidity': False})
    return output


def audit():
    publication, manifest_pin, publication_pin, source_pins, dependencies = source_gate()
    prior, prior_evidence, public_pins = prior_gate(source_pins)
    initials, initial_receipts = original_initials(prior, source_pins, public_pins)
    gate_pins, gate = [], {}
    for name in ('producer-supervisor.json', 'results/launch.json', 'results/exit.json', 'results/index.json'):
        identity, raw = capture(name)
        gate_pins.append(identity)
        gate[name] = parse(raw)
    supervisor, exit_record, index = (gate['producer-supervisor.json'], gate['results/exit.json'], gate['results/index.json'])
    need(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True
         and 0 <= supervisor['wallSeconds'] <= 1200, 'producer-supervised-success')
    need(exit_record.get('closed') is True and exit_record.get('exitCode') == 0
         and 0 <= exit_record['wallSeconds'] <= 1200, 'producer-internal-success')
    eq(gate['results/launch.json']['sourceCommit'], publication['commit'], 'producer-launch-source')
    eq(index.get('schema'), 'm31-nominal-comparison-v1', 'producer-index-schema')
    need(index.get('complete') is True and 'failure' not in index, 'producer-index-complete')
    eq(index.get('sourceCommit'), publication['commit'], 'producer-index-source')
    eq(index.get('config'), EXPECTED_CONFIG, 'producer-config')
    integer(index.get('totalNativeCalls'), 0, 0, 'zero-native-query-count')
    need(type(index.get('cases')) is list and len(index['cases']) == 4, 'four-producer-cases')
    need(type(index.get('wallSeconds')) in (int, float) and 0 <= index['wallSeconds'] <= 1200, 'producer-wall-bound')
    views, descriptors, initial_by_seed = [], [], {}
    for position, (case, entry) in enumerate(zip(CASES, index['cases'])):
        initial = initials[case['caseId']]
        if case['seed'] in initial_by_seed:
            eq(initial, initial_by_seed[case['seed']], 'same-seed-exact-initial-words')
        else:
            initial_by_seed[case['seed']] = initial
        off, journals = audit_off_case(case, entry, initial)
        coupled = coupled_view(case, position, prior, initial)
        descriptors.extend(journals)
        views.append({**case, 'off': off, 'coupled': coupled,
                      'comparison': compare_arms(case, off, coupled)})
    need(initial_by_seed[2026102001] != initial_by_seed[2026102002], 'distinct-initial-seeds')
    integer(COUNTS['completedSteps'], 1, 6000, 'total-completed-step-budget')
    integer(COUNTS['attemptedStages'], 4, 24000, 'total-stage-budget')
    integer(index.get('totalStages'), COUNTS['attemptedStages'], COUNTS['attemptedStages'], 'producer-stage-accounting')
    eq(COUNTS['attemptedStages'], 4*COUNTS['completedSteps'], 'four-stages-per-completed-step')
    eq(COUNTS['safetyRecords'], COUNTS['completedSteps'], 'one-safety-record-per-endpoint')
    eq(sum(len(case['coupled']['frames']) for case in views), 5775, 'frozen-baseline-frame-count')
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
    sensitivity = resolution_sensitivity(views)
    # Recheck captured sources, closure files and every complete nominal part.
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
    viewer = {'schema': 'm31-nominal-comparison-view-v1', 'sourceCommit': publication['commit'],
              'sourceManifestSha256': manifest_pin['sha256'], 'indexPin': index_pin,
              'physicalValidity': False, 'focusId': 17, 'floorZ': 0, 'bodyRadius': .075,
              'timeLabel': 'absolute seconds from shared saved initial state',
              'scope': 'all saved endpoints, paired only while both arms have evidence; no extrapolation',
              'cases': views, 'sameSeedComparisons': sensitivity}
    report = {'schema': 'm31-nominal-comparison-audit-v1', 'passed': True, 'evidenceIntegrityPassed': True,
              'sourceCommit': publication['commit'], 'sourceManifestSha256': manifest_pin['sha256'],
              'sourcePublicationPin': publication_pin, 'indexPin': index_pin,
              'producerClosurePins': gate_pins, 'priorPublications': prior_evidence,
              'originalInitialReceipts': initial_receipts, 'journalPins': descriptors,
              'staticDependencyClosure': dependencies, 'counts': COUNTS,
              'nativeQueries': 0, 'newNumericalProducerCallsByAudit': 0,
              'allNominalPathsCompleted': all(case['off']['status'] == 'completed' for case in views),
              'nominalOutcomeCounts': {'completed': sum(case['off']['status'] == 'completed' for case in views),
                                       'stopped': sum(case['off']['status'] == 'stopped' for case in views)},
              'caseOutcomes': [{**{key: case[key] for key in ('caseId', 'seed', 'dt')},
                  'off': {key: value for key, value in case['off'].items() if key != 'frames'},
                  'coupled': {key: value for key, value in case['coupled'].items() if key != 'frames'},
                  'comparison': case['comparison']} for case in views],
              'sameSeedComparisons': sensitivity, 'readEvents': READ_EVENTS,
              'physicalValidity': False, 'causalAttribution': False, 'exactRationalProof': False,
              'independentReplicates': False,
              'arithmeticScope': 'all saved nominal-arm loads, projections, 17-component derivatives and projected RK endpoints',
              'sqrtPolicy': 'saved positive norm within one ULP of Python math.sqrt; saved norm used downstream',
              'implementationDisclosure': 'standard-library-only auditor; scalar/projection/derivative helpers adapted from prior independent Python audit; no producer imports; baseline relies on prior published audited exports',
              'notRegenerated': ['initializer', 'Boids steering', 'neighbor membership', 'controller numerical law',
                                 'saturation decisions', 'obstacle/contact geometry', 'coupled trajectory', 'native model'],
              'comparisonScope': 'model-level path contrast with diverging own controllers; no isolated force attribution or physical validation'}
    return report, viewer


def main():
    global START
    START = time.monotonic()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'optimized-Python-not-permitted')
    need((BASE/'audit-supervisor-launch.lock').is_file(), 'audit-supervisor-allocation-required')
    target = BASE/'audit'
    need(not target.is_symlink(), 'audit-output-symlink')
    target.mkdir()  # Exclusive: a failed allocation is never retried.
    launch = {'schema': 'm31-nominal-comparison-audit-launch-v1',
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
        failure = {'schema': 'm31-nominal-comparison-audit-v1', 'passed': False,
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
