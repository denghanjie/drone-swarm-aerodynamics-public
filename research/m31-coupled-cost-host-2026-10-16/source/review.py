#!/usr/bin/env python3
"""Saved-record audit only. No geometry, model maps, roots, or timing runs."""
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

CASES = [('n1000-t20', 1000), ('n5000-t20', 5000), ('n5000-t60', 5000), ('n5000-t180', 5000)]
PERMS = ['ABC', 'BCA', 'CAB', 'CBA', 'ACB', 'BAC']
FULL_PHASES = ['input', 'index', 'geometry', 'admission', 'setup', 'solve', 'residual', 'checksum', 'remainder']
CACHED_PHASES = ['solve', 'residual', 'checksum']
TINY = float.fromhex('0x0.0000000000001p-1022')


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


class Audit:
    def __init__(self, package):
        self.package = package
        self.root = package.parent.parent
        self.prior = package.parent/'m31-swarm-coupling-transfer-2026-10-16'
        self.started = time.monotonic()
        self.checks, self.errors = [], []
        self.hash_cache = {}
        self.qualified = {}
        self.qualification_summaries = []
        self.control_summaries = []
        self.calls = []
        self.evidence = {}
        self.resources = {}

    def guard(self):
        require(time.monotonic()-self.started < 55, 'saved review cooperative 55-second guard')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        require(rss <= 1.5*(1 << 30), 'saved review RSS guard')

    def check(self, ok, name, details=None):
        rec = {'name': name, 'pass': bool(ok)}
        if details is not None:
            rec['details'] = safe_json(details)
        self.checks.append(rec)
        if not ok:
            self.errors.append(name)
        return bool(ok)

    def error(self, name, error):
        message = str(error).replace(str(self.package), '<package>').replace(str(self.root), '<repo>')
        self.check(False, name, {'type': type(error).__name__, 'message': message})

    def path(self, base, relative):
        require(isinstance(relative, str) and relative, 'artifact path missing')
        rel = Path(relative)
        require(not rel.is_absolute() and '..' not in rel.parts, 'artifact path must be relative')
        path = (base/rel).resolve()
        require(path.is_relative_to(base.resolve()) and path.is_file(), 'artifact missing or outside its base')
        return path

    def digest(self, path):
        self.guard()
        stat = path.stat()
        key = (str(path), stat.st_size, stat.st_mtime_ns)
        if key not in self.hash_cache:
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1 << 20), b''):
                    self.guard()
                    digest.update(chunk)
            self.hash_cache[key] = digest.hexdigest()
        return self.hash_cache[key]

    def pin(self, base, meta, name, size=None):
        require(isinstance(meta, dict), name+' metadata absent')
        path = self.path(base, meta.get('path'))
        actual_size = path.stat().st_size
        self.check(type(meta.get('bytes')) is int and meta['bytes'] == actual_size, name+'.bytes')
        if size is not None:
            require(actual_size == size, name+' binary shape/size mismatch')
        self.check(valid_sha(meta.get('sha256')) and self.digest(path) == meta['sha256'], name+'.sha256')
        return path

    def close(self, got, wanted, name, atol=1e-12, rtol=1e-12):
        self.check(finite(got) and finite(wanted) and abs(got-wanted) <= atol+rtol*abs(wanted), name)

    def numeric(self, actual, reference, name, atol=0., rtol=1e-9):
        a, b = np.asarray(actual, dtype=float), np.asarray(reference, dtype=float)
        if a.shape != b.shape:
            self.check(False, name, {'actualShape': list(a.shape), 'referenceShape': list(b.shape)})
            return {'length': int(a.size), 'maxAbs': None, 'maxRel': None, 'bad': max(int(a.size), 1),
                    'firstMismatch': None, 'pass': False}
        with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
            delta = np.abs(a-b)
            rel = delta/np.maximum(np.abs(b), TINY)
        bad = ~(np.isfinite(a) & np.isfinite(b)) | (delta > atol+rtol*np.abs(b))
        flat_bad = np.flatnonzero(bad.ravel())
        first = None
        if flat_bad.size:
            i = int(flat_bad[0])
            first = {'index': i, 'actual': float(a.ravel()[i]), 'reference': float(b.ravel()[i])}
        rec = dict(length=int(a.size), maxAbs=float(np.max(delta, initial=0.)),
                   maxRel=float(np.max(rel, initial=0.)), bad=int(np.count_nonzero(bad)),
                   firstMismatch=first, **{'pass': not bool(flat_bad.size)})
        self.check(rec['pass'], name, rec)
        return rec

    def numeric_record(self, saved, expected, name):
        require(isinstance(saved, dict), name+' comparison record absent')
        for key in ('length', 'bad', 'pass'):
            self.check(saved.get(key) == expected[key], name+'.'+key)
        for key in ('maxAbs', 'maxRel'):
            wanted = expected[key]
            if wanted is None or not finite(wanted):
                self.check(saved.get(key) is None, name+'.'+key)
            else:
                self.close(saved.get(key), wanted, name+'.'+key, atol=1e-14, rtol=1e-12)
        self.check(saved.get('firstMismatch') == safe_json(expected['firstMismatch']), name+'.firstMismatch')


def expected_schedule():
    output = []
    def add(workload, case, methods, block, warmup):
        for method in methods:
            output.append(dict(sequence=len(output), workload=workload, id=case,
                               method=method, block=block, warmup=warmup))
    for case, _ in CASES:
        add('full', case, 'ABC', -1, True)
    for block in range(6):
        for j in range(4):
            c = (j+block) % 4
            add('full', CASES[c][0], PERMS[(block+c) % 6], block, False)
    for case, _ in CASES:
        add('cached', case, 'OP', -1, True)
    for block in range(6):
        for j in range(4):
            add('cached', CASES[(j+block) % 4][0], 'PO' if block % 2 else 'OP', block, False)
    return output


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


