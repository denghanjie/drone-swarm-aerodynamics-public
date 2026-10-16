#!/usr/bin/env python3
"""Independent saved ratio-reuse review; no trajectory integration."""
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
MAX_BYTES = 96*1024**2
COVERAGE_THRESHOLD = 1e-12
MOTOR_ARM_RADIUS = math.sqrt(2)*ARM
REFERENCE_TRIAL_PINS = [
    (.005,2444177,'3f4fd16d65576be639b488ddda98423b82a8bd5c74d92a93b8ae3898329578f5'),
    (.0025,3126799,'25284d0565463b390c9174fc2051dbaff447b64f70612969fe8128c071d4c73a'),
    (.00125,4496943,'2288c5161858dbbe32dbfc7bc5bb8b30ed26006bc5a89e3eef1572f6570ed4fb')]


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
        self.cached_evaluations = 0
        self.captured_domain_audits = []

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


def reference_agreement(audit, repository, record, pin):
    ref = read(verify_pin(audit, repository, pin, record['id']+'.prior-reference'))
    fields = ['t','states','commands','forces','modeledCorrections','corrections','derivatives','witness','group']
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


def cached_values(audit, states, commands, cache_x, label):
    """Reconstruct held-root arithmetic at a fixed saved state, without a solve."""
    states, commands, cache_x = (np.asarray(x, dtype=float) for x in (states,commands,cache_x))
    n = len(states)
    audit.require(states.shape == (n,17) and commands.shape == (n,4) and cache_x.shape == (n,4), label+'.shapes')
    audit.require(np.all(np.isfinite(states)) and np.all(np.isfinite(commands))
                  and np.all(np.isfinite(cache_x)), label+'.finite')
    audit.close(np.linalg.norm(states[:,6:10],axis=1), np.ones(n), label+'.unit-quaternion', 1e-12, 0)
    audit.check(np.all(states[:,13:17] > 0), label+'.positive-nominal-rotors')
    audit.check(np.all(np.isfinite(np.sum(states[:,13:17],axis=1))),label+'.finite-nominal-totals')
    audit.check(np.all(commands >= 0) and np.all(commands <= 2.25*HOVER+1e-12),label+'.command-range')
    audit.check(np.all((cache_x > 0) & (cache_x <= 1)), label+'.cached-root-bounds')
    forces = states[:,13:17]*cache_x
    modeled, applied, derivatives = body_fields(states, commands, forces, 'coupled')
    return dict(forces=forces, modeledCorrections=modeled, corrections=applied, derivatives=derivatives)


def witness_roots(witness):
    """The cache is the solver's saved x, never a rounded T/f0 reconstruction."""
    return [[rotor['x'] for rotor in row] for row in witness['rotors']]


def refresh_difference(states, old_forces, joint_forces):
    """Left-limit held-cache error against an instantaneous joint solve."""
    states, old_forces, joint_forces = (np.asarray(v, dtype=float) for v in (states,old_forces,joint_forces))
    delta = old_forces-joint_forces
    world = np.asarray([rotate(state[6:10],np.array([0.,0.,math.fsum(row)]))
                        for state,row in zip(states,delta)])
    moments = np.column_stack((delta @ CORNERS[:,1], -delta @ CORNERS[:,0]))
    return dict(rotor=float(np.max(np.abs(delta)))/HOVER,
                force=float(np.max(np.linalg.norm(world,axis=1)))/(MASS*GRAVITY),
                moment=float(np.max(np.linalg.norm(moments,axis=1)))/(MASS*GRAVITY*MOTOR_ARM_RADIUS))


def stage_cache_index(step, dt, refresh_dt):
    """A step's final k4 keeps the interval cache even at a refresh boundary."""
    interval_steps = round(refresh_dt/dt)
    return step//interval_steps




def inherited_controls(audit, saved):
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


def full_metadata(audit, info, label):
    audit.check(info['evaluation'] == 'instantaneous' and all(info[k] is None for k in ['cacheIndex','cacheTime','cacheAge']), label+'.instantaneous-metadata')


