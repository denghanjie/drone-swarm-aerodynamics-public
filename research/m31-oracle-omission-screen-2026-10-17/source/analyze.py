"""Oracle-assisted retrospective coefficient-mass screen. No simulator imports."""
import hashlib
import json
import struct
from fractions import Fraction as F

STATES = ['run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10']
TIERS = ['1e-8', '1e-4', '1e-2']
PRIOR = 'research/m31-normalizer-replication-2026-10-17/results'


def need(test, code):
    if not test:
        raise ValueError(code)


def wire(x):
    return str(x.numerator) + '/' + str(x.denominator)


def endpoint(x):
    need(set(x) == {'n', 'd'}, 'rational-shape')
    return F(int(x['n']), int(x['d']))


def center(word):
    return F.from_float(struct.unpack('>d', bytes.fromhex(word))[0])


def tree_for(ids, centers, capacity):
    nodes, permutation = [], []

    def visit(members):
        node_id = len(nodes)
        node = {'id': node_id, 'start': len(permutation), 'end': None,
                'left': None, 'right': None}
        nodes.append(node)
        if len(members) <= capacity:
            permutation.extend(members)
        else:
            spans = [max(centers[i][k] for i in members) -
                     min(centers[i][k] for i in members) for k in range(3)]
            axis = max(range(3), key=lambda k: (spans[k], -k))
            ordered = sorted(members, key=lambda i: (centers[i][axis], i))
            mid = len(ordered) // 2
            node['left'] = visit(ordered[:mid])
            node['right'] = visit(ordered[mid:])
        node['end'] = len(permutation)
        return node_id

    visit(ids)
    for n in nodes:
        n['members'] = permutation[n['start']:n['end']]
    return {'capacity': capacity, 'permutation': permutation, 'nodes': nodes}


def select(tree, receiver, weights, budget):
    used, selected, fallback = F(0), [], []
    attempts = 0

    def visit(node_id):
        nonlocal used, attempts
        attempts += 1
        node = tree['nodes'][node_id]
        members = node['members']
        if receiver not in members:
            positive = [j for j in members if weights[j][1] > 0]
            upper = sum((weights[j][1] for j in members), F(0))
            if len(positive) >= 2 and used + upper <= budget:
                selected.append({'node': node_id, 'members': members,
                                 'positiveMembers': positive, 'massUpper': wire(upper)})
                used += upper
                return
        if node['left'] is None:
            fallback.extend(j for j in members if j != receiver)
        else:
            visit(node['left'])
            visit(node['right'])

    visit(0)
    return {'selected': selected, 'fallback': fallback, 'usedUpper': wire(used),
            'positiveCovered': sum(len(n['positiveMembers']) for n in selected),
            'selectedMembers': sum(len(n['members']) for n in selected),
            'nodeVisits': attempts}


def prefix(entries, budget):
    used, members = F(0), []
    for value, j in sorted(entries):
        if used + value > budget:
            break
        used += value
        members.append(j)
    return members, used


def fixtures():
    passed = []

    def case(name, condition):
        need(condition, 'fixture:' + name)
        passed.append({'name': name, 'passed': True})

    case('zero-lower-positive-included', prefix([(F(0), 7), (F(1), 8)], F(0)) == ([7], F(0)))
    case('exact-budget-equality', prefix([(F(1, 3), 1), (F(2, 3), 2)], F(1)) == ([1, 2], F(1)))
    case('tiny-overflow', prefix([(F(1, 3), 1), (F(2, 3), 2)], F(1) - F(1, 10**50))[0] == [1])
    case('tied-stable-id', prefix([(F(1, 10**50), 9), (F(1, 10**50), 2)], F(1, 10**50))[0] == [2])
    case('zero-positive-row', prefix([], F(1)) == ([], F(0)))
    centers = {i: [F(i), F(0), F(0)] for i in range(8)}
    coarse, fine = tree_for(list(centers), centers, 4), tree_for(list(centers), centers, 2)
    weights = {i: (v, v) for i, v in enumerate([F(1), F(1), F(100), F(100)] + [F(3, 5)] * 4)}
    case('greedy-refinement-can-reduce-count',
         select(coarse, 99, weights, F(5, 2))['positiveCovered'] == 4 and
         select(fine, 99, weights, F(5, 2))['positiveCovered'] == 2)
    tiny = tree_for([0, 1], centers, 8)
    case('self-leaf-falls-back', select(tiny, 0, {1: (F(1), F(1))}, F(10))['fallback'] == [1])
    four = tree_for([0, 1, 2, 3], centers, 2)
    w = {0: (F(1), F(1)), 1: (F(0), F(0)), 2: (F(1, 2), F(1, 2)), 3: (F(1, 2), F(1, 2))}
    got = select(four, 99, w, F(1))
    case('one-positive-does-not-spend', len(got['selected']) == 1 and got['selected'][0]['members'] == [2, 3])
    got = select(four, 99, w, F(2))
    case('accepted-parent-prevents-overlap', len(got['selected']) == 1 and got['selected'][0]['node'] == 0 and not got['fallback'])
    return passed


