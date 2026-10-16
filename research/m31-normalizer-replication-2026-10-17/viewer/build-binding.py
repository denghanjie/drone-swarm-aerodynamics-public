"""Saved-data adapter only. Run after parent signals copy/binding; imports no research code."""
import argparse
import hashlib
import json
from pathlib import Path
import re

PACKAGE = 'research/m31-normalizer-replication-2026-10-17'
CONFIG = 'm31-normalizer-replication-v1'
PLAN = [{'id': run + '-t' + str(t), 'runId': run, 't': t} for run in ['run-a', 'run-b'] for t in [0, 5, 10]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root, output = args.root.resolve(strict=True), args.output.resolve(strict=True)
    package = root / PACKAGE
    results = package / 'results'
    if not results.is_dir() or results.is_symlink():
        raise RuntimeError('Saved results are required; no draft or synthetic binding is created')
    pins, data = [], {}

    def load(name, required=False):
        path = results / name
        if not path.exists():
            if required:
                raise RuntimeError('Required saved file missing: ' + name)
            return None
        if not path.is_file() or path.is_symlink() or path.resolve() != path:
            raise RuntimeError('Noncanonical result: ' + name)
        raw = path.read_bytes()
        if len(raw) > (8 * 1024 * 1024 if name.startswith('generation/') else 2 * 1024 * 1024):
            raise RuntimeError('Saved file exceeds viewer input cap')
        value = json.loads(raw)
        relative = path.relative_to(root).as_posix()
        pins.append({'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        data[relative] = value
        return relative

    paths = {'attempt': load('kernel-attempt.json', required=True),
             'kernelSupervision': load('kernel-supervision.json'),
             'checkerSupervision': load('checker-supervision.json'),
             'index': load('index.json'), 'check': load('check.json')}
    identity = data[paths['attempt']]
    required_identity = ['sourceCommit', 'sourceManifestSha256', 'configSha256']
    if not re.fullmatch(r'[0-9a-f]{40}', identity.get('sourceCommit', '')) or any(
            not re.fullmatch(r'[0-9a-f]{64}', identity.get(key, '')) for key in required_identity[1:]):
        raise RuntimeError('Attempt source identity unavailable')
    if identity.get('stage') != 'kernel' or identity.get('launchCutoffUtc') != '2026-10-17T01:00:00Z':
        raise RuntimeError('Wrong replication allocation')
    generations = {run: load('generation/' + run + '.json') for run in ['run-a', 'run-b']}
    for path, value in data.items():
        if any(value.get(key) != identity[key] for key in required_identity):
            raise RuntimeError('Saved identity differs: ' + path)
    index = data.get(paths['index'])
    if index is not None and (index.get('configId') != CONFIG or [
            {key: row.get(key) for key in ['id', 'runId', 't']} for row in index.get('scheduled', [])] != PLAN):
        raise RuntimeError('Saved index changed fixed six-state schedule')
    check = data.get(paths['check'])
    if check is not None and check.get('denominator') != 6:
        raise RuntimeError('Checker denominator is not six')
    for run, path in generations.items():
        if path is None:
            continue
        generation = data[path]
        if (generation.get('id') != run or generation.get('configId') != CONFIG
                or generation.get('seed') != {'run-a': 26171021, 'run-b': 26171022}[run]
                or generation.get('requested', {}).get('airflow') != 'off'
                or generation.get('requested', {}).get('count') != 64
                or not isinstance(generation.get('frames'), list)):
            raise RuntimeError('Wrong new pose source: ' + run)
    binding = {'schema': 'm31-normalizer-replication-view-v1', 'package': PACKAGE, 'configId': CONFIG,
               **{key: identity[key] for key in required_identity}, 'schedule': PLAN,
               'paths': paths, 'generationPaths': generations, 'pins': pins,
               'scope': 'Saved actual replication poses only; airflow off; posthoc queries; playback is not compute timing.',
               'fallback': 'Historical validator link only when no new saved pose frames exist; never implicit pose substitution.'}
    raw = (json.dumps(binding, indent=2, allow_nan=False) + '\n').encode()
    app_path = output / 'app.js'
    app = app_path.read_text()
    updated, count = re.subn(r"const BINDING_SHA='(?:__BINDING_SHA__|[0-9a-f]{64})';",
                            "const BINDING_SHA='" + hashlib.sha256(raw).hexdigest() + "';", app, count=1)
    if count != 1:
        raise RuntimeError('Viewer binding constant missing; no output changed')
    binding_path = output / 'binding.json'
    if binding_path.exists():
        raise RuntimeError('Binding already exists; preserve QA history before a separately approved rebuild')
    with binding_path.open('xb') as stream:
        stream.write(raw)
    app_path.write_text(updated)
    print(json.dumps({'bindingBytes': len(raw), 'bindingSha256': hashlib.sha256(raw).hexdigest(),
                      'savedFiles': len(pins), 'denominator': 6, 'scientificImports': 0, 'scientificExecution': False}))


if __name__ == '__main__':
    main()
