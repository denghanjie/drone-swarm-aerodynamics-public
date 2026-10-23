"""Saved-only radial-certificate audit. Execute only after reviewed public freeze.

Standard-library read/JSON helpers are reused textually from the previous audit;
certificate, control, lifecycle and per-pair verification are independently authored.
No producer, candidate, scientific or previous-auditor module is imported.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import datetime
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
REL = 'research/m31-radial-certificate-2026-10-23'
OLD = 'research/m31-neighbor-density-2026-10-23'
INPUT_COMMIT = 'a38234d150bcdecb50e3c4615e07dc8703039397'
RECEIPT_COMMIT = '33e31e09cb4e40388f3677495aa71f33230e673e'
RECEIPT_PATH = 'research/publication-receipts/m31-neighbor-density-result-2026-10-23.json'
SUPPLEMENTS = {'research/publication-receipts/m31-neighbor-density-result-public-review-2026-10-23.json',
               'research/publication-receipts/m31-neighbor-density-result-public-review-2026-10-23.md'}
PROOF_INPUTS = {'research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs',
                'research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs'}
MAX_SECONDS = 900
MAX_OUTPUT = 16*1024**2
MAX_RESULT = 128*1024**2
MAX_METADATA = 32*1024**2
MAX_PART = 128*1024**2
MAX_RECORD = 8*1024**2
START = None
READ_EVENTS = []
CHECKS = []
SOURCE_PINS = {}
INPUT_PINS = {}
CONSUMED_PINS = {}
COMMITTED = {}
SIGN = 1 << 63
FRACTION_MASK = (1 << 52)-1
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


@lru_cache(maxsize=131072)
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


def global_eligible(positions):
    # Explicitly ordinary Python binary64 subtraction, matching the frozen
    # basic-op screen contract. This is not an independent Math.hypot oracle.
    for axis in range(3):
        values = [point[axis] for point in positions]
        if not all(type(value) in (int, float) and math.isfinite(value) for value in values):
            return False
        span = max(values)-min(values)
        if not math.isfinite(span) or not 0 <= span <= 256:
            return False
    return True


def verify_pair_data(positions, norm_words, classes, omitted):
    n = len(positions)
    expected_slots = n*(n-1)
    need(len(norm_words) == len(classes) == len(omitted) == expected_slots, 'complete-pair-array-widths')
    screen = global_eligible(positions)
    counts = {'logicalPairs': expected_slots, 'componentRejected': 0, 'guardRejected': 0,
              'radialRejected': 0, 'centerEligible': 0, 'normCalls': 0,
              'omittedPairs': 0, 'falseOmissions': 0}
    index = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # These three rounded subtractions are deliberately the only
            # floating geometry replay in this verifier; no norm is computed.
            dx = positions[j][0]-positions[i][0]
            dy = positions[j][1]-positions[i][1]
            dz = positions[j][2]-positions[i][2]
            maximum = max(abs(dx), abs(dy), abs(dz))
            bits = norm_words[index]
            norm = struct.unpack('>d', bits.to_bytes(8, 'big'))[0]
            if screen and maximum >= 4:
                expected = 0
                need(bits == 0, 'uncalled-norm-positive-zero-sentinel')
                counts['componentRejected'] += 1
            else:
                counts['normCalls'] += 1
                if not math.isfinite(norm) or norm > 512 or maximum > 257:
                    expected = 1
                    counts['guardRejected'] += 1
                elif norm >= 3:
                    expected = 2
                    counts['radialRejected'] += 1
                else:
                    need(norm >= 0, 'nonnegative-finite-recorded-hypot')
                    expected = 3
                    counts['centerEligible'] += 1
            need(type(classes[index]) is int and classes[index] == expected, 'recorded-current-baseline-class')
            need(type(omitted[index]) is int and omitted[index] in (0, 1), 'omission-bit-domain')
            counts['omittedPairs'] += omitted[index]
            counts['falseOmissions'] += int(bool(omitted[index]) and expected not in (0, 2))
            index += 1
    need(counts['normCalls']+counts['componentRejected'] == expected_slots, 'actual-hypot-call-accounting')
    return counts


class CacheVerifier:
    def __init__(self, witnesses):
        self.witnesses = witnesses
        self.used = 0
        self.cached = None
        self.certificate_pairs = 0
        self.certificate_omissions = 0
        self.contained_coordinates = 0

    def reset(self):
        self.cached = None

    def step(self, ids, positions, context):
        need(type(ids) is list and type(positions) is list and 2 <= len(ids) <= 64
             and len(positions) == len(ids), 'cache-input-shape')
        for i, ident in enumerate(ids):
            integer(ident)
            need(i == 0 or ids[i-1] < ident, 'canonical-cache-ids')
            need(type(positions[i]) is list and len(positions[i]) == 3, 'cache-position-width')
            for value in positions[i]:
                finite(value)
        pairs = len(ids)*(len(ids)-1)
        if not global_eligible(positions) or any(abs(value) > 1 << 20 for point in positions for value in point):
            self.cached = None
            return {'action': 'fallback', 'reason': 'coordinate-domain', 'buildId': None,
                    'entries': pairs, 'omitted': 0}, [0]*pairs
        reason = 'cold'
        if self.cached:
            if len(self.cached['ids']) != len(ids):
                reason = 'count-change'
            elif self.cached['ids'] != ids:
                reason = 'id-change'
            else:
                reason = None
                for i, point in enumerate(positions):
                    for axis, value in enumerate(point):
                        # Inclusive comparisons are exact order comparisons of
                        # finite binary64 values; they do not evaluate a norm.
                        lower, upper = self.cached['floatBoxes'][i][2*axis:2*axis+2]
                        self.contained_coordinates += 1
                        if not lower <= value <= upper:
                            reason = 'box-exit'
                            break
                    if reason:
                        break
        if reason is None:
            count = self.cached['omittedCount']
            return {'action': 'reuse', 'reason': 'contained', 'buildId': self.cached['id'],
                    'entries': pairs-count, 'omitted': count}, self.cached['mask']
        self.cached = None
        boxes = exact_boxes(positions)
        mask, count = certificate_mask(boxes)
        self.certificate_pairs += pairs
        self.certificate_omissions += count
        self.used += 1
        need(self.used <= len(self.witnesses), 'missing-build-witness')
        expected = {'id': self.used, 'context': context, 'ids': ids, 'reference': positions,
                    'boxes': [[format(bits, '016x') for bits in row] for row in boxes], 'omitted': mask}
        exact(self.witnesses[self.used-1], expected, 'complete-independent-build-witness')
        self.cached = {'id': self.used, 'ids': ids[:], 'mask': mask, 'omittedCount': count,
                       'floatBoxes': [[struct.unpack('>d', bits.to_bytes(8, 'big'))[0] for bits in row] for row in boxes]}
        return {'action': 'build', 'reason': reason, 'buildId': self.used, 'entries': pairs-count,
                'omitted': count}, mask


def control_specs():
    def raised(value, steps=1):
        bits = float_bits(value)
        for _ in range(steps):
            bits = next_up(bits)
        return struct.unpack('>d', bits.to_bytes(8, 'big'))[0]
    return [([0, 1], [0, 3.5], 'build', 2),
            ([0, 1], [.02, 3.48], 'reuse', 2),
            ([0, 1], [.30, 3.20], 'build', 0),
            ([0, 2], [.30, 3.20], 'build', 0),
            ([0, 2, 3], [.30, 3.20, 7], 'build', None),
            ([0, 1], [(1 << 20)+4, (1 << 20)+7.5], 'fallback', 0),
            ([0, 1], [0, 3.5], 'build', 2),
            ([0, 1], [raised(.125), raised(3.625)], 'reuse', 2),
            ([0, 1], [raised(.125, 2), raised(3.625)], 'build', 2),
            ([0, 1], [0, 3], 'build', 0)]


def audit_controls(controls, partial, cache):
    need(type(controls) is list and len(controls) == 10 and len(partial) == 10, 'exact-ten-controls')
    calls = 0
    coverage = {'build': 0, 'reuse': 0, 'fallback': 0}
    for index, (ids, coordinates, action, expected_omitted) in enumerate(control_specs()):
        tick()
        positions = [[x, 0, 0] for x in coordinates]
        saved = controls[index]
        need(set(saved) == {'id', 'ids', 'positions', 'expectedAction', 'expectedOmitted', 'cache',
                            'counts', 'norms', 'classes', 'omitted'}, 'control-fields')
        exact({key: saved[key] for key in ('id', 'ids', 'positions', 'expectedAction', 'expectedOmitted')},
              {'id': index, 'ids': ids, 'positions': positions, 'expectedAction': action,
               'expectedOmitted': expected_omitted}, 'fixed-control-input-and-expectation')
        expected_cache, mask = cache.step(ids, positions, 'control:'+str(index))
        exact(saved['cache'], expected_cache, 'control-lifecycle')
        exact(saved['omitted'], mask, 'control-certificate-mask')
        counts = verify_pair_data(positions, [word_bits(x) for x in saved['norms']], saved['classes'], saved['omitted'])
        exact(saved['counts'], counts, 'control-counts')
        need(expected_cache['action'] == action and counts['falseOmissions'] == 0, 'control-action-and-no-false-omission')
        if expected_omitted is not None:
            need(counts['omittedPairs'] == expected_omitted, 'fixed-control-omission-expectation')
        exact(partial[index], saved, 'incremental-control-preservation')
        calls += counts['normCalls']
        coverage[action] += 1
    CHECKS.append('all ten fixed controls, exact IDs/positions/actions/masks, threshold/endpoint/fallback cases and incremental preserved rows checked')
    return calls, coverage


def json_lines(raw, maximum=MAX_RECORD):
    need(raw.endswith(b'\n'), 'newline-terminated-jsonl')
    source = io.BytesIO(raw)
    while True:
        line = source.readline(maximum+1)
        if not line:
            break
        need(len(line) <= maximum and line.endswith(b'\n'), 'bounded-jsonl-line')
        yield line, parse(line)


def audit_stages(prior_raw, stage_raw, norms, classes, omitted, cache):
    need(len(norms) == 61931520 and len(classes) == len(omitted) == 7741440,
         'complete-stage-major-binary-lengths')
    source_rows = iter(json_lines(prior_raw))
    saved_rows = iter(json_lines(stage_raw))
    totals = {key: 0 for key in ('logicalPairs', 'componentRejected', 'guardRejected', 'radialRejected',
                                'centerEligible', 'normCalls', 'omittedPairs', 'falseOmissions')}
    events = {'build': 0, 'reuse': 0, 'fallback': 0}
    reasons = {}
    refusals = []
    stage_metadata = []
    for ordinal in range(1920):
        tick()
        window, index = divmod(ordinal, 160)
        original = next(source_rows, None)
        saved_pair = next(saved_rows, None)
        need(original is not None and saved_pair is not None, 'complete-source-and-result-stage-schedule')
        line, prior = original
        saved = saved_pair[1]
        need(set(prior) == {'window', 'index', 'caseId', 'globalOrdinal', 'sourceLineSha256',
                           'selectedRecordSha256', 'timeWord', 'time', 'status', 'reason', 'nativeStage',
                           'admissionReasons', 'ids', 'positions', 'counts', 'symbols'}, 'complete-prior-audited-row')
        exact([prior['window'], prior['index'], prior['caseId'], prior['globalOrdinal']],
              [window, index, WINDOWS[window]['caseId'], WINDOWS[window]['start']+index], 'fixed-source-stage-provenance')
        exact(prior['ids'], list(range(64)), 'fixed-source-canonical-IDs')
        need(word(prior['time']) == prior['timeWord'] and len(prior['symbols']) == 12, 'prior-time-and-symbol-record')
        for key in ('sourceLineSha256', 'selectedRecordSha256'):
            need(re.fullmatch('[0-9a-f]{64}', prior[key]), 'prior-stage-journal-identity')
        if prior['status'] == 'native-success':
            need(prior['reason'] is None and prior['nativeStage'] is None and prior['admissionReasons'] == [], 'prior-success-preserved')
        else:
            need((window, index) == (2, 159) and prior['status'] == 'domain-refused'
                 and prior['reason'] == 'native-admission' and prior['nativeStage'] == 'build'
                 and prior['admissionReasons'] == ['near-field'], 'inherited-refusal-preserved')
            refusals.append({key: prior[key] for key in ('window', 'index', 'caseId', 'globalOrdinal', 'timeWord',
                                                       'status', 'reason', 'nativeStage', 'admissionReasons')})
        if index == 0:
            cache.reset()
        expected_cache, mask = cache.step(prior['ids'], prior['positions'], 'window:'+str(window)+':index:'+str(index))
        at = ordinal*4032
        pair_omitted = omitted[at:at+4032]
        need(pair_omitted == bytes(mask), 'every-stage-certificate-mask')
        pair_classes = classes[at:at+4032]
        pair_norms = struct.unpack_from('<4032Q', norms, at*8)
        counts = verify_pair_data(prior['positions'], pair_norms, pair_classes, pair_omitted)
        equal = all(counts[key] == integer(prior['counts'][key]) for key in
                    ('logicalPairs', 'componentRejected', 'guardRejected', 'radialRejected', 'centerEligible'))
        equal = equal and counts['normCalls'] == integer(prior['counts']['componentSurvivors'])
        expected = {'ordinal': ordinal, 'window': window, 'index': index, 'inputLineSha256': digest(line),
                    'cache': expected_cache, 'counts': counts, 'priorCountsEqual': equal}
        exact(saved, expected, 'complete-independent-stage-row')
        need(equal and counts['falseOmissions'] == 0, 'finite-current-omission-and-historical-aggregate-gates')
        for key in totals:
            totals[key] += counts[key]
        events[expected_cache['action']] += 1
        reasons[expected_cache['reason']] = reasons.get(expected_cache['reason'], 0)+1
        stage_metadata.append({'ordinal': ordinal, 'window': window, 'index': index,
                               'inputLineSha256': digest(line), 'status': prior['status'],
                               'omittedPairs': counts['omittedPairs'], 'cacheAction': expected_cache['action']})
    need(next(source_rows, None) is None and next(saved_rows, None) is None, 'no-extra-input-or-result-stage')
    need(len(refusals) == 1 and cache.used == len(cache.witnesses), 'one-inherited-refusal-and-no-unused-witnesses')
    CHECKS.append('all 1920 original-row byte hashes and historical refusal/provenance retained; every stage-major pair slot and actual norm/class/omission accounted')
    CHECKS.append('all current-axis checks replayed with declared Python binary64 subtraction; recorded intrinsic words classified without rerunning Math.hypot')
    return totals, events, reasons, refusals, stage_metadata


def source_gate():
    manifest, manifest_pin = capture(REL+'/source-manifest.json')
    publication, publication_pin = capture(REL+'/source-publication.json')
    need(publication['manifestSha256'] == manifest_pin['sha256']
         and publication['manifestBytes'] == manifest_pin['bytes'], 'public-source-manifest-identity')
    need(re.fullmatch('[0-9a-f]{40}', publication['commit']), 'public-source-commit')
    for key in ('remoteBytesEqualLocal', 'committedBytesEqualLocal', 'independentReviewPassed'):
        need(publication.get(key) is True, 'reviewed-public-source:'+key)
    for pin in manifest['files']:
        need(type(pin) is dict and pin.get('kind') in ('source', 'input'), 'manifest-pin-kind')
        fields = {'path', 'bytes', 'sha256', 'kind'} | ({'originCommit'} if pin['kind'] == 'input' else set())
        need(set(pin) == fields, 'manifest-pin-fields')
        relative = pin['path']
        safe_path(relative)
        validate_pin(pin)
        need(relative not in SOURCE_PINS, 'unique-manifest-pin')
        SOURCE_PINS[relative] = pin
        if pin['kind'] == 'source':
            local_checked(relative, pin)
        else:
            origin = RECEIPT_COMMIT if relative == RECEIPT_PATH or relative in SUPPLEMENTS else INPUT_COMMIT
            need(pin['originCommit'] == origin, 'fixed-immutable-input-origin')
            INPUT_PINS[relative] = pin
    need(integer(publication['verifiedFilePins']) == len(SOURCE_PINS), 'published-pin-count')
    for name in ('config.json', 'SCHEMA.md', 'PROOF-PLAN.md', 'EXECUTION-PROTOCOL.md', 'runtime.json', 'input-pins.json',
                 'source/diagnose.cjs', 'source/candidate.cjs', 'source/audit.py', 'source/common.py',
                 'source/supervise.py', 'source/launch.py', 'source/finalize.py', 'source/ui.cjs',
                 'review/AUDIT-DESIGN.md', 'review/CONDITIONAL-LEMMA.md', 'review/STATIC-CHALLENGE.md',
                 'viewer/index.html', 'viewer/app.js'):
        need(SOURCE_PINS.get(REL+'/'+name, {}).get('kind') == 'source', 'mandatory-source:'+name)
    for name in ('three.module.js', 'three.core.js', 'OrbitControls.js'):
        need(SOURCE_PINS.get('outputs/step02b-source/vendor/'+name, {}).get('kind') == 'source', 'mandatory-display-dependency:'+name)
    required = {OLD+'/'+name for name in ('LITERATURE.md', 'RESULT-CLAIMS.md', 'review/RESULT-REVIEW.md',
                 'producer-supervisor.json', 'audit-supervisor.json', 'audit/audit.json', 'audit/exit.json',
                 'results/stages.jsonl', 'results/summary.json', 'result-manifest.json')}
    required |= PROOF_INPUTS | SUPPLEMENTS | {RECEIPT_PATH}
    need(set(INPUT_PINS) == required and len(INPUT_PINS) == 15, 'exact-fifteen-input-pins')
    input_index = parse(local_checked(REL+'/input-pins.json', SOURCE_PINS[REL+'/input-pins.json']))
    exact(input_index, {'files': [INPUT_PINS[path] for path in sorted(INPUT_PINS)]}, 'frozen-input-pin-index')
    expected = {'schema': 'm31-radial-certificate-config-v1', 'stages': 1920, 'windows': 12,
                'stagesPerWindow': 160, 'drones': 64, 'halfWidth': .125, 'radius': 3, 'marginPower': -20,
                'componentThreshold': 4, 'inputCommit': INPUT_COMMIT, 'inputCheckpoint': OLD,
                'allocations': {'producer': {'seconds': 300, 'mib': 128}, 'audit': {'seconds': 900, 'mib': 16},
                                'finalize': {'seconds': 120, 'mib': 2}, 'ui': {'seconds': 150, 'mib': 16}},
                'readPolicy': {'attemptsPerFile': 3, 'gitReadTimeoutSeconds': 45}, 'nativeCalls': 0,
                'performanceMeasured': False, 'maxHypotCalls': 7741464}
    exact(parse(local_checked(REL+'/config.json', SOURCE_PINS[REL+'/config.json'])), expected, 'fixed-prospective-config')
    for relative, pin in INPUT_PINS.items():
        committed(relative, pin)
    CHECKS.append('exact public reviewed source/config and all fifteen immutable committed inputs checked, including full Three.js module closure')
    return publication, manifest_pin, publication_pin


def frozen_input(relative):
    need(relative in INPUT_PINS, 'input-must-be-prospectively-pinned')
    return parse(committed(relative, INPUT_PINS[relative]))


def prior_gate():
    manifest_path = OLD+'/result-manifest.json'
    need(INPUT_PINS[manifest_path]['bytes'] == 19976
         and INPUT_PINS[manifest_path]['sha256'] == 'acb61c176bcf87250a7658b2675d00fd8af4104a0504da5c1fb80bebdf56a5cb',
         'fixed-prior-result-manifest')
    manifest, receipt = frozen_input(manifest_path), frozen_input(RECEIPT_PATH)
    need(manifest['schema'] == 'm31-neighbor-density-result-v1'
         and receipt['schema'] == 'm31-neighbor-density-public-result-v1', 'prior-public-schema')
    need(receipt['commit'] == INPUT_COMMIT and receipt['sourceCommit'] == manifest['sourceCommit']
         and receipt['manifestPath'] == manifest_path and receipt['manifestBytes'] == 19976
         and receipt['manifestSha256'] == INPUT_PINS[manifest_path]['sha256'] and receipt['verifiedFilePins'] == 88
         and receipt['remoteManifestBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True
         and receipt['independentPublicReviewPassed'] is True and receipt['allAllocationsClosed'] is True
         and receipt['allocationRetries'] == 0 and receipt['nativeCalls'] == 0, 'prior-final-public-closure')
    public = {pin['path']: pin for pin in manifest['files']}
    need(len(public) == len(manifest['files']) == 88, 'prior-public-pin-inventory')
    supplements = {pin['path']: pin for pin in receipt['supplementalPublicationRecords']}
    for relative, pin in INPUT_PINS.items():
        if relative in (manifest_path, RECEIPT_PATH):
            continue
        previous = supplements.get(relative) if relative in SUPPLEMENTS else public.get(relative)
        need(previous is not None, 'prior-public-file-descriptor')
        exact({key: previous[key] for key in ('path', 'bytes', 'sha256')},
              {key: pin[key] for key in ('path', 'bytes', 'sha256')}, 'prior-public-input-identity')
    report = frozen_input(OLD+'/audit/audit.json')
    summary = frozen_input(OLD+'/results/summary.json')
    need(report['passed'] is True and report['evidenceIntegrityPassed'] is True
         and report['independentCountAccountingPassed'] is True and report['stages'] == 1920
         and report['nativeCalls'] == 0 and report['sourceCommit'] == manifest['sourceCommit'], 'prior-independent-audit-passed')
    exact(report['summary'], summary, 'prior-audited-summary')
    old_file_pins = {pin['file']: pin for pin in report['filePins']}
    for name in ('results/stages.jsonl', 'results/summary.json'):
        exact(old_file_pins.get(name), {'file': name, 'bytes': INPUT_PINS[OLD+'/'+name]['bytes'],
                                       'sha256': INPUT_PINS[OLD+'/'+name]['sha256']}, 'prior-audited-data-pin')
    for phase in ('producer', 'audit'):
        closed = frozen_input(OLD+'/'+phase+'-supervisor.json')
        need(closed['closed'] is True and closed['returncode'] == 0 and closed['allocationWallPassed'] is True
             and closed['outputCapPassed'] is True and not closed.get('timeout'), 'prior-closed-'+phase)
    closed = frozen_input(OLD+'/audit/exit.json')
    need(closed['closed'] is True and closed['exitCode'] == 0, 'prior-audit-internal-closure')
    need(summary['schema'] == 'm31-neighbor-density-summary-v1' and summary['stages'] == 1920
         and summary['nativeCalls'] == 0 and len(summary['windows']) == 12 and len(summary['refusals']) == 1,
         'prior-fixed-selection-summary')
    CHECKS.append('published density result, both successful producer/audit closures and independently audited row/summary identities bound without old archive extraction')
    return report, summary


def producer_gate():
    supervisor, supervisor_pin = capture(REL+'/producer-supervisor.json')
    closed, exit_pin = capture(REL+'/results/exit.json')
    need(supervisor.get('closed') is True and supervisor.get('returncode') == 0
         and supervisor.get('allocationWallPassed') is True and supervisor.get('outputCapPassed') is True
         and not supervisor.get('timeout') and not supervisor.get('evidenceOverflow'), 'successful-producer-supervision')
    need(closed.get('closed') is True and closed.get('exitCode') == 0
         and closed['completed'] == 1920 and closed['nativeCalls'] == 0, 'complete-producer-internal-closure')
    need(0 <= finite(closed['wallSeconds']) <= 300 and 0 <= finite(supervisor['wallSeconds']) <= 300, 'producer-wall-bounds')
    expected = {'launch.json', 'input-binding.json', 'controls-partial.jsonl', 'controls.json', 'witnesses.jsonl',
                'norms.bin', 'classes.bin', 'omitted.bin', 'stages.jsonl', 'summary.json', 'exit.json'}
    files = list((BASE/'results').iterdir())
    need({path.name for path in files} == expected
         and all(path.is_file() and not path.is_symlink() for path in files), 'exact-successful-producer-inventory')
    actual = sum(path.stat().st_size for path in files)
    need(actual == supervisor['outputBytes'] <= MAX_RESULT and actual-exit_pin['bytes'] == closed['bytesBeforeExit'],
         'producer-whole-and-pre-exit-byte-accounting')
    launch, _ = capture(REL+'/results/launch.json')
    exact(launch, {'singleUse': True, 'nativeCalls': 0}, 'producer-single-use-launch')
    CHECKS.append('single successful bounded producer, exact eleven-file inventory and complete output/pre-exit byte accounting')
    return closed, supervisor_pin


def audit():
    publication, manifest_pin, publication_pin = source_gate()
    previous_report, previous_summary = prior_gate()
    producer_exit, supervisor_pin = producer_gate()
    binding, _ = capture(REL+'/results/input-binding.json')
    need(set(binding) == {'sourceCommit', 'sourceManifestSha256', 'inputPath', 'inputSha256', 'inputBytes',
                         'readEvents', 'node', 'v8', 'runtimeMappingProven'}, 'producer-input-binding-fields')
    input_path = OLD+'/results/stages.jsonl'
    input_pin = INPUT_PINS[input_path]
    need(binding['sourceCommit'] == publication['commit'] and binding['sourceManifestSha256'] == manifest_pin['sha256']
         and binding['inputPath'] == input_path and binding['inputSha256'] == input_pin['sha256']
         and binding['inputBytes'] == input_pin['bytes'] and binding['runtimeMappingProven'] is False,
         'producer-source-input-and-runtime-limit-binding')
    runtime = parse(local_checked(REL+'/runtime.json', SOURCE_PINS[REL+'/runtime.json']))
    need(binding['node'] == runtime['nodeVersion'] and type(binding['v8']) is str and 0 < len(binding['v8']) <= 128,
         'recorded-runtime-version')
    need(type(binding['readEvents']) is list, 'producer-read-events-list')
    exact(binding['readEvents'], producer_exit['readEvents'], 'producer-read-event-accounting')
    controls, _ = capture(REL+'/results/controls.json')
    partial_raw, _ = captured_bytes(REL+'/results/controls-partial.jsonl', MAX_METADATA)
    witness_raw, _ = captured_bytes(REL+'/results/witnesses.jsonl', MAX_RESULT)
    cache = CacheVerifier([value for _, value in json_lines(witness_raw)])
    control_calls, control_events = audit_controls(controls, [value for _, value in json_lines(partial_raw)], cache)
    norms, _ = captured_bytes(REL+'/results/norms.bin', MAX_RESULT)
    classes, _ = captured_bytes(REL+'/results/classes.bin', MAX_RESULT)
    omitted, _ = captured_bytes(REL+'/results/omitted.bin', MAX_RESULT)
    stages, _ = captured_bytes(REL+'/results/stages.jsonl', MAX_RESULT)
    prior_raw = committed(input_path, input_pin)
    totals, events, reasons, refusals, metadata = audit_stages(prior_raw, stages, norms, classes, omitted, cache)
    exact(refusals, previous_summary['refusals'], 'inherited-refusal-identities-unchanged')
    sample_gate = totals['falseOmissions'] == 0 and totals['omittedPairs'] > 0 and events['reuse'] > 0
    summary = {'complete': True, 'stages': 1920, 'controls': 10, 'nativeCalls': 0,
               'hypotCalls': control_calls+totals['normCalls'], 'controlHypotCalls': control_calls,
               'dataHypotCalls': totals['normCalls'], 'totals': totals, 'sampleGate': sample_gate,
               'controlGate': True, 'cacheEvents': events, 'conditionalOnly': True,
               'runtimeGeneralEquivalenceProven': False, 'performanceMeasured': False,
               'priorAggregateCountsMatch': True,
               'scope': 'fixed exposed saved-state center-stage diagnostic; no full-query equivalence or universal cache guarantee'}
    saved_summary, _ = capture(REL+'/results/summary.json')
    exact(saved_summary, summary, 'complete-independent-summary')
    need(sample_gate and producer_exit['hypotCalls'] == summary['hypotCalls'] <= 7741464,
         'finite-sample-gate-and-actual-call-closure')
    CHECKS.append('exact rational RN-even box/difference/square/sum replay and independent lower-enclosure inequalities checked for every build mask')
    CHECKS.append('every cache transition/build ID/context, inclusive containment, all summary/call totals and finite sample/control gates independently reconciled')
    for relative, pin in list(CONSUMED_PINS.items()):
        local_checked(relative, pin, MAX_RESULT)
    tick()
    result_names = sorted(path.name for path in (BASE/'results').iterdir())
    file_pins = [{'file': 'results/'+name, **CONSUMED_PINS[REL+'/results/'+name]} for name in result_names]
    return {'schema': 'm31-radial-certificate-audit-v1', 'passed': True, 'stages': 1920, 'nativeCalls': 0,
            'summary': summary, 'checks': CHECKS, 'filePins': file_pins,
            'sourceCommit': publication['commit'], 'sourceManifestSha256': manifest_pin['sha256'],
            'sourceManifestPin': manifest_pin, 'sourcePublicationPin': publication_pin,
            'inputCommit': INPUT_COMMIT, 'inputStagePin': input_pin,
            'inputPins': [INPUT_PINS[path] for path in sorted(INPUT_PINS)], 'producerSupervisorPin': supervisor_pin,
            'recordedNode': binding['node'], 'recordedV8': binding['v8'], 'runtimeMappingProven': False,
            'inheritedRefusals': refusals, 'controlCacheEvents': control_events, 'dataCacheReasons': reasons,
            'buildWitnessesVerified': cache.used, 'buildOrderedPairsRationallyChecked': cache.certificate_pairs,
            'buildOmissionsRationallyCertified': cache.certificate_omissions,
            'containmentCoordinateComparisons': cache.contained_coordinates, 'stageVerification': metadata,
            'readEvents': READ_EVENTS, 'producerReadEvents': producer_exit['readEvents'],
            'certificateArithmetic': 'exact integer ratios and independently implemented binary64 RN-even with gradual underflow; no floating multiplication/square root used for certificate',
            'currentAxisArithmetic': 'ordinary Python IEEE binary64 source-minus-receiver subtraction and global-span subtraction; explicitly assumed basic-op conformance',
            'hypotRecalculatedByAudit': False, 'oldPerPairEqualityEstablished': False,
            'oldAggregateCountsMatch': True, 'conditionalOnly': True, 'runtimeGeneralEquivalenceProven': False,
            'limitations': ['recorded intrinsic words are classified, not independently recalculated',
                            'old saved counts provide aggregate consistency, not historical per-pair identity',
                            'conditional expression theorem remains unbound to all actual installed runtime paths',
                            'finite observed omission checks do not qualify arbitrary points or all points inside boxes',
                            'no native load/rotor/admission/solve/full-query equivalence tested',
                            'controls cover only the fixed branches; no additional synthetic or universal coverage claimed'],
            'performanceMeasured': False, 'physicalValidity': False, 'flightSafetyClaim': False,
            'speedupClaim': False, 'researchComplete': False,
            'implementationDisclosure': 'standard-library loader/JSON helpers reused as source text from prior auditor; independent certificate/lifecycle/pair verification; no previous/producer/scientific module imported'}


def main():
    global START
    START = time.monotonic()
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'optimized-audit-not-permitted')
    need((BASE/'audit-supervisor-launch.lock').is_file(), 'single-supervised-audit-allocation-required')
    out = BASE/'audit'
    need(not out.is_symlink(), 'audit-directory-not-symlink')
    out.mkdir()
    charged = 0

    def save(name, value, failure=False):
        nonlocal charged
        raw = compact(value)+b'\n'
        need(charged+len(raw)+(0 if failure else 256*1024) <= MAX_OUTPUT, 'audit-output-budget')
        if not failure:
            tick()
        charged += len(raw)
        with (out/name).open('xb') as stream:
            need(stream.write(raw) == len(raw), 'complete-audit-write')

    code = 0
    try:
        save('launch.json', {'singleUse': True, 'nativeCalls': 0,
                            'startedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            'scope': 'independent saved-only finite distance diagnostic audit'})
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
