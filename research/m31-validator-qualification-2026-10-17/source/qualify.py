#!/usr/bin/env python3
"""Fresh qualification of exposed, immutable saved evidence. No old main/candidate/generator call.

Only standard-library gates run before complete new/old manifest closures pass.
Frozen modules are loaded from pinned byte buffers under non-main module names.
"""
import argparse
import copy
from decimal import Decimal
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import types

SOURCE_LIMIT=16*1024*1024
CHECKER_LIMIT=64*1024*1024
REPORT_LIMIT=2*1024*1024
SCENE_LIMIT=32*1024*1024
ENCODER=json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)
FROZEN_CHECKER_SHA='084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69'
PAIR_SHA='845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
SEMANTIC_SHA='ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'
frozen=None
EXPECTED_CONFIG={'id': 'm31-validator-qualification-v1', 'launchCutoffUtc': '2026-10-16T23:00:00Z', 'limits': {'qualificationSeconds': 600, 'guardianSeconds': 610, 'rssBytes': 1073741824, 'scientificOutputBytes': 67108864, 'referenceBytes': 33554432, 'qualificationReportBytes': 2097152, 'metadataLogBytes': 16777216, 'combinedOutputBytes': 83886080}, 'prior': {'package': 'research/m31-moving-admission-2026-10-17', 'sourceCommit': '2a957d2b0bb26e731c8cd184bc13f51f673e9a0d', 'sourceManifestSha256': '37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21', 'resultCommit': '5a5efeef2d216188fa93a8034c4573d7327c5411', 'resultManifestSha256': 'e60a5bf356f9f27bf31f79fc3274c0c37675353f1b8b0de20a1a6fc1b69487d8', 'resultPublicationReceipt': 'research/publication-receipts/m31-moving-admission-result-2026-10-17.json', 'resultPublicationReceiptSha256': '246869cd1b867de7a4bfb692f948926eef2aeb696e2185fdcfb89dc2aa3c9758', 'checkSha256': '9991d6a3d60d7d0e58f69d0074947b38453013246b2c63ecfa3bf26a7086eb6d', 'checkerSourceSha256': '084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69'}, 'referenceIds': ['positive', 'distant-zero', 'raw-force', 'order-incompatible', 'run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10'], 'negativeControlCount': 21, 'scope': 'Exposed-corpus validator qualification only; no retroactive pass, fresh replication or transfer.'}
RECIPES={'source-report-binding': ['source-report-binding'], 'altered-control-input': ['fixed-control-input-binding'], 'altered-prepared-point': ['prepared-operation-graph'], 'omitted-positive-entry': ['implicit-zero-nonzero'], 'false-zero-active-leaf': ['node-zero-rule', 'node-zero-oracle-member'], 'altered-positive-coefficient': ['coefficient-reference-containment'], 'false-fast-zero-positive': ['filter-zero-oracle-status'], 'wrong-fast-zero-branch': ['filter-zero-oracle-branch'], 'filter-work-mismatch': ['filter-work-counter-reconstruction'], 'raw-force-filter-prepared': ['filter-work-counter-reconstruction'], 'raw-force-refusal-status': ['canonical-model-refusal'], 'ordering-refusal-witness': ['canonical-model-refusal'], 'false-root-one': ['root-defect-corollary', 'independent-root-containment'], 'altered-candidate': ['candidate-load-identity'], 'false-load-box': ['signed-root-load-propagation', 'independent-load-containment'], 'false-error-zero': ['rotor-error-full-box'], 'missing-scheduled-slot': ['scheduled-count'], 'reordered-scheduled-slots': ['scheduled-identity-order'], 'capture-record-disagreement': ['capture-record-input-disagreement'], 'pose-capture-disagreement': ['pose-capture-disagreement'], 'false-zero-counter-interception': ['filter-work-counter-reconstruction']}

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


