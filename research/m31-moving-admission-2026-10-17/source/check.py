#!/usr/bin/env python3
"""Saved-only independent moving-state admission verifier.

Candidate modules and simulator are never imported or executed. The two exact
reference modules are compiled only after complete manifest and fixed-hash gates.
No trajectory regeneration, fixture scan, adaptive witness substitution or retry.
"""
import argparse
import copy
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import types

INDEX_LIMIT = 2*1024*1024
JOURNAL_LIMIT = 4*1024*1024
SCENE_LIMIT = 32*1024*1024
GENERATION_LIMIT = 8*1024*1024
SCIENCE_LIMIT = 256*1024*1024
CHECKER_LIMIT = 64*1024*1024
REPORT_LIMIT = 2*1024*1024
SOURCE_LIMIT = 16*1024*1024
PAIR_SHA = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
SEMANTIC_SHA = 'ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'
METHODS = ('filtered',)
FILTER_FIELDS = ('filterPrepared','filterAttempts','filterZeros','exactScalarCalls')
FILTER_BRANCHES = ('neighbor','upstream','down-cut','near-outside','radial','projection')
CONTROL_IDS = ('positive','distant-zero','raw-force','order-incompatible')
RUN_IDS = ('run-a','run-b')
TIMES = (0,5,10)
SCHEDULE_IDS = tuple(f'{run}-t{t}' for run in RUN_IDS for t in TIMES)
SOURCE_FILES = ('spec.json','config.json','result-contract.json','check.py',
    'pair-reference.py','semantic-reference.py','interval.cjs','rational.cjs','adapter.cjs',
    'pair-prepared.cjs','boxes.cjs','tree.cjs','loads.cjs','binary64-interval.cjs',
    'zero-filter.cjs','methods.cjs','canonical.cjs','run.cjs','supervise.py','guardian.py')
ENCODER = json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)

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


def validate_filter_method(value,target,method,constants,helper,semantic,emit_reference):
    """Validate every new field before a shallow projection to inherited hierarchy.

    The projection shares scientific arrays/certificates; only metadata wrappers
    are rebuilt. No candidate is called and no reported filter success is inferred
    from another candidate result. The independently evaluated pair oracle fixes
    exact zero status and scalar branch priority for each claimed success.
    """
    require_s = semantic.require
    semantic.fields(value,('name','prepared','assembly','result','solve','certificate'),'method-fields')
    require_s(value['name'] == method and method in METHODS,'method-name-or-order')
    assembly=value['assembly']
    semantic.fields(assembly,('mode','globalGuard','tree','queries','work'),'assembly-fields')
    plan=target['plans']['hierarchy']
    expected_mode=method if plan['mode']=='hierarchy' else plan['mode']
    require_s(assembly['mode']==expected_mode,'filter-assembly-mode')
    expected_queries=plan['queries']
    queries=semantic.sequence(assembly['queries'],len(expected_queries),'query-count')
    normalized_queries=[]
    total_zeros=0
    branches={name:0 for name in FILTER_BRANCHES}
    for query, reference_query in zip(queries,expected_queries):
        semantic.fields(query,('i','r','terminals'),'query-fields')
        require_s(type(query['i']) is int and query['i']==reference_query['i'] and
                  type(query['r']) is int and query['r']==reference_query['r'],'query-index-or-order')
        terminals=semantic.sequence(query['terminals'],len(reference_query['terminals']),'terminal-count')
        normalized_terminals=[]
        for terminal, reference_terminal in zip(terminals,reference_query['terminals']):
            require_s(type(terminal) is dict,'terminal-object')
            kind=terminal.get('kind')
            if kind=='zero':
                semantic.fields(terminal,('kind','node','rule','count'),'tree-terminal-fields')
                normalized_terminals.append(terminal)
                continue
            require_s(kind in ('scan','leaf'),'terminal-kind')
            names=('kind','entries','zeroCount','filterZeros') if kind=='scan' else ('kind','node','entries','zeroCount','filterZeros')
            semantic.fields(terminal,names,'filter-terminal-fields')
            require_s(kind==reference_terminal['kind'] and
                      (kind=='scan' or terminal['node']==reference_terminal['node']),
                      'terminal-canonical-traversal')
            members=reference_terminal['members']
            entries=terminal['entries']
            require_s(type(entries) is list and len(entries)<=len(members),'entry-count')
            entry_indices=set()
            for entry in entries:
                semantic.fields(entry,('j','result'),'entry-fields')
                source=semantic.integer(entry['j'],0,len(target['input']['drones'])-1,'entry-source-index')
                entry_indices.add(source)
            zeros=terminal['filterZeros']
            require_s(type(zeros) is list and len(zeros)<=len(members),'filter-zero-count-shape')
            require_s(method=='filtered' or not zeros,'filter-off-nonempty')
            previous=-1
            for zero in zeros:
                semantic.fields(zero,('j','branch'),'filter-zero-fields')
                require_s(semantic.compact_bytes(zero)<=96,'filter-zero-byte-budget')
                source=semantic.integer(zero['j'],0,len(target['input']['drones'])-1,'filter-zero-source-index')
                require_s(source in members and source>previous and source not in entry_indices,
                          'filter-zero-membership-order-or-overlap')
                previous=source
                oracle=target['lookup'][(query['i'],query['r'],source)]['oracle']
                require_s(oracle['status']=='zero','filter-zero-oracle-status')
                require_s(zero['branch'] in FILTER_BRANCHES and zero['branch']==oracle['branch'],
                          'filter-zero-oracle-branch')
                branches[zero['branch']]+=1
                total_zeros+=1
            normalized_terminals.append({k:v for k,v in terminal.items() if k!='filterZeros'})
        normalized_queries.append({'i':query['i'],'r':query['r'],'terminals':normalized_terminals})
    work=assembly['work']
    semantic.fields(work,semantic.WORK_FIELDS+FILTER_FIELDS,'filter-work-fields')
    require_s(all(type(v) is int and 0<=v<=10**9 for v in work.values()),'filter-work-integer')
    expected=dict(plan['work'])
    on=method=='filtered'
    expected.update(filterPrepared=len(target['input']['drones']) if on and not target['globalInvalid'] else 0,
                    filterAttempts=plan['work']['scalarPairs'] if on else 0,
                    filterZeros=total_zeros if on else 0,
                    exactScalarCalls=plan['work']['scalarPairs']-total_zeros if on else plan['work']['scalarPairs'])
    require_s(same(work,expected),'filter-work-counter-reconstruction')
    normalized_assembly=dict(assembly,mode=plan['mode'],queries=normalized_queries,
                             work={k:work[k] for k in semantic.WORK_FIELDS})
    normalized_method=dict(value,name='hierarchy',assembly=normalized_assembly)
    evidence,positive=semantic.validate_method(normalized_method,target,'hierarchy',constants,helper,emit_reference)
    evidence.update(name=method,mode=expected_mode,work=expected,filterZeroBranchCounts=branches)
    return evidence,positive


GENERATOR_FILES = ('outputs/milestone-31-source/sim.cjs',
    'outputs/milestone-31-source/grid.cjs','outputs/milestone-31-source/geometry.cjs',
    'outputs/milestone-31-source/wall-filter.cjs','outputs/milestone-31-source/factory.cjs',
    'outputs/milestone-31-source/factory-wide.cjs','outputs/step02c-source/physics.cjs')
