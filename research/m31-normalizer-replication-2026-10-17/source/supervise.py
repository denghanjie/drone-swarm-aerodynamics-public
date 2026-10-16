"""Exclusive normalizer-replication stages. Prepublication validation is syntax only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

MIB = 1024 * 1024
WALL = 600
GUARDIAN_WALL = 610
RSS = 1073741824
KERNEL_BYTES = 192 * MIB
CHECKER_BYTES = 64 * MIB
METADATA_BYTES = 16 * MIB
TOTAL_BYTES = KERNEL_BYTES + CHECKER_BYTES + METADATA_BYTES
REPORT_BYTES = 65536
EXECUTION_CONTEXT = 'tool-require-escalated'
CONTEXT_EVIDENCE = 'Caller attestation via environment variable; tool invocation retained outside package. Not a sandbox detector.'
PS_COMMAND = ['/bin/ps', '-axo', 'pid=,ppid=,pgid=,rss=']
CUTOFF = '2026-10-17T01:00:00Z'
CUTOFF_EPOCH = datetime.fromisoformat(CUTOFF.replace('Z', '+00:00')).timestamp()
PACKAGE_NAME = 'research/m31-normalizer-replication-2026-10-17'
CONTROL_IDS = ['positive', 'distant-zero', 'raw-force', 'order-incompatible']
SCENE_IDS = [run + '-t' + str(t) for run in ['run-a', 'run-b'] for t in [0, 5, 10]]
ARMS = ['baseline', 'candidate']
LOADER_KEYS = ['LD_PRELOAD', 'LD_AUDIT', 'LD_LIBRARY_PATH', 'DYLD_INSERT_LIBRARIES', 'DYLD_LIBRARY_PATH',
               'DYLD_FRAMEWORK_PATH', 'DYLD_FALLBACK_LIBRARY_PATH', 'DYLD_FALLBACK_FRAMEWORK_PATH']
CLEARED_KEYS = ['NODE_OPTIONS', 'NODE_PATH', 'NODE_V8_COVERAGE', 'NODE_REDIRECT_WARNINGS', 'PYTHONPATH',
                'PYTHONHOME', 'PYTHONSTARTUP', 'PYTHONUSERBASE', 'PYTHONINSPECT'] + LOADER_KEYS


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise RuntimeError('Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(RuntimeError('Nonfinite JSON')))


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def dump(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    sync_directory(path.parent)


def pin(path, root):
    relative = path.relative_to(root)
    if path.resolve() != path or path.is_symlink() or not path.is_file() or '..' in relative.parts:
        raise RuntimeError('Noncanonical evidence file')
    data = path.read_bytes()
    return {'path': relative.as_posix(), 'bytes': len(data), 'sha256': sha(data)}


def launch_gate():
    if time.time() >= CUTOFF_EPOCH:
        raise RuntimeError('Scientific launch cutoff reached')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['kernel', 'checker'])
    stage = parser.parse_args().stage
    launch_gate()
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        raise RuntimeError('Supervisor requires Python -I -B')
    if os.environ.get('RESEARCH_EXECUTION_CONTEXT') != EXECUTION_CONTEXT:
        raise RuntimeError('Explicit escalated execution context required')
    if any(value for key, value in os.environ.items() if key in LOADER_KEYS or key.startswith('DYLD_')):
        raise RuntimeError('Loader injection environment refused')
    package = Path(__file__).resolve().parents[1]
    root = package.parents[1]
    if package.relative_to(root).as_posix() != PACKAGE_NAME:
        raise RuntimeError('Wrong package allocation')
    config_path = package / 'source/config.json'
    config_bytes = config_path.read_bytes()
    config = parse(config_bytes)
    expected_limits = {'kernelSeconds': WALL, 'checkerSeconds': WALL, 'guardianSeconds': GUARDIAN_WALL,
                       'rssBytes': RSS, 'kernelOutputBytes': KERNEL_BYTES, 'checkerOutputBytes': CHECKER_BYTES,
                       'metadataLogBytes': METADATA_BYTES, 'combinedOutputBytes': TOTAL_BYTES,
                       'workerSeconds': 60, 'sceneBytes': 32 * MIB, 'generationBytesPerRun': 8 * MIB,
                       'reportBytes': 2 * MIB, 'indexBytes': 2 * MIB, 'journalBytes': 4 * MIB}
    if (config.get('id') != 'm31-normalizer-replication-v1' or config.get('launchCutoffUtc') != CUTOFF
            or config.get('limits') != expected_limits or config.get('arms') != ARMS
            or config.get('scheduledTimes') != [0, 5, 10]
            or config.get('cases') != [{'id': 'run-a', 'seed': 26171021}, {'id': 'run-b', 'seed': 26171022}]
            or [c.get('id') for c in config.get('controls', [])] != CONTROL_IDS):
        raise RuntimeError('Frozen configuration mismatch')
    mp = package / 'source-manifest.json'
    mb = mp.read_bytes()
    manifest = parse(mb)
    entries = manifest.get('files')
    if not isinstance(entries, list) or not entries:
        raise RuntimeError('Source manifest files missing')
    names = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {'path', 'bytes', 'sha256'}:
            raise RuntimeError('Invalid source pin shape')
        name = entry['path']
        if (not isinstance(name, str) or name.startswith('/') or '\\' in name
                or any(p in ('', '.', '..') for p in name.split('/')) or name in names
                or type(entry['bytes']) is not int or entry['bytes'] < 0
                or not isinstance(entry['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', entry['sha256'])):
            raise RuntimeError('Invalid or duplicate source pin')
        names.add(name)
    required = {PACKAGE_NAME + '/' + name for name in ['PROTOCOL.md', 'runtime-pins.json', 'source/config.json',
                'source/run.cjs', 'source/check.py', 'source/supervise.py', 'source/guardian.py']}
    source_paths = {p.relative_to(root).as_posix() for p in (package / 'source').rglob('*') if p.is_file()}
    required.update(source_paths)
    if not required.issubset(names):
        raise RuntimeError('Required local source closure missing')
    pubpath = package / 'source-publication.json'
    pubbytes = pubpath.read_bytes()
    publication = parse(pubbytes)
    if (any(publication.get(k) is not True for k in ['remoteBytesEqualLocal', 'committedBytesEqualLocal'])
            or publication.get('manifestSha256') != sha(mb) or publication.get('manifestBytes') != len(mb)
            or publication.get('manifestPath') != mp.relative_to(root).as_posix()
            or publication.get('verifiedFilePins') != len(entries)
            or not re.fullmatch(r'[0-9a-f]{40}', publication.get('commit', ''))):
        raise RuntimeError('Exact public source receipt failed')
    verified = datetime.fromisoformat(publication['verifiedUtc'].replace('Z', '+00:00'))
    if verified.tzinfo is None or verified.timestamp() > time.time() or verified.timestamp() >= CUTOFF_EPOCH:
        raise RuntimeError('Publication receipt time invalid')
    env = os.environ.copy()
    for key in CLEARED_KEYS:
        env.pop(key, None)
    runtimes = parse((package / 'runtime-pins.json').read_bytes())
    if set(runtimes) != {'node', 'python'}:
        raise RuntimeError('Both active runtime pins are required')
    runtime_paths = {'node': Path(env['RESEARCH_NODE']).resolve(), 'python': Path(sys.executable).resolve()}
    env['RESEARCH_NODE'] = str(runtime_paths['node'])
    git_env = env.copy()
    git_env.update({'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'})
    prior_pins, prior_private_pins = [], []
    attempt_bytes = None
    authorization_bytes = None
    private = Path(env['RESEARCH_PRIVATE_RUN_DIR']).resolve()
    if private == root or root in private.parents:
        raise RuntimeError('Private raw logs must be outside repository')
    private.mkdir(parents=True, exist_ok=True)
    resultdir = package / 'results'
    resultdir.mkdir(exist_ok=True)
    sync_directory(package)
    if resultdir.resolve() != resultdir or resultdir.is_symlink() or private.is_symlink():
        raise RuntimeError('Noncanonical output directory')
    private_identity = sha(str(private).encode())
    def git(*args):
        return subprocess.run(['git', '-C', str(root), *args], env=git_env,
                              capture_output=True, check=True, timeout=15).stdout
    def identity_check():
        if mp.read_bytes() != mb or pubpath.read_bytes() != pubbytes:
            raise RuntimeError('Publication chain changed')
        if {p.relative_to(root).as_posix() for p in (package / 'source').rglob('*') if p.is_file()} != source_paths:
            raise RuntimeError('Local source closure changed')
        if attempt_bytes is not None and (resultdir / (stage + '-attempt.json')).read_bytes() != attempt_bytes:
            raise RuntimeError('Permanent attempt marker changed')
        if authorization_bytes is not None and (resultdir / (stage + '-authorization.json')).read_bytes() != authorization_bytes:
            raise RuntimeError('Launch authorization changed')
        if git('rev-parse', '--verify', 'HEAD').decode().strip() != publication['commit']:
            raise RuntimeError('HEAD differs from published source')
        if git('show', publication['commit'] + ':' + mp.relative_to(root).as_posix()) != mb:
            raise RuntimeError('Committed manifest mismatch')
        for entry in entries:
            if pin(root / entry['path'], root) != entry:
                raise RuntimeError('Local source pin mismatch')
            data = git('show', publication['commit'] + ':' + entry['path'])
            if len(data) != entry['bytes'] or sha(data) != entry['sha256']:
                raise RuntimeError('Committed source pin mismatch')
        for name, path in runtime_paths.items():
            data = path.read_bytes()
            if set(runtimes[name]) != {'bytes', 'sha256'} or len(data) != runtimes[name]['bytes'] or sha(data) != runtimes[name]['sha256']:
                raise RuntimeError('Runtime identity mismatch')
        for entry in prior_pins:
            if pin(root / entry['path'], root) != entry:
                raise RuntimeError('Prior-stage evidence changed')
        for entry in prior_private_pins:
            path = private / entry['name']
            if path.is_symlink() or not path.is_file():
                raise RuntimeError('Prior private log path changed')
            data = path.read_bytes()
            if len(data) != entry['bytes'] or sha(data) != entry['sha256']:
                raise RuntimeError('Prior private raw log changed')
    identity_check()
    inputs = {'inputs/' + name + '.json' for name in CONTROL_IDS + SCENE_IDS + ['lifetime-a', 'lifetime-b']}
    generations = {'generation/' + name + '.json' for name in ['run-a', 'run-b']}
    calls = {'calls/' + name + '-' + arm + '-r' + str(rep) + '.json'
             for name in CONTROL_IDS + SCENE_IDS for arm in ARMS for rep in (range(1) if name in CONTROL_IDS else range(4))}
    direct = {'direct/' + arm + '.json' for arm in ARMS}
    lifetime = {'lifetime/' + arm + '.json' for arm in ARMS}
    kernel_names = {'index.json', 'kernel-journal.jsonl'} | inputs | generations | calls | direct | lifetime
    references = {'reference/' + name + '.json' for name in CONTROL_IDS + SCENE_IDS + ['lifetime-a', 'lifetime-b']}
    checker_names = {'check.json'} | references
    report_names = {s + '-supervision.json' for s in ['kernel', 'checker']}
    metadata_names = {s + suffix for s in ['kernel', 'checker'] for suffix in
                      ['-attempt.json', '-authorization.json', '-failures.jsonl', '-guardian.jsonl', '-stdout.log', '-stderr.log', '-terminal-error.json']}
    allowed_names = kernel_names | checker_names | report_names | metadata_names
    allowed_dirs = {'inputs', 'generation', 'calls', 'direct', 'lifetime', 'reference'}
    raw_names = {s + '-' + stream + '.raw' for s in ['kernel', 'checker'] for stream in ['stdout', 'stderr']}
    def accounting():
        totals = {'aggregateBytes': 0, 'kernelBytes': 0, 'checkerBytes': 0, 'logMetadataBytes': 0, 'unclassifiedBytes': 0}
        files, violations = [], []
        try:
            for path in sorted(resultdir.rglob('*')):
                name = path.relative_to(resultdir).as_posix()
                if path.is_symlink():
                    violations.append('unexpected-output-file'); continue
                if path.is_dir():
                    if name not in allowed_dirs or (stage == 'kernel' and name == 'reference'):
                        violations.append('unexpected-output-directory')
                    continue
                if not path.is_file():
                    violations.append('unexpected-output-file'); continue
                size = path.stat().st_size
                totals['aggregateBytes'] += size
                files.append({'scope': 'results', 'path': name, 'bytes': size})
                if name not in allowed_names or (stage == 'kernel' and (name in checker_names or name.startswith('checker-'))):
                    totals['unclassifiedBytes'] += size; violations.append('unexpected-output-file'); continue
                totals['kernelBytes' if name in kernel_names else 'checkerBytes' if name in checker_names else 'logMetadataBytes'] += size
                cap = (2 * MIB if name in {'index.json', 'check.json'} else 4 * MIB if name == 'kernel-journal.jsonl'
                       else 8 * MIB if name in generations else REPORT_BYTES if name in report_names or name.endswith(('-authorization.json', '-failures.jsonl', '-guardian.jsonl'))
                       else 32 * MIB if name in kernel_names | checker_names else None)
                if cap is not None and size > cap:
                    violations.append('artifact-output-limit')
            for path in sorted(private.iterdir()):
                if path.is_symlink() or not path.is_file():
                    violations.append('unexpected-private-log'); continue
                size = path.stat().st_size
                totals['aggregateBytes'] += size; totals['logMetadataBytes'] += size
                files.append({'scope': 'private', 'path': path.name, 'bytes': size})
                if path.name not in raw_names or (stage == 'kernel' and path.name.startswith('checker-')):
                    violations.append('unexpected-private-log')
            for key, limit, reason in [('kernelBytes', KERNEL_BYTES, 'kernel-output-limit'),
                                       ('checkerBytes', CHECKER_BYTES, 'checker-output-limit'),
                                       ('logMetadataBytes', METADATA_BYTES, 'log-metadata-limit'),
                                       ('aggregateBytes', TOTAL_BYTES, 'output-limit')]:
                if totals[key] > limit:
                    violations.append(reason)
        except OSError:
            violations.append('output-accounting-failure')
        return {**totals, 'files': files, 'violations': sorted(set(violations))}
    def output_reason(reserve=0):
        result = accounting()
        if result['violations']:
            return result['violations'][0]
        if result['aggregateBytes'] + reserve > TOTAL_BYTES:
            return 'output-limit'
        if result['logMetadataBytes'] + reserve > METADATA_BYTES:
            return 'log-metadata-limit'
        return None
    reason = output_reason(REPORT_BYTES)
    if reason:
        raise RuntimeError(reason)
    if stage == 'checker':
        if (resultdir / 'kernel-terminal-error.json').exists():
            raise RuntimeError('Kernel finalization failed')
        prev = parse((resultdir / 'kernel-supervision.json').read_bytes())
        if (prev.get('stage') != 'kernel' or any(prev.get(k) is not True for k in
                ['success', 'closed', 'childGroupAbsent', 'scientificChildAbsentBeforeRelease', 'sourceAndRuntimeRechecked',
                 'guardianReadyObserved', 'normalRelease', 'guardianWaitStatusKnown', 'failureJournalDurable'])
                or prev.get('exitCode') != 0 or prev.get('guardianExitCode') != 0
                or prev.get('executionContext') != EXECUTION_CONTEXT or prev.get('firstFailure') is not None
                or prev.get('secondaryFailures') != [] or prev.get('terminationReason') is not None
                or prev.get('firstFailureDurable') is not None
                or prev.get('sourceCommit') != publication['commit'] or prev.get('sourceManifestSha256') != sha(mb)
                or prev.get('configSha256') != sha(config_bytes) or prev.get('privateLogDirectorySha256') != private_identity):
            raise RuntimeError('Kernel not closed and qualified for checker')
        if (prev.get('failureJournal') != pin(resultdir / 'kernel-failures.jsonl', root)
                or (resultdir / 'kernel-failures.jsonl').read_bytes() != b''
                or prev.get('authorizationEvidence') != pin(resultdir / 'kernel-authorization.json', root)
                or prev.get('authorization') != parse((resultdir / 'kernel-authorization.json').read_bytes())
                or len(prev.get('closureProbes', [])) != 2
                or any(p.get('absent') is not True for p in prev['closureProbes'])):
            raise RuntimeError('Kernel lifecycle evidence not qualified')
        present = {name for name in kernel_names if (resultdir / name).is_file() and not (resultdir / name).is_symlink()}
        expected_paths = {(resultdir / name).relative_to(root).as_posix() for name in present}
        evidence = prev.get('scientificEvidence')
        if (not {'index.json', 'kernel-journal.jsonl'}.issubset(present) or not isinstance(evidence, list)
                or len(evidence) != len(expected_paths) or {x.get('path') for x in evidence} != expected_paths):
            raise RuntimeError('Kernel evidence pin set incomplete')
        prior_pins.extend(evidence)
        lifecycle = ['kernel-supervision.json', 'kernel-attempt.json', 'kernel-authorization.json', 'kernel-failures.jsonl',
                     'kernel-guardian.jsonl', 'kernel-stdout.log', 'kernel-stderr.log']
        prior_pins.extend(pin(resultdir / name, root) for name in lifecycle)
        raw = prev.get('privateRawLogs')
        if not isinstance(raw, list) or len(raw) != 2 or {x.get('name') for x in raw} != {'kernel-stdout.raw', 'kernel-stderr.raw'}:
            raise RuntimeError('Kernel private raw log set incomplete')
        prior_private_pins.extend(raw)
    stage_names = (kernel_names if stage == 'kernel' else checker_names) | {stage + suffix for suffix in
                  ['-attempt.json', '-authorization.json', '-failures.jsonl', '-guardian.jsonl', '-stdout.log', '-stderr.log', '-supervision.json', '-terminal-error.json']}
    if any((resultdir / name).exists() for name in stage_names) or any((private / (stage + '-' + stream + '.raw')).exists() for stream in ['stdout', 'stderr']):
        raise RuntimeError('Exclusive stage already used or output preexists')
    if stage == 'kernel' and (any(resultdir.iterdir()) or any(private.iterdir())):
        raise RuntimeError('Kernel requires empty result and private directories')
    identity_check(); launch_gate()
    shared = {'stage': stage, 'sourceCommit': publication['commit'], 'sourceManifestSha256': sha(mb),
              'configSha256': sha(config_bytes), 'launchCutoffUtc': CUTOFF,
              'executionContext': EXECUTION_CONTEXT, 'executionContextEvidence': CONTEXT_EVIDENCE,
              'supervisorPid': os.getpid(), 'supervisorPgid': os.getpgrp()}
    dump(resultdir / (stage + '-attempt.json'), {**shared, 'allocation': 'sole attempt; existence prevents retry',
                                              'startedUtc': datetime.now(timezone.utc).isoformat()})
    attempt_bytes = (resultdir / (stage + '-attempt.json')).read_bytes()
    env.update({'RESEARCH_SUPERVISION_STAGE': stage, 'RESEARCH_SOURCE_COMMIT': publication['commit'],
                'RESEARCH_SOURCE_MANIFEST_PATH': str(mp), 'RESEARCH_EXPECTED_MANIFEST_SHA256': sha(mb),
                'RESEARCH_CONFIG_SHA256': sha(config_bytes)})
    command = ([str(runtime_paths['node']), str(package / 'source/run.cjs'), str(package)] if stage == 'kernel'
               else [str(runtime_paths['python']), '-I', '-B', str(package / 'source/check.py'), str(package)])
    template = ['NODE', 'PACKAGE/source/run.cjs', 'PACKAGE'] if stage == 'kernel' else ['PYTHON', '-I', '-B', 'PACKAGE/source/check.py', 'PACKAGE']
    events = resultdir / (stage + '-guardian.jsonl')
    authorization_path = resultdir / (stage + '-authorization.json')
    failure_path = resultdir / (stage + '-failures.jsonl')
    env.update({'RESEARCH_CHILD_COMMAND': json.dumps(command), 'RESEARCH_GUARD_EVENTS': str(events),
                'RESEARCH_GUARD_AUTHORIZATION': str(authorization_path)})
    stdout, stderr = [private / (stage + '-' + stream + '.raw') for stream in ['stdout', 'stderr']]
    output = resultdir / ('index.json' if stage == 'kernel' else 'check.json')
    report = {**shared, 'commandTemplate': template, 'runtimePins': runtimes,
              'runtimeIsolation': {'pythonIsolated': True, 'bytecodeDisabled': True, 'clearedChildEnvironmentKeys': CLEARED_KEYS},
              'wallLimitSeconds': WALL, 'guardianWallLimitSeconds': GUARDIAN_WALL, 'sampledRssLimitBytes': RSS,
              'kernelOutputLimitBytes': KERNEL_BYTES, 'checkerOutputLimitBytes': CHECKER_BYTES,
              'logMetadataLimitBytes': METADATA_BYTES, 'outputLimitBytes': TOTAL_BYTES, 'finalReportLimitBytes': REPORT_BYTES,
              'success': False, 'closed': False, 'samples': 0, 'peakSampledGroupRssBytes': 0,
              'maxSampleGapSeconds': 0, 'nominalSleepSeconds': 0.05, 'terminationReason': None,
              'containmentScope': 'Retained guardian group: kernel runner plus at most one sequential inherited-group worker; checker has no subprocesses. Sampled RSS is neither continuous peak nor hostile escape isolation.',
              'accountingScope': 'Closed new-package results only: kernel192MiB,checker64MiB,metadata and private/public logs16MiB,total272MiB. Records32MiB,generation8MiB,index/check2MiB,journal4MiB,supervision64KiB. Missing planned scientific files remain the checker responsibility and cannot support scientific success.'}
    report.update(firstFailure=None, secondaryFailures=[], failureJournalDurable=False, firstFailureDurable=None,
                  authorization=None, authorizationEvidence=None, guardianReadyObserved=False,
                  guardianEvents=[], closureProbes=[], cleanupActions=[], normalRelease=False,
                  guardianWaitStatusKnown=False, guardianExitCode=None, exitCode=None,
                  scientificChildAbsentBeforeRelease=False)
    started = time.monotonic(); last = started; guardian = None; child_pid = None; child_exit = None
    report['startedMonotonicNs'] = time.monotonic_ns()
    observed_worker_pids = set()
    failure_stream = None
    failure_bytes = b''

    def clean(value, limit=1024):
        value = str(value).replace(str(root), 'REPOSITORY_ROOT').replace(str(private), 'PRIVATE_RUN_DIR')
        for name, runtime in runtime_paths.items():
            value = value.replace(str(runtime), name.upper() + '_EXECUTABLE')
        value = value.replace(str(Path.home()), 'USER_HOME')
        value = re.sub(r'/private/var/folders/[^\s\"\']+', 'PRIVATE_TEMP_PATH', value)
        return value[:limit]

    def fail(kind, **details):
        nonlocal failure_bytes
        failure = {'kind': kind, 'monotonicNs': time.monotonic_ns(), **details}
        first = report['firstFailure'] is None
        if first:
            report['firstFailure'] = failure
            report['terminationReason'] = kind
        else:
            report['secondaryFailures'].append(failure)
        record = {'role': 'firstFailure' if first else 'secondaryFailure', 'failure': failure}
        encoded = (json.dumps(record, allow_nan=False) + '\n').encode()
        try:
            if failure_stream is None or len(failure_bytes) + len(encoded) > REPORT_BYTES:
                raise RuntimeError('failure-journal-unavailable-or-full')
            failure_stream.write(encoded); failure_stream.flush(); os.fsync(failure_stream.fileno())
            failure_bytes += encoded
            if first:
                report['firstFailureDurable'] = True
        except Exception as error:
            report['failureJournalDurable'] = False
            if first:
                report['firstFailureDurable'] = False
            report['secondaryFailures'].append({'kind': 'failure-persistence-error', 'monotonicNs': time.monotonic_ns(),
                                                'exception': type(error).__name__, 'message': clean(error)})

    class ProbeError(Exception):
        def __init__(self, kind, detail):
            self.kind, self.detail = kind, detail

    def sample():
        nonlocal last
        now = time.monotonic(); report['maxSampleGapSeconds'] = max(report['maxSampleGapSeconds'], now - last); last = now
        detail = {'operation': 'process-sample', 'command': PS_COMMAND, 'timeoutSeconds': 2, 'injected': False}
        try:
            process = subprocess.run(PS_COMMAND, capture_output=True, text=True, timeout=2)
        except Exception as error:
            raise ProbeError('sampler-exception', {**detail, 'exception': type(error).__name__, 'message': clean(error)})
        detail.update(returnCode=process.returncode, stderr=clean(process.stderr))
        if process.returncode != 0:
            raise ProbeError('sampler-nonzero', detail)
        rows = []
        for line in process.stdout.splitlines():
            if not line.strip():
                continue
            tokens = line.split()
            if len(tokens) != 4 or any(re.fullmatch(r'[0-9]+', token) is None for token in tokens):
                raise ProbeError('sampler-malformed', {**detail, 'exception': 'ValueError',
                                 'message': 'malformed-numeric-row', 'offendingRow': '[redacted numeric process row]'})
            try:
                rows.append(tuple(map(int, tokens)))
            except ValueError:
                raise ProbeError('sampler-malformed', {**detail, 'exception': 'ValueError',
                                 'message': 'invalid-numeric-row', 'offendingRow': '[redacted numeric process row]'})
        group = [row for row in rows if row[2] == guardian.pid]
        report['samples'] += 1
        rss = sum(row[3] * 1024 for row in group)
        report['peakSampledGroupRssBytes'] = max(report['peakSampledGroupRssBytes'], rss)
        if rss > RSS:
            raise RuntimeError('rss-limit')
        direct_children = [row for row in group if row[0] != guardian.pid and row[1] == guardian.pid]
        inferred_child = direct_children[0][0] if child_pid is None and len(direct_children) == 1 else child_pid
        workers = [row for row in group if row[0] not in {guardian.pid, inferred_child}]
        if (len(group) > (3 if stage == 'kernel' else 2) or len(direct_children) > 1
                or any(row[1] != inferred_child for row in workers) or (stage == 'checker' and workers)
                or any(row[0] == inferred_child and row[1] != guardian.pid for row in group)):
            raise RuntimeError('unexpected-descendant')
        observed_worker_pids.update(row[0] for row in workers)
        parents = {guardian.pid, inferred_child} | observed_worker_pids
        if any(row[1] in parents and row[2] != guardian.pid for row in rows):
            raise RuntimeError('escaped-descendant-observed')
        return group

    def read_events(final=False):
        if not events.exists():
            return []
        if events.is_symlink() or not events.is_file() or events.stat().st_size > REPORT_BYTES:
            raise RuntimeError('invalid-guardian-events')
        data = events.read_bytes()
        if data and not data.endswith(b'\n'):
            if final:
                raise RuntimeError('incomplete-guardian-event')
            data = data.rsplit(b'\n', 1)[0] + b'\n' if b'\n' in data else b''
        result = [parse(line) for line in data.splitlines()]
        last_ns = 0
        for event in result:
            if (not isinstance(event, dict) or type(event.get('monotonicNs')) is not int
                    or event['monotonicNs'] < last_ns or not isinstance(event.get('event'), str)):
                raise RuntimeError('invalid-guardian-event')
            last_ns = event['monotonicNs']
        return result

    def leader_row(rows):
        leaders = [row for row in rows if row[0] == guardian.pid]
        if len(leaders) != 1 or leaders[0][1] != os.getpid() or leaders[0][2] != guardian.pid or leaders[0][3] <= 0:
            raise RuntimeError('leader-sample-not-qualified')
        return leaders[0]

    known = {'wall-limit', 'rss-limit', 'output-limit', 'kernel-output-limit', 'checker-output-limit', 'log-metadata-limit',
             'artifact-output-limit', 'unexpected-output-file', 'unexpected-output-directory', 'unexpected-private-log',
             'output-accounting-failure', 'unexpected-descendant', 'escaped-descendant-observed', 'guardian-failure',
             'guardian-exited-before-release', 'residual-group-member', 'leader-sample-not-qualified',
             'invalid-guardian-events', 'invalid-guardian-event', 'incomplete-guardian-event', 'guardian-event-sequence'}
    try:
        failure_stream = failure_path.open('xb')
        failure_stream.flush(); os.fsync(failure_stream.fileno()); sync_directory(resultdir)
        report['failureJournalDurable'] = True
        with stdout.open('xb') as out, stderr.open('xb') as err:
            launch_gate()
            guardian = subprocess.Popen([str(runtime_paths['python']), '-I', '-B', str(package / 'source/guardian.py')],
                                        cwd=root, env=env, stdout=out, stderr=err, stdin=subprocess.PIPE,
                                        text=True, start_new_session=True)
            report['processGroup'] = guardian.pid
            while True:
                if time.monotonic() - started > WALL:
                    raise RuntimeError('wall-limit')
                reason = output_reason()
                if reason:
                    raise RuntimeError(reason)
                observed = read_events()
                if observed[:len(report['guardianEvents'])] != report['guardianEvents']:
                    raise RuntimeError('guardian-event-sequence')
                for event in observed[len(report['guardianEvents']):]:
                    name = event['event']
                    previous = [item['event'] for item in report['guardianEvents']]
                    if name == 'guardian-failure':
                        fail('guardian-failure', guardianDetail=event)
                        report['guardianEvents'].append(event)
                        break
                    expected = ['guardian-start', 'ready', 'child-start', 'child-exit', 'released']
                    if len(previous) >= len(expected) or name != expected[len(previous)]:
                        raise RuntimeError('guardian-event-sequence')
                    if name in {'guardian-start', 'ready'}:
                        if event.get('pid') != guardian.pid or event.get('pgid') != guardian.pid:
                            raise RuntimeError('guardian-event-sequence')
                        if name == 'ready': report['guardianReadyObserved'] = True
                    if name == 'child-start':
                        if (report['authorization'] is None or event.get('guardian') != guardian.pid
                                or event.get('authorizationMonotonicNs') != report['authorization']['monotonicNs']
                                or event['monotonicNs'] < report['authorization']['monotonicNs']
                                or type(event.get('pid')) is not int or event['pid'] <= 0):
                            raise RuntimeError('guardian-event-sequence')
                        child_pid = event['pid']
                    if name == 'child-exit':
                        if event.get('pid') != child_pid or type(event.get('exitCode')) is not int:
                            raise RuntimeError('guardian-event-sequence')
                        child_exit = event['exitCode']; report['exitCode'] = child_exit
                        if child_exit != 0:
                            fail('child-exit', exitCode=child_exit)
                    report['guardianEvents'].append(event)
                if any(event['event'] == 'guardian-failure' for event in report['guardianEvents']):
                    break
                if guardian.poll() is not None:
                    raise RuntimeError('guardian-exited-before-release')
                rows = sample()
                if report['guardianReadyObserved'] and report['authorization'] is None:
                    leader = leader_row(rows)
                    if len(rows) != 1:
                        raise RuntimeError('unexpected-descendant')
                    report['leaderObservation'] = {**dict(zip(['pid', 'ppid', 'pgid', 'rssKiB'], leader)),
                                                   'monotonicNs': time.monotonic_ns()}
                    launch_gate()
                    authorization = {**shared, 'guardianPid': guardian.pid, 'monotonicNs': time.monotonic_ns(),
                                     'leaderSampleObserved': True, 'leaderObservation': report['leaderObservation']}
                    dump(authorization_path, authorization)
                    authorization_bytes = authorization_path.read_bytes()
                    report['authorization'] = authorization
                    report['authorizationEvidence'] = pin(authorization_path, root)
                    guardian.stdin.write('start\n'); guardian.stdin.flush()
                if child_exit is not None:
                    leader_row(rows)
                    if len(rows) != 1:
                        raise RuntimeError('residual-group-member')
                    report['scientificChildAbsentBeforeRelease'] = True
                    report['releaseObservation'] = {'monotonicNs': time.monotonic_ns(), 'groupRows': [list(row) for row in rows]}
                    guardian.stdin.write('release\n'); guardian.stdin.flush(); guardian.wait(timeout=3)
                    report['normalRelease'] = guardian.returncode == 0
                    break
                time.sleep(0.05)
    except ProbeError as error:
        fail(error.kind, **error.detail)
    except Exception as error:
        fail(str(error) if str(error) in known else 'supervisor-' + type(error).__name__,
             exception=type(error).__name__, message=clean(error))
    finally:
        if guardian is not None:
            try:
                # Never signal an ID after observing that its retained owner has exited.
                if guardian.poll() is None:
                    try:
                        os.killpg(guardian.pid, signal.SIGTERM)
                        report['cleanupActions'].append({'signal': 'SIGTERM', 'monotonicNs': time.monotonic_ns()})
                    except ProcessLookupError:
                        pass
                    try: guardian.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        if guardian.poll() is None:
                            os.killpg(guardian.pid, signal.SIGKILL)
                            report['cleanupActions'].append({'signal': 'SIGKILL', 'monotonicNs': time.monotonic_ns()})
                        guardian.wait(timeout=2)
                report['guardianExitCode'] = guardian.poll()
                report['guardianWaitStatusKnown'] = report['guardianExitCode'] is not None
                if guardian.stdin is not None:
                    guardian.stdin.close()
            except Exception as error:
                fail('cleanup-error', exception=type(error).__name__, message=clean(error))
                report['guardianExitCode'] = guardian.returncode
                report['guardianWaitStatusKnown'] = guardian.returncode is not None
            for _ in range(2):
                probe = {'monotonicNs': time.monotonic_ns(), 'pgid': guardian.pid, 'absent': False}
                try:
                    try: os.killpg(guardian.pid, 0)
                    except ProcessLookupError: probe['absent'] = True
                except Exception as error:
                    probe['exception'] = type(error).__name__
                    fail('closure-probe-error', exception=type(error).__name__, message=clean(error))
                report['closureProbes'].append(probe)
                time.sleep(0.05)
            report['childGroupAbsent'] = all(probe['absent'] for probe in report['closureProbes'])
            report['closed'] = report['childGroupAbsent'] and report['guardianWaitStatusKnown']
            try:
                final_events = read_events(final=True)
                if final_events[:len(report['guardianEvents'])] != report['guardianEvents']:
                    raise RuntimeError('guardian-event-prefix-changed')
                for event in final_events[len(report['guardianEvents']):]:
                    if event['event'] == 'guardian-failure':
                        fail('guardian-failure', guardianDetail=event)
                report['guardianEvents'] = final_events
                report['guardianEventsEvidence'] = pin(events, root)
                if report['normalRelease'] and [event['event'] for event in report['guardianEvents']] != [
                        'guardian-start', 'ready', 'child-start', 'child-exit', 'released']:
                    fail('normal-release-evidence-missing')
                if report['normalRelease'] and final_events[-1]['monotonicNs'] < report['releaseObservation']['monotonicNs']:
                    fail('normal-release-chronology-invalid')
            except Exception as error:
                fail('final-guardian-events-error', exception=type(error).__name__, message=clean(error))
        else:
            report.update(childGroupAbsent=True, closed=True, noGroupCreated=True)
        if not report['closed']:
            fail('closure-unproven')
        report['observedSequentialWorkerPids'] = sorted(observed_worker_pids)
        logs = []
        try:
            for path in [stdout, stderr]:
                if not path.exists(): continue
                raw = path.read_bytes()
                text = clean(raw.decode('utf-8', errors='replace'), limit=len(raw) * 4 + 1024)
                dest = resultdir / (path.stem + '.log')
                with dest.open('x') as stream:
                    stream.write(text); stream.flush(); os.fsync(stream.fileno())
                sync_directory(resultdir)
                logs.append({'path': dest.relative_to(root).as_posix(), 'rawBytes': len(raw), 'rawSha256': sha(raw),
                             'publishedBytes': dest.stat().st_size, 'publishedSha256': sha(dest.read_bytes()),
                             'redaction': 'Machine/runtime prefixes replaced; raw bytes retained privately.'})
            report['privateRawLogs'] = [{'name': name, 'bytes': (private / name).stat().st_size,
                                        'sha256': sha((private / name).read_bytes())} for name in sorted(raw_names)
                                       if (private / name).is_file() and not (private / name).is_symlink()]
        except Exception as error:
            fail('log-finalization-error', exception=type(error).__name__, message=clean(error))
        report['logs'] = logs
        report['privateLogDirectorySha256'] = private_identity
        try:
            report['scientificEvidence'] = [pin(resultdir / name, root) for name in sorted(kernel_names)
                                            if (resultdir / name).is_file() and not (resultdir / name).is_symlink()]
            if stage == 'checker':
                report['checkerEvidence'] = [pin(resultdir / name, root) for name in sorted(checker_names)
                                             if (resultdir / name).is_file() and not (resultdir / name).is_symlink()]
            if output.is_file() and not output.is_symlink(): report['output'] = pin(output, root)
        except Exception as error:
            fail('evidence-pin-error', exception=type(error).__name__, message=clean(error))
        try:
            identity_check(); report['sourceAndRuntimeRechecked'] = True
        except Exception as error:
            report['sourceAndRuntimeRechecked'] = False
            fail('postrun-identity-failure', exception=type(error).__name__, message=clean(error))
        try:
            if not output.is_file() or output.is_symlink():
                fail('incomplete-stage-evidence', artifact=output.name)
            elif output.stat().st_size <= 2 * MIB:
                outcome = parse(output.read_bytes())
                if any(outcome.get(key) != shared[key] for key in ['sourceCommit', 'sourceManifestSha256', 'configSha256']):
                    fail('stage-report-provenance-mismatch')
                if stage == 'checker': report['scientificPassed'] = outcome.get('passed') is True
            if stage == 'kernel' and not (resultdir / 'kernel-journal.jsonl').is_file():
                fail('incomplete-stage-evidence', artifact='kernel-journal.jsonl')
        except Exception as error:
            fail('stage-evidence-read-error', exception=type(error).__name__, message=clean(error))
        report['wallSeconds'] = time.monotonic() - started
        if report['wallSeconds'] > WALL:
            fail('wall-limit')
        reason = output_reason(REPORT_BYTES)
        if reason:
            fail(reason)
        report['outputAccountingBeforeReport'] = accounting()
        recorded_kinds = {failure['kind'] for failure in ([report['firstFailure']] if report['firstFailure'] else []) + report['secondaryFailures']}
        for violation in report['outputAccountingBeforeReport']['violations']:
            if violation not in recorded_kinds:
                fail(violation)
        report['wallSeconds'] = time.monotonic() - started
        if report['wallSeconds'] > WALL and 'wall-limit' not in recorded_kinds:
            fail('wall-limit')
        try:
            if failure_path.is_symlink() or failure_path.read_bytes() != failure_bytes:
                raise RuntimeError('failure-journal-bytes-changed')
            report['failureJournal'] = pin(failure_path, root)
        except Exception as error:
            fail('failure-journal-identity-failure', exception=type(error).__name__, message=clean(error))
            report['failureJournalDurable'] = False
        report['outputAccountingBeforeReport'] = accounting()
        report['success'] = (report['exitCode'] == 0 and report['guardianExitCode'] == 0
                             and report['firstFailure'] is None and not report['secondaryFailures']
                             and report['closed'] and report['sourceAndRuntimeRechecked']
                             and report['guardianReadyObserved'] and report['authorization'] is not None
                             and report['normalRelease'] and report['scientificChildAbsentBeforeRelease']
                             and report['guardianWaitStatusKnown'] and report['failureJournalDurable']
                             and not report['outputAccountingBeforeReport']['violations'])
        if len((json.dumps(report, indent=2) + '\n').encode()) > REPORT_BYTES:
            fail('supervision-report-size-limit')
            raise RuntimeError('Final supervision report budget exceeded; first failure retained in journal')
        try:
            dump(resultdir / (stage + '-supervision.json'), report)
        except Exception as error:
            fail('supervision-report-write-error', exception=type(error).__name__, message=clean(error))
            raise
        finally:
            if failure_stream is not None:
                failure_stream.close()
        print(json.dumps({key: report[key] for key in ['stage', 'success', 'closed', 'wallSeconds', 'peakSampledGroupRssBytes', 'terminationReason']}))
    return 0 if report['success'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        fallback = {'success': False, 'closed': False, 'closureUnproven': True,
                    'terminationReason': 'supervisor-terminal-' + type(error).__name__,
                    'terminalFailure': {'exception': type(error).__name__}}
        try:
            if len(sys.argv) == 2 and sys.argv[1] in {'kernel', 'checker'}:
                directory = Path(__file__).resolve().parents[1] / 'results'
                journal = directory / (sys.argv[1] + '-failures.jsonl')
                if journal.is_file() and not journal.is_symlink() and journal.stat().st_size <= REPORT_BYTES:
                    records = [parse(line) for line in journal.read_bytes().splitlines()]
                    first = next((record['failure'] for record in records if record.get('role') == 'firstFailure'), None)
                    if first is not None:
                        fallback['firstFailure'] = first
                        fallback['terminationReason'] = first['kind']
                        fallback['durableFailureJournal'] = journal.name
                dump(directory / (sys.argv[1] + '-terminal-error.json'), fallback)
        except Exception:
            pass
        print(json.dumps(fallback)); sys.exit(1)
