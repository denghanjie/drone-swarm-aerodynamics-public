"""Independent saved annular diagnostic audit; no producer or physics imports.

Run once only after the new exact-public source freeze and sole evaluator.
No synthetic controls or measurements are processed on import.
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
PAIRED = 'research/m31-lateral-symmetry-2026-10-19/'
AIRFLOW = 'research/m31-airflow-test-2026-10-19/'
INPUT = PAIRED + 'results/comparison.json'
UPSTREAM = AIRFLOW + 'results/comparison.json'
PINS = {
    INPUT: (3793293, 'b253b7199df24e8a2d5ff3000bed1f73937cd898ada8449256c91f0172962be3'),
    UPSTREAM: (1112834, 'dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3'),
}
PUBLICATIONS = {
    PAIRED: 'research/publication-receipts/m31-lateral-symmetry-result-2026-10-19.json',
    AIRFLOW: 'research/publication-receipts/m31-airflow-result-2026-10-19.json',
}
PREDECESSOR_FILES = {
    'PROTOCOL.md', 'source-manifest.json', 'source-publication.json', 'result-manifest.json',
    'results/comparison.json', 'results/execution.json', 'results/evaluate-supervisor.json',
    'results/audit.json', 'results/audit-supervisor.json',
}
BANDS = (('lower', 12., 16., False), ('middle', 16., 20., False), ('upper', 20., 24., True))
FACE_NAMES = ('inner', 'outer', 'top', 'bottom')
ORIGINAL_FIELDS = {'row', 'column', 'index', 'X', 'Z', 'u', 'v', 'a', 'b', 'residualA', 'residualB'}
LIMITS = [
    'Exposed retained stride-four field, not complete raw PIV or independent trials',
    'Axisymmetric no-mean-swirl projection on Y=1 is conditional',
    'Unknown actual component calibration and stitching uncertainty',
    'No physical pass threshold, significance or experimental error bound',
    'Fixed coarsening is sensitivity, not convergence or measurement uncertainty',
    'No new model prediction, fit, physical validity, force/swarm safety or novelty',
]
CONTROL_NAMES = [
    'both-side irregular-grid divergence-free faces and balance',
    'reflected projection and orientation', 'known nonzero volume source',
    'shared positive scale invariance', 'negative common scale sign and magnitude',
    'constant axial flow cancellation', 'zero integrated flux null fractions',
    'fixed coarse endpoints', 'missing node rejected', 'duplicate node rejected',
    'nonfinite component rejected', 'insufficient axes rejected',
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


def validate_originals(rows, counts):
    need(type(rows) is list and len(rows) == 3240, 'original-case-count')
    need(type(counts) is dict, 'upstream-counts-object')
    for field in ('nonfiniteCoordinates', 'missingU', 'accepted'):
        need(type(counts[field]) is int and counts[field] >= 0, 'upstream-count-type-' + field)
    need(counts['accepted'] == len(rows), 'upstream-accepted-count')
    byid = {}
    for original in rows:
        guard()
        need(type(original) is dict and set(original) == ORIGINAL_FIELDS, 'original-fields')
        index = original['index']
        need(type(index) is int and index not in byid, 'unique-original-index')
        need(type(original['row']) is int and type(original['column']) is int, 'original-grid-index-types')
        finite(original['X'], 'original-X')
        finite(original['Z'], 'original-Z')
        for component in ('u', 'v'):
            value = original[component]
            need(value is None or type(value) in (int, float), 'original-component-type')
        byid[index] = original
    return byid


def independent_selection(rows, counts):
    """Decimal membership and a word-keyed coordinate census; no response/model selection."""
    regions, memberships, all_issues = [], {}, []
    if counts['nonfiniteCoordinates'] != 0:
        all_issues.append('upstream-nonfinite-coordinates')
    if counts['missingU'] != 0:
        all_issues.append('upstream-missing-axial')
    for side in ('left', 'right'):
        for label, low, high, inclusive in BANDS:
            chosen = []
            for original in rows:
                x, z = D(original['X']), D(original['Z'])
                sign_matches = x < 0 if side == 'left' else x > 0
                upper_matches = z <= D(high) if inclusive else z < D(high)
                if sign_matches and 1 <= abs(x) <= 3 and D(low) <= z and upper_matches:
                    chosen.append(original)
            x_words, z_words, cells = {}, {}, {}
            for original in chosen:
                x_key, z_key = struct.pack('>d', original['X']), struct.pack('>d', original['Z'])
                x_words[x_key], z_words[z_key] = original['X'], original['Z']
                cells.setdefault((x_key, z_key), []).append(original['index'])
            xs = sorted(x_words.values(), key=lambda value: abs(D(value)))
            zs = sorted(z_words.values(), key=D)
            duplicates = sorted(index for indices in cells.values() if len(indices) != 1 for index in indices)
            missing_count = len(xs) * len(zs) - len(cells)
            missing_preview, lattice = [], []
            if missing_count:
                # At most one absent coordinate is materialized. No absent-product expansion.
                for z in zs:
                    guard()
                    z_key = struct.pack('>d', z)
                    absent = next((x for x in xs if (struct.pack('>d', x), z_key) not in cells), None)
                    if absent is not None:
                        missing_preview.append({'X': absent, 'Z': z})
                        break
                need(len(missing_preview) == 1, 'missing-coordinate-preview-exists')
            elif not duplicates:
                for z in zs:
                    guard()
                    lattice.append([cells[(struct.pack('>d', x), struct.pack('>d', z))][0] for x in xs])
            nonfinite = sorted(original['index'] for original in chosen
                               if not is_finite(original['u']) or not is_finite(original['v']))
            issues = []
            if duplicates:
                issues.append('duplicate-coordinate')
            if missing_count:
                issues.append('incomplete-tensor-grid')
            if len(xs) < 5 or len(zs) < 5:
                issues.append('insufficient-axis-levels')
            if nonfinite:
                issues.append('nonfinite-selected-component')
            region_id = side + '-' + label
            for original in chosen:
                need(original['index'] not in memberships, 'disjoint-windows')
                memberships[original['index']] = region_id
            regions.append({
                'id': region_id, 'side': side,
                'nominalBand': {'lo': low, 'hi': high, 'upperInclusive': inclusive},
                'selectedIndices': [original['index'] for original in chosen],
                'xLevels': xs, 'zLevels': zs, 'nodeIndices': lattice,
                'geometry': {'xLevels': len(xs), 'zLevels': len(zs), 'selectedCount': len(chosen),
                    'uniqueCoordinateCount': len(cells), 'expectedCount': len(xs) * len(zs),
                    'minAbsX': abs(xs[0]) if xs else None, 'maxAbsX': abs(xs[-1]) if xs else None,
                    'minZ': zs[0] if zs else None, 'maxZ': zs[-1] if zs else None},
                'issues': issues, 'duplicateIndices': duplicates,
                'missingCoordinateCount': missing_count, 'missingCoordinatePreview': missing_preview,
                'nonfiniteIndices': nonfinite,
            })
            all_issues.extend(region_id + ':' + issue for issue in issues)
    need(len(regions) == 6 and len(memberships) <= 3240, 'selection-size-bounds')
    return {
        'admission': {'passed': not all_issues, 'issues': all_issues,
                      'upstreamNonfiniteCoordinates': counts['nonfiniteCoordinates'],
                      'upstreamMissingU': counts['missingU']},
        'membership': [{'index': original['index'], 'regionId': memberships.get(original['index']),
                        'reason': 'selected' if original['index'] in memberships else 'outside-windows'}
                       for original in rows],
        'selectedCount': len(memberships), 'outsideCount': len(rows) - len(memberships), 'regions': regions,
    }


def independent_projection(original):
    x, u, v = D(original['X']), D(original['u']), D(original['v'])
    radius_squared = x * x + 1
    radius = radius_squared.sqrt()
    return {'R': radius, 'Vr': radius * v / x, 'axialIntegrand': radius * u,
            'radialIntegrand': radius_squared * v / x}


def weighted_integral(coordinates, values):
    """Nodal-weight trapezoid, independent of producer segment accumulation."""
    need(len(coordinates) == len(values) and len(values) >= 2, 'quadrature-shape')
    total = Decimal(0)
    for index, value in enumerate(values):
        weight = Decimal(0)
        if index:
            need(coordinates[index] > coordinates[index - 1], 'quadrature-increasing-coordinates')
            weight += (coordinates[index] - coordinates[index - 1]) / 2
        if index + 1 < len(coordinates):
            weight += (coordinates[index + 1] - coordinates[index]) / 2
        total += weight * value
    return total


def independent_quadrature(region, projections, coarse):
    nx, nz = len(region['xLevels']), len(region['zLevels'])
    radial = [index for index in range(nx) if not coarse or index % 2 == 0 or index == nx - 1]
    axial = [index for index in range(nz) if not coarse or index % 2 == 0 or index == nz - 1]
    need(radial[0] == 0 and radial[-1] == nx - 1 and axial[0] == 0 and axial[-1] == nz - 1,
         'same-full-coarse-boundaries')
    radii = [(D(region['xLevels'][index]) ** 2 + 1).sqrt() for index in radial]
    heights = [D(region['zLevels'][index]) for index in axial]
    grid = region['nodeIndices']
    face_indices = {
        'inner': [grid[index][0] for index in axial],
        'outer': [grid[index][nx - 1] for index in axial],
        'top': [grid[0][index] for index in radial],
        'bottom': [grid[nz - 1][index] for index in radial],
    }
    faces = {}
    for name in FACE_NAMES:
        horizontal = name in ('top', 'bottom')
        integrands = [projections[index]['axialIntegrand' if horizontal else 'radialIntegrand']
                      for index in face_indices[name]]
        signed = weighted_integral(radii if horizontal else heights, integrands)
        if name in ('inner', 'top'):
            signed = -signed
        faces[name] = {'indices': face_indices[name], 'integrand': integrands, 'value': signed}
    total = sum((faces[name]['value'] for name in FACE_NAMES), Decimal(0))
    scale = sum((abs(faces[name]['value']) for name in FACE_NAMES), Decimal(0))
    return {'radialPositions': radial, 'axialPositions': axial, 'rCoordinates': radii,
            'zCoordinates': [region['zLevels'][index] for index in axial], 'faces': faces,
            'defect': total, 'fluxScale': scale, 'signedFraction': total / scale if scale else None,
            'absoluteFraction': abs(total) / scale if scale else None}


def check_quadrature(stored, expected, label):
    need(type(stored) is dict and set(stored) == set(expected), label + '-quadrature-fields')
    for name in ('radialPositions', 'axialPositions', 'zCoordinates'):
        same_tree(stored[name], expected[name], label + '-' + name)
    need(type(stored['rCoordinates']) is list and len(stored['rCoordinates']) == len(expected['rCoordinates']),
         label + '-radial-coordinate-count')
    for actual, target in zip(stored['rCoordinates'], expected['rCoordinates']):
        close(actual, target, label + '-radial-coordinate')
    need(type(stored['faces']) is dict and set(stored['faces']) == set(FACE_NAMES), label + '-face-names')
    for name in FACE_NAMES:
        actual, target = stored['faces'][name], expected['faces'][name]
        need(type(actual) is dict and set(actual) == {'indices', 'integrand', 'value'}, label + '-face-fields')
        same_tree(actual['indices'], target['indices'], label + '-' + name + '-indices')
        need(type(actual['integrand']) is list and len(actual['integrand']) == len(target['integrand']),
             label + '-integrand-count')
        for value, reference in zip(actual['integrand'], target['integrand']):
            close(value, reference, label + '-' + name + '-integrand')
        close(actual['value'], target['value'], label + '-' + name + '-oriented-flux')
    for name in ('defect', 'fluxScale', 'signedFraction', 'absoluteFraction'):
        if expected[name] is None:
            need(stored[name] is None, label + '-' + name + '-null-zero-face-scale')
        else:
            close(stored[name], expected[name], label + '-' + name)
    # Independently check the exact zero/nonzero branch chosen on saved face integrals.
    saved_scale = sum((abs(D(stored['faces'][name]['value'])) for name in FACE_NAMES), Decimal(0))
    need((saved_scale == 0) == (expected['fluxScale'] == 0), label + '-zero-scale-branch')
    close(stored['fluxScale'], saved_scale, label + '-saved-integrated-face-scale')


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-terminal-evaluator-directory')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved annular diagnostic audit; no retries.\n')
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
        selection_raw = read_local(RESULTS / 'selection.json')
        selection = parse_json(selection_raw)
        need(type(result) is dict and set(result) == {'status', 'sourceCommit', 'inputs', 'originalCases',
             'fullFieldSubsets', 'upstreamCounts', 'selection', 'projectedNodes', 'regions', 'limits'}, 'result-fields')
        need(result['sourceCommit'] == publication['commit'] and result['limits'] == LIMITS, 'result-identity-and-limits')
        docs, input_raws, provenance = {}, {}, {}
        for path, (size, digest) in PINS.items():
            raw = read_local(ROOT / path)
            need(len(raw) == size and sha(raw) == digest, 'immutable-saved-input-pin')
            input_raws[path], docs[path] = raw, parse_json(raw)
        same_tree(result['inputs'], [pin(ROOT / path, input_raws[path]) for path in PINS], 'declared-input-pins')
        old, upstream = docs[INPUT], docs[UPSTREAM]
        need(old['status'] == 'completed-paired-support-diagnostic'
             and upstream['status'] == 'completed-descriptive-airflow-comparison', 'predecessor-completed-status')
        for prefix, path in ((PAIRED, INPUT), (AIRFLOW, UPSTREAM)):
            provenance.update(predecessor_chain(prefix, docs[path], input_raws[path]))
        originals = old['originalCases']
        need(type(originals) is list and len(originals) == 3240, 'original-nested-case-count')
        rows = [case['original'] for case in originals]
        words = same_tree(rows, upstream['cases'], 'upstream-exact-original-rows')
        words += same_tree(result['originalCases'], originals, 'originalCases')
        words += same_tree(result['fullFieldSubsets'], old['fullFieldSubsets'], 'fullFieldSubsets')
        words += same_tree(result['upstreamCounts'], upstream['counts'], 'upstreamCounts')
        validate_originals(rows, upstream['counts'])
        projected_count, quadrature_count, face_count = 0, 0, 0
        with localcontext() as context:
            context.prec = 60
            expected_selection = independent_selection(rows, upstream['counts'])
            same_tree(selection, expected_selection, 'saved-selection-trace')
            same_tree(result['selection'], expected_selection, 'embedded-selection-trace')
            admitted = expected_selection['admission']['passed']
            status = 'completed-annular-balance' if admitted else 'admission-failed'
            need(result['status'] == status and execution['scientificStatus'] == status, 'terminal-admission-status')
            need(type(result['regions']) is list and len(result['regions']) == 6, 'six-region-results')
            if not admitted:
                same_tree(result['projectedNodes'], [], 'no-projected-nodes-after-failed-admission')
                same_tree(result['regions'], [{'id': region['id'], 'full': None, 'coarse': None,
                           'coarseMinusFull': None} for region in expected_selection['regions']],
                          'global-null-flux-after-failed-admission')
            else:
                selected = {entry['index'] for entry in expected_selection['membership']
                            if entry['regionId'] is not None}
                chosen = [original for original in rows if original['index'] in selected]
                stored_nodes = result['projectedNodes']
                need(type(stored_nodes) is list and len(stored_nodes) == len(chosen), 'projected-node-count')
                projections = {}
                for original, stored in zip(chosen, stored_nodes):
                    guard()
                    need(type(stored) is dict and set(stored) == {'index', 'X', 'Z', 'R', 'U', 'v', 'Vr'},
                         'projected-node-fields')
                    for field, source in (('index', 'index'), ('X', 'X'), ('Z', 'Z'), ('U', 'u'), ('v', 'v')):
                        same_tree(stored[field], original[source], 'projected-original-' + field)
                    reference = independent_projection(original)
                    for field in ('R', 'Vr'):
                        close(stored[field], reference[field], 'projected-' + field)
                    projections[original['index']] = reference
                projected_count = len(chosen)
                for geometry, stored in zip(expected_selection['regions'], result['regions']):
                    guard()
                    need(type(stored) is dict and set(stored) == {'id', 'full', 'coarse', 'coarseMinusFull'}
                         and stored['id'] == geometry['id'], 'ordered-region-identity')
                    full = independent_quadrature(geometry, projections, False)
                    coarse = independent_quadrature(geometry, projections, True)
                    check_quadrature(stored['full'], full, geometry['id'] + '-full')
                    check_quadrature(stored['coarse'], coarse, geometry['id'] + '-coarse')
                    difference = stored['coarseMinusFull']
                    need(type(difference) is dict and set(difference) == {'defect', 'signedFraction'},
                         'coarse-minus-full-fields')
                    close(difference['defect'], coarse['defect'] - full['defect'], 'coarse-minus-full-defect')
                    if full['signedFraction'] is None or coarse['signedFraction'] is None:
                        need(difference['signedFraction'] is None, 'coarse-minus-full-undefined-fraction')
                    else:
                        close(difference['signedFraction'], coarse['signedFraction'] - full['signedFraction'],
                              'coarse-minus-full-signed-fraction')
                    quadrature_count += 2
                    face_count += 8
        need(verify_manifest(manifest) == verified, 'post-audit-source-pins')
        retained = {BASE / 'source-manifest.json': manifest_raw, BASE / 'source-publication.json': publication_raw,
                    RESULTS / 'comparison.json': body, RESULTS / 'execution.json': execution_raw,
                    RESULTS / 'controls.json': controls_raw, RESULTS / 'selection.json': selection_raw,
                    RESULTS / 'evaluate-supervisor.json': supervisor_raw}
        retained.update({ROOT / path: raw for path, raw in input_raws.items()})
        retained.update({ROOT / path: raw for path, raw in provenance.items()})
        for path, raw in retained.items():
            need(read_local(path) == raw, 'unchanged-source-input-selection-result-receipts')
        guard()
        report = {
            'schema': 'm31-annular-balance-independent-audit-v1', 'passed': True, 'complete': True,
            'scientificStatus': status, 'sourceManifestSha256': sha(manifest_raw), 'verifiedSourcePins': verified,
            'publicationPin': pin(BASE / 'source-publication.json', publication_raw),
            'inputPins': [pin(ROOT / path, input_raws[path]) for path in PINS],
            'resultPin': pin(RESULTS / 'comparison.json', body),
            'selectionPin': pin(RESULTS / 'selection.json', selection_raw),
            'evaluatorSupervisorPin': pin(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
            'originalCasesChecked': len(rows), 'recursivelyPreservedBinary64Words': words,
            'selectionWindowsChecked': 6, 'selectedNodesChecked': expected_selection['selectedCount'],
            'admissionChecked': expected_selection['admission'], 'projectedNodesChecked': projected_count,
            'quadraturesChecked': quadrature_count, 'orientedFacesChecked': face_count,
            'admissionFailureHasNoProjectedNodesOrFlux': not admitted,
            'arithmetic': 'Independent Decimal60 geometry, radial projection and native-R/Z nodal-weight trapezoids from originals; no producer imports, field/model evaluation or fit.',
            'tolerance': '2e-12 absolute numerical consistency only. Original JSON types and binary64 words, coordinate membership and grid/null branches are exact.',
            'newFits': 0, 'newFieldEvaluations': 0, 'sourcesPreserved': True, 'inputPreserved': True,
            'resultsPreserved': True, 'independentPhysicalValidation': False,
            'scope': 'Six fixed conditional annular reconstructions from exposed retained stride-four planar measurements. No physical threshold or experimental uncertainty estimate.',
            'elapsedSeconds': time.monotonic() - START,
        }
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'scientificStatus': status, 'selectionWindowsChecked': 6,
                          'projectedNodesChecked': projected_count, 'quadraturesChecked': quadrature_count}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()
