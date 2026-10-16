#!/usr/bin/env python3
"""Independent saved force/moment ablation review; no trajectory integration."""
import hashlib
import importlib.util
import json
import math
import pathlib
import resource
import sys
import time
import warnings

try:
    import numpy as np
except Exception as dependency_error:
    print('independent review dependency unavailable: '+type(dependency_error).__name__, file=sys.stderr)
    sys.exit(2)

REFERENCE_SHA = '4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb'
MASS, GRAVITY, ARM, TAU = .027, 9.81, .028, .04
INERTIA = np.array([1.4e-5, 1.4e-5, 2.17e-5])
CORNERS = np.array([[ARM, ARM], [-ARM, ARM], [-ARM, -ARM], [ARM, -ARM]])
SPINS = np.array([1., -1., 1., -1.])
HOVER = MASS*GRAVITY/4
MAX_BYTES = 40*1024**2
COVERAGE_THRESHOLD = 1e-12
REFERENCE_TRIAL_PINS = [
    ('off', .005, 1897818, 'eca1e7332d43a1b273797f89d238fb536249811f814534da6c31d1f89cd177fd'),
    ('off', .0025, 2336210, '8c4b30ec74463c6e9aad25b66ddb4b8a877b627e4776011da4190d33e3645303'),
    ('off', .00125, 3224270, '03dc1f5a4b7074564ce4f820c31feb409a7e7eb49ede250e4bd539c8046e2ff0'),
    ('coupled', .005, 2232718, '341c0fcd9e796f316b528741bccc79b832032952e6e468ef7488645e571a9e5d'),
    ('coupled', .0025, 2782887, '70cbb865cdafa9946e808d84a894ef89b435cac1de496f28c2045f478ede19cf'),
    ('coupled', .00125, 3887942, '37fc64506929f0e5280bf4d3dc7b905532344583850cc1b95383bbf96652ce3f')]


class EvidenceError(Exception):
    pass


class Audit:
    def __init__(self):
        self.start = time.monotonic()
        self.checks = 0
        self.failures = []
        self.trials = []
        self.endpoints = 0
        self.saved_state_coverage = {}

    def guard(self):
        if time.monotonic()-self.start > 115:
            raise EvidenceError('review cooperative wall cap')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        if rss > 768*1024**2:
            raise EvidenceError('review RSS cap')

    def check(self, condition, name):
        self.checks += 1
        if not bool(condition):
            self.failures.append(name)

    def require(self, condition, name):
        self.check(condition, name)
        if not condition:
            raise EvidenceError(name)

    def close(self, actual, expected, name, atol=1e-9, rtol=1e-9):
        a, b = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
        ok = a.shape == b.shape
        error = None
        if ok:
            ok = np.all(np.isfinite(a)) and np.all(np.isfinite(b))
            if ok:
                error = float(np.max(np.abs(a-b), initial=0.))
                ok = np.all(np.abs(a-b) <= atol+rtol*np.abs(b))
        self.check(ok, name)
        return error


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def child(root, relative):
    p = pathlib.Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise EvidenceError('unsafe artifact path')
    full = (root/p).resolve()
    if not full.is_relative_to(root.resolve()):
        raise EvidenceError('artifact escapes package')
    return full


def read(path):
    if path.stat().st_size > MAX_BYTES:
        raise EvidenceError('oversized JSON artifact')
    return json.loads(path.read_text(), parse_constant=lambda _: (_ for _ in ()).throw(EvidenceError('nonfinite JSON token')))


def scientific_files(package):
    return [x for name in ['results','inputs','generation'] for x in (package/name).rglob('*') if x.is_file()]


def verify_pin(audit, package, pin, label):
    path = child(package, pin['path'])
    audit.require(path.is_file(), label+'.present')
    audit.check(path.stat().st_size == pin['bytes'], label+'.bytes')
    audit.check(digest(path) == pin['sha256'], label+'.sha256')
    return path


def rotate(q, vector):
    t = 2*np.cross(q[:3], vector)
    return vector + q[3]*t + np.cross(q[:3], t)


def record_state_coverage(audit, states, mode, require_witness):
    """Descriptive saved-state coverage only; no new campaign outcome gate."""
    kind = 'endpoint' if require_witness else 'captured-stage'
    key = (mode, kind)
    if key not in audit.saved_state_coverage:
        audit.saved_state_coverage[key] = dict(mode=mode, recordKind=kind, vehicleStates=0,
            nonzeroBodyRate=0, unequalNominalRotors=0, bodyRateAndUnequalNominalRotors=0,
            nonzeroNominalRollPitchTorque=0, bodyRateAndNominalRollPitchTorque=0)
    row = audit.saved_state_coverage[key]
    rates = np.linalg.norm(states[:,10:13], axis=1) > COVERAGE_THRESHOLD
    nominal = states[:,13:17]
    unequal = np.ptp(nominal, axis=1) > COVERAGE_THRESHOLD
    torque = np.column_stack((nominal @ CORNERS[:,1], -nominal @ CORNERS[:,0]))
    torque_nonzero = np.linalg.norm(torque, axis=1) > COVERAGE_THRESHOLD
    row['vehicleStates'] += len(states)
    for name, values in [('nonzeroBodyRate',rates), ('unequalNominalRotors',unequal),
                         ('bodyRateAndUnequalNominalRotors',rates & unequal),
                         ('nonzeroNominalRollPitchTorque',torque_nonzero),
                         ('bodyRateAndNominalRollPitchTorque',rates & torque_nonzero)]:
        row[name] += int(np.count_nonzero(values))


def body_fields(states, commands, forces, mode):
    """Keep modeled load correction separate from the torque actually applied."""
    modeled, applied, derivatives = [], [], []
    for state, command, thrust in zip(states, commands, forces):
        nominal, q, omega = state[13:17], state[6:10], state[10:13]
        delta = thrust-nominal
        delta_force = rotate(q, np.array([0., 0., math.fsum(delta)]))
        delta_torque = np.array([np.dot(CORNERS[:, 1], delta), -np.dot(CORNERS[:, 0], delta), 0.])
        torque_forces = nominal if mode == 'force-only' else thrust
        torque = np.array([np.dot(CORNERS[:, 1], torque_forces), -np.dot(CORNERS[:, 0], torque_forces),
                           (7.94e-12/3.16e-10)*np.dot(SPINS, nominal)])
        acceleration = rotate(q, np.array([0., 0., math.fsum(thrust)/MASS]))-np.array([0., 0., GRAVITY])
        dq = .5*np.r_[q[3]*omega+np.cross(q[:3], omega), -np.dot(q[:3], omega)]
        dw = (torque-np.cross(omega, INERTIA*omega))/INERTIA
        derivatives.append(np.r_[state[3:6], acceleration, dq, dw, (command-nominal)/TAU])
        modeled.append(dict(delta=delta, force=delta_force, torque=delta_torque))
        applied.append(dict(delta=delta, force=delta_force, torque=np.zeros(3) if mode == 'force-only' else delta_torque))
    return modeled, applied, np.asarray(derivatives)


