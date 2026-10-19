"""Single independent saved cross-component audit. No producer imports or refits.
Only launch after exact-public source verification and evaluator completion.
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
MIB = 1024 * 1024
CAP = 16 * MIB
START = None
TOLERANCE = Decimal('2e-12')
AIRFLOW = 'research/m31-airflow-test-2026-10-19/'
TRANSFER = 'research/m31-airflow-scale-transfer-2026-10-19/'
INPUT = AIRFLOW + 'results/comparison.json'
PRIOR = TRANSFER + 'results/comparison.json'
PINS = {
    INPUT: (1112834, 'dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3'),
    PRIOR: (1766917, '027165cb42fe4445496779d3f4cdb87a902248d38cdf9a8ddc4adfa1b042d269'),
}
PUBLICATIONS = {
    AIRFLOW: 'research/publication-receipts/m31-airflow-result-2026-10-19.json',
    TRANSFER: 'research/publication-receipts/m31-airflow-scale-result-2026-10-19.json',
}
GAIN = .5450089857597356
ORIGINAL_FIELDS = {'row', 'column', 'index', 'X', 'Z', 'u', 'v', 'a', 'b', 'residualA', 'residualB'}
GEOMETRY_FIELDS = {'radius', 'xi', 'axialCore', 'radialCandidate', 'candidate', 'baseline'}
METRIC_FIELDS = {'count', 'mae', 'rmse', 'bias', 'nrmse'}
PREDECESSOR_FILES = {'PROTOCOL.md', 'source-manifest.json', 'source-publication.json',
                     'result-manifest.json', 'results/comparison.json', 'results/execution.json',
                     'results/evaluate-supervisor.json', 'results/audit.json', 'results/audit-supervisor.json'}
LIMITS = ['Exposed same-experiment component diagnostic, not blind or independent validation',
          'Positive lateral v assumed along increasing x; preprocessing unavailable',
          'Empirical inherited gain is not SI calibration',
          'Axisymmetric steady core completion only; no global continuity or momentum claim',
          'No receiving-force, flight, flocking, safety or novelty claim',
          'No experimental uncertainty or statistical rejection']


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


def write_once(name, value):
    raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    need(len(raw) <= CAP, 'audit-output-cap')
    with (RESULTS / name).open('xb') as stream:
        stream.write(raw)



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
                'source/supervise.py', 'review/SOURCE-AUDIT.md', 'review/GEOMETRY-AND-CONTINUITY.md')}
    for predecessor, publication in PUBLICATIONS.items():
        required |= {predecessor + name for name in PREDECESSOR_FILES}
        required.add(publication)
    need(required <= names, 'manifest-required-inputs-and-provenance')
    return len(entries)


def predecessor_chain(prefix, document, raw):
    retained = {}
    for name in PREDECESSOR_FILES - {'PROTOCOL.md', 'results/comparison.json'}:
        retained[prefix + name] = read_local(ROOT / (prefix + name))
    publication_path = PUBLICATIONS[prefix]
    retained[publication_path] = read_local(ROOT / publication_path)
    source_raw = retained[prefix + 'source-manifest.json']
    source_public = parse_json(retained[prefix + 'source-publication.json'])
    need(source_public['manifestSha256'] == sha(source_raw)
         and source_public['remoteBytesEqualLocal'] is True
         and source_public['committedBytesEqualLocal'] is True
         and document['sourceCommit'] == source_public['commit'], 'prior-source-binding')
    result_path = ROOT / (prefix + 'results/comparison.json')
    execution = parse_json(retained[prefix + 'results/execution.json'])
    need(execution['status'] == 'complete' and execution['resultBytes'] == len(raw)
         and execution['sha256'] == sha(raw), 'prior-execution-binding')
    audit = parse_json(retained[prefix + 'results/audit.json'])
    need(audit['passed'] is True and audit['complete'] is True
         and audit['resultPin'] == pin(result_path, raw)
         and audit['sourceManifestSha256'] == sha(source_raw), 'prior-audit-binding')
    for mode in ('evaluate', 'audit'):
        check_success(parse_json(retained[prefix + 'results/' + mode + '-supervisor.json']),
                      mode, 'prior-' + mode + '-supervised-success')
    result_manifest_raw = retained[prefix + 'result-manifest.json']
    publication = parse_json(retained[publication_path])
    need(publication['manifestPath'] == prefix + 'result-manifest.json'
         and publication['manifestBytes'] == len(result_manifest_raw)
         and publication['manifestSha256'] == sha(result_manifest_raw)
         and publication['remoteBytesEqualLocal'] is True
         and publication['committedBytesEqualLocal'] is True, 'prior-public-result-binding')
    matching = [entry for entry in parse_json(result_manifest_raw)['files']
                if entry['path'] == prefix + 'results/comparison.json']
    need(matching == [pin(result_path, raw)], 'prior-published-result-pin')
    return retained


def independent_completion(x_raw, z_raw, inherited_gain):
    """Rational integral-of-continuity form; no producer xi-polynomial calls."""
    x, z, gain = D(x_raw), D(z_raw), D(inherited_gain)
    root_two = Decimal(2).sqrt()
    c = root_two - 1
    diameter = 2 * root_two
    shifted = z + Decimal('5.817') * diameter
    width = Decimal('.07668') * shifted
    width_squared = width * width
    radius_squared = x * x + 1
    radius = radius_squared.sqrt()
    center = gain * Decimal('10.11') * diameter / shifted
    denominator = (width_squared + c * radius_squared) ** 2
    factor = center * Decimal('.07668') * width * (width_squared - c * radius_squared) / (2 * denominator)
    axial = center * width_squared ** 2 / denominator
    need(z >= Decimal('2.5') * diameter and z * Decimal('.0325') < 2, 'inactive-axial-fade-and-near-admission')
    return {'radius': radius, 'xi': radius / width, 'axialCore': axial,
            'radialCandidate': factor * radius, 'candidate': factor * x, 'baseline': Decimal(0)}


def independent_metrics(records, model):
    if not records:
        return None
    absolute, squared, signed, observed = (Decimal(0) for _ in range(4))
    for record in records:
        error = record[model] - record['v']
        absolute += abs(error)
        squared += error * error
        signed += error
        observed += record['v'] * record['v']
    count = Decimal(len(records))
    return {'count': len(records), 'mae': absolute / count, 'rmse': (squared / count).sqrt(),
            'bias': signed / count, 'nrmse': (squared / observed).sqrt() if observed > 0 else None}


def verify_metrics(stored, expected, label):
    if expected is None:
        need(stored is None, label + '-empty-null')
        return
    need(type(stored) is dict and set(stored) == METRIC_FIELDS, label + '-fields')
    need(type(stored['count']) is int and stored['count'] == expected['count'], label + '-count')
    for field in METRIC_FIELDS - {'count'}:
        if expected[field] is None:
            need(stored[field] is None, label + '-' + field + '-zero-norm-null')
        else:
            close(stored[field], expected[field], label + '-' + field)


def main():
    global START
    START = time.monotonic()
    need(RESULTS.is_dir(), 'requires-completed-evaluator-directory')
    with (RESULTS / 'audit.lock').open('x') as stream:
        stream.write('One independent saved cross-component audit; no retries.\n')
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
        controls = parse_json(controls_raw)
        need(set(controls) == {'passed', 'checks', 'continuityResiduals', 'continuityTolerance'}
             and controls['passed'] is True and controls['checks'] == [
             'odd symmetry at three fixed points', 'plane radial projection identity',
             'radial zero crossing', 'regular radial axis limit', 'three finite-difference continuity controls',
             'zero baseline metric', 'core boundary and missing-value precedence'], 'saved-control-identity')
        same_word(controls['continuityTolerance'], 2e-8, 'fixed-continuity-control-tolerance')
        need(type(controls['continuityResiduals']) is list and len(controls['continuityResiduals']) == 3, 'continuity-control-count')
        for value in controls['continuityResiduals']:
            finite(value, 'saved-continuity-residual')
            need(abs(value) < 2e-8, 'saved-continuity-control-bound')
        need(type(result) is dict and set(result) == {'status', 'sourceCommit', 'inputs', 'inheritedGain',
             'cases', 'includedCount', 'exclusions', 'subsets', 'primaryContrast', 'limits'}, 'result-fields')
        need(result['status'] == 'completed-cross-component-diagnostic'
             and result['sourceCommit'] == publication['commit'] and result['limits'] == LIMITS, 'result-identity-and-limits')
        raw_inputs, documents, provenance = {}, {}, {}
        for path, (length, digest) in PINS.items():
            raw = read_local(ROOT / path)
            need(len(raw) == length and sha(raw) == digest, 'fixed-input-pin')
            raw_inputs[path] = raw
            documents[path] = parse_json(raw)
        need(result['inputs'] == [pin(ROOT / path, raw) for path, raw in raw_inputs.items()], 'declared-ordered-inputs')
        old, prior = documents[INPUT], documents[PRIOR]
        need(old['status'] == 'completed-descriptive-airflow-comparison'
             and old['counts']['accepted'] == 3240
             and prior['status'] == 'completed-scale-transfer-diagnostic', 'predecessor-complete-status')
        need(prior['inputPin'] == pin(ROOT / INPUT, raw_inputs[INPUT]), 'gain-derived-from-fixed-saved-field')
        same_word(prior['gains']['a']['gain'], GAIN, 'prior-exact-gain')
        same_word(result['inheritedGain'], GAIN, 'current-exact-inherited-gain')
        for prefix, path in ((AIRFLOW, INPUT), (TRANSFER, PRIOR)):
            provenance.update(predecessor_chain(prefix, documents[path], raw_inputs[path]))
        original, cases = old['cases'], result['cases']
        need(type(original) is list and type(cases) is list and len(original) == len(cases) == 3240, 'ordered-original-record-count')
        groups = {'primary': [], 'near': [], 'middle': [], 'far': []}
        exclusions = {'outside-core': 0, 'missing-lateral': 0}
        included, words, previous_index = 0, 0, -1
        primary_z = set()
        with localcontext() as context:
            context.prec = 60
            for source, saved in zip(original, cases):
                guard()
                need(type(source) is dict and set(source) == ORIGINAL_FIELDS, 'original-record-fields')
                need(all(type(source[k]) is int for k in ('row', 'column', 'index')), 'original-index-types')
                need(0 <= source['row'] < 272 and 0 <= source['column'] < 537
                     and source['row'] % 4 == 0 and source['column'] % 4 == 0
                     and source['index'] == source['column'] * 272 + source['row']
                     and source['index'] > previous_index, 'original-ordered-unique-indices')
                previous_index = source['index']
                for field in ORIGINAL_FIELDS - {'row', 'column', 'index', 'v'}:
                    finite(source[field], 'original-' + field)
                if source['v'] is not None:
                    finite(source['v'], 'original-v')
                need(8 <= source['Z'] <= 30 and abs(source['X']) <= 4, 'original-geometric-domain')
                need(type(saved) is dict and set(saved) == GEOMETRY_FIELDS | {
                     'original', 'included', 'excludedReason', 'residual'}, 'case-fields')
                need(type(saved['original']) is dict and set(saved['original']) == ORIGINAL_FIELDS, 'copied-original-fields')
                for field in ORIGINAL_FIELDS:
                    actual, expected = saved['original'][field], source[field]
                    if field in ('row', 'column', 'index'):
                        need(type(actual) is int and actual == expected, 'preserved-integer-' + field)
                    elif expected is None:
                        need(actual is None, 'preserved-null-' + field)
                    else:
                        same_word(actual, expected, 'preserved-' + field)
                        words += 1
                predicted = independent_completion(source['X'], source['Z'], GAIN)
                for field in GEOMETRY_FIELDS:
                    close(saved[field], predicted[field], 'independent-' + field)
                same_word(saved['baseline'], 0., 'exact-zero-baseline')
                # Core selection uses independent high-precision geometry, never residuals.
                reason = 'outside-core' if predicted['xi'] > 2 else 'missing-lateral' if source['v'] is None else None
                need(type(saved['included']) is bool and saved['included'] == (reason is None)
                     and saved['excludedReason'] == reason, 'independent-selection-and-precedence')
                if reason is not None:
                    exclusions[reason] += 1
                    need(saved['residual'] is None, 'excluded-residual-null')
                    continue
                included += 1
                expected_residual = predicted['candidate'] - D(source['v'])
                close(saved['residual'], expected_residual, 'included-signed-residual')
                same_word(saved['residual'], saved['candidate'] - source['v'], 'saved-residual-subtraction')
                record = {'v': D(source['v']), 'baseline': Decimal(0), 'candidate': predicted['candidate']}
                if source['Z'] >= 12:
                    groups['primary'].append(record)
                    primary_z.add(source['Z'])
                    groups['middle' if source['Z'] < 20 else 'far'].append(record)
                else:
                    groups['near'].append(record)
            need(type(result['includedCount']) is int and result['includedCount'] == included, 'included-count')
            need(type(result['exclusions']) is dict and set(result['exclusions']) == set(exclusions)
                 and all(type(n) is int for n in result['exclusions'].values())
                 and result['exclusions'] == exclusions and included + sum(exclusions.values()) == 3240, 'exclusion-partition')
            need(len(groups['primary']) >= 20 and len(primary_z) >= 3
                 and sum(record['v'] ** 2 for record in groups['primary']) > 0, 'primary-admission')
            need(type(result['subsets']) is dict and set(result['subsets']) == set(groups), 'group-labels')
            metric_groups, metrics = 0, {}
            for label, records in groups.items():
                stored = result['subsets'][label]
                need(type(stored) is dict and set(stored) == {'count', 'baseline', 'candidate'}
                     and type(stored['count']) is int and stored['count'] == len(records), 'group-count-' + label)
                metrics[label] = {}
                for model in ('baseline', 'candidate'):
                    expected = independent_metrics(records, model)
                    verify_metrics(stored[model], expected, label + '-' + model)
                    metrics[label][model] = expected
                    metric_groups += 1
                if metrics[label]['baseline'] is not None and metrics[label]['baseline']['nrmse'] is not None:
                    same_word(stored['baseline']['nrmse'], 1., 'baseline-unit-nrmse-' + label)
            need(metric_groups == 8, 'eight-metric-groups')
            contrast = result['primaryContrast']
            need(type(contrast) is dict and set(contrast) == {'rmseReduction', 'relativeRmseReduction'}, 'contrast-fields')
            baseline = metrics['primary']['baseline']['rmse']
            candidate = metrics['primary']['candidate']['rmse']
            need(baseline > 0, 'positive-baseline-primary-rmse')
            close(contrast['rmseReduction'], baseline - candidate, 'primary-signed-rmse-reduction')
            close(contrast['relativeRmseReduction'], 1 - candidate / baseline, 'primary-relative-rmse-reduction')
            saved_b = result['subsets']['primary']['baseline']['rmse']
            saved_c = result['subsets']['primary']['candidate']['rmse']
            same_word(contrast['rmseReduction'], saved_b - saved_c, 'saved-contrast-subtraction')
            same_word(contrast['relativeRmseReduction'], 1 - saved_c / saved_b, 'saved-relative-contrast')
        need(verify_manifest(manifest) == verified, 'post-audit-source-pins')
        retained = {BASE / 'source-manifest.json': manifest_raw, BASE / 'source-publication.json': publication_raw,
                    RESULTS / 'comparison.json': body, RESULTS / 'execution.json': execution_raw,
                    RESULTS / 'controls.json': controls_raw, RESULTS / 'evaluate-supervisor.json': supervisor_raw}
        retained.update({ROOT / name: raw for name, raw in raw_inputs.items()})
        retained.update({ROOT / name: raw for name, raw in provenance.items()})
        for path, raw in retained.items():
            need(read_local(path) == raw, 'unchanged-saved-input-source-result-receipts')
        guard()
        report = {'schema': 'm31-crossstream-independent-audit-v1', 'passed': True, 'complete': True,
                  'sourceManifestSha256': sha(manifest_raw), 'verifiedSourcePins': verified,
                  'publicationPin': pin(BASE / 'source-publication.json', publication_raw),
                  'inputPins': [pin(ROOT / name, raw) for name, raw in raw_inputs.items()],
                  'resultPin': pin(RESULTS / 'comparison.json', body),
                  'evaluatorSupervisorPin': pin(RESULTS / 'evaluate-supervisor.json', supervisor_raw),
                  'originalRecordsChecked': 3240, 'originalBinary64WordsChecked': words,
                  'candidateRecordsChecked': 3240, 'includedCountChecked': included,
                  'exclusionsChecked': exclusions, 'groupCountsChecked': {label: len(rows) for label, rows in groups.items()},
                  'metricGroupsChecked': 8, 'inheritedGainExact': True, 'newFits': 0,
                  'arithmetic': 'Independent 60-digit Decimal rational integral-of-continuity expression and metrics; no producer imports or old scientific rerun.',
                  'tolerance': '2e-12 absolute numerical consistency only; exact original binary64 preservation and exact inherited gain.',
                  'completionAssumptions': 'Steady incompressible axisymmetric axial profile, regular axis, zero mean azimuthal velocity; local unfaded core only.',
                  'sourcesPreserved': True, 'inputsPreserved': True, 'resultsPreserved': True,
                  'independentPhysicalValidation': False, 'globalContinuityEstablished': False,
                  'scope': 'Previously exposed saved planar lateral component; no sign fitting, SI calibration, statistical inference or flight validation.',
                  'elapsedSeconds': time.monotonic() - START}
        write_once('audit.json', report)
        print(json.dumps({'passed': True, 'originalRecordsChecked': 3240,
                          'includedCountChecked': included, 'metricGroupsChecked': 8}))
    except BaseException as error:
        write_once('audit-failure.json', {'passed': False, 'errorType': type(error).__name__,
                   'error': str(error)[:500], 'elapsedSeconds': time.monotonic() - START})
        raise


if __name__ == '__main__':
    main()