def cached_metadata(audit, info, cache, t, cfg, label):
    audit.require(isinstance(cache['index'],int) and cache['index'] >= 0 and math.isfinite(cache['t']) and math.isfinite(t),label+'.finite-cache-identity')
    audit.check(info['evaluation'] == 'cached-ratio' and info['cacheIndex'] == cache['index'], label+'.cache-index')
    audit.check(info['cacheTime'] == cache['t'], label+'.cache-time')
    age = t-cache['t']
    audit.close(info['cacheAge'], age, label+'.cache-age', 1e-12, 0)
    audit.check(-1e-12 <= age <= cfg['refreshDt']+1e-12, label+'.cache-age-range')
    audit.check(all(info[k] is None for k in ['edges','positiveTerms','residual','sourceReceiverMismatch','symbolCounts','admitted','descendingEligible']), label+'.current-closure-not-claimed')
    audit.close(info['minRatio'], min(x for row in cache['ratios'] for x in row), label+'.cache-min-ratio', 1e-12, 0)


def cached_check(audit, evaluation, states, commands, cache, t, cfg, label, stage_capture=False):
    audit.guard()
    expected = cached_values(audit, states, commands, cache['ratios'], label)
    cached_metadata(audit, evaluation['info'], cache, t, cfg, label)
    audit.close(evaluation['forces'], expected['forces'], label+'.loads')
    audit.close(evaluation['derivatives'], expected['derivatives'], label+'.full17-derivative')
    for field in ['modeledCorrections','corrections']:
        audit.require(len(evaluation[field]) == len(states), label+'.'+field+'-width')
        for i,(actual,want) in enumerate(zip(evaluation[field],expected[field])):
            for key in ['delta','force','torque']:
                audit.close(actual[key], want[key], label+'.'+field+'.'+str(i)+'.'+key)
    if not stage_capture:
        audit.check(evaluation['witness'] is None, label+'.no-current-geometry-witness')
    torque = max(np.linalg.norm(c['torque']) for c in expected['corrections'])
    for key in ['modeledTorqueMax','appliedTorqueMax']:
        audit.close(evaluation['info'][key], torque, label+'.'+key)
    tilt = max(math.acos(float(np.clip(rotate(np.asarray(s[6:10]),np.array([0.,0.,1.]))[2],-1,1)))*180/math.pi for s in states)
    audit.close(evaluation['info']['maxTiltDegrees'],tilt,label+'.tilt',2e-6,1e-9)
    audit.cached_evaluations += 1
    return expected


def adapter_controls(audit, package, summary, cfg):
    saved = read(package/'results/adapter-controls.json')
    audit.check(saved == summary['adapterControls'], 'adapter-controls-summary-copy')
    prior = inherited_controls(audit,saved['inherited'])
    records = saved['records']
    audit.require([r['id'] for r in records] == ['identity-ratios','current-nominal-scaling','cache-age-rejection','nonfinite-cache-rejection'], 'four-reuse-adapter-controls')
    q = [math.sin(.1),0.,0.,math.cos(.1)]
    state = [0.,0.,4.,.1,-.2,.05]+q+[.2,-.1,.3,HOVER,.9*HOVER,1.1*HOVER,.95*HOVER]
    commands = [[HOVER]*4]
    rec = records[0]
    audit.close(rec['states'],[state],'identity-control-state',1e-14,0)
    audit.close(rec['commands'],commands,'identity-control-commands',1e-14,0)
    compare_tree(audit,rec['cache'],dict(index=0,t=0,ratios=[[1,1,1,1]]),'identity-control-cache')
    audit.check(rec['t'] == .005,'identity-control-time')
    result = cached_check(audit,rec['actual'],rec['states'],rec['commands'],rec['cache'],rec['t'],cfg,'identity-control')
    audit.close(rec['nominalDerivative'],result['derivatives'][0],'identity-control-nominal-derivative')
    audit.check(rec['actual']['derivatives'][0] == rec['nominalDerivative'],'identity-control-saved-derivative-exact')
    for field in ['force','torque']:
        audit.close(rec['actual']['corrections'][0][field],[0,0,0],'identity-control-zero-'+field,0,0)
    audit.check(rec['pass'] is True,'identity-control-pass')
    rec = records[1]
    changed = state.copy()
    changed[13:17] = [x*1.1 for x in changed[13:17]]
    audit.close(rec['states'],[state],'scaling-control-state',1e-14,0)
    audit.close(rec['changedStates'],[changed],'scaling-control-changed-state',1e-14,0)
    audit.close(rec['commands'],commands,'scaling-control-commands',1e-14,0)
    compare_tree(audit,rec['cache'],dict(index=0,t=0,ratios=[[.8,.9,.85,.95]]),'scaling-control-cache')
    audit.check(rec['t'] == .005,'scaling-control-time')
    for field,state_field in [('actual','states'),('changed','changedStates')]:
        cached_check(audit,rec[field],rec[state_field],rec['commands'],rec['cache'],rec['t'],cfg,'scaling-control-'+field)
    err = float(np.max(np.abs(np.asarray(rec['changed']['forces'])-1.1*np.asarray(rec['actual']['forces']))))
    audit.close(rec['maxScalingError'],err,'scaling-control-error',1e-14,0)
    audit.check(rec['cacheUnchanged'] is True and rec['pass'] is (err < 1e-14),'scaling-control-pass')
    compare_tree(audit,records[2],rename_pass(dict(id='cache-age-rejection',guards=[dict(t=-.001,rejected=True),dict(t=.0101,rejected=True)],pass_=True)),'age-control')
    compare_tree(audit,records[3],rename_pass(dict(id='nonfinite-cache-rejection',guards=[dict(key=k,rejected=True) for k in ['time','cacheTime','index']],pass_=True)),'nonfinite-control')
    audit.check(prior and saved['pass'] is True,'all-adapter-controls-pass')
    return bool(saved['pass'])


