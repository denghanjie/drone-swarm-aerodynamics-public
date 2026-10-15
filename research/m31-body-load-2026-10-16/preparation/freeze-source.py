"""Static byte sealer only. Does not import scientific code or realize inputs."""
from pathlib import Path
import json,hashlib
base=Path(__file__).resolve().parents[1];repo=base.parents[1]
if (base/'freeze.json').exists():raise SystemExit('Freeze is immutable')
if any((base/'raw').iterdir()):raise SystemExit('Numerical evidence already exists')
if any((base/'results').iterdir()):raise SystemExit('Launch/review evidence already exists')
if not (base/'FINAL-STATIC-REVIEW.md').is_file():raise SystemExit('Independent final review required')
files=[p for p in base.rglob('*') if p.is_file() and not ({'raw','results','viewer'}&set(p.relative_to(base).parts)) and p.name not in {'README.md','freeze.json'}]
for relative in ['outputs/step02c-source/physics.cjs','research/m31-source-omission-2026-10-16/source/independent.cjs','research/m31-coordinate-origin-2026-10-16/manifest.json','research/m31-coordinate-origin-2026-10-16/LITERATURE-EXPERIMENT-LEDGER.md','research/m31-coordinate-origin-2026-10-16/RESULT-LITERATURE-LEDGER.md','research/m31-browser-receiver-2026-10-16/API-EVIDENCE.md','research/m31-restart-2026-10-15/literature/annotated-ledger.md']:
 files.append(repo/relative)
pins=[]
for p in sorted(set(files)):
 data=p.read_bytes();pins.append({'path':p.relative_to(repo).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
freeze={'status':'FROZEN_SOURCE_UNEXECUTED','parentResultCommit':'436762c2d05408a22ba66400d64e46e759cc7b99','inputRelease':'Fixed namespace; no commit salt. Generate only after independent remote source/freeze verification and shared controls pass.','staticReviewSHA256':hashlib.sha256((base/'FINAL-STATIC-REVIEW.md').read_bytes()).hexdigest(),'scientificInvocations':1,'scientificWallSeconds':300,'rawByteCap':805306368,'resultByteCap':33554432,'savedReviewInvocations':1,'savedReviewWallSeconds':120,'savedReviewOutputByteCap':33554432,'reviewPreparation':'Only after science and external closure are terminal; separate source review/freeze before its sole saved-only invocation.','files':pins}
encoded=(json.dumps(freeze,indent=2)+'\n').encode()
# A failed/partial exclusive write is retained as a terminal preparation failure.
with (base/'freeze.json').open('xb') as output:output.write(encoded)
print(json.dumps({'freezeSHA256':hashlib.sha256(encoded).hexdigest(),'files':len(pins),'bytes':len(encoded)}))
