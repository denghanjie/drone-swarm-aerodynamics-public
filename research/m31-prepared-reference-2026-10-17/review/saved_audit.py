"""Proposed single saved-only prepared-reference audit; standard library only.

No candidate/oracle/checker is imported or executed. Local git cat-file reads
committed source blobs. All other operations inspect saved JSON and byte pins.
Execution requires the parent-reviewed audit manifest SHA as an argument.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import time

PACKAGE = 'research/m31-prepared-reference-2026-10-17'
TREE = 'research/m31-tree-first-reference-2026-10-17'
FRESH = 'research/m31-native-fresh-transfer-2026-10-17'
COMMIT = 'fdea9e3af256cb5745ae630fad4a7a3b8a56fd6e'
SOURCE_SHA = '581d8778c7c0a2f00fab3d4dfb3fd253b882f5aacc76ece3f22f8b4629c7e213'
BASELINE_SHA = '3cd3f06d9d4ef1c43ffeceff445ba3fcd424f32c3e569ead4cceddf442104a7e'
SCENES = [
    'offset-singleton', 'dense-cube-27', 'dense-cube-64', 'sparse-cube-64',
    'four-columns-32', 'tilted-cube-16', 'permuted-cube-27', 'neighbor-boundary-16',
    'near-slab-outside-16', 'radial-outside-16', 'down-cut-boundary-16',
    'near-domain-refusal', 'scaled-cap-refusal', 'upward-order-refusal',
    'global-invalid-three', 'center-guard-fallback', 'center-guard-equality',
    'raw-force-refusal', 'positive', 'distant-zero', 'raw-force',
    'order-incompatible', 'fresh-a-t5', 'fresh-b-t5']
COUNTERS = ['prepareOneCalls', 'preparationValidCalls', 'oracleCalls', 'operandLookups', 'pairPreparations']
BINDINGS = [
    ('unregistered-receiver', 'prepared-unregistered-receiver', 1),
    ('unregistered-source', 'prepared-unregistered-source', 2),
    ('mutated-prepared-center', 'prepared-operand-mutated', 1),
    ('changed-constant-word', 'prepared-constants-context', 0),
    ('changed-corner-order', 'prepared-corners-context', 0),
    ('closed-context', 'prepared-context-closed', 0)]
OLD_CONTROLS = ['positive-falsely-zero', 'dropped-source', 'duplicate-plus-omission-equal-count',
                'forged-node-bound', 'index-id-swap', 'guard-bypass-zero']
FIXTURES = ['one-word', 'signed-zero', 'minimum-subnormal', 'halfway-even-down',
            'halfway-even-up', 'subnormal-half-to-zero', 'negative-halfway-even',
            'scalar-inside-box', 'euclidean-3-4-5', 'strict-threshold-inclusive',
            'strict-threshold-fail', 'reference-overlap-unresolved',
            'rational-square-root-enclosure', 'signed-moment-cancellation']


class AuditError(Exception):
    pass


def need(value, code):
    if not value:
        raise AuditError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def verify_pin(root, pin):
    path = Path(pin['path'])
    need(not path.is_absolute() and '..' not in path.parts, 'safe-pin-path')
    raw = (root / path).read_bytes()
    need(len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], 'local-pin:' + pin['path'])
    return raw


def verify_commit(root, pins):
    verified = 0
    for start in range(0, len(pins), 48):
        batch = pins[start:start + 48]
        query = ''.join(COMMIT + ':' + p['path'] + '\n' for p in batch).encode()
        proc = subprocess.run(['git', 'cat-file', '--batch'], input=query,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=root, timeout=20, check=False)
        need(proc.returncode == 0, 'git-read-exit')
        cursor = 0
        for pin in batch:
            newline = proc.stdout.index(b'\n', cursor)
            header = proc.stdout[cursor:newline].split()
            need(len(header) == 3 and header[1] == b'blob', 'git-read-blob')
            size = int(header[2]); begin = newline + 1
            raw = proc.stdout[begin:begin + size]
            need(proc.stdout[begin + size:begin + size + 1] == b'\n', 'git-read-framing')
            need(size == pin['bytes'] and digest(raw) == pin['sha256'], 'committed-pin:' + pin['path'])
            cursor = begin + size + 1
            verified += 1
        need(cursor == len(proc.stdout), 'git-read-extra-bytes')
    return verified


def case_review(case, previous, new, old, raw_equal):
    name = case['id']; n = case['n']
    need(new == old and case['exactSavedTreeEquality'] is True, 'entire-wire-equality:' + name)
    need(new['id'] == name and len(new['input']['drones']) == n and n <= 64, 'fixed-scene:' + name)
    need([row['id'] for row in new['prepared']] == [row['id'] for row in new['input']['drones']],
         'prepared-id-association:' + name)
    need(new['planned'] == 4 * n * (n - 1), 'planned-pairs:' + name)
    raw_refusals = [row for row in new['prepared'] if row['rejection'] in ('raw-force', 'raw-nonfinite')]
    need(all(row['value'] is None for row in raw_refusals), 'raw-refusal-no-preparation:' + name)
    need(all(row['value'] is not None for row in new['prepared'] if row not in raw_refusals),
         'nonraw-row-prepared:' + name)
    actual_preparations = n - len(raw_refusals)
    calls = len(new['pairs'])
    expected = {'prepareOneCalls': actual_preparations, 'preparationValidCalls': actual_preparations,
                'oracleCalls': calls, 'operandLookups': 2 * calls, 'pairPreparations': 0}
    need(case['reuseCounters'] == expected and all(type(v) is int for v in case['reuseCounters'].values()),
         'actual-preparation-and-suffix-counters:' + name)
    need(calls == previous['treeOracleCalls'] == previous['validation']['scalarPairs'], 'frozen-scalar-count:' + name)
    need(new['coverage']['work']['preparationCalls'] == n, 'logical-versus-actual-preparation:' + name)
    need(new['coverage']['work']['scalarPairs'] == calls, 'wire-scalar-count:' + name)
    need('not a performance estimate' in case['timingScope'], 'timing-scope-label:' + name)
    positive_count = sum(pair['oracle']['status'] == 'positive' for pair in new['pairs'])
    root_count = sum(len(row['roots']) for row in new['loads'])
    load_count = sum(len(row['loads']['rotor']) + 1 + len(row['loads']['force']) + len(row['loads']['moment'])
                     for row in new['loads'])
    return {'id': name, 'n': n, 'wireStructurallyIdentical': True, 'wireBytesIdentical': raw_equal,
            'status': new['status'], 'branch': new['branch'], 'witness': new['witness'],
            'plannedPairs': new['planned'], 'coveredPairs': new['coverage']['coveredPairs'],
            'provedZeroPairs': new['coverage']['work']['zeroPairs'], 'positivePairs': positive_count,
            'rootBoxesEqual': root_count, 'signedLoadBoxesEqual': load_count,
            'rawRefusedIds': [row['id'] for row in raw_refusals],
            'actualPreparationCalls': actual_preparations, 'logicalPreparationCalls': n,
            'preparationRejectedIds': [row['id'] for row in new['prepared'] if row['rejection'] == 'preparation'],
            'reuseCounters': expected, 'mode': new['coverage']['mode']}


def main(root, expected_audit_sha):
    package = root / PACKAGE
    review = package / 'review'
    output = review / 'saved-audit-result.json'
    started_marker = review / 'AUDIT-STARTED.json'
    need(not output.exists() and not started_marker.exists(), 'single-audit-allocation')
    started = time.monotonic()
    report = {'schema': 'm31-prepared-reference-saved-audit-v1', 'status': 'running',
              'startedUtc': datetime.now(timezone.utc).isoformat(), 'sourceCommit': COMMIT,
              'sourceManifestSha256': SOURCE_SHA, 'auditManifestSha256': expected_audit_sha,
              'scientificModulesImported': False, 'scientificExecutions': 0,
              'browserCalls': 0, 'networkCalls': 0, 'cases': [], 'errors': [],
              'processingLimitSeconds': 120, 'timingClaim': False, 'physicalValidation': False}
    with started_marker.open('x') as stream:
        json.dump({'startedUtc': report['startedUtc'], 'auditManifestSha256': expected_audit_sha,
                   'singleUse': True}, stream)
        stream.write('\n')
    def alarm(signum, frame):
        raise AuditError('saved-only-audit-deadline')
    signal.signal(signal.SIGALRM, alarm); signal.alarm(115)
    try:
        audit_raw = (review / 'audit-source-manifest.json').read_bytes()
        need(digest(audit_raw) == expected_audit_sha, 'reviewed-audit-source-manifest')
        audit = json.loads(audit_raw)
        need(audit['scientificSourceCommit'] == COMMIT and audit['scientificSourceManifest']['sha256'] == SOURCE_SHA
             and audit['processingLimitSeconds'] == 120 and audit['executionAuthorized'] is False,
             'audit-source-contract')
        need([p['path'] for p in audit['auditSourceFiles']]
             == [PACKAGE + '/review/saved_audit.py', PACKAGE + '/review/AUDIT-SOURCE-REVIEW.md'],
             'reviewed-audit-source-files')
        # executionAuthorized=False records that this manifest was prepared before
        # the parent reviewed and separately authorized its single invocation.
        pins = audit['auditSourceFiles'] + audit['inputFiles']
        need(len({p['path'] for p in pins}) == len(pins), 'unique-audit-pins')
        for pin in pins:
            verify_pin(root, pin)
        pin_map = {p['path']: p for p in pins}
        for path in (TREE + '/review/saved-result-audit.json', FRESH + '/results/check.json',
                     PACKAGE + '/source-publication.json', PACKAGE + '/STARTED.json'):
            need(path in pin_map, 'saved-dependency-pinned:' + path)
        source_raw = verify_pin(root, audit['scientificSourceManifest'])
        source = json.loads(source_raw)
        need(len(source['files']) == 689, '689-frozen-source-pins')
        for pin in source['files']:
            need(pin_map.get(pin['path']) == pin, 'transitive-scientific-source-pin')
        runtime = source['runtime']['python']; executable = Path(sys.executable).resolve().read_bytes()
        need(sys.flags.isolated == 1 and sys.dont_write_bytecode and sys.version == runtime['version']
             and len(executable) == runtime['bytes'] and digest(executable) == runtime['sha256'], 'pinned-python-runtime')
        need((datetime(2026, 10, 17, 3, tzinfo=timezone.utc) - datetime.now(timezone.utc)).total_seconds() >= 120,
             'full-audit-reservation-before-cutoff')
        committed = verify_commit(root, source['files'] + [audit['scientificSourceManifest']])
        report['sourceVerification'] = {'localSourcePins': 689, 'exactCommitSourcePins': committed - 1,
                                        'sourceManifestExactCommit': True,
                                        'totalReviewedFilePins': len(pins), 'pinnedPythonMatches': True}
        index_path = PACKAGE + '/results/index.json'
        index_raw = verify_pin(root, pin_map[index_path]); index = json.loads(index_raw)
        report['resultIndexSha256'] = digest(index_raw)
        need(index['sourceCommit'] == COMMIT and index['sourceManifestSha256'] == SOURCE_SHA
             and index['status'] == 'completed' and index['complete'] is True and index['qualified'] is True,
             'completed-scientific-result')
        need(index['expectedCases'] == 24 and index['expectedLogicalPairs'] == 79048
             and index['expectedScalarCalls'] == 26570 and index['scalarOracleCalls'] == 26570
             and index['scalarOracleCalls'] <= 30000, 'fixed-scientific-allocation')
        need(index['newSimulations'] == index['newBrowserCalls'] == index['newFullOracleRuns'] == 0
             and index['physicalValidation'] is False and index['performanceClaim'] is False, 'scientific-scope-flags')
        need([c['id'] for c in index['cases']] == SCENES, 'exact-24-case-order')
        baseline_raw = verify_pin(root, index['baselineIndex'])
        need(digest(baseline_raw) == BASELINE_SHA and pin_map[index['baselineIndex']['path']] == index['baselineIndex'],
             'frozen-qualified-baseline-index')
        baseline = json.loads(baseline_raw)
        need(baseline['complete'] is True and baseline['qualified'] is True
             and [c['id'] for c in baseline['cases']] == SCENES, 'qualified-24-case-baseline')
        prior_audit = load(root / TREE / 'review/saved-result-audit.json')
        need(prior_audit['status'] == 'passed' and prior_audit['errors'] == []
             and prior_audit['resultIndexSha256'] == BASELINE_SHA, 'prior-independent-baseline-audit')
        result_paths, result_bytes = [], 0
        for case, previous in zip(index['cases'], baseline['cases']):
            need(case['baseline'] == previous['tree'] and pin_map[case['baseline']['path']] == case['baseline'],
                 'exact-baseline-record-pin:' + case['id'])
            need(case['result']['path'] == PACKAGE + '/results/' + case['id'] + '.json'
                 and pin_map[case['result']['path']] == case['result'], 'candidate-result-pin:' + case['id'])
            new_raw = verify_pin(root, case['result']); old_raw = verify_pin(root, case['baseline'])
            new, old = json.loads(new_raw), json.loads(old_raw)
            report['cases'].append(case_review(case, previous, new, old, new_raw == old_raw))
            result_paths.append(case['result']['path']); result_bytes += len(new_raw)
        # Controls are inspected as saved reports, never invoked by this audit.
        controls = index['bindingControls']
        need(len(controls) == 6, 'six-binding-controls')
        for control, (name, code, lookups) in zip(controls, BINDINGS):
            expected = {'id': name, 'scene': 'dense-cube-27', 'detected': True,
                        'expectedReason': code, 'reason': code,
                        'reuseCounterDelta': {'prepareOneCalls': 0, 'preparationValidCalls': 0,
                                              'oracleCalls': 0, 'operandLookups': lookups, 'pairPreparations': 0},
                        'budgetOracleDelta': 0, 'setupPreparationCalls': 0}
            need(control == expected, 'exact-binding-control-and-zero-suffix:' + name)
        need(len({c['reason'] for c in controls}) == 6, 'distinct-binding-reasons')
        report['bindingControls'] = controls
        old_check = load(root / FRESH / 'results/check.json')
        need(index['arithmeticFixtures'] == old_check['arithmeticFixtures']
             == [{'id': name, 'passed': True} for name in FIXTURES], 'exact-fourteen-arithmetic-reports')
        need(index['nativeCalls'] == old_check['calls'] and len(index['nativeCalls']) == 4
             and all(c['qualified'] is True and c['decision'] == 'qualified' for c in index['nativeCalls']),
             'exact-four-native-reports')
        need(index['loadCorruptions'] == old_check['corruptionChecks'] and len(index['loadCorruptions']) == 4
             and all(c['passed'] is True for c in index['loadCorruptions']), 'exact-four-load-control-reports')
        need(index['retainedCoverageControlIds'] == OLD_CONTROLS
             == [c['id'] for c in baseline['coverageCorruptions']]
             and all(c['detected'] is True for c in baseline['coverageCorruptions'])
             and index['coverageControlsRerun'] is False, 'old-six-coverage-controls-retained-only')
        report['retainedReports'] = {'arithmeticExactlyEqual': 14, 'nativeExactlyEqual': 4,
                                     'loadCorruptionsExactlyEqual': 4, 'coverageControlsRetained': OLD_CONTROLS,
                                     'coverageControlsRerun': False, 'anyReportReexecutedByAudit': False}
        event_raw = verify_pin(root, index['eventJournal'])
        need(pin_map[index['eventJournal']['path']] == index['eventJournal'], 'event-pin-in-audit-manifest')
        events = [json.loads(line) for line in event_raw.splitlines()]
        need(len(events) == 48, '48-journal-events')
        running = 0
        for ordinal, case in enumerate(index['cases']):
            need(events[2 * ordinal] == {'event': 'start', 'ordinal': ordinal, 'id': case['id'], 'callsBefore': running},
                 'event-start:' + case['id'])
            running += case['reuseCounters']['oracleCalls']
            need(events[2 * ordinal + 1] == {'event': 'complete', 'ordinal': ordinal, 'id': case['id'],
                                            'result': case['result'], 'callsAfter': running}, 'event-finish:' + case['id'])
        need(running == 26570, 'event-call-total')
        result_paths.append(index['eventJournal']['path']); result_bytes += len(event_raw)
        need(result_bytes == index['resultBytesBeforeIndex'], 'saved-result-byte-total')
        actual_paths = {str(p.relative_to(root)) for p in (package / 'results').rglob('*') if p.is_file()}
        need(actual_paths == set(result_paths) | {index_path}, 'exact-26-scientific-result-files')
        report['resultVerification'] = {'candidatePins': 24, 'baselinePins': 24,
                                        'eventLines': 48, 'resultFiles': len(actual_paths),
                                        'bytesBeforeIndex': result_bytes, 'indexBytes': len(index_raw),
                                        'byteIdenticalCandidateFiles': sum(c['wireBytesIdentical'] for c in report['cases'])}
        receipt = load(package / 'source-publication.json'); started_receipt = load(package / 'STARTED.json')
        need(receipt['commit'] == COMMIT and receipt['manifestSha256'] == SOURCE_SHA
             and receipt['verifiedFilePins'] == 689 and receipt['remoteBytesEqualLocal'] is True
             and receipt['committedBytesEqualLocal'] is True, 'saved-publication-receipt')
        need(started_receipt['sourceCommit'] == COMMIT and started_receipt['sourceManifestSha256'] == SOURCE_SHA
             and started_receipt['sourcePinsVerified'] == index['sourcePinsAfter'] == 689
             and index['outputsPreserved'] is True, 'scientific-before-after-source-receipts')
        need(datetime.fromisoformat(receipt['verifiedUtc']) < datetime.fromisoformat(started_receipt['utc'])
             <= datetime.fromisoformat(index['startedUtc']) < datetime.fromisoformat(index['finishedUtc'])
             < datetime(2026, 10, 17, 3, tzinfo=timezone.utc), 'scientific-publication-run-time-order')
        need(0 <= index['wallSeconds'] < 600, 'scientific-reservation')
        totals = Counter()
        for case in report['cases']:
            totals.update(case['reuseCounters'])
        report['reuseTotals'] = dict(totals)
        report['totals'] = {key: sum(case[key] for case in report['cases']) for key in
                             ('plannedPairs', 'coveredPairs', 'provedZeroPairs', 'positivePairs', 'rootBoxesEqual',
                              'signedLoadBoxesEqual', 'logicalPreparationCalls', 'actualPreparationCalls')}
        report['rawRefusals'] = [{'scene': case['id'], 'id': identifier} for case in report['cases'] for identifier in case['rawRefusedIds']]
        need(totals == Counter({'prepareOneCalls': 447, 'preparationValidCalls': 447,
                                'oracleCalls': 26570, 'operandLookups': 53140, 'pairPreparations': 0}),
             'expected-global-reuse-counters')
        need(len(report['rawRefusals']) == 2 and report['totals']['logicalPreparationCalls'] == 449,
             'two-raw-refusals-versus-logical-preparations')
        report['decisionTotals'] = dict(Counter(case['status'] + ':' + case['branch'] for case in report['cases']))
        report['savedScientificWallSeconds'] = index['wallSeconds']
        report['oldResidualPreparationCountSourceDerivedNotMeasured'] = 2 * totals['oracleCalls']
        # No numerical predicate is recomputed: byte equality retains the already
        # qualified old coverage proof, scalar decisions, coefficients and loads.
        for pin in pins:
            verify_pin(root, pin)
        need((review / 'audit-source-manifest.json').read_bytes() == audit_raw, 'audit-manifest-unchanged')
        report['allReviewedBytesUnchangedAtClosure'] = True
        report['remoteReceiptConsistentNotRefetched'] = True
        report['status'] = 'passed'
    except Exception as error:
        report['status'] = 'failed'
        report['errors'].append({'class': type(error).__name__, 'message': str(error)[:500]})
    finally:
        signal.alarm(0)
        report['processingSeconds'] = time.monotonic() - started
        report['finishedUtc'] = datetime.now(timezone.utc).isoformat()
        if report['processingSeconds'] >= 120:
            report['status'] = 'failed'
            report['errors'].append({'class': 'AuditError', 'message': '120-second-processing-cap'})
        payload = (json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
        need(len(payload) < 8 * 1024 * 1024, 'audit-output-cap')
        with output.open('xb') as stream:
            stream.write(payload)
    print(json.dumps({'status': report['status'], 'processingSeconds': report['processingSeconds'],
                      'caseCount': len(report['cases']), 'errors': report['errors'],
                      'reuseTotals': report.get('reuseTotals'), 'outputSha256': digest(payload)}))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    need(len(sys.argv) == 3, 'usage-root-audit-manifest-sha')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2]))
