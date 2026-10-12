from pathlib import Path
import json,hashlib,struct,math
root=Path(__file__).resolve().parent.parent;src=root/'milestone-26-source';protocol=json.loads((root/'milestone-26-protocol.json').read_text());checks=[]
def check(name,value):
 checks.append({'check':name,'passed':bool(value)})
 if not value:raise AssertionError(name)
check('Frozen numerical sources unchanged',all(hashlib.sha256((src/f).read_bytes()).hexdigest()==h for f,h in protocol['sourceHashes'].items()))
index=json.loads((src/'index.json').read_text());seen=set()
for e in index:
 r=json.loads((src/e['file']).read_text());j=r['job'];check(j['id']+' prescribed once',j in protocol['jobs'] and j['id'] not in seen);seen.add(j['id']);replay=r['replay'];stride=replay['valuesPerFrame']*8;f=src/replay['file'];check(j['id']+' binary byte count',f.stat().st_size==replay['frames']*stride)
 with f.open('rb') as stream:
  times=[]
  for i in range(replay['frames']):stream.seek(i*stride);times.append(struct.unpack('<d',stream.read(8))[0])
  stream.seek(0);first=list(struct.unpack('<'+'d'*replay['valuesPerFrame'],stream.read(stride)))
  stream.seek((replay['frames']-1)*stride);last=list(struct.unpack('<'+'d'*replay['valuesPerFrame'],stream.read(stride)))
  check(j['id']+' timestamps',times[0]==0 and all(a<b for a,b in zip(times,times[1:])) and abs(times[-1]-r['metrics']['end'])<1e-9)
  check(j['id']+' exact initial and final positions/quaternions',first[1:]==[v for s in r['initial'] for v in s[:3]+s[6:10]] and last[1:]==[v for s in r['final'] for v in s[:3]+s[6:10]])
  for t in [20,60,120,180]:
   p=src/f'checkpoint-{j["id"]}-{t}.json'
   if not p.exists():continue
   c=json.loads(p.read_text());frameIndex=times.index(t);stream.seek(frameIndex*stride);frame=list(struct.unpack('<'+'d'*replay['valuesPerFrame'],stream.read(stride)));check(j['id']+f' exact checkpoint {t}',frame[1:]==[v for s in c['states'] for v in s[:3]+s[6:10]])
 check(j['id']+' index metrics and geometry',e['metrics']==r['metrics'] and json.loads((src/e['geometry']).read_text())['id']==r['config']['course'])
final=(root/'milestone-26-summary.json').exists()
if final:check('All 11 prescribed runs complete',len(seen)==len(protocol['jobs']))
(root/'milestone-26-artifact-checks.json').write_text(json.dumps({'scope':'all completed runs at time of audit','studyComplete':final,'completedRuns':len(index),'checks':checks},indent=2));print({'completedRuns':len(index),'checks':len(checks),'studyComplete':final})
