"""Saved-only independent witness-layout comparison; never a scientific audit."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import importlib.util
import json
import math
import os
import re
import struct
import sys
import time

PACKAGE = 'research/m31-tree-witness-layout-2026-10-17'
OLD = 'research/m31-native-tree-browser-probe-2026-10-17'
DECODER = OLD+'/source/compact-check.py'
DECODER_SHA = '87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee'
MAX_FILE, MAX_TOTAL = 32*1024**2, 64*1024**2
HEX = re.compile(r'^[0-9a-f]{16}$')


def need(value, code):
    if not value: raise ValueError(code)


def fields(value, names, code):
    need(type(value) is dict and set(value) == set(names), code)


def integer(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def sha(raw): return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    out = {}
    for key,value in pairs:
        need(key not in out,'duplicate-json-key'); out[key] = value
    return out


def decode(raw):
    return json.loads(raw,object_pairs_hook=unique,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite-json')))


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()


def path_at(root, relative):
    need(type(relative) is str and relative and not Path(relative).is_absolute()
         and all(p not in ('','.','..') for p in relative.split('/')),'relative-path')
    path = root/relative; need(path.resolve() == path,'symlink-path'); return path


def read_pin(root, pin):
    fields(pin,('path','bytes','sha256'),'pin-fields')
    integer(pin['bytes'],0,MAX_FILE,'pin-byte-cap')
    path = path_at(root,pin['path']); need(path.stat().st_size == pin['bytes'],'pin-size')
    raw = path.read_bytes(); need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'],'pin-bytes')
    return raw


def guard(ctx):
    need(time.monotonic_ns() < (ctx['deadline'] if ctx.get('closing') else ctx['computeDeadline']), 'checker-deadline')
    need(datetime.now(timezone.utc) < ctx['cutoff'],'authorization-cutoff')


def exact_equal(a,b):
    if a is b: return True
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(exact_equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a) == len(b) and all(exact_equal(x,y) for x,y in zip(a,b))
    if type(a) is float: return struct.pack('>d',a) == struct.pack('>d',b)
    return a == b


def preflight(root, expected, commit):
    package = root/PACKAGE; raw = (package/'source-manifest.json').read_bytes()
    need(len(raw) <= MAX_FILE and sha(raw) == expected,'manifest-binding')
    manifest = decode(raw); pins = {p['path']:p for p in manifest['files']}
    need(len(pins) == len(manifest['files']),'manifest-unique-pins')
    config = decode(read_pin(root,pins[PACKAGE+'/config.json']))
    need(config['schema'] == 'm31-tree-witness-layout-supervision-v1' and config['executionAllowed'] is True,
         'execution-not-authorized')
    need(config['stageOrder'] == ['candidate','check']
         and config['limits'] == {'totalWallSeconds':300,'closureAndOverheadSeconds':60,'perFileBytes':MAX_FILE,
             'combinedOutputLogScratchBytes':MAX_TOTAL,'evidenceBytes':56*1024**2,'privateBytes':4*1024**2,
             'otherPublicBytes':2*1024**2,'finalizationByteAllowance':2*1024**2,'chunkBytes':1024**2,'pollSeconds':0.1}
         and all(config['stages'][k]['childWallSeconds'] == 120 for k in ('candidate','check')),'fixed-envelope')
    auth = config['authorization']; need(type(auth) is dict and auth.get('id'),'authorization')
    cutoff = datetime.fromisoformat(config['launchCutoffUtc'])
    need(datetime.fromisoformat(auth['approvedUtc']) <= datetime.now(timezone.utc) < cutoff,'authorization-time')
    need(os.environ.get('RESEARCH_STAGE') == 'check'
         and os.environ.get('RESEARCH_CHILD_BUDGET_MILLISECONDS') == '120000'
         and os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated','supervised-checker')
    token = os.environ.get('RESEARCH_RUN_TOKEN',''); need(len(token) == 64,'run-token')
    attempt = decode((package/'results/run-attempt.json').read_bytes())
    need(attempt['schema'] == 'm31-tree-witness-layout-attempt-v1' and attempt['status'] == 'running'
         and attempt['sourceCommit'] == commit and attempt['sourceManifestSha256'] == expected
         and attempt['runTokenSha256'] == sha(token.encode()) and attempt['stages']['check']['status'] == 'started'
         and attempt['stages']['check']['childWallLimitSeconds'] == 120,
         'live-attempt')
    deadline = int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS'])
    ctx = {'root':root,'package':package,'manifest':manifest,'pins':pins,'expected':expected,'commit':commit,
           'cutoff':cutoff,'deadline':deadline,'computeDeadline':deadline-10_000_000_000,'protected':[]}
    guard(ctx)
    for pin in manifest['files']: guard(ctx); read_pin(root,pin)
    need(pins[DECODER]['sha256'] == DECODER_SHA,'frozen-pure-decoder')
    receipt_raw = (package/'source-publication.json').read_bytes(); receipt = decode(receipt_raw)
    need(receipt['commit'] == commit and receipt['manifestSha256'] == expected
         and receipt['manifestPath'] == PACKAGE+'/source-manifest.json' and receipt['manifestBytes'] == len(raw)
         and receipt['verifiedFilePins'] == len(manifest['files'])
         and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True
         and datetime.fromisoformat(receipt['verifiedUtc'].replace('Z','+00:00')) <=
             datetime.fromisoformat(attempt['startedUtc'].replace('Z','+00:00')),'publication-before-attempt')
    ctx['protected'] += [
        {'path':PACKAGE+'/source-manifest.json','bytes':len(raw),'sha256':sha(raw)},
        {'path':PACKAGE+'/source-publication.json','bytes':len(receipt_raw),'sha256':sha(receipt_raw)}]
    runtime = manifest['runtime']['python']; binary = Path(sys.executable).resolve().read_bytes()
    need(sys.platform == 'darwin' and sys.flags.isolated == 1 and sys.dont_write_bytecode
         and sys.version == runtime['version'] and len(binary) == runtime['bytes'] and sha(binary) == runtime['sha256'],
         'pinned-isolated-python')
    stage = attempt['stages']['candidate']; need(stage['status'] == 'completed' and stage['exitCode'] == 0,'candidate-closed')
    pin = dict(stage['output'],path=PACKAGE+'/results/candidate.json')
    candidate = decode(read_pin(root,pin)); ctx['protected'].append(pin)
    need(candidate['complete'] is True and candidate['passed'] is True and candidate['sourceCommit'] == commit
         and candidate['sourceManifestSha256'] == expected,'candidate-index-binding')
    return ctx,candidate


class TransportSupport:
    def __init__(self, package): self.PACKAGE = package
    fields = staticmethod(fields); integer = staticmethod(integer); need = staticmethod(need)
    read_pin = staticmethod(read_pin); decode = staticmethod(decode); guard = staticmethod(guard)


def decoder(ctx):
    spec = importlib.util.spec_from_file_location('_frozen_lossless_reader',ctx['root']/DECODER)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def old_sequence(value,n):
    if value is None: return None
    fields(value,('kind','data'),'old-gather-fields'); data = value['data']
    need(type(data) is list and len(data) <= 2*n,'old-gather-size')
    if value['kind'] == 'literal': actual = list(data)
    else:
        need(value['kind'] == 'runs' and len(data)%2 == 0,'old-run-shape'); actual = []; end = -1
        for start,count in zip(data[::2],data[1::2]):
            integer(start,0,n-1,'old-run-start'); integer(count,1,n,'old-run-length')
            need(start > end and start+count <= n,'old-run-order'); end = start+count
            actual.extend(range(start,end))
    previous = -1
    for index in actual:
        integer(index,0,n-1,'old-index-range'); need(index > previous,'old-index-order'); previous = index
    runs = sum(i == 0 or actual[i] != actual[i-1]+1 for i in range(len(actual)))
    need(value['kind'] == ('runs' if 2*runs < len(actual) else 'literal'),'old-gather-canonical')
    return actual


def new_sequence(value,n):
    if value is None: return None,None
    fields(value,('kind','count','data'),'layout-gather-fields')
    count = integer(value['count'],0,n,'layout-gather-count'); data = value['data']; kind = value['kind']
    need(type(data) is list and len(data) <= 2*n,'layout-gather-size')
    if kind == 'literal':
        actual = list(data)
    elif kind == 'runs':
        need(len(data)%2 == 0,'layout-run-width'); actual = []; previous_end = -1
        for start,length in zip(data[::2],data[1::2]):
            integer(start,0,n-1,'layout-run-start'); integer(length,1,n,'layout-run-length')
            need(start > previous_end and start+length <= n,'layout-run-order'); previous_end = start+length
            actual.extend(range(start,previous_end))
    else:
        need(kind == 'bitmap','layout-gather-kind')
        need(len(data) == (n+63)//64,'layout-bitmap-width'); actual = []
        for block,word in enumerate(data):
            need(type(word) is str and HEX.fullmatch(word),'layout-bitmap-word')
            bits = int(word,16); valid = min(64,n-64*block)
            need(bits >> valid == 0,'layout-bitmap-padding')
            while bits:
                low = bits & -bits; actual.append(64*block+low.bit_length()-1); bits ^= low
    need(len(actual) == count,'layout-gather-cardinality'); previous = -1
    for index in actual:
        integer(index,0,n-1,'layout-index-range'); need(index > previous,'layout-index-order'); previous = index
    runs = sum(i == 0 or actual[i] != actual[i-1]+1 for i in range(len(actual)))
    costs = {'literal':59+4*count,'runs':56+8*runs,'bitmap':58+8*((n+63)//64)}
    choice = min(('literal','runs','bitmap'),key=lambda k:(costs[k],('literal','runs','bitmap').index(k)))
    need(kind == choice,'layout-gather-canonical-cost')
    return actual,kind


def compare_tree(old,new,poll=lambda:None):
    if old is None:
        need(new is None,'layout-null-preserved'); return {'receivers':0,'culls':0,'gathered':0,'encodings':{}}
    fields(new,('schema','base','receiverIds','cullOffsets','cullCodes','cullDifferences','leavesRefs','gathered'),'layout-fields')
    need(new['schema'] == 'm31-tree-witness-columns-v1','layout-schema')
    need(type(old) is dict and old['schema'] == 'm31-native-center-tree-compact-v1','old-compact-schema')
    need(exact_equal(new['base'],{k:v for k,v in old.items() if k != 'receivers'}),'layout-base-equality')
    n = integer(old['n'],0,5000,'layout-n'); rows = old['receivers']; count = len(rows)
    for key in ('receiverIds','cullOffsets','cullCodes','cullDifferences','leavesRefs','gathered'):
        need(type(new[key]) is list,'layout-column-array')
    need(len(new['receiverIds']) == len(new['leavesRefs']) == len(new['gathered']) == count
         and len(new['cullOffsets']) == count+1,'layout-column-count')
    offsets,codes,differences = new['cullOffsets'],new['cullCodes'],new['cullDifferences']
    need(len(codes) == len(differences) and offsets[0] == 0 and offsets[-1] == len(codes),'layout-offset-endpoints')
    previous = 0
    for offset in offsets:
        integer(offset,0,len(codes),'layout-offset-range'); need(offset >= previous,'layout-offset-order'); previous = offset
    report = {'receivers':count,'culls':len(codes),'gathered':0,'encodings':{}}
    for i,row in enumerate(rows):
        poll(); fields(row,('receiver','culled','leavesRef','gathered'),'old-receiver-fields')
        integer(new['receiverIds'][i],0,max(0,n-1),'layout-receiver-range')
        need(exact_equal(new['receiverIds'][i],row['receiver']),'layout-receiver-order')
        ref = new['leavesRefs'][i]
        if ref is not None: integer(ref,0,len(old['leafDictionary'])-1,'layout-leaf-reference')
        need(exact_equal(ref,row['leavesRef']),'layout-leaf-equality')
        old_values = old_sequence(row['gathered'],n); actual,kind = new_sequence(new['gathered'][i],n)
        need(exact_equal(old_values,actual),'layout-gathered-equality')
        if actual is not None:
            report['gathered'] += len(actual); report['encodings'][kind] = report['encodings'].get(kind,0)+1
        lo,hi = offsets[i:i+2]
        need(hi-lo == len(row['culled']),'layout-cull-count')
        previous_node = -1
        for at,old_cull in zip(range(lo,hi),row['culled']):
            code = integer(codes[at],0,0xffffffff,'layout-cull-code'); node,which = divmod(code,6)
            need(node < len(old['nodes']),'layout-cull-node-range')
            need(node > previous_node,'layout-cull-order'); previous_node = node
            word = differences[at]; need(type(word) is str and HEX.fullmatch(word),'layout-cull-difference-word')
            decoded = {'node':node,'axis':which//2,'side':'min-ge4' if which%2 == 0 else 'max-le-neg4','difference':word}
            need(exact_equal(decoded,old_cull),'layout-cull-equality')
    return report


def controls():
    base = {'schema':'m31-native-center-tree-compact-v1','n':65,'nodes':[{'id':i} for i in range(6)],
            'leafDictionary':[[0],[1],[2]],'literalZero':'8000000000000000'}
    old = dict(base,receivers=[
        {'receiver':0,'culled':[{'node':2,'axis':1,'side':'min-ge4','difference':'4010000000000000'},
                              {'node':5,'axis':0,'side':'min-ge4','difference':'4010000000000000'}],
         'leavesRef':0,'gathered':{'kind':'literal','data':[0]}},
        {'receiver':1,'culled':[{'node':3,'axis':2,'side':'max-le-neg4','difference':'c010000000000000'}],
         'leavesRef':1,'gathered':{'kind':'runs','data':[0,10]}},
        {'receiver':2,'culled':[{'node':4,'axis':0,'side':'min-ge4','difference':'8000000000000000'}],
         'leavesRef':2,'gathered':{'kind':'literal','data':list(range(0,20,2))}}])
    good = {'schema':'m31-tree-witness-columns-v1','base':base,'receiverIds':[0,1,2],
            'cullOffsets':[0,2,3,4],'cullCodes':[14,30,23,24],
            'cullDifferences':['4010000000000000','4010000000000000','c010000000000000','8000000000000000'],
            'leavesRefs':[0,1,2],'gathered':[{'kind':'literal','count':1,'data':[0]},
                {'kind':'runs','count':10,'data':[0,10]},
                {'kind':'bitmap','count':10,'data':['0000000000055555','0000000000000000']}]}
    compare_tree(old,good); out = [{'id':'fixed-three-encodings-and-literal-zero','status':'preserved'}]
    mutations = (
        ('noncanonical-choice','layout-gather-canonical-cost'),('padding','layout-bitmap-padding'),
        ('offset-end','layout-offset-endpoints'),('offset-order','layout-offset-order'),
        ('cull-code','layout-cull-equality'),('difference-word','layout-cull-equality'),
        ('receiver-order','layout-receiver-order'),('gather-order','layout-index-order'),
        ('gather-count','layout-gather-cardinality'),('leaf-reference','layout-leaf-reference'),
        ('unknown-field','layout-fields'),('base-literal-word','layout-base-equality'),
        ('cull-order','layout-cull-order'),('run-overlap','layout-run-order'),
        ('bitmap-width','layout-bitmap-width'),('boolean-id','layout-receiver-range'))
    for name,expected in mutations:
        bad = copy.deepcopy(good)
        if name == 'noncanonical-choice': bad['gathered'][1] = {'kind':'literal','count':10,'data':list(range(10))}
        elif name == 'padding': bad['gathered'][2]['data'][1] = '8000000000000000'
        elif name == 'offset-end': bad['cullOffsets'][-1] = 3
        elif name == 'offset-order': bad['cullOffsets'] = [0,3,2,4]
        elif name == 'cull-code': bad['cullCodes'][0] += 1
        elif name == 'difference-word': bad['cullDifferences'][3] = '0000000000000000'
        elif name == 'receiver-order': bad['receiverIds'][:2] = [1,0]
        elif name == 'gather-order': bad['gathered'][0] = {'kind':'literal','count':2,'data':[1,0]}
        elif name == 'gather-count': bad['gathered'][0]['count'] = 0
        elif name == 'leaf-reference': bad['leavesRefs'][0] = 3
        elif name == 'unknown-field': bad['extra'] = True
        elif name == 'cull-order': bad['cullCodes'][1] = 14
        elif name == 'run-overlap': bad['gathered'][1]['data'] = [0,5,4,5]
        elif name == 'bitmap-width': bad['gathered'][2]['data'].pop()
        elif name == 'boolean-id': bad['receiverIds'][0] = False
        else: bad['base']['literalZero'] = '0000000000000000'
        try: compare_tree(old,bad)
        except ValueError as error:
            need(str(error) == expected,'control-wrong-rejection:'+name)
            out.append({'id':name,'status':'rejected','reason':expected})
        else: raise ValueError('control-not-rejected:'+name)
    return out


def output(ctx, result):
    ctx['closing'] = True
    for pin in ctx['manifest']['files']+ctx['protected']:
        guard(ctx); read_pin(ctx['root'],pin)
    result['sourceAndInputPinsPreserved'] = True
    raw = canonical(result)+b'\n'; need(len(raw) <= 2*1024**2,'report-file-cap')
    total = evidence = private = public = 0
    for part,base in enumerate((ctx['package']/'results',Path(os.environ['RESEARCH_PRIVATE_LOG_DIR']))):
        for path in base.rglob('*'):
            guard(ctx); need(not path.is_symlink(),'output-symlink')
            if path.is_file():
                size = path.stat().st_size; need(size <= MAX_FILE,'output-file-cap'); total += size
                if part: private += size
                elif path.relative_to(base).parts[0] in ('shards','records'): evidence += size
                elif path.name not in ('run-attempt.json','run-attempt.json.tmp'): public += size
    need(evidence <= 56*1024**2 and private <= 4*1024**2 and public+len(raw) <= 2*1024**2,'output-partition-cap')
    need(total+len(raw)+2*1024**2 <= MAX_TOTAL,'combined-output-cap')
    path = ctx['package']/'results/check.json'
    with path.open('xb') as stream: stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    directory = os.open(path.parent,os.O_RDONLY)
    try: os.fsync(directory)
    finally: os.close(directory)


def input_records(ctx):
    index_pin = ctx['pins'][PACKAGE+'/input-index.json']
    index = decode(read_pin(ctx['root'],index_pin))
    fields(index,('schema','sourcePackage','savedTransportPin','browserJournalPin','sourceAttemptPin','records'),'input-index-fields')
    need(index['schema'] == 'm31-tree-witness-layout-inputs-v1' and index['sourcePackage'] == OLD,'input-index-schema')
    expected_anchors = {
        'savedTransportPin':('saved-transport.json','b5245538e86c9f2a657205ce6177c90702e0c27bf22e247d44db5e63fe6900c7'),
        'browserJournalPin':('browser-journal.jsonl','e66b7234016d9851ce0dbc078e80e97c88dd2bbe8ed139db234b46c5d1eaa173'),
        'sourceAttemptPin':('run-attempt.json','ccae2f966e131fe4a4c78640f3268722025060f885138242efa90e32962abc36')}
    bodies = {}
    for key,(filename,digest) in expected_anchors.items():
        pin = index[key]
        need(pin['path'] == OLD+'/results/'+filename and pin['sha256'] == digest
             and pin == ctx['pins'][pin['path']],'fixed-input-anchor')
        raw = read_pin(ctx['root'],pin)
        bodies[key] = [decode(line) for line in raw.splitlines()] if key == 'browserJournalPin' else decode(raw)
    attempt = bodies['sourceAttemptPin']
    need(attempt['status'] == 'failed' and attempt['sourceCommit'] == '4e1818c5b1ac7032018925edf17cecb1a6965e3d'
         and attempt['sourceManifestSha256'] == '52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449','frozen-failed-attempt')
    saved = bodies['savedTransportPin']['records']; journal = bodies['browserJournalPin']
    native = [row for row in journal if row['kind'] == 'native']
    need(len(saved) == 126 and len(journal) == 66 and len(native) == 30,'fixed-input-counts')
    expected = [{'index':i,'origin':'saved','sourceSequence':i,'recordPin':row['recordPin']}
                for i,row in enumerate(saved)]
    expected += [{'index':126+i,'origin':'browser','sourceSequence':row['sequence'],'recordPin':row['recordPin']}
                 for i,row in enumerate(native)]
    need(exact_equal(index['records'],expected),'complete-fixed-input-order')
    inputs = decode(read_pin(ctx['root'],ctx['pins'][PACKAGE+'/input-manifest.json']))
    fields(inputs,('schema','files'),'input-manifest-fields')
    need(inputs['schema'] == 'm31-tree-witness-layout-input-manifest-v1','input-manifest-schema')
    expected_pins = {p['path']:p for p in (index[k] for k in expected_anchors)}
    for row in expected:
        pin = row['recordPin']; expected_pins[pin['path']] = pin
        descriptor = decode(read_pin(ctx['root'],pin))
        for field in descriptor['fields']:
            for chunk in field['stream']['chunks']:
                if chunk['path'] in expected_pins: need(expected_pins[chunk['path']] == chunk,'input-pin-conflict')
                expected_pins[chunk['path']] = chunk
    actual_pins = {p['path']:p for p in inputs['files']}
    need(len(actual_pins) == len(inputs['files']) and actual_pins == expected_pins,'exact-input-file-closure')
    for path,pin in actual_pins.items(): need(pin == ctx['pins'][path],'input-in-execution-manifest')
    return index_pin,expected


def main(root,expected,commit):
    ctx,candidate = preflight(root,expected,commit)
    result = {'schema':'m31-tree-witness-layout-check-v1','sourceCommit':commit,'sourceManifestSha256':expected,
              'complete':False,'passed':False,'layoutQualified':False,'scientificValidated':False,
              'records':[],'controls':[],'errors':[],
              'scope':'Exact saved tree representation only; no native query, initializer, reference, omission proof or derivative/RK qualification.'}
    try:
        index_pin,inputs = input_records(ctx)
        need(candidate['schema'] == 'm31-tree-witness-layout-candidate-v1'
             and candidate['inputIndexPin'] == index_pin and len(candidate['records']) == 156,'candidate-exact-input-index')
        module = decoder(ctx)
        old_reader = module.Resolver(TransportSupport(OLD),ctx)
        new_reader = module.Resolver(TransportSupport(PACKAGE),ctx)
        old_total = new_total = 0; states = {'absent':0,'null':0,'object':0}; targets = []
        for source,item in zip(inputs,candidate['records']):
            guard(ctx)
            fields(item,('index','origin','sourceSequence','sourceRecordPin','method','treeState','recordPin',
                         'originalTreeBinaryBytes','newTreeBinaryBytes','logicalRoundtrip'),'candidate-record-fields')
            need(exact_equal({k:item[k] for k in ('index','origin','sourceSequence')},
                             {k:source[k] for k in ('index','origin','sourceSequence')})
                 and item['sourceRecordPin'] == source['recordPin'] and item['logicalRoundtrip'] is True,'candidate-source-row')
            descriptor = decode(read_pin(root,source['recordPin']))
            fields_by_key = {f['key']:f['stream'] for f in descriptor['fields']}
            need(len(fields_by_key) == len(descriptor['fields']),'source-record-unique-fields')
            method = old_reader.stream(fields_by_key['method']); need(item['method'] == method and method in ('F','H0','H'),'source-method')
            tree_present = 'tree' in fields_by_key
            tree = old_reader.stream(fields_by_key['tree']) if tree_present else None
            state = 'absent' if not tree_present else 'null' if tree is None else 'object'; states[state] += 1
            old_bytes = fields_by_key['tree']['binaryBytes'] if tree_present else 0
            need(item['treeState'] == state and item['originalTreeBinaryBytes'] == old_bytes,'tree-presence-old-bytes')
            n = tree['n'] if type(tree) is dict else None
            if n is None and 'ids' in fields_by_key:
                identifiers = old_reader.stream(fields_by_key['ids']); n = len(identifiers) if type(identifiers) is list else None
            if state == 'absent':
                need(item['recordPin'] is None and item['newTreeBinaryBytes'] == 0,'absent-tree-no-output')
                report = {'receivers':0,'culls':0,'gathered':0,'encodings':{}}; new_bytes = 0
            else:
                pin = item['recordPin']; need(pin['path'] == PACKAGE+'/results/records/%03d-tree.json'%source['index'],'layout-record-path')
                new_descriptor = decode(read_pin(root,pin)); decoded = new_reader.record(pin)
                fields(decoded,('tree',),'new-record-tree-only')
                need(len(new_descriptor['fields']) == 1 and new_descriptor['fields'][0]['key'] == 'tree','new-tree-field')
                new_bytes = new_descriptor['fields'][0]['stream']['binaryBytes']
                need(item['newTreeBinaryBytes'] == new_bytes,'new-tree-byte-binding')
                report = compare_tree(tree,decoded['tree'],poll=lambda:guard(ctx))
            old_total += old_bytes; new_total += new_bytes
            if source['origin'] == 'browser' and method == 'H' and n == 5000:
                targets.append({'index':source['index'],'sourceSequence':source['sourceSequence'],
                    'originalTreeBinaryBytes':old_bytes,'newTreeBinaryBytes':new_bytes,'maximumRatio':0.5,
                    'passed':2*new_bytes <= old_bytes})
            result['records'].append({'index':source['index'],'origin':source['origin'],'sourceSequence':source['sourceSequence'],
                'sourceRecordPin':source['recordPin'],'method':method,'treeState':state,'n':n,'newRecordPin':item['recordPin'],
                'originalTreeBinaryBytes':old_bytes,'newTreeBinaryBytes':new_bytes,'layoutQualified':True,
                'scientificValidated':False,**report})
            old_reader.clear(); new_reader.clear()
        result['controls'] = controls()
        control_ids = ('literal-selection','run-selection','bitmap-boundary-roundtrip','empty-roundtrip',
                       'duplicate-source-rejected','bitmap-tail-rejected','wrong-count-rejected','noncanonical-choice-rejected')
        need(candidate['controls'] == [{'id':identifier,'passed':True} for identifier in control_ids], 'candidate-fixed-controls')
        need([row['sourceSequence'] for row in targets] == [60,63]
             and all(row['passed'] for row in targets) and exact_equal(candidate['targets'],targets),
             'both-saved-large-H-size-targets')
        result['targets'] = targets; result['storageTargetPassed'] = True
        old_reader.verify_preserved(); new_reader.verify_preserved()
        result['recordCount'] = 156; result['treeStates'] = states
        result['originalTreeBinaryBytes'] = old_total; result['newTreeBinaryBytes'] = new_total
        result['binaryTreeRatio'] = new_total/old_total if old_total else None
        evidence_files = [p for sub in ('shards','records') for p in (ctx['package']/'results'/sub).rglob('*') if p.is_file()]
        need({p.relative_to(root).as_posix() for p in evidence_files} == set(new_reader.seen),
             'exact-new-evidence-file-closure')
        result['physicalEvidenceBytes'] = sum(p.stat().st_size for p in evidence_files)
        result['recordDescriptorBytes'] = sum(p.stat().st_size for p in (ctx['package']/'results/records').rglob('*.json'))
        result['sizeScope'] = 'Logical tree-value stream bytes and separate physical unique evidence/descriptor bytes; excludes unchanged read-only native input fields and does not establish whole-attempt fit.'
        result['comparisonPolicy'] = 'Exact scalar types and literal words; complete ordered arrays/receiver/cull/gathered sequences. Object property order is not semantic.'
        result['complete'] = result['passed'] = result['layoutQualified'] = True
    except Exception as error:
        reason = str(error)
        result['errors'].append({'type':type(error).__name__,'code':reason if len(reason)<=200 and all(c.isalnum() or c in '-_:' for c in reason) else 'checker-exception'})
    output(ctx,result)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    need(len(sys.argv) == 4,'arguments-root-sha-commit')
    raise SystemExit(main(Path(sys.argv[1]).resolve(),sys.argv[2],sys.argv[3]))