def controls_review(audit):
    listed = audit.evidence.get('controls', [])
    expected = expected_controls()
    audit.check([r.get('id') for r in listed] == [x[0] for x in expected], 'controls.fixed-coverage-order')
    for ident, tokens, grid in expected:
        audit.guard()
        name = 'control.'+ident
        try:
            rec = load_json(audit.path(audit.package, 'results/control-'+ident+'.json'))
            n = len(tokens)
            audit.check(rec.get('id') == ident and rec.get('n') == n and rec.get('positionTokens') == tokens,
                        name+'.fixed-identity-tokens')
            audit.check(rec.get('expectedGrid') is grid, name+'.expectedGrid')
            matches = [r for r in listed if r.get('id') == ident]
            audit.check(len(matches) == 1 and matches[0] == rec, name+'.evidence-copy')
            for mode in ('all', 'grid'):
                item = rec[mode]
                symbols = np.asarray(item['symbols'], dtype=np.int64)
                require(symbols.shape == (4*n*n,), 'control symbol shape mismatch')
                audit.check(np.all((symbols >= 1) & (symbols <= 11)), name+'.'+mode+'.terminal-symbols')
                audit.check(np.bincount(symbols, minlength=12).tolist() == item['symbolCounts'], name+'.'+mode+'.counts')
                offsets, sources, kvals = np.asarray(item['offsets']), np.asarray(item['sources'], dtype=np.int64), np.asarray(item['K'])
                validate_csr(audit, offsets, sources, kvals, n, name+'.'+mode)
                check_work(audit, item['geometryWork'], n, len(sources), name+'.'+mode+'.work')
                check_certificate(audit, item['certificate'], item['geometryWork'], mode, name+'.'+mode, grid)
            for key in ('symbols', 'symbolCounts', 'offsets', 'sources', 'K', 'admission', 'graph'):
                audit.check(rec['all'][key] == rec['grid'][key], name+'.agreement.'+key)
            if ident in ('far-invalid258', 'nonfinite-nan', 'nonfinite-infinity', 'overflow-span'):
                audit.check(rec['all']['symbolCounts'][11] > 0 and not rec['all']['admission']['admitted'],
                            name+'.invalid-guard-rejection-retained')
            if ident == 'near-field':
                audit.check(rec['all']['symbolCounts'][4] > 0 and not rec['all']['admission']['admitted'],
                            name+'.near-rejection-retained')
            audit.check(rec.get('pass') is True, name+'.candidate-pass')
            audit.control_summaries.append({'id': ident, 'complete': True, 'grid': grid,
                                            'admitted': rec['all']['admission']['admitted']})
        except Exception as error:
            audit.error(name+'.review-error', error)
            audit.control_summaries.append({'id': ident, 'complete': False})


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


def solution_review(audit, saved, ref, n, name, s0):
    values, y, rotors, residual_y = rotor_values(saved, n)
    expected_values, _, _, _ = rotor_values(ref, n)
    comparison = audit.numeric(values, expected_values, name+'.all-saved-values', rtol=1e-9)
    audit.check(np.all(np.isfinite(y) & (y > 0)) and np.all(np.isfinite(residual_y) & (residual_y > 0)),
                name+'.amplitude-domain')
    audit.check(np.all(rotors[:, :, 0] >= 0) and np.all((rotors[:, :, 1] > 0) & (rotors[:, :, 1] <= 1)) and
                np.all(rotors[:, :, 2] > 0), name+'.rotor-domain')
    for key in ('work', 'residualWork'):
        audit.check(saved.get(key) == ref.get(key), name+'.'+key)
    iterations = saved.get('iterations', 1)
    audit.check(iterations == ref.get('iterations', 1) and saved.get('converged', True) == ref.get('converged', True),
                name+'.termination')
    for key, limit in [('residualLog', 1e-9), ('sourceReceiverMismatch', 2e-9)]:
        audit.check(finite(saved.get(key)) and 0 <= saved[key] <= limit, name+'.'+key+'-limit')
    if np.all(y > 0) and np.all(residual_y > 0):
        observed = float(np.max(np.abs(np.log(residual_y)-np.log(y))))
        audit.close(saved.get('residualLog'), observed, name+'.recorded-map-log-distance', atol=2e-12, rtol=2e-12)
        audit.check(observed <= 1e-9, name+'.saved-map-residual-small')
    residual_forces = np.asarray([[r['T'] for r in row] for row in saved['residualMap']['rotors']], dtype=float)
    residual_total = ((residual_forces[:, 0]+residual_forces[:, 1])+residual_forces[:, 2])+residual_forces[:, 3]
    mismatch = float(np.max(np.abs(s0*y*y-residual_total)/s0))
    audit.close(saved.get('sourceReceiverMismatch'), mismatch, name+'.saved-force-total-mismatch', atol=2e-12, rtol=2e-12)
    audit.check(mismatch <= 2e-9, name+'.saved-force-mismatch-small')
    if 'iterations' in saved:
        trace = np.asarray(saved.get('iterates'), dtype=float)
        reference_trace = np.asarray(ref.get('iterates'), dtype=float)
        require(type(iterations) is int and 1 <= iterations <= 64 and trace.shape == (iterations+1, n), 'Picard trace shape')
        comparison['trace'] = audit.numeric(trace.ravel(), reference_trace.ravel(), name+'.saved-trace-vs-reference', rtol=1e-9)
        audit.check(np.array_equal(trace[0], np.ones(n)) and np.array_equal(trace[-1], y), name+'.trace-endpoints')
        require(np.all(np.isfinite(trace) & (trace > 0)), 'Picard trace domain')
        changes = np.max(np.abs(np.diff(np.log(trace), axis=0)), axis=1)
        audit.check(np.all(changes[:-1] > 1e-11) and changes[-1] <= 1e-11 and saved.get('converged') is True,
                    name+'.first-converged-stop')
        audit.close(saved.get('lastChange'), float(changes[-1]), name+'.lastChange', atol=2e-12, rtol=2e-12)
        audit.check(saved.get('lastChange') == ref.get('lastChange'), name+'.reference-lastChange-exact')
    return comparison


