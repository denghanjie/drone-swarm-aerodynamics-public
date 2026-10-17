"""One bounded independent exact-reference allocation; no native candidate imports."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

NAME = 'research/m31-native-fresh-transfer-2026-10-17'
PAIR_SHA = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
SEMANTIC_SHA = 'ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'

def bootstrap(root, expected, commit):
    # Every source byte is checked before the local support module is imported.
    package = root / NAME
    data = (package / 'source-manifest.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('bootstrap-manifest')
    manifest = json.loads(data)
    paths = set()
    for item in manifest['files']:
        relative = item['path']
        path = root / relative
        if relative in paths or Path(relative).is_absolute() or any(p in ('', '.', '..') for p in relative.split('/')) or path.resolve() != path:
            raise ValueError('bootstrap-path')
        paths.add(relative)
        raw = path.read_bytes()
        if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('bootstrap-pin')
    if NAME + '/source/fresh_support.py' not in paths or NAME + '/source/reference.py' not in paths:
        raise ValueError('bootstrap-closure')
    spec = importlib.util.spec_from_file_location('_fresh_support_reference', package / 'source/fresh_support.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.gate(root, expected, commit, 'reference', Path(__file__))

class RawWordHelper:
    """Only raw-word parsing is adapted; inherited function globals stay intact."""
    def __init__(self, helper):
        self.helper = helper
    def literal(self, text):
        return self.helper.parse_bits(text)
    def __getattr__(self, name):
        return getattr(self.helper, name)

def graph_evidence(target):
    ids = [d['id'] for d in target['input']['drones']]
    if target['globalInvalid']:
        return {'status': 'not-evaluated', 'reason': 'global-preparation-refusal', 'positiveEdges': [], 'positiveRotorPairs': 0, 'cycle': None, 'orderWitness': None}
    positives = [p for p in target['pairs'] if p['oracle']['status'] == 'positive']
    edges = sorted(set((p['j'], p['i']) for p in positives))
    unresolved = [p for p in target['pairs'] if p['oracle']['status'] not in ('zero', 'positive')]
    result = {'positiveEdges': [list(e) for e in edges], 'positiveRotorPairs': len(positives), 'cycle': None, 'orderWitness': None, 'status': 'unknown' if unresolved else None, 'reason': 'pair-status-not-resolved' if unresolved else None}
    if unresolved:
        result['unresolvedPairCount'] = len(unresolved)
        return result
    ranks = {identifier: i for i, identifier in enumerate(target['order'])}
    wrong = next((p for p in positives if ranks[p['j']] >= ranks[p['i']]), None)
    if wrong:
        result['orderWitness'] = {k: wrong[k] for k in ('i', 'r', 'j')}
    adjacency = {identifier: [] for identifier in ids}
    for source, receiver in edges:
        adjacency[source].append(receiver)
    colors, stack = {identifier: 0 for identifier in ids}, []
    def visit(node):
        colors[node] = 1
        stack.append(node)
        for child in adjacency[node]:
            if colors[child] == 1:
                return stack[stack.index(child):] + [child]
            if colors[child] == 0:
                cycle = visit(child)
                if cycle:
                    return cycle
        stack.pop()
        colors[node] = 2
        return None
    cycle = None
    for node in ids:
        if colors[node] == 0:
            cycle = visit(node)
            if cycle:
                break
    result['cycle'] = cycle
    result['status'] = 'cyclic' if cycle else ('acyclic-order-incompatible' if wrong else 'acyclic-compatible')
    return result

def reference_record(ctx, descriptor, target, graph, semantic):
    pairs = []
    for pair in target['pairs']:
        row = {'i': pair['i'], 'r': pair['r'], 'j': pair['j'], **pair['oracle']}
        if 'coefficient' in pair:
            row['coefficient'] = semantic.interval_wire(pair['coefficient'])
        pairs.append(row)
    loads = []
    if target['status'] == 'admitted':
        for drone in target['input']['drones']:
            identifier = drone['id']
            loads.append({'id': identifier, 'roots': [semantic.interval_wire(target['roots'][(identifier, r)]) for r in range(4)],
                          'loads': {k: semantic.interval_wire(v) if k == 'collective' else [semantic.interval_wire(x) for x in v]
                                    for k, v in target['loads'][identifier].items()}})
    return {'schema': 'm31-native-fresh-reference-v1', 'sourceCommit': ctx['commit'], 'sourceManifestSha256': ctx['expected'],
            'id': descriptor['id'], 'n': descriptor['n'], 'input': descriptor['input'],
            'inputSha256': descriptor['semanticInputSha256'], 'referenceStatus': target['status'],
            'branch': target['branch'], 'witness': target['witness'], 'prepared': target['prepared'],
            'plannedPairs': target['planned'], 'evaluatedPairs': len(pairs), 'pairs': pairs,
            'graph': graph, 'loads': loads, 'recipe': {'coefficientBits': 192, 'sourceBits': 192, 'rootBisections': 128}}

def main(root, expected, commit):
    support, ctx = bootstrap(root, expected, commit)
    science = ctx['science']
    output = {'schema': 'm31-native-fresh-reference-index-v1', 'sourceCommit': commit, 'sourceManifestSha256': expected,
              'generationIndex': None, 'complete': False, 'qualified': False, 'constants': None,
              'controls': [{'id': c['id'], 'referenceStatus': 'not-attempted', 'reference': None, 'qualified': False} for c in science['movingControls']],
              'targets': [{'id': s['id'], 'referenceStatus': 'not-attempted', 'reference': None, 'qualified': False} for s in science['slots']], 'errors': []}
    code = 1
    try:
        generation, generation_pin = support.closed_stage(ctx, 'generation')
        output['generationIndex'] = generation_pin
        raws, motions = support.validate_generation(ctx, generation)
        reference_dir = ctx['package'] / 'results/reference'
        reference_dir.mkdir(exist_ok=False)
        helper = support.load_module(ctx, 'pair-reference.py', PAIR_SHA)
        semantic = support.load_module(ctx, 'semantic-reference.py', SEMANTIC_SHA)
        spec = support.load(ctx['package'] / 'source/spec.json')
        support.need(spec['maxDrones'] == 180 and science['referenceMaxDrones'] == 180, 'reference-cap-180')
        support.need(all(spec[k] == v for k, v in {'referenceCoefficientBits': 192, 'referenceSourceBits': 192, 'referenceRootBisections': 128, 'positiveTermCap': 2000000}.items()), 'reference-fixed-recipe')
        bits, _trace = helper.constants_from_graph(spec)
        output['constants'] = {k: helper.hex_bits(v) for k, v in bits.items()}
        for c in science['movingControls']:
            want = {'drones': [{'id': d['id'], 'state': [helper.hex_bits(helper.literal(v)) for v in d['state']]} for d in c['drones']]}
            support.need(support.same(want, raws[c['id']]), 'moving-control-literal-binding')
        for kind, descriptors in [('controls', generation['controls']), ('targets', generation['slots'])]:
            for position, descriptor in enumerate(descriptors):
                identifier, count = descriptor['id'], descriptor['n']
                output[kind][position] = dict(descriptor, referenceStatus='started', reference=None, qualified=False)
                support.need(count <= science['referenceMaxDrones'] and count == (64 if kind == 'targets' else (3 if position == 0 else 2)), 'declared-reference-count')
                scene = {'id': identifier, 'family': 'moving-admission', 'expectedClass': 'unconstrained', 'drones': raws[identifier]['drones']}
                # Each of the six predeclared references is evaluated exactly once.
                target = semantic.regenerate_scene(scene, spec, bits, RawWordHelper(helper))
                graph = graph_evidence(target)
                record = reference_record(ctx, descriptor, target, graph, semantic)
                reference_pin = support.write(root, reference_dir / (identifier + '.json'), record)
                ctx['protected'].append(reference_pin)
                if kind == 'controls':
                    expected_ref = descriptor['expectedReference']
                    qualified = target['status'] == expected_ref['status'] and target['branch'] == expected_ref['branch']
                else:
                    qualified = (target['status'] == 'admitted' and target['branch'] == 'loads'
                                 and graph['status'] == 'acyclic-compatible' and graph['positiveRotorPairs'] > 0
                                 and len(target['pairs']) == 4 * 64 * 63 and motions[identifier]['passed'])
                output[kind][position] = dict(descriptor, reference=reference_pin, referenceStatus=target['status'], branch=target['branch'],
                                              graphStatus=graph['status'], positiveRotorPairs=graph['positiveRotorPairs'], qualified=qualified)
                del target, record
        output['complete'] = True
        output['qualified'] = all(x['qualified'] for x in output['controls'] + output['targets'])
        code = 0
    except Exception as error:
        output['errors'].append({'type': type(error).__name__, 'code': str(error)[:160] if str(error).replace('-', '').replace(':', '').isalnum() else 'reference-exception'})
    finally:
        try:
            support.preserve(ctx)
            output['inputsAndSourcesPreserved'] = True
        except Exception:
            output['inputsAndSourcesPreserved'] = False
            output['qualified'] = False
            output['errors'].append({'type': 'PreservationError', 'code': 'postrun-preservation'})
            code = 1
        support.write(root, ctx['package'] / 'results/reference.json', output, 2 * 1024 * 1024)
    return code

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: reference.py ROOT MANIFEST_SHA COMMIT')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]))
