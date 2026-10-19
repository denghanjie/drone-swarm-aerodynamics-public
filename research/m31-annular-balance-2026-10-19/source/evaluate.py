"""Single-use measured annular balance; no model evaluation or fitting."""
import hashlib,json,math,pathlib,time
BASE=pathlib.Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
INPUT='research/m31-lateral-symmetry-2026-10-19/results/comparison.json'
UPSTREAM='research/m31-airflow-test-2026-10-19/results/comparison.json'
PINS={INPUT:(3793293,'b253b7199df24e8a2d5ff3000bed1f73937cd898ada8449256c91f0172962be3'),UPSTREAM:(1112834,'dc5a713bb90d1f1303db5193dfc9bd4abb229f25e8674aa302ccd1aaf5c53bf3')}
BANDS=[('lower',12.,16.,False),('middle',16.,20.,False),('upper',20.,24.,True)]
LIMITS=['Exposed retained stride-four field, not complete raw PIV or independent trials','Axisymmetric no-mean-swirl projection on Y=1 is conditional','Unknown actual component calibration and stitching uncertainty','No physical pass threshold, significance or experimental error bound','Fixed coarsening is sensitivity, not convergence or measurement uncertainty','No new model prediction, fit, physical validity, force/swarm safety or novelty']
def finite(x):return type(x) in (float,int) and math.isfinite(x)
def pin(p,raw):return {'path':p,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def guard():
 raw=(BASE/'source-manifest.json').read_bytes();pub=json.loads((BASE/'source-publication.json').read_text());assert pub['manifestSha256']==hashlib.sha256(raw).hexdigest() and pub['remoteBytesEqualLocal'] and pub['committedBytesEqualLocal']
 for e in json.loads(raw)['files']:
  b=(ROOT/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
 return pub['commit']
def belongs(o,side,band):
 _,lo,hi,closed=band
 return (o['X']<0 if side=='left' else o['X']>0) and 1<=abs(o['X'])<=3 and lo<=o['Z'] and (o['Z']<=hi if closed else o['Z']<hi)
def region(rows,side,band):
 chosen=[o for o in rows if belongs(o,side,band)];xs={float(o['X']).hex():o['X'] for o in chosen};zs={float(o['Z']).hex():o['Z'] for o in chosen};xx=sorted(xs.values(),key=abs);zz=sorted(zs.values());cells={};issues=[]
 for o in chosen:cells.setdefault((float(o['X']).hex(),float(o['Z']).hex()),[]).append(o['index'])
 duplicate=sorted(i for ids in cells.values() if len(ids)>1 for i in ids)
 if duplicate:issues.append('duplicate-coordinate')
 missing_count=len(xx)*len(zz)-len(cells);missing=[];grid=[]
 if missing_count:
  for z in zz:
   for x in xx:
    if (float(x).hex(),float(z).hex()) not in cells:
     missing=[{'X':x,'Z':z}];break
   if missing:break
  issues.append('incomplete-tensor-grid')
 if not missing_count and not duplicate:
  grid=[[cells[(float(x).hex(),float(z).hex())][0] for x in xx] for z in zz]
 if len(xx)<5 or len(zz)<5:issues.append('insufficient-axis-levels')
 nonfinite=sorted(o['index'] for o in chosen if not finite(o['u']) or not finite(o['v']))
 if nonfinite:issues.append('nonfinite-selected-component')
 return {'id':side+'-'+band[0],'side':side,'nominalBand':{'lo':band[1],'hi':band[2],'upperInclusive':band[3]},'selectedIndices':[o['index'] for o in chosen],'xLevels':xx,'zLevels':zz,'nodeIndices':grid,'geometry':{'xLevels':len(xx),'zLevels':len(zz),'selectedCount':len(chosen),'uniqueCoordinateCount':len(cells),'expectedCount':len(xx)*len(zz),'minAbsX':min(map(abs,xx)) if xx else None,'maxAbsX':max(map(abs,xx)) if xx else None,'minZ':zz[0] if zz else None,'maxZ':zz[-1] if zz else None},'issues':issues,'duplicateIndices':duplicate,'missingCoordinateCount':missing_count,'missingCoordinatePreview':missing,'nonfiniteIndices':nonfinite}
def selection(rows,counts):
 regions=[region(rows,side,band) for side in ['left','right'] for band in BANDS];membership={i:r['id'] for r in regions for i in r['selectedIndices']};assert len(membership)==sum(len(r['selectedIndices']) for r in regions)
 issues=[]
 if counts['nonfiniteCoordinates']!=0:issues.append('upstream-nonfinite-coordinates')
 if counts['missingU']!=0:issues.append('upstream-missing-axial')
 for r in regions:
  issues.extend(r['id']+':'+code for code in r['issues'])
 return {'admission':{'passed':not issues,'issues':issues,'upstreamNonfiniteCoordinates':counts['nonfiniteCoordinates'],'upstreamMissingU':counts['missingU']},'membership':[{'index':o['index'],'regionId':membership.get(o['index']),'reason':'selected' if o['index'] in membership else 'outside-windows'} for o in rows],'selectedCount':len(membership),'outsideCount':len(rows)-len(membership),'regions':regions}
def coarse_ids(n):
 ids=list(range(0,n,2))
 if ids[-1]!=n-1:ids.append(n-1)
 return ids
def trap(coords,values):return math.fsum((coords[i+1]-coords[i])*(values[i]+values[i+1])*.5 for i in range(len(coords)-1))
def integrate(r,byid,coarse=False):
 xi=coarse_ids(len(r['xLevels'])) if coarse else list(range(len(r['xLevels'])));zi=coarse_ids(len(r['zLevels'])) if coarse else list(range(len(r['zLevels'])));rr=[math.sqrt(r['xLevels'][j]**2+1) for j in xi];zz=[r['zLevels'][j] for j in zi]
 nodes=r['nodeIndices'];inner=[nodes[j][xi[0]] for j in zi];outer=[nodes[j][xi[-1]] for j in zi];top=[nodes[zi[0]][j] for j in xi];bottom=[nodes[zi[-1]][j] for j in xi]
 faces={}
 for name,ids,coords,sign in [('inner',inner,zz,-1.),('outer',outer,zz,1.),('top',top,rr,-1.),('bottom',bottom,rr,1.)]:
  values=[byid[i]['R']*byid[i]['Vr' if name in ['inner','outer'] else 'U'] for i in ids]
  faces[name]={'indices':ids,'integrand':values,'value':sign*trap(coords,values)}
 flux=[faces[k]['value'] for k in ['inner','outer','top','bottom']];defect=math.fsum(flux);scale=math.fsum(abs(v) for v in flux)
 return {'radialPositions':xi,'axialPositions':zi,'rCoordinates':rr,'zCoordinates':zz,'faces':faces,'defect':defect,'fluxScale':scale,'signedFraction':defect/scale if scale>0 else None,'absoluteFraction':abs(defect)/scale if scale>0 else None}
def projected(rows):return [{'index':o['index'],'X':o['X'],'Z':o['Z'],'R':math.sqrt(o['X']**2+1),'U':o['u'],'v':o['v'],'Vr':math.sqrt(o['X']**2+1)*o['v']/o['X']} for o in rows]
def controls():
 checks=[];q=[1.,1.2,1.6,2.1,2.5,3.];z=[12.,12.3,13.1,13.8,14.5,15.8]
 def fixture(side,source=False,zero=False,scale=1.):
  return [{'index':j*len(q)+i,'X':(-x if side=='left' else x),'Z':h,'u':0. if zero else scale*(2*h+3),'v':0. if source or zero else -scale*(-x if side=='left' else x)} for j,h in enumerate(z) for i,x in enumerate(q)]
 fields=[]
 for side in ['left','right']:
  rows=fixture(side);r=region(rows,side,BANDS[0]);assert not r['issues'];p={o['index']:o for o in projected(rows)};f=integrate(r,p);c=integrate(r,p,True);assert abs(f['defect'])<=2e-12 and abs(c['defect'])<=2e-12;fields.append(f)
 a2=q[0]**2+1;b2=q[-1]**2+1;dz=z[-1]-z[0]
 for f in fields:
  expected_faces={'inner':a2*dz,'outer':-b2*dz,'top':-(2*z[0]+3)*(b2-a2)/2,'bottom':(2*z[-1]+3)*(b2-a2)/2}
  assert all(abs(f['faces'][k]['value']-v)<=2e-12 for k,v in expected_faces.items())
 checks.append('both-side irregular-grid divergence-free faces and balance')
 assert all(abs(fields[0]['faces'][k]['value']-fields[1]['faces'][k]['value'])<=2e-12 for k in fields[0]['faces']);checks.append('reflected projection and orientation')
 rows=fixture('right',source=True);r=region(rows,'right',BANDS[0]);p={o['index']:o for o in projected(rows)};f=integrate(r,p);c=integrate(r,p,True);expected=(q[-1]**2-q[0]**2)*(z[-1]-z[0]);assert abs(f['defect']-expected)<=2e-12 and abs(c['defect']-expected)<=2e-12;checks.append('known nonzero volume source')
 mix=[dict(o,v=-.5*o['X']) for o in fixture('right',source=True)];fm=integrate(r,{o['index']:o for o in projected(mix)})
 rows3=[dict(o,u=3*o['u'],v=3*o['v']) for o in mix];f3=integrate(r,{o['index']:o for o in projected(rows3)});assert abs(f3['fluxScale']-3*fm['fluxScale'])<=2e-12 and abs(f3['absoluteFraction']-fm['absoluteFraction'])<=2e-12 and abs(f3['signedFraction']-fm['signedFraction'])<=2e-12 and all(abs(f3['faces'][k]['value']-3*fm['faces'][k]['value'])<=2e-12 for k in fm['faces']);checks.append('shared positive scale invariance')
 rowsneg=[dict(o,u=-o['u'],v=-o['v']) for o in mix];fn=integrate(r,{o['index']:o for o in projected(rowsneg)});assert abs(fn['fluxScale']-fm['fluxScale'])<=2e-12 and abs(fn['signedFraction']+fm['signedFraction'])<=2e-12 and abs(fn['absoluteFraction']-fm['absoluteFraction'])<=2e-12 and all(abs(fn['faces'][k]['value']+fm['faces'][k]['value'])<=2e-12 for k in fm['faces']);checks.append('negative common scale sign and magnitude')
 constant=[dict(o,u=3.,v=0.) for o in fixture('right')];fc=integrate(r,{o['index']:o for o in projected(constant)});assert fc['fluxScale']>0 and abs(fc['defect'])<=2e-12;checks.append('constant axial flow cancellation')
 rows=fixture('right',zero=True);f=integrate(r,{o['index']:o for o in projected(rows)});assert f['fluxScale']==0 and f['signedFraction'] is None and f['absoluteFraction'] is None;checks.append('zero integrated flux null fractions')
 assert coarse_ids(6)==[0,2,4,5] and coarse_ids(5)==[0,2,4];checks.append('fixed coarse endpoints')
 rows=fixture('right');assert 'incomplete-tensor-grid' in region(rows[1:],'right',BANDS[0])['issues'];checks.append('missing node rejected')
 assert 'duplicate-coordinate' in region(rows+[dict(rows[0],index=999)],'right',BANDS[0])['issues'];checks.append('duplicate node rejected')
 rows[0]['v']=None;assert 'nonfinite-selected-component' in region(rows,'right',BANDS[0])['issues'];checks.append('nonfinite component rejected')
 assert 'insufficient-axis-levels' in region(fixture('right')[:6],'right',BANDS[0])['issues'];checks.append('insufficient axes rejected')
 return {'passed':True,'checks':checks}
def same_tree(a,b):
 if type(a) is not type(b):return False
 if type(a) is float:return a.hex()==b.hex()
 if type(a) is dict:return set(a)==set(b) and all(same_tree(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same_tree(x,y) for x,y in zip(a,b))
 return type(a) in (str,int,bool,type(None)) and a==b
def main():
 start=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
 with (out/'launch.lock').open('x') as f:f.write('sole annular diagnostic\n')
 try:
  commit=guard();(out/'controls.json').write_text(json.dumps(controls(),indent=2)+'\n');docs={}
  for path,(size,sha) in PINS.items():
   raw=(ROOT/path).read_bytes();assert len(raw)==size and hashlib.sha256(raw).hexdigest()==sha;docs[path]=json.loads(raw)
  old=docs[INPUT];up=docs[UPSTREAM];assert old['status']=='completed-paired-support-diagnostic' and up['status']=='completed-descriptive-airflow-comparison'
  originals=old['originalCases'];rows=[c['original'] for c in originals];assert same_tree(rows,up['cases']) and len(rows)==3240 and len({o['index'] for o in rows})==3240 and up['counts']['accepted']==3240
  assert all(finite(o['X']) and finite(o['Z']) for o in rows)
  trace=selection(rows,up['counts']);(out/'selection.json').write_text(json.dumps(trace,indent=2,allow_nan=False)+'\n')
  result={'status':'completed-annular-balance' if trace['admission']['passed'] else 'admission-failed','sourceCommit':commit,'inputs':[{'path':p,'bytes':v[0],'sha256':v[1]} for p,v in PINS.items()],'originalCases':originals,'fullFieldSubsets':old['fullFieldSubsets'],'upstreamCounts':up['counts'],'selection':trace,'projectedNodes':[],'regions':[],'limits':LIMITS}
  if trace['admission']['passed']:
   chosen={i for r in trace['regions'] for i in r['selectedIndices']};pp=projected([o for o in rows if o['index'] in chosen]);result['projectedNodes']=pp;byid={p['index']:p for p in pp}
   for r in trace['regions']:
    full=integrate(r,byid);coarse=integrate(r,byid,True)
    result['regions'].append({'id':r['id'],'full':full,'coarse':coarse,'coarseMinusFull':{'defect':coarse['defect']-full['defect'],'signedFraction':coarse['signedFraction']-full['signedFraction'] if full['signedFraction'] is not None and coarse['signedFraction'] is not None else None}})
  else:
   result['regions']=[{'id':r['id'],'full':None,'coarse':None,'coarseMinusFull':None} for r in trace['regions']]
  assert len(result['regions'])==6 and len(result['projectedNodes'])<=3240
  body=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();assert len(body)<16*1024**2 and time.monotonic()-start<60;(out/'comparison.json').write_bytes(body)
  (out/'execution.json').write_text(json.dumps({'status':'complete','scientificStatus':result['status'],'elapsedSeconds':time.monotonic()-start,'resultBytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},indent=2)+'\n')
  print(json.dumps({'status':result['status'],'admission':trace['admission'],'selectedCount':trace['selectedCount'],'regions':[{'id':r['id'],'signedFraction':r['full']['signedFraction'] if r['full'] else None,'coarseMinusFull':r['coarseMinusFull']} for r in result['regions']]}))
 except BaseException as e:
  (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-start},indent=2)+'\n');raise
if __name__=='__main__':main()
