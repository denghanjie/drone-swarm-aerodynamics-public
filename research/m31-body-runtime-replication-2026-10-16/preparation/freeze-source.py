"""Static byte sealer only. Does not import scientific code or realize inputs."""
from pathlib import Path
import json,hashlib
base=Path(__file__).resolve().parents[1];repo=base.parents[1]
if (base/'freeze.json').exists():raise SystemExit('Freeze is immutable')
if (base/'capture-launch.lock').exists():raise SystemExit('External science capture already reserved')
if any((base/'raw').iterdir()):raise SystemExit('Numerical evidence already exists')
if any((base/'results').iterdir()):raise SystemExit('Launch/review evidence already exists')
if not (base/'FINAL-STATIC-REVIEW.md').is_file():raise SystemExit('Independent final review required')
files=[p for p in base.rglob('*') if p.is_file() and not ({'raw','results','viewer'}&set(p.relative_to(base).parts)) and p.name not in {'README.md','freeze.json'}]
for relative in ['outputs/step02c-source/physics.cjs','research/m31-source-omission-2026-10-16/source/independent.cjs','research/m31-body-load-2026-10-16/manifest.json','research/m31-body-load-2026-10-16/freeze.json','research/m31-body-load-2026-10-16/PROTOCOL.md','research/m31-body-load-2026-10-16/design/ADOPTION.md','research/m31-coordinate-origin-2026-10-16/LITERATURE-EXPERIMENT-LEDGER.md','research/m31-coordinate-origin-2026-10-16/RESULT-LITERATURE-LEDGER.md','research/m31-browser-receiver-2026-10-16/API-EVIDENCE.md','research/m31-restart-2026-10-15/literature/annotated-ledger.md']:
 files.append(repo/relative)
pins=[]
for p in sorted(set(files)):
 if not p.is_file() or p.is_symlink() or p.resolve()!=p.absolute() or not p.absolute().is_relative_to(repo.absolute()):raise SystemExit('Regular contained non-symlink pin required')
 data=p.read_bytes();pins.append({'path':p.relative_to(repo).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
config=json.loads((base/'config.json').read_text())
parent=config.get('parentResultCommit')
if not isinstance(parent,str) or len(parent)!=40 or any(c not in '0123456789abcdef' for c in parent):raise SystemExit('Published parent result required')
if not (base/'design/ADOPTION.md').is_file():raise SystemExit('Distinct allocation required')
freeze={'status':'FROZEN_SOURCE_UNEXECUTED','parentResultCommit':config['parentResultCommit'],'inputRelease':'Fixed namespace; no commit salt. Generate only after independent remote source/freeze verification and runtime/device/pipeline admission plus shared controls pass.','staticReviewSHA256':hashlib.sha256((base/'FINAL-STATIC-REVIEW.md').read_bytes()).hexdigest(),'scientificInvocations':1,'scientificWallSeconds':300,'rawByteCap':805306368,'resultByteCap':33554432,'savedReviewInvocations':1,'savedReviewWallSeconds':120,'savedReviewOutputByteCap':33554432,'reviewPreparation':'Only after science and external closure are terminal; separate source review/freeze before its sole saved-only invocation.','files':pins}
encoded=(json.dumps(freeze,indent=2)+'\n').encode()
# A failed/partial exclusive write is retained as a terminal preparation failure.
with (base/'freeze.json').open('xb') as output:output.write(encoded)
print(json.dumps({'freezeSHA256':hashlib.sha256(encoded).hexdigest(),'files':len(pins),'bytes':len(encoded)}))
