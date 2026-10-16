#!/usr/bin/env python3
"""Independent frozen-snapshot review; source construction is not run permission.

No JavaScript imports. Python stdlib and NumPy only. No input is evaluated until
the separately authorized, once-only saved-evidence invocation calls main().
"""
import argparse
import gzip
import hashlib
import json
import math
import resource
import sys
import time
from pathlib import Path

import numpy as np

COEFFICIENT_ATOL = 2e-12
COEFFICIENT_RTOL = 2e-12
SOLUTION_RTOL = 1e-9


def constants():
    mg, arm, radius, rho = .027*9.81, .028, .023, 1.225
    area = math.pi*radius*radius
    return dict(mg=mg, arm=arm, radius=radius, rho=rho, area=area,
                D=2*math.sqrt(2)*arm, decay=10.11, spread=.07668, origin=-5.817,
                minDown=2.5, neighbor=3., nearRad=.15, downFade=2., downCut=2.5,
                radFade=2., radCut=3., induced=math.sqrt(mg/(8*rho*area)),
                sqrt2minus1=math.sqrt(2)-1)


def rotate_rows(q, body_vector):
    """Historical xyzw rotation identity, independently vectorized; no normalization."""
    v = np.asarray(body_vector, dtype=np.float64)
    t = 2*np.cross(q[:, :3], v)
    return v + (q[:, 3, None]*t + np.cross(q[:, :3], t))


def prepare_geometry(states, c):
    quaternion = states[:, 6:10]
    axis = rotate_rows(quaternion, [0., 0., 1.])
    arm = c['arm']
    offsets = np.stack([rotate_rows(quaternion, [x, y, 0.])
                        for x, y in [(arm, arm), (-arm, arm), (-arm, -arm), (arm, -arm)]], axis=1)
    qnorm = np.hypot(np.hypot(np.hypot(quaternion[:, 0], quaternion[:, 1]),
                              quaternion[:, 2]), quaternion[:, 3])
    anorm = np.hypot(np.hypot(axis[:, 0], axis[:, 1]), axis[:, 2])
    onorm = np.hypot(np.hypot(offsets[:, :, 0], offsets[:, :, 1]), offsets[:, :, 2])
    perpendicular = ((offsets[:, :, 0]*axis[:, None, 0] +
                      offsets[:, :, 1]*axis[:, None, 1]) + offsets[:, :, 2]*axis[:, None, 2])
    f0 = states[:, 13:17].copy()
    # Explicit left-to-right four-term sum matches the specified nominal total.
    s0 = ((f0[:, 0]+f0[:, 1])+f0[:, 2])+f0[:, 3]
    tilt = np.arccos(np.clip(axis[:, 2]/anorm, -1., 1.))
    return dict(q=states[:, :3], axis=axis, offsets=offsets, f0=f0, S0=s0,
                qnorm=qnorm, anorm=anorm, onorm=onorm, perpendicular=perpendicular,
                tilt=tilt)


def fade(values, start, end):
    t = (values-start)/(end-start)
    middle = (1-t)*(1-t)*(1+2*t)
    return np.where(values <= start, 1., np.where(values >= end, 0., middle))


