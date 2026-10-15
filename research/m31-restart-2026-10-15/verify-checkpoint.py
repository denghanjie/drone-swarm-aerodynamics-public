#!/usr/bin/env python3
"""Verify the committed checkpoint payload, without modifying any file."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text())
errors = []
for item in manifest['files']:
    path = root / item['path']
    if not path.is_file():
        errors.append({'path': item['path'], 'issue': 'missing'})
        continue
    raw = path.read_bytes()
    if len(raw) != item['bytes'] or hashlib.sha256(raw).hexdigest() != item['sha256']:
        errors.append({'path': item['path'], 'issue': 'changed'})
expected = {x['path'] for x in manifest['files']} | {'manifest.json'}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
          if p.is_file() and '__pycache__' not in p.parts and p.name != '.DS_Store'}
errors.extend({'path': p, 'issue': 'not in manifest'} for p in sorted(actual - expected))
print(json.dumps({'verifiedFiles': len(manifest['files']), 'errors': errors}, indent=2))
sys.exit(bool(errors))
