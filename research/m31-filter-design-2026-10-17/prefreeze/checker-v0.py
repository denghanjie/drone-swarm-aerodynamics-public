#!/usr/bin/env python3
"""Independent saved-record validation. No candidate imports or subprocesses.

Only the fixed inherited independent helper is compiled from manifest-pinned
bytes, inside the authorized main execution. Old suites and controls are uncalled.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import types

INPUT_LIMIT = 16 * 1024 * 1024
OUTPUT_LIMIT = 32 * 1024 * 1024
SOURCE_LIMIT = 16 * 1024 * 1024
HELPER_SHA = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
SCHEMA = 'm31-filter-correctness-result-v1'
JOURNAL_SCHEMA = 'm31-filter-correctness-journal-v1'
SPEC_ID = 'm31-filter-correctness-v1'
OPS = ('add', 'sub', 'mul', 'div', 'square')
ZERO_BRANCHES = ('neighbor', 'upstream', 'down-cut', 'near-outside', 'radial', 'projection')
CONTROL_IDS = ('inward-add-upper', 'inward-add-lower', 'lost-underflow', 'finite-overflow',
               'zero-divisor', 'lost-square-zero', 'false-positive-zero', 'guard-preempted',
               'wrong-zero-branch', 'altered-prepared-point', 'lost-fallback-coefficient',
               'preparation-bypassed', 'missing-row', 'duplicate-row', 'reordered-rows',
               'journal-disagreement')
CONTROL_FAILURES = ('primitive-containment', 'primitive-containment', 'primitive-containment',
                    'primitive-containment', 'primitive-domain', 'primitive-containment',
                    'candidate-target-status', 'candidate-target-status', 'candidate-target-branch',
                    'prepared-operation-graph', 'candidate-containment-coefficient',
                    'preparation-gate', 'record-count', 'duplicate-record-id', 'record-order',
                    'journal-row-agreement')
ENCODER = json.JSONEncoder(separators=(',', ':'), ensure_ascii=True, allow_nan=False)


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
        require(abs(value) <= 2**53-1, 'unsafe-json-integer')
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


def parse_integer(token):
    require(token != '-0' and len(token) <= 17, 'invalid-json-integer')
    value = int(token)
    require(abs(value) <= 2**53-1, 'unsafe-json-integer')
    return value


def reject_number(_token):
    raise CheckError('float-or-constant-json-token')


def decode(data):
    try:
        value = json.loads(data, object_pairs_hook=no_duplicates, parse_int=parse_integer,
                           parse_float=reject_number, parse_constant=reject_number)
        ascii_value(value)
        return value
    except (UnicodeError, ValueError, RecursionError):
        raise CheckError('invalid-json') from None


def compact(value):
    return ENCODER.encode(value).encode('ascii') + b'\n'


def read_bytes(path, limit):
    require(path.is_file() and not path.is_symlink(), 'required-file-missing-or-symlink')
    require(path.stat().st_size <= limit, 'input-file-budget')
    data = path.read_bytes()
    require(len(data) <= limit, 'input-file-budget')
    return data


def load(path, limit, strict=False):
    data = read_bytes(path, limit)
    value = decode(data)
    if strict:
        require(data == compact(value), 'artifact-compact-line-format')
    return value


def pin(path, limit=SOURCE_LIMIT):
    data = read_bytes(path, limit)
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def relative(path, root):
    try:
        result = path.resolve(strict=True).relative_to(root).as_posix()
    except (OSError, ValueError):
        raise CheckError('path-outside-root-or-missing') from None
    require(not path.is_symlink(), 'symlink-path')
    return result


def verify_sources(path, root, required):
    manifest = load(path, 1024*1024)
    require(type(manifest) is dict and type(manifest.get('files')) is list,
            'source-manifest-shape')
    require(1 <= len(manifest['files']) <= 256, 'source-manifest-count')
    indexed, total = {}, 0
    for item in manifest['files']:
        fields(item, ('path', 'bytes', 'sha256'), 'source-manifest-row')
        name = item['path']
        require(type(name) is str and 0 < len(name) <= 512 and '\\' not in name,
                'source-manifest-path')
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and str(parts) == name and
                all(p not in ('.', '..') for p in parts.parts) and name not in indexed,
                'source-manifest-duplicate-or-path')
        target = root/name
        require(relative(target, root) == name, 'source-path-not-canonical')
        actual = pin(target)
        require(type(item['bytes']) is int and item['bytes'] == actual['bytes'] and
                item['sha256'] == actual['sha256'], 'source-manifest-pin-mismatch')
        indexed[name] = dict(path=name, **actual)
        total += actual['bytes']
        require(total <= 64*1024*1024, 'source-total-budget')
    require(all(relative(target, root) in indexed for target in required),
            'required-source-not-pinned')
    return indexed


def independent_module(path, root, indexed):
    source = read_bytes(path, SOURCE_LIMIT)
    declared = indexed[relative(path, root)]
    digest = hashlib.sha256(source).hexdigest()
    require(len(source) == declared['bytes'] and digest == declared['sha256'] == HELPER_SHA,
            'independent-source-buffer-pin')
    module = types.ModuleType('m31_filter_independent_reference')
    module.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), module.__dict__)
    return module


def validate_spec_contract(spec, contract):
    require(spec.get('id') == SPEC_ID and spec.get('expectedRecords') == 108 and
            spec.get('expectedPrimitiveRecords') == 72 and spec.get('expectedPairRecords') == 36
            and spec.get('fractionBits') == 96 and spec.get('referenceBits') == 192,
            'spec-allocation')
    require(same(spec.get('corners'), [[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]]), 'spec-corners')
    records = spec.get('records')
    require(type(records) is list and len(records) == 108, 'spec-record-count')
    ids, counts = set(), Counter()
    for item in records:
        require(type(item) is dict and type(item.get('id')) is str and
                re.fullmatch(r'[a-z0-9-]{1,64}', item['id']) is not None and item['id'] not in ids,
                'spec-record-id')
        ids.add(item['id'])
        counts[item.get('kind')] += 1
        if item.get('kind') == 'primitive':
            op = item.get('op')
            require(op in OPS + ('nextUp', 'nextDown'), 'spec-primitive-operation')
            fields(item, ('kind','id','op','word' if op in ('nextUp','nextDown') else 'args'),
                   'spec-primitive-fields')
        else:
            fields(item, ('kind','id','receiver','source','rotor'), 'spec-pair-fields')
            require(item['kind'] == 'pair' and type(item['rotor']) is int and 0 <= item['rotor'] < 4,
                    'spec-pair-query')
            require(all(type(item[side]) is list and len(item[side]) == 17
                        for side in ('receiver','source')), 'spec-raw-word-count')
    require(counts == {'primitive':72, 'pair':36}, 'spec-family-allocation')
    require(contract.get('schema') == SCHEMA and contract.get('journalSchema') == JOURNAL_SCHEMA
            and contract.get('specId') == SPEC_ID and contract.get('expectedRecords') == 108
            and contract.get('primitiveRecords') == 72 and contract.get('pairRecords') == 36
            and contract.get('journalEvents') == 110, 'contract-allocation')
    recipes = contract.get('controls', {}).get('recipes')
    require(contract.get('controls', {}).get('count') == 16 and type(recipes) is list and
            tuple(x.get('id') for x in recipes) == CONTROL_IDS and
            tuple(x.get('failure') for x in recipes) == CONTROL_FAILURES, 'contract-controls')
    require(same(contract.get('fastZeroBranches'), list(ZERO_BRANCHES)), 'contract-zero-branches')
    require(same(contract.get('coverage'), {'finiteIntervalPerOperation':list(OPS),
            'minimumFastZeros':1, 'minimumPositiveFallbacks':1,
            'requiredPositiveFallbackId':'tail-positive', 'allSixZeroBranchesRequired':False,
            'allControlWitnessesRequired':True}), 'contract-coverage')
    return records


def primitive_reference(item, helper):
    op = item['op']
    if op in ('nextUp', 'nextDown'):
        word = helper.parse_bits(item['word'])
        if not helper.finite(word):
            return {'domain':'nonfinite'}
        magnitude = word & ((1 << 63)-1)
        if magnitude == 0:
            adjacent = 1 if op == 'nextUp' else (1 << 63) | 1
        elif op == 'nextUp':
            adjacent = word-1 if word >> 63 else word+1
        else:
            adjacent = word+1 if word >> 63 else word-1
        return {'word':format(adjacent, '016x')}
    args = item['args']
    require(type(args) is list and len(args) == (1 if op == 'square' else 2), 'spec-argument-count')
    words = []
    for arg in args:
        fields(arg, ('l','u'), 'spec-interval-fields')
        words.append(tuple(helper.parse_bits(arg[k]) for k in ('l','u')))
    if not all(helper.finite(v) for pair in words for v in pair):
        return {'domain':'nonfinite'}
    bounds = [tuple(helper.dyadic(v) for v in pair) for pair in words]
    if any(lo > hi for lo, hi in bounds):
        return {'domain':'invalid-interval'}
    if op == 'div' and bounds[1][0] <= 0 <= bounds[1][1]:
        return {'domain':'zero-denominator'}
    a, b = bounds[0]
    if op == 'square':
        lo = Fraction(0) if a <= 0 <= b else min(a*a, b*b)
        hi = max(a*a, b*b)
    else:
        c, d = bounds[1]
        if op == 'add': lo, hi = a+c, b+d
        elif op == 'sub': lo, hi = a-d, b-c
        elif op == 'mul': lo, hi = min(a*c,a*d,b*c,b*d), max(a*c,a*d,b*c,b*d)
        else: lo, hi = min(a/c,a/d,b/c,b/d), max(a/c,a/d,b/c,b/d)
    return {'bounds':(lo, hi)}


def build_references(declarations, helper, bits, corners):
    result = []
    for item in declarations:
        if item['kind'] == 'primitive':
            result.append(primitive_reference(item, helper))
        else:
            raw = {k:copy.deepcopy(item[k]) for k in ('receiver','source','rotor')}
            query = {'id':item['id'], 'input':dict(raw, self=False)}
            target = helper.oracle_case(query, bits, corners)
            rejection = target['branch'] if target['branch'] in ('raw-nonfinite','raw-force','preparation') else None
            result.append({'input':raw, 'prepared':{'prepared':target['prepared'], 'rejection':rejection},
                           'oracle':target})
    return result


def validate_primitive(row, item, target, helper):
    key = 'word' if item['op'] in ('nextUp','nextDown') else 'args'
    fields(row, ('kind','id','op',key,'outcome'), 'primitive-record-fields')
    require(same({k:row[k] for k in item}, item), 'primitive-input-binding')
    out = row['outcome']
    require(type(out) is dict, 'primitive-outcome-shape')
    if 'domain' in target:
        require(same(out, {'kind':'fallback','reason':target['domain']}), 'primitive-domain')
        return 'fallback'
    if 'word' in target:
        require(same(out, {'kind':'word','word':target['word']}), 'primitive-adjacency')
        return 'word'
    if out.get('kind') == 'fallback':
        fields(out, ('kind','reason'), 'primitive-fallback-fields')
        require(type(out['reason']) is str and 1 <= len(out['reason']) <= 128, 'primitive-fallback-reason')
        return 'fallback'
    fields(out, ('kind','l','u'), 'primitive-interval-fields')
    require(out['kind'] == 'interval', 'primitive-outcome-kind')
    words = [helper.parse_bits(out[k]) for k in ('l','u')]
    require(all(helper.finite(w) for w in words), 'primitive-nonfinite-endpoint')
    lower, upper = [helper.dyadic(w) for w in words]
    require(lower <= upper, 'primitive-interval-order')
    exact = target['bounds']
    require(lower <= exact[0] and exact[1] <= upper, 'primitive-containment')
    return 'interval'


def validate_scalar(value, target, helper, label):
    require(type(value) is dict, label+'-result-shape')
    require(value.get('status') != 'unresolved', label+'-unresolved-unqualified')
    require(target['status'] != 'reference-undecidable', 'oracle-undecidable-unqualified')
    require(value.get('status') == target['status'], label+'-target-status')
    require(value.get('branch') == target['branch'], label+'-target-branch')
    if target['status'] == 'rejected':
        fields(value, ('status','branch'), label+'-rejected-fields')
    elif target['status'] == 'zero':
        fields(value, ('status','branch','intervals'), label+'-zero-fields')
        require(same(value['intervals'], {'K':{'l':'0','u':'0'},'coefficient':{'l':'0','u':'0'}}),
                label+'-zero-exact')
    else:
        require(target['status'] == 'positive', 'unknown-reference-status')
        fields(value, ('status','branch','intervals'), label+'-positive-fields')
        fields(value['intervals'], ('K','scaledK','beta','nu','coefficient'), label+'-interval-fields')
        parsed = {}
        for name in ('K','scaledK','beta','nu','coefficient'):
            interval = helper.candidate_interval(value['intervals'][name])
            parsed[name] = interval
            exact = target['referenceIntervals'][name]
            require(interval[0] >= 0, label+'-negative-'+name)
            require(interval[0] <= exact[0] and exact[1] <= interval[1], label+'-containment-'+name)
        require(parsed['K'][1] <= 128 and parsed['scaledK'][1] <= 128, label+'-cap-certification')
        require(parsed['nu'][0] > 0, label+'-normalizer-certification')


def validate_pair(row, item, target, helper):
    fields(row, ('kind','id','input','prepared','baseline','candidate'), 'pair-record-fields')
    require(same(row['input'], target['input']), 'raw-input-binding')
    require(same(row['prepared'], target['prepared']), 'prepared-operation-graph')
    candidate = row['candidate']
    fields(candidate, ('decision','result'), 'candidate-fields')
    decision = candidate['decision']
    require(type(decision) is dict, 'decision-fields')
    if target['prepared']['rejection'] is not None:
        require(same(decision, {'kind':'preparation'}), 'preparation-gate')
    validate_scalar(row['baseline'], target['oracle'], helper, 'baseline')
    validate_scalar(candidate['result'], target['oracle'], helper, 'candidate')
    if target['prepared']['rejection'] is None:
        if decision.get('kind') == 'zero':
            fields(decision, ('kind','branch'), 'zero-decision-fields')
            require(decision['branch'] in ZERO_BRANCHES and target['oracle']['status'] == 'zero'
                    and decision['branch'] == target['oracle']['branch'], 'fast-zero-branch-proof')
        else:
            fields(decision, ('kind','reason'), 'fallback-decision-fields')
            require(decision['kind'] == 'fallback' and type(decision['reason']) is str
                    and 1 <= len(decision['reason']) <= 128, 'fallback-decision-shape')
    require(same(candidate['result'], row['baseline']), 'baseline-candidate-result-identity')
    return decision['kind']


def validate_document(document, declarations, references, helper, table, identity):
    errors, rows, finite, decisions, fast, fallback, statuses = [], [], Counter(), Counter(), Counter(), Counter(), Counter()
    def add(code, index=None):
        errors.append({'code':code, **({} if index is None else {'row':index})})
    try:
        fields(document, ('schema','specId','sourceManifestSha256','specSha256','constants','runtime','records'),
               'document-fields')
        require(all(same(document.get(k), v) for k,v in identity.items()), 'document-identity')
        require(same(document['constants'], table), 'constant-encoding-graph')
        fields(document['runtime'], ('node','v8','platform','arch'), 'runtime-fields')
        require(all(type(v) is str and 1 <= len(v) <= 256 for v in document['runtime'].values()), 'runtime-values')
        require(type(document['records']) is list and len(document['records']) <= 128, 'record-array')
        rows = document['records']
    except CheckError as exc:
        add(str(exc))
    if len(rows) != 108: add('record-count')
    seen = set()
    for index, row in enumerate(rows):
        try:
            require(type(row) is dict and type(row.get('id')) is str, 'record-id-shape')
            require(row['id'] not in seen, 'duplicate-record-id')
            seen.add(row['id'])
            require(index < 108 and row['id'] == declarations[index]['id'], 'record-order')
            item, target = declarations[index], references[index]
            require(row.get('kind') == item['kind'], 'record-kind')
            if item['kind'] == 'primitive':
                category = validate_primitive(row, item, target, helper)
                if category == 'interval': finite[item['op']] += 1
            else:
                category = validate_pair(row, item, target, helper)
                decisions[category] += 1
                statuses[target['oracle']['status']] += 1
                if category == 'zero': fast[target['oracle']['branch']] += 1
                if category == 'fallback': fallback[row['candidate']['decision']['reason']] += 1
        except (CheckError, helper.CheckError) as exc:
            add(str(exc), index)
    for op in OPS:
        if finite[op] < 1: add('coverage-finite-'+op)
    if sum(fast.values()) < 1: add('coverage-fast-zero')
    positive_fallbacks = sum(1 for i,row in enumerate(rows) if i < 108 and
        declarations[i]['kind'] == 'pair' and type(row) is dict and
        references[i]['oracle']['status'] == 'positive' and type(row.get('candidate')) is dict and
        type(row['candidate'].get('decision')) is dict and row['candidate']['decision'].get('kind') == 'fallback')
    if positive_fallbacks < 1: add('coverage-positive-fallback')
    return {'passed':not errors, 'totalRecords':len(rows), 'errorCount':len(errors), 'errors':errors[:128],
            'finiteIntervalCounts':dict(finite), 'decisionCounts':dict(decisions),
            'fastZeroBranchCounts':dict(fast), 'fallbackReasonCounts':dict(fallback),
            'oracleStatusCounts':dict(statuses), 'positiveFallbacks':positive_fallbacks}


def expected_journal(document):
    header = {'kind':'header','schema':JOURNAL_SCHEMA,
              **{k:document[k] for k in ('specId','sourceManifestSha256','specSha256')}}
    return [header] + [{'kind':'record','row':r} for r in document['records']] + [{'kind':'complete','records':108}]


def load_journal(path):
    data = read_bytes(path, INPUT_LIMIT)
    lines = data.splitlines(keepends=True)
    require(len(lines) == 110, 'journal-event-count')
    events = []
    for line in lines:
        event = decode(line)
        require(line == compact(event), 'journal-compact-line-format')
        events.append(event)
    return events


def validate_journal(events, document):
    expected = expected_journal(document)
    require(len(events) == len(expected) == 110, 'journal-event-count')
    require(same(events[0], expected[0]), 'journal-header-identity')
    for got, want in zip(events[1:-1], expected[1:-1]):
        require(same(got, want), 'journal-row-agreement')
    require(same(events[-1], expected[-1]), 'journal-completion')


def zero_result(branch):
    return {'status':'zero','branch':branch,'intervals':{'K':{'l':'0','u':'0'},'coefficient':{'l':'0','u':'0'}}}


def run_controls(document, events, declarations, references, helper, validator):
    by_id = {item['id']:i for i,item in enumerate(declarations)}
    results = []
    for control_id, failure in zip(CONTROL_IDS, CONTROL_FAILURES):
        record = {'id':control_id, 'expectedFailure':failure, 'passed':False}
        try:
            mutated = copy.deepcopy(document)
            journal = events
            rows = mutated['records']
            witness = {}
            if control_id in CONTROL_IDS[:6]:
                row_id = {'inward-add-upper':'add-tie-positive','inward-add-lower':'add-tie-negative',
                    'lost-underflow':'mul-underflow-positive','finite-overflow':'mul-overflow',
                    'zero-divisor':'div-zero-divisor','lost-square-zero':'square-zero-crossing'}[control_id]
                index = by_id[row_id]
                row, target = rows[index], references[index]
                witness = {'row':row_id}
                if control_id == 'zero-divisor':
                    require(target.get('domain') == 'zero-denominator', 'control-witness-zero-divisor')
                    row['outcome'] = {'kind':'interval','l':'0000000000000000','u':'0000000000000000'}
                else:
                    lo, hi = target['bounds']
                    witness['exactRange'] = helper.reference_wire({'value':(lo,hi)})['value']
                    if control_id == 'inward-add-upper':
                        require(row['outcome'].get('kind') == 'interval' and hi > 1, 'control-witness-add-upper')
                        row['outcome']['u'] = '3ff0000000000000'
                    elif control_id == 'inward-add-lower':
                        require(row['outcome'].get('kind') == 'interval' and lo < -1, 'control-witness-add-lower')
                        row['outcome']['l'] = 'bff0000000000000'
                    elif control_id == 'lost-underflow':
                        require(lo > 0, 'control-witness-underflow')
                        row['outcome'] = {'kind':'interval','l':'0000000000000000','u':'0000000000000000'}
                    elif control_id == 'finite-overflow':
                        require(lo > helper.dyadic(0x7fefffffffffffff), 'control-witness-overflow')
                        row['outcome'] = {'kind':'interval','l':'7fefffffffffffff','u':'7fefffffffffffff'}
                    else:
                        require(lo == 0 and hi == 1, 'control-witness-square')
                        row['outcome'] = {'kind':'interval','l':'3ff0000000000000','u':'3ff0000000000000'}
            elif control_id in CONTROL_IDS[6:12]:
                row_id = {'guard-preempted':'guard-before-upstream', 'wrong-zero-branch':'neighbor-far',
                          'preparation-bypassed':'invalid-force-zero'}.get(control_id, 'tail-positive')
                index = by_id[row_id]
                row, target = rows[index], references[index]
                oracle = target['oracle']
                witness = {'row':row_id,'referenceStatus':oracle['status'],'referenceBranch':oracle['branch']}
                if row_id == 'tail-positive':
                    require(oracle['status'] == 'positive' and oracle['referenceIntervals']['coefficient'][0] > 0
                            and row['candidate']['decision']['kind'] == 'fallback', 'control-witness-positive-fallback')
                    witness['coefficient'] = helper.reference_wire(oracle['referenceIntervals'])['coefficient']
                if control_id == 'guard-preempted':
                    require(oracle['status'] == 'rejected' and oracle['branch'] == 'center-guard', 'control-witness-guard')
                if control_id == 'wrong-zero-branch':
                    require(oracle['status'] == 'zero' and oracle['branch'] == 'neighbor', 'control-witness-zero-branch')
                if control_id == 'preparation-bypassed':
                    require(target['prepared']['rejection'] == 'raw-force', 'control-witness-preparation')
                if control_id == 'altered-prepared-point':
                    point = row['prepared']['prepared']['receiver']['points'][row['input']['rotor']]
                    point[0] = format(int(point[0],16) ^ 1, '016x')
                elif control_id == 'lost-fallback-coefficient':
                    row['candidate']['result']['intervals']['coefficient'] = {'l':'0','u':'0'}
                else:
                    branch = 'upstream' if control_id in ('guard-preempted','wrong-zero-branch') else 'neighbor'
                    row['candidate'] = {'decision':{'kind':'zero','branch':branch}, 'result':zero_result(branch)}
            elif control_id == 'missing-row':
                witness = {'removedId':rows[-1]['id']}
                rows.pop()
            elif control_id == 'duplicate-row':
                witness = {'duplicatedId':rows[0]['id']}
                rows[1] = copy.deepcopy(rows[0])
            elif control_id == 'reordered-rows':
                witness = {'swappedIds':[rows[0]['id'],rows[1]['id']]}
                rows[0], rows[1] = rows[1], rows[0]
            else:
                journal = copy.deepcopy(events)
                witness = {'row':journal[1]['row']['id']}
                journal[1]['row']['id'] += '-changed'
            # Mathematical checks run before generic equality/journal checks.
            validation = validator(mutated)
            codes = [e['code'] for e in validation['errors']]
            if control_id == 'journal-disagreement':
                require(validation['passed'], 'control-journal-base-must-pass')
                try:
                    validate_journal(journal, mutated)
                except CheckError as exc:
                    codes.append(str(exc))
            record.update(witness=witness, detectedFailures=codes[:32], passed=failure in codes)
        except (CheckError, helper.CheckError, KeyError, TypeError, IndexError) as exc:
            record['witnessFailure'] = str(exc) if isinstance(exc,(CheckError,helper.CheckError)) else 'control-shape-error'
        results.append(record)
    return results


def write_exclusive(path, value, remaining):
    ascii_value(value)
    data = compact(value)
    require(len(data) <= remaining, 'checker-output-budget')
    require(path.parent.is_dir() and not path.parent.is_symlink(), 'checker-output-parent')
    with path.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    directory = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(directory)
    finally: os.close(directory)
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}


class Parser(argparse.ArgumentParser):
    def error(self, _message):
        raise CheckError('invalid-command-line')


def main(argv=None):
    parser = Parser(description='Independent fixed filter record checker')
    for name in ('spec','input','manifest','output','root'):
        parser.add_argument('--'+name, required=True)
    try:
        args = parser.parse_args(argv)
    except CheckError:
        print('{"passed":false,"error":"invalid-command-line"}', file=sys.stderr)
        return 2
    report = {'schema':'m31-filter-independent-check-v1','passed':False,
              'verificationPassed':False,'fullQualification':False,'controlsPassed':False,
              'sourceAndInputsUnchanged':False,'totalRecords':0,'qualifiedRecords':0,
              'faultControls':[],'errors':[], 'scope':'Finite scalar verification only; no load solve or timing claim.',
              'checkerRuntime':{'pythonVersion':'.'.join(str(v) for v in sys.version_info[:3]),
                                'implementation':sys.implementation.name}}
    output_allowed, reference_bytes = False, 0
    try:
        root = Path(args.root).resolve(strict=True)
        spec_path, input_path = Path(args.spec), Path(args.input)
        manifest_path, output = Path(args.manifest), Path(args.output)
        package = spec_path.parent.parent.resolve(strict=True)
        require(spec_path.resolve(strict=True) == package/'source/spec.json', 'spec-path')
        require(input_path.resolve(strict=True) == package/'results/filter-results.json', 'input-path')
        require(manifest_path.resolve(strict=True) == package/'source-manifest.json', 'manifest-path')
        require(output.absolute() == package/'results/independent-check.json', 'output-path')
        relative(output.parent, root)
        output_allowed = True
        source = package/'source'
        required_local = ['PROTOCOL.md','runtime-pins.json','source/spec.json','source/result-contract.json',
            'source/check.py','source/semantic-reference.py','source/binary64-interval.cjs',
            'source/zero-filter.cjs','source/run.cjs','source/guardian.py','source/supervise.py']
        required = [package/name for name in required_local]
        required += [root/'research/m31-screening-cost-2026-10-17/source'/name
                     for name in ('adapter.cjs','rational.cjs','pair-prepared.cjs','interval.cjs','spec.json')]
        indexed = verify_sources(manifest_path, root, required)
        manifest_pin = pin(manifest_path,1024*1024)
        journal_path = input_path.with_suffix(input_path.suffix+'.jsonl')
        input_pins = {p:pin(p,INPUT_LIMIT) for p in (input_path,journal_path)}
        runtime_path = Path(sys.executable).resolve(strict=True)
        runtime_pins = load(package/'runtime-pins.json',65536)
        python_pin = pin(runtime_path,256*1024*1024)
        require(same(python_pin,runtime_pins['python']), 'python-runtime-pin')
        helper = independent_module(source/'semantic-reference.py',root,indexed)
        spec, contract = load(spec_path,2*1024*1024), load(source/'result-contract.json',256*1024)
        declarations = validate_spec_contract(spec,contract)
        bits, trace = helper.constants_from_graph(spec)
        table = {name:helper.hex_bits(word) for name,word in bits.items()}
        references = build_references(declarations,helper,bits,spec['corners'])
        document = load(input_path,INPUT_LIMIT,strict=True)
        events = load_journal(journal_path)
        identity = {'schema':SCHEMA,'specId':SPEC_ID,'sourceManifestSha256':manifest_pin['sha256'],
                    'specSha256':indexed[relative(spec_path,root)]['sha256']}
        validator = lambda doc:validate_document(doc,declarations,references,helper,table,identity)
        validation = validator(document)
        report.update(validation)
        journal_ok = False
        try:
            validate_journal(events,document)
            journal_ok = True
        except CheckError as exc:
            report['errors'].append({'code':str(exc)})
        controls = run_controls(document,events,declarations,references,helper,validator)
        report['faultControls'] = controls
        report['controlsPassed'] = len(controls) == 16 and all(c['passed'] for c in controls)
        report['journalPassed'] = journal_ok
        evidence = []
        for item,target in zip(declarations,references):
            record = {'id':item['id'],'kind':item['kind']}
            if item['kind'] == 'primitive':
                if 'bounds' in target: record['exactRange'] = helper.reference_wire({'value':target['bounds']})['value']
                else: record.update(target)
            else:
                oracle = target['oracle']
                record.update(input=target['input'],prepared=target['prepared'],
                              status=oracle['status'],branch=oracle['branch'])
                if 'referenceIntervals' in oracle:
                    record['referenceIntervals'] = helper.reference_wire(oracle['referenceIntervals'])
            evidence.append(record)
        # Check source, result, journal, and runtime before writing either evidence file.
        require(same(verify_sources(manifest_path,root,required),indexed) and
                same(pin(manifest_path,1024*1024),manifest_pin), 'source-changed-during-check')
        require(all(same(pin(path,INPUT_LIMIT),expected) for path,expected in input_pins.items()),
                'input-changed-during-check')
        require(same(pin(runtime_path,256*1024*1024),python_pin), 'runtime-changed-during-check')
        report['sourceAndInputsUnchanged'] = True
        reference_payload = {'schema':'m31-filter-reference-v1', **identity,
            'helperSha256':HELPER_SHA,'constantGraphTrace':trace,'constants':table,'records':evidence,
            'sourceManifest':manifest_pin,'inputPins':{relative(p,root):v for p,v in input_pins.items()}}
        # reference schema is distinct from result schema.
        reference_payload['schema'] = 'm31-filter-reference-v1'
        ref_pin = write_exclusive(package/'results/reference.json', reference_payload, OUTPUT_LIMIT-2*1024*1024)
        reference_bytes = ref_pin['bytes']
        report['referencePin'] = ref_pin
        report['verificationPassed'] = validation['passed'] and journal_ok
        report['fullQualification'] = report['verificationPassed'] and report['controlsPassed']
        report['passed'] = report['fullQualification'] and report['sourceAndInputsUnchanged']
        report['qualifiedRecords'] = 108 if report['passed'] else 0
        report['errorCount'] = len(report['errors'])
    except Exception as exc:
        report['passed'] = report['verificationPassed'] = report['fullQualification'] = False
        public = str(exc) if isinstance(exc,CheckError) or exc.__class__.__name__ == 'CheckError' else 'checker-internal-or-input-error'
        report['errors'].append({'code':public})
        report['errorCount'] = len(report['errors'])
    if not output_allowed:
        print('{"passed":false,"error":"unsafe-or-invalid-output-path"}',file=sys.stderr)
        return 2
    try:
        write_exclusive(Path(args.output),report,OUTPUT_LIMIT-reference_bytes)
    except Exception:
        print('{"passed":false,"error":"exclusive-report-write-failed"}',file=sys.stderr)
        return 2
    print(json.dumps({'passed':report['passed'],'totalRecords':report['totalRecords'],
                      'controlsPassed':report['controlsPassed']},separators=(',',':')))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
