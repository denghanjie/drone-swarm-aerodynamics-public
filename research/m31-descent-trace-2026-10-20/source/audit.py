"""Independent saved-row selection and scalar audit; source-only until frozen.

The common helper supplies verified bytes, gzip and JSON parsing. Its parsing is
shared, not independently implemented here. No extractor, controller, simulator
or native module is imported or invoked. Only controller/k1 samples are computed.
"""
from pathlib import Path
import hashlib
import json
import math
import re
import struct
import sys
import time

import common as C

B, R = C.BASE, C.ROOT
MAX_OUTPUT = 2*1024*1024
MAX_EXTRACT_OUTPUT = 32*1024*1024
FOCUS = 17
CASES = ('seed2026102001-h005', 'seed2026102001-h0025',
         'seed2026102002-h005', 'seed2026102002-h0025')
FIELDS = ('z', 'vz', 'desiredVz', 'targetZ', 'requestRaw',
          'requestedNetAcceleration', 'commandTotal', 'nominalTotal',
          'nativeAxisZ', 'nominalFz', 'deliveredFz', 'forceShortfall',
          'nominalWeightRatio', 'deliveredWeightRatio', 'deliveredNetAcceleration')
CONDITIONS = ('desiredUp', 'movingDown', 'requestUp', 'acceleratingDown',
              'desiredUpWhileMovingDown', 'requestUpWhileAcceleratingDown')
HEX = re.compile(r'^[0-9a-f]{16}$')
SHA = re.compile(r'^[0-9a-f]{64}$')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def word(value):
    return struct.pack('>d', float(value)).hex()


def decode(value):
    require(isinstance(value, str) and HEX.fullmatch(value), 'invalid-binary64-word')
    number = struct.unpack('>d', bytes.fromhex(value))[0]
    require(math.isfinite(number), 'nonfinite-binary64-word')
    return number


def words(value, size):
    require(type(value) is list and len(value) == size, 'word-vector-size')
    for item in value:
        decode(item)
    return value


def integer(value, minimum, maximum, label):
    require(type(value) is int and minimum <= value <= maximum, label)
    return value


def exact(actual, expected, label):
    """JSON structure, with finite numbers compared by binary64 words."""
    if type(expected) is bool or expected is None or isinstance(expected, str):
        require(type(actual) is type(expected) and actual == expected, label)
    elif type(expected) in (int, float):
        require(type(actual) in (int, float) and math.isfinite(actual), label)
        require(word(actual) == word(expected), label)
    elif type(expected) is list:
        require(type(actual) is list and len(actual) == len(expected), label)
        for left, right in zip(actual, expected):
            exact(left, right, label)
    elif type(expected) is dict:
        require(type(actual) is dict and set(actual) == set(expected), label)
        for key in expected:
            exact(actual[key], expected[key], label+':'+key)
    else:
        raise RuntimeError('unexpected-comparison-type')


def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate-artifact-json-key')
        result[key] = value
    return result


def invalid_constant(value):
    raise RuntimeError('nonfinite-artifact-json-number')


