"""One prospective observation pass over frozen saved records; no model execution."""
import json,struct,math,time
import common as C
B=C.BASE;R=C.ROOT
FIELDS=['z','vz','desiredVz','targetZ','requestRaw','requestedNetAcceleration','commandTotal','nominalTotal','nativeAxisZ','nominalFz','deliveredFz','forceShortfall','nominalWeightRatio','deliveredWeightRatio','deliveredNetAcceleration']
SIGNS=['desiredUp','movingDown','requestUp','acceleratingDown','desiredUpWhileMovingDown','requestUpWhileAcceleratingDown']
def num(w):
 assert isinstance(w,str) and len(w)==16
 x=struct.unpack('>d',bytes.fromhex(w))[0];assert math.isfinite(x);return x

def word(x):return struct.pack('>d',x).hex()
def total(ws):
 s=0.
 for w in ws:s+=num(w)
 return s

def metric(c,s,p,l):
 state=list(map(num,c['stateWords']));desired=num(c['desiredVelocityWords'][2]);target=num(c['target']['zWord'])
 assert word(state[2]+(2.5*desired+1.5*state[5])/6)==c['target']['zWord']
 raw=6*(target-state[2])-4*state[5];req=max(-4,min(5,raw));nom=total(p['forces']);axis=num(p['axis'][2]);fz=num(l['worldForce'][2]);acc=fz/.027-9.81
 assert word(acc)==s['derivativeWords'][5]
 assert p['forces']==s['nominalMotorWords'] and s['consumed']['worldForceWords']==l['worldForce']
 m=dict(zip(FIELDS,[state[2],state[5],desired,target,raw,req,total(c['commandsWords']),nom,axis,axis*nom,fz,axis*nom-fz,(axis*nom)/(.027*9.81),fz/(.027*9.81),acc]))
 assert all(math.isfinite(x) for x in m.values());return m

def signs(m):
 d=m['desiredVz']>0;v=m['vz']<0;r=m['requestedNetAcceleration']>0;a=m['deliveredNetAcceleration']<0
 return dict(zip(SIGNS,[d,v,r,a,d and v,r and a]))

def main():
 assert (B/'extract-supervisor-launch.lock').exists()
 pub=C.gate();cfg=C.load(B/'inputs.json');out=B/'results';out.mkdir();C.write(out/'launch.json',{'sourceCommit':pub['commit'],'zeroModelCalls':True})
 receipts=[];allrows=[];summaries={};priorEnds={};boundaries=[];traceBytes=0
 with (out/'trace.jsonl').open('xb') as f:
  for stream in cfg['streams']:
   idx=C.load(R/stream['index']);entry=next(c for c in idx['cases'] if c['caseId']==stream['caseId']);key=stream['caseId'];receipt={};pending=None;n=0;end=None;lastStep=None
   for obj,provenance in C.records(stream,receipt):
    kind=obj['kind'];body=obj['body']
    if kind=='initial':
     if stream['phase']=='continuation':assert body['input']==priorEnds[key];boundaries.append(key)
    if kind=='controller':
     assert pending is None;pending=(body,provenance);continue
    if pending is not None:
     cb,cp=pending;assert kind=='stage' and body['stageIndex']==1 and body['status']=='completed'
     assert cb['stepIndex']==body['stepIndex'] and cb['originalTimeWord']==body['originalTimeWord'] and cb['relativeTimeWord']==body['relativeTimeWord']
     choose=lambda rows:next(x for x in rows if x['id']==17)
     c=choose(cb['records']);s=choose(body['records']);p=choose(body['native']['prepared']);l=choose(body['native']['loads'])
     assert c['stateWords']==s['rawStateWords'] and c['commandsWords']==s['commandsWords'];assert body['native']['status']=='native-success'
     row={'phase':stream['phase'],'caseId':key,'id':17,'controllerProvenance':cp,'stageProvenance':provenance,'clock':{k:body[k] for k in ['stepIndex','stageIndex','relativeTimeWord','originalTimeWord','dtWord']},'controller':c,'stage':s,'prepared':p,'load':l,'metrics':metric(c,s,p,l)}
     b=(json.dumps(row,separators=(',',':'),allow_nan=False)+'\n').encode();traceBytes+=len(b);assert traceBytes<28*1024*1024;f.write(b);allrows.append(row);n+=1;pending=None
    if kind=='step':lastStep=body
    if kind=='case-end':end=body
   assert n==stream['expectedSamples'] and pending is None and end is not None
   assert end=={k:v for k,v in entry.items() if k!='journal'}
   receipts.append(receipt)
   if stream['phase']=='original':priorEnds[key]=end['finalInput']
   else:
    rows=[x for x in allrows if x['caseId']==key];summaries[key]={'samples':len(rows),'first':rows[0]['metrics'],'last':rows[-1]['metrics'],'firstTime':num(rows[0]['clock']['originalTimeWord']),'lastTime':num(rows[-1]['clock']['originalTimeWord']),'ranges':{k:[min(x['metrics'][k] for x in rows),max(x['metrics'][k] for x in rows)] for k in FIELDS},'counts':{k:sum(signs(x['metrics'])[k] for x in rows) for k in SIGNS},'firstMatches':{k:next(({'time':num(x['clock']['originalTimeWord']),'phase':x['phase'],'controllerSequence':x['controllerProvenance']['sequence']} for x in rows if signs(x['metrics'])[k]),None) for k in SIGNS},'endpoint':{'timeWord':lastStep['originalTimeWord'],'stateWords':next(x['state'] for x in end['finalInput']['drones'] if x['id']==17),'status':end['status'],'reason':end['reason']}}
 assert len(allrows)==1924 and len(boundaries)==4
 view={'physicalValidity':False,'focusId':17,'cases':[{'caseId':key,'summary':s,'samples':[{'time':num(x['clock']['originalTimeWord']),'phase':x['phase'],'controllerSequence':x['controllerProvenance']['sequence'],'values':x['metrics']} for x in allrows if x['caseId']==key]} for key,s in summaries.items()]}
 viewPin=C.write(out/'view-data.json',view);C.gate()
 tracePin={'file':'results/trace.jsonl','bytes':traceBytes,'sha256':C.sha((out/'trace.jsonl').read_bytes())}
 C.write(out/'report.json',{'passed':True,'zeroModelCalls':True,'samples':len(allrows),'boundaries':boundaries,'journalReceipts':receipts,'summaries':summaries,'tracePin':tracePin,'viewPin':viewPin,'readEvents':C.EVENTS})
 assert sum(p.stat().st_size for p in out.iterdir())<32*1024*1024

if __name__=='__main__':
 try:main()
 except Exception as e:
  (B/'results').mkdir(exist_ok=True);C.write(B/'results/failure.json',{'error':str(e).replace(str(R),'[repository]'),'type':type(e).__name__,'readEvents':C.EVENTS});raise
