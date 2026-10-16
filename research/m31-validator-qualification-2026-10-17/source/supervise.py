"""One exclusive exposed-corpus qualification. Source preparation permits syntax only."""
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

STAGE = 'qualification'
MIB = 1024 * 1024
WALL_LIMIT = 600
GUARDIAN_LIMIT = 610
RSS_LIMIT = 1073741824
SCIENCE_LIMIT = 64 * MIB
REFERENCE_LIMIT = 32 * MIB
QUALIFICATION_REPORT_LIMIT = 2 * MIB
METADATA_LIMIT = 16 * MIB
TOTAL_LIMIT = 80 * MIB
SUPERVISION_REPORT_LIMIT = 65536
CUTOFF = '2026-10-16T23:00:00Z'
CUTOFF_EPOCH = datetime.fromisoformat(CUTOFF.replace('Z', '+00:00')).timestamp()
PRIOR_PACKAGE = 'research/m31-moving-admission-2026-10-17'
PRIOR_SOURCE_COMMIT = '2a957d2b0bb26e731c8cd184bc13f51f673e9a0d'
PRIOR_RESULT_COMMIT = '5a5efeef2d216188fa93a8034c4573d7327c5411'
PRIOR_SOURCE_MANIFEST_SHA = '37a865330bbb86d0aef03dd3de775b830d7398abe69717b80c64860d4a8caa21'
PRIOR_RESULT_MANIFEST_SHA = 'e60a5bf356f9f27bf31f79fc3274c0c37675353f1b8b0de20a1a6fc1b69487d8'
REFERENCE_IDS = ['positive', 'distant-zero', 'raw-force', 'order-incompatible',
                 'run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10']
LOADER_KEYS = ['LD_PRELOAD', 'LD_AUDIT', 'LD_LIBRARY_PATH', 'DYLD_INSERT_LIBRARIES',
               'DYLD_LIBRARY_PATH', 'DYLD_FRAMEWORK_PATH', 'DYLD_FALLBACK_LIBRARY_PATH',
               'DYLD_FALLBACK_FRAMEWORK_PATH']
CLEARED_KEYS = ['NODE_OPTIONS', 'NODE_PATH', 'NODE_V8_COVERAGE', 'NODE_REDIRECT_WARNINGS',
                'PYTHONPATH', 'PYTHONHOME', 'PYTHONSTARTUP', 'PYTHONUSERBASE', 'PYTHONINSPECT'] + LOADER_KEYS


def sha(data):
    return hashlib.sha256(data).hexdigest()


def launch_gate():
    if time.time() >= CUTOFF_EPOCH:
        raise RuntimeError('Qualification launch cutoff reached')


