#!/usr/bin/env python3
"""Independent coupled-load saved-result checker; source-authored, not pre-run.

The byte-identical published pair reference is loaded only by main after local
manifest verification. Its old case generator/main/controls are never invoked.
No candidate implementation, child process or network operation is used.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import types
import json
from math import isqrt
from pathlib import Path, PurePosixPath
import re
import sys

MAX_INPUT_BYTES = 32 * 1024 * 1024
MAX_REPORT_BYTES = MAX_INPUT_BYTES - 65536
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_SPEC_BYTES = 256 * 1024
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_SOURCE_TOTAL = 64 * 1024 * 1024
MAX_SOURCE_FILES = 256
MAX_ERRORS = 48

class CheckError(Exception):
    """An intentionally public-safe validation failure."""


def require(condition, code):
    if not condition:
        raise CheckError(code)


def canonical_integer(value):
    require(isinstance(value, str) and len(value) <= 128,
            "endpoint-string-shape")
    require(re.fullmatch(r"0|-?[1-9][0-9]*", value) is not None,
            "endpoint-string-syntax")
    return int(value)


def pairs_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate-json-key")
        result[key] = value
    return result


def reject_json_constant(_value):
    raise CheckError("nonfinite-json-number")


def same_json(left, right):
    """Structural equality without Python's True == 1 or 1.0 == 1 aliases."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_json(a, b) for a, b in zip(left, right))
    return left == right


def load_json(path, limit):
    require(path.is_file(), "required-file-missing")
    require(path.stat().st_size <= limit, "input-file-budget")
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    require(len(data) <= limit, "input-file-budget")
    try:
        return json.loads(data, object_pairs_hook=pairs_without_duplicates,
                          parse_constant=reject_json_constant)
    except (UnicodeError, ValueError, RecursionError):
        raise CheckError("invalid-json") from None


def relative_name(path, root):
    try:
        relative = path.resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        raise CheckError("input-path-outside-root-or-missing") from None
    require(relative.parts and not any(p in (".", "..") for p in relative.parts),
            "invalid-relative-path")
    return relative.as_posix()


def file_sha256(path, limit=MAX_SOURCE_BYTES):
    h = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            total += len(block)
            require(total <= limit, "source-file-budget")
            h.update(block)
    return total, h.hexdigest()


def verify_manifest(manifest_path, root, spec_path, contract_path):
    manifest = load_json(manifest_path, MAX_MANIFEST_BYTES)
    require(isinstance(manifest, dict), "manifest-object-required")
    files = manifest.get("files")
    require(isinstance(files, list) and 1 <= len(files) <= MAX_SOURCE_FILES,
            "manifest-file-count")
    seen = set()
    verified = []
    total = 0
    for item in files:
        require(isinstance(item, dict), "manifest-record-object")
        name = item.get("path")
        require(isinstance(name, str) and len(name) <= 512 and "\\" not in name,
                "manifest-path-shape")
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and str(parts) == name and
                all(part not in (".", "..") for part in parts.parts),
                "manifest-path-not-relative")
        require(name not in seen, "duplicate-manifest-path")
        seen.add(name)
        size = item.get("bytes")
        expected_sha = item.get("sha256")
        require(type(size) is int and 0 <= size <= MAX_SOURCE_BYTES,
                "manifest-size-shape")
        require(isinstance(expected_sha, str) and
                re.fullmatch(r"[0-9a-f]{64}", expected_sha) is not None,
                "manifest-hash-shape")
        source_path = root / name
        require(relative_name(source_path, root) == name,
                "manifest-noncanonical-file-path")
        actual_size, actual_sha = file_sha256(source_path)
        total += actual_size
        require(total <= MAX_SOURCE_TOTAL, "source-total-budget")
        require(actual_size == size and actual_sha == expected_sha,
                "source-manifest-pin-mismatch")
        verified.append({"path": name, "bytes": size, "sha256": actual_sha})
    require(relative_name(spec_path, root) in seen, "spec-not-source-pinned")
    require(relative_name(contract_path, root) in seen,
            "result-contract-not-source-pinned")
    require(relative_name(Path(__file__), root) in seen,
            "checker-not-source-pinned")
    return verified


class PublicArgumentParser(argparse.ArgumentParser):
    def error(self, _message):
        raise CheckError("invalid-command-line")


SCALE = 1 << 96
CATEGORIES = ('rotor', 'collective', 'worldForce', 'worldMoment')
CONTROL_NAMES = ['missing-positive-pair', 'false-root-one', 'altered-candidate',
                 'false-error-zero', 'altered-lever-arm', 'altered-stable-id',
                 'missing-scene', 'duplicate-scene', 'reordered-scenes']
HELPER_SHA256 = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'


class Findings:
    def __init__(self):
        self.total, self.errors = 0, []

    def add(self, code, index=None):
        self.total += 1
        if len(self.errors) < MAX_ERRORS:
            self.errors.append(code if index is None else code + ':scene=' + str(index))

    def check(self, condition, code, index=None):
        if not condition:
            self.add(code, index)


def fraction_wire(value):
    return {'n': str(value.numerator), 'd': str(value.denominator)}


def interval_wire(interval):
    return {'l': fraction_wire(interval[0]), 'u': fraction_wire(interval[1])}


def fields(value, names, code):
    require(isinstance(value, dict) and set(value) == set(names), code)


def sequence(value, count, code):
    require(isinstance(value, list) and len(value) == count, code)
    return value


def integer(value, low, high, code):
    require(type(value) is int and low <= value <= high, code)
    return value


def candidate_interval(value):
    fields(value, ('l', 'u'), 'interval-fields')
    lo, hi = canonical_integer(value['l']), canonical_integer(value['u'])
    require(-(1 << 352) <= lo <= hi <= 1 << 352, 'interval-order-or-range')
    return Fraction(lo, SCALE), Fraction(hi, SCALE)


def upper_value(value):
    number = canonical_integer(value)
    require(0 <= number <= 1 << 352, 'upper-range')
    return Fraction(number, SCALE)