def classify_receiver(i, geometry, c):
    """One complete receiver row; default symbol 1 includes self and far centers."""
    positions, axes, offsets = geometry['q'], geometry['axis'], geometry['offsets']
    n = len(positions)
    symbols = np.ones((n, 4), dtype=np.uint8)
    delta = positions-positions[i]
    center = np.hypot(np.hypot(delta[:, 0], delta[:, 1]), delta[:, 2])
    invalid_center = (~np.isfinite(center) | (center > 512) |
                      (np.max(np.abs(delta), axis=1) > 257))
    invalid_center[i] = False
    symbols[invalid_center] = 11
    eligible = (~invalid_center) & (center < c['neighbor'])
    eligible[i] = False
    source_ids = np.flatnonzero(eligible)
    sparse_rows = []
    for r in range(4):
        d = positions[source_ids]-(positions[i]+offsets[i, r])
        source_axes = axes[source_ids]
        code = np.zeros(len(source_ids), dtype=np.uint8)
        values = np.zeros(len(source_ids), dtype=np.float64)
        active = np.all(np.isfinite(d), axis=1) & (np.max(np.abs(d), axis=1) <= 258)
        code[~active] = 11
        down = ((d[:, 0]*source_axes[:, 0]+d[:, 1]*source_axes[:, 1])+
                d[:, 2]*source_axes[:, 2])
        bad = active & (~np.isfinite(down) | (np.abs(down) > 1024))
        code[bad] = 11
        active &= ~bad
        behind = active & (down <= 0)
        code[behind] = 2
        active &= ~behind
        beyond = active & (down >= c['downCut'])
        code[beyond] = 3
        active &= ~beyond
        normal = d-down[:, None]*source_axes
        radial = np.hypot(np.hypot(normal[:, 0], normal[:, 1]), normal[:, 2])
        bad = active & (~np.isfinite(radial) | (radial > 2048))
        code[bad] = 11
        active &= ~bad
        near = active & (down < c['minDown']*c['D'])
        code[near & (radial < c['nearRad'])] = 4
        code[near & (radial >= c['nearRad'])] = 5
        active &= ~near
        normalized = down/c['D']
        width = c['spread']*(normalized-c['origin'])*c['D']
        bad = active & (~np.isfinite(width) | (width <= 0))
        code[bad] = 11
        active &= ~bad
        outside = active & (radial >= c['radCut']*width)
        code[outside] = 6
        active &= ~outside
        at = np.flatnonzero(active)
        if len(at):
            projection = np.maximum(0., ((axes[i, 0]*source_axes[at, 0] +
                                         axes[i, 1]*source_axes[at, 1]) +
                                        axes[i, 2]*source_axes[at, 2]))
            xi = (radial[at]/c['D'])/(c['spread']*(normalized[at]-c['origin']))
            denominator = 1+c['sqrt2minus1']*xi*xi
            speed = ((c['decay']/(normalized[at]-c['origin']))/(denominator*denominator) *
                     c['induced'] * fade(down[at], c['downFade'], c['downCut']) *
                     fade(radial[at]/width[at], c['radFade'], c['radCut']) * projection)
            good = np.isfinite(speed) & (speed >= 0) & (speed <= 128) & np.isfinite(projection)
            code[at[~good]] = 11
            admitted = at[good]
            values[admitted] = speed[good]
            code[admitted] = np.where(projection[good] <= 0, 7,
                                      np.where(speed[good] > 0, 8, 9)).astype(np.uint8)
        if np.any(code == 0):
            raise ArithmeticError('unclassified eligible pair')
        symbols[source_ids, r] = code
        positive = values > 0
        sparse_rows.append((source_ids[positive], values[positive]))
    return symbols, sparse_rows, dict(centerDistanceCalls=n-1,
                                      eligibleCenterPairs=len(source_ids),
                                      invalidCenterPairs=int(np.count_nonzero(invalid_center)),
                                      pairTermCalls=4*len(source_ids))


def positive_root(alpha):
    """Hyperbolic cubic root, with algebraic scaling to avoid overflow.

    x=2*sqrt(alpha/3)*sinh(asinh(3*sqrt(3)/(2*alpha**1.5))/3).
    The small-argument branch uses the equivalent product of sinh(t)/t and
    asinh(z)/z, whose removable limits at zero are one. No Newton/bisection.
    """
    alpha = np.asarray(alpha, dtype=np.float64)
    if not np.all(np.isfinite(alpha) & (alpha >= 0)):
        raise ValueError('non-finite or negative alpha')
    output = np.ones_like(alpha)
    positive = alpha > 0
    a = alpha[positive]
    if not a.size:
        return output
    loga = np.log(a)
    logz = math.log(3*math.sqrt(3)/2)-1.5*loga
    roots = np.empty_like(a)
    small = logz < 0
    if np.any(small):
        z = np.exp(logz[small])
        h = np.arcsinh(z)
        t = h/3
        ratio1 = np.ones_like(t)
        ratio2 = np.ones_like(z)
        np.divide(np.sinh(t), t, out=ratio1, where=t != 0)
        np.divide(h, z, out=ratio2, where=z != 0)
        roots[small] = (1/a[small])*ratio1*ratio2
    if np.any(~small):
        lz = logz[~small]
        h = lz+np.log1p(np.sqrt(1+np.exp(-2*lz)))
        t = h/3
        logsinh = t-math.log(2)+np.log(-np.expm1(-2*t))
        roots[~small] = np.exp(math.log(2)+.5*(loga[~small]-math.log(3))+logsinh)
    if not np.all(np.isfinite(roots) & (roots > 0)):
        raise ArithmeticError('hyperbolic root left representable positive domain')
    output[positive] = roots
    return output


def csr_map(y, f0, s0, offsets, sources, a):
    """Independent segmented sparse sums; differs from candidate sequential sums."""
    counts = np.diff(offsets)
    products = a*y[sources]
    # Sentinel permits empty rows at the end; reduceat's empty-row behavior is masked.
    padded = np.r_[products, 0.]
    alpha = np.add.reduceat(padded, offsets[:-1])
    alpha[counts == 0] = 0.
    alpha = alpha.reshape((-1, 4))
    x = positive_root(alpha)
    forces = f0*x
    weights = f0/s0[:, None]
    return dict(y=np.sqrt(np.sum(weights*x, axis=1)), alpha=alpha, x=x, T=forces)


def direct_solve(order, f0, s0, offsets, sources, a, guard):
    n = len(f0)
    y = np.ones(n, dtype=np.float64)
    alpha = np.zeros((n, 4), dtype=np.float64)
    x = np.ones((n, 4), dtype=np.float64)
    forces = np.empty((n, 4), dtype=np.float64)
    for i in order:
        guard()
        for r in range(4):
            row = 4*i+r
            start, stop = int(offsets[row]), int(offsets[row+1])
            alpha[i, r] = np.sum(a[start:stop]*y[sources[start:stop]])
        x[i] = positive_root(alpha[i])
        forces[i] = f0[i]*x[i]
        y[i] = math.sqrt(math.fsum(float(v) for v in (f0[i]/s0[i])*x[i]))
    return dict(y=y, alpha=alpha, x=x, T=forces)


