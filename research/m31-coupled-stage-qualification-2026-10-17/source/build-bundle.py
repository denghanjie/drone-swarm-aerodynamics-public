"""SOURCE PACKAGING ONLY. Read exact bytes; never import/evaluate factories.
Not run by the drafting agent. Exclusive outputs: parent reviews then packages.
"""
from pathlib import Path
import hashlib,json
PACKAGE=Path(__file__).resolve().parents[1]
ROOT=PACKAGE.parents[1]
MODULES=[{'id': './vendor/reference-excerpt.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs'}, {'id': './vendor/anchor-kernel.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs'}, {'id': './vendor/lean-anchor.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs'}, {'id': './vendor/kernel.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs'}, {'id': './native-load.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs'}, {'id': './vendor/generation/step02c-source/physics.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs'}, {'id': './vendor/generation/milestone-31-source/sim.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs'}, {'id': './vendor/generation/milestone-31-source/grid.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs'}, {'id': './vendor/generation/milestone-31-source/geometry.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs'}, {'id': './vendor/generation/milestone-31-source/factory.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory.cjs'}, {'id': './vendor/generation/milestone-31-source/factory-wide.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory-wide.cjs'}, {'id': './vendor/generation/milestone-31-source/wall-filter.cjs', 'path': 'research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/wall-filter.cjs'}, {'id': './adapter.cjs', 'path': 'research/m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs'}, {'id': './browser-driver.cjs', 'path': 'research/m31-coupled-stage-qualification-2026-10-17/source/browser-driver.cjs'}]
def main():
    output=PACKAGE/'source/browser-bundle.js'; index=PACKAGE/'source/source-bundle.json'
    if output.exists() or index.exists():raise FileExistsError('exclusive-bundle-output')
    parts=[b"'use strict';\nwindow.__M31_BUNDLE_INSTALL__({\n"]; entries=[];length=len(parts[0])
    for item in MODULES:
        p=ROOT/item['path']
        if not p.resolve().is_relative_to(ROOT) or p.is_symlink():raise ValueError('bundle-source-path')
        prefix=(json.dumps(item['id'])+':function(module,exports,require,Buffer,process){\n').encode();parts.append(prefix);length+=len(prefix)
        raw=p.read_bytes();entries.append({**item,'offset':length,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        parts.extend([raw,b'\n},\n']);length+=len(raw)+len(parts[-1])
    parts.append(b'});\n');bundle=b''.join(parts)
    if len(bundle)>2*1024*1024:raise ValueError('bundle-byte-cap')
    with output.open('xb') as f:f.write(bundle)
    with index.open('x') as f:json.dump({'path':str(output.relative_to(ROOT)),'bytes':len(bundle),'sha256':hashlib.sha256(bundle).hexdigest(),'sources':entries},f,indent=2);f.write('\n')
if __name__=='__main__':main()
