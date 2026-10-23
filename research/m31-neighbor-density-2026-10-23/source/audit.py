"""Independent saved-record density auditor; no scientific imports or queries.

Execution belongs only to the separately frozen, supervised audit allocation.
This file is source preparation until that public gate and allocation exist.
"""
from pathlib import Path
import datetime
import gzip
import hashlib
import io
import json
import math
import os
import re
import selectors
import struct
import subprocess
import sys
import time


BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
REL = 'research/m31-neighbor-density-2026-10-23'
OLD = 'research/m31-buffered-motion-2026-10-22'
INPUT_COMMIT = '0461153a7d6f75cb6e8564850b77e8b6f04cebb2'
MAX_SECONDS = 1200
MAX_OUTPUT = 4*1024**2
MAX_RESULT = 32*1024**2
MAX_METADATA = 16*1024**2
MAX_RECORD = 8*1024**2
MAX_PART = 32*1024**2
START = None
READ_EVENTS = []
CHECKS = []
SOURCE_PINS = {}
CONSUMED_PINS = {}
COMMITTED = {}
INPUT_PINS = {}
COUNTS_KEYS = ['logicalPairs', 'componentSurvivors', 'componentRejected', 'guardRejected',
               'radialRejected', 'centerEligible', 'rotorCalls', 'positiveRotorTerms',
               'positiveVehicleEdges', 'supportedZeroRotorTerms', 'unsupportedNearFieldRotorTerms',
               'invalidRotorTerms']
SCOPE = 'saved exposed N64 builder counts; no timing or physical inference'
RECEIPT_PATH = 'research/publication-receipts/m31-buffered-motion-result-2026-10-22.json'
RECEIPT_COMMIT = 'd948a58315020eda1a1502277362ab65116c873b'
SUPPLEMENT_PATHS = {
    'research/publication-receipts/m31-buffered-motion-provenance-2026-10-22.md',
    'research/publication-receipts/m31-buffered-motion-public-review-2026-10-22.md'}
PROOF_PATHS = {
    'research/m31-buffered-candidates-2026-10-20/LITERATURE.md',
    'research/m31-buffered-candidates-2026-10-20/source/CANDIDATE.md',
    'research/m31-buffered-candidates-2026-10-20/source/candidate-cache.cjs',
    'research/m31-buffered-candidates-2026-10-20/source/candidate-kernel.cjs',
    OLD+'/LITERATURE.md', OLD+'/review/RESULT-REVIEW.md',
    'research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs',
    'research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs',
    'research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs',
    'research/m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs',
    'research/m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs'}
CASE_IDS = ['seed2026102101-original-h0025', 'seed2026102101-memory-h0025',
            'seed2026102102-original-h0025', 'seed2026102102-memory-h0025']
WINDOWS = [{'window': 3*c+j, 'caseId': case, 'start': start, 'length': 160}
           for c, case in enumerate(CASE_IDS)
           for j, start in enumerate([0, 4000, 5632 if c == 0 else 7840])]


def need(condition, label):
    if not condition:
        raise ValueError(label)


def tick():
    need(START is not None and time.monotonic()-START <= MAX_SECONDS, 'audit-wall-budget')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def compact(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate-json-key')
        out[key] = value
    return out


def bad_constant(value):
    raise ValueError('nonfinite-json-literal')


def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad_constant)


def finite(value):
    need(type(value) in (int, float) and math.isfinite(value), 'finite-number')
    return value


def integer(value, minimum=0, maximum=2**53-1):
    need(type(value) in (int, float) and math.isfinite(value)
         and value == int(value) and minimum <= value <= maximum, 'safe-integer-count')
    need(value != 0 or math.copysign(1, value) > 0, 'negative-zero-count')
    return int(value)


def number(word):
    need(type(word) is str and re.fullmatch('[0-9a-f]{16}', word), 'binary64-word')
    value = struct.unpack('>d', bytes.fromhex(word))[0]
    need(math.isfinite(value), 'finite-binary64-word')
    return value


def word(value):
    return struct.pack('>d', finite(value)).hex()


def same(left, right):
    if type(left) is bool or type(right) is bool:
        return type(left) is type(right) and left == right
    if type(left) in (int, float) and type(right) in (int, float):
        return word(left) == word(right)
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def exact(left, right, label):
    need(same(left, right), label)


def safe_path(relative):
    need(type(relative) is str and relative and not relative.startswith('/')
         and '\\' not in relative and all(x not in ('', '.', '..') for x in relative.split('/')),
         'safe-relative-path')
    target = ROOT.joinpath(relative)
    need(target.resolve().is_relative_to(ROOT) and not target.is_symlink(), 'path-within-repository')
    return target


def validate_pin(pin, maximum=MAX_PART):
    need(type(pin) is dict and 'bytes' in pin and 'sha256' in pin, 'identity-pin-shape')
    integer(pin['bytes'], 1, maximum)
    need(type(pin['sha256']) is str and re.fullmatch('[0-9a-f]{64}', pin['sha256']), 'identity-sha256')
    return pin


