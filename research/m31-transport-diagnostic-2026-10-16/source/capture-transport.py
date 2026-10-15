"""One bounded caller recorder; runs only the fixed campaign observer once."""
import time
START = time.monotonic()
import os, signal

CHILD = None
def hard_deadline(signum, frame):
    if CHILD is not None and CHILD.returncode is None:
        try:
            CHILD.kill()  # Direct child only; never claim descendant closure.
        except OSError:
            pass
    os._exit(124)
signal.signal(signal.SIGALRM, hard_deadline)
signal.setitimer(signal.ITIMER_REAL, max(.001, START + 60 - time.monotonic()))

import sys, json, hashlib, selectors, subprocess, tempfile, stat
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
STOP, REAP_END = START + 59.5, START + 59.75
RESULT_CAP, PIPE_CAP = 8388608, 16384
LOCK_BYTES = b'One external transport capture reserved. Permanent; no retry.\n'
selector = None
handles = {}
private = None
reserved = False
launch_start = None
observer_end = None
report = {'kind': 'external-transport-lifecycle-observation', 'observerInvocations': 0,
          'actualObserverExitCode': None, 'observerReaped': False,
          'observerFullElapsedSeconds': None, 'observerPipeCaptureComplete': False,
          'stdoutBytesObserved': 0, 'stderrBytesObserved': 0,
          'stdoutBytesRetained': 0, 'stderrBytesRetained': 0,
          'observerPipeByteCapCombined': PIPE_CAP,
          'callerStopSeconds': 59.5, 'callerReapStopSeconds': 59.75,
          'callerHardSeconds': 60, 'directObserverKillSent': False,
          'descendantCleanupInferredFromCallerKill': False,
          'observerSummaryValidated': False, 'outputAccountingComplete': False,
          'candidateWholeLifecycleVerified': False, 'wholeLifecycleVerified': False,
          'qualified': False, 'requiresActualCaptureExit0AndCompleteFinalSummary': True,
          'retryPermitted': False, 'errors': []}

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def problem(error, phase):
    if len(report['errors']) < 16:
        report['errors'].append({'phase': phase, 'type': type(error).__name__,
                                'reason': str(error) if type(error) is RuntimeError else 'Operation failed'})

def read_file(path, cap):
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_size <= cap, 'Bounded regular capture evidence')
    with path.open('rb') as handle:
        data = handle.read(cap + 1)
    require(len(data) <= cap, 'Capture evidence growth cap')
    return data

def drain(timeout):
    if selector is None:
        return
    for key, _ in selector.select(timeout):
        try:
            chunk = os.read(key.fileobj.fileno(), 4096)
        except BlockingIOError:
            continue
        if not chunk:
            selector.unregister(key.fileobj)
            continue
        name = key.data
        report[name + 'BytesObserved'] += len(chunk)
        remaining = PIPE_CAP - report['stdoutBytesRetained'] - report['stderrBytesRetained']
        retained = chunk[:max(0, remaining)]
        written = handles[name].write(retained)
        report[name + 'BytesRetained'] += written
        require(written == len(retained), 'Complete observer capture write')
        require(len(retained) == len(chunk), 'Observer combined pipe byte cap')
    report['observerPipeCaptureComplete'] = not selector.get_map()

def reap(timeout):
    global observer_end
    try:
        CHILD.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        return
    if observer_end is None:
        observer_end = time.monotonic()  # Taken only after an actual wait/reap.
    report.update(observerReaped=True, actualObserverExitCode=CHILD.returncode,
                  observerFullElapsedSeconds=observer_end - launch_start)

