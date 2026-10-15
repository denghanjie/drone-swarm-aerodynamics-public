"""Saved-record verification only. Usage: python3 m31-envelope-recompute.py REPO.
No model imports/evaluations, new poses, samples, refinements, or experiments.
Writes /tmp/m31-envelope-review.json; source/output references are portable.
"""
import hashlib,json,math,statistics,sys,time
from pathlib import Path
start=time.perf_counter()
if len(sys.argv)!=2: raise SystemExit('Usage: python3 m31-envelope-recompute.py REPOSITORY')
repo=Path(sys.argv[1]).resolve();base=repo/'research/m31-refresh-envelope-2026-10-15'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=read(base/'config.json');R=read(base/'results/result.json');A=read(base/'raw/accuracy.json')
V=read(base/'raw/verification.json');D=read(base/'raw/envelope-decisions.json')
F=read(base/'freeze.json');budget=read(base/'results/budget.json')
with (base/'raw/samples.ndjson').open() as stream: rows=[json.loads(line) for line in stream]
checks=[]
def check(ok,name):checks.append({'passed':bool(ok),'check':name})
def close(x,y):return math.isclose(x,y,rel_tol=3e-14,abs_tol=1e-27)
def arrayclose(x,y):return len(x)==len(y) and all(close(a,b) for a,b in zip(x,y))
review={'scope':'Independent saved-record arithmetic/source review; no model evaluation or new samples.',
 'method':{'script':'m31-envelope-recompute.py','scriptSha256':sha(Path(__file__)),
 'rms':'sqrt(fsum of squared-error trapezoids / duration); prior post-refresh value starts each interval, current refresh-left value ends it when present.',
 'peak':'Uniform observations and all recorded refresh-left values; all refreshes checked to lie on both grids.',
 'coverageSign':'instantaneous reference minus treatment; exactly matches saved load-difference intervals.',
 'timing':'Exact sequential checksum from saved primary loads; counts/order/statistics read and recomputed without benchmark rerun.'},
 'sourceCommit':R['sourceCommit'],'rawHashes':[],'sourceHashes':[],'metrics':[],
 'timing':[],'samplingFailures':[],'targetExceedances':[]}
check(R['sourceCommit']=='f56909390c4875db5a9241ba6bc79596b84628a6','source commit')
check(read(base/'raw/started.json')['sourceCommit']==R['sourceCommit'],'start source')
check(R==read(base/'raw/result.json') and R['config']==C,'raw/result/config equality')
for entry in F['files']:
 p=repo/entry['path'];h=sha(p);ok=h==entry['sha256'] and p.stat().st_size==entry['bytes']
 check(ok,'frozen '+entry['path']);review['sourceHashes'].append({'path':entry['path'],'sha256':h,'matches':ok})
for p in sorted((base/'raw').iterdir()):
 review['rawHashes'].append({'path':str(p.relative_to(repo)),'bytes':p.stat().st_size,'sha256':sha(p)})
check([r['tick'] for r in rows]==list(range(C['finalTick']+1)),'complete ordered 4001 saved ticks')
check(all([v['id'] for v in r['values']]==C['variants'] for r in rows),'six variant order')
check(C['primaryStride']==2 and C['fineStride']==1,'stored primary/fine strides')
weight=.027*9.81;motor=2*math.sqrt(2)*.028
budgets=[C['forceBudgetMgFraction']*weight]+[C['momentBudgetMgDFraction']*weight*motor]*2
check(budgets==R['budgets']==A['budgets'],'numerical budgets')
refresh={vid:[r['tick'] for r in rows if r['values'][i]['refresh']] for i,vid in enumerate(C['variants'])}
decision_by_tick={d['tick']:d for d in D};decision_attempts=sum(len(d['attempts']) for d in D)
check(len(decision_by_tick)==len(D) and D[0]['tick']==0,'unique initial decision chain')
check([d['tick'] for d in D]+[C['finalTick']]==refresh['envelope'],'envelope decision/refresh schedule')
check(all(d['tick']+d['hTick']==(D[i+1]['tick'] if i+1<len(D) else C['finalTick']) for i,d in enumerate(D)),'contiguous envelope horizons')
check(R['refreshCount']==len(D)+1,'terminal refresh included')
coeff=[[1,1,1,1],[.028,.028,-.028,-.028],[-.028,.028,.028,-.028]]
def signed_sum(intervals,cs):
 lo=hi=0.0
 for (a,b),c in zip(intervals,cs):
  lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return [lo,hi]
