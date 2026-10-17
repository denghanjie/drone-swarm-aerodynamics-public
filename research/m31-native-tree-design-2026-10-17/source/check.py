"""Saved native-tree certificate/equivalence audit. Source-only until supervised.

Only Python stdlib is imported. No producer, oracle, scientific helper, numerical
kernel or trajectory is executed. This checks finite saved records, not universal
runtime equivalence or independent exact-reference accuracy of native F.
"""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import copy
import hashlib
import json
import os
import re
import sys
import time

PACKAGE = 'research/m31-native-tree-design-2026-10-17'
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
HEX = re.compile(r'^[0-9a-f]{16}$')
METHODS = ('F', 'H0', 'H')
ZERO = '0000000000000000'
NEGZERO = '8000000000000000'
REGRESSION = {'path': 'research/m31-native-fresh-transfer-2026-10-17/results/inputs/fresh-a-t5.json',
              'bytes': 21955, 'sha256': '48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c'}
F_SOURCE = ('research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs',
            'b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1')
F_DEPENDENCIES = {
    'kernel.cjs': 'efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8',
    'anchor-kernel.cjs': 'c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a',
    'lean-anchor.cjs': '1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96',
    'reference-excerpt.cjs': 'ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e',
}
BOUNDARY = (('plus-inside', '400fffffffffffff', False),
            ('plus-equal', '4010000000000000', True),
            ('plus-outside', '4010000000000001', True),
            ('minus-inside', 'c00fffffffffffff', False),
            ('minus-equal', 'c010000000000000', True),
            ('minus-outside', 'c010000000000001', True))
MUTATIONS = ('coverage-missing', 'coverage-duplicate', 'coverage-self', 'false-cull',
             'node-bound', 'node-membership', 'raw-id', 'prepared-center',
             'csr-source-order', 'coefficient-word', 'root-word', 'load-word',
             'consumption', 'admission', 'refusal-status')


class InvalidRecord(Exception):
    pass


def need(condition, code):
    if not condition:
        raise InvalidRecord(code)


def fields(value, names, code):
    need(type(value) is dict and set(value) == set(names), code)


def integer(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def words(value, width, code):
    need(type(value) is list and len(value) == width, code)
    for item in value:
        bits(item)
    return value


def bits(word):
    need(type(word) is str and HEX.fullmatch(word) is not None, 'binary64-word')
    return int(word, 16)


def dyadic(word):
    value = bits(word)
    exponent, mantissa = (value >> 52) & 2047, value & ((1 << 52) - 1)
    need(exponent != 2047, 'finite-word-required')
    if exponent:
        mantissa |= 1 << 52
        shift = exponent - 1075
    else:
        shift = -1074
    result = Fraction(mantissa << shift) if shift >= 0 else Fraction(mantissa, 1 << -shift)
    return -result if value >> 63 else result


def nearest_integer(n, d):
    q, r = divmod(n, d)
    return q + int(2*r > d or (2*r == d and q % 2))


def rounded_word(value):
    """Exact rational RN-even to a binary64 word; no host floating arithmetic."""
    value = Fraction(value)
    sign, value = int(value < 0), abs(value)
    if not value:
        return ZERO
    n, d = value.numerator, value.denominator
    exponent = n.bit_length() - d.bit_length()
    below = (n < d << exponent) if exponent >= 0 else (n << -exponent < d)
    if below:
        exponent -= 1
    if exponent < -1022:
        result = nearest_integer(n << 1074, d)
    else:
        shift = 52 - exponent
        sig = nearest_integer(n << shift, d) if shift >= 0 else nearest_integer(n, d << -shift)
        if sig == 1 << 53:
            sig >>= 1
            exponent += 1
        if exponent > 1023:
            return f'{(sign << 63) | (2047 << 52):016x}'
        result = ((exponent + 1023) << 52) | (sig - (1 << 52))
    return f'{result | (sign << 63):016x}'


def subtract(a, b):
    result = dyadic(a) - dyadic(b)
    if not result and a == NEGZERO and b == ZERO:
        return NEGZERO
    return rounded_word(result)


def finite(word):
    return ((bits(word) >> 52) & 2047) != 2047


def minimum(values):
    return min(values, key=lambda w: (dyadic(w), 0 if w == NEGZERO else 1))


def maximum(values):
    return max(values, key=lambda w: (dyadic(w), 0 if w == NEGZERO else 1))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(InvalidRecord('nonfinite-json')))


def load(path):
    need(path.stat().st_size <= MAX_FILE, 'file-cap')
    return decode(path.read_bytes())


def path_at(root, relative):
    need(type(relative) is str and relative and not Path(relative).is_absolute()
         and all(p not in ('', '.', '..') for p in relative.split('/')), 'relative-path')
    path = root / relative
    need(path.resolve() == path, 'symlink-path')
    return path


