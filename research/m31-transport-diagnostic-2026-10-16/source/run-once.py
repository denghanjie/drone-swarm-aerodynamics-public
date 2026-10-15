"""Single Node relay; the parent observer owns the entire 60-second envelope."""
import time
START = time.monotonic()
import os, sys, json, signal, selectors, subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PIPE_CAP = 65536
node = None
selector = None
handles = []
record = {'kind': 'single-transport-relay', 'nodeInvocations': 0, 'nodeExitCode': None,
          'nodeReaped': False, 'pipeCaptureComplete': False, 'pipeByteCapTotal': PIPE_CAP,
          'stdoutBytes': 0, 'stderrBytes': 0, 'stdoutObservedBytes':0, 'stderrObservedBytes':0, 'errors': [], 'terminal': False,
          'externalObserverRequired': True, 'qualified': False}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def append(entry):
    entry.update(version=1, nonce=os.environ['RESEARCH_PROCESS_NONCE'])
    data = (json.dumps(entry, separators=(',', ':')) + '\n').encode()
    require(len(data) <= 8192, 'Registry entry cap')
    fd = os.open(os.environ['RESEARCH_PROCESS_REGISTRY'], os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW)
    try:
        require(os.write(fd, data) == len(data), 'Complete registry append')
    finally:
        os.close(fd)

try:
    require(len(sys.argv) == 2 and Path(sys.argv[1]).is_absolute(), 'One absolute Node executable')
    require(os.getppid() == int(os.environ['RESEARCH_OBSERVER_PID']), 'Direct observer parent')
    require(os.getpgrp() == os.getpid(), 'Observer-created relay session')
    deadline = float(os.environ['RESEARCH_WORK_DEADLINE'])
    require(time.monotonic() < deadline, 'Work deadline')
    args = [sys.argv[1], str(BASE / 'source/diagnostic.cjs')]
    append({'phase': 'node-intent', 'id': 'node', 'detached': False,
            'ownership': {'executable': args[0], 'arguments': args[1:]}})
    # Node deliberately stays in the directly owned relay group. If registration
    # is interrupted, the observer still owns the group containing the new child.
    node = subprocess.Popen(args, cwd=BASE.parents[1], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=False)
    record['nodeInvocations'] = 1
    append({'phase': 'node-spawned', 'id': 'node', 'pid': node.pid,
            'pgid': os.getpgrp(), 'detached': False})
    selector = selectors.DefaultSelector()
    for name, stream in [('stdout', node.stdout), ('stderr', node.stderr)]:
        handle = (BASE / 'results' / ('diagnostic-' + name + '.txt')).open('xb', buffering=0)
        handles.append(handle)
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ, (name, handle))
    while selector.get_map() or node.poll() is None:
        left = deadline - time.monotonic()
        require(left > 0, 'Relay work deadline')
        for key, _ in selector.select(min(.025, left)):
            name, handle = key.data
            remaining = PIPE_CAP - record['stdoutBytes'] - record['stderrBytes']
            try:
                chunk = os.read(key.fileobj.fileno(), min(4096, remaining + 1))
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(key.fileobj)
                continue
            record[name + 'ObservedBytes'] += len(chunk)
            retained = chunk[:max(0, remaining)]
            written = handle.write(retained)
            record[name + 'Bytes'] += written
            require(written == len(retained), 'Complete Node pipe write')
            require(len(retained) == len(chunk), 'Node combined pipe cap')
    node.wait(timeout=max(.001, min(.05, deadline - time.monotonic())))
    record.update(nodeExitCode=node.returncode, nodeReaped=True, pipeCaptureComplete=True)
except BaseException as error:
    record['errors'].append({'type': type(error).__name__})
finally:
    if node is not None and node.poll() is None:
        node.kill()  # Direct unreaped child only; browser cleanup belongs to observer.
        try:
            node.wait(timeout=.05)
        except subprocess.TimeoutExpired:
            record['errors'].append({'type': 'NodeReapTimeout'})
    if node is not None:
        record.update(nodeExitCode=node.returncode, nodeReaped=node.returncode is not None)
        for stream in [node.stdout, node.stderr]:
            if stream is not None:
                stream.close()
    if selector is not None:
        selector.close()
    for handle in handles:
        handle.close()

record['terminal'] = True
record['wallSecondsBeforeReceipt'] = time.monotonic() - START
encoded = (json.dumps(record, sort_keys=True) + '\n').encode()
require(len(encoded) <= 8192, 'Relay receipt cap')
with (BASE / 'results/wrapper.json').open('xb') as handle:
    require(handle.write(encoded) == len(encoded), 'Complete relay receipt write')
# The observer must observe this actual exit; this receipt alone cannot pass.
raise SystemExit(0 if record['nodeInvocations'] == 1 and record['nodeExitCode'] == 0
                 and record['nodeReaped'] and record['pipeCaptureComplete']
                 and not record['errors'] else 1)
