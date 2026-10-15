"""Future saved-evidence reviewer. Static source preparation; no invocation allocated."""
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import sys
import time

sys.dont_write_bytecode = True
from byte_primitives import compare_byte_evidence, decode_byte_values, expected_bytes
from review_primitives import admit_review, json_bytes, read_bounded, require, strict_equal, utc_timestamp, validate_page_claims

CAP = 8388608
BASE = REPO = None
CACHE = {}
DOC = {}
GROUPS = []
ERRORS = []
FINDING = None
ADMISSION = None
WORK_END = float('inf')
LOCK = b'One saved GPU-readback review reserved. Permanent; no retry.\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def finite(value, lower=0, upper=60):
    return (type(value) in (int,float) and math.isfinite(value) and lower <= value < upper
            and not (type(value) is float and value == 0 and math.copysign(1,value) < 0))


def integer(value, lower=0, upper=CAP):
    return type(value) is int and lower <= value <= upper


def raw(relative, cap=131072):
    require(time.monotonic() < WORK_END, 'Review work deadline')
    if relative not in CACHE:
        CACHE[relative] = read_bounded(BASE, relative, cap)
    require(len(CACHE[relative]) <= cap, 'Evidence cache cap')
    return CACHE[relative]


def document(relative, cap=131072):
    if relative not in DOC:
        DOC[relative] = json_bytes(raw(relative,cap),cap)
    return DOC[relative]


def same_values(left, right, names):
    require(all(name in left and name in right and strict_equal(left[name],right[name])
                for name in names), 'Named shared-field projection mismatch')


def true_fields(record, names):
    require(all(record.get(name) is True for name in names), 'Required true completion flags')


def false_fields(record, names):
    require(all(record.get(name) is False for name in names), 'Premature qualification or prohibited flag')


def group(name, action):
    try:
        action()
        GROUPS.append({'group':name,'pass':True})
    except Exception as error:
        reason = str(error) if type(error) is ValueError else 'Evidence unavailable or invalid'
        ERRORS.append({'group':name,'type':type(error).__name__,'reason':reason[:240]})
        GROUPS.append({'group':name,'pass':False})


def source_identity():
    freeze = document('freeze.json',1048576)
    receipt = document('publication/capture-execution.json')
    source = receipt['sourceCommit']
    require(type(source) is str and len(source)==40 and all(c in '0123456789abcdef' for c in source), 'Source commit identity')
    require(receipt['sourceFreezeSHA256'] == digest(raw('freeze.json',1048576)), 'Externally retained freeze identity')
    pins = freeze['files']
    require(type(pins) is list and 1<=len(pins)<=256, 'Bounded frozen source inventory')
    seen = set(); total = 0
    for pin in pins:
        path = pin['path']; require(path not in seen, 'Unique frozen source path'); seen.add(path)
        require(time.monotonic()<WORK_END, 'Source read deadline')
        data = read_bounded(REPO,path,1048576); total += len(data)
        require(total<=33554432 and type(pin['bytes']) is int and len(data)==pin['bytes'] and digest(data)==pin['sha256'], 'Exact bounded frozen source bytes')
    needed = ['source/'+name for name in ['capture-transport.py','observe-transport.py','run-once.py','process-registry.cjs',
              'admission.py','host-worker.cjs','host-logic.cjs','validation.cjs','gpu-readback-page.js','browser.html','fixture.wgsl','FIXTURE.json']]
    needed += ['PROTOCOL.md','config.json','runtime-provenance.json','expected.bin']
    needed += [str(Path(__file__).resolve().relative_to(BASE)),str(Path(__file__).with_name('byte_primitives.py').resolve().relative_to(BASE)),
               str(Path(__file__).with_name('review_primitives.py').resolve().relative_to(BASE))]
    require(all(str((BASE/name).relative_to(REPO)) in seen for name in needed), 'Required new source and independent reference pins')
    require(raw('expected.bin',128)==expected_bytes(), 'Independent complete little-endian fixture')
    # Config was the sole evidence file read before admission; freeze now binds it.
    require(read_bounded(BASE,'config.json',16384)==CACHE['config.json'], 'Allocation config unchanged since admission')