def symbols_compare(audit, new_meta, old_meta, n, name, wanted_counts):
    new_path = audit.pin(audit.package, new_meta, name+'.new')
    old_path = audit.pin(audit.prior, old_meta, name+'.reference')
    expected_bytes = 4*n*n
    audit.check(new_meta.get('rawBytes') == expected_bytes and new_path.stat().st_size <= 64*(1 << 20), name+'.size-cap')
    hashes = [hashlib.sha256(), hashlib.sha256()]
    total = mismatches = 0
    counts = np.zeros(12, dtype=np.int64)
    with gzip.open(new_path, 'rb') as left, gzip.open(old_path, 'rb') as right:
        while total < expected_bytes:
            audit.guard()
            amount = min(1 << 20, expected_bytes-total)
            a, b = left.read(amount), right.read(amount)
            require(len(a) == len(b) == amount, 'short symbol tensor')
            hashes[0].update(a)
            hashes[1].update(b)
            aa, bb = np.frombuffer(a, dtype=np.uint8), np.frombuffer(b, dtype=np.uint8)
            mismatches += int(np.count_nonzero(aa != bb))
            require(np.all(aa <= 11), 'symbol outside schema range')
            counts += np.bincount(aa, minlength=12)
            total += amount
        audit.check(left.read(1) == b'' and right.read(1) == b'', name+'.no-trailing-symbols')
    audit.check(hashes[0].hexdigest() == new_meta.get('rawSha256'), name+'.new-raw-hash')
    audit.check(hashes[1].hexdigest() == old_meta.get('rawSha256'), name+'.reference-raw-hash')
    audit.check(mismatches == 0, name+'.all-symbols-exact', {'entries': total, 'mismatches': mismatches})
    audit.check(counts.tolist() == wanted_counts and counts[0] == 0, name+'.complete-counts')
    return mismatches


def read_array(audit, base, meta, dtype, count, name):
    path = audit.pin(base, meta, name, np.dtype(dtype).itemsize*count)
    return np.fromfile(path, dtype=dtype)


def saved_checksum(solution, kvals):
    # Arithmetic over already saved outputs only; no map or root evaluation.
    value = 0.
    for i, y in enumerate(solution['y']):
        total = 0.
        for rotor in solution['rotors'][i]:
            total += rotor['T']
        value += y*(i+1)+total
    return (value+(float(kvals[0]) if len(kvals) else 0.))+(float(kvals[-1]) if len(kvals) else 0.)