def local_checked(relative, pin, maximum=MAX_PART):
    validate_pin(pin, maximum)
    for attempt in range(1, 4):
        tick()
        try:
            target = safe_path(relative)
            need(target.is_file(), 'regular-input-file')
            with target.open('rb') as source:
                raw = source.read(pin['bytes']+1)
            if len(raw) == pin['bytes'] and digest(raw) == pin['sha256']:
                CONSUMED_PINS[relative] = {'bytes': len(raw), 'sha256': digest(raw)}
                return raw
            READ_EVENTS.append({'operation': 'local-identity', 'path': relative, 'attempt': attempt,
                                'kind': 'identity-mismatch', 'bytes': len(raw), 'sha256': digest(raw)})
        except (OSError, ValueError) as error:
            READ_EVENTS.append({'operation': 'local-identity', 'path': relative, 'attempt': attempt,
                                'kind': 'read-error', 'errorType': type(error).__name__})
    raise ValueError('local-identity-read-failed:'+relative)


def capture(relative, maximum=MAX_METADATA):
    tick()
    target = safe_path(relative)
    need(target.is_file(), 'capture-regular-file')
    with target.open('rb') as source:
        raw = source.read(maximum+1)
    need(0 < len(raw) <= maximum, 'capture-size')
    pin = {'bytes': len(raw), 'sha256': digest(raw)}
    CONSUMED_PINS[relative] = pin
    return parse(raw), pin


def git_once(relative, pin, origin):
    """Bound time and both pipes; never expose unverified bytes to JSON/gzip."""
    safe_path(relative)
    validate_pin(pin)
    need(re.fullmatch('[0-9a-f]{40}', origin), 'immutable-input-commit')
    command = ['git', '--no-pager', 'show', '--no-ext-diff', '--no-textconv', origin+':'+relative]
    env = {k: v for k, v in os.environ.items() if k not in
           ('GIT_EXTERNAL_DIFF', 'GIT_DIFF_OPTS', 'GIT_PAGER')}
    env['GIT_TERMINAL_PROMPT'] = '0'
    env['GIT_NO_REPLACE_OBJECTS'] = '1'
    proc = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    begin = time.monotonic()
    output, error = bytearray(), bytearray()
    selector = selectors.DefaultSelector()
    try:
        for stream, name in ((proc.stdout, 'stdout'), (proc.stderr, 'stderr')):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, name)
        while selector.get_map():
            tick()
            need(time.monotonic()-begin <= 45, 'git-read-timeout')
            for key, _ in selector.select(.2):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                target = output if key.data == 'stdout' else error
                target.extend(chunk)
                need(len(target) <= (pin['bytes'] if key.data == 'stdout' else 65536), 'git-read-output-bound')
        remaining = max(.001, 45-(time.monotonic()-begin))
        need(proc.wait(timeout=remaining) == 0, 'git-read-exit')
        return bytes(output)
    finally:
        selector.close()
        if proc.poll() is None:
            proc.kill()
        proc.wait()
        proc.stdout.close()
        proc.stderr.close()


def committed(relative, pin):
    validate_pin(pin)
    origin = pin.get('originCommit', INPUT_COMMIT)
    key = (origin, relative)
    if key in COMMITTED:
        raw = COMMITTED[key]
        need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'conflicting-committed-pin')
        return raw
    for attempt in range(1, 4):
        tick()
        try:
            raw = git_once(relative, pin, origin)
            if len(raw) == pin['bytes'] and digest(raw) == pin['sha256']:
                COMMITTED[key] = raw
                return raw
            READ_EVENTS.append({'operation': 'git-show-identity', 'commit': origin,
                                'path': relative, 'attempt': attempt, 'kind': 'identity-mismatch',
                                'bytes': len(raw), 'sha256': digest(raw)})
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            READ_EVENTS.append({'operation': 'git-show-identity', 'commit': origin,
                                'path': relative, 'attempt': attempt, 'kind': 'read-error',
                                'errorType': type(error).__name__,
                                'detail': str(error).replace(str(ROOT), '[repository]')[:400]})
    raise ValueError('committed-identity-read-failed:'+relative)


class PartReader(io.RawIOBase):
    def __init__(self, buffers):
        super().__init__()
        self.buffers, self.index, self.offset = buffers, 0, 0

    def readable(self):
        return True

    def readinto(self, target):
        tick()
        while self.index < len(self.buffers) and self.offset == len(self.buffers[self.index]):
            self.index += 1
            self.offset = 0
        if self.index == len(self.buffers):
            return 0
        size = min(len(target), len(self.buffers[self.index])-self.offset)
        target[:size] = self.buffers[self.index][self.offset:self.offset+size]
        self.offset += size
        return size


