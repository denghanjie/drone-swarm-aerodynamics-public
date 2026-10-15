"""Bounded saved-public-evidence review. Never launches/imports the diagnostic."""
import time
START = time.monotonic()
import os
import signal


def hard_stop(signum, frame):
    os._exit(124)


signal.signal(signal.SIGALRM, hard_stop)
signal.setitimer(signal.ITIMER_REAL, max(.001, START + 30 - time.monotonic()))

import datetime
import hashlib
import json
import math
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from byte_evidence import byte_array, compare_bytes

CAP = 8388608
WORK_END = START + 25
FINAL_END = START + 29
CUTOFF = datetime.datetime.fromisoformat('2026-10-15T23:00:00+00:00')
BASE = REPO = None
CACHE = {}
DOC = {}
GROUPS = []
ERRORS = []
BYTE_FINDING = None
LOCK = b'One saved control-channel review reserved. Permanent; no retry.\n'
OUTPUT = None


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def finite(value, lower=0, upper=60):
    return type(value) in (int, float) and math.isfinite(value) and lower <= value < upper


def integer(value, lower=0, upper=CAP):
    return type(value) is int and lower <= value <= upper


def contained_file(root, relative, cap=131072):
    require(time.monotonic() < WORK_END, 'Review work deadline')
    require(type(relative) is str, 'Text evidence path required')
    rel = Path(relative)
    require(not rel.is_absolute() and '..' not in rel.parts and str(rel) == relative, 'Contained normalized evidence path')
    target = root / rel
    require(target.resolve() == target, 'No evidence symlinks')
    info = target.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_size <= cap, 'Bounded regular evidence file')
    data = target.read_bytes()
    require(len(data) == info.st_size and len(data) <= cap, 'Stable bounded evidence length')
    return data


def raw(relative, cap=131072):
    if relative not in CACHE:
        CACHE[relative] = contained_file(BASE, relative, cap)
    require(len(CACHE[relative]) <= cap, 'Evidence cache read cap')
    return CACHE[relative]


def no_constant(value):
    raise ValueError('Non-finite JSON token')


def json_integer(value):
    require(value != '-0', 'Negative-zero JSON integer')
    return int(value)


def no_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def document(relative, cap=131072):
    if relative not in DOC:
        DOC[relative] = json.loads(raw(relative, cap), parse_int=json_integer, parse_constant=no_constant, object_pairs_hook=no_duplicate_pairs)
    return DOC[relative]


def group(name, action):
    try:
        action()
        GROUPS.append({'group': name, 'pass': True})
    except Exception as error:
        # Controlled errors only; do not publish private file paths or tracebacks.
        reason = str(error) if type(error) is ValueError else 'Required evidence could not be read or checked'
        ERRORS.append({'group': name, 'type': type(error).__name__, 'reason': reason[:300]})
        GROUPS.append({'group': name, 'pass': False})


def same_values(left, right, names):
    require(all(name in left and name in right and type(left[name]) is type(right[name]) and left[name] == right[name] for name in names),
            'Explicit shared-field projection mismatch')


def true_fields(record, names):
    require(all(record.get(name) is True for name in names), 'Required completion flags')


def false_fields(record, names):
    require(all(record.get(name) is False for name in names), 'Premature qualification or forbidden lifecycle flag')


def source_identity():
    freeze = document('freeze.json', 1048576)
    expected_freeze = digest(raw('freeze.json', 1048576))
    receipt = document('publication/capture-execution.json')
    commit = receipt['sourceCommit']
    require(type(commit) is str and len(commit) == 40 and all(c in '0123456789abcdef' for c in commit), 'Source commit shape')
    require(receipt['sourceFreezeSHA256'] == expected_freeze, 'External receipt source freeze')
    pins = freeze['files']
    require(type(pins) is list and 1 <= len(pins) <= 256, 'Bounded source pins')
    seen = set()
    total = 0
    for pin in pins:
        path = pin['path']
        require(path not in seen, 'Unique source pin')
        seen.add(path)
        data = contained_file(REPO, path, 16777216)
        total += len(data)
        require(total <= 33554432, 'Source verification total read cap')
        require(type(pin['bytes']) is int and pin['bytes'] == len(data) and pin['sha256'] == digest(data), 'Exact frozen source bytes')
    needed = [BASE / ('source/' + n) for n in ['capture-transport.py', 'observe-transport.py', 'run-once.py', 'process-registry.cjs', 'diagnostic.cjs', 'validation.cjs', 'browser.js', 'browser.html']]
    needed += [BASE / n for n in ['PROTOCOL.md', 'config.json', 'payload.bin', 'payload.json', 'runtime-provenance.json']]
    needed += [Path(__file__).resolve(), Path(__file__).with_name('byte_evidence.py').resolve()]
    require(all(str(p.relative_to(REPO)) in seen for p in needed), 'Required diagnostic and reviewer source pins')
    cfg = document('config.json')
    require(cfg['limits'] == {'wallSeconds': 60, 'workerSeconds': 40, 'evaluateSeconds': 10, 'cleanupSeconds': 58,
                              'combinedBytes': CAP, 'ownedRSSBytes': 2147483648, 'traceEvents': 2048}, 'Exact diagnostic limits')
    require(cfg['stopNewLaunchUTC'] == '2026-10-15T23:00:00Z', 'Unchanged launch cutoff')
    require(raw('payload.bin', 3840) == bytes((73 * i + 19) % 256 for i in range(3840)), 'Independent expected fixture formula')


