"""Package exact source bytes; never import or evaluate scientific modules.

Run only as a source-packaging step before manifest freeze. Existing outputs
are refused. The source directory defaults to this script's directory.
"""
from pathlib import Path
import hashlib
import json
import sys

PACKAGE = 'research/m31-native-fresh-transfer-2026-10-17'
MODULES = ['vendor/reference-excerpt.cjs', 'vendor/anchor-kernel.cjs',
           'vendor/lean-anchor.cjs', 'vendor/kernel.cjs', 'vendor/controls.cjs',
           'native-load.cjs', 'native-controls.cjs']


def main():
    source = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parent
    if len(sys.argv) > 2:
        raise ValueError('at most one source-directory argument')
    output = source / 'browser-bundle.js'
    specification = source / 'source-bundle.json'
    if output.exists() or specification.exists():
        raise FileExistsError('source packaging is exclusive; do not overwrite an existing bundle')
    parts = [b"'use strict';\nwindow.__M31_BUNDLE_INSTALL__({\n"]
    entries = []
    length = len(parts[0])
    for name in MODULES:
        prefix = (json.dumps('./' + name) + ':function(module,exports,require,Buffer){\n').encode()
        parts.append(prefix)
        length += len(prefix)
        raw = (source / name).read_bytes()
        entries.append({'id': './' + name, 'path': PACKAGE + '/source/' + name,
                        'offset': length, 'bytes': len(raw),
                        'sha256': hashlib.sha256(raw).hexdigest()})
        parts.extend([raw, b'\n},\n'])
        length += len(raw) + len(parts[-1])
    parts.append(b'});\n')
    bundle = b''.join(parts)
    if len(bundle) > 1024 * 1024:
        raise ValueError('bundle exceeds one MiB')
    pin = {'path': PACKAGE + '/source/browser-bundle.js', 'bytes': len(bundle),
           'sha256': hashlib.sha256(bundle).hexdigest(), 'sources': entries}
    with output.open('xb') as stream:
        stream.write(bundle)
    with specification.open('x') as stream:
        json.dump(pin, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
