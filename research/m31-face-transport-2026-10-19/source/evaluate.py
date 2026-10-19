"""Single-use fixed-model surface transports from saved values only."""
import hashlib,json,math,pathlib,struct,time
BASE=pathlib.Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
ANNULAR='research/m31-annular-balance-2026-10-19/results/comparison.json'
CROSS='research/m31-crossstream-test-2026-10-19/results/comparison.json'
PINS={ANNULAR:(3020398,'e7885559d832f4d7dc0136c9d5656a7c4a83c3ac6ab3aeee45e62c2d8562210a'),CROSS:(2291932,'1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a')}
IDS=['left-lower','left-middle','left-upper','right-lower','right-middle','right-upper'];FACES=['inner','outer','top','bottom'];TOL=2e-12
FIELDS=['axialCore','radialCandidate','candidate','radius','xi']
LIMITS=['Exposed same-experiment boundary diagnostic; no independent validation','Fixed inherited axialCore/radialCandidate; no fit or field evaluation','Axisymmetric no-swirl measured radial interpretation remains conditional','Measured denominator can hide relative radial errors; raw faces remain primary','Fixed coarsening is sensitivity, not experimental uncertainty or convergence','No physical threshold, calibration, force/swarm safety or novelty claim']
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is float:return struct.pack('>d',a)==struct.pack('>d',b)
 if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return type(a) in (int,str,bool,type(None)) and a==b
def finite(v):return type(v) in (int,float) and math.isfinite(v)
def guard():
 raw=(BASE/'source-manifest.json').read_bytes();pub=json.loads((BASE/'source-publication.json').read_text());assert pub['manifestSha256']==hashlib.sha256(raw).hexdigest() and pub['remoteBytesEqualLocal'] is True and pub['committedBytesEqualLocal'] is True
 for p in json.loads(raw)['files']:
  b=(ROOT/p['path']).read_bytes();assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'],p['path']
 return pub['commit']
def node_issues(c,p):
 issues=[]
 if c.get('included') is not True:issues.append('model-not-included')
 if c.get('excludedReason','missing') is not None:issues.append('model-exclusion-reason')
 for k in FIELDS:
  if not finite(c.get(k)):issues.append('nonfinite-'+k)
 if finite(c.get('radius')):
  if c['radius']<=0:issues.append('nonpositive-radius')
  if abs(c['radius']-p['R'])>TOL:issues.append('radius-mismatch')
 if finite(c.get('xi')) and not 0<=c['xi']<=2:issues.append('outside-core')
 return issues
def admission(projected,byid,membership):
 nodes=[{'index':p['index'],'regionId':membership[p['index']],'issues':node_issues(byid[p['index']],p),'radiusDifference':byid[p['index']]['radius']-p['R'] if finite(byid[p['index']].get('radius')) else None} for p in projected]
 counts={r:sum(bool(n['issues']) and n['regionId']==r for n in nodes) for r in IDS}
 return {'passed':not any(n['issues'] for n in nodes),'nodes':nodes,'regionFailures':counts,'issuesCount':sum(len(n['issues']) for n in nodes)}
def trap(x,y):
 assert len(x)==len(y) and len(x)>=2 and all(x[j+1]>x[j] for j in range(len(x)-1))
 return math.fsum((x[j+1]-x[j])*(y[j]+y[j+1])*.5 for j in range(len(x)-1))
def face(ids,coords,obs,model,sign):
 delta=[sign*(a-b) for a,b in zip(model,obs['integrand'])];qm=sign*trap(coords,model);e=qm-obs['value'];j=trap(coords,[abs(x) for x in delta]);cancel=j-abs(e);assert cancel>=-TOL
 return {'indices':ids,'coordinates':coords,'observedIntegrand':obs['integrand'],'modelIntegrand':model,'localSignedError':delta,'observedValue':obs['value'],'modelValue':qm,'signedError':e,'localAbsoluteError':j,'withinFaceCancellation':cancel}