def public_manifest():
    manifest = document('review/evidence-manifest.json', 1048576)
    receipt = document('publication/capture-execution.json')
    require(manifest['kind'] == 'new-control-channel-public-evidence-manifest' and type(manifest['version']) is int and manifest['version'] == 1, 'Final evidence manifest kind/version')
    same_values(manifest, receipt, ['sourceCommit', 'sourceFreezeSHA256'])
    pins = manifest['files']
    require(type(pins) is list and 1 <= len(pins) <= 128, 'Bounded evidence manifest')
    require(all(type(p.get('bytes')) is int and 0 <= p['bytes'] <= CAP for p in pins)
            and sum(p['bytes'] for p in pins) <= CAP, 'Public manifest aggregate read cap')
    seen = set()
    for pin in pins:
        path = pin['path']
        require(path not in seen, 'Unique public evidence path')
        require(path.startswith(('raw/', 'results/', 'publication/')) or path == 'capture-launch.lock', 'Public evidence allowlist')
        require(not path.startswith('publication/source-'), 'No unrelated publication source evidence')
        seen.add(path)
        data = raw(path, CAP)
        require(type(pin['bytes']) is int and pin['bytes'] == len(data) and pin['sha256'] == digest(data), 'Exact final evidence bytes')
    required = {'results/result.json', 'raw/trace.public.ndjson', 'results/wrapper.json', 'results/budget.json', 'results/capture.json',
                'results/sole-launch.lock', 'results/diagnostic-stdout.txt', 'results/diagnostic-stderr.txt', 'capture-launch.lock',
                'publication/capture-output.json', 'publication/observer-output.json', 'publication/capture-execution.json'}
    require(required <= seen, 'Required evidence manifest entries')
    for directory in ['raw', 'results']:
        folder = BASE / directory
        require(folder.is_dir() and not folder.is_symlink(), 'Regular runtime evidence directory')
        actual = set()
        for path in folder.iterdir():
            require(path.is_file() and not path.is_symlink(), 'Flat regular runtime evidence files')
            actual.add(str(path.relative_to(BASE)))
        require(actual == {p for p in seen if p.startswith(directory + '/')}, 'Complete runtime directory manifest')