def read_pin(root, pin):
    fields(pin, ('path', 'bytes', 'sha256'), 'pin-fields')
    integer(pin['bytes'], 0, MAX_FILE, 'pin-size')
    path = path_at(root, pin['path'])
    need(path.stat().st_size == pin['bytes'], 'pin-size-before-read')
    raw = path.read_bytes()
    need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'pin-content')
    return raw


def guard(ctx):
    deadline = ctx['childDeadline'] if ctx.get('closing') else ctx['computeDeadline']
    need(time.monotonic_ns() < deadline <= ctx['childDeadline'] <= ctx['totalDeadline'], 'absolute-deadline')
    need(datetime.now(timezone.utc) < ctx['cutoff'], 'authorized-cutoff')


def preflight(root, expected, commit):
    package = root / PACKAGE
    raw = (package / 'source-manifest.json').read_bytes()
    need(len(raw) <= MAX_FILE and sha(raw) == expected, 'manifest-binding')
    manifest = decode(raw)
    pins = {p['path']: p for p in manifest['files']}
    need(len(pins) == len(manifest['files']), 'duplicate-source-pin')
    for name in ('config.json', 'source/check.py', 'source/cases.json', 'source/harness.cjs', 'source/run.py'):
        need(PACKAGE + '/' + name in pins, 'source-closure')
    config = decode(read_pin(root, pins[PACKAGE + '/config.json']))
    need(config['schema'] == 'm31-native-tree-supervision-v1' and config['executionAllowed'] is True,
         'execution-not-authorized')
    auth = config['authorization']
    fields(auth, ('id', 'approvedUtc', 'reviewedSourceManifestSha256'), 'authorization-fields')
    need(type(auth['id']) is str and auth['id'] and type(auth['reviewedSourceManifestSha256']) is str
         and re.fullmatch('[0-9a-f]{64}', auth['reviewedSourceManifestSha256']), 'authorization-receipt')
    cutoff = datetime.fromisoformat(config['launchCutoffUtc'])
    approved = datetime.fromisoformat(auth['approvedUtc'])
    need(cutoff.tzinfo is not None and approved.tzinfo is not None
         and approved <= datetime.now(timezone.utc) < cutoff, 'authorization-time')
    need(os.environ.get('RESEARCH_STAGE') == 'check'
         and os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated'
         and os.environ.get('RESEARCH_CHILD_BUDGET_MILLISECONDS') == '45000', 'supervised-stage')
    token = os.environ.get('RESEARCH_RUN_TOKEN', '')
    need(re.fullmatch('[0-9a-f]{64}', token) is not None, 'supervised-token')
    attempt = load(package / 'results/run-attempt.json')
    need(attempt['schema'] == 'm31-native-tree-attempt-v1' and attempt['status'] == 'running'
         and attempt['sourceManifestSha256'] == expected and attempt['sourceCommit'] == commit
         and attempt['runTokenSha256'] == sha(token.encode())
         and attempt['stages']['check']['status'] == 'started', 'live-attempt')
    private = Path(os.environ.get('RESEARCH_PRIVATE_LOG_DIR', ''))
    need(private.is_absolute() and private.resolve() == private and private.is_dir()
         and not private.is_relative_to(root)
         and attempt['privateDirectoryIdentitySha256'] == sha(str(private).encode()), 'private-log-directory-binding')
    ctx = {'root': root, 'package': package, 'manifest': manifest, 'pins': pins,
           'expected': expected, 'commit': commit, 'cutoff': cutoff, 'privateDirectory': private,
           'childDeadline': int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS']),
           'totalDeadline': int(os.environ['RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS'])}
    ctx['computeDeadline'] = ctx['childDeadline'] - 10_000_000_000
    guard(ctx)
    for pin in pins.values():
        guard(ctx)
        read_pin(root, pin)
    need(REGRESSION['path'] in pins and pins[REGRESSION['path']] == REGRESSION, 'exposed-regression-pin')
    need(F_SOURCE[0] in pins and pins[F_SOURCE[0]]['sha256'] == F_SOURCE[1], 'unchanged-F-source-pin')
    for name, digest in F_DEPENDENCIES.items():
        relative = 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/' + name
        need(relative in pins and pins[relative]['sha256'] == digest, 'unchanged-numerical-dependency-pin')
    receipt_raw = (package / 'source-publication.json').read_bytes()
    need(len(receipt_raw) <= MAX_FILE, 'publication-cap')
    receipt = decode(receipt_raw)
    need(receipt['commit'] == commit and receipt['manifestSha256'] == expected
         and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True,
         'source-publication-binding')
    need(receipt['manifestPath'] == PACKAGE + '/source-manifest.json'
         and receipt['manifestBytes'] == len(raw) and receipt['verifiedFilePins'] == len(pins)
         and datetime.fromisoformat(receipt['verifiedUtc'].replace('Z', '+00:00')) <=
             datetime.fromisoformat(attempt['startedUtc'].replace('Z', '+00:00')), 'publication-before-run')
    ctx['protectedArtifacts'] = [
        {'path': PACKAGE + '/source-manifest.json', 'bytes': len(raw), 'sha256': sha(raw)},
        {'path': PACKAGE + '/source-publication.json', 'bytes': len(receipt_raw), 'sha256': sha(receipt_raw)}]
    runtime = manifest['runtime']['python']
    binary = Path(sys.executable).resolve().read_bytes()
    need(sys.platform == 'darwin' and sys.flags.isolated == 1 and sys.dont_write_bytecode
         and sys.version == runtime['version'] and len(binary) == runtime['bytes']
         and sha(binary) == runtime['sha256'], 'python-runtime-pin')
    return ctx


