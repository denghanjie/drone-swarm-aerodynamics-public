"""Prospective standard-library saved-evidence auditor. No scientific imports.

Source preparation and AST parsing do not execute an allocation. Reconstructs
selection, normalized encoded-evidence equality and the candidate-list certificate;
never runs F/C, controllers, initialization, derivatives, RK or native solvers.
"""
from pathlib import Path, PurePosixPath
import datetime
import gzip
import hashlib
import io
import json
import math
import os
import re
import struct
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
REL = BASE.relative_to(ROOT).as_posix()
OLD = 'research/m31-paired-resolution-2026-10-21'
CANDIDATE = 'research/m31-buffered-candidates-2026-10-20/source/'
MAX_SECONDS = 1800
MAX_OUTPUT = 256*1024**2
MAX_INPUT = 768*1024**2
MAX_PART = 32*1024**2
MAX_RECORD = 4*1024**2
START = None
PINS, SOURCE_PINS, READ_EVENTS, CHECKS = {}, {}, [], []
OPERATION = 0
WORD = re.compile(r'^[0-9a-f]{16}$')
SHA = re.compile(r'^[0-9a-f]{64}$')
EXCLUSIONS = ['method', 'timing', 'diagnostics.buildPhasesMs',
    'diagnostics.geometryWork.gatheredNonselfCandidates', 'diagnostics.screen.orderedPairVisits',
    'diagnostics.screen.componentTests', 'caseId', 'semanticInputSha256', 'inlineInputCanonicalSha256']
CASE_IDS = ['seed2026102101-original-h0025', 'seed2026102101-memory-h0025',
            'seed2026102102-original-h0025', 'seed2026102102-memory-h0025']
TOTAL_STAGES = [5792, 8000, 8000, 8000]
EXPECTED_CONFIG = {'schema': 'm31-buffered-motion-config-v1', 'caseIds': CASE_IDS,
    'totalStages': TOTAL_STAGES, 'windowLength': 160, 'windowStarts': [0, 4000, 'last160'],
    'repetitions': list(range(-1, 8)), 'maxCalls': 34560, 'exclusions': EXCLUSIONS,
    'allocations': {'extract': {'seconds': 1200, 'mib': 768}, 'producer': {'seconds': 1800, 'mib': 768},
                    'audit': {'seconds': 1800, 'mib': 256}, 'finalize': {'seconds': 120, 'mib': 2},
                    'ui': {'seconds': 150, 'mib': 16}},
    'keepGate': {'medianAggregateRatioMaximum': .9, 'strictWinsMinimum': 7,
                 'reuseRequired': True, 'motionRebuildRequiredWorkloadWide': True}}
IMMUTABLE = {
    CANDIDATE+'candidate.cjs': '2e11acb60ad7ab447bc137e6ade56c24ef2b383444db7d46643648bd83cd807b',
    CANDIDATE+'candidate-kernel.cjs': '4fea99f4e61bff3c5eb54a0090e50b48e41d4cdf7cff5cdc770a37366f321b19',
    CANDIDATE+'candidate-cache.cjs': '9b38064690c2ae5b505cae936d574e3355bcc613b3f69fda8b89ed50732f96ad',
    'research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs':
    'b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1'}
LIMITS = dict(halfWidth=.125, absoluteCoordinateLimit=2**20,
              maxCandidateEntries=2000000, screenThreshold=4, outwardEndpointUlps=1)
COUNTERS = ['queries', 'builds', 'reuses', 'fallbacks', 'invalidations',
            'identityRebuilds', 'boxExitRebuilds', 'buildOrderedPairs',
            'buildAxisIntervalTests', 'containmentCoordinateTests']
SCOPE = 'fixed exposed N64 chopped-window native query cost, not full-flight cost or physical validation'


class AuditFailure(Exception):
    pass


def need(value, label):
    if not value:
        raise AuditFailure(label)


def tick():
    need(START is not None and time.monotonic()-START <= MAX_SECONDS, 'audit-wall-budget')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode()


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate-json-key:'+key)
        result[key] = value
    return result


def bad_constant(value):
    raise AuditFailure('nonfinite-json-number:'+value)


