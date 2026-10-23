"""Independent saved-phase attribution audit. Source preparation: compile only.

Scientific/producer modules are never imported. At its separately authorized
allocation, common.py provides only reviewed gating, identity reads, output and
supervision. All decimal parsing, rational partitioning, aggregation, ranking,
reconciliation and expected serialized evidence are independently implemented.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import io
import json
import math
import re
import sys
import common as infrastructure

BASE = infrastructure.BASE
ROOT = infrastructure.ROOT
REL = BASE.relative_to(ROOT).as_posix()
OLD = 'research/m31-radial-integration-2026-10-23'
OLD_COMMIT = '8c80900fdb5de6b1cf5b3b211c8a461ecac86f1a'
OLD_RECEIPT = 'research/publication-receipts/m31-radial-integration-result-2026-10-23.json'
OLD_PUBLIC_REVIEW = 'research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23.json'
WRAPPER = ('input','buildAndAdmission','schedule','solve','residual','loads','consumption','finalization')
KERNEL = ('input','index','geometry','admission')
SUCCESS_LEAVES = {'input','kernelInput','kernelIndex','geometry','kernelAdmission','buildUnassigned',
                  'schedule','solve','residual','loads','consumption','finalization','outerBoundary','timerResidual'}
REFUSAL_LEAVES = {'input','unfinishedPhaseAndFinalization','outerBoundary','timerResidual'}
QUERY_KEYS = {'call','window','rep','method','index','semantic','referenceSha256','referenceEqual',
              'comparisonMs','inputBeforeSha256','inputAfterSha256','inputPreserved','outerMs','status','reason',
              'cache','witness','excluded','encodePersistMs','methodValid','afterInput','baselineReferenceEqual',
              'baselineReferenceSha256','baselineSemanticSha256'}
CLOCK_BOUNDARY = 'raw current input through validation, copying, canonical ID order, native build/admission, ordered solve, residual, four loads, evidence fields and complete load-word/ID/status consumption'
METRICS = ('outerMs','innerMs','encodePersistMs','comparisonMs')
TOL = Fraction(1, 1000000)
MAX_METADATA = 16*1024**2
MAX_LINE = 4*1024**2
MAX_RESULTS = 128*1024**2
CHECKS = []
SOURCE_INPUT_BYTES = {}
PRODUCER_PINS = {}
SHA = re.compile(r'^[0-9a-f]{64}$')
DECIMAL_TOKEN = re.compile(r'^(-?)([0-9]+)(?:\.([0-9]+))?(?:[eE]([+-]?[0-9]+))?$')

EXPECTED_CONFIG = {'schema': 'm31-phase-attribution-v1', 'calls': 34560, 'stages': 1920, 'windows': 12, 'stagesPerWindow': 160, 'reps': [-1, 0, 1, 2, 3, 4, 5, 6, 7], 'toleranceMs': '0.000001', 'decimalPrecision': 80, 'primary': {'method': 'F', 'bucket': 'measured', 'status': 'native-success', 'majorityShare': '0.5', 'sameWinnerRepMinimum': 6, 'excludeFromRanking': ['timerResidual']}, 'allocations': {'producer': {'seconds': 300, 'mib': 128}, 'audit': {'seconds': 450, 'mib': 128}, 'finalize': {'seconds': 120, 'mib': 2}, 'ui': {'seconds': 180, 'mib': 16}}, 'readPolicy': {'attemptsPerFile': 3, 'gitReadTimeoutSeconds': 45}, 'inputs': {'queries': 'research/m31-radial-integration-2026-10-23/results/queries.jsonl', 'groups': 'research/m31-radial-integration-2026-10-23/results/groups.jsonl', 'oldSummary': 'research/m31-radial-integration-2026-10-23/results/summary.json', 'oldAudit': 'research/m31-radial-integration-2026-10-23/audit/audit.json', 'stages': 'research/m31-neighbor-density-2026-10-23/results/stages.jsonl', 'stageSummary': 'research/m31-neighbor-density-2026-10-23/results/summary.json'}}
FIXED_PRIOR_METADATA = {'research/m31-radial-integration-2026-10-23/result-manifest.json': {'bytes': 537067, 'sha256': '7b0871190878f7d034677beb0f23b9f995871dbdda3fdee0935cf80cb8bc2b34'}, 'research/publication-receipts/m31-radial-integration-result-2026-10-23.json': {'bytes': 11808, 'sha256': 'e1ea07eb2ac6211ca09787c88f5ff4c68bac99681de5ae7b2697df522822077e'}}


class AuditFailure(Exception):
    pass


def need(ok, label):
    if not ok:
        raise AuditFailure(label)


def strict_pairs(items):
    answer = {}
    for key, value in items:
        need(key not in answer, 'duplicate-json-key:'+key)
        answer[key] = value
    return answer


def reject_constant(token):
    raise AuditFailure('nonfinite-json-token:'+token)


def logged_decimal(token):
    """Convert the literal JSON decimal spelling without first using a float."""
    need(type(token) is str and len(token) <= 1024, 'bounded-decimal-token')
    match = DECIMAL_TOKEN.fullmatch(token)
    need(match is not None, 'decimal-token-shape')
    sign, whole, tail, exp = match.groups()
    tail = tail or ''
    exponent = int(exp or '0')
    need(abs(exponent) <= 1024, 'bounded-decimal-exponent')
    numerator = int(whole+tail)
    if sign:
        numerator = -numerator
    shift = exponent-len(tail)
    return Fraction(numerator*10**shift, 1) if shift >= 0 else Fraction(numerator, 10**(-shift))


def exact_json(raw):
    return json.loads(raw, object_pairs_hook=strict_pairs, parse_float=logged_decimal,
                      parse_int=int, parse_constant=reject_constant)


def ordinary_json(raw):
    # Only the inherited JSON result and non-arithmetic metadata use the same
    # ordinary parsed-JSON representation that the producer copies unchanged.
    def finite_float(token):
        result = float(token)
        need(math.isfinite(result), 'nonfinite-copied-metadata-number')
        return result
    return json.loads(raw, object_pairs_hook=strict_pairs, parse_float=finite_float,
                      parse_constant=reject_constant)


def rational(value, label='exact-timing-number'):
    need(type(value) in (int, Fraction), label)
    return Fraction(value)


def natural(value, lower, upper, label):
    need(type(value) is int and lower <= value <= upper, label)
    return value


def decimal_text(value):
    """Render terminating rational values exactly; no Decimal or rounding."""
    value = rational(value)
    if value == 0:
        return '0'
    denominator = value.denominator
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    need(denominator == 1, 'nonterminating-value-must-not-be-rendered-as-time')
    places = max(twos, fives)
    scaled = abs(value.numerator)*2**(places-twos)*5**(places-fives)
    digits = str(scaled).rjust(places+1, '0')
    text = digits if places == 0 else digits[:-places]+'.'+digits[-places:]
    if '.' in text:
        text = text.rstrip('0').rstrip('.')
    return ('-' if value < 0 else '')+text


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                       allow_nan=False)+'\n').encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_identity(pin):
    need(type(pin) is dict and 'bytes' in pin and 'sha256' in pin, 'pin-fields')
    natural(pin['bytes'], 1, 1024**3, 'bounded-pin-bytes')
    need(type(pin['sha256']) is str and SHA.fullmatch(pin['sha256']), 'pin-hash')
    return {'bytes':pin['bytes'], 'sha256':pin['sha256']}


def same(left, right, label):
    # Shape/type checks accompany arithmetic: booleans are not numeric counters.
    if type(left) is dict and type(right) is dict:
        need(set(left) == set(right), label+':keys')
        for key in left:
            same(left[key], right[key], label)
    elif type(left) is list and type(right) is list:
        need(len(left) == len(right), label+':length')
        for a, b in zip(left, right):
            same(a, b, label)
    else:
        need(type(left) is type(right) and left == right, label)


def input_bytes(path):
    need(path in infrastructure.PINS and infrastructure.PINS[path]['kind'] == 'input', 'required-immutable-input:'+path)
    raw = infrastructure.committed(path)
    SOURCE_INPUT_BYTES[path] = pin_identity(infrastructure.PINS[path])
    return raw


def producer_bytes(name, maximum=MAX_RESULTS):
    need(name and '/' not in name and '\\' not in name and name not in ('.','..'), 'producer-file-name')
    path = BASE/'results'/name
    need(path.is_file() and not path.is_symlink(), 'regular-producer-file:'+name)
    size = path.stat().st_size
    need(0 < size <= maximum, 'producer-file-size:'+name)
    raw = path.read_bytes()
    need(len(raw) == size, 'producer-capture-size:'+name)
    pin = {'file':'results/'+name, 'bytes':len(raw), 'sha256':digest(raw)}
    PRODUCER_PINS[pin['file']] = pin
    return raw


def source_and_prior_gate(out):
    pub = infrastructure.gate()
    same(infrastructure.CFG, EXPECTED_CONFIG, 'fixed-prospective-config')
    for name in ('config.json','PROTOCOL.md','SCHEMA.md','review/AUDIT-DESIGN.md','source/common.py',
                 'source/analyze.py','source/audit.py','source/launch.py','source/supervise.py',
                 'source/finalize.py','source/ui.cjs','runtime.json','input-pins.json',
                 'viewer/index.html','viewer/app.js'):
        need(infrastructure.PINS.get(REL+'/'+name,{}).get('kind') == 'source', 'required-source:'+name)
    for name in ('outputs/step02b-source/vendor/three.module.js','outputs/step02b-source/vendor/three.core.js',
                 'outputs/step02b-source/vendor/OrbitControls.js'):
        need(infrastructure.PINS.get(name,{}).get('kind') == 'source', 'required-renderer-closure:'+name)
    for relative, expected in FIXED_PRIOR_METADATA.items():
        same(pin_identity(infrastructure.PINS.get(relative)), expected, 'fixed-prior-metadata-pin')
    manifest = ordinary_json(input_bytes(OLD+'/result-manifest.json'))
    receipt = ordinary_json(input_bytes(OLD_RECEIPT))
    need(receipt['commit'] == OLD_COMMIT and receipt['manifestPath'] == OLD+'/result-manifest.json', 'fixed-prior-public-result')
    same({'bytes':receipt['manifestBytes'],'sha256':receipt['manifestSha256']},
         pin_identity(infrastructure.PINS[OLD+'/result-manifest.json']), 'prior-receipt-manifest-identity')
    need(receipt['remoteManifestBytesEqualLocal'] is True and receipt['committedManifestBytesEqualLocal'] is True
         and receipt['independentPublicReviewPassed'] is True and receipt['allAllocationsClosed'] is True,
         'prior-public-result-verified-and-closed')
    need(receipt['independentPublicReview']['path'] == OLD_PUBLIC_REVIEW, 'fixed-prior-public-review-path')
    same(pin_identity(infrastructure.PINS.get(OLD_PUBLIC_REVIEW)),
         pin_identity(receipt['independentPublicReview']), 'prior-public-review-receipt-binding')
    public_review = ordinary_json(input_bytes(OLD_PUBLIC_REVIEW))
    need(public_review['passed'] is True and public_review['independentReviewPassed'] is True
         and public_review['localBytesEqualPins'] is True and public_review['committedBytesEqualLocal'] is True
         and public_review['remoteBytesEqualLocal'] is True and public_review['allAllocationsClosedAtStartAndEnd'] is True,
         'prior-composite-public-review-complete-and-closed')
    same([public_review['commit'],public_review['manifestPath'],public_review['manifestBytes'],
          public_review['manifestSha256'],public_review['verifiedFilePins']],
         [receipt['commit'],receipt['manifestPath'],receipt['manifestBytes'],
          receipt['manifestSha256'],receipt['verifiedFilePins']], 'prior-composite-public-review-result-binding')
    public = {p['path']:p for p in manifest['files']}
    need(len(public) == len(manifest['files']) == receipt['verifiedFilePins'], 'prior-public-unique-pins')
    required = set(EXPECTED_CONFIG['inputs'].values()) | {
        OLD+'/ALLOCATION-CLOSURE.json', OLD+'/producer-supervisor.json', OLD+'/audit-supervisor.json',
        OLD+'/finalize-supervisor.json', OLD+'/ui-supervisor.json', OLD+'/audit/exit.json', OLD+'/results/exit.json'}
    for relative in required:
        same(pin_identity(infrastructure.PINS.get(relative)), pin_identity(public.get(relative)), 'prior-public-consumed-input')
    old = ordinary_json(input_bytes(EXPECTED_CONFIG['inputs']['oldSummary']))
    previous_audit = ordinary_json(input_bytes(EXPECTED_CONFIG['inputs']['oldAudit']))
    need(previous_audit['passed'] is True and previous_audit['evidenceIntegrityPassed'] is True
         and previous_audit['exactReferenceEquivalence'] is True and previous_audit['baselineStrictReferenceEquivalence'] is True,
         'prior-complete-scientific-audit')
    need(previous_audit['calls'] == old['calls'] == 34560 and previous_audit['stages'] == old['stages'] == 1920,
         'prior-fixed-population')
    same(previous_audit['summary'], old, 'prior-audit-summary-binding')
    need(old['complete'] is True and old['referenceEquality'] is True and old['costGate'] is False
         and old['coverageGate'] is False and old['keepGate'] is False, 'prior-negative-qualification-retained')
    old_pins = {p['file']:p for p in previous_audit['filePins']}
    for key in ('queries','groups','oldSummary'):
        relative = EXPECTED_CONFIG['inputs'][key]
        same(pin_identity(infrastructure.PINS[relative]), pin_identity(old_pins[relative[len(OLD)+1:]]),
             'prior-audited-log-group-summary-pin')
    closure = ordinary_json(input_bytes(OLD+'/ALLOCATION-CLOSURE.json'))
    need(closure['allClosed'] is True and closure['allPassedOperationally'] is True
         and closure['allocationsRetried'] is False and closure['nativeQueries'] == 34560
         and closure['costGate'] is False and closure['coverageGate'] is False and closure['keepGate'] is False,
         'prior-operational-vs-qualification-closure')
    for phase in ('producer','audit','finalize','ui'):
        record = ordinary_json(input_bytes(OLD+'/'+phase+'-supervisor.json'))
        same(record, closure['allocations'][phase], 'prior-supervisor-closure-binding')
        need(record['closed'] is True and record['returncode'] == 0 and record['allocationWallPassed'] is True
             and record['outputCapPassed'] is True, 'prior-successful-phase')
    old_exit = ordinary_json(input_bytes(OLD+'/audit/exit.json'))
    need(old_exit['closed'] is True and old_exit['exitCode'] == 0, 'prior-audit-internal-closed')
    old_producer_exit = ordinary_json(input_bytes(OLD+'/results/exit.json'))
    need(old_producer_exit['closed'] is True and old_producer_exit['exitCode'] == 0
         and old_producer_exit['calls'] == 34560, 'prior-producer-internal-closed')
    same(old_producer_exit['readEvents'],old['readEvents'],'prior-producer-read-history-retained')
    stage_summary = ordinary_json(input_bytes(EXPECTED_CONFIG['inputs']['stageSummary']))
    need(stage_summary['stages'] == 1920, 'prior-stage-summary-population')
    out.tick()
    CHECKS.append('reviewed public source/config and pinned prior public result, full-log audit, negative gates and closed allocations bound without rerunning prior work')
    return pub, old, previous_audit, {'commit':OLD_COMMIT,'verificationScope':receipt['verificationScope'],
        'publicTransportHistoryPreserved':True,'priorCostGate':False,'priorCoverageGate':False,'priorKeepGate':False}


def producer_gate():
    infrastructure.prior('producer')
    supervisor_path = BASE/'producer-supervisor.json'
    need(supervisor_path.is_file() and not supervisor_path.is_symlink(), 'producer-supervisor-regular')
    supervisor_raw = supervisor_path.read_bytes()
    supervisor = ordinary_json(supervisor_raw)
    need(supervisor['closed'] is True and type(supervisor['returncode']) is int and supervisor['returncode'] == 0
         and supervisor['allocationWallPassed'] is True and supervisor['outputCapPassed'] is True
         and not supervisor.get('timeout') and not supervisor.get('evidenceOverflow'), 'producer-successful-supervisor')
    PRODUCER_PINS['producer-supervisor.json'] = {'file':'producer-supervisor.json','bytes':len(supervisor_raw),'sha256':digest(supervisor_raw)}
    expected = {'launch.json','rows.jsonl','summary.json','viewer-rows.json','input-binding.json','exit.json'}
    paths = list((BASE/'results').iterdir())
    need({p.name for p in paths} == expected and all(p.is_file() and not p.is_symlink() for p in paths),
         'complete-regular-producer-inventory')
    need(sum(p.stat().st_size for p in paths) == supervisor['outputBytes'] <= MAX_RESULTS, 'producer-output-byte-cap')
    need(0 <= supervisor['wallSeconds'] <= EXPECTED_CONFIG['allocations']['producer']['seconds'], 'producer-supervisor-wall')
    launch = ordinary_json(producer_bytes('launch.json', MAX_METADATA))
    same(launch, {'singleUse':True,'nativeCalls':0}, 'producer-launch-evidence')
    closed = ordinary_json(producer_bytes('exit.json', MAX_METADATA))
    need(closed['closed'] is True and closed['exitCode'] == 0
         and 0 <= closed['wallSeconds'] <= EXPECTED_CONFIG['allocations']['producer']['seconds'], 'producer-internal-closed')
    need(type(closed['readEvents']) is list, 'producer-read-history')
    return closed


def lines(raw, label):
    for line in io.BytesIO(raw):
        need(len(line) <= MAX_LINE and line.endswith(b'\n') and line.strip(), label+'-bounded-complete-line')
        yield line


def stage_index(previous_audit):
    index = {}
    for ordinal, line in enumerate(lines(input_bytes(EXPECTED_CONFIG['inputs']['stages']), 'stages')):
        need(ordinal < 1920, 'no-extra-stage')
        row = ordinary_json(line)
        window, stage = divmod(ordinal, 160)
        need(type(row['window']) is int and type(row['index']) is int and row['window'] == window and row['index'] == stage,
             'fixed-stage-order')
        index[window,stage] = {k:row[k] for k in ('window','index','status','reason','nativeStage','admissionReasons','timeWord','caseId','globalOrdinal')}
    need(len(index) == 1920, 'complete-stage-population')
    bindings = previous_audit['inputBindings']
    need(type(bindings) is list and len(bindings) == 1920, 'prior-full-input-bindings')
    for ordinal, record in enumerate(bindings):
        window, stage = divmod(ordinal,160)
        need(record['window'] == window and record['index'] == stage, 'prior-input-binding-order')
        current = index[window,stage]
        for key in current:
            same(current[key], record[key], 'prior-stage-input-status-provenance')
        current['referenceSha256'] = record['sharedSemanticPin']['sha256']
        current['sharedSemanticPin'] = record['sharedSemanticPin']
        current['nativeInputSha256'] = record['nativeInputSha256']
        current['strictBaselineSemanticSha256'] = record['strictBaselineSemanticSha256']
    return index


def group_records():
    groups = [exact_json(x) for x in lines(input_bytes(EXPECTED_CONFIG['inputs']['groups']), 'old-groups')]
    need(len(groups) == 108, 'fixed-old-group-count')
    for ordinal, group in enumerate(groups):
        rep, window = ordinal//12-1, ordinal%12
        order = ['F','C'] if (rep+window+10)%2 == 0 else ['C','F']
        need(set(group) == {'window','rep','order','F','C','ratio'}, 'old-group-fields')
        same([group['rep'],group['window'],group['order']], [rep,window,order], 'original-balanced-group-order')
        for method in ('F','C'):
            arm = group[method]
            need(set(arm) == {'resetMs','sumQueryMs','totalMs','admittedMs','refusedMs','admittedCalls','refusedCalls'}, 'old-arm-fields')
            for key in ('resetMs','sumQueryMs','totalMs','admittedMs','refusedMs'):
                need(rational(arm[key]) >= 0, 'old-nonnegative-stream-time')
            natural(arm['admittedCalls'],0,160,'old-admitted-count')
            natural(arm['refusedCalls'],0,160,'old-refused-count')
            need(arm['admittedCalls']+arm['refusedCalls'] == 160, 'complete-old-stream-calls')
    return groups


def phase_partition(query, expected, stage):
    need(type(query) is dict and set(query) == QUERY_KEYS, 'original-query-exact-fields')
    call, rep, window, method, index = expected
    for key, value in (('call',call),('rep',rep),('window',window),('method',method),('index',index)):
        same(query[key], value, 'original-query-order')
    need(query['referenceEqual'] is True and query['inputPreserved'] is True and query['methodValid'] is True
         and query['afterInput'] is None, 'retained-prior-query-validation-flags')
    need(query['referenceSha256'] == query['semantic']['sha256'] == stage['referenceSha256']
         and query['inputBeforeSha256'] == query['inputAfterSha256'] == stage['nativeInputSha256'],
         'retained-reference-and-full-input-bindings')
    same(query['semantic'],stage['sharedSemanticPin'],'retained-full-shared-semantic-descriptor')
    if method == 'F':
        need(query['baselineReferenceEqual'] is True and query['baselineReferenceSha256'] == query['baselineSemanticSha256']
             == stage['strictBaselineSemanticSha256'], 'retained-stricter-baseline-flags')
    else:
        need(query['baselineReferenceEqual'] is None and query['baselineReferenceSha256'] is None
             and query['baselineSemanticSha256'] is None, 'candidate-baseline-only-fields-absent')
    same([query['status'],query['reason']], [stage['status'],stage['reason']], 'query-stage-status-reason')
    success = query['status'] == 'native-success'
    if success:
        need(query['reason'] is None and stage['nativeStage'] is None and stage['admissionReasons'] == [], 'fixed-success-schema')
    else:
        need(query['status'] == 'domain-refused' and query['reason'] == 'native-admission'
             and (window,index) == (2,159) and stage['nativeStage'] == 'build'
             and stage['admissionReasons'] == ['near-field'] and stage['timeWord'] == '400cf5c28f5c28f6',
             'only-inherited-near-field-build-refusal')
    excluded = query['excluded']
    timing = excluded['timing']
    need(set(timing) == {'clock','totalMs','phasesMs','boundary'} and timing['clock'] == 'performance.now'
         and timing['boundary'] == CLOCK_BOUNDARY, 'original-timing-clock-boundary')
    raw_phases = timing['phasesMs']
    need(type(raw_phases) is dict and set(raw_phases) == set(WRAPPER if success else ('input','finalization')),
         'status-specific-exact-wrapper-phase-keys')
    phases = {name:rational(raw_phases[name]) for name in raw_phases}
    need(all(value >= 0 for value in phases.values()), 'nonnegative-recorded-wrapper-phases')
    outer, inner = rational(query['outerMs']), rational(timing['totalMs'])
    need(outer >= 0 and inner >= 0, 'nonnegative-recorded-inner-outer')
    timer_residual = inner-sum(phases.values(), Fraction(0))
    outer_boundary = outer-inner
    need(abs(timer_residual) <= TOL and outer_boundary >= -TOL, 'fixed-wrapper-residual-boundary-tolerance')
    if success:
        need('diagnostics.buildPhasesMs' in excluded and type(excluded['diagnostics.buildPhasesMs']) is dict,
             'success-has-recorded-kernel-phases')
        raw_kernel = excluded['diagnostics.buildPhasesMs']
        need(set(raw_kernel) == set(KERNEL), 'exact-recorded-kernel-phase-keys')
        kernel = {key:rational(raw_kernel[key]) for key in KERNEL}
        need(all(value >= 0 for value in kernel.values()), 'nonnegative-recorded-kernel-phases')
        unassigned = phases['buildAndAdmission']-sum(kernel.values(), Fraction(0))
        need(unassigned >= -TOL, 'fixed-build-unassigned-tolerance')
        leaves = {key:phases[key] for key in WRAPPER if key != 'buildAndAdmission'}
        leaves.update(kernelInput=kernel['input'],kernelIndex=kernel['index'],geometry=kernel['geometry'],
                      kernelAdmission=kernel['admission'],buildUnassigned=unassigned)
    else:
        need('diagnostics.buildPhasesMs' not in excluded, 'refused-kernel-field-absent-not-null')
        kernel = None
        leaves = {'input':phases['input'], 'unfinishedPhaseAndFinalization':phases['finalization']}
    leaves.update(outerBoundary=outer_boundary,timerResidual=timer_residual)
    need(set(leaves) == (SUCCESS_LEAVES if success else REFUSAL_LEAVES), 'exact-disjoint-leaf-set')
    need(sum(leaves.values(),Fraction(0)) == outer, 'rational-disjoint-leaves-exactly-telescope-to-outer')
    evidence, comparison = rational(query['encodePersistMs']), rational(query['comparisonMs'])
    need(evidence >= 0 and comparison >= 0 and comparison <= evidence+TOL, 'nested-partial-evidence-interval')
    row = {'call':call,'window':window,'index':index,'rep':rep,'method':method,'status':query['status'],'reason':query['reason'],
           'outerMs':decimal_text(outer),'innerMs':decimal_text(inner),
           'phasesMs':{key:decimal_text(value) for key,value in sorted(phases.items())},
           'kernelPhasesMs':None if kernel is None else {key:decimal_text(value) for key,value in sorted(kernel.items())},
           'leavesMs':{key:decimal_text(value) for key,value in sorted(leaves.items())},
           'encodePersistMs':decimal_text(evidence),'comparisonMs':decimal_text(comparison)}
    numeric = {'outerMs':outer,'innerMs':inner,'encodePersistMs':evidence,'comparisonMs':comparison,'leavesMs':leaves}
    return row, numeric


def new_aggregate():
    return {'count':0, **{key:Fraction(0) for key in METRICS}, 'leavesMs':{}}


def accumulate(table, key, row):
    if key not in table:
        table[key] = new_aggregate()
    target = table[key]
    target['count'] += 1
    for name in METRICS:
        target[name] += row[name]
    for name, value in row['leavesMs'].items():
        target['leavesMs'][name] = target['leavesMs'].get(name,Fraction(0))+value


def aggregate_records(table, names):
    result = []
    for key, value in sorted(table.items()):
        need(value['count'] > 0, 'no-empty-aggregate')
        need(sum(value['leavesMs'].values(),Fraction(0)) == value['outerMs'], 'aggregate-leaf-conservation')
        record = dict(zip(names,key))
        record.update(count=value['count'], **{name:decimal_text(value[name]) for name in METRICS},
                      leavesMs={name:decimal_text(v) for name,v in sorted(value['leavesMs'].items())})
        result.append(record)
    return result


def largest_component(aggregate):
    need(aggregate['count'] > 0 and aggregate['outerMs'] > 0, 'positive-primary-and-repetition-denominator')
    candidates = [name for name in aggregate['leavesMs'] if name != 'timerResidual']
    need(candidates, 'nonempty-ranked-leaf-set')
    return min(candidates, key=lambda name:(-aggregate['leavesMs'][name],name))


def reconcile_groups(groups, buckets):
    result = []
    for group in groups:
        for method in ('F','C'):
            good = buckets.get((group['rep'],group['window'],method,'native-success'),new_aggregate())
            refused = buckets.get((group['rep'],group['window'],method,'domain-refused'),new_aggregate())
            arm = group[method]
            reset = rational(arm['resetMs'])
            total_queries = good['outerMs']+refused['outerMs']
            deltas = {'sumQueryMs':total_queries-rational(arm['sumQueryMs']),
                      'admittedMs':good['outerMs']-rational(arm['admittedMs']),
                      'refusedMs':refused['outerMs']-rational(arm['refusedMs']),
                      'totalMs':total_queries+reset-rational(arm['totalMs'])}
            need(all(abs(value) <= TOL for value in deltas.values()), 'fixed-exact-decimal-vs-logged-group-tolerance')
            need(good['count'] == arm['admittedCalls'] and refused['count'] == arm['refusedCalls'], 'group-status-count-reconciliation')
            result.append({'rep':group['rep'],'window':group['window'],'method':method,'resetMs':decimal_text(reset),
                'loggedTotalMs':decimal_text(rational(arm['totalMs'])),
                'signedDeltasMs':{name:decimal_text(value) for name,value in sorted(deltas.items())}})
    need(len(result) == 216, 'complete-group-reconciliation')
    return result


def reconstruct(out, pub, old, previous_audit, producer_summary, producer_rows):
    stages = stage_index(previous_audit)
    groups = group_records()
    source_stream = iter(lines(input_bytes(EXPECTED_CONFIG['inputs']['queries']), 'original-query-log'))
    result_stream = iter(lines(producer_rows, 'transformed-query-log'))
    pooled, per_rep, windows = {}, {}, {}
    representative = {}
    count = successes = refusals = 0
    for group in groups:
        rep, window = group['rep'],group['window']
        for method in group['order']:
            for index in range(160):
                out.tick()
                count += 1
                source_line = next(source_stream, None)
                result_line = next(result_stream, None)
                need(source_line is not None and result_line is not None, 'complete-original-and-transformed-stream')
                query = exact_json(source_line)
                row, numeric = phase_partition(query,(count,rep,window,method,index),stages[window,index])
                need(result_line == canonical(row), 'each-transformed-row-exact-canonical-bytes')
                successes += int(row['status'] == 'native-success')
                refusals += int(row['status'] == 'domain-refused')
                bucket = 'warmup' if rep == -1 else 'measured'
                accumulate(pooled,(bucket,method,row['status']),numeric)
                accumulate(per_rep,(rep,method,row['status']),numeric)
                accumulate(windows,(rep,window,method,row['status']),numeric)
                if rep == 0:
                    pair = representative.setdefault((window,index),{'window':window,'index':index,'status':row['status'],'methods':{}})
                    need(pair['status'] == row['status'] and method not in pair['methods'], 'representative-paired-status-unique-arm')
                    pair['methods'][method] = {name:row[name] for name in ('outerMs','innerMs','leavesMs')}
    need(next(source_stream,None) is None and next(result_stream,None) is None and count == 34560,
         'no-extra-original-or-transformed-rows')
    need(successes == 34542 and refusals == 18, 'complete-inherited-status-population')
    reconciled = reconcile_groups(groups,windows)
    primary = pooled[('measured','F','native-success')]
    leading = largest_component(primary)
    rep_winners = [{'rep':rep,'component':largest_component(per_rep[(rep,'F','native-success')])} for rep in range(8)]
    same_winner = sum(record['component'] == leading for record in rep_winners)
    majority = 2*primary['leavesMs'][leading] >= primary['outerMs']
    stable = majority and same_winner >= 6
    decision = {'largestComponent':leading,'numeratorMs':decimal_text(primary['leavesMs'][leading]),
        'denominatorMs':decimal_text(primary['outerMs']),'sameWinnerReps':same_winner,'perRepWinners':rep_winners,
        'atLeastHalf':majority,'stableMajority':stable,
        'classification':'stable-majority-component' if stable else 'distributed-or-unstable',
        'interpretation':'Descriptive priority for source inspection only; not a causal speedup prediction or a revised qualification gate.'}
    expected = {'schema':'m31-phase-attribution-result-v1','complete':True,'nativeCalls':0,'calls':count,'stages':1920,
        'arithmetic':'Exact sums/differences of logged decimal values at precision80; no extra measurement precision. Shares are numerator/denominator pairs, not rounded decisions.',
        'pooled':aggregate_records(pooled,('bucket','method','status')),
        'perRep':aggregate_records(per_rep,('rep','method','status')),
        'byWindowRep':aggregate_records(windows,('rep','window','method','status')),
        'groupReconciliation':reconciled,'decision':decision,'oldResult':old,'sourceCommit':pub['commit'],
        'scope':'Descriptive saved timing partition on exposed dependent N64 stages; no new force query, flight, speed measurement or physical validation.',
        'readEvents':producer_summary['readEvents']}
    need(type(producer_summary['readEvents']) is list, 'retained-producer-read-history')
    need(len(representative) == 1920, 'complete-representative-stage-population')
    viewer = []
    for key,pair in sorted(representative.items()):
        need(set(pair['methods']) == {'F','C'}, 'both-representative-methods-present')
        for arm in pair['methods'].values():
            need(('geometry' in arm['leavesMs']) is (pair['status'] == 'native-success'), 'refused-viewer-geometry-unavailable')
        viewer.append(pair)
    CHECKS.append('all 34560 exact-decimal row partitions byte-matched; inherited status/input/reference flags bound without new scientific comparison; no missing or extra rows')
    CHECKS.append('all pooled/per-repetition/window-status exact rational sums, 216 signed reset reconciliations, deterministic majority/stability branch and 1920 paired rep-zero viewer rows reconstructed')
    return expected, viewer, {'calls':count,'successes':successes,'refusals':refusals,'rowByteComparisons':count,
        'groupReconciliations':216,'viewerPairs':1920,'baselineStrictFlags':17280}


def main():
    out = infrastructure.Output('audit','audit')
    code = 0
    try:
        pub, old, previous_audit, prior_scope = source_and_prior_gate(out)
        closed = producer_gate()
        raw_rows = producer_bytes('rows.jsonl')
        raw_summary = producer_bytes('summary.json',MAX_METADATA)
        raw_viewer = producer_bytes('viewer-rows.json',MAX_METADATA)
        raw_binding = producer_bytes('input-binding.json',MAX_METADATA)
        producer_summary = ordinary_json(raw_summary)
        same(producer_summary['readEvents'],closed['readEvents'],'producer-summary-exit-read-history')
        expected_binding = {'sourceCommit':pub['commit'],'inputs':{key:infrastructure.PINS[path]
                            for key,path in EXPECTED_CONFIG['inputs'].items()},'nativeCalls':0}
        need(raw_binding == canonical(expected_binding),'producer-input-binding-exact-canonical-bytes')
        expected_summary, viewer, counts = reconstruct(out,pub,old,previous_audit,producer_summary,raw_rows)
        need(raw_summary == canonical(expected_summary),'all-summary-lists-decision-old-result-exact-canonical-bytes')
        viewer_raw = canonical(viewer)
        need(raw_viewer == viewer_raw,'independent-viewer-exact-canonical-bytes')
        for relative,pin in list(PRODUCER_PINS.items()):
            out.tick()
            infrastructure.checked_local(BASE/relative,pin)
        # Recheck frozen local source only; origin-Git inputs were already read
        # under immutable pins and their complete raw bytes are retained/cached.
        for pin in infrastructure.PINS.values():
            if pin['kind'] == 'source':
                out.tick(); infrastructure.checked_local(ROOT/pin['path'],pin)
        CHECKS.append('complete closed producer inventory, exact input/summary/viewer bytes and final producer/source identities checked; all previous allocations remain closed')
        report = {'schema':'m31-phase-attribution-audit-v1','passed':True,'calls':34560,'stages':1920,'nativeCalls':0,
            'sourceCommit':pub['commit'],'checks':CHECKS,'counts':counts,'summary':expected_summary,
            'filePins':[PRODUCER_PINS[key] for key in sorted(PRODUCER_PINS)],
            'viewerRowsPin':{'file':'audit/viewer-rows.json','bytes':len(viewer_raw),'sha256':digest(viewer_raw)},
            'sourceInputPins':[{'path':path,**pin} for path,pin in sorted(SOURCE_INPUT_BYTES.items())],
            'sourcePublication':pub,'priorPublicationScope':prior_scope,'readEvents':infrastructure.EVENTS,
            'producerReadEvents':closed['readEvents'],
            'independentArithmetic':{'engine':'fractions.Fraction with independently parsed literal logged decimals',
                'producerDecimalImported':False,'allSumsDifferencesExact':True,'allRowLeafTelescopesExact':True,
                'timeRendering':'terminating denominator factors 2 and 5; exact canonical decimal strings; no rounding',
                'ratioRepresentation':'numeratorMs and denominatorMs only; decisions by exact integer/rational comparisons',
                'clockPrecisionIncreased':False,'toleranceMs':'0.000001','signedValuesPreserved':True},
            'sharedInfrastructure':'common.py only for source/public gates, immutable-origin/local byte reads, output and allocation supervision; no producer partition/statistics code imported',
            'primaryScope':'measured successful F outer-query time; resets, refusals and warmup excluded from target denominator and retained separately',
            'limitations':['exact arithmetic on serialized decimal values is not exact underlying clock measurement',
                'kernel phases are nested; disjoint leaves include signed numerical residuals without clamping',
                'refused finalization contains unclosed wrapper build interval; kernel phases unavailable, not zero',
                'geometry combines cache/list/norm/rotor/assembly work; kernel admission includes graph and coefficient scaling',
                'buildUnassigned and outerBoundary are mixed boundary/work categories, not pure validation/copy cost',
                'comparisonMs is nested in partial encodePersistMs; neither is added to query partition or total process wall',
                'descriptive ranking and majority/stability labels do not establish causal speedup or revise failed prior gates',
                'previously exposed dependent N64 states; no new physical, holdout, scaling or full-flight evidence'],
            'priorCostGate':False,'priorCoverageGate':False,'priorKeepGate':False,
            'physicsValidated':False,'flightSafetyClaim':False,'statisticalInference':False,'researchComplete':False}
        out.save('viewer-rows.json',viewer)
        need((BASE/'audit/viewer-rows.json').read_bytes() == viewer_raw, 'auditor-viewer-written-exact-independent-bytes')
        out.save('audit.json',report)
    except Exception as error:
        code = 1
        out.failed = True
        out.save('failure.json' if (BASE/'audit/audit.json').exists() else 'audit.json',
                 {'schema':'m31-phase-attribution-audit-v1','passed':False,'nativeCalls':0,
                  'failureType':type(error).__name__,
                  'message':str(error).replace(str(ROOT),'[repository]')[:1500],
                  'checksCompleted':CHECKS,'readEvents':infrastructure.EVENTS,'closedWithoutRetry':True})
    finally:
        out.close(code)
    return code


if __name__ == '__main__':
    sys.exit(main())
