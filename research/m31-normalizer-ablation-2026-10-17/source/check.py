#!/usr/bin/env python3
"""Saved-only exact normalizer ablation checker; no candidate/generator invocation."""
import copy
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
import hashlib
from math import isqrt
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import types
SOURCE_LIMIT=16*1024*1024
SCENE_LIMIT=32*1024*1024
CHECKER_LIMIT=64*1024*1024
REPORT_LIMIT=2*1024*1024
ENCODER=json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)
FROZEN_CHECKER_SHA='084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69'
QUALIFIER_SHA='fd3c20618a4f893c6e90c39c23a309b1830530367384fa4392d2562f85f969cd'
PAIR_SHA='845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
SEMANTIC_SHA='ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'
ARMS=('baseline','candidate')
BASELINE_PINS={'methods.cjs': '9cc6f8dc3bd82acc873f73e52b520297bcba90dea6985bf67fa96ac38fa450d6', 'adapter.cjs': '5cf2b2ddc590915c63bae4f3909e90f196277804d1524aa0ef68165e6b1e4145', 'canonical.cjs': '7112bccefcf00d85451e0c08ef937f46823e012fc806628a588489d34608b7d5', 'rational.cjs': 'de2adde5459d37cc537709f7a488605d9c21d8eedf022efc0a3e9461d4d97333', 'interval.cjs': '73f5afce4dbc2551535127abeaa96d2e6389073e898f9b9dcc70a977ff19ded3', 'boxes.cjs': '01195b1a8b2367b57140659919de235466b18d684f1c71b72134991673f2caa9', 'tree.cjs': '589acbb740cd6cbb3e1ddca784b087dc4a6d60b5276daaaf6118bae87d9f0461', 'pair-prepared.cjs': 'e963362c4b095196b5cc0bcc67c1b613f28c4d6a5e5d5e15101a4f847a61ff56', 'loads.cjs': 'c3fa665a8512ad0c9a73f964b26014c3ad329ee73b68589a61404a3d54ab8a4b', 'zero-filter.cjs': 'd755b78fb774cab645e254316318bd86d95c2869e8d7682a8ed4a927968f0d88', 'binary64-interval.cjs': '048068853915c0fa5e90272e4dd491cbe4448fcbdbb7157008c90abbd7e185ad', 'spec.json': 'a47b9b920ddbbd14e1838e9c031a0b34dd1820f14959ef1295cef039e7f48d2f'}
class CheckError(Exception):
    pass

def require(condition, code):
    if not condition:
        raise CheckError(code)

def fields(value, names, code):
    require(type(value) is dict and set(value) == set(names), code)

def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def ascii_value(value, depth=0):
    require(depth <= 64, 'json-depth-budget')
    if value is None or type(value) is bool:
        return
    if type(value) is int:
        require(-(2**53-1) <= value <= 2**53-1, 'unsafe-json-integer')
    elif type(value) is Decimal:
        require(value.is_finite(), 'nonfinite-decimal')
    elif type(value) is str:
        require(all(32 <= ord(c) <= 126 for c in value), 'nonprintable-json-string')
    elif type(value) is list:
        for item in value:
            ascii_value(item, depth+1)
    elif type(value) is dict:
        for key, item in value.items():
            require(type(key) is str, 'nonstring-json-key')
            ascii_value(key, depth+1)
            ascii_value(item, depth+1)
    else:
        raise CheckError('unsupported-json-value')

def no_duplicates(pairs):
    answer = {}
    for key, value in pairs:
        require(key not in answer, 'duplicate-json-key')
        answer[key] = value
    return answer

def parse_integer(text):
    require(text != '-0' and len(text) <= 17, 'invalid-json-integer')
    value = int(text)
    require(abs(value) <= 2**53-1, 'unsafe-json-integer')
    return value

def parse_decimal(text):
    require(len(text) <= 64, 'decimal-token-budget')
    value = Decimal(text)
    require(value.is_finite(), 'nonfinite-decimal')
    return value

def reject_number(_text):
    raise CheckError('float-or-constant-json-token')

def decode(data):
    try:
        value = json.loads(data, object_pairs_hook=no_duplicates,
                           parse_int=parse_integer, parse_float=parse_decimal,
                           parse_constant=reject_number)
        ascii_value(value)
        return value
    except (UnicodeError, ValueError, RecursionError):
        raise CheckError('invalid-json') from None

def require_canonical_line_bytes(data, value):
    """Compare fragments without materializing another scene-sized JSON string."""
    position = 0
    for fragment in ENCODER.iterencode(value):
        block = fragment.encode('ascii')
        end = position+len(block)
        require(data[position:end] == block, 'artifact-noncanonical-bytes')
        position = end
    require(data[position:] == b'\n', 'artifact-canonical-line-ending')

def load(path, limit, canonical_line=False):
    require(path.is_file() and not path.is_symlink(), 'required-file-missing-or-symlink')
    require(path.stat().st_size <= limit, 'input-file-budget')
    with path.open('rb') as handle:
        data = handle.read(limit+1)
    require(len(data) <= limit, 'input-file-budget')
    value = decode(data)
    if canonical_line:
        require_canonical_line_bytes(data, value)
    return value

def file_pin(path, limit):
    require(path.is_file() and not path.is_symlink(), 'pinned-file-missing-or-symlink')
    total, digest = 0, hashlib.sha256()
    with path.open('rb') as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            total += len(block)
            require(total <= limit, 'pinned-file-budget')
            digest.update(block)
    return {'bytes': total, 'sha256': digest.hexdigest()}

