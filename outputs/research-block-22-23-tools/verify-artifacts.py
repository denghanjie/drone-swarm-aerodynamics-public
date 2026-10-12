from pathlib import Path
import json,hashlib,re,math
root=Path(__file__).resolve().parents[1]
errors=[];totals={}
def require(test,msg):
 if not test:errors.append(msg)
def key(c):return tuple(c.get(x) for x in ['seed','scenario','observationDelay','estimator','dt'])
for stage in [22,23]:
 protocol=json.loads((root/f'milestone-{stage}-protocol.json').read_text());study=json.loads((root/f'milestone-{stage}-study.json').read_text());demo=json.loads((root/f'milestone-{stage}-source/demo.json').read_text());summ=json.loads((root/f'milestone-{stage}-summary.json').read_text());index={key(r['config']):r for r in study}
 require(len(index)==len(study)==len(protocol['jobs']),f'{stage}: trial count/duplicate')
 require(set(index)=={key(j) for j in protocol['jobs']},f'{stage}: protocol cases')
 for name,h in protocol['hashes'].items():require(hashlib.sha256((root/f'milestone-{stage}-source'/name).read_bytes()).hexdigest()==h,f'{stage}: hash {name}')
 for r in study:
  c=r['config'];require(c['count']==50 and c['duration']==60,f'{stage}: run constants')
  other=index.get((c['seed'],c['scenario'],c['observationDelay'],'predict' if c['estimator']=='raw' else 'raw',.0025))
  if other:require(r['initial']==other['initial'],f'{stage}: paired starts')
  saved=json.loads((root/f'milestone-{stage}-source'/f'run-{c["seed"]}-{c["scenario"]}-{c["observationDelay"]}-{c["estimator"]}-{c["dt"]}.json').read_text())
  require({k:v for k,v in saved.items() if k!='frames'}==r,f'{stage}: individual record')
  require(all(math.isfinite(x) for s in r['final'] for x in s),f'{stage}: finite final')
 for r in demo:
  ref=index[key(r['config'])];require({k:v for k,v in r.items() if k!='frames'}==ref,f'{stage}: demo exact record')
  f=r['frames'];require(all(len(x)==351 for x in f),f'{stage}: frame shape')
  require(f[-1][0]==r['metrics']['end'],f'{stage}: final time')
  for i in range(50):require(f[-1][1+7*i:8+7*i]==r['final'][i][:3]+r['final'][i][6:10],f'{stage}: exact final pose')
 require(len(demo)==sum(j['record'] for j in protocol['jobs']),f'{stage}: all primary replays retained')
 html=(root/f'milestone-{stage}-lab.html').read_text()
 for link in re.findall(r'(?:href|src)="([^"#]+)"',html):
  if not link.startswith(('http','data:')):require((root/link).exists(),f'{stage}: missing link {link}')
 for v in re.findall(r'<option value="(\d+:[^\"]+)"',html):
  seed,course,delay=v.split(':');require(sum(r['config']['seed']==int(seed) and r['config']['scenario']==course and r['config']['observationDelay']==float(delay) for r in demo)==2,f'{stage}: selector {v}')
 totals[stage]={'runs':len(study),'replays':len(demo),'protocolHashes':len(protocol['hashes'])}
for f in ['sim.cjs','observer.cjs','continuous.cjs','soft-filter.cjs','courses.json']:
 require((root/'milestone-22-source'/f).read_bytes()==(root/'milestone-23-source'/f).read_bytes(),f'Frozen22→23: {f}')
a=json.loads((root/'milestone-22-refinement-audit-protocol.json').read_text())
for n,h in a['hashes'].items():require(hashlib.sha256((root/'milestone-22-source'/n).read_bytes()).hexdigest()==h,f'Audit hash {n}')
require((root/'research-results.html').read_bytes()==(root/'milestone-23-lab.html').read_bytes(),'Dashboard differs from23')
# Exact cross-check against existing checkpoint21 records, without rerunning physics.
old=[]
for f in ['milestone-21-study.json','milestone-21-failure-audit-runs.json']:
 old.extend(json.loads((root/f).read_text()))
regressions=0
for r in json.loads((root/'milestone-22-study.json').read_text()):
 c=r['config']
 if c['estimator']!='raw':continue
 matches=[x for x in old if all(x['config'].get(k)==c[k] for k in ['seed','scenario','observationDelay','dt'])]
 for x in matches:
  regressions+=1
  require(all(r[k]==x[k] for k in ['initial','final','crossings','metrics','samples']),f'Raw checkpoint21 regression:{c}')
totals['exactRawRegressions']=regressions
# Adaptive raw-stop audits are intentionally separate from planned case counts.
audit=json.loads((root/'milestone-23-failure-audit-protocol.json').read_text())
for name,h in audit['hashes'].items():require(hashlib.sha256((root/'milestone-23-source'/name).read_bytes()).hexdigest()==h,f'Raw audit hash:{name}')
ars=json.loads((root/'milestone-23-failure-audit-runs.json').read_text())
require({key(j) for j in audit['jobs']}=={key(r['config']) for r in ars},'Raw audit selection coverage')
totals['rawFailureAuditRuns']=len(ars)
result={'stages':totals,'auditRuns':1+len(ars),'checks':'Protocol case coverage; frozen source hashes; paired starts; individual/study/demo exact equality; finite final states; all primary replays; final poses; HTML links/selectors; frozen22→23 controller; audit hashes; main viewer equality','errors':errors}
(root/'research-block-22-23-artifact-checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
