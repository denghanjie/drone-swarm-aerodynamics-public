"""One saved-result airflow audit; standard library only, no producer imports.

Invoke only after public source verification and the sole evaluator completes,
under the separately allocated external 60-second limit. No preview execution.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import hashlib
import json
import math
import struct
import time
import zlib

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
RESULTS = BASE / 'results'
MIB = 1024 * 1024
MAT_CAP = 4 * MIB
RESULT_CAP = 16 * MIB
START = None
TOLERANCE = Decimal('2e-12')
ROWS, COLUMNS = 272, 537
DATA_PINS = {
    'x_piv.mat': (310555, '4c06c41bbb20e96859da9510a303db8b95fdd5f0ef554fe9eab5e9534fa111aa'),
    'z_piv.mat': (13407, '0b2b45b8f8b548a94d14d41d1ac8233fb26a95ef2b87fdab11d10d395f9f0e44'),
    'u_piv.mat': (1097141, '7e53479b66dac0090b50ea4905cd9c7e2d576cb620855034326efe7ba089fa68'),
    'v_piv.mat': (1107084, 'b6f23844c46c237870a4871f057274fda958f79a6de209d62cfc684f8b4876ac'),
    'README_static.txt': (4960, '2695a000f2beac1c2f84d645bf6c0b24ca879f5b7ecb8d9873e2b6cfd8e4de6b'),
}
BIN_LABELS = ('8<=Z<12', '12<=Z<20', '20<=Z<=30')
METRIC_FIELDS = {'count', 'mae', 'rmse', 'bias', 'maxAbsoluteError', 'maxIndex'}


def need(condition, label):
    if not condition:
        raise ValueError(label)


def guard():
    need(START is not None and time.monotonic() - START < 60, 'audit-deadline')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate-json-key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite-json-' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def read_local(path, limit):
    guard()
    need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'local-path')
    need(path.stat().st_size <= limit, 'file-bound')
    return path.read_bytes()


def identity(path, raw):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def verify_manifest(manifest):
    entries = manifest['files']
    need(type(entries) is list and 0 < len(entries) <= 10000, 'manifest-count')
    names = set()
    for pin in entries:
        guard()
        need(type(pin) is dict and set(pin) == {'path', 'bytes', 'sha256'}, 'manifest-fields')
        name = pin['path']
        need(type(name) is str and name not in names and not Path(name).is_absolute(), 'manifest-name')
        need('..' not in Path(name).parts, 'manifest-traversal')
        names.add(name)
        path = ROOT / name
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'manifest-path')
        need(type(pin['bytes']) is int and 0 <= pin['bytes'] <= 64 * MIB, 'manifest-file-bound')
        need(path.stat().st_size == pin['bytes'], 'manifest-size')
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            while True:
                block = stream.read(MIB)
                if not block:
                    break
                guard()
                digest.update(block)
        need(digest.hexdigest() == pin['sha256'], 'manifest-sha256')
    prefix = BASE.relative_to(ROOT).as_posix() + '/'
    required = {'PROTOCOL.md', 'DATA-PINS.json', 'source/audit.py', 'source/evaluate.py',
                'source/mat5.py', 'source/supervise.py', 'review/SOURCE-AUDIT.md'}
    required |= {'data/' + name for name in DATA_PINS}
    need(all(prefix + name in names for name in required), 'manifest-required-files')
    return len(entries)


class MatCursor:
    """Independent bounded MAT5 tag cursor, including small-data tags."""
    def __init__(self, raw):
        self.raw = memoryview(raw)
        self.offset = 0

    def take(self):
        guard()
        start = self.offset
        need(start + 8 <= len(self.raw), 'mat-short-tag')
        kind16, short_length = struct.unpack_from('<HH', self.raw, start)
        if short_length:
            need(1 <= short_length <= 4 and kind16 in (1, 5, 6, 9), 'mat-small-tag')
            self.offset = start + 8
            return kind16, bytes(self.raw[start + 4:start + 4 + short_length])
        kind, length = struct.unpack_from('<II', self.raw, start)
        need(kind in (1, 5, 6, 9, 14, 15) and length <= MAT_CAP, 'mat-element-domain')
        body = start + 8
        end = body + length
        self.offset = end if kind == 15 else body + ((length + 7) & ~7)
        need(end <= len(self.raw) and self.offset <= len(self.raw), 'mat-short-element')
        return kind, bytes(self.raw[body:end])

    def finished(self):
        need(self.offset == len(self.raw), 'mat-trailing-elements')


def decode_mat(raw, expected_name):
    need(136 <= len(raw) <= MAT_CAP and raw[124:128] == b'\x00\x01IM', 'mat-header')
    top = MatCursor(raw[128:])
    kind, body = top.take()
    top.finished()
    if kind == 15:
        inflater = zlib.decompressobj()
        plain = inflater.decompress(body, MAT_CAP + 1)
        need(len(plain) <= MAT_CAP and inflater.eof and not inflater.unused_data
             and not inflater.unconsumed_tail, 'mat-compression-boundary')
        inner = MatCursor(plain)
        kind, body = inner.take()
        inner.finished()
    need(kind == 14, 'mat-matrix')
    matrix = MatCursor(body)
    flag_type, flags = matrix.take()
    dim_type, dims = matrix.take()
    name_type, name = matrix.take()
    real_type, real = matrix.take()
    matrix.finished()
    need(flag_type == 6 and flags == struct.pack('<II', 6, 0), 'mat-real-dense-double')
    need(dim_type == 5 and len(dims) == 8
         and struct.unpack('<ii', dims) == (ROWS, COLUMNS), 'mat-fixed-shape')
    need(name_type == 1 and name.decode('ascii') == expected_name, 'mat-name')
    need(real_type == 9 and len(real) == ROWS * COLUMNS * 8, 'mat-real-length')
    values = tuple(item[0] for item in struct.iter_unpack('<d', real))
    # Nonfinite payload cells are retained for the declared selection/count rules.
    # The outer tuple is columns: independent explicit MATLAB column reconstruction.
    return tuple(values[c * ROWS:(c + 1) * ROWS] for c in range(COLUMNS))


def D(value):
    return Decimal.from_float(value) if type(value) is float else Decimal(value)


def same_word(actual, expected, label):
    need(type(actual) in (int, float) and math.isfinite(actual), label + '-finite')
    need(struct.pack('>d', actual) == struct.pack('>d', expected), label + '-word')


def close(actual, expected, label):
    need(type(actual) in (int, float) and math.isfinite(actual), label + '-finite')
    need(abs(D(actual) - D(expected)) <= TOLERANCE, label + '-absolute-tolerance')


def independent_fields(x_raw, z_raw):
    """60-digit algebra in l units; no producer model or receiver-force calls."""
    x, z = D(x_raw), D(z_raw)
    root_two = Decimal(2).sqrt()
    diameter = 2 * root_two
    need(z >= Decimal('2.5') * diameter and z * Decimal('.0325') < 2, 'inactive-axial-fade')
    shift_a = z + Decimal('5.817') * diameter
    width_a = Decimal('.07668') * shift_a
    radius_squared = x * x + 1
    width_squared = width_a * width_a
    a = Decimal('10.11') * diameter / shift_a * width_squared ** 2 / (
        width_squared + (root_two - 1) * radius_squared) ** 2
    if radius_squared >= 9 * width_squared:
        a = Decimal(0)
    elif radius_squared > 4 * width_squared:
        t = radius_squared.sqrt() / width_a - 2
        a *= 1 - 3 * t * t + 2 * t * t * t
    shift_b = z + Decimal('6.0585')
    width_b_squared = (Decimal('.0667') * shift_b) ** 2
    b = Decimal('9.508') / shift_b * width_b_squared ** 2 / (
        width_b_squared + (root_two - 1) * x * x) ** 2
    return a, b


def verify_metrics(stored, records, model, label):
    need(type(stored) is dict and set(stored) == METRIC_FIELDS, label + '-fields')
    need(type(stored['count']) is int and stored['count'] == len(records), label + '-count')
    if not records:
        need(all(stored[key] is None for key in METRIC_FIELDS - {'count'}), label + '-empty-null')
        return None
    errors = [r[model] - D(r['u']) for r in records]
    count = Decimal(len(errors))
    expected = {'mae': sum(map(abs, errors)) / count,
                'rmse': (sum(e * e for e in errors) / count).sqrt(),
                'bias': sum(errors) / count,
                'maxAbsoluteError': max(map(abs, errors))}
    for key, value in expected.items():
        close(stored[key], value, label + '-' + key)
    # Select the first maximum of the saved binary64 residuals after every
    # residual has been independently checked. This preserves the producer's
    # exact tie semantics without confusing high-precision near ties with ties.
    peak = records[0]
    for record in records[1:]:
        if abs(record['rounded_' + model]) > abs(peak['rounded_' + model]):
            peak = record
    need(type(stored['maxIndex']) is int and stored['maxIndex'] == peak['index'], label + '-first-max-index')
    need(abs(abs(peak[model] - D(peak['u'])) - expected['maxAbsoluteError']) <= TOLERANCE,
         label + '-independent-max-location')
    return expected


def write_once(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    need(len(raw) <= RESULT_CAP, 'audit-output-cap')
    with (RESULTS / name).open('xb') as stream:
        stream.write(raw)


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-saved-results')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved airflow audit; no retries.\n')
    try:
        manifest_raw = read_local(BASE / 'source-manifest.json', 2 * MIB)
        manifest = parse_json(manifest_raw)
        publication_raw = read_local(BASE / 'source-publication.json', MIB)
        publication = parse_json(publication_raw)
        need(publication['manifestSha256'] == sha(manifest_raw)
             and publication['remoteBytesEqualLocal'] is True
             and publication['committedBytesEqualLocal'] is True, 'public-source-gate')
        verified = verify_manifest(manifest)
        need(not (RESULTS / 'failure.json').exists(), 'evaluator-failure-present')
        supervisor_raw = read_local(RESULTS / 'evaluate-supervisor.json', MIB)
        supervisor = parse_json(supervisor_raw)
        need(supervisor['mode'] == 'evaluate' and supervisor['exitCode'] == 0
             and supervisor['timeout'] is False and 0 <= supervisor['elapsedSeconds'] <= 60,
             'successful-external-evaluator-supervision')
        need(supervisor['outputLimitExceeded'] is False and supervisor['outputCapBytes'] == RESULT_CAP
             and type(supervisor['savedBytesBeforeSupervisor']) is int
             and 0 <= supervisor['savedBytesBeforeSupervisor'] <= RESULT_CAP, 'evaluator-output-bound')
        later_files = {'evaluate-supervisor.json', 'audit.lock', 'audit-supervisor.lock',
                       'audit-stdout.txt', 'audit-stderr.txt'}
        saved_size = 0
        for directory in (RESULTS, BASE / 'ui'):
            if directory.exists():
                for path in directory.rglob('*'):
                    guard()
                    if path.is_file() and not (path.parent == RESULTS and path.name in later_files):
                        saved_size += path.stat().st_size
        need(saved_size == supervisor['savedBytesBeforeSupervisor']
             and saved_size <= RESULT_CAP, 'actual-evaluator-saved-bytes')
        execution_raw = read_local(RESULTS / 'execution.json', MIB)
        execution = parse_json(execution_raw)
        body = read_local(RESULTS / 'comparison.json', RESULT_CAP)
        need(execution['status'] == 'complete' and execution['resultBytes'] == len(body)
             and execution['sha256'] == sha(body) and 0 <= execution['elapsedSeconds'] < 60,
             'completed-result-pin')
        result = parse_json(body)
        controls_raw = read_local(RESULTS / 'controls.json', MIB)
        controls = parse_json(controls_raw)
        need(controls == {'passed': True, 'checks': ['plain/compressed masked MAT',
             'truncation and strict nonfinite refused', 'three symmetry and unit-conversion identities',
             'two fade endpoints']}, 'saved-fixed-controls')
        need(set(result) == {'status', 'sourceCommit', 'units', 'models', 'counts', 'cases',
             'metrics', 'maeDifferenceAminusB', 'bins', 'plane', 'limits'}, 'result-fields')
        need(result['status'] == 'completed-descriptive-airflow-comparison'
             and result['sourceCommit'] == publication['commit']
             and result['units'] == 'axial velocity / Ui', 'result-identity')
        need(result['models'] == {'a': 'M31-directed-axial-wake-v1', 'b': 'RSS-published-planar-fit'}, 'model-identities')
        need(result['plane'] == {'y_l': 1, 'l_m': .0325}, 'measurement-plane')
        need(result['limits'] == ['RSS curve fitted to these experiments; no independent validation',
             'Finite sampled mean cells are not independent trials',
             'Planar field only; full3D airflow and receiving thrust untested',
             'Calibration and stitched-field uncertainties not quantified',
             'Original Bauersfeld observable is flow magnitude; A is project axial interpretation',
             'A assumes shared Ui=UH induced-velocity normalization; no independent SI calibration'], 'claim-limits')
        pins = parse_json(read_local(BASE / 'DATA-PINS.json', MIB))
        need(type(pins) is list and len(pins) == len(DATA_PINS), 'data-pin-count')
        named_pins = {}
        for pin in pins:
            need(set(pin) == {'file', 'bytes', 'sha256'} and pin['file'] not in named_pins, 'data-pin-fields')
            named_pins[pin['file']] = (pin['bytes'], pin['sha256'])
        need(named_pins == DATA_PINS, 'independent-data-pins')
        arrays, raw_pins = {}, []
        for filename, (length, digest) in DATA_PINS.items():
            raw = read_local(BASE / 'data' / filename, MAT_CAP)
            need(len(raw) == length and sha(raw) == digest, 'raw-file-pin')
            raw_pins.append(identity(BASE / 'data' / filename, raw))
            if filename.endswith('.mat'):
                arrays[filename[:-4]] = decode_mat(raw, filename[:-4])
        cases = result['cases']
        need(type(cases) is list and 20 <= len(cases) <= 9216, 'saved-case-count')
        counts = dict(candidates=0, nonfiniteCoordinates=0, outsideDomain=0, missingU=0, accepted=0, missingV=0)
        records, distinct_z, raw_words = [], set(), 0
        with localcontext() as context:
            context.prec = 60
            for column in range(0, COLUMNS, 4):
                for row in range(0, ROWS, 4):
                    guard()
                    counts['candidates'] += 1
                    x, z = arrays['x_piv'][column][row], arrays['z_piv'][column][row]
                    if not math.isfinite(x) or not math.isfinite(z):
                        counts['nonfiniteCoordinates'] += 1
                        continue
                    if z < 8 or z > 30 or x < -4 or x > 4:
                        counts['outsideDomain'] += 1
                        continue
                    u, v = arrays['u_piv'][column][row], arrays['v_piv'][column][row]
                    if not math.isfinite(u):
                        counts['missingU'] += 1
                        continue
                    need(counts['accepted'] < len(cases), 'missing-selected-case')
                    case = cases[counts['accepted']]
                    counts['accepted'] += 1
                    index = column * ROWS + row
                    need(set(case) == {'row', 'column', 'index', 'X', 'Z', 'u', 'v', 'a', 'b', 'residualA', 'residualB'}, 'case-fields')
                    for key, expected in [('row', row), ('column', column), ('index', index)]:
                        need(type(case[key]) is int and case[key] == expected, 'column-major-' + key)
                    for key, expected in [('X', x), ('Z', z), ('u', u)]:
                        same_word(case[key], expected, 'raw-' + key)
                        raw_words += 1
                    if math.isfinite(v):
                        same_word(case['v'], v, 'raw-v')
                        raw_words += 1
                    else:
                        counts['missingV'] += 1
                        need(case['v'] is None, 'masked-v-null')
                    a, b = independent_fields(x, z)
                    for key, expected, residual in [('a', a, 'residualA'), ('b', b, 'residualB')]:
                        close(case[key], expected, 'field-' + key)
                        close(case[residual], expected - D(u), 'signed-residual-' + key)
                        same_word(case[residual], case[key] - u, 'saved-residual-' + key)
                    records.append({'index': index, 'z': z, 'u': u, 'a': a, 'b': b,
                                    'rounded_a': case['residualA'], 'rounded_b': case['residualB']})
                    distinct_z.add(z)
            need(counts['candidates'] == 9180 and counts['accepted'] == len(cases)
                 and len(distinct_z) >= 3, 'complete-fixed-selection')
            need(type(result['counts']) is dict and set(result['counts']) == set(counts)
                 and all(type(value) is int for value in result['counts'].values())
                 and result['counts'] == counts, 'exclusion-counts')
            need(counts['candidates'] == counts['nonfiniteCoordinates'] + counts['outsideDomain']
                 + counts['missingU'] + counts['accepted'], 'candidate-partition')
            need(type(result['metrics']) is dict and set(result['metrics']) == {'a', 'b'}, 'overall-metrics-fields')
            ma = verify_metrics(result['metrics']['a'], records, 'a', 'overall-a')
            mb = verify_metrics(result['metrics']['b'], records, 'b', 'overall-b')
            close(result['maeDifferenceAminusB'], ma['mae'] - mb['mae'], 'paired-mae-difference')
            same_word(result['maeDifferenceAminusB'], result['metrics']['a']['mae'] - result['metrics']['b']['mae'], 'saved-mae-difference')
            need(type(result['bins']) is list and len(result['bins']) == 3, 'bin-count')
            groups = [[], [], []]
            for record in records:
                groups[0 if record['z'] < 12 else 1 if record['z'] < 20 else 2].append(record)
            for stored, label, group in zip(result['bins'], BIN_LABELS, groups):
                need(set(stored) == {'label', 'a', 'b'} and stored['label'] == label, 'bin-identity')
                for model in ('a', 'b'):
                    verify_metrics(stored[model], group, model, label + '-' + model)
        need(verify_manifest(manifest) == verified, 'post-audit-source-pins')
        for path, original in [(BASE / 'source-manifest.json', manifest_raw),
                               (BASE / 'source-publication.json', publication_raw),
                               (RESULTS / 'comparison.json', body),
                               (RESULTS / 'execution.json', execution_raw),
                               (RESULTS / 'controls.json', controls_raw),
                               (RESULTS / 'evaluate-supervisor.json', supervisor_raw)]:
            need(read_local(path, RESULT_CAP) == original, 'retained-source-and-result-bytes')
        guard()
        report = {'schema': 'm31-airflow-independent-audit-v1', 'passed': True, 'complete': True,
                  'sourceManifestSha256': sha(manifest_raw), 'verifiedSourcePins': verified,
                  'publicationPin': identity(BASE / 'source-publication.json', publication_raw),
                  'resultPin': identity(RESULTS / 'comparison.json', body), 'rawDataPins': raw_pins,
                  'evaluatorSupervisorPin': identity(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
                  'countsChecked': counts, 'rawSelectedWordsChecked': raw_words,
                  'fieldPredictionsChecked': 2 * len(cases), 'metricGroupsChecked': 8,
                  'arithmetic': 'Independent 60-digit Decimal l-unit expressions; explicit column-major MAT decoding.',
                  'tolerance': '2e-12 absolute in Ui units; numerical audit tolerance only',
                  'maximumIndexRule': 'First column-major maximum of independently checked binary64 residuals; independent high-precision maximum agrees within tolerance.',
                  'sourcesPreserved': True, 'resultsPreserved': True,
                  'statisticalRejectionEstablished': False, 'independentPhysicalValidation': False,
                  'scope': 'Saved airflow records, exclusion counts, two declared fields and summaries only; no new cases, fitting, uncertainty calibration, or receiving-force model.',
                  'elapsedSeconds': time.monotonic() - START}
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'acceptedCasesChecked': len(cases), 'fieldPredictionsChecked': 2 * len(cases)}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()