def materialize(root, spec, case):
    if case['kind'] == 'saved':
        need(case['input'] == REGRESSION and case['exposedRegression'] is True, 'regression-descriptor')
        value = decode(read_pin(root, case['input']))
        need(len(value['drones']) == 64, 'regression-size')
        return value
    base = words(spec['baseStateWords'], 17, 'base-state')
    drones = []
    if case['kind'] == 'boundary':
        fields(spec['boundaryRecipe'], ('receiverId', 'sourceFirstId', 'sourceCount', 'otherCoordinateWord'), 'boundary-recipe')
        need(spec['boundaryRecipe'] == {'receiverId': 0, 'sourceFirstId': 10, 'sourceCount': 8,
                                       'otherCoordinateWord': ZERO}, 'fixed-boundary-recipe')
        axis = integer(case['axis'], 0, 2, 'boundary-axis')
        descriptor = [(0, [ZERO]*3)] + [(j, [case['sourceWord'] if k == axis else ZERO for k in range(3)])
                                      for j in range(10, 18)]
        for identifier, center in descriptor:
            state = base.copy()
            state[:3] = center
            drones.append({'id': identifier, 'state': state})
    else:
        need(case['kind'] == 'inline', 'case-kind')
        for drone in case['drones']:
            count = integer(drone.get('repeat', 1), 1, 64, 'inline-repeat')
            for i in range(count):
                state = base.copy()
                state[:3] = words(drone['centerWords'], 3, 'inline-center')
                for key, value in drone.get('stateOverrides', {}).items():
                    index = integer(int(key), 0, 16, 'state-override-index')
                    need(str(index) == key, 'state-override-key')
                    bits(value)
                    state[index] = value
                row = {'state': state}
                if not drone.get('omitId', False):
                    row['id'] = drone['id'] + i * drone.get('idStep', 1)
                drones.append(row)
    return {'drones': drones}


def validate_spec(spec):
    need(spec['schema'] == 'm31-native-tree-cases-v1' and spec['mutationControls'] == list(MUTATIONS), 'fixed-spec')
    rows = spec['cases']
    need(len(rows) == 42 and len({c['id'] for c in rows}) == 42, 'fixed-case-count')
    boundary = [(c['id'], c['axis'], c['sourceWord'], c['screenExit']) for c in rows[:18]]
    expected = [(axis_name + '-' + suffix, axis, word, decision)
                for axis, axis_name in enumerate('xyz') for suffix, word, decision in BOUNDARY]
    need(boundary == expected, 'hardcoded-all-axis-boundaries')
    radius = rows[18:27]
    for index, case in enumerate(radius):
        axis, variant = divmod(index, 3)
        target = ('4007ffffffffffff', '4008000000000000', '4008000000000001')[variant]
        need(case['id'] == 'radius-' + 'xyz'[axis] + '-' + ('inside', 'equal', 'outside')[variant]
             and case['drones'][1]['centerWords'] == [target if k == axis else ZERO for k in range(3)]
             and case['expected']['centerEligiblePairs'] == (2 if variant == 0 else 0), 'hardcoded-radius-boundaries')


def tree_from_raw(raw):
    centers = [row['state'][:3] for row in raw]
    bounds_min = [minimum([p[k] for p in centers]) for k in range(3)]
    bounds_max = [maximum([p[k] for p in centers]) for k in range(3)]
    spans = [subtract(hi, lo) for hi, lo in zip(bounds_max, bounds_min)]
    eligible = all(finite(s) and 0 <= dyadic(s) <= 256 for s in spans)
    if not eligible:
        return centers, False, [], {}
    nodes, membership = [], {}
    def build(indices):
        identifier = len(nodes)
        lo = [minimum([centers[i][k] for i in indices]) for k in range(3)]
        hi = [maximum([centers[i][k] for i in indices]) for k in range(3)]
        node = {'id': identifier, 'min': lo, 'max': hi, 'left': None, 'right': None}
        nodes.append(node)
        membership[identifier] = indices.copy()
        if len(indices) <= 8:
            node['members'] = indices.copy()
        else:
            axis = max(range(3), key=lambda k: (dyadic(subtract(hi[k], lo[k])), -k))
            ordered = sorted(indices, key=lambda i: (dyadic(centers[i][axis]), i))
            mid = len(ordered) // 2
            node['left'] = build(ordered[:mid])
            node['right'] = build(ordered[mid:])
        return identifier
    build(list(range(len(raw))))
    return centers, True, nodes, membership


