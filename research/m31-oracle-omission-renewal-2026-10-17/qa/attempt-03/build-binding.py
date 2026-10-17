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

PACKAGE = 'research/m31-oracle-omission-renewal-2026-10-17'
PRIOR = 'research/m31-normalizer-replication-2026-10-17'
TIERS = ['1e-8', '1e-4', '1e-2']
PLAN = [{'id': run + '-t' + str(t), 'runId': run, 't': t}
        for run in ['run-a', 'run-b'] for t in [0, 5, 10]]
MIB = 1024 * 1024


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
    need(output.is_dir(), 'Viewer output directory required')
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
        return json.loads(raw)

    manifest_path = PACKAGE + '/source-manifest.json'
    manifest = load(manifest_path, 4 * MIB)
    need(pins[manifest_path]['sha256'] == args.source_manifest_sha256, 'Accepted manifest differs')
    for p in manifest['files']:
        need(p['path'] not in manifest_pins, 'Duplicate frozen input pin')
        manifest_pins[p['path']] = p
    attempts, evidence = {}, {}
    for stage in ['analyze', 'check']:
        attempts[stage] = load(PACKAGE + '/results/' + stage + '-attempt.json', MIB)
        a = attempts[stage]
        need(a.get('schema') == 'm31-oracle-analysis-attempt-v1' and a.get('stage') == stage and
             a.get('status') == 'completed' and a.get('exitCode') == 0 and
             a.get('firstFailure') is None and a.get('sourceCommit') == args.source_commit and
             a.get('sourceManifestSha256') == args.source_manifest_sha256,
             'Analysis/check not successfully closed under accepted identity')
        path = PACKAGE + '/results/' + stage + '.json'
        evidence[stage] = load(path)
        need(a.get('outputSha256') == pins[path]['sha256'] and a.get('outputBytes') == pins[path]['bytes'],
             'Saved output differs from completed attempt: ' + stage)
    analysis, check = evidence['analyze'], evidence['check']
    need(check.get('schema') == 'm31-oracle-omission-independent-check-v1' and
         check.get('passed') is True and check.get('firstFailure') is None and
         check.get('verified') == {'states': 6, 'rows': 1536, 'tiers': 4608,
                                  'treeSelections': 9216, 'referencePairs': 96768},
         'Independent saved-data check must fully pass before display build')
    need(analysis.get('schema') == 'm31-oracle-omission-screen-v1' and analysis.get('tiers') == TIERS and
         [s.get('id') for s in analysis.get('states', [])] == [p['id'] for p in PLAN],
         'Analysis schema or six-state schedule differs')

    # The prior replication's speed gates failed. Its overall passed flag is not
    # used as a pose-acceptance gate; numerical/admission evidence is checked below.
    prior_index = load(PRIOR + '/results/index.json', 4 * MIB)
    prior_check = load(PRIOR + '/results/check.json', 4 * MIB)
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
        g = load(path, 8 * MIB)
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
        rows = saved.get('rows', [])
        need(len(rows) == 256 and {(r.get('i'), r.get('r')) for r in rows} ==
             {(i, r) for i in ids for r in range(4)}, 'Display requires every rotor row')
        need([q.get('tier') for q in saved.get('summary', [])] == TIERS, 'Summary tier order differs')
        links = {tier: {'T8': [], 'T2': []} for tier in TIERS}
        for row in rows:
            i, r = row['i'], row['r']
            need([q.get('tier') for q in row.get('tiers', [])] == TIERS, 'Row tier order differs')
            for q in row['tiers']:
                for tree in ['T8', 'T2']:
                    for group in q['trees'][tree]['selected']:
                        members = group['members']
                        nodes = saved['trees'][tree]['nodes']
                        node_id = group['node']
                        need(type(node_id) is int and 0 <= node_id < len(nodes) and
                             nodes[node_id]['members'] == members and i not in members,
                             'Selection is not its saved self-free whole node')
                        expected = [j for j in members if (i, r, j) in positive]
                        need(len(expected) >= 2 and group['positiveMembers'] == expected,
                             'Selected positive-member identities differ from reference')
                        links[q['tier']][tree].extend([[i, r, j] for j in expected])
        for q in saved['summary']:
            need(q['positiveTerms'] == len(positive), 'Summary positive denominator differs')
            for tree in ['T8', 'T2']:
                edges = links[q['tier']][tree]
                need(len(edges) == len({tuple(e) for e in edges}) == q['trees'][tree]['positiveCovered'],
                     'Display link count differs from checked summary')
        states.append({**plan, 'inputSha256': input_identity,
                       'inputFileSha256': pins[input_path]['sha256'], 'ids': ids,
                       'poseWords': frames[0]['words'], 'geometry': geometry,
                       'positiveTerms': len(positive), 'summary': saved['summary'], 'links': links})

    display = {'schema': 'm31-oracle-display-v1', 'package': PACKAGE,
               'sourceCommit': args.source_commit, 'sourceManifestSha256': args.source_manifest_sha256,
               'checkerPassed': True, 'tiers': TIERS, 'states': states,
               'scope': 'Saved snapshots and oracle coefficient bookkeeping only; no live approximation, load accuracy or speed claim.'}
    display_raw = (json.dumps(display, separators=(',', ':'), allow_nan=False) + '\n').encode()
    need(len(display_raw) <= 16 * MIB, 'Compact display byte cap exceeded')
    binding = {'schema': 'm31-oracle-view-binding-v1', 'package': PACKAGE,
               'sourceCommit': args.source_commit, 'sourceManifestSha256': args.source_manifest_sha256,
               'schedule': PLAN, 'pins': list(pins.values()),
               'display': {'path': 'display-data.json', 'bytes': len(display_raw), 'sha256': digest(display_raw)},
               'scope': 'Read-only projection of accepted saved outputs and prior airflow-off poses. No scientific rerun.'}
    binding_raw = (json.dumps(binding, indent=2, allow_nan=False) + '\n').encode()
    need(len(binding_raw) <= 128 * 1024, 'Binding byte cap exceeded')
    updated, replacements = re.subn(marker, "const BINDING_SHA='" + digest(binding_raw) + "';", app, count=1)
    need(replacements == 1, 'Binding marker changed during build')
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
                      'scientificExecution': False, 'generatedPoses': False}))


if __name__ == '__main__':
    main()