class Audit:
    def __init__(self):
        self.started = time.monotonic()
        self.checks = []
        self.failures = []
        self.frames = []

    def guard(self):
        if time.monotonic()-self.started >= 230:
            raise RuntimeError('independent review cooperative 230-second wall guard reached')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        if rss > 1.5*(1 << 30):
            raise RuntimeError('independent review RSS guard reached')

    def check(self, passed, name, details=None):
        record = dict(name=name, passed=bool(passed))
        if details is not None:
            record['details'] = details
        self.checks.append(record)
        if not passed:
            self.failures.append(name)

    def close(self, actual, expected, name):
        a, b = np.asarray(actual), np.asarray(expected)
        good = a.shape == b.shape
        if good:
            good = np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(
                np.abs(a-b) <= COEFFICIENT_ATOL+COEFFICIENT_RTOL*np.abs(b))
        self.check(good, name)

    def relative(self, actual, expected, name):
        a, b = np.asarray(actual), np.asarray(expected)
        good = a.shape == b.shape
        maximum_error = None
        if good:
            good = np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(b > 0) and np.all(
                np.abs(a-b) <= SOLUTION_RTOL*np.abs(b))
            if np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(b > 0):
                maximum_error = float(np.max(np.abs(a-b)/np.abs(b), initial=0.))
        self.check(good, name, dict(maximumRelativeError=maximum_error))


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while True:
            chunk = stream.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def read_exact(stream, count):
    chunks, received = [], 0
    while received < count:
        chunk = stream.read(count-received)
        if not chunk:
            raise EOFError('short compressed symbol row')
        chunks.append(chunk)
        received += len(chunk)
    return b''.join(chunks)


EXPECTED_CASES = [('n1000-t20', 1000, 20), ('n5000-t20', 5000, 20),
                  ('n5000-t60', 5000, 60), ('n5000-t180', 5000, 180)]
EXPECTED_SOURCE_PINS = {
    'n1000-t20': (470998, '8adc8213f6b036f498639bf070af53d3777fe1771c34f41bb54498e48be0f304'),
    'n5000-t20': (2357471, '64696f6aca0d74a00f8540f53abcb46b4bd8dd6ed387f5192506c84967ab267e'),
    'n5000-t60': (2351516, '9538f037be4a62abb9a550c7ac2a7aa182556c448136c86d66d1e09492fd050b'),
    'n5000-t180': (2349503, '1a4ba3d4cf3ffee87f783a2ba7e40865a438b342ff71e3ace16e5341ef208af4')}
MAX_TERMS = 2_000_000
MAX_OUTPUT_BYTES = 256*(1 << 20)


def required(condition, message):
    if not condition:
        raise ValueError(message)


def load_json(path):
    required(path.stat().st_size <= MAX_OUTPUT_BYTES, 'JSON size limit exceeded')
    def reject_constant(value):
        raise ValueError('nonfinite JSON token: '+value)
    with path.open('r', encoding='utf-8') as stream:
        return json.load(stream, parse_constant=reject_constant)


def json_safe(value):
    """Keep diagnostic nonfinite values visible without emitting invalid JSON."""
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def safe_error(error, package):
    return dict(type=type(error).__name__, message=str(error).replace(str(package), '<package>'))


def diagnostic_scalar(value):
    """The schema encodes unavailable nonfinite scalar maxima/bounds as null."""
    value = float(value)
    return value if math.isfinite(value) else None


def package_path(package, relative):
    required(isinstance(relative, str) and relative != '', 'missing artifact path')
    rel = Path(relative)
    required(not rel.is_absolute() and '..' not in rel.parts, 'nonrelative artifact path')
    path = (package/rel).resolve()
    required(path.is_relative_to(package) and path.is_file(), 'artifact absent or outside package')
    return path


def valid_hash(value):
    return (isinstance(value, str) and len(value) == 64 and
            all(ch in '0123456789abcdef' for ch in value))


def compare_fields(audit, actual, expected, prefix):
    """Compare only required fields; extra descriptive fields are allowed."""
    required(isinstance(actual, dict), prefix+' must be an object')
    for key, wanted in expected.items():
        name = prefix+'.'+key
        if key not in actual:
            audit.check(False, name+' present')
            continue
        got = actual[key]
        if isinstance(wanted, dict):
            compare_fields(audit, got, wanted, name)
        elif isinstance(wanted, float):
            audit.close(got, wanted, name)
        elif isinstance(wanted, bool):
            audit.check(type(got) is bool and got == wanted, name)
        elif isinstance(wanted, int):
            audit.check(type(got) is int and got == wanted, name)
        else:
            audit.check(got == wanted, name)


