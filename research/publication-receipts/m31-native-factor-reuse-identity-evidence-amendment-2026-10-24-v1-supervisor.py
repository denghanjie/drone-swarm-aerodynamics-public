"""Single-use outer lifecycle supervisor; run only after reviewed public amendment."""
from pathlib import Path
import argparse,hashlib,json,os,resource,signal,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[2]
PREFIX='research/publication-receipts/m31-native-factor-reuse-identity-evidence-amendment-2026-10-24-v1'
START=time.monotonic();CHILD=None
if sys.flags.optimize:raise SystemExit('Python optimization is forbidden: closure assertions must remain active.')
p=argparse.ArgumentParser();p.add_argument('--publication-commit',required=True);p.add_argument('--protocol-sha256',required=True);p.add_argument('--review-file',required=True);p.add_argument('--review-sha256',required=True);a=p.parse_args()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def atomic(path,d):
    tmp=Path(str(path)+'.tmp');
    with tmp.open('w') as f:json.dump(d,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def killgroup():
    if CHILD:
        try:os.killpg(CHILD.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        try:CHILD.wait(timeout=3)
        except subprocess.TimeoutExpired:pass
        try:os.killpg(CHILD.pid,0);return False
        except ProcessLookupError:return True
    return True
def alarm(signum,frame):
    killgroup();os._exit(124)  # Initial durable unknown record remains non-authorizing.
signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,597)
lock=ROOT/(PREFIX+'-launch.lock');outer=ROOT/(PREFIX+'-supervisor-receipt.json')
fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.write(fd,b'Single administrative verifier attempt; incomplete until sealed.\n');os.fsync(fd);os.close(fd)
if outer.exists():raise RuntimeError('supervisor-output-already-exists')
atomic(outer,{'passed':False,'closed':False,'status':'incomplete-or-unknown','scientificExecution':False,'publicationCommit':a.publication_commit})
error=None;rc=None;closed=False;receipt=None;sealed=[]
try:
    pb=(ROOT/(PREFIX+'-protocol.json')).read_bytes();assert hashlib.sha256(pb).hexdigest()==a.protocol_sha256
    protocol=json.loads(pb)
    for pin in protocol['sourceFiles']:
        b=(ROOT/pin['file']).read_bytes();assert identity(b)=={k:pin[k] for k in ['bytes','sha256']}
    stdout=ROOT/(PREFIX+'-supervisor.stdout');stderr=ROOT/(PREFIX+'-supervisor.stderr')
    def limit():resource.setrlimit(resource.RLIMIT_FSIZE,(3145728,3145728))
    with stdout.open('xb') as fo,stderr.open('xb') as fe:
        CHILD=subprocess.Popen([sys.executable,str(ROOT/(PREFIX+'-helper.py')),'--publication-commit',a.publication_commit,'--protocol-sha256',a.protocol_sha256,'--protocol-bytes',str(len(pb)),'--review-file',a.review_file,'--review-sha256',a.review_sha256],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=fo,stderr=fe,start_new_session=True,preexec_fn=limit)
        rc=CHILD.wait(timeout=max(0.1,585-(time.monotonic()-START)))
except BaseException as exc:error={'type':type(exc).__name__,'detail':str(exc)}
finally:closed=killgroup()
try:
    for suffix in ['-receipt.json','-events.jsonl','-composite.json','-supervisor.stdout','-supervisor.stderr']:
        path=ROOT/(PREFIX+suffix)
        if path.exists():
            b=path.read_bytes();assert len(b)<=3145728;sealed.append({'file':PREFIX+suffix,**identity(b)})
            if suffix=='-receipt.json':receipt=json.loads(b)
    if receipt and receipt.get('passed') is True:
        assert receipt['composite'] in sealed
    metadata=ROOT/(PREFIX+'-metadata')
    if metadata.exists():
        captures=sorted(metadata.iterdir());assert len(captures)<=42
        for path in captures:
            assert path.is_file() and not path.is_symlink()
            with path.open('rb') as f:b=f.read(3145729)
            assert len(b)<=3145728
            sealed.append({'file':str(path.relative_to(ROOT)),**identity(b)})
    elapsed=time.monotonic()-START
    passed=error is None and closed and rc==0 and receipt and receipt.get('passed') is True and receipt.get('closed') is True and elapsed<600
    result={'passed':bool(passed),'closed':closed,'status':'complete' if closed else 'incomplete-or-unknown','error':error,'returncode':rc,'processGroupAbsent':closed,'wallSeconds':elapsed,'publicationCommit':a.publication_commit,'protocolSha256':a.protocol_sha256,'reviewSha256':a.review_sha256,'sealedOutputPinsAfterCleanup':sealed,'scientificExecution':False,'scope':'Only this sealed supervisor PASS plus independently reviewed amended composite may support a later amended source-publication gate.'}
    atomic(outer,result);signal.setitimer(signal.ITIMER_REAL,0);print(json.dumps(result));sys.exit(0 if passed else 1)
except BaseException:
    # The durable initial incomplete/unknown record remains non-authorizing if sealing fails.
    killgroup();raise