def run(root):
    output = {'schema': 'm31-oracle-omission-screen-v1',
              'scope': 'Retrospective oracle coefficient-mass analysis; no executable bound, load-error or speed claim',
              'tiers': TIERS, 'fixtures': fixtures(), 'states': []}
    for name in STATES:
        paths = {k: root / PRIOR / d / (name + suffix) for k, d, suffix in
                 [('input', 'inputs', '.json'), ('reference', 'reference', '.json'),
                  ('baseline', 'calls', '-baseline-r0.json')]}
        data = {k: json.loads(p.read_bytes()) for k, p in paths.items()}
        inp, ref, base = data['input'], data['reference'], data['baseline']
        ids = [d['id'] for d in inp['drones']]
        need(len(ids) == 64 and len(set(ids)) == 64, 'state-id-domain')
        need(ref['referenceStatus'] == 'admitted' and ref['id'] == name, 'reference-admission')
        envelope = {'domain': 'm31-moving-admission/input/v1', 'id': name, 'input': inp}
        digest = hashlib.sha256(json.dumps(envelope, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        need(ref['inputSha256'] == digest, 'input-binding')
        need(base['input'] == inp and base['method']['result']['status'] == 'certified', 'baseline-binding')
        prepared = {d['id']: d for d in ref['prepared']}
        need(set(prepared) == set(ids) and all(d['rejection'] is None for d in prepared.values()), 'prepared-domain')
        centers = {i: [center(w) for w in prepared[i]['value']['center']] for i in ids}
        for d in inp['drones']:
            need(prepared[d['id']]['value']['center'] == d['state'][:3], 'center-identity')
        trees = {key: tree_for(ids, centers, cap) for key, cap in [('T8', 8), ('T2', 2)]}
        old_tree = base['method']['assembly']['tree']
        need(old_tree is not None and old_tree['permutation'] == trees['T8']['permutation'], 'T8-permutation')
        need(len(old_tree['nodes']) == len(trees['T8']['nodes']), 'T8-size')
        for old, new in zip(old_tree['nodes'], trees['T8']['nodes']):
            need(all(old[k] == new[k] for k in ['id', 'start', 'end', 'left', 'right']), 'T8-structure')
        lookup = {}
        for p in ref['pairs']:
            i, r, j = p['i'], p['r'], p['j']
            need(type(i) is int and type(j) is int and type(r) is int and
                 i in prepared and j in prepared and 0 <= r < 4 and i != j, 'pair-domain')
            key = (i, r, j)
            need(key not in lookup, 'pair-duplicate')
            if p['status'] == 'zero':
                need('coefficient' not in p, 'zero-coefficient')
                value = (F(0), F(0))
            else:
                need(p['status'] == 'positive', 'pair-status')
                value = tuple(endpoint(p['coefficient'][s]) for s in ['l', 'u'])
                need(0 <= value[0] <= value[1] and value[1] > 0, 'positive-interval')
            lookup[key] = value
        need(len(lookup) == 4 * 64 * 63 == ref['evaluatedPairs'] == ref['plannedPairs'], 'pair-completeness')
        state = {'id': name, 'inputSha256': ref['inputSha256'], 'trees': trees, 'rows': [],
                 'positiveTerms': sum(hi > 0 for lo, hi in lookup.values()), 'summary': []}
        need(state['positiveTerms'] == ref['graph']['positiveRotorPairs'], 'positive-denominator')
        for i in ids:
            for r in range(4):
                weights = {j: lookup[i, r, j] for j in ids if j != i}
                positive = sorted((lo, j) for j, (lo, hi) in weights.items() if hi > 0)
                upper_order = sorted((hi, j) for j, (lo, hi) in weights.items() if hi > 0)
                row = {'i': i, 'r': r, 'positiveTerms': len(positive), 'tiers': []}
                for tier in TIERS:
                    budget = F(tier) / 16
                    prefix_members, used = prefix(positive, budget)
                    feasible, upper_used = prefix(upper_order, budget)
                    row['tiers'].append({'tier': tier, 'budget': wire(budget),
                        'ceilingCount': len(prefix_members), 'ceilingMembers': prefix_members,
                        'ceilingLowerMass': wire(used),
                        'singletonFeasibleCount': len(feasible), 'singletonFeasibleMembers': feasible,
                        'singletonUpperMass': wire(upper_used),
                        'trees': {k: select(tree, i, weights, budget) for k, tree in trees.items()}})
                state['rows'].append(row)
        for ti, tier in enumerate(TIERS):
            item = {'tier': tier, 'positiveTerms': state['positiveTerms'],
                    'optimisticCeiling': sum(row['tiers'][ti]['ceilingCount'] for row in state['rows']),
                    'singletonFeasible': sum(row['tiers'][ti]['singletonFeasibleCount'] for row in state['rows']),
                    'trees': {}}
            for k in trees:
                parts = [row['tiers'][ti]['trees'][k] for row in state['rows']]
                covered = sum(x['positiveCovered'] for x in parts)
                item['trees'][k] = {'positiveCovered': covered,
                    'groups': sum(len(x['selected']) for x in parts),
                    'rowsCovered': sum(bool(x['selected']) for x in parts),
                    'membersCovered': sum(x['selectedMembers'] for x in parts),
                    'nodeVisits': sum(x['nodeVisits'] for x in parts),
                    'tenPercentCountHurdle': state['positiveTerms'] > 0 and 10 * covered >= state['positiveTerms']}
            item['ceilingTenPercentHurdle'] = state['positiveTerms'] > 0 and 10 * item['optimisticCeiling'] >= state['positiveTerms']
            state['summary'].append(item)
        output['states'].append(state)
    return output
