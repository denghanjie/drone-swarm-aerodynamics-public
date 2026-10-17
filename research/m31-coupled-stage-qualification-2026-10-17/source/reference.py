"""Prospective 32-stage prepared reference. Source-only until supervised authorization."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
import resource
import sys
import time

PACKAGE = 'research/m31-coupled-stage-qualification-2026-10-17'
FRESH = 'research/m31-native-fresh-transfer-2026-10-17'
TREE = 'research/m31-tree-first-reference-2026-10-17'
PREPARED = 'research/m31-prepared-reference-2026-10-17'
CAPACITY = 'research/m31-prepared-capacity-2026-10-17'
MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MODULES = {
    'pair': (FRESH + '/source/pair-reference.py', '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'),
    'semantic': (FRESH + '/source/semantic-reference.py', 'ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c'),
    'tree': (TREE + '/source/tree-reference.py', 'd08efc5e80910066d061a664aa7902c7ae7bab27dc710f5c00c9b2bf1671df65'),
    'prepared': (PREPARED + '/source/prepared-reference.py', '19efcb01f4c6d45b517b2388bcdaf045daf382bc11e7442dd8b9627e1807a921'),
    'native_check': (FRESH + '/source/check.py', '026e4ee8663f2d1dddac14b4e4d4fa2d3e5a551497b5e4878522a90cfc2a6a4c'),
    'coverage_check': (CAPACITY + '/review/saved_audit.py', '10aeea08e9964bf53ea9d804b11a8d719d90ee3f06e0637a55fa2f7206da008d'),
}
FIXED_PINS = {
    FRESH + '/source/spec.json': 'a47b9b920ddbbd14e1838e9c031a0b34dd1820f14959ef1295cef039e7f48d2f',
    FRESH + '/results/inputs/fresh-a-t5.json': '48dc63da80d4400a948a102143e872a49645b37b08eac73f932959653a16fa7c',
    FRESH + '/source/native-load.cjs': 'b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1',
    FRESH + '/source/vendor/generation/step02c-source/physics.cjs': '0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1',
    FRESH + '/source/vendor/generation/milestone-31-source/sim.cjs': '2b6fbc51334fd0669b23eb7173c6af83e62414a725b032796df5cb38ac7f1c9e',
    FRESH + '/source/vendor/generation/milestone-31-source/grid.cjs': 'f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302',
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


def preflight(root, expected, commit, stage):
    """No scientific import precedes this independently enforced live-child gate."""
    package = root / PACKAGE
    manifest_raw = (package / 'source-manifest.json').read_bytes()
    need(len(manifest_raw) <= MAX_FILE and sha(manifest_raw) == expected, 'manifest-binding')
    manifest = decode(manifest_raw)
    pins = {p['path']: p for p in manifest['files']}
    need(len(pins) == len(manifest['files']), 'unique-manifest-pins')
    for relative in ('config.json', 'source/reference.py', 'source/check.py', 'source/science-config.json'):
        need(PACKAGE + '/' + relative in pins, 'owned-source-closure')
    config = decode(read_pin(root, pins[PACKAGE + '/config.json']))
    need(config['schema'] == 'm31-coupled-stage-supervision-v1'
         and config['executionAllowed'] is True and isinstance(config['authorization'], dict), 'execution-not-authorized')
    authorization = config['authorization']
    need(set(authorization) == {'id', 'approvedUtc', 'reviewedSourceManifestSha256'}
         and authorization['id'] and len(authorization['reviewedSourceManifestSha256']) == 64,
         'authorization-receipt')
    cutoff = datetime.fromisoformat(config['launchCutoffUtc'])
    approved = datetime.fromisoformat(authorization['approvedUtc'])
    need(cutoff.tzinfo is not None and approved.tzinfo is not None
         and approved <= datetime.now(timezone.utc) < cutoff, 'authorization-time')
    need(os.environ.get('RESEARCH_STAGE') == stage, 'supervised-stage')
    token = os.environ.get('RESEARCH_RUN_TOKEN', '')
    need(len(token) == 64, 'supervised-token')
    attempt = load(package / 'results/run-attempt.json')
    need(attempt['schema'] == 'm31-coupled-stage-attempt-v1' and attempt['status'] == 'running'
         and attempt['sourceManifestSha256'] == expected and attempt['sourceCommit'] == commit
         and attempt['runTokenSha256'] == sha(token.encode())
         and attempt['stages'][stage]['status'] == 'started', 'supervised-live-attempt')
    ctx = {'root': root, 'package': package, 'expected': expected, 'commit': commit,
           'manifest': manifest, 'pins': pins, 'stage': stage, 'cutoff': cutoff,
           'childDeadline': int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS']),
           'totalDeadline': int(os.environ['RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS'])}
    ctx['computeDeadline'] = ctx['childDeadline'] - (30 if stage == 'reference' else 15)*1_000_000_000
    guard(ctx)
    verify_sources(ctx)
    for relative, expected_sha in list(FIXED_PINS.items()) + list(MODULES.values()):
        need(relative in pins and pins[relative]['sha256'] == expected_sha, 'immutable-dependency')
    science = decode(read_pin(root, pins[PACKAGE + '/source/science-config.json']))
    ctx['science'] = science
    receipt = load(package / 'source-publication.json')
    need(receipt['commit'] == commit and receipt['manifestSha256'] == expected
         and receipt['remoteBytesEqualLocal'] is True and receipt['committedBytesEqualLocal'] is True,
         'published-source-binding')
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
    total = extra
    roots = [ctx['package'] / 'results']
    if os.environ.get('RESEARCH_PRIVATE_LOG_DIR'):
        roots.append(Path(os.environ['RESEARCH_PRIVATE_LOG_DIR']))
    for root_index, base in enumerate(roots):
        if base.exists():
            for path in base.rglob('*'):
                need(root_index != 0 or not path.is_symlink(), 'output-symlink')
                if path.is_symlink() or not path.is_dir():
                    size = path.lstat().st_size
                    need(size <= MAX_FILE, 'output-file-cap')
                    total += size
    need(total + 2*1024*1024 <= MAX_TOTAL, 'output-total-cap')


def write(ctx, relative, value):
    guard(ctx)
    raw = canonical(value) + b'\n'
    need(len(raw) <= MAX_FILE, 'output-file-cap')
    output_budget(ctx, len(raw))
    path = path_at(ctx['root'], PACKAGE + '/results/' + relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    return {'path': path.relative_to(ctx['root']).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def journal(ctx, index):
    descriptor = index['journal']
    need(set(descriptor) == {'path', 'bytes', 'sha256', 'records'}, 'journal-descriptor')
    raw = read_pin(ctx['root'], {k: descriptor[k] for k in ('path', 'bytes', 'sha256')})
    need(raw.endswith(b'\n'), 'journal-durable-final-newline')
    lines = raw.splitlines()
    need(len(lines) == descriptor['records'] <= 4096, 'journal-record-count')
    records = []
    for sequence, line in enumerate(lines):
        guard(ctx)
        row = decode(line)
        need(set(row) == {'sequence', 'kind', 'body'} and row['sequence'] == sequence,
             'journal-contiguous-sequence')
        records.append(row)
    return records


def closed_browser(ctx):
    value = load(ctx['package'] / 'results/browser.json')
    need(value['sourceCommit'] == ctx['commit'] and value['sourceManifestSha256'] == ctx['expected']
         and value['complete'] is True, 'browser-complete-binding')
    attempt = load(ctx['package'] / 'results/run-attempt.json')
    need(attempt['stages']['browser']['status'] == 'completed', 'browser-stage-closed')
    return value, journal(ctx, value)


def input_sidecar(ctx, browser, stage):
    pin = browser['inputs'][stage['stageId']]
    need(pin['path'] == PACKAGE + '/results/inputs/' + stage['stageId'] + '.json', 'stage-input-sidecar-path')
    raw = read_pin(ctx['root'], pin)
    need(raw == canonical(stage['nativeInput']), 'stage-input-sidecar-exact-bytes')
    native = stage['native']
    need(native['semanticInputSha256'] == native['inlineInputCanonicalSha256'] == pin['sha256']
         and 'inputFileSha256' not in native, 'inline-semantic-and-actual-file-binding')
    return pin


def public_error(error):
    value = str(error)
    code = value if value and len(value) <= 240 and all(c.isalnum() or c in '-_:.' for c in value) else 'stage-exception'
    return {'type': type(error).__name__, 'reason': code}


class RawWords:
    def __init__(self, helper):
        self.helper = helper

    def literal(self, word):
        return self.helper.parse_bits(word)

    def __getattr__(self, name):
        return getattr(self.helper, name)


def main(root, expected, commit):
    ctx = preflight(root, expected, commit, 'reference')
    result = {'schema': 'm31-coupled-stage-reference-index-v1', 'sourceCommit': commit,
              'sourceManifestSha256': expected, 'complete': False, 'passed': False, 'qualified': False,
              'attempted': 0, 'completed': 0, 'constants': None, 'journal': None,
              'suffixCalls': 0, 'logicalPairs': 0, 'errors': []}
    entries = []
    journal_path = ctx['package'] / 'results/reference.jsonl'
    code = 1
    try:
        browser, records = closed_browser(ctx)
        stages = [row['body'] for row in records if row['kind'] == 'stage' and row['body']['arm'] == 'coupled']
        need(len(stages) == 32 and [s['stageId'] for s in stages]
             == ['coupled-step%d-k%d' % (step, k) for step in range(8) for k in range(1, 5)], '32-ordered-primary-stages')
        need(set(browser['inputs']) == {stage['stageId'] for stage in stages}, 'exact-32-input-sidecars')
        pair, semantic, tree, prepared = [module(ctx, name) for name in ('pair', 'semantic', 'tree', 'prepared')]
        spec = decode(read_pin(root, ctx['pins'][FRESH + '/source/spec.json']))
        need(spec['maxDrones'] == 180 and spec['positiveTermCap'] == 2000000
             and spec['referenceCoefficientBits'] == spec['referenceSourceBits'] == 192
             and spec['referenceRootBisections'] == 128, 'unchanged-reference-recipe')
        bits, _trace = pair.constants_from_graph(spec)
        result['constants'] = {key: pair.hex_bits(value) for key, value in bits.items()}
        with journal_path.open('xb') as stream:
            for stage in stages:
                guard(ctx)
                raw = stage['nativeInput']
                input_pin = input_sidecar(ctx, browser, stage)
                need(len(raw['drones']) == 64, 'fixed-n64')
                need(stage['status'] == 'completed' and raw == {'drones': [
                    {'id': row['id'], 'state': row['stateWords']} for row in stage['records']]}, 'saved-consumed-input-binding')
                scene = {'id': stage['stageId'], 'family': 'coupled-projected-stage',
                         'expectedClass': 'unconstrained', 'drones': raw['drones']}
                result['attempted'] += 1
                budget = {'oracleCalls': 0, 'limit': 30000}
                target, counters, controls = prepared.regenerate_scene(
                    scene, spec, bits, RawWords(pair), semantic, tree,
                    guard=lambda: guard(ctx), budget=budget, run_controls=False)
                record = tree.to_record(target, semantic)
                record.update(sourceCommit=commit, sourceManifestSha256=expected,
                              inputSha256=sha(canonical(raw)), inputFile=input_pin, reuseCounters=counters)
                pin = write(ctx, 'reference/' + stage['stageId'] + '.json', record)
                entry = {'sequence': len(entries), 'kind': 'reference', 'body': {
                    'stageId': stage['stageId'], 'reference': pin,
                    'inputSha256': record['inputSha256'], 'status': target['status'],
                    'branch': target['branch'], 'reuseCounters': counters}}
                encoded = canonical(entry) + b'\n'
                output_budget(ctx, len(encoded))
                stream.write(encoded); stream.flush(); os.fsync(stream.fileno())
                entries.append(entry)
                result['suffixCalls'] += counters['oracleCalls']
                result['logicalPairs'] += target['planned']
                need(not controls and counters['oracleCalls'] == budget['oracleCalls'] <= 16128
                     and counters['prepareOneCalls'] == counters['preparationValidCalls'] == 64
                     and counters['operandLookups'] == 2 * counters['oracleCalls']
                     and counters['pairPreparations'] == 0, 'prepared-count-contract')
                need(target['status'] == 'admitted' and target['branch'] == 'loads', 'first-stage-reference-refusal')
                result['completed'] += 1
                del target, record
        need(result['attempted'] == result['completed'] == 32
             and result['logicalPairs'] == 516096 and result['suffixCalls'] <= 516096, 'reference-final-counts')
        result['complete'] = result['passed'] = result['qualified'] = True
        code = 0
    except Exception as error:
        result['errors'].append(public_error(error))
    finally:
        ctx['closing'] = True
        result['processLifetimePeakRssBytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['peakRssScope'] = 'macOS process lifetime only; not isolated stage or browser/process-tree aggregate, and not an OS memory limit.'
        if journal_path.exists():
            raw = journal_path.read_bytes()
            result['journal'] = {'path': journal_path.relative_to(root).as_posix(),
                                 'bytes': len(raw), 'sha256': sha(raw), 'records': len(entries)}
        try:
            verify_sources(ctx)
            result['sourcesPreserved'] = True
        except Exception as error:
            result['sourcesPreserved'] = result['passed'] = result['qualified'] = False
            result['errors'].append({'type': type(error).__name__, 'reason': 'source-preservation'})
            code = 1
        write(ctx, 'reference.json', result)
    return code


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: reference.py ROOT MANIFEST_SHA COMMIT')
    raise SystemExit(main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]))