def geometry(ref, states, audit):
    c = ref.constants()
    g = ref.prepare_geometry(states, c)
    n = len(states)
    symbols, sources, coeffs, offsets, deps = [], [], [], [0], []
    for i in range(n):
        audit.guard()
        classified, rows, _ = ref.classify_receiver(i, g, c)
        symbols.extend(classified.ravel().tolist())
        incoming = set()
        for ids, values in rows:
            sources.extend(ids.tolist())
            coeffs.extend(values.tolist())
            offsets.append(len(sources))
            incoming.update(ids.tolist())
        deps.append(incoming)
    sources = np.asarray(sources, dtype=int)
    coeffs = np.asarray(coeffs, dtype=float)
    offsets = np.asarray(offsets, dtype=int)
    counts = np.bincount(symbols, minlength=12)
    nominal_ok = np.all(g['f0'] > 0) and np.all(np.isfinite(g['S0']))
    valid_geometry = (np.all(np.isfinite(states)) and np.all(np.abs(g['qnorm']-1) <= 1e-10)
                      and np.all(np.abs(g['anorm']-1) <= 1e-9)
                      and np.all(np.abs(g['onorm']-c['D']/2) <= 1e-9)
                      and np.all(np.abs(g['perpendicular']) <= 1e-9))
    scaled = coeffs*np.sqrt(g['S0'][sources]/c['mg']) if nominal_ok else None
    scaling_ok = scaled is not None and np.all(np.isfinite(scaled) & (scaled <= 128))
    admitted = valid_geometry and nominal_ok and counts[4] == 0 and counts[11] == 0 and scaling_ok
    eligible = all(states[j, 2] > states[i, 2] or (states[j, 2] == states[i, 2] and j < i)
                   for i in range(n) for j in deps[i])
    a = None
    if nominal_ok:
        row_ids = np.repeat(np.arange(4*n), np.diff(offsets))
        a = scaled/np.sqrt(g['f0'].ravel()[row_ids]/(2*c['rho']*c['area']))
    return dict(g=g, c=c, symbols=symbols, sources=sources, K=coeffs, offsets=offsets, a=a,
                counts=counts, admitted=bool(admitted), eligible=bool(eligible),
                edges=sum(map(len, deps)), tilt=float(np.max(g['tilt'])*180/math.pi))


def solve(ref, geom, audit):
    """Independent descending evaluation with analytic positive cubic roots."""
    g, a, offsets, sources = geom['g'], geom['a'], geom['offsets'], geom['sources']
    n = len(g['f0'])
    y, alpha, roots = np.ones(n), np.zeros((n, 4)), np.ones((n, 4))
    order = sorted(range(n), key=lambda i: (-g['q'][i, 2], i))
    for i in order:
        audit.guard()
        for r in range(4):
            begin, end = offsets[4*i+r:4*i+r+2]
            alpha[i, r] = math.fsum(a[k]*y[sources[k]] for k in range(begin, end))
        roots[i] = ref.positive_root(alpha[i])
        y[i] = math.sqrt(math.fsum(g['f0'][i]*roots[i])/g['S0'][i])
    return y, alpha, roots, g['f0']*roots


def endpoint(audit, ref, sample, mode, n, cfg, label, require_witness=True):
    audit.guard()
    states = np.asarray(sample['states'], dtype=float)
    commands = np.asarray(sample['commands'], dtype=float)
    audit.require(states.shape == (n, 17) and commands.shape == (n, 4), label+'.state-command-shape')
    audit.require(np.all(np.isfinite(states)) and np.all(np.isfinite(commands)), label+'.finite-input')
    record_state_coverage(audit, states, mode, require_witness)
    audit.close(np.linalg.norm(states[:, 6:10], axis=1), np.ones(n), label+'.unit-quaternion', 1e-12, 0)
    audit.check(np.all(commands >= 0) and np.all(commands <= 2.25*HOVER+1e-12), label+'.command-range')
    info = sample['info']
    maximum = dict(coefficient=0., load=0., derivative=0.)
    if mode in ['coupled','force-only']:
        geom = geometry(ref, states, audit)
        audit.require(geom['admitted'] and geom['eligible'], label+'.independent-domain')
        w = sample.get('witness')
        if require_witness:
            audit.require(isinstance(w, dict), label+'.witness')
            audit.check(w['symbols'] == geom['symbols'], label+'.all-symbols-exact')
            audit.check(np.array_equal(w['offsets'], geom['offsets']), label+'.offsets-exact')
            audit.check(np.array_equal(w['sources'], geom['sources']), label+'.sources-exact')
            maximum['coefficient'] = audit.close(w['K'], geom['K'], label+'.coefficients', 2e-12, 2e-12)
            audit.close(w['a'], geom['a'], label+'.scaled-coefficients', 2e-12, 2e-12)
        y, alpha, roots, forces = solve(ref, geom, audit)
        if require_witness:
            audit.close(w['y'], y, label+'.source-amplitudes')
            for key, expected in [('alpha', alpha), ('x', roots), ('T', forces)]:
                audit.close([[rotor[key] for rotor in row] for row in w['rotors']], expected, label+'.rotor-'+key)
        saved_y = np.asarray(w['y'], dtype=float) if require_witness else y
        residual_alpha = np.zeros((n, 4))
        for row in range(4*n):
            begin, end = geom['offsets'][row:row+2]
            residual_alpha.flat[row] = math.fsum(geom['a'][k]*saved_y[geom['sources'][k]] for k in range(begin, end))
        residual_x = ref.positive_root(residual_alpha)
        totals = np.sum(geom['g']['f0']*residual_x, axis=1)
        residual_y = np.sqrt(totals/geom['g']['S0'])
        log_residual = float(np.max(np.abs(np.log(residual_y)-np.log(saved_y))))
        mismatch = float(np.max(np.abs(geom['g']['S0']*saved_y*saved_y-totals)/geom['g']['S0']))
        audit.check(log_residual <= cfg['residualLimit'] and mismatch <= cfg['sourceReceiverLimit'], label+'.independent-residual-limits')
        audit.check(0 <= info['residual'] <= cfg['residualLimit'] and 0 <= info['sourceReceiverMismatch'] <= cfg['sourceReceiverLimit'], label+'.reported-residual-limits')
        audit.close(info['residual'], log_residual, label+'.reported-residual')
        audit.close(info['sourceReceiverMismatch'], mismatch, label+'.reported-source-mismatch')
        audit.close(info['minRatio'], float(np.min(roots)), label+'.min-ratio')
        # acos loses resolution at upright; this diagnostic angle is not a load tolerance.
        audit.close(info['maxTiltDegrees'], geom['tilt'], label+'.max-tilt', 2e-6, 1e-9)
        audit.check(info['symbolCounts'] == geom['counts'].tolist(), label+'.symbol-census')
        audit.check(info['edges'] == geom['edges'] and info['positiveTerms'] == len(geom['K']), label+'.graph-counts')
        audit.check(info['admitted'] is True and info['descendingEligible'] is True, label+'.domain-flags')
    else:
        forces = states[:, 13:17]
        if require_witness:
            audit.check(sample['witness'] is None, label+'.off-no-witness')
        audit.check(info['edges'] == info['positiveTerms'] == info['residual'] == info['sourceReceiverMismatch'] == 0
                    and info['minRatio'] == 1 and info['symbolCounts'] is None
                    and info['admitted'] is True and info['descendingEligible'] is True, label+'.off-no-coupling')
        tilt = max(math.acos(float(np.clip(rotate(q, np.array([0., 0., 1.]))[2], -1, 1)))*180/math.pi for q in states[:, 6:10])
        audit.close(info['maxTiltDegrees'], tilt, label+'.off-max-tilt', 2e-6, 1e-9)
    maximum['load'] = audit.close(sample['forces'], forces, label+'.all-forces')
    modeled, applied, derivatives = body_fields(states, commands, forces, mode)
    audit.close(info['modeledTorqueMax'], max(np.linalg.norm(c['torque']) for c in modeled), label+'.modeled-torque-max')
    audit.close(info['appliedTorqueMax'], max(np.linalg.norm(c['torque']) for c in applied), label+'.applied-torque-max')
    for field, corrections in [('modeledCorrections',modeled),('corrections',applied)]:
        audit.require(len(sample[field]) == n, label+'.'+field+'-count')
        for i, correction in enumerate(corrections):
            for key in ['delta', 'force', 'torque']:
                audit.close(sample[field][i][key], correction[key], label+'.'+field+'-'+str(i)+'-'+key)
                if mode == 'force-only' and field == 'corrections' and key == 'torque':
                    audit.close(sample[field][i][key], [0.,0.,0.], label+'.applied-torque-exact-zero-'+str(i), 0, 0)
    maximum['derivative'] = audit.close(sample['derivatives'], derivatives, label+'.full17-derivative')
    if require_witness:
        audit.endpoints += 1
    return maximum


