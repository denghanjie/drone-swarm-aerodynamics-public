"""Saved-word display projection only; no scientific calculation or checker entry."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys,time
PACKAGE='research/m31-native-tree-state1000-2026-10-17'
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];START=time.monotonic();END=START+55
CUTOFF=datetime.datetime.fromisoformat('2026-10-17T07:15:28+00:00')
def need(ok,message):
    if not ok:raise ValueError(message)
def guard(ctx):need(time.monotonic()<END and datetime.datetime.now(datetime.timezone.utc)<CUTOFF,'display-deadline')
def fields(value,names,message):need(type(value)is dict and set(value)==set(names),message)
def integer(value,low,high,message):
    need(type(value)is int and low<=value<=high,message);return value
def decode(raw):return json.loads(raw)
def identity(p):
    raw=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def read_pin(root,pin):
    guard(None);p=root/pin['path'];need(p.resolve()==p and p.is_file() and p.stat().st_size<=32*1048576,'file-location-size');need(identity(p)==pin,'file-identity');return p.read_bytes()
def write(path,value):
    guard(None);raw=(json.dumps(value,separators=(',',':'),allow_nan=False)+'\n').encode();need(len(raw)<=8*1048576,'display-file-cap')
    need(sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file())+len(raw)<=16*1048576,'display-total-cap')
    with path.open('xb') as f:f.write(raw)
    return {'path':str(path.relative_to(HERE)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def inventory():
    manifest=decode((ROOT/PACKAGE/'source-manifest.json').read_bytes());paths={p['path'] for p in manifest['files']}
    paths.update(str(p.relative_to(ROOT)) for p in (ROOT/PACKAGE/'results').rglob('*') if p.is_file())
    paths.update(PACKAGE+'/'+x for x in ['source-manifest.json','source-publication.json','EXTERNAL-EXIT.json'])
    return [identity(ROOT/p) for p in sorted(paths)]
def members(value,n):
    need(type(value)is dict and set(value)=={'kind','count','data'},'membership-schema')
    if value['kind']=='literal':actual=value['data']
    elif value['kind']=='runs':
        v=value['data'];need(len(v)%2==0,'runs-even');actual=[j for start,length in zip(v[::2],v[1::2]) for j in range(start,start+length)]
    else:
        need(value['kind']=='bitmap' and len(value['data'])==(n+63)//64,'bitmap-width');actual=[]
        for wi,word in enumerate(value['data']):
            need(type(word)is str and len(word)==16,'bitmap-word');bits=int(word,16)
            actual.extend(wi*64+bit for bit in range(64) if (bits>>bit)&1)
    need(actual==sorted(set(actual)) and len(actual)==value['count'] and all(type(i)is int and 0<=i<n for i in actual),'membership-values');return actual

def main():
    before=inventory();write(HERE/'immutable-before.json',before);p=ROOT/PACKAGE;results=p/'results'
    attempt=decode((results/'run-attempt.json').read_bytes());check=decode((results/'check.json').read_bytes());external=decode((p/'EXTERNAL-EXIT.json').read_bytes())
    need(attempt['status']=='completed' and check['complete'] is True and check['passed'] is True and check['conditionalNativeQualified'] is True,'closed-qualified-attempt')
    need(check['sourceCommit']==attempt['sourceCommit']==external['sourceCommit'] and check['sourceManifestSha256']==attempt['sourceManifestSha256']==external['sourceManifestSha256'],'result-source-binding')
    need(external['exitCode']==0 and external['attemptSha256']==identity(results/'run-attempt.json')['sha256'],'external-exit-binding')
    need(not check['highPrecisionAccuracyValidated'] and not check['controllerFullyRecomputed'] and not check['rkEndpointValidated'],'narrow-scope')
    manifest=decode((p/'source-manifest.json').read_bytes());decoder=next(x for x in manifest['files'] if x['path']=='research/m31-native-tree-browser-probe-2026-10-17/source/compact-check.py');read_pin(ROOT,decoder)
    spec=importlib.util.spec_from_file_location('_saved_display_reader',ROOT/decoder['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);reader=module.Resolver(sys.modules[__name__],{'root':ROOT})
    need(len(check['stages'])==1,'single-stage');metric=check['stages'][0];stage=reader.record(metric['stagePin']);native=reader.record(metric['nativePins']['H']);tree=native['tree'];base=tree['base'];rows=stage['records'];n=len(rows)
    need(n==1000 and metric['n']==1000 and tree['schema']=='m31-tree-witness-columns-v1' and base['complete'] and base['eligible'],'complete-N1000')
    need(any(x['method']=='H' and x['recordPin']==metric['nativePins']['H'] for x in stage['nativeRefs']),'stage-H-binding')
    receivers=[]
    for i in [0,250,500,750,999]:
        need(tree['receiverIds'][i]==i,'receiver-id');codes=tree['cullCodes'][tree['cullOffsets'][i]:tree['cullOffsets'][i+1]];boxes=[]
        for code in codes:
            node=code//6;need(type(code)is int and 0<=node<len(base['nodes']),'box-node');b=base['nodes'][node];boxes.append({'node':node,'min':b['min'],'max':b['max']})
        receivers.append({'index':i,'id':rows[i]['id'],'gathered':members(tree['gathered'][i],n),'boxes':boxes})
    timings={t['method']:t['queryWallMs'] for t in metric['queryTimings']}
    data={'schema':'m31-tree-probe-display-v1','caseId':metric['caseId'],'n':n,'sourceCommit':attempt['sourceCommit'],'validated':True,'validationScope':'conditional native equivalence, complete omission certificates and derivative wiring; no fresh high-precision, full-controller, trajectory or physical validation','frames':[{'id':'query','label':'Actual projected state · t=0 · no flight advancement','drones':[{'id':r['id'],'pose':r['stateWords'][:3]+r['stateWords'][6:10]} for r in rows]}],'receivers':receivers,'metrics':{'querySumsMs':timings,'HtoFRatio':timings['H']/timings['F'],'omittedPairs':metric['work']['H']['omitted'],'fullPairs':metric['work']['F']['pairs'],'derivativeWords':check['primaryCounts']['derivativeWords']},'provenance':{'attempt':identity(results/'run-attempt.json'),'check':identity(results/'check.json'),'firstStage':metric['stagePin'],'firstH':metric['nativePins']['H'],'externalExit':identity(p/'EXTERNAL-EXIT.json')}}
    (HERE/'data').mkdir(exist_ok=False);data_pin=write(HERE/'data'/('tree-t0-n1000-a.json'),data)
    write(HERE/'record-pins.json',{'schema':'m31-tree-probe-display-pins-v1','headline':'1,000-drone state passed the planned numerical checks.','detail':'All three methods agree; every receiver omission and all17,000primary derivative values were checked. One instant only. No physical-validity or speedup claim.','checkAvailable':True,'cases':[dict(data_pin,caseId=metric['caseId'])]})
    reader.verify_preserved();after=inventory();need(before==after,'source-result-preservation');write(HERE/'immutable-after.json',after)
    write(HERE/'EXPORT-RECEIPT.json',{'scientificCalls':0,'sourceCommit':attempt['sourceCommit'],'decoder':decoder,'exporter':identity(Path(__file__)),'attempt':identity(results/'run-attempt.json'),'check':identity(results/'check.json'),'cases':1,'frames':1,'receivers':5,'displayedDrones':1000,'readPins':list(reader.seen.values()),'preservationPassed':True,'wallSeconds':time.monotonic()-START,'scope':'Saved data projection only; scientific qualification inherited from frozen check result.'})
    print(json.dumps({'cases':1,'frames':1,'receivers':5,'drones':1000,'scientificCalls':0,'preservationPassed':True}))
if __name__=='__main__':main()
