"""Unexecuted administrative draft: exact missing blobs into isolated stores."""
from pathlib import Path
import hashlib,json,os,subprocess,signal,time,sys,resource,re
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('optimized-python-prohibited')

cfg=json.loads(Path(sys.argv[1]).read_bytes())
root=Path.cwd();work=Path('/private/tmp')/cfg['privateStoreName']
start=time.monotonic();events=[];proofs=[];failure=None;journal=None;peakTotal=0;peakStore=0
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_') and k not in ('GH_DEBUG','DEBUG')}
env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_TERMINAL_PROMPT='0',GIT_NO_REPLACE_OBJECTS='1',GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=30 -o StrictHostKeyChecking=yes')
def sha(b):return hashlib.sha256(b).hexdigest()
def safe(s):
    s=s.replace(str(root),'[repository]').replace(str(work),'[private-stores]')
    s=re.sub(r'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+','[redacted]',s)
    return re.sub(r'(?im)(authorization\s*[:=]\s*)[^\r\n]+',r'\1[redacted]',s)
def size(p):return sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
def record(e):
    e={'event':len(events)+1,**e};events.append(e)
    if journal is not None:
        with journal.open('a') as f:f.write(json.dumps(e)+'\n');f.flush();os.fsync(f.fileno())
    return e
def limits():resource.setrlimit(resource.RLIMIT_FSIZE,(48*1024**2,48*1024**2))
def command(args,seconds,store=None):
    global peakTotal,peakStore
    assert time.monotonic()-start<cfg['overallSeconds']
    record({'operation':'command-start','args':[safe(x) for x in args],'secondsLimit':seconds})
    i=len(events);out=work/('stdout-'+str(i));err=work/('stderr-'+str(i))
    t=time.monotonic();reason=None
    with out.open('xb') as a,err.open('xb') as b:
        p=subprocess.Popen(args,cwd=root,env=env,stdout=a,stderr=b,stdin=subprocess.DEVNULL,preexec_fn=limits)
        try:
            while p.poll() is None:
                if time.monotonic()-t>=seconds or time.monotonic()-start>=cfg['overallSeconds']:reason='time-limit';break
                if out.stat().st_size+err.stat().st_size>2*1024**2:reason='pipe-cap';break
                total=size(work);local=size(store) if store else 0;peakTotal=max(peakTotal,total);peakStore=max(peakStore,local)
                if total>256*1024**2 or local>96*1024**2:reason='disk-cap';break
                time.sleep(.1)
        finally:
            if p.poll() is None:p.kill()
            p.wait(timeout=3)
    observedOut=out.stat().st_size;observedErr=err.stat().st_size
    peakTotal=max(peakTotal,size(work));peakStore=max(peakStore,size(store) if store else 0)
    with out.open('rb') as f:raw=f.read(2*1024**2+1)
    with err.open('rb') as f:error=f.read(2*1024**2+1)
    e={'operation':'command-end','args':[safe(x) for x in args],'returncode':p.returncode,'reason':reason,'wallSeconds':time.monotonic()-t,'stdoutBytes':observedOut,'stdoutPrefixSha256':sha(raw),'stderrBytes':observedErr,'stderrPrefixSha256':sha(error),'stderr':safe(error.decode(errors='replace'))[:1500]};record(e)
    assert not reason and p.returncode==0 and observedOut+observedErr<=2*1024**2
    assert size(work)<=256*1024**2 and (not store or size(store)<=96*1024**2)
    return raw
