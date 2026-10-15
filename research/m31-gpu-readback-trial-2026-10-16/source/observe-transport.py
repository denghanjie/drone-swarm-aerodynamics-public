"""One whole-lifecycle transport observer. No numerical implementation is imported."""
import time
START = time.monotonic()
# Source-only preparation. Admission precedes timers, process access and output writes.
import sys as _sys
from pathlib import Path as _Path
from admission import admit_file as _admit_file
try:
    _admit_file(_Path(__file__).resolve().parents[1] / 'config.json', 'launch')
except Exception:
    _sys.stderr.write('Execution unallocated or outside its prospective window.\n')
    raise SystemExit(78)

import signal, os

WRAPPER = None
WRAPPER_REAPED = False
WRAPPER_SIGNALABLE = False
HELPERS = []
def hard_deadline(signum, frame):
    # A direct, unreaped session leader retains its PID. Never signal shared groups
    # or a numeric group after the observer reaps its leader.
    if WRAPPER is not None and WRAPPER_SIGNALABLE:
        try:
            if os.getpgid(WRAPPER.pid) == WRAPPER.pid:
                os.killpg(WRAPPER.pid, signal.SIGKILL)
        except OSError:
            pass
    for child in HELPERS:
        if child.returncode is None:
            try:
                child.kill()
            except OSError:
                pass
    os._exit(124)
signal.signal(signal.SIGALRM, hard_deadline)
signal.setitimer(signal.ITIMER_REAL, max(.001, START + 60 - time.monotonic()))

import sys, json, hashlib, subprocess, selectors, tempfile, datetime, stat
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
WORK_END, CLEANUP_END = START + 40, START + 58
RAW_CAP, RESULT_CAP, RSS_CAP = 8388608, 8388608, 2147483648
PROVENANCE_RESERVE, PIPE_CAP, PS_CAP = 131072, 8192, 4194304
OUT, RAW = BASE / 'results', BASE / 'raw'
REGISTRY = None
NONCE = None
BROWSERS = {}
PRIVATE_ENTRIES = []
CAPTURE_PID = None
RELAY_LOGS = {}
selector = None
reserved = False
report = {'kind': 'whole-transport-lifecycle-observation', 'attempts': 0,
          'wallCapSeconds': 60, 'workStopSeconds': 40, 'cleanupStopSeconds': 58,
          'rawByteCap': RAW_CAP, 'combinedByteCap': RESULT_CAP, 'ownedRSSByteCap': RSS_CAP,
          'provenanceReserveBytes': PROVENANCE_RESERVE, 'wrapperInvocations': 0,
          'wrapperExitCode': None, 'wrapperReaped': False, 'wrapperGroupAbsent': False,
          'wrapperKillSent': False, 'stdoutBytesObserved': 0, 'stderrBytesObserved': 0,
          'stdoutBytesRetained': 0, 'stderrBytesRetained': 0,
          'wrapperPipeCaptureComplete': False, 'pipeByteCapCombined': PIPE_CAP,
          'rssSamples': 0, 'peakObservedOwnedRSSBytes': 0, 'rssProbeErrors': 0,
          'registryComplete': False, 'candidateLifecycleVerified': False,
          'cleanupErrorObserved': False, 'outputAccountingComplete': False,
          'rawBytes': None, 'rawFiles': None, 'resultDirectoryBytes': None,
          'resultDirectoryFiles': None, 'privateDiagnosticBytes': None,
          'privateDiagnosticFiles': None,
          'wholeLifecycleVerified': False, 'qualified': False,
          'externalCompletionObservationRequired': True,
          'requiresCallerObservedObserverExit0AndElapsedUnder60': True,
          'retryPermitted': False, 'errors': []}

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def problem(error, phase):
    if len(report['errors']) < 32:
        report['errors'].append({'phase': phase, 'type': type(error).__name__,
                                 'reason': str(error) if type(error) is RuntimeError else 'Operation failed'})

def cleanup_problem(error, phase):
    report['cleanupErrorObserved'] = True
    problem(error, phase)