def project(states):
    out = np.asarray(states, dtype=float).copy()
    out[:, 6:10] /= np.linalg.norm(out[:, 6:10], axis=1)[:, None]
    return out


def captured_steps(audit, ref, record, case, mode, dt, cfg):
    """Recheck fixed saved stage states, then verify RK4 algebra from saved slopes."""
    total_steps = round(case['duration']/dt)
    captures = {}
    for k, stage in enumerate(record['stages']):
        step, sub = divmod(k, 4)
        expected = step in {0, total_steps-1} and stage['status'] == 'completed'
        audit.check(('witness' in stage) == expected, record['id']+'.stage-capture-policy-'+str(k))
        if not expected:
            continue
        witness = stage['witness']
        sample = dict(witness, info={key:value for key,value in stage.items() if key not in ['witness','t','stage','status']})
        endpoint(audit, ref, sample, mode, case['n'], cfg, record['id']+'.captured-stage-'+str(k), False)
        captures.setdefault(step, []).append(witness)
    steps = record['stepWitnesses']
    failed_projection = (record['failure'] or {}).get('stage')
    projection_step = None
    if failed_projection and failed_projection['stage'] == 'final-projection':
        projection_step = len(record['stages'])//4-1
    audit.check(len({x['step'] for x in steps}) == len(steps), record['id']+'.step-witness-unique')
    expected_steps = [step for step, stages in captures.items() if len(stages) == 4 and step != projection_step]
    audit.check([x['step'] for x in steps] == expected_steps, record['id']+'.step-witness-coverage')
    for step, stages in captures.items():
        records = [x for x in steps if x['step'] == step]
        step_record = records[0] if records else None
        base = np.asarray(step_record['initial'] if step_record else failed_projection['acceptedStart'] if step == projection_step else stages[0]['states'])
        if step_record:
            audit.check(step_record['t'] == step*dt and step_record['h'] == dt, record['id']+'.step-witness-time-'+str(step))
            audit.close(stages[0]['states'], project(base), record['id']+'.stage1-projection-'+str(step), 1e-12, 1e-12)
            audit.close(stages[0]['commands'], step_record['commands'], record['id']+'.step-witness-command-'+str(step), 1e-12, 0)
        if step == 0:
            audit.close(base, record['initial'], record['id']+'.first-step-base', 1e-12, 0)
        for j in range(len(stages)):
            raw = base if j == 0 else base + dt*([.5,.5,1][j-1])*np.asarray(stages[j-1]['derivatives'])
            norm_error = float(np.max(np.abs(np.linalg.norm(raw[:,6:10], axis=1)-1)))
            audit.close(record['stages'][4*step+j]['rawQuaternionNormMaxError'], norm_error,
                        record['id']+'.raw-quaternion-error-'+str(step)+'-'+str(j), 1e-12, 0)
        for j in range(1, len(stages)):
            prior = np.asarray(stages[j-1]['derivatives'])
            expected = project(base + dt*([.5, .5, 1][j-1])*prior)
            audit.close(stages[j]['states'], expected, record['id']+'.stage-assembly-'+str(step)+'-'+str(j+1), 1e-12, 1e-12)
            audit.close(stages[j]['commands'], stages[0]['commands'], record['id']+'.stage-held-command-'+str(step)+'-'+str(j+1), 1e-12, 0)
        if len(stages) == 4:
            ks = [np.asarray(x['derivatives']) for x in stages]
            raw_end = base + dt*(ks[0]+2*ks[1]+2*ks[2]+ks[3])/6
            if step == projection_step:
                actual = np.asarray(failed_projection['states'], dtype=float)
                audit.check(actual.shape == raw_end.shape and np.allclose(actual, raw_end, atol=1e-12, rtol=1e-12, equal_nan=True), record['id']+'.failed-final-assembly')
                continue
            end = project(raw_end)
            audit.require(step_record is not None, record['id']+'.accepted-step-witness-present')
            audit.close(step_record['final'], end, record['id']+'.saved-step-final-assembly-'+str(step), 1e-12, 1e-12)
            if step == total_steps-1 and record['complete']:
                audit.close(record['final'], end, record['id']+'.last-step-final-assembly', 1e-12, 1e-12)
    return sum(map(len, captures.values()))


def angle(a, b):
    a, b = np.asarray(a), np.asarray(b)
    sign = -1 if np.dot(a, b) < 0 else 1
    return 4*math.atan2(np.linalg.norm(a-sign*b), np.linalg.norm(a+sign*b))