def summarize(faces,observed_defect,scale):
 model=math.fsum(faces[k]['modelValue'] for k in FACES);error=math.fsum(faces[k]['signedError'] for k in FACES);vector=math.fsum(abs(faces[k]['signedError']) for k in FACES);local=math.fsum(faces[k]['localAbsoluteError'] for k in FACES);identity=error-(model-observed_defect);between=vector-abs(error);within=local-vector
 assert abs(identity)<=TOL and between>=-TOL and within>=-TOL and scale>=0
 return {'faces':faces,'observedDefect':observed_defect,'observedFluxScale':scale,'modelDefect':model,'errorSum':error,'balanceIdentityResidual':identity,'sumAbsoluteFaceError':vector,'sumLocalAbsoluteError':local,'betweenFaceCancellation':between,'withinFaceCancellation':within,'faceVectorFraction':vector/scale if scale>0 else None,'localErrorFraction':local/scale if scale>0 else None}
def compare(q,model):
 faces={}
 for name in FACES:
  wall=name in ['inner','outer'];f=q['faces'][name];coords=q['zCoordinates'] if wall else q['rCoordinates'];sign=-1 if name in ['inner','top'] else 1
  values=[model[i]['integrationRadius']*model[i]['radialCandidate' if wall else 'axialCore'] for i in f['indices']]
  faces[name]=face(f['indices'],coords,f,values,sign)
 return summarize(faces,q['defect'],q['fluxScale'])
def differences(full,coarse):
 return {'faces':{k:{v:coarse['faces'][k][v]-full['faces'][k][v] for v in ['signedError','localAbsoluteError']} for k in FACES},**{k:coarse[k]-full[k] if coarse[k] is not None and full[k] is not None else None for k in ['faceVectorFraction','localErrorFraction']}}
def transport(old,adm,byid):
 if not adm['passed']:return [],[{'id':i,'full':None,'coarse':None,'coarseMinusFull':None} for i in IDS]
 nodes=[{'index':p['index'],'integrationRadius':p['R'],**{k:byid[p['index']][k] for k in FIELDS}} for p in old['projectedNodes']];model={n['index']:n for n in nodes};regions=[]
 for r in old['regions']:
  f=compare(r['full'],model);c=compare(r['coarse'],model);regions.append({'id':r['id'],'full':f,'coarse':c,'coarseMinusFull':differences(f,c)})
 return nodes,regions
def controls():
 checks=[];x=[0.,1.,3.];ids=[0,1,2]
 def f(obs,mod,sign=1):return face(ids,x,{'integrand':obs,'value':sign*trap(x,obs)},mod,sign)
 for sign in [1,-1]:
  a=f([0.,0.,0.],[2.,2.,2.],sign);b=f([0.,0.,0.],[0.,1.,3.],sign);assert abs(a['modelValue']-sign*6)<=TOL and abs(b['modelValue']-sign*4.5)<=TOL
 checks.append('irregular constant and linear analytic integrals; both outward signs')
 a=f([1.,2.,4.],[1.,2.,4.]);assert a['signedError']==a['localAbsoluteError']==a['withinFaceCancellation']==0;checks.append('perfect face agreement')
 a=f([0.,0.,0.],[1.,-1.,0.]);assert abs(a['signedError']+1)<=TOL and abs(a['localAbsoluteError']-2)<=TOL and abs(a['withinFaceCancellation']-1)<=TOL;checks.append('within-face signed cancellation')
 fs={k:f([0.,0.,0.],[1.,1.,1.] if k=='inner' else [-1.,-1.,-1.] if k=='outer' else [0.,0.,0.]) for k in FACES};s=summarize(fs,0.,0.);assert s['errorSum']==0 and s['sumAbsoluteFaceError']==6 and s['betweenFaceCancellation']==6 and s['faceVectorFraction'] is None and s['localErrorFraction'] is None;checks.append('between-face cancellation and zero observed scale with nonzero error')
 base={k:f([1.,2.,4.],[2.,1.,5.],-1 if k in ['inner','top'] else 1) for k in FACES};s=summarize(base,0.,30.)
 for factor in [3.,-1.]:
  ff={k:f([factor*v for v in [1.,2.,4.]],[factor*v for v in [2.,1.,5.]],-1 if k in ['inner','top'] else 1) for k in FACES};ss=summarize(ff,0.,abs(factor)*30.)
  for k in FACES:
   for v in ['observedValue','modelValue','signedError']:assert abs(ff[k][v]-factor*base[k][v])<=TOL
   for v in ['localAbsoluteError','withinFaceCancellation']:assert abs(ff[k][v]-abs(factor)*base[k][v])<=TOL
  for v in ['faceVectorFraction','localErrorFraction']:assert abs(ss[v]-s[v])<=TOL
 checks.append('shared positive and negative scaling of signs, absolute errors and ratios')
 c={'included':True,'excludedReason':None,'radius':1.,'xi':2.,'axialCore':1.,'radialCandidate':0.,'candidate':0.};p={'R':1.}
 assert node_issues(c,p)==[] and 'outside-core' in node_issues(dict(c,xi=2.01),p);checks.append('closed model-domain boundary')
 assert 'nonfinite-axialCore' in node_issues({k:v for k,v in c.items() if k!='axialCore'},p) and 'nonfinite-candidate' in node_issues(dict(c,candidate=float('nan')),p);checks.append('missing and nonfinite model fields rejected')
 assert 'radius-mismatch' in node_issues(c,{'R':2.}) and 'model-not-included' in node_issues(dict(c,included=False),p);checks.append('radius mismatch and prior exclusion rejected')
 bad=admission([{'index':0,'R':1.}],{0:dict(c,xi=2.01)},{0:IDS[0]});nodes,regions=transport({},bad,{});assert not bad['passed'] and nodes==[] and len(regions)==6 and all(r['full'] is None and r['coarse'] is None and r['coarseMinusFull'] is None for r in regions);checks.append('one failed node globally suppresses all six transports')
 return {'passed':True,'checks':checks}
