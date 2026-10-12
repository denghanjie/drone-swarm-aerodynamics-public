from pathlib import Path
import json,hashlib,struct,math
root=Path(__file__).resolve().parent.parent;src=root/'milestone-29-source';p=json.loads((root/'milestone-29-protocol.json').read_text());f=root/'milestone-29-progress.json';rs=json.loads(f.read_text()) if f.exists() else [];checks=[];repeats={}
def check(name,ok):
 checks.append({'check':name,'passed':bool(ok)})
 if not ok:raise AssertionError(name)
check('Frozen source unchanged',all(hashlib.sha256((src/k).read_bytes()).hexdigest()==h for k,h in p['sourceHashes'].items()))
check('Replay geometry matches corrected wide factory',json.loads((src/'factory-wide.json').read_text())==json.loads((root/'milestone-28-source/factory-wide.json').read_text()))
seen=set();starts={}
for r in rs:
 j=r['job'];check(j['id']+' prescribed once',j in p['jobs'] and j['id'] not in seen);seen.add(j['id']);raw=json.loads((src/(j['id']+'.json')).read_text());check(j['id']+' compact record matches raw result',r=={k:v for k,v in raw.items() if k not in ['initial','final','samples']});check(j['id']+' finite complete states',all(len(state)==17 and all(math.isfinite(v) for v in state) for state in raw['initial']+raw['final']));rp=r['replay'];b=(src/rp['file']).read_bytes();stride=rp['valuesPerFrame']*8;check(j['id']+' bytes',len(b)==stride*rp['frames']);frames=[struct.unpack('<'+'d'*rp['valuesPerFrame'],b[i*stride:(i+1)*stride]) for i in range(rp['frames'])];check(j['id']+' times',frames[0][0]==0 and all(a[0]<b[0] for a,b in zip(frames,frames[1:])) and abs(frames[-1][0]-r['metrics']['end'])<1e-9);check(j['id']+' exact endpoints',list(frames[0][1:])==[v for s in raw['initial'] for v in s[:3]+s[6:10]] and list(frames[-1][1:])==[v for s in raw['final'] for v in s[:3]+s[6:10]])
 check(j['id']+' identical starting states across models',j['count'] not in starts or starts[j['count']]==raw['initial']);starts[j['count']]=raw['initial'];key=(j['count'],j['aeroMode']);state=(raw['initial'],raw['final'],raw['metrics']);check(j['id']+' deterministic repetition',key not in repeats or state==repeats[key]);repeats[key]=state
final=(root/'milestone-29-summary.json').exists()
if final:
 check('All48 cases completed',len(seen)==48)
 check('Final summary matches complete progress',json.loads((root/'milestone-29-summary.json').read_text())==rs)
 index=json.loads((src/'index.json').read_text());check('Exactly16 representative first repeats',len(index)==16 and {x['job']['id'] for x in index}=={r['job']['id'] for r in rs if r['job']['repeat']==1})
(root/'milestone-29-artifact-checks.json').write_text(json.dumps({'studyComplete':final,'completedRuns':len(rs),'checks':checks},indent=2));print({'runs':len(rs),'checks':len(checks),'complete':final})
