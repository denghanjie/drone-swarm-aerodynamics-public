"""Final byte-only publication inventory; no diagnostic or reviewer execution."""
from pathlib import Path
import hashlib,json
b=Path(__file__).resolve().parents[1];repo=b.parents[1];target=b/'manifest.json'
assert not target.exists()
for freeze_path,prefix in [(b/'freeze.json',repo),(b/'review/review-freeze.json',b),(b/'review/evidence-manifest.json',b)]:
 for pin in json.loads(freeze_path.read_bytes())['files']:
  p=prefix/pin['path'];data=p.read_bytes();assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']
a=json.loads((b/'publication/final-review-disposition.json').read_bytes())
assert a['scopedPublicEvidenceVerified'] is True and a['scientificQualified'] is False and a['historicalFailureExplained'] is False
files={p for p in b.rglob('*') if p.is_file() and p!=target}
files.update(repo/'outputs/step02b-source/vendor'/name for name in ['three.core.js','three.module.js','OrbitControls.js'])
pins=[]
for p in sorted(files):
 assert not p.is_symlink() and p.resolve()==p.absolute() and p.is_relative_to(repo)
 data=p.read_bytes();pins.append({'path':p.relative_to(repo).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
m={'kind':'terminal-synthetic-transport-publication-manifest','sourceCommit':'fe2c19a30b4605ec755e8e7103946d7ef037a76a','sourceFreezeSHA256':hashlib.sha256((b/'freeze.json').read_bytes()).hexdigest(),'reviewSourceCommit':'459a5c6f3bb5abf3107c39f9fe2b413c1bbbcbcf','reviewFreezeSHA256':hashlib.sha256((b/'review/review-freeze.json').read_bytes()).hexdigest(),'diagnosticTerminal':True,'reviewTerminal':True,'transferSucceeded':False,'scopedPublicEvidenceVerified':True,'privateTraceVerified':False,'scientificQualified':False,'historicalFailureExplained':False,'retryPermitted':False,'scope':'One fully observed failed synthetic transfer, separately verified public records, visible saved-event Three.js diagram and static next questions. This byte inventory does not expand scientific or private-trace claims.','files':pins}
data=(json.dumps(m,indent=2)+'\n').encode()
with target.open('xb') as f:assert f.write(data)==len(data)
print(json.dumps({'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'pins':len(pins),'totalPinnedBytes':sum(x['bytes'] for x in pins)}))