def archive_buffers(transport):
    need(transport.get('complete') is True and transport.get('nativeQueries') == 0, 'complete-no-query-transport')
    original = transport['original']
    need(original['path'] == 'extract/selected.jsonl.gz' and original['file'] == 'selected.jsonl.gz', 'original-archive-name')
    need(len(transport['parts']) == 6, 'six-published-parts')
    buffers, offset, total_hash = [], 0, hashlib.sha256()
    for i, part in enumerate(transport['parts']):
        need(set(part) == {'file', 'offset', 'bytes', 'sha256'}
             and part['file'] == 'selected.jsonl.gz.part'+str(i).zfill(3)
             and part['offset'] == offset, 'transport-part-order')
        validate_pin(part)
        relative = OLD+'/transport/'+part['file']
        pin = INPUT_PINS[relative]
        exact({k: pin[k] for k in ('bytes', 'sha256')}, {k: part[k] for k in ('bytes', 'sha256')}, 'part-source-pin')
        raw = committed(relative, pin)
        buffers.append(raw)
        offset += len(raw)
        total_hash.update(raw)
    need(offset == original['bytes'] and total_hash.hexdigest() == original['sha256'], 'whole-original-archive-identity')
    CHECKS.append('six immutable committed parts and their complete concatenated original identity verified before decompression')
    return buffers


def saved_counts(native):
    """Only accounting of saved diagnostics; no coordinates or model arithmetic."""
    need(native['schema'] == 'm31-native-load-evidence-v1'
         and native['model'] == 'ordinary-binary64-full-contribution'
         and native['method'] == 'F', 'encoded-unchanged-F-native-evidence')
    need(native['status'] in ('native-success', 'domain-refused'), 'saved-status')
    exact(native['ids'], list(range(64)), '64-canonical-ids')
    need(number(native['constants']['neighbor']) == 3, 'separate-model-center-neighbor-three')
    diagnostics = native['diagnostics']
    screen, geometry = diagnostics['screen'], diagnostics['geometryWork']
    need(screen['schema'] == 'm31-center-screen-work-v1' and screen['eligible'] is True
         and screen['fallback'] is False and screen['coordinateFinite'] is True
         and screen['spanFinite'] is True and screen['componentThreshold'] == 4
         and screen['spanLimit'] == 256 and screen['fallbackReason'] is None, 'eligible-component-four-screen')
    n = 64
    p = integer(geometry['logicalDirectedPairs'])
    norm = integer(screen['actualCenterNormCalls'])
    guard = integer(geometry['centerGuardRejectedPairs'])
    eligible = integer(geometry['centerEligiblePairs'])
    rotor = integer(geometry['pairCalls'])
    positive = integer(geometry['positiveRotorTerms'])
    need(p == n*(n-1) and integer(geometry['directedCenterTests']) == norm <= p, 'logical-and-center-counts')
    need(integer(geometry['gatheredNonselfCandidates']) == integer(screen['orderedPairVisits'])
         == integer(screen['componentTests']) == p, 'full-F-directed-enumeration')
    component = p-norm
    need(integer(geometry['certifiedSkippedPairs']) == integer(screen['skippedCenterNormCalls']) == component,
         'component-rejection-accounting')
    radial = norm-guard-eligible
    need(radial >= 0 and rotor == 4*eligible, 'center-to-rotor-accounting')
    symbols = diagnostics['symbolCounts']
    need(type(symbols) is list and len(symbols) == 12, 'twelve-symbol-counts')
    symbols = [integer(value) for value in symbols]
    need(symbols[0] == symbols[10] == 0 and sum(symbols) == 4*n*n, 'complete-symbol-domain')
    need(symbols[1]+rotor+4*guard == 4*n*n, 'self-unvisited-center-guard-symbol-accounting')
    invalid = symbols[11]-4*guard
    zero = sum(symbols[k] for k in (2, 3, 5, 6, 7, 9))
    near = symbols[4]
    need(invalid >= 0 and positive == symbols[8]
         and rotor == positive+zero+near+invalid, 'rotor-classification-conservation')
    coefficients = native['coefficients']
    need(type(coefficients) is dict and len(coefficients['offsets']) == 4*n+1
         and len(coefficients['sourceIndices']) == len(coefficients['K']) == len(coefficients['a']) == positive,
         'positive-coefficient-entry-count')
    offsets = [integer(value, 0, positive) for value in coefficients['offsets']]
    need(offsets[0] == 0 and offsets[-1] == positive and all(a <= b for a, b in zip(offsets, offsets[1:])),
         'saved-coefficient-offsets')
    positive_edges = 0
    receiver_sources = set()
    for row in range(4*n):
        previous = -1
        for pos in range(offsets[row], offsets[row+1]):
            source = integer(coefficients['sourceIndices'][pos], 0, n-1)
            need(source > previous and source != row//4 and number(coefficients['K'][pos]) > 0
                 and number(coefficients['a'][pos]) >= 0, 'positive-canonical-coefficient-row')
            previous = source
            receiver_sources.add(source)
        if row % 4 == 3:
            positive_edges += len(receiver_sources)
            receiver_sources.clear()
    need(integer(diagnostics['graph']['uniqueVehicleEdges']) == positive_edges <= eligible
         and positive_edges <= positive <= 4*positive_edges, 'saved-positive-vehicle-edge-count')
    admission = diagnostics['admission']
    need(integer(admission['unsupportedNearCount']) == near and integer(admission['invalidTermCount']) == symbols[11],
         'admission-symbol-binding')
    if native['status'] == 'native-success':
        need(native['reason'] is None and admission['admitted'] is True and admission['reasons'] == []
             and near == symbols[11] == 0, 'successful-admitted-build')
    else:
        need(native['reason'] == 'native-admission' and native['stage'] == 'build'
             and admission['admitted'] is False and admission['reasons'] == ['near-field']
             and near > 0 and symbols[11] == 0, 'preserved-near-field-build-refusal')
    return {'logicalPairs': p, 'componentSurvivors': norm, 'componentRejected': component,
            'guardRejected': guard, 'centerEligible': eligible, 'radialRejected': radial,
            'rotorCalls': rotor, 'positiveRotorTerms': positive, 'supportedZeroRotorTerms': zero,
            'positiveVehicleEdges': positive_edges,
            'unsupportedNearFieldRotorTerms': near, 'invalidRotorTerms': invalid}, symbols


