import time
start=time.monotonic(); cpu0=time.process_time()
import os,json,hashlib,pathlib,collections,sys
ROOT=pathlib.Path('research-next/implementation'); BASE=ROOT.parent; OUT=BASE/'postrun-robustness'
def checktime():
 if time.monotonic()-start>30: raise TimeoutError('Verification-only30second wall cap')
def read(p):
 checktime(); return json.loads(pathlib.Path(p).read_text())
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  while True:
   checktime();b=f.read(1048576)
   if not b: break
   h.update(b)
 return h.hexdigest()
r={'schema':'independent-postrun-retention-verification/v1','scope':'Existing artifact identity/shape/count/timing verification only; no integration, field/controller evaluation, fixture rerun or scientific trajectory comparison','checks':[],'errors':[]}
try:
 sup=read(ROOT/'results/supervisor.json'); validity=read(ROOT/'results/execution-validity.json');campaign=read(ROOT/'results/campaign.json');matrix=read(ROOT/'results/matrix-status.json'); freeze=read(ROOT/'FREEZE.json')
 r['supervisor']={k:sup.get(k)for k in ['status','code','signal','killed','elapsedWallMs','totalCpuSeconds','retainedBytes','exactStoppedState']};r['validity']=validity;r['matrixCounts']=dict(collections.Counter(x['status'] for x in matrix['rows']));r['matrix']=matrix['rows'];r['campaign']={k:campaign.get(k)for k in ['status','phase','failure','runIds','provisionalAllScientificGatesPassed','requiresSupervisorValidity']};r['savedGates']=[{'name':g.get('name'),'seed':g.get('seed'),'passed':g.get('passed')}for g in campaign.get('gates',[])];r['jobs']=campaign.get('jobs',[])
 fixtures=read(ROOT/'results/fixtures.json');r['fixtures']={'implementation':{'passed':fixtures['passed'],'tests':len(fixtures['outcomes'])},'independent':[]}
 for p in sorted((ROOT/'results/fixtures').glob('*.cjs.json')):
  f=read(p);body=json.loads(f['stdout']);r['fixtures']['independent'].append({'file':p.name,'processStatus':f['status'],'signal':f['signal'],'passed':body['passed'],'tests':len(body['tests']),'failures':[x for x in body['tests'] if not x['passed']]})
 r['fixtures']['totalTests']=r['fixtures']['implementation']['tests']+sum(x['tests']for x in r['fixtures']['independent'])
 r['sourceIdentity']={'sourceChecked':0,'inputChecked':0,'mismatches':[]}
 for group,prefix in [('source',ROOT),('inputs',BASE)]:
  for item in freeze[group]['files']:
   p=prefix/item['path'];actual=digest(p);r['sourceIdentity']['sourceChecked'if group=='source'else'inputChecked']+=1
   if actual!=item['sha256']:r['sourceIdentity']['mismatches'].append({'path':str(p),'expected':item['sha256'],'actual':actual})
 for relative,key in [('PLAN.md','planSha256'),('ADOPTION.json','adoptionSha256'),('STORAGE-AMENDMENT-001.json','storageAmendmentSha256')]:
  actual=digest(BASE/relative);r['checks'].append({'check':'freeze-document','path':relative,'matches':actual==freeze[key],'sha256':actual})
 r['binaryFiles']=[];seen=set()
 def scan(obj):
  checktime()
  if isinstance(obj,dict):
   rel=obj.get('path'); expected=obj.get('sha256'); bytes_=obj.get('bytes')
   if isinstance(rel,str) and rel.startswith('results/') and isinstance(expected,str) and len(expected)==64 and isinstance(bytes_,int):
    p=ROOT/rel
    if rel not in seen:
     seen.add(rel);size=p.stat().st_size;actual=digest(p);v={'path':rel,'bytes':size,'expectedBytes':bytes_,'sizeMatches':size==bytes_,'sha256Matches':actual==expected,'sha256':actual}
     if 'shape'in obj:
      shape=obj['shape'];product=8
      for q in shape:product*=q
      v.update(shape=shape,shapeByteProduct=product,shapeBytesMatch=product==size)
     if rel.endswith('.bin'):v.update(complete32ByteRecords=size//32,trailingBytes=size%32)
     r['binaryFiles'].append(v)
   for v in obj.values():scan(v)
  elif isinstance(obj,list):
   for v in obj:scan(v)
 for p in sorted((ROOT/'results').rglob('*.json')):scan(read(p))
 r['runs']=[]
 for p in sorted((ROOT/'results/runs').glob('*.json')):
  a=read(p);r['runs'].append({k:a.get(k)for k in ['runId','complete','endTick','stop','work','timing','metrics','heldTick']}|{'raw':a.get('denseStates')or a.get('commonStates'),'audit':{k:a['audit'].get(k)for k in ['samples','pairSamples','signatureChanges','stepRiskChecks','endpointRiskChecks','fullTrialRiskChecks']},'controllers':{'events':len(a['controllers']['events']),'shape':a['controllers']['shape']},'fieldEvents':{k:a['fieldEvents'].get(k)for k in ['count','bytes','tickSchedule']}})
 r['preflights']=[{k:a.get(k)for k in ['id','passed','visitedEndpoints','expectedEndpoints','controllerEvents']} for a in [read(p)for p in sorted((ROOT/'results/preflight').glob('*.json'))]];r['compatibility']=read(ROOT/'results/compatibility.json');r['lastDurableCheckpoint']={k:read(ROOT/'results/last-checkpoint.json').get(k)for k in ['runId','phase','tick','exactStoppedState','meaning']}
 r['failureFiles']=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':digest(p)}for p in sorted((ROOT/'results/failures').glob('*'))if p.is_file()]
 r['partialFiles']=[{'path':str(p.relative_to(BASE)),'bytes':p.stat().st_size}for p in BASE.rglob('*.partial')]
 r['currentRetainedBytes']=sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file());r['under200MBCap']=r['currentRetainedBytes']<=200000000
 r['status']='verification-complete';r['allIdentityChecksPassed']=not r['sourceIdentity']['mismatches'] and all(x['sizeMatches']and x['sha256Matches']and x.get('shapeBytesMatch',True)for x in r['binaryFiles']) and all(x['matches']for x in r['checks'])
except Exception as e:
 r['status']='verification-incomplete';r['errors'].append({'type':type(e).__name__,'message':str(e)})
r['verificationWallSecondsBeforeReportWrite']=time.monotonic()-start;r['verificationCpuSecondsBeforeReportWrite']=time.process_time()-cpu0
p=OUT/'VERIFICATION.json';p.write_text(json.dumps(r,indent=2)+'\n')
t={'wallSecondsIncludingPrimaryReportWrite':time.monotonic()-start,'cpuSecondsIncludingPrimaryReportWrite':time.process_time()-cpu0,'maximumWallSeconds':30,'independentOfOriginalNumericalWindow':True};(OUT/'VERIFICATION-TIMING.json').write_text(json.dumps(t,indent=2)+'\n')
print(json.dumps({k:r.get(k)for k in ['status','allIdentityChecksPassed','matrixCounts','fixtures','sourceIdentity','currentRetainedBytes','partialFiles','preflights','savedGates']},indent=2))
print(json.dumps({'timing':t,'supervisor':r.get('supervisor'),'validity':r.get('validity'),'runTimings':[{'id':a['runId'],'complete':a['complete'],'endTick':a['endTick'],'timing':a['timing'],'work':a['work'],'audit':a['audit'],'raw':a['raw'],'controllers':a['controllers'],'fieldEvents':a['fieldEvents']}for a in r.get('runs',[])]},indent=2))