def finite_float(text):
    result = float(text)
    require(math.isfinite(result), 'overflowing-artifact-json-number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=invalid_constant, parse_float=finite_float)


def local_json(path):
    C.guard()
    require(path.is_file() and not path.is_symlink(), 'json-path')
    require(path.stat().st_size <= MAX_EXTRACT_OUTPUT, 'json-byte-limit')
    return parse(path.read_bytes())


def identity(path):
    raw = path.read_bytes()
    require(len(raw) <= MAX_EXTRACT_OUTPUT, 'artifact-byte-limit')
    return {'file': path.relative_to(B).as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}, raw


def verify_pin(value, filename, maximum):
    require(type(value) is dict and set(value) == {'file', 'bytes', 'sha256'}, 'artifact-pin-shape')
    exact(value['file'], filename, 'artifact-pin-file')
    integer(value['bytes'], 1, maximum, 'artifact-pin-size')
    require(isinstance(value['sha256'], str) and SHA.fullmatch(value['sha256']), 'artifact-pin-hash')
    return C.checked(B/filename, value)


def pick(rows, label):
    require(type(rows) is list and len(rows) == 64, label+':row-count')
    require(all(type(row) is dict and type(row.get('id')) is int for row in rows), label+':id-type')
    exact([row['id'] for row in rows], list(range(64)), label+':unique-canonical-ids')
    row = rows[FOCUS]
    integer(row['id'], FOCUS, FOCUS, label+':focus-id')
    return row


def full_input(value):
    require(type(value) is dict and set(value) == {'drones'}, 'input-shape')
    pick(value['drones'], 'input')
    for row in value['drones']:
        require(set(row) == {'id', 'state'} and type(row['state']) is list and len(row['state']) == 17, 'input-state-shape')
        require(all(isinstance(w, str) and HEX.fullmatch(w) for w in row['state']), 'input-state-word-shape')
    return value


def rotor_sum(saved):
    words(saved, 4)
    answer = 0.0
    for rotor in saved:
        answer = answer + decode(rotor)
    return answer


def derive(controller, derivative, prepared, load):
    # Independently written scalar arithmetic; no steering/control regeneration.
    state = words(controller['stateWords'], 17)
    height, speed = decode(state[2]), decode(state[5])
    desired = decode(words(controller['desiredVelocityWords'], 3)[2])
    target = decode(controller['target']['zWord'])
    built_target = height + (2.5*desired + 1.5*speed)/6
    exact(controller['target']['zWord'], word(built_target), 'saved-target-construction')
    target_delta = target-height
    raw_request = 6*target_delta - 4*speed
    if raw_request < -4:
        request = -4.0
    elif raw_request > 5:
        request = 5.0
    else:
        request = raw_request
    command_sum = rotor_sum(controller['commandsWords'])
    nominal_sum = rotor_sum(prepared['forces'])
    axis_z = decode(words(prepared['axis'], 3)[2])
    nominal_force_z = axis_z*nominal_sum
    delivered_force_z = decode(words(load['worldForce'], 3)[2])
    net_acceleration = delivered_force_z/.027 - 9.81
    exact(derivative['derivativeWords'][5], word(net_acceleration), 'delivered-vertical-derivative')
    exact(prepared['nativeTotal'], word(nominal_sum), 'prepared-nominal-total')
    mass_weight = .027*9.81
    values = {
        'z': height, 'vz': speed, 'desiredVz': desired, 'targetZ': target,
        'requestRaw': raw_request, 'requestedNetAcceleration': request,
        'commandTotal': command_sum, 'nominalTotal': nominal_sum,
        'nativeAxisZ': axis_z, 'nominalFz': nominal_force_z,
        'deliveredFz': delivered_force_z,
        'forceShortfall': nominal_force_z-delivered_force_z,
        'nominalWeightRatio': nominal_force_z/mass_weight,
        'deliveredWeightRatio': delivered_force_z/mass_weight,
        'deliveredNetAcceleration': net_acceleration}
    require(set(values) == set(FIELDS) and all(math.isfinite(v) for v in values.values()), 'metric-fields-or-range')
    return values


def predicates(values):
    result = {'desiredUp': values['desiredVz'] > 0,
              'movingDown': values['vz'] < 0,
              'requestUp': values['requestedNetAcceleration'] > 0,
              'acceleratingDown': values['deliveredNetAcceleration'] < 0}
    result['desiredUpWhileMovingDown'] = result['desiredUp'] and result['movingDown']
    result['requestUpWhileAcceleratingDown'] = result['requestUp'] and result['acceleratingDown']
    return result


def validate_pair(cb, cp, stage, sp, stream, case_config, local_number, current_state):
    C.guard()
    stride, dt, origin = case_config['stepsPerControl'], case_config['dt'], stream['timeOrigin']
    step_index = local_number*stride
    integer(cb.get('stepIndex'), step_index, step_index, 'controller-cadence-step')
    exact(cb.get('controlIndex'), local_number, 'controller-cadence-index')
    exact(cb.get('schema'), 'm31-coupled-controller-v1', 'controller-schema')
    exact(cb.get('arm'), 'coupled', 'controller-arm')
    relative = step_index*dt
    exact(cb.get('relativeTimeWord'), word(relative), 'controller-relative-time')
    exact(cb.get('originalTimeWord'), word(origin+relative), 'controller-original-time')
    integer(sp['sequence'], cp['sequence']+1, cp['sequence']+1, 'adjacent-record-sequences')
    exact(stage.get('schema'), 'm31-coupled-stage-v1', 'stage-schema')
    exact(stage.get('arm'), 'coupled', 'stage-arm')
    integer(stage.get('stageIndex'), 1, 1, 'only-k1')
    integer(stage.get('stepIndex'), step_index, step_index, 'stage-controller-step')
    exact(stage.get('stageId'), f'coupled-step{step_index}-k1', 'stage-id')
    exact(stage.get('status'), 'completed', 'unexpected-refused-k1')
    exact(stage.get('reason'), None, 'completed-k1-reason')
    exact(stage.get('relativeTimeWord'), cb['relativeTimeWord'], 'paired-relative-time')
    exact(stage.get('originalTimeWord'), cb['originalTimeWord'], 'paired-original-time')
    exact(stage.get('dtWord'), word(dt), 'paired-dt')
    integer(stage.get('nativeCalls'), 1, 1, 'paired-native-call-count')
    controller = pick(cb['records'], 'controller')
    derivative = pick(stage['records'], 'stage')
    native = stage['native']
    exact(native.get('schema'), 'm31-native-load-evidence-v1', 'native-schema')
    exact(native.get('status'), 'native-success', 'unexpected-native-k1-status')
    exact(native.get('method'), 'F', 'native-method')
    exact(native.get('caseId'), stage['stageId'], 'native-stage-binding')
    prepared = pick(native['prepared'], 'native-prepared')
    load = pick(native['loads'], 'native-load')
    native_raw = pick(native['raw'], 'native-raw')
    raw = pick(stage['rawBeforeProjection']['drones'], 'raw-stage')
    projected = pick(stage['nativeInput']['drones'], 'projected-stage')
    exact(controller['stateWords'], current_state, 'controller-current-endpoint-binding')
    exact(derivative['rawStateWords'], controller['stateWords'], 'controller-k1-raw-state')
    exact(raw['state'], controller['stateWords'], 'enclosing-raw-state')
    words(derivative['stateWords'], 17)
    words(derivative['derivativeWords'], 17)
    exact(projected['state'], derivative['stateWords'], 'enclosing-projected-state')
    exact(native_raw['state'], derivative['stateWords'], 'native-projected-input')
    exact(derivative['commandsWords'], controller['commandsWords'], 'controller-k1-commands')
    require(type(stage['commandsBeforeEvaluation']) is list and len(stage['commandsBeforeEvaluation']) == 64, 'enclosing-command-count')
    exact(stage['commandsBeforeEvaluation'][FOCUS], controller['commandsWords'], 'enclosing-held-commands')
    exact(derivative['nominalMotorWords'], derivative['stateWords'][13:17], 'motor-state-binding')
    exact(prepared['forces'], derivative['nominalMotorWords'], 'prepared-motor-binding')
    exact(prepared['center'], derivative['stateWords'][:3], 'prepared-position-binding')
    consumed = {'rotorWords': load['rotor'], 'collectiveWord': load['collective'],
                'worldForceWords': load['worldForce'], 'worldMomentWords': load['worldMoment']}
    exact(derivative['consumed'], consumed, 'same-id-consumed-native-load')
    metrics = derive(controller, derivative, prepared, load)
    clock = {key: stage[key] for key in ('stepIndex', 'stageIndex', 'relativeTimeWord', 'originalTimeWord', 'dtWord')}
    expected = {'phase': stream['phase'], 'caseId': stream['caseId'], 'id': FOCUS,
                'controllerProvenance': cp, 'stageProvenance': sp, 'clock': clock,
                'controller': controller, 'stage': derivative, 'prepared': prepared,
                'load': load, 'metrics': metrics}
    return expected


def make_summary(rows, endpoint):
    require(len(rows) > 0, 'empty-case-samples')
    counts = {key: 0 for key in CONDITIONS}
    first_matches = {key: None for key in CONDITIONS}
    ranges = {key: [rows[0]['metrics'][key], rows[0]['metrics'][key]] for key in FIELDS}
    for row in rows:
        values, flags = row['metrics'], predicates(row['metrics'])
        for key in FIELDS:
            if values[key] < ranges[key][0]:
                ranges[key][0] = values[key]
            if values[key] > ranges[key][1]:
                ranges[key][1] = values[key]
        for key in CONDITIONS:
            if flags[key]:
                counts[key] += 1
                if first_matches[key] is None:
                    first_matches[key] = {'time': decode(row['clock']['originalTimeWord']),
                                          'phase': row['phase'],
                                          'controllerSequence': row['controllerProvenance']['sequence']}
    return {'samples': len(rows), 'first': rows[0]['metrics'], 'last': rows[-1]['metrics'],
            'firstTime': decode(rows[0]['clock']['originalTimeWord']),
            'lastTime': decode(rows[-1]['clock']['originalTimeWord']), 'ranges': ranges,
            'counts': counts, 'firstMatches': first_matches, 'endpoint': endpoint}


def prior_publications(cfg):
    """Check existing publication metadata only; never rerun a prior audit."""
    fixed = {
        'original': ('admission', '637c25294f162bea39970d12df0206f25dead889',
                     20563, 'a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b', 100),
        'continuation': ('continuation', 'a0f595f34a4f9ef8cef516caa0cde60053e0eade',
                         33149, '90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81', 157)}
    frozen = local_json(B/'source-manifest.json')['files']
    frozen_by_path = {pin['path']: pin for pin in frozen}
    require(len(frozen_by_path) == len(frozen), 'unique-source-manifest-paths')
    indices, public_pins, evidence = {}, {}, []
    archive = None
    for phase, (tag, commit, size, digest, count) in fixed.items():
        folder = cfg[phase]
        manifest_path = folder+'/result-manifest.json'
        receipt_path = 'research/publication-receipts/m31-boids-'+tag+'-result-2026-10-20.json'
        require(manifest_path in frozen_by_path and receipt_path in frozen_by_path,
                'prior-publication-metadata-in-source-freeze')
        manifest_pin = {'path': manifest_path, 'bytes': size, 'sha256': digest}
        exact(frozen_by_path[manifest_path], manifest_pin, 'frozen-prior-manifest')
        receipt = parse(C.checked(R/receipt_path, frozen_by_path[receipt_path]))
        for key, value in {'commit': commit, 'manifestPath': manifest_path,
                           'manifestBytes': size, 'manifestSha256': digest,
                           'verifiedFilePins': count, 'remoteBytesEqualLocal': True,
                           'committedBytesEqualLocal': True}.items():
            exact(receipt.get(key), value, 'prior-public-receipt:'+key)
        exact(receipt.get('remoteUrl'),
              'https://raw.githubusercontent.com/denghanjie/drone-swarm-aerodynamics-public/'+commit+'/'+manifest_path,
              'prior-exact-commit-public-url')
        manifest = parse(C.checked(R/manifest_path, manifest_pin))
        exact(manifest.get('schema'), 'm31-boids-'+tag+'-result-v1', 'prior-manifest-schema')
        pins = {pin['path']: pin for pin in manifest['files']}
        require(len(pins) == len(manifest['files']) == count, 'prior-manifest-count-and-uniqueness')
        public_pins[phase] = pins
        small = {}
        names = ['results/index.json', 'audit/audit.json', 'audit/exit.json',
                 'results/exit.json', 'native-supervisor.json', 'audit-supervisor.json',
                 'ALLOCATION-CLOSURE.json']
        if phase == 'original':
            names.append('archive/index.json')
        for name in names:
            path = folder+'/'+name
            require(path in pins and path in frozen_by_path, 'prior-required-file-pin')
            exact(frozen_by_path[path], pins[path], 'prior-required-file-public-binding')
            small[name] = parse(C.checked(R/path, pins[path]))
        index, audit, closure = (small['results/index.json'], small['audit/audit.json'],
                                  small['ALLOCATION-CLOSURE.json'])
        exact(index.get('schema'), 'm31-boids-'+tag+'-index-v1', 'prior-index-schema')
        exact(audit.get('schema'), 'm31-boids-'+tag+'-audit-v1', 'prior-audit-schema')
        require(index.get('complete') is True and 'failure' not in index
                and audit.get('passed') is True, 'prior-index-and-audit-passed')
        exact(audit['sourceCommit'], index['sourceCommit'], 'prior-audit-index-source-binding')
        closure_schema = 'm31-boids-allocation-closure-v1' if phase == 'original' else 'm31-boids-continuation-closure-v1'
        exact(closure.get('schema'), closure_schema, 'prior-closure-schema')
        closed_phases = ('native', 'audit', 'display', 'archive') if phase == 'original' else ('storage', 'native', 'audit', 'ui')
        for name in closed_phases:
            exact(closure[name]['status'], 'closed-passed', 'prior-closed-phase:'+name)
            integer(closure[name]['attempts'], 1, 1, 'prior-phase-attempts')
        for name, limit in (('native', 360 if phase == 'original' else 1200),
                            ('audit', 180 if phase == 'original' else 1200)):
            supervisor = small[name+'-supervisor.json']
            require(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
                    and supervisor.get('allocationWallPassed') is True
                    and 0 <= supervisor['wallSeconds'] <= limit, 'prior-supervisor-passed')
            if phase == 'continuation':
                exact(supervisor.get('outputCapPassed'), True, 'prior-output-cap-passed')
            exit_record = small[('results' if name == 'native' else 'audit')+'/exit.json']
            require(exit_record.get('closed') is True and exit_record.get('exitCode') == 0,
                    'prior-process-closed-successfully')
        indices[phase] = index
        if phase == 'original':
            archive = small['archive/index.json']
            exact(archive.get('schema'), 'm31-boids-byte-archive-v1', 'prior-archive-schema')
        evidence.append({'phase': phase, 'commit': commit, 'manifestPin': manifest_pin,
                         'receiptPath': receipt_path, 'closedPhases': list(closed_phases)})
    return indices, archive, public_pins, frozen_by_path, evidence


def input_contract(cfg):
    exact(cfg.get('focusId'), FOCUS, 'focus-id')
    exact(cfg.get('expectedSamples'), 1924, 'prospective-sample-count')
    exact(cfg.get('mass'), .027, 'mass')
    exact(cfg.get('gravity'), 9.81, 'gravity')
    exact(cfg.get('bodyRadius'), .075, 'body-radius')
    exact(cfg.get('original'), 'research/m31-boids-admission-2026-10-20', 'original-checkpoint')
    exact(cfg.get('continuation'), 'research/m31-boids-continuation-2026-10-20', 'continuation-checkpoint')
    streams = cfg.get('streams')
    require(type(streams) is list and len(streams) == 8, 'eight-streams-required')
    indices, archive, public_pins, frozen_pins, evidence = prior_publications(cfg)
    parts_count = 0
    for position, stream in enumerate(streams):
        phase = 'original' if position < 4 else 'continuation'
        case_id = CASES[position % 4]
        exact(stream['phase'], phase, 'stream-phase-order')
        exact(stream['caseId'], case_id, 'stream-case-order')
        exact(stream['timeOrigin'], 0 if phase == 'original' else 1, 'stream-clock-origin')
        exact(stream['expectedSamples'], 100 if phase == 'original' else (362 if position % 4 < 2 else 400), 'stream-sample-plan')
        exact(stream['index'], cfg[phase]+'/results/index.json', 'stream-index-path')
        exact(stream['folder'], cfg[phase]+('/archive' if phase == 'original' else '/results'), 'stream-parts-folder')
        matches = [entry for entry in indices[phase]['cases'] if entry['caseId'] == case_id]
        require(len(matches) == 1, 'unique-prior-case')
        journal = matches[0]['journal']
        if phase == 'original':
            old = [entry for entry in archive['journals'] if entry['originalFile'] == 'results/'+journal['file']]
            require(len(old) == 1 and old[0]['reconstructionVerified'] is True, 'original-public-archive-binding')
            expected = {**journal, 'parts': old[0]['parts']}
            exact(old[0]['bytes'], journal['bytes'], 'archive-byte-binding')
            exact(old[0]['sha256'], journal['sha256'], 'archive-hash-binding')
            exact(stream['descriptor'], expected, 'original-stream-descriptor')
        else:
            exact(stream['descriptor'], journal, 'continuation-stream-descriptor')
        total = 0
        for part_index, part in enumerate(stream['descriptor']['parts']):
            exact(part['file'], journal['file']+f'.part{part_index:03d}', 'part-name-order')
            integer(part['offset'], total, total, 'part-offset')
            total += integer(part['bytes'], 1, 32*1024*1024, 'part-size')
            require(isinstance(part['sha256'], str) and SHA.fullmatch(part['sha256']), 'part-hash')
            path = stream['folder']+'/'+part['file']
            expected_pin = {'path': path, 'bytes': part['bytes'], 'sha256': part['sha256']}
            exact(public_pins[phase].get(path), expected_pin, 'part-exact-public-manifest-pin')
            exact(frozen_pins.get(path), expected_pin, 'part-exact-source-freeze-pin')
            parts_count += 1
        exact(total, journal['bytes'], 'compressed-total-byte-count')
    exact(parts_count, 75, 'public-part-count')
    return indices, evidence


def perform():
    pub = C.gate()
    cfg = local_json(B/'inputs.json')
    indices, prior_evidence = input_contract(cfg)
    supervisor = local_json(B/'extract-supervisor.json')
    require(supervisor.get('returncode') == 0 and 'timeout' not in supervisor
            and supervisor.get('allocationWallPassed') is True
            and supervisor.get('outputCapPassed') is True, 'extraction-supervised-closure')
    require(type(supervisor.get('wallSeconds')) in (int, float)
            and 0 <= supervisor['wallSeconds'] <= 900, 'extraction-wall-bound')
    out = B/'results'
    require({path.name for path in out.iterdir()} == {'launch.json', 'trace.jsonl', 'view-data.json', 'report.json'}, 'extraction-output-closure')
    total_size = sum(path.stat().st_size for path in out.iterdir())
    require(total_size <= MAX_EXTRACT_OUTPUT, 'extraction-output-cap')
    integer(supervisor.get('outputBytes'), total_size, total_size, 'extraction-output-byte-binding')
    launch = local_json(out/'launch.json')
    exact(launch.get('sourceCommit'), pub['commit'], 'extraction-source-commit')
    exact(launch.get('zeroModelCalls'), True, 'extraction-scope')
    report_pin, report_raw = identity(out/'report.json')
    report = parse(report_raw)
    exact(report.get('passed'), True, 'extraction-report-passed')
    exact(report.get('zeroModelCalls'), True, 'extraction-zero-model-calls')
    integer(report.get('samples'), 1924, 1924, 'extraction-sample-count')
    require(type(report.get('readEvents')) is list, 'extraction-read-event-list')
    trace_raw = verify_pin(report['tracePin'], 'results/trace.jsonl', 28*1024*1024)
    view_raw = verify_pin(report['viewPin'], 'results/view-data.json', MAX_EXTRACT_OUTPUT)
    trace_lines = trace_raw.splitlines(keepends=True)
    require(len(trace_lines) == 1924 and all(line.endswith(b'\n') for line in trace_lines), 'exact-trace-line-count')
    extracted_rows = iter(parse(line) for line in trace_lines)
    receipts, boundaries = [], []
    originals, grouped, endpoints = {}, {key: [] for key in CASES}, {}
    sample_count = 0
    for stream in cfg['streams']:
        C.guard()
        key, phase = stream['caseId'], stream['phase']
        index = indices[phase]
        entry = next(item for item in index['cases'] if item['caseId'] == key)
        case_config = next(item for item in index['config']['cases'] if item['caseId'] == key)
        expected_dt = .005 if key.endswith('-h005') else .0025
        exact(case_config['dt'], expected_dt, 'case-dt')
        exact(case_config['stepsPerControl'], 2 if expected_dt == .005 else 4, 'case-cadence')
        receipt, pending, initial, terminal, last_step = {}, None, None, None, None
        number = step_records = 0
        current_state = None
        for obj, provenance in C.records(stream, receipt):
            require(type(obj) is dict and set(obj) == {'sequence', 'kind', 'body'}, 'source-record-envelope')
            require(terminal is None, 'source-record-after-case-end')
            body, kind = obj['body'], obj['kind']
            require(type(body) is dict and kind in ('initial', 'controller', 'stage', 'step', 'safety', 'case-end'), 'source-record-kind')
            if pending is not None:
                require(kind == 'stage', 'controller-must-be-immediately-followed-by-k1')
                cb, cp = pending
                expected = validate_pair(cb, cp, body, provenance, stream, case_config, number, current_state)
                row = next(extracted_rows, None)
                require(row is not None, 'missing-extracted-pair')
                exact(row, expected, 'extracted-pair-binding')
                grouped[key].append({'phase': phase, 'clock': expected['clock'],
                                     'controllerProvenance': cp, 'metrics': expected['metrics']})
                number += 1
                sample_count += 1
                pending = None
            if kind == 'initial':
                require(initial is None and provenance['sequence'] == 0, 'source-initial-order')
                exact(body.get('caseId'), key, 'source-initial-case')
                initial = full_input(body['input'])
                current_state = initial['drones'][FOCUS]['state']
                if phase == 'continuation':
                    exact(initial, originals[key], 'all-64-by-17-boundary-words')
                    boundaries.append(key)
            elif kind == 'controller':
                require(pending is None and initial is not None, 'source-controller-order')
                pending = (body, provenance)
            elif kind == 'step':
                integer(body.get('stepIndex'), step_records, step_records, 'completed-endpoint-step-order')
                exact(body.get('status'), 'completed', 'source-completed-endpoint-status')
                current_state = pick(body['final'], 'completed-endpoint')['stateWords']
                last_step = body
                step_records += 1
            elif kind == 'case-end':
                terminal = body
                exact(terminal, {k: v for k, v in entry.items() if k != 'journal'}, 'source-index-terminal-binding')
                final = full_input(terminal['finalInput'])
                exact(final['drones'][FOCUS]['state'], current_state, 'final-endpoint-state-binding')
        require(initial is not None and terminal is not None and last_step is not None and pending is None, 'stream-selection-closure')
        integer(number, stream['expectedSamples'], stream['expectedSamples'], 'stream-selected-count')
        integer(step_records, terminal['completedSteps'], terminal['completedSteps'], 'source-completed-step-count')
        receipts.append(receipt)
        if phase == 'original':
            originals[key] = terminal['finalInput']
        else:
            origin, dt = stream['timeOrigin'], case_config['dt']
            relative = (step_records-1)*dt+dt
            exact(last_step['relativeTimeWord'], word(relative), 'final-saved-relative-time')
            exact(last_step['originalTimeWord'], word(origin+relative), 'final-saved-original-time')
            endpoints[key] = {'timeWord': last_step['originalTimeWord'],
                              'stateWords': terminal['finalInput']['drones'][FOCUS]['state'],
                              'status': terminal['status'], 'reason': terminal['reason']}
    require(next(extracted_rows, None) is None and sample_count == 1924, 'extra-or-missing-trace-sample')
    exact(boundaries, list(CASES), 'four-continuation-boundaries')
    summaries = {key: make_summary(grouped[key], endpoints[key]) for key in CASES}
    exact(report.get('boundaries'), boundaries, 'extraction-boundary-summary')
    exact(report.get('journalReceipts'), receipts, 'independent-stream-receipts')
    exact(report.get('summaries'), summaries, 'independent-case-summary')
    expected_view = {'physicalValidity': False, 'focusId': FOCUS, 'cases': []}
    for key in CASES:
        samples = [{'time': decode(row['clock']['originalTimeWord']), 'phase': row['phase'],
                    'controllerSequence': row['controllerProvenance']['sequence'], 'values': row['metrics']}
                   for row in grouped[key]]
        expected_view['cases'].append({'caseId': key, 'summary': summaries[key], 'samples': samples})
    exact(parse(view_raw), expected_view, 'trace-view-semantic-binding')
    exact(C.gate(), pub, 'source-publication-unchanged')
    C.checked(out/'report.json', report_pin)
    C.checked(out/'trace.jsonl', report['tracePin'])
    C.checked(out/'view-data.json', report['viewPin'])
    C.guard()
    return {'passed': True, 'closed': True, 'sourceCommit': pub['commit'],
            'zeroModelCalls': True, 'samples': sample_count, 'boundaries': boundaries,
            'boundaryWordsPerCase': 64*17, 'tracePin': report['tracePin'], 'viewPin': report['viewPin'],
            'reportPin': report_pin, 'journalReceipts': receipts, 'readEvents': C.EVENTS,
            'priorPublications': prior_evidence,
            'independence': 'independent row selection, bindings, scalar formulas, summaries and view semantics; shared common.py verified-byte/gzip/JSON reader',
            'scope': 'all recorded controller updates paired only to immediately following k1; no intervening-stage analysis or causal attribution',
            'wallSeconds': time.monotonic()-C.START}


def main():
    require((B/'audit-supervisor-launch.lock').is_file(), 'audit-supervisor-allocation-required')
    target = B/'audit'
    target.mkdir()  # Exclusive: no whole-phase retry and no old-output overwrite.
    try:
        result = perform()
        encoded = (json.dumps(result, separators=(',', ':'), allow_nan=False)+'\n').encode()
        require(len(encoded)+8192 <= MAX_OUTPUT, 'audit-output-budget')
        C.write(target/'report.json', result)
        C.guard()
        require(sum(path.stat().st_size for path in target.iterdir()) <= MAX_OUTPUT, 'audit-output-cap')
        print(json.dumps({'passed': True, 'samples': result['samples'], 'wallSeconds': time.monotonic()-C.START}))
        return 0
    except Exception as error:
        failure = {'passed': False, 'closed': True, 'zeroModelCalls': True,
                   'error': str(error).replace(str(R), '[repository]')[:2000],
                   'type': type(error).__name__, 'readEvents': C.EVENTS,
                   'wallSeconds': time.monotonic()-C.START}
        C.write(target/'failure.json', failure)
        if not (target/'report.json').exists():
            C.write(target/'report.json', failure)
        print(json.dumps({'passed': False, 'type': type(error).__name__}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
