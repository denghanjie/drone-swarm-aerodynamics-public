"""Post-attempt display projection only. No initializer or numerical producer.

Uses the frozen independent binary reader on saved records; this is not a new
scientific check. Scientific qualification remains the saved check.json result.
"""
from pathlib import Path
import hashlib, importlib.util, json, time

PACKAGE = 'research/m31-native-tree-browser-probe-2026-10-17'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
END = time.monotonic()+60
def need(ok, message):
    if not ok: raise ValueError(message)
def guard(ctx): need(time.monotonic()<END, 'display-export-deadline')
def fields(value, names, message): need(type(value) is dict and set(value)==set(names),message)
def integer(value, low, high, message):
    need(type(value) is int and low<=value<=high,message)
    return value
def decode(raw): return json.loads(raw)
def identity(p):
    raw=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def read_pin(root, pin):
    guard(None)
    p=root/pin['path']
    need(not p.is_symlink() and p.resolve().is_relative_to(root) and p.stat().st_size<=32*1024**2,'display-pin-location-size')
    need(identity(p)==pin,'display-pin-identity')
    return p.read_bytes()
def write(p, value):
    raw=(json.dumps(value,separators=(',',':'),allow_nan=False)+'\n').encode()
    need(len(raw)<=8*1024**2,'display-file-cap')
    with p.open('xb') as f: f.write(raw)
    return {'path':p.relative_to(HERE).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def pose(rows, key):
    return [{'id':r['id'],'pose':r[key][:3]+r[key][6:10]} for r in rows]
def main():
    p=ROOT/PACKAGE; results=p/'results'
    attempt=json.loads((results/'run-attempt.json').read_bytes())
    need(attempt['status'] in ('failed','completed'),'attempt-must-be-closed')
    manifest=json.loads((p/'source-manifest.json').read_bytes())
    pin=next(x for x in manifest['files'] if x['path']==PACKAGE+'/source/compact-check.py')
    read_pin(ROOT,pin)
    spec=importlib.util.spec_from_file_location('_display_saved_decoder',ROOT/pin['path'])
    compact=importlib.util.module_from_spec(spec); spec.loader.exec_module(compact)
    import sys
    reader=compact.Resolver(sys.modules[__name__],{'root':ROOT})
    check_path=results/'check.json'
    check=json.loads(check_path.read_bytes()) if check_path.exists() else {}
    validated=attempt['status']=='completed' and check.get('passed') is True and check.get('complete') is True
    metrics={r['caseId']:r for r in check.get('cases',[])} if validated else {}
    jp=results/'browser-journal.jsonl'
    journal=[json.loads(line) for line in jp.read_bytes().splitlines()] if jp.exists() else []
    data={}; pending={}; first_stage_done=False
    # Decode only saved initial-query H/stage/endpoint records. Later native
    # payloads are irrelevant to this fixed display selection.
    for event in journal:
        guard(None)
        if event['kind']=='initial': first_stage_done=False
        if event['kind'] not in ('native','stage','step'): continue
        if event['kind'] in ('native','stage') and first_stage_done: continue
        if event['kind']=='native':
            descriptor=decode(read_pin(ROOT,event['recordPin']))
            method=reader.stream(next(f['stream'] for f in descriptor['fields'] if f['key']=='method'))
            if method!='H': continue
        body=reader.record(event['recordPin'])
        case=body.get('caseId') or body.get('recordMeta',{}).get('caseId')
        if event['kind']=='native':
            meta=body.get('recordMeta',{})
            if body.get('method')=='H' and meta.get('stageId','').endswith('-k1'):
                pending[meta['caseId']]=(body,event['recordPin'])
        elif event['kind']=='stage' and body.get('stageIndex')==1 and body.get('status')=='completed' and case in pending:
            first_stage_done=True
            native,native_pin=pending.pop(case); tree=native.get('tree')
            need(any(r['method']=='H' and r['recordPin']==native_pin for r in body['nativeRefs']),'display-H-stage-binding')
            if tree is None or not tree.get('complete') or not tree.get('eligible'): continue
            rows=body['records']; n=len(rows); selected=sorted(set([0,n//4,n//2,(3*n)//4,n-1])); receivers=[]
            for i in selected:
                row=tree['receivers'][i]; encoded=row['gathered']; gathered=encoded['data']
                if encoded['kind']=='runs': gathered=[j for start,length in zip(gathered[::2],gathered[1::2]) for j in range(start,start+length)]
                receivers.append({'index':i,'id':rows[i]['id'],'gathered':gathered,
                    'boxes':[{'node':c['node'],'min':tree['nodes'][c['node']]['min'],'max':tree['nodes'][c['node']]['max']} for c in row['culled']]})
            data[case]={'schema':'m31-tree-probe-display-v1','caseId':case,'n':n,'sourceCommit':attempt['sourceCommit'],'validated':validated,
                'frames':[{'id':'query','label':'First projected query · t=0','drones':pose(rows,'stateWords')}],
                'receivers':receivers,'metrics':metrics.get(case),
                'provenance':{'attempt':identity(results/'run-attempt.json'),'journal':identity(jp),'firstStage':event['recordPin'],'firstH':native_pin,'check':identity(check_path) if check_path.exists() else None}}
        elif event['kind']=='step' and case in data and body.get('final'):
            data[case]['frames'].append({'id':'final','label':'Accepted endpoint · t=0.0025 s','drones':pose(body['final'],'stateWords')})
            data[case]['provenance']['endpoint']=event['recordPin']
        reader.clear()
    reader.verify_preserved()
    output=HERE/'data'; output.mkdir(exist_ok=False)
    case_pins=[dict(write(output/(case+'.json'),value),caseId=case) for case,value in data.items()]
    if validated:
        headline='Numerical checks passed; the cost gate '+('passed.' if check['engineeringPassed'] else 'did not pass.')
        detail='Four fixed cases, one recorded flight step each. The cost decision uses both 5,000-drone cases; no real-time or physical-validation claim.'
    else:
        headline='Attempt stopped before complete qualification.'
        detail='The saved attempt is terminal and has not been retried. '+('Partial saved geometry is shown without a successful optimization claim.' if data else 'No complete first-query record exists, so no new swarm geometry is displayed. Earlier recorded 3D views remain linked below.')
    write(HERE/'record-pins.json',{'schema':'m31-tree-probe-display-pins-v1','headline':headline,'detail':detail,'checkAvailable':check_path.exists(),'cases':case_pins})
    write(HERE/'EXPORT-RECEIPT.json',{'scientificCalls':0,'sourceCommit':attempt['sourceCommit'],'attempt':identity(results/'run-attempt.json'),'decoder':pin,'cases':len(data),'validated':validated,'readPins':list(reader.seen.values())})
    print(json.dumps({'cases':len(data),'validated':validated,'scientificCalls':0}))
if __name__=='__main__': main()