def held_commands(audit, record, t, commands, label):
    eligible = [c for c in record['controls'] if c['t'] < t-1e-12 or t == 0 and c['t'] == 0]
    audit.require(bool(eligible),label+'.held-control-present')
    audit.check(commands == [v['u'] for v in eligible[-1]['values']],label+'.held-command-exact')


def event_checks(audit, ref, record, case, cfg):
    events = record['events']
    if record['mode'] == 'coupled':
        audit.require(events == [],record['id']+'.no-full-refresh-events')
        return None
    audit.require(len(events) == round(case['duration']/cfg['refreshDt'])+1,record['id']+'.refresh-count')
    maxima = dict(rotor=0.,force=0.,moment=0.)
    post = dict(maxima)
    previous_cache = None
    for index,event in enumerate(events):
        audit.guard()
        label = record['id']+'.refresh-'+str(index)
        t = round(index*cfg['refreshDt'],6)
        role = 'terminal-audit' if index == len(events)-1 else 'propagation-refresh'
        audit.require(event['index'] == index and event['t'] == t and event['role'] == role and event['status'] == 'completed',label+'.identity-completed')
        audit.check(event['oldCacheIndex'] == (index-1 if index else None),label+'.old-cache-index')
        held_commands(audit,record,t,event['commands'],label)
        states,commands = event['states'],event['commands']
        full_metadata(audit,event['instantaneous']['info'],label)
        endpoint(audit,ref,dict(event['instantaneous'],states=states,commands=commands),'coupled',case['n'],cfg,label+'.instantaneous')
        expected_cache = dict(index=index,t=t,ratios=witness_roots(event['instantaneous']['witness']))
        audit.check(event['cache'] == expected_cache,label+'.cache-is-direct-saved-roots')
        if index:
            audit.require(isinstance(event['left'],dict),label+'.left-present')
            cached_check(audit,event['left'],states,commands,previous_cache,t,cfg,label+'.left')
            error = refresh_difference(states,event['left']['forces'],event['instantaneous']['forces'])
            compare_tree(audit,event['error'],error,label+'.pre-refresh-error')
            maxima = {k:max(v,error[k]) for k,v in maxima.items()}
        else:
            audit.check(event['left'] is None and event['error'] is None,label+'.initial-left-null')
            audit.check(states == record['initial'],label+'.initial-state-exact')
        cached_check(audit,event['right'],states,commands,event['cache'],t,cfg,label+'.right')
        post_error = refresh_difference(states,event['right']['forces'],event['instantaneous']['forces'])
        compare_tree(audit,event['postError'],post_error,label+'.post-refresh-error')
        post = {k:max(v,post_error[k]) for k,v in post.items()}
        previous_cache = event['cache']
    audit.check(events[-1]['states'] == record['final'],record['id']+'.terminal-refresh-final-state')
    gates = {k:dict(maximum=maxima[k],tolerance=tol,pass_=maxima[k] <= tol) for k,tol in cfg['eventErrorTolerances'].items()}
    return rename_pass(dict(id=record['id'],dt=record['dt'],positiveEvents=len(events)-1,maxima=maxima,postMaxima=post,
                            postRefreshPass=all(v <= cfg['identityTolerance'] for v in post.values()),gates=gates,pass_=all(g['pass_'] for g in gates.values())))


