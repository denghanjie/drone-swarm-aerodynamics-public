#!/usr/bin/env python3
"""Independent saved-word audit. Source draft: do not run before source review.

No producer/scientific imports. Exact Fraction arithmetic audits delivered native
load words against already checked and pinned exact reference boxes. It does not
recompute coefficients, roots, trajectories or prior experiments.
"""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
from fractions import Fraction

PACKAGE = 'research/m31-native-load-baseline-2026-10-17'
CASES = ('run-a-t0', 'run-a-t5', 'run-a-t10',
         'run-b-t0', 'run-b-t5', 'run-b-t10')
METHOD_ORDER = (('F', 'L'), ('L', 'F'), ('F', 'L'),
                ('L', 'F'), ('F', 'L'), ('L', 'F'))
SCHEDULE = tuple((c, m) for c, methods in zip(CASES, METHOD_ORDER) for m in methods)
CONSTANT_KEYS = ('mg', 'arm', 'radius', 'rho', 'A', 'R', 'D', 'decay',
                 'spread', 'origin', 'minDown', 'neighbor', 'nearRad',
                 'downFade', 'downCut', 'radFade', 'radCut', 'induced', 'kappa')
PREP_KEYS = ('center', 'axis', 'offsets', 'points', 'forces')
CATEGORIES = ('rotor', 'collective', 'worldForce', 'worldMoment')
FAILURE_STATUSES = ('input-refused', 'domain-refused', 'numerical-failure',
                    'resource-failure', 'internal-failure')
TAU = Fraction(1, 100_000_000)
MAX_JSON = 32 * 1024 * 1024
HEX = re.compile(r'^[0-9a-f]{16}$')
SHA = re.compile(r'^[0-9a-f]{64}$')
INT = re.compile(r'^-?(0|[1-9][0-9]*)$')


class InvalidRecord(Exception):
    pass


def require(condition, code):
    if not condition:
        raise InvalidRecord(code)


def fields(value, names, code):
    require(isinstance(value, dict) and set(value) == set(names), code)


def integer(value, low, high, code):
    require(type(value) is int and low <= value <= high, code)
    return value


def vector(value, length, code):
    require(isinstance(value, list) and len(value) == length, code)
    return value


def dyadic(word):
    require(isinstance(word, str) and HEX.fullmatch(word), 'binary64-word')
    bits = int(word, 16)
    exponent, mantissa = (bits >> 52) & 2047, bits & ((1 << 52) - 1)
    require(exponent != 2047, 'nonfinite-success-word')
    if exponent:
        mantissa |= 1 << 52
        shift = exponent - 1023 - 52
    else:
        shift = -1074
    result = Fraction(mantissa << shift, 1) if shift >= 0 else Fraction(mantissa, 1 << -shift)
    return -result if bits >> 63 else result


def rat(value):
    fields(value, ('n', 'd'), 'rational-fields')
    for name in ('n', 'd'):
        require(isinstance(value[name], str) and len(value[name]) <= 4096
                and INT.fullmatch(value[name]), 'rational-integer')
    numerator, denominator = int(value['n']), int(value['d'])
    require(denominator > 0, 'rational-denominator')
    return Fraction(numerator, denominator)


def interval(value):
    fields(value, ('l', 'u'), 'interval-fields')
    lo, hi = rat(value['l']), rat(value['u'])
    require(lo <= hi, 'interval-order')
    return lo, hi


def encoded(value):
    return {'n': str(value.numerator), 'd': str(value.denominator)}


def encoded_interval(lo, hi):
    return {'l': encoded(lo), 'u': encoded(hi)}


def round_integer(numerator, denominator):
    q, r = divmod(numerator, denominator)
    return q + (2 * r > denominator or (2 * r == denominator and q % 2 == 1))


def rounded_word(value):
    """Exact round-to-nearest, ties-to-even; used for delivered-load consistency.

    A zero result is positive zero. Comparisons below deliberately identify both
    zero signs numerically; raw/prepared word identity remains bit-for-bit.
    """
    value = Fraction(value)
    sign = int(value < 0)
    value = abs(value)
    if not value:
        return '0000000000000000'
    n, d = value.numerator, value.denominator
    exponent = n.bit_length() - d.bit_length()
    if exponent >= 0:
        if n < d << exponent:
            exponent -= 1
    elif n << -exponent < d:
        exponent -= 1
    if exponent < -1022:
        significand = round_integer(n << 1074, d)
        bits = significand  # Includes a rounded transition to minimum normal.
    else:
        shift = 52 - exponent
        significand = (round_integer(n << shift, d) if shift >= 0
                       else round_integer(n, d << -shift))
        if significand == 1 << 53:
            significand >>= 1
            exponent += 1
        require(exponent <= 1023, 'native-load-arithmetic-overflow')
        bits = ((exponent + 1023) << 52) | (significand - (1 << 52))
    return f'{bits | (sign << 63):016x}'


def rnd(value):
    return dyadic(rounded_word(value))


def left_sum(values):
    total = Fraction(0)
    for value in values:
        total = rnd(total + value)
    return total


def native_cross(a, b):
    return [rnd(rnd(a[1] * b[2]) - rnd(a[2] * b[1])),
            rnd(rnd(a[2] * b[0]) - rnd(a[0] * b[2])),
            rnd(rnd(a[0] * b[1]) - rnd(a[1] * b[0]))]


