#!/usr/bin/env python3
"""Administrative audit of saved artifacts only; no scientific imports or execution.

Reads saved JSON/JSONL/logs, hashes files/local Git blobs, and reconciles serialized
identities, memberships and integer work counts. Does not decode geometry, evaluate
predicates, recompute coefficients/roots/loads, launch scientific tools, or use network.
"""
from collections import Counter
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]
READS = {}
RULES = ['neighbor', 'upstream', 'down-cut', 'near-outside', 'radial']
WORK = ['preparationCalls', 'globalProofs', 'treeNodes', 'nodeVisits', 'nodeRuleTests',
        'zeroNodes', 'zeroPairs', 'leafVisits', 'scalarPairs', 'scalarZeroPairs',
        'positiveTerms', 'rejectedPairs', 'unresolvedPairs']


def need(condition, label):
    if not condition:
        raise AssertionError(label)


def same(a, b):
    return type(a) is type(b) and (set(a) == set(b) and all(same(a[k], b[k]) for k in a)
        if isinstance(a, dict) else len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
        if isinstance(a, list) else a == b)


def read(path, purpose='saved-evidence content'):
    path = path.resolve()
    name = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    purposes = sorted(set(READS.get(name, {}).get('purposes', []) + [purpose]))
    READS[name] = {'path': name, 'bytes': len(data),
                   'sha256': hashlib.sha256(data).hexdigest(), 'purposes': purposes}
    return data


