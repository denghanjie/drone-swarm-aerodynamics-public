"""Retain the session leader until the supervisor acknowledges child exit."""
import json,os,select,signal,subprocess,sys,time
from pathlib import Path
from datetime import datetime
events=Path(os.environ['RESEARCH_GUARD_EVENTS'])
deadline={'kernel':610,'checker':610}[os.environ['RESEARCH_SUPERVISION_STAGE']]
def emit(record):
    with events.open('a') as f:f.write(json.dumps(record)+'\n');f.flush();os.fsync(f.fileno())
if not sys.flags.isolated:raise RuntimeError('Guardian requires Python isolated mode')
if os.environ.get('NODE_OPTIONS') or os.environ.get('NODE_PATH'):raise RuntimeError('Node preload environment refused')
child=None;start=time.monotonic()
def stopping(_signum,_frame):raise RuntimeError('guardian signalled')
signal.signal(signal.SIGTERM,stopping)
try:
    with events.open('x') as f:f.flush();os.fsync(f.fileno())
    directory_fd=os.open(events.parent,os.O_RDONLY)
    try:os.fsync(directory_fd)
    finally:os.close(directory_fd)
    cutoff=datetime.fromisoformat('2026-10-16T23:00:00+00:00').timestamp()
    if time.time()>=cutoff:raise RuntimeError('scientific launch cutoff')
    child=subprocess.Popen(json.loads(os.environ['RESEARCH_CHILD_COMMAND']))
    emit({'event':'child-start','pid':child.pid,'guardian':os.getpid()})
    while child.poll() is None:
        if time.monotonic()-start>deadline:raise RuntimeError('guardian timeout')
        if select.select([sys.stdin],[],[],0.05)[0] and sys.stdin.readline()=='':raise RuntimeError('supervisor disconnected')
    emit({'event':'child-exit','pid':child.pid,'exitCode':child.returncode})
    while time.monotonic()-start<=deadline:
        if select.select([sys.stdin],[],[],0.05)[0]:
            if sys.stdin.readline().strip()=='release':sys.exit(0)
            raise RuntimeError('supervisor disconnected')
    raise RuntimeError('release timeout')
except Exception as e:
    try:emit({'event':'guardian-failure','reason':type(e).__name__})
    except Exception:pass
    sys.exit(1)
finally:
    # Cleanup cannot depend on a successful lifecycle journal write.
    signal.signal(signal.SIGTERM,signal.SIG_IGN)
    if child and child.poll() is None:
        child.terminate()
        try:child.wait(timeout=1)
        except subprocess.TimeoutExpired:child.kill();child.wait(timeout=1)
