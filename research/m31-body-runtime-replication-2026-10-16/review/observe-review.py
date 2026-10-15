"""One 120-second saved-record review. The fixed checker has no subprocess path."""
import time
START = time.monotonic()
import os, signal

CHILD = None
def hard_deadline(signum, frame):
    if CHILD is not None and CHILD.returncode is None:
        try:
            CHILD.kill()  # Exact direct child only; no process-group signals.
        except OSError:
            pass
    os._exit(124)
signal.signal(signal.SIGALRM, hard_deadline)
signal.setitimer(signal.ITIMER_REAL, max(.001, START + 120 - time.monotonic()))

import sys, json, hashlib, stat, subprocess, selectors
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'review/results'
WORK_END, CLEANUP_END = START + 117, START + 119
CAP, RESERVE, PIPE_CAP = 33554432, 65536, 8192
SOURCE = 'f12d8c836e7b991ec33e6de662d00ed05dcce33e'
FREEZE = 'c0c6b2fda84567a76025b2e5f06832cbc1dd5811c23a246df5623f46baf8f8a9'
REVIEW_FILES = ['review/IMPLEMENTATION.md', 'review/STATIC-CHALLENGE.md',
                'review/observe-review.py', 'review/source/check-records.py',
                'review/capture-review.py', 'review/preparation/seal-review.py']
LOCK = b'One saved failed-record review reserved. Permanent; no retry.\n'
selector = None
handles = {}
reserved = False
launch_start = None
child_end = None
report = {'kind': 'saved-failure-review-lifecycle-observation', 'sourceCommit': SOURCE,
          'sourceFreezeSHA256': FREEZE, 'wallCapSeconds': 120,
          'workStopSeconds': 117, 'cleanupStopSeconds': 119, 'outputByteCap': CAP,
          'finalProvenanceReserveBytes': RESERVE, 'checkerInvocations': 0,
          'checkerExitCode': None, 'checkerChildConfirmedReaped': False,
          'checkerFullElapsedSeconds': None, 'checkerPipeCaptureComplete': False,
          'checkerKillRequested': False, 'stdoutBytesObserved': 0, 'stderrBytesObserved': 0,
          'stdoutBytesRetained': 0, 'stderrBytesRetained': 0, 'pipeByteCapCombined': PIPE_CAP,
          'outputAccountingComplete': False, 'observedIntegrityCandidateVerified': False,
          'integrityVerified': False, 'decisionVerified': False, 'qualified': False,
          'requiresCallerObservedObserverExit0AndCompleteSummary': True,
          'retryPermitted': False, 'errors': []}

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def problem(error, phase):
    if len(report['errors']) < 16:
        report['errors'].append({'phase': phase, 'type': type(error).__name__,
                                'reason': str(error) if type(error) is RuntimeError else 'Review operation failed'})

def soft_deadline(signum, frame):
    report['deadlineReached'] = True
    signal.signal(signal.SIGALRM, hard_deadline)
    signal.setitimer(signal.ITIMER_REAL, max(.001, START + 120 - time.monotonic()))
    raise TimeoutError('Review work deadline')

signal.signal(signal.SIGALRM, soft_deadline)
signal.setitimer(signal.ITIMER_REAL, max(.001, WORK_END - time.monotonic()))

def read(relative, cap=1048576):
    p = Path(relative)
    require(not p.is_absolute() and all(x not in ['', '.', '..'] for x in relative.split('/')), 'Contained evidence path')
    target = BASE / p
    require(target.resolve() == target and stat.S_ISREG(target.lstat().st_mode)
            and target.stat().st_size <= cap, 'Bounded regular evidence')
    with target.open('rb') as handle:
        data = handle.read(cap + 1)
    require(len(data) <= cap, 'Evidence growth cap')
    return data

def digest(data):
    return hashlib.sha256(data).hexdigest()

def check_pin(pin):
    require(set(pin) == {'path', 'bytes', 'sha256'} and type(pin['bytes']) is int
            and 0 <= pin['bytes'] <= 1048576, 'Review pin schema')
    data = read(pin['path'])
    require(len(data) == pin['bytes'] and digest(data) == pin['sha256'], 'Review pinned bytes')

def account(reserve=True):
    total = 0
    files = []
    if OUT.exists():
        require(OUT.is_dir() and not OUT.is_symlink(), 'Regular review output directory')
        for item in OUT.iterdir():
            require(len(files) < 8 and stat.S_ISREG(item.lstat().st_mode), 'Flat bounded review outputs')
            require(item.name in ['sole-review.lock', 'stdout.txt', 'stderr.txt', 'review.json'], 'Expected pre-budget output')
            total += item.stat().st_size
            files.append(item.name)
    report.update(lastObservedOutputFiles=len(files), lastObservedOutputBytes=total)
    require(total + (RESERVE if reserve else 0) <= CAP, 'Review output cap')
    return total, sorted(files)

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
        require(written == len(retained), 'Complete checker pipe persistence')
        require(len(retained) == len(chunk), 'Checker combined pipe cap')
    report['checkerPipeCaptureComplete'] = not selector.get_map()

