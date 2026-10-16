"""Presentation only: derive display values from closed saved records, without science."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent.parent

def read(name,default=None):
    f=p/name
    return json.loads(f.read_text()) if f.exists() else default

def pin(name):
    b=(p/name).read_bytes()
    return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

names=dict(generationRun='results/generation-run.json',run='results/candidate-run.json',reviewRun='results/review-run.json',review='results/independent-review.json',analysis='results/analysis.json',qualification='results/qualification.json',sourcePublication='source-publication.json',configuration='config.json',sourceManifest='source-manifest.json')
records={k:read(v) for k,v in names.items() if (p/v).exists()}
for s in ['p0','p1','p2']:
    for k,f in [(s+'Closure',f'runs/{s}/closure.json'),(s+'Evidence',f'runs/{s}/results/evidence.json')]:
        if not (p/f).exists() and k.endswith('Evidence'):f=f'runs/{s}/results/partial-evidence.json'
        if (p/f).exists():names[k]=f;records[k]=read(f)
seal=records.get('qualification',{});analysis=records.get('analysis',{});audit=records.get('review',{})
closed=all(records.get(k,{}).get('supervisorSuccess') is True and records[k].get('closed') is True and records[k].get('childGroupAbsent') is True for k in ['generationRun','run','reviewRun'])
slots=all(records.get(s+'Closure',{}).get('complete') is True and records[s+'Closure'].get('closureConfirmed') is True for s in ['p0','p1','p2'])
verified=bool(closed and slots and audit.get('pass') is True and audit.get('complete') is True and analysis.get('independentAuditPass') is True and seal.get('sealSuccess') is True and seal.get('evidenceQualified') is True)
passed=verified and seal.get('practicalRulePass') is True
artifacts={}
def same_pin(a,b):
    return a['bytes']==b['bytes'] and a['sha256']==b['sha256']
def require_artifact(actual):
    if verified and (actual['path'] not in artifacts or not same_pin(actual,artifacts[actual['path']])):
        raise ValueError('display record is not in the sealed scientific inventory: '+actual['path'])
if verified:
    for key,name in names.items():
        if name in seal['inputs'] and not same_pin(pin(name),seal['inputs'][name]):
            raise ValueError('display record differs from seal input: '+name)
    required=['generationRun','run','reviewRun','review','analysis','sourcePublication','sourceManifest','p0Closure','p1Closure','p2Closure']
    if any(names[k] not in seal['inputs'] for k in required):raise ValueError('missing seal input binding')
    inventory=records['reviewRun']['artifacts']
    if len({x['path'] for x in inventory})!=len(inventory):raise ValueError('duplicate sealed inventory entry')
    artifacts={x['path']:x for x in inventory}
    for key in ['p0Evidence','p1Evidence','p2Evidence']:require_artifact(pin(names[key]))
    config_name='research/'+p.name+'/config.json'
    config_pin=next(x for x in records['sourceManifest']['files'] if x['path']==config_name)
    if not same_pin(pin('config.json'),config_pin):raise ValueError('configuration differs from frozen source manifest')
    if [x['processId'] for x in analysis['processes']]!=['p0','p1','p2']:raise ValueError('missing or duplicate analysis process')
cases=[]
for c in records['configuration']['cases']:
    name='generation/'+c['id']+'.json';g=read(name)
    if not g or not g.get('poses'):
        if verified:raise ValueError('qualified generation record missing')
        continue
    require_artifact(pin(name));require_artifact(g['poses'])
    if not same_pin(pin(g['poses']['path']),g['poses']):raise ValueError('pose bytes differ from generation record')
    item=dict(**c,frames=g['poses']['frames'],poses=g['poses'],generationPin=pin(name),processes=[],description='Five-second local 3D Boids flight with airflow off. The final pose supplies a separate aerodynamic load query. This short trajectory does not test mature flock behavior or long-flight success.')
    if verified:
        load=f"runs/p0/results/{c['id']}-L.json";q=read(load)
        if q['id']!=c['id'] or q['n']!=c['n'] or q['label']!='L' or len(q['solutions']['O']['y'])!=c['n']:raise ValueError('qualified load identity mismatch')
        require_artifact(pin(load))
        item.update(y=q['solutions']['O']['y'],loadPin=pin(load),loadProcess='p0')
        for process in analysis['processes']:
            a=next(x for x in process['cases'] if x['id']==c['id'])
            item['processes'].append(dict(processId=process['processId'],methods={m:v['totalMs'] for m,v in a['methods'].items()},pairs=a['pairs'],performanceRulePass=a['performanceRulePass']))
    cases.append(item)
if passed:
    headline='The improvement survives\nthree Chrome repetitions.'
    lead='The current-position screen met the fixed timing rule in all six 5,000-drone case × process cells, while preserving the checked outputs.'
    finding='The named Chrome build reproduced a bounded implementation benefit. This is evidence for these inputs and queries; it does not establish physical accuracy, a live-swarm frame rate or novelty.'
elif verified:
    headline='Same tested answers.\nThe browser timing target missed.'
    lead='The screen preserved the checked outputs, but at least one of six required case × process cells missed the fixed practical rule.'
    finding='This browser experiment rejects the joint performance premise on its declared workload. All repetitions are retained; pooling or choosing the fastest process cannot rescue the result.'
else:
    headline='A preserved browser attempt.\nAn unresolved result.'
    lead='At least one required execution, numerical or closure check did not qualify. No performance conclusion is accepted.'
    finding='The completed records and failures remain available. This attempt does not establish a speed gain or a physical result. See the stage summary for the exact failure.'
data=dict(kind='recorded-boids-browser-confirmation',sourceCommit=records['sourcePublication']['commit'],verified=verified,practicalPass=passed,timingCalls=sum(len(records.get(s+'Evidence',{}).get('timings',[])) for s in ['p0','p1','p2']),headline=headline,lead=lead,finding=finding,cases=cases)
(p/'viewer/display.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
names['display']='viewer/display.json'
(p/'viewer/binding.json').write_text(json.dumps(dict(records={k:pin(v) for k,v in names.items() if (p/v).exists()}),indent=2)+'\n')
print(json.dumps(dict(displayCases=len(cases),verified=verified,practicalPass=passed,timingCalls=data['timingCalls'])))
