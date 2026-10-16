#!/usr/bin/env python3
"""Independent saved cost checker: one scene/oracle/control copy at a time.

No candidate module imports. Independent helpers are compiled only from source
buffers whose exact bytes match the frozen manifest. No old suites are called.
"""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import types

INDEX_LIMIT = JOURNAL_LIMIT = 8 * 1024 * 1024
SCENE_LIMIT = 128 * 1024 * 1024
SCIENCE_LIMIT = 384 * 1024 * 1024
CHECKER_LIMIT = 128 * 1024 * 1024
SOURCE_LIMIT = 16 * 1024 * 1024
PAIR_SHA = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
METHODS = ('hierarchy', 'filtered')
SEMANTIC_SHA = 'ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'
FILTER_FIELDS = ('filterPrepared','filterAttempts','filterZeros','exactScalarCalls')
FILTER_BRANCHES = ('neighbor','upstream','down-cut','near-outside','radial','projection')
SOURCE_FILES = ('spec.json','result-contract.json','interval.cjs','rational.cjs','adapter.cjs',
    'pair-prepared.cjs','boxes.cjs','tree.cjs','loads.cjs','binary64-interval.cjs','zero-filter.cjs',
    'methods.cjs','canonical.cjs','run.cjs')
ORDERS = ('AB', 'AB', 'BA', 'BA', 'AB')
SCENE_IDS = ('dense-80-filter-cost', 'dense-120-filter-cost', 'dense-180-filter-cost',
             'sparse-80-filter-cost', 'sparse-120-filter-cost', 'sparse-180-filter-cost')
SIZES = (80,120,180,80,120,180)
DIMENSIONS = ((4,4,5),(4,5,6),(5,6,6))
ENCODER = json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                           allow_nan=False)


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


def reject_number(_text):
    raise CheckError('float-or-constant-json-token')