def public_manifest():
    manifest = document('review/evidence-manifest.json',1048576)
    receipt = document('publication/capture-execution.json')
    require(manifest['kind']=='new-gpu-readback-public-evidence-manifest' and type(manifest['version']) is int and manifest['version']==1,
            'Final public manifest identity')
    same_values(manifest,receipt,['sourceCommit','sourceFreezeSHA256'])
    pins = manifest['files']; require(type(pins) is list and 1<=len(pins)<=128,'Bounded public inventory')
    require(all(type(p.get('bytes')) is int and 0<=p['bytes']<=CAP for p in pins) and sum(p['bytes'] for p in pins)<=CAP,'Aggregate public read cap')
    seen = set()
    allowed={'raw/trace.public.ndjson','raw/returned.json','raw/rejected-return.json','raw/received.bin',
             'results/result.json','results/wrapper.json','results/budget.json','results/capture.json','results/sole-launch.lock',
             'results/diagnostic-stdout.txt','results/diagnostic-stderr.txt','capture-launch.lock',
             'publication/capture-output.json','publication/observer-output.json','publication/capture-execution.json'}
    for pin in pins:
        path=pin['path']; require(path not in seen,'Unique public evidence path'); seen.add(path)
        require(path in allowed,'Exact public evidence allowlist')
        data=raw(path,CAP); require(len(data)==pin['bytes'] and digest(data)==pin['sha256'],'Exact final public evidence bytes')
    required={'raw/trace.public.ndjson','results/result.json','results/wrapper.json','results/budget.json','results/capture.json',
              'results/sole-launch.lock','results/diagnostic-stdout.txt','results/diagnostic-stderr.txt','capture-launch.lock',
              'publication/capture-output.json','publication/observer-output.json','publication/capture-execution.json'}
    require(required<=seen,'Required final public evidence')
    for directory in ['raw','results']:
        folder=BASE/directory; require(folder.is_dir() and not folder.is_symlink(),'Regular runtime evidence directory')
        paths=set()
        for count,path in enumerate(folder.iterdir(),1):
            require(count<=128,'Bounded runtime directory entry count')
            require(path.is_file() and not path.is_symlink(),'Flat regular runtime evidence files')
            paths.add(str(path.relative_to(BASE)))
        require(paths=={p for p in seen if p.startswith(directory+'/')},'Complete raw/results directory inventory')


def closed_write(receipt, data):
    true_fields(receipt,['attempted','opened','closed','complete'])
    require(type(receipt['writtenBytes']) is int and receipt['writtenBytes']==len(data)
            and integer(receipt['writeCalls'],1,len(data)) and type(receipt['bytes']) is int and receipt['bytes']==len(data)
            and receipt['sha256']==digest(data),'Exact closed write receipt against actual bytes')


def no_persistence(receipt):
    false_fields(receipt,['attempted','opened','closed','complete','exists'])
    require(type(receipt['writtenBytes']) is int and receipt['writtenBytes']==0 and type(receipt['writeCalls']) is int
            and receipt['writeCalls']==0 and all(receipt[k] is None for k in ['bytes','sha256','exact','equalsReturned']), 'No invented persistence')
    require(not (BASE/'raw/received.bin').exists(),'No binary file for absent values')


def lifecycle():
    r = document('results/result.json'); w = document('results/wrapper.json')
    b = document('results/budget.json'); c = document('results/capture.json')
    o = document('publication/observer-output.json'); s = document('publication/capture-output.json')
    e = document('publication/capture-execution.json')
    for record in [w, b, c]:
        for name, value in record.items():
            if name.endswith(('Bytes', 'Files', 'Invocations', 'Samples', 'ExitCode')) or name in ['attempts', 'rssProbeErrors', 'registeredDetachedGroups', 'detachedGroupsConfirmedAbsent', 'detachedGroupKillSignals']:
                require(type(value) is int and value >= 0, 'Integer lifecycle counters and byte sizes')
    require(e['kind'] == 'actual-gpu-readback-capture-tool-completion', 'External completion receipt kind')
    capture_start = utc_timestamp(e['captureStartedUTC'])
    capture_end = utc_timestamp(e['captureCompletedUTC'])
    require(ADMISSION['diagnostic_start'] <= capture_start < ADMISSION['diagnostic_stop']
            and capture_start <= capture_end and (capture_end-capture_start).total_seconds() <= 60,
            'External capture interval and allocated launch window')
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


