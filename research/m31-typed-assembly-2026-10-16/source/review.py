#!/usr/bin/env python3
"""Independent A/L/T audit. Source construction is not permission to execute.

Fresh NumPy geometry and analytic roots for three newly frozen A inputs;
exact saved A/L/T comparisons, generation/ownership/schedule/timing audit.
No JavaScript imports, historical target rescoring, or automatic retries.
"""
import argparse
import gzip
import hashlib
import json
import math
import re
import resource
import statistics
import sys
import time
from pathlib import Path
import numpy as np

COEFFICIENT_ATOL=2e-12
COEFFICIENT_RTOL=2e-12
SOLUTION_RTOL=1e-9
MAX_TERMS=2_000_000
RSS_CAP=1610612736
COOPERATIVE_SECONDS=175
CASES=[('n1000-s260103-t2',1000,260103),('n5000-s260101-t2',5000,260101),('n5000-s260102-t2',5000,260102)]
PERMS=['ALT','LTA','TAL','TLA','ATL','LAT']
FULL_PHASES=['input','index','geometry','admission','setup','solve','residual','checksum','remainder']


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


def require(ok, text):
    if not ok:
        raise ValueError(text)


def safe_json(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: safe_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [safe_json(item) for item in value]
    return value


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def load_json(path):
    require(path.stat().st_size <= 132*(1 << 20), 'JSON exceeds result cap')
    def reject(value):
        raise ValueError('nonfinite JSON token '+value)
    with path.open(encoding='utf-8') as stream:
        return json.load(stream, parse_constant=reject)


def diagnostic_scalar(value):
    """The schema encodes unavailable nonfinite scalar maxima/bounds as null."""
    value = float(value)
    return value if math.isfinite(value) else None


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


def expected_controls():
    # Literal position tokens from the frozen prospective control specification;
    # no runtime geometry or generator is evaluated by this saved-only checker.
    out = []
    def add(ident, tokens, use_grid):
        out.append((ident, tokens, use_grid))
    for x, values in [('0', ['2.9999999999999996', '3', '3.0000000000000004']),
                      ('-6', ['-3.0000000000000004', '-3', '-2.9999999999999996'])]:
        for name, value in zip(['below', 'exact', 'above'], values):
            add('radius-'+x+'-'+name, [[x, '0', '0'], [value, '0', '0']], True)
    add('cell-below', [['0', '0', '0'], ['3.9999999999999996', '0.25', '0.5'], ['4', '0', '1']], True)
    add('cell-exact', [['0', '0', '0'], ['0.5', '4', '0.25'], ['1', '4', '0']], True)
    add('cell-above', [['0', '0', '0'], ['0.25', '0.5', '4.000000000000001'], ['0', '1', '4']], True)
    add('signed-zero', [['-0', '0', '0'], ['0', '-0', '0']], True)
    add('coarse-origin', [['0', '0', '0'], ['1', '0.25', '0.5'], ['4', '1', '2']], True)
    add('coarse-translated', [['1099511627776']*3,
        ['1099511627777', '1099511627776.25', '1099511627776.5'],
        ['1099511627780', '1099511627777', '1099511627778']], True)
    xs = ['0', '0.05', '0.1', '0.15000000000000002', '0.2', '0.25', '0.30000000000000004',
          '0.35000000000000003', '0.4', '0.45', '0.5', '0.55', '0.6000000000000001',
          '0.65', '0.7000000000000001', '0.75']
    add('dense-16', [[x, '0', ['0', '0.45', '0.9'][i % 3]] for i, x in enumerate(xs)], True)
    add('span-256', [['0', '0', '0'], ['256', '0', '0']], True)
    add('span-nextUp256', [['0', '0', '0'], ['256.00000000000006', '0', '0']], False)
    add('far-invalid258', [['0', '0', '0'], ['258', '0', '0']], False)
    add('nonfinite-nan', [['0', '0', '0'], ['NaN', '0', '0']], False)
    add('nonfinite-infinity', [['0', '0', '0'], ['Infinity', '0', '0']], False)
    add('overflow-span', [['-1.7976931348623157e+308', '0', '0'], ['1.7976931348623157e+308', '0', '0']], False)
    add('near-field', [['0', '0', '0'], ['0', '0', '0.02']], True)
    add('duplicates', [['1', '1', '1'], ['1', '1', '1']], True)
    return out


def check_work(audit, work, n, m, name):
    fields = ['logicalDirectedPairs', 'gatheredNonselfCandidates', 'directedCenterTests',
              'certifiedSkippedPairs', 'centerEligiblePairs', 'centerGuardRejectedPairs',
              'pairCalls', 'positiveRotorTerms']
    require(isinstance(work, dict) and all(key in work for key in fields), 'geometry work fields missing')
    audit.check(all(type(work[key]) is int and work[key] >= 0 for key in fields), name+'.nonnegative-integers')
    audit.check(work['logicalDirectedPairs'] == n*(n-1), name+'.logical-pairs')
    audit.check(work['gatheredNonselfCandidates'] == work['directedCenterTests'], name+'.gathered-tests')
    audit.check(work['directedCenterTests']+work['certifiedSkippedPairs'] == n*(n-1), name+'.skipped-accounting')
    audit.check(work['pairCalls'] == 4*work['centerEligiblePairs'], name+'.pair-calls')
    audit.check(work['centerEligiblePairs']+work['centerGuardRejectedPairs'] <= work['directedCenterTests'],
                name+'.center-partition')
    audit.check(work['positiveRotorTerms'] == m and m <= 2_000_000, name+'.positive-terms')


def check_certificate(audit, cert, work, mode, name, expected_grid=None):
    require(isinstance(cert, dict), 'certificate absent')
    if mode == 'all':
        wanted = dict(finite=None, min=None, max=None, spans=None, certified=None,
                      useGrid=False, fallback=False, reason='all-pairs-selected')
        audit.check(cert == wanted, name+'.all-pairs-certificate')
    else:
        use = cert.get('useGrid')
        audit.check(type(use) is bool and cert.get('certified') == use and cert.get('fallback') is (not use),
                    name+'.grid-fallback-flags')
        if expected_grid is not None:
            audit.check(use is expected_grid, name+'.expected-grid')
        if use:
            spans = cert.get('spans')
            audit.check(cert.get('finite') is True and isinstance(spans, list) and len(spans) == 3 and
                        all(finite(x) and 0 <= x <= 256 for x in spans), name+'.grid-span-premise')
    if not cert.get('useGrid'):
        audit.check(work['certifiedSkippedPairs'] == 0, name+'.fallback-skips-none')
    else:
        audit.check(work['centerGuardRejectedPairs'] == 0, name+'.certified-no-center-guard-rejects')


def validate_csr(audit, offsets, sources, k, n, name):
    require(offsets.shape == (4*n+1,), 'CSR offsets shape mismatch')
    require(sources.shape == k.shape and offsets[0] == 0 and offsets[-1] == len(sources) and
            np.all(np.diff(offsets.astype(np.int64)) >= 0), 'invalid CSR row partition')
    audit.check(np.all(sources < n) and np.all(np.isfinite(k) & (k > 0)), name+'.valid-positive-CSR')
    ordered = True
    for row in range(4*n):
        ids = sources[int(offsets[row]):int(offsets[row+1])]
        if len(ids) > 1 and not np.all(ids[1:] > ids[:-1]):
            ordered = False
            break
    audit.check(ordered, name+'.strict-source-order')


def rotor_values(solution, n):
    y = np.asarray(solution['y'], dtype=float)
    require(y.shape == (n,), 'amplitude shape mismatch')
    def block(rotors):
        require(len(rotors) == n and all(len(row) == 4 for row in rotors), 'rotor shape mismatch')
        return np.asarray([[[item[key] for key in ('alpha', 'x', 'T')] for item in row] for row in rotors], dtype=float)
    rotors = block(solution['rotors'])
    residual_y = np.asarray(solution['residualMap']['y'], dtype=float)
    require(residual_y.shape == (n,), 'residual amplitude shape mismatch')
    residual_rotors = block(solution['residualMap']['rotors'])
    return np.concatenate((y, rotors.ravel(), residual_y, residual_rotors.ravel())), y, rotors, residual_y


def saved_checksum(solution, kvals):
    # Arithmetic over already saved outputs only; no map or root evaluation.
    value = 0.
    for i, y in enumerate(solution['y']):
        total = 0.
        for rotor in solution['rotors'][i]:
            total += rotor['T']
        value += y*(i+1)+total
    return (value+(float(kvals[0]) if len(kvals) else 0.))+(float(kvals[-1]) if len(kvals) else 0.)


required = require

class Audit:
    def __init__(self, package):
        self.package=package
        self.root=package.parent.parent
        self.started=time.monotonic()
        self.checks=[]
        self.errors=[]
        self.qualified={}
        self.calls=[]
        self.generation=[]
        self.controls=[]
        self.frames=[]
        self.resources={}
        self.evidence={}
    def guard(self):
        require(time.monotonic()-self.started < COOPERATIVE_SECONDS, 'new reviewer 175-second cooperative cap')
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin': rss*=1024
        require(rss<=RSS_CAP, 'new reviewer RSS cap')
    def check(self, ok, name, details=None):
        rec={'name':name,'pass':bool(ok)}
        if details is not None: rec['details']=safe_json(details)
        self.checks.append(rec)
        if not ok: self.errors.append(name)
        return bool(ok)
    def error(self, name, error):
        message=str(error).replace(str(self.package),'<package>').replace(str(self.root),'<repo>')
        self.check(False,name,{'type':type(error).__name__,'message':message})
    def numeric(self, actual, expected, name, atol=2e-12, rtol=2e-12):
        a,b=np.asarray(actual,dtype=float),np.asarray(expected,dtype=float)
        if a.shape!=b.shape:
            self.check(False,name,{'actualShape':list(a.shape),'expectedShape':list(b.shape)})
            return False
        with np.errstate(invalid='ignore',over='ignore'):
            d=np.abs(a-b)
            bad=~(np.isfinite(a)&np.isfinite(b)) | (d>atol+rtol*np.abs(b))
        ids=np.flatnonzero(bad.ravel())
        details={'length':int(a.size),'bad':int(ids.size),'maxAbs':float(np.max(d,initial=0.))}
        if ids.size:
            i=int(ids[0]);details['first']={'index':i,'actual':float(a.ravel()[i]),'expected':float(b.ravel()[i])}
        return self.check(not ids.size,name,details)
    def close(self, actual, expected, name, atol=2e-12, rtol=2e-12):
        return self.numeric(actual,expected,name,atol,rtol)
    def relative(self, actual, expected, name):
        return self.numeric(actual,expected,name,0.,1e-9)
    def exact(self, actual, expected, name):
        # Numeric JSON arrays may contain signed zeros: compare their binary64 representation.
        return self.check(canonical(actual)==canonical(expected),name)
    def path(self, base, relative):
        require(isinstance(relative,str) and relative,'artifact path absent')
        rel=Path(relative)
        require(not rel.is_absolute() and '..' not in rel.parts,'artifact path escapes')
        p=(base/rel).resolve()
        require(p.is_relative_to(base.resolve()) and p.is_file(),'artifact missing or outside base')
        return p
    def digest(self,path):
        h=hashlib.sha256()
        with path.open('rb') as f:
            for b in iter(lambda:f.read(1<<20),b''):
                self.guard();h.update(b)
        return h.hexdigest()
    def pin(self, base, meta, name, size=None):
        require(isinstance(meta,dict),'artifact metadata absent')
        p=self.path(base,meta.get('path'))
        self.check(type(meta.get('bytes')) is int and meta['bytes']==p.stat().st_size,name+'.bytes')
        if size is not None: require(p.stat().st_size==size,name+' shape bytes')
        require(p.stat().st_size<=256*(1<<20),'artifact file cap')
        self.check(valid_sha(meta.get('sha256')) and self.digest(p)==meta['sha256'],name+'.sha256')
        return p

def canonical(value):
    if isinstance(value,bool) or value is None or isinstance(value,str): return (type(value).__name__,value)
    if isinstance(value,(int,float)):
        return ('number',np.float64(value).tobytes())
    if isinstance(value,list): return ('list',tuple(canonical(x) for x in value))
    if isinstance(value,dict): return ('dict',tuple((k,canonical(value[k])) for k in sorted(value)))
    raise TypeError('unsupported canonical value')

def read_array(audit,meta,dtype,count,name):
    p=audit.pin(audit.package,meta,name,count*np.dtype(dtype).itemsize)
    return np.fromfile(p,dtype=dtype)

def bundle(audit,doc,name):
    n=doc['n'];a=doc['artifacts']
    m=a['sources']['bytes']//4
    require(type(n) is int and 0<n<=5000 and 0<=m<=MAX_TERMS,'bundle dimensions')
    off=read_array(audit,a['offsets'],'<u4',4*n+1,name+'.offsets').astype(np.int64)
    src=read_array(audit,a['sources'],'<u4',m,name+'.sources')
    k=read_array(audit,a['K'],'<f8',m,name+'.K')
    aa=read_array(audit,a['a'],'<f8',m,name+'.a')
    validate_csr(audit,off,src,k,n,name)
    audit.check(np.all(np.isfinite(aa)&(aa>0)),name+'.positive-a')
    check_work(audit,doc['geometryWork'],n,m,name+'.work')
    check_certificate(audit,doc['certificate'],doc['geometryWork'],'all',name+'.certificate')
    sy=audit.pin(audit.package,a['symbols'],name+'.symbols')
    require(a['symbols'].get('rawBytes')==4*n*n,'raw symbol size')
    require(sy.stat().st_size<=64*(1<<20),'compressed symbol cap')
    audit.check(valid_sha(doc.get('matrixHash')) and valid_sha(doc.get('solutionHash')),name+'.fingerprint-format')
    return {'doc':doc,'n':n,'m':m,'off':off,'src':src,'k':k,'a':aa,'symbolPath':sy}

def expected_schedule(ids):
    out=[]
    def add(ident,method,block,warmup):
        out.append(dict(sequence=len(out),workload='full',id=ident,method=method,block=block,warmup=warmup))
    for ident in ids:
        for method in 'ALT': add(ident,method,-1,True)
    for block in range(6):
        for j in range(3):
            ix=(j+block)%3
            for method in PERMS[(block+ix)%6]: add(ids[ix],method,block,False)
    return out

def generation_review(audit):
    index=load_json(audit.path(audit.package,'inputs/index.json'))
    audit.check(index.get('kind')=='fresh-airflow-off-boids-states' and index.get('shape')==['vehicle',17] and index.get('dtype')=='float64le','inputs.index-contract')
    entries=index['cases']
    require(len(entries)==3,'exactly three fresh input cases required')
    require([(x.get('id'),x.get('n'),x.get('seed')) for x in entries]==CASES, 'fresh case order/IDs/seeds/counts')
    require(len({x['id'] for x in entries})==3,'duplicate fresh case ID')
    summaries=audit.evidence.get('generation',[])
    audit.check([x.get('id') for x in summaries]==[x[0] for x in CASES],'generation.evidence-order')
    for entry in entries:
        audit.guard();ident,n,seed=entry['id'],entry['n'],entry['seed']
        state=read_array(audit,entry,'<f8',17*n,ident+'.input').reshape(n,17)
        require(entry.get('generationPath')=='generation/'+ident+'.json','generation path mismatch')
        gen=load_json(audit.path(audit.package,entry['generationPath']))
        audit.check(gen.get('id')==ident and gen.get('complete') is True,ident+'.generation-id-complete')
        summary=next(x for x in summaries if x['id']==ident)
        audit.pin(audit.package,summary['pin'],ident+'.generation-summary-pin')
        audit.check(summary.get('complete') is True and summary.get('generationMs')==gen.get('generationMs'),ident+'.generation-summary')
        compare_fields(audit,gen.get('config'),dict(seed=seed,count=n,mode='boids',dt=.0025,duration=2,
            search='grid',filter='wall-priority',airflow='off',observation='ideal'),ident+'.generator-config')
        audit.check(gen['config'].get('course')=='factory-v1',ident+'.wide-course')
        metrics=gen['metrics']
        audit.check(metrics.get('end')==2 and metrics.get('stopReason') is None and metrics.get('failure') is None,ident+'.generation-complete')
        initial=read_array(audit,gen['initial'],'<f8',17*n,ident+'.initial').reshape(n,17)
        final=read_array(audit,gen['final'],'<f8',17*n,ident+'.final').reshape(n,17)
        audit.check(state.tobytes()==final.tobytes(),ident+'.input-is-unaltered-final')
        audit.check(np.all(np.isfinite(initial)) and np.all(np.isfinite(final)),ident+'.finite-full-states')
        poses=read_array(audit,gen['poses'],'<f8',21*(1+7*n),ident+'.poses').reshape(21,1+7*n)
        audit.check(np.all(np.isfinite(poses)),ident+'.finite-poses')
        require(gen['poses'].get('frames')==21 and gen['poses'].get('width')==1+7*n,'pose metadata shape')
        frames=gen['frames'];require(len(frames)==21,'frame pin count')
        for frame_index,pin in enumerate(frames):
            frame=read_array(audit,pin,'<f8',1+7*n,ident+'.frame.'+str(frame_index))
            audit.check(pin.get('t')==poses[frame_index,0] and frame.tobytes()==poses[frame_index].tobytes(),ident+'.frame-concatenation.'+str(frame_index))
        audit.numeric(poses[:,0],np.arange(21)/10,ident+'.pose-times',1e-12,0.)
        for ix,source in [(0,initial),(-1,final)]:
            wanted=np.concatenate((source[:,:3],source[:,6:10]),axis=1)
            audit.check(poses[ix,1:].tobytes()==wanted.tobytes(),ident+'.pose-endpoint.'+str(ix))
        audit.check(gen.get('recording',{}).get('cadence')==.1,ident+'.recording-cadence')
        duration=gen.get('generationMs',gen.get('timing',{}).get('total'))
        audit.check(finite(duration) and duration>=0,ident+'.generation-time-separate')
        audit.numeric([s['t'] for s in gen['samples']],np.arange(21)/10,ident+'.sample-times',1e-12,0.)
        audit.generation.append({'id':ident,'n':n,'seed':seed,'state':state,'entry':entry})
    return entries

def literal_review(audit,rec,n,name):
    symbols=np.asarray(rec['symbols'],dtype=np.int64)
    require(symbols.shape==(4*n*n,),'literal symbols shape')
    audit.check(np.all((symbols>=1)&(symbols<=11)),name+'.terminal-symbols')
    audit.check(np.bincount(symbols,minlength=12).tolist()==rec['symbolCounts'],name+'.symbol-census')
    off=np.asarray(rec['offsets'],dtype=np.int64);src=np.asarray(rec['sources'],dtype=np.int64);k=np.asarray(rec['K'],dtype=float)
    validate_csr(audit,off,src,k,n,name)
    check_work(audit,rec['geometryWork'],n,len(src),name+'.work')
    check_certificate(audit,rec['certificate'],rec['geometryWork'],'all',name+'.certificate')
    audit.check(rec['symbolCounts'][8]==len(src),name+'.positive-symbol-count')
    for row in range(4*n):
        i,r=divmod(row,4);wanted=np.flatnonzero(symbols.reshape(n,n,4)[i,:,r]==8)
        audit.check(np.array_equal(src[off[row]:off[row+1]],wanted),name+'.symbol-support.'+str(row))
    return len(src)

def controls_review(audit):
    planned=expected_controls()+[(f'planes-{n}',None,None) for n in (62,64,66)]
    listed=audit.evidence.get('controls',[])
    audit.check([r.get('id') for r in listed]==[r[0] for r in planned],'controls.fixed24-order')
    for ident,tokens,_ in planned:
        audit.guard()
        rec=load_json(audit.path(audit.package,'results/control-'+ident+'.json'))
        summary=next((x for x in listed if x.get('id')==ident),None)
        require(isinstance(summary,dict),'control summary missing')
        audit.pin(audit.package,summary['pin'],'control.'+ident+'.summary-pin')
        audit.check(summary.get('pass') is True,'control.'+ident+'.summary-pass')
        n=rec['n'];audit.check(rec.get('id')==ident,'control.'+ident+'.id')
        if tokens is not None: audit.check(rec.get('positionTokens')==tokens,'control.'+ident+'.positions')
        else:
            n_expected=int(ident.rsplit('-',1)[-1]);audit.check(n==n_expected,'control.'+ident+'.size')
            expected=[['0','0','0']]*(n//2)+[['0','0','0.6']]*(n//2)
            audit.check(rec.get('positionTokens')==expected,'control.'+ident+'.positions')
        require(n==(len(tokens) if tokens is not None else n),'control size mismatch')
        audit.check(isinstance(rec.get('stateTokens'),list) and len(rec['stateTokens'])==n and all(isinstance(row,list) and len(row)==17 and all(isinstance(v,str) for v in row) for row in rec['stateTokens']),'control.'+ident+'.full-state-token-shape')
        for i,row in enumerate(rec['stateTokens']):
            audit.check(row[:3]==rec['positionTokens'][i],'control.'+ident+'.state-position.'+str(i))
            audit.check([float(x) for x in row[3:13]]==[0,0,0,0,0,0,1,0,0,0],'control.'+ident+'.fixed-nonposition.'+str(i))
            audit.check(np.asarray([float(x) for x in row[13:17]],dtype='<f8').tobytes()==np.full(4,.027*9.81/4,dtype='<f8').tobytes(),'control.'+ident+'.hover-nominal.'+str(i))
        for method in 'ALT':
            item=rec[method];m=literal_review(audit,item,n,'control.'+ident+'.'+method)
            if tokens is None: audit.check(m==4*(n//2)**2,'control.'+ident+'.'+method+'.chunk-count')
            assembly_review(audit,item.get('assemblyStats'),n,m,method,'control.'+ident+'.'+method+'.assembly',item['input']['nominalPositive'] and item['input']['nominalTotalFinite'],offsets=item['offsets'],sources=item['sources'],graph=item['graph'])
            if method!='A':
                for key in ('symbols','symbolCounts','offsets','sources','K','a','input','admission','graph','geometryWork','ordinaryLmax'):
                    audit.exact(item[key],rec['A'][key],'control.'+ident+'.'+method+'.exact-'+key)
        if ident in ('far-invalid258','nonfinite-nan','nonfinite-infinity','overflow-span'):
            audit.check(rec['A']['symbolCounts'][11]>0 and not rec['A']['admission']['admitted'],'control.'+ident+'.invalid-retained')
        if ident=='near-field': audit.check(rec['A']['symbolCounts'][4]>0 and not rec['A']['admission']['admitted'],'control.near-field.rejected')
        audit.check('solutions' not in rec,'control.'+ident+'.no-unallocated-solve')
        audit.check(rec.get('pass') is True,'control.'+ident+'.candidate-pass')
        audit.controls.append({'id':ident,'n':n,'complete':True})

def ownership_review(audit):
    own=load_json(audit.path(audit.package,'results/ownership.json'))
    audit.pin(audit.package,audit.evidence['ownership'],'ownership.evidence-pin')
    audit.check(own.get('sequence')==['L:sparse2','T:sparse2','L:planes62','T:planes62'],'ownership.extra4-build-sequence')
    for method in 'LT':
        kept=own['retained'][method]
        for phase in ('before','after'):
            record=kept[phase]
            literal_review(audit,record,66,'ownership.'+method+'.'+phase)
            assembly_review(audit,record.get('assemblyStats'),66,len(record['sources']),method,'ownership.'+method+'.'+phase+'.assembly',offsets=record['offsets'],sources=record['sources'],graph=record['graph'])
        for key in ('offsets','sources','K','a','symbols','symbolCounts','input','admission','graph','geometryWork','ordinaryLmax','certificate','assemblyStats'):
            audit.exact(kept['before'][key],kept['after'][key],'ownership.'+method+'.unchanged-'+key)
        ctl=load_json(audit.path(audit.package,'results/control-planes-66.json'))
        for key in ('offsets','sources','K','a','symbols','symbolCounts','admission','graph'):
            audit.exact(kept['before'][key],ctl[method][key],'ownership.'+method+'.original-'+key)
    extras=own['extraBuilds']
    require(len(extras)==4,'ownership exact four extra builds')
    for index,extra in enumerate(extras):
        spec=own['sequence'][index];method,ident=spec.split(':')
        audit.check(extra.get('label')==method and extra.get('id')==ident,'ownership.extra.'+str(index)+'.identity')
        n=2 if ident=='sparse2' else 62
        audit.check(extra.get('n')==n,'ownership.extra.'+str(index)+'.size')
        literal_review(audit,extra['bundle'],n,'ownership.extra.'+str(index))
        assembly_review(audit,extra['bundle'].get('assemblyStats'),n,len(extra['bundle']['sources']),method,'ownership.extra.'+str(index)+'.assembly',offsets=extra['bundle']['offsets'],sources=extra['bundle']['sources'],graph=extra['bundle']['graph'])
        positions=[['0','0','0'],['4','0','0']] if n==2 else [['0','0','0']]*31+[['0','0','0.6']]*31
        audit.check(extra.get('positionTokens')==positions,'ownership.extra.'+str(index)+'.positions')
        states=extra.get('stateTokens');require(isinstance(states,list) and len(states)==n,'ownership full states')
        for i,row in enumerate(states):
            require(len(row)==17 and all(isinstance(x,str) for x in row),'ownership full state tokens')
            audit.check(row[:3]==positions[i] and [float(x) for x in row[3:13]]==[0,0,0,0,0,0,1,0,0,0] and [float(x) for x in row[13:17]]==[.027*9.81/4]*4,'ownership.extra.'+str(index)+'.state.'+str(i))
        if n==2:
            b=extra['bundle']
            audit.check(b['symbols']==[1]*16 and b['offsets']==[0]*9 and b['sources']==[] and b['K']==[] and b['a']==[] and b['admission']['admitted'] is True and b['geometryWork']['pairCalls']==0,'ownership.sparse2.'+method+'.expected')
        else:
            base=load_json(audit.path(audit.package,'results/control-planes-62.json'))[method]
            audit.exact(extra['bundle'],base,'ownership.planes62.'+method+'.original')
    audit.check(own.get('pass') is True,'ownership.candidate-pass')
    audit.check(own.get('inputUnchanged') is True,'ownership.inputs-unmodified')
    audit.check(own.get('returnedStorageDisjoint') is True,'ownership.returned-storage-disjoint-reported')

def assembly_review(audit,stats,n,m,method,name,nominal=True,*,offsets,sources,graph):
    if method=='A': return
    require(isinstance(stats,dict),'assembly stats absent')
    off=np.asarray(offsets,dtype=np.int64)
    src=np.asarray(sources,dtype=np.int64)
    require(off.shape==(4*n+1,) and src.shape==(m,) and off[0]==0 and off[-1]==m and np.all(np.diff(off)>=0),'assembly CSR shape/partition')
    counts=np.diff(off)
    require(np.all(counts<=n-1),'assembly row exceeds distinct nonself sources')
    incoming=[]
    for i in range(n):
        audit.guard()
        incoming.append(int(np.unique(src[off[4*i]:off[4*i+4]]).size))
    dependency_entries=sum(incoming)
    compare_fields(audit,graph,dict(uniqueVehicleEdges=dependency_entries,incomingDegree=incoming,
                                  maxIncomingDegree=max(incoming)),name+'.graph-from-CSR')
    typed=method=='T'
    chunks=(m+4095)//4096 if typed else 0
    # Each nonempty canonical row intersects this many consecutive chunk ranges.
    # Half-open ends use end-1: a row ending exactly at4096 adds no empty segment.
    nonempty=counts>0
    row_segments=int(np.sum((off[1:][nonempty]-1)//4096-off[:-1][nonempty]//4096+1)) if typed else 0
    expected=dict(schema='m31-receiver-row-assembly-v1',mode={'L':'lean','T':'typed'}[method],
        inputN=n,positiveEntries=m,dependencyEntries=dependency_entries,
        rowCapacityEntries=n if typed else None,rowLengthsAtLastReceiver=counts[-4:].tolist(),
        maxRowLengthEntries=int(np.max(counts,initial=0)),rowGrowthCount=0 if typed else None,
        rowScratchTypedArrayAllocations=8 if typed else 0,rowScratchIdBytes=16*n if typed else 0,
        rowScratchKBytes=32*n if typed else 0,rowScratchBytes=48*n if typed else 0,
        rotorPointScratchBytes=12*8,rotorPointTypedArrayAllocations=1,chunkPolicyCapacityEntries=4096,
        chunkCount=chunks,chunkGrowthCount=max(0,chunks-1),chunkTypedArrayAllocations=2*chunks,
        chunkCapacityEntries=4096*chunks,chunkUsedEntries=m if typed else 0,
        chunkSpareEntries=4096*chunks-m if typed else 0,chunkAllocatedPayloadBytes=12*4096*chunks,
        rowToChunkCopySegments=row_segments,chunkToFinalCopySegments=chunks,
        rowToChunkCopiedEntries=m if typed else 0,chunkToFinalCopiedEntries=m if typed else 0,
        rowToChunkCopiedBytes=12*m if typed else 0,chunkToFinalCopiedBytes=12*m if typed else 0,
        ordinaryPositiveTupleCount=0 if typed else m,ordinarySetAddCalls=0 if typed else m,
        ordinaryDependencySetCount=0 if typed else n,ordinaryGlobalSourceEntries=0 if typed else m,
        ordinaryGlobalKEntries=0 if typed else m,ordinaryRowToGlobalCopiedEntries=0 if typed else m,
        ordinaryGlobalToFinalCopiedEntries=0 if typed else m,
        dependencyOutputRepresentation='independent ordinary arrays; ascending unique IDs',dependencyOutputArrays=n,
        finalSourceBytes=4*m,finalKBytes=8*m,offsetBytes=4*(4*n+1),scalingBytes=8*m if nominal else 0,
        outputTypedArraysOwnBuffers=True,scratchViewsReturned=False,jsHeapBytesMeasured=False,
        garbageCollectionMeasured=False,commonPreparedGeometryBytes=28*n*8,commonSymbolBytes=4*n*n)
    # Expected payload totals are formed from independently derived counts, never
    # from the candidate's reported components.
    overlap=expected['rowScratchBytes']+expected['rotorPointScratchBytes']+expected['offsetBytes']+expected['chunkAllocatedPayloadBytes']+expected['finalSourceBytes']+expected['finalKBytes']
    expected['finalizationOverlapKnownPayloadBytes']=overlap
    expected['allocatedAssemblyTypedPayloadBytes']=overlap+expected['scalingBytes']
    compare_fields(audit,stats,expected,name)


def independent_case(audit,item):
    ident,n,states=item['id'],item['n'],item['state']
    start_errors=len(audit.errors)
    bs={}
    for method in 'ALT':
        doc=load_json(audit.path(audit.package,'results/'+ident+'-'+method+'.json'))
        audit.check(doc.get('id')==ident and doc.get('label')==method and doc.get('n')==n,ident+'.'+method+'.identity')
        bs[method]=bundle(audit,doc,ident+'.'+method)
        assembly_review(audit,doc.get('assemblyStats'),n,bs[method]['m'],method,ident+'.'+method+'.assembly',offsets=bs[method]['off'],sources=bs[method]['src'],graph=doc['graph'])
        audit.qualified[(ident,method)]=bs[method]
    ref=bs['A'];d=ref['doc'];c=constants();g=prepare_geometry(states,c)
    census=input_census(states,g,c);compare_fields(audit,d['input'],census,ident+'.independent-input')
    for method in 'LT':
        other=bs[method]
        for key in ('off','src','k','a'):
            audit.check(other[key].dtype==ref[key].dtype and other[key].tobytes()==ref[key].tobytes(),ident+'.'+method+'.exact-'+key)
        for key in ('input','admission','graph','certificate','symbolCounts','geometryWork','ordinaryLmax','solutions','matrixHash'):
            audit.exact(other['doc'][key],d[key],ident+'.'+method+'.exact-'+key)
        audit.exact(other['doc'].get('solutionHash',other['doc'].get('solutionHashes')),d.get('solutionHash',d.get('solutionHashes')),ident+'.'+method+'.solution-hash')
    streams={method:gzip.open(bs[method]['symbolPath'],'rb') for method in 'ALT'}
    hashes={method:hashlib.sha256() for method in 'ALT'}
    counts=np.zeros(12,dtype=np.int64);ids_list=[];k_list=[];offs=[0];deps=[]
    mismatch=0;support_bad=0;k_bad=0;first=[];max_error=0.
    work=dict(logicalDirectedPairs=n*(n-1),gatheredNonselfCandidates=n*(n-1),directedCenterTests=n*(n-1),
              certifiedSkippedPairs=0,centerEligiblePairs=0,centerGuardRejectedPairs=0,pairCalls=0,positiveRotorTerms=0)
    try:
        for i in range(n):
            audit.guard();sy,rows,rwork=classify_receiver(i,g,c)
            blocks={method:streams[method].read(4*n) for method in 'ALT'}
            require(all(len(b)==4*n for b in blocks.values()),'truncated symbols')
            for method in 'ALT': hashes[method].update(blocks[method])
            require(blocks['A']==blocks['L']==blocks['T'],'exact ALT symbol mismatch')
            got=np.frombuffer(blocks['A'],dtype=np.uint8).reshape(n,4)
            bad=got!=sy;mismatch+=int(np.count_nonzero(bad))
            if np.any(bad) and len(first)<8:
                for j,r in np.argwhere(bad)[:8-len(first)]: first.append([i,int(j),int(r),int(got[j,r]),int(sy[j,r])])
            counts+=np.bincount(sy.ravel(),minlength=12)
            work['centerEligiblePairs']+=rwork['eligibleCenterPairs'];work['centerGuardRejectedPairs']+=rwork['invalidCenterPairs'];work['pairCalls']+=rwork['pairTermCalls']
            deps.append(np.unique(np.concatenate([ids for ids,ks in rows])))
            for r,(ids,ks) in enumerate(rows):
                row=4*i+r;a,b=int(ref['off'][row]),int(ref['off'][row+1])
                if not np.array_equal(ref['src'][a:b],ids): support_bad+=1
                else:
                    err=np.abs(ref['k'][a:b]-ks);max_error=max(max_error,float(np.max(err,initial=0.)))
                    k_bad+=int(np.any(err>2e-12+2e-12*np.abs(ks)))
                ids_list.append(ids);k_list.append(ks);offs.append(offs[-1]+len(ids))
                require(offs[-1]<=MAX_TERMS,'independent positive guard')
        for method in 'ALT':
            audit.check(streams[method].read(1)==b'',ident+'.'+method+'.symbols-no-trailing')
            audit.check(hashes[method].hexdigest()==bs[method]['doc']['artifacts']['symbols']['rawSha256'],ident+'.'+method+'.raw-symbol-hash')
    finally:
        for stream in streams.values(): stream.close()
    audit.check(mismatch==0,ident+'.independent-all-symbols',{'mismatches':mismatch,'first':first})
    audit.check(support_bad==0,ident+'.independent-all-source-rows',{'badRows':support_bad})
    audit.check(k_bad==0,ident+'.independent-all-K',{'badRows':k_bad,'maxAbs':max_error})
    audit.check(counts.sum()==4*n*n and counts[0]==0,ident+'.terminal-census')
    audit.exact(d['symbolCounts'],counts.tolist(),ident+'.independent-census')
    off=np.asarray(offs,dtype=np.int64);src=np.concatenate(ids_list).astype(np.int64);k=np.concatenate(k_list)
    work['positiveRotorTerms']=len(k);compare_fields(audit,d['geometryWork'],work,ident+'.independent-work')
    graph=graph_census(g['q'],deps);compare_fields(audit,d['graph'],graph,ident+'.independent-graph')
    scaled=k*np.sqrt(g['S0'][src]/c['mg']);rowids=np.repeat(np.arange(4*n),np.diff(off))
    aa=scaled/np.sqrt(g['f0'].ravel()[rowids]/(2*c['rho']*c['area']))
    audit.numeric(ref['a'],aa,ident+'.independent-a')
    capmax=float(np.max(scaled,initial=0.));violations=int(np.count_nonzero(~np.isfinite(scaled)|(scaled>128)))
    reasons=[]
    if not census['geometryValid']: reasons.append('geometry')
    if not census['nominalPositive'] or not census['nominalTotalFinite']: reasons.append('nominal')
    if counts[4]: reasons.append('near-field')
    if counts[11]: reasons.append('invalid-term')
    if violations: reasons.append('scaled-cap')
    admission=dict(admitted=not reasons,reasons=reasons,unsupportedNearCount=int(counts[4]),invalidTermCount=int(counts[11]),scaledCapMax=capmax,scaledCapViolationCount=violations)
    compare_fields(audit,d['admission'],admission,ident+'.independent-admission')
    lmax=float(np.max(np.bincount(rowids,weights=aa,minlength=4*n))/(4*math.sqrt(2)))
    audit.close(d['ordinaryLmax'],lmax,ident+'.independent-ordinary-bound')
    require(admission['admitted'] and graph['descendingEligible'],'target is outside solve domain')
    require(len(audit.errors)==start_errors,'geometry/equivalence gate failed before independent solve')
    expected=direct_solve(graph['order'],g['f0'],g['S0'],off,src,aa,audit.guard)
    sol=d['solutions']['O'];compare_map(audit,sol,expected,n,ident+'.independent-ordered')
    y=np.asarray(sol['y'],dtype=float);res=csr_map(y,g['f0'],g['S0'],off,src,aa)
    compare_map(audit,sol['residualMap'],res,n,ident+'.independent-residual-map')
    for key,values in [('work',expected),('residualWork',res)]:
        wanted=dict(rootClosures=4*n,bisectionIterations=56*int(np.count_nonzero(values['alpha']>0)),positiveTermMultiplications=len(k))
        compare_fields(audit,sol[key],wanted,ident+'.'+key)
    residual=float(np.max(np.abs(np.log(y)-np.log(res['y']))))
    total=((res['T'][:,0]+res['T'][:,1])+res['T'][:,2])+res['T'][:,3]
    discrepancy=float(np.max(np.abs(g['S0']*y*y-total)/g['S0']))
    audit.close(sol['residualLog'],residual,ident+'.residual-log')
    audit.close(sol['sourceReceiverMismatch'],discrepancy,ident+'.force-consistency')
    audit.check(residual<=1e-9 and discrepancy<=2e-9,ident+'.residual-gates')
    for method in 'ALT':
        b=bs[method];s=b['doc']['solutions']['O'];vals,*_=rotor_values(s,n)
        require(np.all(np.isfinite(vals)),'nonfinite qualified solution')
        b['checksum']=saved_checksum(s,b['k']);b['valuesLength']=len(vals)
    audit.frames.append({'id':ident,'n':n,'complete':True,'symbolEntries':4*n*n,'coefficientMaxAbs':max_error,'independentResidualLog':residual,'pass':len(audit.errors)==start_errors})

def timing_review(audit,ids):
    schedule=expected_schedule(ids);listed=audit.evidence.get('timings',[])
    audit.check(len(listed)==63,'timing.63-records')
    rawfiles=list((audit.package/'results').glob('call-*-raw.json'))
    audit.check(len(rawfiles)==63,'timing.63-raw-records')
    for planned in schedule:
        audit.guard();seq=planned['sequence'];name='call.'+str(seq)
        raw=load_json(audit.path(audit.package,f'results/call-{seq:03d}-raw.json'))
        rec=load_json(audit.path(audit.package,f'results/call-{seq:03d}.json'))
        audit.pin(audit.package,rec['raw'],name+'.raw')
        audit.exact({k:v for k,v in rec.items() if k not in ('raw','validation')},raw,name+'.immutable-raw')
        audit.exact(rec,listed[seq],name+'.evidence-copy')
        for k,v in planned.items(): audit.check(rec.get(k)==v,name+'.'+k)
        phases=rec['phasesMs'];require(set(phases)==set(FULL_PHASES),'phase fields mismatch')
        audit.check(finite(rec.get('totalMs')) and rec['totalMs']>0,name+'.positive-duration')
        audit.check(all(finite(v) and v>=(-1e-7 if k=='remainder' else 0) for k,v in phases.items()),name+'.phases-finite')
        audit.close(sum(phases.values()),rec['totalMs'],name+'.phase-total',1e-7,1e-12)
        b=audit.qualified[(planned['id'],planned['method'])];d=b['doc'];s=d['solutions']['O']
        for k in ('geometryWork','certificate'): audit.exact(rec[k],d[k],name+'.'+k)
        if planned['method']!='A':
            comparable=lambda v:{k:x for k,x in v.items() if k!='commonSymbolBytes'}
            audit.exact(comparable(rec['assemblyStats']),comparable(d['assemblyStats']),name+'.assembly')
            audit.check(rec['assemblyStats'].get('commonSymbolBytes')==0,name+'.compact-no-symbol-tensor')
        for k in ('work','residualWork','residualLog','sourceReceiverMismatch'): audit.exact(rec[k],s[k],name+'.'+k)
        audit.check(rec.get('iterations')==1 and rec.get('converged') is True and rec.get('lastChange') is None,name+'.ordered-termination')
        audit.close(rec['checksum'],b['checksum'],name+'.checksum',1e-8,1e-14)
        v=rec['validation']
        for k in ('symbols','offsets','sources','input','admission','graph','certificate','symbolCounts','geometryWork','ordinaryLmax','inputUnchanged','checksum','hashesMatch','pass'): audit.check(v.get(k) is True,name+'.validation-'+k)
        audit.check(v.get('matrixHash')==d['matrixHash'],name+'.matrix-hash')
        sh=d.get('solutionHash',d.get('solutionHashes',{}).get('O'))
        audit.check(v.get('solutionHash')==sh,name+'.solution-hash')
        for k,length in [('K',b['m']),('a',b['m'])]:
            compare_fields(audit,v[k],dict(length=length,maxAbs=0.,maxRel=0.,bad=0,firstMismatch=None,**{'pass':True}),name+'.'+k)
        sv=v['solution']
        for k in ('work','termination','residual','exactResidual','pass'): audit.check(sv.get(k) is True,name+'.solution-'+k)
        compare_fields(audit,sv['values'],dict(length=b['valuesLength'],maxAbs=0.,maxRel=0.,bad=0,firstMismatch=None,**{'pass':True}),name+'.solution-values')
        audit.calls.append(rec)

def analysis(audit,ids):
    out={'scope':'six paired within-process repeats per fresh fixed pose; no population/physical/browser inference','cases':[],'practicalRulePass':None}
    if len(audit.calls)!=63 or audit.errors: return out
    case_pass=[]
    for ident in ids:
        rows=[r for r in audit.calls if r['id']==ident and not r['warmup']]
        grouped={(r['block'],r['method']):r for r in rows}
        item={'id':ident,'methods':{},'pairs':{}}
        for method in 'ALT':
            selected=[grouped[b,method] for b in range(6)]
            item['methods'][method]={k:{'median':statistics.median(v),'min':min(v),'max':max(v)} for k,v in
                [('totalMs',[x['totalMs'] for x in selected])]+[(p,[x['phasesMs'][p] for x in selected]) for p in FULL_PHASES]}
        for left,right in [('T','L'),('L','A'),('T','A')]:
            ratios=[grouped[b,left]['totalMs']/grouped[b,right]['totalMs'] for b in range(6)]
            delta=[grouped[b,left]['totalMs']-grouped[b,right]['totalMs'] for b in range(6)]
            phases={p:sum(grouped[b,left]['phasesMs'][p]-grouped[b,right]['phasesMs'][p] for b in range(6)) for p in FULL_PHASES}
            item['pairs'][left+'/'+right]={'ratios':ratios,'differencesMs':delta,'medianPairedRatio':statistics.median(ratios),'strictWins':sum(x<1 for x in ratios),'matchedPhaseDifferenceSumsMs':phases}
        if ident.startswith('n5000-'):
            tl,ta=item['pairs']['T/L'],item['pairs']['T/A'];ok=tl['medianPairedRatio']<=.90 and tl['strictWins']>=5 and ta['medianPairedRatio']<=1
            item['practicalRulePass']=ok;case_pass.append(ok)
        out['cases'].append(item)
    out['practicalRulePass']=len(case_pass)==2 and all(case_pass)
    return out

def provenance_resources(audit):
    cfg=load_json(audit.path(audit.package,'config.json'))
    audit.check([(x['id'],x['n'],x['seed']) for x in cfg['cases']]==CASES,'config.fixed-cases')
    compare_fields(audit,cfg,dict(schema='m31-typed-assembly-v1',methods=['A','L','T'],permutations=PERMS,blocks=6,
        controls=24,ownershipExtraBuilds=4,qualificationBuilds=9,qualificationSolves=9,warmupCalls=9,
        measuredCalls=54,totalCalls=63,chunkEntries=4096),'config')
    compare_fields(audit,cfg['limits'],dict(candidateWallSeconds=900,candidateCooperativeSeconds=895,
        reviewWallSeconds=180,reviewCooperativeSeconds=175,rssBytes=RSS_CAP,positiveTerms=MAX_TERMS,
        normalScientificBytes=184*(1<<20),scientificBytes=192*(1<<20),scientificDirectoryBytes=208*(1<<20)), 'config.limits')
    compare_fields(audit,cfg['generation'],dict(duration=2,dt=.0025,mode='boids',search='grid',filter='wall-priority',record=True,frameEvery=.1,factoryVariant='wide',expectedCourse='factory-v1',airflow='off',observation='ideal'),'config.generation')
    compare_fields(audit,cfg['primary'],dict(ratio='T/L',maximumMedianPairedRatio=.9,minimumStrictWins=5,
        anchorRatio='T/A',maximumAnchorMedianPairedRatio=1,requiredCases=[x[0] for x in CASES if x[1]==5000]),'config.practical')
    mf=audit.path(audit.package,'source-manifest.json');manifest=load_json(mf)
    pins=manifest.get('files');require(isinstance(pins,list) and pins,'source pins missing')
    seen=set()
    for ix,pin in enumerate(pins):
        audit.check(pin.get('path') not in seen,'manifest.unique.'+str(ix));seen.add(pin.get('path'))
        audit.pin(audit.root,pin,'manifest.'+str(ix))
    run=load_json(audit.path(audit.package,'results/candidate-run.json'))
    audit.check(run.get('kind')=='candidate' and run.get('returncode')==0 and run.get('supervisor_success') is True and not run.get('terminated_for') and not run.get('exception_class'),'candidate.supervisor-success')
    audit.check(run.get('monitorErrors')==[] and run.get('rssSampleErrors')==0,'candidate.monitoring-no-errors')
    audit.check(type(run.get('finalScientificDirectoryBytes')) is int and 0<=run['finalScientificDirectoryBytes']<=208*(1<<20),'candidate.post-wait-directory-cap')
    audit.check(type(run.get('finalSupervisorLogBytes')) is int and 0<=run['finalSupervisorLogBytes']<=4*(1<<20),'candidate.post-wait-log-cap')
    audit.check(run.get('wall_cap_seconds')==900 and finite(run.get('supervisor_elapsed_seconds')) and 0<=run['supervisor_elapsed_seconds']<=900,'candidate.external-wall-cap')
    audit.check(run.get('rss_cap_bytes')==RSS_CAP and finite(run.get('externalSampledPeakRSSKiB')) and run['externalSampledPeakRSSKiB']*1024<=RSS_CAP,'candidate.external-RSS')
    audit.check(type(run.get('rssSamples')) is int and run['rssSamples']>0 and type(run.get('rssSampleErrors')) is int and run['rssSampleErrors']>=0,'candidate.RSS-monitoring')
    audit.check(run.get('source_manifest_sha256')==audit.digest(mf),'candidate.source-manifest')
    audit.check(isinstance(run.get('source_commit'),str) and re.fullmatch('[0-9a-f]{40}',run['source_commit']) is not None,'candidate.source-commit')
    for ix,pin in enumerate(run.get('artifacts',[])): audit.pin(audit.package,pin,'candidate.log.'+str(ix))
    lock=audit.path(audit.package,'results/candidate-invocation.lock')
    audit.check(lock.stat().st_size>0,'candidate.allocation-consumed')
    memory=audit.evidence.get('memory',{})
    audit.check(finite(memory.get('sampledPeakRSSBytes')) and 0<memory['sampledPeakRSSBytes']<=RSS_CAP,'candidate.internal-RSS')
    audit.check(isinstance(memory.get('processResourceUsage'),dict) and isinstance(memory.get('platformMaxRSSUnits'),str),'candidate.memory-units')
    admin={'candidate-invocation.lock','candidate-stdout.txt','candidate-stderr.txt','candidate-run.json',
           'review-invocation.lock','review-stdout.txt','review-stderr.txt','review-run.json','independent-review.json','analysis.json'}
    total=scientific=normal=0
    for directory in ('inputs','generation','results'):
        for p in (audit.package/directory).rglob('*'):
            if not p.is_file(): continue
            require(p.resolve().is_relative_to(audit.package),'scientific file escapes')
            size=p.stat().st_size;total+=size
            rel=p.relative_to(audit.package/directory)
            if directory=='results' and len(rel.parts)==1 and rel.name in admin: continue
            scientific+=size
            if not (directory=='results' and rel.name in ('failure.json','partial-evidence.json')): normal+=size
    audit.check(total<=208*(1<<20),'directory.208MiB-cap')
    audit.check(scientific<=192*(1<<20) and normal<=184*(1<<20),'scientific.192MiB-and184MiB-caps')
    if audit.evidence.get('complete') is True:
        evidence_size=(audit.package/'results/evidence.json').stat().st_size
        audit.check(audit.evidence.get('newScientificBytesBeforeEvidence')==scientific-evidence_size,'candidate.before-evidence-byte-accounting')
    audit.resources={'candidateExternalElapsedSeconds':run.get('supervisor_elapsed_seconds'),
        'externalSampledPeakRSSKiB':run.get('externalSampledPeakRSSKiB'),'rssSamples':run.get('rssSamples'),
        'directoryBytesAtReview':total,'scientificBytes':scientific,'normalScientificBytes':normal,
        'reviewAllocationSeconds':180,'reviewCooperativeSeconds':175}
    for stage in ('environmentStart','environmentEnd'):
        env=audit.evidence.get(stage,{})
        for key in ('cpuModel','architecture','platform','kernel','node','v8','clock','threads'):
            audit.check(key in env and (env[key] is None or isinstance(env[key],str)),stage+'.'+key)
        audit.check(valid_sha(env.get('nodeExecutableSha256')),stage+'.node-sha')
        audit.check(env.get('nodeOptionsEmpty') is True and env.get('executionFlagCount')==0 and env.get('executionFlags')==[],stage+'.default-runtime-flags')
        audit.check(type(env.get('logicalCores')) is int and env['logicalCores']>0 and finite(env.get('installedRAMBytes')) and env['installedRAMBytes']>0,stage+'.hardware')
        audit.check(all(k in env for k in ('physicalCores','powerSource','lowPowerMode','loadAverage')),stage+'.environment-observations')
    a,b=audit.evidence.get('environmentStart',{}),audit.evidence.get('environmentEnd',{})
    for k in ('nodeExecutableSha256','node','v8','architecture','platform','kernel','clock'):
        audit.check(k in a and a.get(k)==b.get(k),'environment.stable-'+k)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();package=args.package.resolve();out=args.output.resolve()
    require(package.is_dir() and out.parent.is_dir(),'package/output directory absent')
    require(not out.exists(),'review output must be new')
    audit=Audit(package);result_analysis=None
    try:
        evidence_path=package/'results/evidence.json'
        if not evidence_path.is_file(): evidence_path=package/'results/partial-evidence.json'
        audit.evidence=load_json(evidence_path)
        audit.check(audit.evidence.get('complete') is True,'candidate.complete')
        provenance_resources(audit)
        controls_review(audit)
        ownership_review(audit)
        entries=generation_review(audit)
        require(len(audit.errors)==0,'pre-qualification saved evidence failed')
        for item in audit.generation: independent_case(audit,item)
        audit.check(len(audit.frames)==3 and all(f['complete'] and f['pass'] for f in audit.frames),'qualification.all-three-independent-cases')
        qualification=audit.evidence.get('qualification',[])
        audit.check(len(qualification)==9,'qualification.nine-saved-builds')
        for ident,_,_ in CASES:
            for method in 'ALT':
                selected=[x for x in qualification if x.get('id')==ident and x.get('label')==method]
                audit.check(len(selected)==1,'qualification.unique.'+ident+'.'+method)
                if selected:
                    b=audit.qualified[(ident,method)]['doc']
                    rec=selected[0]
                    audit.check(rec.get('matrixHash')==b['matrixHash'] and rec.get('solutionHash')==b['solutionHash'],'qualification.listed-hashes.'+ident+'.'+method)
                    audit.pin(audit.package,rec['persistence']['meta'],'qualification.saved-bundle.'+ident+'.'+method)
                    audit.check(finite(rec.get('qualificationComputeMs')) and rec['qualificationComputeMs']>=0 and finite(rec['persistence'].get('totalPersistenceMs')) and rec['persistence']['totalPersistenceMs']>=0 and rec['persistence'].get('fsync') is False,'qualification.untimed-diagnostics.'+ident+'.'+method)
                    audit.check(rec['comparison'].get('inputUnchanged') is True and rec['comparison'].get('pass') is True,'qualification.inputs-unchanged.'+ident+'.'+method)
                    audit.exact(rec,load_json(audit.path(audit.package,'results/qualification-'+ident+'-'+method+'.json')),'qualification.evidence-copy.'+ident+'.'+method)
        require(not audit.errors,'independent qualification failed before timing interpretation')
        timing_review(audit,[e['id'] for e in entries])
        result_analysis=analysis(audit,[e['id'] for e in entries])
    except Exception as error:
        audit.error('review-error',error)
    if result_analysis is None: result_analysis={'practicalRulePass':None,'cases':[],'reason':'incomplete-or-failed-audit'}
    analysis_path=package/'results/analysis.json'
    if not analysis_path.exists():
        with analysis_path.open('x',encoding='utf-8') as f: json.dump(safe_json(result_analysis),f,allow_nan=False,indent=2);f.write('\n')
    else: audit.check(False,'analysis-output-already-exists')
    report={'kind':'independent-fresh-typed-assembly-review','complete':audit.evidence.get('complete') is True,
        'pass':not audit.errors,'checkCount':len(audit.checks),'errors':audit.errors,'checks':audit.checks,
        'generation':[{'id':x['id'],'n':x['n'],'seed':x['seed']} for x in audit.generation],
        'controls':audit.controls,'qualification':audit.frames,'coverage':{'validatedTimingRecords':len(audit.calls)},
        'timing':result_analysis,'resources':audit.resources,
        'limitations':['Fresh geometry/root verification covers exactly three newly frozen states, not physical accuracy.',
            'Independent NumPy hypot/reduction may differ in rounding; exact symbols and inherited tolerances are not relaxed.',
            'Timed transient arrays are not all saved; repeat hashes/assertions do not reconstruct them independently.',
            'Ownership before/after artifacts and source review cannot prove all possible future aliasing behavior.',
            'Two short N5000 simulations and six within-process timings do not establish mature flock or browser performance.',
            '2M positive cap throw is source-reviewed, not exercised by a giant synthetic case.']}
    with out.open('x',encoding='utf-8') as f: json.dump(safe_json(report),f,allow_nan=False,indent=2);f.write('\n')
    print(json.dumps({'pass':not audit.errors,'checks':len(audit.checks),'errors':len(audit.errors),'practicalRulePass':result_analysis.get('practicalRulePass')}))
    return 0 if not audit.errors else 1

if __name__=='__main__':
    raise SystemExit(main())