for decision in D:
 tick=decision['tick'];b=decision['bound'];attempts=decision['attempts'];valid_h=[h for h in C['horizonTicks'] if tick+h<=C['finalTick']]
 check([a['hTick'] for a in attempts]==valid_h[:len(attempts)],'longest-first attempts '+str(tick))
 accepted=[a for a in attempts if a['domainAccepted'] and all(x<=lim for x,lim in zip(a['maxAbsError'],budgets))]
 check(len(accepted)==1 and accepted[0] is attempts[-1] and decision['hTick']==accepted[0]['hTick'],'first acceptable horizon '+str(tick))
 check(b['accepted'] and not b['domainRejected'] and b['formallyCertified'] is False,'accepted noncertified bound '+str(tick))
 check(b['errorSign']=='instantaneous minus held','interval sign '+str(tick))
 h=decision['hTick']*C['tickSeconds'];speed=math.hypot(*rows[tick]['velocity'])
 delta=min(R['Vmax']*h,speed*h+.5*R['Amax']*h*h)
 check(close(delta,decision['delta']) and decision['delta']==attempts[-1]['delta'],'saved-velocity displacement arithmetic '+str(tick))
 intervals=b['intervals'];rotor=intervals['rotorThrusts_N'];held=b['heldRotorLoads_N']
 diffs=[[lo-held[k],hi-held[k]] for k,(lo,hi) in enumerate(rotor)]
 check(diffs==intervals['rotorLoadDifferences_N'],'rotor subtraction '+str(tick))
 loads=[signed_sum(diffs,cs) for cs in coeff]
 check(loads==intervals['loadDifferences'],'signed force/roll/pitch interval sum '+str(tick))
 check([signed_sum(rotor,cs) for cs in coeff]==intervals['modeledLoads'],'modeled interval sum '+str(tick))
 max_abs=[max(abs(lo),abs(hi)) for lo,hi in loads]
 check(max_abs==b['maxAbsError']==attempts[-1]['maxAbsError'],'maxAbs interval arithmetic '+str(tick))
 check(all(e<=lim for e,lim in zip(max_abs,budgets)),'accepted numerical targets '+str(tick))
 check(all(math.isfinite(x) for pair in intervals['winds_mps']+rotor+loads for x in pair),'finite accepted intervals '+str(tick))
 check(all(lo<=hi for lo,hi in intervals['winds_mps']+rotor+loads),'ordered accepted intervals '+str(tick))
 check(all(g['downstream_m'][0]>=2.5*motor for g in b['geometry']),'far-field interval domain '+str(tick))
 check(arrayclose(b['heldWrench'],rows[tick]['values'][-1]['loads']),'held load anchor '+str(tick))

