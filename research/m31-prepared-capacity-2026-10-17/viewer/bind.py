"""Bind terminal saved evidence for the UI; no scientific imports or execution."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[3]
package = 'research/m31-prepared-capacity-2026-10-17'
viewer = root / package / 'viewer'
assert not (viewer / 'binding.json').exists(), 'Viewer already bound; preserve its evidence.'

def pin(path):
    raw = (root / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

result = pin(package + '/results/index.json')
index = json.loads((root / result['path']).read_bytes())
assert index['schema'] == 'm31-prepared-capacity-result-v1'
assert index['status'] in ('completed', 'failed'), 'Terminal result required.'
pins, runs = [result], []
for case in index['cases']:
    for key in ('result', 'profile'):
        if key in case:
            assert pin(case[key]['path']) == case[key], 'Saved case pin mismatch.'
            pins.append(case[key])
    if 'result' in case:
        runs.append({'id': case['id'], 'pin': case['result']})
for path in [package + '/viewer/scene.js', 'outputs/step02b-source/vendor/three.module.js',
             'outputs/step02b-source/vendor/three.core.js', 'outputs/step02b-source/vendor/OrbitControls.js']:
    pins.append(pin(path))
binding = {'schema': 'm31-prepared-capacity-viewer-binding-v1', 'status': 'terminal-bound',
           'sourceCommit': index['sourceCommit'], 'sourceManifestSha256': index['sourceManifestSha256'],
           'result': result, 'runs': runs, 'pins': pins}
raw = (json.dumps(binding, indent=2) + '\n').encode()
with (viewer / 'binding.json').open('xb') as stream:
    stream.write(raw)
app = viewer / 'app.js'
source = app.read_text()
assert source.count("const BINDING_SHA='UNBOUND';") == 1, 'App already bound.'
app.write_text(source.replace("const BINDING_SHA='UNBOUND';", "const BINDING_SHA='" + hashlib.sha256(raw).hexdigest() + "';"))
paths = ['index.html', 'style.css', 'app.js', 'scene.js', 'binding.json', 'bind.py', 'README.md',
         'qa/attempt01/run.cjs', 'qa/attempt01/supervise.py', 'qa/attempt01/PROTOCOL.md']
inventory = {'schema': 'm31-prepared-capacity-viewer-source-v1',
             'files': [pin(package + '/viewer/' + path) for path in paths]}
with (viewer / 'SOURCE-PINS.json').open('x') as stream:
    stream.write(json.dumps(inventory, indent=2) + '\n')
print(json.dumps({'result': result, 'bindingSha256': hashlib.sha256(raw).hexdigest(),
                  'viewerSourcePins': len(inventory['files']), 'scientificCalls': 0}))
