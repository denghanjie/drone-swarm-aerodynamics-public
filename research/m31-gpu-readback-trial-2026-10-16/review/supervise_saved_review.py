"""Disabled-by-default single-child saved-review supervisor; no retry or generic runner."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
import review_primitives as review_support
import supervisor_primitives as supervisor_support
from review_primitives import admit_review, json_bytes, read_bounded, require
from supervisor_primitives import (PIPE_CAP, INNER_SECONDS, SOFT_SECONDS, REAP_SECONDS,
    HARD_SECONDS, LOCK, bounded_piece, bind_checker, digest, total_bytes)

CHILD = None


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def write_all(handle, data):
    at = 0
    while at < len(data):
        n = handle.write(data[at:])
        require(type(n) is int and 0 < n <= len(data)-at, 'Complete exclusive byte write')
        at += n
    return at


def exclusive(path, data, mode=0o600):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb', buffering=0) as handle:
        write_all(handle, data)
    return len(data)


def freeze_admission(base, config_bytes):
    require(Path(__file__).resolve() == base/'review/supervise_saved_review.py'
            and Path(supervisor_support.__file__).resolve() == base/'review/supervisor_primitives.py'
            and Path(review_support.__file__).resolve() == base/'review/review_primitives.py'
            and Path(sys.modules['byte_primitives'].__file__).resolve() == base/'review/byte_primitives.py',
            'Executing supervisor and imported helpers must be frozen trial files')
    source = os.environ.get('RESEARCH_SOURCE_COMMIT', '')
    freeze_sha = os.environ.get('RESEARCH_REMOTE_VERIFIED_FREEZE', '')
    require(re.fullmatch(r'[a-f0-9]{40}', source) is not None and re.fullmatch(r'[a-f0-9]{64}', freeze_sha) is not None,
            'External source identity required')
    data = read_bounded(base, 'freeze.json', 1048576)
    require(digest(data) == freeze_sha, 'Independently verified freeze required')
    freeze = json_bytes(data, 1048576); pins = freeze['files']
    require(type(pins) is list and 1 <= len(pins) <= 256, 'Bounded freeze inventory')
    by_path = {pin['path']:pin for pin in pins}
    require(len(by_path) == len(pins), 'Unique source pins')
    repo = base.parents[1]
    required = ['config.json', 'review/supervise_saved_review.py', 'review/supervisor_primitives.py',
                'review/check_saved_files.py', 'review/review_primitives.py', 'review/byte_primitives.py']
    for relative in required:
        key = str((base/relative).relative_to(repo)); require(key in by_path, 'Required supervisor/checker source pin')
        actual = read_bounded(base, relative, 1048576); pin = by_path[key]
        require(type(pin['bytes']) is int and len(actual) == pin['bytes'] and digest(actual) == pin['sha256'], 'Exact supervisor/checker source bytes')
    require(read_bounded(base, 'config.json', 16384) == config_bytes, 'Unchanged admitted configuration')
    return source, freeze_sha, repo


def main():
    global CHILD
    start = time.monotonic()
    # Configuration is the only data file read before review allocation/window admission.
    try:
        require(len(sys.argv) == 2 and Path(sys.argv[1]).is_absolute(), 'One absolute new trial directory')
        base = Path(sys.argv[1]).resolve()
        config_bytes = read_bounded(base, 'config.json', 16384)
        config = json_bytes(config_bytes, 16384)
        admit_review(config, datetime.datetime.now(datetime.timezone.utc))
    except Exception:
        os.write(sys.stdout.fileno(), b'{"kind":"saved-review-supervisor-admission-refused","runtimeArtifactsTouched":false,"reviewReserved":false}\n')
        return 2

    def hard_stop(signum, frame):
        if CHILD is not None:
            try:
                CHILD.kill()
            except Exception:
                pass
        os._exit(124)
    signal.signal(signal.SIGALRM, hard_stop)
    signal.setitimer(signal.ITIMER_REAL, max(.001, start+HARD_SECONDS-time.monotonic()))
    receipt = {'version':1, 'kind':'saved-gpu-readback-review-supervision', 'terminal':False,
        'sourceCommit':None, 'sourceFreezeSHA256':None, 'qualified':False, 'recordIntegrityVerified':False,
        'externalToolCompletionRequired':True, 'retryPermitted':False,
        'innerCheckerHardSeconds':INNER_SECONDS, 'supervisorSoftSeconds':SOFT_SECONDS,
        'supervisorReapSeconds':REAP_SECONDS, 'supervisorHardSeconds':HARD_SECONDS,
        'checkerSpawnAttempts':0, 'checkerInvocations':0, 'checkerReaped':False, 'actualCheckerExitCode':None,
        'checkerFullElapsedSeconds':None, 'checkerElapsedUnder30':False,
        'softStopTriggered':False, 'directChildKillSent':False, 'pipeByteCapCombined':PIPE_CAP,
        'stdoutBytesObserved':0, 'stdoutBytesRetained':0, 'stderrBytesObserved':0, 'stderrBytesRetained':0,
        'stdoutEOF':False, 'stderrEOF':False, 'pipeCaptureComplete':False, 'privatePipeFilesClosed':False,
        'privateStdoutSHA256':None, 'privateStderrSHA256':None, 'privateStdoutMatchesCapturedBuffer':False,
        'checkerSummaryBound':False, 'checkerRecordIntegrityCandidate':False,
        'checkerReportBytes':None, 'checkerReportSHA256':None, 'checkerSummaryBytes':None, 'checkerSummarySHA256':None,
        'publicCheckerSummaryBytes':0, 'publicCheckerSummaryClosed':False,
        'candidateReviewCompletionVerified':False, 'supervisorLockBytes':0,
        'baseIncludesOnePrivateChildStdoutCopy':True, 'accountedBaseBytes':None,
        'accountedBeforeExternalCompletionBytes':None, 'externalCompletionReceiptBytesIncluded':False,
        'supervisorReceiptBytes':None, 'supervisorSummaryBytes':None, 'wallSecondsBeforeFinalRecords':None,
        'errors':[]}
    stdout = bytearray(); files = {}; selector = selectors.DefaultSelector(); private_dir = None
    child_start = None; reservation = False
    try:
        source, freeze_sha, repo = freeze_admission(base, config_bytes)
        receipt.update(sourceCommit=source, sourceFreezeSHA256=freeze_sha)
        private_value = os.environ.get('RESEARCH_REVIEW_PRIVATE_DIR', '')
        require(private_value and Path(private_value).is_absolute(), 'Private raw-pipe directory required')
        private_dir = Path(private_value)
        require(private_dir.resolve() == private_dir and private_dir.is_dir()
                and repo not in private_dir.parents and private_dir != repo, 'Private directory outside publication tree')
        require(not any(private_dir.iterdir()), 'Fresh private raw-pipe directory')
        # The checker retains its own review.lock. This supervisor has a separate permanent reservation.
        receipt['supervisorLockBytes'] = exclusive(base/'review-supervisor.lock', LOCK)
        reservation = True
        for name in ['stdout', 'stderr']:
            fd = os.open(private_dir/('review-'+name+'.bin'), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            files[name] = os.fdopen(fd, 'wb', buffering=0)
        require(read_bounded(base, 'config.json', 16384) == config_bytes, 'Allocation unchanged before checker launch')
        admit_review(config, datetime.datetime.now(datetime.timezone.utc))
        require(time.monotonic()+INNER_SECONDS < start+SOFT_SECONDS, 'Full inner allowance remains before soft stop')
        child_start = time.monotonic()
        receipt['checkerSpawnAttempts'] += 1
        CHILD = subprocess.Popen([sys.executable, '-E', '-s', '-B', str(base/'review/check_saved_files.py'), str(base)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        receipt['checkerInvocations'] += 1
        for name, stream in [('stdout', CHILD.stdout), ('stderr', CHILD.stderr)]:
            os.set_blocking(stream.fileno(), False); selector.register(stream, selectors.EVENT_READ, name)
        while True:
            now = time.monotonic()
            if CHILD.poll() is not None and not receipt['checkerReaped']:
                receipt['actualCheckerExitCode'] = CHILD.wait(timeout=0)
                receipt['checkerReaped'] = True
                receipt['checkerFullElapsedSeconds'] = time.monotonic()-child_start
                receipt['checkerElapsedUnder30'] = receipt['checkerFullElapsedSeconds'] < INNER_SECONDS
            if receipt['checkerReaped'] and not selector.get_map():
                break
            if now >= start+SOFT_SECONDS and not receipt['softStopTriggered']:
                receipt['softStopTriggered'] = True; receipt['errors'].append('supervisor-soft-stop')
                if not receipt['checkerReaped']:
                    CHILD.kill(); receipt['directChildKillSent'] = True
            if now >= start+REAP_SECONDS:
                receipt['errors'].append('supervisor-reap-or-pipe-deadline'); break
            for key, _ in selector.select(min(.05, max(0, start+REAP_SECONDS-now))):
                name = key.data
                try:
                    data = os.read(key.fileobj.fileno(), 65536)
                except BlockingIOError:
                    continue
                if not data:
                    selector.unregister(key.fileobj); key.fileobj.close(); receipt[name+'EOF'] = True; continue
                receipt[name+'BytesObserved'] += len(data)
                retained = receipt['stdoutBytesRetained']+receipt['stderrBytesRetained']
                keep, dropped = bounded_piece(data, retained)
                if keep:
                    write_all(files[name], keep); receipt[name+'BytesRetained'] += len(keep)
                    if name == 'stdout':
                        stdout.extend(keep)
                if dropped and 'pipe-cap-exceeded' not in receipt['errors']:
                    receipt['errors'].append('pipe-cap-exceeded')
                    if CHILD.poll() is None:
                        CHILD.kill(); receipt['directChildKillSent'] = True
        if not receipt['checkerReaped'] and CHILD.poll() is not None:
            receipt['actualCheckerExitCode'] = CHILD.wait(timeout=0); receipt['checkerReaped'] = True
            receipt['checkerFullElapsedSeconds'] = time.monotonic()-child_start
            receipt['checkerElapsedUnder30'] = receipt['checkerFullElapsedSeconds'] < INNER_SECONDS
    except Exception:
        receipt['errors'].append('supervisor-preflight-or-capture-failed')
    finally:
        if CHILD is not None and not receipt['checkerReaped']:
            try:
                if CHILD.poll() is None:
                    CHILD.kill(); receipt['directChildKillSent'] = True
                remain = max(0, start+REAP_SECONDS-time.monotonic())
                receipt['actualCheckerExitCode'] = CHILD.wait(timeout=remain); receipt['checkerReaped'] = True
                receipt['checkerFullElapsedSeconds'] = time.monotonic()-child_start
                receipt['checkerElapsedUnder30'] = receipt['checkerFullElapsedSeconds'] < INNER_SECONDS
            except Exception:
                receipt['errors'].append('direct-checker-reap-unobserved')
        for key in list(selector.get_map().values()):
            try:
                key.fileobj.close()
            except Exception:
                receipt['errors'].append('checker-pipe-close-failed')
        selector.close()
        closed = len(files) == 2
        for handle in files.values():
            try:
                handle.close()
            except Exception:
                closed = False; receipt['errors'].append('private-pipe-close-failed')
        receipt['privatePipeFilesClosed'] = closed

    try:
        if private_dir is not None:
            for name in ['stdout', 'stderr']:
                filename = 'review-'+name+'.bin'
                if (private_dir/filename).exists():
                    data = read_bounded(private_dir, filename, PIPE_CAP)
                    if len(data) != receipt[name+'BytesRetained']:
                        receipt['errors'].append('private-pipe-write-incomplete')
                    receipt[name+'BytesRetained'] = len(data)
                    receipt['private'+name.capitalize()+'SHA256'] = digest(data)
                    if name == 'stdout':
                        receipt['privateStdoutMatchesCapturedBuffer'] = data == bytes(stdout)
                        if not receipt['privateStdoutMatchesCapturedBuffer']:
                            receipt['errors'].append('private-stdout-content-mismatch')
        receipt['pipeCaptureComplete'] = (receipt['stdoutEOF'] and receipt['stderrEOF'] and receipt['privatePipeFilesClosed']
            and receipt['stdoutBytesObserved'] == receipt['stdoutBytesRetained']
            and receipt['stderrBytesObserved'] == receipt['stderrBytesRetained'] and receipt['privateStdoutMatchesCapturedBuffer'])
        if receipt['pipeCaptureComplete']:
            bound = bind_checker(bytes(stdout), read_bounded(base,'review/results/summary.json',4096),
                read_bounded(base,'review/results/report.json',65536), read_bounded(base,'review.lock',256))
            receipt.update(checkerSummaryBound=True, checkerRecordIntegrityCandidate=bound['recordIntegrityCandidate'],
                checkerReportBytes=bound['reportBytes'], checkerReportSHA256=bound['reportSHA256'],
                checkerSummaryBytes=bound['summaryBytes'], checkerSummarySHA256=bound['summarySHA256'],
                accountedBaseBytes=bound['accountedBaseBytes'])
            receipt['publicCheckerSummaryBytes'] = exclusive(base/'publication/review-output.json', bytes(stdout), 0o644)
            receipt['publicCheckerSummaryClosed'] = True
    except Exception:
        receipt['errors'].append('checker-summary-or-private-pipe-binding-failed')
    # If the public copy write failed, preserve/account its actual partial prefix without repairing it.
    if not receipt['publicCheckerSummaryClosed'] and (base/'publication/review-output.json').exists():
        try:
            receipt['publicCheckerSummaryBytes'] = len(read_bounded(base,'publication/review-output.json',4096))
        except Exception:
            receipt['errors'].append('public-checker-copy-accounting-failed')
            receipt['accountedBaseBytes'] = None
    receipt['candidateReviewCompletionVerified'] = (receipt['checkerInvocations'] == receipt['checkerSpawnAttempts'] == 1
        and receipt['checkerReaped'] and receipt['actualCheckerExitCode'] == 0 and receipt['checkerElapsedUnder30']
        and receipt['pipeCaptureComplete'] and receipt['stderrBytesObserved'] == 0
        and receipt['checkerSummaryBound'] and receipt['checkerRecordIntegrityCandidate']
        and receipt['publicCheckerSummaryClosed'] and not receipt['errors'])
    receipt['terminal'] = True
    receipt['wallSecondsBeforeFinalRecords'] = time.monotonic()-start
    try:
        require(reservation and time.monotonic() < start+HARD_SECONDS, 'Reserved bounded supervisor finalization')
        for _ in range(16):
            receipt_bytes = encode(receipt)
            summary = {'version':1, 'kind':'saved-gpu-readback-review-supervisor-summary',
                'sourceCommit':receipt['sourceCommit'], 'sourceFreezeSHA256':receipt['sourceFreezeSHA256'],
                'terminal':True, 'qualified':False, 'recordIntegrityVerified':False,
                'externalToolCompletionRequired':True, 'candidateReviewCompletionVerified':receipt['candidateReviewCompletionVerified'],
                'actualCheckerExitCode':receipt['actualCheckerExitCode'], 'checkerReaped':receipt['checkerReaped'],
                'checkerFullElapsedSeconds':receipt['checkerFullElapsedSeconds'], 'pipeCaptureComplete':receipt['pipeCaptureComplete'],
                'checkerSummaryBound':receipt['checkerSummaryBound'], 'supervisorReceiptClosed':True, 'supervisorReceiptBytes':len(receipt_bytes),
                'supervisorReceiptSHA256':digest(receipt_bytes), 'supervisorSummaryBytes':receipt['supervisorSummaryBytes'],
                'accountedBeforeExternalCompletionBytes':receipt['accountedBeforeExternalCompletionBytes']}
            summary_bytes = encode(summary)
            total = total_bytes(receipt['accountedBaseBytes'], receipt['stderrBytesRetained'], receipt['supervisorLockBytes'],
                receipt['publicCheckerSummaryBytes'], len(receipt_bytes), len(summary_bytes))
            if (receipt['supervisorReceiptBytes'] == len(receipt_bytes) and receipt['supervisorSummaryBytes'] == len(summary_bytes)
                    and receipt['accountedBeforeExternalCompletionBytes'] == total):
                break
            receipt.update(supervisorReceiptBytes=len(receipt_bytes), supervisorSummaryBytes=len(summary_bytes),
                           accountedBeforeExternalCompletionBytes=total)
        else:
            raise ValueError('Supervisor accounting convergence')
        require(len(receipt_bytes) <= 16384 and len(summary_bytes) <= 4096 and (total is None or total <= 8388608)
                and time.monotonic() < start+HARD_SECONDS, 'Supervisor final byte/time caps')
        exclusive(base/'publication/review-supervisor.json', receipt_bytes, 0o644)
        require(time.monotonic() < start+HARD_SECONDS, 'Supervisor complete stdout deadline')
        require(os.write(sys.stdout.fileno(), summary_bytes) == len(summary_bytes), 'Complete supervisor summary stdout')
        return 0 if receipt['candidateReviewCompletionVerified'] else 1
    except Exception:
        return 125


if __name__ == '__main__':
    raise SystemExit(main())
