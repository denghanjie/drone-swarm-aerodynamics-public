from common import *
from decimal import Decimal, getcontext, Inexact
getcontext().prec=80
getcontext().traps[Inexact]=True
D=Decimal; Z=D(0); TOL=D(CFG['toleranceMs'])
WRAPPER=['input','buildAndAdmission','schedule','solve','residual','loads','consumption','finalization']
KERNEL=['input','index','geometry','admission']
def dec(v):
 assert type(v) in (int,Decimal) and D(v).is_finite()
 return D(v)
def txt(v):
 v=dec(v)
 if v==0:return '0'
 s=format(v,'f');return s.rstrip('0').rstrip('.') if '.' in s else s
def parse(b):return json.loads(b,parse_float=D)
def fresh():return {'count':0,'outerMs':Z,'innerMs':Z,'encodePersistMs':Z,'comparisonMs':Z,'leavesMs':{}}
def add(a,r):
 a['count']+=1
 for k in ['outerMs','innerMs','encodePersistMs','comparisonMs']:a[k]+=D(r[k])
 for k,v in r['leavesMs'].items():a['leavesMs'][k]=a['leavesMs'].get(k,Z)+D(v)
def serial(a):return {'count':a['count'],**{k:txt(a[k]) for k in ['outerMs','innerMs','encodePersistMs','comparisonMs']},'leavesMs':{k:txt(v) for k,v in sorted(a['leavesMs'].items())}}
def winner(a):return sorted((k for k in a['leavesMs'] if k!='timerResidual'),key=lambda k:(-a['leavesMs'][k],k))[0]
out=Output('producer','results');code=0
try:
 pub=gate();raw=committed(CFG['inputs']['queries']);groupraw=committed(CFG['inputs']['groups']);groups=[parse(x) for x in groupraw.splitlines()];assert len(groups)==108
 stages=[json.loads(x) for x in committed(CFG['inputs']['stages']).splitlines()];assert len(stages)==1920
 old=json.loads(committed(CFG['inputs']['oldSummary']));old_audit=json.loads(committed(CFG['inputs']['oldAudit']));assert old_audit['passed'] and old_audit['summary']==old
 expected=[]
 for j,g in enumerate(groups):
  assert g['rep']==j//12-1 and g['window']==j%12 and g['order']==(['F','C'] if (g['rep']+g['window']+10)%2==0 else ['C','F'])
  for method in g['order']:
   expected.extend((g['rep'],g['window'],method,i) for i in range(160))
 pooled={};perrep={};buckets={};viewer={};seen=set();count=0
 for line in raw.splitlines():
  out.tick();q=parse(line);count+=1
  key=(q['rep'],q['window'],q['method'],q['index']);assert key==expected[count-1] and q['call']==count and key not in seen;seen.add(key)
  assert q['referenceEqual'] and q['inputPreserved'] and q['methodValid']
  if q['method']=='F':assert q['baselineReferenceEqual']
  stage=stages[q['window']*160+q['index']];assert stage['window']==q['window'] and stage['index']==q['index'] and stage['status']==q['status']
  success=q['status']=='native-success';assert success or (q['status']=='domain-refused' and q['reason']=='native-admission' and stage['admissionReasons']==['near-field'] and stage['nativeStage']=='build' and q['window']==2 and q['index']==159)
  timing=q['excluded']['timing'];ph={k:dec(v) for k,v in timing['phasesMs'].items()};assert set(ph)==set(WRAPPER if success else ['input','finalization']);assert all(v>=0 for v in ph.values())
  outer=dec(q['outerMs']);inner=dec(timing['totalMs']);assert outer>=0 and inner>=0
  residual=inner-sum(ph.values(),Z);boundary=outer-inner;assert abs(residual)<=TOL and boundary>=-TOL
  kernel=q['excluded'].get('diagnostics.buildPhasesMs');build_other=None
  if success:
   assert kernel is not None and set(kernel)==set(KERNEL);kernel={k:dec(v) for k,v in kernel.items()};assert all(v>=0 for v in kernel.values())
   build_other=ph['buildAndAdmission']-sum(kernel.values(),Z);assert build_other>=-TOL
   leaves={k:v for k,v in ph.items() if k!='buildAndAdmission'}
   leaves.update({'kernelInput':kernel['input'],'kernelIndex':kernel['index'],'geometry':kernel['geometry'],'kernelAdmission':kernel['admission'],'buildUnassigned':build_other})
  else:
   assert kernel is None and 'diagnostics.buildPhasesMs' not in q['excluded']
   leaves={'input':ph['input'],'unfinishedPhaseAndFinalization':ph['finalization']}
  leaves.update(outerBoundary=boundary,timerResidual=residual);assert sum(leaves.values(),Z)==outer
  evidence=dec(q['encodePersistMs']);comparison=dec(q['comparisonMs']);assert evidence>=0 and comparison>=0 and comparison<=evidence+TOL
  r={'call':count,'window':q['window'],'index':q['index'],'rep':q['rep'],'method':q['method'],'status':q['status'],'reason':q['reason'],'outerMs':txt(outer),'innerMs':txt(inner),'phasesMs':{k:txt(v) for k,v in sorted(ph.items())},'kernelPhasesMs':None if kernel is None else {k:txt(v) for k,v in sorted(kernel.items())},'leavesMs':{k:txt(v) for k,v in sorted(leaves.items())},'encodePersistMs':txt(evidence),'comparisonMs':txt(comparison)}
  out.save('rows.jsonl',r,True)
  bucket='warmup' if q['rep']==-1 else 'measured';keys=[(bucket,q['method'],q['status']),(q['rep'],q['method'],q['status']),(q['rep'],q['window'],q['method'],q['status'])]
  for table,k in zip([pooled,perrep,buckets],keys):add(table.setdefault(k,fresh()),r)
  if q['rep']==0:
   v=viewer.setdefault((q['window'],q['index']),{'window':q['window'],'index':q['index'],'status':q['status'],'methods':{}});assert v['status']==q['status'];v['methods'][q['method']]={'outerMs':r['outerMs'],'innerMs':r['innerMs'],'leavesMs':r['leavesMs']}
 assert count==len(expected)==34560
 reconciled=[]
 for g in groups:
  for m in ['F','C']:
   good=buckets.get((g['rep'],g['window'],m,'native-success'),fresh());bad=buckets.get((g['rep'],g['window'],m,'domain-refused'),fresh());a=g[m];reset=dec(a['resetMs']);assert reset>=0
   deltas={'sumQueryMs':good['outerMs']+bad['outerMs']-dec(a['sumQueryMs']),'admittedMs':good['outerMs']-dec(a['admittedMs']),'refusedMs':bad['outerMs']-dec(a['refusedMs']),'totalMs':good['outerMs']+bad['outerMs']+reset-dec(a['totalMs'])}
   assert all(abs(v)<=TOL for v in deltas.values()) and good['count']==a['admittedCalls'] and bad['count']==a['refusedCalls']
   reconciled.append({'rep':g['rep'],'window':g['window'],'method':m,'resetMs':txt(reset),'loggedTotalMs':txt(dec(a['totalMs'])),'signedDeltasMs':{k:txt(v) for k,v in sorted(deltas.items())}})
 primary=pooled[('measured','F','native-success')];assert primary['outerMs']>0 and all(perrep[(i,'F','native-success')]['outerMs']>0 for i in range(8));lead=winner(primary);rep_winners=[{'rep':i,'component':winner(perrep[(i,'F','native-success')])} for i in range(8)];wins=sum(x['component']==lead for x in rep_winners);majority=primary['leavesMs'][lead]>=primary['outerMs']/2
 decision={'largestComponent':lead,'numeratorMs':txt(primary['leavesMs'][lead]),'denominatorMs':txt(primary['outerMs']),'sameWinnerReps':wins,'perRepWinners':rep_winners,'atLeastHalf':majority,'stableMajority':majority and wins>=6,'classification':'stable-majority-component' if majority and wins>=6 else 'distributed-or-unstable','interpretation':'Descriptive priority for source inspection only; not a causal speedup prediction or a revised qualification gate.'}
 def records(table,names):return [dict(zip(names,k),**serial(a)) for k,a in sorted(table.items())]
 summary={'schema':'m31-phase-attribution-result-v1','complete':True,'nativeCalls':0,'calls':count,'stages':1920,'arithmetic':'Exact sums/differences of logged decimal values at precision80; no extra measurement precision. Shares are numerator/denominator pairs, not rounded decisions.','pooled':records(pooled,['bucket','method','status']),'perRep':records(perrep,['rep','method','status']),'byWindowRep':records(buckets,['rep','window','method','status']),'groupReconciliation':reconciled,'decision':decision,'oldResult':old,'sourceCommit':pub['commit'],'scope':'Descriptive saved timing partition on exposed dependent N64 stages; no new force query, flight, speed measurement or physical validation.','readEvents':EVENTS}
 out.save('summary.json',summary);out.save('viewer-rows.json',[viewer[k] for k in sorted(viewer)])
 out.save('input-binding.json',{'sourceCommit':pub['commit'],'inputs':{k:PINS[v] for k,v in CFG['inputs'].items()},'nativeCalls':0})
except Exception as e:
 code=1;out.failed=True;out.save('failure.json',{'type':type(e).__name__,'message':str(e).replace(str(ROOT),'[repository]')[:1500]})
finally:out.close(code)
sys.exit(code)