def frozen_input(relative):
    need(relative in INPUT_PINS, 'missing-prospective-input-pin:'+relative)
    return parse(committed(relative, INPUT_PINS[relative]))


def source_gate():
    manifest, manifest_pin = capture(REL+'/source-manifest.json')
    publication, publication_pin = capture(REL+'/source-publication.json')
    need(publication['manifestSha256'] == manifest_pin['sha256']
         and publication['manifestBytes'] == manifest_pin['bytes'], 'public-source-manifest-hash-and-length')
    need(publication.get('remoteBytesEqualLocal') is True
         and publication.get('committedBytesEqualLocal') is True
         and publication.get('independentReviewPassed') is True, 'reviewed-public-source')
    need(re.fullmatch('[0-9a-f]{40}', publication['commit']), 'source-commit')
    for pin in manifest['files']:
        need(type(pin) is dict and pin.get('kind') in ('source', 'input'), 'manifest-pin-kind')
        need(set(pin) == ({'path', 'bytes', 'sha256', 'kind', 'originCommit'}
                         if pin['kind'] == 'input' else {'path', 'bytes', 'sha256', 'kind'}), 'manifest-pin-fields')
        relative = pin['path']
        safe_path(relative)
        validate_pin(pin)
        need(relative not in SOURCE_PINS, 'unique-source-manifest-pin')
        SOURCE_PINS[relative] = pin
        if pin['kind'] == 'source':
            local_checked(relative, pin)
        else:
            need(re.fullmatch('[0-9a-f]{40}', pin['originCommit']), 'immutable-input-origin')
            receipt_origin = relative == RECEIPT_PATH or relative in SUPPLEMENT_PATHS
            need(pin['originCommit'] == (RECEIPT_COMMIT if receipt_origin else INPUT_COMMIT), 'allowed-input-origin')
            INPUT_PINS[relative] = pin
    need(integer(publication['verifiedFilePins']) == len(SOURCE_PINS), 'public-source-pin-count')
    for name in ('config.json', 'PROTOCOL.md', 'SCHEMA.md', 'runtime.json', 'input-pins.json', 'source/audit.py',
                 'source/diagnose.py', 'source/common.py', 'source/supervise.py', 'source/launch.py',
                 'source/finalize.py', 'source/ui.cjs', 'viewer/index.html', 'viewer/app.js', 'review/AUDIT-DESIGN.md'):
        need(SOURCE_PINS.get(REL+'/'+name, {}).get('kind') == 'source', 'mandatory-prospective-source:'+name)
    for name in ('three.module.js', 'three.core.js', 'OrbitControls.js'):
        relative = 'outputs/step02b-source/vendor/'+name
        need(SOURCE_PINS.get(relative, {}).get('kind') == 'source', 'complete-three-display-dependency:'+relative)
    config = parse(local_checked(REL+'/config.json', SOURCE_PINS[REL+'/config.json']))
    expected = {'schema': 'm31-neighbor-density-config-v1', 'inputCommit': INPUT_COMMIT,
                'inputCheckpoint': OLD, 'windows': 12, 'stagesPerWindow': 160, 'stages': 1920,
                'drones': 64, 'componentThreshold': 4, 'centerNeighborThreshold': 3, 'nativeCalls': 0,
                'allocations': {'producer': {'seconds': 1200, 'mib': 32}, 'audit': {'seconds': 1200, 'mib': 4},
                                'finalize': {'seconds': 120, 'mib': 2}, 'ui': {'seconds': 150, 'mib': 16}},
                'readPolicy': {'attemptsPerFile': 3, 'gitReadTimeoutSeconds': 45},
                'newNumericalModelQueries': False, 'selectedLineByteLimit': 8*1024**2}
    exact(config, expected, 'fixed-prospective-config')
    required = {OLD+'/'+p for p in ('transport/index.json', 'extract/index.json', 'audit/audit.json',
                                   'audit/viewer-data.json', 'ALLOCATION-CLOSURE.json', 'result-manifest.json')}
    required.add(RECEIPT_PATH)
    required.update(OLD+'/transport/selected.jsonl.gz.part'+str(i).zfill(3) for i in range(6))
    required.update(PROOF_PATHS | SUPPLEMENT_PATHS)
    need(set(INPUT_PINS) == required and len(INPUT_PINS) == 26, 'exact-twenty-six-input-pins')
    input_index = parse(local_checked(REL+'/input-pins.json', SOURCE_PINS[REL+'/input-pins.json']))
    exact(input_index, {'files': [INPUT_PINS[path] for path in sorted(INPUT_PINS)]}, 'frozen-input-pin-index')
    CHECKS.append('reviewed public source and complete Three.js display dependency pins checked; exact immutable input inventory and allocation config')
    return publication, manifest_pin, publication_pin


