from pathlib import Path
import json,hashlib,time,gzip,io,sys,traceback,re
import os
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent;root=base.parent.parent
out=base/'extract';out.mkdir();(out/'launch.lock').write_text('single bounded extraction; no native queries\n')
start=time.monotonic();events=[];bytes_written=(out/'launch.lock').stat().st_size;failure_mode=False;cfg=json.loads((base/'config.json').read_bytes());cap=cfg['allocations']['extract']['mib']*1024**2;limit=cfg['allocations']['extract']['seconds']
sha=lambda b:hashlib.sha256(b).hexdigest()
def tick():
 assert time.monotonic()-start<limit,'wall-budget'
 assert sum(p.stat().st_size for p in out.rglob('*') if p.is_file())<cap-2*1024**2,'evidence-budget'
def checked(path,pin):
 for attempt in range(1,4):
  tick()
  try:
   b=path.read_bytes()
   if len(b)==pin['bytes'] and sha(b)==pin['sha256']:return b
   events.append({'path':str(path.relative_to(root)),'attempt':attempt,'kind':'identity-mismatch','bytes':len(b),'sha256':sha(b)})
  except OSError as e:events.append({'path':str(path.relative_to(root)),'attempt':attempt,'kind':'read-error','errno':e.errno})
 raise ValueError('identity-read-failed:'+str(path.relative_to(root)))
def save(name,v):
 data=(json.dumps(v,separators=(',',':'))+'\n').encode()
 with (out/name).open('xb') as f:Charged(f).write(data)
class Charged:
 def __init__(self,f):self.f=f
 def write(self,data):
  global bytes_written
  assert bytes_written+len(data)<=cap-(0 if failure_mode else 2*1024**2),'prewrite-output-budget'
  n=self.f.write(data);assert n==len(data);bytes_written+=n;return n
 def flush(self):return self.f.flush()
 def tell(self):return self.f.tell()
class Parts(io.RawIOBase):
 def __init__(self,parts):self.parts=iter(parts);self.buf=b'';self.at=0;self.h=hashlib.sha256();self.count=0;self.pins=[]
 def readable(self):return True
 def readinto(self,b):
  if self.at==len(self.buf):
   p=next(self.parts,None)
   if p is None:return 0
   assert p['offset']==self.count
   self.buf=checked(root/'research/m31-paired-resolution-2026-10-21/results'/p['file'],p);self.at=0;self.h.update(self.buf);self.count+=len(self.buf);self.pins.append(p)
  n=min(len(b),len(self.buf)-self.at);b[:n]=self.buf[self.at:self.at+n];self.at+=n;return n
exit_code=0
try:
 raw=(base/'source-manifest.json').read_bytes();manifest=json.loads(raw);pub=json.loads((base/'source-publication.json').read_bytes())
 assert sha(raw)==pub['manifestSha256'] and pub['remoteBytesEqualLocal'] and pub['committedBytesEqualLocal'] and pub['independentReviewPassed']
 assert re.fullmatch('[0-9a-f]{40}',pub['commit']) and pub['verifiedFilePins']==len(manifest['files'])
 for p in manifest['files']:
  if '.jsonl.gz.part' not in p['path']:checked(root/p['path'],p)
 ix=json.loads((root/'research/m31-paired-resolution-2026-10-21/results/index.json').read_bytes());assert ix['complete']
 selected=0;windows=[];sources=[];refusals=[]
 with (out/'selected.jsonl.gz').open('xb') as stream,gzip.GzipFile(filename='',mode='wb',fileobj=Charged(stream),mtime=0) as dest:
  for ci,c in enumerate(ix['cases']):
   assert c['caseId']==cfg['caseIds'][ci] and c['attemptedStages']==cfg['totalStages'][ci]
   starts=[0,4000,c['attemptedStages']-160];global_ordinal=0
   for wi,s in enumerate(starts):windows.append({'window':ci*3+wi,'caseId':c['caseId'],'start':s,'length':160})
   for seg in c['segments']:
    journal=seg['journal'];parts=Parts(journal['parts']);rawhash=hashlib.sha256();rawcount=0;records=0;local=0
    with gzip.GzipFile(fileobj=io.BufferedReader(parts),mode='rb') as gz:
     for line in gz:
      tick();rawOffset=rawcount;rawhash.update(line);rawcount+=len(line);row=json.loads(line);assert row['sequence']==records;records+=1
      if row['kind']!='stage':continue
      for wi,s in enumerate(starts):
       if s<=global_ordinal<s+160:
        body=row['body'];rec={'window':ci*3+wi,'index':global_ordinal-s,'caseId':c['caseId'],'globalOrdinal':global_ordinal,'segment':seg['segment'],'localStageOrdinal':local,'rawOffset':rawOffset,'sourceLineSha256':sha(line),'sourceLineBytes':len(line),'record':row}
        dest.write((json.dumps(rec,separators=(',',':'))+'\n').encode());selected+=1
        if body['native']['status']!='native-success':refusals.append({'window':ci*3+wi,'index':global_ordinal-s,'status':body['native']['status'],'reason':body['native']['reason'],'originalTimeWord':body['originalTimeWord']})
      local+=1;global_ordinal+=1
    assert local==seg['attemptedStages'] and records==journal['records']
    assert rawcount==journal['rawBytes'] and rawhash.hexdigest()==journal['rawSha256']
    assert parts.count==journal['bytes'] and parts.h.hexdigest()==journal['sha256']
    sources.append({'caseId':c['caseId'],'segment':seg['segment'],'parts':parts.pins,'records':records,'stages':local,'rawBytes':rawcount,'rawSha256':rawhash.hexdigest()})
   assert global_ordinal==c['attemptedStages']
 assert selected==1920 and len(refusals)==1 and refusals[0]['window']==2 and refusals[0]['index']==159
 pin={'file':'selected.jsonl.gz','bytes':(out/'selected.jsonl.gz').stat().st_size,'sha256':sha((out/'selected.jsonl.gz').read_bytes())}
 save('index.json',{'complete':True,'selected':selected,'windows':windows,'sources':sources,'refusals':refusals,'selectedPin':pin,'readEvents':events,'nativeQueries':0,'wallSeconds':time.monotonic()-start});tick()
except Exception as e:
 exit_code=1;failure_mode=True;save('failure.json',{'type':type(e).__name__,'message':str(e).replace(str(root),'[repository]')[:1000],'trace':traceback.format_exc().replace(str(root),'[repository]')[-2500:],'readEvents':events})
finally:
 failure_mode=True
 save('exit.json',{'closed':True,'exitCode':exit_code,'wallSeconds':time.monotonic()-start,'readEvents':events});sys.exit(exit_code)