def predicate(node, center):
    comparisons = 0
    for axis in range(3):
        difference = subtract(node['min'][axis], center[axis])
        comparisons += 1
        if dyadic(difference) >= 4:
            return {'node': node['id'], 'axis': axis, 'side': 'min-ge4', 'difference': difference}, comparisons
        difference = subtract(node['max'][axis], center[axis])
        comparisons += 1
        if dyadic(difference) <= -4:
            return {'node': node['id'], 'axis': axis, 'side': 'max-le-neg4', 'difference': difference}, comparisons
    return None, comparisons


def certificate(evidence, raw, method):
    tree = evidence.get('tree')
    if raw is None:
        need(tree is None, 'capture-refusal-tree-null')
        return {'culls': 0, 'omitted': 0, 'pairs': 0}
    centers, eligible, nodes, membership = tree_from_raw(raw)
    fields(tree, ('schema', 'mode', 'leafCapacity', 'eligible', 'fallback', 'fallbackReason',
                  'complete', 'n', 'canonicalIds', 'nodes', 'receivers', 'counters'), 'tree-fields')
    need(tree['schema'] == 'm31-native-center-tree-v1' and tree['mode'] == method
         and tree['leafCapacity'] == 8 and tree['n'] == len(raw)
         and tree['canonicalIds'] == [r['id'] for r in raw]
         and tree['eligible'] is eligible and tree['fallback'] is (not eligible)
         and tree['complete'] is True, 'tree-header')
    counters = {'treeNodes': len(nodes), 'treeLeaves': sum('members' in n for n in nodes),
                'receiverTraversals': 0, 'nodeVisits': 0, 'endpointComparisons': 0,
                'culledNodes': 0, 'omittedNonselfCandidates': 0, 'visitedLeaves': 0,
                'gatheredIndices': 0, 'gatheredNonselfCandidates': 0, 'completedReceivers': 0}
    if not eligible:
        spans = [subtract(maximum([p[k] for p in centers]), minimum([p[k] for p in centers])) for k in range(3)]
        fallback_reason = 'span-nonfinite' if not all(finite(s) for s in spans) else 'span-out-of-range'
        need(tree['nodes'] == [] and tree['receivers'] == []
             and tree['fallbackReason'] == fallback_reason, 'tree-fallback')
        need(tree['counters'] == counters, 'fallback-counters')
        return {'culls': 0, 'omitted': 0, 'pairs': len(raw)*(len(raw)-1)}
    need(tree['fallbackReason'] is None and canonical(tree['nodes']) == canonical(nodes), 'tree-reconstruction')
    need(type(tree['receivers']) is list and len(tree['receivers']) == len(raw), 'receiver-coverage-count')
    for i, center in enumerate(centers):
        culls, leaves, gathered, covered = [], [], [], []
        def visit(identifier):
            node = nodes[identifier]
            counters['nodeVisits'] += 1
            decision, count = predicate(node, center)
            counters['endpointComparisons'] += count
            if decision is not None and method == 'H':
                culls.append(decision)
                members = membership[identifier]
                need(i not in members, 'self-cull')
                # Explicit independent check of every omitted source, in addition
                # to node endpoint monotonicity. This is bounded by small N64.
                for j in members:
                    need(any(abs(dyadic(subtract(centers[j][k], center[k]))) >= 4 for k in range(3)),
                         'false-cull-membership')
                covered.extend(members)
                counters['culledNodes'] += 1
                counters['omittedNonselfCandidates'] += len(members)
            elif 'members' in node:
                leaves.append(identifier)
                gathered.extend(node['members'])
                covered.extend(node['members'])
                counters['visitedLeaves'] += 1
            else:
                visit(node['left'])
                visit(node['right'])
        visit(0)
        need(sorted(covered) == list(range(len(raw))), 'independent-complete-partition')
        gathered.sort()
        want = {'receiver': i, 'culled': culls, 'leaves': leaves, 'gathered': gathered}
        need(canonical(tree['receivers'][i]) == canonical(want), 'certificate-receiver-row')
        counters['receiverTraversals'] += 1
        counters['completedReceivers'] += 1
        counters['gatheredIndices'] += len(gathered)
        counters['gatheredNonselfCandidates'] += len(gathered)-1
    need(canonical(tree['counters']) == canonical(counters), 'tree-work-counters')
    return {'culls': counters['culledNodes'], 'omitted': counters['omittedNonselfCandidates'],
            'pairs': counters['gatheredNonselfCandidates']}


