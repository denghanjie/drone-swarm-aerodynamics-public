"""Independent saved-boundary transport audit; no producer or old evaluator imports.
Run once after exact-public source freeze and the sole evaluator. No work on import.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import hashlib
import json
import math
import struct
import time

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
RESULTS = BASE / 'results'
MIB = 1024 * 1024
CAP = 16 * MIB
START = None
TOLERANCE = Decimal('2e-12')
ANNULAR_PREFIX = 'research/m31-annular-balance-2026-10-19/'
CROSS_PREFIX = 'research/m31-crossstream-test-2026-10-19/'
ANNULAR = ANNULAR_PREFIX + 'results/comparison.json'
CROSS = CROSS_PREFIX + 'results/comparison.json'
PINS = {
    ANNULAR: (3020398, 'e7885559d832f4d7dc0136c9d5656a7c4a83c3ac6ab3aeee45e62c2d8562210a'),
    CROSS: (2291932, '1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a'),
}
PUBLICATIONS = {
    ANNULAR_PREFIX: 'research/publication-receipts/m31-annular-balance-result-2026-10-19.json',
    CROSS_PREFIX: 'research/publication-receipts/m31-crossstream-result-2026-10-19.json',
}
PREDECESSOR_FILES = {
    'PROTOCOL.md', 'source-manifest.json', 'source-publication.json', 'result-manifest.json',
    'results/comparison.json', 'results/execution.json', 'results/evaluate-supervisor.json',
    'results/audit.json', 'results/audit-supervisor.json',
}
IDS = ('left-lower', 'left-middle', 'left-upper', 'right-lower', 'right-middle', 'right-upper')
FACES = ('inner', 'outer', 'top', 'bottom')
FIELDS = ('axialCore', 'radialCandidate', 'candidate', 'radius', 'xi')
GAIN = .5450089857597356
LIMITS = [
    'Exposed same-experiment boundary diagnostic; no independent validation',
    'Fixed inherited axialCore/radialCandidate; no fit or field evaluation',
    'Axisymmetric no-swirl measured radial interpretation remains conditional',
    'Measured denominator can hide relative radial errors; raw faces remain primary',
    'Fixed coarsening is sensitivity, not experimental uncertainty or convergence',
    'No physical threshold, calibration, force/swarm safety or novelty claim',
]
CONTROL_NAMES = [
    'irregular constant and linear analytic integrals; both outward signs',
    'perfect face agreement', 'within-face signed cancellation',
    'between-face cancellation and zero observed scale with nonzero error',
    'shared positive and negative scaling of signs, absolute errors and ratios',
    'closed model-domain boundary', 'missing and nonfinite model fields rejected',
    'radius mismatch and prior exclusion rejected',
    'one failed node globally suppresses all six transports',
]


def need(condition, label):
    if not condition:
        raise ValueError(label)


def guard():
    need(START is not None and time.monotonic() - START < 60, 'audit-deadline')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate-json-key')
            result[key] = value
        return result

    def invalid(value):
        raise ValueError('nonfinite-json-' + value)

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def read_local(path, limit=CAP):
    guard()
    need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'local-path')
    need(path.stat().st_size <= limit, 'file-bound')
    return path.read_bytes()


def pin(path, raw):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def D(value):
    return Decimal.from_float(value) if type(value) is float else Decimal(value)


def is_finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def finite(value, label):
    need(is_finite(value), label + '-finite-number')


def close(actual, expected, label):
    finite(actual, label)
    need(abs(D(actual) - D(expected)) <= TOLERANCE, label + '-absolute-tolerance')


def same_word(actual, expected, label):
    finite(actual, label)
    need(struct.pack('>d', actual) == struct.pack('>d', expected), label + '-binary64-word')


def same_tree(actual, expected, label):
    """Exact JSON types, keys, ordering, original values and binary64 sign bits."""
    need(type(actual) is type(expected), label + '-type')
    if type(expected) is float:
        same_word(actual, expected, label)
        return 1
    if type(expected) is dict:
        need(set(actual) == set(expected), label + '-keys')
        return sum(same_tree(actual[key], value, label + '/' + key) for key, value in expected.items())
    if type(expected) is list:
        need(len(actual) == len(expected), label + '-length')
        return sum(same_tree(a, e, label + '/' + str(i)) for i, (a, e) in enumerate(zip(actual, expected)))
    need(type(expected) in (int, str, bool, type(None)) and actual == expected, label + '-value')
    return 0


def check_success(receipt, mode, label):
    need(receipt['mode'] == mode and receipt['exitCode'] == 0
         and receipt['timeout'] is False and 0 <= receipt['elapsedSeconds'] < 60
         and receipt['outputLimitExceeded'] is False and receipt['outputCapBytes'] == CAP
         and type(receipt['savedBytesBeforeSupervisor']) is int
         and 0 <= receipt['savedBytesBeforeSupervisor'] <= CAP, label)


def write_once(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    need(len(raw) <= CAP, 'audit-output-cap')
    with (RESULTS / name).open('xb') as stream:
        stream.write(raw)


def predecessor_chain(prefix, document, raw):
    """Reused evidence-binding mechanics; never calls an earlier evaluator."""
    retained = {}
    for name in PREDECESSOR_FILES - {'PROTOCOL.md', 'results/comparison.json'}:
        retained[prefix + name] = read_local(ROOT / (prefix + name))
    publication_path = PUBLICATIONS[prefix]
    retained[publication_path] = read_local(ROOT / publication_path)
    source_raw = retained[prefix + 'source-manifest.json']
    source_public = parse_json(retained[prefix + 'source-publication.json'])
    need(source_public['manifestSha256'] == sha(source_raw)
         and source_public['remoteBytesEqualLocal'] is True
         and source_public['committedBytesEqualLocal'] is True
         and document['sourceCommit'] == source_public['commit'], 'prior-source-binding')
    result_path = ROOT / (prefix + 'results/comparison.json')
    execution = parse_json(retained[prefix + 'results/execution.json'])
    need(execution['status'] == 'complete' and execution['resultBytes'] == len(raw)
         and execution['sha256'] == sha(raw), 'prior-execution-binding')
    audit = parse_json(retained[prefix + 'results/audit.json'])
    need(audit['passed'] is True and audit['complete'] is True
         and audit['resultPin'] == pin(result_path, raw)
         and audit['sourceManifestSha256'] == sha(source_raw), 'prior-audit-binding')
    for mode in ('evaluate', 'audit'):
        check_success(parse_json(retained[prefix + 'results/' + mode + '-supervisor.json']),
                      mode, 'prior-' + mode + '-supervised-success')
    manifest_raw = retained[prefix + 'result-manifest.json']
    publication = parse_json(retained[publication_path])
    need(publication['manifestPath'] == prefix + 'result-manifest.json'
         and publication['manifestBytes'] == len(manifest_raw)
         and publication['manifestSha256'] == sha(manifest_raw)
         and publication['remoteBytesEqualLocal'] is True
         and publication['committedBytesEqualLocal'] is True, 'prior-public-result-binding')
    matching = [entry for entry in parse_json(manifest_raw)['files']
                if entry['path'] == prefix + 'results/comparison.json']
    need(matching == [pin(result_path, raw)], 'prior-published-result-pin')
    return retained


def verify_manifest(manifest):
    entries = manifest['files']
    need(type(entries) is list and 0 < len(entries) <= 10000, 'manifest-count')
    names = set()
    for entry in entries:
        guard()
        need(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'manifest-fields')
        name = entry['path']
        need(type(name) is str and name not in names and not Path(name).is_absolute()
             and '..' not in Path(name).parts, 'manifest-name')
        names.add(name)
        path = ROOT / name
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'manifest-path')
        need(type(entry['bytes']) is int and 0 <= entry['bytes'] <= 64 * MIB
             and path.stat().st_size == entry['bytes'], 'manifest-size')
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            while True:
                block = stream.read(MIB)
                if not block:
                    break
                guard()
                digest.update(block)
        need(digest.hexdigest() == entry['sha256'], 'manifest-sha256')
    prefix = BASE.relative_to(ROOT).as_posix() + '/'
    required = {prefix + name for name in ('PROTOCOL.md', 'source/evaluate.py', 'source/audit.py',
                'source/supervise.py', 'review/SOURCE-AUDIT.md', 'review/PROTOCOL-REVIEW.md')}
    for previous, publication in PUBLICATIONS.items():
        required |= {previous + name for name in PREDECESSOR_FILES}
        required.add(publication)
    need(required <= names, 'manifest-required-inputs-and-provenance')
    return len(entries)


def inherited_structure(old, cross):
    """Check saved structure/identity only; do not select a new grid or remeasure flux."""
    need(old['status'] == 'completed-annular-balance'
         and old['selection']['admission']['passed'] is True
         and cross['status'] == 'completed-cross-component-diagnostic', 'completed-predecessors')
    same_tree(cross['inheritedGain'], GAIN, 'exact-inherited-gain')
    originals = old['originalCases']
    need(type(originals) is list and len(originals) == 3240, 'original-case-count')
    words = same_tree(originals, cross['cases'], 'annular-crossstream-originalCases')
    byid = {}
    for case in cross['cases']:
        index = case['original']['index']
        need(type(index) is int and index not in byid, 'unique-original-index')
        byid[index] = case
    projected = old['projectedNodes']
    need(type(projected) is list and len(projected) == 1220
         and type(old['selection']['selectedCount']) is int
         and old['selection']['selectedCount'] == 1220, 'inherited-selected-count')
    memberships = {}
    for entry in old['selection']['membership']:
        if entry['regionId'] is not None:
            index = entry['index']
            need(type(index) is int and index not in memberships
                 and entry['regionId'] in IDS, 'saved-membership-identity')
            memberships[index] = entry['regionId']
    projected_ids = set()
    for point in projected:
        guard()
        need(type(point) is dict and set(point) == {'index', 'X', 'Z', 'R', 'U', 'v', 'Vr'},
             'inherited-projected-node-fields')
        index = point['index']
        need(type(index) is int and index not in projected_ids and index in byid, 'projected-index')
        projected_ids.add(index)
        for field in ('X', 'Z', 'R', 'U', 'v', 'Vr'):
            finite(point[field], 'inherited-projected-' + field)
        need(point['R'] > 0, 'positive-inherited-radius')
        for field, original_field in (('X', 'X'), ('Z', 'Z'), ('U', 'u'), ('v', 'v')):
            words += same_tree(point[field], byid[index]['original'][original_field],
                               'inherited-projected-original-' + field)
    need(set(memberships) == projected_ids and len(memberships) == 1220, 'inherited-complete-membership')
    need(type(old['regions']) is list and len(old['regions']) == 6
         and [region['id'] for region in old['regions']] == list(IDS), 'six-ordered-inherited-regions')
    for region in old['regions']:
        for resolution in ('full', 'coarse'):
            q = region[resolution]
            need(type(q) is dict and type(q['faces']) is dict and set(q['faces']) == set(FACES),
                 'non-null-inherited-quadrature')
            finite(q['defect'], 'saved-observed-defect')
            finite(q['fluxScale'], 'saved-observed-scale')
            need(q['fluxScale'] >= 0, 'nonnegative-saved-observed-scale')
            for name in FACES:
                face = q['faces'][name]
                coordinates = q['zCoordinates'] if name in ('inner', 'outer') else q['rCoordinates']
                need(type(face) is dict and set(face) == {'indices', 'integrand', 'value'}
                     and type(coordinates) is list and type(face['indices']) is list
                     and type(face['integrand']) is list and len(coordinates) >= 2
                     and len(face['indices']) == len(coordinates) == len(face['integrand']),
                     'inherited-face-array-shapes')
                need(len(set(face['indices'])) == len(face['indices'])
                     and all(type(index) is int and memberships.get(index) == region['id']
                             for index in face['indices']), 'inherited-face-region-nodes')
                for coordinate in coordinates:
                    finite(coordinate, 'saved-native-coordinate')
                need(all(coordinates[j] < coordinates[j + 1] for j in range(len(coordinates) - 1)),
                     'increasing-saved-native-coordinates')
                for value in face['integrand']:
                    finite(value, 'saved-measured-integrand')
                finite(face['value'], 'saved-measured-face-value')
    return byid, memberships, words


def independent_admission(projected, byid, memberships):
    nodes, failed_counts, issue_count = [], {region: 0 for region in IDS}, 0
    for point in projected:
        guard()
        case = byid[point['index']]
        issues = []
        if case.get('included') is not True:
            issues.append('model-not-included')
        if case.get('excludedReason', 'missing') is not None:
            issues.append('model-exclusion-reason')
        for field in FIELDS:
            if not is_finite(case.get(field)):
                issues.append('nonfinite-' + field)
        difference = None
        if is_finite(case.get('radius')):
            radius = D(case['radius'])
            difference = radius - D(point['R'])
            if radius <= 0:
                issues.append('nonpositive-radius')
            if abs(difference) > TOLERANCE:
                issues.append('radius-mismatch')
        if is_finite(case.get('xi')) and not Decimal(0) <= D(case['xi']) <= Decimal(2):
            issues.append('outside-core')
        region_id = memberships[point['index']]
        if issues:
            failed_counts[region_id] += 1
        issue_count += len(issues)
        nodes.append({'index': point['index'], 'regionId': region_id,
                      'issues': issues, 'radiusDifference': difference})
    return {'passed': issue_count == 0, 'nodes': nodes, 'regionFailures': failed_counts,
            'issuesCount': issue_count}


def check_admission(stored, expected, label):
    need(type(stored) is dict and set(stored) == set(expected), label + '-fields')
    for name in ('passed', 'regionFailures', 'issuesCount'):
        same_tree(stored[name], expected[name], label + '-' + name)
    need(type(stored['nodes']) is list and len(stored['nodes']) == len(expected['nodes']), label + '-node-count')
    for actual, reference in zip(stored['nodes'], expected['nodes']):
        need(type(actual) is dict and set(actual) == set(reference), label + '-node-fields')
        for name in ('index', 'regionId', 'issues'):
            same_tree(actual[name], reference[name], label + '-node-' + name)
        if reference['radiusDifference'] is None:
            need(actual['radiusDifference'] is None, label + '-nonfinite-radius-difference-null')
        else:
            # Subtract exact saved words in Decimal, then check the correctly rounded saved difference.
            same_word(actual['radiusDifference'], float(reference['radiusDifference']),
                      label + '-signed-radius-difference')


def weighted_integral(coordinates, values):
    """Native saved-coordinate nodal weights; never called on measured values alone."""
    need(len(coordinates) == len(values) and len(values) >= 2, 'quadrature-array-shapes')
    total = Decimal(0)
    for index, value in enumerate(values):
        weight = Decimal(0)
        if index:
            need(coordinates[index] > coordinates[index - 1], 'increasing-quadrature-coordinates')
            weight += (coordinates[index] - coordinates[index - 1]) / 2
        if index + 1 < len(coordinates):
            weight += (coordinates[index + 1] - coordinates[index]) / 2
        total += weight * value
    return total


def independent_comparison(q, byid, integration_radii):
    faces = {}
    for name in FACES:
        wall = name in ('inner', 'outer')
        sign = Decimal(-1 if name in ('inner', 'top') else 1)
        original_face = q['faces'][name]
        ids = original_face['indices']
        coordinates = q['zCoordinates'] if wall else q['rCoordinates']
        decimal_coordinates = [D(value) for value in coordinates]
        model_integrand = [D(integration_radii[index]) * D(byid[index]['radialCandidate' if wall else 'axialCore'])
                           for index in ids]
        errors = [sign * (model - D(observed))
                  for model, observed in zip(model_integrand, original_face['integrand'])]
        model_value = sign * weighted_integral(decimal_coordinates, model_integrand)
        # The observed integral is retained as the saved binary64 reference, not recalculated.
        face_error = model_value - D(original_face['value'])
        local_absolute = weighted_integral(decimal_coordinates, [abs(value) for value in errors])
        cancellation = local_absolute - abs(face_error)
        need(cancellation >= -TOLERANCE, 'reference-within-face-cancellation-inequality')
        faces[name] = {
            'indices': ids, 'coordinates': coordinates, 'observedIntegrand': original_face['integrand'],
            'modelIntegrand': model_integrand, 'localSignedError': errors,
            'observedValue': original_face['value'], 'modelValue': model_value,
            'signedError': face_error, 'localAbsoluteError': local_absolute,
            'withinFaceCancellation': cancellation,
        }
    model_sum = sum((face['modelValue'] for face in faces.values()), Decimal(0))
    error_sum = sum((face['signedError'] for face in faces.values()), Decimal(0))
    vector = sum((abs(face['signedError']) for face in faces.values()), Decimal(0))
    local = sum((face['localAbsoluteError'] for face in faces.values()), Decimal(0))
    observed_defect, observed_scale = D(q['defect']), D(q['fluxScale'])
    identity = error_sum - (model_sum - observed_defect)
    between, within = vector - abs(error_sum), local - vector
    need(abs(identity) <= TOLERANCE, 'reference-balance-identity')
    need(between >= -TOLERANCE and within >= -TOLERANCE, 'reference-cancellation-inequalities')
    return {
        'faces': faces, 'observedDefect': q['defect'], 'observedFluxScale': q['fluxScale'],
        'modelDefect': model_sum, 'errorSum': error_sum, 'balanceIdentityResidual': identity,
        'sumAbsoluteFaceError': vector, 'sumLocalAbsoluteError': local,
        'betweenFaceCancellation': between, 'withinFaceCancellation': within,
        'faceVectorFraction': vector / observed_scale if observed_scale else None,
        'localErrorFraction': local / observed_scale if observed_scale else None,
    }


def check_comparison(stored, expected, label):
    need(type(stored) is dict and set(stored) == set(expected), label + '-comparison-fields')
    need(type(stored['faces']) is dict and set(stored['faces']) == set(FACES), label + '-face-names')
    local_nodes = 0
    for name in FACES:
        actual, target = stored['faces'][name], expected['faces'][name]
        need(type(actual) is dict and set(actual) == set(target), label + '-' + name + '-fields')
        for field in ('indices', 'coordinates', 'observedIntegrand', 'observedValue'):
            same_tree(actual[field], target[field], label + '-' + name + '-' + field)
        for field in ('modelIntegrand', 'localSignedError'):
            need(type(actual[field]) is list and len(actual[field]) == len(target[field]),
                 label + '-' + name + '-' + field + '-count')
            for value, reference in zip(actual[field], target[field]):
                close(value, reference, label + '-' + name + '-' + field)
        for field in ('modelValue', 'signedError', 'localAbsoluteError', 'withinFaceCancellation'):
            close(actual[field], target[field], label + '-' + name + '-' + field)
        need(D(actual['withinFaceCancellation']) >= -TOLERANCE,
             label + '-' + name + '-saved-within-face-inequality')
        need(actual['localAbsoluteError'] >= 0, label + '-' + name + '-nonnegative-local-error')
        local_nodes += len(target['indices'])
    for field in ('observedDefect', 'observedFluxScale'):
        same_tree(stored[field], expected[field], label + '-unchanged-' + field)
    for field, reference in expected.items():
        if field in ('faces', 'observedDefect', 'observedFluxScale'):
            continue
        if reference is None:
            need(stored[field] is None, label + '-' + field + '-zero-observed-scale-null')
        else:
            close(stored[field], reference, label + '-' + field)
    need(abs(D(stored['balanceIdentityResidual'])) <= TOLERANCE, label + '-saved-balance-identity')
    need(D(stored['betweenFaceCancellation']) >= -TOLERANCE
         and D(stored['withinFaceCancellation']) >= -TOLERANCE, label + '-saved-cancellation-inequalities')
    need(stored['sumAbsoluteFaceError'] >= 0 and stored['sumLocalAbsoluteError'] >= 0,
         label + '-nonnegative-absolute-error-sums')
    return local_nodes


def check_differences(stored, full, coarse, label):
    need(type(stored) is dict and set(stored) == {'faces', 'faceVectorFraction', 'localErrorFraction'},
         label + '-difference-fields')
    need(type(stored['faces']) is dict and set(stored['faces']) == set(FACES), label + '-difference-faces')
    for name in FACES:
        actual = stored['faces'][name]
        need(type(actual) is dict and set(actual) == {'signedError', 'localAbsoluteError'},
             label + '-' + name + '-difference-fields')
        for field in ('signedError', 'localAbsoluteError'):
            close(actual[field], coarse['faces'][name][field] - full['faces'][name][field],
                  label + '-' + name + '-coarse-minus-full-' + field)
    for field in ('faceVectorFraction', 'localErrorFraction'):
        if full[field] is None or coarse[field] is None:
            need(stored[field] is None, label + '-' + field + '-undefined-difference')
        else:
            close(stored[field], coarse[field] - full[field], label + '-coarse-minus-full-' + field)


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-terminal-evaluator-directory')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved-boundary transport audit; no retries.\n')
    try:
        manifest_raw = read_local(BASE / 'source-manifest.json', 2 * MIB)
        manifest = parse_json(manifest_raw)
        publication_raw = read_local(BASE / 'source-publication.json', MIB)
        publication = parse_json(publication_raw)
        need(publication['manifestSha256'] == sha(manifest_raw)
             and publication['remoteBytesEqualLocal'] is True
             and publication['committedBytesEqualLocal'] is True, 'public-source-gate')
        verified = verify_manifest(manifest)
        need(not (RESULTS / 'failure.json').exists(), 'evaluator-failure-present')
        supervisor_raw = read_local(RESULTS / 'evaluate-supervisor.json', MIB)
        supervisor = parse_json(supervisor_raw)
        check_success(supervisor, 'evaluate', 'evaluator-supervised-success')
        later_files = {'evaluate-supervisor.json', 'audit.lock', 'audit-supervisor.lock',
                       'audit-stdout.txt', 'audit-stderr.txt'}
        saved_size = 0
        for directory in (RESULTS, BASE / 'ui'):
            if directory.exists():
                for path in directory.rglob('*'):
                    guard()
                    if path.is_file() and not (path.parent == RESULTS and path.name in later_files):
                        saved_size += path.stat().st_size
        need(saved_size == supervisor['savedBytesBeforeSupervisor'] and saved_size <= CAP, 'actual-saved-output-bytes')
        execution_raw = read_local(RESULTS / 'execution.json', MIB)
        execution = parse_json(execution_raw)
        body = read_local(RESULTS / 'comparison.json')
        need(execution['status'] == 'complete' and execution['resultBytes'] == len(body)
             and execution['sha256'] == sha(body) and 0 <= execution['elapsedSeconds'] < 60, 'completed-result-pin')
        result = parse_json(body)
        controls_raw = read_local(RESULTS / 'controls.json', MIB)
        same_tree(parse_json(controls_raw), {'passed': True, 'checks': CONTROL_NAMES}, 'saved-fixed-controls')
        admission_raw = read_local(RESULTS / 'admission.json')
        saved_admission = parse_json(admission_raw)
        need(type(result) is dict and set(result) == {'status', 'sourceCommit', 'inputPins', 'inheritedAnnular',
             'inheritedGain', 'admission', 'modelNodes', 'regions', 'limits'}, 'result-fields')
        need(result['sourceCommit'] == publication['commit'] and result['limits'] == LIMITS, 'result-identity-and-limits')
        docs, input_raws, provenance = {}, {}, {}
        for path, (size, digest) in PINS.items():
            raw = read_local(ROOT / path)
            need(len(raw) == size and sha(raw) == digest, 'immutable-saved-input-pin')
            input_raws[path], docs[path] = raw, parse_json(raw)
        same_tree(result['inputPins'], [pin(ROOT / path, input_raws[path]) for path in PINS], 'declared-input-pins')
        old, cross = docs[ANNULAR], docs[CROSS]
        for prefix, path in ((ANNULAR_PREFIX, ANNULAR), (CROSS_PREFIX, CROSS)):
            provenance.update(predecessor_chain(prefix, docs[path], input_raws[path]))
        words = same_tree(result['inheritedAnnular'], old, 'entire-inheritedAnnular')
        same_tree(result['inheritedGain'], cross['inheritedGain'], 'unchanged-inherited-gain')
        byid, memberships, original_words = inherited_structure(old, cross)
        words += original_words
        model_count, comparison_count, face_count, local_node_count = 0, 0, 0, 0
        with localcontext() as context:
            context.prec = 60
            expected_admission = independent_admission(old['projectedNodes'], byid, memberships)
            check_admission(saved_admission, expected_admission, 'saved-admission')
            check_admission(result['admission'], expected_admission, 'embedded-admission')
            admitted = expected_admission['passed']
            status = 'completed-face-transport' if admitted else 'admission-failed'
            need(result['status'] == status and execution['scientificStatus'] == status, 'terminal-admission-status')
            need(type(result['regions']) is list and len(result['regions']) == 6, 'six-region-results')
            if not admitted:
                same_tree(result['modelNodes'], [], 'no-model-nodes-after-failed-admission')
                same_tree(result['regions'], [{'id': region, 'full': None, 'coarse': None,
                           'coarseMinusFull': None} for region in IDS], 'global-null-transports-after-failed-admission')
            else:
                # Copies only: integration geometry and fields retain their exact inherited words.
                expected_nodes = [{'index': point['index'], 'integrationRadius': point['R'],
                                   **{field: byid[point['index']][field] for field in FIELDS}}
                                  for point in old['projectedNodes']]
                words += same_tree(result['modelNodes'], expected_nodes, 'copied-model-nodes-and-integration-radius')
                model_count = len(expected_nodes)
                integration_radii = {point['index']: point['R'] for point in old['projectedNodes']}
                for inherited_region, stored in zip(old['regions'], result['regions']):
                    guard()
                    need(type(stored) is dict and set(stored) == {'id', 'full', 'coarse', 'coarseMinusFull'}
                         and stored['id'] == inherited_region['id'], 'ordered-region-identity')
                    full = independent_comparison(inherited_region['full'], byid, integration_radii)
                    coarse = independent_comparison(inherited_region['coarse'], byid, integration_radii)
                    local_node_count += check_comparison(stored['full'], full, stored['id'] + '-full')
                    local_node_count += check_comparison(stored['coarse'], coarse, stored['id'] + '-coarse')
                    check_differences(stored['coarseMinusFull'], full, coarse, stored['id'])
                    comparison_count += 2
                    face_count += 8
        need(verify_manifest(manifest) == verified, 'post-audit-source-pins')
        retained = {BASE / 'source-manifest.json': manifest_raw, BASE / 'source-publication.json': publication_raw,
                    RESULTS / 'comparison.json': body, RESULTS / 'execution.json': execution_raw,
                    RESULTS / 'controls.json': controls_raw, RESULTS / 'admission.json': admission_raw,
                    RESULTS / 'evaluate-supervisor.json': supervisor_raw}
        retained.update({ROOT / path: raw for path, raw in input_raws.items()})
        retained.update({ROOT / path: raw for path, raw in provenance.items()})
        for path, raw in retained.items():
            need(read_local(path) == raw, 'unchanged-source-input-admission-result-receipts')
        guard()
        report = {
            'schema': 'm31-face-transport-independent-audit-v1', 'passed': True, 'complete': True,
            'scientificStatus': status, 'sourceManifestSha256': sha(manifest_raw), 'verifiedSourcePins': verified,
            'publicationPin': pin(BASE / 'source-publication.json', publication_raw),
            'inputPins': [pin(ROOT / path, input_raws[path]) for path in PINS],
            'resultPin': pin(RESULTS / 'comparison.json', body),
            'admissionPin': pin(RESULTS / 'admission.json', admission_raw),
            'evaluatorSupervisorPin': pin(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
            'originalCasesChecked': 3240, 'entireInheritedAnnularPreserved': True,
            'recursivelyPreservedBinary64Words': words, 'selectedModelNodesAdmissionChecked': 1220,
            'admissionChecked': {'passed': admitted, 'regionFailures': expected_admission['regionFailures'],
                                 'issuesCount': expected_admission['issuesCount']},
            'modelNodesChecked': model_count, 'comparisonsChecked': comparison_count,
            'orientedFacesChecked': face_count, 'faceLocalNodesCheckedWithRepetition': local_node_count,
            'admissionFailureHasNoModelNodesOrTransports': not admitted,
            'arithmetic': 'Independent Decimal60 nodal weights on exact saved native coordinates, inherited annular R and unchanged saved model fields; saved measured integrands for local errors, saved measured integrals/scale/defect as references.',
            'tolerance': '2e-12 absolute numerical consistency only; exact recursive input words and structures. Radius admission disagreement fails without widening.',
            'measuredQuadraturesRecomputed': 0, 'newSquareRoots': 0, 'newFits': 0, 'newFieldEvaluations': 0,
            'sourcesPreserved': True, 'inputPreserved': True, 'resultsPreserved': True,
            'independentPhysicalValidation': False,
            'scope': 'Fixed exposed same-experiment boundary transport comparison. Sampled nodal absolute errors and numerical cancellation are not physical uncertainty, model accuracy percentages or whole-field RMS decomposition.',
            'elapsedSeconds': time.monotonic() - START,
        }
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'scientificStatus': status, 'modelNodesChecked': model_count,
                          'comparisonsChecked': comparison_count, 'orientedFacesChecked': face_count}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()


