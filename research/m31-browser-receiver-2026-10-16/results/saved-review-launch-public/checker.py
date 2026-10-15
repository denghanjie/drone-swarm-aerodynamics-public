#!/usr/bin/env python3
"""One saved-only receiver audit. No source imports, solver, GPU, or browser calls."""
import argparse,collections,hashlib,json,math,os,pathlib,platform,struct,sys,time,traceback
P=argparse.ArgumentParser()
P.add_argument('--repo',required=True)
P.add_argument('--source-commit',required=True)
P.add_argument('--freeze-sha256',required=True)
P.add_argument('--output',required=True)
P.add_argument('--private-cleanup')
P.add_argument('--private-cleanup-sha256')
P.add_argument('--review-lock',default='/tmp/m31-browser-receiver-saved-review.lock')
A=P.parse_args()
START=time.perf_counter()
with open(A.review_lock,'x') as handle:handle.write('Permanent sole saved-only review reservation; never remove or rerun.\n')
REPO=pathlib.Path(A.repo).resolve();BASE=REPO/'research/m31-browser-receiver-2026-10-16';RAW=BASE/'raw'
PUBLIC_ARGV=list(sys.argv)
if '--private-cleanup' in PUBLIC_ARGV:PUBLIC_ARGV[PUBLIC_ARGV.index('--private-cleanup')+1]='<private cleanup path retained in original invocation archive>'
REPORT={'scope':'Saved-only algebra/evidence audit; no scientific modules, root solving, Newton, field, geometry, browser or GPU execution','sourceCommitExpected':A.source_commit,'freezeSha256Expected':A.freeze_sha256,'argv':PUBLIC_ARGV,'originalArgvSha256':hashlib.sha256(json.dumps(sys.argv,separators=(',',':')).encode()).hexdigest(),'checks':0,'integrityFailures':0,'failureExamples':[],'scientificChecks':0,'scientificFindings':0,'scientificExamples':[],'batches':[],'rawFiles':[],'terminal':False,'fullSuiteQualified':False}
def guard():
 if time.perf_counter()-START>55:raise TimeoutError('Internal 55-second saved-review deadline')
def clean(x):
 if isinstance(x,float) and not math.isfinite(x):return repr(x)
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [clean(v) for v in x]
 return x
def check(ok,label,detail=None):
 REPORT['checks']+=1
 if not ok:
  REPORT['integrityFailures']+=1
  if len(REPORT['failureExamples'])<100:REPORT['failureExamples'].append({'check':label,'detail':clean(detail)})
 return bool(ok)
def science(ok,label,detail=None):
 REPORT['scientificChecks']+=1
 if not ok:
  REPORT['scientificFindings']+=1
  if len(REPORT['scientificExamples'])<100:REPORT['scientificExamples'].append({'check':label,'detail':clean(detail)})
 return bool(ok)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):guard();return pathlib.Path(path).read_bytes()