def prior_gate():
    manifest_path = OLD+'/result-manifest.json'
    need(INPUT_PINS[manifest_path]['bytes'] == 545123
         and INPUT_PINS[manifest_path]['sha256'] == '440d2ac225f1587359cfa96af5d27b9a9b37d962ce25d75701c4fc195d753025',
         'fixed-previous-result-manifest')
    manifest, receipt = frozen_input(manifest_path), frozen_input(RECEIPT_PATH)
    need(manifest['schema'] == 'm31-buffered-motion-result-v1', 'previous-result-schema')
    need(receipt['schema'] == 'm31-buffered-motion-public-result-v1' and receipt['commit'] == INPUT_COMMIT
         and receipt['manifestPath'] == manifest_path and receipt['manifestBytes'] == 545123
         and receipt['manifestSha256'] == INPUT_PINS[manifest_path]['sha256']
         and receipt['verifiedFilePins'] == 2104 and receipt['committedBytesEqualLocal'] is True
         and receipt['remoteManifestBytesEqualLocal'] is True, 'previous-final-publication-receipt')
    public = {pin['path']: pin for pin in manifest['files']}
    need(len(public) == len(manifest['files']) == 2104, 'previous-result-pin-inventory')
    supplement = {pin['path']: pin for pin in receipt['supplementalPublicationRecords']}
    for relative, pin in INPUT_PINS.items():
        if relative in (manifest_path, RECEIPT_PATH):
            continue
        identity = {k: pin[k] for k in ('path', 'bytes', 'sha256')}
        if relative in SUPPLEMENT_PATHS:
            exact(supplement.get(relative), identity, 'previous-supplemental-publication-identity')
        elif relative in public:
            exact(public[relative], identity, 'previous-public-input-identity')
        else:
            need(relative in PROOF_PATHS, 'core-input-missing-from-previous-result-manifest')
        if '.jsonl.gz.part' not in relative:
            committed(relative, pin)
    transport = frozen_input(OLD+'/transport/index.json')
    extraction = frozen_input(OLD+'/extract/index.json')
    report = frozen_input(OLD+'/audit/audit.json')
    viewer = frozen_input(OLD+'/audit/viewer-data.json')
    closure = frozen_input(OLD+'/ALLOCATION-CLOSURE.json')
    need(report['passed'] is True and report['evidenceIntegrityPassed'] is True
         and report['exactReferenceEquivalence'] is True and report['candidateCertificatePassed'] is True
         and report['selectedStages'] == 1920 and report['sourcePartsScanned'] == 93
         and report['sourceJournalsScanned'] == 8 and report['newNativeQueriesByAudit'] == 0,
         'previous-independent-source-binding-passed')
    need(report['sourceCommit'] == viewer['sourceCommit'] == manifest['sourceCommit'], 'previous-source-commit-binding')
    exact(report['viewerPin'], {'file': 'viewer-data.json', 'bytes': INPUT_PINS[OLD+'/audit/viewer-data.json']['bytes'],
                               'sha256': INPUT_PINS[OLD+'/audit/viewer-data.json']['sha256']}, 'previous-audit-viewer-pin')
    exact(report['extractionIndexPin'], {k: INPUT_PINS[OLD+'/extract/index.json'][k] for k in ('bytes', 'sha256')},
          'previous-audit-extraction-pin')
    need(extraction['complete'] is True and extraction['selected'] == 1920 and extraction['nativeQueries'] == 0,
         'previous-complete-selection')
    exact(extraction['windows'], WINDOWS, 'fixed-twelve-windows')
    exact(extraction['selectedPin'], {k: transport['original'][k] for k in ('file', 'bytes', 'sha256')}, 'same-selected-original')
    need(closure['allClosed'] is True and closure['transportIdentityVerified'] is True
         and closure['transportParts'] == 6 and closure['transport']['closed'] is True
         and closure['transport']['exitCode'] == 0, 'previous-closed-transport')
    exact(closure['logicalOriginal'], transport['original'], 'previous-closure-original-identity')
    for phase in ('extract', 'producer', 'audit', 'finalize', 'ui'):
        item = closure['phases'][phase]
        need(item['closed'] is True and item['returncode'] == 0 and item['allocationWallPassed'] is True
             and item['outputCapPassed'] is True and not item.get('timeout'), 'previous-closed-phase:'+phase)
    need(viewer['schema'] == 'm31-buffered-motion-view-v1' and viewer['completedEndpoints'] is False
         and len(viewer['windows']) == 12, 'previous-viewer-schema')
    for w, actual in zip(WINDOWS, viewer['windows']):
        exact({k: actual[k] for k in w}, w, 'previous-viewer-fixed-window')
        need(len(actual['frames']) == 160, 'previous-viewer-frame-count')
    CHECKS.append('previous public manifest, final receipt, successful audit, selected archive, viewer and all closed allocations bound; original journals not reopened')
    return transport, viewer, report, receipt