def method_controls(record,target,semantic,helper,constants,completed):
    identifier=record['id']
    method=record['method']
    exceptions=(CheckError,frozen.CheckError,semantic.CheckError,helper.CheckError)
    def run(name,witness,mutate):
        if name in completed:
            return
        clone=copy.deepcopy(method)
        mutate(clone)
        run_mutation(name,witness,lambda:frozen.validate_filter_method(clone,target,'filtered',
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
                changed=next(branch for branch in frozen.FILTER_BRANCHES if branch!=oracle['branch'])
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
                if terminal['kind']=='leaf' and 'false-zero-active-leaf' not in completed:
                    require((qi,ti,ei,query['i'],query['r'],entry['j'],terminal['node'])==(0,0,0,0,0,1,0),
                            'fixed-node-control-witness-identity')
                    members=[j for j in target['members'][terminal['node']] if j!=query['i']]
                    removed_filter_zeros=len(terminal['filterZeros'])
                    require(removed_filter_zeros==1,'fixed-mixed-leaf-regression-witness')
                    def replace_leaf(clone):
                        clone['assembly']['queries'][qi]['terminals'][ti]={
                            'kind':'zero','node':terminal['node'],'rule':'neighbor','count':len(members)}
                    def corrected_node_claim(clone):
                        replace_leaf(clone)
                        clone['assembly']['work']['filterZeros']-=removed_filter_zeros
                        clone['assembly']['work']['exactScalarCalls']+=removed_filter_zeros
                    control_witness=dict(witness,node=terminal['node'],removedFilterZeros=removed_filter_zeros)
                    run('false-zero-active-leaf',control_witness,corrected_node_claim)
                    run('false-zero-counter-interception',control_witness,replace_leaf)
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



def gates(root,package,config_path,manifest_path,results):
    """No frozen module import or numerical construction occurs in this gate."""
    config=load(config_path,1024*1024)
    require(same(config,EXPECTED_CONFIG),'qualification-fixed-config')
    prior=config['prior']
    baseline=root/prior['package']
    receipt_path=root/prior['resultPublicationReceipt']
    require(file_pin(receipt_path,65536)['sha256']==prior['resultPublicationReceiptSha256'],'prior-receipt-pin')
    old_manifest=baseline/'source-manifest.json'
    old_result_manifest=baseline/'result-manifest.json'
    require(file_pin(old_manifest,1024*1024)['sha256']==prior['sourceManifestSha256'] and
        file_pin(old_result_manifest,1024*1024)['sha256']==prior['resultManifestSha256'],'prior-manifest-pins')
    own_required=[package/name for name in ('source/qualify.py','source/config.json','source/result-contract.json',
        'source/supervise.py','source/guardian.py','PROTOCOL.md','runtime-pins.json')]
    dependency_required=[baseline/'source'/name for name in
        ('check.py','pair-reference.py','semantic-reference.py','config.json','spec.json')]+[
        old_manifest,old_result_manifest,receipt_path]
    own_index=verify_sources(manifest_path,root,own_required+dependency_required)
    old_index=verify_sources(old_manifest,root,dependency_required[:5])
    corpus=[baseline/'results'/name for name in ('index.json','kernel-journal.jsonl','generation/run-a.json',
        'generation/run-b.json','check.json','kernel-attempt.json','checker-attempt.json',
        'kernel-supervision.json','checker-supervision.json')]
    corpus += [baseline/'results'/('controls' if i<4 else 'scenes')/(identifier+'.json')
               for i,identifier in enumerate(config['referenceIds'])]
    result_index=verify_sources(old_result_manifest,root,corpus)
    require(len(old_index)==53 and len(result_index)==128,'prior-frozen-closure-counts')
    receipt=load(receipt_path,65536)
    require(receipt.get('commit')==prior['resultCommit'] and
        receipt.get('manifestPath')==relative(old_result_manifest,root) and
        receipt.get('manifestSha256')==prior['resultManifestSha256'] and
        receipt.get('manifestBytes')==file_pin(old_result_manifest,1024*1024)['bytes'] and
        receipt.get('remoteBytesEqualLocal') is True and receipt.get('committedBytesEqualLocal') is True and
        receipt.get('verifiedFilePins')==128,'prior-publication-receipt-binding')
    require(file_pin(baseline/'results/check.json',2*1024*1024)['sha256']==prior['checkSha256'],
            'historical-failure-pin')
    runtime=load(package/'runtime-pins.json',65536)
    fields(runtime,('python',),'qualification-runtime-fields')
    require(same(file_pin(Path(sys.executable).resolve(strict=True),256*1024*1024),runtime['python']),
            'qualification-python-pin')
    manifest_pin=file_pin(manifest_path,1024*1024)
    config_pin=file_pin(config_path,1024*1024)
    commit=os.environ.get('RESEARCH_SOURCE_COMMIT')
    require(type(commit) is str and re.fullmatch('[0-9a-f]{40}',commit) and commit!=prior['sourceCommit'] and
        commit!=prior['resultCommit'],'qualification-source-commit')
    require(os.environ.get('RESEARCH_SUPERVISION_STAGE')=='qualification' and
        os.environ.get('RESEARCH_EXPECTED_MANIFEST_SHA256')==manifest_pin['sha256'] and
        os.environ.get('RESEARCH_SOURCE_MANIFEST_PATH')==str(manifest_path) and
        os.environ.get('RESEARCH_PRIOR_RESULT_MANIFEST_PATH')==str(old_result_manifest) and
        os.environ.get('RESEARCH_PRIOR_RESULT_MANIFEST_SHA256')==prior['resultManifestSha256'] and
        os.environ.get('RESEARCH_PRIOR_SOURCE_COMMIT')==prior['sourceCommit'] and
        os.environ.get('RESEARCH_PRIOR_RESULT_COMMIT')==prior['resultCommit'],'qualification-supervisor-environment')
    attempt_path=results/'qualification-attempt.json'
    attempt=load(attempt_path,65536)
    fields(attempt,('stage','sourceCommit','sourceManifestSha256','configSha256','priorSourceCommit',
        'priorResultCommit','priorResultManifestSha256','launchCutoffUtc','allocation','startedUtc'),'qualification-attempt-fields')
    expected_attempt={'stage':'qualification','sourceCommit':commit,'sourceManifestSha256':manifest_pin['sha256'],
        'configSha256':config_pin['sha256'],'priorSourceCommit':prior['sourceCommit'],
        'priorResultCommit':prior['resultCommit'],'priorResultManifestSha256':prior['resultManifestSha256'],
        'launchCutoffUtc':config['launchCutoffUtc'],'allocation':'sole attempt; existence prevents retry'}
    require(all(same(attempt[k],v) for k,v in expected_attempt.items()) and type(attempt['startedUtc']) is str,
            'qualification-attempt-binding')
    started=datetime.fromisoformat(attempt['startedUtc'].replace('Z','+00:00'))
    cutoff=datetime.fromisoformat(config['launchCutoffUtc'].replace('Z','+00:00'))
    require(started.tzinfo is not None and started.utcoffset()==timezone.utc.utcoffset(started) and started<cutoff,
            'qualification-attempt-cutoff')
    contract=load(package/'source/result-contract.json',1024*1024)
    require(contract.get('schema')=='m31-validator-qualification-contract-v1' and
        same(contract.get('negativeControls'),[{'name':n,'failurePrefixes':p} for n,p in RECIPES.items()]),
        'qualification-contract-recipes')
    return {'config':config,'baseline':baseline,'ownIndex':own_index,'oldIndex':old_index,'resultIndex':result_index,
        'ownRequired':own_required+dependency_required,'oldRequired':dependency_required[:5],'corpusRequired':corpus,
        'manifestPin':manifest_pin,'runtime':runtime,'attemptPin':file_pin(attempt_path,65536),
        'identity':{'sourceCommit':commit,'sourceManifestSha256':manifest_pin['sha256'],
                    'configId':config['id'],'configSha256':config_pin['sha256']}}


def historical_failure(baseline,prior):
    original=frozen.load_artifact(baseline/'results/check.json',REPORT_LIMIT)
    require(original['passed'] is False and original['advancement'] is False and
        original['sourceCommit']==prior['sourceCommit'] and
        original['sourceManifestSha256']==prior['sourceManifestSha256'],'historical-failure-state')
    controls=original['corruptionControls']
    require(len(controls)==20 and sum(row['intendedCoreFailure'] is True for row in controls)==19,
            'historical-control-verdicts')
    failed=next(row for row in controls if row['name']=='false-zero-active-leaf')
    require(failed['executed'] is True and failed['rejected'] is True and failed['intendedCoreFailure'] is False and
        same(failed['errors'],['filter-work-counter-reconstruction']),'historical-interception-verdict')
    for stage,exit_code,success in (('kernel',0,True),('checker',1,False)):
        closure=load(baseline/'results'/f'{stage}-supervision.json',65536)
        require(closure.get('closed') is True and closure.get('exitCode')==exit_code and
            closure.get('success') is success and closure.get('childGroupAbsent') is True and
            closure.get('scientificChildAbsentBeforeRelease') is True and
            closure.get('sourceAndRuntimeRechecked') is True and
            closure.get('sourceCommit')==prior['sourceCommit'] and
            closure.get('sourceManifestSha256')==prior['sourceManifestSha256'],'historical-allocation-closure')
    return {'sourceCommit':prior['sourceCommit'],'resultCommit':prior['resultCommit'],
        'sourceManifestSha256':prior['sourceManifestSha256'],'resultManifestSha256':prior['resultManifestSha256'],
        'checkSha256':prior['checkSha256'],'passed':False,'advancement':False,
        'failedControl':'false-zero-active-leaf','failure':'filter-work-counter-reconstruction'}


def final_gates(state,root,package,manifest_path,results):
    prior=state['config']['prior']
    require(same(verify_sources(manifest_path,root,state['ownRequired']),state['ownIndex']) and
        same(file_pin(manifest_path,1024*1024),state['manifestPin']),'new-source-changed')
    require(same(verify_sources(state['baseline']/'source-manifest.json',root,state['oldRequired']),state['oldIndex']) and
        same(verify_sources(state['baseline']/'result-manifest.json',root,state['corpusRequired']),state['resultIndex']),
        'prior-immutable-closure-changed')
    require(file_pin(state['baseline']/'source-manifest.json',1024*1024)['sha256']==prior['sourceManifestSha256'] and
        file_pin(state['baseline']/'result-manifest.json',1024*1024)['sha256']==prior['resultManifestSha256'],
        'prior-manifest-changed')
    require(same(file_pin(Path(sys.executable).resolve(strict=True),256*1024*1024),state['runtime']['python']) and
        same(file_pin(results/'qualification-attempt.json',65536),state['attemptPin']),'qualification-runtime-or-attempt-changed')


def output_tree(results,ids):
    allowed={'qualification-'+suffix for suffix in ('attempt.json','guardian.jsonl','stdout.log','stderr.log',
        'terminal-error.json','supervision.json')}|{'qualification.json','reference'}
    total=0
    for path in results.iterdir():
        require(not path.is_symlink() and path.name in allowed,'qualification-output-closed-set')
        if path.name=='reference':
            require(path.is_dir(),'qualification-reference-directory')
            for child in path.iterdir():
                require(child.is_file() and not child.is_symlink() and child.name in {i+'.json' for i in ids},
                        'qualification-reference-closed-set')
                require(child.stat().st_size<=SCENE_LIMIT,'qualification-reference-budget')
                total+=child.stat().st_size
        else:
            require(path.is_file(),'qualification-output-file')
            if path.name=='qualification.json':
                require(path.stat().st_size<=REPORT_LIMIT,'qualification-report-budget')
                total+=path.stat().st_size
    require(total<=CHECKER_LIMIT,'qualification-total-output-budget')


def main(argv=None):
    global frozen
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',required=True)
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--root',required=True)
    args=parser.parse_args(argv)
    root=Path(args.root).resolve(strict=True)
    config_path=Path(args.config).resolve(strict=True)
    qualification_package=config_path.parent.parent
    qualification_manifest_path=Path(args.manifest).resolve(strict=True)
    output_results=qualification_package/'results'
    output_path=Path(args.output).absolute()
    require(config_path==qualification_package/'source/config.json' and
        qualification_manifest_path==qualification_package/'source-manifest.json' and
        output_path==output_results/'qualification.json' and not output_path.exists(),'qualification-fixed-paths')
    report={'schema':'m31-validator-qualification-v1','passed':False,'exposedCorpusQualificationPassed':False,
        'historicalOriginalPassed':False,'historicalOriginalAdvancement':False,'transferAuthorized':False,
        'freshReplication':False,'recordIntegrityPassed':False,'denominator':6,
        'counts':{'reached':0,'independentlyVerified':0,'modelAdmitted':0,'certified':0},
        'outcomes':[],'generations':[],'corruptionControls':[],'fixedControlsPassed':False,
        'nontriviality':{'informative':False,'runs':[]},'referenceFiles':[],'errors':[],
        'scope':'Qualification of previously exposed immutable saved evidence; no retroactive pass, fresh replication or transfer.'}
    completed={}
    used=0
    helper=semantic=None
    state=None
    try:
        state=gates(root,qualification_package,config_path,qualification_manifest_path,output_results)
        configured_prior=state['config']['prior']
        report['validationIdentity']=state['identity']
        report['qualificationRuntimePins']=state['runtime']
        report.update({key:state['identity'][key] for key in ('sourceCommit','sourceManifestSha256','configSha256')})
        report.update(priorSourceCommit=configured_prior['sourceCommit'],priorResultCommit=configured_prior['resultCommit'],
            priorResultManifestSha256=configured_prior['resultManifestSha256'])
        package=state['baseline']
        source=package/'source'
        results=package/'results'
        input_path=results/'index.json'
        manifest_path=package/'source-manifest.json'
        indexed=state['oldIndex']
        manifest_pin=file_pin(manifest_path,1024*1024)
        frozen=independent_module(source/'check.py',root,indexed,'m31_frozen_saved_checker',FROZEN_CHECKER_SHA)
        report['historicalOutcome']=historical_failure(package,configured_prior)
        required=[source/name for name in frozen.SOURCE_FILES]+[root/name for name in frozen.GENERATOR_FILES]+[
            package/'runtime-pins.json',package/'PROTOCOL.md',package/'RECORD-CONTRACT.md']
        require(same(verify_sources(manifest_path,root,required),indexed),'prior-source-required-closure')
        config=frozen.load(source/'config.json',SOURCE_LIMIT)
        config_pin=file_pin(source/'config.json',SOURCE_LIMIT)
        frozen.validate_config(config)
        runtime_pins = frozen.load(package / 'runtime-pins.json', 65536)
        frozen.fields(runtime_pins, ('node', 'python'), 'runtime-pins-fields')
        frozen.require(frozen.same(frozen.file_pin(Path(sys.executable).resolve(strict=True), 256 * 1024 * 1024), runtime_pins['python']), 'python-runtime-pin')
        (document, input_pin) = frozen.load_artifact(input_path, frozen.INDEX_LIMIT, with_pin=True)
        frozen.fields(document, ('schema', *frozen.IDENTITY, 'sourceSha256', 'constants', 'controls', 'generations', 'scheduled', 'completion', 'error'), 'index-fields')
        frozen.require(document['schema'] == 'm31-moving-admission-index-v1' and document['configId'] == config['id'] and (document['configSha256'] == config_pin['sha256']) and (document['sourceManifestSha256'] == manifest_pin['sha256']), 'index-source-config-binding')
        frozen.require(type(document['sourceCommit']) is str and re.fullmatch('[0-9a-f]{40}', document['sourceCommit']), 'source-commit-shape')
        require(document['sourceCommit']==configured_prior['sourceCommit'],'prior-index-source-commit')
        frozen.fields(document['runtime'], ('node', 'platform', 'arch', 'executableSha256'), 'runtime-fields')
        frozen.require(document['runtime']['node'] == 'v24.19.0' and document['runtime']['platform'] == 'darwin' and (document['runtime']['arch'] == 'arm64') and (document['runtime']['executableSha256'] == runtime_pins['node']['sha256']), 'runtime-identity')
        for stage in ('kernel', 'checker'):
            frozen.verify_attempt(results / f'{stage}-attempt.json', stage, document, config)
        candidate_paths = [frozen.relative(source / name, root) for name in frozen.CANDIDATE_FILES] + list(frozen.GENERATOR_FILES)
        source_hashes = {name: indexed[name]['sha256'] for name in candidate_paths}
        generator_hashes = {name: indexed[name]['sha256'] for name in frozen.GENERATOR_FILES}
        frozen.bind_sources(document, source_hashes)
        frozen.schedule_shape(document['scheduled'])
        frozen.fields(document['completion'], ('status', 'stage', 'methodCalls', 'generationRuns', 'reachedScheduled', 'missingScheduled'), 'completion-fields')
        frozen.require(document['completion']['status'] == 'complete' and document['completion']['stage'] == 'complete' and (document['error'] is None), 'kernel-incomplete-or-programming-error')
        frozen.require(type(document['controls']) is list and len(document['controls']) == 4 and (type(document['generations']) is list) and (len(document['generations']) == 2), 'allocation-record-counts')
        frozen.require(all((slot['status'] in ('evaluated', 'not-reached') for slot in document['scheduled'])), 'scheduled-incomplete-or-programming-error')
        pins = {frozen.relative(input_path, root): input_pin, frozen.relative(results / 'kernel-journal.jsonl', root): frozen.file_pin(results / 'kernel-journal.jsonl', frozen.JOURNAL_LIMIT)}
        input_pin = pins[frozen.relative(input_path, root)]
        scientific_names = {f'controls/{name}.json' for name in frozen.CONTROL_IDS} | {f'generation/{name}.json' for name in frozen.RUN_IDS} | {f"scenes/{slot['id']}.json" for slot in document['scheduled'] if slot['status'] == 'evaluated'}
        frozen.check_result_tree(results, scientific_names)
        refdir = output_results / 'reference'
        frozen.require(not refdir.exists() or (refdir.is_dir() and (not refdir.is_symlink()) and (not any(refdir.iterdir()))), 'qualification-reference-directory-not-empty')
        refdir.mkdir(exist_ok=True)
        helper = frozen.independent_module(source / 'pair-reference.py', root, indexed, 'm31_pair_reference', PAIR_SHA)
        semantic = frozen.independent_module(source / 'semantic-reference.py', root, indexed, 'm31_semantic_reference', SEMANTIC_SHA)
        spec = frozen.load(source / 'spec.json', SOURCE_LIMIT)
        frozen.check_spec(spec)
        (bits, _trace) = helper.constants_from_graph(spec)
        constants = {name: helper.dyadic(word) for (name, word) in bits.items()}
        frozen.require(frozen.same(document['constants'], {name: helper.hex_bits(word) for (name, word) in bits.items()}), 'constant-operation-graph')
        frozen.metadata_controls(document, source_hashes, completed)
        report['priorRuntime'] = document['runtime']
        generations = {}
        for (case, desc) in zip(config['cases'], document['generations']):
            name = frozen.relative(results / 'generation' / f"{case['id']}.json", root)
            frozen.require(desc['path'] == name, 'generation-descriptor-path')
            path = root / name
            (gen, loaded_pin) = frozen.load_artifact(path, frozen.GENERATION_LIMIT, with_pin=True)
            generation_evidence = frozen.validate_generation(gen, desc, case, config, document, generator_hashes)
            frozen.require(type(desc['bytes']) is int and desc['bytes'] == loaded_pin['bytes'] and (desc['sha256'] == loaded_pin['sha256']), 'generation-buffer-pin')
            pins[name] = loaded_pin
            generations[case['id']] = gen
            report['generations'].append(generation_evidence)
        reached = sum((len(row['reachedTimes']) for row in report['generations']))
        frozen.require(reached == 6, 'fixed-exposed-corpus-all-six-reached')
        missing = 6 - reached
        expected_completion = {'status': 'complete', 'stage': 'complete', 'methodCalls': 4 + reached, 'generationRuns': 2, 'reachedScheduled': reached, 'missingScheduled': missing}
        frozen.require(frozen.same(document['completion'], expected_completion), 'completion-reconstruction')
        report['counts']['reached'] = reached
        initial = generations['run-a']['slots'][0]['input']
        changed = {'input': copy.deepcopy(initial)}
        changed['input']['drones'][0]['state'][0] = helper.hex_bits(helper.parse_bits(changed['input']['drones'][0]['state'][0]) ^ 1)
        run_mutation('capture-record-disagreement', {'scene': 'run-a-t0', 'id': 0, 'stateIndex': 0}, lambda : frozen.same_capture(changed, initial), completed, (frozen.CheckError,))
        changed_frame = copy.deepcopy(generations['run-a']['frames'][0])
        changed_frame['words'][0] = helper.hex_bits(helper.parse_bits(changed_frame['words'][0]) ^ 1)
        run_mutation('pose-capture-disagreement', {'scene': 'run-a-t0', 'id': 0, 'poseIndex': 0}, lambda : frozen.pose_capture(changed_frame, initial), completed, (frozen.CheckError,))
        prior = (0, 0)
        samples = {}
        fixed_ok = []
        jobs = []
        for (ci, (control, desc)) in enumerate(zip(config['controls'], document['controls'])):
            expected = {'drones': [{'id': d['id'], 'state': [helper.hex_bits(helper.literal(v)) for v in d['state']]} for d in control['drones']]}
            jobs.append((control['id'], 'control', desc, expected, {'type': 'control', 'controlIndex': ci}, control['expected']))
        for (si, slot) in enumerate(document['scheduled']):
            gen = generations[slot['runId']]
            gd = document['generations'][si // 3]
            capture = gen['slots'][si % 3]
            frozen.require(slot['generationSha256'] == gd['sha256'], 'scheduled-generation-digest')
            if capture['status'] == 'not-reached':
                frozen.require(slot['status'] == 'not-reached' and slot['reason'] == capture['reason'] and (slot['inputSha256'] is None) and (slot['record'] is None), 'scheduled-missing-binding')
                report['outcomes'].append({'id': slot['id'], 'kind': 'scheduled', 'status': 'not-reached', 'reason': slot['reason'], 'verified': False, 'modelAdmitted': False, 'certified': False})
                continue
            frozen.require(slot['status'] == 'evaluated' and slot['reason'] is None and (slot['inputSha256'] == frozen.input_hash(slot['id'], capture['input'])), 'scheduled-reached-binding')
            cap = {'type': 'generation-slot', 'runId': slot['runId'], 'generationSha256': gd['sha256'], 'slotIndex': si % 3, 't': slot['t']}
            jobs.append((slot['id'], 'scheduled', slot['record'], capture['input'], cap, None))
        for (identifier, kind, desc, captured, capture, expected_result) in jobs:
            path = results / ('controls' if kind == 'control' else 'scenes') / (identifier + '.json')
            name = frozen.relative(path, root)
            (record, loaded_pin) = frozen.load_artifact(path, SCENE_LIMIT, scientific=True, with_pin=True)
            frozen.fields(record, ('id', 'kind', 'input', 'method', 'error'), 'method-record-fields')
            frozen.require(record['id'] == identifier and record['kind'] == kind and (record['error'] is None) and (type(record['method']) is dict), 'method-record-identity-or-error')
            frozen.raw_input(record['input'], len(captured['drones']))
            if kind == 'control':
                frozen.fixed_input(record, captured)
                if identifier == 'positive':
                    clone = {'input': copy.deepcopy(captured)}
                    clone['input']['drones'][0]['state'][0] = helper.hex_bits(helper.parse_bits(clone['input']['drones'][0]['state'][0]) ^ 1)
                    run_mutation('altered-control-input', {'scene': identifier, 'id': 0, 'stateIndex': 0}, lambda : frozen.fixed_input(clone, captured), completed, (frozen.CheckError,))
            else:
                frozen.same_capture(record, captured)
            prior = frozen.descriptor_shape(desc, identifier, kind, name, captured, capture, prior)
            frozen.require(type(desc['bytes']) is int and desc['bytes'] == loaded_pin['bytes'] and (desc['sha256'] == loaded_pin['sha256']), 'method-buffer-pin')
            pins[name] = loaded_pin
            target = frozen.regenerate(identifier, captured, spec, bits, helper, semantic)
            frozen.require(len(desc['call']['phases']) == (1 if target['globalInvalid'] else 3), 'call-phase-completion')
            graph = frozen.graph_evidence(target)
            evidence = {}
            verified = False
            errors = []
            cause = None
            try:
                (evidence, _) = frozen.validate_filter_method(record['method'], target, 'filtered', constants, helper, semantic, True)
                verified = True
            except (frozen.CheckError, semantic.CheckError, helper.CheckError) as failure:
                errors = [str(failure)[:256]]
                candidate_status = record['method'].get('result', {}).get('status')
                cause = 'reference-undecidable' if target['status'] == 'reference-undecidable' else 'unvalidated-numerical-refusal-or-status-gap' if candidate_status == 'unresolved' else 'scientific-record-integrity-failure'
            result = record['method'].get('result', {})
            admitted = verified and target['status'] == 'admitted'
            certified = admitted and evidence.get('toleranceAchieved') is True
            outcome = {'id': identifier, 'kind': kind, 'verified': verified, 'modelAdmitted': admitted, 'certified': certified, 'status': result.get('status'), 'branch': result.get('branch'), 'witness': result.get('witness'), 'referenceStatus': target['status'], 'referenceBranch': target['branch'], 'graph': graph, 'cause': cause, 'errors': errors, 'evidence': evidence}
            reference = frozen.scene_reference(identifier, target, graph, evidence, semantic)
            reference.update(schema='m31-validator-qualification-reference-v1', qualificationSourceCommit=state['identity']['sourceCommit'], priorSourceCommit=configured_prior['sourceCommit'], inputSha256=desc['inputSha256'])
            refpath = refdir / (identifier + '.json')
            pin = frozen.write_exclusive(refpath, reference, min(SCENE_LIMIT, CHECKER_LIMIT - REPORT_LIMIT - used))
            used += pin['bytes']
            report['referenceFiles'].append({'id': identifier, 'path': frozen.relative(refpath, root), **pin})
            report['outcomes'].append(outcome)
            if kind == 'control':
                matches = verified and result.get('status') == expected_result['status'] and (result.get('branch') == expected_result['branch'])
                fixed_ok.append(matches)
                if matches:
                    method_controls(record, target, semantic, helper, constants, completed)
            else:
                report['counts']['independentlyVerified'] += int(verified)
                report['counts']['modelAdmitted'] += int(admitted)
                report['counts']['certified'] += int(certified)
                samples[identifier] = frozen.nontrivial_sample(target, graph, verified, helper)
            del target, record, reference, evidence
        frozen.require(prior[0] == 4 + reached, 'total-method-call-count')
        journal_document = dict(document, _indexPath=frozen.relative(input_path, root))
        report['journal'] = frozen.check_journal(results / 'kernel-journal.jsonl', journal_document, config, input_pin)
        report['fixedControlsPassed'] = len(fixed_ok) == 4 and all(fixed_ok)
        report['nontriviality'] = frozen.nontriviality(samples)
        for name in RECIPES:
            if name not in completed:
                completed[name] = {'name': name, 'executed': False, 'rejected': False, 'intendedCoreFailure': False, 'requiredFailureFamilies': RECIPES[name], 'witness': None, 'errors': ['preregistered-witness-unavailable']}
        report['corruptionControls'] = [completed[name] for name in RECIPES]
        corruption_ok = all((row['executed'] and row['intendedCoreFailure'] for row in report['corruptionControls']))
        frozen.require(sum((pin['bytes'] for pin in pins.values())) <= 192 * 1024 * 1024, 'kernel-scientific-output-budget')
        for (name, pin) in pins.items():
            frozen.require(frozen.same(frozen.file_pin(root / name, max(SCENE_LIMIT, frozen.GENERATION_LIMIT)), pin), 'evidence-changed-during-check')
        frozen.require(frozen.same(frozen.verify_sources(manifest_path, root, required), indexed) and frozen.same(frozen.file_pin(manifest_path, 1024 * 1024), manifest_pin), 'source-changed-during-check')
        frozen.require(frozen.same(frozen.file_pin(Path(sys.executable).resolve(strict=True), 256 * 1024 * 1024), runtime_pins['python']), 'python-runtime-changed')
        frozen.check_result_tree(results, scientific_names)
        report['inputPins'] = [{'path': name, **pin} for (name, pin) in sorted(pins.items())]
        report['conditionalLoadValidation'] = {'denominator': report['counts']['modelAdmitted'], 'allFourTolerancesCertified': report['counts']['certified']}
        report['recordIntegrityPassed'] = report['fixedControlsPassed'] and corruption_ok and (report['counts']['independentlyVerified'] == reached)
        report['passed'] = report['recordIntegrityPassed'] and reached == 6 and (report['counts']['independentlyVerified'] == 6) and (report['counts']['certified'] == 6) and report['nontriviality']['informative']
        frozen.require(len(completed) == 21 and len(report['outcomes']) == 10, 'qualification-fixed-operation-counts')
        report['exposedCorpusQualificationPassed'] = report['passed']
        final_gates(state, root, qualification_package, qualification_manifest_path, output_results)
        output_tree(output_results, state['config']['referenceIds'])
        if not report['passed']:
            report['errors'].append('exposed-corpus-qualification-failed')
    except Exception as failure:
        known=(CheckError,)+(tuple([frozen.CheckError]) if frozen else ())+(tuple([semantic.CheckError]) if semantic else ())+(tuple([helper.CheckError]) if helper else ())
        code=str(failure)[:256] if isinstance(failure,known) else 'qualification-error:'+type(failure).__name__
        report['errors'].append(code)
        report['passed']=False
        report['exposedCorpusQualificationPassed']=False
        report['corruptionControls']=[completed[name] for name in RECIPES if name in completed]
    require(not output_path.exists(),'qualification-report-existing')
    write_exclusive(output_path,report,min(REPORT_LIMIT,CHECKER_LIMIT-used))
    output_tree(output_results,EXPECTED_CONFIG['referenceIds'])
    print(json.dumps({'passed':report['passed'],'exposedCorpusQualificationPassed':report['exposedCorpusQualificationPassed'],
        'historicalOriginalPassed':False,'transferAuthorized':False,'errors':report['errors']},sort_keys=True))
    return 0 if report['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
