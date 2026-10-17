"""Tree-first independent exact scene dispatch; no scientific import at load.

The caller supplies the byte-verified, frozen pair and semantic modules after
its publication/runtime/allocation gates.  Only traversal and coverage change;
each residual scalar query calls the unchanged independent 192-bit oracle.
"""

import re


SCHEMA = 'm31-tree-first-reference-scene-v1'
COVERAGE_SCHEMA = 'm31-tree-first-coverage-v1'
MAX_DRONES = 180
PAIR_SOURCE = 'research/m31-native-fresh-transfer-2026-10-17/source/pair-reference.py'
PAIR_SHA256 = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
SEMANTIC_SOURCE = 'research/m31-native-fresh-transfer-2026-10-17/source/semantic-reference.py'
SEMANTIC_SHA256 = 'ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'


def regenerate_scene(scene, spec, constant_bits, helper, semantic, guard=None):
    """Return an in-memory exact target with compact coverage.

    ``helper`` may be the existing RawWordHelper adapter; ``semantic`` is the
    frozen semantic-reference module.  ``guard`` is an optional administrative
    poll, not a source of scientific decisions.  Its exceptions propagate.
    The target's ``pairs`` contains evaluated scalars only, in original input
    receiver/rotor/source order.  No full pair lookup or post-hoc plan is built.
    """
    require = semantic.require
    require(guard is None or callable(guard), 'tree-reference-guard')
    poll = guard if guard is not None else lambda: None
    poll()
    require(type(spec.get('maxDrones')) is int and 1 <= spec['maxDrones'] <= MAX_DRONES,
            'tree-reference-spec-cap')
    require(spec.get('leafCapacity') == 8, 'tree-reference-leaf-capacity')
    require(spec.get('referenceCoefficientBits') == 192
            and spec.get('referenceSourceBits') == 192
            and spec.get('referenceRootBisections') == 128
            and spec.get('positiveTermCap') == 2000000, 'tree-reference-recipe')

    constants = {name: helper.dyadic(value) for name, value in constant_bits.items()}
    semantic.fields(scene, ('id', 'family', 'expectedClass', 'drones'), 'spec-scene-fields')
    name = scene['id']
    require(isinstance(name, str) and re.fullmatch(r'[a-z][a-z0-9-]{0,63}', name),
            'spec-scene-id')
    drones = scene['drones']
    require(isinstance(drones, list) and 1 <= len(drones) <= spec['maxDrones'],
            'spec-drone-count')
    inputs, prepared, ids, exact, geometry = [], [], [], {}, []
    # The entire inherited preparation pass precedes global invalidity selection.
    for drone in drones:
        poll()
        semantic.fields(drone, ('id', 'state'), 'spec-drone-fields')
        identifier = semantic.integer(drone['id'], 0, 65535, 'spec-stable-id')
        require(identifier not in ids, 'spec-duplicate-id')
        ids.append(identifier)
        state = semantic.sequence(drone['state'], 17, 'spec-raw-state-count')
        require(all(isinstance(v, str) and len(v) <= 128 for v in state), 'spec-raw-literal')
        raw = tuple(helper.literal(v) for v in state)
        inputs.append({'id': identifier, 'state': [helper.hex_bits(v) for v in raw]})
        value, rejection = None, None
        if not all(helper.finite(v) for v in raw):
            rejection = 'raw-nonfinite'
        elif not all(helper.dyadic(v) > 0 for v in raw[13:17]):
            rejection = 'raw-force'
        else:
            value = helper.prepare_one(raw, constant_bits, spec['corners'])
            if not helper.preparation_valid(raw, value, constants):
                rejection = 'preparation'
            else:
                exact[identifier] = semantic.prepared_exact(value, helper)
        prepared.append({'id': identifier, 'value': value, 'rejection': rejection})

    n = len(ids)
    planned = 4 * n * (n - 1)
    work = {key: 0 for key in semantic.WORK_FIELDS}
    work['preparationCalls'] = n
    target = {'schema': SCHEMA, 'id': name, 'input': {'drones': inputs},
              'prepared': prepared, 'exact': exact, 'geometry': geometry,
              'planned': planned, 'pairs': [], 'order': [],
              'expectedClass': scene['expectedClass'], 'tree': None,
              'globalGuard': None, 'guardEvidence': None}
    coverage = {'schema': COVERAGE_SCHEMA, 'mode': None, 'complete': False,
                'logicalPairs': planned, 'requiredCoveredPairs': None,
                'coveredPairs': 0, 'permutation': [], 'queries': [], 'work': work}
    target['coverage'] = coverage
    first_bad = next((row for row in prepared if row['rejection'] is not None), None)
    target['globalInvalid'] = first_bad is not None
    if first_bad is not None:
        target.update(status='rejected', branch=first_bad['rejection'],
                      witness={'id': first_bad['id']})
        coverage.update(mode='global-preparation', requiredCoveredPairs=0, complete=True)
    else:
        for item in prepared:
            value = item['value']
            geometry.append({'center': helper.exact_vector(value['center']),
                             'axis': helper.exact_vector(value['axis']),
                             'points': [helper.exact_vector(p) for p in value['points']]})
        poll()
        target['globalGuard'], target['guardEvidence'] = semantic.global_guard(geometry)
        work['globalProofs'] = 1
        boxes = None
        if target['globalGuard']['passed']:
            # The inherited builder computes bounds/membership once.  Do not
            # retain or expand its membership tuples during query traversal.
            tree, members, boxes = semantic.reconstruct_tree(geometry, ids)
            del members
            target['tree'] = tree
            permutation = tree['permutation']
            work['treeNodes'] = len(tree['nodes'])
            mode = 'hierarchy'
        else:
            tree = None
            permutation = list(ids)
            mode = 'fallback'
        require(len(permutation) == n and set(permutation) == set(ids),
                'tree-reference-permutation')
        id_to_index = {identifier: index for index, identifier in enumerate(ids)}
        inverse = {identifier: position for position, identifier in enumerate(permutation)}
        coverage.update(mode=mode, permutation=permutation, requiredCoveredPairs=planned)
        order_indices = sorted(range(n), key=lambda i: (-geometry[i]['center'][2], ids[i]))
        target['order'] = [ids[i] for i in order_indices]
        ranks = {identifier: index for index, identifier in enumerate(target['order'])}

        for receiver in range(n):
            for rotor in range(4):
                poll()
                self_position = inverse[ids[receiver]]
                query = {'i': receiver, 'id': ids[receiver], 'r': rotor,
                         'selfPosition': self_position, 'terminals': []}
                cursor, accounted = 0, 0

                def add_terminal(terminal):
                    nonlocal cursor, accounted
                    start, end = terminal['start'], terminal['end']
                    require(type(start) is int and type(end) is int
                            and start == cursor and start < end <= n,
                            'tree-reference-terminal-partition')
                    count = end - start - int(start <= self_position < end)
                    require(terminal['count'] == count, 'tree-reference-terminal-count')
                    cursor, accounted = end, accounted + count
                    query['terminals'].append(terminal)

                def scan(start, end, node_id):
                    # Only actually evaluated scalar members are enumerated.
                    sources = sorted(id_to_index[permutation[position]]
                                     for position in range(start, end)
                                     if position != self_position)
                    terminal = {'kind': 'scan' if node_id is None else 'leaf',
                                'node': node_id, 'start': start, 'end': end,
                                'count': len(sources), 'sourceIndices': sources}
                    if node_id is not None:
                        work['leafVisits'] += 1
                    for source in sources:
                        poll()
                        oracle_full = helper.oracle_case(
                            {'id': name, 'input': {'receiver': inputs[receiver]['state'],
                             'source': inputs[source]['state'], 'self': False, 'rotor': rotor}},
                            constant_bits, spec['corners'])
                        oracle = {'status': oracle_full['status'], 'branch': oracle_full['branch']}
                        counters = {'zero': 'scalarZeroPairs', 'positive': 'positiveTerms',
                                    'rejected': 'rejectedPairs',
                                    'reference-undecidable': 'unresolvedPairs'}
                        require(oracle['status'] in counters, 'tree-reference-oracle-status')
                        work['scalarPairs'] += 1
                        work[counters[oracle['status']]] += 1
                        pair = {'i': ids[receiver], 'r': rotor, 'j': ids[source],
                                'ii': receiver, 'jj': source, 'oracle': oracle}
                        if oracle['status'] == 'positive':
                            pair['coefficient'] = semantic.quantize(
                                oracle_full['referenceIntervals']['coefficient'], 192)
                        target['pairs'].append(pair)
                    add_terminal(terminal)

                def visit(node_id):
                    poll()
                    node = tree['nodes'][node_id]
                    work['nodeVisits'] += 1
                    rule, tests = semantic.zero_rule(boxes[node_id], geometry[receiver],
                                                     rotor, constants)
                    work['nodeRuleTests'] += tests
                    if rule is not None:
                        require(rule in semantic.RULES, 'tree-reference-zero-rule')
                        start, end = node['start'], node['end']
                        # Constant-size range arithmetic: never inspect or emit
                        # individual members of a proved-zero terminal.
                        count = end - start - int(start <= self_position < end)
                        add_terminal({'kind': 'zero', 'node': node_id, 'start': start,
                                      'end': end, 'count': count, 'proofRule': rule})
                        work['zeroNodes'] += 1
                        work['zeroPairs'] += count
                    elif node['left'] is None:
                        scan(node['start'], node['end'], node_id)
                    else:
                        visit(node['left'])
                        visit(node['right'])

                if tree is None:
                    scan(0, n, None)
                else:
                    visit(0)
                require(cursor == n and accounted == n - 1,
                        'tree-reference-query-coverage')
                coverage['coveredPairs'] += accounted
                coverage['queries'].append(query)

        require(coverage['coveredPairs'] == planned
                and work['zeroPairs'] + work['scalarPairs'] == planned
                and len(target['pairs']) == work['scalarPairs'], 'tree-reference-coverage')
        coverage['complete'] = True
        # Spatial traversal changes visitation order, never canonical scientific
        # precedence or source order in root/load arithmetic.
        target['pairs'].sort(key=lambda pair: (pair['ii'], pair['r'], pair['jj']))
        rejected = next((p for p in target['pairs'] if p['oracle']['status'] == 'rejected'), None)
        uncertain = next((p for p in target['pairs']
                          if p['oracle']['status'] == 'reference-undecidable'), None)
        wrong = next((p for p in target['pairs'] if p['oracle']['status'] == 'positive'
                      and ranks[p['j']] >= ranks[p['i']]), None)
        if rejected is not None:
            target.update(status='rejected', branch='pair-' + rejected['oracle']['branch'],
                          witness={k: rejected[k] for k in ('i', 'r', 'j')})
        elif uncertain is not None:
            target.update(status='reference-undecidable',
                          branch='pair-' + uncertain['oracle']['branch'],
                          witness={k: uncertain[k] for k in ('i', 'r', 'j')})
        elif wrong is not None:
            target.update(status='rejected', branch='ordering',
                          witness={k: wrong[k] for k in ('i', 'r', 'j')})
        elif work['positiveTerms'] > spec['positiveTermCap']:
            target.update(status='resource', branch='positive-term-budget', witness=None)
        else:
            poll()
            target.update(status='admitted', branch='loads', witness=None)
            target['roots'], target['loads'] = semantic.reference_roots(target)
            poll()
    target['referenceClass'] = ('admitted' if target['status'] == 'admitted' else
                                target['status'] + ':' + target['branch'])
    return target


