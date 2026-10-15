#!/usr/bin/env python3
"""One-shot external supervisor. All artifacts below --directory count toward cap.

No retry or lock removal. Child has 89 s including reads; supervisor has 90 s
from module entry, with 2 MiB reserved within the 32 MiB total output ceiling.
"""
import time
START=time.monotonic()
import argparse, hashlib, json, os, pathlib, resource, selectors, signal, subprocess, sys

CAP=32*1024*1024
RESERVE=2*1024*1024
LOG_CAP=64*1024
WATCHDOG={'process':None,'directory':None}

def hard_deadline(signum,frame):
    process=WATCHDOG['process']; directory=WATCHDOG['directory']
    if process is not None and process.poll() is None:
        try: os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError: pass
    if directory is not None:
        try:
            rows=inventory(directory); base=sum(e['bytes'] for e in rows)
            emergency={'kind':'hard-90-second-terminal-failure','completed':False,'evidenceIntegrityPass':False,'timeout':True,'retryPermitted':False,'outputFiles':len(rows)+1,'outputsBeforeFailure':rows,'totalOutputBytes':base}
            for _ in range(8):
                data=(json.dumps(emergency,sort_keys=True)+'\n').encode(); size=base+len(data)
                if size==emergency['totalOutputBytes']: break
                emergency['totalOutputBytes']=size
            if size<=CAP:
                fd=os.open(directory/'hard-deadline-failure.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                os.write(fd,data); os.close(fd)
        except BaseException: pass
    os._exit(124)

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def inventory(directory):
    rows=[]
    for p in sorted(directory.rglob('*')):
        if p.is_symlink(): raise RuntimeError('symlink in review outputs')
        if p.is_file(): rows.append({'name':str(p.relative_to(directory)),'bytes':p.stat().st_size})
    return rows

def write_exclusive(path,obj):
    data=(json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
    if len(data)>RESERVE//2: raise RuntimeError('failure closure unexpectedly large')
    with open(path,'xb') as f: f.write(data)

def child_limits():
    resource.setrlimit(resource.RLIMIT_FSIZE,(1024*1024,1024*1024))
    os.umask(0o077)

def run():
    parser=argparse.ArgumentParser(); parser.add_argument('--directory',required=True); args=parser.parse_args()
    directory=pathlib.Path(args.directory).resolve()
    WATCHDOG['directory']=directory
    signal.signal(signal.SIGALRM,hard_deadline)
    signal.setitimer(signal.ITIMER_REAL,max(.001,90-(time.monotonic()-START)))
    # The first mutation permanently consumes this sole review attempt.
    with open(directory/'launcher.once.lock','x') as f:
        f.write('Permanent one-attempt saved-review launcher lock; never remove or retry.\n')
    process=None; selector=None; opened=[]; prepared=[]; error=None; timed_out=False; exceeded=False
    child_start=None; child_elapsed=None; killed=False; absent=False; input_index=None
    closure={'kind':'sole-saved-review-external-closure','attempts':1,'retryPermitted':False,'externalWallCapSeconds':90,'subprocessWallCapSeconds':89,'totalOutputCapBytes':CAP,'failureReserveBytes':RESERVE,'terminal':True,'completed':False}
    try:
        prepared_path=directory/'prepared-manifest.json'; prepared_doc=json.loads(prepared_path.read_text()); prepared=prepared_doc['files']
        closure['preparedManifestSHA256']=sha(prepared_path)
        for e in prepared:
            p=directory/e['name']
            if p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']: raise RuntimeError('prepared artifact identity failure')
        known={e['name'] for e in prepared}|{'prepared-manifest.json','launcher.once.lock'}
        if {e['name'] for e in inventory(directory)}!=known: raise RuntimeError('unexpected prelaunch output artifact')
        closure['preparedFilesVerified']=len(prepared)
        argument_path=directory/'arguments.private.json'; arguments=json.loads(argument_path.read_text())
        if arguments['launcherArgv']!=[sys.executable,str(pathlib.Path(__file__).resolve()),'--directory',str(directory)]: raise RuntimeError('exact launcher argument identity failure')
        argv=arguments['checkerArgv']
        if argv[0]!=sys.executable or argv[1]!=str(directory/'checker.py'): raise RuntimeError('checker identity argument failure')
        closure['bindings']={name:sha(directory/name) for name in ('checker.py','launcher.py','input-index.private.json','input-index.public.json','arguments.private.json','arguments.public.json')}
        input_index=json.loads((directory/'input-index.private.json').read_text())
        closure['sourceCommit']=input_index['sourceCommit']; closure['freezeSHA256']=input_index['freezeSHA256']
        closure['scientificTerminalPins']=[{k:e[k] for k in ('group','label','bytes','sha256')} for e in input_index['files'] if (e['group']=='raw' and e['label']=='result.json') or (e['group']=='result' and e['label']=='budget.json')]
        initial=inventory(directory); closure['prelaunchOutputFiles']=len(initial); closure['prelaunchOutputBytes']=sum(e['bytes'] for e in initial)
        if closure['prelaunchOutputBytes']>CAP-RESERVE: raise RuntimeError('prelaunch output cap')
        if time.monotonic()-START>=1: raise RuntimeError('prelaunch preparation consumed launch margin')
        env=dict(os.environ); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONUNBUFFERED']='1'
        child_start=time.monotonic()
        process=subprocess.Popen(argv,cwd=str(directory),env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,preexec_fn=child_limits)
        WATCHDOG['process']=process
        selector=selectors.DefaultSelector(); stored={}; streamed={}
        for name,pipe in [('stdout',process.stdout),('stderr',process.stderr)]:
            handle=open(directory/('checker-'+name+'.log'),'xb'); opened.append(handle); stored[name]=0; streamed[name]=0
            os.set_blocking(pipe.fileno(),False); selector.register(pipe,selectors.EVENT_READ,(name,handle))
        child_deadline=min(child_start+89,START+89.7)
        while process.poll() is None or selector.get_map():
            now=time.monotonic()
            if now>=child_deadline:
                timed_out=True; break
            for key,_ in selector.select(timeout=min(.05,max(0,child_deadline-now))):
                data=os.read(key.fileobj.fileno(),65536)
                if not data: selector.unregister(key.fileobj); key.fileobj.close(); continue
                name,handle=key.data; streamed[name]+=len(data); available=max(0,LOG_CAP-stored[name])
                if available: handle.write(data[:available]); handle.flush(); stored[name]+=min(available,len(data))
                if streamed[name]>LOG_CAP: exceeded=True; break
            if exceeded: break
            if sum(e['bytes'] for e in inventory(directory))>CAP-RESERVE: exceeded=True; break
        if timed_out or exceeded:
            try: os.killpg(process.pid,signal.SIGKILL); killed=True
            except ProcessLookupError: pass
        remaining=max(.001,START+89.9-time.monotonic())
        process.wait(timeout=remaining); child_elapsed=time.monotonic()-child_start
        try: os.killpg(process.pid,0)
        except ProcessLookupError: absent=True
        closure['exitCode']=process.returncode; closure['streamedLogBytes']=streamed; closure['storedLogBytes']=stored
        closure['completed']=process.returncode==0 and not timed_out and not exceeded and absent
    except BaseException as e:
        error={'exceptionClass':type(e).__name__}
        if process is not None and process.poll() is None:
            try: os.killpg(process.pid,signal.SIGKILL); killed=True
            except ProcessLookupError: pass
            try: process.wait(timeout=max(.001,START+89.9-time.monotonic()))
            except BaseException: pass
        if process is not None:
            try: os.killpg(process.pid,0)
            except ProcessLookupError: absent=True
            closure['exitCode']=process.poll()
    finally:
        if selector is not None: selector.close()
        for f in opened: f.close()
        if process is not None:
            for pipe in (process.stdout,process.stderr):
                if pipe is not None and not pipe.closed: pipe.close()
        unchanged=True
        for e in prepared:
            p=directory/e['name']
            if not p.exists() or p.stat().st_size!=e['bytes'] or sha(p)!=e['sha256']: unchanged=False
        closure['preparedArtifactsUnchanged']=unchanged
        closure['timeout']=timed_out; closure['outputCapExceeded']=exceeded
        closure['childProcessGroupKillSent']=killed; closure['childProcessGroupConfirmedAbsent']=absent
        closure['subprocessWallSeconds']=child_elapsed if child_elapsed is not None else (time.monotonic()-child_start if child_start is not None else None)
        closure['error']=error; closure['externalWallSeconds']=time.monotonic()-START
        closure['completed'] &= unchanged and error is None and closure['externalWallSeconds']<90
        report_path=directory/'report.json'
        if report_path.exists():
            closure['reportSHA256']=sha(report_path); closure['reportBytes']=report_path.stat().st_size
            try:
                report=json.loads(report_path.read_text()); closure['evidenceIntegrityPass']=report['evidenceIntegrityPass']; closure['reviewCompleted']=report['completed']
            except BaseException: closure['completed']=False
        else: closure['completed']=False
        # All existing files, archives, locks, logs, private/public indices and exact
        # arguments count, plus the closure's own final serialized byte length.
        rows=inventory(directory); closure['outputsBeforeClosure']=rows
        closure['outputFiles']=len(rows)+1; base_bytes=sum(e['bytes'] for e in rows); total=base_bytes
        for _ in range(8):
            closure['totalOutputBytes']=total
            encoded=(json.dumps(closure,indent=2,sort_keys=True)+'\n').encode()
            updated=base_bytes+len(encoded)
            if updated==total: break
            total=updated
        if total>CAP: raise RuntimeError('total review output cap violated')
        write_exclusive(directory/'runtime.json',closure)
        signal.setitimer(signal.ITIMER_REAL,0)
        print(json.dumps({'completed':closure['completed'],'evidenceIntegrityPass':closure.get('evidenceIntegrityPass'),'externalWallSeconds':closure['externalWallSeconds'],'totalOutputBytes':total,'timeout':timed_out,'outputCapExceeded':exceeded,'error':error},sort_keys=True))
    return 0 if closure['completed'] else 1

if __name__=='__main__': sys.exit(run())
