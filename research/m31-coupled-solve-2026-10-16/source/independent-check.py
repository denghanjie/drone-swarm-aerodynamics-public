#!/usr/bin/env python3
"""Independent saved-record review. No candidate imports or data acquisition.

Source construction is not execution authorization. Invoke only after the
coordinator's source freeze and authorization of the single saved-evidence review.
Python stdlib; binary64 geometry and 80-digit Decimal nonlinear arithmetic.
"""
import argparse
import hashlib
import json
import math
import sys
import time
from decimal import Decimal, localcontext
from pathlib import Path

PRECISION = 80
MAX_OUTER = 160  # Prospective revision from 100, before any target execution.
MAX_INNER = 100
ROOT_RESIDUAL = Decimal('1e-65')
LOG_TARGET = Decimal('1e-40')
FORCE_RELATIVE = Decimal('1e-9')
IDS = ['level-ladder', 'tilted-ladder', 'hexagon-cycle', 'near-rejection']


def dec(value):
    return value if isinstance(value, Decimal) else Decimal(str(value))


def dot(a, b):
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def norm(a):
    return math.hypot(*a)


def unit(a):
    length = norm(a)
    return [x/length for x in a]


def subtract(a, b):
    return [x-y for x, y in zip(a, b)]


def constants():
    mg, arm, radius, rho = .027*9.81, .028, .023, 1.225
    area, corner_radius = math.pi*radius*radius, math.sqrt(2)*arm
    c = dict(D=2*corner_radius, decay=10.11, spread=.07668, origin=-5.817,
             minDown=2.5, neighbor=3., nearRad=.15, downFade=2., downCut=2.5,
             radFade=2., radCut=3., induced=math.sqrt(mg/(8*rho*area)),
             sqrt2minus1=math.sqrt(2)-1)
    return dict(mg=mg, arm=arm, radius=radius, rho=rho, A=area, R=corner_radius, c=c)