def captured_steps(audit, ref, record, case, cfg):
    dt,mode = record['dt'],record['mode']
    total_steps = round(case['duration']/dt)
    steps = record['stepWitnesses']
    audit.require([s['step'] for s in steps] == [0,total_steps-1],record['id']+'.captured-step-policy')
    for saved in steps:
        step = saved['step']
        label = record['id']+'.captured-step-'+str(step)
        audit.check(saved['t'] == step*dt and saved['h'] == dt,label+'.time')
        cache = record['events'][stage_cache_index(step,dt,cfg['refreshDt'])]['cache'] if mode == 'reuse10ms' else None
        audit.check(saved['cacheIndex'] == (cache['index'] if cache else None),label+'.cache-index')
        # Stage commands use the control selected at the step start, unlike boundary samples.
        control = record['controls'][round(step*dt/cfg['controlDt']) if step == 0 else math.floor((step*dt+1e-12)/cfg['controlDt'])]
        audit.check(saved['commands'] == [v['u'] for v in control['values']],label+'.step-command')
        base = np.asarray(saved['initial'],dtype=float)
        witnesses = []
        for sub in range(4):
            stage = record['stages'][4*step+sub]
            w = stage['witness']
            label_stage = label+'.stage-'+str(sub+1)
            info = {k:v for k,v in stage.items() if k not in ['witness','t','stage','status','evaluationAttempted']}
            evaluation = dict(w,info=info)
            audit.check(w['commands'] == saved['commands'],label_stage+'.command-exact')
            raw = base if sub == 0 else base+dt*[.5,.5,1][sub-1]*np.asarray(witnesses[-1]['derivatives'])
            audit.close(w['states'],project(raw),label_stage+'.assembly',1e-12,1e-12)
            audit.close(stage['rawQuaternionNormMaxError'],float(np.max(np.abs(np.linalg.norm(raw[:,6:10],axis=1)-1))),label_stage+'.raw-quaternion',1e-12,0)
            if mode == 'coupled':
                endpoint(audit,ref,evaluation,'coupled',case['n'],cfg,label_stage,False)
            else:
                expected = cached_check(audit,evaluation,w['states'],w['commands'],cache,stage['t'],cfg,label_stage,True)
                geom = geometry(ref,np.asarray(w['states'],dtype=float),audit)
                fresh_error = None
                if geom['admitted'] and geom['eligible']:
                    _,_,_,fresh_forces = solve(ref,geom,audit)
                    fresh_error = refresh_difference(w['states'],expected['forces'],fresh_forces)
                audit.captured_domain_audits.append(dict(id=record['id'],step=step,stage=sub+1,t=stage['t'],
                    admitted=geom['admitted'],descendingEligible=geom['eligible'],cachedVersusFreshLoadError=fresh_error))
            witnesses.append(w)
        slopes = [np.asarray(w['derivatives']) for w in witnesses]
        end = project(base+dt*(slopes[0]+2*slopes[1]+2*slopes[2]+slopes[3])/6)
        audit.close(saved['final'],end,label+'.final-assembly',1e-12,1e-12)
        if step == 0:
            audit.check(saved['initial'] == record['initial'],label+'.initial-source')
        if step == total_steps-1:
            audit.check(saved['final'] == record['final'],label+'.final-source')
    return 8


