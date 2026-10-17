"""Independent exact compact tree audit; no numerical producer imports.

The caller supplies the hash-verified frozen saved-evidence helper as `a`.
This file imports only stdlib and never invokes its CLI or native producers.
"""
from bisect import bisect_left, bisect_right
from fractions import Fraction
import math
import struct


def set_bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask ^= low


def sequence(a, encoded, n):
    a.fields(encoded, ('kind', 'data'), 'compact-sequence-fields')
    values = encoded['data']
    a.need(type(values) is list and len(values) <= n*2, 'compact-sequence-size')
    mask, count, runs = 0, 0, 0
    if encoded['kind'] == 'runs':
        a.need(len(values) % 2 == 0, 'compact-run-width')
        previous_end = -1
        for start, length in zip(values[::2], values[1::2]):
            a.integer(start, 0, n-1, 'compact-run-start')
            a.integer(length, 1, n, 'compact-run-length')
            a.need(start > previous_end and start+length <= n, 'compact-run-order-range')
            previous_end = start+length
            mask |= ((1 << length)-1) << start
            count += length; runs += 1
        a.need(2*runs < count, 'compact-shortest-run-choice')
    else:
        a.need(encoded['kind'] == 'literal', 'compact-sequence-kind')
        previous = -2
        for value in values:
            a.integer(value, 0, n-1, 'compact-literal-range')
            a.need(value > previous, 'compact-literal-order')
            runs += value != previous+1
            previous = value
            mask |= 1 << value
        count = len(values)
        a.need(2*runs >= count, 'compact-shortest-literal-choice')
    a.need(mask.bit_count() == count, 'compact-sequence-cardinality')
    return mask, count


