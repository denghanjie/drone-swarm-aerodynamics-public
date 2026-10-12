"""Stream complete raw evidence into inspectable case summaries and worst cases."""
from pathlib import Path
import gzip, json, hashlib
root=Path(__file__).resolve().parent.parent
raw=root/'results/accuracy-raw.jsonl.gz'
cases={}
with gzip.open(raw,'rt') as f:
    for line in f:
        item=json.loads(line)
        if 'failure' in item: raise RuntimeError('Unexpected failure in full accuracy evidence')
        c=item['config']; key=(c['seed'],c['count'],c['family'],item['epsilon'])
        out=cases.setdefault(key,{'config':{**c,'epsilon':item['epsilon']},'snapshots':0,'receivers':0,'omittedPairs':0,'maxReferenceError':0,'maxInflowError':0,'maxForceError':0,'maxMomentError':0,'worstForce':None,'worstMoment':None})
        out['config'].pop('t',None);out['snapshots']+=1;out['omittedPairs']+=item['counters']['omittedPairs'];out['maxReferenceError']=max(out['maxReferenceError'],item['referenceError'])
        for row in item['rows']:
            out['receivers']+=1;out['maxInflowError']=max(out['maxInflowError'],*row['inflowError'])
            for name,field in [('Force','forceError'),('Moment','momentError')]:
                if row[field]>out['max'+name+'Error'] or out['worst'+name] is None:
                    out['max'+name+'Error']=row[field];out['worst'+name]={'t':c['t'],**row}
hash=hashlib.sha256()
with raw.open('rb') as f:
    for block in iter(lambda:f.read(1024*1024),b''):hash.update(block)
report={'scope':'All 144 seed/count/family/budget cases, streamed from the complete raw evidence; each retains its force and moment worst case','rawEvidence':{'file':raw.name,'bytes':raw.stat().st_size,'sha256':hash.hexdigest(),'publicGitInclusion':False,'reason':'Full raw per-rotor evidence is retained separately because it exceeds the single-file Git hosting limit.','reproduction':'node src/experiment.cjs accuracy','encoding':'Concatenated gzip members containing one JSONL record per snapshot and budget'},'cases':list(cases.values())}
(root/'results/accuracy-cases.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'rawBytes':raw.stat().st_size,'rawSha256':hash.hexdigest()}))
