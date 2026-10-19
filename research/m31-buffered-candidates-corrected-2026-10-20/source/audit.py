#!/usr/bin/env python3
"""One bounded, saved-evidence-only audit. Never imports or runs a native kernel.

Source preparation does not execute this file. Its sole execution belongs to the
separately frozen audit allocation, after the native supervisor has closed.
"""
import copy
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import struct
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
OUT = BASE / 'results'
AUDIT_LIMIT = 2 * 1048576
NATIVE_LIMIT = 512 * 1048576
START = None
PINS = {}
CHECKS = []
WORD = re.compile(r'[0-9a-f]{16}\Z')
SHA = re.compile(r'[0-9a-f]{64}\Z')
AMOUNTS = [0, .02, .04, .06, .08, .10, .30, .32]
LIMITS = dict(halfWidth=.125, absoluteCoordinateLimit=2**20,
              maxCandidateEntries=2000000, screenThreshold=4, outwardEndpointUlps=1)
COUNTERS = ['queries', 'builds', 'reuses', 'fallbacks', 'invalidations',
            'identityRebuilds', 'boxExitRebuilds', 'buildOrderedPairs',
            'buildAxisIntervalTests', 'containmentCoordinateTests']
NAMES = ['initial-near-screen-face', 'cross-positive-and-negative-screen-face-within-box',
         'exact-outward-box-upper-face', 'one-ulp-outside-box-rebuild',
         'fresh-motor-and-input-permutation', 'fresh-attitude', 'changed-id',
         'changed-count', 'global-span-fallback', 'recover-from-fallback',
         'large-coordinate-cache-fallback', 'duplicate-id-refusal']
ORIGINAL = 'research/m31-buffered-candidates-2026-10-20'
ORIGINAL_PINS = {
    'results/failure.json': (187, '9811abfa62c03eed8934331d3204da3d0cf6289a0702025928cb305160dc4a30'),
    'results/exit.json': (99, '5a193035e20aabef93f022bb17ee58d5850cfcbb493c556f4c4e50637b53684b'),
    'results/queries.jsonl': (42917, '3bc3aebf57171b5f78a3de3a66647f67df9346a9e03b20f2df29c4fe8b1ecc92'),
    'results/semantic-9f632f89b794d1836a8bc34854be9e2b9f310aad34cb1ed4ff67b889f4d772ab.json':
        (8724, '9f632f89b794d1836a8bc34854be9e2b9f310aad34cb1ed4ff67b889f4d772ab'),
    'supervisor.json': (83, '672fd4dc6394813afe4aa8935bcfd6ce86a6e6700b354558a72b4c4fb3399cc3'),
}
ORIGINAL_DOMAIN_FILE = next(name for name in ORIGINAL_PINS if name.startswith('results/semantic-'))


class AuditFailure(Exception):
    pass


def need(condition, message):
    if not condition:
        raise AuditFailure(message)


def tick():
    need(START is not None and time.monotonic() - START < 120, 'audit wall budget')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def display(path):
    return str(path.relative_to(ROOT))


