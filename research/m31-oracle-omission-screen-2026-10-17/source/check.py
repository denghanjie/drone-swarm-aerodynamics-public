"""Independent saved-data audit; no analyzer or scientific-kernel imports.

run(root) performs literal fixtures before opening any target file.  It then
checks the saved analysis and prior reference triples, and finally applies
in-memory corruptions to a verified saved record.  It never writes or reruns.
"""
import copy
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

STATES = ('run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10')
TIERS = ('1e-8', '1e-4', '1e-2')
BUDGETS = (Fraction(1, 1600000000), Fraction(1, 160000), Fraction(1, 1600))
PRIOR = 'research/m31-normalizer-replication-2026-10-17/results'
PACKAGE = 'research/m31-oracle-omission-screen-2026-10-17'
FILE_LIMIT = 16 * 1024 * 1024
SCOPE = 'Retrospective oracle coefficient-mass analysis; no executable bound, load-error or speed claim'
ANALYZER_FIXTURES = (
    'zero-lower-positive-included', 'exact-budget-equality', 'tiny-overflow',
    'tied-stable-id', 'zero-positive-row', 'greedy-refinement-can-reduce-count',
    'self-leaf-falls-back', 'one-positive-does-not-spend', 'accepted-parent-prevents-overlap')


class CheckError(Exception):
    pass


def need(condition, code):
    if not condition:
        raise CheckError(code)


