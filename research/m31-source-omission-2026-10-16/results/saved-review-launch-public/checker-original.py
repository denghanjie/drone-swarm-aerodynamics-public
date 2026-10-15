"""Saved-evidence review only; preparation is not execution authorization.
Run once, only after coordinator authorization, under an external <=59 s guard:
python3 m31-omission-saved-review.py REPOSITORY --authorized-after-science
No JavaScript imports, pose generation, geometry, field, root solving or timings.
"""
import base64, contextlib, hashlib, json, math, re, signal, struct, sys, time, traceback, zlib
from collections import Counter
from pathlib import Path
SOURCE='88dc542604d902909b7cc96c0bd0ca93b88cab0c'
FREEZE='855f71dc0f8993ed1fb51eb5e882cfe9c07c5bb5f37ea275e4705bf33114516c'
CAMPAIGN='research/m31-source-omission-2026-10-16'
REFERENCE='research/m31-flock-force-reference-2026-10-15'
ARITH_ABS=2e-16
ARITH_REL=8e-15
START=time.perf_counter()
RUN=Path('/tmp/m31-omission-verifier-runs')/str(time.time_ns())
RUN.mkdir(parents=True,exist_ok=False)
SCRIPT=Path(__file__).read_bytes()
(RUN/'checker.py').write_bytes(SCRIPT)
CHECKS=Counter(); FAILURES=[]; VIOLATIONS=[]; FAILED=0; CURRENT={'phase':'startup'}
REPORT={'scope':'Saved evidence only; no geometry, quaternion rotation, field evaluation, root solving, input generation, fixture execution, integration or timing repeat.',
 'method':{'checkerSha256':hashlib.sha256(SCRIPT).hexdigest(),'invocationArchive':str(RUN),'sourceCommit':SOURCE,'authorizedWallSeconds':60,'internalAlarmSeconds':55,
 'checkerArithmeticTolerance':{'absolute':ARITH_ABS,'relative':ARITH_REL,'residualReconstructionAbsolute':4e-15,'summaryRelative':5e-13,'smallDiscrepancyAbsolute':1e-30},
 'toleranceSeparation':'Checker tolerances apply only to scalar reconstruction and summaries; frozen scientific gates receive no extra checker tolerance. nextUp accumulation is reconstructed as the declared binary64 operation.'},
 'sourceHashes':[],'rawHashes':[],'cases':[],'partialTails':[],
 'limitations':[
 'A passing saved review of a failed campaign confirms retained evidence consistency; it does not turn the scientific failure into a passing qualification.',
 'The generated poses are hash-checked and decoded only for finite layout and prescribed placeholders/motors. No generator, quaternion norm, rotation, geometry or domain predicate is recomputed.',
 'Fresh successful source-audit rows retain all four terms only for positive omissions. Exact-zero term checks and full-code digests are recorded runtime assertions; absent complete vectors/zero doubles are not regenerated.',
 'Historical inputs retain full prior classifications and full resultant loads but no per-source magnitudes; historical omission checks remain aggregate plus prior-code checks.',
 'New output rows omit axes. Body wrench arithmetic and saved world-vector discrepancies are checked, but world rotations cannot be independently reconstructed without forbidden geometry.',
 'Successful timed query output matrices are not retained. Checksums/counters/times and recorded pass assertions can be reconciled, not every repeated output component reconstructed.',
 'C includes exact-zero culling, positive-bound omission, bound/guard work, masking and data-structure overhead. Its C/M or C/B timing ratio does not isolate positive omission alone. A positive upper bound does not imply that every corresponding realized rotor term is positive.',
 'Runtime logical-check count and unavailable partial-call actual instruction counts remain recorded evidence; attempted-call shape counters are independently reconstructed exactly.',
 'Engineering numerical allowances and finite synthetic cases do not establish a universal rounding certificate, physical validity, flight safety, trajectory qualification or algorithmic novelty.']}

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def finite(v): return all(isinstance(x,(float,int)) and not isinstance(x,bool) and math.isfinite(x) for x in v)
def close(a,b,absolute=ARITH_ABS,relative=ARITH_REL): return finite([a,b]) and abs(a-b)<=absolute+relative*max(abs(a),abs(b))
def check(ok,kind,detail=None):
 global FAILED
 CHECKS[kind]+=1
 if not ok:
  FAILED+=1
  if len(FAILURES)<200: FAILURES.append({'check':kind,'context':CURRENT if detail is None else detail})
def must(ok,kind,detail=None):
 check(ok,kind,detail)
 if not ok: raise ValueError('Cannot continue safely: '+kind)
def scientific(ok,kind,required,detail=None):
 CHECKS['scientific observation: '+kind]+=1
 if not ok:
  if len(VIOLATIONS)<200: VIOLATIONS.append({'gate':kind,'acceptedCase':required,'context':CURRENT if detail is None else detail})
  if required: check(False,'accepted evidence violates '+kind,detail)
def nextup(x):
 if x==0: return struct.unpack('<d',struct.pack('<Q',1))[0]
 return struct.unpack('<d',struct.pack('<Q',struct.unpack('<Q',struct.pack('<d',x))[0]+1))[0]
def inflate(b64,size):
 compressed=base64.b64decode(b64,validate=True); decoder=zlib.decompressobj()
 data=decoder.decompress(compressed,size+1)
 must(len(data)==size and decoder.eof and not decoder.unconsumed_tail and not decoder.unused_data,'strict complete deflate payload')
 return data
