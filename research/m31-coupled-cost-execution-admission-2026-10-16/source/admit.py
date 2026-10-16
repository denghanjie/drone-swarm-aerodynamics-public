"""Benign staged child-process admission only; no scientific imports or inputs."""
import datetime, hashlib, json, os, pathlib, select, subprocess, sys, time
if sys.flags.optimize:raise RuntimeError('Nonoptimized Python required')
if os.environ.get('NODE_OPTIONS'):raise RuntimeError('NODE_OPTIONS must be empty')
p=pathlib.Path(__file__).resolve().parent.parent
assert len(sys.argv)==5
context,node,expected_manifest,source_commit=sys.argv[1:]
assert context in ('sandbox','host')
m=p/'source-manifest.json'
assert hashlib.sha256(m.read_bytes()).hexdigest()==expected_manifest
for f in json.loads(m.read_text())['files']:
    b=(p/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
node_sha=hashlib.sha256(pathlib.Path(node).read_bytes()).hexdigest()
python_sha=hashlib.sha256(pathlib.Path(sys.executable).read_bytes()).hexdigest()
assert len(source_commit)==40 and all(c in '0123456789abcdef' for c in source_commit)
out=p/'results';out.mkdir(exist_ok=True)
with (out/(context+'-invocation.lock')).open('x') as f:f.write('One infrastructure invocation consumed. No science.\n')
rec={'contextLabel':context,'kind':'echo-only-process-admission','sourceCommit':source_commit,'sourceCommitVerification':'coordinator independently retrieved remote manifest before dispatch; this script checks local source pins','sourceManifestSha256':expected_manifest,'nodeSha256':node_sha,'pythonSha256':python_sha,'startedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'events':[],'admitted':False,'performanceMeasurement':False,'pidOmitted':True}
proc=None;stage='initial';start=time.monotonic()
with (out/(context+'-journal.jsonl')).open('x') as journal:
    def event(name,**fields):
        global stage
        stage='journal-write-for:'+name;row={'stage':name,'elapsedSeconds':time.monotonic()-start,**fields};journal.write(json.dumps(row)+'\n');journal.flush();os.fsync(journal.fileno());rec['events'].append(row);stage=name
    def safe_event(name,**fields):
        try:event(name,**fields)
        except BaseException as e:
            rec['admitted']=False
            rec.setdefault('journalErrors',[]).append({'operation':stage,'exceptionClass':type(e).__name__,'errno':getattr(e,'errno',None)})
    try:
        event('before-node-popen')
        proc=subprocess.Popen([node,'-e',"process.stdout.write('M31_ECHO_READY\\n');const t=setTimeout(()=>process.exit(3),6000);process.stdin.once('data',b=>{clearTimeout(t);if(b.toString()!=='ACK\\n')process.exit(2);process.stdout.write('M31_ECHO_DONE\\n',()=>process.exit(0));});"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        event('node-popen-returned')
        event('before-handshake-read')
        ready,_,_=select.select([proc.stdout],[],[],2)
        if not ready:raise TimeoutError('handshake timeout')
        line=proc.stdout.readline(128)
        rec['handshakeExact']=line==b'M31_ECHO_READY\n'
        event('handshake-read',exact=rec['handshakeExact'],bytes=len(line))
        if not rec['handshakeExact']:raise ValueError('unexpected echo')
        event('before-ps-popen')
        rss=subprocess.check_output(['/bin/ps','-o','rss=','-p',str(proc.pid)],stderr=subprocess.PIPE,timeout=2)
        rec['rssKiB']=int(rss.strip());event('ps-returned',rssKiB=rec['rssKiB'])
        event('before-child-completion')
        tail,stderr=proc.communicate(input=b'ACK\n',timeout=8)
        rec['childReturnCode']=proc.returncode;rec['remainingStdoutBytes']=len(tail);rec['stderrBytes']=len(stderr)
        event('child-completed',returnCode=proc.returncode)
        rec['admitted']=rec['handshakeExact'] and rec['rssKiB']>0 and proc.returncode==0 and tail==b'M31_ECHO_DONE\n' and not stderr
    except BaseException as e:
        rec['error']={'operation':stage,'exceptionClass':type(e).__name__,'errno':getattr(e,'errno',None)}
        rec['admitted']=False;safe_event('caught-error',**rec['error'])
    finally:
        if proc is not None:
            try:
                safe_event('before-cleanup');stage='cleanup-process'
                if proc.poll() is None:proc.kill()
                tail,stderr=proc.communicate(timeout=2)
                rec['cleanupReturnCode']=proc.returncode;rec['cleanupStdoutBytes']=len(tail);rec['cleanupStderrBytes']=len(stderr)
                safe_event('cleanup-complete',returnCode=proc.returncode)
            except BaseException as e:
                rec['admitted']=False;rec['cleanupError']={'operation':stage,'exceptionClass':type(e).__name__,'errno':getattr(e,'errno',None)}
                safe_event('cleanup-error',**rec['cleanupError'])
        rec['elapsedSeconds']=time.monotonic()-start
        (out/(context+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps({'context':context,'admitted':rec['admitted'],'error':rec.get('error'),'elapsedSeconds':rec['elapsedSeconds']}))
sys.exit(0 if rec['admitted'] else 1)
