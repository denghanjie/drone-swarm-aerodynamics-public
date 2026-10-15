"""UNEXECUTED saved-only reviewer for the one M31 zero-screen campaign.
Run once after coordinator authorization under an external <=59-second guard:
python3 m31-zero-screen-saved-review.py REPOSITORY --source-commit SHA --freeze-sha256 SHA256 --authorized-after-science
SHA values must be supplied from independent publication verification, never read from started/result/freeze metadata.
No scientific module import, generation, geometry, field, root solving, integration or timing repeat.
"""
import base64, contextlib, hashlib, json, math, re, signal, struct, sys, time, traceback, zlib
from collections import Counter
from pathlib import Path
SOURCE=None
FREEZE=None
CAMPAIGN='research/m31-zero-screen-2026-10-16'
REFERENCE='research/m31-omission-ablation-2026-10-16'
ORIGIN='research/m31-source-omission-2026-10-16'
ARITH_ABS=2e-16
ARITH_REL=8e-15
START=time.perf_counter()
RUN=Path('/tmp/m31-zero-screen-verifier-runs')/str(time.time_ns())
RUN.mkdir(parents=True,exist_ok=False)
SCRIPT=Path(__file__).read_bytes()
(RUN/'checker.py').write_bytes(SCRIPT)
CHECKS=Counter(); FAILURES=[]; VIOLATIONS=[]; FAILED=0; CURRENT={'phase':'startup'}
REPORT={'scope':'Saved evidence only; no scientific modules, geometry, quaternion rotation/norm, field evaluation, root solving, generation, integration or timing repeat.',
 'method':{'checkerSha256':hashlib.sha256(SCRIPT).hexdigest(),'invocationArchive':str(RUN),'sourceCommit':SOURCE,'authorizedWallSeconds':60,'internalAlarmSeconds':55,
 'checkerArithmeticTolerance':{'absolute':ARITH_ABS,'relative':ARITH_REL,'residualReconstructionAbsolute':4e-15,'summaryRelative':5e-13,'smallDiscrepancyAbsolute':1e-30},
 'pinAuthority':'Required command-line source/freeze values supplied by coordinator from independent publication verification; never inferred from scientific self-reports.',
 'toleranceSeparation':'Checker tolerances apply only to scalar reconstructions/summaries. Frozen scientific tolerances and bitwise gates are not enlarged.'},
 'sourceHashes':[],'rawHashes':[],'cases':[],'partialTails':[],
 'limitations':[
 'Passing review of a failed campaign means retained evidence consistency, not successful scientific qualification.',
 'Poses are decoded only for finite layout and prescribed placeholders/motors; no norm/rotation/geometry or generator replay.',
 'Complete oracle codes and claimed-zero code7 scalar exceptions are verified as recorded same-pass evidence, not independently regenerated physics.',
 'Codes1,2,4,5 are zero-return classes; code6 is projection-zero evaluation; code0/3 cannot certify an eligible zero; code7 requires its matching numerical-zero scalar exception.',
 'E/L category identities are retained; Z has fallback counts but no fallback source identities or unselected positive bounds.',
 'Center radial norm counts derive from recorded downstream-branch counts and static schedule, not hardware counters.',
 'Production profile counts are aggregate counters; their E/L/Z equality, ranges, and Z shadow/selected conservation are checked. Independent code-derived profile totals are reported separately, not imposed as a new geometry gate.',
 'Body wrench and scalar root/power identities are reconstructed. World rotations are not recomputed.',
 'Successful timed matrices/masks are not duplicated; checksums/counts and saved validation assertions can be reconciled, not every repeated component.',
 'E/Z removes the whole positive-policy/reporting package; L/E tests scheduling with matched instrumentation. Neither is isolated hardware latency or superiority to DOT lean.',
 'Eight paired technical blocks on two same-family inputs do not establish population inference, physical/flight correctness, f32 qualification, or novelty.']}
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
FRESH=[('fresh1000',1000,'valid'),('fresh5000',5000,'valid')]
CASE_TABLE=FIXTURES+FRESH
CASE_INFO={sid:{'n':n,'expected':expected,'kind':'fixture' if i<24 else 'fresh'} for i,(sid,n,expected) in enumerate(CASE_TABLE)}



def equivalent(a,b):
 if isinstance(a,bool) or isinstance(b,bool): return type(a)==type(b) and a==b
 if isinstance(a,(int,float)) and isinstance(b,(int,float)): return close(a,b)
 if isinstance(a,dict) and isinstance(b,dict): return set(a)==set(b) and all(equivalent(a[k],b[k]) for k in a)
 if isinstance(a,list) and isinstance(b,list): return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
 return type(a)==type(b) and a==b

def median8(values):
 a=sorted(values);must(len(a)==8,'exact eight-sample median');return (a[3]+a[4])/2

def intersection(a,b):
 return (int.from_bytes(a,'little') & int.from_bytes(b,'little')).to_bytes(len(a),'little')

ELIGIBLE=bytes(0 if i==0 else 1 for i in range(256))
ZERO=bytes(1 if i==1 else 0 for i in range(256))
SEVEN=bytes(1 if i==7 else 0 for i in range(256))
RETAINED=bytes(1 if i in [2,3] else 0 for i in range(256))
PROFILE=bytes(1 if i in [6,7] else 0 for i in range(256))
ACTUAL_MAP=bytes(2 if i==3 else i for i in range(256))

