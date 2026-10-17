"""Six prebound coverage corruptions; no scientific imports or execution at load.

The driver first validates the untouched full/tree pair, then calls run_bound
once per fixed scene. All witness lookups use literal keys selected from saved
evidence before publication. Missing witnesses and repeated controls fail; no
alternative source, terminal, scene, seed or corruption is selected at runtime.
"""
from copy import deepcopy


CONTROL_IDS = (
    'positive-falsely-zero',
    'dropped-source',
    'duplicate-plus-omission-equal-count',
    'forged-node-bound',
    'guard-bypass-zero',
    'index-id-swap',
)
_EXECUTED = set()
_DENSE_MEMBERS = [1, 3, 9, 10, 18]
_PERMUTED_IDS = [100, 102, 104, 106, 108, 110, 112, 114, 116,
                 118, 120, 122, 124, 126, 101, 103, 105, 107,
                 109, 111, 113, 115, 117, 119, 121, 123, 125]


class BoundWitnessError(Exception):
    pass


def _need(condition, code):
    if not condition:
        raise BoundWitnessError(code)


def _key(pair):
    return pair['ii'], pair['r'], pair['jj']


def _positions(target):
    # Index existing records by identity; never search for a favorable witness.
    result = {_key(pair): index for index, pair in enumerate(target['pairs'])}
    _need(len(result) == len(target['pairs']), 'bound-baseline-duplicate-pairs')
    return result


def _pair(full, tree, positions, key, receiver_id, source_id, status, branch=None):
    _need(key in full['lookup'] and key in positions, 'bound-fixed-pair-missing')
    old, candidate = full['lookup'][key], tree['pairs'][positions[key]]
    _need(_key(old) == key and _key(candidate) == key, 'bound-fixed-pair-index')
    _need(old['i'] == candidate['i'] == receiver_id
          and old['j'] == candidate['j'] == source_id, 'bound-fixed-pair-id')
    _need(old['oracle'] == candidate['oracle']
          and old['oracle']['status'] == status, 'bound-fixed-pair-status')
    _need(branch is None or old['oracle']['branch'] == branch, 'bound-fixed-pair-branch')
    _need(old.get('coefficient') == candidate.get('coefficient'), 'bound-fixed-coefficient')
    return candidate


def _wire_pair(pair, semantic):
    result = {field: deepcopy(pair[field]) for field in ('ii', 'r', 'jj', 'i', 'j', 'oracle')}
    if 'coefficient' in pair:
        result['coefficient'] = semantic.interval_wire(pair['coefficient'])
    return result


def _field(path, before, after):
    _need(before != after, 'bound-mutation-did-not-change-field')
    return {'path': path, 'before': deepcopy(before), 'after': deepcopy(after)}


def _run(name, ordinal, full, candidate, validator, semantic, constants,
         required_failure, witness, changed_fields, description):
    _need(name in CONTROL_IDS and name not in _EXECUTED, 'bound-control-repeated')
    _need(bool(changed_fields), 'bound-mutation-empty')
    _EXECUTED.add(name)
    observed = None
    try:
        validator.validate(full, candidate, semantic, constants)
    except validator.ValidationError as error:
        observed = {'class': type(error).__name__, 'message': str(error)}
    # Administrative exceptions and other error types propagate to the driver;
    # they cannot count as an intended scientific rejection.
    detected = observed is not None and observed['message'] == required_failure
    return {'id': name, 'scene': full['id'], 'sceneOrdinal': ordinal,
            'executed': True, 'witnessPreconditionsPassed': True,
            'baselineValidatedByDriver': True, 'mutation': description,
            'witness': witness, 'changedFields': changed_fields,
            'requiredFailureFamilies': [required_failure],
            'observedException': observed, 'rejected': observed is not None,
            'intendedCoreFailure': detected, 'detected': detected}


