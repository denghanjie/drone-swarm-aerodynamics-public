"""Pure saved-state support: no producer or reference entry point."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
import sys
import time

PACKAGE = 'research/m31-native-tree-state1000-2026-10-17'
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MODULES = {
    'tree_check': ('research/m31-native-tree-design-2026-10-17/source/check.py', '1f40c7b3dc3f962eb623e5d7d2f848d03fc2decb0425e72733ba02722a76782b'),
    'stage_check': ('research/m31-coupled-stage-qualification-2026-10-17/source/check.py', '2e6553ef6a83e979930be0bac78004bea2ee214a54f08654b80625e4c534d9cb'),
    'native_check': ('research/m31-native-fresh-transfer-2026-10-17/source/check.py', '026e4ee8663f2d1dddac14b4e4d4fa2d3e5a551497b5e4878522a90cfc2a6a4c'),
    'coverage_check': ('research/m31-prepared-capacity-2026-10-17/review/saved_audit.py', '10aeea08e9964bf53ea9d804b11a8d719d90ee3f06e0637a55fa2f7206da008d'),
    'compact': ('research/m31-native-tree-browser-probe-2026-10-17/source/compact-check.py', '87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee'),
    'layout': ('research/m31-tree-witness-layout-2026-10-17/source/check.py', '9835d12054ad51cfdaa3530f3019d4745466b30c2bdf421e38701a0344aa716c'),
}
FIXED_PINS = {
    PACKAGE+'/source/layout.cjs': '310fce3d5f72abcdd1493cff487ae9c312027ec65f5e253fb0144dd50fb81c8e',
}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate-json-key')
        result[key] = value
    return result


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite-json')))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()


def path_at(root, relative):
    need(isinstance(relative, str) and relative and not Path(relative).is_absolute()
         and all(p not in ('', '.', '..') for p in relative.split('/')), 'relative-path')
    path = root / relative
    need(path.resolve() == path, 'symlink-path')
    return path


def read_pin(root, pin):
    need(set(pin) == {'path', 'bytes', 'sha256'} and type(pin['bytes']) is int
         and 0 <= pin['bytes'] <= MAX_FILE, 'pin-shape')
    path = path_at(root, pin['path'])
    need(path.stat().st_size == pin['bytes'], 'pin-size-before-read')
    raw = path.read_bytes()
    need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'pin-bytes')
    return raw


def load(path):
    need(path.stat().st_size <= MAX_FILE, 'input-file-cap')
    return decode(path.read_bytes())


def guard(ctx):
    now = time.monotonic_ns()
    active_deadline = ctx['childDeadline'] if ctx.get('closing') else ctx['computeDeadline']
    need(now < active_deadline <= ctx['childDeadline'] <= ctx['totalDeadline'], 'child-absolute-deadline')
    need(datetime.now(timezone.utc) < ctx['cutoff'], 'authorized-utc-cutoff')


def verify_sources(ctx):
    for pin in ctx['manifest']['files']:
        guard(ctx)
        read_pin(ctx['root'], pin)
    for pin in ctx.get('protectedPins', []):
        guard(ctx); read_pin(ctx['root'], pin)


def preflight(root, expected, commit, stage):
    """No scientific import precedes this independently enforced live-child gate."""
    package = root / PACKAGE
    manifest_raw = (package / 'source-manifest.json').read_bytes()
    need(len(manifest_raw) <= MAX_FILE and sha(manifest_raw) == expected, 'manifest-binding')
    manifest = decode(manifest_raw)
    pins = {p['path']: p for p in manifest['files']}
    need(len(pins) == len(manifest['files']), 'unique-manifest-pins')
    for relative in ('config.json', 'source/support.py', 'source/check.py', 'source/science-config.json'):
        need(PACKAGE + '/' + relative in pins, 'owned-source-closure')
    config = decode(read_pin(root, pins[PACKAGE + '/config.json']))
    need(config['schema'] == 'm31-native-tree-state1000-supervision-v1'
         and config['executionAllowed'] is True and isinstance(config['authorization'], dict), 'execution-not-authorized')
    authorization = config['authorization']
    need(set(authorization) == {'id', 'approvedUtc', 'reviewedSourceManifestSha256'}
         and authorization['id'] and len(authorization['reviewedSourceManifestSha256']) == 64,
         'authorization-receipt')
    cutoff = datetime.fromisoformat(config['launchCutoffUtc'])
    approved = datetime.fromisoformat(authorization['approvedUtc'])
    need(cutoff.tzinfo is not None and approved.tzinfo is not None
         and approved <= datetime.now(timezone.utc) < cutoff, 'authorization-time')
    limits = {'check':180}
    need(stage in limits and os.environ.get('RESEARCH_STAGE') == stage
         and os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated'
         and os.environ.get('RESEARCH_CHILD_BUDGET_MILLISECONDS') == str(limits[stage]*1000), 'supervised-stage')
    need(config['limits']['perFileBytes'] == MAX_FILE
         and config['limits']['combinedOutputLogScratchBytes'] == MAX_TOTAL
         and config['limits']['totalWallSeconds'] == 360
         and config['limits']['closureAndOverheadSeconds'] == 60
         and config['limits']['pollSeconds'] == 0.1
         and config['limits']['finalizationByteAllowance'] == 2*1024**2
         and config['stageOrder'] == ['browser','check']
         and config['preflight']['childWallSeconds'] == 15
         and {k:v['childWallSeconds'] for k,v in config['stages'].items()} == {'browser':120,'check':180},
         'fixed-supervision-envelope')
    token = os.environ.get('RESEARCH_RUN_TOKEN', '')
    need(len(token) == 64, 'supervised-token')
    attempt = load(package / 'results/run-attempt.json')
    need(attempt['schema'] == 'm31-native-tree-state1000-attempt-v1' and attempt['status'] == 'running'
         and attempt['stageOrder'] == ['browser','check']
         and set(attempt['stages']) == {'saved-validation','browser','check'}
         and attempt['sourceManifestSha256'] == expected and attempt['sourceCommit'] == commit
         and attempt['runTokenSha256'] == sha(token.encode())
         and attempt['stages'][stage]['status'] == 'started'
         and attempt['stages'][stage]['childWallLimitSeconds'] == limits[stage], 'supervised-live-attempt')
    private = Path(os.environ['RESEARCH_PRIVATE_LOG_DIR']).resolve()
    need(private.is_dir() and not private.is_relative_to(root)
         and attempt['privateDirectoryIdentitySha256'] == sha(str(private).encode()), 'private-directory-binding')
    ctx = {'root': root, 'package': package, 'expected': expected, 'commit': commit,
           'manifest': manifest, 'pins': pins, 'stage': stage, 'cutoff': cutoff,
           'childDeadline': int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS']),
           'totalDeadline': int(os.environ['RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS'])}
    ctx['computeDeadline'] = ctx['childDeadline'] - 15*1_000_000_000
    guard(ctx)
    verify_sources(ctx)
    for relative, expected_sha in list(FIXED_PINS.items()) + list(MODULES.values()):
        need(relative in pins and pins[relative]['sha256'] == expected_sha, 'immutable-dependency')
    science = decode(read_pin(root, pins[PACKAGE + '/source/science-config.json']))
    ctx['science'] = science
    receipt_raw = (package / 'source-publication.json').read_bytes()
    need(len(receipt_raw) <= MAX_FILE, 'publication-file-cap')
    receipt = decode(receipt_raw)
    need(receipt['commit'] == commit and receipt['manifestSha256'] == expected
         and receipt['manifestPath'] == PACKAGE+'/source-manifest.json'
         and receipt['manifestBytes'] == len(manifest_raw) and receipt['verifiedFilePins'] == len(manifest['files'])
         and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True
         and datetime.fromisoformat(receipt['verifiedUtc'].replace('Z','+00:00')) <=
             datetime.fromisoformat(attempt['startedUtc'].replace('Z','+00:00')),
         'published-source-binding')
    ctx['protectedPins'] = [
        {'path':PACKAGE+'/source-manifest.json','bytes':len(manifest_raw),'sha256':sha(manifest_raw)},
        {'path':PACKAGE+'/source-publication.json','bytes':len(receipt_raw),'sha256':sha(receipt_raw)}]
    runtime = manifest['runtime']['python']
    binary = Path(sys.executable).resolve().read_bytes()
    need(sys.platform == 'darwin' and sys.flags.isolated == 1 and sys.dont_write_bytecode
         and sys.version == runtime['version'] and len(binary) == runtime['bytes']
         and sha(binary) == runtime['sha256'], 'pinned-python-runtime')
    return ctx


def module(ctx, name):
    relative, expected = MODULES[name]
    need(ctx['pins'][relative]['sha256'] == expected, 'module-source-pin')
    read_pin(ctx['root'], ctx['pins'][relative])
    spec = importlib.util.spec_from_file_location('_coupled_' + name, ctx['root'] / relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def output_budget(ctx, extra=0):
    total = extra; evidence = private = other = 0
    for is_private,base in ((False,ctx['package']/'results'),(True,Path(os.environ['RESEARCH_PRIVATE_LOG_DIR']))):
        for path in base.rglob('*'):
            guard(ctx)
            if path.is_symlink():
                need(is_private,'output-symlink'); size = path.lstat().st_size
            else:
                if path.is_dir(): continue
                need(path.is_file(),'output-file-kind'); size = path.stat().st_size
            need(size <= MAX_FILE,'output-file-cap'); total += size
            if is_private: private += size
            elif path.relative_to(base).parts[0] in ('shards','records'): evidence += size
            elif path.name not in ('run-attempt.json','run-attempt.json.tmp'): other += size
    need(evidence <= 160*1024**2 and private <= 64*1024**2 and other+extra <= 30*1024**2,'output-partition-cap')
    need(total+2*1024**2 <= MAX_TOTAL,'output-total-cap')


def write(ctx, relative, value):
    guard(ctx)
    raw = canonical(value) + b'\n'
    need(len(raw) <= 2*1024**2, 'output-file-cap')
    output_budget(ctx, len(raw))
    path = path_at(ctx['root'], PACKAGE + '/results/' + relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    directory = os.open(path.parent,os.O_RDONLY)
    try: os.fsync(directory)
    finally: os.close(directory)
    return {'path': path.relative_to(ctx['root']).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def journal(ctx, index):
    descriptor = index['journal']
    need(set(descriptor) == {'path', 'bytes', 'sha256', 'records'}, 'journal-descriptor')
    pin = {k: descriptor[k] for k in ('path', 'bytes', 'sha256')}
    raw = read_pin(ctx['root'], pin)
    ctx['protectedPins'].append(pin)
    need(raw.endswith(b'\n'), 'journal-durable-final-newline')
    lines = raw.splitlines()
    need(len(lines) == descriptor['records'] <= 4096, 'journal-record-count')
    records = []
    for sequence, line in enumerate(lines):
        guard(ctx)
        row = decode(line)
        need(set(row) == {'sequence', 'kind', 'recordPin', 'serializationMilliseconds',
                          'transferMilliseconds', 'persistMilliseconds'} and row['sequence'] == sequence,
             'journal-contiguous-sequence')
        need(row['recordPin']['path'] == PACKAGE + '/results/records/%04d-%s.json' % (sequence, row['kind']),
             'journal-record-path')
        records.append(row)
    return records


def closed_browser(ctx):
    value = completed_output(ctx, 'browser')
    need(value['sourceCommit'] == ctx['commit'] and value['sourceManifestSha256'] == ctx['expected']
         and value['schema'] == 'm31-native-tree-state1000-browser-v1'
         and value['complete'] is True and value['errors'] == []
         and all(value[k] is True for k in ('runtimeIdentityVerified', 'inputsAndSourcesPreserved',
                                          'browserClosed', 'browserRootExitConfirmed', 'browserRootCloseConfirmed'))
         and value['allHelpersExitClaim'] is False and value['memoryLimitClaim'] is False,
         'browser-complete-binding')
    need(value['browserRoot']['error'] is None
         and all(value['browserRoot'][k]['code'] == 0 and value['browserRoot'][k]['signal'] is None
                 for k in ('exit', 'close')), 'browser-root-successful-close')
    attempt = load(ctx['package'] / 'results/run-attempt.json')
    need(attempt['stages']['browser']['status'] == 'completed', 'browser-stage-closed')
    return value, journal(ctx, value)


def completed_output(ctx, stage):
    attempt = load(ctx['package'] / 'results/run-attempt.json')
    record = attempt['stages'][stage]
    need(record['status'] == 'completed' and record['exitCode'] == 0, 'closed-output-stage')
    pin = dict(record['output'],path=PACKAGE+'/results/'+stage+'.json')
    value = decode(read_pin(ctx['root'],pin))
    ctx['protectedPins'].append(pin)
    return value


def public_error(error):
    value = str(error)
    code = value if value and len(value) <= 240 and all(c.isalnum() or c in '-_:.' for c in value) else 'stage-exception'
    return {'type': type(error).__name__, 'reason': code}


def fields(value, names, code):
    need(type(value) is dict and set(value) == set(names), code)


def integer(value, low, high, code):
    need(type(value) is int and low <= value <= high, code)
    return value


def local_module(ctx, filename):
    relative = PACKAGE + '/source/' + filename
    read_pin(ctx['root'], ctx['pins'][relative])
    spec = importlib.util.spec_from_file_location('_tree_probe_' + filename.replace('.', '_'), ctx['root'] / relative)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