def native_loads(prepared, rotor):
    axis = [dyadic(x) for x in prepared['axis']]
    offsets = [[dyadic(x) for x in row] for row in prepared['offsets']]
    collective = left_sum(rotor)
    force = [rnd(x * collective) for x in axis]
    crosses = [native_cross(offset, axis) for offset in offsets]
    moment = [left_sum(rnd(crosses[r][k] * rotor[r]) for r in range(4)) for k in range(3)]
    return {'rotor': rotor, 'collective': collective,
            'worldForce': force, 'worldMoment': moment}


def scalar_error(value, box):
    lo, hi = box
    lower = lo - value if value < lo else value - hi if value > hi else Fraction(0)
    return lower, max(abs(value - lo), abs(value - hi))


def squared_error(values, boxes, normalizer):
    require(normalizer > 0 and len(values) == len(boxes), 'error-shape-normalizer')
    distances = [scalar_error(value, box) for value, box in zip(values, boxes)]
    return (sum(d[0] ** 2 for d in distances) / normalizer ** 2,
            sum(d[1] ** 2 for d in distances) / normalizer ** 2)


def verdict(bounds):
    lo, hi = bounds
    return 'pass' if hi <= TAU ** 2 else 'fail' if lo > TAU ** 2 else 'unresolved'


def sqrt_bounds(value, bits=192):
    require(value >= 0, 'sqrt-negative')
    scale = 1 << bits
    q = math.isqrt((value.numerator << (2 * bits)) // value.denominator)
    lower = Fraction(q, scale)
    return lower, lower if lower ** 2 == value else Fraction(q + 1, scale)


def error_record(bounds, witness):
    lo, hi = bounds
    return {'normalizedError': encoded_interval(sqrt_bounds(lo)[0], sqrt_bounds(hi)[1]),
            'normalizedSquaredError': encoded_interval(lo, hi),
            'decision': verdict(bounds), 'upperWitness': witness}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def parse_json(data):
    require(len(data) <= MAX_JSON, 'json-byte-cap')
    return json.loads(data, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(InvalidRecord('json-nonfinite')))


def read_pin(root, pin):
    fields(pin, ('path', 'bytes', 'sha256'), 'pin-fields')
    require(isinstance(pin['path'], str) and not Path(pin['path']).is_absolute(), 'pin-relative-path')
    path = (root / pin['path']).resolve()
    require(path.is_relative_to(root), 'pin-outside-root')
    integer(pin['bytes'], 0, 2 ** 31, 'pin-size')
    require(isinstance(pin['sha256'], str) and SHA.fullmatch(pin['sha256']), 'pin-sha')
    require(path.is_file() and path.stat().st_size == pin['bytes'], 'pin-size-mismatch:' + pin['path'])
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == pin['sha256'], 'pin-hash-mismatch:' + pin['path'])
    return data