def discrepancy(a, b):
    if not a['complete'] or not b['complete'] or len(a['samples']) != len(b['samples']):
        return None
    maxima = dict(position=0., velocity=0., attitude=0., rotor=0., bodyRate=0.)
    for x, y in zip(a['samples'], b['samples']):
        if x['t'] != y['t']:
            return None
        xs, ys = np.asarray(x['states']), np.asarray(y['states'])
        maxima['position'] = max(maxima['position'], float(np.max(np.linalg.norm(xs[:, :3]-ys[:, :3], axis=1))))
        maxima['velocity'] = max(maxima['velocity'], float(np.max(np.linalg.norm(xs[:, 3:6]-ys[:, 3:6], axis=1))))
        maxima['attitude'] = max(maxima['attitude'], max(angle(q, r) for q, r in zip(xs[:, 6:10], ys[:, 6:10])))
        maxima['bodyRate'] = max(maxima['bodyRate'], float(np.max(np.linalg.norm(xs[:, 10:13]-ys[:, 10:13], axis=1))))
        maxima['rotor'] = max(maxima['rotor'], float(np.max(np.abs(np.asarray(x['forces'])-y['forces'])))/HOVER)
    return maxima


def convergence(a, b, c, cfg):
    coarse, fine = discrepancy(a, b), discrepancy(b, c)
    if coarse is None or fine is None:
        return dict(pass_=False, coarseMedium=coarse, mediumFine=fine)
    gates = {}
    for key, tol in cfg['tolerances'].items():
        d, e = coarse[key], fine[key]
        tiny = d < tol*cfg['roundoffFraction'] and e < tol*cfg['roundoffFraction']
        gates[key] = dict(coarseMedium=d, mediumFine=e, tolerance=tol, bothTiny=tiny,
                          pass_=e <= tol and (tiny or e <= cfg['refinementRatio']*d))
    return dict(pass_=all(g['pass_'] for g in gates.values()), coarseMedium=coarse, mediumFine=fine, gates=gates)


def rename_pass(value):
    if isinstance(value, dict):
        return {('pass' if k == 'pass_' else k):rename_pass(v) for k, v in value.items()}
    if isinstance(value, list):
        return [rename_pass(v) for v in value]
    return value


def compare_tree(audit, saved, expected, label):
    if isinstance(expected, dict):
        audit.require(isinstance(saved, dict) and set(saved) == set(expected), label+'.keys')
        for key in expected:
            compare_tree(audit, saved[key], expected[key], label+'.'+key)
    elif isinstance(expected, list):
        audit.require(isinstance(saved, list) and len(saved) == len(expected), label+'.length')
        for i, (a, b) in enumerate(zip(saved, expected)):
            compare_tree(audit, a, b, label+'.'+str(i))
    elif isinstance(expected, float):
        audit.close(saved, expected, label, 1e-12, 1e-12)
    else:
        audit.check(saved == expected, label)


