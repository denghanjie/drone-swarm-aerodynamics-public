#!/usr/bin/env python3
"""Verify pinned files, or reproduce numerical stages in a copied tree."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,datetime,sys,importlib.util
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--stage',choices=['07','09-neighbors','10','11','12','13','14','14-first','15','15-probes','16','17','18','18-development','18-regression','18-stalls','18-replay','refinement-audit','19','19-solver','20','20-controls','20-replay','21','21-delay','21-audit','21-replay','22','22-observer','22-audit','22-trace','23','23-audit','24','24-check','25','26','26-check','27','27-check','28','28-check','29','30','31']);p.add_argument('--node',default='node');p.add_argument('--skip-figures',action='store_true',help='Reproduce numerical results without optional Matplotlib figures');args=p.parse_args()
manifest=json.loads((ROOT/'research-manifest.json').read_text())
bad=[]
for entry in manifest['files']:
 f=ROOT/entry['path']
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=entry['sha256']:bad.append(entry['path'])
print(json.dumps({'verifiedFiles':len(manifest['files']),'changedOrMissing':bad},indent=2))
if bad:raise SystemExit(1)
if manifest.get('liveStages'):print('Snapshot excludes live output for stages:', ', '.join(manifest['liveStages']))
# Check every protocol-pinned numerical source even when a stage is still live.
for protocol_path in sorted(ROOT.glob('milestone-*-protocol.json')):
 protocol=json.loads(protocol_path.read_text());source_dir=ROOT/(protocol_path.name.replace('-protocol.json','-source'))
 hashes=protocol.get('sourceHashes')
 if not isinstance(hashes,dict):continue
 for rel,digest in hashes.items():
  source=source_dir/rel
  if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest()!=digest:raise SystemExit('Frozen source differs: '+str(source))

if args.stage=='31' and not args.skip_figures and importlib.util.find_spec('matplotlib') is None:
 raise SystemExit('Milestone 31 figures require matplotlib. Install milestone-31-source/plotting-requirements.txt with this Python, or use --skip-figures for numerical-only reproduction.')

if args.stage:
 dest=ROOT.parent/'work'/('reproduction-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
 shutil.copytree(ROOT,dest/'outputs');script={'07':'milestone-07-source/study.cjs','09-neighbors':'milestone-09-source/check-neighbors.mjs','10':'milestone-10-source/study.cjs','11':'milestone-11-source/study.cjs','12':'milestone-12-source/study.cjs','13':'milestone-13-source/study.cjs','14':'milestone-14-joint-source/study.cjs','14-first':'milestone-14-source/study.cjs','15':'milestone-15-source/diagnose.cjs','15-probes':'milestone-15-source/switch-probes.cjs','16':'milestone-16-source/study.cjs','17':'milestone-17-source/study.cjs','18':'milestone-18-source/study.cjs','18-development':'milestone-18-source/development.cjs','18-regression':'milestone-18-source/check-regression.cjs','18-stalls':'milestone-18-source/inspect-stalls.cjs','18-replay':'milestone-18-source/replay-diagnostic.cjs','refinement-audit':'milestone-18-source/refine-failures.cjs','19':'milestone-19-source/study.cjs','19-solver':'milestone-19-source/check-solver.cjs','20':'milestone-20-source/study.cjs','20-controls':'milestone-20-source/check-controls.cjs','20-replay':'milestone-20-source/build-replay.cjs','21':'milestone-21-source/study.cjs','21-delay':'milestone-21-source/check-delay.cjs','21-audit':'milestone-21-source/audit-failure.cjs','21-replay':'milestone-21-source/build-replay.cjs','22':'milestone-22-source/study.cjs','22-observer':'milestone-22-source/check-observer.cjs','22-audit':'milestone-22-source/audit-refinement.cjs','22-trace':'milestone-22-source/trace-refinement.cjs','23':'milestone-23-source/study.cjs','23-audit':'milestone-23-source/audit-raw-failures.cjs','24':'milestone-24-source/study.cjs','24-check':'milestone-24-source/check.cjs','25':'milestone-25-source/study.cjs','26':'milestone-26-source/study.cjs','26-check':'milestone-26-source/check.cjs','27':'milestone-27-source/study.cjs','27-check':'milestone-27-source/check-aero.cjs','28':'milestone-28-source/study.cjs','28-check':'milestone-28-source/check-aero.cjs','29':'milestone-29-source/study.cjs','30':'milestone-30-source/study.cjs','31':'milestone-31-source/study.cjs'}[args.stage]
 print('Isolated reproduction:',dest)
 if args.stage=='27' and (ROOT/'milestone-27-termination.json').exists():
  print('Reproducing only the20 completed erroneous-model cases; canceled refinements remain uncompleted. Use stage28 for corrected evidence.')
  completed=json.loads((ROOT/'milestone-27-progress.json').read_text());records=[]
  for previous in completed:
   job=previous['job'];subprocess.run([args.node,str(dest/'outputs'/script),'job',json.dumps(job)],cwd=dest,check=True)
   r=json.loads((dest/'outputs/milestone-27-source'/(job['id']+'.json')).read_text());records.append({k:v for k,v in r.items() if k not in ['initial','final','samples']})
  (dest/'outputs/milestone-27-progress.json').write_text(json.dumps(records,indent=2))
  (dest/'outputs/milestone-27-source/index.json').write_text(json.dumps([{'config':r['config'],'metrics':r['metrics'],'job':r['job'],'file':r['job']['id']+'.json','geometry':'factory-'+r['job']['course']+'.json'} for r in records]))
 else:
  if args.stage in ['30','31']:
   protocol30=json.loads((dest/('outputs/milestone-'+args.stage+'-protocol.json')).read_text())
   for job in protocol30['jobs']:
    for suffix in ['.json','.f64']:
     copied=dest/('outputs/milestone-'+args.stage+'-source')/(job['id']+suffix)
     if copied.exists():copied.unlink()
    if args.stage=='31':
     copied_source=dest/'outputs/milestone-31-source'
     for copied in list(copied_source.glob('checkpoint-'+job['id']+'-*.json'))+[copied_source/('progress-'+job['id']+'.json')]:
      if copied.exists():copied.unlink()
   if args.stage=='31':
    for copied in [dest/'outputs/milestone-31-progress.json',dest/'outputs/milestone-31-summary.json',dest/'outputs/milestone-31-source/index.json',dest/'outputs/milestone-31-passage.png',dest/'outputs/milestone-31-passage.pdf',dest/'outputs/milestone-31-figure-sources.json']:
     if copied.exists():copied.unlink()
  subprocess.run([args.node,str(dest/'outputs'/script)],cwd=dest,check=True)

 if args.stage=='20':
  subprocess.run([args.node,str(dest/'outputs/milestone-20-source/build-replay.cjs')],cwd=dest,check=True)
 if args.stage=='21':
  for extra in ['audit-failure.cjs','build-replay.cjs']:
   subprocess.run([args.node,str(dest/'outputs/milestone-21-source'/extra)],cwd=dest,check=True)

 if args.stage=='22':
  for extra in ['audit-refinement.cjs','trace-refinement.cjs']:
   subprocess.run([args.node,str(dest/'outputs/milestone-22-source'/extra)],cwd=dest,check=True)
 if args.stage=='23':
  subprocess.run([args.node,str(dest/'outputs/milestone-23-source/audit-raw-failures.cjs')],cwd=dest,check=True)

 if args.stage in ['26','27','28','29']:
  subprocess.run(['python3',str(dest/('outputs/milestone-'+args.stage+'-source/report.py'))],cwd=dest,check=True)
  subprocess.run(['python3',str(dest/('outputs/milestone-'+args.stage+'-source/audit.py'))],cwd=dest,check=True)
 if args.stage=='26':
  subprocess.run(['python3',str(dest/'outputs/milestone-26-source/supplement.py')],cwd=dest,check=True)
 if args.stage in ['27-check','28-check']:
  for extra in ['check-coupling.cjs','check-domain.cjs']:
   subprocess.run([args.node,str(dest/('outputs/milestone-'+args.stage[:2]+'-source')/extra)],cwd=dest,check=True)

 if args.stage=='28':
  subprocess.run(['python3',str(dest/'outputs/milestone-28-source/compare-correction.py')],cwd=dest,check=True)

 if args.stage=='31':
  subprocess.run([args.node,str(dest/'outputs/milestone-31-source/check.cjs')],cwd=dest,check=True)
  subprocess.run([args.node,str(dest/'outputs/milestone-31-source/audit-controls.cjs')],cwd=dest,check=True)
  subprocess.run(['python3',str(dest/'outputs/milestone-31-source/contact-analysis.py')],cwd=dest,check=True)
  if not args.skip_figures:
   subprocess.run([sys.executable,str(dest/'outputs/milestone-31-source/plot.py')],cwd=dest,check=True)
  subprocess.run(['python3',str(dest/'outputs/milestone-31-source/report.py')],cwd=dest,check=True)

 if args.stage=='30':
  subprocess.run([args.node,str(dest/'outputs/milestone-30-source/check.cjs')],cwd=dest,check=True)
  subprocess.run([args.node,str(dest/'outputs/milestone-30-source/check-reference.cjs')],cwd=dest,check=True)
  subprocess.run(['python3',str(dest/'outputs/milestone-30-source/report.py')],cwd=dest,check=True)

 if args.stage=='26':
  for count in ['1000','5000']:
   subprocess.run([args.node,str(dest/'outputs/milestone-26-source/diagnose-contact.cjs'),count],cwd=dest,check=True)
 if args.stage=='28':
  subprocess.run([args.node,str(dest/'outputs/milestone-28-source/check-control-authority.cjs')],cwd=dest,check=True)
