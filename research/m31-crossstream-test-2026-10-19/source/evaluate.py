"""Frozen single-use cross-component diagnostic; no execution on import."""
import hashlib,json,math,pathlib,time
BASE=pathlib.Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
INPUT='research/m31-airflow-test-2026-10-19/results/comparison.json'
PRIOR='research/m31-airflow-scale-transfer-2026-10-19/results/comparison.json'
PINS={INPUT:(1112834,'dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3'),PRIOR:(1766917,'027165cb42fe4445496779d3f4cdb87a902248d38cdf9a8ddc4adfa1b042d269')}
GAIN=.5450089857597356
LIMITS=['Exposed same-experiment component diagnostic, not blind or independent validation','Positive lateral v assumed along increasing x; preprocessing unavailable','Empirical inherited gain is not SI calibration','Axisymmetric steady core completion only; no global continuity or momentum claim','No receiving-force, flight, flocking, safety or novelty claim','No experimental uncertainty or statistical rejection']
def guard():
 b=(BASE/'source-manifest.json').read_bytes();m=json.loads(b);r=json.loads((BASE/'source-publication.json').read_text());assert r['manifestSha256']==hashlib.sha256(b).hexdigest() and r['remoteBytesEqualLocal'] and r['committedBytesEqualLocal']
 for p in m['files']:
  raw=(ROOT/p['path']).read_bytes();assert len(raw)==p['bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],p['path']
 return r['commit']
def radial(r,z):
 k=2*math.sqrt(2);t=z+5.817*k;b=.07668*t;xi=r/b;a=math.sqrt(2)-1;uc=GAIN*10.11*k/t
 return uc/(1+a*xi*xi)**2,uc*.07668*.5*(xi-a*xi**3)/(1+a*xi*xi)**2,xi
def candidate(x,z):
 r=math.sqrt(x*x+1);u,vr,xi=radial(r,z)
 return {'radius':r,'xi':xi,'axialCore':u,'radialCandidate':vr,'candidate':vr*x/r,'baseline':0.}
def reason(c,v):
 if c['xi']>2:return 'outside-core'
 if v is None or not math.isfinite(v):return 'missing-lateral'
 return None
def metric(p,v):
 if not v:return None
 e=[a-b for a,b in zip(p,v)];ss=math.fsum(x*x for x in e);vv=math.fsum(x*x for x in v);n=len(v)
 return {'count':n,'mae':math.fsum(abs(x) for x in e)/n,'rmse':math.sqrt(ss/n),'bias':math.fsum(e)/n,'nrmse':math.sqrt(ss/vv) if vv>0 else None}
def controls():
 checks=[]
 for x in [0.,.5,2.]:
  p=candidate(x,15);n=candidate(-x,15);assert p['candidate']==-n['candidate'];assert abs(p['radius']**2-(x*x+1))<1e-13
 checks+=['odd symmetry at three fixed points','plane radial projection identity']
 a=math.sqrt(2)-1;t=15+5.817*2*math.sqrt(2);b=.07668*t
 assert abs(radial(b/math.sqrt(a),15)[1])<1e-15;assert radial(0,15)[1]==0
 checks+=['radial zero crossing','regular radial axis limit']
 residuals=[]
 for xi in [.3,1.,1.8]:
  r=xi*b;h=1e-5
  uz=(radial(r,15+h)[0]-radial(r,15-h)[0])/(2*h)
  rvr=((r+h)*radial(r+h,15)[1]-(r-h)*radial(r-h,15)[1])/(2*h*r)
  residuals.append(uz+rvr);assert abs(uz+rvr)<2e-8
 checks.append('three finite-difference continuity controls')
 assert metric([0.,0.],[-1.,1.])=={'count':2,'mae':1.,'rmse':1.,'bias':0.,'nrmse':1.}
 assert reason({'xi':2},None)=='missing-lateral' and reason({'xi':2.01},None)=='outside-core' and reason({'xi':2},-1.) is None
 checks+=['zero baseline metric','core boundary and missing-value precedence']
 return {'passed':True,'checks':checks,'continuityResiduals':residuals,'continuityTolerance':2e-8}
def main():
 t=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
 with (out/'launch.lock').open('x') as f:f.write('sole cross-component diagnostic\n')
 try:
  commit=guard();(out/'controls.json').write_text(json.dumps(controls(),indent=2)+'\n');docs={}
  for p,(size,sha) in PINS.items():
   raw=(ROOT/p).read_bytes();assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha;docs[p]=json.loads(raw)
  old=docs[INPUT];prior=docs[PRIOR];assert old['status']=='completed-descriptive-airflow-comparison' and prior['status']=='completed-scale-transfer-diagnostic' and prior['gains']['a']['gain']==GAIN
  rows=old['cases'];assert len(rows)==3240 and len({r['index'] for r in rows})==3240
  cases=[];exclusions={'outside-core':0,'missing-lateral':0}
  for r in rows:
   assert all(math.isfinite(r[k]) for k in ['X','Z','u','a','b']) and 8<=r['Z']<=30 and abs(r['X'])<=4
   c=candidate(r['X'],r['Z']);why=reason(c,r['v'])
   if why:exclusions[why]+=1
   cases.append({'original':r,**c,'included':why is None,'excludedReason':why,'residual':c['candidate']-r['v'] if why is None else None})
  included=[r for r in cases if r['included']];groups={'primary':[r for r in included if r['original']['Z']>=12],'near':[r for r in included if r['original']['Z']<12],'middle':[r for r in included if 12<=r['original']['Z']<20],'far':[r for r in included if r['original']['Z']>=20]}
  p=groups['primary'];assert len(p)>=20 and len({r['original']['Z'] for r in p})>=3 and math.fsum(r['original']['v']**2 for r in p)>0
  subsets={}
  for label,rs in groups.items():
   v=[r['original']['v'] for r in rs];subsets[label]={'count':len(rs),'baseline':metric([r['baseline'] for r in rs],v),'candidate':metric([r['candidate'] for r in rs],v)}
  b=subsets['primary']['baseline']['rmse'];c=subsets['primary']['candidate']['rmse'];contrast={'rmseReduction':b-c,'relativeRmseReduction':1-c/b}
  result={'status':'completed-cross-component-diagnostic','sourceCommit':commit,'inputs':[{'path':p,'bytes':v[0],'sha256':v[1]} for p,v in PINS.items()],'inheritedGain':GAIN,'cases':cases,'includedCount':len(included),'exclusions':exclusions,'subsets':subsets,'primaryContrast':contrast,'limits':LIMITS}
  data=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();assert len(data)<16*1024**2 and time.monotonic()-t<60;(out/'comparison.json').write_bytes(data)
  (out/'execution.json').write_text(json.dumps({'status':'complete','elapsedSeconds':time.monotonic()-t,'resultBytes':len(data),'sha256':hashlib.sha256(data).hexdigest()},indent=2)+'\n');print(json.dumps({'included':len(included),'exclusions':exclusions,'subsets':subsets,'contrast':contrast}))
 except BaseException as e:
  (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-t},indent=2)+'\n');raise
if __name__=='__main__':main()
