"""Single-use, saved-bytes-only capacity audit. Never imports scientific source."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

PACKAGE = 'research/m31-prepared-capacity-2026-10-17'
PREVIOUS = 'research/m31-prepared-reference-2026-10-17'
FRESH = 'research/m31-native-fresh-transfer-2026-10-17'
TREE = 'research/m31-tree-first-reference-2026-10-17'
FILTER = 'research/m31-filter-cost-2026-10-17'
COMMIT = '7528347a34c6638429430268ad6cc9e4bcb6e5f0'
SOURCE_SHA = 'd404173845985fd2eef76c9526adefb981c1486a49f7b8aacd1a6e565cf9ba5f'
CASES = ('fresh-a-t5', 'dense-180-filter-cost', 'sparse-180-filter-cost')
NS = (64, 180, 180)
SUFFIX = (7408, 34707, 3340)
POSITIVES = (228, 3056, 0)
RULES = ('neighbor', 'upstream', 'down-cut', 'near-outside', 'radial')
PHASES = ('inputAndBaselineLoad', 'profiledRegenerate', 'profileSerializationAndWrite',
          'referenceWireSerializationAndWrite', 'exactSavedComparisonAndAccounting')
CUTOFF = datetime(2026, 10, 17, 3, tzinfo=timezone.utc)


class AuditError(Exception):
    pass


def need(value, code):
    if not value:
        raise AuditError(code)


def unique_object(pairs):
    answer = {}
    for key, value in pairs:
        need(key not in answer, 'duplicate-json-key')
        answer[key] = value
    return answer


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(AuditError('nonfinite-json')))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(value):
    need(isinstance(value, str) and value and '\n' not in value and '\r' not in value,
         'safe-path-text')
    path = Path(value)
    need(not path.is_absolute() and '..' not in path.parts, 'relative-safe-path')
    return path


def verify_pin(root, pin):
    need(set(pin) == {'path', 'bytes', 'sha256'} and type(pin['bytes']) is int
         and pin['bytes'] >= 0 and re.fullmatch('[0-9a-f]{64}', pin['sha256']), 'pin-shape')
    raw = (root / safe_path(pin['path'])).read_bytes()
    need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'local-byte-pin:' + pin['path'])
    return raw


def verify_commit(root, pins):
    count = 0
    for start in range(0, len(pins), 32):
        batch = pins[start:start + 32]
        query = ''.join(COMMIT + ':' + p['path'] + '\n' for p in batch).encode()
        proc = subprocess.run(['git', 'cat-file', '--batch'], cwd=root, input=query,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15, check=False)
        need(proc.returncode == 0, 'git-read-exit')
        cursor = 0
        for pin in batch:
            newline = proc.stdout.index(b'\n', cursor)
            fields = proc.stdout[cursor:newline].split()
            need(len(fields) == 3 and fields[1] == b'blob', 'git-read-blob')
            size = int(fields[2]); begin = newline + 1
            raw = proc.stdout[begin:begin + size]
            need(size == pin['bytes'] and digest(raw) == pin['sha256'], 'committed-byte-pin:' + pin['path'])
            need(proc.stdout[begin + size:begin + size + 1] == b'\n', 'git-read-framing')
            cursor = begin + size + 1
            count += 1
        need(cursor == len(proc.stdout), 'git-read-no-extra-bytes')
    return count


def finite_nonnegative(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def fraction(word):
    need(set(word) == {'n', 'd'} and isinstance(word['n'], str) and isinstance(word['d'], str),
         'rational-fields')
    need(re.fullmatch(r'-?(0|[1-9][0-9]*)', word['n']) and re.fullmatch(r'[1-9][0-9]*', word['d']),
         'rational-integer-text')
    value = Fraction(int(word['n']), int(word['d']))
    need(str(value.numerator) == word['n'] and str(value.denominator) == word['d'], 'canonical-rational')
    return value


def interval(bounds):
    need(set(bounds) == {'l', 'u'}, 'interval-fields')
    lower, upper = fraction(bounds['l']), fraction(bounds['u'])
    need(lower <= upper, 'interval-ordered')
    return lower, upper


def check_rows(record, n):
    ids = [row['id'] for row in record['input']['drones']]
    need(len(ids) == n and len(set(ids)) == n and all(type(i) is int and 0 <= i <= 65535 for i in ids),
         'stable-id-list')
    for row in record['input']['drones']:
        need(set(row) == {'id', 'state'} and len(row['state']) == 17
             and all(isinstance(x, str) and re.fullmatch('[0-9a-f]{16}', x) for x in row['state']),
             'raw-17-word-shape')
    need([row['id'] for row in record['prepared']] == ids
         and [row['id'] for row in record['loads']] == ids, 'prepared-and-load-id-order')
    need(sorted(record['order']) == sorted(ids) and len(record['order']) == n, 'solve-order-permutation')
    need(record['status'] == record['referenceClass'] == 'admitted'
         and record['branch'] == 'loads' and record['witness'] is None
         and record['globalInvalid'] is False and record['globalGuard']['passed'] is True
         and set(record['globalGuard']['checks']) == {'centerComponent', 'centerNorm', 'rotorComponent', 'down', 'radial'}
         and all(value is True for value in record['globalGuard']['checks'].values()), 'admitted-wire-status')
    need(all(row['rejection'] is None and row['value'] is not None for row in record['prepared']),
         'all-prepared-admissible')
    roots, loads, nonpoint = 0, 0, 0
    for row in record['loads']:
        need(set(row) == {'id', 'roots', 'loads'} and len(row['roots']) == 4, 'root-row-shape')
        values = row['loads']
        need(set(values) == {'rotor', 'collective', 'force', 'moment'}
             and len(values['rotor']) == 4 and len(values['force']) == len(values['moment']) == 3,
             'signed-load-row-shape')
        for bounds in row['roots']:
            lower, upper = interval(bounds); roots += 1; nonpoint += lower != upper
        for bounds in values['rotor'] + [values['collective']] + values['force'] + values['moment']:
            interval(bounds); loads += 1
    return ids, {'rootBoxes': roots, 'signedLoadBoxes': loads, 'nonpointRootBoxes': nonpoint}


def coverage_review(record, ids):
    """Reconstruct saved combinatorial coverage; never evaluate a zero predicate."""
    n = len(ids); planned = 4 * n * (n - 1)
    cov, tree = record['coverage'], record['tree']
    need(record['planned'] == planned and cov['mode'] == 'hierarchy' and cov['complete'] is True
         and cov['logicalPairs'] == cov['requiredCoveredPairs'] == cov['coveredPairs'] == planned,
         'complete-coverage-declaration')
    permutation = tree['permutation']; nodes = tree['nodes']
    need(cov['permutation'] == permutation and len(permutation) == n
         and set(permutation) == set(ids), 'coverage-permutation')
    original_index = {identifier: i for i, identifier in enumerate(ids)}
    positions = {identifier: i for i, identifier in enumerate(permutation)}
    parents = {}
    for k, node in enumerate(nodes):
        need(node['id'] == k and type(node['start']) is int and type(node['end']) is int
             and 0 <= node['start'] < node['end'] <= n, 'tree-node-range')
        if node['left'] is None:
            need(node['right'] is None and node['end'] - node['start'] <= 8, 'tree-leaf-capacity')
        else:
            left, right = node['left'], node['right']
            need(type(left) is int and type(right) is int and k < left < right < len(nodes), 'tree-child-order')
            need(left not in parents and right not in parents, 'tree-unique-parent')
            parents[left] = parents[right] = k
            a, b = nodes[left], nodes[right]
            need(a['start'] == node['start'] and a['end'] == b['start'] and b['end'] == node['end']
                 and a['end'] - a['start'] == (node['end'] - node['start']) // 2, 'tree-child-partition')
    need(nodes[0]['start'] == 0 and nodes[0]['end'] == n and set(parents) == set(range(1, len(nodes))),
         'tree-complete-reachability')
    need([(q['i'], q['r']) for q in cov['queries']] == [(i, r) for i in range(n) for r in range(4)],
         'coverage-query-order')
    scalar_keys = set(); work = Counter(); rule_counts = Counter()
    for query in cov['queries']:
        i, r = query['i'], query['r']; self_position = positions[ids[i]]
        need(query['id'] == ids[i] and query['selfPosition'] == self_position, 'coverage-query-id')
        cursor, count, seen = 0, 0, set()
        for terminal in query['terminals']:
            start, end, node_id = terminal['start'], terminal['end'], terminal['node']
            need(type(start) is int and type(end) is int and start == cursor and start < end <= n,
                 'terminal-disjoint-range-partition')
            need(type(node_id) is int and 0 <= node_id < len(nodes), 'terminal-node-index')
            node = nodes[node_id]
            need(node['start'] == start and node['end'] == end, 'terminal-node-boundary')
            cursor = end
            expected_count = end - start - int(start <= self_position < end)
            need(type(terminal['count']) is int and terminal['count'] == expected_count, 'terminal-self-exclusion')
            count += expected_count
            ancestor = node_id
            while True:
                seen.add(ancestor)
                if ancestor == 0:
                    break
                ancestor = parents[ancestor]
            if terminal['kind'] == 'zero':
                rule = terminal['proofRule']
                need(rule in RULES and 'sourceIndices' not in terminal, 'saved-zero-rule-label')
                work['zeroNodes'] += 1; work['zeroPairs'] += expected_count
                work['nodeRuleTests'] += RULES.index(rule) + 1
                rule_counts[rule] += 1
            else:
                need(terminal['kind'] == 'leaf' and node['left'] is None and node['right'] is None,
                     'scalar-terminal-is-leaf')
                members = sorted(original_index[permutation[p]] for p in range(start, end) if p != self_position)
                need(terminal['sourceIndices'] == members, 'scalar-source-index-map')
                work['leafVisits'] += 1
                for j in members:
                    key = (i, r, j)
                    need(key not in scalar_keys, 'unique-scalar-coverage')
                    scalar_keys.add(key)
        need(cursor == n and count == n - 1, 'complete-nonself-query-partition')
        work['nodeVisits'] += len(seen)
        work['nodeRuleTests'] += len(RULES) * (len(seen) - sum(t['kind'] == 'zero' for t in query['terminals']))
    pairs = record['pairs']; actual_keys = []
    positives = {}
    for pair in pairs:
        i, r, j = pair['ii'], pair['r'], pair['jj']
        need(type(i) is int and type(j) is int and type(r) is int and 0 <= i < n and 0 <= j < n
             and i != j and 0 <= r < 4 and pair['i'] == ids[i] and pair['j'] == ids[j], 'pair-index-id-map')
        actual_keys.append((i, r, j))
        need(pair['oracle']['status'] in ('positive', 'zero'), 'admitted-pair-status')
        if pair['oracle']['status'] == 'positive':
            key = (ids[i], r, ids[j]); need(key not in positives, 'unique-positive-support')
            interval(pair['coefficient']); positives[key] = pair['coefficient']
        else:
            need('coefficient' not in pair, 'zero-without-positive-coefficient')
    need(actual_keys == sorted(scalar_keys), 'canonical-pairs-equal-saved-leaf-members')
    work.update({'preparationCalls': n, 'globalProofs': 1, 'treeNodes': len(nodes),
                 'scalarPairs': len(pairs), 'scalarZeroPairs': len(pairs) - len(positives),
                 'positiveTerms': len(positives), 'rejectedPairs': 0, 'unresolvedPairs': 0})
    need(work['zeroPairs'] + work['scalarPairs'] == planned and set(cov['work']) == set(work)
         and all(type(value) is int and value == work[key] for key, value in cov['work'].items()),
         'reconstructed-coverage-work')
    return positives, {'logicalPairs': planned, 'scalarPairs': len(pairs), 'positiveTerms': len(positives),
                       'provedZeroPairsDeclared': work['zeroPairs'], 'work': dict(work),
                       'savedZeroRuleCounts': dict(rule_counts), 'zeroPredicatesReevaluated': False}


def producer_map(method, ids):
    result = {}
    need([(q['i'], q['r']) for q in method['assembly']['queries']]
         == [(i, r) for i in range(len(ids)) for r in range(4)], 'producer-query-completeness')
    for query in method['assembly']['queries']:
        i, r = query['i'], query['r']
        for terminal in query['terminals']:
            for entry in terminal.get('entries', []):
                j = entry['j']
                need(type(j) is int and 0 <= j < len(ids) and j != i
                     and entry['result']['status'] == 'positive', 'producer-positive-index-status')
                key = (ids[i], r, ids[j]); need(key not in result, 'producer-unique-positive-support')
                bounds = entry['result']['coefficient']
                need(set(bounds) == {'l', 'u'} and all(isinstance(bounds[k], str)
                     and re.fullmatch(r'-?(0|[1-9][0-9]*)', bounds[k]) for k in ('l', 'u')),
                     'producer96-bound-text')
                need(int(bounds['l']) <= int(bounds['u']), 'producer96-ordered')
                result[key] = bounds
    return result


def compare_180(record, saved, reference, ids, positive):
    need(record['id'] == saved['id'] == reference['sceneId']
         and saved['rawInputSha256'] == reference['rawInputSha256'], '180-scene-and-input-digest-binding')
    need(record['input'] == saved['input'], '180-exact-ordered-raw-words')
    methods = {x['name']: x for x in saved['methods']}
    need(len(methods) == len(saved['methods']) == 2 and set(methods) == {'hierarchy', 'filtered'},
         '180-method-identities')
    maps = []
    for name in ('hierarchy', 'filtered'):
        method = methods[name]
        need(record['prepared'] == method['prepared'], '180-complete-ordered-prepared-equality')
        need(method['result'] == {'branch': 'loads', 'status': 'certified', 'toleranceAchieved': True, 'witness': None},
             '180-saved-admissibility')
        need(set(method['solve']) == {'candidate', 'iterations', 'bisections'}, 'saved-solve-order-unavailable-schema')
        maps.append(producer_map(method, ids))
    need(record['loads'] == reference['independentReference'], '180-complete-ordered-independent-root-load-equality')
    need(reference['referenceCoefficientBits'] == reference['referenceSourceBits'] == 192
         and reference['referenceRootBisections'] == 128 and reference['plannedPairsPerMethod'] == 128880,
         '180-reference-recipe')
    need(maps[0] == maps[1] and set(positive) == set(maps[0]), '180-exact-producer96-map-and-positive-support')
    for key, bounds in positive.items():
        lower, upper = interval(bounds); old = maps[0][key]
        need(Fraction(int(old['l']), 2 ** 96) <= lower <= upper <= Fraction(int(old['u']), 2 ** 96),
             '180-exact192-within96-containment')
    return {'orderedRawAndPreparedExactlyEqual': True, 'orderedIndependent192RootsAndSignedLoadsExactlyEqual': True,
            'producer96MapsExactlyEqual': True, 'positiveSupportExactlyEqualBothMethods': True,
            'new192WithinBothProducer96Bounds': True, 'independent192PairEqualityAvailable': False,
            'savedSolveOrderComparisonAvailable': False}


def profile_review(profile, n, expected_calls, observed_wall):
    need(profile['schema'] == 'm31-complete-cprofile-v1' and profile['completeCallReturned'] is True
         and profile['callerTupleFields'] == ['totalCalls', 'primitiveCalls', 'ownSeconds', 'cumulativeSeconds'],
         'profile-schema-and-caller-tuple-order')
    need('overhead included' in profile['scope'] and 'overlap' in profile['cumulativeAccounting'], 'profile-scope')
    rows = profile['functions']
    need([r['functionId'] for r in rows] == list(range(len(rows)))
         and all(type(r['functionId']) is int for r in rows), 'profile-function-ids')
    edges = 0
    for row in rows:
        safe_path(row['file'])
        need(not any(mark in row['file'] or mark in row['function'] for mark in ('/Users/', '/home/', '/private/', '\\Users\\')),
             'profile-no-private-absolute-path')
        need(isinstance(row['function'], str) and row['function'] and type(row['line']) is int and row['line'] >= 0,
             'profile-function-location')
        need(type(row['primitiveCalls']) is int and type(row['totalCalls']) is int
             and 0 <= row['primitiveCalls'] <= row['totalCalls'], 'profile-function-counts')
        need(finite_nonnegative(row['ownSeconds']) and finite_nonnegative(row['cumulativeSeconds'])
             and row['ownSeconds'] <= row['cumulativeSeconds'] + 1e-9, 'profile-function-times')
        seen = set()
        for edge in row['callers']:
            caller = edge['functionId']; values = edge['pstatsValues']
            need(type(caller) is int and 0 <= caller < len(rows) and caller not in seen, 'profile-caller-edge-id')
            seen.add(caller); edges += 1
            need(isinstance(values, list) and len(values) == 4 and type(values[0]) is int
                 and type(values[1]) is int and 0 <= values[1] <= values[0]
                 and finite_nonnegative(values[2]) and finite_nonnegative(values[3])
                 and values[2] <= values[3] + 1e-9, 'profile-caller-values')
    need(profile['primitiveCalls'] == sum(r['primitiveCalls'] for r in rows)
         and profile['totalCalls'] == sum(r['totalCalls'] for r in rows), 'profile-total-count-reconciliation')
    total = math.fsum(row['ownSeconds'] for row in rows)
    need(finite_nonnegative(profile['totalOwnSeconds'])
         and math.isclose(total, profile['totalOwnSeconds'], rel_tol=1e-9, abs_tol=1e-9)
         and total <= observed_wall + 1e-6, 'profile-own-time-reconciliation')
    expected = ((PREVIOUS + '/source/prepared-reference.py', 'regenerate_scene', 1),
                (TREE + '/source/tree-reference.py', 'regenerate_scene', 1),
                (PREVIOUS + '/source/prepared-reference.py', '_oracle_suffix', expected_calls),
                (PREVIOUS + '/source/prepared-reference.py', 'oracle_case', expected_calls),
                (PREVIOUS + '/source/prepared-reference.py', 'prepare_one', n),
                (FRESH + '/source/pair-reference.py', 'prepare_one', n))
    for filename, function, count in expected:
        found = [r for r in rows if r['file'] == filename and r['function'] == function]
        need(len(found) == 1 and found[0]['primitiveCalls'] == found[0]['totalCalls'] == count,
             'profile-scientific-call-accounting')
    need(not any(r['function'] == 'run_binding_controls' for r in rows), 'profile-no-control-repeat')
    return {'functions': len(rows), 'callerEdges': edges, 'primitiveCalls': profile['primitiveCalls'],
            'totalCalls': profile['totalCalls'], 'ownSecondsSum': total,
            'privatePathsAbsent': True, 'recordedScientificCallCountsMatch': True,
            'cumulativeTimesSummed': False, 'unprofiledSpeedInferred': False}


def main(root, audit_sha):
    review = root / PACKAGE / 'review'
    marker, output = review / 'AUDIT-STARTED.json', review / 'saved-audit-result.json'
    need(not marker.exists() and not output.exists(), 'single-use-audit')
    need((CUTOFF - datetime.now(timezone.utc)).total_seconds() >= 120, 'full120-before-cutoff')
    started = time.monotonic()
    report = {'schema': 'm31-prepared-capacity-saved-audit-v1', 'status': 'running',
              'sourceCommit': COMMIT, 'sourceManifestSha256': SOURCE_SHA,
              'auditManifestSha256': audit_sha, 'startedUtc': datetime.now(timezone.utc).isoformat(),
              'processingLimitSeconds': 120, 'scientificModulesImported': False, 'scientificExecutions': 0,
              'zeroPredicatesReevaluated': False, 'browserCalls': 0, 'networkCalls': 0,
              'physicalValidation': False, 'performanceClaim': False, 'cases': [], 'errors': []}
    with marker.open('x') as stream:
        json.dump({'startedUtc': report['startedUtc'], 'auditManifestSha256': audit_sha, 'singleUse': True}, stream)
        stream.write('\n')
    def alarm(signum, frame):
        raise AuditError('saved-audit-allocation-deadline')
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, 115, 0.25)
    pins = []
    try:
        manifest_raw = (review / 'audit-source-manifest.json').read_bytes()
        need(digest(manifest_raw) == audit_sha, 'parent-reviewed-audit-manifest')
        manifest = decode(manifest_raw)
        need(manifest['scientificSourceCommit'] == COMMIT and manifest['processingLimitSeconds'] == 120
             and manifest['executionAuthorized'] is False, 'audit-source-contract')
        need([p['path'] for p in manifest['auditSourceFiles']]
             == [PACKAGE + '/review/saved_audit.py', PACKAGE + '/review/AUDIT-CONTRACT.md'], 'audit-source-members')
        pins = manifest['auditSourceFiles'] + manifest['inputFiles']
        pin_map = {p['path']: p for p in pins}
        need(len(pin_map) == len(pins), 'unique-all-audit-pins')
        for pin in pins:
            verify_pin(root, pin)
        source_pin = manifest['scientificSourceManifest']
        need(source_pin['path'] == PACKAGE + '/source-manifest.json' and source_pin['sha256'] == SOURCE_SHA
             and pin_map[source_pin['path']] == source_pin, 'scientific-manifest-pin')
        source = decode(verify_pin(root, source_pin))
        need(len(source['files']) == 767 and len({p['path'] for p in source['files']}) == 767
             and all(pin_map.get(p['path']) == p for p in source['files']), 'all767-source-pins-retained')
        runtime = source['runtime']['python']; executable = Path(sys.executable).resolve().read_bytes()
        need(sys.platform == 'darwin' and sys.flags.isolated == 1 and sys.dont_write_bytecode
             and sys.version == runtime['version'] and len(executable) == runtime['bytes']
             and digest(executable) == runtime['sha256'], 'pinned-isolated-macos-python')
        del executable
        count = verify_commit(root, source['files'] + [source_pin])
        report['sourceVerification'] = {'localSourcePins': 767, 'committedSourcePins': count - 1,
                                        'committedSourceManifest': True, 'allReviewedFilePins': len(pins)}
        def read(relative):
            need(relative in pin_map, 'read-file-must-be-pinned:' + relative)
            return decode(verify_pin(root, pin_map[relative]))
        receipt = read(PACKAGE + '/source-publication.json')
        need(receipt['commit'] == COMMIT and receipt['manifestSha256'] == SOURCE_SHA
             and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True
             and receipt['verifiedFilePins'] == 767, 'saved-publication-receipt')
        start_record = read(PACKAGE + '/STARTED.json')
        index = read(PACKAGE + '/results/index.json')
        report['resultIndexSha256'] = pin_map[PACKAGE + '/results/index.json']['sha256']
        need(index['sourceCommit'] == start_record['sourceCommit'] == COMMIT
             and index['sourceManifestSha256'] == start_record['sourceManifestSha256'] == SOURCE_SHA
             and index['sourcePinsBefore'] == index['sourcePinsAfter'] == start_record['sourcePinsVerified'] == 767,
             'scientific-index-source-binding')
        need(index['status'] == 'completed' and all(index[k] is True for k in
             ('complete', 'qualified', 'accuracyQualified', 'outputsPreserved')), 'complete-accurate-scientific-index')
        need([c['id'] for c in index['cases']] == list(CASES) == index['expectedCaseOrder']
             and index['expectedCases'] == index['regenerateSceneCalls'] == 3
             and index['expectedScalarCalls'] == index['scalarOracleCalls'] == 45455
             and index['expectedLogicalPairs'] == 273888, 'fixed-three-scene-allocation')
        need(index['controlsRerun'] is False and index['newFullOracleRuns'] == index['newInputs'] == index['newBrowserCalls'] == 0
             and index['physicalValidation'] is False and index['performanceClaim'] is False, 'scope-limits')
        old_index = read(PREVIOUS + '/results/index.json'); old_audit = read(PREVIOUS + '/review/saved-audit-result.json')
        need(old_index['complete'] is True and old_index['qualified'] is True and len(old_index['cases']) == 24
             and old_audit['status'] == 'passed' and old_audit['errors'] == []
             and old_audit['resultIndexSha256'] == pin_map[PREVIOUS + '/results/index.json']['sha256']
             and index['priorIndex'] == pin_map[PREVIOUS + '/results/index.json']
             and index['priorSavedAudit'] == pin_map[PREVIOUS + '/review/saved-audit-result.json'], 'retained-prior24-audit')
        baseline_cases = {c['id']: c for c in old_index['cases']}
        rss_samples = []; phase_sum = 0; all_hurdles = []
        for ordinal, case in enumerate(index['cases']):
            sid, n, calls, expected_positive = CASES[ordinal], NS[ordinal], SUFFIX[ordinal], POSITIVES[ordinal]
            need(case['ordinal'] == ordinal and case['n'] == n and case['complete'] is True
                 and case['accuracyQualified'] is True, 'case-identity-and-completion')
            for key, suffix in (('result', '.json'), ('profile', '.profile.json')):
                relative = PACKAGE + '/results/' + sid + suffix
                need(case[key] == pin_map[relative], 'case-output-pin')
            record = read(case['result']['path']); profile = read(case['profile']['path'])
            need(record['id'] == sid, 'wire-scene-identity')
            ids, endpoint_counts = check_rows(record, n)
            positive, coverage = coverage_review(record, ids)
            need(coverage['scalarPairs'] == calls and coverage['positiveTerms'] == expected_positive,
                 'fixed-case-suffix-and-positive-counts')
            need(case['coverageWork'] == record['coverage']['work']
                 and all(type(value) is int for value in case['reuseCounters'].values())
                 and case['reuseCounters'] == {'prepareOneCalls': n, 'preparationValidCalls': n,
                      'oracleCalls': calls, 'operandLookups': 2 * calls, 'pairPreparations': 0}, 'case-reuse-accounting')
            if ordinal == 0:
                baseline = baseline_cases[sid]['result']
                need(case['encoding'] == 'bits' and case['baseline'] == baseline == pin_map[baseline['path']], 'fresh-baseline-pin')
                need(record == read(baseline['path']) and case['result']['sha256'] == baseline['sha256'], 'fresh-complete-wire-and-bytes')
                need(record['input']['drones'] == read(FRESH + '/results/inputs/fresh-a-t5.json')['drones'], 'fresh-original-raw-input')
                comparison = {'completeSavedWireAndBytesExactlyEqual': True}
            else:
                scene_path = FILTER + '/results/scenes/' + sid + '.json'
                ref_path = FILTER + '/results/reference-scenes/' + sid + '.json'
                need(case['encoding'] == 'decimal' and case['baselineScene'] == pin_map[scene_path]
                     and case['baselineReference'] == pin_map[ref_path], '180-baseline-pins')
                comparison = compare_180(record, read(scene_path), read(ref_path), ids, positive)
                need(case['comparison']['independent192PairEqualityAvailable'] is False
                     and case['comparison']['savedSolveOrderComparisonAvailable'] is False,
                     '180-unavailable-comparisons-labeled')
            phases = case['phaseWallSeconds']
            need(set(phases) == set(PHASES) and all(finite_nonnegative(v) for v in phases.values()), 'nonnegative-separated-phase-walls')
            phase_sum += sum(phases.values())
            profile_result = profile_review(profile, n, calls, phases['profiledRegenerate'])
            hurdle = phases['profiledRegenerate'] <= 60
            need(case['profiledCallHurdlePassed'] is hurdle, 'recorded-call-hurdle-recomputed')
            all_hurdles.append(hurdle)
            rss_samples.extend(case[k] for k in ('rssBeforeCaseLifetimePeakBytes', 'rssAfterRegenerateLifetimePeakBytes', 'rssAfterCaseLifetimePeakBytes'))
            report['cases'].append({'id': sid, 'n': n, **endpoint_counts, 'comparison': comparison,
                                    'coverage': coverage, 'profile': profile_result,
                                    'recordedPhaseWallSeconds': phases, 'profiledCallHurdlePassed': hurdle})
        need(sum(c['coverage']['logicalPairs'] for c in report['cases']) == 273888
             and sum(c['coverage']['scalarPairs'] for c in report['cases']) == 45455, 'aggregate-work-recomputed')
        need(all(finite_nonnegative(index[k]) for k in ('wallSeconds', 'moduleAndConstantSetupWallSeconds',
             'closureVerificationWallSeconds', 'closureWallSecondsBeforeIndexWrite')),
             'allocation-wall-values')
        need(index['closureVerificationWallSeconds'] <= index['closureWallSecondsBeforeIndexWrite'] < 60
             and phase_sum + index['moduleAndConstantSetupWallSeconds'] + index['closureWallSecondsBeforeIndexWrite']
             <= index['wallSeconds'] + 1e-6 and index['wallSeconds'] < 600, 'wall-phase-budget-reconciliation')
        need('before final index serialization' in index['wallMeasurementScope']
             and 'not completed-process wall time' in index['wallMeasurementScope']
             and 'macOS' in index['rssScope'] and 'process-lifetime peak' in index['rssScope'], 'wall-and-memory-observation-scopes')
        rss_samples.append(index['lifetimePeakRssBytes'])
        need(all(type(v) is int and v > 0 for v in rss_samples)
             and rss_samples == sorted(rss_samples), 'lifetime-rss-monotonic-byte-samples')
        need(index['capacityHurdle']['eachProfiledRegenerateSecondsAtMost'] == 60
             and index['capacityHurdle']['lifetimePeakRssBytesAtMost'] == 2 ** 30, 'fixed-capacity-hurdle')
        hurdle = all(all_hurdles) and index['lifetimePeakRssBytes'] <= 2 ** 30
        need(index['capacityHurdlePassed'] is hurdle
             and index['outcome'] == ('accuracy-qualified-capacity-hurdle-passed' if hurdle else
                                     'accuracy-qualified-capacity-hurdle-failed'), 'aggregate-capacity-hurdle-recomputed')
        publication = datetime.fromisoformat(receipt['verifiedUtc'])
        launch, finished = datetime.fromisoformat(index['startedUtc']), datetime.fromisoformat(index['finishedUtc'])
        marker_utc = datetime.fromisoformat(start_record['utc'])
        need(all(x.tzinfo is not None for x in (publication, launch, finished, marker_utc))
             and publication <= launch <= marker_utc <= finished < CUTOFF
             and (CUTOFF - launch).total_seconds() >= 600
             and (CUTOFF - publication).total_seconds() >= 600, 'published-before-full-reservation-launch')
        journal = index['eventJournal']; need(journal == pin_map[PACKAGE + '/results/events.jsonl'], 'event-journal-pin')
        events = [decode(line) for line in verify_pin(root, journal).splitlines()]
        need(len(events) == 6, 'exact-six-events')
        before = 0
        for ordinal, case in enumerate(index['cases']):
            begin, end = events[2 * ordinal:2 * ordinal + 2]
            need(begin == {'event': 'start', 'id': case['id'], 'ordinal': ordinal, 'callsBefore': before}, 'exact-start-event')
            before += SUFFIX[ordinal]
            need(end == {'event': 'complete', 'id': case['id'], 'ordinal': ordinal, 'result': case['result'],
                         'profile': case['profile'], 'callsAfter': before}, 'exact-complete-event')
        expected_paths = {PACKAGE + '/results/index.json', PACKAGE + '/results/events.jsonl'}
        expected_paths.update(case[key]['path'] for case in index['cases'] for key in ('result', 'profile'))
        actual_paths = {p.relative_to(root).as_posix() for p in (root / PACKAGE / 'results').iterdir()}
        need(expected_paths == actual_paths, 'exact-eight-result-files')
        evidence_paths = expected_paths | {PACKAGE + '/STARTED.json'}
        need(all(pin_map[p]['bytes'] <= 32 * 1024 ** 2 for p in evidence_paths)
             and sum(pin_map[p]['bytes'] for p in evidence_paths) <= 256 * 1024 ** 2
             and index['resultBytesBeforeIndex'] == sum(pin_map[p]['bytes'] for p in evidence_paths
                                                       if p != PACKAGE + '/results/index.json'), 'output-byte-budget-recomputed')
        report.update(status='passed', accuracySavedEvidenceVerified=True,
                      observedCapacityHurdleRecomputed=hurdle, eventsVerified=6,
                      scientificOutputFilesVerified=len(evidence_paths),
                      newOutputBytes=sum(pin_map[p]['bytes'] for p in evidence_paths),
                      recordedLifetimePeakRssBytes=index['lifetimePeakRssBytes'],
                      recordedPreIndexWallSeconds=index['wallSeconds'],
                      independent192PairEqualityFor180Available=False)
    except BaseException as error:
        report['status'] = 'failed'
        report['errors'].append(str(error) if isinstance(error, AuditError) else type(error).__name__)
    finally:
        signal.setitimer(signal.ITIMER_REAL, max(0.001, 120 - (time.monotonic() - started)), 0.25)
        try:
            for pin in pins:
                verify_pin(root, pin)
            report['allReviewedBytesUnchangedAtClosure'] = bool(pins)
        except BaseException as error:
            report['status'] = 'failed'; report['allReviewedBytesUnchangedAtClosure'] = False
            report['errors'].append('closure-preservation-failed:' + type(error).__name__)
        report['wallSecondsBeforeReportWrite'] = time.monotonic() - started
        report['finishedUtc'] = datetime.now(timezone.utc).isoformat()
        if report['wallSecondsBeforeReportWrite'] >= 120 or datetime.now(timezone.utc) >= CUTOFF:
            report['status'] = 'failed'; report['errors'].append('audit-total-deadline-exceeded')
        raw = (json.dumps(report, separators=(',', ':'), allow_nan=False) + '\n').encode()
        need(len(raw) <= 1024 * 1024, 'audit-report-byte-cap')
        with output.open('xb') as stream:
            stream.write(raw)
        signal.setitimer(signal.ITIMER_REAL, 0)
    print(json.dumps({'status': report['status'], 'cases': len(report['cases']), 'errors': report['errors'],
                      'wallSecondsBeforeReportWrite': report['wallSecondsBeforeReportWrite']}))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    need(len(sys.argv) == 3, 'usage-root-audit-manifest-sha256')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2]))