def qualification_review(audit):
    records = audit.evidence.get('qualification', [])
    wanted = [(case, label) for case, _ in CASES for label in ('all', 'grid')]
    audit.check([(r.get('id'), r.get('label')) for r in records] == wanted, 'qualification.fixed-coverage-order')
    index = load_json(audit.path(audit.prior, 'inputs/index.json'))
    entries = {entry['id']: entry for entry in index['cases']}
    for ident, n in CASES:
        audit.guard()
        old = None
        baseline = None
        try:
            entry = entries[ident]
            input_path = audit.pin(audit.prior, entry, ident+'.input-bytes', n*17*8)
            # Saved motor-state arithmetic only: no poses, geometry or model maps.
            nominal = np.fromfile(input_path, dtype='<f8').reshape((n, 17))[:, 13:17].copy()
            s0 = ((nominal[:, 0]+nominal[:, 1])+nominal[:, 2])+nominal[:, 3]
            require(np.all(np.isfinite(nominal) & (nominal > 0)) and np.all(np.isfinite(s0)), 'reference nominal inputs invalid')
            old = load_json(audit.path(audit.prior, 'results/'+ident+'.json'))
            audit.check(old['id'] == ident and old['n'] == n and old['inputSha256'] == entry['sha256'], ident+'.reference-identity')
            old_m = old['geometryWork']['positiveRotorTerms']
            old_arrays = [read_array(audit, audit.prior, old['csr'][key], dtype, count, ident+'.ref-'+key)
                          for key, dtype, count in [('offsets', '<u4', 4*n+1), ('sources', '<u4', old_m), ('K', '<f8', old_m)]]
            for label in ('all', 'grid'):
                name = ident+'.'+label
                before = len(audit.errors)
                try:
                    audit.guard()
                    rec = load_json(audit.path(audit.package, 'results/qualification-'+ident+'-'+label+'.json'))
                    matches = [r for r in records if r.get('id') == ident and r.get('label') == label]
                    audit.check(len(matches) == 1 and matches[0] == rec, name+'.qualification-copy')
                    persistence = rec['persistence']
                    bundle_path = audit.pin(audit.package, persistence['meta'], name+'.bundle')
                    doc = load_json(bundle_path)
                    audit.check(doc.get('id') == ident and doc.get('label') == label and doc.get('n') == n, name+'.identity')
                    for key in ('input', 'admission', 'graph', 'symbolCounts', 'ordinaryLmax'):
                        audit.check(doc.get(key) == old.get(key), name+'.reference-'+key)
                    audit.check(doc['admission']['admitted'] and doc['graph']['descendingEligible'], name+'.admitted-topological')
                    for key in ('centerEligiblePairs', 'centerGuardRejectedPairs', 'pairCalls', 'positiveRotorTerms'):
                        audit.check(doc['geometryWork'][key] == old['geometryWork'][key], name+'.reference-work-'+key)
                    m = doc['geometryWork']['positiveRotorTerms']
                    require(type(m) is int and 0 <= m <= 2_000_000, 'invalid retained term count')
                    artifacts = doc['artifacts']
                    offsets, sources, kvals, aa = [read_array(audit, audit.package, artifacts[key], dtype, count, name+'.'+key)
                        for key, dtype, count in [('offsets', '<u4', 4*n+1), ('sources', '<u4', m), ('K', '<f8', m), ('a', '<f8', m)]]
                    validate_csr(audit, offsets, sources, kvals, n, name)
                    audit.check(np.all(np.isfinite(aa) & (aa >= 0)), name+'.a-finite-nonnegative')
                    row_ids = np.repeat(np.arange(4*n), np.diff(offsets.astype(np.int64)))
                    expected_a = (kvals*np.sqrt(s0[sources]/(.027*9.81)) /
                                  np.sqrt(nominal.ravel()[row_ids]/(2*1.225*(math.pi*.023*.023))))
                    audit.numeric(aa, expected_a, name+'.saved-coefficient-scaling-consistency', atol=2e-12, rtol=2e-12)
                    audit.check(np.array_equal(offsets, old_arrays[0]), name+'.reference-offsets')
                    audit.check(np.array_equal(sources, old_arrays[1]), name+'.reference-sources')
                    k_compare = audit.numeric(kvals, old_arrays[2], name+'.reference-K', atol=2e-12, rtol=2e-12)
                    symbols_compare(audit, artifacts['symbols'], old['symbols'], n, name+'.symbols', doc['symbolCounts'])
                    check_work(audit, doc['geometryWork'], n, m, name+'.work')
                    check_certificate(audit, doc['certificate'], doc['geometryWork'], label, name+'.certificate')
                    matrix_bytes = hashlib.sha256()
                    for values in (offsets, sources, kvals, aa):
                        matrix_bytes.update(values.tobytes())
                    for field in ('matrixHash', 'solutionHashes'):
                        audit.check(doc.get(field) == rec.get(field), name+'.'+field+'-record-copy')
                    audit.check(valid_sha(doc.get('matrixHash')) and all(valid_sha(doc['solutionHashes'].get(k)) for k in ('O', 'P')),
                                name+'.fingerprint-formats')
                    if baseline is not None:
                        audit.check(doc['matrixHash'] == baseline['matrixHash'] and doc['solutionHashes'] == baseline['solutionHashes'],
                                    name+'.all-grid-fingerprint-agreement')
                        audit.numeric(aa, baseline['a'], name+'.all-grid-a', atol=0., rtol=0.)
                    else:
                        baseline = {'matrixHash': doc['matrixHash'], 'solutionHashes': doc['solutionHashes'], 'a': aa.copy()}
                    comparison = rec['comparison']
                    for field in ('symbols', 'offsets', 'sources', 'input', 'admission', 'graph', 'counts', 'L', 'geometry', 'pass'):
                        audit.check(comparison.get(field) is True, name+'.candidate-comparison.'+field)
                    audit.numeric_record(comparison.get('K'), k_compare, name+'.candidate-K-stats')
                    compact_solutions = {}
                    for method, ref_key, comparison_key in [('O', 'direct', 'direct'), ('P', 'picard', 'picard')]:
                        saved = doc['solutions'][method]
                        stats = solution_review(audit, saved, old['solutions'][ref_key], n, name+'.'+method, s0)
                        candidate = comparison[comparison_key]
                        audit.numeric_record(candidate['values'], stats, name+'.'+method+'.candidate-values')
                        for key in ('work', 'termination', 'residual', 'pass'):
                            audit.check(candidate.get(key) is True, name+'.'+method+'.candidate-'+key)
                        if method == 'P':
                            audit.numeric_record(comparison.get('trace'), stats['trace'], name+'.candidate-trace-stats')
                            audit.check(comparison.get('lastChange') is True, name+'.candidate-lastChange')
                        compact_solutions[method] = {key: saved.get(key, default) for key, default in
                            [('work', None), ('residualWork', None), ('iterations', 1), ('converged', True),
                             ('lastChange', None), ('residualLog', None), ('sourceReceiverMismatch', None)]}
                        compact_solutions[method].update(valuesLength=26*n, checksum=saved_checksum(saved, kvals),
                                                        hash=doc['solutionHashes'][method])
                    for key in ('qualificationComputeMs',):
                        audit.check(finite(rec.get(key)) and rec[key] >= 0, name+'.'+key)
                    for key in ('compressionMs', 'hashSerializeBufferedWriteMs', 'totalPersistenceMs'):
                        audit.check(finite(persistence.get(key)) and persistence[key] >= 0, name+'.'+key)
                    audit.close(persistence['compressionMs']+persistence['hashSerializeBufferedWriteMs'], persistence['totalPersistenceMs'],
                                name+'.persistence-phase-accounting', atol=1e-7, rtol=1e-12)
                    audit.check(persistence.get('fsync') is False, name+'.buffered-I-O-label')
                    audit.qualified[(ident, label)] = dict(n=n, m=m, matrixHash=doc['matrixHash'],
                        matrixBytesSha256=matrix_bytes.hexdigest(), solutions=compact_solutions,
                        geometryWork=doc['geometryWork'], certificate=doc['certificate'])
                    audit.qualification_summaries.append(dict(id=ident, label=label, complete=True,
                        **{'pass': len(audit.errors) == before}, matrixBytesSha256=matrix_bytes.hexdigest(),
                        qualificationComputeMs=rec['qualificationComputeMs'], persistence=persistence))
                except Exception as error:
                    audit.error(name+'.review-error', error)
                    audit.qualification_summaries.append(dict(id=ident, label=label, complete=False, **{'pass': False}))
        except Exception as error:
            audit.error(ident+'.reference-review-error', error)


