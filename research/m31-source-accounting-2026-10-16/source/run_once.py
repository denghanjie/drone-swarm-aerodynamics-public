"""External wall bound for the sole fresh CPU audit; no process-table probing."""
import sys, os, signal, subprocess, time, json
from pathlib import Path

base=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2: raise ValueError('Supply Node executable')
with (base/'execution.lock').open('x') as stream:
    stream.write('Sole source-accounting invocation reserved.\n')
start=time.perf_counter()
p=None; stdout=b''; stderr=b''; timed_out=False; incomplete=False; error_type=None
try:
    p=subprocess.Popen([sys.executable,'-B',str(base/'source/audit.py'),sys.argv[1]],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:
        stdout,stderr=p.communicate(timeout=29)
    except subprocess.TimeoutExpired as error:
        timed_out=True
        stdout=error.output or b''; stderr=error.stderr or b''
        try:
            os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError as error:
            error_type=type(error).__name__; incomplete=True
        try:
            stdout,stderr=p.communicate(timeout=1)
        except subprocess.TimeoutExpired as error:
            stdout=error.output or stdout; stderr=error.stderr or stderr
            incomplete=True
except OSError as error:
    error_type=type(error).__name__; incomplete=True
elapsed=time.perf_counter()-start
code=p.poll() if p is not None else None
if p is not None:
    for stream in (p.stdout,p.stderr):
        if stream is not None: stream.close()
(base/'results/driver-stdout.txt').write_bytes(stdout)
(base/'results/driver-stderr.txt').write_bytes(stderr)
receipt={'workerExitCode':code,'timeout':timed_out,'cleanupIncomplete':incomplete,
 'errorType':error_type,'externalWorkerSeconds':elapsed,'within30SecondCeiling':elapsed<30,
 'stdoutBytes':len(stdout),'stderrBytes':len(stderr),'pipeCaptureComplete':not incomplete,
 'scope':'Direct worker completion and pipes; no claim of universal OS process observation'}
with (base/'results/execution.json').open('x') as stream:
    json.dump(receipt,stream,indent=2);stream.write('\n')
print(json.dumps(receipt))
raise SystemExit(0 if code==0 and not timed_out and not incomplete and elapsed<30 else 1)
