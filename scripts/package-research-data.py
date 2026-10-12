#!/usr/bin/env python3
"""Create a deterministic evidence bundle from the explicitly listed files."""
from pathlib import Path
import gzip,hashlib,json,tarfile
ROOT=Path(__file__).resolve().parents[1]
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as source:
  for chunk in iter(lambda:source.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
manifest_path=ROOT/'data/research-data-manifest.json'
m=json.loads(manifest_path.read_text())
out=ROOT/'work/github-publish'/m['asset'];out.parent.mkdir(parents=True,exist_ok=True)
with out.open('wb') as raw, gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=6) as zipped, tarfile.open(fileobj=zipped,mode='w|') as archive:
 for entry in m['files']:
  p=ROOT/entry['path']
  if p.stat().st_size!=entry['bytes'] or digest(p)!=entry['sha256']:
   raise SystemExit('Source changed: '+entry['path'])
  info=archive.gettarinfo(str(p),arcname=entry['path']);info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0;info.mode=0o644
  with p.open('rb') as source: archive.addfile(info,source)
m['archiveSha256']=digest(out)
m['archiveBytes']=out.stat().st_size
manifest_path.write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'asset':str(out),'files':len(m['files']),'bytes':m['archiveBytes'],'sha256':m['archiveSha256']}))