def timing_review(audit):
    listed = audit.evidence.get('timings', [])
    schedule = expected_schedule()
    audit.check(len(listed) == len(schedule), 'timing.evidence-count-140')
    available_raw = list((audit.package/'results').glob('call-*-raw.json'))
    available_validated = [x for x in (audit.package/'results').glob('call-*.json') if not x.name.endswith('-raw.json')]
    audit.check(len(available_raw) == 140 and len(available_validated) == 140, 'timing.raw-and-validated-file-count')
    for planned in schedule:
        audit.guard()
        seq = planned['sequence']
        name = 'call.'+str(seq)
        before = len(audit.errors)
        try:
            raw_path = audit.path(audit.package, f'results/call-{seq:03d}-raw.json')
            raw = load_json(raw_path)
            audit.check(all(raw.get(key) == value for key, value in planned.items()), name+'.raw-schedule')
            path = audit.package/f'results/call-{seq:03d}.json'
            if not path.is_file():
                audit.calls.append({**raw, 'reviewComplete': False})
                audit.check(False, name+'.validation-record-missing')
                continue
            rec = load_json(path)
            audit.pin(audit.package, rec['raw'], name+'.raw-pin')
            audit.check({key: value for key, value in rec.items() if key not in ('raw', 'validation')} == raw, name+'.raw-before-validation-copy')
            audit.check(seq < len(listed) and rec == listed[seq], name+'.evidence-copy')
            audit.check(all(rec.get(key) == value for key, value in planned.items()), name+'.validated-schedule')
            phases = rec['phasesMs']
            keys = FULL_PHASES if planned['workload'] == 'full' else CACHED_PHASES
            audit.check(set(phases) == set(keys), name+'.phase-coverage')
            audit.check(finite(rec.get('totalMs')) and rec['totalMs'] > 0, name+'.duration-positive')
            audit.check(all(finite(phases.get(key)) and phases[key] >= (-1e-7 if key == 'remainder' else 0) for key in keys),
                        name+'.phase-durations')
            audit.close(sum(phases[key] for key in keys), rec['totalMs'], name+'.phase-total-accounting', atol=1e-7, rtol=1e-12)
            ident, method = planned['id'], planned['method']
            label = 'all' if method == 'A' else 'grid'
            solver = 'P' if method in ('C', 'P') else 'O'
            qualified = audit.qualified[(ident, label)]
            sol = qualified['solutions'][solver]
            for key in ('work', 'residualWork', 'iterations', 'converged', 'lastChange'):
                audit.check(rec.get(key) == sol[key], name+'.qualified-'+key)
            for key in ('residualLog', 'sourceReceiverMismatch'):
                audit.close(rec.get(key), sol[key], name+'.qualified-'+key, atol=2e-12, rtol=2e-12)
            audit.check(rec.get('geometryWork') == qualified['geometryWork'], name+'.qualified-geometry-work')
            audit.check(rec.get('certificate') == qualified['certificate'], name+'.qualified-certificate')
            audit.close(rec.get('checksum'), sol['checksum'], name+'.saved-output-checksum', atol=1e-8, rtol=1e-14)
            validation = rec['validation']
            for key in ('offsets', 'sources', 'repeatGeometry', 'certificate', 'checksum', 'hashesMatch', 'pass'):
                audit.check(validation.get(key) is True, name+'.validation-'+key)
            audit.check(validation.get('matrixHash') == qualified['matrixHash'] and validation.get('solutionHash') == sol['hash'],
                        name+'.repeat-hashes')
            zero_matrix = dict(length=qualified['m'], maxAbs=0., maxRel=0., bad=0, firstMismatch=None, **{'pass': True})
            audit.numeric_record(validation['matrix'], zero_matrix, name+'.matrix-repeat-record')
            audit.numeric_record(validation['aa'], zero_matrix, name+'.a-repeat-record')
            solution_validation = validation['solution']
            for key in ('work', 'termination', 'residual', 'pass'):
                audit.check(solution_validation.get(key) is True, name+'.solution-validation-'+key)
            zero_solution = dict(length=sol['valuesLength'], maxAbs=0., maxRel=0., bad=0, firstMismatch=None, **{'pass': True})
            audit.numeric_record(solution_validation['values'], zero_solution, name+'.solution-repeat-record')
            audit.calls.append({**rec, 'reviewComplete': len(audit.errors) == before})
        except Exception as error:
            audit.error(name+'.review-error', error)