def to_record(target, semantic):
    """JSON-ready scene evidence; serialization does not evaluate any oracle."""
    pairs = []
    for pair in target['pairs']:
        row = {k: pair[k] for k in ('i', 'r', 'j', 'ii', 'jj')}
        row.update(pair['oracle'])
        if 'coefficient' in pair:
            row['coefficient'] = semantic.interval_wire(pair['coefficient'])
        pairs.append(row)
    loads = []
    if target['status'] == 'admitted':
        for drone in target['input']['drones']:
            identifier = drone['id']
            loads.append({'id': identifier,
                          'roots': [semantic.interval_wire(target['roots'][(identifier, r)])
                                    for r in range(4)],
                          'loads': {k: semantic.interval_wire(v) if k == 'collective' else
                                    [semantic.interval_wire(x) for x in v]
                                    for k, v in target['loads'][identifier].items()}})
    guard_evidence = target['guardEvidence']
    if guard_evidence is not None:
        guard_evidence = {group: {k: semantic.fraction_wire(v) for k, v in values.items()}
                          for group, values in guard_evidence.items()}
    return {'schema': SCHEMA, 'id': target['id'], 'input': target['input'],
            'prepared': target['prepared'], 'expectedClass': target['expectedClass'],
            'referenceStatus': target['status'], 'branch': target['branch'],
            'witness': target['witness'], 'referenceClass': target['referenceClass'],
            'globalInvalid': target['globalInvalid'], 'globalGuard': target['globalGuard'],
            'guardEvidence': guard_evidence, 'order': target['order'],
            'plannedPairs': target['planned'], 'evaluatedPairs': len(pairs),
            'pairs': pairs, 'tree': target['tree'], 'coverage': target['coverage'],
            'loads': loads, 'recipe': {'coefficientBits': 192, 'sourceBits': 192,
                                      'rootBisections': 128}}