def decode(data):
    try:
        value = json.loads(data, object_pairs_hook=no_duplicates,
                           parse_int=parse_integer, parse_float=reject_number,
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
    size = canonical_size(value)
    require(size <= remaining, 'checker-output-budget')
    require(path.parent.is_dir() and not path.parent.is_symlink(), 'checker-output-parent')
    digest = hashlib.sha256()
    with path.open('xb') as handle:
        for fragment in ENCODER.iterencode(value):
            block = fragment.encode('ascii')
            handle.write(block)
            digest.update(block)
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


def validate_spec(spec):
    fixed = {'id':'m31-filter-cost-v1', 'expectedRecords':6, 'maxDrones':180,
             'stableIdMin':0, 'stableIdMax':65535, 'leafCapacity':8,
             'candidateIterations':48, 'rootBisections':54,
             'referenceCoefficientBits':192, 'referenceSourceBits':192,
             'referenceRootBisections':128, 'fractionBits':96,
             'positiveTermCap':2000000, 'expectedPlannedPairs':422560}
    for key, value in fixed.items():
        require(same(spec.get(key), value), 'spec-fixed:'+key)
    require(same(spec.get('methods'), list(METHODS)), 'spec-methods')
    require(same(spec.get('zeroRuleOrder'),
                 ['neighbor','upstream','down-cut','near-outside','radial']), 'spec-rules')
    require(same(spec.get('corners'), [[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]]),
            'spec-corners')
    require(same(spec.get('tolerance'), {'numerator':'1','denominator':'100000000'}),
            'spec-tolerance')
    scenes = spec.get('scenes')
    require(type(scenes) is list and len(scenes) == 6, 'spec-scenes')
    total = pairs = 0
    for index, scene in enumerate(scenes):
        fields(scene, ('id','family','spacing','dimensions','expectedClass','drones'), 'spec-scene-fields')
        require(scene['spacing'] == ('0.47' if index < 3 else '3.7') and
                same(scene['dimensions'],list(DIMENSIONS[index%3])), 'spec-scene-layout')
        require(scene['id'] == SCENE_IDS[index] and
                scene['family'] == ('dense' if index < 3 else 'sparse') and
                scene['expectedClass'] == 'admitted', 'spec-scene-identity')
        drones = scene['drones']
        require(type(drones) is list and len(drones) == SIZES[index], 'spec-scene-size')
        for position, drone in enumerate(drones):
            fields(drone, ('id','state'), 'spec-drone-fields')
            require(type(drone['id']) is int and drone['id'] == 2000+position,
                    'spec-drone-id-order')
            require(type(drone['state']) is list and len(drone['state']) == 17 and
                    all(type(v) is str and len(v) <= 128 for v in drone['state']),
                    'spec-literal-state')
        total += len(drones)
        pairs += 4*len(drones)*(len(drones)-1)
    require(total == 760 and pairs == 422560, 'spec-total-counts')
    timing = spec.get('timing')
    require(type(timing) is dict and timing.get('clock') == 'process.hrtime.bigint' and
            timing.get('repetitions') == 4 and
            same(timing.get('warmupOrders'), [list(METHODS)]) and
            same(timing.get('measuredOrders'),
                 [['hierarchy','filtered'],['filtered','hierarchy'],
                  ['filtered','hierarchy'],['hierarchy','filtered']]), 'spec-timing')


def time_integer(value):
    require(type(value) is str and len(value) <= 20 and
            re.fullmatch(r'0|[1-9][0-9]*', value) is not None, 'timing-integer')
    return int(value)


def interval(value, positive=False):
    fields(value, ('startNs','endNs','totalNs'), 'timing-interval-fields')
    start, end, total = (time_integer(value[k]) for k in ('startNs','endNs','totalNs'))
    require(0 <= start <= end and end-start == total and
            (not positive or total > 0), 'timing-outer-interval')
    return start, end, total


def fraction_wire(value):
    return {'n':str(value.numerator), 'd':str(value.denominator)}


def median(values):
    ordered = sorted(values)
    require(len(ordered) == 4, 'summary-repetition-count')
    return (Fraction(ordered[1])+Fraction(ordered[2]))/2


def summary(trials, scene_id):
    pairs, durations, ratios = [], {m:[] for m in METHODS}, []
    wins = 0
    for repetition in range(1, 5):
        pair = trials[2*repetition:2*repetition+2]
        values = {t['method']:time_integer(t['timing']['totalNs']) for t in pair}
        ratio = Fraction(values['filtered'], values['hierarchy'])
        ratios.append(ratio)
        wins += int(values['filtered'] < values['hierarchy'])
        for method in METHODS:
            durations[method].append(values[method])
        pairs.append({'repetition':repetition, 'pairOrder':ORDERS[repetition],
                      'hierarchyNs':str(values['hierarchy']),
                      'filteredNs':str(values['filtered']), 'ratio':fraction_wire(ratio)})
    off, on = median(durations['hierarchy']), median(durations['filtered'])
    paired = median(ratios)
    return {'sceneId':scene_id, 'pairs':pairs, 'hierarchyMedianNs':fraction_wire(off),
            'filteredMedianNs':fraction_wire(on), 'medianPairedRatio':fraction_wire(paired),
            'ratioOfMedians':fraction_wire(on/off), 'winCount':wins,
            'practicalBenefitPassed':paired <= Fraction(9,10) and wins >= 3}


def validate_scene_index(document, contract):
    descriptors = document.get('scenes')
    require(type(descriptors) is list and len(descriptors) == 6, 'scene-count')
    seen = set()
    for index, row in enumerate(descriptors):
        fields(row, contract['storage']['sceneDescriptorFields'], 'scene-descriptor-fields')
        require(row['id'] not in seen, 'duplicate-scene-id')
        seen.add(row['id'])
        require(row['id'] == SCENE_IDS[index] and type(row['sceneIndex']) is int and
                row['sceneIndex'] == index, 'scene-order')
        require(row['path'] == 'results/scenes/'+SCENE_IDS[index]+'.json', 'scene-path')
        require(type(row['bytes']) is int and 0 < row['bytes'] <= SCENE_LIMIT,
                'scene-byte-shape')
        for key in ('sha256','rawInputSha256'):
            require(type(row[key]) is str and re.fullmatch('[0-9a-f]{64}',row[key]),
                    'scene-pin-shape')
        representatives = row['representatives']
        require(type(representatives) is list and len(representatives) == 2,
                'representative-count')
        for mi, representative in enumerate(representatives):
            fields(representative, contract['storage']['representativeFields'],
                   'representative-fields')
            require(representative['method'] == METHODS[mi] and
                    type(representative['trialSequence']) is int and
                    representative['trialSequence'] == index*10+2+mi,
                    'representative-selection')
            for key in ('scientificDigest','commonDigest'):
                require(type(representative[key]) is str and
                        re.fullmatch('[0-9a-f]{64}',representative[key]), 'representative-digest-shape')
    require(sum(row['bytes'] for row in descriptors) <= SCIENCE_LIMIT, 'science-corpus-budget')


def validate_ledger(document, contract):
    trials = document.get('trials')
    require(type(trials) is list and len(trials) == 60, 'trial-schedule')
    # All schedule checks precede timing and binding, including fresh control13.
    for sequence, trial in enumerate(trials):
        fields(trial, contract['trialProtocol']['trialFields'], 'trial-fields')
        scene_index, local = divmod(sequence, 10)
        repetition, position = divmod(local, 2)
        method = METHODS[0 if ORDERS[repetition][position] == 'A' else 1]
        require(type(trial['sequence']) is int and trial['sequence'] == sequence and
                type(trial['sceneIndex']) is int and trial['sceneIndex'] == scene_index and
                trial['sceneId'] == SCENE_IDS[scene_index] and
                trial['phase'] == ('warmup' if repetition == 0 else 'measured') and
                type(trial['repetition']) is int and trial['repetition'] == repetition and
                trial['pairOrder'] == ORDERS[repetition] and
                type(trial['pairPosition']) is int and trial['pairPosition'] == position and
                trial['method'] == method, 'trial-schedule')
    previous = 0
    for si in range(6):
        start, end, _ = interval(document['scenes'][si]['inputConversionTiming'])
        require(start >= previous, 'input-conversion-chronology')
        previous = end
        for trial in trials[si*10:(si+1)*10]:
            timing = trial['timing']
            fields(timing, contract['trialProtocol']['timingFields'], 'timing-fields')
            start, end, total = interval({k:timing[k] for k in ('startNs','endNs','totalNs')}, True)
            require(start >= previous, 'trial-time-overlap')
            fields(timing['offsetsNs'], contract['trialProtocol']['offsetFields'], 'timing-offset-fields')
            offsets = [time_integer(timing['offsetsNs'][k])
                       for k in contract['trialProtocol']['offsetFields']]
            require(0 <= offsets[0] <= offsets[1] <= offsets[2] <= offsets[3] == total,
                    'timing-offset-order')
            fields(timing['stagesNs'], contract['trialProtocol']['stageFields'], 'timing-stage-fields')
            stages = [time_integer(timing['stagesNs'][k])
                      for k in contract['trialProtocol']['stageFields']]
            require(stages == [offsets[0]]+[offsets[i]-offsets[i-1] for i in range(1,4)] and
                    sum(stages) == total, 'timing-stage-partition')
            harness = trial['harnessTiming']
            fields(harness, contract['trialProtocol']['harnessTimingFields'], 'harness-fields')
            hs, he, ht = interval({k:harness[k] for k in ('startNs','endNs','totalNs')})
            require(hs >= end and time_integer(harness['serializationNs'])+
                    time_integer(harness['hashNs']) == ht, 'harness-time-partition')
            previous = he
            for key in ('scientificDigest','commonDigest'):
                require(type(trial[key]) is str and re.fullmatch('[0-9a-f]{64}',trial[key]),
                        'trial-digest-shape')
            fields(trial['work'], contract['trialProtocol']['workFields'], 'trial-work-fields')
            require(all(type(v) is int and 0 <= v <= 10**9 for v in trial['work'].values()),
                    'trial-work-shape')
    expected = [summary(trials[i*10:(i+1)*10], SCENE_IDS[i]) for i in range(6)]
    require(same(document.get('summaries'), expected), 'timing-summary-reconstruction')
    require(type(document.get('primaryBenefitPassed')) is bool and
            document['primaryBenefitPassed'] == all(x['practicalBenefitPassed'] for x in expected[:3]),
            'primary-benefit-reconstruction')
    return expected


def digest_envelopes(record, positives, context, contract):
    method_digests, common_digests = {}, {}
    for method, scientific, canonical_positive in zip(METHODS, record['methods'], positives):
        envelope = dict(domain=contract['encoding']['methodDigestDomain'], **context,
                        method=method, scientific=scientific)
        method_digests[method] = canonical_hash(envelope)
        common = {k:scientific[k] for k in ('prepared','result','solve','certificate')}
        common['canonicalPositiveEntries'] = canonical_positive
        common_digests[method] = canonical_hash(dict(
            domain=contract['encoding']['commonDigestDomain'], **context, scientific=common))
    return method_digests, common_digests


def bind_trials(trials, descriptor, method_digests, common_digests, expected_work):
    for trial in trials:
        method = trial['method']
        require(trial['scientificDigest'] == method_digests[method], 'trial-scientific-digest-binding')
        require(trial['commonDigest'] == common_digests[method], 'trial-common-digest-binding')
        require(same(trial['work'], expected_work[method]), 'trial-work-reconstruction')
    for row in descriptor['representatives']:
        method = row['method']
        require(row['scientificDigest'] == method_digests[method] and
                row['commonDigest'] == common_digests[method], 'representative-digest-binding')


def check_journal(path, document, contract, result_pin):
    require(path.stat().st_size <= JOURNAL_LIMIT, 'journal-byte-budget')
    expected = [('run-start', {k:document[k] for k in
                 ('specSha256','sourceManifestSha256','runtime','sourceSha256','constants')})]
    for si, descriptor in enumerate(document['scenes']):
        expected.append(('input-ready', {'sceneIndex':si,'sceneId':descriptor['id'],
            'rawInputSha256':descriptor['rawInputSha256'],
            'inputConversionTiming':descriptor['inputConversionTiming']}))
        for local, trial in enumerate(document['trials'][si*10:(si+1)*10]):
            expected.append(('trial-complete',trial))
            if local == 3:
                expected.append(('representative-shard',descriptor))
        expected.append(('scene-complete', {'sceneIndex':si,'sceneId':descriptor['id'],
            'firstSequence':si*10,'lastSequence':si*10+9,'sha256':descriptor['sha256']}))
    expected.append(('run-complete', {'resultPath':'results/timing-index.json',
        'resultBytes':result_pin['bytes'],'resultSha256':result_pin['sha256'],
        'trialCount':60,'sceneCount':6}))
    with path.open('rb') as handle:
        for index, (kind, payload) in enumerate(expected):
            line = handle.readline(65537)
            require(line.endswith(b'\n') and len(line) <= 65536, 'journal-line-budget-or-ending')
            row = decode(line)
            require_canonical_line_bytes(line, row)
            fields(row, ('schema','eventSequence','type','payload'), 'journal-event-fields')
            require(row['schema'] == contract['journal']['schema'] and
                    type(row['eventSequence']) is int and row['eventSequence'] == index and
                    row['type'] == kind and same(row['payload'],payload), 'journal-event-binding')
        require(not handle.read(1), 'journal-extra-data')
    return {'passed':True,'events':len(expected),**file_pin(path,JOURNAL_LIMIT)}


def control_result(name, witness, operation, recipes, exception_class):
    require(canonical_size(witness) <= 65536, 'control-witness-byte-budget')
    families = recipes[name]['failurePrefixes']
    error = None
    try:
        operation()
    except exception_class as failure:
        error = str(failure)[:256]
    except Exception as failure:
        error = 'control-exception:'+type(failure).__name__
    targeted = error is not None and any(error.startswith(prefix) for prefix in families)
    return {'name':name,'executed':True,'rejected':error is not None,
            'intendedCoreFailure':targeted,'requiredFailureFamilies':families,
            'witness':witness,'errors':[] if error is None else [error]}


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
    expected.update(filterPrepared=len(target['input']['drones']) if on else 0,
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


def filter_controls(record,target,semantic,helper,constants,recipes,completed):
    if all(name in completed for name in ('false-fast-zero-positive','wrong-fast-zero-branch','filter-work-mismatch')):
        return
    method=record['methods'][1]
    def run(name,witness,mutate):
        if name in completed:
            return
        clone=copy.deepcopy(method)
        mutate(clone)
        completed[name]=control_result(name,witness,
            lambda:validate_filter_method(clone,target,'filtered',constants,helper,semantic,False),
            recipes,semantic.CheckError)
        del clone
    for qi,query in enumerate(method['assembly']['queries']):
        for ti,terminal in enumerate(query['terminals']):
            if terminal['kind'] not in ('leaf','scan'):
                continue
            if 'false-fast-zero-positive' not in completed:
                for ei,entry in enumerate(terminal['entries']):
                    pair=target['lookup'][(query['i'],query['r'],entry['j'])]
                    if pair['oracle']['status']!='positive' or pair['coefficient'][0]<=0:
                        continue
                    witness={'scene':record['id'],'receiverIndex':query['i'],'r':query['r'],
                             'sourceIndex':entry['j'],'coefficient':semantic.interval_wire(pair['coefficient'])}
                    def false_fast(clone):
                        t=clone['assembly']['queries'][qi]['terminals'][ti]
                        j=t['entries'].pop(ei)['j']
                        t['zeroCount']+=1
                        t['filterZeros'].append({'j':j,'branch':'neighbor'})
                        t['filterZeros'].sort(key=lambda item:item['j'])
                        clone['assembly']['work']['filterZeros']+=1
                        clone['assembly']['work']['exactScalarCalls']-=1
                    run('false-fast-zero-positive',witness,false_fast)
                    break
            if 'wrong-fast-zero-branch' not in completed:
                for zi,zero in enumerate(terminal['filterZeros']):
                    oracle=target['lookup'][(query['i'],query['r'],zero['j'])]['oracle']
                    require(oracle['status']=='zero' and zero['branch']==oracle['branch'],
                            'filter-branch-control-witness')
                    changed=next(branch for branch in FILTER_BRANCHES if branch!=oracle['branch'])
                    witness={'scene':record['id'],'receiverIndex':query['i'],'r':query['r'],
                             'sourceIndex':zero['j'],'referenceBranch':oracle['branch'],'changedBranch':changed}
                    def wrong_branch(clone):
                        clone['assembly']['queries'][qi]['terminals'][ti]['filterZeros'][zi]['branch']=changed
                    run('wrong-fast-zero-branch',witness,wrong_branch)
                    break
    if 'filter-work-mismatch' not in completed:
        expected=method['assembly']['work']['scalarPairs']-method['assembly']['work']['filterZeros']
        require(expected==method['assembly']['work']['exactScalarCalls'],'filter-work-control-witness')
        def wrong_work(clone):
            clone['assembly']['work']['exactScalarCalls']+=1
        run('filter-work-mismatch',{'scene':record['id'],'scalarPairs':method['assembly']['work']['scalarPairs'],
            'validatedFilterZeros':method['assembly']['work']['filterZeros'],
            'expectedExactScalarCalls':expected,'changedExactScalarCalls':expected+1},wrong_work)


def scientific_controls(record, target, semantic, helper, constants, recipes, completed):
    method = record['methods'][0]
    def run(name, witness, mutate):
        if name in completed:
            return
        clone = copy.deepcopy(method)
        mutate(clone)
        def validate():
            validate_filter_method(clone,target,'hierarchy',constants,helper,semantic,False)
        completed[name] = control_result(name,witness,validate,recipes,semantic.CheckError)
        del clone
    for qi, query in enumerate(method['assembly']['queries']):
        for ti, terminal in enumerate(query['terminals']):
            if terminal['kind'] != 'leaf':
                continue
            for ei, entry in enumerate(terminal['entries']):
                pair = target['lookup'][(query['i'],query['r'],entry['j'])]
                if pair['oracle']['status'] != 'positive':
                    continue
                witness = {'scene':record['id'],'receiverIndex':query['i'],'r':query['r'],
                    'sourceIndex':entry['j'],'i':pair['i'],'j':pair['j'],
                    'coefficient':semantic.interval_wire(pair['coefficient'])}
                def omit(clone):
                    value=clone['assembly']['queries'][qi]['terminals'][ti]
                    value['entries'].pop(ei)
                    value['zeroCount']+=1
                run('omitted-positive-entry',witness,omit)
                members=[j for j in target['members'][terminal['node']] if j != query['i']]
                def false_zero(clone):
                    clone['assembly']['queries'][qi]['terminals'][ti]={
                        'kind':'zero','node':terminal['node'],'rule':'neighbor','count':len(members)}
                run('false-zero-active-leaf',dict(witness,node=terminal['node'],memberCount=len(members)),false_zero)
                if pair['coefficient'][0] > 0:
                    def coefficient(clone):
                        clone['assembly']['queries'][qi]['terminals'][ti]['entries'][ei]['result']['coefficient']={'l':'0','u':'0'}
                    run('altered-positive-coefficient',witness,coefficient)
                if all(n in completed for n in ('omitted-positive-entry','false-zero-active-leaf',
                                               'altered-positive-coefficient')):
                    break
            if all(n in completed for n in ('omitted-positive-entry','false-zero-active-leaf',
                                           'altered-positive-coefficient')):
                break
        if all(n in completed for n in ('omitted-positive-entry','false-zero-active-leaf',
                                       'altered-positive-coefficient')):
            break
    for di, drone in enumerate(target['input']['drones']):
        identifier=drone['id']
        for rotor in range(4):
            reference=target['roots'][(identifier,rotor)]
            word=helper.parse_bits(method['solve']['candidate'][di]['x'][rotor])
            proposal=helper.dyadic(word)
            witness={'scene':record['id'],'id':identifier,'r':rotor,
                     'referenceRoot':semantic.interval_wire(reference)}
            if reference[1] < 1:
                def root_one(clone):
                    clone['certificate']['rows'][di*4+rotor]['xstar']={
                        'l':str(1<<96),'u':str(1<<96)}
                run('false-root-one',witness,root_one)
                changed=word^1
                if helper.finite(changed) and 0 < helper.dyadic(changed) <= 1:
                    def candidate(clone):
                        clone['solve']['candidate'][di]['x'][rotor]=helper.hex_bits(changed)
                    expected_load=target['exact'][identifier]['forces'][rotor]*helper.dyadic(changed)
                    old_load=semantic.rational(method['certificate']['loads'][di]['candidate']['rotor'][rotor])
                    require(expected_load != old_load,'candidate-control-identity-witness')
                    run('altered-candidate',dict(witness,originalWord=helper.hex_bits(word),
                        changedWord=helper.hex_bits(changed),originalLoad=semantic.fraction_wire(old_load),
                        changedExactLoad=semantic.fraction_wire(expected_load)),candidate)
            if rotor == 0:
                original=semantic.rational(method['certificate']['loads'][di]['candidate']['rotor'][0])
                def altered_load(clone):
                    clone['certificate']['loads'][di]['candidate']['rotor'][0]=semantic.fraction_wire(original+1)
                run('altered-candidate-load',dict(witness,original=semantic.fraction_wire(original),
                    altered=semantic.fraction_wire(original+1)),altered_load)
            load_reference=target['loads'][identifier]['rotor'][rotor]
            if load_reference[0] > 0:
                def load_zero(clone):
                    clone['certificate']['loads'][di]['bounds']['rotor'][rotor]={'l':'0','u':'0'}
                run('false-load-box',dict(witness,referenceLoad=semantic.interval_wire(load_reference)),load_zero)
            if proposal < reference[0] or proposal > reference[1]:
                gap=reference[0]-proposal if proposal < reference[0] else proposal-reference[1]
                normalized=target['exact'][identifier]['forces'][rotor]*gap/(constants['mg']/4)
                require(normalized > 0,'error-control-positive-witness')
                def error_zero(clone):
                    clone['certificate']['loads'][di]['error']['rotor'][rotor]='0'
                run('false-error-zero',dict(witness,candidate=semantic.fraction_wire(proposal),
                    strictNormalizedErrorLowerBound=semantic.fraction_wire(normalized)),error_zero)
        if all(n in completed for n in ('false-root-one','altered-candidate',
                'altered-candidate-load','false-load-box','false-error-zero')):
            break


def metadata_controls(document, contract, recipes, completed):
    for name in ('missing-scene','duplicate-scene','reordered-scenes'):
        clone={'scenes':copy.deepcopy(document['scenes'])}
        if name == 'missing-scene':
            clone['scenes'].pop()
        elif name == 'duplicate-scene':
            clone['scenes'][1]=copy.deepcopy(clone['scenes'][0])
        else:
            clone['scenes'][0],clone['scenes'][1]=clone['scenes'][1],clone['scenes'][0]
        completed[name]=control_result(name,{'expected':list(SCENE_IDS),
            'observed':[row['id'] for row in clone['scenes']]},
            lambda:validate_scene_index(clone,contract),recipes,CheckError)
    for name in ('timing-partition-mismatch','trial-order-mismatch'):
        clone=copy.deepcopy(document)
        if name == 'timing-partition-mismatch':
            stages=clone['trials'][2]['timing']['stagesNs']
            stages['preparation']=str(time_integer(stages['preparation'])+1)
        else:
            clone['trials'][2],clone['trials'][3]=clone['trials'][3],clone['trials'][2]
        completed[name]=control_result(name,{'scene':SCENE_IDS[0],'trialSequence':2},
            lambda:validate_ledger(clone,contract),recipes,CheckError)


def binding_controls(trials, descriptor, digests, common, work, recipes, completed):
    for name in ('trial-digest-mismatch','trial-work-mismatch'):
        clone=copy.deepcopy(trials)
        if name == 'trial-digest-mismatch':
            old=clone[2]['scientificDigest']
            clone[2]['scientificDigest']=('1' if old == '0'*64 else '0')*64
        else:
            clone[2]['work']['scalarPairs']+=1
        completed[name]=control_result(name,{'scene':SCENE_IDS[0],'trialSequence':2,
            'expectedDigest':digests['hierarchy'],'expectedWork':work['hierarchy']},
            lambda:bind_trials(clone,descriptor,digests,common,work),recipes,CheckError)


def clear_reference_caches(helper):
    for name in ('dyadic','rn','literal','fp_add','fp_mul','rotate_bits'):
        function=getattr(helper,name)
        function.cache_clear()


class Parser(argparse.ArgumentParser):
    def error(self, _message):
        raise CheckError('invalid-command-line')


def main(argv=None):
    parser=Parser(description='Independent streaming saved scientific/timing checker')
    for name in ('spec','input','manifest','output','root'):
        parser.add_argument('--'+name,required=True)
    try:
        args=parser.parse_args(argv)
    except CheckError:
        print('{"passed":false,"error":"invalid-command-line"}',file=sys.stderr)
        return 2
    report={'schema':'m31-filter-cost-independent-check-v1','passed':False,
        'verificationPassed':False,'fullQualification':False,'tolerancePassed':False,
        'scientificQualification':False,'trialDigestConsistency':False,'timingIntegrity':False,
        'totalRecords':0,'qualifiedRecords':0,'admittedRecords':0,
        'scenes':[],'faultControls':[],'errors':[],
        'checkerRuntime':{'pythonVersion':'.'.join(str(v) for v in sys.version_info[:3]),
                          'implementation':sys.implementation.name},
        'scope':'Six static Node scenes; every logical pair and full-model load check retained; timings descriptive; no 5000-drone/browser/dynamics/physical/novelty conclusion.'}
    output_allowed=False
    evidence_bytes=0
    inputs=[]
    indexed=None
    completed={}
    recipes={}
    try:
        root=Path(args.root).resolve(strict=True)
        spec_path=Path(args.spec)
        package=spec_path.parent.parent.resolve(strict=True)
        input_path,manifest_path,output=Path(args.input),Path(args.manifest),Path(args.output)
        require(input_path.resolve(strict=True) == package/'results/timing-index.json', 'input-path')
        require(output.absolute() == package/'results/independent-check.json', 'output-path')
        relative(output.parent,root)
        output_allowed=True
        contract_path=spec_path.parent/'result-contract.json'
        semantic_path=spec_path.parent/'semantic-reference.py'
        pair_path=spec_path.parent/'pair-reference.py'
        required=[spec_path.parent/name for name in SOURCE_FILES]+[Path(__file__),semantic_path,pair_path]
        required += [package/name for name in ('PROTOCOL.md','MODEL.md','runtime-pins.json','source/supervise.py','source/guardian.py')]
        indexed=verify_sources(manifest_path,root,required)
        manifest_pin=file_pin(manifest_path,1024*1024)
        semantic=independent_module(semantic_path,root,indexed,'m31_filter_cost_semantic_reference',SEMANTIC_SHA)
        helper=independent_module(pair_path,root,indexed,'m31_filter_cost_pair_reference',PAIR_SHA)
        spec,contract=load(spec_path,2*1024*1024),load(contract_path,256*1024)
        require(contract['schema']=='m31-filter-cost-result-contract-v1','contract-schema')
        require(contract['controls']['count']==18 and len(contract['controls']['recipes'])==18,
                'contract-control-count')
        validate_spec(spec)
        require(same(contract['sourceFiles'],list(SOURCE_FILES)), 'source-closure-contract')
        require(same(contract['methods'],list(METHODS)), 'contract-methods')
        source_hashes={}
        for name in contract['sourceFiles']:
            key=relative(spec_path.parent/name,root)
            require(key in indexed,'candidate-source-not-pinned')
            source_hashes[name]=indexed[key]['sha256']
        bits,trace=helper.constants_from_graph(spec)
        constants={name:helper.dyadic(word) for name,word in bits.items()}
        table={name:helper.hex_bits(word) for name,word in bits.items()}
        document=load(input_path,INDEX_LIMIT,canonical_line=True)
        fields(document,contract['storage']['resultFields'],'index-fields')
        spec_sha=indexed[relative(spec_path,root)]['sha256']
        require(document['schema']==contract['storage']['resultSchema'] and
                document['specId']==spec['id'] and document['specSha256']==spec_sha and
                document['sourceManifestSha256']==manifest_pin['sha256'],'index-identity')
        require(same(document['sourceSha256'],source_hashes),'source-hash-report')
        require(same(document['constants'],table),'constant-encoding-graph')
        require(document['clock']=='process.hrtime.bigint' and
                document['recordedHarnessScope']==contract['trialProtocol']['recordedHarnessScope'],
                'timing-clock-or-scope')
        fields(document['runtime'],('node','v8','platform','arch'),'runtime-fields')
        require(all(type(v) is str and 1<=len(v)<=256 for v in document['runtime'].values()),
                'runtime-values')
        validate_scene_index(document,contract)
        summaries=validate_ledger(document,contract)
        report['timingIntegrity']=True
        report['timingSummaries']=summaries
        report['primaryBenefitPassed']=document['primaryBenefitPassed']
        report['benefitScope']='All three dense scene medianPairedRatio<=9/10 and strict wins>=3/4; sparse contextual; separate from scientific qualification.'
        journal_path=Path(str(input_path)+'.jsonl')
        result_pin=file_pin(input_path,INDEX_LIMIT)
        inputs=[(input_path,INDEX_LIMIT,result_pin),(journal_path,JOURNAL_LIMIT,file_pin(journal_path,JOURNAL_LIMIT))]
        report['journal']=check_journal(journal_path,document,contract,result_pin)
        scene_dir=package/'results/scenes'
        require(scene_dir.is_dir() and not scene_dir.is_symlink() and
                {p.name for p in scene_dir.iterdir()} == {s+'.json' for s in SCENE_IDS},
                'unexpected-scientific-scene-files')
        anomaly_dir=package/'results/anomalies'
        require(not anomaly_dir.exists() or (anomaly_dir.is_dir() and not anomaly_dir.is_symlink() and
                not any(anomaly_dir.iterdir())), 'anomaly-present-on-success')
        for descriptor in document['scenes']:
            path=package/descriptor['path']
            require(relative(path,package)==descriptor['path'],'scene-path-not-canonical')
            pin=file_pin(path,SCENE_LIMIT)
            require(pin=={k:descriptor[k] for k in ('bytes','sha256')},'scene-file-pin')
            inputs.append((path,SCENE_LIMIT,pin))
        recipes={row['name']:row for row in contract['controls']['recipes']}
        require(len(recipes)==18,'duplicate-control-name')
        metadata_controls(document,contract,recipes,completed)
        reference_dir=output.parent/'reference-scenes'
        reference_dir.mkdir(exist_ok=True)
        require(not reference_dir.is_symlink() and not any(reference_dir.iterdir()),
                'reference-output-not-fresh')
        directory=os.open(output.parent,os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        for scene_index,scene in enumerate(spec['scenes']):
            descriptor=document['scenes'][scene_index]
            path=package/descriptor['path']
            record=load(path,SCENE_LIMIT,canonical_line=True)
            fields(record,contract['storage']['sceneFields'],'scene-fields')
            require(record['schema']==contract['storage']['sceneSchema'] and
                    record['specId']==spec['id'] and record['specSha256']==spec_sha and
                    record['sourceManifestSha256']==manifest_pin['sha256'] and
                    record['id']==scene['id'],'scene-identity')
            semantic_scene={k:scene[k] for k in ('id','family','expectedClass','drones')}
            target=semantic.regenerate_scene(semantic_scene,spec,bits,helper)
            require(target['status']=='admitted' and target['referenceClass']=='admitted',
                    'declared-reference-class-disagreement')
            require(same(record['input'],target['input']),'raw-input-regeneration')
            raw_sha=canonical_hash({'domain':contract['encoding']['rawInputDigestDomain'],
                                   'sceneId':scene['id'],'input':target['input']})
            require(record['rawInputSha256']==raw_sha==descriptor['rawInputSha256'],
                    'raw-input-digest-binding')
            require(type(record['methods']) is list and len(record['methods'])==2,'method-count')
            method_reports,positives,reference=[],[],None
            for method_index,method in enumerate(METHODS):
                evidence,positive=validate_filter_method(record['methods'][method_index],target,
                    method,constants,helper,semantic,method_index==0)
                emitted=evidence.pop('independentReference',None)
                if emitted:
                    reference=emitted
                method_reports.append(evidence)
                positives.append(positive)
            for key in ('prepared','result','solve','certificate'):
                require(same(record['methods'][0][key],record['methods'][1][key]),'method-equality:'+key)
            require(same(positives[0],positives[1]),'method-equality:positive-coefficients')
            context={'specSha256':spec_sha,'sourceManifestSha256':manifest_pin['sha256'],
                     'sceneId':scene['id'],'rawInputSha256':raw_sha}
            digests,common=digest_envelopes(record,positives,context,contract)
            require(common['hierarchy']==common['filtered'],'common-digest-equality')
            work={method:method_reports[i]['work'] for i,method in enumerate(METHODS)}
            trials=document['trials'][scene_index*10:(scene_index+1)*10]
            bind_trials(trials,descriptor,digests,common,work)
            if scene_index==0:
                binding_controls(trials,descriptor,digests,common,work,recipes,completed)
            scientific_controls(record,target,semantic,helper,constants,recipes,completed)
            filter_controls(record,target,semantic,helper,constants,recipes,completed)
            require(reference is not None,'reference-evidence-missing')
            reference_payload={'schema':'m31-filter-cost-reference-scene-v1','sceneId':scene['id'],
                'rawInputSha256':raw_sha,'plannedPairsPerMethod':target['planned'],
                'referenceCoefficientBits':192,'referenceSourceBits':192,'referenceRootBisections':128,
                'independentReference':reference}
            ref_path=reference_dir/(scene['id']+'.json')
            ref_pin=write_exclusive(ref_path,reference_payload,CHECKER_LIMIT-evidence_bytes-2*1024*1024)
            evidence_bytes+=ref_pin['bytes']
            report['scenes'].append({'id':scene['id'],'referenceClass':target['referenceClass'],
                'plannedPairsPerMethod':target['planned'],'verified':True,'methodEquality':True,
                'methods':method_reports,'methodDigests':digests,'commonDigests':common,
                'referenceEvidence':dict(path='reference-scenes/'+ref_path.name,**ref_pin)})
            report['totalRecords']+=1
            report['qualifiedRecords']+=1
            report['admittedRecords']+=1
            # Nothing in the persistent report/completed controls references these graphs.
            del record,target,positives,reference,reference_payload,method_reports,evidence,positive,emitted
            del work,trials,digests,common,context,semantic_scene
            clear_reference_caches(helper)
        require(len(completed)==18 and set(completed)==set(recipes),'control-proven-witness-missing')
        report['faultControls']=[completed[row['name']] for row in contract['controls']['recipes']]
        require(all(row['executed'] and row['rejected'] and row['intendedCoreFailure']
                    for row in report['faultControls']), 'negative-controls-incomplete-or-ineffective')
        report['scientificQualification']=True
        report['trialDigestConsistency']=True
        report['fullQualification']=report['qualifiedRecords']==6
        report['tolerancePassed']=all(m['toleranceAchieved'] is True
                                      for scene in report['scenes'] for m in scene['methods'])
        require(report['tolerancePassed'],'load-tolerance-not-achieved')
        report['expectedPlannedPairsPerMethod']=422560
        report['independentCoefficientOutcomes']=422560
        report['validatedMethodOutcomes']=845120
        report['expectedConstantEncodings']=table
        report['constantGraphIntermediateEncodings']=trace
        report['sourceManifest']=dict(path=relative(manifest_path,root),**manifest_pin)
        report['verifiedSources']=list(indexed.values())
        report['input']=dict(path=relative(input_path,root),**result_pin)
        report['verificationPassed']=True
        report['passed']=True
    except Exception as error:
        if isinstance(error,CheckError) or type(error).__name__=='CheckError':
            report['errors'].append(str(error)[:256])
        else:
            report['errors'].append('checker-exception:'+type(error).__name__)
    if completed:
        report['faultControls']=[completed[name] for name in recipes if name in completed]
    # Recheck source and input pins even when scientific validation failed.
    if indexed is not None:
        try:
            after=verify_sources(manifest_path,root,required)
            require(same(after,indexed) and file_pin(manifest_path,1024*1024)==manifest_pin,
                    'source-after-mismatch')
            for path,limit,pin in inputs:
                require(file_pin(path,limit)==pin,'input-after-mismatch')
            report['sourcesUnchangedAfter']=True
            report['inputsUnchangedAfter']=True
        except Exception as error:
            report['errors'].append(str(error)[:256] if type(error).__name__=='CheckError'
                                    else 'after-pin-exception:'+type(error).__name__)
    if report['errors']:
        for key in ('passed','verificationPassed','fullQualification','tolerancePassed'):
            report[key]=False
    report['errors']=report['errors'][:48]
    report['errorCount']=len(report['errors'])
    report['referenceEvidenceBytes']=evidence_bytes
    try:
        require(output_allowed,'report-output-not-allowed')
        write_exclusive(output,report,CHECKER_LIMIT-evidence_bytes)
    except Exception:
        print('{"passed":false,"error":"exclusive-report-write-failed"}',file=sys.stderr)
        return 2
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
