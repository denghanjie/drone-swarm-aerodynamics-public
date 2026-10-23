from common import *
import gzip,io,traceback
KEYS=['logicalPairs','componentSurvivors','componentRejected','guardRejected','radialRejected','centerEligible','rotorCalls','positiveRotorTerms','positiveVehicleEdges','supportedZeroRotorTerms','unsupportedNearFieldRotorTerms','invalidRotorTerms']
out=Output('producer','results');code=0
try:
 pub=gate();old=CFG['inputCheckpoint'];get=lambda rel:json.loads(committed(old+'/'+rel))
 audit=get('audit/audit.json');assert audit['passed'] and audit['selectedStages']==1920 and audit['exactReferenceEquivalence']
 closed=get('ALLOCATION-CLOSURE.json');assert closed['allClosed']
 idx=get('transport/index.json');ix=get('extract/index.json');assert idx['complete'] and len(idx['parts'])==6 and ix['selected']==1920
 original=idx['original'];assert original['sha256']==ix['selectedPin']['sha256'] and original['bytes']==ix['selectedPin']['bytes']
 h=hashlib.sha256();chunks=[];length=0
 for p in idx['parts']:
  out.tick();raw=committed(old+'/transport/'+p['file']);assert p['offset']==length and len(raw)==p['bytes'] and sha(raw)==p['sha256'];h.update(raw);length+=len(raw);chunks.append(raw)
 assert length==original['bytes'] and h.hexdigest()==original['sha256']
 view=get('audit/viewer-data.json');assert len(view['windows'])==12
 def group(rows):
  assert rows
  return {'stages':len(rows),'totals':{k:sum(r['counts'][k] for r in rows) for k in KEYS},'min':{k:min(r['counts'][k] for r in rows) for k in KEYS},'max':{k:max(r['counts'][k] for r in rows) for k in KEYS},'componentNonzeroStages':sum(r['counts']['componentRejected']>0 for r in rows),'radialNonzeroStages':sum(r['counts']['radialRejected']>0 for r in rows)}
 rows=[]
 with gzip.GzipFile(fileobj=io.BytesIO(b''.join(chunks))) as gz:
  while True:
   out.tick();line=gz.readline(8*1024**2+1)
   if not line:break
   assert len(line)<=8*1024**2 and len(rows)<1920
   rec=json.loads(line);w,i=divmod(len(rows),160);assert (rec['window'],rec['index'])==(w,i)
   b=rec['record']['body'];native=b['native'];d=native['diagnostics'];s=d['screen'];g=d['geometryWork'];n=64
   assert native['schema']=='m31-native-load-evidence-v1' and native['method']=='F'
   assert native['status'] in ('native-success','domain-refused') and s['eligible'] is True
   assert s['componentThreshold']==4 and number(native['constants']['neighbor'])==3
   inp=b['nativeInput']['drones'];ids=[integer(x['id']) for x in inp];assert len(ids)==64 and ids==sorted(set(ids)) and ids==native['ids']
   positions=[[number(v) for v in x['state'][:3]] for x in inp];assert all(len(x['state'])==17 for x in inp)
   for j,p in enumerate(native['prepared']):assert p['id']==ids[j] and p['center']==inp[j]['state'][:3]
   assert len(native['prepared'])==64
   oldw=view['windows'][w];frame=oldw['frames'][i];assert oldw['window']==w and oldw['caseId']==rec['caseId'] and oldw['start']+i==rec['globalOrdinal']
   assert frame['index']==i and frame['globalOrdinal']==rec['globalOrdinal'] and frame['timeWord']==b['originalTimeWord'] and word(frame['time'])==b['originalTimeWord']
   assert frame['status']==native['status'] and frame['reason']==native['reason']
   assert [[word(v) for v in p] for p in frame['positions']]==[x['state'][:3] for x in inp]
   P=integer(g['logicalDirectedPairs']);N=integer(s['actualCenterNormCalls']);G=integer(g['centerGuardRejectedPairs']);E=integer(g['centerEligiblePairs']);R=integer(g['pairCalls']);T=integer(g['positiveRotorTerms']);U=integer(d['graph']['uniqueVehicleEdges']);symbols=[integer(v) for v in d['symbolCounts']]
   assert P==n*(n-1) and N==integer(g['directedCenterTests']) and 0<=N<=P
   C=P-N;D=N-G-E;assert D>=0 and C==integer(g['certifiedSkippedPairs'])==integer(s['skippedCenterNormCalls']) and R==4*E
   assert len(symbols)==12 and symbols[0]==symbols[10]==0 and sum(symbols)==4*n*n
   assert symbols[1]+R+4*G==4*n*n
   invalid=symbols[11]-4*G;zeros=sum(symbols[k] for k in (2,3,5,6,7,9));assert invalid>=0 and T==symbols[8] and R==T+zeros+symbols[4]+invalid
   co=native['coefficients'];offsets=[integer(x) for x in co['offsets']];src=[integer(x) for x in co['sourceIndices']]
   assert len(offsets)==4*n+1 and offsets[0]==0 and offsets[-1]==T and offsets==sorted(offsets) and len(src)==len(co['K'])==T
   assert all(number(k)>0 for k in co['K'])
   unionCount=0
   for j in range(n):
    union=set()
    for rotor in range(4):
     at=4*j+rotor;row=src[offsets[at]:offsets[at+1]];assert row==sorted(set(row)) and all(0<=v<n and v!=j for v in row);union.update(row)
    unionCount+=len(union)
   assert U==unionCount and 0<=U<=E and U<=T<=4*U
   reasons=d['admission']['reasons'];assert isinstance(reasons,list) and all(isinstance(v,str) for v in reasons)
   if native['status']=='native-success':assert d['admission']['admitted'] is True and not reasons
   else:assert (w,i)==(2,159) and native['reason']=='native-admission' and d['admission']['admitted'] is False and 'near-field' in reasons
   counts=dict(zip(KEYS,[P,N,C,G,D,E,R,T,U,zeros,symbols[4],invalid]))
   row={'window':w,'index':i,'caseId':rec['caseId'],'globalOrdinal':rec['globalOrdinal'],'sourceLineSha256':rec['sourceLineSha256'],'selectedRecordSha256':sha(line),'timeWord':b['originalTimeWord'],'time':number(b['originalTimeWord']),'status':native['status'],'reason':native['reason'],'nativeStage':native.get('stage'),'admissionReasons':reasons,'ids':ids,'positions':positions,'counts':counts,'symbols':symbols}
   rows.append(row);out.save('stages.jsonl',row,True)
 assert len(rows)==1920
 windows=[]
 for w in range(12):windows.append(dict(group(rows[w*160:(w+1)*160]),window=w,caseId=view['windows'][w]['caseId'],start=view['windows'][w]['start']))
 refusals=[{k:r[k] for k in ('window','index','caseId','globalOrdinal','timeWord','status','reason','nativeStage','admissionReasons')} for r in rows if r['status']!='native-success'];assert len(refusals)==1
 overall=group(rows);component=overall['totals']['componentRejected']>0;radial=overall['totals']['radialRejected']>0
 summary={'schema':'m31-neighbor-density-summary-v1','stages':1920,'nativeCalls':0,'countsKeys':KEYS,'overall':overall,'windows':windows,'byStatus':{s:group([r for r in rows if r['status']==s]) for s in ('native-success','domain-refused')},'refusals':refusals,'decision':{'componentOpportunityExists':component,'radialOpportunityExists':radial,'bufferWidthTuningForTheseClips':'unresolved' if component else 'retire','radialFollowup':'consider-separate-proof' if radial else 'no-distance-headroom-observed'},'scope':'saved exposed N64 builder counts; no timing or physical inference'}
 out.save('summary.json',summary)
 out.save('input-binding.json',{'sourceCommit':pub['commit'],'sourceManifestSha256':pub['manifestSha256'],'original':original,'consumedPins':[PINS[p] for p in sorted(CACHE)],'readEvents':EVENTS})
except Exception as e:
 code=1;out.failed=True;out.save('failure.json',{'type':type(e).__name__,'message':str(e).replace(str(ROOT),'[repository]')[:1000],'trace':traceback.format_exc().replace(str(ROOT),'[repository]')[-2500:],'readEvents':EVENTS})
finally:out.close(code)
sys.exit(code)