def run_bound(case_id, full, tree, validator, semantic, constants):
    """Return four controls for dense, one permuted, one guard, otherwise [].

    Caller contract: the unchanged baseline has just passed validator.validate.
    The fixed 24-case driver invokes each relevant scene exactly once. This
    module additionally rejects a second invocation of any selected control.
    """
    if case_id not in ('dense-cube-27', 'permuted-cube-27', 'center-guard-fallback'):
        return []
    _need(full['id'] == tree['id'] == case_id, 'bound-scene-identity')
    positions = _positions(tree)
    results = []

    if case_id == 'dense-cube-27':
        _need([row['id'] for row in full['input']['drones']] == list(range(100, 127)),
              'bound-dense-id-order')
        query = tree['coverage']['queries'][0]
        terminal = query['terminals'][0]
        _need((query['i'], query['id'], query['r'], query['selfPosition']) == (0, 100, 0, 0),
              'bound-dense-query')
        _need(terminal == {'kind': 'leaf', 'node': 2, 'start': 0, 'end': 6,
                           'count': 5, 'sourceIndices': _DENSE_MEMBERS},
              'bound-dense-residual-leaf')
        _need(tree['coverage']['permutation'][:6] == [100, 101, 109, 110, 118, 103],
              'bound-dense-permutation-prefix')
        positive = _pair(full, tree, positions, (0, 0, 9), 100, 109, 'positive', 'active')
        _need(semantic.interval_wire(positive['coefficient']) == {
            'l': {'n': '2424107759519877893894402684079226642605509254943144211717',
                  'd': '3138550867693340381917894711603833208051177722232017256448'},
            'u': {'n': '1212053879759938946947201342039613321302754627471572105859',
                  'd': '1569275433846670190958947355801916604025588861116008628224'}},
              'bound-saved-positive-coefficient')
        _pair(full, tree, positions, (0, 0, 18), 100, 118, 'positive', 'active')
        for source in (1, 3, 10):
            _pair(full, tree, positions, (0, 0, source), 100, 100 + source, 'zero')

        # C1: complete range, false zero proof, two positive contributions hidden.
        candidate = deepcopy(tree)
        false_terminal = {'kind': 'zero', 'node': 2, 'start': 0, 'end': 6,
                          'count': 5, 'proofRule': 'neighbor'}
        candidate['coverage']['queries'][0]['terminals'][0] = false_terminal
        removed_keys = {(0, 0, source) for source in _DENSE_MEMBERS}
        removed = [_wire_pair(tree['pairs'][positions[key]], semantic)
                   for key in sorted(removed_keys)]
        candidate['pairs'] = [pair for pair in candidate['pairs'] if _key(pair) not in removed_keys]
        work_before = deepcopy(candidate['coverage']['work'])
        work = candidate['coverage']['work']
        for key, delta in (('scalarPairs', -5), ('scalarZeroPairs', -3),
                           ('positiveTerms', -2), ('zeroPairs', 5),
                           ('zeroNodes', 1), ('leafVisits', -1)):
            work[key] += delta
        results.append(_run(CONTROL_IDS[0], 1, full, candidate, validator, semantic, constants,
                            'node-proof-rule',
                            {'ii': 0, 'i': 100, 'r': 0, 'jj': 9, 'j': 109,
                             'permutationPosition': 2, 'node': 2, 'range': [0, 6],
                             'coefficient': semantic.interval_wire(positive['coefficient'])},
                            [_field('coverage/queries/0/terminals/0', terminal, false_terminal),
                             _field('pairs@keys=(0,0,[1,3,9,10,18])', removed, []),
                             _field('coverage/work', work_before, work)],
                            'Replace the fixed five-member leaf by a neighbor-zero range; remove its five scalar rows.'))

        # C2: retain required membership, omit its explicit scalar evaluation.
        candidate = deepcopy(tree)
        pair_index = positions[(0, 0, 1)]
        removed = _wire_pair(candidate['pairs'].pop(pair_index), semantic)
        work_before = deepcopy(candidate['coverage']['work'])
        candidate['coverage']['work']['scalarPairs'] -= 1
        candidate['coverage']['work']['scalarZeroPairs'] -= 1
        results.append(_run(CONTROL_IDS[1], 1, full, candidate, validator, semantic, constants,
                            'scalar-pair-canonical-membership',
                            {'ii': 0, 'i': 100, 'r': 0, 'jj': 1, 'j': 101,
                             'permutationPosition': 1, 'node': 2, 'range': [0, 6],
                             'requiredSourceIndices': _DENSE_MEMBERS},
                            [_field('pairs/' + str(pair_index), removed, None),
                             _field('coverage/work', work_before, candidate['coverage']['work'])],
                            'Delete the fixed zero scalar record while retaining its required leaf membership and count.'))

        # C3: duplicate an existing zero row over a different zero; same totals.
        candidate = deepcopy(tree)
        member_after = [3, 3, 9, 10, 18]
        candidate['coverage']['queries'][0]['terminals'][0]['sourceIndices'] = member_after
        destination, source = positions[(0, 0, 1)], positions[(0, 0, 3)]
        before = _wire_pair(candidate['pairs'][destination], semantic)
        candidate['pairs'][destination] = deepcopy(candidate['pairs'][source])
        after = _wire_pair(candidate['pairs'][destination], semantic)
        results.append(_run(CONTROL_IDS[2], 1, full, candidate, validator, semantic, constants,
                            'scalar-member-list',
                            {'ii': 0, 'i': 100, 'r': 0, 'omitted': {'jj': 1, 'j': 101, 'position': 1},
                             'duplicated': {'jj': 3, 'j': 103, 'position': 5},
                             'node': 2, 'range': [0, 6], 'countBeforeAndAfter': 5,
                             'pairArrayLengthBeforeAndAfter': len(tree['pairs'])},
                            [_field('coverage/queries/0/terminals/0/sourceIndices', _DENSE_MEMBERS, member_after),
                             _field('pairs/' + str(destination), before, after)],
                            'Replace source 101 by a duplicate of zero source 103 in both leaf membership and scalar rows; all totals stay fixed.'))

        # C4: a well-ordered point interval that excludes an actual member.
        lower = {'n': '1170935903116329', 'd': '9007199254740992'}
        upper = {'n': '8376695306909123', 'd': '9007199254740992'}
        _need(full['tree']['nodes'][0]['center'][0] == [lower, upper]
              and tree['tree']['nodes'][0]['center'][0] == [lower, upper], 'bound-root-x-box')
        candidate = deepcopy(tree)
        candidate['tree']['nodes'][0]['center'][0][0] = deepcopy(upper)
        results.append(_run(CONTROL_IDS[3], 1, full, candidate, validator, semantic, constants,
                            'tree-identity',
                            {'node': 0, 'coordinate': 0, 'excludedStableId': 100,
                             'excludedPreparedCoordinate': lower, 'newLower': upper},
                            [_field('tree/nodes/0/center/0/0', lower, upper)],
                            'Set root x lower bound to its genuine upper bound, excluding prepared center ID 100.'))

    elif case_id == 'center-guard-fallback':
        _need([row['id'] for row in full['input']['drones']] == [741, 742, 743],
              'bound-guard-id-order')
        _need(tree['coverage']['mode'] == 'fallback' and tree['tree'] is None
              and full['globalGuard']['passed'] is False
              and full['globalGuard']['checks']['centerComponent'] is False,
              'bound-failed-global-guard')
        _need(full['guardEvidence']['upper']['centerComponent'] == 258
              and full['guardEvidence']['limits']['centerComponent'] == 257,
              'bound-center-guard-evidence')
        _need((full['status'], full['branch'], full['witness'])
              == ('rejected', 'pair-center-guard', {'i': 741, 'r': 0, 'j': 742}),
              'bound-guard-canonical-failure')
        _pair(full, tree, positions, (0, 0, 1), 741, 742, 'rejected', 'center-guard')
        candidate = deepcopy(tree)
        pair_index = positions[(0, 0, 1)]
        before = deepcopy(candidate['pairs'][pair_index]['oracle'])
        after = {'status': 'zero', 'branch': 'neighbor'}
        candidate['pairs'][pair_index]['oracle'] = after
        work_before = deepcopy(candidate['coverage']['work'])
        candidate['coverage']['work']['rejectedPairs'] -= 1
        candidate['coverage']['work']['scalarZeroPairs'] += 1
        results.append(_run(CONTROL_IDS[4], 15, full, candidate, validator, semantic, constants,
                            'scalar-oracle',
                            {'ii': 0, 'i': 741, 'r': 0, 'jj': 1, 'j': 742,
                             'centerComponentUpper': 258, 'centerComponentLimit': 257,
                             'canonicalWitness': full['witness']},
                            [_field('pairs/' + str(pair_index) + '/oracle', before, after),
                             _field('coverage/work', work_before, candidate['coverage']['work'])],
                            'Change the fixed center-guard refusal to neighbor zero without dropping membership or forging the global guard.'))

    else:
        _need([row['id'] for row in full['input']['drones']] == _PERMUTED_IDS,
              'bound-permuted-id-order')
        first = _pair(full, tree, positions, (0, 0, 9), 100, 118, 'positive', 'active')
        second = _pair(full, tree, positions, (0, 0, 18), 100, 109, 'positive', 'active')
        _need(first['coefficient'] != second['coefficient'], 'bound-swapped-coefficients-distinct')
        _need(tree['coverage']['permutation'][4] == 118
              and tree['coverage']['permutation'][2] == 109, 'bound-swapped-permutation-positions')
        query = tree['coverage']['queries'][0]
        _need((query['i'], query['id'], query['r']) == (0, 100, 0)
              and query['terminals'][0]['kind'] == 'leaf'
              and query['terminals'][0]['node'] == 2
              and (query['terminals'][0]['start'], query['terminals'][0]['end']) == (0, 6),
              'bound-swapped-residual-leaf')
        candidate = deepcopy(tree)
        first_index, second_index = positions[(0, 0, 9)], positions[(0, 0, 18)]
        candidate['pairs'][first_index]['j'] = 109
        candidate['pairs'][second_index]['j'] = 118
        results.append(_run(CONTROL_IDS[5], 6, full, candidate, validator, semantic, constants,
                            'scalar-j',
                            {'ii': 0, 'i': 100, 'r': 0,
                             'first': {'jj': 9, 'j': 118, 'position': 4},
                             'second': {'jj': 18, 'j': 109, 'position': 2},
                             'bothStatuses': 'positive', 'bothBranches': 'active'},
                            [_field('pairs/' + str(first_index) + '/j', 118, 109),
                             _field('pairs/' + str(second_index) + '/j', 109, 118)],
                            'Swap two valid stable source IDs while retaining input indices, coefficients, membership and all counts.'))

    _need(len(results) == (4 if case_id == 'dense-cube-27' else 1), 'bound-control-count')
    return results
