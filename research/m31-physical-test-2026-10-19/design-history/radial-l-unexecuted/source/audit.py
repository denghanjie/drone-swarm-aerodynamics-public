"""One independent post-execution audit; stdlib only, no producer imports.

Invoke once, under the declared external 60-second limit, after public source
verification and evaluator completion. Never run this to preview force data.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import hashlib
import json
import math
import struct
import sys
import time
import zlib

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
RESULTS = BASE / 'results'
CAP = 1024 * 1024
START = None
TOLERANCE = Decimal('2e-12')
DATA_PINS = {
    'x_l': (255, '7b3d8b097d2121b3fb69249692b557ac6a30458166dd60452dbbb2ed0dda51e6'),
    'z_l': (264, 'da2b40e5f16c1d3b4c48f1f66209c7bcc6fac8307a5280ebec386a05303f7910'),
    'upper_F_W': (525, 'd9fd6534473e8c797d6b542646ab83f78e7c4173508fd2edb8cd0bfc4013c8d0'),
    'lower_F_W': (1411, '3fb714fa8b2faca8f44cb3cf1788b61bc8bd11591eacf8290a20725428287da4'),
    'upper_Fstd_W': (380, '04d02706e733b1485a866dcfb08173991079518e397fe55cc7333cd7198de2dc'),
    'lower_Fstd_W': (383, '747fe9a7b6651814db38ae5aa8ffb42f623faff29022d822d14e0c26b8082a19'),
}
OBSERVED = ('upper_F_W', 'lower_F_W', 'upper_Fstd_W', 'lower_Fstd_W')


def need(condition, label):
    if not condition:
        raise ValueError(label)


def guard():
    need(START is not None and time.monotonic() - START < 60, 'audit-deadline')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def json_bytes(raw):
    def invalid(value):
        raise ValueError('nonfinite-json-' + value)
    return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=invalid)


def read_local(path, cap):
    guard()
    need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'file-path')
    need(path.stat().st_size <= cap, 'file-size')
    return path.read_bytes()


def identity(path, raw):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def frozen_files(manifest):
    entries = manifest['files']
    need(type(entries) is list and 0 < len(entries) <= 10000, 'manifest-count')
    names = set()
    for pin in entries:
        guard()
        need(set(pin) == {'path', 'bytes', 'sha256'}, 'manifest-pin-fields')
        name = pin['path']
        need(type(name) is str and name not in names and not Path(name).is_absolute(), 'manifest-name')
        names.add(name)
        f = ROOT / name
        need(f.resolve().is_relative_to(ROOT) and not f.is_symlink(), 'manifest-path')
        need(type(pin['bytes']) is int and 0 <= pin['bytes'] <= 64 * CAP, 'manifest-size-bound')
        need(f.stat().st_size == pin['bytes'], 'manifest-size')
        digest = hashlib.sha256()
        with f.open('rb') as stream:
            while True:
                block = stream.read(CAP)
                if not block:
                    break
                guard()
                digest.update(block)
        need(digest.hexdigest() == pin['sha256'], 'manifest-sha')
    prefix = BASE.relative_to(ROOT).as_posix() + '/'
    required = {'PROTOCOL.md', 'SCHEMA.json', 'source/audit.py', 'source/mat5.py', 'source/evaluate.py'}
    required |= {'data/' + name + '.mat' for name in DATA_PINS}
    need(all(prefix + name in names for name in required), 'manifest-required-inputs')
    return len(entries)


class MatCursor:
    """Independent little-endian MAT5 element reader with bounded slices."""
    def __init__(self, data):
        self.data = memoryview(data)
        self.pos = 0

    def one(self):
        guard()
        start = self.pos
        need(start + 8 <= len(self.data), 'mat-tag-truncated')
        kind16, small_count = struct.unpack_from('<HH', self.data, start)
        if small_count:
            need(1 <= small_count <= 4 and kind16 in (1, 5, 6, 9), 'mat-small-tag')
            self.pos += 8
            return kind16, bytes(self.data[start + 4:start + 4 + small_count])
        kind, count = struct.unpack_from('<II', self.data, start)
        need(kind in (1, 5, 6, 9, 14, 15) and count <= CAP, 'mat-element-domain')
        body_start = start + 8
        end = body_start + count
        # MATLAB v5 miCOMPRESSED payloads are not followed by 8-byte padding.
        next_pos = end if kind == 15 else body_start + ((count + 7) & ~7)
        need(end <= len(self.data) and next_pos <= len(self.data), 'mat-element-truncated')
        self.pos = next_pos
        return kind, bytes(self.data[body_start:end])

    def finished(self):
        need(self.pos == len(self.data), 'mat-trailing-content')


def decode_mat(raw, expected_name):
    need(136 <= len(raw) <= CAP, 'mat-file-bound')
    need(raw[124:128] == b'\x00\x01IM', 'mat-version-endian')
    top = MatCursor(raw[128:])
    kind, body = top.one()
    top.finished()
    if kind == 15:
        inflater = zlib.decompressobj()
        plain = inflater.decompress(body, CAP + 1)
        need(len(plain) <= CAP and inflater.eof and not inflater.unused_data
             and not inflater.unconsumed_tail, 'mat-deflate-boundary')
        inner = MatCursor(plain)
        kind, body = inner.one()
        inner.finished()
    need(kind == 14, 'mat-matrix-required')
    matrix = MatCursor(body)
    flags_kind, flags = matrix.one()
    dims_kind, dims_raw = matrix.one()
    name_kind, name_raw = matrix.one()
    real_kind, values_raw = matrix.one()
    matrix.finished()
    need(flags_kind == 6 and flags == struct.pack('<II', 6, 0), 'mat-plain-double-only')
    need(dims_kind == 5 and len(dims_raw) == 8, 'mat-rank-two')
    dimensions = struct.unpack('<ii', dims_raw)
    need(dimensions == (14, 12), 'mat-fixed-shape')
    need(name_kind == 1 and name_raw.decode('ascii') == expected_name, 'mat-variable-name')
    need(real_kind == 9 and len(values_raw) == 14 * 12 * 8, 'mat-real-size')
    values = tuple(item[0] for item in struct.iter_unpack('<d', values_raw))
    need(all(math.isfinite(v) for v in values), 'mat-nonfinite')
    # Explicit row/column representation, rather than treating the stream as rows.
    return [[values[row + 14 * column] for column in range(12)] for row in range(14)]


def bits_equal(actual, expected, label):
    need(type(actual) in (int, float) and math.isfinite(actual), label + '-type')
    need(struct.pack('>d', actual) == struct.pack('>d', expected), label)


def D(value):
    return Decimal.from_float(value) if type(value) is float else Decimal(value)


def close(actual, expected, label):
    need(type(actual) in (int, float) and math.isfinite(actual), label + '-finite')
    e = D(expected)
    need(abs(D(actual) - e) <= TOLERANCE * max(Decimal(1), abs(e)), label)


def independent_prediction(z_m, arm_radius, upper_scale, lower_scale):
    """70-digit scalar reduction, independent of the evaluator's binary64 code.

    Source at (0,0,z), receiver at the origin, both upright. Four receiver
    corners have equal radial distance l; the reverse direction has down=-z.
    Same hardware and symmetric nominal rotor loads cancel induced scales.
    """
    z, l, qu, ql = map(D, (z_m, arm_radius, upper_scale, lower_scale))
    need(l > 0 and qu > 0 and ql > 0 and z >= 5 * l, 'audited-near-domain')
    need(z < Decimal('2.5') and z < 3, 'selected-active-downstream-domain')
    need(-z < 0, 'upper-upstream-exclusion')
    diagonal_coordinate = l / Decimal(2).sqrt()
    radius = (2 * diagonal_coordinate * diagonal_coordinate).sqrt()
    need(abs(radius - l) < Decimal('1e-60'), 'stacked-rotor-radius')
    shifted_down = z / (2 * l) + Decimal('5.817')
    width = Decimal('0.07668') * (z + Decimal('11.634') * l)
    radial_fraction = radius / width
    if radial_fraction >= 3:
        alpha = Decimal(0)
    else:
        profile_denominator = 1 + (Decimal(2).sqrt() - 1) * radial_fraction ** 2
        profile = Decimal('10.11') / shifted_down / profile_denominator ** 2
        # Smooth fades expressed as a polynomial; selected values may be interior.
        down_t = max(Decimal(0), min(Decimal(1), (z - 2) / Decimal('.5')))
        rad_t = max(Decimal(0), min(Decimal(1), radial_fraction - 2))
        profile *= (1 - 3 * down_t ** 2 + 2 * down_t ** 3)
        profile *= (1 - 3 * rad_t ** 2 + 2 * rad_t ** 3)
        alpha = profile * (qu / ql).sqrt()
    if not alpha:
        rotor = Decimal(1)
    else:
        lower, upper = Decimal(0), Decimal(1)
        # Independent high-precision enclosure of a strictly increasing cubic.
        for iteration in range(160):
            midpoint = (lower + upper) / 2
            if midpoint ** 3 + alpha * midpoint < 1:
                lower = midpoint
            else:
                upper = midpoint
        need(lower ** 3 + alpha * lower <= 1 <= upper ** 3 + alpha * upper,
             'root-enclosure')
        rotor = (lower + upper) / 2
        need(upper - lower < Decimal('1e-45'), 'root-width')
    return {'upper': qu, 'lower': ql * rotor, 'alpha': alpha, 'rotorRatio': rotor}


def prediction_matches(actual, expected, label):
    need(type(actual) is dict and set(actual) == set(expected), label + '-fields')
    for field in expected:
        close(actual[field], expected[field], label + '-' + field)


def write_once(name, value):
    raw = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    need(len(raw) <= CAP, 'audit-report-cap')
    with (RESULTS / name).open('xb') as stream:
        stream.write(raw)


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-completed-results-directory')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved-result audit; no retries.\n')
    try:
        manifest_raw = read_local(BASE / 'source-manifest.json', 2 * CAP)
        manifest = json_bytes(manifest_raw)
        publication_raw = read_local(BASE / 'source-publication.json', CAP)
        publication = json_bytes(publication_raw)
        need(publication['manifestSha256'] == sha(manifest_raw)
             and publication['remoteBytesEqualLocal'] is True
             and publication['committedBytesEqualLocal'] is True, 'public-source-gate')
        verified = frozen_files(manifest)
        need(not (RESULTS / 'failure.json').exists(), 'evaluator-failed')
        supervisor_raw = read_local(RESULTS / 'evaluate-supervisor.json', CAP)
        supervisor = json_bytes(supervisor_raw)
        need(supervisor['mode'] == 'evaluate' and supervisor['exitCode'] == 0
             and supervisor['timeout'] is False and 0 <= supervisor['elapsedSeconds'] <= 60,
             'evaluator-supervised-success')
        execution_raw = read_local(RESULTS / 'execution.json', CAP)
        execution = json_bytes(execution_raw)
        body = read_local(RESULTS / 'comparison.json', 32 * CAP)
        need(execution['status'] == 'completed' and execution['resultBytes'] == len(body)
             and execution['resultSha256'] == sha(body), 'completed-result-pin')
        result = json_bytes(body)
        controls_raw = read_local(RESULTS / 'controls.json', CAP)
        controls = json_bytes(controls_raw)
        need(controls == {'passed': True,
             'parser': ['plain', 'compressed', 'small tag', 'column major', 'truncated rejected', 'nonfinite rejected'],
             'model': ['zero root', 'four cubic residuals', 'near refused', 'upper null']}, 'saved-controls')
        schema = json_bytes(read_local(BASE / 'SCHEMA.json', CAP))
        named = {entry['name']: entry for entry in schema}
        need(len(named) == len(schema), 'schema-unique-names')
        grids, raw_pins = {}, []
        for name, (length, digest) in DATA_PINS.items():
            raw = read_local(BASE / 'data' / (name + '.mat'), CAP)
            need(len(raw) == length and sha(raw) == digest, 'independent-raw-data-pin')
            metadata = named[name]
            need(metadata['bytes'] == length and metadata['sha256'] == digest
                 and metadata['shape'] == [14, 12] and metadata['order'] == 'column-major', 'schema-data-pin')
            grids[name] = decode_mat(raw, name)
            raw_pins.append(identity(BASE / 'data' / (name + '.mat'), raw))
        for row in range(14):
            for col in range(12):
                for name in ('x_l', 'z_l'):
                    bits_equal(grids[name][row][col], named[name]['values'][row + 14 * col], 'coordinate-schema')
                bits_equal(grids['x_l'][row][col], grids['x_l'][0][col], 'rectilinear-x')
                bits_equal(grids['z_l'][row][col], grids['z_l'][row][0], 'rectilinear-z')
            bits_equal(grids['x_l'][row][0], 0.0, 'stacked-column')
        z_grid = [grids['z_l'][i][0] for i in range(14)]
        need(all(z_grid[i] < z_grid[i + 1] for i in range(13)), 'vertical-order')
        need([i for i, z in enumerate(z_grid) if z >= 6] == list(range(2, 14)), 'geometry-only-selection')
        need(result['status'] == 'completed-descriptive-comparison'
             and result['model'] == 'Kiran-stacked-fixedPWM-v1', 'comparison-identity')
        need(result['units'] == 'force divided by W; approximate W=0.265 N', 'comparison-units')
        need(result['counts'] == {'cases': 12, 'nominalEvaluations': 12, 'sensitivityEvaluations': 972}, 'counts')
        cases = result['cases']
        need(type(cases) is list and len(cases) == 12, 'case-count')
        expected_parameters = [(l, dz, qu, ql) for l in (.03245, .0325, .03255)
                               for dz in (-.001, 0., .001) for qu in (.9, 1., 1.1) for ql in (.9, 1., 1.1)]
        absolute_errors, sensitivity_count, observation_count = [], 0, 0
        with localcontext() as context:
            context.prec = 70
            for case, row in zip(cases, range(2, 14)):
                guard()
                need(case['row'] == row and case['column'] == 0, 'case-index')
                bits_equal(case['x_l'], grids['x_l'][row][0], 'case-x')
                bits_equal(case['z_l'], grids['z_l'][row][0], 'case-z')
                z = grids['z_l'][row][0] * .0325
                bits_equal(case['z_m'], z, 'case-dimensional-z')
                need(set(case['observed']) == set(OBSERVED), 'observed-fields')
                for name in OBSERVED:
                    value = grids[name][row][0]
                    bits_equal(case['observed'][name], value, 'observed-column-major-word')
                    if 'std' in name:
                        need(value >= 0, 'selected-nonnegative-spread')
                    observation_count += 1
                prediction = independent_prediction(z, .0325, 1., 1.)
                prediction_matches(case['prediction'], prediction, 'nominal')
                error = D(grids['lower_F_W'][row][0]) - prediction['lower']
                close(case['lowerResidual'], error, 'lower-signed-residual')
                absolute_errors.append(abs(error))
                need(len(case['sensitivity']) == 81, 'sensitivity-count')
                lower_values = []
                for stored, (l, dz, qu, ql) in zip(case['sensitivity'], expected_parameters):
                    guard()
                    need(set(stored) == {'l', 'dz', 'qu', 'ql', 'upper', 'lower', 'alpha', 'rotorRatio'}, 'sensitivity-fields')
                    for key, value in zip(('l', 'dz', 'qu', 'ql'), (l, dz, qu, ql)):
                        bits_equal(stored[key], value, 'sensitivity-parameter')
                    predicted = independent_prediction(z + dz, l, qu, ql)
                    prediction_matches({key: stored[key] for key in predicted}, predicted, 'sensitivity')
                    lower_values.append(predicted['lower'])
                    sensitivity_count += 1
                need(len(case['sampledLowerRange']) == 2, 'sampled-range-size')
                close(case['sampledLowerRange'][0], min(lower_values), 'sampled-minimum')
                close(case['sampledLowerRange'][1], max(lower_values), 'sampled-maximum')
            need(sensitivity_count == 972 and observation_count == 48, 'complete-case-coverage')
            contrast = D(grids['upper_F_W'][2][0]) - D(grids['upper_F_W'][13][0])
            primary = result['primary']
            need(set(primary) == {'nearRow', 'farRow', 'measuredDifference', 'predictedDifference',
                 'minimumDifferentialBiasToReconcile', 'equalOpposingPerCaseBias',
                 'approxDifferenceN', 'calibratedStatisticalRejection'}, 'primary-fields')
            need(primary['nearRow'] == 2 and primary['farRow'] == 13
                 and primary['calibratedStatisticalRejection'] is False, 'primary-scope')
            bits_equal(primary['predictedDifference'], 0., 'upper-null')
            rounded_contrast = grids['upper_F_W'][2][0] - grids['upper_F_W'][13][0]
            bits_equal(primary['measuredDifference'], rounded_contrast, 'primary-raw-contrast-word')
            bits_equal(primary['minimumDifferentialBiasToReconcile'], abs(rounded_contrast), 'primary-bias-word')
            bits_equal(primary['equalOpposingPerCaseBias'], abs(rounded_contrast) / 2, 'primary-half-bias-word')
            for key, value in [('measuredDifference', contrast), ('minimumDifferentialBiasToReconcile', abs(contrast)),
                               ('equalOpposingPerCaseBias', abs(contrast) / 2), ('approxDifferenceN', contrast * Decimal('.265'))]:
                close(primary[key], value, 'primary-' + key)
            mae = sum(absolute_errors) / 12
            need(set(result['secondary']) == {'mae', 'maxAbsoluteError', 'maxAbsoluteErrorApproxN', 'maeApproxN'}, 'secondary-fields')
            for key, value in [('mae', mae), ('maxAbsoluteError', max(absolute_errors)),
                               ('maxAbsoluteErrorApproxN', max(absolute_errors) * Decimal('.265')),
                               ('maeApproxN', mae * Decimal('.265'))]:
                close(result['secondary'][key], value, 'secondary-' + key)
        need(result['excluded'] == [
            {'row': 0, 'z_m': z_grid[0] * .0325, 'reason': 'near domain'},
            {'row': 1, 'z_m': z_grid[1] * .0325, 'reason': 'preselected conservative margin'}], 'excluded-cases')
        need(result['limitations'] == ['Aggregate published means, not individual trials',
             'SD semantics unresolved; not confidence intervals', 'Tare drift calibration and full pose uncertainty unavailable',
             'Lower nominal baseline equals W by assumption', 'Sensitivity grid is illustrative, not a validated uncertainty enclosure',
             'Not a blind holdout, not a novelty claim'], 'required-limitations')
        need(frozen_files(manifest) == verified, 'post-audit-source-preservation')
        need(read_local(RESULTS / 'comparison.json', 32 * CAP) == body
             and read_local(RESULTS / 'execution.json', CAP) == execution_raw
             and read_local(RESULTS / 'controls.json', CAP) == controls_raw
             and read_local(RESULTS / 'evaluate-supervisor.json', CAP) == supervisor_raw
             and read_local(BASE / 'source-publication.json', CAP) == publication_raw, 'result-preservation')
        guard()
        report = {'schema': 'm31-physical-independent-audit-v1', 'passed': True, 'complete': True,
                  'sourceManifestSha256': sha(manifest_raw), 'publicationPin': identity(BASE / 'source-publication.json', publication_raw),
                  'resultPin': identity(RESULTS / 'comparison.json', body), 'rawDataPins': raw_pins,
                  'evaluatorSupervisorPin': identity(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
                  'verifiedSourcePins': verified, 'sourcesPreserved': True, 'resultsPreserved': True,
                  'rawSelectedWordsChecked': observation_count, 'coordinateCellsChecked': 336,
                  'nominalCasesChecked': 12, 'sensitivityCasesChecked': sensitivity_count,
                  'arithmetic': 'Independent 70-digit Decimal model, explicit stacked rotor geometry, 160-step monotonic cubic enclosure.',
                  'modelComparisonTolerance': 'absolute error <= 2e-12 * max(1, abs(independent value)); numerical audit tolerance only',
                  'selectedObservationComparison': 'exact binary64 word equality after independent MATLAB v5 decode',
                  'calibratedPhysicalValidation': False, 'statisticalRejectionEstablished': False,
                  'scope': 'Saved-result arithmetic and data binding; no new cases, fitting, statistical CI, or experimental uncertainty calibration.',
                  'elapsedSeconds': time.monotonic() - START}
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'nominalCasesChecked': 12, 'sensitivityCasesChecked': sensitivity_count}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()
