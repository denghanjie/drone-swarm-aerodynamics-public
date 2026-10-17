"""Bounded saved42 codec/proof qualification; no fresh producer calls."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import struct
import subprocess
import sys
import time

PACKAGE = 'research/m31-native-tree-browser-probe-2026-10-17'
OLD = 'research/m31-native-tree-design-2026-10-17'
OLD_WORK = 'e4125bd48f2b0ee440443b02ab5486cda3cc6212d535fb375ef2ed9d4bac7f60'
OLD_CASES = '9cf2a3e99bd645abeb83e92eeb6efcdff81cf2ad71a1e31db8ce8ff9667ba0e1'


def decoder_controls(s, ctx, compact):
    """Mutate tiny in-memory byte streams, never any durable saved evidence."""
    class MemoryPins:
        def __init__(self): self.files = {}
        def __getattr__(self, name): return getattr(s, name)
        def read_pin(self, root, pin):
            raw = self.files[pin['path']]
            s.need(len(raw) == pin['bytes'] and s.sha(raw) == pin['sha256'], 'pin-bytes')
            return raw
    memory = MemoryPins()
    def descriptor(raw, elements):
        digest = s.sha(raw); path = PACKAGE+'/results/shards/'+digest+'.bin'
        memory.files[path] = raw
        return {'schema':'m31-value-stream-v1','binaryBytes':len(raw),'jsonBytes':256,'elements':elements,
                'chunks':[{'path':path,'bytes':len(raw),'sha256':digest}]}
    outcomes = []
    tests = [
        ('unknown-tag', b'\xff', 1, 'stream-unknown-tag'),
        ('trailing-byte', b'\x00\x00', 1, 'stream-trailing-or-element-count'),
        ('truncated-word', b'\x07'+b'\x00'*7, 1, 'stream-truncated'),
        ('empty-optimized-array', b'\x08'+b'\x00'*4, 1, 'stream-empty-optimized-array'),
        ('nonfinite-number', b'\x03'+struct.pack('>d',float('inf')), 1, 'stream-nonfinite-number'),
        ('duplicate-key', b'\x06\x00\x00\x00\x02'+(b'\x04\x00\x00\x00\x01a\x00')*2, 5, 'stream-object-key'),
        ('optimized-depth', (b'\x05\x00\x00\x00\x01')*64+b'\x09\x00\x00\x00\x01'+b'\x00'*4, 66, 'stream-depth'),
    ]
    for name, raw, elements, expected in tests:
        s.guard(ctx); reader = compact.Resolver(memory,ctx)
        try: reader.stream(descriptor(raw,elements))
        except ValueError as error:
            s.need(str(error) == expected, 'decoder-control-wrong-rejection:'+name)
            outcomes.append({'id':name,'status':'rejected','reason':expected})
        else: raise ValueError('decoder-control-not-rejected:'+name)
    valid = descriptor(b'\x07'+bytes.fromhex('8000000000000000'),1)
    reader = compact.Resolver(memory,ctx)
    s.need(reader.stream(valid) == '8000000000000000', 'decoder-literal-word-preserved')
    signed = reader.stream(descriptor(b'\x03'+bytes.fromhex('8000000000000000'),1))
    s.need(struct.pack('>d',signed).hex() == '8000000000000000', 'decoder-signed-zero-preserved')
    for name, expected in (('warm-cache-unknown-chunk-field','chunk-pin-fields'),
                           ('wrong-shard-path','content-addressed-shard-path'),
                           ('wrong-byte-sum','stream-byte-sum')):
        changed = copy.deepcopy(valid)
        if name == 'warm-cache-unknown-chunk-field': changed['chunks'][0]['extra'] = True
        elif name == 'wrong-shard-path': changed['chunks'][0]['path'] += '.extra'
        else: changed['binaryBytes'] += 1
        try: reader.stream(changed)
        except ValueError as error:
            s.need(str(error) == expected, 'decoder-control-wrong-rejection:'+name)
            outcomes.append({'id':name,'status':'rejected','reason':expected})
        else: raise ValueError('decoder-control-not-rejected:'+name)
    outcomes.append({'id':'literal-word-and-signed-zero','status':'preserved'})
    return outcomes


def bootstrap(root, expected, commit):
    raw = (root / PACKAGE / 'source-manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('bootstrap-manifest')
    manifest = json.loads(raw)
    path = PACKAGE + '/source/reference.py'
    pin = next(p for p in manifest['files'] if p['path'] == path)
    source = (root / path).read_bytes()
    if len(source) != pin['bytes'] or hashlib.sha256(source).hexdigest() != pin['sha256']:
        raise ValueError('bootstrap-support-pin')
    spec = importlib.util.spec_from_file_location('_probe_reference_support', root / path)
    support = importlib.util.module_from_spec(spec); spec.loader.exec_module(support)
    return support, support.preflight(root, expected, commit, 'saved-validation')


def main(root, expected, commit):
    s, ctx = bootstrap(root, expected, commit)
    result = {'schema': 'm31-tree-saved-validation-v1', 'sourceCommit': commit,
              'sourceManifestSha256': expected, 'complete': False, 'passed': False,
              'records': 0, 'cases': 0, 'controls': [], 'errors': []}
    process = None
    try:
        for relative, digest in ((OLD + '/results/work.json', OLD_WORK), (OLD + '/source/cases.json', OLD_CASES)):
            s.need(ctx['pins'][relative]['sha256'] == digest, 'frozen-saved-source-pin')
        native = s.module(ctx, 'tree_check')
        compact = s.local_module(ctx, 'compact-check.py')
        resolver = compact.Resolver(s, ctx)
        work = s.decode(s.read_pin(root, ctx['pins'][OLD + '/results/work.json']))
        cases = s.decode(s.read_pin(root, ctx['pins'][OLD + '/source/cases.json']))
        native.validate_spec(cases)
        inputs = {c['id']: native.materialize(root, cases, c) for c in cases['cases']}
        node = Path(os.environ['RESEARCH_NODE']).resolve()
        binary = node.read_bytes(); runtime = ctx['manifest']['runtime']['node']
        s.need(len(binary) == runtime['bytes'] and s.sha(binary) == runtime['sha256'], 'saved-codec-node-pin')
        driver = PACKAGE + '/source/qualify-transport.cjs'
        s.read_pin(root, ctx['pins'][driver])
        logfile = Path(os.environ['RESEARCH_PRIVATE_LOG_DIR']) / 'saved-codec.log'
        with logfile.open('xb') as log:
            process = subprocess.Popen([str(node), str(root / driver), str(root), expected, commit],
                                       cwd=root, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
            timeout = max(0.001, (ctx['computeDeadline']-time.monotonic_ns())/1e9)
            try:
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait(timeout=1); raise ValueError('saved-codec-deadline')
        s.need(code == 0, 'saved-codec-exit')
        index_path = ctx['package'] / 'results/saved-transport.json'
        s.need(index_path.stat().st_size <= s.MAX_FILE, 'saved-index-file-cap')
        index_raw = index_path.read_bytes(); index = s.decode(index_raw)
        ctx['protectedPins'].append({'path':PACKAGE+'/results/saved-transport.json',
                                     'bytes':len(index_raw),'sha256':s.sha(index_raw)})
        s.need(index['schema'] == 'm31-saved-transport-v1' and index['complete'] is True and index['passed'] is True
               and index['sourceCommit'] == commit and index['sourceManifestSha256'] == expected,
               'saved-transport-index')
        s.need(len(index['records']) == 126 and len(work['cases']) == 42, 'saved-exact-count')
        original_pins = {(p['caseId'], p['method']): {k: p[k] for k in ('path', 'bytes', 'sha256')}
                         for p in work['evidenceFiles']}
        for case_index, (row, descriptor) in enumerate(zip(work['cases'], cases['cases'])):
            s.guard(ctx)
            baseline = native.verify_case(row, descriptor, inputs[row['id']])
            prepared = compact.prepare(native, row['methods']['F']['raw']) if row['methods']['F']['raw'] is not None else None
            for method_index, method in enumerate(('F', 'H0', 'H')):
                item = index['records'][3*case_index+method_index]
                old_pin = original_pins[(row['id'], method)]
                s.need(item['caseId'] == row['id'] and item['method'] == method and item['sourceOldPin'] == old_pin,
                       'saved-record-order-source')
                s.need(ctx['pins'][old_pin['path']] == old_pin, 'all126-old-sidecars-pinned')
                original = s.decode(s.read_pin(root, old_pin))
                actual = resolver.record(item['recordPin'])
                logical = copy.deepcopy(actual)
                if method != 'F':
                    stats = compact.certificate(native, actual.get('tree'), actual['raw'], method, prepared,
                                                poll=lambda: s.guard(ctx))
                    s.need({k: stats[k] for k in ('culls', 'omitted', 'pairs')} == baseline['work'][method],
                           'optimized-exhaustive-proof-agreement')
                    logical['tree'] = compact.expand_small(native, actual.get('tree'))
                s.need(s.canonical(logical) == s.canonical(original) == s.canonical(row['methods'][method]),
                       'saved-lossless-full-payload-roundtrip')
                result['records'] += 1
            resolver.clear(); result['cases'] += 1
        result['arithmetic'] = native.arithmetic_controls()
        result['controls'] = native.mutation_controls(work['cases'], cases['cases'], inputs, ctx)
        # Focused new corruption laws use the first fixed boundary's actual
        # compact record. They never query a native producer.
        witness = resolver.record(index['records'][2]['recordPin'])
        for name, expected_reason in (('run-length','compact-run-length'),
                                     ('dictionary-reference','compact-dictionary-reference'),
                                     ('candidate-missing','compact-actual-gathered-binding')):
            changed = copy.deepcopy(witness['tree']); first = changed['receivers'][0]
            if name == 'run-length': first['gathered'] = {'kind': 'runs', 'data': [0, 0]}
            elif name == 'dictionary-reference': first['leavesRef'] = len(changed['leafDictionary'])
            else: first['gathered'] = {'kind': 'literal', 'data': []}
            try:
                compact.certificate(native, changed, witness['raw'], 'H', poll=lambda: s.guard(ctx))
            except native.InvalidRecord as error:
                s.need(str(error) == expected_reason, 'compact-mutation-wrong-rejection:'+name)
                result['controls'].append({'id': name, 'kind': 'saved-compact-mutation', 'status': 'rejected',
                                           'reason': str(error)[:160]})
            else:
                raise ValueError('compact-mutation-not-rejected:' + name)
        codec_ids = ('literal-word-and-signed-zero','unknown-tag-rejected','trailing-byte-rejected',
                     'truncated-word-rejected','empty-optimized-array-rejected','fixed-boundary-word-roundtrip')
        s.need(type(index['codecControls']) is list and len(index['codecControls']) == len(codec_ids)
               and all(c == {'id':identifier,'pass':True} for c,identifier in zip(index['codecControls'],codec_ids)),
               'codec-controls')
        result['codecControls'] = index['codecControls']
        result['independentDecoderControls'] = decoder_controls(s,ctx,compact)
        resolver.verify_preserved()
        result['complete'] = result['passed'] = True
    except Exception as error:
        result['errors'].append(s.public_error(error))
    finally:
        if process is not None and process.poll() is None:
            process.kill(); process.wait(timeout=1)
    ctx['closing'] = True
    s.verify_sources(ctx)
    s.write(ctx, 'saved-validation.json', result)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: validate-saved.py ROOT SHA COMMIT')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]))