def trial(audit, ref, package, entry, case, mode, dt, cfg):
    ident = case['id']+'-'+mode+'-'+str(dt)
    audit.require(entry['id'] == ident, ident+'.entry-id')
    record = read(verify_pin(audit, package, entry['pin'], ident))
    audit.require(record['id'] == ident and record['case'] == case['id'] and record['mode'] == mode and record['dt'] == dt, ident+'.identity')
    audit.check(record['complete'] == entry['complete'], ident+'.completion-matches')
    audit.check(entry['failure'] == (record['failure']['kind'] if record['failure'] else None), ident+'.failure-matches')
    initial = np.asarray(record['initial'], dtype=float)
    audit.require(initial.shape == (case['n'], 17) and np.all(np.isfinite(initial)), ident+'.initial-shape')
    if case['command'] == 'fixed-nominal':
        expected = np.asarray([position+[0., 0., 0., 0., 0., 0., 1., 0., 0., 0.]+[HOVER]*4 for position in case['positions']])
        audit.close(initial, expected, ident+'.literal-initial', 1e-12, 0)
    if record['samples']:
        audit.check(record['samples'][0]['t'] == 0, ident+'.initial-sample')
        audit.close(record['samples'][0]['states'], initial, ident+'.initial-sample-state', 1e-12, 0)
    else:
        audit.require(not record['complete'] and record['failure'] and not record['stages'], ident+'.empty-samples-only-initial-failure')
    end = record['end']
    audit.check(math.isfinite(end) and 0 <= end <= case['duration']+1e-12, ident+'.end-range')
    if record['complete']:
        audit.check(record['failure'] is None and abs(end-case['duration']) <= 1e-12, ident+'.complete-horizon')
        expected_samples = round(case['duration']/cfg['sampleDt'])+1
        audit.require(len(record['samples']) == expected_samples, ident+'.complete-samples')
        audit.close(record['final'], record['samples'][-1]['states'], ident+'.final-sample-state', 1e-12, 0)
    else:
        audit.require(isinstance(record['failure'], dict), ident+'.failed-reason-present')
    errors = dict(coefficient=0., load=0., derivative=0.)
    for k, sample in enumerate(record['samples']):
        audit.check(abs(sample['t']-k*cfg['sampleDt']) <= 1e-12 and sample['t'] <= end+1e-12, ident+'.sample-time-'+str(k))
        result = endpoint(audit, ref, sample, mode, case['n'], cfg, ident+'.endpoint-'+str(k))
        for key, value in result.items():
            if value is not None:
                errors[key] = max(errors[key], value)
        if case['command'] == 'fixed-nominal':
            audit.close(sample['commands'], np.full((case['n'], 4), HOVER), ident+'.fixed-command-'+str(k), 1e-12, 0)
        # Samples at control boundaries preserve the command held over the preceding step.
        if record['controls']:
            eligible = [x for x in record['controls'] if x['t'] < sample['t']-1e-12 or sample['t'] == 0 and x['t'] == 0]
            if eligible:
                audit.close(sample['commands'], [x['u'] for x in eligible[-1]['values']], ident+'.held-command-'+str(k), 1e-12, 0)
    stages, controls = record['stages'], record['controls']
    total_steps = round(case['duration']/dt)
    audit.check(len(stages) <= total_steps*4, ident+'.stage-cap')
    rejected = [k for k,s in enumerate(stages) if s['status'] == 'rejected']
    audit.check(not rejected or rejected == [len(stages)-1], ident+'.only-terminal-stage-rejected')
    if record['complete']:
        audit.check(len(stages) == total_steps*4 and not rejected, ident+'.stage-count')
        audit.check(len(controls) == round(case['duration']/cfg['controlDt']), ident+'.control-count')
    for k, stage in enumerate(stages):
        if k % 256 == 0:
            audit.guard()
        step, sub = divmod(k, 4)
        expected_t = (step + [0, .5, .5, 1][sub])*dt
        audit.check(stage['stage'] == sub+1 and abs(stage['t']-expected_t) <= 1e-12, ident+'.stage-schedule-'+str(k))
        if stage['status'] == 'rejected':
            audit.check(record['failure'] is not None and stage['reason'] == record['failure']['kind'], ident+'.rejected-stage-reason')
            continue
        audit.require(stage['status'] == 'completed', ident+'.stage-status')
        audit.check(math.isfinite(stage['rawQuaternionNormMaxError']) and stage['rawQuaternionNormMaxError'] >= 0
                    and math.isfinite(stage['minRatio']) and 0 < stage['minRatio'] <= 1
                    and math.isfinite(stage['maxTiltDegrees']) and 0 <= stage['maxTiltDegrees'] <= 180,
                    ident+'.stage-diagnostic-domain-'+str(k))
        audit.check(math.isfinite(stage['modeledTorqueMax']) and stage['modeledTorqueMax'] >= 0
                    and math.isfinite(stage['appliedTorqueMax']) and stage['appliedTorqueMax'] >= 0,
                    ident+'.stage-torque-diagnostic-'+str(k))
        if mode == 'force-only':
            audit.check(stage['appliedTorqueMax'] == 0, ident+'.force-only-stage-added-torque-zero-'+str(k))
        else:
            audit.check(stage['modeledTorqueMax'] == stage['appliedTorqueMax'], ident+'.full-stage-modeled-applied-torque-'+str(k))
        audit.check(stage['admitted'] is True and stage['descendingEligible'] is True
                    and math.isfinite(stage['residual']) and 0 <= stage['residual'] <= cfg['residualLimit']
                    and math.isfinite(stage['sourceReceiverMismatch']) and 0 <= stage['sourceReceiverMismatch'] <= cfg['sourceReceiverLimit'], ident+'.stage-reported-domain-'+str(k))
        if mode in ['coupled','force-only']:
            audit.check(isinstance(stage['symbolCounts'], list) and len(stage['symbolCounts']) == 12
                        and sum(stage['symbolCounts']) == 4*case['n']**2
                        and stage['symbolCounts'][4] == stage['symbolCounts'][11] == 0
                        and stage['symbolCounts'][8] == stage['positiveTerms'], ident+'.stage-census-'+str(k))
        else:
            audit.check(stage['edges'] == stage['positiveTerms'] == stage['residual'] == stage['sourceReceiverMismatch'] == 0, ident+'.off-stage-'+str(k))
    saturated = 0
    for k, control in enumerate(controls):
        audit.check(abs(control['t']-k*cfg['controlDt']) <= 1e-12 and control['t'] <= end+1e-12, ident+'.control-time-'+str(k))
        audit.require(len(control['values']) == case['n'], ident+'.control-width-'+str(k))
        saturated += sum(bool(x['saturated']) for x in control['values'])
        for v in control['values']:
            audit.check(len(v['u']) == 4 and all(math.isfinite(x) and 0 <= x <= 2.25*HOVER+1e-12 for x in v['u']), ident+'.control-domain-'+str(k))
            if case['command'] == 'fixed-nominal':
                audit.close(v['u'], [HOVER]*4, ident+'.fixed-control-'+str(k), 1e-12, 0)
                audit.check(v['saturated'] is False, ident+'.fixed-control-not-saturated-'+str(k))
    failure = record['failure']
    endpoint_rejection = bool(failure and not failure.get('stage') and failure['kind'] in ['coupling domain rejected', 'residual rejected'])
    endpoint_attempts = len(record['samples'])+int(endpoint_rejection)
    compare_tree(audit, record['counts'], dict(integrationStageAttempts=len(stages), endpointAttempts=endpoint_attempts, coupledQueryAttempts=len(stages)+endpoint_attempts if mode in ['coupled','force-only'] else 0, saturatedControllerUpdates=saturated), ident+'.counts')
    if failure and failure.get('stage'):
        failed = failure['stage']
        if failed['stage'] == 'final-projection':
            audit.check(not rejected and len(stages)%4 == 0 and abs(failed['t']-len(stages)*dt/4) <= 1e-12, ident+'.failed-final-projection-schedule')
            raw = np.asarray(failed['states'], dtype=float)
            norms = np.linalg.norm(raw[:,6:10], axis=1)
            audit.check(failure['kind'] == 'invalid quaternion' and np.any(~np.isfinite(norms) | (norms <= 0)), ident+'.failed-final-projection-domain')
            audit.close(failed['acceptedStart'], record['final'], ident+'.failed-projection-last-accepted', 1e-12, 0)
        else:
            k = len(stages)-1
            step, sub = divmod(k, 4)
            audit.check(rejected == [k], ident+'.failed-stage-attempt-retained')
            audit.check(failed['stage'] == sub+1 and abs(failed['t']-(step+[0, .5, .5, 1][sub])*dt) <= 1e-12, ident+'.failed-stage-schedule')
        if mode in ['coupled','force-only'] and failure['kind'] == 'coupling domain rejected':
            domain = geometry(ref, np.asarray(failed['states'], dtype=float), audit)
            audit.check(not domain['admitted'] or not domain['eligible'], ident+'.independent-failed-stage-rejection')
    elif endpoint_rejection and failure['kind'] == 'coupling domain rejected':
        domain = geometry(ref, np.asarray(failure['lastAcceptedStates'], dtype=float), audit)
        audit.check(not domain['admitted'] or not domain['eligible'], ident+'.independent-failed-endpoint-rejection')
    captured = captured_steps(audit, ref, record, case, mode, dt, cfg)
    separation = record['minimumSweptSeparation']
    audit.check(separation is None or math.isfinite(separation) and separation >= 0, ident+'.swept-separation-domain')
    if record['complete']:
        audit.check(separation is not None and separation >= .15-1e-12, ident+'.reported-complete-contact-clearance')
    audit.trials.append(dict(id=ident, complete=record['complete'], end=end, savedEndpoints=len(record['samples']), stageAttemptRecords=len(stages), capturedStageDerivativesChecked=captured, failure=entry['failure'], maximumEndpointErrors=errors))
    return record