def rational(value):
    fields(value, ('n', 'd'), 'rational-fields')
    # Finite binary64 products can have subnormal denominators beyond 128 digits.
    for key in ('n', 'd'):
        require(isinstance(value[key], str) and len(value[key]) <= 2048 and
                re.fullmatch(r'0|-?[1-9][0-9]*', value[key]) is not None,
                'rational-integer-shape')
    numerator, denominator = int(value['n']), int(value['d'])
    require(denominator > 0, 'rational-denominator')
    result = Fraction(numerator, denominator)
    require(result.numerator == numerator and result.denominator == denominator,
            'rational-not-reduced')
    return result


def contains(outer, inner, code):
    require(outer[0] <= inner[0] <= inner[1] <= outer[1], code)


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, b):
    products = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    return min(products), max(products)


def scaled(a, factor):
    return times(a, (factor, factor))


def sum_intervals(values):
    answer = (Fraction(0), Fraction(0))
    for value in values:
        answer = plus(answer, value)
    return answer


def quantize(interval, bits):
    scale = 1 << bits
    lower, upper = interval[0] * scale, interval[1] * scale
    return (Fraction(lower.numerator // lower.denominator, scale),
            Fraction(-((-upper.numerator) // upper.denominator), scale))


def sqrt_bounds(value, bits):
    require(value >= 0, 'sqrt-domain')
    scale = 1 << bits
    squared = value * scale * scale
    lower = isqrt(squared.numerator // squared.denominator)
    upper = lower if lower * lower == squared else lower + 1
    return Fraction(lower, scale), Fraction(upper, scale)


def cross(a, b):
    return tuple(a[(k+1)%3]*b[(k+2)%3] - a[(k+2)%3]*b[(k+1)%3]
                 for k in range(3))


def prepared_exact(value, helper):
    forces = helper.exact_vector(value['forces'])
    axis = helper.exact_vector(value['axis'])
    offsets = [helper.exact_vector(row) for row in value['offsets']]
    return {'forces': forces, 'axis': axis, 'levers': [cross(v, axis) for v in offsets],
            'weights': tuple(v / sum(forces, Fraction(0)) for v in forces)}


def load_boxes(prepared, roots):
    rotor = [scaled(x, f) for x, f in zip(roots, prepared['forces'])]
    collective = sum_intervals(rotor)
    force = [scaled(collective, v) for v in prepared['axis']]
    moment = [sum_intervals(scaled(rotor[r], prepared['levers'][r][k]) for r in range(4))
              for k in range(3)]
    return {'rotor': rotor, 'collective': collective, 'force': force, 'moment': moment}


def bisect_cubic(alpha):
    """Exactly 128 prescribed bisections; exact roots are retained as points."""
    require(alpha >= 0, 'reference-alpha-domain')
    if alpha == 0:
        return Fraction(1), Fraction(1)
    lower, upper = Fraction(0), Fraction(1)
    for _ in range(128):
        middle = (lower + upper) / 2
        value = middle**3 + alpha * middle
        if value == 1:
            lower = upper = middle
        elif value < 1:
            lower = middle
        else:
            upper = middle
    return lower, upper


def source_box(weights, roots, bits):
    weighted = sum_intervals(scaled(root, weight) for root, weight in zip(roots, weights))
    return sqrt_bounds(weighted[0], bits)[0], sqrt_bounds(weighted[1], bits)[1]


def reference_roots(target):
    roots, sources, loads = {}, {}, {}
    rows = {(drone_id, r): [] for drone_id in target['order'] for r in range(4)}
    for pair in target['pairs']:
        if pair['oracle']['status'] == 'positive':
            rows[(pair['i'], pair['r'])].append((pair['j'], pair['coefficient']))
    for drone_id in target['order']:
        group = []
        for r in range(4):
            alpha = sum_intervals(times(coefficient, sources[source])
                                  for source, coefficient in rows[(drone_id, r)])
            root = (bisect_cubic(alpha[1])[0], bisect_cubic(alpha[0])[1])
            require(0 < root[0] <= root[1] <= 1, 'reference-root-domain')
            roots[(drone_id, r)] = root
            group.append(root)
        sources[drone_id] = source_box(target['exact'][drone_id]['weights'], group, 192)
        loads[drone_id] = load_boxes(target['exact'][drone_id], group)
    return roots, loads


def read_contract(path):
    value = load_json(path, MAX_SPEC_BYTES)
    require(isinstance(value, dict) and value.get('schema') == 'm31-coupled-load-result-v1'
            and value.get('journalSchema') == 'm31-coupled-load-journal-v1', 'contract-schema')
    require(value.get('documentFields') == ['schema', 'specId', 'runtime', 'sourceSha256',
                                           'constants', 'records'], 'contract-document-fields')
    require(value.get('recordFields') == ['id', 'input', 'prepared', 'coverage', 'pairs',
                                         'result', 'solve', 'certificate'], 'contract-record-fields')
    require(value.get('negativeControls') == CONTROL_NAMES, 'contract-controls')
    require(value.get('sourceFiles') == ['spec.json', 'result-contract.json', 'interval.cjs',
            'rational.cjs', 'adapter.cjs', 'pair.cjs', 'coupled.cjs', 'run.cjs'], 'contract-sources')
    require(same_json(value.get('allowedStressUnresolved'), {
        'tiny-force': ['pair-normalizer'], 'huge-force': ['pair-unresolved-range']}),
        'contract-stress-policy')
    require(same_json(value.get('allowedStressPairs'), {
        'tiny-force': [{'i':0,'r':0,'j':1,'branch':'normalizer'}],
        'huge-force': [{'i':0,'r':r,'j':1,'branch':'unresolved-range'} for r in range(4)]}),
        'contract-stress-pair-identities')
    return value


def regenerate(spec, constant_bits, helper):
    """New declared scenes only: no inherited generator or inherited suite calls."""
    require(spec.get('id') == 'm31-coupled-loads-v1', 'spec-id')
    fixed = {'expectedRecords': 19, 'maxDrones': 16, 'stableIdMin': 0, 'stableIdMax': 65535,
             'candidateIterations': 48, 'rootBisections': 54, 'referenceCoefficientBits': 192,
             'referenceSourceBits': 192, 'referenceRootBisections': 128, 'fractionBits': 96,
             'positiveTermCap': 2000000, 'expectedPlannedPairs': 2632}
    for name, value in fixed.items():
        require(type(spec.get(name)) is int and spec[name] == value, 'spec-fixed:' + name)
    require(same_json(spec.get('tolerance'), {'numerator': '1', 'denominator': '100000000'}),
            'spec-tolerance')
    require(same_json(spec.get('corners'), [[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]]),
            'spec-corner-order')
    c = {name: helper.dyadic(value) for name, value in constant_bits.items()}
    scenes = sequence(spec.get('scenes'), spec['expectedRecords'], 'spec-scene-count')
    expected, scene_ids, total_planned = [], set(), 0
    for scene in scenes:
        fields(scene, ('id', 'drones', 'expectedClass'), 'spec-scene-fields')
        name = scene['id']
        require(isinstance(name, str) and re.fullmatch(r'[a-z][a-z0-9-]{0,63}', name)
                and name not in scene_ids, 'spec-scene-id')
        scene_ids.add(name)
        drones = scene['drones']
        require(isinstance(drones, list) and 1 <= len(drones) <= 16, 'spec-drone-count')
        inputs, prepared, ids, exact = [], [], set(), {}
        for drone in drones:
            fields(drone, ('id', 'state'), 'spec-drone-fields')
            identifier = integer(drone['id'], 0, 65535, 'spec-stable-id')
            require(identifier not in ids, 'spec-duplicate-stable-id')
            ids.add(identifier)
            state = sequence(drone['state'], 17, 'spec-raw-state-count')
            require(all(isinstance(v, str) and len(v) <= 128 for v in state), 'spec-raw-literals')
            raw = tuple(helper.literal(v) for v in state)
            inputs.append({'id': identifier, 'state': [helper.hex_bits(v) for v in raw]})
            value, rejection = None, None
            if not all(helper.finite(v) for v in raw):
                rejection = 'raw-nonfinite'
            elif not all(helper.dyadic(v) > 0 for v in raw[13:17]):
                rejection = 'raw-force'
            else:
                value = helper.prepare_one(raw, constant_bits, spec['corners'])
                if not helper.preparation_valid(raw, value, c):
                    rejection = 'preparation'
                else:
                    exact[identifier] = prepared_exact(value, helper)
            prepared.append({'id': identifier, 'value': value, 'rejection': rejection})
        planned = 4 * len(drones) * (len(drones)-1)
        total_planned += planned
        target = {'id': name, 'input': {'drones': inputs}, 'prepared': prepared,
                  'planned': planned, 'pairs': [], 'exact': exact,
                  'expectedClass': scene['expectedClass'], 'order': []}
        first_bad = next((p for p in prepared if p['rejection'] is not None), None)
        if first_bad is not None:
            target.update(status='rejected', branch=first_bad['rejection'],
                          witness={'id': first_bad['id']})
        else:
            by_id = {p['id']: p['value'] for p in prepared}
            order = sorted(ids, key=lambda i: (-helper.exact_vector(by_id[i]['center'])[2], i))
            target['order'] = order
            rank = {identifier: index for index, identifier in enumerate(order)}
            for receiver in inputs:
                for rotor in range(4):
                    for source in inputs:
                        if receiver['id'] == source['id']:
                            continue
                        case = {'id': name, 'input': {'receiver': receiver['state'],
                                'source': source['state'], 'self': False, 'rotor': rotor}}
                        oracle = helper.oracle_case(case, constant_bits, spec['corners'])
                        pair = {'i': receiver['id'], 'r': rotor, 'j': source['id'], 'oracle': oracle}
                        if oracle['status'] == 'positive':
                            pair['coefficient'] = quantize(oracle['referenceIntervals']['coefficient'], 192)
                        target['pairs'].append(pair)
            rejected = next((p for p in target['pairs'] if p['oracle']['status'] == 'rejected'), None)
            uncertain = next((p for p in target['pairs'] if p['oracle']['status'] == 'reference-undecidable'), None)
            wrong_order = next((p for p in target['pairs'] if p['oracle']['status'] == 'positive'
                                and rank[p['j']] >= rank[p['i']]), None)
            count = sum(p['oracle']['status'] == 'positive' for p in target['pairs'])
            if rejected:
                target.update(status='rejected', branch='pair-' + rejected['oracle']['branch'],
                              witness={k: rejected[k] for k in ('i','r','j')})
            elif uncertain:
                target.update(status='reference-undecidable', branch='pair-' + uncertain['oracle']['branch'],
                              witness={k: uncertain[k] for k in ('i','r','j')})
            elif wrong_order:
                target.update(status='rejected', branch='ordering',
                              witness={k: wrong_order[k] for k in ('i','r','j')})
            elif count > spec['positiveTermCap']:
                target.update(status='resource', branch='positive-term-budget', witness=None)
            else:
                target.update(status='admitted', branch='loads', witness=None)
                target['roots'], target['loads'] = reference_roots(target)
        actual_class = ('admitted' if target['status'] == 'admitted' else
                        target['status'] + ':' + target['branch'])
        target['referenceClass'] = actual_class
        target['expectedClassAgrees'] = scene['expectedClass'] == actual_class
        expected.append(target)
    require(total_planned == spec['expectedPlannedPairs'], 'spec-planned-pair-count')
    return expected


def validate_pair(result, target, scene_id, contract):
    require(isinstance(result, dict), 'pair-result-object')
    status, branch, oracle = result.get('status'), result.get('branch'), target['oracle']
    require(isinstance(branch, str) and re.fullmatch(r'[a-z][a-z0-9-]{0,63}', branch), 'pair-branch-shape')
    if status == 'unresolved':
        fields(result, ('status','branch'), 'pair-unresolved-fields')
        require('pair-' + branch in contract['allowedStressUnresolved'].get(scene_id, []),
                'unexpected-pair-refusal')
        identity = {key:target[key] for key in ('i','r','j')}
        identity['branch'] = branch
        require(any(same_json(identity,allowed) for allowed in
                    contract['allowedStressPairs'].get(scene_id,[])), 'unexpected-stress-pair-identity')
        require(oracle['status'] in ('positive','reference-undecidable') or
                (oracle['status'] == 'rejected' and oracle['branch'] == 'cap'),
                'pair-refusal-before-proved-early-branch')
        return None
    require(oracle['status'] != 'reference-undecidable', 'pair-reference-undecidable')
    require(status == oracle['status'] and branch == oracle['branch'], 'pair-status-or-branch')
    if status == 'rejected':
        fields(result, ('status','branch'), 'pair-rejected-fields')
        return None
    fields(result, ('status','branch','intervals'), 'pair-result-fields')
    if status == 'zero':
        require(same_json(result['intervals'], {'K': {'l':'0','u':'0'},
                                              'coefficient': {'l':'0','u':'0'}}), 'pair-zero-intervals')
        return (Fraction(0), Fraction(0))
    require(status == 'positive', 'pair-status')
    fields(result['intervals'], ('K','scaledK','beta','nu','coefficient'), 'pair-interval-fields')
    parsed = {}
    for name, value in result['intervals'].items():
        parsed[name] = candidate_interval(value)
        require(parsed[name][0] >= 0, 'pair-negative-interval:' + name)
        contains(parsed[name], oracle['referenceIntervals'][name], 'pair-reference-containment:' + name)
    require(parsed['K'][1] <= 128 and parsed['scaledK'][1] <= 128, 'pair-cap')
    require(parsed['nu'][0] > 0, 'pair-positive-normalizer')
    return parsed['coefficient']


def absolute_error(point, box):
    return max(abs(point-box[0]), abs(point-box[1]))


def validate_certificate(row, target, coefficients, helper, constants):
    solve, certificate = row['solve'], row['certificate']
    fields(solve, ('iterations','bisections','candidate'), 'solve-fields')
    require(type(solve['iterations']) is int and solve['iterations'] == 48 and
            type(solve['bisections']) is int and solve['bisections'] == 54, 'solve-recipe-metadata')
    ids = [d['id'] for d in target['input']['drones']]
    candidates = sequence(solve['candidate'], len(ids), 'candidate-count')
    xhat, yhat = {}, {}
    for identifier, candidate in zip(ids, candidates):
        fields(candidate, ('id','x'), 'candidate-fields')
        require(type(candidate['id']) is int and candidate['id'] == identifier, 'candidate-id-order')
        values = sequence(candidate['x'], 4, 'candidate-rotor-count')
        roots = []
        for rotor, value in enumerate(values):
            word = helper.parse_bits(value)
            require(helper.finite(word), 'candidate-nonfinite')
            exact = helper.dyadic(word)
            require(0 < exact <= 1, 'candidate-domain')
            xhat[(identifier,rotor)] = exact
            roots.append((exact,exact))
        yhat[identifier] = source_box(target['exact'][identifier]['weights'], roots, 96)
    fields(certificate, ('rows','Kbar','loads','maxErrors'), 'certificate-fields')
    Kbar = upper_value(certificate['Kbar'])
    require(Kbar >= 1, 'global-factor-domain')
    rows = sequence(certificate['rows'], 4*len(ids), 'certificate-row-count')
    grouped = {(identifier,r): [] for identifier in ids for r in range(4)}
    for pair, coefficient in zip(target['pairs'], coefficients):
        if pair['oracle']['status'] == 'positive':
            require(coefficient is not None, 'missing-certified-coefficient')
            grouped[(pair['i'],pair['r'])].append(times(coefficient, yhat[pair['j']]))
    xstar = {}
    for index, saved in enumerate(rows):
        identifier, rotor = ids[index//4], index%4
        fields(saved, ('id','r','s','p','kbar','xstar'), 'certificate-row-fields')
        require(type(saved['id']) is int and saved['id'] == identifier and
                type(saved['r']) is int and saved['r'] == rotor, 'certificate-row-id-order')
        source = candidate_interval(saved['s'])
        require(source[0] >= 0, 'row-source-domain')
        contains(source, sum_intervals(grouped[(identifier,rotor)]), 'complete-row-contraction')
        proposal = xhat[(identifier,rotor)]
        defect = candidate_interval(saved['p'])
        contains(defect, plus((proposal**3,proposal**3), scaled(source, proposal)),
                 'row-defect-enclosure')
        require(defect[0] > 0, 'defect-positive-lower')
        kbar = upper_value(saved['kbar'])
        require(kbar >= max(Fraction(1), defect[1], 1/defect[0]), 'row-factor-upper')
        require(Kbar >= kbar, 'global-factor-upper')
        root = candidate_interval(saved['xstar'])
        require(0 <= root[0] <= root[1] <= 1, 'root-interval-domain')
        contains(root, (proposal/(kbar*Kbar), min(Fraction(1),proposal*kbar*Kbar)),
                 'root-defect-corollary')
        contains(root, target['roots'][(identifier,rotor)], 'independent-root-containment')
        xstar[(identifier,rotor)] = root
    loads = sequence(certificate['loads'], len(ids), 'load-count')
    maxima = {name: Fraction(0) for name in CATEGORIES}
    reference_evidence = []
    mg, radius = constants['mg'], constants['R']
    require(mg > 0 and radius > 0, 'normalization-domain')
    for identifier, load in zip(ids, loads):
        fields(load, ('id','candidate','bounds','error'), 'load-fields')
        require(type(load['id']) is int and load['id'] == identifier, 'load-id-order')
        geometry = target['exact'][identifier]
        proposal_boxes = load_boxes(geometry, [(xhat[(identifier,r)], xhat[(identifier,r)]) for r in range(4)])
        propagated = load_boxes(geometry, [xstar[(identifier,r)] for r in range(4)])
        reference = target['loads'][identifier]
        fields(load['candidate'], ('rotor','collective','force','moment'), 'candidate-load-fields')
        fields(load['bounds'], ('rotor','collective','force','moment'), 'load-bounds-fields')
        point, boxes = {}, {}
        for name, count in (('rotor',4),('force',3),('moment',3)):
            point[name] = [rational(v) for v in sequence(load['candidate'][name], count,
                                                       'candidate-load-vector-count')]
            boxes[name] = [candidate_interval(v) for v in sequence(load['bounds'][name], count,
                                                                  'load-box-vector-count')]
            for k in range(count):
                require(proposal_boxes[name][k] == (point[name][k],point[name][k]),
                        'candidate-load-identity:' + name)
                contains(boxes[name][k], propagated[name][k], 'signed-root-load-propagation:' + name)
                contains(boxes[name][k], reference[name][k], 'independent-load-containment:' + name)
        point['collective'] = rational(load['candidate']['collective'])
        boxes['collective'] = candidate_interval(load['bounds']['collective'])
        require(proposal_boxes['collective'] == (point['collective'],point['collective']),
                'candidate-load-identity:collective')
        contains(boxes['collective'], propagated['collective'], 'signed-root-load-propagation:collective')
        contains(boxes['collective'], reference['collective'], 'independent-load-containment:collective')
        fields(load['error'], CATEGORIES, 'load-error-fields')
        rotor_errors = [upper_value(v) for v in sequence(load['error']['rotor'],4,'rotor-error-count')]
        for r, error in enumerate(rotor_errors):
            require(error * (mg/4) >= absolute_error(point['rotor'][r], boxes['rotor'][r]),
                    'rotor-error-full-box')
        maxima['rotor'] = max(maxima['rotor'], *rotor_errors)
        collective_error = upper_value(load['error']['collective'])
        require(collective_error * mg >= absolute_error(point['collective'], boxes['collective']),
                'collective-error-full-box')
        maxima['collective'] = max(maxima['collective'], collective_error)
        for category, name, denominator in (('worldForce','force',mg),('worldMoment','moment',mg*radius)):
            error = upper_value(load['error'][category])
            norm_squared = sum((absolute_error(point[name][k],boxes[name][k])**2 for k in range(3)), Fraction(0))
            require((error*denominator)**2 >= norm_squared, category + '-error-full-box')
            maxima[category] = max(maxima[category], error)
        reference_evidence.append({'id': identifier,
            'roots': [interval_wire(target['roots'][(identifier,r)]) for r in range(4)],
            'loads': {name: interval_wire(value) if name == 'collective' else
                      [interval_wire(v) for v in value] for name,value in reference.items()}})
    fields(certificate['maxErrors'], CATEGORIES, 'scene-max-error-fields')
    declared = {name: upper_value(certificate['maxErrors'][name]) for name in CATEGORIES}
    for name in CATEGORIES:
        require(declared[name] >= maxima[name], 'scene-max-error-upper:' + name)
    achieved = all(value*100000000 <= 1 for value in declared.values())
    require(same_json(row['result'], {'status': 'certified' if achieved else 'tolerance-failed',
             'branch': 'loads', 'witness': None, 'toleranceAchieved': achieved}),
            'tolerance-status-exact-decision')
    return {'toleranceAchieved': achieved, 'maxErrorUppers': certificate['maxErrors'],
            'independentReference': reference_evidence}


def validate_scene(row, target, contract, spec, helper, constants):
    fields(row, contract['recordFields'], 'record-fields')
    require(row['id'] == target['id'], 'record-id-or-order')
    require(same_json(row['input'],target['input']), 'raw-input-regeneration')
    require(same_json(row['prepared'],target['prepared']), 'prepared-operation-graph')
    fields(row['coverage'], ('plannedPairs','observedPairs','positiveTerms','stopReason'), 'coverage-fields')
    fields(row['result'], ('status','branch','witness','toleranceAchieved'), 'scene-result-fields')
    pairs = sequence(row['pairs'], len(target['pairs']), 'pair-count')
    coefficients, failures = [], []
    # Continue pair validation after failures. Every later saved pair remains audited.
    for index, (pair, expected_pair) in enumerate(zip(pairs,target['pairs'])):
        coefficient = None
        try:
            fields(pair, ('i','r','j','result'), 'pair-record-fields')
            require(all(type(pair[k]) is int and pair[k] == expected_pair[k] for k in ('i','r','j')),
                    'pair-stable-id-or-order')
            coefficient = validate_pair(pair['result'],expected_pair,target['id'],contract)
        except CheckError as error:
            failures.append(str(error) + ':pair=' + str(index))
        coefficients.append(coefficient)
    positive_count = sum(isinstance(p,dict) and isinstance(p.get('result'),dict) and
                         p['result'].get('status') == 'positive' for p in pairs)
    globally_invalid = any(p['rejection'] is not None for p in target['prepared'])
    require(same_json(row['coverage'], {'plannedPairs': target['planned'], 'observedPairs': len(pairs),
        'positiveTerms': positive_count, 'stopReason': 'global-preparation' if globally_invalid else None}),
        'coverage-counters')
    require(not failures, 'pair-validation:' + '|'.join(failures[:4]))
    if globally_invalid:
        require(same_json(row['result'], {'status':'rejected','branch':target['branch'],
                'witness':target['witness'],'toleranceAchieved':None}), 'global-rejection-priority')
        require(row['solve'] is None and row['certificate'] is None, 'global-rejection-payload')
        return {'qualified': True, 'toleranceAchieved': None, 'pairCount': len(pairs),
                'positiveTerms': positive_count, 'unresolvedPairs': 0}
    rejected = next((p for p in pairs if p['result']['status'] == 'rejected'), None)
    uncertain = next((p for p in pairs if p['result']['status'] == 'unresolved'), None)
    rank = {identifier:index for index,identifier in enumerate(target['order'])}
    wrong_order = next((p for p in pairs if p['result']['status'] == 'positive' and
                        rank[p['j']] >= rank[p['i']]), None)
    if rejected:
        decision = {'status':'rejected','branch':'pair-' + rejected['result']['branch'],
                    'witness':{k:rejected[k] for k in ('i','r','j')},'toleranceAchieved':None}
    elif uncertain:
        decision = {'status':'unresolved','branch':'pair-' + uncertain['result']['branch'],
                    'witness':{k:uncertain[k] for k in ('i','r','j')},'toleranceAchieved':None}
    elif wrong_order:
        decision = {'status':'rejected','branch':'ordering',
                    'witness':{k:wrong_order[k] for k in ('i','r','j')},'toleranceAchieved':None}
    elif positive_count > spec['positiveTermCap']:
        decision = {'status':'resource','branch':'positive-term-budget','witness':None,'toleranceAchieved':None}
    else:
        decision = None
    unresolved_count = sum(p['result']['status'] == 'unresolved' for p in pairs)
    common = {'pairCount':len(pairs),'positiveTerms':positive_count,'unresolvedPairs':unresolved_count}
    if decision is not None:
        require(same_json(row['result'],decision), 'scene-refusal-priority')
        require(row['solve'] is None and row['certificate'] is None, 'refusal-payload')
        return dict(common,qualified=unresolved_count == 0,toleranceAchieved=None)
    require(target['status'] == 'admitted', 'independent-scene-not-admitted')
    return dict(common,qualified=True,**validate_certificate(row,target,coefficients,helper,constants))


def safe_branch(value):
    return value if isinstance(value,str) and re.fullmatch(r'[a-z][a-z0-9-]{0,63}',value) else '_invalid'


def validate_core(document, spec, contract, expected, constant_table, source_hashes, helper):
    """Identical baseline/control validator. Never consults the append-only journal."""
    findings, records = Findings(), []
    try:
        fields(document, contract['documentFields'], 'document-fields')
        require(document['schema'] == contract['schema'], 'document-schema')
        require(document['specId'] == spec['id'], 'document-spec-id')
        require(same_json(document['sourceSha256'],source_hashes), 'source-hash-report')
        require(same_json(document['constants'],constant_table), 'constant-encoding-graph')
        runtime = document['runtime']
        fields(runtime, ('node','v8','platform','arch'), 'runtime-fields')
        require(all(isinstance(v,str) and 1 <= len(v) <= 256 for v in runtime.values()), 'runtime-string')
        require(isinstance(document['records'],list) and len(document['records']) <= 64, 'records-array-budget')
        records = document['records']
    except CheckError as error:
        findings.add(str(error))
    findings.check(len(records) == len(expected), 'record-count')
    global_ok = findings.total == 0
    seen, evidence = set(), []
    statuses, reference_statuses, branches, pair_statuses = Counter(), Counter(), Counter(), Counter()
    qualified, admitted, tolerance_passed, observed_pairs, positives, planned = 0, 0, 0, 0, 0, 0
    constants = {name:helper.dyadic(helper.parse_bits(value)) for name,value in constant_table.items()}
    for index,row in enumerate(records):
        if index >= len(expected):
            findings.add('unexpected-extra-record',index)
            continue
        target = expected[index]
        before = findings.total
        if isinstance(row,dict):
            identifier = row.get('id')
            if isinstance(identifier,str):
                findings.check(identifier not in seen, 'duplicate-record-id',index)
                seen.add(identifier)
            result = row.get('result')
            result = result if isinstance(result,dict) else {}
        else:
            result = {}
        status, branch = safe_branch(result.get('status')), safe_branch(result.get('branch'))
        statuses[status] += 1
        branches[branch] += 1
        reference_statuses[target['status']] += 1
        planned += target['planned']
        item = {'id':target['id'],'referenceStatus':target['status'],'referenceBranch':target['branch'],
                'referenceWitness':target['witness'],'referenceClass':target['referenceClass'],
                'declaredExpectedClass':target['expectedClass'],'expectedClassAgrees':target['expectedClassAgrees'],
                'candidateStatus':status,'candidateBranch':branch,'verified':False,'qualified':False}
        try:
            details = validate_scene(row,target,contract,spec,helper,constants)
            item.update(details)
            item['verified'] = global_ok and findings.total == before
            item['qualified'] = item['verified'] and details['qualified']
            qualified += int(item['qualified'])
            admitted += int(item['qualified'] and target['status'] == 'admitted')
            tolerance_passed += int(item['qualified'] and details['toleranceAchieved'] is True)
            observed_pairs += details['pairCount']
            positives += details['positiveTerms']
            for pair in row['pairs']:
                pair_statuses[pair['result']['status']] += 1
        except CheckError as error:
            findings.add(str(error),index)
            item['failure'] = str(error)
        except Exception as error:
            findings.add('scene-exception:' + type(error).__name__,index)
            item['failure'] = 'scene-exception:' + type(error).__name__
        if not item['qualified'] and item['verified']:
            item['unqualifiedReason'] = 'declared-stress-refusal'
        evidence.append(item)
    # expectedClass is a prospective claim, never an admission oracle. Ordinary
    # disagreement invalidates the claim; named stress differences remain explicit.
    for index,target in enumerate(expected):
        if target['id'] not in contract['allowedStressUnresolved']:
            findings.check(target['expectedClassAgrees'], 'declared-reference-class-disagreement',index)
    return {'verificationPassed': findings.total == 0,
            'fullQualification': findings.total == 0 and qualified == len(expected),
            'tolerancePassed': findings.total == 0 and tolerance_passed == admitted,
            'totalRecords':len(records),'qualifiedRecords':qualified,
            'unqualifiedRecords':len(expected)-qualified,'admittedRecords':admitted,
            'tolerancePassedRecords':tolerance_passed,'toleranceFailedRecords':admitted-tolerance_passed,
            'expectedPlannedPairs':spec['expectedPlannedPairs'],'reportedPlannedPairs':planned,
            'observedPairs':observed_pairs,'positiveTerms':positives,
            'referenceStatusCounts':dict(reference_statuses),'observedStatusCounts':dict(statuses),
            'observedBranchCounts':dict(branches),'observedPairStatusCounts':dict(pair_statuses),
            'errorCount':findings.total,'errors':findings.errors,'scenes':evidence}


def validate_journal(path, document, spec, contract):
    require(path.is_file() and path.stat().st_size <= MAX_INPUT_BYTES, 'journal-missing-or-budget')
    with path.open('rb') as handle:
        data = handle.read(MAX_INPUT_BYTES+1)
    require(len(data) <= MAX_INPUT_BYTES, 'journal-budget')
    lines = data.splitlines()
    require(len(lines) == spec['expectedRecords']+2, 'journal-line-count')
    decoded = []
    for line in lines:
        try:
            decoded.append(json.loads(line,object_pairs_hook=pairs_without_duplicates,
                                      parse_constant=reject_json_constant))
        except (ValueError,UnicodeError,RecursionError):
            raise CheckError('journal-invalid-json') from None
    require(same_json(decoded[0], {'kind':'header','schema':contract['journalSchema'],
                                  'specId':spec['id']}), 'journal-header')
    require(same_json(decoded[-1], {'kind':'complete','records':spec['expectedRecords']}),
            'journal-completion')
    require(isinstance(document,dict) and isinstance(document.get('records'),list) and
            len(document['records']) == spec['expectedRecords'], 'journal-final-count')
    for index,(entry,row) in enumerate(zip(decoded[1:-1],document['records'])):
        require(same_json(entry,{'kind':'record','row':row}), 'journal-final-row:scene=' + str(index))
    return {'passed':True,'rows':spec['expectedRecords'],'bytes':len(data),
            'sha256':hashlib.sha256(data).hexdigest()}


def negative_controls(document, expected, validator, helper, constants):
    positive_witness = root_witness = error_witness = None
    for scene_index,target in enumerate(expected):
        if positive_witness is None:
            for pair_index,pair in enumerate(target['pairs']):
                if pair['oracle']['status'] == 'positive':
                    positive_witness = (scene_index,pair_index,{
                        'scene':target['id'],'i':pair['i'],'r':pair['r'],'j':pair['j'],
                        'oracleStatus':'positive','oracleBranch':pair['oracle']['branch'],
                        'coefficient':interval_wire(pair['coefficient'])})
                    break
        if target['status'] != 'admitted':
            continue
        row = document['records'][scene_index]
        for drone_index,drone in enumerate(target['input']['drones']):
            for rotor in range(4):
                identifier = drone['id']
                reference = target['roots'][(identifier,rotor)]
                xhat = helper.dyadic(helper.parse_bits(row['solve']['candidate'][drone_index]['x'][rotor]))
                if root_witness is None and reference[1] < 1:
                    root_witness = (scene_index,drone_index,rotor,{
                        'scene':target['id'],'id':identifier,'r':rotor,
                        'referenceRoot':interval_wire(reference),'proof':'reference upper is strictly below one'})
                if error_witness is None and (xhat < reference[0] or xhat > reference[1]):
                    gap = reference[0]-xhat if xhat < reference[0] else xhat-reference[1]
                    normalized = target['exact'][identifier]['forces'][rotor]*gap/(constants['mg']/4)
                    require(normalized > 0, 'negative-error-witness-not-strict')
                    error_witness = (scene_index,drone_index,rotor,{
                        'scene':target['id'],'id':identifier,'r':rotor,'candidate':fraction_wire(xhat),
                        'referenceRoot':interval_wire(reference),'separatingRootGap':fraction_wire(gap),
                        'strictNormalizedErrorLowerBound':fraction_wire(normalized),
                        'proof':'candidate lies strictly outside independently enclosed true root'})
    require(positive_witness is not None and root_witness is not None and error_witness is not None,
            'negative-control-proven-witness-missing')
    psi, ppi, pair_proof = positive_witness
    rsi, rdi, rri, root_proof = root_witness
    esi, edi, eri, error_proof = error_witness

    def missing_pair(clone):
        clone['records'][psi]['pairs'].pop(ppi)

    def root_one(clone):
        clone['records'][rsi]['certificate']['rows'][rdi*4+rri]['xstar'] = {'l':str(SCALE),'u':str(SCALE)}

    def candidate_bits(clone):
        values = clone['records'][rsi]['solve']['candidate'][rdi]['x']
        values[rri] = helper.hex_bits(helper.parse_bits(values[rri]) ^ 1)

    def error_zero(clone):
        clone['records'][esi]['certificate']['loads'][edi]['error']['rotor'][eri] = '0'

    def lever(clone):
        values = clone['records'][rsi]['prepared'][rdi]['value']['offsets'][rri]
        values[0] = helper.hex_bits(helper.parse_bits(values[0]) ^ 1)

    def stable_id(clone):
        pair = clone['records'][psi]['pairs'][ppi]
        pair['j'] = pair['i']

    def missing_scene(clone):
        clone['records'].pop()

    def duplicate_scene(clone):
        clone['records'][1] = copy.deepcopy(clone['records'][0])

    def reorder_scenes(clone):
        clone['records'][0],clone['records'][1] = clone['records'][1],clone['records'][0]

    probes = [
        ('missing-positive-pair',missing_pair,pair_proof),
        ('false-root-one',root_one,root_proof),
        ('altered-candidate',candidate_bits,{'scene':expected[rsi]['id'],'id':root_proof['id'],'r':rri,
                                          'mutation':'xor one least-significant stored binary64 bit'}),
        ('false-error-zero',error_zero,error_proof),
        ('altered-lever-arm',lever,{'scene':expected[rsi]['id'],'id':root_proof['id'],'r':rri,
                                  'mutation':'xor one least-significant prepared offset bit'}),
        ('altered-stable-id',stable_id,pair_proof),
        ('missing-scene',missing_scene,{'removedScene':expected[-1]['id']}),
        ('duplicate-scene',duplicate_scene,{'replacement':expected[0]['id'],'replaced':expected[1]['id']}),
        ('reordered-scenes',reorder_scenes,{'exchanged':[expected[0]['id'],expected[1]['id']]})]
    controls = []
    for name,mutation,witness in probes:
        clone = copy.deepcopy(document)
        mutation(clone)
        verdict = validator(clone)
        controls.append({'name':name,'executed':True,'rejected':not verdict['verificationPassed'],
                         'witness':witness,'errorCount':verdict['errorCount'],'errors':verdict['errors']})
    return controls


def load_frozen_reference(path, root, indexed):
    name = relative_name(path,root)
    require(name in indexed and indexed[name]['sha256'] == HELPER_SHA256, 'independent-helper-pin')
    # Execute precisely the hashed source buffer. An import loader could instead
    # accept a stale timestamp/size-valid __pycache__ artifact outside the pins.
    with path.open('rb') as handle:
        source = handle.read(MAX_SOURCE_BYTES+1)
    require(len(source) == indexed[name]['bytes'] and
            hashlib.sha256(source).hexdigest() == indexed[name]['sha256'] == HELPER_SHA256,
            'independent-helper-source-buffer-pin')
    module = types.ModuleType('m31_frozen_pair_reference')
    module.__file__ = str(path)
    exec(compile(source,str(path),'exec'),module.__dict__)
    return module


def main(argv=None):
    parser = PublicArgumentParser(description='Independent complete-row coupled-load saved-result checker')
    for name in ('spec','input','manifest','output','root'):
        parser.add_argument('--'+name,required=True)
    try:
        args = parser.parse_args(argv)
    except CheckError:
        print('{"verificationPassed":false,"error":"invalid-command-line"}',file=sys.stderr)
        return 2
    report = {'schema':'m31-coupled-load-independent-check-v1','passed':False,
              'verificationPassed':False,'fullQualification':False,'tolerancePassed':False,
              'checkerRuntime':{'pythonVersion':'.'.join(str(v) for v in sys.version_info[:3]),
                                'implementation':sys.implementation.name},
              'scope':'complete current-state pair coverage; ordered coupled roots; exact signed loads and full-box normalized errors',
              'expectedRecords':19,'totalRecords':0,'faultControls':[],'errors':[]}
    output_allowed = False
    try:
        root = Path(args.root).resolve(strict=True)
        require(root.is_dir(), 'root-not-directory')
        output = Path(args.output)
        try:
            output.parent.resolve(strict=True).relative_to(root)
        except (OSError,ValueError):
            raise CheckError('output-parent-outside-root-or-missing') from None
        output_allowed = True
        spec_path,input_path,manifest_path = Path(args.spec),Path(args.input),Path(args.manifest)
        contract_path,helper_path = spec_path.parent/'result-contract.json',spec_path.parent/'pair-reference.py'
        for path in (spec_path,input_path,manifest_path,contract_path,helper_path):
            relative_name(path,root)
        verified = verify_manifest(manifest_path,root,spec_path,contract_path)
        indexed = {item['path']:item for item in verified}
        # The copied independent module is imported only after every local manifest
        # entry, this checker, and its immutable original helper hash are verified.
        helper = load_frozen_reference(helper_path,root,indexed)
        spec,contract = load_json(spec_path,MAX_SPEC_BYTES),read_contract(contract_path)
        constant_bits,constant_trace = helper.constants_from_graph(spec)
        constant_table = {name:helper.hex_bits(value) for name,value in constant_bits.items()}
        expected = regenerate(spec,constant_bits,helper)
        source_hashes = {}
        for name in contract['sourceFiles']:
            relative = relative_name(spec_path.parent/name,root)
            require(relative in indexed, 'candidate-source-not-pinned')
            source_hashes[name] = indexed[relative]['sha256']
        document = load_json(input_path,MAX_INPUT_BYTES)

        def validator(candidate):
            return validate_core(candidate,spec,contract,expected,constant_table,source_hashes,helper)

        baseline = validator(document)
        for key,value in baseline.items():
            if key not in ('verificationPassed','fullQualification','tolerancePassed','errorCount'):
                report[key] = value
        report['baselineErrorCount'] = baseline['errorCount']
        report['baselineVerificationPassed'] = baseline['verificationPassed']
        report['expectedConstantEncodings'] = constant_table
        report['constantGraphIntermediateEncodings'] = constant_trace
        report['verifiedSources'] = verified
        report['sourceManifest'] = {'path':relative_name(manifest_path,root),
                                    'sha256':file_sha256(manifest_path,MAX_MANIFEST_BYTES)[1]}
        report['input'] = {'path':relative_name(input_path,root),
                           'sha256':file_sha256(input_path,MAX_INPUT_BYTES)[1]}
        journal_path = Path(str(input_path)+'.jsonl')
        try:
            relative_name(journal_path,root)
            report['journal'] = validate_journal(journal_path,document,spec,contract)
            report['journal']['path'] = relative_name(journal_path,root)
        except CheckError as error:
            report['journal'] = {'passed':False,'errors':[str(error)]}
            report['errors'].append(str(error))
        if baseline['verificationPassed']:
            constants = {name:helper.dyadic(value) for name,value in constant_bits.items()}
            report['faultControls'] = negative_controls(document,expected,validator,helper,constants)
        else:
            report['errors'].append('controls-not-run-on-invalid-baseline')
        controls_passed = (len(report['faultControls']) == len(CONTROL_NAMES) and
                           [item['name'] for item in report['faultControls']] == CONTROL_NAMES and
                           all(item['executed'] and item['rejected'] for item in report['faultControls']))
        if not controls_passed:
            report['errors'].append('negative-controls-incomplete-or-ineffective')
        report['verificationPassed'] = baseline['verificationPassed'] and report['journal']['passed'] and controls_passed
        report['fullQualification'] = report['verificationPassed'] and baseline['fullQualification']
        report['tolerancePassed'] = report['verificationPassed'] and baseline['tolerancePassed']
        report['passed'] = report['verificationPassed']
        # Rehash the complete frozen inventory after the scientific reference and
        # fault controls, and retain the first inventory for direct comparison.
        after = verify_manifest(manifest_path,root,spec_path,contract_path)
        require(same_json(after,verified), 'checker-source-after-mismatch')
        report['sourcesUnchangedAfter'] = True
    except CheckError as error:
        report['errors'].append(str(error))
        report['passed'] = report['verificationPassed'] = report['fullQualification'] = report['tolerancePassed'] = False
    except Exception as error:
        report['errors'].append('checker-exception:' + type(error).__name__)
        report['passed'] = report['verificationPassed'] = report['fullQualification'] = report['tolerancePassed'] = False
    report['errors'] = report['errors'][:MAX_ERRORS]
    payload = (json.dumps(report,indent=2,sort_keys=True)+'\n').encode('utf-8')
    try:
        require(output_allowed and len(payload) <= MAX_REPORT_BYTES, 'report-output-path-or-budget')
        with Path(args.output).open('xb') as handle:
            handle.write(payload)
    except Exception:
        print('{"verificationPassed":false,"error":"exclusive-report-write-failed"}',file=sys.stderr)
        return 2
    print(json.dumps({'verificationPassed':report['verificationPassed'],
                      'fullQualification':report['fullQualification'],
                      'tolerancePassed':report['tolerancePassed'],
                      'totalRecords':report['totalRecords'],'faultControls':len(report['faultControls'])}))
    return 0 if report['verificationPassed'] else 1


if __name__ == '__main__':
    sys.exit(main())
