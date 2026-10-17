"""Single prospective 24-scene exact-reference comparison, no simulation/browser."""
from pathlib import Path
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import signal
import sys
import time

PACKAGE='research/m31-tree-first-reference-2026-10-17'
FRESH='research/m31-native-fresh-transfer-2026-10-17'
OLD='research/m31-exact-screening-2026-10-17'
MAX_BYTES=256*1024*1024
MAX_FILE=32*1024*1024

def need(value, code):
    if not value:
        raise RuntimeError(code)

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

def verify(root,manifest):
    for pin in manifest['files']:
        p=Path(pin['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'manifest-path')
        raw=(root/p).read_bytes()
        need(len(raw)==pin['bytes'] and digest(raw)==pin['sha256'], 'source-preservation')
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

class CountedHelper:
    def __init__(self, original, bits_input, counter, poll):
        self.original,self.bits_input,self.counter,self.poll=original,bits_input,counter,poll
    def literal(self,value):
        return self.original.parse_bits(value) if self.bits_input else self.original.literal(value)
    def oracle_case(self,*args):
        self.poll()
        self.counter['calls']+=1
        need(self.counter['calls']<=160000,'scalar-oracle-budget')
        return self.original.oracle_case(*args)
    def __getattr__(self,name):
        return getattr(self.original,name)

def main(root,expected,commit):
    package=root/PACKAGE
    data=(package/'source-manifest.json').read_bytes()
    need(digest(data)==expected,'manifest-identity')
    manifest=json.loads(data)
    runtime=manifest['runtime']['python']
    executable=Path(sys.executable).resolve().read_bytes()
    need(sys.flags.isolated==1 and sys.dont_write_bytecode and sys.version==runtime['version']
         and len(executable)==runtime['bytes'] and digest(executable)==runtime['sha256'], 'pinned-python-runtime')
    receipt=load(package/'source-publication.json')
    need(receipt['commit']==commit and receipt['manifestSha256']==expected and receipt['remoteBytesEqualLocal'] is True
         and receipt['committedBytesEqualLocal'] is True and receipt['verifiedFilePins']==len(manifest['files']), 'public-source-gate')
    cutoff=dt.datetime(2026,10,17,3,tzinfo=dt.timezone.utc)
    need((cutoff-dt.datetime.now(dt.timezone.utc)).total_seconds()>=600,'full-budget-before-cutoff')
    before=verify(root,manifest)
    need((cutoff-dt.datetime.now(dt.timezone.utc)).total_seconds()>=600,'full-budget-after-pin-verification')
    need(not (package/'STARTED.json').exists() and not (package/'results').exists(), 'single-use-allocation')
    results=package/'results'
    results.mkdir()
    protected=[]
    def save(path,obj):
        b=(json.dumps(obj,separators=(',',':'),allow_nan=False)+'\n').encode()
        need(len(b)<=MAX_FILE,'file-byte-budget')
        need(sum(f.stat().st_size for f in results.rglob('*') if f.is_file())+len(b)<=MAX_BYTES,'evidence-byte-budget')
        with path.open('xb') as stream:
            stream.write(b)
        pin={'path':str(path.relative_to(root)),'bytes':len(b),'sha256':digest(b)}
        protected.append(pin)
        return pin
    save(package/'STARTED.json',{'utc':utc(),'sourceCommit':commit,'sourceManifestSha256':expected,'sourcePinsVerified':before})
    started=time.monotonic()
    counter={'calls':0}
    index={'schema':'m31-tree-first-reference-result-v1','sourceCommit':commit,'sourceManifestSha256':expected,
           'startedUtc':utc(),'status':'running','cases':[],'complete':False,'qualified':False,
           'expectedCases':24,'expectedLogicalPairs':79048,'scalarOracleCap':160000,
           'newSimulations':0,'newBrowserCalls':0,'physicalValidation':False,'performanceClaim':False}
    def poll():
        need(time.monotonic()-started<540,'scientific-wall-budget')
    def alarm(signum,frame):
        raise TimeoutError('scientific-wall-budget')
    signal.signal(signal.SIGALRM,alarm)
    signal.alarm(540)
    native_targets={}
    events=None
    try:
        pair=module(root/FRESH/'source/pair-reference.py','_tree_pair')
        semantic=module(root/FRESH/'source/semantic-reference.py','_tree_semantic')
        dispatch=module(package/'source/tree-reference.py','_tree_dispatch')
        validator=module(package/'source/validate.py','_tree_validation')
        corrupt=module(package/'source/corruptions.py','_tree_corruptions')
        native=module(root/FRESH/'source/check.py','_tree_native_saved_checker')
        spec=load(root/FRESH/'source/spec.json')
        old=load(root/OLD/'source/spec.json')
        for key in ('constants','PIBits','corners','referenceCoefficientBits','referenceSourceBits','referenceRootBisections','positiveTermCap'):
            need(spec[key]==old[key],'model-spec-equality')
        need(spec['maxDrones']==180,'unchanged-reference-cap')
        bits,_=pair.constants_from_graph(spec)
        constants={k:pair.dyadic(v) for k,v in bits.items()}
        constant_words={k:pair.hex_bits(v) for k,v in bits.items()}
        descriptors=load(package/'source/cases.json')
        need(len(descriptors)==24 and sum(4*d['n']*(d['n']-1) for d in descriptors)==79048,'complete-case-allocation')
        events=(results/'events.jsonl').open('x')
        index['coverageCorruptions']=[]
        generation=load(root/FRESH/'results/generation.json')
        saved_descriptors={r['id']:r for r in generation['controls']+generation['slots']}
        for ordinal,d in enumerate(descriptors):
            poll()
            index['activeCase']=d['id']
            if d['encoding']=='decimal':
                source=old['scenes'][d['sourceIndex']]
                need(source['id']==d['id'],'old-case-identity')
                scene={k:source[k] for k in ('id','expectedClass','drones')}
                scene['family']='exact-screening'
            else:
                raw=load(root/d['inputPath'])
                scene={'id':d['id'],'expectedClass':d['expectedClass'],'family':'moving-admission','drones':raw['drones']}
            need(len(scene['drones'])==d['n'] and d['n']<=64,'fixed-case-size')
            helper=CountedHelper(pair,d['encoding']=='bits',counter,poll)
            events.write(json.dumps({'event':'start','ordinal':ordinal,'id':d['id'],'callsBefore':counter['calls']})+'\n');events.flush()
            start_calls=counter['calls'];t=time.monotonic()
            full=semantic.regenerate_scene(scene,spec,bits,helper)
            full_wall=time.monotonic()-t;full_calls=counter['calls']-start_calls
            start_calls=counter['calls'];t=time.monotonic()
            tree=dispatch.regenerate_scene(scene,spec,bits,helper,semantic,guard=poll)
            tree_wall=time.monotonic()-t;tree_calls=counter['calls']-start_calls
            need(full_calls==len(full['pairs']) and tree_calls==len(tree['pairs']), 'counted-oracle-accounting')
            need(full['referenceClass']==d['expectedClass'],'fixed-expected-class')
            validation=validator.validate(full,tree,semantic,constants)
            full_record,tree_record=wire(full,semantic),wire(tree,semantic)
            full_pin=save(results/(d['id']+'-full.json'),full_record)
            tree_pin=save(results/(d['id']+'-tree.json'),tree_record)
            controls=corrupt.run_bound(d['id'],full,tree,validator,semantic,constants)
            index['coverageCorruptions'].extend(controls)
            if d['id'] in ('fresh-a-t5','fresh-b-t5'):
                # Small-test adapter only: expand using the already checked full
                # scalar evidence, then replace signed boxes by tree results.
                # No expanded zero dictionary exists in the production dispatcher.
                saved=load(root/FRESH/('results/reference/'+d['id']+'.json'))
                need(saved['prepared']==tree_record['prepared'] and saved['loads']==tree_record['loads'],'fresh-reference-saved-equality')
                adapted=copy.deepcopy(saved)
                adapted['prepared']=tree_record['prepared'];adapted['loads']=tree_record['loads']
                sparse={(p['i'],p['r'],p['j']):p for p in tree_record['pairs'] if p['oracle']['status']=='positive'}
                saved_positive={(p['i'],p['r'],p['j']):p['coefficient'] for p in saved['pairs'] if p['status']=='positive'}
                need({key:p['coefficient'] for key,p in sparse.items()}==saved_positive,'fresh-saved-positive-map-equality')
                for row in adapted['pairs']:
                    if row['status']=='positive':
                        row['coefficient']=sparse[(row['i'],row['r'],row['j'])]['coefficient']
                desc=saved_descriptors[d['id']]
                target=native.reference_target(d['id'],raw,adapted,constant_words,desc['semanticInputSha256'])
                target['inputFileSha256']=desc['input']['sha256']
                native_targets[d['id']]=target
            summary={'id':d['id'],'n':d['n'],'full':full_pin,'tree':tree_pin,'validation':validation,
                     'observedWallSeconds':{'full':full_wall,'tree':tree_wall},
                     'timingScope':'single fixed full-then-tree execution, not randomized/repeated or a performance claim',
                     'fullOracleCalls':full_calls,'treeOracleCalls':tree_calls}
            index['cases'].append(summary)
            events.write(json.dumps({'event':'complete','ordinal':ordinal,'id':d['id'],'full':full_pin,'tree':tree_pin,'callsAfter':counter['calls']})+'\n');events.flush()
            del full,tree,full_record,tree_record
        events.close()
        need(len(index['coverageCorruptions'])==6 and all(c['detected'] for c in index['coverageCorruptions']), 'six-coverage-corruptions')
        poll()
        index['arithmeticFixtures']=native.arithmetic_fixtures()
        need(len(index['arithmeticFixtures'])==14 and all(x['passed'] for x in index['arithmeticFixtures']), 'fourteen-arithmetic-fixtures')
        browser=load(root/FRESH/'results/browser.json')
        oldcheck=load(root/FRESH/'results/check.json')
        reports=[];evidences={}
        for call in browser['calls']:
            e=call['evidence'];key=(e['caseId'],e['method']);evidences[key]=e
            reports.append(native.audit_evidence(e,native_targets[e['caseId']],e['method']))
        need(reports==oldcheck['calls'] and all(x['qualified'] for x in reports),'unchanged-native-strict-verdicts')
        index['nativeCalls']=reports
        index['loadCorruptions']=native.corruption_checks(evidences,native_targets)
        need(index['loadCorruptions']==oldcheck['corruptionChecks'] and all(x['passed'] for x in index['loadCorruptions']), 'four-load-corruptions')
        index['complete']=True
        index['qualified']=True
        index['status']='completed'
        index.pop('activeCase',None)
    except BaseException as error:
        index['status']='failed'
        index['complete']=False
        index['qualified']=False
        index['errorClass']=type(error).__name__
        message=str(error)
        index['reason']=message if len(message)<=160 and message.replace('-','').replace(':','').isalnum() else 'execution-exception'
    finally:
        # A separate 60-second closure allowance stays inside the 600-second
        # total reservation. No child browser or process group exists.
        remaining=max(1,int(600-(time.monotonic()-started)))
        signal.alarm(min(60,remaining))
        try:
            if events is not None:
                events.close()
                journal=(results/'events.jsonl').read_bytes()
                need(len(journal)<=MAX_FILE and sum(f.stat().st_size for f in results.rglob('*') if f.is_file())<=MAX_BYTES,'journal-byte-budget')
                event_pin={'path':str((results/'events.jsonl').relative_to(root)),'bytes':len(journal),'sha256':digest(journal)}
                protected.append(event_pin)
                index['eventJournal']=event_pin
            index['sourcePinsAfter']=verify(root,manifest)
            for pin in protected:
                b=(root/pin['path']).read_bytes()
                need(len(b)==pin['bytes'] and digest(b)==pin['sha256'],'output-preservation')
            index['outputsPreserved']=True
        except BaseException:
            index['status']='failed';index['complete']=False;index['qualified']=False;index['outputsPreserved']=False
        index['scalarOracleCalls']=counter['calls']
        index['wallSeconds']=time.monotonic()-started
        index['finishedUtc']=utc()
        index['resultBytesBeforeIndex']=sum(f.stat().st_size for f in results.rglob('*') if f.is_file())
        if index['wallSeconds']>=600:
            index['status']='failed';index['complete']=False;index['qualified']=False;index['deadlineExceeded']=True
        save(results/'index.json',index)
        signal.alarm(0)
    print(json.dumps({'status':index['status'],'qualified':index['qualified'],'cases':len(index['cases']),
                      'scalarOracleCalls':counter['calls'],'wallSeconds':index['wallSeconds']}))
    return 0 if index['status']=='completed' and index['qualified'] else 1

if __name__=='__main__':
    need(len(sys.argv)==4,'usage-root-manifest-commit')
    raise SystemExit(main(Path(sys.argv[1]).resolve(),sys.argv[2],sys.argv[3]))