CANDIDATE_FILES = ('methods.cjs','adapter.cjs','canonical.cjs','rational.cjs','interval.cjs',
    'boxes.cjs','tree.cjs','pair-prepared.cjs','loads.cjs','zero-filter.cjs',
    'binary64-interval.cjs','spec.json','run.cjs','config.json')
IDENTITY = ('configId','configSha256','sourceManifestSha256','sourceCommit','runtime')


def strict_science(value):
    """Scientific subtrees cannot exploit Decimal/int or bool/int equality."""
    require(type(value) is not Decimal, 'scientific-numeric-token')
    if type(value) is dict:
        for item in value.values():
            strict_science(item)
    elif type(value) is list:
        for item in value:
            strict_science(item)


def numeric(value, code):
    require(type(value) in (int,Decimal), code)
    result = Fraction(value)
    require(abs(result) < 10**15, code)
    return result


def time_integer(value):
    require(type(value) is str and len(value) <= 20 and
            re.fullmatch(r'0|[1-9][0-9]*',value) is not None,'timing-integer')
    return int(value)


def raw_input(value, count, code='raw-input'):
    fields(value,('drones',),code+'-fields')
    require(type(value['drones']) is list and len(value['drones']) == count,code+'-count')
    for index, drone in enumerate(value['drones']):
        fields(drone,('id','state'),code+'-drone-fields')
        require(type(drone['id']) is int and drone['id'] == index,code+'-id-order')
        require(type(drone['state']) is list and len(drone['state']) == 17 and
                all(type(v) is str and re.fullmatch('[0-9a-f]{16}',v) for v in drone['state']),
                code+'-state-words')
    return value


def input_hash(identifier, value):
    return canonical_hash({'domain':'m31-moving-admission/input/v1','id':identifier,'input':value})


def pose_words(value):
    return [word for drone in value['drones'] for word in drone['state'][:3]+drone['state'][6:10]]


def same_capture(record, captured):
    require(same(record['input'],captured),'capture-record-input-disagreement')


def pose_capture(frame, captured):
    require(same(frame['words'],pose_words(captured)),'pose-capture-disagreement')


def generator_options(config, case):
    return dict(seed=case['seed'],**{key:config['generation'][key] for key in
        ('count','duration','dt','mode','search','filter','record','frameEvery')})


def validate_config(config):
    fields(config,('id','cases','generation','scheduledTimes','method','controls',
                  'nontriviality','limits','launchCutoffUtc'),'config-fields')
    require(config['id']=='m31-moving-admission-v1' and config['method']=='filtered','config-identity')
    require(same(config['cases'],[{'id':'run-a','seed':26171001},{'id':'run-b','seed':26171002}]),'config-cases')
    require(same(config['scheduledTimes'],list(TIMES)),'config-schedule')
    expected={'count':64,'duration':10,'dt':Decimal('0.0025'),'mode':'boids','search':'grid',
        'filter':'wall-priority','record':True,'frameEvery':Decimal('0.2'),
        'factoryVariant':'wide','airflow':'off','observation':'ideal'}
    require(same(config['generation'],expected),'config-generator')
    require(same(config['nontriviality'],{'positiveTimesPerRun':2,
        'horizontalAxisSquaredMinimum':{'n':1,'d':1000000},
        'relativeCoordinateChangeMinimum':{'n':1,'d':1000},
        'requireChangedPositiveEdgeSet':True}),'config-nontriviality')
    require(len(config['controls'])==4,'config-control-count')
    for index, control in enumerate(config['controls']):
        fields(control,('id','expected','drones'),'config-control-fields')
        require(control['id']==CONTROL_IDS[index] and len(control['drones'])==(3 if index==0 else 2),
                'config-control-identity')
        require(same(control['expected'],({'status':'certified','branch':'loads'} if index<2 else
            {'status':'rejected','branch':'raw-force' if index==2 else 'ordering'})),
            'config-control-expectation')
        for di, drone in enumerate(control['drones']):
            fields(drone,('id','state'),'config-control-drone')
            require(type(drone['id']) is int and drone['id']==di and len(drone['state'])==17 and
                    all(type(v) is str and len(v)<=128 for v in drone['state']),'config-control-state')
    for name, expected_limit in {'kernelSeconds':600,'checkerSeconds':600,'guardianSeconds':610,
        'rssBytes':1073741824,'outputBytes':SCIENCE_LIMIT,'sceneBytes':SCENE_LIMIT,
        'generationBytesPerRun':GENERATION_LIMIT,'metadataLogBytes':16*1024*1024,
        'checkerBytes':CHECKER_LIMIT,'checkerReportBytes':REPORT_LIMIT,'indexBytes':INDEX_LIMIT,
        'journalBytes':JOURNAL_LIMIT,'kernelOutputBytes':192*1024*1024,
        'checkerOutputBytes':CHECKER_LIMIT,'combinedBytes':272*1024*1024,
        'combinedOutputBytes':272*1024*1024}.items():
        require(type(config['limits'].get(name)) is int and config['limits'][name]==expected_limit,
                'config-resource:'+name)
    require(config['launchCutoffUtc']=='2026-10-16T23:00:00Z','config-cutoff')


def bind_sources(document, expected):
    require(same(document['sourceSha256'],expected),'source-report-binding')


