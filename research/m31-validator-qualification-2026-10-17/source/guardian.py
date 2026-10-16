"""Retain the process-group leader through qualified saved-only child closure."""
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
if os.environ.get('RESEARCH_SUPERVISION_STAGE') != 'qualification':
    raise RuntimeError('Wrong supervision stage')
if os.environ.get('NODE_OPTIONS') or os.environ.get('NODE_PATH'):
    raise RuntimeError('Node preload environment refused')
events = Path(os.environ['RESEARCH_GUARD_EVENTS'])
deadline = 610
child = None
start = time.monotonic()


def emit(record):
    with events.open('a') as stream:
        stream.write(json.dumps(record) + '\n'); stream.flush(); os.fsync(stream.fileno())


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
        raise RuntimeError('Qualification launch cutoff reached')
    child = subprocess.Popen(json.loads(os.environ['RESEARCH_CHILD_COMMAND']))
    emit({'event': 'child-start', 'pid': child.pid, 'guardian': os.getpid()})
    while child.poll() is None:
        if time.monotonic() - start > deadline: raise RuntimeError('Guardian timeout')
        if select.select([sys.stdin], [], [], 0.05)[0] and sys.stdin.readline() == '':
            raise RuntimeError('Supervisor disconnected')
    emit({'event': 'child-exit', 'pid': child.pid, 'exitCode': child.returncode})
    while time.monotonic() - start <= deadline:
        if select.select([sys.stdin], [], [], 0.05)[0]:
            if sys.stdin.readline().strip() == 'release': sys.exit(0)
            raise RuntimeError('Supervisor disconnected')
    raise RuntimeError('Release timeout')
except Exception as error:
    try: emit({'event': 'guardian-failure', 'reason': type(error).__name__})
    except Exception: pass
    sys.exit(1)
finally:
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    if child and child.poll() is None:
        child.terminate()
        try: child.wait(timeout=1)
        except subprocess.TimeoutExpired:
            child.kill(); child.wait(timeout=1)
