"""Independent saved-stage checker; no native producer or exact oracle execution."""
from pathlib import Path
from fractions import Fraction
import copy
import hashlib
import importlib.util
import json
import resource
import sys

PACKAGE = 'research/m31-coupled-stage-qualification-2026-10-17'


def bootstrap(root, expected, commit):
    raw = (root / PACKAGE / 'source-manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('bootstrap-manifest')
    manifest = json.loads(raw)
    path = root / PACKAGE / 'source/reference.py'
    pins = [p for p in manifest['files'] if p['path'] == PACKAGE + '/source/reference.py']
    source = path.read_bytes()
    if len(pins) != 1 or len(source) != pins[0]['bytes'] or hashlib.sha256(source).hexdigest() != pins[0]['sha256']:
        raise ValueError('bootstrap-support-pin')
    spec = importlib.util.spec_from_file_location('_coupled_reference_support', path)
    support = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(support)
    return support, support.preflight(root, expected, commit, 'check')


class StageAudit:
    def __init__(self, support, ctx):
        self.s, self.ctx = support, ctx
        self.a = support.module(ctx, 'native_check')
        self.coverage = support.module(ctx, 'coverage_check')
        self.d, self.r = self.a.dyadic, self.a.rnd
        # Decimal literals are converted with the independent exact RN routine.
        self.m = self.r(Fraction('0.027')); self.g = self.r(Fraction('9.81'))
        self.I = [self.r(Fraction(v)) for v in ('0.000014', '0.000014', '0.0000217')]
        self.arm = self.r(Fraction('0.028')); self.km = self.r(Fraction('7.94e-12'))
        self.kf = self.r(Fraction('3.16e-10')); self.tau = self.r(Fraction('0.04'))
        self.mg = self.r(self.m * self.g)
        self.counts = {'stages': 0, 'droneStages': 0, 'derivativeWords': 0,
                       'projections': 0, 'nativeReferences': 0, 'steps': 0}

    def need(self, value, code):
        self.a.require(value, code)

    def vec(self, words, width, code):
        return [self.d(x) for x in self.a.vector(words, width, code)]

    def equal(self, words, values, code):
        self.need(self.vec(words, len(values), code) == values, code)

    def add(self, a, b):
        return [self.r(x + y) for x, y in zip(a, b)]

    def scale(self, a, b):
        return [self.r(x * b) for x in a]

    def cross(self, a, b):
        return self.a.native_cross(a, b)

    def rotate(self, q, v):
        t = self.scale(self.cross(q, v), 2)
        return self.add(v, self.add(self.scale(t, q[3]), self.cross(q, t)))

    def projection(self, raw_words, state_words, square_word, norm_word):
        raw = self.vec(raw_words, 17, 'raw-state-width')
        state = self.vec(state_words, 17, 'state-width')
        q = raw[6:10]
        square = self.a.left_sum(self.r(x*x) for x in q)
        self.need(self.d(square_word) == square and square > 0, 'projection-square-arithmetic')
        norm = self.d(norm_word); bits = int(norm_word, 16)
        self.need(norm > 0 and 0 < bits < 0x7fefffffffffffff, 'projection-sqrt-domain')
        previous = self.d('%016x' % (bits - 1)); following = self.d('%016x' % (bits + 1))
        lower, upper = (previous + norm)/2, (norm + following)/2
        self.need(lower*lower <= square <= upper*upper
                  and (square not in (lower*lower, upper*upper) or bits % 2 == 0),
                  'projection-correctly-rounded-sqrt')
        want = raw[:6] + [self.r(x/norm) for x in q] + raw[10:]
        self.need(state == want, 'projection-divide-arithmetic')
        self.need(raw_words[:6] == state_words[:6] and raw_words[10:] == state_words[10:],
                  'projection-preserves-nonquaternion-words')
        self.need(abs(sum(x*x for x in state[6:10])-1) <= Fraction(1, 10**10), 'projected-unit-tolerance')
        self.counts['projections'] += 1
        return state

    def consumed(self, row):
        load = row['consumed']
        self.a.fields(load, ('rotorWords', 'collectiveWord', 'worldForceWords', 'worldMomentWords'), 'consumed-fields')
        return {'rotor': self.vec(load['rotorWords'], 4, 'consumed-rotor'),
                'collective': self.d(load['collectiveWord']),
                'worldForce': self.vec(load['worldForceWords'], 3, 'consumed-force'),
                'worldMoment': self.vec(load['worldMomentWords'], 3, 'consumed-moment')}

    def nominal(self, state):
        q, forces = state[6:10], state[13:17]
        axis = self.rotate(q, [Fraction(0), Fraction(0), Fraction(1)])
        corners = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        offsets = [self.rotate(q, [sx*self.arm, sy*self.arm, Fraction(0)]) for sx, sy in corners]
        prepared = {'axis': [self.a.rounded_word(x) for x in axis],
                    'offsets': [[self.a.rounded_word(x) for x in offset] for offset in offsets]}
        return self.a.native_loads(prepared, forces)

    def derivative(self, row):
        state = self.projection(row['rawStateWords'], row['stateWords'], row['normSquareWord'], row['normWord'])
        command = self.vec(row['commandsWords'], 4, 'command-width')
        self.need(row['nominalMotorWords'] == row['stateWords'][13:17], 'nominal-motor-state-binding')
        self.need(all(v >= 0 for v in command) and all(v > 0 for v in state[13:17]), 'motor-command-domains')
        load = self.consumed(row)
        q, w = state[6:10], state[10:13]
        inverse = [-q[0], -q[1], -q[2], q[3]]
        body = self.rotate(inverse, load['worldMoment'])
        yaw = self.a.left_sum(self.r(self.r(self.r(sign*self.km)/self.kf)*force)
                             for sign, force in zip((1, -1, 1, -1), state[13:17]))
        torque = body[:2] + [self.r(body[2] + yaw)]
        gyro = self.cross(w, [self.r(x*i) for x, i in zip(w, self.I)])
        self.equal(row['bodyArmWords'], body, 'world-to-body-moment-arithmetic')
        self.equal(row['totalBodyWords'], torque, 'nominal-yaw-added-once')
        self.need(self.d(row['nominalYawWord']) == yaw, 'nominal-yaw-state-law')
        self.equal(row['gyroWords'], gyro, 'gyroscopic-arithmetic')
        qv = self.add(self.add(self.scale(w, q[3]), self.scale(q[:3], Fraction(0))), self.cross(q, w))
        qw = self.r(self.r(q[3]*0) - self.a.left_sum(self.r(x*y) for x, y in zip(q[:3], w)))
        qdot = self.scale(qv + [qw], Fraction(1, 2))
        acceleration = [self.r(v/self.m) for v in load['worldForce']]
        acceleration[2] = self.r(acceleration[2]-self.g)
        angular = [self.r(self.r(t-g)/i) for t, g, i in zip(torque, gyro, self.I)]
        motor = [self.r(self.r(u-f)/self.tau) for u, f in zip(command, state[13:17])]
        expected = state[3:6] + acceleration + qdot + angular + motor
        self.equal(row['derivativeWords'], expected, 'total-load-derivative-arithmetic')
        self.counts['droneStages'] += 1; self.counts['derivativeWords'] += 17
        return state, load, expected

    @staticmethod
    def exact_cross(a, b):
        return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

    def inverse_matrix(self, q):
        """Exact unit-quaternion inverse; division by ||q||² includes projection residual."""
        v, w, norm2 = [-x for x in q[:3]], q[3], sum(x*x for x in q)
        self.need(norm2 > 0, 'rational-frame-quaternion')
        columns = []
        for k in range(3):
            basis = [Fraction(int(j == k)) for j in range(3)]
            first = self.exact_cross(v, basis); second = self.exact_cross(v, first)
            columns.append([basis[j] + 2*(w*first[j]+second[j])/norm2 for j in range(3)])
        return [[columns[k][j] for k in range(3)] for j in range(3)]

    @staticmethod
    def interval_map(matrix, boxes):
        return [(sum(min(a*lo, a*hi) for a, (lo, hi) in zip(row, boxes)),
                 sum(max(a*lo, a*hi) for a, (lo, hi) in zip(row, boxes))) for row in matrix]

    def frame_bound(self, row, ref_load, radius):
        q = self.vec(row['stateWords'][6:10], 4, 'frame-q')
        matrix = self.inverse_matrix(q)
        actual = self.vec(row['bodyArmWords'], 3, 'body-arm')
        boxes = self.interval_map(matrix, ref_load['worldMoment'])
        bounds = self.a.squared_error(actual, boxes, self.mg*radius)
        self.need(self.a.verdict(bounds) == 'pass', 'body-moment-reference-bound')
        delivered = self.vec(row['consumed']['worldMomentWords'], 3, 'frame-delivered-moment')
        ideal = self.interval_map(matrix, [(x, x) for x in delivered])
        conversion = self.a.squared_error(actual, ideal, self.mg*radius)
        self.need(self.a.verdict(conversion) == 'pass', 'frame-projection-conversion-bound')
        return {'bodyReference': self.a.encoded_interval(*bounds),
                'conversionOnly': self.a.encoded_interval(*conversion), 'squaredNormalized': True}

    def target(self, stage, record, constants):
        ids = self.a.raw_input(stage['nativeInput'], 64)
        self.need(record['sourceCommit'] == self.ctx['commit']
                  and record['sourceManifestSha256'] == self.ctx['expected'], 'reference-source-binding')
        digest = self.s.sha(self.s.canonical(stage['nativeInput']))
        input_pin = self.s.input_sidecar(self.ctx, self.browser, stage)
        self.need(record['inputFile'] == input_pin, 'reference-actual-input-file-binding')
        self.need(record['id'] == stage['stageId'] and record['input'] == stage['nativeInput']
                  and record['inputSha256'] == digest and record['referenceStatus'] == 'admitted'
                  and record['branch'] == 'loads' and record['recipe'] == {
                      'coefficientBits': 192, 'sourceBits': 192, 'rootBisections': 128}, 'reference-stage-binding')
        # Reuse the frozen independent combinatorial audit without inventing
        # individual zero-pair rows or reevaluating any exact oracle predicate.
        adapted = dict(record, planned=record['plannedPairs'])
        adapted['pairs'] = [dict(p, oracle={k: p[k] for k in ('status', 'branch')}) for p in record['pairs']]
        if record['coverage']['mode'] == 'hierarchy':
            positive, coverage = self.coverage.coverage_review(adapted, ids)
        else:
            positive, coverage = self.fallback_coverage(record, ids)
        self.need(record['evaluatedPairs'] == coverage['scalarPairs'] <= 16128, 'stage-suffix-count')
        counts = record['reuseCounters']
        self.need(counts == {'prepareOneCalls': 64, 'preparationValidCalls': 64,
                            'oracleCalls': coverage['scalarPairs'], 'operandLookups': 2*coverage['scalarPairs'],
                            'pairPreparations': 0}, 'reference-prepared-reuse-counts')
        ranks = {identifier: k for k, identifier in enumerate(record['order'])}
        self.need(set(ranks) == set(ids) and len(record['order']) == 64
                  and all(ranks[j] < ranks[i] for i, r, j in positive), 'positive-acyclic-order')
        prepared = record['prepared']
        self.need([p['id'] for p in prepared] == ids and all(p['rejection'] is None for p in prepared), 'reference-preparation')
        loads = {}
        self.need([p['id'] for p in record['loads']] == ids, 'reference-load-ids')
        for row in record['loads']:
            for box in self.a.vector(row['roots'], 4, 'four-root-boxes'):
                lo, hi = self.a.interval(box); self.need(0 < lo <= hi <= 1, 'reference-root-range')
            value = row['loads']
            loads[row['id']] = {'rotor': [self.a.interval(x) for x in self.a.vector(value['rotor'], 4, 'reference-rotors')],
                'collective': self.a.interval(value['collective']),
                'worldForce': [self.a.interval(x) for x in self.a.vector(value['force'], 3, 'reference-force')],
                'worldMoment': [self.a.interval(x) for x in self.a.vector(value['moment'], 3, 'reference-moment')]}
        self.need(constants['mg'] == '3fd0f3a14cec41dd' and constants['R'] == '3fa4462fb7ff5035', 'normalization-words')
        return {'id': stage['stageId'], 'ids': ids, 'raw': stage['nativeInput']['drones'],
                'digest': digest, 'inputFileSha256': input_pin['sha256'],
                'prepared': {p['id']: p['value'] for p in prepared}, 'loads': loads,
                'positive': {key: self.a.interval(box) for key, box in positive.items()},
                'constants': {key: constants[key] for key in self.a.CONSTANT_KEYS}}, coverage

    def fallback_coverage(self, record, ids):
        """Full scalar fallback is allowed only when its complete partition is saved."""
        cov = record['coverage']; n = len(ids); planned = 4*n*(n-1)
        self.need(cov['mode'] == 'fallback' and record['tree'] is None and cov['complete'] is True
                  and cov['permutation'] == ids and cov['coveredPairs'] == cov['requiredCoveredPairs']
                  == cov['logicalPairs'] == record['plannedPairs'] == planned, 'fallback-complete-declaration')
        self.need([(q['i'], q['r']) for q in cov['queries']] == [(i, r) for i in range(n) for r in range(4)],
                  'fallback-query-order')
        for query in cov['queries']:
            i = query['i']
            self.need(query['id'] == ids[i] and query['selfPosition'] == i and query['terminals'] == [{
                'kind': 'scan', 'node': None, 'start': 0, 'end': n, 'count': n-1,
                'sourceIndices': [j for j in range(n) if j != i]}], 'fallback-scalar-membership')
        pairs = record['pairs']
        self.need([(p['ii'], p['r'], p['jj']) for p in pairs]
                  == [(i, r, j) for i in range(n) for r in range(4) for j in range(n) if j != i], 'fallback-pair-completeness')
        positive = {}
        for p in pairs:
            self.need(p['i'] == ids[p['ii']] and p['j'] == ids[p['jj']] and p['status'] in ('positive', 'zero'),
                      'fallback-pair-id-status')
            if p['status'] == 'positive':
                positive[(p['i'], p['r'], p['j'])] = p['coefficient']
        self.need(cov['work']['scalarPairs'] == planned and cov['work']['zeroPairs'] == 0
                  and cov['work']['positiveTerms'] == len(positive), 'fallback-work-count')
        return positive, {'logicalPairs': planned, 'scalarPairs': planned,
                          'positiveTerms': len(positive), 'zeroPredicatesReevaluated': False}

    def stage(self, stage, target=None, manufactured=False):
        self.s.guard(self.ctx)
        self.need(stage['schema'] == 'm31-coupled-stage-v1' and stage['status'] == 'completed'
                  and stage['reason'] is None and type(stage['stepIndex']) is int
                  and type(stage['stageIndex']) is int, 'stage-completed')
        rows = stage['records']; ids = [row['id'] for row in rows]
        self.need(all(type(i) is int and 0 <= i <= 65535 for i in ids)
                  and ids == sorted(set(ids)) and len(ids) == (1 if manufactured else 64), 'stage-stable-ids')
        self.need(stage['nativeInput'] == {'drones': [{'id': r['id'], 'state': r['stateWords']} for r in rows]},
                  'stage-native-input-consumption')
        self.need(stage['rawBeforeProjection'] == {'drones': [{'id': r['id'], 'state': r['rawStateWords']} for r in rows]}
                  and stage['commandsBeforeEvaluation'] == [r['commandsWords'] for r in rows], 'stage-before-after-binding')
        native_report = None
        if target is not None:
            self.need(stage['nativeCalls'] == 1 and stage['arm'] == 'coupled', 'single-primary-query')
            # Explicit derived compatibility view: the original producer record
            # has no fictional file digest; this value comes from verified bytes.
            derived = dict(stage['native'], inputFileSha256=target['inputFileSha256'])
            native_report = self.a.audit_evidence(derived, target, 'F')
            self.need(native_report['qualified'], 'native-four-category-gates')
            self.counts['nativeReferences'] += 1
        else:
            self.need(stage['native'] is None and stage['nativeCalls'] == 0, 'no-control-native-query')
        frame_max = Fraction(0)
        for index, row in enumerate(rows):
            state, load, derivative = self.derivative(row)
            if target is not None:
                delivered = stage['native']['loads'][index]
                self.need(delivered['id'] == row['id'] and row['consumed'] == {
                    'rotorWords': delivered['rotor'], 'collectiveWord': delivered['collective'],
                    'worldForceWords': delivered['worldForce'], 'worldMomentWords': delivered['worldMoment']},
                    'actual-delivered-words-consumed')
                bounds = self.frame_bound(row, target['loads'][row['id']], self.d(target['constants']['R']))
                frame_max = max(frame_max, self.a.rat(bounds['bodyReference']['u']))
            elif not manufactured:
                self.need(load == self.nominal(state), 'off-nominal-load-arithmetic')
        self.counts['stages'] += 1
        return {'stageId': stage['stageId'], 'passed': True, 'native': native_report,
                'bodyMomentMaxSquaredNormalizedUpper': self.a.encoded(frame_max)}

    def step(self, step, stages, expected_start, commands):
        self.need(step['schema'] == 'm31-coupled-step-v1' and step['status'] == 'completed'
                  and step['reason'] is None and type(step['stepIndex']) is int, 'step-schema')
        ids = [row['id'] for row in expected_start]
        self.need(step['start'] == expected_start and len(stages) == 4
                  and step['stageIds'] == [s['stageId'] for s in stages], 'step-base-and-stage-binding')
        h = self.d(step['dtWord']); step_index = step['stepIndex']
        t = self.r(step_index*h); half = self.r(h/2)
        base = [self.vec(row['stateWords'], 17, 'base-state') for row in expected_start]
        derivatives = []
        for k, stage in enumerate(stages):
            self.need(stage['arm'] == step['arm'] and stage['stepIndex'] == step_index
                      and stage['stageIndex'] == k+1 and stage['dtWord'] == step['dtWord'], 'rk-stage-identity')
            self.need([row['id'] for row in stage['records']] == ids
                      and [row['commandsWords'] for row in stage['records']] == commands, 'rk-id-command-binding')
            at = t if k == 0 else self.r(t + (half if k < 3 else h))
            self.need(self.d(stage['relativeTimeWord']) == at, 'rk-stage-time')
            for i, row in enumerate(stage['records']):
                want = base[i] if k == 0 else [self.r(v+self.r((half if k < 3 else h)*d))
                                                         for v, d in zip(base[i], derivatives[k-1][i])]
                self.equal(row['rawStateWords'], want, 'rk-stage-state-chain')
            derivatives.append([self.vec(row['derivativeWords'], 17, 'rk-derivative') for row in stage['records']])
        self.need([row['id'] for row in step['rawFinal']] == ids and [row['id'] for row in step['final']] == ids,
                  'rk-final-id-binding')
        for i, (raw, final) in enumerate(zip(step['rawFinal'], step['final'])):
            want = []
            for j, value in enumerate(base[i]):
                terms = [derivatives[k][i][j] for k in range(4)]
                weighted = self.r(self.r(self.r(terms[0]+self.r(2*terms[1]))+self.r(2*terms[2]))+terms[3])
                want.append(self.r(value+self.r(self.r(h*weighted)/6)))
            self.equal(raw['stateWords'], want, 'rk-endpoint-arithmetic')
            self.projection(raw['stateWords'], final['stateWords'], final['normSquareWord'], final['normWord'])
        self.need(self.d(step['relativeTimeWord']) == self.r(t+h), 'rk-endpoint-time')
        self.counts['steps'] += 1
        return [{'id': row['id'], 'stateWords': row['stateWords']} for row in step['final']]


def analytic_box(kind, x):
    """Fixed 40-term exact series; rigorous remainder, no libm transcendental oracle."""
    x = Fraction(x)
    if abs(x) > Fraction(1, 2):
        raise ValueError('analytic-fixed-domain')
    if kind == 'exp':
        term = total = Fraction(1)
        for k in range(1, 40):
            term *= x/k; total += term
        next_term = term*x/40
        error = 2*abs(next_term)  # remaining absolute term ratio is <1/2.
    else:
        term = Fraction(1) if kind == 'cos' else x
        total = term
        for k in range(1, 40):
            a = 2*k if kind == 'cos' else 2*k+1
            term *= -x*x/((a-1)*a); total += term
        a = 80 if kind == 'cos' else 81
        error = abs(term*x*x/((a-1)*a))  # alternating decreasing remainder.
    return total-error, total+error


def basic_values(audit, case):
    initial = [Fraction(0), Fraction(0), Fraction(1)]
    initial += [audit.r(Fraction(x)) for x in (('0.2', '-0.1', '0.05') if case == 'translation' else ('0', '0', '0'))]
    initial += [Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(case == 'principal-spin')]
    initial += [audit.r(Fraction('0.04' if case == 'motor-relaxation' else '0.06'))]*4
    command = [audit.r(Fraction('0.08' if case == 'motor-relaxation' else '0.06'))]*4
    return initial, command


def manufactured_checks(audit, events):
    runs = [e['body'] for e in events if e['kind'] == 'manufactured-run']
    cases = ('translation', 'principal-spin', 'motor-relaxation')
    audit.need([r['id'] for r in runs] == [case+'-h'+str(level) for case in cases for level in range(3)],
               'fixed-manufactured-run-order')
    reports = wiring_checks(audit, events)
    duration = audit.r(Fraction('0.01'))
    tolerances = {'position': Fraction(2, 10**12), 'velocity': Fraction(2, 10**12),
                  'attitude': Fraction(2, 10**10), 'omega': Fraction(2, 10**12), 'motor': Fraction(1, 10**8)}
    floor_squared = Fraction(1, 10**24)
    groups = {case: [] for case in cases}
    for run in runs:
        audit.s.guard(audit.ctx)
        case = run['caseId']; level = int(run['id'][-1]); count = 4*(2**level)
        initial, command = basic_values(audit, case)
        audit.need(run['schema'] == 'm31-manufactured-run-v1' and run['complete'] is True
                   and run['nativeCalls'] == 0 and run['reason'] is None and run['steps'] == count
                   and audit.d(run['durationWord']) == duration
                   and audit.d(run['dtWord']) == audit.r(Fraction('0.0025')/(2**level)), 'analytic-grid-contract')
        audit.need(len(run['initial']) == 1 and run['initial'][0]['id'] == 11, 'analytic-initial-id')
        audit.equal(run['initial'][0]['stateWords'], initial, 'analytic-fixed-initial')
        audit.need(len(run['commandsWords']) == 1, 'analytic-command-count')
        audit.equal(run['commandsWords'][0], command, 'analytic-fixed-command')
        stage_events = [e['record'] for e in run['events'] if e['kind'] == 'stage']
        step_events = [e['record'] for e in run['events'] if e['kind'] == 'step']
        audit.need(len(run['events']) == 5*count and len(stage_events) == 4*count and len(step_events) == count,
                   'analytic-all-stage-counts')
        audit.need([e['kind'] for e in run['events']] == ['stage', 'stage', 'stage', 'stage', 'step']*count,
                   'analytic-event-order')
        current = run['initial']
        for step_index, step in enumerate(step_events):
            selected = stage_events[4*step_index:4*step_index+4]
            audit.need(step['arm'] == run['id'] and step['stepIndex'] == step_index
                       and step['dtWord'] == run['dtWord'], 'analytic-step-identity')
            for stage in selected:
                audit.stage(stage, manufactured=True)
                row = stage['records'][0]; load = audit.consumed(row)
                state = audit.vec(row['stateWords'], 17, 'analytic-state')
                audit.need(load['rotor'] == state[13:17]
                           and load['collective'] == audit.a.left_sum(state[13:17])
                           and load['worldForce'] == [0, 0, audit.mg]
                           and load['worldMoment'] == [0, 0, 0], 'independent-manufactured-load-law')
                audit.need(audit.d(stage['originalTimeWord']) == audit.d(stage['relativeTimeWord']), 'analytic-time-origin-zero')
            current = audit.step(step, selected, current, run['commandsWords'])
        audit.need(run['final'] == current, 'analytic-final-from-stage-chain')
        exact = [(x, x) for x in initial]
        if case == 'translation':
            exact[:3] = [(initial[k]+duration*initial[3+k],)*2 for k in range(3)]
        elif case == 'principal-spin':
            exact[8] = analytic_box('sin', duration/2); exact[9] = analytic_box('cos', duration/2)
        else:
            lo, hi = analytic_box('exp', -duration/audit.tau)
            delta = initial[13]-command[0]
            box = (command[0]+min(delta*lo, delta*hi), command[0]+max(delta*lo, delta*hi))
            exact[13:17] = [box]*4
        actual = audit.vec(current[0]['stateWords'], 17, 'analytic-final')
        errors = {}
        for name, start, stop in (('position', 0, 3), ('velocity', 3, 6), ('omega', 10, 13)):
            errors[name] = audit.a.squared_error(actual[start:stop], exact[start:stop], Fraction(1))
        plus = audit.a.squared_error(actual[6:10], exact[6:10], Fraction(1, 2))
        minus = audit.a.squared_error(actual[6:10], [(-hi, -lo) for lo, hi in exact[6:10]], Fraction(1, 2))
        errors['attitude'] = (min(plus[0], minus[0]), min(plus[1], minus[1]))
        motor = [audit.a.squared_error([actual[k]], [exact[k]], audit.mg/4) for k in range(13, 17)]
        errors['motor'] = (max(x[0] for x in motor), max(x[1] for x in motor))
        groups[case].append(errors)
    for case, errors in groups.items():
        gates = {}
        for name, tolerance in tolerances.items():
            coarse, medium, fine = [e[name] for e in errors]
            passed = (fine[1] <= tolerance*tolerance
                      and medium[1] <= max(floor_squared, coarse[0]/4)
                      and fine[1] <= max(floor_squared, medium[0]/4))
            gates[name] = {'passed': passed, 'squaredErrors': [audit.a.encoded_interval(*e[name]) for e in errors],
                           'finestTolerance': audit.a.encoded(tolerance), 'roundoffFloor': audit.a.encoded(Fraction(1, 10**12))}
        reports.append({'id': case, 'passed': all(g['passed'] for g in gates.values()),
                        'gates': gates, 'observedOrder': None, 'producerExactFinalUsed': False})
    return reports


def wiring_checks(audit, events):
    controls = [e['body'] for e in events if e['kind'] == 'wiring-control']
    expected_ids = ('null-load', 'tilted-unequal', 'nominal-yaw', 'motor-lag', 'reversed-load-ids',
                    'duplicate-load-id', 'missing-load-id', 'stale-stage-token', 'stale-raw-input',
                    'nonfinite-load', 'zero-quaternion', 'nonfinite-quaternion')
    audit.need([c['id'] for c in controls] == list(expected_ids), 'fixed-wiring-control-order')
    reasons = {'duplicate-load-id': 'native-load-id', 'missing-load-id': 'native-load-missing-id',
               'stale-stage-token': 'stale-stage-token', 'stale-raw-input': 'native-raw-binding',
               'nonfinite-load': 'native-load-shape', 'zero-quaternion': 'projection-quaternion',
               'nonfinite-quaternion': 'projection-state'}
    def saved_number(value):
        audit.need(isinstance(value, dict) and set(value) == {'binary64Word'}, 'snapshot-number')
        return audit.d(value['binary64Word'])
    def snapshot_words(values):
        return [v['binary64Word'] for v in values]
    reports = []
    for control in controls:
        identifier = control['id']; fixture = control['fixture']; raw = fixture['rawInput']['drones']
        audit.need(control['schema'] == 'm31-wiring-control-v1' and control['nativeCalls'] == 0, 'wiring-no-native-call')
        # The fixed negative witness may be malformed, but every unmodified
        # coordinate/ID is still bound to the prospective manufactured fixture.
        tilted = identifier in ('tilted-unequal', 'nominal-yaw', 'motor-lag')
        values, _ = basic_values(audit, 'translation')
        command = [audit.r(Fraction(v)) for v in ('0.07', '0.08', '0.09', '0.1')]
        if tilted:
            values[6:10] = [Fraction(0), audit.d('3fe6a09e667f3bcd'), Fraction(0), audit.d('3fe6a09e667f3bcd')]
            values[10:13] = [audit.r(Fraction(v)) for v in ('0.1', '-0.2', '0.3')]
            values[13:17] = [audit.r(Fraction(v)) for v in ('0.03', '0.04', '0.05', '0.06')]
        expected_raw = [{'id': 11, 'state': [audit.a.rounded_word(x) for x in values]}]
        if identifier in ('reversed-load-ids', 'duplicate-load-id', 'missing-load-id'):
            second, _ = basic_values(audit, 'translation')
            second[0] = Fraction(2); second[13] = audit.r(Fraction('0.05'))
            expected_raw.append({'id': 29, 'state': [audit.a.rounded_word(x) for x in second]})
        if identifier == 'zero-quaternion':
            expected_raw[0]['state'][6:10] = ['0000000000000000']*4
        elif identifier == 'nonfinite-quaternion':
            expected_raw[0]['state'][6] = '7ff0000000000000'
        audit.need(raw == expected_raw and fixture['commandsWords'] == [
            [audit.a.rounded_word(x) for x in command] for _ in raw]
            and fixture['contextToken'] == 'control-'+identifier, 'fixed-wiring-raw-command-fixture')
        if identifier in reasons:
            audit.need(control['expected'] == control['observed'] == 'rejected'
                       and control['reason'] == reasons[identifier] and control['records'] == [], 'fixed-rejection-reason')
            env = fixture['envelope']
            if identifier == 'zero-quaternion':
                witness = all(audit.d(word) == 0 for word in raw[0]['state'][6:10]) and env is None
            elif identifier == 'nonfinite-quaternion':
                witness = raw[0]['state'][6] == '7ff0000000000000' and env is None
            elif identifier == 'stale-stage-token':
                witness = env['contextToken'] != fixture['contextToken']
            elif identifier == 'stale-raw-input':
                witness = snapshot_words(env['result']['raw'][0]['state']) != env['inputWords']['drones'][0]['state']
            elif identifier == 'nonfinite-load':
                bits = int(env['result']['loads'][0]['worldForce'][0]['binary64Word'], 16)
                witness = ((bits >> 52) & 2047) == 2047
            else:
                ids = [saved_number(row['id']) for row in env['result']['loads']]
                witness = len(set(ids)) < len(ids) if identifier == 'duplicate-load-id' else set(ids) != set(r['id'] for r in raw)
            audit.need(witness, 'fixed-rejection-input-witness')
        else:
            audit.need(control['expected'] == control['observed'] == 'accepted' and control['reason'] is None,
                       'fixed-accepted-control')
            rows = control['records']
            audit.need([r['id'] for r in rows] == [r['id'] for r in raw], 'wiring-id-map')
            for index, row in enumerate(rows):
                audit.need(row['rawStateWords'] == raw[index]['state']
                           and row['commandsWords'] == fixture['commandsWords'][index], 'wiring-input-consumption')
                state, load, _derivative = audit.derivative(row)
                if identifier in ('tilted-unequal', 'nominal-yaw', 'motor-lag'):
                    expected = {'rotor': [audit.r(Fraction(x)) for x in ('0.02', '0.03', '0.04', '0.06')],
                                'collective': audit.r(Fraction('0.15')),
                                'worldForce': [audit.r(Fraction('0.15')), 0, 0],
                                'worldMoment': [0, audit.r(Fraction('-0.00028')), audit.r(Fraction('0.0014'))]}
                    audit.need(load == expected, 'tilted-fixed-prescribed-load')
                    body = audit.vec(row['bodyArmWords'], 3, 'tilted-body')
                    target = [Fraction('-0.0014'), Fraction('-0.00028'), Fraction(0)]
                    audit.need(sum((x-y)**2 for x, y in zip(body, target)) <= Fraction(1, 10**24), 'independent-tilted-frame-control')
                else:
                    audit.need(load == audit.nominal(state), 'independent-nominal-control-load')
                if identifier == 'nominal-yaw':
                    effective_yaw = audit.a.left_sum(audit.r(audit.r(audit.r(sign*audit.km)/audit.kf)*force)
                        for sign, force in zip((1, -1, 1, -1), load['rotor']))
                    audit.need(audit.d(row['nominalYawWord']) != effective_yaw, 'nominal-versus-effective-yaw-witness')
            if identifier == 'reversed-load-ids':
                ids = [saved_number(row['id']) for row in fixture['envelope']['result']['loads']]
                audit.need(ids == list(reversed([r['id'] for r in rows])), 'reversed-id-fixture-witness')
        reports.append({'id': identifier, 'passed': True, 'independentInputAndArithmeticCheck': True})
    return reports


def corruption_checks(audit, on, targets, events=None):
    """Fixed first-stage mutations; no search for an attractive scientific witness."""
    stage = on[0]; target = targets[stage['stageId']]; native = stage['native']
    reports = []
    for name in ('load-word', 'squared-force-law', 'body-frame-force', 'load-id-association'):
        changed = copy.deepcopy(native)
        changed['inputFileSha256'] = target['inputFileSha256']
        witness = True
        if name == 'load-word':
            changed['loads'][0]['rotor'][0] = '0000000000000000'
        elif name == 'squared-force-law':
            witness = any(0 < audit.d(z['x']) < 1 for s in changed['solution'] for z in s['rotors'])
            for index, solution in enumerate(changed['solution']):
                rotor = [audit.r(audit.r(audit.d(changed['prepared'][index]['forces'][r])*audit.d(z['x']))*audit.d(z['x']))
                         for r, z in enumerate(solution['rotors'])]
                for r, value in enumerate(rotor):
                    solution['rotors'][r]['T'] = audit.a.rounded_word(value)
                audit.a.set_load_words(changed, index, rotor)
        elif name == 'body-frame-force':
            witness = any(audit.d(p['axis'][0]) != 0 or audit.d(p['axis'][1]) != 0 for p in changed['prepared'])
            for load in changed['loads']:
                load['worldForce'] = ['0000000000000000', '0000000000000000', load['collective']]
        else:
            changed['loads'][0]['id'] = changed['loads'][1]['id']
        audit.need(witness, 'fixed-corruption-witness-unavailable:'+name)
        detected = False; reason = None
        try:
            checked = audit.a.audit_evidence(changed, target, 'F')
            category = 'worldForce' if name == 'body-frame-force' else 'rotor'
            detected = not checked['loadArithmetic']['passed'] and checked['loadArithmetic']['categoryFailureCounts'][category] > 0
            reason = 'independent-native-load-arithmetic'
        except audit.a.InvalidRecord as error:
            reason = str(error)
            detected = name == 'load-id-association' and reason == 'native-load-solution-ids'
        reports.append({'id': name, 'passed': detected, 'detection': reason})
    fixture = next(e['body']['records'][0] for e in events if e['kind'] == 'wiring-control' and e['body']['id'] == 'tilted-unequal')
    for name in ('double-force', 'missing-moment', 'wrong-frame', 'motor-state-overwrite'):
        row = copy.deepcopy(fixture)
        if name == 'double-force':
            row['consumed']['worldForceWords'] = [audit.a.rounded_word(2*audit.d(x)) for x in row['consumed']['worldForceWords']]
        elif name == 'missing-moment':
            row['consumed']['worldMomentWords'] = ['0000000000000000']*3
        elif name == 'wrong-frame':
            row['bodyArmWords'] = row['consumed']['worldMomentWords'][:]
        else:
            row['stateWords'][13:17] = row['consumed']['rotorWords'][:]
        audit.need(row != fixture, 'fixed-row-corruption-nondegenerate')
        detected = False; reason = None
        try:
            audit.derivative(row)
        except audit.a.InvalidRecord as error:
            reason = str(error)
            expected = {'double-force': 'total-load-derivative-arithmetic',
                        'missing-moment': 'world-to-body-moment-arithmetic',
                        'wrong-frame': 'world-to-body-moment-arithmetic',
                        'motor-state-overwrite': 'projection-divide-arithmetic'}
            detected = reason == expected[name]
        reports.append({'id': name, 'passed': detected, 'detection': reason})
    changed = copy.deepcopy(on[1])
    audit.need(on[1]['nativeInput'] != stage['nativeInput'], 'fixed-stale-stage-nondegenerate')
    changed['nativeInput'] = copy.deepcopy(stage['nativeInput'])
    detected = False; reason = None
    try:
        audit.stage(changed, targets[changed['stageId']])
    except audit.a.InvalidRecord as error:
        reason = str(error); detected = reason == 'stage-native-input-consumption'
    reports.append({'id': 'stale-stage', 'passed': detected, 'detection': reason})
    changed = copy.deepcopy(stage)
    changed['records'][0]['id'] = changed['records'][1]['id']
    detected = False; reason = None
    try:
        audit.stage(changed, target)
    except audit.a.InvalidRecord as error:
        reason = str(error); detected = reason == 'stage-stable-ids'
    reports.append({'id': 'consumed-id-association', 'passed': detected, 'detection': reason})
    return reports


def journal_checks(audit, events, initial):
    kinds = [e['kind'] for e in events]
    expected = ['source', 'factories', 'initial'] + ['wiring-control']*12
    for _case in range(3):
        expected += ['manufactured-run']*3 + ['manufactured-summary']
    for arm in ('coupled', 'off'):
        for step_index in range(8):
            if step_index in (0, 4):
                expected += ['controller']
            expected += ['stage']
            if arm == 'coupled' and step_index == 0:
                expected += ['raw-diagnostic']
            expected += ['stage']*3 + ['step', 'safety']
        expected += ['arm-summary']
    expected += ['driver-summary']
    audit.need(kinds == expected, 'complete-journal-prospective-order')
    source = events[0]['body']; compatibility = source['adapterControls']
    bundle_index_path = PACKAGE + '/source/source-bundle.json'
    audit.need(bundle_index_path in audit.ctx['pins'], 'bundle-index-pinned')
    bundle_index = audit.s.decode(audit.s.read_pin(audit.ctx['root'], audit.ctx['pins'][bundle_index_path]))
    audit.need(source['bundle'] == {k: bundle_index[k] for k in ('path', 'bytes', 'sha256')}
               and source['sources'] == bundle_index['sources'], 'browser-source-slice-provenance')
    bundle_bytes = audit.s.read_pin(audit.ctx['root'], source['bundle'])
    for source_pin in source['sources']:
        original = audit.s.read_pin(audit.ctx['root'], audit.ctx['pins'][source_pin['path']])
        audit.need(len(original) == source_pin['bytes'] and audit.s.sha(original) == source_pin['sha256']
                   and bundle_bytes[source_pin['offset']:source_pin['offset']+source_pin['bytes']] == original,
                   'executed-source-exact-original-slice')
    factories = events[1]['body']
    audit.need(len(factories['ids']) == len(set(factories['ids']))
               and set(factories['ids']) == {p['id'] for p in source['sources']}
               and factories['globalProcessModified'] is False and factories['globalBufferModified'] is False,
               'exact-factory-source-set')
    audit.need(source['verifiedBeforeFactoryExecution'] is True and source['nativeArithmetic'] is True
               and compatibility['executedGroups'] == compatibility['expectedGroups'] == 9
               and compatibility['executedChecks'] == compatibility['expectedChecks'] == 56
               and compatibility['beforeScientificFactories'] is True, 'browser-fixed-compatibility-counts')
    checks = [check for group in compatibility['groups'] for check in group['checks']]
    audit.need(len(checks) == 56 and all(check['pass'] is True for check in checks), 'browser-fixed-compatibility-results')
    first = events[2]['body']
    audit.need(first['schema'] == 'm31-coupled-initial-v1' and first['input'] == initial
               and audit.d(first['originalTimeWord']) == 5 and audit.d(first['relativeTimeWord']) == 0,
               'complete-saved-initial-input')
    summary = events[-1]['body']
    counts = {'coupledStages': 32, 'coupledCompleted': 32, 'primaryNativeCalls': 32,
              'offStages': 32, 'offCompleted': 32, 'offNativeCalls': 0, 'steps': 16,
              'controllers': 4, 'rawDiagnostics': 1, 'wiringControls': 12,
              'manufacturedRuns': 9, 'manufacturedSummaries': 3, 'manufacturedStages': 336}
    audit.need(summary['complete'] is True and summary['counts'] == counts
               and summary['failures'] == [] and summary['exactCounts'] is True, 'driver-count-accounting')
    for event in events:
        row = event['body']
        if event['kind'] == 'safety':
            audit.need(row['issues'] == [] and row['pass'] is True, 'source-safety-observation')
        elif event['kind'] == 'arm-summary':
            final_step = [e['body'] for e in events if e['kind'] == 'step' and e['body']['arm'] == row['arm']][-1]
            audit.need(row['complete'] is True and row['completedSteps'] == 8
                       and row['final'] == {'drones': [{'id': r['id'], 'state': r['stateWords']}
                                                     for r in final_step['final']]}, 'arm-summary-final-state-binding')
        elif event['kind'] == 'raw-diagnostic':
            stage = next(e['body'] for e in events if e['kind'] == 'stage' and e['body']['stageId'] == row['stageId'])
            audit.need(row['stageId'] == 'coupled-step0-k2' and row['nativeCalls'] == row['referenceCalls'] == 0
                       and row['fullPreparationAttempted'] is False and row['admissionConclusion'] is None
                       and len(row['records']) == 64 and audit.d(row['qToleranceWord']) == audit.r(Fraction('1e-10')),
                       'raw-prerequisite-diagnostic-scope')
            for diagnostic, consumed in zip(row['records'], stage['records']):
                audit.need(diagnostic['id'] == consumed['id']
                           and diagnostic['rawStateWords'] == consumed['rawStateWords']
                           and diagnostic['normSquareWord'] == consumed['normSquareWord']
                           and diagnostic['normWord'] == consumed['normWord'], 'raw-diagnostic-stage-binding')
                defect = abs(audit.r(audit.d(diagnostic['normWord'])-1))
                audit.need(audit.d(diagnostic['defectWord']) == defect
                           and diagnostic['passesNormPrerequisite'] == (defect <= audit.r(Fraction('1e-10'))),
                           'raw-diagnostic-exact-arithmetic')
    return counts


def controller_bindings(audit, control):
    """Independent neighbor geometry and elementary target arithmetic; no trig oracle."""
    rows = control['records']; states = [audit.vec(r['stateWords'], 17, 'controller-state') for r in rows]
    radius = audit.r(Fraction('1.8')); squared_radius = radius*radius
    margin = squared_radius/Fraction(1 << 40)
    for i, (row, state) in enumerate(zip(rows, states)):
        expected = []
        for j, other in enumerate(states):
            if i == j:
                continue
            differences = [audit.r(x-y) for x, y in zip(state[:3], other[:3])]
            distance_squared = sum(x*x for x in differences)
            audit.need(abs(distance_squared-squared_radius) > margin, 'neighbor-radius-comparison-unresolved')
            if distance_squared < squared_radius:
                expected.append(rows[j]['id'])
        audit.need(row['neighborIds'] == expected, 'independent-controller-neighbor-ids')
        velocity = audit.vec(row['desiredVelocityWords'], 3, 'desired-velocity')
        target = row['target']
        audit.need(audit.d(target['vxWord']) == velocity[0] and audit.d(target['vyWord']) == velocity[1],
                   'controller-target-velocity-binding')
        z = audit.r(state[2]+audit.r(audit.r(audit.r(Fraction(5, 2)*velocity[2])
                            +audit.r(Fraction(3, 2)*state[5]))/6))
        audit.need(audit.d(target['zWord']) == z, 'controller-target-z-arithmetic')
        audit.d(target['yawWord']); audit.vec(row['desiredQuaternionWords'], 4, 'desired-quaternion')
        command = audit.vec(row['commandsWords'], 4, 'controller-command')
        maximum = audit.r(audit.r(audit.r(Fraction(9, 4)*audit.m)*audit.g)/4)
        audit.need(all(0 <= value <= maximum for value in command) and type(row['saturated']) is bool,
                   'controller-command-clamp-domain')


def feedback_checks(audit, stages, steps, controllers):
    on = [s for s in stages if s['arm'] == 'coupled']
    off = [s for s in stages if s['arm'] == 'off']
    audit.need(on[0]['nativeInput'] == off[0]['nativeInput'], 'matched-initial-stage')
    on_c = [c for c in controllers if c['arm'] == 'coupled']
    off_c = [c for c in controllers if c['arm'] == 'off']
    audit.need([r['commandsWords'] for r in on_c[0]['records']] == [r['commandsWords'] for r in off_c[0]['records']],
               'matched-initial-controller-commands')
    affected = [r['id'] for r in on[0]['records'] if r['consumed']['rotorWords'] != r['nominalMotorWords']]
    derivative_difference = [a['id'] for a, b in zip(on[0]['records'], off[0]['records'])
                             if a['derivativeWords'] != b['derivativeWords']]
    second_stage_difference = [a['id'] for a, b in zip(on[1]['records'], off[1]['records'])
                               if a['rawStateWords'] != b['rawStateWords']]
    controller_state_difference = [a['id'] for a, b in zip(on_c[1]['records'], off_c[1]['records'])
                                    if a['stateWords'] != b['stateWords']]
    command_difference = [a['id'] for a, b in zip(on_c[1]['records'], off_c[1]['records'])
                          if a['commandsWords'] != b['commandsWords']]
    audit.need(affected and derivative_difference and second_stage_difference
               and controller_state_difference and command_difference, 'nonzero-effect-through-second-control')
    return {'passed': True, 'initialLoadAffectedIds': affected, 'initialDerivativeDifferentIds': derivative_difference,
            'firstRawK2DifferentIds': second_stage_difference, 'secondControllerInputDifferentIds': controller_state_difference,
            'secondControllerCommandDifferentIds': command_difference,
            'scope': 'Exact saved word differences and the checked recurrence establish this continuation feedback; no trajectory or physical validity bound.'}


def main(root, expected, commit):
    support, ctx = bootstrap(root, expected, commit)
    result = {'schema': 'm31-coupled-stage-check-v1', 'sourceCommit': commit,
              'sourceManifestSha256': expected, 'complete': False, 'passed': False,
              'stages': [], 'controls': [], 'corruptions': [], 'errors': []}
    code = 1
    try:
        audit = StageAudit(support, ctx)
        browser, events = support.closed_browser(ctx)
        audit.browser = browser
        references = support.load(ctx['package'] / 'results/reference.json')
        audit.need(references['complete'] is True and references['qualified'] is True
                   and references['sourceCommit'] == commit and references['sourceManifestSha256'] == expected,
                   'complete-reference-index')
        reference_events = support.journal(ctx, references)
        audit.need(len(reference_events) == 32, 'reference-record-count')
        targets, reports = {}, {}
        suffix_calls = 0
        stages = [e['body'] for e in events if e['kind'] == 'stage']
        steps = [e['body'] for e in events if e['kind'] == 'step']
        audit.need(len(stages) == 64 and len(steps) == 16, 'primary-off-exact-stage-step-counts')
        on = [s for s in stages if s['arm'] == 'coupled']
        expected_ids = ['coupled-step%d-k%d' % (step, k) for step in range(8) for k in range(1, 5)]
        audit.need([s['stageId'] for s in on] == expected_ids, 'primary-stage-order')
        audit.need(set(browser['inputs']) == set(expected_ids), 'all-actual-stage-input-sidecars')
        for stage, event in zip(on, reference_events):
            support.guard(ctx)
            descriptor = event['body']
            audit.need(event['kind'] == 'reference' and descriptor['stageId'] == stage['stageId'], 'reference-stage-order')
            record = support.decode(support.read_pin(root, descriptor['reference']))
            audit.need(descriptor['inputSha256'] == record['inputSha256']
                       and descriptor['status'] == record['referenceStatus'] == 'admitted'
                       and descriptor['branch'] == record['branch'] == 'loads'
                       and descriptor['reuseCounters'] == record['reuseCounters'], 'reference-descriptor-binding')
            target, coverage = audit.target(stage, record, references['constants'])
            suffix_calls += coverage['scalarPairs']
            targets[stage['stageId']] = target
            report = audit.stage(stage, target)
            report['coverage'] = coverage
            reports[stage['stageId']] = report
        audit.need(references['attempted'] == references['completed'] == 32
                   and references['logicalPairs'] == 516096
                   and references['suffixCalls'] == suffix_calls <= 516096, 'reference-index-work-accounting')
        result['referenceAccounting'] = {'calls': 32, 'logicalPairs': 516096, 'suffixCalls': suffix_calls,
                                         'preparedDrones': 2048, 'rootBoxes': 8192, 'signedLoadBoxes': 22528}
        for stage in stages:
            if stage['arm'] == 'off':
                reports[stage['stageId']] = audit.stage(stage)
        initial = support.decode(support.read_pin(root, ctx['pins'][support.FRESH + '/results/inputs/fresh-a-t5.json']))
        audit.need(set(initial) == {'drones'}, 'initial-raw-format')
        result['runtimeCounts'] = journal_checks(audit, events, initial)
        start = [{'id': row['id'], 'stateWords': row['state']} for row in initial['drones']]
        controllers = [e['body'] for e in events if e['kind'] == 'controller']
        audit.need(len(controllers) == 4, 'exact-controller-update-count')
        for arm in ('coupled', 'off'):
            current = start
            arm_stages = [s for s in stages if s['arm'] == arm]
            arm_steps = [s for s in steps if s['arm'] == arm]
            controls = [c for c in controllers if c['arm'] == arm]
            audit.need(len(arm_stages) == 32 and len(arm_steps) == 8 and len(controls) == 2,
                       'each-arm-complete-counts')
            commands = None
            for step_index, step in enumerate(arm_steps):
                audit.need(step['stepIndex'] == step_index and audit.d(step['dtWord']) == audit.r(Fraction('0.0025')),
                           'fixed-eight-step-grid')
                if step_index in (0, 4):
                    control = controls[step_index//4]
                    audit.need(control['schema'] == 'm31-coupled-controller-v1'
                               and type(control['stepIndex']) is int and type(control['controlIndex']) is int
                               and control['stepIndex'] == step_index and control['controlIndex'] == step_index//4
                               and [{'id': r['id'], 'stateWords': r['stateWords']} for r in control['records']] == current,
                               'actual-evolved-controller-input')
                    commands = [r['commandsWords'] for r in control['records']]
                    controller_bindings(audit, control)
                    for command in commands:
                        audit.vec(command, 4, 'controller-output-words')
                    control_time = audit.r(step_index*audit.r(Fraction('0.0025')))
                    audit.need(audit.d(control['relativeTimeWord']) == control_time
                               and audit.d(control['originalTimeWord']) == audit.r(5+control_time), 'controller-original-time')
                chosen = arm_stages[4*step_index:4*step_index+4]
                for stage in chosen:
                    audit.need(audit.d(stage['originalTimeWord']) == audit.r(5+audit.d(stage['relativeTimeWord'])),
                               'absolute-stage-time-origin-five')
                current = audit.step(step, chosen, current, commands)
                t = audit.r(step_index*audit.d(step['dtWord']))
                audit.need(audit.d(step['originalTimeWord']) == audit.r(5+audit.r(t+audit.d(step['dtWord']))),
                           'absolute-endpoint-time-operation-order')
        result['feedback'] = feedback_checks(audit, stages, steps, controllers)
        result['stages'] = [reports[s['stageId']] for s in stages]
        result['arithmeticFixtures'] = audit.a.arithmetic_fixtures()
        audit.need(all(c['passed'] for c in result['arithmeticFixtures']), 'arithmetic-fixtures')
        result['controls'] = manufactured_checks(audit, events)
        result['counts'] = dict(audit.counts)
        before_mutations = dict(audit.counts)
        result['corruptions'] = corruption_checks(audit, on, targets, events)
        audit.need(all(c['passed'] for c in result['controls'] + result['corruptions']), 'all-fixed-controls')
        result['negativeControlAuditCounterDelta'] = {key: audit.counts[key]-before_mutations[key] for key in before_mutations}
        audit.need(result['counts']['stages'] == 400 and result['counts']['nativeReferences'] == 32
                   and result['counts']['steps'] == 100 and result['counts']['droneStages'] == 4438
                   and result['counts']['derivativeWords'] == 75446, 'independent-audit-work-counts')
        result['controllerScope'] = 'Frozen controller source provenance and actual state/command consumption; no independent transcendental controller oracle.'
        result['zeroSignPolicy'] = 'Literal source, stage, ID and consumed-load bindings preserve word strings. Reconstructed rational arithmetic identifies positive and negative zero; derivative zero-sign equality is not claimed.'
        result['complete'] = result['passed'] = True
        code = 0
    except Exception as error:
        result['errors'].append(support.public_error(error))
    finally:
        ctx['closing'] = True
        result['processLifetimePeakRssBytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['peakRssScope'] = 'macOS process lifetime only; not isolated stage or browser/process-tree aggregate, and not an OS memory limit.'
        try:
            support.verify_sources(ctx)
            result['sourcesPreserved'] = True
        except Exception:
            result['sourcesPreserved'] = result['passed'] = False
            result['errors'].append({'type': 'PreservationError', 'reason': 'source-preservation'})
            code = 1
        support.write(ctx, 'check.json', result)
    return code


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: check.py ROOT MANIFEST_SHA COMMIT')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]))
