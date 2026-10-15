"""Source-only freeze; no operational import, browser or numerical work."""
from pathlib import Path
import hashlib,json
b=Path(__file__).resolve().parents[1];repo=b.parents[1]
assert not (b/'freeze.json').exists() and not (b/'capture-launch.lock').exists() and not (b/'review.lock').exists()
assert all(not (b/n).exists() or not list((b/n).iterdir()) for n in ['raw','results','review/results'])
pins=[]
for p in sorted(b.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(b)
 if {'publication','viewer','raw','results','__pycache__'} & set(rel.parts) or rel.name in ['README.md','freeze.json']:continue
 assert not p.is_symlink() and p.resolve()==p.absolute()
 data=p.read_bytes();pins.append({'path':p.relative_to(repo).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
freeze={'kind':'frozen-synthetic-control-channel-source','status':'FROZEN_SOURCE_UNEXECUTED','parentResultCommit':'98880952397aedbc99bdd11794ad6085d883328a','staticFollowupCommit':'57d275a1eed21475c76880cbab0ad1cf5edae8b1','diagnosticInvocations':1,'wallSeconds':60,'combinedBytes':8388608,'savedReviewInvocations':1,'savedReviewWallSeconds':30,'scientificInvocations':0,'files':pins}
data=(json.dumps(freeze,indent=2)+'\n').encode()
with (b/'freeze.json').open('xb') as f:assert f.write(data)==len(data)
print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'pins':len(pins)}))