coverage={'samples':0,'maxExcess':-math.inf,'worst':None,'targetViolations':0}
for i,vid in enumerate(C['variants']):
 events=refresh[vid]
 if vid!='instant':check(all(t%C['primaryStride']==0 for t in events),'all refreshes on primary grid '+vid)
 previous=None;before_previous=None
 for row in rows:
  tick=row['tick'];v=row['values'][i];instant=row['values'][0]
  if vid=='instant':check(v['left'] is None and v['bound'] is None,'instant scope '+str(tick));continue
  check((v['left'] is not None)==(v['refresh'] and tick>0),'left-limit event accounting '+vid+' '+str(tick))
  if v['left'] is not None:
   if vid!='predict-5ms':check(v['left']['winds']==rows[previous]['values'][i]['winds'] and v['left']['loads']==rows[previous]['values'][i]['loads'],'old hold at event '+vid+' '+str(tick))
   else:
    ref=rows[previous]['values'][0]['winds']
    predicted=ref if before_previous is None else [max(0,u+(u-p)*((tick-previous)/(previous-before_previous))) for u,p in zip(ref,rows[before_previous]['values'][0]['winds'])]
    check(predicted==v['left']['winds'],'causal prediction left '+str(tick))
  if v['refresh']:
   check(v['winds']==instant['winds'] and v['loads']==instant['loads'],'refresh matches saved reference '+vid+' '+str(tick))
   before_previous,previous=previous,tick
  if vid=='predict-5ms':
   ref=rows[previous]['values'][0]['winds']
   predicted=ref if before_previous is None else [max(0,u+(u-p)*((tick-previous)/(previous-before_previous))) for u,p in zip(ref,rows[before_previous]['values'][0]['winds'])]
   check(predicted==v['winds'],'causal prediction sample '+str(tick))
  else:check(v['winds']==rows[previous]['values'][0]['winds'] and v['loads']==rows[previous]['values'][0]['loads'],'constant stored hold '+vid+' '+str(tick))
  if vid!='envelope':continue
  for side,item in [('sample',v)]+([('left',v['left'])] if v['left'] is not None else []):
   bound=item['bound']
   if bound is not None:
    d=decision_by_tick[bound['anchor']]
    check(bound['intervals']==d['bound']['intervals']['loadDifferences'],'linked coverage interval '+str(tick)+' '+side)
    check(d['tick']<=tick<=d['tick']+d['hTick'],'coverage within horizon '+str(tick)+' '+side)
   else:check(tick==C['finalTick'] and side=='sample','only terminal sample has no future bound')
   for k in range(3):
    error=instant['loads'][k]-item['loads'][k]
    coverage['targetViolations']+=abs(error)>budgets[k]+C['containmentCheckTolerance']
    if bound is not None:
     lo,hi=bound['intervals'][k];excess=max(lo-error,error-hi);coverage['samples']+=1
     if excess>coverage['maxExcess']:
      coverage['maxExcess']=excess;coverage['worst']={'tick':tick,'k':k,'side':side,'error':error,'interval':[lo,hi],'anchor':bound['anchor']}
check(coverage==R['coverage']==A['coverage']==V['coverage'],'coverage reconstructed exactly')
check(coverage['maxExcess']<=C['containmentCheckTolerance'] and coverage['targetViolations']==0,'sampled envelope containment and targets')

