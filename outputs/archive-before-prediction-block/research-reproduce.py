#!/usr/bin/env python3
"""Verify pinned files, or reproduce numerical stages in a copied tree."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,datetime
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--stage',choices=['07','09-neighbors','10','11','12','13','14','14-first','15','15-probes','16','17','18','18-development','18-regression','18-stalls','18-replay','refinement-audit','19','19-solver','20','20-controls','20-replay','21','21-delay','21-audit','21-replay']);p.add_argument('--node',default='node');args=p.parse_args()
manifest=json.loads((ROOT/'research-manifest.json').read_text())
bad=[]
for entry in manifest['files']:
 f=ROOT/entry['path']
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=entry['sha256']:bad.append(entry['path'])
print(json.dumps({'verifiedFiles':len(manifest['files']),'changedOrMissing':bad},indent=2))
if bad:raise SystemExit(1)
if args.stage:
 dest=ROOT.parent/'work'/('reproduction-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
 shutil.copytree(ROOT,dest/'outputs');script={'07':'milestone-07-source/study.cjs','09-neighbors':'milestone-09-source/check-neighbors.mjs','10':'milestone-10-source/study.cjs','11':'milestone-11-source/study.cjs','12':'milestone-12-source/study.cjs','13':'milestone-13-source/study.cjs','14':'milestone-14-joint-source/study.cjs','14-first':'milestone-14-source/study.cjs','15':'milestone-15-source/diagnose.cjs','15-probes':'milestone-15-source/switch-probes.cjs','16':'milestone-16-source/study.cjs','17':'milestone-17-source/study.cjs','18':'milestone-18-source/study.cjs','18-development':'milestone-18-source/development.cjs','18-regression':'milestone-18-source/check-regression.cjs','18-stalls':'milestone-18-source/inspect-stalls.cjs','18-replay':'milestone-18-source/replay-diagnostic.cjs','refinement-audit':'milestone-18-source/refine-failures.cjs','19':'milestone-19-source/study.cjs','19-solver':'milestone-19-source/check-solver.cjs','20':'milestone-20-source/study.cjs','20-controls':'milestone-20-source/check-controls.cjs','20-replay':'milestone-20-source/build-replay.cjs','21':'milestone-21-source/study.cjs','21-delay':'milestone-21-source/check-delay.cjs','21-audit':'milestone-21-source/audit-failure.cjs','21-replay':'milestone-21-source/build-replay.cjs'}[args.stage]
 print('Isolated reproduction:',dest)
 subprocess.run([args.node,str(dest/'outputs'/script)],cwd=dest,check=True)

 if args.stage=='20':
  subprocess.run([args.node,str(dest/'outputs/milestone-20-source/build-replay.cjs')],cwd=dest,check=True)
 if args.stage=='21':
  for extra in ['audit-failure.cjs','build-replay.cjs']:
   subprocess.run([args.node,str(dest/'outputs/milestone-21-source'/extra)],cwd=dest,check=True)
