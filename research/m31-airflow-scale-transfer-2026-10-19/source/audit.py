"""Independent, single-use audit of saved near-to-far airflow scale transfer.

No old/new producer imports, MAT decoding, wake calls or synthetic execution.
Launch only after public-source verification and the sole evaluator completes.
"""
from pathlib import Path
from decimal import Decimal, localcontext
import hashlib
import json
import math
import struct
import time

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
RESULTS = BASE / 'results'
PREVIOUS = 'research/m31-airflow-test-2026-10-19/'
INPUT = PREVIOUS + 'results/comparison.json'
INPUT_SIZE = 1112834
INPUT_SHA = 'dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3'
PREVIOUS_PUBLICATION = 'research/publication-receipts/m31-airflow-result-2026-10-19.json'
MIB = 1024 * 1024
CAP = 16 * MIB
TOLERANCE = Decimal('2e-12')
START = None
COUNTS = {'calibration': 800, 'evaluation': 2440, 'middle': 1640, 'far': 800}
ORIGINAL_FIELDS = {'row', 'column', 'index', 'X', 'Z', 'u', 'v', 'a', 'b', 'residualA', 'residualB'}
METRIC_FIELDS = {'count', 'mae', 'rmse', 'bias', 'nrmse'}
PREDECESSOR_FILES = {'PROTOCOL.md', 'source-manifest.json', 'source-publication.json',
                     'result-manifest.json', 'results/comparison.json', 'results/execution.json',
                     'results/evaluate-supervisor.json', 'results/audit.json', 'results/audit-supervisor.json'}
LIMITS = ['Already exposed same-dataset records; not blind or independent validation',
          'Empirical gains are not identified reference-speed calibrations',
          'Original RSS reference fitted to this experimental study',
          'Planar mean field; no3D wake, receiving-force or swarm validation',
          'No experimental uncertainty or statistical rejection',
          'Unknown spatially varying calibration and velocity observable differences remain']


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


def read_local(path, limit=CAP):
    guard()
    need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'local-path')
    need(path.stat().st_size <= limit, 'file-bound')
    return path.read_bytes()


def pin(path, raw):
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def verify_manifest(manifest):
    entries = manifest['files']
    need(type(entries) is list and 0 < len(entries) <= 10000, 'manifest-count')
    names = set()
    for entry in entries:
        guard()
        need(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'manifest-fields')
        name = entry['path']
        need(type(name) is str and name not in names and not Path(name).is_absolute()
             and '..' not in Path(name).parts, 'manifest-name')
        names.add(name)
        path = ROOT / name
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'manifest-path')
        need(type(entry['bytes']) is int and 0 <= entry['bytes'] <= 64 * MIB
             and path.stat().st_size == entry['bytes'], 'manifest-size')
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            while True:
                block = stream.read(MIB)
                if not block:
                    break
                guard()
                digest.update(block)
        need(digest.hexdigest() == entry['sha256'], 'manifest-sha256')
    prefix = BASE.relative_to(ROOT).as_posix() + '/'
    required = {prefix + name for name in ('PROTOCOL.md', 'source/evaluate.py', 'source/audit.py',
                                         'source/supervise.py', 'review/SOURCE-AUDIT.md')}
    required |= {PREVIOUS + name for name in PREDECESSOR_FILES}
    required.add(PREVIOUS_PUBLICATION)
    need(required <= names, 'manifest-required-input-and-receipts')
    return len(entries)


def D(value):
    return Decimal.from_float(value) if type(value) is float else Decimal(value)


def finite(value, label):
    need(type(value) in (int, float) and math.isfinite(value), label + '-finite-number')


def close(actual, expected, label):
    finite(actual, label)
    need(abs(D(actual) - D(expected)) <= TOLERANCE, label + '-absolute-tolerance')


def same_word(actual, expected, label):
    finite(actual, label)
    need(struct.pack('>d', actual) == struct.pack('>d', expected), label + '-binary64-word')


