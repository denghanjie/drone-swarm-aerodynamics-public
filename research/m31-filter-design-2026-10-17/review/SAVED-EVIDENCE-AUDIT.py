#!/usr/bin/env python3
"""Administrative saved-evidence audit only. Never imports scientific code.

Reads JSON/bytes, counts and compares saved fields, checks Git blobs and hashes.
Does not evaluate primitives, geometry, intervals, roots, or either oracle.
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

MIB = 1024 * 1024
SOURCE_COMMIT = 'abcee1164faa21c0e5a4b189daa4578699ea7577'
MANIFEST_SHA = 'cce61010030bdb8a62cdfd152fb2bb7ec1267fcc6d97f48bd9368098a3a71736'
SCIENTIFIC = {'filter-results.json', 'filter-results.json.jsonl'}
CHECKER = {'independent-check.json', 'reference.json'}
STAGES = ('kernel', 'checker')
META_SUFFIXES = ('-attempt.json', '-guardian.jsonl', '-stdout.log', '-stderr.log')
REPORTS = {s+'-supervision.json' for s in STAGES}
ALLOWED = SCIENTIFIC | CHECKER | REPORTS | {s+t for s in STAGES for t in META_SUFFIXES}
RAW_NAMES = {s+'-'+stream+'.raw' for s in STAGES for stream in ('stdout', 'stderr')}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicates(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k] = v
    return result


def load_bytes(data):
    return json.loads(data, object_pairs_hook=no_duplicates)


def compact(value):
    return json.dumps(value, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()+b'\n'


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-dir', required=True)
    args = parser.parse_args()
    package = Path(__file__).resolve().parents[1]
    root = package.parents[1]
    results = package/'results'
    private = Path(args.private_dir).resolve(strict=True)
    errors, reads, source_checks, stage_checks = [], {}, [], []
    check_count = 0

    def check(ok, code):
        nonlocal check_count
        check_count += 1
        if not ok:
            errors.append(code)

    def read(path, scope='repository'):
        check(path.is_file() and not path.is_symlink(), 'file-type:'+path.name)
        data = path.read_bytes()
        name = str(path.relative_to(root)) if scope == 'repository' else path.name
        reads[scope+':'+name] = {'scope':scope, 'path':name, 'bytes':len(data), 'sha256':sha(data)}
        return data

    def data(path, strict=False):
        raw = read(path)
        value = load_bytes(raw)
        if strict:
            check(raw == compact(value), 'compact-json:'+path.name)
        return value

    def pin(path, scope='repository'):
        raw = read(path, scope)
        return {'bytes':len(raw), 'sha256':sha(raw)}

    def full_pin(path):
        return {'path':str(path.relative_to(root)), **pin(path)}

    def git_bytes(relative):
        return subprocess.run(['git', 'show', SOURCE_COMMIT+':'+relative], cwd=root,
                              check=True, capture_output=True).stdout

    manifest_path = package/'source-manifest.json'
    manifest_raw = read(manifest_path)
    manifest = load_bytes(manifest_raw)
    manifest_relative = str(manifest_path.relative_to(root))
    check(sha(manifest_raw) == MANIFEST_SHA, 'manifest-expected-hash')
    check(git_bytes(manifest_relative) == manifest_raw, 'manifest-git-bytes')
    check(len(manifest['files']) == 51 and len({x['path'] for x in manifest['files']}) == 51,
          'manifest-51-unique-pins')
    for entry in manifest['files']:
        local = root/entry['path']
        check(local.resolve(strict=True).is_relative_to(root), 'manifest-root:'+entry['path'])
        local_data = read(local)
        committed_data = git_bytes(entry['path'])
        local_ok = len(local_data) == entry['bytes'] and sha(local_data) == entry['sha256']
        git_ok = len(committed_data) == entry['bytes'] and sha(committed_data) == entry['sha256']
        check(local_ok, 'source-local:'+entry['path'])
        check(git_ok and local_data == committed_data, 'source-git:'+entry['path'])
        source_checks.append({**entry, 'localMatch':local_ok, 'gitMatch':git_ok})
    publication = data(package/'source-publication.json')
    check(publication['commit'] == SOURCE_COMMIT and publication['manifestSha256'] == MANIFEST_SHA
          and publication['manifestBytes'] == len(manifest_raw) and publication['verifiedFilePins'] == 51
          and publication['remoteBytesEqualLocal'] is True and publication['committedBytesEqualLocal'] is True,
          'publication-receipt-identity')
    blob = subprocess.run(['git', 'rev-parse', SOURCE_COMMIT+':'+manifest_relative], cwd=root,
                          check=True, capture_output=True, text=True).stdout.strip()
    check(blob == publication['manifestGitBlob'], 'publication-manifest-git-blob')
    check(publication['remoteUrl'] == 'https://raw.githubusercontent.com/denghanjie/drone-swarm-aerodynamics-public/'
          +SOURCE_COMMIT+'/'+manifest_relative, 'publication-exact-commit-url')
    spec = data(package/'source/spec.json')
    contract = data(package/'source/result-contract.json')
    runtimes = data(package/'runtime-pins.json')
    document = data(results/'filter-results.json', True)
    reference = data(results/'reference.json', True)
    report = data(results/'independent-check.json', True)
    declarations, rows, refs = spec['records'], document['records'], reference['records']
    check(len(rows) == len(refs) == len(declarations) == 108, '108-records-and-references')
    ids = [r['id'] for r in rows]
    check(ids == [r['id'] for r in declarations] == [r['id'] for r in refs] and len(set(ids)) == 108,
          'record-order-identity-unique')
    identity = {'specId':spec['id'], 'sourceManifestSha256':MANIFEST_SHA,
                'specSha256':pin(package/'source/spec.json')['sha256']}
    check(all(document[k] == v and reference[k] == v for k, v in identity.items()), 'saved-identities')
    check(document['schema'] == contract['schema'] and reference['schema'] == 'm31-filter-reference-v1',
          'saved-schemas')
    check(same(document['constants'], reference['constants']), 'constant-tables-equal')
    check(reference['helperSha256'] == contract['independentHelper']['sha256']
          == pin(package/'source/semantic-reference.py')['sha256'], 'helper-reference-pin')
    check(same(reference['sourceManifest'], {'bytes':len(manifest_raw),'sha256':MANIFEST_SHA}),
          'reference-manifest-pin')
    check(same(report['referencePin'], pin(results/'reference.json')), 'checker-reference-pin')
    for relative, expected in reference['inputPins'].items():
        check(same(pin(root/relative), expected), 'reference-input-pin:'+relative)
    journal_raw = read(results/'filter-results.json.jsonl')
    lines = journal_raw.splitlines(keepends=True)
    events = [load_bytes(line) for line in lines]
    check(len(events) == 110 and all(line == compact(e) for line,e in zip(lines,events)),
          'journal-110-compact-events')
    expected_header = {'kind':'header','schema':contract['journalSchema'], **identity}
    check(same(events[0], expected_header), 'journal-header')
    check(same(events[-1], {'kind':'complete','records':108}), 'journal-completion')
    check(all(same(e, {'kind':'record','row':r}) for e,r in zip(events[1:-1],rows)), 'journal-all-rows')

    kinds, outcomes, refusals, finite = Counter(), Counter(), Counter(), Counter()
    decisions, fast, reasons, fallback_branches, statuses, branches, prep = (Counter() for _ in range(7))
    positive_fallbacks = 0
    ref_by_id = {r['id']:r for r in refs}
    for item, row, ref in zip(declarations, rows, refs):
        kinds[row['kind']] += 1
        check(row['kind'] == item['kind'] == ref['kind'], 'row-kind:'+row['id'])
        if row['kind'] == 'primitive':
            check(all(same(row[k], v) for k,v in item.items()), 'primitive-input:'+row['id'])
            op, category = row['op'], row['outcome']['kind']
            outcomes[op+':'+category] += 1
            if category == 'interval': finite[op] += 1
            if category == 'fallback': refusals[row['outcome']['reason']] += 1
        else:
            raw = {k:item[k] for k in ('receiver','source','rotor')}
            check(same(row['input'], raw) and same(ref['input'], raw), 'raw-binding:'+row['id'])
            check(same(row['prepared'], ref['prepared']), 'prepared-binding:'+row['id'])
            check(same(row['baseline'], row['candidate']['result']), 'saved-fallback-identity:'+row['id'])
            check(all(row['baseline'][k] == ref[k] for k in ('status','branch')),
                  'saved-reference-classification:'+row['id'])
            decision, status, branch = row['candidate']['decision'], ref['status'], ref['branch']
            decisions[decision['kind']] += 1
            statuses[status] += 1
            branches[branch] += 1
            if decision['kind'] == 'zero':
                fast[branch] += 1
                check(status == 'zero' and decision['branch'] == branch, 'saved-fast-branch:'+row['id'])
            elif decision['kind'] == 'fallback':
                reasons[decision['reason']] += 1
                fallback_branches[branch] += 1
                positive_fallbacks += int(status == 'positive')
            else:
                prep[branch] += 1
                check(decision == {'kind':'preparation'} and row['prepared']['rejection'] == branch,
                      'saved-preparation-gate:'+row['id'])
    summaries = {'finiteIntervalCounts':dict(finite),'primitiveOutcomeCounts':dict(outcomes),
                 'primitiveRefusalReasonCounts':dict(refusals),'decisionCounts':dict(decisions),
                 'fastZeroBranchCounts':dict(fast),'fallbackReasonCounts':dict(reasons),
                 'oracleStatusCounts':dict(statuses),'oracleBranchCounts':dict(branches),
                 'fallbackBranchCounts':dict(fallback_branches),'positiveFallbacks':positive_fallbacks}
    check(kinds == {'primitive':72,'pair':36}, 'record-family-counts')
    check(all(same(report[k], v) for k,v in summaries.items()), 'report-counts-reconciled')
    check(all(report[k] is True for k in ('passed','verificationPassed','fullQualification','controlsPassed',
          'sourceAndInputsUnchanged','journalPassed')) and report['qualifiedRecords'] == 108
          and report['totalRecords'] == 108 and report['errors'] == [] and report['errorCount'] == 0,
          'checker-qualification-and-zero-errors')
    controls = report['faultControls']
    check(len(controls) == contract['controls']['count'] == 16, '16-controls')
    control_checks = []
    for control, recipe in zip(controls, contract['controls']['recipes']):
        passed = (control['id'] == recipe['id'] and control['expectedFailure'] == recipe['failure']
                  and control['passed'] is True and recipe['failure'] in control['detectedFailures']
                  and 'witnessFailure' not in control)
        witness = control['witness']
        row_id = witness.get('row')
        if row_id:
            check(row_id in ref_by_id, 'control-witness-row:'+control['id'])
            target = ref_by_id[row_id]
            if 'exactRange' in witness:
                check(same(witness['exactRange'],target['exactRange']), 'control-range-binding:'+control['id'])
            if 'referenceStatus' in witness:
                check(witness['referenceStatus'] == target['status'] and witness['referenceBranch'] == target['branch'],
                      'control-classification-binding:'+control['id'])
            if 'coefficient' in witness:
                check(same(witness['coefficient'],target['referenceIntervals']['coefficient']),
                      'control-coefficient-binding:'+control['id'])
        if control['id'] == 'missing-row': check(witness['removedId'] == ids[-1], 'control-missing-witness')
        if control['id'] == 'duplicate-row': check(witness['duplicatedId'] == ids[0], 'control-duplicate-witness')
        if control['id'] == 'reordered-rows': check(witness['swappedIds'] == ids[:2], 'control-order-witness')
        check(passed, 'control-intended-detection:'+control['id'])
        control_checks.append({'id':control['id'],'expectedFailure':recipe['failure'],
                               'detectedFailures':control['detectedFailures'],'savedWitnessConsistent':passed})

    actual_result_files = list(results.rglob('*'))
    check(all(p.is_file() and not p.is_symlink() for p in actual_result_files), 'results-flat-regular')
    check({p.name for p in actual_result_files} == ALLOWED, 'exact-14-result-files')
    check({p.name for p in private.iterdir()} == RAW_NAMES and all(p.is_file() and not p.is_symlink()
          for p in private.iterdir()), 'exact-4-private-raw-logs')
    private_identity = sha(str(private).encode())

    def accounting(entries):
        totals = {'aggregateBytes':0,'documentBytes':0,'journalBytes':0,'checkerBytes':0,
                  'logMetadataBytes':0,'reportBytes':0,'unclassifiedBytes':0}
        for entry in entries:
            p = (results if entry['scope'] == 'results' else private)/entry['path']
            size = len(read(p, 'repository' if entry['scope'] == 'results' else 'private'))
            check(size == entry['bytes'], 'accounting-file-size:'+entry['path'])
            totals['aggregateBytes'] += size
            n = entry['path']
            if entry['scope'] == 'private': category = 'logMetadataBytes'
            elif n == 'filter-results.json': category = 'documentBytes'
            elif n == 'filter-results.json.jsonl': category = 'journalBytes'
            elif n in CHECKER: category = 'checkerBytes'
            elif n in REPORTS: category = 'reportBytes'
            elif n in ALLOWED: category = 'logMetadataBytes'
            else: category = 'unclassifiedBytes'
            totals[category] += size
        return totals

    starts = {}
    for stage in STAGES:
        supervision = data(results/(stage+'-supervision.json'))
        attempt = data(results/(stage+'-attempt.json'))
        starts[stage] = datetime.fromisoformat(attempt['startedUtc'].replace('Z','+00:00'))
        check(attempt['stage'] == stage and attempt['sourceCommit'] == SOURCE_COMMIT
              and attempt['sourceManifestSha256'] == MANIFEST_SHA
              and attempt['allocation'] == 'sole attempt; existence prevents retry', 'attempt-identity:'+stage)
        check(supervision['stage'] == stage and supervision['sourceCommit'] == SOURCE_COMMIT
              and supervision['sourceManifestSha256'] == MANIFEST_SHA
              and same(supervision['runtimePins'],runtimes), 'supervision-identity:'+stage)
        check(all(supervision[k] is True for k in ('success','closed','scientificChildAbsentBeforeRelease',
              'childGroupAbsent','sourceAndRuntimeRechecked')) and supervision['exitCode'] == 0
              and supervision['guardianExitCode'] == 0 and supervision['terminationReason'] is None,
              'supervision-closure:'+stage)
        check(supervision['wallLimitSeconds'] == 300 and supervision['guardianWallLimitSeconds'] == 310
              and supervision['sampledRssLimitBytes'] == 512*MIB and supervision['outputLimitBytes'] == 96*MIB
              and supervision['wallSeconds'] <= 300 and supervision['peakSampledGroupRssBytes'] <= 512*MIB
              and supervision['samples'] > 0, 'stage-budgets:'+stage)
        lifecycle = [load_bytes(line) for line in read(results/(stage+'-guardian.jsonl')).splitlines()]
        check(len(lifecycle) == 2 and lifecycle[0]['event'] == 'child-start'
              and lifecycle[1]['event'] == 'child-exit' and lifecycle[1]['exitCode'] == 0
              and lifecycle[0]['pid'] == lifecycle[1]['pid']
              and lifecycle[0]['guardian'] == supervision['processGroup'], 'guardian-lifecycle:'+stage)
        check(supervision['privateLogDirectorySha256'] == private_identity, 'private-directory-binding:'+stage)
        for expected in supervision['privateRawLogs']:
            check(same(pin(private/expected['name'],'private'), {k:expected[k] for k in ('bytes','sha256')}),
                  'private-raw-log-pin:'+stage+':'+expected['name'])
        for expected in supervision['logs']:
            public = root/expected['path']
            raw_name = public.stem+'.raw'
            raw = read(private/raw_name, 'private')
            public_data = read(public)
            check(len(raw) == expected['rawBytes'] and sha(raw) == expected['rawSha256']
                  and len(public_data) == expected['publishedBytes'] and sha(public_data) == expected['publishedSha256'],
                  'public-private-log-pins:'+public.name)
            check(raw == public_data, 'these-logs-need-no-redaction:'+public.name)
        for key in ('output','journal'):
            if key in supervision:
                expected = supervision[key]
                check(same(full_pin(root/expected['path']),expected), 'stage-'+key+'-pin:'+stage)
        for key in ('scientificEvidence','checkerEvidence'):
            for expected in supervision.get(key,[]):
                check(same(full_pin(root/expected['path']),expected), 'stage-evidence-pin:'+stage+':'+expected['path'])
        snapshot = supervision['outputAccountingBeforeReport']
        totals = accounting(snapshot['files'])
        check(all(snapshot[k] == v for k,v in totals.items()) and snapshot['violations'] == []
              and supervision['finalOutputBytesBeforeReport'] == totals['aggregateBytes'],
              'snapshot-accounting:'+stage)
        expected_names = SCIENTIFIC | {stage+t for t in META_SUFFIXES}
        if stage == 'checker': expected_names |= CHECKER | {'kernel'+t for t in META_SUFFIXES} | {'kernel-supervision.json'}
        check({e['path'] for e in snapshot['files'] if e['scope'] == 'results'} == expected_names,
              'snapshot-result-set:'+stage)
        expected_raw = RAW_NAMES if stage == 'checker' else {n for n in RAW_NAMES if n.startswith('kernel-')}
        check({e['path'] for e in snapshot['files'] if e['scope'] == 'private'} == expected_raw,
              'snapshot-private-set:'+stage)
        stage_checks.append({'stage':stage,'success':True,'closed':True,'wallSeconds':supervision['wallSeconds'],
                             'peakSampledGroupRssBytes':supervision['peakSampledGroupRssBytes'],
                             'samples':supervision['samples'],'maxSampleGapSeconds':supervision['maxSampleGapSeconds'],
                             'accountingBeforeReport':totals})
    verified = datetime.fromisoformat(publication['verifiedUtc'])
    check(verified < starts['kernel'] < starts['checker'], 'publication-before-ordered-attempts')
    final_entries = [{'scope':'results','path':p.name,'bytes':p.stat().st_size} for p in sorted(results.iterdir())]
    final_entries += [{'scope':'private','path':p.name,'bytes':p.stat().st_size} for p in sorted(private.iterdir())]
    final = accounting(final_entries)
    check(final['aggregateBytes'] <= 96*MIB and final['documentBytes'] <= 16*MIB
          and final['journalBytes'] <= 16*MIB and final['checkerBytes'] <= 32*MIB
          and final['logMetadataBytes'] <= 8*MIB and final['unclassifiedBytes'] == 0
          and all((results/n).stat().st_size <= 65536 for n in REPORTS), 'final-all-output-budgets')
    check(load_bytes(read(private/'kernel-stdout.raw','private')) == {'records':108,'journalEvents':110},
          'kernel-stdout-counts')
    check(load_bytes(read(private/'checker-stdout.raw','private')) == {'passed':True,'totalRecords':108,'controlsPassed':True},
          'checker-stdout-status')
    check(all((private/(s+'-stderr.raw')).stat().st_size == 0 for s in STAGES), 'empty-stderr')
    audit_script_pin = pin(Path(__file__))
    output = {'schema':'m31-filter-saved-evidence-administrative-audit-v1','passed':not errors,
              'sourceCommit':SOURCE_COMMIT,'sourceManifestSha256':MANIFEST_SHA,'checkCount':check_count,
              'errors':errors,'sourcePins':source_checks,'records':dict(kinds),'journalEvents':len(events),
              'summaries':summaries,'preparationRejectionBranches':dict(prep),'controls':control_checks,
              'stages':stage_checks,'finalOutputAccounting':final,'savedEvidencePins':list(reads.values()),
              'auditScriptPin':audit_script_pin,
              'scope':'Saved-byte identity, JSON binding, counts, lifecycle and resource-accounting audit only.',
              'notPerformed':['No scientific source import or model/oracle evaluation','No candidate/checker rerun',
                              'No numerical containment recomputation','No new network fetch',
                              'No live process-group re-probe or signals','No frozen source edits'],
              'sourcePublicationEvidence':'Saved exact-commit HTTPS receipt cross-checked against local/Git manifest and all 51 pins; remote fetch not repeated.',
              'closureEvidence':'Saved supervisor closure assertions agree with paired guardian child-start/zero-exit events; process-group IDs were not re-probed after possible reuse.',
              'readingScope':'All evidence and source metadata pins read in this new package; inherited source bytes were hashed only. No additional inherited semantic content read.'}
    destination = package/'review/SAVED-EVIDENCE-AUDIT.json'
    destination.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':not errors,'checks':check_count,'sourcePins':len(source_checks),
                      'records':dict(kinds),'controls':len(controls),'finalOutputBytes':final['aggregateBytes'],
                      'errors':errors},sort_keys=True))
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
