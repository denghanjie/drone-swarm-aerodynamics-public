from pathlib import Path
import json,hashlib,time,sys,os,signal
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent;out=base/'transport';out.mkdir();start=time.monotonic();cap=768*1024**2;written=0;failed=False
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('transport-wall-cap')));signal.alarm(300)
def save(name,data):
 global written
 assert (failed or time.monotonic()-start<300) and written+len(data)<=cap-(0 if failed else 1024**2)
 with (out/name).open('xb') as f:f.write(data)
 written+=len(data)
def jsave(name,value):save(name,(json.dumps(value,separators=(',',':'))+'\n').encode())
code=0
try:
 jsave('launch.json',{'singleUse':True,'nativeQueries':0,'maxSeconds':300,'maxBytes':cap})
 original=base/'extract/selected.jsonl.gz';expected=json.loads((base/'extract/index.json').read_bytes())['selectedPin'];parts=[];total=0;h=hashlib.sha256()
 with original.open('rb') as f:
  while True:
   b=f.read(32*1024**2)
   if not b:break
   name='selected.jsonl.gz.part'+str(len(parts)).zfill(3);save(name,b);parts.append({'file':name,'offset':total,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()});total+=len(b);h.update(b)
 assert total==expected['bytes'] and h.hexdigest()==expected['sha256']
 jsave('index.json',{'complete':True,'original':{'path':'extract/selected.jsonl.gz',**expected},'parts':parts,'nativeQueries':0})
except Exception as e:
 failed=True;code=1;jsave('failure.json',{'type':type(e).__name__,'message':str(e).replace(str(base),'[checkpoint]')[:700]})
finally:
 signal.alarm(0);failed=True;jsave('exit.json',{'closed':True,'exitCode':code,'wallSeconds':time.monotonic()-start,'bytesBeforeExit':written});sys.exit(code)
