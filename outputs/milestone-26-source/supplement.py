from pathlib import Path
import json,math,datetime
root=Path(__file__).resolve().parent.parent;src=root/'milestone-26-source';protocol=json.loads((root/'milestone-26-protocol.json').read_text());rows=[]
for j in protocol['jobs']:
 if j['kind']=='primary':continue
 coarse=next(x for x in protocol['jobs'] if x['kind']=='primary' and x['seed']==j['seed'] and x['count']==j['count'] and x['course']==j['course']);files=[src/(x['id']+'.json') for x in (coarse,j)]
 if not all(x.exists() for x in files):continue
 a,b=[json.loads(x.read_text()) for x in files]
 if j['kind']=='window-refinement' and not (a['metrics']['end']<20 and b['metrics']['end']<20):continue
 error=max(math.dist(x[:3],y[:3]) for x,y in zip(a['final'],b['final']));ends=[a['metrics']['end'],b['metrics']['end']];stops=[a['metrics']['stopReason'],b['metrics']['stopReason']]
 def identity(r):
  f=r['metrics']['failure'] or {};return {'drone':f.get('drone'),'pair':f.get('pair'),'obstacles':[h['id'] for h in f.get('hits',[])]}
 event=identity(a)==identity(b);passed=error<.01 and abs(ends[0]-ends[1])<.01 and stops[0]==stops[1] and a['metrics']['passed']==b['metrics']['passed']
 rows.append({'coarse':coarse['id'],'fine':j['id'],'scope':'supplemental early-stop description; original missing20s checkpoint result retained' if j['kind']=='window-refinement' else 'available prescribed full-mission comparison','maximumEndpointDifferenceM':error,'endTimes':ends,'stopReasons':stops,'eventIdentities':[identity(a),identity(b)],'eventIdentityAgreement':event,'jointThresholdsMet':passed,'note':'Endpoints at different stop times are not time-synchronized paths. No claim about later motion or physical accuracy.'})
(root/'milestone-26-available-comparisons.json').write_text(json.dumps({'generated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'studyComplete':(root/'milestone-26-summary.json').exists(),'comparisons':rows},indent=2));print([(x['fine'],x['maximumEndpointDifferenceM'],x['jointThresholdsMet']) for x in rows])