def verify_artifact(audit, package, metadata, prefix, expected_bytes=None):
    required(isinstance(metadata, dict), prefix+' artifact metadata missing')
    path = package_path(package, metadata.get('path'))
    size = path.stat().st_size
    audit.check(type(metadata.get('bytes')) is int and metadata['bytes'] == size,
                prefix+'.bytes')
    if expected_bytes is not None:
        required(size == expected_bytes, prefix+' byte length does not match shape')
    required(size <= MAX_OUTPUT_BYTES, prefix+' file size limit exceeded')
    digest = sha256_file(path)
    audit.check(valid_hash(metadata.get('sha256')) and metadata['sha256'] == digest,
                prefix+'.sha256')
    return path


def load_csr(audit, package, metadata, n, prefix):
    required(isinstance(metadata, dict), 'CSR metadata absent')
    objects = [metadata.get(k) for k in ('offsets', 'sources', 'K')]
    required(all(isinstance(obj, dict) for obj in objects), 'CSR members absent')
    shape = objects[1].get('shape')
    required(isinstance(shape, list) and len(shape) == 1 and type(shape[0]) is int,
             'CSR sources shape malformed')
    m = shape[0]
    required(0 <= m <= MAX_TERMS, 'CSR term count violates cap')
    arrays = []
    for name, obj, dtype, width, expected_shape, encoding in [
            ('offsets', objects[0], '<u4', 4, [4*n+1], 'uint32le'),
            ('sources', objects[1], '<u4', 4, [m], 'uint32le'),
            ('K', objects[2], '<f8', 8, [m], 'float64le')]:
        compare_fields(audit, obj, dict(shape=expected_shape, encoding=encoding), prefix+'.'+name)
        path = verify_artifact(audit, package, obj, prefix+'.'+name, width*expected_shape[0])
        arrays.append(np.fromfile(path, dtype=dtype))
    offsets, sources, k = arrays
    offsets = offsets.astype(np.int64)
    required(offsets[0] == 0 and offsets[-1] == m and np.all(np.diff(offsets) >= 0),
             'CSR offsets are not a valid row partition')
    required(np.all(sources < n), 'CSR source id out of bounds')
    audit.check(np.all(np.isfinite(k) & (k > 0)), prefix+'.positive-finite-K')
    return offsets, sources, k


def input_census(states, g, c):
    finite = bool(np.all(np.isfinite(states)))
    qe = np.abs(g['qnorm']-1)
    ae = np.abs(g['anorm']-1)
    oe = np.abs(g['onorm']-c['D']/2)
    od = np.abs(g['perpendicular'])
    qb = int(np.count_nonzero(~np.isfinite(qe) | (qe > 1e-10)))
    ab = int(np.count_nonzero(~np.isfinite(ae) | (ae > 1e-9)))
    ob = int(np.count_nonzero(~np.isfinite(oe) | ~np.isfinite(od) |
                              (oe > 1e-9) | (od > 1e-9)))
    tilt_degrees = g['tilt']*(180/math.pi)
    return dict(finite=finite, quaternionNormMaxError=diagnostic_scalar(np.max(qe)),
                quaternionBadCount=qb, axisNormMaxError=diagnostic_scalar(np.max(ae)),
                axisBadCount=ab, offsetNormMaxError=diagnostic_scalar(np.max(oe)),
                offsetDotMaxAbs=diagnostic_scalar(np.max(od)), offsetBadCount=ob,
                nominalZeroCount=int(np.count_nonzero(g['f0'] == 0)),
                nominalNegativeCount=int(np.count_nonzero(g['f0'] < 0)),
                nominalPositive=bool(np.all(np.isfinite(g['f0']) & (g['f0'] > 0))),
                nominalTotalFinite=bool(np.all(np.isfinite(g['S0']))),
                geometryValid=bool(finite and qb == 0 and ab == 0 and ob == 0),
                maxTiltDegrees=diagnostic_scalar(np.max(tilt_degrees)),
                tiltWithin45Count=int(np.count_nonzero(tilt_degrees <= 45)))


def graph_census(positions, dependencies):
    n = len(positions)
    order = np.lexsort((np.arange(n), -positions[:, 2]))
    rank = np.empty(n, dtype=np.int64)
    rank[order] = np.arange(n)
    incoming = [len(sources) for sources in dependencies]
    height_violations = sum(int(np.count_nonzero(positions[sources, 2] <= positions[i, 2]))
                            for i, sources in enumerate(dependencies))
    order_violations = sum(int(np.count_nonzero(rank[sources] >= rank[i]))
                           for i, sources in enumerate(dependencies))
    eligible = order_violations == 0
    depth = None
    if eligible:
        depth = np.zeros(n, dtype=np.int64)
        for i in order:
            sources = dependencies[i]
            if len(sources):
                depth[i] = 1+np.max(depth[sources])
    return dict(uniqueVehicleEdges=sum(incoming), incomingDegree=incoming,
                maxIncomingDegree=max(incoming), heightViolationEdges=height_violations,
                orderViolationEdges=order_violations, descendingEligible=eligible,
                order=order.tolist(), dependencyDepth=None if depth is None else depth.tolist(),
                maxDependencyDepth=None if depth is None else int(np.max(depth)))


