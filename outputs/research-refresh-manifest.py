#!/usr/bin/env python3
"""Hash stable artifacts; explicitly exclude mutable output when studies are live."""
from pathlib import Path
import argparse,hashlib,json,datetime,os
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--live-stages',nargs='*',default=[],help='Stages whose mutable output must not be pinned during execution');args=parser.parse_args();live=set(args.live_stages)
completed={}
for m in live:
 f=root/f'milestone-{m}-progress.json'
 try:completed[m]={r['job']['id'] for r in json.loads(f.read_text())}
 except FileNotFoundError:completed[m]=set()
files=[];excluded=[]
for p in sorted(root.rglob('*')):
 if not p.is_file() or p.name=='.DS_Store' or '__pycache__' in p.parts or p in [root/'research-manifest.json',root/'research-manifest.json.tmp']:continue
 rel=str(p.relative_to(root));reason=None
 if live and rel=='research-block-26-29-progress.json':reason='live progress snapshot'
 for m in live:
  prefix=f'milestone-{m}-source/'
  if rel in [f'milestone-{m}-{x}' for x in ['progress.json','summary.json','comparisons.json','execution.log','queue-status.json']]:reason='study may write this output'
  if rel.startswith(prefix):
   name=rel[len(prefix):]
   if name=='index.json' or name.startswith('progress-') or name.startswith('checkpoint-'):reason='mutable index/progress/checkpoint'
   elif p.suffix in ['.f64','.json'] and name not in ['factory-wide.json','factory-narrow.json']:
    if p.stem not in completed[m]:reason='not registered as a completed immutable trial'
 if reason:excluded.append({'path':rel,'reason':reason});continue
 b=p.read_bytes();files.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'schema':'research-artifacts-v2','date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'description':'Stable-artifact snapshot. Completed trials and frozen sources are pinned; explicitly listed live outputs are excluded. Earlier snapshots and failed runs are preserved. This manifest does not certify physical validity or research completion.','liveStages':sorted(live),'excluded':excluded,'files':files}
target=root/'research-manifest.json';tmp=root/'research-manifest.json.tmp';tmp.write_text(json.dumps(manifest,indent=2));os.replace(tmp,target)
print(json.dumps({'pinnedFiles':len(files),'excludedLiveFiles':len(excluded),'liveStages':sorted(live)}))