def check_success(receipt, mode, label):
    need(receipt['mode'] == mode and receipt['exitCode'] == 0
         and receipt['timeout'] is False and 0 <= receipt['elapsedSeconds'] < 60
         and receipt['outputLimitExceeded'] is False and receipt['outputCapBytes'] == CAP
         and type(receipt['savedBytesBeforeSupervisor']) is int
         and 0 <= receipt['savedBytesBeforeSupervisor'] <= CAP, label)


def prior_provenance(old, input_raw):
    """Bind the saved input to retained successful audit/publication receipts."""
    retained = {}
    for name in PREDECESSOR_FILES - {'results/comparison.json', 'PROTOCOL.md'}:
        retained[PREVIOUS + name] = read_local(ROOT / (PREVIOUS + name))
    retained[PREVIOUS_PUBLICATION] = read_local(ROOT / PREVIOUS_PUBLICATION)
    source_raw = retained[PREVIOUS + 'source-manifest.json']
    source_public = parse_json(retained[PREVIOUS + 'source-publication.json'])
    need(source_public['manifestSha256'] == sha(source_raw)
         and source_public['remoteBytesEqualLocal'] is True
         and source_public['committedBytesEqualLocal'] is True
         and old['sourceCommit'] == source_public['commit'], 'prior-public-source-binding')
    execution = parse_json(retained[PREVIOUS + 'results/execution.json'])
    need(execution['status'] == 'complete' and execution['resultBytes'] == len(input_raw)
         and execution['sha256'] == sha(input_raw), 'prior-execution-input-pin')
    audit = parse_json(retained[PREVIOUS + 'results/audit.json'])
    need(audit['passed'] is True and audit['complete'] is True
         and audit['resultPin'] == pin(ROOT / INPUT, input_raw)
         and audit['sourceManifestSha256'] == sha(source_raw), 'prior-independent-audit-binding')
    for mode in ('evaluate', 'audit'):
        check_success(parse_json(retained[PREVIOUS + 'results/' + mode + '-supervisor.json']),
                      mode, 'prior-' + mode + '-supervised-success')
    result_manifest_raw = retained[PREVIOUS + 'result-manifest.json']
    publication = parse_json(retained[PREVIOUS_PUBLICATION])
    need(publication['manifestPath'] == PREVIOUS + 'result-manifest.json'
         and publication['manifestBytes'] == len(result_manifest_raw)
         and publication['manifestSha256'] == sha(result_manifest_raw)
         and publication['remoteBytesEqualLocal'] is True
         and publication['committedBytesEqualLocal'] is True, 'prior-public-result-binding')
    entries = parse_json(result_manifest_raw)['files']
    matching = [entry for entry in entries if entry['path'] == INPUT]
    need(matching == [pin(ROOT / INPUT, input_raw)], 'prior-published-input-pin')
    return retained


def independent_gain(training, model):
    """Only the independently formed 800-record calibration tuple enters."""
    need(len(training) == 800, 'gain-training-count')
    numerator, denominator = Decimal(0), Decimal(0)
    for record in training:
        p, u = D(record[model]), D(record['u'])
        numerator += p * u
        denominator += p * p
    need(denominator > 0, 'positive-calibration-predictor-norm')
    gain = max(Decimal(0), numerator / denominator)
    need(gain.is_finite(), 'finite-independent-gain')
    return {'numerator': numerator, 'denominator': denominator, 'gain': gain}


def independent_metrics(records, prediction):
    """Equal-cell aggregate norm; normalized RMS is not mean percentage error."""
    need(len(records) > 0, 'nonempty-fixed-metric-group')
    absolute, squared, signed, observed_squared = (Decimal(0) for _ in range(4))
    for record in records:
        error = record[prediction] - record['u']
        absolute += abs(error)
        squared += error * error
        signed += error
        observed_squared += record['u'] * record['u']
    need(observed_squared > 0, 'positive-observed-group-norm')
    count = Decimal(len(records))
    return {'count': len(records), 'mae': absolute / count, 'rmse': (squared / count).sqrt(),
            'bias': signed / count, 'nrmse': (squared / observed_squared).sqrt()}