def soft_deadline(signum, frame):
    report['deadlineReached'] = True
    signal.signal(signal.SIGALRM, hard_deadline)
    signal.setitimer(signal.ITIMER_REAL, max(.001, START + 60 - time.monotonic()))
    raise TimeoutError('Transport work deadline')

signal.signal(signal.SIGALRM, soft_deadline)
signal.setitimer(signal.ITIMER_REAL, max(.001, WORK_END - time.monotonic()))

def read_file(path, cap):
    require(path.is_file() and not path.is_symlink(), 'Regular evidence file required')
    require(path.stat().st_size <= cap, 'Evidence read cap')
    with path.open('rb') as handle:
        data = handle.read(cap + 1)
    require(len(data) <= cap, 'Evidence growth cap')
    return data

def directory_bytes(directory):
    if not directory.exists():
        return 0, 0
    require(directory.is_dir() and not directory.is_symlink(), 'Regular evidence directory')
    total = count = 0
    for path in directory.iterdir():
        require(count < 4096, 'Evidence file-count cap')
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), 'Flat regular evidence files only')
        count += 1
        total += st.st_size
    return total, count

def account(reserve=True):
    raw_bytes, raw_files = directory_bytes(RAW)
    result_bytes, result_files = directory_bytes(OUT)
    private_bytes, private_files = directory_bytes(REGISTRY.parent) if REGISTRY else (0, 0)
    pipe_bytes = report['stdoutBytesObserved'] + report['stderrBytesObserved']
    report.update(lastObservedRawBytes=raw_bytes, lastObservedRawFiles=raw_files,
                  lastObservedResultDirectoryBytes=result_bytes,
                  lastObservedResultDirectoryFiles=result_files,
                  lastObservedPrivateDiagnosticBytes=private_bytes,
                  lastObservedPrivateDiagnosticFiles=private_files,
                  wrapperPipeBytes=pipe_bytes)
    require(raw_bytes <= RAW_CAP, 'Raw byte cap')
    # Relay bytes are persisted in private files and counted there exactly once.
    require(raw_bytes + result_bytes + private_bytes + (PROVENANCE_RESERVE if reserve else 0) <= RESULT_CAP,
            'Combined result/diagnostic byte cap')
    return {'rawBytes': raw_bytes, 'rawFiles': raw_files,
            'resultDirectoryBytes': result_bytes, 'resultDirectoryFiles': result_files,
            'privateDiagnosticBytes': private_bytes, 'privateDiagnosticFiles': private_files}

def cleanup_helpers():
    # Keep unreaped direct children in HELPERS even when one kill/wait fails.
    for child in list(HELPERS):
        try:
            if child.returncode is None:
                child.kill()
                remaining = CLEANUP_END - time.monotonic()
                if remaining > 0:
                    child.wait(timeout=min(.025, remaining))
        except BaseException as error:
            cleanup_problem(error, 'cleanup-probe-child')
        finally:
            if child.returncode is not None:
                HELPERS.remove(child)