try:
    require(len(sys.argv) == 2 and Path(sys.argv[1]).is_absolute(), 'One absolute pinned Node executable')
    # Outside results so the observer can still demand a fresh results directory.
    with (BASE / 'capture-launch.lock').open('xb') as handle:
        require(handle.write(LOCK_BYTES) == len(LOCK_BYTES), 'Complete permanent capture lock')
    reserved = True
    private = Path(tempfile.mkdtemp(prefix='m31-transport-capture-'))
    handles = {name: (private / ('observer-' + name + '.bin')).open('xb', buffering=0)
               for name in ['stdout', 'stderr']}
    env = os.environ.copy()
    env['RESEARCH_CAPTURE_PID'] = str(os.getpid())
    require(time.monotonic() < STOP, 'Caller launch reserve')
    launch_start = time.monotonic()  # Includes Popen and interpreter startup.
    CHILD = subprocess.Popen([sys.executable, str(BASE / 'source/observe-transport.py'), sys.argv[1]],
                             cwd=REPO, env=env, start_new_session=True,
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
        raise TimeoutError('Conservative caller deadline')
except BaseException as error:
    problem(error, 'capture')
finally:
    if CHILD is not None:
        if CHILD.returncode is None:
            try:
                CHILD.kill()
                report['directObserverKillSent'] = True
            except BaseException as error:
                problem(error, 'direct-observer-kill')
        while time.monotonic() < REAP_END:
            try:
                reap(min(.01, max(0, REAP_END - time.monotonic())))
            except BaseException as error:
                problem(error, 'direct-observer-reap')
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
    require(time.monotonic() < REAP_END, 'Caller final evidence reserve')
    require(report['observerReaped'] and report['observerPipeCaptureComplete'], 'Complete actual observer exit and pipes')
    stdout = read_file(private / 'observer-stdout.bin', PIPE_CAP)
    stderr = read_file(private / 'observer-stderr.bin', PIPE_CAP)
    require(len(stdout) == report['stdoutBytesObserved'] == report['stdoutBytesRetained']
            and len(stderr) == report['stderrBytesObserved'] == report['stderrBytesRetained'], 'Exact retained observer bytes')
    require(stdout.endswith(b'\n') and len(stdout.splitlines()) == 1, 'One complete observer summary')
    inner = json.loads(stdout)
    budget_bytes = read_file(BASE / 'results/budget.json', 32768)
    budget = json.loads(budget_bytes)
    require(inner.get('kind') == 'caller-retained-transport-observer-summary'
            and inner.get('budgetSHA256') == hashlib.sha256(budget_bytes).hexdigest()
            and inner.get('budgetBytes') == len(budget_bytes)
            and inner.get('summaryBytes') == len(stdout)
            and budget.get('observerSummaryBytes') == len(stdout), 'Exact observer summary/budget binding')
    require(inner.get('sourceCommit') == os.environ.get('RESEARCH_SOURCE_COMMIT')
            and inner.get('sourceFreezeSHA256') == os.environ.get('RESEARCH_REMOTE_VERIFIED_FREEZE'), 'Caller source identity')
    require(inner.get('outputAccountingComplete') is True and budget.get('outputAccountingComplete') is True,
            'Complete inner output accounting')
    candidate_total = inner.get('accountedTotalResultBytes')
    require(type(candidate_total) is int and 0 <= candidate_total <= RESULT_CAP
            and budget.get('accountedTotalResultBytes') == candidate_total, 'Exact inner total bytes')
    inner_total = candidate_total
    report.update(observerSummaryValidated=True, observerSummarySHA256=hashlib.sha256(stdout).hexdigest(),
                  observerBudgetSHA256=hashlib.sha256(budget_bytes).hexdigest(),
                  sourceCommit=inner['sourceCommit'], sourceFreezeSHA256=inner['sourceFreezeSHA256'],
                  observedInnerAccountedResultBytes=inner_total)
    require(report['observerInvocations'] == 1 and report['actualObserverExitCode'] == 0
            and report['observerFullElapsedSeconds'] < 60 and not report['directObserverKillSent']
            and inner.get('candidateLifecycleVerified') is True
            and budget.get('candidateLifecycleVerified') is True
            and not inner.get('errors') and not budget.get('errors') and not stderr
            and not report['errors'], 'Observed whole lifecycle candidate conjunction')
    report['candidateWholeLifecycleVerified'] = True
except BaseException as error:
    problem(error, 'validate-observer')

# Caller stdout is the observer summary already counted by the inner receipt;
# its private persistence is counted once. Caller stderr/lock/receipt/summary add.
capture_bytes = report['stdoutBytesRetained'] + report['stderrBytesRetained']
report.update(terminal=True, active=False, privateCaptureBytes=capture_bytes,
              captureLockBytes=len(LOCK_BYTES) if reserved else 0,
              wallSecondsBeforeFinalRecords=time.monotonic() - START,
              scope='Actual fixed observer process from before Popen through actual reap; observer evidence supplies descendant closure. Caller kill never proves descendant cleanup. Sampled RSS includes the direct caller in observer samples.',
              deadlineScope='Caller stops at59.5/reaps through59.75/hard-exits60, a conservative restriction within the same allowance. Observer40/58/60 and worker40 remain unchanged.',
              accountingScope='Observer accounted total already includes its summary retained here once. Add caller stderr, permanent lock, public capture receipt, and final caller stdout summary. Missing inner final totals remain null.',
              receiptBytes=0, callerSummaryBytes=0, accountedCombinedResultBytes=None,
              observedCallerArtifactBytes=0)
report['outputAccountingComplete'] = inner_total is not None and report['observerPipeCaptureComplete']
report['candidateWholeLifecycleVerified'] = report['candidateWholeLifecycleVerified'] and not report['errors']
for _ in range(24):
    receipt = (json.dumps(report, sort_keys=True) + '\n').encode()
    summary = {'kind': 'external-transport-capture-summary',
               'captureReceiptSHA256': hashlib.sha256(receipt).hexdigest(),
               'captureReceiptBytes': len(receipt), 'summaryBytes': report['callerSummaryBytes'],
               'candidateWholeLifecycleVerified': report['candidateWholeLifecycleVerified'],
               'wholeLifecycleVerified': False, 'qualified': False,
               'requiresActualCaptureExit0AndCompleteFinalSummary': True,
               'actualObserverExitCode': report['actualObserverExitCode'],
               'observerFullElapsedSeconds': report['observerFullElapsedSeconds'],
               'outputAccountingComplete': report['outputAccountingComplete'],
               'accountedCombinedResultBytes': report['accountedCombinedResultBytes']}
    summary_bytes = (json.dumps(summary, sort_keys=True) + '\n').encode()
    additional = report['captureLockBytes'] + report['stderrBytesRetained'] + len(receipt) + len(summary_bytes)
    total = inner_total + additional if report['outputAccountingComplete'] else None
    observed_caller = capture_bytes + report['captureLockBytes'] + len(receipt) + len(summary_bytes)
    if report['receiptBytes'] == len(receipt) and report['callerSummaryBytes'] == len(summary_bytes) \
            and report['accountedCombinedResultBytes'] == total and report['observedCallerArtifactBytes'] == observed_caller:
        break
    report.update(receiptBytes=len(receipt), callerSummaryBytes=len(summary_bytes),
                  accountedCombinedResultBytes=total, observedCallerArtifactBytes=observed_caller)
else:
    os._exit(125)
if len(receipt) > 16384 or len(summary_bytes) > 4096 or (total is not None and total > RESULT_CAP):
    os._exit(125)
if reserved:
    (BASE / 'results').mkdir(exist_ok=True)
    require((BASE / 'results').is_dir() and not (BASE / 'results').is_symlink(), 'Regular final results directory')
    with (BASE / 'results/capture.json').open('xb') as handle:
        require(handle.write(receipt) == len(receipt), 'Complete public capture receipt')
if os.write(sys.stdout.fileno(), summary_bytes) != len(summary_bytes):
    os._exit(125)
raise SystemExit(0 if report['candidateWholeLifecycleVerified'] else 1)