max_peak_delta=0.;max_rms_delta=0.;duration=C['finalTick']*C['tickSeconds'];computed={}
for vi,vid in enumerate(C['variants']):
 saved=next(m for m in R['metrics'] if m['id']==vid);comp={'id':vid}
 for name,stride in [('primary',C['primaryStride']),('refined',C['fineStride'])]:
  summary=[]
  for k,observable in enumerate(['thrust','roll','pitch']):
   candidates=[];areas=[]
   for tick in range(0,C['finalTick']+1,stride):
    row=rows[tick];v=row['values'][vi];ref=row['values'][0]['loads'][k]
    e=v['loads'][k]-ref;candidates.append((abs(e),tick,'sample'))
    if v['left'] is not None:candidates.append((abs(v['left']['loads'][k]-ref),tick,'left'))
    if tick:
     prior=rows[tick-stride];e0=prior['values'][vi]['loads'][k]-prior['values'][0]['loads'][k]
     e1=(v['left']['loads'][k] if v['left'] is not None else v['loads'][k])-ref
     areas.append((e0*e0+e1*e1)*.5*stride*C['tickSeconds'])
   peak,tick,side=max(candidates,key=lambda x:x[0]);rms=math.sqrt(math.fsum(areas)/duration)
   m={'observable':observable,'peak':peak,'rms':rms,'worstTick':tick,'worstSide':side,'budget':budgets[k],'peakWithinBudget':peak<=budgets[k]+C['containmentCheckTolerance']}
   old=saved[name][k];max_peak_delta=max(max_peak_delta,abs(peak-old['peak']));max_rms_delta=max(max_rms_delta,abs(rms-old['rms']))
   check(peak==old['peak'] and close(rms,old['rms']) and (tick,side)==(old['worstTick'],old['worstSide']),'peak/RMS/location '+vid+' '+name+' '+observable)
   check(m['peakWithinBudget']==old['peakWithinBudget'],'numerical target classification '+vid+' '+name+' '+observable)
   if name=='refined' and not m['peakWithinBudget']:review['targetExceedances'].append({'variant':vid,**m})
   summary.append(m)
  comp[name]=summary
 sampling=[]
 for k,observable in enumerate(['thrust','roll','pitch']):
  primary,fine=comp['primary'][k],comp['refined'][k];floor=C['momentSamplingFloor'] if k else C['forceSamplingFloor']
  decision={'observable':observable}
  for q in ['peak','rms']:
   delta=abs(primary[q]-fine[q]);threshold=max(C['samplingRelativeTolerance']*fine[q],floor)
   decision[q+'Difference']=delta;decision[q+'Stable']=delta<=threshold
   check(decision[q+'Stable']==saved['sampling'][k][q+'Stable'],'sampling screen '+vid+' '+q+' '+observable)
   if not decision[q+'Stable']:review['samplingFailures'].append({'variant':vid,'quantity':q,'observable':observable,'difference':delta,'threshold':threshold})
  sampling.append(decision)
 comp['sampling']=sampling;review['metrics'].append(comp);computed[vid]=comp

timings=[read(p) for p in sorted((base/'raw').glob('timing-*.json'))]
check(len(timings)==36,'36 timing rows')
for pass_id in range(6):
 actual=[t['id'] for t in timings if t['pass']==pass_id]
 check(actual==[C['variants'][(pass_id+j)%6] for j in range(6)],'rotated order '+str(pass_id))
for vi,vid in enumerate(C['variants']):
 checksum=0.
 for tick in range(0,C['finalTick']+1,C['primaryStride']):
  a=rows[tick]['values'][vi]['loads'];checksum+=(a[0]+a[1])+a[2]
 selected=[t for t in timings if t['id']==vid];expected_fields=2001 if vid=='instant' else len(refresh[vid]);expected_bounds=decision_attempts if vid=='envelope' else 0
 check(len(selected)==6 and {t['pass'] for t in selected}==set(range(6)),'passes '+vid)
 check(all(t['checksum']==checksum and t['fieldCalls']==expected_fields and t['boundCalls']==expected_bounds and t['warmup']==(t['pass']==0) for t in selected),'checksums/calls/warmup '+vid)
 check(checksum==A['expectedPrimaryChecksums'][vid],'accuracy checksum '+vid)
 vals=[t['totalMs'] for t in selected if not t['warmup']];stats={'minimum':min(vals),'median':statistics.median(vals),'maximum':max(vals)}
 old=next(t for t in R['timingSummary'] if t['id']==vid)
 check(stats==old['totalMs'] and expected_fields==old['fieldCalls'] and expected_bounds==old['boundCalls'],'timing summary '+vid)
 review['timing'].append({'id':vid,'totalMs':stats,'fieldCalls':expected_fields,'boundCalls':expected_bounds,'checksum':checksum})