def rotor_arrays(record, n):
    rotors = record.get('rotors')
    required(isinstance(rotors, list) and len(rotors) == n and
             all(isinstance(row, list) and len(row) == 4 for row in rotors),
             'rotor record shape mismatch')
    arrays = {key: np.array([[item[key] for item in row] for row in rotors], dtype=float)
              for key in ('alpha', 'x', 'T')}
    return arrays


def compare_map(audit, record, expected, n, name):
    required(isinstance(record, dict), name+' record absent')
    audit.relative(record.get('y'), expected['y'], name+'.all-y')
    arrays = rotor_arrays(record, n)
    audit.close(arrays['alpha'], expected['alpha'], name+'.all-alpha')
    audit.relative(arrays['x'], expected['x'], name+'.all-x')
    audit.relative(arrays['T'], expected['T'], name+'.all-T')
    audit.check(np.all(np.isfinite(arrays['alpha']) & (arrays['alpha'] >= 0)), name+'.alpha-domain')
    audit.check(np.all(np.isfinite(arrays['x']) & (arrays['x'] > 0) & (arrays['x'] <= 1)),
                name+'.root-domain')
    return arrays


def audit_solutions(audit, saved, g, offsets, sources, a, graph, prefix):
    n, m = len(g['f0']), len(a)
    required(np.all(np.isfinite(a) & (a >= 0)), 'nonfinite or negative a cannot enter load solve')
    def map_work(values):
        return dict(rootClosures=4*n,
                    bisectionIterations=56*int(np.count_nonzero(values['alpha'] > 0)),
                    positiveTermMultiplications=m)
    expected_direct = direct_solve(graph['order'], g['f0'], g['S0'], offsets, sources, a, audit.guard)
    required(isinstance(saved, dict), 'admitted eligible case has no solutions')
    summaries = {}
    for name in ('direct', 'picard'):
        audit.guard()
        sol = saved.get(name)
        required(isinstance(sol, dict), name+' solution absent')
        y = np.asarray(sol.get('y'), dtype=float)
        required(y.shape == (n,) and np.all(np.isfinite(y) & (y > 0)),
                 name+' source amplitude domain or shape failure')
        iterations = 1
        generating = expected_direct
        expected_work = map_work(generating)
        if name == 'picard':
            iterations = sol.get('iterations')
            required(type(iterations) is int and 1 <= iterations <= 64, 'Picard iteration count invalid')
            iterates = np.asarray(sol.get('iterates'), dtype=float)
            required(iterates.shape == (iterations+1, n), 'Picard iterate shape invalid')
            required(np.all(np.isfinite(iterates) & (iterates > 0)), 'Picard iterate domain invalid')
            audit.check(np.array_equal(iterates[0], np.ones(n)), prefix+'.picard.initial-all-ones')
            audit.check(np.array_equal(y, iterates[-1]), prefix+'.picard.returned-last-iterate')
            changes = np.max(np.abs(np.diff(np.log(iterates), axis=0)), axis=1)
            audit.check(np.all(changes[:-1] > 1e-11), prefix+'.picard.first-stop-only')
            converged = bool(changes[-1] <= 1e-11)
            compare_fields(audit, sol, dict(converged=converged, lastChange=float(changes[-1])),
                           prefix+'.picard')
            audit.check(converged, prefix+'.picard.converged-within-cap')
            audit.check(converged or iterations == 64, prefix+'.picard.cap-if-unconverged')
            # Check every synchronous update, including the final generating map.
            expected_work = dict(rootClosures=0, bisectionIterations=0, positiveTermMultiplications=0)
            for k in range(1, iterations+1):
                audit.guard()
                generating = csr_map(iterates[k-1], g['f0'], g['S0'], offsets, sources, a)
                audit.relative(iterates[k], generating['y'], prefix+'.picard.update-'+str(k))
                for key, value in map_work(generating).items():
                    expected_work[key] += value
        arrays = compare_map(audit, sol, generating, n, prefix+'.'+name+'.generating')
        audit.relative(y, expected_direct['y'], prefix+'.'+name+'.independent-direct-y')
        audit.relative(arrays['T'], expected_direct['T'], prefix+'.'+name+'.independent-direct-T')
        audit.relative(arrays['x'], expected_direct['x'], prefix+'.'+name+'.independent-direct-x')
        compare_fields(audit, sol.get('work'), expected_work, prefix+'.'+name+'.work')
        residual = csr_map(y, g['f0'], g['S0'], offsets, sources, a)
        compare_map(audit, sol.get('residualMap'), residual, n, prefix+'.'+name+'.residualMap')
        compare_fields(audit, sol.get('residualWork'), map_work(residual), prefix+'.'+name+'.residualWork')
        residual_log = float(np.max(np.abs(np.log(residual['y'])-np.log(y))))
        residual_total = ((residual['T'][:, 0]+residual['T'][:, 1])+
                          residual['T'][:, 2])+residual['T'][:, 3]
        mismatch = float(np.max(np.abs(g['S0']*y*y-residual_total)/g['S0']))
        compare_fields(audit, sol, dict(residualLog=residual_log, sourceReceiverMismatch=mismatch),
                       prefix+'.'+name)
        audit.check(residual_log <= 1e-9 and mismatch <= 2e-9,
                    prefix+'.'+name+'.independent-residual-small')
        summaries[name] = dict(iterations=iterations, independentResidualLog=residual_log,
                               independentSourceReceiverMismatch=mismatch,
                               allRotorForcesCompared=4*n, allAmplitudesCompared=n)
    return summaries