def unique(items):
    result = {}
    for key, value in items:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def decode(data):
    return json.loads(data, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def load(relative):
    return decode(read(PACKAGE / relative))


def stamp(text):
    return datetime.fromisoformat(text.replace('Z', '+00:00'))


def pin(relative, expected_size, expected_sha, purpose='metadata-only file pin'):
    data = read(ROOT / relative, purpose)
    need(len(data) == expected_size and hashlib.sha256(data).hexdigest() == expected_sha,
         'file pin mismatch: ' + relative)
    return data


def git_blob(commit, path):
    return subprocess.run(['git', 'cat-file', 'blob', commit + ':' + path], cwd=ROOT,
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def method_structure(record, method, checked):
    ids = [d['id'] for d in record['input']['drones']]
    n = len(ids)
    need(len(set(ids)) == n, 'duplicate input identity')
    id_index = {identifier: i for i, identifier in enumerate(ids)}
    assembly, result = method['assembly'], method['result']
    tally = {k: 0 for k in WORK}
    tally['preparationCalls'] = n
    rule_counts = {k: 0 for k in RULES}
    mode = assembly['mode']
    nonzero = []
    if mode == 'global-preparation':
        need(not assembly['queries'] and assembly['tree'] is None and assembly['globalGuard'] is None,
             'global invalidity assembly')
        invalid = next(p for p in method['prepared'] if p['rejection'] is not None)
        need(result == {'status': 'rejected', 'branch': invalid['rejection'],
                        'witness': {'id': invalid['id']}, 'toleranceAchieved': None},
             'first saved preparation refusal')
    else:
        need(mode in ('complete', 'hierarchy', 'fallback'), 'mode')
        if method['name'] == 'complete':
            need(mode == 'complete' and assembly['globalGuard'] is None, 'complete guard policy')
        else:
            tally['globalProofs'] = 1
            guard = assembly['globalGuard']
            need(type(guard['passed']) is bool and all(type(v) is bool for v in guard['checks'].values()),
                 'guard boolean types')
            need(guard['passed'] == all(guard['checks'].values()), 'saved guard conjunction')
            need(mode == ('hierarchy' if guard['passed'] else 'fallback'), 'fallback mode')
        tree = assembly['tree']
        nodes, parents = None, {}
        if mode == 'hierarchy':
            permutation, nodes = tree['permutation'], tree['nodes']
            need(sorted(permutation) == sorted(ids), 'tree membership universe')
            tally['treeNodes'] = len(nodes)
            seen = []

            def visit(node_id, start, end):
                need(node_id not in seen and 0 <= node_id < len(nodes), 'tree cycle/id')
                seen.append(node_id)
                node = nodes[node_id]
                need((node['id'], node['start'], node['end']) == (node_id, start, end), 'tree ranges')
                if node['left'] is None:
                    need(node['right'] is None and 1 <= end-start <= 8, 'leaf size/children')
                else:
                    need(end-start > 8, 'internal leaf capacity')
                    middle = start + (end-start)//2
                    parents[node['left']] = node_id
                    parents[node['right']] = node_id
                    visit(node['left'], start, middle)
                    visit(node['right'], middle, end)
            visit(0, 0, n)
            need(seen == list(range(len(nodes))), 'tree complete preorder')
        else:
            need(tree is None, 'unexpected tree')
        need([(q['i'], q['r']) for q in assembly['queries']] ==
             [(i, r) for i in range(n) for r in range(4)], 'query completeness/order')
        for query in assembly['queries']:
            i, r, terminals = query['i'], query['r'], query['terminals']
            covered, stopped, visited = [], set(), set()
            if mode != 'hierarchy':
                need(len(terminals) == 1 and terminals[0]['kind'] == 'scan', 'complete/fallback scan')
            for terminal in terminals:
                kind = terminal['kind']
                if kind == 'scan':
                    members = [j for j in range(n) if i != j]
                else:
                    node_id = terminal['node']
                    need(mode == 'hierarchy' and node_id not in stopped, 'terminal node uniqueness')
                    stopped.add(node_id)
                    node = nodes[node_id]
                    members = [id_index[v] for v in tree['permutation'][node['start']:node['end']]
                               if v != ids[i]]
                    ancestor = node_id
                    while True:
                        visited.add(ancestor)
                        if ancestor == 0:
                            break
                        ancestor = parents[ancestor]
                covered.extend(members)
                if kind == 'zero':
                    need(terminal['rule'] in RULES and terminal['count'] == len(members), 'zero membership/count')
                    tally['zeroNodes'] += 1
                    tally['zeroPairs'] += len(members)
                    tally['nodeRuleTests'] += RULES.index(terminal['rule']) + 1
                    rule_counts[terminal['rule']] += 1
                    continue
                need(kind in ('scan', 'leaf'), 'terminal kind')
                if kind == 'leaf':
                    need(node['left'] is None, 'scalar terminal is leaf')
                    tally['leafVisits'] += 1
                entries = terminal['entries']
                js = [e['j'] for e in entries]
                need(js == sorted(set(js)) and set(js) <= set(members), 'entry membership/order')
                need(terminal['zeroCount'] == len(members)-len(entries), 'implicit zero count')
                tally['scalarPairs'] += len(members)
                tally['scalarZeroPairs'] += terminal['zeroCount']
                for entry in entries:
                    status = entry['result']['status']
                    need(status in ('positive', 'rejected', 'unresolved'), 'saved nonzero status')
                    tally[{'positive': 'positiveTerms', 'rejected': 'rejectedPairs',
                           'unresolved': 'unresolvedPairs'}[status]] += 1
                    nonzero.append({'i': i, 'r': r, 'j': entry['j'], 'result': entry['result']})
            need(sorted(covered) == [j for j in range(n) if i != j], 'complete disjoint nonself partition')
            if mode == 'hierarchy':
                canonical = []
                def terminals_in_order(node_id):
                    if node_id in stopped:
                        canonical.append(node_id)
                    else:
                        need(nodes[node_id]['left'] is not None, 'missing leaf terminal')
                        terminals_in_order(nodes[node_id]['left'])
                        terminals_in_order(nodes[node_id]['right'])
                terminals_in_order(0)
                need(canonical == [t['node'] for t in terminals], 'left-first stopped-node traversal')
                tally['nodeVisits'] += len(visited)
                tally['nodeRuleTests'] += 5*(len(visited)-sum(t['kind'] == 'zero' for t in terminals))
        need(tally['scalarPairs']+tally['zeroPairs'] == 4*n*(n-1), 'logical pair coverage')
    need(same(tally, assembly['work']) and same(tally, checked['work']), 'saved/checker work reconciliation')
    need(same(rule_counts, checked['zeroRuleCounts']), 'zero rule counters')
    need(checked['accountedPairs'] == tally['scalarPairs']+tally['zeroPairs'], 'checker accounted count')
    nonzero.sort(key=lambda p: (p['i'], p['r'], p['j']))
    rejected = next((p for p in nonzero if p['result']['status'] == 'rejected'), None)
    if rejected is not None:
        need(result['status'] == 'rejected' and result['branch'] == 'pair-'+rejected['result']['branch']
             and result['witness'] == {'i': ids[rejected['i']], 'r': rejected['r'], 'j': ids[rejected['j']]},
             'canonical first saved pair refusal')
    return tally, nonzero, rule_counts


def audit():
    publication = load('source-publication.json')
    manifest = load('source-manifest.json')
    spec, contract = load('source/spec.json'), load('source/result-contract.json')
    runtime = load('runtime-pins.json')
    kernel, checker = load('results/screening-results.json'), load('results/independent-check.json')
    commit = publication['commit']
    need(re.fullmatch('[0-9a-f]{40}', commit) is not None, 'commit shape')
    manifest_bytes = pin(publication['manifestPath'], publication['manifestBytes'], publication['manifestSha256'])
    need(git_blob(commit, publication['manifestPath']) == manifest_bytes, 'committed manifest equality')
    git_hash = hashlib.sha1(b'blob '+str(len(manifest_bytes)).encode()+b'\0'+manifest_bytes).hexdigest()
    need(git_hash == publication['manifestGitBlob'], 'manifest Git object identity')
    need(publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True,
         'saved publication verification')
    need('/'+commit+'/' in publication['remoteUrl'], 'exact-commit publication URL')
    seen = set()
    for item in manifest['files']:
        need(item['path'] not in seen, 'duplicate manifest entry')
        seen.add(item['path'])
        content = pin(item['path'], item['bytes'], item['sha256'])
        need(git_blob(commit, item['path']) == content, 'committed source pin: '+item['path'])
    need(len(seen) == publication['verifiedFilePins'] == 73, 'manifest pin count')
    need(same(checker['verifiedSources'], manifest['files']), 'checker source pin inventory')
    source_pins = {name: next(i['sha256'] for i in manifest['files']
                  if i['path'] == (PACKAGE/'source'/name).relative_to(ROOT).as_posix())
                  for name in contract['sourceFiles']}
    need(same(kernel['sourceSha256'], source_pins), 'kernel source hashes')
    need(same(kernel['constants'], checker['expectedConstantEncodings']), 'saved constant identity')
    need(checker['sourceManifest']['sha256'] == publication['manifestSha256'], 'checker manifest identity')
    need(checker['input']['sha256'] == hashlib.sha256(read(PACKAGE/'results/screening-results.json')).hexdigest(),
         'checker kernel-input identity')
    journal_data = read(PACKAGE/'results/screening-results.json.jsonl')
    journal = [decode(line) for line in journal_data.splitlines()]
    need(len(journal) == 20 and journal[0] == {'kind': 'header', 'schema': contract['journalSchema'], 'specId': spec['id']}
         and journal[-1] == {'kind': 'complete', 'records': 18}, 'complete journal framing')
    need(all(same(j, {'kind': 'record', 'row': r}) for j, r in zip(journal[1:-1], kernel['records'])),
         'journal exact record identity')
    need(checker['journal']['passed'] is True and checker['journal']['rows'] == 18
         and checker['journal']['bytes'] == len(journal_data)
         and checker['journal']['sha256'] == hashlib.sha256(journal_data).hexdigest(), 'checker journal pin')
    stages, attempts = {}, {}
    for stage in ('kernel', 'checker'):
        report, attempt = load('results/'+stage+'-supervision.json'), load('results/'+stage+'-attempt.json')
        stages[stage], attempts[stage] = report, attempt
        need(report['stage'] == attempt['stage'] == stage and report['sourceCommit'] == attempt['sourceCommit'] == commit,
             'stage source identity')
        need(report['sourceManifestSha256'] == attempt['sourceManifestSha256'] == publication['manifestSha256'],
             'stage manifest identity')
        need(stamp(publication['verifiedUtc']) < stamp(attempt['startedUtc']), 'publication precedes allocation')
        need(all(report[k] is True for k in ('success', 'closed', 'scientificChildAbsentBeforeRelease',
             'childGroupAbsent', 'sourceAndRuntimeRechecked')), 'saved stage closure')
        need(report['exitCode'] == report['guardianExitCode'] == 0 and report['terminationReason'] is None,
             'saved successful exits')
        need(report['wallSeconds'] < report['wallLimitSeconds'] and
             report['peakSampledGroupRssBytes'] < report['sampledRssLimitBytes'], 'saved stage resource limits')
        need(same(report['runtimePins'], runtime), 'runtime pin consistency')
        for name in ('output', 'journal'):
            if name in report:
                item = report[name]
                pin(item['path'], item['bytes'], item['sha256'])
        for item in report['logs']:
            data = pin(item['path'], item['publishedBytes'], item['publishedSha256'])
            need(item['rawBytes'] == len(data) and item['rawSha256'] == hashlib.sha256(data).hexdigest(),
                 'published/raw log equality')
        events = [decode(line) for line in read(PACKAGE/('results/'+stage+'-guardian.jsonl')).splitlines()]
        need(len(events) == 2 and events[0]['event'] == 'child-start' and events[1]['event'] == 'child-exit'
             and events[0]['pid'] == events[1]['pid'] and events[0]['guardian'] == report['processGroup']
             and events[1]['exitCode'] == 0, 'saved guardian lifecycle')
    need(stamp(attempts['kernel']['startedUtc'])+timedelta(seconds=stages['kernel']['wallSeconds'])
         < stamp(attempts['checker']['startedUtc']), 'sequential allocations')
    need(len(list((PACKAGE/'results').glob('*-attempt.json'))) == 2, 'sole saved stage attempts')
    need(all(checker[k] is True for k in ('verificationPassed', 'fullQualification', 'tolerancePassed',
         'passed', 'baselineVerificationPassed', 'sourcesUnchangedAfter')) and checker['errors'] == []
         and checker['baselineErrorCount'] == 0, 'saved checker success')
    rows, scenes = kernel['records'], checker['scenes']
    need([r['id'] for r in rows] == [s['id'] for s in spec['scenes']] == [s['id'] for s in scenes],
         'complete scene identities/order')
    totals = {name: Counter() for name in ('complete', 'hierarchy')}
    modes, rules, outcomes, scene_summaries = Counter(), Counter(), Counter(), []
    planned = skipped = 0
    for row, checked in zip(rows, scenes):
        n = len(row['input']['drones'])
        planned += 4*n*(n-1)
        need(checked['verified'] is True and checked['methodEquality'] is True and checked['expectedClassAgrees'] is True,
             'saved scene verification')
        need([m['name'] for m in row['methods']] == ['complete', 'hierarchy'], 'method order')
        extracted = []
        for method, cm in zip(row['methods'], checked['methods']):
            need(cm['verified'] is True, 'saved method verification')
            tally, nonzero, rule_count = method_structure(row, method, cm)
            totals[method['name']].update(tally)
            extracted.append(nonzero)
            if method['name'] == 'hierarchy':
                modes[method['assembly']['mode']] += 1
                rules.update(rule_count)
        for field in ('prepared', 'result', 'solve', 'certificate'):
            need(same(row['methods'][0][field], row['methods'][1][field]), 'common payload equality:'+field)
        need(same(extracted[0], extracted[1]), 'all saved nonzero singleton equality')
        result = row['methods'][0]['result']
        outcomes[result['status']] += 1
        if result['status'] == 'certified':
            need(result['toleranceAchieved'] is True and checked['referenceStatus'] == 'admitted', 'admitted tolerance')
        else:
            need(result['status'] == checked['referenceStatus'] == 'rejected'
                 and result['branch'] == checked['referenceBranch']
                 and same(result['witness'], checked['referenceWitness']) and result['toleranceAchieved'] is None,
                 'saved independently confirmed refusal')
        if row['methods'][0]['assembly']['mode'] == 'global-preparation':
            skipped += 4*n*(n-1)
        scene_summaries.append({'id': row['id'], 'drones': n, 'status': result['status'],
            'branch': result['branch'], 'witness': result['witness'], 'hierarchyMode': row['methods'][1]['assembly']['mode'],
            'completeScalarPairs': row['methods'][0]['assembly']['work']['scalarPairs'],
            'hierarchyScalarPairs': row['methods'][1]['assembly']['work']['scalarPairs'],
            'prunedNonselfPairs': row['methods'][1]['assembly']['work']['zeroPairs']})
    need(len(rows) == checker['totalRecords'] == checker['qualifiedRecords'] == checker['methodEqualityRecords'] == 18,
         'qualified counts')
    need(outcomes == {'certified': 12, 'rejected': 6} and checker['admittedRecords'] == checker['tolerancePassedRecords'] == 12
         and checker['toleranceFailedRecords'] == checker['unqualifiedRecords'] == 0, 'outcome counts')
    need(planned == 46744 and sum(len(r['input']['drones']) for r in rows) == 312, 'structural scene budget')
    controls = checker['faultControls']
    need([c['name'] for c in controls] == contract['negativeControls'], 'all declared controls')
    for control in controls:
        need(control['executed'] is True and control['rejected'] is True and control['intendedCoreFailure'] is True
             and control['errorCount'] > 0 and control['witness'], 'control result/witness')
        need(any(any(error.startswith(family) for family in control['requiredFailureFamilies'])
                 for error in control['errors']), 'control targeted failure evidence')
    result_files = [p for p in (PACKAGE/'results').iterdir() if p.is_file()]
    total_bytes = sum(p.stat().st_size for p in result_files)
    need(total_bytes < 384*1024*1024, 'current saved results aggregate budget')
    for stage in ('kernel', 'checker'):
        need((PACKAGE/('results/'+stage+'-supervision.json')).stat().st_size <= 65536, 'supervision report budget')
    return {'schema': 'm31-screening-saved-administrative-audit-v1', 'passed': True,
        'scope': 'Saved artifacts, structural partitions, integer counts and local file/Git identities only; no scientific reevaluation or network.',
        'sourceCommit': commit, 'manifestSha256': publication['manifestSha256'], 'localAndCommittedSourcePins': len(seen),
        'remoteEvidence': 'Recorded exact-commit TLS verification receipt cross-linked; no new remote fetch.',
        'processClosureEvidence': 'Both saved guardians record matching child start/exit0; supervision records child/group absence and closure. No live process probing.',
        'completedJournalRows': 18, 'qualifiedScenes': 18, 'admittedTolerancePassedScenes': 12,
        'independentlyConfirmedRefusals': 6, 'commonPayloadEqualScenes': 18, 'targetedControls': len(controls),
        'logicalPairsPerMethod': planned, 'globallyRejectedPlannedPairsPerMethod': skipped,
        'accountedPairsPerMethod': planned-skipped, 'workTotals': {k: dict(v) for k, v in totals.items()},
        'hierarchyModes': dict(modes), 'zeroProofTerminalCounts': dict(rules), 'scenes': scene_summaries,
        'savedResultFiles': len(result_files), 'savedResultBytes': total_bytes,
        'stages': {k: {name: v[name] for name in ('wallSeconds', 'peakSampledGroupRssBytes', 'samples', 'maxSampleGapSeconds',
                     'success', 'closed', 'childGroupAbsent')} for k, v in stages.items()},
        'limits': ['Saved proof validity relies on the completed independent checker; this script does not recompute geometry or numerical proofs.',
                   'Saved attempt/closure evidence supports the recorded sole allocations; no claim about unrecorded activity.',
                   'Counters and supervision duration do not establish speedup, total-cost savings, physical validity or 5000-drone completion.']}


if __name__ == '__main__':
    try:
        answer = audit()
    except Exception as error:
        answer = {'schema': 'm31-screening-saved-administrative-audit-v1', 'passed': False,
                  'error': type(error).__name__+': '+str(error)}
    answer['readInventory'] = sorted(READS.values(), key=lambda x: x['path'])
    answer['auditScriptSha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = PACKAGE/'review/SAVED-EVIDENCE-AUDIT.json'
    with destination.open('x') as handle:
        json.dump(answer, handle, indent=2)
        handle.write('\n')
    print(json.dumps({k: answer[k] for k in ('passed', 'error', 'qualifiedScenes', 'accountedPairsPerMethod') if k in answer}))
    raise SystemExit(0 if answer['passed'] else 1)
