"""Prospective saved-only radial integration auditor; never import scientific modules.

Adapted as source text from buffered-motion source/audit.py (identity/normalization,
query schedule, timing and inventory architecture) and radial-certificate
source/audit.py (independently authored exact-ratio RN-even certificate routines).
No prior auditor is imported or executed. Source preparation permits AST parsing
only. This file executes solely under its new reviewed single-use allocation.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction
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
OLD = 'research/m31-buffered-motion-2026-10-22'
RADIAL = 'research/m31-radial-certificate-2026-10-23'
DENSITY = 'research/m31-neighbor-density-2026-10-23'
MAX_SECONDS = 1800
MAX_OUTPUT = 128*1024**2
MAX_INPUT = 768*1024**2
MAX_PART = 32*1024**2
MAX_RECORD = 4*1024**2
START = None
PINS, SOURCE_PINS, READ_EVENTS, CHECKS = {}, {}, [], []
OPERATION = 0
WORD = re.compile(r'^[0-9a-f]{16}$')
SHA = re.compile(r'^[0-9a-f]{64}$')
SIGN, FRACTION_MASK = 1 << 63, (1 << 52)-1
BASELINE_EXCLUSIONS = ['method', 'timing', 'diagnostics.buildPhasesMs',
    'diagnostics.geometryWork.gatheredNonselfCandidates', 'diagnostics.screen.orderedPairVisits',
    'diagnostics.screen.componentTests', 'caseId', 'semanticInputSha256', 'inlineInputCanonicalSha256']
ADDED_EXCLUSIONS = ['diagnostics.geometryWork.directedCenterTests',
    'diagnostics.geometryWork.certifiedSkippedPairs', 'diagnostics.screen.actualCenterNormCalls',
    'diagnostics.screen.skippedCenterNormCalls']
EXCLUSIONS = BASELINE_EXCLUSIONS + ADDED_EXCLUSIONS
CASE_IDS = ['seed2026102101-original-h0025', 'seed2026102101-memory-h0025',
            'seed2026102102-original-h0025', 'seed2026102102-memory-h0025']
TOTAL_STAGES = [5792, 8000, 8000, 8000]
WINDOWS = [{'window': ci*3+wi, 'caseId': case, 'start': start, 'length': 160}
           for ci, case in enumerate(CASE_IDS)
           for wi, start in enumerate((0, 4000, TOTAL_STAGES[ci]-160))]
COUNTERS = ['queries', 'builds', 'reuses', 'fallbacks', 'invalidations',
            'identityRebuilds', 'boxExitRebuilds', 'buildOrderedPairs',
            'buildIntervalCoordinateTests', 'containmentCoordinateTests']
SCOPE = 'fixed exposed N64 chopped-window conditional radial integration cost; not full-flight throughput, universal equivalence or physical validation'
IMMUTABLE = {
    REL+'/source/candidate.cjs': '2e11acb60ad7ab447bc137e6ade56c24ef2b383444db7d46643648bd83cd807b',
    REL+'/source/candidate-kernel.cjs': '4fea99f4e61bff3c5eb54a0090e50b48e41d4cdf7cff5cdc770a37366f321b19',
    'research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs':
    'b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1'}
EXPECTED_CONFIG = {'schema': 'm31-radial-integration-config-v1', 'caseIds': ['seed2026102101-original-h0025', 'seed2026102101-memory-h0025', 'seed2026102102-original-h0025', 'seed2026102102-memory-h0025'], 'totalStages': [5792, 8000, 8000, 8000], 'windowLength': 160, 'windowStarts': [0, 4000, 'last160'], 'repetitions': [-1, 0, 1, 2, 3, 4, 5, 6, 7], 'maxCalls': 34560, 'exclusions': ['method', 'timing', 'diagnostics.buildPhasesMs', 'diagnostics.geometryWork.gatheredNonselfCandidates', 'diagnostics.screen.orderedPairVisits', 'diagnostics.screen.componentTests', 'caseId', 'semanticInputSha256', 'inlineInputCanonicalSha256', 'diagnostics.geometryWork.directedCenterTests', 'diagnostics.geometryWork.certifiedSkippedPairs', 'diagnostics.screen.actualCenterNormCalls', 'diagnostics.screen.skippedCenterNormCalls'], 'allocations': {'producer': {'seconds': 1800, 'mib': 768}, 'audit': {'seconds': 1800, 'mib': 128}, 'finalize': {'seconds': 120, 'mib': 2}, 'ui': {'seconds': 150, 'mib': 16}}, 'keepGate': {'medianAggregateRatioMaximum': 0.9, 'strictWinsMinimum': 7, 'reuseRequired': True, 'motionRebuildRequiredWorkloadWide': True}, 'runtimeGeneralEquivalenceProven': False, 'baselineExclusions': ['method', 'timing', 'diagnostics.buildPhasesMs', 'diagnostics.geometryWork.gatheredNonselfCandidates', 'diagnostics.screen.orderedPairVisits', 'diagnostics.screen.componentTests', 'caseId', 'semanticInputSha256', 'inlineInputCanonicalSha256'], 'readPolicy': {'attemptsPerFile': 3, 'gitReadTimeoutSeconds': 45}}
FIXED_PRIOR_METADATA = {'research/m31-buffered-motion-2026-10-22/result-manifest.json': {'bytes': 545123, 'sha256': '440d2ac225f1587359cfa96af5d27b9a9b37d962ce25d75701c4fc195d753025'}, 'research/publication-receipts/m31-buffered-motion-result-2026-10-22.json': {'bytes': 3090, 'sha256': 'c026b172b3b237280d50097692bae595f372f1b284fecce0082a445ab2fe8c25'}, 'research/m31-radial-certificate-2026-10-23/result-manifest.json': {'bytes': 23297, 'sha256': 'c3825a3e6886ecdff8ebfa521484f6b21704091966bbd82271d9225b70566514'}, 'research/publication-receipts/m31-radial-certificate-result-2026-10-23.json': {'bytes': 3730, 'sha256': '48a91e2190c9ea49ceb7f313fc99072c28b23edd40bd49491a13eaa16628b00d'}}

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


def identity(pin):
    need(type(pin) is dict and 'bytes' in pin and 'sha256' in pin, 'identity-fields')
    return {'bytes': pin['bytes'], 'sha256': pin['sha256']}


def normalization(value, path='', exclusions=None):
    ignored = EXCLUSIONS if exclusions is None else exclusions
    if type(value) in (int, float):
        return word(finite(value))
    if type(value) is list:
        return [normalization(v, path+'[]', ignored) for v in value]
    if type(value) is dict:
        return {k: normalization(value[k], path+'.'+k if path else k, ignored)
                for k in sorted(value) if (path+'.'+k if path else k) not in ignored}
    need(value is None or type(value) in (str, bool), 'normalization-value')
    return value


def rooted(value, path):
    for key in path.split('.'):
        need(type(value) is dict and key in value, 'required-rooted-field:'+path)
        value = value[key]
    return value


def reinsert_work(shared, added):
    # shared is a fresh parsed canonical object; scientific values are already words.
    for path in ADDED_EXCLUSIONS:
        parts = path.split('.'); parent = shared
        for part in parts[:-1]:
            need(type(parent) is dict and part in parent, 'strict-baseline-parent')
            parent = parent[part]
        need(parts[-1] not in parent, 'strict-baseline-field-was-excluded')
        parent[parts[-1]] = normalization(added[path], exclusions=[])
    return compact(normalization(shared, exclusions=[]))+b'\n'


def source_gate():
    manifest, manifest_pin = capture('source-manifest.json', MAX_RECORD)
    publication, publication_pin = capture('source-publication.json', MAX_RECORD)
    need(publication['manifestSha256'] == manifest_pin['sha256'], 'public-source-manifest')
    need(publication.get('remoteBytesEqualLocal') is True and publication.get('committedBytesEqualLocal') is True
         and publication.get('independentReviewPassed') is True, 'public-reviewed-source-required')
    need(type(publication.get('commit')) is str and re.fullmatch('[0-9a-f]{40}', publication['commit']), 'source-commit')
    for pin in manifest['files']:
        need({'path','bytes','sha256'} <= set(pin) and pin['path'] not in SOURCE_PINS, 'unique-source-pin')
        SOURCE_PINS[pin['path']] = pin
        checked(pin['path'], pin)
    integer(publication.get('verifiedFilePins'), len(SOURCE_PINS), len(SOURCE_PINS), 'published-pin-count')
    for name in ('config.json','PROTOCOL.md','SCHEMA.md','review/AUDIT-DESIGN.md','source/audit.py',
                 'source/run.cjs','source/common.cjs','source/candidate-cache.cjs','source/candidate.cjs',
                 'source/candidate-kernel.cjs','source/supervise.py','source/launch.py','runtime.json'):
        need(REL+'/'+name in SOURCE_PINS, 'mandatory-source:'+name)
    for name in ('outputs/step02b-source/vendor/three.module.js',
                 'outputs/step02b-source/vendor/three.core.js',
                 'outputs/step02b-source/vendor/OrbitControls.js'):
        need(name in SOURCE_PINS, 'renderer-closure-pin:'+name)
    exact(frozen(REL+'/config.json'), EXPECTED_CONFIG, 'fixed-config')
    for relative, sha in IMMUTABLE.items():
        need(SOURCE_PINS.get(relative, {}).get('sha256') == sha, 'unchanged-wrapper-kernel-native-source')
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
    need(set(IMMUTABLE) <= visited and REL+'/source/candidate-cache.cjs' in visited, 'native-cache-dependency-closure')
    CHECKS.append('exact reviewed public source/config, unchanged wrapper/kernel/native and transitive CJS plus renderer closure inspected as text')
    return publication, manifest_pin, publication_pin, sorted(visited)


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


def cas_pin(value, kind):
    need(type(value) is dict and set(value) == {'file', 'bytes', 'sha256'}, 'CAS-pin-fields')
    need(type(value['sha256']) is str and SHA.fullmatch(value['sha256'])
         and value['file'] == kind+'-'+value['sha256']+'.json', 'CAS-name')
    integer(value['bytes'], 1, MAX_RECORD, 'CAS-size')
    return REL+'/results/'+value['file']


def rational(bits):
    """Exact real value of one finite binary64 word, with no floating operation."""
    exponent = (bits >> 52) & 2047
    fraction = bits & FRACTION_MASK
    need(exponent != 2047, 'finite-certificate-word')
    mantissa, power = (fraction, -1074) if exponent == 0 else ((1 << 52)+fraction, exponent-1075)
    if bits & SIGN:
        mantissa = -mantissa
    return Fraction(mantissa << power, 1) if power >= 0 else Fraction(mantissa, 1 << (-power))


def nearest_integer(numerator, denominator):
    quotient, remainder = divmod(numerator, denominator)
    if 2*remainder > denominator or (2*remainder == denominator and quotient & 1):
        quotient += 1
    return quotient


def rn_bits(value):
    """Integer-only binary64 round-to-nearest, ties-to-even, gradual underflow."""
    numerator, denominator = value.numerator, value.denominator
    if numerator == 0:
        return 0
    sign = SIGN if numerator < 0 else 0
    numerator = abs(numerator)
    exponent = numerator.bit_length()-denominator.bit_length()
    if (numerator < denominator << exponent) if exponent >= 0 else (numerator << (-exponent) < denominator):
        exponent -= 1
    if exponent < -1022:
        significand = nearest_integer(numerator << 1074, denominator)
        need(significand <= 1 << 52, 'subnormal-rounding-domain')
        return sign | significand
    shift = 52-exponent
    significand = nearest_integer(numerator << shift, denominator) if shift >= 0 else nearest_integer(numerator, denominator << (-shift))
    if significand == 1 << 53:
        significand >>= 1
        exponent += 1
    need(-1022 <= exponent <= 1023 and (1 << 52) <= significand < (1 << 53), 'finite-normal-rounding-domain')
    return sign | ((exponent+1023) << 52) | (significand-(1 << 52))


def word_bits(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{16}', value), 'binary64-word-shape')
    return int(value, 16)


def float_bits(value):
    return int(word(value), 16)


def next_up(bits):
    need(((bits >> 52) & 2047) != 2047, 'finite-next-up-input')
    if bits & ~SIGN == 0:
        return 1
    return bits-1 if bits & SIGN else bits+1


def next_down(bits):
    return next_up(bits ^ SIGN) ^ SIGN


def down_nonnegative(value):
    bits = next_down(rn_bits(value))
    return 0 if bits & SIGN else bits


def exact_boxes(reference):
    half = Fraction(1, 8)
    boxes = []
    for point in reference:
        need(type(point) is list and len(point) == 3, 'reference-coordinate-width')
        row = []
        for coordinate in point:
            center = rational(float_bits(coordinate))
            need(abs(center) <= 1 << 20, 'reference-coordinate-domain')
            lower = next_down(rn_bits(center-half))
            upper = next_up(rn_bits(center+half))
            need(rational(lower) <= center <= rational(upper), 'reference-inside-exact-outward-box')
            row.extend([lower, upper])
        boxes.append(row)
    return boxes


def certificate_mask(boxes):
    """Independently replay every basic op and prove the rational lower inequality."""
    threshold = Fraction(3)+Fraction(1, 1 << 20)
    threshold_square = next_up(rn_bits(threshold*threshold))
    upper = rational(threshold_square)
    need(upper >= threshold*threshold, 'exact-upper-threshold-enclosure')
    mask = []
    omitted = 0
    for i, receiver in enumerate(boxes):
        tick()
        for j, source in enumerate(boxes):
            if i == j:
                continue
            gaps, squares = [], []
            for axis in range(3):
                lower = rational(rn_bits(rational(source[2*axis])-rational(receiver[2*axis+1])))
                higher = rational(rn_bits(rational(source[2*axis+1])-rational(receiver[2*axis])))
                need(lower <= higher, 'rounded-difference-interval-order')
                gap = max(Fraction(0), lower, -higher)
                gaps.append(gap)
                squares.append(down_nonnegative(gap*gap))
            first = down_nonnegative(rational(squares[0])+rational(squares[1]))
            total = down_nonnegative(rational(first)+rational(squares[2]))
            lower_square = rational(total)
            need(0 <= lower_square <= sum(gap*gap for gap in gaps), 'exact-rational-squared-lower-enclosure')
            exclude = int(lower_square >= upper)
            if exclude:
                need(sum(gap*gap for gap in gaps) >= threshold*threshold, 'omitted-pair-rational-certificate')
                omitted += 1
            mask.append(exclude)
    return mask, omitted


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



def prior_gate():
    for relative, pin in FIXED_PRIOR_METADATA.items():
        exact(identity(SOURCE_PINS.get(relative)), pin, 'fixed-prior-metadata')
    old_manifest = frozen(OLD+'/result-manifest.json')
    radial_manifest = frozen(RADIAL+'/result-manifest.json')
    old_receipt = frozen('research/publication-receipts/m31-buffered-motion-result-2026-10-22.json')
    radial_receipt = frozen('research/publication-receipts/m31-radial-certificate-result-2026-10-23.json')
    for base, manifest, receipt, commit in (
            (OLD, old_manifest, old_receipt, '0461153a7d6f75cb6e8564850b77e8b6f04cebb2'),
            (RADIAL, radial_manifest, radial_receipt, 'afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d')):
        need(receipt['commit'] == commit and receipt['manifestPath'] == base+'/result-manifest.json', 'fixed-prior-public-result')
        exact({'bytes':receipt['manifestBytes'],'sha256':receipt['manifestSha256']},
              identity(SOURCE_PINS[base+'/result-manifest.json']), 'prior-manifest-receipt-identity')
        need(receipt['remoteManifestBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True,
             'prior-public-manifest-and-commit')
        need(len(manifest['files']) == receipt['verifiedFilePins'], 'prior-manifest-pin-count')
    need(old_receipt['independentPublicCheck']['passedWithDisplayProvenanceQualification'] is True,
         'old-qualified-independent-public-review')
    need(radial_receipt['independentPublicReviewPassed'] is True, 'radial-independent-public-review')
    old_public = {p['path']:p for p in old_manifest['files']}
    radial_public = {p['path']:p for p in radial_manifest['files']}
    need(len(old_public)==len(old_manifest['files']) and len(radial_public)==len(radial_manifest['files']), 'unique-prior-public-pins')
    old_names = ['transport/index.json','extract/index.json','audit/audit.json','ALLOCATION-CLOSURE.json']
    radial_names = ['results/stages.jsonl','results/classes.bin','results/omitted.bin',
                    'results/witnesses.jsonl','results/summary.json','audit/audit.json','ALLOCATION-CLOSURE.json']
    for base, public, names in ((OLD,old_public,old_names),(RADIAL,radial_public,radial_names)):
        for name in names:
            relative=base+'/'+name
            exact(identity(SOURCE_PINS.get(relative)), identity(public.get(relative)), 'prior-public-input-pin:'+name)
    transport, extraction = frozen(OLD+'/transport/index.json'), frozen(OLD+'/extract/index.json')
    old_audit, old_closure = frozen(OLD+'/audit/audit.json'), frozen(OLD+'/ALLOCATION-CLOSURE.json')
    radial_audit, radial_closure = frozen(RADIAL+'/audit/audit.json'), frozen(RADIAL+'/ALLOCATION-CLOSURE.json')
    need(old_audit['passed'] is True and old_audit['evidenceIntegrityPassed'] is True
         and old_audit['exactReferenceEquivalence'] is True and old_audit['selectedStages']==1920,
         'prior-selected-provenance-audit-passed')
    need(old_audit['sourcePartsScanned']==93 and old_audit['sourceJournalsScanned']==8,
         'prior-selection-provenance-scope')
    need(old_closure['allClosed'] is True and old_closure['transportIdentityVerified'] is True
         and old_closure['transportParts']==6, 'prior-selected-transport-closed')
    for phase in ('extract','producer','audit','finalize','ui'):
        c=old_closure['phases'][phase]
        need(c['closed'] is True and c['returncode']==0 and c['allocationWallPassed'] is True
             and c['outputCapPassed'] is True, 'prior-buffered-phase-closed')
    exact(identity(SOURCE_PINS[OLD+'/extract/index.json']), old_audit['extractionIndexPin'], 'prior-audited-extraction-index')
    exact(identity(extraction['selectedPin']), old_audit['filePins'][OLD+'/extract/selected.jsonl.gz'], 'prior-audited-compressed-selection')
    need(transport['complete'] is True and transport['nativeQueries']==0 and extraction['complete'] is True
         and extraction['selected']==1920 and extraction['nativeQueries']==0, 'complete-immutable-selected-archive')
    exact(extraction['windows'], WINDOWS, 'fixed-selected-windows')
    exact(identity(transport['original']), identity(extraction['selectedPin']), 'transport-original-selected-identity')
    need(extraction['selectedPin']['file']=='selected.jsonl.gz' and extraction['selectedPin']['bytes']==194862495
         and extraction['selectedPin']['sha256']=='b0d833c23eb6e81c2aa600ef82b2e344587762775a07c412a198d49fc2a56dfa',
         'fixed-selected-compressed-identity')
    need(len(transport['parts'])==6, 'exact-six-selected-transport-parts')
    offset=0
    for i,part in enumerate(transport['parts']):
        need(part['file']=='selected.jsonl.gz.part'+str(i).zfill(3) and part['offset']==offset, 'selected-part-order-offset')
        integer(part['bytes'],1,MAX_PART,'selected-part-size')
        relative=OLD+'/transport/'+part['file']
        exact(identity(SOURCE_PINS.get(relative)),identity(part),'selected-part-source-pin')
        exact(identity(old_public.get(relative)),identity(part),'selected-part-public-pin')
        offset+=part['bytes']
    need(offset==extraction['selectedPin']['bytes'],'selected-concatenated-size')
    need(radial_audit['passed'] is True and radial_audit['stages']==1920 and radial_audit['nativeCalls']==0
         and radial_audit['conditionalOnly'] is True and radial_audit['runtimeMappingProven'] is False
         and radial_audit['runtimeGeneralEquivalenceProven'] is False, 'prior-conditional-radial-audit')
    need(radial_closure['allClosed'] is True and radial_closure['scientificPassed'] is True
         and radial_closure['originalAllPassed'] is False and radial_closure['displayRecoveryPassed'] is True,
         'prior-radial-closure-retains-original-ui-failure')
    radial_report_pins={p['file']:p for p in radial_audit['filePins']}
    for name in radial_names:
        if name.startswith('results/'):
            exact(identity(SOURCE_PINS[RADIAL+'/'+name]),identity(radial_report_pins.get(name)),'prior-radial-audited-file')
    radial_summary=frozen(RADIAL+'/results/summary.json')
    exact(radial_summary,radial_audit['summary'],'prior-radial-summary-binding')
    need(radial_summary['sampleGate'] is True and radial_summary['controlGate'] is True
         and radial_summary['priorAggregateCountsMatch'] is True,'prior-radial-finite-gates')
    exact(identity(SOURCE_PINS.get(DENSITY+'/results/stages.jsonl')),identity(radial_audit['inputStagePin']),
          'prior-neighbor-stage-input-binding')
    for name in ('results/stages.jsonl','results/summary.json'):
        exact(identity(SOURCE_PINS.get(DENSITY+'/'+name)),identity(radial_public.get(DENSITY+'/'+name)),
              'prior-neighbor-public-pin')
    density_summary=frozen(DENSITY+'/results/summary.json')
    need(density_summary.get('stages')==1920,'prior-neighbor-stage-count')
    CHECKS.append('six-part selected archive bound to prior complete provenance audit/public result without reopening 93 original parts; radial classes/masks bound to passed finite audit and original failed UI history')
    return extraction,transport,radial_audit,{'oldResultCommit':old_receipt['commit'],
        'radialResultCommit':radial_receipt['commit'],'priorArchiveProvenanceReused':True,
        'originalSourcePartsRescanned':0,'selectedTransportParts':6,
        'priorDisplayProvenanceQualification':old_receipt['displayProvenanceQualification'],
        'priorRadialOriginalUiFailurePreserved':True}


def selected_reference(saved, neighbor):
    need(set(saved)=={'window','index','caseId','globalOrdinal','segment','localStageOrdinal',
                     'rawOffset','sourceLineSha256','sourceLineBytes','record'},'selected-envelope-fields')
    for name in ('segment','localStageOrdinal','rawOffset'):
        integer(saved[name],0,2**53-1,'selected-provenance-integer')
    integer(saved['sourceLineBytes'],1,MAX_RECORD,'original-line-size')
    need(type(saved['sourceLineSha256']) is str and SHA.fullmatch(saved['sourceLineSha256']),'original-line-hash')
    record=saved['record']
    need(set(record)=={'sequence','kind','body'} and record['kind']=='stage','selected-stage-envelope')
    integer(record['sequence'],0,2**53-1,'selected-source-sequence')
    body=record['body']; local=saved['localStageOrdinal']
    need(body['schema']=='m31-coupled-stage-v1' and body['arm']=='coupled','selected-stage-schema')
    need(body['stepIndex']==local//4 and body['stageIndex']==local%4+1
         and body['stageId']=='coupled-step'+str(local//4)+'-k'+str(local%4+1),'selected-stage-id')
    input_check(body['nativeInput'])
    native=body['native']
    need(native['schema']=='m31-native-load-evidence-v1' and native['model']=='ordinary-binary64-full-contribution'
         and native['method']=='F','archived-encoded-native-model')
    h=digest(compact(body['nativeInput']))
    need(native['caseId']==body['stageId'] and native['semanticInputSha256']==h
         and native['inlineInputCanonicalSha256']==h,'archived-adapter-annotation-binding')
    exact(native['ids'],list(range(64)),'archived-canonical-ids')
    exact(native['raw'],body['nativeInput']['drones'],'archived-raw-input-words')
    need(len(native['prepared'])==64,'archived-complete-prepared-states')
    for ident,drone in enumerate(body['nativeInput']['drones']):
        need(native['prepared'][ident]['id']==ident,'prepared-canonical-id')
        exact(native['prepared'][ident]['center'],drone['state'][:3],'prepared-center-input-words')
    status=native['status']
    need(status in ('native-success','domain-refused'),'selected-native-status')
    if status=='native-success':
        need(body['status']=='completed' and native['reason'] is None,'archived-success-status')
        need(len(native['solution'])==len(native['loads'])==64,'archived-complete-success')
    else:
        need(body['status']=='failed' and body['reason']=='native-non-success'
             and native['reason']=='native-admission' and native['stage']=='build','archived-inherited-build-refusal')
        need(native['diagnostics']['admission']['admitted'] is False
             and native['diagnostics']['admission']['reasons']==['near-field'],'archived-inherited-near-field')
        need(not any(k in native for k in ('loads','solution','consumption')),'refused-no-consumable-output')
    for name in ('window','index','caseId','globalOrdinal','sourceLineSha256'):
        exact(neighbor[name],saved[name],'neighbor-selected-provenance')
    exact(neighbor['ids'],native['ids'],'neighbor-identical-ids')
    positions=[[number(w) for w in d['state'][:3]] for d in body['nativeInput']['drones']]
    exact(neighbor['positions'],positions,'neighbor-identical-position-words')
    need(neighbor['timeWord']==body['originalTimeWord'] and word(neighbor['time'])==body['originalTimeWord'],
         'neighbor-identical-time-word')
    need(neighbor['status']==status and neighbor['reason']==native['reason'],'neighbor-identical-status-reason')
    exact(neighbor['nativeStage'],native.get('stage'),'neighbor-native-stage')
    exact(neighbor['admissionReasons'],native['diagnostics']['admission']['reasons'],'neighbor-refusal-reasons')
    return body,native,h,positions


def selection_audit(extraction,transport,radial_audit,binding,references):
    exact(binding['selectedPin'],extraction['selectedPin'],'producer-selected-binding')
    need(len(references)==1920,'complete-reference-table')
    neighbor_raw=checked(DENSITY+'/results/stages.jsonl',SOURCE_PINS[DENSITY+'/results/stages.jsonl'])
    radial_raw=checked(RADIAL+'/results/stages.jsonl',SOURCE_PINS[RADIAL+'/results/stages.jsonl'])
    neighbor_lines=neighbor_raw.splitlines(keepends=True); radial_lines=radial_raw.splitlines(keepends=True)
    need(len(neighbor_lines)==len(radial_lines)==1920 and all(x.endswith(b'\n') for x in neighbor_lines+radial_lines),
         'exact-previous-stage-line-inventory')
    classes=checked(RADIAL+'/results/classes.bin',SOURCE_PINS[RADIAL+'/results/classes.bin'])
    omitted=checked(RADIAL+'/results/omitted.bin',SOURCE_PINS[RADIAL+'/results/omitted.bin'])
    need(len(classes)==len(omitted)==1920*4032,'prior-pair-binary-size')
    witnesses={}
    witness_raw=checked(RADIAL+'/results/witnesses.jsonl',SOURCE_PINS[RADIAL+'/results/witnesses.jsonl'])
    for line in witness_raw.splitlines(keepends=True):
        need(line.endswith(b'\n') and len(line)<=MAX_RECORD,'prior-witness-line')
        witness=parse(line);ident=witness['id']
        need(ident not in witnesses,'unique-prior-build-id');witnesses[ident]=witness
    need(len(witnesses)==19,'fixed-prior-witness-inventory')
    zipped=b''.join(checked(OLD+'/transport/'+p['file'],p) for p in transport['parts'])
    need(len(zipped)==extraction['selectedPin']['bytes'] and digest(zipped)==extraction['selectedPin']['sha256'],
         'complete-selected-compressed-identity-before-decode')
    selected={}; refusals=[]; input_bindings=[]; reached_builds=set();counts_totals={}
    with gzip.GzipFile(fileobj=io.BytesIO(zipped),mode='rb') as stream:
        for ordinal in range(1920):
            line=bounded_line(stream,'selected');saved=parse(line);w,i=divmod(ordinal,160)
            exact([saved['window'],saved['index'],saved['caseId'],saved['globalOrdinal']],
                  [w,i,WINDOWS[w]['caseId'],WINDOWS[w]['start']+i],'fixed-selected-record-order')
            neighbor=parse(neighbor_lines[ordinal]);prior=parse(radial_lines[ordinal])
            need(neighbor['selectedRecordSha256']==digest(line),'whole-selected-envelope-byte-binding')
            body,native,h,positions=selected_reference(saved,neighbor)
            exact([prior['ordinal'],prior['window'],prior['index']],[ordinal,w,i],'radial-stage-order')
            need(prior['inputLineSha256']==digest(neighbor_lines[ordinal]) and prior['priorCountsEqual'] is True,
                 'radial-exact-neighbor-line-binding')
            cls=classes[ordinal*4032:(ordinal+1)*4032];mask=omitted[ordinal*4032:(ordinal+1)*4032]
            need(all(c in (0,1,2,3) for c in cls) and all(v in (0,1) for v in mask),'prior-class-mask-domains')
            need(all(not m or c in (0,2) for m,c in zip(mask,cls)),'prior-no-omitted-guard-or-eligible-pair')
            count={'logicalPairs':4032,'componentRejected':cls.count(0),'guardRejected':cls.count(1),
                   'radialRejected':cls.count(2),'centerEligible':cls.count(3),
                   'normCalls':4032-cls.count(0),'omittedPairs':mask.count(1),'falseOmissions':0}
            exact(prior['counts'],count,'prior-class-mask-stage-accounting')
            for key,value in count.items():counts_totals[key]=counts_totals.get(key,0)+value
            for key in ('logicalPairs','componentRejected','guardRejected','radialRejected','centerEligible'):
                need(neighbor['counts'][key]==count[key],'prior-neighbor-class-aggregate')
            pc=prior['cache'];build_id=pc['buildId']
            need(pc['action'] in ('build','reuse') and build_id in witnesses,'fixed-prior-data-cache-present')
            witness=witnesses[build_id]
            exact(witness['ids'],native['ids'],'prior-witness-canonical-ids')
            need(bytes(witness['omitted'])==mask and pc['omitted']==count['omittedPairs']
                 and pc['entries']==4032-count['omittedPairs'],'prior-witness-stage-mask-identity')
            if pc['action']=='build':
                need(i==0 and pc['reason']=='cold' and witness['context']=='window:'+str(w)+':index:'+str(i),
                     'fixed-prior-data-build-context')
                exact(witness['reference'],positions,'prior-build-reference-position-words')
                reached_builds.add(build_id)
            else:need(i>0 and pc['reason']=='contained','prior-contained-reuse')
            for point,box in zip(positions,witness['boxes']):
                need(len(box)==6 and all(number(box[2*k])<=point[k]<=number(box[2*k+1]) for k in range(3)),
                     'prior-stage-inclusive-box-containment')
            reference=references[ordinal]
            need(set(reference)=={'window','index','semantic'} and reference['window']==w and reference['index']==i,
                 'reference-exact-order-fields')
            semantic=compact(normalization(native))+b'\n';ref=reference['semantic']
            need(len(semantic)==ref['bytes'] and digest(semantic)==ref['sha256'],'independent-shared-reference-canonicalization')
            need(checked(cas_pin(ref,'semantic'),ref)==semantic,'full-shared-reference-canonical-bytes')
            added={path:rooted(native,path) for path in ADDED_EXCLUSIONS}
            for value in added.values():integer(value,0,4032,'archived-added-work-counter-type')
            strict=compact(normalization(native,exclusions=BASELINE_EXCLUSIONS))+b'\n'
            need(reinsert_work(parse(semantic),added)==strict,'reconstructed-nine-exclusion-baseline-canonical-bytes')
            baseline=count['normCalls'];candidate=sum(1 for c,m in zip(cls,mask) if c!=0 and not m)
            need(added[ADDED_EXCLUSIONS[0]]==added[ADDED_EXCLUSIONS[2]]==baseline
                 and added[ADDED_EXCLUSIONS[1]]==added[ADDED_EXCLUSIONS[3]]==4032-baseline,
                 'archived-baseline-actual-work-matches-prior-classes')
            diag=native['diagnostics']
            need(diag['screen']['eligible'] is True,'fixed-selected-global-screen-eligible')
            for path in ('diagnostics.geometryWork.gatheredNonselfCandidates','diagnostics.screen.orderedPairVisits',
                         'diagnostics.screen.componentTests'):
                integer(rooted(native,path),4032,4032,'archived-full-directed-enumeration')
            need(diag['geometryWork']['centerEligiblePairs']==count['centerEligible']
                 and diag['geometryWork']['centerGuardRejectedPairs']==count['guardRejected'],'archived-protected-center-work')
            selected[w,i]={'input':body['nativeInput'],'inputHash':h,'reference':ref,'baselineSha256':digest(strict),
                'baselineAdded':added,'status':native['status'],'reason':native['reason'],'positions':positions,
                'screenEligible':True,'hasBuildPhases':'buildPhasesMs' in diag,'priorCache':pc,
                'priorBoxes':witness['boxes'],'mask':mask,'classes':cls,'baselineNormCalls':baseline,
                'candidateNormCalls':candidate,'omittedCandidates':count['omittedPairs']}
            input_bindings.append({'window':w,'index':i,'caseId':saved['caseId'],'globalOrdinal':saved['globalOrdinal'],
                'segment':saved['segment'],'localStageOrdinal':saved['localStageOrdinal'],'sourceSequence':saved['record']['sequence'],
                'sourceLineSha256':saved['sourceLineSha256'],'sourceLineBytes':saved['sourceLineBytes'],'rawOffset':saved['rawOffset'],
                'selectedRecordSha256':digest(line),'nativeInputSha256':h,'positionWordsSha256':digest(compact([d['state'][:3] for d in body['nativeInput']['drones']])),
                'timeWord':body['originalTimeWord'],'status':native['status'],'reason':native['reason'],
                'nativeStage':native.get('stage'),'admissionReasons':diag['admission']['reasons'],
                'neighborLineSha256':digest(neighbor_lines[ordinal]),'radialLineSha256':digest(radial_lines[ordinal]),
                'priorBuildId':build_id,'classSliceSha256':digest(cls),'omissionSliceSha256':digest(mask),
                'sharedSemanticPin':ref,'strictBaselineSemanticSha256':digest(strict)})
            if native['status']!='native-success':refusals.append({'window':w,'index':i,'status':native['status'],
                'reason':native['reason'],'originalTimeWord':body['originalTimeWord']})
        need(stream.read(1)==b'','no-extra-selected-records')
    exact(refusals,extraction['refusals'],'identical-inherited-refusal')
    need(len(refusals)==1 and refusals[0]['window']==2 and refusals[0]['index']==159
         and refusals[0]['originalTimeWord']=='400cf5c28f5c28f6','fixed-inherited-near-field-trial')
    need(len(reached_builds)==12,'twelve-prior-data-builds')
    exact(counts_totals,radial_audit['summary']['totals'],'prior-complete-class-mask-aggregate-accounting')
    CHECKS.append('all 1920 complete selected envelopes bound to exact neighbor/radial lines, IDs/input/prepared centers/time/status/refusal, pair classes/masks and canonical scientific bytes; old nine-path baseline bytes reconstructed')
    return selected,refusals,input_bindings

def fresh_cache():
    return dict(counters={k:0 for k in COUNTERS},cached=None,
                last=dict(action='reset',reason=None,n=None,candidateEntries=0))


def cache_step(state,current):
    drones=sorted(current['drones'],key=lambda d:d['id'])
    ids=[d['id'] for d in drones]
    centers=[[number(v) for v in d['state'][:3]] for d in drones]
    n=len(ids);counts=state['counters'];counts['queries']+=1;cache=state['cached']
    def invalidate():
        if state['cached'] is not None:counts['invalidations']+=1
        state['cached']=None
    fallback=None
    if any(max(p[k] for p in centers)-min(p[k] for p in centers)>256 for k in range(3)):
        fallback='global-screen-ineligible'
    elif any(abs(v)>2**20 for p in centers for v in p):fallback='absolute-coordinate-bound'
    if fallback:
        counts['fallbacks']+=1;invalidate()
        state['last']=dict(action='fallback',reason=fallback,n=n,candidateEntries=0)
        return
    reason='cold'
    if cache is not None:
        reason='count-change' if len(cache['ids'])!=n else ('id-change' if cache['ids']!=ids else None)
        if reason:counts['identityRebuilds']+=1
        else:
            for i,center in enumerate(centers):
                for k,value in enumerate(center):
                    counts['containmentCoordinateTests']+=1
                    if not cache['boxes'][6*i+2*k]<=value<=cache['boxes'][6*i+2*k+1]:
                        reason='box-exit';counts['boxExitRebuilds']+=1;break
                if reason:break
        if reason is None:
            counts['reuses']+=1
            state['last']=dict(action='reuse',reason='all-current-centers-inside-stored-boxes',n=n,candidateEntries=cache['entries'])
            return
    invalidate()
    box_bits=exact_boxes(centers);mask,omissions=certificate_mask(box_bits)
    box_words=[format(v,'016x') for row in box_bits for v in row]
    rows=[[] for _ in ids];at=0
    for i in range(n):
        for j in range(n):
            if i==j:continue
            if not mask[at]:rows[i].append(ids[j])
            at+=1
    entries=n*(n-1)-omissions
    need(entries<=2000000,'candidate-entry-cap')
    counts['buildOrderedPairs']+=n*(n-1)
    counts['buildIntervalCoordinateTests']+=3*n*(n-1)
    state['cached']=dict(ids=ids,boxes=[number(x) for x in box_words],boxWords=box_words,
                         rows=rows,entries=entries,mask=bytes(mask))
    counts['builds']+=1
    state['last']=dict(action='build',reason=reason,n=n,candidateEntries=entries)


def expected_stats(state):
    cache=state['cached'];threshold=Fraction(3)+Fraction(1,1<<20)
    threshold_word=format(next_up(rn_bits(threshold*threshold)),'016x')
    limits=dict(halfWidth=.125,absoluteCoordinateLimit=2**20,maxCandidateEntries=2000000,
                screenThreshold=3,margin=2**-20,thresholdSquared=number(threshold_word),outwardEndpointUlps=1)
    return {**state['counters'],'cached':cache is not None,'cachedN':len(cache['ids']) if cache else 0,
            'cachedCandidateEntries':cache['entries'] if cache else 0,'last':state['last'],'limits':limits}


def witness_check(value,state,item):
    cache=state['cached']
    keys={'schema','cached','ids','boxes','rows','entries','last','boxEncoding'}|({'boxLayout'} if cache else set())
    need(set(value)==keys and value['schema']=='m31-radial-integration-witness-v1'
         and value['boxEncoding']=='binary64-be-hex','candidate-witness-schema')
    need(value['cached'] is (cache is not None),'candidate-witness-cache-presence')
    exact(value['last'],state['last'],'candidate-witness-last-event')
    if cache is None:
        need(value['ids']==value['boxes']==value['rows']==[] and value['entries']==0,'empty-fallback-witness')
        need(item['omittedCandidates']==0,'no-prior-omissions-on-fallback')
        return 0
    need(value['boxLayout']=='six words per canonical ID: xLo,xHi,yLo,yHi,zLo,zHi','candidate-box-layout')
    exact(value['ids'],cache['ids'],'candidate-witness-canonical-ids')
    exact(value['boxes'],cache['boxWords'],'candidate-exact-rational-box-words')
    exact(value['rows'],cache['rows'],'candidate-exact-complete-ordered-rows')
    integer(value['entries'],cache['entries'],cache['entries'],'candidate-entry-count')
    need(cache['mask']==item['mask'],'new-rational-mask-equals-exact-prior-stage-mask')
    need(cache['boxWords']==[w for row in item['priorBoxes'] for w in row],'new-rational-boxes-equal-prior-build-boxes')
    for i,point in enumerate(item['positions']):
        need(all(cache['boxes'][6*i+2*k]<=point[k]<=cache['boxes'][6*i+2*k+1] for k in range(3)),
             'every-candidate-current-inclusive-containment')
    prior=item['priorCache'];last=state['last']
    need(last['action']==prior['action'] and last['candidateEntries']==prior['entries'],'new-prior-cache-action-entry-agreement')
    need(last['reason']==('all-current-centers-inside-stored-boxes' if prior['reason']=='contained' else prior['reason']),
         'new-prior-cache-reason-agreement')
    return item['omittedCandidates']


def excluded_check(row,item,state):
    ex=row['excluded']
    keys={'method','timing','diagnostics.geometryWork.gatheredNonselfCandidates',
          'diagnostics.screen.orderedPairVisits','diagnostics.screen.componentTests'}|set(ADDED_EXCLUSIONS)
    if item['hasBuildPhases']:keys.add('diagnostics.buildPhasesMs')
    need(set(ex)==keys and ex['method']=='F','exact-present-new-evidence-exclusion-fields')
    timing=ex['timing']
    need(set(timing)=={'clock','totalMs','phasesMs','boundary'} and timing['clock']=='performance.now','native-timing-schema')
    need('complete load-word/ID/status consumption' in timing['boundary'],'native-complete-consumption-timing-boundary')
    need(0<=finite(timing['totalMs'])<=row['outerMs'],'native-total-inside-query-outer')
    phase_sum=0.0
    need(type(timing['phasesMs']) is dict,'native-phase-object')
    for value in timing['phasesMs'].values():phase_sum+=finite(value,True)
    need(abs(phase_sum-timing['totalMs'])<=max(1e-6,timing['totalMs']*1e-12),'native-phase-telescope')
    if item['hasBuildPhases']:
        need(type(ex['diagnostics.buildPhasesMs']) is dict,'build-phases-object')
        for value in ex['diagnostics.buildPhasesMs'].values():finite(value,True)
    gathered=4032 if state is None or state['cached'] is None else state['cached']['entries']
    for key in ('diagnostics.geometryWork.gatheredNonselfCandidates','diagnostics.screen.orderedPairVisits'):
        integer(ex[key],gathered,gathered,'actual-gathered-ordered-work')
    component=gathered if item['screenEligible'] else 0
    integer(ex['diagnostics.screen.componentTests'],component,component,'actual-component-test-work')
    actual=item['baselineNormCalls'] if state is None else item['candidateNormCalls']
    for key in (ADDED_EXCLUSIONS[0],ADDED_EXCLUSIONS[2]):
        integer(ex[key],actual,actual,'actual-center-call-counter-aliases')
    for key in (ADDED_EXCLUSIONS[1],ADDED_EXCLUSIONS[3]):
        integer(ex[key],4032-actual,4032-actual,'total-skipped-center-counter-aliases')
    if state is None:
        for key in ADDED_EXCLUSIONS:
            integer(ex[key],0,4032,'baseline-added-field-numeric-type')
            exact(ex[key],item['baselineAdded'][key],'baseline-added-field-exact-archive-equality')
        # selection_audit compared actual reconstructed canonical bytes for this
        # exact shared CAS plus these four values. Equal operands prove the same
        # bytes for each F call without storing duplicate complete CAS bodies.
        need(row['baselineReferenceEqual'] is True
             and row['baselineReferenceSha256']==row['baselineSemanticSha256']==item['baselineSha256'],
             'each-F-strict-nine-path-reference-binding')
    else:
        need(row['baselineReferenceEqual'] is None and row['baselineReferenceSha256'] is None
             and row['baselineSemanticSha256'] is None,'candidate-has-no-baseline-only-flags')
    return dict(logicalDirectedPairs=4032,gatheredNonselfCandidates=gathered,
                componentTests=component,actualCenterNormCalls=actual,
                skippedCenterNormCalls=4032-actual,
                omittedCandidates=0 if state is None else item['omittedCandidates'],
                actualCenterCallsAvoidedVersusF=0 if state is None else item['baselineNormCalls']-actual)


def query_audit(items,saved_groups,saved_summary):
    queries=line_records(jsonl_capture('results/queries.jsonl'))
    need(len(saved_groups)==108,'complete-group-count')
    witnesses,witness_refs={},{};coverage=dict(builds=0,reuses=0,boxExitRebuilds=0,fallbacks=0)
    work_keys=['logicalDirectedPairs','gatheredNonselfCandidates','componentTests','actualCenterNormCalls',
               'skippedCenterNormCalls','omittedCandidates','actualCenterCallsAvoidedVersusF']
    work_totals={phase:{method:{'calls':0,'admittedCalls':0,'refusedCalls':0,**{k:0 for k in work_keys}}
                        for method in ('F','C')} for phase in ('warmup','measured')}
    counts=dict(queries=0,candidateWitnesses=0,referenceComparisons=0,baselineStrictChecks=0,
                admittedQueries=0,refusedQueries=0,omittedCurrentPairsChecked=0,
                cacheStepsIndependentlyReconstructed=0,warmupQueries=0,measuredQueries=0,
                rationalBuildsReconstructed=0,rationalBuildOrderedPairs=0)
    row_keys={'call','window','rep','method','index','semantic','referenceSha256','referenceEqual',
        'comparisonMs','inputBeforeSha256','inputAfterSha256','inputPreserved','outerMs','status','reason',
        'cache','witness','excluded','encodePersistMs','methodValid','afterInput','baselineReferenceEqual',
        'baselineReferenceSha256','baselineSemanticSha256'}
    groups=[];representative={};call=0
    for rep in range(-1,8):
        phase='warmup' if rep==-1 else 'measured'
        for window in range(12):
            order=['F','C'] if (rep+window+10)%2==0 else ['C','F']
            saved_group=saved_groups[(rep+1)*12+window]
            need(set(saved_group)=={'window','rep','order','F','C','ratio'},'group-fields')
            exact([saved_group['window'],saved_group['rep'],saved_group['order']],[window,rep,order],'group-schedule')
            group=dict(window=window,rep=rep,order=order)
            for method in order:
                reset_ms=finite(saved_group[method]['resetMs'],True)
                aggregate=dict(resetMs=reset_ms,sumQueryMs=0.0,totalMs=reset_ms,admittedMs=0.0,
                               refusedMs=0.0,admittedCalls=0,refusedCalls=0)
                state=fresh_cache() if method=='C' else None
                for index in range(160):
                    tick();call+=1;row=next(queries,None)
                    need(type(row) is dict and set(row)==row_keys,'query-row-exact-fields')
                    exact([row[k] for k in ('call','window','rep','method','index')],
                          [call,window,rep,method,index],'complete-query-schedule')
                    item=items[window,index]
                    exact(row['semantic'],item['reference'],'each-call-full-shared-scientific-CAS')
                    need(row['referenceEqual'] is True and row['referenceSha256']==item['reference']['sha256'],
                         'each-call-scientific-reference-equality')
                    need(row['methodValid'] is True and row['afterInput'] is None,'each-call-method-and-no-mutation')
                    need(row['inputPreserved'] is True and row['inputBeforeSha256']==row['inputAfterSha256']==item['inputHash'],
                         'each-call-exact-full-input-word-binding')
                    need(row['status']==item['status'] and row['reason']==item['reason'],'each-call-inherited-outcome')
                    finite(row['outerMs'],True);finite(row['encodePersistMs'],True);finite(row['comparisonMs'],True)
                    need(row['comparisonMs']<=row['encodePersistMs'],'common-comparison-inside-encoding-overhead')
                    if method=='C':
                        # The inherited refusal occurs after build enumeration.
                        cache_step(state,item['input'])
                        exact(row['cache'],expected_stats(state),'every-cache-state-and-counter')
                        ref=row['witness'];relative=cas_pin(ref,'witness')
                        if ref['sha256'] not in witnesses:
                            witnesses[ref['sha256']]=parse(checked(relative,ref));witness_refs[ref['sha256']]=dict(ref)
                        else:exact(ref,witness_refs[ref['sha256']],'deduplicated-witness-pin')
                        counts['omittedCurrentPairsChecked']+=witness_check(witnesses[ref['sha256']],state,item)
                        counts['candidateWitnesses']+=1;counts['cacheStepsIndependentlyReconstructed']+=1
                        action=state['last']['action']
                        if action=='build':
                            counts['rationalBuildsReconstructed']+=1
                            counts['rationalBuildOrderedPairs']+=4032
                        if rep>=0:
                            coverage['builds']+=int(action=='build');coverage['reuses']+=int(action=='reuse')
                            coverage['boxExitRebuilds']+=int(action=='build' and state['last']['reason']=='box-exit')
                            coverage['fallbacks']+=int(action=='fallback')
                    else:
                        need(row['cache'] is None and row['witness'] is None,'baseline-no-candidate-cache-witness')
                        counts['baselineStrictChecks']+=1
                    work=excluded_check(row,item,state)
                    totals=work_totals[phase][method];totals['calls']+=1
                    admitted=row['status']=='native-success'
                    totals['admittedCalls' if admitted else 'refusedCalls']+=1
                    for key,value in work.items():totals[key]+=value
                    if rep==0:
                        representative.setdefault((window,index),{})[method]={
                            'normCalls':work['actualCenterNormCalls'],'omittedCandidates':work['omittedCandidates'],
                            'cacheAction':row['cache']['last']['action'] if method=='C' else None,
                            'status':row['status'],'referenceEqual':row['referenceEqual']}
                    aggregate['sumQueryMs']+=row['outerMs'];aggregate['totalMs']+=row['outerMs']
                    aggregate['admittedMs' if admitted else 'refusedMs']+=row['outerMs']
                    aggregate['admittedCalls' if admitted else 'refusedCalls']+=1
                    counts['admittedQueries' if admitted else 'refusedQueries']+=1
                    counts['warmupQueries' if rep==-1 else 'measuredQueries']+=1
                    counts['referenceComparisons']+=1;counts['queries']+=1
                need(aggregate['totalMs']>0,'positive-stream-duration')
                exact(saved_group[method],aggregate,'exact-reset-inclusive-status-partition-timing')
                group[method]=aggregate
            group['ratio']=group['C']['totalMs']/group['F']['totalMs']
            exact(saved_group,group,'exact-complete-group-arithmetic');groups.append(group)
    need(next(queries,None) is None and call==34560,'no-missing-or-extra-query')
    need(counts['admittedQueries']==34542 and counts['refusedQueries']==18 and counts['warmupQueries']==3840
         and counts['measuredQueries']==30720 and counts['candidateWitnesses']==counts['baselineStrictChecks']==17280,
         'full-query-refusal-warmup-measured-coverage')
    reps=[]
    for rep in range(8):
        f,c=0.0,0.0
        for group in groups:
            if group['rep']==rep:f+=group['F']['totalMs'];c+=group['C']['totalMs']
        reps.append(dict(rep=rep,F=f,C=c,ratio=c/f))
    ratios=sorted(r['ratio'] for r in reps);median=(ratios[3]+ratios[4])/2
    wins=sum(r['C']<r['F'] for r in reps)
    coverage_gate=coverage['reuses']>0 and coverage['boxExitRebuilds']>0
    cost_gate=median<=.9 and wins>=7
    summary=dict(complete=True,calls=call,referenceEquality=True,reps=reps,medianRatio=median,strictWins=wins,
        coverage=coverage,coverageGate=coverage_gate,costGate=cost_gate,keepGate=cost_gate and coverage_gate,
        runtimeGeneralEquivalenceProven=False,performanceMeasured=True,stages=1920,scope=SCOPE)
    need(set(saved_summary)==set(summary)|{'readEvents','wallSeconds'},'summary-exact-fields')
    exact({k:saved_summary[k] for k in summary},summary,'independent-summary-fixed-gates')
    need(type(saved_summary['readEvents']) is list and 0<=finite(saved_summary['wallSeconds'])<=1800,'producer-summary-budget-read-history')
    summary.update(readEvents=saved_summary['readEvents'],wallSeconds=saved_summary['wallSeconds'])
    viewer=[]
    need(len(representative)==1920,'complete-representative-pair-table')
    for window in range(12):
        for index in range(160):
            pair=representative[window,index]
            need(set(pair)=={'F','C'} and pair['F']['status']==pair['C']['status'],'representative-paired-current-status')
            viewer.append(dict(window=window,index=index,baselineNormCalls=pair['F']['normCalls'],
                candidateNormCalls=pair['C']['normCalls'],omittedCandidates=pair['C']['omittedCandidates'],
                cacheAction=pair['C']['cacheAction'],status=pair['C']['status'],
                referenceEqual=pair['F']['referenceEqual'] and pair['C']['referenceEqual']))
    CHECKS.append('all 34560 scientific reference matches, 17280 stricter F comparisons and candidate cache steps; every actual work counter and all 18 inherited refusal replays checked')
    CHECKS.append('all 108 reset-inclusive groups, eight aggregate ratios/median/strict wins and unchanged cost/motion-coverage gates reconstructed in source order; 1920 rep-zero viewer rows derived from saved paired calls')
    return summary,counts,witness_refs,work_totals,viewer

def inventory(producer_exit,items,witness_refs):
    expected={'launch.lock','input-binding.json','environment.json','references.json',
              'queries.jsonl','groups.jsonl','summary.json','exit.json'}
    expected.update(item['reference']['file'] for item in items.values())
    expected.update(ref['file'] for ref in witness_refs.values())
    files=list((BASE/'results').iterdir())
    need({p.name for p in files}==expected,'exact-producer-result-inventory')
    total,before_exit=0,0
    for path in files:
        need(path.is_file() and not path.is_symlink(),'regular-producer-result-file')
        relative=path.relative_to(ROOT).as_posix()
        if relative not in PINS:
            need(path.name=='launch.lock','unverified-produced-file')
            raw=path.read_bytes()
            need(raw==b'single bounded native replay\n','producer-single-use-launch-record')
            PINS[relative]={'bytes':len(raw),'sha256':digest(raw)}
        total+=PINS[relative]['bytes']
        if path.name!='exit.json':before_exit+=PINS[relative]['bytes']
    need(total<=MAX_INPUT and producer_exit['bytesWritten']==before_exit,'producer-exact-pre-exit-payload-accounting')
    CHECKS.append('complete lossless semantic/witness/result inventory and pre-exit byte accounting; source and consumed artifact identities rechecked before successful report')
    return total


def audit():
    publication,manifest_pin,publication_pin,dependencies=source_gate()
    extraction,transport,radial_audit,source_evidence=prior_gate()
    producer_exit=closure_gate('producer')
    binding,_=capture('results/input-binding.json',MAX_RECORD)
    environment,_=capture('results/environment.json',MAX_RECORD)
    references,_=capture('results/references.json')
    saved_summary,_=capture('results/summary.json',MAX_RECORD)
    saved_groups=list(line_records(jsonl_capture('results/groups.jsonl')))
    exact(binding['extractionIndex'],identity(SOURCE_PINS[OLD+'/extract/index.json']),'producer-extraction-index-identity')
    need(set(binding)=={'extractionIndex','selectedPin','sourceCommit','manifestSha256'},'input-binding-fields')
    need(binding['sourceCommit']==environment['sourceCommit']==publication['commit']
         and binding['manifestSha256']==manifest_pin['sha256'],'producer-reviewed-source-binding')
    runtime=frozen(REL+'/runtime.json')
    need(environment['node']==runtime['nodeVersion']=='v24.19.0','producer-pinned-node-version')
    need(producer_exit['calls']==34560 and producer_exit['readEvents']==saved_summary['readEvents'],'producer-closed-call-read-history')
    items,refusals,input_bindings=selection_audit(extraction,transport,radial_audit,binding,references)
    summary,counts,witnesses,work_totals,viewer=query_audit(items,saved_groups,saved_summary)
    output_bytes=inventory(producer_exit,items,witnesses)
    # Identity rereads only; no second selected decompression or original scan.
    for relative,pin in list(PINS.items()):checked(relative,pin)
    tick()
    result_pins=[{'file':relative[len(REL)+1:],**pin} for relative,pin in sorted(PINS.items())
                 if relative.startswith(REL+'/results/') or relative==REL+'/producer-supervisor.json']
    report={'schema':'m31-radial-integration-audit-v1','passed':True,
        'evidenceIntegrityPassed':True,'exactReferenceEquivalence':True,
        'baselineStrictReferenceEquivalence':True,'candidateCertificateReconstructionPassed':True,
        'conditionalOnly':True,'runtimeGeneralEquivalenceProven':False,'runtimeMappingProven':False,
        'performanceMeasured':True,'stages':1920,'calls':34560,'nativeCalls':0,
        'nativeQueriesByAudit':0,'hypotCallsByAudit':0,'checks':CHECKS,'summary':summary,
        'sourceCommit':publication['commit'],'sourceManifestPin':manifest_pin,
        'sourcePublicationPin':publication_pin,'sourceEvidence':source_evidence,
        'selectedArchivePin':extraction['selectedPin'],'selectedTransportPins':transport['parts'],
        'extractionIndexPin':identity(SOURCE_PINS[OLD+'/extract/index.json']),
        'inputBindings':input_bindings,'selectedRefusals':refusals,'counts':counts,
        'workTotals':work_totals,
        'workTotalsSchema':{'partition':'warmup rep -1 and measured reps 0..7; each has F and C arms',
            'units':'integer directed pair instances and calls accumulated over every saved query, including refusals',
            'actualCenterNormCalls':'saved current actual counter, independently derived from prior retained class!=0 slots',
            'skippedCenterNormCalls':'logical directed pairs minus actual norm calls, including component skips',
            'omittedCandidates':'cache mask omissions; F has zero; may overlap earlier component rejection',
            'actualCenterCallsAvoidedVersusF':'F actual norms minus C actual norms at identical inputs; F has zero'},
        'baselineStrictChecks':{'calls':counts['baselineStrictChecks'],'canonicalByteReconstructions':1920,
            'scope':'old nine-path canonical bytes reconstructed from each verified shared CAS and archived four counters, then exact same CAS and four numeric values plus both strict hashes checked for every F call'},
        'producerOutputBytes':output_bytes,'filePins':result_pins,
        'sourcePins':[SOURCE_PINS[p] for p in sorted(SOURCE_PINS)],
        'consumedPins':[{'path':p,**pin} for p,pin in sorted(PINS.items())],
        'rendererPins':[SOURCE_PINS[p] for p in sorted(SOURCE_PINS) if '/vendor/three.' in p or p.endswith('/vendor/OrbitControls.js')],
        'staticDependencyClosure':dependencies,'readEvents':READ_EVENTS,
        'producerReadEvents':saved_summary['readEvents'],'priorExtractionReadEvents':extraction['readEvents'],
        'normalizationExclusions':EXCLUSIONS,'baselineNormalizationExclusions':BASELINE_EXCLUSIONS,
        'normalizationScope':'all comparands encoded evidence-v1; sorted rooted exact binary64 words, arrays/strings/null/nonfinite wrappers preserved; method and archived adapter bindings checked separately',
        'certificateScope':'each candidate build independently reconstructed with integer-ratio RN-even arithmetic; every cache lifecycle/counter/box/row checked, tied to fixed prior finite class/mask evidence',
        'arithmeticDisclosure':'certificate operations use exact ratios and explicit gradual-underflow handling; current global-span and timing sums use Python IEEE binary64, no norm or native model recomputed',
        'implementationDisclosure':'identity/normalization/query-timing architecture adapted as source text from buffered-motion auditor; exact-ratio routines reused as source text from radial-certificate auditor; no auditor or scientific module imported',
        'timingScope':'same-process instrumented complete-query replay; reset/query and owned input copy in primary time; F-only old-nine normalization/comparison and C-only witness copying outside may influence later runtime; comparisonMs covers common thirteen-path comparison only; encodePersistMs excludes its own row append',
        'limitations':['conditional arithmetic theorem remains unbound to all installed runtime paths',
            'fixed previously exposed N64 samples are dependent, not holdout or universal evidence',
            'prior intrinsic class words are reused as audited input evidence, not recomputed by this auditor',
            'no original 93-part scan, new synthetic controls, new integrated trajectory or physical validation',
            'known short-window lack of motion rebuild remains failed coverage; gate definitions are unchanged',
            'actual omitted norm work is separate from total query cost and from proposed candidate omissions',
            'only Node executable is pinned; Python/browser/environment are not a hermetic runtime'],
        'physicalValidity':False,'flightSafetyClaim':False,'statisticalInference':False,
        'largeSwarmSpeedClaim':False,'researchComplete':False}
    return report,viewer


def main():
    global START
    START=time.monotonic()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'),'optimized-audit-not-permitted')
    need((BASE/'audit-supervisor-launch.lock').is_file(),'audit-supervisor-allocation-required')
    out=BASE/'audit';need(not out.is_symlink(),'audit-output-symlink');out.mkdir()
    def save(name,value):
        raw=compact(value)+b'\n'
        need(sum(p.stat().st_size for p in out.iterdir())+len(raw)+16384<=MAX_OUTPUT,'audit-output-budget')
        with (out/name).open('xb') as stream:stream.write(raw)
    save('launch.json',{'schema':'m31-radial-integration-audit-launch-v1',
        'startedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,
        'maxWallSeconds':MAX_SECONDS,'maxOutputBytes':MAX_OUTPUT,'scope':'saved evidence only; no native/model/hypot calls'})
    code=0
    try:
        report,viewer=audit();raw=compact(viewer)+b'\n'
        report['viewerRowsPin']={'file':'audit/viewer-rows.json','bytes':len(raw),'sha256':digest(raw)}
        report['wallSeconds']=time.monotonic()-START
        need(len(raw)+len(compact(report))+32768<=MAX_OUTPUT,'combined-audit-output-budget')
        save('viewer-rows.json',viewer);tick();save('audit.json',report);tick()
    except Exception as error:
        code=1;name='failure.json' if (out/'audit.json').exists() else 'audit.json'
        save(name,{'schema':'m31-radial-integration-audit-v1','passed':False,'evidenceIntegrityPassed':False,
            'allocation':'closed-no-rerun','failure':type(error).__name__+': '+str(error).replace(str(ROOT),'[repository]')[:1500],
            'checksCompleted':CHECKS,'readEvents':READ_EVENTS,'wallSeconds':time.monotonic()-START})
    save('exit.json',{'closed':True,'exitCode':code,'wallSeconds':time.monotonic()-START})
    return code


if __name__=='__main__':
    sys.exit(main())
