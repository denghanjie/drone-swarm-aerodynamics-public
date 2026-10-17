"""One saved-baseline exact prepared-operand qualification; no new flight/browser."""
from pathlib import Path
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import signal
import sys
import time
import traceback

PACKAGE='research/m31-prepared-reference-2026-10-17'
TREE='research/m31-tree-first-reference-2026-10-17'
FRESH='research/m31-native-fresh-transfer-2026-10-17'
OLD='research/m31-exact-screening-2026-10-17'
MAX_BYTES=256*1024*1024
MAX_FILE=32*1024*1024

def need(value,code):
    if not value:raise RuntimeError(code)
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_bytes())
def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

def verify(root,manifest):
    for pin in manifest['files']:
        p=Path(pin['path']);need(not p.is_absolute() and '..' not in p.parts,'manifest-path')
        raw=(root/p).read_bytes();need(len(raw)==pin['bytes'] and digest(raw)==pin['sha256'],'source-preservation')
    return len(manifest['files'])

def wire(target,semantic):
    out={key:target[key] for key in ('id','input','prepared','planned','globalInvalid','globalGuard','order','status','branch','witness','referenceClass','tree')}
    out['pairs']=[]
    for p in target['pairs']:
        row={k:p[k] for k in ('i','j','r','ii','jj','oracle')}
        if 'coefficient' in p:
            row['coefficient']=semantic.interval_wire(p['coefficient'])
        out['pairs'].append(row)
    out['loads']=[]
    if target['status']=='admitted':
        for row in target['input']['drones']:
            i=row['id']
            out['loads'].append({'id':i,'roots':[semantic.interval_wire(target['roots'][(i,r)]) for r in range(4)],
                                'loads':{key:semantic.interval_wire(v) if key=='collective' else [semantic.interval_wire(x) for x in v]
                                         for key,v in target['loads'][i].items()}})
    if 'coverage' in target:
        out['coverage']=target['coverage']
    return out

class InputHelper:
    def __init__(self,original,raw_words):self.original,self.raw_words=original,raw_words
    def literal(self,value):return self.original.parse_bits(value) if self.raw_words else self.original.literal(value)
    def __getattr__(self,name):return getattr(self.original,name)