def relative(path, root):
    try:
        value = path.resolve(strict=True).relative_to(root).as_posix()
    except (OSError, ValueError):
        raise CheckError('path-outside-root-or-missing') from None
    require(not path.is_symlink(), 'symlink-path')
    return value

def canonical_hash(value):
    ascii_value(value)
    digest = hashlib.sha256()
    for fragment in ENCODER.iterencode(value):
        digest.update(fragment.encode('ascii'))
    return digest.hexdigest()

def canonical_size(value):
    ascii_value(value)
    return sum(len(fragment) for fragment in ENCODER.iterencode(value))

def write_exclusive(path, value, remaining):
    size = canonical_size(value)+1
    require(size <= remaining, 'checker-output-budget')
    require(path.parent.is_dir() and not path.parent.is_symlink(), 'checker-output-parent')
    digest = hashlib.sha256()
    with path.open('xb') as handle:
        for fragment in ENCODER.iterencode(value):
            block = fragment.encode('ascii')
            handle.write(block)
            digest.update(block)
        handle.write(b'\n')
        digest.update(b'\n')
        handle.flush()
        os.fsync(handle.fileno())
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return {'bytes': size, 'sha256': digest.hexdigest()}

def verify_sources(path, root, required):
    manifest = load(path, 1024*1024)
    require(type(manifest) is dict and type(manifest.get('files')) is list,
            'source-manifest-shape')
    require(1 <= len(manifest['files']) <= 256, 'source-manifest-count')
    indexed, total = {}, 0
    for row in manifest['files']:
        fields(row, ('path', 'bytes', 'sha256'), 'source-manifest-row')
        name = row['path']
        require(type(name) is str and len(name) <= 512 and '\\' not in name,
                'source-manifest-path')
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and str(parts) == name and
                all(p not in ('.', '..') for p in parts.parts) and name not in indexed,
                'source-manifest-duplicate-or-path')
        target = root/name
        require(relative(target, root) == name, 'source-path-not-canonical')
        pin = file_pin(target, SOURCE_LIMIT)
        require(type(row['bytes']) is int and row['bytes'] == pin['bytes'] and
                row['sha256'] == pin['sha256'], 'source-manifest-pin-mismatch')
        indexed[name] = dict(path=name, **pin)
        total += pin['bytes']
        require(total <= 64*1024*1024, 'source-total-budget')
    for target in required:
        require(relative(target, root) in indexed, 'required-source-not-pinned')
    return indexed

def independent_module(path, root, indexed, name, fixed_sha=None):
    key = relative(path, root)
    require(key in indexed, 'independent-source-not-pinned')
    with path.open('rb') as handle:
        source = handle.read(SOURCE_LIMIT+1)
    pin = indexed[key]
    digest = hashlib.sha256(source).hexdigest()
    require(len(source) == pin['bytes'] and digest == pin['sha256'] and
            (fixed_sha is None or digest == fixed_sha), 'independent-source-buffer-pin')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), module.__dict__)
    return module


def integer(value, code, minimum=0):
    require(type(value) is int and value >= minimum, code)
    return value


def timing(value):
    require(type(value) is str and re.fullmatch(r'0|[1-9][0-9]{0,19}',value), 'timing-integer')
    return int(value)


def projected_schedule(slots):
    return [{k:v for k,v in slot.items() if k!='calls'} for slot in slots]


