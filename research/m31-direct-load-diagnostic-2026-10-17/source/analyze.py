"""Fixed oracle-assisted load diagnostic; stdlib only; proposal is not a proof.

Source preparation only until separately frozen and allocated. A bounded external
dispatcher must verify all pins before calling run(root, config=None), serialize
the returned object, and apply its declared time/output/RSS acceptance gates.
This module has no main routine and imports no simulator or prior checker.
"""
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import struct

STATES = ('run-a-t0', 'run-a-t5', 'run-a-t10',
          'run-b-t0', 'run-b-t5', 'run-b-t10')
TIERS = ('1e-8', '1e-4', '1e-2')
CATEGORIES = ('rotor', 'collective', 'worldForce', 'worldMoment')
PRIOR = 'research/m31-normalizer-replication-2026-10-17/results'
BITS = 192
SCALE = 1 << BITS
ITERATIONS = 48
BISECTIONS = 54
ZERO = F(0)
ONE = F(1)
CONSTANT_BITS = {'mg': '3fd0f3a14cec41dd', 'R': '3fa4462fb7ff5035'}
CONSTANT_PROVENANCE = {
    'path': PRIOR + '/index.json',
    'sha256': '3e9793e26a9a59803aa1056098e7c0f1e500ade02fd0928a171a5dc187ac7393'}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def read_json(path):
    raw = path.read_bytes()
    return json.loads(raw, object_pairs_hook=no_duplicates), {
        'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def qread(value):
    need(type(value) is dict and set(value) == {'n', 'd'}, 'rational-shape')
    need(all(type(value[k]) is str and
             re.fullmatch(r'0|-?[1-9][0-9]*', value[k]) is not None
             for k in ('n', 'd')), 'rational-text')
    n, d = int(value['n']), int(value['d'])
    need(d > 0, 'rational-denominator')
    q = F(n, d)
    need(q.numerator == n and q.denominator == d, 'rational-reduced')
    return q


def bread(value):
    need(type(value) is dict and set(value) == {'l', 'u'}, 'interval-shape')
    lo, hi = qread(value['l']), qread(value['u'])
    need(lo <= hi, 'interval-order')
    return lo, hi


def qwire(q):
    return {'n': str(q.numerator), 'd': str(q.denominator)}


def bwire(box):
    return {'l': qwire(box[0]), 'u': qwire(box[1])}


def number(word):
    need(type(word) is str and re.fullmatch(r'[0-9a-f]{16}', word) is not None,
         'binary64-word')
    value = struct.unpack('>d', bytes.fromhex(word))[0]
    need(math.isfinite(value), 'binary64-finite')
    return value


def dyadic(word):
    return F.from_float(number(word))


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def scaled(a, q):
    lo, hi = a[0] * q, a[1] * q
    return (lo, hi) if q >= 0 else (hi, lo)


def positive_product(a, b):
    need(a[0] >= 0 and b[0] >= 0, 'nonnegative-product-domain')
    return a[0] * b[0], a[1] * b[1]


def sum_boxes(values):
    lo, hi = ZERO, ZERO
    for a, b in values:
        lo += a
        hi += b
    return lo, hi


def sqrt_point(q):
    """Enclose sqrt(q) on the fixed 2^-192 absolute grid, without floats."""
    need(q >= 0, 'sqrt-domain')
    numerator = q.numerator * SCALE * SCALE
    k = math.isqrt(numerator // q.denominator)
    upper = k if k * k * q.denominator == numerator else k + 1
    return F(k, SCALE), F(upper, SCALE)


def sqrt_box(box):
    need(0 <= box[0] <= box[1], 'sqrt-box-domain')
    return sqrt_point(box[0])[0], sqrt_point(box[1])[1]


def outward_root_grid(box):
    """Round only root endpoints outward to the fixed 2^-192 grid."""
    lower, upper = box[0] * SCALE, box[1] * SCALE
    return (F(lower.numerator // lower.denominator, SCALE),
            F(-((-upper.numerator) // upper.denominator), SCALE))


def cross(a, b):
    return tuple(a[(k+1) % 3] * b[(k+2) % 3] -
                 a[(k+2) % 3] * b[(k+1) % 3] for k in range(3))


def exact_geometry(value):
    need(len(value['forces']) == 4 and len(value['axis']) == 3 and
         len(value['offsets']) == 4 and all(len(v) == 3 for v in value['offsets']),
         'prepared-vector-shape')
    forces = tuple(dyadic(v) for v in value['forces'])
    need(all(v > 0 for v in forces), 'positive-nominal-forces')
    axis = tuple(dyadic(v) for v in value['axis'])
    offsets = [tuple(dyadic(v) for v in row) for row in value['offsets']]
    total = sum(forces, ZERO)
    return {'forces': forces, 'axis': axis,
            'levers': tuple(cross(offset, axis) for offset in offsets),
            'weights': tuple(v / total for v in forces)}


def load_boxes(geometry, roots):
    rotor = [scaled(roots[r], geometry['forces'][r]) for r in range(4)]
    collective = sum_boxes(rotor)
    force = [scaled(collective, a) for a in geometry['axis']]
    moment = [sum_boxes(scaled(rotor[r], geometry['levers'][r][k])
                        for r in range(4)) for k in range(3)]
    return {'rotor': rotor, 'collective': collective,
            'force': force, 'moment': moment}


def point_loads(geometry, candidate):
    boxes = load_boxes(geometry, [(x, x) for x in candidate])
    need(all(lo == hi for key in ('rotor', 'force', 'moment')
             for lo, hi in boxes[key]) and
         boxes['collective'][0] == boxes['collective'][1], 'point-load-identity')
    return {key: boxes[key][0] if key == 'collective' else
            [v[0] for v in boxes[key]] for key in boxes}


def point_wire(load):
    return {key: qwire(value) if key == 'collective' else
            [qwire(q) for q in value] for key, value in load.items()}


def absolute_distance(box, point):
    lo, hi = box
    if point < lo:
        return lo - point, hi - point
    if point > hi:
        return point - hi, point - lo
    return ZERO, max(point - lo, hi - point)


def scalar_error(box, point, scale):
    need(scale > 0, 'positive-error-scale')
    return scaled(absolute_distance(box, point), ONE / scale)


def norm_error(boxes, points, scale):
    need(len(boxes) == len(points) == 3 and scale > 0, 'norm-error-domain')
    distances = [absolute_distance(box, point) for box, point in zip(boxes, points)]
    squared = (sum((v[0] * v[0] for v in distances), ZERO),
               sum((v[1] * v[1] for v in distances), ZERO))
    return scaled(sqrt_box(squared), ONE / scale)


def max_box(boxes):
    values = list(boxes)
    need(bool(values), 'empty-maximum')
    return max(v[0] for v in values), max(v[1] for v in values)


def load_errors(boxes, point, mg, radius):
    return {
        'rotor': max_box(scalar_error(boxes['rotor'][r], point['rotor'][r], mg / 4)
                         for r in range(4)),
        'collective': scalar_error(boxes['collective'], point['collective'], mg),
        'worldForce': norm_error(boxes['force'], point['force'], mg),
        'worldMoment': norm_error(boxes['moment'], point['moment'], mg * radius)}


def tier_status(box, tolerance):
    if box[1] <= tolerance:
        return 'pass'
    if box[0] > tolerance:
        return 'definite-fail'
    return 'unresolved'


def audit_summary(errors, audit):
    need(audit in ('A', 'B', 'C'), 'audit-summary-kind')
    maximum = {category: max_box(row[category] for row in errors)
               for category in CATEGORIES}
    tiers = []
    for tier in TIERS:
        if audit == 'A':
            categories = {category: tier_status(maximum[category], F(tier))
                          for category in CATEGORIES}
            overall = ('pass' if all(v == 'pass' for v in categories.values()) else
                       'definite-fail' if 'definite-fail' in categories.values() else
                       'unresolved')
        else:
            categories = {category: ('pass' if maximum[category][1] <= F(tier)
                                     else 'not-certified') for category in CATEGORIES}
            overall = ('pass' if all(v == 'pass' for v in categories.values())
                       else 'not-certified')
        tiers.append({'tier': tier, 'categories': categories, 'overall': overall})
    return {'maxErrors': {key: bwire(value) for key, value in maximum.items()},
            'tiers': tiers}


def native_cubic(alpha):
    """Exactly 54 binary64 bisections; no residual or tolerance stopping."""
    lo, hi = 0.0, 1.0
    for _ in range(BISECTIONS):
        mid = (lo + hi) / 2.0
        if mid * mid * mid + alpha * mid > 1.0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def native_proposal(ids, prepared, rows, omitted):
    """Python FP64 proposal; explicit left-to-right reductions, no math.fsum."""
    weights = {}
    for i in ids:
        forces = [number(v) for v in prepared[i]['forces']]
        total = 0.0
        for force in forces:
            total = total + force
        need(math.isfinite(total) and total > 0.0, 'native-force-total')
        weights[i] = [force / total for force in forces]
    terms = {}
    for i in ids:
        for r in range(4):
            terms[i, r] = []
            for j, coefficient in rows[i, r]:
                if (i, r, j) not in omitted:
                    midpoint = float((coefficient[0] + coefficient[1]) / 2)
                    need(math.isfinite(midpoint) and midpoint >= 0.0,
                         'native-coefficient-midpoint')
                    terms[i, r].append((j, midpoint))
    candidate = {i: [1.0, 1.0, 1.0, 1.0] for i in ids}
    for _ in range(ITERATIONS):
        y = {}
        for i in ids:
            total = 0.0
            for r in range(4):
                total = total + weights[i][r] * candidate[i][r]
            y[i] = math.sqrt(total)
        following = {}
        for i in ids:
            following[i] = []
            for r in range(4):
                alpha = 0.0
                for j, midpoint in terms[i, r]:
                    alpha = alpha + midpoint * y[j]
                need(math.isfinite(alpha) and alpha >= 0.0, 'native-alpha-domain')
                following[i].append(native_cubic(alpha))
        candidate = following
    need(all(math.isfinite(v) and 0.0 < v <= 1.0
             for row in candidate.values() for v in row), 'native-candidate-domain')
    return candidate


def source_y(ids, geometry, candidate):
    return {i: sqrt_point(sum((geometry[i]['weights'][r] * candidate[i][r]
                               for r in range(4)), ZERO)) for i in ids}


def contraction(terms, y, omitted_sources):
    kept, dropped, mass = [], [], []
    for j, coefficient in terms:
        contribution = positive_product(coefficient, y[j])
        if j in omitted_sources:
            dropped.append(contribution)
            mass.append(coefficient)
        else:
            kept.append(contribution)
    retained, omitted = sum_boxes(kept), sum_boxes(dropped)
    full = plus(retained, omitted)
    upper_only = plus(retained, (ZERO, omitted[1]))
    return full, upper_only, sum_boxes(mass), omitted


def current_certificate(ids, geometry, rows, candidate, point, y, omitted, mode,
                        mg, radius):
    need(mode in ('B', 'C'), 'certificate-mode')
    proof = []
    global_k = ONE
    for i in ids:
        for r in range(4):
            omitted_sources = {j for j, _ in rows[i, r] if (i, r, j) in omitted}
            full, upper_only, _, _ = contraction(rows[i, r], y, omitted_sources)
            s = full if mode == 'B' else upper_only
            x = candidate[i][r]
            p = (x * x * x + x * s[0], x * x * x + x * s[1])
            need(p[0] > 0, 'positive-defect-lower')
            k = max(ONE, p[1], ONE / p[0])
            global_k = max(global_k, k)
            proof.append({'i': i, 'r': r, 's': s, 'p': p, 'k': k})
    roots = {i: [None] * 4 for i in ids}
    for row in proof:
        x = candidate[row['i']][row['r']]
        factor = row['k'] * global_k
        raw_root = (x / factor, min(ONE, x * factor))
        root = outward_root_grid(raw_root)
        need(0 <= root[0] <= raw_root[0] <= x <= raw_root[1] <= root[1] <= 1,
             'root-box-domain')
        roots[row['i']][row['r']] = root
        row['xstar'] = root
    errors = [load_errors(load_boxes(geometry[i], roots[i]), point[i], mg, radius)
              for i in ids]
    return {'rows': [{'i': row['i'], 'r': row['r'], 's': bwire(row['s']),
                      'p': bwire(row['p']), 'k': qwire(row['k']),
                      'xstar': bwire(row['xstar'])} for row in proof],
            'K': qwire(global_k), **audit_summary(errors, mode)}


def omission_mask(coefficients):
    ordered = sorted(coefficients, key=lambda key: (coefficients[key][1], *key))
    return ordered[:(len(ordered) + 9) // 10]


def fixtures():
    """Fixed analytic controls; no target files, numerical search, or tuning."""
    results = []

    def case(name, condition):
        need(condition, 'fixture:' + name)
        results.append({'name': name, 'passed': True})

    case('sqrt-one-exact', sqrt_point(ONE) == (ONE, ONE))
    lo, hi = sqrt_point(F(2))
    case('sqrt-two-fixed192', lo * lo <= 2 <= hi * hi and hi - lo == F(1, SCALE))
    grid = outward_root_grid((F(1, 3), F(2, 3)))
    case('root-grid-outward-nondyadic',
         grid[0] <= F(1, 3) <= F(2, 3) <= grid[1] and
         F(1, 3) - grid[0] < F(1, SCALE) and grid[1] - F(2, 3) < F(1, SCALE))
    case('root-grid-exact-boundaries',
         outward_root_grid((ZERO, ONE)) == (ZERO, ONE))
    case('cubic-alpha-zero', native_cubic(0.0) == 1.0)
    case('cubic-alpha-seven-fourths', native_cubic(1.75) == 0.5)
    g = {'forces': (ONE,) * 4, 'axis': (ZERO, ZERO, -ONE),
         'weights': (F(1, 10), F(2, 10), F(3, 10), F(4, 10)),
         'levers': tuple(cross(offset, (ZERO, ZERO, -ONE)) for offset in
                         ((ONE, ZERO, ZERO), (-ONE, ZERO, ZERO),
                          (ZERO, ONE, ZERO), (ZERO, -ONE, ZERO)))}
    case('candidate-y-one', source_y([7], {7: g}, {7: [ONE] * 4})[7] == (ONE, ONE))
    load = point_loads(g, [F(1, 2)] * 4)
    case('signed-cancellation-and-linear-rotor-load',
         load == {'rotor': [F(1, 2)] * 4, 'collective': F(2),
                  'force': [ZERO, ZERO, F(-2)], 'moment': [ZERO] * 3})
    boxes = load_boxes(g, [(ZERO, ONE)] * 4)
    case('signed-load-boxes', boxes['moment'] == [(-ONE, ONE), (-ONE, ONE), (ZERO, ZERO)]
         and boxes['force'] == [(ZERO, ZERO), (ZERO, ZERO), (F(-4), ZERO)])
    full, upper_only, mass, weighted = contraction(
        [(1, (ONE, F(2))), (2, (F(3), F(4)))],
        {1: (F(1, 2), F(3, 4)), 2: (F(1, 2), F(3, 4))}, {2})
    case('upper-only-contraction-contains-full',
         full == (F(2), F(9, 2)) and upper_only == (F(1, 2), F(9, 2)) and
         mass == (F(3), F(4)) and weighted == (F(3, 2), F(3)) and
         upper_only[0] <= full[0] <= full[1] <= upper_only[1])
    tau, epsilon = F('1e-8'), F(1, SCALE)
    boundary = scalar_error((tau, tau), ZERO, ONE)
    case('exact-error-boundary-pass', boundary == (tau, tau) and
         tier_status(boundary, tau) == 'pass')
    case('exact-error-boundary-fail',
         tier_status((tau + epsilon, tau + epsilon), tau) == 'definite-fail')
    case('exact-error-boundary-overlap',
         tier_status((tau - epsilon, tau + epsilon), tau) == 'unresolved')
    case('signed-euclidean-three-four-five',
         norm_error([(F(-3), F(-3)), (F(4), F(4)), (ZERO, ZERO)],
                    [ZERO] * 3, ONE) == (F(5), F(5)))
    coefficients = {(90, 0, j): (ZERO, ONE) for j in range(11, 0, -1)}
    case('ceil-ten-percent-upper-tie-zero-lower',
         omission_mask(coefficients) == [(90, 0, 1), (90, 0, 2)])
    return results


def load_state(root, name):
    relative_input = PRIOR + '/inputs/' + name + '.json'
    relative_reference = PRIOR + '/reference/' + name + '.json'
    inp, input_pin = read_json(root / relative_input)
    reference, reference_pin = read_json(root / relative_reference)
    need(reference['schema'] == 'm31-normalizer-ablation-reference-v1' and
         reference['id'] == name and reference['referenceStatus'] == 'admitted',
         'reference-identity-admission')
    envelope = {'domain': 'm31-moving-admission/input/v1', 'id': name, 'input': inp}
    digest = hashlib.sha256(json.dumps(envelope, sort_keys=True,
                                      separators=(',', ':')).encode()).hexdigest()
    need(reference['inputSha256'] == digest, 'reference-input-binding')
    ids = [d['id'] for d in inp['drones']]
    need(len(ids) == 64 and all(type(i) is int and 0 <= i <= 65535 for i in ids) and
         len(set(ids)) == len(ids), 'state-id-domain')
    need([d['id'] for d in reference['prepared']] == ids and
         all(d['rejection'] is None for d in reference['prepared']), 'prepared-id-admission')
    prepared = {d['id']: d['value'] for d in reference['prepared']}
    for drone in inp['drones']:
        need(len(drone['state']) == 17 and
             prepared[drone['id']]['forces'] == drone['state'][13:17] and
             prepared[drone['id']]['center'] == drone['state'][:3],
             'prepared-raw-force-center-binding')
    geometry = {i: exact_geometry(prepared[i]) for i in ids}
    lookup, coefficients = {}, {}
    for pair in reference['pairs']:
        key = pair['i'], pair['r'], pair['j']
        i, r, j = key
        need(type(i) is int and type(r) is int and type(j) is int and
             i in prepared and j in prepared and i != j and 0 <= r < 4 and
             key not in lookup, 'pair-key-domain-uniqueness')
        if pair['status'] == 'zero':
            need('coefficient' not in pair, 'zero-has-coefficient')
            lookup[key] = None
        else:
            need(pair['status'] == 'positive', 'pair-status')
            coefficient = bread(pair['coefficient'])
            need(0 <= coefficient[0] <= coefficient[1] and coefficient[1] > 0 and
                 all((q * SCALE).denominator == 1 for q in coefficient),
                 'positive-fixed192-coefficient')
            lookup[key] = coefficient
            coefficients[key] = coefficient
    need(len(lookup) == 4 * 64 * 63 == reference['evaluatedPairs'] ==
         reference['plannedPairs'], 'complete-reference-pairs')
    need(len(coefficients) == reference['graph']['positiveRotorPairs'],
         'positive-term-denominator')
    # Freeze accumulation in input source order. No geometric traversal order.
    rows = {(i, r): [(j, coefficients[i, r, j]) for j in ids
                     if (i, r, j) in coefficients] for i in ids for r in range(4)}
    need([v['id'] for v in reference['loads']] == ids, 'reference-load-order')
    reference_loads = {}
    for entry in reference['loads']:
        boxes = entry['loads']
        need(set(boxes) == {'rotor', 'collective', 'force', 'moment'} and
             len(boxes['rotor']) == 4 and len(boxes['force']) == len(boxes['moment']) == 3,
             'reference-load-shape')
        reference_loads[entry['id']] = {
            key: bread(value) if key == 'collective' else [bread(v) for v in value]
            for key, value in boxes.items()}
    return {'id': name, 'ids': ids, 'prepared': prepared, 'geometry': geometry,
            'rows': rows, 'coefficients': coefficients, 'referenceLoads': reference_loads,
            'inputSha256': digest,
            'inputFile': {'path': relative_input, **input_pin},
            'referenceFile': {'path': relative_reference, **reference_pin}}


def produce_proposal(state, label, mask, mg, radius):
    ids, geometry = state['ids'], state['geometry']
    native = native_proposal(ids, state['prepared'], state['rows'], set(mask))
    exact = {i: [F.from_float(v) for v in native[i]] for i in ids}
    point = {i: point_loads(geometry[i], exact[i]) for i in ids}
    y = source_y(ids, geometry, exact)
    errors = [load_errors(state['referenceLoads'][i], point[i], mg, radius) for i in ids]
    proposal = {
        'id': label, 'omittedCount': len(mask),
        'candidate': [{'id': i, 'xHex': [v.hex() for v in native[i]]} for i in ids],
        'candidateLoads': [{'id': i, 'loads': point_wire(point[i])} for i in ids],
        'sourceY': [{'id': i, 'y': bwire(y[i])} for i in ids],
        'A': audit_summary(errors, 'A'),
        'B': current_certificate(ids, geometry, state['rows'], exact, point, y,
                                 set(mask), 'B', mg, radius)}
    if label == 'omit10':
        proposal['C'] = current_certificate(ids, geometry, state['rows'], exact, point, y,
                                            set(mask), 'C', mg, radius)
        diagnostics = []
        omitted = set(mask)
        for i in ids:
            for r in range(4):
                sources = {j for j, _ in state['rows'][i, r] if (i, r, j) in omitted}
                _, _, mass, weighted = contraction(state['rows'][i, r], y, sources)
                diagnostics.append({'i': i, 'r': r, 'omittedCount': len(sources),
                                    'coefficientMass': bwire(mass),
                                    'candidateWeightedMass': bwire(weighted)})
        proposal['omissionDiagnostics'] = diagnostics
    return proposal


def run(root, config=None):
    """Called only by a separately authorized, pin-verifying resource dispatcher."""
    root = Path(root)
    if config is None:
        config, _ = read_json(Path(__file__).with_name('config.json'))
    need(config['schema'] == 'm31-direct-load-config-v1' and
         config['constantBits'] == CONSTANT_BITS, 'configuration-constants')
    need(config['constantProvenance'] == CONSTANT_PROVENANCE,
         'constant-provenance-required')
    need(config['states'] == list(STATES) and config['prior'] == PRIOR and
         type(config['candidateIterations']) is int and config['candidateIterations'] == ITERATIONS and
         type(config['rootBisections']) is int and config['rootBisections'] == BISECTIONS and
         config['tiers'] == list(TIERS) and
         type(config['sqrtFractionBits']) is int and config['sqrtFractionBits'] == BITS and
         type(config['rootFractionBits']) is int and config['rootFractionBits'] == BITS,
         'fixed-scientific-configuration')
    need(config['mask'] == {'fractionNumerator': 1, 'fractionDenominator': 10,
                           'rounding': 'ceiling',
                           'order': ['coefficientUpper', 'receiverID', 'rotorIndex', 'sourceID']}
         and type(config['mask']['fractionNumerator']) is int and
         type(config['mask']['fractionDenominator']) is int, 'fixed-mask-configuration')
    mg, radius = (dyadic(config['constantBits'][k]) for k in ('mg', 'R'))
    need(mg > 0 and radius > 0, 'normalization-constants-positive')
    output = {
        'schema': 'm31-direct-load-diagnostic-v1',
        'scope': 'Oracle-assisted exposed-state accuracy diagnostic; no speed or Q-current interface claim',
        'constantBits': config['constantBits'], 'constantProvenance': config['constantProvenance'],
        'arithmetic': {'proposal': 'Python FP64, explicit left-to-right sums, no fused operations',
                       'coefficientConversion': 'float of exact rational endpoint midpoint',
                       'termOrder': 'input source order within each receiver and rotor',
                       'initialCandidate': 'all ones', 'iterations': ITERATIONS,
                       'cubicBisections': BISECTIONS, 'sqrtFractionBits': BITS,
                       'rootFractionBits': BITS,
                       'certificate': 'exact rational operations; sqrt fixed192 enclosure and roots outward fixed192 grid'},
        'tiers': list(TIERS), 'primaryTier': '1e-8',
        'interpretation': 'Independent checker applies full-control A strict gate after all 12 proposals; looser tiers are diagnostics only',
        'fixtures': fixtures(), 'states': [], 'proposalCount': 0}
    for name in STATES:
        state = load_state(root, name)
        mask = omission_mask(state['coefficients'])
        record = {'id': name, 'inputSha256': state['inputSha256'],
                  'inputFile': state['inputFile'], 'referenceFile': state['referenceFile'],
                  'positiveTerms': len(state['coefficients']),
                  'maskRule': 'ceil(P/10), coefficient upper ascending then stable (i,r,j)',
                  'mask': [{'i': i, 'r': r, 'j': j} for i, r, j in mask],
                  'proposals': []}
        # Audit outcomes never truncate, tune, or otherwise alter this schedule.
        for label, selected in (('full', []), ('omit10', mask)):
            record['proposals'].append(produce_proposal(state, label, selected, mg, radius))
            output['proposalCount'] += 1
        output['states'].append(record)
    need(output['proposalCount'] == 12, 'fixed-twelve-proposals')
    return output
