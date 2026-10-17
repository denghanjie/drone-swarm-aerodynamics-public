"""One three-scene, profiled capacity pilot of frozen prepared exact references."""
from pathlib import Path
from fractions import Fraction
import cProfile
import datetime as dt
import hashlib
import importlib.util
import json
import pstats
import resource
import signal
import sys
import time
import traceback

PACKAGE = 'research/m31-prepared-capacity-2026-10-17'
PREPARED = 'research/m31-prepared-reference-2026-10-17'
TREE = 'research/m31-tree-first-reference-2026-10-17'
FRESH = 'research/m31-native-fresh-transfer-2026-10-17'
FILTER = 'research/m31-filter-cost-2026-10-17'
CASES = ('fresh-a-t5', 'dense-180-filter-cost', 'sparse-180-filter-cost')
EXPECTED_SUFFIX = (7408, 34707, 3340)
EXPECTED_POSITIVE = (228, 3056, 0)
PREVIOUS_RECEIPT = 'research/publication-receipts/m31-prepared-result-2026-10-17.json'
MAX_BYTES, MAX_FILE = 256 * 1024 * 1024, 32 * 1024 * 1024
MODULE_PINS = {
    FRESH + '/source/pair-reference.py': '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0',
    FRESH + '/source/semantic-reference.py': 'ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c',
    TREE + '/source/tree-reference.py': 'd08efc5e80910066d061a664aa7902c7ae7bab27dc710f5c00c9b2bf1671df65',
    PREPARED + '/source/prepared-reference.py': '19efcb01f4c6d45b517b2388bcdaf045daf382bc11e7442dd8b9627e1807a921',
}


def need(value, code):
    if not value:
        raise RuntimeError(code)


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def verify(root, manifest):
    for pin in manifest['files']:
        path = Path(pin['path'])
        need(not path.is_absolute() and '..' not in path.parts, 'manifest-path')
        raw = (root / path).read_bytes()
        need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'source-preservation')
    return len(manifest['files'])


def wire(target,semantic):
    out={key:target[key] for key in ('id','input','prepared','planned','globalInvalid','globalGuard','order','status','branch','witness','referenceClass','tree')}
    out['pairs']=[]
    for p in target['pairs']:
        row={k:p[k] for k in ('i','j','r','ii','jj','oracle')}
        if 'coefficient' in p:
            row['coefficient']=semantic.interval_wire(p['coefficient'])
        out['pairs'].append(row)
    out['loads']=[]
    if target['status']=='admitted':
        for row in target['input']['drones']:
            i=row['id']
            out['loads'].append({'id':i,'roots':[semantic.interval_wire(target['roots'][(i,r)]) for r in range(4)],
                                'loads':{key:semantic.interval_wire(v) if key=='collective' else [semantic.interval_wire(x) for x in v]
                                         for key,v in target['loads'][i].items()}})
    if 'coverage' in target:
        out['coverage']=target['coverage']
    return out


class InputHelper:
    def __init__(self, original, raw_words):
        self.original, self.raw_words = original, raw_words

    def literal(self, value):
        return self.original.parse_bits(value) if self.raw_words else self.original.literal(value)

    def __getattr__(self, name):
        return getattr(self.original, name)


def by_id(rows):
    result = {row['id']: row for row in rows}
    need(len(result) == len(rows), 'unique-stable-ids')
    return result


