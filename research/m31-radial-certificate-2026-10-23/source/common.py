from pathlib import Path
import json,hashlib,time,subprocess,os,re,struct,math,sys
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
BASE=Path(__file__).resolve().parent.parent;ROOT=BASE.parent.parent
CFG=json.loads((BASE/'config.json').read_bytes());EVENTS=[];CACHE={};PINS={}
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def load(p):return json.loads(p.read_bytes())
def number(w):
 assert isinstance(w,str) and re.fullmatch('[0-9a-f]{16}',w)
 n=struct.unpack('>d',bytes.fromhex(w))[0];assert math.isfinite(n);return n
def word(v):return struct.pack('>d',v).hex()
def integer(v):
 assert type(v) in (int,float) and math.isfinite(v) and 0<=v<=2**53-1 and int(v)==v
 return int(v)
def checked_local(path,pin):
 for attempt in range(1,4):
  try:
   b=path.read_bytes()
   if len(b)==pin['bytes'] and sha(b)==pin['sha256']:return b
   EVENTS.append({'path':str(path.relative_to(ROOT)),'attempt':attempt,'kind':'local-identity-mismatch'})
  except OSError as e:EVENTS.append({'path':str(path.relative_to(ROOT)),'attempt':attempt,'kind':'local-read-error','errno':e.errno})
 raise RuntimeError('local-identity-read-failed:'+str(path.relative_to(ROOT)))
def committed(path):
 if path in CACHE:return CACHE[path]
 pin=PINS[path];assert pin['kind']=='input';commit=pin['originCommit'];assert re.fullmatch('[0-9a-f]{40}',commit)
 env=dict(os.environ);env['GIT_NO_REPLACE_OBJECTS']='1'
 for attempt in range(1,CFG['readPolicy']['attemptsPerFile']+1):
  start=time.monotonic()
  try:
   obj=commit+':'+path;limit=CFG['readPolicy']['gitReadTimeoutSeconds']
   size=subprocess.run(['git','cat-file','-s',obj],cwd=ROOT,env=env,capture_output=True,timeout=limit,check=True)
   assert int(size.stdout)==pin['bytes'],'committed-size-mismatch'
   remaining=limit-(time.monotonic()-start);assert remaining>0
   got=subprocess.run(['git','show',obj],cwd=ROOT,env=env,capture_output=True,timeout=remaining,check=True)
   assert len(got.stdout)==pin['bytes'] and sha(got.stdout)==pin['sha256'],'committed-identity-mismatch'
   CACHE[path]=got.stdout;return got.stdout
  except Exception as e:
   msg=(getattr(e,'stderr',b'') or b'').decode(errors='replace')[:300]
   EVENTS.append({'path':path,'attempt':attempt,'kind':type(e).__name__,'detail':msg.replace(str(ROOT),'[repository]') or str(e).replace(str(ROOT),'[repository]')[:300]})
 raise RuntimeError('committed-identity-read-failed:'+path)
def gate(read_inputs=True):
 raw=(BASE/'source-manifest.json').read_bytes();m=json.loads(raw);pub=load(BASE/'source-publication.json')
 assert pub['manifestSha256']==sha(raw) and pub['manifestBytes']==len(raw)
 assert pub['remoteBytesEqualLocal'] and pub['committedBytesEqualLocal'] and pub['independentReviewPassed']
 assert re.fullmatch('[0-9a-f]{40}',pub['commit']) and pub['verifiedFilePins']==len(m['files'])
 assert len({p['path'] for p in m['files']})==len(m['files'])
 PINS.update({p['path']:p for p in m['files']})
 for p in m['files']:
  if p['kind']=='source':checked_local(ROOT/p['path'],p)
  else:
   assert p['kind']=='input'
   if read_inputs:committed(p['path'])
 return pub
def prior(phase):
 x=load(BASE/(phase+'-supervisor.json'));assert x['closed'] and x['returncode']==0 and x['allocationWallPassed'] and x['outputCapPassed'] and not x.get('timeout')
class Output:
 def __init__(self,phase,folder):
  self.start=time.monotonic();self.phase=phase;self.out=BASE/folder;self.out.mkdir();self.bytes=0;self.failed=False;self.save('launch.json',{'singleUse':True,'nativeCalls':0})
 def tick(self):assert time.monotonic()-self.start<CFG['allocations'][self.phase]['seconds']-3,'wall-budget'
 def save(self,name,value,append=False):
  b=canonical(value);cap=CFG['allocations'][self.phase]['mib']*1024**2
  assert self.bytes+len(b)<=cap-(0 if self.failed else 512*1024),'output-budget'
  if not self.failed:self.tick()
  with (self.out/name).open('ab' if append else 'xb') as f:assert f.write(b)==len(b)
  self.bytes+=len(b)
 def close(self,code):
  self.failed=True;self.save('exit.json',{'closed':True,'exitCode':code,'wallSeconds':time.monotonic()-self.start,'readEvents':EVENTS})
