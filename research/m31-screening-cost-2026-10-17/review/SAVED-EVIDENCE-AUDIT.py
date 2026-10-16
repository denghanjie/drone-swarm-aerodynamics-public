"""Generic saved-file audit only: JSON, hashes, counts, timing arithmetic, Git blobs.

Never imports or executes candidate, oracle, checker, or scientific helpers.
Writes only a new review artifact, outside the frozen source/result corpus.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
RESULTS = BASE / 'results'
METHODS = ('complete', 'hierarchy')
ORDERS = ('AB', 'AB', 'BA', 'BA', 'AB')
checks = 0


def need(condition, code):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(code)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def equal(a, b, code):
    need(canon(a) == canon(b), code)


def duplicate_free(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate-json-key')
        out[key] = value
    return out


def parse_int(text):
    need(text != '-0', 'negative-zero-token')
    return int(text)


def reject_number(_text):
    raise AssertionError('noninteger-json-number')


def domain(value):
    if value is None or type(value) is bool:
        return
    if type(value) is int:
        need(abs(value) <= 9007199254740991, 'unsafe-json-integer')
    elif type(value) is str:
        need(all(32 <= ord(c) <= 126 for c in value), 'nonprintable-json-string')
    elif type(value) is list:
        for item in value:
            domain(item)
    elif type(value) is dict:
        for key, item in value.items():
            domain(key)
            domain(item)
    else:
        raise AssertionError('unsupported-json-type')


def decode(data):
    value = json.loads(data, object_pairs_hook=duplicate_free,
                       parse_int=parse_int, parse_float=reject_number,
                       parse_constant=reject_number)
    domain(value)
    return value


def strict_load(path, canonical=False):
    need(path.is_file() and not path.is_symlink(), 'missing-or-symlink-input')
    raw = path.read_bytes()
    value = decode(raw)
    if canonical:
        ending = b'' if canonical == 'bare' else b'\n'
        need(raw == canon(value) + ending, 'noncanonical-file-bytes')
    return value


def ordinary(path):
    return json.loads(path.read_bytes())


def pin(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': sha(raw)}


def check_pin(path, expected, label):
    need(path.is_file() and not path.is_symlink(), label + ':file')
    actual = pin(path)
    need(actual['bytes'] == expected['bytes'] and
         actual['sha256'] == expected['sha256'], label + ':pin')
    return actual


def integer(text):
    need(type(text) is str and re.fullmatch(r'0|[1-9][0-9]{0,19}', text) is not None,
         'noncanonical-time-string')
    return int(text)


def interval(value, positive=False):
    a, b, t = (integer(value[k]) for k in ('startNs', 'endNs', 'totalNs'))
    need(b >= a and t == b-a and (t > 0 or not positive), 'interval-arithmetic')
    return a, b, t


def rational(q):
    need(set(q) == {'n', 'd'}, 'fraction-fields')
    need(all(type(q[k]) is str and re.fullmatch(r'0|-?[1-9][0-9]*', q[k])
             for k in ('n', 'd')), 'fraction-canonical-integers')
    n, d = int(q['n']), int(q['d'])
    need(d > 0, 'fraction-denominator')
    x = Fraction(n, d)
    need(x.numerator == n and x.denominator == d, 'fraction-reduced')
    return x


def wire(x):
    x = Fraction(x)
    return {'n': str(x.numerator), 'd': str(x.denominator)}


def median(values):
    values = sorted(values)
    need(len(values) == 4, 'median-four-values')
    return (values[1] + values[2]) / 2


def summary(scene_id, trials):
    pairs = []
    for repetition in range(1, 5):
        pair = {t['method']: t for t in trials
                if t['phase'] == 'measured' and t['repetition'] == repetition}
        a, b = (integer(pair[m]['timing']['totalNs']) for m in METHODS)
        pairs.append({'repetition': repetition, 'pairOrder': ORDERS[repetition],
                      'completeNs': str(a), 'hierarchyNs': str(b),
                      'ratio': wire(Fraction(a, b))})
    a = median([Fraction(p['completeNs']) for p in pairs])
    b = median([Fraction(p['hierarchyNs']) for p in pairs])
    return {'sceneId': scene_id, 'pairs': pairs, 'completeMedianNs': wire(a),
            'hierarchyMedianNs': wire(b),
            'medianPairedRatio': wire(median([rational(p['ratio']) for p in pairs])),
            'ratioOfMedians': wire(a/b)}


def common_projection(method, raw):
    entries = []
    for query in method['assembly']['queries']:
        for terminal in query['terminals']:
            for entry in terminal.get('entries', []):
                if entry['result']['status'] == 'positive':
                    entries.append((query['i'], query['r'], entry['j'],
                                    entry['result']['coefficient']))
    entries.sort(key=lambda x: x[:3])
    projected = [{'i': raw['drones'][i]['id'], 'r': r,
                  'j': raw['drones'][j]['id'], 'coefficient': q}
                 for i, r, j, q in entries]
    return {**{key: method[key] for key in ('prepared', 'result', 'solve', 'certificate')},
            'canonicalPositiveEntries': projected}


def main(private):
    publication = ordinary(BASE/'source-publication.json')
    manifest = ordinary(BASE/'source-manifest.json')
    manifest_sha = sha((BASE/'source-manifest.json').read_bytes())
    need(publication['remoteBytesEqualLocal'] is True and
         publication['committedBytesEqualLocal'] is True, 'publication-receipt')
    need(publication['manifestSha256'] == manifest_sha, 'manifest-receipt-sha')
    commit = publication['commit']
    manifest_blob = subprocess.run(['git', 'cat-file', 'blob',
        commit+':'+publication['manifestPath']], cwd=ROOT, check=True,
        capture_output=True).stdout
    need(manifest_blob == (BASE/'source-manifest.json').read_bytes(), 'git-manifest-bytes')
    seen = set()
    for item in manifest['files']:
        need(item['path'] not in seen, 'manifest-duplicate-path')
        seen.add(item['path'])
        check_pin(ROOT/item['path'], item, 'local-source')
        raw = subprocess.run(['git', 'cat-file', 'blob', commit+':'+item['path']],
            cwd=ROOT, check=True, capture_output=True).stdout
        need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'git-source-pin')
    spec = strict_load(BASE/'source/spec.json')
    contract = strict_load(BASE/'source/result-contract.json')
    index = strict_load(RESULTS/'timing-index.json', True)
    checker = strict_load(RESULTS/'independent-check.json', 'bare')
    equal(checker['verifiedSources'], manifest['files'], 'checker-source-pin-list')
    check_pin(ROOT/checker['input']['path'], checker['input'], 'checker-input-pin')
    check_pin(ROOT/checker['sourceManifest']['path'], checker['sourceManifest'], 'checker-manifest-pin')
    check_pin(RESULTS/'timing-index.json.jsonl', checker['journal'], 'checker-journal-pin')
    need(checker['journal']['passed'] is True and checker['journal']['events'] == 80,
         'checker-journal-count')
    supervisors = {stage: ordinary(RESULTS/(stage+'-supervision.json'))
                   for stage in ('kernel', 'checker')}
    need(index['specSha256'] == sha((BASE/'source/spec.json').read_bytes()) and
         index['sourceManifestSha256'] == manifest_sha, 'index-context')
    need(index['specId'] == spec['id'] and index['clock'] == 'process.hrtime.bigint',
         'index-spec-clock')
    equal(index['recordedHarnessScope'], contract['trialProtocol']['recordedHarnessScope'],
          'disclosed-harness-scope')
    equal(index['sourceSha256'], {n: sha((BASE/'source'/n).read_bytes())
          for n in contract['sourceFiles']}, 'candidate-source-pins')
    need(len(index['trials']) == 60 and len(index['scenes']) == 6, 'allocation-counts')
    for stage, report in supervisors.items():
        need(all(report[k] is True for k in ('success', 'closed', 'childGroupAbsent',
             'scientificChildAbsentBeforeRelease', 'sourceAndRuntimeRechecked')), 'supervision-success')
        need(report['sourceCommit'] == commit and report['sourceManifestSha256'] == manifest_sha,
             'supervision-source-context')
        need(report['exitCode'] == report['guardianExitCode'] == 0 and
             report['terminationReason'] is None, 'supervision-exit')
        need(report['wallSeconds'] <= 1800 and report['peakSampledGroupRssBytes'] <= 1073741824,
             'supervision-budget')
        need(not report['anomalyEvidence'] and
             not report['outputAccountingBeforeReport']['violations'], 'supervision-no-anomaly')
        for item in report['scientificEvidence'] + report.get('checkerEvidence', []):
            check_pin(ROOT/item['path'], item, 'saved-supervision-evidence')
        for log in report['logs']:
            actual = pin(ROOT/log['path'])
            need(actual['bytes'] == log['publishedBytes'] and
                 actual['sha256'] == log['publishedSha256'], 'public-log-pin')
        for item in report['privateRawLogs']:
            check_pin(private/item['name'], item, 'private-raw-log-pin')
        attempt = ordinary(RESULTS/(stage+'-attempt.json'))
        need(attempt['stage'] == stage and attempt['sourceCommit'] == commit and
             attempt['sourceManifestSha256'] == manifest_sha, 'attempt-context')
        lifecycle = [ordinary_line for ordinary_line in
                     map(json.loads, (RESULTS/(stage+'-guardian.jsonl')).read_text().splitlines())]
        need([v['event'] for v in lifecycle] == ['child-start', 'child-exit'] and
             lifecycle[1]['exitCode'] == 0, 'guardian-saved-lifecycle')
    need(supervisors['kernel']['privateLogDirectorySha256'] ==
         supervisors['checker']['privateLogDirectorySha256'] ==
         sha(str(private.resolve()).encode()), 'private-directory-identity')
    previous_end = 0
    audits = []
    work_totals = {m: {'scalarPairs': 0, 'zeroPairs': 0, 'positiveTerms': 0} for m in METHODS}
    all_ratios = []
    for si, (scene, descriptor) in enumerate(zip(spec['scenes'], index['scenes'])):
        sid = scene['id']
        need(descriptor['sceneIndex'] == si and descriptor['id'] == sid and
             descriptor['path'] == 'results/scenes/'+sid+'.json', 'scene-order-path')
        check_pin(BASE/descriptor['path'], descriptor, 'scene-shard')
        shard = strict_load(BASE/descriptor['path'], True)
        need(shard['id'] == sid and shard['specId'] == spec['id'] and
             shard['specSha256'] == index['specSha256'] and
             shard['sourceManifestSha256'] == manifest_sha, 'shard-context')
        raw = shard['input']
        raw_sha = sha(canon({'domain': 'm31-screening-cost/raw-input/v1',
                            'sceneId': sid, 'input': raw}))
        need(raw_sha == descriptor['rawInputSha256'] == shard['rawInputSha256'], 'raw-digest')
        need([d['id'] for d in raw['drones']] == [d['id'] for d in scene['drones']], 'raw-id-order')
        need(all(len(d['state']) == 17 and all(re.fullmatch('[0-9a-f]{16}', w)
                 for w in d['state']) for d in raw['drones']), 'raw-word-shape')
        context = {'specSha256': index['specSha256'], 'sourceManifestSha256': manifest_sha,
                   'sceneId': sid, 'rawInputSha256': raw_sha}
        digests, common_digests, counters = {}, {}, {}
        for mi, method in enumerate(shard['methods']):
            name = METHODS[mi]
            need(method['name'] == name, 'method-order')
            digests[name] = sha(canon({'domain': 'm31-screening-cost/method/v1',
                **context, 'method': name, 'scientific': method}))
            common_digests[name] = sha(canon({'domain': 'm31-screening-cost/common/v1',
                **context, 'scientific': common_projection(method, raw)}))
            counters[name] = method['assembly']['work']
            for key in work_totals[name]:
                work_totals[name][key] += counters[name][key]
            need(counters[name]['scalarPairs'] + counters[name]['zeroPairs'] ==
                 4*len(raw['drones'])*(len(raw['drones'])-1), 'saved-work-pair-partition')
            need(method['result']['status'] == 'certified' and
                 method['result']['toleranceAchieved'] is True, 'saved-certified-status')
            for upper in method['certificate']['maxErrors'].values():
                need(int(upper)*100000000 <= 2**96, 'saved-tolerance-arithmetic')
        need(common_digests['complete'] == common_digests['hierarchy'], 'common-digest-equality')
        for mi, representative in enumerate(descriptor['representatives']):
            name = METHODS[mi]
            equal(representative, {'method': name, 'trialSequence': si*10+2+mi,
                  'scientificDigest': digests[name], 'commonDigest': common_digests[name]},
                  'first-measured-representative')
        a, b, _ = interval(descriptor['inputConversionTiming'])
        need(a >= previous_end, 'conversion-chronology')
        previous_end = b
        trials = index['trials'][si*10:si*10+10]
        stage_totals = {m: {k: 0 for k in contract['trialProtocol']['stageFields']} for m in METHODS}
        for local, trial in enumerate(trials):
            repetition, position = divmod(local, 2)
            order = ORDERS[repetition]
            name = 'complete' if order[position] == 'A' else 'hierarchy'
            expected = {'sequence': si*10+local, 'sceneIndex': si, 'sceneId': sid,
                'phase': 'warmup' if repetition == 0 else 'measured',
                'repetition': repetition, 'pairOrder': order, 'pairPosition': position, 'method': name}
            equal({k: trial[k] for k in expected}, expected, 'trial-schedule')
            need(trial['scientificDigest'] == digests[name] and
                 trial['commonDigest'] == common_digests[name], 'trial-digest-binding')
            equal(trial['work'], counters[name], 'trial-counter-binding')
            t = trial['timing']; start, end, total = interval(t, True)
            need(start >= previous_end, 'serial-method-chronology')
            offsets = [integer(t['offsetsNs'][k]) for k in ('prepared','spatial','assembled','completed')]
            need(offsets == sorted(offsets) and offsets[-1] == total, 'phase-offset-order')
            stages = [offsets[0]] + [offsets[i]-offsets[i-1] for i in range(1, 4)]
            equal(t['stagesNs'], {k: str(v) for k, v in zip(contract['trialProtocol']['stageFields'], stages)},
                  'exact-stage-partition')
            need(sum(stages) == total, 'stage-sum')
            hs, he, ht = interval(trial['harnessTiming'])
            need(hs >= end and integer(trial['harnessTiming']['serializationNs'])+
                 integer(trial['harnessTiming']['hashNs']) == ht, 'harness-partition-chronology')
            previous_end = he
            if repetition:
                for key, value in zip(contract['trialProtocol']['stageFields'], stages):
                    stage_totals[name][key] += value
        recalculated = summary(sid, trials)
        equal(index['summaries'][si], recalculated, 'all-summary-arithmetic')
        equal(checker['timingSummaries'][si], recalculated, 'checker-timing-summary')
        ratios = [rational(p['ratio']) for p in recalculated['pairs']]
        all_ratios.extend(ratios)
        audits.append({'sceneId': sid, 'drones': len(raw['drones']),
            'completeMedianSeconds': float(rational(recalculated['completeMedianNs'])/10**9),
            'hierarchyMedianSeconds': float(rational(recalculated['hierarchyMedianNs'])/10**9),
            'ratioOfMedians': recalculated['ratioOfMedians'],
            'medianPairedRatio': recalculated['medianPairedRatio'],
            'pairedRatios': recalculated['pairs'],
            'ratioRange': [float(min(ratios)), float(max(ratios))],
            'representativeScalarPairs': {m: counters[m]['scalarPairs'] for m in METHODS},
            'measuredStageTotalsNs': stage_totals,
            'methodDigests': digests, 'commonDigests': common_digests})
        equal(checker['scenes'][si]['methodDigests'], digests, 'checker-method-digests')
        equal(checker['scenes'][si]['commonDigests'], common_digests, 'checker-common-digests')
        for mi, method_report in enumerate(checker['scenes'][si]['methods']):
            name = METHODS[mi]
            equal(method_report['work'], counters[name], 'checker-work-agreement')
            need(method_report['verified'] is True and method_report['toleranceAchieved'] is True and
                 method_report['accountedPairs'] == 4*len(raw['drones'])*(len(raw['drones'])-1),
                 'checker-saved-scientific-verdict')
        reference = checker['scenes'][si]['referenceEvidence']
        check_pin(RESULTS/reference['path'], reference, 'reference-evidence')
        ref = strict_load(RESULTS/reference['path'], 'bare')
        need(ref['sceneId'] == sid and ref['rawInputSha256'] == raw_sha and
             len(ref['independentReference']) == len(raw['drones']), 'reference-count-identity')
        need(ref['referenceCoefficientBits'] == ref['referenceSourceBits'] == 192 and
             ref['referenceRootBisections'] == 128 and ref['plannedPairsPerMethod'] ==
             4*len(raw['drones'])*(len(raw['drones'])-1), 'reference-recipe-count-metadata')
        del shard, raw, ref
    journal = (RESULTS/'timing-index.json.jsonl').read_bytes().splitlines(keepends=True)
    expected_events = [('run-start', {k: index[k] for k in
                       ('specSha256','sourceManifestSha256','runtime','sourceSha256','constants')})]
    for si, descriptor in enumerate(index['scenes']):
        expected_events.append(('input-ready', {k: descriptor[k] for k in
            ('sceneIndex','rawInputSha256','inputConversionTiming')} | {'sceneId': descriptor['id']}))
        for local, trial in enumerate(index['trials'][si*10:si*10+10]):
            expected_events.append(('trial-complete', trial))
            if local == 3:
                expected_events.append(('representative-shard', descriptor))
        expected_events.append(('scene-complete', {'sceneIndex': si, 'sceneId': descriptor['id'],
            'firstSequence': si*10, 'lastSequence': si*10+9, 'sha256': descriptor['sha256']}))
    expected_events.append(('run-complete', {'resultPath': 'results/timing-index.json',
        'resultBytes': pin(RESULTS/'timing-index.json')['bytes'],
        'resultSha256': pin(RESULTS/'timing-index.json')['sha256'], 'trialCount': 60, 'sceneCount': 6}))
    need(len(journal) == len(expected_events) == 80, 'journal-event-count')
    for sequence, (line, (kind, payload)) in enumerate(zip(journal, expected_events)):
        value = decode(line)
        need(line == canon(value)+b'\n', 'journal-canonical-bytes')
        equal(value, {'schema': 'm31-screening-cost-journal-v1', 'eventSequence': sequence,
                     'type': kind, 'payload': payload}, 'journal-index-full-binding')
    for key in ('passed','verificationPassed','scientificQualification','fullQualification',
                'tolerancePassed','timingIntegrity','trialDigestConsistency','inputsUnchangedAfter',
                'sourcesUnchangedAfter'):
        need(checker[key] is True, 'checker-qualification:'+key)
    need(checker['errorCount'] == 0 and checker['errors'] == [] and
         checker['totalRecords'] == checker['qualifiedRecords'] == checker['admittedRecords'] == 6,
         'checker-counts-errors')
    need(checker['independentCoefficientOutcomes'] == 527776 and
         checker['validatedMethodOutcomes'] == 1055552, 'checker-coverage-counts')
    recipes = contract['controls']['recipes']
    need(len(checker['faultControls']) == len(recipes) == 15, 'control-count')
    for control, recipe in zip(checker['faultControls'], recipes):
        need(control['name'] == recipe['name'] and all(control[k] is True for k in
             ('executed','rejected','intendedCoreFailure')), 'control-result')
        equal(control['requiredFailureFamilies'], recipe['failurePrefixes'], 'control-failure-families')
        need(any(any(error.startswith(prefix) for prefix in recipe['failurePrefixes'])
                 for error in control['errors']), 'control-intended-error')
    need(not list((RESULTS/'anomalies').glob('*')), 'no-anomaly-output')
    public_bytes = sum(p.stat().st_size for p in RESULTS.rglob('*') if p.is_file())
    raw_bytes = sum((private/name).stat().st_size for name in
                    ('kernel-stdout.raw','kernel-stderr.raw','checker-stdout.raw','checker-stderr.raw'))
    need(public_bytes+raw_bytes < 384*1024*1024, 'saved-aggregate-cap')
    science_bytes = sum(d['bytes'] for d in index['scenes'])
    reference_bytes = sum(s['referenceEvidence']['bytes'] for s in checker['scenes'])
    need(reference_bytes == checker['referenceEvidenceBytes'], 'reference-total-bytes')
    expected_files = {'timing-index.json', 'timing-index.json.jsonl', 'independent-check.json'}
    expected_files |= {'scenes/'+s['id']+'.json' for s in spec['scenes']}
    expected_files |= {'reference-scenes/'+s['id']+'.json' for s in spec['scenes']}
    expected_files |= {stage+ending for stage in ('kernel','checker') for ending in
                      ('-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log','-supervision.json')}
    actual_files = {str(p.relative_to(RESULTS)) for p in RESULTS.rglob('*') if p.is_file()}
    need(actual_files == expected_files and not any(p.is_symlink() for p in RESULTS.rglob('*')),
         'closed-saved-output-set')
    need(all(d['bytes'] <= 64*1024*1024 for d in index['scenes']) and
         science_bytes <= 128*1024*1024, 'science-file-category-caps')
    need(all((RESULTS/n).stat().st_size <= 8*1024*1024 for n in
             ('timing-index.json','timing-index.json.jsonl')), 'index-journal-caps')
    need(reference_bytes+(RESULTS/'independent-check.json').stat().st_size <= 96*1024*1024,
         'checker-corpus-cap')
    metadata_bytes = raw_bytes + sum((RESULTS/n).stat().st_size for n in actual_files
        if any(n.endswith(s) for s in ('-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log')))
    need(metadata_bytes <= 16*1024*1024 and all((RESULTS/(s+'-supervision.json')).stat().st_size
         <= 65536 for s in ('kernel','checker')), 'logs-report-caps')
    audit = {'schema': 'm31-cost-generic-saved-audit-v1', 'passed': True,
        'scope': 'Saved JSON/hash/count/timing arithmetic only; no scientific import, oracle, candidate, checker, generator or control rerun.',
        'sourceCommit': commit, 'sourceManifestSha256': manifest_sha,
        'localAndGitManifestPinsVerified': len(seen), 'genericChecksPassed': checks,
        'trials': 60, 'measuredTrials': 48, 'warmupTrials': 12, 'journalEvents': 80,
        'representativeSelectionVerified': True, 'allTrialMethodAndCommonDigestsVerified': True,
        'allTimingStagesAndHarnessPartitionsVerified': True,
        'jsonFraming': {'kernelIndexShardsJournal': 'canonical JSON plus newline',
                        'checkerAndReferenceFiles': 'canonical JSON without newline'},
        'allSummariesExactlyRecomputed': True, 'all24PairedRatiosAboveOne': all(x > 1 for x in all_ratios),
        'scenes': audits, 'workTotalsOneCallPerMethodScene': work_totals,
        'workTotalsAllCalls': {m: {k: v*5 for k, v in row.items()} for m, row in work_totals.items()},
        'checkerSavedVerdict': {k: checker[k] for k in ('passed','qualifiedRecords','admittedRecords',
            'tolerancePassed','independentCoefficientOutcomes','validatedMethodOutcomes','errorCount')},
        'controlsSavedVerdicts': [{'name': c['name'], 'errors': c['errors'],
             'intendedCoreFailure': c['intendedCoreFailure']} for c in checker['faultControls']],
        'supervision': {stage: {k: report[k] for k in ('wallSeconds','peakSampledGroupRssBytes',
             'samples','maxSampleGapSeconds','success','closed')} for stage, report in supervisors.items()},
        'savedBytes': {'scienceShards': science_bytes, 'referenceEvidence': reference_bytes,
                      'allResults': public_bytes, 'privateRawLogs': raw_bytes,
                      'logsAndMetadata': metadata_bytes,
                      'resultsPlusPrivateRawLogs': public_bytes+raw_bytes},
        'privateRawLogsIndependentlyRehashed': True,
        'pins': {name: pin(RESULTS/name) for name in ('timing-index.json','timing-index.json.jsonl',
                  'independent-check.json','kernel-supervision.json','checker-supervision.json')}}
    out = BASE/'review/SAVED-EVIDENCE-AUDIT.json'
    out.write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps({k: audit[k] for k in ('passed','genericChecksPassed',
          'localAndGitManifestPinsVerified','all24PairedRatiosAboveOne','savedBytes')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--private-dir', type=Path, required=True)
    main(parser.parse_args().private_dir)