def trial(audit, ref, package, entry, mode, dt, cfg):
    case = cfg['cases'][0]
    ident = case['id']+'-'+mode+'-'+str(dt)
    audit.require(entry['id'] == ident,ident+'.scheduled-entry')
    record = read(verify_pin(audit,package,entry['pin'],ident))
    audit.require(record['id'] == ident and record['case'] == case['id'] and record['mode'] == mode and record['dt'] == dt,ident+'.identity')
    # A partial prefix is retained candidate evidence, never a complete independent audit.
    audit.require(record['complete'] is True and entry['complete'] is True and record['failure'] is None and entry['failure'] is None,ident+'.complete-path-required')
    audit.check(abs(record['end']-case['duration']) <= 1e-12,ident+'.complete-horizon')
    initial = np.asarray(record['initial'],dtype=float)
    final = np.asarray(record['final'],dtype=float)
    audit.require(initial.shape == final.shape == (case['n'],17) and np.all(np.isfinite(initial)) and np.all(np.isfinite(final)),ident+'.initial-final-domain')
    controls = record['controls']
    audit.require(len(controls) == round(case['duration']/cfg['controlDt']),ident+'.control-count')
    saturated = 0
    for index,control in enumerate(controls):
        audit.check(control['t'] == round(index*cfg['controlDt'],6),ident+'.control-time-'+str(index))
        audit.require(len(control['values']) == case['n'],ident+'.control-width-'+str(index))
        for value in control['values']:
            audit.check(isinstance(value['saturated'],bool),ident+'.saturation-boolean')
            saturated += int(value['saturated'])
            audit.check(len(value['u']) == 4 and all(math.isfinite(x) and 0 <= x <= 2.25*HOVER+1e-12 for x in value['u']),ident+'.control-range')
    event_summary = event_checks(audit,ref,record,case,cfg)
    samples = record['samples']
    audit.require(len(samples) == round(case['duration']/cfg['sampleDt'])+1,ident+'.sample-count')
    audit.check(samples[0]['states'] == record['initial'] and samples[-1]['states'] == record['final'],ident+'.sample-initial-final-source')
    for index,sample in enumerate(samples):
        t = round(index*cfg['sampleDt'],6)
        label = ident+'.sample-'+str(index)
        audit.check(sample['t'] == t,label+'.time')
        held_commands(audit,record,t,sample['commands'],label)
        if mode == 'coupled':
            audit.check(sample['eventIndex'] is None and sample['sampleSide'] == 'instantaneous',label+'.instantaneous-source')
            full_metadata(audit,sample['info'],label)
            endpoint(audit,ref,sample,'coupled',case['n'],cfg,label)
        else:
            event_index = round(t/cfg['refreshDt'])
            event = record['events'][event_index]
            side = 'right' if index == 0 else 'left'
            audit.check(sample['eventIndex'] == event_index and sample['sampleSide'] == side,label+'.refresh-source-side')
            audit.check(sample['states'] == event['states'] and sample['commands'] == event['commands'],label+'.event-state-command-exact')
            audit.check(all(sample[k] == event[side][k] for k in ['forces','modeledCorrections','corrections','derivatives','info','witness']),label+'.event-evaluation-exact')
            cache = record['events'][event_index if index == 0 else event_index-1]['cache']
            cached_check(audit,sample,sample['states'],sample['commands'],cache,t,cfg,label)
    stages = record['stages']
    steps = round(case['duration']/dt)
    audit.require(len(stages) == steps*4,ident+'.stage-count')
    for index,stage in enumerate(stages):
        if index % 256 == 0:
            audit.guard()
        step,sub = divmod(index,4)
        label = ident+'.stage-'+str(index)
        t = (step+[0,.5,.5,1][sub])*dt
        audit.require(stage['status'] == 'completed' and stage['evaluationAttempted'] is True,label+'.completed-evaluation')
        audit.check(stage['stage'] == sub+1 and abs(stage['t']-t) <= 1e-12,label+'.schedule')
        audit.check(('witness' in stage) == (step in [0,steps-1]),label+'.capture-policy')
        audit.check(math.isfinite(stage['rawQuaternionNormMaxError']) and stage['rawQuaternionNormMaxError'] >= 0,label+'.raw-quaternion-domain')
        audit.check(math.isfinite(stage['maxTiltDegrees']) and 0 <= stage['maxTiltDegrees'] <= 180,label+'.tilt-domain')
        audit.check(math.isfinite(stage['modeledTorqueMax']) and stage['modeledTorqueMax'] >= 0 and stage['modeledTorqueMax'] == stage['appliedTorqueMax'],label+'.full-wrench-diagnostic')
        if mode == 'coupled':
            full_metadata(audit,stage,label)
            audit.check(stage['admitted'] is True and stage['descendingEligible'] is True,label+'.reported-domain')
            audit.check(math.isfinite(stage['residual']) and 0 <= stage['residual'] <= cfg['residualLimit'] and math.isfinite(stage['sourceReceiverMismatch']) and 0 <= stage['sourceReceiverMismatch'] <= cfg['sourceReceiverLimit'],label+'.reported-residuals')
            census = stage['symbolCounts']
            audit.check(isinstance(census,list) and len(census) == 12 and sum(census) == 4*case['n']**2 and census[4] == census[11] == 0 and census[8] == stage['positiveTerms'],label+'.reported-census')
            audit.check(math.isfinite(stage['minRatio']) and 0 < stage['minRatio'] <= 1,label+'.load-ratio-domain')
        else:
            cache = record['events'][stage_cache_index(step,dt,cfg['refreshDt'])]['cache']
            cached_metadata(audit,stage,cache,stage['t'],cfg,label)
    captured = captured_steps(audit,ref,record,case,cfg)
    evaluators = sum(int(s['evaluationAttempted']) for s in stages)
    events = record['events']
    expected_counts = dict(integrationStageAttempts=len(stages),endpointAttempts=len(samples),
        jointQueryAttempts=evaluators+len(samples) if mode == 'coupled' else len(events),
        cachedApplicationAttempts=0 if mode == 'coupled' else evaluators+2*len(events)-1,
        refreshEventAttempts=len(events),propagationRefreshAttempts=max(0,len(events)-1),
        terminalAuditAttempts=int(bool(events)),saturatedControllerUpdates=saturated)
    compare_tree(audit,record['counts'],expected_counts,ident+'.attempt-counts')
    separation = record['minimumSweptSeparation']
    audit.check(isinstance(separation,(int,float)) and math.isfinite(separation) and separation >= .15-1e-12,ident+'.candidate-reported-contact-clearance')
    audit.check(math.isfinite(record['elapsedMs']) and 0 <= record['elapsedMs'] <= 300000,ident+'.elapsed-domain')
    description = dict(id=ident,mode=mode,dt=dt,maxRecordedStageTiltDegrees=max(s['maxTiltDegrees'] for s in stages),
        finalCentroid=np.mean(final[:,:3],axis=0).tolist(),minimumSweptSeparation=separation,counts=expected_counts)
    audit.trials.append(dict(id=ident,complete=True,savedSamples=len(samples),refreshEvents=len(events),
        capturedStageDerivativesChecked=captured,counts=expected_counts))
    # Do not retain three large event histories in memory for sampled comparisons.
    minimal = {k:record[k] for k in ['id','case','mode','dt','complete','initial','final','samples','counts']}
    minimal['eventSummary'],minimal['description'] = event_summary,description
    return minimal