def selected_rows(buffers, viewer):
    with io.BufferedReader(PartReader(buffers)) as stream, gzip.GzipFile(fileobj=stream, mode='rb') as zipped:
        for window in WINDOWS:
            for index in range(160):
                tick()
                line = zipped.readline(MAX_RECORD+1)
                need(0 < len(line) <= MAX_RECORD and line.endswith(b'\n'), 'bounded-complete-selected-record')
                saved = parse(line)
                need(type(saved) is dict and set(saved) == {'window', 'index', 'caseId', 'globalOrdinal', 'segment',
                     'localStageOrdinal', 'rawOffset', 'sourceLineSha256', 'sourceLineBytes', 'record'}, 'selected-envelope-fields')
                ordinal = window['start']+index
                exact([saved['window'], saved['index'], saved['caseId'], saved['globalOrdinal']],
                      [window['window'], index, window['caseId'], ordinal], 'selected-fixed-order')
                need(re.fullmatch('[0-9a-f]{64}', saved['sourceLineSha256']), 'original-line-sha256')
                integer(saved['sourceLineBytes'], 1, 4*1024**2)
                integer(saved['rawOffset'])
                integer(saved['segment'], 0, 1)
                integer(saved['localStageOrdinal'])
                record = saved['record']
                need(type(record) is dict and set(record) == {'sequence', 'kind', 'body'}
                     and record['kind'] == 'stage', 'original-whole-stage-envelope')
                integer(record['sequence'])
                body = record['body']
                need(body['schema'] == 'm31-coupled-stage-v1' and body['arm'] == 'coupled', 'original-stage-schema')
                native = body['native']
                counts, symbols = saved_counts(native)
                need(body['status'] == ('completed' if native['status'] == 'native-success' else 'failed'),
                     'original-stage-native-outcome')
                if native['status'] != 'native-success':
                    need(body['reason'] == 'native-non-success'
                         and not any(key in native for key in ('loads', 'solution', 'consumption')), 'original-refusal-not-consumed')
                native_input = body['nativeInput']
                need(type(native_input) is dict and set(native_input) == {'drones'}
                     and len(native_input['drones']) == len(native['raw']) == len(native['prepared']) == 64, 'full-saved-native-input')
                positions = []
                for ident, drone in enumerate(native_input['drones']):
                    need(type(drone) is dict and set(drone) == {'id', 'state'} and drone['id'] == ident
                         and len(drone['state']) == 17, 'canonical-seventeen-word-input')
                    integer(drone['id'], ident, ident)
                    values = [number(x) for x in drone['state']]
                    need(all(value > 0 for value in values[13:]), 'saved-positive-nominal-input')
                    exact(native['raw'][ident], drone, 'saved-encoded-raw-input')
                    need(native['prepared'][ident]['id'] == ident, 'prepared-id')
                    exact(native['prepared'][ident]['center'], drone['state'][:3], 'prepared-input-center-words')
                    positions.append(values[:3])
                frame = viewer['windows'][window['window']]['frames'][index]
                expected_frame = {'index': index, 'globalOrdinal': ordinal, 'time': number(body['originalTimeWord']),
                                  'timeWord': body['originalTimeWord'], 'status': native['status'], 'reason': native['reason'],
                                  'positions': positions, 'segment': saved['segment'], 'stageIndex': body['stageIndex'],
                                  'sourceLineSha256': saved['sourceLineSha256'], 'sourceLineBytes': saved['sourceLineBytes'],
                                  'sourceSequence': record['sequence'], 'rawOffset': saved['rawOffset'],
                                  'kind': 'recorded-attempted-RK-stage-input', 'completedEndpoint': False}
                exact({k: frame[k] for k in expected_frame}, expected_frame, 'previous-audited-frame-bitwise-binding')
                yield {'window': window['window'], 'index': index, 'caseId': window['caseId'], 'globalOrdinal': ordinal,
                       'sourceLineSha256': saved['sourceLineSha256'], 'selectedRecordSha256': digest(line),
                       'timeWord': body['originalTimeWord'], 'time': number(body['originalTimeWord']),
                       'status': native['status'], 'reason': native['reason'], 'nativeStage': native.get('stage'),
                       'admissionReasons': native['diagnostics']['admission']['reasons'],
                       'ids': list(range(64)), 'positions': positions, 'counts': counts, 'symbols': symbols}
        need(zipped.read(1) == b'', 'exactly-1920-selected-records')


def group(rows):
    need(rows, 'nonempty-fixed-group')
    return {'stages': len(rows),
            'totals': {key: sum(row['counts'][key] for row in rows) for key in COUNTS_KEYS},
            'min': {key: min(row['counts'][key] for row in rows) for key in COUNTS_KEYS},
            'max': {key: max(row['counts'][key] for row in rows) for key in COUNTS_KEYS},
            'componentNonzeroStages': sum(row['counts']['componentRejected'] > 0 for row in rows),
            'radialNonzeroStages': sum(row['counts']['radialRejected'] > 0 for row in rows)}