def schedule_shape(entries):
    require(type(entries) is list and len(entries)==6,'scheduled-count')
    for i,entry in enumerate(entries):
        fields(entry,('id','runId','t','status','reason','generationSha256','inputSha256','record'),
               'scheduled-fields')
        require(entry['id']==SCHEDULE_IDS[i] and entry['runId']==RUN_IDS[i//3] and
                type(entry['t']) is int and entry['t']==TIMES[i%3],'scheduled-identity-order')


def descriptor_shape(desc, identifier, kind, expected_path, captured, capture, prior):
    fields(desc,('id','kind','path','bytes','sha256','inputSha256','capture','call'),'descriptor-fields')
    require(desc['id']==identifier and desc['kind']==kind and desc['path']==expected_path,
            'descriptor-identity-path')
    require(same(desc['capture'],capture),'descriptor-capture-binding')
    require(desc['inputSha256']==input_hash(identifier,captured),'descriptor-input-digest')
    call=desc['call']
    fields(call,('sequence','startNs','endNs','totalNs','phases'),'call-fields')
    require(type(call['sequence']) is int and call['sequence']==prior[0]+1,'call-sequence')
    start,end,total=(time_integer(call[k]) for k in ('startNs','endNs','totalNs'))
    require(prior[1]<=start<=end and end-start==total,'call-timing-order')
    phases=call['phases']
    require(type(phases) is list and 1<=len(phases)<=3,'call-phase-count')
    last=0
    for index,phase in enumerate(phases):
        fields(phase,('name','offsetNs'),'call-phase-fields')
        offset=time_integer(phase['offsetNs'])
        require(phase['name']==('prepared','spatial','assembled')[index] and last<=offset<=total,
                'call-phase-order')
        last=offset
    return call['sequence'],end


def bind_file(desc,path,limit):
    pin=file_pin(path,limit)
    require(type(desc['bytes']) is int and desc['bytes']==pin['bytes'] and desc['sha256']==pin['sha256'],
            'artifact-file-pin')
    return pin


def identity_fields(value,document):
    for key in IDENTITY:
        require(same(value[key],document[key]),'generation-identity:'+key)


def validate_generation(value,desc,case,config,document,generator_hashes):
    fields(value,('schema',*IDENTITY,'id','seed','requested','generatorOptions','generatorSource',
        'initial','final','frames','slots','terminal','callbacks','runSummary','error'),'generation-fields')
    fields(desc,('id','path','bytes','sha256','seed','status','frameCount','reachedTimes','missingTimes','error'),
           'generation-descriptor-fields')
    require(value['schema']=='m31-moving-admission-generation-v1' and value['id']==case['id'] and
            desc['id']==case['id'] and type(value['seed']) is int and value['seed']==case['seed'] and
            desc['seed']==case['seed'],'generation-case')
    identity_fields(value,document)
    require(value['error'] is None and desc['error'] is None and desc['status']=='completed',
            'generator-programming-error')
    require(same(value['requested'],config['generation']) and
            same(value['generatorOptions'],generator_options(config,case)),'generation-options')
    require(same(value['generatorSource'],{'entry':GENERATOR_FILES[0],
        'environment':{'FLOCK_FACTORY_VARIANT':'wide'},'sha256':generator_hashes}),
        'generation-source-binding')
    count=config['generation']['count']
    raw_input(value['initial'],count,'generation-initial')
    raw_input(value['final'],count,'generation-final')
    summary=value['runSummary']
    fields(summary,('diagnostics','lastControl','config','crossings','metrics','timing',
                   'neighborVisits','samples','recording'),'generation-summary-fields')
    expected_config={key:value['generatorOptions'][key] for key in
        ('filter','seed','count','mode','dt','duration','search')}
    expected_config.update(course='factory-v1',airflow='off',observation='ideal')
    require(same(summary['config'],expected_config),'generation-summary-config')
    require(same(summary['recording'],{'cadence':Decimal('0.2'),'streamed':True}),
            'generation-recording')
    metrics=summary['metrics']
    require(type(metrics) is dict and 'end' in metrics and 'stopReason' in metrics,
            'generation-metrics')
    stop=metrics['stopReason']
    require(stop is None or (type(stop) is str and 1<=len(stop)<=256),'generation-stop-reason')
    frames=value['frames']
    require(type(frames) is list and 1<=len(frames)<=52,'generation-frame-count')
    for frame in frames:
        fields(frame,('t','words'),'frame-fields')
        require(type(frame['words']) is list and len(frame['words'])==7*count and
            all(type(v) is str and re.fullmatch('[0-9a-f]{16}',v) for v in frame['words']),
            'frame-raw-words')
    end=numeric(frames[-1]['t'],'frame-time')
    require(0<end<=10 and (end*400).denominator==1,'generation-end-grid')
    require(abs(numeric(metrics['end'],'metrics-end')-end)<=Fraction(1,10**10),'generation-end-binding')
    require((stop is None and end==10) or (stop is not None and end<=10),'generation-stop-end')
    expected_frames=[Fraction(i,5) for i in range(int(end*5)+1)]
    if expected_frames[-1]!=end:
        expected_frames.append(end)
    require([numeric(f['t'],'frame-time') for f in frames]==expected_frames,'generation-frame-schedule')
    pose_capture(frames[0],value['initial'])
    pose_capture(frames[-1],value['final'])
    samples=summary['samples']
    expected_samples=[Fraction(i,10) for i in range(int(end*10)+1)]
    if expected_samples[-1]!=end:
        expected_samples.append(end)
    require(type(samples) is list and [numeric(s.get('t'),'sample-time') for s in samples]==expected_samples,
            'generation-sample-schedule')
    require(same(metrics.get('final'),samples[-1]),'generation-final-sample')
    callbacks=value['callbacks']
    callback_times=[Fraction(t) for t in TIMES if t<=end]
    if stop is not None and end not in callback_times:
        callback_times.append(end)
    require(type(callbacks) is list and len(callbacks)==len(callback_times),'generation-callback-count')
    last_wall=Fraction(0)
    for callback,t in zip(callbacks,callback_times):
        fields(callback,('t','passed','stopReason','wallMs'),'callback-fields')
        wall=numeric(callback['wallMs'],'callback-wall-time')
        require(numeric(callback['t'],'callback-time')==t and wall>=last_wall and
                type(callback['passed']) is int and 0<=callback['passed']<=count and
                callback['stopReason']==(stop if t==end else None),'callback-schedule-or-status')
        last_wall=wall
    slots=value['slots']
    require(type(slots) is list and len(slots)==3,'generation-slot-count')
    reached,missing=[],[]
    for slot,t in zip(slots,TIMES):
        fields(slot,('t','status','input','reason'),'generation-slot-fields')
        require(type(slot['t']) is int and slot['t']==t,'generation-slot-order')
        if t<=end:
            require(slot['status']=='reached' and slot['reason'] is None,'generation-reached-slot')
            raw_input(slot['input'],count,'generation-slot-input')
            pose_capture(next(f for f in frames if numeric(f['t'],'frame-time')==t),slot['input'])
            reached.append(t)
        else:
            require(slot['status']=='not-reached' and slot['input'] is None and slot['reason']==stop and
                    stop is not None,'generation-missing-slot')
            missing.append(t)
    require(same(slots[0]['input'],value['initial']),'generation-initial-capture')
    terminal=value['terminal']
    if end in TIMES:
        require(terminal is None,'unexpected-terminal-capture')
        require(same(next(s['input'] for s in slots if s['t']==end),value['final']),
                'generation-final-scheduled-capture')
    else:
        fields(terminal,('t','input','reason'),'terminal-fields')
        require(numeric(terminal['t'],'terminal-time')==end and terminal['reason']==stop and stop is not None,
                'terminal-time-reason')
        raw_input(terminal['input'],count,'terminal-input')
        require(same(terminal['input'],value['final']),'generation-final-terminal-capture')
        pose_capture(frames[-1],terminal['input'])
    require(type(desc['frameCount']) is int and desc['frameCount']==len(frames) and
            same(desc['reachedTimes'],reached) and same(desc['missingTimes'],missing),
            'generation-descriptor-summary')
    return {'id':case['id'],'reachedTimes':reached,'missingTimes':missing,
            'frameCount':len(frames),'end':fraction_wire(end),'stopReason':stop,'verified':True}


def fraction_wire(value):
    return {'n':str(value.numerator),'d':str(value.denominator)}


class RawWordHelper:
    """Only input literal parsing is adapted; inherited function globals are intact."""
    def __init__(self,helper):
        self.helper=helper
    def literal(self,text):
        return self.helper.parse_bits(text)
    def __getattr__(self,name):
        return getattr(self.helper,name)


def regenerate(identifier,captured,spec,bits,helper,semantic):
    scene={'id':identifier,'family':'moving-admission','expectedClass':'unconstrained',
           'drones':captured['drones']}
    return semantic.regenerate_scene(scene,spec,bits,RawWordHelper(helper))


def graph_evidence(target):
    ids=[d['id'] for d in target['input']['drones']]
    if target['globalInvalid']:
        return {'status':'not-evaluated','reason':'global-preparation-refusal',
                'positiveEdges':[],'positiveRotorPairs':0,'cycle':None,'orderWitness':None}
    positives=[p for p in target['pairs'] if p['oracle']['status']=='positive']
    edges=sorted(set((p['j'],p['i']) for p in positives))
    unresolved=[p for p in target['pairs'] if p['oracle']['status'] not in ('zero','positive')]
    result={'positiveEdges':[list(e) for e in edges],'positiveRotorPairs':len(positives),
            'cycle':None,'orderWitness':None,'status':'unknown' if unresolved else None,
            'reason':'pair-status-not-resolved' if unresolved else None}
    if unresolved:
        result['unresolvedPairCount']=len(unresolved)
        return result
    ranks={identifier:i for i,identifier in enumerate(target['order'])}
    wrong=next((p for p in positives if ranks[p['j']]>=ranks[p['i']]),None)
    if wrong:
        result['orderWitness']={k:wrong[k] for k in ('i','r','j')}
    adjacency={identifier:[] for identifier in ids}
    for source,receiver in edges:
        adjacency[source].append(receiver)
    colors={identifier:0 for identifier in ids}
    stack=[]
    def visit(node):
        colors[node]=1
        stack.append(node)
        for child in adjacency[node]:
            if colors[child]==1:
                return stack[stack.index(child):]+[child]
            if colors[child]==0:
                cycle=visit(child)
                if cycle:
                    return cycle
        stack.pop()
        colors[node]=2
        return None
    cycle=None
    for node in ids:
        if colors[node]==0:
            cycle=visit(node)
            if cycle:
                break
    result['cycle']=cycle
    result['status']='cyclic' if cycle else ('acyclic-order-incompatible' if wrong else 'acyclic-compatible')
    return result


def scene_reference(identifier,target,graph,evidence,semantic):
    pairs=[]
    for pair in target['pairs']:
        row={'i':pair['i'],'r':pair['r'],'j':pair['j'],**pair['oracle']}
        if 'coefficient' in pair:
            row['coefficient']=semantic.interval_wire(pair['coefficient'])
        pairs.append(row)
    return {'schema':'m31-moving-admission-reference-v1','id':identifier,
        'referenceStatus':target['status'],'branch':target['branch'],'witness':target['witness'],
        'prepared':target['prepared'],'plannedPairs':target['planned'],'evaluatedPairs':len(pairs),
        'pairs':pairs,'graph':graph,'loads':evidence.pop('independentReference',[])}

# Fixed recipes: original records only; one disposable clone at a time.
RECIPES = {
 'source-report-binding':['source-report-binding'],
 'altered-control-input':['fixed-control-input-binding'],
 'altered-prepared-point':['prepared-operation-graph'],
 'omitted-positive-entry':['implicit-zero-nonzero'],
 'false-zero-active-leaf':['node-zero-rule','node-zero-oracle-member'],
 'altered-positive-coefficient':['coefficient-reference-containment'],
 'false-fast-zero-positive':['filter-zero-oracle-status'],
 'wrong-fast-zero-branch':['filter-zero-oracle-branch'],
 'filter-work-mismatch':['filter-work-counter-reconstruction'],
 'raw-force-filter-prepared':['filter-work-counter-reconstruction'],
 'raw-force-refusal-status':['canonical-model-refusal'],
 'ordering-refusal-witness':['canonical-model-refusal'],
 'false-root-one':['root-defect-corollary','independent-root-containment'],
 'altered-candidate':['candidate-load-identity'],
 'false-load-box':['signed-root-load-propagation','independent-load-containment'],
 'false-error-zero':['rotor-error-full-box'],
 'missing-scheduled-slot':['scheduled-count'],
 'reordered-scheduled-slots':['scheduled-identity-order'],
 'capture-record-disagreement':['capture-record-input-disagreement'],
 'pose-capture-disagreement':['pose-capture-disagreement'],
}


def run_mutation(name,witness,operation,completed,exceptions):
    require(name in RECIPES and name not in completed,'control-recipe-duplicate')
    require(canonical_size(witness)<=65536,'control-witness-budget')
    error=None
    try:
        operation()
    except exceptions as failure:
        error=str(failure)[:256]
    except Exception as failure:
        error='control-exception:'+type(failure).__name__
    targeted=error is not None and any(error.startswith(prefix) for prefix in RECIPES[name])
    completed[name]={'name':name,'executed':True,'rejected':error is not None,
        'intendedCoreFailure':targeted,'requiredFailureFamilies':RECIPES[name],
        'witness':witness,'errors':[] if error is None else [error]}


def fixed_input(record,expected):
    require(same(record['input'],expected),'fixed-control-input-binding')


def method_controls(record,target,semantic,helper,constants,completed):
    identifier=record['id']
    method=record['method']
    exceptions=(CheckError,semantic.CheckError,helper.CheckError)
    def run(name,witness,mutate):
        if name in completed:
            return
        clone=copy.deepcopy(method)
        mutate(clone)
        run_mutation(name,witness,lambda:validate_filter_method(clone,target,'filtered',
            constants,helper,semantic,False),completed,exceptions)
    if identifier=='raw-force':
        run('raw-force-filter-prepared',{'scene':identifier,'expectedFilterPrepared':0},
            lambda clone:clone['assembly']['work'].__setitem__('filterPrepared',1))
        run('raw-force-refusal-status',{'scene':identifier,'expectedStatus':'rejected'},
            lambda clone:clone['result'].__setitem__('status','certified'))
        return
    if identifier=='order-incompatible':
        require(target['branch']=='ordering' and type(target['witness']) is dict,'ordering-control-witness')
        witness=dict(scene=identifier,expectedWitness=target['witness'])
        run('ordering-refusal-witness',witness,
            lambda clone:clone['result']['witness'].__setitem__('i',65535))
        return
    if identifier!='positive':
        return
    require(target['status']=='admitted','positive-control-admission-witness')
    old=method['prepared'][0]['value']['points'][0][0]
    run('altered-prepared-point',{'scene':identifier,'drone':0,'rotor':0,'coordinate':0,'original':old},
        lambda clone:clone['prepared'][0]['value']['points'][0].__setitem__(0,helper.hex_bits(helper.parse_bits(old)^1)))
    run('filter-work-mismatch',{'scene':identifier,'counter':'exactScalarCalls'},
        lambda clone:clone['assembly']['work'].__setitem__('exactScalarCalls',method['assembly']['work']['exactScalarCalls']+1))
    for qi,query in enumerate(method['assembly']['queries']):
        for ti,terminal in enumerate(query['terminals']):
            if terminal['kind'] not in ('leaf','scan'):
                continue
            for zi,zero in enumerate(terminal['filterZeros']):
                oracle=target['lookup'][(query['i'],query['r'],zero['j'])]['oracle']
                require(oracle['status']=='zero' and oracle['branch']==zero['branch'],'fast-zero-control-witness')
                changed=next(branch for branch in FILTER_BRANCHES if branch!=oracle['branch'])
                run('wrong-fast-zero-branch',{'scene':identifier,'query':qi,'terminal':ti,'source':zero['j'],
                    'expected':oracle['branch'],'changed':changed},
                    lambda clone:clone['assembly']['queries'][qi]['terminals'][ti]['filterZeros'][zi].__setitem__('branch',changed))
            for ei,entry in enumerate(terminal['entries']):
                pair=target['lookup'][(query['i'],query['r'],entry['j'])]
                if pair['oracle']['status']!='positive' or pair['coefficient'][0]<=0:
                    continue
                witness={'scene':identifier,'i':pair['i'],'r':pair['r'],'j':pair['j'],
                         'coefficient':semantic.interval_wire(pair['coefficient'])}
                def omit(clone):
                    t=clone['assembly']['queries'][qi]['terminals'][ti]
                    t['entries'].pop(ei)
                    t['zeroCount']+=1
                run('omitted-positive-entry',witness,omit)
                if terminal['kind']=='leaf':
                    members=[j for j in target['members'][terminal['node']] if j!=query['i']]
                    run('false-zero-active-leaf',dict(witness,node=terminal['node']),
                        lambda clone:clone['assembly']['queries'][qi]['terminals'].__setitem__(ti,
                            {'kind':'zero','node':terminal['node'],'rule':'neighbor','count':len(members)}))
                run('altered-positive-coefficient',witness,
                    lambda clone:clone['assembly']['queries'][qi]['terminals'][ti]['entries'][ei]['result'].__setitem__(
                        'coefficient',{'l':'0','u':'0'}))
                def false_fast(clone):
                    t=clone['assembly']['queries'][qi]['terminals'][ti]
                    j=t['entries'].pop(ei)['j']
                    t['zeroCount']+=1
                    t['filterZeros'].append({'j':j,'branch':'neighbor'})
                    t['filterZeros'].sort(key=lambda item:item['j'])
                    clone['assembly']['work']['filterZeros']+=1
                    clone['assembly']['work']['exactScalarCalls']-=1
                run('false-fast-zero-positive',witness,false_fast)
    for di,drone in enumerate(target['input']['drones']):
        for rotor in range(4):
            identifier=drone['id']
            reference=target['roots'][(identifier,rotor)]
            word=helper.parse_bits(method['solve']['candidate'][di]['x'][rotor])
            proposal=helper.dyadic(word)
            witness={'scene':'positive','id':identifier,'r':rotor,'referenceRoot':semantic.interval_wire(reference)}
            if reference[1]<1:
                run('false-root-one',witness,lambda clone:clone['certificate']['rows'][di*4+rotor].__setitem__(
                    'xstar',{'l':str(1<<96),'u':str(1<<96)}))
                changed=word^1
                if helper.finite(changed) and 0<helper.dyadic(changed)<=1:
                    expected_load=target['exact'][identifier]['forces'][rotor]*helper.dyadic(changed)
                    old_load=semantic.rational(method['certificate']['loads'][di]['candidate']['rotor'][rotor])
                    require(expected_load!=old_load,'candidate-control-identity-witness')
                    run('altered-candidate',dict(witness,originalWord=helper.hex_bits(word),changedWord=helper.hex_bits(changed)),
                        lambda clone:clone['solve']['candidate'][di]['x'].__setitem__(rotor,helper.hex_bits(changed)))
            load_reference=target['loads'][identifier]['rotor'][rotor]
            if load_reference[0]>0:
                run('false-load-box',dict(witness,referenceLoad=semantic.interval_wire(load_reference)),
                    lambda clone:clone['certificate']['loads'][di]['bounds']['rotor'].__setitem__(rotor,{'l':'0','u':'0'}))
            if proposal<reference[0] or proposal>reference[1]:
                gap=reference[0]-proposal if proposal<reference[0] else proposal-reference[1]
                normalized=target['exact'][identifier]['forces'][rotor]*gap/(constants['mg']/4)
                require(normalized>0,'error-control-positive-witness')
                run('false-error-zero',dict(witness,candidate=semantic.fraction_wire(proposal),
                    strictNormalizedErrorLowerBound=semantic.fraction_wire(normalized)),
                    lambda clone:clone['certificate']['loads'][di]['error']['rotor'].__setitem__(rotor,'0'))


def metadata_controls(document,expected_sources,completed):
    changed=dict(document['sourceSha256'])
    key=sorted(changed)[0]
    changed[key]='0'*64 if changed[key]!='0'*64 else '1'*64
    run_mutation('source-report-binding',{'path':key},
        lambda:bind_sources({'sourceSha256':changed},expected_sources),completed,(CheckError,))
    entries=copy.deepcopy(document['scheduled'])
    entries.pop()
    run_mutation('missing-scheduled-slot',{'removed':'run-b-t10'},
        lambda:schedule_shape(entries),completed,(CheckError,))
    entries=copy.deepcopy(document['scheduled'])
    entries[0],entries[1]=entries[1],entries[0]
    run_mutation('reordered-scheduled-slots',{'swapped':['run-a-t0','run-a-t5']},
        lambda:schedule_shape(entries),completed,(CheckError,))


def nontrivial_sample(target,graph,verified,helper):
    tilt=None
    for p in target['prepared']:
        if p['rejection'] is None:
            axis=helper.exact_vector(p['value']['axis'])
            squared=axis[0]**2+axis[1]**2
            if squared>Fraction(1,1000000):
                tilt={'id':p['id'],'horizontalAxisSquared':fraction_wire(squared)}
                break
    positions=[]
    for drone in target['input']['drones']:
        words=[helper.parse_bits(word) for word in drone['state'][:3]]
        positions.append([helper.dyadic(word) for word in words] if all(helper.finite(word) for word in words) else None)
    resolved=verified and graph['status'] in ('cyclic','acyclic-compatible','acyclic-order-incompatible')
    return {'resolved':resolved,'edges':graph['positiveEdges'] if resolved else None,
            'tilt':tilt if verified else None,'positions':positions if verified else None}


def nontriviality(samples):
    reports=[]
    for run in RUN_IDS:
        available={t:samples.get(f'{run}-t{t}') for t in TIMES}
        positive_times=[t for t,s in available.items() if s and s['resolved'] and s['edges']]
        tilt=next((dict(t=t,**s['tilt']) for t,s in available.items() if t>0 and s and s['tilt']),None)
        initial=available[0]
        changed=None
        if initial and initial['resolved']:
            changed=next(({'t':t,'initialEdges':initial['edges'],'changedEdges':s['edges']}
                for t,s in available.items() if t>0 and s and s['resolved'] and s['edges']!=initial['edges']),None)
        displacement={name:None for name in ('x','y','z')}
        if initial and initial['positions'] and initial['positions'][0] is not None:
            p0=initial['positions']
            for t,s in available.items():
                if t==0 or not s or not s['positions'] or s['positions'][0] is None:
                    continue
                pt=s['positions']
                for i in range(1,64):
                    if p0[i] is None or pt[i] is None:
                        continue
                    for k,name in enumerate(('x','y','z')):
                        delta=(pt[i][k]-pt[0][k])-(p0[i][k]-p0[0][k])
                        if displacement[name] is None and abs(delta)>Fraction(1,1000):
                            displacement[name]={'t':t,'id':i,'relativeChange':fraction_wire(delta)}
        informative=len(positive_times)>=2 and tilt is not None and changed is not None and all(displacement.values())
        reports.append({'id':run,'informative':informative,'positiveTimes':positive_times,
            'tiltWitness':tilt,'relativeCoordinateWitnesses':displacement,'changedEdgeWitness':changed})
    return {'informative':all(row['informative'] for row in reports),'runs':reports}


def check_journal(path,document,config,result_pin):
    expected=[('run-start',{k:document[k] for k in (*IDENTITY,'sourceSha256','constants')})]
    def method_events(desc):
        expected.append(('method-start',{k:desc[k] for k in ('id','kind','inputSha256','capture')}|
                         {'sequence':desc['call']['sequence']}))
        expected.append(('method-complete',desc))
    for desc in document['controls']:
        method_events(desc)
    for case,desc in zip(config['cases'],document['generations']):
        expected.append(('generation-start',dict(id=case['id'],seed=case['seed'],generatorOptions=generator_options(config,case))))
        expected.append(('generation-complete',desc))
    expected.append(('generations-ready',{'ids':list(RUN_IDS),'sha256':[d['sha256'] for d in document['generations']]}))
    for slot in document['scheduled']:
        if slot['status']=='not-reached':
            expected.append(('slot-not-reached',slot))
        else:
            method_events(slot['record'])
    expected.append(('run-complete',{'path':document['_indexPath'],'bytes':result_pin['bytes'],
        'sha256':result_pin['sha256'],'completion':document['completion']}))
    require(path.stat().st_size<=JOURNAL_LIMIT,'journal-byte-budget')
    with path.open('rb') as handle:
        for sequence,(kind,payload) in enumerate(expected,1):
            line=handle.readline(65537)
            require(line.endswith(b'\n') and len(line)<=65536,'journal-line-budget-or-ending')
            row=decode_artifact(line)
            fields(row,('schema','sequence','type','payload'),'journal-fields')
            require(row['schema']=='m31-moving-admission-journal-v1' and
                type(row['sequence']) is int and row['sequence']==sequence and row['type']==kind and
                same(row['payload'],payload),'journal-event-binding')
        require(not handle.read(1),'journal-extra-event')
    return {'passed':True,'events':len(expected),**file_pin(path,JOURNAL_LIMIT)}


def decode_artifact(data,scientific=False):
    require(data.endswith(b'\n'),'artifact-line-ending')
    # Compare structure and whitespace without re-rendering diagnostic decimals.
    inside=False
    escaped=False
    for byte in data[:-1]:
        if inside:
            if escaped:
                escaped=False
            elif byte==92:
                escaped=True
            elif byte==34:
                inside=False
        elif byte==34:
            inside=True
        else:
            require(byte not in (9,10,13,32),'artifact-noncompact-layout')
    def ordered_pairs(pairs):
        require([key for key,_ in pairs]==sorted(key for key,_ in pairs),'artifact-unsorted-keys')
        return no_duplicates(pairs)
    try:
        value=json.loads(data,object_pairs_hook=ordered_pairs,parse_int=parse_integer,
                         parse_float=parse_decimal,parse_constant=reject_number)
        ascii_value(value)
    except (UnicodeError,ValueError,RecursionError):
        raise CheckError('artifact-invalid-json') from None
    if scientific:
        strict_science(value)
        require_canonical_line_bytes(data,value)
    return value


def load_artifact(path,limit,scientific=False,with_pin=False):
    require(path.is_file() and not path.is_symlink(),'artifact-missing-or-symlink')
    require(path.stat().st_size<=limit,'artifact-byte-budget')
    data=path.read_bytes()
    require(len(data)<=limit,'artifact-byte-budget')
    value=decode_artifact(data,scientific)
    pin={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    return (value,pin) if with_pin else value


def check_spec(spec):
    for key,value in {'candidateIterations':48,'rootBisections':54,'referenceCoefficientBits':192,
        'referenceSourceBits':192,'referenceRootBisections':128,'fractionBits':96,
        'positiveTermCap':2000000,'leafCapacity':8}.items():
        require(type(spec.get(key)) is int and spec[key]==value,'spec-fixed:'+key)
    require(same(spec['corners'],[[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]]) and
            same(spec['tolerance'],{'numerator':'1','denominator':'100000000'}),'spec-load-semantics')
    # Old scene literals and timing declarations are intentionally never evaluated.


def verify_attempt(path,stage,document,config):
    attempt=load(path,65536)
    fields(attempt,('stage','sourceCommit','sourceManifestSha256','configSha256','launchCutoffUtc',
                   'allocation','startedUtc'),'attempt-fields')
    require(attempt['stage']==stage and attempt['sourceCommit']==document['sourceCommit'] and
        attempt['sourceManifestSha256']==document['sourceManifestSha256'] and
        attempt['configSha256']==document['configSha256'] and
        attempt['launchCutoffUtc']==config['launchCutoffUtc'] and
        attempt['allocation']=='sole attempt; existence prevents retry' and
        type(attempt['startedUtc']) is str,'attempt-source-binding')


def check_result_tree(results,expected_science):
    metadata={f'{stage}-{tail}' for stage in ('kernel','checker') for tail in
        ('attempt.json','guardian.jsonl','stdout.log','stderr.log','terminal-error.json','supervision.json')}
    observed=[]
    for entry in results.iterdir():
        require(not entry.is_symlink(),'results-symlink')
        if entry.name in ('controls','scenes','generation','reference'):
            require(entry.is_dir(),'results-directory-type')
            for child in entry.iterdir():
                require(child.is_file() and not child.is_symlink(),'results-nested-or-symlink')
                name=f'{entry.name}/{child.name}'
                if entry.name!='reference':
                    require(name in expected_science,'unexpected-scientific-file')
                    observed.append(name)
                else:
                    require(child.name in {identifier+'.json' for identifier in (*CONTROL_IDS,*SCHEDULE_IDS)},
                            'unexpected-reference-file')
        else:
            require(entry.is_file() and entry.name in metadata|{'index.json','kernel-journal.jsonl','check.json'},
                    'unexpected-results-file')
    require(set(observed)==expected_science,'scientific-file-set')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',required=True)
    parser.add_argument('--input',required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--root',required=True)
    args=parser.parse_args(argv)
    root=Path(args.root).resolve(strict=True)
    config_path=Path(args.config).resolve(strict=True)
    source=config_path.parent
    package=source.parent
    results=package/'results'
    input_path=Path(args.input).resolve(strict=True)
    manifest_path=Path(args.manifest).resolve(strict=True)
    output_path=Path(args.output)
    report={'schema':'m31-moving-admission-check-v1','passed':False,'advancement':False,
        'denominator':6,'counts':{'reached':0,'independentlyVerified':0,'modelAdmitted':0,'certified':0},
        'outcomes':[],'generations':[],'corruptionControls':[],'fixedControlsPassed':False,
        'nontriviality':{'informative':False,'runs':[]},'errors':[],'referenceFiles':[],
        'scope':'Saved scheduled-state admission only; no trajectory reproduction, feedback, browser timing or physical validation.'}
    completed={}
    used=0
    semantic=helper=None
    try:
        require(input_path==results/'index.json' and output_path.absolute()==results/'check.json' and
                manifest_path==package/'source-manifest.json','checker-fixed-paths')
        require(not output_path.exists(),'checker-output-already-exists')
        required=[source/name for name in SOURCE_FILES]+[root/name for name in GENERATOR_FILES]+[
            package/'runtime-pins.json',package/'PROTOCOL.md',package/'RECORD-CONTRACT.md']
        indexed=verify_sources(manifest_path,root,required)
        manifest_pin=file_pin(manifest_path,1024*1024)
        config_pin=file_pin(config_path,SOURCE_LIMIT)
        config=load(config_path,SOURCE_LIMIT)
        validate_config(config)
        contract=load(source/'result-contract.json',1024*1024)
        require(contract.get('schema')=='m31-moving-admission-contract-v1' and
            same(contract.get('corruptionControls'),[{'name':name,'failurePrefixes':families}
                for name,families in RECIPES.items()]),'checker-contract-recipes')
        runtime_pins=load(package/'runtime-pins.json',65536)
        fields(runtime_pins,('node','python'),'runtime-pins-fields')
        require(same(file_pin(Path(sys.executable).resolve(strict=True),256*1024*1024),runtime_pins['python']),
                'python-runtime-pin')
        document,input_pin=load_artifact(input_path,INDEX_LIMIT,with_pin=True)
        fields(document,('schema',*IDENTITY,'sourceSha256','constants','controls','generations',
                          'scheduled','completion','error'),'index-fields')
        require(document['schema']=='m31-moving-admission-index-v1' and document['configId']==config['id'] and
            document['configSha256']==config_pin['sha256'] and
            document['sourceManifestSha256']==manifest_pin['sha256'],'index-source-config-binding')
        require(type(document['sourceCommit']) is str and re.fullmatch('[0-9a-f]{40}',document['sourceCommit']),
                'source-commit-shape')
        fields(document['runtime'],('node','platform','arch','executableSha256'),'runtime-fields')
        require(document['runtime']['node']=='v24.19.0'
            and document['runtime']['platform']=='darwin' and document['runtime']['arch']=='arm64' and
            document['runtime']['executableSha256']==runtime_pins['node']['sha256'],'runtime-identity')
        for stage in ('kernel','checker'):
            verify_attempt(results/f'{stage}-attempt.json',stage,document,config)
        env_commit=os.environ.get('RESEARCH_SOURCE_COMMIT')
        env_manifest=os.environ.get('RESEARCH_EXPECTED_MANIFEST_SHA256')
        require(env_commit==document['sourceCommit'] and env_manifest==manifest_pin['sha256'] and
                os.environ.get('RESEARCH_SUPERVISION_STAGE')=='checker','supervisor-environment-binding')
        candidate_paths=[relative(source/name,root) for name in CANDIDATE_FILES]+list(GENERATOR_FILES)
        source_hashes={name:indexed[name]['sha256'] for name in candidate_paths}
        generator_hashes={name:indexed[name]['sha256'] for name in GENERATOR_FILES}
        bind_sources(document,source_hashes)
        schedule_shape(document['scheduled'])
        fields(document['completion'],('status','stage','methodCalls','generationRuns','reachedScheduled','missingScheduled'),
               'completion-fields')
        require(document['completion']['status']=='complete' and document['completion']['stage']=='complete' and
                document['error'] is None,'kernel-incomplete-or-programming-error')
        require(type(document['controls']) is list and len(document['controls'])==4 and
                type(document['generations']) is list and len(document['generations'])==2,'allocation-record-counts')
        require(all(slot['status'] in ('evaluated','not-reached') for slot in document['scheduled']),
                'scheduled-incomplete-or-programming-error')
        pins={relative(input_path,root):input_pin,
              relative(results/'kernel-journal.jsonl',root):file_pin(results/'kernel-journal.jsonl',JOURNAL_LIMIT)}
        input_pin=pins[relative(input_path,root)]
        scientific_names=({f'controls/{name}.json' for name in CONTROL_IDS}|{f'generation/{name}.json' for name in RUN_IDS}|
            {f'scenes/{slot["id"]}.json' for slot in document['scheduled'] if slot['status']=='evaluated'})
        check_result_tree(results,scientific_names)
        refdir=results/'reference'
        if refdir.exists():
            require(refdir.is_dir() and not refdir.is_symlink() and not any(refdir.iterdir()),'reference-directory-not-empty')
        else:
            refdir.mkdir()
        # Only these two fixed, previously reviewed source buffers are executable.
        helper=independent_module(source/'pair-reference.py',root,indexed,'m31_pair_reference',PAIR_SHA)
        semantic=independent_module(source/'semantic-reference.py',root,indexed,'m31_semantic_reference',SEMANTIC_SHA)
        spec=load(source/'spec.json',SOURCE_LIMIT)
        check_spec(spec)
        bits,_trace=helper.constants_from_graph(spec)
        constants={name:helper.dyadic(word) for name,word in bits.items()}
        require(same(document['constants'],{name:helper.hex_bits(word) for name,word in bits.items()}),'constant-operation-graph')
        metadata_controls(document,source_hashes,completed)
        report.update(configId=config['id'],configSha256=config_pin['sha256'],
            sourceManifestSha256=manifest_pin['sha256'],sourceCommit=document['sourceCommit'],runtime=document['runtime'])
        generations={}
        for case,desc in zip(config['cases'],document['generations']):
            name=relative(results/'generation'/f'{case["id"]}.json',root)
            require(desc['path']==name,'generation-descriptor-path')
            path=root/name
            gen,loaded_pin=load_artifact(path,GENERATION_LIMIT,with_pin=True)
            generation_evidence=validate_generation(gen,desc,case,config,document,generator_hashes)
            require(type(desc['bytes']) is int and desc['bytes']==loaded_pin['bytes'] and
                    desc['sha256']==loaded_pin['sha256'],'generation-buffer-pin')
            pins[name]=loaded_pin
            generations[case['id']]=gen
            report['generations'].append(generation_evidence)
        reached=sum(len(row['reachedTimes']) for row in report['generations'])
        missing=6-reached
        expected_completion={'status':'complete','stage':'complete','methodCalls':4+reached,
            'generationRuns':2,'reachedScheduled':reached,'missingScheduled':missing}
        require(same(document['completion'],expected_completion),'completion-reconstruction')
        report['counts']['reached']=reached
        # Provenance mutations precede generic digest comparisons.
        initial=generations['run-a']['slots'][0]['input']
        changed={'input':copy.deepcopy(initial)}
        changed['input']['drones'][0]['state'][0]=helper.hex_bits(helper.parse_bits(changed['input']['drones'][0]['state'][0])^1)
        run_mutation('capture-record-disagreement',{'scene':'run-a-t0','id':0,'stateIndex':0},
            lambda:same_capture(changed,initial),completed,(CheckError,))
        changed_frame=copy.deepcopy(generations['run-a']['frames'][0])
        changed_frame['words'][0]=helper.hex_bits(helper.parse_bits(changed_frame['words'][0])^1)
        run_mutation('pose-capture-disagreement',{'scene':'run-a-t0','id':0,'poseIndex':0},
            lambda:pose_capture(changed_frame,initial),completed,(CheckError,))
        prior=(0,0)
        samples={}
        fixed_ok=[]
        jobs=[]
        for ci,(control,desc) in enumerate(zip(config['controls'],document['controls'])):
            expected={'drones':[{'id':d['id'],'state':[helper.hex_bits(helper.literal(v)) for v in d['state']]}
                                for d in control['drones']]}
            jobs.append((control['id'],'control',desc,expected,{'type':'control','controlIndex':ci},control['expected']))
        for si,slot in enumerate(document['scheduled']):
            gen=generations[slot['runId']]
            gd=document['generations'][si//3]
            capture=gen['slots'][si%3]
            require(slot['generationSha256']==gd['sha256'],'scheduled-generation-digest')
            if capture['status']=='not-reached':
                require(slot['status']=='not-reached' and slot['reason']==capture['reason'] and
                        slot['inputSha256'] is None and slot['record'] is None,'scheduled-missing-binding')
                report['outcomes'].append({'id':slot['id'],'kind':'scheduled','status':'not-reached',
                    'reason':slot['reason'],'verified':False,'modelAdmitted':False,'certified':False})
                continue
            require(slot['status']=='evaluated' and slot['reason'] is None and
                    slot['inputSha256']==input_hash(slot['id'],capture['input']),'scheduled-reached-binding')
            cap={'type':'generation-slot','runId':slot['runId'],'generationSha256':gd['sha256'],'slotIndex':si%3,'t':slot['t']}
            jobs.append((slot['id'],'scheduled',slot['record'],capture['input'],cap,None))
        for identifier,kind,desc,captured,capture,expected_result in jobs:
            path=results/('controls' if kind=='control' else 'scenes')/(identifier+'.json')
            name=relative(path,root)
            record,loaded_pin=load_artifact(path,SCENE_LIMIT,scientific=True,with_pin=True)
            fields(record,('id','kind','input','method','error'),'method-record-fields')
            require(record['id']==identifier and record['kind']==kind and record['error'] is None and
                    type(record['method']) is dict,'method-record-identity-or-error')
            raw_input(record['input'],len(captured['drones']))
            if kind=='control':
                fixed_input(record,captured)
                if identifier=='positive':
                    clone={'input':copy.deepcopy(captured)}
                    clone['input']['drones'][0]['state'][0]=helper.hex_bits(helper.parse_bits(clone['input']['drones'][0]['state'][0])^1)
                    run_mutation('altered-control-input',{'scene':identifier,'id':0,'stateIndex':0},
                        lambda:fixed_input(clone,captured),completed,(CheckError,))
            else:
                same_capture(record,captured)
            prior=descriptor_shape(desc,identifier,kind,name,captured,capture,prior)
            require(type(desc['bytes']) is int and desc['bytes']==loaded_pin['bytes'] and
                    desc['sha256']==loaded_pin['sha256'],'method-buffer-pin')
            pins[name]=loaded_pin
            target=regenerate(identifier,captured,spec,bits,helper,semantic)
            require(len(desc['call']['phases'])==(1 if target['globalInvalid'] else 3),'call-phase-completion')
            graph=graph_evidence(target)
            evidence={}
            verified=False
            errors=[]
            cause=None
            try:
                evidence,_=validate_filter_method(record['method'],target,'filtered',constants,helper,semantic,True)
                verified=True
            except (CheckError,semantic.CheckError,helper.CheckError) as failure:
                errors=[str(failure)[:256]]
                candidate_status=record['method'].get('result',{}).get('status')
                cause=('reference-undecidable' if target['status']=='reference-undecidable' else
                    'unvalidated-numerical-refusal-or-status-gap' if candidate_status=='unresolved' else
                    'scientific-record-integrity-failure')
            result=record['method'].get('result',{})
            admitted=verified and target['status']=='admitted'
            certified=admitted and evidence.get('toleranceAchieved') is True
            outcome={'id':identifier,'kind':kind,'verified':verified,'modelAdmitted':admitted,'certified':certified,
                'status':result.get('status'),'branch':result.get('branch'),'witness':result.get('witness'),
                'referenceStatus':target['status'],'referenceBranch':target['branch'],
                'graph':graph,'cause':cause,'errors':errors,'evidence':evidence}
            reference=scene_reference(identifier,target,graph,evidence,semantic)
            refpath=refdir/(identifier+'.json')
            pin=write_exclusive(refpath,reference,min(SCENE_LIMIT,CHECKER_LIMIT-REPORT_LIMIT-used))
            used+=pin['bytes']
            report['referenceFiles'].append({'id':identifier,'path':relative(refpath,root),**pin})
            report['outcomes'].append(outcome)
            if kind=='control':
                matches=verified and result.get('status')==expected_result['status'] and result.get('branch')==expected_result['branch']
                fixed_ok.append(matches)
                if matches:
                    method_controls(record,target,semantic,helper,constants,completed)
            else:
                report['counts']['independentlyVerified']+=int(verified)
                report['counts']['modelAdmitted']+=int(admitted)
                report['counts']['certified']+=int(certified)
                samples[identifier]=nontrivial_sample(target,graph,verified,helper)
            del target,record,reference,evidence
        require(prior[0]==4+reached,'total-method-call-count')
        journal_document=dict(document,_indexPath=relative(input_path,root))
        report['journal']=check_journal(results/'kernel-journal.jsonl',journal_document,config,input_pin)
        report['fixedControlsPassed']=len(fixed_ok)==4 and all(fixed_ok)
        report['nontriviality']=nontriviality(samples)
        for name in RECIPES:
            if name not in completed:
                completed[name]={'name':name,'executed':False,'rejected':False,'intendedCoreFailure':False,
                    'requiredFailureFamilies':RECIPES[name],'witness':None,'errors':['preregistered-witness-unavailable']}
        report['corruptionControls']=[completed[name] for name in RECIPES]
        corruption_ok=all(row['executed'] and row['intendedCoreFailure'] for row in report['corruptionControls'])
        require(sum(pin['bytes'] for pin in pins.values())<=192*1024*1024,'kernel-scientific-output-budget')
        for name,pin in pins.items():
            require(same(file_pin(root/name,max(SCENE_LIMIT,GENERATION_LIMIT)),pin),'evidence-changed-during-check')
        require(same(verify_sources(manifest_path,root,required),indexed) and
                same(file_pin(manifest_path,1024*1024),manifest_pin),'source-changed-during-check')
        require(same(file_pin(Path(sys.executable).resolve(strict=True),256*1024*1024),runtime_pins['python']),
                'python-runtime-changed')
        check_result_tree(results,scientific_names)
        report['inputPins']=[{'path':name,**pin} for name,pin in sorted(pins.items())]
        report['conditionalLoadValidation']={'denominator':report['counts']['modelAdmitted'],
            'allFourTolerancesCertified':report['counts']['certified']}
        report['passed']=(report['fixedControlsPassed'] and corruption_ok and
            report['counts']['independentlyVerified']==reached)
        report['advancement']=(report['passed'] and reached==6 and report['counts']['independentlyVerified']==6 and
            report['counts']['certified']==6 and report['nontriviality']['informative'])
        if not report['passed']:
            report['errors'].append('independent-integrity-or-fixed-controls-failed')
    except Exception as failure:
        known=(CheckError,)+(tuple([semantic.CheckError]) if semantic else ())+(tuple([helper.CheckError]) if helper else ())
        code=str(failure)[:256] if isinstance(failure,known) else 'checker-error:'+type(failure).__name__
        report['errors'].append(code)
        report['passed']=False
        report['advancement']=False
        report['corruptionControls']=[completed[name] for name in RECIPES if name in completed]
    require(output_path.absolute()==results/'check.json' and not output_path.exists(),'report-output-path-or-existing')
    write_exclusive(output_path,report,min(REPORT_LIMIT,CHECKER_LIMIT-used))
    print(json.dumps({'passed':report['passed'],'advancement':report['advancement'],'errors':report['errors']},sort_keys=True))
    return 0 if report['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