def adapter_controls(audit, package, summary):
    saved = read(package/'results/adapter-controls.json')
    audit.check(saved == summary['adapterControls'], 'adapter-controls-summary-copy')
    records = saved['records']
    audit.require([r['id'] for r in records] == ['rotor-0','rotor-1','rotor-2','rotor-3','zero-correction','quaternion-angle'], 'six-adapter-controls')
    for rotor in range(4):
        rec = records[rotor]
        delta = np.zeros(4); delta[rotor] = .01
        expected = dict(force=[0., 0., .01], torque=[CORNERS[rotor,1]*.01, -CORNERS[rotor,0]*.01, 0.])
        compare_tree(audit, rec['expected'], expected, rec['id']+'.expected')
        audit.close(rec['actual']['delta'], delta, rec['id']+'.delta', 1e-14, 0)
        errors = []
        for key in ['force','torque']:
            errors.append(audit.close(rec['actual'][key], expected[key], rec['id']+'.'+key, 1e-14, 0))
        error = max(x for x in errors if x is not None)
        audit.close(rec['maxError'], error, rec['id']+'.error', 1e-14, 0)
        audit.check(rec['pass'] is (error < 1e-14), rec['id']+'.pass')
    rec = records[4]
    for key, size in [('delta',4),('force',3),('torque',3)]:
        audit.close(rec['actual'][key], np.zeros(size), 'zero-adapter-'+key, 0, 0)
    audit.check(rec['pass'] is True, 'zero-adapter-pass')
    rec = records[5]
    audit.close(rec['actual'], [0., math.pi/2], 'angle-control', 1e-14, 0)
    audit.close(rec['expected'], [0., math.pi/2], 'angle-control-expected', 1e-14, 0)
    audit.check(rec['pass'] is True and saved['pass'] is True, 'adapter-controls-pass')
    return bool(saved['pass'])


def review_supervisor(audit, package, cfg, summary):
    supervisor = read(package/'results/candidate-run.json')
    audit.require(supervisor['supervisor_success'] is True and supervisor['returncode'] == 0, 'candidate-supervisor-success')
    audit.check(not any(supervisor.get(k) for k in ['exception_class','terminated_for','cleanup_exception_class']), 'candidate-no-supervisor-exception')
    audit.check(supervisor['supervisor_elapsed_seconds'] <= cfg['limits']['candidateWallSeconds'], 'candidate-wall-cap')
    audit.check(supervisor['rssSamples'] > 0 and supervisor['rssSampleErrors'] == 0 and not supervisor['monitorErrors'], 'candidate-monitor-coverage')
    audit.check(supervisor['externalSampledPeakRSSKiB']*1024 <= cfg['limits']['rssBytes'], 'candidate-rss-cap')
    audit.check(digest(package/'source-manifest.json') == supervisor['source_manifest_sha256'], 'source-manifest-run-identity')
    manifest = read(package/'source-manifest.json')
    repository = package.parent.parent
    for pin in manifest['files']:
        audit.guard()
        verify_pin(audit, repository, pin, 'source-manifest.'+pin['path'])
    audit.check(len({p['path'] for p in supervisor['artifacts']}) == len(supervisor['artifacts']), 'supervisor-artifact-uniqueness')
    for pin in supervisor['artifacts']:
        audit.guard()
        verify_pin(audit, package, pin, 'supervisor-artifact.'+pin['path'])
    audit.check(sum(x['bytes'] for x in supervisor['artifacts']) == supervisor['finalScientificDirectoryBytes'], 'supervisor-artifact-byte-total')
    logs = sum(x['bytes'] for x in supervisor['artifacts'] if x['path'].endswith(('-stdout.txt','-stderr.txt')))
    audit.check(logs == supervisor['finalSupervisorLogBytes'] and logs <= 4*1024**2, 'candidate-log-accounting')
    audit.check(supervisor['finalScientificDirectoryBytes']+(package/'results/candidate-run.json').stat().st_size <= MAX_BYTES, 'candidate-final-aggregate-cap')
    audit.check(math.isfinite(summary['peakRSSBytes']) and summary['peakRSSBytes'] <= cfg['limits']['rssBytes'], 'candidate-internal-rss-cap')
    audit.check(math.isfinite(summary['elapsedMs']) and 0 <= summary['elapsedMs'] <= 300000, 'candidate-internal-elapsed-domain')
    return supervisor


def paired_comparison(left, right):
    maximum = discrepancy(left, right)
    chord, rate = None, None
    if maximum is not None:
        chord, rate = 0., 0.
        for a, b in zip(left['samples'], right['samples']):
            for x, y in zip(a['states'], b['states']):
                ax = rotate(np.asarray(x[6:10]), np.array([0.,0.,1.]))
                ay = rotate(np.asarray(y[6:10]), np.array([0.,0.,1.]))
                chord = max(chord, float(np.linalg.norm(ax-ay)))
                rate = max(rate, math.hypot(*(x[k]-y[k] for k in range(10,13))))
    return dict(left=left['mode'], right=right['mode'], dt=left['dt'], maximumSampled=maximum,
                maximumSampledBodyAxisAngle=None if chord is None else 2*math.asin(min(1.,chord/2)),
                maximumSampledBodyRateDifference=rate)


def reference_agreement(audit, repository, record, pin):
    ref = read(verify_pin(audit, repository, pin, record['id']+'.prior-reference'))
    fields = ['t','states','commands','forces','corrections','derivatives','witness','group']
    mismatches = []
    if len(record['samples']) != len(ref['samples']):
        mismatches.append('sample count')
    for k, (actual, expected) in enumerate(zip(record['samples'],ref['samples'])):
        for field in fields:
            if actual[field] != expected[field]:
                mismatches.append(str(k)+':'+field)
    # Exact numerical equality of the prescribed fields; elapsed clocks are excluded.
    audit.check(record['initial'] == ref['initial'], record['id']+'.reference-initial-exact')
    if record['complete'] and ref['complete']:
        audit.check(record['final'] == ref['final'], record['id']+'.reference-final-exact')
    return dict(id=record['id'], reference=pin['path'], sha256=pin['sha256'], fields=fields,
                samples=len(record['samples']), mismatches=mismatches,
                pass_=record['complete'] and ref['complete'] and not mismatches)


def force_only_pair_controls(records, cfg):
    answer = []
    for record in records:
        attitude = rate = torque = drift = 0.
        for sample in record['samples']:
            for i, state in enumerate(sample['states']):
                attitude = max(attitude, angle(state[6:10], [0.,0.,0.,1.]))
                rate = max(rate, math.hypot(*state[10:13]))
                torque = max(torque, math.hypot(*sample['corrections'][i]['torque']))
                drift = max(drift, math.hypot(state[0]-record['initial'][i][0],state[1]-record['initial'][i][1]))
        first = record['samples'][0] if record['samples'] else None
        pitch = first is not None and first['modeledCorrections'][0]['torque'][1] > 0
        collective = first is not None and first['corrections'][0]['force'][2] < 0
        answer.append(dict(dt=record['dt'], maxAttitude=attitude, maxRate=rate, maxAppliedTorque=torque,
                           maxHorizontalDrift=drift, positiveModeledPitch=pitch, negativeCollective=collective,
                           pass_=record['complete'] and pitch and collective and max(attitude,rate,torque,drift) <= cfg['identityTolerance']))
    return rename_pass(answer)