def semantic_payload(evidence):
    """Exact allowlist: retain all unknown semantic/diagnostic fields by default."""
    result = copy.deepcopy(evidence)
    for key in ('method', 'timing', 'tree'):
        result.pop(key, None)
    diagnostic = result.get('diagnostics')
    if diagnostic is not None:
        diagnostic.pop('buildPhasesMs', None)
        work = diagnostic.get('geometryWork')
        if work is not None:
            for key in ('gatheredNonselfCandidates',):
                work.pop(key, None)
        screen = diagnostic.get('screen')
        if screen is not None:
            for key in ('orderedPairVisits', 'componentTests'):
                screen.pop(key, None)
    return result


def raw_binding(evidence, submitted):
    raw = evidence['raw']
    if evidence.get('stage') == 'input':
        need(raw is None and evidence['ids'] is None and evidence['prepared'] is None,
             'capture-refusal-materialization')
        return None
    expected = sorted(submitted['drones'], key=lambda d: d['id'])
    need(canonical(raw) == canonical(expected), 'canonical-raw-binding')
    identifiers = [r['id'] for r in raw]
    need(identifiers == sorted(set(identifiers)) and evidence['ids'] == identifiers, 'canonical-identities')
    for r in raw:
        integer(r['id'], 0, 9007199254740991, 'raw-id-domain')
        need(all(finite(w) for w in words(r['state'], 17, 'raw-state-width')), 'raw-finite')
    prepared = evidence['prepared']
    need(type(prepared) is list and len(prepared) == len(raw), 'prepared-count')
    for r, p in zip(raw, prepared):
        need(p['id'] == r['id'] and p['center'] == r['state'][:3]
             and p['forces'] == r['state'][13:17], 'prepared-raw-binding')
        words(p['axis'], 3, 'prepared-axis')
        need(len(p['offsets']) == len(p['points']) == 4, 'prepared-rotor-count')
        for offset, point in zip(p['offsets'], p['points']):
            words(offset, 3, 'prepared-offset'); words(point, 3, 'prepared-point')
    return raw