def actual_return_and_trace():
    global FINDING
    r=document('results/result.json',65536)
    require(r['kind']=='synthetic-gpu-readback-diagnostic' and type(r['version']) is int and r['version']==1
            and r['fixtureId']=='m31-u32-readback-128-v1','GPU host identity')
    true_fields(r,['terminal','executionAllocated','runtimePinsBefore','runtimePinsAfter','localObservationComplete',
                   'browserCloseAttempted','browserCloseReturned','browserClosed','externalCompletionRequired'])
    false_fields(r,['qualified','scientificSuccess','explainsHistoricalFailure','performanceClaim','retryPermitted','independentPersistenceVerified'])
    require(type(r['browserLaunches']) is int and r['browserLaunches']==1 and type(r['evaluateCalls']) is int and r['evaluateCalls']==1
            and type(r['applicationFetchCalls']) is int and r['applicationFetchCalls']==0,'One observed host invocation')
    require(r['browserVersion']=='155.0.8059.80' and finite(r['elapsedSeconds'],upper=40)
            and r['errors']==r['cleanupErrors']==r['protocolDeviations']==[],'Complete host observation')
    require(strict_equal(r['expected'],{'bytes':128,'sha256':digest(expected_bytes())}),'Independent expected fixture receipt')
    ev=r['evaluation']; ret=r['returned']; persistence=r['persistence']; timing=r['timing']; ins=r['instrumentation']
    true_fields(ev,['settled']); false_fields(ev,['timedOut','deadlineExceeded'])
    require(type(ev['limitMilliseconds']) is int and ev['limitMilliseconds']==12000 and finite(ev['hostMilliseconds'],upper=12000),
            'Complete evaluation within fixed host allowance')
    true_fields(ins['ready'],['playwright','cdpNetwork','cdpAudits','routes'])
    require(set(ins['ready'])=={'playwright','cdpNetwork','cdpAudits','routes'},'Fixed instrumentation readiness')
    true_fields(ins,['complete','collectionBeforeEvaluate','captureClosedAfterCleanup']); true_fields(ins['traceCloses'],['private','public'])
    false_fields(ins,['crossClockOrderingClaimed'])
    require(ins['clock']=='worker-monotonic-receipt' and ins['browserClock']=='browser-performance-independent','Separate clock domains')
    for key in ['droppedEvents','truncatedEvents','observerExceptions','callbackErrors','unexpectedRedirectObservations',
                'unexpectedApplicationRequestObservations','unexpectedRouteRequests']:
        require(type(ins[key]) is int and ins[key]==0,'Complete bounded host observation')
    trace=raw('raw/trace.public.ndjson',2097152)
    require(trace.endswith(b'\n'),'Complete public trace newline')
    lines=trace.splitlines(); require(1<=len(lines)<=2048 and all(0<len(line)<8192 for line in lines),'Bounded public trace records')
    require(type(ins['eventCount']) is int and ins['eventCount']==ins['attemptedEvents']==len(lines)
            and type(ins['eventCap']) is int and ins['eventCap']==2048,'Exact retained trace count')
    kinds={}; previous=-1
    for index,line in enumerate(lines,1):
        event=json_bytes(line,8192)
        require(type(event) is dict and set(event)=={'version','id','sequence','clock','milliseconds','kind','data'},'Trace envelope shape')
        require(type(event['version']) is int and event['version']==1 and type(event['sequence']) is int and event['sequence']==index
                and event['id']=='e'+str(index) and event['clock']=='worker-monotonic-receipt','Contiguous host trace identities')
        require(finite(event['milliseconds'],upper=40000) and event['milliseconds']>=previous
                and type(event['kind']) is str and type(event['data']) is dict,'Host trace time/data shape')
        previous=event['milliseconds']; kinds.setdefault(event['kind'],[]).append(event)
        if event['kind'].startswith(('gpu-host-','persistence-')):
            require(event['data'].get('transferID')=='gpu-readback-1','Sole GPU-readback transfer identity')
        if event['kind'] in ['pw-request','cdp-request']:
            d=event['data']; require(d.get('method')=='GET' and d.get('redirected') is False
                and d.get('resourceType') not in ['fetch','xhr','Fetch','XHR'] and d.get('urlLabel') in ['fixture-html','fixture-script'],
                'Only fixed fixture requests observed')
    def one(kind):
        rows=kinds.get(kind,[]); require(len(rows)==1,'Exactly one '+kind+' event'); return rows[0]
    launch=one('browser-launch-intent'); ready=one('observers-ready'); started=one('gpu-host-evaluate-started'); cleanup=one('cleanup-finished')
    require(launch['sequence']<ready['sequence']<started['sequence']<cleanup['sequence']==len(lines)
            and ready['id']==r['observerReadyEvent'] and cleanup['data'].get('complete') is True,'Observed host boundaries')
    require(not any(kinds.get(k) for k in ['worker-error','observer-callback-error','page-crash','unexpected-route-blocked']), 'No hidden host failure event')
    require(r['trace']['public']=={'bytes':len(trace),'sha256':digest(trace)},'Actual closed public trace receipt')
    private=r['trace']['private']; require(type(private) is dict and set(private)=={'bytes','sha256'}
            and integer(private['bytes'],1,3145728) and type(private['sha256']) is str and len(private['sha256'])==64
            and all(c in '0123456789abcdef' for c in private['sha256']),'Bounded private trace receipt only')
    stdout=raw('results/diagnostic-stdout.txt',4096)
    require(stdout.endswith(b'\n') and len(stdout.splitlines())==1 and raw('results/diagnostic-stderr.txt')==b'','Exact bounded host pipe records')
    summary=document('results/diagnostic-stdout.txt',4096)
    require(summary['kind']=='synthetic-gpu-readback-worker-summary' and summary['status']==r['status']
            and summary['resultBytes']==len(raw('results/result.json',65536)) and summary['resultSHA256']==digest(raw('results/result.json',65536)), 'Host summary binding')
    true_fields(summary,['terminal','externalCompletionRequired','resultWriteClosed']); false_fields(summary,['qualified'])
    require(type(ret['received']) is bool and type(ret['validationPassed']) is bool and type(ret['candidateByPageSelfReport']) is bool,'Return flags')
    byte_events=['gpu-host-envelope-validated','persistence-started','persistence-write','persistence-completed']
    common={'pageEvidenceKind':'page-self-report','gpuExecutionIndependentlyAttested':False,'processClosureIndependentlyReobserved':False,
            'producerEnvelopeInvalidityIndependentlyVerified':False}
    if not ret['received']:
        require(ret['validationPassed'] is False and ret['validationError'] is None and ret['json'] is None and ret['rejectionProjection'] is None
                and all(ret[k] is None for k in ['bytes','sha256','exact','pageStatus']) and ret['pageFailureCodes']==[]
                and ret['candidateByPageSelfReport'] is False,'No invented return data')
        require(type(ev['errorName']) is str and ev['errorName'] and r['pageReport'] is None and r['browserContext'] is None
                and all(value is None for value in timing.values()),'Settled host rejection without page inference')
        rejected=one('gpu-host-evaluate-error')
        require(started['sequence']<rejected['sequence']<cleanup['sequence'] and rejected['data'].get('errorName')==ev['errorName'], 'Evaluate rejection trace')
        require(not any(kinds.get(k) for k in ['gpu-host-evaluate-returned','gpu-host-envelope-rejected','gpu-host-envelope-without-bytes']+byte_events),'No later extraction events')
        require(not (BASE/'raw/returned.json').exists() and not (BASE/'raw/rejected-return.json').exists(),'No return artifact after failed call')
        no_persistence(persistence)
        require(r['status']==r['lastPhase']=='evaluate-rejected','Observed rejection classification')
        FINDING={**common,'hostOutcome':r['status'],'actualByteFacts':None,'pageCandidateBySelfReport':None,'pageAndBytesCandidateOnly':False}
        return
    require(ev['errorName'] is None and finite(timing['hostValidationMilliseconds'],upper=40000),'Returned evaluation metadata')
    returned_event=one('gpu-host-evaluate-returned')
    require(started['sequence']<returned_event['sequence']<cleanup['sequence'] and not kinds.get('gpu-host-evaluate-error'),'Returned call trace')
    if not ret['validationPassed']:
        require(type(ret['validationError']) is str and 1<=len(ret['validationError'])<=120 and ret['json'] is None
                and all(ret[k] is None for k in ['bytes','sha256','exact','pageStatus']) and ret['pageFailureCodes']==[]
                and ret['candidateByPageSelfReport'] is False and r['pageReport'] is None and r['browserContext'] is None,
                'Bounded rejected-envelope metadata')
        projection_bytes=raw('raw/rejected-return.json',32768); closed_write(ret['rejectionProjection'],projection_bytes)
        projection=document('raw/rejected-return.json',32768)
        require(type(projection) is dict and set(projection)=={'kind','errorCode','rootType','rootIsArray','originalRetained'}
                and projection['kind']=='rejected-decoded-return-projection' and projection['errorCode']==ret['validationError']
                and projection['rootType'] in ['null','undefined','object','boolean','number','bigint','string','symbol','function']
                and type(projection['rootIsArray']) is bool and projection['originalRetained'] is False,'Safe original-not-retained projection')
        rejected=one('gpu-host-envelope-rejected')
        require(returned_event['sequence']<rejected['sequence']<cleanup['sequence'] and rejected['data'].get('valid') is False,'Envelope rejection observation')
        require(not (BASE/'raw/returned.json').exists() and not any(kinds.get(k) for k in ['gpu-host-envelope-without-bytes']+byte_events),'No invented valid envelope or bytes')
        no_persistence(persistence)
        require(timing['hostPersistenceMilliseconds'] is None and timing['browserElapsedMilliseconds'] is None
                and r['status']==r['lastPhase']=='envelope-rejected','Complete retained rejection classification')
        FINDING={**common,'hostOutcome':r['status'],'actualByteFacts':None,'pageCandidateBySelfReport':None,'pageAndBytesCandidateOnly':False,
                 'rejectionScope':'Retained projection only; original rejected object was not retained'}
        return
    require(ret['validationError'] is None and ret['rejectionProjection'] is None and not (BASE/'raw/rejected-return.json').exists(),'One validated actual envelope')
    actual_json=raw('raw/returned.json',32768); closed_write(ret['json'],actual_json)
    actual=document('raw/returned.json',32768); page=validate_page_claims(actual)
    require(ret['pageStatus']==page['status'] and ret['pageFailureCodes']==page['failureCodes']
            and ret['candidateByPageSelfReport']==page['candidateByPageSelfReport'],'Actual page outcome projection')
    projection={'phaseEvidenceKind':'page-self-report','browserElapsedMilliseconds':actual['browserElapsedMilliseconds'],
                'lastWorkStage':actual['lastWorkStage'],'counts':actual['counts'],'observation':actual['observation'],'independentPersistenceVerified':False}
    require(strict_equal(r['pageReport'],projection) and strict_equal(r['browserContext'],actual['context'])
            and timing['browserElapsedMilliseconds']==actual['browserElapsedMilliseconds'],'Named page self-report projections')
    if page['values'] is None:
        require(all(ret[k] is None for k in ['bytes','sha256','exact']) and timing['hostPersistenceMilliseconds'] is None,'No page bytes supplied')
        no_persistence(persistence); event=one('gpu-host-envelope-without-bytes')
        require(returned_event['sequence']<event['sequence']<cleanup['sequence'] and event['data'].get('valid') is True
                and not any(kinds.get(k) for k in ['gpu-host-envelope-rejected']+byte_events),'Validated no-byte page report trace')
        require(r['status']==r['lastPhase']=='page-failed-without-bytes','No-byte page failure classification')
        FINDING={**common,'hostOutcome':r['status'],'actualByteFacts':None,'pageCandidateBySelfReport':False,'pageAndBytesCandidateOnly':False}
        return
    actual_values=decode_byte_values(page['values']); actual_file=raw('raw/received.bin',128)
    facts=compare_byte_evidence(page['values'],actual_file)
    require(facts['returned_equals_persisted'],'Persisted actual file must equal retained actual returned values')
    require(type(ret['bytes']) is int and ret['bytes']==128 and ret['sha256']==digest(actual_values)
            and type(ret['exact']) is bool and ret['exact']==facts['returned_equals_expected'],'Independently reconstructed return receipt')
    closed_write(persistence,actual_file); true_fields(persistence,['exists','equalsReturned'])
    require(type(persistence['exact']) is bool and persistence['exact']==facts['persisted_equals_expected']
            and finite(timing['hostPersistenceMilliseconds'],upper=40000),'Independent exact-file result')
    validated=one('gpu-host-envelope-validated'); first=one('persistence-started'); last=one('persistence-completed')
    require(returned_event['sequence']<validated['sequence']<first['sequence']<last['sequence']<cleanup['sequence']
            and not kinds.get('gpu-host-envelope-rejected') and not kinds.get('gpu-host-envelope-without-bytes'),'Byte persistence phase ordering')
    vd=validated['data']; require(vd.get('valid') is True and vd.get('jsonBytes')==len(actual_json) and vd.get('bytes')==128
            and vd.get('sha256')==digest(actual_values) and type(vd.get('exact')) is bool and vd['exact']==facts['returned_equals_expected'],'Validated byte trace projection')
    require(first['data'].get('bytes')==128 and first['data'].get('sha256')==digest(actual_values)
            and last['data'].get('complete') is True and last['data'].get('bytes')==128 and last['data'].get('sha256')==digest(actual_values),'Persistence trace projection')
    writes=kinds.get('persistence-write',[]); require(len(writes)==persistence['writeCalls'],'Actual write-event count')
    at=0
    for number,event in enumerate(writes,1):
        d=event['data']; require(first['sequence']<event['sequence']<last['sequence'] and type(d.get('writeCalls')) is int and d['writeCalls']==number
                and type(d.get('writtenBytes')) is int and at<d['writtenBytes']<=128,'Cumulative actual byte writes'); at=d['writtenBytes']
    require(at==128 and r['lastPhase']=='persistence-returned','Complete persisted actual byte range')
    outcome='page-failed-with-bytes' if page['status']=='failed' else ('candidate-byte-transfer-recorded' if facts['all_bytes_match'] else 'valid-byte-mismatch')
    require(r['status']==outcome,'Independent separation of page outcome and byte outcome')
    FINDING={**common,'hostOutcome':outcome,'actualByteFacts':facts,'pageCandidateBySelfReport':page['candidateByPageSelfReport'],
             'pageAndBytesCandidateOnly':page['candidateByPageSelfReport'] and facts['all_bytes_match']}