def check_metrics(stored, expected, label):
    need(type(stored) is dict and set(stored) == METRIC_FIELDS, label + '-fields')
    need(type(stored['count']) is int and stored['count'] == expected['count'], label + '-count')
    for field in METRIC_FIELDS - {'count'}:
        close(stored[field], expected[field], label + '-' + field)


def write_once(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    need(len(raw) <= CAP, 'audit-output-cap')
    with (RESULTS / name).open('xb') as stream:
        stream.write(raw)


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-completed-evaluator-directory')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved-only scale-transfer audit; no retries.\n')
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
        check_success(supervisor, 'evaluate', 'evaluator-supervised-success')
        later_files = {'evaluate-supervisor.json', 'audit.lock', 'audit-supervisor.lock',
                       'audit-stdout.txt', 'audit-stderr.txt'}
        saved_size = 0
        for directory in (RESULTS, BASE / 'ui'):
            if directory.exists():
                for path in directory.rglob('*'):
                    guard()
                    if path.is_file() and not (path.parent == RESULTS and path.name in later_files):
                        saved_size += path.stat().st_size
        need(saved_size == supervisor['savedBytesBeforeSupervisor'] and saved_size <= CAP, 'actual-saved-output-bytes')
        execution_raw = read_local(RESULTS / 'execution.json', MIB)
        execution = parse_json(execution_raw)
        body = read_local(RESULTS / 'comparison.json')
        need(execution['status'] == 'complete' and execution['resultBytes'] == len(body)
             and execution['sha256'] == sha(body) and 0 <= execution['elapsedSeconds'] < 60, 'completed-result-pin')
        result = parse_json(body)
        controls_raw = read_local(RESULTS / 'controls.json', MIB)
        need(parse_json(controls_raw) == {'passed': True, 'checks': ['exact gain', 'nonnegative clamp',
             'two positive scale invariances', 'degenerate denominator refused',
             'evaluation-only perturbation leaves calibration unchanged']}, 'saved-fixed-controls')
        need(type(result) is dict and set(result) == {'status', 'sourceCommit', 'inputPin', 'gains',
             'calibrationIndices', 'cases', 'subsets', 'evaluationChanges', 'limits'}, 'result-fields')
        need(result['status'] == 'completed-scale-transfer-diagnostic'
             and result['sourceCommit'] == publication['commit'] and result['limits'] == LIMITS, 'result-identity-and-limits')
        input_raw = read_local(ROOT / INPUT)
        need(len(input_raw) == INPUT_SIZE and sha(input_raw) == INPUT_SHA, 'immutable-saved-input-pin')
        need(result['inputPin'] == pin(ROOT / INPUT, input_raw), 'declared-input-pin')
        old = parse_json(input_raw)
        need(old['status'] == 'completed-descriptive-airflow-comparison'
             and old['counts']['accepted'] == 3240, 'predecessor-complete-status')
        provenance = prior_provenance(old, input_raw)
        original = old['cases']
        cases = result['cases']
        need(type(original) is list and type(cases) is list and len(original) == len(cases) == 3240, 'ordered-record-count')
        previous_index = -1
        for record in original:
            guard()
            need(type(record) is dict and set(record) == ORIGINAL_FIELDS, 'original-record-fields')
            need(all(type(record[key]) is int for key in ('row', 'column', 'index')), 'original-integer-indices')
            need(0 <= record['row'] < 272 and 0 <= record['column'] < 537
                 and record['row'] % 4 == 0 and record['column'] % 4 == 0
                 and record['index'] == record['column'] * 272 + record['row']
                 and record['index'] > previous_index, 'original-column-major-order-and-uniqueness')
            previous_index = record['index']
            for field in ORIGINAL_FIELDS - {'row', 'column', 'index', 'v'}:
                finite(record[field], 'original-' + field)
            if record['v'] is not None:
                finite(record['v'], 'original-v')
            need(8 <= record['Z'] <= 30 and abs(record['X']) <= 4
                 and record['a'] > 0 and record['b'] > 0, 'original-domain-and-positive-predictions')
        # These tuples are formed from original coordinates alone, before either fit.
        training = tuple(record for record in original if record['Z'] < 12)
        evaluation = tuple(record for record in original if record['Z'] >= 12)
        need(len(training) == 800 and len(evaluation) == 2440, 'calibration-evaluation-counts')
        need(type(result['calibrationIndices']) is list
             and all(type(index) is int for index in result['calibrationIndices'])
             and result['calibrationIndices'] == [record['index'] for record in training], 'exact-calibration-indices')
        need(type(result['gains']) is dict and set(result['gains']) == {'a', 'b'}, 'gain-fields')
        words = 0
        with localcontext() as context:
            context.prec = 60
            # No evaluation record is passed to either fit. Both gains are frozen
            # in this independent dictionary before any corrected value is made.
            gains = {model: independent_gain(training, model) for model in ('a', 'b')}
            for model in ('a', 'b'):
                stored = result['gains'][model]
                need(type(stored) is dict and set(stored) == {'numerator', 'denominator', 'gain'}, 'stored-gain-fields')
                for field, expected in gains[model].items():
                    close(stored[field], expected, model + '-gain-' + field)
                need(stored['denominator'] > 0 and stored['gain'] >= 0, 'stored-gain-domain')
                same_word(stored['gain'], max(0., stored['numerator'] / stored['denominator']), 'saved-gain-ratio-' + model)
            groups = {name: [] for name in COUNTS}
            for source, saved in zip(original, cases):
                guard()
                need(type(saved) is dict and set(saved) == ORIGINAL_FIELDS | {
                     'ca', 'cb', 'correctedResidualA', 'correctedResidualB', 'partition'}, 'extended-record-fields')
                for field in ORIGINAL_FIELDS:
                    if field in ('row', 'column', 'index'):
                        need(type(saved[field]) is int and saved[field] == source[field], 'preserved-' + field)
                    elif source[field] is None:
                        need(saved[field] is None, 'preserved-null-' + field)
                    else:
                        same_word(saved[field], source[field], 'preserved-' + field)
                        words += 1
                record = {'u': D(source['u']), 'a': D(source['a']), 'b': D(source['b'])}
                for model, residual in [('a', 'correctedResidualA'), ('b', 'correctedResidualB')]:
                    corrected = gains[model]['gain'] * record[model]
                    record['c' + model] = corrected
                    close(saved['c' + model], corrected, 'corrected-' + model)
                    close(saved[residual], corrected - record['u'], 'corrected-residual-' + model)
                    same_word(saved['c' + model], result['gains'][model]['gain'] * source[model], 'saved-corrected-product-' + model)
                    same_word(saved[residual], saved['c' + model] - source['u'], 'saved-corrected-subtraction-' + model)
                group = 'calibration' if source['Z'] < 12 else 'evaluation'
                need(saved['partition'] == group, 'coordinate-only-partition')
                groups[group].append(record)
                if group == 'evaluation':
                    groups['middle' if source['Z'] < 20 else 'far'].append(record)
            need({name: len(records) for name, records in groups.items()} == COUNTS, 'all-four-subset-counts')
            need(type(result['subsets']) is dict and set(result['subsets']) == set(COUNTS), 'subset-fields')
            metrics, metric_groups = {}, 0
            for name, records in groups.items():
                stored_subset = result['subsets'][name]
                need(type(stored_subset) is dict and set(stored_subset) == {'count', 'a', 'b'}
                     and type(stored_subset['count']) is int and stored_subset['count'] == COUNTS[name], 'subset-identity-' + name)
                metrics[name] = {}
                for model in ('a', 'b'):
                    need(type(stored_subset[model]) is dict and set(stored_subset[model]) == {'raw', 'corrected'}, 'metric-pair-fields')
                    metrics[name][model] = {}
                    for version, prediction in [('raw', model), ('corrected', 'c' + model)]:
                        expected = independent_metrics(records, prediction)
                        check_metrics(stored_subset[model][version], expected, name + '-' + model + '-' + version)
                        metrics[name][model][version] = expected
                        metric_groups += 1
            need(metric_groups == 16, 'complete-metric-coverage')
            need(type(result['evaluationChanges']) is dict and set(result['evaluationChanges']) == {'a', 'b'}, 'evaluation-change-models')
            for model in ('a', 'b'):
                changes = result['evaluationChanges'][model]
                need(type(changes) is dict and set(changes) == {'maeReduction', 'relativeMaeReduction'}, 'change-fields')
                before = metrics['evaluation'][model]['raw']['mae']
                after = metrics['evaluation'][model]['corrected']['mae']
                close(changes['maeReduction'], before - after, 'signed-evaluation-reduction-' + model)
                if before > 0:
                    close(changes['relativeMaeReduction'], 1 - after / before, 'relative-evaluation-reduction-' + model)
                else:
                    need(changes['relativeMaeReduction'] is None, 'zero-raw-mae-null-relative-change')
        need(verify_manifest(manifest) == verified, 'post-audit-frozen-files')
        retained = {BASE / 'source-manifest.json': manifest_raw, BASE / 'source-publication.json': publication_raw,
                    RESULTS / 'comparison.json': body, RESULTS / 'execution.json': execution_raw,
                    RESULTS / 'controls.json': controls_raw, RESULTS / 'evaluate-supervisor.json': supervisor_raw,
                    ROOT / INPUT: input_raw}
        retained.update({ROOT / name: raw for name, raw in provenance.items()})
        for path, raw in retained.items():
            need(read_local(path) == raw, 'unchanged-input-receipt-and-result-bytes')
        guard()
        report = {'schema': 'm31-airflow-scale-transfer-independent-audit-v1', 'passed': True, 'complete': True,
                  'sourceManifestSha256': sha(manifest_raw), 'verifiedSourcePins': verified,
                  'publicationPin': pin(BASE / 'source-publication.json', publication_raw),
                  'inputPin': pin(ROOT / INPUT, input_raw), 'resultPin': pin(RESULTS / 'comparison.json', body),
                  'evaluatorSupervisorPin': pin(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
                  'recordsChecked': 3240, 'originalBinary64WordsChecked': words, 'subsetCountsChecked': COUNTS,
                  'calibrationOnlyGainsChecked': 2, 'correctedPredictionsChecked': 6480, 'metricGroupsChecked': 16,
                  'primaryEndpointChecked': 'Corrected normalized RMS discrepancy over pooled evaluation cells, separately for both declared models.',
                  'arithmetic': 'Independent 60-digit Decimal gains and metrics from saved input words; no producer imports or wake evaluation.',
                  'tolerance': '2e-12 absolute on gains, saved fit sums, velocities and metrics; numerical consistency only.',
                  'calibrationUsesEvaluationCells': False, 'sourcesPreserved': True, 'inputPreserved': True, 'resultsPreserved': True,
                  'independentPhysicalValidation': False, 'identifiedReferenceSpeedCalibration': False,
                  'scope': 'Exposed within-dataset planar transfer diagnostic; no new measurements, raw PIV decoding, model replacement, statistical inference or uncertainty calibration.',
                  'elapsedSeconds': time.monotonic() - START}
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'recordsChecked': 3240, 'calibrationOnlyGainsChecked': 2,
                          'correctedPredictionsChecked': 6480, 'metricGroupsChecked': 16}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()