def reap(timeout):
    global child_end
    try:
        CHILD.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        return
    if child_end is None:
        child_end = time.monotonic()
    report.update(checkerChildConfirmedReaped=True, checkerExitCode=CHILD.returncode,
                  checkerFullElapsedSeconds=child_end - launch_start)

try:
    require(len(sys.argv) == 1, 'Fixed review entry point accepts no arguments')
    require(os.getppid() == int(os.environ['M31_SAVED_REVIEW_CAPTURE_PID']), 'Direct frozen review capture required')
    OUT.mkdir(exist_ok=True)
    require(OUT.is_dir() and not OUT.is_symlink() and not list(OUT.iterdir()), 'Fresh one-shot review outputs')
    with (OUT / 'sole-review.lock').open('xb') as handle:
        require(handle.write(LOCK) == len(LOCK), 'Complete permanent review lock')
    reserved = True
    rb = read('review/review-freeze.json')
    require(os.environ.get('RESEARCH_REVIEW_FREEZE_SHA256') == digest(rb), 'Externally supplied review freeze hash')
    rf = json.loads(rb)
    require(rf['kind'] == 'frozen-saved-failure-record-review' and rf['sourceCommit'] == SOURCE
            and rf['sourceFreezeSHA256'] == FREEZE and rf['invocations'] == 1
            and rf['wallSeconds'] == 120 and rf['outputByteCap'] == CAP, 'Frozen review identity')
    require(sorted(p['path'] for p in rf['files']) == sorted(REVIEW_FILES), 'Complete review source inventory')
    for pin in rf['files']:
        check_pin(pin)
    require(rf['scienceManifest']['path'] == 'review/science-manifest.json', 'Saved manifest path')
    check_pin(rf['scienceManifest'])
    report.update(reviewFreezeSHA256=digest(rb), scienceManifestSHA256=rf['scienceManifest']['sha256'])
    handles = {name: (OUT / (name + '.txt')).open('xb', buffering=0) for name in ['stdout', 'stderr']}
    env = os.environ.copy()
    env.update(M31_SAVED_REVIEW_PARENT_PID=str(os.getpid()), M31_SAVED_REVIEW_DEADLINE=str(WORK_END))
    account()
    require(time.monotonic() < WORK_END, 'Review work remains')
    launch_start = time.monotonic()
    # Same group is intentional: fixed checker source creates no descendants.
    # Only its retained direct-child handle may be signaled; no group signal.
    CHILD = subprocess.Popen([sys.executable, str(BASE / 'review/source/check-records.py')],
                             cwd=BASE, env=env, start_new_session=False,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    report['checkerInvocations'] = 1
    selector = selectors.DefaultSelector()
    for name, stream in [('stdout', CHILD.stdout), ('stderr', CHILD.stderr)]:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
    while time.monotonic() < WORK_END:
        drain(min(.01, max(0, WORK_END - time.monotonic())))
        reap(0)
        account()
        if report['checkerChildConfirmedReaped'] and report['checkerPipeCaptureComplete']:
            break
    else:
        raise TimeoutError('Review work limit')
except BaseException as error:
    problem(error, 'review-work')
finally:
    signal.signal(signal.SIGALRM, hard_deadline)
    signal.setitimer(signal.ITIMER_REAL, max(.001, START + 120 - time.monotonic()))
    if CHILD is not None:
        if CHILD.returncode is None:
            try:
                report['checkerKillRequested'] = True
                CHILD.kill()
            except BaseException as error:
                problem(error, 'review-child-stop')
        while time.monotonic() < CLEANUP_END:
            try:
                reap(min(.01, max(0, CLEANUP_END - time.monotonic())))
            except BaseException as error:
                problem(error, 'review-child-reap')
            try:
                drain(0)
            except BaseException as error:
                problem(error, 'review-final-drain')
            if report['checkerChildConfirmedReaped'] and report['checkerPipeCaptureComplete']:
                break
            time.sleep(min(.005, max(0, CLEANUP_END - time.monotonic())))
        for stream in [CHILD.stdout, CHILD.stderr]:
            if stream is not None:
                stream.close()
    if selector is not None:
        selector.close()
    for handle in handles.values():
        try:
            handle.close()
        except BaseException as error:
            problem(error, 'review-pipe-file-close')

try:
    require(time.monotonic() < CLEANUP_END, 'Review finalization reserve')
    total, files = account(reserve=False)
    require(report['checkerChildConfirmedReaped'] and report['checkerPipeCaptureComplete'], 'Complete checker closure')
    report.update(outputAccountingComplete=True, preBudgetOutputBytes=total, preBudgetOutputFiles=len(files))
    require(files == ['review.json', 'sole-review.lock', 'stderr.txt', 'stdout.txt'], 'Exact four pre-budget outputs')
    require(read('review/review-freeze.json') == rb, 'Review freeze stable')
    for pin in rf['files']:
        check_pin(pin)
    check_pin(rf['scienceManifest'])
    worker_bytes = read('review/results/review.json', 65536)
    worker = json.loads(worker_bytes)
    stdout = read('review/results/stdout.txt', PIPE_CAP)
    stderr = read('review/results/stderr.txt', PIPE_CAP)
    require(len(stdout) == report['stdoutBytesObserved'] == report['stdoutBytesRetained']
            and len(stderr) == report['stderrBytesObserved'] == report['stderrBytesRetained'] == 0, 'Exact persisted checker pipes')
    require(stdout.endswith(b'\n') and len(stdout.splitlines()) == 1, 'One complete checker summary')
    worker_summary = json.loads(stdout)
    require(worker_summary['reportBytes'] == len(worker_bytes) and worker_summary['status'] == worker['status']
            and worker_summary['integrityVerified'] is True and worker_summary['decisionVerified'] is False
            and worker_summary['qualified'] is False, 'Checker summary binding')
    require(worker['completed'] is True and worker['integrityVerified'] is True and worker['terminalFailureVerified'] is True
            and worker['status'] == 'terminal-failure-record-integrity-verified'
            and worker['sourceCommit'] == SOURCE and worker['sourceFreezeSHA256'] == FREEZE
            and worker['reviewFreezeSHA256'] == digest(rb) and worker['scienceManifestSHA256'] == rf['scienceManifest']['sha256']
            and worker['decisionVerified'] is False and worker['qualified'] is False and worker['errors'] == [], 'Checker terminal integrity record')
    require(report['checkerInvocations'] == 1 and report['checkerExitCode'] == 0 and not report['checkerKillRequested']
            and report['checkerFullElapsedSeconds'] < 120 and not report['errors'], 'Actual saved-review integrity conjunction')
    report.update(observedIntegrityCandidateVerified=True, workerReportSHA256=digest(worker_bytes),
                  workerReportBytes=len(worker_bytes), workerIntegrityVerified=True, terminalFailureVerified=True)
except BaseException as error:
    problem(error, 'review-final-evidence')

report.update(terminal=True, active=False,
              status='review-closed' if report['checkerChildConfirmedReaped'] and report['checkerPipeCaptureComplete'] else 'review-incomplete-closure',
              wallSecondsBeforeFinalRecords=time.monotonic() - START,
              ownershipScope='Fixed frozen checker source creates no child or browser. Only its direct Popen child handle is stopped/reaped; no shared or numeric process-group signal.',
              elapsedScope='Internal timer begins before evidence I/O and stays armed through budget/stdout/exit. Caller must retain actual observer exit0 and complete hash/length-matching summary.',
              accountingScope='Persisted checker stdout/stderr count once in directory bytes; add exact budget and final stdout summary. Incomplete totals remain null.',
              budgetBytes=0, observerSummaryBytes=0, accountedTotalOutputBytes=None)
report['observedIntegrityCandidateVerified'] = report['observedIntegrityCandidateVerified'] and not report['errors']
for _ in range(24):
    budget_bytes = (json.dumps(report, sort_keys=True) + '\n').encode()
    summary = {'kind': 'caller-retained-saved-review-summary', 'sourceCommit': SOURCE, 'sourceFreezeSHA256': FREEZE,
               'reviewFreezeSHA256': report.get('reviewFreezeSHA256'),
               'observedIntegrityCandidateVerified': report['observedIntegrityCandidateVerified'],
               'integrityVerified': False, 'decisionVerified': False, 'qualified': False,
               'requiresCallerObservedObserverExit0AndCompleteSummary': True,
               'budgetSHA256': digest(budget_bytes), 'budgetBytes': len(budget_bytes),
               'summaryBytes': report['observerSummaryBytes'], 'outputAccountingComplete': report['outputAccountingComplete'],
               'accountedTotalOutputBytes': report['accountedTotalOutputBytes'], 'checkerExitCode': report['checkerExitCode']}
    summary_bytes = (json.dumps(summary, sort_keys=True) + '\n').encode()
    total = report['preBudgetOutputBytes'] + len(budget_bytes) + len(summary_bytes) if report['outputAccountingComplete'] else None
    if report['budgetBytes'] == len(budget_bytes) and report['observerSummaryBytes'] == len(summary_bytes) \
            and report['accountedTotalOutputBytes'] == total:
        break
    report.update(budgetBytes=len(budget_bytes), observerSummaryBytes=len(summary_bytes), accountedTotalOutputBytes=total)
else:
    os._exit(125)
if len(budget_bytes) > 16384 or len(summary_bytes) > 8192 or len(budget_bytes) + len(summary_bytes) > RESERVE \
        or (total is not None and total > CAP):
    os._exit(125)
if reserved:
    with (OUT / 'budget.json').open('xb') as handle:
        require(handle.write(budget_bytes) == len(budget_bytes), 'Complete review budget')
if os.write(sys.stdout.fileno(), summary_bytes) != len(summary_bytes):
    os._exit(125)
raise SystemExit(0 if report['observedIntegrityCandidateVerified'] else 1)