def main():
    global BASE, REPO, ADMISSION, WORK_END
    start=time.monotonic()
    def hard_stop(signum,frame):
        os._exit(124)
    # No runtime artifact, lock, result directory or subprocess before this gate.
    try:
        require(len(sys.argv)==2 and Path(sys.argv[1]).is_absolute(),'One absolute future campaign directory')
        BASE=Path(sys.argv[1]).resolve(); REPO=BASE.parents[1]
        config_bytes=read_bounded(BASE,'config.json',16384)
        config=json_bytes(config_bytes,16384)
        ADMISSION=admit_review(config,datetime.datetime.now(datetime.timezone.utc))
        CACHE['config.json']=config_bytes; DOC['config.json']=config
    except Exception:
        message=b'{"kind":"gpu-saved-review-admission-refused","runtimeArtifactsTouched":false,"reviewReserved":false}\n'
        os.write(sys.stdout.fileno(),message)
        return 2
    # Allocation/window admission precedes even reviewer alarm setup.
    signal.signal(signal.SIGALRM,hard_stop)
    signal.setitimer(signal.ITIMER_REAL,max(.001,start+30-time.monotonic()))
    WORK_END=start+25
    output=None
    try:
        with (BASE/'review.lock').open('xb') as handle:
            require(handle.write(LOCK)==len(LOCK),'Complete exclusive review reservation')
        candidate_output=BASE/'review/results'; candidate_output.mkdir(exist_ok=False)
        output=candidate_output
        for name,action in [('frozen_source_and_allocation',source_identity),('final_public_manifest',public_manifest),
                            ('actual_bytes_and_reported_page_phases',actual_return_and_trace),
                            ('external_lifecycle_projections',lifecycle),('resource_and_output_accounting',accounting)]:
            group(name,action)
    except Exception as error:
        ERRORS.append({'group':'reservation','type':type(error).__name__,'reason':'Exclusive reservation or fresh output failed'})
    passed=len(GROUPS)==5 and all(row['pass'] for row in GROUPS) and not ERRORS
    report={'kind':'saved-gpu-readback-public-evidence-review','terminal':True,'active':False,
            'recordIntegrityCandidate':passed,'recordIntegrityVerified':False,'qualified':False,
            'requiresExternalReviewExit0AndCompleteFinalSummary':True,'finding':FINDING,
            'gpuExecutionIndependentlyAttested':False,'processClosureIndependentlyReobserved':False,
            'groups':GROUPS,'errors':ERRORS,'wallSecondsBeforeFinalRecords':time.monotonic()-start,
            'wallCapSeconds':30,'workStopSeconds':25,'finalStopSeconds':29,'retryPermitted':False,
            'reviewArtifactBytes':None,'accountedDiagnosticAndLaterPublicReviewBytes':None,
            'scope':'Independent saved public byte/record comparison; page phases and historical process closure remain recorded observations, not independently reobserved GPU or process events.',
            'accountingScope':'Diagnostic receipt plus later publication copies/manifest and review lock/report/summary plus one stdout summary copy. External review recorder must separately add its later completion receipt.'}
    try:
        require(output is not None and time.monotonic()<start+29,'Review finalization admission/deadline')
        prefix=None
        if any(row['group']=='resource_and_output_accounting' and row['pass'] for row in GROUPS):
            manifest=DOC['review/evidence-manifest.json']
            prefix=DOC['results/capture.json']['accountedCombinedResultBytes']+len(CACHE['review/evidence-manifest.json'])
            prefix+=sum(len(CACHE[pin['path']]) for pin in manifest['files'] if pin['path'].startswith('publication/'))
        for _ in range(12):
            encoded=(json.dumps(report,sort_keys=True)+'\n').encode()
            summary={'kind':'saved-gpu-readback-review-summary','reportBytes':len(encoded),'reportSHA256':digest(encoded),
                     'recordIntegrityCandidate':passed,'recordIntegrityVerified':False,'qualified':False,
                     'requiresExternalReviewExit0AndCompleteFinalSummary':True,
                     'hostOutcome':FINDING['hostOutcome'] if FINDING else None,
                     'actualBytesMatch':FINDING['actualByteFacts']['all_bytes_match'] if FINDING and FINDING['actualByteFacts'] else None,
                     'pageCandidateBySelfReport':FINDING['pageCandidateBySelfReport'] if FINDING else None,
                     'gpuExecutionIndependentlyAttested':False,'groupsPassed':sum(row['pass'] for row in GROUPS),
                     'groupsTotal':len(GROUPS),'errors':len(ERRORS),
                     'accountedDiagnosticAndLaterPublicReviewBytes':report['accountedDiagnosticAndLaterPublicReviewBytes']}
            summary_bytes=(json.dumps(summary,sort_keys=True)+'\n').encode()
            own=len(LOCK)+len(encoded)+len(summary_bytes)
            total=prefix+own+len(summary_bytes) if prefix is not None else None
            if report['reviewArtifactBytes']==own and report['accountedDiagnosticAndLaterPublicReviewBytes']==total:
                break
            report.update(reviewArtifactBytes=own,accountedDiagnosticAndLaterPublicReviewBytes=total)
        else:
            raise ValueError('Review accounting fixed point')
        require(time.monotonic()<start+29 and len(encoded)<=65536 and len(summary_bytes)<=4096 and (total is None or total<=CAP),'Bounded review outputs and final deadline')
        with (output/'report.json').open('xb') as handle:
            require(time.monotonic()<start+29,'Review report write deadline')
            require(handle.write(encoded)==len(encoded),'Complete review report')
        require(time.monotonic()<start+29,'Review summary create deadline')
        with (output/'summary.json').open('xb') as handle:
            require(time.monotonic()<start+29,'Review summary write deadline')
            require(handle.write(summary_bytes)==len(summary_bytes),'Complete review summary')
        require(time.monotonic()<start+29,'Review stdout deadline')
        require(os.write(sys.stdout.fileno(),summary_bytes)==len(summary_bytes),'Complete review stdout')
    except Exception:
        return 125
    return 0 if passed else 1


if __name__=='__main__':
    raise SystemExit(main())
