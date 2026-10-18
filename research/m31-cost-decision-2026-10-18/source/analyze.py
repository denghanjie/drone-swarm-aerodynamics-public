"""Independent saved-byte/timing analysis; no scientific producer imports."""
from pathlib import Path
import hashlib,json,statistics,time,math
P=Path(__file__).resolve().parents[1];R=P/'results';start=time.monotonic()
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def stats(v):return {'medianMs':statistics.median(v),'minMs':min(v),'maxMs':max(v),'p25Ms':statistics.quantiles(v,n=4,method='inclusive')[0],'p75Ms':statistics.quantiles(v,n=4,method='inclusive')[2]}
def main():
 (P/'analysis.lock').open('x').close()
 root=P.parents[1];manifest=load(P/'source-manifest.json');publication=load(P/'source-publication.json')
 need(sha((P/'source-manifest.json').read_bytes())==publication['manifestSha256'] and publication['remoteBytesEqualLocal'],'published-manifest')
 for pin in manifest['files']:
  b=(root/pin['path']).read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'postrun-source-pin')
 expected=(P/'expected.json').read_bytes().strip();expectedHash=sha(expected)
 need(len(list(R.glob('query-*.json')))==116 and len(list(R.glob('transfer-*.json')))==116 and not (R/'failure.json').exists(),'row-inventory')
 need(load(R/'supervisor.json')['exitCode']==0 and load(R/'supervisor.json')['reason']is None,'supervisor')
 need(load(R/'browser-summary.json')['complete'] and load(R/'browser-summary.json')['calls']==116,'browser')
 need(load(R/'browser-exit.json')['rootExit']=={'code':0,'signal':None} and load(R/'browser-exit.json')['rootClose']=={'code':0,'signal':None},'browser-root-exit')
 need(load(R/'browser-exit.json')['completed'] and load(R/'browser-exit.json')['contextClosed'],'closed')
 orders=[['F','H','H0','HC'],['H','HC','F','H0'],['HC','H0','H','F'],['H0','F','HC','H']]
 rows=[]
 for call in range(1,117):
  need(time.monotonic()-start<30,'analysis-deadline');r=load(R/f'query-{call:03d}.json');p=r['semanticPin'];actual=(R/p['path']).read_bytes()
  need(len(actual)==p['bytes'] and sha(actual)==p['sha256']==expectedHash and actual==expected,'actual-semantic-bytes')
  need(r['call']==call and r['inputUnchanged'] and r['semanticEqual'] and r['hostEqual'] and r['status']=='native-success','correctness')
  need(type(r['queryMs'])in(int,float) and 0<r['queryMs']<180000,'time')
  if call<=112:
   block=(call-1)//4;pos=(call-1)%4
   need(r['kind']==('warm'if block<4 else'measured')and r['block']==(block if block<4 else block-4)and r['position']==pos and r['arm']==orders[block%4][pos],'schedule')
  else:need(r['kind']=='diagnostic' and r['block']==0 and r['position']==call-113 and r['arm']==['F','H','HC','H0'][call-113],'diagnostic-schedule')
  r['transfer']=load(R/f'transfer-{call:03d}.json')
  need(r['transfer']['call']==call,'transfer-binding')
  values=[r['nativeMs'],r['encodeMs'],r['compareMs'],r['transfer']['transferAndPersistMs'],r['transfer']['persistMs'],*r['phases'].values(),*r['buildPhases'].values()]
  need(all(type(v)in(int,float) and math.isfinite(v)and v>=0 for v in values),'finite-phase-times')
  rows.append(r)
 measured=[r for r in rows if r['kind']=='measured'];pairs=[]
 for block in range(24):
  arms={r['arm']:r for r in measured if r['block']==block};f=arms['F']['queryMs'];h=arms['H']['queryMs']
  pairs.append({'block':block,'order':orders[block%4],'Fms':f,'Hms':h,'HtoF':h/f,'HCtoH':arms['HC']['queryMs']/h,'H0toF':arms['H0']['queryMs']/f,'win':h<f})
 ratio=statistics.median(p['HtoF']for p in pairs);wins=sum(p['win']for p in pairs);keep=ratio<=.9 and wins>=20
 arms={}
 for arm in ['F','H','HC','H0']:
  rs=[r for r in measured if r['arm']==arm]
  arms[arm]={**stats([r['queryMs']for r in rs]),'native':stats([r['nativeMs']for r in rs]),'phaseMedianMs':{k:statistics.median(r['phases'][k]for r in rs)for k in rs[0]['phases']},'encodeMedianMs':statistics.median(r['encodeMs']for r in rs),'compareMedianMs':statistics.median(r['compareMs']for r in rs),'transferIncludingPersistenceMedianMs':statistics.median(r['transfer']['transferAndPersistMs']for r in rs),'persistenceMedianMs':statistics.median(r['transfer']['persistMs']for r in rs),'positionMedianMs':{str(i):statistics.median(r['queryMs']for r in rs if r['position']==i)for i in range(4)}}
 result={'complete':True,'correctnessPassed':True,'queriesChecked':116,'measuredQueries':96,'expectedSemanticSha256':expectedHash,'medianPairedHtoF':ratio,'strictWins':wins,'pairs':pairs,'arms':arms,'keepGatePassed':keep,'verdict':'keep-for-further-study'if keep else'no-worthwhile-speed-improvement-demonstrated','medianPairedCaptureRatio':statistics.median(p['HCtoH']for p in pairs),'medianPairedH0toF':statistics.median(p['H0toF']for p in pairs),'diagnostics':[r for r in rows if r['kind']=='diagnostic'],'scope':'One saved projected N1000 state, one browser process, warmed repeated queries. No general speedup, sustained flight, physical validation or novelty. The baseline F already uses component screening.','analysisWallSeconds':time.monotonic()-start}
 with (R/'analysis.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({k:result[k]for k in ['complete','queriesChecked','medianPairedHtoF','strictWins','keepGatePassed','medianPairedCaptureRatio']}))
if __name__=='__main__':main()
