"""Retained group owner for inert qualification children only."""
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import time
case, directory = sys.argv[1:]
folder = Path(directory)
start = time.monotonic()
child = None
released = False

def emit(event, **values):
    with (folder / 'events.jsonl').open('a') as f:
        f.write(json.dumps({'event': event, 'monotonicNs': time.monotonic_ns(), **values}) + '\n')
        f.flush(); os.fsync(f.fileno())

def command(deadline):
    while time.monotonic() < deadline:
        if select.select([sys.stdin], [], [], 0.02)[0]:
            value = sys.stdin.readline()
            if not value: raise RuntimeError('supervisor-disconnected')
            return value.strip()
    raise TimeoutError('guardian-deadline')

def stop(_signum, _frame):
    raise RuntimeError('guardian-signalled')

if not sys.flags.isolated or not sys.dont_write_bytecode or os.getpid() != os.getpgrp():
    sys.exit(12)
signal.signal(signal.SIGTERM, stop)
try:
    with (folder / 'events.jsonl').open('x'): pass
    emit('guardian-start', pid=os.getpid(), pgid=os.getpgrp())
    if case == 'early-guardian-exit':
        emit('early-exit'); released = True; sys.exit(5)
    if case == 'delayed-ready': time.sleep(0.2)
    emit('ready', pid=os.getpid(), pgid=os.getpgrp())
    if command(start + 5) != 'start': raise RuntimeError('wrong-start-command')
    authorization = json.loads((folder / 'authorization.json').read_text())
    if authorization['guardianPid'] != os.getpid(): raise RuntimeError('wrong-authorization')
    child = subprocess.Popen([sys.executable, '-I', '-B', str(Path(__file__).with_name('inert.py')), case, str(folder)])
    emit('child-start', pid=child.pid, guardian=os.getpid())
    while child.poll() is None:
        if time.monotonic() - start > 5: raise TimeoutError('guardian-deadline')
        if select.select([sys.stdin], [], [], 0.02)[0]:
            if sys.stdin.readline() == '': raise RuntimeError('supervisor-disconnected')
            raise RuntimeError('premature-command')
    emit('child-exit', pid=child.pid, exitCode=child.returncode)
    if command(start + 5) != 'release': raise RuntimeError('wrong-release-command')
    released = True
    emit('released')
except Exception as e:
    try: emit('guardian-failure', exception=type(e).__name__, message=str(e))
    except Exception: pass
finally:
    if not released:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        os.killpg(os.getpgrp(), signal.SIGTERM)
        if child and child.poll() is None:
            try: child.wait(timeout=0.2)
            except subprocess.TimeoutExpired: pass
        if child:
            try: emit('cleanup-child-exit', pid=child.pid, exitCode=child.poll())
            except Exception: pass
        os.killpg(os.getpgrp(), signal.SIGKILL)