def approximation_comparison(full, reuse, cfg):
    maximum = discrepancy(full,reuse)
    gates = {k:dict(maximum=None if maximum is None else maximum[k],tolerance=tol,
                    pass_=maximum is not None and maximum[k] <= tol) for k,tol in cfg['approximationTolerances'].items()}
    return rename_pass(dict(dt=reuse['dt'],left='coupled',right='reuse10ms',maximumSampled=maximum,
                            gates=gates,pass_=all(g['pass_'] for g in gates.values())))


def frozen_config(audit, cfg):
    metrics = dict(position=.001,velocity=.001,attitude=math.pi/1800,rotor=.001,bodyRate=.001)
    audit.require(cfg['kind'] == 'prospective-full-wrench-ratio-reuse','frozen-kind')
    audit.require(cfg['cases'] == [dict(id='boids16',n=16,seed=260201,duration=2,command='local-boids',conditionalMode='reuse10ms')],'frozen-case')
    audit.require(cfg['modes'] == ['coupled','reuse10ms'] and cfg['timesteps'] == [.005,.0025,.00125],'frozen-modes-steps')
    audit.require(cfg['controlDt'] == cfg['refreshDt'] == .01 and cfg['sampleDt'] == .1 and cfg['sampleSide'] == 'initial-right-positive-left','frozen-cadences-sides')
    audit.require(cfg['tolerances'] == cfg['approximationTolerances'] == metrics and cfg['eventErrorTolerances'] == dict(rotor=.001,force=.001,moment=.001),'frozen-thresholds')
    audit.require(cfg['momentLengthScale'] == 'motor-arm-radius' and cfg['refinementRatio'] == .75 and cfg['roundoffFraction'] == .01,'frozen-refinement-normalization')
    audit.require(cfg['identityTolerance'] == 1e-12 and cfg['residualLimit'] == 1e-9 and cfg['sourceReceiverLimit'] == 2e-9,'frozen-residual-identity')
    audit.require(cfg['limits'] == dict(candidateWallSeconds=300,reviewWallSeconds=120,candidateCooperativeSeconds=280,rssBytes=805306368,evidenceBytes=MAX_BYTES),'frozen-resource-bounds')
    pins = [dict(case='boids16',mode='coupled',dt=dt,path='research/m31-force-ablation-2026-10-16/results/boids16-coupled-'+str(dt)+'.json',bytes=size,sha256=sha) for dt,size,sha in REFERENCE_TRIAL_PINS]
    audit.require(cfg['references'] == pins,'three-immutable-reference-pins')