def profile_wire(profiler, root, completed):
    """Preserve every pstats function and caller edge without private paths."""
    stats = pstats.Stats(profiler)

    def location(key):
        filename, line, name = key
        path = Path(filename)
        if path.is_absolute():
            try:
                filename = path.relative_to(root).as_posix()
            except ValueError:
                filename = path.name
        return {'file': filename, 'line': line, 'function': name}

    keys = sorted(stats.stats, key=lambda key: (location(key)['file'], key[1], key[2], key[0]))
    identifiers = {key: index for index, key in enumerate(keys)}
    rows = []
    for key in keys:
        primitive, total, own, cumulative, callers = stats.stats[key]
        edges = []
        for caller, values in sorted(callers.items(), key=lambda item: identifiers[item[0]]):
            edges.append({'functionId': identifiers[caller],
                          'pstatsValues': list(values) if isinstance(values, tuple) else values})
        rows.append({'functionId': identifiers[key], **location(key), 'primitiveCalls': primitive,
                     'totalCalls': total, 'ownSeconds': own, 'cumulativeSeconds': cumulative,
                     'callers': edges})
    return {'schema': 'm31-complete-cprofile-v1', 'completeCallReturned': completed,
            'scope': 'Exactly one regenerate_scene call; default cProfile clock, profiler overhead included.',
            'cumulativeAccounting': 'Cumulative times overlap and must not be added across functions.',
            'callerTupleFields': ['totalCalls', 'primitiveCalls', 'ownSeconds', 'cumulativeSeconds'],
            'primitiveCalls': stats.prim_calls, 'totalCalls': stats.total_calls,
            'totalOwnSeconds': stats.total_tt, 'functions': rows}


def producer_positive_map(method, raw_rows):
    ids = [row['id'] for row in raw_rows]
    result = {}
    for query in method['assembly']['queries']:
        need(type(query['i']) is int and 0 <= query['i'] < len(ids)
             and type(query['r']) is int and 0 <= query['r'] < 4, 'producer-query-indices')
        for terminal in query['terminals']:
            for entry in terminal.get('entries', []):
                need(entry['result']['status'] == 'positive', 'producer-positive-only-admitted')
                need(type(entry['j']) is int and 0 <= entry['j'] < len(ids), 'producer-source-index')
                key = (ids[query['i']], query['r'], ids[entry['j']])
                need(key not in result, 'producer-positive-duplicate')
                result[key] = entry['result']['coefficient']
    return result


def compare_180(record, saved, reference):
    need(record['id'] == saved['id'] == reference['sceneId'], 'scene-identity')
    need(saved['rawInputSha256'] == reference['rawInputSha256'], 'saved-reference-raw-input-binding')
    need(record['input'] == saved['input'], 'exact-raw-word-order')
    need(by_id(record['input']['drones']) == by_id(saved['input']['drones']), 'exact-stable-id-raw-words')
    methods = {method['name']: method for method in saved['methods']}
    need(len(methods) == len(saved['methods']) == 2 and set(methods) == {'hierarchy', 'filtered'}, 'saved-method-set')
    for method in methods.values():
        need(by_id(record['prepared']) == by_id(method['prepared']), 'exact-stable-id-prepared-words')
        need(method['result'] == {'branch': 'loads', 'status': 'certified',
                                 'toleranceAchieved': True, 'witness': None}, 'saved-method-admissibility')
    need(by_id(record['loads']) == by_id(reference['independentReference']), 'exact-independent-roots-signed-loads')
    need(record['planned'] == reference['plannedPairsPerMethod'] == 128880, 'full-180-logical-pairs')
    need(all(reference[key] == value for key, value in
             (('referenceCoefficientBits', 192), ('referenceSourceBits', 192), ('referenceRootBisections', 128))), 'saved-reference-precision')
    old_maps = [producer_positive_map(methods[name], saved['input']['drones'])
                for name in ('hierarchy', 'filtered')]
    need(old_maps[0] == old_maps[1], 'exact-producer96-maps-between-methods')
    positives = {(pair['i'], pair['r'], pair['j']): pair['coefficient']
                 for pair in record['pairs'] if pair['oracle']['status'] == 'positive'}
    need(len(positives) == sum(pair['oracle']['status'] == 'positive' for pair in record['pairs']), 'new-positive-unique')
    need(set(positives) == set(old_maps[0]) == set(old_maps[1]), 'exact-positive-support')
    for key, bounds in positives.items():
        lower = Fraction(int(bounds['l']['n']), int(bounds['l']['d']))
        upper = Fraction(int(bounds['u']['n']), int(bounds['u']['d']))
        old = old_maps[0][key]
        need(Fraction(int(old['l']), 1 << 96) <= lower <= upper
             <= Fraction(int(old['u']), 1 << 96), 'exact-rational-producer96-containment')
    return {'rawWordsExactlyEqual': True, 'preparedWordsExactlyEqualBothMethods': True,
            'independentRootAndSignedLoadBoxesExactlyEqual': True,
            'positiveSupportExactlyEqualBothMethods': True, 'positiveTerms': len(positives),
            'producer96BoundsExactlyEqualBetweenMethods': True,
            'new192WithinSaved96BoundsExactRational': True,
            'savedSolveOrderComparisonAvailable': False,
            'savedSolveOrderUnavailableReason': 'Prior producer schema stores candidate rows, not the solve traversal order.',
            'independent192PairEqualityAvailable': False,
            'independent192PairEqualityUnavailableReason': 'Prior independentReference stores roots and signed loads, not pair coefficients.'}


