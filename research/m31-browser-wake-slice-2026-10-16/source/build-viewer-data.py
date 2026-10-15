"""Bind original saved evidence to a static viewer; no scientific array decoding.

Run only after the coordinator reports the sole scientific invocation terminal.
This script reads JSON and hashes files. It never imports a model or checker,
rotates a quaternion, evaluates a wake, executes a shader, or calculates gates.
It writes only the requested output manifest. URLs target the published viewer
location, not the local output directory.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--review', type=Path, help='Approved terminal saved-review JSON; published as results/independent-review.json')
parser.add_argument('--review-runtime', type=Path, help='Original external saved-review closure JSON')
parser.add_argument('--review-checker', type=Path, help='Actual approved saved-review checker, hashed only')
parser.add_argument('--review-index', type=Path, help='Actual approved input index, hashed only; never published by this builder')
parser.add_argument('--review-runtime-public-path', default='results/saved-review-launch-public/runtime.json', help='Public runtime path relative to checkpoint')
args = parser.parse_args()
base = args.checkpoint.resolve()
repo = base.parents[1]
public_view = base / 'viewer'
result_path = base / 'results/result.json'
budget_path = base / 'results/budget.json'
result = json.loads(result_path.read_text())
budget = json.loads(budget_path.read_text())
if result.get('terminal') is not True or budget.get('terminal') is not True or budget.get('active') is not False:
    raise SystemExit('Refusing manifest: scientific invocation is not terminal')
ids = [27, 445, 4500, 988]
if result.get('config', {}).get('receiverIds') != ids:
    raise SystemExit('Frozen receiver order differs')
raw_index = {item['name']: item for item in result['files']}
files = {}
def add(key, path, label, *, raw_name=None, public_path=None):
    payload = path.read_bytes()
    descriptor = {'url': os.path.relpath(public_path or path, public_view), 'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest(), 'label': label}
    if raw_name:
        original = raw_index.get(raw_name)
        if not original or any(original[field] != descriptor[field] for field in ('bytes', 'sha256')):
            raise SystemExit('Original raw result index does not bind ' + raw_name)
        descriptor['rawName'] = raw_name
    files[key] = descriptor
    return descriptor
add('result', result_path, 'Original terminal scientific result')
add('budget', budget_path, 'Terminal scientific supervision ledger')
add('freeze', base/'freeze.json', 'Prospective source/input freeze')
add('selection', base/'selection/selection.json', 'Frozen exposed receiver selection')
add('schema', base/'schema.json', 'Retained record layout')
poses_path = repo/result['config']['sourceReferenceDirectory']/'raw'/(result['config']['sourceCase']+'-states.f64')
pose_spec = add('poses', poses_path, 'Original 5,000 saved poses')
pose_spec['repoPath'] = poses_path.relative_to(repo).as_posix()
freeze = json.loads((base/'freeze.json').read_text())
pose_pin = next((item for item in freeze['files'] if item['path'] == pose_spec['repoPath']), None)
if not pose_pin or any(pose_pin[field] != pose_spec[field] for field in ('bytes', 'sha256')):
    raise SystemExit('Original poses are not bound by the frozen input index')
references = {}
for stage in ['R', 'Q']:
    entry = {}
    for key, suffix in [('metadata','metadata.u32'),('scalars','scalars.f64'),('terms','terms.f64'),('sums','ordinarySums.f64'),('validity','sumValidity.u8'),('counts','counts.json')]:
        name = stage+'-'+suffix
        if (base/'raw'/name).exists():
            file_key = stage+key[0].upper()+key[1:]
            add(file_key, base/'raw'/name, stage+' '+key, raw_name=name)
            entry[key] = file_key
    if entry:
        references[stage] = entry
for key, name, label in [
    ('originalOffsets','R-prepared-offsets.f64','Saved prepared receiver offsets'),
    ('gpuTerms','terms-gpu.u32','Original materialized GPU term words'),
    ('gpuControls','controls-gpu.u32','Original GPU control words'),
    ('gpuSerial','reduce-gpu.u32','Original serial reduction words'),
]:
    if (base/'raw'/name).exists():
        add(key, base/'raw'/name, label, raw_name=name)
for stage in ['R','Q','controls','terms','serial']:
    name = stage+'-assessment.json'
    if (base/'raw'/name).exists():
        add(stage+'Report', base/'raw'/name, stage+' original saved assessment', raw_name=name)
review_contract = {'version': 1, 'bound': False, 'status': 'Independent saved review pending; viewer remains locked'}
if args.review:
    if not all([args.review_runtime, args.review_checker, args.review_index]):
        raise SystemExit('Binding review requires --review-runtime, --review-checker and --review-index')
    closure = json.loads(args.review_runtime.read_text())
    if closure.get('terminal') is not True or closure.get('active') is not False or closure.get('qualifiedReviewClosure') is not True:
        raise SystemExit('Independent saved-review external closure is not qualified')
    review = json.loads(args.review.read_text())
    if review.get('terminal') is not True:
        raise SystemExit('Saved review is not terminal')
    if review.get('sourceCommit') != result['sourceCommit'] or review.get('freezeSha256') != files['freeze']['sha256']:
        raise SystemExit('Saved review source/freeze mismatch')
    for key in ['inputIndexSha256','checkerSha256']:
        if not isinstance(review.get(key), str) or len(review[key]) != 64 or any(c not in '0123456789abcdef' for c in review[key]):
            raise SystemExit('Missing independent-review identity: '+key)
    for field, actual_path in [('checkerSha256', args.review_checker), ('inputIndexSha256', args.review_index)]:
        if hashlib.sha256(actual_path.read_bytes()).hexdigest() != review[field]:
            raise SystemExit('Actual saved-review identity mismatch: '+field)
    runtime_public = (base/args.review_runtime_public_path).resolve()
    if not runtime_public.is_relative_to(base):
        raise SystemExit('Review closure public path must remain inside checkpoint')
    add('reviewClosure', args.review_runtime, 'Original independent-review external closure', public_path=runtime_public)
    add('review', args.review, 'Original independent saved review', public_path=base/'results/independent-review.json')
    review_contract = {'version': 1, 'bound': True, 'integrityField': 'reviewPass', 'numericalField': 'fullSuiteQualified', 'inputIndexSha256': review['inputIndexSha256'], 'checkerSha256': review['checkerSha256']}
manifest = {
    'schemaVersion': 1,
    'scope': 'Static display of original saved poses/terms/reports; no fresh wake, root, flight, timing or scientific gate execution',
    'nSources': 5000, 'receiverIds': ids, 'poseStride': 17, 'quaternionOffset': 6,
    'sourceCommit': result['sourceCommit'], 'references': references, 'reviewContract': review_contract,
    'default': {'selectionIndex': 3, 'rotor': 3, 'color': 'error-TR', 'sourceRule': 'largest absolute difference of valid saved T and R terms; ascending source ID breaks ties', 'view': 'focused'},
    'files': files,
}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({'manifestWritten': True, 'fileCount': len(files), 'reviewBound': review_contract['bound'], 'scientificArraysDecoded': False, 'newScientificEvaluation': False}))