def csr(evidence, n):
    q = evidence['coefficients']
    fields(q, ('offsets', 'sourceIndices', 'K', 'a'), 'csr-fields')
    offsets, sources = q['offsets'], q['sourceIndices']
    count = len(sources)
    need(count <= 2_000_000 and len(offsets) == 4*n+1 and offsets[0] == 0
         and offsets[-1] == count and len(q['K']) == len(q['a']) == count, 'csr-shape')
    for z in offsets:
        integer(z, 0, count, 'csr-offset-range')
    for row in range(4*n):
        lo, hi = offsets[row:row+2]
        need(lo <= hi, 'csr-offset-order')
        previous = -1
        for z in range(lo, hi):
            source = integer(sources[z], 0, n-1, 'csr-source-range')
            need(source > previous and source != row//4, 'csr-positive-order-self')
            previous = source
            need(dyadic(q['K'][z]) > 0 and dyadic(q['a'][z]) > 0, 'csr-positive-words')


def consumption(evidence):
    ids = evidence['ids']
    need([r['id'] for r in evidence['solution']] == ids
         and [r['id'] for r in evidence['loads']] == ids, 'solution-load-id-binding')
    h, load_count = 2166136261, 0
    status = 'native-success'
    for c in status:
        h = ((h ^ ord(c)) * 16777619) & 0xffffffff
    def mix(word):
        nonlocal h
        value = bits(word)
        h = ((h ^ (value >> 32)) * 16777619) & 0xffffffff
        h = ((h ^ (value & 0xffffffff)) * 16777619) & 0xffffffff
    for solution, load in zip(evidence['solution'], evidence['loads']):
        need(0 < dyadic(solution['y']) <= 1 and len(solution['rotors']) == 4, 'solution-domain')
        for rotor in solution['rotors']:
            need(dyadic(rotor['alpha']) >= 0 and 0 < dyadic(rotor['x']) <= 1
                 and dyadic(rotor['T']) > 0, 'rotor-solution-domain')
        mix(rounded_word(Fraction(load['id'])))
        values = words(load['rotor'], 4, 'rotor-load-width') + [load['collective']] \
            + words(load['worldForce'], 3, 'force-width') + words(load['worldMoment'], 3, 'moment-width')
        for word in values:
            dyadic(word)
            mix(word)
            load_count += 1
    want = {'kind': 'native-load-id-status-fnv32', 'status': status, 'loadWords': load_count,
            'identityWords': len(ids), 'statusCharacters': len(status), 'value': h}
    need(evidence['consumption'] == want, 'consumption-word-id-status')


def verify_case(row, case, expected_input):
    need(row['id'] == case['id'] and canonical(row['input']) == canonical(expected_input), 'case-input-binding')
    need(set(row['methods']) == set(METHODS) and row['inputUnchanged'] == {m: True for m in METHODS},
         'complete-methods-input-preservation')
    stats = {}
    for method in METHODS:
        evidence = row['methods'][method]
        need(evidence['schema'] == 'm31-native-load-evidence-v1' and evidence['method'] == method
             and evidence['status'] == case['expected']['status']
             and evidence['reason'] == case['expected']['reason'], 'expected-native-status-reason')
        raw = raw_binding(evidence, row['input'])
        if raw is not None:
            csr(evidence, len(raw))
            if 'eligible' in case['expected']:
                need(evidence['diagnostics']['screen']['eligible'] is case['expected']['eligible'], 'expected-eligibility')
            diagnostic = evidence['diagnostics']
            expected = case['expected']
            if 'centerEligiblePairs' in expected:
                need(diagnostic['geometryWork']['centerEligiblePairs'] == expected['centerEligiblePairs']
                     and diagnostic['geometryWork']['directedCenterTests'] == 2, 'strict-center-radius-control')
            if 'admissionReason' in expected:
                need(diagnostic['admission']['admitted'] is False
                     and expected['admissionReason'] in diagnostic['admission']['reasons'], 'expected-admission-reason')
            if 'descendingEligible' in expected:
                need(diagnostic['admission']['admitted'] is True
                     and diagnostic['graph']['descendingEligible'] is expected['descendingEligible'], 'expected-graph-refusal')
            if case['id'] == 'invalid-far-geometry':
                need(diagnostic['input']['geometryValid'] is False
                     and 'geometry' in diagnostic['admission']['reasons']
                     and 'invalid-term' in diagnostic['admission']['reasons']
                     and diagnostic['admission']['invalidTermCount'] == 8, 'invalid-far-before-outside')
        if evidence['status'] == 'native-success':
            need(evidence['diagnostics']['admission']['admitted'] is True
                 and evidence['diagnostics']['graph']['descendingEligible'] is True, 'successful-admission')
            consumption(evidence)
        if method in ('H', 'H0'):
            stats[method] = certificate(evidence, raw, method)
        else:
            need(evidence.get('tree') is None, 'unchanged-F-no-tree')
        if raw is not None:
            n = len(raw)
            work = evidence['diagnostics']['geometryWork']
            screen = evidence['diagnostics']['screen']
            need(work['logicalDirectedPairs'] == n*(n-1)
                 and work['certifiedSkippedPairs'] == n*(n-1)-work['directedCenterTests'], 'logical-pair-accounting')
            if screen['eligible']:
                count = n*(n-1) if method == 'F' else stats[method]['pairs']
                need(work['gatheredNonselfCandidates'] == count
                     and screen['orderedPairVisits'] == count and screen['componentTests'] == count,
                     'gather-work-certificate-binding')
            else:
                need(work['gatheredNonselfCandidates'] == n*(n-1)
                     and screen['orderedPairVisits'] == n*(n-1) and screen['componentTests'] == 0,
                     'fallback-work-all-pairs-binding')
    baseline = canonical(semantic_payload(row['methods']['F']))
    for method in ('H0', 'H'):
        need(canonical(semantic_payload(row['methods'][method])) == baseline, 'full-native-semantic-equivalence')
    if case['kind'] == 'boundary':
        h = row['methods']['H']['tree']['receivers'][0]
        omitted = stats['H']['omitted']
        need(bool(h['culled']) is case['screenExit'], 'boundary-group-decision')
        need((omitted > 0) is case['screenExit'], 'boundary-pair-decision')
    return {'id': case['id'], 'status': 'pass', 'nativeStatus': case['expected']['status'],
            'exposedRegression': case.get('exposedRegression', False), 'work': stats}


def arithmetic_controls():
    fixtures = [(word, ZERO, word) for _, word, _ in BOUNDARY]
    fixtures += [('4010000000000000', '3cb0000000000000', '4010000000000000'),
                 ('4010000000000000', '3cc0000000000000', '400fffffffffffff'),
                 ('4010000000000000', 'bcc0000000000000', '4010000000000000'),
                 ('4010000000000000', 'bcd0000000000000', '4010000000000001'),
                 ('c010000000000000', 'bcb0000000000000', 'c010000000000000'),
                 (NEGZERO, ZERO, NEGZERO), (ZERO, NEGZERO, ZERO), (NEGZERO, NEGZERO, ZERO),
                 ('0000000000000001', ZERO, '0000000000000001'),
                 ('4070000000000001', '3d20000000000000', '4070000000000000')]
    for a, b, result in fixtures:
        need(subtract(a, b) == result, 'fixed-RN-subtraction-fixture')
    for _, word, decision in BOUNDARY:
        need((abs(dyadic(subtract(word, ZERO))) >= 4) is decision, 'fixed-screen-comparison-fixture')
    return {'status': 'pass', 'subtractionFixtures': len(fixtures), 'thresholdComparisons': len(BOUNDARY),
            'source': 'hardcoded binary64 word answers; exact integer/Fraction RN-even'}


def mutation_controls(rows, cases, inputs, ctx):
    by_id = {r['id']: r for r in rows}
    descriptors = {c['id']: c for c in cases}
    outcomes = []
    for name in MUTATIONS:
        guard(ctx)
        target = 'x-plus-equal'
        if name in ('false-cull',): target = 'x-plus-inside'
        if name in ('raw-id', 'prepared-center', 'csr-source-order', 'coefficient-word',
                    'root-word', 'load-word', 'consumption', 'admission'): target = 'positive-canonical'
        if name == 'refusal-status': target = 'invalid-far-geometry'
        row = copy.deepcopy(by_id[target]); h = row['methods']['H']
        tree = h['tree']; receiver = tree['receivers'][0] if tree and tree['receivers'] else None
        wanted = 'certificate-receiver-row'
        if name == 'coverage-missing': receiver['gathered'].pop()
        elif name == 'coverage-duplicate': receiver['gathered'].append(receiver['gathered'][-1])
        elif name == 'coverage-self': receiver['gathered'].remove(0)
        elif name == 'false-cull':
            receiver['culled'].append({'node': 0, 'axis': 0, 'side': 'min-ge4', 'difference': '4010000000000000'})
        elif name == 'node-bound':
            tree['nodes'][0]['min'][0] = '4010000000000000'; wanted = 'tree-reconstruction'
        elif name == 'node-membership':
            leaf = next(n for n in tree['nodes'] if 'members' in n)
            leaf['members'][0] = leaf['members'][-1]; wanted = 'tree-reconstruction'
        elif name == 'raw-id': h['raw'][0]['id'] += 1; wanted = 'canonical-raw-binding'
        elif name == 'prepared-center': h['prepared'][0]['center'][0] = '3ff0000000000000'; wanted = 'prepared-raw-binding'
        elif name == 'csr-source-order':
            q = h['coefficients']; need(q['sourceIndices'], 'mutation-positive-fixture-required')
            first_row = next(i for i in range(len(q['offsets'])-1) if q['offsets'][i+1]-q['offsets'][i] >= 2)
            z = q['offsets'][first_row]
            q['sourceIndices'][z], q['sourceIndices'][z+1] = q['sourceIndices'][z+1], q['sourceIndices'][z]
            wanted = 'csr-positive-order-self'
        elif name == 'coefficient-word':
            need(h['coefficients']['K'], 'mutation-positive-fixture-required')
            h['coefficients']['K'][0] = rounded_word(dyadic(h['coefficients']['K'][0])*2)
            wanted = 'full-native-semantic-equivalence'
        elif name == 'root-word':
            old = h['solution'][0]['y']
            h['solution'][0]['y'] = '3fe0000000000000' if old != '3fe0000000000000' else '3fe0000000000001'
            wanted = 'full-native-semantic-equivalence'
        elif name == 'load-word': h['loads'][0]['rotor'][0] = '3fb0000000000001'; wanted = 'consumption-word-id-status'
        elif name == 'consumption': h['consumption']['value'] ^= 1; wanted = 'consumption-word-id-status'
        elif name == 'admission':
            h['diagnostics']['admission']['admitted'] = False; wanted = 'successful-admission'
        elif name == 'refusal-status': h['status'] = 'native-success'; wanted = 'expected-native-status-reason'
        try:
            verify_case(row, descriptors[target], inputs[target])
        except InvalidRecord as error:
            need(str(error) == wanted, 'mutation-unexpected-rejection:' + name + ':' + str(error))
            outcomes.append({'id': name, 'kind': 'saved-record-mutation-control', 'status': 'rejected', 'reason': wanted})
        else:
            raise InvalidRecord('mutation-not-rejected:' + name)
    return outcomes


def output_budget(ctx, extra):
    total = extra
    for base in (ctx['package'] / 'results', ctx['privateDirectory']):
        if base.exists():
            for path in base.rglob('*'):
                need(not path.is_symlink(), 'output-symlink')
                if not path.is_dir():
                    need(path.is_file() and path.stat().st_size <= MAX_FILE, 'output-file-cap')
                    total += path.stat().st_size
    need(total + 2*1024*1024 <= MAX_TOTAL, 'output-total-cap')


def main(root, expected, commit):
    ctx = preflight(root, expected, commit)
    result = {'schema': 'm31-native-tree-check-v1', 'sourceManifestSha256': expected,
              'sourceCommit': commit, 'status': 'failed', 'reason': None, 'complete': False, 'passed': False,
              'scope': 'Small fixed saved evidence and exposed64 regression only; no fresh performance or exact-load qualification.',
              'primaryCases': [], 'arithmeticControls': None, 'mutationControls': []}
    try:
        spec = decode(read_pin(root, ctx['pins'][PACKAGE + '/source/cases.json']))
        validate_spec(spec)
        inputs = {c['id']: materialize(root, spec, c) for c in spec['cases']}
        work_path = ctx['package'] / 'results/work.json'
        journal_path = ctx['package'] / 'results/work.jsonl'
        need(work_path.stat().st_size <= MAX_FILE, 'work-file-cap')
        work_raw = work_path.read_bytes()
        work = decode(work_raw)
        ctx['protectedArtifacts'].append({'path': PACKAGE + '/results/work.json',
                                          'bytes': len(work_raw), 'sha256': sha(work_raw)})
        need(work['schema'] == 'm31-native-tree-work-v1' and work['status'] == 'completed'
             and work['reason'] is None and work['sourceCommit'] == commit
             and work['sourceManifestSha256'] == expected and work['complete'] is True
             and work['runtimeIdentityVerified'] is True and work['inputsAndSourcesPreserved'] is True,
             'work-source-completion')
        need(journal_path.stat().st_size <= MAX_FILE, 'journal-cap')
        journal_raw = journal_path.read_bytes()
        ctx['protectedArtifacts'].append({'path': PACKAGE + '/results/work.jsonl',
                                          'bytes': len(journal_raw), 'sha256': sha(journal_raw)})
        need(journal_raw.endswith(b'\n'), 'journal-complete-line')
        journal = [decode(line) for line in journal_raw.splitlines()]
        need(canonical(journal) == canonical(work['cases']), 'durable-journal-work-binding')
        need([r['id'] for r in work['cases']] == [c['id'] for c in spec['cases']], 'exact-case-order')
        need(work['journal'] == {'path': PACKAGE + '/results/work.jsonl', 'bytes': len(journal_raw),
                                 'sha256': sha(journal_raw), 'records': len(journal)}, 'journal-descriptor-binding')
        sidecars = work['evidenceFiles']
        need(type(sidecars) is list and len(sidecars) == len(work['cases'])*3, 'exact-sidecar-count')
        for index, row in enumerate(work['cases']):
            for method_index, method in enumerate(METHODS):
                guard(ctx)
                pin = sidecars[3*index+method_index]
                fields(pin, ('caseId', 'method', 'path', 'bytes', 'sha256'), 'sidecar-descriptor-fields')
                need(pin['caseId'] == row['id'] and pin['method'] == method
                     and pin['path'] == PACKAGE + '/results/evidence/' + f'{index:03d}-' + row['id'] + '-' + method + '.json',
                     'sidecar-case-method-path-binding')
                encoded = decode(read_pin(root, {k: pin[k] for k in ('path', 'bytes', 'sha256')}))
                ctx['protectedArtifacts'].append({k: pin[k] for k in ('path', 'bytes', 'sha256')})
                need(canonical(encoded) == canonical(row['methods'][method]), 'sidecar-body-binding')
        result['arithmeticControls'] = arithmetic_controls()
        for row, case in zip(work['cases'], spec['cases']):
            guard(ctx)
            result['primaryCases'].append(verify_case(row, case, inputs[case['id']]))
        saved = {r['id']: r for r in work['cases']}
        for method in METHODS:
            need(canonical(semantic_payload(saved['positive-canonical']['methods'][method])) ==
                 canonical(semantic_payload(saved['positive-permuted']['methods'][method])), 'input-permutation-invariance')
        result['mutationControls'] = mutation_controls(work['cases'], spec['cases'], inputs, ctx)
        result['status'] = 'pass'
        result['checkedCases'] = len(result['primaryCases'])
        result['checkedQueries'] = len(result['primaryCases']) * 3
        result['evidence'] = {'work': {'bytes': len(work_raw), 'sha256': sha(work_raw)},
                              'journal': {'bytes': len(journal_raw), 'sha256': sha(journal_raw)}}
    except Exception as error:
        result['reason'] = (type(error).__name__ + ':' + str(error))[:512]
    ctx['closing'] = True
    result['complete'] = True
    result['passed'] = result['status'] == 'pass'
    guard(ctx)
    for pin in ctx['pins'].values():
        guard(ctx); read_pin(root, pin)
    for pin in ctx['protectedArtifacts']:
        guard(ctx); read_pin(root, pin)
    raw = canonical(result) + b'\n'
    output_budget(ctx, len(raw))
    with (ctx['package'] / 'results/check.json').open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    need(len(sys.argv) == 4, 'arguments-root-manifest-commit')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]))