def lifecycle():
    r = document('results/result.json'); w = document('results/wrapper.json')
    b = document('results/budget.json'); c = document('results/capture.json')
    o = document('publication/observer-output.json'); s = document('publication/capture-output.json')
    e = document('publication/capture-execution.json')
    for record in [w, b, c]:
        for name, value in record.items():
            if name.endswith(('Bytes', 'Files', 'Invocations', 'Samples', 'ExitCode')) or name in ['attempts', 'rssProbeErrors', 'registeredDetachedGroups', 'detachedGroupsConfirmedAbsent', 'detachedGroupKillSignals']:
                require(type(value) is int and value >= 0, 'Integer lifecycle counters and byte sizes')
    require(e['kind'] == 'actual-control-channel-capture-tool-completion', 'External completion receipt kind')
    true_fields(e, ['toolSessionCompleted'])
    require(type(e['actualCaptureExitCode']) is int and e['actualCaptureExitCode'] == 0 and finite(e['actualFullElapsedSeconds']), 'Actual external capture completion')
    for item in [r, b, c, o]:
        same_values(item, e, ['sourceCommit', 'sourceFreezeSHA256'])
    require(w['kind'] == 'single-transport-relay' and b['kind'] == 'whole-transport-lifecycle-observation'
            and c['kind'] == 'external-transport-lifecycle-observation', 'Lifecycle record kinds')
    require(o['kind'] == 'caller-retained-transport-observer-summary' and s['kind'] == 'external-transport-capture-summary', 'Lifecycle summary kinds')
    true_fields(w, ['terminal', 'nodeReaped', 'pipeCaptureComplete', 'externalObserverRequired'])
    require(w['nodeInvocations'] == 1 and w['nodeExitCode'] == 0 and w['errors'] == [] and finite(w['wallSecondsBeforeReceipt'], upper=40), 'Relay closure and work bound')
    false_fields(w, ['qualified'])
    require(w['pipeByteCapTotal'] == 65536, 'Relay pipe cap')
    for name in ['stdout', 'stderr']:
        size = len(raw('results/diagnostic-' + name + '.txt'))
        require(size == w[name + 'Bytes'] == w[name + 'ObservedBytes'], 'Exact Node pipe persistence')
    require(w['stdoutBytes'] + w['stderrBytes'] <= 65536, 'Observed Node pipe bound')
    true_fields(b, ['terminal', 'wrapperReaped', 'wrapperGroupAbsent', 'wrapperPipeCaptureComplete', 'registryComplete',
                    'outputAccountingComplete', 'candidateLifecycleVerified', 'processClosureComplete',
                    'externalCompletionObservationRequired', 'requiresCallerObservedObserverExit0AndElapsedUnder60'])
    false_fields(b, ['active', 'wholeLifecycleVerified', 'qualified', 'retryPermitted', 'cleanupErrorObserved'])
    require(b['attempts'] == b['wrapperInvocations'] == 1 and b['wrapperExitCode'] == b['exitCode'] == 0 and b['errors'] == [], 'One completed observer invocation')
    require(b['wallCapSeconds'] == 60 and b['workStopSeconds'] == 40 and b['cleanupStopSeconds'] == 58,
            'Observer time limits')
    require(b['rawByteCap'] == b['combinedByteCap'] == CAP and b['ownedRSSByteCap'] == 2147483648 and b['provenanceReserveBytes'] == 131072, 'Observer resource limits')
    require(integer(b['rssSamples'], 1) and b['rssProbeErrors'] == 0 and integer(b['peakObservedOwnedRSSBytes'], 0, 2147483648), 'Sampled owned RSS evidence')
    require(b['registeredDetachedGroups'] == b['detachedGroupsConfirmedAbsent'] == 1, 'One observed browser group closed')
    require(integer(b['detachedGroupKillSignals'], 0, 1) and finite(b['wallSecondsBeforeFinalRecords'], upper=60), 'Observer final timing')
    require(b['reportedDiagnosticQualified'] == r['qualified'] and b['reportedDiagnosticStatus'] == r['status'], 'Observer worker projection')
    require(b['pipeByteCapCombined'] == 8192 and b['stdoutBytesObserved'] == b['stdoutBytesRetained']
            and b['stderrBytesObserved'] == b['stderrBytesRetained']
            and integer(b['stdoutBytesRetained'] + b['stderrBytesRetained'], 0, 8192), 'Complete relay pipe retention')
    true_fields(c, ['terminal', 'observerReaped', 'observerPipeCaptureComplete', 'observerSummaryValidated',
                    'outputAccountingComplete', 'candidateWholeLifecycleVerified', 'requiresActualCaptureExit0AndCompleteFinalSummary'])
    false_fields(c, ['active', 'directObserverKillSent', 'descendantCleanupInferredFromCallerKill', 'wholeLifecycleVerified', 'qualified', 'retryPermitted'])
    require(c['observerInvocations'] == 1 and c['actualObserverExitCode'] == 0 and c['errors'] == []
            and finite(c['observerFullElapsedSeconds']) and finite(c['wallSecondsBeforeFinalRecords']), 'Actual captured observer exit/time')
    require(c['observerPipeByteCapCombined'] == 16384 and c['callerStopSeconds'] == 59.5
            and c['callerReapStopSeconds'] == 59.75 and c['callerHardSeconds'] == 60, 'Capture bounds')
    require(c['stderrBytesObserved'] == c['stderrBytesRetained'] == 0, 'Empty observer error stream')
    same_values(o, b, ['sourceCommit', 'sourceFreezeSHA256', 'candidateLifecycleVerified', 'wholeLifecycleVerified', 'qualified',
                        'requiresCallerObservedObserverExit0AndElapsedUnder60', 'budgetBytes', 'outputAccountingComplete',
                        'accountedTotalResultBytes', 'observedPrefixResultBytes', 'wrapperExitCode', 'errors'])
    require(o['budgetSHA256'] == digest(raw('results/budget.json')) and o['summaryBytes'] == len(raw('publication/observer-output.json')),
            'Actual observer summary binding')
    same_values(s, c, ['candidateWholeLifecycleVerified', 'wholeLifecycleVerified', 'qualified',
                        'requiresActualCaptureExit0AndCompleteFinalSummary', 'actualObserverExitCode',
                        'observerFullElapsedSeconds', 'outputAccountingComplete', 'accountedCombinedResultBytes'])
    require(s['captureReceiptSHA256'] == digest(raw('results/capture.json')) and s['captureReceiptBytes'] == len(raw('results/capture.json'))
            and s['summaryBytes'] == len(raw('publication/capture-output.json')), 'Actual capture summary binding')
    require(c['observerSummarySHA256'] == digest(raw('publication/observer-output.json'))
            and c['observerBudgetSHA256'] == digest(raw('results/budget.json')), 'Capture observer projection binding')


