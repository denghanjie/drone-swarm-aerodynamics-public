"""One 240-second outer viewer-QA attempt; direct child handling only."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import resource
import subprocess
import time

out = Path(__file__).resolve().parent
started = time.monotonic()
node = os.environ['RESEARCH_NODE']
required = ['RESEARCH_ROOT', 'RESEARCH_CHROME', 'NODE_PATH']
assert all(os.environ.get(key) for key in required)
assert not (out / 'report.json').exists()
marker = {'schema': 'm31-native-viewer-qa-attempt-v1', 'attempt': 2,
          'startedUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'resourceScope': '240 s outer wall; 32 MiB aggregate QA artifacts and per-file child limit; no enforced memory ceiling; direct child handles, no process-group signals',
          'status': 'started', 'newScientificCalls': 0,
          'sourceFiles': [{'path': name, 'bytes': (out / name).stat().st_size,
                           'sha256': hashlib.sha256((out / name).read_bytes()).hexdigest()}
                          for name in ['run.cjs', 'supervise.py']]}
with (out / 'STARTED.json').open('x') as stream:
    stream.write(json.dumps(marker, indent=2) + '\n')
def limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (32 * 1024 * 1024, 32 * 1024 * 1024))
child = subprocess.Popen([node, str(out / 'run.cjs')], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         cwd=os.environ['RESEARCH_ROOT'], env=os.environ.copy(), preexec_fn=limits,
                         start_new_session=False)
supervisor_failure = None
try:
    stdout, stderr = child.communicate(timeout=230)
except subprocess.TimeoutExpired:
    supervisor_failure = '230-second child timeout; requested direct-child graceful termination'
    child.terminate()
    try:
        stdout, stderr = child.communicate(timeout=8)
    except subprocess.TimeoutExpired:
        child.kill()
        stdout, stderr = child.communicate(timeout=1)
def clean(raw):
    text = raw.decode('utf8', errors='replace')
    for key in ['RESEARCH_ROOT', 'RESEARCH_NODE', 'RESEARCH_CHROME', 'NODE_PATH', 'HOME']:
        if os.environ.get(key):
            text = text.replace(os.environ[key], '[PRIVATE_PATH]')
    return text[:12000]
elapsed = time.monotonic() - started
report_path = out / 'report.json'
report = json.loads(report_path.read_bytes()) if report_path.exists() else {}
total = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
sources_unchanged = all((out / pin['path']).stat().st_size == pin['bytes'] and
                        hashlib.sha256((out / pin['path']).read_bytes()).hexdigest() == pin['sha256']
                        for pin in marker['sourceFiles'])
passed = child.returncode == 0 and supervisor_failure is None and report.get('passed') is True and elapsed <= 240 and total < 32 * 1024 * 1024 and sources_unchanged
record = {**marker, 'status': 'completed' if passed else 'failed', 'exitCode': 0 if passed else 1,
          'childExitCode': child.returncode, 'childReaped': child.poll() is not None, 'qaSourcesUnchanged': sources_unchanged,
          'wallSeconds': elapsed, 'outputBytesBeforeAttemptRecord': total,
          'firstFailure': supervisor_failure or report.get('failure'),
          'stdout': clean(stdout), 'stderr': clean(stderr),
          'report': {'bytes': report_path.stat().st_size, 'sha256': hashlib.sha256(report_path.read_bytes()).hexdigest()} if report_path.exists() else None}
with (out / 'attempt.json').open('x') as stream:
    stream.write(json.dumps(record, indent=2) + '\n')
print(json.dumps({'status': record['status'], 'childExitCode': child.returncode,
                  'wallSeconds': elapsed, 'firstFailure': record['firstFailure']}))
raise SystemExit(record['exitCode'])