def square_vehicle(index, center, axis, c, corner=None):
    horizontal = cross([0., 0., 1.], axis)
    u = unit(horizontal) if norm(horizontal) > 1e-12 else [1., 0., 0.]
    if corner is not None:
        e = unit(corner)
        f = cross(axis, e)
        u = [(-e[k]+f[k])/math.sqrt(2) for k in range(3)]
    v = cross(axis, u)
    offsets = [[c['arm']*(s*u[k]+t*v[k]) for k in range(3)]
               for s, t in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    f0 = [(c['mg']/4)*(.8+.1*((index+2*r) % 5)) for r in range(4)]
    return dict(id=index, q=center, axis=axis, offsets=offsets, f0=f0, S0=sum(f0))


def fixture_definitions(c):
    level, tilted = [], []
    for i in range(8):
        level.append(square_vehicle(i, [0., 0., .4*i], [0., 0., 1.], c))
        angle = (-1)**i*math.pi/12
        tilted.append(square_vehicle(i, [.035*(-1)**i, .02*(i % 3), .4*i],
                                     [math.sin(angle), 0., math.cos(angle)], c))
    length = 2*math.sqrt(10)*c['R']
    centers = [[length*math.cos(i*math.pi/3), length*math.sin(i*math.pi/3), 0.]
               for i in range(6)]
    hexagon = []
    for i in range(6):
        tangent = subtract(centers[i], centers[(i-1) % 6])
        axis = [3/math.sqrt(10)*tangent[k]/length +
                (1/math.sqrt(10) if k == 2 else 0.) for k in range(3)]
        hexagon.append(square_vehicle(i, centers[i], axis, c))
    angle = math.pi/12
    near = [square_vehicle(0, [0., 0., 0.], [-math.sin(angle), 0., math.cos(angle)],
                           c, [-math.cos(angle), 0., -math.sin(angle)]),
            square_vehicle(1, [c['R'], 0., 0.], [math.sin(angle), 0., math.cos(angle)],
                           c, [math.cos(angle), 0., -math.sin(angle)])]
    return dict(zip(IDS, [level, tilted, hexagon, near]))


def fade(start, end, value):
    if value <= start:
        return 1.
    if value >= end:
        return 0.
    t = (value-start)/(end-start)
    return 1 - 3*t*t + 2*t*t*t


def independent_pair(vehicles, i, r, j, c):
    """Vector-form reconstruction of historical support, not its packed layout."""
    out = dict(symbol=0, term=0., down=0., radial=0., projection=0.,
               center=0., validity=0, stage=0)
    if i == j:
        out.update(symbol=1, validity=1)
        return out
    receiver, source = vehicles[i], vehicles[j]
    center_delta = subtract(source['q'], receiver['q'])
    out['center'] = norm(center_delta)
    out['validity'] |= 16
    if (not math.isfinite(out['center']) or out['center'] > 512 or
            max(map(abs, center_delta)) > 257):
        out.update(symbol=11, stage=3)
        return out
    if out['center'] >= c['neighbor']:
        out['symbol'] = 1
        out['validity'] |= 1
        return out
    rotor = [receiver['q'][k]+receiver['offsets'][r][k] for k in range(3)]
    d = subtract(source['q'], rotor)
    if not all(map(math.isfinite, d)) or max(map(abs, d)) > 258:
        out.update(symbol=11, stage=4)
        return out
    h = dot(d, source['axis'])
    out['down'] = h
    if not math.isfinite(h) or abs(h) > 1024:
        out.update(symbol=11, stage=4)
        return out
    out['validity'] |= 2
    if h <= 0 or h >= c['downCut']:
        out['symbol'] = 2 if h <= 0 else 3
        out['validity'] |= 1
        return out
    radial = norm([d[k]-h*source['axis'][k] for k in range(3)])
    out['radial'] = radial
    if not math.isfinite(radial) or radial > 2048:
        out.update(symbol=11, stage=4)
        return out
    out['validity'] |= 4
    if h < c['minDown']*c['D']:
        out['symbol'] = 4 if radial < c['nearRad'] else 5
        if out['symbol'] == 4:
            out['stage'] = 4
        else:
            out['validity'] |= 1
        return out
    downstream = h/c['D']
    width = c['spread']*(downstream-c['origin'])*c['D']
    if not width > 0 or not math.isfinite(width):
        out.update(symbol=11, stage=4)
        return out
    if radial >= c['radCut']*width:
        out['symbol'] = 6
        out['validity'] |= 1
        return out
    projection = max(0., dot(receiver['axis'], source['axis']))
    out['projection'] = projection
    out['validity'] |= 8
    xi = radial/width
    denominator = 1+c['sqrt2minus1']*xi*xi
    speed = (c['decay']/(downstream-c['origin']) / denominator**2 * c['induced'] *
             fade(c['downFade'], c['downCut'], h) *
             fade(c['radFade'], c['radCut'], radial/width) * projection)
    if not (math.isfinite(speed) and 0 <= speed <= 128 and math.isfinite(projection)):
        out.update(symbol=11, stage=4)
        return out
    out['term'] = speed
    out['validity'] |= 1
    out['symbol'] = 7 if projection <= 0 else (8 if speed > 0 else 9)
    return out


class Audit:
    def __init__(self):
        self.started = time.monotonic()
        self.checks = 0
        self.check_records = []
        self.failures = []
        self.case_reports = []

    def guard(self):
        if time.monotonic()-self.started >= 115:
            raise RuntimeError('independent review cooperative wall guard reached')

    def check(self, condition, label):
        self.checks += 1
        self.check_records.append(dict(name=label, passed=bool(condition)))
        if not condition:
            self.failures.append(label)

    def close(self, actual, expected, label):
        actual, expected = float(actual), float(expected)
        self.check(math.isfinite(actual) and math.isfinite(expected) and
                   abs(actual-expected) <= 2e-12+2e-12*abs(expected), label)

    def relative(self, actual, expected, label):
        actual, expected = dec(actual), dec(expected)
        self.check(actual.is_finite() and expected.is_finite() and expected > 0 and
                   abs(actual-expected) <= FORCE_RELATIVE*expected, label)


class DecimalSystem:
    def __init__(self, a, vehicles, audit):
        self.a = [[[dec(t) for t in row] for row in vehicle] for vehicle in a]
        self.f0 = [[dec(t) for t in vehicle['f0']] for vehicle in vehicles]
        self.s0 = [sum(row, Decimal(0)) for row in self.f0]
        self.n = len(vehicles)
        self.audit = audit
        self.root_calls = self.newton_updates = self.map_calls = 0

    def root(self, alpha):
        self.root_calls += 1
        if not alpha.is_finite() or alpha < 0:
            raise ValueError('invalid serialized-system alpha')
        if alpha == 0:
            return Decimal(1)
        x = min(Decimal(1), Decimal(1)/alpha)
        for unused in range(MAX_INNER):
            # Newton rearranged to avoid subtracting two nearly equal values.
            x = (2*x*x*x+1)/(3*x*x+alpha)
            self.newton_updates += 1
            if not (x.is_finite() and 0 < x <= 1):
                raise ArithmeticError('Decimal Newton left positive root domain')
            if abs(x*x*x+alpha*x-1) <= ROOT_RESIDUAL:
                return x
        raise ArithmeticError('Decimal Newton exhausted frozen inner cap')

    def evaluate(self, y):
        self.audit.guard()
        self.map_calls += 1
        y = [dec(t) for t in y]
        if len(y) != self.n or not all(t.is_finite() and 0 < t <= 1 for t in y):
            raise ValueError('invalid positive amplitude cube state')
        mapped, rotors = [], []
        for i in range(self.n):
            row = []
            for r in range(4):
                alpha = sum((self.a[i][r][j]*y[j] for j in range(self.n)), Decimal(0))
                x = self.root(alpha)
                row.append(dict(alpha=alpha, x=x, T=self.f0[i][r]*x))
            mapped.append((sum((z['T'] for z in row), Decimal(0))/self.s0[i]).sqrt())
            rotors.append(row)
        return dict(y=mapped, rotors=rotors)

    @staticmethod
    def log_distance(a, b):
        return max(abs(dec(x).ln()-dec(y).ln()) for x, y in zip(a, b))

    def solve(self):
        y = [Decimal(1)]*self.n
        changes = []
        for iteration in range(1, MAX_OUTER+1):
            result = self.evaluate(y)
            change = self.log_distance(y, result['y'])
            changes.append(change)
            y = result['y']
            if change <= LOG_TARGET:
                break
        final = self.evaluate(y)
        residual = self.log_distance(y, final['y'])
        return dict(y=y, map=final, iterations=iteration, residual_log=residual,
                    converged=residual <= LOG_TARGET, step_history=changes)


def float_vehicles(vehicles):
    return [dict(id=int(v['id']), q=list(map(float, v['q'])), axis=list(map(float, v['axis'])),
                 offsets=[list(map(float, o)) for o in v['offsets']],
                 f0=list(map(float, v['f0'])), S0=float(v['S0'])) for v in vehicles]


def check_vehicle(saved, expected, audit, prefix, c):
    audit.check(saved['id'] == expected['id'], prefix+' id')
    for field in ['q', 'axis', 'f0']:
        audit.check(len(saved[field]) == len(expected[field]), prefix+' '+field+' shape')
        for k, (x, y) in enumerate(zip(saved[field], expected[field])):
            audit.close(x, y, prefix+' '+field+' '+str(k))
    audit.check(len(saved['offsets']) == 4, prefix+' rotor count')
    for r, (got, want) in enumerate(zip(saved['offsets'], expected['offsets'])):
        audit.check(len(got) == 3, prefix+' offset dimension')
        for k in range(3):
            audit.close(got[k], want[k], prefix+' offset '+str((r, k)))
        audit.check(abs(dot(got, saved['axis'])) <= 1e-12, prefix+' perpendicular offset')
        audit.check(abs(norm(got)-c['R']) <= 1e-12, prefix+' offset norm')
    audit.check(abs(norm(saved['axis'])-1) <= 1e-12, prefix+' unit axis')
    audit.check(all(x > 0 and math.isfinite(x) for x in saved['f0']), prefix+' positive f0')
    audit.close(saved['S0'], sum(saved['f0']), prefix+' nominal total')


def check_work(saved, count, n, active_rows, positive_terms, audit, label):
    expected = dict(rootClosures=count*4*n, bisectionIterations=count*56*active_rows,
                    positiveTermMultiplications=count*positive_terms)
    for key, value in expected.items():
        audit.check(saved[key] == value, label+' '+key)


def check_map(saved, reference, audit, label):
    audit.check(len(saved['y']) == len(reference['y']), label+' y count')
    audit.check(len(saved['rotors']) == len(reference['rotors']), label+' rotor row count')
    for i in range(len(reference['y'])):
        audit.relative(saved['y'][i], reference['y'][i], label+' amplitude '+str(i))
        audit.check(len(saved['rotors'][i]) == 4, label+' four roots')
        for r in range(4):
            got, expected = saved['rotors'][i][r], reference['rotors'][i][r]
            audit.close(got['alpha'], expected['alpha'], label+' alpha '+str((i, r)))
            audit.relative(got['x'], expected['x'], label+' root '+str((i, r)))
            audit.relative(got['T'], expected['T'], label+' force '+str((i, r)))


def review_case(saved, expected, c, audit):
    name, n = saved['id'], len(expected)
    failures_before_geometry = len(audit.failures)
    audit.guard()
    vehicles = float_vehicles(saved['vehicles'])
    audit.check(len(vehicles) == n, name+' vehicle count')
    for i in range(n):
        check_vehicle(vehicles[i], expected[i], audit, name+' vehicle '+str(i), c)
    pairs = {(int(p['i']), int(p['r']), int(p['j'])): p for p in saved['pairs']}
    audit.check(len(pairs) == len(saved['pairs']) == 4*n*(n-1), name+' pair coverage')
    expected_a = [[[0.]*n for r in range(4)] for i in range(n)]
    expected_edges, unsupported = set(), []
    max_cap, positive_terms = 0., 0
    for i in range(n):
        for r in range(4):
            for j in range(n):
                if i == j:
                    continue
                key = (i, r, j)
                got, term = pairs[key], independent_pair(vehicles, i, r, j, c['c'])
                for field in ['symbol', 'validity', 'stage']:
                    audit.check(got[field] == term[field], name+' pair '+str(key)+' '+field)
                for field in ['term', 'down', 'radial', 'projection', 'center']:
                    audit.close(got[field], term[field], name+' pair '+str(key)+' '+field)
                audit.close(got['K'], term['term'], name+' coefficient K '+str(key))
                if term['symbol'] in [4, 11]:
                    unsupported.append((i, r, j, term['symbol']))
                scaled = term['term']*math.sqrt(vehicles[j]['S0']/c['mg'])
                max_cap = max(max_cap, scaled)
                audit.check(math.isfinite(scaled) and 0 <= scaled <= 128,
                            name+' whole-cube pair cap '+str(key))
                expected_a[i][r][j] = scaled/math.sqrt(vehicles[i]['f0'][r]/(2*c['rho']*c['A']))
                if term['term'] > 0:
                    positive_terms += 1
                    expected_edges.add((j, i))
    audit.check(len(saved['a']) == n, name+' coefficient vehicle dimension')
    for i in range(n):
        audit.check(len(saved['a'][i]) == 4, name+' coefficient rotor dimension')
        for r in range(4):
            audit.check(len(saved['a'][i][r]) == n, name+' coefficient source dimension')
            for j in range(n):
                audit.close(saved['a'][i][r][j], expected_a[i][r][j], name+' a '+str((i, r, j)))
                audit.check(dec(saved['a'][i][r][j]).is_finite() and saved['a'][i][r][j] >= 0,
                            name+' finite nonnegative a')
    edges = sorted(expected_edges)
    audit.check(saved['graph']['edges'] == [list(e) for e in edges], name+' graph edges')
    order = sorted(range(n), key=lambda i: (-vehicles[i]['q'][2], i))
    audit.check(saved['graph']['order'] == order, name+' descending order')
    positions = {i: k for k, i in enumerate(order)}
    eligible = all(positions[j] < positions[i] for j, i in edges)
    audit.check(saved['graph']['descendingEligible'] == eligible, name+' direct eligibility')
    audit.check(saved['geometryWork']['pairCalls'] == 4*n*(n-1), name+' geometry work')
    audit.check(saved['geometryWork']['positiveRotorTerms'] == positive_terms, name+' positive term count')
    audit.close(saved['admission']['scaledCapMax'], max_cap, name+' maximum scaled cap')
    error_pairs = sorted((int(e['i']), int(e['r']), int(e['j']), int(e['symbol']))
                         for e in saved['admission']['errors'] if e['kind'] == 'unsupported-pair')
    audit.check(error_pairs == sorted(unsupported), name+' unsupported record')
    audit.check(all(e['kind'] == 'unsupported-pair' for e in saved['admission']['errors']),
                name+' no unexplained admission error')
    admitted = not unsupported
    audit.check(saved['admission']['admitted'] == admitted, name+' admission status')
    lmax = max(sum(row) for vehicle in expected_a for row in vehicle)/(4*math.sqrt(2))
    audit.close(saved['ordinaryLmax'], lmax, name+' ordinary Lmax')
    report = dict(id=name, independent_geometry_admitted=admitted, pair_calls=4*n*(n-1),
                  positive_rotor_terms=positive_terms, unique_edges=len(edges),
                  independent_descending_eligible=eligible, ordinary_Lmax=lmax)
    audit.case_reports.append(report)
    if name == 'near-rejection':
        audit.check(not admitted, name+' deliberate rejection')
        audit.check(pairs[(0, 0, 1)]['symbol'] == pairs[(1, 0, 0)]['symbol'] == 4,
                    name+' both constructed corner predicates reject')
        audit.check(saved['solutions'] is None, name+' no solver after rejection')
        audit.check(saved['graph']['prescribedCyclePresent'] is None, name+' cycle flag')
        return
    audit.check(admitted, name+' intended admissible fixture')
    if not admitted:
        audit.check(saved['solutions'] is None, name+' no solver after unsupported geometry')
        return
    audit.check(positive_terms > 0, name+' nonzero influence')
    if name.endswith('ladder'):
        audit.check(eligible, name+' theorem descending DAG')
        audit.check(all(vehicles[j]['q'][2] > vehicles[i]['q'][2] for j, i in edges),
                    name+' strict positive center height for every edge')
        audit.check(all(v['axis'][2] >= math.cos(math.pi/4) for v in vehicles),
                    name+' 45-degree sufficient domain')
        audit.check(saved['graph']['prescribedCyclePresent'] is None, name+' cycle flag')
    else:
        cycle = all((j, (j-1) % 6) in expected_edges for j in range(6))
        audit.check(cycle and saved['graph']['prescribedCyclePresent'] is True, name+' six-edge cycle')
        audit.check(all(pairs[((j-1) % 6, r, j)]['K'] > 0 for j in range(6) for r in range(4)),
                    name+' cycle at all four receiver rotors')
        audit.check(not eligible, name+' descending pass ineligible')
    if len(audit.failures) != failures_before_geometry:
        report['reference_skipped'] = 'geometry, coefficient, admission or theoretical-graph checks failed'
        return
    system = DecimalSystem(saved['a'], saved['vehicles'], audit)
    reference = system.solve()
    audit.check(reference['converged'], name+' Decimal residual target within frozen cap')
    report['decimal_reference'] = reference
    active_rows = sum(any(dec(t) > 0 for t in row) for v in saved['a'] for row in v)
    solutions = saved['solutions']
    initial_map = system.evaluate([Decimal(1)]*n)
    check_map(solutions['uncoupled']['map'], initial_map, audit, name+' uncoupled')
    check_work(solutions['uncoupled']['work'], 1, n, active_rows, positive_terms, audit, name+' uncoupled work')
    picard = solutions['picard']
    iterates, iterations = picard['iterates'], int(picard['iterations'])
    audit.check(1 <= iterations <= 64 and len(iterates) == iterations+1, name+' Picard cap and trace length')
    audit.check(iterates[0] == [1]*n, name+' Picard initial state')
    audit.check(iterates[-1] == picard['y'], name+' final state equals trace terminal')
    for k in range(iterations):
        next_map = initial_map if k == 0 else system.evaluate(iterates[k])
        for i in range(n):
            audit.relative(iterates[k+1][i], next_map['y'][i], name+' Picard transition '+str((k, i)))
        delta = max(abs(math.log(float(x))-math.log(float(y))) for x, y in zip(iterates[k], iterates[k+1]))
        if k < iterations-1:
            audit.check(delta > 1e-11-3e-15, name+' no skipped Picard stop '+str(k))
        else:
            audit.check(delta <= 1e-11+3e-15, name+' terminal Picard stop')
    audit.check(picard['converged'] is True, name+' candidate convergence flag')
    check_work(picard['work'], iterations, n, active_rows, positive_terms, audit, name+' Picard work')
    check_work(picard['residualWork'], 1, n, active_rows, positive_terms, audit, name+' Picard residual work')
    if eligible:
        audit.check(solutions['direct'] is not None, name+' direct solve present')
    else:
        audit.check(solutions['direct'] is None, name+' no direct solve on cycle')
    final_reports = {}
    for method in ['picard', 'direct']:
        result = solutions[method]
        if result is None:
            continue
        final_map = system.evaluate(result['y'])
        check_map(result['residualMap'], final_map, audit, name+' '+method+' final residual map')
        residual = system.log_distance(result['y'], final_map['y'])
        audit.close(result['residualLog'], residual, name+' '+method+' residual log')
        max_force_error = Decimal(0)
        for i in range(n):
            audit.relative(result['y'][i], reference['y'][i], name+' '+method+' reference amplitude '+str(i))
            for r in range(4):
                got = dec(result['residualMap']['rotors'][i][r]['T'])
                want = reference['map']['rotors'][i][r]['T']
                audit.relative(got, want, name+' '+method+' reference force '+str((i, r)))
                max_force_error = max(max_force_error, abs(got-want)/want)
        if method == 'direct':
            check_map(dict(y=final_map['y'], rotors=result['rotors']), final_map, audit, name+' direct stored loads')
            check_work(result['work'], 1, n, active_rows, positive_terms, audit, name+' direct work')
            check_work(result['residualWork'], 1, n, active_rows, positive_terms, audit, name+' direct residual work')
            for i in range(n):
                audit.relative(result['y'][i], picard['y'][i],
                               name+' direct versus simultaneous amplitude '+str(i))
                for r in range(4):
                    audit.relative(result['rotors'][i][r]['T'], reference['map']['rotors'][i][r]['T'],
                                   name+' direct stored reference force '+str((i, r)))
                    audit.relative(result['rotors'][i][r]['T'],
                                   picard['residualMap']['rotors'][i][r]['T'],
                                   name+' direct versus simultaneous force '+str((i, r)))
        consistency = max(abs(system.s0[i]*dec(result['y'][i])**2 -
                              sum((t['T'] for t in final_map['rotors'][i]), Decimal(0))) for i in range(n))
        final_reports[method] = dict(high_precision_log_residual=residual,
                                    theoretical_log_error_estimate=2*residual,
                                    theoretical_rotor_relative_error_estimate=(2*residual).exp()-1,
                                    maximum_saved_rotor_relative_difference=max_force_error,
                                    maximum_source_receiver_total_mismatch_N=consistency,
                                    interpretation='80-digit numerical estimates; not outward-rounded certificates')
    report['candidate_final_checks'] = final_reports
    report['uncoupled_maximum_rotor_relative_difference'] = max(
        abs(initial_map['rotors'][i][r]['T']-reference['map']['rotors'][i][r]['T']) /
        reference['map']['rotors'][i][r]['T'] for i in range(n) for r in range(4))
    report['independent_work'] = dict(decimal_root_closures=system.root_calls,
                                      decimal_newton_updates=system.newton_updates,
                                      decimal_map_evaluations=system.map_calls)


def reject_constant(value):
    raise ValueError('non-finite JSON constant: '+value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    audit, raw, fatal = Audit(), b'', None
    with localcontext() as context:
        context.prec = PRECISION
        try:
            raw = args.input.read_bytes()
            data = json.loads(raw, parse_float=Decimal, parse_constant=reject_constant)
            audit.check(data['kind'] == 'four-rotor-static-coupling-development-verification', 'record kind')
            c = constants()
            for key in ['mg', 'arm', 'radius', 'rho', 'A', 'R']:
                audit.close(data['constants'][key], c[key], 'constant '+key)
            for key, value in c['c'].items():
                audit.close(data['constants']['c'][key], value, 'pair constant '+key)
            expected = fixture_definitions(c)
            audit.check([case['id'] for case in data['cases']] == IDS, 'exact frozen fixture list')
            for case in data['cases']:
                review_case(case, expected[case['id']], c, audit)
            audit.check(data['candidatePass'] is True, 'candidate-only gate result')
        except Exception as exc:
            fatal = type(exc).__name__+': '+str(exc)
            audit.check(False, 'review terminated: '+fatal)
        output = dict(kind='independent-four-rotor-coupling-saved-review',
                      passed=not audit.failures, checks=audit.check_records,
                      check_count=audit.checks, failures=audit.failures,
                      fatal=fatal, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      input_sha256=hashlib.sha256(raw).hexdigest(), python=sys.version.split()[0],
                      precision=PRECISION, outer_cap=MAX_OUTER, inner_cap=MAX_INNER,
                      reference_log_target=str(LOG_TARGET), root_residual_target=str(ROOT_RESIDUAL),
                      coefficient_tolerance='2e-12 absolute + 2e-12 relative',
                      force_relative_tolerance=str(FORCE_RELATIVE),
                      stop_reconstruction_absolute_allowance=3e-15,
                      wall_seconds=time.monotonic()-audit.started, cases=audit.case_reports,
                      limits='Binary64 independent geometry; Decimal80 numerical roots, not interval arithmetic. '
                             'No physical validation, runtime benchmark, GPU or 5000-drone claim.')
        with args.output.open('x') as stream:
            json.dump(output, stream, indent=2, default=str, allow_nan=False)
            stream.write('\n')
    print(json.dumps(dict(passed=not audit.failures, checks=audit.checks,
                          failures=len(audit.failures), fatal=fatal)))
    return 0 if not audit.failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
