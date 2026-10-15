"""Sole external launcher for the independently prepared saved-only checker."""
import hashlib, json, os, pathlib, resource, shutil, signal, subprocess, sys, time

START=time.perf_counter()
ROOT=pathlib.Path(__file__).resolve().parent
MANIFEST_SHA='daa47238ece6bec85e8281f5dc03072aad64629fee092d10f10aa36c60cd392e'
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

manifest=ROOT/'invocation.json'
if sha(manifest)!=MANIFEST_SHA:raise SystemExit('Prospective invocation identity mismatch')
m=json.loads(manifest.read_text())
for name in ['checker','preparation','inputIndex','pythonExecutable']:
    p=pathlib.Path(m[name]['path'])
    if p.stat().st_size!=m[name]['bytes'] or sha(p)!=m[name]['sha256']:
        raise SystemExit('Prospective input identity mismatch: '+name)
with (ROOT/'sole-launch.lock').open('x') as f:f.write('One saved-review attempt reserved permanently; no retry.\n')
archive=ROOT/'launch';archive.mkdir()
for source,name in [(manifest,'invocation.json'),(ROOT/'checker.py','checker.py'),(ROOT/'preparation.md','preparation.md'),(ROOT/'input-index.json','input-index.json'),(pathlib.Path(__file__),'launcher.py')]:
    shutil.copyfile(source,archive/name)
args=[m['executable']]+m['argv'];(archive/'arguments.json').write_text(json.dumps(args,indent=2)+'\n')
record={'terminal':False,'active':True,'attempts':1,'externalWallCapSeconds':60,'subprocessCapSeconds':59,'outputCapBytes':16777216,'failureReserveBytes':2097152,'retryPermitted':False}
status_path=archive/'runtime.json';status_path.write_text(json.dumps(record,indent=2)+'\n')
p=None
def output_bytes():
    # Include every newly emitted archive copy, arguments, logs and runtime
    # record, plus the report and both permanent locks. Runtime appears only
    # through the archive traversal, so it is never counted twice.
    paths=list(archive.iterdir())+[ROOT/'review.json',ROOT/'sole-launch.lock',ROOT/'checker.lock']
    return sum(p.stat().st_size for p in paths if p.is_file())
def restrict_files():
    resource.setrlimit(resource.RLIMIT_FSIZE,(14*1024*1024,14*1024*1024))
try:
    with (archive/'stdout.txt').open('x') as stdout,(archive/'stderr.txt').open('x') as stderr:
        p=subprocess.Popen(args,stdout=stdout,stderr=stderr,start_new_session=True,preexec_fn=restrict_files)
        child_start=time.perf_counter();record['timeout']=False;record['outputCapExceeded']=False
        while p.poll() is None:
            elapsed=time.perf_counter()-START
            if elapsed>=59 or time.perf_counter()-child_start>=59 or output_bytes()>14*1024*1024:
                record['timeout']=elapsed>=59 or time.perf_counter()-child_start>=59
                record['outputCapExceeded']=output_bytes()>14*1024*1024
                os.killpg(p.pid,signal.SIGKILL)
                p.wait(timeout=.5)
                break
            time.sleep(.02)
        record['exitCode']=p.returncode
except BaseException as error:
    record['launchError']={'type':type(error).__name__,'message':str(error)[:2000]}
    if p is not None and p.poll() is None:
        try:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=.5)
        except BaseException as cleanup:record['cleanupError']=type(cleanup).__name__
finally:
    group_absent=p is None
    if p is not None:
        try:os.killpg(p.pid,0)
        except ProcessLookupError:group_absent=True
        except OSError as error:record['groupProbeError']=type(error).__name__
    record.update(terminal=True,active=False,wallSeconds=time.perf_counter()-START,checkerUnchangedAfter=sha(ROOT/'checker.py')==m['checker']['sha256'],inputIndexUnchangedAfter=sha(ROOT/'input-index.json')==m['inputIndex']['sha256'],groupConfirmedAbsent=group_absent)
    record['outputBytesBeforeRuntime']=output_bytes()
    record['qualifiedReviewClosure']=record.get('exitCode')==0 and not record.get('timeout') and not record.get('outputCapExceeded') and not record.get('launchError') and group_absent and record['checkerUnchangedAfter'] and record['inputIndexUnchangedAfter'] and record['wallSeconds']<60 and record['outputBytesBeforeRuntime']<16777216-8192
    status_path.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'archive':str(archive),'runtime':record}))
raise SystemExit(0 if record['qualifiedReviewClosure'] else 1)
