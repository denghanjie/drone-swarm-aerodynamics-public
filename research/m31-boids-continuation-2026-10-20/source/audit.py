"""One saved-evidence allocation. Never imports or invokes the scientific producer.

Checks binary64 consistency, not exact rational or native-model accuracy. Read
AUDIT-CONTRACT.md before interpreting a passing report. Source-only until the
separate public-source gate and native allocation have closed.
"""
from pathlib import Path, PurePosixPath
import datetime
import gzip
import hashlib
import io
import json
import math
import re
import struct
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
REL = BASE.relative_to(ROOT).as_posix()
FRESH = 'research/m31-native-fresh-transfer-2026-10-17/source/'
OLD = 'research/m31-coupled-stage-qualification-2026-10-17/source/'
PRIOR = 'research/m31-boids-admission-2026-10-20'
PRIOR_COMMIT = '637c25294f162bea39970d12df0206f25dead889'
PRIOR_RECEIPT = 'research/publication-receipts/m31-boids-admission-result-2026-10-20.json'
PRIOR_MANIFEST_HASH = 'a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b'
PRIOR_SMALL_FILES = ('results/index.json', 'audit/audit.json', 'audit/exit.json',
                     'results/exit.json', 'native-supervisor.json', 'audit-supervisor.json',
                     'ALLOCATION-CLOSURE.json')
MAX_SECONDS = 1200
MAX_OUTPUT = 64 * 1024 * 1024
MAX_INPUT = 3 * 1024 * 1024 * 1024
MAX_PART = 32 * 1024 * 1024
MAX_RECORD = 4 * 1024 * 1024
HEX = re.compile(r'^[0-9a-f]{16}$')
HASH = re.compile(r'^[0-9a-f]{64}$')
START = None
COUNTS = {'records': 0, 'controllerRecords': 0, 'attemptedStages': 0,
          'successfulStages': 0, 'refusedStages': 0, 'completedSteps': 0,
          'safetyRecords': 0, 'projectionRows': 0, 'derivativeRows': 0,
          'nativeLoadRows': 0, 'sqrtComparisons': 0, 'sqrtOneUlpDifferences': 0,
          'projectionNormsReconstructedForRefusal': 0}
EXPECTED_CONFIG = {
    'schema': 'm31-boids-continuation-config-v1', 'n': 64, 'duration': 4,
    'controlDt': .01, 'timeOrigin': 1, 'maxNativeCalls': 19200,
    'maxWallSeconds': 1200, 'maxOutputBytes': MAX_INPUT, 'maxRecordBytes': MAX_RECORD,
    'cases': [
        {'caseId': 'seed2026102001-h005', 'seed': 2026102001, 'dt': .005, 'steps': 800, 'stepsPerControl': 2},
        {'caseId': 'seed2026102001-h0025', 'seed': 2026102001, 'dt': .0025, 'steps': 1600, 'stepsPerControl': 4},
        {'caseId': 'seed2026102002-h005', 'seed': 2026102002, 'dt': .005, 'steps': 800, 'stepsPerControl': 2},
        {'caseId': 'seed2026102002-h0025', 'seed': 2026102002, 'dt': .0025, 'steps': 1600, 'stepsPerControl': 4}]}
IMMUTABLE = {
    OLD + 'adapter.cjs': 'b14b81107a5c5f08db1b14e369e61baccd3bef18ef3c6d2717fd150165ab4332',
    FRESH + 'native-load.cjs': 'b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1',
    FRESH + 'vendor/generation/step02c-source/physics.cjs': '0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1',
    FRESH + 'vendor/generation/milestone-31-source/sim.cjs': '2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e',
    FRESH + 'vendor/generation/milestone-31-source/grid.cjs': 'f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302',
    FRESH + 'vendor/generation/milestone-31-source/geometry.cjs': 'e209e492fc523ab3c0c7df62745fb0d3dd7204f35e53309938a19d7895ed3d4f'}


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


def pin(path, relative=None, limit=MAX_INPUT):
    guard()
    need(path.is_file() and not path.is_symlink(), 'pin-not-regular-file')
    size = path.stat().st_size
    need(size <= limit, 'input-size-budget')
    digest = hashlib.sha256()
    count = 0
    with path.open('rb') as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            guard()
            count += len(block)
            digest.update(block)
    need(count == size == path.stat().st_size, 'file-size-changed')
    return {'file': relative or path.relative_to(BASE).as_posix(), 'bytes': size, 'sha256': digest.hexdigest()}


def read_json(relative, limit=MAX_RECORD):
    path = safe_path(BASE, relative)
    need(path.stat().st_size <= limit, 'json-size-budget:' + relative)
    guard()
    return parse(path.read_bytes())


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