def ndjson(path,complete):
 if not path.exists(): return []
 data=path.read_bytes(); lines=data.splitlines(); out=[]
 for i,line in enumerate(lines):
  try: out.append(json.loads(line))
  except (ValueError,UnicodeDecodeError):
   if not complete and i==len(lines)-1 and not data.endswith(b'\n'):
    REPORT['partialTails'].append({'path':path.name,'bytes':len(line),'sha256':sha(line),'type':'unparsed terminal NDJSON tail'}); break
   raise
 return out
def rows(path,n,complete):
 if not path.exists(): return None
 data=path.read_bytes(); full=len(data)//136; rest=len(data)%136
 must(full<=n,'binary row coverage within case size',path.name)
 if complete: must(full==n and rest==0,'complete accepted binary row count',path.name)
 if rest:
  must(not complete,'partial binary only in failed/incomplete campaign',path.name)
  REPORT['partialTails'].append({'path':path.name,'bytes':rest,'sha256':sha(data[full*136:]),'type':'partial binary row'})
 return list(struct.iter_unpack('<17d',data[:full*136]))
def power(f,u,area): return f*(u/2+math.sqrt(u*u/4+f/(2*1.225*area)))
def alarm(signum,frame): raise TimeoutError('Saved-review 55-second internal limit')

EXPAND=[bytes((x&3,(x>>2)&3,(x>>4)&3,(x>>6)&3)) for x in range(256)]
NONZERO=bytes([0]+[1]*255)
F0=.027*9.81/4; ARM=.028; AREA=math.pi*.023**2
V0=math.sqrt(F0/(2*1.225*AREA)); NOMINAL=power(F0,0,AREA)

FIXTURES=[]
for stem in ['center3','down0','farStart','downEnd','nearRadius']:
 for suffix in ['-1e-12','0','1e-12']:
  expected='valid'
  if stem in ['farStart','nearRadius'] and suffix=='-1e-12': expected='reject'
  if stem=='nearRadius' and suffix=='0': expected='agreement'
  FIXTURES.append((stem+'-'+suffix,2,expected))
FIXTURES += [('radial-2',2,'valid'),('radial-3',2,'valid'),('downFade2',2,'valid'),('centerInferenceInvalid',2,'reject'),('combinedTiltYaw',2,'valid'),('normDefect',2,'valid'),('tiltRejected',2,'reject'),('multipleWeak',5,'valid'),('signedMoment',3,'valid')]
HISTORICAL=[('historical-case-'+str(ci)+'-t-'+str(t),[1000,1000,5000][ci],'valid') for ci in range(3) for t in [0,20,30,60]]
FRESH=[('fresh1000',1000,'valid'),('fresh5000',5000,'valid')]
CASE_TABLE=FIXTURES+HISTORICAL+FRESH
CASE_INFO={sid:{'n':n,'expected':expected,'kind':'fixture' if i<24 else 'exposed' if i<36 else 'fresh'} for i,(sid,n,expected) in enumerate(CASE_TABLE)}


