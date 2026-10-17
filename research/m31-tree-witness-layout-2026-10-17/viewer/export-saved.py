"""Display prior actual geometry with separately checked storage figures only."""
from pathlib import Path
import hashlib,json
V=Path(__file__).resolve().parent;P=V.parent;ROOT=P.parents[1]
OLD=ROOT/'research/m31-native-tree-browser-probe-2026-10-17/viewer'
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def write(p,v):
 b=(json.dumps(v,separators=(',',':'),allow_nan=False)+'\n').encode()
 assert len(b)<=8*1024**2
 with p.open('xb') as f:f.write(b)
 return {'path':p.relative_to(V).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 attempt=read(P/'results/run-attempt.json');assert attempt['status'] in ('failed','completed')
 cp=P/'results/check.json';check=read(cp) if cp.exists() else {}
 passed=attempt['status']=='completed' and check.get('passed') is True and check.get('layoutQualified') is True
 rows={r['sourceRecordPin']['path']:r for r in check.get('records',[])} if passed else {}
 previous=read(OLD/'record-pins.json');source_manifest=read(OLD/'VIEWER-MANIFEST.json')
 source_pins={p['path']:p for p in source_manifest['files']}
 assert pin(OLD/'record-pins.json')==source_pins[str((OLD/'record-pins.json').relative_to(ROOT))]
 (V/'data').mkdir(exist_ok=False);files=[]
 for item in previous['cases']:
  source=OLD/item['path'];identity=pin(source)
  assert identity==source_pins[identity['path']] and identity['sha256']==item['sha256'] and identity['bytes']==item['bytes']
  data=read(source);assert data['validated'] is False
  source_h=data['provenance']['firstH'];row=rows.get(source_h['path'])
  if passed:
   assert row and row['sourceRecordPin']==source_h and row['layoutQualified'] is True and row['scientificValidated'] is False
   old,new=row['originalTreeBinaryBytes'],row['newTreeBinaryBytes']
   data['metrics']={'oldTreeBytes':old,'newTreeBytes':new,'savedBytes':old-new,'fraction':new/old}
  else:data['metrics']=None
  data['layoutQualified']=passed
  data['provenance']['originalDisplay']=identity
  data['provenance']['layoutAttempt']=pin(P/'results/run-attempt.json')
  data['provenance']['layoutCheck']=pin(cp) if cp.exists() else None
  data['provenance']['newTreeRecord']=row['newRecordPin'] if row else None
  files.append(dict(write(V/item['path'],data),caseId=data['caseId']))
 headline='Saved-tree reconstruction and storage target passed.' if passed else 'Saved-layout qualification did not complete.'
 detail=('All 156 saved record selections were checked. Both saved 5,000-drone H trees met the fixed half-size target. The original flight experiment remains incomplete; these are its earlier captured states.' if passed else 'The original flight experiment remains incomplete. Prior saved geometry is shown for context, without a new successful storage claim.')
 write(V/'record-pins.json',{'schema':'m31-tree-probe-display-pins-v1','headline':headline,'detail':detail,'checkAvailable':cp.exists(),'cases':files})
 write(V/'EXPORT-RECEIPT.json',{'scientificCalls':0,'layoutQualified':passed,'originalViewerManifest':pin(OLD/'VIEWER-MANIFEST.json'),'attempt':pin(P/'results/run-attempt.json'),'check':pin(cp) if cp.exists() else None,'cases':len(files),'scope':'Original geometry copied exactly; storage metrics bound by original H descriptor pins to full independent layout report. No fresh native/physics/reference execution.'})
 print(json.dumps({'cases':len(files),'layoutQualified':passed,'scientificCalls':0}))
if __name__=='__main__':main()