def summarize(rows):
    need(len(rows) == 1920, 'exact-stage-census')
    refused = [row for row in rows if row['status'] != 'native-success']
    need(len(refused) == 1 and refused[0]['window'] == 2 and refused[0]['index'] == 159,
         'same-inherited-refusal-census')
    overall = group(rows)
    component = overall['componentNonzeroStages'] > 0
    radial = overall['radialNonzeroStages'] > 0
    windows = [{**{k: window[k] for k in ('window', 'caseId', 'start')},
                **group(rows[window['window']*160:(window['window']+1)*160])} for window in WINDOWS]
    refusal_keys = ('window', 'index', 'caseId', 'globalOrdinal', 'timeWord', 'status', 'reason', 'nativeStage', 'admissionReasons')
    return {'schema': 'm31-neighbor-density-summary-v1', 'stages': 1920, 'nativeCalls': 0,
            'countsKeys': COUNTS_KEYS, 'overall': overall, 'windows': windows,
            'byStatus': {status: group([row for row in rows if row['status'] == status])
                         for status in ('native-success', 'domain-refused')},
            'refusals': [{key: row[key] for key in refusal_keys} for row in refused],
            'decision': {'componentOpportunityExists': component, 'radialOpportunityExists': radial,
                         'bufferWidthTuningForTheseClips': 'unresolved' if component else 'retire',
                         'radialFollowup': 'consider-separate-proof' if radial else 'no-distance-headroom-observed'},
            'scope': SCOPE}


def producer_gate():
    supervisor, supervisor_pin = capture(REL+'/producer-supervisor.json')
    closed, exit_pin = capture(REL+'/results/exit.json')
    need(supervisor.get('closed') is True and supervisor.get('returncode') == 0
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True
         and not supervisor.get('timeout') and not supervisor.get('evidenceOverflow'), 'closed-successful-producer-supervision')
    need(closed.get('closed') is True and closed.get('exitCode') == 0, 'closed-successful-producer-exit')
    need(0 <= finite(supervisor['wallSeconds']) <= 1200 and 0 <= finite(closed['wallSeconds']) <= 1200,
         'producer-wall-bounds')
    expected = {'launch.json', 'stages.jsonl', 'summary.json', 'input-binding.json', 'exit.json'}
    paths = list((BASE/'results').iterdir())
    need({path.name for path in paths} == expected and all(path.is_file() and not path.is_symlink() for path in paths),
         'exact-closed-producer-inventory')
    size = sum(path.stat().st_size for path in paths)
    need(size == supervisor['outputBytes'] <= MAX_RESULT, 'producer-complete-output-byte-accounting')
    launch, _ = capture(REL+'/results/launch.json')
    exact(launch, {'singleUse': True, 'nativeCalls': 0}, 'producer-single-use-no-query-launch')
    need(type(closed['readEvents']) is list, 'producer-retained-read-events')
    CHECKS.append('single-use successful producer closure, wall/output limits and complete regular-file inventory checked')
    return closed, supervisor_pin, exit_pin


def captured_bytes(relative, maximum):
    tick()
    target = safe_path(relative)
    need(target.is_file(), 'captured-data-regular-file')
    with target.open('rb') as source:
        raw = source.read(maximum+1)
    need(0 < len(raw) <= maximum, 'captured-data-size')
    pin = {'bytes': len(raw), 'sha256': digest(raw)}
    CONSUMED_PINS[relative] = pin
    return raw, pin


