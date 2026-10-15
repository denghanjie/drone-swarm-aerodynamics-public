#!/usr/bin/env python3
import hashlib,json,os,pathlib,resource,selectors,signal,stat,subprocess,sys,time

t0=time.monotonic(); cpu0=time.process_time()
base=pathlib.Path(__file__).resolve().parent; root=base.parent
phase=sys.argv[1] if len(sys.argv)==2 else ''
if phase != 'screen': sys.exit('Invalid phase')
cap=20
outcap=300000
pfx=base/('execution-'+phase)
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_text())
def size():
    n=0
    for d in (base,):
        for p in d.rglob('*'):
            try: s=p.lstat()
            except FileNotFoundError: continue
            if stat.S_ISLNK(s.st_mode): raise RuntimeError('Symlink in budget scope')
            if stat.S_ISREG(s.st_mode): n+=s.st_size
    return n
def write(suffix,data):
    with pathlib.Path(str(pfx)+suffix).open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
def encode(v): return (json.dumps(v,sort_keys=True)+'\n').encode()
if any(base.glob('execution-'+phase+'*')): sys.exit('Prior execution; retry refused')
freeze=base/'FREEZE.json'; release=load(base/('RELEASE-'+phase+'.json'))
fh=digest(freeze)
if (release.get('status')!='RELEASED' or release.get('phase')!=phase
    or release.get('freezeSha256')!=fh): sys.exit('Release binding invalid')
seen=set()
for item in load(freeze)['files']:
    p=root/item['path']; rel=p.relative_to(root).as_posix()
    if (p.resolve()!=p or not p.is_file() or rel in seen
        or digest(p)!=item['sha256']): sys.exit('Frozen hash failed')
    seen.add(rel)
for p in (pathlib.Path(__file__).resolve(),base/'run-predictor.cjs'):
    if p.relative_to(root).as_posix() not in seen: sys.exit('Launcher not frozen')
rem=release.get('globalRemainingBytes'); initial=size()
if (type(rem)!=int or rem<outcap+20000
    or initial+outcap+20000>500000): sys.exit('Byte budget failed')
if time.monotonic()-t0>=cap-2: sys.exit('Preflight timed out')
write('-started.json',encode({'phase':phase,'freezeSha256':fh,'wallCapSeconds':cap,
    'childCpuHardLimitSeconds':cap-2,'supervisorCpuHardLimitSeconds':2,'initialBytes':initial,'phaseOutputCapBytes':outcap}))
p=None; reason=None; sent=None; logs=[bytearray(),bytearray()]; counts=[0,0]
before=resource.getrusage(resource.RUSAGE_CHILDREN)
def limit(): resource.setrlimit(resource.RLIMIT_CPU,(cap-2,cap-2))
def stop(sig):
    try: p.send_signal(sig)
    except ProcessLookupError: pass
try:
    env=os.environ.copy(); env['PREDICTOR_SUPERVISED']=phase
    p=subprocess.Popen(['node','run-predictor.cjs',phase],cwd=base,env=env,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        preexec_fn=limit)
    def parent_cpu(_s,_f): raise RuntimeError('supervisor_cpu_limit')
    signal.signal(signal.SIGXCPU,parent_cpu)
    resource.setrlimit(resource.RLIMIT_CPU,(1,2))
    sel=selectors.DefaultSelector()
    for i,f in enumerate((p.stdout,p.stderr)):
        os.set_blocking(f.fileno(),False); sel.register(f,selectors.EVENT_READ,i)
    while sel.get_map() or p.poll() is None:
        elapsed=time.monotonic()-t0
        if reason is None and (elapsed>=cap-2 or size()>480000):
            reason='wall_timeout' if elapsed>=cap-2 else 'byte_budget'
            stop(signal.SIGTERM); sent=elapsed
        if sent is not None and (elapsed>=cap-1 or elapsed-sent>=0.5):
            stop(signal.SIGKILL)
        for key,_ in sel.select(0.05):
            chunk=os.read(key.fileobj.fileno(),65536); i=key.data
            if not chunk: sel.unregister(key.fileobj); key.fileobj.close()
            else:
                counts[i]+=len(chunk); logs[i].extend(chunk[:max(0,8192-len(logs[i]))])
        if elapsed>=cap-0.5:
            stop(signal.SIGKILL); break
    p.wait(timeout=max(0.01,cap-0.25-(time.monotonic()-t0)))
except BaseException as e:
    reason=reason or type(e).__name__
    if p is not None:
        stop(signal.SIGKILL)
        try: p.wait(timeout=0.1)
        except subprocess.TimeoutExpired: pass
after=resource.getrusage(resource.RUSAGE_CHILDREN)
for suffix,data in zip(('.stdout.txt','.stderr.txt'),logs): write(suffix,data)
write('-receipt.json',encode({'phase':phase,'freezeSha256':fh,
    'returncode':None if p is None else p.returncode,'reason':reason,
    'timedout':reason=='wall_timeout','wallSecondsBeforeReceipt':time.monotonic()-t0,
    'childCpuSeconds':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
    'supervisorCpuSeconds':time.process_time()-cpu0,'cpuLimiter':'RLIMIT_CPU: child cap-2, supervisor hard2/soft1; driver creates no descendants',
    'childCpuHardLimitSeconds':cap-2,'supervisorCpuHardLimitSeconds':2,'cpuLimiterApplied':p is not None,
    'stdoutBytesRead':counts[0],'stderrBytesRead':counts[1],
    'truncated':[n>8192 for n in counts],'bytesBeforeReceipt':size()}))
sys.exit(0 if p is not None and p.returncode==0 and reason is None else 1)