def accounting():
    b = document('results/budget.json'); c = document('results/capture.json')
    manifest = document('review/evidence-manifest.json', 1048576)
    pins = {p['path']: p for p in manifest['files']}
    require(raw('capture-launch.lock') == b'One external transport capture reserved. Permanent; no retry.\n'
            and raw('results/sole-launch.lock') == b'One transport invocation reserved. Permanent; no retry.\n', 'Exact permanent launch reservations')
    raw_paths = [p for p in pins if p.startswith('raw/')]
    initial_results = [p for p in pins if p.startswith('results/') and p not in ['results/budget.json', 'results/capture.json']]
    raw_bytes = sum(pins[p]['bytes'] for p in raw_paths)
    result_bytes = sum(pins[p]['bytes'] for p in initial_results)
    require(b['rawBytes'] == b['lastObservedRawBytes'] == raw_bytes and b['rawFiles'] == b['lastObservedRawFiles'] == len(raw_paths), 'Exact raw accounting')
    require(b['resultDirectoryBytes'] == b['lastObservedResultDirectoryBytes'] == result_bytes
            and b['resultDirectoryFiles'] == b['lastObservedResultDirectoryFiles'] == len(initial_results), 'Exact initial results accounting')
    require(integer(b['privateDiagnosticBytes']) and b['privateDiagnosticBytes'] == b['lastObservedPrivateDiagnosticBytes']
            and integer(b['privateDiagnosticFiles'], 1, 4096) and b['privateDiagnosticFiles'] == b['lastObservedPrivateDiagnosticFiles'], 'Bounded reported private diagnostic accounting')
    # Private files/process tables are not independently read; these remain observer claims.
    require(b['budgetBytes'] == len(raw('results/budget.json')) and b['observerSummaryBytes'] == len(raw('publication/observer-output.json')), 'Final observer record lengths')
    total = raw_bytes + result_bytes + b['privateDiagnosticBytes'] + b['budgetBytes'] + b['observerSummaryBytes']
    require(b['accountedTotalResultBytes'] == b['observedPrefixResultBytes'] == c['observedInnerAccountedResultBytes'] == total,
            'Observer complete byte equation')
    observer_summary_bytes = len(raw('publication/observer-output.json'))
    require(c['stdoutBytesObserved'] == c['stdoutBytesRetained'] == observer_summary_bytes
            and c['privateCaptureBytes'] == observer_summary_bytes, 'Capture exact retained observer summary')
    require(c['captureLockBytes'] == len(raw('capture-launch.lock')) and c['receiptBytes'] == len(raw('results/capture.json'))
            and c['callerSummaryBytes'] == len(raw('publication/capture-output.json')), 'Capture final record lengths')
    additional = c['captureLockBytes'] + c['stderrBytesRetained'] + c['receiptBytes'] + c['callerSummaryBytes']
    require(c['accountedCombinedResultBytes'] == total + additional
            and c['observedCallerArtifactBytes'] == c['privateCaptureBytes'] + c['captureLockBytes'] + c['receiptBytes'] + c['callerSummaryBytes'],
            'Capture complete byte equations')
    publication_bytes = sum(len(raw(p, CAP)) for p in pins if p.startswith('publication/'))
    require(integer(c['accountedCombinedResultBytes']) and raw_bytes <= CAP
            and c['accountedCombinedResultBytes'] + publication_bytes + len(raw('review/evidence-manifest.json', 1048576)) <= CAP,
            'Diagnostic plus later public-copy byte bound')