def json_float(value):
    result = float(value)
    need(math.isfinite(result), 'overflowing-json-number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=strict_pairs, parse_constant=bad_constant, parse_float=json_float)


def finite(value, nonnegative=False):
    need(type(value) in (int, float) and math.isfinite(value), 'finite-number')
    need(not nonnegative or value >= 0, 'nonnegative-number')
    return value


def integer(value, minimum, maximum, label):
    need(type(value) is int and minimum <= value <= maximum, label)
    return value


def word(value):
    return struct.pack('>d', float(value)).hex()


def number(value):
    need(type(value) is str and WORD.fullmatch(value), 'binary64-word')
    result = struct.unpack('>d', bytes.fromhex(value))[0]
    need(math.isfinite(result), 'finite-binary64-word')
    return result


def exact(left, right, label):
    """Deep equality preserving numeric sign bits and boolean distinctions."""
    if type(left) in (int, float) and type(right) in (int, float):
        need(word(finite(left)) == word(finite(right)), label)
    elif type(left) is dict and type(right) is dict:
        need(left.keys() == right.keys(), label+':keys')
        for key in left:
            exact(left[key], right[key], label)
    elif type(left) is list and type(right) is list:
        need(len(left) == len(right), label+':length')
        for a, b in zip(left, right):
            exact(a, b, label)
    else:
        need(type(left) is type(right) and left == right, label)


def safe_path(relative):
    need(type(relative) is str and relative and '\\' not in relative, 'path-format')
    parts = PurePosixPath(relative)
    need(not parts.is_absolute() and all(p not in ('', '.', '..') for p in relative.split('/')), 'unsafe-path')
    result = ROOT
    for part in parts.parts:
        result = result/part
        need(not result.is_symlink(), 'symlink:'+relative)
    need(result.is_file(), 'missing-file:'+relative)
    return result


def checked(relative, pin):
    """At most three identity reads; no bad bytes are exposed to a parser."""
    global OPERATION
    integer(pin['bytes'], 1, MAX_INPUT, 'pin-size')
    need(type(pin['sha256']) is str and SHA.fullmatch(pin['sha256']), 'pin-sha256')
    path = safe_path(relative)
    OPERATION += 1
    for attempt in range(1, 4):
        tick()
        try:
            with path.open('rb') as stream:
                raw = stream.read(pin['bytes']+1)
            if len(raw) == pin['bytes'] and digest(raw) == pin['sha256']:
                PINS[relative] = {'bytes': pin['bytes'], 'sha256': pin['sha256']}
                return raw
            event = {'kind': 'identity-mismatch', 'bytes': len(raw), 'sha256': digest(raw)}
        except OSError as error:
            event = {'kind': 'read-error', 'errno': error.errno}
        READ_EVENTS.append({'path': relative, 'operation': OPERATION, 'attempt': attempt, **event})
    raise AuditFailure('verified-read-exhausted:'+relative)


def capture(name, maximum=MAX_OUTPUT):
    relative = REL+'/'+name
    path = safe_path(relative)
    need(0 < path.stat().st_size <= maximum, 'capture-size')
    raw = path.read_bytes()
    need(0 < len(raw) <= maximum, 'capture-size')
    pin = {'bytes': len(raw), 'sha256': digest(raw)}
    PINS[relative] = pin
    return parse(raw), pin


def frozen(relative):
    need(relative in SOURCE_PINS, 'missing-source-pin:'+relative)
    return parse(checked(relative, SOURCE_PINS[relative]))


def normalization(value, path=''):
    if type(value) in (int, float):
        return word(finite(value))
    if type(value) is list:
        return [normalization(item, path+'[]') for item in value]
    if type(value) is dict:
        return {key: normalization(value[key], path+'.'+key if path else key)
                for key in sorted(value) if (path+'.'+key if path else key) not in EXCLUSIONS}
    need(value is None or type(value) in (str, bool), 'normalization-value')
    return value


def source_gate():
    manifest, manifest_pin = capture('source-manifest.json', MAX_RECORD)
    publication, publication_pin = capture('source-publication.json', MAX_RECORD)
    need(publication['manifestSha256'] == manifest_pin['sha256'], 'public-source-manifest')
    need(publication.get('remoteBytesEqualLocal') is True and publication.get('committedBytesEqualLocal') is True
         and publication.get('independentReviewPassed') is True, 'public-reviewed-source-required')
    need(type(publication.get('commit')) is str and re.fullmatch('[0-9a-f]{40}', publication['commit']), 'source-commit')
    for pin in manifest['files']:
        need(set(pin) == {'path', 'bytes', 'sha256'} and pin['path'] not in SOURCE_PINS, 'unique-source-pin')
        SOURCE_PINS[pin['path']] = pin
        if '.jsonl.gz.part' not in pin['path']:
            checked(pin['path'], pin)
    integer(publication.get('verifiedFilePins'), len(SOURCE_PINS), len(SOURCE_PINS), 'published-pin-count')
    for name in ('config.json', 'PROTOCOL.md', 'review/AUDIT-DESIGN.md', 'source/audit.py',
                 'source/run.cjs', 'source/extract.py', 'source/common.cjs', 'source/supervise.py',
                 'source/launch.py', 'runtime.json'):
        need(REL+'/'+name in SOURCE_PINS, 'mandatory-source:'+name)
    exact(frozen(REL+'/config.json'), EXPECTED_CONFIG, 'fixed-config')
    for relative, sha in IMMUTABLE.items():
        need(SOURCE_PINS.get(relative, {}).get('sha256') == sha, 'unchanged-candidate/native-source')
    queue, visited = [REL+'/source/run.cjs'], set()
    while queue:
        relative = queue.pop()
        if relative in visited:
            continue
        visited.add(relative)
        need(relative in SOURCE_PINS, 'unmanifested-dependency:'+relative)
        text = checked(relative, SOURCE_PINS[relative]).decode()
        for name in re.findall(r"require\(['\"]([^'\"]+)['\"]\)", text):
            if name.startswith('node:'):
                continue
            need(name.startswith('.'), 'nonlocal-or-unpinned-package-import')
            target = safe_path(relative).parent.joinpath(name).resolve()
            need(target.is_relative_to(ROOT), 'dependency-escape')
            queue.append(target.relative_to(ROOT).as_posix())
    need(set(IMMUTABLE) <= visited, 'candidate/native-dependency-closure')
    CHECKS.append('exact reviewed public source, fixed config and unchanged transitive candidate/native imports inspected as text')
    return publication, manifest_pin, publication_pin, sorted(visited)


def prior_gate():
    manifest_path = OLD+'/result-manifest.json'
    receipt_path = 'research/publication-receipts/m31-paired-resolution-result-2026-10-21.json'
    exact(SOURCE_PINS.get(manifest_path), {'path': manifest_path, 'bytes': 51543,
          'sha256': 'e54ba424f77676f0f04e7037e01d646b4d2e4c7b76acfe085a479cd4887cac44'}, 'fixed-prior-manifest')
    exact(SOURCE_PINS.get(receipt_path), {'path': receipt_path, 'bytes': 2002,
          'sha256': '04222b030249899253cfc47808c5643d43cc90f3e6d87c42c1332b59db9039fa'}, 'fixed-final-prior-receipt')
    manifest, receipt = frozen(manifest_path), frozen(receipt_path)
    need(manifest['schema'] == 'm31-paired-resolution-result-v1', 'prior-manifest-schema')
    public = {p['path']: p for p in manifest['files']}
    need(len(public) == len(manifest['files']) == 237, 'prior-pin-count')
    expected_receipt = {'commit': '7fae6ca51733a9bc9b6b2ada5156d05a7a64f747',
        'manifestPath': manifest_path, 'manifestBytes': 51543,
        'manifestSha256': SOURCE_PINS[manifest_path]['sha256'], 'verifiedFilePins': 237,
        'remoteBytesEqualLocal': True, 'committedBytesEqualLocal': True}
    for key, value in expected_receipt.items():
        exact(receipt.get(key), value, 'prior-publication-receipt')
    names = ['results/index.json', 'audit/audit.json', 'ALLOCATION-CLOSURE.json']
    old = {}
    for name in names:
        relative = OLD+'/'+name
        exact(SOURCE_PINS.get(relative), public.get(relative), 'prior-selected-pin')
        old[name] = frozen(relative)
    index, report, closure = old['results/index.json'], old['audit/audit.json'], old['ALLOCATION-CLOSURE.json']
    need(index.get('complete') is True and 'failure' not in index, 'old-producer-complete')
    need(report.get('passed') is True and report.get('evidenceIntegrityPassed') is True, 'old-evidence-passed')
    need(report['sourceCommit'] == index['sourceCommit'] == '08fc10c6fb3d38dc0e22b7f1aa595e8cb9a50848', 'old-source-commit')
    need(report['indexPin']['bytes'] == public[OLD+'/results/index.json']['bytes']
         and report['indexPin']['sha256'] == public[OLD+'/results/index.json']['sha256'], 'old-audit-index-binding')
    need(closure['schema'] == 'm31-paired-resolution-closure-v1' and closure['allAllocationsClosed'] is True, 'old-closed')
    for phase in ('producer', 'audit', 'finalize', 'ui'):
        need(closure['phases'][phase]['status'] == 'closed-passed' and closure['phases'][phase]['attempts'] == 1, 'old-phase-closed')
    need([c['caseId'] for c in index['cases']] == CASE_IDS and [c['attemptedStages'] for c in index['cases']] == TOTAL_STAGES, 'old-fixed-four-paths')
    need(index['totalNativeCalls'] == index['totalStages'] == closure['nativeQueries'] == 29792, 'old-stage-total')
    journals = [s['journal'] for c in index['cases'] for s in c['segments']]
    exact(report['journalPins'], journals, 'old-audited-journal-descriptors')
    part_count = 0
    for c in index['cases']:
        need(c['dt'] == .0025 and c['stepsPerControl'] == 4 and len(c['segments']) == 2, 'old-fine-path-configuration')
        for segment in c['segments']:
            descriptor = segment['journal']
            need(descriptor['file'] == c['caseId']+'-s'+str(segment['segment'])+'.jsonl.gz', 'old-journal-name')
            offset = 0
            for j, part in enumerate(descriptor['parts']):
                need(part['file'] == descriptor['file']+'.part'+str(j).zfill(3) and part['offset'] == offset, 'old-part-order')
                integer(part['bytes'], 1, MAX_PART, 'old-part-cap')
                relative = OLD+'/results/'+part['file']
                expected = {'path': relative, 'bytes': part['bytes'], 'sha256': part['sha256']}
                exact(SOURCE_PINS.get(relative), expected, 'old-part-source-pin')
                exact(public.get(relative), expected, 'old-part-public-pin')
                offset += part['bytes']; part_count += 1
            need(offset == descriptor['bytes'], 'old-compressed-total')
    need(len(journals) == 8 and part_count == 93, 'old-journal-part-count')
    CHECKS.append('published closed paired-resolution comparator and all 93 source-part identities bound before independent scan')
    return index, {'resultCommit': receipt['commit'], 'manifestPin': SOURCE_PINS[manifest_path],
                   'receiptPin': SOURCE_PINS[receipt_path], 'sourcePartCount': part_count,
                   'oldTrajectoryArithmeticReaudited': False}


def closure_gate(phase):
    folder = 'results' if phase == 'producer' else phase
    supervisor, _ = capture(phase+'-supervisor.json', MAX_RECORD)
    closed, _ = capture(folder+'/exit.json', MAX_RECORD)
    limit = EXPECTED_CONFIG['allocations'][phase]
    need(supervisor.get('closed') is True and supervisor.get('returncode') == 0 and not supervisor.get('timeout')
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True,
         'closed-supervised-'+phase)
    need(0 <= finite(supervisor['wallSeconds']) <= limit['seconds'], 'supervisor-wall-'+phase)
    need(closed.get('closed') is True and closed.get('exitCode') == 0, 'closed-internal-'+phase)
    need(0 <= finite(closed['wallSeconds']) <= limit['seconds'], 'internal-wall-'+phase)
    need(not (BASE/folder/'failure.json').exists(), 'failed-'+phase)
    files = list((BASE/folder).iterdir())
    need(all(p.is_file() and not p.is_symlink() for p in files), 'regular-closed-output-'+phase)
    actual_bytes = sum(p.stat().st_size for p in files)
    need(actual_bytes == supervisor['outputBytes'] <= limit['mib']*1024**2, 'closed-output-byte-account-'+phase)
    return closed


class Parts(io.RawIOBase):
    def __init__(self, descriptor):
        super().__init__()
        self.descriptor, self.index, self.buffer, self.at = descriptor, 0, b'', 0
        self.count, self.hash, self.finished = 0, hashlib.sha256(), False

    def readable(self):
        return True

    def readinto(self, target):
        tick()
        if not target:
            return 0
        if self.at == len(self.buffer):
            if self.index == len(self.descriptor['parts']):
                need(self.count == self.descriptor['bytes'] and self.hash.hexdigest() == self.descriptor['sha256'], 'source-compressed-identity')
                self.finished = True
                return 0
            part = self.descriptor['parts'][self.index]
            need(part['offset'] == self.count, 'source-compressed-offset')
            self.buffer = checked(OLD+'/results/'+part['file'], part)
            self.count += len(self.buffer); self.hash.update(self.buffer)
            self.at = 0; self.index += 1
        count = min(len(target), len(self.buffer)-self.at)
        target[:count] = self.buffer[self.at:self.at+count]
        self.at += count
        return count


def bounded_line(stream, label):
    tick()
    line = stream.readline(MAX_RECORD+1)
    need(0 < len(line) <= MAX_RECORD and line.endswith(b'\n'), label+'-record-bound')
    return line


def input_check(value):
    need(type(value) is dict and set(value) == {'drones'} and len(value['drones']) == 64, 'selected-input-shape')
    for ident, row in enumerate(value['drones']):
        need(type(row) is dict and set(row) == {'id', 'state'}, 'selected-input-row')
        integer(row['id'], ident, ident, 'selected-canonical-id')
        need(len(row['state']) == 17, 'selected-state-width')
        for v in row['state']:
            number(v)
        need(all(number(v) > 0 for v in row['state'][13:]), 'selected-positive-motor-states')


def reference_check(body, case, segment, local):
    step, stage = local//4, local%4+1
    need(body['schema'] == 'm31-coupled-stage-v1' and body['arm'] == 'coupled', 'selected-stage-schema')
    need(body['stepIndex'] == step and body['stageIndex'] == stage, 'selected-stage-index')
    need(body['stageId'] == 'coupled-step'+str(step)+'-k'+str(stage), 'selected-stage-id')
    dt = case['dt']
    t = step*dt+(0 if stage == 1 else dt if stage == 4 else dt/2)
    need(body['relativeTimeWord'] == word(t) and body['originalTimeWord'] == word(segment['timeOrigin']+t)
         and body['dtWord'] == word(dt), 'selected-stage-own-time')
    input_check(body['nativeInput'])
    native = body['native']
    need(native['schema'] == 'm31-native-load-evidence-v1' and native['model'] == 'ordinary-binary64-full-contribution'
         and native['method'] == 'F', 'selected-encoded-native-model')
    h = digest(compact(body['nativeInput']))
    need(native['caseId'] == body['stageId'] and native['semanticInputSha256'] == h
         and native['inlineInputCanonicalSha256'] == h, 'archived-adapter-annotation-binding')
    need(native['ids'] == list(range(64)), 'selected-native-ids')
    exact(native['raw'], body['nativeInput']['drones'], 'selected-native-raw-input')
    need(native['status'] in ('native-success', 'domain-refused'), 'fixed-selected-status-domain')
    if native['status'] == 'native-success':
        need(body['status'] == 'completed' and native['reason'] is None, 'selected-success-status')
        need(all(len(native[k]) == 64 for k in ('prepared', 'solution', 'loads')), 'selected-success-complete-evidence')
    else:
        need(body['status'] == 'failed' and body['reason'] == 'native-non-success'
             and native['reason'] == 'native-admission' and native['stage'] == 'build', 'selected-recorded-refusal')
        need(native['diagnostics']['admission']['admitted'] is False
             and native['diagnostics']['admission']['reasons'] == ['near-field'], 'selected-refusal-admission')
        need(not any(k in native for k in ('loads', 'solution', 'consumption')), 'refusal-nonconsumable')
    return h


def cas_pin(value, kind):
    need(type(value) is dict and set(value) == {'file', 'bytes', 'sha256'}, 'CAS-pin-fields')
    need(type(value['sha256']) is str and SHA.fullmatch(value['sha256'])
         and value['file'] == kind+'-'+value['sha256']+'.json', 'CAS-name')
    integer(value['bytes'], 1, MAX_RECORD, 'CAS-size')
    return REL+'/results/'+value['file']


def selection_audit(old_index, extraction, binding, references):
    windows = [{'window': ci*3+wi, 'caseId': case, 'start': start, 'length': 160}
               for ci, case in enumerate(CASE_IDS) for wi, start in enumerate((0, 4000, TOTAL_STAGES[ci]-160))]
    exact(extraction['windows'], windows, 'fixed-window-table')
    need(extraction['complete'] is True and extraction['selected'] == 1920 and extraction['nativeQueries'] == 0, 'closed-extraction-counts')
    exact(binding['selectedPin'], extraction['selectedPin'], 'producer-selected-pin-binding')
    pin = extraction['selectedPin']
    need(pin['file'] == 'selected.jsonl.gz', 'selected-stream-name')
    zipped = checked(REL+'/extract/'+pin['file'], pin)
    refs = {}
    need(type(references) is list and len(references) == 1920, 'reference-count')
    for pos, ref in enumerate(references):
        need(set(ref) == {'window', 'index', 'semantic'} and (ref['window'], ref['index']) == (pos//160, pos%160), 'reference-order')
        cas_pin(ref['semantic'], 'semantic')
        refs[pos//160, pos%160] = ref['semantic']
    selected, sources, refusals = {}, [], []
    with gzip.GzipFile(fileobj=io.BytesIO(zipped), mode='rb') as chosen:
        for ci, case in enumerate(old_index['cases']):
            global_ordinal = 0
            for seg in case['segments']:
                descriptor = seg['journal']; parts = Parts(descriptor)
                count, raw_bytes, raw_hash, local = 0, 0, hashlib.sha256(), 0
                with io.BufferedReader(parts) as stream, gzip.GzipFile(fileobj=stream, mode='rb') as gz:
                    for sequence in range(descriptor['records']):
                        line = bounded_line(gz, 'source'); offset = raw_bytes
                        raw_bytes += len(line); raw_hash.update(line)
                        need(raw_bytes <= descriptor['rawBytes'], 'source-raw-byte-budget')
                        record = parse(line)
                        need(type(record) is dict and set(record) == {'sequence', 'kind', 'body'}
                             and type(record['sequence']) is int and record['sequence'] == sequence, 'source-envelope-sequence')
                        count += 1
                        if record['kind'] != 'stage':
                            continue
                        for w in windows[ci*3:ci*3+3]:
                            if w['start'] <= global_ordinal < w['start']+160:
                                index = global_ordinal-w['start']
                                saved = parse(bounded_line(chosen, 'selected'))
                                expected = {'window': w['window'], 'index': index, 'caseId': case['caseId'],
                                    'globalOrdinal': global_ordinal, 'segment': seg['segment'], 'localStageOrdinal': local,
                                    'rawOffset': offset, 'sourceLineSha256': digest(line), 'sourceLineBytes': len(line), 'record': record}
                                exact(saved, expected, 'independent-selected-full-record-provenance')
                                body = record['body']; input_hash = reference_check(body, case, seg, local)
                                reference = refs[w['window'], index]
                                semantic = compact(normalization(body['native']))+b'\n'
                                need(len(semantic) == reference['bytes'] and digest(semantic) == reference['sha256'], 'independent-reference-normalization')
                                need(checked(cas_pin(reference, 'semantic'), reference) == semantic, 'full-reference-canonical-bytes')
                                diag = body['native']['diagnostics']
                                selected[w['window'], index] = {'input': body['nativeInput'], 'inputHash': input_hash,
                                    'reference': reference, 'status': body['native']['status'], 'reason': body['native']['reason'],
                                    'time': number(body['originalTimeWord']), 'timeWord': body['originalTimeWord'],
                                    'globalOrdinal': global_ordinal, 'segment': seg['segment'], 'stageIndex': body['stageIndex'],
                                    'sourceLineSha256': digest(line), 'sourceLineBytes': len(line), 'rawOffset': offset,
                                    'sourceSequence': sequence, 'screenEligible': diag['screen']['eligible'],
                                    'hasBuildPhases': 'buildPhasesMs' in diag}
                                if body['native']['status'] != 'native-success':
                                    refusals.append({'window': w['window'], 'index': index, 'status': body['native']['status'],
                                        'reason': body['native']['reason'], 'originalTimeWord': body['originalTimeWord']})
                        local += 1; global_ordinal += 1
                    need(gz.read(1) == b'' and parts.finished, 'complete-source-gzip')
                need(raw_bytes == descriptor['rawBytes'] and raw_hash.hexdigest() == descriptor['rawSha256'], 'source-raw-identity')
                need(local == seg['attemptedStages'], 'source-segment-stage-count')
                sources.append({'caseId': case['caseId'], 'segment': seg['segment'], 'parts': descriptor['parts'],
                    'records': count, 'stages': local, 'rawBytes': raw_bytes, 'rawSha256': raw_hash.hexdigest()})
            need(global_ordinal == case['attemptedStages'], 'source-path-stage-count')
        need(chosen.read(1) == b'', 'no-extra-selected-records')
    need(len(selected) == 1920 and len(refusals) == 1 and refusals[0]['window'] == 2 and refusals[0]['index'] == 159, 'selected-refusal-coverage')
    exact(extraction['sources'], sources, 'extraction-source-scan-binding')
    exact(extraction['refusals'], refusals, 'extraction-refusal-binding')
    CHECKS.append('all 93 verified parts rescanned, raw/compressed identities reconciled, all 1920 complete selected records and exact normalized encoded references independently bound')
    return windows, selected, refusals


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


def witness_check(value, state, current):
    cache = state['cached']
    keys = {'schema', 'cached', 'ids', 'boxes', 'rows', 'entries', 'last', 'boxEncoding'} | ({'boxLayout'} if cache else set())
    need(set(value) == keys and value['schema'] == 'm31-buffered-candidate-witness-v1'
         and value['boxEncoding'] == 'binary64-be-hex', 'full-witness-schema')
    need(value['cached'] is (cache is not None), 'witness-cache-presence')
    exact(value['last'], state['last'], 'witness-last-event')
    if cache is None:
        need(value['ids'] == value['boxes'] == value['rows'] == [] and value['entries'] == 0, 'empty-fallback-witness')
        return 0
    need(value['boxLayout'] == 'six words per canonical ID: xLo,xHi,yLo,yHi,zLo,zHi', 'witness-box-layout')
    exact(value['ids'], cache['ids'], 'witness-canonical-ids')
    need(value['boxes'] == [word(x) for x in cache['boxes']], 'exact-outward-binary64-box-words')
    exact(value['rows'], cache['rows'], 'exact-complete-ordered-candidate-rows')
    integer(value['entries'], cache['entries'], cache['entries'], 'witness-entry-count')
    centers = [[number(v) for v in d['state'][:3]] for d in current['drones']]
    boxes, ids, omitted = cache['boxes'], cache['ids'], 0
    for i, receiver in enumerate(centers):
        tick()
        need(all(boxes[6*i+2*k] <= receiver[k] <= boxes[6*i+2*k+1] for k in range(3)), 'witness-current-containment')
        row = set(cache['rows'][i])
        for j, source in enumerate(centers):
            if i == j or ids[j] in row:
                continue
            omitted += 1
            need(any(boxes[6*j+2*k]-boxes[6*i+2*k+1] >= 4 or boxes[6*j+2*k+1]-boxes[6*i+2*k] <= -4
                     for k in range(3)), 'omitted-pair-interval-certificate')
            need(any(abs(source[k]-receiver[k]) >= 4 for k in range(3)), 'omitted-pair-current-component-screen')
    return omitted


def excluded_check(row, item, state):
    ex = row['excluded']
    keys = {'method', 'timing', 'diagnostics.geometryWork.gatheredNonselfCandidates',
            'diagnostics.screen.orderedPairVisits', 'diagnostics.screen.componentTests'}
    if item['hasBuildPhases']:
        keys.add('diagnostics.buildPhasesMs')
    need(set(ex) == keys and ex['method'] == 'F', 'exact-new-evidence-exclusion-fields')
    timing = ex['timing']
    need(set(timing) == {'clock', 'totalMs', 'phasesMs', 'boundary'} and timing['clock'] == 'performance.now', 'native-timing-schema')
    need('complete load-word/ID/status consumption' in timing['boundary'], 'native-timing-consumption-boundary')
    need(0 <= finite(timing['totalMs']) <= row['outerMs'], 'nested-query-timing')
    phase_sum = 0.0
    for value in timing['phasesMs'].values():
        phase_sum += finite(value, True)
    need(abs(phase_sum-timing['totalMs']) <= max(1e-6, timing['totalMs']*1e-12), 'native-phase-telescope')
    if item['hasBuildPhases']:
        for value in ex['diagnostics.buildPhasesMs'].values():
            finite(value, True)
    gathered = 64*63 if state is None or state['cached'] is None else state['cached']['entries']
    for key in ('diagnostics.geometryWork.gatheredNonselfCandidates', 'diagnostics.screen.orderedPairVisits'):
        integer(ex[key], gathered, gathered, 'enumeration-work-current-candidate-count')
    component = gathered if item['screenEligible'] else 0
    integer(ex['diagnostics.screen.componentTests'], component, component, 'current-component-work')


def jsonl_capture(name):
    relative = REL+'/'+name
    path = safe_path(relative)
    need(0 < path.stat().st_size <= MAX_INPUT, 'JSONL-size')
    # Identity capture is one read pass, with bounded lines; no uncaptured retry.
    h, count = hashlib.sha256(), 0
    with path.open('rb') as stream:
        while True:
            tick()
            chunk = stream.read(1024*1024)
            if not chunk:
                break
            count += len(chunk); h.update(chunk)
            need(count <= MAX_INPUT, 'JSONL-byte-cap')
    PINS[relative] = {'bytes': count, 'sha256': h.hexdigest()}
    return path


def line_records(path):
    with path.open('rb') as stream:
        while True:
            tick()
            line = stream.readline(MAX_RECORD+1)
            if not line:
                break
            need(len(line) <= MAX_RECORD and line.endswith(b'\n'), 'JSONL-complete-bounded-line')
            yield parse(line)


def query_audit(windows, items, saved_groups, saved_summary):
    need(type(saved_groups) is list and len(saved_groups) == 108, '108-complete-window-groups')
    path = jsonl_capture('results/queries.jsonl')
    queries = iter(line_records(path))
    call = 0
    groups, views = [], [{**w, 'frames': [], 'ratios': []} for w in windows]
    coverage = {'builds': 0, 'reuses': 0, 'boxExitRebuilds': 0, 'fallbacks': 0}
    witnesses, witness_refs = {}, {}
    counts = {'queries': 0, 'candidateWitnesses': 0, 'referenceComparisons': 0,
              'admittedQueries': 0, 'refusedQueries': 0, 'omittedCurrentPairsChecked': 0,
              'cacheStepsIndependentlyReconstructed': 0, 'warmupQueries': 0, 'measuredQueries': 0}
    row_keys = {'call', 'window', 'rep', 'method', 'index', 'semantic', 'referenceSha256',
        'referenceEqual', 'comparisonMs', 'inputBeforeSha256', 'inputAfterSha256', 'inputPreserved',
        'outerMs', 'status', 'reason', 'cache', 'witness', 'excluded', 'encodePersistMs', 'methodValid', 'afterInput'}
    for rep in range(-1, 8):
        for window in range(12):
            order = ['F', 'C'] if (rep+window+10) % 2 == 0 else ['C', 'F']
            saved_group = saved_groups[(rep+1)*12+window]
            need(set(saved_group) == {'window', 'rep', 'order', 'F', 'C', 'ratio'}, 'group-fields')
            need(saved_group['window'] == window and saved_group['rep'] == rep and saved_group['order'] == order, 'group-schedule')
            group = {'window': window, 'rep': rep, 'order': order}
            for method in order:
                reset_ms = finite(saved_group[method]['resetMs'], True)
                aggregate = {'resetMs': reset_ms, 'sumQueryMs': 0.0, 'totalMs': reset_ms,
                             'admittedMs': 0.0, 'refusedMs': 0.0, 'admittedCalls': 0, 'refusedCalls': 0}
                state = fresh_cache() if method == 'C' else None
                for index in range(160):
                    tick(); call += 1
                    row = next(queries, None)
                    need(type(row) is dict and set(row) == row_keys, 'query-row-schema')
                    exact([row[k] for k in ('call', 'window', 'rep', 'method', 'index')],
                          [call, window, rep, method, index], 'complete-query-schedule')
                    item = items[window, index]
                    exact(row['semantic'], item['reference'], 'each-call-full-reference-CAS-pin')
                    need(row['referenceEqual'] is True and row['referenceSha256'] == item['reference']['sha256'], 'each-call-reference-comparison')
                    need(row['methodValid'] is True and row['afterInput'] is None, 'saved-valid-method-and-unmutated-input')
                    need(row['inputPreserved'] is True and row['inputBeforeSha256'] == row['inputAfterSha256'] == item['inputHash'], 'each-call-exact-input-binding')
                    need(row['status'] == item['status'] and row['reason'] == item['reason'], 'each-call-recorded-outcome')
                    finite(row['outerMs'], True); finite(row['encodePersistMs'], True); finite(row['comparisonMs'], True)
                    need(row['comparisonMs'] <= row['encodePersistMs'], 'comparison-within-encoding-overhead')
                    if method == 'C':
                        # The selected refusal is at build/admission, after enumeration.
                        # It therefore advances cache state exactly like other selected inputs.
                        cache_step(state, item['input'])
                        exact(row['cache'], expected_stats(state), 'every-candidate-cache-state-and-counter')
                        ref = row['witness']; relative = cas_pin(ref, 'witness')
                        if ref['sha256'] not in witnesses:
                            raw = checked(relative, ref)
                            witnesses[ref['sha256']] = parse(raw)
                            witness_refs[ref['sha256']] = dict(ref)
                        else:
                            exact(ref, witness_refs[ref['sha256']], 'deduplicated-witness-pin')
                        counts['omittedCurrentPairsChecked'] += witness_check(witnesses[ref['sha256']], state, item['input'])
                        counts['candidateWitnesses'] += 1
                        counts['cacheStepsIndependentlyReconstructed'] += 1
                        if rep >= 0:
                            action = state['last']['action']
                            coverage['builds'] += action == 'build'; coverage['reuses'] += action == 'reuse'
                            coverage['boxExitRebuilds'] += action == 'build' and state['last']['reason'] == 'box-exit'
                            coverage['fallbacks'] += action == 'fallback'
                        if rep == 0:
                            views[window]['frames'].append({'index': index, 'globalOrdinal': item['globalOrdinal'],
                                'time': item['time'], 'timeWord': item['timeWord'], 'status': item['status'], 'reason': item['reason'],
                                'positions': [[number(x) for x in drone['state'][:3]] for drone in item['input']['drones']],
                                'cache': row['cache'], 'segment': item['segment'], 'stageIndex': item['stageIndex'],
                                'sourceLineSha256': item['sourceLineSha256'], 'sourceLineBytes': item['sourceLineBytes'],
                                'sourceSequence': item['sourceSequence'], 'rawOffset': item['rawOffset'],
                                'kind': 'recorded-attempted-RK-stage-input', 'completedEndpoint': False})
                    else:
                        need(row['cache'] is None and row['witness'] is None, 'baseline-has-no-candidate-witness')
                    excluded_check(row, item, state)
                    aggregate['sumQueryMs'] += row['outerMs']
                    aggregate['totalMs'] += row['outerMs']
                    admitted = row['status'] == 'native-success'
                    aggregate['admittedMs' if admitted else 'refusedMs'] += row['outerMs']
                    aggregate['admittedCalls' if admitted else 'refusedCalls'] += 1
                    counts['admittedQueries' if admitted else 'refusedQueries'] += 1
                    counts['warmupQueries' if rep == -1 else 'measuredQueries'] += 1
                    counts['referenceComparisons'] += 1; counts['queries'] += 1
                need(aggregate['totalMs'] > 0, 'positive-stream-duration')
                exact(saved_group[method], aggregate, 'reset-inclusive-and-status-partition-timing')
                group[method] = aggregate
            group['ratio'] = group['C']['totalMs']/group['F']['totalMs']
            exact(saved_group, group, 'complete-group-arithmetic')
            groups.append(group)
            if rep >= 0:
                views[window]['ratios'].append(group['ratio'])
    need(next(queries, None) is None and call == 34560, 'no-missing-or-extra-query')
    need(counts['admittedQueries'] == 34542 and counts['refusedQueries'] == 18
         and counts['warmupQueries'] == 3840 and counts['measuredQueries'] == 30720
         and counts['candidateWitnesses'] == 17280, 'full-outcome-and-phase-accounting')
    reps = []
    for rep in range(8):
        f, c = 0.0, 0.0
        for group in groups:
            if group['rep'] == rep:
                f += group['F']['totalMs']; c += group['C']['totalMs']
        reps.append({'rep': rep, 'F': f, 'C': c, 'ratio': c/f})
    ratios = sorted(r['ratio'] for r in reps)
    median = (ratios[3]+ratios[4])/2
    wins = sum(r['C'] < r['F'] for r in reps)
    coverage_gate = coverage['reuses'] > 0 and coverage['boxExitRebuilds'] > 0
    cost_gate = median <= .9 and wins >= 7
    summary = {'complete': True, 'calls': call, 'referenceEquality': True, 'reps': reps,
               'medianRatio': median, 'strictWins': wins, 'coverage': coverage,
               'coverageGate': coverage_gate, 'costGate': cost_gate, 'keepGate': cost_gate and coverage_gate, 'scope': SCOPE}
    need(set(saved_summary) == set(summary) | {'readEvents', 'wallSeconds'}, 'summary-full-fields')
    exact({k: saved_summary[k] for k in summary}, summary, 'independent-summary-and-keep-decision')
    need(type(saved_summary['readEvents']) is list and 0 <= finite(saved_summary['wallSeconds']) <= 1800, 'producer-summary-budget-anomalies')
    summary.update({'readEvents': saved_summary['readEvents'], 'wallSeconds': saved_summary['wallSeconds']})
    CHECKS.append('all 34560 query/reference matches, 17280 reconstructed cache steps and witnesses, omitted-current pairs, balanced reset schedule and status-preserving timing sums')
    CHECKS.append('all 108 group totals, 96 measured window ratios, eight aggregate ratios/median/strict wins and prespecified cost plus motion-coverage gate independently reconstructed')
    return summary, views, counts, witness_refs, groups


def inventory(extraction, producer_exit, items, witness_refs):
    expected = {'launch.lock', 'input-binding.json', 'environment.json', 'references.json',
                'queries.jsonl', 'groups.jsonl', 'summary.json', 'exit.json'}
    expected.update(item['reference']['file'] for item in items.values())
    expected.update(ref['file'] for ref in witness_refs.values())
    files = list((BASE/'results').iterdir())
    need({p.name for p in files} == expected, 'exact-producer-output-inventory')
    total, before_exit = 0, 0
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if relative not in PINS:
            need(path.name == 'launch.lock', 'unverified-produced-file')
            raw = path.read_bytes()
            need(raw == b'single bounded native replay\n', 'producer-launch-record')
            PINS[relative] = {'bytes': len(raw), 'sha256': digest(raw)}
        total += PINS[relative]['bytes']
        if path.name != 'exit.json':
            before_exit += PINS[relative]['bytes']
    need(total <= MAX_INPUT and producer_exit['bytesWritten'] == before_exit, 'producer-exact-payload-accounting')
    need({p.name for p in (BASE/'extract').iterdir()} == {'launch.lock', 'selected.jsonl.gz', 'index.json', 'exit.json'}, 'exact-extraction-inventory')
    raw = safe_path(REL+'/extract/launch.lock').read_bytes()
    need(raw == b'single bounded extraction; no native queries\n', 'extraction-launch-record')
    PINS[REL+'/extract/launch.lock'] = {'bytes': len(raw), 'sha256': digest(raw)}
    CHECKS.append('closed result/extraction inventories and exact producer pre-exit byte accounting; all artifact and source identities rechecked before report')
    return total


def audit():
    publication, manifest_pin, publication_pin, dependencies = source_gate()
    old_index, source_evidence = prior_gate()
    extraction_exit = closure_gate('extract')
    producer_exit = closure_gate('producer')
    extraction, extraction_pin = capture('extract/index.json')
    binding, _ = capture('results/input-binding.json', MAX_RECORD)
    environment, _ = capture('results/environment.json', MAX_RECORD)
    references, _ = capture('results/references.json')
    saved_summary, _ = capture('results/summary.json', MAX_RECORD)
    group_path = jsonl_capture('results/groups.jsonl')
    saved_groups = list(line_records(group_path))
    exact(binding['extractionIndex'], extraction_pin, 'producer-extraction-index-identity')
    need(binding['sourceCommit'] == environment['sourceCommit'] == publication['commit']
         and binding['manifestSha256'] == manifest_pin['sha256'], 'producer-source-publication-binding')
    runtime = frozen(REL+'/runtime.json')
    need(environment['node'] == runtime['nodeVersion'], 'producer-runtime-version')
    need(producer_exit['calls'] == 34560 and producer_exit['readEvents'] == saved_summary['readEvents'], 'producer-closed-query-anomaly-accounting')
    need(extraction_exit['readEvents'] == extraction['readEvents'], 'extraction-closed-anomalies')
    windows, items, selected_refusals = selection_audit(old_index, extraction, binding, references)
    summary, views, counts, witnesses, groups = query_audit(windows, items, saved_groups, saved_summary)
    output_bytes = inventory(extraction, producer_exit, items, witnesses)
    # Includes all 93 source parts: identity only, without a second raw scan.
    for relative, pin in list(PINS.items()):
        checked(relative, pin)
    tick()
    viewer = {'schema': 'm31-buffered-motion-view-v1', 'windows': views, 'summary': summary,
              'groups': groups, 'sourceCommit': publication['commit'],
              'scope': 'recorded attempted RK-stage input samples, including refused trial; no candidate integrated trajectory',
              'completedEndpoints': False, 'physicalValidity': False}
    report = {'schema': 'm31-buffered-motion-audit-v1', 'passed': True,
              'evidenceIntegrityPassed': True, 'exactReferenceEquivalence': True,
              'candidateCertificatePassed': True, 'checks': CHECKS, 'summary': summary,
              'sourceCommit': publication['commit'], 'sourceManifestPin': manifest_pin,
              'sourcePublicationPin': publication_pin, 'sourceEvidence': source_evidence,
              'extractionIndexPin': extraction_pin, 'selectedRefusals': selected_refusals,
              'counts': counts, 'selectedStages': 1920, 'sourcePartsScanned': 93,
              'sourceJournalsScanned': 8, 'sourceRawRecordsScanned': 46564,
              'sourceTrajectoryArithmeticReaudited': False, 'newNativeQueriesByAudit': 0,
              'newNumericalProducerCallsByAudit': 0, 'producerOutputBytes': output_bytes,
              'staticDependencyClosure': dependencies, 'filePins': PINS,
              'readEvents': READ_EVENTS, 'extractionReadEvents': extraction['readEvents'],
              'producerReadEvents': saved_summary['readEvents'],
              'normalizationExclusions': EXCLUSIONS,
              'normalizationScope': 'all comparands encoded evidence-v1; exact sorted-key binary64 canonical bytes; method and archived adapter bindings separately validated',
              'certificateScope': 'independently reconstructed canonical candidate rows, outward box words, every reset/cache counter and every omitted current pair for every candidate query',
              'notRecomputed': ['initializer', 'controllers', 'quaternion projection', 'derivatives', 'RK integration',
                               'contact geometry', 'native geometry coefficients', 'native root solve', 'native residual model'],
              'branchCoverageScope': 'only recorded N64 inputs and observed cache events; no fresh synthetic controls or unobserved fallback/identity/resource branches qualified',
              'timingScope': 'same-process instrumented chopped-window replay; reset and query inside primary total, encoding/comparison/persistence outside but may influence runtime',
              'implementationDisclosure': 'standard-library-only audit; cache transition helpers adapted textually from prior independent candidate audit; no old audit or scientific module imported',
              'physicalValidity': False, 'flightSafetyClaim': False, 'statisticalInference': False,
              'largeSwarmSpeedClaim': False, 'researchComplete': False}
    return report, viewer


def main():
    global START
    START = time.monotonic()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'optimized-audit-not-permitted')
    need((BASE/'audit-supervisor-launch.lock').is_file(), 'audit-supervisor-allocation-required')
    out = BASE/'audit'
    need(not out.is_symlink(), 'audit-output-symlink')
    out.mkdir()
    def save(name, value):
        raw = compact(value)+b'\n'
        need(sum(p.stat().st_size for p in out.iterdir())+len(raw)+16384 <= MAX_OUTPUT, 'audit-output-budget')
        with (out/name).open('xb') as stream:
            stream.write(raw)
    save('launch.json', {'schema': 'm31-buffered-motion-audit-launch-v1',
        'startedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'python': sys.version,
        'maxWallSeconds': MAX_SECONDS, 'maxOutputBytes': MAX_OUTPUT, 'scope': 'saved evidence only; no native/model calls'})
    code = 0
    try:
        report, viewer = audit()
        raw = compact(viewer)+b'\n'
        report['viewerPin'] = {'file': 'viewer-data.json', 'bytes': len(raw), 'sha256': digest(raw)}
        report['wallSeconds'] = time.monotonic()-START
        need(len(raw)+len(compact(report))+32768 <= MAX_OUTPUT, 'combined-audit-output-budget')
        save('viewer-data.json', viewer); tick(); save('audit.json', report); tick()
    except Exception as error:
        code = 1
        name = 'failure.json' if (out/'audit.json').exists() else 'audit.json'
        save(name, {'schema': 'm31-buffered-motion-audit-v1', 'passed': False, 'evidenceIntegrityPassed': False,
            'allocation': 'closed-no-rerun', 'failure': type(error).__name__+': '+str(error).replace(str(ROOT), '[repository]')[:1500],
            'checksCompleted': CHECKS, 'readEvents': READ_EVENTS, 'wallSeconds': time.monotonic()-START})
    save('exit.json', {'closed': True, 'exitCode': code, 'wallSeconds': time.monotonic()-START})
    return code


if __name__ == '__main__':
    sys.exit(main())
