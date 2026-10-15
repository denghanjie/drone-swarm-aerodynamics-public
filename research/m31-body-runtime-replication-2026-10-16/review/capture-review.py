"""Sole fixed entry: observe one saved-review observer's actual exit/full interval."""
import time
START = time.monotonic()
import os, signal

CHILD = None
def hard_deadline(signum, frame):
    if CHILD is not None and CHILD.returncode is None:
        try:
            CHILD.kill()
        except OSError:
            pass
    os._exit(124)
signal.signal(signal.SIGALRM, hard_deadline)
signal.setitimer(signal.ITIMER_REAL, max(.001, START + 120 - time.monotonic()))

import sys, json, hashlib, stat, selectors, subprocess, tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
STOP, REAP_END = START + 119.5, START + 119.75
CAP, PIPE_CAP = 33554432, 16384
SOURCE = 'f12d8c836e7b991ec33e6de662d00ed05dcce33e'
FREEZE = 'c0c6b2fda84567a76025b2e5f06832cbc1dd5811c23a246df5623f46baf8f8a9'
REVIEW_FILES = ['review/IMPLEMENTATION.md', 'review/STATIC-CHALLENGE.md',
                'review/observe-review.py', 'review/source/check-records.py',
                'review/capture-review.py', 'review/preparation/seal-review.py']
LOCK = b'One saved review capture reserved. Permanent; no retry.\n'
selector = None
handles = {}
private = None
reserved = False
launch_start = None
observer_end = None
report = {'kind': 'actual-saved-review-observer-completion', 'sourceCommit': SOURCE,
          'sourceFreezeSHA256': FREEZE, 'observerInvocations': 0, 'actualObserverExitCode': None,
          'observerReaped': False, 'observerFullElapsedSeconds': None,
          'observerPipeCaptureComplete': False, 'observerSummaryValidated': False,
          'stdoutBytesObserved': 0, 'stderrBytesObserved': 0, 'stdoutBytesRetained': 0, 'stderrBytesRetained': 0,
          'pipeByteCapCombined': PIPE_CAP, 'captureStopSeconds': 119.5,
          'captureReapStopSeconds': 119.75, 'captureHardSeconds': 120,
          'directObserverKillRequested': False, 'checkerCleanupInferredFromCallerKill': False,
          'candidateIntegrityVerified': False, 'integrityVerified': False, 'decisionVerified': False,
          'qualified': False, 'outputAccountingComplete': False,
          'requiresActualCaptureExit0AndCompleteFinalSummary': True, 'retryPermitted': False, 'errors': []}

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def problem(error, phase):
    if len(report['errors']) < 16:
        report['errors'].append({'phase': phase, 'type': type(error).__name__,
                                'reason': str(error) if type(error) is RuntimeError else 'Capture operation failed'})

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_path(target, cap=1048576):
    require(stat.S_ISREG(target.lstat().st_mode) and target.stat().st_size <= cap, 'Bounded regular capture input')
    with target.open('rb') as handle:
        data = handle.read(cap + 1)
    require(len(data) <= cap, 'Capture input growth cap')
    return data

def read(relative, cap=1048576):
    p = Path(relative)
    require(not p.is_absolute() and all(x not in ['', '.', '..'] for x in relative.split('/')), 'Contained capture input')
    target = BASE / p
    require(target.resolve() == target, 'No input symlink traversal')
    return read_path(target, cap)

def check_pin(pin):
    require(set(pin) == {'path', 'bytes', 'sha256'} and type(pin['bytes']) is int
            and 0 <= pin['bytes'] <= 1048576, 'Review pin schema')
    data = read(pin['path'])
    require(len(data) == pin['bytes'] and digest(data) == pin['sha256'], 'Frozen review source bytes')

def drain(timeout):
    if selector is None:
        return
    for key, _ in selector.select(timeout):
        remaining = PIPE_CAP - report['stdoutBytesRetained'] - report['stderrBytesRetained']
        try:
            chunk = os.read(key.fileobj.fileno(), min(4096, remaining + 1))
        except BlockingIOError:
            continue
        if not chunk:
            selector.unregister(key.fileobj)
            continue
        name = key.data
        report[name + 'BytesObserved'] += len(chunk)
        retained = chunk[:remaining]
        written = handles[name].write(retained)
        report[name + 'BytesRetained'] += written
        require(written == len(retained), 'Complete review observer capture write')
        require(len(retained) == len(chunk), 'Review observer combined pipe cap')
    report['observerPipeCaptureComplete'] = not selector.get_map()

def reap(timeout):
    global observer_end
    try:
        CHILD.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        return
    if observer_end is None:
        observer_end = time.monotonic()
    report.update(observerReaped=True, actualObserverExitCode=CHILD.returncode,
                  observerFullElapsedSeconds=observer_end - launch_start)