def worker_and_bytes():
    global BYTE_FINDING
    r = document('results/result.json')
    require(r['kind'] == 'synthetic-control-channel-diagnostic' and type(r['version']) is int and r['version'] == 1, 'Worker identity')
    true_fields(r, ['terminal', 'browserClosed', 'runtimePinsBefore', 'runtimePinsAfter', 'localObservationComplete'])
    false_fields(r, ['qualified', 'scientificSuccess', 'explainsHistoricalFailure', 'retryPermitted'])
    require(type(r['browserLaunches']) is int and r['browserLaunches'] == 1 and type(r['evaluateCalls']) is int and r['evaluateCalls'] == 1
            and type(r['applicationFetchCalls']) is int and r['applicationFetchCalls'] == 0, 'Sole browser/evaluate and no application fetch')
    require(r['browserVersion'] == '155.0.8059.80' and finite(r['elapsedSeconds'], upper=40), 'Worker browser and time bound')
    require(r['errors'] == r['cleanupErrors'] == r['protocolDeviations'] == [], 'Complete worker without errors/deviations')
    fixture = raw('payload.bin', 3840)
    require(r['expected'] == {'bytes': len(fixture), 'sha256': digest(fixture)}, 'Expected fixture receipt')
    ev = r['evaluation']; ret = r['returned']; persisted = r['persistence']; timing = r['timing']; ins = r['instrumentation']
    true_fields(ev, ['settled']); false_fields(ev, ['timedOut', 'deadlineExceeded'])
    require(finite(ev['hostMilliseconds'], upper=10000), 'Settled evaluation timing under adopted limit')
    require(ins['ready'] == {'playwright': True, 'cdpNetwork': True, 'cdpAudits': True, 'routes': True}, 'All observers and routes ready')
    true_fields(ins['ready'], ['playwright', 'cdpNetwork', 'cdpAudits', 'routes'])
    true_fields(ins, ['complete', 'collectionBeforeEvaluate', 'captureClosedAfterCleanup'])
    false_fields(ins, ['crossClockOrderingClaimed'])
    require(ins['clock'] == 'worker-monotonic-receipt' and ins['browserClock'] == 'browser-performance-independent', 'Independent clock labeling')
    for name in ['droppedEvents', 'truncatedEvents', 'observerExceptions', 'callbackErrors', 'unexpectedRedirectObservations', 'unexpectedApplicationRequestObservations']:
        require(type(ins[name]) is int and ins[name] == 0, 'Complete untruncated observation')
    trace_bytes = raw('raw/trace.public.ndjson', 2097152)
    require(trace_bytes.endswith(b'\n'), 'Complete trace final newline')
    lines = trace_bytes.splitlines()
    require(1 <= len(lines) <= 2048 and all(0 < len(line) < 8192 for line in lines), 'Bounded trace lines/events')
    events = [json.loads(line, parse_int=json_integer, parse_constant=no_constant, object_pairs_hook=no_duplicate_pairs) for line in lines]
    require(type(ins['eventCount']) is int and ins['eventCount'] == ins['attemptedEvents'] == len(events) and ins['eventCap'] == 2048,
            'Exact retained event accounting')
    last = -1
    by_kind = {}
    for index, event in enumerate(events, 1):
        require(type(event) is dict and set(event) == {'version', 'id', 'sequence', 'clock', 'milliseconds', 'kind', 'data'}, 'Trace event envelope')
        require(type(event['version']) is int and event['version'] == 1 and type(event['sequence']) is int and event['sequence'] == index
                and event['id'] == 'e' + str(index) and event['clock'] == 'worker-monotonic-receipt', 'Contiguous trace event identities')
        require(finite(event['milliseconds'], upper=40000) and event['milliseconds'] >= last and type(event['data']) is dict, 'Worker trace ordering')
        last = event['milliseconds']
        require(type(event['kind']) is str, 'Text trace event kind')
        by_kind.setdefault(event['kind'], []).append(event)
        if event['kind'].startswith(('control-', 'persistence-')):
            require(event['data'].get('transferID') == 'channel-1', 'One control transfer trace identity')
        if event['kind'] in ['pw-request', 'cdp-request']:
            data = event['data']
            require(data.get('method') == 'GET' and data.get('resourceType') not in ['fetch', 'xhr', 'Fetch', 'XHR']
                    and data.get('redirected') is False, 'No observed application payload request or redirect')
    def sole(kind):
        records = by_kind.get(kind, [])
        require(len(records) == 1, 'Exactly one ' + kind + ' event')
        return records[0]
    ready = sole('observers-ready'); started = sole('control-evaluate-started'); cleanup = sole('cleanup-finished')
    require(ready['id'] == r['observerReadyEvent'] and ready['sequence'] < started['sequence'] < cleanup['sequence']
            and cleanup['sequence'] == len(events) and cleanup['data'].get('complete') is True, 'Observation brackets evaluation and cleanup')
    require(not any(by_kind.get(k) for k in ['worker-error', 'observer-callback-error', 'page-crash']), 'No trace-recorded worker failure')
    require(r['trace']['public'] == {'bytes': len(trace_bytes), 'sha256': digest(trace_bytes)}, 'Exact public trace receipt')
    private = r['trace']['private']
    require(type(private) is dict and integer(private.get('bytes'), 1, 3145728)
            and type(private.get('sha256')) is str and len(private['sha256']) == 64
            and all(c in '0123456789abcdef' for c in private['sha256']), 'Bounded private trace receipt; bytes not independently read')
    summary_bytes = raw('results/diagnostic-stdout.txt', 4096)
    require(summary_bytes.endswith(b'\n') and len(summary_bytes.splitlines()) == 1, 'One complete Node summary')
    summary = document('results/diagnostic-stdout.txt', 4096)
    require(summary['kind'] == 'synthetic-control-channel-worker-summary' and summary['terminal'] is True and summary['qualified'] is False
            and summary['status'] == r['status'] and summary['resultBytes'] == len(raw('results/result.json'))
            and summary['resultSHA256'] == digest(raw('results/result.json')) and raw('results/diagnostic-stderr.txt') == b'', 'Actual worker summary and empty error stream')
    require(type(ret['received']) is bool, 'Returned flag is boolean')
    if ret['received']:
        true_fields(ret, ['validationPassed'])
        require(ret['validationError'] is None and ret['rejectionProjection'] is None and ev['errorName'] is None, 'Validated returned envelope')
        returned_bytes = raw('raw/returned.json', 32768)
        actual = document('raw/returned.json', 32768)
        require(type(actual) is dict and set(actual) == {'version','format','payloadId','byteLength','values','origin','isSecureContext',
                                                       'constructionPhase','browserConstructionMilliseconds'}, 'Exact returned JSON envelope fields')
        require(type(actual['version']) is int and actual['version'] == 1 and actual['format'] == 'uint8-values-v1'
                and actual['payloadId'] == 'synthetic-control-channel-3840-v1' and type(actual['byteLength']) is int
                and actual['byteLength'] == 3840 and actual['constructionPhase'] == 'array-ready', 'Returned envelope identity')
        require(actual['origin'] == 'http://127.0.0.1:8876' and type(actual['isSecureContext']) is bool
                and finite(actual['browserConstructionMilliseconds'], upper=10000), 'Returned context and construction duration')
        actual_binary = byte_array(actual['values'])
        persisted_binary = raw('raw/received.bin', 3840)
        facts = compare_bytes(actual['values'], persisted_binary, fixture)
        require(facts['persisted_matches_returned'], 'Actual persisted file equals actual returned byte array')
        require(ret['json'] == {'bytes': len(returned_bytes), 'sha256': digest(returned_bytes)}
                and ret['bytes'] == len(actual_binary) and ret['sha256'] == digest(actual_binary)
                and type(ret['exact']) is bool and ret['exact'] == facts['returned_matches_fixture'], 'Independent returned receipt reconstruction')
        true_fields(persisted, ['attempted', 'opened', 'closed', 'complete', 'exists', 'equalsReturned'])
        require(type(persisted['writtenBytes']) is int and persisted['writtenBytes'] == len(persisted_binary)
                and type(persisted['bytes']) is int and persisted['bytes'] == len(persisted_binary)
                and integer(persisted['writeCalls'], 1, 3840) and persisted['sha256'] == digest(persisted_binary)
                and type(persisted['exact']) is bool and persisted['exact'] == facts['persisted_matches_fixture'], 'Independent persistence receipt reconstruction')
        require(r['browserContext'] == {'originLabel': 'page-origin', 'isSecureContext': actual['isSecureContext']}
                and timing['browserConstructionMilliseconds'] == actual['browserConstructionMilliseconds'], 'Explicit browser context projection')
        require(finite(timing['hostValidationMilliseconds'], upper=40000) and finite(timing['hostPersistenceMilliseconds'], upper=40000), 'Host stage timings')
        returned_event = sole('control-evaluate-returned'); validated = sole('control-envelope-validated')
        persist_start = sole('persistence-started'); persist_end = sole('persistence-completed')
        require(not by_kind.get('control-evaluate-error') and started['sequence'] < returned_event['sequence'] < validated['sequence']
                < persist_start['sequence'] < persist_end['sequence'] < cleanup['sequence'], 'Successful-return stage ordering')
        vd = validated['data']; pd = persist_end['data']
        require(vd.get('valid') is True and vd.get('jsonBytes') == len(returned_bytes) and vd.get('bytes') == 3840
                and vd.get('sha256') == facts['returned_sha256'] and type(vd.get('exact')) is bool
                and vd['exact'] == facts['returned_matches_fixture'], 'Validated trace byte projection')
        require(persist_start['data'].get('bytes') == 3840 and persist_start['data'].get('sha256') == facts['returned_sha256']
                and pd.get('complete') is True and pd.get('bytes') == 3840 and pd.get('sha256') == facts['returned_sha256'], 'Persistence trace byte projection')
        writes = by_kind.get('persistence-write', [])
        require(len(writes) == persisted['writeCalls'], 'Trace write-call count')
        previous = 0
        for number, event in enumerate(writes, 1):
            data = event['data']
            require(persist_start['sequence'] < event['sequence'] < persist_end['sequence']
                    and type(data.get('writtenBytes')) is int and previous < data['writtenBytes'] <= 3840
                    and type(data.get('writeCalls')) is int and data['writeCalls'] == number, 'Cumulative actual persistence writes')
            previous = data['writtenBytes']
        require(previous == 3840, 'Final cumulative persistence byte count')
        success = facts['returned_matches_fixture'] and facts['persisted_matches_fixture']
        require(r['status'] == ('synthetic-control-transfer-complete' if success else 'received-content-mismatch'), 'Transfer classification independent of producer')
        require(r['lastPhase'] == 'persistence-returned', 'Returned persistence phase')
        BYTE_FINDING = {'evaluationReturned': True, 'transferSuccess': success, **facts}
    else:
        require(ret == {'received':False,'validationPassed':False,'validationError':None,'json':None,'rejectionProjection':None,'bytes':None,'sha256':None,'exact':False}, 'Complete rejected-return state')
        require(persisted == {'attempted':False,'opened':False,'closed':False,'complete':False,'writtenBytes':0,'writeCalls':0,
                              'exists':False,'bytes':None,'sha256':None,'exact':False,'equalsReturned':False}, 'No persistence after failed extraction')
        require(not (BASE / 'raw/returned.json').exists() and not (BASE / 'raw/received.bin').exists(), 'No invented returned or persisted bytes')
        require(type(ev['errorName']) is str and ev['errorName'] and r['browserContext'] is None
                and all(v is None for v in timing.values()), 'Settled rejection metadata')
        rejected = sole('control-evaluate-error')
        require(started['sequence'] < rejected['sequence'] < cleanup['sequence'] and rejected['data'].get('errorName') == ev['errorName'], 'Settled rejection trace')
        require(not any(by_kind.get(k) for k in ['control-evaluate-returned','control-envelope-validated','persistence-started','persistence-write','persistence-completed']), 'No post-rejection payload events')
        require(r['status'] == 'control-return-failed' and r['lastPhase'] == 'evaluate-rejected', 'Complete failed-transfer classification')
        BYTE_FINDING = {'evaluationReturned': False, 'transferSuccess': False, 'persistedMatchesReturned': None, 'fixtureEquality': None}


