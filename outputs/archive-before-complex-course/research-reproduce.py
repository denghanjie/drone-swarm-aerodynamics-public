#!/usr/bin/env python3
"""Verify pinned files, or reproduce numerical stages in a copied tree."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,datetime
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--stage',choices=['07','09-neighbors','10','11','12']);p.add_argument('--node',default='node');args=p.parse_args()
manifest=json.loads((ROOT/'research-manifest.json').read_text())
bad=[]
for entry in manifest['files']:
 f=ROOT/entry['path']
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=entry['sha256']:bad.append(entry['path'])
print(json.dumps({'verifiedFiles':len(manifest['files']),'changedOrMissing':bad},indent=2))
if bad:raise SystemExit(1)
if args.stage:
 dest=ROOT.parent/'work'/('reproduction-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
 shutil.copytree(ROOT,dest/'outputs');script={'07':'milestone-07-source/study.cjs','09-neighbors':'milestone-09-source/check-neighbors.mjs','10':'milestone-10-source/study.cjs','11':'milestone-11-source/study.cjs','12':'milestone-12-source/study.cjs'}[args.stage]
 print('Isolated reproduction:',dest)
 subprocess.run([args.node,str(dest/'outputs'/script)],cwd=dest,check=True)