def run(audit, package, output_path):
    cfg = read(package/'config.json')
    frozen_config(audit,cfg)
    audit.require(not (package/'results/partial-analysis.json').exists(),'no-global-interruption')
    summary = read(package/'results/analysis.json')
    audit.require(summary['complete'] is True and summary['kind'] == cfg['kind'],'candidate-analysis-complete')
    supervisor = review_supervisor(audit,package,cfg,summary)
    refpath = package.parent/'m31-typed-assembly-2026-10-16/source/numeric-reference.py'
    audit.require(digest(refpath) == REFERENCE_SHA,'independent-numeric-reference-identity')
    spec = importlib.util.spec_from_file_location('ratio_reuse_numeric_reference',refpath)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    adapter_pass = adapter_controls(audit,package,summary,cfg)
    entries = summary['trials']
    audit.require(len(entries) in [3,6],'three-or-six-fixed-paths')
    full,reference_rows = [],[]
    for index,dt in enumerate(cfg['timesteps']):
        record = trial(audit,ref,package,entries[index],'coupled',dt,cfg)
        full.append(record)
        reference_rows.append(rename_pass(reference_agreement(audit,package.parent.parent,record,cfg['references'][index])))
    convergence_rows = [dict(case='boids16',mode='coupled',**rename_pass(convergence(*full,cfg)))]
    compare_tree(audit,summary['referenceAgreement'],reference_rows,'exact-prior-repetition')
    primary = adapter_pass and all(r['pass'] for r in reference_rows) and convergence_rows[0]['pass']
    audit.check(summary['primaryPass'] is primary and summary['reuseExecuted'] is primary,'primary-conditional-decision')
    audit.require(len(entries) == (6 if primary else 3),'conditional-path-count')
    reuse,comparisons,event_errors = [],[],[]
    if primary:
        for index,dt in enumerate(cfg['timesteps']):
            reuse.append(trial(audit,ref,package,entries[3+index],'reuse10ms',dt,cfg))
        convergence_rows.append(dict(case='boids16',mode='reuse10ms',**rename_pass(convergence(*reuse,cfg))))
        comparisons = [approximation_comparison(a,b,cfg) for a,b in zip(full,reuse)]
        event_errors = [r['eventSummary'] for r in reuse]
    descriptions = [r['description'] for r in full+reuse]
    for record in full+reuse:
        audit.check(record['initial'] == full[0]['initial'],record['id']+'.shared-initial-state')
    allocation = primary and all(r['pass'] for r in convergence_rows) and all(r['postRefreshPass'] for r in event_errors)
    approximation = allocation and all(r['pass'] for r in comparisons) and all(r['pass'] for r in event_errors)
    decision = 'eligible-for-larger-test' if approximation else 'missed-declared-targets' if allocation else 'incomplete-diagnostic'
    for field,expected in [('convergence',convergence_rows),('comparisons',comparisons),('eventErrors',event_errors),('descriptive',descriptions)]:
        compare_tree(audit,summary[field],expected,'analysis-'+field)
    audit.check(summary['allocationPass'] is allocation and summary['approximationPass'] is approximation and summary['decision'] == decision,'separate-integrity-approximation-decision')
    joint = sum(r['counts']['jointQueryAttempts'] for r in full+reuse)
    audit.check(summary['totalJointQueryAttempts'] == joint,'total-joint-attempts')
    audit.check(sum(r['counts']['jointQueryAttempts'] for r in full) == 11263,'full-complete-query-count')
    if primary:
        audit.check(sum(r['counts']['jointQueryAttempts'] for r in reuse) == 603 and joint == 11866,'reuse-complete-query-count')
        audit.check(sum(r['counts']['cachedApplicationAttempts'] for r in reuse) == 12403,'reuse-complete-cached-count')
        audit.check(sum(r['counts']['propagationRefreshAttempts'] for r in reuse) == 600 and sum(r['counts']['terminalAuditAttempts'] for r in reuse) == 3,'propagation-terminal-query-split')
        audit.check(len(audit.captured_domain_audits) == 24,'fixed-captured-reuse-domain-audits')
    audit.check(audit.endpoints == (666 if primary else 63),'independent-endpoint-refresh-coverage')
    audit.check(audit.cached_evaluations == (1293 if primary else 3),'independent-cached-evaluation-coverage')
    names = [r['id']+'.json' for r in full+reuse]
    actual = sorted(x.name for x in (package/'results').glob('boids16-*.json'))
    audit.check(actual == sorted(names),'no-extra-or-missing-path-files')
    normal_bytes = sum((package/'results'/name).stat().st_size for name in names+['adapter-controls.json','analysis.json'])
    audit.check(normal_bytes <= MAX_BYTES-8*1024**2,'normal-candidate-evidence-cap')
    aggregate = sum(p.stat().st_size for p in scientific_files(package) if p.resolve() != output_path.resolve())
    audit.check(aggregate <= MAX_BYTES,'pre-review-aggregate-cap')
    return dict(primaryPass=primary,reuseExecuted=primary,allocationPass=allocation,approximationPass=approximation,decision=decision,
        convergence=convergence_rows,referenceAgreement=reference_rows,comparisons=comparisons,eventErrors=event_errors,descriptive=descriptions,
        totalJointQueryAttempts=joint,syntheticCachedControlAttempts=8,aggregateBeforeReviewBytes=aggregate,
        sourceCommit=supervisor['source_commit'],sourceManifestSHA256=supervisor['source_manifest_sha256'],
        candidateElapsedSeconds=supervisor['supervisor_elapsed_seconds'],candidateSampledPeakRSSKiB=supervisor['externalSampledPeakRSSKiB'])


