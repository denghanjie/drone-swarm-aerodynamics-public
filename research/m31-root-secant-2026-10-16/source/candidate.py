"""Causal saved-root secant diagnostic. No imports of a solver or integrator."""
import hashlib
import json
import math
import pathlib
import resource
import sys
import time


def require(ok, name):
    if not ok:
        raise ValueError(name)


def finite_tree(v):
    if isinstance(v, list):
        return all(finite_tree(x) for x in v)
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def matrix(v, rows, cols):
    return isinstance(v, list) and len(v) == rows and all(isinstance(x, list) and len(x) == cols for x in v) and finite_tree(v)


def safe(v):
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if isinstance(v, list):
        return [safe(x) for x in v]
    if isinstance(v, dict):
        return {k: safe(x) for k, x in v.items()}
    return v


def encoded(v):
    return json.dumps(safe(v), separators=(',', ':'), allow_nan=False)+'\n'


def predict(history, target_time):
    """Only one/two earlier fresh (index,time,roots) tuples are visible here."""
    last = history[-1]
    if len(history) == 1:
        return [row[:] for row in last[2]], None
    prev = history[-2]
    scale = (target_time-last[1])/(last[1]-prev[1])
    return [[b+scale*(b-a) for a, b in zip(ra, rb)] for ra, rb in zip(prev[2], last[2])], scale


def invalid_roots(roots):
    out = []
    for i, row in enumerate(roots):
        for r, x in enumerate(row):
            if not math.isfinite(x) or not 0 < x <= 1:
                reason = ('nan' if math.isnan(x) else 'positive-infinity' if x > 0 else 'negative-infinity') if not math.isfinite(x) else ('nonpositive' if x <= 0 else 'above-one')
                out.append(dict(drone=i, rotor=r, value=x if math.isfinite(x) else None, reason=reason))
    return out


def rotate_z(q, z):
    x, y, zq, w = q
    return [2*(x*zq+w*y)*z, 2*(y*zq-w*x)*z, (1-2*(x*x+y*y))*z]


def loads(states, roots, arm):
    forces, corrections = [], []
    corners = [(arm, arm), (-arm, arm), (-arm, -arm), (arm, -arm)]
    for s, row in zip(states, roots):
        f = [s[13+r]*row[r] for r in range(4)]
        d = [f[r]-s[13+r] for r in range(4)]
        forces.append(f)
        corrections.append(dict(delta=d, force=rotate_z(s[6:10], math.fsum(d)), torque=[math.fsum(c[1]*v for c, v in zip(corners, d)), -math.fsum(c[0]*v for c, v in zip(corners, d)), 0.]))
    return dict(forces=forces, corrections=corrections)


def near(a, b, cfg):
    if isinstance(a, dict):
        return isinstance(b, dict) and a.keys() == b.keys() and all(near(a[k], b[k], cfg) for k in a)
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(near(x, y, cfg) for x, y in zip(a, b))
    return math.isfinite(a) and math.isfinite(b) and abs(a-b) <= cfg['agreementAtol']+cfg['agreementRtol']*abs(b)


def errors(a, b, cfg):
    mg = cfg['mass']*cfg['gravity']
    radius = math.sqrt(2)*cfg['armCoordinate']
    rotor = [[abs(x-y)/(mg/4) for x, y in zip(ar, br)] for ar, br in zip(a['forces'], b['forces'])]
    force = [math.dist(x['force'], y['force'])/mg for x, y in zip(a['corrections'], b['corrections'])]
    moment = [math.dist(x['torque'], y['torque'])/(mg*radius) for x, y in zip(a['corrections'], b['corrections'])]
    values = dict(rotor=rotor, force=force, moment=moment)
    require(all(finite_tree(x) for x in values.values()), 'uncomputable-error')
    flat = [(rotor[i][r], i, r) for i in range(len(rotor)) for r in range(4)]
    v, i, r = max(flat, key=lambda x: x[0])
    argmax = dict(rotor=dict(drone=i, rotor=r))
    maxima = dict(rotor=v)
    for name in ('force', 'moment'):
        i = max(range(len(values[name])), key=lambda j: values[name][j])
        argmax[name] = dict(drone=i, rotor=None)
        maxima[name] = values[name][i]
    return dict(**values, maxima=maxima, argmax=argmax)


