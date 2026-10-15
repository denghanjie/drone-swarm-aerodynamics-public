#!/usr/bin/env python3
"""Verify this published checkpoint and optional raw archive; no integration."""
import argparse,hashlib,json,tarfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);a=p.parse_args();r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((r/'manifest.json').read_text())
for x in manifest['files']:
 b=(r/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
if a.archive:
 m=json.loads((r/'raw-manifest.json').read_text());assert a.archive.stat().st_size==m['archiveBytes'];assert sha(a.archive.read_bytes())==m['archiveSha256']
 with tarfile.open(a.archive,'r:gz') as t:
  members=t.getmembers();assert len(members)==len(m['files'])
  for v,e in zip(members,m['files']):
   assert v.isfile() and v.name==e['path'] and v.size==e['bytes'];assert sha(t.extractfile(v).read())==e['sha256']
print(json.dumps({'verifiedFiles':len(manifest['files']),'rawArchiveVerified':bool(a.archive),'scope':'Byte integrity only; no experiment rerun or physical-validation claim'}))