timed_fields=sum(t['fieldCalls'] for t in timings);timed_bounds=sum(t['boundCalls'] for t in timings)
science_fields=2*len(rows)+sum(len(refresh[v]) for v in C['variants'] if v!='instant')+1
science_bounds=decision_attempts+4
check(R['fieldCalls']==science_fields+timed_fields==27709,'all field calls including oracle and fixture')
check(R['oracleCalls']==len(rows) and V['oracleCalls']==len(rows),'oracle counts')
check(R['boundCalls']==science_bounds+timed_bounds==4309,'all bound calls including rejected fixtures')
check(V['fieldCalls']==science_fields and V['boundCalls']==science_bounds,'verification/timing accounting')
check(A['metrics']==R['metrics'],'accuracy/result metrics equality')
raw_bytes=sum(p.stat().st_size for p in (base/'raw').iterdir())
check(raw_bytes==budget['entries'][0]['rawBytesAfter']==6278564,'raw bytes')
check(not R['physicalValidation'] and not R['formalFloatingPointCertificate'] and not R['noveltyEstablished'],'limited result scope')
review['coverage']=coverage
review['accounting']={'rawBytes':raw_bytes,'fieldCalls':R['fieldCalls'],'oracleCalls':R['oracleCalls'],'boundCalls':R['boundCalls'],
 'scienceFieldCalls':science_fields,'scienceBoundCalls':science_bounds,'timingFieldCalls':timed_fields,'timingBoundCalls':timed_bounds,
 'envelopeDecisions':len(D),'attemptsPerEnvelopePass':decision_attempts,'refreshesPerEnvelopePass':len(refresh['envelope']),
 'pilotSupervisorWallSeconds':budget['entries'][0]['wallSeconds'],'experimentElapsedSeconds':R['elapsedSeconds']}
ts={t['id']:t['totalMs'] for t in review['timing']};env=ts['envelope'];pred=ts['predict-5ms'];fixed=ts['hold-2.5ms']
review['comparisons']={'predict5msLowerPeakForEveryObservable':all(p['peak']<e['peak'] for p,e in zip(computed['predict-5ms']['refined'],computed['envelope']['refined'])),
 'predict5msRecordedRangeStrictlyBelowEnvelope':pred['maximum']<env['minimum'],
 'envelopeAndHold2p5msRecordedRangesOverlap':max(env['minimum'],fixed['minimum'])<=min(env['maximum'],fixed['maximum']),
 'envelopeMedianVsHold2p5msFraction':env['median']/fixed['median']-1}
review['sourceSemantics']=[
 'Containment checks use reference minus held; peak/RMS code uses treatment minus reference. Squaring/absolute value removes the sign, while interval coverage uses the correct original sign.',
 'Every refresh event is on both grids. Trapezoids terminate at old left-limit values and restart from new post-refresh values; no interval bridges a refresh jump.',
 'Predictor uses only two previous actual inflow samples, clips extrapolated inflow at zero, and holds before its second refresh; these saved winds were recomputed arithmetically without the field or receiver model.',
 'Envelope accepted intervals and moment signs were reconstructed from saved rotor thrust intervals and held rotor loads, without reevaluating bounds, fields, or bisection.',
 'Shortest-horizon failure, oracle mismatch, sampled interval violation, or envelope target failure throws before timing; source catch retains detailed failure context and preceding rows. Hard watchdog termination may preserve only already-written evidence.',
 'Scheduler/bound/receiver and pose overhead are included in the full query loop; verification, persistence, and absent flight/Boids/render/GPU operations are excluded.',
 'Observed coverage and successful sampling screens are restricted to this encounter and saved grids. Margins are not certified outward rounding and no physical or general cadence/safety acceptance follows.',
 'No meaningful speed advantage over hold-2.5ms is established by overlapping five-repeat ranges; the causal predictor has lower peak errors and a lower nonoverlapping recorded time range in this encounter.'
]
review['maximumMetricDiscrepancy']={'peak':max_peak_delta,'rms':max_rms_delta}
review['checkCount']=len(checks);review['failedChecks']=[c for c in checks if not c['passed']];review['passed']=not review['failedChecks']
review['verificationWallSecondsBeforeOutput']=time.perf_counter()-start
Path('/tmp/m31-envelope-review.json').write_text(json.dumps(review,indent=2,allow_nan=False)+'\n')
print(json.dumps({'passed':review['passed'],'checks':len(checks),'failedChecks':review['failedChecks'],
 'coverage':coverage,'samplingFailures':review['samplingFailures'],'comparisons':review['comparisons'],
 'metricDiscrepancy':review['maximumMetricDiscrepancy'],'verificationWallSecondsIncludingOutput':time.perf_counter()-start},indent=2))
