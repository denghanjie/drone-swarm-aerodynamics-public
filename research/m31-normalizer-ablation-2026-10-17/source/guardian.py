"""Retain the group leader until closure is acknowledged; kill owned group on failure."""
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import time
from datetime import datetime

if not sys.flags.isolated or not sys.dont_write_bytecode:
    raise RuntimeError('Guardian requires Python -I -B')
if os.environ.get('RESEARCH_SUPERVISION_STAGE') not in {'kernel', 'checker'}:
    raise RuntimeError('Wrong supervision stage')
if os.environ.get('NODE_OPTIONS') or os.environ.get('NODE_PATH'):
    raise RuntimeError('Node preload environment refused')
if os.getpid() != os.getpgrp():
    raise RuntimeError('Guardian must own its new process group')
events = Path(os.environ['RESEARCH_GUARD_EVENTS'])
child = None
released = False
start = time.monotonic()


def emit(value):
    with events.open('a') as stream:
        stream.write(json.dumps(value) + '\n'); stream.flush(); os.fsync(stream.fileno())


def stopping(_signal, _frame):
    raise RuntimeError('Guardian signalled')


signal.signal(signal.SIGTERM, stopping)
try:
    with events.open('x') as stream:
        stream.flush(); os.fsync(stream.fileno())
    fd = os.open(events.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    if time.time() >= datetime.fromisoformat('2026-10-16T23:00:00+00:00').timestamp():
        raise RuntimeError('Scientific launch cutoff reached')
    child = subprocess.Popen(json.loads(os.environ['RESEARCH_CHILD_COMMAND']))
    emit({'event': 'child-start', 'pid': child.pid, 'guardian': os.getpid()})
    while child.poll() is None:
        if time.monotonic() - start > 610:
            raise RuntimeError('Guardian timeout')
        if select.select([sys.stdin], [], [], 0.05)[0] and sys.stdin.readline() == '':
            raise RuntimeError('Supervisor disconnected')
    emit({'event': 'child-exit', 'pid': child.pid, 'exitCode': child.returncode})
    while time.monotonic() - start <= 610:
        if select.select([sys.stdin], [], [], 0.05)[0]:
            if sys.stdin.readline().strip() == 'release':
                released = True
                break
            raise RuntimeError('Supervisor disconnected')
    if not released:
        raise RuntimeError('Release timeout')
except Exception as error:
    try: emit({'event': 'guardian-failure', 'reason': type(error).__name__})
    except Exception: pass
finally:
    if not released:
        # The current process remains the live group leader, so this ID cannot be reused.
        # Include a runner's inherited-group worker even if the runner already exited.
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        os.killpg(os.getpgrp(), signal.SIGTERM)
        if child and child.poll() is None:
            try: child.wait(timeout=1)
            except subprocess.TimeoutExpired: pass
        # Kill the whole still-owned group, including this guardian, on every failure.
        os.killpg(os.getpgrp(), signal.SIGKILL)
