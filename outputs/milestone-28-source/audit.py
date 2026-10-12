from pathlib import Path
import json,hashlib,struct,math
root=Path(__file__).resolve().parent.parent;src=root/'milestone-28-source';protocol=json.loads((root/'milestone-28-protocol.json').read_text());checks=[]
def check(name,value):
 checks.append({'check':name,'passed':bool(value)})
 if not value:raise AssertionError(name)
check('Frozen numerical sources unchanged',all(hashlib.sha256((src/f).read_bytes()).hexdigest()==h for f,h in protocol['sourceHashes'].items()))
index=json.loads((src/'index.json').read_text());seen=set();starts={};runs={}
for e in index:
 r=json.loads((src/e['file']).read_text());j=r['job'];check(j['id']+' prescribed once',j in protocol['jobs'] and j['id'] not in seen);seen.add(j['id']);runs[j['id']]=r;group=(j['seed'],j['count'],j['course']);check(j['id']+' identical matched starting states',group not in starts or starts[group]==r['initial']);starts[group]=r['initial'];check(j['id']+' finite full states',all(isinstance(v,(int,float)) and math.isfinite(v) for state in r['initial']+r['final'] for v in state));check(j['id']+' unit endpoint quaternions',all(abs(math.sqrt(sum(v*v for v in state[6:10]))-1)<1e-10 for state in r['initial']+r['final']));replay=r['replay'];stride=replay['valuesPerFrame']*8;f=src/replay['file'];check(j['id']+' binary byte count',f.stat().st_size==replay['frames']*stride)
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
# Event identity is additional scientific evidence, not a replacement for the frozen joint criterion.
events=[]
def event(r):
 f=r['metrics']['failure'] or {};return {'reason':r['metrics']['stopReason'],'drone':f.get('drone'),'pair':f.get('pair'),'obstacles':[h['id'] for h in f.get('hits',[])],'source':f.get('source'),'receiver':f.get('receiver'),'domainMessage':f.get('message')}
for job in protocol['jobs']:
 if job['kind']=='primary' or job['id'] not in runs:continue
 coarse=next(j for j in protocol['jobs'] if j['seed']==job['seed'] and j['count']==job['count'] and j['course']==job['course'] and j['aeroMode']==job['aeroMode'] and j['kind']==('refinement' if job['kind']=='cadence' else 'primary'))
 if coarse['id'] not in runs:continue
 a,b=runs[coarse['id']],runs[job['id']];ea,eb=event(a),event(b);events.append({'coarse':coarse['id'],'fine':job['id'],'events':[ea,eb],'rawFailures':[a['metrics']['failure'],b['metrics']['failure']],'sameEventIdentity':ea==eb,'endTimes':[a['metrics']['end'],b['metrics']['end']],'maximumEndpointDifferenceM':max(math.dist(x[:3],y[:3]) for x,y in zip(a['final'],b['final']))})
(root/'milestone-28-event-comparisons.json').write_text(json.dumps({'scope':'supplement to frozen criteria; unequal-time endpoints are not synchronized paths','comparisons':events},indent=2))
final=(root/'milestone-28-summary.json').exists()
if final:check('All 25 prescribed runs complete',len(seen)==len(protocol['jobs']))
(root/'milestone-28-artifact-checks.json').write_text(json.dumps({'scope':'all completed runs at time of audit','studyComplete':final,'completedRuns':len(index),'checks':checks},indent=2));print({'completedRuns':len(index),'checks':len(checks),'studyComplete':final})
