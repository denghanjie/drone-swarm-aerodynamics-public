"""Source-only checks. Does not import JS or any scientific/checker source."""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--campaign', type=pathlib.Path, required=True)
parser.add_argument('--node', required=True)
args = parser.parse_args()
p = pathlib.Path(__file__).resolve().parent
checks = []
def add(name, passed, detail=''):
    checks.append({'name': name, 'pass': bool(passed), 'detail': detail})

for path in sorted(p.glob('*.js')):
    run = subprocess.run([args.node, '--input-type=module', '--check'], input=path.read_text(), text=True, capture_output=True)
    add('syntax:' + path.name, run.returncode == 0, run.stderr.strip() or 'Syntax check on stdin; no module execution')
html = (p / 'index.html').read_text()
app = (p / 'app.js').read_text()
ev = (p / 'evidence.js').read_text()
scene = (p / 'scene.js').read_text()
adapter = (p / 'adapter.js').read_text()
meta = json.loads((p / 'data.json').read_text())
ids = re.findall(r'\bid="([^"]+)"', html)
refs = re.findall(r"\$\('([^']+)'\)", app)
add('html:unique-ids', len(ids) == len(set(ids)), str(len(ids)) + ' IDs')
add('html:literal-app-ids-exist', set(refs) <= set(ids), ','.join(sorted(set(refs) - set(ids))))
controls = re.findall(r"'([^']+)'", re.search(r'const controls = \[([^]]+)\]', app).group(1))
add('html:controls-present-disabled', all(re.search(r'id="' + re.escape(x) + r'"[^>]*\bdisabled', html) for x in controls))
add('html:local-import-map', '"three":"../../../outputs/step02b-source/vendor/three.module.js"' in html)
add('html:favicon', 'href="data:,"' in html)
add('html:separate-historical-replay', 'milestone-31-lab.html' in html and 'Separate historical missions with airflow off' in html)
add('manifest:review-lock', meta['bindingState'] == 'pending-independent-review' and meta['reviewContract']['bound'] is False and 'ADAPTER_READY = false' in adapter)
add('loader:pending-before-anchor-fetch', ev.index('throw new PendingEvidence') < ev.index('const anchors ='))
add('manifest:six-cells', len(meta['cells']) == 6 and {(c['origin'], c['arm']) for c in meta['cells']} == {(o, a) for o in range(2) for a in ['A', 'B', 'C']})
exposure = [(c['origin'], c['arm'], bool(c['terms']), bool(c['serial'])) for c in meta['cells']]
add('manifest:actual-exposure', exposure == [(0, 'A', True, True), (0, 'B', True, True), (0, 'C', True, True), (1, 'A', False, False), (1, 'B', False, False), (1, 'C', True, False)])
add('manifest:cell-isolation', all(all(c[k] is None or c[k].startswith('o' + str(c['origin']) + '-' + c['arm'] + '-') for k in ['terms', 'serial']) for c in meta['cells']))
result = json.loads((args.campaign / 'results/result.json').read_text())
freeze = json.loads((args.campaign / 'freeze.json').read_text())
raw = {x['name']: x for x in result['files']}
frozen = {x['path']: x for x in freeze['files']}
issues = []
for key, spec in meta['files'].items():
    content = (args.campaign / 'viewer' / spec['url']).resolve().read_bytes()
    if len(content) != spec['bytes'] or hashlib.sha256(content).hexdigest() != spec['sha256']:
        issues.append(key + ':actual-bytes')
    if 'rawName' in spec and any(spec[k] != raw[spec['rawName']][k] for k in ['bytes', 'sha256']):
        issues.append(key + ':raw-index')
    if 'repoPath' in spec and any(spec[k] != frozen[spec['repoPath']][k] for k in ['bytes', 'sha256']):
        issues.append(key + ':freeze')
add('manifest:actual-hashes-and-index-pins', not issues, ','.join(issues) or str(len(meta['files'])) + ' real descriptors; no numerical evaluation')
add('manifest:source-identity', meta['sourceCommit'] == result['sourceCommit'] == 'ccafbd9b9fd3a3cdd7ffacb5fb360ee5f3dc1abc')
add('decoder:26-words-18-scalars', '80000 * 104' in ev and '80000 * 144' in ev and 'gpu ? 104 : 32' in ev and len(re.findall(r"'[^']*'", re.search(r'export const FIELDS = \[([^]]+)\]', ev).group(1))) == 18)
read_lines = [line.strip() for line in ev.splitlines() if re.search(r'\.(getUint32|getFloat32|getFloat64|getBigUint64)\(', line)]
add('decoder:explicit-little-endian-reads', all(', true)' in line for line in read_lines), str(len(read_lines)) + ' source lines; manual contract inspection accompanies this token check')
add('decoder:validity-and-identity', '!identityValid || !reached[k]' in ev and 'termValid' in ev and 'return null' in ev)
add('scene:interaction-only-rendering', 'requestAnimationFrame' not in scene and 'enableDamping = false' in scene)
add('scene:actual-focus-filter', 'matrix.scale(hiddenScale)' in scene and "mode === 'focused'" in scene)
add('scene:context-and-observer-disposal', 'setFrame' in scene and 'resize.disconnect()' in scene and 'renderer.forceContextLoss()' in scene)
add('scene:draw-only-recenter', 'frame.origin' in scene and ').sub(shift)' in scene)
imports = []
for path in p.glob('*.js'):
    imports += re.findall(r"(?:from\s+|import\()['\"]([^'\"]+)", path.read_text())
add('source:no-scientific-imports', not any(re.search(r'generator|experiment|assessment|checker|\.wgsl|host', value) for value in imports), ', '.join(imports))
private = []
for path in p.iterdir():
    if path.suffix in ['.js', '.html', '.css', '.md', '.json'] and path.name not in ['static-checks.json', 'artifacts.json']:
        if re.search(r'/(?:Users|home|private/tmp|tmp)/', path.read_text()):
            private.append(path.name)
add('publication:no-private-absolute-paths', not private, ','.join(private))
report = {
    'status': 'static-source-checks-only',
    'timestampUTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'allPass': all(item['pass'] for item in checks),
    'executed': {'javascriptSyntaxOnly': True, 'htmlAndManifestStructure': True, 'actualFileHashAndOriginalIndexComparison': True, 'browser': False, 'WebGL': False, 'generator': False, 'scientificModel': False, 'GPUScience': False, 'reviewChecker': False, 'numericalGateRecomputation': False},
    'checks': checks,
    'remaining': ['Bind actual independent review receipt, input index and external closure', 'Implement and review verifyPublishedEvidence against those exact artifacts', 'Parent browser QA and final integration']
}
(p / 'static-checks.json').write_text(json.dumps(report, indent=2) + '\n')
artifacts = []
for path in sorted(p.iterdir()):
    if path.is_file() and path.name != 'artifacts.json':
        content = path.read_bytes()
        artifacts.append({'path': path.name, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
(p / 'artifacts.json').write_text(json.dumps({'status': 'source-handoff-review-binding-pending-browser-qa-unexecuted', 'files': artifacts}, indent=2) + '\n')
print(json.dumps({'allPass': report['allPass'], 'checks': len(checks), 'failed': [item for item in checks if not item['pass']], 'files': len(artifacts)}, indent=2))
raise SystemExit(0 if report['allPass'] else 1)