def audit():
    publication, manifest_pin, publication_pin = source_gate()
    transport, viewer, old_audit, receipt = prior_gate()
    producer_exit, supervisor_pin, exit_pin = producer_gate()
    binding, binding_pin = capture(REL+'/results/input-binding.json')
    need(set(binding) == {'sourceCommit', 'sourceManifestSha256', 'original', 'consumedPins', 'readEvents'},
         'producer-input-binding-fields')
    need(binding['sourceCommit'] == publication['commit']
         and binding['sourceManifestSha256'] == manifest_pin['sha256'], 'producer-current-source-binding')
    exact(binding['original'], transport['original'], 'producer-original-archive-binding')
    exact(binding['consumedPins'], [INPUT_PINS[path] for path in sorted(INPUT_PINS)], 'producer-exact-committed-input-pins')
    exact(binding['readEvents'], producer_exit['readEvents'], 'producer-anomaly-accounting')
    buffers = archive_buffers(transport)
    need(set(COMMITTED) == {(pin['originCommit'], relative) for relative, pin in INPUT_PINS.items()},
         'all-twenty-six-committed-input-identities-consumed')
    data, data_pin = captured_bytes(REL+'/results/stages.jsonl', MAX_RESULT)
    summary_raw, summary_pin = captured_bytes(REL+'/results/summary.json', MAX_METADATA)
    actual_lines = io.BytesIO(data)
    rows = []
    for expected in selected_rows(buffers, viewer):
        actual = actual_lines.readline(MAX_RECORD+1)
        need(0 < len(actual) <= MAX_RECORD and actual.endswith(b'\n'), 'complete-produced-stage-line')
        # Actual byte comparison includes exact JSON field set, sorting, escaping,
        # number rendering, newline, and the full selected-record digest.
        need(actual == compact(expected)+b'\n', 'independent-stage-canonical-bytes')
        rows.append(expected)
    need(actual_lines.read(1) == b'', 'no-extra-produced-stage-record')
    summary = summarize(rows)
    need(summary_raw == compact(summary)+b'\n', 'independent-complete-summary-canonical-bytes')
    CHECKS.append('all 1920 whole selected records independently streamed once and bound bitwise to prior audited frames, native inputs and prepared centers')
    CHECKS.append('all saved center/component/rotor/symbol counters and positive CSR vehicle edges independently reconciled; inherited failed build preserved')
    CHECKS.append('every produced row and all twelve clip, status and overall sums/extrema/censuses/branch decisions match independently reconstructed canonical bytes')
    for relative, pin in list(CONSUMED_PINS.items()):
        local_checked(relative, pin, MAX_RESULT)
    tick()
    file_pins = [{'file': name, **CONSUMED_PINS[REL+'/'+name]}
                 for name in ('results/stages.jsonl', 'results/summary.json', 'results/input-binding.json', 'results/exit.json')]
    report = {'schema': 'm31-neighbor-density-audit-v1', 'passed': True,
              'evidenceIntegrityPassed': True, 'independentCountAccountingPassed': True,
              'stages': 1920, 'nativeCalls': 0, 'summary': summary, 'checks': CHECKS,
              'sourceCommit': publication['commit'], 'sourceManifestSha256': manifest_pin['sha256'],
              'sourceManifestPin': manifest_pin, 'sourcePublicationPin': publication_pin,
              'filePins': file_pins, 'producerSupervisorPin': supervisor_pin,
              'original': transport['original'], 'inputPins': [INPUT_PINS[path] for path in sorted(INPUT_PINS)],
              'inputCommit': INPUT_COMMIT, 'priorAuditPin': INPUT_PINS[OLD+'/audit/audit.json'],
              'priorFinalReceiptPin': INPUT_PINS[RECEIPT_PATH],
              'priorDisplayProvenanceQualification': receipt.get('displayProvenanceQualification'),
              'sourceRecordBindingScope': 'previous independent audit binds this exact selected archive to original journals; only selected archive is rescanned here',
              'readEvents': READ_EVENTS, 'producerReadEvents': producer_exit['readEvents'],
              'scope': SCOPE, 'independence': 'Python standard library only; no producer/common or scientific module imported',
              'geometryRecomputed': False, 'pairMembershipRecomputed': False,
              'nativeModelQueries': 0, 'originalJournalsReopened': False,
              'zeroSkinInterpretation': 'current component survivors are an optimistic lower bound on pairs retained by the same conservative component-box rule; outward rounding may retain more',
              'radialInterpretation': 'radialRejected is saved center Euclidean distance rejection at neighbor=3, distinct from rotor-axis radial classification and component threshold=4',
              'positiveEdgeInterpretation': 'positive coefficient vehicle edges do not enumerate all status-relevant pairs; absent terms can be near-field unsupported',
              'timingInference': False, 'physicalValidity': False, 'flightSafetyClaim': False,
              'statisticalInference': False, 'speedupClaim': False, 'researchComplete': False}
    return report


def main():
    global START
    START = time.monotonic()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'optimized-audit-not-permitted')
    need((BASE/'audit-supervisor-launch.lock').is_file(), 'single-audit-supervisor-allocation-required')
    out = BASE/'audit'
    need(not out.is_symlink(), 'audit-directory-not-symlink')
    out.mkdir()
    charged = 0

    def save(name, value, failure=False):
        nonlocal charged
        raw = compact(value)+b'\n'
        reserve = 0 if failure else 128*1024
        need(charged+len(raw)+reserve <= MAX_OUTPUT, 'audit-output-budget')
        if not failure:
            tick()
        charged += len(raw)
        with (out/name).open('xb') as target:
            need(target.write(raw) == len(raw), 'audit-complete-write')

    code = 0
    try:
        save('launch.json', {'singleUse': True, 'nativeCalls': 0,
                            'startedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            'scope': 'independent saved-record count audit'})
        report = audit()
        report['wallSeconds'] = time.monotonic()-START
        save('audit.json', report)
    except Exception as error:
        code = 1
        save('failure.json', {'type': type(error).__name__,
                             'message': str(error).replace(str(ROOT), '[repository]')[:2000],
                             'checksCompleted': CHECKS, 'readEvents': READ_EVENTS,
                             'wallSeconds': time.monotonic()-START}, failure=True)
    finally:
        save('exit.json', {'closed': True, 'exitCode': code, 'wallSeconds': time.monotonic()-START,
                           'readEvents': READ_EVENTS}, failure=True)
    return code


if __name__ == '__main__':
    sys.exit(main())
