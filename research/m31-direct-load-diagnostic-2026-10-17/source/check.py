"""Independent, single-use saved direct-load diagnostic checker (source draft).

No producer/scientific imports.  run(root) is for the separately allocated
checker stage only; this source has not been imported or executed in preparation.
Literal fixtures precede all target reads.  Failure stops without repair/retry.
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import re
from fractions import Fraction as Q

STATES = ('run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10')
TIERS = ('1e-8', '1e-4', '1e-2')
CATEGORIES = ('rotor', 'collective', 'worldForce', 'worldMoment')
PRIOR = 'research/m31-normalizer-replication-2026-10-17/results'
CONSTANT_BITS = {'mg': '3fd0f3a14cec41dd', 'R': '3fa4462fb7ff5035'}
CONSTANT_PROVENANCE = {'path': PRIOR + '/index.json',
    'sha256': '3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393'}
GRID = 1 << 192
FILE_LIMIT = 16 * 1024 * 1024
PRODUCER_FIXTURES = ('sqrt-one-exact', 'sqrt-two-fixed192', 'root-grid-outward-nondyadic',
    'root-grid-exact-boundaries', 'cubic-alpha-zero', 'cubic-alpha-seven-fourths',
    'candidate-y-one', 'signed-cancellation-and-linear-rotor-load', 'signed-load-boxes',
    'upper-only-contraction-contains-full', 'exact-error-boundary-pass',
    'exact-error-boundary-fail', 'exact-error-boundary-overlap',
    'signed-euclidean-three-four-five', 'ceil-ten-percent-upper-tie-zero-lower')
ARITHMETIC = {'proposal': 'Python FP64, explicit left-to-right sums, no fused operations',
    'coefficientConversion': 'float of exact rational endpoint midpoint',
    'termOrder': 'input source order within each receiver and rotor',
    'initialCandidate': 'all ones', 'iterations': 48, 'cubicBisections': 54,
    'sqrtFractionBits': 192, 'rootFractionBits': 192,
    'certificate': 'exact rational operations; sqrt fixed192 enclosure and roots outward fixed192 grid'}
MASK_RULE = 'ceil(P/10), coefficient upper ascending then stable (i,r,j)'


class CheckError(Exception):
    pass


def need(condition, code):
    if not condition:
        raise CheckError(code)


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def exact(a, b, code):
    need(same(a, b), code)


def fields(value, names, code):
    need(type(value) is dict and set(value) == set(names), code)


def qwire(value):
    return {'n': str(value.numerator), 'd': str(value.denominator)}


def qread(value):
    fields(value, ('n', 'd'), 'rational-shape')
    for part in ('n', 'd'):
        need(type(value[part]) is str and len(value[part]) <= 4096 and
             re.fullmatch(r'0|-?[1-9][0-9]*', value[part]), 'rational-text')
    numerator, denominator = int(value['n']), int(value['d'])
    need(denominator > 0, 'rational-denominator')
    result = Q(numerator, denominator)
    exact(value, qwire(result), 'rational-normalization')
    return result


def bwire(bounds):
    return {'l': qwire(bounds[0]), 'u': qwire(bounds[1])}


def bread(value):
    fields(value, ('l', 'u'), 'interval-shape')
    low, high = qread(value['l']), qread(value['u'])
    need(low <= high, 'interval-order')
    return low, high


def binary64(word):
    """Integer sign/exponent/significand decoding, with no struct or FP decode."""
    need(type(word) is str and re.fullmatch(r'[0-9a-f]{16}', word), 'binary64-word')
    bits = int(word, 16)
    exponent, mantissa = (bits >> 52) & 2047, bits & ((1 << 52) - 1)
    need(exponent < 2047, 'binary64-finite')
    numerator = mantissa if exponent == 0 else (1 << 52) + mantissa
    power = -1074 if exponent == 0 else exponent - 1075
    if bits >> 63:
        numerator = -numerator
    return Q(numerator << power) if power >= 0 else Q(numerator, 1 << -power)


def candidate_hex(text):
    need(type(text) is str and len(text) < 64, 'candidate-hex-shape')
    match = re.fullmatch(r'0x([0-9a-f]+)\.([0-9a-f]+)p([+-][0-9]+)', text)
    need(match is not None, 'candidate-hex-syntax')
    whole, tail, exponent = match.groups()
    exponent = int(exponent)
    need(-2000 <= exponent <= 0, 'candidate-hex-exponent')
    result = Q(int(whole + tail, 16), 16 ** len(tail))
    result *= Q(1 << exponent) if exponent >= 0 else Q(1, 1 << -exponent)
    need(0 < result <= 1, 'candidate-domain')
    need(float(result).hex() == text, 'candidate-hex-canonical-binary64')
    return result


def read_json(root, path, pins):
    path = Path(path)
    if not path.is_absolute():
        path = root / path
    need(path.resolve() == path and path.is_file(), 'input-path')
    relative = str(path.relative_to(root))
    need(path.stat().st_size <= FILE_LIMIT, 'input-file-limit:' + relative)
    raw = path.read_bytes()
    need(len(raw) <= FILE_LIMIT, 'input-file-limit:' + relative)

    def unique(pairs):
        value = {}
        for key, item in pairs:
            need(key not in value, 'duplicate-json-key')
            value[key] = item
        return value

    def nonfinite(_):
        raise CheckError('nonfinite-json')

    value = json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)
    pin = {'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    pins.append(pin)
    return value, pin


def integer_square_root(number):
    """Newton floor square root, independent of producer's math.isqrt call."""
    need(type(number) is int and number >= 0, 'integer-sqrt-domain')
    if number < 2:
        return number
    estimate = 1 << ((number.bit_length() + 1) // 2)
    while True:
        following = (estimate + number // estimate) // 2
        if following >= estimate:
            need(estimate * estimate <= number < (estimate + 1) ** 2, 'integer-sqrt-proof')
            return estimate
        estimate = following


def square_root(value):
    need(value >= 0, 'sqrt-domain')
    scaled = value * GRID * GRID
    low_integer = integer_square_root(scaled.numerator // scaled.denominator)
    high_integer = low_integer if Q(low_integer * low_integer) == scaled else low_integer + 1
    low, high = Q(low_integer, GRID), Q(high_integer, GRID)
    need(low * low <= value <= high * high, 'sqrt-outward-proof')
    return low, high


def outward(bounds):
    a, b = bounds[0] * GRID, bounds[1] * GRID
    return Q(a.numerator // a.denominator, GRID), Q(-(-b.numerator // b.denominator), GRID)


def add(bounds):
    values = list(bounds)
    return sum((v[0] for v in values), Q(0)), sum((v[1] for v in values), Q(0))


def multiply(left, right):
    products = [a * b for a in left for b in right]
    return min(products), max(products)


def scale(bounds, value):
    return multiply(bounds, (value, value))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def geometry(value):
    need(len(value['forces']) == 4 and len(value['axis']) == 3 and len(value['offsets']) == 4
         and all(len(offset) == 3 for offset in value['offsets']), 'prepared-shape')
    forces = [binary64(word) for word in value['forces']]
    need(all(force > 0 for force in forces), 'prepared-positive-forces')
    axis = [binary64(word) for word in value['axis']]
    offsets = [[binary64(word) for word in offset] for offset in value['offsets']]
    total = sum(forces, Q(0))
    return {'forces': forces, 'axis': axis, 'levers': [cross(offset, axis) for offset in offsets],
            'weights': [force / total for force in forces]}


def loads(g, roots):
    rotor = [scale(bounds, force) for bounds, force in zip(roots, g['forces'])]
    collective = add(rotor)
    return {'rotor': rotor, 'collective': collective,
        'force': [scale(collective, component) for component in g['axis']],
        'moment': [add(scale(rotor[r], g['levers'][r][k]) for r in range(4)) for k in range(3)]}


def point_loads(g, candidate):
    boxes = loads(g, [(value, value) for value in candidate])
    return {key: value[0] if key == 'collective' else [pair[0] for pair in value]
            for key, value in boxes.items()}


def point_wire(value):
    return {key: qwire(item) if key == 'collective' else [qwire(v) for v in item]
            for key, item in value.items()}


def distance(bounds, point):
    displacement = bounds[0] - point, bounds[1] - point
    low = Q(0) if displacement[0] <= 0 <= displacement[1] else min(abs(v) for v in displacement)
    return low, max(abs(v) for v in displacement)


def norm_distance(boxes, point, normalization):
    need(normalization > 0 and len(boxes) == len(point) == 3, 'norm-domain')
    components = [distance(bounds, value) for bounds, value in zip(boxes, point)]
    squares = [sum((value[k] ** 2 for value in components), Q(0)) for k in (0, 1)]
    return square_root(squares[0])[0] / normalization, square_root(squares[1])[1] / normalization


def maximum(intervals):
    values = list(intervals)
    need(bool(values), 'maximum-domain')
    return max(v[0] for v in values), max(v[1] for v in values)


def errors(boxes, point, mg, radius):
    return {'rotor': maximum(scale(distance(box, value), 4 / mg)
                    for box, value in zip(boxes['rotor'], point['rotor'])),
        'collective': scale(distance(boxes['collective'], point['collective']), 1 / mg),
        'worldForce': norm_distance(boxes['force'], point['force'], mg),
        'worldMoment': norm_distance(boxes['moment'], point['moment'], mg * radius)}


def classify(bounds, tolerance, certificate=False):
    if bounds[1] <= tolerance:
        return 'pass'
    if certificate:
        return 'not-certified'
    return 'definite-fail' if bounds[0] > tolerance else 'unresolved'


def summary(per_drone, certificate=False):
    maxima = {category: maximum(row[category] for row in per_drone) for category in CATEGORIES}
    tiers = []
    for tier in TIERS:
        statuses = {category: classify(maxima[category], Q(tier), certificate) for category in CATEGORIES}
        all_pass = all(status == 'pass' for status in statuses.values())
        overall = 'pass' if all_pass else ('not-certified' if certificate else
            'definite-fail' if 'definite-fail' in statuses.values() else 'unresolved')
        tiers.append({'tier': tier, 'categories': statuses, 'overall': overall})
    return {'maxErrors': {category: bwire(maxima[category]) for category in CATEGORIES}, 'tiers': tiers}


def check_summary(saved, expected, audit):
    fields(saved, ('maxErrors', 'tiers'), audit + '-summary-shape')
    exact(saved['maxErrors'], expected['maxErrors'], audit + '-error-intervals')
    exact(saved['tiers'], expected['tiers'], audit + '-tier-classification')


def mask_for(coefficients):
    # Stable tuple key is explicit; positivity comes from status, not lower>0.
    order = sorted(coefficients, key=lambda key: (coefficients[key][1], key[0], key[1], key[2]))
    quotient, remainder = divmod(len(order), 10)
    return order[:quotient + int(remainder != 0)]


def mask_wire(mask):
    return [{'i': i, 'r': r, 'j': j} for i, r, j in mask]


def check_mask(saved, coefficients):
    need(type(saved) is list, 'mask-list')
    expected = mask_wire(mask_for(coefficients))
    need(len(saved) == len(expected), 'mask-ceiling-cardinality')
    exact(saved, expected, 'mask-upper-rank-and-ties')


def native_replay(context, mask):
    """Independent replay of the fixed proposal recipe, not another proposal."""
    ids, omitted = context['ids'], set(mask)
    positions = {identifier: index for index, identifier in enumerate(ids)}
    weights, terms = [], []
    for identifier in ids:
        forces = [float(value) for value in context['geometry'][identifier]['forces']]
        total = 0.0
        for value in forces:
            total = total + value
        need(math.isfinite(total) and total > 0, 'replay-force-total')
        weights.append([value / total for value in forces])
        for rotor in range(4):
            terms.append([(positions[source], float((bounds[0] + bounds[1]) / 2))
                for source, bounds in context['rows'][identifier, rotor]
                if (identifier, rotor, source) not in omitted])
    candidate = [[1.0] * 4 for _ in ids]
    for _ in range(48):
        source_values = []
        for index in range(len(ids)):
            total = 0.0
            for rotor in range(4):
                total = total + weights[index][rotor] * candidate[index][rotor]
            source_values.append(math.sqrt(total))
        flat = []
        for row in terms:
            coefficient = 0.0
            for source, midpoint in row:
                coefficient = coefficient + midpoint * source_values[source]
            need(math.isfinite(coefficient) and coefficient >= 0.0, 'replay-alpha')
            left, right = 0.0, 1.0
            for _ in range(54):
                middle = (left + right) / 2.0
                if middle * middle * middle + coefficient * middle > 1.0:
                    right = middle
                else:
                    left = middle
            flat.append((left + right) / 2.0)
        candidate = [flat[4*i:4*i+4] for i in range(len(ids))]
    need(all(math.isfinite(value) and 0 < value <= 1 for row in candidate for value in row), 'replay-candidate-domain')
    return [{'id': identifier, 'xHex': [value.hex() for value in candidate[index]]} for index, identifier in enumerate(ids)]


def contractions(terms, y, omitted_sources):
    full_parts, upper_parts, deleted_coefficients, deleted_products = [], [], [], []
    for source, coefficient in terms:
        contribution = multiply(coefficient, y[source])
        full_parts.append(contribution)
        upper_parts.append((Q(0), contribution[1]) if source in omitted_sources else contribution)
        if source in omitted_sources:
            deleted_coefficients.append(coefficient)
            deleted_products.append(contribution)
    return add(full_parts), add(upper_parts), add(deleted_coefficients), add(deleted_products)


def certificate(context, candidate, point, y, mask, mode, mg, radius):
    omitted = set(mask)
    algebra, global_factor = [], Q(1)
    for identifier in context['ids']:
        for rotor in range(4):
            terms = context['rows'][identifier, rotor]
            omitted_sources = {source for source, _ in terms if (identifier, rotor, source) in omitted}
            variants = contractions(terms, y, omitted_sources)
            contraction = variants[0 if mode == 'B' else 1]
            value = candidate[identifier][rotor]
            defect = (value**3 + value*contraction[0], value**3 + value*contraction[1])
            need(defect[0] > 0, mode + '-defect-positive')
            local_factor = max(Q(1), defect[1], Q(1) / defect[0])
            global_factor = max(global_factor, local_factor)
            algebra.append((identifier, rotor, contraction, defect, local_factor))
    roots = {identifier: [None] * 4 for identifier in context['ids']}
    rows = []
    for identifier, rotor, contraction, defect, local_factor in algebra:
        value = candidate[identifier][rotor]
        factor = local_factor * global_factor
        raw_root = (value / factor, min(Q(1), value * factor))
        root = outward(raw_root)
        need(0 <= root[0] <= raw_root[0] <= value <= raw_root[1] <= root[1] <= 1, mode + '-root-candidate-containment')
        roots[identifier][rotor] = root
        rows.append({'i': identifier, 'r': rotor, 's': bwire(contraction), 'p': bwire(defect),
                     'k': qwire(local_factor), 'xstar': bwire(root)})
    load_bounds = {identifier: loads(context['geometry'][identifier], roots[identifier]) for identifier in context['ids']}
    per_drone = [errors(load_bounds[identifier], point[identifier], mg, radius) for identifier in context['ids']]
    need(all(interval[0] == 0 for row in per_drone for interval in row.values()), mode + '-certificate-error-lower-zero')
    result = {'rows': rows, 'K': qwire(global_factor), **summary(per_drone, certificate=True)}
    return result, roots, load_bounds


def check_certificate(saved, expected, mode):
    fields(saved, ('rows', 'K', 'maxErrors', 'tiers'), mode + '-certificate-shape')
    need(type(saved['rows']) is list and len(saved['rows']) == len(expected['rows']), mode + '-row-count')
    for row, wanted in zip(saved['rows'], expected['rows']):
        fields(row, ('i', 'r', 's', 'p', 'k', 'xstar'), mode + '-row-shape')
        exact([row['i'], row['r']], [wanted['i'], wanted['r']], mode + '-row-order')
        exact(row['s'], wanted['s'], mode + '-complete-contraction')
        exact(row['p'], wanted['p'], mode + '-defect-interval')
        exact(row['k'], wanted['k'], mode + '-local-factor')
    exact(saved['K'], expected['K'], mode + '-global-factor')
    for row, wanted in zip(saved['rows'], expected['rows']):
        exact(row['xstar'], wanted['xstar'], mode + '-root-corollary-grid')
    check_summary({key: saved[key] for key in ('maxErrors', 'tiers')},
                  {key: expected[key] for key in ('maxErrors', 'tiers')}, mode)


def source_context(root, name, pins):
    inp, input_pin = read_json(root, PRIOR + '/inputs/' + name + '.json', pins)
    ref, reference_pin = read_json(root, PRIOR + '/reference/' + name + '.json', pins)
    need(ref['schema'] == 'm31-normalizer-ablation-reference-v1' and ref['id'] == name and
         ref['referenceStatus'] == 'admitted', 'reference-admission-identity')
    envelope = {'domain': 'm31-moving-admission/input/v1', 'id': name, 'input': inp}
    binding = hashlib.sha256(json.dumps(envelope, sort_keys=True, separators=(',', ':'),
                                       ensure_ascii=True, allow_nan=False).encode('ascii')).hexdigest()
    exact(ref['inputSha256'], binding, 'reference-input-binding')
    ids = [drone['id'] for drone in inp['drones']]
    need(len(ids) == 64 and all(type(i) is int and 0 <= i <= 65535 for i in ids) and len(set(ids)) == 64, 'input-id-domain')
    need(type(ref['prepared']) is list and len(ref['prepared']) == 64, 'prepared-count')
    exact([drone['id'] for drone in ref['prepared']], ids, 'prepared-id-order')
    exact_geometry = {}
    for raw, prepared in zip(inp['drones'], ref['prepared']):
        need(prepared['rejection'] is None and len(raw['state']) == 17, 'prepared-admission-state')
        exact(prepared['value']['forces'], raw['state'][13:17], 'prepared-force-binding')
        exact(prepared['value']['center'], raw['state'][:3], 'prepared-center-binding')
        exact_geometry[raw['id']] = geometry(prepared['value'])
    coefficients, seen = {}, set()
    need(type(ref['pairs']) is list and len(ref['pairs']) == 16128, 'reference-pair-count')
    for pair in ref['pairs']:
        key = pair['i'], pair['r'], pair['j']
        i, rotor, j = key
        need(all(type(v) is int for v in key) and i in exact_geometry and j in exact_geometry and
             i != j and 0 <= rotor < 4 and key not in seen, 'reference-pair-domain-duplicate')
        seen.add(key)
        if pair['status'] == 'zero':
            need('coefficient' not in pair, 'reference-zero-coefficient')
        else:
            need(pair['status'] == 'positive', 'reference-pair-status')
            bounds = bread(pair['coefficient'])
            need(0 <= bounds[0] <= bounds[1] and bounds[1] > 0 and
                 all((value * GRID).denominator == 1 for value in bounds), 'reference-positive-interval')
            coefficients[key] = bounds
    exact(ref['evaluatedPairs'], 16128, 'reference-evaluated-count')
    exact(ref['plannedPairs'], 16128, 'reference-planned-count')
    exact(ref['graph']['positiveRotorPairs'], len(coefficients), 'reference-positive-count')
    rows = {(i, rotor): [(j, coefficients[i, rotor, j]) for j in ids if (i, rotor, j) in coefficients]
            for i in ids for rotor in range(4)}
    exact([entry['id'] for entry in ref['loads']], ids, 'reference-load-order')
    reference_loads = {}
    for entry in ref['loads']:
        need(len(entry['roots']) == 4, 'reference-root-count')
        roots = [bread(bounds) for bounds in entry['roots']]
        need(all(0 < low <= high <= 1 for low, high in roots), 'reference-root-domain')
        boxes = entry['loads']
        fields(boxes, ('rotor', 'collective', 'force', 'moment'), 'reference-load-shape')
        need(len(boxes['rotor']) == 4 and len(boxes['force']) == len(boxes['moment']) == 3, 'reference-load-vector-count')
        actual = {key: bread(value) if key == 'collective' else [bread(v) for v in value] for key, value in boxes.items()}
        need(actual == loads(exact_geometry[entry['id']], roots), 'reference-root-load-consistency')
        reference_loads[entry['id']] = actual
    return {'name': name, 'ids': ids, 'geometry': exact_geometry, 'rows': rows, 'coefficients': coefficients,
            'referenceLoads': reference_loads, 'inputSha256': binding, 'inputFile': input_pin, 'referenceFile': reference_pin}


def check_candidate(saved, expected, ids):
    exact(saved, expected, 'native-proposal-replay')
    candidate = {}
    for identifier, row in zip(ids, saved):
        fields(row, ('id', 'xHex'), 'candidate-row-shape')
        need(len(row['xHex']) == 4, 'candidate-rotor-count')
        candidate[identifier] = [candidate_hex(text) for text in row['xHex']]
    return candidate


def check_proposal(saved, context, label, mask, mg, radius):
    names = ['id', 'omittedCount', 'candidate', 'candidateLoads', 'sourceY', 'A', 'B']
    if label == 'omit10':
        names += ['C', 'omissionDiagnostics']
    fields(saved, names, 'proposal-shape')
    exact(saved['id'], label, 'proposal-identity')
    exact(saved['omittedCount'], len(mask), 'proposal-omitted-count')
    ids = context['ids']
    replay = native_replay(context, mask)
    candidate = check_candidate(saved['candidate'], replay, ids)
    point = {identifier: point_loads(context['geometry'][identifier], candidate[identifier]) for identifier in ids}
    expected_points = [{'id': identifier, 'loads': point_wire(point[identifier])} for identifier in ids]
    exact(saved['candidateLoads'], expected_points, 'candidate-load-identity')
    y = {identifier: square_root(sum((weight * value for weight, value in
         zip(context['geometry'][identifier]['weights'], candidate[identifier])), Q(0))) for identifier in ids}
    expected_y = [{'id': identifier, 'y': bwire(y[identifier])} for identifier in ids]
    exact(saved['sourceY'], expected_y, 'exact-weight-candidate-y')
    audit_a = summary([errors(context['referenceLoads'][identifier], point[identifier], mg, radius) for identifier in ids])
    check_summary(saved['A'], audit_a, 'A')
    audit_b, roots_b, loads_b = certificate(context, candidate, point, y, mask, 'B', mg, radius)
    check_certificate(saved['B'], audit_b, 'B')
    expected = {'candidate': replay, 'candidateLoads': expected_points, 'sourceY': expected_y, 'A': audit_a, 'B': audit_b}
    if label == 'omit10':
        audit_c, roots_c, loads_c = certificate(context, candidate, point, y, mask, 'C', mg, radius)
        check_certificate(saved['C'], audit_c, 'C')
        expected['C'] = audit_c
        for b, c in zip(audit_b['rows'], audit_c['rows']):
            bs, cs = bread(b['s']), bread(c['s'])
            need(cs[0] <= bs[0] and cs[1] == bs[1], 'C-vs-B-contraction-order')
        for identifier in ids:
            for b, c in zip(roots_b[identifier], roots_c[identifier]):
                need(c[0] <= b[0] <= b[1] <= c[1], 'C-vs-B-root-containment')
            for category in ('rotor', 'collective', 'force', 'moment'):
                bb, cb = loads_b[identifier][category], loads_c[identifier][category]
                if category == 'collective':
                    bb, cb = [bb], [cb]
                need(all(c[0] <= b[0] <= b[1] <= c[1] for b, c in zip(bb, cb)), 'C-vs-B-load-containment')
        need(all(bread(audit_c['maxErrors'][key])[1] >= bread(audit_b['maxErrors'][key])[1]
                 for key in CATEGORIES), 'C-vs-B-error-upper-order')
        diagnostics, omitted = [], set(mask)
        for identifier in ids:
            for rotor in range(4):
                terms = context['rows'][identifier, rotor]
                sources = {source for source, _ in terms if (identifier, rotor, source) in omitted}
                _, _, mass, weighted = contractions(terms, y, sources)
                diagnostics.append({'i': identifier, 'r': rotor, 'omittedCount': len(sources),
                                    'coefficientMass': bwire(mass), 'candidateWeightedMass': bwire(weighted)})
        exact(saved['omissionDiagnostics'], diagnostics, 'omission-all-row-masses')
        need(sum(row['omittedCount'] for row in diagnostics) == len(mask), 'omission-diagnostic-count-total')
        expected['omissionDiagnostics'] = diagnostics
    for audit in ('B', 'C') if label == 'omit10' else ('B',):
        need(all(bread(audit_a['maxErrors'][key])[0] <= bread(expected[audit]['maxErrors'][key])[1]
                 for key in CATEGORIES), 'A-vs-' + audit + '-error-consistency')
        for a_tier, proof_tier in zip(audit_a['tiers'], expected[audit]['tiers']):
            need(not (a_tier['overall'] == 'definite-fail' and proof_tier['overall'] == 'pass'),
                 'A-vs-' + audit + '-tier-consistency')
    return expected


def decision(outcomes):
    """No average, loose tier, or empty-positive state can override this order."""
    need(len(outcomes) == 6, 'decision-six-states')
    full_pass = all(row['full']['A']['tiers'][0]['overall'] == 'pass' for row in outcomes)
    if not full_pass:
        return 'full-control-inadequate-no-omission-attribution'
    if any(row['positiveTerms'] == 0 for row in outcomes):
        return 'zero-positive-state-no-nontrivial-all-six-advance'
    if any(row['omit10']['A']['tiers'][2]['overall'] == 'definite-fail' for row in outcomes):
        return 'fixed-route-stress-accuracy-definite-failure'
    if not all(row['omit10']['A']['tiers'][0]['overall'] == 'pass' for row in outcomes):
        return 'strict-accuracy-not-established-no-advance'
    if not all(row['omit10']['B']['tiers'][0]['overall'] == 'pass' for row in outcomes):
        return 'full-contraction-certificate-insufficient'
    if not all(row['omit10']['C']['tiers'][0]['overall'] == 'pass' for row in outcomes):
        return 'upper-only-omission-certificate-insufficient'
    return 'strict-headroom-only-separate-practical-experiment-required'


def check_config(config):
    exact(config['schema'], 'm31-direct-load-config-v1', 'config-schema')
    exact(config['states'], list(STATES), 'config-states')
    exact(config['prior'], PRIOR, 'config-prior')
    exact(config['constantBits'], CONSTANT_BITS, 'constant-identity')
    exact(config['constantProvenance'], CONSTANT_PROVENANCE, 'constant-provenance')
    exact(config['candidateIterations'], 48, 'config-iterations')
    exact(config['rootBisections'], 54, 'config-bisections')
    exact(config['sqrtFractionBits'], 192, 'config-sqrt-precision')
    exact(config['rootFractionBits'], 192, 'config-root-precision')
    exact(config['tiers'], list(TIERS), 'config-tiers')
    exact(config['mask'], {'fractionNumerator': 1, 'fractionDenominator': 10, 'rounding': 'ceiling',
          'order': ['coefficientUpper', 'receiverID', 'rotorIndex', 'sourceID']}, 'config-mask')


def fixtures(log):
    def case(name, condition):
        log.append({'name': name, 'passed': bool(condition)})
        need(condition, 'fixture:' + name)

    def rejects(function, code):
        try:
            function()
        except CheckError as exc:
            return str(exc) == code
        return False

    case('canonical-rational-rejection', rejects(lambda: qread({'n': '2', 'd': '4'}), 'rational-normalization'))
    case('integer-binary64-decoding', binary64('3ff0000000000000') == 1 and
         binary64('bfe0000000000000') == -Q(1, 2) and binary64('0000000000000001') == Q(1, 1 << 1074))
    case('candidate-hex-exact', candidate_hex('0x1.0000000000000p-1') == Q(1, 2))
    case('sqrt-zero-perfect-square', square_root(Q(0)) == (0, 0) and square_root(Q(9, 4)) == (Q(3, 2), Q(3, 2)))
    lower, upper = square_root(Q(2))
    case('irrational-sqrt-inclusion-width', lower**2 < 2 < upper**2 and upper-lower == Q(1, GRID))
    low, high = outward((Q(1, 3), Q(2, 3)))
    case('outward-root-grid-not-nearest', low <= Q(1, 3) <= Q(2, 3) <= high and
         Q(1, 3)-low < Q(1, GRID) and high-Q(2, 3) < Q(1, GRID))
    case('distance-not-reference-midpoint', distance((Q(1), Q(3)), Q(2)) == (0, 1) and distance((Q(1), Q(3)), Q(5)) == (2, 4))
    tau = Q('1e-8')
    case('A-exact-boundary-and-overlap', classify((tau, tau), tau) == 'pass' and
         classify((tau, tau+Q(1, GRID)), tau) == 'unresolved' and
         classify((tau+Q(1, GRID), tau+Q(2, GRID)), tau) == 'definite-fail')
    case('BC-upper-failure-is-not-inaccuracy', classify((Q(0), Q(1)), tau, True) == 'not-certified')
    case('signed-Euclidean-norm', norm_distance([(-Q(3), -Q(3)), (Q(4), Q(4)), (Q(0), Q(0))], [Q(0)]*3, Q(1)) == (5, 5))
    case('componentwise-small-is-not-norm-pass', classify(norm_distance([(Q(3, 5), Q(3, 5))]*3, [Q(0)]*3, Q(1)), Q(1)) == 'definite-fail')
    g = {'forces': [Q(1)]*4, 'axis': [Q(0), Q(0), -Q(1)],
         'levers': [(0,1,0), (0,-1,0), (-1,0,0), (1,0,0)], 'weights': [Q(1,4)]*4}
    point = point_loads(g, [Q(1,2)]*4)
    case('linear-rotor-not-squared-and-signed-force', point['rotor'] == [Q(1,2)]*4 and point['force'] == [0,0,-2] and point['moment'] == [0,0,0])
    bounds = loads(g, [(Q(0), Q(1))]*4)
    case('signed-moment-enclosure', bounds['moment'] == [(-1,1),(-1,1),(0,0)] and bounds['force'][2] == (-4,0))
    e = errors(bounds, point, Q(4), Q(2))
    case('rotor-mg-quarter-and-moment-mgR', e['rotor'] == (0,Q(1,2)) and e['worldMoment'][1] == square_root(Q(2))[1] / 8)
    coeff = {(50,0,j): (Q(0), Q(1)) for j in range(11,0,-1)}
    case('ceil-positive-count-zero-lower-ties', mask_for(coeff) == [(50,0,1),(50,0,2)])
    coeff = {(8,1,2):(Q(0),Q(1)), (8,0,9):(Q(0),Q(1)), (7,3,10):(Q(0),Q(1))}
    case('mask-receiver-rotor-source-ties', mask_for(coeff) == [(7,3,10)])
    full, partial, mass, weighted = contractions([(1,(Q(1),Q(2))), (2,(Q(3),Q(4)))],
        {1:(Q(1,2),Q(3,4)), 2:(Q(1,2),Q(3,4))}, {2})
    case('C-keeps-upper-and-removes-only-deleted-lower', full == (2,Q(9,2)) and partial == (Q(1,2),Q(9,2)) and mass == (3,4) and weighted == (Q(3,2),3))
    tiny_context = {'ids':[3], 'geometry':{3:g}, 'rows':{(3,r):[] for r in range(4)}}
    points = {3: point_loads(g, [Q(1,2),Q(1),Q(1),Q(1)])}
    proof, roots, _ = certificate(tiny_context, {3:[Q(1,2),Q(1),Q(1),Q(1)]}, points, {3:(Q(1),Q(1))}, [], 'B', Q(4), Q(1))
    case('one-bad-row-global-K-propagates', qread(proof['K']) == 8 and roots[3][1] == (Q(1,8),Q(1)))
    case('certificate-lower-errors-zero', all(bread(value)[0] == 0 for value in proof['maxErrors'].values()))
    coupled = {'ids':[10,20], 'geometry':{10:g,20:g},
        'rows':{(identifier,r):([] if identifier == 10 else [(10,(Q(7,4),Q(7,4)))])
                for identifier in (10,20) for r in range(4)}}
    coupled_x = {10:[Q(1)]*4,20:[Q(1,2)]*4}
    coupled_points = {identifier:point_loads(g,coupled_x[identifier]) for identifier in (10,20)}
    coupled_y = {10:(Q(1),Q(1)),20:square_root(Q(1,2))}
    coupled_proof, coupled_roots, _ = certificate(coupled,coupled_x,coupled_points,coupled_y,[],'B',Q(4),Q(1))
    case('nontrivial-coupled-chain-exact-certificate', qread(coupled_proof['K']) == 1 and
         all(bread(row['p']) == (1,1) and qread(row['k']) == 1 for row in coupled_proof['rows']) and
         coupled_roots[10] == [(1,1)]*4 and coupled_roots[20] == [(Q(1,2),Q(1,2))]*4 and
         all(bread(value) == (0,0) for value in coupled_proof['maxErrors'].values()))
    case('native-coupled-replay-full-versus-deletion',
         native_replay(coupled, []) == [{'id':10,'xHex':['0x1.0000000000000p+0']*4},
                                       {'id':20,'xHex':['0x1.0000000000000p-1']*4}] and
         native_replay(coupled, [(20,r,10) for r in range(4)]) ==
             [{'id':identifier,'xHex':['0x1.0000000000000p+0']*4} for identifier in (10,20)])
    expected_mask = mask_wire(mask_for({(1,0,2):(Q(0),Q(1))}))
    case('corrupt-mask-cardinality-rejected', rejects(lambda: check_mask([], {(1,0,2):(Q(0),Q(1))}), 'mask-ceiling-cardinality') and len(expected_mask) == 1)
    wrong = copy.deepcopy(proof)
    wrong['K'] = qwire(Q(1))
    case('corrupt-global-factor-rejected', rejects(lambda: check_certificate(wrong, proof, 'B'), 'B-global-factor'))
    wrong = copy.deepcopy(proof)
    wrong['rows'][0]['xstar'] = bwire((Q(1,2),Q(1,2)))
    case('corrupt-root-hull-rejected', rejects(lambda: check_certificate(wrong, proof, 'B'), 'B-root-corollary-grid'))
    ok = {'tiers':[{'overall':'pass'} for _ in TIERS]}
    outcomes = [{'positiveTerms':1,'full':{'A':copy.deepcopy(ok)},
                 'omit10':{k:copy.deepcopy(ok) for k in ('A','B','C')}} for _ in STATES]
    case('strict-all-six-headroom-only', decision(outcomes) == 'strict-headroom-only-separate-practical-experiment-required')
    outcomes[5]['full']['A']['tiers'][0]['overall'] = 'unresolved'
    outcomes[0]['omit10']['A']['tiers'][2]['overall'] = 'definite-fail'
    case('full-control-gate-precedes-omission-attribution', decision(outcomes) == 'full-control-inadequate-no-omission-attribution')
    outcomes[5]['full']['A']['tiers'][0]['overall'] = 'pass'
    case('stress-definite-failure-fixed-route-stop', decision(outcomes) == 'fixed-route-stress-accuracy-definite-failure')
    outcomes[0]['omit10']['A']['tiers'][2]['overall'] = 'pass'
    outcomes[5]['omit10']['A']['tiers'][0]['overall'] = 'unresolved'
    case('one-unresolved-state-blocks-strict-gate', decision(outcomes) == 'strict-accuracy-not-established-no-advance')
    outcomes[5]['omit10']['A']['tiers'][0]['overall'] = 'pass'
    outcomes[0]['positiveTerms'] = 0
    case('zero-positive-state-no-vacuous-advance', decision(outcomes) == 'zero-positive-state-no-nontrivial-all-six-advance')


def corruption_controls(saved_state, context, expected, log):
    saved = saved_state['proposals'][1]

    def control(name, value, mutate, validate, code):
        clone = copy.deepcopy(value)
        mutate(clone)
        failure = None
        try:
            validate(clone)
        except CheckError as exc:
            failure = str(exc)
        log.append({'name':name, 'expectedFailure':code, 'actualFailure':failure,
                    'rejected':failure is not None, 'intendedCoreFailure':failure == code})
        need(failure == code, 'corruption-control:' + name)

    control('mask-wrong-ceiling-cardinality', saved_state['mask'],
            lambda v: v.append({'i':context['ids'][0],'r':0,'j':context['ids'][1]}),
            lambda v: check_mask(v, context['coefficients']), 'mask-ceiling-cardinality')
    control('candidate-changed-after-audits', saved['candidate'],
            lambda v: v[0]['xHex'].__setitem__(0, '0x1.0000000000000p-1' if v[0]['xHex'][0] != '0x1.0000000000000p-1' else '0x1.0000000000000p-2'),
            lambda v: check_candidate(v, expected['candidate'], context['ids']), 'native-proposal-replay')
    control('candidate-load-not-induced-by-x', saved['candidateLoads'],
            lambda v: v[0]['loads']['rotor'].__setitem__(0, qwire(qread(v[0]['loads']['rotor'][0])+1)),
            lambda v: exact(v, expected['candidateLoads'], 'candidate-load-identity'), 'candidate-load-identity')
    control('incorrect-exact-weight-y', saved['sourceY'],
            lambda v: v[0].__setitem__('y', bwire((Q(0),Q(0)))),
            lambda v: exact(v, expected['sourceY'], 'exact-weight-candidate-y'), 'exact-weight-candidate-y')
    control('A-understated-or-shifted-error', saved['A'],
            lambda v: v['maxErrors'].__setitem__('rotor', bwire((Q(1),Q(1)))) if bread(v['maxErrors']['rotor']) != (1,1)
                      else v['maxErrors'].__setitem__('rotor', bwire((Q(0),Q(0)))),
            lambda v: check_summary(v, expected['A'], 'A'), 'A-error-intervals')
    control('A-wrong-threshold-decision', saved['A'],
            lambda v: v['tiers'][0].__setitem__('overall', 'unresolved' if v['tiers'][0]['overall'] == 'pass' else 'pass'),
            lambda v: check_summary(v, expected['A'], 'A'), 'A-tier-classification')
    control('B-incomplete-contraction', saved['B'],
            lambda v: v['rows'][0].__setitem__('s', bwire((Q(0), bread(v['rows'][0]['s'])[1]+1))),
            lambda v: check_certificate(v, expected['B'], 'B'), 'B-complete-contraction')
    control('B-understated-local-factor', saved['B'], lambda v: v['rows'][0].__setitem__('k', qwire(Q(0))),
            lambda v: check_certificate(v, expected['B'], 'B'), 'B-local-factor')
    control('B-understated-global-factor', saved['B'], lambda v: v.__setitem__('K', qwire(Q(0))),
            lambda v: check_certificate(v, expected['B'], 'B'), 'B-global-factor')
    control('B-narrow-root-corollary', saved['B'], lambda v: v['rows'][0].__setitem__('xstar', bwire((Q(0),Q(0)))),
            lambda v: check_certificate(v, expected['B'], 'B'), 'B-root-corollary-grid')
    control('C-wrong-contraction-upper', saved['C'],
            lambda v: v['rows'][0].__setitem__('s', bwire((Q(0), bread(v['rows'][0]['s'])[1]+1))),
            lambda v: check_certificate(v, expected['C'], 'C'), 'C-complete-contraction')
    control('C-mislabeled-inaccuracy', saved['C'],
            lambda v: v['tiers'][0].__setitem__('overall', 'definite-fail'),
            lambda v: check_certificate(v, expected['C'], 'C'), 'C-tier-classification')
    control('omission-mass-not-candidate-dependent', saved['omissionDiagnostics'],
            lambda v: v[0].__setitem__('candidateWeightedMass', bwire((Q(0), bread(v[0]['candidateWeightedMass'])[1]+1))),
            lambda v: exact(v, expected['omissionDiagnostics'], 'omission-all-row-masses'), 'omission-all-row-masses')


def run(root, config=None, analysis_path=None):
    """Dispatcher-compatible; optional paths exist for source integration only."""
    report = {'schema':'m31-direct-load-independent-check-v1', 'passed':False, 'firstFailure':None,
        'fixtures':[], 'corruptionControls':[], 'inputPins':[], 'outcomes':[], 'decision':None,
        'verified':{'states':0,'proposals':0,'candidateRotors':0,'referencePairs':0,'A':0,'B':0,'C':0,'certificateRows':0,'omissionDiagnosticRows':0},
        'scope':'Independent saved oracle-assisted accuracy diagnostic; no fresh flight, physical truth, speed or Q-current interface claim.'}
    stage = 'literal-fixtures-before-target-reads'
    try:
        fixtures(report['fixtures'])
        root = Path(root).resolve()
        package = Path(__file__).resolve().parents[1]
        stage = 'fixed-configuration'
        if config is None:
            config, _ = read_json(root, Path(__file__).resolve().with_name('config.json'), report['inputPins'])
        check_config(config)
        stage = 'constant-provenance'
        index, pin = read_json(root, CONSTANT_PROVENANCE['path'], report['inputPins'])
        exact(pin['sha256'], CONSTANT_PROVENANCE['sha256'], 'constant-index-file-binding')
        exact({key:index['constants'][key] for key in ('mg','R')}, CONSTANT_BITS, 'constant-index-values')
        mg, radius = binary64(CONSTANT_BITS['mg']), binary64(CONSTANT_BITS['R'])
        stage = 'saved-producer-record'
        document, _ = read_json(root, analysis_path or package / 'results/analyze.json', report['inputPins'])
        fields(document, ('schema','scope','constantBits','constantProvenance','arithmetic','tiers','primaryTier',
                          'interpretation','fixtures','states','proposalCount'), 'analysis-shape')
        exact(document['schema'], 'm31-direct-load-diagnostic-v1', 'analysis-schema')
        exact(document['scope'], 'Oracle-assisted exposed-state accuracy diagnostic; no speed or Q-current interface claim', 'analysis-scope')
        exact(document['constantBits'], CONSTANT_BITS, 'constant-identity')
        exact(document['constantProvenance'], CONSTANT_PROVENANCE, 'constant-provenance')
        exact(document['arithmetic'], ARITHMETIC, 'analysis-arithmetic-contract')
        exact(document['tiers'], list(TIERS), 'analysis-tiers')
        exact(document['primaryTier'], '1e-8', 'analysis-primary-tier')
        exact(document['interpretation'], 'Independent checker applies full-control A strict gate after all 12 proposals; looser tiers are diagnostics only', 'analysis-interpretation')
        exact(document['fixtures'], [{'name':name,'passed':True} for name in PRODUCER_FIXTURES], 'producer-fixtures')
        exact(document['proposalCount'], 12, 'twelve-proposals-required')
        need(type(document['states']) is list and len(document['states']) == 6, 'six-states-required')
        first = None
        for state_index, name in enumerate(STATES):
            stage = name
            context = source_context(root, name, report['inputPins'])
            saved = document['states'][state_index]
            fields(saved, ('id','inputSha256','inputFile','referenceFile','positiveTerms','maskRule','mask','proposals'), 'state-shape')
            exact(saved['id'], name, 'state-identity')
            for field in ('inputSha256','inputFile','referenceFile'):
                exact(saved[field], context[field], 'state-' + field + '-binding')
            exact(saved['positiveTerms'], len(context['coefficients']), 'state-positive-denominator')
            exact(saved['maskRule'], MASK_RULE, 'state-mask-rule')
            check_mask(saved['mask'], context['coefficients'])
            mask = mask_for(context['coefficients'])
            need(type(saved['proposals']) is list and len(saved['proposals']) == 2, 'two-proposals-per-state')
            outcome = {'id':name,'positiveTerms':len(context['coefficients']),'omittedCount':len(mask)}
            for proposal, label, selected in zip(saved['proposals'], ('full','omit10'), ([],mask)):
                expected = check_proposal(proposal, context, label, selected, mg, radius)
                outcome[label] = {audit:{key:expected[audit][key] for key in ('maxErrors','tiers')}
                                  for audit in ('A','B','C') if audit in expected}
                report['verified']['proposals'] += 1
                report['verified']['candidateRotors'] += 256
                report['verified']['A'] += 1
                report['verified']['B'] += 1
                report['verified']['certificateRows'] += 256
                if label == 'omit10':
                    report['verified']['C'] += 1
                    report['verified']['certificateRows'] += 256
                    report['verified']['omissionDiagnosticRows'] += 256
                    if state_index == 0:
                        first = (saved, context, expected)
            report['outcomes'].append(outcome)
            report['verified']['states'] += 1
            report['verified']['referencePairs'] += 16128
            del context, expected
        stage = 'saved-record-corruption-controls'
        corruption_controls(*first, report['corruptionControls'])
        exact(report['verified'], {'states':6,'proposals':12,'candidateRotors':3072,'referencePairs':96768,
             'A':12,'B':12,'C':6,'certificateRows':4608,'omissionDiagnosticRows':1536}, 'complete-audit-counts')
        report['decision'] = decision(report['outcomes'])
        report['fullControlStrictPass'] = all(row['full']['A']['tiers'][0]['overall'] == 'pass' for row in report['outcomes'])
        report['allSixStrictHeadroom'] = report['decision'] == 'strict-headroom-only-separate-practical-experiment-required'
        report['passed'] = True  # Record validity is separate from scientific headroom.
    except Exception as exc:
        report['firstFailure'] = {'stage':stage,'type':type(exc).__name__,
            'code':str(exc)[:256] if isinstance(exc, CheckError) else 'checker-internal:' + type(exc).__name__}
    return report