def exact_sqrt_interval(value):
    scale=1<<96
    scaled=value*scale
    low=scaled.numerator//scaled.denominator
    high=-((-scaled.numerator)//scaled.denominator)
    require(low>=0,'cache-normalizer-domain')
    left=isqrt(low*scale); right=isqrt(high*scale)
    return {'l':str(left),'u':str(right if right*right==high*scale else right+1)}


def validate_direct(rows, contract, arm, constants):
    require(contract.get('schema')=='m31-normalizer-direct-contract-v1','cache-contract-schema')
    require(type(rows) is list and len(rows)==32 and len(contract['rows'])==32,'cache-transcript-count')
    for row,fixed in zip(rows,contract['rows']):
        fields(row,('name','group','ordinal','result','error','access'),'cache-transcript-fields')
        for key in ('name','group','ordinal'):
            require(same(row[key],fixed[key]),'cache-transcript-binding:'+key)
        expected=fixed['expected']
        require(same(row['access'],expected['access'][arm]),'cache-access-order')
        if expected.get('error') is not None:
            require(row['result'] is None and same(row['error'],expected['error']),'cache-exception-propagation')
        else:
            require(row['error'] is None and type(row['result']) is dict,'cache-unexpected-error')
            require(row['result'].get('status')==expected['status'] and row['result'].get('branch')==expected['branch'],'cache-status-branch')
            if expected['status']=='positive':
                fields(row['result'],('status','branch','intervals'),'cache-positive-fields')
                intervals=row['result']['intervals']
                fields(intervals,('K','scaledK','beta','nu','coefficient'),'cache-interval-fields')
                beta=exact_sqrt_interval(Fraction(fixed['sourceForceSum'])/constants['mg'])
                nu=exact_sqrt_interval(Fraction(fixed['receiverForce'])/(2*constants['rho']*constants['A']))
                require(same(intervals['beta'],beta),'cache-beta-normalizer')
                require(same(intervals['nu'],nu),'cache-nu-normalizer')
    return True


def lifetime_state_binding(record,expected):
    require(same(record['input'],expected),'lifetime-state-binding')


def cache_mutations(rows,contract,constants,lifetime):
    controls=[]
    specs=[('wrong-source-beta','cache-beta-normalizer',1,'beta'),
           ('wrong-receiver-nu','cache-nu-normalizer',8,'nu'),
           ('wrong-rotor-nu','cache-nu-normalizer',7,'nu'),
           ('wrong-state-binding','lifetime-state-binding',0,'binding'),
           ('swallowed-qualified-exception','cache-status-branch',16,'qualified'),
           ('swallowed-unexpected-exception','cache-exception-propagation',24,'unexpected')]
    require(contract['mutations']==[v[0] for v in specs],'cache-mutation-roster')
    for name,family,index,field in specs:
        clone=copy.deepcopy(rows['candidate']); row=clone[index]
        if field in ('beta','nu'):
            require(row['result']['status']=='positive','cache-positive-mutation-witness')
            donor=rows['candidate'][0 if field=='beta' else 6]['result']['intervals'][field]
            require(not same(row['result']['intervals'][field],donor),'cache-distinct-normalizer-witness')
            row['result']['intervals'][field]=copy.deepcopy(donor)
        elif field=='binding':
            changed_record=copy.deepcopy(lifetime['record'])
            word=changed_record['input']['drones'][0]['state'][13]
            changed_record['input']['drones'][0]['state'][13]=format(int(word,16)^1,'016x')
        elif field=='qualified':
            require(row['error'] is None and row['result']['status']=='unresolved','cache-qualified-witness')
            row['result']['status']='zero'
        else:
            require(row['error'] is not None,'cache-unexpected-witness'); row['error']=None
        error=None
        try:
            if field=='binding': lifetime_state_binding(changed_record,lifetime['expected'])
            else: validate_direct(clone,contract,'candidate',constants)
        except CheckError as exc: error=str(exc)
        controls.append({'name':name,'executed':True,'rejected':error is not None,
            'intendedCoreFailure':error is not None and error.startswith(family),
            'requiredFailureFamilies':[family],'witness':({'id':'lifetime-b','droneIndex':0,'stateIndex':13} if field=='binding' else {'ordinal':index+1,'field':field}),'errors':[] if error is None else [error]})
    return controls


def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    require(len(argv)==1,'checker-cli')
    package=Path(argv[0]).resolve(strict=True)
    require(package==Path(__file__).resolve(strict=True).parent.parent and package.name=='m31-normalizer-ablation-2026-10-17','checker-fixed-package')
    root=package.parent.parent
    source=package/'source'; results=package/'results'; output=results/'check.json'
    require(not output.exists(),'checker-output-already-exists')
    report={'schema':'m31-normalizer-ablation-check-v1','sourceCommit':os.environ.get('RESEARCH_SOURCE_COMMIT'),
        'sourceManifestSha256':None,'configSha256':None,'passed':False,'recordIntegrityPassed':False,
        'equivalencePassed':False,'admissionPassed':False,'benefitPassed':False,'fixedControlsPassed':False,
        'denominator':6,'counts':{'reached':0,'independentlyVerified':0,'modelAdmitted':0,'certified':0},
        'outcomes':[],'generations':[],'corruptionControls':[],'cacheControls':[],
        'nontriviality':{'informative':False,'runs':[]},'performance':[],'referenceFiles':[],
        'errors':[],'transferAuthorized':False,'scope':'Fresh fixed six-state isolated-worker ablation; no browser transfer or physical-validity claim.'}
    old=q=helper=semantic=None
    pins={}; used=0
    try:
        require(os.environ.get('RESEARCH_SUPERVISION_STAGE')=='checker','supervised-checker-required')
        manifest=package/'source-manifest.json'
        require(Path(os.environ.get('RESEARCH_SOURCE_MANIFEST_PATH','')).resolve()==manifest,'source-manifest-environment')
        mp=file_pin(manifest,1024*1024)
        require(mp['sha256']==os.environ.get('RESEARCH_EXPECTED_MANIFEST_SHA256'),'manifest-environment-digest')
        commit=os.environ.get('RESEARCH_SOURCE_COMMIT','')
        require(re.fullmatch('[0-9a-f]{40}',commit) is not None,'source-commit-shape')
        historical=root/'research/m31-moving-admission-2026-10-17/source'
        qualification=root/'research/m31-validator-qualification-2026-10-17/source/qualify.py'
        required=[source/'check.py',source/'config.json',source/'baseline/spec.json',
            source/'direct-contract.json',source/'lifetime-config.json',package/'runtime-pins.json',
            historical/'check.py',historical/'pair-reference.py',historical/'semantic-reference.py',qualification]
        indexed=verify_sources(manifest,root,required)
        for name,digest in BASELINE_PINS.items():
            require(file_pin(source/'baseline'/name,SOURCE_LIMIT)['sha256']==digest,'unchanged-baseline-source:'+name)
        config=load(source/'config.json',SOURCE_LIMIT); cp=file_pin(source/'config.json',SOURCE_LIMIT)
        runtime=load(package/'runtime-pins.json',65536)
        require(same(file_pin(Path(sys.executable).resolve(strict=True),256*1024*1024),runtime['python']),'python-runtime-pin')
        require(config['id']=='m31-normalizer-ablation-v1' and config['method']=='filtered','config-id')
        require(same(config['cases'],[{'id':'run-a','seed':26171011},{'id':'run-b','seed':26171012}]),'config-fresh-seeds')
        require(config['scheduledTimes']==[0,5,10] and config['pairedOrders']==[
            ['baseline','candidate'],['candidate','baseline'],['candidate','baseline'],['baseline','candidate']], 'config-pair-order')
        require(config['launchCutoffUtc']=='2026-10-16T23:00:00Z','config-cutoff')
        receipt=load(package/'source-publication.json',65536)
        require(receipt.get('commit')==commit and receipt.get('manifestSha256')==mp['sha256'] and receipt.get('manifestBytes')==mp['bytes'] and receipt.get('remoteBytesEqualLocal') is True and receipt.get('committedBytesEqualLocal') is True and receipt.get('verifiedFilePins')==len(indexed),'public-source-verification')
        verified=datetime.fromisoformat(receipt['verifiedUtc'].replace('Z','+00:00'))
        cutoff=datetime.fromisoformat(config['launchCutoffUtc'].replace('Z','+00:00'))
        previous=verified
        pins[relative(package/'source-publication.json',root)]=file_pin(package/'source-publication.json',65536)
        for stage in ('kernel','checker'):
            ap=results/f'{stage}-attempt.json'; attempt=load(ap,65536)
            require(attempt.get('stage')==stage and attempt.get('sourceCommit')==commit and
                attempt.get('sourceManifestSha256')==mp['sha256'] and attempt.get('configSha256')==cp['sha256'] and
                attempt.get('launchCutoffUtc')==config['launchCutoffUtc'] and
                attempt.get('allocation')=='sole attempt; existence prevents retry','attempt-source-binding')
            started=datetime.fromisoformat(attempt['startedUtc'].replace('Z','+00:00'))
            require(previous<=started<cutoff,'attempt-publication-cutoff-chronology'); previous=started
            pins[relative(ap,root)]=file_pin(ap,65536)
        closed=load(results/'kernel-supervision.json',2*1024*1024)
        require(all(closed.get(k) is True for k in ('success','closed','childGroupAbsent',
            'scientificChildAbsentBeforeRelease','sourceAndRuntimeRechecked')) and
            closed.get('exitCode')==0 and closed.get('guardianExitCode')==0,'kernel-closed-success')
        require(not (results/'kernel-terminal-error.json').exists(),'kernel-terminal-error')
        pins[relative(results/'kernel-supervision.json',root)]=file_pin(results/'kernel-supervision.json',2*1024*1024)
        report.update(sourceCommit=commit,sourceManifestSha256=mp['sha256'],configSha256=cp['sha256'])
        # Only these four pinned Python modules are loaded; their main functions are never called.
        old=independent_module(historical/'check.py',root,indexed,'frozen_moving_checker',FROZEN_CHECKER_SHA)
        q=independent_module(qualification,root,indexed,'frozen_qualified_controls',QUALIFIER_SHA)
        q.frozen=old  # Explicit dependency handle expected by the frozen qualification functions.
        helper=independent_module(historical/'pair-reference.py',root,indexed,'frozen_pair_reference',PAIR_SHA)
        semantic=independent_module(historical/'semantic-reference.py',root,indexed,'frozen_semantic_reference',SEMANTIC_SHA)
        document,ip=old.load_artifact(results/'index.json',2*1024*1024,with_pin=True)
        pins[relative(results/'index.json',root)]=ip
        old.fields(document,('schema',*old.IDENTITY,'constants','sourceSha256','controls','generations',
            'scheduled','calls','directControls','lifetime','completion','error'),'index-fields')
        require(document['schema']=='m31-normalizer-ablation-index-v1' and document['configId']==config['id'] and
            document['configSha256']==cp['sha256'] and document['sourceManifestSha256']==mp['sha256'] and
            document['sourceCommit']==commit,'index-source-identity')
        require(document['runtime']=={'node':'v24.19.0','platform':'darwin','arch':'arm64',
            'executableSha256':runtime['node']['sha256']},'node-runtime-identity')
        require(document['error'] is None and document['completion']['status']=='complete','kernel-incomplete')
        expected_source={name:row['sha256'] for name,row in indexed.items() if
            (name.startswith(relative(source,root)+'/') and (name.endswith('.cjs') or name.endswith('/config.json') or name.endswith('/spec.json') or name.endswith('/direct-contract.json') or name.endswith('/lifetime-config.json'))) or name in old.GENERATOR_FILES}
        old.bind_sources(document,expected_source)
        generator_hashes={name:indexed[name]['sha256'] for name in old.GENERATOR_FILES}
        old.schedule_shape(projected_schedule(document['scheduled']))
        require(len(document['controls'])==4 and len(document['generations'])==2,'allocation-counts')
        spec=old.load(source/'baseline/spec.json',SOURCE_LIMIT); old.check_spec(spec)
        require(spec.get('maxDrones')==180,'unchanged-max-drones')
        bits,_=helper.constants_from_graph(spec)
        constants={name:helper.dyadic(word) for name,word in bits.items()}
        require(same(document['constants'],{name:helper.hex_bits(word) for name,word in bits.items()}),'constant-operation-graph')
        refdir=results/'reference'
        require(not refdir.exists() or (refdir.is_dir() and not refdir.is_symlink() and not any(refdir.iterdir())),'reference-directory-not-empty')
        refdir.mkdir(exist_ok=True)
        generations={}
        for case,desc in zip(config['cases'],document['generations']):
            expected=relative(results/'generation'/f"{case['id']}.json",root)
            require(desc['path']==expected,'generation-path')
            gen,pin=old.load_artifact(root/expected,8*1024*1024,with_pin=True)
            require(same({k:desc[k] for k in ('bytes','sha256')},pin),'generation-pin')
            report['generations'].append(old.validate_generation(gen,desc,case,config,document,generator_hashes))
            generations[case['id']]=gen; pins[expected]=pin
        require(sum(len(g['reachedTimes']) for g in report['generations'])==6,'all-six-scheduled-states-required')
        report['counts']['reached']=6
        completed={arm:{} for arm in ARMS}
        projected=dict(document,scheduled=projected_schedule(document['scheduled']))
        for arm in ARMS:
            old.metadata_controls(projected,expected_source,completed[arm])
            initial=generations['run-a']['slots'][0]['input']
            changed={'input':copy.deepcopy(initial)}
            changed['input']['drones'][0]['state'][0]=helper.hex_bits(helper.parse_bits(changed['input']['drones'][0]['state'][0])^1)
            q.run_mutation('capture-record-disagreement',{'scene':'run-a-t0'},lambda:old.same_capture(changed,initial),completed[arm],(old.CheckError,))
            frame=copy.deepcopy(generations['run-a']['frames'][0]); frame['words'][0]=helper.hex_bits(helper.parse_bits(frame['words'][0])^1)
            q.run_mutation('pose-capture-disagreement',{'scene':'run-a-t0'},lambda:old.pose_capture(frame,initial),completed[arm],(old.CheckError,))
        jobs=[]; flat=[]
        for control,entry in zip(config['controls'],document['controls']):
            fields(entry,('id','expected','calls'),'control-entry-fields')
            require(entry['id']==control['id'] and same(entry['expected'],control['expected']),'fixed-control-identity')
            captured={'drones':[{'id':d['id'],'state':[helper.hex_bits(helper.literal(v)) for v in d['state']]} for d in control['drones']]}
            jobs.append((control['id'],'control',captured,entry['calls'],control['expected']))
            flat.extend(entry['calls'])
        for i,slot in enumerate(document['scheduled']):
            gen=generations[slot['runId']]; cap=gen['slots'][i%3]; gd=document['generations'][i//3]
            require(slot['status']=='evaluated' and slot['reason'] is None and cap['status']=='reached' and
                slot['generationSha256']==gd['sha256'] and slot['inputSha256']==old.input_hash(slot['id'],cap['input']), 'scheduled-capture-binding')
            require(slot['record']==next(d for d in slot['calls'] if d['arm']=='baseline'),'scheduled-first-record-binding')
            jobs.append((slot['id'],'scheduled',cap['input'],slot['calls'],None)); flat.extend(slot['calls'])
        require(same(document['calls'],flat) and len(flat)==56,'complete-call-ledger')
        samples={}; fixed_ok=[]; seen_paths=set()
        for identifier,kind,captured,descriptors,expected_result in jobs:
            expected_order=[(a,0) for a in ARMS] if kind=='control' else [(a,r) for r,order in enumerate(config['pairedOrders']) for a in order]
            require([(d['arm'],d['repetition']) for d in descriptors]==expected_order,'call-order')
            representatives={}; timing_rows={r:{} for r in range(4)}
            for desc in descriptors:
                fields(desc,('id','kind','arm','repetition','path','bytes','sha256','inputSha256','wallNs','exitCode','methodNs','phases'),'call-descriptor-fields')
                require(desc['id']==identifier and desc['kind']==kind and type(desc['exitCode']) is int and desc['exitCode']==0 and type(desc['repetition']) is int and 0<=desc['repetition']<=3,'call-descriptor-identity')
                require(desc['inputSha256']==old.input_hash(identifier,captured),'call-input-digest')
                name=desc['path']; path=root/name
                require(name==relative(results/'calls'/(identifier+'-'+desc['arm']+'-r'+str(desc['repetition'])+'.json'),root),'call-fixed-path')
                require(name.startswith(relative(results,root)+'/') and relative(path,root)==name and name not in seen_paths,'call-path')
                seen_paths.add(name)
                record,pin=old.load_artifact(path,SCENE_LIMIT,scientific=True,with_pin=True)
                require(same({k:desc[k] for k in ('bytes','sha256')},pin),'call-buffer-pin'); pins[name]=pin
                fields(record,('id','kind','arm','repetition','input','method','error','methodNs','phases'),'call-record-fields')
                for key in ('id','kind','arm','repetition','methodNs','phases'):
                    require(same(record[key],desc[key]),'call-record-binding:'+key)
                require(record['error'] is None and type(record['method']) is dict,'call-error')
                old.raw_input(record['input'],len(captured['drones'])); old.same_capture(record,captured)
                wall=timing(desc['wallNs']); duration=timing(record['methodNs'])
                require(0<duration<=wall<=config['limits']['workerSeconds']*10**9,'worker-cost-boundary')
                phases=record['phases']; last=0
                require(type(phases) is list and len(phases) in (1,3),'method-phase-count')
                for pi,phase in enumerate(phases):
                    fields(phase,('name','offsetNs'),'phase-fields'); off=timing(phase['offsetNs'])
                    require(phase['name']==('prepared','spatial','assembled')[pi] and last<=off<=duration,'phase-order'); last=off
                arm=desc['arm']
                if arm not in representatives: representatives[arm]=record
                else: require(same(record['method'],representatives[arm]['method']),'repeat-complete-method-equivalence')
                if kind=='scheduled': timing_rows[desc['repetition']][arm]=wall
            require(same(representatives['baseline']['method'],representatives['candidate']['method']),'arm-complete-method-equivalence')
            bind_input_file(identifier,captured,results,root,old,pins)
            target=old.regenerate(identifier,captured,spec,bits,helper,semantic)
            graph=old.graph_evidence(target); per_arm={}; certified=True; admitted=True
            for arm in ARMS:
                record=representatives[arm]
                require(len(record['phases'])==(1 if target['globalInvalid'] else 3),'method-phase-completion')
                evidence,_=old.validate_filter_method(record['method'],target,'filtered',constants,helper,semantic,True)
                ok_admitted=target['status']=='admitted'; ok_certified=ok_admitted and evidence.get('toleranceAchieved') is True
                per_arm[arm]={'verified':True,'modelAdmitted':ok_admitted,'certified':ok_certified,'evidence':evidence}
                admitted=admitted and ok_admitted; certified=certified and ok_certified
                if kind=='control':
                    result=record['method']['result']; ok=result['status']==expected_result['status'] and result['branch']==expected_result['branch']; fixed_ok.append(ok)
                    if identifier=='positive':
                        changed={'input':copy.deepcopy(captured)}; changed['input']['drones'][0]['state'][0]=helper.hex_bits(helper.parse_bits(changed['input']['drones'][0]['state'][0])^1)
                        q.run_mutation('altered-control-input',{'scene':identifier},lambda:old.fixed_input(changed,captured),completed[arm],(old.CheckError,))
                    if ok: q.method_controls(record,target,semantic,helper,constants,completed[arm])
            reference=old.scene_reference(identifier,target,graph,per_arm['baseline']['evidence'],semantic)
            reference.update(schema='m31-normalizer-ablation-reference-v1',sourceCommit=commit,inputSha256=old.input_hash(identifier,captured),arms=per_arm)
            refpath=refdir/(identifier+'.json'); pin=write_exclusive(refpath,reference,min(SCENE_LIMIT,CHECKER_LIMIT-REPORT_LIMIT-used)); used+=pin['bytes']
            report['referenceFiles'].append({'id':identifier,'path':relative(refpath,root),**pin})
            report['outcomes'].append({'id':identifier,'kind':kind,'equivalent':True,'arms':{a:{k:v for k,v in per_arm[a].items() if k!='evidence'} for a in ARMS},'status':target['status'],'branch':target['branch'],'graph':graph})
            if kind=='scheduled':
                report['counts']['independentlyVerified']+=1; report['counts']['modelAdmitted']+=int(admitted); report['counts']['certified']+=int(certified)
                samples[identifier]=old.nontrivial_sample(target,graph,True,helper)
                ratios=[Fraction(timing_rows[r]['candidate'],timing_rows[r]['baseline']) for r in range(4)]
                ordered=sorted(ratios); median=(ordered[1]+ordered[2])/2; wins=sum(x<1 for x in ratios)
                report['performance'].append({'id':identifier,'pairs':[{'repetition':r,'baselineWallNs':str(timing_rows[r]['baseline']),'candidateWallNs':str(timing_rows[r]['candidate']),'ratio':old.fraction_wire(ratios[r])} for r in range(4)],'medianRatio':old.fraction_wire(median),'wins':wins,'benefitPassed':median<=Fraction(9,10) and wins>=3})
            del target,representatives,reference,per_arm
        report['fixedControlsPassed']=len(fixed_ok)==8 and all(fixed_ok)
        report['nontriviality']=old.nontriviality(samples)
        for arm in ARMS:
            require(set(completed[arm])==set(q.RECIPES),'qualified-control-roster')
            report['corruptionControls'].extend([dict(completed[arm][name],arm=arm) for name in q.RECIPES])
        # Direct/lifetime integration is fixed below by source contracts, never by transcript claims.
        direct=load(source/'direct-contract.json',SOURCE_LIMIT)
        rows=extract_direct(document,root,old,pins)
        for arm in ARMS: validate_direct(rows[arm],direct,arm,constants)
        for a,b in zip(rows['baseline'],rows['candidate']):
            require(same(a['result'],b['result']) and same(a['error'],b['error']),'cache-pair-equivalence')
        lifetime_evidence,used,lifetime_mutation=verify_lifetime(document,load(source/'lifetime-config.json',SOURCE_LIMIT),root,old,helper,semantic,spec,bits,constants,pins,refdir,used,report,commit)
        report['lifetime']=lifetime_evidence
        report['cacheControls']=cache_mutations(rows,direct,constants,lifetime_mutation)
        verify_kernel_ledger(document,results,root,old,pins,config,ip)
        require(same(document['completion'],{'status':'complete','stage':'complete','methodCalls':62,'generationRuns':2,'reachedScheduled':6,'missingScheduled':0}),'completion-operation-counts')
        require(len(report['corruptionControls'])==42 and len(report['cacheControls'])==6,'corruption-operation-counts')
        report['equivalencePassed']=True
        report['recordIntegrityPassed']=report['fixedControlsPassed'] and all(c['intendedCoreFailure'] for c in report['corruptionControls']+report['cacheControls'])
        report['admissionPassed']=report['counts']['certified']==6 and report['nontriviality']['informative']
        report['benefitPassed']=len(report['performance'])==6 and all(p['benefitPassed'] for p in report['performance'])
        require(sum(pin['bytes'] for pin in pins.values())<=192*1024*1024,'kernel-evidence-budget')
        for name,pin in pins.items(): require(same(file_pin(root/name,max(SCENE_LIMIT,2*1024*1024)),pin),'input-changed-during-check')
        require(same(verify_sources(manifest,root,required),indexed) and same(file_pin(manifest,1024*1024),mp),'source-changed-during-check')
        require(same(file_pin(Path(sys.executable).resolve(strict=True),256*1024*1024),runtime['python']),'python-runtime-changed')
        report['inputPins']=[{'path':name,**pin} for name,pin in sorted(pins.items())]
        report['passed']=report['recordIntegrityPassed'] and report['equivalencePassed'] and report['admissionPassed'] and report['benefitPassed']
        if not report['passed']: report['errors'].append('correctness-admission-or-benefit-gate-failed')
    except Exception as exc:
        known=(CheckError,)+(tuple([old.CheckError]) if old else ())+(tuple([q.CheckError]) if q else ())+(tuple([helper.CheckError]) if helper else ())+(tuple([semantic.CheckError]) if semantic else ())
        report['errors'].append(str(exc)[:256] if isinstance(exc,known) else 'checker-error:'+type(exc).__name__)
        report['passed']=False
    write_exclusive(output,report,REPORT_LIMIT)
    return 0 if report['passed'] else 1


def extract_direct(document,root,old,pins):
    result={}
    require(type(document['directControls']) is list and len(document['directControls'])==2,'direct-descriptor-count')
    package=root/'research/m31-normalizer-ablation-2026-10-17'
    for arm,desc in zip(ARMS,document['directControls']):
        fields(desc,('arm','path','bytes','sha256'),'direct-descriptor-fields')
        path=package/'results/direct'/f'{arm}.json'
        require(desc['arm']==arm and desc['path']==relative(path,root),'direct-descriptor-identity')
        value,pin=old.load_artifact(path,SCENE_LIMIT,scientific=True,with_pin=True)
        require(same({k:desc[k] for k in ('bytes','sha256')},pin),'direct-file-pin')
        fields(value,('schema','arm','synthetic','rows'),'direct-transcript-fields')
        require(value['schema']=='m31-normalizer-direct-v1' and value['arm']==arm and value['synthetic'] is True,'direct-transcript-identity')
        pins[relative(path,root)]=pin; result[arm]=value['rows']
    return result


def bind_input_file(identifier,expected,results,root,old,pins):
    path=results/'inputs'/(identifier+'.json')
    value,pin=old.load_artifact(path,SCENE_LIMIT,scientific=True,with_pin=True)
    require(same(value,expected),'saved-raw-input-binding:'+identifier)
    pins[relative(path,root)]=pin


def verify_lifetime(document,fixtures,root,old,helper,semantic,spec,bits,constants,pins,refdir,used,report,commit):
    results=refdir.parent
    require(len(document['lifetime'])==2,'lifetime-descriptor-count')
    captures={}
    for key in ('a','b'):
        captures['lifetime-'+key]={'drones':[{'id':d['id'],'state':[helper.hex_bits(helper.literal(v)) for v in d['state']]} for d in fixtures[key]['drones']]}
        bind_input_file('lifetime-'+key,captures['lifetime-'+key],results,root,old,pins)
    expected_witnesses=[(0,0,1),(1,0,2)]
    require([(w['receiverId'],w['rotor'],w['sourceId']) for w in fixtures['witnesses']]==expected_witnesses,'lifetime-witness-contract')
    arms={}
    for arm,desc in zip(ARMS,document['lifetime']):
        fields(desc,('id','kind','arm','repetition','path','bytes','sha256','inputSha256','wallNs','exitCode'),'lifetime-descriptor-fields')
        path=results/'lifetime'/(arm+'.json')
        require(desc['id']=='lifetime' and desc['kind']=='lifetime' and desc['arm']==arm and desc['repetition']==0 and desc['inputSha256'] is None and desc['exitCode']==0 and desc['path']==relative(path,root),'lifetime-descriptor-identity')
        wall=timing(desc['wallNs']); require(0<wall<=60*10**9,'lifetime-wall-budget')
        value,pin=old.load_artifact(path,SCENE_LIMIT,scientific=True,with_pin=True)
        require(same({k:desc[k] for k in ('bytes','sha256')},pin),'lifetime-file-pin')
        fields(value,('arm','records'),'lifetime-file-fields')
        require(value['arm']==arm and len(value['records'])==3,'lifetime-record-count')
        total=0
        for identifier,record in zip(('lifetime-a','lifetime-b','lifetime-a'),value['records']):
            fields(record,('id','kind','arm','repetition','input','method','error','methodNs','phases'),'lifetime-record-fields')
            require(record['id']==identifier and record['kind']=='lifetime' and record['arm']==arm and record['repetition']==0 and record['error'] is None,'lifetime-record-identity')
            lifetime_state_binding(record,captures[identifier])
            duration=timing(record['methodNs']); total+=duration; last=0
            require(duration>0 and len(record['phases'])==3,'lifetime-method-timing')
            for i,phase in enumerate(record['phases']):
                fields(phase,('name','offsetNs'),'lifetime-phase-fields'); off=timing(phase['offsetNs'])
                require(phase['name']==('prepared','spatial','assembled')[i] and last<=off<=duration,'lifetime-phase-order'); last=off
        require(total<=wall,'lifetime-complete-cost')
        require(same(value['records'][0]['method'],value['records'][2]['method']),'lifetime-a-return-equivalence')
        pins[relative(path,root)]=pin; arms[arm]=value['records']
    for i in range(3): require(same(arms['baseline'][i]['method'],arms['candidate'][i]['method']),'lifetime-cross-arm-equivalence')
    coefficients={}; summaries=[]
    for i,identifier in enumerate(('lifetime-a','lifetime-b')):
        target=old.regenerate(identifier,captures[identifier],spec,bits,helper,semantic)
        graph=old.graph_evidence(target); evidence={}
        for arm in ARMS:
            evidence[arm],_=old.validate_filter_method(arms[arm][i]['method'],target,'filtered',constants,helper,semantic,True)
            require(target['status']=='admitted' and evidence[arm].get('toleranceAchieved') is True,'lifetime-independent-admission')
        coefficients[identifier]={(p['i'],p['r'],p['j']):p['coefficient'] for p in target['pairs'] if p['oracle']['status']=='positive'}
        reference=old.scene_reference(identifier,target,graph,evidence['baseline'],semantic)
        reference.update(schema='m31-normalizer-ablation-reference-v1',sourceCommit=commit,inputSha256=old.input_hash(identifier,captures[identifier]),arms=evidence)
        path=refdir/(identifier+'.json'); pin=write_exclusive(path,reference,min(SCENE_LIMIT,CHECKER_LIMIT-REPORT_LIMIT-used)); used+=pin['bytes']
        report['referenceFiles'].append({'id':identifier,'path':relative(path,root),**pin})
        summaries.append({'id':identifier,'independentlyVerified':True,'certified':True,'inputSha256':old.input_hash(identifier,captures[identifier])})
    witnesses=[]
    for i,key in enumerate(expected_witnesses):
        require(key in coefficients['lifetime-a'] and key in coefficients['lifetime-b'],'lifetime-positive-witness')
        a=coefficients['lifetime-a'][key]; b=coefficients['lifetime-b'][key]
        require((b[0]>a[1]) if i==0 else (b[1]<a[0]),'lifetime-strict-coefficient-sensitivity')
        witnesses.append({'receiverId':key[0],'rotor':key[1],'sourceId':key[2],
            'a':semantic.interval_wire(a),'b':semantic.interval_wire(b),'direction':'increase' if i==0 else 'decrease'})
    return {'passed':True,'outcomes':summaries,'strictCoefficientWitnesses':witnesses},used,{'record':arms['candidate'][1],'expected':captures['lifetime-b']}


def verify_kernel_ledger(document,results,root,old,pins,config,index_pin):
    expected=[]
    identity={k:document[k] for k in old.IDENTITY}
    expected.append(('run-start',dict(identity,sourceSha256=document['sourceSha256'],constants=document['constants'])))
    expected.extend(('worker-complete',d) for d in document['lifetime'])
    expected.extend(('worker-complete',d) for c in document['controls'] for d in c['calls'])
    for case,desc in zip(config['cases'],document['generations']):
        expected.append(('generation-start',{'id':case['id'],'seed':case['seed'],'generatorOptions':old.generator_options(config,case)}))
        expected.append(('generation-complete',desc))
    expected.append(('generations-ready',{'ids':[d['id'] for d in document['generations']],'sha256':[d['sha256'] for d in document['generations']]}))
    expected.extend(('worker-complete',d) for slot in document['scheduled'] for d in slot['calls'])
    expected.append(('run-complete',{'path':relative(results/'index.json',root),**index_pin,'completion':document['completion']}))
    require(len(expected)==65,'journal-fixed-event-count')
    path=results/'kernel-journal.jsonl'; pin=file_pin(path,4*1024*1024); data=path.read_bytes(); lines=data.splitlines(keepends=True)
    require(len(lines)==len(expected),'journal-event-count')
    for i,(line,(kind,payload)) in enumerate(zip(lines,expected)):
        require(len(line)<=65536,'journal-line-budget')
        event=old.decode_artifact(line)
        fields(event,('schema','sequence','type','payload'),'journal-fields')
        require(event['schema']=='m31-moving-admission-journal-v1' and type(event['sequence']) is int and event['sequence']==i+1 and event['type']==kind and same(event['payload'],payload),'journal-event-binding')
    pins[relative(path,root)]=pin
    expected_dirs={'calls':{Path(d['path']).name for d in document['calls']},
        'direct':{'baseline.json','candidate.json'},'lifetime':{'baseline.json','candidate.json'},
        'generation':{'run-a.json','run-b.json'},'inputs':{c['id']+'.json' for c in config['controls']}|{s['id']+'.json' for s in document['scheduled']}|{'lifetime-a.json','lifetime-b.json'}}
    for name,names in expected_dirs.items():
        directory=results/name
        require(directory.is_dir() and not directory.is_symlink() and {p.name for p in directory.iterdir()}==names,'scientific-directory-closure:'+name)
        require(all(p.is_file() and not p.is_symlink() for p in directory.iterdir()),'scientific-file-type')


if __name__=='__main__':
    raise SystemExit(main())
