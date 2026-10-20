from pathlib import Path
import json,hashlib,time,sys
B=Path(__file__).resolve().parent.parent
R=B.parent.parent
START=time.monotonic();MAX=520*1024*1024;PART=32*1024*1024
written=0

def guard():
 assert time.monotonic()-START<=180,'archive wall budget'
 assert written<=MAX-1024*1024,'archive output budget'

def digest(path):
 h=hashlib.sha256();n=0
 with path.open('rb') as f:
  while data:=f.read(1024*1024):guard();h.update(data);n+=len(data)
 return n,h.hexdigest()

def save(path,obj):
 global written
 raw=(json.dumps(obj,indent=2)+'\n').encode();assert written+len(raw)<=MAX
 with path.open('xb') as f:f.write(raw)
 written+=len(raw)

manifest_raw=(B/'archive-source-manifest.json').read_bytes();manifest=json.loads(manifest_raw);pub=json.loads((B/'archive-source-publication.json').read_text())
assert pub['manifestSha256']==hashlib.sha256(manifest_raw).hexdigest() and pub['remoteBytesEqualLocal'] is True and pub['committedBytesEqualLocal'] is True
for pin in manifest['files']:
 n,h=digest(R/pin['path']);assert n==pin['bytes'] and h==pin['sha256'],pin['path']
assert (B/'archive-supervisor-launch.lock').is_file()
index=json.loads((B/'results/index.json').read_text());assert index['complete'] is True
out=B/'archive';out.mkdir();save(out/'launch.json',{'sourceCommit':pub['commit'],'scope':'lossless byte copying only','partBytes':PART,'maxWallSeconds':180,'maxOutputBytes':MAX})
try:
 records=[]
 for case in index['cases']:
  src=case['journal'];name=src['file'];assert Path(name).name==name
  source=B/'results'/name;assert source.is_file() and not source.is_symlink()
  total=0;h=hashlib.sha256();parts=[]
  with source.open('rb') as f:
   while data:=f.read(PART):
    guard();assert written+len(data)<=MAX-1024*1024
    part_name=name+'.part'+str(len(parts)).zfill(3);p=out/part_name
    with p.open('xb') as target:target.write(data)
    parts.append({'file':part_name,'offset':total,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});h.update(data);total+=len(data);written+=len(data)
  assert total==src['bytes'] and h.hexdigest()==src['sha256'],'original journal identity'
  rehash=hashlib.sha256();count=0
  for part in parts:
   guard();raw=(out/part['file']).read_bytes();assert len(raw)==part['bytes'] and hashlib.sha256(raw).hexdigest()==part['sha256'];assert count==part['offset'];count+=len(raw);rehash.update(raw)
  assert count==total and rehash.hexdigest()==src['sha256'],'reconstruction identity'
  records.append({'originalFile':'results/'+name,'bytes':total,'sha256':src['sha256'],'parts':parts,'reconstructionVerified':True})
 for pin in manifest['files']:
  n,h=digest(R/pin['path']);assert n==pin['bytes'] and h==pin['sha256'],pin['path']
 for src in records:
  n,h=digest(B/src['originalFile']);assert n==src['bytes'] and h==src['sha256'],'original changed after copying'
 guard();save(out/'index.json',{'schema':'m31-boids-byte-archive-v1','journals':records,'originalJournalsUnchanged':True,'noScientificEvaluation':True})
 guard();save(out/'exit.json',{'exitCode':0,'closed':True,'wallSeconds':time.monotonic()-START,'bytesBeforeExit':written});guard()
except Exception as e:
 save(out/'failure.json',{'message':str(e).replace(str(R),'[repository]'),'closed':True,'wallSeconds':time.monotonic()-START});raise
print(json.dumps({'journalCount':len(records),'parts':sum(len(r['parts']) for r in records),'wallSeconds':time.monotonic()-START,'bytes':written}))