def parse_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise RuntimeError('Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(RuntimeError('Raw nonfinite JSON')))


def sync_directory(directory):
    fd = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def dump(file, record):
    with file.open('x') as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    sync_directory(file.parent)


def pin(file, root):
    relative = file.relative_to(root)
    if file.resolve() != file or file.is_symlink() or not file.is_file() or '..' in relative.parts:
        raise RuntimeError('Noncanonical or nonfile evidence path')
    data = file.read_bytes()
    return {'path': relative.as_posix(), 'bytes': len(data), 'sha256': sha(data)}


def manifest_files(manifest):
    entries = manifest.get('files')
    if not isinstance(entries, list) or not entries:
        raise RuntimeError('Manifest files missing')
    names = set()
    for entry in entries:
        if set(entry) != {'path', 'bytes', 'sha256'}:
            raise RuntimeError('Invalid manifest pin shape')
        name = entry['path']
        if not isinstance(name, str) or name.startswith('/') or '\\' in name or any(p in ('', '.', '..') for p in name.split('/')):
            raise RuntimeError('Invalid manifest path')
        if name in names or type(entry['bytes']) is not int or entry['bytes'] < 0 or not re.fullmatch(r'[0-9a-f]{64}', entry['sha256']):
            raise RuntimeError('Invalid or duplicate manifest pin')
        names.add(name)
    return entries


def publication_gate(receipt, manifest_path, manifest_bytes, entries, root, expected_commit=None):
    commit = receipt.get('commit', '')
    if not re.fullmatch(r'[0-9a-f]{40}', commit) or (expected_commit and commit != expected_commit):
        raise RuntimeError('Publication commit mismatch')
    if any(receipt.get(key) is not True for key in ['remoteBytesEqualLocal', 'committedBytesEqualLocal']):
        raise RuntimeError('Exact public source verification absent')
    if (receipt.get('manifestSha256') != sha(manifest_bytes)
            or receipt.get('manifestBytes') != len(manifest_bytes)
            or receipt.get('manifestPath') != manifest_path.relative_to(root).as_posix()
            or receipt.get('verifiedFilePins') != len(entries)):
        raise RuntimeError('Publication manifest binding mismatch')
    verified = datetime.fromisoformat(receipt['verifiedUtc'].replace('Z', '+00:00'))
    if verified.tzinfo is None or verified.timestamp() > time.time() or verified.timestamp() >= CUTOFF_EPOCH:
        raise RuntimeError('Publication verification time invalid')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=[STAGE])
    parser.parse_args()
    launch_gate()
    if not sys.flags.isolated or not sys.dont_write_bytecode:
        raise RuntimeError('Supervisor requires Python -I -B')
    if any(value for key, value in os.environ.items() if key in LOADER_KEYS or key.startswith('DYLD_')):
        raise RuntimeError('Dynamic loader injection environment refused')
    package = Path(__file__).resolve().parents[1]
    root = package.parents[1]
    if package.relative_to(root).as_posix() != 'research/m31-validator-qualification-2026-10-17':
        raise RuntimeError('Wrong package allocation')
    config_path = package / 'source/config.json'
    config_bytes = config_path.read_bytes()
    config = parse_json(config_bytes)
    expected_limits = {'qualificationSeconds': WALL_LIMIT, 'guardianSeconds': GUARDIAN_LIMIT,
                       'rssBytes': RSS_LIMIT, 'scientificOutputBytes': SCIENCE_LIMIT,
                       'referenceBytes': REFERENCE_LIMIT, 'qualificationReportBytes': QUALIFICATION_REPORT_LIMIT,
                       'metadataLogBytes': METADATA_LIMIT, 'combinedOutputBytes': TOTAL_LIMIT}
    if (config.get('id') != 'm31-validator-qualification-v1' or config.get('launchCutoffUtc') != CUTOFF
            or config.get('limits') != expected_limits or config.get('referenceIds') != REFERENCE_IDS
            or config.get('negativeControlCount') != 21):
        raise RuntimeError('Frozen qualification configuration mismatch')
    prior = config['prior']
    expected_prior = {'package': PRIOR_PACKAGE, 'sourceCommit': PRIOR_SOURCE_COMMIT,
                      'resultCommit': PRIOR_RESULT_COMMIT, 'sourceManifestSha256': PRIOR_SOURCE_MANIFEST_SHA,
                      'resultManifestSha256': PRIOR_RESULT_MANIFEST_SHA}
    if any(prior.get(key) != value for key, value in expected_prior.items()):
        raise RuntimeError('Wrong exposed corpus allocation')
    prior_package = root / PRIOR_PACKAGE
    old_source_manifest_path = prior_package / 'source-manifest.json'
    old_result_manifest_path = prior_package / 'result-manifest.json'
    old_source_bytes = old_source_manifest_path.read_bytes()
    old_result_bytes = old_result_manifest_path.read_bytes()
    if sha(old_source_bytes) != PRIOR_SOURCE_MANIFEST_SHA or sha(old_result_bytes) != PRIOR_RESULT_MANIFEST_SHA:
        raise RuntimeError('Prior manifest pin mismatch')
    old_source_manifest = parse_json(old_source_bytes)
    old_result_manifest = parse_json(old_result_bytes)
    old_source_entries = manifest_files(old_source_manifest)
    old_result_entries = manifest_files(old_result_manifest)
    if len(old_source_entries) != 53 or len(old_result_entries) != 128 or old_result_manifest.get('originalSourceCommit') != PRIOR_SOURCE_COMMIT:
        raise RuntimeError('Prior source/result closure mismatch')
    prior_receipt_path = root / prior['resultPublicationReceipt']
    prior_receipt_bytes = prior_receipt_path.read_bytes()
    if sha(prior_receipt_bytes) != prior['resultPublicationReceiptSha256']:
        raise RuntimeError('Prior result publication receipt changed')
    prior_receipt = parse_json(prior_receipt_bytes)
    publication_gate(prior_receipt, old_result_manifest_path, old_result_bytes, old_result_entries, root, PRIOR_RESULT_COMMIT)
    mp = package / 'source-manifest.json'
    mb = mp.read_bytes()
    manifest = parse_json(mb)
    entries = manifest_files(manifest)
    pubpath = package / 'source-publication.json'
    pubbytes = pubpath.read_bytes()
    publication = parse_json(pubbytes)
    publication_gate(publication, mp, mb, entries, root)
    if datetime.fromisoformat(prior_receipt['verifiedUtc'].replace('Z', '+00:00')) > datetime.fromisoformat(publication['verifiedUtc'].replace('Z', '+00:00')):
        raise RuntimeError('New qualification publication predates exposed corpus receipt')
    if publication['commit'] in {PRIOR_SOURCE_COMMIT, PRIOR_RESULT_COMMIT}:
        raise RuntimeError('New source commit must differ from historical commits')
    required_local = ['PROTOCOL.md', 'runtime-pins.json', 'source/config.json', 'source/result-contract.json',
                      'source/qualify.py', 'source/supervise.py', 'source/guardian.py', 'review/SUPERVISOR-INTERFACE.md']
    required = {str((package / name).relative_to(root)) for name in required_local}
    required.update({str(old_source_manifest_path.relative_to(root)), str(old_result_manifest_path.relative_to(root)),
                     prior['resultPublicationReceipt']})
    required.update(PRIOR_PACKAGE + '/source/' + name for name in ['check.py', 'pair-reference.py', 'semantic-reference.py', 'config.json', 'spec.json'])
    if not required.issubset({entry['path'] for entry in entries}):
        raise RuntimeError('Required source/corpus gate pin missing')
    if any(entry['path'].startswith(str(package.relative_to(root)) + '/') for entry in old_result_entries + old_source_entries):
        raise RuntimeError('Historical manifests unexpectedly contain the new package')
    runtime_path = Path(sys.executable).resolve()
    runtime_pins = parse_json((package / 'runtime-pins.json').read_bytes())
    if set(runtime_pins) != {'python'}:
        raise RuntimeError('Qualification declares only its active Python runtime')
    env = os.environ.copy()
    for key in CLEARED_KEYS:
        env.pop(key, None)
    git_env = env.copy()
    git_env.update({'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_OPTIONAL_LOCKS': '0'})
    attempt_bytes = None
    def git(*args):
        return subprocess.run(['git', '-C', str(root), *args], env=git_env,
                              capture_output=True, check=True, timeout=15).stdout
    def committed_pin(entry, commit):
        current = pin(root / entry['path'], root)
        if current != entry:
            raise RuntimeError('Local frozen source/corpus pin mismatch')
        committed = git('show', commit + ':' + entry['path'])
        if len(committed) != entry['bytes'] or sha(committed) != entry['sha256']:
            raise RuntimeError('Committed frozen source/corpus pin mismatch')
    def identity_check():
        if mp.read_bytes() != mb or pubpath.read_bytes() != pubbytes or prior_receipt_path.read_bytes() != prior_receipt_bytes:
            raise RuntimeError('Publication chain changed')
        if attempt_bytes is not None and (package / 'results/qualification-attempt.json').read_bytes() != attempt_bytes:
            raise RuntimeError('Permanent qualification attempt changed')
        if git('rev-parse', '--verify', 'HEAD').decode().strip() != publication['commit']:
            raise RuntimeError('HEAD differs from published qualification source')
        for file, data, commit in [(mp, mb, publication['commit']),
                                   (old_source_manifest_path, old_source_bytes, PRIOR_SOURCE_COMMIT),
                                   (old_result_manifest_path, old_result_bytes, PRIOR_RESULT_COMMIT)]:
            committed_pin({'path': str(file.relative_to(root)), 'bytes': len(data), 'sha256': sha(data)}, commit)
        for entry in entries:
            committed_pin(entry, publication['commit'])
        for entry in old_source_entries:
            committed_pin(entry, PRIOR_SOURCE_COMMIT)
        for entry in old_result_entries:
            committed_pin(entry, PRIOR_RESULT_COMMIT)
        data = runtime_path.read_bytes()
        if len(data) != runtime_pins['python']['bytes'] or sha(data) != runtime_pins['python']['sha256']:
            raise RuntimeError('Python runtime pin mismatch')
        historical_bytes = (prior_package / 'results/check.json').read_bytes()
        historical = parse_json(historical_bytes)
        if (sha(historical_bytes) != prior['checkSha256'] or historical.get('passed') is not False
                or historical.get('advancement') is not False or historical.get('sourceCommit') != PRIOR_SOURCE_COMMIT):
            raise RuntimeError('Historical failed qualification changed')
        if sha((prior_package / 'source/check.py').read_bytes()) != prior['checkerSourceSha256']:
            raise RuntimeError('Historical checker source changed')
    identity_check()
    resultdir = package / 'results'
    resultdir.mkdir(exist_ok=True)
    sync_directory(package)
    if resultdir.is_symlink() or resultdir.resolve() != resultdir:
        raise RuntimeError('Noncanonical results directory')
    private = Path(env['RESEARCH_PRIVATE_RUN_DIR']).resolve()
    if private == root or root in private.parents:
        raise RuntimeError('Private logs must be outside the repository')
    private.mkdir(parents=True, exist_ok=True)
    if private.is_symlink() or private.resolve() != private:
        raise RuntimeError('Noncanonical private log directory')
    if any(resultdir.iterdir()) or any(private.iterdir()):
        raise RuntimeError('Exclusive qualification requires empty result and private-log directories')
    output = resultdir / 'qualification.json'
    scientific_names = {'qualification.json'} | {'reference/' + name + '.json' for name in REFERENCE_IDS}
    metadata_names = {STAGE + suffix for suffix in ['-attempt.json', '-guardian.jsonl', '-stdout.log', '-stderr.log', '-supervision.json', '-terminal-error.json']}
    allowed_names = scientific_names | metadata_names
    raw_names = {STAGE + '-' + stream + '.raw' for stream in ['stdout', 'stderr']}
    def account_output():
        totals = {'aggregateBytes': 0, 'scientificBytes': 0, 'logMetadataBytes': 0, 'unclassifiedBytes': 0}
        files, violations = [], []
        try:
            for file in sorted(resultdir.rglob('*')):
                name = file.relative_to(resultdir).as_posix()
                if file.is_symlink():
                    violations.append('unexpected-output-file'); continue
                if file.is_dir():
                    if name != 'reference': violations.append('unexpected-output-directory')
                    continue
                if not file.is_file():
                    violations.append('unexpected-output-file'); continue
                size = file.stat().st_size
                totals['aggregateBytes'] += size
                files.append({'scope': 'results', 'path': name, 'bytes': size})
                if name not in allowed_names:
                    totals['unclassifiedBytes'] += size; violations.append('unexpected-output-file'); continue
                totals['scientificBytes' if name in scientific_names else 'logMetadataBytes'] += size
                cap = QUALIFICATION_REPORT_LIMIT if name == 'qualification.json' else REFERENCE_LIMIT if name in scientific_names else SUPERVISION_REPORT_LIMIT if name == STAGE + '-supervision.json' else None
                if cap is not None and size > cap: violations.append('artifact-output-limit')
            for file in sorted(private.iterdir()):
                if file.is_symlink() or not file.is_file():
                    violations.append('unexpected-private-log'); continue
                size = file.stat().st_size
                totals['aggregateBytes'] += size; totals['logMetadataBytes'] += size
                files.append({'scope': 'private', 'path': file.name, 'bytes': size})
                if file.name not in raw_names: violations.append('unexpected-private-log')
            if totals['scientificBytes'] > SCIENCE_LIMIT: violations.append('scientific-output-limit')
            if totals['logMetadataBytes'] > METADATA_LIMIT: violations.append('log-metadata-limit')
            if totals['aggregateBytes'] > TOTAL_LIMIT: violations.append('output-limit')
        except OSError:
            violations.append('output-accounting-failure')
        return {**totals, 'files': files, 'violations': sorted(set(violations))}
    def output_reason(reserve=0):
        accounting = account_output()
        if accounting['violations']: return accounting['violations'][0]
        if accounting['aggregateBytes'] + reserve > TOTAL_LIMIT: return 'output-limit'
        if accounting['logMetadataBytes'] + reserve > METADATA_LIMIT: return 'log-metadata-limit'
        return None
    identity_check()
    launch_gate()
    shared = {'stage': STAGE, 'sourceCommit': publication['commit'], 'sourceManifestSha256': sha(mb),
              'configSha256': sha(config_bytes), 'priorSourceCommit': PRIOR_SOURCE_COMMIT,
              'priorResultCommit': PRIOR_RESULT_COMMIT, 'priorResultManifestSha256': PRIOR_RESULT_MANIFEST_SHA,
              'launchCutoffUtc': CUTOFF}
    dump(resultdir / (STAGE + '-attempt.json'), {**shared, 'allocation': 'sole attempt; existence prevents retry',
                                               'startedUtc': datetime.now(timezone.utc).isoformat()})
    attempt_bytes = (resultdir / (STAGE + '-attempt.json')).read_bytes()
    env.update({'RESEARCH_SUPERVISION_STAGE': STAGE, 'RESEARCH_SOURCE_MANIFEST_PATH': str(mp),
                'RESEARCH_EXPECTED_MANIFEST_SHA256': sha(mb), 'RESEARCH_SOURCE_COMMIT': publication['commit'],
                'RESEARCH_PRIOR_RESULT_MANIFEST_PATH': str(old_result_manifest_path),
                'RESEARCH_PRIOR_RESULT_MANIFEST_SHA256': PRIOR_RESULT_MANIFEST_SHA,
                'RESEARCH_PRIOR_SOURCE_COMMIT': PRIOR_SOURCE_COMMIT, 'RESEARCH_PRIOR_RESULT_COMMIT': PRIOR_RESULT_COMMIT})
    command = [str(runtime_path), '-I', '-B', str(package / 'source/qualify.py'), '--config', str(config_path),
               '--manifest', str(mp), '--output', str(output), '--root', str(root)]
    events = resultdir / (STAGE + '-guardian.jsonl')
    env['RESEARCH_CHILD_COMMAND'] = json.dumps(command)
    env['RESEARCH_GUARD_EVENTS'] = str(events)
    stdout, stderr = [private / (STAGE + '-' + stream + '.raw') for stream in ['stdout', 'stderr']]
    report = {**shared, 'commandTemplate': ['PYTHON', '-I', '-B', 'PACKAGE/source/qualify.py', '--config',
               'PACKAGE/source/config.json', '--manifest', 'PACKAGE/source-manifest.json', '--output',
               'PACKAGE/results/qualification.json', '--root', 'REPOSITORY_ROOT'],
              'runtimePins': runtime_pins, 'runtimeIsolation': {'pythonIsolated': True, 'bytecodeDisabled': True, 'clearedChildEnvironmentKeys': CLEARED_KEYS},
              'priorSourceManifestSha256': PRIOR_SOURCE_MANIFEST_SHA, 'priorSourceFileCount': len(old_source_entries),
              'priorResultFileCount': len(old_result_entries), 'historicalOriginalPassed': False,
              'historicalOriginalAdvancement': False, 'transferAuthorized': False,
              'wallLimitSeconds': WALL_LIMIT, 'guardianWallLimitSeconds': GUARDIAN_LIMIT,
              'sampledRssLimitBytes': RSS_LIMIT, 'scientificOutputLimitBytes': SCIENCE_LIMIT,
              'qualificationReportLimitBytes': QUALIFICATION_REPORT_LIMIT, 'referenceLimitBytes': REFERENCE_LIMIT,
              'logMetadataLimitBytes': METADATA_LIMIT, 'outputLimitBytes': TOTAL_LIMIT,
              'finalReportLimitBytes': SUPERVISION_REPORT_LIMIT, 'nominalSleepSeconds': 0.05,
              'success': False, 'closed': False, 'samples': 0, 'peakSampledGroupRssBytes': 0,
              'maxSampleGapSeconds': 0, 'terminationReason': None,
              'scope': 'Exposed-corpus validator qualification only. Historical failed gate remains false; no new trajectory, retroactive pass or transfer authorization.',
              'containmentScope': 'Reviewed child spawns no subprocesses; retained guardian owns its process group. Sampling is not continuous peak or hostile escape isolation.',
              'accountingScope': 'New results only: qualification.json and ten reference files share64MiB; report2MiB and each reference32MiB. Metadata plus public/private logs share16MiB; combined80MiB. Old corpus is read-only and rehashed before/after.'}
    started = time.monotonic(); last = started; guardian = None; child_exit = None; child_pid = None
    def sample():
        nonlocal last
        now = time.monotonic(); report['maxSampleGapSeconds'] = max(report['maxSampleGapSeconds'], now - last); last = now
        table = subprocess.run(['ps', '-axo', 'pid=,ppid=,pgid=,rss='], capture_output=True, text=True, check=True, timeout=2).stdout
        rows = [tuple(map(int, line.split())) for line in table.splitlines() if len(line.split()) == 4]
        group = [row for row in rows if row[2] == guardian.pid]
        rss = sum(row[3] * 1024 for row in group)
        report['samples'] += 1; report['peakSampledGroupRssBytes'] = max(report['peakSampledGroupRssBytes'], rss)
        if rss > RSS_LIMIT: raise RuntimeError('rss-limit')
        if len(group) > 2 or any(row[0] != guardian.pid and row[1] != guardian.pid for row in group): raise RuntimeError('unexpected-descendant')
        if any(row[1] in {guardian.pid, child_pid} and row[2] != guardian.pid for row in rows): raise RuntimeError('escaped-descendant-observed')
        return group
    known_reasons = {'wall-limit', 'rss-limit', 'output-limit', 'scientific-output-limit', 'log-metadata-limit',
                     'artifact-output-limit', 'unexpected-output-file', 'unexpected-output-directory',
                     'unexpected-private-log', 'output-accounting-failure', 'unexpected-descendant',
                     'escaped-descendant-observed', 'guardian-failure', 'guardian-exited-before-release', 'residual-group-member'}
    try:
        with stdout.open('xb') as out, stderr.open('xb') as err:
            launch_gate()
            guardian = subprocess.Popen([str(runtime_path), '-I', '-B', str(package / 'source/guardian.py')],
                                        cwd=root, env=env, stdout=out, stderr=err, stdin=subprocess.PIPE,
                                        text=True, start_new_session=True)
            report['processGroup'] = guardian.pid
            while True:
                if time.monotonic() - started > WALL_LIMIT: raise RuntimeError('wall-limit')
                reason = output_reason()
                if reason: raise RuntimeError(reason)
                if events.exists():
                    for line in events.read_text().splitlines():
                        try: event = parse_json(line)
                        except json.JSONDecodeError: continue
                        if event['event'] == 'child-start': child_pid = event['pid']
                        if event['event'] == 'child-exit': child_exit = event['exitCode']
                        if event['event'] == 'guardian-failure': raise RuntimeError('guardian-failure')
                rows = sample()
                if guardian.poll() is not None: raise RuntimeError('guardian-exited-before-release')
                if child_exit is not None:
                    if any(row[0] != guardian.pid for row in rows): raise RuntimeError('residual-group-member')
                    report['scientificChildAbsentBeforeRelease'] = True
                    guardian.stdin.write('release\n'); guardian.stdin.flush(); guardian.wait(timeout=3)
                    break
                time.sleep(0.05)
            report['exitCode'] = child_exit; report['guardianExitCode'] = guardian.returncode
    except Exception as error:
        report['terminationReason'] = str(error) if str(error) in known_reasons else 'supervisor-' + type(error).__name__
    finally:
        if guardian is not None:
            if guardian.poll() is None:
                try: os.killpg(guardian.pid, signal.SIGTERM)
                except ProcessLookupError: pass
                try: guardian.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    if guardian.poll() is None: os.killpg(guardian.pid, signal.SIGKILL)
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
        logs = []
        for file in [stdout, stderr]:
            if not file.exists(): continue
            data = file.read_bytes()
            text = data.decode('utf-8', errors='replace').replace(str(root), 'REPOSITORY_ROOT').replace(str(private), 'PRIVATE_RUN_DIR').replace(str(runtime_path), 'PYTHON_EXECUTABLE').replace(str(Path.home()), 'USER_HOME')
            text = re.sub(r'/private/var/folders/[^\s\"\']+', 'PRIVATE_TEMP_PATH', text)
            dest = resultdir / (file.stem + '.log')
            with dest.open('x') as stream:
                stream.write(text); stream.flush(); os.fsync(stream.fileno())
            sync_directory(resultdir)
            logs.append({'path': str(dest.relative_to(root)), 'rawBytes': len(data), 'rawSha256': sha(data),
                         'publishedBytes': dest.stat().st_size, 'publishedSha256': sha(dest.read_bytes()),
                         'redaction': 'Machine/runtime prefixes replaced; raw logs retained privately.'})
        report['logs'] = logs
        report['privateLogDirectorySha256'] = sha(str(private).encode())
        report['privateRawLogs'] = [{'name': name, 'bytes': (private / name).stat().st_size,
                                    'sha256': sha((private / name).read_bytes())} for name in sorted(raw_names)
                                   if (private / name).is_file() and not (private / name).is_symlink()]
        report['scientificEvidence'] = [pin(resultdir / name, root) for name in sorted(scientific_names)
                                        if (resultdir / name).is_file() and not (resultdir / name).is_symlink()]
        if output.exists(): report['output'] = pin(output, root)
        try:
            identity_check(); report['sourceAndRuntimeRechecked'] = True; report['priorCorpusRechecked'] = True
        except Exception:
            report['sourceAndRuntimeRechecked'] = False; report['priorCorpusRechecked'] = False
            report['terminationReason'] = 'postrun-identity-failure'
        report['outputAccountingBeforeReport'] = account_output()
        report['finalOutputBytesBeforeReport'] = report['outputAccountingBeforeReport']['aggregateBytes']
        reason = output_reason(SUPERVISION_REPORT_LIMIT)
        if reason: report['terminationReason'] = reason
        if not all((resultdir / name).is_file() and not (resultdir / name).is_symlink() for name in scientific_names):
            if report['terminationReason'] is None: report['terminationReason'] = 'incomplete-qualification-evidence'
        report['qualificationReportPassed'] = False
        if output.is_file() and not output.is_symlink() and output.stat().st_size <= QUALIFICATION_REPORT_LIMIT:
            outcome = parse_json(output.read_bytes())
            report['qualificationReportPassed'] = outcome.get('passed') is True and outcome.get('exposedCorpusQualificationPassed') is True
            provenance_fields = ['sourceCommit', 'sourceManifestSha256', 'configSha256', 'priorSourceCommit', 'priorResultCommit', 'priorResultManifestSha256']
            if any(outcome.get(key) != shared[key] for key in provenance_fields):
                report['terminationReason'] = 'qualification-report-provenance-mismatch'
            if any(outcome.get(key) is not False for key in ['historicalOriginalPassed', 'historicalOriginalAdvancement', 'transferAuthorized']):
                report['terminationReason'] = 'historical-failure-or-scope-relabelled'
        report['wallSeconds'] = time.monotonic() - started
        if report['wallSeconds'] > WALL_LIMIT: report['terminationReason'] = 'wall-limit'
        report['success'] = (report.get('exitCode') == 0 and report.get('guardianExitCode') == 0
                             and report['terminationReason'] is None and report['closed']
                             and report['qualificationReportPassed'] and report['sourceAndRuntimeRechecked'])
        if len((json.dumps(report, indent=2) + '\n').encode()) > SUPERVISION_REPORT_LIMIT:
            raise RuntimeError('Supervision report budget exceeded')
        dump(resultdir / (STAGE + '-supervision.json'), report)
        print(json.dumps({key: report[key] for key in ['stage', 'success', 'closed', 'wallSeconds', 'peakSampledGroupRssBytes', 'terminationReason']}))
    return 0 if report['success'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        fallback = {'success': False, 'closed': False, 'terminationReason': 'supervisor-terminal-' + type(error).__name__, 'closureUnproven': True}
        try:
            if len(sys.argv) == 2 and sys.argv[1] == STAGE:
                dump(Path(__file__).resolve().parents[1] / 'results' / (STAGE + '-terminal-error.json'), fallback)
        except Exception:
            pass
        print(json.dumps(fallback)); sys.exit(1)