def admit_event(event, index, cfg):
    n = cfg['n']
    require(event['index'] == index and event['t'] == round(index*cfg['refreshDt'], 6), 'ordered-event')
    require(event['status'] == 'completed' and event['role'] == ('terminal-audit' if index == cfg['events']-1 else 'propagation-refresh'), 'event-role-status')
    require(event['oldCacheIndex'] == (index-1 if index else None), 'event-cache-predecessor')
    states, commands = event['states'], event['commands']
    require(matrix(states, n, 17) and matrix(commands, n, 4), 'current-state-command-shape')
    require(all(all(v > 0 for v in s[13:17]) and abs(math.hypot(*s[6:10])-1) <= 1e-12 for s in states), 'current-motor-quaternion-domain')
    mg = cfg['mass']*cfg['gravity']
    require(all(0 <= v <= 2.25*mg/4+1e-12 for row in commands for v in row), 'command-range')
    info = event['instantaneous']['info']
    require(info['evaluation'] == 'instantaneous' and info['admitted'] is True and info['descendingEligible'] is True, 'inherited-fresh-admission')
    require(0 <= info['residual'] <= cfg['residualLimit'] and 0 <= info['sourceReceiverMismatch'] <= cfg['sourceReceiverLimit'], 'inherited-residual')
    roots = [[v['x'] for v in row] for row in event['instantaneous']['witness']['rotors']]
    require(matrix(roots, n, 4) and not invalid_roots(roots), 'oracle-root-domain')
    require(event['cache'] == dict(index=index, t=event['t'], ratios=roots), 'direct-witness-cache-identity')
    fresh = loads(states, roots, cfg['armCoordinate'])
    require(near(fresh['forces'], event['instantaneous']['forces'], cfg) and near(fresh['corrections'], event['instantaneous']['corrections'], cfg), 'fresh-load-correspondence')
    return roots, fresh


def summarize(rows, cfg):
    out = dict(targets=len(rows), scoredEvents=sum(r['scoreStatus'] == 'scored' for r in rows), invalidEvents=sum(not r['validRoots'] for r in rows), invalidRoots=sum(len(r['invalidRoots']) for r in rows))
    out['modes'] = {}
    for mode in ('predict', 'hold'):
        maxima, where = {}, {}
        for name in cfg['thresholds']:
            scored = [r for r in rows if r['errors'][mode] is not None]
            if scored:
                row = max(scored, key=lambda r: r['errors'][mode]['maxima'][name])
                maxima[name] = row['errors'][mode]['maxima'][name]
                where[name] = dict(event=row['index'], t=row['t'], **row['errors'][mode]['argmax'][name])
            else:
                maxima[name], where[name] = None, None
        complete = len(scored) == len(rows)
        out['modes'][mode] = dict(complete=complete, maxima=maxima if complete else {k: None for k in maxima}, finiteDiagnosticMaxima=maxima, argmax=where)
    out['paired'] = [dict(event=r['index'], t=r['t'], validRoots=r['validRoots'], **{m: r['errors'][m]['maxima'] if r['errors'][m] else None for m in ('predict', 'hold')}) for r in rows]
    out['comparisons'] = {name: {relation: sum(r['errors']['predict'] is not None and r['errors']['hold'] is not None and fn(r['errors']['predict']['maxima'][name], r['errors']['hold']['maxima'][name]) for r in rows) for relation, fn in [('better', lambda x,y:x<y), ('equal', lambda x,y:x==y), ('worse', lambda x,y:x>y)]} for name in cfg['thresholds']}
    out['gates'] = {name: dict(tolerance=tol, absolute=out['modes']['predict']['complete'] and out['modes']['predict']['maxima'][name] <= tol, noWorseThanHold=out['modes']['predict']['complete'] and out['modes']['hold']['complete'] and out['modes']['predict']['maxima'][name] <= out['modes']['hold']['maxima'][name]) for name, tol in cfg['thresholds'].items()}
    out['pass'] = len(rows) == cfg['targets'] and out['scoredEvents'] == len(rows) and out['invalidRoots'] == 0 and all(x['absolute'] and x['noWorseThanHold'] for x in out['gates'].values())
    return out