def verify(repo):
 global CURRENT
 base=repo/CAMPAIGN; raw=base/'raw'; cfg=read(base/'config.json'); schema=read(base/'schema.json')
 freeze_bytes=(base/'freeze.json').read_bytes(); freeze=json.loads(freeze_bytes)
 must(sha(freeze_bytes)==FREEZE and len(freeze['files'])==66,'pinned 66-file freeze')
 for item in freeze['files']:
  CURRENT={'phase':'frozen-file','path':item['path']}
  b=(repo/item['path']).read_bytes(); matched=len(b)==item['bytes'] and sha(b)==item['sha256']
  check(matched,'frozen file hash/size',item['path']); REPORT['sourceHashes'].append({'path':item['path'],'bytes':len(b),'sha256':sha(b),'matches':matched})
 CURRENT={'phase':'outcome-and-inventory'}
 budget=read(base/'results/budget.json'); started=read(raw/'started.json')
 rp=base/'results/result.json'; result=read(rp) if rp.exists() else None
 complete=result is not None and result.get('status')=='completed'
 failed=result is not None and result.get('status')=='failed'
 REPORT['scientificStatus']=result.get('status') if result else 'no driver terminal result; interrupted or preflight failure'
 for p,label in [(base/'results/budget.json','scientific-budget-original.json'),(raw/'started.json','scientific-started-original.json'),(rp,'scientific-result-original.json')]:
  if p.exists(): (RUN/label).write_bytes(p.read_bytes())
 must(started['sourceCommit']==SOURCE and started['cfg']==cfg and started['schema']==schema,'frozen started provenance/config/schema')
 if complete:
  check(result['sourceCommit']==SOURCE and result['config']==cfg and result['schema']==schema,'completed result provenance/config/schema')
  check(result==read(raw/'result.json'),'raw/published successful result equality')
 if failed: check(result==read(raw/'failure.json'),'raw/published failed result equality')
 check(schema['rowType']=='Float64LE' and schema['poseType']=='Float64LE' and schema['rowColumns']==['U0','U1','U2','U3','f0','f1','f2','f3','bodyThrust','roll','pitch','worldFx','worldFy','worldFz','worldMx','worldMy','worldMz'] and schema['poseColumns']==['x','y','z','vx','vy','vz','qx','qy','qz','qw','wx','wy','wz','motor0','motor1','motor2','motor3'],'exact 17-column schemas')
 check(cfg['fixtureCases']==24 and cfg['historicalCases']==12 and cfg['freshCases']==[{'id':'fresh1000','shape':[10,10,10],'seed':733109},{'id':'fresh5000','shape':[20,25,10],'seed':891007}],'frozen cases/seeds/shapes without generation')
 check(cfg['referenceCommit']=='3b8273f17b927d56289a2a3839b047bd6a01a15a' and cfg['referenceManifestSha256']==sha((repo/REFERENCE/'manifest.json').read_bytes()),'closed reference manifest pin')
 limits={'wallCapSeconds':300,'rawByteCap':134217728,'failureReserveBytes':4194304,'fieldCallCap':152,'independentCenterCap':26000000,'boundAttemptShapeCap':290000000,'rotorVisitShapeCap':2750000000,'receiverCallCap':700000,'verificationWallCapSeconds':60}
 check(all(cfg[k]==v for k,v in limits.items()),'unchanged resource caps')
 raw_inventory={}
 for p in sorted(raw.iterdir()):
  must(p.is_file(),'flat raw file inventory',p.name)
  b=p.read_bytes(); raw_inventory[p.name]={'name':p.name,'bytes':len(b),'sha256':sha(b)}
 REPORT['rawHashes']=list(raw_inventory.values()); raw_bytes=sum(v['bytes'] for v in raw_inventory.values())
 listed=[] if result is None else result['files']
 must(len({x['name'] for x in listed})==len(listed),'unique listed evidence names')
 for item in listed: check(raw_inventory.get(item['name'])==item,'retained file inventory hash/size',item['name'])
 if complete: check(set(raw_inventory)=={x['name'] for x in listed}|{'result.json'},'complete successful raw inventory')
 REPORT['unlistedRawFiles']=[v for k,v in raw_inventory.items() if k not in {x['name'] for x in listed}]
 targets=started['targets']; allowances=started['allowances']; L=started['L']; cap=started['Bcap']
 check(allowances=={'geometry':1e-12,'boundRelative':1e-12,'boundAbsolute':1e-12,'rotor':1e-12,'inflowAudit':1e-11},'frozen numerical allowances')
 expected_targets={'thrust':.005*.027*9.81,'roll':.0005*.027*9.81*(2*math.sqrt(2)*ARM),'pitch':.0005*.027*9.81*(2*math.sqrt(2)*ARM)}
 check(all(close(targets[k],v) for k,v in expected_targets.items()) and close(L,F0/(3*V0)),'target and Lipschitz scalar formulas')
 eta=allowances['rotor']
 cap_check=min((targets['thrust']-4*eta)/(4*L),(targets['roll']-4*ARM*eta)/(2*ARM*L),(targets['pitch']-4*ARM*eta)/(2*ARM*L))
 check(close(cap,cap_check) and cap>0,'reserved signed load budget and capacity formulas')
 REPORT['targetsAndAllowances']={'targets':targets,'allowances':allowances,'L':L,'Bcap':cap}
 if (raw/'scalar-checks.json').exists():
  sc=read(raw/'scalar-checks.json');check(sc['checks']==5 and sc['pass'] is True and sc['Bcap']==cap,'retained scalar-check record')
  # Scalar binary64 arithmetic only; no geometry or root evaluation.
  half=cap/2
  check(nextup(0)>0 and nextup(1)==1+sys.float_info.epsilon and math.isinf(nextup(sys.float_info.max)) and nextup(half+half)>cap and nextup(half+half*(1-1e-8))<=cap,'saved capacity scalar identities')
 summaries={} 
 for p in raw.glob('*-summary.json'):
  s=read(p); must(s['id'] in CASE_INFO,'recognized case summary',p.name); summaries[s['id']]=s
 saved_summaries=[summaries[sid] for sid,_,_ in CASE_TABLE if sid in summaries] if result is None else result.get('results',result.get('completedResults',[]))
 for s in saved_summaries: check(summaries.get(s['id'])==s,'terminal/raw completed summary equality',s['id'])
 check([s['id'] for s in saved_summaries]==[x[0] for x in CASE_TABLE[:len(saved_summaries)]],'completed summaries form frozen case prefix')
 if complete: check(len(summaries)==len(saved_summaries)==38,'all 38 case summaries')
 raw_reference=read(repo/REFERENCE/'raw/result.json'); prior_by_id={s['id']:s for s in raw_reference['snapshots']}
 calls=[] if result is None else result.get('calls',[]); call_by_key={(c['id'],c['method']):c for c in calls}
 all_rows={}; diagnostic=Counter()
 def u_tol(a,b): return cfg['inflowAbsTolerance']+cfg['inflowRelTolerance']*max(abs(a),abs(b))
 def row_checks(rs,method,required,sid):
  for i,row in enumerate(rs):
   global CURRENT
   CURRENT={'phase':'saved-output-scalars','case':sid,'method':method,'receiver':i}
   must(finite(row),'finite retained 17-value output row')
   f=list(row[4:8]); T=mx=my=0.0
   for value,(sx,sy) in zip(f,[(1,1),(-1,1),(-1,-1),(1,-1)]): T+=value; mx+=sy*ARM*value; my-=sx*ARM*value
   if method=='I': mx=ARM*(f[0]+f[1]-f[2]-f[3]);my=ARM*(-f[0]+f[1]+f[2]-f[3])
   check(close(row[8],T) and close(row[9],mx) and close(row[10],my),'saved-rotor signed body wrench arithmetic')
   for k in range(4):
    U,thrust=row[k],row[4+k]
    scientific(U>=0 and 0<=thrust<=F0,'Receiver range',required)
    scientific(U!=0 or thrust==F0,'Zero-inflow identity',required)
    x=thrust/F0; alpha=U/V0
    scientific(abs(x*x*x+alpha*x-1)<=cfg['rootResidualTolerance'],'Root residual',required)
    if U>=0 and thrust>=0: scientific(abs(power(thrust,U,AREA)-NOMINAL)<=cfg['powerAbsoluteTolerance']+cfg['powerRelativeTolerance']*abs(NOMINAL),'Power identity',required)
 def full_comparison(rs,ref,required,label):
  maxima=[0.0]*17
  check(len(rs)==len(ref),'full comparison complete equal row counts',label)
  for i,(a,b) in enumerate(zip(rs,ref)):
   for k in range(17):
    d=abs(a[k]-b[k]); maxima[k]=max(maxima[k],d)
    tol=u_tol(a[k],b[k]) if k<4 else cfg['rotorTolerance'] if k<8 else cfg['bodyThrustTolerance'] if k==8 else cfg['bodyMomentTolerance'] if k<11 else cfg['worldForceTolerance'] if k<14 else cfg['worldMomentTolerance']
    scientific(d<=tol,'Full implementation mismatch',required,{'case':label,'receiver':i,'component':k,'difference':d,'tolerance':tol})
  return maxima
 def approximation(rs,ref,decs,required,sid):
  maxima=dict.fromkeys(['inflow','rotor','thrust','roll','pitch','worldForce','worldMoment','usedCapacity'],0.0)
  for i,(a,b,d) in enumerate(zip(rs,ref,decs)):
   B=d['B']; maxima['usedCapacity']=max(maxima['usedCapacity'],B/cap)
   scientific(0<=B<=cap,'Omission capacity',required,{'case':sid,'receiver':i,'B':B})
   for k in range(4):
    du,df=b[k]-a[k],a[4+k]-b[4+k]
    scientific(-u_tol(b[k],a[k])<=du<=B+u_tol(b[k],a[k]),'Aggregate inflow bound',required,{'case':sid,'receiver':i,'rotor':k,'du':du,'B':B})
    scientific(-eta<=df<=L*B+eta,'Rotor error bound/sign',required,{'case':sid,'receiver':i,'rotor':k,'df':df})
    maxima['inflow']=max(maxima['inflow'],abs(du));maxima['rotor']=max(maxima['rotor'],abs(df))
   dt=a[8]-b[8]; mx=abs(a[9]-b[9]); my=abs(a[10]-b[10])
   scientific(-4*eta<=dt<=4*L*B+4*eta,'Thrust analytic bound',required,{'case':sid,'receiver':i,'deltaT':dt,'predictedUpper':4*L*B+4*eta})
   scientific(mx<=2*ARM*L*B+4*ARM*eta and my<=2*ARM*L*B+4*ARM*eta,'Moment analytic bound',required,{'case':sid,'receiver':i,'rollError':mx,'pitchError':my,'predictedUpper':2*ARM*L*B+4*ARM*eta})
   scientific(abs(dt)<=targets['thrust'] and mx<=targets['roll'] and my<=targets['pitch'],'Declared load budget',required,{'case':sid,'receiver':i})
   for key,val in [('thrust',abs(dt)),('roll',mx),('pitch',my),('worldForce',math.hypot(*(a[k]-b[k] for k in range(11,14)))),('worldMoment',math.hypot(*(a[k]-b[k] for k in range(14,17))))]: maxima[key]=max(maxima[key],val)
  return maxima
 for sid,n,expected in CASE_TABLE:
  summary=summaries.get(sid); accepted=summary is not None and summary.get('pass') is True; rejected=bool(summary and summary.get('domain')=='all reject'); kind=CASE_INFO[sid]['kind']
  present=summary is not None or any(p.name.startswith(sid+'-') for p in raw.iterdir())
  if not present: continue
  CURRENT={'phase':'case-coverage','case':sid}
  if summary: check(summary['n']==n and summary['kind']==kind and (kind=='exposed' or summary.get('expected')==expected),'case identity/count/kind/expected decision')
  state_rows=rows(raw/(sid+'-states.f64'),n,accepted and kind!='exposed') if kind!='exposed' else None
  if state_rows is not None:
   for i,s in enumerate(state_rows): check(finite(s) and list(s[3:6])==[0,0,0] and list(s[10:13])==[0,0,0] and all(v==F0 for v in s[13:17]),'saved state layout/finite/prescribed placeholders',{'case':sid,'receiver':i})
   diagnostic['savedStateRows']+=len(state_rows)
  data={}
  for method in ['B','M','C','I']:
   rs=rows(raw/(sid+'-'+method+'.f64'),n,accepted and not rejected)
   if rs is not None: data[method]=rs; row_checks(rs,method,accepted,sid); diagnostic['outputRows']+=len(rs)
  if accepted and not rejected: check(set(data)==({'C'} if kind=='exposed' else {'B','M','C','I'}),'complete accepted method outputs',sid)
  all_rows[sid]=data
  decs=ndjson(raw/(sid+'-decisions.ndjson'),complete); audits=ndjson(raw/(sid+'-source-audit.ndjson'),complete)
  check(len(decs)<=n and len(audits)<=n,'retained receiver prefixes within N',sid)
  if accepted and not rejected: check(len(decs)==n and (kind=='exposed' or len(audits)==n),'complete accepted decision/audit rows',sid)
  mt=[]; totals=Counter(); upstream=None
  if kind=='exposed' and decs:
   old=sid[len('historical-'):]; upstream=ndjson(repo/'research/m31-flock-domain-2026-10-15/raw'/(old+'.ndjson'),True)
   check(len(upstream)==n,'full pinned historical domain rows',sid)
  for i,d in enumerate(decs):
   CURRENT={'phase':'saved-decision-mask','case':sid,'receiver':i}
   must(d['receiver']==i,'ordered decision receivers')
   mask=inflate(d['maskDeflateBase64'],(n+3)//4);check(sha(mask)==d['maskSha256'],'complete decision mask digest')
   expanded=b''.join(EXPAND[v] for v in mask);check(all(x==0 for x in expanded[n:]),'zero unused padding bits');expanded=expanded[:n]
   check(expanded[i]==0,'self mask code zero')
   hc=[expanded.count(bytes([k])) for k in range(4)]
   omitted_ids=[];pos=expanded.find(b'\3')
   while pos>=0: omitted_ids.append(pos);pos=expanded.find(b'\3',pos+1)
   check([pair[0] for pair in d['omitted']]==omitted_ids,'ascending complete positive-omission source identities')
   check(d['candidates']==n-hc[0] and d['zeroCulls']==hc[1] and d['retained']==hc[2] and 0<=d['nearFallbacks']<=hc[2],'mask and decision counter accounting')
   B=ordinary=0.0
   for pair in d['omitted']:
    must(len(pair)==2 and finite(pair) and pair[1]>0,'finite positive source bound')
    ordinary+=pair[1];B=nextup(B+pair[1])
   check(d['B']==B and B>=ordinary,'declared nextUp bound accumulation exact')
   scientific(0<=B<=cap,'Omission capacity',accepted,{'case':sid,'receiver':i,'B':B})
   totals.update({'candidates':n-hc[0],'boundAttempts':n-hc[0],'zeroCulls':hc[1],'positiveOmissions':hc[3],'retained':hc[2],'nearFallbacks':d['nearFallbacks'],'rotorVisits':4*hc[2]})
   if upstream:
    oldrow=upstream[i];codes=inflate(oldrow['codesDeflateBase64'],4*n)
    check(oldrow['receiver']==i and sha(codes)==oldrow['productionCodesSha256']==oldrow['independentCodesSha256'],'pinned prior code vector receiver/hash')
    check(expanded.translate(NONZERO)==codes[0::4].translate(NONZERO),'historical full source-center eligibility correspondence')
    positive=codes.find(b'\7')
    while positive>=0:
     scientific(expanded[positive//4]!=1,'Historical claimed-zero has positive support',accepted,{'case':sid,'receiver':i,'source':positive//4,'rotor':positive%4})
     positive=codes.find(b'\7',positive+1)
    diagnostic['historicalInflatedCodeBytes']+=len(codes)
   mt.append(expanded)
  diagnostic['decisionRows']+=len(decs)
  candidate_was_valid=call_by_key.get((sid,'C'),{}).get('ok',False) if result else ('C' in data)
  for i,audit in enumerate(audits):
   CURRENT={'phase':'saved-independent-source-audit','case':sid,'receiver':i}
   must(audit['receiver']==i and finite(audit['row']) and len(audit['row'])==17,'ordered finite audit output row')
   check(bool(re.fullmatch('[0-9a-f]{64}',audit['codesSha256'])),'retained complete-code digest format')
   if 'I' in data and i<len(data['I']): check(tuple(audit['row'])==data['I'][i],'audit/binary independent output equality')
   if candidate_was_valid and i<len(decs):
    decision=decs[i];mask=mt[i]
    check([[v[0],v[1]] for v in audit['omitted']]==decision['omitted'],'audit/decision positive source and bound identity')
    check(audit['zeroInspections']==4*mask.count(b'\1'),'recorded exact-zero inspection coverage')
    sums=[0.0]*4
    for item in audit['omitted']:
     must(len(item)==6 and finite(item),'finite saved omitted-source term tuple')
     j,B=item[:2]
     for k,v in enumerate(item[2:]):
      scientific(0<=v<=B+allowances['inflowAudit'],'Per-source upper bound',accepted,{'case':sid,'receiver':i,'source':j,'rotor':k,'term':v,'bound':B})
      sums[k]+=v
    check(all(close(a,b) for a,b in zip(sums,audit['omittedSums'])),'four saved omitted sums scalar reconstruction')
    if 'C' in data and i<len(data['C']):
     for k in range(4):
      full,cand=audit['row'][k],data['C'][i][k]
      scientific(abs((full-cand)-sums[k])<=u_tol(full,cand),'Omitted terms do not explain field difference',accepted,{'case':sid,'receiver':i,'rotor':k})
      scientific(sums[k]<=decision['B']+u_tol(full,cand),'Summed omitted terms within retained bound',accepted,{'case':sid,'receiver':i,'rotor':k})
   else: check(not audit['omitted'] and audit['zeroInspections']==0,'no candidate audit when candidate rejected')
   must(len(audit['solutions'])==4,'four retained independent root diagnostics')
   for k,sol in enumerate(audit['solutions']):
    vals=[sol['thrust'],sol['x'],sol['alpha'],sol['residual'],*sol['bracket'],sol['iterations']]
    must(finite(vals),'finite saved independent solution')
    lo,hi=sol['bracket'];x=sol['x'];alpha=sol['alpha'];iters=sol['iterations']
    scientific(0<=lo<=x<=hi<=1 and hi-lo<=cfg['bracketWidthTolerance'] and isinstance(iters,int) and 0<=iters<=96 and abs(sol['residual'])<=cfg['rootResidualTolerance'],'Independent root bracket/residual',accepted,{'case':sid,'receiver':i,'rotor':k})
    check(close(sol['thrust'],audit['row'][4+k]) and close(sol['thrust'],F0*x) and close(alpha,audit['row'][k]/math.sqrt(F0/(2*1.225*(math.pi*.023*.023)))) and close(sol['residual'],x*x*x+alpha*x-1,4e-15),'independent saved root scalar identities')
   diagnostic['auditRows']+=1;diagnostic['retainedPositiveSourceTermTuples']+=len(audit['omitted']);diagnostic['recordedZeroTermChecks']+=audit['zeroInspections']
  if 'I' not in data and audits: row_checks([x['row'] for x in audits],'I',accepted,sid)
  ref=None
  if kind=='exposed' and 'C' in data:
   old=sid[len('historical-'):]; pr=prior_by_id[old]
   rr=(repo/REFERENCE/'raw'/(old+'-rotors.f64')).read_bytes();vv=(repo/REFERENCE/'raw'/(old+'-vehicles.f64')).read_bytes()
   rotorrows=list(struct.iter_unpack('<16d',rr)); vehiclerows=list(struct.iter_unpack('<35d',vv))
   must(len(rotorrows)==4*n and len(vehiclerows)==n,'complete historical saved reference rows')
   ref=[]
   for i,v in enumerate(vehiclerows): ref.append(tuple([rotorrows[4*i+k][1] for k in range(4)]+[rotorrows[4*i+k][4] for k in range(4)]+[v[k] for k in [1,5,6,11,12,13,25,26,27]]))
  elif 'I' in data: ref=data['I']
  elif audits: ref=[tuple(x['row']) for x in audits]
  errors=None; differences={}
  if ref is not None:
   for method in ['B','M']:
    if method in data:
     maxima=full_comparison(data[method][:len(ref)],ref,accepted,sid+'-'+method);differences[method]=maxima
     if summary and 'fullDifferences' in summary: check(all(close(a,b,1e-30,5e-13) for a,b in zip(maxima,summary['fullDifferences'][method])),'all 17 saved full-comparison maxima',sid+'-'+method)
   if 'C' in data and decs:
    errors=approximation(data['C'],ref,decs,accepted,sid)
    if summary and 'errors' in summary: check(set(errors)==set(summary['errors']) and all(close(v,summary['errors'][k]) for k,v in errors.items()),'saved approximation maximum summaries',sid)
  ccall=call_by_key.get((sid,'C'))
  if ccall and ccall['ok']:
   check(len(decs)==n and all(ccall['counts'][k]==v for k,v in totals.items()),'actual completed C counters from all masks',sid)
   check(0<=ccall['counts']['profileEvaluations']<=ccall['counts']['rotorVisits'],'C profile-evaluation count range',sid)
   if summary:
    recorded=summary['counts'] if kind=='exposed' else summary.get('counts',{}).get('C')
    if recorded is not None: check(recorded==ccall['counts'],'summary/call C counters equality',sid)
  if kind!='exposed':
   statuses=[call_by_key.get((sid,m)) for m in ['B','M','C','I']]
   if all(statuses):
    decisions=[x['ok'] for x in statuses]
    scientific(len(set(decisions))==1,'Domain decisions differ',accepted,{'case':sid,'decisions':decisions})
    scientific(expected!='valid' or decisions[0],'Expected valid case rejected',accepted,{'case':sid})
    scientific(expected!='reject' or not decisions[0],'Expected rejection accepted',accepted,{'case':sid})
    if rejected: check(not any(decisions),'accepted rejection summary has four rejecting calls',sid)
    if all(decisions):
     bc,mc,ic=statuses[0]['counts'],statuses[1]['counts'],statuses[3]
     check(ic['centerChecks']==n*(n-1) and ic['rotorVisits']==bc['rotorVisits']==mc['rotorVisits']==4*bc['candidates'],'full-reference direct/eligible work counter identities',sid)
     check(bc['candidates']==mc['candidates'] and bc['profileEvaluations']==mc['profileEvaluations'],'B/M full support and candidate counters',sid)
     if summary and 'counts' in summary:
      sc=summary['counts'];check(sc['B']==bc and sc['M']==mc and sc['I']['centerChecks']==ic['centerChecks'] and sc['I']['rotorVisits']==ic['rotorVisits'] and sc['I']['candidates']==bc['candidates'] and sc['I']['contributions']==bc['profileEvaluations'],'all full-reference summary counters',sid)
  REPORT['cases'].append({'id':sid,'kind':kind,'expected':expected,'count':n,'acceptedSummary':accepted,'recordedDomainRejection':rejected,'outputRows':{m:len(v) for m,v in data.items()},'decisionRows':len(decs),'auditRows':len(audits),'decisionCounts':dict(totals),'recomputedErrors':errors,'fullComparisonMaxima':differences})
 # Reconstruct every attempted-call shape from the frozen order, including full charges for invalid returns.
 orders=cfg['timingOrders'];check(orders==[['B','M','C'],['M','C','B'],['C','B','M'],['B','C','M'],['C','M','B'],['M','B','C']],'frozen timing orders')
 planned=[(sid,m,n) for sid,n,_ in FIXTURES for m in ['B','M','C','I']]+[(sid,'C',n) for sid,n,_ in HISTORICAL]+[(sid,m,n) for sid,n,_ in FRESH for m in ['B','M','C','I']]
 planned += [(sid+'-timing-'+str(rep)+'-'+m,m,n) for sid,n,_ in FRESH for rep,order in enumerate(orders) for m in order]
 for i,call in enumerate(calls):
  must(i<len(planned),'recorded calls within frozen schedule')
  pid,pm,pn=planned[i]
  check(call['id']==pid and call['method']==pm and call.get('n',pn)==pn,'exact attempted call order/identity/size',i)
  if not call['ok']:
   domain_file=raw/(pid+'-'+pm+'-domain.json');check(domain_file.exists() and read(domain_file)==call,'domain call witness file equality',i)
 if result:
  counts=result['counts'];attempts=counts['fieldCalls'];must(0<=attempts<=len(planned),'attempted call count in fixed schedule')
  expected_counts={'fieldCalls':attempts,'independentCenterShape':0,'boundAttemptShape':0,'rotorVisitShape':0,'receiverCalls':0,'integrationSteps':0}
  for sid,method,n in planned[:attempts]:
   pair=n*(n-1);expected_counts['independentCenterShape']+=pair if method=='I' else 0;expected_counts['boundAttemptShape']+=pair if method=='C' else 0;expected_counts['rotorVisitShape']+=4*pair;expected_counts['receiverCalls']+=4*n
  check(counts==expected_counts,'all exact charged operation-shape counters')
  check(len(calls)<=attempts<=len(calls)+1,'at most one unreturned last attempted call')
  if attempts>len(calls):
   pending=planned[len(calls)];ctx=result.get('context',{});check((ctx.get('id'),ctx.get('method'),ctx.get('n'))==pending or result.get('error')=='Attempt shape cap','unreturned attempted call retained in failure context')
  if complete: check(attempts==len(calls)==152 and counts=={'fieldCalls':152,'independentCenterShape':25994070,'boundAttemptShape':289930070,'rotorVisitShape':2719361120,'receiverCalls':640832,'integrationSteps':0},'complete exact matrix shape totals')
  REPORT['operationAccounting']=expected_counts;REPORT['recordedRuntimeLogicalChecks']=result.get('checks')
 timings=ndjson(raw/'timings.ndjson',complete)
 if complete: check(timings==result['timings'] and len(timings)==36,'complete timing records and result equality')
 expected_timing=[(sid,rep,m) for sid,_,_ in FRESH for rep,order in enumerate(orders) for m in order]
 timing_groups={}
 for i,t in enumerate(timings):
  CURRENT={'phase':'saved-timing','index':i}
  must(i<len(expected_timing),'timing prefix within fixed schedule')
  sid,rep,m=expected_timing[i];check((t['id'],t['rep'],t['method'])==(sid,rep,m) and t['warmup']==(rep==0),'exact timing order and warmup designation')
  check(finite([t['wallSeconds'],t['checksum']]) and t['wallSeconds']>0,'finite positive saved timing/checksum')
  c=call_by_key.get((sid+'-timing-'+str(rep)+'-'+m,m));basecall=call_by_key.get((sid,m))
  if c: check(c['ok'] and c['wallSeconds']==t['wallSeconds'] and c['counts']==t['counts'],'timing/call ledger agreement')
  if basecall: check(basecall['counts']==t['counts'],'timed and correctness query work counters')
  checksum=0.0
  for row in all_rows[sid][m]:
   for value in row: checksum+=value
  check(close(t['checksum'],checksum),'timing checksum against retained correctness scalars')
  group=timing_groups.setdefault(sid,{}).setdefault(m,{'warmup':[],'measured':[]});group['warmup' if rep==0 else 'measured'].append(t['wallSeconds'])
 timing_summary={}
 for sid,methods in timing_groups.items():
  summary={}
  for m,g in methods.items():
   vals=sorted(g['measured']);summary[m]={'warmupSeconds':g['warmup'],'measuredSeconds':g['measured'],'measuredCount':len(vals),'minimum':vals[0] if vals else None,'maximum':vals[-1] if vals else None,'median':vals[len(vals)//2] if len(vals)==5 else None}
   if complete: check(len(g['warmup'])==1 and len(vals)==5,'one warmup and five measured samples',sid+'-'+m)
  if all(m in summary and summary[m]['median'] is not None for m in ['B','M','C']):
   summary['ratiosOfMedians']={'C_over_B':summary['C']['median']/summary['B']['median'],'C_over_M':summary['C']['median']/summary['M']['median']}
  summary['interpretation']='C bundles exact-zero culling, positive omissions, bound/guard/mask work and its implementation overhead; five technical repeats are not independent swarm samples.'
  timing_summary[sid]=summary
 REPORT['timingSummaries']=timing_summary
 CURRENT={'phase':'failure-witness-and-budget'}
 if failed:
  err=result['error'];detail=result.get('detail') or {};ctx=result.get('context') or {};w=ctx.get('witness')
  reproduced=None
  if err=='Full implementation mismatch':
   a,b=detail['actual'],detail['reference'];check(close(abs(a-b),detail['d']) and detail['actualRow'][detail['k']]==a and detail['referenceRow'][detail['k']]==b,'retained failure scalar and row consistency');reproduced=abs(a-b)>detail['t']
  elif err=='Timed checksum changed': reproduced=detail['actual']!=detail['expected']
  elif err in ['Per-source upper bound','Claimed exact-zero source has nonzero term']:
   reproduced=detail['term']>detail['B']+allowances['inflowAudit'] if err=='Per-source upper bound' else detail['term']!=0
  elif err in ['Domain decisions differ','Expected valid case rejected','Expected rejection accepted']:
   sid=detail.get('id');states=[call_by_key.get((sid,m),{}).get('ok') for m in ['B','M','C','I']]
   reproduced=len(set(states))>1 if err=='Domain decisions differ' else states[0] is False if err=='Expected valid case rejected' else states[0] is True
  elif err=='Cooperative time cap': reproduced=detail.get('elapsed',0)>=cfg['wallCapSeconds']-2
  elif err=='Raw evidence cap': reproduced=detail.get('bytes',0)+detail.get('nextBytes',0)>=cfg['rawByteCap']-cfg['failureReserveBytes'] if 'nextBytes' in detail else None
  else: reproduced=any(v['gate']==err for v in VIOLATIONS) or None
  if w:
   n=ctx['n'];terms_bytes=base64.b64decode(w['termsBase64'],validate=True);codes=base64.b64decode(w['codesBase64'],validate=True)
   check(len(terms_bytes)==4*n*8 and len(codes)==4*n,'full preserved current-receiver failure term/code vector lengths')
   terms=[v[0] for v in struct.iter_unpack('<d',terms_bytes)];check(finite(terms),'preserved failure terms finite')
   if 'j' in detail and 'k' in detail and 'term' in detail: check(terms[4*detail['j']+detail['k']]==detail['term'],'failure term matches complete saved witness')
  if reproduced is not None: check(reproduced,'recorded terminal failure reproduced from retained scalars/decisions')
  REPORT['failureAnalysis']={'recordedError':err,'detail':detail,'contextIdentity':{k:ctx.get(k) for k in ['id','method','n','receiver','stage']},'reproducedWithoutNewScience':reproduced,'note':'Null means insufficient retained scalar evidence for this failure class; no geometry or model evaluation was attempted.'}
 must(len(budget['entries'])==1,'one supervised scientific invocation')
 entry=budget['entries'][0];check(budget.get('active') is None,'no active supervised science process')
 check(entry['rawBytesAfter']==raw_bytes,'raw byte count matches supervisor')
 check(budget['wallCapSeconds']==300 and budget['rawByteCap']==134217728,'supervisor caps match freeze')
 check(entry['completeProcess']==(entry['exitCode']==0 and entry['stop'] is None),'supervisor completion semantics')
 if complete: check(entry['exitCode']==0 and entry['completeProcess'] and not budget['requiresFailureReview'],'completed scientific status matches supervisor')
 if failed: check(entry['exitCode']!=0 and budget['requiresFailureReview'],'failed scientific status matches supervisor')
 scientific(raw_bytes<cfg['rawByteCap'],'raw storage cap',complete)
 scientific(0<entry['wallSeconds']<cfg['wallCapSeconds'],'executable wall cap',complete)
 if result: check(finite([result['elapsedSeconds']]) and 0<=result['elapsedSeconds']<=entry['wallSeconds'],'driver/supervisor elapsed accounting')
 if complete: check(raw_bytes<cfg['rawByteCap']-cfg['failureReserveBytes'],'success preserves full failure reserve')
 REPORT['retainedCoverage']=dict(diagnostic)
 REPORT['budgetAndInventory']={'rawFiles':len(raw_inventory),'rawBytes':raw_bytes,'supervisor':entry,'terminalFlagAtReview':budget['terminal'],'completedCaseSummaries':len(saved_summaries),'recordedCalls':len(calls),'timingsRetained':len(timings)}
 REPORT['scientificQualificationCompleted']=complete
 REPORT['outcome']='Complete campaign retained evidence verified' if complete else 'Terminal incomplete/failed campaign retained evidence reviewed; no qualification claim'

exit_code=0
with (RUN/'stdout.txt').open('w') as stdout,(RUN/'stderr.txt').open('w') as stderr:
 with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
  signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,55)
  try:
   if len(sys.argv)!=3 or sys.argv[2]!='--authorized-after-science': raise ValueError('Requires explicit prior authorization: python3 m31-omission-saved-review.py REPOSITORY --authorized-after-science')
   verify(Path(sys.argv[1]).resolve())
  except BaseException as exc:
   exit_code=1;REPORT['exception']={'type':type(exc).__name__,'message':str(exc),'context':CURRENT};traceback.print_exc()
  finally: signal.setitimer(signal.ITIMER_REAL,0)
  REPORT.update({'checkCount':sum(CHECKS.values()),'checkCategories':dict(CHECKS),'failedCheckCount':FAILED,'failedChecks':FAILURES,'observedScientificGateViolations':VIOLATIONS,'passed':exit_code==0 and FAILED==0,'verificationWallSecondsBeforeOutput':time.perf_counter()-START})
  if not REPORT['passed']: exit_code=1
  canonical=Path('/tmp/m31-omission-saved-review.json');REPORT['canonicalAlreadyExisted']=canonical.exists()
  serialized=json.dumps(REPORT,indent=2,allow_nan=False)+'\n';(RUN/'review.json').write_text(serialized)
  try:
   with canonical.open('x') as handle: handle.write(serialized)
  except FileExistsError: pass
  print(json.dumps({k:REPORT.get(k) for k in ['passed','scientificStatus','scientificQualificationCompleted','checkCount','failedCheckCount','failedChecks','exception','retainedCoverage','budgetAndInventory','timingSummaries','failureAnalysis']},indent=2))
runtime={'wallSecondsThroughReviewAndLogs':time.perf_counter()-START,'internalAlarmSeconds':55,'authorizedWallSeconds':60,'exitCode':exit_code,'passed':REPORT['passed'],'checkCount':REPORT['checkCount'],'checkerSha256':sha(SCRIPT),'invocationArchive':str(RUN)}
(RUN/'runtime.json').write_text(json.dumps(runtime,indent=2)+'\n')
print((RUN/'stdout.txt').read_text(),end='')
if (RUN/'stderr.txt').stat().st_size: print((RUN/'stderr.txt').read_text(),end='',file=sys.stderr)
print(json.dumps({'runtime':runtime}))
raise SystemExit(exit_code)
