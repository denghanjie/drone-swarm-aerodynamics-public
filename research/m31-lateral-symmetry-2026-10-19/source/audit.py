"""One independent saved-value pairing audit; no producer or physics imports.
Launch only after the new public source freeze and successful sole evaluator.
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
MATCH_LIMIT = Decimal('.01')
PREVIOUS = 'research/m31-crossstream-test-2026-10-19/'
INPUT = PREVIOUS + 'results/comparison.json'
INPUT_BYTES = 2291932
INPUT_SHA = '1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a'
GAIN = .5450089857597356
PUBLICATIONS = {PREVIOUS: 'research/publication-receipts/m31-crossstream-result-2026-10-19.json'}
PREDECESSOR_FILES = {'PROTOCOL.md', 'source-manifest.json', 'source-publication.json',
                     'result-manifest.json', 'results/comparison.json', 'results/execution.json',
                     'results/evaluate-supervisor.json', 'results/audit.json', 'results/audit-supervisor.json'}
REASONS = ('prior-excluded', 'axis', 'no-eligible-counterpart', 'ambiguous-counterparts', 'counterpart-ambiguous', 'paired')
REGIONS = ('primary', 'near', 'middle', 'far')
COMPONENTS = ('observedE', 'observedO', 'predictedE', 'predictedO', 'errorE', 'errorO')
ENERGIES = ('directSSE', 'evenSSE', 'oddSSE')
LIMITS = ['Previously exposed same-experiment paired-support diagnostic',
          'Approximate mirror geometry; components are not exact field parity',
          'No model fit, center shift, interpolation, field evaluation or component removal',
          'No causal identification of swirl, drift, asymmetry or measurement error',
          'No SI calibration, independent physical validation, force/swarm safety or novelty',
          'Algebraic energy identity is not physical evidence']


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


def finite(value, label):
    need(type(value) in (int, float) and math.isfinite(value), label + '-finite-number')


def close(actual, expected, label):
    finite(actual, label)
    need(abs(D(actual) - D(expected)) <= TOLERANCE, label + '-absolute-tolerance')


def same_word(actual, expected, label):
    finite(actual, label)
    need(struct.pack('>d', actual) == struct.pack('>d', expected), label + '-binary64-word')


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
    result_manifest_raw = retained[prefix + 'result-manifest.json']
    publication = parse_json(retained[publication_path])
    need(publication['manifestPath'] == prefix + 'result-manifest.json'
         and publication['manifestBytes'] == len(result_manifest_raw)
         and publication['manifestSha256'] == sha(result_manifest_raw)
         and publication['remoteBytesEqualLocal'] is True
         and publication['committedBytesEqualLocal'] is True, 'prior-public-result-binding')
    matching = [entry for entry in parse_json(result_manifest_raw)['files']
                if entry['path'] == prefix + 'results/comparison.json']
    need(matching == [pin(result_path, raw)], 'prior-published-result-pin')
    return retained



def same_tree(actual, expected, label):
    """Exact recursive JSON preservation, including float sign bits and types."""
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
                'source/supervise.py', 'review/SOURCE-AUDIT.md', 'review/PAIR-DECOMPOSITION.md')}
    required |= {PREVIOUS + name for name in PREDECESSOR_FILES}
    required.add(PUBLICATIONS[PREVIOUS])
    need(required <= names, 'manifest-required-inputs-and-provenance')
    return len(entries)


def independent_matching(rows):
    """Explicit bipartite graph, keyed by original Z word; no response inputs."""
    byid, levels, adj = {}, {}, {}
    for row in rows:
        original = row['original']
        index = original['index']
        need(type(index) is int and index not in byid, 'unique-original-index')
        finite(original['X'], 'original-X')
        finite(original['Z'], 'original-Z')
        need(type(row['included']) is bool and 8 <= original['Z'] <= 30
             and abs(original['X']) <= 4, 'original-domain-and-inclusion-type')
        byid[index] = row
        adj[index] = set()
        if row['included']:
            finite(original['v'], 'included-measurement')
            finite(row['candidate'], 'included-candidate')
            if original['X'] != 0:
                key = struct.pack('>d', original['Z'])
                if key not in levels:
                    levels[key] = {'left': [], 'right': []}
                levels[key]['left' if original['X'] < 0 else 'right'].append(index)
    comparisons = 0
    coordinates = {index: D(row['original']['X']) for index, row in byid.items()}
    for sides in levels.values():
        comparisons += len(sides['left']) * len(sides['right'])
        need(comparisons <= 10497600, 'eligibility-comparison-bound')
        for left in sides['left']:
            guard()
            for right in sides['right']:
                if abs(coordinates[left] + coordinates[right]) <= MATCH_LIMIT:
                    adj[left].add(right)
                    adj[right].add(left)
    links = []
    for right in sorted(byid):
        if byid[right]['original']['X'] > 0 and len(adj[right]) == 1:
            left = next(iter(adj[right]))
            if len(adj[left]) == 1:
                links.append((left, right))
    memberships = {}
    for pair_id, (left, right) in enumerate(links):
        need(left not in memberships and right not in memberships, 'no-cell-reuse')
        memberships[left] = pair_id
        memberships[right] = pair_id
    table, counts = [], {reason: 0 for reason in REASONS}
    for row in rows:
        index = row['original']['index']
        neighbors = sorted(adj[index])
        if not row['included']:
            reason = 'prior-excluded'
        elif row['original']['X'] == 0:
            reason = 'axis'
        elif len(neighbors) == 0:
            reason = 'no-eligible-counterpart'
        elif len(neighbors) > 1:
            reason = 'ambiguous-counterparts'
        elif len(adj[neighbors[0]]) > 1:
            reason = 'counterpart-ambiguous'
        else:
            reason = 'paired'
        need((reason == 'paired') == (index in memberships), 'matching-reason-partition')
        counts[reason] += 1
        table.append({'index': index, 'reason': reason, 'pairId': memberships.get(index),
                      'partnerIndex': neighbors[0] if reason == 'paired' else None,
                      'eligibleNeighbors': neighbors})
    need(sum(counts.values()) == len(rows) and counts['paired'] == 2 * len(links), 'matching-counts')
    return byid, links, table, counts, comparisons


def belongs(z, region):
    if region == 'primary':
        return z >= 12
    if region == 'near':
        return z < 12
    if region == 'middle':
        return 12 <= z < 20
    need(region == 'far', 'known-region')
    return z >= 20


def independent_components(left, right):
    vl, vr = D(left['original']['v']), D(right['original']['v'])
    pl, pr = D(left['candidate']), D(right['candidate'])
    el, er = pl - vl, pr - vr
    observed_e, observed_o = (vr + vl) / 2, (vr - vl) / 2
    predicted_e, predicted_o = (pr + pl) / 2, (pr - pl) / 2
    # Residual-first arithmetic differs from producer subtraction of components.
    error_e, error_o = (er + el) / 2, (er - el) / 2
    direct = er * er + el * el
    even, odd = 2 * error_e * error_e, 2 * error_o * error_o
    need(abs(direct - even - odd) <= TOLERANCE, 'independent-pair-energy-identity')
    return {'observedE': observed_e, 'observedO': observed_o, 'predictedE': predicted_e,
            'predictedO': predicted_o, 'errorE': error_e, 'errorO': error_o,
            'directSSE': direct, 'evenSSE': even, 'oddSSE': odd}


def independent_side_metrics(records, baseline):
    if not records:
        return None
    errors = [(Decimal(0) if baseline else D(record['candidate'])) - D(record['original']['v'])
              for record in records]
    n = Decimal(len(errors))
    return {'count': len(errors), 'mae': sum(abs(error) for error in errors) / n,
            'rmse': (sum(error * error for error in errors) / n).sqrt(), 'bias': sum(errors) / n}


def independent_summary(pairs, byid):
    if not pairs:
        return None
    n = Decimal(len(pairs))
    rms = {field: (sum(pair[field] * pair[field] for pair in pairs) / n).sqrt() for field in COMPONENTS}
    direct, even, odd = (sum(pair[field] for pair in pairs) for field in ENERGIES)
    need(abs(direct - even - odd) <= TOLERANCE, 'independent-pooled-energy-identity')
    total = even + odd
    sides = {}
    for label, keys in [('left', ('leftIndex',)), ('right', ('rightIndex',)), ('joint', ('leftIndex', 'rightIndex'))]:
        records = [byid[pair[key]] for pair in pairs for key in keys]
        sides[label] = {'baseline': independent_side_metrics(records, True),
                        'candidate': independent_side_metrics(records, False)}
    return {'rms': rms, 'directSSE': direct, 'evenSSE': even, 'oddSSE': odd,
            'energyShareE': even / total if total > 0 else None,
            'energyShareO': odd / total if total > 0 else None,
            'pairedCandidateRMSE': (direct / (2 * n)).sqrt(),
            'maxAbsXSum': max(pair['absXSum'] for pair in pairs), 'sides': sides}


def check_summary(stored, expected, label):
    if expected is None:
        need(stored is None, label + '-empty-summary-null')
        return
    need(type(stored) is dict and set(stored) == set(expected), label + '-summary-fields')
    need(type(stored['rms']) is dict and set(stored['rms']) == set(COMPONENTS), label + '-rms-fields')
    for field, value in expected['rms'].items():
        close(stored['rms'][field], value, label + '-rms-' + field)
    for field in (*ENERGIES, 'energyShareE', 'energyShareO', 'pairedCandidateRMSE', 'maxAbsXSum'):
        if expected[field] is None:
            need(stored[field] is None, label + '-' + field + '-zero-energy-null')
        else:
            close(stored[field], expected[field], label + '-' + field)
    need(abs(stored['directSSE'] - stored['evenSSE'] - stored['oddSSE']) <= 2e-12, label + '-saved-energy-identity')
    need(type(stored['sides']) is dict and set(stored['sides']) == {'left', 'right', 'joint'}, label + '-sides')
    for side in ('left', 'right', 'joint'):
        need(type(stored['sides'][side]) is dict and set(stored['sides'][side]) == {'baseline', 'candidate'}, label + '-models')
        for model in ('baseline', 'candidate'):
            actual, target = stored['sides'][side][model], expected['sides'][side][model]
            need(type(actual) is dict and set(actual) == {'count', 'mae', 'rmse', 'bias'}
                 and type(actual['count']) is int and actual['count'] == target['count'], label + '-side-metric-fields-count')
            for field in ('mae', 'rmse', 'bias'):
                close(actual[field], target[field], label + '-' + side + '-' + model + '-' + field)
    close(stored['pairedCandidateRMSE'], expected['sides']['joint']['candidate']['rmse'], label + '-joint-rmse-consistency')


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-completed-evaluator-directory')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved paired-support audit; no retries.\n')
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
        later_files = {'evaluate-supervisor.json', 'audit.lock', 'audit-supervisor.lock', 'audit-stdout.txt', 'audit-stderr.txt'}
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
        need(parse_json(controls_raw) == {'passed': True, 'checks': [
             'pure same-direction component', 'pure opposite-direction component', 'mixed residual identity',
             'perfect agreement with null energy fractions', 'exact mutual matching', 'response invariance',
             'outside tolerance rejected', 'same sign and unequal Z rejected', 'mutual ambiguity rejected',
             'axis and prior exclusion precedence', 'empty group null']}, 'saved-fixed-controls')
        selection_raw = read_local(RESULTS / 'selection.json')
        selection = parse_json(selection_raw)
        need(type(result) is dict and set(result) == {'status', 'sourceCommit', 'inputPin', 'inheritedGain',
             'originalCases', 'fullFieldSubsets', 'matching', 'countsByReason', 'eligibilityComparisons',
             'pairs', 'groups', 'limits'}, 'result-fields')
        need(result['status'] == 'completed-paired-support-diagnostic'
             and result['sourceCommit'] == publication['commit'] and result['limits'] == LIMITS, 'result-identity-and-limits')
        input_raw = read_local(ROOT / INPUT)
        need(len(input_raw) == INPUT_BYTES and sha(input_raw) == INPUT_SHA, 'immutable-saved-input-pin')
        need(result['inputPin'] == pin(ROOT / INPUT, input_raw), 'declared-input-pin')
        old = parse_json(input_raw)
        need(old['status'] == 'completed-cross-component-diagnostic', 'predecessor-completed-status')
        same_word(old['inheritedGain'], GAIN, 'predecessor-exact-gain')
        same_word(result['inheritedGain'], old['inheritedGain'], 'unchanged-inherited-gain')
        provenance = predecessor_chain(PREVIOUS, old, input_raw)
        rows = old['cases']
        need(type(rows) is list and len(rows) == 3240, 'original-case-count')
        words = same_tree(result['originalCases'], rows, 'originalCases')
        words += same_tree(result['fullFieldSubsets'], old['subsets'], 'fullFieldSubsets')
        with localcontext() as context:
            context.prec = 60
            byid, links, table, counts, comparisons = independent_matching(rows)
            need(len(links) <= 1620, 'pair-bound')
            same_tree(result['matching'], table, 'matching')
            same_tree(result['countsByReason'], counts, 'countsByReason')
            same_tree(result['eligibilityComparisons'], comparisons, 'eligibilityComparisons')
            expected_selection = {}
            for region in REGIONS:
                eligible = sum(row['included'] and belongs(row['original']['Z'], region) for row in rows)
                number = sum(belongs(byid[right]['original']['Z'], region) for left, right in links)
                expected_selection[region] = {'eligibleCells': eligible, 'pairs': number, 'pairedCells': 2 * number,
                    'unmatchedCells': eligible - 2 * number, 'coverage': 2 * number / eligible if eligible else None}
            same_tree(selection, {'matching': table, 'countsByReason': counts, 'groups': expected_selection,
                                 'eligibilityComparisons': comparisons}, 'selection-trace')
            primary = expected_selection['primary']
            levels = {struct.pack('>d', byid[right]['original']['Z']) for left, right in links
                      if byid[right]['original']['Z'] >= 12}
            need(primary['pairs'] >= 20 and len(levels) >= 3
                 and 10 * primary['pairedCells'] >= 9 * primary['eligibleCells'], 'primary-pair-support-admission')
            saved_pairs = result['pairs']
            need(type(saved_pairs) is list and len(saved_pairs) == len(links), 'saved-pair-count')
            pairs = []
            for pair_id, ((left_index, right_index), stored) in enumerate(zip(links, saved_pairs)):
                guard()
                left, right = byid[left_index], byid[right_index]
                lo, ro = left['original'], right['original']
                need(type(stored) is dict and set(stored) == {'pairId', 'leftIndex', 'rightIndex',
                     'Xleft', 'Xright', 'Z', 'absXSum'} | set(COMPONENTS) | set(ENERGIES), 'pair-fields')
                for field, expected in [('pairId', pair_id), ('leftIndex', left_index), ('rightIndex', right_index)]:
                    need(type(stored[field]) is int and stored[field] == expected, 'ordered-pair-' + field)
                for field, expected in [('Xleft', lo['X']), ('Xright', ro['X']), ('Z', ro['Z'])]:
                    same_word(stored[field], expected, 'pair-original-' + field)
                need(struct.pack('>d', lo['Z']) == struct.pack('>d', ro['Z']) and lo['X'] < 0 < ro['X'], 'pair-sign-and-exact-level')
                mismatch = abs(D(lo['X']) + D(ro['X']))
                close(stored['absXSum'], mismatch, 'pair-mismatch')
                same_word(stored['absXSum'], abs(lo['X'] + ro['X']), 'saved-pair-mismatch')
                components = independent_components(left, right)
                for field, expected in components.items():
                    close(stored[field], expected, 'pair-' + field)
                need(abs(stored['directSSE'] - stored['evenSSE'] - stored['oddSSE']) <= 2e-12, 'saved-pair-energy-identity')
                pairs.append({'pairId': pair_id, 'leftIndex': left_index, 'rightIndex': right_index,
                              'Z': ro['Z'], 'absXSum': mismatch, **components})
            need(type(result['groups']) is dict and set(result['groups']) == set(REGIONS), 'region-fields')
            for region in REGIONS:
                stored = result['groups'][region]
                need(type(stored) is dict and set(stored) == set(expected_selection[region]) | {'summary'}, 'region-summary-fields')
                same_tree({key: stored[key] for key in expected_selection[region]}, expected_selection[region], region + '-selection')
                chosen = [pair for pair in pairs if belongs(pair['Z'], region)]
                expected = independent_summary(chosen, byid)
                check_summary(stored['summary'], expected, region)
                if chosen:
                    saved_chosen = [pair for pair in saved_pairs if belongs(pair['Z'], region)]
                    same_word(stored['summary']['maxAbsXSum'], max(pair['absXSum'] for pair in saved_chosen), region + '-saved-max-mismatch')
        need(verify_manifest(manifest) == verified, 'post-audit-source-pins')
        retained = {BASE / 'source-manifest.json': manifest_raw, BASE / 'source-publication.json': publication_raw,
                    RESULTS / 'comparison.json': body, RESULTS / 'execution.json': execution_raw,
                    RESULTS / 'controls.json': controls_raw, RESULTS / 'selection.json': selection_raw,
                    RESULTS / 'evaluate-supervisor.json': supervisor_raw, ROOT / INPUT: input_raw}
        retained.update({ROOT / name: raw for name, raw in provenance.items()})
        for path, raw in retained.items():
            need(read_local(path) == raw, 'unchanged-source-input-selection-result-receipts')
        guard()
        report = {'schema': 'm31-lateral-symmetry-independent-audit-v1', 'passed': True, 'complete': True,
                  'sourceManifestSha256': sha(manifest_raw), 'verifiedSourcePins': verified,
                  'publicationPin': pin(BASE / 'source-publication.json', publication_raw),
                  'inputPin': pin(ROOT / INPUT, input_raw), 'resultPin': pin(RESULTS / 'comparison.json', body),
                  'selectionPin': pin(RESULTS / 'selection.json', selection_raw),
                  'evaluatorSupervisorPin': pin(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
                  'originalCasesChecked': 3240, 'recursivelyPreservedBinary64Words': words,
                  'pairsChecked': len(links), 'eligibilityComparisonsChecked': comparisons,
                  'matchingReasonsChecked': counts, 'regionCoverageChecked': expected_selection,
                  'regionSummariesChecked': 4, 'sideMetricGroupsChecked': 24,
                  'primaryEndpointChecked': 'Pooled same-direction residual energy share over admitted primary pairs; null at exact zero residual energy.',
                  'arithmetic': 'Independent 60-digit Decimal geometry graph, residual-first components and aggregate energies/metrics; no producer imports or field evaluation.',
                  'tolerance': '2e-12 absolute numerical consistency only; exact recursive original binary64 preservation. Geometry-boundary disagreement fails without widening.',
                  'inheritedGainPreserved': True, 'newFits': 0, 'newFieldEvaluations': 0,
                  'sourcesPreserved': True, 'inputPreserved': True, 'resultsPreserved': True,
                  'independentPhysicalValidation': False, 'causalComponentIdentification': False,
                  'scope': 'Exposed same-experiment paired-support diagnostic; approximate mirrored locations, no field-parity or causal claim.',
                  'elapsedSeconds': time.monotonic() - START}
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'originalCasesChecked': 3240, 'pairsChecked': len(links),
                          'regionSummariesChecked': 4, 'sideMetricGroupsChecked': 24}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()