def main():
    start = time.monotonic()
    p = pathlib.Path(sys.argv[1]).resolve()
    repo = p.parent.parent
    cfg = json.loads((p/'config.json').read_text())
    out = p/'results'
    def guard():
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        require(time.monotonic()-start < cfg['limits']['cooperativeSeconds'], 'cooperative-wall-cap')
        require(rss < cfg['limits']['rssBytes'], 'cooperative-rss-cap')
    for pin in [cfg['input']]+cfg['provenance']:
        b = (repo/pin['path']).read_bytes()
        require(len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256'], 'dependency-pin')
    old_review = json.loads((repo/cfg['provenance'][0]['path']).read_text())
    old_closure = json.loads((repo/cfg['provenance'][1]['path']).read_text())
    old_manifest = json.loads((repo/cfg['provenance'][2]['path']).read_text())
    old_receipt = json.loads((repo/cfg['provenance'][3]['path']).read_text())
    require(old_review['pass'] is True and old_review['complete'] is True and old_review['failures'] == [], 'inherited-review-passed')
    require(old_closure['supervisor_success'] is True and old_closure['returncode'] == 0, 'inherited-review-closure')
    for pin in [cfg['input']]+cfg['provenance'][:2]:
        require(pin in old_manifest['files'], 'inherited-manifest-membership')
    require(old_receipt['remoteManifestMatchesLocal'] is True and old_receipt['localAndCommittedPinsMatch'] is True and old_receipt['manifestSha256'] == cfg['provenance'][2]['sha256'], 'inherited-publication-evidence')
    fixtures = []
    base = [[.5, .75, 1., .1]]
    for name, history, target in [('startup', [(0, 0., base)], 1.), ('constant', [(0, 0., base), (1, 1., base)], 2.), ('linear', [(0, 0., [[.2,.3,.4,.5]]), (1, 2., [[.3,.4,.5,.6]])], 3.), ('overshoot', [(0, 0., [[.8]]), (1, 1., [[.95]])], 2.)]:
        predicted, scale = predict(history, target)
        fixtures.append(dict(id=name, roots=predicted, scale=scale, invalidRoots=invalid_roots(predicted)))
    invalid = [[math.nan, math.inf, -math.inf, 0., 1.1]]
    fixtures.append(dict(id='serialization', roots=invalid, scale=None, invalidRoots=invalid_roots(invalid)))
    with (out/'controls.json').open('x') as f:
        f.write(encoded(fixtures))
    source = json.loads((repo/cfg['input']['path']).read_text(), parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite-input-json')))
    require(source['complete'] is True and source['failure'] is None and source['dt'] == cfg['dt'] and source['mode'] == 'reuse10ms', 'completed-source')
    require(source['id'] == 'boids16-reuse10ms-0.00125' and source['case'] == 'boids16' and source['end'] == cfg['duration'], 'source-identity')
    require(len(source['events']) == cfg['events'], 'source-event-count')
    first = source['events'][0]
    x0, _ = admit_event(first, 0, cfg)
    history = [(0, first['t'], x0)]
    rows = []
    with (out/'prediction-trace.jsonl').open('x') as trace, (out/'events.jsonl').open('x') as data:
        for k in range(1, cfg['events']):
            guard()
            target_time = source['events'][k]['t']
            estimate, scale = predict(history, target_time)
            antecedents = [h[0] for h in history]
            trace.write(encoded(dict(index=k, t=target_time, predecessorIds=antecedents, scale=scale, predictedRoots=estimate)))
            trace.flush()
            # Prediction has been retained before exposing the target root to scoring.
            event = source['events'][k]
            roots, fresh = admit_event(event, k, cfg)
            hold_roots = history[-1][2]
            held = loads(event['states'], hold_roots, cfg['armCoordinate'])
            require(near(held['forces'], event['left']['forces'], cfg) and near(held['corrections'], event['left']['corrections'], cfg), 'held-left-correspondence')
            invalid = invalid_roots(estimate)
            record = dict(index=k, t=target_time, predecessorIds=antecedents, method='cold-start-hold' if k == 1 else 'secant', scale=scale, predictedRoots=estimate, holdRoots=hold_roots, oracleRoots=roots, validRoots=not invalid, invalidRoots=invalid, scoreStatus='scored', scoreReason=None, loads=dict(predict=None, hold=held, fresh=fresh), errors=dict(predict=None, hold=errors(held, fresh, cfg)))
            try:
                require(finite_tree(estimate), 'nonfinite-predicted-root')
                predicted = loads(event['states'], estimate, cfg['armCoordinate'])
                record['errors']['predict'] = errors(predicted, fresh, cfg)
                record['loads']['predict'] = predicted
            except (ValueError, OverflowError) as exc:
                record['scoreStatus'], record['scoreReason'] = 'unscored', str(exc)
            data.write(encoded(record)); data.flush()
            rows.append(record)
            history = (history+[(k, target_time, roots)])[-2:]
    primary = summarize(rows, cfg)
    secondary = summarize(rows[1:], cfg)
    # Secondary has no qualification: its199-event population excludes mandatory startup.
    secondary.pop('pass')
    result = dict(kind=cfg['kind'], input=cfg['input'], inheritedGeometry=True, inputAdmission=True, complete=True, primary=primary, secondarySecantOnly=secondary, scientificPass=primary['pass'], decision='passed-endpoint-screen' if primary['pass'] else 'rejected-fixed-secant', elapsedSeconds=time.monotonic()-start, performanceMeasurement=False)
    guard()
    with (out/'summary.json').open('x') as f:
        f.write(encoded(result))
    print(encoded(dict(complete=True, decision=result['decision'], events=len(rows))).strip())


if __name__ == '__main__':
    if sys.flags.optimize:
        raise RuntimeError('Nonoptimized Python required')
    main()
