"""Exclusive normalizer-ablation stages. Prepublication validation is syntax only."""
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
CUTOFF = '2026-10-16T23:00:00Z'
CUTOFF_EPOCH = datetime.fromisoformat(CUTOFF.replace('Z', '+00:00')).timestamp()
PACKAGE_NAME = 'research/m31-normalizer-ablation-2026-10-17'
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
    if (config.get('id') != 'm31-normalizer-ablation-v1' or config.get('launchCutoffUtc') != CUTOFF
            or config.get('limits') != expected_limits or config.get('arms') != ARMS
            or config.get('scheduledTimes') != [0, 5, 10]
            or config.get('cases') != [{'id': 'run-a', 'seed': 26171011}, {'id': 'run-b', 'seed': 26171012}]
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
                      ['-attempt.json', '-guardian.jsonl', '-stdout.log', '-stderr.log', '-terminal-error.json']}
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
                       else 8 * MIB if name in generations else REPORT_BYTES if name in report_names
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
                ['success', 'closed', 'childGroupAbsent', 'scientificChildAbsentBeforeRelease', 'sourceAndRuntimeRechecked'])
                or prev.get('exitCode') != 0 or prev.get('guardianExitCode') != 0
                or prev.get('sourceCommit') != publication['commit'] or prev.get('sourceManifestSha256') != sha(mb)
                or prev.get('configSha256') != sha(config_bytes) or prev.get('privateLogDirectorySha256') != private_identity):
            raise RuntimeError('Kernel not closed and qualified for checker')
        present = {name for name in kernel_names if (resultdir / name).is_file() and not (resultdir / name).is_symlink()}
        expected_paths = {(resultdir / name).relative_to(root).as_posix() for name in present}
        evidence = prev.get('scientificEvidence')
        if (not {'index.json', 'kernel-journal.jsonl'}.issubset(present) or not isinstance(evidence, list)
                or len(evidence) != len(expected_paths) or {x.get('path') for x in evidence} != expected_paths):
            raise RuntimeError('Kernel evidence pin set incomplete')
        prior_pins.extend(evidence)
        lifecycle = ['kernel-supervision.json', 'kernel-attempt.json', 'kernel-guardian.jsonl', 'kernel-stdout.log', 'kernel-stderr.log']
        prior_pins.extend(pin(resultdir / name, root) for name in lifecycle)
        raw = prev.get('privateRawLogs')
        if not isinstance(raw, list) or len(raw) != 2 or {x.get('name') for x in raw} != {'kernel-stdout.raw', 'kernel-stderr.raw'}:
            raise RuntimeError('Kernel private raw log set incomplete')
        prior_private_pins.extend(raw)
    stage_names = (kernel_names if stage == 'kernel' else checker_names) | {stage + suffix for suffix in
                  ['-attempt.json', '-guardian.jsonl', '-stdout.log', '-stderr.log', '-supervision.json', '-terminal-error.json']}
    if any((resultdir / name).exists() for name in stage_names) or any((private / (stage + '-' + stream + '.raw')).exists() for stream in ['stdout', 'stderr']):
        raise RuntimeError('Exclusive stage already used or output preexists')
    if stage == 'kernel' and (any(resultdir.iterdir()) or any(private.iterdir())):
        raise RuntimeError('Kernel requires empty result and private directories')
    identity_check(); launch_gate()
    shared = {'stage': stage, 'sourceCommit': publication['commit'], 'sourceManifestSha256': sha(mb),
              'configSha256': sha(config_bytes), 'launchCutoffUtc': CUTOFF}
    dump(resultdir / (stage + '-attempt.json'), {**shared, 'allocation': 'sole attempt; existence prevents retry',
                                              'startedUtc': datetime.now(timezone.utc).isoformat()})
    attempt_bytes = (resultdir / (stage + '-attempt.json')).read_bytes()
    env.update({'RESEARCH_SUPERVISION_STAGE': stage, 'RESEARCH_SOURCE_COMMIT': publication['commit'],
                'RESEARCH_SOURCE_MANIFEST_PATH': str(mp), 'RESEARCH_EXPECTED_MANIFEST_SHA256': sha(mb)})
    command = ([str(runtime_paths['node']), str(package / 'source/run.cjs'), str(package)] if stage == 'kernel'
               else [str(runtime_paths['python']), '-I', '-B', str(package / 'source/check.py'), str(package)])
    template = ['NODE', 'PACKAGE/source/run.cjs', 'PACKAGE'] if stage == 'kernel' else ['PYTHON', '-I', '-B', 'PACKAGE/source/check.py', 'PACKAGE']
    events = resultdir / (stage + '-guardian.jsonl')
    env.update({'RESEARCH_CHILD_COMMAND': json.dumps(command), 'RESEARCH_GUARD_EVENTS': str(events)})
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
    started = time.monotonic(); last = started; guardian = None; child_pid = None; child_exit = None
    observed_worker_pids = set()
    def sample():
        nonlocal last
        now = time.monotonic(); report['maxSampleGapSeconds'] = max(report['maxSampleGapSeconds'], now - last); last = now
        table = subprocess.run(['ps', '-axo', 'pid=,ppid=,pgid=,rss='], capture_output=True, text=True, check=True, timeout=2).stdout
        rows = [tuple(map(int, line.split())) for line in table.splitlines() if len(line.split()) == 4]
        group = [row for row in rows if row[2] == guardian.pid]
        report['samples'] += 1
        rss = sum(row[3] * 1024 for row in group)
        report['peakSampledGroupRssBytes'] = max(report['peakSampledGroupRssBytes'], rss)
        if rss > RSS:
            raise RuntimeError('rss-limit')
        direct_children = [row for row in group if row[0] != guardian.pid and row[1] == guardian.pid]
        if child_pid is None and len(direct_children) == 1:
            inferred_child = direct_children[0][0]
        else:
            inferred_child = child_pid
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
    known = {'wall-limit', 'rss-limit', 'output-limit', 'kernel-output-limit', 'checker-output-limit', 'log-metadata-limit',
             'artifact-output-limit', 'unexpected-output-file', 'unexpected-output-directory', 'unexpected-private-log',
             'output-accounting-failure', 'unexpected-descendant', 'escaped-descendant-observed', 'guardian-failure',
             'guardian-exited-before-release', 'residual-group-member'}
    try:
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
                if events.exists():
                    for line in events.read_text().splitlines():
                        try:
                            event = parse(line)
                        except json.JSONDecodeError:
                            continue
                        if event['event'] == 'child-start': child_pid = event['pid']
                        if event['event'] == 'child-exit': child_exit = event['exitCode']
                        if event['event'] == 'guardian-failure': raise RuntimeError('guardian-failure')
                rows = sample()
                if guardian.poll() is not None:
                    raise RuntimeError('guardian-exited-before-release')
                if child_exit is not None:
                    if any(row[0] != guardian.pid for row in rows):
                        raise RuntimeError('residual-group-member')
                    report['scientificChildAbsentBeforeRelease'] = True
                    guardian.stdin.write('release\n'); guardian.stdin.flush(); guardian.wait(timeout=3)
                    break
                time.sleep(0.05)
            report['exitCode'] = child_exit; report['guardianExitCode'] = guardian.returncode
    except Exception as error:
        report['terminationReason'] = str(error) if str(error) in known else 'supervisor-' + type(error).__name__
    finally:
        if guardian is not None:
            # The retained owned leader anchors group identity; never signal an already-exited group ID.
            if guardian.poll() is None:
                try: os.killpg(guardian.pid, signal.SIGTERM)
                except ProcessLookupError: pass
                try: guardian.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    if guardian.poll() is None:
                        os.killpg(guardian.pid, signal.SIGKILL)
                    guardian.wait(timeout=2)
            absent = True
            for _ in range(2):
                try: os.killpg(guardian.pid, 0); absent = False
                except ProcessLookupError: pass
                time.sleep(0.05)
            report['childGroupAbsent'] = absent
        else:
            report['childGroupAbsent'] = True
        report['closed'] = report['childGroupAbsent']
        report['observedSequentialWorkerPids'] = sorted(observed_worker_pids)
        logs = []
        for path in [stdout, stderr]:
            if not path.exists(): continue
            raw = path.read_bytes()
            text = raw.decode('utf-8', errors='replace').replace(str(root), 'REPOSITORY_ROOT').replace(str(private), 'PRIVATE_RUN_DIR')
            for name, runtime in runtime_paths.items(): text = text.replace(str(runtime), name.upper() + '_EXECUTABLE')
            text = text.replace(str(Path.home()), 'USER_HOME')
            text = re.sub(r'/private/var/folders/[^\s\"\']+', 'PRIVATE_TEMP_PATH', text)
            dest = resultdir / (path.stem + '.log')
            with dest.open('x') as stream:
                stream.write(text); stream.flush(); os.fsync(stream.fileno())
            sync_directory(resultdir)
            logs.append({'path': dest.relative_to(root).as_posix(), 'rawBytes': len(raw), 'rawSha256': sha(raw),
                         'publishedBytes': dest.stat().st_size, 'publishedSha256': sha(dest.read_bytes()),
                         'redaction': 'Machine/runtime prefixes replaced; raw bytes retained privately.'})
        report['logs'] = logs
        report['privateLogDirectorySha256'] = private_identity
        report['privateRawLogs'] = [{'name': name, 'bytes': (private / name).stat().st_size,
                                    'sha256': sha((private / name).read_bytes())} for name in sorted(raw_names)
                                   if (private / name).is_file() and not (private / name).is_symlink()]
        report['scientificEvidence'] = [pin(resultdir / name, root) for name in sorted(kernel_names)
                                        if (resultdir / name).is_file() and not (resultdir / name).is_symlink()]
        if stage == 'checker':
            report['checkerEvidence'] = [pin(resultdir / name, root) for name in sorted(checker_names)
                                         if (resultdir / name).is_file() and not (resultdir / name).is_symlink()]
        if output.is_file() and not output.is_symlink(): report['output'] = pin(output, root)
        try:
            identity_check(); report['sourceAndRuntimeRechecked'] = True
        except Exception:
            report['sourceAndRuntimeRechecked'] = False; report['terminationReason'] = 'postrun-identity-failure'
        report['outputAccountingBeforeReport'] = accounting()
        reason = output_reason(REPORT_BYTES)
        if reason: report['terminationReason'] = reason
        if not output.is_file() or output.is_symlink():
            if report['terminationReason'] is None: report['terminationReason'] = 'incomplete-stage-evidence'
        elif output.stat().st_size <= 2 * MIB:
            outcome = parse(output.read_bytes())
            if any(outcome.get(key) != shared[key] for key in ['sourceCommit', 'sourceManifestSha256', 'configSha256']):
                report['terminationReason'] = 'stage-report-provenance-mismatch'
            if stage == 'checker': report['scientificPassed'] = outcome.get('passed') is True
        if stage == 'kernel' and not (resultdir / 'kernel-journal.jsonl').is_file():
            report['terminationReason'] = 'incomplete-stage-evidence'
        report['wallSeconds'] = time.monotonic() - started
        if report['wallSeconds'] > WALL: report['terminationReason'] = 'wall-limit'
        report['success'] = (report.get('exitCode') == 0 and report.get('guardianExitCode') == 0
                             and report['terminationReason'] is None and report['closed'] and report['sourceAndRuntimeRechecked'])
        if len((json.dumps(report, indent=2) + '\n').encode()) > REPORT_BYTES:
            raise RuntimeError('Final supervision report budget exceeded')
        dump(resultdir / (stage + '-supervision.json'), report)
        print(json.dumps({key: report[key] for key in ['stage', 'success', 'closed', 'wallSeconds', 'peakSampledGroupRssBytes', 'terminationReason']}))
    return 0 if report['success'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        fallback = {'success': False, 'closed': False, 'closureUnproven': True,
                    'terminationReason': 'supervisor-terminal-' + type(error).__name__}
        try:
            if len(sys.argv) == 2 and sys.argv[1] in {'kernel', 'checker'}:
                dump(Path(__file__).resolve().parents[1] / 'results' / (sys.argv[1] + '-terminal-error.json'), fallback)
        except Exception:
            pass
        print(json.dumps(fallback)); sys.exit(1)