def shared_coordinates(a, centers):
    cache, scale = {}, 52
    for center in centers:
        for word in center:
            value = a.dyadic(word)
            cache[word] = value
            scale = max(scale, value.denominator.bit_length()-1)
    factor = 1 << scale
    integers = {w: v.numerator*(factor//v.denominator) for w, v in cache.items()}
    return [[integers[w] for w in c] for c in centers], integers, scale


def prepare(a, raw):
    centers, eligible, nodes, membership = a.tree_from_raw(raw)
    n, all_ids = len(raw), (1 << len(raw))-1
    if not eligible:
        return {'centers': centers, 'eligible': False, 'nodes': [], 'n': n, 'all': all_ids}
    xyz, values, scale = shared_coordinates(a, centers)
    threshold = (4 << scale) - (1 << (scale-52))
    sorted_values, prefixes = [], []
    for axis in range(3):
        ordered = sorted(range(n), key=lambda i: (xyz[i][axis], i))
        sorted_values.append([xyz[i][axis] for i in ordered])
        prefix = [0]
        for i in ordered:
            prefix.append(prefix[-1] | (1 << i))
        prefixes.append(prefix)
    descendants, ancestors, leaves, tests = [], [], [], []
    parent = [-1]*len(nodes)
    for node in nodes:
        if node['left'] is not None:
            parent[node['left']] = parent[node['right']] = node['id']
    for node in nodes:
        identifier = node['id']
        descendants.append(sum(1 << i for i in membership[identifier]))
        chain, cursor = 0, identifier
        while cursor != -1:
            chain |= 1 << cursor; cursor = parent[cursor]
        ancestors.append(chain)
        if 'members' in node:
            leaves.append(identifier)
        predicates = []
        for k in range(3):
            # Ties round to even ±4. These exact thresholds are intentionally
            # 4-2^-52 and -4+2^-52, not the unrounded ±4 comparison.
            upper = values[node['min'][k]] - threshold
            lower = values[node['max'][k]] + threshold
            predicates.append(prefixes[k][bisect_right(sorted_values[k], upper)])
            predicates.append(all_ids ^ prefixes[k][bisect_left(sorted_values[k], lower)])
        tests.append(predicates)
    return {'centers': centers, 'eligible': True, 'nodes': nodes, 'n': n, 'all': all_ids,
            'xyz': xyz, 'values': values, 'scale': scale, 'descendants': descendants,
            'ancestors': ancestors, 'leaves': leaves, 'tests': tests}


def certificate(a, tree, raw, method, prepared=None, poll=lambda: None):
    if raw is None:
        a.need(tree is None, 'compact-capture-refusal-null')
        return {'culls': 0, 'omitted': 0, 'pairs': 0}
    p = prepared if prepared is not None else prepare(a, raw)
    nodes, n, all_ids = p['nodes'], p['n'], p['all']
    a.fields(tree, ('schema', 'mode', 'leafCapacity', 'eligible', 'fallback', 'fallbackReason',
                   'complete', 'n', 'canonicalIds', 'nodes', 'receivers', 'counters', 'leafDictionary'), 'compact-tree-fields')
    a.need(tree['schema'] == 'm31-native-center-tree-compact-v1' and tree['mode'] == method
           and tree['leafCapacity'] == 8 and tree['n'] == n
           and tree['canonicalIds'] == [r['id'] for r in raw]
           and tree['eligible'] is p['eligible'] and tree['fallback'] is (not p['eligible'])
           and tree['complete'] is True, 'compact-tree-header')
    counters = {'treeNodes': len(nodes), 'treeLeaves': len(p.get('leaves', [])),
                'receiverTraversals': 0, 'nodeVisits': 0, 'endpointComparisons': 0,
                'culledNodes': 0, 'omittedNonselfCandidates': 0, 'visitedLeaves': 0,
                'gatheredIndices': 0, 'gatheredNonselfCandidates': 0, 'completedReceivers': 0}
    if not p['eligible']:
        centers = p['centers']
        spans = [a.subtract(a.maximum([c[k] for c in centers]), a.minimum([c[k] for c in centers])) for k in range(3)]
        reason = 'span-nonfinite' if not all(a.finite(w) for w in spans) else 'span-out-of-range'
        a.need(tree['fallbackReason'] == reason and tree['nodes'] == tree['receivers'] == tree['leafDictionary'] == []
               and tree['counters'] == counters, 'compact-fallback-empty')
        return {'culls': 0, 'omitted': 0, 'pairs': n*(n-1)}
    a.need(tree['fallbackReason'] is None and a.canonical(tree['nodes']) == a.canonical(nodes), 'compact-tree-reconstruction')
    dictionary = tree['leafDictionary']
    a.need(type(dictionary) is list and len(dictionary) <= n, 'compact-dictionary-size')
    keys, leaf_sets, ancestor_sets = set(), [], []
    for entry in dictionary:
        poll()
        a.need(type(entry) is list and len(entry) <= len(p['leaves']), 'compact-leaf-sequence-size')
        key = tuple(entry)
        a.need(key not in keys, 'compact-duplicate-dictionary-entry'); keys.add(key)
        covered, ancestors, previous = 0, 0, -1
        for identifier in entry:
            a.integer(identifier, 0, len(nodes)-1, 'compact-leaf-node-range')
            a.need(identifier > previous and 'members' in nodes[identifier], 'compact-leaf-order-kind')
            covered |= p['descendants'][identifier]; ancestors |= p['ancestors'][identifier]; previous = identifier
        leaf_sets.append(covered); ancestor_sets.append(ancestors)
    a.need(type(tree['receivers']) is list and len(tree['receivers']) == n, 'compact-receiver-count')
    visited = [0]*len(nodes); culled_receivers = [0]*len(nodes)
    trace_groups, used_dictionary = {}, set()
    for i, row in enumerate(tree['receivers']):
        poll()
        a.fields(row, ('receiver', 'culled', 'leavesRef', 'gathered'), 'compact-receiver-fields')
        a.need(row['receiver'] == i, 'compact-receiver-order')
        reference = a.integer(row['leavesRef'], 0, len(dictionary)-1, 'compact-dictionary-reference')
        used_dictionary.add(reference)
        gathered, count = sequence(a, row['gathered'], n)
        a.need(gathered == leaf_sets[reference] and gathered & (1 << i), 'compact-actual-gathered-binding')
        omitted, previous, ancestry = 0, -1, ancestor_sets[reference]
        a.need(type(row['culled']) is list and len(row['culled']) <= len(nodes), 'compact-cull-size')
        for cull in row['culled']:
            a.fields(cull, ('node', 'axis', 'side', 'difference'), 'compact-cull-fields')
            identifier = a.integer(cull['node'], 0, len(nodes)-1, 'compact-cull-node')
            a.need(identifier > previous, 'compact-cull-order'); previous = identifier
            members = p['descendants'][identifier]
            a.need(not members & (omitted | gathered | (1 << i)), 'compact-overlap-self-cull')
            omitted |= members; ancestry |= p['ancestors'][identifier]
            first = next((k for k, mask in enumerate(p['tests'][identifier]) if mask & (1 << i)), None)
            a.need(first is not None and method == 'H', 'compact-false-cull')
            axis, side = first//2, ('min-ge4' if first % 2 == 0 else 'max-le-neg4')
            endpoint = nodes[identifier]['min' if first % 2 == 0 else 'max'][axis]
            difference = a.subtract(endpoint, p['centers'][i][axis])
            a.need(cull['axis'] == axis and cull['side'] == side and cull['difference'] == difference,
                   'compact-first-predicate-word')
            culled_receivers[identifier] |= 1 << i
        a.need(gathered | omitted == all_ids and not gathered & omitted, 'compact-complete-partition')
        a.need(method != 'H0' or (not row['culled'] and gathered == all_ids), 'compact-H0-all-actual-candidates')
        trace_groups[ancestry] = trace_groups.get(ancestry, 0) | (1 << i)
        counters['receiverTraversals'] += 1; counters['completedReceivers'] += 1
        counters['culledNodes'] += len(row['culled']); counters['visitedLeaves'] += len(dictionary[reference])
        counters['omittedNonselfCandidates'] += omitted.bit_count()
        counters['gatheredIndices'] += count; counters['gatheredNonselfCandidates'] += count-1
    a.need(used_dictionary == set(range(len(dictionary))), 'compact-unused-dictionary')
    for ancestry, receivers in trace_groups.items():
        poll()
        for identifier in set_bits(ancestry):
            visited[identifier] |= receivers
    for identifier, receivers in enumerate(visited):
        poll()
        remaining, success = receivers, 0
        counters['nodeVisits'] += receivers.bit_count()
        for predicate_mask in p['tests'][identifier]:
            counters['endpointComparisons'] += remaining.bit_count()
            first_success = remaining & predicate_mask
            success |= first_success; remaining ^= first_success
        a.need(culled_receivers[identifier] == (success if method == 'H' else 0), 'compact-first-cull-traversal')
    a.need(a.canonical(tree['counters']) == a.canonical(counters), 'compact-exact-work-counters')
    return {'culls': counters['culledNodes'], 'omitted': counters['omittedNonselfCandidates'],
            'pairs': counters['gatheredNonselfCandidates'], 'proof': 'complete exact node partition and midpoint predicate masks'}


def expand_small(a, tree):
    """Qualification only, N<=64: reconstruct the frozen exhaustive logical form."""
    if tree is None:
        return None
    a.need(tree['n'] <= 64, 'small-expansion-only')
    out = {k: v for k, v in tree.items() if k not in ('leafDictionary', 'receivers')}
    out['schema'] = 'm31-native-center-tree-v1'
    out['receivers'] = []
    for row in tree['receivers']:
        mask, count = sequence(a, row['gathered'], tree['n'])
        out['receivers'].append({'receiver': row['receiver'], 'culled': row['culled'],
                                 'leaves': tree['leafDictionary'][row['leavesRef']], 'gathered': list(set_bits(mask))})
    return out


class Resolver:
    """Lossless bounded binary reader. Cached equal streams were byte-verified.

    jsonBytes is a bounded source diagnostic: Python does not pretend its number
    formatting is JS JSON.stringify. Binary sizes, elements and types are exact.
    """
    def __init__(self, support, ctx):
        self.s, self.ctx = support, ctx
        self.cache = {}
        self.seen = {}

    def clear(self):
        self.cache.clear()

    def stream(self, descriptor):
        s = self.s
        s.fields(descriptor, ('schema', 'binaryBytes', 'jsonBytes', 'elements', 'chunks'), 'stream-fields')
        s.need(descriptor['schema'] == 'm31-value-stream-v1', 'stream-schema')
        for key, cap in (('binaryBytes', 96*1024*1024), ('jsonBytes', 256*1024*1024), ('elements', 16_000_000)):
            s.integer(descriptor[key], 1, cap, 'stream-bound-'+key)
        chunks = descriptor['chunks']
        s.need(type(chunks) is list and 0 < len(chunks) <= 96, 'stream-chunk-count')
        for i, pin in enumerate(chunks):
            s.fields(pin, ('path', 'bytes', 'sha256'), 'chunk-pin-fields')
            s.need(pin['path'] == s.PACKAGE + '/results/shards/' + pin['sha256'] + '.bin', 'content-addressed-shard-path')
            s.integer(pin['bytes'], 1, 1024*1024, 'chunk-byte-bound')
            s.need(i == len(chunks)-1 or pin['bytes'] == 1024*1024, 'chunk-fixed-boundary')
        s.need(sum(p['bytes'] for p in chunks) == descriptor['binaryBytes'], 'stream-byte-sum')
        identity = tuple((p['path'], p['bytes'], p['sha256']) for p in chunks)
        key = (identity, descriptor['binaryBytes'], descriptor['elements'])
        if key in self.cache:
            return self.cache[key]
        pieces, total = [], 0
        for i, pin in enumerate(chunks):
            s.guard(self.ctx)
            pieces.append(s.read_pin(self.ctx['root'], pin)); total += pin['bytes']
            self.seen[pin['path']] = pin
        s.need(total == descriptor['binaryBytes'], 'stream-byte-sum')
        raw = b''.join(pieces)
        at, elements = 0, 0
        def take(n):
            nonlocal at
            s.need(type(n) is int and n >= 0 and at+n <= len(raw), 'stream-truncated')
            value = raw[at:at+n]; at += n
            return value
        def u32():
            return int.from_bytes(take(4), 'big')
        def add(n):
            nonlocal elements
            elements += n
            s.need(elements <= descriptor['elements'] <= 16_000_000, 'stream-element-limit')
        def value(depth=0):
            s.need(depth <= 64, 'stream-depth')
            add(1)
            tag = take(1)[0]
            if tag == 0: return None
            if tag == 1: return False
            if tag == 2: return True
            if tag == 3:
                result = struct.unpack('>d', take(8))[0]
                s.need(math.isfinite(result), 'stream-nonfinite-number')
                # Preserve Number value including negative zero, while IDs and
                # dimensions must remain Python ints for independent validators.
                return int(result) if result.is_integer() and (result != 0 or math.copysign(1, result) > 0) else result
            if tag == 4:
                length = u32(); s.need(length <= 256*1024*1024, 'stream-string-bound')
                return take(length).decode('utf-8', 'strict')
            if tag == 7: return take(8).hex()
            if tag == 5:
                count = u32(); s.need(count <= descriptor['elements']-elements, 'stream-array-bound')
                return [value(depth+1) for _ in range(count)]
            if tag == 6:
                count = u32(); s.need(2*count <= descriptor['elements']-elements, 'stream-object-bound')
                result = {}
                for _ in range(count):
                    k = value(depth+1)
                    s.need(type(k) is str and k not in result, 'stream-object-key')
                    result[k] = value(depth+1)
                return result
            if tag in (8, 9, 10):
                count = u32(); s.need(count > 0, 'stream-empty-optimized-array')
                s.need(depth+1 <= 64, 'stream-depth')
                add(count)
                width = 4 if tag == 9 else 8
                block = take(count*width)
                if tag == 8: return [block[i:i+8].hex() for i in range(0, len(block), 8)]
                if tag == 9: return [v[0] for v in struct.iter_unpack('>I', block)]
                result = [v[0] for v in struct.iter_unpack('>d', block)]
                s.need(all(math.isfinite(v) for v in result), 'stream-nonfinite-array')
                return [int(v) if v.is_integer() and (v != 0 or math.copysign(1, v) > 0) else v for v in result]
            raise ValueError('stream-unknown-tag')
        decoded = value()
        s.need(at == len(raw) and elements == descriptor['elements'], 'stream-trailing-or-element-count')
        self.cache[key] = decoded
        return decoded

    def record(self, pin):
        s = self.s
        raw = s.read_pin(self.ctx['root'], pin)
        self.seen[pin['path']] = pin
        s.need(len(raw) <= 2*1024*1024, 'record-descriptor-cap')
        descriptor = s.decode(raw)
        s.fields(descriptor, ('schema', 'fields', 'binaryBytes', 'jsonBytes', 'elements'), 'record-fields')
        s.need(descriptor['schema'] == 'm31-lossless-record-v1' and type(descriptor['fields']) is list
               and len(descriptor['fields']) <= 128,
               'record-schema')
        s.integer(descriptor['binaryBytes'], 0, 96*1024*1024, 'record-binary-bound')
        s.integer(descriptor['elements'], 1, 16_000_000, 'record-elements-bound')
        s.integer(descriptor['jsonBytes'], 2, 256*1024*1024, 'record-json-diagnostic-bound')
        result, binary, elements = {}, 0, 1
        for field in descriptor['fields']:
            s.fields(field, ('key', 'stream'), 'record-field-descriptor')
            key = field['key']
            s.need(type(key) is str and len(key.encode('utf-8')) <= 4096 and key not in result, 'record-duplicate-field')
            binary += field['stream']['binaryBytes']; elements += 1+field['stream']['elements']
            s.need(binary <= descriptor['binaryBytes'] <= 96*1024*1024
                   and elements <= descriptor['elements'] <= 16_000_000, 'record-cumulative-bound')
            result[key] = self.stream(field['stream'])
        s.need(binary == descriptor['binaryBytes'] <= 96*1024*1024
               and elements == descriptor['elements'] <= 16_000_000, 'record-exact-bounds')
        s.integer(descriptor['jsonBytes'], 2, 256*1024*1024, 'record-json-diagnostic-bound')
        return result

    def verify_preserved(self):
        for pin in self.seen.values():
            self.s.guard(self.ctx)
            self.s.read_pin(self.ctx['root'], pin)