def other_records(audit):
    readings = audit.evidence.get('readings', [])
    caches = audit.evidence.get('cache', [])
    audit.check([r.get('id') for r in readings] == [c[0] for c in CASES], 'readings.fixed-coverage')
    audit.check([r.get('id') for r in caches] == [c[0] for c in CASES], 'cache.fixed-coverage')
    for ident, n in CASES:
        try:
            r = next(r for r in readings if r.get('id') == ident)
            for key in ('inputReadDecodeMs', 'referenceLoadMs'):
                audit.check(finite(r.get(key)) and r[key] >= 0, ident+'.'+key)
            entry = next(x for x in load_json(audit.path(audit.prior, 'inputs/index.json'))['cases'] if x['id'] == ident)
            audit.check(r.get('inputSha256') == entry['sha256'], ident+'.reading-input-sha')
            c = next(c for c in caches if c.get('id') == ident)
            m = audit.qualified[(ident, 'grid')]['m']
            audit.check(c.get('typedCSRBytes') == 4*(4*n+1)+20*m and c.get('nominalAndS0ScalarCount') == 5*n and
                        c.get('orderLength') == n, ident+'.cache-byte-and-shape-accounting')
            audit.check(c.get('origin') == 'qualified grid matrix and qualified schedule' and c.get('buildCostReportedInQualification') is True,
                        ident+'.cache-origin')
            audit.check(finite(c.get('validationMs')) and c['validationMs'] >= 0 and isinstance(c.get('otherResidentState'), str), ident+'.cache-scope')
        except Exception as error:
            audit.error(ident+'.other-records-error', error)
    for stage in ('environmentStart', 'environmentEnd'):
        env = audit.evidence.get(stage)
        audit.check(isinstance(env, dict), stage+'.present')
        if not isinstance(env, dict):
            continue
        for key in ('cpuModel', 'architecture', 'platform', 'kernel', 'node', 'v8', 'clock', 'threads'):
            audit.check(key in env and (env[key] is None or isinstance(env[key], str)), stage+'.'+key)
        audit.check(valid_sha(env.get('nodeExecutableSha256')), stage+'.node-binary-sha')
        audit.check(type(env.get('logicalCores')) is int and env['logicalCores'] > 0 and
                    finite(env.get('installedRAMBytes')) and env['installedRAMBytes'] > 0, stage+'.hardware-counts')
        audit.check(isinstance(env.get('executionFlags'), list) and type(env.get('executionFlagCount')) is int and
                    isinstance(env.get('loadAverage'), list) and len(env['loadAverage']) == 3 and
                    all(finite(x) for x in env['loadAverage']), stage+'.runtime-observations')
        audit.check(all(key in env for key in ('physicalCores', 'powerSource', 'lowPowerMode')) and env.get('pidOmitted') is True,
                    stage+'.scope-fields')
    start, end = audit.evidence.get('environmentStart', {}), audit.evidence.get('environmentEnd', {})
    for key in ('nodeExecutableSha256', 'node', 'v8', 'architecture', 'platform', 'kernel', 'clock'):
        audit.check(key in start and start.get(key) == end.get(key), 'environment.stable-'+key)


def provenance_resources(audit):
    manifest_path = audit.path(audit.package, 'source-manifest.json')
    manifest = load_json(manifest_path)
    pins = manifest.get('files')
    require(isinstance(pins, list) and pins, 'source manifest pins absent')
    seen = set()
    for i, pin in enumerate(pins):
        audit.guard()
        audit.check(pin.get('path') not in seen, 'manifest.unique-path.'+str(i))
        seen.add(pin.get('path'))
        audit.pin(audit.root, pin, 'manifest.pin.'+str(i))
    run = load_json(audit.path(audit.package, 'results/candidate-run.json'))
    audit.check(run.get('kind') == 'candidate' and run.get('returncode') == 0 and not run.get('terminated_for') and
                not run.get('exception_class'), 'candidate.supervisor-success')
    audit.check(run.get('wall_cap_seconds') == 300 and finite(run.get('supervisor_elapsed_seconds')) and
                0 <= run['supervisor_elapsed_seconds'] <= 302, 'candidate.external-time-cap')
    audit.check(run.get('source_manifest_sha256') == audit.digest(manifest_path), 'candidate.pinned-source-manifest')
    audit.check(isinstance(run.get('source_commit'), str) and re.fullmatch('[0-9a-f]{40}', run['source_commit']) is not None,
                'candidate.source-commit-identity')
    audit.check(run.get('rss_cap_bytes') == 1610612736 and finite(run.get('externalSampledPeakRSSKiB')) and
                run['externalSampledPeakRSSKiB']*1024 <= 1610612736, 'candidate.external-sampled-RSS')
    audit.check(type(run.get('rssSamples')) is int and run['rssSamples'] > 0 and
                type(run.get('rssSampleErrors')) is int and run['rssSampleErrors'] >= 0,
                'candidate.external-RSS-samples-present')
    for i, pin in enumerate(run.get('artifacts', [])):
        audit.pin(audit.package, pin, 'candidate.run-artifact.'+str(i))
    memory = audit.evidence.get('memory', {})
    audit.check(finite(memory.get('sampledPeakRSSBytes')) and memory['sampledPeakRSSBytes'] <= 1610612736,
                'candidate.internal-sampled-RSS')
    audit.check(isinstance(memory.get('platformMaxRSSUnits'), str) and isinstance(memory.get('processResourceUsage'), dict),
                'candidate.RSS-unit-semantics')
    known = {'candidate-invocation.lock', 'candidate-stdout.txt', 'candidate-stderr.txt', 'candidate-run.json',
             'review-invocation.lock', 'review-stdout.txt', 'review-stderr.txt', 'review-run.json',
             'independent-review.json', 'analysis.json'}
    total = scientific = normal = before_evidence = 0
    for path in (audit.package/'results').rglob('*'):
        if not path.is_file():
            continue
        require(path.resolve().is_relative_to(audit.package), 'result file outside package')
        size = path.stat().st_size
        total += size
        relative = path.relative_to(audit.package/'results')
        if len(relative.parts) == 1 and relative.name in known:
            continue
        scientific += size
        if str(relative) not in ('failure.json', 'partial-evidence.json'):
            normal += size
        if str(relative) != 'evidence.json':
            before_evidence += size
    audit.check(scientific <= 128*(1 << 20) and normal <= 124*(1 << 20), 'candidate.scientific-byte-cap')
    audit.check(total <= 132*(1 << 20), 'results.total-byte-cap-at-review')
    if audit.evidence.get('complete') is True:
        audit.check(audit.evidence.get('newScientificBytesBeforeEvidence') == before_evidence, 'candidate.before-evidence-byte-accounting')
    audit.resources = dict(candidateExternalElapsedSeconds=run.get('supervisor_elapsed_seconds'),
        candidateSampledPeakRSSBytes=memory.get('sampledPeakRSSBytes'), scientificBytes=scientific,
        externalSampledPeakRSSKiB=run.get('externalSampledPeakRSSKiB'), rssSamples=run.get('rssSamples'),
        rssSampleErrors=run.get('rssSampleErrors'),
        normalScientificBytes=normal, resultBytesAtReview=total, sourceCommit=run.get('source_commit'),
        sourceManifestSha256=run.get('source_manifest_sha256'))