def main():
    audit = Audit()
    warnings.filterwarnings('ignore',category=RuntimeWarning)
    np.seterr(all='ignore')
    if len(sys.argv) != 3:
        print('review requires package and output arguments',file=sys.stderr)
        return 2
    package,output_path = pathlib.Path(sys.argv[1]).resolve(),pathlib.Path(sys.argv[2]).resolve()
    result = dict(kind='independent-saved-ratio-reuse-review',complete=False,
        method='independent fixed-state geometry/analytic roots/body derivatives/cache arithmetic/event errors/saved-slope algebra; no trajectory integration',
        limits=['A passing audit establishes saved-evidence consistency; approximation acceptance is a separate field.',
                'Incomplete paths or globally interrupted analysis fail closed; candidate prefixes remain evidence but are not accepted as a full audit.',
                'Ordinary cached stages have no current geometry or closure evaluation; captured current-domain reconstructions are descriptive only.',
                'Initial/controller generation, group summaries and swept collision checks are not independently rerun.',
                'Only first/last saved RK steps are reconstructed; sampled refinement is not a rigorous trajectory-error bound.',
                'Analytic guard records are checked against frozen predicates and source; candidate rejection code is not re-executed.',
                'Joint-query counts are evaluator attempts, not measured speedups; synthetic controls and reviewer work are separate.',
                'One exposed seed and provisional model do not establish physical validity, stability, continuous safety, novelty or 5000-drone performance.'])
    try:
        with output_path.open('x',encoding='utf8') as output:
            try:
                result.update(run(audit,package,output_path))
                result['complete'] = True
            except Exception as error:
                audit.check(False,'review-error.'+type(error).__name__)
                print('independent saved review stopped: '+type(error).__name__,file=sys.stderr)
            result.update(pass_=result['complete'] and not audit.failures,checkCount=audit.checks,failures=audit.failures,
                savedInstantaneousEndpointsAndEventsChecked=audit.endpoints,cachedEvaluationsChecked=audit.cached_evaluations,
                capturedReuseCurrentDomainAudits=audit.captured_domain_audits,trials=audit.trials,elapsedSeconds=time.monotonic()-audit.start)
            result = rename_pass(result)
            encoded = json.dumps(result,allow_nan=False,indent=2)+'\n'
            aggregate = sum(x.stat().st_size for x in scientific_files(package) if x.resolve() != output_path)
            if aggregate+len(encoded.encode()) > MAX_BYTES:
                result['pass'] = False
                result['failures'] = result['failures'][:32]+['review-output-aggregate-byte-cap']
                result['trials'] = []
                result['capturedReuseCurrentDomainAudits'] = []
                encoded = json.dumps(result,allow_nan=False,indent=2)+'\n'
                if aggregate+len(encoded.encode()) > MAX_BYTES:
                    raise EvidenceError('no aggregate capacity for review failure record')
            output.write(encoded)
        print(json.dumps({'complete':result['complete'],'pass':result['pass'],'checks':audit.checks}))
        return 0 if result['pass'] else 1
    except Exception as error:
        print('independent saved review output failure: '+type(error).__name__,file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