def audit_case(audit, package, entry, saved, c):
    ident, n, t = entry['id'], entry['n'], entry['t']
    before_errors = len(audit.failures)
    frame = dict(id=ident, complete=False, pass_=False)
    audit.frames.append(frame)
    prefix = ident
    path = verify_artifact(audit, package, entry, prefix+'.input-artifact', n*17*8)
    audit.check(valid_hash(entry.get('sourceSha256')) and type(entry.get('sourceBytes')) is int and
                entry['sourceBytes'] > 0, prefix+'.source-provenance-metadata')
    source_name = entry.get('source')
    audit.check(isinstance(source_name, str) and not Path(source_name).is_absolute() and
                '..' not in Path(source_name).parts, prefix+'.public-source-identity')
    expected_source = f'outputs/milestone-31-source/checkpoint-heldout-2001-{n}-wide-wall-priority-0.0025-{t}.json'
    source_bytes, source_sha = EXPECTED_SOURCE_PINS[ident]
    compare_fields(audit, entry, dict(source=expected_source, sourceBytes=source_bytes,
                                     sourceSha256=source_sha), prefix+'.source-pins')
    states = np.fromfile(path, dtype='<f8').reshape((n, 17))
    g = prepare_geometry(states, c)
    census = input_census(states, g, c)
    compare_fields(audit, saved, dict(id=ident, n=n, t=t, inputSha256=entry['sha256']), prefix)
    compare_fields(audit, saved.get('input'), census, prefix+'.input')
    case_copy = load_json(package_path(package, 'results/'+ident+'.json'))
    audit.check(case_copy == saved, prefix+'.completed-case-matches-evidence')
    offsets, sources, k_saved = load_csr(audit, package, saved.get('csr'), n, prefix+'.csr')
    symbol_meta = saved.get('symbols')
    symbol_path = verify_artifact(audit, package, symbol_meta, prefix+'.symbols')
    audit.check(symbol_path.stat().st_size <= 64*(1 << 20), prefix+'.symbol-compressed-cap')
    compare_fields(audit, symbol_meta, dict(encoding='gzip-uint8', shape=[n, n, 4], rawBytes=4*n*n),
                   prefix+'.symbols')
    symbol_hash = hashlib.sha256()
    counts = np.zeros(12, dtype=np.int64)
    work = dict(directedCenterTests=0, centerEligiblePairs=0, centerGuardRejectedPairs=0,
                pairCalls=0, positiveRotorTerms=0)
    expected_sources, expected_k, expected_offsets = [], [], [0]
    dependencies = []
    symbol_mismatches = 0
    support_bad_rows, coefficient_bad_rows = 0, 0
    max_coefficient_error = 0.
    first_symbol_mismatches, first_support_rows, first_coefficient_rows = [], [], []
    with gzip.open(symbol_path, 'rb') as stream:
        for i in range(n):
            audit.guard()
            symbols, rows, row_work = classify_receiver(i, g, c)
            actual_bytes = read_exact(stream, 4*n)
            symbol_hash.update(actual_bytes)
            actual_symbols = np.frombuffer(actual_bytes, dtype=np.uint8).reshape((n, 4))
            bad_symbols = actual_symbols != symbols
            mismatch_count = int(np.count_nonzero(bad_symbols))
            symbol_mismatches += mismatch_count
            if mismatch_count and len(first_symbol_mismatches) < 16:
                for j, r in np.argwhere(bad_symbols)[:16-len(first_symbol_mismatches)]:
                    first_symbol_mismatches.append(dict(receiver=i, source=int(j), rotor=int(r),
                                                        saved=int(actual_symbols[j, r]),
                                                        independent=int(symbols[j, r])))
            counts += np.bincount(symbols.ravel(), minlength=12)
            work['directedCenterTests'] += row_work['centerDistanceCalls']
            work['centerEligiblePairs'] += row_work['eligibleCenterPairs']
            work['centerGuardRejectedPairs'] += row_work['invalidCenterPairs']
            work['pairCalls'] += row_work['pairTermCalls']
            dependencies.append(np.unique(np.concatenate([ids for ids, values in rows])))
            for r, (ids, values) in enumerate(rows):
                row = 4*i+r
                start, stop = int(offsets[row]), int(offsets[row+1])
                support_equal = np.array_equal(sources[start:stop], ids)
                if not support_equal:
                    support_bad_rows += 1
                    if len(first_support_rows) < 16:
                        first_support_rows.append(row)
                else:
                    errors = np.abs(k_saved[start:stop]-values)
                    if len(errors):
                        max_coefficient_error = max(max_coefficient_error, float(np.max(errors)))
                    coefficients_equal = np.all(np.isfinite(k_saved[start:stop])) and np.all(
                        errors <= COEFFICIENT_ATOL+COEFFICIENT_RTOL*np.abs(values))
                    if not coefficients_equal:
                        coefficient_bad_rows += 1
                        if len(first_coefficient_rows) < 16:
                            first_coefficient_rows.append(row)
                expected_sources.append(ids)
                expected_k.append(values)
                expected_offsets.append(expected_offsets[-1]+len(ids))
                required(expected_offsets[-1] <= MAX_TERMS, 'independent positive term cap exceeded')
        audit.check(stream.read(1) == b'', prefix+'.symbols.no-trailing-raw-bytes')
    audit.check(symbol_hash.hexdigest() == symbol_meta.get('rawSha256'), prefix+'.symbols.rawSha256')
    audit.check(symbol_mismatches == 0, prefix+'.all-symbols-exact',
                dict(mismatchCount=symbol_mismatches, first=first_symbol_mismatches))
    audit.check(support_bad_rows == 0, prefix+'.all-csr-support-exact',
                dict(mismatchRows=support_bad_rows, first=first_support_rows))
    audit.check(coefficient_bad_rows == 0, prefix+'.all-K-within-tolerance',
                dict(mismatchRows=coefficient_bad_rows, first=first_coefficient_rows,
                     maximumAbsoluteError=max_coefficient_error))
    audit.check(counts[0] == 0 and counts.sum() == 4*n*n, prefix+'.complete-terminal-symbol-census')
    compare_fields(audit, saved, dict(symbolCounts=counts.tolist()), prefix)
    independent_offsets = np.asarray(expected_offsets, dtype=np.int64)
    independent_sources = np.concatenate(expected_sources)
    independent_k = np.concatenate(expected_k)
    work['positiveRotorTerms'] = len(independent_k)
    compare_fields(audit, saved.get('geometryWork'), work, prefix+'.geometryWork')
    graph = graph_census(g['q'], dependencies)
    compare_fields(audit, saved.get('graph'), graph, prefix+'.graph')
    nominal_ok = census['nominalPositive'] and census['nominalTotalFinite']
    a = None
    cap_max = cap_violations = lmax = None
    if nominal_ok:
        scales = np.sqrt(g['S0']/c['mg'])
        scaled = independent_k*scales[independent_sources]
        cap_max = diagnostic_scalar(np.max(scaled, initial=0.))
        cap_violations = int(np.count_nonzero(~np.isfinite(scaled) | (scaled > 128)))
        row_ids = np.repeat(np.arange(4*n), np.diff(independent_offsets))
        nominal_induced = np.sqrt(g['f0'].ravel()/(2*c['rho']*c['area']))
        a = scaled/nominal_induced[row_ids]
        row_sums = np.bincount(row_ids, weights=a, minlength=4*n)
        lmax = diagnostic_scalar(np.max(row_sums)/(4*math.sqrt(2)))
    reasons = []
    if not census['geometryValid']:
        reasons.append('geometry')
    if not nominal_ok:
        reasons.append('nominal')
    if counts[4]:
        reasons.append('near-field')
    if counts[11]:
        reasons.append('invalid-term')
    if cap_violations:
        reasons.append('scaled-cap')
    admission = dict(admitted=not reasons, reasons=reasons, unsupportedNearCount=int(counts[4]),
                     invalidTermCount=int(counts[11]), scaledCapMax=cap_max,
                     scaledCapViolationCount=cap_violations)
    compare_fields(audit, saved.get('admission'), admission, prefix+'.admission')
    compare_fields(audit, saved, dict(ordinaryLmax=lmax), prefix)
    solution_summary = None
    if admission['admitted'] and graph['descendingEligible']:
        geometry_review_ok = len(audit.failures) == before_errors
        has_solution = isinstance(saved.get('solutions'), dict)
        audit.check(has_solution, prefix+'.admitted-topological-solution-present')
        if geometry_review_ok and has_solution:
            solution_summary = audit_solutions(audit, saved['solutions'], g, independent_offsets,
                                               independent_sources, a, graph, prefix)
        else:
            solution_summary = dict(skipped=True, reason='prior-case-audit-failed-or-solution-absent')
    else:
        audit.check(saved.get('solutions') is None and 'solutions' in saved,
                    prefix+'.no-solve-outside-admitted-topological-domain')
    frame.update(complete=True, pass_=len(audit.failures) == before_errors, n=n, t=t,
                 admission=admission, input=census, symbolEntriesCompared=4*n*n,
                 symbolMismatchCount=symbol_mismatches, csrSupportMismatchRows=support_bad_rows,
                 coefficientMismatchRows=coefficient_bad_rows,
                 maximumAbsoluteCoefficientError=max_coefficient_error,
                 geometryWork=work,
                 graph={key: graph[key] for key in ('uniqueVehicleEdges', 'maxIncomingDegree',
                        'heightViolationEdges', 'orderViolationEdges', 'descendingEligible',
                        'maxDependencyDepth')}, ordinaryLmax=lmax, solutions=solution_summary)