def initial_equality(force_only, full):
    fields = ['states','commands','forces','modeledCorrections','witness']
    if not force_only['samples'] or not full['samples']:
        return dict(dt=force_only['dt'], fields=[], equal=False, pass_=False, reason='initial sample unavailable')
    a, b = force_only['samples'][0], full['samples'][0]
    equal = all(a[key] == b[key] for key in fields)
    applied = all(x['force'] == y['force'] and x['torque'] == [0,0,0] for x,y in zip(a['corrections'],b['corrections']))
    return dict(dt=force_only['dt'], fields=fields, equal=equal, pass_=equal and applied)


def force_only_mask(records):
    answer = []
    for record in records:
        stages = all(s['status'] == 'completed' and s['appliedTorqueMax'] == 0 for s in record['stages'])
        endpoints = all(correction['torque'] == [0,0,0] and correction['force'] == modeled['force']
                        for sample in record['samples']
                        for correction, modeled in zip(sample['corrections'],sample['modeledCorrections']))
        answer.append(dict(id=record['id'], stagePass=stages, endpointPass=endpoints,
                           pass_=record['complete'] and stages and endpoints))
    return rename_pass(answer)


def descriptive(record):
    stages = [s for s in record['stages'] if s['status'] == 'completed']
    final = np.asarray(record['final'], dtype=float)
    return dict(id=record['id'], mode=record['mode'], dt=record['dt'],
                maxRecordedStageTiltDegrees=max((s['maxTiltDegrees'] for s in stages), default=None),
                maxRecordedStageModeledTorque=max((s['modeledTorqueMax'] for s in stages), default=None),
                maxRecordedStageAppliedTorque=max((s['appliedTorqueMax'] for s in stages), default=None),
                finalCentroid=np.mean(final[:,:3], axis=0).tolist(),
                minimumSweptSeparation=record['minimumSweptSeparation'],
                saturatedControllerUpdates=record['counts']['saturatedControllerUpdates'])


def run(audit, package, output_path):
    cfg = read(package/'config.json')
    audit.require(cfg['timesteps'] == [.005,.0025,.00125] and cfg['modes'] == ['off','coupled','force-only'], 'frozen-resolution-modes')
    audit.require([c['id'] for c in cfg['cases']] == ['offset-pair','boids16'], 'frozen-case-order')
    pair_case, boids_case = cfg['cases']
    audit.require(pair_case['n'] == 2 and pair_case['duration'] == .5 and pair_case['command'] == 'fixed-nominal'
                  and pair_case['positions'] == [[-6,0,4.5],[-5.96,0,5.1]], 'frozen-offset-pair')
    audit.require(boids_case['n'] == 16 and boids_case['duration'] == 2 and boids_case['seed'] == 260201
                  and boids_case['command'] == 'local-boids' and boids_case['conditionalMode'] == 'force-only', 'frozen-boids-case')
    audit.require(cfg['identityTolerance'] == 1e-12 and cfg['controlDt'] == .01 and cfg['sampleDt'] == .1, 'frozen-identity-cadences')
    audit.require(cfg['tolerances'] == dict(position=.001,velocity=.001,attitude=math.pi/1800,rotor=.001,bodyRate=.001)
                  and cfg['refinementRatio'] == .75 and cfg['roundoffFraction'] == .01, 'frozen-convergence-rule')
    audit.require(cfg['residualLimit'] == 1e-9 and cfg['sourceReceiverLimit'] == 2e-9, 'frozen-residual-limits')
    audit.require(cfg['limits'] == dict(candidateWallSeconds=300,reviewWallSeconds=120,
                  candidateCooperativeSeconds=280,rssBytes=805306368,evidenceBytes=MAX_BYTES),
                  'frozen-output-review-bounds')
    expected_pins = [dict(case='boids16',mode=mode,dt=dt,path='research/m31-motion-feedback-2026-10-16/results/boids16-'+mode+'-'+str(dt)+'.json',bytes=size,sha256=sha)
                     for mode,dt,size,sha in REFERENCE_TRIAL_PINS]
    audit.require(cfg['references'] == expected_pins, 'six-frozen-prior-reference-pins')
    refpath = package.parent/'m31-typed-assembly-2026-10-16/source/numeric-reference.py'
    audit.require(digest(refpath) == REFERENCE_SHA, 'independent-numeric-reference-identity')
    spec = importlib.util.spec_from_file_location('force_ablation_numeric_reference', refpath)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    summary = read(package/'results/analysis.json')
    audit.require(summary['complete'] is True and summary['kind'] == cfg['kind'], 'candidate-analysis-complete')
    adapter_pass = adapter_controls(audit,package,summary)
    audit.check(not (package/'results/partial-analysis.json').exists(), 'no-global-interruption')
    supervisor = review_supervisor(audit,package,cfg,summary)
    repository = package.parent.parent
    entries, at, seen = summary['trials'], 0, []
    audit.require(len(entries) in [9,12], 'fixed-nine-or-twelve-path-schedule')
    convergence_rows, references, by_mode = [], [], {}
    pair = []
    for dt in cfg['timesteps']:
        pair.append(trial(audit,ref,package,entries[at],pair_case,'force-only',dt,cfg)); at += 1
    convergence_rows.append(dict(case='offset-pair',mode='force-only',**rename_pass(convergence(*pair,cfg))))
    pair_controls = force_only_pair_controls(pair,cfg)
    pair_masks = force_only_mask(pair)
    expected_controls = dict(forceOnlyPair=pair_controls,forceOnlyMask=pair_masks)
    for mode in ['off','coupled']:
        records = []
        for dt in cfg['timesteps']:
            record = trial(audit,ref,package,entries[at],boids_case,mode,dt,cfg); at += 1
            records.append(record)
            pin = next(p for p in cfg['references'] if p['mode'] == mode and p['dt'] == dt)
            references.append(rename_pass(reference_agreement(audit,repository,record,pin)))
        by_mode[mode] = records
        convergence_rows.append(dict(case='boids16',mode=mode,**rename_pass(convergence(*records,cfg))))
    compare_tree(audit,summary['referenceAgreement'],references,'reference-agreement')
    primary = (adapter_pass and all(r['complete'] for r in entries[:9]) and all(r['pass'] for r in convergence_rows)
               and all(r['pass'] for r in pair_controls) and all(r['pass'] for r in pair_masks)
               and all(r['pass'] for r in references))
    audit.check(summary['primaryPass'] is primary,'primary-gate')
    audit.check(summary['exploratoryExecuted'] is primary,'conditional-force-only-execution')
    audit.require(len(entries) == (12 if primary else 9),'conditional-path-count')
    comparisons, descriptions = [], []
    allocation = False
    if primary:
        force_only = []
        for dt in cfg['timesteps']:
            force_only.append(trial(audit,ref,package,entries[at],boids_case,'force-only',dt,cfg)); at += 1
        by_mode['force-only'] = force_only
        convergence_rows.append(dict(case='boids16',mode='force-only',**rename_pass(convergence(*force_only,cfg))))
        initial = [rename_pass(initial_equality(a,b)) for a,b in zip(force_only,by_mode['coupled'])]
        expected_controls['initialEquality'] = initial
        for i in range(3):
            for left,right in [('off','coupled'),('off','force-only'),('force-only','coupled')]:
                comparisons.append(paired_comparison(by_mode[left][i],by_mode[right][i]))
        descriptions = [descriptive(record) for records in by_mode.values() for record in records]
        allocation = (all(r['complete'] for r in entries) and all(r['pass'] for r in convergence_rows)
                      and all(r['pass'] for r in initial))
    expected_controls['forceOnlyMask'] = force_only_mask(pair+by_mode.get('force-only',[]))
    allocation = allocation and all(r['pass'] for r in expected_controls['forceOnlyMask'])
    compare_tree(audit,summary['controls'],expected_controls,'ablation-controls')
    compare_tree(audit,summary['convergence'],convergence_rows,'all-convergence')
    compare_tree(audit,summary['comparisons'],comparisons,'all-pairwise-comparisons')
    compare_tree(audit,summary['descriptive'],descriptions,'all-descriptive-records')
    audit.check(summary['allocationPass'] is allocation,'allocation-decision')
    for records in [pair]+list(by_mode.values()):
        for record in records:
            baseline = pair[0]['initial'] if record['case'] == 'offset-pair' else by_mode['off'][0]['initial']
            audit.check(record['initial'] == baseline,record['id']+'.initial-identical-across-modes-resolutions')
            seen.append(record['id']+'.json')
    trial_files = sorted(x.name for x in (package/'results').glob('*.json') if x.name.startswith(('offset-pair-','boids16-')))
    audit.check(trial_files == sorted(seen),'no-extra-or-missing-trial-files')
    normal_bytes = sum((package/'results'/name).stat().st_size for name in seen+['adapter-controls.json','analysis.json'])
    audit.check(normal_bytes <= MAX_BYTES-8*1024**2,'candidate-normal-evidence-cap')
    aggregate = sum(p.stat().st_size for p in scientific_files(package) if p.resolve() != output_path.resolve())
    audit.check(aggregate <= MAX_BYTES,'pre-review-aggregate-cap')
    tilt = []
    for records in by_mode.values():
        for record in records:
            actual_angles = [math.atan2(math.hypot(*axis[:2]),axis[2])*180/math.pi
                             for s in record['samples'] for q in np.asarray(s['states'])[:,6:10]
                             for axis in [rotate(q,np.array([0.,0.,1.]))]]
            tilt.append(dict(id=record['id'],independentMaximumSampledTiltDegrees=max(actual_angles,default=None),
                             candidateReportedMaximumStageTiltDegrees=descriptive(record)['maxRecordedStageTiltDegrees']))
    return dict(primaryPass=primary,exploratoryExecuted=primary,allocationPass=allocation,
                allConvergencePass=all(r['pass'] for r in convergence_rows),convergence=convergence_rows,
                controls=expected_controls,referenceAgreement=references,comparisons=comparisons,
                descriptive=descriptions,tilt=tilt,aggregateBeforeReviewBytes=aggregate,
                sourceCommit=supervisor['source_commit'],sourceManifestSHA256=supervisor['source_manifest_sha256'],
                candidateElapsedSeconds=supervisor['supervisor_elapsed_seconds'],candidateSampledPeakRSSKiB=supervisor['externalSampledPeakRSSKiB'])