def main():
 t=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
 with (out/'launch.lock').open('x') as f:f.write('sole saved-model surface transport comparison\n')
 try:
  commit=guard();(out/'controls.json').write_text(json.dumps(controls(),indent=2)+'\n');docs={}
  for path,(size,sha) in PINS.items():
   raw=(ROOT/path).read_bytes();assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha;docs[path]=json.loads(raw)
  old=docs[ANNULAR];cross=docs[CROSS];assert old['status']=='completed-annular-balance' and old['selection']['admission']['passed'] and cross['status']=='completed-cross-component-diagnostic' and cross['inheritedGain']==.5450089857597356
  assert same(old['originalCases'],cross['cases']) and len(old['originalCases'])==3240 and len(old['projectedNodes'])==1220 and old['selection']['selectedCount']==1220
  assert [r['id'] for r in old['regions']]==IDS and all(r[k] is not None for r in old['regions'] for k in ['full','coarse'])
  byid={c['original']['index']:c for c in old['originalCases']};assert len(byid)==3240;membership={m['index']:m['regionId'] for m in old['selection']['membership'] if m['regionId'] is not None};assert len(membership)==1220 and set(membership)=={p['index'] for p in old['projectedNodes']}
  for p in old['projectedNodes']:
   o=byid[p['index']]['original'];assert all(same(p[a],o[b]) for a,b in [('X','X'),('Z','Z'),('U','u'),('v','v')])
  adm=admission(old['projectedNodes'],byid,membership);(out/'admission.json').write_text(json.dumps(adm,indent=2,allow_nan=False)+'\n');nodes,regions=transport(old,adm,byid)
  result={'status':'completed-face-transport' if adm['passed'] else 'admission-failed','sourceCommit':commit,'inputPins':[{'path':p,'bytes':v[0],'sha256':v[1]} for p,v in PINS.items()],'inheritedAnnular':old,'inheritedGain':cross['inheritedGain'],'admission':adm,'modelNodes':nodes,'regions':regions,'limits':LIMITS}
  raw=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();assert len(raw)<16*1024**2 and time.monotonic()-t<60;(out/'comparison.json').write_bytes(raw)
  (out/'execution.json').write_text(json.dumps({'status':'complete','scientificStatus':result['status'],'elapsedSeconds':time.monotonic()-t,'resultBytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},indent=2)+'\n');print(json.dumps({'status':result['status'],'admitted':adm['passed'],'regionFailures':adm['regionFailures'],'regions':[{'id':r['id'],'full':{k:r['full'][k] for k in ['faceVectorFraction','localErrorFraction','errorSum','betweenFaceCancellation','withinFaceCancellation']} if r['full'] else None,'coarseMinusFull':r['coarseMinusFull']} for r in regions]}))
 except BaseException as e:
  (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-t},indent=2)+'\n');raise
if __name__=='__main__':main()
