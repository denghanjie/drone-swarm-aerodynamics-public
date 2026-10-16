"""Independent saved-files-only checker for the inert launch qualification."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import sys
import time
from datetime import datetime, timezone

CASE_IDS = ['capability', 'normal', 'child-exit7', 'sampler-nonzero', 'sampler-malformed',
            'delayed-ready', 'child-timeout', 'early-guardian-exit']
CUTOFF = '2026-10-16T23:00:00Z'
CUTOFF_EPOCH = datetime.fromisoformat(CUTOFF.replace('Z', '+00:00')).timestamp()
TOTAL_LIMIT = 1048576
REPORT_LIMIT = 65536
EVENT_LIMIT = 32768


class CheckError(Exception):
    pass


def need(condition, code):
    if not condition:
        raise CheckError(code)


def deadline(_signum, _frame):
    raise CheckError('checker-deadline')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def parse(data):
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(CheckError('nonfinite-json')))


def raw(path, limit):
    need(path.is_file() and not path.is_symlink() and path.resolve() == path, 'noncanonical-or-missing-file')
    need(path.stat().st_size <= limit, 'file-budget')
    with path.open('rb') as stream:
        data = stream.read(limit + 1)
    need(len(data) <= limit, 'file-budget')
    return data


def load(path, limit=REPORT_LIMIT):
    return parse(raw(path, limit))


def file_pin(path, root, limit=REPORT_LIMIT):
    data = raw(path, limit)
    return {'path': path.relative_to(root).as_posix(), 'bytes': len(data), 'sha256': sha(data)}


def utc(value):
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    need(dt.tzinfo is not None, 'timezone-required')
    return dt.timestamp()


def dump(path, value):
    data = (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()
    need(len(data) <= REPORT_LIMIT, 'checker-report-budget')
    with path.open('xb') as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def tree_pins(results, root):
    answer = []
    for path in sorted(results.rglob('*')):
        need(not path.is_symlink(), 'result-symlink')
        if path.is_dir():
            continue
        need(path.is_file(), 'unexpected-result-object')
        limit = EVENT_LIMIT if path.suffix in {'.jsonl', '.log'} else REPORT_LIMIT
        answer.append(file_pin(path, root, limit))
    need(sum(row['bytes'] for row in answer) <= TOTAL_LIMIT, 'result-tree-budget')
    return answer


def source_gate(package, root):
    config = load(package / 'source/config.json')
    need(config.get('schema') == 'm31-launch-qualification-v1' and config.get('cases') == CASE_IDS, 'config-schedule')
    need(config.get('cutoffUtc') == CUTOFF and config.get('executionContext') == 'tool-require-escalated', 'config-context')
    need(config.get('limits') == {'runSeconds': 60, 'checkerSeconds': 15, 'guardianSeconds': 5, 'caseSeconds': 4,
          'rssBytes': 134217728, 'totalOutputBytes': TOTAL_LIMIT, 'reportBytes': REPORT_LIMIT, 'eventLogBytes': EVENT_LIMIT}, 'config-limits')
    runtime = raw(Path(sys.executable).resolve(), 256 * 1024 * 1024)
    need(config.get('runtime') == {'bytes': len(runtime), 'sha256': sha(runtime)}, 'runtime-pin')
    manifest_path = package / 'source-manifest.json'
    manifest_bytes = raw(manifest_path, 1024 * 1024)
    manifest = parse(manifest_bytes)
    receipt = load(package / 'source-publication.json')
    need(re.fullmatch('[0-9a-f]{40}', receipt.get('commit', '')) is not None, 'source-commit-shape')
    need(receipt.get('remoteBytesEqualLocal') is True and receipt.get('committedBytesEqualLocal') is True, 'publication-verification')
    entries = manifest.get('files')
    need(type(entries) is list and 1 <= len(entries) <= 128, 'source-entry-count')
    need(receipt.get('manifestPath') == manifest_path.relative_to(root).as_posix()
         and receipt.get('manifestSha256') == sha(manifest_bytes) and receipt.get('manifestBytes') == len(manifest_bytes)
         and receipt.get('verifiedFilePins') == len(entries), 'publication-manifest-binding')
    need(utc(receipt['verifiedUtc']) <= time.time() and utc(receipt['verifiedUtc']) < CUTOFF_EPOCH, 'publication-time')
    names = set()
    for entry in entries:
        need(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'source-pin-shape')
        name = entry['path']
        need(type(name) is str and name.startswith(package.relative_to(root).as_posix() + '/')
             and '\\' not in name and all(p not in {'', '.', '..'} for p in name.split('/')) and name not in names, 'source-path')
        need(type(entry['bytes']) is int and entry['bytes'] >= 0 and type(entry['sha256']) is str
             and re.fullmatch('[0-9a-f]{64}', entry['sha256']) is not None, 'source-pin-value')
        names.add(name)
        need(file_pin(root / name, root, 1024 * 1024) == entry, 'source-pin-mismatch')
    required = [package / 'PROTOCOL.md'] + [package / 'source' / name for name in ['config.json', 'run.py', 'guard.py', 'inert.py', 'check.py']]
    need(all(path.relative_to(root).as_posix() in names for path in required), 'source-required-closure')
    identity = {'sourceCommit': receipt['commit'], 'sourceManifestSha256': sha(manifest_bytes),
                'configSha256': sha(raw(package / 'source/config.json', REPORT_LIMIT)), 'executionContext': config['executionContext']}
    return config, identity, receipt, entries, file_pin(manifest_path, root, 1024 * 1024)


def numeric_row(row, expected_pid=None):
    need(type(row) is dict and set(row).issubset({'pid', 'ppid', 'pgid', 'rssKiB', 'monotonicNs'}) and all(type(row.get(k)) is int and row[k] >= 0 for k in ['pid', 'ppid', 'pgid', 'rssKiB']), 'numeric-process-observation')
    need(row['pid'] > 0 and row['pgid'] > 0 and row['rssKiB'] > 0, 'positive-process-observation')
    if expected_pid is not None:
        need(row['pid'] == row['pgid'] == expected_pid, 'leader-observation-identity')


def stamp(value):
    need(type(value) is int and value > 0, 'monotonic-stamp')
    return value


def check_case(case, folder, identity, config, expected_context_evidence):
    value = load(folder / 'report.json')
    need(value.get('case') == case, 'case-identity')
    for key in ['sourceCommit', 'sourceManifestSha256', 'configSha256', 'executionContext', 'supervisorPid', 'supervisorPgid']:
        need(value.get(key) == identity[key], 'case-provenance')
    need(value.get('runtime') == config['runtime'] and value.get('executionContextEvidence') == expected_context_evidence, 'case-runtime-context')
    need(type(value.get('wallSeconds')) in {float, int} and math.isfinite(value['wallSeconds']) and 0 <= value['wallSeconds'] <= 5, 'case-time-budget')
    need(value.get('closed') is True and type(value.get('samples')) is int and value['samples'] >= 0, 'case-closure-samples')
    need(type(value.get('peakSampledGroupRssBytes')) is int and 0 <= value['peakSampledGroupRssBytes'] <= config['limits']['rssBytes'], 'case-rss-budget')
    first = value.get('firstFailure')
    second = value.get('secondaryFailures')
    expected_first = {'capability': None, 'normal': None, 'delayed-ready': None,
        'child-exit7': 'child-exit', 'sampler-nonzero': 'sampler-nonzero',
        'sampler-malformed': 'sampler-malformed', 'child-timeout': 'child-timeout',
        'early-guardian-exit': 'guardian-exit-before-release'}[case]
    if expected_first is None:
        need(first is None and second == [], 'unexpected-case-failure')
    else:
        need(type(first) is dict and first.get('kind') == expected_first, 'expected-first-failure')
        need(second == [{'kind': 'missing-inert-output'}], 'secondary-missing-output-preserved')
    expected_files = {'report.json'}
    if case == 'capability':
        numeric_row(value.get('capabilityObservation'))
        need(value['peakSampledGroupRssBytes'] == value['capabilityObservation']['rssKiB'] * 1024, 'capability-rss-binding')
        need(value['capabilityObservation']['pid'] == identity['supervisorPid'] and value['capabilityObservation']['pgid'] == identity['supervisorPgid'], 'capability-supervisor-identity')
        need(value['samples'] == 1 and value.get('authorization') is None and value.get('events') == []
             and value.get('closureProbes') == [] and value.get('normalRelease') is False, 'capability-no-child')
        need(load(folder / 'inert-output.json') == {'case': case, 'capability': True}, 'capability-output')
        expected_files.add('inert-output.json')
    else:
        expected_files.update({'stdout.log', 'stderr.log', 'events.jsonl'})
        need(raw(folder / 'stdout.log', EVENT_LIMIT) == raw(folder / 'stderr.log', EVENT_LIMIT) == b'', 'unexpected-raw-log')
        event_bytes = raw(folder / 'events.jsonl', EVENT_LIMIT)
        need(event_bytes.endswith(b'\n'), 'event-final-newline')
        events = [parse(line) for line in event_bytes.splitlines()]
        need(events == value.get('events'), 'persisted-event-copy')
        times = [stamp(e.get('monotonicNs')) for e in events]
        need(all(a <= b for a, b in zip(times, times[1:])), 'event-time-order')
        kinds = [e.get('event') for e in events]
        for event in events:
            if event.get('event') == 'guardian-failure':
                need(event.get('exception') == 'RuntimeError' and event.get('message') == 'guardian-signalled', 'expected-cleanup-event')
        pid = value.get('guardianPid')
        need(type(pid) is int and pid > 0, 'guardian-pid')
        probes = value.get('closureProbes')
        need(type(probes) is list and len(probes) == 2 and all(p.get('absent') is True for p in probes), 'two-closure-probes')
        ptimes = [stamp(p.get('monotonicNs')) for p in probes]
        need(ptimes[0] <= ptimes[1] and (not times or times[-1] <= ptimes[0]), 'closure-probe-order')
        started = stamp(value.get('startedMonotonicNs'))
        need(not times or started <= times[0], 'case-start-event-order')
        need(kinds and kinds[0] == 'guardian-start' and events[0].get('pid') == events[0].get('pgid') == pid, 'guardian-start-identity')
        guardian_started = times[0]
        if case == 'early-guardian-exit':
            need(kinds == ['guardian-start', 'early-exit'] and first.get('exitCode') == value.get('guardianExitCode') == 5,
                 'early-guardian-exit-contract')
            need(value.get('authorization') is None and value.get('normalRelease') is False, 'early-exit-no-authorization')
        else:
            need(len(kinds) >= 2 and kinds[1] == 'ready' and events[1].get('pid') == events[1].get('pgid') == pid, 'ready-identity')
            need(value['samples'] > 0 and value['peakSampledGroupRssBytes'] > 0, 'actual-positive-samples')
            leader = value.get('leaderObservation')
            numeric_row(leader, pid)
            need(leader['ppid'] == identity['supervisorPid'] and value['peakSampledGroupRssBytes'] >= leader['rssKiB'] * 1024, 'leader-ownership-rss-binding')
            observed = stamp(leader.get('monotonicNs'))
            need(times[1] <= observed, 'ready-before-leader-observation')
            if case == 'delayed-ready':
                need(times[1] - guardian_started >= 200000000, 'delayed-ready-minimum')
            if case in {'sampler-nonzero', 'sampler-malformed'}:
                need(value.get('authorization') is None and value.get('normalRelease') is False
                     and kinds == ['guardian-start', 'ready', 'guardian-failure'], 'injected-failure-prevents-child')
                need(first.get('injected') is True and first.get('operation') == 'process-sample', 'injection-labeled')
                if case == 'sampler-nonzero':
                    need(first.get('returnCode') == 13 and first.get('stderr') == 'INJECTED process inspection failure', 'injected-nonzero-detail')
                else:
                    need(first.get('returnCode') == 0 and first.get('offendingRow') == 'INJECTED MALFORMED ROW'
                         and first.get('exception') == 'ValueError', 'injected-malformed-detail')
                need(type(value.get('guardianExitCode')) is int and value['guardianExitCode'] < 0, 'forced-guardian-exit')
            else:
                expected_files.add('authorization.json')
                auth = value.get('authorization')
                need(type(auth) is dict and load(folder / 'authorization.json') == auth, 'persisted-authorization')
                need(auth.get('guardianPid') == pid and auth.get('leaderSampleObserved') is True, 'start-authorization')
                authorized = stamp(auth.get('monotonicNs'))
                need(observed <= authorized and auth.get('leaderObservation') == leader, 'sample-before-authorization')
                need(len(events) >= 3 and kinds[2] == 'child-start' and events[2].get('guardian') == pid,
                     'authorized-child-start')
                child = events[2].get('pid')
                need(type(child) is int and child > 0 and child != pid and authorized <= times[2], 'authorization-before-child-start')
                if case == 'child-timeout':
                    need(kinds == ['guardian-start', 'ready', 'child-start', 'guardian-failure', 'cleanup-child-exit'] and first.get('deadlineSeconds') == 0.3
                         and value.get('normalRelease') is False, 'child-timeout-contract')
                    need(type(value.get('guardianExitCode')) is int and value['guardianExitCode'] < 0, 'timeout-forced-cleanup')
                    need(stamp(first.get('monotonicNs')) - authorized >= 300000000 and first['monotonicNs'] <= times[3], 'timeout-threshold')
                    need(events[4].get('pid') == child and type(events[4].get('exitCode')) is int and events[4]['exitCode'] < 0, 'timeout-child-actually-exited')
                else:
                    need(kinds == ['guardian-start', 'ready', 'child-start', 'child-exit', 'released'], 'normal-release-events')
                    expected_exit = 7 if case == 'child-exit7' else 0
                    need(events[3].get('pid') == child and events[3].get('exitCode') == expected_exit,
                         'child-exit-contract')
                    need(value.get('normalRelease') is True and value.get('guardianExitCode') == 0, 'normal-release-contract')
                    release = value.get('releaseObservation')
                    need(type(release) is dict and times[3] <= stamp(release.get('monotonicNs')) <= times[4], 'release-observation-order')
                    group = release.get('groupRows')
                    need(type(group) is list and len(group) == 1 and type(group[0]) is list and len(group[0]) == 4, 'release-leader-only')
                    numeric_row(dict(zip(['pid', 'ppid', 'pgid', 'rssKiB'], group[0])), pid)
                    need(group[0][1] == identity['supervisorPid'] and value['peakSampledGroupRssBytes'] >= group[0][3] * 1024, 'release-ownership-rss-binding')
                    if case == 'child-exit7':
                        need(first.get('exitCode') == 7, 'child-exit-primary-preserved')
        if case in {'normal', 'delayed-ready'}:
            expected_files.add('inert-output.json')
            need(load(folder / 'inert-output.json') == {'inert': True, 'case': case}, 'inert-output-contract')
        else:
            need(not (folder / 'inert-output.json').exists(), 'unexpected-inert-output')
    need({p.name for p in folder.iterdir()} == expected_files and all(p.is_file() and not p.is_symlink() for p in folder.iterdir()), 'case-file-set')
    return {'case': case, 'passed': True, 'expectedFirstFailure': expected_first,
            'secondaryMissingOutputExpected': expected_first is not None, 'closed': True,
            'normalRelease': value['normalRelease'], 'samples': value['samples'],
            'startedMonotonicNs': stamp(value.get('startedMonotonicNs')),
            'lastMonotonicNs': value['closureProbes'][-1]['monotonicNs'] if value['closureProbes'] else value['startedMonotonicNs']}


def main():
    start = time.monotonic()
    need(sys.flags.isolated and sys.dont_write_bytecode, 'isolated-runtime-required')
    need(len(sys.argv) == 2, 'package-argument-required')
    package = Path(sys.argv[1]).resolve()
    need(package == Path(__file__).resolve().parents[1]
         and package.name == 'm31-launch-qualification-2026-10-17', 'package-identity')
    root = package.parents[1]
    results = package / 'results'
    need(results.is_dir() and not results.is_symlink(), 'saved-results-required')
    need(not (results / 'check-attempt.json').exists() and not (results / 'check.json').exists(), 'checker-exclusive-attempt')
    need(time.time() < CUTOFF_EPOCH, 'checker-launch-cutoff')
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(15)
    report = {'schema': 'm31-launch-qualification-check-v1', 'passed': False, 'errors': [], 'cases': [],
              'scientificQualification': False, 'historicalRootCauseEstablished': False,
              'scientificRerunAuthorized': False, 'executionContextEvidenceScope': 'Saved caller attestation checked; external tool dispatch is not a sandbox detector.'}
    attempt_created = False
    try:
        config, identity, receipt, source_entries, manifest_pin = source_gate(package, root)
        need(os.environ.get('RESEARCH_EXECUTION_CONTEXT') == config['executionContext'], 'checker-execution-context')
        report.update(identity)
        source_receipt_pin = file_pin(package / 'source-publication.json', root)
        index = load(results / 'index.json')
        attempt = load(results / 'attempt.json')
        context_evidence = 'Caller attestation via environment variable; tool invocation retained outside package. Not a sandbox detector.'
        for key in ['supervisorPid', 'supervisorPgid']:
            need(type(attempt.get(key)) is int and attempt[key] > 0 and index.get(key) == attempt[key], 'supervisor-identity-binding')
            identity[key] = attempt[key]
        report.update(identity)
        for value in [index, attempt]:
            need(all(value.get(k) == identity[k] for k in ['sourceCommit', 'sourceManifestSha256', 'configSha256', 'executionContext']), 'run-source-binding')
            need(value.get('runtime') == config['runtime'] and value.get('executionContextEvidence') == context_evidence, 'run-runtime-context-binding')
        need(attempt.get('soleAttempt') is True and utc(receipt['verifiedUtc']) <= utc(attempt['startedUtc']) < CUTOFF_EPOCH
             and utc(attempt['startedUtc']) <= time.time(), 'run-attempt-chronology')
        dump(results / 'check-attempt.json', {**identity, 'runtime': config['runtime'], 'soleAttempt': True,
              'startedUtc': datetime.now(timezone.utc).isoformat(), 'checkerDeadlineSeconds': 15})
        attempt_created = True
        checker_attempt_pin = file_pin(results / 'check-attempt.json', root)
        initial_pins = tree_pins(results, root)
        need(index.get('cases') == CASE_IDS and index.get('fatalFailure') is None, 'all-eight-cases-required')
        need(type(index.get('wallSeconds')) in {int, float} and math.isfinite(index['wallSeconds']) and 0 <= index['wallSeconds'] <= 60, 'run-wall-budget')
        pinned = index.get('files')
        need(type(pinned) is list and len({p.get('path') for p in pinned}) == len(pinned), 'index-pin-set')
        expected_files = [row for row in initial_pins if row['path'] not in {
            (results / 'index.json').relative_to(root).as_posix(), (results / 'check-attempt.json').relative_to(root).as_posix()}]
        need(sorted(pinned, key=lambda x: x['path']) == expected_files, 'index-files-exact-closure')
        expected_reports = [file_pin(results / case / 'report.json', root) for case in CASE_IDS]
        need(index.get('reports') == expected_reports, 'index-case-report-pins')
        need({p.name for p in results.iterdir()} == set(CASE_IDS) | {'attempt.json', 'index.json', 'check-attempt.json'}, 'result-top-level-set')
        for case in CASE_IDS:
            report['cases'].append(check_case(case, results / case, identity, config, context_evidence))
        need(all(a['lastMonotonicNs'] <= b['startedMonotonicNs'] for a, b in zip(report['cases'], report['cases'][1:])), 'case-execution-order')
        need(tree_pins(results, root) == initial_pins, 'saved-evidence-changed-during-check')
        need(file_pin(results / 'check-attempt.json', root) == checker_attempt_pin, 'checker-attempt-changed')
        for entry in source_entries:
            need(file_pin(root / entry['path'], root, 1024 * 1024) == entry, 'source-changed-during-check')
        need(file_pin(package / 'source-manifest.json', root, 1024 * 1024) == manifest_pin
             and file_pin(package / 'source-publication.json', root) == source_receipt_pin, 'publication-changed-during-check')
        runtime = raw(Path(sys.executable).resolve(), 256 * 1024 * 1024)
        need({'bytes': len(runtime), 'sha256': sha(runtime)} == config['runtime'], 'runtime-changed-during-check')
        report['savedEvidencePins'] = initial_pins
        report['passed'] = len(report['cases']) == 8
    except Exception as error:
        report['errors'].append(str(error) if isinstance(error, CheckError) else 'checker-error:' + type(error).__name__)
        report['passed'] = False
    finally:
        report['wallSeconds'] = time.monotonic() - start
        if report['wallSeconds'] > 15:
            report['passed'] = False; report['errors'].append('checker-deadline')
        if not attempt_created:
            # A preflight failure also consumes the checker attempt; no second invocation.
            dump(results / 'check-attempt.json', {'soleAttempt': True, 'preflightFailed': True,
                  'startedUtc': datetime.now(timezone.utc).isoformat(), 'checkerDeadlineSeconds': 15})
        data_size = len((json.dumps(report, indent=2, allow_nan=False) + '\n').encode())
        need(sum(row['bytes'] for row in tree_pins(results, root)) + data_size <= TOTAL_LIMIT, 'final-result-tree-budget')
        dump(results / 'check.json', report)
        signal.alarm(0)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