def main():
    audit = Audit()
    # Invalid-domain evidence must not emit library warnings with local source paths.
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    np.seterr(all='ignore')
    if len(sys.argv) != 3:
        print('review requires package and output arguments', file=sys.stderr)
        return 2
    package, output_path = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    result = dict(kind='independent-saved-force-moment-ablation-review', complete=False,
                  method='independent saved-state geometry/analytic roots/modeled and applied wrench/full derivative; no trajectory integration',
                  limits=['First/last saved stage derivatives and RK4 assembly are checked; other stages have diagnostics only and are not reintegrated.',
                          'Boids commands/initialization and collision detector are candidate-source provenance, not independently rerun.',
                          'Sampled timestep comparisons do not bound between-sample error or physical error.',
                          'Forces are modeled rotor loads; force-only applies their collective force but masks added roll/pitch torque.',
                          'Nominal roll/pitch/yaw torque, gyroscopic terms and motor dynamics are retained; physical validity is unresolved.',
                          'Each arm evolves its own states, commands and geometry; raw pairwise differences are not additive causal attribution.',
                          'Saved-state coverage counts describe exercised states and are not an additional outcome gate.'])
    try:
        with output_path.open('x', encoding='utf8') as output:
            try:
                result.update(run(audit, package, output_path))
                result['complete'] = True
            except Exception as error:
                audit.check(False, 'review-error.'+type(error).__name__)
                # Do not print exception strings, tracebacks, command lines or private paths.
                print('independent saved review stopped: '+type(error).__name__, file=sys.stderr)
            result.update(pass_=result['complete'] and not audit.failures, checkCount=audit.checks, failures=audit.failures,
                          savedEndpointsChecked=audit.endpoints, trials=audit.trials, elapsedSeconds=time.monotonic()-audit.start,
                          savedStateCoverage=dict(thresholds=dict(bodyRateNormRadPerSecond=COVERAGE_THRESHOLD,
                              nominalRotorRangeNewtons=COVERAGE_THRESHOLD, nominalRollPitchTorqueNormNewtonMetres=COVERAGE_THRESHOLD),
                              rows=list(audit.saved_state_coverage.values())))
            result = rename_pass(result)
            encoded = json.dumps(result, allow_nan=False, indent=2)+'\n'
            aggregate = sum(x.stat().st_size for x in scientific_files(package) if x.resolve() != output_path)
            if aggregate+len(encoded.encode()) > MAX_BYTES:
                result['pass'] = False
                result['failures'].append('review-output-aggregate-byte-cap')
                result['trials'] = []
                result['failures'] = result['failures'][:32]+['review-output-compacted']
                encoded = json.dumps(result, allow_nan=False, indent=2)+'\n'
                if aggregate+len(encoded.encode()) > MAX_BYTES:
                    raise EvidenceError('no aggregate capacity for review failure record')
            output.write(encoded)
        print(json.dumps({'complete':result['complete'], 'pass':result['pass'], 'checks':audit.checks, 'endpoints':audit.endpoints}))
        return 0 if result['pass'] else 1
    except Exception as error:
        print('independent saved review output failure: '+type(error).__name__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
