"""Display-only saved-data adapter. Do not run until the parent accepts analysis/check.

Imports only the standard library. No simulator, analyzer, checker, reference,
approximation or solver is imported/executed. Reads saved evidence and writes a
compact display projection plus content pins. It never edits scientific results.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

PACKAGE = 'research/m31-direct-load-diagnostic-2026-10-17'
PRIOR = 'research/m31-normalizer-replication-2026-10-17'
TIERS = ['1e-8', '1e-4', '1e-2']
PLAN = [{'id': run + '-t' + str(t), 'runId': run, 't': t}
        for run in ['run-a', 'run-b'] for t in [0, 5, 10]]
MIB = 1024 * 1024
SOURCE_COMMIT = 'ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf'
MANIFEST_SHA = '93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b'
RESULT_PINS = {
    'analyze-attempt.json': (971, 'd9b3e2894d909d78f3aeb85a7dfeb6b8cbb980e5474904bda36c3c6b7546e32d'),
    'analyze.json': (5452100, '8b2cee37458583fbf4b78f343134f2805221f211209ba13d53208a42eaa8624b'),
    'check-attempt.json': (980, '5f2e629f8708b1d3d67f236263419ea423e75c6542efb5edac74c240d3197589'),
    'check.json': (45680, '18caa7a9d1153adead64e3f5741dc15225d5e1fa1dd1f5b17e0c6f817046fe35')}
CATEGORIES = ['rotor', 'collective', 'worldForce', 'worldMoment']


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'Duplicate JSON object key')
        out[key] = value
    return out


def verify_inventory(root, manifest):
    need(len(manifest['files']) == 159, 'Expected 159 immutable source/input pins')
    inventory = []
    for p in manifest['files']:
        relative = p['path']
        need(not Path(relative).is_absolute() and '..' not in Path(relative).parts,
             'Noncanonical frozen path')
        path = root / relative
        need(path.is_file() and not path.is_symlink() and path.resolve() == path,
             'Missing or noncanonical frozen file')
        raw = path.read_bytes()
        need(len(raw) == p['bytes'] and digest(raw) == p['sha256'], 'Frozen source/input pin differs: ' + relative)
        inventory.append({'path': relative, 'bytes': len(raw), 'sha256': digest(raw)})
    for name, (size, expected) in RESULT_PINS.items():
        path = root / PACKAGE / 'results' / name
        raw = path.read_bytes()
        need(len(raw) == size and digest(raw) == expected, 'Accepted result pin differs: ' + name)
        inventory.append({'path': PACKAGE + '/results/' + name, 'bytes': len(raw), 'sha256': digest(raw)})
    return inventory


def summary(proposal, audit):
    value = proposal[audit]
    need(set(value['maxErrors']) == set(CATEGORIES) and
         [v['tier'] for v in value['tiers']] == TIERS, 'Audit projection schema differs')
    allowed = ['pass', 'definite-fail', 'unresolved'] if audit == 'A' else ['pass', 'not-certified']
    for tier in value['tiers']:
        need(set(tier['categories']) == set(CATEGORIES) and tier['overall'] in allowed and
             all(v in allowed for v in tier['categories'].values()), 'Invalid saved audit status')
    for box in value['maxErrors'].values():
        need(set(box) == {'l', 'u'}, 'Saved normalized-error box missing')
        for q in box.values():
            need(set(q) == {'n', 'd'} and isinstance(q['n'], str) and isinstance(q['d'], str) and
                 re.fullmatch('0|[1-9][0-9]*', q['n']) and re.fullmatch('[1-9][0-9]*', q['d']),
                 'Saved normalized-error rational malformed')
    return {'maxErrors': value['maxErrors'], 'tiers': value['tiers']}



def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_input_hash(identifier, inp):
    # This is the semantic input identity written by moving-admission/check.py.
    # It differs from the saved JSON file's byte hash (including its newline).
    envelope = {'domain': 'm31-moving-admission/input/v1', 'id': identifier, 'input': inp}
    raw = json.dumps(envelope, sort_keys=True, separators=(',', ':'),
                     ensure_ascii=True, allow_nan=False).encode('ascii')
    return digest(raw)


def words(value, length):
    return (isinstance(value, list) and len(value) == length and
            all(isinstance(w, str) and re.fullmatch('[0-9a-f]{16}', w) for w in value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--source-manifest-sha256', required=True)
    args = parser.parse_args()
    root, output = args.root.resolve(strict=True), args.output.resolve(strict=True)
    need(re.fullmatch('[0-9a-f]{40}', args.source_commit), 'Expected accepted source commit required')
    need(re.fullmatch('[0-9a-f]{64}', args.source_manifest_sha256), 'Expected accepted manifest digest required')
    need(output.is_dir() and output == root / PACKAGE / 'viewer', 'Canonical package viewer output directory required')
    need(args.source_commit == SOURCE_COMMIT and args.source_manifest_sha256 == MANIFEST_SHA, 'Wrong accepted allocation')
    need(not (output / 'binding.json').exists() and not (output / 'display-data.json').exists(),
         'Preserve existing display build; use a separately reviewed fresh output directory')
    app_path = output / 'app.js'
    need(app_path.is_file() and not app_path.is_symlink(), 'Draft app.js required')
    app = app_path.read_text()
    marker = r"const BINDING_SHA='(?:__BINDING_SHA__|[0-9a-f]{64})';"
    need(len(re.findall(marker, app)) == 1, 'Unique binding marker required')
    pins = {}
    manifest_pins = {}

    def load(relative, cap=16 * MIB, frozen=False):
        need((relative.startswith(PACKAGE + '/') or relative.startswith(PRIOR + '/')) and
             '..' not in Path(relative).parts and not Path(relative).is_absolute(), 'Noncanonical evidence path')
        path = root / relative
        need(path.is_file() and not path.is_symlink() and path.resolve() == path, 'Missing or noncanonical saved evidence: ' + relative)
        need(path.stat().st_size <= cap, 'Saved evidence size limit: ' + relative)
        raw = path.read_bytes()
        pin = {'path': relative, 'bytes': len(raw), 'sha256': digest(raw)}
        if frozen:
            expected = manifest_pins.get(relative)
            need(expected is not None and all(expected.get(k) == pin[k] for k in ['bytes', 'sha256']),
                 'Evidence differs from frozen analysis input: ' + relative)
        need(relative not in pins or pins[relative] == pin, 'Evidence changed during display build')
        pins[relative] = pin
        return json.loads(raw, object_pairs_hook=unique_object)

    manifest_path = PACKAGE + '/source-manifest.json'
    manifest = load(manifest_path, 4 * MIB)
    need(pins[manifest_path]['sha256'] == args.source_manifest_sha256, 'Accepted manifest differs')
    for p in manifest['files']:
        need(p['path'] not in manifest_pins, 'Duplicate frozen input pin')
        manifest_pins[p['path']] = p
    before = verify_inventory(root, manifest)
    publication = load(PACKAGE + '/source-publication.json', MIB)
    need(publication.get('commit') == SOURCE_COMMIT and publication.get('manifestSha256') == MANIFEST_SHA and
         publication.get('verifiedFilePins') == 159 and publication.get('remoteBytesEqualLocal') is True and
         publication.get('committedBytesEqualLocal') is True, 'Accepted publication receipt differs')
    attempts, evidence = {}, {}
    for stage in ['analyze', 'check']:
        attempts[stage] = load(PACKAGE + '/results/' + stage + '-attempt.json', MIB)
        a = attempts[stage]
        need(a.get('schema') == 'm31-direct-load-attempt-v1' and a.get('stage') == stage and
             a.get('status') == 'completed' and a.get('exitCode') == 0 and
             a.get('firstFailure') is None and a.get('sourceCommit') == args.source_commit and
             a.get('sourceManifestSha256') == args.source_manifest_sha256 and a.get('verifiedPins') == 159,
             'Analysis/check not successfully closed under accepted identity')
        path = PACKAGE + '/results/' + stage + '.json'
        evidence[stage] = load(path)
        need(a.get('outputSha256') == pins[path]['sha256'] and a.get('outputBytes') == pins[path]['bytes'],
             'Saved output differs from completed attempt: ' + stage)
    analysis, check = evidence['analyze'], evidence['check']
    need(check.get('schema') == 'm31-direct-load-independent-check-v1' and
         check.get('passed') is True and check.get('firstFailure') is None and
         check.get('verified') == {'states': 6, 'proposals': 12, 'candidateRotors': 3072,
                                  'referencePairs': 96768, 'A': 12, 'B': 12, 'C': 6,
                                  'certificateRows': 4608, 'omissionDiagnosticRows': 1536},
         'Independent saved-data check must fully pass before display build')
    need(analysis.get('schema') == 'm31-direct-load-diagnostic-v1' and analysis.get('tiers') == TIERS and
         analysis.get('proposalCount') == 12 and
         [s.get('id') for s in analysis.get('states', [])] == [p['id'] for p in PLAN] and
         [s.get('id') for s in check.get('outcomes', [])] == [p['id'] for p in PLAN],
         'Analysis/check schema or six-state schedule differs')
    check_pins = {p['path']: p for p in check['inputPins']}
    need(len(check_pins) == len(check['inputPins']) and
         check_pins.get(PACKAGE + '/results/analyze.json') == pins[PACKAGE + '/results/analyze.json'],
         'Checker does not bind accepted analysis bytes')

    # The prior replication's speed gates failed. Its overall passed flag is not
    # used as a pose-acceptance gate; numerical/admission evidence is checked below.
    prior_index = load(PRIOR + '/results/index.json', 4 * MIB, frozen=True)
    prior_check = load(PRIOR + '/results/check.json', 4 * MIB, frozen=True)
    identity_keys = ['sourceCommit', 'sourceManifestSha256', 'configSha256']
    need(prior_check.get('denominator') == 6 and all(prior_check.get(k) is True for k in
         ['recordIntegrityPassed', 'equivalencePassed', 'admissionPassed']), 'Prior numerical/admission evidence not accepted')
    need(prior_index.get('schema') == 'm31-normalizer-ablation-index-v1' and
         prior_index.get('configId') == 'm31-normalizer-replication-v1' and
         all(prior_index.get(k) == prior_check.get(k) for k in identity_keys), 'Prior evidence identity mismatch')
    need([{k: s.get(k) for k in ['id', 'runId', 't']} for s in prior_index.get('scheduled', [])] == PLAN,
         'Prior index schedule differs from six saved snapshots')
    need(re.fullmatch('[0-9a-f]{40}', prior_index.get('sourceCommit', '')) and all(
         re.fullmatch('[0-9a-f]{64}', prior_index.get(k, '')) for k in identity_keys[1:]), 'Prior source identity unavailable')
    generations = {}
    for run in ['run-a', 'run-b']:
        path = PRIOR + '/results/generation/' + run + '.json'
        g = load(path, 8 * MIB, frozen=True)
        need(g.get('schema') == 'm31-moving-admission-generation-v1' and g.get('id') == run and
             g.get('configId') == 'm31-normalizer-replication-v1' and
             g.get('seed') == {'run-a': 26171021, 'run-b': 26171022}[run] and
             g.get('requested', {}).get('airflow') == 'off' and g.get('requested', {}).get('count') == 64 and
             g.get('error') is None and all(g.get(k) == prior_index.get(k) for k in identity_keys),
             'Wrong or incomplete prior generation')
        descriptors = [d for d in prior_index.get('generations', []) if d.get('id') == run]
        need(len(descriptors) == 1 and all(descriptors[0].get(k) == pins[path][k] for k in ['path', 'bytes', 'sha256']),
             'Prior index does not bind generation bytes')
        desc = descriptors[0]
        need(desc.get('status') == 'completed' and desc.get('error') is None and desc.get('seed') == g['seed'] and
             isinstance(g.get('frames'), list) and desc.get('frameCount') == len(g['frames']) and
             desc.get('reachedTimes') == [0, 5, 10] and desc.get('missingTimes') == [],
             'Prior generation descriptor is not complete for all three snapshots')
        generations[run] = g

    states = []
    for plan, saved in zip(PLAN, analysis['states']):
        name = plan['id']
        input_path = PRIOR + '/results/inputs/' + name + '.json'
        reference_path = PRIOR + '/results/reference/' + name + '.json'
        inp = load(input_path, MIB, frozen=True)
        ref = load(reference_path, 32 * MIB, frozen=True)
        need(saved.get('inputFile') == pins[input_path] == check_pins.get(input_path) and
             saved.get('referenceFile') == pins[reference_path] == check_pins.get(reference_path),
             'Producer/checker source input/reference byte pins differ')
        drones = inp.get('drones', [])
        ids = [d.get('id') for d in drones]
        need(len(ids) == 64 and len(set(ids)) == 64 and all(type(i) is int and 0 <= i <= 65535 for i in ids), 'Invalid saved IDs')
        id_set = set(ids)
        need(all(words(d.get('state'), 17) for d in drones), 'Invalid saved raw state words')
        input_identity = canonical_input_hash(name, inp)
        need(ref.get('schema') == 'm31-normalizer-ablation-reference-v1' and ref.get('id') == name and
             ref.get('referenceStatus') == 'admitted' and ref.get('sourceCommit') == prior_index['sourceCommit'] and
             ref.get('inputSha256') == saved.get('inputSha256') == input_identity,
             'Canonical reference/input identity differs')
        reference_descriptors = [d for d in prior_check.get('referenceFiles', []) if d.get('id') == name]
        need(len(reference_descriptors) == 1 and
             all(reference_descriptors[0].get(k) == pins[reference_path][k] for k in ['path', 'bytes', 'sha256']),
             'Prior independent check does not bind reference bytes')
        g = generations[plan['runId']]
        frames = [f for f in g.get('frames', []) if f.get('t') == plan['t']]
        slots = [s for s in g.get('slots', []) if s.get('t') == plan['t']]
        projected = [w for d in drones for w in d['state'][:3] + d['state'][6:10]]
        need(len(frames) == 1 and words(frames[0].get('words'), 448) and frames[0]['words'] == projected,
             'Saved generation frame differs from actual scheduled input')
        need(len(slots) == 1 and slots[0].get('status') == 'reached' and slots[0].get('input') == inp,
             'Saved generation slot differs from scheduled input')
        scheduled = next(s for s in prior_index['scheduled'] if s['id'] == name)
        generation_path = PRIOR + '/results/generation/' + plan['runId'] + '.json'
        need(scheduled.get('status') == 'evaluated' and scheduled.get('reason') is None and
             scheduled.get('inputSha256') == input_identity and
             scheduled.get('generationSha256') == pins[generation_path]['sha256'],
             'Prior index does not bind this snapshot input and generation')
        prepared_list = ref.get('prepared', [])
        prepared = {d['id']: d for d in prepared_list}
        need(len(prepared_list) == len(prepared) == 64 and set(prepared) == set(ids), 'Prepared identities differ')
        geometry = []
        for d in drones:
            p = prepared[d['id']]
            v = p.get('value', {})
            need(p.get('rejection') is None and words(v.get('center'), 3) and v['center'] == d['state'][:3] and
                 isinstance(v.get('points'), list) and len(v['points']) == 4 and all(words(a, 3) for a in v['points']),
                 'Prepared line endpoints are missing or mismatched')
            geometry.append({'id': d['id'], 'center': v['center'], 'points': v['points']})

        # Read only saved classifications for display membership. No coefficient
        # arithmetic, query, proof check or selection algorithm is re-executed.
        positive = set()
        pair_keys = set()
        for p in ref.get('pairs', []):
            i, r, j = p.get('i'), p.get('r'), p.get('j')
            # i/j are stable IDs emitted by semantic-reference.py. Its internal
            # array indices were ii/jj; those are not the saved pair identities.
            need(type(i) is int and type(j) is int and type(r) is int and i in id_set and
                 j in id_set and 0 <= r < 4 and i != j and p.get('status') in ['positive', 'zero'], 'Invalid reference pair for display')
            key = (i, r, j)
            need(key not in pair_keys, 'Duplicate saved reference pair')
            pair_keys.add(key)
            if p['status'] == 'positive':
                positive.add(key)
        need(len(pair_keys) == 16128 and len(positive) == saved.get('positiveTerms') ==
             ref.get('graph', {}).get('positiveRotorPairs'), 'Full positive denominator differs')
        mask = saved.get('mask', [])
        links = [[p['i'], p['r'], p['j']] for p in mask]
        need(len(links) == len({tuple(v) for v in links}) == (len(positive) + 9) // 10 and
             all(tuple(v) in positive for v in links), 'Saved omission mask identity/count differs')
        need([p.get('id') for p in saved.get('proposals', [])] == ['full', 'omit10'], 'Fixed two-proposal schedule differs')
        proposals = {}
        outcome = next(v for v in check['outcomes'] if v['id'] == name)
        need(outcome['positiveTerms'] == len(positive) and outcome['omittedCount'] == len(mask),
             'Checker denominator or omission count differs')
        for proposal in saved['proposals']:
            label = proposal['id']
            need(proposal['omittedCount'] == (0 if label == 'full' else len(mask)) and
                 [v['id'] for v in proposal['candidate']] == ids and
                 all(len(v['xHex']) == 4 for v in proposal['candidate']), 'Saved candidate identity differs')
            audits = {audit: summary(proposal, audit) for audit in (['A', 'B'] if label == 'full' else ['A', 'B', 'C'])}
            need(audits == outcome[label], 'Saved producer/checker audit projection differs')
            proposals[label] = {'omittedCount': proposal['omittedCount'], 'audits': audits}
        states.append({**plan, 'inputSha256': input_identity,
                       'inputFileSha256': pins[input_path]['sha256'],
                       'referenceFileSha256': pins[reference_path]['sha256'], 'ids': ids,
                       'poseWords': frames[0]['words'], 'geometry': geometry,
                       'positiveTerms': len(positive), 'proposals': proposals, 'omittedLinks': links})

    display = {'schema': 'm31-direct-load-display-v1', 'package': PACKAGE,
               'sourceCommit': args.source_commit, 'sourceManifestSha256': args.source_manifest_sha256,
               'checkerPassed': True, 'tiers': TIERS, 'states': states,
               'decision': check['decision'], 'fullControlStrictPass': check['fullControlStrictPass'],
               'allSixStrictHeadroom': check['allSixStrictHeadroom'],
               'scope': 'Saved airflow-off snapshots, oracle-assisted post-hoc numerical loads and omitted coefficient links; no live physics, physical validation or speed claim.'}
    display_raw = (json.dumps(display, separators=(',', ':'), allow_nan=False) + '\n').encode()
    need(len(display_raw) <= 16 * MIB, 'Compact display byte cap exceeded')
    binding = {'schema': 'm31-direct-load-view-binding-v1', 'package': PACKAGE,
               'sourceCommit': args.source_commit, 'sourceManifestSha256': args.source_manifest_sha256,
               'schedule': PLAN, 'pins': list(pins.values()),
               'immutableSourcePinCount': 159, 'resultFileCount': 4,
               'display': {'path': 'display-data.json', 'bytes': len(display_raw), 'sha256': digest(display_raw)},
               'scope': 'Read-only projection of accepted saved outputs and prior airflow-off poses. No scientific rerun.'}
    binding_raw = (json.dumps(binding, indent=2, allow_nan=False) + '\n').encode()
    need(len(binding_raw) <= 128 * 1024, 'Binding byte cap exceeded')
    updated, replacements = re.subn(marker, "const BINDING_SHA='" + digest(binding_raw) + "';", app, count=1)
    need(replacements == 1, 'Binding marker changed during build')
    need(digest((root / manifest_path).read_bytes()) == MANIFEST_SHA and
         verify_inventory(root, manifest) == before, 'Scientific files changed during display preparation')
    # All saved-data validation precedes writing. Outputs are exclusive; failures
    # never overwrite an earlier display build or alter original result bytes.
    with (output / 'display-data.json').open('xb') as stream:
        stream.write(display_raw)
    with (output / 'binding.json').open('xb') as stream:
        stream.write(binding_raw)
    app_path.write_text(updated)
    print(json.dumps({'states': len(states), 'sourcePins': len(pins),
                      'displayBytes': len(display_raw), 'displaySha256': digest(display_raw),
                      'bindingSha256': digest(binding_raw), 'scientificImports': 0,
                      'scientificExecution': False, 'generatedPoses': False,
                      'immutableSourcePins': 159, 'immutableResults': 4, 'omittedLinks': [len(s['omittedLinks']) for s in states]}))


if __name__ == '__main__':
    main()