def js(path):return json.loads(read(path))
def finite(x):return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def integer(x):return finite(x) and int(x)==x
def close(x,y,atol=2e-15,rtol=2e-12):return finite(x) and finite(y) and abs(x-y)<=atol+rtol*max(abs(x),abs(y))
def bits(x):return struct.unpack('<I',struct.pack('<f',x))[0]
def f32(word):return struct.unpack('<f',struct.pack('<I',word))[0]
def f64hex(x):return struct.pack('<d',x).hex()
def rows(name,stride,kind='d'):
 path=RAW/name
 if not path.exists():return None
 b=read(path);size=struct.calcsize('<'+kind)*stride
 check(len(b)%size==0,'Complete binary row stride',{'file':name,'bytes':len(b),'strideBytes':size})
 return list(struct.iter_unpack('<'+kind*stride,b[:len(b)//size*size]))
def poly(x,alpha):return x*x*x+alpha*x-1
METRICS=['rootOriginalX','rootRepresentedX','originalCubicAtReturnedX','representedCubicAtReturnedX','rotorTotal','inputRepresentation','shaderVersusRepresented','alphaDivision','alphaForceEffect','rootX','rootForceEffect','finalMultiplication','hostResidual','shaderResidual','representedPower','originalPower']
NEW_ROOT_ROWS=0;NEW_ROOT_ITERATIONS=0;SOURCE_AUDITS={}
def root_record(row,alpha,force0,label,index):
 global NEW_ROOT_ROWS,NEW_ROOT_ITERATIONS
 NEW_ROOT_ROWS+=1
 if not science(len(row)==6 and all(finite(v) for v in row),'Finite independent root record',{'label':label,'index':index}):return False
 ar,x,f,lo,hi,it=row
 science(ar==alpha,'Independent alpha identity',{'label':label,'index':index,'actual':ar,'expected':alpha})
 science(0<=lo<=x<=hi<=1 and hi-lo<=G['referenceBracketWidth'],'Independent numerical bracket',{'label':label,'index':index,'row':row})
 science(integer(it) and 0<=it<=96,'Independent iteration metadata',{'label':label,'index':index,'iterations':it})
 if integer(it) and 0<=it<=96:NEW_ROOT_ITERATIONS+=int(it)
 science(abs(poly(x,ar))<=G['referenceResidualAbsolute'],'Independent root residual',{'label':label,'index':index,'residual':poly(x,ar)})
 science(poly(lo,ar)<=G['referenceResidualAbsolute'] and poly(hi,ar)>=-G['referenceResidualAbsolute'],'Numerical bracket endpoint residual signs with stated tolerance',{'label':label,'index':index})
 science(f==force0*x,'Independent force multiplication',{'label':label,'index':index})
 if ar==0:science(x==1 and lo==1 and hi==1 and it==0,'Independent zero-alpha identity',{'label':label,'index':index})
 return True

def source_reference(case_id,n):
 if case_id in SOURCE_AUDITS:return SOURCE_AUDITS[case_id]
 directory=REPO/CFG['sourceReferenceDirectory']/'raw';b=read(directory/(case_id+'-I.f64'))
 check(len(b)==n*17*8,'Prior I matrix byte coverage',case_id)
 matrix=list(struct.iter_unpack('<'+'d'*17,b))
 audit=[json.loads(v) for v in read(directory/(case_id+'-source-audit.ndjson')).decode().splitlines() if v.strip()]
 check(len(matrix)==n and len(audit)==n,'Prior matrix/audit row count',case_id)
 result=[]
 for i,(m,a) in enumerate(zip(matrix,audit)):
  if i%128==0:guard()
  check(a.get('receiver')==i and len(a.get('solutions',[]))==4,'Prior audit receiver/order',{'case':case_id,'row':i})
  for k,r in enumerate(a['solutions']):
   check(m[4+k]==r['thrust'],'Prior matrix/audit thrust identity',{'case':case_id,'row':i,'rotor':k})
   result.append((m[k],F0,VI,r['x'],m[4+k],r['bracket'][0],r['bracket'][1],r['iterations']))
 SOURCE_AUDITS[case_id]=result
 return result

def audit_valid(case_id,expected_n,saved_n=None):
 global NEW_ROOT_ROWS,NEW_ROOT_ITERATIONS
 original=rows(case_id+'-original.f64',8);packed=rows(case_id+'-packed.u32',4,'I');words=rows(case_id+'-gpu.u32',8,'I');qrows=rows(case_id+'-Q.f64',6);arows=rows(case_id+'-A.f64',6)
 found={k:len(v) if v is not None else None for k,v in [('original',original),('packed',packed),('gpu',words),('Q',qrows),('A',arows)]}
 result={'id':case_id,'expectedRecords':expected_n,'retainedRecords':found,'complete':all(v is not None and len(v)==expected_n for v in [original,packed,words,qrows,arows])}
 REPORT['batches'].append(result)
 if FULL_EXPECTED:check(result['complete'],'Full-suite binary row coverage',result)
 for name,rs in [('original',original),('packed',packed),('gpu',words),('Q',qrows),('A',arows)]:
  if rs is not None:check(len(rs)<=expected_n,'Bounded retained prefix',{'batch':case_id,'stream':name,'rows':len(rs)})
 if original is None:
  check(all(x is None for x in [packed,words,qrows,arows]),'No dependent records without originals',case_id);return
 if saved_n is not None:
  source_rows=source_reference(case_id,saved_n)
  for i,r in enumerate(original):check(i<len(source_rows) and struct.pack('<8d',*r)==struct.pack('<8d',*source_rows[i]),'Reused original R record bit identity',{'case':case_id,'index':i})
 else:
  for i,r in enumerate(original):
   NEW_ROOT_ROWS+=1
   if integer(r[7]):NEW_ROOT_ITERATIONS+=int(r[7])
   check(i<len(CFG['scalarInflows']) and f64hex(r[0])==f64hex(CFG['scalarInflows'][i]),'Scalar source order/bit identity',i)
 for i,r in enumerate(original):
  if i%128==0:guard()
  if not science(all(finite(x) for x in r),'Finite original reference',{'batch':case_id,'index':i}):continue
  U,f0,vi,x,f,lo,hi,it=r
  science(0<=U<=128 and f0==F0 and vi==VI,'Original input domain/constants',{'batch':case_id,'index':i})
  science(0<=lo<=x<=hi<=1 and hi-lo<=G['referenceBracketWidth'] and integer(it) and 0<=it<=96,'Original root bracket/iteration metadata',{'batch':case_id,'index':i})
  science(abs(poly(x,U/vi))<=1e-12 and abs(f-F0*x)<=1e-14,'Original reference equation/force',{'batch':case_id,'index':i})
  UQ=f32(bits(U));science(math.isfinite(UQ) and 0<=UQ<=128 and (UQ==0 if U==0 else UQ>0 and UQ/VQ>=2**-120),'Packed input admission',{'batch':case_id,'index':i})
  if packed is not None and i<len(packed):check(packed[i]==(bits(U),bits(FQ),bits(VQ),0),'Exact packed input bits',{'batch':case_id,'index':i})
 if qrows is not None:
  for i,r in enumerate(qrows):
   if i%128==0:guard()
   if check(i<len(original),'Q prefix aligns with original',{'batch':case_id,'index':i}):root_record(r,f32(bits(original[i][0]))/VQ,FQ,case_id+'/Q',i)
 if arows is not None:
  for i,r in enumerate(arows):
   if i%128==0:guard()
   if check(words is not None and i<len(words),'A prefix aligns with GPU',{'batch':case_id,'index':i}):root_record(r,f32(words[i][0]),FQ,case_id+'/A',i)
 if qrows is not None and arows is not None:check(len(arows)<=len(qrows)<=len(arows)+1,'Alternating Q/A complete prefixes',case_id)
 if words is None:
  check(qrows is None and arows is None,'No Q/A without GPU readback',case_id);return
 stops=collections.Counter();zero_steps=0;caps=0;old_failures=0;gate_failures=0;first_failure=None
 metric_values={k:[] for k in METRICS};all_metrics=True;valid_metadata=True
 for i,w in enumerate(words):
  if i%128==0:guard()
  g=tuple(f32(v) for v in w)
  if not science(all(finite(v) for v in g),'Finite GPU output',{'batch':case_id,'index':i,'gpu':g}):valid_metadata=False;all_metrics=False;continue
  alpha,x,f,resid,it,stop,step,reserved=g
  ok=integer(it) and 0<=it<=12 and stop in (0,1,2) and reserved==0 and step>=0
  ok=ok and alpha>=0 and 0<x<=1 and 0<=f<=FQ
  U=original[i][0];UQ=f32(bits(U))
  if UQ==0:ok=ok and alpha==0 and x==1 and bits(f)==bits(FQ) and it==0 and stop==0 and step==0 and resid==0
  else:
   ok=ok and alpha>0 and it>=1 and stop!=0
   if stop==1:ok=ok and step<f32(bits(1e-15))
   if stop==2:ok=ok and it==12 and step>=f32(bits(1e-15))
  if not science(ok,'GPU domain/stop/zero metadata',{'batch':case_id,'index':i,'gpu':g}):valid_metadata=False
  if stop in (0,1,2):stops[str(int(stop))]+=1
  if stop==1 and step==0:zero_steps+=1
  if stop==2:caps+=1
  rf=original[i][4];rotor=abs(f-rf);old_failures+=rotor>G['originalRotorDiagnosticN']
  if not (0<x<=1 and 0<=f<=FQ and alpha>=0):all_metrics=False;continue
  if not(qrows is not None and arows is not None and i<len(qrows) and i<len(arows)):
   all_metrics=False
   if finite(rotor):science(rotor<=G['rotorTotalAbsoluteN'],'Retained GPU rotor gate',{'batch':case_id,'index':i,'error':rotor})
   continue
  q=qrows[i];a=arows[i];rx=original[i][3]
  if not all(finite(v) for v in q+a):all_metrics=False;continue
  aq,xq,fq,ql,qh,qi=q;aa,xa,fa,al,ah,ai=a
  ratio=f/FQ
  err={'rootOriginalX':abs(x-rx),'rootRepresentedX':abs(x-xq),'originalCubicAtReturnedX':abs(poly(x,U/VI)),'representedCubicAtReturnedX':abs(poly(x,aq)),'rotorTotal':rotor,'inputRepresentation':abs(fq-rf),'shaderVersusRepresented':abs(f-fq),'alphaDivision':abs(alpha-aq),'alphaForceEffect':abs(fa-fq),'rootX':abs(x-xa),'rootForceEffect':abs(FQ*(x-xa)),'finalMultiplication':abs(f-FQ*x),'hostResidual':abs(poly(x,alpha)),'shaderResidual':abs(resid),'representedPower':abs(ratio*(UQ/VQ/2+math.sqrt((UQ/VQ)*(UQ/VQ)/4+ratio))-1),'originalPower':abs(f*(U/2+math.sqrt(U*U/4+f/(2*1.225*AREA)))/(F0*VI)-1)}
  telescope=(fq-rf)+(fa-fq)+(FQ*x-fa)+(f-FQ*x)
  science(abs(telescope-(f-rf))<=1e-15,'Signed decomposition reconstruction',{'batch':case_id,'index':i})
  for k in METRICS:science(finite(err[k]),'Finite error diagnostic',{'batch':case_id,'index':i,'metric':k});metric_values[k].append((err[k],i))
  passed=rotor<=G['rotorTotalAbsoluteN'] and err['rootX']<=G['rootXAbsolute'] and err['hostResidual']<=G['hostResidualAbsolute'] and err['representedPower']<=G['representedPowerRatioAbsolute']
  science(passed,'Prespecified four receiver gates',{'batch':case_id,'index':i,'errors':{k:err[k] for k in ['rotorTotal','rootX','hostResidual','representedPower']}})
  if not passed:
   gate_failures+=1
   if first_failure is None:first_failure=i
 result.update(stopCounts={k:stops[k] for k in ['0','1','2']},exactZeroStepStops=zero_steps,iterationCapRecords=caps,oldPrecisionFailures=old_failures,computedGateFailures=gate_failures,allAvailableRowsHaveFullAttribution=all_metrics,metadataValid=valid_metadata)
 summary_path=RAW/(case_id+'-summary.json')
 if summary_path.exists():
  summary=js(summary_path);check(all_metrics and len(words)==expected_n,'Summary requires complete attribution',case_id)
  check(summary.get('id')==case_id and summary.get('n')==expected_n,'Batch summary identity',case_id)
  check(summary.get('stops')==result['stopCounts'],'Recomputed stop totals',case_id)
  for k in ['exactZeroStepStops','iterationCapRecords','oldPrecisionFailures']:check(summary.get(k)==result[k],'Recomputed '+k,case_id)
  check(summary.get('gateFailures')==gate_failures and summary.get('pass')==(gate_failures==0),'Recomputed batch gate outcome',case_id)
  check((summary.get('firstFailure') or {}).get('index')==first_failure,'First numerical gate failure index',case_id)
  check(summary.get('distinctOriginalInflows')==len(set(r[0] for r in original)) and summary.get('distinctPackedInflows')==len(set(bits(r[0]) for r in original)),'Distinct input counts',case_id)
  result['maxima']={}
  for k in METRICS:
   values=metric_values[k]
   if not values:check(False,'Missing metric values for summary',{'batch':case_id,'metric':k});continue
   maximum,index=max(values,key=lambda x:x[0]);m=summary.get('maxima',{}).get(k,{})
   check(close(m.get('value'),maximum),'Recomputed maximum',{'batch':case_id,'metric':k,'saved':m.get('value'),'computed':maximum})
   candidates={idx:v for v,idx in values};mi=m.get('index')
   check(isinstance(mi,int) and mi in candidates and close(candidates.get(mi),maximum),'Maximum index identifies a numerical maximum',{'batch':case_id,'metric':k,'savedIndex':mi,'computedIndex':index})
   result['maxima'][k]={'value':maximum,'index':index}
  if DRIVER is not None:check(summary in DRIVER.get('batches',[]),'Raw summary agrees with driver result',case_id)
 elif FULL_EXPECTED:check(False,'Missing full-suite summary',case_id)
 audit_api(case_id,len(words))

def audit_api(case_id,n):
 rp=RAW/(case_id+'-readback.json');ap=RAW/(case_id+'-api.json')
 if rp.exists():
  r=js(rp);d=r.get('dispatch',{})
  check(r.get('returnedCount')==n and r.get('words')==8*n,'Readback declared coverage',case_id)
  check(d.get('count')==n and d.get('groups')==(n+63)//64 and d.get('inputBytes')==16*n and d.get('outputBytes')==32*n and d.get('submitted') is True,'Submitted dispatch metadata',case_id)
 elif FULL_EXPECTED:check(False,'Missing full-suite readback metadata',case_id)
 if ap.exists():
  api=js(ap);science(not api.get('validation') and not api.get('loss') and not api.get('uncaptured'),'GPU API/scope/device health',{'batch':case_id,'api':api})
 elif FULL_EXPECTED:check(False,'Missing full-suite API metadata',case_id)

def audit_invalid():
 packed=rows('invalid5-packed.u32',4,'I');words=rows('invalid5-gpu.u32',8,'I')
 expected=[(bits(-1),bits(FQ),bits(VQ),0),(0x7fc00000,bits(FQ),bits(VQ),0),(0x7f800000,bits(FQ),bits(VQ),0),(bits(1),bits(FQ),0,0),(bits(1),bits(-1),bits(VQ),0)]
 complete=packed is not None and words is not None and len(packed)==5 and len(words)==5
 REPORT['batches'].append({'id':'invalid5','expectedRecords':5,'complete':complete,'retainedPacked':len(packed) if packed is not None else None,'retainedGPU':len(words) if words is not None else None})
 if FULL_EXPECTED:check(complete,'Complete invalid guards')
 if packed is not None:check(packed==expected,'Exact invalid raw input words')
 if words is not None:
  for i,w in enumerate(words):science(tuple(f32(v) for v in w)==(0,0,0,0,0,3,0,0),'Invalid guard complete sentinel',{'index':i,'words':w})
  audit_api('invalid5',len(words))
 sp=RAW/'invalid5-summary.json'
 if sp.exists():
  s=js(sp);check(complete and s.get('id')=='invalid5' and s.get('n')==5 and s.get('pass') is True,'Invalid guard summary')
  if DRIVER is not None:check(s in DRIVER.get('batches',[]),'Invalid raw/result summary agreement')
 elif FULL_EXPECTED:check(False,'Missing invalid summary')

try:
 script=read(__file__);executable=read(sys.executable)
 REPORT['checker']={'path':str(pathlib.Path(__file__).resolve()),'bytes':len(script),'sha256':sha(script),'python':sys.version,'executable':sys.executable,'executableBytes':len(executable),'executableSha256':sha(executable),'platform':platform.platform(),'lock':A.review_lock}
 check(len(A.source_commit)==40 and all(v in '0123456789abcdef' for v in A.source_commit),'Expected source commit format')
 freeze_bytes=read(BASE/'freeze.json');FREEZE=json.loads(freeze_bytes)
 check(sha(freeze_bytes)==A.freeze_sha256,'Expected freeze digest')
 pin_paths=set()
 for pin in FREEZE['files']:
  guard();p=(REPO/pin['path']).resolve();check(p.is_relative_to(REPO),'Contained frozen path',pin['path'])
  if not p.is_relative_to(REPO):continue
  b=read(p);check(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'Frozen bytes/hash',pin['path']);check(pin['path'] not in pin_paths,'Unique freeze path',pin['path']);pin_paths.add(pin['path'])
 REPORT['freezePinsChecked']=len(FREEZE['files'])
 CFG=js(BASE/'config.json');G=CFG['gates'];ENC=js(BASE/'constant-encoding.json');RUNTIME=js(BASE/'runtime-provenance.json')
 check(CFG['batchOrder']==['scalar32','invalid5','fresh1000','fresh5000'],'Frozen batch order')
 check(CFG['limits']['dispatches']==4 and CFG['limits']['gpuValidRoots']==24032 and CFG['limits']['gpuInvalidGuards']==5 and CFG['limits']['gpuIterationReservation']==288384 and CFG['limits']['hostBisectionRoots']==48096 and CFG['limits']['hostIterationReservation']==4617216,'Frozen reservations')
 check(CFG['limits']['fieldEvaluations']==0 and CFG['limits']['integrationSteps']==0 and CFG['timingComparison'] is False,'Excluded scientific work')
 F0=ENC['f0']['value'];VI=ENC['vi']['value'];AREA=ENC['area']['value'];FQ=f32(ENC['f0']['binary32Bits']);VQ=f32(ENC['vi']['binary32Bits'])
 check(f64hex(F0)==ENC['f0']['binary64LEHex'] and f64hex(VI)==ENC['vi']['binary64LEHex'] and bits(F0)==ENC['f0']['binary32Bits'] and bits(VI)==ENC['vi']['binary32Bits'],'Frozen original/packed constant encodings')
 check(F0==.027*9.81/4 and AREA==math.pi*.023*.023 and close(VI,math.sqrt(F0/(2*1.225*AREA)),atol=0,rtol=3e-16),'Frozen constant expressions')
 check(len(CFG['scalarInflows'])==32 and len(ENC['scalarInflows'])==32,'Scalar literal count')
 for i,u in enumerate(CFG['scalarInflows']):check(f64hex(u)==ENC['scalarInflows'][i]['binary64LEHex'] and bits(u)==ENC['scalarInflows'][i]['binary32Bits'],'Scalar literal encodings',i)
 DRIVER=js(RAW/'result.json') if (RAW/'result.json').exists() else None
 LEDGER=js(BASE/'results/budget.json') if (BASE/'results/budget.json').exists() else None
 FULL_EXPECTED=DRIVER is not None and DRIVER.get('status')=='completed' and DRIVER.get('pass') is True
 REPORT['recordedOutcome']=DRIVER.get('status') if DRIVER else 'partial-without-driver-result'
 if DRIVER:REPORT['driverOutcome']={k:DRIVER.get(k) for k in ['status','pass','error','cleanupErrors','cleanupError','elapsedSeconds']}
 check(LEDGER is not None,'Supervisor ledger retained')
 if LEDGER:
  check(LEDGER.get('terminal') is True and LEDGER.get('active') is False and LEDGER.get('attempts')==1 and LEDGER.get('retryPermitted') is False and LEDGER.get('status')=='closed','Terminal one-attempt supervisor ledger')
  check(LEDGER.get('wallCapSeconds')==180 and LEDGER.get('rawByteCap')==33554432,'Supervisor frozen caps')
  REPORT['supervisor']={k:LEDGER.get(k) for k in ['exitCode','timeout','wallSeconds','rawFiles','rawBytes','processGroupCleanup','launchError']}
 if RAW.exists():
  for p in sorted(RAW.iterdir()):
   check(p.is_file(),'Raw evidence is regular file',p.name)
   if p.is_file():b=read(p);REPORT['rawFiles'].append({'name':p.name,'bytes':len(b),'sha256':sha(b)})
 raw_map={r['name']:r for r in REPORT['rawFiles']};raw_size=sum(r['bytes'] for r in REPORT['rawFiles']);REPORT['rawByteTotal']=raw_size
 check(raw_size<=CFG['limits']['rawBytes'],'Raw byte cap')
 if LEDGER:check(LEDGER.get('rawFiles')==len(raw_map) and LEDGER.get('rawBytes')==raw_size,'Supervisor raw inventory agreement')
 if DRIVER:
  check(DRIVER.get('terminal') is True and DRIVER.get('sourceCommit')==A.source_commit,'Driver terminal/source identity')
  check(DRIVER.get('config')==CFG,'Driver frozen config')
  check(isinstance(DRIVER.get('pass'),bool),'Explicit scientific qualification flag')
  if DRIVER.get('status')!='completed':check(DRIVER.get('pass') is False,'Noncompleted cannot qualify')
  saved_files={r['name']:r for r in DRIVER.get('files',[])}
  check(set(saved_files)==set(raw_map)-{'result.json'},'Driver complete raw manifest coverage')
  for name,r in saved_files.items():check(raw_map.get(name)==r,'Driver raw file hash',name)
  other=BASE/'results/result.json'
  if other.exists():check(js(other)==DRIVER,'Duplicated terminal result equality')
  elif FULL_EXPECTED:check(False,'Full terminal public result exists')
  counts=DRIVER.get('counts',{});REPORT['operationCounts']=counts
  for k,cap in CFG['limits'].items():
   if k in counts:check(integer(counts[k]) and 0<=counts[k]<=cap,'Operation reservation cap',{'field':k,'actual':counts[k],'cap':cap})
  check(counts.get('gpuIterationReservation')==12*counts.get('gpuValidRoots',-1) and counts.get('hostIterationReservation')==96*counts.get('hostBisectionRoots',-1),'Attempt iteration reservation identities')
  d=counts.get('dispatches');prefix={0:(0,0),1:(32,0),2:(32,5),3:(4032,5),4:(24032,5)}
  check(d in prefix and (counts.get('gpuValidRoots'),counts.get('gpuInvalidGuards'))==prefix.get(d),'Fixed dispatch-prefix accounting')
  check(counts.get('fieldEvaluations')==0 and counts.get('integrationSteps')==0,'No field/integration work')
  if FULL_EXPECTED:check(d==4 and counts.get('hostBisectionRoots')==48096,'Full scheduled reservation accounting')
 started_path=RAW/'started.json'
 if started_path.exists():
  started=js(started_path);check(started.get('sourceCommit')==A.source_commit and started.get('freezeSha256')==A.freeze_sha256 and started.get('config')==CFG and started.get('invocations')==1,'Started source/freeze/config provenance')
  check(started.get('runtimePinsVerified')==RUNTIME['pins'],'Saved runtime pin identity')
 elif FULL_EXPECTED:check(False,'Full started provenance retained')
 cp=RAW/'constants.json'
 if cp.exists():
  c=js(cp);check(all(c.get(k)==v for k,v in [('F0',F0),('VI',VI),('FQ',FQ),('VQ',VQ),('area',AREA),('rho',1.225)]),'Saved original and represented constants')
 if (RAW/'served-source-contract.json').exists():
  contract=js(RAW/'served-source-contract.json');check(len(contract.get('files',[]))==3,'Served source contract coverage')
  for e in contract['files']:
   b=read(BASE/'source'/e['name']);check(len(b)==e['bytes'] and sha(b)==e['sha256'],'Served frozen source identity',e['name'])
 if DRIVER and FULL_EXPECTED:
  requests=DRIVER.get('servedSources',[]);check({x['name'] for x in requests}=={'browser.html','browser.js','receiver.wgsl'},'Actual served source request coverage')
  for e in requests:
   b=read(BASE/'source'/e['name']);check(len(b)==e['bytes'] and sha(b)==e['sha256'],'Actual served source request identity',e['name'])
 capability=js(RAW/'capability.json') if (RAW/'capability.json').exists() else None
 REPORT['capabilityEvidence']=capability
 if capability and FULL_EXPECTED:
  check(capability.get('supported') is True and capability.get('compiled') is True and capability.get('browserVersion')==RUNTIME['chromeBundleVersion'],'Browser capability/compiler/version')
  adapter=capability.get('adapter',{});check(adapter.get('isFallbackAdapter') is False,'Explicit nonfallback adapter')
  for name in ['limits','deviceLimits']:
   ls=adapter.get(name,{});check(ls.get('maxStorageBufferBindingSize',0)>=640000 and ls.get('maxBufferSize',0)>=640000 and ls.get('maxComputeWorkgroupsPerDimension',0)>=313,'Adapter/device frozen limits',name)
  check(not capability.get('validation') and not capability.get('loss') and not capability.get('uncaptured') and all(m.get('type')!='error' for m in capability.get('messages',[])),'Initialization error/loss/compile health')
 elif FULL_EXPECTED:check(False,'Full capability evidence retained')
 if DRIVER and DRIVER.get('status')=='unsupported':check(capability is not None and capability.get('supported') is False and DRIVER.get('counts',{}).get('dispatches')==0 and DRIVER.get('counts',{}).get('hostBisectionRoots')==0,'Unsupported terminal scope')
 audit_valid('scalar32',32);audit_invalid();audit_valid('fresh1000',4000,1000);audit_valid('fresh5000',20000,5000)
 REPORT['newReferenceRowsRetained']=NEW_ROOT_ROWS;REPORT['retainedNewReferenceIterations']=NEW_ROOT_ITERATIONS
 if DRIVER:
  counts=DRIVER.get('counts',{});hc=counts.get('hostBisectionRoots',-1);hi=counts.get('actualHostIterations',-1)
  check(NEW_ROOT_ROWS<=hc<=NEW_ROOT_ROWS+1,'New reference prefix versus charged attempts',{'retained':NEW_ROOT_ROWS,'charged':hc})
  check(NEW_ROOT_ITERATIONS<=hi<=NEW_ROOT_ITERATIONS+96*(hc-NEW_ROOT_ROWS),'Actual iteration accounting versus retained prefixes',{'retained':NEW_ROOT_ITERATIONS,'actual':hi})
  if FULL_EXPECTED:check(NEW_ROOT_ROWS==48096 and hc==NEW_ROOT_ROWS and hi==NEW_ROOT_ITERATIONS,'Complete reference/iteration accounting')
 if FULL_EXPECTED:
  for name in ['started.json','constants.json','served-source-contract.json','capability.json','process-registration-summary.json','final-gpu-health.json']:check(name in raw_map,'Required completed evidence file',name)
  check(DRIVER.get('batches') and [b.get('id') for b in DRIVER['batches']]==CFG['batchOrder'],'Driver completed batch order')
  check(not DRIVER.get('cleanupErrors') and not DRIVER.get('cleanupError'),'Driver cleanup health')
  health=js(RAW/'final-gpu-health.json');check(not health.get('loss') and not health.get('uncaptured'),'Final GPU health')
  registration=js(RAW/'process-registration-summary.json');check(registration.get('registeredBrowser') is True and registration.get('registeredDetachedGroups',0)>=1,'Registered detached browser before scientific work')
  if LEDGER:
   cleanup=LEDGER.get('processGroupCleanup',{});check(LEDGER.get('exitCode')==0 and LEDGER.get('timeout') is False and finite(LEDGER.get('wallSeconds')) and 0<=LEDGER['wallSeconds']<180,'Supervisor terminal time/exit')
   check(cleanup.get('confirmedAbsent') is True and cleanup.get('registryComplete') is True and not cleanup.get('errors') and cleanup.get('registeredDetachedGroups',0)>=1 and cleanup.get('groupsChecked',0)>=2,'Supervisor registry/ownership/group absence')
   check(0<=cleanup.get('killSignalsSent',-1)<=cleanup.get('ownershipChecksPassed',-1)<=cleanup.get('groupsChecked',-1),'Ownership-gated kill counts')
   check(finite(DRIVER.get('elapsedSeconds')) and 0<=DRIVER['elapsedSeconds']<=LEDGER['wallSeconds'],'Nested elapsed time consistency')
  check(REPORT['scientificFindings']==0,'Full-pass scientific findings absent',REPORT['scientificFindings'])
 if A.private_cleanup:
  private_bytes=read(A.private_cleanup);private=json.loads(private_bytes);details=private.get('cleanup',[]);entries=private.get('entries',[])
  check(isinstance(A.private_cleanup_sha256,str) and sha(private_bytes)==A.private_cleanup_sha256,'Private cleanup expected hash')
  REPORT['privateCleanupEvidence']={'supplied':True,'bytes':len(private_bytes),'sha256':sha(private_bytes),'groups':len(details),'registeredProcesses':len(entries),'identityDataOmitted':True,'liveOwnershipBranchExercised':any(x.get('ownershipVerified') for x in details),'killBranchExercised':any(x.get('killSent') for x in details),'limitation':'No failure-injection claim; branches not taken are not runtime-tested.'}
  check(private.get('registryComplete') is True,'Private registry complete')
  check(all(isinstance(x.get('pgid'),int) and x['pgid']>0 for x in details),'Private group identifiers valid')
  check(len({x['pgid'] for x in details})==len(details),'Private unique group coverage')
  expected_groups={private['nodePID']} if private.get('nodePID') else set()
  expected_groups.update(e['pid'] for e in entries if e.get('detached') and isinstance(e.get('pid'),int) and e['pid']>0)
  check({x['pgid'] for x in details}==expected_groups,'Private Node and detached groups covered')
  if FULL_EXPECTED:check(all(x.get('confirmedAbsent') is True and not x.get('identityUnconfirmed') and not x.get('cleanupErrorType') for x in details),'Private group absence/identity health')
  check(all(not x.get('killSent') or x.get('ownershipVerified') is True for x in details),'Private signals require verified ownership')
  if LEDGER:
   c=LEDGER.get('processGroupCleanup',{});check(c.get('groupsChecked')==len(details) and c.get('registeredProcesses')==len(entries) and c.get('registeredDetachedGroups')==sum(bool(e.get('detached') and e.get('pid')) for e in entries) and c.get('killSignalsSent')==sum(bool(x.get('killSent')) for x in details) and c.get('ownershipChecksPassed')==sum(bool(x.get('ownershipVerified')) for x in details),'Private/public cleanup aggregate agreement')
 else:REPORT['privateCleanupEvidence']={'supplied':False,'limitation':'Public terminal cleanup aggregates checked; private per-group record was not supplied.'}
 REPORT['fullSuiteQualified']=bool(FULL_EXPECTED and REPORT['integrityFailures']==0 and REPORT['scientificFindings']==0)
 REPORT['reviewPass']=REPORT['integrityFailures']==0
 REPORT['status']='consistent-full-pass' if REPORT['fullSuiteQualified'] else ('consistent-recorded-nonqualification' if REPORT['reviewPass'] else 'inconsistent-evidence')
except BaseException as e:
 REPORT['fatal']={'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc()};REPORT['reviewPass']=False;REPORT['fullSuiteQualified']=False;REPORT['status']='review-failed-or-incomplete'
finally:
 REPORT['terminal']=True;REPORT['elapsedSecondsBeforeOutput']=time.perf_counter()-START
 REPORT['interpretation']='Final-step metadata establishes only the recorded threshold/cap outcome. It does not establish oscillation, a multi-step trajectory, physical adequacy, full-field/flock correctness, speed or old binary64 compatibility.'
 payload=(json.dumps(clean(REPORT),indent=2,allow_nan=False)+'\n').encode()
 with open(A.output,'xb') as handle:handle.write(payload)
 print(json.dumps({'status':REPORT['status'],'reviewPass':REPORT.get('reviewPass',False),'fullSuiteQualified':REPORT['fullSuiteQualified'],'checks':REPORT['checks'],'scientificChecks':REPORT['scientificChecks'],'integrityFailures':REPORT['integrityFailures'],'scientificFindings':REPORT['scientificFindings'],'elapsedSeconds':time.perf_counter()-START,'outputBytes':len(payload),'outputSha256':sha(payload)},allow_nan=False))
sys.exit(0 if REPORT.get('reviewPass') else 1)
