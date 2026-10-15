"""Static sealer: source bytes only, no diagnostic import or browser."""
from pathlib import Path
import hashlib,json
b=Path(__file__).resolve().parents[1];r=b.parents[1]
assert not (b/'freeze.json').exists() and not (b/'capture-launch.lock').exists()
assert not (b/'raw').exists() or not list((b/'raw').iterdir())
assert not (b/'results').exists() or not list((b/'results').iterdir())
files=[p for p in b.rglob('*') if p.is_file() and not ({'publication','review','viewer','raw','results'}&set(p.relative_to(b).parts)) and p.name not in {'README.md','freeze.json'}]
pins=[]
for p in sorted(files):
 assert not p.is_symlink() and p.resolve()==p.absolute()
 data=p.read_bytes();pins.append({'path':p.relative_to(r).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
freeze={'kind':'frozen-synthetic-transport-source','status':'FROZEN_SOURCE_UNEXECUTED','parentResultCommit':'22ca9e45cfe777def90dcab03530ba00055d3e99','diagnosticInvocations':1,'wallSeconds':60,'combinedBytes':8388608,'savedReviewInvocations':1,'savedReviewWallSeconds':30,'savedReviewBytes':8388608,'scientificInvocations':0,'files':pins}
data=(json.dumps(freeze,indent=2)+'\n').encode()
with (b/'freeze.json').open('xb') as f:assert f.write(data)==len(data)
print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'pins':len(pins)}))
