"""One-factor near-to-far transfer of saved airflow records. No execution on import."""
import hashlib,json,math,pathlib,time
BASE=pathlib.Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
INPUT='research/m31-airflow-test-2026-10-19/results/comparison.json'
DIGEST='dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3'
LIMITS=['Already exposed same-dataset records; not blind or independent validation','Empirical gains are not identified reference-speed calibrations','Original RSS reference fitted to this experimental study','Planar mean field; no3D wake, receiving-force or swarm validation','No experimental uncertainty or statistical rejection','Unknown spatially varying calibration and velocity observable differences remain']
def guard():
 b=(BASE/'source-manifest.json').read_bytes();m=json.loads(b);r=json.loads((BASE/'source-publication.json').read_text());assert r['manifestSha256']==hashlib.sha256(b).hexdigest() and r['remoteBytesEqualLocal'] and r['committedBytesEqualLocal']
 for p in m['files']:
  raw=(ROOT/p['path']).read_bytes();assert len(raw)==p['bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],p['path']
 return r['commit']
def fit(p,u):
 assert len(p)==len(u)>0 and all(math.isfinite(v) for v in p+u)
 num=math.fsum(a*b for a,b in zip(p,u));den=math.fsum(a*a for a in p)
 if den<=0:raise ValueError('zero predictor norm')
 g=max(0.,num/den);assert math.isfinite(g);return {'numerator':num,'denominator':den,'gain':g}
def metric(p,u):
 assert len(p)==len(u)>0
 es=[a-b for a,b in zip(p,u)];sq=math.fsum(e*e for e in es);usq=math.fsum(v*v for v in u)
 if usq<=0:raise ValueError('zero observed norm')
 return {'count':len(u),'mae':math.fsum(abs(e) for e in es)/len(u),'rmse':math.sqrt(sq/len(u)),'bias':math.fsum(es)/len(u),'nrmse':math.sqrt(sq/usq)}
def partition(rows):return [r for r in rows if r['Z']<12],[r for r in rows if r['Z']>=12]
def controls():
 assert fit([1.,2.,3.],[2.,4.,6.])['gain']==2 and fit([1.,2.],[-1.,-2.])['gain']==0
 p=[1.,2.,3.];u=[1.1,1.8,3.2];g=fit(p,u)['gain'];n=metric([g*v for v in p],u)['nrmse']
 for k in [.5,3.]:
  scaled=[k*v for v in u];gg=fit(p,scaled)['gain'];nn=metric([gg*v for v in p],scaled)['nrmse'];assert abs(gg-k*g)<1e-14 and abs(nn-n)<1e-14
 try:fit([0.,0.],[1.,2.])
 except ValueError:pass
 else:raise AssertionError('degenerate predictor accepted')
 rows=[{'Z':8.,'p':1.,'u':2.},{'Z':10.,'p':2.,'u':3.},{'Z':15.,'p':3.,'u':-100.}];a,_=partition(rows);f1=fit([x['p'] for x in a],[x['u'] for x in a]);rows[-1]['u']=100.;a,_=partition(rows);assert f1==fit([x['p'] for x in a],[x['u'] for x in a])
 return {'passed':True,'checks':['exact gain','nonnegative clamp','two positive scale invariances','degenerate denominator refused','evaluation-only perturbation leaves calibration unchanged']}
def main():
 t=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
 with (out/'launch.lock').open('x') as f:f.write('sole scale transfer diagnostic\n')
 try:
  commit=guard();(out/'controls.json').write_text(json.dumps(controls(),indent=2)+'\n');raw=(ROOT/INPUT).read_bytes();assert len(raw)==1112834 and hashlib.sha256(raw).hexdigest()==DIGEST
  old=json.loads(raw);rows=old['cases'];assert old['status']=='completed-descriptive-airflow-comparison' and len(rows)==3240 and len({r['index'] for r in rows})==3240
  for r in rows:
   assert all(math.isfinite(r[k]) for k in ['X','Z','u','a','b']) and r['a']>0 and r['b']>0 and 8<=r['Z']<=30 and abs(r['X'])<=4
  train,test=partition(rows);assert len(train)==800 and len(test)==2440
  gains={k:fit([r[k] for r in train],[r['u'] for r in train]) for k in ['a','b']}
  cases=[]
  for r in rows:
   ca=gains['a']['gain']*r['a'];cb=gains['b']['gain']*r['b'];cases.append({**r,'ca':ca,'cb':cb,'correctedResidualA':ca-r['u'],'correctedResidualB':cb-r['u'],'partition':'calibration' if r['Z']<12 else 'evaluation'})
  selected={'calibration':[r for r in cases if r['Z']<12],'evaluation':[r for r in cases if r['Z']>=12],'middle':[r for r in cases if 12<=r['Z']<20],'far':[r for r in cases if r['Z']>=20]};assert [len(selected[k]) for k in selected]==[800,2440,1640,800]
  subsets={}
  for name,rs in selected.items():
   subsets[name]={'count':len(rs)}
   for k in ['a','b']:subsets[name][k]={'raw':metric([r[k] for r in rs],[r['u'] for r in rs]),'corrected':metric([r['c'+k] for r in rs],[r['u'] for r in rs])}
  changes={}
  for k in ['a','b']:
   before=subsets['evaluation'][k]['raw']['mae'];after=subsets['evaluation'][k]['corrected']['mae'];changes[k]={'maeReduction':before-after,'relativeMaeReduction':1-after/before if before>0 else None}
  result={'status':'completed-scale-transfer-diagnostic','sourceCommit':commit,'inputPin':{'path':INPUT,'bytes':len(raw),'sha256':DIGEST},'gains':gains,'calibrationIndices':[r['index'] for r in train],'cases':cases,'subsets':subsets,'evaluationChanges':changes,'limits':LIMITS}
  b=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();assert len(b)<16*1024**2 and time.monotonic()-t<60;(out/'comparison.json').write_bytes(b)
  (out/'execution.json').write_text(json.dumps({'status':'complete','elapsedSeconds':time.monotonic()-t,'resultBytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},indent=2)+'\n');print(json.dumps({'gains':gains,'evaluation':subsets['evaluation'],'changes':changes}))
 except BaseException as e:
  (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-t},indent=2)+'\n');raise
if __name__=='__main__':main()
