"""Ready-gated retained group owner; scientific spawn needs observed-leader authorization."""
import json
import os
from pathlib import Path
import re
import select
import signal
import subprocess
import sys
import time
from datetime import datetime

CUTOFF = '2026-10-17T01:00:00Z'
if not sys.flags.isolated or not sys.dont_write_bytecode:
    raise RuntimeError('Guardian requires Python -I -B')
stage = os.environ.get('RESEARCH_SUPERVISION_STAGE')
if stage not in {'kernel', 'checker'}:
    raise RuntimeError('Wrong supervision stage')
if os.environ.get('RESEARCH_EXECUTION_CONTEXT') != 'tool-require-escalated':
    raise RuntimeError('Explicit escalated execution context required')
if os.environ.get('NODE_OPTIONS') or os.environ.get('NODE_PATH'):
    raise RuntimeError('Node preload environment refused')
if os.getpid() != os.getpgrp():
    raise RuntimeError('Guardian must own its new process group')
events = Path(os.environ['RESEARCH_GUARD_EVENTS'])
authorization_path = Path(os.environ['RESEARCH_GUARD_AUTHORIZATION'])
child = None
released = False
start = time.monotonic()


def emit(event, **values):
    timestamp = time.monotonic_ns()
    with events.open('a') as stream:
        stream.write(json.dumps({'event': event, 'monotonicNs': timestamp, **values}, allow_nan=False) + '\n')
        stream.flush(); os.fsync(stream.fileno())
    return timestamp


def command():
    while time.monotonic() - start <= 610:
        if select.select([sys.stdin], [], [], 0.05)[0]:
            value = sys.stdin.readline()
            if not value:
                raise RuntimeError('supervisor-disconnected')
            return value.strip()
    raise RuntimeError('guardian-timeout')


def stopping(_signal, _frame):
    raise RuntimeError('guardian-signalled')


def clean(value):
    value = str(value).replace(str(Path(__file__).resolve().parents[3]), 'REPOSITORY_ROOT')
    value = value.replace(os.environ.get('RESEARCH_PRIVATE_RUN_DIR', '__UNSET_PRIVATE__'), 'PRIVATE_RUN_DIR')
    value = value.replace(str(Path.home()), 'USER_HOME').replace(sys.executable, 'PYTHON_EXECUTABLE')
    value = re.sub(r'/private/var/folders/[^\s\"\']+', 'PRIVATE_TEMP_PATH', value)
    return value[:256]


signal.signal(signal.SIGTERM, stopping)
try:
    with events.open('x') as stream:
        stream.flush(); os.fsync(stream.fileno())
    fd = os.open(events.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    emit('guardian-start', pid=os.getpid(), pgid=os.getpgrp())
    ready_ns = emit('ready', pid=os.getpid(), pgid=os.getpgrp())
    if command() != 'start':
        raise RuntimeError('wrong-start-command')
    if (authorization_path.parent != events.parent or authorization_path.name != stage + '-authorization.json'
            or authorization_path.is_symlink() or not authorization_path.is_file()
            or authorization_path.stat().st_size > 65536):
        raise RuntimeError('invalid-authorization-path')
    authorization = json.loads(authorization_path.read_bytes())
    expected = {'stage': stage, 'sourceCommit': os.environ['RESEARCH_SOURCE_COMMIT'],
                'sourceManifestSha256': os.environ['RESEARCH_EXPECTED_MANIFEST_SHA256'],
                'configSha256': os.environ['RESEARCH_CONFIG_SHA256'], 'launchCutoffUtc': CUTOFF,
                'executionContext': 'tool-require-escalated', 'guardianPid': os.getpid(),
                'supervisorPid': os.getppid(), 'leaderSampleObserved': True}
    leader = authorization.get('leaderObservation', {})
    authorized_ns = authorization.get('monotonicNs')
    observed_ns = leader.get('monotonicNs')
    if (any(authorization.get(k) != v for k, v in expected.items())
            or leader.get('pid') != os.getpid() or leader.get('pgid') != os.getpgrp()
            or leader.get('ppid') != os.getppid() or type(leader.get('rssKiB')) is not int or leader['rssKiB'] <= 0
            or type(authorized_ns) is not int or type(observed_ns) is not int
            or not ready_ns <= observed_ns <= authorized_ns <= time.monotonic_ns()):
        raise RuntimeError('wrong-authorization')
    child_command = json.loads(os.environ['RESEARCH_CHILD_COMMAND'])
    if time.monotonic() - start > 610:
        raise RuntimeError('guardian-timeout')
    # This is the last check immediately before the scientific child can be spawned.
    if time.time() >= datetime.fromisoformat(CUTOFF.replace('Z', '+00:00')).timestamp():
        raise RuntimeError('scientific-launch-cutoff')
    child = subprocess.Popen(child_command)
    emit('child-start', pid=child.pid, guardian=os.getpid(), authorizationMonotonicNs=authorized_ns)
    while child.poll() is None:
        if time.monotonic() - start > 610:
            raise RuntimeError('guardian-timeout')
        if select.select([sys.stdin], [], [], 0.05)[0]:
            if not sys.stdin.readline():
                raise RuntimeError('supervisor-disconnected')
            raise RuntimeError('premature-command')
    emit('child-exit', pid=child.pid, exitCode=child.returncode)
    if command() != 'release':
        raise RuntimeError('wrong-release-command')
    emit('released')
    released = True
except Exception as error:
    try: emit('guardian-failure', exception=type(error).__name__, reason=clean(error))
    except Exception: pass
finally:
    if not released:
        # This live group leader owns the ID; include any inherited-group worker.
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        os.killpg(os.getpgrp(), signal.SIGTERM)
        if child and child.poll() is None:
            try: child.wait(timeout=1)
            except subprocess.TimeoutExpired: pass
        if child:
            try: emit('cleanup-child-exit', pid=child.pid, exitCode=child.poll())
            except Exception: pass
        os.killpg(os.getpgrp(), signal.SIGKILL)