def main(root, expected, commit):
    package = root / PACKAGE
    manifest_raw = (package / 'source-manifest.json').read_bytes()
    need(digest(manifest_raw) == expected, 'manifest-identity')
    manifest = json.loads(manifest_raw)
    runtime = manifest['runtime']['python']
    executable = Path(sys.executable).resolve().read_bytes()
    need(sys.platform == 'darwin' and sys.flags.isolated == 1 and sys.dont_write_bytecode
         and sys.version == runtime['version'] and len(executable) == runtime['bytes']
         and digest(executable) == runtime['sha256'], 'pinned-macos-python-runtime')
    del executable
    receipt = load(package / 'source-publication.json')
    need(receipt['commit'] == commit and receipt['manifestSha256'] == expected
         and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True
         and receipt['verifiedFilePins'] == len(manifest['files']), 'public-source-gate')
    cutoff = dt.datetime(2026, 10, 17, 3, tzinfo=dt.timezone.utc)
    need((cutoff - dt.datetime.now(dt.timezone.utc)).total_seconds() >= 600, 'full-budget-before-cutoff')
    publication_time = dt.datetime.fromisoformat(receipt['verifiedUtc'])
    need(publication_time.tzinfo is not None
         and publication_time <= dt.datetime.now(dt.timezone.utc)
         and (cutoff - publication_time).total_seconds() >= 600, 'publication-reserves-full-budget')
    before = verify(root, manifest)
    pins = {pin['path']: pin for pin in manifest['files']}
    need(len(pins) == len(manifest['files']), 'unique-source-pins')
    required = [PREPARED + '/source-manifest.json', PREPARED + '/result-manifest.json', PREVIOUS_RECEIPT,
                PREPARED + '/source/run.py',
                PREPARED + '/source-publication.json', PREPARED + '/results/index.json',
                PREPARED + '/review/saved-audit-result.json', PREPARED + '/review/audit-source-manifest.json',
                PREPARED + '/review/saved_audit.py', FRESH + '/source/spec.json',
                FRESH + '/results/inputs/fresh-a-t5.json', FILTER + '/source/spec.json',
                FILTER + '/source/pair-reference.py', FILTER + '/source/semantic-reference.py',
                FILTER + '/results/independent-check.json', FILTER + '/source-manifest.json',
                FILTER + '/result-manifest.json']
    required += list(MODULE_PINS)
    for scene_id in CASES[1:]:
        required += [FILTER + '/results/scenes/' + scene_id + '.json',
                     FILTER + '/results/reference-scenes/' + scene_id + '.json']
    need(all(path in pins for path in required), 'prerequisite-source-membership')
    for path, sha in MODULE_PINS.items():
        need(pins[path]['sha256'] == sha, 'unchanged-scientific-module')
    for filename in ('pair-reference.py', 'semantic-reference.py'):
        need(pins[FILTER + '/source/' + filename]['sha256'] == pins[FRESH + '/source/' + filename]['sha256'], 'identical-old-new-oracle-source')
    previous_manifest = load(root / PREPARED / 'source-manifest.json')
    need(all(pins.get(pin['path']) == pin for pin in previous_manifest['files']), 'all-prior-source-pins-retained')
    previous_result_manifest = load(root / PREPARED / 'result-manifest.json')
    previous_receipt = load(root / PREVIOUS_RECEIPT)
    need(previous_receipt['commit'] == '1ce0f3bff31ae5c296fd7ab711bcc5949bf297bd'
         and previous_receipt['manifestSha256'] == pins[PREPARED + '/result-manifest.json']['sha256']
         == '3bb348f971327ec84b0e942968a3872397f30e70edf8c24171fdb0cc86071418'
         and previous_receipt['remoteBytesEqualLocal'] is True
         and previous_receipt['committedBytesEqualLocal'] is True
         and previous_receipt['verifiedFilePins'] == len(previous_result_manifest['files']),
         'public-predecessor-result-prerequisite')
    previous = load(root / PREPARED / 'results/index.json')
    audit = load(root / PREPARED / 'review/saved-audit-result.json')
    need(previous['complete'] is True and previous['qualified'] is True and len(previous['cases']) == 24,
         'qualified-prior24-prerequisite')
    need(audit['status'] == 'passed' and audit['errors'] == []
         and audit['allReviewedBytesUnchangedAtClosure'] is True
         and audit['resultIndexSha256'] == pins[PREPARED + '/results/index.json']['sha256'], 'qualified-saved-audit-prerequisite')
    for case in previous['cases']:
        need(pins.get(case['result']['path']) == case['result'], 'all-prior24-results-pinned')
    previous_cases = by_id(previous['cases'])
    need(CASES[0] in previous_cases, 'fresh-control-baseline')
    old_check = load(root / FILTER / 'results/independent-check.json')
    need(old_check['passed'] is True and old_check['scientificQualification'] is True
         and old_check['fullQualification'] is True and old_check['errorCount'] == 0, 'qualified-filter-baseline')
    old_scenes = by_id(old_check['scenes'])
    for scene_id in CASES[1:]:
        evidence = old_scenes[scene_id]['referenceEvidence']
        expected_pin = {**evidence, 'path': FILTER + '/results/' + evidence['path']}
        need(pins.get(expected_pin['path']) == expected_pin and old_scenes[scene_id]['verified'] is True,
             'independent-reference-pin-membership')
    spec = load(root / FRESH / 'source/spec.json')
    old_spec = load(root / FILTER / 'source/spec.json')
    need({k: v for k, v in spec.items() if k != 'scenes'} ==
         {k: v for k, v in old_spec.items() if k != 'scenes'}, 'unchanged-complete-reference-settings')
    need((spec['maxDrones'], spec['leafCapacity'], spec['referenceCoefficientBits'],
          spec['referenceSourceBits'], spec['referenceRootBisections'], spec['fractionBits']) ==
         (180, 8, 192, 192, 128, 96), 'fixed-cap-precision-recipe')
    need((cutoff - dt.datetime.now(dt.timezone.utc)).total_seconds() >= 600, 'full-budget-after-pin-verification')
    need(not (package / 'STARTED.json').exists() and not (package / 'results').exists(), 'single-use-allocation')
    started = time.monotonic()
    results = package / 'results'
    results.mkdir()
    protected, events = [], None
    budget = {'oracleCalls': 0, 'limit': 60000}
    closure_started, closure_deadline = None, None

    def bytes_now():
        return sum(path.stat().st_size for path in results.rglob('*') if path.is_file()) + (
            (package / 'STARTED.json').stat().st_size if (package / 'STARTED.json').exists() else 0)

    def save(path, value):
        raw = (json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n').encode()
        need(len(raw) <= MAX_FILE and bytes_now() + len(raw) <= MAX_BYTES, 'artifact-byte-budget')
        with path.open('xb') as stream:
            stream.write(raw)
        pin = {'path': path.relative_to(root).as_posix(), 'bytes': len(raw), 'sha256': digest(raw)}
        protected.append(pin)
        return pin

    def poll():
        need(time.monotonic() - started < 540, 'scientific-wall-budget')

    def alarm(signum, frame):
        raise TimeoutError('allocation-wall-budget')

    def begin_closure():
        nonlocal closure_started, closure_deadline
        now = time.monotonic()
        if closure_deadline is None:
            closure_started = now
            closure_deadline = min(started + 600, now + 60)
        # Reuse one absolute deadline, including exception-profile preservation.
        # Repeat after expiry so a caught timeout cannot silently disarm closure.
        signal.setitimer(signal.ITIMER_REAL, max(0.001, closure_deadline - now), 0.25)

    def rss():
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    index = {'schema': 'm31-prepared-capacity-result-v1', 'sourceCommit': commit,
             'sourceManifestSha256': expected, 'startedUtc': utc(), 'status': 'running',
             'complete': False, 'qualified': False, 'accuracyQualified': False,
             'capacityHurdlePassed': False, 'outcome': 'incomplete', 'cases': [],
             'expectedCaseOrder': list(CASES), 'expectedCases': 3, 'regenerateSceneCalls': 0,
             'expectedScalarCalls': 45455, 'expectedLogicalPairs': 273888,
             'sourcePinsBefore': before, 'retainedQualifiedCases': 24,
             'priorIndex': pins[PREPARED + '/results/index.json'],
             'priorSavedAudit': pins[PREPARED + '/review/saved-audit-result.json'],
             'controlsRerun': False, 'newFullOracleRuns': 0, 'newInputs': 0,
             'newBrowserCalls': 0, 'physicalValidation': False, 'performanceClaim': False,
             'capacityHurdle': {'eachProfiledRegenerateSecondsAtMost': 60, 'lifetimePeakRssBytesAtMost': 1073741824,
                                'scope': 'Observed practical pilot hurdle; not an OS memory cap or production speed claim.'},
             'wallMeasurementScope': 'Allocation start through closure verification before final index serialization and stdout; not completed-process wall time.',
             'rssScope': 'macOS getrusage(RUSAGE_SELF).ru_maxrss in bytes, sampled through closure before final index serialization: process-lifetime peak, not a stage allocation or delta.'}
    save(package / 'STARTED.json', {'utc': utc(), 'sourceCommit': commit,
                                   'sourceManifestSha256': expected, 'sourcePinsVerified': before})
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, 540 - (time.monotonic() - started)))
    try:
        phase_start = time.monotonic()
        pair = module(root / FRESH / 'source/pair-reference.py', '_capacity_pair')
        semantic = module(root / FRESH / 'source/semantic-reference.py', '_capacity_semantic')
        tree = module(root / TREE / 'source/tree-reference.py', '_capacity_tree')
        candidate = module(root / PREPARED / 'source/prepared-reference.py', '_capacity_prepared')
        bits, _ = pair.constants_from_graph(spec)
        index['moduleAndConstantSetupWallSeconds'] = time.monotonic() - phase_start
        events = (results / 'events.jsonl').open('x')

        def event(value):
            raw = json.dumps(value, separators=(',', ':')) + '\n'
            need(events.tell() + len(raw.encode()) <= MAX_FILE and bytes_now() + len(raw.encode()) <= MAX_BYTES,
                 'journal-byte-budget')
            events.write(raw)
            events.flush()

        for ordinal, scene_id in enumerate(CASES):
            poll()
            entry = {'id': scene_id, 'ordinal': ordinal, 'complete': False, 'accuracyQualified': False,
                     'phaseWallSeconds': {}, 'rssBeforeCaseLifetimePeakBytes': rss()}
            index['cases'].append(entry)
            index['activeCase'] = scene_id
            phase_start = time.monotonic()
            if ordinal == 0:
                raw = load(root / FRESH / 'results/inputs/fresh-a-t5.json')
                scene = {'id': scene_id, 'family': 'moving-admission', 'expectedClass': 'admitted', 'drones': raw['drones']}
                baseline = load(root / previous_cases[scene_id]['result']['path'])
                entry.update(n=64, encoding='bits', baseline=previous_cases[scene_id]['result'])
            else:
                source = next(row for row in old_spec['scenes'] if row['id'] == scene_id)
                scene = {key: source[key] for key in ('id', 'family', 'expectedClass', 'drones')}
                saved_path = FILTER + '/results/scenes/' + scene_id + '.json'
                reference_path = FILTER + '/results/reference-scenes/' + scene_id + '.json'
                saved, reference = load(root / saved_path), load(root / reference_path)
                entry.update(n=180, encoding='decimal', baselineScene=pins[saved_path], baselineReference=pins[reference_path])
            need(len(scene['drones']) == entry['n'], 'fixed-case-size')
            entry['phaseWallSeconds']['inputAndBaselineLoad'] = time.monotonic() - phase_start
            event({'event': 'start', 'id': scene_id, 'ordinal': ordinal, 'callsBefore': budget['oracleCalls']})
            calls_before = budget['oracleCalls']
            profiler = cProfile.Profile()
            input_helper = InputHelper(pair, ordinal == 0)
            call_returned = False
            index['regenerateSceneCalls'] += 1
            phase_start = time.monotonic()
            profiler.enable()
            try:
                target, counters, controls = candidate.regenerate_scene(
                    scene, spec, bits, input_helper, semantic, tree,
                    guard=poll, budget=budget, run_controls=False)
                call_returned = True
            finally:
                profiler.disable()
                entry['phaseWallSeconds']['profiledRegenerate'] = time.monotonic() - phase_start
                entry['rssAfterRegenerateLifetimePeakBytes'] = rss()
                if not call_returned:
                    begin_closure()
                phase_start = time.monotonic()
                entry['profile'] = save(results / (scene_id + '.profile.json'), profile_wire(profiler, root, call_returned))
                entry['phaseWallSeconds']['profileSerializationAndWrite'] = time.monotonic() - phase_start
            phase_start = time.monotonic()
            record = wire(target, semantic)
            entry['result'] = save(results / (scene_id + '.json'), record)
            entry['reuseCounters'] = counters
            entry['phaseWallSeconds']['referenceWireSerializationAndWrite'] = time.monotonic() - phase_start
            # Both the complete reference wire and profile are preserved before outcome assertions.
            phase_start = time.monotonic()
            need(controls == [], 'no-controls-rerun')
            need(record['referenceClass'] == 'admitted' and record['status'] == 'admitted', 'admitted-case')
            need(counters['oracleCalls'] == len(record['pairs']) == budget['oracleCalls'] - calls_before, 'suffix-call-accounting')
            need(counters['oracleCalls'] == EXPECTED_SUFFIX[ordinal]
                 and sum(pair['oracle']['status'] == 'positive' for pair in record['pairs']) == EXPECTED_POSITIVE[ordinal],
                 'fixed-suffix-and-positive-counts')
            need(counters['prepareOneCalls'] == counters['preparationValidCalls'] == entry['n'], 'once-per-scene-preparation')
            need(counters['operandLookups'] == 2 * counters['oracleCalls'] and counters['pairPreparations'] == 0,
                 'prepared-reuse-accounting')
            need(record['coverage']['complete'] is True and record['coverage']['coveredPairs'] == record['planned'], 'complete-coverage')
            if ordinal == 0:
                need(record == baseline, 'fresh-exact-complete-saved-wire')
                entry['comparison'] = {'completeSavedWireExactlyEqual': True, 'independent192PairEqualityAvailable': True}
            else:
                entry['comparison'] = compare_180(record, saved, reference)
            entry['phaseWallSeconds']['exactSavedComparisonAndAccounting'] = time.monotonic() - phase_start
            entry.update(complete=True, accuracyQualified=True, reuseCounters=counters,
                         coverageWork=record['coverage']['work'], rssAfterCaseLifetimePeakBytes=rss())
            entry['profiledCallHurdlePassed'] = entry['phaseWallSeconds']['profiledRegenerate'] <= 60
            event({'event': 'complete', 'ordinal': ordinal, 'id': scene_id,
                   'result': entry['result'], 'profile': entry['profile'], 'callsAfter': budget['oracleCalls']})
            del target, record, profiler
            if ordinal == 0:
                del baseline, raw
            else:
                del saved, reference
        need(index['regenerateSceneCalls'] == 3 and [entry['id'] for entry in index['cases']] == list(CASES), 'exact-three-call-allocation')
        need(budget['oracleCalls'] == 45455 and sum(4 * case['n'] * (case['n'] - 1)
             for case in index['cases']) == 273888, 'fixed-total-suffix-and-logical-counts')
        index.update(status='completed', complete=True, qualified=True, accuracyQualified=True)
        index.pop('activeCase', None)
    except BaseException as error:
        index.update(status='failed', complete=False, qualified=False, accuracyQualified=False,
                     errorClass=type(error).__name__)
        message = str(error)
        index['reason'] = message if len(message) <= 160 and message.replace('-', '').replace(':', '').isalnum() else 'execution-exception'
        index['traceLocations'] = [{'file': Path(frame.filename).name, 'line': frame.lineno, 'function': frame.name}
                                   for frame in traceback.extract_tb(error.__traceback__)]
    finally:
        begin_closure()
        closure_start = time.monotonic()
        try:
            if events is not None:
                events.close()
                raw = (results / 'events.jsonl').read_bytes()
                need(len(raw) <= MAX_FILE and bytes_now() <= MAX_BYTES, 'journal-byte-budget')
                pin = {'path': PACKAGE + '/results/events.jsonl', 'bytes': len(raw), 'sha256': digest(raw)}
                protected.append(pin)
                index['eventJournal'] = pin
            index['sourcePinsAfter'] = verify(root, manifest)
            for pin in protected:
                raw = (root / pin['path']).read_bytes()
                need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'output-preservation')
            index['outputsPreserved'] = True
        except BaseException:
            index.update(status='failed', complete=False, qualified=False, accuracyQualified=False, outputsPreserved=False)
        index['closureVerificationWallSeconds'] = time.monotonic() - closure_start
        index['closureWallSecondsBeforeIndexWrite'] = time.monotonic() - closure_started
        index['scalarOracleCalls'] = budget['oracleCalls']
        index['lifetimePeakRssBytes'] = rss()
        index['capacityHurdlePassed'] = (index['complete'] and all(case.get('profiledCallHurdlePassed') is True
                                         for case in index['cases']) and index['lifetimePeakRssBytes'] <= 1073741824)
        index['wallSeconds'] = time.monotonic() - started
        index['finishedUtc'] = utc()
        index['resultBytesBeforeIndex'] = bytes_now()
        if time.monotonic() >= closure_deadline or index['wallSeconds'] >= 600 or dt.datetime.now(dt.timezone.utc) >= cutoff:
            index.update(status='failed', complete=False, qualified=False, accuracyQualified=False,
                         capacityHurdlePassed=False, deadlineExceeded=True)
        index['outcome'] = ('accuracy-unqualified-or-incomplete' if not index['accuracyQualified'] else
                            'accuracy-qualified-capacity-hurdle-passed' if index['capacityHurdlePassed'] else
                            'accuracy-qualified-capacity-hurdle-failed')
        save(results / 'index.json', index)
        signal.setitimer(signal.ITIMER_REAL, 0)
    print(json.dumps({key: index[key] for key in ('status', 'outcome', 'accuracyQualified', 'capacityHurdlePassed',
                                                 'regenerateSceneCalls', 'scalarOracleCalls', 'wallSeconds')}))
    return 0 if index['complete'] and index['accuracyQualified'] else 1


if __name__ == '__main__':
    need(len(sys.argv) == 4, 'usage-root-manifest-commit')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]))