def run_review(audit, package, review_output):
    index = load_json(package_path(package, 'inputs/index.json'))
    evidence = load_json(package_path(package, 'results/evidence.json'))
    audit.check(evidence.get('complete') is True, 'evidence.complete')
    audit.check(not (package/'results/failure.json').exists(), 'no-candidate-failure-record')
    audit.check(isinstance(evidence.get('runtime'), dict) and
                isinstance(evidence['runtime'].get('node'), str), 'candidate.runtime.node-recorded')
    entries, cases = index.get('cases'), evidence.get('cases')
    required(isinstance(entries, list) and isinstance(cases, list), 'case tables absent')
    expected_ids = [item[0] for item in EXPECTED_CASES]
    audit.check([entry.get('id') for entry in entries] == expected_ids, 'fixed-input-order-and-coverage')
    audit.check([case.get('id') for case in cases] == expected_ids, 'fixed-evidence-order-and-coverage')
    c = constants()
    nested = {key: value for key, value in c.items() if key not in ('mg', 'arm', 'radius', 'rho', 'area')}
    compare_fields(audit, evidence.get('constants'),
                   dict(mg=c['mg'], arm=c['arm'], radius=c['radius'], rho=c['rho'],
                        A=c['area'], R=c['D']/2, c=nested), 'constants')
    output_bytes = normal_bytes = 0
    bookkeeping = {'stdout.txt', 'stderr.txt', 'invocation.lock', 'run.json',
                   'review-stdout.txt', 'review-stderr.txt', 'review-invocation.lock',
                   'review-run.json', 'independent-review.json'}
    for path in (package/'results').rglob('*'):
        if path.is_file():
            required(path.resolve().is_relative_to(package), 'result symlink escapes package')
            relative = path.relative_to(package/'results')
            if (len(relative.parts) == 1 and relative.name in bookkeeping) or path.resolve() == review_output:
                continue
            size = path.stat().st_size
            output_bytes += size
            if str(relative) not in ('failure.json', 'partial-evidence.json'):
                normal_bytes += size
    audit.check(output_bytes <= MAX_OUTPUT_BYTES, 'candidate.total-output-byte-cap', dict(bytes=output_bytes))
    audit.check(normal_bytes <= 255*(1 << 20), 'candidate.normal-science-byte-cap', dict(bytes=normal_bytes))
    for ident, n, t in EXPECTED_CASES:
        audit.guard()
        matching_entries = [entry for entry in entries if entry.get('id') == ident]
        matching_cases = [case for case in cases if case.get('id') == ident]
        try:
            required(len(matching_entries) == len(matching_cases) == 1, ident+' absent or duplicated')
            entry, saved = matching_entries[0], matching_cases[0]
            required(entry.get('n') == n and entry.get('t') == t, ident+' dimensions/time differ from protocol')
            audit_case(audit, package, entry, saved, c)
        except Exception as error:
            # Preserve completed comparisons and continue to the next fixed case.
            audit.check(False, ident+'.review-error', safe_error(error, package))
            if not audit.frames or audit.frames[-1]['id'] != ident:
                audit.frames.append(dict(id=ident, complete=False, pass_=False))
            audit.frames[-1]['error'] = safe_error(error, package)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('output_json', type=Path)
    args = parser.parse_args()
    # Exclusive output creation preserves the once-only run record on later failure.
    with args.output_json.open('x', encoding='utf-8') as output:
        audit = Audit()
        package = args.package.absolute()
        try:
            package = args.package.resolve(strict=True)
            required(package.is_dir(), 'package path is not a directory')
            run_review(audit, package, args.output_json.resolve())
        except Exception as error:
            audit.check(False, 'review-fatal-error', safe_error(error, package))
        for frame in audit.frames:
            frame['pass'] = frame.pop('pass_')
        result = dict(schema='m31-swarm-independent-review-v1',
                      **{'pass': not audit.failures and len(audit.frames) == 4 and
                         all(frame['complete'] for frame in audit.frames)},
                      checkCount=len(audit.checks), passedChecks=sum(check['passed'] for check in audit.checks),
                      errors=audit.failures, cases=audit.frames, checks=audit.checks,
                      elapsedSeconds=time.monotonic()-audit.started,
                      reviewMethod=dict(geometry='independent NumPy receiver-row vector arithmetic',
                                        roots='positive hyperbolic closed form, no bisection or Newton',
                                        picard='every saved update and final generating/residual map',
                                        candidateCodeImported=False,
                                        symbolTolerance=0, coefficientAbsoluteTolerance=COEFFICIENT_ATOL,
                                        coefficientRelativeTolerance=COEFFICIENT_RTOL,
                                        solutionRelativeTolerance=SOLUTION_RTOL))
        json.dump(json_safe(result), output, allow_nan=False, indent=2)
        output.write('\n')
    print(json.dumps({'pass': result['pass'], 'checkCount': result['checkCount'],
                      'errorCount': len(result['errors'])}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
