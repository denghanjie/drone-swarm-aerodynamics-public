"""Recreate a published byte artifact on a fresh clone; no model execution."""
from pathlib import Path
import json,hashlib,os,sys
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
base=Path(__file__).resolve().parent.parent
ix=json.loads((base/'transport/index.json').read_bytes());original=ix['original']
assert ix['complete'] and original['path']=='extract/selected.jsonl.gz'
target=base/original['path'];assert not target.exists(),'refuse-to-overwrite';target.parent.mkdir(exist_ok=True)
temporary=target.with_suffix('.reassembling');total=0;h=hashlib.sha256()
with temporary.open('xb') as dest:
 for i,p in enumerate(ix['parts']):
  assert p['file']=='selected.jsonl.gz.part'+str(i).zfill(3) and p['offset']==total
  b=(base/'transport'/p['file']).read_bytes();assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'];dest.write(b);total+=len(b);h.update(b)
assert total==original['bytes'] and h.hexdigest()==original['sha256']
assert not target.exists();temporary.rename(target)
print('Exact selected evidence reconstructed; no scientific calculation run.')
