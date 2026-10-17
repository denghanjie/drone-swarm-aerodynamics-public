"""One independent saved-data audit. No scientific helper imports or execution.

Only standard-library JSON/metadata/byte inspection is performed. The audit
compares saved evidence; it does not reevaluate zero predicates, coefficients,
preparation, roots, native loads, arithmetic fixtures or corruption validators.
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import time

PACKAGE = 'research/m31-tree-first-reference-2026-10-17'
FRESH = 'research/m31-native-fresh-transfer-2026-10-17'
COMMIT = 'e9c464b04b43e4f8dff5904bc657969d6ab1d3d6'
MANIFEST_SHA = '4e8658c657416e99096ff581528e5006021fc7d0f0590c8ab1610ba307317cd6'
SCENES = [
    'offset-singleton', 'dense-cube-27', 'dense-cube-64', 'sparse-cube-64',
    'four-columns-32', 'tilted-cube-16', 'permuted-cube-27', 'neighbor-boundary-16',
    'near-slab-outside-16', 'radial-outside-16', 'down-cut-boundary-16',
    'near-domain-refusal', 'scaled-cap-refusal', 'upward-order-refusal',
    'global-invalid-three', 'center-guard-fallback', 'center-guard-equality',
    'raw-force-refusal', 'positive', 'distant-zero', 'raw-force',
    'order-incompatible', 'fresh-a-t5', 'fresh-b-t5']
COUNTS = [1, 27, 64, 64, 32, 16, 27, 16, 16, 16, 16, 2, 2, 2, 3, 3, 3, 2, 3, 2, 2, 2, 64, 64]
RULES = ['neighbor', 'upstream', 'down-cut', 'near-outside', 'radial']
COMMON = ['id', 'input', 'prepared', 'planned', 'globalInvalid', 'globalGuard',
          'order', 'status', 'branch', 'witness', 'referenceClass', 'tree', 'loads']
FIXTURES = ['one-word', 'signed-zero', 'minimum-subnormal', 'halfway-even-down',
            'halfway-even-up', 'subnormal-half-to-zero', 'negative-halfway-even',
            'scalar-inside-box', 'euclidean-3-4-5', 'strict-threshold-inclusive',
            'strict-threshold-fail', 'reference-overlap-unresolved',
            'rational-square-root-enclosure', 'signed-moment-cancellation']
CONTROL_EXPECTED = {
    'positive-falsely-zero': ('dense-cube-27', 1, 'node-proof-rule'),
    'dropped-source': ('dense-cube-27', 1, 'scalar-pair-canonical-membership'),
    'duplicate-plus-omission-equal-count': ('dense-cube-27', 1, 'scalar-member-list'),
    'forged-node-bound': ('dense-cube-27', 1, 'tree-identity'),
    'index-id-swap': ('permuted-cube-27', 6, 'scalar-j'),
    'guard-bypass-zero': ('center-guard-fallback', 15, 'scalar-oracle')}


class AuditFailure(Exception):
    pass


def require(value, code):
    if not value:
        raise AuditFailure(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def pair_key(pair):
    return pair['ii'], pair['r'], pair['jj']


def pin_file(root, pin):
    path = Path(pin['path'])
    require(not path.is_absolute() and '..' not in path.parts, 'safe-pin-path')
    data = (root / path).read_bytes()
    require(len(data) == pin['bytes'] and sha(data) == pin['sha256'], 'file-pin:' + str(path))
    return data


def committed_pins(root, pins):
    """Read exact-commit blobs with bounded local git batches; no network."""
    verified = 0
    for begin in range(0, len(pins), 48):
        group = pins[begin:begin + 48]
        request = ''.join(COMMIT + ':' + pin['path'] + '\n' for pin in group).encode()
        proc = subprocess.run(['git', 'cat-file', '--batch'], input=request,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=root, check=False, timeout=25)
        require(proc.returncode == 0, 'git-batch-exit')
        cursor = 0
        for pin in group:
            newline = proc.stdout.index(b'\n', cursor)
            header = proc.stdout[cursor:newline].split()
            require(len(header) == 3 and header[1] == b'blob', 'git-blob-header')
            size = int(header[2])
            start = newline + 1
            blob = proc.stdout[start:start + size]
            require(proc.stdout[start + size:start + size + 1] == b'\n', 'git-blob-framing')
            require(size == pin['bytes'] and sha(blob) == pin['sha256'],
                    'committed-pin:' + pin['path'])
            cursor = start + size + 1
            verified += 1
        require(cursor == len(proc.stdout), 'git-batch-trailing-bytes')
    return verified


def canonical_from_saved(full):
    bad = next((row for row in full['prepared'] if row['rejection'] is not None), None)
    if bad is not None:
        return 'rejected', bad['rejection'], {'id': bad['id']}
    rejected = next((p for p in full['pairs'] if p['oracle']['status'] == 'rejected'), None)
    uncertain = next((p for p in full['pairs'] if p['oracle']['status'] == 'reference-undecidable'), None)
    rank = {identifier: i for i, identifier in enumerate(full['order'])}
    wrong = next((p for p in full['pairs'] if p['oracle']['status'] == 'positive'
                  and rank[p['j']] >= rank[p['i']]), None)
    if rejected is not None:
        return 'rejected', 'pair-' + rejected['oracle']['branch'], {k: rejected[k] for k in ('i', 'r', 'j')}
    if uncertain is not None:
        return 'reference-undecidable', 'pair-' + uncertain['oracle']['branch'], {k: uncertain[k] for k in ('i', 'r', 'j')}
    if wrong is not None:
        return 'rejected', 'ordering', {k: wrong[k] for k in ('i', 'r', 'j')}
    if sum(p['oracle']['status'] == 'positive' for p in full['pairs']) > 2000000:
        return 'resource', 'positive-term-budget', None
    return 'admitted', 'loads', None


def audit_scene(full, tree, descriptor, ordinal):
    name, n = SCENES[ordinal], COUNTS[ordinal]
    require(full['id'] == tree['id'] == descriptor['id'] == name, 'scene-identity:' + name)
    require(descriptor['n'] == n, 'scene-count:' + name)
    for field in COMMON:
        require(full[field] == tree[field], 'exact-common-' + field + ':' + name)
    ids = [row['id'] for row in full['input']['drones']]
    require(len(ids) == n and len(set(ids)) == n, 'unique-input-ids:' + name)
    require([row['id'] for row in full['prepared']] == ids, 'prepared-id-order:' + name)
    planned = 4 * n * (n - 1)
    require(full['planned'] == planned, 'planned-pairs:' + name)
    required = 0 if full['globalInvalid'] else planned
    expected_keys = ([] if full['globalInvalid'] else
                     [(i, r, j) for i in range(n) for r in range(4) for j in range(n) if j != i])
    require([pair_key(p) for p in full['pairs']] == expected_keys, 'complete-full-oracle:' + name)
    full_pairs = {pair_key(p): p for p in full['pairs']}
    scalar_pairs = {pair_key(p): p for p in tree['pairs']}
    require(len(scalar_pairs) == len(tree['pairs']), 'unique-scalar-keys:' + name)
    for variant in (full, tree):
        for pair in variant['pairs']:
            i, r, j = pair_key(pair)
            require(type(i) is int and type(j) is int and type(r) is int
                    and 0 <= i < n and 0 <= j < n and i != j and 0 <= r < 4,
                    'pair-index-domain:' + name)
            require(pair['i'] == ids[i] and pair['j'] == ids[j], 'pair-index-id-binding:' + name)
            require(pair['oracle']['status'] in ('zero', 'positive', 'rejected', 'reference-undecidable'),
                    'pair-status:' + name)
            require(('coefficient' in pair) == (pair['oracle']['status'] == 'positive'),
                    'coefficient-presence:' + name)
    for key, pair in scalar_pairs.items():
        require(key in full_pairs and pair == full_pairs[key], 'exact-scalar-record:' + name)
    full_positive = {key: p['coefficient'] for key, p in full_pairs.items() if p['oracle']['status'] == 'positive'}
    tree_positive = {key: p['coefficient'] for key, p in scalar_pairs.items() if p['oracle']['status'] == 'positive'}
    require(full_positive == tree_positive, 'complete-positive-support-and-boxes:' + name)
    require(canonical_from_saved(full) == (full['status'], full['branch'], full['witness']),
            'canonical-decision:' + name)
    expected_class = 'admitted' if full['status'] == 'admitted' else full['status'] + ':' + full['branch']
    require(full['referenceClass'] == expected_class, 'canonical-reference-class:' + name)

    cov = tree['coverage']
    require(cov['schema'] == 'm31-tree-first-coverage-v1' and cov['complete'] is True,
            'coverage-header:' + name)
    expected_mode = ('global-preparation' if full['globalInvalid'] else
                     'hierarchy' if full['globalGuard']['passed'] else 'fallback')
    require(cov['mode'] == expected_mode, 'guard-mode:' + name)
    require(cov['logicalPairs'] == planned and cov['requiredCoveredPairs'] == required
            and cov['coveredPairs'] == required, 'coverage-counts:' + name)
    expected_permutation = ([] if full['globalInvalid'] else
                            ids if full['tree'] is None else full['tree']['permutation'])
    require(cov['permutation'] == expected_permutation, 'permutation-identity:' + name)
    if not full['globalInvalid']:
        require(sorted(expected_permutation) == sorted(ids) and len(set(expected_permutation)) == n,
                'permutation-bijection:' + name)
        require(sorted(full['order']) == sorted(ids), 'solve-order-bijection:' + name)
    permutation = expected_permutation
    inverse_input = {identifier: i for i, identifier in enumerate(ids)}
    inverse_position = {identifier: p for p, identifier in enumerate(permutation)}
    parent, nodes = {}, []
    if full['tree'] is not None:
        nodes = full['tree']['nodes']
        for index, node in enumerate(nodes):
            require(node['id'] == index and 0 <= node['start'] < node['end'] <= n,
                    'node-identity-range:' + name)
            if node['left'] is None:
                require(node['right'] is None and node['end'] - node['start'] <= 8,
                        'leaf-capacity:' + name)
            else:
                left, right = node['left'], node['right']
                require(index < left < right < len(nodes), 'acyclic-child-order:' + name)
                require(left not in parent and right not in parent, 'unique-node-parent:' + name)
                parent[left] = parent[right] = index
                a, b = nodes[left], nodes[right]
                require(a['start'] == node['start'] and a['end'] == b['start']
                        and b['end'] == node['end']
                        and a['end'] - a['start'] == (node['end'] - node['start']) // 2,
                        'node-child-partition:' + name)
        require(nodes[0]['start'] == 0 and nodes[0]['end'] == n
                and set(parent) == set(range(1, len(nodes))), 'tree-root-and-reachability:' + name)
    queries = cov['queries']
    expected_queries = [] if full['globalInvalid'] else [(i, r) for i in range(n) for r in range(4)]
    require([(q['i'], q['r']) for q in queries] == expected_queries, 'query-order:' + name)
    zero_keys, leaf_keys = set(), set()
    rules, work = Counter(), Counter()
    for query in queries:
        i, r = query['i'], query['r']
        self_position = inverse_position[ids[i]]
        require(query['id'] == ids[i] and query['selfPosition'] == self_position,
                'query-id-self-position:' + name)
        cursor, covered, visited = 0, [], set()
        for terminal in query['terminals']:
            start, end = terminal['start'], terminal['end']
            require(type(start) is int and type(end) is int and start == cursor and start < end <= n,
                    'terminal-range-partition:' + name)
            cursor = end
            members = sorted(inverse_input[permutation[p]] for p in range(start, end) if p != self_position)
            require(terminal['count'] == len(members), 'terminal-self-adjustment:' + name)
            covered.extend(members)
            kind = terminal['kind']
            if kind in ('zero', 'leaf'):
                require(expected_mode == 'hierarchy', 'hierarchy-without-guard:' + name)
                node_id = terminal['node']
                require(type(node_id) is int and 0 <= node_id < len(nodes), 'terminal-node-id:' + name)
                node = nodes[node_id]
                require(start == node['start'] and end == node['end'], 'terminal-node-range:' + name)
                current = node_id
                while True:
                    visited.add(current)
                    if current == 0:
                        break
                    current = parent[current]
            else:
                require(kind == 'scan' and expected_mode == 'fallback' and terminal['node'] is None
                        and start == 0 and end == n, 'fallback-scan:' + name)
            if kind == 'zero':
                rule = terminal['proofRule']
                require(rule in RULES and 'sourceIndices' not in terminal, 'compact-zero-proof:' + name)
                rules[rule] += 1
                work['zeroNodes'] += 1
                work['zeroPairs'] += len(members)
                work['nodeRuleTests'] += RULES.index(rule) + 1
                for j in members:
                    key = i, r, j
                    require(full_pairs[key]['oracle']['status'] == 'zero', 'zero-member-full-oracle:' + name)
                    require(key not in zero_keys, 'unique-zero-member:' + name)
                    zero_keys.add(key)
            else:
                require(terminal['sourceIndices'] == members, 'exact-leaf-member-list:' + name)
                if kind == 'leaf':
                    require(node['left'] is None and node['right'] is None, 'actual-leaf:' + name)
                    work['leafVisits'] += 1
                for j in members:
                    key = i, r, j
                    require(key not in leaf_keys, 'unique-scalar-membership:' + name)
                    leaf_keys.add(key)
        require(cursor == n and sorted(covered) == [j for j in range(n) if j != i],
                'complete-nonself-query-partition:' + name)
        work['nodeVisits'] += len(visited)
        work['nodeRuleTests'] += 5 * (len(visited) - sum(t['kind'] == 'zero' for t in query['terminals']))
    require(not zero_keys.intersection(leaf_keys) and zero_keys.union(leaf_keys) == set(expected_keys),
            'complete-disjoint-scene-partition:' + name)
    require(set(scalar_pairs) == leaf_keys and [pair_key(p) for p in tree['pairs']] == sorted(leaf_keys),
            'canonical-scalar-record-coverage:' + name)
    work.update({'preparationCalls': n, 'globalProofs': 0 if full['globalInvalid'] else 1,
                 'treeNodes': len(nodes), 'scalarPairs': len(scalar_pairs),
                 'scalarZeroPairs': sum(p['oracle']['status'] == 'zero' for p in tree['pairs']),
                 'positiveTerms': len(tree_positive),
                 'rejectedPairs': sum(p['oracle']['status'] == 'rejected' for p in tree['pairs']),
                 'unresolvedPairs': sum(p['oracle']['status'] == 'reference-undecidable' for p in tree['pairs'])})
    require(set(cov['work']) == {'preparationCalls', 'globalProofs', 'treeNodes', 'nodeVisits',
                                'nodeRuleTests', 'zeroNodes', 'zeroPairs', 'leafVisits', 'scalarPairs',
                                'scalarZeroPairs', 'positiveTerms', 'rejectedPairs', 'unresolvedPairs'},
            'work-field-set:' + name)
    require(all(type(value) is int and value == work[key] for key, value in cov['work'].items()),
            'recomputed-work-counts:' + name)
    root_boxes = load_boxes = negative_load_endpoints = 0
    if full['status'] == 'admitted':
        require([row['id'] for row in full['loads']] == ids, 'load-id-order:' + name)
        for row in full['loads']:
            require(len(row['roots']) == 4, 'four-root-boxes:' + name)
            values = row['loads']
            require(set(values) == {'rotor', 'collective', 'force', 'moment'}
                    and len(values['rotor']) == 4 and len(values['force']) == len(values['moment']) == 3,
                    'signed-load-category-completeness:' + name)
            boxes = values['rotor'] + [values['collective']] + values['force'] + values['moment']
            root_boxes += 4
            load_boxes += len(boxes)
            negative_load_endpoints += sum(box[side]['n'].startswith('-') for box in boxes for side in ('l', 'u'))
    else:
        require(full['loads'] == [], 'failure-has-no-loads:' + name)
    require(descriptor['fullOracleCalls'] == len(full_pairs)
            and descriptor['treeOracleCalls'] == len(scalar_pairs), 'recorded-call-counts:' + name)
    val = descriptor['validation']
    expected_summary = {'passed': True, 'logicalPairs': planned, 'coveredPairs': required,
                        'fullOraclePairs': len(full_pairs), 'scalarPairs': len(scalar_pairs),
                        'provedZeroPairs': len(zero_keys), 'positivePairs': len(full_positive),
                        'zeroProofNodes': work['zeroNodes'], 'zeroProofRules': dict(rules),
                        'queries': len(queries), 'exactPositiveCoefficients': True,
                        'exactRoots': True, 'exactSignedLoads': True,
                        'canonicalDecision': {'status': full['status'], 'branch': full['branch'], 'witness': full['witness']}}
    require(val == expected_summary, 'saved-validator-summary:' + name)
    return {'id': name, 'n': n, 'mode': expected_mode, 'status': full['status'], 'branch': full['branch'],
            'canonicalWitness': full['witness'], 'plannedPairs': planned, 'coveredPairs': required,
            'fullOraclePairs': len(full_pairs), 'scalarPairs': len(scalar_pairs),
            'provedZeroPairs': len(zero_keys), 'positivePairs': len(full_positive),
            'zeroProofRules': dict(rules), 'queries': len(queries), 'rootBoxesCompared': root_boxes,
            'signedLoadBoxesCompared': load_boxes, 'negativeLoadEndpointsCompared': negative_load_endpoints,
            'work': dict(cov['work']), 'savedEvidenceChecksPassed': True}


def expected_control_changes(control_id, baseline):
    pairs = baseline['pairs']
    positions = {pair_key(pair): i for i, pair in enumerate(pairs)}
    work = baseline['coverage']['work']
    changes = []
    def add(path, before, after):
        require(before != after, 'control-mutation-nonempty:' + control_id)
        changes.append({'path': path, 'before': deepcopy(before), 'after': deepcopy(after)})
    def changed_work(deltas):
        after = deepcopy(work)
        for key, delta in deltas.items():
            after[key] += delta
        add('coverage/work', work, after)
    if control_id == 'positive-falsely-zero':
        term = baseline['coverage']['queries'][0]['terminals'][0]
        require(term['sourceIndices'] == [1, 3, 9, 10, 18] and term['node'] == 2, 'control-positive-fixed-leaf')
        add('coverage/queries/0/terminals/0', term,
            {'kind': 'zero', 'node': 2, 'start': 0, 'end': 6, 'count': 5, 'proofRule': 'neighbor'})
        removed = [pairs[positions[(0, 0, j)]] for j in [1, 3, 9, 10, 18]]
        require(removed[2]['oracle'] == {'status': 'positive', 'branch': 'active'}, 'control-positive-witness')
        add('pairs@keys=(0,0,[1,3,9,10,18])', removed, [])
        changed_work({'scalarPairs': -5, 'scalarZeroPairs': -3, 'positiveTerms': -2,
                      'zeroPairs': 5, 'zeroNodes': 1, 'leafVisits': -1})
    elif control_id == 'dropped-source':
        p = positions[(0, 0, 1)]
        require(pairs[p]['j'] == 101 and pairs[p]['oracle']['status'] == 'zero', 'control-drop-fixed-zero')
        add('pairs/' + str(p), pairs[p], None)
        changed_work({'scalarPairs': -1, 'scalarZeroPairs': -1})
    elif control_id == 'duplicate-plus-omission-equal-count':
        dest, source = positions[(0, 0, 1)], positions[(0, 0, 3)]
        require(pairs[dest]['oracle']['status'] == pairs[source]['oracle']['status'] == 'zero'
                and pairs[dest]['j'] == 101 and pairs[source]['j'] == 103, 'control-duplicate-fixed-zeros')
        add('coverage/queries/0/terminals/0/sourceIndices', [1, 3, 9, 10, 18], [3, 3, 9, 10, 18])
        add('pairs/' + str(dest), pairs[dest], pairs[source])
    elif control_id == 'forged-node-bound':
        lower, upper = baseline['tree']['nodes'][0]['center'][0]
        require(lower == {'n': '1170935903116329', 'd': '9007199254740992'}
                and upper == {'n': '8376695306909123', 'd': '9007199254740992'}, 'control-forged-fixed-bound')
        add('tree/nodes/0/center/0/0', lower, upper)
    elif control_id == 'index-id-swap':
        first, second = positions[(0, 0, 9)], positions[(0, 0, 18)]
        require(pairs[first]['j'] == 118 and pairs[second]['j'] == 109
                and pairs[first]['oracle']['status'] == pairs[second]['oracle']['status'] == 'positive'
                and pairs[first]['coefficient'] != pairs[second]['coefficient'], 'control-index-fixed-positives')
        add('pairs/' + str(first) + '/j', 118, 109)
        add('pairs/' + str(second) + '/j', 109, 118)
    else:
        p = positions[(0, 0, 1)]
        require(baseline['globalGuard']['passed'] is False and baseline['coverage']['mode'] == 'fallback'
                and pairs[p]['i'] == 741 and pairs[p]['j'] == 742
                and pairs[p]['oracle'] == {'status': 'rejected', 'branch': 'center-guard'}, 'control-guard-fixed-refusal')
        add('pairs/' + str(p) + '/oracle', pairs[p]['oracle'], {'status': 'zero', 'branch': 'neighbor'})
        changed_work({'rejectedPairs': -1, 'scalarZeroPairs': 1})
    return changes


def main(root):
    started = time.monotonic()
    package = root / PACKAGE
    output = package / 'review/saved-result-audit.json'
    require(not output.exists(), 'single-audit-output-exists')
    report = {'schema': 'm31-tree-first-independent-saved-audit-v1',
              'startedUtc': datetime.now(timezone.utc).isoformat(), 'status': 'running',
              'sourceCommit': COMMIT, 'sourceManifestSha256': MANIFEST_SHA,
              'scientificModulesImported': False, 'scientificOrNativeExecutions': 0,
              'browserCalls': 0, 'networkCalls': 0, 'processingCapSeconds': 180,
              'scope': 'Saved evidence and byte/metadata checks only; no numerical recomputation.',
              'cases': [], 'errors': []}
    def timeout(signum, frame):
        raise AuditFailure('saved-audit-processing-deadline')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(175)
    try:
        raw_index = (package / 'results/index.json').read_bytes()
        index = json.loads(raw_index)
        report['resultIndexSha256'] = sha(raw_index)
        require(index['sourceCommit'] == COMMIT and index['sourceManifestSha256'] == MANIFEST_SHA
                and index['status'] == 'completed' and index['complete'] is True and index['qualified'] is True,
                'completed-result-identity')
        require(index['newSimulations'] == index['newBrowserCalls'] == 0
                and index['physicalValidation'] is False and index['performanceClaim'] is False,
                'scope-flags')
        require([x['id'] for x in index['cases']] == SCENES and len(index['cases']) == 24,
                'literal-24-scene-order')
        require(index['expectedCases'] == 24 and index['expectedLogicalPairs'] == 79048
                and index['scalarOracleCap'] == 160000, 'fixed-allocation')
        manifest_raw = (package / 'source-manifest.json').read_bytes()
        require(sha(manifest_raw) == MANIFEST_SHA, 'manifest-current-hash')
        manifest = json.loads(manifest_raw)
        pins = manifest['files']
        require(len(pins) == 585 and len({p['path'] for p in pins}) == 585, '585-unique-source-pins')
        for pin in pins:
            pin_file(root, pin)
        manifest_pin = {'path': PACKAGE + '/source-manifest.json', 'bytes': len(manifest_raw), 'sha256': MANIFEST_SHA}
        committed = committed_pins(root, pins + [manifest_pin])
        publication = load(package / 'source-publication.json')
        start_receipt = load(package / 'STARTED.json')
        require(publication['commit'] == COMMIT and publication['manifestSha256'] == MANIFEST_SHA
                and publication['verifiedFilePins'] == 585
                and publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True,
                'saved-publication-receipt')
        require(start_receipt['sourceCommit'] == COMMIT and start_receipt['sourceManifestSha256'] == MANIFEST_SHA
                and start_receipt['sourcePinsVerified'] == 585 and index['sourcePinsAfter'] == 585
                and index['outputsPreserved'] is True, 'saved-before-after-source-receipts')
        report['sourcePins'] = {'localVerified': len(pins), 'exactCommitVerified': committed - 1,
                                'manifestExactCommitVerified': True, 'declaredSourceBytes': sum(p['bytes'] for p in pins),
                                'remotePublicationReceiptConsistent': True, 'remoteRefetchedByAudit': False}
        evidence_files, evidence_bytes, retained = [], 0, {}
        for ordinal, descriptor in enumerate(index['cases']):
            full_raw = pin_file(root, descriptor['full'])
            tree_raw = pin_file(root, descriptor['tree'])
            full, tree = json.loads(full_raw), json.loads(tree_raw)
            reduction = audit_scene(full, tree, descriptor, ordinal)
            report['cases'].append(reduction)
            evidence_files.extend([descriptor['full']['path'], descriptor['tree']['path']])
            evidence_bytes += len(full_raw) + len(tree_raw)
            if descriptor['id'] in ('dense-cube-27', 'permuted-cube-27', 'center-guard-fallback'):
                retained[descriptor['id']] = tree
            if descriptor['id'] in ('fresh-a-t5', 'fresh-b-t5'):
                old = load(root / FRESH / ('results/reference/' + descriptor['id'] + '.json'))
                raw = load(root / FRESH / ('results/inputs/' + descriptor['id'] + '.json'))
                require(full['input'] == raw and full['prepared'] == old['prepared']
                        and full['loads'] == old['loads'], 'fresh-saved-input-prepared-loads:' + descriptor['id'])
                saved_positive = {(p['i'], p['r'], p['j']): p['coefficient'] for p in old['pairs'] if p['status'] == 'positive'}
                new_positive = {(p['i'], p['r'], p['j']): p['coefficient'] for p in tree['pairs'] if p['oracle']['status'] == 'positive'}
                require(saved_positive == new_positive, 'fresh-saved-positive-support:' + descriptor['id'])
        events_raw = pin_file(root, index['eventJournal'])
        events = [json.loads(line) for line in events_raw.splitlines()]
        require(len(events) == 48, '48-event-lines')
        running_calls = 0
        for ordinal, descriptor in enumerate(index['cases']):
            start, finish = events[2 * ordinal:2 * ordinal + 2]
            require(start == {'event': 'start', 'ordinal': ordinal, 'id': SCENES[ordinal], 'callsBefore': running_calls},
                    'event-start:' + SCENES[ordinal])
            running_calls += descriptor['fullOracleCalls'] + descriptor['treeOracleCalls']
            require(finish == {'event': 'complete', 'ordinal': ordinal, 'id': SCENES[ordinal],
                               'full': descriptor['full'], 'tree': descriptor['tree'], 'callsAfter': running_calls},
                    'event-complete:' + SCENES[ordinal])
        require(running_calls == index['scalarOracleCalls'] == 105578 and running_calls <= 160000,
                'combined-oracle-count')
        evidence_files.append(index['eventJournal']['path'])
        evidence_bytes += len(events_raw)
        require(evidence_bytes == index['resultBytesBeforeIndex'], 'result-byte-accounting')
        actual_files = {str(p.relative_to(root)) for p in (package / 'results').rglob('*') if p.is_file()}
        require(actual_files == set(evidence_files) | {PACKAGE + '/results/index.json'}, 'exact-result-file-set')
        report['outputs'] = {'pinnedSceneFilesVerified': 48, 'eventJournalPinVerified': True,
                             'eventLinesVerified': 48, 'bytesBeforeIndex': evidence_bytes,
                             'actualResultFiles': len(actual_files), 'indexBytes': len(raw_index)}
        controls = index['coverageCorruptions']
        require([c['id'] for c in controls] == list(CONTROL_EXPECTED), 'six-literal-control-order')
        control_reduction = []
        for control in controls:
            cid = control['id']
            scene, ordinal, failure = CONTROL_EXPECTED[cid]
            require(control['scene'] == scene and control['sceneOrdinal'] == ordinal,
                    'control-scene:' + cid)
            require(all(control[field] is True for field in ('executed', 'witnessPreconditionsPassed',
                        'baselineValidatedByDriver', 'rejected', 'intendedCoreFailure', 'detected')),
                    'control-success-flags:' + cid)
            require(control['requiredFailureFamilies'] == [failure]
                    and control['observedException'] == {'class': 'ValidationError', 'message': failure},
                    'control-specific-failure:' + cid)
            require(control['changedFields'] == expected_control_changes(cid, retained[scene]),
                    'control-saved-before-after:' + cid)
            control_reduction.append({'id': cid, 'scene': scene, 'requiredAndObservedFailure': failure,
                                      'beforeAfterVerifiedAgainstBaseline': True, 'changedFieldCount': len(control['changedFields'])})
        report['coverageCorruptions'] = control_reduction
        require(index['arithmeticFixtures'] == [{'id': name, 'passed': True} for name in FIXTURES],
                'fourteen-arithmetic-reports')
        old_check = load(root / FRESH / 'results/check.json')
        require(index['nativeCalls'] == old_check['calls'] and len(index['nativeCalls']) == 4
                and all(x['qualified'] is True and x['decision'] == 'qualified' for x in index['nativeCalls']),
                'four-unchanged-native-reports')
        require(index['loadCorruptions'] == old_check['corruptionChecks'] and len(index['loadCorruptions']) == 4
                and all(x['passed'] is True for x in index['loadCorruptions']), 'four-unchanged-load-corruption-reports')
        report['retainedReports'] = {'arithmeticFixtureIds': FIXTURES, 'arithmeticPassed': 14,
                                     'nativeReportsExactlyEqualSavedFresh': 4,
                                     'loadCorruptionReportsExactlyEqualSavedFresh': 4,
                                     'freshInputPreparedLoadAndPositiveMapsExactlyEqual': 2,
                                     'reevaluatedByAudit': False}
        numeric = ['plannedPairs', 'coveredPairs', 'fullOraclePairs', 'scalarPairs', 'provedZeroPairs',
                   'positivePairs', 'queries', 'rootBoxesCompared', 'signedLoadBoxesCompared', 'negativeLoadEndpointsCompared']
        report['totals'] = {key: sum(row[key] for row in report['cases']) for key in numeric}
        totals = report['totals']
        require(totals['plannedPairs'] == 79048
                and totals['fullOraclePairs'] + totals['scalarPairs'] == 105578
                and totals['coveredPairs'] == totals['scalarPairs'] + totals['provedZeroPairs'], 'cross-case-totals')
        aggregate_work, aggregate_rules = Counter(), Counter()
        for row in report['cases']:
            aggregate_work.update(row['work'])
            aggregate_rules.update(row['zeroProofRules'])
        report['workTotals'] = dict(aggregate_work)
        report['zeroProofRuleTotals'] = dict(aggregate_rules)
        report['decisionTotals'] = dict(Counter(row['status'] + ':' + row['branch'] for row in report['cases']))
        report['modeTotals'] = dict(Counter(row['mode'] for row in report['cases']))
        report['savedRunWallSeconds'] = index['wallSeconds']
        require(0 <= index['wallSeconds'] < 600, 'saved-run-within-allocation')
        require(datetime.fromisoformat(publication['verifiedUtc']) < datetime.fromisoformat(start_receipt['utc'])
                <= datetime.fromisoformat(index['startedUtc']) < datetime.fromisoformat(index['finishedUtc'])
                < datetime(2026, 10, 17, 3, tzinfo=timezone.utc), 'publication-execution-time-order')
        # Re-read audited sources and result files at closure; byte checks only.
        for pin in pins:
            pin_file(root, pin)
        for descriptor in index['cases']:
            pin_file(root, descriptor['full'])
            pin_file(root, descriptor['tree'])
        pin_file(root, index['eventJournal'])
        require((package / 'results/index.json').read_bytes() == raw_index, 'result-index-unchanged')
        report['sourceAndResultBytesUnchangedAfterAudit'] = True
        report['status'] = 'passed'
    except Exception as error:
        report['status'] = 'failed'
        report['errors'].append({'class': type(error).__name__, 'message': str(error)[:500]})
    finally:
        signal.alarm(0)
        report['processingSeconds'] = time.monotonic() - started
        report['finishedUtc'] = datetime.now(timezone.utc).isoformat()
        if report['processingSeconds'] >= 180:
            report['status'] = 'failed'
            report['errors'].append({'class': 'AuditFailure', 'message': '180-second-cap-exceeded'})
        payload = (json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
        require(len(payload) < 8 * 1024 * 1024, 'audit-output-byte-cap')
        with output.open('xb') as stream:
            stream.write(payload)
    print(json.dumps({'status': report['status'], 'processingSeconds': report['processingSeconds'],
                      'caseCount': len(report['cases']), 'errors': report['errors'],
                      'totals': report.get('totals'), 'outputSha256': sha(payload)}))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    require(len(sys.argv) == 2, 'usage-root')
    raise SystemExit(main(Path(sys.argv[1]).resolve()))