def canonical(value):
    def validate(x):
        if x is None or type(x) is bool:
            return
        if type(x) is int:
            require(abs(x) <= 2 ** 53 - 1, 'canonical-safe-integer')
        elif isinstance(x, str):
            require(all(32 <= ord(c) <= 126 for c in x), 'canonical-ascii')
        elif isinstance(x, list):
            for item in x:
                validate(item)
        elif isinstance(x, dict):
            for key, item in x.items():
                validate(key)
                validate(item)
        else:
            raise InvalidRecord('canonical-json-type')
    validate(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def raw_input(value):
    fields(value, ('drones',), 'raw-input-fields')
    drones = vector(value['drones'], 64, 'retained-drone-count')
    ids = []
    for row in drones:
        fields(row, ('id', 'state'), 'raw-drone-fields')
        ids.append(integer(row['id'], 0, 2 ** 31 - 1, 'stable-id'))
        for word in vector(row['state'], 17, 'raw-state-width'):
            dyadic(word)
        require(all(dyadic(x) > 0 for x in row['state'][13:17]), 'raw-force-positive')
    require(ids == sorted(set(ids)), 'raw-id-order-uniqueness')
    return ids


def reference_target(case_id, raw, reference, constants, digest):
    ids = raw_input(raw)
    require(reference['id'] == case_id and reference['inputSha256'] == digest, 'reference-input-identity')
    require(reference['referenceStatus'] == 'admitted' and reference['branch'] == 'loads', 'saved-reference-admission')
    require(reference['graph']['status'] == 'acyclic-compatible', 'saved-reference-graph')
    prepared = vector(reference['prepared'], 64, 'reference-prepared-count')
    require([x['id'] for x in prepared] == ids, 'reference-prepared-ids')
    prepared_map = {}
    for row in prepared:
        require(row['rejection'] is None, 'reference-prepared-rejection')
        value = row['value']
        fields(value, PREP_KEYS, 'reference-prepared-fields')
        for name, size in (('center', 3), ('axis', 3), ('forces', 4)):
            for word in vector(value[name], size, 'reference-prepared-width'):
                dyadic(word)
        for name in ('offsets', 'points'):
            for xyz in vector(value[name], 4, 'reference-four-rotors'):
                for word in vector(xyz, 3, 'reference-three-coordinates'):
                    dyadic(word)
        prepared_map[row['id']] = value
    pairs, positive = reference['pairs'], {}
    require(len(pairs) == 4 * 64 * 63, 'reference-pair-count')
    seen = set()
    for row in pairs:
        key = (row['i'], row['r'], row['j'])
        require(row['i'] in ids and row['j'] in ids and row['i'] != row['j']
                and type(row['r']) is int and 0 <= row['r'] < 4 and key not in seen, 'reference-pair-coverage')
        seen.add(key)
        require(row['status'] in ('positive', 'zero'), 'reference-pair-status')
        if row['status'] == 'positive':
            box = interval(row['coefficient'])
            require(box[0] > 0, 'reference-positive-coefficient')
            positive[key] = box
    require(len(positive) == reference['graph']['positiveRotorPairs'], 'reference-positive-count')
    loads = vector(reference['loads'], 64, 'reference-load-count')
    require([row['id'] for row in loads] == ids, 'reference-load-ids')
    load_map = {}
    for row in loads:
        fields(row['loads'], ('rotor', 'collective', 'force', 'moment'), 'reference-load-fields')
        load_map[row['id']] = {
            'rotor': [interval(x) for x in vector(row['loads']['rotor'], 4, 'reference-rotor-width')],
            'collective': interval(row['loads']['collective']),
            'worldForce': [interval(x) for x in vector(row['loads']['force'], 3, 'reference-force-width')],
            'worldMoment': [interval(x) for x in vector(row['loads']['moment'], 3, 'reference-moment-width')]}
    require(all(key in constants for key in CONSTANT_KEYS), 'reference-constant-keys')
    for key in CONSTANT_KEYS:
        dyadic(constants[key])
    require(constants['mg'] == '3fd0f3a14cec41dd' and constants['R'] == '3fa4462fb7ff5035', 'normalization-words')
    return {'id': case_id, 'ids': ids, 'raw': raw['drones'], 'digest': digest,
            'prepared': prepared_map, 'loads': load_map, 'positive': positive,
            'constants': {key: constants[key] for key in CONSTANT_KEYS}}


def consumption_check(loads, recorded):
    words, value = 0, 2166136261
    status = 'native-success'
    for character in status:
        value = ((value ^ ord(character)) * 16777619) & 0xffffffff
    for load in loads:
        for word in [rounded_word(Fraction(load['id']))] + load['rotor'] + [load['collective']] + load['worldForce'] + load['worldMoment']:
            dyadic(word)
            for half in (word[:8], word[8:]):
                value = ((value ^ int(half, 16)) * 16777619) & 0xffffffff
            words += 1
    return recorded == {'kind': 'native-load-id-status-fnv32', 'status': status,
                        'loadWords': words - len(loads), 'identityWords': len(loads),
                        'statusCharacters': len(status), 'value': value}


def audit_evidence(evidence, target, method):
    require(evidence['schema'] == 'm31-native-load-evidence-v1', 'native-evidence-schema')
    require(evidence['caseId'] == target['id'] and evidence['method'] == method, 'native-call-identity')
    require(evidence['semanticInputSha256'] == target['digest']
            and evidence['inputFileSha256'] == target['inputFileSha256'], 'native-input-digest')
    require(evidence['model'] == 'ordinary-binary64-full-contribution', 'native-model-name')
    require(evidence['status'] in ('native-success',) + FAILURE_STATUSES, 'native-status')
    result = {'caseId': target['id'], 'method': method, 'nativeStatus': evidence['status'],
              'referenceStatus': 'admitted', 'decision': 'unqualified', 'qualified': False}
    if evidence['status'] != 'native-success':
        require(isinstance(evidence.get('reason'), str) and evidence['reason'], 'native-failure-reason')
        result['reason'] = evidence['reason']
        result['statusDisagreement'] = True
        return result
    require(evidence['reason'] is None, 'native-success-reason')
    diagnostics = evidence['diagnostics']
    require(diagnostics['admission']['admitted'] is True
            and diagnostics['admission']['reasons'] == []
            and diagnostics['graph']['descendingEligible'] is True, 'native-success-admission-diagnostics')
    for name in ('finite', 'geometryValid', 'nominalPositive', 'nominalTotalFinite'):
        require(diagnostics['input'][name] is True, 'native-success-input-diagnostics')
    for name, limit in (('residualLog', 1e-9), ('sourceReceiverMismatch', 2e-9)):
        value = diagnostics[name]
        require(type(value) in (int, float) and math.isfinite(value) and 0 <= value <= limit,
                'native-success-residual-engineering-guard')
    ids = target['ids']
    require(evidence['ids'] == ids, 'native-id-order')
    require(isinstance(evidence['raw'], list), 'native-raw-array')
    identity = {'raw': evidence['raw'] == target['raw'],
                'constants': evidence['constants'] == target['constants'], 'prepared': True}
    prepared = vector(evidence['prepared'], 64, 'native-prepared-count')
    require([x['id'] for x in prepared] == ids, 'native-prepared-ids')
    for row in prepared:
        identity['prepared'] &= {k: row[k] for k in PREP_KEYS} == target['prepared'][row['id']]
        for key in ('nativeTotal', 'nativeBeta'):
            require(dyadic(row[key]) > 0, 'native-positive-normalizer')
        for word in vector(row['nativeNu'], 4, 'native-nu-width'):
            require(dyadic(word) > 0, 'native-positive-nu')
        expected_total = left_sum(dyadic(x) for x in row['forces'])
        require(dyadic(row['nativeTotal']) == expected_total, 'native-total-arithmetic')
    csr = evidence['coefficients']
    fields(csr, ('offsets', 'sourceIndices', 'K', 'a'), 'csr-fields')
    offsets = vector(csr['offsets'], 257, 'csr-offset-count')
    count = len(csr['sourceIndices'])
    require(count <= 2_000_000 and offsets[0] == 0 and offsets[-1] == count, 'csr-positive-budget')
    require(len(csr['K']) == len(csr['a']) == count, 'csr-term-array-counts')
    native_positive, coefficient_errors = set(), []
    for row_index in range(256):
        start = integer(offsets[row_index], 0, count, 'csr-offset')
        stop = integer(offsets[row_index + 1], start, count, 'csr-monotonic-offset')
        last = -1
        i, rotor = divmod(row_index, 4)
        for offset in range(start, stop):
            source = integer(csr['sourceIndices'][offset], 0, 63, 'csr-source-index')
            require(source > last and source != i, 'csr-source-order-self')
            last = source
            key = (ids[i], rotor, ids[source])
            k, a = dyadic(csr['K'][offset]), dyadic(csr['a'][offset])
            require(0 < k <= 128 and a > 0, 'native-positive-coefficient-range')
            require(rnd(k * dyadic(prepared[source]['nativeBeta'])) <= 128, 'native-scaled-cap-range')
            native_positive.add(key)
            if key in target['positive']:
                coefficient_errors.append(scalar_error(a, target['positive'][key]))
    missing, extra = sorted(set(target['positive']) - native_positive), sorted(native_positive - set(target['positive']))
    require(diagnostics['geometryWork']['positiveRotorTerms'] == count, 'native-positive-work-count')
    support = {'matches': not missing and not extra, 'exactPositiveCount': len(target['positive']),
               'nativePositiveCount': count, 'missingCount': len(missing), 'extraCount': len(extra),
               'missingWitnesses': missing[:4], 'extraWitnesses': extra[:4]}
    if coefficient_errors:
        support['coefficientAbsoluteError'] = encoded_interval(max(x[0] for x in coefficient_errors),
                                                              max(x[1] for x in coefficient_errors))
        support['coefficientErrorIsDiagnosticOnly'] = True
    solutions = vector(evidence['solution'], 64, 'native-solution-count')
    delivered = vector(evidence['loads'], 64, 'native-load-count')
    require([x['id'] for x in solutions] == ids and [x['id'] for x in delivered] == ids, 'native-load-solution-ids')
    consumption_matches = consumption_check(delivered, evidence['consumption'])
    mg, radius = dyadic(target['constants']['mg']), dyadic(target['constants']['R'])
    maxima = {category: (Fraction(0), Fraction(0)) for category in CATEGORIES}
    witnesses = {category: None for category in CATEGORIES}
    arithmetic_failures = []
    for p, solution, load in zip(prepared, solutions, delivered):
        require(0 < dyadic(solution['y']) <= 1, 'native-source-y-range')
        rotors = vector(solution['rotors'], 4, 'native-solution-rotors')
        actual = {'rotor': [dyadic(x) for x in vector(load['rotor'], 4, 'native-rotor-loads')],
                  'collective': dyadic(load['collective']),
                  'worldForce': [dyadic(x) for x in vector(load['worldForce'], 3, 'native-world-force')],
                  'worldMoment': [dyadic(x) for x in vector(load['worldMoment'], 3, 'native-world-moment')]}
        expected_rotor = []
        for r, rotor in enumerate(rotors):
            require(dyadic(rotor['alpha']) >= 0 and 0 < dyadic(rotor['x']) <= 1, 'native-solution-range')
            expected_rotor.append(rnd(dyadic(p['forces'][r]) * dyadic(rotor['x'])))
            if dyadic(rotor['T']) != actual['rotor'][r]:
                arithmetic_failures.append({'id': p['id'], 'category': 'solution-T-versus-delivered', 'rotor': r})
        expected = native_loads(p, expected_rotor)
        for category in CATEGORIES:
            if actual[category] != expected[category]:
                arithmetic_failures.append({'id': p['id'], 'category': category})
        ref = target['loads'][p['id']]
        tests = [('rotor', r, squared_error([actual['rotor'][r]], [ref['rotor'][r]], mg / 4)) for r in range(4)]
        tests += [('collective', None, squared_error([actual['collective']], [ref['collective']], mg)),
                  ('worldForce', None, squared_error(actual['worldForce'], ref['worldForce'], mg)),
                  ('worldMoment', None, squared_error(actual['worldMoment'], ref['worldMoment'], mg * radius))]
        for category, rotor, bounds in tests:
            old = maxima[category]
            maxima[category] = (max(old[0], bounds[0]), max(old[1], bounds[1]))
            if witnesses[category] is None or bounds[1] > old[1]:
                witnesses[category] = {'id': p['id'], 'rotor': rotor}
    errors = {key: error_record(maxima[key], witnesses[key]) for key in CATEGORIES}
    qualified = (all(identity.values()) and support['matches'] and not arithmetic_failures and consumption_matches
                 and all(errors[key]['decision'] == 'pass' for key in CATEGORIES))
    result.update(identity=identity, support=support, errors=errors,
                  consumptionMatches=consumption_matches,
                  loadArithmetic={'passed': not arithmetic_failures, 'failureCount': len(arithmetic_failures),
                                  'categoryFailureCounts': {category: sum(item['category'] == category
                                                            for item in arithmetic_failures)
                                                            for category in CATEGORIES},
                                  'witnesses': arithmetic_failures[:8]},
                  qualified=qualified, decision='qualified' if qualified else 'unqualified')
    return result


def arithmetic_fixtures():
    """Fixed prospective assertions. Called only in a later authorized checker run."""
    checks = []
    def check(name, condition):
        checks.append({'id': name, 'passed': bool(condition)})
    check('one-word', dyadic('3ff0000000000000') == 1)
    check('signed-zero', dyadic('8000000000000000') == 0)
    check('minimum-subnormal', dyadic('0000000000000001') == Fraction(1, 1 << 1074))
    check('halfway-even-down', rounded_word(1 + Fraction(1, 1 << 53)) == '3ff0000000000000')
    check('halfway-even-up', rounded_word(1 + Fraction(3, 1 << 53)) == '3ff0000000000002')
    check('subnormal-half-to-zero', rounded_word(Fraction(1, 1 << 1075)) == '0000000000000000')
    check('negative-halfway-even', rounded_word(-1 - Fraction(1, 1 << 53)) == 'bff0000000000000')
    check('scalar-inside-box', scalar_error(Fraction(1), (Fraction(0), Fraction(2))) == (0, 1))
    check('euclidean-3-4-5', squared_error([Fraction(0)] * 3, [(Fraction(3), Fraction(3)),
          (Fraction(4), Fraction(4)), (Fraction(0), Fraction(0))], Fraction(1)) == (25, 25))
    check('strict-threshold-inclusive', verdict((TAU ** 2, TAU ** 2)) == 'pass')
    check('strict-threshold-fail', verdict((2 * TAU ** 2, 3 * TAU ** 2)) == 'fail')
    check('reference-overlap-unresolved', verdict((TAU ** 2 / 2, 2 * TAU ** 2)) == 'unresolved')
    check('rational-square-root-enclosure', sqrt_bounds(Fraction(2))[0] ** 2 <= 2 <= sqrt_bounds(Fraction(2))[1] ** 2)
    check('signed-moment-cancellation', left_sum([Fraction(1), Fraction(-1)]) == 0)
    return checks


def set_load_words(evidence, index, rotor):
    computed = native_loads(evidence['prepared'][index], rotor)
    for key, value in computed.items():
        evidence['loads'][index][key] = ([rounded_word(x) for x in value]
                                         if isinstance(value, list) else rounded_word(value))


def corruption_checks(evidences, targets):
    """Four fixed corruptions; all-row laws avoid selecting attractive witnesses."""
    specs = [('load-word', 'run-a-t0'), ('squared-force-law', 'run-a-t0'),
             ('body-frame-force', 'run-a-t5'), ('load-id-association', 'run-a-t0')]
    reports = []
    for name, case_id in specs:
        original = evidences[(case_id, 'F')]
        if original['status'] != 'native-success':
            reports.append({'id': name, 'passed': False, 'reason': 'fixed-native-success-witness-unavailable'})
            continue
        baseline = audit_evidence(original, targets[case_id], 'F')
        if not baseline['loadArithmetic']['passed'] or not all(baseline['identity'].values()):
            reports.append({'id': name, 'passed': False, 'reason': 'fixed-clean-arithmetic-witness-unavailable'})
            continue
        changed = copy.deepcopy(original)
        if name == 'load-word':
            changed['loads'][0]['rotor'][0] = '0000000000000000'
        elif name == 'squared-force-law':
            witnessed = False
            for index, solution in enumerate(changed['solution']):
                witnessed |= any(0 < dyadic(z['x']) < 1 for z in solution['rotors'])
                rotor = [rnd(rnd(dyadic(changed['prepared'][index]['forces'][r]) * dyadic(z['x'])) * dyadic(z['x']))
                         for r, z in enumerate(solution['rotors'])]
                for r, value in enumerate(rotor):
                    solution['rotors'][r]['T'] = rounded_word(value)
                set_load_words(changed, index, rotor)
            if not witnessed:
                reports.append({'id': name, 'passed': False, 'reason': 'fixed-nontrivial-root-witness-unavailable'})
                continue
        elif name == 'body-frame-force':
            witnessed = False
            for prepared, load in zip(changed['prepared'], changed['loads']):
                axis = [dyadic(x) for x in prepared['axis']]
                witnessed |= axis[0] != 0 or axis[1] != 0
                load['worldForce'] = ['0000000000000000', '0000000000000000', load['collective']]
            if not witnessed:
                reports.append({'id': name, 'passed': False, 'reason': 'fixed-tilt-witness-unavailable'})
                continue
        else:
            changed['loads'][0]['id'] = changed['loads'][1]['id']
        changed_words = sum(a != b for old, new in zip(original['loads'], changed['loads'])
                            for a, b in zip(old['rotor'] + [old['collective']] + old['worldForce'] + old['worldMoment'],
                                            new['rotor'] + [new['collective']] + new['worldForce'] + new['worldMoment']))
        changed_ids = sum(old['id'] != new['id'] for old, new in zip(original['loads'], changed['loads']))
        if changed_words + changed_ids == 0:
            reports.append({'id': name, 'passed': False, 'reason': 'fixed-transformation-has-no-word-change'})
            continue
        try:
            result = audit_evidence(changed, targets[case_id], 'F')
            expected_category = 'worldForce' if name == 'body-frame-force' else 'rotor'
            detected = (name != 'load-id-association' and not result['loadArithmetic']['passed']
                        and result['loadArithmetic']['categoryFailureCounts'][expected_category] > 0)
            reports.append({'id': name, 'passed': detected, 'detection': result['decision'],
                            'changedLoadWords': changed_words, 'changedIds': changed_ids})
        except InvalidRecord as error:
            reports.append({'id': name, 'passed': name == 'load-id-association'
                            and str(error) == 'native-load-solution-ids', 'detection': str(error),
                            'changedLoadWords': changed_words, 'changedIds': changed_ids})
    return reports


def dotted(value, path):
    for name in path.split('.'):
        require(isinstance(value, dict) and name in value, 'missing-browser-field:' + path)
        value = value[name]
    return value


def browser_controls(browser, contract):
    controls = browser['controls']
    inherited = controls['inherited']
    records = inherited['records']
    require(inherited['expectedCount'] == 48 and len(records) == 48, 'inherited-control-count')
    require([row['id'] for row in records] == contract['inheritedControlIds'], 'inherited-control-ids')
    for row in records:
        require(row['pass'] is True and row['inputUnchanged'] is True
                and row['screenExpectation'] is True and row['comparison']['pass'] is True
                and row['omissionAudit']['pass'] is True and row['solutionComparison']['pass'] is True,
                'inherited-control-record-assertions')
        require(row['inputBeforeTokens'] == row['stateTokens']
                and row['inputBeforeSha256'] == row['inputAfterSha256'], 'inherited-control-input-identity')
        for key in ('offsets', 'sources', 'K', 'a', 'symbols', 'admission', 'graph', 'symbolCounts'):
            require(row['L'][key] == row['F'][key], 'inherited-control-saved-native-parity')
    wrappers = controls['wrapper']
    require(wrappers['expectedCount'] == len(contract['wrapperControls'])
            and len(wrappers['records']) == len(contract['wrapperControls']) <= 24, 'wrapper-control-count')
    for row, expected in zip(wrappers['records'], contract['wrapperControls']):
        require(row['id'] == expected['id'] and row['method'] == expected['method']
                and row['expectedStatus'] == expected['expectedStatus'], 'wrapper-control-identity')
        require(row['evidence']['status'] == expected['expectedStatus'] and row['pass'] is True,
                'wrapper-control-assertion')
        require(row['inputUnchanged'] is True and row['checks']['pass'] is True
                and isinstance(row['checks']['checks'], list) and row['checks']['checks']
                and all(item['pass'] is True for item in row['checks']['checks']), 'wrapper-individual-assertions')
    require(inherited['passed'] is True and wrappers['passed'] is True, 'browser-control-failure')
    ownership = controls['ownership']
    require(ownership['sequence'] == contract['ownershipSequence'], 'ownership-sequence')
    require(all(ownership[key] is True for key in ('inputUnchanged', 'returnedStorageDisjoint', 'pass')),
            'ownership-control-failure')
    require(len(ownership['extraBuilds']) == 6
            and all(row['inputUnchanged'] is True and row['inputBeforeSha256'] == row['inputAfterSha256']
                    and row['inputBeforeTokens'] == row['stateTokens'] for row in ownership['extraBuilds']),
            'ownership-extra-build-assertions')
    require(controls['ownershipBuilds'] == ownership['extraBuilds'], 'ownership-journal-record-identity')
    require(all(ownership['retained'][method]['before'] == ownership['retained'][method]['after']
                for method in ('F', 'L')), 'ownership-retained-storage')
    previous_id = None
    ordered = [(row, 'control:' + row['id']) for row in wrappers['records']]
    ordered += [(row, 'target:' + row['caseId'] + ':' + row['method']) for row in browser['calls']]
    for row, result_id in ordered:
        own = row['ownership']
        require(all(own[key] is True for key in ('inputStorageDisjoint', 'previousResultUnchanged',
                                                'previousStorageDisjoint', 'pass'))
                and own['previousResultId'] == previous_id, 'native-result-storage-ownership')
        if row['evidence']['status'] == 'native-success':
            previous_id = result_id
    return {'passed': True, 'inheritedCount': 48, 'wrapperCount': len(wrappers['records']),
            'scope': 'fixed counts/IDs/statuses and assertions from verified browser-control source; '
                     'independent exact target audit is reported separately'}


def browser_provenance(root, browser, manifest):
    package = root / PACKAGE
    runtime = parse_json((package / 'runtime.json').read_bytes())
    require(browser['browser']['product'] == 'Chrome/' + runtime['chrome']['version']
            and browser['browser']['version'] == runtime['chrome']['version']
            and browser['browser']['headless'] is True, 'named-chrome-identity')
    for field in ('platform', 'architecture'):
        require(browser['runtime'][field] == runtime[field], 'browser-platform-identity')
    require(browser['runtime']['node'] == runtime['node']
            and all(runtime['node'][key] == manifest['runtime']['node'][key] for key in ('bytes', 'sha256')),
            'browser-node-runtime-identity')
    require(browser['runtime']['playwright']['version'] == runtime['playwright']['version']
            and browser['runtime']['chromeFilesVerified'] == len(runtime['chrome']['files'])
            and browser['runtime']['playwrightFilesVerified'] == len(runtime['playwright']['files']),
            'browser-component-runtime-identity')
    launch = browser['browserLaunch']
    require(launch['count'] == launch['profileCount'] == 1 and launch['detachedApplied'] is False
            and SHA.fullmatch(launch['profileIdentitySha256']), 'browser-launch-identity')
    source_bundle = parse_json((package / 'source/source-bundle.json').read_bytes())
    bundle_pin = {key: source_bundle[key] for key in ('path', 'bytes', 'sha256')}
    bundle = read_pin(root, bundle_pin)
    receipt = browser['sourceReceipt']
    require(receipt['bundle'] == bundle_pin and receipt['sources'] == source_bundle['sources']
            and receipt['verifiedBeforeFactoryExecution'] is True and receipt['nativeArithmetic'] is True,
            'browser-executed-source-identity')
    require(len(source_bundle['sources']) == 7, 'browser-source-count')
    ids, previous_end = [], 0
    for item in source_bundle['sources']:
        ids.append(item['id'])
        start = integer(item['offset'], previous_end, len(bundle), 'bundle-slice-offset')
        stop = start + integer(item['bytes'], 1, len(bundle) - start, 'bundle-slice-length')
        source_bytes = read_pin(root, {key: item[key] for key in ('path', 'bytes', 'sha256')})
        require(bundle[start:stop] == source_bytes, 'bundle-slice-source-byte-identity')
        previous_end = stop
    expected_ids = ['./vendor/reference-excerpt.cjs', './vendor/anchor-kernel.cjs',
                    './vendor/lean-anchor.cjs', './vendor/kernel.cjs', './vendor/controls.cjs',
                    './native-load.cjs', './native-controls.cjs']
    require(ids == expected_ids and sorted(receipt['factoryExecutionIds']) == sorted(ids),
            'browser-factory-allowlist')
    adapter = browser['controls']['adapter']
    require(adapter == receipt['adapterControls'] and adapter['pass'] is True
            and adapter['beforeScientificFactories'] is True
            and adapter['expectedGroups'] == adapter['executedGroups'] == 9
            and adapter['expectedChecks'] == adapter['executedChecks'] == 56, 'browser-adapter-counts')
    groups = vector(adapter['groups'], 9, 'browser-adapter-groups')
    require(len({row['id'] for row in groups}) == 9
            and all(row['pass'] is True and row['errorClass'] is None
                    and len(row['checks']) == row['expectedChecks']
                    and all(item['pass'] is True for item in row['checks']) for row in groups)
            and sum(len(row['checks']) for row in groups) == 56, 'browser-adapter-assertions')
    return {'passed': True, 'bundleAndSevenSlicesMatchPinnedStandaloneSources': True,
            'runtimeIdentityScope': 'named-version and verified-runner component-hash report; not full transitive attestation'}


def main(root, expected_manifest_sha, expected_commit):
    package = root / PACKAGE
    manifest_bytes = (package / 'source-manifest.json').read_bytes()
    require(SHA.fullmatch(expected_manifest_sha) and hashlib.sha256(manifest_bytes).hexdigest()
            == expected_manifest_sha, 'source-manifest-hash')
    require(re.fullmatch(r'[0-9a-f]{40}', expected_commit), 'source-commit-format')
    manifest = parse_json(manifest_bytes)
    pinned_paths = set()
    for pin in manifest['files']:
        require(pin['path'] not in pinned_paths, 'duplicate-source-pin')
        pinned_paths.add(pin['path'])
        read_pin(root, pin)
    required_paths = {PACKAGE + '/source/check.py', PACKAGE + '/source/checker-contract.json',
                      PACKAGE + '/runtime.json', PACKAGE + '/source/source-bundle.json',
                      PACKAGE + '/source/browser-bundle.js'}
    require(required_paths <= pinned_paths, 'checker-required-source-pins')
    require(Path(__file__).resolve() == (package / 'source/check.py').resolve(), 'checker-location')
    python_bytes = Path(sys.executable).resolve().read_bytes()
    require(len(python_bytes) == manifest['runtime']['python']['bytes'] and hashlib.sha256(python_bytes).hexdigest()
            == manifest['runtime']['python']['sha256'], 'checker-python-runtime')
    contract = parse_json((package / 'source/checker-contract.json').read_bytes())
    require(contract['schema'] == 'm31-native-checker-contract-v1', 'checker-contract-schema')
    require(contract['expectedSchedule'] == [{'caseId': c, 'method': m} for c, m in SCHEDULE], 'checker-schedule')
    fixture_report = arithmetic_fixtures()
    require(all(row['passed'] for row in fixture_report), 'checker-arithmetic-fixture-failure')
    index = parse_json(read_pin(root, contract['index']))
    require(contract['index']['sha256'] == '3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393',
            'retained-index-pin')
    require([row['id'] for row in contract['states']] == list(CASES), 'checker-six-states')
    targets = {}
    for row in contract['states']:
        raw = parse_json(read_pin(root, row['input']))
        ref = parse_json(read_pin(root, row['reference']))
        require(ref['schema'] == contract['savedReferenceSchema']
                and ref['sourceCommit'] == contract['savedSourceCommit'] == index['sourceCommit'],
                'saved-reference-source-identity')
        envelope = {'domain': 'm31-moving-admission/input/v1', 'id': row['id'], 'input': raw}
        digest = hashlib.sha256(canonical(envelope)).hexdigest()
        require(digest == row['semanticInputSha256'], 'retained-semantic-envelope-hash')
        targets[row['id']] = reference_target(row['id'], raw, ref, index['constants'], digest)
        targets[row['id']]['inputFileSha256'] = row['input']['sha256']
    browser_bytes = (package / 'results/browser.json').read_bytes()
    browser = parse_json(browser_bytes)
    require(browser['schema'] == 'm31-native-browser-qualification-v1'
            and browser['sourceManifestSha256'] == expected_manifest_sha
            and browser['sourceCommit'] == expected_commit and browser['complete'] is True,
            'browser-completion-provenance')
    require(isinstance(contract['requiredBrowserEquals'], dict) and contract['requiredBrowserEquals'],
            'missing-frozen-browser-identity-assertions')
    for path, expected in contract['requiredBrowserEquals'].items():
        require(dotted(browser, path) == expected, 'browser-identity-assertion:' + path)
    provenance_report = browser_provenance(root, browser, manifest)
    control_report = browser_controls(browser, contract)
    calls = vector(browser['calls'], 12, 'browser-target-call-count')
    reports, evidences = [], {}
    for sequence, (call, (case_id, method)) in enumerate(zip(calls, SCHEDULE)):
        require(call['sequence'] == sequence and call['caseId'] == case_id and call['method'] == method,
                'browser-call-schedule')
        require(call['inputUnchanged'] is True and call['semanticInputSha256'] == targets[case_id]['digest']
                and call['inputFileSha256'] == targets[case_id]['inputFileSha256'],
                'browser-raw-identity')
        diagnostic_ms = call['diagnosticCallMs']
        require(type(diagnostic_ms) in (int, float) and math.isfinite(diagnostic_ms) and diagnostic_ms >= 0,
                'diagnostic-duration-format')
        evidences[(case_id, method)] = call['evidence']
        reports.append(audit_evidence(call['evidence'], targets[case_id], method))
    corruption_report = corruption_checks(evidences, targets)
    # An unavailable corruption witness closes qualification; it is not replaced.
    parity = []
    for case_id in CASES:
        left, right = evidences[(case_id, 'F')], evidences[(case_id, 'L')]
        keys = ('status', 'reason', 'ids', 'raw', 'constants', 'prepared', 'coefficients', 'solution', 'loads')
        differences = [key for key in keys if left.get(key) != right.get(key)]
        parity.append({'caseId': case_id, 'matches': not differences, 'differentFields': differences})
    qualified = (all(row['qualified'] for row in reports) and all(row['matches'] for row in parity)
                 and all(row['passed'] for row in corruption_report))
    return {'schema': 'm31-native-load-check-v1', 'passed': True,
            'decision': 'qualified' if qualified else 'unqualified',
            'qualificationScope': 'retained-six-state native-load accuracy in the recorded named Chrome only',
            'performanceClaim': False, 'onlineCertificationClaim': False,
            'sourceManifestSha256': expected_manifest_sha, 'sourceCommit': expected_commit,
            'browserOutputSha256': hashlib.sha256(browser_bytes).hexdigest(),
            'normalization': {'mg': targets[CASES[0]]['constants']['mg'], 'R': targets[CASES[0]]['constants']['R'],
                              'tolerance': encoded(TAU), 'comparison': 'exact squared normalized error bounds'},
            'attemptedTargetCalls': 12, 'qualifiedTargetCalls': sum(row['qualified'] for row in reports),
            'browserControls': control_report, 'arithmeticFixtures': fixture_report,
            'browserProvenance': provenance_report,
            'corruptionChecks': corruption_report, 'nativeParity': parity, 'calls': reports}


if __name__ == '__main__':
    output = None
    try:
        require(len(sys.argv) == 4, 'usage: check.py ROOT MANIFEST_SHA SOURCE_COMMIT')
        root = Path(sys.argv[1]).resolve()
        output = root / PACKAGE / 'results/check.json'
        require(output.parent.is_dir() and not output.exists(), 'checker-output-exists-or-parent-missing')
        report = main(root, sys.argv[2], sys.argv[3])
        exit_code = 0
    except Exception as error:
        report = {'schema': 'm31-native-load-check-v1', 'passed': False, 'decision': 'invalid-record',
                  'errorClass': type(error).__name__, 'reason': str(error)[:1000]}
        exit_code = 1
    if output is not None and output.parent.is_dir() and not output.exists():
        encoded_report = (json.dumps(report, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()
        require(len(encoded_report) <= MAX_JSON, 'checker-report-byte-cap')
        with output.open('xb') as handle:
            handle.write(encoded_report)
            handle.flush()
            os.fsync(handle.fileno())
    print(json.dumps({'passed': report['passed'], 'decision': report['decision']}))
    sys.exit(exit_code)