def stats(values):
    return None if not values else dict(count=len(values), median=statistics.median(values), minimum=min(values), maximum=max(values))


def pairs(rows, left, right, delta_label):
    found = []
    for block in range(6):
        a = [r for r in rows if r['block'] == block and r['method'] == left]
        b = [r for r in rows if r['block'] == block and r['method'] == right]
        if len(a) == len(b) == 1 and finite(a[0]['totalMs']) and finite(b[0]['totalMs']) and b[0]['totalMs'] > 0:
            first, second = a[0], b[0]
            found.append(dict(block=block, numeratorMethod=left, denominatorMethod=right,
                              numeratorMs=first['totalMs'], denominatorMs=second['totalMs'],
                              ratio=first['totalMs']/second['totalMs'],
                              deltaDefinition=delta_label, deltaMs=second['totalMs']-first['totalMs']))
    return found


def build_analysis(audit):
    cases = []
    all_call_coverage = len(audit.calls) == 140 and all(r.get('reviewComplete') for r in audit.calls)
    qualification_ok = (len(audit.qualification_summaries) == 8 and
                        all(r.get('pass') and r.get('complete') for r in audit.qualification_summaries))
    for ident, n in CASES:
        full = [r for r in audit.calls if r.get('reviewComplete') and r.get('id') == ident and not r.get('warmup') and r.get('workload') == 'full']
        cached = [r for r in audit.calls if r.get('reviewComplete') and r.get('id') == ident and not r.get('warmup') and r.get('workload') == 'cached']
        methods = {}
        for method in 'ABCOP':
            rows = [r for r in (full if method in 'ABC' else cached) if r['method'] == method]
            phase_names = FULL_PHASES if method in 'ABC' else CACHED_PHASES
            methods[method] = dict(totalMs=stats([r['totalMs'] for r in rows]),
                phasesMs={key: stats([r['phasesMs'][key] for r in rows]) for key in phase_names},
                rawDurationsMs=[{'block': r['block'], 'sequence': r['sequence'], 'totalMs': r['totalMs']} for r in rows])
        bc, ab, op = pairs(full, 'B', 'C', 'C-minus-B'), pairs(full, 'A', 'B', 'B-minus-A'), pairs(cached, 'O', 'P', 'P-minus-O')
        qualified_for_claim = all_call_coverage and qualification_ok and not audit.errors
        wins = sum(p['numeratorMs'] < p['denominatorMs'] for p in bc)
        ratio_stats = stats([p['ratio'] for p in bc])
        practical = None
        if qualified_for_claim and len(bc) == 6:
            practical = ratio_stats['median'] <= .95 and wins >= 5
        contributions = {}
        if len(bc) == 6:
            for key in FULL_PHASES:
                contributions[key] = sum(next(r for r in full if r['block'] == block and r['method'] == 'C')['phasesMs'][key] -
                                         next(r for r in full if r['block'] == block and r['method'] == 'B')['phasesMs'][key] for block in range(6))
        total_delta = sum(p['deltaMs'] for p in bc)
        cases.append(dict(id=ident, n=n, methods=methods,
            primary=dict(contrast='B/C same-grid ordered/Picard', pairs=bc, ratio=ratio_stats,
                         deltaMs=stats([p['deltaMs'] for p in bc]), strictWins=wins, practicalRulePass=practical,
                         sumMatchedSavingsMs=total_delta, phaseContributionSumsMs=contributions,
                         phaseAccountingRemainderMs=total_delta-sum(contributions.values()) if contributions else None),
            allPairsDiagnostic=dict(contrast='A/B all-pairs ordered/grid ordered', pairs=ab,
                                    ratio=stats([p['ratio'] for p in ab]), deltaMs=stats([p['deltaMs'] for p in ab])),
            cachedSeparate=dict(contrast='O/P cached ordered/Picard', pairs=op, ratio=stats([p['ratio'] for p in op]),
                                deltaMs=stats([p['deltaMs'] for p in op]))))
    tested = [case['primary']['practicalRulePass'] for case in cases if case['n'] == 5000]
    practical_all = all(tested) if len(tested) == 3 and all(x is not None for x in tested) else None
    return dict(kind='independent-saved-cost-analysis', complete=all_call_coverage and qualification_ok and not audit.errors,
        cases=cases, practicalRule=dict(contrast='B/C only', maximumMedianPairedRatio=.95, minimumStrictWins=5,
            measuredBlocks=6, requiredCases=[c for c, n in CASES if n == 5000], **{'pass': practical_all}),
        qualification=audit.qualification_summaries, diagnosticIOIsRepeatedBenchmark=False,
        readings=audit.evidence.get('readings', []), cachePreparation=audit.evidence.get('cache', []),
        environmentStart=audit.evidence.get('environmentStart'), environmentEnd=audit.evidence.get('environmentEnd'),
        resources=audit.resources,
        observedCallPrefix=[{key: r.get(key) for key in ('sequence', 'workload', 'id', 'method', 'block', 'warmup', 'totalMs', 'reviewComplete')} for r in audit.calls],
        scope='Exposed fixed-pose CPU development workloads. A is diagnostic; O/P cached results are separate. No browser, flight, physical-validation, best-available implementation or independent-scenario claim.')