def compact(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode()


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def parse(data):
    def bad(value):
        raise AuditFailure('nonfinite JSON constant: ' + value)
    return json.loads(data, object_pairs_hook=strict_pairs, parse_constant=bad)


def raw(path, limit=NATIVE_LIMIT):
    tick()
    need(path.is_file() and not path.is_symlink(), 'missing/nonregular file: ' + display(path))
    size = path.stat().st_size
    need(0 < size <= limit, 'file size: ' + display(path))
    data = path.read_bytes()
    need(len(data) == size, 'file changed while reading')
    PINS[str(path.relative_to(ROOT))] = dict(bytes=size, sha256=digest(data))
    return data


def read(path, limit=NATIVE_LIMIT):
    return parse(raw(path, limit))


def result(name):
    need(isinstance(name, str) and Path(name).name == name, 'unsafe result filename')
    return read(OUT / name)


def pin(reference, prefix):
    need(isinstance(reference, dict) and set(reference) == {'file', 'bytes', 'sha256'}, 'reference shape')
    name = reference['file']
    need(isinstance(name, str) and Path(name).name == name and name.startswith(prefix), 'reference filename')
    data = raw(OUT / name)
    need(reference['bytes'] == len(data) and reference['sha256'] == digest(data), 'reference bytes/hash: ' + name)
    return parse(data), data


def finite(value, nonnegative=False):
    need(type(value) in (int, float) and math.isfinite(value), 'finite numeric field')
    if nonnegative:
        need(value >= 0, 'negative duration/counter')
    return value


def word(value):
    return struct.pack('>d', float(value)).hex()


def number(value):
    need(isinstance(value, str) and WORD.fullmatch(value), 'binary64 word')
    ans = struct.unpack('>d', bytes.fromhex(value))[0]
    need(math.isfinite(ans), 'nonfinite binary64 evidence')
    return ans


def date(value):
    d = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    need(d.tzinfo is not None, 'timestamp timezone')
    return d


def source_chain():
    manifest_data = raw(BASE / 'source-manifest.json')
    manifest = parse(manifest_data)
    receipt = read(BASE / 'source-publication.json')
    need(receipt['manifestSha256'] == digest(manifest_data), 'manifest publication hash')
    need(receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True,
         'exact public/committed byte verification')
    need(re.fullmatch(r'[0-9a-f]{40}', receipt['commit']), 'full source commit')
    files = manifest['files']
    seen = set()
    for p in files:
        tick()
        name = p['path']
        need(name not in seen and not Path(name).is_absolute() and '..' not in Path(name).parts,
             'manifest unique safe paths')
        seen.add(name)
        data = raw(ROOT / name)
        need(p['bytes'] == len(data) and p['sha256'] == digest(data), 'source pin: ' + name)
    required = [BASE / 'PROTOCOL.md', BASE / 'CLAIMS.md', BASE / 'review/CORRECTION-REVIEW.md',
                BASE / 'source/audit.py', BASE / 'source/audit-supervise.py',
                BASE / 'source/run.cjs', BASE / 'source/candidate.cjs',
                BASE / 'source/candidate-kernel.cjs', BASE / 'source/candidate-cache.cjs',
                BASE / 'source/CANDIDATE.md',
                ROOT / 'research/m31-cost-decision-2026-10-18/input-words.json',
                ROOT / 'research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs']
    required += [ROOT / ORIGINAL / name for name in ORIGINAL_PINS]
    for p in required:
        need(str(p.relative_to(ROOT)) in seen, 'missing required manifest member: ' + display(p))
    for name in ['candidate.cjs', 'candidate-kernel.cjs', 'candidate-cache.cjs']:
        old = ROOT / ORIGINAL / 'source' / name
        need(str(old.relative_to(ROOT)) in seen, 'original candidate source provenance')
        need(raw(BASE / 'source' / name) == raw(old), 'correction must not change candidate source')
    # Traverse literal local CJS imports as text, never as modules.
    queue = [BASE / 'source/run.cjs']
    visited = set()
    while queue:
        p = queue.pop().resolve()
        if p in visited:
            continue
        visited.add(p)
        need(str(p.relative_to(ROOT)) in seen, 'unmanifested local dependency')
        for name in re.findall(r"require\(['\"]([^'\"]+)['\"]\)", p.read_text()):
            if name.startswith('.'):
                target = (p.parent / name).resolve()
                need(target.suffix == '.cjs', 'unexpected local module kind')
                queue.append(target)
    env = result('environment.json')
    need(env['sourceCommit'] == receipt['commit'] and env['manifestSha256'] == receipt['manifestSha256'],
         'run source identity')
    age = (date(env['startedUtc']) - date(receipt['verifiedUtc'])).total_seconds()
    need(0 <= age < 86400, 'public source verification launch age')
    need(isinstance(env['node'], str) and env['node'].startswith('v'), 'runtime recorded')
    launch = date(raw(OUT / 'launch.lock', 256).decode())
    need(0 <= (date(env['startedUtc']) - launch).total_seconds() < 180, 'launch/environment chronology')
    supervisor = read(BASE / 'supervisor.json')
    need((BASE / 'supervisor-launch.lock').is_file(), 'native supervisor single-use lock')
    need(supervisor.get('returncode') == 0 and not supervisor.get('timeout'), 'native supervisor completion')
    need(0 <= finite(supervisor['wallSeconds']) <= 210, 'native supervisor wall cap')
    CHECKS.append('public source, full transitive local dependency pins, input pin, launch age and supervisor')
    return receipt, env


def original_failure():
    """Recheck immutable failed allocation; never restart or interpret its costs."""
    old = ROOT / ORIGINAL
    for name, (size, sha) in ORIGINAL_PINS.items():
        data = raw(old / name)
        need(len(data) == size and digest(data) == sha, 'original failure provenance pin')
    failure = read(old / 'results/failure.json')
    closed = read(old / 'results/exit.json')
    supervisor = read(old / 'supervisor.json')
    need(failure['calls'] == closed['calls'] == 18 and failure['allocation'] == 'closed-no-rerun'
         and closed['allocation'] == 'closed' and closed['exitCode'] == 1,
         'original allocation failed closed at 18 calls')
    need(supervisor['returncode'] == 1 and not supervisor.get('timeout'), 'original supervisor failure closure')
    rows = [parse(line) for line in raw(old / 'results/queries.jsonl').splitlines()]
    need(len(rows) == 18, 'original exactly eighteen calls')
    for i, row in enumerate(rows):
        stage = i // 2
        need(row['call'] == i+1 and row['phase'] == 'control' and row['batch'] == -1
             and row['stage'] == stage and row['method'] == ('F' if i%2 == 0 else 'C'), 'original control-only schedule')
        need(row['status'] == ('domain-refused' if stage == 8 else 'native-success'), 'original status sequence')
        ref = row['semantic']
        need(Path(ref['file']).name == ref['file'], 'original reference filename')
        data = raw(old / 'results' / ref['file'])
        need(len(data) == ref['bytes'] and digest(data) == ref['sha256'], 'original actual semantic bytes/hash')
        if i % 2:
            need(ref == rows[i-1]['semantic'], 'original full F/C pair equality')
    need(not list((old / 'results').glob('batch-*.json')) and not list((old / 'results').glob('warmup-*.json'))
         and not (old / 'results/summary.json').exists(), 'original no completed timing panel')
    CHECKS.append('immutable original failed allocation: eighteen control calls, nine exact semantic pairs, no warmup or measured panel; no timing interpretation')
    return dict(package=ORIGINAL, calls=18, pairs=9, stoppedStage=8,
                status='domain-refused', reason='native-admission', measuredQueries=0,
                correction='control status expectation only; fresh separate 168-call allocation')


def input_shape(value, duplicate=False):
    need(set(value) == {'drones'} and isinstance(value['drones'], list), 'input shape')
    ids = []
    for drone in value['drones']:
        need(set(drone) == {'id', 'state'}, 'drone shape')
        ident = drone['id']
        need(type(ident) is int and 0 <= ident <= 2**53 - 1, 'safe canonical ID')
        need(isinstance(drone['state'], list) and len(drone['state']) == 17, '17-state shape')
        for v in drone['state']:
            number(v)
        need(all(number(v) > 0 for v in drone['state'][13:17]), 'positive nominal forces')
        ids.append(ident)
    need(0 < len(ids) <= 5000, 'input count')
    need((len(set(ids)) < len(ids)) if duplicate else (len(set(ids)) == len(ids)), 'duplicate ID control')


def saved_inputs():
    seed = read(ROOT / 'research/m31-cost-decision-2026-10-18/input-words.json')
    # Historical input may carry provenance alongside its drones array.
    initial = {'drones': seed['drones']}
    input_shape(initial)
    need(len(initial['drones']) == 1000, 'seed population')
    inputs = []
    for s, a in enumerate(AMOUNTS):
        value = result('input-' + str(s) + '.json')
        input_shape(value)
        expected = copy.deepcopy(initial)
        for d, old in zip(expected['drones'], initial['drones']):
            ident = d['id']
            d['state'][0] = word(number(old['state'][0]) + (1 if ident % 2 == 0 else -1) * a)
            d['state'][1] = word(number(old['state'][1]) + (1 if ident % 3 == 0 else -1) * a / 2)
            for r in range(13, 17):
                d['state'][r] = word(number(old['state'][r]) * (1 + .001 * s))
        need(value == expected, 'prescribed snapshot words: ' + str(s))
        need(value == read(ROOT / ORIGINAL / ('results/input-' + str(s) + '.json')), 'corrected snapshots unchanged from original allocation')
        inputs.append(value)
    generation = result('generation.json')
    need(generation['amounts'] == AMOUNTS and generation['kind'] == 'prescribed-synthetic-positions-and-thrust-not-integration', 'generation recipe')
    finite(generation['generationAndInputPersistenceMs'], True)
    controls = result('control-inputs.json')
    need(controls == read(ROOT / ORIGINAL / 'results/control-inputs.json'), 'corrected control inputs unchanged from original allocation')
    need(len(controls) == 12 and [c['name'] for c in controls] == NAMES, 'control order/names')
    for i, c in enumerate(controls):
        need(set(c) == {'name', 'input'}, 'control fields')
        input_shape(c['input'], i == 11)
    force = number(initial['drones'][0]['state'][13])
    def drone(ident, x, z=0):
        return {'id': ident, 'state': [word(v) for v in [x, 0, z, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, force, force, force, force]]}
    p = {'drones': [drone(0, 0), drone(1, 0, 1), drone(2, 4.05, 1.5)]}
    expected = [copy.deepcopy(p)]
    p['drones'][2]['state'][0] = word(3.99); expected.append(copy.deepcopy(p))
    p['drones'][2]['state'][0] = word(math.nextafter(4.05 + .125, math.inf)); expected.append(copy.deepcopy(p))
    p['drones'][2]['state'][0] = word(math.nextafter(number(p['drones'][2]['state'][0]), math.inf)); expected.append(copy.deepcopy(p))
    p['drones'][1]['state'][13] = word(force * 1.01)
    q = copy.deepcopy(p); q['drones'].reverse(); expected.append(q)
    # Saved trig words are checked for the prescribed small tilt, without a
    # cross-runtime Math.sin/Math.cos bit-equivalence assumption. Frozen source
    # fixes their exact generating expressions; all other fields match exactly.
    tilt = controls[5]['input']['drones'][1]['state']
    sn, cs = number(tilt[7]), number(tilt[9])
    need(abs(sn - .024997395914712332) <= 1e-15 and abs(cs - .9996875162757026) <= 1e-15,
         'prescribed small attitude perturbation')
    p['drones'][1]['state'][7] = tilt[7]; p['drones'][1]['state'][9] = tilt[9]; expected.append(copy.deepcopy(p))
    p['drones'][1]['id'] = 3; expected.append(copy.deepcopy(p))
    p['drones'].append(drone(4, -.5, 2)); expected.append(copy.deepcopy(p))
    p['drones'][3]['state'][0] = word(300); expected.append(copy.deepcopy(p))
    p['drones'][3]['state'][0] = word(-.5); expected.append(copy.deepcopy(p))
    for d in p['drones']:
        d['state'][0] = word(number(d['state'][0]) + 2**40)
    expected.append(copy.deepcopy(p))
    p['drones'][1]['id'] = 0; expected.append(copy.deepcopy(p))
    need([c['input'] for c in controls] == expected, 'frozen control field changes')
    CHECKS.append('eight independently reconstructed binary64 snapshots and all twelve control recipes')
    return inputs, [c['input'] for c in controls]


def scalar_semantic(v):
    if isinstance(v, dict):
        need(list(v) == sorted(v), 'canonical semantic object key order')
        for item in v.values():
            scalar_semantic(item)
    elif isinstance(v, list):
        for item in v:
            scalar_semantic(item)
    else:
        need(v is None or type(v) in (str, bool), 'unencoded semantic number')


def encoded(v):
    if type(v) in (int, float):
        return word(v)
    if isinstance(v, list):
        return [encoded(x) for x in v]
    if isinstance(v, dict):
        return {k: encoded(v[k]) for k in sorted(v)}
    return v


def semantic_shape(value, current, refused, domain_refused=False):
    base_keys = {'schema', 'model', 'status', 'reason', 'constants', 'raw', 'ids', 'prepared', 'coefficients', 'diagnostics'}
    need(set(value) == base_keys | ({'stage'} if refused or domain_refused else {'loads', 'solution', 'consumption'}), 'full semantic top-level fields')
    need(value['schema'] == 'm31-native-load-result-v1' and value['model'] == 'ordinary-binary64-full-contribution', 'native model/schema')
    need(isinstance(value['constants'], dict) and set(value['constants']) == {'mg', 'arm', 'radius', 'rho', 'A', 'R', 'D', 'decay', 'spread', 'origin', 'minDown', 'neighbor', 'nearRad', 'downFade', 'downCut', 'radFade', 'radCut', 'induced', 'kappa'}, 'complete constants')
    for v in value['constants'].values():
        number(v)
    if refused:
        need(value['status'] == 'input-refused' and value['reason'] == 'duplicate-id' and value['stage'] == 'input', 'duplicate refusal semantics')
        need(all(value[k] is None for k in ['raw', 'ids', 'prepared', 'coefficients', 'diagnostics']), 'refusal partial evidence')
        return
    if domain_refused:
        # Exactly this already observed control failure, not a broad relaxation
        # of successful-query requirements or a tolerance-based comparison.
        need(value['status'] == 'domain-refused' and value['reason'] == 'native-admission'
             and value['stage'] == 'build', 'precise wide-span domain refusal')
        need(value == read(ROOT / ORIGINAL / ORIGINAL_DOMAIN_FILE), 'exact original wide-span semantic record')
        canonical = sorted(current['drones'], key=lambda x: x['id'])
        need(value['ids'] == [word(d['id']) for d in canonical]
             and value['raw'] == [{'id': word(d['id']), 'state': d['state']} for d in canonical], 'domain refusal raw current input')
        need(len(value['prepared']) == len(canonical) == 4 and value['coefficients'] is not None, 'domain refusal retained build evidence')
        diag = value['diagnostics']
        need(set(diag) == {'admission', 'input', 'graph', 'symbolCounts', 'screen', 'geometryWork'}, 'domain refusal exact partial diagnostic fields')
        need(diag['admission']['admitted'] is False and diag['admission']['reasons'] == ['invalid-term']
             and diag['admission']['invalidTermCount'] == word(24), 'wide-span inherited invalid-term refusal')
        need(diag['screen']['eligible'] is False and diag['screen']['fallbackReason'] == 'span-out-of-range', 'global fallback predicate evidence')
        return
    need(value['status'] == 'native-success' and value['reason'] is None, 'native success')
    canonical = sorted(current['drones'], key=lambda x: x['id'])
    ids = [word(d['id']) for d in canonical]
    need(value['ids'] == ids and value['raw'] == [{'id': word(d['id']), 'state': d['state']} for d in canonical], 'raw canonical input identity')
    n = len(canonical)
    for name in ['prepared', 'loads', 'solution']:
        need(isinstance(value[name], list) and len(value[name]) == n and [r['id'] for r in value[name]] == ids, 'full per-ID outputs: ' + name)
    for d, p, load, sol in zip(canonical, value['prepared'], value['loads'], value['solution']):
        need(set(p) == {'id', 'center', 'axis', 'offsets', 'points', 'forces', 'nativeTotal', 'nativeBeta', 'nativeNu'}, 'prepared fields')
        need(p['center'] == d['state'][:3] and p['forces'] == d['state'][13:17], 'fresh prepared centers/forces')
        need(len(p['axis']) == 3 and len(p['offsets']) == len(p['points']) == len(p['nativeNu']) == 4, 'prepared shape')
        need(all(len(v) == 3 for v in p['offsets'] + p['points']), 'prepared rotor vectors')
        need(set(load) == {'id', 'rotor', 'collective', 'worldForce', 'worldMoment'}, 'load fields')
        need(len(load['rotor']) == 4 and len(load['worldForce']) == len(load['worldMoment']) == 3, 'load shape')
        need(set(sol) == {'id', 'y', 'rotors'} and len(sol['rotors']) == 4 and all(set(r) == {'alpha', 'x', 'T'} for r in sol['rotors']), 'solution fields')
    coeff = value['coefficients']
    need(set(coeff) == {'offsets', 'sourceIndices', 'K', 'a'}, 'coefficient fields')
    offsets = [int(number(v)) for v in coeff['offsets']]
    sources = [int(number(v)) for v in coeff['sourceIndices']]
    need(all(word(v) == w for v, w in zip(offsets, coeff['offsets'])) and all(word(v) == w for v, w in zip(sources, coeff['sourceIndices'])), 'integer coefficient indexing')
    need(len(offsets) == 4*n+1 and offsets[0] == 0 and offsets[-1] == len(sources) == len(coeff['K']) == len(coeff['a']) <= 2000000, 'coefficient full shape')
    for r in range(4*n):
        need(0 <= offsets[r] <= offsets[r+1] <= len(sources), 'coefficient offset order')
        row = sources[offsets[r]:offsets[r+1]]
        need(row == sorted(set(row)) and all(0 <= v < n and v != r//4 for v in row), 'coefficient canonical source order')
    need(all(number(v) > 0 for v in coeff['K'] + coeff['a']), 'positive coefficients')
    diag = value['diagnostics']
    need(set(diag) == {'admission', 'input', 'graph', 'symbolCounts', 'screen', 'geometryWork', 'ordinaryLmax', 'scheduleIndices', 'solveWork', 'residualWork', 'residualLog', 'sourceReceiverMismatch'}, 'complete semantic diagnostics')
    need('gatheredNonselfCandidates' not in diag['geometryWork'] and 'orderedPairVisits' not in diag['screen'] and 'componentTests' not in diag['screen'], 'exact allowed diagnostic exclusions')
    need(diag['admission']['admitted'] is True and diag['graph']['descendingEligible'] is True, 'native admitted graph')
    need(sorted(diag['scheduleIndices']) == sorted(word(i) for i in range(n)), 'full schedule permutation')
    need(0 <= number(diag['residualLog']) <= 1e-9 and 0 <= number(diag['sourceReceiverMismatch']) <= 2e-9, 'native residual bounds')
    consumption = value['consumption']
    need(set(consumption) == {'kind', 'status', 'loadWords', 'identityWords', 'statusCharacters', 'value'}, 'consumption fields')
    need(consumption['kind'] == 'native-load-id-status-fnv32' and consumption['status'] == 'native-success' and consumption['loadWords'] == word(11*n) and consumption['identityWords'] == word(n), 'complete load consumption count')


def journal(inputs, controls):
    data = raw(OUT / 'queries.jsonl')
    need(data.endswith(b'\n'), 'complete journal final line')
    rows = [parse(line) for line in data.splitlines()]
    schedule = [('control', -1, s, m) for s in range(12) for m in ['F', 'C']]
    for batch in range(-1, 8):
        order = ['F', 'C'] if batch % 2 == 0 else ['C', 'F']
        schedule.extend(('warmup' if batch == -1 else 'measured', batch, s, m) for m in order for s in range(8))
    need(len(rows) == len(schedule) == 168, 'exact native query allocation')
    records, cached = {}, {}
    keys = {'inputPreserved', 'inputBeforeSha256', 'inputAfterSha256', 'witness', 'derivedLoadsSha256', 'call', 'phase', 'batch', 'stage', 'method', 'outerMs', 'status', 'reason', 'semantic', 'cache', 'excluded', 'encodePersistMs'}
    for call, (row, expected) in enumerate(zip(rows, schedule), 1):
        tick()
        need(set(row) == keys and row['call'] == call and (row['phase'], row['batch'], row['stage'], row['method']) == expected, 'query schedule/fields')
        phase, batch, stage, method = expected
        current = controls[stage] if phase == 'control' else inputs[stage]
        refused = phase == 'control' and stage == 11
        domain_refused = phase == 'control' and stage == 8
        current_hash = digest(compact(current))
        need(row['inputPreserved'] is True and row['inputBeforeSha256'] == row['inputAfterSha256'] == current_hash, 'saved input preservation')
        finite(row['outerMs'], True); finite(row['encodePersistMs'], True)
        ref = row['semantic']; sha = ref['sha256']
        need(isinstance(sha, str) and SHA.fullmatch(sha) and ref['file'] == 'semantic-' + sha + '.json', 'content-addressed semantic name')
        if sha not in cached:
            value, body = pin(ref, 'semantic-')
            scalar_semantic(value)
            need(body == compact(value) + b'\n', 'canonical full semantic bytes')
            cached[sha] = (value, body)
        value, body = cached[sha]
        need(ref['bytes'] == len(body), 'semantic referenced size')
        semantic_shape(value, current, refused, domain_refused)
        need(row['status'] == value['status'] and row['reason'] == value['reason'], 'journal semantic status')
        need(row['derivedLoadsSha256'] == digest(compact(value.get('loads'))), 'derived-load digest')
        ex = row['excluded']; timing = ex['timing']
        need(set(timing) == {'clock', 'totalMs', 'phasesMs', 'boundary'} and timing['clock'] == 'performance.now', 'native timing fields')
        need(0 <= finite(timing['totalMs']) <= row['outerMs'], 'inner/outer timer nesting')
        need('complete load-word/ID/status consumption' in timing['boundary'], 'native timing boundary')
        for v in timing['phasesMs'].values():
            finite(v, True)
        need(abs(sum(timing['phasesMs'].values()) - timing['totalMs']) <= max(1e-6, timing['totalMs']*1e-12), 'native phase telescope')
        if not refused:
            expected_ex = {'timing', 'geometryWork', 'screen'} | (set() if domain_refused else {'buildPhasesMs'})
            need(set(ex) == expected_ex, 'excluded records complete for success/domain-refusal')
            geometry = dict(ex['geometryWork']); geometry.pop('gatheredNonselfCandidates')
            screen = dict(ex['screen']); screen.pop('orderedPairVisits'); screen.pop('componentTests')
            need(encoded(geometry) == value['diagnostics']['geometryWork'] and encoded(screen) == value['diagnostics']['screen'], 'saved diagnostic exclusions retain all other fields')
        else:
            need(set(ex) == {'timing'}, 'refused excluded fields')
        wanted_witness = method == 'C' and (phase == 'control' or batch == 0)
        need((row['witness'] is not None) == wanted_witness and (row['cache'] is not None) == (method == 'C'), 'witness/cache allocation')
        records[expected] = (row, value)
    pairs = []
    for phase, batch, stage, method in schedule:
        if method != 'F':
            continue
        left, _ = records[(phase, batch, stage, 'F')]
        right, _ = records[(phase, batch, stage, 'C')]
        need(left['semantic'] == right['semantic'], 'full F/C semantic byte equality')
        pairs.append((left['call'], right['call']))
    comparisons = result('comparisons.json')
    need(len(comparisons) == 84 and [(c['a'], c['b']) for c in comparisons] == pairs, 'all pair comparisons recorded')
    for c in comparisons:
        need(set(c) == {'a', 'b', 'comparisonMs'}, 'comparison timing fields')
        finite(c['comparisonMs'], True)
    control_rows = [records[('control', -1, s, 'C')][0] for s in range(12)]
    need(control_rows[3]['derivedLoadsSha256'] != control_rows[4]['derivedLoadsSha256'] != control_rows[5]['derivedLoadsSha256'], 'force/attitude changes delivered loads')
    CHECKS.append('168 exact scheduled queries, 84 full semantic equalities, input preservation, complete output structure and timing nesting')
    return rows, records, control_rows


def fresh_cache():
    return dict(counters={k: 0 for k in COUNTERS}, cached=None,
                last=dict(action='reset', reason=None, n=None, candidateEntries=0))


def cache_step(state, current, refused=False):
    if refused:
        return
    drones = sorted(current['drones'], key=lambda d: d['id'])
    ids = [d['id'] for d in drones]
    centers = [[number(v) for v in d['state'][:3]] for d in drones]
    n = len(ids); counts = state['counters']; counts['queries'] += 1
    cache = state['cached']
    def invalidate():
        if state['cached'] is not None:
            counts['invalidations'] += 1
        state['cached'] = None
    fallback = None
    if any(max(p[k] for p in centers) - min(p[k] for p in centers) > 256 for k in range(3)):
        fallback = 'global-screen-ineligible'
    elif any(abs(v) > 2**20 for p in centers for v in p):
        fallback = 'absolute-coordinate-bound'
    if fallback:
        counts['fallbacks'] += 1; invalidate()
        state['last'] = dict(action='fallback', reason=fallback, n=n, candidateEntries=0)
        return
    reason = 'cold'
    if cache is not None:
        reason = 'count-change' if len(cache['ids']) != n else ('id-change' if cache['ids'] != ids else None)
        if reason:
            counts['identityRebuilds'] += 1
        else:
            for i, center in enumerate(centers):
                for k, value in enumerate(center):
                    counts['containmentCoordinateTests'] += 1
                    if not cache['boxes'][6*i+2*k] <= value <= cache['boxes'][6*i+2*k+1]:
                        reason = 'box-exit'; counts['boxExitRebuilds'] += 1; break
                if reason:
                    break
        if reason is None:
            counts['reuses'] += 1
            state['last'] = dict(action='reuse', reason='all-current-centers-inside-stored-boxes', n=n, candidateEntries=cache['entries'])
            return
    invalidate()
    boxes = [bound for center in centers for value in center
             for bound in (math.nextafter(value-.125, -math.inf), math.nextafter(value+.125, math.inf))]
    rows = [[] for _ in ids]
    for i in range(n):
        tick()
        for j in range(n):
            if i == j:
                continue
            counts['buildOrderedPairs'] += 1
            excluded = False
            for k in range(3):
                counts['buildAxisIntervalTests'] += 1
                if boxes[6*j+2*k] - boxes[6*i+2*k+1] >= 4 or boxes[6*j+2*k+1] - boxes[6*i+2*k] <= -4:
                    excluded = True; break
            if not excluded:
                rows[i].append(ids[j])
    entries = sum(map(len, rows))
    need(entries <= 2000000, 'candidate cap')
    state['cached'] = dict(ids=ids, boxes=boxes, rows=rows, entries=entries)
    counts['builds'] += 1
    state['last'] = dict(action='build', reason=reason, n=n, candidateEntries=entries)


def expected_stats(state):
    cache = state['cached']
    return {**state['counters'], 'cached': cache is not None,
            'cachedN': len(cache['ids']) if cache else 0,
            'cachedCandidateEntries': cache['entries'] if cache else 0,
            'last': state['last'], 'limits': LIMITS}


def witness_check(witness, state, current, omission=True):
    cache = state['cached']
    keys = {'schema', 'cached', 'ids', 'boxes', 'rows', 'entries', 'last'} | ({'boxLayout'} if cache else set())
    need(set(witness) == keys and witness['schema'] == 'm31-buffered-candidate-witness-v1', 'witness schema')
    need(witness['cached'] == (cache is not None) and witness['last'] == state['last'], 'witness event')
    if not cache:
        need(witness['ids'] == witness['boxes'] == witness['rows'] == [] and witness['entries'] == 0, 'empty fallback witness')
        return 0
    need(witness['boxLayout'] == 'six words per canonical ID: xLo,xHi,yLo,yHi,zLo,zHi', 'witness layout')
    need(witness['ids'] == cache['ids'], 'witness current canonical IDs')
    need(witness['boxes'] == cache['boxes'], 'witness exact build boxes / required rebuild')
    ids = witness['ids']; n = len(ids); id_set = set(ids)
    need(len(witness['rows']) == n and len(witness['boxes']) == 6*n, 'witness full shape')
    for i, row in enumerate(witness['rows']):
        need(row == sorted(set(row)) and ids[i] not in row and all(v in id_set for v in row), 'witness source identity/order/uniqueness')
    need(witness['rows'] == cache['rows'] and witness['entries'] == cache['entries'], 'witness exact conservative candidate coverage')
    if not omission:
        return 0
    centers = [[number(v) for v in d['state'][:3]] for d in sorted(current['drones'], key=lambda d: d['id'])]
    boxes = witness['boxes']; omitted = 0
    for i, p in enumerate(centers):
        tick()
        need(all(boxes[6*i+2*k] <= p[k] <= boxes[6*i+2*k+1] for k in range(3)), 'witness current containment')
        row = set(witness['rows'][i])
        for j, q in enumerate(centers):
            if i == j or ids[j] in row:
                continue
            omitted += 1
            need(any(boxes[6*j+2*k] - boxes[6*i+2*k+1] >= 4 or boxes[6*j+2*k+1] - boxes[6*i+2*k] <= -4 for k in range(3)), 'omitted pair lacks interval separation')
            need(any(abs(q[k] - p[k]) >= 4 for k in range(3)), 'omitted pair survives current F component screen')
    return omitted


def cache_audit(records, controls, inputs, control_rows):
    state = fresh_cache(); control_states = []; witnesses = []; omitted = 0
    for s, row in enumerate(control_rows):
        cache_step(state, controls[s], s == 11)
        need(row['cache'] == expected_stats(state), 'exact control cache counters/event: ' + str(s))
        witness, _ = pin(row['witness'], 'witness-')
        need(row['witness']['file'] == 'witness-' + str(row['call']) + '.json', 'witness call identity')
        omitted += witness_check(witness, state, controls[s], s != 11)
        control_states.append(copy.deepcopy(state)); witnesses.append(witness)
    need(control_rows[10]['cache'] == control_rows[11]['cache'] and witnesses[10] == witnesses[11], 'duplicate refuses before any cache access')
    need(result('control-cache.json') == [r['cache'] for r in control_rows], 'control cache export')
    state = fresh_cache(); expected_stream = []
    for s in range(8):
        row = records[('measured', 0, s, 'C')][0]
        cache_step(state, inputs[s])
        need(row['cache'] == expected_stats(state), 'exact measured cache counters/event')
        need(state['last']['action'] == ('build' if s in (0, 6) else 'reuse'), 'stream cache event schedule')
        witness, _ = pin(row['witness'], 'witness-')
        need(row['witness']['file'] == 'witness-' + str(row['call']) + '.json', 'stream witness call identity')
        omitted += witness_check(witness, state, inputs[s])
        expected_stream.append(copy.deepcopy(expected_stats(state)))
    for batch in range(-1, 8):
        phase = 'warmup' if batch == -1 else 'measured'
        for s in range(8):
            need(records[(phase, batch, s, 'C')][0]['cache'] == expected_stream[s], 'identical reset/cache evidence every stream')
    # Negative tests mutate only small, already-saved control witnesses. No
    # native query, coefficient calculation, or timing experiment occurs here.
    tests = []
    def rejects(name, damaged, expected, current):
        rejected = False; why = ''
        try:
            witness_check(damaged, expected, current, False)
        except AuditFailure as error:
            rejected = True; why = str(error)
        need(rejected, 'audit negative test accepted: ' + name)
        tests.append(dict(name=name, rejected=True, reason=why,
                          mutatedWitnessSha256=digest(compact(damaged))))
    source = witnesses[0]
    row_index = next(i for i, row in enumerate(source['rows']) if len(row) >= 2)
    damaged = copy.deepcopy(source); damaged['rows'][row_index].pop(); rejects('missing-candidate', damaged, control_states[0], controls[0])
    damaged = copy.deepcopy(source); damaged['rows'][row_index].append(damaged['rows'][row_index][0]); rejects('duplicate-candidate', damaged, control_states[0], controls[0])
    damaged = copy.deepcopy(source); damaged['rows'][row_index].reverse(); rejects('noncanonical-order', damaged, control_states[0], controls[0])
    damaged = copy.deepcopy(source); damaged['ids'][0] = 999999; rejects('stale-identity', damaged, control_states[0], controls[0])
    damaged = copy.deepcopy(witnesses[2]); damaged['last'] = copy.deepcopy(witnesses[3]['last']); rejects('missed-box-exit-rebuild', damaged, control_states[3], controls[3])
    CHECKS.append('all control and first measured-stream witnesses, outward boxes, exact rows, all omitted current pairs, counters, reuse and invalidation; five rejecting witness mutations')
    return dict(witnessCount=20, omittedOrderedPairsChecked=omitted, negativeTests=tests,
                streamCacheEvents=[v['last'] for v in expected_stream])


def timing_and_view(records, inputs):
    totals = {}; batches = []
    for batch in range(-1, 8):
        phase = 'warmup' if batch == -1 else 'measured'
        for method in ['F', 'C']:
            timing = result(phase + '-' + str(batch) + '-' + method + '.json')
            need(set(timing) == {'resetMs', 'sumQueryMs', 'totalMs'}, 'stream timing fields')
            total = finite(timing['resetMs'], True)
            for s in range(8):
                total += records[(phase, batch, s, method)][0]['outerMs']
            need(total == timing['totalMs'] and total - timing['resetMs'] == timing['sumQueryMs'], 'sequential reset-plus-query sum')
            need(total > 0, 'positive stream time')
            totals[(batch, method)] = total
        if batch >= 0:
            f, c = totals[(batch, 'F')], totals[(batch, 'C')]
            expected = dict(batch=batch, order=['F', 'C'] if batch % 2 == 0 else ['C', 'F'], F=f, C=c, ratio=c/f)
            need(result('batch-' + str(batch) + '.json') == expected, 'paired batch arithmetic')
            batches.append(expected)
    ratios = sorted(b['ratio'] for b in batches)
    median = (ratios[3] + ratios[4]) / 2
    wins = sum(b['C'] < b['F'] for b in batches)
    gate = median <= .9 and wins >= 7
    summary = result('summary.json')
    need(set(summary) == {'completed', 'calls', 'batches', 'medianRatio', 'strictWins', 'numericalEquality', 'costGate', 'scope', 'wallMs', 'bytesWritten'}, 'summary fields')
    need(summary['completed'] is True and summary['calls'] == 168 and summary['numericalEquality'] is True, 'completed correctness gate')
    need(summary['batches'] == batches and summary['medianRatio'] == median and summary['strictWins'] == wins and summary['costGate'] is gate, 'decision arithmetic')
    need(summary['scope'] == 'fixed synthetic state stream, Node query-only cost, not flight or physical validation', 'claim scope')
    need(0 <= summary['wallMs'] <= 180000, 'native summary wall budget')
    view = result('view-data.json')
    frames = [dict(stage=s, positions=[[number(v) for v in d['state'][:3]] for d in inputs[s]['drones']], cache=records[('measured', 0, s, 'C')][0]['cache']) for s in range(8)]
    need(view == dict(schema='m31-buffered-view-v1', synthetic=True, drones=1000, frames=frames,
                      batches=batches, medianRatio=median, strictWins=wins, costGate=gate), 'viewer is exact saved synthetic data')
    exit_record = result('exit.json')
    need(set(exit_record) == {'calls', 'wallMs', 'bytesWritten', 'exitCode', 'allocation'} and exit_record['exitCode'] == 0 and exit_record['allocation'] == 'closed' and exit_record['calls'] == 168, 'native allocation closed successfully')
    need(summary['wallMs'] <= finite(exit_record['wallMs']) <= 180000, 'native exit deadline')
    need(not (OUT / 'failure.json').exists(), 'native failure present')
    CHECKS.append('all reset-inclusive sequential totals, eight ratios, median, strict wins and frozen decision; saved-view equality')
    return dict(batches=batches, medianRatio=median, strictWins=wins, costGate=gate), summary, exit_record


def inventory(summary, exit_record):
    native = {}
    for p in OUT.iterdir():
        tick()
        if p.name in {'audit.lock', 'audit.json'}:
            continue
        need(p.is_file() and not p.is_symlink(), 'unexpected result directory/symlink')
        data = raw(p)
        native[p.name] = dict(bytes=len(data), sha256=digest(data))
    total = sum(v['bytes'] for v in native.values())
    need(total <= NATIVE_LIMIT, 'native persisted payload cap')
    need(exit_record['bytesWritten'] == total - native['exit.json']['bytes'], 'exit exact payload accounting')
    need(summary['bytesWritten'] == total - sum(native[n]['bytes'] for n in ['summary.json', 'view-data.json', 'exit.json']), 'summary exact payload accounting')
    expected_names = {'launch.lock', 'environment.json', 'generation.json', 'control-inputs.json', 'queries.jsonl', 'control-cache.json', 'comparisons.json', 'summary.json', 'view-data.json', 'exit.json'}
    expected_names |= {'input-' + str(s) + '.json' for s in range(8)}
    expected_names |= {'batch-' + str(b) + '.json' for b in range(8)}
    expected_names |= {(('warmup' if b == -1 else 'measured') + '-' + str(b) + '-' + m + '.json') for b in range(-1, 8) for m in ['F', 'C']}
    journal_rows = [parse(line) for line in (OUT / 'queries.jsonl').read_bytes().splitlines()]
    expected_names |= {r['semantic']['file'] for r in journal_rows}
    expected_names |= {r['witness']['file'] for r in journal_rows if r['witness'] is not None}
    need(set(native) == expected_names, 'exact native result inventory')
    CHECKS.append('complete native artifact inventory and exact payload accounting within 512 MiB')
    return total, native


def main():
    global START
    START = time.monotonic()
    lock = OUT / 'audit.lock'
    # Permanent on success, failure, interruption or supervisor kill. No rerun.
    with lock.open('xb') as f:
        f.write((dt.datetime.now(dt.timezone.utc).isoformat() + '\n').encode())
    def expired(signum, frame):
        raise AuditFailure('audit wall budget')
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    report = {'schema': 'm31-buffered-saved-audit-v1', 'passed': False,
              'allocation': 'closed-no-rerun', 'nativeQueriesExecuted': 0,
              'scope': 'saved finite implementation-equivalence and fixed synthetic-stream query-cost evidence; no physical validation or general proof'}
    code = 1
    try:
        receipt, env = source_chain()
        previous_failure = original_failure()
        inputs, controls = saved_inputs()
        rows, records, control_rows = journal(inputs, controls)
        cache = cache_audit(records, controls, inputs, control_rows)
        timing, summary, exit_record = timing_and_view(records, inputs)
        payload, artifacts = inventory(summary, exit_record)
        tick()
        report.update(passed=True, sourceCommit=receipt['commit'], manifestSha256=receipt['manifestSha256'],
                      originalFailure=previous_failure,
                      environment=env, calls=168, pairedComparisons=84, cache=cache, timing=timing,
                      nativePayloadBytes=payload, nativeArtifacts=artifacts)
        code = 0
    except Exception as error:
        report['failure'] = (type(error).__name__ + ': ' + str(error)).replace(str(ROOT), '[repository]')[:1500]
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        report.update(checks=CHECKS, filePins=PINS, wallSeconds=time.monotonic()-START)
        if report['wallSeconds'] >= 120:
            report['passed'] = False; report['failure'] = 'audit wall budget'; code = 1
        body = compact(report) + b'\n'
        # Reserve space for the external supervisor receipt and permanent lock.
        if len(body) + lock.stat().st_size > AUDIT_LIMIT - 8192:
            body = compact(dict(schema=report['schema'], passed=False, allocation='closed-no-rerun',
                                failure='audit output budget', nativeQueriesExecuted=0)) + b'\n'
            code = 1
        with (OUT / 'audit.json').open('xb') as f:
            f.write(body)
        print(json.dumps({'passed': code == 0, 'report': display(OUT / 'audit.json'), 'bytes': len(body)}))
    return code


if __name__ == '__main__':
    sys.exit(main())
