#!/usr/bin/env python3
"""Independent exact-screening saved checker; no candidate implementation imports.

Only main, after source-pin verification, loads the frozen independent pair source.
The old generators, main routines and qualification suites are never called.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path, PurePosixPath
import re
import sys
import types

MAX_INPUT_BYTES = 128 * 1024 * 1024
MAX_JOURNAL_BYTES = 128 * 1024 * 1024
MAX_REPORT_BYTES = 96 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_SPEC_BYTES = 512 * 1024
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_SOURCE_TOTAL = 64 * 1024 * 1024
MAX_SOURCE_FILES = 256
MAX_ERRORS = 48
SCALE = 1 << 96
CATEGORIES = ('rotor','collective','worldForce','worldMoment')
RULES = ('neighbor','upstream','down-cut','near-outside','radial')
WORK_FIELDS = ('preparationCalls','globalProofs','treeNodes','nodeVisits','nodeRuleTests',
               'zeroNodes','zeroPairs','leafVisits','scalarPairs','scalarZeroPairs',
               'positiveTerms','rejectedPairs','unresolvedPairs')
CONTROL_NAMES = ['missing-source-subtree','duplicate-source-coverage','false-zero-active-leaf',
                 'omitted-positive-entry','wrong-tree-membership','wrong-tree-bound',
                 'altered-prepared-offset','false-global-guard','incomplete-fallback',
                 'altered-positive-coefficient','false-root-one','altered-candidate',
                 'false-error-zero','missing-scene','duplicate-scene','reordered-scenes']
SOURCE_FILES = ['spec.json','result-contract.json','interval.cjs','rational.cjs','adapter.cjs',
                'pair-prepared.cjs','boxes.cjs','tree.cjs','loads.cjs','methods.cjs','run.cjs']
HELPER_SHA256 = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'

class CheckError(Exception):
    """An intentionally public-safe validation failure."""


def require(condition, code):
    if not condition:
        raise CheckError(code)


def canonical_integer(value):
    require(isinstance(value, str) and len(value) <= 108,
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


class Findings:
    def __init__(self):
        self.total, self.errors = 0, []

    def add(self, code, index=None):
        self.total += 1
        if len(self.errors) < MAX_ERRORS:
            self.errors.append((code if index is None else code + ':scene=' + str(index))[:256])

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
        require(isinstance(value[key], str) and len(value[key]) <= 4096 and
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


def absolute_error(point, box):
    return max(abs(point-box[0]), abs(point-box[1]))


def validate_certificate(row, target, coefficients, helper, constants, emit_reference=False):
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
        if emit_reference:
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


def compact_bytes(value):
    return len(json.dumps(value,separators=(',',':'),ensure_ascii=True).encode('utf-8'))


def read_contract(path):
    value = load_json(path,MAX_SPEC_BYTES)
    require(isinstance(value,dict) and value.get('schema') == 'm31-exact-screening-result-v1'
            and value.get('journalSchema') == 'm31-exact-screening-journal-v1','contract-schema')
    required = {
        'documentFields':['schema','specId','runtime','sourceSha256','constants','records'],
        'recordFields':['id','input','methods'],
        'methodFields':['name','prepared','assembly','result','solve','certificate'],
        'assemblyFields':['mode','globalGuard','tree','queries','work'],
        'methods':['complete','hierarchy'],'workFields':list(WORK_FIELDS),
        'zeroRuleOrder':list(RULES),'negativeControls':CONTROL_NAMES,
        'allowedStressPairs':{},'sourceFiles':SOURCE_FILES,
        'methodEquality':['prepared','result','canonicalPositiveEntries','solve','certificate']}
    for name,expected in required.items():
        require(same_json(value.get(name),expected),'contract-fixed:'+name)
    limits = {'kernelBytes':MAX_INPUT_BYTES,'journalBytes':MAX_JOURNAL_BYTES,
              'checkerBytes':MAX_REPORT_BYTES,'nonzeroEntryBytes':384,'certificateRowBytes':1024,
              'loadRecordBytes':98304,'treeNodeBytes':8192,'fixed96IntegerChars':108,
              'loadRationalIntegerChars':4096,'treeNumeratorChars':310,'treeDenominatorChars':324,
              'maxErrors':48,'maxErrorChars':256,'controlWitnessBytes':65536}
    require(same_json(value.get('wireLimits'),limits),'contract-wire-limits')
    return value


def box_of(vectors):
    require(bool(vectors),'empty-box-membership')
    return tuple((min(v[k] for v in vectors),max(v[k] for v in vectors)) for k in range(3))


def subtract(a,b):
    return a[0]-b[1],a[1]-b[0]


def absolute_max(interval):
    return max(abs(interval[0]),abs(interval[1]))


def absolute_min(interval):
    return Fraction(0) if interval[0] <= 0 <= interval[1] else min(abs(interval[0]),abs(interval[1]))


def box_wire(box):
    return [[fraction_wire(endpoint) for endpoint in interval] for interval in box]


def global_guard(geometry):
    centers = box_of([v['center'] for v in geometry])
    axes = box_of([v['axis'] for v in geometry])
    points = box_of([point for v in geometry for point in v['points']])
    center_difference = tuple(subtract(v,v) for v in centers)
    displacement = tuple(subtract(a,b) for a,b in zip(centers,points))
    height = sum_intervals(times(a,b) for a,b in zip(displacement,axes))
    residual = tuple(subtract(d,times(height,a)) for d,a in zip(displacement,axes))
    upper = {'centerComponent':max(absolute_max(v) for v in center_difference),
             'centerNorm':sum((absolute_max(v)**2 for v in center_difference),Fraction(0)),
             'rotorComponent':max(absolute_max(v) for v in displacement),
             'down':absolute_max(height),
             'radial':sum((absolute_max(v)**2 for v in residual),Fraction(0))}
    limits = {'centerComponent':Fraction(257),'centerNorm':Fraction(512**2),
              'rotorComponent':Fraction(258),'down':Fraction(1024),'radial':Fraction(2048**2)}
    checks = {key:upper[key] <= limit for key,limit in limits.items()}
    return {'passed':all(checks.values()),'checks':checks}, {'upper':upper,'limits':limits}


def reconstruct_tree(geometry,ids):
    nodes,permutation,members,boxes = [],[],{},{}
    def build(indices):
        node_id = len(nodes)
        center = box_of([geometry[i]['center'] for i in indices])
        axis = box_of([geometry[i]['axis'] for i in indices])
        node = {'id':node_id,'start':len(permutation),'end':None,'left':None,'right':None,
                'center':box_wire(center),'axis':box_wire(axis)}
        nodes.append(node)
        members[node_id] = tuple(indices)
        boxes[node_id] = {'center':center,'axis':axis}
        if len(indices) <= 8:
            # Preserve incoming recursive order; a small root preserves input order.
            permutation.extend(ids[i] for i in indices)
        else:
            spans = [interval[1]-interval[0] for interval in center]
            split_axis = max(range(3),key=lambda k:(spans[k],-k))
            ordered = sorted(indices,key=lambda i:(geometry[i]['center'][split_axis],ids[i]))
            midpoint = len(ordered)//2
            node['left'] = build(ordered[:midpoint])
            node['right'] = build(ordered[midpoint:])
        node['end'] = len(permutation)
        return node_id
    build(list(range(len(ids))))
    return {'permutation':permutation,'nodes':nodes},members,boxes


def zero_rule(node,receiver,rotor,constants):
    centers,axes = node['center'],node['axis']
    center_distance = tuple((v[0]-receiver['center'][k],v[1]-receiver['center'][k])
                            for k,v in enumerate(centers))
    displacement = tuple((v[0]-receiver['points'][rotor][k],v[1]-receiver['points'][rotor][k])
                         for k,v in enumerate(centers))
    height = sum_intervals(times(a,b) for a,b in zip(displacement,axes))
    residual = tuple(subtract(d,times(height,a)) for d,a in zip(displacement,axes))
    radial_lower = sum((absolute_min(v)**2 for v in residual),Fraction(0))
    # W=(spread*(H/D-origin))*D; subtract origin before multiplying spread.
    width = scaled((height[0]/constants['D']-constants['origin'],
                    height[1]/constants['D']-constants['origin']),constants['spread']*constants['D'])
    conditions = (
        sum((absolute_min(v)**2 for v in center_distance),Fraction(0)) >= constants['neighbor']**2,
        height[1] <= 0,
        height[0] >= constants['downCut'],
        height[1] < constants['minDown']*constants['D'] and radial_lower >= constants['nearRad']**2,
        height[0] >= constants['minDown']*constants['D'] and width[0] > 0 and
            radial_lower >= constants['radCut']**2*width[1]**2)
    for index,condition in enumerate(conditions):
        if condition:
            return RULES[index],index+1
    return None,len(RULES)


def blank_work(count):
    result = {name:0 for name in WORK_FIELDS}
    result['preparationCalls'] = count
    return result


def assembly_plan(target,method,constants):
    n = len(target['input']['drones'])
    work = blank_work(n)
    if target['globalInvalid']:
        return {'mode':'global-preparation','globalGuard':None,'tree':None,'queries':[],
                'work':work,'rules':{name:0 for name in RULES}}
    guard = target['globalGuard'] if method == 'hierarchy' else None
    mode = 'complete' if method == 'complete' else ('hierarchy' if guard['passed'] else 'fallback')
    if method == 'hierarchy':
        work['globalProofs'] = 1
    tree = target['tree'] if mode == 'hierarchy' else None
    if tree is not None:
        work['treeNodes'] = len(tree['nodes'])
    queries,rule_counts = [],{name:0 for name in RULES}
    for receiver in range(n):
        for rotor in range(4):
            terminals = []
            def add_scalar(kind,eligible,node=None):
                terminal = {'kind':kind,'members':tuple(sorted(eligible))}
                if node is not None:
                    terminal['node'] = node
                    work['leafVisits'] += 1
                terminals.append(terminal)
                work['scalarPairs'] += len(eligible)
                for source in eligible:
                    status = target['lookup'][(receiver,rotor,source)]['oracle']['status']
                    counter = {'zero':'scalarZeroPairs','positive':'positiveTerms',
                               'rejected':'rejectedPairs','reference-undecidable':'unresolvedPairs'}[status]
                    work[counter] += 1
            if mode != 'hierarchy':
                add_scalar('scan',[j for j in range(n) if j != receiver])
            else:
                def visit(node_id):
                    node = tree['nodes'][node_id]
                    eligible = tuple(j for j in target['members'][node_id] if j != receiver)
                    work['nodeVisits'] += 1
                    rule,tests = zero_rule(target['boxes'][node_id],target['geometry'][receiver],rotor,constants)
                    work['nodeRuleTests'] += tests
                    if rule is not None:
                        # A finite full-oracle cross-check supplements, but does not
                        # replace, the independent node interval proof.
                        require(all(target['lookup'][(receiver,rotor,j)]['oracle']['status'] == 'zero'
                                    for j in eligible),'reference-zero-rule-contradiction')
                        terminals.append({'kind':'zero','node':node_id,'rule':rule,
                                          'count':len(eligible),'members':eligible})
                        work['zeroNodes'] += 1
                        work['zeroPairs'] += len(eligible)
                        rule_counts[rule] += 1
                    elif node['left'] is None:
                        add_scalar('leaf',eligible,node_id)
                    else:
                        visit(node['left'])
                        visit(node['right'])
                visit(0)
            covered = [j for terminal in terminals for j in terminal['members']]
            require(sorted(covered) == [j for j in range(n) if j != receiver],
                    'reference-plan-partition')
            queries.append({'i':receiver,'r':rotor,'terminals':terminals})
    require(work['zeroPairs']+work['scalarPairs'] == target['planned'],'reference-work-coverage')
    return {'mode':mode,'globalGuard':guard,'tree':tree,'queries':queries,'work':work,'rules':rule_counts}


def regenerate(spec,constant_bits,helper):
    require(isinstance(spec,dict) and spec.get('id') == 'm31-exact-screening-v1','spec-id')
    fixed = {'expectedRecords':18,'maxDrones':64,'stableIdMin':0,'stableIdMax':65535,
             'leafCapacity':8,'candidateIterations':48,'rootBisections':54,'referenceCoefficientBits':192,
             'referenceSourceBits':192,'referenceRootBisections':128,'fractionBits':96,
             'positiveTermCap':2000000,'expectedPlannedPairs':46744}
    for name,value in fixed.items():
        require(type(spec.get(name)) is int and spec[name] == value,'spec-fixed:'+name)
    require(same_json(spec.get('methods'),['complete','hierarchy']) and
            same_json(spec.get('zeroRuleOrder'),list(RULES)),'spec-methods-rules')
    require(same_json(spec.get('tolerance'),{'numerator':'1','denominator':'100000000'}),'spec-tolerance')
    require(same_json(spec.get('corners'),[[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]]),'spec-corners')
    constants = {name:helper.dyadic(value) for name,value in constant_bits.items()}
    expected,scene_ids,total_planned,total_drones = [],set(),0,0
    for scene in sequence(spec.get('scenes'),18,'spec-scene-count'):
        fields(scene,('id','drones','expectedClass','purpose'),'spec-scene-fields')
        name = scene['id']
        require(isinstance(name,str) and re.fullmatch(r'[a-z][a-z0-9-]{0,63}',name)
                and name not in scene_ids,'spec-scene-id')
        scene_ids.add(name)
        drones = scene['drones']
        require(isinstance(drones,list) and 1 <= len(drones) <= 64,'spec-drone-count')
        inputs,prepared,ids,exact,geometry = [],[],[],{},[]
        for drone in drones:
            fields(drone,('id','state'),'spec-drone-fields')
            identifier = integer(drone['id'],0,65535,'spec-stable-id')
            require(identifier not in ids,'spec-duplicate-id')
            ids.append(identifier)
            state = sequence(drone['state'],17,'spec-raw-state-count')
            require(all(isinstance(v,str) and len(v) <= 128 for v in state),'spec-raw-literal')
            raw = tuple(helper.literal(v) for v in state)
            inputs.append({'id':identifier,'state':[helper.hex_bits(v) for v in raw]})
            value,rejection = None,None
            if not all(helper.finite(v) for v in raw):
                rejection = 'raw-nonfinite'
            elif not all(helper.dyadic(v) > 0 for v in raw[13:17]):
                rejection = 'raw-force'
            else:
                value = helper.prepare_one(raw,constant_bits,spec['corners'])
                if not helper.preparation_valid(raw,value,constants):
                    rejection = 'preparation'
                else:
                    exact[identifier] = prepared_exact(value,helper)
            prepared.append({'id':identifier,'value':value,'rejection':rejection})
        planned = 4*len(ids)*(len(ids)-1)
        total_planned += planned
        total_drones += len(ids)
        target = {'id':name,'input':{'drones':inputs},'prepared':prepared,'exact':exact,
                  'planned':planned,'pairs':[],'lookup':{},'order':[],
                  'expectedClass':scene['expectedClass'],'tree':None,'globalGuard':None}
        first_bad = next((v for v in prepared if v['rejection'] is not None),None)
        target['globalInvalid'] = first_bad is not None
        if first_bad is not None:
            target.update(status='rejected',branch=first_bad['rejection'],witness={'id':first_bad['id']})
        else:
            for item in prepared:
                p = item['value']
                geometry.append({'center':helper.exact_vector(p['center']),
                                 'axis':helper.exact_vector(p['axis']),
                                 'points':[helper.exact_vector(point) for point in p['points']]})
            target['geometry'] = geometry
            target['globalGuard'],target['guardEvidence'] = global_guard(geometry)
            if target['globalGuard']['passed']:
                target['tree'],target['members'],target['boxes'] = reconstruct_tree(geometry,ids)
            order_indices = sorted(range(len(ids)),key=lambda i:(-geometry[i]['center'][2],ids[i]))
            target['order'] = [ids[i] for i in order_indices]
            ranks = {identifier:index for index,identifier in enumerate(target['order'])}
            for receiver,drone in enumerate(inputs):
                for rotor in range(4):
                    for source,other in enumerate(inputs):
                        if receiver == source:
                            continue
                        oracle_full = helper.oracle_case({'id':name,'input':{'receiver':drone['state'],
                            'source':other['state'],'self':False,'rotor':rotor}},constant_bits,spec['corners'])
                        oracle = {'status':oracle_full['status'],'branch':oracle_full['branch']}
                        pair = {'i':ids[receiver],'r':rotor,'j':ids[source],
                                'ii':receiver,'jj':source,'oracle':oracle}
                        if oracle['status'] == 'positive':
                            # One outward fixed192 quantization; do not retain a second
                            # unquantized reference or a rounded coefficient midpoint.
                            pair['coefficient'] = quantize(oracle_full['referenceIntervals']['coefficient'],192)
                        target['pairs'].append(pair)
                        target['lookup'][(receiver,rotor,source)] = pair
            rejected = next((p for p in target['pairs'] if p['oracle']['status'] == 'rejected'),None)
            uncertain = next((p for p in target['pairs'] if p['oracle']['status'] == 'reference-undecidable'),None)
            wrong = next((p for p in target['pairs'] if p['oracle']['status'] == 'positive' and
                          ranks[p['j']] >= ranks[p['i']]),None)
            positives = sum(p['oracle']['status'] == 'positive' for p in target['pairs'])
            if rejected is not None:
                target.update(status='rejected',branch='pair-'+rejected['oracle']['branch'],
                              witness={k:rejected[k] for k in ('i','r','j')})
            elif uncertain is not None:
                target.update(status='reference-undecidable',branch='pair-'+uncertain['oracle']['branch'],
                              witness={k:uncertain[k] for k in ('i','r','j')})
            elif wrong is not None:
                target.update(status='rejected',branch='ordering',witness={k:wrong[k] for k in ('i','r','j')})
            elif positives > spec['positiveTermCap']:
                target.update(status='resource',branch='positive-term-budget',witness=None)
            else:
                target.update(status='admitted',branch='loads',witness=None)
                target['roots'],target['loads'] = reference_roots(target)
        target['referenceClass'] = ('admitted' if target['status'] == 'admitted' else
                                    target['status']+':'+target['branch'])
        target['plans'] = {method:assembly_plan(target,method,constants) for method in ('complete','hierarchy')}
        expected.append(target)
    require(total_planned == 46744 and total_drones == 312,'spec-total-counts')
    return expected


def validate_tree_wire(value,target):
    fields(value,('permutation','nodes'),'tree-fields')
    sequence(value['permutation'],len(target['input']['drones']),'tree-permutation-count')
    sequence(value['nodes'],len(target['tree']['nodes']),'tree-node-count')
    for node in value['nodes']:
        fields(node,('id','start','end','left','right','center','axis'),'tree-node-fields')
        require(compact_bytes(node) <= 8192,'tree-node-byte-budget')
        for name in ('center','axis'):
            for interval in sequence(node[name],3,'tree-vector-count'):
                lower,upper = sequence(interval,2,'tree-interval-count')
                for endpoint in (lower,upper):
                    fields(endpoint,('n','d'),'tree-rational-fields')
                    require(isinstance(endpoint['n'],str) and len(endpoint['n']) <= 310 and
                            isinstance(endpoint['d'],str) and len(endpoint['d']) <= 324,
                            'tree-rational-string-budget')
                require(rational(lower) <= rational(upper),'tree-interval-order')
    require(same_json(value,target['tree']),'tree-operation-graph')


def validate_nonzero(value,pair):
    require(isinstance(value,dict),'nonzero-result-object')
    oracle = pair['oracle']
    require(oracle['status'] != 'reference-undecidable','reference-uncertain-pair')
    require(value.get('status') != 'unresolved','unresolved-not-qualified')
    if oracle['status'] == 'positive':
        fields(value,('status','branch','coefficient'),'positive-result-fields')
        require(value['status'] == 'positive' and value['branch'] == 'active','positive-status')
        coefficient = candidate_interval(value['coefficient'])
        require(coefficient[0] >= 0,'negative-coefficient')
        contains(coefficient,pair['coefficient'],'coefficient-reference-containment')
        return coefficient
    require(oracle['status'] == 'rejected','explicit-nonzero-oracle-zero')
    require(same_json(value,oracle),'rejected-pair-status-branch')
    return None


def validate_assembly(assembly,target,method,constants):
    fields(assembly,('mode','globalGuard','tree','queries','work'),'assembly-fields')
    plan = target['plans'][method]
    require(same_json(assembly['globalGuard'],plan['globalGuard']),'global-guard-operation-graph')
    require(assembly['mode'] == plan['mode'],'assembly-mode')
    if plan['tree'] is None:
        require(assembly['tree'] is None,'unexpected-tree')
    else:
        validate_tree_wire(assembly['tree'],target)
    queries = sequence(assembly['queries'],len(plan['queries']),'query-count')
    saved_pairs = {}
    coverage_count = 0
    for query,reference_query in zip(queries,plan['queries']):
        fields(query,('i','r','terminals'),'query-fields')
        require(type(query['i']) is int and query['i'] == reference_query['i'] and
                type(query['r']) is int and query['r'] == reference_query['r'],'query-index-or-order')
        receiver,rotor = query['i'],query['r']
        terminals = sequence(query['terminals'],len(reference_query['terminals']),'terminal-count')
        covered = []
        for terminal,reference_terminal in zip(terminals,reference_query['terminals']):
            require(isinstance(terminal,dict),'terminal-object')
            kind = terminal.get('kind')
            require(kind in ('zero','leaf','scan'),'terminal-kind')
            if kind == 'scan':
                fields(terminal,('kind','entries','zeroCount'),'scan-fields')
                require(plan['mode'] in ('complete','fallback'),'scan-in-screened-mode')
                members = tuple(j for j in range(len(target['input']['drones'])) if j != receiver)
            else:
                fields(terminal,('kind','node','rule','count') if kind == 'zero' else
                       ('kind','node','entries','zeroCount'),'tree-terminal-fields')
                require(plan['mode'] == 'hierarchy','tree-terminal-without-global-proof')
                node_id = integer(terminal['node'],0,len(target['tree']['nodes'])-1,'terminal-node-id')
                members = tuple(sorted(j for j in target['members'][node_id] if j != receiver))
                if kind == 'zero':
                    proven_rule,_ = zero_rule(target['boxes'][node_id],target['geometry'][receiver],rotor,constants)
                    require(terminal['rule'] in RULES and terminal['rule'] == proven_rule,'node-zero-rule')
                    require(all(target['lookup'][(receiver,rotor,j)]['oracle']['status'] == 'zero'
                                for j in members),'node-zero-oracle-member')
                    require(type(terminal['count']) is int and terminal['count'] == len(members),'node-zero-count')
                else:
                    require(target['tree']['nodes'][node_id]['left'] is None,'nonleaf-scalar-terminal')
            covered.extend(members)
            require(kind == reference_terminal['kind'] and
                    (kind == 'scan' or terminal['node'] == reference_terminal['node']),
                    'terminal-canonical-traversal')
            if kind == 'zero':
                continue
            entries = terminal['entries']
            require(isinstance(entries,list) and len(entries) <= len(members),'entry-count')
            seen,previous = set(),-1
            for entry in entries:
                fields(entry,('j','result'),'entry-fields')
                require(compact_bytes(entry) <= 384,'entry-byte-budget')
                source = integer(entry['j'],0,len(target['input']['drones'])-1,'entry-source-index')
                require(source in members and source not in seen and source > previous,'entry-membership-or-order')
                seen.add(source)
                previous = source
                pair = target['lookup'][(receiver,rotor,source)]
                coefficient = validate_nonzero(entry['result'],pair)
                key = (receiver,rotor,source)
                require(key not in saved_pairs,'duplicate-singleton')
                saved_pairs[key] = {'result':entry['result'],'coefficient':coefficient}
            require(type(terminal['zeroCount']) is int and terminal['zeroCount'] == len(members)-len(entries),
                    'implicit-zero-count')
            for source in members:
                if source not in seen:
                    require(target['lookup'][(receiver,rotor,source)]['oracle']['status'] == 'zero',
                            'implicit-zero-nonzero')
        require(sorted(covered) == [j for j in range(len(target['input']['drones'])) if j != receiver],
                'source-partition-incomplete-or-overlap')
        coverage_count += len(covered)
    require(coverage_count == (0 if target['globalInvalid'] else target['planned']),'accounted-pair-count')
    require(same_json(assembly['work'],plan['work']),'work-counter-reconstruction')
    coefficients,canonical_positive = [],[]
    for pair in target['pairs']:
        saved = saved_pairs.get((pair['ii'],pair['r'],pair['jj']))
        if pair['oracle']['status'] == 'positive':
            require(saved is not None and saved['coefficient'] is not None,'missing-positive-singleton')
            coefficients.append(saved['coefficient'])
            canonical_positive.append({'i':pair['i'],'r':pair['r'],'j':pair['j'],
                                       'coefficient':saved['result']['coefficient']})
        else:
            coefficients.append(None)
    return coefficients,canonical_positive,coverage_count


def validate_method(value,target,method,constants,helper,emit_reference):
    fields(value,('name','prepared','assembly','result','solve','certificate'),'method-fields')
    require(value['name'] == method,'method-name-or-order')
    require(same_json(value['prepared'],target['prepared']),'prepared-operation-graph')
    fields(value['result'],('status','branch','witness','toleranceAchieved'),'result-fields')
    coefficients,canonical_positive,coverage = validate_assembly(value['assembly'],target,method,constants)
    result = {'name':method,'mode':target['plans'][method]['mode'],
              'work':target['plans'][method]['work'],'zeroRuleCounts':target['plans'][method]['rules'],
              'accountedPairs':coverage,'positiveCoefficientRecords':len(canonical_positive),
              'verified':True,'toleranceAchieved':None}
    if target['status'] == 'admitted':
        require(isinstance(value['certificate'],dict),'certificate-object')
        for row in value['certificate'].get('rows',[]):
            require(compact_bytes(row) <= 1024,'certificate-row-byte-budget')
        for load in value['certificate'].get('loads',[]):
            require(compact_bytes(load) <= 98304,'load-record-byte-budget')
        result.update(validate_certificate(value,target,coefficients,helper,constants,emit_reference))
    else:
        require(target['status'] != 'reference-undecidable','reference-scene-uncertain')
        require(same_json(value['result'],{'status':target['status'],'branch':target['branch'],
                'witness':target['witness'],'toleranceAchieved':None}),'canonical-model-refusal')
        require(value['solve'] is None and value['certificate'] is None,'refusal-payload')
    return result,canonical_positive


def validate_core(document,spec,contract,expected,constant_table,source_hashes,helper,emit_reference=True):
    findings,records = Findings(),[]
    try:
        fields(document,contract['documentFields'],'document-fields')
        require(document['schema'] == contract['schema'] and document['specId'] == spec['id'],'document-identity')
        require(same_json(document['sourceSha256'],source_hashes),'source-hash-report')
        require(same_json(document['constants'],constant_table),'constant-encoding-graph')
        fields(document['runtime'],('node','v8','platform','arch'),'runtime-fields')
        require(all(isinstance(v,str) and 1 <= len(v) <= 256 for v in document['runtime'].values()),'runtime-values')
        require(isinstance(document['records'],list) and len(document['records']) <= 64,'records-array-budget')
        records = document['records']
    except CheckError as error:
        findings.add(str(error))
    findings.check(len(records) == len(expected),'record-count')
    global_valid = findings.total == 0
    constants = {name:helper.dyadic(helper.parse_bits(value)) for name,value in constant_table.items()}
    scenes,seen = [],set()
    qualified,admitted,tolerance_passed,equal = 0,0,0,0
    for index,row in enumerate(records):
        if index >= len(expected):
            findings.add('extra-scene',index)
            continue
        target = expected[index]
        before = findings.total
        item = {'id':target['id'],'declaredExpectedClass':target['expectedClass'],
                'referenceClass':target['referenceClass'],'referenceStatus':target['status'],
                'referenceBranch':target['branch'],'referenceWitness':target['witness'],
                'expectedClassAgrees':target['expectedClass'] == target['referenceClass'],
                'plannedPairsPerMethod':target['planned'],'methods':[],
                'methodEquality':False,'verified':False}
        scenes.append(item)
        try:
            fields(row,contract['recordFields'],'record-fields')
            require(isinstance(row['id'],str) and row['id'] not in seen,'duplicate-scene-id')
            seen.add(row['id'])
            require(row['id'] == target['id'],'record-id-or-order')
            require(same_json(row['input'],target['input']),'raw-input-regeneration')
            methods = sequence(row['methods'],2,'method-count')
            successful,positives = [],[]
            for method_index,name in enumerate(('complete','hierarchy')):
                try:
                    method_report,positive_records = validate_method(methods[method_index],target,name,
                        constants,helper,emit_reference and method_index == 0)
                    if 'independentReference' in method_report:
                        reference = method_report.pop('independentReference')
                        if reference:
                            item['independentReference'] = reference
                    item['methods'].append(method_report)
                    successful.append(True)
                    positives.append(positive_records)
                except CheckError as error:
                    findings.add(str(error)+':method='+name,index)
                    item['methods'].append({'name':name,'verified':False,'failure':str(error)[:256]})
                    successful.append(False)
                    positives.append(None)
            # Equality cannot mask a missing semantic validator: it is checked only
            # after each method independently passes, and controls require a named
            # core failure family rather than an equality-only failure.
            if all(successful):
                for name in ('prepared','result','solve','certificate'):
                    require(same_json(methods[0][name],methods[1][name]),'method-equality:'+name)
                require(same_json(positives[0],positives[1]),'method-equality:positive-coefficients')
                item['methodEquality'] = True
                equal += 1
        except CheckError as error:
            findings.add(str(error),index)
            item['failure'] = str(error)[:256]
        except Exception as error:
            findings.add('scene-exception:'+type(error).__name__,index)
            item['failure'] = 'scene-exception:'+type(error).__name__
        findings.check(item['expectedClassAgrees'],'declared-reference-class-disagreement',index)
        item['verified'] = global_valid and findings.total == before
        if item['verified']:
            qualified += 1
            if target['status'] == 'admitted':
                admitted += 1
                tolerance_passed += int(all(m['toleranceAchieved'] is True for m in item['methods']))
    return {'verificationPassed':findings.total == 0,'fullQualification':findings.total == 0 and qualified == 18,
            'tolerancePassed':findings.total == 0 and tolerance_passed == admitted,
            'totalRecords':len(records),'qualifiedRecords':qualified,'unqualifiedRecords':18-qualified,
            'admittedRecords':admitted,'tolerancePassedRecords':tolerance_passed,
            'toleranceFailedRecords':admitted-tolerance_passed,'methodEqualityRecords':equal,
            'expectedPlannedPairsPerMethod':46744,'errorCount':findings.total,'errors':findings.errors,'scenes':scenes}


def negative_controls(document,expected,validator,helper,constants):
    terminal_witness = positive_leaf = coefficient_witness = membership_witness = bound_witness = None
    fallback_witness = guard_witness = root_witness = error_witness = prepared_witness = None
    for si,target in enumerate(expected):
        method = document['records'][si]['methods'][1]
        tree = target['tree']
        if tree is not None:
            if membership_witness is None and len(tree['permutation']) >= 2:
                membership_witness = (si,{'scene':target['id'],'ids':tree['permutation'][:2]})
            if bound_witness is None:
                for node in tree['nodes']:
                    for coordinate,interval in enumerate(target['boxes'][node['id']]['center']):
                        if interval[0] < interval[1]:
                            excluded = next(j for j in target['members'][node['id']]
                                            if target['geometry'][j]['center'][coordinate] == interval[0])
                            bound_witness = (si,node['id'],coordinate,{
                                'scene':target['id'],'node':node['id'],'coordinate':coordinate,
                                'excludedStableId':target['input']['drones'][excluded]['id'],
                                'excludedValue':fraction_wire(interval[0]),'newLower':fraction_wire(interval[1])})
                            break
                    if bound_witness is not None:
                        break
        plan = target['plans']['hierarchy']
        if guard_witness is None and plan['mode'] == 'fallback':
            failed = next(key for key,value in target['globalGuard']['checks'].items() if not value)
            guard_witness = (si,{'scene':target['id'],'failedCheck':failed,
                'computedUpper':fraction_wire(target['guardEvidence']['upper'][failed]),
                'allowedUpper':fraction_wire(target['guardEvidence']['limits'][failed])})
        for qi,query in enumerate(plan['queries']):
            for ti,terminal in enumerate(query['terminals']):
                if plan['mode'] == 'hierarchy' and terminal_witness is None and terminal['members']:
                    terminal_witness = (si,qi,ti,{'scene':target['id'],'receiverIndex':query['i'],
                        'r':query['r'],'node':terminal['node'],
                        'witnessSourceIndex':terminal['members'][0],
                        'memberCount':len(terminal['members'])})
                if terminal['kind'] == 'zero':
                    continue
                saved = method['assembly']['queries'][qi]['terminals'][ti]
                for ei,entry in enumerate(saved['entries']):
                    pair = target['lookup'][(query['i'],query['r'],entry['j'])]
                    proof = {'scene':target['id'],'receiverIndex':query['i'],'r':query['r'],
                             'sourceIndex':entry['j'],'i':pair['i'],'j':pair['j'],
                             'referenceStatus':pair['oracle']['status'],'referenceBranch':pair['oracle']['branch']}
                    if fallback_witness is None and plan['mode'] == 'fallback':
                        fallback_witness = (si,qi,ti,ei,proof)
                    if pair['oracle']['status'] == 'positive':
                        proof = dict(proof,coefficient=interval_wire(pair['coefficient']))
                        if positive_leaf is None and terminal['kind'] == 'leaf':
                            positive_leaf = (si,qi,ti,ei,dict(proof,node=terminal['node'],
                                                           memberCount=len(terminal['members'])))
                        if coefficient_witness is None and pair['coefficient'][0] > 0:
                            coefficient_witness = (si,qi,ti,ei,proof)
        if target['status'] != 'admitted':
            continue
        if prepared_witness is None:
            prepared_witness = (si,{'scene':target['id'],'id':target['input']['drones'][0]['id'],
                                    'rotor':0,'coordinate':0})
        for di,drone in enumerate(target['input']['drones']):
            for rotor in range(4):
                reference = target['roots'][(drone['id'],rotor)]
                proposal = helper.dyadic(helper.parse_bits(method['solve']['candidate'][di]['x'][rotor]))
                if root_witness is None and reference[1] < 1:
                    root_witness = (si,di,rotor,{'scene':target['id'],'id':drone['id'],'r':rotor,
                                               'referenceRoot':interval_wire(reference)})
                if error_witness is None and (proposal < reference[0] or proposal > reference[1]):
                    gap = reference[0]-proposal if proposal < reference[0] else proposal-reference[1]
                    normalized = target['exact'][drone['id']]['forces'][rotor]*gap/(constants['mg']/4)
                    require(normalized > 0,'error-control-not-strict')
                    error_witness = (si,di,rotor,{'scene':target['id'],'id':drone['id'],'r':rotor,
                        'candidate':fraction_wire(proposal),'referenceRoot':interval_wire(reference),
                        'strictNormalizedErrorLowerBound':fraction_wire(normalized)})
    require(all(w is not None for w in (terminal_witness,positive_leaf,coefficient_witness,
            membership_witness,bound_witness,fallback_witness,guard_witness,root_witness,
            error_witness,prepared_witness)),'control-proven-witness-missing')
    tsi,tqi,tti,tproof = terminal_witness
    psi,pqi,pti,pei,pproof = positive_leaf
    csi,cqi,cti,cei,cproof = coefficient_witness
    msi,mproof = membership_witness
    bsi,bni,bki,bproof = bound_witness
    fsi,fqi,fti,fei,fproof = fallback_witness
    gsi,gproof = guard_witness
    rsi,rdi,rri,rproof = root_witness
    esi,edi,eri,eproof = error_witness
    osi,oproof = prepared_witness
    def hierarchy(clone,scene):
        return clone['records'][scene]['methods'][1]
    def terminals(clone,scene,query):
        return hierarchy(clone,scene)['assembly']['queries'][query]['terminals']
    def missing(clone):
        terminals(clone,tsi,tqi).pop(tti)
    def duplicate(clone):
        values = terminals(clone,tsi,tqi)
        values.insert(tti,copy.deepcopy(values[tti]))
    def false_zero(clone):
        terminals(clone,psi,pqi)[pti] = {'kind':'zero','node':pproof['node'],
            'rule':'neighbor','count':pproof['memberCount']}
    def omit_positive(clone):
        terminal = terminals(clone,psi,pqi)[pti]
        terminal['entries'].pop(pei)
        terminal['zeroCount'] += 1
    def membership(clone):
        values = hierarchy(clone,msi)['assembly']['tree']['permutation']
        values[0],values[1] = values[1],values[0]
    def bound(clone):
        interval = hierarchy(clone,bsi)['assembly']['tree']['nodes'][bni]['center'][bki]
        interval[0] = copy.deepcopy(interval[1])
    def prepared(clone):
        values = hierarchy(clone,osi)['prepared'][0]['value']['offsets'][0]
        values[0] = helper.hex_bits(helper.parse_bits(values[0]) ^ 1)
    def guard(clone):
        value = hierarchy(clone,gsi)['assembly']['globalGuard']
        value['passed'] = True
        value['checks'] = {key:True for key in value['checks']}
    def fallback(clone):
        terminal = terminals(clone,fsi,fqi)[fti]
        terminal['entries'].pop(fei)
        terminal['zeroCount'] += 1
    def coefficient(clone):
        terminals(clone,csi,cqi)[cti]['entries'][cei]['result']['coefficient'] = {'l':'0','u':'0'}
    def root_one(clone):
        hierarchy(clone,rsi)['certificate']['rows'][rdi*4+rri]['xstar'] = {'l':str(SCALE),'u':str(SCALE)}
    def candidate(clone):
        values = hierarchy(clone,rsi)['solve']['candidate'][rdi]['x']
        values[rri] = helper.hex_bits(helper.parse_bits(values[rri]) ^ 1)
    def error_zero(clone):
        hierarchy(clone,esi)['certificate']['loads'][edi]['error']['rotor'][eri] = '0'
    def missing_scene(clone):
        clone['records'].pop()
    def duplicate_scene(clone):
        clone['records'][1] = copy.deepcopy(clone['records'][0])
    def reorder_scenes(clone):
        clone['records'][0],clone['records'][1] = clone['records'][1],clone['records'][0]
    probes = [
        ('missing-source-subtree',missing,tproof,('terminal-count',)),
        ('duplicate-source-coverage',duplicate,tproof,('terminal-count',)),
        ('false-zero-active-leaf',false_zero,pproof,('node-zero-rule','node-zero-oracle-member')),
        ('omitted-positive-entry',omit_positive,pproof,('implicit-zero-nonzero',)),
        ('wrong-tree-membership',membership,mproof,('tree-operation-graph',)),
        ('wrong-tree-bound',bound,bproof,('tree-operation-graph',)),
        ('altered-prepared-offset',prepared,oproof,('prepared-operation-graph',)),
        ('false-global-guard',guard,gproof,('global-guard-operation-graph',)),
        ('incomplete-fallback',fallback,fproof,('implicit-zero-nonzero',)),
        ('altered-positive-coefficient',coefficient,cproof,('coefficient-reference-containment',)),
        ('false-root-one',root_one,rproof,('root-defect-corollary','independent-root-containment')),
        ('altered-candidate',candidate,rproof,('candidate-domain','complete-row-contraction',
            'row-defect-enclosure','root-defect-corollary','candidate-load-identity')),
        ('false-error-zero',error_zero,eproof,('rotor-error-full-box',)),
        ('missing-scene',missing_scene,{'removedScene':expected[-1]['id']},('record-count',)),
        ('duplicate-scene',duplicate_scene,{'duplicate':expected[0]['id'],'replaced':expected[1]['id']},
            ('duplicate-scene-id','record-id-or-order')),
        ('reordered-scenes',reorder_scenes,{'exchanged':[expected[0]['id'],expected[1]['id']]},
            ('record-id-or-order',))]
    controls = []
    for name,mutation,witness,families in probes:
        require(compact_bytes(witness) <= 65536,'control-witness-byte-budget')
        clone = copy.deepcopy(document)
        mutation(clone)
        verdict = validator(clone,False)
        targeted = any(any(error.startswith(family) for family in families) for error in verdict['errors'])
        controls.append({'name':name,'executed':True,'rejected':not verdict['verificationPassed'],
                         'intendedCoreFailure':targeted,'requiredFailureFamilies':list(families),
                         'witness':witness,'errorCount':verdict['errorCount'],'errors':verdict['errors']})
    return controls


def validate_journal(path,document,spec,contract):
    require(path.is_file() and path.stat().st_size <= MAX_JOURNAL_BYTES,'journal-missing-or-budget')
    digest = hashlib.sha256()
    rows = document.get('records') if isinstance(document,dict) else None
    require(isinstance(rows,list) and len(rows) == 18,'journal-final-count')
    total = 0
    with path.open('rb') as handle:
        for index in range(20):
            line = handle.readline(MAX_JOURNAL_BYTES+1)
            require(bool(line),'journal-line-count')
            total += len(line)
            require(total <= MAX_JOURNAL_BYTES,'journal-byte-budget')
            digest.update(line)
            try:
                decoded = json.loads(line,object_pairs_hook=pairs_without_duplicates,
                                     parse_constant=reject_json_constant)
            except (ValueError,UnicodeError,RecursionError):
                raise CheckError('journal-invalid-json') from None
            if index == 0:
                expected = {'kind':'header','schema':contract['journalSchema'],'specId':spec['id']}
            elif index == 19:
                expected = {'kind':'complete','records':18}
            else:
                expected = {'kind':'record','row':rows[index-1]}
            require(same_json(decoded,expected),'journal-final-row-or-wrapper:'+str(index))
        require(not handle.read(1),'journal-extra-data')
    return {'passed':True,'rows':18,'bytes':total,'sha256':digest.hexdigest()}


def load_frozen_reference(path,root,indexed):
    name = relative_name(path,root)
    require(name in indexed and indexed[name]['sha256'] == HELPER_SHA256,'independent-helper-pin')
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
    parser = PublicArgumentParser(description='Independent exact-screening saved-result checker')
    for name in ('spec','input','manifest','output','root'):
        parser.add_argument('--'+name,required=True)
    try:
        args = parser.parse_args(argv)
    except CheckError:
        print('{"verificationPassed":false,"error":"invalid-command-line"}',file=sys.stderr)
        return 2
    report = {'schema':'m31-exact-screening-independent-check-v1','passed':False,'verificationPassed':False,
              'fullQualification':False,'tolerancePassed':False,'totalRecords':0,'admittedRecords':0,
              'checkerRuntime':{'pythonVersion':'.'.join(str(v) for v in sys.version_info[:3]),
                                'implementation':sys.implementation.name},
              'scope':'finite exact hierarchy versus complete M-current; every implicit zero and complete signed loads independently checked',
              'faultControls':[],'errors':[]}
    output_allowed = False
    try:
        root = Path(args.root).resolve(strict=True)
        require(root.is_dir(),'root-not-directory')
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
        helper = load_frozen_reference(helper_path,root,indexed)
        spec,contract = load_json(spec_path,MAX_SPEC_BYTES),read_contract(contract_path)
        constant_bits,constant_trace = helper.constants_from_graph(spec)
        constant_table = {name:helper.hex_bits(value) for name,value in constant_bits.items()}
        expected = regenerate(spec,constant_bits,helper)
        source_hashes = {}
        for name in SOURCE_FILES:
            relative = relative_name(spec_path.parent/name,root)
            require(relative in indexed,'candidate-source-not-pinned')
            source_hashes[name] = indexed[relative]['sha256']
        document = load_json(input_path,MAX_INPUT_BYTES)
        def validator(candidate,emit_reference=True):
            return validate_core(candidate,spec,contract,expected,constant_table,source_hashes,helper,emit_reference)
        baseline = validator(document)
        for key,value in baseline.items():
            if key not in ('verificationPassed','fullQualification','tolerancePassed','errorCount'):
                report[key] = value
        report['baselineVerificationPassed'] = baseline['verificationPassed']
        report['baselineErrorCount'] = baseline['errorCount']
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
            report['journal'] = {'passed':False,'errors':[str(error)[:256]]}
            report['errors'].append(str(error)[:256])
        if baseline['verificationPassed']:
            constants = {name:helper.dyadic(value) for name,value in constant_bits.items()}
            report['faultControls'] = negative_controls(document,expected,validator,helper,constants)
        else:
            report['errors'].append('controls-not-run-on-invalid-baseline')
        controls_passed = (len(report['faultControls']) == 16 and
            [c['name'] for c in report['faultControls']] == CONTROL_NAMES and
            all(c['executed'] and c['rejected'] and c['intendedCoreFailure'] for c in report['faultControls']))
        if not controls_passed:
            report['errors'].append('negative-controls-incomplete-or-ineffective')
        after = verify_manifest(manifest_path,root,spec_path,contract_path)
        require(same_json(after,verified),'source-after-mismatch')
        report['sourcesUnchangedAfter'] = True
        report['verificationPassed'] = baseline['verificationPassed'] and report['journal']['passed'] and controls_passed
        report['fullQualification'] = report['verificationPassed'] and baseline['fullQualification']
        report['tolerancePassed'] = report['verificationPassed'] and baseline['tolerancePassed']
        report['passed'] = report['verificationPassed']
    except CheckError as error:
        report['errors'].append(str(error)[:256])
    except Exception as error:
        report['errors'].append('checker-exception:'+type(error).__name__)
    report['errors'] = report['errors'][:MAX_ERRORS]
    payload = (json.dumps(report,separators=(',',':'),sort_keys=True)+'\n').encode('utf-8')
    try:
        require(output_allowed and len(payload) <= MAX_REPORT_BYTES,'report-output-path-or-budget')
        with Path(args.output).open('xb') as handle:
            handle.write(payload)
    except Exception:
        print('{"verificationPassed":false,"error":"exclusive-report-write-failed"}',file=sys.stderr)
        return 2
    print(json.dumps({'verificationPassed':report['verificationPassed'],
                      'fullQualification':report['fullQualification'],'tolerancePassed':report['tolerancePassed'],
                      'totalRecords':report['totalRecords'],'admittedRecords':report['admittedRecords'],
                      'faultControls':len(report['faultControls'])}))
    return 0 if report['verificationPassed'] else 1


if __name__ == '__main__':
    sys.exit(main())