def same(left, right):
    """Type-sensitive equality: bool cannot stand in for an integer count."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def exact(actual, expected, code):
    need(same(actual, expected), code)


def fields(value, names, code):
    need(type(value) is dict and set(value) == set(names), code)


def integer(value, code):
    need(type(value) is int and value >= 0, code)
    return value


def wire(value):
    return str(value.numerator) + '/' + str(value.denominator)


def rational(value, code='rational-normalization'):
    need(type(value) is str and re.fullmatch(r'-?(?:0|[1-9][0-9]*)/[1-9][0-9]*', value), code)
    numerator, denominator = value.split('/')
    result = Fraction(int(numerator), int(denominator))
    need(wire(result) == value, code)
    return result


def endpoint(value):
    fields(value, ('n', 'd'), 'endpoint-shape')
    need(type(value['n']) is str and type(value['d']) is str, 'endpoint-integer-strings')
    return rational(value['n'] + '/' + value['d'], 'endpoint-normalization')


def dyadic(word):
    """Decode binary64 as integers, without host floating-point evaluation."""
    need(type(word) is str and re.fullmatch(r'[0-9a-f]{16}', word), 'center-word')
    bits = int(word, 16)
    exponent, mantissa = (bits >> 52) & 2047, bits & ((1 << 52) - 1)
    need(exponent != 2047, 'center-nonfinite')
    numerator = mantissa if exponent == 0 else (1 << 52) + mantissa
    power = -1074 if exponent == 0 else exponent - 1075
    if bits >> 63:
        numerator = -numerator
    return Fraction(numerator << power) if power >= 0 else Fraction(numerator, 1 << -power)


def canonical_input_hash(name, inp):
    envelope = {'domain': 'm31-moving-admission/input/v1', 'id': name, 'input': inp}
    payload = json.dumps(envelope, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=True, allow_nan=False).encode('ascii')
    return hashlib.sha256(payload).hexdigest()


def load(root, relative, pins):
    path = root / relative
    need(path.resolve() == path and path.is_file() and not path.is_symlink(), 'file-path:' + relative)
    need(path.stat().st_size <= FILE_LIMIT, 'file-size:' + relative)
    payload = path.read_bytes()
    need(len(payload) <= FILE_LIMIT, 'file-size:' + relative)

    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'duplicate-json-key:' + relative)
            result[key] = value
        return result

    def nonfinite(value):
        raise CheckError('nonfinite-json:' + relative)

    value = json.loads(payload, object_pairs_hook=unique, parse_constant=nonfinite)
    pins.append({'path': relative, 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()})
    return value


def reconstruct(ids, centers, capacity):
    """Build split topology first; flatten it separately into a preorder tree."""
    def split(members):
        if len(members) <= capacity:
            return list(members)
        spans = []
        for axis in range(3):
            coordinates = [centers[j][axis] for j in members]
            spans.append(max(coordinates) - min(coordinates))
        axis = spans.index(max(spans))
        order = sorted(members, key=lambda j: (centers[j][axis], j))
        middle = len(order) // 2
        return (split(order[:middle]), split(order[middle:]))

    topology = split(ids)
    nodes, permutation = [], []

    def flatten(part):
        index = len(nodes)
        node = {'id': index, 'start': len(permutation), 'end': None,
                'left': None, 'right': None, 'members': []}
        nodes.append(node)
        if type(part) is list:
            permutation.extend(part)
        else:
            node['left'] = flatten(part[0])
            node['right'] = flatten(part[1])
        node['end'] = len(permutation)
        node['members'] = permutation[node['start']:node['end']]
        return index

    flatten(topology)
    return {'capacity': capacity, 'permutation': permutation, 'nodes': nodes}


def nesting(coarse, fine):
    coarse_sets = [frozenset(node['members']) for node in coarse['nodes']]
    fine_sets = [frozenset(node['members']) for node in fine['nodes']]
    leaves = [frozenset(node['members']) for node in coarse['nodes'] if node['left'] is None]
    need(all(members in fine_sets for members in coarse_sets), 'T2-nesting-coarse-node')
    need(all(members in coarse_sets or any(members <= leaf for leaf in leaves)
             for members in fine_sets), 'T2-nesting-leaf-refinement')


def prefix(weights, endpoint_index, budget):
    ordered = sorted((interval[endpoint_index], j) for j, interval in weights.items() if interval[1] > 0)
    totals = [Fraction(0)]
    for amount, _ in ordered:
        totals.append(totals[-1] + amount)
    length = max(index for index, total in enumerate(totals) if total <= budget)
    need(length == len(ordered) or totals[length + 1] > budget, 'prefix-maximality')
    return [j for _, j in ordered[:length]], totals[length]


def selection(tree, receiver, weights, budget):
    """An explicit stack supplies the independently checked left-first walk."""
    stack, used, visits, selected, fallback = [0], Fraction(0), 0, [], []
    while stack:
        node = tree['nodes'][stack.pop()]
        visits += 1
        members = node['members']
        if receiver not in members:
            positives = [j for j in members if weights[j][1] > 0]
            amount = sum((weights[j][1] for j in members), Fraction(0))
            if len(positives) >= 2 and amount <= budget - used:
                selected.append({'node': node['id'], 'members': list(members),
                                 'positiveMembers': positives, 'massUpper': wire(amount)})
                used += amount
                continue
        if node['left'] is None:
            fallback.extend(j for j in members if j != receiver)
        else:
            stack.extend((node['right'], node['left']))
    return {'selected': selected, 'fallback': fallback, 'usedUpper': wire(used),
            'positiveCovered': sum(len(group['positiveMembers']) for group in selected),
            'selectedMembers': sum(len(group['members']) for group in selected), 'nodeVisits': visits}


def check_selection(saved, tree, receiver, weights, budget):
    fields(saved, ('selected', 'fallback', 'usedUpper', 'positiveCovered', 'selectedMembers', 'nodeVisits'), 'tree-selection-shape')
    need(type(saved['selected']) is list and type(saved['fallback']) is list, 'tree-selection-lists')
    declared = rational(saved['usedUpper'])
    need(Fraction(0) <= declared <= budget, 'tree-cumulative-budget')
    covered, used = [], Fraction(0)
    for group in saved['selected']:
        fields(group, ('node', 'members', 'positiveMembers', 'massUpper'), 'tree-group-shape')
        index = integer(group['node'], 'tree-node-id')
        need(index < len(tree['nodes']), 'tree-node-domain')
        exact(group['members'], tree['nodes'][index]['members'], 'tree-group-members')
        need(receiver not in group['members'], 'tree-partition-self')
        positives = [j for j in group['members'] if weights[j][1] > 0]
        need(len(positives) >= 2, 'tree-two-positive-minimum')
        exact(group['positiveMembers'], positives, 'tree-positive-members')
        amount = sum((weights[j][1] for j in group['members']), Fraction(0))
        need(rational(group['massUpper']) == amount, 'tree-group-upper-mass')
        used += amount
        need(used <= budget, 'tree-cumulative-budget')
        covered.extend(group['members'])
    covered.extend(saved['fallback'])
    need(all(type(j) is int for j in covered), 'tree-partition-integer')
    need(receiver not in covered, 'tree-partition-self')
    need(len(covered) == len(set(covered)), 'tree-partition-duplicate')
    need(set(covered) == set(weights), 'tree-source-partition')
    need(used == declared, 'tree-selected-mass-total')
    expected = selection(tree, receiver, weights, budget)
    exact(saved['selected'], expected['selected'], 'tree-left-first-selection')
    exact(saved['fallback'], expected['fallback'], 'tree-left-first-fallback')
    for key in ('positiveCovered', 'selectedMembers', 'nodeVisits'):
        exact(saved[key], expected[key], 'tree-' + key)
    return expected


def check_tier(saved, tier_index, receiver, weights, trees):
    fields(saved, ('tier', 'budget', 'ceilingCount', 'ceilingMembers', 'ceilingLowerMass',
                  'singletonFeasibleCount', 'singletonFeasibleMembers', 'singletonUpperMass', 'trees'), 'tier-shape')
    budget = BUDGETS[tier_index]
    exact(saved['tier'], TIERS[tier_index], 'tier-order')
    need(rational(saved['budget']) == budget, 'tier-budget')
    lower_members, lower_mass = prefix(weights, 0, budget)
    upper_members, upper_mass = prefix(weights, 1, budget)
    exact(saved['ceilingCount'], len(lower_members), 'prefix-ceiling-count')
    exact(saved['ceilingMembers'], lower_members, 'prefix-ceiling-members')
    need(rational(saved['ceilingLowerMass']) == lower_mass, 'prefix-ceiling-lower-mass')
    exact(saved['singletonFeasibleCount'], len(upper_members), 'prefix-feasible-count')
    exact(saved['singletonFeasibleMembers'], upper_members, 'prefix-feasible-members')
    need(rational(saved['singletonUpperMass']) == upper_mass, 'prefix-feasible-upper-mass')
    fields(saved['trees'], ('T8', 'T2'), 'tier-trees')
    for key in ('T8', 'T2'):
        check_selection(saved['trees'][key], trees[key], receiver, weights, budget)


def check_identity(saved, name, digest):
    exact(saved['id'], name, 'state-identity')
    exact(saved['inputSha256'], digest, 'state-input-binding')


def check_denominator(saved, positive):
    exact(saved['positiveTerms'], positive, 'positive-denominator')


def check_trees(saved, expected):
    fields(saved, ('T8', 'T2'), 'state-trees')
    for key in ('T8', 'T2'):
        exact(saved[key], expected[key], key + '-structure')
    nesting(saved['T8'], saved['T2'])


def source_context(name, inp, reference, baseline):
    need(type(inp) is dict and type(inp.get('drones')) is list and len(inp['drones']) == 64, 'input-drone-count')
    ids, centers = [], {}
    for drone in inp['drones']:
        need(type(drone) is dict and type(drone.get('id')) is int, 'input-stable-id')
        identifier = drone['id']
        need(identifier not in centers, 'input-duplicate-id')
        need(type(drone.get('state')) is list and len(drone['state']) >= 3, 'input-state')
        ids.append(identifier)
        centers[identifier] = tuple(dyadic(word) for word in drone['state'][:3])
    need(reference['schema'] == 'm31-normalizer-ablation-reference-v1', 'reference-schema')
    need(reference['id'] == name and reference['referenceStatus'] == 'admitted', 'reference-admission')
    digest = canonical_input_hash(name, inp)
    exact(reference['inputSha256'], digest, 'reference-input-binding')
    need(baseline['id'] == name and baseline['kind'] == 'scheduled' and baseline['arm'] == 'baseline'
         and type(baseline['repetition']) is int and baseline['repetition'] == 0 and baseline['error'] is None,
         'baseline-identity')
    exact(baseline['input'], inp, 'baseline-input-binding')
    need(baseline['method']['result']['status'] == 'certified', 'baseline-certification')
    need(type(reference['prepared']) is list and len(reference['prepared']) == 64, 'prepared-count')
    prepared = {}
    for entry in reference['prepared']:
        identifier = entry['id']
        need(type(identifier) is int and identifier in centers and identifier not in prepared, 'prepared-domain')
        need(entry['rejection'] is None, 'prepared-admission')
        prepared[identifier] = entry
    for drone in inp['drones']:
        exact(prepared[drone['id']]['value']['center'], drone['state'][:3], 'prepared-center-binding')
    trees = {key: reconstruct(ids, centers, capacity) for key, capacity in (('T8', 8), ('T2', 2))}
    old_tree = baseline['method']['assembly']['tree']
    need(type(old_tree) is dict, 'baseline-tree-present')
    exact(old_tree['permutation'], trees['T8']['permutation'], 'T8-baseline-permutation')
    need(type(old_tree['nodes']) is list and len(old_tree['nodes']) == len(trees['T8']['nodes']), 'T8-baseline-size')
    for old, new in zip(old_tree['nodes'], trees['T8']['nodes']):
        exact({key: old[key] for key in ('id', 'start', 'end', 'left', 'right')},
              {key: new[key] for key in ('id', 'start', 'end', 'left', 'right')}, 'T8-baseline-structure')
    need(type(reference['pairs']) is list and len(reference['pairs']) == 16128, 'pair-list-count')
    weights = {(i, rotor): {} for i in ids for rotor in range(4)}
    positive = 0
    for pair in reference['pairs']:
        i, rotor, j = pair['i'], pair['r'], pair['j']
        need(type(i) is int and type(j) is int and type(rotor) is int and
             i in centers and j in centers and i != j and 0 <= rotor < 4, 'pair-domain')
        row = weights[i, rotor]
        need(j not in row, 'pair-duplicate')
        if pair['status'] == 'zero':
            need('coefficient' not in pair, 'zero-coefficient')
            interval = (Fraction(0), Fraction(0))
        else:
            need(pair['status'] == 'positive', 'pair-status')
            fields(pair['coefficient'], ('l', 'u'), 'coefficient-shape')
            interval = (endpoint(pair['coefficient']['l']), endpoint(pair['coefficient']['u']))
            need(0 <= interval[0] <= interval[1] and interval[1] > 0, 'positive-interval')
            positive += 1
        row[j] = interval
    domain = set(ids)
    need(all(set(row) == domain - {i} for (i, _), row in weights.items()), 'pair-completeness')
    exact(reference['evaluatedPairs'], 16128, 'evaluated-pair-count')
    exact(reference['plannedPairs'], 16128, 'planned-pair-count')
    exact(reference['graph']['positiveRotorPairs'], positive, 'reference-positive-denominator')
    return {'name': name, 'digest': digest, 'ids': ids, 'trees': trees, 'weights': weights, 'positive': positive}


def hurdle(covered, denominator):
    return denominator > 0 and covered * 10 >= denominator


def summaries(rows, denominator):
    result = []
    for index, tier in enumerate(TIERS):
        parts = [row['tiers'][index] for row in rows]
        ceiling = sum(part['ceilingCount'] for part in parts)
        item = {'tier': tier, 'positiveTerms': denominator, 'optimisticCeiling': ceiling,
                'singletonFeasible': sum(part['singletonFeasibleCount'] for part in parts),
                'trees': {}, 'ceilingTenPercentHurdle': hurdle(ceiling, denominator)}
        for key in ('T8', 'T2'):
            selections = [part['trees'][key] for part in parts]
            covered = sum(part['positiveCovered'] for part in selections)
            item['trees'][key] = {'positiveCovered': covered, 'groups': sum(len(part['selected']) for part in selections),
                'rowsCovered': sum(bool(part['selected']) for part in selections),
                'membersCovered': sum(part['selectedMembers'] for part in selections),
                'nodeVisits': sum(part['nodeVisits'] for part in selections),
                'tenPercentCountHurdle': hurdle(covered, denominator)}
        result.append(item)
    return result


def check_state(saved, context):
    fields(saved, ('id', 'inputSha256', 'trees', 'rows', 'positiveTerms', 'summary'), 'state-shape')
    check_identity(saved, context['name'], context['digest'])
    check_denominator(saved, context['positive'])
    check_trees(saved['trees'], context['trees'])
    need(type(saved['rows']) is list and len(saved['rows']) == 256, 'state-row-count')
    for index, row in enumerate(saved['rows']):
        fields(row, ('i', 'r', 'positiveTerms', 'tiers'), 'row-shape')
        receiver, rotor = context['ids'][index // 4], index % 4
        exact(row['i'], receiver, 'row-receiver-order')
        exact(row['r'], rotor, 'row-rotor-order')
        weights = context['weights'][receiver, rotor]
        exact(row['positiveTerms'], sum(upper > 0 for lower, upper in weights.values()), 'row-positive-denominator')
        need(type(row['tiers']) is list and len(row['tiers']) == 3, 'row-tier-count')
        for tier_index, tier in enumerate(row['tiers']):
            check_tier(tier, tier_index, receiver, weights, context['trees'])
    expected = summaries(saved['rows'], context['positive'])
    exact(saved['summary'], expected, 'summary-counts-and-hurdles')
    return expected


def fixed_fixtures(log):
    def case(name, condition):
        log.append({'name': name, 'passed': bool(condition)})
        need(condition, 'fixed-fixture:' + name)

    def rejects(function, expected):
        try:
            function()
        except CheckError as exc:
            return str(exc) == expected
        return False

    case('reduced-rational-arithmetic', rational('1/3') + rational('1/6') == Fraction(1, 2))
    case('noncanonical-and-invalid-rationals', all(rejects(lambda s=s: rational(s), 'rational-normalization')
         for s in ('2/4', '-0/1', '01/2', '1/0', '1/-2')))
    case('noncanonical-reference-endpoint', rejects(lambda: endpoint({'n': '2', 'd': '4'}), 'endpoint-normalization'))
    case('exact-tier-budget', BUDGETS == tuple(Fraction(tier) / 16 for tier in TIERS))
    case('integer-binary64-decoding', dyadic('3ff0000000000000') == 1 and dyadic('bfe0000000000000') == -Fraction(1, 2)
         and dyadic('0000000000000001') == Fraction(1, 1 << 1074) and dyadic('8000000000000000') == 0)
    case('binary64-infinity-rejected', rejects(lambda: dyadic('7ff0000000000000'), 'center-nonfinite'))
    weights = {4: (Fraction(3, 10), Fraction(1, 2)), 2: (Fraction(1, 10), Fraction(1, 5)),
               3: (Fraction(1, 5), Fraction(1, 4)), 1: (Fraction(1, 10), Fraction(1, 5))}
    case('lower-prefix-ties-and-maximality', prefix(weights, 0, Fraction(3, 10)) == ([1, 2], Fraction(1, 5)))
    case('upper-prefix-feasibility', prefix(weights, 1, Fraction(3, 10)) == ([1], Fraction(1, 5)))
    case('zero-lower-positive-retained', prefix({19: (Fraction(0), Fraction(1))}, 0, Fraction(0)) == ([19], Fraction(0)))
    case('zero-positive-prefix', prefix({19: (Fraction(0), Fraction(0))}, 0, Fraction(1)) == ([], Fraction(0)))
    centers = {i: (Fraction(i), Fraction(0), Fraction(0)) for i in range(16)}
    tree = reconstruct(list(range(8)), centers, 2)
    case('preorder-split-topology', [(n['id'], n['left'], n['right'], n['members']) for n in tree['nodes']] ==
         [(0, 1, 4, list(range(8))), (1, 2, 3, list(range(4))), (2, None, None, [0, 1]),
          (3, None, None, [2, 3]), (4, 5, 6, [4, 5, 6, 7]), (5, None, None, [4, 5]), (6, None, None, [6, 7])])
    weights = {i: (Fraction(1, 20), Fraction(1, 20)) for i in range(1, 8)}
    got = selection(tree, 0, weights, Fraction(3, 20))
    case('left-first-cumulative-selection', [part['node'] for part in got['selected']] == [3]
         and got['fallback'] == [1, 4, 5, 6, 7] and got['nodeVisits'] == 7 and got['usedUpper'] == '1/10')
    got = selection(tree, 0, weights, Fraction(1, 5))
    case('budget-equality-and-parent-rejection', [part['node'] for part in got['selected']] == [3, 5]
         and got['fallback'] == [1, 6, 7] and got['usedUpper'] == '1/5')
    check_selection(got, tree, 0, weights, Fraction(1, 5))
    excessive = copy.deepcopy(got)
    excessive['selected'].append({'node': 6, 'members': [6, 7], 'positiveMembers': [6, 7], 'massUpper': '1/10'})
    excessive['fallback'] = [1]
    case('actual-cumulative-overspend-rejected', rejects(lambda: check_selection(excessive, tree, 0, weights, Fraction(1, 5)), 'tree-cumulative-budget'))
    sparse = {i: (Fraction(0), Fraction(1) if i == 2 else Fraction(0)) for i in range(1, 8)}
    case('two-positive-members-required', not selection(tree, 0, sparse, Fraction(100))['selected'])
    nesting(reconstruct(list(range(16)), centers, 8), reconstruct(list(range(16)), centers, 2))
    case('T8-T2-member-set-nesting', True)
    tie_centers = {9: (Fraction(1), Fraction(0), Fraction(0)), 2: (Fraction(0), Fraction(1), Fraction(0))}
    case('axis-tie-x-first-and-stable-ids', reconstruct([9, 2], tie_centers, 1)['permutation'] == [2, 9]
         and reconstruct([9, 2], {9: (0, 0, 0), 2: (0, 0, 0)}, 1)['permutation'] == [2, 9])
    case('leaf-preserves-incoming-order', reconstruct([9, 2], tie_centers, 8)['permutation'] == [9, 2])
    case('zero-denominator-never-passes', hurdle(0, 0) is False and hurdle(1, 10) is True and hurdle(1, 11) is False)


def corruption_controls(saved, context, log):
    """Each case starts from a fresh in-memory copy of verified saved data."""
    receiver = context['ids'][0]
    weights = context['weights'][receiver, 0]
    trees, budget = context['trees'], BUDGETS[0]
    tier = saved['rows'][0]['tiers'][0]
    tree_selection = tier['trees']['T8']

    def control(name, original, mutate, validate, expected):
        clone = copy.deepcopy(original)
        mutate(clone)
        actual = None
        try:
            validate(clone)
        except CheckError as exc:
            actual = str(exc)
        entry = {'name': name, 'expectedFailure': expected, 'actualFailure': actual,
                 'rejected': actual is not None, 'intendedCoreFailure': actual == expected}
        log.append(entry)
        need(entry['intendedCoreFailure'], 'corruption-control:' + name)

    validate_tier = lambda value: check_tier(value, 0, receiver, weights, trees)
    validate_tree = lambda value: check_selection(value, trees['T8'], receiver, weights, budget)
    control('overstated-ceiling', tier, lambda value: value.__setitem__('ceilingCount', value['ceilingCount'] + 1), validate_tier, 'prefix-ceiling-count')
    control('overstated-feasible-singletons', tier, lambda value: value.__setitem__('singletonFeasibleCount', value['singletonFeasibleCount'] + 1), validate_tier, 'prefix-feasible-count')
    control('incorrect-ceiling-members', tier, lambda value: value['ceilingMembers'].append(next(iter(weights))), validate_tier, 'prefix-ceiling-members')
    need(bool(tree_selection['fallback']), 'control-fallback-witness')
    control('duplicate-source', tree_selection, lambda value: value['fallback'].append(value['fallback'][0]), validate_tree, 'tree-partition-duplicate')
    control('self-source', tree_selection, lambda value: value['fallback'].append(receiver), validate_tree, 'tree-partition-self')
    control('missing-source', tree_selection, lambda value: value['fallback'].pop(), validate_tree, 'tree-source-partition')
    declared = rational(tree_selection['usedUpper'])
    wrong_mass = declared / 2 if declared > 0 else budget / 2
    control('incorrect-upper-mass-total', tree_selection, lambda value: value.__setitem__('usedUpper', wire(wrong_mass)), validate_tree, 'tree-selected-mass-total')
    control('exceeded-cumulative-budget', tree_selection, lambda value: value.__setitem__('usedUpper', wire(budget + 1)), validate_tree, 'tree-cumulative-budget')
    control('incorrect-tree-visits', tree_selection, lambda value: value.__setitem__('nodeVisits', value['nodeVisits'] + 1), validate_tree, 'tree-nodeVisits')
    control('altered-state-identity', {'id': saved['id'], 'inputSha256': saved['inputSha256']},
            lambda value: value.__setitem__('id', STATES[1]), lambda value: check_identity(value, context['name'], context['digest']), 'state-identity')
    control('altered-input-binding', {'id': saved['id'], 'inputSha256': saved['inputSha256']},
            lambda value: value.__setitem__('inputSha256', 'invalid'), lambda value: check_identity(value, context['name'], context['digest']), 'state-input-binding')
    control('altered-positive-denominator', {'positiveTerms': saved['positiveTerms']},
            lambda value: value.__setitem__('positiveTerms', value['positiveTerms'] + 1), lambda value: check_denominator(value, context['positive']), 'positive-denominator')
    control('altered-T8-child', saved['trees'],
            lambda value: value['T8']['nodes'][0].__setitem__('left', value['T8']['nodes'][0]['right']),
            lambda value: check_trees(value, trees), 'T8-structure')
    control('flipped-ten-percent-hurdle', saved['summary'],
            lambda value: value[0].__setitem__('ceilingTenPercentHurdle', not value[0]['ceilingTenPercentHurdle']),
            lambda value: exact(value, summaries(saved['rows'], context['positive']), 'summary-counts-and-hurdles'), 'summary-counts-and-hurdles')


def run(root):
    report = {'schema': 'm31-oracle-omission-independent-check-v1', 'passed': False,
              'firstFailure': None, 'fixtures': [], 'corruptionControls': [], 'inputPins': [],
              'verified': {'states': 0, 'rows': 0, 'tiers': 0, 'treeSelections': 0, 'referencePairs': 0},
              'outcomes': [], 'scope': SCOPE,
              'limitations': ['Saved reference coefficient intervals are trusted inputs, not recomputed physics.',
                  'No executable conservative bound, load-error guarantee, runtime saving, or physical-validity claim.',
                  'Count hurdles use each complete state denominator; a zero denominator never passes.',
                  'Observed file hashes bind this audit; the runner supplies frozen-source and analysis-attempt binding.']}
    stage = 'fixed-fixtures-before-target-reads'
    try:
        fixed_fixtures(report['fixtures'])
        root = Path(root).resolve()
        stage = 'saved-analyzer-output'
        document = load(root, PACKAGE + '/results/analyze.json', report['inputPins'])
        fields(document, ('schema', 'scope', 'tiers', 'fixtures', 'states'), 'analysis-shape')
        exact(document['schema'], 'm31-oracle-omission-screen-v1', 'analysis-schema')
        exact(document['scope'], SCOPE, 'analysis-scope')
        exact(document['tiers'], list(TIERS), 'analysis-tiers')
        exact(document['fixtures'], [{'name': name, 'passed': True} for name in ANALYZER_FIXTURES], 'analyzer-fixture-roster')
        need(type(document['states']) is list and len(document['states']) == 6, 'six-states-required')
        first_context = None
        for index, name in enumerate(STATES):
            stage = name
            inp = load(root, PRIOR + '/inputs/' + name + '.json', report['inputPins'])
            reference = load(root, PRIOR + '/reference/' + name + '.json', report['inputPins'])
            baseline = load(root, PRIOR + '/calls/' + name + '-baseline-r0.json', report['inputPins'])
            context = source_context(name, inp, reference, baseline)
            result = check_state(document['states'][index], context)
            report['outcomes'].append({'id': name, 'verified': True, 'positiveTerms': context['positive'], 'summary': result})
            for key, increment in (('states', 1), ('rows', 256), ('tiers', 768), ('treeSelections', 1536), ('referencePairs', 16128)):
                report['verified'][key] += increment
            if index == 0:
                first_context = context
            del inp, reference, baseline, context
        stage = 'saved-record-corruption-controls'
        corruption_controls(document['states'][0], first_context, report['corruptionControls'])
        exact(report['verified'], {'states': 6, 'rows': 1536, 'tiers': 4608, 'treeSelections': 9216, 'referencePairs': 96768}, 'complete-verification-counts')
        report['passed'] = True
    except Exception as exc:
        # One failure is retained, and processing stops.  No repair, retry or rerun.
        report['firstFailure'] = {'stage': stage, 'type': type(exc).__name__,
                                  'code': str(exc)[:256] if isinstance(exc, CheckError) else 'checker-internal:' + type(exc).__name__}
    return report