def process_table():
    # Bound time AND bytes, including stderr. ps is a direct child, never a group.
    child = subprocess.Popen(['/bin/ps', '-ww', '-axo', 'pid=,ppid=,pgid=,rss=,stat=,command='],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    HELPERS.append(child)
    sel = selectors.DefaultSelector()
    data = {'out': bytearray(), 'err': bytearray()}
    end = min(CLEANUP_END, time.monotonic() + .25)
    try:
        for name, stream in [('out', child.stdout), ('err', child.stderr)]:
            os.set_blocking(stream.fileno(), False)
            sel.register(stream, selectors.EVENT_READ, name)
        while sel.get_map():
            require(time.monotonic() < end, 'Process probe deadline')
            for key, _ in sel.select(min(.01, max(0, end - time.monotonic()))):
                remaining = PS_CAP - len(data['out']) - len(data['err'])
                try:
                    chunk = os.read(key.fileobj.fileno(), min(16384, remaining + 1))
                except BlockingIOError:
                    continue
                if not chunk:
                    sel.unregister(key.fileobj)
                    continue
                data[key.data].extend(chunk)
                require(len(data['out']) + len(data['err']) <= PS_CAP, 'Process probe byte cap')
        child.wait(timeout=max(.001, min(.025, end - time.monotonic())))
        require(child.returncode == 0 and not data['err'], 'Process probe failed')
    finally:
        sel.close()
        if child.returncode is None:
            child.kill()
            try:
                child.wait(timeout=.025)
            except subprocess.TimeoutExpired:
                pass
        child.stdout.close()
        child.stderr.close()
        if child.returncode is not None:
            HELPERS.remove(child)
    require(child.returncode is not None, 'Process probe child unreaped')
    table = {}
    for line in data['out'].decode('utf-8', 'strict').splitlines():
        parts = line.strip().split(None, 5)
        require(len(parts) == 6, 'Malformed process row')
        pid, ppid, pgid, rss = map(int, parts[:4])
        require(pid > 0 and ppid >= 0 and pgid >= 0 and rss >= 0 and pid not in table,
                'Invalid process identity row')
        table[pid] = {'pid': pid, 'ppid': ppid, 'pgid': pgid, 'rss': rss * 1024,
                      'state': parts[4], 'command': parts[5], 'observerProbe': pid == child.pid}
    require(table and os.getpid() in table, 'Incomplete process table')
    return table

def registry_entries(final=False):
    global PRIVATE_ENTRIES
    data = read_file(REGISTRY, 65536)
    complete = not data or data.endswith(b'\n')
    lines = data.splitlines()
    if not complete:
        lines = lines[:-1]
    require(len(lines) <= 32, 'Registry record count cap')
    entries = []
    parse_error = None
    for line in lines:
        try:
            entry = json.loads(line)
            require(isinstance(entry, dict) and entry.get('version') == 1 and entry.get('nonce') == NONCE,
                    'Private registry authority mismatch')
            require(entry.get('phase') in ['node-intent', 'node-spawned', 'spawn-intent', 'spawned'],
                    'Registry phase')
        except BaseException as error:
            parse_error = error
            break
        entries.append(entry)
    # Previously admitted identities remain usable if a later append/read fails.
    require(entries[:len(PRIVATE_ENTRIES)] == PRIVATE_ENTRIES, 'Append-only registry history')
    intents = {}
    completions = {}
    for entry in entries:
        eid = entry.get('id')
        require(isinstance(eid, str), 'Registry id')
        target = intents if entry['phase'].endswith('intent') else completions
        require(eid not in target, 'Duplicate registry phase')
        target[eid] = entry
        if target is completions:
            require(eid in intents, 'Spawn without earlier intent')
    for eid, entry in intents.items():
        if eid == 'node':
            require(entry['phase'] == 'node-intent' and entry.get('detached') is False,
                    'Node must share relay group')
            require(entry.get('ownership') == {'executable': sys.argv[1], 'arguments': [str(BASE / 'source/host-worker.cjs')]},
                    'Exact fixed Node invocation')
            if eid in completions:
                require(completions[eid].get('phase') == 'node-spawned'
                        and type(completions[eid].get('pid')) is int and completions[eid]['pid'] > 0
                        and completions[eid].get('pgid') == WRAPPER.pid and completions[eid].get('detached') is False,
                        'Node group registration')
            continue
        require(entry['phase'] == 'spawn-intent', 'Auxiliary intent shape')
        if not entry.get('detached'):
            continue
        owner = entry.get('ownership', {})
        profile, exe = owner.get('profileArgument'), owner.get('executable')
        require(entry.get('kind') == 'chrome' and exe == os.environ.get('RESEARCH_CHROME_EXECUTABLE')
                and isinstance(profile, str) and profile.startswith('--user-data-dir=/')
                and not any(c.isspace() for c in profile), 'Exact browser ownership intent')
        require(len([i for i in intents.values() if i.get('detached')]) <= 1, 'One browser launch only')
        if eid not in BROWSERS:
            BROWSERS[eid] = {'executable': exe, 'profile': profile, 'pid': None,
                             'seen': False, 'absent': False, 'killSent': False}
        item = BROWSERS[eid]
        require(item['executable'] == exe and item['profile'] == profile, 'Stable browser intent')
        if eid in completions:
            completion = completions[eid]
            pid = completion.get('pid')
            require(completion.get('ownership') == owner and completion.get('detached') is True
                    and completion.get('kind') == 'chrome', 'Browser completion binding')
            if pid is not None:
                require(type(pid) is int and pid > 0 and item['pid'] in [None, pid], 'Browser PID binding')
                item['pid'] = pid
    PRIVATE_ENTRIES = entries
    if parse_error is not None:
        raise parse_error
    if final:
        require(complete, 'Incomplete final registry append')
        require('node' in intents and 'node' in completions and set(intents) == set(completions),
                'All spawn intents completed')
        report['registryComplete'] = True
    return entries

def browser_match(row, item):
    command = row['command']
    exe = item['executable']
    return row['pid'] == row['pgid'] and (command == exe or command.startswith(exe + ' ')) \
        and item['profile'] in command.split()

def inspect_groups(table, kill=False):
    groups = {WRAPPER.pid} if WRAPPER is not None else set()
    for item in BROWSERS.values():
        try:
            groups.update(inspect_browser(table, item, kill))
        except BaseException as error:
            if not kill:
                raise
            cleanup_problem(error, 'cleanup-browser')
    return groups

def inspect_browser(table, item, kill):
    groups = set()
    matches = [row for row in table.values() if browser_match(row, item)]
    require(len(matches) <= 1, 'Unique browser command/profile identity')
    if item['absent']:
        require(not matches, 'Browser reappeared after confirmed absence')
        return groups
    if matches:
        row = matches[0]
        require(item['pid'] in [None, row['pid']], 'Intent/PID identity mismatch')
        item.update(pid=row['pid'], seen=True)
        groups.add(row['pid'])
        if kill:
            # Fresh process-table ownership proof immediately precedes signal.
            # An exact unique profile is mandatory; never kill by PID alone.
            try:
                require(os.getpgid(row['pid']) == row['pid'], 'Browser group changed')
                os.killpg(row['pid'], signal.SIGKILL)
                item['killSent'] = True
            except ProcessLookupError:
                pass
    elif item['pid'] is not None:
        members = [row for row in table.values() if row['pgid'] == item['pid']]
        if not members:
            item['absent'] = True
        else:
            groups.add(item['pid'])
            if kill:
                require(False, 'Browser group has no verifiable live leader; no signal sent')
    return groups

def sample():
    registry_entries()
    table = process_table()
    groups = inspect_groups(table)
    owned = {row['pid'] for row in table.values() if row['pgid'] in groups}
    changed = True
    while changed:
        count = len(owned)
        owned.update(row['pid'] for row in table.values() if row['ppid'] in owned)
        changed = count != len(owned)
    require(CAPTURE_PID in table and table[os.getpid()]['ppid'] == CAPTURE_PID,
            'Direct capture parent identity')
    observed_auxiliary = {os.getpid(), CAPTURE_PID} | {child.pid for child in HELPERS} \
        | {row['pid'] for row in table.values() if row['observerProbe']}
    rss = sum(table[pid]['rss'] for pid in owned | observed_auxiliary if pid in table)
    report['rssSamples'] += 1
    report['peakObservedOwnedRSSBytes'] = max(report['peakObservedOwnedRSSBytes'], rss)
    require(rss <= RSS_CAP, 'Sampled owned-process RSS cap')
    require(all(table[pid]['pgid'] in groups for pid in owned), 'Unregistered detached descendant')
    return table

def drain(timeout):
    if selector is None:
        return
    for key, _ in selector.select(timeout):
        field = key.data + 'BytesObserved'
        remaining = PIPE_CAP - report['stdoutBytesRetained'] - report['stderrBytesRetained']
        try:
            chunk = os.read(key.fileobj.fileno(), min(4096, remaining + 1))
        except BlockingIOError:
            continue
        if not chunk:
            selector.unregister(key.fileobj)
            continue
        report[field] += len(chunk)
        retained = chunk[:remaining]
        written = RELAY_LOGS[key.data].write(retained)
        report[key.data + 'BytesRetained'] += written
        require(written == len(retained), 'Complete private relay pipe write')
        require(len(retained) == len(chunk), 'Relay combined pipe byte cap')
    report['wrapperPipeCaptureComplete'] = not selector.get_map()

def cleanup():
    global WRAPPER_REAPED, WRAPPER_SIGNALABLE
    # Freeze spawning by killing the directly owned relay+Node group first, while
    # its leader remains unreaped. Chrome intents were written before its spawn.
    if WRAPPER is not None and not WRAPPER_REAPED:
        try:
            require(os.getpgid(WRAPPER.pid) == WRAPPER.pid, 'Relay group identity')
            os.killpg(WRAPPER.pid, signal.SIGKILL)
            report['wrapperKillSent'] = True
        except ProcessLookupError:
            pass
        except BaseException as error:
            cleanup_problem(error, 'cleanup-relay-signal')
        # Disable signal-handler group signaling BEFORE any call that can reap.
        # This closes the wait-return / Python assignment signal window.
        WRAPPER_SIGNALABLE = False
        try:
            WRAPPER.wait(timeout=max(.001, min(.05, CLEANUP_END - time.monotonic())))
        except subprocess.TimeoutExpired:
            pass
        except BaseException as error:
            cleanup_problem(error, 'cleanup-relay-wait')
        WRAPPER_REAPED = WRAPPER.returncode is not None
        report.update(wrapperReaped=WRAPPER_REAPED, wrapperExitCode=WRAPPER.returncode)
    while time.monotonic() < CLEANUP_END:
        if REGISTRY is not None:
            try:
                registry_entries()
            except BaseException as error:
                cleanup_problem(error, 'cleanup-registry')
        cleanup_helpers()
        table = None
        if WRAPPER is not None or BROWSERS:
            try:
                table = process_table()
            except BaseException as error:
                cleanup_problem(error, 'cleanup-process-probe')
                cleanup_helpers()
        if table is not None:
            inspect_groups(table, kill=True)
        if WRAPPER is not None and WRAPPER_REAPED and table is not None:
            # Never signal this numeric group again after reaping.
            if not any(row['pgid'] == WRAPPER.pid for row in table.values()):
                report['wrapperGroupAbsent'] = True
        elif WRAPPER is not None and not WRAPPER_REAPED:
            try:
                WRAPPER.wait(timeout=.01)
            except subprocess.TimeoutExpired:
                pass
            except BaseException as error:
                cleanup_problem(error, 'cleanup-relay-wait')
            WRAPPER_REAPED = WRAPPER.returncode is not None
            report.update(wrapperReaped=WRAPPER_REAPED, wrapperExitCode=WRAPPER.returncode)
        try:
            drain(0)
        except BaseException as error:
            cleanup_problem(error, 'cleanup-relay-pipes')
        if (WRAPPER is None or report['wrapperGroupAbsent']) and all(item['absent'] for item in BROWSERS.values()) \
                and (selector is None or report['wrapperPipeCaptureComplete']) and not HELPERS:
            break
        time.sleep(min(.025, max(0, CLEANUP_END - time.monotonic())))
    if REGISTRY is not None:
        try:
            registry_entries(final=True)
        except BaseException as error:
            cleanup_problem(error, 'cleanup-final-registry')
    cleanup_helpers()
    require(WRAPPER is not None and report['wrapperReaped'] and report['wrapperGroupAbsent']
            and report['wrapperPipeCaptureComplete'] and all(item['absent'] for item in BROWSERS.values())
            and not HELPERS, 'Complete owned-process and pipe closure')

try:
    require(len(sys.argv) == 2 and Path(sys.argv[1]).is_absolute(), 'Supply one absolute pinned Node executable')
    CAPTURE_PID = int(os.environ['RESEARCH_CAPTURE_PID'])
    require(CAPTURE_PID > 0 and os.getppid() == CAPTURE_PID, 'Direct capture parent required')
    cfg = json.loads(read_file(BASE / 'config.json', 1048576))
    limits = cfg['limits']
    require(limits == {'wallSeconds':60, 'workerSeconds':40, 'evaluateSeconds':12, 'cleanupSeconds':58,
                       'combinedBytes':RESULT_CAP, 'ownedRSSBytes':RSS_CAP, 'traceEvents':2048},
            'Exact adopted diagnostic resource envelope required')
    _admit_file(BASE / 'config.json', 'launch')
    OUT.mkdir(exist_ok=True)
    require(not OUT.is_symlink() and not list(OUT.iterdir()), 'Fresh diagnostic result directory')
    with (OUT / 'sole-launch.lock').open('xb') as handle:
        require(handle.write(b'One transport invocation reserved. Permanent; no retry.\n') == 56, 'Complete permanent invocation lock')
    reserved = True
    report['attempts'] = 1
    require(not RAW.exists() or (RAW.is_dir() and not RAW.is_symlink() and not list(RAW.iterdir())),
            'Fresh raw evidence directory')
    freeze_bytes = read_file(BASE / 'freeze.json', 1048576)
    freeze_sha = hashlib.sha256(freeze_bytes).hexdigest()
    require(os.environ.get('RESEARCH_REMOTE_VERIFIED_FREEZE') == freeze_sha, 'Independent source freeze receipt')
    source = os.environ.get('RESEARCH_SOURCE_COMMIT', '')
    require(len(source) == 40 and all(c in '0123456789abcdef' for c in source), 'Published source commit')
    freeze = json.loads(freeze_bytes)
    pinned = set()
    for pin in freeze['files']:
        relative = Path(pin['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Contained source pin')
        target = REPO / relative
        require(target.resolve() == target, 'Source pin cannot traverse symlink')
        data = read_file(target, 16777216)
        require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Frozen source bytes')
        pinned.add(target)
    require(all(BASE / ('source/' + name) in pinned for name in ['capture-transport.py', 'observe-transport.py', 'run-once.py', 'process-registry.cjs', 'host-worker.cjs', 'host-logic.cjs', 'admission.py', 'validation.cjs', 'gpu-readback-page.js', 'browser.html']),
            'All diagnostic source pins included')
    require(all(BASE / name in pinned for name in ['PROTOCOL.md', 'config.json', 'runtime-provenance.json', 'expected.bin', 'source/fixture.wgsl', 'source/FIXTURE.json']), 'All diagnostic input pins included')
    report.update(sourceCommit=source, sourceFreezeSHA256=freeze_sha)
    private = Path(tempfile.mkdtemp(prefix='m31-gpu-readback-private-'))
    REGISTRY = private / 'processes.ndjson'
    with REGISTRY.open('xb'):
        pass
    REGISTRY.chmod(0o600)
    NONCE = os.urandom(16).hex()  # Process authority only; never numerical input.
    RELAY_LOGS = {name: (private / ('relay-' + name + '.bin')).open('xb', buffering=0)
                  for name in ['stdout', 'stderr']}
    env = os.environ.copy()
    env.update(RESEARCH_PROCESS_REGISTRY=str(REGISTRY), RESEARCH_PROCESS_NONCE=NONCE,
               RESEARCH_OBSERVER_PID=str(os.getpid()), RESEARCH_WORK_DEADLINE=str(WORK_END))
    account()
    require(time.monotonic() < WORK_END, 'Work time remains')
    WRAPPER = subprocess.Popen([sys.executable, str(BASE / 'source/run-once.py'), sys.argv[1]],
                               cwd=REPO, env=env, start_new_session=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    WRAPPER_SIGNALABLE = True
    report['wrapperInvocations'] = 1
    selector = selectors.DefaultSelector()
    for name, stream in [('stdout', WRAPPER.stdout), ('stderr', WRAPPER.stderr)]:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, name)
    while time.monotonic() < WORK_END:
        drain(.025)
        account()
        try:
            table = sample()
        except BaseException:
            report['rssProbeErrors'] += 1
            raise
        leader = table.get(WRAPPER.pid)
        require(leader is not None and leader['pgid'] == WRAPPER.pid, 'Unreaped relay leader identity')
        if 'Z' in leader['state']:
            break
    else:
        raise TimeoutError('Work limit')
except BaseException as error:
    problem(error, 'work')
finally:
    # Work is over. The independent hard timer stays armed through final writes.
    signal.signal(signal.SIGALRM, hard_deadline)
    signal.setitimer(signal.ITIMER_REAL, max(.001, START + 60 - time.monotonic()))
    try:
        cleanup()
    except BaseException as error:
        cleanup_problem(error, 'cleanup')
    if selector is not None:
        selector.close()
    if WRAPPER is not None:
        for stream in [WRAPPER.stdout, WRAPPER.stderr]:
            if stream is not None:
                stream.close()
    for handle in RELAY_LOGS.values():
        try:
            handle.close()
        except BaseException as error:
            cleanup_problem(error, 'cleanup-relay-log')

try:
    require(time.monotonic() < CLEANUP_END, 'Cleanup/finalization reserve')
    if REGISTRY is not None:
        private_record = {'entries': PRIVATE_ENTRIES, 'browsers': BROWSERS,
                          'relayPID': WRAPPER.pid if WRAPPER else None}
        data = (json.dumps(private_record, sort_keys=True) + '\n').encode()
        require(len(data) <= 65536, 'Private ownership receipt cap')
        with (REGISTRY.parent / 'cleanup.json').open('xb') as handle:
            require(handle.write(data) == len(data), 'Complete private ownership receipt')
except BaseException as error:
    problem(error, 'private-final-evidence')

closure_complete = report['wrapperReaped'] and report['wrapperGroupAbsent'] \
    and report['wrapperPipeCaptureComplete'] and report['registryComplete'] \
    and all(item['absent'] for item in BROWSERS.values()) and not HELPERS \
    and not report['cleanupErrorObserved']
try:
    require(time.monotonic() < CLEANUP_END, 'Terminal accounting reserve')
    terminal_account = account(reserve=False)
    # A successful scan is final only after every known writer/probe is closed.
    require(closure_complete, 'Output accounting requires complete process closure')
    report.update(terminal_account)
    report['outputAccountingComplete'] = True
except BaseException as error:
    problem(error, 'terminal-output-accounting')

try:
    require(time.monotonic() < CLEANUP_END, 'Final evidence reserve')
    relay = json.loads(read_file(OUT / 'wrapper.json', 8192))
    worker = json.loads(read_file(OUT / 'result.json', 16777216))
    require(relay.get('terminal') is True and relay.get('nodeInvocations') == 1
            and relay.get('nodeReaped') is True and relay.get('pipeCaptureComplete') is True
            and relay.get('errors') == [], 'Complete relay receipt')
    require((OUT / 'diagnostic-stdout.txt').stat().st_size == relay['stdoutBytes']
            and (OUT / 'diagnostic-stderr.txt').stat().st_size == relay['stderrBytes'], 'Exact Node pipe persistence')
    require(worker.get('terminal') is True and worker.get('kind') == 'synthetic-gpu-readback-diagnostic'
            and worker.get('sourceCommit') == report.get('sourceCommit')
            and worker.get('sourceFreezeSHA256') == report.get('sourceFreezeSHA256'),
            'Terminal worker identity')
    report.update(exitCode=relay['nodeExitCode'], reportedDiagnosticQualified=worker.get('qualified'),
                  reportedDiagnosticStatus=worker.get('status'))
    require(report['wrapperExitCode'] == 0 and relay['nodeExitCode'] == 0, 'Actual successful relay/Node exits')
    require(report['wrapperInvocations'] == 1 and report['rssSamples'] > 0 and report['rssProbeErrors'] == 0
            and report['registryComplete'] and report['wrapperReaped'] and report['wrapperGroupAbsent']
            and report['wrapperPipeCaptureComplete'] and all(item['absent'] for item in BROWSERS.values())
            and report['outputAccountingComplete']
            and not report['errors'], 'Whole lifecycle candidate conjunction')
    report['candidateLifecycleVerified'] = True
except BaseException as error:
    problem(error, 'final-evidence')
    report['candidateLifecycleVerified'] = False

report.update(terminal=True, active=False,
              status='closed' if closure_complete else 'terminal-incomplete-closure',
              processClosureComplete=closure_complete,
              registeredDetachedGroups=len(BROWSERS),
              detachedGroupsConfirmedAbsent=sum(item['absent'] for item in BROWSERS.values()),
              detachedGroupKillSignals=sum(item['killSent'] for item in BROWSERS.values()),
              wallSecondsBeforeFinalRecords=time.monotonic() - START,
              rssScope='Sampled direct capture parent, observer, probe children, owned relay/Node/browser groups and observed descendants; shared pages may be counted repeatedly; transient/GPU-driver peaks are not proven bounded.',
              elapsedScope='Observer clock begins before evidence I/O; hard timer remains armed through final records/stdout/exit. Caller must retain actual observer exit and full external elapsed under 60 seconds.')
report['candidateLifecycleVerified'] = report['candidateLifecycleVerified'] and not report['errors']
report.update(budgetBytes=0, observerSummaryBytes=0,
              accountedTotalResultBytes=0 if report['outputAccountingComplete'] else None,
              observedPrefixResultBytes=0,
              outputAccountingScope='Final raw/result/private bytes plus exact budget and summary sizes only when outputAccountingComplete is true; otherwise final totals are null and observedPrefixResultBytes is the last complete scan plus final record sizes, not a final total.')
summary = {}
for _ in range(24):
    budget_bytes = (json.dumps(report, sort_keys=True) + '\n').encode()
    summary = {'kind': 'caller-retained-transport-observer-summary',
               'sourceCommit': report.get('sourceCommit'), 'sourceFreezeSHA256': report.get('sourceFreezeSHA256'),
               'candidateLifecycleVerified': report['candidateLifecycleVerified'], 'wholeLifecycleVerified': False,
               'qualified': False, 'requiresCallerObservedObserverExit0AndElapsedUnder60': True,
               'budgetSHA256': hashlib.sha256(budget_bytes).hexdigest(),
               'budgetBytes': len(budget_bytes), 'summaryBytes': report['observerSummaryBytes'],
               'outputAccountingComplete': report['outputAccountingComplete'],
               'accountedTotalResultBytes': report['accountedTotalResultBytes'],
               'observedPrefixResultBytes': report['observedPrefixResultBytes'],
               'wrapperExitCode': report['wrapperExitCode'], 'errors': report['errors']}
    summary_bytes = (json.dumps(summary, sort_keys=True) + '\n').encode()
    total = report.get('lastObservedRawBytes', 0) + report.get('lastObservedResultDirectoryBytes', 0) + report.get('lastObservedPrivateDiagnosticBytes', 0) \
        + len(budget_bytes) + len(summary_bytes)
    final_total = total if report['outputAccountingComplete'] else None
    if report['budgetBytes'] == len(budget_bytes) and report['observerSummaryBytes'] == len(summary_bytes) \
            and report['accountedTotalResultBytes'] == final_total and report['observedPrefixResultBytes'] == total:
        break
    report.update(budgetBytes=len(budget_bytes), observerSummaryBytes=len(summary_bytes),
                  accountedTotalResultBytes=final_total, observedPrefixResultBytes=total)
else:
    os._exit(125)
if len(budget_bytes) > 32768 or len(summary_bytes) > 8192 or total > RESULT_CAP:
    os._exit(125)
if reserved:
    with (OUT / 'budget.json').open('xb') as handle:
        require(handle.write(budget_bytes) == len(budget_bytes), 'Complete observer budget receipt')
# No uncontrolled print/traceback: one bounded summary, hard timer still active.
if os.write(sys.stdout.fileno(), summary_bytes) != len(summary_bytes):
    os._exit(125)
raise SystemExit(0 if report['candidateLifecycleVerified'] else 1)
