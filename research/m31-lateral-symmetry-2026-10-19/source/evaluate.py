"""One prospective paired-support diagnostic on saved values; no model evaluation."""
import hashlib,json,math,pathlib,time
BASE=pathlib.Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
INPUT='research/m31-crossstream-test-2026-10-19/results/comparison.json'
BYTES=2291932;SHA='1721ea55f3c475347ae73f5728f34db7fefea31b1e56b294a256bde2e606170a'
TOL=.01
LIMITS=['Previously exposed same-experiment paired-support diagnostic','Approximate mirror geometry; components are not exact field parity','No model fit, center shift, interpolation, field evaluation or component removal','No causal identification of swirl, drift, asymmetry or measurement error','No SI calibration, independent physical validation, force/swarm safety or novelty','Algebraic energy identity is not physical evidence']
def guard():
 raw=(BASE/'source-manifest.json').read_bytes();m=json.loads(raw);pub=json.loads((BASE/'source-publication.json').read_text());assert pub['manifestSha256']==hashlib.sha256(raw).hexdigest() and pub['remoteBytesEqualLocal'] and pub['committedBytesEqualLocal']
 for f in m['files']:
  b=(ROOT/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
 return pub['commit']
def match(rows):
 byid={r['original']['index']:r for r in rows};assert len(byid)==len(rows)
 groups={};adj={i:[] for i in byid};comparisons=0
 for r in rows:
  o=r['original']
  if r['included'] and o['X']!=0:groups.setdefault(float(o['Z']).hex(),[]).append(o['index'])
 for ids in groups.values():
  positives=[i for i in ids if byid[i]['original']['X']>0];negatives=[i for i in ids if byid[i]['original']['X']<0]
  for right in positives:
   for left in negatives:
    comparisons+=1;assert comparisons<=10497600
    if abs(byid[right]['original']['X']+byid[left]['original']['X'])<=TOL:adj[right].append(left);adj[left].append(right)
 for v in adj.values():v.sort()
 links=[]
 for right in sorted(byid):
  if byid[right]['original']['X']>0 and len(adj[right])==1:
   left=adj[right][0]
   if len(adj[left])==1:links.append((left,right))
 pid={i:j for j,pair in enumerate(links) for i in pair};assert len(pid)==2*len(links)
 table=[];counts={k:0 for k in ['prior-excluded','axis','no-eligible-counterpart','ambiguous-counterparts','counterpart-ambiguous','paired']}
 for r in rows:
  o=r['original'];i=o['index'];neighbors=adj[i]
  reason='prior-excluded' if not r['included'] else 'axis' if o['X']==0 else 'no-eligible-counterpart' if not neighbors else 'ambiguous-counterparts' if len(neighbors)>1 else 'counterpart-ambiguous' if len(adj[neighbors[0]])>1 else 'paired'
  assert (reason=='paired')==(i in pid);counts[reason]+=1
  table.append({'index':i,'reason':reason,'pairId':pid.get(i),'partnerIndex':neighbors[0] if reason=='paired' else None,'eligibleNeighbors':neighbors})
 return links,table,counts,comparisons

def component(vl,vr,pl,pr):
 oe=(vr+vl)/2;oo=(vr-vl)/2;pe=(pr+pl)/2;po=(pr-pl)/2;ee=pe-oe;eo=po-oo
 direct=(pr-vr)**2+(pl-vl)**2;even=2*ee*ee;odd=2*eo*eo;assert abs(direct-even-odd)<=2e-12
 return {'observedE':oe,'observedO':oo,'predictedE':pe,'predictedO':po,'errorE':ee,'errorO':eo,'directSSE':direct,'evenSSE':even,'oddSSE':odd}
def metric(pred,obs):
 n=len(obs)
 if not n:return None
 err=[p-v for p,v in zip(pred,obs)]
 return {'count':n,'mae':math.fsum(abs(e) for e in err)/n,'rmse':math.sqrt(math.fsum(e*e for e in err)/n),'bias':math.fsum(err)/n}
def summary(pairs,byid):
 if not pairs:return None
 n=len(pairs);rms={k:math.sqrt(math.fsum(p[k]**2 for p in pairs)/n) for k in ['observedE','observedO','predictedE','predictedO','errorE','errorO']}
 direct=math.fsum(p['directSSE'] for p in pairs);even=math.fsum(p['evenSSE'] for p in pairs);odd=math.fsum(p['oddSSE'] for p in pairs);assert abs(direct-even-odd)<=2e-12;total=even+odd
 sides={}
 for name,keys in [('left',['leftIndex']),('right',['rightIndex']),('joint',['leftIndex','rightIndex'])]:
  rs=[byid[p[key]] for p in pairs for key in keys];obs=[r['original']['v'] for r in rs];pred=[r['candidate'] for r in rs]
  sides[name]={'baseline':metric([0.]*len(rs),obs),'candidate':metric(pred,obs)}
 return {'rms':rms,'directSSE':direct,'evenSSE':even,'oddSSE':odd,'energyShareE':even/total if total>0 else None,'energyShareO':odd/total if total>0 else None,'pairedCandidateRMSE':math.sqrt(direct/(2*n)),'maxAbsXSum':max(p['absXSum'] for p in pairs),'sides':sides}
def in_region(z,name):return z>=12 if name=='primary' else z<12 if name=='near' else 12<=z<20 if name=='middle' else z>=20

def controls():
 checks=[]
 a=component(2,2,0,0);assert a['errorE']==-2 and a['errorO']==0;checks.append('pure same-direction component')
 a=component(-3,3,0,0);assert a['errorE']==0 and a['errorO']==-3;checks.append('pure opposite-direction component')
 a=component(0,0,1,3);assert a['errorE']==2 and a['errorO']==1 and a['directSSE']==10;checks.append('mixed residual identity')
 def row(i,x,z=15.,included=True,v=1.):return {'original':{'index':i,'X':x,'Z':z,'v':v},'included':included,'candidate':v}
 perfect={0:row(0,-1),1:row(1,1)};p={'leftIndex':0,'rightIndex':1,'absXSum':0.,**component(1.,1.,1.,1.)};s=summary([p],perfect);assert s['energyShareE'] is None and s['energyShareO'] is None and s['pairedCandidateRMSE']==0;checks.append('perfect agreement with null energy fractions')
 rows=[row(0,-1),row(1,1)];a=match(rows);assert a[0]==[(0,1)];rows[0]['original']['v']=-500;assert match(rows)==a;checks+=['exact mutual matching','response invariance']
 assert match([row(0,-1),row(1,1.0101)])[0]==[];checks.append('outside tolerance rejected')
 assert match([row(0,1),row(1,1.001)])[0]==[] and match([row(0,-1),row(1,1,16.)])[0]==[];checks.append('same sign and unequal Z rejected')
 a=match([row(0,-1),row(1,1),row(2,1.001)]);assert a[0]==[] and a[2]['ambiguous-counterparts']==1 and a[2]['counterpart-ambiguous']==2;checks.append('mutual ambiguity rejected')
 a=match([row(0,0),row(1,0,included=False)]);assert a[2]['axis']==1 and a[2]['prior-excluded']==1;checks.append('axis and prior exclusion precedence')
 assert summary([],{}) is None;checks.append('empty group null')
 return {'passed':True,'checks':checks}
def main():
 start=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
 with (out/'launch.lock').open('x') as f:f.write('sole lateral paired-support diagnostic\n')
 try:
  commit=guard();(out/'controls.json').write_text(json.dumps(controls(),indent=2)+'\n');raw=(ROOT/INPUT).read_bytes();assert len(raw)==BYTES and hashlib.sha256(raw).hexdigest()==SHA;old=json.loads(raw);assert old['status']=='completed-cross-component-diagnostic'
  rows=old['cases'];assert len(rows)==3240;byid={r['original']['index']:r for r in rows}
  for r in rows:
   assert all(math.isfinite(r['original'][k]) for k in ['X','Z'])
   if r['included']:assert math.isfinite(r['original']['v']) and math.isfinite(r['candidate'])
  links,matching,reasons,comparisons=match(rows);selection={}
  for name in ['primary','near','middle','far']:
   eligible=sum(r['included'] and in_region(r['original']['Z'],name) for r in rows);n=sum(in_region(byid[right]['original']['Z'],name) for left,right in links)
   selection[name]={'eligibleCells':eligible,'pairs':n,'pairedCells':2*n,'unmatchedCells':eligible-2*n,'coverage':2*n/eligible if eligible else None}
  (out/'selection.json').write_text(json.dumps({'matching':matching,'countsByReason':reasons,'groups':selection,'eligibilityComparisons':comparisons},indent=2)+'\n')
  primary=selection['primary'];assert primary['pairs']>=20 and primary['coverage']>=.9 and len({byid[r]['original']['Z'] for l,r in links if byid[r]['original']['Z']>=12})>=3,'insufficient prospective paired support'
  pairs=[]
  for j,(left,right) in enumerate(links):
   l=byid[left];r=byid[right];lo=l['original'];ro=r['original'];pairs.append({'pairId':j,'leftIndex':left,'rightIndex':right,'Xleft':lo['X'],'Xright':ro['X'],'Z':ro['Z'],'absXSum':abs(lo['X']+ro['X']),**component(lo['v'],ro['v'],l['candidate'],r['candidate'])})
  groups={name:{**selection[name],'summary':summary([p for p in pairs if in_region(p['Z'],name)],byid)} for name in selection}
  result={'status':'completed-paired-support-diagnostic','sourceCommit':commit,'inputPin':{'path':INPUT,'bytes':BYTES,'sha256':SHA},'inheritedGain':old['inheritedGain'],'originalCases':rows,'fullFieldSubsets':old['subsets'],'matching':matching,'countsByReason':reasons,'eligibilityComparisons':comparisons,'pairs':pairs,'groups':groups,'limits':LIMITS}
  data=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();assert len(data)<16*1024**2 and time.monotonic()-start<60;(out/'comparison.json').write_bytes(data)
  (out/'execution.json').write_text(json.dumps({'status':'complete','elapsedSeconds':time.monotonic()-start,'resultBytes':len(data),'sha256':hashlib.sha256(data).hexdigest()},indent=2)+'\n');print(json.dumps({'reasons':reasons,'groups':groups}))
 except BaseException as e:
  (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-start},indent=2)+'\n');raise
if __name__=='__main__':main()