def main(root,expected,commit):
    package=root/PACKAGE
    manifest_raw=(package/'source-manifest.json').read_bytes();need(digest(manifest_raw)==expected,'manifest-identity');manifest=json.loads(manifest_raw)
    runtime=manifest['runtime']['python'];exe=Path(sys.executable).resolve().read_bytes()
    need(sys.flags.isolated==1 and sys.dont_write_bytecode and sys.version==runtime['version'] and len(exe)==runtime['bytes'] and digest(exe)==runtime['sha256'],'pinned-python-runtime')
    receipt=load(package/'source-publication.json')
    need(receipt['commit']==commit and receipt['manifestSha256']==expected and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True and receipt['verifiedFilePins']==len(manifest['files']),'public-source-gate')
    cutoff=dt.datetime(2026,10,17,3,tzinfo=dt.timezone.utc)
    need((cutoff-dt.datetime.now(dt.timezone.utc)).total_seconds()>=600,'full-budget-before-cutoff')
    before=verify(root,manifest)
    pin_map={p['path']:p for p in manifest['files']}
    need(len(pin_map)==len(manifest['files']),'unique-source-pins')
    baseline_path=TREE+'/results/index.json'
    need(baseline_path in pin_map,'baseline-index-pinned')
    baseline_index=load(root/baseline_path)
    need(baseline_index['qualified'] is True and baseline_index['complete'] is True and len(baseline_index['cases'])==24,'qualified-baseline-before-import')
    for baseline_case in baseline_index['cases']:
        p=baseline_case['tree']
        need(pin_map.get(p['path'])==p,'baseline-record-pin-membership')
    need(PACKAGE+'/source/cases.json' in pin_map,'case-order-pinned')
    need((cutoff-dt.datetime.now(dt.timezone.utc)).total_seconds()>=600,'full-budget-after-pin-verification')
    need(not (package/'STARTED.json').exists() and not (package/'results').exists(),'single-use-allocation')
    results=package/'results';results.mkdir();protected=[]
    def save(path,value):
        raw=(json.dumps(value,separators=(',',':'),allow_nan=False)+'\n').encode()
        need(len(raw)<=MAX_FILE and sum(f.stat().st_size for f in results.rglob('*') if f.is_file())+len(raw)<=MAX_BYTES,'artifact-byte-budget')
        with path.open('xb') as stream:stream.write(raw)
        pin={'path':str(path.relative_to(root)),'bytes':len(raw),'sha256':digest(raw)};protected.append(pin);return pin
    save(package/'STARTED.json',{'utc':utc(),'sourceCommit':commit,'sourceManifestSha256':expected,'sourcePinsVerified':before})
    started=time.monotonic();budget={'oracleCalls':0,'limit':30000};events=None
    index={'schema':'m31-prepared-reference-result-v1','sourceCommit':commit,'sourceManifestSha256':expected,'startedUtc':utc(),'status':'running','complete':False,'qualified':False,'cases':[],'bindingControls':[],
           'expectedCases':24,'expectedLogicalPairs':79048,'expectedScalarCalls':26570,'newSimulations':0,'newBrowserCalls':0,'newFullOracleRuns':0,'physicalValidation':False,'performanceClaim':False}
    def poll():need(time.monotonic()-started<540,'scientific-wall-budget')
    def alarm(signum,frame):raise TimeoutError('scientific-wall-budget')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(540)
    try:
        pair=module(root/FRESH/'source/pair-reference.py','_prepared_pair')
        semantic=module(root/FRESH/'source/semantic-reference.py','_prepared_semantic')
        tree=module(root/TREE/'source/tree-reference.py','_prepared_frozen_tree')
        candidate=module(package/'source/prepared-reference.py','_prepared_candidate')
        native=module(root/FRESH/'source/check.py','_prepared_native_check')
        spec=load(root/FRESH/'source/spec.json');old=load(root/OLD/'source/spec.json');bits,_=pair.constants_from_graph(spec)
        need(spec['maxDrones']==180 and spec['leafCapacity']==8,'unchanged-reference-cap')
        constants={key:pair.hex_bits(value) for key,value in bits.items()}
        cases=load(package/'source/cases.json');previous=load(root/TREE/'results/index.json');by_id={c['id']:c for c in previous['cases']}
        need(previous['qualified'] and previous['complete'] and len(cases)==24 and [d['id'] for d in cases]==[c['id'] for c in previous['cases']],'fixed-qualified-baseline')
        need(sum(4*d['n']*(d['n']-1) for d in cases)==79048,'fixed-logical-pairs')
        index['baselineIndex']={'path':TREE+'/results/index.json','bytes':(root/TREE/'results/index.json').stat().st_size,'sha256':digest((root/TREE/'results/index.json').read_bytes())}
        generation=load(root/FRESH/'results/generation.json');descriptors={d['id']:d for d in generation['controls']+generation['slots']};native_targets={}
        events=(results/'events.jsonl').open('x')
        for ordinal,d in enumerate(cases):
            poll();index['activeCase']=d['id']
            if d['encoding']=='decimal':
                source=old['scenes'][d['sourceIndex']];need(source['id']==d['id'],'old-case-identity');scene={k:source[k] for k in ('id','expectedClass','drones')};scene['family']='exact-screening'
            else:
                raw=load(root/d['inputPath']);scene={'id':d['id'],'family':'moving-admission','expectedClass':d['expectedClass'],'drones':raw['drones']}
            need(len(scene['drones'])==d['n'] and d['n']<=64,'fixed-case-size')
            baseline=load(root/by_id[d['id']]['tree']['path'])
            events.write(json.dumps({'event':'start','ordinal':ordinal,'id':d['id'],'callsBefore':budget['oracleCalls']})+'\n');events.flush()
            calls_before=budget['oracleCalls'];t=time.monotonic()
            target,counters,controls=candidate.regenerate_scene(scene,spec,bits,InputHelper(pair,d['encoding']=='bits'),semantic,tree,guard=poll,budget=budget,run_controls=d['id']=='dense-cube-27')
            elapsed=time.monotonic()-t;record=wire(target,semantic);pin=save(results/(d['id']+'.json'),record)
            need(record==baseline,'exact-saved-tree-equality')
            need(target['referenceClass']==d['expectedClass'],'expected-reference-class')
            need(counters['oracleCalls']==len(target['pairs'])==by_id[d['id']]['treeOracleCalls']==budget['oracleCalls']-calls_before,'scalar-call-accounting')
            need(counters['operandLookups']==2*counters['oracleCalls'],'two-bound-operands-per-pair')
            need(counters['pairPreparations']==0,'no-pair-preparation')
            index['bindingControls'].extend(controls)
            if d['id'] in ('fresh-a-t5','fresh-b-t5'):
                saved=load(root/FRESH/('results/reference/'+d['id']+'.json'))
                need(saved['prepared']==record['prepared'] and saved['loads']==record['loads'],'fresh-saved-box-equality')
                positives={(p['i'],p['r'],p['j']):p['coefficient'] for p in record['pairs'] if p['oracle']['status']=='positive'}
                need(positives=={(p['i'],p['r'],p['j']):p['coefficient'] for p in saved['pairs'] if p['status']=='positive'},'fresh-saved-positive-map')
                adapted=copy.deepcopy(saved);adapted['prepared']=record['prepared'];adapted['loads']=record['loads']
                for p in adapted['pairs']:
                    if p['status']=='positive':p['coefficient']=positives[(p['i'],p['r'],p['j'])]
                descriptor=descriptors[d['id']];nt=native.reference_target(d['id'],raw,adapted,constants,descriptor['semanticInputSha256']);nt['inputFileSha256']=descriptor['input']['sha256'];native_targets[d['id']]=nt
            index['cases'].append({'id':d['id'],'n':d['n'],'result':pin,'baseline':by_id[d['id']]['tree'],'exactSavedTreeEquality':True,'reuseCounters':counters,'observedWallSeconds':elapsed,'timingScope':'one ordered qualification including binding controls where scheduled; not a performance estimate'})
            events.write(json.dumps({'event':'complete','ordinal':ordinal,'id':d['id'],'result':pin,'callsAfter':budget['oracleCalls']})+'\n');events.flush()
            del target,record,baseline
        need(len(index['bindingControls'])==6 and all(c['detected'] for c in index['bindingControls']),'six-binding-controls')
        need(budget['oracleCalls']==26570,'fixed-scalar-count')
        index['arithmeticFixtures']=native.arithmetic_fixtures();need(len(index['arithmeticFixtures'])==14 and all(x['passed'] for x in index['arithmeticFixtures']),'fourteen-arithmetic-fixtures')
        browser=load(root/FRESH/'results/browser.json');oldcheck=load(root/FRESH/'results/check.json');reports=[];evidences={}
        for call in browser['calls']:
            e=call['evidence'];key=(e['caseId'],e['method']);evidences[key]=e;reports.append(native.audit_evidence(e,native_targets[e['caseId']],e['method']))
        need(reports==oldcheck['calls'] and len(reports)==4 and all(x['qualified'] for x in reports),'unchanged-native-verdicts');index['nativeCalls']=reports
        index['loadCorruptions']=native.corruption_checks(evidences,native_targets)
        need(index['loadCorruptions']==oldcheck['corruptionChecks'] and all(x['passed'] for x in index['loadCorruptions']),'four-load-corruptions')
        index['retainedCoverageControlIds']=[c['id'] for c in previous['coverageCorruptions']]
        index['coverageControlsRerun']=False
        index.update(status='completed',complete=True,qualified=True);index.pop('activeCase',None)
    except BaseException as error:
        index.update(status='failed',complete=False,qualified=False,errorClass=type(error).__name__)
        message=str(error);index['reason']=message if len(message)<=160 and message.replace('-','').replace(':','').isalnum() else 'execution-exception'
        index['traceLocations']=[{'file':Path(f.filename).name,'line':f.lineno,'function':f.name} for f in traceback.extract_tb(error.__traceback__)]
    finally:
        signal.alarm(min(60,max(1,int(600-(time.monotonic()-started)))))
        try:
            if events is not None:
                events.close();b=(results/'events.jsonl').read_bytes();need(len(b)<=MAX_FILE,'journal-byte-budget')
                ep={'path':str((results/'events.jsonl').relative_to(root)),'bytes':len(b),'sha256':digest(b)};protected.append(ep);index['eventJournal']=ep
            index['sourcePinsAfter']=verify(root,manifest)
            for p in protected:
                b=(root/p['path']).read_bytes();need(len(b)==p['bytes'] and digest(b)==p['sha256'],'output-preservation')
            index['outputsPreserved']=True
        except BaseException:index.update(status='failed',complete=False,qualified=False,outputsPreserved=False)
        index['scalarOracleCalls']=budget['oracleCalls'];index['wallSeconds']=time.monotonic()-started;index['finishedUtc']=utc()
        index['resultBytesBeforeIndex']=sum(f.stat().st_size for f in results.rglob('*') if f.is_file())
        if index['wallSeconds']>=600:index.update(status='failed',complete=False,qualified=False,deadlineExceeded=True)
        save(results/'index.json',index);signal.alarm(0)
    print(json.dumps({'status':index['status'],'qualified':index['qualified'],'cases':len(index['cases']),'scalarOracleCalls':budget['oracleCalls'],'wallSeconds':index['wallSeconds']}))
    return 0 if index['status']=='completed' and index['qualified'] else 1

if __name__=='__main__':
    need(len(sys.argv)==4,'usage-root-manifest-commit')
    raise SystemExit(main(Path(sys.argv[1]).resolve(),sys.argv[2],sys.argv[3]))