try:
    require(len(sys.argv) == 1, 'Fixed capture entry accepts no arguments')
    with (BASE / 'review/capture-review.lock').open('xb') as handle:
        require(handle.write(LOCK) == len(LOCK), 'Complete permanent review capture lock')
    reserved = True
    rb = read('review/review-freeze.json')
    require(digest(rb) == os.environ.get('RESEARCH_REVIEW_FREEZE_SHA256'), 'External review freeze authority')
    rf = json.loads(rb)
    require(rf['kind'] == 'frozen-saved-failure-record-review' and rf['sourceCommit'] == SOURCE
            and rf['sourceFreezeSHA256'] == FREEZE and rf['invocations'] == 1
            and rf['wallSeconds'] == 120 and rf['outputByteCap'] == CAP, 'Review freeze identity')
    require(sorted(p['path'] for p in rf['files']) == sorted(REVIEW_FILES), 'All six review source pins')
    for pin in rf['files']:
        check_pin(pin)
    require(rf['scienceManifest']['path'] == 'review/science-manifest.json', 'Review manifest path')
    check_pin(rf['scienceManifest'])
    report['reviewFreezeSHA256'] = digest(rb)
    private = Path(tempfile.mkdtemp(prefix='m31-runtime-saved-review-capture-'))
    handles = {name: (private / ('observer-' + name + '.bin')).open('xb', buffering=0)
               for name in ['stdout', 'stderr']}
    env = os.environ.copy()
    env['M31_SAVED_REVIEW_CAPTURE_PID'] = str(os.getpid())
    require(time.monotonic() < STOP, 'Capture launch reserve')
    launch_start = time.monotonic()  # Before Popen and observer interpreter startup.
    CHILD = subprocess.Popen([sys.executable, str(BASE / 'review/observe-review.py')],
                             cwd=BASE, env=env, start_new_session=False,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    report['observerInvocations'] = 1
    selector = selectors.DefaultSelector()
    for name, stream in [('stdout', CHILD.stdout), ('stderr', CHILD.stderr)]:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
    while time.monotonic() < STOP:
        drain(min(.01, max(0, STOP - time.monotonic())))
        reap(0)
        if report['observerReaped'] and report['observerPipeCaptureComplete']:
            break
    else:
        raise TimeoutError('Conservative whole review deadline')
except BaseException as error:
    problem(error, 'capture')
finally:
    if CHILD is not None:
        if CHILD.returncode is None:
            try:
                report['directObserverKillRequested'] = True
                CHILD.kill()
            except BaseException as error:
                problem(error, 'capture-observer-stop')
        while time.monotonic() < REAP_END:
            try:
                reap(min(.01, max(0, REAP_END - time.monotonic())))
            except BaseException as error:
                problem(error, 'capture-observer-reap')
            try:
                drain(0)
            except BaseException as error:
                problem(error, 'capture-final-drain')
            if report['observerReaped'] and report['observerPipeCaptureComplete']:
                break
            time.sleep(min(.005, max(0, REAP_END - time.monotonic())))
        for stream in [CHILD.stdout, CHILD.stderr]:
            if stream is not None:
                stream.close()
    if selector is not None:
        selector.close()
    for handle in handles.values():
        handle.close()

inner_total = None
try:
    require(time.monotonic() < REAP_END, 'Capture final evidence reserve')
    require(report['observerReaped'] and report['observerPipeCaptureComplete'], 'Actual review observer closure')
    stdout = read_path(private / 'observer-stdout.bin', PIPE_CAP)
    stderr = read_path(private / 'observer-stderr.bin', PIPE_CAP)
    require(len(stdout) == report['stdoutBytesObserved'] == report['stdoutBytesRetained']
            and len(stderr) == report['stderrBytesObserved'] == report['stderrBytesRetained'], 'Exact observer captures')
    require(stdout.endswith(b'\n') and len(stdout.splitlines()) == 1, 'Complete observer summary')
    inner = json.loads(stdout)
    budget_bytes = read('review/results/budget.json', 16384)
    budget = json.loads(budget_bytes)
    require(inner['kind'] == 'caller-retained-saved-review-summary' and inner['budgetSHA256'] == digest(budget_bytes)
            and inner['budgetBytes'] == len(budget_bytes) and inner['summaryBytes'] == len(stdout)
            and budget['observerSummaryBytes'] == len(stdout), 'Observer budget summary binding')
    for item in [inner, budget]:
        require(item['sourceCommit'] == SOURCE and item['sourceFreezeSHA256'] == FREEZE
                and item['reviewFreezeSHA256'] == digest(rb) and item['integrityVerified'] is False
                and item['decisionVerified'] is False and item['qualified'] is False, 'Review identity and restricted claims')
    require(inner['outputAccountingComplete'] is True and budget['outputAccountingComplete'] is True, 'Complete observer output account')
    candidate_total = inner['accountedTotalOutputBytes']
    require(type(candidate_total) is int and 0 <= candidate_total <= CAP
            and budget['accountedTotalOutputBytes'] == candidate_total, 'Exact observer output total')
    inner_total = candidate_total
    require(read('review/review-freeze.json') == rb, 'Review freeze remains stable')
    for pin in rf['files']:
        check_pin(pin)
    check_pin(rf['scienceManifest'])
    report.update(observerSummaryValidated=True, observerSummarySHA256=digest(stdout),
                  observerBudgetSHA256=digest(budget_bytes), observedInnerAccountedOutputBytes=inner_total)
    require(report['observerInvocations'] == 1 and report['actualObserverExitCode'] == 0
            and report['observerFullElapsedSeconds'] < 120 and not report['directObserverKillRequested']
            and inner['observedIntegrityCandidateVerified'] is True and budget['observedIntegrityCandidateVerified'] is True
            and budget['checkerChildConfirmedReaped'] is True and budget['checkerExitCode'] == 0
            and budget['checkerPipeCaptureComplete'] is True and budget['checkerKillRequested'] is False
            and budget['errors'] == [] and not stderr and not report['errors'], 'Actual full review integrity conjunction')
    report['candidateIntegrityVerified'] = True
except BaseException as error:
    problem(error, 'validate-review-observer')

report.update(terminal=True, active=False, captureLockBytes=len(LOCK) if reserved else 0,
              privateCaptureBytes=report['stdoutBytesRetained'] + report['stderrBytesRetained'],
              wallSecondsBeforeFinalRecords=time.monotonic() - START,
              outputAccountingComplete=inner_total is not None and report['observerPipeCaptureComplete'],
              scope='Before fixed observer Popen through actual wait/reap, including observer startup and final exit. Killing the observer does not prove checker closure.',
              deadlineScope='Shared120-second allowance: capture119.5/119.75/120, observer117/119/120, checker cooperative110. No second review allocation.',
              accountingScope='Observer total already includes its summary retained here once. Add capture lock, observer stderr, capture receipt and final capture summary. Missing inner total remains null.',
              receiptBytes=0, captureSummaryBytes=0, accountedCombinedOutputBytes=None)
report['candidateIntegrityVerified'] = report['candidateIntegrityVerified'] and not report['errors']
for _ in range(24):
    receipt = (json.dumps(report, sort_keys=True) + '\n').encode()
    summary = {'kind': 'caller-retained-review-capture-summary', 'sourceCommit': SOURCE,
               'sourceFreezeSHA256': FREEZE, 'reviewFreezeSHA256': report.get('reviewFreezeSHA256'),
               'captureReceiptSHA256': digest(receipt), 'captureReceiptBytes': len(receipt),
               'summaryBytes': report['captureSummaryBytes'], 'candidateIntegrityVerified': report['candidateIntegrityVerified'],
               'integrityVerified': False, 'decisionVerified': False, 'qualified': False,
               'requiresActualCaptureExit0AndCompleteFinalSummary': True,
               'actualObserverExitCode': report['actualObserverExitCode'],
               'observerFullElapsedSeconds': report['observerFullElapsedSeconds'],
               'outputAccountingComplete': report['outputAccountingComplete'],
               'accountedCombinedOutputBytes': report['accountedCombinedOutputBytes']}
    summary_bytes = (json.dumps(summary, sort_keys=True) + '\n').encode()
    total = inner_total + report['captureLockBytes'] + report['stderrBytesRetained'] + len(receipt) + len(summary_bytes) \
        if report['outputAccountingComplete'] else None
    if report['receiptBytes'] == len(receipt) and report['captureSummaryBytes'] == len(summary_bytes) \
            and report['accountedCombinedOutputBytes'] == total:
        break
    report.update(receiptBytes=len(receipt), captureSummaryBytes=len(summary_bytes), accountedCombinedOutputBytes=total)
else:
    os._exit(125)
if len(receipt) > 8192 or len(summary_bytes) > 4096 or (total is not None and total > CAP):
    os._exit(125)
if reserved:
    target = BASE / 'review/results'
    target.mkdir(exist_ok=True)
    require(target.is_dir() and not target.is_symlink(), 'Regular capture receipt directory')
    with (target / 'capture.json').open('xb') as handle:
        require(handle.write(receipt) == len(receipt), 'Complete review capture receipt')
if os.write(sys.stdout.fileno(), summary_bytes) != len(summary_bytes):
    os._exit(125)
raise SystemExit(0 if report['candidateIntegrityVerified'] else 1)