def controller(body, case, step_index, current):
    eq(body.get('schema'), 'm31-coupled-controller-v1', 'controller-schema')
    eq(body.get('arm'), 'coupled', 'controller-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'controller-step')
    same_number(body.get('controlIndex'), step_index/case['stepsPerControl'], 'controller-index')
    eq(body.get('relativeTimeWord'), word(step_index*case['dt']), 'controller-time')
    eq(body.get('originalTimeWord'), word(1.0 + step_index*case['dt']), 'controller-original-time')
    rows = body.get('records')
    eq(states(rows, 'stateWords', False), current, 'controller-current-state')
    commands, directed_neighbors = [], set()
    saturated_count = 0
    for i, row in enumerate(rows):
        ids = row.get('neighborIds')
        need(isinstance(ids, list), 'neighbor-list')
        for value in ids:
            integer(value, 0, 63, 'neighbor-id')
        eq(ids, sorted(set(ids)), 'neighbor-order-or-duplicate')
        need(i not in ids, 'self-neighbor')
        directed_neighbors.update((i, j) for j in ids)
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
        saturated_count += int(row['saturated'])
        commands.append(row['commandsWords'])
    add_count('controllerRecords')
    return commands, directed_neighbors, saturated_count


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


def stage(body, case, step_index, stage_index, raw, commands):
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
    eq(body.get('originalTimeWord'), word(1.0+relative), 'stage-original-time')
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


def endpoint(body, case, step_index, current, ks):
    eq(body.get('schema'), 'm31-coupled-step-v1', 'step-schema')
    eq(body.get('stepId'), f'coupled-step{step_index}', 'step-id')
    eq(body.get('arm'), 'coupled', 'step-arm')
    integer(body.get('stepIndex'), step_index, step_index, 'step-index')
    dt = case['dt']
    t = step_index*dt+dt
    eq(body.get('relativeTimeWord'), word(t), 'step-time')
    eq(body.get('originalTimeWord'), word(1.0+t), 'step-original-time')
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


class PartReader(io.RawIOBase):
    """One forward-only virtual compressed file; never assembles the parts."""
    def __init__(self, descriptor):
        super().__init__()
        self.descriptor = descriptor
        self.part_index = 0
        self.stream = None
        self.part_bytes = 0
        self.part_hash = None
        self.total_bytes = 0
        self.total_hash = hashlib.sha256()
        self.verified = False

    def readable(self):
        return True

    def readinto(self, buffer):
        guard()
        if not buffer:
            return 0
        while self.part_index < len(self.descriptor['parts']):
            part = self.descriptor['parts'][self.part_index]
            if self.stream is None:
                self.stream = safe_path(BASE/'results', part['file']).open('rb')
                self.part_bytes = 0
                self.part_hash = hashlib.sha256()
            count = self.stream.readinto(buffer)
            if count:
                block = memoryview(buffer)[:count]
                self.part_bytes += count
                self.total_bytes += count
                need(self.part_bytes <= part['bytes'], 'part-grew-during-stream')
                need(self.total_bytes <= self.descriptor['bytes'], 'compressed-stream-overrun')
                self.part_hash.update(block)
                self.total_hash.update(block)
                return count
            self.stream.close()
            self.stream = None
            eq(self.part_bytes, part['bytes'], 'part-stream-byte-count')
            eq(self.part_hash.hexdigest(), part['sha256'], 'part-stream-hash')
            self.part_index += 1
        eq(self.total_bytes, self.descriptor['bytes'], 'aggregate-compressed-byte-count')
        eq(self.total_hash.hexdigest(), self.descriptor['sha256'], 'aggregate-compressed-hash')
        self.verified = True
        return 0

    def close(self):
        if self.stream is not None:
            self.stream.close()
            self.stream = None
        super().close()


def journal_descriptor(case, value):
    need(type(value) is dict and set(value) == {'file', 'bytes', 'sha256', 'records', 'parts', 'rawBytes', 'rawSha256'}, 'journal-descriptor-fields')
    eq(value['file'], case['caseId']+'.jsonl.gz', 'logical-journal-filename')
    integer(value['bytes'], 1, MAX_INPUT, 'logical-compressed-size')
    maximum_records = case['steps']*6 + case['steps']//case['stepsPerControl'] + 2
    integer(value['records'], 2, maximum_records, 'journal-record-bound')
    integer(value['rawBytes'], 1, value['records']*MAX_RECORD, 'raw-journal-byte-bound')
    for key in ('sha256', 'rawSha256'):
        need(isinstance(value[key], str) and HASH.fullmatch(value[key]), 'journal-hash-format')
    parts = value['parts']
    need(isinstance(parts, list) and 1 <= len(parts) <= 256, 'journal-parts-count')
    offset = 0
    for i, part in enumerate(parts):
        need(type(part) is dict and set(part) == {'file', 'bytes', 'sha256', 'offset'}, 'journal-part-fields')
        eq(part['file'], value['file']+f'.part{i:03d}', 'journal-part-name-order')
        integer(part['offset'], offset, offset, 'journal-part-contiguous-offset')
        integer(part['bytes'], 1, MAX_PART, 'journal-part-size-bound')
        need(isinstance(part['sha256'], str) and HASH.fullmatch(part['sha256']), 'part-hash-format')
        eq(safe_path(BASE/'results', part['file']).stat().st_size, part['bytes'], 'part-physical-byte-count')
        offset += part['bytes']
    eq(offset, value['bytes'], 'parts-aggregate-byte-accounting')
    return value


class Journal:
    def __init__(self, descriptor):
        self.descriptor = descriptor
        self.parts = PartReader(descriptor)
        self.compressed = io.BufferedReader(self.parts, buffer_size=1024*1024)
        self.stream = gzip.GzipFile(fileobj=self.compressed, mode='rb')
        self.sequence = 0
        self.records = descriptor['records']
        self.raw_bytes = 0
        self.raw_hash = hashlib.sha256()

    def take(self, kind):
        guard()
        line = self.stream.readline(MAX_RECORD+1)
        need(0 < len(line) <= MAX_RECORD and line.endswith(b'\n'), 'missing-or-oversize-record')
        self.raw_bytes += len(line)
        self.raw_hash.update(line)
        need(self.raw_bytes <= self.descriptor['rawBytes'], 'raw-journal-budget')
        value = parse(line)
        need(type(value) is dict and set(value) == {'sequence', 'kind', 'body'}, 'journal-envelope')
        integer(value['sequence'], self.sequence, self.sequence, 'journal-sequence')
        eq(value['kind'], kind, 'journal-record-order:' + kind)
        need(type(value['body']) is dict, 'journal-body')
        sequence = self.sequence
        self.sequence += 1
        need(self.sequence <= self.records, 'extra-journal-record')
        add_count('records')
        return value['body'], sequence

    def finish(self):
        need(self.stream.read(1) == b'', 'trailing-journal-data')
        need(self.parts.verified, 'compressed-stream-not-fully-verified')
        eq(self.raw_bytes, self.descriptor['rawBytes'], 'raw-stream-byte-count')
        eq(self.raw_hash.hexdigest(), self.descriptor['rawSha256'], 'raw-stream-hash')
        self.stream.close()
        self.compressed.close()
        eq(self.sequence, self.records, 'journal-record-count')


def frame(current, at, kind, sequence, step_index, safety_passed):
    return {'time': at, 'originalTime': 1.0+at, 'positions': [vector(row[:3], 3) for row in current], 'kind': kind,
            'sequence': sequence, 'stepIndex': step_index, 'safetyPassed': safety_passed}


def descriptive(view):
    initial, final = view['frames'][0]['positions'], view['frames'][-1]['positions']
    displacement = [[b[k]-a[k] for k in range(3)] for a, b in zip(initial, final)]
    com = [left_sum([row[k] for row in displacement])/64 for k in range(3)]
    length = lambda v: math.sqrt((v[0]*v[0]+v[1]*v[1])+v[2]*v[2])
    centered = [[row[k]-com[k] for k in range(3)] for row in displacement]
    return {'scope': 'initial to last completed endpoint; refused trial excluded',
            'lastCompletedEndpointTime': view['lastTime'],
            'maxCenterDisplacement': max(length(row) for row in displacement),
            'maxAbsoluteVerticalDisplacement': max(abs(row[2]) for row in displacement),
            'centerOfMassDisplacement': com,
            'maxComRemovedCenterDisplacement': max(length(row) for row in centered),
            'physicalValidity': False, 'causalEmergenceClaim': False}


def update_body_axis_descriptor(observations, current, at, step_index):
    for i, state in enumerate(current):
        z = rotate(vector(state[6:10], 4), [0.0, 0.0, 1.0])[2]
        need(math.isfinite(z), 'saved-body-axis-z-finite')
        old = observations['completedEndpointBodyAxisZMinimum']
        if old is None or z < old:
            observations['completedEndpointBodyAxisZMinimum'] = z
            observations['atMinimumBodyAxisZ'] = {'id': i, 'stepIndex': step_index, 'relativeTime': at}


def audit_case(case, entry, prior_case):
    eq(entry.get('caseId'), case['caseId'], 'case-index-order')
    journal = journal_descriptor(case, entry.get('journal'))
    identity = {**journal, 'file': 'results/'+journal['file'],
                'parts': [{**part, 'file': 'results/'+part['file']} for part in journal['parts']],
                'storage': 'logical gzip stream; only the ordered parts are physical files'}
    stream = Journal(journal)
    initial, sequence = stream.take('initial')
    eq(initial.get('caseId'), case['caseId'], 'initial-case-id')
    current = states(initial.get('input'))
    eq(initial['input'], prior_case['finalInput'], 'continuation-all-17-words-prior-final-input-binding')
    initial_words = [row[:] for row in current]
    view = {**case, 'timeOrigin': 1, 'frames': [frame(current, 0, 'initial', sequence, None, None)],
            'refusedFrame': None, 'refusal': None}
    commands = None
    previous_neighbors = None
    observations = {'scope': 'saved continuation controller rows and completed endpoints; no physical threshold',
                    'controllerUpdates': 0, 'vehicleCommandRecords': 0, 'saturatedVehicleCommandRecords': 0,
                    'directedNeighborSetComparisons': 0, 'directedNeighborAdditions': 0,
                    'directedNeighborRemovals': 0, 'maximumDirectedNeighborChangesAtOneUpdate': 0,
                    'initialDirectedNeighborCount': None, 'lastDirectedNeighborCount': None,
                    'completedEndpointBodyAxisZMinimum': None, 'atMinimumBodyAxisZ': None,
                    'initialBodyAxisZMinimum': min(rotate(vector(s[6:10], 4), [0.0, 0.0, 1.0])[2] for s in current),
                    'positiveAerodynamicEdgeTurnoverComputed': False}
    completed = attempted = 0
    status, reason, refusal = 'completed', None, None
    for step_index in range(case['steps']):
        guard()
        if step_index % case['stepsPerControl'] == 0:
            body, _ = stream.take('controller')
            commands, neighbors, saturated_count = controller(body, case, step_index, current)
            observations['controllerUpdates'] += 1
            observations['vehicleCommandRecords'] += 64
            observations['saturatedVehicleCommandRecords'] += saturated_count
            if previous_neighbors is None:
                observations['initialDirectedNeighborCount'] = len(neighbors)
            else:
                additions = len(neighbors-previous_neighbors)
                removals = len(previous_neighbors-neighbors)
                observations['directedNeighborSetComparisons'] += 1
                observations['directedNeighborAdditions'] += additions
                observations['directedNeighborRemovals'] += removals
                observations['maximumDirectedNeighborChangesAtOneUpdate'] = max(
                    observations['maximumDirectedNeighborChangesAtOneUpdate'], additions+removals)
            observations['lastDirectedNeighborCount'] = len(neighbors)
            previous_neighbors = neighbors
        ks = []
        base = numeric(current)
        for stage_index in range(1, 5):
            if stage_index == 1:
                raw = current
            else:
                scale = case['dt'] if stage_index == 4 else case['dt']/2
                raw = [[word(value+scale*ks[-1][i][j]) for j, value in enumerate(row)] for i, row in enumerate(base)]
            body, sequence = stream.take('stage')
            result = stage(body, case, step_index, stage_index, raw, commands)
            attempted += 1
            if result is None:
                n = body['native']
                status, reason = 'stopped', 'native-refusal'
                refusal = {'status': n['status'], 'reason': n['reason'], 'stage': n['stage'],
                           'admission': n.get('diagnostics', {}).get('admission') if n.get('diagnostics') else None,
                           'stepIndex': step_index, 'stageIndex': stage_index,
                           'relativeTimeWord': body['relativeTimeWord']}
                trial = frame(states(body['nativeInput']), num(body['relativeTimeWord']), 'refused-stage', sequence, step_index, None)
                trial.update({'stageIndex': stage_index, 'status': n['status'], 'reason': n['reason']})
                view['refusedFrame'] = trial
                break
            ks.append(result)
        if refusal is not None:
            break
        body, sequence = stream.take('step')
        current = endpoint(body, case, step_index, current, ks)
        completed += 1
        check, _ = stream.take('safety')
        passed = safety(check, step_index)
        view['frames'].append(frame(current, num(body['relativeTimeWord']), 'completed-endpoint', sequence, step_index, passed))
        update_body_axis_descriptor(observations, current, num(body['relativeTimeWord']), step_index)
        if not passed:
            status, reason = 'stopped', 'endpoint-contact-or-vehicle-limit'
            break
    terminal, _ = stream.take('case-end')
    expected = {'caseId': case['caseId'], 'completedSteps': completed, 'attemptedStages': attempted,
                'status': status, 'reason': reason, 'refusal': refusal, 'lastTime': completed*case['dt'],
                'finalInput': input_from(current)}
    eq(terminal, expected, 'case-end-state-or-outcome')
    eq({key: value for key, value in entry.items() if key != 'journal'}, expected, 'index-case-end-binding')
    stream.finish()
    view.update({key: expected[key] for key in ('completedSteps', 'attemptedStages', 'status', 'reason', 'refusal', 'lastTime')})
    view['lastOriginalTime'] = 1.0+view['lastTime']
    view['descriptiveMotion'] = descriptive(view)
    view['savedRegimeDescriptors'] = observations
    return view, initial_words, identity


def pair_summaries(cases):
    out = []
    for coarse, fine in ((cases[0], cases[1]), (cases[2], cases[3])):
        guard()
        horizon = min(coarse['completedSteps'], fine['completedSteps']//2)
        maximum, argmax, inherited_initial = 0.0, None, 0.0
        for k in range(horizon+1):
            a, b = coarse['frames'][k], fine['frames'][2*k]
            for i, (left, right) in enumerate(zip(a['positions'], b['positions'])):
                d = [left[j]-right[j] for j in range(3)]
                distance = math.sqrt((d[0]*d[0]+d[1]*d[1])+d[2]*d[2])
                if k == 0:
                    inherited_initial = max(inherited_initial, distance)
                if argmax is None or distance > maximum:
                    maximum, argmax = distance, {'coarseStep': k, 'fineStep': 2*k, 'id': i,
                                                   'coarseSavedTime': a['time'], 'fineSavedTime': b['time']}
        out.append({'seed': coarse['seed'], 'coarseCaseId': coarse['caseId'], 'fineCaseId': fine['caseId'],
                    'commonEndpointCountIncludingInitial': horizon+1, 'commonNominalHorizon': horizon*coarse['dt'],
                    'maxCommonEndpointCenterDifference': maximum, 'atMaximum': argmax,
                    'inheritedInitialMaxCenterDifference': inherited_initial,
                    'resetToCommonInitialState': False,
                    'scope': 'saved matching continuation step indices including inherited initial discrepancy; no extrapolation',
                    'convergenceClaim': False, 'physicalValidity': False})
    return out


def prior_gate(source_pins):
    """Trust the published prior audit for its closed corpus, not a rerun."""
    def prior_json(relative):
        path = safe_path(ROOT, relative)
        need(path.stat().st_size <= MAX_RECORD, 'prior-small-file-size')
        return parse(path.read_bytes())

    receipt = prior_json(PRIOR_RECEIPT)
    eq(receipt.get('commit'), PRIOR_COMMIT, 'prior-public-result-commit')
    eq(receipt.get('manifestPath'), PRIOR+'/result-manifest.json', 'prior-manifest-path')
    eq(receipt.get('manifestSha256'), PRIOR_MANIFEST_HASH, 'prior-manifest-known-hash')
    integer(receipt.get('manifestBytes'), 20563, 20563, 'prior-manifest-known-bytes')
    need(receipt.get('remoteBytesEqualLocal') is True and receipt.get('committedBytesEqualLocal') is True, 'prior-public-receipt-gate')
    manifest_pin = pin(safe_path(ROOT, PRIOR+'/result-manifest.json'), PRIOR+'/result-manifest.json', MAX_RECORD)
    eq(manifest_pin['sha256'], receipt['manifestSha256'], 'prior-public-manifest-hash-binding')
    eq(manifest_pin['bytes'], receipt['manifestBytes'], 'prior-public-manifest-byte-binding')
    manifest = prior_json(PRIOR+'/result-manifest.json')
    eq(manifest.get('schema'), 'm31-boids-admission-result-v1', 'prior-result-manifest-schema')
    files = manifest.get('files')
    need(isinstance(files, list) and len(files) == 100, 'prior-result-pin-count')
    integer(receipt.get('verifiedFilePins'), len(files), len(files), 'prior-public-verified-count')
    listed = {}
    for item in files:
        need(type(item) is dict and isinstance(item.get('path'), str) and item['path'] not in listed, 'prior-manifest-entry')
        listed[item['path']] = item
    selected = {}
    for name in PRIOR_SMALL_FILES:
        relative = PRIOR+'/'+name
        need(relative in listed and relative in source_pins, 'prior-required-file-pin')
        actual = pin(safe_path(ROOT, relative), relative, MAX_RECORD)
        expected = listed[relative]
        eq(actual['bytes'], expected.get('bytes'), 'prior-selected-byte-pin')
        eq(actual['sha256'], expected.get('sha256'), 'prior-selected-hash-pin')
        eq(actual, source_pins[relative], 'prior-selected-current-source-pin')
        selected[name] = actual
    index, report = prior_json(PRIOR+'/results/index.json'), prior_json(PRIOR+'/audit/audit.json')
    eq(index.get('schema'), 'm31-boids-admission-index-v1', 'prior-index-schema')
    need(index.get('complete') is True and 'failure' not in index, 'prior-incomplete-producer')
    eq(report.get('schema'), 'm31-boids-admission-audit-v1', 'prior-audit-schema')
    need(report.get('passed') is True and report.get('evidenceIntegrityPassed') is True
         and report.get('allPrescribedPathsCompleted') is True, 'prior-passing-completed-audit')
    for report_key, name in (('indexPin', 'results/index.json'), ('producerExitPin', 'results/exit.json'),
                             ('nativeSupervisorPin', 'native-supervisor.json')):
        actual = selected[name]
        eq(report.get(report_key), {'file': name, 'bytes': actual['bytes'], 'sha256': actual['sha256']}, 'prior-audit-file-binding')
    for name, limit in (('results/exit.json', 360), ('audit/exit.json', 180)):
        closure = prior_json(PRIOR+'/'+name)
        need(closure.get('closed') is True and closure.get('exitCode') == 0, 'prior-internal-closure')
        need(type(closure.get('wallSeconds')) in (int, float) and 0 <= closure['wallSeconds'] <= limit, 'prior-internal-allocation-wall')
    for name, limit in (('native-supervisor.json', 360), ('audit-supervisor.json', 180)):
        closure = prior_json(PRIOR+'/'+name)
        need(closure.get('returncode') == 0 and 'timeout' not in closure and closure.get('allocationWallPassed') is True, 'prior-external-closure')
        need(type(closure.get('wallSeconds')) in (int, float) and 0 <= closure['wallSeconds'] <= limit, 'prior-allocation-wall')
    closure = prior_json(PRIOR+'/ALLOCATION-CLOSURE.json')
    eq(closure.get('schema'), 'm31-boids-allocation-closure-v1', 'prior-allocation-closure-schema')
    for phase in ('native', 'audit', 'display', 'archive'):
        need(type(closure.get(phase)) is dict, 'prior-allocation-phase')
        eq(closure[phase].get('status'), 'closed-passed', 'prior-allocation-phase-status')
        integer(closure[phase].get('attempts'), 1, 1, 'prior-allocation-phase-attempts')
    need(isinstance(index.get('cases'), list) and len(index['cases']) == 4, 'prior-four-cases')
    need(isinstance(index.get('config', {}).get('cases'), list) and len(index['config']['cases']) == 4, 'prior-case-configs')
    for case, prior_case, prior_config in zip(EXPECTED_CONFIG['cases'], index['cases'], index['config']['cases']):
        eq(prior_case.get('caseId'), case['caseId'], 'prior-case-order')
        eq(prior_config.get('caseId'), case['caseId'], 'prior-config-case-order')
        eq(prior_config.get('seed'), case['seed'], 'prior-seed-binding')
        eq(prior_config.get('dt'), case['dt'], 'prior-dt-binding')
        eq(prior_case.get('status'), 'completed', 'prior-case-must-complete')
        eq(prior_case.get('reason'), None, 'prior-case-reason')
        eq(prior_case.get('refusal'), None, 'prior-case-refusal')
        same_number(prior_case.get('lastTime'), 1, 'prior-origin-time')
        integer(prior_case.get('completedSteps'), case['steps']//4, case['steps']//4, 'prior-completed-steps')
        states(prior_case.get('finalInput'))
    evidence = {'resultCommit': PRIOR_COMMIT, 'receiptPin': source_pins[PRIOR_RECEIPT],
                'manifestPin': manifest_pin, 'selectedPriorPins': list(selected.values()),
                'scope': 'published prior index/audit/closure small-file binding; prior journals are not reread',
                'originalTimeOrigin': 1, 'resetToCommonInitialState': False}
    return index, evidence


def source_gate():
    manifest_path = safe_path(BASE, 'source-manifest.json')
    manifest_pin = pin(manifest_path, limit=MAX_RECORD)
    manifest = parse(manifest_path.read_bytes())
    publication = read_json('source-publication.json')
    eq(publication.get('manifestSha256'), manifest_pin['sha256'], 'public-manifest-hash')
    need(publication.get('remoteBytesEqualLocal') is True and publication.get('committedBytesEqualLocal') is True, 'public-byte-verification-gate')
    need(isinstance(publication.get('commit'), str) and re.fullmatch(r'[0-9a-f]{40}', publication['commit']), 'public-commit')
    files = manifest.get('files')
    need(isinstance(files, list) and 1 <= len(files) <= 512, 'manifest-file-list')
    integer(publication.get('verifiedFilePins'), len(files), len(files), 'public-verified-file-count')
    pinned = {}
    for item in files:
        need(type(item) is dict and isinstance(item.get('path'), str), 'manifest-entry')
        path = item['path']
        need(path not in pinned, 'duplicate-manifest-path')
        need(isinstance(item.get('sha256'), str) and HASH.fullmatch(item['sha256']), 'manifest-hash-format')
        identity = pin(safe_path(ROOT, path), path)
        eq(identity['bytes'], item.get('bytes'), 'manifest-byte-pin:' + path)
        eq(identity['sha256'], item['sha256'], 'manifest-hash-pin:' + path)
        pinned[path] = identity
    mandatory = {REL+'/'+x for x in ('config.json', 'runtime.json', 'PROTOCOL.md', 'AUDIT-CONTRACT.md',
                                    'source/run.cjs', 'source/journal.cjs', 'source/motion.cjs', 'source/audit.py', 'source/supervise.py')}
    mandatory.update(IMMUTABLE)
    mandatory.update({PRIOR_RECEIPT, PRIOR+'/result-manifest.json'})
    mandatory.update(PRIOR+'/'+name for name in PRIOR_SMALL_FILES)
    mandatory.update({REL+'/source/storage-test.cjs', REL+'/source/storage-check.py'})
    mandatory.update({REL+'/'+name for name in ('source/finalize-view.py', 'source/ui.cjs', 'viewer/app.js', 'viewer/index.html')})
    need(mandatory <= set(pinned), 'manifest-mandatory-source-closure')
    for path, digest in IMMUTABLE.items():
        eq(pinned[path]['sha256'], digest, 'immutable-inherited-source:' + path)
    # Static dependency closure only: read text, never load a JavaScript module.
    queue, visited = [REL+'/source/run.cjs', REL+'/source/motion.cjs'], set()
    while queue:
        path = queue.pop()
        if path in visited:
            continue
        visited.add(path)
        need(path in pinned, 'dependency-not-pinned:' + path)
        text = safe_path(ROOT, path).read_text()
        for dependency in re.findall(r"require\(['\"]([^'\"]+)['\"]\)", text):
            if dependency.startswith('node:'):
                continue
            need(dependency.startswith('.'), 'unpinned-package-dependency:' + dependency)
            target = (ROOT/path).parent.joinpath(dependency).resolve()
            need(target.is_relative_to(ROOT), 'dependency-outside-repository')
            queue.append(target.relative_to(ROOT).as_posix())
    runtime = read_json('runtime.json')
    eq(runtime, {'nodeSha256': 'd0c6c74401e6a544bb4d4b2a9ded9c43298d4e6dcd5ebac4dd010c4c81774105', 'nodeBytes': 121304480}, 'runtime-pin')
    return publication, manifest_pin, pinned, sorted(visited)


def audit():
    publication, manifest_pin, source_pins, closure = source_gate()
    prior_index, prior_evidence = prior_gate(source_pins)
    gate_pins = [pin(safe_path(BASE, name)) for name in
                 ('source-manifest.json', 'source-publication.json', 'native-supervisor.json',
                  'results/launch.json', 'results/exit.json', 'storage-supervisor.json', 'storage/qualification.json')]
    config = read_json('config.json')
    eq(config, EXPECTED_CONFIG, 'prospective-config')
    qualification, storage_supervisor = read_json('storage/qualification.json'), read_json('storage-supervisor.json')
    need(qualification.get('passed') is True and qualification.get('closed') is True
         and isinstance(qualification.get('checks'), list) and len(qualification['checks']) > 0, 'storage-qualification-gate')
    need(storage_supervisor.get('returncode') == 0 and 'timeout' not in storage_supervisor
         and storage_supervisor.get('allocationWallPassed') is True
         and storage_supervisor.get('outputCapPassed') is True, 'storage-external-closure')
    integer(storage_supervisor.get('outputBytes'), 1, 8*1024*1024, 'storage-output-cap')
    need(type(storage_supervisor.get('wallSeconds')) in (int, float)
         and 0 <= storage_supervisor['wallSeconds'] <= 20, 'storage-allocation-wall')
    supervisor = read_json('native-supervisor.json')
    need(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True, 'native-external-closure')
    need(type(supervisor.get('wallSeconds')) in (int, float) and 0 <= supervisor['wallSeconds'] <= 1200, 'native-allocation-wall-budget')
    exit_record, launch, index = read_json('results/exit.json'), read_json('results/launch.json'), read_json('results/index.json')
    need(exit_record.get('exitCode') == 0 and exit_record.get('closed') is True, 'native-internal-closure')
    eq(index.get('schema'), 'm31-boids-continuation-index-v1', 'index-schema')
    need(index.get('complete') is True and 'failure' not in index, 'incomplete-producer-allocation')
    eq(index.get('config'), config, 'index-config-binding')
    eq(index.get('sourceCommit'), publication['commit'], 'index-public-source-binding')
    eq(launch.get('sourceCommit'), publication['commit'], 'launch-public-source-binding')
    for value in (index.get('wallSeconds'), exit_record.get('wallSeconds')):
        need(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1200, 'native-internal-wall-budget')
    eq(index.get('nativeTimingIsNotBenchmark'), True, 'native-timing-scope')
    need(isinstance(index.get('cases'), list) and len(index['cases']) == 4, 'all-prescribed-cases-required')
    expected_files = {'launch.json', 'index.json', 'exit.json'}
    for case, entry in zip(config['cases'], index['cases']):
        descriptor = journal_descriptor(case, entry.get('journal'))
        expected_files.update(part['file'] for part in descriptor['parts'])
    actual_files = {p.name for p in (BASE/'results').iterdir()}
    eq(actual_files, expected_files, 'unexpected-or-missing-result-file')
    total_output_bytes = sum(safe_path(BASE/'results', name).stat().st_size for name in actual_files)
    need(total_output_bytes <= MAX_INPUT, 'producer-output-cap')
    integer(supervisor.get('outputBytes'), total_output_bytes, total_output_bytes, 'native-supervisor-output-byte-binding')
    views, initial_by_case, journals = [], {}, []
    for case, entry, prior_case in zip(config['cases'], index['cases'], prior_index['cases']):
        view, initial, journal = audit_case(case, entry, prior_case)
        initial_by_case[case['caseId']] = initial
        views.append(view)
        journals.append(journal)
    for seed in (2026102001, 2026102002):
        need(initial_by_case[f'seed{seed}-h005'] != initial_by_case[f'seed{seed}-h0025'], 'inherited-coarse-fine-initial-difference')
    integer(index.get('totalNativeCalls'), COUNTS['attemptedStages'], COUNTS['attemptedStages'], 'total-native-call-binding')
    integer(index.get('totalStages'), COUNTS['attemptedStages'], COUNTS['attemptedStages'], 'total-stage-binding')
    need(COUNTS['attemptedStages'] <= 19200, 'native-call-budget')
    need(COUNTS['controllerRecords'] <= 1600, 'controller-update-budget')
    before_index = safe_path(BASE, 'results/launch.json').stat().st_size + sum(x['bytes'] for x in journals)
    integer(index.get('outputBytesBeforeIndex'), before_index, before_index, 'producer-output-byte-accounting')
    index_pin = pin(safe_path(BASE, 'results/index.json'))
    pairwise = pair_summaries(views)
    for path, expected in source_pins.items():
        eq(pin(safe_path(ROOT, path), path), expected, 'source-changed-during-audit')
    for expected in journals:
        for part in expected['parts']:
            identity = {'file': part['file'], 'bytes': part['bytes'], 'sha256': part['sha256']}
            eq(pin(safe_path(BASE, part['file']), limit=MAX_PART), identity, 'part-changed-during-audit')
    for expected in gate_pins:
        eq(pin(safe_path(BASE, expected['file'])), expected, 'closure-gate-changed-during-audit')
    eq(pin(safe_path(BASE, 'results/index.json')), index_pin, 'index-changed-during-audit')
    counts = {**COUNTS, 'prescribedCases': 4, 'completedCases': sum(c['status'] == 'completed' for c in views),
              'stoppedCases': sum(c['status'] == 'stopped' for c in views),
              'unsafeCompletedEndpoints': sum(f['safetyPassed'] is False for c in views for f in c['frames'])}
    viewer = {'schema': 'm31-boids-continuation-view-v1', 'sourceCommit': publication['commit'],
              'sourceManifestSha256': manifest_pin['sha256'], 'indexPin': index_pin,
              'timeOrigin': 1, 'timeLabel': 'seconds since continuation; starts prior t=1',
              'priorContinuation': prior_evidence,
              'physicalValidity': False, 'scope': 'saved computational trajectory; no endpoint native query',
              'cases': views, 'counts': counts, 'sameSeedComparisons': pairwise}
    report = {'schema': 'm31-boids-continuation-audit-v1', 'passed': True, 'evidenceIntegrityPassed': True,
              'sourceCommit': publication['commit'], 'sourceManifestSha256': manifest_pin['sha256'],
              'priorContinuation': prior_evidence,
              'sourcePublicationPin': pin(safe_path(BASE, 'source-publication.json')),
              'nativeSupervisorPin': pin(safe_path(BASE, 'native-supervisor.json')),
              'producerExitPin': pin(safe_path(BASE, 'results/exit.json')),
              'storageQualificationPin': pin(safe_path(BASE, 'storage/qualification.json')),
              'storageSupervisorPin': pin(safe_path(BASE, 'storage-supervisor.json')),
              'indexPin': index_pin, 'journalPins': journals, 'staticDependencyClosure': closure,
              'counts': counts, 'allPrescribedPathsCompleted': counts['completedCases'] == 4,
              'allAttemptedNativeStagesAdmitted': counts['refusedStages'] == 0,
              'physicalValidity': False, 'exactRationalProof': False, 'nativeModelAccuracyValidated': False,
              'arithmeticScope': 'binary64 consistency of saved bindings, preparation, loads, derivatives and projected RK arithmetic',
              'sqrtPolicy': 'saved sqrt within one ULP of Python math.sqrt; recorded value used downstream; refusal projection tests the three permitted sqrt candidates',
              'notRegenerated': ['initializer', 'neighbor membership', 'Boids steering', 'controller numerical law',
                                 'native geometry coefficient model', 'native root solve', 'residual model', 'obstacle/contact geometry'],
              'caseOutcomes': [{k: c[k] for k in ('caseId', 'status', 'reason', 'lastTime', 'lastOriginalTime', 'completedSteps', 'attemptedStages', 'refusal', 'descriptiveMotion', 'savedRegimeDescriptors')} for c in views],
              'sameSeedComparisons': pairwise}
    return report, viewer


def main():
    global START
    START = time.monotonic()
    need((BASE/'audit-supervisor-launch.lock').is_file(), 'external-audit-allocation-required')
    output = BASE/'audit'
    need(not output.is_symlink(), 'audit-output-symlink')
    output.mkdir()  # Exclusive allocation: existing output refuses every retry.
    launch = {'schema': 'm31-boids-continuation-audit-launch-v1', 'startedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'maxWallSeconds': MAX_SECONDS, 'maxOutputBytes': MAX_OUTPUT, 'python': sys.version,
              'scope': 'saved evidence only; no producer or scientific module execution'}
    launch_bytes = json_bytes(launch)
    with (output/'launch.json').open('xb') as stream:
        stream.write(launch_bytes)
    try:
        report, viewer = audit()
        guard()
        viewer_bytes = json_bytes(viewer)
        report['viewerPin'] = {'file': 'audit/viewer-data.json', 'bytes': len(viewer_bytes), 'sha256': hashlib.sha256(viewer_bytes).hexdigest()}
        report['wallSeconds'] = time.monotonic()-START
        report_bytes = json_bytes(report)
        need(len(launch_bytes)+len(viewer_bytes)+len(report_bytes)+4096 <= MAX_OUTPUT, 'audit-output-budget')
        with (output/'viewer-data.json').open('xb') as stream:
            stream.write(viewer_bytes)
        guard()
        with (output/'audit.json').open('xb') as stream:
            stream.write(report_bytes)
        guard()
        exit_code = 0
    except Exception as error:
        exit_code = 1
        failure = {'schema': 'm31-boids-continuation-audit-v1', 'passed': False, 'evidenceIntegrityPassed': False,
                   'failure': type(error).__name__+': '+str(error).replace(str(ROOT), '[repository]')[:2000],
                   'countsAtFailure': COUNTS, 'wallSeconds': time.monotonic()-START,
                   'physicalValidity': False, 'singleAllocationClosed': True}
        # A viewer written before a late persistence failure is unusable without
        # passed audit, exit 0 and the external supervisor's independent closure.
        path = output/'audit.json'
        if not path.exists():
            with path.open('xb') as stream:
                stream.write(json_bytes(failure))
        else:
            with (output/'failure.json').open('xb') as stream:
                stream.write(json_bytes(failure))
    with (output/'exit.json').open('xb') as stream:
        stream.write(json_bytes({'closed': True, 'exitCode': exit_code, 'wallSeconds': time.monotonic()-START}))
    print(json.dumps({'passed': exit_code == 0, 'wallSeconds': time.monotonic()-START}))
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