try:
    assert re.fullmatch('m31-targeted-ssh-[a-z0-9-]+',cfg['privateStoreName'])
    assert cfg['remote']=='git@github.com:denghanjie/drone-swarm-aerodynamics-public.git'
    assert cfg['overallSeconds']==885 and 1<=len(cfg['pins'])<=3
    assert not work.exists();work.mkdir(mode=0o700)
    journal=work/'events.jsonl';journal.touch(exist_ok=False)
    record({'operation':'start','scope':'Exact missing blobs only; no scientific execution','outerSupervisorSeconds':900,'innerSeconds':885})
    with (root/cfg['launchLock']).open('x') as f:f.write('one prospective targeted SSH acquisition\n')
    for rec in cfg['pinnedRecords']:
        b=(root/rec['file']).read_bytes();assert len(b)==rec['bytes'] and sha(b)==rec['sha256']
    for p in cfg['pins']:
        oid=p['gitBlobOid'];assert re.fullmatch('[0-9a-f]{40}',oid)
        for ref in [cfg['scientificSourceCommit'],p['originCommit']]:
            raw=command(['git','ls-tree','-z',ref,'--',p['path']],45)
            meta,name=raw.rstrip(b'\0').split(b'\t');mode,kind,obj=meta.split()
            assert name.decode()==p['path'] and kind==b'blob' and obj.decode()==oid and mode in (b'100644',b'100755')
            record({'operation':'tree-binding','commit':ref,'path':p['path'],'mode':mode.decode(),'kind':kind.decode(),'gitBlobOid':obj.decode(),'passed':True})
        store=work/oid;store.mkdir()
        command(['git','init','--bare','--template=',str(store)],15,store)
        assert not list((store/'objects').rglob('*.pack')) and not (store/'objects/info/alternates').exists()
        assert command(['git','--git-dir='+str(store),'cat-file','--batch-all-objects','--batch-check'],15,store)==b''
        command(['git','--git-dir='+str(store),'-c','gc.auto=0','-c','maintenance.auto=false','-c','fetch.writeCommitGraph=false','fetch','--no-tags','--no-write-fetch-head','--no-recurse-submodules','--no-auto-maintenance',cfg['remote'],oid],180,store)
        objects=command(['git','--git-dir='+str(store),'cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)'],30,store)
        assert objects.decode().splitlines()==[oid+' blob '+str(p['bytes'])],'unexpected-object-set'
        t=time.monotonic();a=hashlib.sha256();g=hashlib.sha1(('blob '+str(p['bytes'])+'\0').encode());n=0;hashComplete=False
        record({'operation':'stream-hash-start','path':p['path'],'gitBlobOid':oid,'expectedBytes':p['bytes']})
        proc=subprocess.Popen(['git','--git-dir='+str(store),'cat-file','blob',oid],cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        try:
            import selectors
            sel=selectors.DefaultSelector();sel.register(proc.stdout,selectors.EVENT_READ)
            while sel.get_map():
                assert time.monotonic()-t<45 and time.monotonic()-start<cfg['overallSeconds']
                for key,_ in sel.select(.1):
                    b=os.read(key.fileobj.fileno(),65536)
                    if not b:sel.unregister(key.fileobj);break
                    n+=len(b);assert n<=p['bytes'];a.update(b);g.update(b)
            assert proc.wait(timeout=3)==0
            hashComplete=True
        finally:
            if proc.poll() is None:proc.kill();proc.wait(timeout=3)
            proc.stdout.close();sel.close()
            record({'operation':'stream-hash-end','path':p['path'],'gitBlobOid':oid,'complete':hashComplete,'observedBytes':n,'sha256':a.hexdigest(),'observedGitBlobSha1':g.hexdigest(),'wallSeconds':time.monotonic()-t})
        assert n==p['bytes'] and a.hexdigest()==p['sha256'] and g.hexdigest()==oid
        proof={'descriptor':p,'freshAuthenticatedSshBlob':True,'freshAnonymousBody':False,'isolatedObjectInventory':objects.decode().splitlines(),'bytes':n,'sha256':a.hexdigest(),'gitBlobOid':g.hexdigest()};proofs.append(proof);record({'operation':'verified-blob',**proof})
except BaseException as e:failure={'type':type(e).__name__,'detail':safe(str(e))[:1500]}
finally:
    elapsed=time.monotonic()-start
    finalSize=size(work) if work.exists() else 0;peakTotal=max(peakTotal,finalSize)
    result={'closed':True,'passed':failure is None and len(proofs)==len(cfg['pins']) and elapsed<=cfg['overallSeconds'] and peakTotal<=256*1024**2 and peakStore<=96*1024**2,'scientificSourceCommit':cfg['scientificSourceCommit'],'events':events,'proofs':proofs,'error':failure,'wallSeconds':elapsed,'finalDiskBytesBeforeReceipt':finalSize,'observedPeakTotalBytes':peakTotal,'observedPeakStoreBytes':peakStore,'limitsDisclosure':'96MiB/store,256MiB total and2MiB diagnostics are monitored thresholds with failure on observed excess, not strict aggregate ceilings;48MiB per-file OS limit is hard. Outer900s supervisor covers complete invocation.','rawBodySource':'New isolated SSH-fetched objects only; original repository used solely for tree metadata','noScientificExecution':True}
    with (work/'receipt.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'passed':result['passed'],'proofs':len(proofs),'error':failure}))