def run(audit):
    full = audit.package/'results/evidence.json'
    partial = audit.package/'results/partial-evidence.json'
    if full.is_file():
        audit.evidence = load_json(full)
    elif partial.is_file():
        audit.evidence = load_json(partial)
    else:
        audit.check(False, 'evidence.absent')
    audit.check(audit.evidence.get('complete') is True, 'evidence.complete')
    audit.check(not (audit.package/'results/failure.json').exists(), 'candidate.no-failure-record')
    constants = audit.evidence.get('constants', {})
    area, radius, arm, rho, mg = math.pi*.023*.023, .023, .028, 1.225, .027*9.81
    expected_constants = dict(mg=mg, arm=arm, radius=radius, rho=rho, A=area, R=math.sqrt(2)*arm)
    expected_c = dict(D=2*math.sqrt(2)*arm, decay=10.11, spread=.07668, origin=-5.817,
        minDown=2.5, neighbor=3, nearRad=.15, downFade=2, downCut=2.5, radFade=2, radCut=3,
        induced=math.sqrt(mg/(8*rho*area)), sqrt2minus1=math.sqrt(2)-1)
    for key, value in expected_constants.items():
        audit.close(constants.get(key), value, 'constants.'+key)
    for key, value in expected_c.items():
        audit.close(constants.get('c', {}).get(key), value, 'constants.c.'+key)
    for label, action in [('provenance-resources', provenance_resources), ('controls', controls_review),
                          ('qualification', qualification_review), ('timing', timing_review), ('other-records', other_records)]:
        try:
            audit.guard()
            action(audit)
        except Exception as error:
            audit.error(label+'.fatal-error', error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    package = args.package.resolve()
    analysis_path = package/'results/analysis.json'
    require(args.output.resolve() != analysis_path.resolve(), 'review output must differ from analysis.json')
    # Exclusive outputs preserve the once-only saved-record invocation.
    with args.output.open('x', encoding='utf-8') as output, analysis_path.open('x', encoding='utf-8') as analysis_output:
        audit = Audit(package)
        try:
            run(audit)
        except Exception as error:
            audit.error('review.fatal-error', error)
        try:
            analysis = build_analysis(audit)
        except Exception as error:
            audit.error('analysis.fatal-error', error)
            analysis = dict(kind='independent-saved-cost-analysis', complete=False, cases=[], practicalRule={'pass': None})
        coverage = {workload+('-warmup' if warmup else '-measured'): sum(r.get('workload') == workload and
                    r.get('warmup') is warmup and r.get('reviewComplete') for r in audit.calls)
                    for workload in ('full', 'cached') for warmup in (True, False)}
        result = dict(schema='m31-coupled-cost-saved-review-v1', **{'pass': not audit.errors and analysis['complete']},
            complete=analysis['complete'], checkCount=len(audit.checks), passedChecks=sum(c['pass'] for c in audit.checks),
            errors=audit.errors, checks=audit.checks, qualification=audit.qualification_summaries,
            controls=audit.control_summaries, coverage=coverage, resources=audit.resources,
            practicalRulePass=analysis['practicalRule']['pass'], analysisPath='results/analysis.json',
            elapsedSeconds=time.monotonic()-audit.started,
            limitations=['No geometry, field, root, solver or timing query was run by this reviewer.',
                'Timed transient arrays are not retained: repeat fingerprints and recorded comparison assertions do not independently reconstruct those arrays.',
                'Full JS JSON fingerprints are compared with qualified fingerprints, not reserialized in Python; qualification matrix binary bytes and numerical values are independently checked.',
                'Coefficient scaling and force-total consistency use saved K, nominal motor states and saved solutions only; no geometry or load map is recomputed.',
                'Clock records and hardware metadata are audited for internal consistency, not independently measured again.',
                'An unmet practical timing rule can coexist with a passing evidence audit.'])
        json.dump(safe_json(analysis), analysis_output, allow_nan=False, indent=2)
        analysis_output.write('\n')
        json.dump(safe_json(result), output, allow_nan=False, indent=2)
        output.write('\n')
    print(json.dumps({'pass': result['pass'], 'checkCount': result['checkCount'], 'errorCount': len(result['errors']),
                      'practicalRulePass': result['practicalRulePass']}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