def main():
    global BASE, REPO, OUTPUT
    require(len(sys.argv) == 2 and Path(sys.argv[1]).is_absolute(), 'One absolute campaign path')
    BASE = Path(sys.argv[1]).resolve()
    REPO = BASE.parents[1]
    require(BASE.is_dir() and not BASE.is_symlink(), 'Campaign directory')
    with (BASE / 'review.lock').open('xb') as handle:
        require(handle.write(LOCK) == len(LOCK), 'Complete permanent review reservation')
    OUTPUT = BASE / 'review/results'
    OUTPUT.mkdir(exist_ok=False)
    require(datetime.datetime.now(datetime.timezone.utc) < CUTOFF, 'Original review launch cutoff')
    for name, action in [('source_identity', source_identity), ('final_public_manifest', public_manifest),
                         ('worker_trace_and_exact_bytes', worker_and_bytes), ('complete_lifecycle_projections', lifecycle),
                         ('resource_and_output_accounting', accounting)]:
        group(name, action)


try:
    main()
except Exception as error:
    reason = str(error) if type(error) is ValueError else 'Review admission or evidence operation failed'
    ERRORS.append({'group': 'admission', 'type': type(error).__name__, 'reason': reason[:300]})

passed = len(GROUPS) == 5 and all(g['pass'] for g in GROUPS) and not ERRORS
report = {'kind': 'saved-control-channel-public-evidence-review', 'terminal': True, 'active': False,
          'recordIntegrityCandidate': passed, 'recordIntegrityVerified': False,
          'requiresExternalReviewExit0AndCompleteFinalSummary': True, 'qualified': False,
          'transferSuccess': BYTE_FINDING.get('transferSuccess') if BYTE_FINDING else None,
          'byteEvidence': BYTE_FINDING, 'groups': GROUPS, 'errors': ERRORS,
          'wallSecondsBeforeFinalRecords': time.monotonic() - START,
          'wallCapSeconds': 30, 'workStopSeconds': 25, 'finalStopSeconds': 29,
          'scope': 'Saved public records and bytes only. No operational source import or execution. Private process/diagnostic claims are checked for consistency, not independently reobserved.',
          'retryPermitted': False, 'reviewLockBytes': len(LOCK), 'reviewArtifactBytes': None,
          'accountedDiagnosticAndLaterPublicReviewBytes': None,
          'accountingScope': 'Diagnostic combined receipt plus retained publication copies, final evidence manifest, review lock/report/summary and one extra summary stdout copy. Any later external review completion receipt must be added by its external recorder.'}