def verify(repo):
 global CURRENT
 base=repo/CAMPAIGN;raw=base/'raw';cfg=read(base/'config.json');schema=read(base/'schema.json')
 freeze_bytes=(base/'freeze.json').read_bytes();freeze=json.loads(freeze_bytes)
 must(sha(freeze_bytes)==FREEZE,'externally pinned freeze bytes')
 must(isinstance(freeze.get('files'),list) and len({x['path'] for x in freeze['files']})==len(freeze['files']),'unique-file freeze')
 required={CAMPAIGN+'/'+p for p in ['PROTOCOL.md','config.json','schema.json','source/experiment.cjs','source/control.cjs','source/run-step.py','EXISTING-WORK-AUDIT.md','PRIOR-WORK-COMPARISON.md','PREFLIGHT-RESOLUTIONS.md']}|{ORIGIN+'/source/'+p for p in ['candidate.cjs','independent.cjs','cases.cjs']}|{REFERENCE+'/source/zero-control.cjs',REFERENCE+'/manifest.json','outputs/step02c-source/physics.cjs','outputs/milestone-28-source/aero.cjs','outputs/step03a-source/wake.cjs','outputs/milestone-26-source/grid.cjs'}
 check(required<={x['path'] for x in freeze['files']},'required source/protocol/history/dependency pins')
 REPORT['method'].update({'sourceCommit':SOURCE,'freezeSha256':FREEZE,'freezeFileCount':len(freeze['files'])})
 for item in freeze['files']:
  CURRENT={'phase':'frozen-file','path':item['path']};relative=Path(item['path'])
  must(not relative.is_absolute() and '..' not in relative.parts,'contained frozen source path')
  b=(repo/relative).read_bytes();matched=len(b)==item['bytes'] and sha(b)==item['sha256']
  check(matched,'frozen file hash/size',item['path']);REPORT['sourceHashes'].append({'path':item['path'],'bytes':len(b),'sha256':sha(b),'matches':matched})
 CURRENT={'phase':'outcome-and-inventory'}
 budget=read(base/'results/budget.json');sp=raw/'started.json';started=read(sp) if sp.exists() and sp.stat().st_size else None
 rp=base/'results/result.json';result=read(rp) if rp.exists() else None
 complete=result is not None and result.get('status')=='completed';failed=result is not None and result.get('status')=='failed'
 REPORT['scientificStatus']=result.get('status') if result else 'no terminal driver result; interrupted/preflight failure'
 for p,label in [(base/'results/budget.json','scientific-budget-original.json'),(sp,'scientific-started-original.json'),(rp,'scientific-result-original.json')]:
  if p.exists(): (RUN/label).write_bytes(p.read_bytes())
 if started is not None: must(started['sourceCommit']==SOURCE and started['cfg']==cfg and started['schema']==schema,'external source and frozen started provenance/config/schema')
 if complete:
  must(started is not None,'completed run has started provenance')
  check(result['sourceCommit']==SOURCE and result['config']==cfg and result['schema']==schema,'completed result provenance/config/schema')
  check(result==read(raw/'result.json'),'raw/published successful result equality')
 if failed: check(result==read(raw/'failure.json'),'raw/published failed result equality')
 check(schema['rowType']=='Float64LE' and schema['poseType']=='Float64LE' and schema['rowColumns']==['U0','U1','U2','U3','f0','f1','f2','f3','bodyThrust','roll','pitch','worldFx','worldFy','worldFz','worldMx','worldMy','worldMz'] and schema['poseColumns']==['x','y','z','vx','vy','vz','qx','qy','qz','qw','wx','wy','wz','motor0','motor1','motor2','motor3'],'exact 17-column schemas')
 check(cfg['fixtureCases']==24 and cfg['historicalCases']==0 and cfg['freshCases']==[{'id':'fresh1000','shape':[10,10,10],'seed':253741},{'id':'fresh5000','shape':[20,25,10],'seed':608897}],'frozen cases/seeds/shapes without generation')
 check(cfg['referenceCommit']=='f5dd23e20b4e64eda647f30870c4a8e0a717e99e' and cfg['referenceDirectory']==REFERENCE and cfg['referenceManifestSha256']=='f2eef0eac63d10ab80bd0984bdebe644410bed25eaa6617c6937615f252838ae' and sha((repo/REFERENCE/'manifest.json').read_bytes())==cfg['referenceManifestSha256'],'closed parent reference manifest pin')
 limits={'wallCapSeconds':300,'rawByteCap':134217728,'failureReserveBytes':4194304,'fieldCallCap':202,'independentCenterCap':26000000,'screenAttemptShapeCap':780000000,'rotorVisitShapeCap':4300000000,'receiverCallCap':1000000,'verificationWallCapSeconds':60}
 check(all(cfg[k]==v for k,v in limits.items()),'unchanged resource caps')
 exact_charges={'fieldCalls':202,'independentCenterShape':25994070,'screenAttemptShape':779820210,'rotorVisitShape':4263017400,'receiverCalls':985040,'integrationSteps':0}
 check(cfg['expectedCharges']==exact_charges,'prospective exact charge vector')
 criteria={r:{'maximumMedianPairedRatio':.95,'minimumFasterBlocks':7,'measuredBlocks':8,'requireBothFreshCases':True} for r in ['E_over_Z','L_over_E']}
 check(cfg['performanceCriteria']==criteria,'prospective separate E/Z and L/E cost definitions')
 check(cfg['stopNewLaunchUTC']=='2026-10-15T23:00:00Z','fixed new-launch deadline')
 tolerances={'inflowAbsTolerance':1e-11,'inflowRelTolerance':1e-12,'rotorTolerance':1e-12,'bodyThrustTolerance':5e-12,'bodyMomentTolerance':2e-13,'worldForceTolerance':1e-11,'worldMomentTolerance':1e-12,'rootResidualTolerance':1e-12,'bracketWidthTolerance':2e-15,'powerAbsoluteTolerance':1e-14,'powerRelativeTolerance':1e-12}
 check(all(cfg[k]==v for k,v in tolerances.items()),'unchanged full-reference numerical gates')
 raw_inventory={}
 for p in sorted(raw.iterdir()):
  must(p.is_file(),'flat raw inventory',p.name);b=p.read_bytes();raw_inventory[p.name]={'name':p.name,'bytes':len(b),'sha256':sha(b)}
 REPORT['rawHashes']=list(raw_inventory.values());raw_bytes=sum(x['bytes'] for x in raw_inventory.values())
 listed=[] if result is None else result.get('files',[])
 must(len({x['name'] for x in listed})==len(listed),'unique listed evidence names')
 for item in listed: check(raw_inventory.get(item['name'])==item,'retained file inventory hash/size',item['name'])
 if complete: check(set(raw_inventory)=={x['name'] for x in listed}|{'result.json'},'complete successful raw inventory')
 REPORT['unlistedRawFiles']=[v for k,v in raw_inventory.items() if k not in {x['name'] for x in listed}]
 must(len(budget['entries'])==1 and budget.get('active') is None and budget.get('terminal') is True,'one completed terminal supervised science attempt')
 entry=budget['entries'][0];check(entry['rawBytesAfter']==raw_bytes,'supervisor raw byte inventory equality')
 check(budget['wallCapSeconds']==300 and budget['rawByteCap']==134217728,'supervisor cap identity')
 check(entry['completeProcess']==(entry.get('exitCode')==0 and entry.get('stop') is None),'supervisor completion semantics')
 if started is None:
  must(not complete,'preflight failure has no successful qualification')
  REPORT.update({'scientificQualificationCompleted':False,'outcome':'Terminal preflight/incomplete evidence; no qualification','budgetAndInventory':{'rawFiles':len(raw_inventory),'rawBytes':raw_bytes,'supervisor':entry},'failureAnalysis':{'recordedError':result.get('error') if result else None,'evidenceIncomplete':True}});return
 summaries={}
 for p in raw.glob('*-summary.json'):
  s=read(p);must(s['id'] in CASE_INFO,'recognized case summary',p.name);summaries[s['id']]=s
 saved_summaries=[summaries[sid] for sid,_,_ in CASE_TABLE if sid in summaries] if result is None or not any(k in result for k in ['results','completedResults']) else result.get('results',result.get('completedResults',[]))
 for s in saved_summaries: check(summaries.get(s['id'])==s,'terminal/raw case summary equality',s['id'])
 check([s['id'] for s in saved_summaries]==[x[0] for x in CASE_TABLE[:len(saved_summaries)]],'complete summaries form ordered case prefix')
 if complete: check(result.get('pass') is True and len(summaries)==len(saved_summaries)==26 and all(s.get('pass') is True for s in saved_summaries),'all26passing completed case summaries and terminal pass')
 has_call_ledger=result is not None and isinstance(result.get('calls'),list);calls=result['calls'] if has_call_ledger else []
 call_by_key={(c['id'],c['method']):c for c in calls};check(len(call_by_key)==len(calls),'unique retained call identities')
 all_rows={};diagnostic=Counter()
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

 for sid,n,expected in CASE_TABLE:
  summary=summaries.get(sid);accepted=summary is not None and summary.get('pass') is True;rejected=bool(summary and summary.get('domain')=='all reject');kind=CASE_INFO[sid]['kind']
  if not (summary is not None or any(name.startswith(sid+'-') for name in raw_inventory)): continue
  CURRENT={'phase':'case-coverage','case':sid}
  if summary: check(summary['n']==n and summary['kind']==kind and summary.get('expected')==expected,'case identity/size/kind/expectation')
  state_rows=rows(raw/(sid+'-states.f64'),n,accepted)
  if state_rows is not None:
   for i,s in enumerate(state_rows): check(finite(s) and list(s[3:6])==[0,0,0] and list(s[10:13])==[0,0,0] and all(v==F0 for v in s[13:17]),'saved state finite layout and prescribed placeholders',{'case':sid,'receiver':i})
   diagnostic['savedStateRows']+=len(state_rows)
  data={}
  for method in ['M','Z','E','L','I']:
   rs=rows(raw/(sid+'-'+method+'.f64'),n,accepted and not rejected)
   if rs is not None: data[method]=rs;row_checks(rs,method,accepted,sid);diagnostic['outputRows']+=len(rs)
  if accepted and not rejected: check(set(data)=={'M','Z','E','L','I'},'complete accepted five-method output matrices',sid)
  all_rows[sid]=data;decisions={};masks={};totals={}
  for method in ['Z','E','L']:
   decs=ndjson(raw/(sid+'-'+method+'-decisions.ndjson'),complete);decisions[method]=decs;masks[method]=[];totals[method]=Counter()
   check(len(decs)<=n,'decision prefix within N',sid+'-'+method)
   if accepted and not rejected: check(len(decs)==n,'complete accepted decision stream',sid+'-'+method)
   for i,d in enumerate(decs):
    CURRENT={'phase':'saved-decision','case':sid,'method':method,'receiver':i}
    must(d['receiver']==i,'ordered decision receiver identities')
    packed=inflate(d['maskDeflateBase64'],(n+3)//4);check(sha(packed)==d['maskSha256'],'complete decision mask hash')
    expanded=b''.join(EXPAND[x] for x in packed);check(expanded[n:]==b'\0'*(len(expanded)-n),'zero mask padding');expanded=expanded[:n]
    check(expanded[i]==0,'self category zero');hc=[expanded.count(bytes([k])) for k in range(4)];masks[method].append(expanded)
    must(finite([d[k] for k in ['candidates','zeroCulls','retained','nearFallbacks']]),'finite decision counters')
    if method=='Z':
     check(d['semantics']=='shadow-C' and d['candidates']==n-hc[0] and d['zeroCulls']==hc[1] and d['retained']==hc[2] and 0<=d['nearFallbacks']<=hc[2] and d['actualRetained']==hc[2]+hc[3] and d['actualPositiveOmissions']==0,'Z shadow/actual mask accounting')
     ids=[];pos=expanded.find(b'\3')
     while pos>=0: ids.append(pos);pos=expanded.find(b'\3',pos+1)
     check([x[0] for x in d['omitted']]==ids,'Z ascending exhaustive shadow selection identities')
     B=0.0
     for pair in d['omitted']:
      must(len(pair)==2 and finite(pair) and pair[1]>0,'finite positive shadow bound');B=nextup(B+pair[1])
     check(d['B']==B and math.isfinite(B) and B>=0,'Z exact recorded nextUp shadow accumulation')
     totals[method].update({'candidates':n-hc[0],'boundAttempts':n-hc[0],'zeroCulls':hc[1],'positiveOmissions':hc[3],'retained':hc[2],'nearFallbacks':d['nearFallbacks'],'rotorVisits':4*hc[2]})
    else:
     check(d['semantics']=='source-screen-category-v1','E/L category schema')
     check(d['candidates']==d['screenCalls']==n-hc[0] and d['zeroCulls']==hc[1] and d['nearFallbacks']==hc[2] and d['remainingRetained']==hc[3] and d['retained']==hc[2]+hc[3],'E/L full mask-derived category counters')
     check(d['actualPositiveOmissions']==d['actualOmittedInflowBound']==0 and isinstance(d['downstreamZeroExits'],int) and 0<=d['downstreamZeroExits']<=hc[1],'E/L zero omission and downstream branch range')
     check(d['centerRadialHypotCalls']==n-hc[0]-(d['downstreamZeroExits'] if method=='L' else 0),'derived per-receiver radial norm schedule')
     totals[method].update({k:d[k] for k in ['candidates','screenCalls','zeroCulls','retained','nearFallbacks','remainingRetained','downstreamZeroExits','centerRadialHypotCalls','actualPositiveOmissions']})
     totals[method].update({'positiveOmissions':0,'rotorVisits':4*(hc[2]+hc[3])})
   diagnostic[method+'decisionRows']+=len(decs)
  for i in range(min(len(masks['Z']),len(masks['E']),len(masks['L']))):
   CURRENT={'phase':'cross-method-decisions','case':sid,'receiver':i};e,l,z=[masks[m][i] for m in ['E','L','Z']];ed,ld,zd=[decisions[m][i] for m in ['E','L','Z']]
   scientific(e==l,'E/L category identity',accepted)
   scientific(e.translate(ACTUAL_MAP)==z.translate(ACTUAL_MAP),'Z mapped actual category identity',accepted)
   pos=z.find(b'\3');shadow_ok=True
   while pos>=0:
    if e[pos]!=3: shadow_ok=False
    pos=z.find(b'\3',pos+1)
   scientific(shadow_ok,'Z shadow selection is E/L remaining retained',accepted)
   keys=['receiver','candidates','screenCalls','zeroCulls','retained','nearFallbacks','remainingRetained','downstreamZeroExits','actualPositiveOmissions','actualOmittedInflowBound']
   scientific(all(ed[k]==ld[k] for k in keys),'E/L shared scalar identity',accepted)
   scientific(ed['candidates']==zd['candidates'] and ed['zeroCulls']==zd['zeroCulls'] and ed['retained']==zd['actualRetained'] and ed['nearFallbacks']==zd['nearFallbacks'],'Z actual mapped counts',accepted)
  audits=ndjson(raw/(sid+'-source-audit.ndjson'),complete);check(len(audits)<=n,'oracle prefix within N',sid)
  if accepted and not rejected: check(len(audits)==n,'complete independent audit coverage',sid)
  oracle_totals=Counter();oracle_profile_by_method=Counter()
  for i,audit in enumerate(audits):
   CURRENT={'phase':'complete-oracle-code-audit','case':sid,'receiver':i}
   must(audit['receiver']==i and audit['codesLength']==4*n,'ordered oracle receiver and declared4Nlength')
   codes=inflate(audit['codesDeflateBase64'],4*n);check(sha(codes)==audit['codesSha256'],'complete oracle code SHA256')
   hist=[codes.count(bytes([k])) for k in range(8)]
   must(sum(hist)==4*n and hist[3]==0,'oracle codes0through7 with no completed-domain rejection code')
   check(audit['codeCounts']==hist,'complete oracle classification histogram')
   eligible=(4*n-hist[0])//4
   check((4*n-hist[0])%4==0 and audit['eligible']==eligible and audit['contributions']==hist[6]+hist[7],'oracle eligibility and profile contribution conservation')
   oracle_totals.update({'candidates':eligible,'rotorVisits':4*eligible,'contributions':hist[6]+hist[7]})
   check(codes[4*i:4*i+4]==b'\0'*4,'four self oracle codes zero')
   rotor_codes=[codes[k::4] for k in range(4)]
   eligible_bytes=rotor_codes[0].translate(ELIGIBLE)
   check(all(c.translate(ELIGIBLE)==eligible_bytes for c in rotor_codes),'four-rotor eligible/outside identity')
   expected_exceptions=[];shared=None
   if i<len(masks['E']) and call_by_key.get((sid,'E'),{}).get('ok') is True:
    shared=masks['E'][i];check(shared.translate(ELIGIBLE)==eligible_bytes,'complete screen/oracle source eligibility identity')
    zeros=shared.translate(ZERO)
    for k,rc in enumerate(rotor_codes):
     zero7=intersection(zeros,rc.translate(SEVEN));pos=zero7.find(b'\1')
     while pos>=0: expected_exceptions.append((pos,k));pos=zero7.find(b'\1',pos+1)
    expected_exceptions.sort()
    check(audit['zeroInspections']==4*shared.count(b'\1'),'all shared zero rotor slots inspected exactly once')
   else:
    check(audit['zeroInspections']==0,'no unavailable screen zero checks claimed')
   exceptions=audit['zeroCode7Exceptions'];must(isinstance(exceptions,list),'zero code7 exception array')
   valid_exceptions=all(isinstance(x,list) and len(x)==3 and isinstance(x[0],int) and not isinstance(x[0],bool) and isinstance(x[1],int) and not isinstance(x[1],bool) and 0<=x[0]<n and 0<=x[1]<4 and finite([x[2]]) and x[2]==0 for x in exceptions)
   must(valid_exceptions,'finite numerical-zero exception shape/source/rotor bounds')
   actual_ids=[(x[0],x[1]) for x in exceptions]
   check(actual_ids==expected_exceptions and len(set(actual_ids))==len(actual_ids) and audit['zeroCode7Count']==len(exceptions),'ordered unique exhaustive claimed-zero code7 exceptions')
   # Eligibility equality and no code3 imply all non7 claimed-zero codes belong exactly to1,2,4,5,6.
   for method in ['Z','E','L']:
    if i<len(masks[method]):
     keep=masks[method][i].translate(RETAINED)
     oracle_profile_by_method[method]+=sum(intersection(keep,rc.translate(PROFILE)).count(b'\1') for rc in rotor_codes)
   must(isinstance(audit['row'],list) and len(audit['row'])==17 and finite(audit['row']),'finite complete independent audit row')
   if 'I' in data and i<len(data['I']): check(tuple(audit['row'])==data['I'][i],'oracle JSON row equals retained binary scalars')
   must(len(audit['solutions'])==4,'four retained independent root diagnostics')
   for k,sol in enumerate(audit['solutions']):
    vals=[sol['thrust'],sol['x'],sol['alpha'],sol['residual'],*sol['bracket'],sol['iterations']];must(finite(vals),'finite saved independent solution')
    lo,hi=sol['bracket'];x=sol['x'];alpha=sol['alpha'];iters=sol['iterations']
    scientific(0<=lo<=x<=hi<=1 and hi-lo<=cfg['bracketWidthTolerance'] and isinstance(iters,int) and 0<=iters<=96 and abs(sol['residual'])<=cfg['rootResidualTolerance'],'Independent root bracket/residual',accepted)
    check(close(sol['thrust'],audit['row'][4+k]) and close(sol['thrust'],F0*x) and close(alpha,audit['row'][k]/V0) and close(sol['residual'],x*x*x+alpha*x-1,4e-15),'independent saved root scalar identities')
   diagnostic['auditRows']+=1;diagnostic['retainedOracleCodeBytes']+=len(codes);diagnostic['zeroCode7Exceptions']+=len(exceptions);diagnostic['recordedZeroTermChecks']+=audit['zeroInspections']
  if 'I' not in data and audits: row_checks([a['row'] for a in audits],'I',accepted,sid)
  ref=data.get('I') or [tuple(a['row']) for a in audits];differences={};bitwise={}
  if ref:
   for method in ['M','Z','E','L']:
    if method in data:
     maxima=full_comparison(data[method][:len(ref)],ref,accepted,sid+'-'+method);differences[method]=maxima
     if summary and 'fullDifferences' in summary: check(len(summary['fullDifferences'][method])==17 and all(close(a,b,1e-30,5e-13) for a,b in zip(maxima,summary['fullDifferences'][method])),'all17 saved full-comparison maxima',sid+'-'+method)
  for method in ['E','L']:
   if method in data and 'Z' in data:
    unequal=sum(struct.pack('<d',a)!=struct.pack('<d',b) for ar,br in zip(data[method],data['Z']) for a,b in zip(ar,br))
    bitwise[method+'_vs_Z']={'differingComponents':unequal,'totalComparedComponents':17*min(len(data[method]),len(data['Z']))}
    scientific(len(data[method])==len(data['Z']) and unequal==0,'bitwise'+method+'/Z complete saved output equality',accepted)
  for method in ['M','Z','E','L']:
   call=call_by_key.get((sid,method))
   if call and call.get('ok'):
    c=call['counts'];check(all(isinstance(v,int) and not isinstance(v,bool) and v>=0 for v in c.values()),'nonnegative integer actual work counters',sid+'-'+method)
    check(c['positiveOmissions']==0 and c['rotorVisits']==4*c['retained'] and 0<=c['profileEvaluations']<=c['rotorVisits'],'actual work conservation',sid+'-'+method)
    if method in ['E','L']:
     check(len(decisions[method])==n and all(c.get(k)==v for k,v in totals[method].items()),'complete E/L counters reconstructed from receiver records/masks',sid+'-'+method)
     check(c['actualPositiveOmissions']==0,'zero actual positive omission count')
    elif method=='Z':
     zs=call['shadowCounts'];extra=call['selectedSourceWork'];check(len(decisions['Z'])==n and all(zs.get(k)==v for k,v in totals['Z'].items()),'complete Z shadow counters reconstructed from masks',sid)
     check(c['actualPositiveOmissions']==0 and c['retained']==zs['retained']+zs['positiveOmissions'] and extra['rotorVisits']==4*zs['positiveOmissions'] and c['rotorVisits']==zs['rotorVisits']+extra['rotorVisits'],'Z actual/shadow/selected work conservation')
     check(c['profileEvaluations']==zs['profileEvaluations']+extra['profileEvaluations'] and 0<=zs['profileEvaluations']<=zs['rotorVisits'] and 0<=extra['profileEvaluations']<=extra['rotorVisits'],'Z profile work conservation/ranges')
     check(all(c[k]==zs[k] for k in ['candidates','boundAttempts','zeroCulls','nearFallbacks']),'Z shared actual/shadow counters')
    else:
     check(c['boundAttempts']==c['zeroCulls']==c['nearFallbacks']==0 and c['retained']==c['candidates'],'M complete no-screen work')
    if method in data:
     checksum=0.0
     for row in data[method]:
      for value in row: checksum+=value
     check(close(checksum,call['checksum']),'correctness checksum from saved full matrix',sid+'-'+method)
    if summary and not rejected: check(summary['counts'][method]==c,'summary/call actual work equality',sid+'-'+method)
  available={m:call_by_key.get((sid,m)) for m in ['M','Z','E','L','I']}
  if all(available.values()):
   statuses=[available[m]['ok'] for m in ['M','Z','E','L','I']]
   scientific(len(set(statuses))==1,'Domain decisions differ',accepted,{'case':sid,'decisions':statuses})
   scientific(expected!='valid' or statuses[0],'Expected valid case rejected',accepted,{'case':sid})
   scientific(expected!='reject' or not statuses[0],'Expected rejection accepted',accepted,{'case':sid})
   if rejected: check(not any(statuses),'accepted rejection has five rejecting calls',sid)
   if all(statuses):
    counts={m:available[m]['counts'] for m in ['M','Z','E','L']};ic=available['I']
    check(ic['centerChecks']==n*(n-1) and ic['rotorVisits']==oracle_totals['rotorVisits'] and all(c['candidates']==oracle_totals['candidates'] for c in counts.values()),'independent direct/eligible recorded work identity')
    check(all(counts['E'][k]==counts['L'][k] for k in counts['E'] if k!='centerRadialHypotCalls') and counts['E']['centerRadialHypotCalls']-counts['L']['centerRadialHypotCalls']==counts['E']['downstreamZeroExits'],'E/L shared aggregate identity and derived radial norm saving')
    check(all(counts[m][k]==counts['Z'][k] for m in ['E','L'] for k in ['candidates','zeroCulls','retained','nearFallbacks','rotorVisits','profileEvaluations']),'E/L/Z actual aggregate equality')
    if summary and not rejected:
     sc=summary['counts']['I'];check(sc=={'centerChecks':n*(n-1),'rotorVisits':oracle_totals['rotorVisits'],'contributions':oracle_totals['contributions'],'candidates':oracle_totals['candidates']},'independent complete counts from full code streams')
     eq=summary['equivalence'];check(eq['categoryIdentity'] is True and eq['ZmappedActualIdentity'] is True and eq['bitwiseEandLvsZ'] is True and eq['actualPositiveOmissions']==0,'summary narrowed equivalence assertions')
  REPORT['cases'].append({'id':sid,'kind':kind,'expected':expected,'count':n,'acceptedSummary':accepted,'recordedDomainRejection':rejected,'outputRows':{m:len(v) for m,v in data.items()},'decisionRows':{m:len(v) for m,v in decisions.items()},'auditRows':len(audits),'maskDerivedCounts':{m:dict(v) for m,v in totals.items()},'oracleCounts':dict(oracle_totals),'oracleCodeDerivedRetainedProfiles':dict(oracle_profile_by_method),'bitwiseComparisons':bitwise,'fullComparisonMaxima':differences})

 # Full-shape charges are reconstructed from the frozen order, including expected rejection attempts.
 orders=cfg['timingOrders'];check(orders==[['M','Z','L','E']]+[['M','Z','L','E'],['Z','E','M','L'],['E','L','Z','M'],['L','M','E','Z']]*2,'fixed balanced warmup/measured timing order')
 planned=[(sid,m,n) for sid,n,_ in CASE_TABLE for m in ['M','Z','E','L','I']]
 planned += [(sid+'-timing-'+str(rep)+'-'+m,m,n) for sid,n,_ in FRESH for rep,order in enumerate(orders) for m in order]
 for i,call in enumerate(calls):
  must(i<len(planned),'recorded calls within frozen schedule');pid,pm,pn=planned[i]
  check(call['id']==pid and call['method']==pm and call.get('n',pn)==pn,'exact attempted call identity/order/size',i)
  if not call['ok']:
   p=raw/(pid+'-'+pm+'-domain.json');check(p.exists() and read(p)==call,'rejected call retained domain witness',i)
 if result:
  counts=result['counts'];attempts=counts['fieldCalls'];must(isinstance(attempts,int) and 0<=attempts<=len(planned),'attempt count within schedule')
  expected_counts={'fieldCalls':attempts,'independentCenterShape':0,'screenAttemptShape':0,'rotorVisitShape':0,'receiverCalls':0,'integrationSteps':0}
  for sid,method,n in planned[:attempts]:
   pair=n*(n-1);expected_counts['independentCenterShape']+=pair if method=='I' else 0;expected_counts['screenAttemptShape']+=pair if method in ['Z','E','L'] else 0;expected_counts['rotorVisitShape']+=4*pair;expected_counts['receiverCalls']+=4*n
  check(counts==expected_counts,'all exact charged shape counters')
  if has_call_ledger:
   check(len(calls)<=attempts<=len(calls)+1,'at most one unreturned attempted call')
   if attempts>len(calls):
    ctx=result.get('context',{});check((ctx.get('id'),ctx.get('method'),ctx.get('n'))==planned[len(calls)],'unreturned attempt identified by current failure context')
  if complete: check(attempts==len(calls)==202 and counts==exact_charges,'complete202call exact accounting')
  REPORT['operationAccounting']=expected_counts;REPORT['recordedRuntimeLogicalChecks']=result.get('checks')
 timings=ndjson(raw/'timings.ndjson',complete);validations=ndjson(raw/'timing-validations.ndjson',complete)
 if complete: check(timings==result['timings'] and len(timings)==len(validations)==72,'complete timing/validation/result equality')
 expected_timing=[(sid,rep,m) for sid,_,_ in FRESH for rep,order in enumerate(orders) for m in order]
 check(len(validations)<=len(timings),'validation prefix within returned timing prefix')
 for i,v in enumerate(validations):
  must(i<len(expected_timing),'validation inside schedule');check((v['id'],v['rep'],v['method'])==expected_timing[i] and v['passed'] is True,'ordered successful timing validation prefix',i)
 timing_by_key={};timing_groups={}
 for i,t in enumerate(timings):
  CURRENT={'phase':'saved-timing','index':i};must(i<len(expected_timing),'timing prefix within schedule');sid,rep,m=expected_timing[i]
  check((t['id'],t['rep'],t['method'])==(sid,rep,m) and t['warmup']==(rep==0),'exact timing identity/order/warmup')
  required=complete or i<len(validations);timing_by_key[(sid,rep,m)]=t
  scientific(t.get('ok') is True,'Timed query rejected',required)
  scientific(finite([t.get('wallSeconds')]) and t['wallSeconds']>0,'Invalid timed duration',required)
  call=call_by_key.get((sid+'-timing-'+str(rep)+'-'+m,m));basecall=call_by_key.get((sid,m))
  if call: check(all(call.get(k)==t.get(k) for k in ['ok','wallSeconds','counts','checksum','shadowCounts','selectedSourceWork']),'returned timing/call evidence equality')
  if t.get('ok'):
   check(finite([t['checksum']]),'finite returned timing checksum')
   if basecall:
    scientific(basecall['counts']==t['counts'],'Timed work counters changed',required)
    scientific(basecall['checksum']==t['checksum'],'Timed checksum changed',required)
    if m=='Z': scientific(basecall['shadowCounts']==t['shadowCounts'] and basecall['selectedSourceWork']==t['selectedSourceWork'],'Timed Z shadow/selected counters changed',required)
   if sid in all_rows and m in all_rows[sid]:
    checksum=0.0
    for row in all_rows[sid][m]:
     for value in row: checksum+=value
    scientific(close(t['checksum'],checksum),'Timing checksum versus retained correctness scalars',required)
   g=timing_groups.setdefault(sid,{}).setdefault(m,{'warmup':[],'measured':[]});g['warmup' if rep==0 else 'measured'].append(t['wallSeconds'])
 timing_summary={}
 for sid,methods in timing_groups.items():
  out={}
  for m,g in methods.items():
   vals=g['measured'];out[m]={'warmupSeconds':g['warmup'],'measuredSeconds':vals,'measuredCount':len(vals),'minimum':min(vals) if vals else None,'maximum':max(vals) if vals else None,'median':median8(vals) if len(vals)==8 else None}
   if complete: check(len(g['warmup'])==1 and len(vals)==8,'one warmup and eight measured passes',sid+'-'+m)
  timing_summary[sid]=out
 REPORT['timingSummaries']=timing_summary;by_case={}
 for sid,n,expected in FRESH:
  blocks=[]
  for rep in range(1,9):
   group=[timing_by_key.get((sid,rep,m)) for m in ['M','Z','E','L']]
   if not all(t and t.get('ok') and finite([t.get('wallSeconds')]) and t['wallSeconds']>0 for t in group): break
   values={m:t['wallSeconds'] for m,t in zip(['M','Z','E','L'],group)}
   blocks.append({'rep':rep,**values,'E_over_Z':values['E']/values['Z'],'L_over_E':values['L']/values['E'],'L_over_M':values['L']/values['M']})
  if len(blocks)!=8: continue
  cost={}
  for ratio in ['E_over_Z','L_over_E']:
   a,b=ratio.split('_over_');med=median8([x[ratio] for x in blocks]);wins=sum(x[a]<x[b] for x in blocks)
   cost[ratio]={'medianPairedRatio':med,'fasterBlocks':wins,'met':med<=.95 and wins>=7}
  marginal={m:{'median':median8([x[m] for x in blocks]),'minimum':min(x[m] for x in blocks),'maximum':max(x[m] for x in blocks)} for m in ['M','Z','E','L']}
  by_case[sid]={'blocks':blocks,'criteria':cost,'timeSummary':marginal,'medianPairedLOverM':median8([x['L_over_M'] for x in blocks]),'scope':'Descriptive technical blocks, no population confidence interval'}
 performance={'byCase':by_case,'jointCriteria':{r:len(by_case)==2 and all(x['criteria'][r]['met'] for x in by_case.values()) for r in ['E_over_Z','L_over_E']}}
 if complete: check(set(by_case)=={x[0] for x in FRESH},'two complete paired performance inputs')
 if (raw/'performance.json').exists():
  saved_performance=read(raw/'performance.json');check(equivalent(performance,saved_performance),'independent paired E/Z and L/E ratios/wins/criteria/timeSummary')
  if complete: check(saved_performance==result['performance'],'terminal/performance artifact equality')
 elif complete: check(False,'completed campaign retains performance artifact')
 REPORT['performance']=performance;REPORT['performanceQualified']=complete
 REPORT['performanceInterpretation']='Separate prespecified descriptive criteria. An unmet criterion is a completed negative cost result if numerical qualification completed; incompleteness cannot qualify a primary cost conclusion.'
 CURRENT={'phase':'failure-witness-and-budget'}
 if failed:
  err=result['error'];detail=result.get('detail') or {};ctx=result.get('context') or {};w=ctx.get('witness');reproduced=None
  if err=='Bitwise output equivalence failed':
   a=base64.b64decode(detail['actualRowFloat64LEBase64'],validate=True);b=base64.b64decode(detail['referenceRowFloat64LEBase64'],validate=True)
   must(len(a)==len(b)==136,'failure bitwise full-row byte lengths');k=detail['k'];must(isinstance(k,int) and 0<=k<17,'failure component index')
   reproduced=a[8*k:8*k+8]!=b[8*k:8*k+8]
   av=list(struct.unpack('<17d',a));bv=list(struct.unpack('<17d',b))
   check(all((v==j or (j is None and not math.isfinite(v))) for v,j in zip(av,detail['actualRow'])) and all((v==j or (j is None and not math.isfinite(v))) for v,j in zip(bv,detail['referenceRow'])),'failure row JSON/numerical bytes agreement')
   REPORT['bitwiseFailure']={'actualHex':a[8*k:8*k+8].hex(),'referenceHex':b[8*k:8*k+8].hex(),'component':k,'signedZeroDistinguished':av[k]==bv[k]==0 and reproduced}
  elif err=='Exact equivalence checksum':
   a=base64.b64decode(detail['actualFloat64LEBase64'],validate=True);b=base64.b64decode(detail['referenceFloat64LEBase64'],validate=True);must(len(a)==len(b)==8,'failure checksum byte lengths');reproduced=a!=b
   REPORT['bitwiseFailure']={'actualHex':a.hex(),'referenceHex':b.hex(),'type':'checksum'}
  elif err=='Timed decisions changed':
   a=detail['actual'];b=detail['reference'];am=base64.b64decode(a['maskBase64'],validate=True);bm=base64.b64decode(b['maskBase64'],validate=True)
   must(len(am)==len(bm)==(CASE_INFO[detail['id']]['n']+3)//4,'timed failure complete mask byte lengths');reproduced=am!=bm or a!=b
   REPORT['timedDecisionFailure']={'actualMaskSha256':sha(am),'referenceMaskSha256':sha(bm),'receiver':detail['i']}
  elif err=='Full implementation mismatch':
   a,b=detail['actual'],detail['reference'];check(close(abs(a-b),detail['d']) and detail['actualRow'][detail['k']]==a and detail['referenceRow'][detail['k']]==b,'failure scalar/full-row consistency');reproduced=abs(a-b)>detail['t']
  elif err=='Claimed exact-zero source has nonzero term': reproduced=detail['term']!=0
  elif err=='Claimed-zero eligibility/support mismatch': reproduced=detail['support'] not in [1,2,4,5,6,7]
  elif err=='Timed work counters changed': reproduced=detail['actual']!=detail['expected']
  elif err in ['Domain decisions differ','Expected valid case rejected','Expected rejection accepted']:
   sid=detail.get('id');dec=[call_by_key.get((sid,m),{}).get('ok') for m in ['M','Z','E','L','I']];reproduced=len(set(dec))>1 if err=='Domain decisions differ' else dec[0] is False if err=='Expected valid case rejected' else dec[0] is True
  elif err=='Cooperative time cap': reproduced=detail.get('elapsed',0)>=cfg['wallCapSeconds']-2
  elif err=='Raw evidence cap': reproduced=detail.get('bytes',0)+detail.get('nextBytes',0)>=cfg['rawByteCap']-cfg['failureReserveBytes'] if 'nextBytes' in detail else None
  else: reproduced=any(v['gate']==err for v in VIOLATIONS) or None
  if w:
   n=ctx['n'];tb=base64.b64decode(w['termsBase64'],validate=True);codes=base64.b64decode(w['codesBase64'],validate=True)
   check(len(tb)==4*n*8 and len(codes)==4*n,'full current-receiver failure vectors preserved');terms=[v[0] for v in struct.iter_unpack('<d',tb)];check(finite(terms),'finite retained failure terms')
   if 'j' in detail and 'k' in detail and 'term' in detail: check(terms[4*detail['j']+detail['k']]==detail['term'],'failure term matches saved full witness')
  if reproduced is not None: check(reproduced,'terminal failure reproduced from saved scalars/bytes/decisions')
  REPORT['failureAnalysis']={'recordedError':err,'detail':detail,'contextIdentity':{k:ctx.get(k) for k in ['id','method','n','receiver','stage']},'reproducedWithoutNewScience':reproduced,'evidenceIncomplete':bool(result.get('evidenceIncomplete')),'note':'Null reproduction means insufficient retained evidence for this failure class; no geometry/model evaluation attempted.'}
 if complete: check(entry['exitCode']==0 and entry['completeProcess'] and not budget['requiresFailureReview'],'completed scientific status matches supervisor')
 if failed: check(entry['exitCode']!=0 and budget['requiresFailureReview'],'failed scientific status matches supervisor')
 scientific(raw_bytes<cfg['rawByteCap'],'raw storage cap',complete)
 scientific(0<entry['wallSeconds']<cfg['wallCapSeconds'],'scientific executable wall cap',complete)
 if result and 'elapsedSeconds' in result: check(finite([result['elapsedSeconds']]) and 0<=result['elapsedSeconds']<=entry['wallSeconds'],'driver/supervisor elapsed accounting')
 if failed and result.get('evidenceIncomplete'):
  REPORT['failureEvidenceIncomplete']=True;REPORT['discardedFailureSerialization']=result.get('failureSerialization');check((raw/'failure.json').stat().st_size<=cfg['failureReserveBytes'],'bounded failure serialization')
 if complete: check(raw_bytes<cfg['rawByteCap']-cfg['failureReserveBytes'],'success preserves failure reserve')
 REPORT['retainedCoverage']=dict(diagnostic)
 REPORT['budgetAndInventory']={'rawFiles':len(raw_inventory),'rawBytes':raw_bytes,'supervisor':entry,'terminalFlagAtReview':budget['terminal'],'completedCaseSummaries':len(saved_summaries),'recordedCalls':len(calls),'timingsRetained':len(timings)}
 REPORT['scientificQualificationCompleted']=complete
 REPORT['outcome']='Complete campaign retained evidence reviewed' if complete else 'Terminal incomplete/failed evidence reviewed; no qualification claim'
exit_code=0
with (RUN/'stdout.txt').open('w') as stdout,(RUN/'stderr.txt').open('w') as stderr:
 with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
  signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,55)
  try:
   if len(sys.argv)!=7 or sys.argv[2]!='--source-commit' or sys.argv[4]!='--freeze-sha256' or sys.argv[6]!='--authorized-after-science': raise ValueError('Requires authorization: python3 m31-zero-screen-saved-review.py REPOSITORY --source-commit SHA --freeze-sha256 SHA256 --authorized-after-science')
   SOURCE,FREEZE=sys.argv[3],sys.argv[5]
   must(SOURCE=='4717d9b5bb3d82fe2b3d75ea26801de201d124b6' and FREEZE=='2f1313c8476c09352ae22711be15afce5c7a3d229755a0502b1266201cb41f6a','externally supplied published source and freeze identities')
   (RUN/'arguments.json').write_text(json.dumps(sys.argv,indent=2)+'\n')
   verify(Path(sys.argv[1]).resolve())
  except BaseException as exc:
   exit_code=1;REPORT['exception']={'type':type(exc).__name__,'message':str(exc),'context':CURRENT};traceback.print_exc()
  finally: signal.setitimer(signal.ITIMER_REAL,0)
  REPORT.update({'checkCount':sum(CHECKS.values()),'checkCategories':dict(CHECKS),'failedCheckCount':FAILED,'failedChecks':FAILURES,'observedScientificGateViolations':VIOLATIONS,'passed':exit_code==0 and FAILED==0,'verificationWallSecondsBeforeOutput':time.perf_counter()-START})
  if not REPORT['passed']: exit_code=1
  canonical=Path('/tmp/m31-zero-screen-saved-review.json');REPORT['canonicalAlreadyExisted']=canonical.exists()
  def json_safe(value):
   if isinstance(value,float) and not math.isfinite(value): return {'nonfiniteFloat':str(value)}
   if isinstance(value,dict): return {k:json_safe(v) for k,v in value.items()}
   if isinstance(value,(list,tuple)): return [json_safe(v) for v in value]
   return value
  serialized=json.dumps(json_safe(REPORT),indent=2,allow_nan=False)+'\n';(RUN/'review.json').write_text(serialized)
  try:
   with canonical.open('x') as handle: handle.write(serialized)
  except FileExistsError: pass
  print(json.dumps({k:REPORT.get(k) for k in ['passed','scientificStatus','scientificQualificationCompleted','checkCount','failedCheckCount','failedChecks','exception','retainedCoverage','budgetAndInventory','timingSummaries','performance','performanceQualified','failureAnalysis']},indent=2))
runtime={'wallSecondsThroughReviewAndLogs':time.perf_counter()-START,'internalAlarmSeconds':55,'authorizedWallSeconds':60,'exitCode':exit_code,'passed':REPORT['passed'],'checkCount':REPORT['checkCount'],'checkerSha256':sha(SCRIPT),'invocationArchive':str(RUN)}
(RUN/'runtime.json').write_text(json.dumps(runtime,indent=2)+'\n')
print((RUN/'stdout.txt').read_text(),end='')
if (RUN/'stderr.txt').stat().st_size: print((RUN/'stderr.txt').read_text(),end='',file=sys.stderr)
print(json.dumps({'runtime':runtime}))
raise SystemExit(exit_code)