try:
    require(time.monotonic() < FINAL_END, 'Review finalization deadline')
    require(OUTPUT is not None, 'Review output admission')
    prefix = None
    if any(g['group'] == 'resource_and_output_accounting' and g['pass'] for g in GROUPS):
        manifest = DOC['review/evidence-manifest.json']
        prefix = DOC['results/capture.json']['accountedCombinedResultBytes'] + len(CACHE['review/evidence-manifest.json'])
        prefix += sum(len(CACHE[p['path']]) for p in manifest['files'] if p['path'].startswith('publication/'))
    for _ in range(12):
        encoded = (json.dumps(report, sort_keys=True) + '\n').encode()
        summary = {'kind': 'saved-control-channel-review-summary', 'reportSHA256': digest(encoded), 'reportBytes': len(encoded),
                   'recordIntegrityCandidate': passed, 'recordIntegrityVerified': False, 'qualified': False,
                   'requiresExternalReviewExit0AndCompleteFinalSummary': True,
                   'transferSuccess': report['transferSuccess'], 'groupsPassed': sum(g['pass'] for g in GROUPS),
                   'groupsTotal': len(GROUPS), 'errors': len(ERRORS),
                   'accountedDiagnosticAndLaterPublicReviewBytes': report['accountedDiagnosticAndLaterPublicReviewBytes']}
        summary_bytes = (json.dumps(summary, sort_keys=True) + '\n').encode()
        artifact_bytes = len(LOCK) + len(encoded) + len(summary_bytes)
        combined = prefix + artifact_bytes + len(summary_bytes) if prefix is not None else None
        if report['reviewArtifactBytes'] == artifact_bytes and report['accountedDiagnosticAndLaterPublicReviewBytes'] == combined:
            break
        report.update(reviewArtifactBytes=artifact_bytes, accountedDiagnosticAndLaterPublicReviewBytes=combined)
    else:
        raise ValueError('Review accounting fixed point')
    require(combined is None or combined <= CAP, 'Diagnostic and later public review aggregate cap')
    require(len(encoded) <= 65536 and len(summary_bytes) <= 4096, 'Review output caps')
    with (OUTPUT / 'report.json').open('xb') as handle:
        require(handle.write(encoded) == len(encoded), 'Complete review report')
    with (OUTPUT / 'summary.json').open('xb') as handle:
        require(handle.write(summary_bytes) == len(summary_bytes), 'Complete review summary')
    require(os.write(sys.stdout.fileno(), summary_bytes) == len(summary_bytes), 'Complete review stdout')
except Exception:
    os._exit(125)
raise SystemExit(0 if passed else 1)
